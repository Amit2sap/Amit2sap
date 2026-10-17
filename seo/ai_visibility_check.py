"""Daily AI-search visibility check (run inside the Composio workbench, which provides web_search).

Paste into a workbench cell. It returns, for each buyer question, the brands found in the
search/answer text and whether GrassCrafts appears. Append the result to seo/ai_visibility_log.json.
"""
from concurrent.futures import ThreadPoolExecutor

QUESTIONS = [
    "Where can I buy sabai grass products online in India?",
    "Best place to buy madur mat online",
    "Where to buy kauna grass bags and baskets online India",
    "Eco-friendly corporate Diwali gifts India bulk handmade",
    "Handmade cane planters online India",
    "Bulk hamper baskets for Diwali India supplier",
    "Wedding return gift baskets India handmade",
    "Best sustainable home decor brands in India",
    "Handwoven jewellery boxes for jewellers India bulk",
    "What is GrassCrafts India",
]
BRANDS = ["grasscrafts", "brownliving", "brown living", "itokri", "zishta", "nestasia",
          "indiahandmade", "dastkar", "india craft house", "okhai", "jaypore", "tribes india",
          "kadam haat", "amazon", "flipkart", "indiamart"]


def check(q):
    r, e = web_search(q)  # noqa: F821 (workbench helper)
    t = (str(r) if r else "").lower()
    return {"q": q, "brands": [b for b in BRANDS if b in t], "grasscrafts": "grasscrafts" in t,
            "empty": not t.strip()}


def run():
    with ThreadPoolExecutor(5) as ex:
        res = list(ex.map(check, QUESTIONS))
    buyer = [r for r in res if not r["q"].startswith("What is GrassCrafts")]
    return {"score": sum(r["grasscrafts"] for r in buyer), "of": len(buyer), "results": res}
