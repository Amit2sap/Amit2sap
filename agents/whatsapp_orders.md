# WhatsApp order messages (runs inside the Reply watcher, 15:07 and 19:07 IST)

Owner request, 25 Oct 2026. Transactional (UTILITY) messages only: never send a marketing template from this job.

**Sender:** Composio WhatsApp account `whatsapp_guha-marko`, phone_number_id `1292616473939901` (+91 81004 47884, "Gift Hamper"), WABA 28037860215843187. Tool: WHATSAPP_SEND_TEMPLATE_MESSAGE, language_code `en`.

**State file:** `outreach/whatsapp_orders_log.json`. If it is missing, create it as:
`{"start_after": "2026-10-25T09:30:00Z", "confirmed": [], "shipped": [], "skipped": [], "optout": []}`
Never message an order created before `start_after`, except the shipped message for an order fulfilled after `start_after`.

## Each run
1. Shopify query: `orders(first: 50, reverse: true, query: "created_at:>=<2 days ago>")` with name, createdAt, cancelledAt, test, phone, statusPageUrl, paymentGatewayNames, totalPriceSet, shippingAddress {firstName phone countryCodeV2}, customer {firstName defaultPhoneNumber {phoneNumber}}, fulfillments {createdAt trackingInfo {company number url}}. Also query orders with `fulfillment_status:shipped updated_at:>=<2 days ago>` for the shipped step.
2. Skip: cancelled orders, test orders, orders outside India (countryCodeV2 not IN), orders with no phone, and phones in `optout`.
3. **Phone:** take order.phone, else shippingAddress.phone, else customer.defaultPhoneNumber. Keep digits only, drop a leading 0, and if 10 digits are left, prefix 91. The result must be 12 digits starting with 91.
4. **Confirmation** (order createdAt >= start_after and name not in `confirmed`):
   - Prepaid (gateway is not "Cash on Delivery"): template `order_confirmation` with body params [first name, order name, "₹" + total with Indian commas]. The text says "We have received your payment of {{3}}".
   - Cash on Delivery: template `order_confirmation_cod` with the same 3 params, **only if its status is APPROVED** (check once per run with WHATSAPP_GET_MESSAGE_TEMPLATES name_or_content "order_confirmation_cod"). If it is not approved, add the order to `skipped` with the reason and do NOT use `order_confirmation`, because that text claims payment was received.
5. **Shipped** (a fulfillment createdAt >= start_after and name not in `shipped`): template `order_shipped` with params [first name, order name, carrier, tracking link]. Carrier = trackingInfo.company, else "our courier". Tracking link = trackingInfo.url, else the order's statusPageUrl.
6. First name: shippingAddress.firstName, else customer.firstName, else "there".
7. Add each sent order name to `confirmed` or `shipped`, and record send errors in `skipped`. If a customer replies STOP or taps "Stop promotions" on any message, add their phone to `optout`.
8. Commit and push the state file. Report one line: "WhatsApp orders: N confirmations, M shipped, K skipped". Stay silent if all three are 0.

## Notes
- Replies to +91 81004 47884 go to a temporary webhook (ngrok), so read customer replies in WhatsApp Manager until the owner fixes it.
- Marketing templates (`diwali_offer`, `abandoned_cart`, `review_request`) go only to customers whose Shopify SMS marketing state is SUBSCRIBED, and only when the owner asks. This job does not send them.
