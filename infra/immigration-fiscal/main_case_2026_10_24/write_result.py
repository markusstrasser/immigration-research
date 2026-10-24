"""Write the generated tables of RESULT.md (between its table markers) from derived/summary.json and the gate files.

Every number is rounded once from the file. Decomposition rows use controlled rounding: printed parts must add to the
printed total, and the script stops if they cannot be made to. Prose and the log outside the markers are left as they are.
Run: uv run --no-project python3 write_result.py [--dir DIR]. With --dir the tables are read from DIR.
"""
import csv
import json
import sys
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
D = Path(args[args.index("--dir") + 1]).resolve() if "--dir" in args else HERE / "derived"
S = json.loads((D / "summary.json").read_text())
CHECKS = json.loads((D / "checks.json").read_text())
API = json.loads((D / "api_check.json").read_text())
CONTRACT = json.loads((D / "contract.json").read_text())
IND = json.loads((D / "independent_check.json").read_text())
V = S["v10"]
SRC = CHECKS["rate_source"]
START, END = "<!-- tables:start (write_result.py) -->", "<!-- tables:end -->"
NAMES = {"capital_rate_theta_bound": "22 capital rate bounded over θ", "k12_capital_where_enrolled": "23 K-12 capital where enrolled",
         "where_used_prices": "24 where-used prices (parks, colleges)", "public_land": "25 land under public capital"}
for gate, ok in [("checks.json", CHECKS["pass"]), ("api_check.json", API["pass"]), ("contract.json", CONTRACT["pass"]), ("independent_check.json", IND["pass"])]:
    if not ok:
        raise SystemExit(f"[BLOCKED] {gate} did not pass; no tables written")
if SRC["sha256"] != IND["rate_sha256"]:
    raise SystemExit("[BLOCKED] independent check ran on a different rate file")


def r(x, d=3):
    return Decimal(repr(x)).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_EVEN)


def controlled(parts, total, d=3, fixed=(0,)):
    """Round parts so they add to the rounded total; move the adjustable parts with the largest rounding error by one
    unit. The base (index 0, a published v9 figure) stays as v9 prints it."""
    out = [r(p, d) + 0 for p in parts]  # + 0 drops a negative zero
    want, unit = r(total, d), Decimal(1).scaleb(-d)
    gap = int((want - sum(out)) / unit)
    free = [i for i in range(len(parts)) if i not in fixed]
    if abs(gap) > len(free):
        raise SystemExit(f"[BLOCKED] controlled rounding cannot close: gap {gap} units")
    order = sorted(free, key=lambda i: (Decimal(repr(parts[i])) - out[i]) * (1 if gap > 0 else -1), reverse=True)
    for i in order[:abs(gap)]:
        out[i] += unit if gap > 0 else -unit
    assert sum(out) == want
    return out, [o != r(p, d) for o, p in zip(out, parts)]


def fmt(x, d=3, sign=False):
    v = (r(x, d) if not isinstance(x, Decimal) else x) + 0
    if v == 0:
        return f"{abs(v)}"
    return f"{v:+}" if sign else f"{v}"


def signed(v, moved=False):
    return ("0.000" if v == 0 else f"{v:+}") + ("*" if moved else "")


L = []
L.append("### Band [CALCULATION: summary.json v10.band_bn, v10.cash_set_bn, v10.v9_band_bn, v10.v9_cash_set_bn]\n")
L.append("| | low $bn | high $bn |\n|---|---:|---:|")
for name, key in [("v9 (oct16), set", "v9_band_bn"), ("v10 candidate (oct24), set", "band_bn"), ("v9 (oct16), cash", "v9_cash_set_bn"), ("v10 candidate (oct24), cash", "cash_set_bn")]:
    L.append(f"| {name} | {fmt(V[key][0], 1)} | {fmt(V[key][1], 1)} |")
pm, pw = V["per_member_usd"], V["per_member_without_coverage_people_usd"]
L.append(f"\nPer member of the {V['population']['with_coverage'] / 1e6:.2f}M lineage: set ${r(pm['set'][0], 0):,}–{r(pm['set'][1], 0):,}; "
         f"cash ${r(pm['cash'][0], 0):,}–{r(pm['cash'][1], 0):,}. Per member of the {V['population']['without_coverage'] / 1e6:.2f}M before "
         f"coverage: set ${r(pw['set'][0], 0):,}–{r(pw['set'][1], 0):,}. [CALCULATION: v10.per_member_usd, v10.per_member_without_coverage_people_usd]\n")

L.append("### Change from v9 by item, standalone and joint [CALCULATION: v10.change_by_item, v10.interactions]\n")
L.append("Each item alone on v9, then the order dependence (joint minus the sum of standalones). Controlled rounding to "
         "$0.001bn; a part marked * was moved one unit so the column adds.\n")
L.append("| | set low | set high | cash low | cash high |\n|---|---:|---:|---:|---:|")
items = V["new_items"]
cols = {}
for which in ("set", "cash"):
    for e in (0, 1):
        v9 = V["v9_band_bn" if which == "set" else "v9_cash_set_bn"][e]
        parts = [v9] + [V["change_by_item"][i][which][e] for i in items] + [V["interactions"]["total"][which][e]]
        total = V["band_bn" if which == "set" else "cash_set_bn"][e]
        assert abs(sum(parts) - total) < 1e-9
        cols[(which, e)] = controlled(parts, total)
labels = ["v9 (oct16)"] + [NAMES[i] for i in items] + ["order dependence (joint − sum)"]
for k, lab in enumerate(labels):
    cells = []
    for c in [("set", 0), ("set", 1), ("cash", 0), ("cash", 1)]:
        v, moved = cols[c][0][k], cols[c][1][k]
        cells.append(signed(v, moved) if k else f"{v}" + ("*" if moved else ""))
    L.append(f"| {lab} | " + " | ".join(cells) + " |")
L.append("| **v10 candidate** | " + " | ".join(fmt(V["band_bn" if w == "set" else "cash_set_bn"][e]) for w, e in [("set", 0), ("set", 1), ("cash", 0), ("cash", 1)]) + " |")
L.append("\nJoint amounts at the end specifications (method mean; item 23's return part at item 22's rate), set: " + "; ".join(
    f"{NAMES[i].split(' ')[0]} {fmt(V['post_terms_at_ends_bn']['set'][0][i], 3, True)} / {fmt(V['post_terms_at_ends_bn']['set'][1][i], 3, True)}" for i in items)
    + ". [CALCULATION: v10.post_terms_at_ends_bn]\n")

o = V["item22"]
L.append("### Item 22's capital and rates [CALCULATION: v10.item22]\n")
L.append("| | low end | high end |\n|---|---:|---:|")
L.append(f"| capital return at the case rate, in-run (= the 7% arm's total), $bn | {fmt(o['capital_at_case_rate_bn'][0])} | {fmt(o['capital_at_case_rate_bn'][1])} |")
for lev in o["rates"]["rate_by_level_by_end"]:
    L.append(f"| {lev}: capital at the case rate $bn; rate | {fmt(o['by_level_at_case_rate_bn'][0][lev])}; {Decimal(repr(o['rates']['rate_by_level_by_end'][lev][0])) * 100:.4f}% "
             f"| {fmt(o['by_level_at_case_rate_bn'][1][lev])}; {Decimal(repr(o['rates']['rate_by_level_by_end'][lev][1])) * 100:.4f}% |")
L.append(f"| rate change, $bn | {fmt(o['rate_delta_at_ends_bn'][0])} | {fmt(o['rate_delta_at_ends_bn'][1])} |")
worst = max(f["max_abs_error_item22_bn"] for f in IND["files"].values())
L.append(f"\nIndependent check (`check_item22.py`, Python, without items.cjs): item 22 recomputed from each row's capital pieces × the "
         f"rate file on {sum(f['rows'] for f in IND['files'].values())} rows (set and cash); largest error {worst:.1e} $bn. "
         "[CALCULATION: independent_check.json]\n")

W = V["companions"]["where_used_prices_beside"]
L.append("### Item 24 beside the band: where-used prices, not identified [CALCULATION: v10.companions.where_used_prices_beside, v10.item24_beside]\n")
L.append(f"{W['status']}.\n")
L.append("| | low $bn | high $bn |\n|---|---:|---:|")
L.append(f"| v10 with item 24, set | {fmt(W['band_bn'][0], 1)} | {fmt(W['band_bn'][1], 1)} |")
L.append(f"| v10 with item 24, cash | {fmt(W['cash_set_bn'][0], 1)} | {fmt(W['cash_set_bn'][1], 1)} |")
for e_rows in [("parks", "parks_matched_municipal"), ("colleges, at v10's rates", "college_gross_book_capital")]:
    L.append(f"| {e_rows[0]}, at the end specifications | {fmt(W['parts_at_ends_bn'][0][e_rows[1]], 3, True)} | {fmt(W['parts_at_ends_bn'][1][e_rows[1]], 3, True)} |")
L.append(f"| change from v10 (set and cash) | {fmt(W['change_from_v10_bn']['set'][0], 3, True)} | {fmt(W['change_from_v10_bn']['set'][1], 3, True)} |")
L.append(f"| item 24 alone on v9 | {fmt(W['standalone_on_v9_bn']['set'][0], 3, True)} | {fmt(W['standalone_on_v9_bn']['set'][1], 3, True)} |")
fy = W["first_year"]
L.append(f"\nIn year one item 24 adds {fmt(fy['change_from_v10_first_year_bn']['set'][0])} / {fmt(fy['change_from_v10_first_year_bn']['set'][1])}: "
         f"the recreation response at the year-one ends (specifications {fy['ends'][0][0]} and {fy['ends'][0][1]}) is "
         f"{fy['parks_at_ends'][0][0]['recreation_response']}, and year one charges no capital return.\n")

L.append("### Companions [CALCULATION: v10.companions; v9 values from main_case_2026_10_16/derived/summary.json]\n")
L.append("| companion | v10 set $bn | v10 cash $bn | v9 set $bn | change, set |\n|---|---:|---:|---:|---:|")
LAB = {"lineage_arm_a": "count arm a", "lineage_arm_c": "count arm c", "lineage_c3_minus_se": "C3 − one SE", "lineage_c3_plus_se": "C3 + one SE",
       "shared_allocation": "household-sharing allocation, item 11 excluded", "school_within_district": "schools at the within-district 0.836 response",
       "first_year": "year-one response coefficients", "coverage_da_middle_0_17": "coverage from DA, through age 17", "coverage_da_middle": "coverage from DA, through 29",
       "health_residual_key_population": "item 21 population arm", "health_residual_key_no_ethnicity": "item 21 no-translation arm",
       "health_residual_key_plain_pooled": "item 21 plain-pooled arm",
       "ancestry_share_g4_at_nothing": "[FRAMING-SENSITIVE] ancestry share, G4+ at nothing (beside)",
       "ancestry_share_g4_at_bound": "[FRAMING-SENSITIVE] ancestry share, G4+ at its bound (beside)"}
for k, c in V["companions"].items():
    if k == "where_used_prices_beside":
        continue
    v9b = c["v9_band_bn"]
    cells = []
    for e in (0, 1):
        (pv9, pch), moved = controlled([v9b[e], c["band_bn"][e] - v9b[e]], c["band_bn"][e], 1)
        cells.append((f"{pv9}" + ("*" if moved[0] else ""), f"{pch:+}" + ("*" if moved[1] else "")))
    L.append(f"| {LAB.get(k, k)} | {fmt(c['band_bn'][0], 1)}–{fmt(c['band_bn'][1], 1)} | {fmt(c['cash_set_bn'][0], 1)}–{fmt(c['cash_set_bn'][1], 1)} "
             f"| {cells[0][0]}–{cells[1][0]} | {cells[0][1]} / {cells[1][1]} |")
L.append("\nA change marked * was moved $0.1bn by controlled rounding so that v9 + change = v10 as printed; v9 is printed as v9 prints it.\n")

with open(D / "sign_reversal.csv", newline="") as f:
    rows = list(csv.DictReader(f))
L.append("### Sign-reversal readings [CALCULATION: sign_reversal.csv oct16_*, oct24_*]\n")
L.append("| measure | v9 low | v9 high | v10 low | v10 high |\n|---|---:|---:|---:|---:|")
for row in rows:
    L.append(f"| `{row['measure']}` | {row['oct16_low']} | {row['oct16_high']} | {row['oct24_low']} | {row['oct24_high']} |")
L.append("")

for k, why in V["pending"].items():
    L.append(f"- Pending, {k.replace('_', ' ')}: {why}.")
lt = V["item25_mechanism_test"]
L.append(f"\nItem 25 mechanism test: {len(lt['lines'])} per-line charges against `{lt['lane']}/derived/land_by_line.csv` at the case "
         f"rate; largest absolute error {lt['max_abs_error_bn']:.1e} $bn. This tests the mechanism only; it is not a v10 land result. "
         "[CALCULATION: v10.item25_mechanism_test]\n")
L.append(f"Gates passed: {CHECKS['count']} in main_case (checks.json), {API['checks']} consumer-API checks (api_check.json), "
         f"v9's output contract {CONTRACT['verdict']} with {len(CONTRACT['self_checks'])} negative probes (contract.json). End specifications: set "
         f"{V['end_specifications']['set']}, cash {V['end_specifications']['cash']} (by method, numbered in the 64); same as v9: "
         f"{V['end_specifications']['same_as_v9']}.")

block = START + "\n" + "\n".join(L) + "\n" + END
res = HERE / "RESULT.md"
text = res.read_text()
if START not in text or END not in text:
    raise SystemExit("[BLOCKED] RESULT.md has no table markers")
a, b = text.index(START), text.index(END) + len(END)
res.write_text(text[:a] + block + text[b:])
print("write_result: tables written,", len(L), "lines")
