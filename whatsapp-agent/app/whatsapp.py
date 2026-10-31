"""WhatsApp Cloud API: signature check, webhook parsing and outbound messages."""

from __future__ import annotations

import hashlib
import hmac
import logging
import re
from dataclasses import dataclass

import httpx

from .config import Settings, mask_phone

log = logging.getLogger(__name__)

MAX_TEXT_LEN = 4096


# ------------------------------------------------------------------ security
def verify_signature(app_secret: str, body: bytes, header: str | None) -> bool:
    """Check Meta's ``X-Hub-Signature-256: sha256=<hex>`` header against the raw body."""
    if not app_secret or not header or not header.startswith("sha256="):
        return False
    expected = hmac.new(app_secret.encode(), body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, header.split("=", 1)[1].strip())


# ------------------------------------------------------------------- parsing
@dataclass
class IncomingMessage:
    message_id: str
    from_phone: str
    name: str | None
    kind: str  # text | button | interactive | image | audio | ...
    text: str | None  # None when there is nothing readable (e.g. a voice note)
    timestamp: str | None = None


def parse_webhook(payload: dict) -> list[IncomingMessage]:
    """Extract customer messages from a webhook payload. Status callbacks are ignored."""
    out: list[IncomingMessage] = []
    if not isinstance(payload, dict) or payload.get("object") != "whatsapp_business_account":
        return out
    for entry in payload.get("entry") or []:
        for change in entry.get("changes") or []:
            if change.get("field") != "messages":
                continue
            value = change.get("value") or {}
            names = {
                c.get("wa_id"): (c.get("profile") or {}).get("name")
                for c in value.get("contacts") or []
            }
            # value["statuses"] (sent/delivered/read callbacks) is deliberately skipped.
            for msg in value.get("messages") or []:
                mid, sender, kind = msg.get("id"), msg.get("from"), msg.get("type")
                if not mid or not sender:
                    continue
                text: str | None = None
                if kind == "text":
                    text = (msg.get("text") or {}).get("body")
                elif kind == "button":  # quick-reply button on a template
                    b = msg.get("button") or {}
                    text = b.get("text") or b.get("payload")
                elif kind == "interactive":
                    inter = msg.get("interactive") or {}
                    reply = inter.get("button_reply") or inter.get("list_reply") or {}
                    text = reply.get("title") or reply.get("id")
                elif kind in {"image", "video", "document"}:
                    text = (msg.get(kind) or {}).get("caption")  # may be None
                out.append(
                    IncomingMessage(
                        message_id=mid,
                        from_phone=sender,
                        name=names.get(sender),
                        kind=kind or "unknown",
                        text=text.strip() if isinstance(text, str) and text.strip() else None,
                        timestamp=msg.get("timestamp"),
                    )
                )
    return out


def split_message(text: str, limit: int = MAX_TEXT_LEN) -> list[str]:
    """Split text into chunks <= limit, preferring paragraph, line, then word breaks."""
    text = text.strip()
    if len(text) <= limit:
        return [text] if text else []
    chunks: list[str] = []
    while len(text) > limit:
        window = text[:limit]
        cut = max(window.rfind("\n\n"), window.rfind("\n"), window.rfind(" "))
        if cut < limit // 2:
            cut = limit
        chunks.append(text[:cut].rstrip())
        text = text[cut:].lstrip()
    if text:
        chunks.append(text)
    return chunks


def template_param(value: object, limit: int = 1000) -> str:
    """Meta rejects template variables containing newlines, tabs or 4+ spaces in a row."""
    text = str(value if value is not None else "").replace("\r", "")
    text = re.sub(r"\s*\n\s*", " | ", text.strip())
    text = re.sub(r"[\t ]{2,}", " ", text)
    return (text or "-")[:limit]


# ------------------------------------------------------------------- sending
class WhatsAppClient:
    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None):
        self.settings = settings
        self.http = http or httpx.AsyncClient(timeout=20.0)
        self.url = (
            f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
            f"{settings.whatsapp_phone_number_id}/messages"
        )

    async def aclose(self) -> None:
        await self.http.aclose()

    async def _post(self, payload: dict) -> dict:
        resp = await self.http.post(
            self.url,
            json=payload,
            headers={"Authorization": f"Bearer {self.settings.whatsapp_access_token}"},
        )
        if resp.status_code >= 400:
            # Meta's error body never contains our token; log code + message only.
            try:
                err = resp.json().get("error", {})
            except ValueError:
                err = {}
            log.error(
                "WhatsApp API error status=%s code=%s msg=%s",
                resp.status_code,
                err.get("code"),
                err.get("message"),
            )
            resp.raise_for_status()
        return resp.json()

    async def send_text(self, to: str, text: str) -> None:
        for chunk in split_message(text):
            await self._post(
                {
                    "messaging_product": "whatsapp",
                    "recipient_type": "individual",
                    "to": to,
                    "type": "text",
                    "text": {"preview_url": True, "body": chunk},
                }
            )
        log.info("sent text to=%s chars=%d", mask_phone(to), len(text))

    async def send_image(self, to: str, image_url: str, caption: str = "") -> None:
        image: dict = {"link": image_url}
        if caption:
            image["caption"] = caption[:1024]
        await self._post(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "image",
                "image": image,
            }
        )
        log.info("sent image to=%s", mask_phone(to))

    async def send_document(self, to: str, link: str, filename: str, caption: str = "") -> None:
        document: dict = {"link": link, "filename": filename}
        if caption:
            document["caption"] = caption[:1024]
        await self._post(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to,
                "type": "document",
                "document": document,
            }
        )
        log.info("sent document to=%s", mask_phone(to))

    async def send_template(self, to: str, name: str, lang: str, body_params: list[str]) -> dict:
        return await self._post(
            {
                "messaging_product": "whatsapp",
                "to": to,
                "type": "template",
                "template": {
                    "name": name,
                    "language": {"code": lang},
                    "components": [
                        {
                            "type": "body",
                            "parameters": [
                                {"type": "text", "text": template_param(p)} for p in body_params
                            ],
                        }
                    ],
                },
            }
        )

    async def mark_read(self, message_id: str) -> None:
        try:
            await self._post(
                {"messaging_product": "whatsapp", "status": "read", "message_id": message_id}
            )
        except Exception:  # read receipts are best-effort
            log.warning("mark_read failed for message")
