#!/usr/bin/env python3
"""The people the v5 lineage line adds to the account, on the account's frame, and the closing share C3.

Added persons are the descendants of Mexican immigrants whom the CPS misses because they no longer report Mexican
origin: the identity-loss correction of the self-identified third-plus count (identity_loss_propagation_2026_09_27
derived/population_arms.csv, its RESULT sections 1-2 and 5; the floor row from mexican_origin_population_total_2026_09_19
derived/arm3_correction_bounds.csv). The split into the two pricing classes is that lane's, the measured generation
split of bounds_coverage_fiscal.py arm 5: 1 - p3 of the corrected third-plus is lost at the third-generation rate at
every generation (G3 attriters and the G4+ descendants of attriters), and the rest of the added persons are later
losses (a child of identified parents who does not identify). The brief's first reading (only the floor's 0.80M at the
G3 rate) misread that rule (team-lead, 2026-10-05) and is not priced.

Frame. The population lane sums published CPS ASEC 2025 weights over all person records. Audit row 4 rescales only
the Mexico-born outside California and Texas; the third-plus keeps its CPS weights. The account's third-plus is the
civilian household universe (generation_account_2026_09_24 frame.py: PRPERTYP 2 or age under 15), so the factor that
moves the lane's added persons to the account's frame is the account's G3+ over the lane's self-identified
third-plus, 14,342,575 / 14,383,006.5 (the armed forces), applied on the assumption that hidden persons are civilian
in the same proportion. The union ratio 39,712,493 / 40,968,044.7 would also strip the row-4 reweight of the
Mexico-born from people born in the US; it is printed beside, not used.

C3 is imported, never copied: generation_carryover_2026_09_27/summarize.py SPLIT_C3, the entry whose label contains
"(central)" (exactly one, or the script stops), measure ba_plus, loaded with importlib as
mexican_origin_population_total_2026_09_19/bounds_coverage_fiscal.py loads it. Every SPLIT_C3 entry is written so the
engine step can price each; an entry without a (C3, SE) pair stops the script. For test runs while that file is being
rerun, `--c3-override C3,SE` replaces the central's value only (team-lead, 2026-10-05); the run is marked a test in
population.json (c3.override) and in every later output.

Group-size inputs for the finite-removal responses: s, the group's share of residents as the finite-response lane
defines it (40.896574m / 340.110988m, finite_response_2026_09_26/derived/r_values.json s_national_memo), rises by the
added persons (US-born, so the same CPS weights on either frame); the metro group shares of the property-price fall
scale by 1 + added / the ACS proxy group (receipt_side_long_run_2026_09_28/derived/housing.json), which assumes the
added persons live where the group lives [ASSUMPTION].

Fractional ancestry (sensitivity): arm3_grandparent_counts.csv gives third-generation children by the number of
Mexico-born grandparents and the self-identified among them, so the hidden (children - self-identified) carry a
measured quarter-per-grandparent weight. Later losses (G4+) have no grandparent detail; they take the same weight,
an upper bound because each generation of intermarriage halves the fraction [ASSUMPTION].

Inputs : ../identity_loss_propagation_2026_09_27/derived/population_arms.csv
         ../mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv, arm3_grandparent_counts.csv
         ../generation_account_2026_09_24/derived/generation_results_sept29.csv (G3plus, convention a, population)
         ../generation_carryover_2026_09_27/summarize.py SPLIT_C3 (imported, read-only)
         ../finite_response_2026_09_26/derived/r_values.json, ../receipt_side_long_run_2026_09_28/derived/housing.json
Outputs: derived/population.json, derived/population_arms_account.csv, derived/gates_population.json
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/population.py
"""
from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
ARMS = FISCAL / "identity_loss_propagation_2026_09_27/derived/population_arms.csv"
BOUNDS = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_correction_bounds.csv"
GRANDPARENTS = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_grandparent_counts.csv"
GEN = FISCAL / "generation_account_2026_09_24/derived/generation_results_sept29.csv"
R_VALUES = FISCAL / "finite_response_2026_09_26/derived/r_values.json"
HOUSING = FISCAL / "receipt_side_long_run_2026_09_28/derived/housing.json"
SUMMARIZE = FISCAL / "generation_carryover_2026_09_27/summarize.py"
ACCOUNT_UNION = 39_712_493.3312     # audit row 4 (ladder 274), the account's count
POP_LANE_UNION = 40_968_044.7       # the population lane's union (arm1_counts_cps.csv), for the printed beside-ratio
# Arms the brief names (a, b central, c at rho 0.5) and the floor beside them; the rest of population_arms.csv is
# carried in the CSV only.
PRICED = {"floor": ("floor", None), "a": ("a_current", 0.5), "b": ("b_one_step", 0.5), "c": ("c_compound", 0.5)}
CENTRAL_ARM = "b"

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def load_c3(override: tuple[float, float] | None) -> tuple[str, float, float, dict]:
    spec = importlib.util.spec_from_file_location("generation_carryover_summarize", SUMMARIZE)
    gc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gc)
    central = [k for k in gc.SPLIT_C3 if "(central)" in k]
    if len(central) != 1:
        raise SystemExit(f"[BLOCKED] SPLIT_C3 must have exactly one entry labelled '(central)'; found {central!r}")
    label = central[0]
    # An entry awaiting its measurement holds None (summarize.py sets it after the upstream rerun): stop, never fall
    # back to another entry or an older value. An explicit test override stands in for the central only.
    pair = lambda v: isinstance(v.get("ba_plus"), tuple) and len(v["ba_plus"]) == 2 and all(  # noqa: E731
        isinstance(x, (int, float)) for x in v["ba_plus"])
    unset = [k for k, v in gc.SPLIT_C3.items() if not pair(v) and not (override and k == label)]
    if unset:
        raise SystemExit(f"[BLOCKED] SPLIT_C3 ba_plus is not a (C3, SE) pair for {unset!r} (central: {label!r}); "
                         "rerun once summarize.py sets it")
    every = {k: {"c3": float(v["ba_plus"][0]), "se": float(v["ba_plus"][1])} for k, v in gc.SPLIT_C3.items() if k != label or not override}
    if override:
        print(f"[OVERRIDE] C3 {override[0]} (SE {override[1]}) replaces {label!r}'s value for this test run only", flush=True)
        every[label] = {"c3": override[0], "se": override[1]}
        return label, override[0], override[1], every
    c3, se = gc.SPLIT_C3[label]["ba_plus"]
    return label, float(c3), float(se), every


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--c3-override", metavar="C3,SE", help="test runs only: replace SPLIT_C3's central value")
    args = ap.parse_args()
    override = tuple(float(x) for x in args.c3_override.split(",")) if args.c3_override else None
    if override is not None and len(override) != 2:
        raise SystemExit("[BLOCKED] --c3-override takes C3,SE")
    print("[inputs]", flush=True)
    arms = rows(ARMS)
    bounds = rows(BOUNDS)
    gen = [r for r in rows(GEN) if r["convention"] == "a" and r["generation"] == "G3plus"]
    gate("generation_results_sept29.csv has one G3plus (a) population at both ends",
         len(gen) == 2 and gen[0]["population"] == gen[1]["population"], f"{gen[0]['population']}")
    g3_account = float(gen[0]["population"])
    self_id = {float(r["self_id_third_plus"]) for r in bounds}
    gate("arm3_correction_bounds.csv carries one self-identified third-plus count", len(self_id) == 1, f"{self_id}")
    self_id = self_id.pop()
    frame = g3_account / self_id
    gate("the frame factor is the armed-forces share only (0.99 < f < 1)", 0.99 < frame < 1.0, f"{frame:.6f}")
    floor = next(r for r in bounds if r["assumption"].startswith("floor"))
    floor_added = float(floor["added"])
    p3 = float(floor["third_gen_identification_rate"])
    a_row = next(r for r in arms if r["arm"] == "a_current")
    p3_full = float(a_row["p_eff_fourth_plus"])
    gate("the floor's p3 is the arms' G3 rate rounded (4 decimals)", abs(round(p3_full, 4) - p3) < 1e-12,
         f"{p3_full:.10f} vs {p3}")

    # The split, re-derived from each arm's corrected third-plus and checked against the file.
    worst = 0.0
    for r in arms:
        added, corrected = float(r["added_M"]), float(r["corrected_third_plus_M"])
        g3 = min(added, (1.0 - p3_full) * corrected)
        worst = max(worst, abs(g3 - float(r["g3_rate_attriters_M"])), abs(added - g3 - float(r["later_loss_attriters_M"])))
        worst = max(worst, abs(corrected - added - self_id / 1e6))
    gate("population_arms.csv: G3-rate = min(added, (1 - p3) x corrected third-plus), later = the rest, and corrected - "
         "added = the self-identified third-plus (1e-6 M)", worst < 1e-6, f"max |diff| {worst:.2e} M")
    gate("the floor row's added persons are all at the G3 rate: (1 - p3) x its corrected third-plus covers them",
         (1.0 - p3_full) * float(floor["corrected_third_plus"]) >= floor_added - 1.0, f"{floor_added:,.1f}")

    print("[C3]", flush=True)
    label, c3, c3_se, every = load_c3(override)
    gate("C3 central is imported from summarize.py SPLIT_C3 (one '(central)' entry, ba_plus, 0 <= C3 <= 1.5)",
         0.0 <= c3 <= 1.5, f"{label}: {c3} (SE {c3_se})")

    rv = json.loads(R_VALUES.read_text())
    s_v4 = rv["s_national_memo"]
    target_memo, resident_memo = 40.896574e6, 340.110988e6
    gate("s is the finite-response lane's 40.896574m / 340.110988m", abs(s_v4 - target_memo / resident_memo) < 1e-15, f"{s_v4!r}")
    housing = json.loads(HOUSING.read_text())
    proxy = float(housing["amounts"]["group_pop"])
    gate("the property lane's ACS proxy group is 36-42 million", 36e6 < proxy < 42e6, f"{proxy:,.0f}")

    # Grandparent cells: the hidden third generation's quarter-per-grandparent weight.
    gp = rows(GRANDPARENTS)
    hid = [(float(r["fractional_weight"]), float(r["children"]) - float(r["self_id_mexican"])) for r in gp]
    ids = [(float(r["fractional_weight"]), float(r["self_id_mexican"])) for r in gp]
    gate("grandparent cells: four cells, hidden children positive in each", len(hid) == 4 and all(h > 0 for _, h in hid))
    frac_hidden = sum(w * h for w, h in hid) / sum(h for _, h in hid)
    frac_ident = sum(w * h for w, h in ids) / sum(h for _, h in ids)
    frac_all = sum(float(r["fractional_children"]) for r in gp) / sum(float(r["children"]) for r in gp)
    gate("grandparent cells reproduce arm3_fractional_counting.csv's 0.5916 for all third-generation children",
         abs(frac_all - 0.5916) < 5e-5, f"{frac_all:.6f}")

    def account(m):  # population-lane millions -> account persons
        return m * 1e6 * frame

    out_rows, priced = [], {}
    for r in arms:
        added, g3, later = float(r["added_M"]), float(r["g3_rate_attriters_M"]), float(r["later_loss_attriters_M"])
        out_rows.append({"arm": r["arm"], "rho": r["rho"], "p_eff_fourth_plus": r["p_eff_fourth_plus"],
                         "added_cps": f"{added * 1e6:.1f}", "added_account": f"{account(added):.1f}",
                         "g3_rate_account": f"{account(g3):.1f}", "later_loss_account": f"{account(later):.1f}",
                         "lineage_population_account": f"{ACCOUNT_UNION + account(added):.1f}"})
    out_rows.insert(0, {"arm": "floor", "rho": "", "p_eff_fourth_plus": "1.0", "added_cps": f"{floor_added:.1f}",
                        "added_account": f"{floor_added * frame:.1f}", "g3_rate_account": f"{floor_added * frame:.1f}",
                        "later_loss_account": "0.0", "lineage_population_account": f"{ACCOUNT_UNION + floor_added * frame:.1f}"})
    for key, (arm, rho) in PRICED.items():
        if key == "floor":
            added_cps, g3_cps = floor_added, floor_added
        else:
            r = next(x for x in arms if x["arm"] == arm and abs(float(x["rho"]) - rho) < 1e-12)
            added_cps, g3_cps = float(r["added_M"]) * 1e6, float(r["g3_rate_attriters_M"]) * 1e6
        added, g3 = added_cps * frame, g3_cps * frame
        later = added - g3
        priced[key] = {
            "source_arm": arm, "rho": rho, "added_cps": added_cps, "added": added, "g3_rate": g3, "later": later,
            "population": ACCOUNT_UNION + added,
            "s": (target_memo + added) / resident_memo,
            "k_metro": 1.0 + added / proxy,
        }
    gate("arm b is the brief's central: about 3.0M added on the population lane's frame, 44.02M lineage",
         abs(priced["b"]["added_cps"] / 1e6 - 3.048) < 0.01
         and abs(float(next(x for x in arms if x["arm"] == "b_one_step")["union_M"]) - 44.0163) < 1e-3,
         f"{priced['b']['added_cps'] / 1e6:.4f}M; account frame {priced['b']['added'] / 1e6:.4f}M")

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    OUT.mkdir(exist_ok=True)
    result = {
        "meta": {
            "source": "main_case_lineage_2026_10_05/population.py",
            "account_union": ACCOUNT_UNION,
            "frame_factor": frame,
            "frame_rule": "the account's civilian G3+ (generation_results_sept29.csv, convention a) over the population lane's "
                          "self-identified third-plus (all person records): row 4 leaves US-born weights alone",
            "union_ratio_not_used": ACCOUNT_UNION / POP_LANE_UNION,
            "g3_account": g3_account, "self_id_third_plus_cps": self_id,
            "p3": p3_full,
            "split_rule": "bounds_coverage_fiscal.py arm 5 (identity_loss_propagation population_arms.csv): G3-rate = "
                          "min(added, (1 - p3) x corrected third-plus), later losses = the rest",
            "s_v4": s_v4, "s_rule": "(40.896574m + added) / 340.110988m, finite_response_2026_09_26 s_national_memo",
            "acs_proxy_group": proxy,
            "central_arm": CENTRAL_ARM,
        },
        "c3": {"label": label, "measure": "ba_plus", "value": c3, "se": c3_se, "every_entry": every,
               "override": override is not None,
               "source": "--c3-override (test run; not the imported value)" if override
               else "generation_carryover_2026_09_27/summarize.py SPLIT_C3 (imported)"},
        "fractional_ancestry": {"hidden_third_generation": frac_hidden, "identified_third_generation": frac_ident,
                                "all_third_generation": frac_all,
                                "rule": "a quarter per Mexico-born grandparent; hidden = children - self-identified per cell "
                                        "(arm3_grandparent_counts.csv); later losses take the same weight, an upper bound"},
        "arms": priced,
    }
    (OUT / "population.json").write_text(json.dumps(result, indent=1) + "\n")
    with (OUT / "population_arms_account.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out_rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(out_rows)
    (OUT / "gates_population.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    print("[arms on the account's frame]")
    for k, a in priced.items():
        print(f"  {k}: added {a['added'] / 1e6:.4f}M (G3 rate {a['g3_rate'] / 1e6:.4f}M, later {a['later'] / 1e6:.4f}M); "
              f"lineage {a['population'] / 1e6:.4f}M; s {a['s']:.6f}; metro x{a['k_metro']:.6f}")
    print(f"  frame factor {frame:.6f}; C3 {c3} ({label}); fractional weight of the hidden {frac_hidden:.4f}")


if __name__ == "__main__":
    main()
