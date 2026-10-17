# Website check: grasscrafts.com, 17 Oct 2026

**Scope:** appearance, set-up, menu, blocks, tiles, colour, backlinks and authority.

**Method:** a live fetch of the home page, all 64 internal links on it and a product page, plus the live theme 189377052845 (settings_data, templates) and the Admin API (collections).

**No changes made.** Fixes are proposed below, to be built in a draft theme copy after the owner says go (notify, back up, change).

## Working fine
- All 64 internal links from the home page return 200, with no redirect chains.
- Fonts are consistent: Playfair Display for headings, Lora for body text.
- The core palette is on-brand: cream #faf8f5, brown #3e2723, leaf green #6b8e4e buttons.
- Home-page order makes sense: hero, then promise, then Google reviews, then products, then materials, then contact.
- Canonical, sitemap and robots are fine. All 47 collections have an SEO title and description.

## Problems found (priority order)

| # | Area | Finding | Fix |
|---|---|---|---|
| 1 | Claim | The home "Material Edit" says Sitalpati is "GI-tagged". The GI registry shows application 901 "Cooch Behar Sitalpati" as *Advertised*, not registered. | Change to "Bengal's most refined weave" and drop "GI-tagged". (Madurkathi GI 567 is correct.) |
| 2 | Colour | 20 colour schemes. Five are leftovers with neon gradients (pink/red, cyan/magenta/yellow, orange/pink) or red text. Schemes 3–5 have near-white text (#efecec) on cream, so any block set to them is invisible. The hero banner uses a purple scheme (#46296e), which is off-palette. | Move the hero to the brand scheme and delete the 8 unused or broken schemes. Keep 6 schemes: cream, white, soft earthy, forest-green bar, dark footer, button. |
| 3 | Tiles | 26 of 47 collections have **no collection image**, including Cane, Sabai, Planters, Corporate Gifts, Cane Planters, Wall Plates, Table Mats and Jute Mats, so tiles and menu cards show a blank or a random product. | Set a collection image for each (best product photo). Admin API, no theme change. |
| 4 | Blocks | The home "New Arrivals" block shows 8 bamboo pendant lamps in a row. "The Earth Edit" shows a **sold-out** product first. "Most Loved" shows "Only 2 left" on every card. | Mix New Arrivals across categories, and sort Earth Edit so in-stock items come first. Keep low-stock only when true (it is inventory-driven). |
| 5 | Blocks | index.json carries 5 disabled sections plus one empty `_blocks` section (dead weight in the editor). | Remove the empty section; leave the disabled ones (backup) or delete them after 30 days. |
| 6 | Menu | 27 links in the mega menu. "Shop by Material" goes to /search, not a page. **Sitalpati is missing** from the materials list, although the home page links to it. Five "Earth Edit —" sub-collections duplicate category lists. "MAKHANA" is a top-level item in capitals, next to decor. | Make "Shop by Material" link to /collections/all (or a materials page) and add Sitalpati. Group Earth Edit under one heading. Move Makhana under "Gifting / Gourmet" in title case. After Diwali (8 Nov) swap "Diwali Gift Hampers" for "Wedding Season" and then "Christmas & New Year". |
| 7 | Tiles / names | Messy collection titles show on tiles and as H1: "Chic Planters for Every Home \| Stylish and **Elegent** Designs"; "Christmas Collection \| Celebrate with Handcrafted Fashion…" (handle festival-collection); "Handcrafted Asana Mats \| Elegant & Functional…"; "Handcrafted Genuine Leather Bags" (2 products, off-brand). | Retitle to short names (SEO titles are already set separately): "Planters", "Festive & Christmas", "Asana Mats". Decide whether to unpublish Leather. |
| 8 | Cards | `show_vendor` is on, so every product card says "GrassCrafts", and many titles already contain "GrassCrafts" too ("GrassCrafts Handwoven Bamboo…", "… \| GrassCrafts"). | Turn off the vendor on cards. Strip the brand from product titles in batches (the SEO title keeps it). |
| 9 | Reviews | The product page carries **two review systems**: Klaviyo Reviews (badge and widget) and Judge.me (badge, widget and the Google strip). | Keep Judge.me and remove the Klaviyo review blocks. |
| 10 | Speed | 11 app embeds load on every page: Inbox chat, Klaviyo, UpPromote ×2, Instafeed, AVADA, Notify-me, Wishlist ×2, POWR slider, Judge.me, Clarity. The home page has 88 script tags, and the HTML is 490 KB. | Switch off the POWR slider, Instafeed and UpPromote (unused) and the Wishlist collections embed. That removes about 6 scripts per page. App settings belong to the owner, so the owner decides. |
| 11 | Schema / social | The Organization schema says name "grasscrafts.com", email null, and an old leaf logo. It appears twice (theme and AVADA). og:image is an old 2025 photo over http. The brand text says "since 2015 … Straw, **Seagrass**…". | Set the name to "GrassCrafts" with the sristi@ email and the current logo. Upload a share image in Theme settings. Fix the brand text (does GrassCrafts sell seagrass? if not, drop it). |
| 12 | A11y | The hero image has an empty alt. | Add alt text: "Handwoven Kauna and Sabai grass baskets – GrassCrafts". |

## Backlinks and authority
- **Ahrefs:** domain rating and backlinks need a paid plan ("Insufficient plan"). PageSpeed's free daily quota was used up today. So I have **no DR number** and won't guess one.
- **Web search:** no third-party page mentions grasscrafts.com or "GrassCrafts by Abalone". Authority is effectively **very low**: few or no referring domains. Competitors such as iTokri, Jaypore and Memeraki are cited by craft blogs.
- **Brand mismatch:** the social links point to "abalonehomedecor" (Facebook) and "abalonedesignstudio" (YouTube). Google can't easily tie them to GrassCrafts.

### Free authority plan (honest links only; no buying links, no PBNs)
1. **Google Search Console:** verify the domain, submit the sitemap and read the Links report. This gives real backlink data for free. Ahrefs Webmaster Tools is free too, once Search Console is verified.
2. **Directory listings with the same name, address and phone (NAP) everywhere:**
   - business directories: Justdial, IndiaMART, TradeIndia, Sulekha;
   - Google Business Profile (already done);
   - Bing Places and Apple Business Connect.
3. **Craft and government listings:** the Ministry of Textiles / Development Commissioner (Handicrafts) artisan pages, the GI-craft portals for Madurkathi (GI 567), and Biswa Bangla / India Handmade Bazaar seller pages.
4. **Marketplaces with a brand link:** Jaypore (already being pitched), Okhai, iTokri and Amazon Karigar each give a brand page.
5. **Press and PR:**
   - Kolkata lifestyle press: The Telegraph *t2*, *Times of Kolkata*, *Homegrown*.
   - "Woman-founder Bengal craft" stories built on Sristi's story. Replies to journalist requests through Qwoted and HARO.
6. **Linkable content:**
   - The Journal already has guides (madur mats, wedding return gifts). Add a "Natural fibre comparison chart" and "GI crafts of Bengal". These earn citations from craft blogs.
   - Outreach to 10 craft and sustainability bloggers a week, handled by the Website agent.
7. **Unify social handles:** rename the Facebook page URL and YouTube handle to GrassCrafts where possible. Add sameAs links in the schema.

## Proposed fix pack (after the owner says go)
- **A. No theme change (done through the Admin API, backed up first):**
  - items 3 and 7: collection images and titles;
  - item 6: menu (backup of main-menu taken first);
  - the Sitalpati claim (item 1);
  - item 12: hero alt.
- **B. New draft theme copy, which the owner publishes:**
  - item 2: colour scheme clean-up and hero scheme;
  - item 4: block sorting;
  - item 5: the empty section;
  - item 8: vendor off;
  - item 9: remove the Klaviyo review blocks;
  - item 11: schema and brand text.
- **C. Owner only:** item 10 (app embeds) and the Search Console verification.
