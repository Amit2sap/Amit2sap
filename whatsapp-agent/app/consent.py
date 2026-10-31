"""Opt-in / opt-out handling and the send policy for business-initiated templates.

STOP / UNSUBSCRIBE / "band karo" opt a customer out of marketing; START opts them back in.
Opt-in is also recorded when a customer messages us first or ticks Shopify marketing consent.
"""

from __future__ import annotations

import re

from .config import Settings
from .store import Store

OPT_OUT_WORDS = {
    "stop",
    "unsubscribe",
    "stop all",
    "stop promotions",  # Meta's marketing-template quick-reply button
    "opt out",
    "optout",
    "band karo",
    "band kro",
    "bandh karo",
    "message band karo",
    "बंद करो",
    "बंद",
}
OPT_IN_WORDS = {"start", "subscribe", "opt in", "optin", "resume promotions", "chalu karo", "शुरू करो"}

OPT_OUT_REPLY = (
    "You're unsubscribed ✅ We won't send you offers or promotions on WhatsApp any more. "
    "You'll still get updates about orders you place. Reply START any time to subscribe again."
)
OPT_IN_REPLY = (
    "Welcome back! ✅ You're subscribed to GrassCrafts offers on WhatsApp. "
    "Reply STOP any time to unsubscribe."
)

MARKETING = "MARKETING"
UTILITY = "UTILITY"


def _normalise(text: str) -> str:
    # Strip ASCII punctuation, Devanagari danda and 🙏 only: \w would also drop Hindi vowel signs.
    t = re.sub(r"[!-/:-@\[-`{-~।॥🙏]+", " ", (text or "").lower())
    return " ".join(t.split())


def consent_command(text: str | None) -> str | None:
    """Return 'opt_out', 'opt_in' or None. Only a whole-message keyword counts, so
    "stop the order" or "when will it start shipping" are treated as normal questions."""
    t = _normalise(text or "")
    if not t:
        return None
    if t in OPT_OUT_WORDS:
        return "opt_out"
    if t in OPT_IN_WORDS:
        return "opt_in"
    return None


def can_send(store: Store, settings: Settings, phone: str, category: str) -> tuple[bool, str]:
    """May we send a template of this category to this number? Returns (allowed, reason)."""
    if not phone:
        return False, "no_phone"
    state = store.get_marketing(phone)
    if category == MARKETING:
        if state == "opted_out":
            return False, "opted_out"
        if settings.marketing_requires_opt_in and state != "opted_in":
            return False, "no_opt_in"
        return True, "ok"
    if settings.utility_requires_opt_in and state != "opted_in":
        return False, "no_opt_in"
    return True, "ok"
