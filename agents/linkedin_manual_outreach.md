# LinkedIn manual outreach kit for Amit + Lusha budget (owner, 29 Oct 2026)

Amit sends LinkedIn connection requests and messages HIMSELF from his own profile. Agents never log in to LinkedIn, never send, never scrape LinkedIn. Agents pick the targets and write the texts; Amit copies, sends and ticks the task.

## When
Every **Monday** inside the Lead Research run (08:07 IST), after the day's segments. One kit per week. If a week is skipped, do not double up the next week.

## The kit (max 5 people a week)
1. **Pick 5 targets**, best fit first (in this order):
   - people at companies that already REPLIED or are open Pipedrive deals/leads (warm),
   - premium corporate-gifting firms, wedding/event planners, premium hotels/resorts, jewellers, gourmet hamper brands in `outreach/leads/*.json` that have only a generic inbox,
   - never a company in `outreach/sent_log.json` do_not_send, never a company with a lost deal, never the same person twice (check `outreach/linkedin_manual_log.json`).
   Role must be a buyer: founder/owner, procurement/purchase head, admin head, marketing or gifting head, F&B/rooms head (hotels).
2. **Find the person** (cheapest first): the company's own website team/about page; then Apollo people search (free, see agents/prospecting_tools_budget.md); then Lusha `prospecting_contact_search` (1 credit per 25 results; previews show name, title, LinkedIn URL when available — no reveal needed for LinkedIn outreach). Do NOT reveal an email just for LinkedIn.
3. **Write two texts per person** in Amit's voice ("Amit, GrassCrafts, Kolkata"):
   - **Connection note** — max 200 characters (LinkedIn free-plan limit), personal, one line on why them, no link, no prices.
   - **Follow-up message** after they accept — 3–5 short lines: who we are (handwoven Sabai/Kauna/cane/water-hyacinth baskets and hampers from Kolkata, women artisans), one idea for THEIR business (e.g. reusable outer basket for their festive hampers, guest favours, amenity trays), soft ask ("open to a quick look at our trade sample sheet?"), link https://grasscrafts.com/pages/wholesale. NEVER prices, discounts, MOQ, lead times, samples, GST/GI claims, invented clients or numbers. Allowed fact: over 200 women artisans across communities.
4. **Deliver** as Todoist tasks in project "GrassCrafts – owner actions" (id 6hrWjrHwPxWHV4rw), label `linkedin`, due Monday (connection) — one task per person: title "LinkedIn: connect with <Name>, <Title> @ <Company>", description = profile URL (or "search: <Name> <Company>" if no URL), the connection note, and the follow-up message. Priority p3 (p2 if warm).
5. **Log** each person in `outreach/linkedin_manual_log.json` (name, title, company, profile_url, source, date_suggested, status "suggested"). Add a note on the Pipedrive org/lead: "LinkedIn connect suggested to Amit <date>".
6. **Follow-ups:** Amit ticks the Todoist task when sent. The next Monday kit checks completed tasks (Todoist find-completed-tasks, label linkedin): mark them "sent" in the log; if Amit says someone accepted/replied, set status and add the follow-up task; a buyer reply = hot lead → Sristi brief (CC Amit) + Pipedrive deal "Contact Made".

## Lusha free plan — budget (40 credits; check `account_usage` first every time, it is free)
Prices: contact or company search = 1 credit per 25 results; email reveal = 1; phone reveal = 5 (NEVER); lookalikes 1 per 5.
Monthly plan (assume credits reset monthly; verify on the 1st with account_usage and log the balance):
| Use | Credits / month |
|---|---|
| Monday LinkedIn kit: 1 contact search a week | 4 |
| Email reveal for a named buyer at a WARM/HOT lead or an A-fit company with only a generic inbox (max 4 a week) | up to 16 |
| Decision-maker/buying-group search for a hot lead (Sristi asks for a named buyer) | up to 10 |
| Reserve (never spend below 8 left before the 25th) | 10 |
Rules: one search must serve several targets (batch by segment/city); never reveal phones; never reveal for cold, low-fit or B2C contacts; a revealed email counts as verified only if Lusha marks it valid; log every credit spent (date, tool, company, credits, balance) in `reports/agents/lead_research.md`. If balance ≤ 8, stop reveals and only do free steps.
