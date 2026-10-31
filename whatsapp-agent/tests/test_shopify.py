import asyncio
import json

import httpx

from app.shopify import ShopifyClient, normalize_order_number

from .conftest import Recorder

ORDER = {
    "name": "#1234",
    "createdAt": "2026-10-01T10:00:00Z",
    "cancelledAt": None,
    "phone": None,
    "shippingAddress": {"phone": "+91 98765 43210"},
    "displayFinancialStatus": "PAID",
    "displayFulfillmentStatus": "FULFILLED",
    "fulfillments": [
        {"status": "SUCCESS", "trackingInfo": [{"number": "AWB123", "url": "https://track.example/AWB123", "company": "Delhivery"}]}
    ],
    "lineItems": {"nodes": [{"name": "Round Cane Tray", "quantity": 2}]},
}


def shop_with(data, settings):
    rec = Recorder(lambda req: httpx.Response(200, json={"data": data}))
    client = ShopifyClient(settings, httpx.AsyncClient(transport=httpx.MockTransport(rec)))
    return client, rec


def test_order_number_normalisation():
    assert normalize_order_number("1234") == "#1234"
    assert normalize_order_number("#1234") == "#1234"
    assert normalize_order_number("order no. 1234") == "#1234"
    assert normalize_order_number("abc") == ""


def test_order_status_revealed_when_phone_matches(settings):
    shop, rec = shop_with({"orders": {"nodes": [ORDER]}}, settings)
    # WhatsApp sends numbers as country code + number; compare last 10 digits.
    result = asyncio.run(shop.get_order_status("1234", "919876543210"))
    assert result["verified"] is True
    assert result["financial_status"] == "PAID"
    assert result["fulfillment_status"] == "FULFILLED"
    assert result["tracking"] == [{"number": "AWB123", "url": "https://track.example/AWB123", "company": "Delhivery"}]
    assert result["line_items"] == [{"name": "Round Cane Tray", "quantity": 2}]

    req = rec.requests[0]
    assert req.url.path == "/admin/api/2025-01/graphql.json"
    assert req.headers["X-Shopify-Access-Token"] == "shpat_test"
    assert json.loads(req.content)["variables"] == {"q": "name:#1234"}


def test_order_status_matches_order_phone_field(settings):
    order = dict(ORDER, phone="09876543210", shippingAddress={"phone": "+91 11111 22222"})
    shop, _ = shop_with({"orders": {"nodes": [order]}}, settings)
    assert asyncio.run(shop.get_order_status("#1234", "919876543210"))["verified"] is True


def test_order_status_hidden_when_phone_differs(settings):
    shop, _ = shop_with({"orders": {"nodes": [ORDER]}}, settings)
    result = asyncio.run(shop.get_order_status("#1234", "919000000001"))
    assert result["verified"] is False
    for leaked in ("financial_status", "fulfillment_status", "tracking", "line_items", "created_at"):
        assert leaked not in result
    assert "email" in result["message"]
    blob = json.dumps(result)
    assert "AWB123" not in blob and "Cane Tray" not in blob and "PAID" not in blob


def test_order_status_hidden_when_order_has_no_phone(settings):
    order = dict(ORDER, phone=None, shippingAddress=None)
    shop, _ = shop_with({"orders": {"nodes": [order]}}, settings)
    assert asyncio.run(shop.get_order_status("#1234", "919876543210"))["verified"] is False


def test_order_not_found(settings):
    shop, _ = shop_with({"orders": {"nodes": []}}, settings)
    assert asyncio.run(shop.get_order_status("#9999", "919876543210")) == {"found": False, "order_number": "#9999"}


def test_search_products_filters_price_and_formats(settings):
    nodes = [
        {
            "title": "Round Cane Tray", "handle": "round-cane-tray", "status": "ACTIVE",
            "priceRangeV2": {"minVariantPrice": {"amount": "899.0", "currencyCode": "INR"},
                             "maxVariantPrice": {"amount": "1099.0", "currencyCode": "INR"}},
            "featuredMedia": {"preview": {"image": {"url": "https://cdn.shopify.com/tray.jpg"}}},
            "variants": {"nodes": [{"availableForSale": False}, {"availableForSale": True}]},
        },
        {
            "title": "Laundry Basket", "handle": "big-basket", "status": "ACTIVE",
            "priceRangeV2": {"minVariantPrice": {"amount": "5800.0", "currencyCode": "INR"},
                             "maxVariantPrice": {"amount": "5800.0", "currencyCode": "INR"}},
            "featuredMedia": None,
            "variants": {"nodes": [{"availableForSale": False}]},
        },
    ]
    shop, rec = shop_with({"products": {"nodes": nodes}}, settings)
    result = asyncio.run(shop.search_products('tray" OR status:draft', max_price=1000))
    assert result["count"] == 1
    p = result["products"][0]
    assert p == {
        "title": "Round Cane Tray", "handle": "round-cane-tray",
        "url": "https://grasscrafts.com/products/round-cane-tray",
        "price": {"min": 899.0, "max": 1099.0, "currency": "INR"},
        "in_stock": True, "image_url": "https://cdn.shopify.com/tray.jpg",
    }
    q = json.loads(rec.requests[0].content)["variables"]["q"]
    assert q.startswith("status:active ")
    assert ":" not in q[len("status:active "):] and '"' not in q


def test_get_product_inactive_is_not_found(settings):
    shop, _ = shop_with({"productByIdentifier": {"status": "DRAFT", "title": "x", "handle": "x"}}, settings)
    assert asyncio.run(shop.get_product("https://grasscrafts.com/products/x?v=1"))["found"] is False
