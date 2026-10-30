# Paste this into ChatGPT — GrassCrafts SEO project: who does what (v1, 30 Oct 2026)
(Use together with the v3 instructions of 29 Oct. This file overrides the "SEO data extraction" brief where they differ.)

## Goal (owner)
First target: improve the queries already on Google's pages 1-2 before creating new blogs. No promise of #1 rankings; build a measurable plan.

## Who does what (no duplicate work)

| Step | Owner | Notes |
|---|---|---|
| 1. Search Console extraction (all periods, datasets A–J) | **Claude** | Composio Search Console, read-only. Claude saves the files; the owner uploads them to you. Do not pull a second full extract via Windsor. |
| 2. Site audit (titles, meta, H1, canonical, schema, alt, thin pages, links) | **Claude** | From Shopify admin data + sitemap (more reliable than crawling; Shopify sometimes blocks crawlers). |
| 3. Keyword clusters (16 groups, makhana separate) | **You (ChatGPT)** | Use Claude's files only. |
| 4. Competitor check: real Google results for the top 30 non-branded queries | **You** | Your web search. Record date, country (India), city (Kolkata for local intent), device; keep organic, local pack, shopping and ads separate. Do not call anything top-5 unless you saw the results page. |
| 5. Opportunity scoring and priority list | **You** | Use Claude's data + your competitor checks. Explain the scoring. |
| Content calendar (titles, target keywords, internal links) | **You** | Only after the existing-page plan; information-gain rule from v3 applies. |
| Making any change on the website | **Claude agents only** | Website and Data & SEO agents back up and log every change. You never edit Shopify. |
| Weekly measurement | **Claude** (Mon/Thu report + dashboard) | You may cross-check with Windsor, using the standard below. |

## One data standard (so numbers match)
- Property: `sc-domain:grasscrafts.com` (domain property). Also verified: https://www.grasscrafts.com/ (URL-prefix).
- Periods: last 28 complete days ending 2-3 days before today (Search Console delay), compared with the 28 days before. Longer periods as calendar ranges with exact dates.
- Data state: **final** only. State the exact start and end date on every number.
- Sales: only Shopify orders that are not voided, cancelled or tests (owner's own orders are tests). GA4 purchases labelled "GA4 (may include tests)".
- Known API limits (record them, don't treat them as errors): Google hides rare/anonymised queries, so query rows never add up to the site total; real query rows are a few hundred, not 1,000; searchAppearance cannot be combined with other dimensions.

## Already done — do not recommend again; build on it
- 26 Oct: new SEO titles/descriptions for /pages/grass-weaving-sustainability, /products/wedding-gift-hamper-basket-2, /products/rectangular-water-hyacinth-storage-basket (judge results after 9 Nov).
- 30 Oct: /products/wedding-gift-hamper-basket-2 title "Basket for Wedding Gift – Handwoven Straw Hamper ₹1,050 | GrassCrafts" (re-measure 13 Nov). /pages/wholesale-corporate-gifting: artisan facts + Madurkathi dining-set tile added; quote button, WhatsApp and enquiry form already at the top.
- 29 Oct: Sabai collection links to the guide and blog; free-shipping figure fixed.
- 27 Oct: top 10 products got new SEO titles/descriptions and "Quick answers".
- 22 Oct: landing content + FAQ schema on diamond-jewellery-boxes, diwali-gift-hampers, wedding-gift-hamper, corporate-gifts-handcrafted-gifts. 45 backlink targets planned (0 inbound links in Bing so far).
- 23 Oct: all 208 active products audited (alt text, SEO fields complete).
- 29 Oct: 4 blogs published (straw/jute mats, hotel amenities, jewellery packaging, cane boxes). No new general blogs until 12 Nov (owner priority: conversion and existing pages).

## Known findings (Claude's tracker) — verify and extend, don't rediscover
- Striking distance (pos 5–20): sabai grass (~380 impr, pos ~8, /pages/grass-weaving-sustainability), kauna grass (~140, pos 5.7, /collections/kauna-grass-manipur), straw mat (~120, pos ~10, homepage), hyacinth basket (~100, pos 7.9), cane planters (~70, homepage pos ~9), madurkathi (~70, blog pos 8.2), cane box (~55, homepage), jute mat for table (~50, homepage).
- Wedding basket queries rank 2.4–8 with 0 clicks (≈230 impressions, 2–29 Oct).
- Pages competing for the same query: cane planters (homepage vs /collections/cane-planter pos ~25 vs /products/cane-planters), sabai grass (page vs blog guide vs collection), cane box, madurkathi (blog vs collection), kauna grass.
- 15 of 30 tracked keywords have no impressions, including most makhana terms.

## What you send back (end your reply with these blocks; the owner pastes them to Claude)
FOR CLAUDE / SEO PAGE PLAN
PAGE | URL | Target query | Current pos / impr / clicks (with dates) | What to change (title, meta, copy, internal link, schema) | Facts needed or [ASK SRISTI] | Priority 1-3

FOR CLAUDE / COMPETITOR CHECK
SERP | Query | Date | Country/city | Device | Our position seen | Top 5 organic (domain, URL, page type) | Local pack | What they do better

FOR CLAUDE / CONTENT CALENDAR
TOPIC | Title | Target query | New thing (information gain) | Internal links | Publish after (date)

## Rules (unchanged)
Read-only. No invented volumes, difficulty, rankings, competitors or traffic. Separate observed facts, estimates and recommendations. Preserve URLs exactly. No prices, MOQ, lead times or samples in B2B copy. No GI claim except Madurkathi (GI no. 567). No "living wages" or percentages about artisans.
