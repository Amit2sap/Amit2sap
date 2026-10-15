"""Read-only Shopify Admin GraphQL client used by the agent's tools, and webhook verification."""

from __future__ import annotations

import base64
import hashlib
import hmac
import logging
import re

import httpx

from .config import Settings, last10

log = logging.getLogger(__name__)


class ShopifyError(Exception):
    pass


SEARCH_PRODUCTS = """
query SearchProducts($q: String!, $first: Int!) {
  products(first: $first, query: $q, sortKey: RELEVANCE) {
    nodes {
      title
      handle
      status
      priceRangeV2 {
        minVariantPrice { amount currencyCode }
        maxVariantPrice { amount currencyCode }
      }
      featuredMedia { preview { image { url } } }
      variants(first: 20) { nodes { availableForSale } }
    }
  }
}
"""

GET_PRODUCT = """
query GetProduct($handle: String!) {
  productByIdentifier(identifier: {handle: $handle}) {
    title
    handle
    status
    description(truncateAt: 500)
    priceRangeV2 {
      minVariantPrice { amount currencyCode }
      maxVariantPrice { amount currencyCode }
    }
    featuredMedia { preview { image { url } } }
    variants(first: 30) { nodes { title price availableForSale } }
  }
}
"""

GET_ORDER = """
query GetOrder($q: String!) {
  orders(first: 1, query: $q, sortKey: CREATED_AT, reverse: true) {
    nodes {
      name
      createdAt
      cancelledAt
      phone
      shippingAddress { phone }
      displayFinancialStatus
      displayFulfillmentStatus
      fulfillments(first: 5) {
        status
        trackingInfo(first: 3) { number url company }
      }
      lineItems(first: 30) { nodes { name quantity } }
    }
  }
}
"""


def verify_webhook_hmac(secret: str, body: bytes, header: str | None) -> bool:
    """Check Shopify's ``X-Shopify-Hmac-Sha256`` (base64 HMAC-SHA256 of the raw body)."""
    if not secret or not header:
        return False
    digest = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    expected = base64.b64encode(digest).decode()
    return hmac.compare_digest(expected, header.strip())


def _sanitize_search(text: str) -> str:
    """Strip Shopify search-syntax characters so customer text can't alter the filter."""
    cleaned = re.sub(r"[^\w\s\-]", " ", text, flags=re.UNICODE)
    return " ".join(cleaned.split())[:100]


def _money(m: dict | None) -> float | None:
    try:
        return float(m["amount"]) if m else None
    except (KeyError, TypeError, ValueError):
        return None


def _price_range(p: dict) -> dict:
    pr = p.get("priceRangeV2") or {}
    lo, hi = _money(pr.get("minVariantPrice")), _money(pr.get("maxVariantPrice"))
    cur = (pr.get("minVariantPrice") or {}).get("currencyCode", "INR")
    return {"min": lo, "max": hi, "currency": cur}


def _image(p: dict) -> str | None:
    return (((p.get("featuredMedia") or {}).get("preview") or {}).get("image") or {}).get("url")


def normalize_order_number(order_number: str) -> str:
    d = re.sub(r"\D", "", order_number or "")
    return f"#{d}" if d else ""


class ShopifyClient:
    def __init__(self, settings: Settings, http: httpx.AsyncClient | None = None):
        self.settings = settings
        self.http = http or httpx.AsyncClient(timeout=20.0)
        self.endpoint = (
            f"https://{settings.shopify_store_domain}/admin/api/"
            f"{settings.shopify_api_version}/graphql.json"
        )

    async def aclose(self) -> None:
        await self.http.aclose()

    def product_url(self, handle: str) -> str:
        return f"{self.settings.storefront_base_url}/products/{handle}"

    async def graphql(self, query: str, variables: dict) -> dict:
        resp = await self.http.post(
            self.endpoint,
            json={"query": query, "variables": variables},
            headers={
                "X-Shopify-Access-Token": self.settings.shopify_admin_token,
                "Content-Type": "application/json",
            },
        )
        if resp.status_code >= 400:
            log.error("Shopify HTTP %s", resp.status_code)
            raise ShopifyError(f"Shopify returned HTTP {resp.status_code}")
        data = resp.json()
        if data.get("errors"):
            log.error("Shopify GraphQL errors: %s", str(data["errors"])[:300])
            raise ShopifyError("Shopify query failed")
        return data.get("data") or {}

    # ---------------------------------------------------------------- tools
    async def search_products(self, query: str, max_price: float | None = None) -> dict:
        terms = _sanitize_search(query)
        q = f"status:active {terms}".strip()
        data = await self.graphql(SEARCH_PRODUCTS, {"q": q, "first": 25})
        results = []
        for p in (data.get("products") or {}).get("nodes") or []:
            if p.get("status") != "ACTIVE":
                continue
            price = _price_range(p)
            if max_price is not None and price["min"] is not None and price["min"] > max_price:
                continue
            variants = (p.get("variants") or {}).get("nodes") or []
            results.append(
                {
                    "title": p.get("title"),
                    "handle": p.get("handle"),
                    "url": self.product_url(p.get("handle", "")),
                    "price": price,
                    "in_stock": any(v.get("availableForSale") for v in variants),
                    "image_url": _image(p),
                }
            )
            if len(results) >= 8:
                break
        return {"query": terms, "max_price": max_price, "count": len(results), "products": results}

    async def get_product(self, handle: str) -> dict:
        handle = (handle or "").strip().lower()
        if "/products/" in handle:
            handle = handle.split("/products/", 1)[1]
        handle = re.sub(r"[^a-z0-9\-]", "", handle.split("?")[0])
        if not handle:
            return {"found": False, "error": "No product handle given."}
        data = await self.graphql(GET_PRODUCT, {"handle": handle})
        p = data.get("productByIdentifier")
        if not p or p.get("status") != "ACTIVE":
            return {"found": False, "handle": handle}
        variants = [
            {
                "title": v.get("title"),
                "price": float(v["price"]) if v.get("price") is not None else None,
                "in_stock": bool(v.get("availableForSale")),
            }
            for v in (p.get("variants") or {}).get("nodes") or []
        ]
        return {
            "found": True,
            "title": p.get("title"),
            "handle": p.get("handle"),
            "url": self.product_url(p.get("handle", "")),
            "price": _price_range(p),
            "in_stock": any(v["in_stock"] for v in variants),
            "variants": variants,
            "description": " ".join((p.get("description") or "").split()),
            "image_url": _image(p),
        }

    async def get_order_status(self, order_number: str, sender_phone: str) -> dict:
        name = normalize_order_number(order_number)
        if not name:
            return {"found": False, "message": "Please share your order number, e.g. #1234."}
        data = await self.graphql(GET_ORDER, {"q": f"name:{name}"})
        nodes = (data.get("orders") or {}).get("nodes") or []
        order = next((o for o in nodes if o.get("name") == name), None)
        if not order:
            return {"found": False, "order_number": name}

        sender = last10(sender_phone)
        phones = {
            last10(order.get("phone")),
            last10((order.get("shippingAddress") or {}).get("phone")),
        } - {""}
        if not sender or sender not in phones:
            # PRIVACY: never reveal anything about an order that isn't linked to this number.
            return {
                "found": True,
                "verified": False,
                "order_number": name,
                "message": (
                    "This WhatsApp number does not match the phone on the order, so the "
                    "status cannot be shared here. Ask the customer to email from the address "
                    "used on the order, or to share the order number and that email so the "
                    "team can verify and follow up."
                ),
            }

        tracking = []
        for f in order.get("fulfillments") or []:
            for t in f.get("trackingInfo") or []:
                tracking.append(
                    {"number": t.get("number"), "url": t.get("url"), "company": t.get("company")}
                )
        return {
            "found": True,
            "verified": True,
            "order_number": name,
            "created_at": order.get("createdAt"),
            "cancelled": bool(order.get("cancelledAt")),
            "financial_status": order.get("displayFinancialStatus"),
            "fulfillment_status": order.get("displayFulfillmentStatus"),
            "tracking": tracking,
            "line_items": [
                {"name": li.get("name"), "quantity": li.get("quantity")}
                for li in (order.get("lineItems") or {}).get("nodes") or []
            ],
        }
