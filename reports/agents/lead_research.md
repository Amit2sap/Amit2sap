# Lead Research log (segment agents)

## 2026-10-18
Segment agents ran in parallel. Hunter belonged to corporate today: 1 search and 1 verification used, about 30 searches and 61 verifications left; the quota resets 16 Nov. Kolkata prospects were skipped for Durga Puja week.

- corporate: 10 leads. Best: Swageazy (₹5.4 Cr raise, 800+ enterprise clients; Hemant Arora, Senior Sourcing Manager, Hunter-valid). Kavyatva already buys natural-fibre baskets for its hampers.
- wedding: 10 leads. Best: Deepali Creations, Hyderabad (sells and rents baskets and trays). Volume: Tamarind Global Weddings (welcome hampers).
- hotels: 10 leads. Best: Riomara Kochi (opens Dec 2026, pre-opening). Also King's Mansion Goa (GM Claude Pinto) and Soma Seven Springs.
- diamond_jewellery: 10 leads. Best: Chandukaka Saraf (25th showroom opens 18 Oct). Ivana Jewels has openings 18–25 Oct.
- cane_planters: 10 leads. Best: Awfis Elite Aerocity (100,000 sq ft, biophilic). Volume: Nothing Before Coffee and Third Wave Coffee rollouts.
- sustainable_decor: 10 leads. Best: The Sustainable Marketplace (onboarding brands). Contacts are search-confirmed only; recheck before sending.
- luxury_watches: 10 leads. Best: Jaipur Watch Company (founder Gaurav Mehta). Pitch window: December, ahead of Valentine's Day.
- gourmet: 10 leads. Best: Mittal Teas (founder Nikita Mittal). Gourmet Company already uses wicker baskets.
- wellness: 9 leads. Best: ELE|NA Ayur, Ajabgarh (spa opens 1 Nov). Volume: Tattva, Bodhi and Carlton spa chains.
- real_estate: 10 leads. Best: Century Real Estate and Sattva, both proven key-handover hamper buyers (from BoxUp).
- ethnic_wear: 10 leads. Best: Snusha, Pune (new bridal store). SHREE plans 20–25 stores.
- Blockers:
  - The shared Composio workbench (session "upon") timed out repeatedly under parallel load, and agents overwrote each other's variables. Next time give each segment its own session or use unique variable names.
  - web_search drops source URLs unless the query asks for them; COMPOSIO_SEARCH_EXA_ANSWER returns them.
  - A rate-limit pause from 03:4x to 05:10 UTC interrupted the run; all agents resumed and finished.
- Revisit after 21 Oct (Kolkata, skipped for Puja week): Virachi (ethnic wear), Srijan Realty (real estate), Golden Tips Tea (gourmet), Seiko Kolkata salon (luxury watches).

## 2026-10-20
Group 0 (corporate, wedding, hotels, real_estate), run one segment after another (finished 22 Oct UTC). Hunter belonged to hotels today: 1 search + 1 verification used (27 searches, 55 verifications left; resets 16 Nov). Source: Composio EXA answer (cited URLs) in the workbench, with unique variable names. No competitor watch (not Monday). Kolkata/WB prospects skipped (Puja week): CYC Events, Summit Falling Water Darjeeling, Rishi Pranaya.
- 2026-10-20 corporate: 9 leads. Best: Consortium Gifts (EcoVadis Gold Sept 2026; MD Gaurav Bhagat). Also GIVOO (bulk-gifting platform launched 15 Oct), Bigsmall Corporate (vendor-partnership page), Weavehand (bamboo-basket hampers). The Good Road skipped (already in sent_log).
- 2026-10-20 wedding: 9 leads. Best: Aarunya Club & Convention by Tivoli, Greater Noida (opens 15 Nov, peak season). Also Poonam Mayank Sharma (expanding, Oct 2026) and trousseau packers Grace, DOTTEDi, Weddings & Marigolds. Shaandaar Events skipped (sales@ already in sent_log).
- 2026-10-20 hotels: 9 leads. Best: The Leela Jaisalmer (opens Dec 2026; GM Abhissek Basu, Hunter-valid). Also Bookmark Cheetahgarh Jawai, Azalea Goa, juSTa Monsoon Palace and Wyndham Garden Udaipur (all opened Oct 2026), Rosetta Sakleshpur (new GM).
- 2026-10-20 real_estate: 9 leads. Best: Puravankara (Purva Zenium Phase 2 completing Oct 2026; crm@). Also GHR Infra (1,190-home handovers), Rustomjee Urbania towers done; new CRM heads at Adarsh, Bhumika, Mayfair, ANHAD.
- Blockers: direct page fetch is blocked (proxy 403 / DNS), so contacts come from search-indexed page text only. Exa hides Cloudflare-protected emails ("[email protected]"), so those leads were left out. Generic info@/sales@ inboxes make up most of the contacts.

## 2026-10-21
Group 1 run, segments done one after another. Hunter day = diamond_jewellery: 1 domain search + 1 verification used (lucirajewelry.com); quota before use 29 searches / 59 verifications, resets 16 Nov. No competitor watch (not Monday). Composio web_search answers dropped or invented details, so every signal was re-checked with WebSearch and every contact taken from the company's own site.

- diamond_jewellery: 8 leads. Best: Lucira Jewelry (7th store, Malleshwaram, 10 Oct; 20+ stores planned). Ananya Verma, Executive Merchandiser, Hunter-valid. Also PNG Jewellers, Thangamayil, Palmonas, ORRA, Tamannaah Fine Jewellery, Firefly, Limelight. Skipped KISNA and Lalithaa (already in sent_log).
- cane_planters: 6 leads. Best: UrbanWrk (2nd Hyderabad centre, 85,000 sq ft, 22 Sep). Also The Hazelnut Factory (named contact on own site), MyBranch, Beanlore, The Executive Centre Gurugram, WeWork India. Note: MyBranch and Beanlore have a phone number only.
- sustainable_decor: 6 leads. Best: The Artment (Rs 10 Cr raise, co-founder Aditya Agarwal's email on own site). Also Verdlo (0% commission for founding brands), Wibhoo, Sokka Tableware, Neytt, Vedas Homes (WhatsApp only).
- wellness: 3 leads. Best: Jeena Sikho Lifecare (new hospitals and Panchakarma clinics in pipeline). Also Trē Wellness and Kapiva Ayurveda Clinics.
- Blockers: no tool refused. Dropped for lack of a sourced contact: Vysyaraju Jewellers, CMR Jewellery, P-TAL, Vojara (email not verifiable), Activ8 Pilates, Smartworks. WebFetch could not resolve some hosts (DNS), so the workbench was used to fetch pages.

## 2026-10-22
Group 2 run (luxury_watches, gourmet, ethnic_wear), one segment after another; restarted once after a container restart (no leads had been written before it). Hunter day = cane_planters, so no Hunter use. No competitor watch (Thursday). Composio web_search answers again invented or shifted dates (e.g. TAG Heuer Noida "15 Oct 2026" was Apr 2026; Sierra x DWC "Mar 2026" was Nov 2025), so every signal was re-checked with WebSearch and every contact read from the company's own page.
- 2026-10-22 luxury_watches: 6 leads. Best: Ramesh Watch Company, Hyderabad (11 stores, MD Rohit Chugani plans to double the footprint and enter Vizag/Vijayawada; info@rameshwatch.com). Also Rotoris, IST 1947, Delhi Watch Company, Sebastian Watch Co., Time Avenue. Dropped: Johnson & Co (no current signal), Swiss Time House Kochi (site 403), Seiko India (site unreachable).
- 2026-10-22 gourmet: 6 leads. Best: Manam Chocolate (Diwali Edit 2026 + corporate bulk page naming Bikramjit Mohapatra, bikramjit.m@manamchocolate.com). Also Something's Brewing, Orchard Treasure, Golden Tips Tea, Makaibari, SMOOR (phone only). Skipped Third Wave Coffee (orders@ already in sent_log).
- 2026-10-22 ethnic_wear: 5 leads. Best: Kasturi Kundal (first Delhi boutique, Mehrauli, Sep 2026). Also Matsya by Utkarsh Ahuja (Kala Ghoda couture flagship, Sep 2026), KALKI Fashion (Chennai flagship with bridal suites), Kresha Bajaj (Treasury of Trousseau 2026), The Indian Ethnic Co. (Ahmedabad store, May 2026). Dropped Vionara Hyderabad (opened Oct 2026, but no sourced contact; vionara.in is an unrelated shoe brand).
- 2026-10-22 dead addresses from handoff: Ravi Sweets -> ravisweetshyd@gmail.com (own Stores page); Event Basket -> info@eventbasket.in (own contact page); Puravankara -> info@puravankara.com (company letterhead, 2021 BSE filing); Riomara Kochi -> no valid replacement found (only reservations@ on the site), status no_valid_contact; Hamper Hubb -> dropped (domain does not resolve).
- Blockers: none refused. Direct page fetches worked through the Composio workbench.
