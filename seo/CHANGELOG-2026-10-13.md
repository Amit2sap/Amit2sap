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

## Duplicate products merged (14 Oct)
- **Wall plates:** 10 listings → `/products/wall-plates` (Design 1–10 × Small/Medium/Large/Set of 3, 40 variants, stock 75).
- **Dry flower wreaths:** 7 listings → `/products/dry-flower-wreath` (Style: Classic, Mini, Petite, Rustic, Harvest, Garden, Meadow; stock 14).
- **Cane planters:** 4 duplicate listings → `/products/handwoven-cane-planter-set` (Design 1–4; stock 13). Distinct cane planters left as they were.
- 18 old listings ARCHIVED (not deleted), with 301 redirects to the merged products. Prices, stock and images carried over.
- Pre-merge backup: `backups/products/merged_duplicates_2026-10-14.json`.
- Corporate gifting catalogue PDF (7 pages, 18 products, 23 clients) emailed to the store owner; outreach emails sent to prospects with public emails.

## Makhana Google Maps link (15 Oct)
- Added "Find Makhana by Grasscrafts on Google Maps" link (https://share.google/zzV2YdvRPsrO9Vw0n) at the end of the Makhana product description and the /collections/makhana description. Backup: `backups/content/makhana_before_maps_link_2026-10-15.json`.
- **Makhana health claims removed (15 Oct):** replaced "Low Glycaemic Index — suitable for diabetics", "Rich in Antioxidants — supports healthy ageing and immunity", "High in Protein & Fibre — keeps you full" and "superfood/guilt-free" wording with neutral, factual bullets (nothing added in the pack, fasting-friendly, gift-worthy, storage). SEO title/meta no longer say "high-protein, low-calorie". Original text in `backups/content/makhana_before_maps_link_2026-10-15.json`.
- **"Happy Diwali" ₹0 product archived** (gid://shopify/Product/8353899839661); it can be restored from Archived products in Shopify.
- Confirmed both blog articles (Diwali corporate gifts guide; jute vs water hyacinth vs sabai vs cane) are published.

## Google and AI search work (17 Oct)
- **New page** `/pages/wholesale-corporate-gifting` (Page 166751240365, published): a B2B landing page with clear statements AI tools can quote, the segments we supply, the client list, a gifting calendar, an FAQ, FAQPage JSON-LD, its own SEO title and description. No MOQ or lead times are stated.
- **Corporate Gifts collection:** "Contact us with your quantity…" became "See our wholesale & corporate gifting page, or contact us with your quantity…". Nothing else changed.
- **About page:** the bulk-orders answer now links to the wholesale page. Old text: "<a href="/pages/contact">Contact us</a> to discuss your requirements and receive a personalized quote."
- **Our Story page:** Organization JSON-LD corrected.
  - Old: name "Grasscrafts", logo "https://grasscrafts.com/logo.png" (missing file), sameAs instagram.com/grasscrafts and facebook.com/grasscrafts (both wrong accounts).
  - New: name "GrassCrafts", a fuller description, addressRegion West Bengal, sameAs instagram.com/grasscrafts.com_ and the Facebook profile id 100088339917762, logo removed.
  - Added a link to the wholesale page in the "Bespoke Luxury" paragraph.
- Search Console baseline and the AI-visibility check are recorded in `seo/growth_seo_aeo_plan.md`.
