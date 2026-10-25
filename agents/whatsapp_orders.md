# WhatsApp order messages (runs inside the Reply watcher, 15:07 and 19:07 IST)

Owner request, 25 Oct 2026. Transactional (UTILITY) messages only: never send a marketing template from this job.

**Sender:** Composio WhatsApp account `whatsapp_guha-marko`, phone_number_id `1292616473939901` (+91 81004 47884, "Gift Hamper"), WABA 28037860215843187. Tool: WHATSAPP_SEND_TEMPLATE_MESSAGE, language_code `en`.

**State file:** `outreach/whatsapp_orders_log.json`. If it is missing, create it as:
`{"start_after": "2026-10-25T09:30:00Z", "exclude": ["#1042"], "confirmed": [], "shipped": [], "skipped": [], "optout": []}`
**Never message an order listed in `exclude`** (owner, 25 Oct: #1042 may be cancelled). The owner adds or removes order names there.
Never message an order created before `start_after`, except the shipped message for an order fulfilled after `start_after`.

## Each run
1. Shopify query: `orders(first: 50, reverse: true, query: "created_at:>=<2 days ago>")` with name, createdAt, cancelledAt, test, phone, statusPageUrl, paymentGatewayNames, totalPriceSet, shippingAddress {firstName phone countryCodeV2}, customer {firstName defaultPhoneNumber {phoneNumber}}, fulfillments {createdAt trackingInfo {company number url}}. Also query orders with `fulfillment_status:shipped updated_at:>=<2 days ago>` for the shipped step.
2. Skip: orders in `exclude`, cancelled orders, test orders, orders outside India (countryCodeV2 not IN), orders with no phone, and phones in `optout`.
3. **Phone:** take order.phone, else shippingAddress.phone, else customer.defaultPhoneNumber. Keep digits only, drop a leading 0, and if 10 digits are left, prefix 91. The result must be 12 digits starting with 91.
4. **Templates (25 Oct, v2 = ends with "For any questions, please WhatsApp us on +91 62907 44782", because replies to +91 81004 47884 are not received).** Once per run, check status with WHATSAPP_GET_MESSAGE_TEMPLATES (name_or_content "_v2" and "order_confirmation_cod").
   - **Confirmation** (order createdAt >= start_after and name not in `confirmed`), params [first name, order name, "₹" + total with Indian commas]:
     - Prepaid (gateway is not "Cash on Delivery"): `order_confirmation_v2` if APPROVED, else `order_confirmation` (v1 has no reply prompt, so it is fine).
     - Cash on Delivery: `order_confirmation_cod_v2` if APPROVED, else `order_confirmation_cod` if APPROVED, else add to `skipped` ("COD template pending"). **Never** use `order_confirmation`/`_v2` for COD: that text says payment was received.
   - **Shipped** (a fulfillment createdAt >= start_after and name not in `shipped`): **only** `order_shipped_v2`, params [first name, order name, carrier, tracking link]. Carrier = trackingInfo.company, else "our courier". Tracking link = trackingInfo.url, else statusPageUrl. If v2 is not APPROVED yet, add to `skipped` ("shipped v2 pending") and retry next run. Do not use v1 `order_shipped`: it says "Reply to this message", and replies are lost.
5. First name: shippingAddress.firstName, else customer.firstName, else "there".
6. Add each sent order name to `confirmed` or `shipped`, and record send errors in `skipped`. If a customer replies STOP or taps "Stop promotions" on any message, add their phone to `optout`.
7. Commit and push the state file. Report one line: "WhatsApp orders: N confirmations, M shipped, K skipped". Stay silent if all three are 0.

## Notes
- Replies to +91 81004 47884 go to a temporary webhook (ngrok), so read customer replies in WhatsApp Manager until the owner fixes it.
- Marketing templates (`diwali_offer`, `abandoned_cart`, `review_request`) go only to customers whose Shopify SMS marketing state is SUBSCRIBED, and only when the owner asks. This job does not send them.
