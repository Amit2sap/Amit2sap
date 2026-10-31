"""SQLite persistence: conversation history, de-duplication, pauses and rate limits,
plus the automation data (leads, consent, Shopify checkouts, scheduled jobs, send log, stats)."""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from pathlib import Path
from typing import Any

LEAD_STATUSES = ("new", "contacted", "won", "lost")
LEAD_FIELDS = (
    "name",
    "company",
    "city",
    "lead_type",
    "product_interest",
    "quantity",
    "budget_per_piece",
    "needed_by",
    "customisation",
    "email",
    "notes",
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_messages_phone_ts ON messages (phone, ts);

CREATE TABLE IF NOT EXISTS processed (
    message_id TEXT PRIMARY KEY,
    ts REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS paused (
    phone TEXT PRIMARY KEY,
    ts REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS hits (
    phone TEXT NOT NULL,
    ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_hits_phone_ts ON hits (phone, ts);

-- Bulk / corporate leads captured by the bot.
CREATE TABLE IF NOT EXISTS leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    phone TEXT NOT NULL,
    name TEXT, company TEXT, city TEXT, lead_type TEXT,
    product_interest TEXT, quantity TEXT, budget_per_piece TEXT, needed_by TEXT,
    customisation TEXT, email TEXT, notes TEXT,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'won', 'lost')),
    created_ts REAL NOT NULL,
    updated_ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_leads_phone ON leads (phone);

-- Marketing consent per WhatsApp number: unknown | opted_in | opted_out.
CREATE TABLE IF NOT EXISTS contacts (
    phone TEXT PRIMARY KEY,
    name TEXT,
    marketing TEXT NOT NULL DEFAULT 'unknown',
    source TEXT,
    updated_ts REAL NOT NULL
);

-- Shopify checkouts (for abandoned-cart reminders).
CREATE TABLE IF NOT EXISTS checkouts (
    token TEXT PRIMARY KEY,
    phone TEXT,
    first_name TEXT,
    cart_url TEXT,
    total TEXT,
    completed INTEGER NOT NULL DEFAULT 0,
    reminded INTEGER NOT NULL DEFAULT 0,
    updated_ts REAL NOT NULL
);

-- Shopify orders seen through webhooks (phone lookup for shipping updates).
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    name TEXT,
    phone TEXT,
    first_name TEXT,
    checkout_token TEXT,
    ts REAL NOT NULL
);

-- Persistent work queue for the background scheduler. One row per unique key.
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    key TEXT NOT NULL UNIQUE,
    due_ts REAL NOT NULL,
    payload TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    attempts INTEGER NOT NULL DEFAULT 0,
    result TEXT,
    created_ts REAL NOT NULL,
    done_ts REAL
);
CREATE INDEX IF NOT EXISTS idx_jobs_due ON jobs (status, due_ts);

-- Every business-initiated message, keyed so nothing is ever sent twice.
CREATE TABLE IF NOT EXISTS sent_log (
    key TEXT PRIMARY KEY,
    phone TEXT NOT NULL,
    template TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT NOT NULL,
    detail TEXT,
    ts REAL NOT NULL
);

-- Small event log for the digest and the dashboard (no message text).
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kind TEXT NOT NULL,
    phone TEXT,
    detail TEXT,
    ts REAL NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_events_kind_ts ON events (kind, ts);

-- One row per recipient per broadcast run (python -m app.broadcast --confirm).
CREATE TABLE IF NOT EXISTS broadcast_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    campaign TEXT NOT NULL,
    template TEXT NOT NULL,
    phone TEXT NOT NULL,
    status TEXT NOT NULL,
    ts REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
"""


class Store:
    def __init__(self, path: str, history_turns: int = 20, ttl_hours: int = 24):
        if path != ":memory:":
            Path(path).parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.executescript(SCHEMA)
        self._lock = threading.Lock()
        self.history_turns = history_turns
        self.ttl_seconds = ttl_hours * 3600

    def close(self) -> None:
        self._conn.close()

    # ---------------------------------------------------------------- dedupe
    def mark_processed(self, message_id: str) -> bool:
        """Record a message id. Returns False if it was already seen (a Meta retry)."""
        with self._lock:
            cur = self._conn.execute(
                "INSERT OR IGNORE INTO processed (message_id, ts) VALUES (?, ?)",
                (message_id, time.time()),
            )
            return cur.rowcount == 1

    # --------------------------------------------------------------- history
    def append(self, phone: str, role: str, content: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO messages (phone, role, content, ts) VALUES (?, ?, ?, ?)",
                (phone, role, content, time.time()),
            )

    def history(self, phone: str) -> list[dict]:
        """Last N turns from the past 24h as Messages API params.

        The list always starts with a user message and alternates roles
        (consecutive same-role messages are merged).
        """
        cutoff = time.time() - self.ttl_seconds
        with self._lock:
            rows = self._conn.execute(
                "SELECT role, content FROM messages WHERE phone = ? AND ts >= ? "
                "ORDER BY id DESC LIMIT ?",
                (phone, cutoff, self.history_turns * 2),
            ).fetchall()
        rows.reverse()
        out: list[dict] = []
        for role, content in rows:
            if not out and role != "user":
                continue
            if out and out[-1]["role"] == role:
                out[-1]["content"] += "\n" + content
            else:
                out.append({"role": role, "content": content})
        return out

    def clear_history(self, phone: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM messages WHERE phone = ?", (phone,))

    # ---------------------------------------------------------------- pauses
    def pause(self, phone: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO paused (phone, ts) VALUES (?, ?)", (phone, time.time())
            )

    def resume(self, phone: str) -> None:
        with self._lock:
            self._conn.execute("DELETE FROM paused WHERE phone = ?", (phone,))

    def is_paused(self, phone: str) -> bool:
        with self._lock:
            return (
                self._conn.execute("SELECT 1 FROM paused WHERE phone = ?", (phone,)).fetchone()
                is not None
            )

    def paused_list(self) -> list[str]:
        with self._lock:
            return [r[0] for r in self._conn.execute("SELECT phone FROM paused ORDER BY ts")]

    # ------------------------------------------------------------ rate limit
    def hit(self, phone: str, window_seconds: int = 3600) -> int:
        """Record one inbound message; return how many arrived in the window (including this one)."""
        now = time.time()
        with self._lock:
            self._conn.execute("INSERT INTO hits (phone, ts) VALUES (?, ?)", (phone, now))
            return self._conn.execute(
                "SELECT COUNT(*) FROM hits WHERE phone = ? AND ts >= ?",
                (phone, now - window_seconds),
            ).fetchone()[0]

    # --------------------------------------------------------------- cleanup
    def prune(self) -> None:
        now = time.time()
        with self._lock:
            self._conn.execute("DELETE FROM messages WHERE ts < ?", (now - self.ttl_seconds,))
            self._conn.execute("DELETE FROM processed WHERE ts < ?", (now - 7 * 86400,))
            self._conn.execute("DELETE FROM hits WHERE ts < ?", (now - 2 * 3600,))
            self._conn.execute("DELETE FROM events WHERE ts < ?", (now - 90 * 86400,))
            self._conn.execute(
                "DELETE FROM jobs WHERE status != 'pending' AND created_ts < ?", (now - 90 * 86400,)
            )
            self._conn.execute(
                "DELETE FROM checkouts WHERE updated_ts < ?", (now - 60 * 86400,)
            )

    def _rows(self, sql: str, params: tuple = ()) -> list[dict]:
        with self._lock:
            cur = self._conn.execute(sql, params)
            cols = [c[0] for c in cur.description]
            return [dict(zip(cols, r)) for r in cur.fetchall()]

    def _one(self, sql: str, params: tuple = ()) -> dict | None:
        rows = self._rows(sql, params)
        return rows[0] if rows else None

    # ----------------------------------------------------------------- leads
    def save_lead(self, phone: str, fields: dict[str, Any], now: float | None = None) -> tuple[int, bool]:
        """Create a lead, or fill in the open lead from the same number in the last 30 days.

        Returns (lead_id, created). Empty values never overwrite saved ones.
        """
        now = now or time.time()
        clean = {
            k: str(v).strip()[:500]
            for k, v in fields.items()
            if k in LEAD_FIELDS and v not in (None, "") and str(v).strip()
        }
        with self._lock:
            row = self._conn.execute(
                "SELECT id FROM leads WHERE phone = ? AND status IN ('new', 'contacted') "
                "AND updated_ts >= ? ORDER BY id DESC LIMIT 1",
                (phone, now - 30 * 86400),
            ).fetchone()
            if row:
                if clean:
                    sets = ", ".join(f"{k} = ?" for k in clean)
                    self._conn.execute(
                        f"UPDATE leads SET {sets}, updated_ts = ? WHERE id = ?",
                        (*clean.values(), now, row[0]),
                    )
                return row[0], False
            cols = ", ".join(clean)
            marks = ", ".join("?" for _ in clean)
            sql = (
                f"INSERT INTO leads (phone, {cols + ', ' if cols else ''}status, created_ts, updated_ts) "
                f"VALUES (?, {marks + ', ' if marks else ''}'new', ?, ?)"
            )
            cur = self._conn.execute(sql, (phone, *clean.values(), now, now))
            return int(cur.lastrowid), True

    def get_lead(self, lead_id: int) -> dict | None:
        return self._one("SELECT * FROM leads WHERE id = ?", (lead_id,))

    def list_leads(self, limit: int = 500) -> list[dict]:
        return self._rows("SELECT * FROM leads ORDER BY id DESC LIMIT ?", (limit,))

    def set_lead_status(self, lead_id: int, status: str) -> bool:
        if status not in LEAD_STATUSES:
            return False
        with self._lock:
            cur = self._conn.execute(
                "UPDATE leads SET status = ?, updated_ts = ? WHERE id = ?",
                (status, time.time(), lead_id),
            )
            return cur.rowcount == 1

    # --------------------------------------------------------------- consent
    def get_marketing(self, phone: str) -> str:
        row = self._one("SELECT marketing FROM contacts WHERE phone = ?", (phone,))
        return row["marketing"] if row else "unknown"

    def set_marketing(self, phone: str, state: str, source: str, name: str | None = None) -> None:
        """Explicit change (STOP / START)."""
        with self._lock:
            self._conn.execute(
                "INSERT INTO contacts (phone, name, marketing, source, updated_ts) VALUES (?, ?, ?, ?, ?) "
                "ON CONFLICT(phone) DO UPDATE SET marketing = excluded.marketing, "
                "source = excluded.source, updated_ts = excluded.updated_ts, "
                "name = COALESCE(excluded.name, contacts.name)",
                (phone, name, state, source, time.time()),
            )

    def record_opt_in(self, phone: str, source: str, name: str | None = None) -> bool:
        """Implicit opt-in (customer messaged us, or ticked Shopify marketing consent).

        Never overrides an earlier opt-out. Returns True if the number is now opted in.
        """
        with self._lock:
            self._conn.execute(
                "INSERT INTO contacts (phone, name, marketing, source, updated_ts) "
                "VALUES (?, ?, 'opted_in', ?, ?) "
                "ON CONFLICT(phone) DO UPDATE SET "
                "name = COALESCE(excluded.name, contacts.name), "
                "source = CASE WHEN contacts.marketing = 'unknown' THEN excluded.source ELSE contacts.source END, "
                "marketing = CASE WHEN contacts.marketing = 'unknown' THEN 'opted_in' ELSE contacts.marketing END",
                (phone, name, source, time.time()),
            )
        return self.get_marketing(phone) == "opted_in"

    def remember_name(self, phone: str, name: str | None) -> None:
        if not name:
            return
        with self._lock:
            self._conn.execute(
                "INSERT INTO contacts (phone, name, updated_ts) VALUES (?, ?, ?) "
                "ON CONFLICT(phone) DO UPDATE SET name = excluded.name",
                (phone, name, time.time()),
            )

    def segment(self, name: str) -> list[dict]:
        if name == "opted_in":
            return self._rows(
                "SELECT phone, name FROM contacts WHERE marketing = 'opted_in' ORDER BY phone"
            )
        raise ValueError(f"Unknown segment '{name}'")

    # ------------------------------------------------------- shopify mirror
    def upsert_checkout(
        self,
        token: str,
        phone: str,
        first_name: str | None,
        cart_url: str | None,
        total: str | None,
        completed: bool,
        now: float | None = None,
    ) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO checkouts (token, phone, first_name, cart_url, total, completed, updated_ts) "
                "VALUES (?, ?, ?, ?, ?, ?, ?) ON CONFLICT(token) DO UPDATE SET "
                "phone = COALESCE(NULLIF(excluded.phone, ''), checkouts.phone), "
                "first_name = COALESCE(excluded.first_name, checkouts.first_name), "
                "cart_url = COALESCE(excluded.cart_url, checkouts.cart_url), "
                "total = COALESCE(excluded.total, checkouts.total), "
                "completed = MAX(checkouts.completed, excluded.completed), "
                "updated_ts = excluded.updated_ts",
                (token, phone, first_name, cart_url, total, int(completed), now or time.time()),
            )

    def get_checkout(self, token: str) -> dict | None:
        return self._one("SELECT * FROM checkouts WHERE token = ?", (token,))

    def complete_checkout(self, token: str) -> bool:
        """Mark a checkout as paid. Returns True if a reminder had been sent for it (recovered cart)."""
        with self._lock:
            self._conn.execute("UPDATE checkouts SET completed = 1 WHERE token = ?", (token,))
            row = self._conn.execute(
                "SELECT reminded FROM checkouts WHERE token = ?", (token,)
            ).fetchone()
        return bool(row and row[0])

    def mark_checkout_reminded(self, token: str) -> None:
        with self._lock:
            self._conn.execute("UPDATE checkouts SET reminded = 1 WHERE token = ?", (token,))

    def save_order(
        self, order_id: str, name: str, phone: str, first_name: str | None, checkout_token: str | None
    ) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO orders (order_id, name, phone, first_name, checkout_token, ts) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, name, phone, first_name, checkout_token, time.time()),
            )

    def get_order(self, order_id: str) -> dict | None:
        return self._one("SELECT * FROM orders WHERE order_id = ?", (order_id,))

    # ------------------------------------------------------------------ jobs
    def schedule(self, kind: str, key: str, due_ts: float, payload: dict, reschedule: bool = False) -> bool:
        """Queue a job once per key. With reschedule=True a still-pending job gets the new due time."""
        with self._lock:
            if reschedule:
                cur = self._conn.execute(
                    "INSERT INTO jobs (kind, key, due_ts, payload, created_ts) VALUES (?, ?, ?, ?, ?) "
                    "ON CONFLICT(key) DO UPDATE SET due_ts = excluded.due_ts, payload = excluded.payload "
                    "WHERE jobs.status = 'pending'",
                    (kind, key, due_ts, json.dumps(payload), time.time()),
                )
            else:
                cur = self._conn.execute(
                    "INSERT OR IGNORE INTO jobs (kind, key, due_ts, payload, created_ts) VALUES (?, ?, ?, ?, ?)",
                    (kind, key, due_ts, json.dumps(payload), time.time()),
                )
            return cur.rowcount == 1

    def claim_due_jobs(self, now: float, limit: int = 50) -> list[dict]:
        """Atomically move due jobs from pending to running and return them."""
        with self._lock:
            rows = self._conn.execute(
                "SELECT id, kind, key, payload, attempts FROM jobs WHERE status = 'pending' AND due_ts <= ? "
                "ORDER BY due_ts LIMIT ?",
                (now, limit),
            ).fetchall()
            claimed = []
            for jid, kind, key, payload, attempts in rows:
                cur = self._conn.execute(
                    "UPDATE jobs SET status = 'running' WHERE id = ? AND status = 'pending'", (jid,)
                )
                if cur.rowcount == 1:
                    claimed.append(
                        {"id": jid, "kind": kind, "key": key, "payload": json.loads(payload), "attempts": attempts}
                    )
            return claimed

    def finish_job(self, job_id: int, status: str, result: str = "") -> None:
        with self._lock:
            self._conn.execute(
                "UPDATE jobs SET status = ?, result = ?, done_ts = ? WHERE id = ?",
                (status, result[:300], time.time(), job_id),
            )

    def retry_job(self, job_id: int, due_ts: float, error: str) -> None:
        with self._lock:
            self._conn.execute(
                "UPDATE jobs SET status = 'pending', attempts = attempts + 1, due_ts = ?, result = ? WHERE id = ?",
                (due_ts, error[:300], job_id),
            )

    def reset_running_jobs(self) -> None:
        """After a restart, jobs left 'running' go back to the queue (sent_log stops double sends)."""
        with self._lock:
            self._conn.execute("UPDATE jobs SET status = 'pending' WHERE status = 'running'")

    def jobs(self, key_prefix: str = "") -> list[dict]:
        return self._rows("SELECT * FROM jobs WHERE key LIKE ? ORDER BY id", (key_prefix + "%",))

    # -------------------------------------------------------------- send log
    def claim_send(self, key: str, phone: str, template: str, category: str) -> bool:
        """Reserve a send. Returns False if this key was already sent (or is being sent)."""
        with self._lock:
            cur = self._conn.execute(
                "INSERT OR IGNORE INTO sent_log (key, phone, template, category, status, ts) "
                "VALUES (?, ?, ?, ?, 'sending', ?)",
                (key, phone, template, category, time.time()),
            )
            return cur.rowcount == 1

    def finish_send(self, key: str, status: str, detail: str = "") -> None:
        with self._lock:
            self._conn.execute(
                "UPDATE sent_log SET status = ?, detail = ?, ts = ? WHERE key = ?",
                (status, detail[:300], time.time(), key),
            )

    def release_send(self, key: str) -> None:
        """Forget a failed send so it can be retried."""
        with self._lock:
            self._conn.execute("DELETE FROM sent_log WHERE key = ?", (key,))

    def sent(self, key_prefix: str = "") -> list[dict]:
        return self._rows("SELECT * FROM sent_log WHERE key LIKE ? ORDER BY ts", (key_prefix + "%",))

    # ---------------------------------------------------------------- events
    def log_event(self, kind: str, phone: str | None = None, detail: str = "", now: float | None = None) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO events (kind, phone, detail, ts) VALUES (?, ?, ?, ?)",
                (kind, phone, detail[:200], now or time.time()),
            )

    def count_events(self, kind: str, since: float, until: float | None = None, distinct_phone: bool = False) -> int:
        what = "COUNT(DISTINCT phone)" if distinct_phone else "COUNT(*)"
        with self._lock:
            return self._conn.execute(
                f"SELECT {what} FROM events WHERE kind = ? AND ts >= ? AND ts < ?",
                (kind, since, until or time.time() + 1),
            ).fetchone()[0]

    def top_details(self, kind: str, since: float, until: float | None = None, limit: int = 5) -> list[tuple[str, int]]:
        with self._lock:
            return self._conn.execute(
                "SELECT detail, COUNT(*) AS n FROM events WHERE kind = ? AND ts >= ? AND ts < ? "
                "GROUP BY detail ORDER BY n DESC, detail LIMIT ?",
                (kind, since, until or time.time() + 1, limit),
            ).fetchall()

    def recent_conversations(self, limit: int = 30) -> list[dict]:
        return self._rows(
            "SELECT phone, COUNT(*) AS messages, MAX(ts) AS last_ts FROM messages "
            "GROUP BY phone ORDER BY last_ts DESC LIMIT ?",
            (limit,),
        )

    # ------------------------------------------------------------- broadcast
    def log_broadcast(self, campaign: str, template: str, phone: str, status: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT INTO broadcast_log (campaign, template, phone, status, ts) VALUES (?, ?, ?, ?, ?)",
                (campaign, template, phone, status[:200], time.time()),
            )

    def broadcast_results(self, campaign: str) -> list[dict]:
        return self._rows("SELECT * FROM broadcast_log WHERE campaign = ? ORDER BY id", (campaign,))

    # ------------------------------------------------------------------ meta
    def get_meta(self, key: str) -> str | None:
        row = self._one("SELECT value FROM meta WHERE key = ?", (key,))
        return row["value"] if row else None

    def set_meta(self, key: str, value: str) -> None:
        with self._lock:
            self._conn.execute(
                "INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value)
            )

    def claim_meta(self, key: str, value: str) -> bool:
        """Set key to value unless it already has that value. True if this call changed it."""
        with self._lock:
            row = self._conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
            if row and row[0] == value:
                return False
            self._conn.execute("INSERT OR REPLACE INTO meta (key, value) VALUES (?, ?)", (key, value))
            return True
