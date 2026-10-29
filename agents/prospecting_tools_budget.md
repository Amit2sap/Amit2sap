# B2B prospecting tools — order of use and free-plan budgets (owner, 29 Oct 2026)

Goal: only the best, authentic B2B buyers; never waste free credits. Pipedrive stays the ONE CRM — never create contacts, lists or sequences inside Apollo, Lusha or Vibe, and never send email or call from them (all email goes through the Gmail agent and its 100/day cap).

## Order of use (stop at the first step that gives a verified answer)
1. **Free:** company's own website (team/about/contact pages) via Exa / Firecrawl; Pipedrive + outreach/leads + sent_log duplicate check.
2. **Apollo people search** (`apollo_mixed_people_api_search`, `apollo_mixed_companies_search`) — names, titles, LinkedIn URLs; normally NO credits. Use it to find the right buyer and for Amit's LinkedIn kit. Check the response's mcp_credits block; if a search shows a cost, stop and log.
3. **Apollo email reveal** (`apollo_people_match`, 1 lead credit) — only for an A-fit or warm company whose only published contact is a generic inbox, and only for a buyer role (founder/owner, procurement/purchase, admin, gifting/marketing head, hotel F&B/rooms head). Accept only emails Apollo marks verified.
4. **Lusha** — second opinion when Apollo has no verified email (rules in agents/linkedin_manual_outreach.md; 40 credits).
5. **Vibe Prospecting** — company DISCOVERY only. FREE: `fetch-entities-statistics` (counts) and `fetch-entities` masked previews (5 rows: company name, website, city, description). PAID (checked 29 Oct): `show-sample` = 5 credits per table; export = about 1 credit per company row (10 rows quoted 10 credits; contact enrichment costs more); non-paid accounts are capped at 30 rows per export by default. Agents use only the free calls, then verify companies on their own websites. NEVER `show-sample`, enrich or `export-to-csv` without the owner's explicit OK in chat. Results are noisy for our niche (a 'corporate gifting' keyword search returned HR firms and snack brands), so treat them as ideas, not leads.

## Monthly budgets (check balances first: Apollo `apollo_users_api_profile` include_credit_usage, Lusha `account_usage` — both free)
| Tool | Balance 29 Oct | Monthly spend cap | Reserve |
|---|---|---|---|
| Apollo lead credits | 200 (100 = one-time bonus) | email reveals ≤ 10/week (≈40/month) | keep ≥ 40 |
| Apollo direct-dial (phone) | 160 | ONLY when Sristi asks for a hot lead's number: ≤ 5/month | — |
| Apollo AI credits | 5,000 | research summaries only if useful; never sequences | — |
| Lusha | 40 | per agents/linkedin_manual_outreach.md (≤ 16 reveals) | keep ≥ 8 |
| Vibe Prospecting | balance not shown by the API (see vibeprospecting.ai account page) | 0 paid without owner OK (sample 5 cr, ~1 cr per company row) | — |
Never reveal phones from Lusha (5 credits). If any balance hits its reserve, only free steps until the reset; log it in the owner email.

## Who does what
- **Lead Research (weekdays):** steps 1–3 for its segments; max 2 Apollo reveals a day; Mondays also Amit's LinkedIn kit.
- **Email & Actions / Reply watcher:** when a warm reply comes from a generic inbox and Sristi needs a named buyer → one Apollo reveal.
- **Log every credit spent** (date, tool, company, role, credits, new balance) in reports/agents/lead_research.md; weekly totals go into the Monday owner report.
