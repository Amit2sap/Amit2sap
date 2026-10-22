# Checkout changes, 2026-10-22 (owner request: COD, tax, free shipping)

## 1. Free shipping now starts at ₹1,299.00 (CHANGED)
Backups: backups/checkout/delivery_profiles_before_2026-10-22.json (before), backups/checkout/delivery_profiles_after_2026-10-22.json (after).

| Profile | Method (India zone) | Before | After |
|---|---|---|---|
| General profile (gid://shopify/DeliveryProfile/90595819693), zone "Domestic" | Free shipping ₹0 (MethodDefinition/660702724269) | subtotal >= ₹1,300.00 | subtotal >= ₹1,299.00 |
| General profile, zone "Domestic" | Standard ₹120 (MethodDefinition/602482901165) | ₹0 to ₹1,299.99 | ₹0 to ₹1,298.99 |
| Free Shipping Condition (gid://shopify/DeliveryProfile/95156043949), zone "india" | Free shipping ₹0 (MethodDefinition/660702396589) | subtotal >= ₹1,300.00 | subtotal >= ₹1,299.00 |
| Free Shipping Condition, zone "india" | Shipping ₹120 (MethodDefinition/660702429357) | ₹0 to ₹1,299.99 | ₹0 to ₹1,298.99 |

Not touched: International zone (₹1,700 flat), MAKHANA profile (free, no minimum), rate prices, names, products.
The ₹120 upper limit moved to ₹1,298.99 so a ₹1,299 cart sees only the free rate (otherwise it would see both).
Shopify re-creates edited conditions, so the condition IDs are new (listed in the after backup).

Verified: profiles re-read (General v3, Free Shipping Condition v12). draftOrderCalculate (calculation only, nothing saved):
Kauna Jewellery Display Tray ₹1,299 to Delhi offers only "Free shipping ₹0"; Kauna Planter ₹980 offers only "Shipping ₹120".
A storefront cart test was not possible: this session's network proxy blocks grasscrafts.com.

Undo (Admin GraphQL deliveryProfileUpdate, one call per profile; read the profile first to get the current condition IDs):
- Free Shipping Condition: locationGroupsToUpdate [{id: "gid://shopify/DeliveryLocationGroup/95908823213", zonesToUpdate: [{id: "gid://shopify/DeliveryZone/411091435693", methodDefinitionsToUpdate: [
  {id: "gid://shopify/DeliveryMethodDefinition/660702396589", conditionsToUpdate: [{id: "<current >= condition id>", criteria: 1300, criteriaUnit: "INR", field: TOTAL_PRICE, operator: GREATER_THAN_OR_EQUAL_TO}]},
  {id: "gid://shopify/DeliveryMethodDefinition/660702429357", conditionsToUpdate: [{id: "<current <= condition id>", criteria: 1299.99, criteriaUnit: "INR", field: TOTAL_PRICE, operator: LESS_THAN_OR_EQUAL_TO}]}]}]}]
- General profile: same shape with location group 91169620141, zone 390200131757, free method 660702724269 (back to 1300) and Standard method 602482901165 (back to 1299.99).
- Or in admin: Settings > Shipping and delivery > each profile > India zone > edit each rate's condition.

## 2. Cash on Delivery (NOT changed, owner step)
The Admin API cannot create or turn on a manual payment method (no such mutation; paymentCustomization only hides or renames existing methods through a Functions app). Owner steps are in reports/checkout_fixes_2026-10-22.md.
Snapshot: backups/checkout/shop_tax_and_payment_state_2026-10-22.json.

## 3. Include tax in prices (NOT changed, owner step)
The Admin API cannot change Shop.taxesIncluded (read-only; no mutation). Current: taxesIncluded=false, taxShipping=false.
Margin tables and the two options are in reports/checkout_fixes_2026-10-22.md.

No products, prices, inventory, discounts, apps, payments or theme touched.

## 4. All product variants set to not taxable (CHANGED, owner: "We don't charge GST or any tax on any product", 22 Oct)
Before: 173 of 539 variants had taxable=true (39 products), so Shopify added 18% IGST at checkout on them.
Backup (product id, handle, variant id, title, taxable before): backups/checkout/taxable_variants_before_2026-10-22.json.
Change: productVariantsBulkUpdate per product with variants [{id, taxable: false}] only. 39 products, 173 variants, 0 userErrors, no retries needed. Nothing else changed (prices, inventory, titles, SKUs, tax codes untouched).
Verified: productVariants(query:"taxable:true") returns 0; nodes() re-read of all 173 IDs shows taxable=false.
draftOrderCalculate (nothing saved): Madurkathi Fridge Top Cover Red ₹750 + Handwoven Cane Planters Kaziranga/Small ₹1,150, ship to New Delhi DL 110001: subtotal ₹1,900, totalTax ₹0, taxLines [], shipping Free ₹0, total ₹1,900.
Shop settings read: taxesIncluded=false, taxShipping=false (shipping not taxed). Not changeable by API: India GST collection/registration and per-product/collection tax overrides (owner check: Settings > Taxes and duties > India).

Undo (only if the owner asks): for each product in the backup, run
  productVariantsBulkUpdate(productId: "<product_id>", variants: [{id: "<variant_id>", taxable: true}, ...])
using the product_id/variant_id pairs in backups/checkout/taxable_variants_before_2026-10-22.json (only those 173 variants were taxable before; leave all others false).
Or in admin: Products > open product > variant > Pricing > tick "Charge tax on this variant" > Save.

No prices, inventory, discounts, apps, payments or theme touched.
