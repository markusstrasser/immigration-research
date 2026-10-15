"""SCF outside composition checks; no income-tax estimate is observed here.

uv run --no-project python3 infra/immigration-fiscal/top_income_share_2026_10_15/outside_checks.py
Raw 2019 acquisition (10.1 MB) is documented in derived/outside_sources.csv.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import resource
import time

import numpy as np
import pandas as pd
import pyreadstat

LANE = Path(__file__).resolve().parent
ROOT = LANE.parents[2]
CACHE = LANE / "_cache/outside"
CPI = ROOT / "infra/immigration-fiscal/consumption_key_2026_09_24/_cache/sources/bls_cpi_u_2015_2024.json"
RAW = {
    2019: CACHE / "scf2019/p19i6.dta",
    2022: ROOT / "sources/immigration-fiscal/data/external/stage3/frb/scf2022/p22i6.dta",
}
BINS = [(0, 50_000, "under50k"), (50_000, 75_000, "50k_75k"),
        (75_000, 100_000, "75k_100k"), (100_000, 200_000, "100k_200k"),
        (200_000, 500_000, "200k_500k"), (500_000, 1_000_000, "500k_1m"),
        (1_000_000, float("inf"), "1m_plus"),
        (1_000_000, 1_500_000, "1m_1p5m"), (1_500_000, 2_000_000, "1p5m_2m"),
        (2_000_000, 5_000_000, "2m_5m"), (5_000_000, float("inf"), "5m_plus"),
        (200_000, float("inf"), "200k_plus")]
PAYMENTS = [(6464, 6465), (6469, 6470), (6474, 6475), (6479, 6480),
            (6965, 6966), (6971, 6972), (6977, 6978), (6983, 6984)]
COLS = ["y1", "yy1", "x42001", "x5729", "x6809", "x6810", "x7004",
        "x6558", "x6566", "x6574"] + [f"x{x}" for pair in PAYMENTS for x in pair]


def cpi_annual(path: Path = CPI) -> dict[int, float]:
    """Read authoritative BLS series, rejecting missing annual-average observations."""
    data = json.loads(path.read_text())
    series = data["Results"]["series"]
    found = [s for s in series if s["seriesID"] == "CUUR0000SA0"]
    if len(found) != 1:
        raise ValueError("[BLOCKED] exact BLS CPI-U series missing")
    result = {int(r["year"]): float(r["value"]) for r in found[0]["data"] if r["period"] == "M13"}
    if not {2018, 2021, 2023} <= result.keys():
        raise ValueError("[BLOCKED] SCF income-year CPI-U annual average missing")
    return result


def monthly_factor(freq: pd.Series) -> np.ndarray:
    """Literal Federal Reserve MCONV macro, including zero for unsupported codes."""
    mapping = {2: 52 / 12, 3: 26 / 12, 4: 1, 5: 1 / 3, 6: 1 / 12,
               11: 1 / 6, 12: 1 / 2, 31: 2, 23: 13 / 12, 24: 52 / (6 * 12)}
    return freq.map(mapping).fillna(0).to_numpy(float)


def gross_income(d: pd.DataFrame) -> np.ndarray:
    """Fed INCOME before its price transformations; previous-calendar-year dollars."""
    pension = sum(d[f"x{x}"].to_numpy(float) for x in [6558, 6566, 6574])
    for amount, freq in PAYMENTS:
        pension += np.maximum(0, d[f"x{amount}"].to_numpy(float) * monthly_factor(d[f"x{freq}"]) * 12)
    return np.maximum(0, d.x5729.to_numpy(float)) + pension


def validate_implicates(d: pd.DataFrame) -> None:
    if not d.y1.is_unique or not (d.x42001 > 0).all():
        raise ValueError("[BLOCKED] duplicate implicate ID or nonpositive SCF weight")
    if not (d.y1.astype(int) // 10 == d.yy1.astype(int)).all():
        raise ValueError("[BLOCKED] SCF household ID mapping changed")
    groups = d.groupby("yy1").y1.apply(lambda s: set(s.astype(int) % 10))
    if not groups.map(lambda s: s == {1, 2, 3, 4, 5}).all():
        raise ValueError("[BLOCKED] each family must have all five implicates")


def summarize(d: pd.DataFrame, year: int, prices: dict[int, float]) -> tuple[list[dict], list[dict]]:
    validate_implicates(d)
    d = d.copy()
    d["income2023"] = gross_income(d) * prices[2023] / prices[year - 1]
    d["implicate"] = d.y1.astype(int) % 10
    definitions = {
        "hispanic_any_race": (d.x7004 == 1) | (d.x6809 == 3),
        "fed_racecl4_hispanic": (d.x6809 == 3) & (d.x6810 == 5),
    }
    detailed, averaged = [], []
    for definition, hispanic in definitions.items():
        for lower, upper, label in BINS:
            selected = (d.income2023 >= lower) & (d.income2023 < upper)
            rows = []
            for imp in range(1, 6):
                mask = selected & (d.implicate == imp)
                w = d.loc[mask, "x42001"].to_numpy(float)
                inc = d.loc[mask, "income2023"].to_numpy(float)
                h = hispanic[mask].to_numpy(bool)
                den = float(w.sum())
                income = float((w * inc).sum())
                row = dict(scf_year=year, income_year=year - 1, hispanic_definition=definition,
                           bin=label, lower_real2023=lower, upper_real2023="" if np.isinf(upper) else upper,
                           implicate=imp, families_weighted=den, hispanic_families_weighted=float(w[h].sum()),
                           income_weighted=income, hispanic_income_weighted=float((w[h] * inc[h]).sum()),
                           family_share=float(w[h].sum() / den) if den else None,
                           income_share=float((w[h] * inc[h]).sum() / income) if income else None,
                           sample_families=int(mask.sum()), sample_hispanic_families=int(h.sum()),
                           kish_n=float(den ** 2 / (w ** 2).sum()) if den else 0)
                rows.append(row)
                detailed.append(row)
            avg = {k: rows[0][k] for k in ["scf_year", "income_year", "hispanic_definition", "bin", "lower_real2023", "upper_real2023"]}
            for key in ["families_weighted", "hispanic_families_weighted", "income_weighted", "hispanic_income_weighted", "family_share", "income_share", "kish_n"]:
                vals = [r[key] for r in rows]
                avg[key] = float(np.mean(vals)) if all(v is not None for v in vals) else None
            for key in ["sample_families", "sample_hispanic_families", "family_share", "income_share"]:
                vals = [r[key] for r in rows if r[key] is not None]
                avg[key + "_min"] = min(vals) if vals else None
                avg[key + "_max"] = max(vals) if vals else None
            avg["unique_families_any_implicate"] = int(d.loc[selected, "yy1"].nunique())
            avg["unique_hispanic_families_any_implicate"] = int(d.loc[selected & hispanic, "yy1"].nunique())
            avg["sampling_se_status"] = "NOT_ESTIMATED_no_bootstrap_weights"
            averaged.append(avg)
    return detailed, averaged


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bridge_rows(average: list[dict], bridge_path: Path) -> list[dict]:
    """Conditional diagnostics, never observed tax shares: distinct survey objects."""
    if not bridge_path.exists():
        raise ValueError("[BLOCKED] CPS Hispanic bridge missing; run cps_pool.py first")
    bridge = pd.read_csv(bridge_path, dtype={"bin19": str})
    labels = {"200k_500k": "12", "500k_1m": "13", "1m_plus": "1M+"}
    rows = []
    for scf in average:
        if scf["hispanic_definition"] != "hispanic_any_race" or scf["bin"] not in labels:
            continue
        for sample in [f"year_{scf['scf_year']}_real2023", "pooled_real2023"]:
            match = bridge[(bridge["sample"] == sample) & (bridge.bin19 == labels[scf["bin"]])]
            if len(match) != 1:
                raise ValueError(f"[BLOCKED] ambiguous/missing CPS bridge {sample} {scf['bin']}")
            cps = match.iloc[0]
            rows.append(dict(scf_year=scf["scf_year"], bin=scf["bin"], cps_sample=sample,
                             scf_hispanic_family_share=scf["family_share"],
                             scf_hispanic_gross_income_share=scf["income_share"],
                             cps_union_of_hispanic_tax_share=float(cps.ratio),
                             cps_union_of_hispanic_carrier_share=float(cps.carrier_ratio),
                             conditional_tax_share_proxy=scf["income_share"] * float(cps.ratio),
                             conditional_family_share_proxy=scf["family_share"] * float(cps.carrier_ratio),
                             scf_unique_hispanic_families=scf["unique_hispanic_families_any_implicate"],
                             cps_union_records=int(cps.union_records), cps_hispanic_records=int(cps.hispanic_records),
                             status="CONDITIONAL_cross_object_bridge_not_observed_income_tax"))
    return rows


def source_rows() -> list[dict]:
    sources = [
        (RAW[2019], "https://www.federalreserve.gov/econres/files/scf2019s.zip", "2019 SCF nominal public raw; extracted p19i6.dta"),
        (RAW[2022], "https://www.federalreserve.gov/econres/files/scf2022s.zip", "2022 SCF nominal public raw; preexisting local archive"),
        (RAW[2022].with_name("rscfp2022.dta"), "https://www.federalreserve.gov/econres/files/scfp2022s.zip", "Official summary extract; independent income reconstruction and WGT check"),
        (CACHE / "bulletin.macro.txt", "https://www.federalreserve.gov/econres/files/bulletin.macro.txt", "Fed INCOME, MCONV, WGT and H_RACE definitions; fetched 2026-10-15"),
        (CPI, "https://api.bls.gov/publicAPI/v2/timeseries/data/", "CUUR0000SA0 M13; preexisting primary BLS response"),
        (CACHE / "scf_2019.html", "https://www.federalreserve.gov/econres/scf_2019.htm", "SCF2019 file links and five-implicate documentation"),
        (CACHE / "scf_2022.html", "https://www.federalreserve.gov/econres/scf_2022.htm", "SCF2022 file links and five-implicate documentation"),
    ]
    rows = []
    for p, url, obj in sources:
        if not p.is_file() or p.stat().st_size == 0:
            raise ValueError(f"[BLOCKED] missing primary outside-check source {p}")
        rows.append(dict(path=str(p.relative_to(ROOT)), url=url, bytes=p.stat().st_size,
                         sha256=hashlib.file_digest(p.open("rb"), "sha256").hexdigest(), object=obj))
    return rows


def reconstruction_check(raw: pd.DataFrame) -> dict:
    """Keyed parity with official extract; permit only one common dollar scale."""
    summary, _ = pyreadstat.read_dta(RAW[2022].with_name("rscfp2022.dta"), usecols=["y1", "income", "wgt"])
    ours = pd.DataFrame(dict(y1=raw.y1, nominal_income=gross_income(raw), weight=raw.x42001 / 5))
    merged = summary.merge(ours, on="y1", validate="one_to_one")
    if len(merged) != len(raw) or len(merged) != len(summary):
        raise ValueError("[BLOCKED] official SCF summary/raw row coverage mismatch")
    positive = merged.nominal_income > 0
    ratios = merged.loc[positive, "income"] / merged.loc[positive, "nominal_income"]
    scale = float(ratios.median())
    relative_error = float(np.max(np.abs(ratios / scale - 1)))
    absolute_error = float(np.max(np.abs(merged.income - merged.nominal_income * scale)))
    weight_error = float(np.max(np.abs(merged.wgt - merged.weight)))
    if relative_error > 1e-12 or weight_error > 1e-9 or (merged.loc[~positive, "income"] != 0).any():
        raise ValueError("[BLOCKED] reconstructed SCF income or weights fail official extract parity")
    return dict(scf_year=2022, matched_implicate_rows=len(merged), common_summary_price_factor=scale,
                max_relative_income_discrepancy=relative_error,
                max_absolute_income_discrepancy=absolute_error, max_weight_discrepancy=weight_error,
                status="PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=LANE / "derived")
    args = parser.parse_args()
    started = time.perf_counter()
    prices = cpi_annual()
    detailed, average, audits = [], [], []
    for year, path in RAW.items():
        d, _ = pyreadstat.read_dta(path, usecols=COLS)
        if year == 2022:
            reconstruction = reconstruction_check(d)
        det, avg = summarize(d, year, prices)
        detailed.extend(det)
        average.extend(avg)
        audits.append(dict(scf_year=year, families=d.yy1.nunique(), implicate_rows=len(d),
                           implicates=5, average_weighted_families=float(d.x42001.sum() / 5),
                           nominal_income_year=year - 1, cpi_income_year=prices[year - 1],
                           cpi2023=prices[2023], factor=prices[2023] / prices[year - 1]))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for name, rows in [("outside_scf_implicates.csv", detailed), ("outside_scf.csv", average),
                       ("outside_scf_audit.csv", audits), ("outside_sources.csv", source_rows()),
                       ("outside_reconstruction.csv", [reconstruction]),
                       ("outside_bridge.csv", bridge_rows(average, LANE / "derived/cps_hispanic_bridge.csv"))]:
        write_csv(args.out_dir / name, rows)
    # Darwin reports bytes; Linux reports KiB. No nondeterministic timing in derived files.
    import sys
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_gib = peak / (1024 ** 3 if sys.platform == "darwin" else 1024 ** 2)
    if peak_gib >= 2.5:
        raise RuntimeError(f"[FAILED] memory budget exceeded: {peak_gib:.3f} GiB")
    print(f"SCF outside checks: {len(average)} rows; {time.perf_counter() - started:.3f}s; peak {peak_gib:.3f} GiB")


if __name__ == "__main__":
    main()
