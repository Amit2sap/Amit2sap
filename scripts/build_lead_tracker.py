#!/usr/bin/env python3
"""Build the GrassCrafts lead tracker (sales/lead_tracker.xlsx).

Re-run at the end of every Email & Actions run:  python3 scripts/build_lead_tracker.py
Sources (recorded data only, nothing invented): outreach/leads/*.json, outreach/sent_log.json,
outreach/competitor_customers.json, reports/agents/handoff.md, reports/hot_leads_2026-10-22.md.
The handoff / hot-leads / warm_leads facts are read from the files where structured
(sent_log warm_leads, handoff 'bounces to do_not_send' lines); the per-lead reply details
transcribed from those documents live in REPLIES below and must be extended when new replies arrive.
"""
import json, glob, re, os, collections, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = lambda *a: os.path.join(ROOT, *a)

COLS = ["Priority", "Segment", "Company", "City", "Contact name", "Role", "Email", "Phone (business)",
        "Source URL", "Buying signal", "Occasion/deadline", "Status", "First emailed", "Last contact",
        "Last reply (short)", "Next action", "Owner", "Notes"]

# ---- recorded facts keyed by lower-case email (from sent_log warm_leads, handoff.md, hot_leads_2026-10-22.md) ----
# priority, status, first, last, reply, next, owner, deadline(ISO for sorting), extra fields
R = {
 "ekta.smile@gmail.com": dict(priority="Hot", status="hot - with Sristi", first="2026-10-18", last="2026-10-18",
    reply="Website bulk form: 500 water hyacinth rectangular placemats for corporate gifting, needed by 2 Nov 2026",
    next="Sristi: check weaving capacity for 500 by 2 Nov (stock ~108), then call/WhatsApp and quote. If 2 Nov not possible, tell her early.",
    owner="Sristi", deadline="2026-11-02", company="Ekta Bagla Agarwal (Mumbai; company not given)", contact="Ekta Bagla Agarwal",
    phone="+91 98202 14335", segment="website_enquiry", city="Mumbai", source="sent_log.json warm_leads (website bulk form)",
    signal="Bulk quote request: 500 handwoven water hyacinth rectangular placemats", occasion="Corporate gifting; needed by 2 Nov 2026"),
 "sales@upahaarcorporategifts.com": dict(priority="Hot", status="hot - with Sristi", first="2026-10-15", last="2026-10-22",
    reply="20 Oct: 'Please share price list'", next="Sristi: reply in the Gmail thread with price list and MOQ; ask volumes and dates.",
    owner="Sristi", deadline="", company="Upahaar Corporate Gifting Solution", city="Nashik", segment="corporate",
    phone="74980 09312 / 91455 93366 (from web search; verify)", source="sent_log.json warm_leads",
    signal="Asked for price list to offer our range to their corporate clients", occasion="Not stated (likely Diwali / year-end)",
    notes="22 Oct: we acknowledged in thread (Sristi CC). No prices sent. Duplicate acknowledgement by a parallel agent possible."),
 "contact@nawalfoundation.in": dict(priority="Hot", status="hot - with Sristi", first="", last="2026-10-17",
    reply="Partnership interest: wants our baskets in her corporate hampers", next="Sristi: send trade price list (3-4 basket sizes, MOQ), call to agree model. Partnership terms are owner decision.",
    owner="Sristi", deadline="", company="Hamperology / Nawal Foundation", contact="Dr. Arrpita Kapoor", role="Founder", segment="corporate",
    source="sent_log.json warm_leads", signal="Wants to use our baskets in hampers for corporate clients",
    occasion="Diwali / year-end hampers", notes="17 Oct: we asked volumes, model, cities, call; Sristi CC'd."),
 "contact@cherishx.com": dict(priority="Warm", status="replied", first="", last="2026-10-17", reply="Replied 17 Oct (in thread); only an auto-reply since",
    next="Sristi: send price list in the thread when ready.", owner="Sristi", company="CherishX", segment="corporate",
    source="sent_log.json warm_leads", signal="Wholesale baskets for gifting/experiences; we offered price list + samples",
    occasion="Diwali (volumes asked, not given)"),
 "yogesh@farmley.com": dict(priority="Warm", status="replied", first="2026-10-15", last="2026-10-15", reply="Referred to this contact by wecare@farmley.com",
    next="Sristi: send price list once ready.", owner="Sristi", company="Farmley", segment="gourmet", source="sent_log.json warm_leads",
    signal="Baskets as gift packaging", notes="Proposal + catalogue sent 15 Oct."),
 "marketing@hungerinc.in": dict(priority="Warm", status="replied", first="2026-10-15", last="2026-10-15", reply="Redirected by gifting team to this contact",
    next="Sristi: send price list once ready.", owner="Sristi", company="Bombay Sweet Shop (Hunger Inc.)", segment="gourmet",
    source="sent_log.json warm_leads", signal="Baskets as gift packaging", notes="Proposal + catalogue sent 15 Oct."),
 "marketingsupport.senco@sencogold.co.in": dict(priority="Warm", status="replied", first="2026-10-16", last="2026-10-16", reply="Customer care redirected us to this contact",
    next="Sristi: send price list once ready.", owner="Sristi", company="Senco Gold & Diamonds", segment="diamond_jewellery",
    source="sent_log.json warm_leads", signal="Festive / store gifting", notes="Pitch + catalogue sent 16 Oct."),
 "connect.jaypore@abfrl.adityabirla.com": dict(priority="Warm", status="replied", first="2026-10-16", last="2026-10-16", reply="Customer care redirected us to this contact",
    next="Sristi: send price list once ready.", owner="Sristi", company="Jaypore (ABFRL)", segment="ethnic_wear",
    source="sent_log.json warm_leads", signal="Festive / store gifting", notes="Pitch + catalogue sent 16 Oct."),
 "care@giva.co": dict(priority="Warm", status="replied", first="", last="", reply="Asked us to fill their collaboration Google Form",
    next="Sristi/Amit: submit GIVA collaboration form (needs prices and terms).", owner="Sristi", company="GIVA", segment="diamond_jewellery",
    source="sent_log.json warm_leads", signal="Collaboration form requested"),
 "corporate@theknotcompany.in": dict(priority="Warm", status="replied", first="", last="2026-10-16", reply="16 Oct: will keep us in mind",
    next="Follow up ~30 Oct with New Year / client gifting angle.", owner="Agent", deadline="2026-10-30", company="The Knot Company",
    segment="corporate", source="sent_log.json warm_leads", signal="Corporate / client gifting"),
 "mmr.blr@denhotels.com": dict(priority="Warm", status="replied", first="2026-10-22", last="2026-10-22",
    reply="22 Oct: Materials Manager asked for our contact details; we replied with Sristi's details (CC Sristi)",
    next="Sristi: expect his contact; send trade catalogue and discuss room/laundry baskets, trays, planters. No prices/samples promised.",
    owner="Sristi", company="The Den Bengaluru (Whitefield)", contact="Bijin Ansalin", role="Materials Manager", segment="hotels", city="Bengaluru (Whitefield)",
    phone="+91 9513677316 / +91 8071117316 (his signature)", source="sent_log.json warm_leads", signal="Replied to hotels cold email asking for contact details",
    notes="Warm, not hot (no price/quote/sample ask yet)."),
 "abhissek.basu@theleela.com": dict(priority="Warm", status="replied", reply="22 Oct: 'Thank you for reaching out' (courtesy only)",
    next="If no further reply by ~29 Oct, short personal follow-up from Sristi.", owner="Agent", deadline="2026-12-01"),
 "info@weavehand.com": dict(priority="Warm", status="replied", first="2026-10-22", last="2026-10-22",
    reply="22 Oct: 'will discuss with my team and get back to you soon'", next="Normal follow-up timing; no reply needed now.", owner="Agent",
    company="WeaveHand", contact="Team WeaveHand", segment="corporate", source="sent_log.json warm_leads", signal="Replied to corporate cold email"),
 # in hot-leads report, no reply yet
 "info@ele-na.com": dict(next="Sristi: short personal email this week; no prices in writing.", owner="Sristi", deadline="2026-11-01", notes="In 22 Oct hot-leads report (#7). Spa opens 1 Nov 2026."),
 "hemant@swageazy.com": dict(next="Personal email or LinkedIn note to Hemant before 7 Nov.", owner="Sristi", deadline="2026-11-07", notes="In 22 Oct hot-leads report (#9). Alternate: Sameer Wahie, Founder, sameer@swageazy.com."),
 "reservations@thetivolihotels.com": dict(next="Call banquet team early Nov; ask for purchase/events head.", owner="Sristi", deadline="2026-11-15", notes="In 22 Oct hot-leads report (#10). Opens 15 Nov 2026."),
 "ananya.verma@lucirajewelry.com": dict(next="Follow up in ~1 week; call to store number is fine.", owner="Sristi", notes="In 22 Oct hot-leads report (#13)."),
 "care@chandukakasaraf.in": dict(next="Personal email or call this week.", owner="Sristi", notes="In 22 Oct hot-leads report (#14)."),
 "info@snusha.com": dict(next="Personal email this week.", owner="Sristi", notes="In 22 Oct hot-leads report (#15)."),
 "connect@sattvagroup.in": dict(owner="Sristi", notes="In 22 Oct hot-leads report (#16)."),
 "reservations@riomara.com": dict(status="bounced", next="Optional: call hotel or find pre-opening GM on LinkedIn; Lead Research looking for a new contact.", owner="Sristi", deadline="2026-12-01",
    notes="reservations@riomara.com bounced 22 Oct (550 no such user). In hot-leads report (#12)."),
}

# non-email-keyed extra rows from hot_leads_2026-10-22.md (no contact email recorded)
EXTRA = [
 dict(priority="Hot", segment="export_rfq", company="go4WorldBusiness: Netherlands importer", city="Netherlands", email="", phone="",
      source="sales/buyer_intelligence_2026-10-18.md section 2 (go4WorldBusiness request #1329192)",
      signal="Request for seagrass, water hyacinth, rattan or bamboo baskets, 200-500 of each type", occasion="Posted 14 Oct 2026",
      status="new", next="Owner decision on export orders; check export papers (IEC etc.), then reply on go4WorldBusiness.", owner="Sristi",
      notes="No contact recorded (behind go4WorldBusiness login). Hot-leads report #17.", deadline=""),
 dict(priority="Hot", segment="export_rfq", company="go4WorldBusiness: Hong Kong importer", city="Hong Kong", email="", phone="",
      source="sales/buyer_intelligence_2026-10-18.md section 2",
      signal="110x180 cm pandanus mats with cotton border; Indian suppliers welcome (we could offer Madurkathi)", occasion="One 20 ft container (~7,000 pcs); posted Sep 2026",
      status="new", next="Check Madurkathi at that size/volume, then reply on go4WorldBusiness.", owner="Sristi",
      notes="No contact recorded (go4WorldBusiness login). Hot-leads report #18.", deadline=""),
 dict(priority="Hot", segment="export_rfq", company="go4WorldBusiness: UAE importers (makhana)", city="UAE", email="", phone="",
      source="sales/buyer_intelligence_2026-10-18.md section 2",
      signal="Makhana, suta 4/5, 5% max broken, 10-20 kg PP bags; 1-4 x 40 ft containers", occasion="Posted Aug-Sep 2026 (repeats; similar asks from Greece, Thailand, Ireland)",
      status="new", next="Check grade, volume and export papers, then reply on go4WorldBusiness.", owner="Sristi",
      notes="No contact recorded (go4WorldBusiness login). Hot-leads report #19.", deadline=""),
 dict(priority="Cold", segment="real_estate", company="Century Real Estate", city="Bengaluru", email="", phone="+91 80 4433 4400",
      source="https://www.boxupgifting.com/blogs/case-studies/home-is-where-the-heart-is-key-handover-gift-hampers-from-century-real-estate",
      signal="Buys key-handover hampers from BoxUp; launched The Astoria (334 homes) 10 Oct", occasion="Handovers ongoing",
      status="new", next="Call Century's office (phone only) and ask for CRM / customer-experience head.", owner="Sristi",
      notes="Not contacted (no email). Hot-leads report #16. Phone from centuryrealestate.in/contact.", deadline=""),
]

MONTHS = {"jan":1,"feb":2,"mar":3,"apr":4,"may":5,"jun":6,"jul":7,"aug":8,"sep":9,"oct":10,"nov":11,"dec":12}
def deadline_from_text(t):
    t = (t or "").lower()
    m = re.search(r"(\d{1,2})\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s*(2026|2027)?", t)
    if m: return "%s-%02d-%02d" % (m.group(3) or "2026", MONTHS[m.group(2)], int(m.group(1)))
    m = re.search(r"(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s*(2026|2027)", t)
    if m: return "%s-%02d-01" % (m.group(2), MONTHS[m.group(1)])
    m = re.search(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\b", t)
    if m: return "2026-%02d-28" % MONTHS[m.group(1)] if MONTHS[m.group(1)] >= 10 else "2027-%02d-28" % MONTHS[m.group(1)]
    return ""

def main():
    sent_log = json.load(open(P("outreach/sent_log.json")))
    sent = {e.lower() for e in sent_log["sent"]}
    dns = {e.lower() for e in sent_log["do_not_send"]}
    handoff = open(P("reports/agents/handoff.md")).read()
    bounced_in_handoff = {e.lower() for e in re.findall(r"[\w.+-]+@[\w.-]+\.\w+", " ".join(
        l for l in handoff.splitlines() if "bounce" in l.lower() and "do_not_send" not in l.lower()))}

    rows, seen_email, seen_company = [], {}, {}
    def add(r):
        rows.append(r)
        if r["Email"]: seen_email[r["Email"].lower()] = r
        seen_company[re.sub(r"\W+", "", r["Company"].lower())] = r

    for f in sorted(glob.glob(P("outreach/leads/*.json"))):
        for x in json.load(open(f)):
            em = (x.get("email") or "").strip()
            o = R.get(em.lower(), {})
            st = x.get("status", "new")
            first = x.get("emailed") or ""
            if st == "dropped": status = "lost"
            elif st == "no_valid_contact": status = "bounced"
            elif em.lower() in dns: status = "do-not-contact"
            elif o.get("status"): status = o["status"]
            elif em.lower() in sent or first: status = "emailed"
            else: status = "new"
            if not first and em.lower() in sent: first = ""
            notes = " ".join(s for s in [x.get("notes") or x.get("note") or "", o.get("notes", "")] if s)
            if x.get("alt_email"): notes += " Alt email: %s." % x["alt_email"]
            occ = x.get("occasion", "")
            dl = o.get("deadline") or deadline_from_text(occ)
            add({"Priority": o.get("priority", "Cold"), "Segment": x["segment"], "Company": x["company"], "City": x.get("city", ""),
                 "Contact name": x.get("contact_name", ""), "Role": x.get("role", ""), "Email": em, "Phone (business)": x.get("business_phone", ""),
                 "Source URL": x.get("signal_url", ""), "Buying signal": x.get("signal", ""), "Occasion/deadline": occ, "Status": status,
                 "First emailed": o.get("first", first) or first, "Last contact": o.get("last", first) or first,
                 "Last reply (short)": o.get("reply", ""),
                 "Next action": o.get("next", "Send intro email" if status == "new" else ("Follow up if no reply" if status == "emailed" else "")),
                 "Owner": o.get("owner", "Agent"), "Notes": notes.strip(), "_dl": dl})

    for em, o in R.items():     # warm/hot records not in leads files
        if em in seen_email: continue
        wl = next((w for w in sent_log["warm_leads"] if w["contact"].lower() == em), {})
        add({"Priority": o["priority"], "Segment": o.get("segment", ""), "Company": o.get("company", wl.get("company", "")), "City": o.get("city", ""),
             "Contact name": o.get("contact", wl.get("person", "")), "Role": o.get("role", ""), "Email": em,
             "Phone (business)": o.get("phone", wl.get("phone", "")), "Source URL": o.get("source", ""), "Buying signal": o.get("signal", ""),
             "Occasion/deadline": o.get("occasion", ""), "Status": o["status"], "First emailed": o.get("first", ""), "Last contact": o.get("last", ""),
             "Last reply (short)": o.get("reply", ""), "Next action": o.get("next", ""), "Owner": o.get("owner", "Agent"),
             "Notes": " ".join(filter(None, [o.get("notes", ""), "Record: " + wl.get("status", "")[:400] if wl.get("status") else ""])),
             "_dl": o.get("deadline", "")})

    for e in EXTRA:
        k = re.sub(r"\W+", "", e["company"].lower())
        if k in seen_company:      # already a lead row: just attach the hot-leads-report action
            r = seen_company[k]
            r["Next action"], r["Owner"] = e["next"], e["owner"]
            r["Phone (business)"] = r["Phone (business)"] or e["phone"]
            r["Notes"] = (r["Notes"] + " " + e["notes"]).strip()
            continue
        add({"Priority": e["priority"], "Segment": e["segment"], "Company": e["company"], "City": e["city"], "Contact name": "", "Role": "",
             "Email": e["email"], "Phone (business)": e["phone"], "Source URL": e["source"], "Buying signal": e["signal"],
             "Occasion/deadline": e["occasion"], "Status": e["status"], "First emailed": "", "Last contact": "", "Last reply (short)": "",
             "Next action": e["next"], "Owner": e["owner"], "Notes": e["notes"], "_dl": e["deadline"]})

    for c in json.load(open(P("outreach/competitor_customers.json"))):
        key = re.sub(r"\W+", "", c["buyer"].lower())
        if key in seen_company or any(key in k or k in key for k in seen_company if len(k) > 5):
            r = next(v for k, v in seen_company.items() if k == key or (len(k) > 5 and (key in k or k in key)))
            r["Notes"] = (r["Notes"] + " Competitor customer: %s (%s)." % (c["competitor_used"], c["source_url"])).strip()
            continue
        add({"Priority": "Cold", "Segment": c["segment"], "Company": c["buyer"], "City": "", "Contact name": "", "Role": c.get("decision_maker_role", ""),
             "Email": "", "Phone (business)": "", "Source URL": c["source_url"], "Buying signal": "Buys %s from %s" % (c["products"], c["competitor_used"]),
             "Occasion/deadline": "%s; %s" % (c["occasion"], c["timing_month"]), "Status": "new", "First emailed": "", "Last contact": "", "Last reply (short)": "",
             "Next action": "Find a decision-maker contact", "Owner": "Agent", "Notes": "From competitor_customers.json (found %s)." % c["date_found"], "_dl": ""})

    # bounce flags recorded in handoff
    for r in rows:
        if r["Email"].lower() in bounced_in_handoff and r["Status"] in ("new", "emailed"):
            r["Status"] = "bounced"

    order = {"Hot": 0, "Warm": 1, "Cold": 2}
    rows.sort(key=lambda r: (order[r["Priority"]], r["_dl"] or "9999", r["Segment"], r["Company"]))

    wb = Workbook()
    hdr_fill = PatternFill("solid", fgColor="2F5D3A"); fills = {"Hot": "F8CBAD", "Warm": "FFE699"}
    def sheet(ws, data, cols):
        ws.append(cols)
        for c in ws[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = hdr_fill; c.alignment = Alignment(wrap_text=True, vertical="top")
        for r in data:
            ws.append([r[c] for c in cols])
            if r["Priority"] in fills:
                ws.cell(ws.max_row, 1).fill = PatternFill("solid", fgColor=fills[r["Priority"]])
        ws.freeze_panes = "D2"; ws.auto_filter.ref = ws.dimensions
        for i, c in enumerate(cols, 1):
            w = {"Source URL": 30, "Buying signal": 45, "Next action": 45, "Notes": 45, "Last reply (short)": 35, "Occasion/deadline": 30}.get(c, 18)
            ws.column_dimensions[get_column_letter(i)].width = w
        for row in ws.iter_rows(min_row=2):
            for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws = wb.active; ws.title = "Leads"; sheet(ws, rows, COLS)

    statuses = ["new", "emailed", "replied", "hot - with Sristi", "quoted", "won", "lost", "bounced", "do-not-contact"]
    segs = sorted({r["Segment"] for r in rows}); cnt = collections.Counter((r["Segment"], r["Status"]) for r in rows)
    s = wb.create_sheet("Summary"); s.append(["Segment"] + statuses + ["Total"])
    for c in s[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = hdr_fill
    for g in segs: s.append([g] + [cnt[(g, t)] for t in statuses] + [sum(cnt[(g, t)] for t in statuses)])
    s.append(["Total"] + [sum(cnt[(g, t)] for g in segs) for t in statuses] + [len(rows)])
    for c in s[s.max_row]: c.font = Font(bold=True)
    s.append([]); s.append(["Priority counts", "Hot", sum(r["Priority"] == "Hot" for r in rows), "Warm", sum(r["Priority"] == "Warm" for r in rows),
                            "Cold", sum(r["Priority"] == "Cold" for r in rows)])
    s.append(["Generated " + datetime.date.today().isoformat() + " by scripts/build_lead_tracker.py (static values)"])
    s.column_dimensions["A"].width = 22
    hot = [r for r in rows if r["Priority"] in ("Hot", "Warm")]
    sheet(wb.create_sheet("Hot leads"), hot, COLS)
    out = P("sales/lead_tracker.xlsx"); wb.save(out)
    print("rows", len(rows), "hot", sum(r["Priority"] == "Hot" for r in rows), "warm", sum(r["Priority"] == "Warm" for r in rows), "->", out)

if __name__ == "__main__":
    main()
