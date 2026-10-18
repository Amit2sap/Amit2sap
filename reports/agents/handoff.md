# Handoff queue between agents
Format: - [ ] YYYY-MM-DD from:<agent> to:<agent|owner> | item

- [ ] 2026-10-17 from:email_actions to:owner | Sristi: trade price list, MOQ and lead times due Tue 20 Oct (brief emailed and WhatsApp sent). Then SRISTI HERSELF sends the price list (owner rule, 17 Oct: agents never send prices) to Hamperology, CherishX, GIVA (submit their form), Farmley, Bombay Sweet Shop, Senco, Jaypore and The Knot Co, per the action dates in sales/sristi_trade_pricing_brief_2026-10-17.md.
- [ ] 2026-10-17 from:email_actions to:owner | Sristi's day-by-day plan was emailed (sales/sristi_action_plan_2026-10-17.md). Agents: track her DONE replies, and include outstanding steps in the daily owner email.
- [ ] 2026-10-17 from:email_actions to:owner | Reviews: (1) mark delivered orders Fulfilled in Shopify so Judge.me sends review emails; (2) Judge.me: turn on the app embeds (Review Widget, Star Rating Badge, All Reviews) and rich snippets, and enable the Reviews tab on the Facebook Page; (3) print the QR cards (marketing/review_card); (4) Sristi sends the Live-buyer WhatsApp and B2B testimonial emails (outreach/REVIEW_KIT.md).

## 18 Oct: owner items for ranking
1. **Publish draft theme** "Grasscrafts – llms.txt fix (DRAFT 18 Oct)" (189395402925). Only change: llms.txt now carries verified facts.
2. **Google Search Console:** verify grasscrafts.com, submit the sitemap, then connect Bing Webmaster Tools.
3. **Google Business app:** add Products (top 10 + Makhana); accept or reject the Google-suggested 2nd phone 062915 14742.
4. **Google & YouTube app:** check products are approved and free listings are on.
5. **Listings with the details in seo/citation_kit.md:** Justdial, IndiaMART, TradeIndia, Bing Places, Apple Business Connect.
6. **Sristi:** marketplace applications to Brown Living, Tribes India, Ethica Online, iTokri and BongHaat.
7. **Homepage title** (Online Store → Preferences): "GrassCrafts | Handwoven Kauna, Sabai Grass & Cane Baskets, Decor & Gifts".
8. **Windsor:** disconnect 7 of 8 accounts (keep GA4) so the agents can read data again.

## 18 Oct (later)
- llms.txt fix published and verified live.
- **Finish the Composio connections:** Bing Webmaster Tools and Google Analytics. The links expire in 10 minutes; ask Claude for fresh ones.
- **Bing Webmaster:** at bing.com/webmasters → "Import from Google Search Console" (1 click; GSC is already verified).
- **Google Business products:** paste them from seo/gbp_products_to_add.md.
- **Second phone 062915 14742:** is it ours? Claude will accept or reject it once you answer.
- **Merchant Center:** open the Shopify Google & YouTube app and check product approval and free listings (owner login only).
- **Directories:** Justdial, IndiaMART, TradeIndia, Bing Places and Apple Business Connect need OTP or identity checks on the owner's phone. Use seo/citation_kit.md.

## 18 Oct: listings
- **Owner reports:** Justdial, IndiaMART, TradeIndia, Bing Places and Bing Webmaster are done. Apple Business Connect is blocked at phone verification.
- **Web search (18 Oct):**
  - The new listings are not indexed yet; that is normal, and directories take days to weeks.
  - Search answers link GrassCrafts to "near Belghoria Expressway" and "Nimta", while the Google listing says Dum Dum / Nabapally 700079. An old listing with a different address may exist, so check that every listing uses the same address.
- **Apple:**
  - Use document verification (GST certificate, Udyam certificate or a utility bill in the business name).
  - Or contact Apple support inside Business Connect, and retry the phone call after 24 hours.
- The data agent re-checks indexing weekly.

## 18 Oct: address and conversion (owner to-do)
- **Address, so the Google address is used everywhere.** This connection cannot edit store details or policies (`write_legal_policies` scope missing). Please make these changes:
  1. Settings → Store details → Address: Ananta Dutta Lane, Manikpur, Nabapally, near Nabapally Sporting Club, Dum Dum, Kolkata 700079, West Bengal. The auto-generated privacy policy picks this up.
  2. Settings → Policies → Contact information: replace it with the text in `seo/conversion_diagnosis_2026-10-18.md` (address section of the chat reply). Old text is backed up in `backups/policies/`.
  3. Justdial, IndiaMART, TradeIndia, Bing Places and Apple: use the same address string.
  4. Settings → Locations → "Shop location" (Belghoria 700081, the courier pickup point): change it only if goods are now dispatched from Dum Dum.
- **Conversion:** see `seo/conversion_diagnosis_2026-10-18.md`. The top fixes are COD, tax-inclusive prices, a free-shipping threshold of ₹1,299 or lower, and turning on the abandoned-checkout email.
- **Checked 18 Oct, after the owner's update:**
  - The contact-information page is correct.
  - The store address was saved with its two lines mixed up, so the privacy policy reads "Manikpur, Sporting Club, Dum Dum,, Nabapally, near Nabapally". Fix: line 1 "Ananta Dutta Lane, Manikpur, Nabapally"; line 2 "Near Nabapally Sporting Club, Dum Dum".
  - The privacy policy still shows amit2sap@gmail.com (the store contact email).
  - The shop location is still Belghoria 700081 (pickup).
