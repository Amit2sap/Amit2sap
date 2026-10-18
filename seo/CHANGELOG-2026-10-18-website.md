# Website changes, 17–18 Oct 2026 (owner said "go all", "remove Klaviyo", "match top websites")

## Live now (Admin API; backups in backups/)
- **Collection images:** 21 collections that had no image now use their best product photo, with alt text.
  - Backup: backups/collections/collections_before_2026-10-17.json
- **Collection titles cleaned:** Planters, Festive & Christmas Gifts, Gifts Under ₹1,000, Asana & Puja Mats, Jute Mats & Rugs, Wall Plates & Wall Décor, Corporate Gifts, Bed, Yoga & Nap Mats, Sabai Grass, Haldi/Mehendi/Baby Shower Gift Hampers, Cane Baskets & Trays, Straw Baskets & Trays, Earth Edit — Dining.
  - Handles and SEO titles are unchanged.
- **Main menu:** 5 top-level items.
  - **Gift Atelier:** Diwali, Corporate, Wedding, Diamond & Jewellery Boxes, Makhana, Gifts Under ₹1,000.
  - **Collections:** links to /collections/all, with Shop by Material (now includes Sitalpati) pointing to the materials guide.
  - **The Earth Edit:** short sub-names.
  - **Wholesale & Corporate:** new top-level link, as iTokri and The Decor Kart do.
  - **Our Heritage.**
  - Backup: backups/menus/main_menu_before_restructure_2026-10-17b.json
- **The Earth Edit:** the 2 sold-out items were moved to the end of the collection.
- **Stock set to 2** (owner instruction, 18 Oct):
  - Sitalpati Tote Bag: 2.
  - Bespoke Jute Mandala Rug: 2 each for Small, Medium and Big.
  - Both were 0 before.
- **Bamboo image alt text** added (shopify_images/1771576603178_2.jpg).

## Draft theme 189380886701 "Grasscrafts – Clean-up + no Klaviyo (DRAFT 17 Oct)", for the owner to publish
- Copy of live 189377052845: all 418 files present, checksums identical before the edits. Live files are backed up in backups/themes/189377052845_2026-10-17/.
- **Klaviyo removed:**
  - Klaviyo Reviews badge and widget, plus the two empty app sections on the product page.
  - Klaviyo onsite embed switched off.
  - Judge.me stays as the only review app.
- **App embeds switched off:** POWR image slider, Instafeed, UpPromote (×2), Wishlist collection hearts.
  - Instafeed and UpPromote still inject legacy scripts until the apps are uninstalled. That is the owner's call.
- **Colours:**
  - 8 unused neon, gradient and purple schemes deleted.
  - Schemes 3–5 had near-white text on cream; their text is now brown and readable.
  - The hero now uses the brand green scheme.
- **Product page:** the "GrassCrafts" vendor line is removed; the cart vendor and New Arrivals vendor are off.
- **Claim fix:** Sitalpati is no longer called "GI-tagged". GI application 901 is only *Advertised* on the IP India register. The Madurkathi GI claim stays.
- **Brand text:** "Straw, Seagrass" replaced with the real material list.
- **Homepage rebuilt to match the top sites** (iTokri, Ellementry, Nestasia, The Decor Kart, Zwende, Okhai). Order:
  1. Hero
  2. **Why GrassCrafts strip** (verified facts only): handwoven in India, free shipping ₹1,300+ / ₹120 below, 3-day returns with unboxing video, Google rating read live from the metafield, bulk orders.
  3. Google reviews
  4. **Shop by Category**: 8 tiles.
  5. New Arrivals
  6. Most Loved
  7. **Gift by Occasion**: Diwali, Wedding, Corporate, Haldi, Mehendi, Baby shower.
  8. **Shop by Price**: under ₹999 (84 products), ₹1,000–2,500 (104), above ₹2,500 (43). Each uses a storefront filter URL, all tested.
  9. The Earth Edit
  10. Material Edit
  11. Journal
  12. **FAQ**: 6 questions, copied from /pages/faq.
  13. **SEO text block**
  14. Contact
  - The duplicate "From India's Grasslands" text is hidden, and the empty section is removed.
- **Announcement bar:** "Rated 4.7★ on Google by our customers" (links to /pages/review-us) · Free shipping ₹1,300+ · "Bulk & corporate gifting orders – get a quote".
- **Preview check (18 Oct):** home, product and collection pages render with no Liquid errors and no Klaviyo code.

## Not done (rules or owner-only)
- **No discount banners.** Competitors run "upto 70% off", but prices and discounts are the owner's decision.
- **Store name** is "grasscrafts.com", which feeds schema and page titles. The owner can change it under Settings → Store details → Store name.
- **Uninstall unused apps**, under Settings → Apps: Klaviyo (if email isn't used), Instafeed, UpPromote, POWR.
