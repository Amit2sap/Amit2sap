# 2026-10-25 Draft prices on the 2 makhana DRAFT products (owner request; Sristi to review)
Both products stay DRAFT (not visible to buyers). Calculation: sales/makhana_draft_pricing_2026-10-25.md (costs are ASSUMPTIONS).
- Makhana Gift Hamper (gid://shopify/Product/15265744486573): option "Size" added. Small (250 g) ₹849 (variant 67567176581293, was Default Title ₹0); Large (500 g) ₹1,349 (new variant 67643861008557). taxable false.
- Bulk Makhana (gid://shopify/Product/15265744683181): option "Pack" added. 1 kg ₹1,149 (variant 67567177171117, was Default Title ₹0); 5 kg (5 x 1 kg) ₹5,499 (new variant 67643861041325). taxable false.
Before: each product had one Default Title variant at ₹0, inventory untracked.
Undo: productOptionsDelete on the new option (strategy POSITION) or delete the new variants, then set price back to 0.
