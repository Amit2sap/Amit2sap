# Store changes — 13 Oct 2026

## Diwali gifting
- **Collection "Diwali Gift Hampers"** (`/collections/diwali-gift-hampers`): added 22 in-stock gift products (now 34). Hamper baskets, jewellery trays and boxes, bamboo puja/serving trays, asana mats, wreaths, wall plates, a pendant lamp and a cane planter set. Rewrote the description with budget tiers, a DIWALI10 banner and a bulk/corporate gifting call-to-action. Sort set to best-selling.
- **Discount code `DIWALI10`**: 10% off orders of ₹1,999 or more, all customers, 13 Oct 2026 → 12 Nov 2026 23:59 IST.

## SEO rewrite (84 active products)
Only products that had **no SEO title** were changed. About 140 products already had optimised titles and meta descriptions, so they were left alone.

- 84 products got an SEO title (≤60 chars) and a meta description (≤155 chars).
- 64 products got a clearer, keyword-rich product title, replacing generic names like "Box", "Cane Planters" and "Dry flower Wreath".
- 37 products whose descriptions were thin or generic got a structured description: intro, "Why you'll love it" bullets, details, use cases and care.
- Sizes and materials come only from the existing descriptions. **Handles/URLs were not changed**, so links, ads and Google rankings keep working.

Content source: `seo_updates.py` → `seo_updates.json`.

## Rollback
The full pre-change export of all 245 products (title, description, SEO, tags) is in
`backups/products/all_products_2026-10-13.json`. Any product can be restored from it.

## Needs your attention
- **"Happy Diwali"** (`gid://shopify/Product/8353899839661`) is ACTIVE at **₹0** with no description or image text. Archive it, or turn it into a real product.
- Duplicate titles remain for the 10 "Handwoven Sabai Grass Wall Plate Decor" listings. Add each one's colour/pattern to its title; this needs the product photos.
- Check that `/pages/contact` exists. The Diwali collection's bulk-order link points there.
- Optionally add bulk gift products to the "Corporate Gifts | Handcrafted Gifts" collection, which is currently empty of copy.

## Follow-up changes
- **Shipping:** the General profile's India rules changed from ₹120 below ₹999 / free from ₹1,000 to ₹120 below ₹1,300 / free from ₹1,300. This matches the "Free Shipping Condition" profile and closes the ₹999.01–₹999.99 gap.
- **Diwali collection:** added a "Free shipping above ₹1,300 across India" line.
- **Corporate Gifts collection** (`/collections/corporate-gifts-handcrafted-gifts`): renamed to "Corporate Gifts | Handcrafted Eco-Friendly Gifts" and added 20 products (now 27). Wrote a description with budget tiers and a bulk/custom-order call-to-action, set an SEO title and meta description, and set sort to best-selling. The URL is unchanged.
- **Main menu:** added "Diwali Gift Hampers" as the first item under THE GIFT ATELIER. All other items are unchanged; the previous menu is backed up in `backups/menus/main-menu_2026-10-13.json`.
- Confirmed: `/pages/contact` exists.
- **Main menu reordered (14 Oct):** THE GIFT ATELIER moved to first position. Inside it: Diwali → Corporate → Wedding → She Creates → Rakhi (moved last, not removed). Other sections keep their order.
- **Collection SEO (14 Oct):** wrote SEO titles + meta descriptions for 19 collections that had none, and corrected "free shipping above ₹999" to ₹1,300 in Water Hyacinth, Jute and Madurkathi meta descriptions. Values in `seo/collection_seo_2026-10-14.json`.

## SEO fixes from Search Console data (14 Oct)
GSC (Jul–Oct 2026): ~10–18k impressions/month, avg position 7–8, CTR ~1.5%, 92% of clicks from India.
- **Redirects:** created 30 new 301 redirects for broken internal links (old collection handles, products linked by numeric ID, Rakhi blog product links, /pages/what-is-* links) and repointed 5 existing redirects that led to dead pages (mats-coasters, bed-runners, jute-mat, tissue-box, sling-bag).
- **Articles:** fixed broken collection links in the Madurkathi article (2nd highest-traffic page) and the Kauna article.
- **Sabai grass page** (`/pages/grass-weaving-sustainability`, 3.5k impressions): new SEO title + meta description.
- **Collections:** new descriptions with FAQs and internal links for Sabai grass, Kauna (now consistently Manipur), Cane, Cane planters, Baby shower, Table mats, Bamboo; new SEO title/meta for Kauna and Kash grass.
- **Sitemap:** submitted https://grasscrafts.com/sitemap.xml to the sc-domain property. Three old sitemap entries with errors remain in GSC (remove manually: /sitemap, /sitemap.xml/grasscrafts.com/sitemap.xml, www /sitemap_index.xml).
- Backup of all article/page bodies before edits: `backups/content/articles_pages_2026-10-14.json`.
- **New blog drafts (UNPUBLISHED, review before publishing)** in "The Grass Guide":
  - `eco-friendly-diwali-corporate-gifts-india`: "Eco-Friendly Diwali Corporate Gifts in India (2026 Guide)". Budget tiers, bulk-order section, FAQs, SEO title/meta.
  - `jute-vs-water-hyacinth-vs-sabai-vs-cane-baskets`: material comparison table + FAQs, SEO title/meta.
