"""Master agent: turn a run snapshot (reports/master/<date>.json) into dashboard datasets.

Usage: python3 scripts/master_report.py 2026-10-29
Writes reports/master/data/{kpis,agents,actions,history,summary}.json and
reports/master/<date>.md (the short text report emailed to the owner).
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "reports" / "master"
DATA = MASTER / "data"


def change(k):
    if k.get("prev") in (None, 0) or k.get("value") is None:
        return None
    return round((k["value"] - k["prev"]) / abs(k["prev"]), 3)


def main(date):
    snap = json.load(open(MASTER / f"{date}.json"))
    DATA.mkdir(parents=True, exist_ok=True)

    kpis = []
    for k in snap["kpis"]:
        row = {f: k.get(f) for f in ("id", "area", "metric", "value", "prev", "unit", "window", "good", "source")}
        row["change"] = change(k)
        kpis.append(row)

    # history: one row per KPI per run, kept across runs for trend lines
    hist_path = DATA / "history.json"
    history = json.load(open(hist_path)) if hist_path.exists() else []
    history = [h for h in history if h["date"] != date]
    history += [{"date": date, "id": k["id"], "value": k["value"]} for k in kpis if k["value"] is not None]
    history.sort(key=lambda h: (h["id"], h["date"]))

    out = {
        "kpis": kpis,
        "agents": snap["agents"],
        "actions": snap["recommendations"],
        "history": history,
        "summary": [{"date": date, "takeaway": snap["takeaway"], "window": snap["window"]}],
    }
    for name, rows in out.items():
        json.dump(rows, open(DATA / f"{name}.json", "w"), indent=1, ensure_ascii=False)

    lines = [f"# GrassCrafts master report {date}", "", snap["takeaway"], "", "## Agent scores"]
    lines += [f"- {a['agent']}: {a['score']}/100 ({a['status']}). Next: {a['next']}" for a in sorted(snap["agents"], key=lambda a: -a["score"])]
    lines += ["", "## Top actions"] + [f"{r['rank']}. [{r['owner']}] {r['action']}" for r in snap["recommendations"]]
    lines += ["", "## Key numbers"]
    for k in kpis:
        ch = f" ({k['change']:+.0%} vs before)" if k["change"] is not None else ""
        lines.append(f"- {k['metric']}: {k['value']:,} {k['unit']}{ch} [{k['window']}]")
    (MASTER / f"{date}.md").write_text("\n".join(lines) + "\n")
    print("wrote", ", ".join(f"{n}={len(r)}" for n, r in out.items()))


if __name__ == "__main__":
    main(sys.argv[1])
