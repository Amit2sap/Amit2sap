# Blog featured images + alt text - 2026-10-22

Request (Amit): new blog articles had no picture; add pictures and alt text.
Scope: blog `news-the-grass-guide` (only blog; 30 articles audited). Articles published since 1 Oct 2026 (6) plus any without featured image (same 4). Only `articleUpdate` used. No prices, products, inventory or theme touched.
Backup (before state, id/handle/image/body): `backups/blog/articles_before_images_2026-10-22.json`

Images are existing GrassCrafts product images (our Shopify CDN) of ACTIVE products; Shopify copied each into the article's own `/articles/` CDN path.

| Article handle | Featured image source product | Featured alt text | Body change |
|---|---|---|---|
| eco-friendly-diwali-corporate-gifts-india | kauna-grass-gift-hamper-basket | Handwoven Kauna grass gift hamper basket filled with stationery, an eco-friendly Diwali corporate gift | 1 linked image inserted after first paragraph |
| jute-vs-water-hyacinth-vs-sabai-vs-cane-baskets | sabai-grass-lidded-basket-wooden-handle | Handwoven Sabai grass lidded baskets in three sizes, an example of natural fibre baskets | same, links to that product |
| madur-mat-buying-guide | yoga-mats (Madurkathi quilted mat) | Madurkathi grass and cotton quilted madur mat, a handwoven yoga and meditation mat | same |
| wedding-return-gift-hamper-baskets-india | square-kauna-grass-gift-hamper-basket | Square handwoven Kauna grass gift hamper basket, a reusable wedding return gift basket | same |
| haldi-mehendi-basket-decoration-ideas | featured already set (Haldi hamper basket, alt OK) - left unchanged | (unchanged) | 1 linked image inserted (wedding-gift-hamper-basket, cane trousseau): alt "Handmade cane trousseau gift hamper basket that can be decorated for Haldi and Mehendi ceremonies" |
| bulk-hamper-baskets-india-buying-guide | already had featured image + descriptive alts on all 3 body images | no change | none |

Skipped / notes
- Diwali article links `/products/basket-with-handle-copy`, which did not come back as an ACTIVE product; not changed (outside scope) - check that link.
- Body content otherwise byte-identical (only one `<p><a><img></a></p>` added).

Verification: all 6 article URLs returned 200 via Composio workbench; og:image shows the new image on each.

Undo: for each article run `articleUpdate(id, article:{body:<body from backup JSON>})`. Featured image: Shopify cannot clear via this input reliably; set `image:{url:null}`/remove in Admin > Blog posts > Featured image, or re-save the backup `image` (the four had none).
