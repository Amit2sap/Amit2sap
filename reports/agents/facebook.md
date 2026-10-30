# facebook agent log

## 2026-10-21 (Wed, off day)
- Read Page feed via Composio (no token printed). Only posts in the 7-day window: the 14 Oct Live (70 comments) and one 14 Oct post (0 comments). Newer posts: none.
- Live comments are live chat from 7 days ago (host answered live); not replied to publicly. No hot leads (no price list, bulk or sample requests). Items for owner: "Mera sofa dispatch hua kya?" (order status), "Table mats available hai kya??" and "red wala wall hanging price" (could be answered from Shopify if wanted).
- No posts (off day). No new blocker.

## 2026-10-20 (Tue, posting day)
- Posted 1 native photo post (Diwali table dressing): Madurkathi table runner and 6 mats set, handle madurkathi-table-runner-6-mats-set, from Rs 450. Post id 142803116227246_1675586341245413. No Live today, so no teaser or roundup.
- Comments: read 25 of 70 on the 14 Oct Live via the feed (FACEBOOK_GET_COMMENTS refused: needs pages_read_engagement / pages_read_user_content). Replies via FACEBOOK_CREATE_COMMENT on the comment ids also failed (tool read the id as a page id; numeric id refused with a 400). No replies sent; not worked around.
- Unanswered, could be answered from Shopify by the owner: "Table mats available hai kya??" (yes, from Rs 300 / Rs 450 sets), "cane storage dam" (cane storage basket Rs 1,099), "red wall hanging price", "Mera sofa dispatch hua kya?" (order status, owner). No hot leads (no price list, bulk or sample asks).
- BLOCKER (new, owner): Facebook connection lacks permission to read/reply to Page comments (needs pages_read_engagement and pages_manage_engagement, or Page Public Content Access).

## 2026-10-22 (Thu, posting day)
- Posted 1 native photo post (Diwali 8 Nov / Bhai Dooj 11 Nov gifting): Water Hyacinth Open Caddy, handle water-hyacinth-open-caddy-handwoven-artisan-storage, Rs 1,799. Post id 142803116227246_1675787184558662. Different product from 20 Oct.
- Comments: tried FACEBOOK_GET_COMMENTS once, refused (#10 pages_read_engagement / Page Public Content Access). Skipped, no replies. Known blocker, unchanged.
- No hot leads. No new blocker.

## 2026-10-23 (Fri, off day)
- Read posts of the last 7 days via FACEBOOK_GET_PAGE_POSTS with comment counts: 3 posts, 0 comments on each, so nothing to answer (FACEBOOK_GET_COMMENTS not needed). Note: a post dated 2026-10-23 11:46 UTC (id 142803116227246_1677004184436962) exists that this agent did not make. No post by Social (off day). No hot leads.

## 2026-10-24 (Sat, posting day)
- Comments: 7-day posts have 0 comments (Live posts of 7/12/14 Oct are older; not read). No replies.
- Posted 1 native photo post: Sabai Pot-Shaped Box with Lid (handle box-1, from Rs 1,199). Post id 142803116227246_1677887837681930. No hot leads.

## 2026-10-25 (Sun, off day)
- Comments: live video post 142803116227246_1429292278642198 (24 Oct) has 52 comments, mostly greetings/price asks. Replied to 8 (thanks, festive wish, no prices; price/design asks pointed to grasscrafts.com and WhatsApp +91 62907 44782). Other posts 0 comments. Note FACEBOOK_CREATE_COMMENT needs the numeric comment id only (compound id is read as a page id). Remaining ~44 comments (greetings, size feedback) left for next run.

## 2026-10-29 (owner-requested posting run)
- Posted 1 native photo post: Handwoven Bamboo Gift Basket (handle handwoven-bamboo-gift-basket-black, Rs 680). Post id 142803116227246_1683305083806872.
- Comments: replied to 1 real question ("Price of makhana?" on the 24 Oct Live, comment 1850436836167201: from Rs 199 for the 100 g pack, website and WhatsApp). Left unanswered: natural jute/floor mat asks and "lamps on verandah?" on post 142803116227246_2602283660197160 (77 comments; not read fully). No hot leads.

## 2026-10-29 (Thu, social run, USAGE SAVER)
- No post (usage saver). FACEBOOK_GET_COMMENTS refused again (#10 pages_read_user_content / Page Public Content Access), so full threads not readable (blocker unchanged). Used the 5 comments embedded in FACEBOOK_GET_PAGE_POSTS for the 28 Oct Live post (77 comments) and replied to 3 (natural jute mat, natural floor mat, lamps on verandah): pointed to grasscrafts.com / WhatsApp +91 62907 44782, no claims or prices. ~70 comments there still unread. No hot leads.

## 2026-10-29 (owner-approved catch-up, main session)
- After the owner reconnected Facebook (facebook_unroll-miller), read all 131 comments on the 28 Oct (77) and 24 Oct (54) Lives. Replied to 40 buying questions (price/pp → website + WhatsApp, booking, COD, payment mode, shipping, sizes/colours/mats/boxes → WhatsApp Sristi, makhana pack sizes, handmade). Greetings/compliments/tag spam skipped. No prices quoted. Method saved in agents/facebook.md.
- Correction 29 Oct (owner): 2 makhana replies (24 Oct Live) listed "250 g, 500 g, 1 kg and 5 kg packs, all free shipping" and linked the collection. Edited in place to the live facts: 100/250/500 g/1 kg packs + separate 5 kg bulk; free shipping on 250 g and above; 100 g at standard rates; product-page link. Fact-check rule added to agents/README.md and agents/facebook.md.

## 2026-10-30 (Fri, USAGE SAVER)
- No post (usage saver). Read 9 posts from the last 7 days via GET_PAGE_POSTS: unanswered top-level comments on the 28 Oct and 24 Oct Lives were only greetings, compliments, tags and spam (no buying questions), so no replies. No hot leads.
