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
