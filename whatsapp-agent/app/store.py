"""SQLite persistence: conversation history, de-duplication, pauses and rate limits."""

from __future__ import annotations

import sqlite3
import threading
import time
from pathlib import Path

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
