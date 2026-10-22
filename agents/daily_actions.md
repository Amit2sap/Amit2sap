# Daily actions page: comment kit, Pinterest saves, collab pitches (owner, 22 Oct 2026)

**Page:** https://claude.ai/artifact/T8hhYdcLaL545XpKfCCoZF. It is private to the owner; Amit can share it with Sristi from the page's Share menu.
Agents write to the page's database with the ArtifactData tool (load it with ToolSearch). Pass `url` = the page above and `collection` = "items". The page shows the latest `date` first.

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
