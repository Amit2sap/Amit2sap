# GrassCrafts website audit: 17 Oct 2026

**Scope.** This was a read-only audit of the live site https://grasscrafts.com. Nothing was changed in Shopify or anywhere else.

**Method.**
- **Live pages:** fetched with Python requests and a mobile Chrome User-Agent, through the Composio remote workbench.
- **Store and theme data:** read through the Shopify Admin GraphQL API (read-only queries).
- **Live theme:** "Grasscrafts Live + Google reviews (17 Oct 2026)", id 189376495789, published today.

**Baseline (from the brief).** Over the last 90 days, 5,327 sessions led to 69 add-to-carts, 50 checkouts reached and 3 orders.

**PageSpeed Insights.** Not available. The API returned "Quota exceeded … Queries per day" on the first try and again on the retry, so it was skipped as instructed. No PSI, LCP, CLS or TBT numbers appear in this report. Proxy metrics (HTML size, script counts, hero image weight) are given instead. Re-run PSI by hand at https://pagespeed.web.dev for `/` and `/products/cane-planters-1`.

---

## 1. Scorecard

Columns:
- **H1:** the number of H1 tags in the main content.
- **Product schema:** whether the page has Product JSON-LD.
- **Ext. scripts:** the number of `<script src>` tags in the HTML. App scripts loaded later at runtime are not counted.
- **HTML:** the uncompressed HTML size.

| Page | HTTP | `<title>` (live) | Meta description (live) | H1 | Main CTA | Trust signals | Product schema | Ext. scripts | HTML | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| `/` | 200 | "Grasscrafts \| Handwoven Home Decor and Gifts from India" (OK) | OK (Sitalpati/kauna/madurkathi) | 1 (logo image, alt "grasscrafts.com"; no keyword H1) | **None in hero.** The image banner and rich text have no button. The first CTA is the per-product "Shop Now" in New Arrivals. | No reviews, no Google 4.7★, no WhatsApp on the homepage | n/a (Organization + WebSite only) | 26 | 466 KB | Weak |
| `/collections/all` | 200 | **"Bags, storage solutions, and bed runners"** (wrong) | **Generic AVADA text** (wrong) | 1 ("Collection: Products") | Product grid | None | none | 28 | **892 KB** | Poor |
| `/collections/cane-planter` | 200 | **"Bags, storage solutions, and bed runners"** (admin SEO title "Cane Planters Online India…" is ignored) | **Generic AVADA text** | 1 | Grid + filters | FAQ text and "Free shipping … above ₹1,300" | none (the FAQ in the copy has no FAQPage schema) | 28 | 438 KB | Poor (SEO) |
| `/products/cane-planters-1` | 200 | **"Bags, storage solutions, and bed runners"** (admin "Tall Cane Floor Planter \| 38 inch \| GrassCrafts" is ignored) | **Generic AVADA text** | 1 | "Add to cart" (clear) | 4.7★ / 21 Google reviews block (18 cards); Judge.me widget with 0 reviews | **2 Product blocks**: theme (price, INR, InStock) + AVADA (price, **no availability**) | 33 | 387 KB | Medium |
| `/products/wedding-gift-hamper-basket` | 200 | **"Bags, storage solutions, and bed runners"** | **Generic AVADA text** | 1 | "Add to cart"; **no bulk/quote CTA** | Same Google block | 2 Product blocks | 33 | 394 KB | Medium; weak for B2B |
| `/cart` (empty) | 200 | "Your Shopping Cart" | none (fine) | 2 ("Your cart", "Your cart is empty") | Continue shopping | Only the ₹1250 announcement bar | n/a | 27 | 325 KB | n/a (checkout itself not testable) |
| `/pages/wholesale-corporate-gifting` | 200 | "Bulk Handwoven Hamper Baskets & Corporate Gifts \| GrassCrafts" (OK) | OK | 1 | "Get a quote": email/WhatsApp link at the **bottom only**. No form on the page; the contact form is a link. | Named clients (HCL Foundation My E-haat, VBev, …), GST invoice, pan-India | FAQPage (4 Q&A) | 26 | 327 KB | Good copy, weak conversion |
| `/pages/review-us` | 200 | "Review GrassCrafts" (OK) | Auto-generated from body text (cut mid-word) | 1 | Google review link (placeid), FB link | WhatsApp + email shown | n/a | 26 | 323 KB | OK |
| `/blogs/news` | **404** | n/a | n/a | n/a | n/a | n/a | n/a | n/a | n/a | The real blog is `/blogs/news-the-grass-guide`; `/blogs/news` is not linked anywhere seen |
| `/blogs/news-the-grass-guide` | 200 | "The Grass Guide \| Natural Fiber Craft Stories…" (OK) | OK | 1 | Article cards (each card printed **twice**) | none | n/a | 25 | 295 KB | OK |
| **Any article URL** (checked 4) | 200 | **"Blogs"** | **"Please check our Blogs for more information on Bags, storage solutions, and bed runners"** | 1 ("The Grass Guide") | n/a | n/a | **No BlogPosting** | 25 | ~295 KB | **Broken: article body not shown** |
| Policies (refund, shipping, privacy, terms, contact) | 200 all | OK | none | 1 | n/a | n/a | n/a | 25 | ~280 KB | All present; content gaps (see 4.5) |

**Overall rating (judgement):**
- **SEO:** poor. The live titles and meta descriptions are wrong on every product, collection and article, and all article bodies are hidden.
- **Conversion UX:** medium-weak. Shipping messages contradict each other, product pages say nothing about delivery or returns, there is no WhatsApp on product pages and no hero CTA.
- **Content and catalogue:** medium. Admin SEO fields and alt text are well filled, but 42% of active products have a single image and 12 products are active "-copy" listings.

---

## 2. Top 10 recommendations, in priority order

Effort: S = under 1 hour, M = half a day, L = 1 day or more.

| # | Recommendation | Impact | Effort | Type | Evidence |
|---|---|---|---|---|---|
| 1 | **Restore `templates/article.json` in the live theme.** Copy the 451-byte file from the theme "Grasscrafts Live — March 2026" (id 152536449197), which was live until today. Add it to the draft "Grasscrafts – Bulk enquiry + Cart bar" (id 189377052845) before that draft is published. | **SEO critical.** All 31 published articles, including today's wedding-hamper and madur-mat guides, show the blog listing instead of the article. Google and AI crawlers cannot see the content. | S | Theme file (owner approval) | §4.1 |
| 2 | **Stop AVADA SEO from overwriting titles and descriptions.** In the AVADA SEO Suite app, turn off the "meta tag templates" for products, collections and articles (or fix the template), so the SEO title and description from Shopify admin show again. | **SEO critical.** Every product and collection page has the same `<title>` "Bags, storage solutions, and bed runners", and every article is titled "Blogs". Search results show near-duplicate titles and the curated SEO titles never reach Google. | S | Owner action in the app (or theme snippet edit) | §4.2 |
| 3 | **Use one free-shipping threshold everywhere and state it before checkout.** Announcement bar, collection copy, shipping policy and the cart (a progress bar) should all show the real rule (₹1,300 per the brief; ₹120 below). | **Conversion high.** Shipping cost shown for the first time at checkout is a common reason people abandon (94% here). The site currently gives three different numbers. | S | Content + settings | §4.3 |
| 4 | **Add a delivery, returns and payment trust block under "Add to cart"** on every product page, for example: "Ships in X days, delivered in Y days · Free shipping above ₹1,300 · Easy returns on damage within N days · Secure UPI/cards via Razorpay". Rewrite the shipping policy, which is one line today, with real dispatch and delivery times. | **Conversion high.** The page only says "Shipping calculated at checkout." The refund and FAQ rules conflict (3 days + unboxing video vs 48 hours for damage). | M | Theme block (text) + content | §4.3, §4.5 |
| 5 | **Diagnose the checkout drop with owner-side data.** Watch the Clarity recordings for `/checkouts/*`, check whether COD is offered (no COD wording anywhere on the site), whether Razorpay UPI or intent is enabled, the shipping rates shown, and whether login or extra fields are required. | **Conversion high:** 50 checkouts became 3 orders. | M | Owner action (Shopify + Razorpay + Clarity admin) | §4.6 |
| 6 | **Put WhatsApp / "Bulk quote" on product pages and on mobile.** Add a sticky WhatsApp button (wa.me/916290744782) and a "Need 25+ pieces? Get a bulk quote" line on hamper, tray and box products. The draft theme "Bulk enquiry + Cart bar" seems built for this; publish it only after fix #1 is applied to it. | **B2B conversion high.** WhatsApp appears only on `/pages/wholesale-corporate-gifting` and `/pages/review-us`. Wedding hamper pages have no bulk path. | S–M | Theme change | §4.4 |
| 7 | **Add more photos to single-image products, starting with the wedding-season items.** 88 of 208 active products (42%) have only 1 image. These include `wedding-gift-hamper-basket`, `-2`, `-copy`, `wedding-gift-hamper-bag`, 3 Mehendi, 4 Haldi (copies included) and 2 baby-shower hampers, the cane planters (`cane-planters`, `-1`, `-2`, `-4`), all 7 Madurkathi table-mat variants and 4 bamboo pendant lamps. Add a scale shot (in hand or with a product), a filled-hamper shot and a close-up of the weave. | **Conversion medium-high.** These are the season's hero products. | M–L | Content (owner photos) | §4.7 |
| 8 | **Clean the catalogue and schema.** (a) Merge or redirect the 12 active "-copy" products (`wedding-gift-hamper-basket-copy`, `haldi-ceremony-gift-hamper-basket-copy`/`-copy-1`, `cane-planters-copy`, `basket-copy`/`-copy-1`, `basket-planter-copy`, `basket-with-handle-copy`, `flower-vase-copy`/`-copy-1`, `table-runner-with-mats-copy`, `the-bespoke-sabai-trays-…-copy`). (b) Turn off AVADA's Product JSON-LD, which duplicates the theme's and lacks `availability`. (c) Set the brand name to "GrassCrafts" instead of "grasscrafts.com". | **SEO medium:** duplicate content, rich-result clarity. | M | App setting + content | §4.8 |
| 9 | **Refresh navigation and homepage for the current season.** Remove or move past-season menu items: "Rakhi Gift Edit" (Aug), "She Creates: Artisan Tribute" (Women's Day, Mar), "Maternal Heritage" (Mother's Day collection). Fix the typo "Earth Edit - Dinning". Add a hero CTA such as "Wedding & Corporate Gift Hampers → / Bulk quote" and the Google 4.7★ (21 reviews) badge on the homepage. Keep "Diwali Gift Hampers" until 8 Nov. | **Conversion medium.** The hero has no button and the homepage has no reviews or proof. | S | Content (menu + theme editor) | §4.9 |
| 10 | **Cut app weight.** Remove Instafeed (its script loads on every page but the homepage has no Instagram feed section). Check whether UpPromote (affiliate + message bar) + Secomapp referral, Swym Wishlist Plus and the Notify-me/BestPush restock app are used, and remove the unused ones. Then re-run PageSpeed mobile. | **Mobile speed/SEO medium.** 8 app embeds and 25–33 external scripts per page; `/collections/all` HTML is 892 KB. | S–M | Owner action (uninstall apps) | §4.10 |

---

## 3. Quick wins vs bigger projects

### Quick wins (under 1 hour each, can be done this week)

| What | Who | Impact |
|---|---|---|
| Restore `templates/article.json` (#1) | Owner approves; copy the file from theme 152536449197 | SEO critical |
| Turn off the AVADA meta-title/description templates (#2) | Owner, in the AVADA app | SEO critical |
| One free-shipping number everywhere (#3): announcement bar "₹1250" → ₹1,300; shipping policy "Rs 1500" → ₹1,300 + delivery times | Content | Conversion |
| WhatsApp button on product pages (#6) | Theme block / app embed | Conversion, B2B |
| Menu cleanup (Rakhi, She Creates, Maternal Heritage; "Dinning" typo) and a hero CTA (#9) | Content | Conversion |
| Uninstall Instafeed (#10) | Owner | Speed |
| Public contact email: the contact-information policy shows `amit2sap@gmail.com`, while review-us shows `sristi@grasscrafts.com`. Use one business address. | Owner (Settings → Store details) | Trust |
| Make the refund policy and FAQ match (3 days + unboxing video vs 48 hours for damage claims) | Content | Trust |

### Bigger projects (half a day or more)

| What | Why |
|---|---|
| Checkout investigation (#5): Clarity recordings, COD decision, Razorpay UPI setup, shipping-rate display | 94% checkout abandonment is the biggest revenue leak |
| Photo programme (#7): 88 single-image products, wedding hampers first | Product-page confidence for gifts sold on looks |
| Delivery/returns/payment trust block in the product template (#4) | Answers the "when will it arrive / can I return it" questions before checkout |
| Catalogue de-duplication + redirects (#8) | Removes thin/duplicate listings |
| B2B quote form on the wholesale page and on hamper products (quantity, budget, date, city), with a gallery of past bulk orders | The wholesale page has strong copy but only an email/WhatsApp line at the bottom and no images |
| App audit + PageSpeed baseline once the API quota resets (#10) | No measured Core Web Vitals in this audit |

---

## 4. Evidence

### 4.1 Article pages render the blog listing (live theme lacks `templates/article.json`)

**What the live article pages show.** Checked `/blogs/news-the-grass-guide/wedding-return-gift-hamper-baskets-india`, `/…/makhana-the-ancient-superfood-that-grows-where-the-lotus-blooms-1`, `/…/ganesh-chaturthi` and `/…/sabai-grass-the-sustainable-wonder-of-indian-craftsmanship`. Each one:
- returns HTTP 200;
- has the title "Blogs";
- has the H1 "The Grass Guide";
- has the same 5,437 characters of visible text, which is the article card list;
- has only one section (`main`), with no `<article>` element and no BlogPosting JSON-LD.

**Theme files (Shopify Admin API).**
- Live theme 189376495789: `templates/article.json` and `templates/article.liquid` return **NOT_FOUND**. `sections/main-article.liquid` exists (3,616 bytes).
- Previous live theme "Grasscrafts Live — March 2026" (152536449197) has `templates/article.json` (451 bytes).
- Comparing the two themes' template lists, `article.json` is the only file missing.
- The draft "Grasscrafts – Bulk enquiry + Cart bar (DRAFT 17…)" (189377052845) is also missing it.

**Articles affected.** 31 articles are published. 21 use `templateSuffix: "article"`, 8 use `""` and 2 use `null`; all are affected.

**Root cause.** `seo/CHANGELOG-2026-10-17-reviews.md` says the live theme was duplicated from the old live theme via the API on 17 Oct and published by the owner the same day. The duplicate did not carry `article.json` over.

### 4.2 AVADA SEO overwrites titles and meta descriptions

**Where it comes from.** `layout/theme.liquid` line 5 has `{% include 'avada-seo' %}`, which runs *before* the `<title>{{ page_title }}</title>` tag. The included `snippets/avada-seo-meta.liquid` contains:
```liquid
{%- if request.page_type == 'product' -%}{%- unless avada_seo_ovr_product_ids contains product.id -%}
{%- capture avada_seo_meta_title -%}Bags, storage solutions, and bed runners{%- endcapture -%}
... (same for 'collection'; for 'article' the title is "Blogs")
{%- assign page_title = seo_title -%}
{%- assign page_description = avada_seo_meta_description | strip_html | strip -%}
```

**Seen live.** `/products/cane-planters-1`, `/products/wedding-gift-hamper-basket`, `/products/kauna-grass-gift-hamper-basket`, `/collections/all`, `/collections/cane-planter` and `/collections/sabai-grass` all have `<title>Bags, storage solutions, and bed runners – grasscrafts.com</title>`. They also share the meta description "Shop handmade and sustainable bags, storage solutions, and bed runners at affordable prices on Grasscrafts.com…".

**What admin holds instead (ignored on the live site):**
- `cane-planters-1`: "Tall Cane Floor Planter | 38 inch | GrassCrafts"
- `wedding-gift-hamper-basket`: "Cane Wedding Gift Hamper Basket | Handmade | GrassCrafts"
- `cane-planter` collection: "Cane Planters Online India | Handwoven Floor & Table Planters"

Of the first 50 active products checked, all had their own SEO title and description in admin. Every collection checked (48) has an SEO title.

**Also affected:** the `og_title` and `og_description` used for social sharing previews.

### 4.3 Shipping messages conflict, and product pages say nothing about delivery

| Where | Text |
|---|---|
| Announcement bar (every page) | "Free Shipping on Orders Above ₹1250" |
| `/collections/cane-planter` copy | "Free shipping across India on orders above ₹1,300." |
| `/policies/shipping-policy` (the whole policy) | "Free Shipping on order above Rs 1500/-" |
| Product pages | "Shipping calculated at checkout." No dispatch time, delivery estimate or returns line near "Add to cart" (matches for "dispatch" = 0, "return" = 0 on both product pages checked) |
| Brief | ₹1,300 free, ₹120 below |

**Delivery complaint on product pages.** The Google reviews block shows a 3★ review by "sibyl bhatt" (Mar 2025) as the second card: "it's been 15 days now… check with indiapost". A delivery complaint shown near "Add to cart" without a stated delivery promise can add to doubt.

### 4.4 Contact and WhatsApp visibility

- **`wa.me/916290744782`:** found only on `/pages/wholesale-corporate-gifting`, plus as text on `/pages/review-us`. There is no WhatsApp link on the homepage, collection or product pages. The "whatsapp" matches elsewhere are only labels inside the Notify-me app's config JSON.
- **Shopify Inbox chat:** the embed (`shopify://apps/inbox/blocks/chat`) is on every page, so a chat bubble exists.
- **`/pages/contact`:** a phone number (6290744782), a "1–2 business days" response time and a form. No WhatsApp link and no email address.
- **Wholesale page:** the strongest B2B copy (who we supply, named clients, GST invoice, FAQ schema). Its only CTA is the last paragraph: "Email us … or WhatsApp us at +91 62907 44782 … contact form". There is no quote form and only the logo image (1 `<img>` in the HTML).
- **Wedding hamper product page:** "bulk" = 0, "enquir/inquir" = 0.

### 4.5 Policies

All policies are present (HTTP 200): refund, shipping, privacy, terms, contact information, plus a subscription policy link. Gaps:
- **Refund policy:** 3 days to initiate a return, "receipt … AND first opening video" required, return shipping paid by the customer, refund in 5–7 business days.
- **FAQ:** "contact us within 48 hours of delivery with photos". This conflicts with the refund policy.
- **Shipping policy:** one line, with no delivery times, courier or areas served. The FAQ mentions "India Post and major courier partners".
- **Contact information:** email `amit2sap@gmail.com` (a personal Gmail), phone, Nimta (Kolkata) address.

### 4.6 Checkout and payments (not directly testable)

- The checkout cannot be fetched without a cart session. robots.txt disallows `/checkout`, which is normal.
- No COD or "cash on delivery" wording on any audited page. No Razorpay wording or "secure payment" line on product or cart pages.
- The footer "Payment methods" area rendered no recognisable payment-icon titles in the HTML.
- **Clarity is installed** (`microsoft-clarity/clarity_js` app block), so checkout-step recordings are available to the owner.

### 4.7 Product data (Shopify Admin API)

- **Products:** 245 in total: 208 active, 18 draft, 19 archived. 48 collections.
- **Single-image products:** 88 of 208 active (counted from `mediaCount` across all active products).
- **Wedding/occasion hampers with 1 image:** `wedding-gift-hamper-basket`, `wedding-gift-hamper-basket-2`, `wedding-gift-hamper-basket-copy`, `wedding-gift-hamper-bag`, `haldi-ceremony-gift-hamper-basket-copy`, `-copy-1`, `-3`, `mehendi-gift-hamper-basket`, `mehendi_ceremony-gift-hamper_basket`, `mehendi-ceremony-gift-hamper-basket-3`, `baby-shower-gift-hamper-2`, `-3`. Exceptions with 3 images: `haldi-ceremony-gift-hamper-basket-1`, `kash-grass-wedding-gift-hamper-basket`, `kauna-grass-gift-hamper-basket`.
- **Alt text:** every image on the first 100 active products returned had non-empty alt text, which matches `seo/CHANGELOG-2026-10-17-alt-text.md`. Live HTML had 0 `<img>` tags without alt on the audited pages.
- **H1 inside product descriptions:** at least one description contains its own `<h1>` (`/products/kauna-grass-gift-hamper-basket` has 2 H1s: the title and "Kauna Petite Heritage Round Basket — Handwoven Artisan Gift Hamper"). Other descriptions were not scanned.

### 4.8 Structured data

- **Product pages:** each has 2 Product JSON-LD blocks.
  - AVADA block: `offers.price` and `priceCurrency: INR`, but no `availability`.
  - Theme block: `price`, `INR`, `availability: InStock`, `category`.
  - Both use `"brand": {"name": "grasscrafts.com"}`.
  - Neither has `aggregateRating`. The Judge.me average is `data-average-rating="0.00"`, i.e. no on-site reviews yet.
- **Homepage:** Organization, ContactPoint, WebSite and SearchAction (from AVADA).
- **Wholesale page:** FAQPage with 4 Q&A.
- **Collection pages:** only Organization; the cane-planter FAQ copy has no FAQPage schema.
- **Articles:** no BlogPosting. `theme.liquid` has BlogPosting under `{% if template == 'article' %}`, but no article template exists (§4.1). That same block also hard-codes a **Women's Day 2026 FAQPage** that would be added to *every* article once the template is restored. Remove or scope that FAQ when fixing #1.
- **Sitemap and robots:** `sitemap.xml` is a valid index (products, pages, collections, blogs, articles, agentic discovery). robots.txt is the Shopify default plus Nutch/Ahrefs/MJ12/Pinterest rules; nothing important is blocked.

### 4.9 Legacy and seasonal content, homepage

- **Menu** (on every page): "Diwali Gift Hampers" (current), "Rakhi Gift Edit" (Rakhi was in Aug), "She Creates: Artisan Tribute" (collection `womens-day-she-creates`), "Maternal Heritage" (collection `maternal-heritage-bespoke-luxury-for-her`, SEO title "Mother's Day Gifts…"), and "Earth Edit - Dinning" (typo).
- **Blog:** includes "Mother's Day Celebration 2026", the Rakhi 2026 and Women's Day 2026 posts, and two makhana handles (`…lotus-blooms`, now titled as a Yoga Day article, and `…lotus-blooms-1`). Each card on the blog index is printed twice in the HTML.
- **Homepage sections:** image_banner → rich_text → most_loved → featured_collection → collection_list → featured_blog → material_story_grid → contact_form.
  - The hero image (`grasscrafts-hero-banner….png`) has `fetchpriority="high"` and a srcset up to 3840w. Served as WebP to modern browsers it is 59 KB at 750w; as PNG (if WebP is not accepted) it is 535 KB.
  - There are no buttons in the banner or rich-text sections.
  - The homepage has no review stars or Google rating; "review" = 0 in the visible text.

### 4.10 Third-party apps and scripts

**App embeds (BEGIN app block) on the product page:** klaviyo-email-marketing-sms (onsite embed), instafeed (head-block), uppromote-affiliate (customer-referral + message-bar), microsoft-clarity, judge-me-reviews (core), inbox (chat), avada-seo-suite.

**Theme-extension assets also loaded:**
- Swym Wishlist Plus (`swym-relay`: addtowishlistbutton.js, apps.bundle.js, swym-ext-shopify.js, variantSelector.js, wishlistcollections.js)
- Secomapp affiliate (`customer-referral.js`)
- BestPush / Notify-me restock (`restock-sdk-loader.js`, api.notify-me.app)
- Judge.me loader

`asyncLoad` also loads `cdn.nfcube.com/instafeed-….js` and UpPromote `uppromote.js` (cloudfront).

**Klaviyo Reviews:** markup strings are present on product pages, but per the 17 Oct changelog the widget does not render.

**Not found in the HTML:** POWR, Hotjar, TikTok, Pinterest tag, Elfsight. GA4 and Meta pixel were not visible in the raw HTML; they may run as Shopify Customer Events web pixels, which do not show in page source.

**Counts and sizes:**

| Page | External `<script src>` | Inline scripts |
|---|---|---|
| Homepage | 26 | 61 |
| Collections | 28 | 56 |
| Product pages | 33 | 61 |
| Policies / blog | 25 | 53 |

- Product page: 65 script/CSS files, about 272 KB compressed in total. The largest are Shopify `portable-wallets.en.js` (93 KB), `shopify-perf-kit` (27 KB), Judge.me CSS (18 KB), Swym `variantSelector.js` (15 KB) and Instafeed (14 KB). The product page HTML is 88 KB gzipped.
- `/collections/all` HTML is 892 KB uncompressed, the heaviest page audited.

**Instafeed is unused on the homepage.** Its script loads on every page, but none of the homepage sections is an Instagram feed.

### 4.11 Broken links and images

84 internal links collected from 5 pages were requested; every one returned 200, except 6 product URLs that returned **429** (rate limit from fast requests, not broken pages). The wedding-gift-hamper-basket page returned 200 when fetched normally. `/blogs/news` and `/blogs` return 404 but are not linked from the audited pages. No `<img>` without alt was found.
