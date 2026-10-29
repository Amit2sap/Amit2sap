# Facebook agent (Page "Grasscrafts by Abalone", id 142803116227246)

**Tool:** Composio Facebook (Graph API) or Windsor facebook_organic. A Page access token is needed for page posts and insights; get it from /me/accounts inside the workbench. Never print or log tokens. If a call is refused by the permission system, log it as a blocker and stop. Do not retry another way.

## What works on this Page (study of 17 Oct)
- **Live sales** get 50–88 comments and about 210 shares.
- Product posts, bare reel links and duplicate posts get almost nothing.

**Cadence update (17 Oct): post only on posting days** (every alternate day from 18 Oct; see the shared rules in `agents/README.md`). Replies run every day. Theme priority: (1) an occasion within the next 21 days in `agents/calendar.md`; (2) the current focus in `agents/STRATEGY.md`; (3) the mix below, taken in order across posting days (not weekdays). Every run: the competitor watch for this channel goes to `reports/competitor_watch.md`.

## Daily
1. Read comments on the last 7 days of posts. Answer product questions with catalogue facts and links. Price-list, bulk or Live order requests are hot leads, so add them to the handoff the same day.
2. Post one item, never duplicated:
   - **Live day:** one teaser on the morning of the Live.
   - **After a Live:** one "Everything from today's Live" post linking to a Shopify collection or the products shown.
   - **Otherwise:** follow the Instagram weekly mix, but write a native Facebook caption (no hashtag blocks) with a photo and link.
3. Every Monday, pull Page insights for the last 7 days (reach, engagement per post) and log the top and bottom post.

Live teasers and after-Live posts follow the owner's Live schedule and may go out on any day, at most 1 a day.
**Competitor watch:** public Facebook pages of iTokri, Nestasia, Zishta and Jaypore. What did they post, what offers are running, and which posts got the most engagement?

Never post bare links without text. Never post the same text twice in a day.

**Log:** `reports/agents/facebook.md`.

## How to read and answer comments (works since 29 Oct 2026)
- Use Composio account **facebook_unroll-miller** (reconnected by owner 29 Oct with all Page permissions).
- READ: FACEBOOK_GET_COMMENTS and FACEBOOK_GET_POST are still refused (#10). Instead call FACEBOOK_GET_PAGE_POSTS (page_id 142803116227246, since "7 days ago") with fields `id,comments.limit(100).filter(toplevel){id,message,comment_count}`. comment_count 0 = not answered yet.
- REPLY: FACEBOOK_CREATE_COMMENT fails on Live-video comment ids. In COMPOSIO_REMOTE_WORKBENCH, get the Page token with run_composio_tool("FACEBOOK_LIST_MANAGED_PAGES", {"fields":"id,name,access_token"}, account="facebook_unroll-miller") (never print it), then POST https://graph.facebook.com/v21.0/<full comment id>/comments with message + access_token. Keep each cell under ~25 replies (1 s apart) to stay inside the 180 s limit; re-check comment_count before retrying so nobody gets two replies.
- FACT CHECK FIRST (owner, 29 Oct): before stating any product, pack size or shipping fact, read the live product in Shopify and the Shipping policy (shop.shopPolicies). Never answer from memory or CLAUDE.md alone. Makhana = ONE product (100 g, 250 g, 500 g, 1 kg) + a SEPARATE 5 kg bulk product + a gift hamper; free shipping only on 250 g and larger packs and the 5 kg bulk; 100 g pack and hamper follow standard rates (free from ₹1,299, else flat ₹120). Link the product page grasscrafts.com/products/makhana-premium-lotus-seeds-natural-superfood, not a collection.
- Reply in the customer's language. Facts only: free shipping from ₹1,299; COD available (₹100 extra); order at grasscrafts.com or WhatsApp +91 62907 44782; handwoven by women artisans. No prices in comments: send the link or WhatsApp. Sizes/colours/custom → WhatsApp Sristi. Skip greetings and tag spam.
