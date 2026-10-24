"""Opt-in / opt-out handling and the broadcast CLI (dry run vs --confirm)."""

import asyncio
import json
from dataclasses import replace

import pytest
from fastapi.testclient import TestClient

from app import broadcast as broadcast_mod
from app.broadcast import BroadcastError, run_broadcast
from app.consent import MARKETING, UTILITY, can_send, consent_command

from .conftest import sign, text_payload
from .test_webhook import FakeAgent, make_app

CUSTOMER = "919876543210"


def post(client, payload):
    body = json.dumps(payload).encode()
    return client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})


def texts_to(rec, phone):
    return [b["text"]["body"] for b in rec.bodies() if b.get("type") == "text" and b["to"] == phone]


# ------------------------------------------------------------------ consent
def test_consent_keywords_are_whole_message_only():
    for word in ("STOP", "stop.", "Unsubscribe", "band karo", "Band Karo 🙏", "बंद करो", "Stop promotions"):
        assert consent_command(word) == "opt_out", word
    for word in ("START", "start!", "Subscribe"):
        assert consent_command(word) == "opt_in", word
    for text in ("stop the order please", "when will shipping start?", "hi", "", None):
        assert consent_command(text) is None


def test_first_message_records_opt_in(settings):
    agent = FakeAgent()
    app, rec, services = make_app(settings, agent)
    post(TestClient(app), text_payload(body="Do you have trays?"))
    assert services.store.get_marketing(CUSTOMER) == "opted_in"
    assert len(agent.calls) == 1


def test_stop_opts_out_and_start_resubscribes(settings):
    agent = FakeAgent()
    app, rec, services = make_app(settings, agent)
    client = TestClient(app)
    store = services.store

    post(client, text_payload(msg_id="m1", body="hello"))
    post(client, text_payload(msg_id="m2", body="STOP"))
    assert store.get_marketing(CUSTOMER) == "opted_out"
    assert "unsubscribed" in texts_to(rec, CUSTOMER)[-1]
    assert len(agent.calls) == 1  # STOP is not passed to the AI

    # A later normal message must not silently re-subscribe them.
    post(client, text_payload(msg_id="m3", body="where is my order?"))
    assert store.get_marketing(CUSTOMER) == "opted_out"
    assert can_send(store, settings, CUSTOMER, MARKETING) == (False, "opted_out")
    assert can_send(store, settings, CUSTOMER, UTILITY) == (True, "ok")  # order updates still allowed

    post(client, text_payload(msg_id="m4", body="band karo"))
    assert store.count_events("opt_out", 0) == 2

    post(client, text_payload(msg_id="m5", body="START"))
    assert store.get_marketing(CUSTOMER) == "opted_in"
    assert "subscribed" in texts_to(rec, CUSTOMER)[-1]


def test_stop_works_while_chat_is_paused(settings):
    agent = FakeAgent()
    app, rec, services = make_app(settings, agent)
    services.store.pause(CUSTOMER)
    post(TestClient(app), text_payload(body="UNSUBSCRIBE"))
    assert services.store.get_marketing(CUSTOMER) == "opted_out"
    assert agent.calls == []


def test_opt_out_handling_can_be_switched_off(settings):
    agent = FakeAgent()
    app, rec, services = make_app(replace(settings, opt_out_enabled=False), agent)
    post(TestClient(app), text_payload(body="STOP"))
    assert services.store.get_marketing(CUSTOMER) == "opted_in"
    assert len(agent.calls) == 1


def test_marketing_never_sent_to_opted_out(settings):
    app, rec, services = make_app(settings)
    services.store.set_marketing(CUSTOMER, "opted_out", "whatsapp_stop")
    result = asyncio.run(
        services.notifier.send_template_once("x:1", CUSTOMER, "diwali_offer", ["Asha", "DIWALI10"])
    )
    assert result == "skipped:opted_out"
    assert rec.requests == [] and services.store.sent() == []


# ---------------------------------------------------------------- broadcast
def seed(store):
    store.record_opt_in("919800000001", "whatsapp_inbound", "Asha Rao")
    store.record_opt_in("919800000002", "shopify", None)
    store.record_opt_in("919800000003", "whatsapp_inbound", "Ravi")
    store.set_marketing("919800000003", "opted_out", "whatsapp_stop")  # in no segment
    store.set_marketing("919800000004", "opted_out", "whatsapp_stop")


def run(settings, services, confirm, **kw):
    lines, sleeps = [], []

    async def fake_sleep(sec):
        sleeps.append(sec)

    result = asyncio.run(
        run_broadcast(
            settings, services.store, services.whatsapp, "diwali_offer", "opted_in",
            ["{name}", "DIWALI10"], confirm=confirm, campaign="diwali-test",
            sleep=fake_sleep, out=lines.append, **kw,
        )
    )
    return result, lines, sleeps


def test_broadcast_dry_run_sends_nothing(settings):
    s = replace(settings, broadcast_enabled=True)
    app, rec, services = make_app(s)
    seed(services.store)
    result, lines, sleeps = run(s, services, confirm=False)
    assert result["counts"] == {"would_send": 2}
    assert rec.requests == [] and services.store.sent() == []
    assert services.store.broadcast_results("diwali-test") == []
    assert "DRY RUN" in lines[0]
    assert any("Asha | DIWALI10" in l for l in lines)
    assert any("there | DIWALI10" in l for l in lines)  # no name on file
    assert not any("9800000001" in l for l in lines)  # numbers are masked


def test_broadcast_confirm_sends_rate_limited_once(settings):
    s = replace(settings, broadcast_enabled=True)
    app, rec, services = make_app(s)
    seed(services.store)
    result, lines, sleeps = run(s, services, confirm=True, rate_per_second=4)
    assert result["sent"] == 2
    sent = [b for b in rec.bodies() if b.get("type") == "template"]
    assert sorted(b["to"] for b in sent) == ["919800000001", "919800000002"]
    assert {b["template"]["name"] for b in sent} == {"diwali_offer"}
    assert sleeps == [0.25]  # paced between sends
    log = services.store.broadcast_results("diwali-test")
    assert [(r["phone"], r["status"]) for r in log] == [("919800000001", "sent"), ("919800000002", "sent")]

    # Someone opts out, then the campaign is re-run: no repeats, opted-out skipped.
    services.store.set_marketing("919800000002", "opted_out", "whatsapp_stop")
    result, _, _ = run(s, services, confirm=True)
    assert result["counts"] == {"duplicate": 1}
    assert len([b for b in rec.bodies() if b.get("type") == "template"]) == 2


def test_broadcast_confirm_requires_flag_and_marketing_template(settings):
    app, rec, services = make_app(settings)  # BROADCAST_ENABLED is off by default
    seed(services.store)
    with pytest.raises(BroadcastError, match="BROADCAST_ENABLED"):
        run(settings, services, confirm=True)
    s = replace(settings, broadcast_enabled=True)
    with pytest.raises(BroadcastError, match="MARKETING"):
        asyncio.run(run_broadcast(s, services.store, services.whatsapp, "order_confirmation", "opted_in",
                                  ["a", "b", "c"], confirm=True, out=lambda _: None))
    with pytest.raises(BroadcastError, match="needs 2"):
        asyncio.run(run_broadcast(s, services.store, services.whatsapp, "diwali_offer", "opted_in",
                                  ["only one"], out=lambda _: None))
    assert rec.requests == []


def test_broadcast_cli_defaults_to_dry_run(settings, monkeypatch, capsys):
    s = replace(settings, broadcast_enabled=True)
    from app.store import Store

    seed(Store(s.database_path))
    monkeypatch.setattr(broadcast_mod, "get_settings", lambda: s)
    sent = []

    class NoSend:
        def __init__(self, *_):
            pass

        async def send_template(self, *a):
            sent.append(a)

        async def aclose(self):
            pass

    monkeypatch.setattr(broadcast_mod, "WhatsAppClient", NoSend)
    argv = ["--template", "diwali_offer", "--segment", "opted_in", "--param", "{name}", "--param", "DIWALI10"]
    assert broadcast_mod.main(argv) == 0
    assert sent == [] and "DRY RUN" in capsys.readouterr().out
    assert broadcast_mod.main(argv + ["--dry-run"]) == 0 and sent == []
    assert broadcast_mod.main(argv + ["--confirm"]) == 0
    assert len(sent) == 2


# ----------------------------------------------------------- template sync
def test_templates_sync_creates_and_shows_status(settings, capsys):
    import httpx

    from app import templates_sync

    s = replace(settings, whatsapp_business_account_id="WABA1")
    posted = []

    def handler(request):
        if request.method == "POST":
            body = json.loads(request.content)
            posted.append(body)
            if body["name"] == "owner_alert":
                return httpx.Response(400, json={"error": {"message": "Template already exists"}})
            return httpx.Response(200, json={"id": "1", "status": "PENDING", "category": body["category"]})
        return httpx.Response(200, json={"data": [
            {"name": "diwali_offer", "language": "en", "status": "APPROVED", "category": "MARKETING"}]})

    http = httpx.Client(transport=httpx.MockTransport(handler))
    assert templates_sync.main([], settings=s, http=http) == 0
    names = {(b["name"], b["language"]) for b in posted}
    assert ("order_confirmation", "hi") in names and ("diwali_offer", "en") in names
    cats = {b["name"]: b["category"] for b in posted}
    assert cats["order_confirmation"] == cats["order_shipped"] == "UTILITY"
    assert cats["diwali_offer"] == cats["abandoned_cart"] == "MARKETING"
    body = next(b for b in posted if b["name"] == "order_shipped")["components"][0]
    assert body["type"] == "BODY" and len(body["example"]["body_text"][0]) == 4
    out = capsys.readouterr().out
    assert "already exists" in out and "APPROVED" in out
