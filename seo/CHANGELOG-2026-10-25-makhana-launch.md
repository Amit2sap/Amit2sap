# 2026-10-25 Makhana launch + inventory and shipping fixes (owner request)
Backups: backups/products/makhana_before_2026-10-25.json, backups/pages/faq_shipping_before_2026-10-25.txt, backups/theme/gc-free-shipping-bar_before_2026-10-25.liquid (+ earlier gc-product-trust / llms backups).

## Products (live now)
- Makhana Gift Hamper (15265744486573): sizes renamed Small (100 g) ₹649 / Large (250 g) ₹949; description rewritten (placeholders removed, facts only: basket sizes from the lidded basket product); SEO title/description; tags; stock tracked 2 + 2; 3 real photos (basket main image, makhana, basket sizes) + the existing makhana photo; ACTIVE; published to Online Store, POS, Google & YouTube, Inbox, Facebook & Instagram, Pinterest; in Makhana collection. Shipping: General profile (₹120 below ₹1,299).
- Bulk Makhana (15265744683181): 1 kg variant deleted (would undercut retail 1 kg ₹1,599); 5 kg (5 x 1 kg) ₹5,499 only; stock tracked 1; description rewritten; tag makhana-free-shipping; moved to delivery profile "MAKHANA - shipping included" (free, no minimum); 2 photos added (duplicate removed); ACTIVE; same channels; in Makhana collection.
- Main makhana (8622201995437): tag makhana-free-shipping added; description shipping sentence -> "Makhana packs ship free across India, with no minimum order." + links to hamper and bulk.
- Makhana collection: pack list adds bulk and hamper; shipping sentence and FAQ now state makhana packs ship free, hamper follows standard rates.
- FAQ page: ₹1,300 -> ₹1,299 and makhana free-shipping sentence.
Undo: products -> status DRAFT; restore descriptions from backups; deliveryProfileUpdate variantsToDissociate 67643861041325; tagsRemove makhana-free-shipping.

## Inventory fixes
- Cane flower vase Small (variant 45396070727853): -1 -> 0 (oversold correction).
- Toran (4 variants) still NOT tracked: admin shows 0 but the site sells unlimited. Needs owner stock count.

## Theme (owner to publish): "Grasscrafts – makhana + shipping fix 25 Oct" (189623959725, was "toran + llms 23 Oct")
Reused because the shop is at the 20-theme limit. Made identical to live 189658235053 (config/settings_data.json copied, checksum 45266ecf… verified; all other config/templates/sections/layout/gc-snippets identical), then:
- snippets/gc-product-trust.liquid (md5 4646f178…): products tagged makhana-free-shipping show "Free shipping across India, no minimum"; others keep "from ₹1,299".
- snippets/gc-free-shipping-bar.liquid (md5 55f9b403…): threshold ₹1,300 -> ₹1,299 (129900); makhana lines excluded from the progress total; makhana-only cart shows "Makhana ships FREE across India".
- templates/llms.txt.liquid (md5 827bc2f9…): makhana free-shipping rule + hamper and bulk links.
Undo after publish: publish 189658235053 ("Grasscrafts – COD ₹100 24 Oct") again.

## Shipping policy (owner to paste; no API scope)
seo/shipping_policy_2026-10-25.txt: "Makhana packs (250 g, 500 g, 1 kg and the 5 kg bulk pack) ship free, with no minimum. The makhana gift hamper follows the standard rates above."

## Verified live 25 Oct
- Owner published 189623959725 ("Grasscrafts – makhana + shipping fix 25 Oct"); live checksums: settings_data 45266ecf…, gc-free-shipping-bar 55f9b403…, gc-product-trust 4646f178…, llms 827bc2f9…. Undo: publish 189658235053.
- Shipping policy live with: "Makhana packs (250 g, 500 g, 1 kg and the 5 kg bulk pack) ship free, with no minimum. The makhana gift hamper follows the standard rates above."
