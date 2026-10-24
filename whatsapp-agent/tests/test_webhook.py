import json

import httpx
from fastapi.testclient import TestClient

from app.main import Services, create_app
from app.shopify import ShopifyClient
from app.store import Store
from app.whatsapp import WhatsAppClient, parse_webhook, split_message, verify_signature

from .conftest import APP_SECRET, VERIFY_TOKEN, Recorder, sign, text_payload


class FakeAgent:
    def __init__(self, reply="Hello from GrassCrafts!"):
        self.calls = []
        self._reply = reply

    async def reply(self, history, text, phone, name=None):
        self.calls.append({"history": history, "text": text, "phone": phone, "name": name})
        return self._reply


def make_app(settings, agent=None):
    rec = Recorder()
    http = httpx.AsyncClient(transport=httpx.MockTransport(rec))
    wa = WhatsAppClient(settings, http)
    shop = ShopifyClient(settings, http)
    store = Store(settings.database_path)
    services = Services(settings, store, wa, shop, agent or FakeAgent())
    return create_app(settings, services), rec, services


# ------------------------------------------------------------ signatures
def test_verify_signature_valid_and_invalid():
    body = b'{"a":1}'
    assert verify_signature(APP_SECRET, body, sign(body))
    assert not verify_signature(APP_SECRET, body, sign(body, "wrong-secret"))
    assert not verify_signature(APP_SECRET, body + b" ", sign(body))
    assert not verify_signature(APP_SECRET, body, None)
    assert not verify_signature(APP_SECRET, body, "md5=abc")
    assert not verify_signature("", body, sign(body, ""))


def test_post_rejects_bad_signature(settings):
    app, rec, services = make_app(settings)
    client = TestClient(app)
    body = json.dumps(text_payload()).encode()
    r = client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body, "nope")})
    assert r.status_code == 403
    r = client.post("/webhook", content=body)
    assert r.status_code == 403
    assert services.agent.calls == []
    assert rec.requests == []


# ------------------------------------------------------------- handshake
def test_verify_handshake(settings):
    app, _, _ = make_app(settings)
    client = TestClient(app)
    r = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": VERIFY_TOKEN, "hub.challenge": "12345"},
    )
    assert r.status_code == 200
    assert r.text == "12345"

    r = client.get(
        "/webhook",
        params={"hub.mode": "subscribe", "hub.verify_token": "wrong", "hub.challenge": "12345"},
    )
    assert r.status_code == 403
    r = client.get("/webhook", params={"hub.mode": "unsubscribe", "hub.verify_token": VERIFY_TOKEN})
    assert r.status_code == 403


# --------------------------------------------------------------- parsing
def test_parse_text_button_interactive_and_status():
    p = text_payload(body="  Do you have trays?  ")
    msgs = parse_webhook(p)
    assert len(msgs) == 1
    m = msgs[0]
    assert (m.message_id, m.from_phone, m.name, m.kind, m.text) == (
        "wamid.1", "919876543210", "Asha", "text", "Do you have trays?"
    )

    value = p["entry"][0]["changes"][0]["value"]
    value["messages"] = [
        {"id": "b1", "from": "911", "type": "button", "button": {"text": "Track order", "payload": "TRACK"}},
        {"id": "i1", "from": "911", "type": "interactive",
         "interactive": {"type": "button_reply", "button_reply": {"id": "x", "title": "Gift boxes"}}},
        {"id": "l1", "from": "911", "type": "interactive",
         "interactive": {"type": "list_reply", "list_reply": {"id": "y", "title": "Planters"}}},
        {"id": "a1", "from": "911", "type": "audio", "audio": {"id": "m"}},
    ]
    texts = [(m.kind, m.text) for m in parse_webhook(p)]
    assert texts == [
        ("button", "Track order"), ("interactive", "Gift boxes"),
        ("interactive", "Planters"), ("audio", None),
    ]

    status_only = text_payload()
    v = status_only["entry"][0]["changes"][0]["value"]
    del v["messages"]
    v["statuses"] = [{"id": "wamid.out", "status": "delivered", "recipient_id": "919876543210"}]
    assert parse_webhook(status_only) == []
    assert parse_webhook({"object": "page"}) == []


def test_split_message():
    assert split_message("short") == ["short"]
    long = ("word " * 2000).strip()  # ~10k chars
    parts = split_message(long)
    assert len(parts) == 3
    assert all(len(p) <= 4096 for p in parts)
    assert " ".join(parts) == long
    assert all(len(p) <= 100 for p in split_message("x" * 250, limit=100))


def test_message_path_end_to_end_with_dedupe(settings):
    agent = FakeAgent("We have lovely trays! https://grasscrafts.com/products/tray")
    app, rec, services = make_app(settings, agent)
    client = TestClient(app)
    body = json.dumps(text_payload(body="Do you have trays?")).encode()
    headers = {"X-Hub-Signature-256": sign(body)}

    r = client.post("/webhook", content=body, headers=headers)
    assert r.status_code == 200
    assert len(agent.calls) == 1
    assert agent.calls[0]["text"] == "Do you have trays?"
    assert agent.calls[0]["phone"] == "919876543210"

    sent = rec.bodies()
    assert sent[0] == {"messaging_product": "whatsapp", "status": "read", "message_id": "wamid.1"}
    assert sent[1]["to"] == "919876543210"
    assert sent[1]["text"]["body"].startswith("We have lovely trays")
    assert rec.requests[1].url.path == "/v21.0/123456/messages"
    assert rec.requests[1].headers["Authorization"] == "Bearer wa-token"

    # Meta retry of the same message id is ignored.
    r = client.post("/webhook", content=body, headers=headers)
    assert r.status_code == 200
    assert len(agent.calls) == 1

    # History is stored for the next turn.
    assert services.store.history("919876543210") == [
        {"role": "user", "content": "Do you have trays?"},
        {"role": "assistant", "content": "We have lovely trays! https://grasscrafts.com/products/tray"},
    ]


def test_status_callback_is_ignored(settings):
    app, rec, services = make_app(settings)
    client = TestClient(app)
    p = text_payload()
    v = p["entry"][0]["changes"][0]["value"]
    del v["messages"]
    v["statuses"] = [{"id": "wamid.out", "status": "read"}]
    body = json.dumps(p).encode()
    r = client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert r.status_code == 200
    assert services.agent.calls == [] and rec.requests == []


def test_owner_pause_and_resume(settings):
    agent = FakeAgent()
    app, rec, services = make_app(settings, agent)
    client = TestClient(app)

    def post(payload):
        body = json.dumps(payload).encode()
        return client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})

    post(text_payload(msg_id="o1", sender="919999900000", body="/pause 98765 43210"))
    assert services.store.is_paused("919876543210")

    post(text_payload(msg_id="c1", body="hello?"))
    assert agent.calls == []  # paused: no auto reply
    forwarded = [b for b in rec.bodies() if b.get("type") == "text" and b["to"] == "919999900000"]
    assert any("hello?" in b["text"]["body"] for b in forwarded)

    post(text_payload(msg_id="o2", sender="919999900000", body="/resume +919876543210"))
    assert not services.store.is_paused("919876543210")
    post(text_payload(msg_id="c2", body="hello again"))
    assert len(agent.calls) == 1
    # The message sent during the pause is kept as context.
    assert agent.calls[0]["history"][0]["content"] == "hello?"


def test_global_pause(settings):
    from dataclasses import replace

    s = replace(settings, paused=True)
    agent = FakeAgent()
    app, rec, _ = make_app(s, agent)
    client = TestClient(app)
    body = json.dumps(text_payload()).encode()
    client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert agent.calls == []


def test_rate_limit(settings):
    from dataclasses import replace

    s = replace(settings, rate_limit_per_hour=2)
    agent = FakeAgent()
    app, rec, _ = make_app(s, agent)
    client = TestClient(app)
    for i in range(4):
        body = json.dumps(text_payload(msg_id=f"r{i}")).encode()
        client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert len(agent.calls) == 2
    notices = [b for b in rec.bodies() if b.get("type") == "text" and "quite a few" in b["text"]["body"]]
    assert len(notices) == 1


def test_agent_error_sends_fallback(settings):
    class Boom(FakeAgent):
        async def reply(self, *a, **k):
            raise RuntimeError("model down")

    app, rec, _ = make_app(settings, Boom())
    client = TestClient(app)
    body = json.dumps(text_payload()).encode()
    r = client.post("/webhook", content=body, headers={"X-Hub-Signature-256": sign(body)})
    assert r.status_code == 200
    texts = [b["text"]["body"] for b in rec.bodies() if b.get("type") == "text"]
    assert texts and "trouble" in texts[-1]
