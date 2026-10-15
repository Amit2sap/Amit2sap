"""Shopify webhooks, the persistent scheduler and abandoned-cart logic (all HTTP mocked)."""

import asyncio
import base64
import hashlib
import hmac
import json
from dataclasses import replace

from fastapi.testclient import TestClient

from app.shopify import verify_webhook_hmac
from app.store import Store

from .test_webhook import make_app

SHOP_SECRET = "shpss_test_secret"
NOW = 1_790_000_000.0  # fixed clock for scheduler tests


def shop_sign(body: bytes, secret: str = SHOP_SECRET) -> str:
    return base64.b64encode(hmac.new(secret.encode(), body, hashlib.sha256).digest()).decode()


def auto_settings(settings, **kw):
    base = dict(
        shopify_webhook_secret=SHOP_SECRET,
        order_confirmation_enabled=True,
        shipping_update_enabled=True,
        abandoned_cart_enabled=True,
        review_request_enabled=True,
        review_url="https://g.page/r/grasscrafts/review",
    )
    base.update(kw)
    return replace(settings, **base)


def post_shopify(client, topic, payload, webhook_id=None, secret=SHOP_SECRET):
    body = json.dumps(payload).encode()
    headers = {"X-Shopify-Hmac-Sha256": shop_sign(body, secret), "X-Shopify-Topic": topic}
    if webhook_id:
        headers["X-Shopify-Webhook-Id"] = webhook_id
    return client.post("/shopify/webhook", content=body, headers=headers)


def templates_sent(rec):
    return [b for b in rec.bodies() if b.get("type") == "template"]


ORDER = {
    "id": 5551,
    "name": "#1042",
    "total_price": "2499.00",
    "currency": "INR",
    "phone": None,
    "checkout_token": "chk-1",
    "buyer_accepts_marketing": False,
    "customer": {"first_name": "Asha", "phone": None},
    "shipping_address": {"first_name": "Asha", "phone": "098765 43210"},
}

CHECKOUT = {
    "token": "chk-1",
    "phone": "+91 98765 43210",
    "abandoned_checkout_url": "https://grasscrafts.com/checkouts/chk-1/recover",
    "total_price": "1999.00",
    "currency": "INR",
    "completed_at": None,
    "updated_at": "2026-09-21T10:00:00+05:30",
    "buyer_accepts_marketing": True,
    "customer": {"first_name": "Asha"},
}


# ------------------------------------------------------------------- HMAC
def test_shopify_hmac_verification():
    body = b'{"id": 1}'
    good = shop_sign(body)
    assert verify_webhook_hmac(SHOP_SECRET, body, good)
    assert not verify_webhook_hmac(SHOP_SECRET, body + b" ", good)
    assert not verify_webhook_hmac(SHOP_SECRET, body, shop_sign(body, "other"))
    assert not verify_webhook_hmac(SHOP_SECRET, body, None)
    assert not verify_webhook_hmac("", body, shop_sign(body, ""))  # no secret configured = reject all


def test_shopify_endpoint_rejects_bad_hmac(settings):
    app, rec, services = make_app(auto_settings(settings))
    client = TestClient(app)
    r = post_shopify(client, "orders/create", ORDER, secret="wrong")
    assert r.status_code == 401
    r = client.post("/shopify/webhook", content=json.dumps(ORDER).encode(), headers={"X-Shopify-Topic": "orders/create"})
    assert r.status_code == 401
    assert services.store.get_order("5551") is None and rec.requests == []


# --------------------------------------------------------- order + shipping
def test_order_confirmation_sent_once_as_utility(settings):
    app, rec, services = make_app(auto_settings(settings))
    client = TestClient(app)
    assert post_shopify(client, "orders/create", ORDER, webhook_id="w1").json() == {"status": "ok"}
    sent = templates_sent(rec)
    assert len(sent) == 1
    t = sent[0]
    assert t["to"] == "919876543210"
    assert t["template"]["name"] == "order_confirmation"
    params = [p["text"] for p in t["template"]["components"][0]["parameters"]]
    assert params == ["Asha", "#1042", "₹2,499"]

    # Shopify retries the same webhook, and a second delivery with a new id: still one message.
    assert post_shopify(client, "orders/create", ORDER, webhook_id="w1").json() == {"status": "duplicate"}
    post_shopify(client, "orders/create", ORDER, webhook_id="w2")
    assert len(templates_sent(rec)) == 1
    assert [r["template"] for r in services.store.sent()] == ["order_confirmation"]


def test_order_confirmation_off_by_default(settings):
    app, rec, services = make_app(replace(settings, shopify_webhook_secret=SHOP_SECRET))
    client = TestClient(app)
    post_shopify(client, "orders/create", ORDER)
    assert templates_sent(rec) == []
    assert services.store.get_order("5551")["phone"] == "919876543210"  # still recorded


def test_fulfillment_sends_tracking_and_schedules_review(settings):
    s = auto_settings(settings, review_request_days=7)
    app, rec, services = make_app(s)
    client = TestClient(app)
    post_shopify(client, "orders/create", ORDER)
    fulfillment = {
        "id": 777,
        "order_id": 5551,
        "name": "#1042.1",
        "tracking_company": "Delhivery",
        "tracking_number": "AWB123",
        "tracking_url": "https://track.example/AWB123",
    }
    post_shopify(client, "fulfillments/create", fulfillment)
    shipped = [t for t in templates_sent(rec) if t["template"]["name"] == "order_shipped"]
    assert len(shipped) == 1
    assert [p["text"] for p in shipped[0]["template"]["components"][0]["parameters"]] == [
        "Asha", "#1042", "Delhivery", "https://track.example/AWB123"]

    review = services.store.jobs("review_request:")
    assert len(review) == 1 and review[0]["status"] == "pending"
    sched = services.scheduler
    # Not yet due ...
    assert asyncio.run(sched.run_due(review[0]["due_ts"] - 60)) == []
    # ... due after 7 days, sent once, as long as the customer has opted in (Shopify consent here).
    services.store.record_opt_in("919876543210", "test")
    assert asyncio.run(sched.run_due(review[0]["due_ts"] + 1)) == [("review_request:5551", "sent")]
    assert asyncio.run(sched.run_due(review[0]["due_ts"] + 999)) == []
    reviews = [t for t in templates_sent(rec) if t["template"]["name"] == "review_request"]
    assert len(reviews) == 1
    assert reviews[0]["template"]["components"][0]["parameters"][2]["text"] == "https://g.page/r/grasscrafts/review"


# ----------------------------------------------------------- abandoned cart
def cart_app(settings, **kw):
    app, rec, services = make_app(auto_settings(settings, abandoned_cart_delay_minutes=60, **kw))
    return app, rec, services, services.automations, services.scheduler


def test_abandoned_cart_sends_once_after_delay(settings):
    _, rec, services, auto, sched = cart_app(settings)
    auto.handle_webhook("checkouts/create", CHECKOUT, now=NOW)
    job = services.store.jobs("abandoned_cart:")[0]
    assert job["due_ts"] == CHECKOUT_UPDATED + 3600

    assert asyncio.run(sched.run_due(CHECKOUT_UPDATED + 59 * 60)) == []
    assert templates_sent(rec) == []
    assert asyncio.run(sched.run_due(CHECKOUT_UPDATED + 61 * 60)) == [("abandoned_cart:chk-1", "sent")]
    sent = templates_sent(rec)
    assert len(sent) == 1 and sent[0]["template"]["name"] == "abandoned_cart"
    assert [p["text"] for p in sent[0]["template"]["components"][0]["parameters"]] == [
        "Asha", "https://grasscrafts.com/checkouts/chk-1/recover"]

    # Later updates don't re-arm a reminder that was already sent.
    later = dict(CHECKOUT, updated_at="2026-09-21T12:00:00+05:30")
    auto.handle_webhook("checkouts/update", later, now=NOW)
    asyncio.run(sched.run_due(CHECKOUT_UPDATED + 10 * 3600))
    assert len(templates_sent(rec)) == 1

    # The customer then buys: counted as a recovered cart.
    auto.handle_webhook("orders/create", ORDER, now=NOW)
    assert services.store.count_events("cart_recovered", 0) == 1


def test_abandoned_cart_skips_completed_checkout(settings):
    _, rec, services, auto, sched = cart_app(settings)
    auto.handle_webhook("checkouts/create", CHECKOUT, now=NOW)
    auto.handle_webhook("orders/create", ORDER, now=NOW)  # paid before the reminder was due
    assert asyncio.run(sched.run_due(CHECKOUT_UPDATED + 2 * 3600)) == [("abandoned_cart:chk-1", "skipped:completed")]
    assert templates_sent(rec) == []
    assert services.store.count_events("cart_recovered", 0) == 0  # no reminder, so not "recovered"

    # completed_at on a checkouts/update also counts.
    auto.handle_webhook("checkouts/create", dict(CHECKOUT, token="chk-2"), now=NOW)
    auto.handle_webhook("checkouts/update", dict(CHECKOUT, token="chk-2", completed_at="2026-09-21T10:20:00+05:30"), now=NOW)
    asyncio.run(sched.run_due(CHECKOUT_UPDATED + 3 * 3600))
    assert templates_sent(rec) == []


def test_abandoned_cart_skips_opted_out_and_missing_phone(settings):
    _, rec, services, auto, sched = cart_app(settings)
    services.store.set_marketing("919876543210", "opted_out", "whatsapp_stop")
    auto.handle_webhook("checkouts/create", CHECKOUT, now=NOW)  # its consent tick can't undo STOP
    no_phone = dict(CHECKOUT, token="chk-3", phone=None, customer={"first_name": "Ravi"})
    auto.handle_webhook("checkouts/create", no_phone, now=NOW)
    results = dict(asyncio.run(sched.run_due(CHECKOUT_UPDATED + 2 * 3600)))
    assert results == {"abandoned_cart:chk-1": "skipped:opted_out", "abandoned_cart:chk-3": "skipped:no_phone"}
    assert templates_sent(rec) == []


def test_abandoned_cart_needs_opt_in_by_default(settings):
    _, rec, services, auto, sched = cart_app(settings)
    auto.handle_webhook("checkouts/create", dict(CHECKOUT, buyer_accepts_marketing=False), now=NOW)
    assert asyncio.run(sched.run_due(CHECKOUT_UPDATED + 2 * 3600)) == [("abandoned_cart:chk-1", "skipped:no_opt_in")]
    assert templates_sent(rec) == []


def test_abandoned_cart_disabled_queues_nothing(settings):
    _, rec, services, auto, sched = cart_app(settings, abandoned_cart_enabled=False)
    auto.handle_webhook("checkouts/create", CHECKOUT, now=NOW)
    assert services.store.get_checkout("chk-1")["phone"] == "919876543210"
    assert services.store.jobs() == []


def test_jobs_survive_restart_and_failed_send_retries(settings):
    calls = {"n": 0}

    def flaky(request):
        import httpx

        calls["n"] += 1
        if calls["n"] == 1:
            return httpx.Response(500, json={"error": {"code": 1, "message": "temporary"}})
        return httpx.Response(200, json={"messages": [{"id": "wamid.ok"}]})

    _, _, services, auto, _ = cart_app(settings)
    auto.handle_webhook("checkouts/create", CHECKOUT, now=NOW)
    services.store.close()

    # "Restart": a fresh app on the same SQLite file picks up the pending job.
    import httpx

    from app.main import Services
    from app.shopify import ShopifyClient
    from app.whatsapp import WhatsAppClient

    from .conftest import Recorder
    from .test_webhook import FakeAgent

    rec = Recorder(flaky)
    http = httpx.AsyncClient(transport=httpx.MockTransport(rec))
    s = auto_settings(settings)
    store = Store(s.database_path)
    services2 = Services(s, store, WhatsAppClient(s, http), ShopifyClient(s, http), FakeAgent())
    due = CHECKOUT_UPDATED + 2 * 3600
    assert asyncio.run(services2.scheduler.run_due(due)) == [("abandoned_cart:chk-1", "retry")]
    assert store.sent() == []  # failed send released its claim
    assert asyncio.run(services2.scheduler.run_due(due + 600)) == [("abandoned_cart:chk-1", "sent")]
    assert asyncio.run(services2.scheduler.run_due(due + 9999)) == []
    assert len(store.sent("abandoned_cart:")) == 1


from app.automations import parse_ts  # noqa: E402

CHECKOUT_UPDATED = parse_ts(CHECKOUT["updated_at"], 0)
