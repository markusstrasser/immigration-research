#!/usr/bin/env python3
"""Third-plus non-Hispanic whites (W) per person and per line under the v4 case's rules: the white end of the C3 blend.

W is the white_replacement_2026_09_28 sept29 run's third-plus slice (native, both parents US-born, non-Hispanic white
alone), its rough re-key on the adopted v4 case: the case's lines, nationals, responses, capital stocks and rates; the
September 27 rough CPS and MEPS keys on audit row-4 weights, the slice scaled to the account's 39,712,493; the v4
receipt lines, state prices, road miles and the pension accrual at whites' own ratios (that lane's rules 1-5,
rekey_sept29.py docstring). Its library is imported read-only (rekey_sept29.setup(), then run29), which writes nothing.
It is not the engine: the engine's union-only corrections (school reprice, college re-key, lane constants) are zero for
whites and whites carry no production term.

Two age structures:
  g3plus_ages  whites' per-age rates at the identified G3+'s age structure (CPS five-year bands, 80+; the lane's own
               reweighting, as its A3 does at the union's ages). The central: C3 is measured on gaps matched by age
               and sex, and the attriters are assumed to have identified G3+'s age mix, so the white end of their
               blend is whites at that age mix. R.PI gains a "g3plus" entry in this process only.
  own          the lane's A1, whites at their own ages (ladder 263's central comparison), beside: it adds whites'
               older age structure to the blend, which on the cash set carries their retirees' benefits.
The A3 run at the union's ages is recomputed as the positive control of the reweighting path.

The engine step puts W's per-person line amounts into every cell of each line (every allocation, key and receipt
scenario), because the rough keys have no allocation arms or key variants: the amounts are the same at both ends
(gate). The capital return is then keyed by the case's component rules on those amounts; the lane's own capital
(its simplified keys) is written beside for the reconciliation.

Inputs : ../white_replacement_2026_09_28/rekey_sept29.py and its inputs (engine_lines_sept29*.json and the rest)
         ../white_replacement_2026_09_28/derived/rekey_summary_sept29.csv (the oracle)
Outputs: derived/white_lines.json, derived/gates_white.json
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/white_lines.py
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
WHITE = FISCAL / "white_replacement_2026_09_28"
ORACLE = WHITE / "derived/rekey_summary_sept29.csv"
# Scenarios the lane published: positive controls for this lane's reading of its library.
CONTROLS = {"own": "A1_third_plus_nh_white", "union_ages_control": "A3_third_plus_nh_white_at_union_ages"}
ACCOUNT_UNION = 39_712_493.3312
GEN = FISCAL / "generation_account_2026_09_24/derived/generation_results_sept29.csv"
BASES = ("accrual", "cash")
ENDS = ("low", "high")

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def main() -> None:
    sys.path.insert(0, str(WHITE))
    print("[the white lane's library: setup (its positive controls; output kept to its failures)]", flush=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import rekey_sept29 as W  # noqa: E402
        n4 = W.setup()
    log = buf.getvalue()
    failed = [ln for ln in log.splitlines() if "FAIL" in ln]
    gate("rekey_sept29.setup(): every positive control of the white lane passes", not failed and not W.FAILS,
         f"{log.count('PASS')} passes" + (f"; {failed[:3]}" if failed else ""))
    gate("the row-4 frame is the account's 39,712,493 (2 persons)", abs(n4 - ACCOUNT_UNION) < 2, f"{n4:,.4f}")
    oracle = {(r["group"], r["basis"], r["end"]): r for r in csv.DictReader(ORACLE.open())}
    # The identified G3+ age structure on the lane's frame: native, both parents born in US areas, Mexican origin, in
    # the civilian household universe (the weights carry it), as generation_account_2026_09_24 frame.py masks G3plus.
    d = W.R.d
    g3 = (d.PRCITSHP.isin([1, 2, 3]) & d.PEFNTVTY.isin(W.R.US) & d.PEMNTVTY.isin(W.R.US) & d.PRDTHSP.eq(1)).to_numpy()
    g3_pop = float(W.R.w[g3].sum())
    g3_account = {float(r["population"]) for r in csv.DictReader(GEN.open()) if r["convention"] == "a" and r["generation"] == "G3plus"}
    g3_account = g3_account.pop() if len(g3_account) == 1 else float("nan")
    gate("the lane's frame holds the account's G3+ (generation_results_sept29.csv, 14,342,575; 50 persons)",
         abs(g3_pop - g3_account) < 50, f"{g3_pop:,.1f} vs {g3_account:,.1f}")
    W.R.PI["g3plus"] = W.R.structure(g3, W.R.w, W.R.cage)
    scen = {"g3plus_ages": W.R.scenario("w3", "g3plus"), "own": W.R.scenario("w3"),
            "union_ages_control": W.R.scenario("w3", "union")}
    for k, sc in scen.items():
        gate(f"{k}: the slice is scaled to the account's count (2 persons)", abs(float(sc["population"]) - ACCOUNT_UNION) < 2,
             f"{float(sc['population']):,.4f}")
    out = {}
    for age, sc in scen.items():
        pop = float(sc["population"])
        out[age] = {}
        for b in BASES:
            out[age][b] = {}
            amounts = {}
            for end in ENDS:
                r, rows, buckets, terms, acc = W.run29(sc, end, b)
                if age in CONTROLS:
                    want = oracle[(CONTROLS[age], b, end)]
                    gate(f"{age} {b} {end}: run29 reproduces rekey_summary_sept29.csv {CONTROLS[age]} cost, capital and net budget (5e-5)",
                         all(abs(r[k] - float(want[k])) < 5e-5 for k in ("cost", "capital", "net_budget")) and r["production_gain"] == 0.0,
                         f"cost {r['cost']:.4f} vs {want['cost']}")
                amounts[end] = {f"{s}|{lid}": a for s, lid, nat, a, resp in rows}
                out[age][b][end] = {
                    "cost_bn": r["cost"], "net_budget_bn": r["net_budget"], "capital_lane_keys_bn": r["capital"],
                    "production_gain_bn": r["production_gain"], "population": pop,
                    "lines": [{"side": s, "id": lid, "national_bn": nat, "amount_bn": a, "response": resp,
                               "per_person_usd": a * 1e9 / pop} for s, lid, nat, a, resp in rows],
                }
            same = max(abs(amounts["low"][k] - amounts["high"][k]) for k in amounts["low"])
            gate(f"{age} {b}: W's line amounts are the same at both ends (no allocation arm in the rough keys)",
                 set(amounts["low"]) == set(amounts["high"]) and same == 0.0, f"max |low - high| {same:.1e} bn")
            zero = [k for k in amounts["low"] if k.split("|", 1)[1] in W.R.ADJUST and amounts["low"][k] != 0.0]
            gate(f"{age} {b}: the engine's union-only corrections are zero for whites", not zero, f"{zero}")
    del out["union_ages_control"]

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    OUT.mkdir(exist_ok=True)
    ages = {"band": [f"{b}+" if b == 80 else f"{b}-{b + 4}" for b in W.R.BANDS],
            "g3plus": [float(x) for x in W.R.PI["g3plus"]], "union": [float(x) for x in W.R.PI["union"]],
            "third_plus_nh_white": [float(x) for x in W.R.structure(W.R.MASK["w3"], W.R.w, W.R.cage)]}
    result = {"meta": {"source": "main_case_lineage_2026_10_05/white_lines.py",
                       "lane": "white_replacement_2026_09_28 (rekey_sept29.run29, scenario w3)",
                       "central": "g3plus_ages",
                       "rule": "the lane's rough re-key on the v4 case (its rules 1-5); per person = amount / the slice's "
                               "population; same amounts at both ends; capital_lane_keys_bn is the lane's own capital "
                               "(its simplified keys), beside the engine's component rules; g3plus_ages reweights the "
                               "slice's CPS and MEPS persons to the identified G3+'s five-year age structure",
                       "g3plus_population_on_lane_frame": g3_pop, "age_structures": ages},
              **out}
    (OUT / "white_lines.json").write_text(json.dumps(result, indent=1) + "\n")
    (OUT / "gates_white.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    for age in out:
        for b in BASES:
            x = out[age][b]
            print(f"  {age} {b}: W costs {x['low']['cost_bn']:.4f} / {x['high']['cost_bn']:.4f} bn, "
                  f"${x['low']['cost_bn'] * 1e9 / x['low']['population']:,.0f} / "
                  f"${x['high']['cost_bn'] * 1e9 / x['high']['population']:,.0f} per person")


if __name__ == "__main__":
    main()
