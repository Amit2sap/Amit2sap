# Master agent (performance review of the agent team)

**Growth KPIs from 4 Nov (owner, 31 Oct):** every Monday report the metrics and targets in `agents/growth_playbook.md` section 7, name the best and worst post, and recommend whether to boost the best reel (owner decides; never spend).

Owner request 29 Oct 2026: check how every agent performs (efficiency, scope for improvement, suggestions to raise productivity) and how the agents are moving GrassCrafts on Google Business, website, Instagram, LinkedIn, Pinterest, AEO, SEO and sales. Report with a dashboard every **Monday and Thursday at 9 AM IST**.

- Dashboard (Dashboard artifact): https://claude.ai/artifact/W8mCBBXQJJ9SfDk9UMVS75
- Snapshot per run: `reports/master/<date>.json` (input) -> `python3 scripts/master_report.py <date>` -> `reports/master/data/*.json` + `reports/master/<date>.md`
- Model: one Sonnet subagent, short run. Read-only on every channel: the master agent never posts, emails customers, edits the website or changes another agent's playbook. It only proposes.

## Steps (keep the run under ~25 tool calls)
0. **Directives check:** read `reports/agents/master_directives.md`. For each directive count CONFIRMED / REFUSED / open. Open after the agent has run twice since issue: re-issue it in the next round with "(re-issued)" and lower that agent's reliability score. REFUSED: rewrite it so it fits the rule named, or drop it. Measure whether confirmed directives moved the numbers and say so in the agent's impact line.
1. Setup as in agents/README.md. Copy the previous `reports/master/<last date>.json` to `reports/master/<today>.json` and update every value.
2. **Agent logs** (read only the entries since the last report): `reports/agents/*.md`, `reports/agents/handoff.md` (count open `- [ ]`), `outreach/sent_log.json` (sent count, warm_leads, do_not_send), `outreach/won_orders.json`, `seo/ai_visibility_log.json`, `seo/data/<latest>.json`, latest `seo/CHANGELOG-*`.
3. **Live numbers** (one batched Composio call where possible):
   - Instagram: INSTAGRAM_GET_USER_INFO (`me`, followers_count, media_count); INSTAGRAM_GET_USER_INSIGHTS total_value for reach, accounts_engaged, total_interactions, profile_views, website_clicks, views over the last 28 days.
   - Facebook: FACEBOOK_GET_PAGE_DETAILS page 142803116227246 (fan_count, followers_count).
   - Pinterest: PINTEREST_GET_ACCOUNT_ANALYTICS last 28 days and the 28 days before (IMPRESSION, SAVE, OUTBOUND_CLICK, PIN_CLICK, ENGAGEMENT); profile follower_count.
   - Search Console / GA4 / Bing: use the Data & SEO agent's latest `seo/data/<date>.json` (it runs 07:37 Mon/Thu, before this report). Do not query again.
   - Shopify: `run-analytics-query` `FROM sales SHOW orders, net_sales TIMESERIES week SINCE -28d UNTIL today` and `FROM sessions SHOW sessions, conversion_rate SINCE -28d UNTIL today`. If Shopify is unavailable, use GA4 transactions and say so.
   - Pipedrive: getDeals (open/won/lost counts and values), getLeads count.
   - Google Business (fixed 29 Oct): Firecrawl `firecrawl_scrape` with `alexandria` = firecrawl-maps `businesses/search` (query "Grasscrafts.com by ABALONE Nimta Kolkata", country "in", latitude 22.67, longitude 88.41) for rating and review_count of GrassCrafts by Abalone (feature_id 0x39f89f5d6b52c28f:0x40fa1c7c512d2f50) and Makhana by GrassCrafts (query "Makhana by GrassCrafts Kolkata", feature_id 0x39f89f44621d3069:0x82bae12f479ce3fd); then `businesses/rating_trend` on the main feature_id for new reviews per month and owner reply rate (about 25 credits a run). Post views/calls/directions are NOT available (Supermetrics GMB trial expired 11 Jul 2026); use GA4 sessions with utm_source=google_business from the Data & SEO file instead.
   - Live Google rank re-check (from 5 Nov): Firecrawl `firecrawl_search` (sources ["web"], location "India", limit 20, highlights false) for the 13 queries in grasscrafts_seo_audit/live_rank_check_2026-10-30.csv (about 50 credits). Save live_rank_check_<date>.csv in the same format and report GrassCrafts' position change per query vs the 30 Oct baseline, kept separate from Search Console average position.
   - Thursday 5 Nov report (owner/ChatGPT request): compare with 30 Oct for organic rankings, Search Console clicks and impressions, enquiries (wholesale form + WhatsApp + email replies) and Shopify-verified sales; for each Website/Data & SEO change logged since 30 Oct (seo/CHANGELOG-*), say whether it produced a measurable change or is too early (most need 2–4 weeks).
   - LinkedIn (fixed 29 Oct): Composio LINKEDIN_LIST_REACTIONS (count 100) on every post URN in reports/agents/linkedin.md; sum reactions. Impressions are not available for a personal profile; use GA4 sessions with utm_source=linkedin from the Data & SEO file and replies to Amit from the Monday manual kit.
4. **Score each agent with agents/scorecard_95.md** (owner, 29 Oct: target 95 for every agent; pass/fail items, N/A items scaled out, show the failed items as the agent's "issue" and the fix as "next"). Older rule kept for reference:  output against its playbook (40, of which content agents lose up to 10 when their published pieces have no "New thing:" line or no first-hand element per marketing/information_gain_playbook.md), business impact in the numbers above (40), reliability and blockers (20). Count how many story-bank questions Sristi answered since the last report. Write 1 line each for output, impact, issue, next step. Compare with the last report: name what improved or slipped.
5. **Recommendations**: 5-7 ranked actions, each with owner and effort. Prefer actions that cut usage or move sales. Never recommend anything that breaks the hard rules in CLAUDE.md.
6. Run `python3 scripts/master_report.py <today>`.
6b. **Issue directives:** append "## Round N — issued <date>" to `reports/agents/master_directives.md` with one `- [ ] Dn (<agent>) ...` line per new recommendation an agent can do itself (numbering continues). Owner-only items go to the email, not here. Directives must stay inside CLAUDE.md hard rules and owner decisions. No owner approval is needed for directives (owner, 29 Oct).
7. **Dashboard refresh** (Dashboard artifact above): upload each changed `reports/master/data/{kpis,agents,actions,directives,summary}.json` with the Artifact tool (`url` = dashboard, `asset: true`, `file_path`), then with ArtifactData read `datasets/<id>` and `update` it with the new `source.url`, `source.name` and `updated: {at, by: "Master agent (Claude)"}` (pin `if_version`). Do not change `files/index.html` unless a new metric needs a new tile.
8. **Email** amit2sap@gmail.com (one email, subject "GrassCrafts master report <date>"): the takeaway, results of confirmed directives, anything only the owner can do, the dashboard link. Keep it under 15 lines. This counts as the owner summary, not outreach.
9. Append 3-5 lines to `reports/agents/master.md`; commit "master: report <date>" and push.

## Rules
- Sales = Shopify orders that are not voided, cancelled or tests (owner's own orders are tests). Never use GA4 purchases as sales (30 Oct: all 4 Oct GA4 purchases were voided). Show GA4 purchases separately, labelled.
- Read the latest ChatGPT growth feed the owner pastes (sales/chatgpt_feed_*.md); verify its numbers before using them and list any disagreement.
- Scope: GrassCrafts agents only. Do NOT include, score, mention or read anything about the Aurelia study coach or the job-application agent (owner, 29 Oct), even though agents/README.md lists them under usage.
- Facts only from tools and repo files. A number you could not read is "not available", never 0 or a guess. Name the window for every number.
- Do not count historical orders (e.g. Pipedrive deals entered on 28 Oct for Jan/Feb 2026 form orders) as new sales.
- Respect the USAGE SAVER rules in agents/README.md: if the weekly limit is in tier 2 or 3, skip step 3's live calls except Shopify and Pinterest, and say so in the report.
