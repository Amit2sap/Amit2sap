"""Minimal server-rendered admin dashboard behind HTTP Basic auth (ADMIN_USER / ADMIN_PASSWORD).

GET  /admin                       leads, recent conversations, paused chats, stats
POST /admin/leads/{id}/status     change a lead's status (plain HTML form)
GET  /admin/leads.csv             all leads as CSV
"""

from __future__ import annotations

import csv
import hashlib
import hmac
import io
import time
from datetime import datetime
from html import escape
from typing import Callable
from urllib.parse import parse_qs

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from .config import Settings, mask_phone
from .digest import IST, digest_stats
from .store import LEAD_FIELDS, LEAD_STATUSES, Store

security = HTTPBasic(auto_error=False)

CSV_COLUMNS = ["id", "status", "created", "phone", *LEAD_FIELDS]

STYLE = """
body{font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f7f5ef;color:#2b2a26}
header{background:#3f5a36;color:#fff;padding:14px 20px}header h1{margin:0;font-size:20px}
main{padding:16px 20px;max-width:1200px}
section{background:#fff;border:1px solid #e3dfd3;border-radius:8px;padding:12px 16px;margin:0 0 16px}
h2{font-size:16px;margin:4px 0 10px}table{border-collapse:collapse;width:100%;font-size:13px}
th,td{border-bottom:1px solid #eee;padding:6px;text-align:left;vertical-align:top}
th{background:#faf8f2}.wrap{overflow-x:auto}.muted{color:#777}
.stats{display:flex;flex-wrap:wrap;gap:10px}.stat{border:1px solid #e3dfd3;border-radius:6px;padding:8px 12px;min-width:120px}
.stat b{display:block;font-size:20px}.s-new{color:#b45309}.s-contacted{color:#1d4ed8}.s-won{color:#15803d}.s-lost{color:#777}
select,button{font-size:13px}a{color:#3f5a36}
"""


def _fmt_ts(ts: float | None) -> str:
    return datetime.fromtimestamp(ts, IST).strftime("%d %b %H:%M") if ts else ""


def build_admin_router(settings: Settings, get_store: Callable[[], Store]) -> APIRouter:
    router = APIRouter()

    def csrf_token() -> str:
        return hmac.new(settings.admin_password.encode(), b"grasscrafts-admin-csrf", hashlib.sha256).hexdigest()

    def require_admin(credentials: HTTPBasicCredentials | None = Depends(security)) -> str:
        if not settings.admin_password:
            raise HTTPException(status_code=404, detail="Admin dashboard is disabled (set ADMIN_PASSWORD).")
        ok = credentials is not None and (
            hmac.compare_digest(credentials.username.encode(), settings.admin_user.encode())
            & hmac.compare_digest(credentials.password.encode(), settings.admin_password.encode())
        )
        if not ok:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
                headers={"WWW-Authenticate": 'Basic realm="GrassCrafts admin"'},
            )
        return credentials.username

    @router.get("/admin", response_class=HTMLResponse)
    def dashboard(_: str = Depends(require_admin)) -> HTMLResponse:
        store = get_store()
        now = time.time()
        day, week = digest_stats(store, now - 86400, now), digest_stats(store, now - 7 * 86400, now)
        leads = store.list_leads(200)
        paused = set(store.paused_list())
        token = csrf_token()

        def stat(label: str, key: str) -> str:
            return f'<div class="stat"><span class="muted">{escape(label)}</span><b>{day[key]}</b><span class="muted">7 days: {week[key]}</span></div>'

        stats_html = "".join(
            stat(label, key)
            for label, key in (
                ("Conversations (24 h)", "conversations"),
                ("Messages in", "messages"),
                ("New leads", "new_leads"),
                ("Escalations", "escalations"),
                ("Carts recovered", "carts_recovered"),
                ("Opt-outs", "opt_outs"),
                ("Automated sends", "templates_sent"),
            )
        )
        topics = ", ".join(f"{escape(t)} ({n})" for t, n in week["top_questions"]) or "none yet"

        lead_rows = []
        for l in leads:
            options = "".join(
                f'<option value="{s}"{" selected" if s == l["status"] else ""}>{s}</option>' for s in LEAD_STATUSES
            )
            details = "<br>".join(
                f"<span class='muted'>{escape(k.replace('_', ' '))}:</span> {escape(str(l[k]))}"
                for k in ("product_interest", "quantity", "budget_per_piece", "needed_by", "customisation", "notes")
                if l.get(k)
            )
            lead_rows.append(
                "<tr>"
                f"<td>#{l['id']}<br><span class='muted'>{_fmt_ts(l['created_ts'])}</span></td>"
                f"<td>{escape(l.get('name') or '')}<br>{escape(l.get('company') or '')}<br>"
                f"<span class='muted'>{escape(l.get('city') or '')}</span></td>"
                f"<td><a href=\"https://wa.me/{escape(l['phone'])}\">+{escape(l['phone'])}</a><br>{escape(l.get('email') or '')}</td>"
                f"<td>{escape(l.get('lead_type') or '')}</td><td>{details}</td>"
                f"<td class='s-{escape(l['status'])}'><form method='post' action='/admin/leads/{l['id']}/status'>"
                f"<input type='hidden' name='csrf' value='{token}'><select name='status'>{options}</select> "
                "<button type='submit'>Save</button></form></td>"
                "</tr>"
            )
        leads_html = (
            "<table><tr><th>Lead</th><th>Name / company</th><th>Contact</th><th>Type</th><th>Details</th><th>Status</th></tr>"
            + "".join(lead_rows)
            + "</table>"
            if lead_rows
            else "<p class='muted'>No leads yet.</p>"
        )

        conv_rows = "".join(
            f"<tr><td>{escape(mask_phone(c['phone']))}</td><td>{c['messages']}</td>"
            f"<td>{_fmt_ts(c['last_ts'])}</td><td>{'paused' if c['phone'] in paused else ''}</td></tr>"
            for c in store.recent_conversations(30)
        )
        conv_html = (
            "<table><tr><th>Customer</th><th>Messages (24 h memory)</th><th>Last activity</th><th></th></tr>"
            + conv_rows
            + "</table>"
            if conv_rows
            else "<p class='muted'>No conversations in the last 24 hours.</p>"
        )
        paused_html = (
            "<ul>" + "".join(f"<li>+{escape(p)} <span class='muted'>(/resume {escape(p)})</span></li>" for p in sorted(paused)) + "</ul>"
            if paused
            else "<p class='muted'>No paused chats.</p>"
        )
        html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>GrassCrafts admin</title>
<style>{STYLE}</style></head><body><header><h1>GrassCrafts WhatsApp assistant</h1></header><main>
<section><h2>Message stats</h2><div class="stats">{stats_html}</div>
<p class="muted">Top questions (7 days): {topics}</p></section>
<section><h2>Leads ({len(leads)}) <a href="/admin/leads.csv" style="font-size:13px">Download CSV</a></h2>
<div class="wrap">{leads_html}</div></section>
<section><h2>Recent conversations</h2><div class="wrap">{conv_html}</div></section>
<section><h2>Paused chats</h2>{paused_html}</section>
</main></body></html>"""
        return HTMLResponse(html, headers={"Cache-Control": "no-store"})

    @router.post("/admin/leads/{lead_id}/status")
    async def update_status(lead_id: int, request: Request, _: str = Depends(require_admin)):
        form = parse_qs((await request.body()).decode("utf-8", "replace"))
        status = (form.get("status") or [""])[0]
        if not hmac.compare_digest((form.get("csrf") or [""])[0], csrf_token()):
            raise HTTPException(status_code=403, detail="Invalid form token; reload the page.")
        if status not in LEAD_STATUSES:
            raise HTTPException(status_code=400, detail="Unknown status")
        if not get_store().set_lead_status(lead_id, status):
            raise HTTPException(status_code=404, detail="Lead not found")
        return RedirectResponse("/admin", status_code=303)

    @router.get("/admin/leads.csv")
    def leads_csv(_: str = Depends(require_admin)) -> Response:
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(CSV_COLUMNS)
        for l in get_store().list_leads(100000):
            # Customer-typed text is prefixed with ' if it could run as a spreadsheet formula.
            fields = [l.get(k) or "" for k in LEAD_FIELDS]
            fields = [("'" + v) if v[:1] in ("=", "+", "-", "@") else v for v in fields]
            writer.writerow([l["id"], l["status"], _fmt_ts(l["created_ts"]), "+" + l["phone"], *fields])
        return Response(
            "﻿" + buf.getvalue(),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": 'attachment; filename="grasscrafts-leads.csv"',
                "Cache-Control": "no-store",
            },
        )

    return router
