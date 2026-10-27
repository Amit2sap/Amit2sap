# Tool map (tested 27 Oct 2026) — which connector each agent uses

## Working and adopted
| Tool | What it gives us | Who uses it | Limits / cost |
|---|---|---|---|
| **Pipedrive** (claude.ai connector) | CRM: organisations, people, deals, activities, notes. Account "ABALONE design studio, Grasscrafts.com", INR, 1 pipeline: Qualified → Contact Made → Demo Scheduled → Proposal Made → Negotiations Started | Reply watcher + Email & Actions: every lead that REPLIES with interest becomes an organisation + person + deal (stage "Contact Made"; hot = "Qualified" label Hot lead) with a note of the thread; won orders marked Won (e.g. Shweta Chitale). Cold, never-replied leads stay in outreach/leads/*.json only. | Free tier; keep records lean. Never invent values; deal value only if the buyer stated a quantity/price. |
| **Jotform** (claude.ai connector) | Our 4 catalogue/order forms (Sabai, Sabai-2, Water Hyacinth, Kauna) — all have submissions | Reply watcher: each run list submissions since the last run (mcp__Jotform__list_submissions with the 4 form ids, date filter), treat each as a buyer enquiry: brief to Sristi (CC Amit) + Pipedrive deal. | Free plan. |
| **Exa** (claude.ai connector) | Web search with sources, page fetch | Lead research (company sites, contact pages), AI Search checks | Use instead of paid search where possible. |
| **Firecrawl** (claude.ai connector) | Search + scrape any URL incl. Amazon.in / Flipkart listing pages | Data & SEO marketplace watch (Mon/Thu, 10 categories) — first choice; TinyFish only if Firecrawl fails | Billed per page: max ~10 scrapes per run; government search and tool discovery are free. |
| **Lusha** (claude.ai connector) | B2B decision-maker emails/phones | ONLY for hot/warm B2B leads that have a generic inbox and need a named buyer (e.g. procurement/marketing head). Reveal email only (1 credit), never phones (5 credits). | FREE plan: 40 credits total, 100 calls/day. Log each use in reports/agents/lead_research.md. Lusha "valid" contacts count as verified business emails. |
| **Google Drive** (claude.ai connector, native) | Read/search/create files (the old Composio Drive create was 403) | Share the trade sample sheet PDF, monthly reports with Sristi | — |
| **Moda** | Editable designs, catalogue, social graphics | Trade catalogue updates, social carousels from REAL photos only | Image generation stays paused. |
| **Supermetrics** | Marketing data incl. social (manage_social_media) | Data & SEO (Instagram/Facebook insights if authorised) | Check auth status before use. |
| Shopify, Composio (Gmail, Instagram, Facebook, Pinterest, LinkedIn, GSC, GA4, Bing, Hunter, WhatsApp, Upload-Post), claude-code-remote | unchanged | as before | |

## Plugins (skills) worth using
- marketing:brand-review — check product copy/claims before publishing (e.g. the unsourced "carbon-negative", "2,200 L water saved" claims).
- marketing:competitive-brief, marketing:seo-audit, marketing:performance-report — monthly reviews, run inside the existing agent, not as extra agents.
- marketing:email-sequence — redesign the follow-up sequence once reply data exists.

## Connected but NOT usable now
- **Ahrefs**: "Insufficient plan" (API not in plan). **Semrush**: active subscription but 0 API units. Do not call them in scheduled runs.
- **Consensus, Anthropic Economic Index, BigQuery, Indeed, HyperFrames (HeyGen video; compose works only from claude.ai chat, not agents)**: no GrassCrafts use now (Indeed is for Amit's job search).
- Incomplete sign-ins (owner can finish in claude.ai connector settings if wanted): Gmail (native; Composio Gmail already works), Apollo.io, Unsplash (not needed: real photos only), Vibe Prospecting, Postman, Scite, Bling.
