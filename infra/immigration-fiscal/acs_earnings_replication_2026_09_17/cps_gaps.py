#!/usr/bin/env python3
"""CPS ASEC 2025 (income year 2024) earnings/income gaps, ledger group definitions.

Builds the CPS state exactly as the all-age ledger's analyze.py does (imports the
held extend_ledger builder), then computes wage and total personal income means
and common-age per-person gaps with the 160 replicate weights.

Writes derived/cps_gaps.csv and derived/cps_audit.json. Reads nothing outside the
held CPS zip; writes nothing outside this lane.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))
sys.path.insert(0, str(FISCAL / "build"))

import extend_ledger as ext  # noqa: E402

# PTOTVAL (total personal income) is not in the base generator's column list.
# prepare() consumes base.PERSON as usecols at call time, so appending here is
# enough; nothing on disk is modified.
for _f in ["PTOTVAL"]:
    if _f not in ext.base.PERSON:
        ext.base.PERSON.append(_f)

import common as C  # noqa: E402

CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
LEDGER_ESTIMATES = FISCAL / "all_age_ledger_2026_09_17/derived/estimates.csv"
OUT = HERE / "derived"

# ACS/CPS geographic codes
CA, TX = 6, 48


def build_groups(d: pd.DataFrame, ledger_group: dict) -> dict[str, np.ndarray]:
    """Ledger groups plus the ACS-aligned CPS pools, all on the civilian domain."""
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    g = {}
    # (i), (iii), (v): held ledger definitions
    for name in ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
                 "third_plus_nh_white", "all_native"]:
        g[name] = ledger_group[name] & civilian
    # (ii) ACS-aligned pool: CPS-native, Mexican detailed-Hispanic self-ID,
    # regardless of parent birthplace. PRDTHSP == 1 is "Mexican" in the CPS
    # detailed Hispanic-origin recode; the ledger uses the same code for its
    # third-plus self-ID group (extend_ledger.py:237).
    g["usborn_mexican_selfid"] = native & d.PRDTHSP.eq(1).to_numpy() & civilian
    # (iv) ACS-aligned reference: ALL CPS natives who are non-Hispanic white
    # (no two-US-born-parents restriction). PEHSPNON == 2 is non-Hispanic;
    # PRDTRACE == 1 is white alone.
    g["native_nh_white"] = (native & d.PEHSPNON.eq(2).to_numpy()
                            & d.PRDTRACE.eq(1).to_numpy() & civilian)
    return g


def gate1(groups, weights, d):
    """CPS civilian household populations must match the held ledger to 1 person."""
    est = pd.read_csv(LEDGER_ESTIMATES)
    est = est[est.scenario.eq("all_age_shared") & est.metric.eq("absolute_total")]
    checks = {}
    for name in ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]:
        row = est[est.target.eq(name)]
        if len(row) != 1:
            raise SystemExit(f"[BLOCKED] ledger population row missing/duplicate: {name}")
        held = float(row.population.iloc[0])
        mine = float(weights[groups[name], 0].sum())
        checks[name] = {"ledger": held, "lane": mine, "difference": mine - held}
        if abs(mine - held) > 1.0:
            raise SystemExit(f"[BLOCKED] Gate 1 failed for {name}: {mine} vs {held}")
    return checks


def table(groups, band, weights, values, refs, domain, denom=160):
    rows = []
    cells = {n: C.cell_totals(m, band, weights, values) for n, m in groups.items()}
    shares = {}
    for ref in refs:
        n0 = cells[ref]["n"][:, 0]
        shares[ref] = n0 / n0.sum()
    for name, cell in cells.items():
        for b in range(C.NBANDS):
            row = dict(survey="CPS", domain=domain, group=name, band=C.BAND_LABELS[b])
            pop, pop_se = C.sdr(cell["n"][b], denom)
            row.update(population=pop, population_se=pop_se)
            for key in values:
                m = C.safe_div(cell[key], cell["n"])[b]
                e, s = C.sdr(m, denom)
                row[f"mean_{key}"] = e
                row[f"mean_{key}_se"] = s
            rows.append(row)
        # all-age crude
        row = dict(survey="CPS", domain=domain, group=name, band="all")
        pop, pop_se = C.sdr(cell["n"].sum(axis=0), denom)
        row.update(population=pop, population_se=pop_se)
        for key in values:
            e, s = C.sdr(C.crude_mean(cell, key), denom)
            row[f"mean_{key}"] = e
            row[f"mean_{key}_se"] = s
        rows.append(row)
    gaps = []
    for ref in refs:
        for name, cell in cells.items():
            if name == ref:
                continue
            for key in values:
                v = C.common_age_gap(cell, cells[ref], key, shares[ref])
                e, s = C.sdr(v, denom)
                a = C.age_matched_total_gap(cell, cells[ref], key)
                ae, ase = C.sdr(a, denom)
                gaps.append(dict(survey="CPS", domain=domain, group=name, reference=ref,
                                 variable=key,
                                 common_age_gap_per_person=e, common_age_gap_se=s,
                                 common_age_ci_low=e - 1.96 * s, common_age_ci_high=e + 1.96 * s,
                                 age_matched_gap_bn=ae / 1e9, age_matched_gap_bn_se=ase / 1e9))
    return rows, gaps


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--cps-zip", type=Path, default=CPS_ZIP)
    args = ap.parse_args()
    if not args.cps_zip.exists():
        raise SystemExit(f"[BLOCKED] CPS zip not found: {args.cps_zip}")
    OUT.mkdir(parents=True, exist_ok=True)

    state = ext.build(argparse.Namespace(cps_zip=args.cps_zip))
    d = state["d"]
    weights = state["person_weights"]          # (n, 161), column 0 is the full weight
    groups = build_groups(d, state["group"])
    checks = gate1(groups, weights, d)
    print("[gate1] populations match the held ledger to <1 person", flush=True)

    band = C.bands_of(d.A_AGE.to_numpy())
    values = {"WSAL_VAL": d.WSAL_VAL.to_numpy(dtype=float),
              "PTOTVAL": d.PTOTVAL.to_numpy(dtype=float)}
    refs = ["native_nh_white", "third_plus_nh_white"]

    rows, gaps = table(groups, band, weights, values, refs, "national")
    fips = d.GESTFIPS.to_numpy()
    for code, label in [(CA, "CA"), (TX, "TX")]:
        sub = {n: m & (fips == code) for n, m in groups.items()}
        r2, g2 = table(sub, band, weights, values, refs, label)
        rows += r2
        gaps += g2

    pd.DataFrame(rows).to_csv(OUT / "cps_cells.csv", index=False)
    pd.DataFrame(gaps).to_csv(OUT / "cps_gaps.csv", index=False)

    # employment rate 16+ for comparability with the ACS side (ESR analogue:
    # CPS ASEC has no ESR here; use positive annual earnings as the recorded
    # analogue and label it as such).
    emp = {}
    age = d.A_AGE.to_numpy()
    for name, m in groups.items():
        sel = m & (age >= 16)
        w = weights[sel]
        e = (d.PEARNVAL.to_numpy()[sel] > 0).astype(float)
        num = e @ w
        den = w.sum(axis=0)
        est, se = C.sdr(num / den, 160)
        emp[name] = {"any_earnings_rate_16plus": est, "se": se}

    audit = {
        "cps_zip": str(args.cps_zip),
        "cps_sha256": ext.base.sha(args.cps_zip),
        "person_rows": int(len(d)),
        "replicate_weights": 160,
        "variance": "4/160 * sum((rep - full)^2)",
        "gate1_population_check": checks,
        "group_definitions": {
            "mexico_born": "PRCITSHP in {4,5} & PENATVTY==303 (ledger)",
            "mexican_second_gen": "PRCITSHP in {1,2,3} & (PEFNTVTY==303 | PEMNTVTY==303) (ledger)",
            "mexican_third_plus_selfid": "native & both parents US-area & PRDTHSP==1 (ledger)",
            "usborn_mexican_selfid": "native & PRDTHSP==1 (ACS-aligned; parent birthplace ignored)",
            "native_nh_white": "native & PEHSPNON==2 & PRDTRACE==1 (ACS-aligned reference)",
            "third_plus_nh_white": "native & both parents US-area & PEHSPNON==2 & PRDTRACE==1 (ledger reference)",
        },
        "domain": "civilian household population: PRPERTYP==2 | A_AGE<15",
        "employment_analogue_16plus": emp,
    }
    (OUT / "cps_audit.json").write_text(json.dumps(audit, indent=2))
    print(f"[done] wrote {OUT/'cps_gaps.csv'} and {OUT/'cps_cells.csv'}", flush=True)


if __name__ == "__main__":
    main()
