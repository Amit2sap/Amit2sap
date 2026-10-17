# Website & Search agent (Shopify + Google + AI search)

## Daily
1. **AI-visibility check.** Run `seo/ai_visibility_check.py` in the Composio workbench and append the result to `seo/ai_visibility_log.json`.
2. **Store health.** Pull last-24-hour sessions, add-to-carts, checkouts and orders (Shopify analytics). Log the conversion funnel.
3. **Abandoned checkouts.** Count those from the last 24 hours. If a checkout over ₹1,000 has an email and no order within 24 hours, add it to the handoff so the Email & Actions agent sends one polite reminder. The customer must have started the checkout themselves; send only one reminder.
4. **Unfulfilled orders.** List orders that are still unfulfilled after 5 days and alert the owner through the handoff.

## Weekly
- **Mon:** Search Console. Top queries and pages (28 days), CTR outliers (more than 100 impressions and under 1% CTR), and position changes for: sabai grass, kauna grass, madurkathi/madur mat, cane planters, corporate gifts, wedding hamper baskets, wall plates. Log them, then fix the worst one: title, meta description or internal links. Back up first.
- **Blog:** moved to the alternate-day Blog Engine below. No separate Wednesday article.
- **Fri:**
  - On-page fixes: missing collection descriptions and weak alt text on new products.
  - 2–3 new "get cited" pitches. Pick targets from the study (skip anyone already in `outreach/pr_pitches.json`) and log them in that file.
- **Always:**
  - Back up a page or collection before editing it.
  - Log changes in the `seo/CHANGELOG-*.md` files.
  - Never change prices, inventory, discounts, payments or themes.

## Blog Engine (owner, 17 Oct): one article every posting day (every alternate day from 18 Oct)

1. **Pick the topic.** Take the first unchecked topic in `agents/blog_topics.md`, unless an occasion within 21 days in `agents/calendar.md`, or a gap in `agents/STRATEGY.md`, needs a sooner one.
   - Before writing, search Shopify articles for the same keyword. If one exists, update and extend that article instead of writing a duplicate. Back it up first.
2. **Research.** Use web search on the top 5 results and the questions people ask (People-Also-Ask and AI answers for the query). Note what they cover and what they miss.
3. **Write it, optimised for AI answers.** 1,200–1,800 words, written for India, in plain English.
   - **Structure:**
     - Answer-first intro: the first 2 sentences answer the query directly.
     - Clear H2 and H3 headings phrased as questions.
     - A comparison or price table using only ACTIVE catalogue prices from Shopify.
     - "How to choose", "care" and "uses" sections.
     - 5–7 FAQs plus FAQPage JSON-LD.
   - **Links:** 3–5 internal links to collections and products, plus 1–2 links to authoritative sources (for example the GI registry for Madurkathi).
   - **Byline and voice:** byline "Sristi Dey, founder, GrassCrafts". First-hand artisan detail, but only facts already in repo files or the catalogue.
   - **B2B line** where it fits: "Ordering in bulk for a wedding, hotel or company? WhatsApp +91 62907 44782."
   - **Never** invent statistics, awards, clients or certifications. No GI claim for Sabai. Never mention trade prices, MOQ or lead times.
4. **Images.**
   - **Featured image and in-article images:** real GrassCrafts product photos from Shopify (cdn.shopify.com), with descriptive alt text (product + material + use).
   - **Real photos are required for anything that shows a product.** An AI-generated picture must never pass as our product.
   - **Optional AI images:** only decorative or explainer graphics (for example a "how Sabai grass becomes a basket" diagram or a seasonal banner). Use them only if an image-generation tool is connected (for example through Composio). Upload with Shopify `stagedUploadsCreate` + `fileCreate`, give them alt text, and say in the log that the image is AI-generated.
   - If no image tool is connected, use product photos only and log "AI image tool not connected" once a week. That is a note, not a blocker.
5. **Publish.**
   - `articleCreate` on the main blog: SEO title of 60 characters or fewer, and a meta description of 155 characters or fewer (metafields global.title_tag / description_tag).
   - A handle containing the keyword, tags, a summary, and the featured image.
   - Then add the article URL to the matching collection description's "Guides" line (back up first).
6. **Promote.**
   - Add a line to `reports/agents/handoff.md` so the Pinterest, Instagram and Facebook agents can use the article on their next posting day.
   - Request indexing: resubmit the sitemap in Search Console, then inspect the URL.
7. **Log it** in `seo/CHANGELOG-blog.md`: date, title, URL, keyword, images used, and internal links.
