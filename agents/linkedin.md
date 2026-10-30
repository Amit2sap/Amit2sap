# LinkedIn playbook (from 22 Oct 2026)

**USPs and pitch (owner, 30 Oct 2026):** every B2B pitch, post and proposal uses the 8 USPs and the wording in `sales/grasscrafts_usp_pitch_2026-10-30.md` (made to order, brand customisation, artisan craftsmanship, natural fibres, premium presentation, reusable, versatile B2B range, artisan story). Segment templates in `outreach/templates.py` stay as the base; add the matching USP bullets and the segment hook from that file.


**Account:** Composio LinkedIn connection `linkedin_lacca-cob`, posting as the member profile "grasscrafts ." (author `urn:li:person:19s_VB0aGJ`, linkedin.com/in/grasscrafts-889b4624). The owner approved this on 22 Oct until a company page is connected. When a company page is connected, switch to it: the author becomes `urn:li:organization:<id>`, found with LINKEDIN_GET_COMPANY_INFO.

**Who it's for:** B2B buyers only. Write for HR and admin heads, procurement, gifting-company founders, hotel GMs and housekeeping heads, wedding planners, and jewellery and watch retailers. It is not for consumers.

**When:** posting days only (`(today - 2026-10-18).days % 2 == 0`), at most 1 post a day. It runs inside the Social agent, after Pinterest.

**What to post** (rotate, with an occasion from `agents/calendar.md` that falls within 6–8 weeks):
1. Corporate gifting: Diwali, New Year or Holi hampers built on Kauna or Sabai baskets, branded or plastic-free.
2. Hotel and spa amenities: laundry baskets, tissue-box covers, trays, Madurkathi mats.
3. Wedding and trousseau baskets for planners.
4. Artisan story: the craft, the region and the materials (Sabai, Kauna, Madurkathi GI no. 567, water hyacinth, cane).
5. Retail packaging: handwoven jewellery or watch boxes and display trays.

**Format:**
- 120–220 words, a strong first line, short paragraphs and 3–5 hashtags.
- One real product photo from our Shopify CDN, uploaded with LINKEDIN_REGISTER_IMAGE_UPLOAD or as an image in LINKEDIN_CREATE_LINKED_IN_POST.
- End with a call to action: "Bulk and corporate enquiries: sristi@grasscrafts.com" or the relevant grasscrafts.com page.

**Never:**
- quote trade prices, MOQ, lead times or samples;
- invent clients, numbers, awards or certifications (use only facts from the catalogue and `agents/ai_search.md`; check the "400+ artisans" headline before repeating it);
- tag people or companies;
- send messages or connection requests;
- scrape anything.

Log each post (date, URN and topic) in `reports/agents/linkedin.md`.

## Amit's personal LinkedIn outreach (owner, 29 Oct 2026)
Connection requests and messages from Amit's own profile are MANUAL. Agents only prepare the weekly kit (Mondays, Lead Research run) per agents/linkedin_manual_outreach.md and deliver it as Todoist tasks. Never send from any profile, never scrape.

