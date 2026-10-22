# website agent log

## 2026-10-21 (Wed, off day)
- Funnel, last 24h (Shopify): 54 sessions, 0 add-to-cart, 0 checkout reached, 0 orders (0.0%). No cart additions at all is unusual, so worth a check that Add to cart works (not verified here).
- Abandoned checkouts since 20 Oct: 0. No reminders for handoff.
- Unfulfilled open orders: 0.
- Content/SEO changes: none applied. seo/website_backlog.md does not exist and no owner-notice proposals are logged, so no 48h window has passed. No backups or changelog needed.
- Blockers: none from Shopify. Blog Engine and AI-visibility check not run (off day / not in scope).

## 20 Oct: Website & Search daily run
- Funnel (last 24h): 64 sessions, 1 with add-to-cart, 0 reached checkout, 0 orders.
- Abandoned checkouts: 0 in 24h (latest 16 Oct, ₹340). No reminders.
- Unfulfilled over 5 days: #1037 (19 May) and #1001 (Feb 2025), both paid; owner alert in handoff.
- Blog Engine: published "Haldi and Mehendi Basket Decoration Ideas" (topic ticked). Live check passed. Collection Guides line deferred (needs 48h notice). Handed to social.
- AI-visibility check skipped (AI Search agent owns it). No change proposal or theme work today. Blockers: none.
- 2026-10-22: Blog featured images + alt text added to 4 new articles (Diwali corporate gifts, material comparison, madur mat guide, wedding return gifts); 1 body image inserted in Haldi/Mehendi article; bulk-hamper guide already OK. All 200 live. See seo/CHANGELOG-2026-10-22-blog-images.md

## 2026-10-22 (Thu, posting day): daily run
- Funnel, last 24h: 47 sessions, 0 add-to-cart, 0 reached checkout, 0 orders. Third day of near-zero cart additions; flagged to owner in handoff.
- Abandoned checkouts, last 24h: 0 (latest 16 Oct). No reminders.
- Unfulfilled open, not-cancelled orders: 0 (#1001, #1037 not flagged).
- Blog Engine: published "Sabai Grass Products: A Buyer's Guide to Uses, Prices and Care (2026)", https://grasscrafts.com/blogs/news-the-grass-guide/sabai-grass-products-buyers-guide-india . Live 200, FAQPage present, 12 product links all ACTIVE and 200. Featured + body image are real active-product photos, alt text 13 words each. Topic ticked, handed to social.
- New image rule added to agents/website.md (Blog Engine, Images).
- Not done: collection Guides line (needs 48h notice), sitemap resubmit/URL inspection (no tool), AI-visibility check (AI Search agent owns it). Blockers: none.
- Changelog: seo/CHANGELOG-2026-10-22-website.md, seo/CHANGELOG-blog.md.

## 2026-10-22 (backlinks task from owner)
- Built `seo/backlinks_plan_2026-10-22.md` (45 verified opportunities) and `seo/backlinks_owner_checklist.md` (ordered, with copy-paste text). URLs checked through the Composio workbench; bot-blocked sites are marked.
- Outreach: Gmail Sent already showed 224 messages dated 22 Oct (UTC), above the owner's "well under 200" limit, so **no pitch was sent**. 7 personal pitches (Suspire, Upcycleluxe, Tapwell, Box n Bond, AIACA, Souvenirs of India, Taalapatra) are saved as Gmail drafts, not logged as sent. Logged in `seo/citation_targets.json` as draft_ready_not_sent. Send on 23 Oct.
- Blocker: outbound curl is blocked in this sandbox (403 from proxy); used the Composio workbench for URL checks.

## 2026-10-22 (owner-approved landing content)
- Maker-direct landing content on 4 collections: diamond-jewellery-boxes (from ₹450, 8-row sizes table, jewellers section), diwali-gift-hampers (from ₹200, 8 rows), wedding-gift-hamper (from ₹340, 2 rows; other baskets have no verified sizes), corporate-gifts-handcrafted-gifts (from ₹199, 8 rows). New SEO titles/metas, 5 FAQs + FAQPage JSON-LD each, links to blog guides, wholesale page and each other. Backup: backups/collections/landing_before_2026-10-22.json. Changelog + undo: seo/CHANGELOG-2026-10-22-landing.md.
- Live 200 check not possible today (proxy 403, Composio sandbox down); Admin API read-back confirms content. Re-check next run. Remove DIWALI10 line after 12 Nov.
