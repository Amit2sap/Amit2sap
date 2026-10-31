# Website expert upgrade, phase 1 (23 Oct 2026)
Approved by owner request of 23 Oct 2026 ("upgrade grasscrafts.com like an expert"). No prices, inventory, discounts, payments, checkout, shipping, tax or apps touched.

## 1. Products (200+8 = 208 ACTIVE audited)
- Audit: all 208 active products already have SEO title, SEO description, image alt text (first 10 images each) and Charge tax off on every variant (first 30 variants). Only 3 descriptions were thin.
- Rewritten (intro, 5 bullets, Care, Bulk & corporate): `sabai-desk-organizer` (sizes 10 in / 12 in from the variants), `eco-friendly-straw-crossbody-sling-bag-handcrafted`.
- Not changed: `gift-cards` (39 words; a gift card, no craft facts to add).
- Backup: backups/products/upgrade_2026-10-23.json. Undo: productUpdate descriptionHtml with the saved value.

## 2. Collections
- Every collection already had intro text. The gap was the SEO meta description (null) on top collections. Added a meta description (under 155 chars, existing facts only) to 10: storage-baskets, earth-edit-dining, earth-edit-living, best-sellers, everyday-essentials-under-1000, the-tote-atelier, water-hyacinth, jute, baskets-trays, bed-mats-1.
- Backup: backups/collections/upgrade_2026-10-23.json (previous seo). Undo: collectionUpdate seo.description null.

## 3. Theme copy (unpublished): "Grasscrafts – expert upgrade 23 Oct"
- Theme id gid://shopify/OnlineStoreTheme/189621403821 (copied from live 189572546733). Preview: https://grasscrafts.com/?preview_theme_id=189621403821
- Homepage (templates/index.json): new sections gc_trust_bar (Free shipping over ₹1,299 · Cash on Delivery · No GST added · Handwoven by Indian artisans), gc_occasion_row (Shop by occasion: corporate, wedding, Diwali, makhana, home decor), gc_bulk_cta (Bulk & corporate orders band linking /pages/wholesale-corporate-gifting and https://wa.me/916290744782). All existing sections kept in order.
- BreadcrumbList JSON-LD: snippet gc-breadcrumb-jsonld, added as section gc_breadcrumb_ld to templates/product.json and templates/collection.json. Not found in theme.liquid, meta-tags, avada-seo or main-product; check the live page source for a duplicate from an app before publishing.
- New snippets: gc-home-trust, gc-home-occasion, gc-home-bulk-cta, gc-breadcrumb-jsonld. Sources: seo/theme_draft_2026-10-23/. templates/article.json confirmed present in the copy.
- Undo: do not publish the copy; delete it. Live theme untouched.
- Note for owner: the existing USP strip says "Free shipping ₹1,300+" and FAQ says ₹1,300; the new bar uses ₹1,299 as told. Align when convenient.

## 4. Menu proposal (not applied)
Main menu: Shop by material (Sabai, Kauna, Madurkathi, Cane, Water hyacinth, Bamboo, Jute) | Shop by occasion (Corporate gifting, Wedding, Diwali hampers, Haldi/Mehendi, Baby shower) | Makhana (/collections/makhana) | Bulk & corporate (/pages/wholesale-corporate-gifting) | Blog (/blogs/news-the-grass-guide).

## Main menu restructure (owner approved 23 Oct, live)
New top level: Shop by Occasion | Shop by Material | Shop by Product | Makhana | Bulk & Corporate | Our Story (incl. Journal).
Added to menu: Haldi, Mehendi, Baby Shower hampers, Festive & Christmas Gifts, Table Mats, Jute Mats & Rugs. Every old link kept. Verified live: menu renders, no Liquid errors.
Undo: rebuild from backups/menus/main-menu_before_2026-10-23.md (Online Store > Navigation > Main menu).

## Published (owner, 23 Oct)
Theme 189621403821 "Grasscrafts – expert upgrade 23 Oct" is now LIVE. Verified homepage, makhana product, makhana collection and blog: HTTP 200, no Liquid errors, trust bar, occasion row, bulk band, breadcrumbs on product/collection, add-to-cart works.
Leftover: snippets/gc-product-trust.liquid still says "Free shipping in India above ₹1,300" on product pages (live theme cannot be edited via API). Owner to change to ₹1,299 in Edit code. Undo publish: publish the previous theme "Grasscrafts – llms.txt update 22 Oct" (189572546733).
