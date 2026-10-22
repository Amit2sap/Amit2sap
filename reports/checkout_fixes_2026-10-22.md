# Checkout fixes, 22 Oct 2026

Three fixes from the 18 Oct conversion check. One is done. The other two need you in Shopify admin, because the API cannot change them.

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

## 3. Prices shown with tax included: YOUR DECISION, then YOUR STEP

The API cannot change this setting. Today it is **off** (GST is added on top at checkout). Shipping is not taxed.

**What I found (important):** most of your products are set to **not charge GST** in Shopify ("Charge tax" is unticked). Only about 172 of 539 variants charge GST, mainly **Madurkathi** mats, runners and fridge covers, straw bed mats, dry flower wreaths, **bamboo** trays, lamps and gift basket, plus some cane planter and wall plate variants. Shopify charges these **18% IGST** (₹135 on the ₹750 fridge cover). In the last 12 months, Shopify collected ₹0 tax on every product sold.

So for your 10 best-sellers, the switch changes **nothing**: no GST is added today, and none would be taken out.

**Top 10 best-sellers (last 12 months, by sales):**

| # | Product (active) | Price today | GST added at checkout today | Customer pays today | GST inside price if switched on (option 1) | Net to you, option 1 | Change vs today |
|---|---|---|---|---|---|---|---|
| 1 | The Willingdon Tote | ₹7,800 | ₹0 (variant not taxable) | ₹7,800 | ₹0 | ₹7,800 | none |
| 2 | Handmade Sitalpati Handbag (cane handle) | ₹4,450 | ₹0 (variant not taxable) | ₹4,450 | ₹0 | ₹4,450 | none |
| 3 | Handwoven Natural Straw Tote (Sustainable Everyday Carry) | ₹3,850 | ₹0 (variant not taxable) | ₹3,850 | ₹0 | ₹3,850 | none |
| 4 | Kauna Grass Embroidered Handbag | ₹1,799 | ₹0 (variant not taxable) | ₹1,799 | ₹0 | ₹1,799 | none |
| 5 | Water Hyacinth Rectangular Placemats, set of 4 | ₹750 | ₹0 (variant not taxable) | ₹750 | ₹0 | ₹750 | none |
| 6 | Kauna Grass Gift Hamper Basket (without handle) | ₹599 | ₹0 (variant not taxable) | ₹599 | ₹0 | ₹599 | none |
| 7 | Water Hyacinth Round Placemats, set of 4 | ₹900 | ₹0 (variant not taxable) | ₹900 | ₹0 | ₹900 | none |
| 8 | Heritage Kauna Trinket Box, small | ₹980 | ₹0 (variant not taxable) | ₹980 | ₹0 | ₹980 | none |
| 9 | Handmade Sitalpati Straw Bag | ₹4,050 | ₹0 (variant not taxable) | ₹4,050 | ₹0 | ₹4,050 | none |
| 10 | Water Hyacinth Storage Basket, small | ₹699 | ₹0 (variant not taxable) | ₹699 | ₹0 | ₹699 | none |

**Where it matters: products that charge GST today (main variant shown):**

| # | Product (active, taxable) | Price today | GST 18% added today | Customer pays today | Option 1: GST inside price | Option 1: net to you | Option 1: change | Option 2: new price | Option 2: net to you |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Madurkathi Fridge Top Cover (Red/Black/Green) | ₹750 | ₹135 | ₹885 | ₹114.41 | ₹635.59 | -₹114.41 (-15.3%) | ₹885 | ₹750 |
| 2 | Madurkathi Table Runner & 6 Mats Set, mats-6 + runner | ₹850 | ₹153 | ₹1,003 | ₹129.66 | ₹720.34 | -₹129.66 (-15.3%) | ₹1,003 | ₹850 |
| 3 | Madurkathi Dining Suite / Nilachal Suite, mats-6 + runner | ₹950 | ₹171 | ₹1,121 | ₹144.92 | ₹805.08 | -₹144.92 (-15.3%) | ₹1,121 | ₹950 |
| 4 | Madurkathi Table Mats 48 in, mats-6 + runner | ₹650 | ₹117 | ₹767 | ₹99.15 | ₹550.85 | -₹99.15 (-15.3%) | ₹767 | ₹650 |
| 5 | Natural Straw Bed / Yoga Mat | ₹1,160 | ₹208.80 | ₹1,368.80 | ₹176.95 | ₹983.05 | -₹176.95 (-15.3%) | ₹1,368.80 | ₹1,160 |
| 6 | Dry Flower Wreath, Classic | ₹1,450 | ₹261 | ₹1,711 | ₹221.19 | ₹1,228.81 | -₹221.19 (-15.3%) | ₹1,711 | ₹1,450 |
| 7 | Bamboo Serving Tray | ₹1,550 | ₹279 | ₹1,829 | ₹236.44 | ₹1,313.56 | -₹236.44 (-15.3%) | ₹1,829 | ₹1,550 |
| 8 | Bamboo Puja Tray | ₹1,350 | ₹243 | ₹1,593 | ₹205.93 | ₹1,144.07 | -₹205.93 (-15.3%) | ₹1,593 | ₹1,350 |
| 9 | Bamboo Globe / Dome Pendant Lamp | ₹2,850 | ₹513 | ₹3,363 | ₹434.75 | ₹2,415.25 | -₹434.75 (-15.3%) | ₹3,363 | ₹2,850 |
| 10 | Cane Planters, Kaziranga/Shillong Medium | ₹1,350 | ₹243 | ₹1,593 | ₹205.93 | ₹1,144.07 | -₹205.93 (-15.3%) | ₹1,593 | ₹1,350 |

**Your two options:**
1. **Switch on and keep prices.** The customer pays exactly the listed price (no surprise at checkout). On the taxable products you keep about **15.3% less** (₹750 fridge cover: you keep ₹635.59 instead of ₹750). Non-taxable products are not affected.
2. **First raise the taxable products' prices by 18%, then switch on.** The customer pays the same total as today (₹885 for the fridge cover), you keep the same ₹750, and the listed price now shows the full amount. Round the new prices (for example ₹1,368.80 to ₹1,369 or ₹1,399).

**To switch it on:** Shopify admin > **Settings > Taxes and duties** > **India** (or the main tax settings on that page) > tick **"Include tax in prices"** (on some screens: "All prices include tax") > **Save**. If you choose option 2, change the prices first; agents will not change prices without your OK.

**Before deciding, please check with your CA:**
- Which products should charge GST. Today it is mixed, even inside one product (Cane Planters: the Majuli designs charge no GST, Kaziranga, Shillong and Agartala charge 18%). If you are GST-registered, GST may be owed on all sales whether or not Shopify adds it at checkout.
- Whether 18% is the right rate. Many handloom, grass and bamboo items have a lower GST rate, depending on the HSN code.

Also check: the Madurkathi Fridge Top Cover "Maroon" variant is priced **₹7,500** (the others are ₹750). This looks like a typo. I did not change it.

Undo steps and backups: seo/CHANGELOG-2026-10-22-checkout.md, backups/checkout/.
