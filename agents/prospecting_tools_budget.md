# B2B prospecting tools — order of use and free-plan budgets (owner, 29 Oct 2026)

Goal: only the best, authentic B2B buyers; never waste free credits. Pipedrive stays the ONE CRM — never create contacts, lists or sequences inside Apollo, Lusha or Vibe, and never send email or call from them (all email goes through the Gmail agent and its 100/day cap).

## Order of use (stop at the first step that gives a verified answer) — tested 29 Oct
1. **Free:** the company's own website (team/about/contact pages) via Exa / Firecrawl; Pipedrive + outreach/leads + sent_log duplicate check.
2. **Find the buyer's NAME:** website first; then **Lusha `prospecting_contact_search`** (1 credit per 25 people; previews give name, title and often the LinkedIn URL, no reveal needed). Batch: one search should cover several target companies (pass several domains / one segment + city).
   - Apollo people search is **NOT available on the Apollo free plan** (tested 29 Oct: "plan does not include People API Search"). Do not call `apollo_mixed_people_api_search`, `apollo_agent_find_prospects` or other Apollo agent tools.
3. **Get the work EMAIL for a named buyer:** **Apollo `apollo_people_match`** with name + company domain (or LinkedIn URL) — 1 lead credit only if found; accept only an email Apollo marks verified. Use Apollo FIRST because it has 200 credits vs Lusha's 40. Never set reveal_phone_number / waterfall options.
4. **Lusha email reveal** (1 credit) — only if Apollo found nothing and the lead is warm/hot.
5. **Vibe Prospecting** — company DISCOVERY only. FREE: `fetch-entities-statistics` (counts) and `fetch-entities` masked previews (5 rows: company name, website, city, description). PAID (checked 29 Oct): `show-sample` = 5 credits per table; export = about 1 credit per company row (contact enrichment costs more); non-paid accounts are capped at 30 rows per export. Agents use only the free calls, at most once a month (first Monday) per segment, filtering by industry category + city rather than website keywords (a 'corporate gifting' keyword search returned HR firms and snack brands); then verify each company on its own website. NEVER `show-sample`, enrich or `export-to-csv` without the owner's explicit OK in chat.
6. Never use Apollo `apollo_organizations_enrich` (1 credit) — Firecrawl/the company site gives the same facts.

## Monthly budgets (check balances first: Apollo `apollo_users_api_profile` include_credit_usage, Lusha `account_usage` — both free)
| Tool | Balance 29 Oct | Monthly spend cap | Reserve |
|---|---|---|---|
| Apollo lead credits | 200 (100 = one-time bonus) | `people_match` email lookups ≤ 10/week (≈40/month) | keep ≥ 40 |
| Apollo direct-dial (phone) | 160 | not used (async phone reveal; Sristi uses published numbers) | — |
| Apollo AI credits | 5,000 | research summaries only if useful; never sequences | — |
| Lusha | 40 | contact searches to find names ≤ 6/month (each covers 25 people) + email reveals only when Apollo fails (≤ 8/month) | keep ≥ 8 |
| Vibe Prospecting | balance not shown by the API (see vibeprospecting.ai account page) | 0 paid without owner OK (sample 5 cr, ~1 cr per company row) | — |
Never reveal phones from Lusha (5 credits). If any balance hits its reserve, only free steps until the reset; log it in the owner email.

## Who does what
- **Lead Research (weekdays):** steps 1–4 for its segments; max 2 Apollo `people_match` a day, only for A-fit companies whose only published contact is a generic inbox (the named-buyer email then gets a personal pitch from the Email agent). Mondays also Amit's LinkedIn kit (names from step 2, no email lookups needed).
- **Email & Actions / Reply watcher:** when a warm reply comes from a generic inbox and Sristi needs a named buyer → one Apollo reveal.
- **Log every credit spent** (date, tool, company, role, credits, new balance) in reports/agents/lead_research.md; weekly totals go into the Monday owner report.
