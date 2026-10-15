# GrassCrafts WhatsApp Assistant

An automatic WhatsApp customer-service assistant for **grasscrafts.com**. Customers message your WhatsApp Business number (+91 8100447884). The assistant:

- answers product questions with live prices, stock, photos and links from your Shopify store;
- tells customers the status of their order, but only when they message from the phone number on that order;
- knows your shipping, discount and payment rules from `store_facts.md`, a file you can edit;
- replies in English, Hindi or Bengali, matching the customer;
- collects bulk, corporate, wedding and reseller enquiries as **leads** (name, company, quantity, budget, dates...), alerts you with a neat summary and can send your corporate catalogue PDF;
- passes custom orders, complaints and refunds to you on WhatsApp (and by e-mail if you set it up);
- lets you take over any chat with `/pause` and hand it back with `/resume`;
- optional **automations** (all off until you switch them on): order confirmations, shipping updates with tracking, one abandoned-cart reminder, review requests, Diwali-style broadcasts to subscribed customers, and a daily summary for you;
- handles **STOP / START** (and "band karo") so customers can unsubscribe from offers;
- has a small password-protected **dashboard** at `/admin` with your leads (CSV download), recent chats and stats.

It never makes up prices, stock, delivery dates or discounts. If it doesn't know something, it hands the chat to you.

---

## How it works (one minute version)

```
Customer ──WhatsApp──> Meta Cloud API ──webhook──> this app (on Render)
                                                     │  ├─ Claude (writes the reply, picks tools)
                                                     │  ├─ Shopify Admin API (products, orders; read-only)
                                                     │  └─ SQLite (last 20 turns per customer, 24 h)
Customer <──WhatsApp── Meta Cloud API <──reply───────┘
```

| File | What it is |
|---|---|
| `app/main.py` | Web server: webhook endpoints, pause and resume, rate limiting |
| `app/whatsapp.py` | Sending and receiving WhatsApp messages, signature check |
| `app/shopify.py` | Product search, product details, order lookup with privacy check |
| `app/agent.py` | The assistant's instructions and tools |
| `app/store.py` | Small database for chat memory, pauses, leads, opt-outs, scheduled messages and stats |
| `app/automations.py` | Shopify webhooks: order, shipping, abandoned-cart and review messages |
| `app/scheduler.py` | Background timer that sends due messages and the daily digest |
| `app/consent.py` | STOP / START handling and who may receive which message |
| `app/broadcast.py` | `python -m app.broadcast`: offers to subscribed customers |
| `app/templates_sync.py` | `python -m app.templates_sync`: creates your message templates in Meta |
| `app/digest.py`, `app/admin.py` | Daily digest and the `/admin` dashboard |
| `templates/whatsapp_templates.json` | **Text of your WhatsApp templates** (English and Hindi) |
| `store_facts.md` | **Your editable shop rules** (shipping, offers, payments, returns, care, bulk, contact) |
| `.env.example` | Every setting, with an explanation |
| `render.yaml` | One-click Render deployment |

---

## Status as of 15 Oct 2026

| Item | Status |
|---|---|
| +91 8100447884 | Registered on the Cloud API (**CONNECTED**). Display name "Gift Hamper" is under Meta review; rename to "Grasscrafts" in WhatsApp Manager if wanted. |
| Phone number ID (`WHATSAPP_PHONE_NUMBER_ID`) | `1292616473939901` |
| WABA ID (`WHATSAPP_BUSINESS_ACCOUNT_ID`) | `28037860215843187` |
| Templates | All 11 (6 templates, en + hi) submitted, waiting for Meta approval. Check with `python -m app.templates_sync --status`. |
| Old duplicate entry of 8100447884 | Phone ID `800035566521159` in WABA `24086536527714735`, code expired. The API cannot delete it: remove it in WhatsApp Manager → Phone numbers. |
| Two-step verification PIN | Set during registration and given to the owner. It is not stored here. |

So in step 2 below, **skip "Add your real number"**: the number is already added and verified. Do the rest: create your own Meta app (step 1), then the system user and permanent token, and assign WABA `28037860215843187` to it. Then follow steps 3–7.

## Before you start

Have these ready:
- Admin access to the **Meta Business** account (business.facebook.com) that owns, or will own, +91 8100447884.
- Shopify admin access to grasscrafts.com.
- A GitHub account that can see this repository (Render deploys from it).
- A card for the Anthropic API (pay as you go). Render's free plan needs no card.
- About 1 to 2 hours.

> **Important about the number +91 8100447884:** a number connected to the Cloud API cannot also be used in the normal WhatsApp or WhatsApp Business phone app, **unless** you connect it with Meta's *Coexistence* option (WhatsApp Business app users can keep the app). If the number is on the WhatsApp Business app today, choose "Connect your existing WhatsApp Business app" when you add the number in step 2. Otherwise the number must be removed from the phone app first. Back up your chats first.

---

## Step 1. Create a Meta app with WhatsApp

1. Go to **developers.facebook.com**, log in, and click **My Apps → Create App**.
2. Use case: **Other**, then app type **Business**. Name it "GrassCrafts Assistant" and pick your Business portfolio.
3. On the app dashboard, find **WhatsApp** and click **Set up**. Choose your Business portfolio when asked.
4. Go to **App settings → Basic**:
   - Copy the **App secret** (click *Show*). This is `WHATSAPP_APP_SECRET`.
   - Add a **Privacy Policy URL** (for example `https://grasscrafts.com/policies/privacy-policy`). You need it to make the app Live.

## Step 2. Get the permanent token, phone number ID and WABA ID

**Add your real number**
1. In the app, open **WhatsApp → API Setup**. Under *Step 5: Add a phone number*, click **Add phone number** and add **+91 8100447884**. Set the display name to "GrassCrafts" (Meta reviews display names) and verify the number by SMS or call.
2. On the same page, choose +91 8100447884 in the **From** dropdown. Copy:
   - **Phone number ID**, a long number. This is `WHATSAPP_PHONE_NUMBER_ID`. It is **not** the phone number itself.
   - **WhatsApp Business Account ID** (the WABA ID). This is `WHATSAPP_BUSINESS_ACCOUNT_ID`, used to create your message templates (see Automations).

**Create a permanent token.** The token on the API Setup page expires in 24 hours, so don't use it.
1. Go to **business.facebook.com → Settings → Users → System users → Add**. Name it "grasscrafts-bot" and give it the **Admin** role.
2. Click **Assign assets**. Select **Apps → GrassCrafts Assistant → Full control**, and **WhatsApp accounts → your WABA → Full control**.
3. Click **Generate new token**. Pick the app, set expiry to **Never**, and tick the permissions **whatsapp_business_messaging** and **whatsapp_business_management**.
4. Copy the token now, because it is shown only once. This is `WHATSAPP_ACCESS_TOKEN`. Treat it like a password.

**Payment method:** in **WhatsApp Manager → Account tools → Payment methods**, add a card. Meta asks for this even when most messages are free (see the cost notes).

## Step 3. Create a Shopify custom app (read-only)

1. In Shopify admin, open **Settings → Apps and sales channels → Develop apps**. If asked, click **Allow custom app development**.
2. Click **Create an app** and name it "WhatsApp Assistant".
3. Under **Configuration → Admin API integration → Configure**, tick only these:
   - `read_products`
   - `read_orders`
   - `read_customers`
   Then click **Save**.
4. Open **API credentials → Install app → Install**.
5. Click **Reveal token once** and copy the **Admin API access token** (starts with `shpat_`). This is `SHOPIFY_ADMIN_TOKEN`.
6. The store domain is already set: `605e40-ba.myshopify.com`.

> The bot can only **read** your store. It cannot change products, orders or customers.
> Shopify shows order data older than 60 days only with the `read_all_orders` permission. Without it, the bot finds only recent orders, which covers most "where is my order" questions.

## Step 4. Get an Anthropic API key

1. Go to **console.anthropic.com** and sign up or log in.
2. Under **Billing**, add a card and buy some credit (US$10 is plenty to start). Turn on a **monthly spend limit** too, for example US$30.
3. Under **API keys**, click **Create key**, name it "grasscrafts-whatsapp", and copy it. This is `ANTHROPIC_API_KEY`.

The bot uses the model `claude-sonnet-5-5` by default. You can change it with `ANTHROPIC_MODEL`.

## Step 5. Deploy to Render

1. Go to **render.com** and sign up with GitHub.
2. Click **New + → Blueprint**, pick this repository, and choose the branch you want to run (for example `main` after merging).
3. Render reads `render.yaml` and creates **grasscrafts-whatsapp-agent**. It asks for the secret values:

   | Setting | Value |
   |---|---|
   | `WHATSAPP_APP_SECRET` | from step 1 |
   | `WHATSAPP_ACCESS_TOKEN` | permanent token from step 2 |
   | `WHATSAPP_PHONE_NUMBER_ID` | from step 2 |
   | `OWNER_WHATSAPP_NUMBER` | **your personal** WhatsApp number, e.g. `919876543210`. Not the shop number. |
   | `SHOPIFY_ADMIN_TOKEN` | from step 3 |
   | `ANTHROPIC_API_KEY` | from step 4 |

   `WHATSAPP_VERIFY_TOKEN` is generated for you. Render also asks for `SHOPIFY_WEBHOOK_SECRET`, `WHATSAPP_BUSINESS_ACCOUNT_ID` and `ADMIN_PASSWORD`; you can leave them empty now and fill them in when you set up the Automations.
4. Click **Apply** and wait until the deploy shows **Live** (about 3 to 5 minutes).
5. Copy your service URL, for example `https://grasscrafts-whatsapp-agent.onrender.com`. Open `<your URL>/health` in a browser. It should show `{"status":"ok"}`.
6. In Render, open the service, go to **Environment**, and copy the value of `WHATSAPP_VERIFY_TOKEN`. You need it in the next step.

Optional settings (`PAUSED`, `RATE_LIMIT_PER_HOUR`, SMTP e-mail and so on) are explained in `.env.example`. Add them under **Environment**. Render restarts the service after each change.

**About the free plan:** the service sleeps after 15 minutes without messages. The first message after a quiet period takes about a minute to answer (Meta keeps retrying, so nothing is lost). Restarts also wipe the small database, which clears chat memory and `/pause` settings. **The automations need the service awake** (abandoned-cart reminders, review requests and the daily digest are sent by a timer inside the app, and their queue lives in the database). On the free plan they only run while the service is awake and their queue is lost on restart. For a business number we recommend the **Starter** plan (about US$7 a month). To switch, set `plan: starter`, uncomment the `disk:` block in `render.yaml`, and set `DATABASE_PATH` to `/var/data/agent.db`. That keeps the bot always awake and its memory permanent.

## Step 6. Connect the webhook in Meta

1. On the free plan, open `<your URL>/health` first to wake the service.
2. In the Meta app, open **WhatsApp → Configuration → Webhook → Edit**:
   - **Callback URL:** `https://<your URL>/webhook`
   - **Verify token:** the `WHATSAPP_VERIFY_TOKEN` value from Render
   - Click **Verify and save**. If it fails, check the URL ends in `/webhook` and the token matches exactly.
3. Under **Webhook fields**, click **Manage** and **Subscribe** to **messages**. Leave the other fields off.
4. Make the app live: at the top of the app dashboard, switch **App Mode** from *Development* to **Live**. In Development mode, only test numbers you added yourself reach the bot.

## Step 7. Test it

From a phone that is **not** the owner number, send these to +91 8100447884:
1. "Hi, do you have cane trays under 1000?" You should get products with ₹ prices, links like `https://grasscrafts.com/products/...`, and maybe a photo.
2. "क्या आपके पास प्लांटर हैं?" The reply should be in Hindi.
3. "Is there any Diwali offer?" It should mention DIWALI10 (10% off ₹1,999 and above, until 12 Nov 2026).
4. "Where is my order #1001?" from a number that is **not** on that order. The bot should refuse politely and ask for the order e-mail.
5. "I need 100 gift hampers for my company." Your owner phone should get an alert, and the customer is told a person will follow up.

If nothing comes back, check **Render → Logs**. Logs show message IDs and the last 4 digits of numbers only, never message text. Common causes:
- A wrong `WHATSAPP_APP_SECRET` (logs say "invalid signature").
- An expired or wrong token (a WhatsApp API error, code 190).
- The app is still in Development mode.

## Step 8. Daily use: pause, resume and editing store facts

**Taking over a chat.** From your owner WhatsApp (`OWNER_WHATSAPP_NUMBER`), send these to the shop number:

| Message | What happens |
|---|---|
| `/pause 9876543210` | The bot stops replying to that customer. Their new messages are forwarded to you. |
| `/reply 9876543210 Hello! This is Amit from GrassCrafts...` | Sends your message to the customer from the shop number |
| `/resume 9876543210` | The bot starts replying to that customer again, remembering the conversation |
| `/status` | Shows which customers are paused |
| anything else | Shows the command list |

You can type numbers with or without +91 and spaces.

**Pausing the whole bot.** In Render, open **Environment**, set `PAUSED` to `true`, and save. The bot goes silent for everyone; owner commands still work. Set it back to `false` to resume.

**Editing store facts (shipping, offers, COD and so on):**
1. Open `whatsapp-agent/store_facts.md` on GitHub and click the pencil icon.
2. Change the text in plain English. Add a new offer line, delete expired offers, change the shipping threshold.
3. Click **Commit changes**. Render redeploys automatically in a few minutes.

Keep it factual and short. The bot treats every line as true, so **remove offers when they end**. DIWALI10 is already written with its end date.

**Escalation alerts.** Alerts are sent to your owner number as normal WhatsApp messages. WhatsApp only allows this if **you have messaged the shop number in the last 24 hours** (see the next section). You have two ways to make sure alerts always arrive:
- Send `/status` to the shop number once a day, **or**
- Create the **utility template** `owner_alert` (it is in `templates/whatsapp_templates.json`; see "Templates" under Automations). Once Meta approves it, set `OWNER_ALERT_TEMPLATE=owner_alert` in Render. Alerts and the daily digest then always arrive.
- You can also get e-mail copies by setting the `SMTP_*` settings. Gmail works with an App Password.

## Step 9. WhatsApp rules you should know

- **24-hour customer-service window.** When a customer messages you, you can reply freely for 24 hours. The bot only ever replies to incoming messages, so it always works within this window.
- **Business-initiated messages need approved templates.** To message someone first, or after 24 hours of silence, WhatsApp requires a **pre-approved message template**. Examples: order updates, "your order shipped", Diwali promotions, abandoned-cart reminders. The bot can send these through the optional **Automations** below, using the templates in `templates/whatsapp_templates.json`.
- Meta may limit how many new customers you can start conversations with per day until your business is verified (**Business settings → Security center → Start verification**). Replying to customers who message you is not limited this way.
- Follow WhatsApp's Commerce and Business Policies. Don't use the bot for prohibited products, and respect customers who ask you to stop. The bot does this automatically: see "Opt-in and opt-out" below.
- **Only message people who agreed to hear from you.** WhatsApp requires opt-in before you send business-initiated messages. Customers who are spammed block or report the number, which lowers your quality rating and can get the number restricted.

## Step 10. Rough monthly costs

| Item | Estimate |
|---|---|
| **Render** | Free plan ₹0 (sleeps when idle, memory resets). Starter about US$7 (≈₹600) per month plus about US$0.25 for a 1 GB disk. |
| **WhatsApp (Meta)** | Replies to customers inside the 24-hour window are **free**. Approved *utility* templates sent inside an open window are also free. Templates you send outside the window are charged per message. In India, roughly ₹0.12 for utility and about ₹0.80 to ₹0.90 for marketing. Check Meta's current rate card. See "What the automations cost" below. |
| **Claude (Anthropic)** | `claude-sonnet-5-5` costs US$2 per million input tokens and US$10 per million output tokens. One customer message usually needs 1 to 3 model calls and costs about US$0.01 to 0.03 (₹1 to 2.5). The fixed instructions are cached, which cuts cost. About **1,000 customer messages a month comes to roughly US$15 to 30**. Set a spend limit in the Anthropic console. |
| **Shopify** | The custom app is free. |

**Typical small shop total:** about ₹1,500 to 3,000 a month on Render Starter, or less on the free plan.

**Ways to lower the cost:**
- Keep `ANTHROPIC_EFFORT=low`, which is the default.
- Lower `HISTORY_TURNS`.
- Set a model with lower prices through `ANTHROPIC_MODEL`. Test replies before switching.

---

## Automations

Everything in this section is **optional** and is switched on with a setting in Render (**your service → Environment**; Render restarts the service after each change). Anything that messages a customer first starts **off**. All settings are explained in `.env.example`.

| Feature | Setting to turn it on | Default | Messages customers first? |
|---|---|---|---|
| Bulk / corporate lead capture | `LEAD_CAPTURE_ENABLED` | **on** | No (only replies) |
| Corporate catalogue PDF | `CATALOGUE_PDF_URL` | off (empty) | No (only when asked) |
| Order confirmation | `ORDER_CONFIRMATION_ENABLED=true` | off | Yes, utility template |
| Shipped + tracking | `SHIPPING_UPDATE_ENABLED=true` | off | Yes, utility template |
| Abandoned-cart reminder | `ABANDONED_CART_ENABLED=true` | off | Yes, marketing template |
| Review request | `REVIEW_REQUEST_ENABLED=true` | off | Yes, marketing template |
| STOP / START handling | `OPT_OUT_ENABLED` | **on** | No |
| Broadcast campaigns | `BROADCAST_ENABLED=true` + `--confirm` | off | Yes, marketing template |
| Daily digest for you | `DIGEST_ENABLED=true` | off | Only to you |
| Admin dashboard | `ADMIN_PASSWORD=<something long>` | off | No |

**Before switching on anything that sends templates:** create the templates and wait for Meta to approve them (next section), and set `SHOPIFY_WEBHOOK_SECRET` and the Shopify webhooks.

> **Render plan:** the free plan sleeps after 15 minutes and wipes the database on restart, so reminders, review requests and the digest can be late or lost. Use the **Starter** plan with the disk (Step 5). If you stay on the free plan for a while, at least set up a free uptime monitor (for example UptimeRobot or cron-job.org) to open `https://<your URL>/health` every 10 minutes.

### 1. Bulk, corporate, wedding and reseller leads

When a customer sounds like a bulk buyer ("200 hampers for our employees", "return gifts for a wedding", "boxes for my jewellery shop", "I want to resell"), the bot keeps helping them choose and, a little at a time, asks for: name, company, city, which products, quantity, budget per piece, needed-by date, customisation (logo or colours) and e-mail. It does not fire a list of questions at them, and it never quotes bulk prices itself.

As soon as it knows roughly what and how many, it **saves a lead** and sends you a summary on WhatsApp (and e-mail if set up) like:

```
🧺 New bulk lead #12 (corporate)
Name: Ravi   Company: Acme   City: Pune
Wants: jute gift hampers   Quantity: 200   Budget / piece: ₹500
Needed by: 25 Oct   Customisation: logo on box   Email: ravi@acme.example
WhatsApp: +91 98765 43210  https://wa.me/919876543210
```

If the customer adds details later, the same lead is updated and you get an "Updated lead" message. Follow up yourself (use `/pause <number>` to take over the chat), then mark the lead **contacted**, **won** or **lost** in `/admin`.

**Catalogue PDF:** upload your corporate catalogue to Shopify (**Content → Files → Upload**), copy its link (starts with `https://cdn.shopify.com/...`) and set `CATALOGUE_PDF_URL` to it. The bot then offers bulk customers the catalogue and sends it as a WhatsApp document. Leave it empty and the bot never mentions a catalogue.

### 2. Shopify order, shipping, abandoned-cart and review messages

How it works: Shopify tells the bot (a "webhook") when an order is placed, shipped, or a checkout is started. The bot queues the message in its database and a timer inside the app sends it when it is due. Each message is recorded, so **no customer gets the same message twice**, even if Shopify repeats a webhook or the app restarts.

- **Order confirmation** (`order_confirmation`, utility): straight after the order is placed.
- **Shipped** (`order_shipped`, utility): when you mark the order fulfilled in Shopify, with courier and tracking link.
- **Abandoned cart** (`abandoned_cart`, marketing): **one** reminder, `ABANDONED_CART_DELAY_MINUTES` (default 60) after the customer last touched their checkout. It is skipped if they have paid by then, if there is no phone number, or if they opted out. If they buy after the reminder, it counts as a **recovered cart** in your digest.
- **Review request** (`review_request`, marketing): `REVIEW_REQUEST_DAYS` (default 7) after fulfilment. Set `REVIEW_URL` to where you want reviews (for example your Google review link from Google Business Profile → **Ask for reviews**).

**Who receives what.** Order and shipping updates go to the phone on the order (unless you set `UTILITY_REQUIRES_OPT_IN=true`). Marketing messages (abandoned cart, review request, broadcasts) only go to customers who **opted in** and have **not opted out**. A customer counts as opted in when they messaged your WhatsApp number, ticked "email me with news and offers" / SMS marketing consent at Shopify checkout, or sent START. For the strongest WhatsApp consent, also edit your checkout's marketing checkbox text (**Settings → Checkout → Marketing options**) to mention WhatsApp, for example "Send me order updates and offers on WhatsApp".

**Set up the Shopify webhooks (about 5 minutes).** Easiest way, in the Shopify admin:
1. Go to **Settings → Notifications**, scroll to the bottom and click **Webhooks**.
2. At the bottom you'll see "Your webhooks will be signed with **<a long code>**". Copy that code into Render as `SHOPIFY_WEBHOOK_SECRET`.
3. Click **Create webhook** four times, one for each event below. Format **JSON**, URL `https://<your URL>/shopify/webhook`, webhook API version **2025-01** (or the latest):
   - **Order creation** (`orders/create`)
   - **Fulfillment creation** (`fulfillments/create`)
   - **Checkout creation** (`checkouts/create`)
   - **Checkout update** (`checkouts/update`)
4. Use **Send test** on one of them. In Render → Logs you should see `shopify webhook ... ok` (or `ignored` for Shopify's dummy data). `invalid HMAC` means the secret doesn't match.

Alternative: create the webhooks from your custom app (**Settings → Apps and sales channels → Develop apps → WhatsApp Assistant → Configuration → Webhooks**, or with the Admin API). In that case the signing secret is the app's **API secret key** (under API credentials), and the app needs the `read_orders` scope (plus `read_fulfillments`/`read_checkouts` if Shopify asks for them). Subscribe to the same four topics.

### 3. Opt-in and opt-out (always respected)

- A customer who sends **STOP**, **UNSUBSCRIBE**, **band karo** / **बंद करो** or taps the template's **Stop promotions** button is marked as opted out of marketing and gets a confirmation. They will still get order and shipping updates for orders they place.
- **START** (or **SUBSCRIBE**) subscribes them again.
- Only a message that is *just* that word counts, so "stop my order" is handled as a normal question (the bot passes cancellations to you).
- STOP works even while a chat is paused. A customer who opted out is never re-subscribed just by messaging again.
- Opt-outs are counted in your daily digest and the dashboard.

### 4. Broadcast campaigns (for example Diwali offers)

Broadcasts send an approved **marketing** template to everyone who is opted in. Run them from Render's **Shell** tab (Starter plan) or any computer with the same settings and database:

```bash
# 1. Dry run (the default): shows who would receive it. Nothing is sent.
python -m app.broadcast --template diwali_offer --segment opted_in --param "{name}" --param DIWALI10

# 2. Try a small batch for real (needs BROADCAST_ENABLED=true in Render first)
python -m app.broadcast --template diwali_offer --segment opted_in --param "{name}" --param DIWALI10 --limit 5 --confirm

# 3. Everyone
python -m app.broadcast --template diwali_offer --segment opted_in --param "{name}" --param DIWALI10 --confirm
```

- `--param` fills the template's `{{1}}`, `{{2}}`... in order; `{name}` becomes the customer's first name (or "there").
- Nothing is sent without `--confirm`, and `--confirm` refuses to run unless `BROADCAST_ENABLED=true`.
- It sends about 5 messages a second (`BROADCAST_RATE_PER_SECOND`), skips anyone who opted out, logs the result for every number, and never sends the same campaign to a number twice (re-running continues where it stopped). Use `--campaign diwali-2026-b` to send the same template again as a new campaign.
- Keep promotions occasional (a few a month at most). Meta limits how many marketing messages one person receives from all businesses, and too many blocks lower your number's quality rating.

### 5. Daily digest for you

Set `DIGEST_ENABLED=true` and `DIGEST_HOUR` (India time, default 9 for 9 am). Once a day you get a summary of the last 24 hours: conversations, new leads, escalations, abandoned carts recovered, opt-outs, automated messages sent and the top question topics. `DIGEST_CHANNELS` chooses `whatsapp`, `email` or both (e-mail needs the `SMTP_*` settings). Set `OWNER_ALERT_TEMPLATE=owner_alert` so the WhatsApp digest arrives even if you haven't messaged the shop number in 24 hours.

### 6. Admin dashboard

Set `ADMIN_USER` (default `admin`) and a long `ADMIN_PASSWORD`, then open `https://<your URL>/admin` and log in. You'll see message stats, all leads with a status dropdown (new / contacted / won / lost), **Download CSV** (`/admin/leads.csv`, opens in Excel or Google Sheets), recent conversations (phone numbers masked) and paused chats. With no password set, the dashboard is switched off.

### 7. Templates: create them and get them approved

The text of every template is in `templates/whatsapp_templates.json` (English, plus Hindi for customer messages):

| Template | Category | Used for |
|---|---|---|
| `order_confirmation` | UTILITY | Order placed |
| `order_shipped` | UTILITY | Order shipped, with tracking |
| `abandoned_cart` | MARKETING | Cart reminder |
| `review_request` | MARKETING | Review request |
| `owner_alert` | UTILITY | Alerts and digest to you |
| `diwali_offer` | MARKETING | Example broadcast |

Edit the wording in that file if you like (keep the `{{1}}`-style variables, and don't start or end a message with one). Then:
1. In Render, set `WHATSAPP_BUSINESS_ACCOUNT_ID` (your WABA ID from Step 2).
2. Open **Render → your service → Shell** and run `python -m app.templates_sync`. It submits every template and prints its status. (`python -m app.templates_sync --dry-run` only shows what would be sent.)
3. Meta usually reviews within minutes to a day. Check with `python -m app.templates_sync --status`, or in **WhatsApp Manager → Account tools → Message templates**. Wait for **APPROVED** before switching on the matching feature.
4. If a template is **REJECTED**, the reason is shown. Common causes: promotional words in a utility template (Meta may then re-categorise it as marketing), a variable at the very start or end, or missing sample values. Edit the text, delete the rejected one in WhatsApp Manager, and run the sync again.
5. Switch on `TEMPLATE_LANG=hi` to send the Hindi versions instead of English.

You can also create templates by hand in WhatsApp Manager: copy the name, category, language and body from the JSON file exactly.

### 8. Store facts the bot must not guess

`store_facts.md` now has sections for **returns and refunds**, **care of natural-fibre products**, **customisation and bulk minimum order quantity** and **lead times**. Lines that say `[OWNER: fill in ...]` are placeholders: the bot is told the answer is *not confirmed* and hands those questions to you instead of guessing. The text inside the brackets (like "e.g. 7 days") is never shown to the bot. To publish a rule, replace the whole bracket with the real policy and commit.

### What the automations cost (India)

Meta charges per **template message delivered** (prices change, check Meta's India rate card in WhatsApp Manager → Insights or the pricing page):

| Message | Category | Approximate cost each |
|---|---|---|
| Order confirmation, shipped update | Utility | about ₹0.12 to ₹0.15, and **free** if the customer messaged you in the last 24 hours |
| Abandoned cart, review request, broadcast | Marketing | about ₹0.80 to ₹0.90, always charged |
| Owner alert / digest to you | Utility | about ₹0.12, free if you messaged the shop number in the last 24 hours |
| Bot replies to customer messages | Service | free |

Example month: 300 orders (600 utility updates ≈ ₹80), 150 cart reminders (≈ ₹130), 250 review requests (≈ ₹215) and one 1,000-person Diwali broadcast (≈ ₹850) comes to roughly **₹1,300**, plus 18% GST. Template messages don't use Claude, so they add no Anthropic cost. Meta needs a payment method on the WhatsApp account (Step 2) before templates can be delivered.

---

## Safety built in

- Every webhook is checked against Meta's `X-Hub-Signature-256` with your App secret. Fake requests are rejected (HTTP 403).
- Duplicate deliveries (Meta retries) are ignored using the message ID.
- **Order privacy:** order details are shared only if the last 10 digits of the sender's WhatsApp number match the order's phone or shipping phone.
- **Rate limit:** about 20 messages per customer per hour. After that the bot sends one polite notice and stops replying for that hour.
- Logs at INFO level never contain message text or full phone numbers. Secrets are never logged or sent to the model.
- If anything fails (Claude, Shopify or WhatsApp), the customer gets a polite "please try again or contact us" message.
- Shopify webhooks are checked against `X-Shopify-Hmac-Sha256` with `SHOPIFY_WEBHOOK_SECRET`; unsigned or wrongly signed requests are rejected (HTTP 401), and repeated deliveries are ignored.
- Every automated message has a unique record in the database, so it is sent at most once. Marketing messages are never sent to anyone who opted out.
- The dashboard needs your admin password, masks phone numbers in the conversation list and protects the lead status form against cross-site requests.
- If the model declines a request, a server-side fallback model is tried first (`ANTHROPIC_REFUSAL_FALLBACK=true`, Claude API only). If you switch to a model that doesn't support this, set it to `false`.

## For developers

```bash
cd whatsapp-agent
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
pytest -q                       # all tests mock HTTP; no keys needed
cp .env.example .env            # fill in values
set -a; . ./.env; set +a
uvicorn app.main:app --reload --port 8000
# expose locally for Meta, e.g.: ngrok http 8000  -> use https://<id>.ngrok.app/webhook
```

**Notes:**
- The assistant runs a manual tool-use loop with the Anthropic Python SDK. Assistant turns are passed back unchanged during a turn, and only plain text turns are stored between messages.
- The system prompt and tools are prompt-cached.
- `store_facts.md` is re-read whenever it changes, so you can set `STORE_FACTS_PATH` to a file on a persistent disk and edit it without a redeploy.
- Endpoints: `GET /webhook` (verification), `POST /webhook` (messages), `POST /shopify/webhook` (Shopify, HMAC-verified), `GET /admin`, `POST /admin/leads/{id}/status`, `GET /admin/leads.csv` (HTTP Basic), `GET /health` (also `/healthz`).
- Background work: `app/scheduler.py` runs an asyncio loop (started only when an automation that needs it is on). Jobs are rows in the SQLite `jobs` table with a unique key; `sent_log` holds one row per business-initiated message key, claimed before sending, so retries and restarts never double-send (at-most-once).
- CLIs: `python -m app.broadcast --help`, `python -m app.templates_sync --help`.
- The tool set depends only on settings (`save_lead`, plus `send_catalogue` when `CATALOGUE_PDF_URL` is set), so the prompt cache stays warm.
