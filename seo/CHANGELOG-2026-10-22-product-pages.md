# Product pages: SEO descriptions + extra photos (22 Oct 2026)

Owner request (Amit, 22 Oct 2026). Before-state backup: `backups/products/seo_and_media_before_2026-10-22.json`.

## Part A: SEO (meta) descriptions set on 73 products

All 73 ACTIVE products that had an empty SEO description now have one (140-158 characters, written from each product's own title and description; no prices, no invented specs). Each ends with one true buying cue: "Handwoven in India", "Free shipping over ₹1,299" or "Cash on Delivery available".

How it was set: `productUpdate(product:{id, seo:{title, description}})`. **Note:** sending `seo{description}` alone clears the SEO title (seen on the first product, `willingdon-tote-hand-woven-grass-bag`, and restored right away), so every call re-sent the existing SEO title unchanged. Titles and body text were not changed.

Before state: `backups/products/seo_and_media_before_2026-10-22.json` (key `seo`): every one had description = null.

Undo (one product): `productUpdate(product:{id:"<id>", seo:{title:"<seo_before.title from backup>", description:""}})`. Always re-send the title.

| Handle | New SEO description | Chars |
|---|---|---|
| `willingdon-tote-hand-woven-grass-bag` | The Willingdon Tote, a structured, roomy bag hand-woven from natural Sabai grass for work, travel and gifting. Handwoven in India. Cash on Delivery available. | 158 |
| `handwoven-cane-tray-desk-organizer` | Handwoven natural cane tray with built-in compartments to organise a desk, table or countertop, or to use as a serving tray. Free shipping over ₹1,299. | 151 |
| `handwoven-cane-storage-basket` | Handwoven natural cane storage basket for towels, groceries, linens and everyday essentials in the bathroom, kitchen or living room. Handwoven in India. | 152 |
| `tissue-box-1` | The Woven Tissue Keeper: a handcrafted natural grass tissue box cover that also works as a jewellery or storage box for eco decor. Handwoven in India. | 150 |
| `bed-runner` | Natural straw mat, 7 x 4.5 ft, for bed, yoga, floor or outdoor use. The breathable open weave stays cool to the touch. Handwoven in India by skilled artisans. | 158 |
| `bed-runner-1` | Handcrafted natural straw bed mat, 7 x 4.5 ft, with a breathable open weave for cooler sleep. Use as a bed, floor or sleeping mat. Free shipping over ₹1,299. | 157 |
| `bed-runner-2` | Natural straw bed mat and yoga mat, 7 x 4.5 ft. A breathable open weave for cool rest or practice, indoors or outdoors. Cash on Delivery available in India. | 156 |
| `bed-runner-3` | Natural straw bed mat, 7 x 4.5 ft, lightweight and breathable for warm nights. Use it as a sleeping, floor or outdoor mat. Handwoven in India by artisans. | 154 |
| `handmade-eco-friendly-straw-tote-bag` | Handwoven natural straw tote bag made from grass fibres. A lightweight, roomy carry for shopping, travel, beach days and gifting. Free shipping over ₹1,299. | 156 |
| `madurkathi-dining-suite` | Madurkathi grass dining suite: one 60 x 12 in table runner and six 18 x 12 in mats in deep crimson with geometric borders and tassels. Handwoven in India. | 154 |
| `handwoven-cane-picnic-basket` | Handwoven rattan picnic basket with a sturdy handle, 15 x 10 x 11 in. Light to carry on outings and handsome as home storage. Cash on Delivery available. | 153 |
| `yoga-mats` | Madurkathi quilted yoga and meditation mat, 6 x 3 ft. Dual-sided: cool Madurkathi grass on one side, soft cotton on the other. Handwoven in India. | 146 |
| `quilted-bed-mats-6` | Madurkathi quilted 3-fold bed mat, Style D, 6 x 4.5 ft: natural grass with indigo block-print stripes and amber bands, cotton reverse. Handwoven in India. | 154 |
| `asana-mats-1` | Dual-sided Madurkathi grass asana mat, 23 x 18 in, sky blue and burgundy stripes, purple floral border, quilted cotton back, for puja. Handwoven in India. | 154 |
| `asana-mats` | Dual-sided Madurkathi grass asana mat, 23 x 18 in: forest green and burgundy stripes with a batik border and quilted cotton back. Cash on Delivery available. | 157 |
| `puja-mats` | Madurkathi puja and asana mat, Sabang design, 23 x 18 in. Dual-sided: handwoven grass on one side, quilted cotton on the other. Cash on Delivery available. | 155 |
| `puja-mats-1` | Madurkathi puja and asana mat, Pingla design, 23 x 18 in, with two usable sides, handwoven grass and quilted cotton, for puja and yoga. Handwoven in India. | 155 |
| `meditation-mats` | Madurkathi grass asana mat, 23 x 18 in: natural and black diamond stripes, navy paisley border and quilted cotton back, for puja. Handwoven in India. | 149 |
| `puja-mats-2` | Madurkathi puja and asana mat, Tamluk design, 23 x 18 in. Grass on one side, quilted handloom cotton on the other, for daily puja. Free shipping over ₹1,299. | 157 |
| `puja-mats-3` | Madurkathi puja and asana mat, Kanthi design, 23 x 18 in, with handwoven grass and quilted cotton sides for puja and meditation. Cash on Delivery available. | 156 |
| `asana-mats-2` | Madurkathi grass asana mat, 23 x 18 in, sky blue and red stripes with a yellow Warli folk-art border and quilted cotton back. Free shipping over ₹1,299. | 152 |
| `meditation-mats-2` | Madurkathi grass asana mat, 23 x 18 in: black diamond stripes, yellow and red paisley border, quilted cotton back for puja or meditation. Handwoven in India. | 157 |
| `meditation-mats-3` | Madurkathi grass asana mat, 23 x 18 in, natural white with multicolour stripes, black and gold paisley border and cotton back. Cash on Delivery available. | 154 |
| `quilted-bed-mats-3` | Madurkathi quilted 3-fold bed mat, Style C, 6 x 4.5 ft: terracotta and natural stripes with a floral block-print border, cotton reverse. Handwoven in India. | 156 |
| `quilted-bed-mats-4` | Madurkathi quilted 3-fold bed mat, Style B, 6 x 4.5 ft: grey-blue grass with a black and cream paisley cotton border. Folds flat. Free shipping over ₹1,299. | 156 |
| `quilted-bed-mats-5` | Madurkathi quilted 3-fold bed mat, Style A, 6 x 4.5 ft: lavender-blue grass weave, pink floral cotton border. Bed, floor or yoga mat. Handwoven in India. | 153 |
| `double-sided-nap-mats` | Double-sided Madurkathi nap mat, 6 x 4.5 ft: cool grass on one face, soft cotton with a navy and teal floral border on the other. Cash on Delivery available. | 157 |
| `sabai-grass-round-basket-planter` | Handwoven Sabai grass round basket, 12 x 12 x 6 in, in natural beige and green. Use it as a planter cover or a storage basket. Free shipping over ₹1,299. | 153 |
| `cane-planters-4` | The Cane Atelier Planter: a hand-woven cane planter, 12 in high and 15 in wide, for home, office or terrace, or as handy storage. Handwoven in India. | 149 |
| `handwoven-cane-planter-set` | Handwoven natural cane planters in small (8 in), medium (10 in), large (12 in) or a set of 3, for indoor plants and housewarming gifts. Handwoven in India. | 155 |
| `handwoven-cane-round-tray-kadai-basket-set-of-3` | Set of 3 handwoven cane kadai-shape round trays with handles (8, 10 and 12 in) for fruit, desk, kitchen or decor use. Cash on Delivery available in India. | 154 |
| `handwoven-cane-storage-basket-with-handle` | Handwoven natural cane storage basket with a sturdy handle, 10 x 8 x 4 in, for towels, groceries, linens or essentials. Free shipping over ₹1,299 in India. | 155 |
| `kash-grass-bird-basket-planter` | Bird-shaped Kash grass basket with a net-top lid, 12 x 7 x 5 in, in natural beige, for use as a planter, fruit basket or decor piece. Handwoven in India. | 153 |
| `kash-grass-net-top-round-basket` | Handwoven Kash grass round basket with a net-pattern lid, 10 in wide and 4 in high, natural beige, for fruit, bread or storage. Cash on Delivery available. | 155 |
| `kash-grass-net-top-basket-12x6` | Handwoven Kash grass rectangular basket with a net-top lid, 12 x 6 x 4 in, natural beige, for bread, fruit or decorative storage. Free shipping over ₹1,299. | 156 |
| `kash-grass-rectangular-tray-12x10` | Large Kash grass rectangular tray, 12 x 10 x 2.5 in, in natural beige. A serving tray, coffee table centrepiece or kitchen organiser. Handwoven in India. | 153 |
| `kash-grass-rectangular-basket-tray-10x8` | Kash grass rectangular basket tray, 10 x 8 x 2.5 in, in warm natural beige, for serving, desk organising or decor. Cash on Delivery available in India. | 151 |
| `kash-grass-round-basket-tray-10in` | Round Kash grass basket tray, 10 in wide and 3 in high, natural beige, to use as a fruit bowl, desk organiser or decor accent. Free shipping over ₹1,299. | 153 |
| `kash-grass-wedding-gift-hamper-basket` | Handwoven Kash grass wedding gift hamper basket in natural tones, roomy for curated gifts and reusable for storage later. Handwoven in India by artisans. | 153 |
| `madurkathi-grass-table-mats-runner-terracotta-black-multi-band` | Madurkathi grass table mats (17 x 12 in) and 48 in runner in terracotta and black bands with a red border, in sets of 4 or 6 mats. Handwoven in India. | 150 |
| `madurkathi-grass-table-mats-runner-micro-diamond-lattice` | Madurkathi grass table mats (17 x 12 in) and runner (48 x 12 in) in a black and natural micro-diamond lattice. Sets of 4 or 6. Cash on Delivery available. | 154 |
| `madurkathi-grass-table-mats-runner-vertical-pinstripe-black-natural` | Madurkathi grass table mats (17 x 12 in) and 48 in runner with fine black and natural pinstripes for modern dining. Sets of 4 or 6. Free shipping over ₹1,299. | 158 |
| `madurkathi-grass-table-mats-runner-burgundy-herringbone` | Madurkathi grass table mats (17 x 12 in) and runner (48 x 12 in) in deep burgundy with a cream herringbone stripe. Sets of 4 or 6 mats. Handwoven in India. | 155 |
| `madurkathi-grass-table-mats-runner-checkerboard-weave-rounded` | Madurkathi grass table mats with rounded corners in a black and natural checkerboard weave, 17 x 12 in, plus a 48 in runner. Cash on Delivery available. | 152 |
| `madurkathi-grass-table-mats-runner-striped-herringbone-grey-burgundy` | Madurkathi grass table mats (17 x 12 in) and 48 in runner in grey striped herringbone with a burgundy band, in sets of 4 or 6. Free shipping over ₹1,299. | 153 |
| `madurkathi-grass-table-mats-runner-set-diamond-weave` | Madurkathi grass table mats in a natural diamond weave with a black border, 17 x 12 in, in sets of 4 or 6 or with a 48 x 12 in runner. Handwoven in India. | 154 |
| `kauna-grass-handbag-resilience-grace` | Kauna grass handbag made by women artisans in Manipur: lightweight, structured and golden-toned for everyday carry, travel and gifting. Handwoven in India. | 155 |
| `kauna-grass-embroidered-handbag-artisan` | Kauna grass embroidered handbag with smooth cane handles, lightweight and structured for everyday carry, travel or gifting. Cash on Delivery available. | 151 |
| `handwoven-cane-ottoman` | Handwoven solid cane ottoman (morah) with a spiral top, 15 in high and 14 in wide, for floor seating, a side table or plant stand. Handwoven in India. | 150 |
| `cane-stool` | The Cane Perch: a solid cane stool with a handwoven spiral seat, 12.5 in diameter, for balcony, tea corner or floor seating. Free shipping over ₹1,299. | 151 |
| `handwoven-cane-ottoman-morah` | Solid cane morah ottoman with a handwoven spiral seat, 15 in high, 14 in diameter, sold single or as a pair, for seating or decor. Cash on Delivery available. | 158 |
| `handwoven-ottomans-3` | The Grasscrafts Ottoman: an apple-shaped stool in solid cane with a handwoven spiral seat, 14 in diameter, for low seating and decor. Handwoven in India. | 153 |
| `kauna-grass-gift-hamper-basket` | Petite round Kauna reed gift hamper basket, 6 in wide, 4 in high, with a lattice weave and braided handle for wedding and festive gifts. Handwoven in India. | 156 |
| `sabai-grass-lidded-basket-wooden-handle` | Sabai grass basket with a net-pattern lid and wooden handle in small, medium or large, for bread, fruit, gifting or storage. Free shipping over ₹1,299. | 151 |
| `laundry-storage` | Sabai Grand Floor Basket, 20 in high and 14 in wide, in an emerald and natural weave, for laundry, throws or yoga mats. Handwoven in India by artisans. | 151 |
| `straw-tote-bag-2` | The Harvest Tote: a handwoven natural straw shoulder bag in golden-brown tones with woven handles, for markets and errands. Cash on Delivery available. | 151 |
| `handwoven-natural-straw-tote-bag` | Handwoven natural straw tote bag of grass fibres, light yet sturdy for shopping, markets, beach days, travel and gifting. Free shipping over ₹1,299. | 148 |
| `grande-tote-bag-handwoven` | Sabai Grande: a large, open-weave tote bag hand-woven from natural Sabai grass, roomy enough for a full day out, travel or the beach. Handwoven in India. | 153 |
| `verdant-heirloom-handcrafted-sabai-basket` | The Verdant Heirloom: a Sabai grass basket on an iron frame, 12 x 9.5 x 6 in, in forest green and natural, for textiles or blooms. Cash on Delivery available. | 158 |
| `square-kauna-grass-gift-hamper-basket` | Square Kauna grass gift hamper basket, 7 x 7 x 5 in, with a braided handle and crisscross weave, for weddings and festive gifting. Handwoven in India. | 150 |
| `nilachal-madurkathi-dining-set` | The Nilachal Suite: Madurkathi grass runner (60 x 12 in) and six 18 x 12 in placemats in teal-blue with a burnt-orange border. Free shipping over ₹1,299. | 153 |
| `handwoven-bamboo-gift-basket-black` | Bamboo gift basket, 7.5 x 7.5 x 3 in, in a geometric diamond weave, black or maroon, for gift hampers, festive gifting and storage. Handwoven in India. | 151 |
| `handwoven-bamboo-serving-tray` | Handwoven bamboo serving tray, 15 x 12 x 1.5 in, with a solid bamboo frame, in teal blue or black, for serving or coffee tables. Cash on Delivery available. | 156 |
| `handwoven-bamboo-puja-tray` | Handwoven bamboo puja tray, 14 x 9 x 2 in, with a solid frame and handles, in green, black or maroon, for diyas and offerings. Free shipping over ₹1,299. | 153 |
| `handwoven-square-bamboo-tray-set-of-3` | Set of 3 square bamboo trays (8, 11 and 14 in) with a chevron weave and maroon bamboo frame, for Rakhi, puja, festive decor and styling. Handwoven in India. | 156 |
| `handwoven-bamboo-pendant-lamp-eco-friendly-woven-ceiling-light` | Handwoven bamboo pendant lamp, 18 in high and 12 in wide, in a diamond lattice that casts patterned light on walls and ceiling. Cash on Delivery available. | 155 |
| `handwoven-bamboo-dome-pendant-lamp-wide-woven-ceiling-light` | Wide handwoven bamboo dome pendant lamp, 10 in high and 17 in across, for dining tables, kitchen islands and low ceilings. Free shipping over ₹1,299. | 149 |
| `handwoven-bamboo-bell-pendant-lamp-tapered-artisan-ceiling-light` | Tapered bamboo bell pendant lamp, 12 x 12 in, hand-woven in an open lattice that casts soft shadow patterns, for cosy corners and tables. Handwoven in India. | 157 |
| `handwoven-bamboo-two-tier-drum-pendant-lamp-double-layer-woven-ceiling-light` | Two-tier bamboo drum pendant lamp, 12 in high and 17 in wide, with a double woven layer for dining and living rooms. Cash on Delivery available in India. | 153 |
| `handwoven-bamboo-hanging-lamp-21-inch-dome` | Low-profile bamboo hanging lamp, 21 in wide and 5 in high, for dining tables, counters, cafes and hotels. Fits a standard pendant fitting. Handwoven in India. | 158 |
| `handwoven-bamboo-layered-pendant-lamp-15x14` | Layered bamboo pendant lamp, 15 in high and 14 in wide, with a tiered woven lattice shade for dining, lounge and reception spaces. Free shipping over ₹1,299. | 157 |
| `handwoven-bamboo-globe-pendant-lamp-11x18` | Bamboo globe pendant lamp, 11 in high and 18 in wide, with a fine lattice weave for a soft patterned glow over dining tables. Cash on Delivery available. | 153 |
| `handwoven-bamboo-cage-pendant-lamp-12x12` | Bamboo cage pendant lamp, 12 x 12 in, with an open vertical weave that frames the light, for homes, dining rooms, cafes and hotels. Handwoven in India. | 151 |

## Part B: extra product photos from own channels

In progress (see below).
