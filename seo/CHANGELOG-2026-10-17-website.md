# 17 Oct 2026: draft theme "Grasscrafts – Bulk enquiry + Cart bar (DRAFT 17 Oct)" (id 189377052845)

Copied from the live theme 189376495789 ("Grasscrafts Live + Google reviews"). The owner must press Publish.

## Changes
1. **Bulk / corporate enquiry on every product page** (`snippets/gc-bulk-enquiry.liquid`, block `gc_bulk` after the buy buttons).
   - A collapsible "Buying in bulk? Get a quote" form: name, company, email, phone, quantity, needed-by date, occasion, city, notes.
   - The product name and URL are attached automatically.
   - It uses Shopify's built-in contact form, so submissions arrive at the store contact email. There is also a WhatsApp link with prefilled text.
   - It makes no price, MOQ or lead-time promises.
2. **Trust points under the buy buttons** (`snippets/gc-product-trust.liquid`): handwoven by artisans in India; free shipping in India above ₹1,300; UPI, cards and netbanking; WhatsApp us.
3. **Free-shipping progress bar** in the cart drawer and on the cart page (`snippets/gc-free-shipping-bar.liquid`; edits in `snippets/cart-drawer.liquid` and `sections/main-cart-footer.liquid`).
   - The ₹1,300 threshold is checked against the delivery profile: ₹120 below ₹1,299.99, free from ₹1,300.
   - Tested: a ₹199 item shows "Add Rs. 1,101.00 more" with the bar at 15%. A ₹3,580 item shows "You've unlocked FREE shipping".
   - The bar appears in INR carts only.
4. **"Circular Legacy" section removed** from product pages. It showed unverified numbers (2,400 L of water, 3.2 kg CO₂e, 850 g of plastic). The section file is still in the theme, and the settings are backed up in `seo/google_reviews/product.json`.

## Verification
- In the preview, the product page shows the trust points, the bulk form and 18 Google review cards, with no Liquid errors.
- Add-to-cart and the cart drawer render with the checkout button working, again with no errors.

## Undo
Publish the previous theme, "Grasscrafts Live + Google reviews (17 Oct 2026)".

## Known limits
- Makhana-only carts already ship free (separate profile), but the bar still shows the ₹1,300 message for them.
- The Shopify contact form goes to the store's contact email. Check that it is an inbox Sristi reads.

## Fix: blog articles broken on the live theme (found by the audit, 17 Oct)
- **Cause:** when the live theme was copied for the Google reviews change, `templates/article.json` was dropped. The original file had a `share` block that the theme's custom `main-article` section does not define, so Shopify skipped the invalid file during the copy. As a result, all article URLs showed the blog list (title "Blogs").
- **Fix, in draft theme 189377052845:**
  - Restored `templates/article.json` without the invalid `share` block.
  - Restored `sections/footer-group.context.in.json`, which is empty but was also dropped.
  - Rewrote `sections/main-article.liquid`:
    - removed the hard-coded Mother's Day FAQPage schema and Mother's Day description that appeared on every article (it also claimed "carbon-neutral");
    - the article schema now uses the real article excerpt and author;
    - the image is optional (this fixes the "invalid url input" Liquid error).
- **Verified in preview:** both new guides render their body with 0 Liquid errors and no Mother's Day text.
- **Live status:** the live theme cannot be edited through the API. Publishing the draft fixes the live site.

## Owner-approved batch: items 3, 7, 8 and 10, plus AVADA (17 Oct, evening)
**Live now (content changes; backups in backups/):**
- **Main menu:** removed "She Creates: Artisan Tribute", "Rakhi Gift Edit" and "Maternal Heritage" (the collections still exist). Fixed "Earth Edit - Dinning" to "Earth Edit — Dining". Backup: `backups/menus/main_menu_before_cleanup_2026-10-17.json`.
- **Brand name:** vendor changed to "GrassCrafts" on 239 products (it was "grasscrafts.com" or "Grasscrafts"). The product page now shows "GrassCrafts", and the JSON-LD brand is "GrassCrafts". Backup: `backups/products/vendor_handles_before_2026-10-17.txt`.
- **12 "-copy" product URLs:** these were real, distinct products, so none were hidden. Each got a descriptive handle, with an automatic 301 redirect from the old URL (verified).
- **/pages/wholesale-corporate-gifting:** added a 4-photo product grid, a "Get a bulk quote" jump link, a WhatsApp link and a native Shopify quote form that emails the store contact address. Backup of the changed part: `backups/pages/`.

**In draft theme 189377052845 (owner publishes):**
- Announcement bar now reads "Free shipping in India on orders of ₹1,300+" (was ₹1250) and links to the shipping policy.
- Homepage: hero buttons "Shop Bestsellers" and "Bulk & Corporate Orders", and the Google 4.7★ reviews strip below the intro.
- AVADA meta template neutralised (`snippets/avada-seo-meta.liquid`). Note: on the live site the override was **not** active (titles and descriptions were already correct), so this is preventive only. The audit's claim was wrong.

**Owner to paste:** shipping and contact policies (the API lacks the `write_legal_policies` scope). Text is in `seo/policy_text_to_paste_2026-10-17.md`.

**Not done:** the refund policy (3 days + unboxing video) still conflicts with the FAQ (48 hours). The owner must choose which one is correct.

## Returns: "3 days with unboxing video" everywhere (owner confirmed, 17 Oct)
- **/pages/faq (live):**
  - The return answer now says 3 days with an unboxing video, proof of purchase, unused and original packaging, refund in 5–7 business days, return shipping paid by the customer, plus a link to the Refund policy. It used to say "48 hours with photos".
  - The international answer now gives the real flat ₹1,700 rate; it used to say "focused on India".
  - The India answer now states the ₹1,300 free-shipping threshold.
  - The bulk answer now links to the wholesale quote form.
  - Backup: `backups/pages/faq_2026-10-17_before.html`.
- **Draft theme trust points:** added "3-day returns with unboxing video", linking to the refund policy.
- **Scanned:** all products, 31 articles and theme.liquid. There are no other return-window statements; the only "48 hours" left is weaving time on the indigo jute mat.
- **Refund policy itself (owner to edit):** it says "3 days from the date of purchase" in one place and "3 days after delivery" in another. Pick one, ideally "3 days from delivery".
- **Pre-publish check of the draft:** home, collection, product, FAQ, wholesale, blog, article, search, cart and the cart drawer with add-to-cart all return 200 with 0 Liquid errors.

## 17 Oct, live
- Owner published theme 189377052845. Verified live: home (hero buttons, Google strip, ₹1,300+), product (bulk form, 3-day returns, Google reviews, no Circular Legacy), both new articles render, FAQ, wholesale form, collection, cart, search and the cart drawer with add-to-cart. All return 200 with 0 Liquid errors.
- Refund policy updated by the owner (3 days from delivery + unboxing video). The shipping and contact policies were still the old text at the time of this check.
- Policies verified live (17 Oct): shipping (₹1,300/₹120/₹1,700), refund (3 days from delivery + unboxing video) and contact (sristi@grasscrafts.com) are correct. The privacy policy still lists amit2sap@gmail.com (optional fix).
