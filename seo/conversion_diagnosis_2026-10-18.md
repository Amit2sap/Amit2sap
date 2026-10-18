# Why there are no orders: checkout and conversion diagnosis, 18 Oct 2026

**Sources:**
- Shopify sessions analytics (last 60 days)
- abandonedCheckouts (last 16)
- delivery profiles and shop tax settings
- live product, cart and policy pages (mobile user agent)

**Last order:** #1041 on 14 Sep 2026, paid by Razorpay.

## 1. The traffic is smaller than it looks

| Segment (60 days) | Sessions | Added to cart | Reached checkout | Ordered |
|---|---|---|---|---|
| Desktop, United States | 1,284 | 0 | 0 | 0 |
| Desktop, Singapore / China / Vietnam / Japan / Brazil / Korea | about 235 | 0 | 0 | 0 |
| **Mobile, India** | **659** | **24** | **13** | **1** |
| Desktop, India | 210 | 1 | 1 | 0 |

- Over half of all sessions (about 1,500 of 2,494) are foreign desktop visits with zero cart adds. These are bots or crawlers, not shoppers.
- The real audience is about 870 India sessions in 60 days, roughly 15 a day.
- The **add-to-cart rate is normal**: 3.6% on Indian mobile, against a typical 3–5%. Products and pages are not the main problem.
- **Checkout completion is the problem**: 1 of 14 checkouts became an order (about 7%). A healthy Indian D2C store converts 40–50% of checkouts.

## 2. Where checkouts die

The last 16 abandoned checkouts split into two groups.

- **10 left before entering an address.**
  - 6 of these look automated: 4 within one minute on 16 Oct (00:03–00:04 UTC) and 2 within 30 seconds on 15 Sep.
  - The rest left at the first screen. This usually happens when there is no COD option, or when the visitor was only checking the final price.
- **6 real buyers entered an address and left at the shipping or payment step:**
  - Bangalore, ₹1,550
  - New Delhi, ₹1,799
  - Dhoraji, ₹1,750
  - Hyderabad, ₹1,350
  - Kolkata, ₹1,019
  - Dehradun, ₹1,005

## 3. Causes (most likely first)

| # | Cause | Evidence | Fix (owner decision: payments, prices and checkout are not changed without your OK) |
|---|---|---|---|
| 1 | **No Cash on Delivery** | Razorpay is the only gateway. Every past order is prepaid. The product page says "UPI, cards, netbanking". New, unknown brands in India lose most first-time buyers without COD. | Turn on COD: Settings → Payments → Manual payment methods → **Cash on Delivery (COD)**. Optionally limit it to orders under ₹3,000, or use Razorpay Magic Checkout (COD plus 1-click). |
| 2 | **Price shock at checkout** | `taxesIncluded = false`, so GST is added on top. The Dehradun fridge cover went from ₹750 to **₹1,005** (+34%: ₹120 shipping and ₹135 tax). The Flower Vase went from ₹199 to **₹319** (+60%). Pages say "Shipping calculated at checkout". | Either switch on **Settings → Taxes and duties → "Include tax in prices"** (prices stay the same and GST comes out of them, so check margins first), or raise listed prices to include GST. Show "Inclusive of all taxes" on the product page. |
| 3 | **The free-shipping line sits ₹1 above best-sellers** | Free shipping starts at ₹1,300, but the Kauna Jewellery Tray (in 3 recent checkouts) is ₹1,299 and gets ₹120 added. | Set free shipping at **₹1,299 or ₹999**, or reprice. Two delivery profiles (General and "Free Shipping Condition") both carry the ₹120/₹1,300 rule, so change both. |
| 4 | **Weak return promise** | 3-day window, unboxing video required, and the buyer pays return shipping. | 7-day "damaged or wrong item: free replacement" promise. Keep the unboxing-video rule for damage claims only. |
| 5 | **No abandoned-checkout follow-up** | Klaviyo was removed on 17 Oct, so nothing now emails people who leave checkout. | Marketing → Automations → turn on **"Abandoned checkout"** (Shopify's free template, sent after 10 hours). Also check Settings → Notifications → Abandoned checkout. |
| 6 | **Bots inflate the numbers** | 1,284 US desktop sessions with 0 cart adds. | No store change needed. Read conversion on India only. Optionally block high-volume bot regions with Cloudflare later. |

## 4. Quick wins without touching payments

These can be done in the next draft theme:
- "Inclusive of all taxes" wording (only after fix #2 is done, so it is true).
- A COD badge (only once COD is on).
- A shipping-cost line under the price: "₹120 shipping under ₹1,300 · free above".
- Make the Google 4.7★ strip visible above Add to cart on mobile.

## 5. Target after fixes
- Checkout completion: 7% → 35–45%.
- At the current India traffic that is about 5–6 orders a month, before any SEO growth.
- Re-measure 14 days after COD and tax-inclusive pricing go live.
