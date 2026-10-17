# GrassCrafts agent team

Each agent is a separate daily scheduled run (a fresh session) with one job. All agents share the rules below.

| Agent | Playbook | Runs (IST) | Channels |
|---|---|---|---|
| Lead Research (11 segment agents, run in parallel) | `agents/lead_research.md` | 09:07 daily | Web search, Hunter.io → `outreach/leads/*.json` |
| Email & Actions (lead agent) | `outreach/DAILY_RUNBOOK.md` + `agents/email_actions.md` | 09:52 daily | Gmail, WhatsApp alerts to Sristi, hot leads |
| Google Business | `agents/google_business.md` | 10:44 daily | GrassCrafts by Abalone + Makhana by GrassCrafts (Zapier) |
| Website & Search | `agents/website.md` | 11:22 daily | Shopify, Search Console, AI-search check |
| Instagram | `agents/instagram.md` | 12:11 daily | @grasscrafts.com_ |
| Facebook | `agents/facebook.md` | 12:43 daily | Page "Grasscrafts by Abalone" (142803116227246) |
| Pinterest | `agents/pinterest.md` | 13:18 daily | Pinterest account amit2sap |

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
  - **Off days:** reply to comments, reviews and messages; run the competitor watch; prepare the next post. No feed posts.
  - Replies, reviews, hot leads and emails still run **every day**.
- **Festivals and seasons.** Pick the theme from `agents/calendar.md`. An occasion within the next 21 days wins; otherwise use the weekly mix. B2B pitches go 6–8 weeks before the occasion.
- **Competitor watch (every agent, every day).**
  - Spend about 10 minutes checking the competitors in `agents/STRATEGY.md` **on your own channel**. What did they post or publish, what offer or new product did they launch, which keywords or pages rank, what got engagement?
  - Append 2–5 dated bullets to `reports/competitor_watch.md` under your agent name. Each bullet gives the observation, a source URL, and "→ what we should do".
  - Use only public information: web search snippets, public pages and public posts. No logging in to competitor accounts, no fake accounts, no copying their images or text.
  - The lead agent turns these findings into updates to `agents/STRATEGY.md` every day.
- **Competitor customer intelligence (every agent, every day, owner 17 Oct).** Find **who buys from our competitors**, what they buy, how often, and at what price. Then we can target them and shape our offer.
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
- **Owner email.** Only email amit2sap@gmail.com when the owner must act (a blocker, a complaint, a hot lead). The Email & Actions agent sends the one daily summary.

## Scheduled tasks (created 17 Oct 2026)
Fresh-session scheduled tasks cannot carry connectors in this organisation. So every task fires into the main session `session_01CExgX3LnZkdy4AwdW7vCVh`, which holds Composio, Shopify, Zapier and Windsor. Each task then launches its own background subagent with this playbook.

| Agent | Task ID | Time (IST) |
|---|---|---|
| Lead Research (11 segment agents) | trig_01XKSz9LU53FqDRG1yEBbnth | 09:07 |
| Email & Actions (lead) | trig_01XBZ9tjd6uumiGACGGgYK6L | 09:52 |
| Google Business | trig_01RqepKXvQDRmUEzzVRymJ31 | 10:44 |
| Website & Search | trig_01U3ezGQGdHZNkSeNyUyJEuN | 11:22 |
| Instagram | trig_013nvpY1RgSiVREyaGQW3y3U | 12:11 |
| Facebook | trig_014gkGWjNj9vrFmFdFnmnQc8 | 12:43 |
| Pinterest | trig_01CArxgJ6ZCgnFgHeXaGn9W8 | 13:18 |

**Known blockers at set-up:**
- **Instagram:** Composio is connected to the wrong account (@terraleatherco). Windsor reads are paused (free plan, 8 accounts connected).
- **Pinterest:** connected via Composio (`pinterest_whosen-hoose`) on 17 Oct; test pin 1127799931724040361 posted.
- **Facebook:** reading posts with a Page token worked, but one later Page-token call was refused by the permission prompt.
