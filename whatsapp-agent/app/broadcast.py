"""Send an approved MARKETING template to a customer segment.

    python -m app.broadcast --template diwali_offer --segment opted_in --param "{name}" --param DIWALI10
    python -m app.broadcast --template diwali_offer --segment opted_in --param "{name}" --param DIWALI10 --confirm

Without --confirm it is a dry run: nothing is sent, you see who would get it.
--confirm also needs BROADCAST_ENABLED=true. "{name}" in a --param becomes the customer's first name.
Opted-out customers are always skipped, each number gets a campaign at most once, and sends
are rate-limited (BROADCAST_RATE_PER_SECOND). Every recipient's result is logged in SQLite.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys
from datetime import datetime
from typing import Awaitable, Callable

from .automations import Notifier
from .config import Settings, get_settings, mask_phone
from .consent import MARKETING, can_send
from .store import Store
from .templates_sync import find_template
from .whatsapp import WhatsAppClient

log = logging.getLogger(__name__)


class BroadcastError(Exception):
    pass


def render_params(params: list[str], name: str | None) -> list[str]:
    first = (name or "").split()[0] if (name or "").strip() else "there"
    return [p.replace("{name}", first) for p in params]


async def run_broadcast(
    settings: Settings,
    store: Store,
    whatsapp,
    template: str,
    segment: str,
    params: list[str],
    confirm: bool = False,
    campaign: str | None = None,
    limit: int | None = None,
    rate_per_second: float | None = None,
    sleep: Callable[[float], Awaitable[None]] = asyncio.sleep,
    out: Callable[[str], None] = print,
) -> dict:
    spec = find_template(settings.templates_path, template)
    if spec is None:
        raise BroadcastError(f"Template '{template}' is not in {settings.templates_path}.")
    if spec["category"] != MARKETING:
        raise BroadcastError(f"'{template}' is a {spec['category']} template; broadcasts use MARKETING templates only.")
    if settings.template_lang not in spec["languages"]:
        raise BroadcastError(f"'{template}' has no '{settings.template_lang}' version (TEMPLATE_LANG).")
    if len(params) != len(spec.get("params", [])):
        raise BroadcastError(
            f"'{template}' needs {len(spec.get('params', []))} --param values ({', '.join(spec.get('params', []))}); got {len(params)}."
        )
    if confirm and not settings.broadcast_enabled:
        raise BroadcastError("Broadcasts are switched off. Set BROADCAST_ENABLED=true to send.")

    campaign = campaign or f"{template}-{datetime.now().strftime('%Y%m%d')}"
    recipients = store.segment(segment)
    if limit:
        recipients = recipients[:limit]
    rate = rate_per_second or settings.broadcast_rate_per_second
    notifier = Notifier(settings, store, whatsapp)
    counts: dict[str, int] = {}
    mode = "SENDING" if confirm else "DRY RUN (add --confirm to send)"
    out(f"{mode}: template={template} campaign={campaign} segment={segment} recipients={len(recipients)}")

    for i, r in enumerate(recipients):
        phone = r["phone"]
        values = render_params(params, r.get("name"))
        allowed, reason = can_send(store, settings, phone, MARKETING)
        if not allowed:
            status = f"skipped:{reason}"
        elif not confirm:
            status = "would_send"
        else:
            try:
                status = await notifier.send_template_once(
                    f"broadcast:{campaign}:{phone}", phone, template, values, MARKETING
                )
            except Exception as exc:
                status = f"failed:{exc}"
            if i < len(recipients) - 1 and rate > 0:
                await sleep(1.0 / rate)
        if confirm:
            store.log_broadcast(campaign, template, phone, status)
        counts[status] = counts.get(status, 0) + 1
        out(f"  {mask_phone(phone):<10} {status:<22} {' | '.join(values)}")

    summary = ", ".join(f"{k}: {v}" for k, v in sorted(counts.items())) or "no recipients"
    out(f"Done. {summary}")
    return {"campaign": campaign, "counts": counts, "sent": counts.get("sent", 0)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", required=True)
    parser.add_argument("--segment", default="opted_in", choices=["opted_in"])
    parser.add_argument("--param", action="append", default=[], help='template variable, in order; "{name}" = first name')
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--dry-run", action="store_true", help="default: show who would receive it")
    group.add_argument("--confirm", action="store_true", help="actually send")
    parser.add_argument("--campaign", help="campaign id (default: template-YYYYMMDD); re-runs skip numbers already sent")
    parser.add_argument("--limit", type=int, help="only the first N recipients (test with a small batch)")
    parser.add_argument("--rate", type=float, help="messages per second (default BROADCAST_RATE_PER_SECOND)")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.WARNING)
    settings = get_settings()
    store = Store(settings.database_path, settings.history_turns, settings.history_ttl_hours)

    async def go() -> dict:
        wa = WhatsAppClient(settings)
        try:
            return await run_broadcast(
                settings, store, wa, args.template, args.segment, args.param,
                confirm=args.confirm, campaign=args.campaign, limit=args.limit, rate_per_second=args.rate,
            )
        finally:
            await wa.aclose()

    try:
        asyncio.run(go())
    except BroadcastError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
