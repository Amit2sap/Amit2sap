# 27 Oct 2026: makhana article SEO + real photo; wholesale quote form fields (owner request via ChatGPT research)

## 1. Article "Makhana for Diwali: Easy Roast, Kheer & Reusable Gift Ideas" (gid://shopify/Article/635143225517)
- SEO description (global.description_tag) set: "Easy Diwali makhana ideas: roast at home, makhana kheer, and gifting in a reusable handwoven GrassCrafts basket. Bulk and corporate enquiries welcome."
- Featured image: AI illustrative PNG replaced with the real makhana product photo (files/IMG-20260620-WA0000.jpg), alt "GrassCrafts Mithila makhana (premium lotus seeds), real product photo".
- Backup: backups/articles/makhana_diwali_article_before_2026-10-27.json. Undo: articleUpdate with the old image URL/alt; delete the description_tag metafield.

## 2. Wholesale page quote form (gid://shopify/Page/166751240365, /pages/wholesale-corporate-gifting)
Replaced the single textarea line
`<label style="grid-column:1/-1">Anything else? (sizes, colours, branding, budget per piece)<br><textarea name="contact[body]" rows="3" style="width:100%;padding:9px"></textarea></label>`
with fields: Supply type (Basket only / Filled hamper / Not sure yet), What goes inside, Basket inner size needed, Branding (None / Tag or card / Printed ribbon / Other), Target budget per piece (₹), Delivery country (if outside India), and the textarea relabelled "Anything else? (colours, lining, samples)".
Undo: pageUpdate with the old line restored (exact text above). Existing fields (name, company, email, phone, products, quantity, occasion, needed by, city) unchanged.
Note for owner: the page says "Pan-India delivery with GST invoice" while CLAUDE.md says no GST is charged on any product. Not changed; owner/Sristi to confirm wording.
