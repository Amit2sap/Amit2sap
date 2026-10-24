# google_business agent log

## 2026-10-17 (set-up, main session)
- Posts created: wedding baskets, cane planters, corporate gifts. 7 review replies. Listing renamed to GrassCrafts by Abalone (pending Google review). Duplicate Makhana record deleted.
- 17 Oct (main session): corporate gifts post localPosts/7715750396808583857 → /collections/corporate-gifts-handcrafted-gifts.
- 18 Oct (main session):
  - Main listing: 12 specific services replace the single vague one.
  - Makhana listing: description rewritten (unverified "GI-tagged" removed) and 4 services added.
  - Keyword report Jul–Sep: abalone 167, flower vase 44, table runner 21; no product or material keywords. Strategy added to agents/google_business.md.
  - Google suggests a 2nd phone, 062915 14742: owner to accept or reject.

## 2026-10-18 (daily run, scheduled agent; posting day 0, Sunday)
- **Reviews:** main listing 21 reviews, avg 4.7, all 21 already have replies → 0 new replies. Makhana listing 1 review (5★), API returns totals only, no review body → nothing to reply to. No 1–3★ reviews → no owner alert.
- **Pending edits:** main listing title "GrassCrafts by Abalone" is live, no `hasPendingEdits`/`hasGoogleUpdated`; categories Handicraft + Corporate gift supplier, Gift basket shop, Handicraft Exporter; description has no URLs/phone. Makhana listing `hasPendingEdits: true` (the 18 Oct description rewrite is still under Google review); no `hasGoogleUpdated`.
- **Posts (theme: Diwali 8 Nov, within 21 days):**
  - Main: localPosts/2740850834105275854, "Handwoven Kauna grass Diwali gift hamper basket, Kolkata – from ₹340", SHOP → /products/kauna-grass-gift-hamper-basket (₹340 / ₹599 variants, Shopify featured image).
  - Makhana (first posting day of the week Mon 12–Sun 18): localPosts/7834306535527080087, "Makhana gift hamper for Diwali – plain Mithila makhana, Kolkata", 250 g ₹499 / 500 g ₹849 / 1 kg ₹1,599, SHOP → /collections/makhana. No GI claim.
- **Competitor watch:** 4 bullets in reports/competitor_watch.md. No Maps/Places tool, so competitor ratings/review counts not available (web snippets only).
- **Handoff:** flagged misleading old Makhana post ("Navratri Special Menu", restaurant-style) and placeholder/"fair-trade certified" text in older main posts for owner OK to delete/edit; weekly owner reminders repeated.
- **Blockers:** none for GBP (Zapier GET/POST and create_post worked). Next: Mon 19 Oct performance pull + website reviews refresh; next main post 20 Oct (Sabai item, Dussehra/Diwali).

## 2026-10-21 (daily run, scheduled agent; off day, Wednesday)
- **Blocker:** Zapier returned "Task limits for this account have been reached." on both review GETs (main and Makhana). Nothing could be read or written, so no review replies, no pending-edit check, and no check on whether the 20 Oct posts went live or were rejected. No workaround attempted.
- Not done: reviews on both listings, pending edits, post status. No posts due (off day), no Monday tasks.
- Still open from 18 Oct: delete old posts 2927915436701370500 and 2277602207260524481; repost Makhana Diwali post without WhatsApp number.
- No review data seen, so no 1-3 star alert from this run.

## 2026-10-20 (daily run, posting day 1, Tuesday)
- **Reviews / pending edits:** BLOCKED. Zapier returned "Task limits for this account have been reached" on both review GETs (and so no location GET). No review replies and no pending-edit check today. Windsor was used only for creating the post, as instructed.
- **Main post (Diwali 8 Nov, within 21 days):** localPosts/940114025326787285 (state PROCESSING via Windsor create_local_post). "Handwoven Sabai grass gift box, Kolkata - Rs 750", SHOP -> /products/storage-box, Shopify featured image. No phone number in text.
- **Makhana post:** NOT posted. Windsor google_my_business exposes only the main location (7612515921482745833), and Zapier is limit-blocked. The 18 Oct rejected Makhana post (7834306535527080087) is not yet replaced.
- **Not Monday:** no performance pull or competitor watch.
- **Blockers:** Zapier task limit (reviews, Makhana post, 2 old posts still to delete); Windsor has no Makhana location.

## 2026-10-22 (daily run, posting day 2, Thursday)
- **Reviews / pending edits:** BLOCKED. One Zapier review GET for the main listing still returned "Task limits for this account have been reached." Skipped reviews and pending edits, no retries. Not Monday: no performance pull.
- **Main post (Bhai Dooj 11 Nov, Diwali 8 Nov, within 21 days):** localPosts/4099381715667300718 (PROCESSING via Windsor create_local_post). "Sabai grass pot-shaped gift box with lid, Kolkata - from Rs 1,199", pink/blue/green, 8x8 in and 10 in, SHOP -> /products/box-1, Shopify CDN featured image. No phone number, no trade terms. Different product from the 20 Oct post (storage-box).
- **Makhana:** skipped (not connected in Windsor; had its weekly turn).
- **Blockers (unchanged, no new owner alert):** Zapier task limit since 18 Oct; Windsor has only the main location. Review replies, post status check and old-post deletions still pending.

## 2026-10-24 (posts via Composio Upload-Post, account upload_post_halide-drawly)
- Main (Diwali 8 Nov / Bhai Dooj): localPosts/8460222548547168693, handmade dry flower wreath, link /products/dry-flower-wreath, Shopify CDN photo uploaded as s3key. No prices, no phone.
- Makhana: localPosts/2026296411966267435, premium Mithila makhana gifting/bulk, link /collections/makhana, product photo. No GI claim.
- Both completed; Upload-Post usage 3/10 (limit resets daily from 23 Oct 12:39 UTC). Reviews/pending-edit checks not done this run (not in scope).
