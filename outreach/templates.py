"""Cold-outreach email templates for GrassCrafts B2B prospects (one per segment)."""
import re

SIG = ("\n\nWarm regards,\nAmit Dey\nGrassCrafts — handwoven natural-fibre gifts\n"
       "grasscrafts.com  |  Instagram @grasscrafts.com_\n\n"
       "If this isn't the right inbox, I'd be grateful if you could forward it to the person who handles "
       "gifting or purchasing. If you'd rather not hear from us, just reply \"no thanks\" and I won't email again.")
CLIENTS = ("We have supplied businesses such as My E-haat Display Centre (HCL Foundation), Grill Splendour "
           "Services, VBev, Broadarks Technology and Ru & Ki Gifts.")


def greet(co):
    co = (co or "").strip()
    ok = 2 < len(co) < 45 and not re.search(r"[@:/\[\]]|email|contact|here are|following", co, re.I)
    return (f"Hello {co} team," if ok else "Hello,"), (co if ok else None)


def render(seg, co):
    g, name = greet(co)
    if seg == "Jewellery":
        s = f"Handwoven jewellery boxes for {name}'s festive packaging" if name else "Handwoven, plastic-free jewellery boxes for festive packaging"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna and Sabai grass jewellery boxes, display trays and gift boxes, woven by Indian artisans with no plastic.\n\n"
             "For the festive and wedding season they work as a premium, reusable alternative to standard jewellery packaging — the box becomes part of the gift. We take bulk orders with custom sizes and colours, and can mix designs in one order.\n\n"
             f"{CLIENTS} I've attached our catalogue with retail prices; volume pricing depends on quantity.\n\nWould you be open to a quick call, or shall I send a couple of samples?")
    elif seg == "Corporate gifting companies":
        s = f"Handwoven eco gift range for {name}'s corporate clients" if name else "Handwoven eco-friendly gift range for your corporate clients"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven, plastic-free gift baskets, bamboo trays, Sabai grass gift boxes and desk organisers, woven by Indian artisans.\n\n"
             "For Diwali and year-end hampers, our pieces work either as the hamper packaging or as the gift itself, and we're happy to supply on a reseller basis. Prices start under ₹500 per piece, with volume pricing on bulk orders.\n\n"
             f"{CLIENTS} Our catalogue is attached.\n\nWould it help if I shared a shortlist and samples for your eco-gifting range?")
    elif seg == "Wedding & event planners":
        s = f"Handwoven return-gift and trousseau baskets for {name}" if name else "Handwoven return-gift and trousseau baskets for your weddings"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna and Sabai grass hamper baskets, bamboo trays and gift boxes — a natural, plastic-free option for wedding return gifts, trousseau packing and ceremonies like Haldi, Mehendi and Godh Bharai.\n\n"
             "We take bulk orders, can mix designs, and offer custom sizes and colours on request. Hamper baskets start under ₹500.\n\n"
             f"{CLIENTS} I've attached our catalogue.\n\nCould we share options for your upcoming wedding season?")
    elif seg == "Festive hamper brands":
        s = f"Reusable handwoven baskets for {name}'s festive hampers" if name else "Reusable handwoven baskets for your festive hampers"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven Kauna grass hamper baskets, bamboo baskets and trays, and Sabai grass gift boxes, woven by Indian artisans with no plastic.\n\n"
             "For Diwali and gifting hampers, they can replace cardboard or plastic packaging with something customers keep and reuse. We supply in bulk with custom sizes and colours on request; hamper baskets start under ₹500.\n\n"
             f"{CLIENTS} Our catalogue is attached.\n\nWould you like samples of two or three basket styles to try?")
    elif seg == "Cane planters (hotels, cafes, designers)":
        s = f"Handwoven cane planters for {name}'s spaces" if name else "Handwoven cane planters for hotels, cafés and interiors"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven cane planters – table-top, floor planters with stands, tall 38-inch statement planters and sets of three – along with cane baskets, trays and ottomans, all woven by Indian artisans.\n\n"
             "For lobbies, rooms, cafés, offices and design projects, they bring natural texture without plastic and are easy to repeat across a whole property. We take project and repeat orders, and can match sizes across a set.\n\n"
             f"{CLIENTS} I've attached our catalogue.\n\nShall I send a shortlist of planter sizes for your next project or refresh?")
    elif seg == "Sustainable decor brands":
        s = f"Handwoven natural-fibre decor for {name}'s range" if name else "Handwoven natural-fibre decor for your store"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven decor in seven natural fibres – Sabai grass, Kauna grass, GI-tagged Madurkathi, cane, water hyacinth, bamboo and jute: baskets, wall plates, planters, trays, madur mats and boxes, woven by Indian artisans.\n\n"
             "If your brand stocks sustainable home decor, we can supply ready designs for your store or online shop on a repeat basis. Small mixed trial orders are fine.\n\n"
             f"{CLIENTS} Our catalogue is attached.\n\nWould a trial assortment for your next season be useful?")
    else:
        s = f"Handwoven baskets, planters and decor for {name}" if name else "Handwoven baskets, planters and decor for your store"
        b = (f"{g}\n\nI'm Amit from GrassCrafts. We make handwoven baskets, planters, wall plates, trays and gift boxes from Kauna, Sabai grass, cane, bamboo and water hyacinth, woven by Indian artisans with no plastic.\n\n"
             "If you stock home decor or gifts, we'd love to supply you at wholesale prices — in time for Diwali and the wedding season. Small mixed orders are fine to start with.\n\n"
             f"{CLIENTS} I've attached our catalogue with retail prices.\n\nShall I share our wholesale pricing?")
    return s, b + SIG
