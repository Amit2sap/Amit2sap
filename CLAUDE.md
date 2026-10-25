# GrassCrafts growth agent team — start here

Every new Claude session on this repo reads this file first. It is the memory of the work done so far (written 23 Oct 2026). Work on branch `claude/grassctafts-sales-growth-d8azah`; `git pull` before work, commit and push after.

## Business
- GrassCrafts / "GrassCrafts by Abalone", Kolkata. Handwoven Sabai, Kauna, Madurkathi, Sitalpati, Kash, cane, water hyacinth, bamboo, jute decor, baskets, bags, mats, hampers; Mithila makhana; dry flower torans (₹960, 3 ft; made to order, inventory untracked by owner decision 25 Oct).
- Owner: Amit Dey (amit2sap@gmail.com). Founder: Sristi Dey (sristi@grasscrafts.com, WhatsApp +91 62907 44782). Hot leads go to Sristi with Amit in CC.
- Shopify store 605e40-ba (grasscrafts.com, INR). Facts: free shipping from ₹1,299, NO GST on any product ("Charge tax" off on every variant), Cash on Delivery on, ₹100 extra per COD order (owner, 24 Oct; Releasit COD app). Makhana packs (250 g, 500 g, 1 kg, 5 kg bulk; tag makhana-free-shipping) ship free with no minimum; the makhana gift hamper follows standard shipping.

## Hard rules (owner decisions)
- Outreach: max 100 outbound emails/day (new + follow-ups + pitches); replies are never capped and answered same day. Only business emails published on the company's own site or Hunter "valid"; never guess; check outreach/sent_log.json (sent + do_not_send) first.
- Never quote prices, discounts, MOQ, lead times or samples in outreach — except the Sristi-approved priced trade catalogue. Never accept partnerships or sign-ups: save a draft and flag.
- Never invent facts, reviews, certifications, client names or numbers. No consumer profiling or follower scraping. Never auto-comment on other people's posts (owner approves via the actions page).
- Website: back up before every change (backups/), log undo steps (seo/CHANGELOG-*.md). Theme edits only in an unpublished theme copy; the owner publishes. Never change prices, inventory, discounts, payments, checkout, shipping or apps without the owner.
- Image generation is PAUSED (agents/lifestyle_images.md). Use only real photos.
- Usage: Sonnet subagents for routine runs, one job at a time, no image viewing, small outputs.

## Where things are
- Rules per agent: agents/*.md (README.md = shared rules + schedule). Open tasks: reports/agents/handoff.md (lines starting "- [ ]"). Logs: reports/agents/*.md. Changes: seo/CHANGELOG-*.md.
- Leads: outreach/leads/*.json, outreach/sent_log.json, outreach/DAILY_RUNBOOK.md, sales/b2b_targeting_playbook.md.
- Daily actions page (owner approvals): https://claude.ai/artifact/T8hhYdcLaL545XpKfCCoZF (ArtifactData, collection "items").
- Market map: https://claude.ai/artifact/FCLmZodrJBK1zNUhKHpwER. Trade catalogue (Moda): https://moda.app/canvas/8ffa7e7d-19d4-4579-b84f-b0778f1d3288.

## Connections (Composio unless noted)
Gmail gmail_movie-arab · Instagram instagram_basoid-oer (@grasscrafts.com_) · Facebook Page 142803116227246 · Pinterest pinterest_whosen-hoose · LinkedIn linkedin_lacca-cob (author urn:li:person:19s_VB0aGJ) · Search Console (sc-domain:grasscrafts.com) · GA4 · Bing Webmaster · Hunter · WhatsApp API whatsapp_guha-marko (WABA 28037860215843187, sender +91 81004 47884 "Gift Hamper", phone_number_id 1292616473939901; 12 approved templates; marketing only to customers with SMS/WhatsApp consent) · Google Business via Upload-Post upload_post_halide-drawly (GrassCrafts by Abalone locations/7612515921482745833, Makhana by GrassCrafts locations/12224672824102233760) · Gemini (no key). Shopify and Moda are claude.ai connectors. Not working: Windsor (removed), Zapier (task limit), Google Drive/Sheets create (403), Pipedream (not signed in).

## Scheduled tasks (IST)
Data & SEO 07:37 Mon/Thu · Lead research 08:07 Mon–Fri · Email & Actions 10:22 daily · Google Business 11:14 Tue/Thu/Sat · Social 13:41 daily · AI Search 13:47 Thu · Reply watcher 15:07 & 19:07 · Website 17:22 Mon/Wed/Fri. Each launches one Sonnet subagent with its agents/*.md playbook.

## Waiting on the owner (23 Oct)
Live theme 189623959725 "makhana + shipping fix 25 Oct" (published 25 Oct; undo 189658235053) · Releasit COD ₹100 fee NOT working yet (site text says ₹100 extra) · AVADA SEO app: add availability to its Product snippet or turn it off · Sristi: confirm real costs behind the makhana hamper (₹649/₹949) and bulk 5 kg (₹5,499) prices, now live, priced-catalogue corrections, call the cane-stool hot lead.
