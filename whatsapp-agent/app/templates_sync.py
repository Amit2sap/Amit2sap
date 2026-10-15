"""Create the WhatsApp message templates in Meta and show their approval status.

    python -m app.templates_sync              # create any missing templates, then show status
    python -m app.templates_sync --status     # only show status
    python -m app.templates_sync --dry-run    # print what would be submitted
    python -m app.templates_sync --only diwali_offer

Needs WHATSAPP_ACCESS_TOKEN and WHATSAPP_BUSINESS_ACCOUNT_ID (the WABA ID).
Template text lives in templates/whatsapp_templates.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import httpx

from .config import Settings, get_settings


def load_templates(path: str) -> list[dict]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["templates"]


def find_template(path: str, name: str) -> dict | None:
    return next((t for t in load_templates(path) if t["name"] == name), None)


def build_requests(template: dict) -> list[dict]:
    """One Graph API request body per language."""
    out = []
    for lang, spec in template["languages"].items():
        components: list[dict] = [
            {"type": "BODY", "text": spec["body"], "example": {"body_text": [spec["example"]]}}
        ]
        if template.get("footer"):
            components.append({"type": "FOOTER", "text": template["footer"]})
        if template.get("buttons"):
            components.append({"type": "BUTTONS", "buttons": template["buttons"]})
        out.append(
            {
                "name": template["name"],
                "language": lang,
                "category": template["category"],
                "components": components,
            }
        )
    return out


def _endpoint(settings: Settings) -> str:
    return (
        f"https://graph.facebook.com/{settings.whatsapp_api_version}/"
        f"{settings.whatsapp_business_account_id}/message_templates"
    )


def create_templates(settings: Settings, templates: list[dict], http: httpx.Client) -> list[tuple[str, str, str]]:
    results = []
    headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
    for template in templates:
        for body in build_requests(template):
            resp = http.post(_endpoint(settings), json=body, headers=headers)
            if resp.status_code < 400:
                status = resp.json().get("status", "submitted")
            else:
                try:
                    err = resp.json().get("error", {})
                except ValueError:
                    err = {}
                text = err.get("error_user_msg") or err.get("message") or f"HTTP {resp.status_code}"
                status = "already exists" if "already exists" in text.lower() else f"error: {text}"
            results.append((body["name"], body["language"], status))
    return results


def fetch_status(settings: Settings, http: httpx.Client) -> list[dict]:
    headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
    url = _endpoint(settings)
    params: dict | None = {"fields": "name,language,status,category,rejected_reason", "limit": 100}
    rows: list[dict] = []
    while url:
        resp = http.get(url, params=params, headers=headers)
        resp.raise_for_status()
        data = resp.json()
        rows += data.get("data", [])
        url = (data.get("paging") or {}).get("next")
        params = None  # the "next" link already carries the query
    return rows


def main(argv: list[str] | None = None, settings: Settings | None = None, http: httpx.Client | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--status", action="store_true", help="only show approval status")
    parser.add_argument("--dry-run", action="store_true", help="print the requests without sending")
    parser.add_argument("--only", action="append", help="template name (repeatable)")
    args = parser.parse_args(argv)
    settings = settings or get_settings()

    templates = load_templates(settings.templates_path)
    if args.only:
        templates = [t for t in templates if t["name"] in set(args.only)]
    if args.dry_run:
        for t in templates:
            for body in build_requests(t):
                print(json.dumps(body, ensure_ascii=False, indent=2))
        return 0
    if not settings.whatsapp_access_token or not settings.whatsapp_business_account_id:
        print("Set WHATSAPP_ACCESS_TOKEN and WHATSAPP_BUSINESS_ACCOUNT_ID first.", file=sys.stderr)
        return 2

    http = http or httpx.Client(timeout=30.0)
    if not args.status:
        print("Submitting templates to Meta:")
        for name, lang, status in create_templates(settings, templates, http):
            print(f"  {name:<20} {lang:<4} {status}")
        print()
    wanted = {t["name"] for t in templates}
    print("Approval status in WhatsApp Manager:")
    for row in sorted(fetch_status(settings, http), key=lambda r: (r.get("name", ""), r.get("language", ""))):
        if row.get("name") in wanted:
            reason = row.get("rejected_reason")
            extra = f" ({reason})" if reason and reason != "NONE" else ""
            print(f"  {row.get('name', ''):<20} {row.get('language', ''):<4} {row.get('category', ''):<10} {row.get('status', '')}{extra}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
