#!/usr/bin/env python3
"""Van Hook & Bachmeier's Supplemental Table 2.1 beside the CPS ASEC 2025 on the generations the CPS can see.

VHB (Texas-Style Exclusion, Russell Sage 2024, online supplement, Supplemental Table 2.1; transcribed from the page
image, sha256 d99b81e0..., see RESULT.md) report the share of linked Mexican-ancestry adults 20+ who identify as
Mexican and as Hispanic by generation. Their generations come from record linkage; the CPS sees birthplace for the
person and both parents, so G1, G2 (two Mexico-born parents), G2.5 (one Mexico-born parent, the other US-born) and
G2 with one Mexico-born and one other foreign-born parent are measurable for adults here, on the same 20+ age
restriction and the same items (Mexican = PRDTHSP 1, "Mexican, Mexican American, Chicano"; Hispanic = PEHSPNON 1).
G3 and G4 are not separable among adults (no grandparent birthplaces), so the account's third-generation rate p3
(children linked to co-resident parents, mexican_origin_population_total_2026_09_19 arm 3) is printed beside.

Inputs : ../mexican_origin_population_total_2026_09_19/_cache/cps_asec2025_person_subset.parquet (read-only)
         ../mexican_origin_population_total_2026_09_19/derived/arm3_multiplier.csv (p3)
The third-plus (native, both parents US-area born) Hispanics by detailed origin are written beside: "Other Hispanic"
(PRDTHSP 8) caps the stock of third-plus people who identify as Hispanic but not as Mexican, the channel VHB's 82.8%
Hispanic / 51.0% Mexican fourth-plus row implies is large.

Outputs: derived/vhb_table_2_1.csv, derived/cps_benchmark.csv, derived/cps_third_plus_hispanic_detail.csv
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/benchmark.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
POP_DIR = FISCAL / "mexican_origin_population_total_2026_09_19"
PARQUET = POP_DIR / "_cache/cps_asec2025_person_subset.parquet"
MULT = POP_DIR / "derived/arm3_multiplier.csv"

MEXICO = 303
US_AREA = (57, 60, 66, 69, 73, 78)      # bounds_coverage_fiscal.py US_AREA
REP_N = 160

# Supplemental Table 2.1, percent identifying as Mexican / as Hispanic, adults 20+, N = 10,500.
VHB = [("G1", "First", 86.8, 90.7), ("G2", "Second", 83.8, 91.2), ("G2.5", "2.5th", 72.3, 80.0),
       ("G3", "Third", 74.2, 84.6), ("G4+", "Fourth-or-higher", 51.0, 82.8)]


def rate(d: pd.DataFrame, cls: np.ndarray, ident: np.ndarray, reps: list[str]) -> tuple[float, float, int]:
    w = d.loc[cls]
    num, den = float(w.loc[ident[cls], "pwwgt0"].sum()), float(w["pwwgt0"].sum())
    r = num / den
    rr = np.array([w.loc[ident[cls], c].sum() / w[c].sum() for c in reps])
    return r, float(np.sqrt(4.0 / REP_N * np.sum((rr - r) ** 2))), int(cls.sum())


def main() -> None:
    OUT.mkdir(exist_ok=True)
    reps = [f"pwwgt{i}" for i in range(1, REP_N + 1)]
    cols = ["A_AGE", "PEHSPNON", "PRDTHSP", "PENATVTY", "PEMNTVTY", "PEFNTVTY", "PRCITSHP", "pwwgt0", *reps]
    d = pd.read_parquet(PARQUET, columns=cols)
    adult = (d.A_AGE >= 20).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    mex_born = (d.PENATVTY == MEXICO).to_numpy()
    mom_mex, dad_mex = (d.PEMNTVTY == MEXICO).to_numpy(), (d.PEFNTVTY == MEXICO).to_numpy()
    mom_us, dad_us = d.PEMNTVTY.isin(US_AREA).to_numpy(), d.PEFNTVTY.isin(US_AREA).to_numpy()
    hisp = (d.PEHSPNON == 1).to_numpy()
    mex_id = hisp & (d.PRDTHSP == 1).to_numpy()
    classes = {
        "G1 (Mexico-born, any citizenship)": mex_born,
        "G1 (Mexico-born, foreign-born)": mex_born & d.PRCITSHP.isin([4, 5]).to_numpy(),
        "G2 (two Mexico-born parents)": native & mom_mex & dad_mex,
        "G2.5 (one Mexico-born parent, the other US-born)": native & ((mom_mex & dad_us) | (dad_mex & mom_us)),
        "G2 (one Mexico-born parent, the other born abroad elsewhere)":
            native & ((mom_mex & ~dad_mex & ~dad_us) | (dad_mex & ~mom_mex & ~mom_us)),
        "G2 (both parents born abroad, at least one in Mexico: VHB's second)":
            native & (mom_mex | dad_mex) & ~mom_us & ~dad_us,
        "G2 (any Mexico-born parent: the account's G2)": native & (mom_mex | dad_mex),
    }
    rows = []
    for age_label, age in (("20+", adult), ("all ages", np.ones(len(d), bool))):
        for label, cls in classes.items():
            m, m_se, n = rate(d, cls & age, mex_id, reps)
            h, h_se, _ = rate(d, cls & age, hisp, reps)
            rows.append({"ages": age_label, "generation": label, "unweighted_n": n,
                         "id_mexican": f"{m:.6f}", "id_mexican_se": f"{m_se:.6f}",
                         "id_hispanic": f"{h:.6f}", "id_hispanic_se": f"{h_se:.6f}"})
    with MULT.open(newline="") as f:
        q = {r["quantity"]: r["children"] for r in csv.DictReader(f)}
    ab = float(q["A and B: 3rd-generation identifiers"])
    p3 = ab / (ab + float(q["B not A: 3rd-generation attriters (recoverable)"]))
    rows.append({"ages": "children (co-resident parents)", "generation": "G3 (account p3, arm 3)", "unweighted_n": "",
                 "id_mexican": f"{p3:.6f}", "id_mexican_se": "", "id_hispanic": "", "id_hispanic_se": ""})
    with (OUT / "cps_benchmark.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    labels = {1: "Mexican", 2: "Puerto Rican", 3: "Cuban", 4: "Dominican", 5: "Salvadoran",
              6: "Central American (exc. Salvadoran)", 7: "South American", 8: "Other Hispanic"}  # 2025 ASEC dictionary
    t3 = native & mom_us & dad_us & hisp
    with (OUT / "cps_third_plus_hispanic_detail.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["ages", "prdthsp", "origin", "persons", "unweighted_n"])
        for age_label, age in (("20+", adult), ("all ages", np.ones(len(d), bool))):
            for code, lab in labels.items():
                m = t3 & age & (d.PRDTHSP == code).to_numpy()
                w.writerow([age_label, code, lab, f"{float(d.loc[m, 'pwwgt0'].sum()):.1f}", int(m.sum())])
    with (OUT / "vhb_table_2_1.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["generation", "vhb_label", "pct_id_mexican", "pct_id_hispanic", "source"])
        for g, lab, m, h in VHB:
            w.writerow([g, lab, m, h, "Van Hook & Bachmeier 2024 online supplement, Supplemental Table 2.1 "
                        "(IGENS-20 linked files, adults 20+, N = 10,500)"])
    for r in rows:
        print(f"  {r['ages']:<14} {r['generation']:<62} n {r['unweighted_n']!s:>5}  Mexican {float(r['id_mexican']):.4f}"
              + (f"  Hispanic {float(r['id_hispanic']):.4f}" if r["id_hispanic"] else ""))


if __name__ == "__main__":
    main()
