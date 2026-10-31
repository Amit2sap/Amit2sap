# Why GrassCrafts and Makhana don't rank, and the plan (18 Oct 2026)

## 1. Diagnosis (checked today)

### Website (Google organic)
- **Indexed:** yes. The site already ranks for material searches; the July–Oct Search Console baseline is 33.5k impressions, 547 clicks, average position 8.2.
  - Today, for "sabai grass basket online india", grasscrafts.com is the 3rd result.
  - For "buy madurkathi mat online", the results are Zishta, Mizizi, Dharini, Amazon and Craftzone; we are not there.
- **Authority is the bottleneck.**
  - Almost no other website links to or mentions grasscrafts.com. A web search for the brand finds no third-party pages.
  - Competitors (iTokri, Zishta, Brown Living, Tribes India) have marketplace and press links.
  - Without links, Google keeps us on page 1–2 for niche material terms only.
- **Fixed today:**
  - **Duplicate brand in titles:** 73 product titles and 19 collection titles showed the brand twice ("… – Grasscrafts – GrassCrafts").
  - **Makhana collection:** it had 2 lines of text and the title "Makhana Fox Nuts … | grasscrafts.com". It now has prices, pack sizes, gifting and bulk options, an FAQ and the title "Buy Mithila Makhana Online – Plain Fox Nuts 250 g, 500 g, 1 kg".
- **Still to fix:**
  - **Homepage title:** owner, under Online Store → Preferences.
  - **Product meta descriptions:** 21 products have none.
  - **Search Console:** not connected to the agents.

### Makhana (Google and Google Maps)
- "Makhana" is dominated by big brands (Farmley, Happilo) and marketplaces. A one-product page cannot win the head term.
- For "mithila makhana buy online kolkata", Google shows Vanya International, IndiaMART wholesalers, Bigbasket and Mithila Naturals; we are not there.
- **Winnable searches:** "plain mithila makhana", "makhana gift hamper", "bulk makhana for corporate gifting", "makhana for vrat", "makhana kolkata".
- **Makhana Business Profile:**
  - The description claimed "GI-tagged" without proof that our supplier is a registered GI user. Removed today.
  - It had no services; 4 added today.
  - It has hardly any reviews.

### Google Business Profile (main listing)
- **Keyword report (Jul–Sep):** people found us for "abalone" (167), "flower vase" (44), "table runner" (21), "gift shop near me" and "vase". Google links the listing to the old Abalone vase/decor shop, not to grass baskets, Madurkathi mats or corporate gifts.
- **Services:** only one vague service ("We are manufacturing handmade Indian handicrafts…"). Replaced today with 12 specific ones: Sabai, Kauna, Madurkathi, Sitalpati, cane, Kash, water hyacinth/jute/bamboo, corporate hampers, wedding baskets, Diwali hampers, jewellery boxes, wholesale/export.
- **Photos and products:** 292 photos, but no items in the Business Profile **Products** section. Products have to be added in the Google Business app, or by linking Merchant Center.
- **Local ranking:** Maps ranking depends on distance from the searcher. Buyers outside Dum Dum and Kolkata will rarely see the listing, whatever the service-area list says. Its value is (a) Kolkata searches and (b) brand trust (reviews) when people search our name.
- **Google-side edit:** Google added a second phone number (062915 14742). It shows as a Google-suggested update; the owner should accept or reject it.

### AI search engines (ChatGPT, Gemini, Perplexity, Google AI Overviews)
- **There was no dedicated AI-search agent.** Only one line in the Website agent ran `seo/ai_visibility_check.py`. It has 2 log entries: 0/7 on 16 Oct, 1/9 on 17 Oct.
- **llms.txt** (the file AI crawlers read) contained claims we cannot prove:
  - "Fair Trade aligned", "carbon-neutral shipping", "zero-waste production";
  - "200+ women artisans" and "10 trees planted per order";
  - three broken links.
  - **Rewritten today with verified facts only,** in draft theme 189395402925. The owner publishes it.
- AI engines name the brands that **other sites** mention (marketplaces, listicles, press, Reddit/Quora answers) and pages that state facts plainly. We have the on-site facts; we lack third-party mentions.

## 2. Strategy (90 days)

### A. Authority and backlinks (biggest lever; honest links only)
| Week | Action | Who |
|---|---|---|
| 1 | Set up Google Search Console and Bing Webmaster Tools, and submit the sitemap | Owner (needs Google login), agent guides |
| 1–2 | Business listings with the same name, address, phone and website everywhere: Justdial, IndiaMART, TradeIndia, Sulekha, Bing Places, Apple Business Connect | Owner creates the accounts; the agent prepares every text (`seo/citation_kit.md`) |
| 2–4 | Marketplace brand pages that AI engines already cite: Brown Living, Tribes India (TRIFED), Amazon Karigar, Flipkart Samarth, iTokri seller, Jaypore | Sristi applies; the agent drafts applications |
| 2–8 | "Get cited" emails: 3 a week to authors of "sustainable gift brands India", "eco corporate gifts", "sabai/madur products" listicles and craft blogs, offering facts, photos and a quote from Sristi | Website agent drafts; Email agent sends from the business inbox (personal 1:1 emails, no bulk) |
| 3–12 | Press: Kolkata lifestyle (The Telegraph t2, Times of India Kolkata, Homegrown), and the "woman founder reviving Bengal grass crafts" angle | Agent drafts the pitch; Sristi approves |
| ongoing | Linkable content: materials comparison chart, "GI crafts of Bengal", corporate gifting price guide | Website agent, every alternate day |
| ongoing | Partner links: ask B2B buyers (hampers, jewellers, hotels) to credit "baskets by GrassCrafts" on their sites | Lead agents ask after an order, never as a condition |

### B. Google Business Profile
1. **Done today:** 12 specific services (main) and 4 (Makhana); unverified GI claim removed.
2. **Posts on every posting day** must name the exact product and material in the first line ("Handwoven Sabai grass laundry basket – ₹…"), link to that product, and alternate material topics. Rule added to the agent.
3. **Reviews that mention products:** ask every buyer (WhatsApp after delivery, QR card in parcel) to mention what they bought. No incentives, no gating, no scripted text.
4. **Owner:**
   - In the Google Business app, add **Products** (top 10 items plus Makhana with prices).
   - Accept or reject the Google-suggested phone number.
   - Consider renaming the main listing to "GrassCrafts" once Google's review of the pending edit finishes. The "Abalone" keyword still brings 167 searches, so keep it until reviews build.
5. **Merchant Center:** the "Google & YouTube" channel is installed and Makhana is published to it.
   - In the Google & YouTube app, check that products are approved and that **free listings** are on.
   - That puts products into the Google Shopping tab and the Business Profile.
6. **Monthly:** pull the search-keyword report. Success = "sabai", "madur", "basket", "corporate gift" and "makhana" appear in it.

### C. AI search (new agent: `agents/ai_search.md`)
- **Every 2 days:** run the 15 buyer questions (including 4 makhana ones), log who gets named, and add competitor sources to the target list.
- **Every week:** pick 2 questions where we are missing:
  - make sure a page on our site answers them plainly (FAQ + facts);
  - get 1 third-party mention for that topic.
- Keep `llms.txt`, the FAQ, the About and wholesale pages, and the Organization details consistent (name "GrassCrafts", Kolkata, founded 2015, founder Sristi Dey).
- **Never** claim certifications, artisan counts, carbon or trees unless the owner sends proof.

## 3. Targets
| Metric | Now | 30 days | 90 days |
|---|---|---|---|
| Referring domains | ~0 | 10 | 30 |
| AI buyer questions naming GrassCrafts | 1/15 | 3/15 | 7/15 |
| Business Profile keywords about our products (in top 20) | 0 | 3 | 8 |
| Organic clicks/month (GSC) | ~180 | 250 | 450 |
| Makhana collection position for "plain mithila makhana" | not ranking | top 30 | top 10 |
