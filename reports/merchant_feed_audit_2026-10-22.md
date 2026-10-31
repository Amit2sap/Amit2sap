# Merchant feed audit, 2026-10-22

Scope: all 208 ACTIVE products read from Shopify (Admin API) right after the Google & YouTube app was installed (free listings). Merchant Center itself cannot be read by agents, so this audits the Shopify side of the feed only. Publication checked: Google & YouTube (`gid://shopify/Publication/137160884397`). Backup of what was read: `backups/merchant/products_before_2026-10-22.json`.

## Result in one line
No blocking feed issue found on the Shopify side: every active product is published to Google & YouTube, has an image of at least 437px, a description of at least 280 characters, a standard product category, a price above 0 and vendor GrassCrafts. **No safe fix was needed, so no product was changed.**

## Counts per issue (208 active products)
| Check | Count | Severity |
|---|---|---|
| No image | 0 | ok |
| Featured image under 250x250 | 0 (smallest side is 437px, the gift card) | ok |
| Description under 100 chars (text only) | 0 (shortest 280) | ok |
| Title over 150 chars | 0 (47 are over 70, longest ~130; fine) | ok |
| Title ALL CAPS or promotional text | 0 | ok |
| Price 0 | 0 | ok |
| No Shopify standard category | 0 | ok |
| Vendor not GrassCrafts / empty | 0 | ok |
| Out of stock with "continue selling" | 0 (all use DENY) | ok |
| Not published to Google & YouTube | 0 (208 of 208 published) | ok |
| Compare-at price lower than price (on at least one variant) | 37 | Warning, owner action |
| Variants missing SKU | 186 products | Low (SKU not required by Google) |
| Products fully out of stock (shown as out_of_stock, not disapproved) | 6 | Info |
| SEO description empty | 73 | Low (website agent) |
| Product type empty | 7 | Low |
| Barcode/GTIN empty | 208 | Expected for handmade, see below |
| Products with fewer than 3 images | 146 | Info (more photos help ranking) |
| Category looks wrong for the product | 15 (yoga-mat/bag categories used for bed runners, puja mats, table-runner sets; jewellery boxes under Health & Beauty) | Medium, owner/website agent |

## What was fixed
Nothing. Fix (a) publish missing products: 0 missing. Fix (b) missing category: 0 missing. Fix (c) empty vendor: 0 empty. No mutations were run, so there are no undo steps beyond the read-only backup. Changelog: `seo/CHANGELOG-2026-10-22-merchant.md`.

## Items for the owner / website agent (not changed here)
1. **Compare-at price lower than price (37 products).** On these, at least one variant has a compare-at price below its selling price (for example BAG008 price 4450 vs compare-at 2400). Shopify admin shows no strike-through, but Merchant Center may flag price/sale-price mismatch and the feed sends confusing prices. Either clear the compare-at value or raise it above the price. Handles:
- `handmade-sitalpati-handbag-cane-handle`
- `handmade-sitalpati-straw-bag-bengal-heritage-weave`
- `table-mats-1`
- `box-1`
- `laundry-basket-3`
- `basket-planter-1`
- `planter-2`
- `handwoven-cane-round-tray-kadai-basket-set-of-3`
- `planter-5`
- `handmade-sitalpati-hand-bag`
- `handwoven-round-table-mat-12inch-indian-artisan`
- `handwoven-round-kashi-grass-table-mat-12inch-indian-artisan`
- `natural-jute-table-mat-handwoven-placemat-sustainable-dining`
- `handwoven-jute-table-mat-eco-friendly-placemat`
- `handwoven-jute-dining-table-mat-placemat-17x13-eco-friendly`
- `handwoven-jute-table-mat-indian-artisan`
- `madurkathi-grass-table-mats-runner-terracotta-black-multi-band`
- `madurkathi-grass-table-mats-runner-micro-diamond-lattice`
- `madurkathi-grass-table-mats-runner-vertical-pinstripe-black-natural`
- `madurkathi-grass-table-mats-runner-burgundy-herringbone`
- `madurkathi-grass-table-mats-runner-checkerboard-weave-rounded`
- `madurkathi-grass-table-mats-runner-striped-herringbone-grey-burgundy`
- `madurkathi-grass-table-mats-runner-set-diamond-weave`
- `table-mats-with-runner-12`
- `laundry-storage`
- `basket-with-partition`
- `bespoke-water-hyacinth-coffer-jali-net-pattern-storage-box`
- `spiral-water-hyacinth-basket-with-handle`
- `handwoven-water-hyacinth-coiled-organizer`
- `natural-grass-fibre-handwoven-storage-box`
- `handwoven-sitalpati-natural-fibre-artisan-bag`
- `water-hyacinth-open-caddy-handwoven-artisan-storage`
- `bespoke-sabai-trays-burnt-sienna`
- `handcrafted-cane-vase`
- `hand-woven-water-hyacinth-heritage-basket`
- `heirloom-hamper-handwoven-water-hyacinth-tall-basket`
- `water-hyacinth-wall-vanity-organiser-basket`
2. **Wrong standard category.** Google uses the category to decide ad/listing type and can mismatch searches. Suggested review: bed runners, puja mats and table-runner sets currently in "Yoga & Pilates Mats / Yoga Mat Bags" (e.g. `bed-runner-2`, `puja-mats`, `puja-mats-1`, `puja-mats-2`, `puja-mats-3`, `asana-mats*`/`meditation-mats*` are genuinely mats and fine); the three jewellery products (`handwoven-sabai-grass-round-jewellery-basket`, `handwoven-oval-kauna-grass-jewellery-box`, `handwoven-kauna-grass-jewellery-display-tray`) are under Health & Beauty > Jewelry Cleaning & Care, better under Home & Garden > Decor or Apparel & Accessories > Jewelry > Jewelry Storage; `kash-grass-wedding-gift-hamper-basket` is under Gift Giving (acceptable). Left unchanged because the brief allows setting categories only where missing.
3. **Missing SKUs** on 186 products (mostly older Madurkathi, jute, bag, planter products). Not a Merchant Center error, but SKUs make the feed id stable and help order handling. Handles are listed in the backup (variants with `sku` null/empty).
4. **Out-of-stock products (6):** `gift-cards`, `handmade-kauna-grass-handbag-customizable-eco-friendly`, `yoga-mats`, `solstice-atelier-handwoven-cane-sunburst-tray`, `kash-grass-bird-basket-planter`, `cane-flower-vase-pen-stand`. They sync as out of stock (policy DENY), which is correct. Gift cards are normally not eligible for Google free listings and will be skipped by the app.
5. **Placeholder wording in 3 jewellery descriptions:** "Exact dimensions and additional clear product photographs will be added after verification." Replace with real dimensions and more photos; Google reviewers dislike placeholder text and single images.
6. **Weight is 0 or empty on most variants.** Shipping weight is not required for free listings, but is needed if shipping settings/ads are added later.
7. **SEO description missing on 73 products** (the 5 pendant lamps among them). Merchant Center does not use it, but it affects Google organic snippets.
8. **7 products have an empty product type** (`gift-cards`, `handwoven-round-kashi-grass-table-mat-12inch-indian-artisan`, `cane-stool`, `handwoven-ottomans-3`, `handwoven-water-hyacinth-round-dish-storage-organizer`, `handwoven-water-hyacinth-round-organizer`, `handwoven-water-hyacinth-round-catch-all-organizer`); filling it helps campaign grouping.

## GTIN / brand
All 208 products have vendor `GrassCrafts` (consistent) and no barcode. For handmade goods the Google & YouTube app sends brand=GrassCrafts and identifier_exists=no, so a missing GTIN does not disapprove products. Do not invent barcodes.

## Top owner actions
1. In Shopify admin > Google & YouTube > Overview, confirm Merchant Center is connected, the store is verified and claimed, and shipping (India) and return policy are set in Merchant Center settings. These are the most common reasons for "limited" status and cannot be seen by agents.
2. Clean up the 37 products where compare-at price is lower than price (clear it, or raise it).
3. Check Product status (see below) and send agents a screenshot of any errors; also review the wrong-category list.

## Merchant Center steps for the owner
1. Shopify admin > Sales channels > Google & YouTube > Overview. Open the "Product status" card: note counts for Approved / Pending / Disapproved / Not approved. New feeds usually stay Pending for up to 3 to 5 days.
2. Open Merchant Center (merchants.google.com) > Products > Diagnostics. Look at the "Item issues" and "Account issues" tabs. Screenshot any error or warning (including the affected product count) and send it so agents can fix them.
3. In Merchant Center > Settings: confirm business info, website URL verified and claimed, shipping and returns set to India, and that "Free listings" is turned on (Growth > Manage programs).
4. Re-check after 3 to 5 days; repeat the audit after any price or category change.

Method note: counts were computed from Shopify product data (first 20 variants per product; the three 16-variant products and the 20-variant product were fully covered). The last 8 products of the backup are stored in compact form.
