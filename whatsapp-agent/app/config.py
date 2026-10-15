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


def _float(value: str | None, default: float) -> float:
    try:
        return float(value) if value not in (None, "") else default
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

    # ---- Automations (see README "Automations"). Anything that messages customers first is OFF by default.
    whatsapp_business_account_id: str = ""  # WABA ID, used by `python -m app.templates_sync`
    template_lang: str = "en"  # language code used when sending templates
    templates_path: str = str(BASE_DIR / "templates" / "whatsapp_templates.json")

    # 1. Bulk / corporate lead capture (in-chat only, so on by default)
    lead_capture_enabled: bool = True
    catalogue_pdf_url: str = ""
    catalogue_filename: str = "GrassCrafts-Corporate-Catalogue.pdf"

    # 2. Shopify webhooks and follow-up messages
    shopify_webhook_secret: str = field(default="", repr=False)
    order_confirmation_enabled: bool = False
    shipping_update_enabled: bool = False
    abandoned_cart_enabled: bool = False
    abandoned_cart_delay_minutes: int = 60
    review_request_enabled: bool = False
    review_request_days: int = 7
    review_url: str = ""
    scheduler_interval_seconds: int = 60

    # 3. Opt-in / opt-out
    opt_out_enabled: bool = True
    marketing_requires_opt_in: bool = True  # marketing templates only to customers with a recorded opt-in
    utility_requires_opt_in: bool = False  # order/shipping updates also need a recorded opt-in

    # 4. Broadcasts (CLI)
    broadcast_enabled: bool = False
    broadcast_rate_per_second: float = 5.0

    # 5. Owner daily digest
    digest_enabled: bool = False
    digest_hour: int = 9  # IST, 0-23
    digest_channels: str = "whatsapp,email"

    # 6. Admin dashboard (disabled while ADMIN_PASSWORD is empty)
    admin_user: str = "admin"
    admin_password: str = field(default="", repr=False)

    @property
    def review_link(self) -> str:
        return self.review_url or self.storefront_base_url

    @property
    def scheduler_needed(self) -> bool:
        return any(
            (
                self.order_confirmation_enabled,
                self.shipping_update_enabled,
                self.abandoned_cart_enabled,
                self.review_request_enabled,
                self.digest_enabled,
            )
        )

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
            whatsapp_business_account_id=e("WHATSAPP_BUSINESS_ACCOUNT_ID", ""),
            template_lang=e("TEMPLATE_LANG", "en"),
            templates_path=e(
                "TEMPLATES_PATH", str(BASE_DIR / "templates" / "whatsapp_templates.json")
            ),
            lead_capture_enabled=_bool(e("LEAD_CAPTURE_ENABLED"), True),
            catalogue_pdf_url=e("CATALOGUE_PDF_URL", ""),
            catalogue_filename=e("CATALOGUE_FILENAME", "GrassCrafts-Corporate-Catalogue.pdf"),
            shopify_webhook_secret=e("SHOPIFY_WEBHOOK_SECRET", ""),
            order_confirmation_enabled=_bool(e("ORDER_CONFIRMATION_ENABLED"), False),
            shipping_update_enabled=_bool(e("SHIPPING_UPDATE_ENABLED"), False),
            abandoned_cart_enabled=_bool(e("ABANDONED_CART_ENABLED"), False),
            abandoned_cart_delay_minutes=_int(e("ABANDONED_CART_DELAY_MINUTES"), 60),
            review_request_enabled=_bool(e("REVIEW_REQUEST_ENABLED"), False),
            review_request_days=_int(e("REVIEW_REQUEST_DAYS"), 7),
            review_url=e("REVIEW_URL", ""),
            scheduler_interval_seconds=_int(e("SCHEDULER_INTERVAL_SECONDS"), 60),
            opt_out_enabled=_bool(e("OPT_OUT_ENABLED"), True),
            marketing_requires_opt_in=_bool(e("MARKETING_REQUIRES_OPT_IN"), True),
            utility_requires_opt_in=_bool(e("UTILITY_REQUIRES_OPT_IN"), False),
            broadcast_enabled=_bool(e("BROADCAST_ENABLED"), False),
            broadcast_rate_per_second=_float(e("BROADCAST_RATE_PER_SECOND"), 5.0),
            digest_enabled=_bool(e("DIGEST_ENABLED"), False),
            digest_hour=min(max(_int(e("DIGEST_HOUR"), 9), 0), 23),
            digest_channels=e("DIGEST_CHANNELS", "whatsapp,email"),
            admin_user=e("ADMIN_USER", "admin"),
            admin_password=e("ADMIN_PASSWORD", ""),
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings.from_env()


def mask_phone(phone: str | None) -> str:
    """For logs: keep only the last 4 digits."""
    d = digits_only(phone)
    return f"***{d[-4:]}" if d else "unknown"
