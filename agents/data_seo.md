# Data & SEO agent (our own Windsor.ai + Ahrefs)

**What it replaces:**
- **Windsor:** one place to read every channel's numbers.
- **Ahrefs:** rank tracking, keywords, backlinks, site health and competitor checks.

It uses the store's own connections, so there are no account limits and no paid plan. Toolkit: `seo/data_agent.py`. Run it in the Composio workbench with `exec(requests.get(<raw GitHub URL>).text)` and then `run_all()`.

## Sources
| Feature | Source | Status |
|---|---|---|
| Rank tracker (30 target keywords), clicks, impressions, CTR | Google Search Console (`sc-domain:grasscrafts.com`) | Connected |
| Striking-distance keywords, low-CTR pages, cannibalisation | Derived from GSC | Connected |
| Sitemap and index health, URL inspection | GSC | Connected |
| Backlinks and referring pages, Bing keywords, crawl issues | Bing Webmaster Tools | Connected; site verified |
| Traffic by channel, revenue | GA4 property 358606571 | Connected |
| Sales, sessions, conversion | Shopify analytics (Shopify MCP `run-analytics-query`) | Connected |
| Google Business views, clicks, search keywords | Zapier GoogleMyBusinessCLIAPI | Connected |
| Instagram, Facebook, Pinterest | Composio | Connected |
| Brand mentions and SERP checks | `web_search` | Connected |
| AI-answer visibility | AI Search agent | Connected |
| Full backlink index and keyword volumes | DataForSEO (pay-as-you-go, about US$1–2 per run) | Optional, not connected |

## Schedule
- **Daily (08:37 IST):**
  - run `run_all()`;
  - save `seo/data/<date>.json`;
  - write `reports/agents/data_seo.md` with `to_markdown()`;
  - commit.
- **Monday:**
  - GBP keywords (monthly endpoint) for both listings;
  - Shopify 7-day sales by channel;
  - compare week on week.
- **Actions it may take directly (content only, backed up first):**
  - rewrite SEO titles and descriptions for low-CTR pages (impressions ≥200, CTR <1%);
  - add internal links from blog and collection text to the page that should rank for a cannibalised query;
  - at most 10 changes a day, each logged.
- **Hand to other agents:**
  - new article topics → Website agent;
  - outreach targets from Bing backlinks and brand mentions → AI Search and Email agents.

## Rules
- Never change prices, inventory, discounts, apps or theme files directly. Theme changes go in a draft copy that the owner publishes.
- Always back up before editing.
- Never invent numbers. If a source is not connected, say so in the report.

## Keyword data without Ahrefs Keywords Explorer (22 Oct 2026)
Our Ahrefs plan returns "Insufficient plan" for Keywords Explorer. Use these free sources instead, in this order:
1. **Bing keyword research** (Composio `BING_WEBMASTER_TOOLS_RESEARCH_KEYWORDS`, connection bing_webmaster_tools_winly-than; country "in", language "en-IN"; reports: impressions, history, related). Tested on 22 Oct and it works. Bing is a small share of Indian search, so use the numbers to compare keywords against each other, not as Google volumes.
2. **Google Search Console** (Composio): real Google impressions and clicks for queries we already rank for.
3. **Google Trends:** relative interest and seasonality. Use web search snippets for now. The SerpApi free tier (if the owner connects it) gives the API.
4. **Google Keyword Planner** (free inside a Google Ads account, no spend needed): the owner can export volume ranges when needed.
Label every figure with its source. Never present Bing impressions as Google volume.

## Marketplace and trends watch (owner, 27 Oct 2026) — every run (Mon and Thu)
Goal: understand how the top sellers win (price, pack size, sets, photos, titles, reviews, offers) and apply a better strategy for GrassCrafts. 5 categories per run, 10 a week.
- **Monday set:** hamper/gift baskets · placemats and table mats · jute/straw bags and totes · planters (cane, grass) · makhana (plain, gift packs).
- **Thursday set:** storage baskets and organisers · jewellery boxes and gift boxes · wall plates and wall decor · floor/yoga/madur/sitalpati mats · festive decor (torans, door hangings, diyas trays).
- **Pull (TinyFish via Composio, connection tinyfish_mcp; use the free search and fetch_content tools only, never the paid browser/automation tools):** for each category, the Amazon.in and Flipkart bestseller or top search results page — the top 10 listings: title, brand, price, MRP/discount, pack size or set, rating and rating count. Plus Google Trends (India, last 90 days) for 1–2 search terms per category, via the Composio workbench. If TinyFish is not connected or refuses, use the workbench web_search helper and log the gap; never invent numbers.
- **Write:** reports/competitors/marketplace_<date>.md: one short table per category; then 3–5 patterns (what the winners do: price band, sets, sizes, title keywords, photo style, offers) and where GrassCrafts sits (our matching products and prices from Shopify).
- **Apply (content only, back up first, log in seo/CHANGELOG-<date>-marketplace.md):** up to 5 changes a run to our own listings — SEO titles/descriptions using the buyer keywords the winners use, Quick answers, collection intros. Price, set, pack-size or new-product ideas go to agents/STRATEGY.md "Growth backlog" and one line in reports/agents/handoff.md for the owner: never change prices, variants or inventory yourself.
- Keep it small: about 10 fetches per run; no images; no reviews scraping beyond counts.
- Tools (27 Oct): marketplace pages via Firecrawl first (billed, max ~10 scrapes/run), TinyFish only as fallback. Ahrefs has no API access and Semrush was removed — skip both.
