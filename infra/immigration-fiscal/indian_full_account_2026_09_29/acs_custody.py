"""Institutionalization in the ACS 2023 1-year PUMS by origin group: the offending proxy for groups with no
offending data of their own (Indian-origin), with the Mexican-origin union, NH Black and NH white beside it for
calibration against the measured custody shares the Black and white lanes use.

Institutional = RELSHIPP 37 (institutionalized group quarters: prisons, jails, detention, nursing homes and other
long-term care). Ages 18-64 hold almost all of the correctional part; the 65+ part is mostly nursing homes.
Groups (the ACS has no parent birthplace, so the second generation is proxied by race or ethnicity):
  india_born           POBP 210
  asian_indian_usborn  NATIVITY 1 and RAC2P = Asian Indian alone (the code is read off the data: RAC2P mode of the
                       India-born, checked against the data dictionary's 'Asian Indian alone')
  indian_origin        the two together (G3+ Asian Indians are in it too: the ACS cannot separate them)
  mexico_born          POBP 303
  mexican_usborn       NATIVITY 1 and HISP 2 (Mexican)
  union_proxy          the two together (the union's ACS proxy, as institutional_bound_2026_09_17 uses)
  nh_black             HISP 1 and RAC1P 2;  nh_white HISP 1 and RAC1P 1;  nh_white_usborn  and NATIVITY 1
  all
Rates and SEs by successive difference replication over PWGTP1-80 (SE = sqrt(4/80 sum (r_k - r)^2)).
Outputs: derived/acs_institutional_cells.csv (group x five-year band x institutional: persons, main weight),
derived/acs_institutional.csv (per group: population, institutional 18-64, the rate per member and 18-64, its SE,
and the ratio to all residents' rate per member with its SE).
Run from the repository root (about 3 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/acs_custody.py
"""
from __future__ import annotations

import csv
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
DER = LANE / "derived"
ZIP = Path.home() / "research-data/immigration-fiscal/data/census/acs_pums_2023_person.zip"
REP = [f"PWGTP{i}" for i in range(1, 81)]
COLS = ["PWGTP", "AGEP", "RELSHIPP", "POBP", "NATIVITY", "RAC1P", "RAC2P", "HISP"] + REP
BANDS = list(range(0, 80, 5)) + [80]
INDIA, MEXICO = 210, 303


def load():
    if not ZIP.exists():
        raise SystemExit(f"[BLOCKED] missing ACS PUMS person file: {ZIP}")
    parts = []
    with zipfile.ZipFile(ZIP) as z:
        for name in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(name) as f:
                parts.append(pd.read_csv(f, usecols=COLS, dtype={c: "int32" for c in COLS}))
    return pd.concat(parts, ignore_index=True)


def main():
    d = load()
    india = d.POBP.eq(INDIA)
    code = int(d.loc[india, "RAC2P"].mode().iloc[0])
    share = float(d.loc[india & d.RAC2P.eq(code), "PWGTP"].sum() / d.loc[india, "PWGTP"].sum())
    if share < 0.8:
        raise SystemExit(f"[BLOCKED] RAC2P {code} holds only {share:.3f} of the India-born: not the Asian Indian code")
    print(f"RAC2P Asian Indian alone = {code}: {share:.4f} of India-born persons (weighted)")
    native = d.NATIVITY.eq(1)
    nhisp = d.HISP.eq(1)
    groups = {
        "india_born": india,
        "asian_indian_usborn": native & d.RAC2P.eq(code),
        "mexico_born": d.POBP.eq(MEXICO),
        "mexican_usborn": native & d.HISP.eq(2),
        "nh_black": nhisp & d.RAC1P.eq(2),
        "nh_white": nhisp & d.RAC1P.eq(1),
        "nh_white_usborn": nhisp & d.RAC1P.eq(1) & native,
        "all": pd.Series(True, index=d.index),
    }
    groups["indian_origin"] = groups["india_born"] | groups["asian_indian_usborn"]
    groups["union_proxy"] = groups["mexico_born"] | groups["mexican_usborn"]
    inst = d.RELSHIPP.eq(37).to_numpy()
    band = np.minimum(d.AGEP.to_numpy() // 5 * 5, 80)
    adult = ((d.AGEP >= 18) & (d.AGEP <= 64)).to_numpy()
    W = d[["PWGTP"] + REP].to_numpy(np.float64)
    cells, rows, reps = [], [], {}
    for g, m in groups.items():
        m = m.to_numpy()
        pop = W[m].sum(axis=0)
        pop1864 = W[m & adult].sum(axis=0)
        i1864 = W[m & adult & inst].sum(axis=0)
        reps[g] = dict(pop=pop, pop1864=pop1864, i1864=i1864, per_member=i1864 / pop, rate1864=i1864 / pop1864)
        for b in BANDS:
            for flag in (0, 1):
                sel = m & (band == b) & (inst == bool(flag))
                cells.append({"group": g, "band": b, "institutional": flag, "persons": int(sel.sum()),
                              "weighted": f"{W[sel, 0].sum():.0f}"})
    sdr = lambda x: float(np.sqrt(4 / 80 * ((x[1:] - x[0]) ** 2).sum()))  # noqa: E731
    for g, r in reps.items():
        rel = r["per_member"] / reps["all"]["per_member"]
        rel_u = r["per_member"] / reps["union_proxy"]["per_member"]
        m = groups[g].to_numpy()
        rows.append({"group": g, "sample_persons": int(m.sum()), "sample_institutional_18_64": int((m & adult & inst).sum()),
                     "population": f"{r['pop'][0]:.0f}", "population_18_64": f"{r['pop1864'][0]:.0f}",
                     "institutional_18_64": f"{r['i1864'][0]:.0f}",
                     "rate_18_64": f"{r['rate1864'][0]:.6f}", "rate_18_64_se": f"{sdr(r['rate1864']):.6f}",
                     "per_member": f"{r['per_member'][0]:.6f}", "per_member_se": f"{sdr(r['per_member']):.6f}",
                     "per_member_over_all": f"{rel[0]:.6f}", "per_member_over_all_se": f"{sdr(rel):.6f}",
                     "per_member_over_union_proxy": f"{rel_u[0]:.6f}", "per_member_over_union_proxy_se": f"{sdr(rel_u):.6f}",
                     "rac2p_asian_indian_code": code})
    DER.mkdir(exist_ok=True)
    for name, data in (("acs_institutional_cells.csv", cells), ("acs_institutional.csv", rows)):
        with open(DER / name, "w", newline="") as f:
            wr = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator="\n")
            wr.writeheader()
            wr.writerows(data)
    print(pd.DataFrame(rows)[["group", "sample_persons", "sample_institutional_18_64", "population", "rate_18_64",
                              "rate_18_64_se", "per_member_over_all", "per_member_over_all_se",
                              "per_member_over_union_proxy"]].to_string(index=False))


if __name__ == "__main__":
    main()
