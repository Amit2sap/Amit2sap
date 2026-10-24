"""Owner daily digest: a short summary of the last 24 hours, sent on WhatsApp and/or e-mail."""

from __future__ import annotations

import asyncio
import logging
import re
import time
from datetime import datetime, timedelta, timezone

from .config import Settings
from .store import Store

log = logging.getLogger(__name__)

IST = timezone(timedelta(hours=5, minutes=30))

# Customer questions are stored as a topic only (never the text), for "top questions".
TOPIC_RULES: list[tuple[str, str]] = [
    ("Order status / tracking", r"\b(order|track|tracking|deliver|delivery|shipped|dispatch|awb|kab aayega)\b|#\d{3,}"),
    ("Bulk / corporate / wedding", r"\b(bulk|corporate|wholesale|reseller|resell|wedding|shaadi|shadi|return gifts?|employees|clients|jewell?ery|\d{2,}\s*(pcs|pieces|nos|units|boxes|hampers))\b"),
    ("Custom / branding", r"\b(custom|customi[sz]e|personali[sz]ed?|logo|branding|print|engrav)"),
    ("Returns / refunds / damage", r"\b(return|refund|damaged?|broken|exchange|cancel)"),
    ("Discounts / offers", r"\b(discount|offer|coupon|code|sale|diwali10)\b"),
    ("Shipping / delivery charges", r"\b(shipping|courier|pin ?code|pincode|charges?)\b"),
    ("Payment / COD", r"\b(cod|cash on delivery|payment|upi|pay)\b"),
    ("Price", r"\b(price|cost|rate|kitna|kitne|how much|₹|rs\.?)"),
    ("Product availability", r"\b(basket|tray|box|hamper|planter|mat|available|stock|have)\b"),
]


def classify_question(text: str) -> str:
    t = (text or "").lower()
    for topic, pattern in TOPIC_RULES:
        if re.search(pattern, t):
            return topic
    return "Other"


def digest_stats(store: Store, since: float, until: float) -> dict:
    return {
        "conversations": store.count_events("inbound", since, until, distinct_phone=True),
        "messages": store.count_events("inbound", since, until),
        "new_leads": store.count_events("lead", since, until),
        "escalations": store.count_events("escalation", since, until),
        "carts_recovered": store.count_events("cart_recovered", since, until),
        "opt_outs": store.count_events("opt_out", since, until),
        "opt_ins": store.count_events("opt_in", since, until),
        "templates_sent": store.count_events("template_sent", since, until),
        "top_questions": store.top_details("inbound", since, until, limit=5),
    }


def build_digest(store: Store, now: float | None = None, hours: int = 24) -> str:
    now = now or time.time()
    st = digest_stats(store, now - hours * 3600, now)
    day = datetime.fromtimestamp(now, IST).strftime("%d %b %Y")
    lines = [
        f"📊 *GrassCrafts daily digest* ({day}, last {hours} h)",
        f"💬 Conversations: {st['conversations']} ({st['messages']} messages)",
        f"🧺 New bulk/corporate leads: {st['new_leads']}",
        f"🔔 Escalations to you: {st['escalations']}",
        f"🛒 Abandoned carts recovered: {st['carts_recovered']}",
        f"🚫 Opt-outs: {st['opt_outs']}",
        f"📨 Automated messages sent: {st['templates_sent']}",
    ]
    if st["top_questions"]:
        lines.append("❓ Top questions:")
        lines += [f"  • {topic}: {n}" for topic, n in st["top_questions"]]
    else:
        lines.append("❓ Top questions: none")
    open_leads = [l for l in store.list_leads(200) if l["status"] == "new"]
    if open_leads:
        lines.append(f"\n👉 {len(open_leads)} lead(s) still marked *new*. See /admin to follow up.")
    return "\n".join(lines)


async def send_digest(settings: Settings, store: Store, whatsapp, email_sender=None, now: float | None = None) -> str:
    """Send the digest on the configured channels. Returns the digest text."""
    text = build_digest(store, now)
    channels = {c.strip().lower() for c in settings.digest_channels.split(",") if c.strip()}
    if "whatsapp" in channels and settings.owner_phone:
        try:
            if settings.owner_alert_template:
                await whatsapp.send_template(
                    settings.owner_phone,
                    settings.owner_alert_template,
                    settings.owner_alert_template_lang,
                    ["daily digest", text.split("\n", 1)[1] if "\n" in text else text],
                )
            else:
                await whatsapp.send_text(settings.owner_phone, text)
        except Exception:
            log.exception("digest WhatsApp send failed")
    if "email" in channels and settings.smtp_enabled and email_sender is not None:
        try:
            await asyncio.to_thread(email_sender, "GrassCrafts WhatsApp daily digest", text.replace("*", ""))
        except Exception:
            log.exception("digest e-mail failed")
    log.info("daily digest sent")
    return text
