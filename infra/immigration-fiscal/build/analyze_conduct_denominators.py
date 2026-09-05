#!/usr/bin/env python3
"""Recalculate source-defined conduct comparisons without writing any database.

Native-First: pandas/pyreadstat read existing source files; CSV/JSON are the outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pyreadstat

from load_light_tx_crime import _read, _melt, _melt_nat
from load_spi_citizenship import summarize_spi


def audit(data_root: Path, output: Path, scaap_pdf: Path | None = None) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    base = data_root / "external" / "crime_frontier"
    tables = {name: _read(base / "light_texas", name, pd) for name in
              ["big_category.dta", "big_category_pew.dta", "big_category_nat.dta"]}
    if any(table is None for table in tables.values()):
        raise ValueError("All three Light source tables are required")
    cms, pew, nat = (tables[n] for n in
                     ["big_category.dta", "big_category_pew.dta", "big_category_nat.dta"])
    merged = cms.merge(nat, on=["year", "category"], suffixes=("_base", "_split"), validate="one_to_one")
    for field in ["citizen_charge", "tot_citizen"]:
        if not np.array_equal(merged[f"{field}_base"], merged[f"{field}_split"]):
            raise ValueError(f"Native-born {field} changed across source tables")
    for field, naturalized in [("immigrants_charge", "naturalized_charge"),
                               ("tot_legal2_immi", "naturalized_citizen")]:
        if not np.allclose(merged[f"{field}_base"], merged[f"{field}_split"] + merged[naturalized], atol=2, rtol=0):
            raise ValueError(f"Naturalized split does not conserve {field}")
    rows = _melt(cms, "CMS") + _melt(pew, "Pew") + _melt_nat(nat)
    rates = pd.DataFrame(rows)
    if rates[["charge_count", "population"]].isna().any().any() or (rates.population <= 0).any():
        raise ValueError("Missing counts or nonpositive population")
    rates["recalculated_per_100k"] = rates.charge_count / rates.population * 1e5
    max_error = float((rates.recalculated_per_100k - rates.crime_rate_per_100k).abs().max())
    if max_error > .01:
        raise ValueError(f"Counts/denominators disagree with source rates by {max_error}")
    rates.to_csv(output / "tx_rates.csv", index=False)
    comparator = rates.loc[rates.status_class.eq("native_born"),
                           ["year", "crime_category", "denom_source", "recalculated_per_100k"]]
    comparison = rates.merge(comparator, on=["year", "crime_category", "denom_source"],
                             suffixes=("", "_native"), validate="many_to_one")
    comparison["ratio_to_native_born"] = comparison.recalculated_per_100k / comparison.recalculated_per_100k_native
    comparison.to_csv(output / "tx_comparisons.csv", index=False)
    headline = comparison.loc[(comparison.year == 2018) & comparison.crime_category.eq("violent")]
    raw2018 = nat.loc[(nat.year == 2018) & (nat.category == 1)].iloc[0]
    legacy_rate = float((raw2018.citizen_charge - raw2018.naturalized_charge) /
                        (raw2018.tot_citizen - raw2018.naturalized_citizen) * 1e5)

    spi_path = base / "spi" / "ICPSR_37692" / "DS0001" / "37692-0001-Data.dta"
    spi, _ = pyreadstat.read_dta(str(spi_path), usecols=["V0945", "V0946", "V0950", "V0951", "RV0001", "RV0004", "V1585"])
    _, metadata = pyreadstat.read_dta(str(spi_path), metadataonly=True)
    summary = summarize_spi(spi)
    summary.to_csv(output / "spi_official_citizenship.csv", index=False)
    legacy = np.select([spi.V0950.eq(2), spi.V0950.isin([-1, -2])], ["noncitizen", "ambiguous"], default="us_citizen")
    official = np.select([spi.RV0004.eq(2), spi.RV0004.eq(1)], ["noncitizen", "us_citizen"], default="ambiguous")
    changes = pd.DataFrame({"legacy": legacy, "official": official, "weight": spi.V1585})
    changes.groupby(["legacy", "official"]).agg(sample_n=("weight", "size"), weighted_inmates=("weight", "sum")).to_csv(output / "spi_classification_changes.csv")
    schema = {"light": {name: {"columns": list(df.columns), "years": sorted(df.year.unique().tolist())}
                        for name, df in tables.items()},
              "spi": {"survey_year": 2016, "rows": len(spi), "columns": metadata.column_names_to_labels,
                      "RV0004_codes": {str(k): int(v) for k, v in spi.RV0004.value_counts(dropna=False).items()},
                      "V0946_codes": {str(k): int(v) for k, v in spi.V0946.value_counts(dropna=False).items()}}}
    (output / "source_schema.json").write_text(json.dumps(schema, indent=2) + "\n")
    result = {"tx_rows": len(rates), "max_source_rate_rounding_error": max_error,
              "tx_2018_violent": headline.to_dict("records"),
              "legacy_double_subtracted_native_rate_2018": legacy_rate,
              "spi_official": summary.astype(object).where(summary.notna(), None).to_dict("records"),
              "spi_changed_assignments": int((legacy != official).sum()),
              "spi_age_check": {"min_age": float(spi.RV0001.min()), "under18": int(spi.RV0001.lt(18).sum()), "missing": int(spi.RV0001.isna().sum())},
              "spi_rates": "Not estimated: matched national 2016 adult citizenship denominator not available in this run",
              "fraud_case_arithmetic": {"paid_loss_approx_usd": 2200000,
                   "case_beneficiaries_approx": 350, "loss_per_case_beneficiary_approx_usd": 2200000 / 350,
                   "period": "April 2022-April 2025",
                   "source": "https://www.justice.gov/opa/pr/four-men-plead-guilty-2m-minnesota-medicaid-fraud",
                   "interpretation": "Selected admitted scheme; not immigrant or program-wide fraud prevalence; recoveries not netted"}}
    sources = [base / "light_texas" / "124923-V1.zip", spi_path,
               base / "spi" / "ICPSR_37692" / "DS0001" / "37692-0001-Codebook.pdf"]
    if scaap_pdf is not None:
        import pdfplumber
        scaap = []
        with pdfplumber.open(scaap_pdf) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    for row in table:
                        if not row or str(row[0]).strip() != "2024":
                            continue
                        if len(row) != 9:
                            raise ValueError(f"FY24 award schema changed: {len(row)} columns")
                        year, state, name, application, salary, total, confirmed, unknown, award = row
                        num = lambda x: float(x.replace(",", "").replace("$", "").strip())
                        scaap.append({"fiscal_year": int(year), "state": state, "jurisdiction": name,
                                      "application": application, "salary_usd": num(salary),
                                      "total_days": num(total), "confirmed_days": num(confirmed),
                                      "unknown_days": num(unknown), "award_usd": num(award)})
        if not scaap:
            raise ValueError("No FY2024 SCAAP rows parsed")
        frame = pd.DataFrame(scaap)
        if frame.application.duplicated().any():
            raise ValueError("Duplicate SCAAP applications")
        frame.to_csv(output / "scaap_fy24_awards.csv", index=False)
        result["scaap_fy24"] = {"applications": len(frame), "fields": list(frame.columns),
                                "sums": frame[["total_days", "confirmed_days", "unknown_days", "award_usd"]].sum().to_dict(),
                                "scope": "Participating applicants and custody person-time; no population offending rate"}
        sources.append(scaap_pdf)
    result["source_hashes"] = [{"path": str(p), "sha256": hashlib.sha256(p.read_bytes()).hexdigest(), "bytes": p.stat().st_size}
                              for p in sources]
    (output / "numerical-results.json").write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scaap-awards", type=Path)
    args = parser.parse_args()
    result = audit(args.data_root, args.output, args.scaap_awards)
    print(json.dumps({k: v for k, v in result.items() if k not in ["source_hashes", "tx_2018_violent"]}, indent=2, allow_nan=False))
