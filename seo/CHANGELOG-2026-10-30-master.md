# Master agent changes, 30 Oct 2026 (owner: "complete the action items as soon as possible")
Backups: backups/2026-10-30/.

1. **/pages/wholesale-corporate-gifting** (Page gid 166751240365), live 2026-10-30T11:37:46Z (Admin API pageUpdate, no userErrors).
   - Opening paragraph: "woven by artisan communities across India, mainly in West Bengal" → "More than 200 women artisans weave for us in community groups across India: each community works with the material that grows near it, with skills passed down from one generation to the next. Madurkathi is a GI-registered craft (GI no. 567)." Added "dining sets" to the product list. (Facts: marketing/story_bank.md, owner 29 Oct.)
   - Product grid: added "Madurkathi dining sets" tile → /products/nilachal-madurkathi-dining-set (real product photo). Reason: the October bulk order from a ChatGPT buyer was 12 of these sets; 27 of 97 ChatGPT visits land on this page.
   - Unchanged: quote link above the fold, WhatsApp link, trade sample sheet link, client list (owner-confirmed, outreach/REVIEW_KIT.md), FAQ, enquiry form, FAQPage JSON-LD.
   - Undo: pageUpdate with the two blocks in backups/2026-10-30/wholesale_page_body_before.html.
2. **/products/wedding-gift-hamper-basket-2** SEO (Product gid 8146425249965). Reason: "basket for wedding gift" pos 2.4, "basket for wedding" pos 2.8 and similar ≈230 impressions, 0 clicks (GSC 2-29 Oct).
   - Title: "Wedding Gift Hamper Basket, Handwoven Straw | GrassCrafts" → "Basket for Wedding Gift – Handwoven Straw Hamper ₹1,050 | GrassCrafts"
   - Description → "Handwoven straw hamper basket for wedding gifts, Haldi, trousseau and return gifts – ₹1,050, reusable after the wedding. Bulk orders for wedding planners. Free shipping from ₹1,299, no GST."
   - Price ₹1,050 from Shopify variant. Undo: old values in backups/2026-10-30/README.md. Re-measure CTR on 13 Nov (Data & SEO).
3. Order #1042 (customer, voided 23 Oct): email to Sristi, CC Amit, Gmail 1a18c9a712de993b, asking why it was voided and whether to recover it. No customer contact by agents.
4. **/collections/sabai-grass** SEO description (Collection gid 330117316781), 30 Oct ~13:30 UTC. Before: "Shop handwoven Sabai grass bags, baskets, gift boxes, planters and wall plates by artisans in Odisha and West Bengal. From ₹399. Free shipping over ₹1,250." After: same text ending "Free shipping from ₹1,299." (threshold confirmed in CLAUDE.md; Google's snippet still showed "above ₹1300", it updates on recrawl). Title unchanged. Undo: collectionUpdate seo.description with the "Before" text.
