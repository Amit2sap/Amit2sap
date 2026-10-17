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
