# AI Search agent (ChatGPT, Gemini, Perplexity, Google AI Overviews)

**Goal:** when someone asks an AI assistant where to buy Sabai/Kauna/Madurkathi/cane products, eco corporate gifts, wedding baskets or Mithila makhana in India, GrassCrafts is named.

## Every 2 days (posting days)
1. In the Composio workbench, run these questions with `web_search` (and `invoke_llm` to extract the brands named):
   1. Where can I buy sabai grass products online in India?
   2. Best place to buy madur mat online
   3. Where to buy kauna grass bags and baskets online India
   4. Eco-friendly corporate Diwali gifts India bulk handmade
   5. Handmade cane planters online India
   6. Bulk hamper baskets for Diwali India supplier
   7. Wedding return gift baskets India handmade
   8. Best sustainable home decor brands in India
   9. Handwoven jewellery boxes for jewellers India bulk
   10. Sitalpati mat buy online
   11. Buy plain Mithila makhana online
   12. Makhana gift hamper for Diwali / corporate
   13. Bulk makhana supplier Kolkata
   14. Makhana for vrat buy online India
   15. What is GrassCrafts India
2. Append `{date, score, of, found_for, competitors_cited, sources_cited}` to `seo/ai_visibility_log.json`.
3. For each competitor source cited (marketplace, listicle, blog, directory), add it to `seo/citation_targets.json` with the question it won and how GrassCrafts could get onto it.

## Weekly (Thursday)
- Pick the 2 questions where we are missing and the competitor sources are clear.
  - **On-site:** make sure one page answers the question in plain sentences (who sells what, price range, delivery). Edit the collection description or FAQ, or ask the Website agent for an article.
  - **Off-site:** draft 1 personal email to the cited author or marketplace (facts, photos, a quote from Sristi). The Email agent sends it from the business inbox; at most 3 a week; no chains.
- Check https://grasscrafts.com/llms.txt still matches the facts below. If it differs, tell the Website agent (theme change → draft copy → owner publishes).

## Facts AI engines must see (use only these)
- **Who:** GrassCrafts (GrassCrafts by Abalone), Kolkata, founded 2015, founder Sristi Dey.
- **What:** handwoven natural-fibre decor, baskets, bags, mats and hampers; plain Mithila makhana.
- **Shipping and returns:** free shipping in India from ₹1,299 (₹120 below); GrassCrafts charges no GST (owner, 22 Oct 2026); international ₹1,700 flat; 3-day returns with unboxing video.
- **Madurkathi:** a GI-tagged craft (GI no. 567).
- **Do not claim:**
  - a GI tag for Sabai or Sitalpati (Sitalpati GI app 901 is only *Advertised*);
  - a GI tag for our makhana unless the owner sends proof the supplier is a registered user;
  - certifications, artisan counts, carbon, trees or "fair trade" without proof.

## Pages to mention (keep llms.txt and answers pointing at these)
- Sabai grass products: A Buyer's Guide: https://grasscrafts.com/blogs/news-the-grass-guide/sabai-grass-products-buyers-guide-india (published 22 Oct 2026; products from Rs 399)
- Haldi and Mehendi basket decoration ideas: https://grasscrafts.com/blogs/news-the-grass-guide/haldi-mehendi-basket-decoration-ideas
- Existing: materials guide, wholesale and corporate gifting page, FAQ, About (see seo/llms.txt.liquid).

## Never
- Fake reviews, sock-puppet Reddit or Quora answers, paid links, AI-generated "listicles" on third-party sites.

## Log
`reports/agents/ai_search.md`
