"""Cold-outreach email templates for GrassCrafts B2B prospects (one per segment)."""
import re

SIG = ("\n\nWarm regards,\nAmit Dey\nGrassCrafts — handwoven natural-fibre gifts\n"
       "grasscrafts.com  |  Instagram @grasscrafts.com_\n\n"
       "If this isn't the right inbox, I'd be grateful if you could forward it to the person who handles "
       "gifting or purchasing. If you'd rather not hear from us, just reply \"no thanks\" and I won't email again.")
# Owner USPs, 30 Oct 2026 (sales/grasscrafts_usp_pitch_2026-10-30.md). No prices, MOQ, lead times or samples.
USP = {
    "made": "- Made to your requirements: design, dimensions, shape, colours, materials and functional details, subject to feasibility.",
    "brand": "- Customised for your brand: baskets, gift hampers, reusable packaging and presentation that match your identity and occasion.",
    "craft": "- Authentic Indian artisan craftsmanship: traditional weaving skills and distinctive natural textures.",
    "fibre": "- Natural-fibre alternatives: Sabai grass, Kauna, Madurkathi, cane, bamboo and jute instead of conventional synthetic products.",
    "premium": "- Premium, differentiated presentation: unique handcrafted designs for gifting, weddings, luxury and premium retail.",
    "reuse": "- Reusable with everyday utility: many baskets and containers keep serving a purpose after the gift.",
    "range": "- Versatile B2B range: corporate gifting, hospitality, wedding hampers, retail packaging and home décor.",
    "story": "- Artisan-made with a story: products that communicate craftsmanship, cultural heritage and thoughtful material choices.",
}
SEG_USP = {
    "Jewellery": ("brand", "premium", "reuse", "story"),
    "Corporate gifting companies": ("made", "brand", "premium", "range"),
    "Wedding & event planners": ("made", "craft", "premium", "reuse"),
    "Festive hamper brands": ("brand", "fibre", "reuse", "premium"),
    "Cane planters (hotels, cafes, designers)": ("made", "fibre", "craft", "story"),
    "Sustainable decor brands": ("craft", "fibre", "range", "story"),
    "Diamond jewellery boxes & baskets": ("made", "brand", "premium", "reuse"),
    "Luxury watches": ("brand", "premium", "reuse", "story"),
    "Hotels & resorts": ("made", "fibre", "reuse", "story"),
    "Spas & wellness": ("fibre", "craft", "reuse", "story"),
    "Real estate developers": ("brand", "premium", "reuse", "story"),
    "Ethnic wear boutiques": ("made", "craft", "premium", "reuse"),
}
DEFAULT_USP = ("craft", "fibre", "range", "story")


def usp_block(seg):
    keys = SEG_USP.get(seg, DEFAULT_USP)
    return "What makes us useful to businesses like yours:\n" + "\n".join(USP[k] for k in keys) + "\n\n"


CLIENTS = ("We have supplied businesses such as My E-haat Display Centre (HCL Foundation), Grill Splendour "
           "Services, VBev, Broadarks Technology and Ru & Ki Gifts.")


def greet(co):
    co = (co or "").strip()
    ok = 2 < len(co) < 45 and not re.search(r"[@:/\[\]]|email|contact|here are|following", co, re.I)
    return (f"Hello {co} team," if ok else "Hello,"), (co if ok else None)


def render(seg, co):
    g, name = greet(co)
    if seg == "Jewellery":
        s = f"Handwoven jewellery boxes for {name}'s festive packaging" if name else "Handwoven natural-fibre jewellery boxes for festive packaging"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna and Sabai grass jewellery boxes, display trays and gift boxes, woven by Indian artisans — a natural-fibre alternative to synthetic packaging.\n\n"
             "For the festive and wedding season they work as a premium, reusable alternative to standard jewellery packaging — the box becomes part of the gift. We take bulk orders with custom sizes and colours, and can mix designs in one order.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould you be open to a quick call, or could you point me to the person who handles packaging?")
    elif seg == "Corporate gifting companies":
        s = f"Handwoven eco gift range for {name}'s corporate clients" if name else "Handwoven eco-friendly gift range for your corporate clients"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven gift baskets, bamboo trays, Sabai grass gift boxes and desk organisers, woven by Indian artisans — a natural-fibre alternative to synthetic gifting.\n\n"
             "For Diwali and year-end hampers, our pieces work either as the hamper packaging or as the gift itself, and we're happy to supply on a reseller basis.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould it help if I shared a shortlist for your eco-gifting range?")
    elif seg == "Wedding & event planners":
        s = f"Handwoven return-gift and trousseau baskets for {name}" if name else "Handwoven return-gift and trousseau baskets for your weddings"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna and Sabai grass hamper baskets, bamboo trays and gift boxes — a natural-fibre alternative to synthetic packaging for wedding return gifts, trousseau packing and ceremonies like Haldi, Mehendi and Godh Bharai.\n\n"
             "We take bulk orders, can mix designs, and offer custom sizes and colours on request.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nCould we share options for your upcoming wedding season?")
    elif seg == "Festive hamper brands":
        s = f"Reusable handwoven baskets for {name}'s festive hampers" if name else "Reusable handwoven baskets for your festive hampers"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna grass hamper baskets, bamboo baskets and trays, and Sabai grass gift boxes, woven by Indian artisans — a natural-fibre alternative to synthetic packaging.\n\n"
             "For Diwali and gifting hampers, they can replace cardboard or plastic packaging with something customers keep and reuse. We supply in bulk with custom sizes and colours on request.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould a shortlist of two or three basket styles for your hampers be useful?")
    elif seg == "Cane planters (hotels, cafes, designers)":
        s = f"Handwoven cane planters for {name}'s spaces" if name else "Handwoven cane planters for hotels, cafés and interiors"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven cane planters – table-top, floor planters with stands, tall 38-inch statement planters and sets of three – along with cane baskets, trays and ottomans, all woven by Indian artisans.\n\n"
             "For lobbies, rooms, cafés, offices and design projects, they bring natural texture as a natural-fibre alternative to synthetic décor and are easy to repeat across a whole property. We take project and repeat orders, and can match sizes across a set.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nShall I send a shortlist of planter sizes for your next project or refresh?")
    elif seg == "Sustainable decor brands":
        s = f"Handwoven natural-fibre decor for {name}'s range" if name else "Handwoven natural-fibre decor for your store"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven decor in seven natural fibres – Sabai grass, Kauna grass, GI-tagged Madurkathi, cane, water hyacinth, bamboo and jute: baskets, wall plates, planters, trays, madur mats and boxes, woven by Indian artisans.\n\n"
             "If your brand stocks sustainable home decor, we can supply ready designs for your store or online shop on a repeat basis. Small mixed trial orders are fine.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould a trial assortment for your next season be useful?")
    elif seg == "Diamond jewellery boxes & baskets":
        s = f"Handwoven jewellery boxes and bridal baskets for {name}" if name else "Handwoven jewellery boxes and bridal baskets for your showroom"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Sabai and Kauna grass jewellery boxes, boxes with lids, display trays and bridal hamper baskets, woven by Indian artisans — a natural-fibre alternative to synthetic packaging.\n\n"
             "For bridal sets, festive collections and client gifting, a handwoven box becomes part of the gift and is kept long after the purchase. We take bulk orders with custom sizes and colours on request, and can mix designs in one order.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould you be open to a quick call to see whether this suits your wedding-season or Akshaya Tritiya packaging?")
    elif seg == "Luxury watches":
        s = f"Handwoven client-gifting boxes for {name}" if name else "Handwoven client-gifting boxes for your watch boutique"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven cane and grass boxes with lids, trays and desk organisers, woven by Indian artisans — a natural-fibre alternative to synthetic packaging.\n\n"
             "Watch boutiques use pieces like these as a gift-with-purchase, for VIP client gifting at Diwali and New Year, or as display trays. We take bulk orders, and sizes can be customised on request.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould a shortlist for your next client-gifting occasion be useful?")
    elif seg == "Hotels & resorts":
        s = f"Handwoven room and lobby pieces for {name}" if name else "Handwoven natural-fibre room and lobby pieces for your property"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven laundry and storage baskets, tissue box covers, cane trays, cane planters, table mats and Madurkathi mats, woven by Indian artisans — a natural-fibre alternative to synthetic products.\n\n"
             "For rooms, spas, restaurants and lobbies they add natural texture and support a property's sustainability story, and they're easy to repeat across every room. We take project and repeat orders and can match sizes across a set.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nShall I send a shortlist for your rooms or your festive lobby décor this season?")
    elif seg == "Spas & wellness":
        s = f"Handwoven Madurkathi mats and baskets for {name}" if name else "Handwoven Madurkathi mats and baskets for your spa or studio"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make GI-tagged Madurkathi grass mats, straw yoga mats, grass trays, tissue box covers and baskets, woven by artisans in Bengal — a natural-fibre alternative to synthetic products.\n\n"
             "Spas, wellness centres and yoga studios use them for treatment rooms, meditation and retail shelves, as a natural alternative to synthetic mats. We take bulk and repeat orders.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould you like a shortlist for your treatment rooms or retail corner?")
    elif seg == "Real estate developers":
        s = f"Handwoven homebuyer gifts for {name}" if name else "Handwoven key-handover and festive gifts for your homebuyers"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Sabai grass gift boxes, Kauna hamper baskets and grass and cane planters, woven by Indian artisans — a natural-fibre alternative to synthetic products.\n\n"
             "Developers use gifts like these at key handover, for housewarmings, and for festive greetings to homebuyers and channel partners. They're useful in a new home and show a sustainability touch. We take bulk orders.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould a shortlist for your next handover or festive campaign help?")
    elif seg == "Ethnic wear boutiques":
        s = f"Handwoven trousseau baskets and boxes for {name}" if name else "Handwoven trousseau baskets and boxes for your bridal clients"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven trousseau baskets, Sabai grass boxes and hamper baskets, woven by Indian artisans — a natural-fibre alternative to synthetic packaging.\n\n"
             "Bridal and saree boutiques use them for trousseau packing and premium packaging for their best clients. The basket becomes part of the wedding. We take bulk orders with custom sizes and colours on request.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nCould we share options for this wedding season?")
    else:
        s = f"Handwoven baskets, planters and decor for {name}" if name else "Handwoven baskets, planters and decor for your store"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven baskets, planters, wall plates, trays and gift boxes from Kauna, Sabai grass, cane, bamboo and water hyacinth, woven by Indian artisans — a natural-fibre alternative to synthetic products.\n\n"
             "If you stock home decor or gifts, we'd love to supply you on a trade basis for the festive and wedding seasons. Small mixed orders are fine to start with.\n\n"
             f"{CLIENTS} You can see our range on our trade sample sheet: https://grasscrafts.com/pages/trade-sample-sheet.\n\nWould a short call to discuss a trial assortment suit you?")
    i = b.find("\n\n", b.find("I'm Amit")) + 2
    return s, b[:i] + usp_block(seg) + b[i:] + SIG
