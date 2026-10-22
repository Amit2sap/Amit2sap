# Checkout fixes, 22 Oct 2026

Three fixes from the 18 Oct conversion check. Free shipping and GST are done. Cash on Delivery needs you in Shopify admin, because the API cannot change it.

## 1. Free shipping from ₹1,299: DONE

| | Before | Now |
|---|---|---|
| Free shipping (India) | cart ₹1,300 or more | cart **₹1,299** or more |
| ₹120 shipping (India) | cart up to ₹1,299.99 | cart up to ₹1,298.99 |

- Changed in both profiles that had the rule: **General profile** and **Free Shipping Condition**.
- No change to international shipping (₹1,700) or the Makhana profile (always free).
- Checked: Shopify's price calculator offers only "Free shipping ₹0" for the ₹1,299 Kauna Jewellery Display Tray, and still ₹120 for a ₹980 planter. I could not open a real checkout from here (the website is blocked from this session). Please place one test: add the tray to the cart and check that shipping shows ₹0.
- Note: the limit applies to the cart total after discounts. A ₹1,299 item with a 10% code (₹1,169) still pays ₹120.

## 2. Cash on Delivery: YOUR STEP (about 3 minutes)

The API cannot add payment methods, so I did not change anything here.

1. Shopify admin > **Settings > Payments**.
2. Under **Manual payment methods**, click **Add manual payment method** (or **Add**) > **Cash on Delivery (COD)**.
3. **Additional details** (shown at checkout), suggested text:
   > Pay in cash or UPI when your order arrives. Please keep the exact amount ready. COD is available on orders across India.
4. **Payment instructions** (shown after the order), suggested text:
   > Thank you! We will call or WhatsApp you to confirm your order before dispatch. Please pay the courier on delivery.
5. Click **Activate**.

Optional: COD only for orders under ₹3,000 (this limits the risk of returned COD parcels). Shopify cannot do this by itself. You need one of:
- a payment-rules app from the Shopify App Store (search "hide payment methods" or "COD rules"; set the rule "hide Cash on Delivery when cart total is ₹3,000 or more"), or
- **Razorpay Magic Checkout**, which has COD with its own order limits and RTO protection. You already use Razorpay, so ask them to turn it on.

Also ask your courier (Shiprocket or other) whether they collect COD in your area and what the COD fee is.

## 3. GST at checkout: DONE (owner confirmed: GrassCrafts charges no GST)

You confirmed on 22 Oct: "We don't charge GST or any tax on any product." So I switched **"Charge tax" off on every product variant**. The "include tax in prices" decision and the two options from the earlier draft of this report are no longer needed.

- **Changed:** 173 variants on 39 products (all Madurkathi mats, runners, dining sets and fridge covers, straw bed runners, dry flower wreaths, bamboo trays, lamps and gift basket, the Diwali and wreath items, the 36 wall-plate variants and the 10 Kaziranga/Shillong/Agartala cane planter variants). Only the "Charge tax" tick was changed. Prices, stock, titles and SKUs are the same.
- **Checked:** a search for taxable variants now returns **0 of 539**, and all 173 were re-read one by one (all "not taxable").
- **Checked at checkout (Shopify's price calculator, nothing saved):** Madurkathi Fridge Cover (Red, ₹750) + Cane Planter Kaziranga Small (₹1,150) to New Delhi: subtotal ₹1,900, **tax ₹0**, shipping ₹0 (free over ₹1,299), total **₹1,900**. Before this change the same fridge cover had ₹135 IGST added.
- **Shop tax settings (read by API):** "Include tax in prices" is off and **shipping is not taxed** (taxShipping = false). With every variant non-taxable, nothing is added on top, so you do not need to change "Include tax in prices".

**Your steps (optional, about 2 minutes, makes it future-proof):**
1. Shopify admin > **Settings > Taxes and duties** > **India**. If GST collection is switched on there and you are not registered to collect GST through Shopify, you can turn collection off (or remove the GSTIN). The API cannot read or change this.
2. On the same India page, look under **Tax overrides** (product/collection overrides). If any override is listed (for example a collection with 18%), delete it. The API cannot list these, so please check once.
3. **New products:** Shopify ticks "Charge tax" by default. When you or an agent add a product, untick **Charge tax on this product** in the Pricing section before saving.

Fridge Cover prices today (not changed by me): Red, Black, Green, Maroon, Grey ₹750; Beige ₹999. Please check that Beige ₹999 is intended.

Before/after backup: backups/checkout/taxable_variants_before_2026-10-22.json.

Undo steps and backups: seo/CHANGELOG-2026-10-22-checkout.md, backups/checkout/.
