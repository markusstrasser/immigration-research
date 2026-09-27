"""Gates for the IR-5 fraud-vs-cohort lane. Exit 1 if any gate fails.

1. Natality totals: US-resident births per year within 0.5% of NCHS published totals.
2. IR-5 series in derived/cohort_vs_ir5.csv equals the sister lane's ir5_flow.csv (read, not retyped),
   and cohort.py reads that file.
3. Birthplace series have no break at the file switches (1985 record weights end, 1989 new
   layout, 2003 revised layout): the growth rate into the switch year stays within 10 points of
   the mean of the growth rates either side, for Mexico-born and all foreign-born mothers.
3b. Every 2005+ birth row is labelled [MODEL]; every FY2005-24 comparison row uses measured
   births; every FY2026+ projection row is labelled [MODEL]; birth order is present.
4. Every fraud-rate quote appears in the archived sources/ text.
5. Consular Mexican IR-5 counts FY2019-24 equal the IR-5 column of the archived RVO Table VIII rows.
6. The figure exists.
"""
import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
FLOW = HERE.parent / "late_arrival_tail_2026_09_27" / "derived" / "ir5_flow.csv"
fails = []


def gate(ok, msg):
    print(f"  {'✓' if ok else '✗'} {msg}")
    if not ok:
        fails.append(msg)


def norm(s):
    return re.sub(r"[^a-z0-9%]+", " ", s.lower()).strip()


births = list(csv.DictReader((D / "births_mexico_mothers.csv").open()))
diffs = [abs(float(r["gate_pct_diff"])) for r in births if r["gate_pct_diff"] != ""]
gate(len(diffs) == 31 and max(diffs) <= 0.5,
     f"natality totals vs NCHS: {len(diffs)} years, max |diff| {max(diffs):.4f}%")

flow = {(r["country"], int(r["fy"])): float(r["ir5_parents"]) for r in csv.DictReader(FLOW.open())}
cv = list(csv.DictReader((D / "cohort_vs_ir5.csv").open()))
bad = [r["fy"] for r in cv if float(r["ir5_mexico"]) != flow[("mexico", int(r["fy"]))]
       or float(r["ir5_all"]) != flow[("all", int(r["fy"]))]]
gate(len(cv) == 20 and not bad, f"IR-5 FY2005-24 equals sister CSV (mismatches: {bad})")
gate("late_arrival_tail_2026_09_27" in (HERE / "cohort.py").read_text(), "cohort.py reads the sister lane's CSV")

for col in ("births_mexico_born_mother", "births_foreign_born_mother", "births_mexico_born_mother_first"):
    v = {int(r["birth_year"]): float(r[col]) for r in births if r[col] != ""}
    for y in (1985, 1989, 2003):
        g = v[y] / v[y - 1] - 1
        side = (v[y - 1] / v[y - 2] - 1 + v[y + 1] / v[y] - 1) / 2 if y + 1 in v else v[y - 1] / v[y - 2] - 1
        gate(abs(g - side) < 0.10, f"no break in {col} at {y}: growth {g:+.3f} vs neighbours {side:+.3f}")
share = {int(r["birth_year"]): float(r["mexico_born_share_of_mexican_origin"])
         for r in births if r["mexico_born_share_of_mexican_origin"]}
gate(abs(share[2003] - share[2002]) < 0.02,
     f"no break at 2002/03: Mexico-born share of Mexican-origin {share[2002]:.3f} -> {share[2003]:.3f}")

gate(all((r["status"] == "[MODEL]") == (int(r["birth_year"]) >= 2005) for r in births),
     "births: [MODEL] exactly on 2005+ rows")
gate(all(r["cohort_status"] == "measured" for r in cv), "FY2005-24 comparison uses measured births only")
proj = list(csv.DictReader((D / "cohort_projection.csv").open()))
gate(all((r["cohort_status"] == "[MODEL]") == (int(r["fy"]) >= 2026) for r in proj),
     "projection: [MODEL] exactly on FY2026+ rows")
gate(all(r["births_mexico_born_mother_first"] != "" for r in births), "first-birth series present (run r2)")

src_text = norm(" ".join(p.read_text(errors="replace") for p in (HERE / "sources").glob("*.txt")))
for r in csv.DictReader((D / "fraud_rates.csv").open()):
    # elided quotes ("...") are checked fragment by fragment
    frags = [norm(f)[:60] for f in re.split(r"\.\.\.|…", r["quote"]) if norm(f)]
    gate(bool(frags) and all(f in src_text for f in frags), f"quote archived: {r['source']} {r['year']}")

iv = {int(r["fy"]): int(r["ir5_iv_issued_mexico"]) for r in csv.DictReader((HERE / "reads" / "ir5_mexico_iv_issued.csv").open())}
for fy in range(2019, 2025):
    t = (HERE / "sources" / f"state_rvo_tableVIII_IR_by_birth_FY{fy}.txt").read_text()
    m = re.search(r"Mexico ((?:[\d,]+ ){11}[\d,]+)", t)
    ir5 = int(m.group(1).split()[8].replace(",", "")) if m else None
    gate(ir5 == iv[fy], f"RVO Table VIII FY{fy} Mexico IR-5 {ir5} == {iv[fy]}")

png = D / "cohort_vs_ir5.png"
gate(png.exists() and png.stat().st_size > 20_000, "figure present")

print(f"{'PASS' if not fails else 'FAIL'}: {len(fails)} failing gates")
sys.exit(1 if fails else 0)
