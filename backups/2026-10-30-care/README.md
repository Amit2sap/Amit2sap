# Backup before care blocks (30 Oct 2026)

Collections changed: sabai-grass (gid://shopify/Collection/330117316781) and kauna-grass-manipur (gid://shopify/Collection/330117185709).

The change is append-only: a `<div class="gc-care-block">…</div>` was added at the very end of each collection's descriptionHtml. Everything before it is the post-D34 description (see backups/2026-10-30-directives/ and seo/CHANGELOG-2026-10-30-website.md).

Undo: in Shopify admin (or collectionUpdate), delete the `<div class="gc-care-block">…</div>` block at the end of each description. Nothing else was changed.

Care text source (owner, 30 Oct: "check knowledge article for care"):
- Kauna: blog article "Kauna Grass: A Sustainable Luxury Material from Manipur" (section "Caring for Kauna Products") + "Jute vs Water Hyacinth vs Sabai Grass vs Cane" table ("Keep dry; avoid crushing the weave").
- Sabai: "Jute vs Water Hyacinth vs Sabai Grass vs Cane" table ("Dust gently; protect from moisture") + its "How to care for natural-fibre baskets" list.
