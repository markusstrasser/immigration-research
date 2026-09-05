# /// script
# requires-python = ">=3.11"
# dependencies = ["duckdb", "numpy", "pandas"]
# ///
"""Describe ACS arrival cohorts and extend the existing 2023 partial fiscal model.

Native-First: pandas streams the official CSVs; NumPy computes the official SDR
replicates; DuckDB reads existing donor cells without changing any warehouse.
Generated files belong outside tracked source (for example .scratch/).

YOEP is most recent entry to live in the US, not necessarily first immigration.
These are repeated cross sections, not a panel or an identified policy effect.
Income is rolling past-12-month income adjusted to the survey year's dollars;
new entrants' income may include earnings before entering the United States.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import zipfile

import duckdb
import numpy as np
import pandas as pd

from build_federal_microsim_sipp_2024 import employee_oasdi_hi_proxy, _acs_age_band
from public_mvp_io import income_band_annual


WEIGHTS = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]
FIELDS = ["AGEP", "SEX", "NATIVITY", "POBP", "YOEP", "FYOEP", "HISP",
          "RAC1P", "SCHL", "ESR", "RELSHIPP", "PERNP", "PINCP", "WAGP",
          "ADJINC", "ENG", "LANX"]
PROFILE_METRICS = ["mean_age", "male_share", "employment_population",
                   "earnings_mean_survey_dollars", "total_income_mean_survey_dollars",
                   "less_than_hs_share", "ba_plus_share", "limited_english_share",
                   "entry_year_allocated_share", "positive_earnings_share"]
AGE_METRICS = ["mean_age", "under18_share", "age65plus_share"]
FISCAL_METRICS = ["projected_employee_payroll", "projected_selected_transfers",
                  "projected_partial_balance", "direct_acs_employee_payroll"]
FISCAL_SCOPES = {
    "projected_employee_payroll": "Employee payroll proxy transported from SIPP; tax component only",
    "projected_selected_transfers": "Allocated SNAP/TANF/SSI transported from SIPP; benefit component only",
    "projected_partial_balance": "Projected employee payroll less allocated SNAP/TANF/SSI; not full fiscal impact",
    "direct_acs_employee_payroll": "Employee payroll formula on ACS rolling-year earnings; tax proxy only, not actual taxes",
}


def sdr_estimate(estimates: np.ndarray) -> dict:
    """One full estimate and 80 whole-estimate replicates, including negatives."""
    if estimates.shape != (81,) or not np.isfinite(estimates).all():
        raise ValueError("Expected 81 finite full/replicate estimates")
    point = float(estimates[0])
    se = float(np.sqrt((4 / 80) * np.square(estimates[1:] - point).sum()))
    return {"estimate": point, "acs_sdr_se": se,
            "ci95_low": point - 1.96 * se, "ci95_high": point + 1.96 * se}


def ratios(numerator: np.ndarray, denominator: np.ndarray) -> np.ndarray:
    if not np.isfinite(denominator).all() or (denominator <= 0).any():
        raise ValueError("Nonpositive/nonfinite full or replicate group denominator")
    return numerator / denominator


def cohort_masks(frame: pd.DataFrame, year: int) -> dict[str, np.ndarray]:
    native = frame.NATIVITY.eq(1).to_numpy()
    fb = frame.NATIVITY.eq(2).to_numpy()
    origin = {"foreign_born": fb,
              "mexico_born": fb & frame.POBP.eq(303).to_numpy(),
              "somalia_born": fb & frame.POBP.eq(448).to_numpy()}
    result = {"native": native,
              "native_nhwhite": native & frame.HISP.eq(1).to_numpy()
              & frame.RAC1P.eq(1).to_numpy()}
    for name, mask in origin.items():
        result[f"{name}/stock"] = mask
        result[f"{name}/entry_0_3"] = mask & frame.YOEP.between(year - 3, year).to_numpy()
        result[f"{name}/entry_1_3"] = mask & frame.YOEP.between(year - 3, year - 1).to_numpy()
        if name != "somalia_born":
            for duration in range(4):
                result[f"{name}/entry_d{duration}"] = mask & frame.YOEP.eq(year - duration).to_numpy()
        if year >= 2022:
            result[f"{name}/entry_since2022"] = mask & frame.YOEP.between(2022, year).to_numpy()
    return result


@contextmanager
def person_streams(path: Path):
    if path.is_dir():
        paths = [path / "psam_pusa.csv", path / "psam_pusb.csv"]
        if not all(p.is_file() for p in paths):
            raise FileNotFoundError("Both national ACS person CSV parts are required")
        yield [(p.name, p) for p in paths]
    else:
        with zipfile.ZipFile(path) as archive:
            members = [n for n in archive.namelist() if Path(n).name in
                       ("psam_pusa.csv", "psam_pusb.csv")]
            if len(members) != 2:
                raise ValueError("Expected exactly two national ACS person parts")
            streams = [(name, archive.open(name)) for name in sorted(members)]
            try:
                yield streams
            finally:
                for _, stream in streams:
                    stream.close()


def sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def education_bucket(code: int) -> str:
    if 1 <= code <= 15:
        return "<HS"
    if code in (16, 17):
        return "HS / GED"
    if code in (18, 19, 20):
        return "some college / associate"
    if 21 <= code <= 24:
        return "other"
    raise ValueError(f"Unknown education code {code}")


def load_donors(database: Path) -> dict:
    donors = {}
    with duckdb.connect(str(database), read_only=True) as con:
        for table in ("sipp_person_donor_cells_usborn_2024", "sipp_person_donor_cells_2024"):
            rows = con.execute(f"""SELECT nativity_code, education_bucket, age_band,
                income_band, employee_oasdi_hi_proxy_annual, allocated_snap_tanf_ssi_annual,
                payroll_less_allocated_benefits_proxy_annual, person_year_count
                FROM {table}""").fetchall()
            for nativity, education, age, income, payroll, transfers, balance, count in rows:
                key = (int(nativity), education, age, income)
                if key in donors or count <= 0:
                    raise ValueError(f"Invalid/duplicate donor cell {key}")
                donors[key] = (payroll, transfers, balance, count)
    if len(donors) != 128:
        raise ValueError(f"Expected 128 supported donor cells, found {len(donors)}")
    return donors


def analyze(year: int, path: Path, database: Path, out: Path, limit: int | None) -> None:
    sums: dict[tuple[str, str], np.ndarray] = {}
    samples = defaultdict(int)
    fiscal_sums: dict[tuple[str, str], np.ndarray] = {}
    fiscal_samples = defaultdict(int)
    # Preserve full/replicate sufficient statistics for auditable derived contrasts.
    country_sums = defaultdict(lambda: np.zeros(81))
    country_samples = defaultdict(int)
    donor_low_support = defaultdict(float)
    rows_read = 0
    negative_replicates = 0
    donors = load_donors(database) if year == 2023 else None

    def accumulate(destination, counts, key, mask, w, values):
        if not mask.any():
            return
        matrix = np.column_stack((np.ones(int(mask.sum())), values[mask]))
        aggregate = w[mask].T @ matrix
        if key not in destination:
            destination[key] = np.zeros_like(aggregate)
        destination[key] += aggregate
        counts[key] += int(mask.sum())

    with person_streams(path) as streams:
        for member, stream in streams:
            for frame in pd.read_csv(stream, usecols=FIELDS + WEIGHTS, dtype=float,
                                     chunksize=100_000, nrows=limit):
                rows_read += len(frame)
                w = frame[WEIGHTS].to_numpy()
                if not np.isfinite(w).all() or (w[:, 0] <= 0).any():
                    raise ValueError("Invalid main or replicate weights")
                # Never drop a record because a replicate is zero or negative.
                negative_replicates += int((w[:, 1:] < 0).sum())
                age = frame.AGEP.to_numpy()
                adult = frame.AGEP.between(25, 64).to_numpy()
                institutional = frame.RELSHIPP.eq(37).to_numpy()
                military = frame.ESR.isin([4, 5]).to_numpy()
                cni = adult & ~institutional & ~military
                required = ["SCHL", "ESR", "PERNP", "PINCP", "SEX", "ADJINC", "LANX"]
                if frame.loc[adult, required].isna().any().any():
                    raise ValueError("Unexpected missing adult outcome/covariate")
                if not frame.loc[cni, "ESR"].isin([1, 2, 3, 6]).all():
                    raise ValueError("Unexpected civilian employment code")
                if not frame.NATIVITY.isin([1, 2]).all():
                    raise ValueError("Unexpected nativity code")
                factor = frame.ADJINC.to_numpy() / 1_000_000
                earnings = frame.PERNP.to_numpy() * factor
                income = frame.PINCP.to_numpy() * factor
                limited = frame.ENG.isin([2, 3, 4]).to_numpy()
                if not (frame.loc[adult, "LANX"].eq(2) |
                        frame.loc[adult, "ENG"].isin([1, 2, 3, 4])).all():
                    raise ValueError("Adult English universe/coding mismatch")
                values = np.column_stack((age, frame.SEX.eq(1), frame.ESR.isin([1, 2]),
                    earnings, income, frame.SCHL.between(1, 15), frame.SCHL.between(21, 24),
                    limited, frame.FYOEP.eq(1), earnings > 0))
                age_values = np.column_stack((age, age < 18, age >= 65))
                groups = cohort_masks(frame, year)
                for group, mask in groups.items():
                    accumulate(sums, samples, (group, "all_ages"), mask, w, age_values)
                    accumulate(sums, samples, (group, "civilian_noninstitutional_25_64"),
                               mask & cni, w, values)
                # Birthplace mix is a count of surviving observed residents, not admissions.
                for window in ("stock", "entry_0_3", "entry_1_3"):
                    selected = frame.loc[groups[f"foreign_born/{window}"], ["POBP"] + WEIGHTS]
                    for country, block in selected.groupby("POBP", sort=False):
                        country_sums[(window, int(country))] += block[WEIGHTS].sum().to_numpy()
                        country_samples[(window, int(country))] += len(block)

                if donors is not None:
                    positions = np.flatnonzero(adult)
                    projection = np.full((len(frame), 4), np.nan)
                    support = np.zeros(len(frame))
                    nativity_codes = frame.NATIVITY.to_numpy()
                    education_codes = frame.SCHL.to_numpy()
                    for pos in positions:
                        key = (int(nativity_codes[pos]), education_bucket(int(education_codes[pos])),
                               _acs_age_band(int(age[pos])), income_band_annual(float(income[pos])))
                        if key not in donors:
                            raise ValueError(f"Unsupported ACS recipient cell {key}")
                        payroll, transfers, balance, count = donors[key]
                        projection[pos] = (payroll, transfers, balance,
                                           employee_oasdi_hi_proxy(float(earnings[pos])))
                        support[pos] = count
                    for group in ("native", "native_nhwhite", "foreign_born/stock", "mexico_born/stock"):
                        for universe, base in (("all_adults_25_64", adult),
                                               ("civilian_noninstitutional_25_64", cni)):
                            mask = groups[group] & base
                            key = (group, universe)
                            accumulate(fiscal_sums, fiscal_samples, key, mask, w, projection)
                            donor_low_support[key] += float(w[mask & (support < 10), 0].sum())
                print(f"{year} {member}: {rows_read:,} records", flush=True)

    estimates = []
    replicate_outputs = {}
    for (group, universe), aggregate in sums.items():
        metrics = AGE_METRICS if universe == "all_ages" else PROFILE_METRICS
        denominator = aggregate[:, 0]
        base = {"survey_year": year, "group": group, "universe": universe,
                "sample_n": samples[(group, universe)]}
        estimates.append(base | {"metric": "population"} | sdr_estimate(denominator))
        replicate_outputs[f"{group}|{universe}|population"] = denominator.tolist()
        for col, metric in enumerate(metrics, 1):
            values = ratios(aggregate[:, col], denominator)
            estimates.append(base | {"metric": metric} | sdr_estimate(values))
            replicate_outputs[f"{group}|{universe}|{metric}"] = values.tolist()

    countries = []
    with duckdb.connect(str(database), read_only=True) as con:
        labels = {int(code): label for code, label in con.execute("SELECT * FROM pobp_dim").fetchall()}
    for (window, code), counts in country_sums.items():
        total = sums[(f"foreign_born/{window}", "all_ages")][:, 0]
        countries.append({"survey_year": year, "window": window, "pobp": code,
                          "country": labels.get(code, f"POBP {code}"),
                          "sample_n": country_samples[(window, code)],
                          "population": float(counts[0]), **sdr_estimate(ratios(counts, total))})

    fiscal = []
    for (group, universe), aggregate in fiscal_sums.items():
        for col, metric in enumerate(FISCAL_METRICS, 1):
            # Intentionally no total uncertainty interval for transported SIPP means.
            values = ratios(aggregate[:, col], aggregate[:, 0])
            row = {"survey_year": year, "group": group, "universe": universe,
                   "sample_n": fiscal_samples[(group, universe)], "metric": metric,
                   "population": float(aggregate[0, 0]), "estimate": float(values[0]),
                   "weight_assigned_donor_n_lt10": donor_low_support[(group, universe)],
                   "scope": FISCAL_SCOPES[metric]}
            if metric == "direct_acs_employee_payroll":
                row |= sdr_estimate(values)
            replicate_outputs[f"{group}|{universe}|{metric}"] = values.tolist()
            fiscal.append(row)

    inputs = [path] if path.is_file() else sorted(path.glob("psam_pus[ab].csv"))
    manifest = {"survey_year": year, "rows_read": rows_read, "smoke_nrows_per_part": limit,
                "negative_replicate_weights_retained": negative_replicates,
                "sources": [{"path": str(p.resolve()), "bytes": p.stat().st_size,
                             "sha256": sha256(p)} for p in inputs],
                "donor_database_sha256": sha256(database) if year == 2023 else None,
                "accuracy_source": f"https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/{year}AccuracyPUMS.pdf",
                "income_units": f"{year} dollars, rolling past 12 months, includes zeros and losses",
                "cohort_definition": "YOEP most recent entry, survey year minus entry year; 0–3 or 1–3 integer years",
                "ci_scope": "95% normal SDR survey sampling intervals, no nonresponse/coverage/model uncertainty",
                "fiscal_scope": "2023 stock projection only; SIPP donors reference2023; no fiscal projection for new cohorts"}
    out.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(estimates).to_csv(out / f"profiles_{year}.csv", index=False)
    pd.DataFrame(countries).to_csv(out / f"origin_mix_{year}.csv", index=False)
    if fiscal:
        pd.DataFrame(fiscal).to_csv(out / f"fiscal_comparison_{year}.csv", index=False)
    (out / f"replicate_estimates_{year}.json").write_text(json.dumps(replicate_outputs))
    (out / f"manifest_{year}.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"done": year, "rows": rows_read, "profile_rows": len(estimates),
                      "country_rows": len(countries), "fiscal_rows": len(fiscal)}), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--person-data", type=Path, required=True)
    parser.add_argument("--database", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--smoke-nrows", type=int)
    args = parser.parse_args()
    analyze(args.year, args.person_data, args.database, args.out, args.smoke_nrows)


if __name__ == "__main__":
    main()
