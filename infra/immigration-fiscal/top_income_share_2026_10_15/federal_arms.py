"""Hold the case's IRS/CBO national cell masses fixed; replace upper-bin union shares.

The baseline is the *published-weight*, nominal-AGI CPS key. Row4 and status
adjustments belong to the case's subsequent stack, not a second CPS rake.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent


def load_keys():
    spec = importlib.util.spec_from_file_location(
        "top_income_case_keys", FISCAL / "tax_key_heldout_2026_09_28/keys.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def rake(total, rows, cols):
    """The same iterative proportional fitting as heldout.py, zero cells retained."""
    total, rows, cols = map(lambda x: np.asarray(x, float), (total, rows, cols))
    if np.any(total < 0) or np.any(total.sum(axis=0) <= 0) or np.any(total.sum(axis=1) <= 0):
        raise ValueError("[BLOCKED] negative tax mass or unsupported raking margin")
    r = rows[:, None] * total / total.sum(axis=1, keepdims=True)
    for _ in range(20000):
        r *= cols[None, :] / r.sum(axis=0)[None, :]
        r *= (rows / r.sum(axis=1))[:, None]
        if max(abs(r.sum(axis=0) - cols).max(), abs(r.sum(axis=1) - rows).max()) < 1e-12:
            return r
    raise ValueError("[BLOCKED] IRS/CBO rake did not converge")


def nonincreasing(values, weights):
    """Weighted least-squares isotonic fit, constrained to a non-increasing sequence."""
    blocks = []
    for i, (v, w) in enumerate(zip(values, weights, strict=True)):
        if not (np.isfinite(v) and np.isfinite(w) and w > 0):
            raise ValueError("[BLOCKED] isotonic rule requires finite supported bins")
        blocks.append([i, i + 1, float(v * w), float(w)])
        while len(blocks) > 1 and blocks[-2][2] / blocks[-2][3] < blocks[-1][2] / blocks[-1][3]:
            b = blocks.pop()
            a = blocks.pop()
            blocks.append([a[0], b[1], a[2] + b[2], a[3] + b[3]])
    out = np.empty(len(values))
    for start, stop, vw, w in blocks:
        out[start:stop] = vw / w
    return out


def move_bin_share(theta, mass, target):
    """A bounded shift that preserves the ordering of CBO-cell shares inside a bin.

    A common mixture toward the all-zero or all-one vector hits the requested
    aggregate share while retaining bounded, ordered cell shares.
    """
    theta, mass = np.asarray(theta, float), np.asarray(mass, float)
    if not 0 <= target <= 1 or mass.sum() <= 0:
        raise ValueError("[BLOCKED] invalid target share or bin mass")
    current = float(mass @ theta / mass.sum())
    if abs(current - target) < 1e-14:
        return theta.copy()
    if target < current:
        return theta * (target / current)
    return theta + (1 - theta) * ((target - current) / (1 - current))


def main():
    keys = load_keys()
    cells_path = HERE / "derived/cps_cells.csv"
    cells = pd.read_csv(cells_path)
    cbo = keys.cbo_shares()
    groups = [g for g, v in cbo.items() if v > 0]
    _, irs = keys.irs_2023()
    cols = keys._pool14(irs)

    def arrays(sample):
        table = cells[cells["sample"].eq(sample)].set_index(["cbo_group", "bin14"])
        index = pd.MultiIndex.from_product([groups, range(14)], names=["cbo_group", "bin14"])
        table = table.reindex(index)
        if table.total_fedtax.isna().any():
            raise ValueError(f"[BLOCKED] missing cells: {sample}")
        t = table.total_fedtax.to_numpy().reshape(len(groups), 14)
        u = table.union_fedtax.to_numpy().reshape(len(groups), 14)
        return t, np.divide(u, t, out=np.zeros_like(u), where=t > 0)

    total, theta0 = arrays("baseline_2025_nominal")
    mass = rake(total, [cbo[g] for g in groups], cols)
    baseline = float((mass * theta0).sum())
    held = json.loads((FISCAL / "tax_key_heldout_2026_09_28/derived/translation_inputs.json").read_text())
    want = held["reweighted_share"]["personal"] + held["share_change"]["irs_2023_raked_with_cbo_groups"]["personal"]
    if abs(baseline - want) > 1e-12:
        raise ValueError(f"[BLOCKED] current key does not reproduce heldout: {baseline} vs {want}")
    pooled_total, pooled_theta = arrays("pooled_real2023")
    if np.any((total > 0) & (pooled_total <= 0)):
        raise ValueError("[BLOCKED] pooled sample cannot support the baseline's tax cells")
    binshare = lambda th: (mass * th).sum(axis=0) / cols
    current_bins, pooled_bins = binshare(theta0), binshare(pooled_theta)
    central = nonincreasing(pooled_bins[11:], cols[11:])
    source_bins = pd.read_csv(FISCAL / "tax_key_heldout_2026_09_28/derived/translation_bins.csv")
    pre_joint_500 = float(source_bins.loc[(source_bins.allocation == "personal") & (source_bins.bin == 13), "union_share_in_bin"].iloc[0])
    variants = {"current": theta0.copy()}
    for name, bins, shares in [
        ("carry_500k", [13], [current_bins[12]]),
        ("carry_500k_pre_joint_rake", [13], [pre_joint_500]),
        ("fixed_1_5pct", [13], [0.015]),
        ("pooled_top_only", [13], [pooled_bins[13]]),
        ("pooled_unconstrained", [11, 12, 13], pooled_bins[11:]),
        ("pooled_monotone_central", [11, 12, 13], central),
    ]:
        th = theta0.copy()
        for b, s in zip(bins, shares, strict=True):
            th[:, b] = move_bin_share(theta0[:, b], mass[:, b], float(s))
        variants[name] = th
    arms = {}
    for name, th in variants.items():
        value = float((mass * th).sum())
        arms[name] = {"share": value, "share_change": value - baseline,
                      "upper_bin_shares": binshare(th)[11:].tolist()}
    if abs(arms["current"]["share_change"]) > 1e-15:
        raise ValueError("[BLOCKED] current arm moved the case")
    result = {"baseline_share": baseline, "current_upper_bin_shares": current_bins[11:].tolist(),
              "pre_joint_rake_500k_share": pre_joint_500,
              "pooled_upper_bin_shares_on_case_masses": pooled_bins[11:].tolist(),
              "upper_bins": ["$200k–500k", "$500k–1M", "$1M+"],
              "irs_bin_masses": cols.tolist(), "cbo_groups": groups,
              "raked_cell_masses": mass.tolist(), "arms": arms,
              "rule": "pooled real2023 cell shares aggregated using the case's fixed IRS/CBO cell masses; weighted non-increasing fit above $200k",
              "held_fixed": "national IRS and CBO margins; below-$200k shares; status/row4 stack factors; v5-v8 added-person, white-end, mixed-unit, coverage and production corrections",
              "inputs_sha256": {str(p.relative_to(FISCAL)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [cells_path, FISCAL / "tax_key_heldout_2026_09_28/keys.py",
                                          FISCAL / "tax_key_heldout_2026_09_28/derived/translation_inputs.json"]}}
    (HERE / "derived/federal_arms.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("PASS current IRS/CBO key parity; wrote federal_arms.json")


if __name__ == "__main__":
    main()
