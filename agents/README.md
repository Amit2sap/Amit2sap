# GrassCrafts agent team

Each agent is a separate daily scheduled run (a fresh session) with one job. All agents share the rules below.

| Agent | Playbook | Runs (IST) | Channels |
|---|---|---|---|
| Data & SEO | `agents/data_seo.md` | 08:37 Mon, Thu | Windsor, Ahrefs, Search Console |
| Lead Research (one agent, 3–4 segments a day in rotation) | `agents/lead_research.md` | 09:07 Mon–Fri (Sonnet, ≤8 leads per segment) | Web search, Hunter.io → `outreach/leads/*.json` |
| Email & Actions (lead agent) | `outreach/DAILY_RUNBOOK.md` + `agents/email_actions.md` | 10:22 daily | Gmail, WhatsApp alerts to Sristi, hot leads |
| Google Business | `agents/google_business.md` | paused until Pipedream is connected | GrassCrafts by Abalone + Makhana by GrassCrafts (Zapier) |
| Website & Search | `agents/website.md` | 11:52 Mon, Wed, Fri | Shopify, Search Console |
| Social (Instagram, then Facebook, then Pinterest, one agent) | `agents/instagram.md`, `agents/facebook.md`, `agents/pinterest.md` | 12:41 daily | @grasscrafts.com_, Page 142803116227246, Pinterest amit2sap |
| AI Search | `agents/ai_search.md` | 13:47 Thursdays | Buyer questions, llms.txt, citation targets |

**Usage rules (owner, 19 Oct 2026):** runs are spaced at least 30 minutes apart and never run side by side. Routine agents (Data & SEO, Google Business, Website, Social, AI Search) run on the lighter Sonnet model. Lead Research and Email & Actions keep the default model. Keep reports short.

**Usage fixes (owner, 23 Oct 2026):** (1) no image viewing in routine runs; catalogue fixes change only the pages that need it, one screenshot per changed page; product-photo job off. (2) every agent reads only the files its step needs. (3) Email & Actions runs on Sonnet and sends in batches (up to 20 emails per Composio call). (4) one agent at a time: Data & SEO 07:37 Mon/Thu, Lead Research 08:07 weekdays, Email 10:22, Social 13:41, AI Search 13:47 Thu, Reply watcher 15:07 and 19:07 (skips if the email run is still going), Website 17:22 Mon/Wed/Fri. (5) move all runs to a fresh session once Pipedream is signed in.

**Usage limit (owner, 23 Oct 2026):** fewer runs to stay inside the session limit. Reply watcher 3x a day, Website Mon/Wed/Fri, Data & SEO Mon/Thu, Lead Research weekdays on Sonnet, Google Business paused until Pipedream works.

## Setup at the start of every run
1. If the repo is missing, clone `https://github.com/amit2sap/amit2sap`. Then `git checkout claude/grassctafts-sales-growth-d8azah && git pull origin claude/grassctafts-sales-growth-d8azah`.
2. Read this file, `agents/STRATEGY.md` (live strategy), `agents/calendar.md` (festivals and seasons) and your own playbook. Read the last 3 days of your own log in `reports/agents/`.
3. Tools come from the MCP servers: Composio (Gmail session, Search Console, Facebook Graph, workbench web_search), Shopify, Zapier (Google Business Profile), Windsor.ai. If a tool you need is missing or refused, **do not work around it**. Log it as a blocker for the owner.

## Shared rules (every agent)
- **Facts.** Use only facts from the store (Shopify product data and prices) or from repo files. Never invent MOQ, trade prices, lead times, awards, client names, certifications or reviews. Madurkathi is GI-tagged (GI no. 567). Do not claim a GI for Sabai.
- **No commitments.** Never quote trade or volume prices, discounts, lead times, samples or partnerships. Route those to the Email & Actions agent: add a line to `reports/agents/handoff.md`.
- **Hot leads.** Anyone asking for a price list, bulk quote or samples is a hot lead. Hand it off the same day (see `outreach/DAILY_RUNBOOK.md` section 1b).
- **Contact details.** WhatsApp/phone: +91 62907 44782. Website: grasscrafts.com. Brand name: "GrassCrafts" (Google listing: "GrassCrafts by Abalone").
- **Posting days (owner, 17 Oct): every alternate day.**
  - Posting days are 18, 20, 22 Oct 2026 and so on: post only when `(today - 2026-10-18).days % 2 == 0`.
  - On a posting day: at most 1 feed post per channel (Pinterest: up to 5 pins). No duplicate text across channels; adapt it per channel.
  - Blog articles follow the same posting days.
  - **Off days:** reply to comments, reviews and messages; prepare the next post. No feed posts.
  - Replies, reviews, hot leads and emails still run **every day**.
- **Festivals and seasons.** Pick the theme from `agents/calendar.md`. An occasion within the next 21 days wins; otherwise use the weekly mix. B2B pitches go 6–8 weeks before the occasion.
- **Competitor watch (every agent, weekly on Mondays only, from 19 Oct 2026).**
  - Spend about 10 minutes checking the competitors in `agents/STRATEGY.md` **on your own channel**. What did they post or publish, what offer or new product did they launch, which keywords or pages rank, what got engagement?
  - Append 2–5 dated bullets to `reports/competitor_watch.md` under your agent name. Each bullet gives the observation, a source URL, and "→ what we should do".
  - Use only public information: web search snippets, public pages and public posts. No logging in to competitor accounts, no fake accounts, no copying their images or text.
  - The lead agent turns these findings into updates to `agents/STRATEGY.md` on Mondays.
- **Competitor customer intelligence (with the Monday competitor watch, owner 17 Oct; weekly from 19 Oct).** Find **who buys from our competitors**, what they buy, how often, and at what price. Then we can target them and shape our offer.
  - **Business buyers** (companies, hotels, jewellers, planners, gifting firms). Public evidence only, each with a source URL:
    - client logos and "our clients" pages;
    - case studies, testimonials and press ("X partners with Brown Living for Diwali hampers");
    - LinkedIn and Instagram posts where a company shows a competitor's gift or tags them;
    - GeM and tender awards; trade-fair buyer lists;
    - IndiaMART buy requirements.
  - Record each one in `outreach/competitor_customers.json` with these fields: buyer, segment, competitor used, products, occasion, timing (month), quantity, budget or price signal, decision-maker role, source URL, date found.
  - Also add the buyer as a lead in `outreach/leads/<segment>.json`, with `"competitor_used"` filled in.
  - **Consumers.** Only **aggregate patterns** from public reviews and ratings (Google, Amazon, Trustpilot, Instagram comments): what people buy, price bands, occasions, complaints, and what they praise. **Never profile or contact individual consumers** from a competitor's reviews.
  - **Budget.** Use real figures only: tender value, the competitor's published price, or the buyer's own retail price. Anything else is labelled `"estimate: <basis>"`. Never present a guess as fact.
  - No logging in to competitor or customer accounts, no fake identities, no buying lists of personal data.
- **B2B priorities** (owner, 17 Oct): corporate gifts, cane planters, wedding baskets, sustainable décor brands. Every channel gives these about 60% of its content.
- **Logging.** Before finishing, append a dated entry to `reports/agents/<agent>.md` covering what you did, numbers seen, and blockers. Commit with message "<agent>: daily run <date>", then push to the branch.
- **Reviews (owner, 17 Oct).** Follow `outreach/REVIEW_KIT.md`. Agents never write or post reviews as a customer. They only collect real reviews with permission, reply to reviews, and reuse permitted reviews in posts (quoted exactly).
- **Owner email.** Only email amit2sap@gmail.com when the owner must act (a blocker, a complaint, a hot lead). The Email & Actions agent sends the one daily summary.

## Scheduled tasks (created 17 Oct 2026, changed 19 Oct 2026 to save usage)
Fresh-session scheduled tasks cannot carry connectors in this organisation (checked again 19 Oct). So every task fires into the main session `session_01CExgX3LnZkdy4AwdW7vCVh`, which holds Composio, Shopify, Zapier and Windsor. Each task then launches ONE background subagent with its playbook.

| Agent | Task ID | Time (IST) | Subagent model |
|---|---|---|---|
| Data & SEO | trig_01CUREij3CJdjc5fZN4htmSe | 07:37 Mon, Thu | Sonnet |
| Lead Research | trig_01XKSz9LU53FqDRG1yEBbnth | 08:07 Mon–Fri | Sonnet |
| Email & Actions (lead) | trig_01XBZ9tjd6uumiGACGGgYK6L | 10:22 daily | Sonnet |
| Google Business | trig_01RqepKXvQDRmUEzzVRymJ31 | 11:14 Tue, Sat | Sonnet |
| Social (Instagram + Facebook + Pinterest + LinkedIn + actions page) | trig_013nvpY1RgSiVREyaGQW3y3U | 13:41 daily (posts on alternate days) | Sonnet |
| Reply watcher | trig_01Mb2NVBNMF8FgnxKjN9gJg6 | 15:07, 19:07 | Sonnet |
| AI Search | trig_01DgrfXPRKk3z49NyuonLWcn | 16:07 Mon, Thu (moved 29 Oct from 13:47, which clashed with Social) | Sonnet |
| Website & Search | trig_01U3ezGQGdHZNkSeNyUyJEuN | 17:22 Mon, Wed, Fri | Sonnet |
| Usage guard | trig_01EWtAc9rBda9NTBXixc4Mv2 | every 4 h (:37) | Haiku, own session |
| Facebook / Pinterest (old, merged into Social) | trig_014gkGWjNj9vrFmFdFnmnQc8 / trig_01CArxgJ6ZCgnFgHeXaGn9W8 | disabled | — |

**Shared weekly limit (29 Oct):** the same Claude account also runs the Aurelia study coach (7 runs/weekday) and the job-application agent (2 runs/weekday, which failed on 28 Oct with "usage limit reached"). They draw on the same weekly limit as GrassCrafts; the usage guard pauses the Aurelia tasks in tier 3.

**LinkedIn manual kit (owner, 29 Oct):** Mondays in the Lead Research run, 5 people for Amit to contact himself (agents/linkedin_manual_outreach.md); Lusha used only per that file's budget.

**Usage optimisations (29 Oct):** actions-page kit only on posting days; owner to-dos in Todoist instead of long owner emails; no two jobs at the same minute (AI Search moved); Social on off days = comments + approved saves only.

**Known blockers at set-up:**
- **Instagram:** Composio is connected to the wrong account (@terraleatherco). Windsor reads are paused (free plan, 8 accounts connected).
- **Pinterest:** connected via Composio (`pinterest_whosen-hoose`) on 17 Oct; test pin 1127799931724040361 posted.
- **Facebook:** reading posts with a Page token worked, but one later Page-token call was refused by the permission prompt.
- **AI Search agent** (agents/ai_search.md): weekly, Thursdays 13:47 IST, scheduled task trig_01DgrfXPRKk3z49NyuonLWcn. Runs the buyer-question checks, keeps llms.txt honest and builds the citation targets.
- **Data & SEO agent** (agents/data_seo.md, toolkit seo/data_agent.py): Mon/Thu at 08:37 IST, scheduled task trig_01CUREij3CJdjc5fZN4htmSe. Our own Windsor + Ahrefs: GSC rank tracker, striking distance, cannibalisation, low CTR, Bing backlinks, GA4, GBP and Shopify.

**Windsor.ai is retired (owner, 22 Oct 2026).** The owner is removing every Windsor connection. Agents must not use Windsor tools for anything. Instead use:
- Instagram: Composio, @grasscrafts.com_ (instagram_basoid-oer)
- Facebook, Pinterest, Search Console and GA4: Composio
- Google Business: Pipedream, in the new session, once it is connected

If a playbook below still mentions Windsor, ignore that line.

## Usage saving (owner, 26 Oct: weekly limit 84% used, resets Wed 16:30 IST)
Until the Wednesday reset: one short Sonnet subagent per job, no extra research, no image viewing, read only the files the job needs, reports of 5 lines or fewer, skip a job when it has nothing new to do (no replies, no orders, no due follow-ups). Interactive owner sessions: short answers, no re-reading of large files.

## Usage guard (owner, 27 Oct 2026)
Scheduled task "GrassCrafts Usage guard (every 4 hours)" (trig_01EWtAc9rBda9NTBXixc4Mv2, runs in its own small Haiku session session_019TVCSFPyP9JjQGivxX4AVd; fresh sessions lack the scheduling tools). It reads the Claude weekly-limit status and pauses/resumes GrassCrafts tasks by tier, marking its own pauses with " [paused by usage guard]" in the task name:
- Never paused: Email & Actions, Reply watcher.
- Tier 2 (paused when the limit is near and the reset is more than 36 h away, or when the limit is hit): Lead Research, Google Business.
- Tier 3 (paused first, on any warning): Social, Website, Data & SEO, AI Search.
- On "allowed" it resumes only the tasks it paused. Tasks the owner pauses himself (no suffix) are left alone.
- 28 Oct: owner parked all WhatsApp tasks (agents/whatsapp_orders.md paused). Usage guard did not resume after the 16:30 reset by 18:04 (its run was at 14:07, before reset); main session resumed the 6 tasks manually.
