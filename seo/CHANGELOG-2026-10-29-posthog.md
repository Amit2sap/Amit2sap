# 29 Oct 2026 — PostHog analytics in a theme copy (owner approved)

**Theme copy:** "Grasscrafts – PostHog analytics 29 Oct" (gid://shopify/OnlineStoreTheme/189857562797), duplicated from live theme 189623959725 "makhana + shipping fix 25 Oct". NOT published — the owner publishes.

## Changes in the copy
1. New file `snippets/posthog.liquid`: PostHog loader + init (project 695384 "GrassCrafts website", public key phc_CK7…, host us.i.posthog.com). Page views, page leave, autocapture clicks, heatmaps, session replays with ALL form inputs masked; `person_profiles: identified_only` (no profiles for anonymous visitors); extra event `product_viewed` (handle, title, price) on product pages. Not loaded in the theme editor (`request.design_mode`).
2. `snippets/meta-tags.liquid`: one line added at the end: `{% render 'posthog' %}` (this snippet is rendered inside `<head>` of layout/theme.liquid). Backup: backups/theme/meta-tags_before_posthog_2026-10-29.liquid (md5 94fe115f…, identical to live).

## PostHog project settings (changed via PostHog connector)
Name "GrassCrafts website", timezone Asia/Kolkata, currency INR, authorised + recording domains https://grasscrafts.com and https://www.grasscrafts.com only, session replay ON (min 3 s, 30-day retention), heatmaps ON, dead-click capture ON, console logs OFF, IP addresses anonymised.

## Checks done
- Shopify accepted both files (no Liquid errors).
- Loader JS tested in Node: inserts https://us-assets.i.posthog.com/static/array.js and queues init + events.
- Could not load the preview from here (unpublished-theme preview needs the owner's logged-in browser).

## Not covered
Shopify checkout and thank-you pages are Shopify-hosted and do not use the theme, so PostHog sees visitors up to the cart / "Check out" click, not payment. Purchases stay in Shopify analytics.

## Owner steps
1. Preview: Shopify admin > Online Store > Themes > "Grasscrafts – PostHog analytics 29 Oct" > ⋯ > Preview. Click around a product, add to cart.
2. Publish it. Then PostHog > Activity should show events within a minute.
3. Privacy policy: add one line, e.g. "We use PostHog analytics to understand how visitors use our site; form fields are masked." (owner wording).

## Undo
Publish the previous theme 189623959725 again, or delete `snippets/posthog.liquid` and the last line of `snippets/meta-tags.liquid` in the live theme. Optionally turn off session replay in PostHog project settings.

## Change 2 (owner approved 29 Oct): removed the Women's Day FAQ schema from every article
`layout/theme.liquid` in the same copy: deleted the hidden FAQPage JSON-LD block that was output on EVERY blog article (3 Women's Day 2026 questions: "100% biodegradable", "over 200 women artisans in rural India, providing living wages, skill development, and safe ethical workspaces", "Women lead over 60% of grassroots sustainability movements"). Reason: unconfirmed claims (living wages, 60% stat) and FAQ markup that does not match the visible article (against Google's structured-data rules). BlogPosting schema and the Kash-flower article FAQ are kept.
Backup: backups/theme/theme.liquid_before_faq_removal_2026-10-29.liquid (md5 ff3a6417…, identical to live). New file md5 f7aaaa3b… (verified on Shopify).
Owner confirmed "over 200 women artisans" is true (see CLAUDE.md Business) — can be used in future visible content, without the living-wage wording.
Privacy policy paste-in: seo/privacy_policy_posthog_addition_2026-10-29.txt.
