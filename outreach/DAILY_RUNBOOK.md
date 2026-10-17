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
