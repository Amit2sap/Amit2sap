# Review kit: collecting genuine reviews and showing them on the website, Google and Facebook

**Ground rules** (Google review policy, Meta policy, and India's consumer-protection rules on online reviews):
- Only real customers write reviews. Agents and staff never write, edit or post a review as a customer.
- Ask **every** buyer, not just happy ones. No discount, gift or contest in exchange for a review.
- Never re-post a review without the customer's permission. Show the first name and city only.
- Every review, good or bad, gets a polite reply.

## 1. Where reviews appear, and how

| Place | How reviews get there | Cost |
|---|---|---|
| **Website (grasscrafts.com)** | Judge.me widgets on product pages, star badges in collections, all-reviews widget on /pages/review-us. Website orders get Judge.me's automatic review-request email. Reviews from WhatsApp, Facebook or email are added with the customer's permission through the Judge.me CSV import. | Free plan |
| **Google Search** | Judge.me adds star rich snippets to product pages, so stars can appear in Google results. Google decides when to show them. | Free plan |
| **Google Shopping** | Judge.me pushes product reviews to Google Merchant Center. Needs a Merchant Center account. | Paid "Awesome" plan (about $15/month); skip for now |
| **Google Business Profile** | **No app can post reviews there.** Only customers can, using the Google review link or the QR card. Our Google Business agent replies to every review and may post a "customer story" update quoting a review the customer has allowed us to use. | Free |
| **Facebook Page** | Customers recommend the Page through the Reviews tab (facebook.com/142803116227246/reviews). Our Facebook agent posts one "customer review" card a week, built from a Judge.me review or a review the customer allowed us to use, with their photo if they gave one. Judge.me's automatic social sharing may need the paid plan; we don't rely on it. | Free |

## 2. Getting more reviews

- **Website orders:** Judge.me sends the request automatically. **This only works once orders are marked "Fulfilled" in Shopify.** Today all but 2 orders show UNFULFILLED, so Judge.me sends nothing.
- **QR card in every parcel:** files are in `marketing/review_card/`. It links to Google, and to /pages/review-us for the website and Facebook.
- **Facebook Live and WhatsApp buyers:** Sristi sends the WhatsApp message below from 6290744782, 3–5 days after delivery.
- **B2B clients:** Sristi or Amit send the testimonial email below.
- **Past website buyers:** 16 personal requests were sent on 17 Oct (`outreach/review_requests.json`).

### WhatsApp message for Live and WhatsApp buyers (Sristi sends from her phone)
> Hi {name} 🙏 This is Sristi from GrassCrafts. I hope your {product} reached you safely and that you're enjoying it.
> Could you spare a minute to share an honest review? It really helps our artisans.
> ⭐ Google: https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA
> 🛍️ Our website (and Facebook): https://grasscrafts.com/pages/review-us
> If you send me a line and a photo here, may I share it on our website with your first name and city? Thank you!

Send it once only, no reminders. If they reply with a review and say yes, forward it to amit2sap@gmail.com, or save it in the "Reviews" WhatsApp chat, so the agents can add it to the website.

### Email to B2B clients
Clients: My E-haat Display Centre (HCL Foundation), Grill Splendour Services, VBev, Broadarks Technology, Ru & Ki Gifts. Their contacts are with Sristi; they're not in Shopify.

> **Subject:** A short testimonial for GrassCrafts?
>
> Dear {name},
>
> Thank you for choosing GrassCrafts for {order / occasion}. We hope the {products} worked well for {company}.
>
> Would you be willing to share 2–3 lines about your experience? For example: quality, finishing, delivery and how your team or clients liked the pieces. With your permission, we'd show it on our website and wholesale page with your name, designation and company.
>
> If it's easier, a Google review helps us a lot too: https://search.google.com/local/writereview?placeid=ChIJj8JSa12f-DkRUC8tUXwc-kA
>
> Warm regards,
> Sristi Dey, Founder, GrassCrafts
> +91 62907 44782 | grasscrafts.com

## 3. Pipeline: from review to website (agents)

1. **Capture.** Any review received by email, WhatsApp (forwarded), a Facebook comment or Messenger goes into `outreach/reviews_collected.json` only with explicit permission. Fields: name (first name + city), text, rating (only if the customer gave one), date, product, source, permission quote, photo URL.
2. **Export (Email & Actions agent, every Monday).** Convert new entries into `outreach/judgeme_import_<date>.csv` (columns as in `judgeme_import_TEMPLATE.csv`). Fill in `source` (e.g. "whatsapp", "facebook", "email") and `product_handle`. Email it to the owner to upload in Judge.me → Reviews → Import → CSV. Imported reviews show as unverified; that's honest and expected.
3. **Reuse (on posting days).**
   - **Facebook agent:** one review card a week.
   - **Instagram agent:** one review story or post a week.
   - **Google Business agent:** one "customer story" update every 2 weeks.
   - **Website agent:** quote B2B testimonials on /pages/wholesale-corporate-gifting.
   - In every case, quote the review exactly. Never edit its meaning.
4. **Replies.** The Google Business agent replies to Google reviews within 24 h. Judge.me reviews get a reply from the owner in Judge.me; the agents draft it in the daily email.
