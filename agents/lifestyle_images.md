# Lifestyle images (automated, free) — added 23 Oct 2026

**PAUSED by owner (23 Oct 2026): do NOT generate or composite any images until the owner says to resume. Use only the owner's real photos and images already on Shopify.**

Owner wants lifestyle pictures made automatically for every new product photo sent in chat.

Method (keeps the REAL product unchanged — never let an AI redraw the product):
1. Scene: Composio GEMINI_GENERATE_IMAGE (Instant, no key, 1K 1:1). Prompt a straight-on photorealistic room with the hanging/placement spot left EMPTY ("no garland, no toran, nothing hanging, no text").
2. Product cut-out: `scripts/toran_composite.py` (rembg isnet-general-use + colour mask) run locally in /home/user/Amit2sap (pip install "rembg[cpu]"; the Composio workbench crashes on the model). Download the scene's s3url with curl within 1 hour.
3. Place: `place(scene, cutout(photo), centre_x, top_y, width)` — measure the spot by viewing the scene once; add soft shadow + warm grade.
4. Check ONE contact sheet: keep only images where the product is complete (base strip, accents) and looks natural. Light/white products on light photo backgrounds cut out badly (23 Oct: Ivory & Gold and Blush Pink torans failed) — ask the owner for photos on a darker plain cloth.
5. Upload: commit JPGs to media/<product>/lifestyle/, use raw.githubusercontent URLs as Shopify originalSource, descriptive alt text.

Never present a composite as a customer photo; never alter product colours or parts.
