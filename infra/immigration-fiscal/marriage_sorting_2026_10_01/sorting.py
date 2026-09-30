"""CPS 2022-25 descriptive marital sorting relative to explicit peer pools.

No ethnicity-preference or racism parameter is identified. See README.md.
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <lane>/sorting.py
"""
from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path
import warnings

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "civic_trajectory_mexican_2026_09_27" / "asec_intermarriage.py"
spec = importlib.util.spec_from_file_location("civic_marriage", SOURCE)
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
FLAGS = ("ind_origin", "mex_origin", "nh_white", "nh_black")
GROUPS = {
    "Indian G2": ("ind_G2", "ind_origin"),
    "Native NH white": ("white_native", "nh_white"),
    "Native NH black": ("black_native", "nh_black"),
    "Mexican G2": ("mex_G2", "mex_origin"),
    "Mexican G3+": ("mex_G3plus", "mex_origin"),
    "Indian G1": ("ind_G1", "ind_origin"),
    "NH white G2": ("white_G2", "nh_white"),
    "NH black G2": ("black_G2", "nh_black"),
}
# Pool, partner characteristics held fixed, and whether to use ego characteristics.
SPECS = {
    "married_state": ("married", (), False),
    "married_age_education": ("married", ("ageband", "ba"), False),
    "married_age_education_earnings": ("married", ("ageband", "ba", "earn"), False),
    "adults_state": ("adults", (), False),
    "adults_age_education": ("adults", ("ageband", "ba"), False),
    "adults_age_education_earnings": ("adults", ("ageband", "ba", "earn"), False),
    "adults_own_age_education_earnings": ("adults", ("ageband", "ba", "earn"), True),
}
PRIMARY = "married_age_education_earnings"
WINDOWS = {"2022-2025": (2022, 2023, 2024, 2025), "2022-2023": (2022, 2023), "2024-2025": (2024, 2025)}


def classify(d):
    d = base.origin(d.copy())
    d["nh_black"] = d.non_hisp & d.PRDTRACE.eq(2)
    native = d.PRCITSHP.isin([1, 2, 3])
    parent_ind_mex = d.PEMNTVTY.isin([210, 303]) | d.PEFNTVTY.isin([210, 303])
    # Unknown (-4/0/999) is never assigned as a known foreign-born parent.
    foreign_parent = d.PEMNTVTY.between(100, 899) | d.PEFNTVTY.between(100, 899)
    d["white_native"] = d.usb_nh_white
    d["black_native"] = native & d.nh_black & ~parent_ind_mex
    d["white_G2"] = d.white_native & foreign_parent
    d["black_G2"] = d.black_native & foreign_parent
    for group in ("ind_G1", "ind_G2"):
        d[group] = d.igen.eq(group)
    for group in ("mex_G2", "mex_G3plus"):
        d[group] = d.gen.eq(group)
    d["ageband"] = (d.A_AGE >= 40).astype(int)
    d["ba"] = (d.A_HGA >= 43).astype(int)
    d["earn"] = np.select([d.PEARNVAL <= 0, d.PEARNVAL < 75000], [0, 1], default=2)
    return d


def link_marriages(d):
    m = d[d.A_AGE.between(25, 54) & d.A_MARITL.isin([1, 2])].copy()
    sp = d.set_index(["PH_SEQ", "A_LINENO"]).reindex(
        pd.MultiIndex.from_arrays([m.PH_SEQ, m.A_SPOUSE]))
    if not sp.PPPOS.notna().all() or not (sp.A_SPOUSE.to_numpy() == m.A_LINENO.to_numpy()).all():
        raise ValueError("Missing or nonreciprocal spouse pointer")
    for col in FLAGS + ("A_SEX", "A_AGE", "ageband", "ba", "earn"):
        m["sp_" + col] = sp[col].to_numpy()
    audit = {"married_ego_25_54": len(m), "same_sex_records": int(m.A_SEX.eq(m.sp_A_SEX).sum())}
    m = m[m.A_SEX.ne(m.sp_A_SEX)].copy()
    audit["opposite_sex_spouse_outside_25_54"] = int((~m.sp_A_AGE.between(25, 54)).sum())
    # Preserve this unrestricted-spouse slice solely for legacy parity.
    legacy = m
    m = m[m.sp_A_AGE.between(25, 54)].copy()
    audit["both_spouses_25_54"] = len(m)
    return m, legacy, audit


def peer_shares(pool, egos, extras, own):
    """Return per-ego shares under all 161 weights; never clip/fill an invalid cell."""
    keys = ["GESTFIPS", "A_SEX", *extras]
    cells = pool.groupby(keys, sort=True).indices
    cell_index = pd.MultiIndex.from_tuples(list(cells), names=keys)
    w = pool[base.WCOLS].to_numpy(float)
    shares = np.empty((len(cells), len(FLAGS), base.R))
    cell_n = np.empty(len(cells))
    cell_eff = np.empty(len(cells))
    for j, idx in enumerate(cells.values()):
        cw = w[idx]
        den = cw.sum(axis=0)
        if np.any(den <= 0):
            raise ValueError(f"Nonpositive replicate pool denominator in cell {cell_index[j]}")
        cell_n[j] = len(idx)
        cell_eff[j] = den[0] ** 2 / np.square(cw[:, 0]).sum()
        for k, flag in enumerate(FLAGS):
            shares[j, k] = (cw * pool[flag].to_numpy()[idx, None]).sum(axis=0) / den
    if np.any((shares < 0) | (shares > 1)):
        raise ValueError("Replicate pool share outside [0,1]")
    arrays = [egos.GESTFIPS, 3 - egos.A_SEX]
    arrays += [egos[x if own else "sp_" + x] for x in extras]
    pos = cell_index.get_indexer(pd.MultiIndex.from_arrays(arrays))
    valid = pos >= 0
    if not valid.all() and not own:
        raise ValueError("Actual spouse's comparison cell missing")
    return shares, pos, valid, cell_n, cell_eff


def metric(totals, name):
    """totals=(denominator, observed numerator, expected numerator)."""
    den, obs, expected = totals
    if np.any(den <= 0):
        raise ValueError("Nonpositive group denominator")
    p, q = obs / den, expected / den
    if np.any((p <= 0) | (p >= 1) | (q <= 0) | (q >= 1)):
        raise ValueError("Boundary p or q: log-odds index not estimable")
    if name == "p":
        return p
    if name == "q":
        return q
    if name == "log_K":
        return np.log(p / (1 - p)) - np.log(q / (1 - q))
    raise ValueError(name)


def pooled_value_se(blocks, name, reference=None):
    """First-order worst-covariance SE across year blocks, including reference covariance.

    Replace one year's totals at a time. Aligned replicate indices across years
    are not interpreted as a valid pooled survey design.
    """
    total = sum(b[:, 0] for b in blocks)
    ref_total = sum(b[:, 0] for b in reference) if reference is not None else None
    point = metric(total, name)
    if reference is not None:
        point -= metric(ref_total, name)
    components = []
    for j, block in enumerate(blocks):
        replicate = metric(total[:, None] - block[:, :1] + block, name)
        if reference is not None:
            rb = reference[j]
            replicate -= metric(ref_total[:, None] - rb[:, :1] + rb, name)
        components.append(base.se_sdr(replicate))
    return float(point), float(sum(components))


def run(out):
    warnings.filterwarnings("ignore", category=pd.errors.PerformanceWarning)
    if "PEARNVAL" not in base.PCOLS:
        base.PCOLS = base.PCOLS + ["PEARNVAL"]
    blocks, counts, diagnostics, gates, parity = {}, {}, [], [], []
    old = pd.read_csv(SOURCE.parent / "derived/intermarriage.csv")
    old_checks = [("ind_G2", "ind_G2", "spouse_indian_origin", "ind_origin"),
                  ("ind_G1", "ind_G1", "spouse_indian_origin", "ind_origin"),
                  ("mex_G2", "mex_G2", "spouse_mexican_origin", "mex_origin"),
                  ("white_native", "usb_nh_white", "spouse_nh_white", "nh_white")]
    legacy_sums = {x[0]: np.zeros(3) for x in old_checks}
    for year in base.ARCHIVES:
        d = classify(base.load_year(year))
        m, legacy, gate = link_marriages(d)
        gates.append({"year": year, **gate})
        for mask, _, _, flag in old_checks:
            f = legacy[legacy[mask]]
            legacy_sums[mask] += [len(f), f.pwwgt0.sum(), (f.pwwgt0 * f["sp_" + flag]).sum()]
        for spec_name, (pool_name, extras, own) in SPECS.items():
            pool = m if pool_name == "married" else d[d.A_AGE.between(25, 54)]
            shares, pos, valid, ns, effs = peer_shares(pool, m, extras, own)
            if not valid.all():
                print(f"[DEGRADED] {year} {spec_name}: {int((~valid).sum())} records lack an own-stratum pool; exclusions are recorded in pool_diagnostics.csv", flush=True)
            for group, (flag, origin) in GROUPS.items():
                for sex, sex_code in (("both", None), ("men", 1), ("women", 2)):
                    selected = m[flag].to_numpy() & (True if sex_code is None else m.A_SEX.eq(sex_code).to_numpy())
                    good = selected & valid
                    f = m[good]
                    if len(f) == 0:
                        raise ValueError(f"Empty group {year} {spec_name} {group} {sex}")
                    w = f[base.WCOLS].to_numpy(float)
                    q = shares[pos[good], FLAGS.index(origin)]
                    key = (spec_name, group, sex, year)
                    blocks[key] = np.stack([w.sum(axis=0),
                        (w * f["sp_" + origin].to_numpy()[:, None]).sum(axis=0), (w * q).sum(axis=0)])
                    counts[key] = len(f)
                    full_weight = m.loc[selected, "pwwgt0"].sum()
                    excluded = np.zeros(len(f), dtype=bool)
                    for x in extras:
                        excluded |= f[x].to_numpy() != f["sp_" + x].to_numpy()
                    # q=0/1 is allowed for individual cells, never silently clipped.
                    diagnostics.append({"year": year, "spec": spec_name, "group": group, "sex": sex,
                        "n_selected": int(selected.sum()), "n_used": len(f), "weight_selected": full_weight,
                        "weight_used": w[:, 0].sum(), "missing_pool_weight": full_weight - w[:, 0].sum(),
                        "weighted_pool_n_sum": (w[:, 0] * ns[pos[good]]).sum(),
                        "weighted_pool_effective_n_sum": (w[:, 0] * effs[pos[good]]).sum(),
                        "pool_n_below_20_weight": w[ns[pos[good]] < 20, 0].sum(),
                        "q_zero_weight": w[q[:, 0] == 0, 0].sum(),
                        "q_one_weight": w[q[:, 0] == 1, 0].sum(),
                        "actual_spouse_outside_own_stratum_weight": w[excluded, 0].sum() if own else 0.0})
        print(f"  {year}: all peer pools and replicates complete", flush=True)
    for mask, generation, measure, _ in old_checks:
        previous = old[(old.generation == generation) & (old.measure == measure) & (old.adjustment == "raw")].iloc[0]
        n, den, num = legacy_sums[mask]
        if n != previous.n or abs(num / den - previous.estimate) >= 1e-6:
            raise ValueError(f"Legacy parity failed: {mask}")
        parity.append({"group": mask, "n": int(n), "p": num / den, "legacy_p": previous.estimate})
    rows = []
    for window, years in WINDOWS.items():
        for spec_name in SPECS:
            for sex in ("both", "men", "women"):
                for group in GROUPS:
                    bs = [blocks[(spec_name, group, sex, y)] for y in years]
                    row = {"window": window, "spec": spec_name, "group": group, "sex": sex,
                           "n_person_year_records": sum(counts[(spec_name, group, sex, y)] for y in years)}
                    for name in ("p", "q", "log_K"):
                        point, se = pooled_value_se(bs, name)
                        row[name], row[name + "_se_overlap_bound"] = point, se
                    row["K"] = np.exp(row["log_K"])
                    row["K_low95"] = np.exp(row["log_K"] - 1.96 * row["log_K_se_overlap_bound"])
                    row["K_high95"] = np.exp(row["log_K"] + 1.96 * row["log_K_se_overlap_bound"])
                    row["observed_over_expected"] = row["p"] / row["q"]
                    row["normalized_excess"] = (row["p"] - row["q"]) / (1 - row["q"])
                    for ref, label in (("Native NH white", "white"), ("Native NH black", "black"), ("NH white G2", "white_G2")):
                        rb = [blocks[(spec_name, ref, sex, y)] for y in years]
                        value, se = pooled_value_se(bs, "log_K", rb)
                        row["ratio_to_" + label] = np.exp(value)
                        row["ratio_to_" + label + "_low95"] = np.exp(value - 1.96 * se)
                        row["ratio_to_" + label + "_high95"] = np.exp(value + 1.96 * se)
                    rows.append(row)
    out.mkdir(parents=True, exist_ok=True)
    result = pd.DataFrame(rows)
    result.to_csv(out / "estimates.csv", index=False, float_format="%.10g", lineterminator="\n")
    pd.DataFrame(diagnostics).to_csv(out / "pool_diagnostics.csv", index=False, float_format="%.10g", lineterminator="\n")
    pd.DataFrame(parity).to_csv(out / "legacy_parity.csv", index=False, float_format="%.10g", lineterminator="\n")
    # Deterministic, inspectable replicate sufficient statistics, also used by tests.
    replicate_rows = []
    for key, b in blocks.items():
        for r in range(base.R):
            replicate_rows.append(dict(zip(("spec", "group", "sex", "year"), key)) |
                                  {"replicate": r, "den": b[0, r], "observed_num": b[1, r], "expected_num": b[2, r]})
    pd.DataFrame(replicate_rows).to_csv(out / "replicate_totals.csv", index=False, float_format="%.12g", lineterminator="\n")
    manifest = {"primary_spec": PRIMARY, "source_script": str(SOURCE.relative_to(HERE.parents[2])),
                "source_script_sha256": base.sha(SOURCE), "generator_sha256": base.sha(Path(__file__)),
                "archives": {str(y): {"path": str(p), "sha256": h} for y, (p, h) in base.ARCHIVES.items()},
                "gates": gates, "legacy_parity": "PASS", "estimand": "descriptive opportunity-adjusted odds index",
                "uncertainty": "sum of year-block replicate SEs; first-order worst-covariance overlap bound"}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    primary = result[(result.window == "2022-2025") & (result.spec == PRIMARY) & (result.sex == "both")]
    print(primary[["group", "n_person_year_records", "p", "q", "K", "ratio_to_white", "ratio_to_white_low95", "ratio_to_white_high95"]].to_string(index=False))
    print("PASS: hashes, weights, reciprocal spouse links, legacy parity, and all replicate denominators")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    run(args.out)
