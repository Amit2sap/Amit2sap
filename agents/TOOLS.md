# Tool map (tested 27 Oct 2026) — which connector each agent uses

## Working and adopted
| Tool | What it gives us | Who uses it | Limits / cost |
|---|---|---|---|
| **Pipedrive** (claude.ai connector) | CRM: organisations, people, deals, activities, notes. Account "ABALONE design studio, Grasscrafts.com", INR, 1 pipeline: Qualified → Contact Made → Demo Scheduled → Proposal Made → Negotiations Started | Reply watcher + Email & Actions: every lead that REPLIES with interest becomes an organisation + person + deal (stage "Contact Made"; hot = "Qualified" label Hot lead) with a note of the thread; won orders marked Won (e.g. Shweta Chitale). Cold, never-replied leads stay in outreach/leads/*.json only. | Free tier; keep records lean. Never invent values; deal value only if the buyer stated a quantity/price. |
| **Jotform** (claude.ai connector) | Our 4 catalogue/order forms (Sabai, Sabai-2, Water Hyacinth, Kauna) — all have submissions | Reply watcher: each run list submissions since the last run (mcp__Jotform__list_submissions with the 4 form ids, date filter), treat each as a buyer enquiry: brief to Sristi (CC Amit) + Pipedrive deal. | Free plan. |
| **Exa** (claude.ai connector) | Web search with sources, page fetch | Lead research (company sites, contact pages), AI Search checks | Use instead of paid search where possible. |
| **Firecrawl** (claude.ai connector) | Search + scrape any URL incl. Amazon.in / Flipkart listing pages | Data & SEO marketplace watch (Mon/Thu, 10 categories) — first choice; TinyFish only if Firecrawl fails | Billed per page: max ~10 scrapes per run; government search and tool discovery are free. |
| **Lusha** (claude.ai connector) | B2B decision-maker emails/phones | ONLY for hot/warm B2B leads that have a generic inbox and need a named buyer (e.g. procurement/marketing head). Reveal email only (1 credit), never phones (5 credits). | FREE plan: 40 credits (balance 40 on 29 Oct), 100 calls/day. Monthly budget and rules in agents/linkedin_manual_outreach.md (also used to find people for Amit's weekly LinkedIn kit, search previews only). Log each use in reports/agents/lead_research.md. Lusha "valid" contacts count as verified business emails. |
| **Google Drive** (claude.ai connector, native) | Read/search/create files (the old Composio Drive create was 403) | Share the trade sample sheet PDF, monthly reports with Sristi | — |
| **Moda** | Editable designs, catalogue, social graphics | Trade catalogue updates, social carousels from REAL photos only | Image generation stays paused. |
| **Supermetrics** | Marketing data incl. social (manage_social_media) | Data & SEO (Instagram/Facebook insights if authorised) | Check auth status before use. |
| Shopify, Composio (Gmail, Instagram, Facebook, Pinterest, LinkedIn, GSC, GA4, Bing, Hunter, WhatsApp, Upload-Post), claude-code-remote | unchanged | as before | |

## New connectors reviewed 29 Oct 2026
| Tool | Verdict | Use |
|---|---|---|
| **Todoist** (claude.ai, Amit's Free account) | ADOPTED | Project "GrassCrafts – owner actions" (id 6hrWjrHwPxWHV4rw) = the owner's to-do list with phone reminders. Email & Actions adds each NEW owner decision/click as a task (dueString, priority p1–p4; Free plan has no deadlines, no assignees) and completes tasks the owner has done; the daily owner email then only says "N open owner tasks in Todoist" instead of repeating them. Sristi stays on her daily form email (not Todoist). |
| **PostHog** (project 695384 "GrassCrafts website") | ADOPTED 29 Oct (owner) | Snippet in theme copy 189857562797 "Grasscrafts – PostHog analytics 29 Oct", waiting for the owner to publish (seo/CHANGELOG-2026-10-29-posthog.md). Once live: Website agent (Mon) and the weekly owner report read web analytics, funnel product_viewed -> add to cart -> checkout click, and 3-5 replays of sessions that added to cart but did not check out; report what blocked them. Read only; never change PostHog settings without the owner. |
| **LunarCrush** | NOT USED | Crypto/stocks social analytics; no subscription, outputs limited. No GrassCrafts value. |
| **Kuliko AI** (study library), **LinkedIn Hiring Pro** (one free job post) | NOT USED | Not GrassCrafts work. |
| Plugin MCPs (Canva, Figma, HubSpot, Klaviyo, Similarweb, Notion, Slack, Asana, Supermetrics plugin, Ahrefs plugin…) | FAIL to connect from cloud sessions (proxy 403) | Do not call. Their skills (marketing:brand-review, performance-report, seo-audit, content-creation) still work without the connector. |

## Kapso (WhatsApp platform) — set up 29 Oct 2026, not live yet
**Status check 30 Oct 2026 (read-only):** Kapso now has a production number +1 711-734-3219 "GrassCrafts" (phone_number_id 1400850673110435, WABA 1111534238529862, connected 30 Oct 09:11 UTC). Health = DEGRADED: (1) display name "GrassCrafts" PENDING_REVIEW, so sending is limited; (2) Meta billing error 141006 on the WABA (payment method), which blocks business-initiated messages; (3) webhook not yet verified by Meta. The +91 81004 47884 "Gift Hamper" number shows code_verification_status EXPIRED, and all numbers' webhooks point to a temporary ngrok URL (inbound may be lost). The 16 approved templates belong to the 81004 WABA (28037860215843187); a new WABA needs its own templates. Agents send nothing until the owner fixes billing and confirms which number to use.
**Composio connection kapso_parser-billon ACTIVE (29 Oct)** — use this (works in all sessions; the .mcp.json route below is only a fallback). On 29 Oct Kapso held ONLY its Sandbox number (phone_number_id 597907523413541); the GrassCrafts Meta number +91 81004 47884 is not yet connected inside Kapso (owner: Kapso → WhatsApp → Connect number via Meta embedded signup). Read-only until the owner restarts WhatsApp work.
Project MCP server in `.mcp.json` (https://api.kapso.ai/mcp, key read from env var KAPSO_API_KEY — never commit the key). Needs, from the owner: (1) KAPSO_API_KEY added in the cloud environment settings, (2) api.kapso.ai allowed in the environment's network access, (3) a NEW session. Until the owner restarts WhatsApp work (paused 28 Oct) and Meta billing error 141006 is fixed, agents use Kapso READ-ONLY (inbox, conversations) and send nothing.

## Plugins (skills) worth using
- marketing:brand-review — check product copy/claims before publishing (e.g. the unsourced "carbon-negative", "2,200 L water saved" claims).
- marketing:competitive-brief, marketing:seo-audit, marketing:performance-report — monthly reviews, run inside the existing agent, not as extra agents.
- marketing:email-sequence — redesign the follow-up sequence once reply data exists.

## Connected but NOT usable now
- **Ahrefs**: "Insufficient plan" (API not in plan). Do not call it in scheduled runs.
- **Semrush: REMOVED by owner decision 27 Oct (paid only). Never use.**
- **Consensus, Anthropic Economic Index, BigQuery, Indeed, HyperFrames (HeyGen video; compose works only from claude.ai chat, not agents)**: no GrassCrafts use now (Indeed is for Amit's job search).
- **REMOVED by owner decision 27 Oct, never use:** Gmail (native connector; Composio Gmail gmail_movie-arab stays), Unsplash, Postman, Scite, Bling.
- **Apollo.io and Vibe Prospecting RE-ADDED by owner 29 Oct** (free plans): use only per agents/prospecting_tools_budget.md (Apollo free plan: NO people search; use only people_match for a named buyer's email, 1 credit, 200 credits incl. one-time 100 bonus; Vibe: free counts/masked previews only, no paid sample/export without owner OK).
- **Meta Ads (Composio metaads)**: CONNECTED 28 Oct (account metaads_coolth-ditone, Sristi Dey II, ads_read; token valid ~60 days, renew before late Dec). Was: connection being set up 28 Oct (owner to sign in as the ad-account owner, likely Sristi Dey II). Ad accounts seen: Sristi Dey II act_1003688057061695, Grasscrafts act_779321797815849 / act_781482474833321 (read-only), act_1380279345583309, Sristi Dey act_1183034639541794. Use METAADS_GET_INSIGHTS for the weekly report and a daily lead check.
