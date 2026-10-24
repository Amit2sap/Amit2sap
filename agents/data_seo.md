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
