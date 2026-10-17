# Daily outreach runbook (run Mon–Fri ~10:00 IST)

Sender: amit2sap@gmail.com (Composio Gmail account `gmail_movie-arab`). Hunter.io account `hunter_coster-alert` (free: 50 searches / 100 verifications per month, resets on the 16th).
State lives in this repo: `outreach/sent_log.json`, `outreach/reserve_prospects.json`, `outreach/decision_makers_*.json`, templates in `outreach/templates.py`, targeting rules in `sales/b2b_targeting_playbook.md`. The Composio workbench resets often; never rely on its files.

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
   End with: "Reply DONE <step> after each step."
3. **WhatsApp alert to Sristi (+91 62907 44782)** from the API number 8100447884, using the approved `owner_alert` template ({{1}} = company + contact name and role, {{2}} = "HOT LEAD" + what they want + the first action with phone number + "full brief sent to sristi@grasscrafts.com"; no line breaks, under ~600 characters). If the template is not approved yet, skip this step and say so in the report.
4. Mark the lead `"stage": "hot - with Sristi"` in `warm_leads` (sent_log.json). Stop automatic follow-ups to that company; Sristi owns the conversation from here.
5. Put it at the top of the daily report.

## 2. Follow-ups (weekdays)
- First email with no human reply after 5 business days: one short follow-up in the same thread (no attachment), naming the next occasion from the playbook calendar.
- Still nothing 7 days later: a second, final follow-up offering 2–3 samples. Then stop for good.
- Never follow up on bounced, "no thanks", or auto-closed support-ticket addresses (care@, support@, customercare@): send to the address they pointed to instead, or skip.

## 3. New outreach (weekdays)
- 150 per day total from the personal Gmail (do not exceed ~200).
- Up to 20 personal emails to named decision-makers (playbook section 1 roles), found via Hunter.io domain search or the company site, verified (Hunter verifier or SMTP RCPT check). One personal email each.
- The rest go to verified info@/sales@ addresses from web search, mixed per the playbook: ~30% corporate gifting firms, 25% food/sweets/tea/D2C gift brands, 15% hotels/resorts, 15% wedding planners, 15% jewellers/decor stores.
- Always: skip anything in `sent` or `do_not_send`; one address per company domain; SMTP-verify; attach the catalogue PDF (re-download from the Sent folder if the workbench reset).

## 4. Save + report
- Append new sends to `sent`, update `log[date]`, `warm_leads`, `do_not_send`; commit and push to `claude/grassctafts-sales-growth-d8azah`.
- Email the owner (amit2sap@gmail.com) a short report: sent today, replies, hot leads with draft links, bounces, anything that needs a decision.

## Daily (every day, including weekends), added 17 Oct
- **AI-visibility check:** run `seo/ai_visibility_check.py` in the workbench, append to `seo/ai_visibility_log.json`, and include the score in the daily report.
- **Replies to media pitches** (`outreach/pr_pitches.json`): flag them to the owner the same day.
- **Replies to review requests** (`outreach/review_requests.json`): thank the customer. If they give permission, save the review to `outreach/reviews_collected.json`. Send any complaints to the owner straight away.
