"""SEO rewrite for grasscrafts.com products that had no SEO title.

Builds seo_updates.json: one entry per product with an optional new title,
an SEO title (<=60 chars), a meta description (<=155 chars) and, for products
whose description was thin or generic, a rewritten description.

Facts (materials, sizes) are taken only from each product's existing
description. Handles (URLs) are never changed, so existing links keep working.
"""
import json
from pathlib import Path

CARE = "Wipe with a dry or slightly damp cloth. Keep away from prolonged moisture and direct heat; air-dry in shade if it gets wet."


def desc(intro, bullets, details=None, use=None, care=CARE, note="Handmade by Indian artisans — slight variations in weave, colour and size make every piece one of a kind."):
    html = f"<p>{intro}</p>\n<h3>Why you'll love it</h3>\n<ul>\n"
    html += "".join(f"<li>{b}</li>\n" for b in bullets)
    html += "</ul>\n"
    if details:
        html += "<h3>Details</h3>\n<ul>\n" + "".join(f"<li>{d}</li>\n" for d in details) + "</ul>\n"
    if use:
        html += f"<h3>Perfect for</h3>\n<p>{use}</p>\n"
    html += f"<h3>Care</h3>\n<p>{care}</p>\n"
    html += f"<p><em>{note}</em></p>"
    return html


HANDMADE = "Handwoven by skilled Indian artisans — every piece is unique"
ECO = "Natural, biodegradable fibre — plastic-free and eco-friendly"

U = {}  # product numeric id -> dict(title, seo_title, seo_desc, desc)

# ---------- Bags ----------
U["7877505941677"] = dict(
    title="Sabai Grande Tote Bag | Handwoven Sabai Grass Laptop Tote | 15 x 15 in",
    seo_title="Sabai Grass Laptop Tote Bag | Handwoven | GrassCrafts",
    seo_desc="Handwoven Sabai grass tote with sun-burst weave and dark-finish handles. 15x15 in, fits a slim laptop. Eco-luxury work bag, handmade in India.")
U["7877515477165"] = dict(
    title="Handmade Straw Crossbody Sling Bag | Eco-Friendly Natural Fibre Bag",
    seo_title="Straw Crossbody Sling Bag | Handmade Eco Bag | GrassCrafts",
    seo_desc="Lightweight handmade straw crossbody sling bag for daily use and outings. Sustainable natural-fibre fashion, handcrafted by Indian artisans.",
    desc=desc("A lightweight, handcrafted straw crossbody sling bag that pairs with everything from a summer dress to everyday denim — sustainable fashion you'll actually reach for daily.",
              ["Hands-free crossbody design for errands, travel and day outings", "Lightweight yet durable natural straw weave", HANDMADE, ECO],
              use="Daily carry, holidays, brunches and gifting to someone who loves sustainable fashion."))
U["7885429473453"] = dict(
    title="Green Straw Sling Bag | Detachable Crossbody Strap | Handmade Eco Purse",
    seo_title="Green Straw Sling Bag with Crossbody Strap | GrassCrafts",
    seo_desc="Handmade green straw sling bag with detachable crossbody strap and secure closure. Breathable, lightweight, eco-friendly. Shop at GrassCrafts.")
U["7912309948589"] = dict(
    title="Handwoven Straw Jali Tote Bag | Mesh Weave Shopping & Office Bag",
    seo_title="Straw Jali Tote Bag | Handwoven Shopping Bag | GrassCrafts",
    seo_desc="Handwoven natural straw tote with Jali (mesh) design. Multipurpose bag for shopping, office and daily use. Eco-friendly, handmade in India.",
    desc=desc("Our handwoven straw tote features a traditional Jali (mesh) weave — airy, light and strong enough for daily shopping, office runs and lunch.",
              ["Open Jali (mesh) weave in natural straw", "Roomy, multipurpose tote for shopping, office or lunch", "A reusable, plastic-free alternative to carry bags", HANDMADE],
              use="Market days, office, college and as an affordable eco-gift."))
U["7988441252013"] = dict(
    title="Handmade Straw Satchel Handbag | Genuine Leather Handles | Crossbody",
    seo_title="Straw Satchel Handbag with Leather Handles | GrassCrafts",
    seo_desc="Handmade straw satchel with genuine leather handles and detachable strap. 13x9x5 in, lined, with zip compartments. Customisable eco handbag.")
U["7988462813357"] = dict(
    title="Imperial Sabai Laptop Tote – Burnt Orange | Leather Handles | 13 x 12 in",
    seo_title="Burnt Orange Sabai Grass Laptop Tote | GrassCrafts",
    seo_desc="Handwoven burnt-orange Sabai grass tote with leather handles, brass hardware and zip lining. 13x12x5 in, fits a laptop. Handmade in India.")
U["8036291412141"] = dict(
    title="Sovereign Sabai Shoulder Bag | Golden Yellow Handwoven Grass Bag",
    seo_title="Golden Sabai Grass Shoulder Bag | Handwoven | GrassCrafts",
    seo_desc="Handwoven golden-yellow Sabai grass shoulder bag with leather handle, brass hardware and zip lining. 12x6x4 in. Artisan luxury, made in India.")
U["8036292722861"] = dict(
    title="Handmade Straw Tote Bag | Genuine Leather Handles | 13 x 12 in",
    seo_title="Straw Tote Bag with Leather Handles | Handmade | GrassCrafts",
    seo_desc="Handmade straw tote with genuine leather handles, wearable crossbody or by hand. 13x12x5 in. Customisable colours. Eco-friendly, made in India.")
U["8145616044205"] = dict(
    title="Handmade Straw Laptop Bag | Eco-Friendly Office Bag for Women",
    seo_title="Straw Laptop Bag | Handmade Eco Office Bag | GrassCrafts",
    seo_desc="Lightweight, durable handmade straw laptop bag for work and outings. Holds your laptop and essentials. Sustainable office bag, made in India.",
    desc=desc("A handmade straw laptop bag that makes your workday more sustainable — lightweight on the shoulder, sturdy enough for your laptop and daily essentials.",
              ["Sized for a laptop plus everyday essentials", "Lightweight yet durable natural straw", "Goes from office to casual outings", HANDMADE],
              use="Office, college, co-working days and a thoughtful gift for working professionals."))
U["8146745917613"] = dict(
    seo_title="Shell-Adorned Kauna Grass Tote Bag | GrassCrafts",
    seo_desc="Hand-woven Kauna reed tote adorned with genuine seashells and pearlescent accents. A wearable piece of coastal art, handmade in India.")

# ---------- Boxes ----------
U["7881405530285"] = dict(
    title="Cane Cylindrical Multipurpose Box | Handmade Tissue & Jewellery Box",
    seo_title="Handmade Cane Multipurpose Box | Tissue & Jewellery Box",
    seo_desc="Natural cane multipurpose box — use as tissue holder, jewellery box or kitchen storage. Handmade, eco-friendly decor by GrassCrafts.",
    desc=desc("A handmade cane box that does it all — tissue holder on the dressing table, jewellery box in the bedroom or a neat storage piece in the kitchen.",
              ["Crafted from natural cane", "Multipurpose: tissues, jewellery, kitchen or desk storage", "Adds warm, rustic texture to any room", HANDMADE],
              use="Home organisation, housewarming gifts and festive gifting."))
U["7901463937197"] = dict(
    title="Handwoven Sabai Grass Gift Box | Jewellery, Puja & Dry Fruit Box",
    seo_title="Sabai Grass Gift Box for Jewellery, Puja & Dry Fruits",
    seo_desc="Handmade Sabai grass box for jewellery, puja items, chocolates or dry fruits. A reusable, eco-friendly gift box crafted by Indian artisans.",
    desc=desc("A handwoven Sabai grass box made for gifting — fill it with dry fruits, chocolates or puja essentials, and it lives on afterwards as a jewellery or keepsake box.",
              ["Natural Sabai grass, handwoven", "Store jewellery, puja materials, chocolates or dry fruits", "A reusable gift box — no wrapping waste", HANDMADE],
              use="Diwali and festive gifting, return gifts, weddings and corporate hampers."))
U["8058926039213"] = dict(
    title="Sabai Grass Pot-Shaped Box with Lid | Jewellery & Puja Box | 5.5 in",
    seo_title="Sabai Grass Box with Lid | Jewellery & Puja Box | 5.5 in",
    seo_desc="Pot-shaped Sabai grass box with lid (5.5 in H x 5 in dia). Store jewellery, puja items, chocolates or dry fruits. Handmade eco gift box.",
    desc=desc("This pot-shaped Sabai grass box with a fitted lid is a little treasure chest — perfect for jewellery, puja materials, chocolates or dry fruits.",
              ["Pot-shaped silhouette with fitted lid", "Natural Sabai grass", "Doubles as a reusable gift box", HANDMADE],
              ["Height: 5.5 in (with lid)", "Diameter: 5 in"],
              "Festive gifting, return gifts, dressing tables and puja rooms."))
U["8058969948333"] = dict(
    title="Sabai Grass Pot Box with Lid | Custom Colours | Gift & Jewellery Box",
    seo_title="Sabai Grass Pot Box with Lid | Custom Colours | GrassCrafts",
    seo_desc="Pot-shaped Sabai grass box with lid, 5.5 in H x 5 in dia, custom colours available. Ideal for jewellery, puja items or dry-fruit gifting.",
    desc=desc("A pot-shaped Sabai grass box with lid, available in custom colours — ideal for coordinated wedding, festive or corporate gifting.",
              ["Custom colour options available", "Natural Sabai grass with fitted lid", "Holds jewellery, puja items, chocolates or dry fruits", HANDMADE],
              ["Height: 5.5 in (with lid)", "Diameter: 5 in"],
              "Bulk and themed gifting — weddings, Diwali and corporate events."))
U["8126463475885"] = dict(
    title="Handmade Cane Jewellery & Tissue Box | 14 x 7 in Organiser",
    seo_title="Handmade Cane Jewellery & Tissue Box | GrassCrafts",
    seo_desc="Natural cane multipurpose box, 14 x 7 x 5.5 in — jewellery box, tissue box or organiser. Eco-friendly, handmade home decor and gift.",
    desc=desc("A handmade cane box with a clean rectangular form — use it as a jewellery box, a tissue box or a desk organiser.",
              ["Natural cane, handwoven", "Multipurpose: jewellery, tissues, stationery", "Elegant eco-friendly decor piece", HANDMADE],
              ["Length: 14 in", "Width: 7 in", "Height: 5.5 in"],
              "Bedrooms, living rooms, offices and gifting."))
U["8136027766957"] = dict(
    title="Sabai Grass Cube Storage Box | 4 in Mini Gift Box",
    seo_title="Sabai Grass Cube Box | 4 inch Mini Gift Box | GrassCrafts",
    seo_desc="Handmade 4-inch Sabai grass cube box for jewellery, puja items, chocolates or dry fruits. Eco-friendly mini gift box from GrassCrafts.")
U["8138092347565"] = dict(
    title="Round Sabai Grass Gift Box with Lid | Pink, Rust Red & Brown",
    seo_title="Round Sabai Grass Gift Box with Lid | GrassCrafts",
    seo_desc="Handwoven round Sabai grass box in pink, rust red or brown (5 in dia). Store jewellery, puja items, chocolates or dry fruits. Eco gift box.",
    desc=desc("Intricately handwoven from natural Sabai grass, this round box is as lovely to give as it is to keep — for jewellery, puja essentials, chocolates or dry fruits.",
              ["Three colours: Pink, Rust Red and Brown", "Natural Sabai grass with intricate hand weaving", "Reusable gift box and decor piece", HANDMADE],
              ["Pink: 5 in diameter, 5 in height", "Rust Red: 5 in diameter, 6 in height", "Brown: 5 in diameter, 7 in height"],
              "Diwali gifting, return gifts, weddings and dressing tables."))
U["8500966457517"] = dict(
    seo_title="Sabai Grass Round Storage Box | 5 inch | GrassCrafts",
    seo_desc="Hand-coiled Sabai grass box, 5 in x 5 in, geometric pattern with crimson accents. A jewellery box or desk accent. Handmade in India.")
U["8398793244845"] = dict(
    seo_title="Partitioned Cane Organiser Box | Hand-Braided | GrassCrafts",
    seo_desc="Hand-braided partitioned cane box from premium sustainable cane. Organise rituals, tools or heirlooms. A thoughtful handmade gift for her.")

# ---------- Baskets ----------
U["7881425420461"] = dict(
    title="Handwoven Grass Roti Basket | Natural Chapati & Bread Basket",
    seo_title="Handwoven Roti Basket | Natural Grass Chapati Basket",
    seo_desc="Handmade grass roti basket to serve chapatis, bread or snacks. Natural, eco-friendly dining essential and gift, crafted by Indian artisans.",
    desc=desc("Serve rotis, chapatis, bread or snacks in a handwoven natural grass basket — a small switch that brings handmade warmth to every meal.",
              ["Natural grass/straw, handwoven", "Serve rotis, puris, bread or dry snacks", "Breathable weave — no plastic", HANDMADE],
              use="Everyday dining, festive feasts and housewarming gifts."))
U["7901489103021"] = dict(
    title="Sabai Grass Kitchen Basket with Iron Frame | Fruit & Vegetable Basket",
    seo_title="Sabai Grass Kitchen Basket | Fruit & Vegetable Basket",
    seo_desc="Handwoven Sabai grass kitchen basket with a round iron frame for strength. Use as a fruit bowl, veggie basket or storage. Eco-friendly.",
    desc=desc("Handwoven from Sabai grass over a round iron frame, this kitchen basket is sturdier than it looks — made for fruits, vegetables and everyday storage.",
              ["Round iron frame for extra strength", "Natural Sabai grass or straw weave", "Fruit bowl, vegetable basket or storage", HANDMADE],
              use="Kitchens, dining tables and housewarming gifts."))
U["7901513416877"] = dict(
    title="Hexagonal Sabai Grass Desk Organiser | Office Pen & Stationery Holder",
    seo_title="Hexagonal Sabai Grass Desk Organiser | GrassCrafts",
    seo_desc="Handcrafted hexagonal Sabai grass desk organiser with green weave accents. Eco-friendly office decor and a thoughtful corporate gift.")
U["8029737222317"] = dict(
    title="Sabai Grass Storage Basket with Iron Frame | 12 x 12 x 6 in",
    seo_title="Sabai Grass Storage Basket | Fruit Bowl | 12x12 in",
    seo_desc="Handwoven Sabai grass basket on a sturdy iron frame, 12x12x6 in. Use as a fruit bowl, storage basket or decor. Eco-friendly, handmade.",
    desc=desc("A handwoven Sabai grass basket reinforced with a sturdy iron frame — beautiful as a fruit bowl, useful as everyday storage.",
              ["Iron frame for strength and shape", "Natural Sabai grass or straw", "Fruit bowl, storage or decor", HANDMADE],
              ["Size: 12 in x 12 in x 6 in"],
              "Kitchens, living rooms and gifting."))
U["8060350988461"] = dict(
    title="Large Cane Laundry Basket with Lid | 16 in x 14 in Storage Basket",
    seo_title="Cane Laundry Basket with Lid | 16 x 14 in | GrassCrafts",
    seo_desc="Handmade natural cane storage basket with lid, 16 in H x 14 in dia. For laundry, blankets or household items. Eco-friendly home storage.",
    desc=desc("A large handmade cane basket with lid that keeps laundry, blankets and household items out of sight — in style.",
              ["Natural cane with a fitted lid", "Laundry, blankets, toys or household storage", "Rustic yet refined look for any room", HANDMADE],
              ["Height: 16 in", "Diameter: 14 in"],
              "Bedrooms, bathrooms and housewarming gifts."))
U["8060390899885"] = dict(
    title="Tall Cane Laundry Basket with Lid | 26 in Storage Hamper",
    seo_title="Tall Cane Laundry Basket with Lid | 26 inch | GrassCrafts",
    seo_desc="Tall handmade cane laundry basket with lid, 26 in high. Store laundry, blankets or linens. Natural, eco-friendly storage hamper.",
    desc=desc("A tall, spacious cane basket with lid — a laundry hamper that looks like a piece of decor.",
              ["Natural cane with a fitted lid", "Generous capacity for laundry, blankets and linens", HANDMADE, ECO],
              ["Height: 26 in"],
              "Bedrooms, bathrooms and walk-in closets."))
U["8060396306605"] = dict(
    title="Cane Storage Basket with Handle | 16 in Laundry & Grocery Basket",
    seo_title="Cane Storage Basket with Handle | 16 inch | GrassCrafts",
    seo_desc="Handmade cane basket with handle, 16 in long. Carry laundry, toys, blankets or groceries. Natural, eco-friendly storage basket.",
    desc=desc("A handmade cane basket with a handle that moves around the house with you — laundry, toys, blankets or groceries.",
              ["Natural cane with a sturdy handle", "Laundry, toys, blankets or groceries", HANDMADE, ECO],
              ["Length: 16 in"],
              "Everyday home storage and gifting."))
U["8062498177197"] = dict(
    seo_title="Large Cane Storage Basket with Lid | Hand-Braided",
    seo_desc="Large hand-braided cane basket with lid and loop-and-knot closure. Store linens or creative tools in heritage style. Handmade in India.")
U["8506283327661"] = dict(
    seo_title="Hand-Braided Cane Carryall Basket with Handle | GrassCrafts",
    seo_desc="Hand-braided cane basket with arched handle — market basket, studio carryall or gift basket. Sustainable cane, handmade in India.")
U["8506292601005"] = dict(
    seo_title="Sabai Grass Tray | Burnt Sienna Weave | GrassCrafts",
    seo_desc="Shallow Sabai grass tray with two-tone burnt sienna weave on an iron frame. For tea service, journals or display. Handmade gift for her.")
U["8506478035117"] = dict(
    seo_title="Rectangular Sabai Grass Tray | Handwoven | GrassCrafts",
    seo_desc="Low-profile rectangular Sabai grass tray with multi-tonal weave. Ideal for tea service, stationery or display. Handmade in India.")
U["8506863222957"] = dict(
    seo_title="Tall Water Hyacinth Storage Basket | Laundry Bin",
    seo_desc="Tall handwoven water hyacinth basket — a sculptural laundry or storage bin for bedroom or living room. Sustainable, handmade in India.")
U["8141939114157"] = dict(
    title="Handwoven Kash Grass Bird Hanging Lamp Shade | Net-Top Decor Basket",
    seo_title="Kash Grass Bird Hanging Lamp Shade | GrassCrafts",
    seo_desc="Handwoven Kash grass bird-shaped hanging lamp shade with net-pattern top. Statement lighting for dining or living rooms. Handmade in India.")

# ---------- Gift hampers ----------
def hamper(occasion, material, price_note=None):
    return desc(f"A handmade {material} basket made for {occasion} gifting — fill it with sweets, essentials or keepsakes, and it keeps being useful long after the celebration.",
                [f"Ready to fill for {occasion}", f"Handcrafted from natural {material}", "Reusable afterwards for fruits, towels or storage", HANDMADE],
                use=f"{occasion}, weddings and bulk/custom hampers — contact us for quantity orders.")

U["8146420170925"] = dict(
    title="Cane Wedding Gift Hamper Basket | Handmade Trousseau Basket",
    seo_title="Cane Wedding Gift Hamper Basket | Handmade | GrassCrafts",
    seo_desc="Handmade natural cane wedding gift hamper basket. Fill with sweets or trousseau gifts, reuse for storage. Bulk wedding hamper orders welcome.")
U["8146425249965"] = dict(
    title="Straw Wedding Gift Hamper Basket | Handmade Reusable Hamper",
    seo_title="Straw Wedding Gift Hamper Basket | Handmade | GrassCrafts",
    seo_desc="Handmade natural straw wedding gift hamper basket. Rustic, reusable and eco-friendly. Bulk orders for weddings and events welcome.")
U["8146433409197"] = dict(
    title="Cane Haldi Ceremony Gift Hamper Basket | Handmade",
    seo_title="Haldi Ceremony Gift Hamper Basket | Cane | GrassCrafts",
    seo_desc="Handmade natural cane Haldi ceremony gift hamper basket. Fill with haldi essentials and sweets; reuse for storage. Bulk orders welcome.")
U["8146444583085"] = dict(
    title="Round Grass Haldi Ceremony Gift Hamper Basket | Small",
    seo_title="Round Grass Haldi Gift Hamper Basket | GrassCrafts",
    seo_desc="Small round handmade grass basket for Haldi ceremony gift hampers. Eco-friendly, reusable and affordable for bulk wedding gifting.")
U["8146742739117"] = dict(
    title="Round Grass Haldi Ceremony Gift Hamper Basket | Medium",
    seo_title="Haldi Ceremony Gift Hamper Basket | Medium | GrassCrafts",
    seo_desc="Handmade round grass and straw basket for Haldi ceremony gift hampers. Eco-friendly, reusable — ideal for wedding gifting in bulk.")
U["8146477744301"] = dict(
    title="Grass Baby Shower Gift Hamper Tray | Godh Bharai Hamper | Small",
    seo_title="Baby Shower Gift Hamper Tray | Godh Bharai | GrassCrafts",
    seo_desc="Handmade round grass tray for baby shower and Godh Bharai gift hampers. Eco-friendly, reusable and perfect for mom-to-be gifting.")
U["8146516115629"] = dict(
    title="Grass Baby Shower Gift Hamper Tray | Godh Bharai Hamper | Medium",
    seo_title="Godh Bharai Gift Hamper Tray | Handmade | GrassCrafts",
    seo_desc="Handwoven grass tray for baby shower and Godh Bharai hampers. Fill with goodies for the mom-to-be; reuse for storage. Eco-friendly.")
U["8146737299629"] = dict(
    title="Grass Baby Shower Gift Hamper Tray | Godh Bharai Hamper | Large",
    seo_title="Large Baby Shower Gift Hamper Tray | GrassCrafts",
    seo_desc="Large handmade grass tray for baby shower and Godh Bharai gift hampers. A reusable, eco-friendly base for mom-to-be gifts.")
U["8146483282093"] = dict(
    title="Cane Baby Shower Gift Hamper Basket | Mom-to-Be Hamper",
    seo_title="Cane Baby Shower Gift Hamper Basket | Mom-to-Be Gift",
    seo_desc="Handmade natural cane basket for baby shower and mom-to-be gift hampers. Fill with baby essentials; reuse as storage. Eco-friendly gift.")
U["8148948910253"] = dict(
    title="Cane Mehendi Ceremony Gift Hamper Basket | Handmade",
    seo_title="Mehendi Ceremony Gift Hamper Basket | Cane | GrassCrafts",
    seo_desc="Handwoven natural cane Mehendi gift hamper basket for henna cones, bangles and sweets. Reusable, eco-friendly wedding gifting.")
U["8148994064557"] = dict(
    title="Straw Mehendi Ceremony Gift Hamper Basket | Medium",
    seo_title="Straw Mehendi Gift Hamper Basket | GrassCrafts",
    seo_desc="Handmade natural straw Mehendi ceremony gift hamper basket for henna cones, bangles and sweets. Reusable, eco-friendly wedding gift.")
U["8149002682541"] = dict(
    title="Straw Mehendi Ceremony Gift Hamper Basket | Small",
    seo_title="Small Mehendi Gift Hamper Basket | Straw | GrassCrafts",
    seo_desc="Small handmade straw basket for Mehendi ceremony gift hampers. Affordable, reusable and eco-friendly — ideal for bulk wedding gifting.")

# ---------- Planters & vases ----------
cane_planter_bullets = ["Hand-woven natural cane", "Indoor & outdoor: home, office, balcony, terrace", "Doubles as a storage basket", HANDMADE]
U["8057576816813"] = dict(
    title="Cane Floor Planter with Detachable Stand | 12 in Basket Planter",
    seo_title="Cane Floor Planter with Stand | 12 inch | GrassCrafts",
    seo_desc="Hand-woven cane planter with detachable 4 in stand, 12 in high x 12 in dia. For home, office, terrace or resorts. Eco-friendly decor.",
    desc=desc("A hand-woven cane planter on a detachable stand that lifts your greenery off the floor and into the spotlight.",
              cane_planter_bullets, ["Planter height: 12 in", "Detachable stand: 4 in", "Diameter: 12 in"],
              "Living rooms, offices, cafés, resorts and housewarming gifts."))
U["8057598378157"] = dict(
    title="Tall Cane Floor Planter | 38 in Statement Planter for Indoor Plants",
    seo_title="Tall Cane Floor Planter | 38 inch | GrassCrafts",
    seo_desc="Statement 38 in tall hand-woven cane floor planter, 12 in diameter. For homes, offices, hotels and resorts. Eco-friendly handmade decor.",
    desc=desc("A 38-inch hand-woven cane floor planter — a statement piece that turns a single plant into a design feature.",
              cane_planter_bullets, ["Height: 38 in", "Diameter: 12 in"],
              "Entrances, living rooms, hotel lobbies and resorts."))
U["8057607159981"] = dict(
    title="Cane Planter with Stand | 8 in Table & Floor Planter",
    seo_title="Cane Planter with Stand | 8 inch | GrassCrafts",
    seo_desc="Hand-woven cane planter, 8 in high (16 in with stand), 8 in diameter. Indoor/outdoor eco-friendly planter and housewarming gift.",
    desc=desc("A compact hand-woven cane planter with an optional stand — use it on a table or raise it to floor height.",
              cane_planter_bullets, ["Planter height: 8 in", "Height with stand: 16 in", "Diameter: 8 in"],
              "Homes, offices, balconies and housewarming gifts."))
U["8061631758509"] = dict(
    title="Cane Table-Top Planters | Round & Oval | Handwoven Indoor Planters",
    seo_title="Round & Oval Cane Table-Top Planters | GrassCrafts",
    seo_desc="Hand-woven round and oval cane table-top planters for desks, shelves and windowsills. Eco-friendly indoor planters, handmade in India.")
U["8125581787309"] = dict(
    title="Handwoven Cane Planters | Small, Medium & Large | 8–12 in",
    seo_title="Handwoven Cane Planters | Small to Large | GrassCrafts",
    seo_desc="Hand-woven cane planters in 3 sizes (8, 10, 12 in). Indoor/outdoor use, double as storage. Eco-friendly housewarming gift.")
U["8125586768045"] = dict(
    title="Natural Cane Basket Planters | 3 Sizes | Indoor & Outdoor",
    seo_title="Natural Cane Basket Planters | 3 Sizes | GrassCrafts",
    seo_desc="Hand-woven natural cane basket planters, small to large (8–12 in). For homes, offices, cafés and terraces. Handmade eco decor.")
U["8138159259821"] = dict(
    title="Cane Cup Planter with Saucer | Mini Desk Planter",
    seo_title="Cane Cup Planter with Saucer | Mini Planter | GrassCrafts",
    seo_desc="Hand-woven cane cup planter with saucer — 4 in cup, 10 in saucer. A charming desk or windowsill planter and housewarming gift.",
    desc=desc("A hand-woven cane cup-and-saucer planter — a playful little piece for succulents and small plants on desks and windowsills.",
              cane_planter_bullets, ["Cup: 4 in high, 4 in diameter", "With saucer: 5 in high, 10 in diameter"],
              "Desks, windowsills, cafés and gifting."))
grass_planter = ["Natural Sabai grass or straw, handwoven", "Slip over a nursery pot — no repotting needed", "Three sizes to group together", HANDMADE]
grass_sizes = ["Small: 6 x 6 in", "Medium: 8 x 8 in", "Big: 10 x 10 in"]
for pid, variant in [("8071233110189", "Natural"), ("8071287734445", "Classic"), ("8140781519021", "Woven")]:
    U[pid] = dict(
        title=f"Sabai Grass Basket Planter | {variant} Weave | Small, Medium & Big",
        seo_title=f"Sabai Grass Basket Planter | {variant} Weave | GrassCrafts",
        seo_desc="Handwoven Sabai grass basket planters in 3 sizes (6, 8, 10 in). Eco-friendly pot covers for indoor plants, made by Indian artisans.",
        desc=desc("Handwoven by skilled Indian artisans from natural Sabai grass or straw, these basket planters give your indoor plants a warm, earthy home.",
                  grass_planter, grass_sizes, "Living rooms, balconies, offices and plant-lover gifts."))
U["8432664543405"] = dict(
    title="Handwoven Cane Flower Vase & Pen Stand | Small & Big",
    seo_title="Cane Flower Vase & Pen Stand | Handmade | GrassCrafts",
    seo_desc="Hand-woven cane flower vase that doubles as a pen stand. Small and big sizes. Elegant eco-friendly desk decor and corporate gift.",
    desc=desc("A hand-woven cane vase for dried flowers — or a pen stand on your desk. Small enough for anywhere, elegant enough for gifting.",
              ["Natural hand-woven cane", "Flower vase or pen stand", "Great for desks, shelves and dining tables", HANDMADE],
              ["Small: 3 in diameter, 4 in height", "Big: 4 in diameter, 4 in height"],
              "Offices, study tables and corporate gifting."))
U["8433332191405"] = dict(
    title="Kasi Grass Mini Flower Vase | 4 in Handwoven Desk Vase",
    seo_title="Kasi Grass Mini Flower Vase | 4 inch | GrassCrafts",
    seo_desc="Handwoven Kasi grass mini flower vase, 4 in tall. Adds calm and colour to your desk or study table. Affordable eco gift under ₹200.")
U["8433333829805"] = dict(
    title="Handwoven Grass Pen Holder | Natural Fibre Desk Organiser",
    seo_title="Handwoven Grass Pen Holder | Eco Desk Organiser",
    seo_desc="Handwoven natural grass pen holder for office and study desks. Eco-friendly, artisan-made — a perfect bulk corporate gift.")
U["8026906591405"] = dict(
    seo_title="Kauna Grass Planter | Natural Fibre Pot Holder",
    seo_desc="Handwoven Kauna grass planter sleeve from Manipur. Fits standard nursery pots — no repotting. Indoor & outdoor eco-friendly decor.")

# ---------- Wreaths ----------
wreath_bullets = ["Handmade with natural dried flowers", "Eco-friendly, sustainable materials", "Festive door, wall or table centrepiece", "Long-lasting — no watering needed"]
WREATH_CARE = "Hang indoors or in a sheltered spot away from rain and direct sun. Dust gently with a soft dry brush or a hairdryer on cool setting."
for i, pid in enumerate(["7977547628717", "7977547923629", "7977548316845", "7988506034349", "7988506362029", "8398791966893", "8398792491181"]):
    names = ["Classic", "Mini", "Petite", "Rustic", "Harvest", "Garden", "Meadow"]
    U[pid] = dict(
        title=f"Handmade Dry Flower Wreath – {names[i]} | Festive Door & Wall Decor",
        seo_title=f"Dry Flower Wreath – {names[i]} | Festive Door Decor",
        seo_desc="Handmade dry flower wreath for Diwali, Christmas and year-round decor. Eco-friendly door or wall wreath crafted from natural materials.",
        desc=desc("Welcome guests with a handmade dry flower wreath — a natural, long-lasting alternative to fresh flowers that brings festive warmth to doors, walls and tables.",
                  wreath_bullets, use="Diwali and Christmas decor, housewarming and festive gifting.", care=WREATH_CARE, note="Handmade — natural dried flowers vary slightly in colour and shape, so every wreath is one of a kind."))

# ---------- Wall plates ----------
wall_ids = ["8088281743533", "8088377852077", "8088418943149", "8088459641005", "8088490180781",
            "8088503517357", "8088613322925", "8140088836269", "8140090671277", "8140091850925"]
for pid in wall_ids:
    U[pid] = dict(
        seo_title="Sabai Grass Wall Plate Decor | Handwoven Wall Art",
        seo_desc="Handwoven Sabai grass and palm-leaf wall plates — no nylon thread. Boho wall art for living rooms, bedrooms and hallways. Made in India.")

# ---------- Mats ----------
puja = desc("A dual-sided asana mat with handwoven Madurkathi grass on one side and quilted handloom cotton on the other — both sides fully usable.",
            ["Two usable sides: Madurkathi grass and quilted cotton", "Keeps you cool and supported", "Indoor & outdoor; easy to wash", HANDMADE],
            ["Length: 23 in", "Breadth: 18 in"],
            "Puja, meditation, yoga and festive gifting.")
for i, pid in enumerate(["8037145018541", "8037157830829", "8049565597869", "8049571725485"]):
    U[pid] = dict(
        title=f"Madurkathi Puja & Asana Mat | Dual-Sided Grass & Cotton | 23×18 in – Design {i + 1}",
        seo_title="Madurkathi Puja & Asana Mat | Dual-Sided | 23x18 in",
        seo_desc="Dual-sided Madurkathi grass and quilted cotton asana mat, 23x18 in. For puja, meditation and yoga. Washable, handmade in India.",
        desc=puja)
U["7934413209773"] = dict(
    title="Madurkathi Grass Table Runner & 6 Mats Set | 58 in Runner",
    seo_title="Madurkathi Table Runner & 6 Placemats Set | GrassCrafts",
    seo_desc="Handmade Madurkathi grass table set: 58x12 in runner + 6 mats (18x12 in). Eco-friendly dining decor and a lovely housewarming gift.",
    desc=desc("Dress your dining table in handmade Madurkathi grass — earthy tones and natural texture that suit rustic, boho and modern settings alike.",
              ["Natural Madurkathi grass, handwoven", "Complete set: 1 runner + 6 mats", "Easy to wipe clean", HANDMADE],
              ["Runner: 58 in x 12 in", "Mats: 18 in x 12 in"],
              "Everyday dining, festive hosting and housewarming gifts."))
for pid in ["7934420811949", "8150556115117"]:
    U[pid] = dict(
        title="Madurkathi Grass Table Mats with Runner | 48 in Runner Set" + (" – Natural" if pid == "7934420811949" else " – Classic"),
        seo_title="Madurkathi Grass Table Mats & Runner Set | GrassCrafts",
        seo_desc="Handmade Madurkathi grass table mats (17x12 in) with 48x12 in runner. Natural, eco-friendly dining decor and festive gift.",
        desc=desc("Handmade Madurkathi grass table mats and runner that bring earthy texture to every meal — and make a thoughtful gift for anyone who loves artisanal living.",
                  ["Natural Madurkathi grass, handwoven", "Suits rustic, boho or modern tables", "Easy to wipe clean", HANDMADE],
                  ["Mats: 17 in x 12 in", "Runner: 48 in x 12 in"],
                  "Dining tables, festive hosting and housewarming gifts."))
U["8429876478125"] = dict(
    seo_title="Water Hyacinth Round Placemats | 12 inch | GrassCrafts",
    seo_desc="Handwoven water hyacinth round placemats, 12 in diameter. Natural, biodegradable table mats for dining and coffee tables. Made in India.")

# ---------- Other ----------
U["7884502433965"] = dict(
    title="GrassCrafts Gift Card | Handmade Eco-Friendly Gifts",
    seo_title="GrassCrafts Gift Card | Give Handmade Eco Gifts",
    seo_desc="Let them choose from handwoven bags, baskets and decor. GrassCrafts gift cards — ideal for family abroad, teachers, friends and corporate gifting.")

if __name__ == "__main__":
    out = []
    for pid, u in U.items():
        assert len(u["seo_title"]) <= 70, (pid, len(u["seo_title"]), u["seo_title"])
        assert len(u["seo_desc"]) <= 160, (pid, len(u["seo_desc"]))
        out.append({"id": f"gid://shopify/Product/{pid}", **u})
    Path(__file__).with_name("seo_updates.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out), "updates;", sum("title" in u for u in out), "titles;", sum("desc" in u for u in out), "descriptions")
