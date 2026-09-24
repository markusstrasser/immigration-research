"""Sum the audit's effects on the main case ($203.2-249.6bn) into one net range per band end.

Effects are $bn a year of cost to other residents; negative means the published main case is too
high. The band's low end ($203.2bn) uses the shared allocation and its high end ($249.6bn) the
personal one, so every figure is computed at both ends.

The tax block (rows 2, 3, 13, 4 and the state-aware status flag) is read from the CPS imputation
lane's stacks, never summed row by row: each of those rows is measured on top of the others
(`cps_imputation_keys_2026_09_23` RESULT step 5e). For on-books case c (low, central, high share)
and fill-in method m, block = the row 4 + state-aware stack (row 2 and m under the ACS-reweighted
weights) + row 3's increment over row 2 and m at published weights. Its central is the mean of
the two methods at the central case; its low and high are the extremes over the six scenarios.
The other rows are independent bounds, (low, central, high) with `low` the most negative.
Rows 11 and 12 are classification and key choices, reported beside the net, not in it.
Run: uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/synthesis.py
"""
import csv
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
CPS = HERE.parent / "cps_imputation_keys_2026_09_23" / "derived" / "status_combination_onbooks_lane.csv"
MAIN_CASE = {"shared": 203.2, "personal": 249.6}
METHODS = {"b_hotdeck_union_matched": "hot deck (b)", "b_matched_over_pooled": "hot deck net of control (b)-net"}
CASES = ("low", "central", "high")
mts = json.loads((HERE / "derived" / "spending_mts_credits.json").read_text())
ptc = mts["ptc_effect_on_main_case_bn"]

# Row 9: the donor filter's Medicaid part applies only to the community remainder once row 5 carves
# long-term care out ($689.5bn of $954.2bn). The records carry 3.0% of Medicare and 3.7% of
# Medicaid dollars; scaling the whole bound by 0.8 treats roughly 70% of it as Medicaid.
ROW9_SCALE = 0.8
ROWS = [
    # id, label, low, central, high, grade/status, source
    ("1", "premium tax credits keyed as EITC+ACTC", ptc, ptc, ptc, "A measured", "spending.md #1; spending_mts_credits.py"),
    ("5", "Medicaid long-term care keyed by the MEPS community key", -12.5, -11.1, -8.1, "B measured",
     "ltss_share_2026_09_23 RESULT (T-MSIS/TAF, CMS-64 IHSS)"),
    ("6", "education key 93% K-12", -4.8, -3.5, -2.2, "B measured", "spending.md #5"),
    ("7", "justice key on FBI 2019 arrests", 1.12, 1.12, 1.12, "B measured", "crime.md #1 (2024 Table 43C)"),
    ("8", "unallocable S&L spending given the administration elasticity", 2.0, 2.0, 2.0, "C measured", "spending.md #7"),
    ("9", "MEPS donor filter (non-LTSS remainder)", -2.0 * ROW9_SCALE, -1.0 * ROW9_SCALE, 0.0, "C bound",
     "spending.md #4, scaled for row 5"),
    ("10", "foster care keyed by WIC", -2.0, -1.5, -1.0, "C bound", "spending.md #9"),
    ("small", "origin allocation, grants, top-codes, flags", -0.5, -0.1, 0.4, "D", "cps.md rows 4-6, 12; spending.md #8, #11"),
]
# Decision 2 (medical ethnicity, before the operator): the joint LTSS + pooled-MEPS figure replaces
# row 5. -17.7 at that lane's p99.5 headline; -8.7 to -21.1 across its seven specifications.
ROW5_JOINT = (-21.1, -17.7, -8.7)
BESIDE = [
    ("11", "household rental assistance held fixed", 0.0, 7.5, "spending.md #6: 0 now, +7.5 if it responded fully"),
    ("12", "income-security consumption keyed by public assistance", -20.0, -7.5, "spending.md #12: -7.5 population key, -20 all-cash key"),
]


def read_block():
    with CPS.open(newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["share_type"] == "origin"]

    def get(arm, case, alloc, method):
        hit = [r for r in rows if (r["arm"], r["case"], r["allocation"], r["method"]) == (arm, case, alloc, method)]
        if len(hit) != 1:
            raise SystemExit(f"[BLOCKED] {CPS.name}: {len(hit)} rows for {arm}/{case}/{alloc}/{method}")
        return float(hit[0]["change_bn"])

    out = {}
    for alloc in MAIN_CASE:
        for case in CASES:
            for m in METHODS:
                base = get("row4+status_state_aware", case, alloc, m)
                row3 = get("row3", case, alloc, m) - get("medicare_key_fix", case, alloc, m)
                out[alloc, case, m] = dict(base=base, row3=row3, block=base + row3)
            # Sensitivity: no fill-in correction (row 13 = 0), the audit's rules alone in the stack.
            a = "audit_rules_alone"
            base = get("row4+status_state_aware", case, alloc, a)
            row3 = get("row3", case, alloc, a) - get("medicare_key_fix", case, alloc, a)
            out[alloc, case, a] = dict(base=base, row3=row3, block=base + row3)
    return out


def main():
    block = read_block()
    o_low, o_cen, o_high = (sum(r[i] for r in ROWS) for i in (2, 3, 4))
    j_shift = [ROW5_JOINT[i] - ROWS[1][2 + i] for i in range(3)]
    out = HERE / "derived" / "synthesis_net.csv"
    summary = {}
    with out.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["band_end", "row", "item", "low_bn", "central_bn", "high_bn", "status", "source"])
        for alloc, mc in MAIN_CASE.items():
            vals = {k[1:]: v["block"] for k, v in block.items() if k[0] == alloc and k[2] in METHODS}
            nof = [block[alloc, c, "audit_rules_alone"]["block"] for c in CASES]
            b_cen = sum(vals["central", m] for m in METHODS) / len(METHODS)
            b_low, b_high = min(vals.values()), max(vals.values())
            for (case, m), v in sorted(vals.items()):
                d = block[alloc, case, m]
                w.writerow([alloc, f"block:{case}:{m}", "rows 2+3+13+4+status stack", "", f"{v:.2f}", "",
                            "stack", f"row4+status {d['base']:.2f} + row3 {d['row3']:.2f}"])
            w.writerow([alloc, "tax block", "rows 2, 3, 13, 4 and the status flag, stacked", f"{b_low:.2f}",
                        f"{b_cen:.2f}", f"{b_high:.2f}", "B stacked", CPS.relative_to(HERE.parent).as_posix()])
            for r in ROWS:
                w.writerow([alloc, r[0], r[1], f"{r[2]:.2f}", f"{r[3]:.2f}", f"{r[4]:.2f}", r[5], r[6]])
            n = (b_low + o_low, b_cen + o_cen, b_high + o_high)
            nj = tuple(n[i] + j_shift[i] for i in range(3))
            w.writerow([alloc, "net", "tax block + rows 1, 5-10, small", *(f"{x:.2f}" for x in n), "", ""])
            nn = (min(nof) + o_low, nof[1] + o_cen, max(nof) + o_high)
            w.writerow([alloc, "net, no fill-in correction", "row 13 = 0: rules alone in the stack",
                        *(f"{x:.2f}" for x in nn), "sensitivity", "RESULT step 6"])
            w.writerow([alloc, "net, decision 2", "row 5 replaced by the joint LTSS + medical figure",
                        *(f"{x:.2f}" for x in nj), "", "ltss_share_2026_09_23 RESULT, combining rule"])
            summary[alloc] = dict(main=mc, block=(b_low, b_cen, b_high), net=n, net_j=nj, net_nf=nn)
        for b in BESIDE:
            w.writerow(["both", b[0], b[1], f"{b[2]:.2f}", "", f"{b[3]:.2f}", "choice", b[4]])
    s, p = summary["shared"], summary["personal"]
    print(f"tax block  shared {s['block'][0]:.1f} / {s['block'][1]:.1f} / {s['block'][2]:.1f}"
          f"   personal {p['block'][0]:.1f} / {p['block'][1]:.1f} / {p['block'][2]:.1f}")
    print(f"other rows {o_low:.1f} / {o_cen:.1f} / {o_high:.1f}")
    print(f"net        shared {s['net'][0]:.1f} / {s['net'][1]:.1f} / {s['net'][2]:.1f}"
          f"   personal {p['net'][0]:.1f} / {p['net'][1]:.1f} / {p['net'][2]:.1f}")
    print(f"main case at central net: {s['main'] + s['net'][1]:.1f}-{p['main'] + p['net'][1]:.1f}"
          f" (range {s['main'] + s['net'][0]:.1f}-{p['main'] + p['net'][2]:.1f})")
    print(f"with decision 2: {s['main'] + s['net_j'][1]:.1f}-{p['main'] + p['net_j'][1]:.1f}"
          f" (range {s['main'] + s['net_j'][0]:.1f}-{p['main'] + p['net_j'][2]:.1f})")
    print(f"no fill-in correction (row 13 = 0): {s['main'] + s['net_nf'][1]:.1f}-{p['main'] + p['net_nf'][1]:.1f}"
          f" (range {s['main'] + s['net_nf'][0]:.1f}-{p['main'] + p['net_nf'][2]:.1f})")
    print(f"with choices 11-12 beside: {s['main'] + s['net'][0] + BESIDE[1][2]:.1f}"
          f" to {p['main'] + p['net'][2] + BESIDE[0][3]:.1f}")


if __name__ == "__main__":
    main()
