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
