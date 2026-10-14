# GrassCrafts WhatsApp Assistant

An automatic WhatsApp customer-service assistant for **grasscrafts.com**. Customers message your WhatsApp Business number (+91 8100447884). The assistant:

- answers product questions with live prices, stock, photos and links from your Shopify store;
- tells customers the status of their order, but only when they message from the phone number on that order;
- knows your shipping, discount and payment rules from `store_facts.md`, a file you can edit;
- replies in English, Hindi or Bengali, matching the customer;
- passes bulk or corporate enquiries, custom orders, complaints and refunds to you on WhatsApp (and by e-mail if you set it up);
- lets you take over any chat with `/pause` and hand it back with `/resume`.

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
| `app/store.py` | Small database for chat memory, pauses and duplicate protection |
| `store_facts.md` | **Your editable shop rules** (shipping, offers, payments, contact) |
| `.env.example` | Every setting, with an explanation |
| `render.yaml` | One-click Render deployment |

---

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
   - **WhatsApp Business Account ID** (the WABA ID). Keep it for reference.

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

   `WHATSAPP_VERIFY_TOKEN` is generated for you.
4. Click **Apply** and wait until the deploy shows **Live** (about 3 to 5 minutes).
5. Copy your service URL, for example `https://grasscrafts-whatsapp-agent.onrender.com`. Open `<your URL>/healthz` in a browser. It should show `{"status":"ok"}`.
6. In Render, open the service, go to **Environment**, and copy the value of `WHATSAPP_VERIFY_TOKEN`. You need it in the next step.

Optional settings (`PAUSED`, `RATE_LIMIT_PER_HOUR`, SMTP e-mail and so on) are explained in `.env.example`. Add them under **Environment**. Render restarts the service after each change.

**About the free plan:** the service sleeps after 15 minutes without messages. The first message after a quiet period takes about a minute to answer (Meta keeps retrying, so nothing is lost). Restarts also wipe the small database, which clears chat memory and `/pause` settings. For a business number we recommend the **Starter** plan (about US$7 a month). To switch, set `plan: starter`, uncomment the `disk:` block in `render.yaml`, and set `DATABASE_PATH` to `/var/data/agent.db`. That keeps the bot always awake and its memory permanent.

## Step 6. Connect the webhook in Meta

1. On the free plan, open `<your URL>/healthz` first to wake the service.
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
- Create a **utility template** in WhatsApp Manager (for example a template named `owner_alert` with body text "New customer enquiry from {{1}}: {{2}}"). Once Meta approves it, set `OWNER_ALERT_TEMPLATE=owner_alert` in Render.
- You can also get e-mail copies by setting the `SMTP_*` settings. Gmail works with an App Password.

## Step 9. WhatsApp rules you should know

- **24-hour customer-service window.** When a customer messages you, you can reply freely for 24 hours. The bot only ever replies to incoming messages, so it always works within this window.
- **Business-initiated messages need approved templates.** To message someone first, or after 24 hours of silence, WhatsApp requires a **pre-approved message template**. Examples: order updates, "your order shipped", Diwali promotions, abandoned-cart reminders. This bot does not send those. Create templates in WhatsApp Manager and send them with a tool such as Shopify Inbox, Interakt, AiSensy or WATI, or extend this code.
- Meta may limit how many new customers you can start conversations with per day until your business is verified (**Business settings → Security center → Start verification**). Replying to customers who message you is not limited this way.
- Follow WhatsApp's Commerce and Business Policies. Don't use the bot for prohibited products, and respect customers who ask you to stop.

## Step 10. Rough monthly costs

| Item | Estimate |
|---|---|
| **Render** | Free plan ₹0 (sleeps when idle, memory resets). Starter about US$7 (≈₹600) per month plus about US$0.25 for a 1 GB disk. |
| **WhatsApp (Meta)** | Replies to customers inside the 24-hour window are **free**. Approved *utility* templates sent inside an open window are also free. Templates you send outside the window are charged per message. In India, roughly ₹0.12 for utility and about ₹0.80 for marketing. Check Meta's current rate card. |
| **Claude (Anthropic)** | `claude-sonnet-5-5` costs US$2 per million input tokens and US$10 per million output tokens. One customer message usually needs 1 to 3 model calls and costs about US$0.01 to 0.03 (₹1 to 2.5). The fixed instructions are cached, which cuts cost. About **1,000 customer messages a month comes to roughly US$15 to 30**. Set a spend limit in the Anthropic console. |
| **Shopify** | The custom app is free. |

**Typical small shop total:** about ₹1,500 to 3,000 a month on Render Starter, or less on the free plan.

**Ways to lower the cost:**
- Keep `ANTHROPIC_EFFORT=low`, which is the default.
- Lower `HISTORY_TURNS`.
- Set a model with lower prices through `ANTHROPIC_MODEL`. Test replies before switching.

---

## Safety built in

- Every webhook is checked against Meta's `X-Hub-Signature-256` with your App secret. Fake requests are rejected (HTTP 403).
- Duplicate deliveries (Meta retries) are ignored using the message ID.
- **Order privacy:** order details are shared only if the last 10 digits of the sender's WhatsApp number match the order's phone or shipping phone.
- **Rate limit:** about 20 messages per customer per hour. After that the bot sends one polite notice and stops replying for that hour.
- Logs at INFO level never contain message text or full phone numbers. Secrets are never logged or sent to the model.
- If anything fails (Claude, Shopify or WhatsApp), the customer gets a polite "please try again or contact us" message.
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
- Endpoints: `GET /webhook` (verification), `POST /webhook` (messages), `GET /healthz`.
