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
