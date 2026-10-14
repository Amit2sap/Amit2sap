"""Configuration loaded from environment variables.

Secrets are kept out of ``repr()`` so they never end up in logs or tracebacks.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _bool(value: str | None, default: bool = False) -> bool:
    if value is None or value.strip() == "":
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _int(value: str | None, default: int) -> int:
    try:
        return int(value) if value not in (None, "") else default
    except ValueError:
        return default


def digits_only(value: str | None) -> str:
    return re.sub(r"\D", "", value or "")


def normalize_phone(value: str | None, default_country_code: str = "91") -> str:
    """Return a WhatsApp-style phone id (country code + number, digits only).

    "+91 81004 47884", "08100447884" and "8100447884" all become "918100447884".
    """
    d = digits_only(value)
    if len(d) == 11 and d.startswith("0"):
        d = d[1:]
    if len(d) == 10:
        d = default_country_code + d
    return d


def last10(value: str | None) -> str:
    return digits_only(value)[-10:]


@dataclass(frozen=True)
class Settings:
    # WhatsApp Cloud API
    whatsapp_verify_token: str = field(default="", repr=False)
    whatsapp_app_secret: str = field(default="", repr=False)
    whatsapp_access_token: str = field(default="", repr=False)
    whatsapp_phone_number_id: str = ""
    whatsapp_api_version: str = "v21.0"
    owner_whatsapp_number: str = ""
    owner_alert_template: str = ""  # optional approved template name for owner alerts
    owner_alert_template_lang: str = "en"
    default_country_code: str = "91"

    # Shopify
    shopify_store_domain: str = "605e40-ba.myshopify.com"
    shopify_admin_token: str = field(default="", repr=False)
    shopify_api_version: str = "2025-01"
    storefront_base_url: str = "https://grasscrafts.com"

    # Anthropic
    anthropic_api_key: str = field(default="", repr=False)
    anthropic_model: str = "claude-sonnet-5-5"
    anthropic_effort: str = "low"
    anthropic_max_tokens: int = 8000
    anthropic_refusal_fallback: bool = True
    max_tool_iterations: int = 6

    # Behaviour
    paused: bool = False
    rate_limit_per_hour: int = 20
    history_turns: int = 20
    history_ttl_hours: int = 24
    database_path: str = str(BASE_DIR / "data" / "agent.db")
    store_facts_path: str = str(BASE_DIR / "store_facts.md")
    log_level: str = "INFO"

    # Optional SMTP for escalation e-mails
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = field(default="", repr=False)
    smtp_from: str = ""
    smtp_to: str = ""
    smtp_use_ssl: bool = False

    @property
    def owner_phone(self) -> str:
        return normalize_phone(self.owner_whatsapp_number, self.default_country_code)

    @property
    def smtp_enabled(self) -> bool:
        return bool(self.smtp_host and self.smtp_to and (self.smtp_from or self.smtp_user))

    @classmethod
    def from_env(cls) -> "Settings":
        e = os.environ.get
        return cls(
            whatsapp_verify_token=e("WHATSAPP_VERIFY_TOKEN", ""),
            whatsapp_app_secret=e("WHATSAPP_APP_SECRET", ""),
            whatsapp_access_token=e("WHATSAPP_ACCESS_TOKEN", ""),
            whatsapp_phone_number_id=e("WHATSAPP_PHONE_NUMBER_ID", ""),
            whatsapp_api_version=e("WHATSAPP_API_VERSION", "v21.0"),
            owner_whatsapp_number=e("OWNER_WHATSAPP_NUMBER", ""),
            owner_alert_template=e("OWNER_ALERT_TEMPLATE", ""),
            owner_alert_template_lang=e("OWNER_ALERT_TEMPLATE_LANG", "en"),
            default_country_code=e("DEFAULT_COUNTRY_CODE", "91"),
            shopify_store_domain=e("SHOPIFY_STORE_DOMAIN", "605e40-ba.myshopify.com"),
            shopify_admin_token=e("SHOPIFY_ADMIN_TOKEN", ""),
            shopify_api_version=e("SHOPIFY_API_VERSION", "2025-01"),
            storefront_base_url=e("STOREFRONT_BASE_URL", "https://grasscrafts.com").rstrip("/"),
            anthropic_api_key=e("ANTHROPIC_API_KEY", ""),
            anthropic_model=e("ANTHROPIC_MODEL", "claude-sonnet-5-5"),
            anthropic_effort=e("ANTHROPIC_EFFORT", "low"),
            anthropic_max_tokens=_int(e("ANTHROPIC_MAX_TOKENS"), 8000),
            anthropic_refusal_fallback=_bool(e("ANTHROPIC_REFUSAL_FALLBACK"), True),
            max_tool_iterations=_int(e("MAX_TOOL_ITERATIONS"), 6),
            paused=_bool(e("PAUSED"), False),
            rate_limit_per_hour=_int(e("RATE_LIMIT_PER_HOUR"), 20),
            history_turns=_int(e("HISTORY_TURNS"), 20),
            history_ttl_hours=_int(e("HISTORY_TTL_HOURS"), 24),
            database_path=e("DATABASE_PATH", str(BASE_DIR / "data" / "agent.db")),
            store_facts_path=e("STORE_FACTS_PATH", str(BASE_DIR / "store_facts.md")),
            log_level=e("LOG_LEVEL", "INFO"),
            smtp_host=e("SMTP_HOST", ""),
            smtp_port=_int(e("SMTP_PORT"), 587),
            smtp_user=e("SMTP_USER", ""),
            smtp_password=e("SMTP_PASSWORD", ""),
            smtp_from=e("SMTP_FROM", ""),
            smtp_to=e("SMTP_TO", ""),
            smtp_use_ssl=_bool(e("SMTP_USE_SSL"), False),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()


def mask_phone(phone: str | None) -> str:
    """For logs: keep only the last 4 digits."""
    d = digits_only(phone)
    return f"***{d[-4:]}" if d else "unknown"
