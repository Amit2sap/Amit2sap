# Product image alt text clean-up (17 Oct 2026)

All 208 products were checked (5 pages of Admin GraphQL). 356 product images had their alt text rewritten with `fileUpdate` in 5 batches, all with no userErrors.

## What was changed
- **Weak alts:** empty, one or two generic words ("bag", "Box", "basket", "planter", "MAKHANA", "fridge top cover", "Mat"), or old "X - grasscrafts.com" labels.
- **New pattern:** `<product type and material>[ – <variant colour/style from the product's own variant–image link>][, second view / close-up / styled view] – GrassCrafts`.
  - Colours come only from the variant the image is linked to in Shopify, never from guessing what the photo shows.
- **Wrong brand or text in old alts, now fixed:**
  - "Grassroots brand" (Imperial Sabai laptop tote).
  - "Grassfits.com" (Sabai round storage box).
  - "GrassCrafts by Aaroon" (bamboo hanging lamp).
  - "orr basket" and "WOOVEN" typos.
  - "mother's day gift" on the cane cup planter.
  - "Style A" on the image shared by bed mats Style A and Style B, now neutral.
- **Kept as is:** about 150 alts that already described the scene in a full sentence (lifestyle shots, bamboo lamps, jewellery trays, Majuli/Kaziranga cane planters, the wall plate designs, and the Sabang, Pingla, Tamluk and Kanthi asana mats).

## Not changed / for the owner
- The product "Happy Diwali" (8353899839661) has no images.
- 9 separate products all have the same title, "Handwoven Sabai Grass Wall Plate Decor", so they compete with each other in search. Each needs its own title (and ideally a place-based design name like the 10-design product).
- One storage basket image (30799246852269, Water Hyacinth Storage Basket) is described as a "handbag". Check that the photo belongs to that product.

The old alt values are in the session transcript; they were short generic labels, so restoring them is not recommended.
