# Master agent (performance review of the agent team)

Owner request 29 Oct 2026: check how every agent performs (efficiency, scope for improvement, suggestions to raise productivity) and how the agents are moving GrassCrafts on Google Business, website, Instagram, LinkedIn, Pinterest, AEO, SEO and sales. Report with a dashboard every **Monday and Thursday at 9 AM IST**.

- Dashboard (Dashboard artifact): https://claude.ai/artifact/W8mCBBXQJJ9SfDk9UMVS75
- Snapshot per run: `reports/master/<date>.json` (input) -> `python3 scripts/master_report.py <date>` -> `reports/master/data/*.json` + `reports/master/<date>.md`
- Model: one Sonnet subagent, short run. Read-only on every channel: the master agent never posts, emails customers, edits the website or changes another agent's playbook. It only proposes.

## Steps (keep the run under ~25 tool calls)
1. Setup as in agents/README.md. Copy the previous `reports/master/<last date>.json` to `reports/master/<today>.json` and update every value.
2. **Agent logs** (read only the entries since the last report): `reports/agents/*.md`, `reports/agents/handoff.md` (count open `- [ ]`), `outreach/sent_log.json` (sent count, warm_leads, do_not_send), `outreach/won_orders.json`, `seo/ai_visibility_log.json`, `seo/data/<latest>.json`, latest `seo/CHANGELOG-*`.
3. **Live numbers** (one batched Composio call where possible):
   - Instagram: INSTAGRAM_GET_USER_INFO (`me`, followers_count, media_count); INSTAGRAM_GET_USER_INSIGHTS total_value for reach, accounts_engaged, total_interactions, profile_views, website_clicks, views over the last 28 days.
   - Facebook: FACEBOOK_GET_PAGE_DETAILS page 142803116227246 (fan_count, followers_count).
   - Pinterest: PINTEREST_GET_ACCOUNT_ANALYTICS last 28 days and the 28 days before (IMPRESSION, SAVE, OUTBOUND_CLICK, PIN_CLICK, ENGAGEMENT); profile follower_count.
   - Search Console / GA4 / Bing: use the Data & SEO agent's latest `seo/data/<date>.json` (it runs 07:37 Mon/Thu, before this report). Do not query again.
   - Shopify: `run-analytics-query` `FROM sales SHOW orders, net_sales TIMESERIES week SINCE -28d UNTIL today` and `FROM sessions SHOW sessions, conversion_rate SINCE -28d UNTIL today`. If Shopify is unavailable, use GA4 transactions and say so.
   - Pipedrive: getDeals (open/won/lost counts and values), getLeads count.
   - Google Business and LinkedIn: no insight reader is connected (29 Oct). Count posts from the logs and keep the "blind" status until a reader exists.
4. **Score each agent 0-100**: output against its playbook (40), business impact in the numbers above (40), reliability and blockers (20). Write 1 line each for output, impact, issue, next step. Compare with the last report: name what improved or slipped.
5. **Recommendations**: 5-7 ranked actions, each with owner and effort. Prefer actions that cut usage or move sales. Never recommend anything that breaks the hard rules in CLAUDE.md.
6. Run `python3 scripts/master_report.py <today>`.
7. **Dashboard refresh** (Dashboard artifact above): upload each changed `reports/master/data/{kpis,agents,actions,summary}.json` with the Artifact tool (`url` = dashboard, `asset: true`, `file_path`), then with ArtifactData read `datasets/<id>` and `update` it with the new `source.url`, `source.name` and `updated: {at, by: "Master agent (Claude)"}` (pin `if_version`). Do not change `files/index.html` unless a new metric needs a new tile.
8. **Email** amit2sap@gmail.com (one email, subject "GrassCrafts master report <date>"): the takeaway, top 3 actions, the dashboard link. Keep it under 15 lines. This counts as the owner summary, not outreach.
9. Append 3-5 lines to `reports/agents/master.md`; commit "master: report <date>" and push.

## Rules
- Facts only from tools and repo files. A number you could not read is "not available", never 0 or a guess. Name the window for every number.
- Do not count historical orders (e.g. Pipedrive deals entered on 28 Oct for Jan/Feb 2026 form orders) as new sales.
- Respect the USAGE SAVER rules in agents/README.md: if the weekly limit is in tier 2 or 3, skip step 3's live calls except Shopify and Pinterest, and say so in the report.
