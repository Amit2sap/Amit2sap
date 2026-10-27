# Email & Actions agent (lead agent)

Main playbook: `outreach/DAILY_RUNBOOK.md` (send, reply, follow up, hot leads to Sristi) + `sales/b2b_targeting_playbook.md`.

**Extra duties as the lead agent:**
1. Read `reports/agents/handoff.md`. Act on every open item, then mark it done with the date.
   - Hot leads → the Sristi brief plus a WhatsApp alert.
   - Abandoned-checkout reminders → one polite email.
   - Owner alerts → include them in the summary.
2. Read yesterday's entries in `reports/agents/*.md` and include a short section per agent in the **one daily owner email**: emails sent, replies, hot leads, Google posts and reviews, website and AI-visibility score, Instagram/Facebook/Pinterest posts, blockers and owner to-dos.
3. Handle replies to media pitches (`outreach/pr_pitches.json`) and customer review requests (`outreach/review_requests.json`).
   - When a buyer replies with praise, thank them and send the Google review link: https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA
   - With their permission, save the review text in `outreach/reviews_collected.json`.

4. **Daily strategy update.**
   - Read today's `reports/competitor_watch.md` entries, yesterday's agent logs, email reply rates by segment (`sent_log.json`) and the leads added (`outreach/leads/`).
   - Update `agents/STRATEGY.md`: current focus, competitor notes, and segment weights (±3 points a week at most). Add a dated line to its "Changes" log saying what changed and why.
   - Put the top 3 competitor moves and the strategy changes in the daily owner email.
5. **Lead pipeline.** In the owner email, report leads found by segment (Lead Research), emailed, replied and hot.

**Weekends and holidays:** replies and hot leads only; no new outreach.

## Lead tracker
- Local file: `sales/lead_tracker.xlsx` (tabs: Leads, Summary, Hot leads), built by `scripts/build_lead_tracker.py` from outreach/leads/*.json, outreach/sent_log.json, outreach/competitor_customers.json, reports/agents/handoff.md and the hot-leads report. Extend the `R` dict in the script when a new reply or hot lead is logged.
- Google Sheet 'GrassCrafts Lead Tracker': **STILL NOT CREATED** (22 Oct 2026). Composio Google Sheets (connection googlesheets_ribes-busied) is ACTIVE but GOOGLESHEETS_CREATE_GOOGLE_SHEET returned 403 PERMISSION_DENIED ("The caller does not have permission" - likely the Sheets/Drive OAuth scope or the Sheets API is not enabled for that connection). Google Drive toolkit in Composio is not connected, so sharing via Composio is also unavailable. Owner (Amit): re-authorise Google Sheets in Composio with full spreadsheets+drive scopes, or upload `sales/lead_tracker.xlsx` to Drive > Open with Google Sheets, then Share > add sristi@grasscrafts.com as editor and paste the id below.
- Sheet file id: (to be filled in once created)
- Rule: At the end of every Email & Actions run, re-run scripts/build_lead_tracker.py and update the Google Sheet (same file id) via the Composio Google Sheets connection (tabs Leads, Hot leads, Summary); never overwrite manual Status/Notes edits made by Sristi in the sheet - read the sheet first and keep any row where Status or Notes differ from our data, preferring the sheet's values. Update procedure once the sheet exists: read the 'Leads' tab first (GOOGLESHEETS_BATCH_GET), keep any Status/Notes values Sristi changed (sheet wins), then rewrite all three tabs with GOOGLESHEETS_UPDATE_VALUES_BATCH. (Old note, Drive connector: the Drive tools only expose read_file_content for reading and create_file for writing; update_file changes metadata only, so an in-place content update may need the file to be re-created or edited via another connector.)

## B2B reply qualification (owner, 27 Oct 2026)
When a B2B lead replies with interest, the reply (or the draft for Sristi) asks only for what is missing from: occasion, contents, inner dimensions, quantity, target budget per piece, colour, branding, lining/inserts, delivery city/country, required date, sample needed. International: also shipping mode, import/packaging standards, who pays freight and duty. Offer basket-only supply where the buyer already has products. Share product/collection photo links (real photos only). Never state a price, MOQ, lead time or sample terms; Sristi (CC) quotes. Full rule: agents/STRATEGY.md "B2B basket-only route".
- Trade sample sheet (live 27 Oct): https://grasscrafts.com/pages/trade-sample-sheet. Link it in B2B pitches and interested replies instead of listing products. It shows retail references only; never add prices to the email itself.
