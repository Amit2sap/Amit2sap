# Maker-direct landing content on 4 collections (22 Oct 2026)

Owner approval: Amit, 22 Oct 2026 ("go"). This approval replaced the usual 48h notice for these 4 collections only. No theme edits.
Backup of the old descriptionHtml + SEO title/description: `backups/collections/landing_before_2026-10-22.json`.
Change: `collectionUpdate` (descriptionHtml + seo) on each collection. No products, prices, discounts or themes touched.

| Collection | ID | New SEO title (chars) | Meta (chars) | From ₹ | Sizes table |
|---|---|---|---|---|---|
| https://grasscrafts.com/collections/diamond-jewellery-boxes | 349642490029 | Handwoven Jewellery Boxes & Watch Boxes, Bulk \| GrassCrafts (59) | 154 | ₹450 | 8 products |
| https://grasscrafts.com/collections/diwali-gift-hampers | 349642293421 | Eco Diwali Hamper Baskets & Gift Baskets \| GrassCrafts (54) | 153 | ₹200 | 8 products |
| https://grasscrafts.com/collections/wedding-gift-hamper | 321301938349 | Wedding Hamper Baskets & Trousseau Baskets \| GrassCrafts (56) | 147 | ₹340 | 2 products (only 2 with verified dimensions) |
| https://grasscrafts.com/collections/corporate-gifts-handcrafted-gifts | 330091004077 | Eco Corporate Gift Baskets & Diwali Hampers \| GrassCrafts (57) | 156 | ₹199 | 8 products |

"From ₹" = lowest live variant price among ACTIVE products in the collection on 22 Oct 2026 (archived products ignored).

## What each description now has
- H2 + 2-3 short paragraphs: GrassCrafts is the maker (Kolkata, since 2015, handwoven by Indian artisans; no artisan counts), materials, which products suit which use.
- Sizes table (product, size, material) built only from dimensions stated in product descriptions or variant options.
- Delivery: free shipping in India from ₹1,299 (₹120 below), Cash on Delivery, no GST, 3-day returns with unboxing video.
- Bulk line linking to https://grasscrafts.com/pages/wholesale-corporate-gifting ("custom sizes and branding on request; trade price list on request"). No MOQ, lead times or trade discounts.
- 5 FAQs (care, sizes, bulk, delivery, materials) + FAQPage JSON-LD in a `<script type="application/ld+json">` block (parsed OK; stored intact in Shopify, confirmed by Admin API read-back).
- Links to related blog guides and to the other 3 landing collections.
- Jewellery only: "For jewellers and watch retailers" section (bridal sets, display tray, gift-with-purchase, natural-fibre alternative to plastic packaging).

## Kept / removed from the old text
- Kept: Diwali and corporate "shop by budget" bands; DIWALI10 line (verified ACTIVE in Shopify, ends 12 Nov 2026, end date now shown); custom hampers, branded tags, custom colours on selected Sabai boxes, gift cards.
- Removed (could not be verified): "supports women artisans", "master weavers", "100% natural/biodegradable", "ESG goals". Fixed old shipping threshold "₹1,300" to ₹1,299.

## Products left out of size tables (no verified dimensions or conflicting data)
- Jewellery: Sabai Grass Pot-Shaped Box (box-1; title/description say 5.5 in, variants say 8 in / 10 in), Natural Grass Fibre Storage Box (material unclear: grass vs cane), Water Hyacinth Round Box with Jali Lid, Bespoke Water Hyacinth Coffer, Sabai Round Jewellery Basket, Oval Kauna Jewellery Box, Kauna Display Tray (all "dimensions to be added").
- Wedding: Kash Grass Wedding Hamper Basket, Straw Wedding Hamper Basket, Cane Wedding/Trousseau Basket (no dimensions anywhere). The page asks buyers to WhatsApp for these sizes.
- Diwali: Rectangular water hyacinth placemats (description gives a diameter for a rectangular mat), plus items without dimensions.

## Verification
- Admin API read-back: all 4 collections show the new descriptionHtml (with the JSON-LD script intact) and the new SEO title/description.
- Live storefront fetch: NOT done. Direct curl gets a proxy 403, WebFetch cannot resolve grasscrafts.com, and the Composio workbench and remote bash returned "Failed to execute in sandbox" (5 tries). Re-check on the next run: each URL returns 200, shows the H2, and the FAQPage JSON-LD parses.

## Follow-ups
- After 12 Nov 2026: remove the DIWALI10 heading from diwali-gift-hampers (back up first).
- Ask Sristi for the dimensions of the Kash, straw and cane wedding baskets, then add them to the wedding table (it has 2 rows; target was 4-8).
- Product metafields on wedding baskets carry unverified impact claims (custom.artisan_families, women_artisans_pct, fair_wage_premium, "GRI Standards"); some product descriptions claim water/plastic savings. Flag for owner review; not changed here.

## Undo
For each collection in `backups/collections/landing_before_2026-10-22.json`:
```graphql
mutation($input: CollectionInput!) { collectionUpdate(input: $input) { collection { handle } userErrors { message } } }
# variables: {"input": {"id": "<id>", "descriptionHtml": "<backup descriptionHtml>", "seo": {"title": "<backup seo.title>", "description": "<backup seo.description>"}}}
```
The wedding collection had no SEO description before; pass `"description": ""` to clear it.
