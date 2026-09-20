#!/usr/bin/env python3
"""SDR replicate variance for the institutional-cost bound on the Mexican-origin fiscal gaps.

Recomputes every quantity in ../institutional_bound_2026_09_17/derived/institutional_bound.csv
(headline `adverse` and `moderate` arms) from the ACS 2024 1-year person PUMS with the 80
replicate weights, variance = 4/80 * sum((rep - full)^2), 95% CI = est +/- 1.96 * se.

Cost constants and the cost/delta algebra come from the bound lane's compute_bound.py: the
constant block is read out of that file's source text and exec'd, so no number is redefined
here and importing (which would re-run that lane's script) is avoided.

Group quarters in the 2024 1-year person PUMS: there is no TYPEHUGQ column; RELSHIPP 37 =
institutionalized GQ (the API's TYPEHUGQ=2), 38 = noninstitutionalized GQ (TYPEHUGQ=3), and
SERIALNO[4:6] == "HU" marks the household population (TYPEHUGQ=1).

Writes derived/institutional_bound_with_variance.csv and derived/audit.json.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
BOUND = HERE.parent / "institutional_bound_2026_09_17"
ZIP = _data_paths.data_root(require_exists=False) / 'external/acs_pums_2024_1yr/csv_pus.zip'

REPS = [f"PWGTP{i}" for i in range(1, 81)]
WCOLS = ["PWGTP"] + REPS
COLS = ["SERIALNO", "AGEP", "SEX", "NATIVITY", "POBP", "HISP", "RAC1P", "RELSHIPP"] + WCOLS
CHUNK = 400_000
Z = 1.959964

# ---- constants and band/target definitions, exec'd out of the bound lane's source ----
_src = (BOUND / "compute_bound.py").read_text()
_block = _src[_src.index("# ---- cost parameters"):_src.index("# ---- load ACS cells")]
CONST: dict = {}
exec(compile(_block, str(BOUND / "compute_bound.py"), "exec"), CONST)  # noqa: S102
PRISON = CONST["PRISON"]
NF_PUBLIC = CONST["NF_PUBLIC"]
BANDS = CONST["BANDS"]
OLD = CONST["OLD"]
REFS = CONST["REFS"]
ARMS = ("adverse", "moderate")

# bound-lane group name -> this lane's PUMS predicate name (brief naming)
GROUPS = {
    "mexico_born": lambda d: d["POBP"].eq(303),
    "usborn_mexican": lambda d: d["NATIVITY"].eq(1) & d["HISP"].eq(2),
    "native_nh_white": lambda d: d["NATIVITY"].eq(1) & d["HISP"].eq(1) & d["RAC1P"].eq(1),
    "all_natives": lambda d: d["NATIVITY"].eq(1),
}
BRIEF_NAME = {"mexico_born": "mexico_born", "usborn_mexican": "usborn_mexican_selfid",
              "native_nh_white": "native_nh_white", "all_natives": "all_natives"}
TARGETS = ["mexico_born", "usborn_mexican", "mexican_total"]
BAND_BINS = [-1, 17, 24, 34, 44, 54, 64, 74, 10**9]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def tabulate() -> tuple[dict, dict, dict, dict]:
    """-> N, I, IM as {(group, band): np.array(81)} plus meta counts."""
    N: dict = {(g, b): np.zeros(81, dtype=np.int64) for g in GROUPS for b in BANDS}
    I: dict = {k: np.zeros(81, dtype=np.int64) for k in N}
    IM: dict = {k: np.zeros(81, dtype=np.int64) for k in N}
    meta = {"records": 0, "hu_records": 0, "gq_inst_records": 0, "gq_noninst_records": 0,
            "serialno_relshipp_disagreements": 0,
            "gate_usborn_mex_male_18_39_institutional": 0, "parts": []}
    dtypes = {c: np.int32 for c in WCOLS}
    dtypes.update({c: np.int32 for c in ["AGEP", "SEX", "NATIVITY", "POBP", "HISP", "RAC1P", "RELSHIPP"]})
    dtypes["SERIALNO"] = str

    with zipfile.ZipFile(ZIP) as z:
        members = sorted(n for n in z.namelist() if n.lower().endswith(".csv"))
        if not members:
            raise SystemExit(f"[BLOCKED] no csv members in {ZIP}")
        for name in members:
            meta["parts"].append(name)
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                for ci, d in enumerate(pd.read_csv(fh, usecols=COLS, dtype=dtypes, chunksize=CHUNK)):
                    meta["records"] += len(d)
                    hu = d["SERIALNO"].str.slice(4, 6).eq("HU").to_numpy()
                    inst = d["RELSHIPP"].eq(37).to_numpy()
                    noninst = d["RELSHIPP"].eq(38).to_numpy()
                    meta["hu_records"] += int(hu.sum())
                    meta["gq_inst_records"] += int(inst.sum())
                    meta["gq_noninst_records"] += int(noninst.sum())
                    meta["serialno_relshipp_disagreements"] += int((hu & (inst | noninst)).sum()
                                                                   + (~hu & ~(inst | noninst)).sum())
                    male = d["SEX"].eq(1).to_numpy()
                    band = pd.cut(d["AGEP"], bins=BAND_BINS, labels=BANDS).to_numpy()
                    W = d[WCOLS].to_numpy(dtype=np.int64)

                    gate = (d["NATIVITY"].eq(1) & d["HISP"].eq(2)).to_numpy() & male & inst \
                        & d["AGEP"].between(18, 39).to_numpy()
                    meta["gate_usborn_mex_male_18_39_institutional"] += int(W[gate, 0].sum())

                    for g, fn in GROUPS.items():
                        gm = fn(d).to_numpy()
                        if not gm.any():
                            continue
                        Wg, bg, ig, mg = W[gm], band[gm], inst[gm], male[gm]
                        for b in BANDS:
                            bm = bg == b
                            if not bm.any():
                                continue
                            N[(g, b)] += Wg[bm].sum(axis=0)
                            im = bm & ig
                            if im.any():
                                I[(g, b)] += Wg[im].sum(axis=0)
                                imm = im & mg
                                if imm.any():
                                    IM[(g, b)] += Wg[imm].sum(axis=0)
                    print(f"  chunk {ci}: {len(d):,} rows (cum {meta['records']:,})", flush=True)
    return N, I, IM, meta


def gate1(N, I, IM) -> dict:
    """Full-weight N/I/IM per group x band vs the API-based cells of the bound lane."""
    aN: dict = {}
    aI: dict = {}
    aIM: dict = {}
    for r in csv.DictReader(open(BOUND / "derived/acs_cells.csv")):
        g, b, w = r["group"], r["band"], float(r["weighted"])
        aN[(g, b)] = aN.get((g, b), 0.0) + w
        if r["typehugq"] == "2":
            aI[(g, b)] = aI.get((g, b), 0.0) + w
            if r["sex"] == "1":
                aIM[(g, b)] = aIM.get((g, b), 0.0) + w
    diffs = []
    for g in GROUPS:
        for b in BANDS:
            for label, mine, api in (("N", N[(g, b)][0], aN[(g, b)]),
                                     ("I", I[(g, b)][0], aI.get((g, b), 0.0)),
                                     ("IM", IM[(g, b)][0], aIM.get((g, b), 0.0))):
                if float(mine) != api:
                    diffs.append({"group": g, "band": b, "quantity": label,
                                  "pums": float(mine), "api": api, "diff": float(mine) - api})
    return {"cells_compared": len(GROUPS) * len(BANDS) * 3, "mismatches": diffs,
            "pass": not diffs}


def quantities(N, I, IM, k: int, S: dict) -> dict:
    """All bound quantities for weight column k. Mirrors compute_bound.py's algebra."""
    n = {(g, b): float(N[(g, b)][k]) for g in GROUPS for b in BANDS}
    i = {(g, b): float(I[(g, b)][k]) for g in GROUPS for b in BANDS}
    im = {(g, b): float(IM[(g, b)][k]) for g in GROUPS for b in BANDS}
    for b in BANDS:
        n[("mexican_total", b)] = n[("mexico_born", b)] + n[("usborn_mexican", b)]
        i[("mexican_total", b)] = i[("mexico_born", b)] + i[("usborn_mexican", b)]
        im[("mexican_total", b)] = im[("mexico_born", b)] + im[("usborn_mexican", b)]

    def cost(g, b, arm):
        if b in OLD:
            return NF_PUBLIC
        if arm == "adverse":
            return PRISON
        return PRISON * (im[(g, b)] / i[(g, b)] if i[(g, b)] else 0.0)

    def C(g, b, arm):
        return i[(g, b)] * cost(g, b, arm)

    out = {}
    for arm in ARMS:
        for g in TARGETS:
            pop_g = sum(n[(g, b)] for b in BANDS)
            cost_g = sum(C(g, b, arm) for b in BANDS)
            out[(arm, g, "", "target_population")] = pop_g
            out[(arm, g, "", "target_institutional_cost_bn")] = cost_g / 1e9
            out[(arm, g, "", "target_institutional_cost_per_person")] = cost_g / pop_g
            for r in REFS:
                d_gap = -sum(C(g, b, arm) - (n[(g, b)] / n[(r, b)]) * C(r, b, arm) for b in BANDS)
                d_std = -sum(S[b] * (C(g, b, arm) / n[(g, b)] - C(r, b, arm) / n[(r, b)]) for b in BANDS)
                out[(arm, g, r, "delta_age_matched_gap_bn")] = d_gap / 1e9
                out[(arm, g, r, "delta_age_matched_gap_per_target_person")] = d_gap / pop_g
                out[(arm, g, r, "delta_standardized_per_person")] = d_std
    return out


def main() -> None:
    OUT.mkdir(exist_ok=True)
    N, I, IM, meta = tabulate()

    g1 = gate1(N, I, IM)
    g1["gate_male_18_39_usborn_mexican_institutional"] = meta["gate_usborn_mex_male_18_39_institutional"]
    g1["gate_male_18_39_expected"] = 107917
    g1["gate_male_18_39_pass"] = meta["gate_usborn_mex_male_18_39_institutional"] == 107917
    print(f"[gate1] cells pass={g1['pass']} mismatches={len(g1['mismatches'])} "
          f"male18_39={g1['gate_male_18_39_usborn_mexican_institutional']} "
          f"(pass={g1['gate_male_18_39_pass']})", flush=True)
    for m in g1["mismatches"][:20]:
        print("   mismatch:", m, flush=True)

    # age standard: native NH white full-weight ACS age shares (fixed across replicates)
    white_tot = sum(float(N[("native_nh_white", b)][0]) for b in BANDS)
    S = {b: float(N[("native_nh_white", b)][0]) / white_tot for b in BANDS}

    full = quantities(N, I, IM, 0, S)
    reps = [quantities(N, I, IM, k, S) for k in range(1, 81)]

    # ---- gate 2: full-weight deltas reproduce the bound lane's CSV ----
    stored = {}
    for r in csv.DictReader(open(BOUND / "derived/institutional_bound.csv")):
        if r["arm"] in ARMS:
            stored[(r["arm"], r["target"], r["reference"])] = r
    g2 = {"tolerance_bn": 0.01, "mismatches": [], "compared": 0}
    for (arm, g, ref), row in stored.items():
        for q, tol in (("delta_age_matched_gap_bn", 0.01),
                       ("target_institutional_cost_bn", 0.01),
                       ("delta_age_matched_gap_per_target_person", 0.05),
                       ("delta_standardized_per_person", 0.05)):
            mine = full[(arm, g, ref, q)] if q.startswith("delta") else full[(arm, g, "", q)]
            g2["compared"] += 1
            if abs(mine - float(row[q])) > tol:
                g2["mismatches"].append({"arm": arm, "target": g, "reference": ref, "quantity": q,
                                         "recomputed": mine, "stored": float(row[q]),
                                         "diff": mine - float(row[q]), "tolerance": tol})
    g2["pass"] = not g2["mismatches"]
    print(f"[gate2] compared={g2['compared']} pass={g2['pass']} mismatches={len(g2['mismatches'])}", flush=True)
    for m in g2["mismatches"][:20]:
        print("   mismatch:", m, flush=True)

    # ---- SDR variance ----
    rows = []
    for key in full:
        arm, g, ref, q = key
        est = full[key]
        v = 4.0 / 80.0 * sum((r[key] - est) ** 2 for r in reps)
        se = v ** 0.5
        rows.append(dict(arm=arm, target=BRIEF_NAME.get(g, g), reference=BRIEF_NAME.get(ref, ref),
                         quantity=q, estimate=round(est, 4), se=round(se, 4),
                         ci95_low=round(est - Z * se, 4), ci95_high=round(est + Z * se, 4),
                         cv_pct=round(100 * se / abs(est), 3) if est else None,
                         excludes_zero=bool((est - Z * se) * (est + Z * se) > 0)))
    rows.sort(key=lambda r: (r["arm"], r["target"], r["reference"], r["quantity"]))
    with open(OUT / "institutional_bound_with_variance.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # stored CPS gaps for the headline-sign question
    stored_gaps = json.load(open(BOUND / "derived/audit.json"))[
        "stored_cps_gaps_all_age_shared_mexican_observed_total"]
    sign = {}
    for arm in ARMS:
        for ref, gapkey in (("native_nh_white", "gap_total_vs_third_plus_nh_white_bn"),
                            ("all_natives", "gap_total_vs_all_native_bn")):
            k = (arm, "mexican_total", ref, "delta_age_matched_gap_bn")
            est, se = full[k], (4.0 / 80.0 * sum((r[k] - full[k]) ** 2 for r in reps)) ** 0.5
            gap = stored_gaps[gapkey]
            sign[f"{arm}|mexican_total|vs_{ref}"] = {
                "stored_gap_bn": gap, "delta_bn": round(est, 3), "delta_se_bn": round(se, 3),
                "gap_plus_delta_bn": round(gap + est, 3),
                "gap_plus_delta_ci95": [round(gap + est - Z * se, 3), round(gap + est + Z * se, 3)],
                "sign_flip_possible_within_ci": bool((gap + est - Z * se) * (gap + est + Z * se) <= 0)}
        k = (arm, "mexican_total", "", "target_institutional_cost_bn")
        est, se = full[k], (4.0 / 80.0 * sum((r[k] - full[k]) ** 2 for r in reps)) ** 0.5
        abs_tot = stored_gaps["absolute_total_bn"]
        sign[f"{arm}|absolute_balance"] = {
            "stored_absolute_bn": abs_tot, "cost_bn": round(est, 3), "cost_se_bn": round(se, 3),
            "balance_minus_cost_bn": round(abs_tot - est, 3),
            "balance_minus_cost_ci95": [round(abs_tot - est - Z * se, 3), round(abs_tot - est + Z * se, 3)],
            "sign_flip_possible_within_ci": bool((abs_tot - est - Z * se) * (abs_tot - est + Z * se) <= 0)}

    audit = {
        "lane": "institutional_variance_2026_09_17",
        "source_zip": str(ZIP), "source_sha256": sha256(ZIP),
        "source_parts": meta["parts"],
        "acs": "ACS 2024 1-year person PUMS, 80 replicate weights, SDR variance 4/80 * sum((rep-full)^2)",
        "records_read": meta["records"], "household_records": meta["hu_records"],
        "gq_institutional_records": meta["gq_inst_records"],
        "gq_noninstitutional_records": meta["gq_noninst_records"],
        "serialno_vs_relshipp_disagreements": meta["serialno_relshipp_disagreements"],
        "constants_from": str(BOUND / "compute_bound.py"),
        "constants": {"prison_annual_per_person": PRISON, "nf_public_per_resident_year": NF_PUBLIC},
        "white_age_shares_full_weight": {b: round(S[b], 5) for b in BANDS},
        "gate1_cells_vs_api": g1,
        "gate2_full_weight_vs_institutional_bound_csv": g2,
        "headline_sign_check": sign,
        "stored_cps_gaps": stored_gaps,
        "rows_written": len(rows),
        "note": "Intervals cover ACS sampling error only. Cost parameters (prison/NF unit costs, "
                "public share) and the CPS-side gap estimates carry their own uncertainty, not "
                "propagated here.",
    }
    json.dump(audit, open(OUT / "audit.json", "w"), indent=1)
    print(json.dumps(sign, indent=1))
    print(f"wrote {len(rows)} rows -> {OUT / 'institutional_bound_with_variance.csv'}")


if __name__ == "__main__":
    main()
