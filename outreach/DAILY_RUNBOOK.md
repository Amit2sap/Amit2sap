# Daily outreach runbook (run Mon–Fri ~10:00 IST)

Sender: amit2sap@gmail.com (Composio Gmail account `gmail_movie-arab`). Hunter.io account `hunter_coster-alert` (free: 50 searches / 100 verifications per month, resets on the 16th).
State lives in this repo: `outreach/sent_log.json`, `outreach/reserve_prospects.json`, `outreach/decision_makers_*.json`, templates in `outreach/templates.py`, targeting rules in `sales/b2b_targeting_playbook.md`. The Composio workbench resets often; never rely on its files.


## Run lock — one sender at a time (owner rule, 28 Oct 2026)
On 28 Oct two email runs overlapped and 25 companies got the same pitch twice. From now on:
1. **Who sends:** only the scheduled Email & Actions and Reply watcher runs in the main session (session_01CExgX3LnZkdy4AwdW7vCVh) send outreach, follow-ups or replies. Any other session (manual, catch-up, ChatGPT agent) may research and save Gmail DRAFTS only; it never sends unless the owner names that session in that chat.
2. **Lock before sending:** `git pull`, then read `outreach/RUN_LOCK.json`. If `active` is true and `started_utc` is less than 90 minutes old, stop and report "skipped: <job> running". Otherwise write `{"active": true, "job": "<job>", "session": "<id>", "started_utc": "<now>"}`, commit "lock: <job>" and push BEFORE the first send. If the push is rejected, pull and re-check the lock.
3. **Live check per address:** right before each batch, run a Gmail search `in:sent to:<address> newer_than:30d` for every recipient and drop anyone already emailed (sent_log can lag behind Gmail).
4. **Release:** at the end (also on error) set `active` to false, commit "unlock: <job>" and push.

## 0. Skip check
- Saturday/Sunday: do step 1 only (read replies, alert owner on hot leads). No sending.
- Indian public holiday or major festival day: same as weekend. Check with a web search ("public holiday India <date>") and this list (verify dates each year):
  2026: 20 Oct (Dussehra; Kolkata/Bengal closed 17–21 Oct for Durga Puja), 6–11 Nov (Dhanteras–Diwali–Bhai Dooj), 24 Nov (Guru Nanak Jayanti), 25 Dec.
  2027: 1 Jan, 26 Jan, Holi, Eid, Good Friday, 15 Aug, 2 Oct, Diwali week.
- Skip Kolkata/West Bengal prospects during Durga Puja week.

## 1. Read replies (every day, including weekends)
- Gmail search `newer_than:1d -from:me` (or since the last run). Ignore bank, job, newsletter mail.
- Bounces (mailer-daemon "Address not found"): add the address to `do_not_send`.
- "Delivery incomplete" (temporary): ignore unless it turns into a failure.
- Human replies:
  - Interested / asking for prices, samples, MOQ, calls: create an in-thread **reply draft** (do not send) and list it in the owner report. Never quote prices, discounts, lead times or commit to samples without the owner.
  - "Write to X instead": send the pitch to X the same day (plus a one-line note that their team suggested it).
  - "No thanks" / unsubscribe: add to `do_not_send`, no reply needed.
  - Auto-replies / ticket acknowledgements: ignore.

## 1b. HOT LEAD hand-off to Sristi Dey (founder)
A reply is a **HOT LEAD** if the prospect shows buying interest: asks for a price list, quote, MOQ, samples, catalogue details for an order, a call or meeting, or names a quantity, occasion or date.
Within the same run:
1. **Reply to the prospect** in the same thread, **CC sristi@grasscrafts.com**: thank them and say that Sristi Dey, founder of GrassCrafts, is copied and will share the price list / details personally. Mention her WhatsApp +91 62907 44782. No prices from us.
2. **Email Sristi a HOT LEAD BRIEF** (sristi@grasscrafts.com, subject "HOT LEAD BRIEF: <company> — persona, steps & timeline"). Always include these 6 sections (example: the Hamperology brief, 17 Oct):
   1. **Lead details**: organisation, contact name and role, phone/WhatsApp, email, source (which email or campaign, date), subject of the thread.
   2. **Buyer persona**: type of business, size, values, whether this person decides, likely needs and worries (use `sales/b2b_targeting_playbook.md`).
   3. **Buying intention**: what they actually asked for, in their own words; the occasion, quantity and date if known; signal strength (strong / medium); what we want it to become (trial order, repeat seasonal buyer, reseller).
   4. **How to approach**: the angle to lead with, options to offer, what not to promise, questions to ask.
   5. **Steps & timeline**: dated steps. TODAY within 2 h: WhatsApp or call (give a ready-to-send message). Day 1: call. Day 2: price list + MOQ + lead time. Day 3–4: samples. Day 5–7: trial order, with delivery before the occasion. Then the repeat-business plan (next occasions from the calendar).
   6. **What Sristi needs ready**: price list, photos, samples, etc.
   7. **Purchasing background and competitors**:
      - their position in the organisation and their decision power;
      - which vendors or competitors they buy from or stock today, and which products;
      - budget signals (their own retail price points, tender values, order sizes), each with a source, estimates labelled;
      - their buying pattern (occasions and months).
      Use `outreach/competitor_customers.json`, `outreach/leads/*.json` and `sales/lead_intel_*.md`.
   End with: "Reply DONE <step> after each step."
3. **WhatsApp alert to Sristi (+91 62907 44782)** from the API number 8100447884, using the approved `owner_alert` template ({{1}} = company + contact name and role, {{2}} = "HOT LEAD" + what they want + the first action with phone number + "full brief sent to sristi@grasscrafts.com"; no line breaks, under ~600 characters). If the template is not approved yet, skip this step and say so in the report.
4. Mark the lead `"stage": "hot - with Sristi"` in `warm_leads` (sent_log.json). Stop automatic follow-ups to that company; Sristi owns the conversation from here.
5. Put it at the top of the daily report.

**Owner rule (17 Oct): Sristi sends all price lists, quotes and samples herself.** Agents prepare the brief and the timeline, then track her progress. They never send price lists.

## 2. Follow-ups (weekdays)
- First email with no human reply after 5 business days: one short follow-up in the same thread (no attachment), naming the next occasion from the playbook calendar.
- Still nothing 7 days later: a second, final, short follow-up (no sample offer; samples are Sristi's decision). Then stop for good.
- Never follow up on bounced, "no thanks", or auto-closed support-ticket addresses (care@, support@, customercare@): send to the address they pointed to instead, or skip.

## 3. New outreach (weekdays)
- **Volume (owner, 22 Oct 2026):** at most **100 NEW emails a day**, the best 100 available. They must be verified and authentic, so that the Gmail account isn't flagged as spam. Follow-ups count toward the same 100. Replies to people who wrote to us are not capped. Answer them immediately: the hourly Reply watcher (09:07–21:07 IST, scheduled task trig_01Mb2NVBNMF8FgnxKjN9gJg6) replies at 11:07, 15:07 and 19:07 IST (owner, 22 Oct).
- **Who qualifies.** Each new address must meet all of these:
  - published on the company's own website, or found by Hunter with status "valid";
  - not "accept_all" or "unknown" unless the address is on the company's own site;
  - not in `sent` or `do_not_send`;
  - the company has a current buying signal or a clear fit with the segment.
  
  Skip anything uncertain: a smaller, better list beats a full one.
- **Ranking.** Fill the 100 in this order:
  1. today's "new" leads with a named decision-maker;
  2. other "new" leads;
  3. the strongest verified info@ or sales@ addresses in the segment mix.
  
  Never pad the list to reach 100.
- **Daily guard:** before sending, count today's Gmail Sent. Total outbound (new emails plus follow-ups) stays at or below 100. Replies are extra.
- Up to 20 personal emails to named decision-makers (playbook section 1 roles), found via Hunter.io domain search or the company site, verified (Hunter verifier or SMTP RCPT check). One personal email each.
- **Leads first.** Email the `status: "new"` leads in `outreach/leads/*.json`, found by the Lead Research segment agents that morning, before any generic address.
  - Use the personal-email rule for named contacts.
  - After sending, set `status` to `"emailed"` with the date.
- **The rest** go to verified info@/sales@ addresses from web search.
- **Segment mix (owner, 17 Oct):** use the "Mix %" column in `agents/lead_research.md`, adjusted by `agents/STRATEGY.md`. The 11 segments are corporate 18, wedding 14, hotels & resorts 12, diamond jewellery 12, cane planters 9, sustainable décor 8, luxury watches 7, gourmet 7, wellness 5, real estate 4, ethnic wear 4.
- **Template for each segment slug:**

  | Slug | Template |
  |---|---|
  | corporate | "Corporate gifting companies" |
  | wedding | "Wedding & event planners" |
  | hotels | "Hotels & resorts" |
  | diamond_jewellery | "Diamond jewellery boxes & baskets" |
  | cane_planters | "Cane planters (hotels, cafes, designers)" |
  | sustainable_decor | "Sustainable decor brands" |
  | luxury_watches | "Luxury watches" |
  | gourmet | "Festive hamper brands" |
  | wellness | "Spas & wellness" |
  | real_estate | "Real estate developers" |
  | ethnic_wear | "Ethnic wear boutiques" |

- **Occasion line:** add one sentence on the segment's next occasion from `agents/calendar.md` (6–8 weeks out). Example: "ahead of the wedding season" or "for Christmas and New Year client gifting"
- Always: skip anything in `sent` or `do_not_send`; one address per company domain; SMTP-verify; attach the catalogue PDF (re-download from the Sent folder if the workbench reset).

## 4. Save + report
- Append new sends to `sent`, update `log[date]`, `warm_leads`, `do_not_send`; commit and push to `claude/grassctafts-sales-growth-d8azah`.
- Email the owner (amit2sap@gmail.com) a short report: sent today, replies, hot leads with draft links, bounces, anything that needs a decision.

## Daily (every day, including weekends), added 17 Oct
- **AI-visibility check:** run `seo/ai_visibility_check.py` in the workbench, append to `seo/ai_visibility_log.json`, and include the score in the daily report.
- **Replies to media pitches** (`outreach/pr_pitches.json`): flag them to the owner the same day.
- **Replies to review requests** (`outreach/review_requests.json`): thank the customer. If they give permission, save the review to `outreach/reviews_collected.json`. Send any complaints to the owner straight away.

## Google Business Profile (daily, via Zapier), added 17 Oct
- Check for new reviews (Zapier `new_review_v3`, location `locations/7612515921482745833`, account `accounts/113404890366334703365`). Reply to every review within 24 hours and sign it "– Sristi, GrassCrafts".
  - **4–5★:** thank them and mention the product they wrote about.
  - **1–3★:** apologise, offer to fix it, ask them to WhatsApp +91 62907 44782, and alert the owner the same day.
- When a past buyer replies to a review request with praise, thank them and send the Google review link: https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA
- **Weekly (Thursday):** one Google post (`create_post`) linking to a collection: wedding baskets, cane planters, corporate gifts, or a new arrival. Only facts and prices from the catalogue.

## CRM + order forms (owner, 27 Oct 2026) — every reply-watcher and Email & Actions run
1. For every interested reply: create/update in Pipedrive (claude.ai connector) an organisation + person + deal, stage "Contact Made"; label Hot lead for quote/call/sample requests; add a short note with the thread summary. Won orders: mark the deal Won.
2. Jotform order forms (claude.ai connector): list new submissions since the last run on forms 252869411925465, 252893366646471, 252891622774466, 252628825024053. Treat each as a buyer enquiry: brief to sristi@grasscrafts.com (CC amit2sap@gmail.com) and a Pipedrive deal.
3. If Pipedrive or Jotform tools are not available in the session, log it once in reports/agents/handoff.md and continue. Details: agents/TOOLS.md.
4. Pipedrive is the shared lead list (agents/STRATEGY.md, 28 Oct): before emailing any company, search Pipedrive (searchOrganization / searchPersons); skip it if an open Deal exists. Also email open Pipedrive Leads added by the ChatGPT agent or owner that have a published email and no "Emailed" note, then add the note.
5. Sristi loop (owner, 28 Oct): follow agents/sristi_daily.md — the 10:22 run sends Sristi the morning form email (orders to ship = daily unfulfilled-order check, calls due from Pipedrive, hot leads, each with a prefilled "Update this lead" form button); every reply-watcher run captures her form submissions and replies into Pipedrive and creates the next activities.
