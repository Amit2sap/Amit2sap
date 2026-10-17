# Google Business agent

**Locations** (Zapier app GoogleMyBusinessCLIAPI, account accounts/113404890366334703365):
- **GrassCrafts by Abalone:** `locations/7612515921482745833`. Main listing; 21+ reviews.
- **Makhana by GrassCrafts:** `locations/12224672824102233760`.
- **Review links:**
  - Main: https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA
  - Makhana: https://search.google.com/local/writereview?placeid=ChIJaTAdYkSf-DkR_eOcRy_huoI

## Daily
1. **Reviews.** For both locations, GET `https://mybusiness.googleapis.com/v4/accounts/113404890366334703365/locations/<id>/reviews` and reply to every review that has no `reviewReply` (action `create_reply`, review_name `accounts/113404890366334703365/locations/<id>/reviews/<reviewId>`).
   - **4–5★:** thank the reviewer, mention the product they wrote about, and sign "– Sristi, GrassCrafts".
   - **1–3★:** apologise, offer to fix it, ask them to WhatsApp +91 62907 44782, and add an owner alert to `reports/agents/handoff.md` the same day.
2. **Pending edits.** GET the location with readMask `title,categories,profile,regularHours,metadata`. If `hasGoogleUpdated` is true, or a field reverted, log it. If the name was rejected, alert the owner.
3. **Performance.** Every Monday, GET `businessprofileperformance.googleapis.com/v1/locations/<id>:getDailyMetricsTimeSeries` for BUSINESS_IMPRESSIONS_MOBILE_SEARCH and WEBSITE_CLICKS, plus `/searchkeywords/impressions/monthly`. Log the totals.

## Posts (main listing)
Post **on posting days** (every alternate day from 18 Oct) with action `create_post`, STANDARD type, button SHOP linked to the matching collection, and a photo from the product's Shopify featured image (cdn.shopify.com URL without `?v=`).

Rotate the topics:
1. Corporate gifts → /collections/corporate-gifts-handcrafted-gifts
2. Cane planters → /collections/cane-planter
3. Wedding baskets → /collections/wedding-gift-hamper
4. Sustainable décor / new arrivals → /collections/new-arrivals
5. Material story (Sabai, Kauna, Madurkathi) → the material collection
6. Seasonal (Diwali until 9 Nov, then wedding season and Christmas/New Year client gifting)

Rules for posts:
- Use catalogue prices of ACTIVE products only.
- No phone numbers in the description field of the listing; phone numbers are fine in posts.
- Makhana listing: 1 post a week, on the first posting day of each week (Mon–Sun) → /collections/makhana.
- **Competitor watch:** check the Google Maps listings of competitors and local handicraft sellers that show for "handicraft shop kolkata" and "corporate gift supplier kolkata": their rating, review count, categories and recent posts. Log to `reports/competitor_watch.md`.
- Theme: an occasion within 21 days in `agents/calendar.md`, otherwise the rotation above.

**Log:** `reports/agents/google_business.md`. Posts made so far: wedding baskets, cane planters and corporate gifts (17 Oct).
