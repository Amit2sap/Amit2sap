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

## Weekly (Monday): refresh the Google reviews shown on the website
1. GET the main listing's reviews (v4 `.../locations/7612515921482745833/reviews`, pageSize 50).
2. Rebuild `seo/google_reviews/google_reviews.json`:
   - `average` and `count` come from the API's averageRating and totalReviewCount.
   - Include every review that has text, newest first, including low ratings. Copy the text exactly; use the Google translation where the API gives one.
   - Use first name + surname exactly as Google shows them, and the date as "Mon YYYY".
3. Write the file to the shop metafield `custom.google_reviews` (type json) with metafieldsSet, owner `gid://shopify/Shop/65880031405`.
4. The product pages render it through `snippets/google-reviews.liquid` (section "Google reviews" in templates/product.json). Never add review schema markup for these reviews.

## Ranking strategy (added 18 Oct)
**Why we don't rank:** the Jul–Sep search-keyword report shows Google links us to "abalone", "flower vase" and "table runner", not to our products.

Fix it with:
1. **Post copy:**
   - The first line names the exact product and material plus "Kolkata" or "India", e.g. "Handwoven Sabai grass laundry basket, Kolkata – ₹…".
   - The SHOP button links to that **product** page, not the homepage.
   - Alternate the materials: Sabai → Madurkathi → Kauna → cane → corporate hampers → wedding baskets.
2. **Services:** keep the 12 specific services (main) and 4 (Makhana) set on 18 Oct. Never put URLs or phone numbers in descriptions.
3. **Reviews:** in the reply, repeat the product name the buyer wrote about, naturally (no keyword stuffing).
4. **Monthly (1st):** pull `searchkeywords/impressions/monthly` for both listings and log the top 20. Success = product/material keywords appear.
5. **Makhana posts** use long-tail topics: "plain Mithila makhana", "makhana for vrat", "makhana gift hamper", "bulk makhana Kolkata".
6. **Never claim** "GI-tagged" for makhana without the owner's proof.
7. **Owner items to chase weekly in handoff.md:**
   - add Products in the Google Business app;
   - accept or reject the Google-suggested 2nd phone number;
   - turn on Merchant Center free listings.

## Profile link (owner, 23 Oct 2026)
GrassCrafts by Abalone: https://share.google/hoCy2Zftpp22vAvzs (Google Knowledge Graph id /g/11gy1lyyl_; search URL https://www.google.com/search?kgmid=/g/11gy1lyyl_).
Posting route: Composio toolkit upload_post (account upload_post_almude-mitty, alias grasscrafts) once the owner finishes the Upload-Post sign-up and the Composio link. Use UPLOAD_POST_LIST_PLATFORM_DESTINATIONS (platform google_business) to pick this location, then UPLOAD_POST_PUBLISH_POST. Posts only; reviews and hours stay manual.
Next theme update: add this profile to the Organization JSON-LD "sameAs" and to the "Rated 4.7★ on Google" link.
