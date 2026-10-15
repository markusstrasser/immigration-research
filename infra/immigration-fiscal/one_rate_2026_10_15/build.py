"""Reprice corrected v8 at one real rate per specification, importing upstream read-only.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/one_rate_2026_10_15/build.py
"""
from __future__ import annotations

import hashlib
import copy
import json
import resource
import subprocess
import sys
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "pension_tr2026_2026_10_06"))
import pension_tr2026 as T  # noqa: E402
import render_result  # noqa: E402


def require(condition, message):
    if not condition:
        raise RuntimeError(f"[BLOCKED] one_rate: {message}")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def row4_lane(lane):
    """Replay row4_oct07.py:93-114 on the same person frame and declared factors."""
    source = json.loads((FISCAL / "row4_class_2026_09_29/derived/row4_parta.json").read_text())
    factors = source["factors"]
    with zipfile.ZipFile(FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip") as archive:
        states = T.pd.read_csv(archive.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
    out = copy.copy(lane)
    for key in ("p", "q"):
        frame = getattr(lane, key)
        st = frame[["PH_SEQ"]].merge(states, on="PH_SEQ", how="left", validate="many_to_one").GESTFIPS.to_numpy()
        require(not T.np.isnan(st.astype(float)).any(), "row4 person missing state")
        mexico = (frame.PENATVTY.to_numpy() == 303) & ~T.np.isin(st, [6, 48])
        f = T.np.ones(len(frame))
        f[mexico & (frame.PRCITSHP.to_numpy() == 4)] = factors["natz"]
        f[mexico & (frame.PRCITSHP.to_numpy() == 5)] = factors["noncit"]
        setattr(out, key, frame.assign(w=frame.w.to_numpy() * f))
    require(abs(out.p.loc[out.p.union, "w"].sum() - 39712493) < 1, "row4 population differs")
    return out


def rate_arms():
    load_start = time.perf_counter()
    lane = T.Lane()
    print(f"[timing] source_lane_load_seconds={time.perf_counter()-load_start:.3f}", flush=True)
    row4_start = time.perf_counter()
    lane4 = row4_lane(lane)
    print(f"[timing] row4_load_seconds={time.perf_counter()-row4_start:.3f}", flush=True)
    paths, _ = T.build_paths(lane.econ)
    denominator = T.grid(lane.econ, lane.prelim, paths["oasdi_2025"], [T.BASE])
    mortality = T.T.quotes()["tr2026_mortality_decline"]["value"]
    arms = {}
    for label, rate in (("unchanged", None), ("flat_2", 0.02), ("flat_3", 0.03)):
        arm_start = time.perf_counter()
        econ = T.economy_2026(rates=True, wages=True, parameters=True)
        original_discount = econ.discount
        if rate is not None:
            # Preserve the upstream rate-arm construction: historical accumulation
            # unchanged, future new-issue discounting replaced by a flat real rate.
            econ.discount = lambda arm, r=rate, original=original_discount: original(r if arm == "new_issue" else arm)
        T.L.survival.cache_clear()
        with T.patched(T.L, "_decline", lambda: (mortality["65plus"], mortality["total"])), T.patched(
                T.PA, "hi_cost_path", T.hi_cost_path_tr2026):
            grid = T.hybrid(T.grid(econ, lane.prelim, paths["separate_2026"], [T.G]), denominator)
            result = T.run_arm(lane, grid, paths["separate_2026"], paths["hi_2026"],
                               econ=econ, share=T.tob_share_tr2026())
            result4 = T.run_arm(lane4, grid, paths["separate_2026"], paths["hi_2026"],
                                econ=econ, share=T.tob_share_tr2026())
        arms[label] = {k: v for k, v in result.items() if not k.startswith("_")}
        arms[label]["result_row4"] = {k: v for k, v in result4.items() if not k.startswith("_")}
        print(f"[rates] {label}: OASDI net/tax {result['ratio_net']:.12f}; Part A {result['part_a_bn']:.12f}bn; seconds={time.perf_counter()-arm_start:.3f}", flush=True)
    T.L.survival.cache_clear()
    stored = json.loads((T.OUT / "summary.json").read_text())["beside"]["all_2026_inputs_separate_funds"]
    require({"ratio_net", "part_a_bn", "future_share_group"}.issubset(stored), "Trustees summary control schema changed")
    row4 = json.loads((FISCAL / "row4_class_2026_09_29/derived/row4_oct07_inputs.json").read_text())["pension"]["results"]["arm"]["row4"]
    for group in T.GROUPS:
        for key, value in row4["groups"][group].items():
            require(abs(arms["unchanged"]["result_row4"]["groups"][group][key] - value) < 1e-10,
                    f"row4 unchanged {group}/{key} differs")
    for key in ("ratio_net", "part_a_bn", "future_share_group"):
        require(abs(arms["unchanged"][key] - stored[key]) < 1e-10, f"Trustees unchanged {key} differs")
    # summary.json deliberately flattens groups; arms.csv retains the complete
    # group data, serialized to nine decimal places by its producer.
    table = T.pd.read_csv(T.OUT / "arms.csv")
    require({"arm", "group", "per_tax_dollar", "net_per_tax_dollar", "part_a_per_hi_tax_dollar"}.issubset(table.columns),
            "Trustees group CSV schema changed")
    for group in T.GROUPS:
        row = table[(table.arm == "all_2026_inputs_separate_funds") & (table.group == group)]
        require(len(row) == 1, f"missing Trustees control group {group}")
        for key in ("per_tax_dollar", "part_a_per_hi_tax_dollar", "net_own_rate"):
            expected = float(row.iloc[0]["net_per_tax_dollar" if key == "net_own_rate" else key])
            actual = arms["unchanged"]["ratio_net"] if key == "net_own_rate" and group == "union" else arms["unchanged"]["groups"][group][key]
            require(abs(actual - expected) < 5.1e-10,
                    f"unchanged {group}/{key} differs")
    econ = T.economy_2026(rates=True, wages=True, parameters=True)
    return {"arms": arms, "trustees_capital": perpetuity_equivalent(econ)}


def perpetuity_equivalent(econ):
    """A transparent flat capital rate for a level real perpetuity on this path."""
    # A level perpetuity at the capital stock's 2024 real replacement value.
    # Same annual timing/indexing as upstream discount(), inflation deflates
    # every future payment. Extend the ultimate rate after the 2200 horizon.
    discount = econ.discount("new_issue")
    k0 = 2024 - T.L.Y0
    nominal = T.pd.Series(econ.new_issue_nominal).ffill().bfill().to_numpy()
    real = (1 + nominal) / (1 + econ.cola) - 1
    inflation = 1.0
    factors = []
    for k in range(k0 + 1, len(discount)):
        inflation *= 1 + econ.cola[k - 1]
        factors.append(float(discount[k] * inflation))
    terminal = float(real[-1])
    require(terminal > 0, "nonpositive ultimate real rate")
    annuity = sum(factors) + factors[-1] / terminal
    equivalent = 1 / annuity
    return {"flat_real_equivalent": equivalent,
            "derivation": "inverse PV of annual end-year constant-real perpetuity; 2025-2200 discount/COLA factors from imported Economy, then ultimate-rate tail",
            "annuity_factor": annuity, "ultimate_real_rate": terminal,
            "real_path_2024_2040": {str(y): float(real[y - T.L.Y0]) for y in range(2024, 2041)}}


def main():
    start = time.perf_counter()
    require((HERE / "evaluate.cjs").is_file(), "evaluate.cjs is missing")
    OUT.mkdir(exist_ok=True)
    rates = rate_arms()
    write_json(OUT / "rates.json", rates)
    eval_start = time.perf_counter()
    subprocess.run(["node", str(HERE / "evaluate.cjs")], check=True)
    print(f"[timing] full_evaluator_seconds={time.perf_counter()-eval_start:.3f}", flush=True)
    inventory_start = time.perf_counter()
    inventory = subprocess.run(["node", str(HERE / "inventory_sizes.cjs")], check=True, capture_output=True, text=True)
    print(f"[timing] external_normal_cost_probe_seconds={time.perf_counter()-inventory_start:.3f}", flush=True)
    write_json(OUT / "inventory_sizes.json", json.loads(inventory.stdout))
    inputs = ["main_case_2026_10_15/derived/summary.json", "main_case_2026_10_15/derived/corrections.json",
              "main_case_2026_10_15/derived/corrections_cash.json", "pension_tr2026_2026_10_06/derived/summary.json",
              "pension_tr2026_2026_10_06/derived/arms.csv", "row4_class_2026_09_29/derived/row4_oct07_inputs.json",
              "row4_class_2026_09_29/derived/row4_parta.json", "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
              "within_group_distribution_2026_09_29/_cache/oct14/lines.json",
              "coverage_bound_2026_10_14/derived/coverage_bound_oct15.json",
              "union_completion_2026_10_14/derived/pricing_lines.csv",
              "main_case_2026_10_15/package.cjs", "main_case_2026_10_14/item_row4.cjs",
              "main_case_2026_10_15/item_union.cjs", "main_case_2026_10_15/child_records.cjs"]
    inputs += sorted({str(Path(m.__file__).relative_to(FISCAL)) for m in sys.modules.values()
                      if getattr(m, "__file__", None) and Path(m.__file__).is_relative_to(FISCAL)
                      and not Path(m.__file__).is_relative_to(HERE)})
    write_json(OUT / "source_hashes.json", {p: hashlib.sha256((FISCAL / p).read_bytes()).hexdigest() for p in inputs})
    render_result.render()
    print(f"[measurement] seconds={time.perf_counter()-start:.3f}; python_maxrss={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}; children_maxrss={resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}")


if __name__ == "__main__":
    main()
