import hashlib
import hmac
import json
import sys
from pathlib import Path

import httpx
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from app.config import Settings  # noqa: E402

APP_SECRET = "test-app-secret"
VERIFY_TOKEN = "test-verify-token"


@pytest.fixture
def settings(tmp_path):
    return Settings(
        whatsapp_verify_token=VERIFY_TOKEN,
        whatsapp_app_secret=APP_SECRET,
        whatsapp_access_token="wa-token",
        whatsapp_phone_number_id="123456",
        owner_whatsapp_number="+91 99999 00000",
        shopify_admin_token="shpat_test",
        anthropic_api_key="sk-test",
        database_path=str(tmp_path / "test.db"),
        store_facts_path=str(ROOT / "store_facts.md"),
    )


def sign(body: bytes, secret: str = APP_SECRET) -> str:
    return "sha256=" + hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()


class Recorder:
    """httpx MockTransport handler that records requests and returns canned responses."""

    def __init__(self, responder=None):
        self.requests: list[httpx.Request] = []
        self.responder = responder or (lambda req: httpx.Response(200, json={"messages": [{"id": "wamid.out"}]}))

    def __call__(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        return self.responder(request)

    def bodies(self):
        return [json.loads(r.content) for r in self.requests]


def text_payload(msg_id="wamid.1", sender="919876543210", body="Hi", name="Asha"):
    return {
        "object": "whatsapp_business_account",
        "entry": [
            {
                "id": "WABA",
                "changes": [
                    {
                        "field": "messages",
                        "value": {
                            "messaging_product": "whatsapp",
                            "metadata": {"phone_number_id": "123456"},
                            "contacts": [{"wa_id": sender, "profile": {"name": name}}],
                            "messages": [
                                {
                                    "id": msg_id,
                                    "from": sender,
                                    "timestamp": "1700000000",
                                    "type": "text",
                                    "text": {"body": body},
                                }
                            ],
                        },
                    }
                ],
            }
        ],
    }
