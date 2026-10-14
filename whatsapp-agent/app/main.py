"""FastAPI app: Meta webhook endpoints and the message-processing pipeline."""

from __future__ import annotations

import asyncio
import json
import logging
from collections import defaultdict
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from .agent import FALLBACK_REPLY, Agent
from .config import Settings, get_settings, mask_phone, normalize_phone
from .shopify import ShopifyClient
from .store import Store
from .whatsapp import IncomingMessage, WhatsAppClient, parse_webhook, verify_signature

log = logging.getLogger("grasscrafts")

RATE_LIMIT_REPLY = (
    "You've sent quite a few messages in a short time 🙏 I'll pause for a bit. "
    "If it's urgent, please use https://grasscrafts.com/pages/contact and our team will help."
)
NON_TEXT_REPLY = (
    "Thanks! I can only read text messages for now. Could you please type your question? 🙂"
)
OWNER_HELP = (
    "GrassCrafts bot commands:\n"
    "/pause <number> - stop auto-replies to a customer (you take over)\n"
    "/resume <number> - turn auto-replies back on\n"
    "/reply <number> <message> - send a message to a customer through the bot\n"
    "/status - show paused customers"
)


@dataclass
class Services:
    settings: Settings
    store: Store
    whatsapp: WhatsAppClient
    shopify: ShopifyClient
    agent: Agent


def build_services(settings: Settings) -> Services:
    store = Store(settings.database_path, settings.history_turns, settings.history_ttl_hours)
    wa = WhatsAppClient(settings)
    shop = ShopifyClient(settings)
    return Services(settings, store, wa, shop, Agent(settings, shop, wa))


class Processor:
    """Handles one inbound message end to end. One customer is processed at a time."""

    def __init__(self, services: Services):
        self.s = services
        self._locks: dict[str, asyncio.Lock] = defaultdict(asyncio.Lock)

    async def handle(self, msg: IncomingMessage) -> None:
        async with self._locks[msg.from_phone]:
            try:
                await self._handle(msg)
            except Exception:
                log.exception("processing failed for customer=%s", mask_phone(msg.from_phone))
                try:
                    await self.s.whatsapp.send_text(msg.from_phone, FALLBACK_REPLY)
                except Exception:
                    log.exception("fallback send failed")

    async def _handle(self, msg: IncomingMessage) -> None:
        settings, store, wa = self.s.settings, self.s.store, self.s.whatsapp
        phone = msg.from_phone
        log.info(
            "inbound id=%s from=%s type=%s chars=%d",
            msg.message_id[-8:],
            mask_phone(phone),
            msg.kind,
            len(msg.text or ""),
        )
        log.debug("inbound body: %s", msg.text)
        await wa.mark_read(msg.message_id)

        if settings.owner_phone and phone == settings.owner_phone:
            await self.owner_command(msg.text or "")
            return

        if settings.paused or store.is_paused(phone):
            if msg.text:
                store.append(phone, "user", msg.text)
            if settings.owner_phone and not settings.paused:
                # Forward to the owner so they can answer during a takeover.
                name = f"{msg.name} " if msg.name else ""
                await wa.send_text(
                    settings.owner_phone,
                    f"💬 {name}+{phone} (paused): {msg.text or '[' + msg.kind + ']'}",
                )
            log.info("auto-reply paused for %s", mask_phone(phone))
            return

        count = store.hit(phone)
        if count > settings.rate_limit_per_hour:
            if count == settings.rate_limit_per_hour + 1:
                await wa.send_text(phone, RATE_LIMIT_REPLY)
            log.warning("rate limit hit for %s (%d/h)", mask_phone(phone), count)
            return

        if not msg.text:
            await wa.send_text(phone, NON_TEXT_REPLY)
            return

        history = store.history(phone)
        reply = await self.s.agent.reply(history, msg.text, phone, msg.name)
        store.append(phone, "user", msg.text)
        store.append(phone, "assistant", reply)
        await wa.send_text(phone, reply)

    async def owner_command(self, text: str) -> None:
        settings, store, wa = self.s.settings, self.s.store, self.s.whatsapp
        owner = settings.owner_phone
        parts = text.strip().split(maxsplit=1)
        cmd = parts[0].lower() if parts else ""
        arg = parts[1] if len(parts) > 1 else ""

        if cmd in {"/pause", "/resume"}:
            target = normalize_phone(arg, settings.default_country_code)
            if len(target) < 11:
                await wa.send_text(owner, f"Please give a number, e.g. {cmd} 9876543210")
                return
            if cmd == "/pause":
                store.pause(target)
                await wa.send_text(owner, f"⏸️ Auto-replies paused for +{target}.")
            else:
                store.resume(target)
                await wa.send_text(owner, f"▶️ Auto-replies resumed for +{target}.")
            log.info("owner %s %s", cmd, mask_phone(target))
        elif cmd == "/reply":
            num, _, body = arg.partition(" ")
            target = normalize_phone(num, settings.default_country_code)
            if len(target) < 11 or not body.strip():
                await wa.send_text(owner, "Usage: /reply 9876543210 your message")
                return
            await wa.send_text(target, body.strip())
            store.append(target, "assistant", body.strip())
            await wa.send_text(owner, f"✅ Sent to +{target}.")
        elif cmd == "/status":
            paused = store.paused_list()
            lines = [f"Global PAUSED: {'yes' if settings.paused else 'no'}"]
            lines.append("Paused customers: " + (", ".join("+" + p for p in paused) or "none"))
            await wa.send_text(owner, "\n".join(lines))
        else:
            await wa.send_text(owner, OWNER_HELP)


def create_app(settings: Settings | None = None, services: Services | None = None) -> FastAPI:
    settings = settings or (services.settings if services else get_settings())
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    # httpx logs full request URLs at INFO; keep them quiet.
    logging.getLogger("httpx").setLevel(logging.WARNING)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if app.state.services is None:
            app.state.services = build_services(settings)
        app.state.processor = Processor(app.state.services)
        app.state.services.store.prune()
        yield
        await app.state.services.whatsapp.aclose()
        await app.state.services.shopify.aclose()

    app = FastAPI(title="GrassCrafts WhatsApp Agent", lifespan=lifespan, docs_url=None, redoc_url=None)
    app.state.services = services
    app.state.processor = Processor(services) if services else None

    @app.get("/")
    @app.get("/healthz")
    async def health():
        return {"status": "ok"}

    @app.get("/webhook")
    async def verify(request: Request):
        q = request.query_params
        if (
            q.get("hub.mode") == "subscribe"
            and settings.whatsapp_verify_token
            and q.get("hub.verify_token") == settings.whatsapp_verify_token
        ):
            return PlainTextResponse(q.get("hub.challenge", ""))
        return PlainTextResponse("Forbidden", status_code=403)

    @app.post("/webhook")
    async def receive(request: Request, background: BackgroundTasks):
        body = await request.body()
        if not verify_signature(
            settings.whatsapp_app_secret, body, request.headers.get("X-Hub-Signature-256")
        ):
            log.warning("rejected webhook with invalid signature")
            return JSONResponse({"error": "invalid signature"}, status_code=403)
        try:
            payload = json.loads(body)
        except ValueError:
            return JSONResponse({"error": "invalid json"}, status_code=400)

        store = app.state.services.store
        processor: Processor = app.state.processor
        for msg in parse_webhook(payload):
            if not store.mark_processed(msg.message_id):
                log.info("duplicate message %s ignored", msg.message_id[-8:])
                continue
            background.add_task(processor.handle, msg)
        return {"status": "ok"}

    return app


app = create_app()
