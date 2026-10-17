# GrassCrafts agent team

Each agent is a separate daily scheduled run (a fresh session) with one job. All agents share the rules below.

| Agent | Playbook | Runs (IST) | Channels |
|---|---|---|---|
| Email & Actions (lead agent) | `outreach/DAILY_RUNBOOK.md` + `agents/email_actions.md` | 09:52 daily | Gmail, WhatsApp alerts to Sristi, hot leads |
| Google Business | `agents/google_business.md` | 10:44 daily | GrassCrafts by Abalone + Makhana by GrassCrafts (Zapier) |
| Website & Search | `agents/website.md` | 11:22 daily | Shopify, Search Console, AI-search check |
| Instagram | `agents/instagram.md` | 12:11 daily | @grasscrafts.com_ |
| Facebook | `agents/facebook.md` | 12:43 daily | Page "Grasscrafts by Abalone" (142803116227246) |
| Pinterest | `agents/pinterest.md` | 13:18 daily | Pinterest account amit2sap |

## Setup at the start of every run
1. If the repo is missing, clone `https://github.com/amit2sap/amit2sap`. Then `git checkout claude/grassctafts-sales-growth-d8azah && git pull origin claude/grassctafts-sales-growth-d8azah`.
2. Read this file and your own playbook. Read `reports/agents/` for the last 3 days of your own log.
3. Tools come from the MCP servers: Composio (Gmail session, Search Console, Facebook Graph, workbench web_search), Shopify, Zapier (Google Business Profile), Windsor.ai. If a tool you need is missing or refused, **do not work around it**. Log it as a blocker for the owner.

## Shared rules (every agent)
- **Facts.** Use only facts from the store (Shopify product data and prices) or from repo files. Never invent MOQ, trade prices, lead times, awards, client names, certifications or reviews. Madurkathi is GI-tagged (GI no. 567). Do not claim a GI for Sabai.
- **No commitments.** Never quote trade or volume prices, discounts, lead times, samples or partnerships. Route those to the Email & Actions agent: add a line to `reports/agents/handoff.md`.
- **Hot leads.** Anyone asking for a price list, bulk quote or samples is a hot lead. Hand it off the same day (see `outreach/DAILY_RUNBOOK.md` section 1b).
- **Contact details.** WhatsApp/phone: +91 62907 44782. Website: grasscrafts.com. Brand name: "GrassCrafts" (Google listing: "GrassCrafts by Abalone").
- **Posting limits.** At most 1 feed post per channel per day. No duplicate text across channels on the same day; adapt it per channel.
- **B2B priorities** (owner, 17 Oct): corporate gifts, cane planters, wedding baskets, sustainable décor brands. Every channel gives these about 60% of its content.
- **Logging.** Before finishing, append a dated entry to `reports/agents/<agent>.md` covering what you did, numbers seen, and blockers. Commit with message "<agent>: daily run <date>", then push to the branch.
- **Owner email.** Only email amit2sap@gmail.com when the owner must act (a blocker, a complaint, a hot lead). The Email & Actions agent sends the one daily summary.
