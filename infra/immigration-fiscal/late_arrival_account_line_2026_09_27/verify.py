"""Re-derive the Mexico-born total from the late-arrival subgroup plus its complement and match it to the
generation lane's Mexico-born (G1) line for the same case, both conventions, both band ends (1e-6 bn).

Sources: this lane's _cache/cells_<case>_<reading>.json (full precision; every reading, since the readings
only move persons between G1 cells) and derived/late_arrival_line.csv (six decimals, checked to 1e-5); the
generation lane's derived/generation_summary.json (read-only), which holds one case, named in its `case`.
A case the generation lane has not run is reported [PENDING] and checked only against the case's published
band (main_case_bands.csv, row `adopted`, the nine cells summed). Exit 1 on any failure.
--set sept29 checks the v4 cases instead (sept29, the main case adopted on 2026-09-29, and sept29_cash, its cash
set): the generation lane's generation_summary_<case>.json, the published band of the adopted case's lane (V4_LANE),
and derived/late_arrival_line_sept29.csv.
--set oct05 checks the v5 cases (oct05, main case v5 adopted on 2026-10-05, and oct05_cash) the same way: the generation
lane's generation_summary_<case>.json (run_generations_v5.cjs), the published band of the v5 lane (V5_LANE) and
derived/late_arrival_line_oct05.csv. The G3plus cell also holds the case's added people, so it is checked against the
generation lane's G3plus (cost, members and adults) too.
Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/late_arrival_account_line_2026_09_27/verify.py [--set sept29|oct05]
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
GEN = FISCAL / "generation_account_2026_09_24/derived/generation_summary.json"
MAIN = {"sept27": "main_case_long_run_2026_09_27", "sept26_schools": "main_case_schools_full_2026_09_26"}
# The v4 cases: the adopted case's lane (repoint with generation_account_2026_09_24/v4_split.cjs V4_LANE) and each
# case's generation summary (run_generations_v4.cjs).
V4_LANE = "main_case_2026_09_29"
V4_GEN = {c: FISCAL / f"generation_account_2026_09_24/derived/generation_summary_{c}.json" for c in ("sept29", "sept29_cash")}
# The v5 cases: the v5 lane and each case's generation summary (run_generations_v5.cjs).
V5_LANE = "main_case_2026_10_05"
V5_GEN = {c: FISCAL / f"generation_account_2026_09_24/derived/generation_summary_{c}.json" for c in ("oct05", "oct05_cash")}
LATE = ["G1_L50_50_64", "G1_L50_65p", "G1_L55_55_64", "G1_L55_65p"]
REST = ["G1_Y_u50", "G1_Y_50_64", "G1_Y_65p"]
fails = []


def check(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}")
    if not ok:
        fails.append(label)


def v4_band(case):
    """A v4 case's published band as a main_case_bands.csv row: the candidate's bands.csv (set or cash, the methods'
    mean) or the adopted lane's main_case_bands.csv (adopted or cash_set)."""
    lane = FISCAL / V4_LANE / "derived"
    if V4_LANE == "main_case_candidate_v4_2026_09_29":
        r = next(r for r in csv.DictReader((lane / "bands.csv").open())
                 if r["case"] == {"sept29": "set", "sept29_cash": "cash"}[case] and r["method"] == "mean")
        return {"cost_low_bn": r["own_low_bn"], "cost_high_bn": r["own_high_bn"]}
    return next(r for r in csv.DictReader((lane / "main_case_bands.csv").open())
                if r["profile"] == "long_run_non_school_full" and r["variant"] == {"sept29": "adopted", "sept29_cash": "cash_set"}[case])


def v5_band(case):
    """A v5 case's published band: the v5 lane's main_case_bands.csv row (adopted or cash_set)."""
    return next(r for r in csv.DictReader((FISCAL / V5_LANE / "derived/main_case_bands.csv").open())
                if r["profile"] == "long_run_non_school_full" and r["variant"] == {"oct05": "adopted", "oct05_cash": "cash_set"}[case])


def main():
    which = sys.argv[sys.argv.index("--set") + 1] if "--set" in sys.argv else "default"
    if which not in ("default", "sept29", "oct05"):
        sys.exit("--set must be default, sept29 or oct05")
    v4, v5 = which == "sept29", which == "oct05"
    sets = V5_GEN if v5 else V4_GEN
    gens = {c: json.loads(sets[c].read_text()) for c in sets} if v4 or v5 else None
    gen = None if v4 or v5 else json.loads(GEN.read_text())
    line = list(csv.DictReader((HERE / f"derived/late_arrival_line{'_' + which if v4 or v5 else ''}.csv").open()))
    for case in (sets if v4 or v5 else MAIN):
        if v4 or v5:
            gen, band = gens[case], (v5_band(case) if v5 else v4_band(case))
        else:
            band = next(r for r in csv.DictReader((FISCAL / MAIN[case] / "derived/main_case_bands.csv").open())
                        if r["variant"] == "adopted" and r["profile"] in ("long_run_non_school_full", "cbo_category_lag_non_school_full"))
        for reading in ("central", "lower", "upper"):
            c = json.loads((HERE / "_cache" / f"cells_{case}_{reading}.json").read_text())
            if v4:
                check(f"{case} {reading}: the cells and the generation summary are one lane's payload ({V4_LANE})",
                      c["main"] == gen["lane"] == V4_LANE and c["v4"]["payload"] == gen["payload"], c["v4"]["payload"])
            if v5:
                check(f"{case} {reading}: the cells and the generation summary are one lane's payload ({V5_LANE})",
                      c["main"] == gen["lane"] == V5_LANE and c["v5"]["payload"] == gen["payload"], c["v5"]["payload"])
            for conv in ("a", "b"):
                cells = c["conventions"][conv]
                for k, end in enumerate(("low", "high")):
                    late = sum(cells[g][end]["cost_bn"] for g in LATE)
                    rest = sum(cells[g][end]["cost_bn"] for g in REST)
                    union = sum(v[end]["cost_bn"] for g, v in cells.items() if g != "union")
                    tag = f"{case} {reading} ({conv}) {end}"
                    check(f"{tag}: the cells add to the case's band ({float(band['cost_low_bn' if k == 0 else 'cost_high_bn']):.4f})",
                          abs(union - float(band["cost_low_bn" if k == 0 else "cost_high_bn"])) < 5.01e-5, f"{union:.6f}")
                    if gen.get("case") == case:
                        ref = gen["conventions"][conv]["G1"]["cost_bn"][k]
                        same_spec = json.dumps(gen["low_spec" if k == 0 else "high_spec"], sort_keys=True) == \
                            json.dumps(c["low_spec" if k == 0 else "high_spec"], sort_keys=True)
                        check(f"{tag}: late + younger = the generation lane's G1 {ref:.6f}", same_spec and abs(late + rest - ref) < 1e-6,
                              f"late {late:.6f} + younger {rest:.6f}; |diff| {abs(late + rest - ref):.1e}")
                    elif reading == "central" and conv == "a" and end == "low":
                        print(f"  [PENDING] {case}: the generation lane holds case {gen.get('case')}, not {case}; "
                              "G1 checked against the case's band only")
                    if v5:
                        g3, ref3 = cells["G3plus"], gen["conventions"][conv]["G3plus"]
                        check(f"{tag}: the G3plus cell, with the added people, is the generation lane's G3plus (cost 1e-6; members and adults 1e-6)",
                              abs(g3[end]["cost_bn"] - ref3["cost_bn"][k]) < 1e-6 and abs(g3["population"] - ref3["population"]) < 1e-6
                              and abs(g3["adults"] - ref3["adults"]) < 1e-6,
                              f"{g3[end]['cost_bn']:.6f}; {g3['population']:,.1f} members")
                    rows = {r["subgroup"]: float(r["bn"]) for r in line if r["case"] == case and r["reading"] == reading
                            and r["convention"] == conv and r["spec"] == end and r["program"] == "total"}
                    check(f"{tag}: late_arrival_line{'_' + which if v4 or v5 else ''}.csv late50 + younger = mexico_born (1e-5)",
                          abs(rows["late50"] + rows["younger_50p"] + rows["younger_u50"] - rows["mexico_born"]) < 1e-5
                          and abs(rows["mexico_born"] - late - rest) < 1e-5)
    if fails:
        print(f"✗ {len(fails)} check(s) failed")
        sys.exit(1)
    print("  ✓ all checks passed")


if __name__ == "__main__":
    main()
