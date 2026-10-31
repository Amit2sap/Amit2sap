# Daily actions page: comment kit, Pinterest saves, collab pitches (owner, 22 Oct 2026)

**Growth playbook from 4 Nov (owner, 31 Oct):** the kit also lists up to 3 micro-creator collab drafts a week and Instagram Collab-post proposals for hamper brands that replied with interest, plus any reel the Instagram tool cannot publish (clip + caption for the owner). All need owner approval. See `agents/growth_playbook.md`.

**Page:** https://claude.ai/artifact/T8hhYdcLaL545XpKfCCoZF. It is private to the owner; Amit can share it with Sristi from the page's Share menu.
Agents write to the page's database with the ArtifactData tool (load it with ToolSearch). Pass `url` = the page above and `collection` = "items". The page shows the latest `date` first.

**Usage rule (owner, 29 Oct 2026):** build the next kit ONLY on posting days ((today - 2026-10-18).days even). On off days the Social run only executes approved saves and replies to comments. Recent kits often had 0 verifiable comment items, so do not spend searches padding them: if no dated post with a real URL is found in 3 searches, write 0 comment items and move on.

## Item schema (one document per action)
`doc_id` = `<YYYY-MM-DD>-<kind>-<n>`, for example `2026-10-23-comment-01`.

| Field | Meaning |
|---|---|
| date | "YYYY-MM-DD" in IST |
| kind | "comment", "save" or "collab" |
| order | 1..n |
| status | "pending" when created. The owner sets done/skipped (comments) or approved/skipped (saves, collabs). Agents set "executed" after acting. |
| platform | "linkedin", "instagram", "pinterest" or "email" |
| author | the person or account who made the post |
| context | short note, for example "HR Head, Infosys · 3k likes" |
| url | the exact public post, pin or profile URL (https) |
| excerpt | 1–2 lines of the post |
| comment | comment kind only: the exact text to paste |
| board | save kind only: our Pinterest board to save to |
| subject, body, to_email | collab kind only: the pitch email |
| executed_at, result | written by the agent after acting |

## Social agent: every day (part of the Social run)
1. **Execute what the owner approved.** Query items where kind=="save" and status=="approved". For each, save that pin to the named board (Composio Pinterest, pinterest_whosen-hoose), then update status="executed" with `executed_at` and `result`. Pin the write with `if_version`.
2. **Build tomorrow's kit,** dated the next day in IST:
   - **8–10 comments** spread across LinkedIn (corporate gifting, HR, admin, procurement, hospitality and sustainability leaders in India), Instagram (wedding planners, decor creators, eco brands) and Pinterest (popular pins in our categories).
   - **Post rules:** only public posts from the last 7 days, found by web search, with a working URL. Skip any post or author already in items in the last 14 days. Never pick competitors' own posts.
   - **Comment rules:** 1–3 sentences, specific to that post, adding real insight from GrassCrafts' world (materials, craft, gifting practice), in a warm expert voice. No link, no price, no "DM us", no hashtags, no emojis on LinkedIn, at most 1 emoji on Instagram. Never claim anything we can't verify.
   - **3–5 Pinterest saves:** pins from other creators (not competitors) that fit our boards, each with `board` set.
   - **2–3 collab pitches** to wedding planners, decor creators and gifting pages: a verified business email only (published on their own site or Hunter "valid"), not in sent_log or do_not_send. Each needs a short personal subject and body proposing a feature or collab. No prices, samples or free-product promises; offers of products or payment are the owner's decision.
   - Write everything with one ArtifactData batch call (no if_version needed for new docs).
3. Put the page link and the count in the daily summary line.

## Email agent: every run
Query items where kind=="collab" and status=="approved". Send each from Gmail within the daily 100 cap, after checking sent_log, then set status="executed" with `executed_at` and `result`, and log it in outreach/sent_log.json.

**How to find collab targets when site fetch is blocked (23 Oct):** run the search and the check inside the Composio workbench (COMPOSIO_REMOTE_WORKBENCH): `web_search()` for "<segment> <city> email address", keep business-domain emails only (no gmail/yahoo), drop any domain in outreach/sent_log.json or outreach/leads/, then `requests.get` the site's home, /contact, /contact-us and /pages/contact pages and keep the email ONLY if it appears on the company's own page (store that page as url). Pinterest saves need a global pin search; Composio's Pinterest search covers only our own pins, so skip saves unless the owner pastes pin links.

**Bounce check (24 Oct):** 4 of 9 collab emails bounced even though each address was published on the company's site (weandyoudecor, earthheart, mattergifts, inchingindia). From now on also run Hunter email-verifier on every collab address before adding it; skip any that are not "valid" or "accept_all", and note the Hunter result in the item's context.


## Master directives
- Master directive (confirmed 2026-10-31): D16 (put linkedin_lesson_post.md on the next posting-day kit for owner approval), D29 (log items met).
