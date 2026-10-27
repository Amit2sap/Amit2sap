# Lead Research: one agent per B2B segment

**Schedule:** runs every day at 09:07 IST, before the Email & Actions agent (10:22).

**Format (owner, 19 Oct 2026, to save usage):** one background agent works through **3–4 segments a day, one after another**, in a 3-day rotation. Group = `(today - 2026-10-20).days % 3`:
- 0: `corporate`, `wedding`, `hotels`, `real_estate`
- 1: `diamond_jewellery`, `cane_planters`, `sustainable_decor`, `wellness`
- 2: `luxury_watches`, `gourmet`, `ethnic_wear`

Every segment is still covered every 3 days. Competitor observations only on Mondays.

**Output per segment on its day:** up to **10 verified opportunities**, saved to `outreach/leads/<segment_slug>.json`.

**Who uses them:** the Email & Actions agent emails these leads first, before using generic info@ addresses.

## Segments

| slug | Segment | Mix % | What we sell them (ACTIVE catalogue only) | Who decides | Where to look |
|---|---|---|---|---|---|
| `corporate` | Corporate gifts: gifting companies, plus HR/Admin at companies with 200+ staff | 18 | Kauna hamper baskets, Sabai gift boxes, cane desk organisers, trays | Gifting-company founder or sourcing head; CHRO, employee-engagement or admin head | Google "corporate gifting company <city>", IndiaMART, LinkedIn company pages, Gift World Expo exhibitors |
| `wedding` | Wedding planners, venues, trousseau packers | 14 | Wedding, Haldi and Mehendi hamper baskets, trousseau baskets, trays | Founder or creative director | WedMeGood, WeddingWire, Instagram planner bios, banquet venue sites |
| `hotels` | **Hotels and resorts** (boutique, heritage, eco, 4–5★) | 12 | Laundry/storage baskets, tissue box covers, cane trays, cane planters, Madurkathi and straw mats, table mats | GM, purchase manager, housekeeping head, F&B/banquet manager, interior lead for new properties | Hotel group sites, "new hotel opening <state> 2027" news, FHRAI and HICSA lists, Google Maps listings |
| `diamond_jewellery` | **Diamond and gold jewellers**: jewellery boxes and baskets | 12 | Sabai and Kauna jewellery boxes, boxes with lids, display trays, bridal hamper baskets | Director, marketing head, visual-merchandising or packaging head | Jeweller websites, GJEPC/IIJS exhibitor lists, Instagram bios of jewellery brands |
| `cane_planters` | Cafés, co-working spaces, interior designers, architects, landscapers | 9 | Cane planters (table, stand, 38 in floor, sets of 3), grass planters | Owner, principal designer, project buyer | Houzz, IIID directory, India Design ID exhibitors, café-chain sites |
| `sustainable_decor` | Sustainable décor brands, concept stores, eco marketplaces | 8 | Wall plates, madur mats, Sabai boxes, water hyacinth baskets | Founder or buyer | Brown Living sellers, "sustainable home decor store <city>", Instagram |
| `luxury_watches` | **Luxury watch boutiques, multi-brand retailers and Indian watch brands** | 7 | Handwoven boxes with lids, cane trays and desk organisers as client gifts or gift-with-purchase; custom sizes on request | Boutique owner or director, CRM/clienteling head, marketing head | Retailer websites (multi-brand chains and city boutiques), mall directories, LinkedIn |
| `gourmet` | Gourmet, tea, coffee, dry-fruit and sweet brands (hamper packaging) | 7 | Kauna hamper baskets, bamboo trays, Sabai boxes | Founder, packaging or product head | D2C brand sites, Instagram, IndiaMART |
| `wellness` | Spas, Ayurveda and wellness centres, yoga studios | 5 | Madurkathi mats (GI no. 567), straw yoga mats, Kash trays, tissue box covers, baskets | Owner, spa director, purchase manager | Google Maps, wellness-resort lists, yoga-studio sites |
| `real_estate` | Real-estate developers (key-handover and homebuyer festive gifts) | 4 | Sabai gift boxes, Kauna hampers, planters as housewarming gifts | CRM head, marketing head, admin | Developer websites, RERA project lists, LinkedIn |
| `ethnic_wear` | Saree, bridal and ethnic-wear boutiques (trousseau packing, premium packaging) | 4 | Trousseau baskets, Sabai boxes, hamper baskets | Owner or founder | Instagram boutique bios, Google Maps, wedding-fair exhibitor lists |

**Changing the mix:** the owner can change the mix % here. The lead agent may move a segment by up to ±3 points a week, based on replies (see `agents/STRATEGY.md`).

## Daily workflow (each segment agent)
1. **Read the context.**
   - `agents/calendar.md`: which occasion is within the next 6–8 weeks for this segment.
   - `agents/STRATEGY.md`: the current focus.
   - Your own lead file: skip companies already listed.
   - `outreach/sent_log.json`: skip anything in `sent` or `do_not_send`.
2. **Find opportunities with buying signals.** Use the Composio workbench web_search and the sources in the table above. Prefer companies that show at least one signal:
   - a new property, store or outlet opening;
   - a festive or bridal collection launch;
   - hiring a gifting, procurement or visual-merchandising role;
   - exhibiting at a trade fair;
   - Instagram posts showing hampers or gift packaging;
   - a sustainability or plastic-free pledge;
   - an existing competitor's products in their stores or gifts.
3. **Find a decision-maker contact.** Use only **business contact details the company itself publishes or that are verifiable**, in this order:
   1. **Hunter.io** domain search for a named person in the "Who decides" roles. Then verify with the Hunter verifier, or an SMTP RCPT check in the workbench.
   2. Emails and phone numbers on the **company's own website** (Contact, Corporate, Bulk orders or Careers page). You find these with web search snippets.
   3. Business listings: the **Google Business listing, IndiaMART, JustDial**, and the **Instagram or Facebook business-profile** contact button or bio.
   4. **LinkedIn:** name and role only, taken from search results. Do not log in to LinkedIn or scrape it. Find the email for that person with Hunter.

   **Rules for contacts:**
   - **No personal mobile numbers** taken from personal profiles, leaked lists or people-search sites. Save only business numbers the company publishes (landline, business WhatsApp, office mobile shown on its own site or listing).
   - Do not send automated WhatsApp or SMS to these numbers. WhatsApp requires opt-in. Numbers are for Sristi to call **after** a prospect replies, or when the company lists the number for business enquiries.
   - Record the **source URL** for every email and phone number. No source means don't save it.
   - Don't guess email patterns unless Hunter or SMTP verifies the result. Mark the result `"verified": "hunter_valid" | "smtp_ok" | "published"`.
   - **Hunter free plan:** 50 searches and 100 verifications per month, reset on the 16th. That allows only about **1 domain search and 3 verifications a day across all segments**.
     - The search rotates down the segment table, one segment per day: row number `(today - 2026-10-18).days % 11` in the table (0 = corporate, 10 = ethnic_wear).
     - Only that day's segment agent may use the search, and only on its best opportunity.
     - Every other contact comes from published sources.
     - Check what is left first with Hunter's account endpoint. Stop at zero.
4. **Save the leads.** Append to `outreach/leads/<slug>.json`, a list of objects:
   ```json
   {"found": "2026-10-18", "segment": "hotels", "company": "...", "city": "...", "website": "...",
    "signal": "Opening a 120-key resort in Goa, Dec 2026", "signal_url": "https://...",
    "contact_name": "...", "role": "...", "email": "...", "email_source": "https://... or hunter",
    "verified": "hunter_valid", "business_phone": "+91...", "phone_source": "https://...",
    "products_to_pitch": ["laundry basket", "tissue box cover", "cane planters"],
    "occasion": "Christmas lobby décor / new property opening",
    "competitor_used": "e.g. Brown Living (source URL) or unknown", "current_products": "...", "budget_signal": "their retail hamper ₹1,499–4,999 (source) or estimate: <basis>",
    "buying_pattern": "festive + wedding, ~2x/year (source or estimate)", "status": "new"}
   ```
4b. **Competitor customers.** Spend part of every run finding buyers who already buy this segment's products from competitors (see the shared rule in `agents/README.md`). Log them in `outreach/competitor_customers.json` and add them as leads. They are the warmest leads we have: they already buy the category.
5. **Write a log entry.** Add a dated line to `reports/agents/lead_research.md`: segment, leads added, best opportunity of the day, and any blocker.
6. **Flag hot opportunities.** A very strong signal (for example a new hotel opening within 60 days, or a jeweller launching bridal packaging) gets a line in `reports/agents/handoff.md` for a personal email.

## Rules
- Facts only. Never invent a company, person, signal or contact. If you can't verify a contact, don't save it.
- One contact per company domain per 90 days.
- Kolkata/West Bengal prospects: skip during Durga Puja week.
- Stay within the tools you have. If web search or Hunter is refused, log the blocker; do not work around it.

**Hunter budget (26 Oct):** only ~26 of 100 monthly verifications left until 16 Nov. Until then: lead research verifies at most 3 addresses per run (strongest buying signal first); keep the rest for the actions-page collab pitches (agents/daily_actions.md), which verify every address before it goes to the owner.

## Tools update (27 Oct 2026) — see agents/TOOLS.md
Use Exa (claude.ai connector) for searches and contact-page reads. Lusha only for warm/hot leads needing a named buyer (free plan, 40 credits; email reveal only). Ahrefs is not usable (no API access); Semrush was removed (paid only).
