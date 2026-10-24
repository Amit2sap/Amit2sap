"""Lead capture tools, the admin dashboard (auth, CSV, status form), the daily digest and
store-fact placeholders."""

import asyncio
import json
from dataclasses import replace

from fastapi.testclient import TestClient

from app.agent import Agent, build_tools, prepare_store_facts
from app.digest import build_digest, classify_question
from app.store import Store

from .test_agent import FakeShopify, FakeWhatsApp, StubClient, resp, text, tool_use
from .test_webhook import make_app

CUSTOMER = "919876543210"
NOW = 1_790_000_000.0


class DocWhatsApp(FakeWhatsApp):
    def __init__(self):
        super().__init__()
        self.documents = []

    async def send_document(self, to, link, filename, caption=""):
        self.documents.append((to, link, filename))


def lead_agent(settings, responses):
    client = StubClient(responses)
    store = Store(settings.database_path)
    wa = DocWhatsApp()
    return Agent(settings, FakeShopify(), wa, client=client, store=store), client.beta.messages, store, wa


# -------------------------------------------------------------------- leads
def test_save_lead_stores_and_alerts_owner(settings):
    responses = [
        resp("tool_use", tool_use("t1", "save_lead", {
            "lead_type": "corporate", "company": "Acme Pvt Ltd", "city": "Pune",
            "product_interest": "jute gift hampers", "quantity": "200", "budget_per_piece": "₹500",
            "needed_by": "25 Oct 2026",
        })),
        resp("end_turn", text("Thank you! Our team will share a quote on this number.")),
        resp("tool_use", tool_use("t2", "save_lead", {
            "lead_type": "corporate", "customisation": "logo on the box", "email": "ravi@acme.example"})),
        resp("end_turn", text("Noted, thanks!")),
    ]
    agent, msgs, store, wa = lead_agent(settings, responses)
    asyncio.run(agent.reply([], "Need 200 Diwali hampers for our employees", CUSTOMER, "Ravi"))

    leads = store.list_leads()
    assert len(leads) == 1
    lead = leads[0]
    assert (lead["name"], lead["company"], lead["quantity"], lead["status"]) == ("Ravi", "Acme Pvt Ltd", "200", "new")
    assert lead["phone"] == CUSTOMER

    to, body = wa.texts[0]
    assert to == "919999900000"
    for expected in ("New bulk lead #1", "(corporate)", "Acme Pvt Ltd", "Pune", "jute gift hampers",
                     "200", "₹500", "25 Oct 2026", "Customisation: -", "https://wa.me/919876543210"):
        assert expected in body
    result = json.loads(msgs.calls[1]["messages"][-1]["content"][0]["content"])
    assert result["saved"] is True and result["owner_notified"] is True
    assert "email" in result["still_unknown"]

    # Next message adds details: same lead updated, not duplicated.
    asyncio.run(agent.reply([], "logo on the box please, ravi@acme.example", CUSTOMER, "Ravi"))
    leads = store.list_leads()
    assert len(leads) == 1
    assert leads[0]["customisation"] == "logo on the box" and leads[0]["company"] == "Acme Pvt Ltd"
    assert "Updated bulk lead #1" in wa.texts[1][1]
    assert store.count_events("lead", 0) == 1


def test_lead_and_catalogue_tools_follow_settings(settings):
    names = lambda s: {t["name"] for t in build_tools(s)}  # noqa: E731
    assert "save_lead" in names(settings) and "send_catalogue" not in names(settings)
    assert "save_lead" not in names(replace(settings, lead_capture_enabled=False))
    with_pdf = replace(settings, catalogue_pdf_url="https://cdn.example/catalogue.pdf")
    assert {"save_lead", "send_catalogue"} <= names(with_pdf)

    agent, msgs, _, _ = lead_agent(settings, [resp("end_turn", text("hi"))])
    asyncio.run(agent.reply([], "hi", CUSTOMER))
    system = msgs.calls[0]["system"][0]["text"]
    assert "save_lead" in system and "send_catalogue" not in system


def test_send_catalogue_sends_pdf_document(settings):
    s = replace(settings, catalogue_pdf_url="https://cdn.example/catalogue.pdf")
    responses = [
        resp("tool_use", tool_use("t1", "send_catalogue", {}), tool_use("t2", "send_catalogue", {})),
        resp("end_turn", text("Sent you our catalogue!")),
    ]
    agent, msgs, _, wa = lead_agent(s, responses)
    asyncio.run(agent.reply([], "send catalogue", CUSTOMER))
    assert wa.documents == [(CUSTOMER, "https://cdn.example/catalogue.pdf", "GrassCrafts-Corporate-Catalogue.pdf")]
    assert "send_catalogue" in msgs.calls[0]["system"][0]["text"]


def test_send_catalogue_skipped_without_url(settings):
    responses = [resp("tool_use", tool_use("t1", "send_catalogue", {})), resp("end_turn", text("ok"))]
    agent, msgs, _, wa = lead_agent(settings, responses)
    asyncio.run(agent.reply([], "catalogue?", CUSTOMER))
    assert wa.documents == []
    assert json.loads(msgs.calls[1]["messages"][-1]["content"][0]["content"])["sent"] is False


# -------------------------------------------------------------------- admin
def admin_app(settings, password="s3cret"):
    app, rec, services = make_app(replace(settings, admin_user="owner", admin_password=password))
    return TestClient(app), services


def test_admin_requires_basic_auth(settings):
    client, services = admin_app(settings)
    for path in ("/admin", "/admin/leads.csv"):
        assert client.get(path).status_code == 401
        assert client.get(path).headers["WWW-Authenticate"].startswith("Basic")
        assert client.get(path, auth=("owner", "wrong")).status_code == 401
        assert client.get(path, auth=("someone", "s3cret")).status_code == 401
    assert client.post("/admin/leads/1/status", content="status=won").status_code == 401

    disabled, _ = admin_app(settings, password="")
    assert disabled.get("/admin", auth=("owner", "")).status_code == 404


def test_admin_dashboard_csv_and_status_update(settings):
    client, services = admin_app(settings)
    store = services.store
    lead_id, _ = store.save_lead(CUSTOMER, {
        "name": "Ravi <script>", "company": "=HYPERLINK(\"x\")", "quantity": "200", "lead_type": "wedding"})
    store.append("919811112222", "user", "hello")
    store.pause("919811112222")

    r = client.get("/admin", auth=("owner", "s3cret"))
    assert r.status_code == 200
    html = r.text
    assert "Ravi &lt;script&gt;" in html and "<script>" not in html
    assert "***2222" in html and "919811112222</td>" not in html  # conversations are masked
    assert "Paused chats" in html and "Download CSV" in html

    r = client.get("/admin/leads.csv", auth=("owner", "s3cret"))
    assert r.status_code == 200 and r.headers["content-type"].startswith("text/csv")
    rows = r.text.lstrip("﻿").splitlines()
    assert rows[0].startswith("id,status,created,phone,name,company")
    assert "+919876543210" in rows[1] and "'=HYPERLINK" in rows[1]  # formula neutralised

    # Status form needs the page's form token.
    token = html.split("name='csrf' value='")[1].split("'")[0]
    bad = client.post(f"/admin/leads/{lead_id}/status", content="status=won&csrf=nope",
                      auth=("owner", "s3cret"), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert bad.status_code == 403
    ok = client.post(f"/admin/leads/{lead_id}/status", content=f"status=won&csrf={token}",
                     auth=("owner", "s3cret"), headers={"Content-Type": "application/x-www-form-urlencoded"},
                     follow_redirects=False)
    assert ok.status_code == 303
    assert store.get_lead(lead_id)["status"] == "won"
    invalid = client.post(f"/admin/leads/{lead_id}/status", content=f"status=maybe&csrf={token}",
                          auth=("owner", "s3cret"), headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert invalid.status_code == 400


def test_health_endpoint(settings):
    app, _, _ = make_app(settings)
    client = TestClient(app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/healthz").json() == {"status": "ok"}


# ------------------------------------------------------------------- digest
def test_question_topics():
    assert classify_question("Where is my order #1042?") == "Order status / tracking"
    assert classify_question("need 200 pcs for corporate gifting") == "Bulk / corporate / wedding"
    assert classify_question("kitna price hai is tray ka") == "Price"
    assert classify_question("hello") == "Other"


def test_digest_content(settings):
    store = Store(settings.database_path)
    day = NOW - 3600
    for phone, topic in [("911", "Price"), ("911", "Price"), ("912", "Order status / tracking"), ("913", "Price")]:
        store.log_event("inbound", phone, topic, now=day)
    store.log_event("inbound", "914", "Price", now=NOW - 3 * 86400)  # older than 24 h: excluded
    store.log_event("lead", "912", "corporate", now=day)
    store.log_event("escalation", "913", now=day)
    store.log_event("cart_recovered", "911", "#1042", now=day)
    store.log_event("opt_out", "913", now=day)
    store.log_event("opt_out", "914", now=day)
    store.save_lead("912", {"name": "Ravi"})

    text = build_digest(store, now=NOW)
    assert "daily digest" in text
    assert "Conversations: 3 (4 messages)" in text
    assert "New bulk/corporate leads: 1" in text
    assert "Escalations to you: 1" in text
    assert "Abandoned carts recovered: 1" in text
    assert "Opt-outs: 2" in text
    assert "• Price: 3" in text and "• Order status / tracking: 1" in text
    assert text.index("Price: 3") < text.index("Order status")
    assert "1 lead(s) still marked *new*" in text


def test_digest_sent_once_per_day_after_digest_hour(settings):
    s = replace(settings, digest_enabled=True, digest_hour=9, digest_channels="whatsapp")
    app, rec, services = make_app(s)
    sched = services.scheduler
    from datetime import datetime

    from app.digest import IST

    morning = datetime(2026, 10, 15, 8, 30, tzinfo=IST).timestamp()
    nine = datetime(2026, 10, 15, 9, 1, tzinfo=IST).timestamp()
    assert asyncio.run(sched.maybe_send_digest(morning)) is False
    assert asyncio.run(sched.maybe_send_digest(nine)) is True
    assert asyncio.run(sched.maybe_send_digest(nine + 3600)) is False
    assert asyncio.run(sched.maybe_send_digest(nine + 86400)) is True
    digests = [b for b in rec.bodies() if b.get("type") == "text" and "daily digest" in b["text"]["body"]]
    assert len(digests) == 2 and digests[0]["to"] == "919999900000"

    off, rec2, services2 = make_app(replace(settings, digest_enabled=False))
    assert asyncio.run(services2.scheduler.maybe_send_digest(nine)) is False


# --------------------------------------------------------------- store facts
def test_placeholders_never_reach_the_model(settings, tmp_path):
    facts = tmp_path / "facts.md"
    facts.write_text(
        "<!-- owner notes: [OWNER: fill in] explained here -->\n"
        "## Returns and refunds\n"
        "- Return window: [OWNER: fill in, e.g. 7 days from delivery]\n"
        "- [OWNER: fill in]\n"
        "## Shipping\n- Free shipping above ₹1,300.\n",
        encoding="utf-8",
    )
    out = prepare_store_facts(facts.read_text(encoding="utf-8"))
    assert "7 days" not in out and "OWNER" not in out and "owner notes" not in out
    assert "- Return window: NOT CONFIRMED" in out
    assert "- Returns and refunds: NOT CONFIRMED" in out
    assert "Free shipping above ₹1,300." in out

    agent, msgs, _, _ = lead_agent(replace(settings, store_facts_path=str(facts)), [resp("end_turn", text("hi"))])
    asyncio.run(agent.reply([], "what is your return policy?", CUSTOMER))
    system = msgs.calls[0]["system"][0]["text"]
    assert "Return window: NOT CONFIRMED" in system and "7 days" not in system
    assert "NOT CONFIRMED has not been decided" in system


def test_shipped_store_facts_have_owner_sections(settings):
    from pathlib import Path

    raw = Path(settings.store_facts_path).read_text(encoding="utf-8")
    for heading in ("## Returns and refunds", "## Caring for natural-fibre products",
                    "## Customisation and bulk orders", "## Lead times"):
        assert heading in raw
    assert raw.count("[OWNER: fill in") >= 10
    assert "[OWNER" not in prepare_store_facts(raw)
