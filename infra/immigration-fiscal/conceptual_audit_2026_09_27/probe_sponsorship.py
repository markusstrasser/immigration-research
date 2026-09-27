#!/usr/bin/env python3
"""Read-only diagnostics of sponsorship calibration and lineage survival.

Timing arms and survival-consistent birth weights are model sensitivities, not
estimated cohort corrections. Inputs remain in their producing lanes.

The audit read the lineage lane before its §E fix (4e9c2e2). To keep reproducing that
finding, this probe imports the lane's `lineage.py` and `inputs.py` as of a72fd62, the
last commit before the fix, written from git to `_cache/`. Their data paths resolve
against the lane directory, as they did in place. One check confirms that the lane as it
stands gives the survival-weighted gap the audit computed.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SPONSOR = FISCAL / "lineage_sponsored_parents_2026_09_27"
LINEAGE = FISCAL / "lineage_cost_2026_09_19"
AUDITED_AT = "a72fd62"
AUDITED = HERE / "_cache" / f"lineage_cost_{AUDITED_AT}"
FIXED_GAP_0PCT = -1288162.18   # the lane since 4e9c2e2 (lineage_cost_2026_09_19 RESULT, Revisions)


def load_audited_lineage() -> dict:
    """Write the audited `inputs.py` and `lineage.py` to `_cache/` and register them as the
    `inputs` and `lineage` modules, so that `common` binds them. Returns their sha256."""
    AUDITED.mkdir(parents=True, exist_ok=True)
    hashes = {}
    for name in ("inputs", "lineage"):  # lineage imports inputs
        src = subprocess.run(["git", "-C", str(FISCAL), "show",
                              f"{AUDITED_AT}:infra/immigration-fiscal/lineage_cost_2026_09_19/{name}.py"],
                             capture_output=True, check=True).stdout
        path = AUDITED / f"{name}.py"
        path.write_bytes(src)
        spec = importlib.util.spec_from_file_location(name, path)
        module = importlib.util.module_from_spec(spec)
        module.__file__ = str(LINEAGE / f"{name}.py")  # data paths resolve as they did in place
        sys.modules[name] = module
        spec.loader.exec_module(module)
        hashes[str(path.relative_to(FISCAL))] = hashlib.sha256(src).hexdigest()
    return hashes


AUDITED_SHA256 = load_audited_lineage()
sys.path.insert(0, str(SPONSOR))
import common as C  # noqa: E402  (binds the audited `inputs` and `lineage` registered above)
import pandas as pd  # noqa: E402


def fixed_lane_gap() -> float:
    """Central lineage gap at 0% from the lane as it stands. It runs in a fresh interpreter,
    because this one holds the audited modules under the lane's module names."""
    code = (f"import sys; sys.dont_write_bytecode = True; sys.path.insert(0, {str(SPONSOR)!r}); "
            "import common as C; c = C.Ctx(); "
            "print(repr(C.disc(C.total_stream(c.mex()), 0) - C.disc(C.total_stream(c.white()), 0)))")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, check=True)
    return float(r.stdout.split()[-1])


def main() -> None:
    ctx = C.Ctx()
    cal = json.loads((SPONSOR / "derived/calibration.json").read_text())
    table = pd.read_csv(SPONSOR / "derived/calibration.csv")
    row = table[(table.window == "central") & (table.estimator == "equal_hazard")].iloc[0]
    stock = table[(table.window == "central") & (table.estimator == "stock_hazard_x_e59")].iloc[0]
    duration = (row.naturalised_adults_2024 + row.g2_adults_21plus) / (
        row.naturalisations_per_year + row.g2_turning_21_per_year
    )
    ratio = stock.E_parents_per_naturalised / row.E_parents_per_naturalised
    assert abs(ratio - row.e59_total_table / duration) < 1e-12

    p = cal["E_chosen"]["central"] / cal["m_living_parents_at_60"]
    timing = []
    for delay in (0, 4, 10):
        age, year = 60 + delay, 6 + delay
        parents = cal["naturalisation_rate"] * p * ctx.living_parents(age, gap=29)
        vec = C.PA.late_profile(ctx.mb, ctx.acs, age, "statutory", "central", ctx.bar_price)
        stream = ctx.parent_stream(vec, age, year)
        timing.append({"extra_years_after_baseline": delay, "parent_age": age,
                       "admission_year": year, "parents": parents,
                       "channel_0pct": parents * C.disc(stream, 0),
                       "channel_3pct": parents * C.disc(stream, .03)})
    arms = pd.read_csv(SPONSOR / "derived/arms.csv")
    for rate, key in ((0.0, "channel_0pct"), (.03, "channel_3pct")):
        stored = arms[(arms.arm == "2_L25_a60_pcal_central_new_central")
                      & (arms.discount == rate)].iloc[0]
        assert abs(timing[0][key] - stored.channel) < .001

    # Under the lane's point-birth-at-29 convention, expected births require a
    # surviving parent. The audited count recurrence omits these probabilities
    # (fixed in 4e9c2e2).
    lx = ctx.tables["total"].lx.to_numpy()
    first_survival = float(lx[C.L.GEN_LEN] / lx[C.FOUNDER_AGE])
    later_survival = float(lx[C.L.GEN_LEN] / lx[0])
    by_lineage = {}
    for name, groups in (("mexican", ctx.mex()), ("white", ctx.white())):
        weights = {g: (1.0 if g == "G1" else
                       first_survival * later_survival ** (int(g[1:]) - 2)) for g in groups}
        original = sum(v[1] for v in groups.values())
        adjusted = sum(weights[g] * v[1] for g, v in groups.items())
        by_lineage[name] = {
            "generation_counts": {g: {"original": float(v[0]),
                                       "survival_weighted": float(v[0] * weights[g])}
                                  for g, v in groups.items()},
            "fiscal": {str(r): {"original": C.disc(original, r),
                                 "survival_weighted": C.disc(adjusted, r)}
                       for r in (0, .03)}}
    gap = {str(r): {k: by_lineage["mexican"]["fiscal"][str(r)][k]
                      - by_lineage["white"]["fiscal"][str(r)][k]
                   for k in ("original", "survival_weighted")} for r in (0, .03)}
    assert abs(gap["0"]["original"] + 1297150.3576) < .01
    fixed = fixed_lane_gap()
    assert abs(fixed - FIXED_GAP_0PCT) < .01

    # Hold fiscal profiles fixed and perturb only survival before reproduction.
    # The audited lineage function leaves the number born in every generation fixed.
    altered_tables = {k: v.copy() for k, v in ctx.tables.items()}
    for tab in altered_tables.values():
        tab.loc[tab.index >= C.L.GEN_LEN, ["lx", "Lx"]] *= .5
    altered = C.L.lineage(ctx.profiles, altered_tables, ctx.cfg())
    baseline = ctx.mex()
    unchanged_counts = all(altered[g][0] == baseline[g][0] for g in altered)
    assert unchanged_counts
    paths = [SPONSOR / "arms.py", SPONSOR / "common.py", SPONSOR / "calibration.py",
             SPONSOR / "derived/calibration.csv", C.LINEAGE_DIR / "lineage.py",
             C.LINEAGE_DIR / "inputs.py"]
    print(json.dumps({
        "checks_passed": True,
        "interpretation": "Diagnostics and conditional sensitivities; no corrected forecast",
        "calibration": {"stock_over_eligible_inflow_years": float(duration),
                        "parent_remaining_life_years": float(row.e59_total_table),
                        "stock_over_flow_estimate_ratio": float(ratio),
                        "ratio_cancels_admissions_numerator": True},
        "sponsorship_timing_fixed_p_and_naturalization_probability": timing,
        "lineage": {"survival_25_to_29": first_survival, "survival_0_to_29": later_survival,
                    "counts_unchanged_when_survival_halved_at_29": unchanged_counts,
                    "by_lineage": by_lineage, "gap": gap,
                    "fixed_lane_gap_0pct": fixed,
                    "survival_weighted_minus_fixed_lane_0pct": gap["0"]["survival_weighted"] - fixed},
        "audited_lineage": {"commit": AUDITED_AT, "sha256": AUDITED_SHA256},
        "source_sha256": {str(p.relative_to(FISCAL)): hashlib.sha256(p.read_bytes()).hexdigest()
                          for p in paths}
    }, indent=2))


if __name__ == "__main__":
    main()
