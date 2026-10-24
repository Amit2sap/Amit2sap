# 2026-10-24 Cash on Delivery ₹100 fee (owner decision, 24 Oct)

Owner: COD costs ₹100 extra on all orders. Fee is charged by the Releasit COD Form app (installed by owner 24 Oct; owner enables "Additional fee" in the app — agents cannot change app settings).

## Draft theme for owner to publish
Theme "Grasscrafts – COD ₹100 24 Oct" (gid://shopify/OnlineStoreTheme/189658235053), duplicate of live 189623959725:
- snippets/gc-product-trust.liquid: "Cash on Delivery" -> "Cash on Delivery (₹100 extra)". md5 03959467eaa352a55c8f1b562a73b5bc = seo/gc-product-trust.liquid.
- templates/llms.txt.liquid: added "- Payment: UPI, cards, netbanking and Cash on Delivery in India (Cash on Delivery has an extra ₹100 charge per order, shown at checkout)". md5 593aaa71dac7f9463ce285bfc4634900 = seo/llms.txt.liquid.
- Note: themeDuplicate finishes asynchronously and overwrote the first upsert; files were re-written after the copy finished and verified by checksum.
Backups: backups/theme/gc-product-trust_before_2026-10-24.liquid, backups/theme/llms.txt_before_2026-10-24.liquid.
Undo after publish: publish 189623959725 again.

## Shipping policy (owner to paste; API lacks write_legal_policies scope)
Backup: backups/policies/shipping_policy_before_2026-10-24.html. New text in seo/shipping_policy_2026-10-24.txt (also fixes ₹1,300 -> ₹1,299).
