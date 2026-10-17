# 17 Oct 2026: reviews setup

- **Orders:** 37 open orders (#1003–#1036, #1038–#1041) marked Fulfilled, with notifyCustomer=false, so no shipping emails went to customers. The owner confirmed all were delivered. #1001 and #1037 were cancelled and left as they are. Judge.me can now send its review-request emails for these orders, according to its own timing settings.
- **Google reviews on product pages:**
  - All 21 Google reviews (4.7★) were pulled from the Google Business Profile API.
  - The 18 that have text are stored in the shop metafield `custom.google_reviews`.
  - Added the snippet `google-reviews.liquid` and a "Google reviews" section placed after the product info in `templates/product.json`.
  - These changes are in the theme copy **"Grasscrafts Live + Google reviews (17 Oct 2026)"** (id 189376495789), duplicated from the live theme on 17 Oct. The preview renders correctly.
  - **The owner must publish it**; the API blocks theme publishing.
  - Source files are in `seo/google_reviews/`.
- **New page:** /pages/review-us (Google + website + Facebook review links, plus the Judge.me all-reviews widget). The QR card's second QR code points here.
- **Noticed, not changed:**
  - The Judge.me product widget block has `review_data: sample_data`. Check in the theme editor that no sample reviews show on the live site.
  - Product pages also carry a Klaviyo Reviews widget, so there are two review widgets. Keep one.
  - The "Circular Legacy" section shows numbers (2400 L water, 3.2 kg CO₂e, 850 g plastic) attributed to "Grasscrafts Internal Audit 2026". Make sure these can be backed up, or remove them (greenwashing risk).
