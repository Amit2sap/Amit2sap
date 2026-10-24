# Competitor study, 22 Oct 2026

Requested by Amit. The goal is for GrassCrafts to reach about 10% share in each of its 8 segments.

- Data file: `sales/data/competitor_study_2026-10-22.json`
- New B2B buyers found: 17, added to `outreach/competitor_customers.json`

## 0. What the data can and cannot tell us

Read this section first.

| Source | Status on 22 Oct | What was used instead |
|---|---|---|
| Ahrefs (traffic, DR, keyword volumes) | **Blocked.** Every endpoint returned "Insufficient plan", including the free DR endpoint. | **Search presence proxy (estimate).** This counts how often a brand's own pages appeared in the results of 25 web searches: 22 segment keyword searches and 3 AI-style questions. The search tool is US-indexed, so this is **not** Google India rank and **not** traffic. |
| Keyword volumes | Blocked (Ahrefs) | The keywords that competitors rank for and we don't are taken from their URLs seen in those results. Volume: n/a. |
| AI-search mentions | OK | The 22 Oct run in `seo/ai_visibility_log.json` (14 questions) plus 3 new segment questions asked today. |
| Shopify detection and catalogue size | OK | `/products.json` read 250 products per page, capped at 15,000. |
| Amazon.in | OK | Total results for a search of the brand name, and how many page-1 results carry the brand. |
| Flipkart, Etsy, Myntra | Not usable | Flipkart counts echo the query, Etsy returned 403 and Myntra returned an empty page. |
| Facebook followers | OK | From the public page preview (og:description). No login was used. |
| Instagram, Pinterest, LinkedIn | Not verifiable | Instagram returned 429. Pinterest counts were ambiguous. LinkedIn needs a login. All recorded as **n/a**. |
| Meta Ad Library | **Blocked** | It returned 403 with a JS challenge. Ads activity is **n/a** for every brand and scored 0 for all, so it does not change the ranking. |
| Posting frequency | Not verifiable (Instagram blocked) | **New products added in the last 30 days**, from Shopify `created_at`, as a proxy for launch cadence. |

The Composio workbench `web_search` helper was missing, so the AI re-ask used the WebSearch tool. The sandbox then stopped responding at about 10:55 UTC. Because of that, the Ellementry, India Craft House and Kadam Haat catalogues are page-1 counts only.

**Owner fix for next time:**
- Upgrade the Ahrefs plan, or connect Semrush or Similarweb. This would give real India traffic and keyword volumes.
- Open the Meta Ad Library links in section 6 in a browser on the phone. It takes 2 minutes per brand.

## 1. Scoreboard (top 12 of 26 brands scored)

**How the score works:**
- Each component is scored 0–10.
- Weights: search 30%, AI 15%, social 20%, footprint 15%, ads 10%, overlap 10%.
- "Search" is the estimate described in section 0. Ads is n/a, so the maximum possible total is 9.

| # | Brand | Total | Search presence (hits) | AI mentions | Facebook followers | Shopify products / Amazon.in results | Segment overlap (of 8) |
|---|---|---|---|---|---|---|---|
| 1 | **Nestasia** | **7.6** | 18 | 1 | 194,625 | ≥14,750 / 1,000 | 7 |
| 2 | **Brown Living** | **6.5** | 14 | 2 | 11,862 | 4,163 / weak (3 of 16 cards) | 7.5 |
| 3 | **iTokri** | **5.4** | 7 | 1 | 227,664 | ≥15,000 / 72 | 6 |
| 4 | **Zishta** | **4.3** | 2 | 2 | 81,977 | 442 / 87 | 3 |
| 5 | **Kadam Haat** (Kolkata) | **3.9** | 1 | 2 | 10,052 | 270 / 200 | 3 |
| 6 | The India Craft House | 3.7 | 4 | 1 | 14,699 | ≥3,000 / 0 | 4 |
| 7 | Okhai | 3.7 | 0 | 0 | 132,461 | ≥9,603 / 125 | 6 |
| 8 | Jaypore | 3.2 | 0 | 0 | 456,293 | not Shopify / 4,000 | 4 |
| 9 | Ellementry | 3.2 | 0 | 0 | 53,943 | 1,187 / 333 | 4 |
| 10 | Kottanz | 3.0 | 0 | 1 | 111,604 | not Shopify / 83 | 3 |
| 11 | Sirohi | 2.8 | 0 | 0 | 5,054 | 486 / 52 | 5 |
| 12 | BoxUp | 2.5 | 0 | 0 | 4,508 | 2,005 / 13 | 3.5 |
| – | *GrassCrafts (us)* | *4.2* | *0* | *3 (of 14)* | *2,656* | *208 / 3 (seller not verified)* | *8* |

**Other brands scored** (full list in the JSON):
- FNP 2.4 (490k FB followers) and IGP 2.4 (566k). They are huge, but their pages never surfaced for our segment queries.
- The Knot Company 2.6, Tribes India 2.7, Dastkar 2.6.
- Makhana brands: Farmley 2.8, Mr Makhana 2.6, Mithila Naturals 2.5, Chau Foods 1.6.

**What the scores say about GrassCrafts:**
- We have **the widest segment overlap**: all 8 segments.
- We are **the 3rd most-cited brand in AI answers** for our own questions.
- We show **no search presence in this sample**.
- Our social reach is the smallest of the brands that matter.

**Reaching 10% share:**
- Our share of search-result appearances in this sample is 0 of about 75 brand hits. 10% means about 7–8 hits on these 25 queries.
- That is roughly where iTokri is today.

## 2. Top 2 per segment

| Segment | #1 | #2 | Evidence | Also seen |
|---|---|---|---|---|
| 1. Corporate gifting baskets | Brown Living | Nestasia | Brown Living held 4 of 10 results for "eco friendly corporate gift hampers India" and has 416 corporate-tagged products plus a bulk form. Nestasia has 1,339 corporate-tagged products and price-band collections (under ₹500, under ₹1,000). | FNP (names Reliance Jewels, Accenture and others), BoxUp (19 case studies), Bombay Sweet Shop (holds the "corporate gift baskets" result) |
| 2. Diwali and occasion hampers | Brown Living | Nestasia | Brown Living held 8 of 10 results for "eco friendly Diwali hamper basket". Nestasia has a dedicated /collections/diwali-hampers page. | iTokri (/collections/diwali-gift-hampers), Bombay Sweet Shop (3 results) |
| 3. Wedding and trousseau | Nestasia | Kottanz | Nestasia held 6 of 9 results for "wedding hamper basket India", with handwoven baskets at ₹999–1,250 and 570 trousseau-tagged products. Kottanz is cited in AI answers for "wedding return gifts". | Sirohi (moonj trousseau and a B2B page); WedMeGood vendors hold "trousseau packing" |
| 4. Jewellery and watch boxes | Universal Flockers | Geetansh Luxpac | No D2C brand ranks here. The results are all IndiaMART manufacturers. Universal Flockers lists Tanishq, Kalyan, PC Jewellers and PP Jewellers as clients. Geetansh sells watch boxes from ₹350. | Tagsen (AI-cited); **no natural-fibre box maker anywhere in these results** |
| 5. Natural-fibre home decor | Nestasia | Brown Living | Nestasia held 6 of 10 results for "sabai grass basket buy online" (₹1,150–5,350). Brown Living is AI-cited for Sabai and has 99 baskets and 43 water hyacinth products. | Dastkar is #1 for cane planters; GlobalLinker sellers hold "storage baskets" |
| 6. Table and wall decor | iTokri | Zishta | iTokri held 3 of 10 results for "water hyacinth table mats" and has 100 runners. The AI answer for "table mats, runners" named Zishta first (madur mats ₹1,030–1,350). | Okhai (61 wall plates); GlobalLinker/SigmaScott hold all 10 "wall plates" results |
| 7. Bags and handbags | The India Craft House | Brown Living | India Craft House has 2 results and the AI answer for "sabai/kauna handbags". Brown Living holds the Kauna purse results. | iTokri and Hunar Setu (sitalpati); Vibecity (Kauna ₹1,199) |
| 8. Makhana | Farmley | Chau Foods | Farmley: 562 Amazon.in results, all 60 page-1 cards are its own. Chau Foods: cited in 3 of 4 AI makhana answers. | Mithila Naturals (GI), Tata Sampann, Happilo, Mr Makhana |

## 3. Top-5 profiles

### 3.1 Nestasia (nestasia.in, Shopify, Kolkata-founded)

- **Positioning:** "India's most loved lifestyle store". Modern decor, with handwoven pieces presented as fashion-colour accents. Also runs 15 physical stores (competitor_watch, 18 Oct).
- **Hero products and price bands** (median price, with 10th–90th percentile range):

| Product type | Products | Median price | Range |
|---|---|---|---|
| Hampers | 748 | ₹1,188 | ₹225–2,685 |
| Trays | 560 | ₹1,240 | – |
| Table mats | 447 | ₹845 | – |
| Planters | 362 | ₹600 | – |
| Baskets | 280 | ₹950 | – |
| Sabai | 25 | ₹970 | ₹655–2,530 |
| Kauna | 10 | ₹1,235 | – |

  Across the whole store, the median price is ₹890.
- **Content and themes:**
  - Festival and celebrity campaigns, and corporate gifts sorted by price band (under ₹500 or under ₹1,000, plus a premium employee line).
  - WhatsApp bulk orders.
  - Product copy explicitly names uses such as "bridal hamper" and "Diwali gift".
- **Launch cadence:** 176 new products in 30 days, 329 in 60 days. Posting frequency: n/a.
- **Social:**
  - Facebook: 194,625 followers, 14,356 talking about this.
  - Instagram: estimate about 1.1M followers but 0.01% engagement (73 likes per post), from Qoruz, a third-party source, Jul 2026.
- **Keywords where its pages rank and ours didn't appear** (volume n/a):
  1. wedding hamper basket
  2. handwoven gift basket
  3. sabai grass basket(s) set
  4. sabai grass kitchen basket
  5. sabai storage basket
  6. diwali hampers
  7. corporate gifting
  8. diwali gifts for corporates
  9. wedding gifts and hampers
  10. kitchen organization baskets

  Our GSC shows 0 impressions for "diwali hamper basket" and "sabai grass basket". We do appear for "gift hamper basket for wedding" (position 6.7).
- **Ads:** n/a (Ad Library blocked).
- **Reviews (aggregate):** Trustpilot 3.5 from about 172 reviews.
  - Praised: design and finish, and safe packaging.
  - Complaints: items differ from photos, breakage, refunds given as store credit only, and slow support.
- **B2B clients shown:** none named on its corporate pages.

### 3.2 Brown Living (brownliving.in, Shopify, Mumbai)

- **Positioning:** a sustainability marketplace ("mindful living") that resells artisan brands. Kadam Haat and Okhai-style makers sell through it, and it runs B2B through the "Sustainable Edit" and a B2B Gifting Studio.
- **Hero products and price bands:**
  - 4,163 products, median price ₹849.
  - By product type:

| Product type | Products | Median price |
|---|---|---|
| Hampers | 129 | ₹1,290 |
| Baskets | 99 | ₹1,395 |
| Planters | 38 | ₹1,782 |
| Kauna | 36 | ₹1,373 |
| Water hyacinth | 43 | ₹1,538 |
| Sabai | 14 | ₹1,546 |
| Madur | 14 | ₹1,150 |
| Makhana | 7 | ₹225 |

  - Diwali hamper with an artisanal-basket option: ₹1,389.
- **Content and themes:**
  - SEO listicles in its journal, for example "7 best Diwali gift ideas for clients", which is published under 4 URLs.
  - Corporate hamper product pages with packaging details, for example "kraft paper, 100% recyclable" and "supports a Varanasi artisan".
- **Launch cadence:** 156 new products in 30 days.
- **Social:** Facebook 11,862 followers. Instagram n/a.
- **Keywords where its pages rank and ours didn't appear** (volume n/a):
  1. eco friendly corporate gift hampers
  2. corporate diwali gift hamper
  3. eco friendly diwali gifts set
  4. diwali gifts ideas for clients
  5. festive diwali gift hamper
  6. sustainable corporate gifts
  7. kauna grass purse
  8. madurkathi floor mat
  9. rattan cane planter set
  10. b2b gifting studio
- **Ads:** n/a. Current offer: 20% off its B2B catalogue on 50+ items, until 31 Oct (https://brownliving.in/pages/discounts).
- **Reviews (aggregate):** Trustpilot about 3 from 84–93 reviews.
  - Praised: product quality.
  - Complaints: deliveries over a month late, missing items, and support that is hard to reach (replies to 8% of negative reviews).
- **B2B clients shown:** it says "300+ organisations" but names none.

### 3.3 iTokri (itokri.com, Shopify, Gwalior)

- **Positioning:** "Authentic Indian fabrics and handicrafts since 2012". It is mostly textiles, with a craft-decor long tail.
- **Hero products and price bands:**
  - More than 15,000 products, median price ₹2,315.
  - Runners: 100 products, median ₹3,959.
  - Water hyacinth: 13 products, ₹2,041–3,959.
  - Wall plates: 11 products, median ₹7,521.
  - Sitalpati sling bags.
- **Content and themes:**
  - Long-tail product pages with origin, size and weight.
  - Handwritten notes and free gifts, which reviews often praise.
  - Themed collections, such as International Yoga Day.
  - Free shipping and COD above ₹500.
- **Launch cadence:** 4,178 new products in 30 days. It adds new products all the time.
- **Social:** Facebook 227,664 followers, 7,601 talking about this.
- **Keywords where its pages rank and ours didn't appear** (volume n/a):
  1. diwali gift hampers
  2. water hyacinth table mat
  3. water hyacinth placemat 20 x 13
  4. sabai grass bread basket
  5. sitalpati sling bags
  6. sitalpati basket bag
  7. madur mats for yoga
  8. handmade hampers
  9. itokri sitalpati
  10. jute table runner
- **Ads:** n/a.
- **Reviews (aggregate):** Trustpilot 4.5 from 292 reviews; reviews.io 4.7.
  - Praised: craft quality, notes and gifts, and support.
  - Complaints: missing promised free gifts, colour mismatch, and occasional very late delivery.
- **B2B clients shown:** none. It runs a reseller ("Craft Partner") programme.

### 3.4 Zishta (zishta.com, Shopify, Bengaluru)

- **Positioning:** traditional kitchen and heritage products: kansa, cast iron and madur mats. It uses Shark Tank and heritage storytelling.
- **Hero products and price bands:**
  - Madur mats: 26 products, median ₹1,150.
  - Table mats and runners: ₹1,030–1,350.
  - Trays: median ₹2,900.
  - Diwali products: 39, median ₹2,550.
  - Large madur mat: ₹1,163.50 (MRP ₹1,790).
- **Content and themes:** "traditional guides" and press-led articles.
- **Launch cadence:** 42 new products in 30 days.
- **Social:** Facebook 81,977 followers.
- **Keywords where its pages rank and ours didn't appear** (volume n/a):
  1. handmade madur mats table runners
  2. madur mats table mats
  3. natural river grass madur mats
  4. madur mat online
  5. madurkathi table runner

  Our GSC: "madur mat" at position 13.7 and "madurkathi mats" at 16.3.
- **Reviews:** n/a. Search returned other brands.
- **B2B clients shown:** none found.

### 3.5 Kadam Haat (kadamhaat.com, Shopify, Kolkata): our closest like-for-like rival

- **Positioning:** a social enterprise working since 2009 with 800+ craftspeople. Its fibres are sabai, sitalpati, moonj and bamboo. Its homepage title is "Buy Handcraft Basket & Decor's Online". It is also sold on Brown Living.
- **Hero products:** sitalpati basket bag with leather handle, sabai and moonj baskets. About 270 products. Full price bands were not readable because Shopify rate-limited the request.
- **Social:** Facebook 10,052 followers. Amazon.in shows 200 results, 46 of 48 page-1 cards its own.
- **AI:** cited for Sabai and for madur mat.
- **B2B and partners shown:** its NGO arm KADAM lists HCL Foundation, HDFC Bank and Tata Realty as partners. These are CSR partners and not confirmed product buyers.

## 4. B2B businesses publicly linked to competitors (added to outreach/competitor_customers.json)

| Business | Competitor | Source |
|---|---|---|
| Reliance Jewels, JK Lakshmi Cement, Accenture, Monster.com, Religare | FNP (supplier claim, unverified) | https://www.passionateinmarketing.com/?p=521176 |
| Tanishq, Kalyan Jewellers, PC Jewellers, PP Jewellers | Universal Flockers (jewellery packaging) | https://m.indiamart.com/universal-flockers |
| IRCTC, Urban Company, Cello, Mahindra Rise, Safari | TapWell (corporate gifts) | https://peerlist.io/company/tapwell |
| HCL Foundation, HDFC Bank, Tata Realty | KADAM / Kadam Haat (CSR partners) | https://ich.unesco.org/en/accredited-ngos/kadam-01470 |

Already in the file: Century Real Estate, Sattva and Trilight (BoxUp), Gourmet Company, and Kavyatva.

## 5. How we win, per segment

Each segment has 3 moves. The Meta audience suggestions are interest targeting for when the owner chooses to run ads. No spend is committed here.

### 1. Corporate gifting baskets
1. **SEO.** Build an "eco friendly corporate gift hampers India, handwoven" landing page.
   - Use the bulk hamper guide.
   - Add 3 price-band blocks, as Nestasia does. The bands are the owner's call.
   - Make the angle "the maker, not a reseller". Brown Living and Nestasia resell, and their reviews complain about delivery.
2. **B2B.** Target the gifting firms that already buy natural-fibre baskets: Kavyatva, Kottanz, BoxUp and The Knot Company. Pitch GrassCrafts as their basket supplier.
   - Also pitch the TapWell and FNP named clients (IRCTC, Urban Company, Accenture) with a no-food, branded-basket option. This matches the Cisco/NetApp "eco, no food" ask in the buyer intel.
3. **Meta ads (when run).**
   - Audience: job titles HR Manager, Admin Manager and Procurement, plus the interests Corporate gifting, Employee engagement and Sustainability, in Kolkata, Bengaluru, Mumbai and NCR.
   - Creative: a 15-second reel of a basket being woven, then filled, then logo-tagged, with the line "Handwoven in Bengal, not bought from a trader".

### 2. Diwali and occasion hampers
1. **Content.** Publish a "Diwali hamper basket, handwoven" collection with a visible "from ₹" price. Brown Living holds 8 of 10 results with kraft-box hampers, but none of them is a basket that stays in the home.
2. **SEO keywords:** diwali hamper basket, empty hamper basket for diwali, eco friendly diwali gifts basket, reusable hamper basket. Our GSC shows 0 impressions for these today.
3. **Product.** Offer a "basket-only" SKU so gourmet brands can fill it themselves (Theobroma already sells a ₹400 empty-basket add-on). Pitch it to SMOOR, Bikanervala and Gopaldhara from the buyer intel, for New Year and Holi.

### 3. Wedding and trousseau
1. **SEO.** Win the "wedding hamper basket" results, where Nestasia holds 6 of 9 with cotton-yarn baskets.
   - Fix the 0% CTR on our wedding hamper page (position 5.2) after the title lock lifts on 1 Nov.
   - Add "trousseau packing basket", "tatwa basket" and "shagun tray" pages.
2. **B2B.** Target Kolkata tatwa packers (Anuradha's Tatwas, Anookhi, Petal Crafts) and WedMeGood trousseau vendors. They currently use leatherette baskets at about ₹150, so our angle is natural Sabai/Kauna that the couple keeps.
3. **Meta ads.**
   - Audience: Engaged (life event, 3–6 months), plus the interests Bridal wear, WedMeGood and ShaadiSaga, in West Bengal and the metros.
   - Creative: a carousel of "Haldi, Mehendi, Tatwa" baskets, with dimensions shown.

### 4. Jewellery and watch boxes
1. **Opening.** No natural-fibre box maker appears in any result or AI answer. All of them are flocked, leatherette or MDF box makers on IndiaMART.
   - Build a "handwoven jewellery box for jewellers, bulk" page. We were already AI-cited for this query on 22 Oct.
2. **B2B.** Target the jewellers named on Universal Flockers' client list (Tanishq, Kalyan, PC Jewellers) and Kolkata diamond houses. Pitch it as a premium festive and bridal presentation box, not a replacement for their everyday boxes.
   - Also target watch retailers running Diwali gift programmes, such as Zimson with Tissot.
3. **Packaging.** Get Sristi's confirmation of an insert option (velvet or cotton lining) and a logo tag. No claim goes out until she confirms it.

### 5. Natural-fibre home decor
1. **SEO.** Fix the cannibalisation on "cane planters": point the homepage to the collection. Dastkar is #1 for this query, with a thin page.
   - Make the Sabai collection the page that ranks for "sabai grass basket". Nestasia holds it with 25 products; we have 25 Sabai products too.
2. **Marketplace.** Apply to Brown Living as a seller, as Kadam Haat already does. Brown Living is the AI-cited source for Sabai and Kauna.
   - List on Amazon.in. We show 3 results there and the seller is unverified, while Kadam Haat shows 200 and Nestasia 1,000.
3. **Meta ads.**
   - Audience: Interior design, Home decor, Sustainable living, plus followers of Nestasia, Ellementry and Brown Living (interest targeting where available).
   - Creative: a "Made in Bengal by women weavers" maker video and before/after shelf styling.

### 6. Table and wall decor
1. **Product and SEO.** Make the water hyacinth placemat (the first 500-unit corporate enquiry) the hero. Title it "water hyacinth table mats set of 4/6" with size in cm, as iTokri does ("20 × 13 in").
   - Our water hyacinth basket page sits at position 9.9 with a 0.36% CTR.
2. **Wall plates.** All 10 results for "sabai wall plates" are one GlobalLinker seller. We have only 1 wall-plate product, against Okhai's 61. Adding a wall-plate set of 3 or 7 is a low-competition win, subject to Sristi's supply.
3. **Content.** Publish a "madur vs water hyacinth vs jute table mats" comparison guide. It goes after Zishta's AI answer, and our madur mats start at ₹399 against Zishta's ₹1,030.

### 7. Bags and handbags
1. **SEO.** Build a "sabai grass tote bag" page with dimensions and strap length (India Craft House wins this result with exactly that). Add "kauna grass bag" and "sitalpati bag" variants.
   - We already rank 8.9 for "sabai grass bags" and 7.3 for "kauna grass bag".
2. **Pricing visibility.** Our totes have a median of ₹3,850. Vibecity's Kauna totes are ₹1,199 and Nestasia's are ₹1,160. Show the craft difference (lined, leather handles) in the first image. Any price change is the owner's call.
3. **Meta ads.**
   - Audience: women 24–45, with the interests Handloom, Sustainable fashion, Fabindia and Okhai.
   - Creative: a reel of "one tote, three looks", with a material close-up.

### 8. Makhana
1. **Positioning.** Lead with "plain Mithila makhana, from a Kolkata craft brand". Use it as a hamper filler, not a snack war with Farmley (562 Amazon results).
   - Pair it with a Kauna basket as a "makhana gift hamper". Chau Foods holds 3 of 4 AI answers, including "makhana gift hamper".
2. **SEO and listings.**
   - Get a GBP product listing and a page for "bulk makhana Kolkata". The current AI answers there are traders (Mahabir Stores and others).
   - An IndiaMART listing is the owner's call.
3. **B2B.** Target Kolkata sweet shops and gifting firms for Diwali and New Year hampers. Make no GI claim unless the source is certified.

## 6. Three biggest openings

1. **Jewellery and watch boxes have no natural-fibre player at all.** We are already AI-cited for "handwoven jewellery boxes bulk". Jewellers' packaging suppliers publish their client lists (Tanishq, Kalyan, PC Jewellers).
2. **Diwali, wedding and corporate "basket" results are held by resellers with weak service.** Nestasia's cotton-yarn baskets (Trustpilot 3.5) and Brown Living's kraft boxes (Trustpilot about 3, delivery complaints) hold them. A maker-direct, reusable Sabai or Kauna basket page with dimensions and a "from ₹" price can take these results.
3. **Wall plates and water hyacinth table mats have thin competition.** Wall-plate results are one GlobalLinker seller. iTokri's water hyacinth mats cost ₹2,000+, against our ₹250–480 placemats. We also already have a 500-unit corporate placemat enquiry.

**Owner to-dos from this study:**
- Fix data access: Ahrefs plan, and the Meta Ad Library check in a browser for Nestasia, Brown Living, iTokri, Zishta and Kadam Haat (links below).
- Decide on Brown Living and Amazon.in listings.
- Confirm wall-plate supply and the jewellery-box insert.

Meta Ad Library links (open in a browser):
- [Nestasia](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=nestasia)
- [Brown Living](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=brown%20living)
- [iTokri](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=itokri)
- [Zishta](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=zishta)
- [Kadam Haat](https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=IN&q=kadam%20haat)

## 7. Sources

**Shopify catalogues** (read 22 Oct; counts in the JSON):
- https://nestasia.in/products.json
- https://brownliving.in/products.json
- https://itokri.com/products.json
- https://zishta.com/products.json
- https://kadamhaat.com/products.json
- https://okhai.org/products.json
- https://sirohi.org/products.json
- https://boxupgifting.com/products.json
- https://theknotcompany.in/products.json
- https://ellementry.com/products.json
- https://theindiacrafthouse.com/products.json
- https://farmley.com/products.json
- https://mrmakhana.com/products.json
- https://grasscrafts.com/products.json

**Facebook pages** (follower counts):
- https://www.facebook.com/nestasia.in
- https://www.facebook.com/BrownLivingIndia
- https://www.facebook.com/itokri
- https://www.facebook.com/zishta
- https://www.facebook.com/kadamhaat
- https://www.facebook.com/OkhaiIndia
- https://www.facebook.com/jaypore
- https://www.facebook.com/fnpind
- https://www.facebook.com/MyIGP
- https://www.facebook.com/Kottanz
- https://www.facebook.com/ellementryhome
- https://www.facebook.com/TheIndiaCraftHouse
- https://www.facebook.com/abalonehomedecor

**Amazon.in:** https://www.amazon.in/s?k=<brand>, searched for each brand.

**Search results cited in section 2:**
- https://nestasia.in/collections/wedding-gifts
- https://nestasia.in/products/sabai-grass-baskets-set
- https://nestasia.in/collections/diwali-hampers
- https://brownliving.in/products/corporate-diwali-gift-hamper-door-hanging-set-plantable-crackers-wooden-planter
- https://brownliving.in/blogs/brown-living-journal/7-best-diwali-gifts-ideas-for-clients-in-2023
- https://brownliving.in/products/ethnic-yellow-purse-handwoven-kauna-grass
- https://itokri.com/collections/diwali-gift-hampers
- https://itokri.com/products/2022-1184-1-1-handmade-water-hyacinth-table-mat-from-assam
- https://itokri.com/collections/sitalpati-sling-bags
- https://zishta.com/en-au/products/handmade-madur-mats-table-runners-table-mats
- https://theindiacrafthouse.com/products/the-india-craft-house-sabai-grass-handmade-utility-tote-bag-mmb04b
- https://indiahandmade.com/dastkar-crafts-nature-s-cradle-eco-friendly-handcrafted-cane-planter-plant-stand-for-indoor-plants-indoor-gardening-kit-natural-flower-pot.html
- https://www.globallinker.com/products/handmade-craft-for-home-decor-sabai-grass-wall-plate-size-30cm-blue-color-6972906
- https://m.indiamart.com/geethansh-luxpac
- https://m.indiamart.com/universal-flockers
- https://bombaysweetshop.com/pages/diwali-corporate-gifting-2026
- https://www.vibecity.com/retro-tote-bag/56264751
- https://merakisan.com/top-makhana-brands-in-india/

**Reviews:**
- https://www.trustpilot.com/review/nestasia.in
- https://ie.trustpilot.com/review/brownliving.in
- https://nz.trustpilot.com/review/itokri.com

**Third-party estimate:** https://qoruz.com/nestasia.in/instagram

**Internal:**
- `seo/ai_visibility_log.json` (22 Oct run)
- `seo/data/2026-10-21.json` (GSC)
- `reports/competitor_watch.md`
- `sales/buyer_intelligence_2026-10-18.md`
