# Review of the ChatGPT agent's "GrassCrafts Competitor Intelligence Database" (26 Oct 2026)

Source: owner upload, GrassCrafts_Competitor_Intelligence_Database_2026-10-26.xlsx. Sheets: Competitor_Master (35 brands, 3 segments), Competitor_Posts (65 observations, 23–26 Oct), Daily_Actions (30), KPI_Tracker (43 rows), README. Scope is mostly **makhana** (retail, D2C, B2B) plus natural-fibre packaging (Sirohi, Rosa Dori). The agent works only on the **Makhana by GrassCrafts** GBP listing.

## What the competitors do (patterns, 23–26 Oct)
- **Retail/D2C makhana** (Farmley, Tata Sampann, Happilo, Open Secret, Mr. Makhana, Mithila Naturals, MithilaRam, Makhana.com): flavour-led ranges and **deep discounts** (MRP cuts of 9–50%, e.g. Open Secret 200 g ₹399 vs ₹549; MithilaRam 85 g ₹149 vs ₹299), quick-commerce listings, health/"clean" claims, and GI/origin claims.
- **B2B makhana** (MeraKisan, Farm2Factory, Grain Routes, Ghatside, VEDPHAL, NutVatika, Vitika, MAKVORA, Makhana Farm Co.): grades, MOQs (10–100 kg), private label, free samples, quote forms, and **custom Diwali hampers with order-by dates** (Elvvora "order by 3 Nov"; another page says 31 Oct).
- **Natural-fibre packaging** (Sirohi, Rosa Dori; reserve: Kenzio, My E-Haat): reusable baskets and boxes, Sital Pati food baskets, private label, custom projects. These are **our direct competitors on the basket side**.

## Where GrassCrafts should play (agreed with the agent's recommendations)
1. **Do not compete on flavours or discounts.** Own "**plain Mithila makhana + a reusable handwoven basket made by us**", with roast-at-home and kheer recipes. No health, GI or "clean" claims unless proven.
2. **Become the basket supplier to makhana and gifting brands.** Grain Routes, VEDPHAL, Ghatside, Tapua Foods, Elvvora, Kenzio, Snakiy, MAKVORA and Roast Foods all sell festive hampers. Pitch our baskets as their reusable outer packaging (basket-only, their contents).
3. **Basket-only vs filled hamper**: say clearly on the wholesale page which we offer and how to quote each.
4. **Sirohi / Rosa Dori**: differentiate on fibre range (Kauna, Sabai, Madurkathi, Sitalpati, cane, water hyacinth), custom sizes and colours, and the maker story, using real photos.

## Issues the agent found on our side (verified or checked 26 Oct)
| Issue | Status |
|---|---|
| Public makhana page shows "Sold out" (agent crawls 24/25/26 Oct) while Admin shows stock | Admin 26 Oct: ACTIVE, published in IN/US/GB, 6/6/6 sellable, one market (India). Not a product-setting problem; likely the crawler location or an app script (Releasit / Notify-me). **Owner to test on phone.** If it shows Sold out in India, disable the Releasit/Notify-me embed first. |
| Makhana product page shows the **main listing's** 21 Google reviews (4.7★) next to a link to the Makhana listing | Real: `snippets/google-reviews.liquid` renders on every product. Fix in the next theme copy: hide or relabel it for products tagged `makhana`. |
| Two near-duplicate makhana articles (…lotus-blooms and …lotus-blooms-1) with health claims ("low glycaemic", "anti-inflammatory") and a GI-tag line | Website agent: keep one, redirect the other, remove unproven health claims and the GI line (owner rule: no GI claim without proof). |
| Makhana shipping conflict across pages | Fixed 25 Oct (makhana packs free, hamper standard). |
| Draft makhana products at ₹0 | Fixed 25 Oct (live at ₹649/₹949 and ₹5,499). |

## KPIs the agent pulled (verified rows)
- Shopify 18–24 Oct: **410 sessions, 4 sessions with add-to-cart (1%), 3 checkouts, 1 order (₹1,170)**, conversion 0.24%. The weak point is **add-to-cart**, which supports the "Sold out" check above.
- Makhana GBP listing: about 24 impressions a week, 0 calls, 1 website click, 3 direction requests.

## Coordination problem
The ChatGPT agent **posts on the Makhana GBP listing every day** (23, 24, 25, 26 Oct). Our GBP agent posts there weekly, and the owner session posted on 25 Oct, so 25 Oct had two Makhana posts. **One owner per listing is needed** (owner decision).
