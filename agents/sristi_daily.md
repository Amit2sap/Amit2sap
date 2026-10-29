# Sristi's daily lead form email + capture loop (owner, 28 Oct 2026)

Sristi is busy: she never writes emails. She taps a form. Claude captures her answers and prepares the next day.

## The form
Jotform "GrassCrafts – Sristi lead update": https://form.jotform.com/263003605636047 (form id 263003605636047).
Fields: Lead, Lead ID (both prefilled from the link), What happened? (choice), Where did this lead come from? (WhatsApp/Facebook/Instagram ad; Email from GrassCrafts; Website or Google; Repeat customer/referral; Exhibition or walk-in; Not sure — added 28 Oct to measure the Meta ad), Next step (choice), Next date, Quantity/requirement, Order value ₹, Notes.
Prefilled link per lead: https://form.jotform.com/263003605636047?lead=<URL-encoded company>&leadId=<Pipedrive deal or lead id>
(If the prefill keys do not fill, open the form in the Jotform builder once and set the field "unique names" to lead and leadId.)

## A. Morning email to Sristi (sent by the 10:22 Email & Actions run, every day incl. weekends; also right after the owner pastes ChatGPT data)
To sristi@grasscrafts.com, CC amit2sap@gmail.com. Subject: "Today's leads – <date> – <N> to act on". HTML email, mobile friendly, no long text. Sections:
1. **Orders to ship** (daily unfulfilled-order check, Shopify: orders unfulfilled, not cancelled, not test, last 30 days; plus won B2B orders with a due date from outreach/won_orders.json and Pipedrive Won deals): order, customer, items, due date, days waiting. Flag anything older than 3 days in red.
2. **Today's calls / follow-ups** from Pipedrive activities due today or overdue, sorted P1 → P3.
3. **New hot leads** (replies, form enquiries, ChatGPT leads pasted by the owner).
Each lead is one card:
   - Company · priority (P1/P2/P3) · current status · WhatsApp/phone as a tap link (https://wa.me/91XXXXXXXXXX) · email
   - One-line description and requirement (what they buy, quantity if known, occasion, date)
   - Questions with ready options (what the form asks): What happened? / Next step / Next date
   - A big button "Update this lead" = the prefilled form link above
   - RULE (owner, 29 Oct): EVERY lead card in EVERY section (orders, call retries, new leads, older leads, call-only leads) gets its own "Update this lead" button. No lead is ever listed without one. If a lead has no Pipedrive id, use a lowercase slug of its name as leadId.
4. Footer: "Tap a button, pick an option, Save. No email reply needed." Also accept short email replies like "1 won, 2 call Friday" if she replies instead.
Never put prices, MOQ or lead times in this email unless Sristi herself gave them.

## B. Capture (reply watcher 19:07, and the 10:22 run)
- List new submissions of form 263003605636047 since the last run (Jotform list_submissions / analyze_submissions).
- Also read Sristi's email replies to the morning email.
- For each answer: update Pipedrive (stage per status: interested/catalogue -> Contact Made; quote -> Proposal Made; sample -> Demo Scheduled; won -> Won with value; not interested -> Lost "not interested now"; wrong contact -> Lost "wrong contact" + lead research task), add a note with her words, and create the next activity on Next date with Next step as subject.
- Add a dated line to reports/agents/sristi_log.md.

## C. Next day's tasks
The next morning email is built from Pipedrive activities due (B creates them), so Sristi's ticks today become tomorrow's list automatically. Unanswered leads roll over with "(no update yesterday)".
- Capture the "Where did this lead come from?" answer into the Pipedrive deal note and count ad-sourced leads/orders weekly for the Meta Ads cost-per-order line in the Monday report.
