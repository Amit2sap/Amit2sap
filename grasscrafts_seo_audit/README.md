# GrassCrafts SEO audit — Search Console data (Claude, extracted 30 Oct 2026)

**Full dataset (all files, for ChatGPT):** download https://backend.composio.dev/api/v3/sl/n0PSmeVGgY (grasscrafts_seo_audit.zip, 336 KB; Composio file link). The repo keeps the summary files below; the full raw tables are in the zip only (the session network could not save the zip into the repo).

Property `sc-domain:grasscrafts.com`, data_state **final**, read-only (Composio GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY, row_limit 25,000 with pagination; no request hit the limit).

| Period | Dates | Clicks | Impressions | CTR | Avg pos |
|---|---|---|---|---|---|
| last_28d | 30 Sep–27 Oct 2026 | 166 | 9,072 | 1.83% | 8.15 |
| prev_28d | 2–29 Sep 2026 | 167 | 9,357 | 1.78% | 7.50 |
| last_3m | 28 Jul–27 Oct 2026 | 561 | 33,092 | 1.70% | 8.26 |
| last_6m | 28 Apr–27 Oct 2026 | 997 | 61,265 | 1.63% | 8.35 |
| last_12m | 28 Oct 2025–27 Oct 2026 | 1,623 | 124,524 | 1.30% | 8.28 |

## Files in the zip (row counts)
gsc_query_report.csv 7,887 (all periods) · gsc_query_page_report.csv 10,719 · gsc_page_report.csv 3,001 · gsc_daily_trend.csv 365 · gsc_country.csv 128 · gsc_device.csv 3 · gsc_search_appearance.csv 3 · gsc_query_country.csv 938 · gsc_query_device.csv 740 · gsc_totals.csv 5 · A_top_queries_by_impressions (28d 627, 3m 1,000) · B_top_queries_by_clicks (28d 627, 3m 1,000) · C2_competing_pages (28d 24, 3m 48) · D_zero_click_queries (28d 64, 3m 65) · E_striking_distance_pos4-20 (28d 59, 3m 79) · F_branded_vs_nonbranded · G_india_vs_international · README.md · data_dictionary.md.

In this folder: gsc_totals.csv, segments_last_28d.csv, E_striking_distance_pos4-20_last_3m.csv (all 79), C2_competing_pages_last_3m.csv (all 48), D_zero_click_top_last_3m.csv (top 25 of 65), executive_summary.md.

## Limits (record, don't treat as errors)
- Google hides rare/anonymised queries: 51–57% of impressions are in no query row (gsc_totals.csv). Query sums never equal site totals.
- searchAppearance pulled on its own (cannot combine with query/page). Country, device and query×country/device are last_28d only.
- "Branded" = regex `grass ?crafts?|grasscraft|abalone`; it also tags generic phrases like "kauna grass craft" and "sabai grass craft" as branded, so branded figures are slightly high.
- Step 2 (site audit from Shopify) is not in this extract yet.
