# 27 Oct 2026: makhana price and variant changes (owner instruction)
- Bulk Makhana 5 kg (gid://shopify/ProductVariant/67643861041325): ₹5,499 -> ₹7,500 (owner/Sristi WhatsApp, 27 Oct).
- Makhana – Premium Lotus Seeds: NEW variant "100 gm" (gid://shopify/ProductVariant/67707492597933), ₹199, no tax, stock 6 tracked, placed first (order now 100 gm / 250 gm / 500 gm / 1 kg). Other prices unchanged (₹499 / ₹849 / ₹1,599).
- Shipping NOT changed: the 100 gm variant is in the General profile (₹120 below ₹1,299, free from ₹1,299); the other makhana variants stay in "MAKHANA - shipping included". Owner to decide (handoff).
- Backup: backups/products/makhana_prices_before_2026-10-27.json. Undo: productVariantsBulkUpdate price 5499.00 on the bulk variant; productVariantsBulkDelete the 100 gm variant.
- To update after the owner's shipping decision: llms.txt (live theme, sizes and "always ship free" line), FAQ/shipping page wording.

## Shipping wording (owner decision 27 Oct: keep ₹120 for the 100 g pack)
- Updated live: FAQ page (gid://shopify/Page/101703811245), makhana product description (adds 100 g to sizes), makhana collection description (adds 100 g ₹199, bulk 5 kg ₹7,500, new shipping wording in text and FAQ). Wording: "Makhana packs of 250 g and larger ship free ... The 100 g pack ships free on orders of ₹1,299 and above (₹120 below that)."
- Backup: backups/pages/makhana_shipping_text_before_2026-10-27.json. Undo: restore those three bodies.
- Owner to paste: seo/shipping_policy_2026-10-27.txt into Settings > Policies > Shipping policy (API has no policy scope).
- Theme (needs an unpublished copy, owner publishes): llms.txt.liquid sizes/shipping line; gc-free-shipping-bar.liquid treats every makhana-tagged item as free, so a cart with only the 100 g pack would wrongly show "Makhana ships FREE".
