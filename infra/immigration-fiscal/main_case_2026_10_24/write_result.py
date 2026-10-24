"""Write the generated tables of RESULT.md (between its table markers) from derived/summary.json.

Every number is rounded once from the file. Decomposition rows use controlled rounding: printed parts must add to the
printed total, and the script stops if they cannot be made to. Prose and the log outside the markers are left as they are.
"""
import json
from decimal import ROUND_HALF_EVEN, Decimal
from pathlib import Path

HERE = Path(__file__).resolve().parent
S = json.loads((HERE / "derived" / "summary.json").read_text())
V = S["v10"]
START, END = "<!-- tables:start (write_result.py) -->", "<!-- tables:end -->"
NAMES = {"capital_rate_theta_bound": "22 capital rate bounded over θ", "k12_capital_where_enrolled": "23 K-12 capital where enrolled",
         "where_used_prices": "24 where-used prices (parks, colleges)", "public_land": "25 land under public capital"}


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


L = []
L.append("### Band [CALCULATION: derived/summary.json v10.band_bn, v10.cash_set_bn, v10.v9_band_bn]\n")
L.append("| | low $bn | high $bn |\n|---|---:|---:|")
for name, key in [("v9 (oct16), set", "v9_band_bn"), ("v10 candidate (oct24), set", "band_bn"), ("v9 (oct16), cash", "v9_cash_set_bn"), ("v10 candidate (oct24), cash", "cash_set_bn")]:
    L.append(f"| {name} | {fmt(V[key][0], 1)} | {fmt(V[key][1], 1)} |")
pm = V["per_member_usd"]
L.append(f"\nPer member of the {V['population']['with_coverage'] / 1e6:.2f}M lineage: set ${r(pm['set'][0], 0):,}–{r(pm['set'][1], 0):,}; "
         f"cash ${r(pm['cash'][0], 0):,}–{r(pm['cash'][1], 0):,}. [CALCULATION: v10.per_member_usd]\n")

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
        cells.append((("0.000" if v == 0 else f"{v:+}") if k else f"{v}") + ("*" if moved else ""))
    L.append(f"| {lab} | " + " | ".join(cells) + " |")
L.append("| **v10 candidate** | " + " | ".join(fmt(V["band_bn" if w == "set" else "cash_set_bn"][e]) for w, e in [("set", 0), ("set", 1), ("cash", 0), ("cash", 1)]) + " |")
L.append("\nPair interactions (set; cash is the same to 1e-9): " + "; ".join(
    f"{' + '.join(NAMES[x].split(' ')[0] for x in k.split('+'))}: {fmt(v['set'][0], 3, True)} / {fmt(v['set'][1], 3, True)}"
    for k, v in V["interactions"]["pairs"].items()) + f"; higher order {fmt(V['interactions']['higher_order']['set'][0], 6, True)} / "
    f"{fmt(V['interactions']['higher_order']['set'][1], 6, True)}. [CALCULATION: v10.interactions.pairs]\n")
L.append("Joint amounts at the end specifications (method mean; the return parts of 23 and 24 at item 22's rates), set: " + "; ".join(
    f"{NAMES[i].split(' ')[0]} {fmt(V['post_terms_at_ends_bn']['set'][0][i], 3, True)} / {fmt(V['post_terms_at_ends_bn']['set'][1][i], 3, True)}" for i in items)
    + ". [CALCULATION: v10.post_terms_at_ends_bn]\n")

o = V["item22"]
L.append("### Item 22 against its source [CALCULATION: v10.item22]\n")
L.append("| | low $bn | high $bn |\n|---|---:|---:|")
L.append(f"| capital return at the case rate, in-run (= the 7% arm's total) | {fmt(o['capital_at_case_rate_bn'][0])} | {fmt(o['capital_at_case_rate_bn'][1])} |")
L.append(f"| rate change, rate lane (`theta_pairing.bound.set.rate_delta_bn`) | {fmt(o['lane_rate_delta_bn'][0])} | {fmt(o['lane_rate_delta_bn'][1])} |")
L.append(f"| rate change, v10 in-run | {fmt(o['in_run_rate_delta_bn'][0])} | {fmt(o['in_run_rate_delta_bn'][1])} |")
L.append(f"| in-run minus lane | {fmt(o['in_run_minus_lane_bn'][0], 3, True)} | {fmt(o['in_run_minus_lane_bn'][1], 3, True)} |")
for lev in ("state_local", "state_local_highways", "federal"):
    L.append(f"| capital at case rate, {lev}: in-run / lane | {fmt(o['by_level_at_case_rate_bn']['in_run'][0][lev])} / {fmt(o['by_level_at_case_rate_bn']['lane'][0][lev])} "
             f"| {fmt(o['by_level_at_case_rate_bn']['in_run'][1][lev])} / {fmt(o['by_level_at_case_rate_bn']['lane'][1][lev])} |")
L.append("")

L.append("### Companions [CALCULATION: v10.companions; v9 values from main_case_2026_10_16/derived/summary.json v9.companions]\n")
L.append("| companion | v10 set $bn | v10 cash $bn | v9 set $bn | change, set |\n|---|---:|---:|---:|---:|")
LAB = {"lineage_arm_a": "count arm a", "lineage_arm_c": "count arm c", "lineage_c3_minus_se": "C3 − one SE", "lineage_c3_plus_se": "C3 + one SE",
       "shared_allocation": "household-sharing allocation, item 11 excluded", "school_within_district": "schools at the within-district 0.836 response",
       "first_year": "year-one response coefficients", "coverage_da_middle_0_17": "coverage from DA, through age 17", "coverage_da_middle": "coverage from DA, through 29",
       "health_residual_key_population": "item 21 population arm", "health_residual_key_no_ethnicity": "item 21 no-translation arm",
       "health_residual_key_plain_pooled": "item 21 plain-pooled arm"}
for k, c in V["companions"].items():
    v9b = c["v9_band_bn"]
    src = " (v9 recomputed; not in v9.companions)" if "v9_band_bn_recomputed" in c else ""
    cells = []
    for e in (0, 1):
        (pv9, pch), moved = controlled([v9b[e], c["band_bn"][e] - v9b[e]], c["band_bn"][e], 1)
        cells.append((f"{pv9}" + ("*" if moved[0] else ""), f"{pch:+}" + ("*" if moved[1] else "")))
    L.append(f"| {LAB.get(k, k)}{src} | {fmt(c['band_bn'][0], 1)}–{fmt(c['band_bn'][1], 1)} | {fmt(c['cash_set_bn'][0], 1)}–{fmt(c['cash_set_bn'][1], 1)} "
             f"| {cells[0][0]}–{cells[1][0]} | {cells[0][1]} / {cells[1][1]} |")
L_note = "\nA change marked * was moved $0.1bn by controlled rounding so that v9 + change = v10 as printed; v9 is printed as v9 prints it.\n"
for k, why in V["pending"].items():
    if why:
        L.append(f"| {k.replace('_', ' ')} | pending | pending | | |")
L.append(L_note)
lt = V["item25_mechanism_test"]
L.append(f"Item 25 mechanism test: {len(lt['lines'])} per-line charges (17 lines × central/low/high values × 2 ends) against "
         f"`{lt['lane']}/derived/land_by_line.csv` at the case rate; largest absolute error {lt['max_abs_error_bn']:.1e} $bn. "
         "This tests the mechanism only; it is not a v10 land result. [CALCULATION: v10.item25_mechanism_test]\n")
L.append(f"Gates passed: {S['checks']} (derived/checks.json). End specifications: set {V['end_specifications']['set']}, cash "
         f"{V['end_specifications']['cash']} (by method, numbered in the 64); same as v9: {V['end_specifications']['same_as_v9']}.")

block = START + "\n" + "\n".join(L) + "\n" + END
res = HERE / "RESULT.md"
text = res.read_text()
if START not in text or END not in text:
    raise SystemExit("[BLOCKED] RESULT.md has no table markers")
a, b = text.index(START), text.index(END) + len(END)
res.write_text(text[:a] + block + text[b:])
print("write_result: tables written,", len(L), "lines")
