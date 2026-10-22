# Merchant feed changelog 2026-10-22
- Audit only: 208 active products read from Shopify; all already published to Google & YouTube, categorised, with vendor GrassCrafts. No mutations were run.
- Backup (read-only snapshot): backups/merchant/products_before_2026-10-22.json
- Undo: nothing to undo.
- Issues for owner/website agent (compare-at < price, wrong categories, missing SKUs, etc.): reports/merchant_feed_audit_2026-10-22.md

## Part 2: owner-approved fixes (Amit, 22 Oct 2026: "clear them" and "fix categories")

Before-state backup (full objects as read live just before the change): `backups/merchant/compare_at_and_categories_before_2026-10-22.json`. Price, SKU, inventory and all other fields were not touched. Verified by re-reading after the change (no errors from Shopify; spot re-read of 12 products showed compareAtPrice null on cleared variants, price unchanged, real-sale variants kept).

### A. Compare-at cleared (productVariantsBulkUpdate, compareAtPrice -> null), 61 variants on 37 products
Rule: only variants where compareAtPrice <= price at the moment of the change. Variants with compare-at above price (real sale) were left alone.

Undo: for each variant below run productVariantsBulkUpdate(productId, variants:[{id, compareAtPrice:"<old value>"}]).

| Product handle | Variant id | Price (unchanged) | Old compare-at |
|---|---|---|---|
| handmade-sitalpati-handbag-cane-handle | 43686023299245 | 4450.00 | 2400.00 |
| handmade-sitalpati-straw-bag-bengal-heritage-weave | 43686054265005 | 4050.00 | 2250.00 |
| table-mats-1 | 44378252345517 | 650.00 | 599.00 |
| box-1 | 44159833047213 | 1199.00 | 1150.00 |
| box-1 | 45741003440301 | 1399.00 | 1150.00 |
| box-1 | 44159833079981 | 1199.00 | 1150.00 |
| box-1 | 45741003473069 | 1399.00 | 1150.00 |
| box-1 | 45741000753325 | 1199.00 | 1150.00 |
| box-1 | 45741003505837 | 1399.00 | 1150.00 |
| laundry-basket-3 | 45763510173869 | 6800.00 | 6400.00 |
| laundry-basket-3 | 45763510206637 | 7800.00 | 6400.00 |
| basket-planter-1 | 44187717599405 | 499.00 | 480.00 |
| basket-planter-1 | 44187717632173 | 599.00 | 480.00 |
| basket-planter-1 | 44187717664941 | 1347.00 | 480.00 |
| planter-2 | 44187717861549 | 499.00 | 480.00 |
| planter-2 | 44187717894317 | 599.00 | 480.00 |
| planter-2 | 44187717927085 | 1347.00 | 480.00 |
| handwoven-cane-round-tray-kadai-basket-set-of-3 | 44320832520365 | 2680.00 | 1250.00 |
| planter-5 | 44352670793901 | 499.00 | 480.00 |
| planter-5 | 44352670826669 | 599.00 | 480.00 |
| planter-5 | 44352670859437 | 1347.00 | 480.00 |
| handmade-sitalpati-hand-bag | 44364703596717 | 4050.00 | 2100.00 |
| handwoven-round-table-mat-12inch-indian-artisan | 44378223607981 | 930.00 | 620.00 |
| handwoven-round-table-mat-12inch-indian-artisan | 44378223640749 | 1850.00 | 620.00 |
| handwoven-round-kashi-grass-table-mat-12inch-indian-artisan | 44378204831917 | 930.00 | 620.00 |
| handwoven-round-kashi-grass-table-mat-12inch-indian-artisan | 44378204864685 | 1850.00 | 620.00 |
| natural-jute-table-mat-handwoven-placemat-sustainable-dining | 44378192281773 | 750.00 | 450.00 |
| natural-jute-table-mat-handwoven-placemat-sustainable-dining | 44378192314541 | 1480.00 | 450.00 |
| handwoven-jute-table-mat-eco-friendly-placemat | 44378191790253 | 750.00 | 450.00 |
| handwoven-jute-table-mat-eco-friendly-placemat | 44378191823021 | 1480.00 | 450.00 |
| handwoven-jute-dining-table-mat-placemat-17x13-eco-friendly | 44378190217389 | 750.00 | 520.00 |
| handwoven-jute-dining-table-mat-placemat-17x13-eco-friendly | 44378190250157 | 1480.00 | 520.00 |
| handwoven-jute-table-mat-indian-artisan | 44378208764077 | 750.00 | 520.00 |
| handwoven-jute-table-mat-indian-artisan | 44378208796845 | 1480.00 | 520.00 |
| madurkathi-grass-table-mats-runner-terracotta-black-multi-band | 44378255622317 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-micro-diamond-lattice | 44378257850541 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-vertical-pinstripe-black-natural | 44378259030189 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-burgundy-herringbone | 44378259390637 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-checkerboard-weave-rounded | 44378260897965 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-striped-herringbone-grey-burgundy | 44378261094573 | 650.00 | 599.00 |
| madurkathi-grass-table-mats-runner-set-diamond-weave | 44378263060653 | 650.00 | 599.00 |
| table-mats-with-runner-12 | 44378266337453 | 650.00 | 599.00 |
| laundry-storage | 44566604611757 | 1699.00 | 1450.00 |
| basket-with-partition | 45219815391405 | 3450.00 | 2250.00 |
| bespoke-water-hyacinth-coffer-jali-net-pattern-storage-box | 45373319446701 | 1699.00 | 1350.00 |
| spiral-water-hyacinth-basket-with-handle | 45740874072237 | 1699.00 | 1350.00 |
| handwoven-water-hyacinth-coiled-organizer | 45740878823597 | 1499.00 | 1350.00 |
| natural-grass-fibre-handwoven-storage-box | 45741014286509 | 1850.00 | 1800.00 |
| natural-grass-fibre-handwoven-storage-box | 45741014319277 | 2250.00 | 1800.00 |
| natural-grass-fibre-handwoven-storage-box | 45741014352045 | 2550.00 | 1800.00 |
| handwoven-sitalpati-natural-fibre-artisan-bag | 45743650734253 | 4050.00 | 2100.00 |
| water-hyacinth-open-caddy-handwoven-artisan-storage | 45762332885165 | 1799.00 | 1350.00 |
| bespoke-sabai-trays-burnt-sienna | 45762353004717 | 1699.00 | 1650.00 |
| handcrafted-cane-vase | 45763511124141 | 1499.00 | 850.00 |
| handcrafted-cane-vase | 45763511156909 | 2299.00 | 850.00 |
| handcrafted-cane-vase | 45763526262957 | 3199.00 | 850.00 |
| hand-woven-water-hyacinth-heritage-basket | 45765461147821 | 1549.00 | 1350.00 |
| heirloom-hamper-handwoven-water-hyacinth-tall-basket | 45765474320557 | 4450.00 | 1350.00 |
| water-hyacinth-wall-vanity-organiser-basket | 46820189307053 | 2150.00 | 1350.00 |
| water-hyacinth-wall-vanity-organiser-basket | 46820189339821 | 2150.00 | 1350.00 |
| water-hyacinth-wall-vanity-organiser-basket | 46820189372589 | 2150.00 | 1350.00 |

Variants left untouched because compare-at is above price (real sale), e.g. table-mats-1 `Table mat - 4`/`- 6`/`Table runner - 1` (599 vs 390/570/300), laundry-basket-3 Small, basket-planter-1 Small, round table mat Single, laundry-storage Small.

### B. Categories (productUpdate, category)
Undo: productUpdate(product:{id, category:"<old id>"}).

| Product (handle) | Old category (id) | New category (id) |
|---|---|---|
| bed-runner-2 (7885185581229) | Sporting Goods > ... > Yoga & Pilates Mats (sg-2-26-3) | Home & Garden > Decor > Rugs (hg-3-57), same as sibling bed-runner, -1, -3 |
| puja-mats (8037145018541) | ... > Yoga Mat Bags & Straps > Yoga Mat Bags (sg-2-26-5-1) | Sporting Goods > Fitness & General Exercise Equipment > Yoga & Pilates > Yoga & Pilates Mats (sg-2-26-3) |
| puja-mats-1 (8037157830829) | sg-2-26-5-1 | sg-2-26-3 |
| puja-mats-2 (8049565597869) | sg-2-26-5-1 | sg-2-26-3 |
| puja-mats-3 (8049571725485) | sg-2-26-5-1 | sg-2-26-3 |
| handwoven-sabai-grass-round-jewellery-basket (8759481598125) | Health & Beauty > Jewelry Cleaning & Care > Jewelry Holders > Jewelry Boxes > Travel Jewelry Cases (hb-2-3-1-3) | Health & Beauty > Jewelry Cleaning & Care > Jewelry Holders > Jewelry Boxes (hb-2-3-1) |

Skipped on purpose: the other two jewellery products (box and display tray) already sit on the correct Shopify nodes (Jewelry Boxes hb-2-3-1, Jewelry Trays hb-2-3-3); jewellery holders only exist under Health & Beauty in the taxonomy, so the audit concern was a false alarm. Asana/meditation mats, yoga-mats and quilted/jute mats were already right. Puja mats are dual-sided asana mats, so the Yoga & Pilates Mats node (not a rug) matches the identical asana-mats products. bespoke-water-hyacinth-coffer (Decor > Trunks) kept: no clearly better node. The audit's "15" wrong categories was an over-count; 6 were clearly wrong.
