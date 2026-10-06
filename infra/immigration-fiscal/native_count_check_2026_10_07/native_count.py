#!/usr/bin/env python3
"""US-born Mexican self-identifiers: CPS ASEC 2025 against the ACS 2024, net of timing and frame.

The identity-enforcement lane (g3_identity_enforcement_2026_10_06, §8) found that the ASEC 2025 final weights give
third-plus Mexican records 5.5% more weight, relative to third-plus non-Hispanics, than the 2022–24 files did, about
0.75M people. The account prices its US-born members at those weights (audit row 4 reweights only the Mexico-born).
This script asks whether the ASEC 2025's US-born Mexican self-ID count sits above the ACS once the two surveys'
reference dates and universes are allowed for.

- ACS: the 2024 one-year person file, household population (GQ excluded), HISP 2 and NATIVITY 1, through the
  population-total lane's cached subset; the 2023 one-year person file for the year's growth.
- CPS: the ASEC 2025 person file (MARSUPWT), PRDTHSP 1 and PRCITSHP 1–3 (born in the US, in a territory, or abroad
  to a US parent).
- Timing: the ASEC refers to March 2025, about 0.75 years after the ACS 2024 midpoint. The US-born group grows at its
  own measured 2023–24 rate, the whole population at its own; the CPS-to-ACS ratio of total population (which also
  holds the universe difference) is carried with the national growth removed.

    expected CPS = ACS_2024 × (CPS total / ACS total) × ((1 + g_group) / (1 + g_all))^0.75

Gates: the CPS and ACS totals match the dataset audit's `derived/cps_vs_acs_origin.csv` (total population 337.69M and
331.72M); every band's count is positive.

Writes derived/summary.json and derived/by_age.csv. From the repository root:
  uv run --no-project python3 infra/immigration-fiscal/native_count_check_2026_10_07/native_count.py
"""
from __future__ import annotations

import csv
import json
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent / "derived"
ACS24 = ROOT / "infra/immigration-fiscal/mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet"
ACS23 = ROOT / "sources/immigration-fiscal/data/census/acs_pums_2023_person.zip"
CPS = ROOT / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
AUDIT = ROOT / "infra/immigration-fiscal/dataset_integrity_2026_09_23/derived/cps_vs_acs_origin.csv"
BANDS, LABELS = [0, 18, 35, 55, 200], ["0-17", "18-34", "35-54", "55+"]
YEARS = 0.75


def gate(name: str, ok: bool, **detail) -> None:
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def main() -> None:
    a = pd.read_parquet(ACS24, columns=["SERIALNO", "PWGTP", "AGEP", "HISP", "NATIVITY"])
    a = a[~a.SERIALNO.str.contains("GQ")]
    with zipfile.ZipFile(CPS) as z:
        c = pd.read_csv(z.open("pppub25.csv"), usecols=["A_AGE", "PRDTHSP", "PRCITSHP", "MARSUPWT"])
    c["w"] = c.MARSUPWT / 100
    nat23 = tot23 = 0.0
    with zipfile.ZipFile(ACS23) as z:
        for f in ("psam_pusa.csv", "psam_pusb.csv"):
            for ch in pd.read_csv(z.open(f), usecols=["SERIALNO", "PWGTP", "HISP", "NATIVITY"], chunksize=500_000,
                                  dtype={"SERIALNO": str}):
                ch = ch[~ch.SERIALNO.str.contains("GQ")]
                tot23 += float(ch.PWGTP.sum())
                nat23 += float(ch.PWGTP[(ch.HISP == 2) & (ch.NATIVITY == 1)].sum())

    audit = {r["origin"]: r for r in csv.DictReader(open(AUDIT))}
    tot_acs, tot_cps = float(a.PWGTP.sum()) / 1e6, float(c.w.sum()) / 1e6
    gate("acs_total_matches_audit", abs(tot_acs - float(audit["Total population"]["acs_household_m"])) < 1e-6)
    gate("cps_total_matches_audit", abs(tot_cps - float(audit["Total population"]["cps_m"])) < 1e-6)

    am = (a.HISP == 2) & (a.NATIVITY == 1)
    cm = (c.PRDTHSP == 1) & c.PRCITSHP.isin([1, 2, 3])
    a["band"] = pd.cut(a.AGEP, BANDS, right=False, labels=LABELS)
    c["band"] = pd.cut(c.A_AGE, BANDS, right=False, labels=LABELS)
    acs_b = a[am].groupby("band", observed=True).PWGTP.sum() / 1e6
    cps_b = c[cm].groupby("band", observed=True).w.sum() / 1e6
    gate("bands_positive", bool((acs_b > 0).all() and (cps_b > 0).all()))

    nat24 = float(acs_b.sum())
    g_group, g_all = nat24 / (nat23 / 1e6) - 1, tot_acs / (tot23 / 1e6) - 1
    frame = tot_cps / tot_acs
    expected = nat24 * frame * ((1 + g_group) / (1 + g_all)) ** YEARS
    cps_nat = float(cps_b.sum())
    out = {
        "lane": "native_count_check_2026_10_07",
        "acs_2024_us_born_mexican_m": nat24,
        "acs_2023_us_born_mexican_m": nat23 / 1e6,
        "growth_us_born_mexican": g_group,
        "growth_household_population": g_all,
        "cps_to_acs_total_ratio": frame,
        "years_between_reference_dates": YEARS,
        "cps_2025_us_born_mexican_m": cps_nat,
        "expected_at_acs_level_m": expected,
        "residual_m": cps_nat - expected,
        "residual_share": cps_nat / expected - 1,
        "raw_excess_over_total_ratio_m": cps_nat - nat24 * frame,
    }
    OUT.mkdir(exist_ok=True)
    (OUT / "summary.json").write_text(json.dumps(out, indent=1) + "\n")
    with open(OUT / "by_age.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["band", "acs_2024_m", "cps_2025_m", "ratio"])
        for b in LABELS:
            w.writerow([b, round(float(acs_b[b]), 6), round(float(cps_b[b]), 6), round(float(cps_b[b] / acs_b[b]), 6)])
    print(f"  ✓ CPS {cps_nat:.3f}M vs expected {expected:.3f}M at the ACS level: residual {cps_nat - expected:+.3f}M "
          f"({cps_nat / expected - 1:+.2%}); growth {g_group:.2%} vs {g_all:.2%}")


if __name__ == "__main__":
    main()
