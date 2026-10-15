"""Tool-use loop tests with a stubbed Anthropic client (no network)."""

import asyncio
import json
from types import SimpleNamespace

from app.agent import FALLBACK_BETA, Agent


def text(t):
    return SimpleNamespace(type="text", text=t)


def tool_use(id_, name, input_):
    return SimpleNamespace(type="tool_use", id=id_, name=name, input=input_)


def resp(stop_reason, *content):
    return SimpleNamespace(stop_reason=stop_reason, content=list(content))


class StubMessages:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    async def create(self, **kwargs):
        # Snapshot messages: the agent keeps appending to the same list.
        self.calls.append({**kwargs, "messages": list(kwargs["messages"])})
        return self.responses.pop(0)


class StubClient:
    def __init__(self, responses):
        self.beta = SimpleNamespace(messages=StubMessages(responses))


class FakeShopify:
    def __init__(self):
        self.calls = []

    async def search_products(self, query, max_price=None):
        self.calls.append(("search_products", query, max_price))
        return {"count": 1, "products": [{"title": "Round Cane Tray", "handle": "round-cane-tray",
                                          "price": {"min": 899.0}, "in_stock": True,
                                          "image_url": "https://cdn.shopify.com/tray.jpg"}]}

    async def get_product(self, handle):
        self.calls.append(("get_product", handle))
        return {"found": True}

    async def get_order_status(self, order_number, sender_phone):
        self.calls.append(("get_order_status", order_number, sender_phone))
        return {"found": True, "verified": False, "message": "ask for email"}


class FakeWhatsApp:
    def __init__(self):
        self.texts, self.images, self.templates = [], [], []

    async def send_text(self, to, body):
        self.texts.append((to, body))

    async def send_image(self, to, url, caption=""):
        self.images.append((to, url, caption))

    async def send_template(self, to, name, lang, params):
        self.templates.append((to, name, lang, params))


def make_agent(settings, responses):
    client = StubClient(responses)
    shop, wa = FakeShopify(), FakeWhatsApp()
    return Agent(settings, shop, wa, client=client), client.beta.messages, shop, wa


def test_tool_loop_runs_tools_and_returns_final_text(settings):
    responses = [
        resp("tool_use", text("Let me check."), tool_use("t1", "search_products", {"query": "tray", "max_price": 1000})),
        resp("tool_use", tool_use("t2", "send_product_image",
                                  {"image_url": "https://cdn.shopify.com/tray.jpg", "caption": "Round Cane Tray ₹899"})),
        resp("end_turn", text("Here's our Round Cane Tray for ₹899: https://grasscrafts.com/products/round-cane-tray")),
    ]
    agent, msgs, shop, wa = make_agent(settings, responses)
    history = [{"role": "user", "content": "hi"}, {"role": "assistant", "content": "Hello!"}]

    out = asyncio.run(agent.reply(history, "trays under 1000?", "919876543210", "Asha"))

    assert out.startswith("Here's our Round Cane Tray")
    assert shop.calls == [("search_products", "tray", 1000.0)]
    assert wa.images == [("919876543210", "https://cdn.shopify.com/tray.jpg", "Round Cane Tray ₹899")]
    assert len(msgs.calls) == 3

    first = msgs.calls[0]
    assert first["model"] == "claude-sonnet-5-5"
    assert first["output_config"] == {"effort": "low"}
    assert first["betas"] == [FALLBACK_BETA] and first["fallbacks"] == "default"
    assert {t["name"] for t in first["tools"]} == {
        "search_products", "get_product", "get_order_status", "escalate_to_owner", "send_product_image",
        "save_lead"}  # lead capture is on by default; send_catalogue only appears with CATALOGUE_PDF_URL
    assert "Free shipping across India on orders above ₹1,300" in first["system"][0]["text"]
    assert first["messages"][:2] == history
    assert first["messages"][2]["role"] == "user"
    assert first["messages"][2]["content"].endswith("trays under 1000?")

    # Second call: assistant turn passed back unchanged, then tool results in one user turn.
    second = msgs.calls[1]["messages"]
    assert second[3] == {"role": "assistant", "content": responses[0].content}
    assert second[4]["role"] == "user"
    result = second[4]["content"][0]
    assert result["type"] == "tool_result" and result["tool_use_id"] == "t1"
    assert json.loads(result["content"])["products"][0]["handle"] == "round-cane-tray"


def test_order_tool_receives_sender_phone_not_model_input(settings):
    responses = [
        resp("tool_use", tool_use("t1", "get_order_status", {"order_number": "#1234"})),
        resp("end_turn", text("Please email us from the address on the order.")),
    ]
    agent, _, shop, _ = make_agent(settings, responses)
    asyncio.run(agent.reply([], "where is order 1234", "919876543210"))
    assert shop.calls == [("get_order_status", "#1234", "919876543210")]


def test_escalation_notifies_owner(settings):
    responses = [
        resp("tool_use", tool_use("t1", "escalate_to_owner",
                                  {"summary": "Corporate order: 200 gift boxes for Diwali, budget ₹500 each"})),
        resp("end_turn", text("Thanks! Our team will contact you shortly on WhatsApp.")),
    ]
    agent, msgs, _, wa = make_agent(settings, responses)
    out = asyncio.run(agent.reply([], "need 200 gift boxes", "919876543210", "Ravi"))
    assert "team" in out
    assert len(wa.texts) == 1
    to, body = wa.texts[0]
    assert to == "919999900000"
    assert "+919876543210" in body and "200 gift boxes" in body and "Ravi" in body
    tool_result = json.loads(msgs.calls[1]["messages"][-1]["content"][0]["content"])
    assert tool_result["notified"] is True


def test_tool_error_is_reported_to_model(settings):
    class BrokenShop(FakeShopify):
        async def search_products(self, query, max_price=None):
            raise RuntimeError("shopify down")

    responses = [
        resp("tool_use", tool_use("t1", "search_products", {"query": "basket"})),
        resp("end_turn", text("Sorry, I couldn't check right now.")),
    ]
    client = StubClient(responses)
    agent = Agent(settings, BrokenShop(), FakeWhatsApp(), client=client)
    out = asyncio.run(agent.reply([], "baskets?", "919876543210"))
    assert out == "Sorry, I couldn't check right now."
    tr = client.beta.messages.calls[1]["messages"][-1]["content"][0]
    assert tr["is_error"] is True


def test_refusal_and_iteration_limit(settings):
    agent, _, _, _ = make_agent(settings, [resp("refusal")])
    assert "can't help" in asyncio.run(agent.reply([], "x", "919876543210"))

    looping = [resp("tool_use", tool_use(f"t{i}", "get_product", {"handle": "a"})) for i in range(10)]
    agent, msgs, _, _ = make_agent(settings, looping)
    out = asyncio.run(agent.reply([], "x", "919876543210"))
    assert "trouble" in out
    assert len(msgs.calls) == settings.max_tool_iterations


def test_fallback_can_be_disabled(settings):
    from dataclasses import replace

    s = replace(settings, anthropic_refusal_fallback=False)
    agent, msgs, _, _ = make_agent(s, [resp("end_turn", text("hi"))])
    asyncio.run(agent.reply([], "hello", "919876543210"))
    assert "fallbacks" not in msgs.calls[0] and "betas" not in msgs.calls[0]
