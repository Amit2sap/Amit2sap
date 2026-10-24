# Sabai grass ranking fix (17 Oct 2026)

## Diagnosis (Search Console, 15 Jul – 15 Oct)
- "sabai grass": 1,649 impressions, 12 clicks (0.7% CTR), position 7.3. All of it goes to **/pages/grass-weaving-sustainability**, not the homepage. The homepage only showed in the earlier 13 Oct baseline.
- /collections/sabai-grass ranks at about position 76 for "sabai grass". It does win "sabai grass bags" (158 impressions, position 9) and "sabai grass handbags" (position 10).
- **Cause:** Google reads "sabai grass" as an informational search ("what is it"), so it ranks the guide. The guide's only links went to the homepage, with no product or collection links, so searchers had nowhere to buy.

## Fix
1. **/pages/grass-weaving-sustainability**
   - Backup of the old text: `backups/pages/grass-weaving-sustainability_2026-10-17_content.md`.
   - Rewritten with clean HTML (the MS Word inline styles are gone).
   - New opening answer and a "Shop Sabai grass products" table with 6 real products and prices.
   - Links to the Sabai collection throughout, using descriptive anchors.
   - New sections: care, and bulk orders.
   - FAQ with FAQPage JSON-LD.
   - Dropped the unverified "British Army WWII rope" claim.
   - Page title: "Sabai Grass: What It Is, Uses, Benefits & Handwoven Sabai Products".
   - SEO title: "Sabai Grass (Babui Ghas): What It Is, Uses & Products to Buy | GrassCrafts".
   - Meta description now mentions products and "from ₹399".
2. **/collections/sabai-grass**
   - Description expanded for buyer searches: Sabai grass bags, wall plates, boxes, baskets, planters, with "from" prices.
   - Links to the guide and the basket comparison article.
   - (SEO title and description were already updated earlier on 17 Oct.)
3. **Not done:** adding collection links to the blog post "Sabai Grass: The Sustainable Wonder". The update was declined when I submitted it.

## Expected effect and follow-up
- More clicks from the guide (better snippet) and a path from the guide to the collection and products.
- The collection should move up for buyer-intent searches.
- Check again in 2–3 weeks on the Monday Search Console run: watch "sabai grass" CTR and collection positions for "sabai grass products / bags / baskets".
- **Owner:** in Search Console, use URL Inspection → Request indexing for both URLs to speed up re-crawling.
