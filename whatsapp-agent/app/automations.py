"""Shopify webhook automations: order confirmations, shipping updates, abandoned-cart
reminders and review requests.

Webhooks only write to SQLite and queue jobs; the scheduler (app/scheduler.py) sends them.
Every business-initiated message goes through ``Notifier.send_template_once``, which checks
consent and records a unique key in ``sent_log`` so nothing is ever sent twice.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from .config import Settings, mask_phone, normalize_phone
from .consent import MARKETING, UTILITY, can_send
from .store import Store
from .whatsapp import WhatsAppClient

log = logging.getLogger(__name__)

# Template name -> category. Names match templates/whatsapp_templates.json.
TEMPLATE_CATEGORY = {
    "order_confirmation": UTILITY,
    "order_shipped": UTILITY,
    "abandoned_cart": MARKETING,
    "review_request": MARKETING,
    "owner_alert": UTILITY,
    "diwali_offer": MARKETING,
}

TOPICS = {"orders/create", "fulfillments/create", "checkouts/create", "checkouts/update"}


# ------------------------------------------------------------- payload helpers
def _first(*values: Any) -> str:
    for v in values:
        if v not in (None, ""):
            return str(v)
    return ""


def _addr(payload: dict, key: str) -> dict:
    return payload.get(key) or {}


def payload_phone(payload: dict, cc: str = "91") -> str:
    """Best phone for a Shopify order / checkout / fulfillment payload, normalised."""
    customer = payload.get("customer") or {}
    raw = _first(
        payload.get("phone"),
        _addr(payload, "shipping_address").get("phone"),
        _addr(payload, "billing_address").get("phone"),
        customer.get("phone"),
        _addr(customer, "default_address").get("phone"),
        _addr(payload, "destination").get("phone"),
    )
    phone = normalize_phone(raw, cc)
    return phone if len(phone) >= 11 else ""


def payload_first_name(payload: dict) -> str:
    customer = payload.get("customer") or {}
    return _first(
        customer.get("first_name"),
        _addr(payload, "shipping_address").get("first_name"),
        _addr(payload, "billing_address").get("first_name"),
        _addr(payload, "destination").get("first_name"),
    ).strip() or "there"


def accepts_marketing(payload: dict) -> bool:
    customer = payload.get("customer") or {}
    if payload.get("buyer_accepts_marketing") or customer.get("accepts_marketing"):
        return True
    for key in ("sms_marketing_consent", "email_marketing_consent"):
        consent = customer.get(key) or payload.get(key) or {}
        if (consent.get("state") or "").lower() == "subscribed":
            return True
    return False


def money(amount: Any, currency: str | None) -> str:
    try:
        value = float(amount)
    except (TypeError, ValueError):
        return str(amount or "")
    if (currency or "INR").upper() == "INR":
        return f"₹{value:,.0f}" if value == int(value) else f"₹{value:,.2f}"
    return f"{currency} {value:,.2f}"


def parse_ts(value: Any, default: float) -> float:
    from datetime import datetime

    if not value:
        return default
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()
    except ValueError:
        return default


# --------------------------------------------------------------------- sender
class Notifier:
    def __init__(self, settings: Settings, store: Store, whatsapp: WhatsAppClient):
        self.settings = settings
        self.store = store
        self.whatsapp = whatsapp

    async def send_template_once(
        self, key: str, phone: str, template: str, params: list[str], category: str | None = None
    ) -> str:
        """Send a template unless policy forbids it or this key was already sent.

        Returns 'sent', 'duplicate' or 'skipped:<reason>'. Raises if the WhatsApp call fails
        (the claim is released so the job can retry).
        """
        category = category or TEMPLATE_CATEGORY.get(template, MARKETING)
        allowed, reason = can_send(self.store, self.settings, phone, category)
        if not allowed:
            log.info("skip %s to=%s: %s", template, mask_phone(phone), reason)
            return f"skipped:{reason}"
        if not self.store.claim_send(key, phone, template, category):
            return "duplicate"
        try:
            resp = await self.whatsapp.send_template(phone, template, self.settings.template_lang, params)
        except Exception as exc:
            self.store.release_send(key)
            raise RuntimeError(f"send failed: {type(exc).__name__}") from exc
        msg_id = ""
        if isinstance(resp, dict):
            msg_id = ((resp.get("messages") or [{}])[0] or {}).get("id", "")
        self.store.finish_send(key, "sent", msg_id)
        self.store.log_event("template_sent", phone, template)
        log.info("sent template %s to=%s", template, mask_phone(phone))
        return "sent"


# ------------------------------------------------------------ shopify handling
class ShopifyAutomations:
    def __init__(self, settings: Settings, store: Store, notifier: Notifier):
        self.settings = settings
        self.store = store
        self.notifier = notifier

    # Webhook side: fast, database only. ---------------------------------------
    def handle_webhook(self, topic: str, payload: dict, now: float | None = None) -> str:
        now = now or time.time()
        if topic == "orders/create":
            return self._order_created(payload, now)
        if topic == "fulfillments/create":
            return self._fulfillment_created(payload, now)
        if topic in {"checkouts/create", "checkouts/update"}:
            return self._checkout(payload, now)
        return "ignored"

    def _record_consent(self, payload: dict, phone: str) -> None:
        if phone and accepts_marketing(payload):
            self.store.record_opt_in(phone, "shopify", payload_first_name(payload))

    def _order_created(self, payload: dict, now: float) -> str:
        s = self.settings
        order_id = str(payload.get("id") or "")
        name = str(payload.get("name") or (f"#{payload['order_number']}" if payload.get("order_number") else ""))
        phone = payload_phone(payload, s.default_country_code)
        first = payload_first_name(payload)
        token = str(payload.get("checkout_token") or "")
        if not order_id:
            return "ignored"
        self.store.save_order(order_id, name, phone, first, token or None)
        self._record_consent(payload, phone)
        if token and self.store.complete_checkout(token):
            self.store.log_event("cart_recovered", phone, name, now=now)
        if s.order_confirmation_enabled and phone:
            total = money(payload.get("total_price"), payload.get("currency"))
            self.store.schedule(
                "order_confirmation",
                f"order_confirmation:{order_id}",
                now,
                {"phone": phone, "params": [first, name, total]},
            )
        return "ok"

    def _fulfillment_created(self, payload: dict, now: float) -> str:
        s = self.settings
        fid = str(payload.get("id") or "")
        order_id = str(payload.get("order_id") or "")
        if not fid:
            return "ignored"
        order = self.store.get_order(order_id) or {}
        phone = payload_phone(payload, s.default_country_code) or order.get("phone") or ""
        first = order.get("first_name") or payload_first_name(payload)
        order_name = order.get("name") or str(payload.get("name") or "").split(".")[0]
        if not phone:
            return "no_phone"
        if s.shipping_update_enabled:
            company = _first(payload.get("tracking_company"), "our courier partner")
            tracking = _first(
                payload.get("tracking_url"),
                (payload.get("tracking_urls") or [None])[0],
                payload.get("tracking_number"),
                f"{s.storefront_base_url}/account",
            )
            self.store.schedule(
                "order_shipped",
                f"order_shipped:{fid}",
                now,
                {"phone": phone, "params": [first, order_name, company, tracking]},
            )
        if s.review_request_enabled and order_id:
            self.store.schedule(
                "review_request",
                f"review_request:{order_id}",  # one review request per order, even with split shipments
                now + s.review_request_days * 86400,
                {"phone": phone, "params": [first, order_name, s.review_link]},
            )
        return "ok"

    def _checkout(self, payload: dict, now: float) -> str:
        s = self.settings
        token = str(payload.get("token") or payload.get("cart_token") or "")
        if not token:
            return "ignored"
        phone = payload_phone(payload, s.default_country_code)
        completed = bool(payload.get("completed_at"))
        self.store.upsert_checkout(
            token,
            phone,
            payload_first_name(payload),
            payload.get("abandoned_checkout_url"),
            money(payload.get("total_price"), payload.get("currency")),
            completed,
            now,
        )
        self._record_consent(payload, phone)
        if s.abandoned_cart_enabled and not completed:
            updated = parse_ts(payload.get("updated_at"), now)
            # Re-scheduled on every update, so the reminder goes out after the customer goes quiet.
            self.store.schedule(
                "abandoned_cart",
                f"abandoned_cart:{token}",
                updated + s.abandoned_cart_delay_minutes * 60,
                {"token": token},
                reschedule=True,
            )
        return "ok"

    # Job side: called by the scheduler when a job is due. ------------------------
    async def run_job(self, kind: str, payload: dict, key: str) -> str:
        s = self.settings
        if kind == "abandoned_cart":
            if not s.abandoned_cart_enabled:
                return "skipped:disabled"
            token = payload.get("token", "")
            checkout = self.store.get_checkout(token)
            if not checkout:
                return "skipped:unknown_checkout"
            if checkout["completed"]:
                return "skipped:completed"
            if not checkout["phone"]:
                return "skipped:no_phone"
            if not checkout["cart_url"]:
                return "skipped:no_cart_url"
            result = await self.notifier.send_template_once(
                key,
                checkout["phone"],
                "abandoned_cart",
                [checkout["first_name"] or "there", checkout["cart_url"]],
            )
            if result == "sent":
                self.store.mark_checkout_reminded(token)
            return result

        enabled = {
            "order_confirmation": s.order_confirmation_enabled,
            "order_shipped": s.shipping_update_enabled,
            "review_request": s.review_request_enabled,
        }
        if kind not in enabled:
            return "skipped:unknown_job"
        if not enabled[kind]:
            return "skipped:disabled"
        return await self.notifier.send_template_once(
            key, payload.get("phone", ""), kind, [str(p) for p in payload.get("params", [])]
        )
