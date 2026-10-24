"""GrassCrafts Data & SEO agent toolkit (our own replacement for Windsor.ai + Ahrefs).

Run inside the Composio workbench, which provides run_composio_tool, web_search and invoke_llm.
Paste this file into a cell, then call run_all(). It returns a dict; save it as
seo/data/<date>.json and the markdown from to_markdown() as reports/agents/data_seo.md.

Coverage (Windsor/Ahrefs feature -> source):
- Rank tracking, keywords, pages, CTR  -> Google Search Console (google_search_console, connected)
- Striking-distance keywords, cannibalisation, content gaps -> derived from GSC
- Sitemap/index health, URL inspection -> GSC
- Backlinks / referring domains, Bing keywords -> Bing Webmaster Tools (bing_webmaster_tools)
- Traffic by channel, landing pages, revenue -> GA4 (google_analytics), plus Shopify analytics (Shopify MCP, run by the agent)
- Google Business Profile views, clicks, keywords -> Zapier GoogleMyBusinessCLIAPI (run by the agent)
- Brand mentions (unlinked) and SERP checks -> web_search
- AI-answer visibility -> seo/ai_visibility_check.py
Paid option for full backlink and keyword-volume data: DataForSEO (toolkit 'dataforseo', pay-as-you-go). Not connected.
"""
import datetime as _dt
import json

SITE = "sc-domain:grasscrafts.com"
BING_SITE = "https://grasscrafts.com/"
GA4_PROPERTY = "properties/358606571"

TARGET_KEYWORDS = [
    "sabai grass", "sabai grass bags", "sabai grass products", "sabai grass basket",
    "kauna grass", "kauna grass basket", "kauna grass bag",
    "madurkathi", "madur mat", "madurkathi mats", "asana mat",
    "sitalpati", "sitalpati mat", "cane planters", "cane basket", "cane planter online",
    "water hyacinth basket", "jute rug", "bamboo pendant lamp",
    "corporate gifts eco friendly", "diwali hamper basket", "wedding gift hamper basket",
    "return gift baskets", "jewellery box handmade", "storage baskets online india",
    "makhana", "mithila makhana", "plain makhana", "makhana online", "makhana gift hamper",
]


def _rows(r):
    d = r.get("data", r) if isinstance(r, dict) else {}
    return d.get("rows", []) if isinstance(d, dict) else []


def gsc(dims, start, end, limit=1000, filters=None):
    a = {"site_url": SITE, "start_date": start, "end_date": end, "dimensions": dims, "row_limit": limit}
    if filters:
        a["dimension_filter_groups"] = filters
    r, e = run_composio_tool("GOOGLE_SEARCH_CONSOLE_SEARCH_ANALYTICS_QUERY", a)  # noqa: F821
    return [] if e else _rows(r)


def windows(today=None):
    t = today or _dt.date.today()
    end = t - _dt.timedelta(days=3)  # GSC data lags about 3 days
    s = end - _dt.timedelta(days=27)
    pe = s - _dt.timedelta(days=1)
    ps = pe - _dt.timedelta(days=27)
    return [str(x) for x in (s, end, ps, pe)]


def summary():
    s, e, ps, pe = windows()
    cur, prev = gsc([], s, e), gsc([], ps, pe)
    return {"period": [s, e], "current": cur[0] if cur else {}, "previous": prev[0] if prev else {}}


def rank_tracker():
    s, e, ps, pe = windows()
    cur = {r["keys"][0]: r for r in gsc(["query"], s, e, 5000)}
    prev = {r["keys"][0]: r for r in gsc(["query"], ps, pe, 5000)}
    out = []
    for k in TARGET_KEYWORDS:
        c, p = cur.get(k), prev.get(k)
        out.append({"keyword": k,
                    "position": round(c["position"], 1) if c else None,
                    "prev_position": round(p["position"], 1) if p else None,
                    "impressions": int(c["impressions"]) if c else 0,
                    "clicks": int(c["clicks"]) if c else 0})
    return out


def striking_distance(min_impr=20):
    """Ranks 5-20 with demand: cheapest wins (title, internal links, content)."""
    s, e, _, _ = windows()
    rows = gsc(["query", "page"], s, e, 5000)
    hits = [{"query": r["keys"][0], "page": r["keys"][1], "position": round(r["position"], 1),
             "impressions": int(r["impressions"]), "clicks": int(r["clicks"])}
            for r in rows if 5 <= r["position"] <= 20 and r["impressions"] >= min_impr]
    return sorted(hits, key=lambda x: -x["impressions"])[:30]


def low_ctr_pages(min_impr=200):
    s, e, _, _ = windows()
    rows = gsc(["page"], s, e, 1000)
    out = [{"page": r["keys"][0], "impressions": int(r["impressions"]), "ctr": round(r["ctr"] * 100, 2),
            "position": round(r["position"], 1)} for r in rows if r["impressions"] >= min_impr and r["ctr"] < 0.01]
    return sorted(out, key=lambda x: -x["impressions"])[:20]


def cannibalisation(min_impr=30):
    """Queries where 2+ of our pages compete (often the homepage beats the category page)."""
    s, e, _, _ = windows()
    rows = gsc(["query", "page"], s, e, 5000)
    by = {}
    for r in rows:
        by.setdefault(r["keys"][0], []).append((r["keys"][1], int(r["impressions"]), round(r["position"], 1)))
    out = []
    for q, pages in by.items():
        if len(pages) > 1 and sum(p[1] for p in pages) >= min_impr:
            out.append({"query": q, "pages": sorted(pages, key=lambda x: -x[1])[:4]})
    return sorted(out, key=lambda x: -sum(p[1] for p in x["pages"]))[:20]


def sitemaps():
    r, e = run_composio_tool("GOOGLE_SEARCH_CONSOLE_LIST_SITEMAPS", {"site_url": SITE})  # noqa: F821
    if e:
        return {"error": str(e)}
    d = r.get("data", r)
    return [{"path": x.get("path"), "errors": x.get("errors"), "pending": x.get("isPending"),
             "lastDownloaded": x.get("lastDownloaded")} for x in d.get("sitemap", [])]


def bing():
    """Backlinks + Bing performance. Needs an active bing_webmaster_tools connection and a verified site."""
    out = {}
    r, e = run_composio_tool("BING_WEBMASTER_TOOLS_LIST_SITES", {})  # noqa: F821
    if e:
        return {"error": "bing not connected: " + str(e)[:120]}
    out["sites"] = r.get("data", r)
    r, e = run_composio_tool("BING_WEBMASTER_TOOLS_GET_INBOUND_LINKS", {"site_url": BING_SITE})  # noqa: F821
    out["inbound_links"] = (r.get("data", r) if not e else {"error": str(e)[:200]})
    r, e = run_composio_tool("BING_WEBMASTER_TOOLS_GET_SEARCH_PERFORMANCE",  # noqa: F821
                             {"site_url": BING_SITE, "report": "top_queries"})
    out["top_queries"] = (r.get("data", r) if not e else {"error": str(e)[:200]})
    return out


def ga4():
    a = {"property": GA4_PROPERTY, "dateRanges": [{"startDate": "28daysAgo", "endDate": "yesterday"}],
         "dimensions": [{"name": "sessionDefaultChannelGroup"}],
         "metrics": [{"name": "sessions"}, {"name": "totalUsers"}, {"name": "transactions"}, {"name": "purchaseRevenue"}]}
    r, e = run_composio_tool("GOOGLE_ANALYTICS_RUN_REPORT", a)  # noqa: F821
    if e:
        return {"error": "ga4 not connected: " + str(e)[:120]}
    d = r.get("data", r)
    rows = d.get("rows", [])
    return [{"channel": x["dimensionValues"][0]["value"], **{m: x["metricValues"][i]["value"]
             for i, m in enumerate(["sessions", "users", "transactions", "revenue"])}} for x in rows]


def brand_mentions():
    """Unlinked mentions = outreach list (ask them to add a link)."""
    out = []
    for q in ['"grasscrafts" -site:grasscrafts.com', '"GrassCrafts by Abalone"', '"grasscrafts.com" review']:
        r, e = web_search(q)  # noqa: F821
        out.append({"query": q, "result": (str(r)[:600] if r else str(e)[:120])})
    return out


def run_all():
    return {"date": str(_dt.date.today()), "summary": summary(), "rank_tracker": rank_tracker(),
            "striking_distance": striking_distance(), "low_ctr_pages": low_ctr_pages(),
            "cannibalisation": cannibalisation(), "sitemaps": sitemaps(), "bing": bing(), "ga4": ga4(),
            "brand_mentions": brand_mentions()}


def to_markdown(rep):
    c, p = rep["summary"]["current"], rep["summary"]["previous"]
    lines = [f"# Data & SEO report {rep['date']}",
             f"- **Google (last 28 days):** {int(c.get('clicks', 0))} clicks, {int(c.get('impressions', 0))} impressions, "
             f"average position {round(c.get('position', 0), 1)}; previous: {int(p.get('clicks', 0))} clicks, "
             f"{int(p.get('impressions', 0))} impressions.",
             "", "## Rank tracker", "| Keyword | Position | Previous | Impressions | Clicks |", "|---|---|---|---|---|"]
    for r in rep["rank_tracker"]:
        lines.append(f"| {r['keyword']} | {r['position'] or '–'} | {r['prev_position'] or '–'} | {r['impressions']} | {r['clicks']} |")
    lines += ["", "## Striking distance (positions 5–20)", "| Query | Page | Position | Impressions |", "|---|---|---|---|"]
    for r in rep["striking_distance"][:15]:
        lines.append(f"| {r['query']} | {r['page'].replace('https://grasscrafts.com', '')} | {r['position']} | {r['impressions']} |")
    lines += ["", "## Pages competing for the same query"]
    for r in rep["cannibalisation"][:10]:
        lines.append(f"- **{r['query']}:** " + "; ".join(f"{u.replace('https://grasscrafts.com', '')} ({i} impr, pos {pos})" for u, i, pos in r["pages"]))
    lines += ["", "## Low-CTR pages (rewrite titles and descriptions)"]
    for r in rep["low_ctr_pages"][:10]:
        lines.append(f"- {r['page'].replace('https://grasscrafts.com', '')}: {r['impressions']} impressions, CTR {r['ctr']}%, position {r['position']}")
    lines += ["", f"- **Bing:** {('connected' if 'error' not in rep['bing'] else rep['bing']['error'])}",
              f"- **GA4:** {('connected' if not (isinstance(rep['ga4'], dict) and 'error' in rep['ga4']) else rep['ga4']['error'])}"]
    return "\n".join(lines)
