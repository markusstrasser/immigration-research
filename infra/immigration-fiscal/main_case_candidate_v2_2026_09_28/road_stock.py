"""The road arm's upward case (BRIEF.md, 08b1b7d): the road stock's response read from highway construction.

The attack on the first candidate (candidate_attack_2026_09_28, f0e262e, section 3) refits the scaling test's state model
on nontoll highway construction (Census code F44), the capital outlay that builds and replaces the stock. Across states
it scales with population at 0.792 (95% CI 0.675-0.908), and at 0.758 with a land control. That excludes a fixed stock
(response 0) and gives the stock an upward case: a stock that responds like construction, not like operations.

This script runs that probe unchanged (runpy; the probe is read-only, writes nothing and sets sys.dont_write_bytecode;
its printout is captured, not shown) and keeps its exact slopes. Each is read over the removal as the case reads every
slope, r = [1 - (1 - s)^b] / s at the account's s. Gates: the probe's operations slope is the one the case uses
(service_response_long_run_2026_09_27/derived/responses.json), its s is the case's, its r of that slope is the case's
S&L highway response at the low end, and its construction rows are the attack's printed ones.
Writes derived/road_stock.json; exit 1 and nothing written on a failed gate.
Run from the repository root (scipy for the probe's t critical values):
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with scipy python3 infra/immigration-fiscal/main_case_candidate_v2_2026_09_28/road_stock.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import contextlib
import hashlib
import io
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
PROBE = "candidate_attack_2026_09_28/probe_road_stock.py"
RESPONSES = "service_response_long_run_2026_09_27/derived/responses.json"
SOURCES = [PROBE, RESPONSES, "scaling_test_2026_09_20/derived/state/panel.csv",
           "tiebout_sorting_2026_09_18/_cache/state_covariates.csv",
           "service_response_long_run_2026_09_27/_cache/2020_Gaz_counties_national.zip"] + [
    f"local_spending_composition_2026_09_18/_cache/indunit_{y}.zip" for y in (2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023)]
# The attack's printed rows (RESULT.md section 3): b, SE, the 95% CI and r(b), to the digits it prints.
PRINTED = {"year_effects": (0.792, 0.058, 0.675, 0.908, 0.8022), "land": (0.758, 0.046, 0.666, 0.850, 0.7699),
           "land_growth": (0.758, 0.046, 0.665, 0.851, 0.7700), "state_year": (0.575, 0.781, -0.995, 2.144, 0.5905)}
MODELS = {"year_effects": ((), "year", "year effects"), "land": (("log_land",), "year", "+ log land"),
          "land_growth": (("log_land", "growth"), "year", "+ log land + growth 2012-23"),
          "state_year": ((), "state_year", "state and year effects")}
GATES: list[dict] = []


def gate(name, ok, detail=""):
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' — ' + detail if detail else ''}")


def sha256(rel):
    return hashlib.sha256((FISCAL / rel).read_bytes()).hexdigest()


def main():
    before = {rel: sha256(rel) for rel in SOURCES}
    with contextlib.redirect_stdout(io.StringIO()):
        g = runpy.run_path(str(FISCAL / PROBE), run_name="candidate_attack_probe_road_stock")
    fit, d, r_of, s = g["fit"], g["d"], g["r_of"], g["S"]
    lr = json.loads((FISCAL / RESPONSES).read_text())
    sl = next(x for x in lr["lines"]["economic_affairs_services"]["subfunctions"] if x["id"] == "sl_highways")
    b_case = lr["elasticities"]["highways_nontoll"]["across_states"]["b"]

    print("[gates: the probe is the case's model]")
    b_ops, se_ops, crit, n, groups = fit(d, "E44")
    gate("the probe's operations slope (E44, year effects) is the case's highways_nontoll across-state b (1e-12)",
         abs(b_ops - b_case) < 1e-12, f"{b_ops:.12f}")
    gate("the probe's s is the case's removal share", s == lr["meta"]["s"], f"{s}")
    gate("r of the operations slope is the case's S&L highway response at the low end (1e-12)",
         abs(r_of(b_ops) - sl["response"]["low"]) < 1e-12, f"{r_of(b_ops):.12f}")
    gate("the panel is the attack's: 350 rows, 50 states", len(d) == 350 and d.state.nunique() == 50 and n == 350 and groups == 50)

    print("\n[construction (F44)]")
    rows = {}
    for key, (extra, fe, label) in MODELS.items():
        b, se, crit, n, groups = fit(d, "F44", extra, fe)
        rows[key] = {"model": label, "b": b, "se": se, "ci95": [b - crit * se, b + crit * se], "r": r_of(b), "n": n, "states": groups}
        pb, pse, plo, phi, pr = PRINTED[key]
        ok = (round(b, 3) == pb and round(se, 3) == pse and round(b - crit * se, 3) == plo and round(b + crit * se, 3) == phi
              and round(r_of(b), 4) == pr)
        gate(f"construction, {label}: the attack's printed row", ok,
             f"b {b:.6f} SE {se:.6f} CI [{b - crit * se:.4f}, {b + crit * se:.4f}] r {r_of(b):.6f}")
    gate("a fixed stock (response 0) lies outside every across-state interval",
         all(rows[k]["ci95"][0] > 0 for k in ("year_effects", "land", "land_growth")),
         ", ".join(f"{k} {rows[k]['ci95'][0]:.3f}" for k in ("year_effects", "land", "land_growth")))
    gate("construction scales above operations across states (the stock's upward case)",
         rows["year_effects"]["r"] > sl["response"]["low"] and rows["land"]["r"] > sl["response"]["low"],
         f"r {rows['year_effects']['r']:.4f} and {rows['land']['r']:.4f} against {sl['response']['low']:.4f}")
    gate("the sources did not change during the run", before == {rel: sha256(rel) for rel in SOURCES})

    if not all(x["passed"] for x in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not x['passed'] for x in GATES)} gate(s) failed; nothing written")
    DERIVED.mkdir(exist_ok=True)
    (DERIVED / "road_stock.json").write_text(json.dumps({
        "meta": {"lane": "main_case_candidate_v2_2026_09_28", "case": "sept28_candidate_v2",
                 "definition": ("state-local nontoll highway construction (Census F44) regressed on log population across states with "
                                "year effects (the scaling test's model; state-clustered SEs, t critical values with G - 1 df), refitted by "
                                "the attack's probe; r = [1 - (1 - s)^b] / s"),
                 "probe": PROBE, "sources": before},
        "s": s, "operations_across_states": {"b": b_ops, "se": se_ops, "r": r_of(b_ops)},
        "construction": rows,
        "stock_responses_low_end": {"construction_year_effects": rows["year_effects"]["r"], "construction_land": rows["land"]["r"]},
        "gates": GATES}, indent=1) + "\n")
    print(f"\nall {len(GATES)} gates passed; wrote derived/road_stock.json")


if __name__ == "__main__":
    main()
