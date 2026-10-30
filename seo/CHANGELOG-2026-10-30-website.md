# Website changelog 2026-10-30 (directives D32, D34, D7; owner approved 30 Oct, 48h notice waived)

Backups: backups/2026-10-30-directives/ (collections.json, products.json). Method: Shopify Admin API (collectionUpdate / productUpdate, descriptionHtml only). Prices, inventory, discounts, payments, checkout, shipping, apps and the live theme untouched.

## D32 /pages/wholesale-corporate-gifting: audit, NO CHANGE (status: verified live)
Checked via Shopify page body (updatedAt 2026-10-30T11:37Z, Master's edit) and a mobile Firecrawl render (mobile=true, maxAge 0, HTTP 200):
- Bulk-enquiry button above the fold: "Get a bulk quote" anchor (#wholesale-quote) is in the first paragraph block, with the trade sample sheet link and WhatsApp link. PASS.
- Mobile enquiry route: form (POST /contact, tel/email/qty fields, 1-col grid via auto-fit minmax(220px)) plus WhatsApp wa.me/916290744782 link with prefilled text. Both render in the mobile output. PASS. (No email address shown; form + WhatsApp judged sufficient.)
- Categories with links: 5 image tiles to products (Kauna hamper, Madurkathi dining set, wedding basket, jewellery box, cane planter) plus 5 collection links under "Who we supply". PASS.
- Artisan wording matches CLAUDE.md (200+ women artisans, community groups, material from where it grows, skills passed down). No "living wages".
- Flags for owner/Sristi (not changed, outside this task): FAQ says "hamper baskets start under ₹500" and the page lists past clients by name; confirm both are approved facts. Theme banner shows "Rated 4.7★ on Google".
Undo: none needed.

## D34 Collection buyer-selection sections (status: live, read back via Admin API)
- /collections/sabai-grass (id 330117316781): appended "Which Sabai piece for which use" (floor basket sizes, lidded basket, storage boxes, desk organiser, gift boxes, planters, table mats) with links; sizes/colours from live variants only.
- /collections/kauna-grass-manipur (id 330117185709): appended "Which Kauna piece for which use" (hamper baskets, jewellery box/tray, trinket box, bedside caddy, planters, handbags). Also corrected a stale sentence "Free shipping across India on orders above ₹1,250" to "orders of ₹1,299 and above" (live Shipping policy says ₹1,299).
- No care instructions written; handoff line "[ASK SRISTI] care details for Sabai and Kauna" added.
Undo: collectionUpdate(collection:{id, descriptionHtml}) with the descriptionHtml in backups/2026-10-30-directives/collections.json (note: this restores the old ₹1,250 sentence; fix that line if restoring).

## D7 Trust block on top 10 products (status: live, read back on 3 of 10 incl. makhana)
Facts verified live first: Shipping policy (free from ₹1,299, ₹120 below; makhana 250 g+ free no minimum, 100 g and hamper standard; COD ₹100 extra), productVariants(query:"taxable:true") returned 0, so no GST on any variant. Block appended at END of descriptionHtml, wrapped in <div class="gc-trust-block"> (heading "Shopping with GrassCrafts"). Selection: Shopify ShopifyQL 90-day orders (only 8 products sold) plus 30-day product landing sessions.
Products (10): Dry Flower Toran 3 ft; Makhana Premium Lotus Seeds; Kauna Embroidered Handbag (8189831315629); Water Hyacinth Rectangular Placemats; Sitalpati Handbag cane handle; Bamboo Cage Pendant Lamp 12x12; Kauna Grass Gift Hamper Basket; Water Hyacinth Rectangular Storage Basket; Kauna Jewellery Display Tray; Cane Planters set.
Makhana block: shipping line reworded (250 g and larger free no minimum; 100 g free from ₹1,299), COD and no-GST lines kept, artisan line omitted (food product).
Undo: productUpdate(product:{id, descriptionHtml}) with the originals in backups/2026-10-30-directives/products.json, or simply delete the <div class="gc-trust-block">...</div> at the end.

## Care blocks on Sabai and Kauna collections (30 Oct, owner-approved)
- Source: owner said "check knowledge article for care". Text taken from blog articles "Kauna Grass: A Sustainable Luxury Material from Manipur" (Caring for Kauna Products) and "Jute vs Water Hyacinth vs Sabai Grass vs Cane" (care table + care list).
- Changed: appended `<div class="gc-care-block">` to the end of /collections/sabai-grass (330117316781) and /collections/kauna-grass-manipur (330117185709). Nothing else changed. Read back via Admin API: OK.
- Backup/undo: backups/2026-10-30-care/README.md. Undo = delete the gc-care-block div from each description.
