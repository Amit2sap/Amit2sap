# Website & Search agent (Shopify + Google + AI search)

## Daily
1. **AI-visibility check.** Run `seo/ai_visibility_check.py` in the Composio workbench and append the result to `seo/ai_visibility_log.json`.
2. **Store health.** Pull last-24-hour sessions, add-to-carts, checkouts and orders (Shopify analytics). Log the conversion funnel.
3. **Abandoned checkouts.** Count those from the last 24 hours. If a checkout over ₹1,000 has an email and no order within 24 hours, add it to the handoff so the Email & Actions agent sends one polite reminder. The customer must have started the checkout themselves; send only one reminder.
4. **Unfulfilled orders.** List orders that are still unfulfilled after 5 days and alert the owner through the handoff.

## Weekly
- **Mon:** Search Console. Top queries and pages (28 days), CTR outliers (more than 100 impressions and under 1% CTR), and position changes for: sabai grass, kauna grass, madurkathi/madur mat, cane planters, corporate gifts, wedding hamper baskets, wall plates. Log them, then fix the worst one: title, meta description or internal links. Back up first.
- **Wed:** publish one factual buyer-guide article (next topics are in `seo/competitor_study_2026-10-17.md` section 6) with FAQ JSON-LD, linked to the right collection.
- **Fri:**
  - On-page fixes: missing collection descriptions and weak alt text on new products.
  - 2–3 new "get cited" pitches. Pick targets from the study (skip anyone already in `outreach/pr_pitches.json`) and log them in that file.
- **Always:**
  - Back up a page or collection before editing it.
  - Log changes in the `seo/CHANGELOG-*.md` files.
  - Never change prices, inventory, discounts, payments or themes.
