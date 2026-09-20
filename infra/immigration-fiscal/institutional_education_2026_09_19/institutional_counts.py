#!/usr/bin/env python3
"""ACS institutional counts by education/origin/age, with all 80 SDR replicates.

Native-First: extend the existing PUMS tabulation pattern with numpy/pandas;
no new database, survey linkage, central price, or fiscal-account mutation.
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import hashlib
import json
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = _data_paths.data_root(require_exists=False) / 'external/acs_pums_2024_1yr/csv_pus.zip'
MEMBERS = ("psam_pusa.csv", "psam_pusb.csv")
WEIGHTS = ["PWGTP"] + [f"PWGTP{i}" for i in range(1, 81)]
FIELDS = ["SERIALNO", "AGEP", "SEX", "NATIVITY", "POBP", "HISP", "RAC1P", "RELSHIPP", "SCHL"]
ORIGINS = ("mexico_born", "other_central_america", "caribbean", "south_america", "southeast_asia", "all_native", "native_nh_white")
EDUCATIONS = ("all", "lt_hs", "hs_only", "some_college", "ba_plus")
BANDS = ("25-34", "35-44", "45-54", "55-64", "65-74", "75+")
BAND_STARTS = np.array([25, 35, 45, 55, 65, 75])
QUANTITIES = ("population_all", "household_population", "institutional_population", "institutional_male_population")
PRICES = (0, 50_000, 100_000, 150_000)
PRICE_STATUS = "explicit_uncalibrated_assumption_not_bound_or_central_estimate"
SPARSE_N = 30  # Disclosure heuristic only, not a reliability certification.
EXPECTED_NATIONAL_POPULATION = 340_110_990
EXPECTED_GATE = 107_917
DOMAINS = [(origin, education) for origin in ORIGINS for education in EDUCATIONS]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sdr_variance(estimates: np.ndarray) -> np.ndarray:
    """Last axis is full weight then PWGTP1..80; covariance stays paired."""
    x = np.asarray(estimates, dtype=float)
    if x.ndim == 0 or x.shape[-1] != 81 or not np.isfinite(x).all():
        raise ValueError("Expected finite full-weight + 80-replicate estimates")
    return (4.0 / 80.0) * np.sum((x[..., 1:] - x[..., :1]) ** 2, axis=-1)


def contrast(left: np.ndarray, right: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Paired survey contrast; never treat shared reference estimates as independent."""
    if np.shape(left) != np.shape(right):
        raise ValueError("Contrast shapes differ")
    delta = np.asarray(left, dtype=float) - np.asarray(right, dtype=float)
    return delta[..., 0], sdr_variance(delta)


def origin_masks(d: pd.DataFrame) -> dict[str, np.ndarray]:
    native = d.NATIVITY.eq(1).to_numpy()
    foreign = d.NATIVITY.eq(2).to_numpy()
    return {
        "mexico_born": foreign & d.POBP.eq(303).to_numpy(),
        "other_central_america": foreign & d.POBP.between(310, 316).to_numpy(),
        "caribbean": foreign & d.POBP.between(321, 344).to_numpy(),
        "south_america": foreign & d.POBP.between(360, 374).to_numpy(),
        "southeast_asia": foreign & d.POBP.isin([205, 206, 211, 223, 226, 233, 236, 242, 247]).to_numpy(),
        "all_native": native,
        "native_nh_white": native & d.HISP.eq(1).to_numpy() & d.RAC1P.eq(1).to_numpy(),
    }


def education_masks(d: pd.DataFrame) -> dict[str, np.ndarray]:
    adult = d.AGEP.ge(25).to_numpy()
    valid = d.SCHL.between(1, 24).to_numpy() & (d.SCHL.fillna(0) % 1 == 0).to_numpy()
    if np.any(adult & ~valid):
        raise ValueError("Missing or invalid SCHL for an age-25+ person")
    return {
        "all": adult,
        "lt_hs": adult & d.SCHL.between(1, 15).to_numpy(),
        "hs_only": adult & d.SCHL.isin([16, 17]).to_numpy(),
        "some_college": adult & d.SCHL.between(18, 20).to_numpy(),
        "ba_plus": adult & d.SCHL.between(21, 24).to_numpy(),
    }


def residence_masks(d: pd.DataFrame) -> dict[str, np.ndarray]:
    household = d.SERIALNO.str.slice(4, 6).eq("HU").to_numpy()
    gq = d.SERIALNO.str.slice(4, 6).eq("GQ").to_numpy()
    inst = d.RELSHIPP.eq(37).to_numpy()
    noninst = d.RELSHIPP.eq(38).to_numpy()
    if not np.all(household | gq) or not np.array_equal(gq, inst | noninst):
        raise ValueError("SERIALNO HU/GQ disagrees with RELSHIPP 37/38")
    return {
        "population_all": np.ones(len(d), dtype=bool),
        "household_population": household,
        "institutional_population": inst,
        "institutional_male_population": inst & d.SEX.eq(1).to_numpy(),
    }


def empty_arrays() -> tuple[dict[str, np.ndarray], dict[str, np.ndarray]]:
    return ({q: np.zeros((len(DOMAINS), len(BANDS), 81), dtype=np.int64) for q in QUANTITIES},
            {q: np.zeros((len(DOMAINS), len(BANDS)), dtype=np.int64) for q in QUANTITIES})


def accumulate(d: pd.DataFrame, weighted: dict, raw: dict, meta: dict) -> None:
    origins, educations, residence = origin_masks(d), education_masks(d), residence_masks(d)
    weights = d[WEIGHTS].to_numpy(dtype=np.int64)
    if not np.isfinite(weights).all() or (weights[:, 0] < 0).any():
        raise ValueError("Nonfinite weights or negative full weights")
    age = d.AGEP.to_numpy()
    bands = np.searchsorted(BAND_STARTS, age, side="right") - 1
    meta["records"] += len(d)
    meta["national_population_all_ages"] += int(weights[:, 0].sum())
    gate = (d.NATIVITY.eq(1) & d.HISP.eq(2) & d.SEX.eq(1) & d.AGEP.between(18, 39)).to_numpy()
    gate = gate & residence["institutional_population"]
    meta["usborn_mexican_male_18_39_institutional"] += int(weights[gate, 0].sum())
    for q, mask in residence.items():
        meta["all_age_raw_records"][q] += int(mask.sum())
    for domain, (origin, education) in enumerate(DOMAINS):
        domain_mask = origins[origin] & educations[education]
        for band in range(len(BANDS)):
            in_cell = domain_mask & (bands == band)
            if not in_cell.any():
                continue
            for q, mask in residence.items():
                selected = in_cell & mask
                raw[q][domain, band] += int(selected.sum())
                weighted[q][domain, band] += weights[selected].sum(axis=0)


def gates(weighted: dict, raw: dict, meta: dict) -> dict:
    checks = {
        "national_population_all_ages": meta["national_population_all_ages"] == EXPECTED_NATIONAL_POPULATION,
        "usborn_mexican_male_18_39_institutional": meta["usborn_mexican_male_18_39_institutional"] == EXPECTED_GATE,
        "all_finite": all(np.isfinite(x).all() for x in [*weighted.values(), *raw.values()]),
        "nonnegative_counts": all((x >= 0).all() for x in [*weighted.values(), *raw.values()]),
    }
    for q in QUANTITIES:
        for oi, origin in enumerate(ORIGINS):
            start = oi * len(EDUCATIONS)
            for label, values in (("weighted", weighted[q]), ("raw", raw[q])):
                checks[f"education_partition|{q}|{origin}|{label}"] = bool(
                    np.array_equal(values[start], values[start + 1:start + 5].sum(axis=0)))
        estimate, variance = contrast(weighted[q], weighted[q])
        checks[f"zero_self_contrast|{q}"] = bool(np.all(estimate == 0) and np.all(variance == 0))
    for label, values in (("weighted", weighted), ("raw", raw)):
        checks[f"residence_subset|{label}"] = bool(np.all(
            values["population_all"] >= values["household_population"] + values["institutional_population"]))
        checks[f"male_institution_subset|{label}"] = bool(np.all(
            values["institutional_population"] >= values["institutional_male_population"]))
    failed = [key for key, value in checks.items() if not value]
    if failed:
        raise ValueError(f"Institutional gates failed: {failed}")
    return {"passed": len(checks), "failed": 0, "checks": checks}


def export(out: Path, weighted: dict, raw: dict, meta: dict, source: Path, source_info: dict) -> dict:
    validation = gates(weighted, raw, meta)
    out.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(out / "counts.npz", **weighted, **{f"{q}_n": raw[q] for q in QUANTITIES})
    pd.DataFrame([{"domain_index": i, "origin": origin, "education": education,
                   "native_reference_is_third_plus": False}
                  for i, (origin, education) in enumerate(DOMAINS)]).to_csv(out / "domains.csv", index=False)
    pd.DataFrame({"band_index": range(6), "band": BANDS, "age_min": BAND_STARTS,
                  "age_max": [34, 44, 54, 64, 74, 99]}).to_csv(out / "bands.csv", index=False)
    pd.DataFrame({"weight_index": range(81), "weight_name": WEIGHTS}).to_csv(out / "weights.csv", index=False)
    rows, prices = [], []
    for domain, (origin, education) in enumerate(DOMAINS):
        for band, label in enumerate(BANDS):
            base = {"domain_index": domain, "origin": origin, "education": education, "band": label}
            for q in QUANTITIES:
                estimate = int(weighted[q][domain, band, 0])
                se = float(np.sqrt(sdr_variance(weighted[q][domain, band])))
                n = int(raw[q][domain, band])
                rows.append({**base, "quantity": q, "estimate": estimate, "se": se,
                             "ci95_low": estimate - 1.959963984540054 * se,
                             "ci95_high": estimate + 1.959963984540054 * se,
                             "raw_n": n, "sparse_raw_n_lt_30": n < SPARSE_N,
                             "zero_observed_records": n == 0})
            inst = weighted["institutional_population"][domain, band]
            n_inst = int(raw["institutional_population"][domain, band])
            for price in PRICES:
                priced = price * inst
                prices.append({**base, "unit_price_2024_dollars": price, "price_status": PRICE_STATUS,
                               "cost_2024_dollars": int(priced[0]),
                               "sampling_se_conditional_on_price": float(np.sqrt(sdr_variance(priced))),
                               "institutional_raw_n": n_inst, "sparse_raw_n_lt_30": n_inst < SPARSE_N})
    pd.DataFrame(rows).to_csv(out / "counts.csv", index=False)
    pd.DataFrame(prices).to_csv(out / "unit_cost_scenarios.csv", index=False)
    audit = {
        "schema_version": 1, "lane": HERE.name, "source": str(source.resolve()), **source_info,
        "implementation_sha256": sha256(Path(__file__)), "metadata": meta, "gates": validation,
        "dimensions": {"domains": len(DOMAINS), "bands": len(BANDS), "weights": len(WEIGHTS)},
        "source_urls": {
            "data": "https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/csv_pus.zip",
            "dictionary": "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf",
            "accuracy": "https://www2.census.gov/programs-surveys/acs/tech_docs/pums/accuracy/2024AccuracyPUMS.pdf",
        },
        "variance": "ACS SDR 4/80 times squared deviations from full-weight estimate; paired replicates",
        "price_grid_2024_dollars": list(PRICES), "price_status": PRICE_STATUS,
        "scope": "ACS 2024 1-year resident stocks aged 25+, 50 states and DC, households and group quarters",
        "interpretation": "Institutions of every type share the stated hypothetical price. No prison identification, generation-3 proxy equivalence, admission effect, central cost, marginal-cost estimate, or CPS denominator conversion.",
        "sparse_rule": "Raw n < 30 flags sparse observations; heuristic only, no suppression or reliability guarantee.",
        "exports": {},
    }
    for name in ("counts.npz", "domains.csv", "bands.csv", "weights.csv", "counts.csv", "unit_cost_scenarios.csv"):
        audit["exports"][name] = sha256(out / name)
    (out / "audit.json").write_text(json.dumps(audit, indent=2) + "\n")
    return audit


def build(source: Path, out: Path, chunk_size: int = 200_000) -> dict:
    if chunk_size < 1:
        raise ValueError("chunk_size must be positive")
    before = source.stat()
    weighted, raw = empty_arrays()
    meta = {"records": 0, "national_population_all_ages": 0,
            "usborn_mexican_male_18_39_institutional": 0,
            "all_age_raw_records": {q: 0 for q in QUANTITIES}}
    dtypes = {field: np.int32 for field in FIELDS + WEIGHTS if field not in ("SERIALNO", "SCHL")}
    dtypes.update({"SERIALNO": str, "SCHL": float})
    with zipfile.ZipFile(source) as archive:
        available = {name for name in archive.namelist() if name.endswith(".csv")}
        if available != set(MEMBERS):
            raise ValueError(f"Expected US person parts {MEMBERS}, found {sorted(available)}")
        part_info = [{"name": name, "uncompressed_bytes": archive.getinfo(name).file_size,
                      "crc32": f"{archive.getinfo(name).CRC:08x}"} for name in MEMBERS]
        for member in MEMBERS:
            with archive.open(member) as stream:
                for data in pd.read_csv(stream, usecols=FIELDS + WEIGHTS, dtype=dtypes, chunksize=chunk_size):
                    accumulate(data, weighted, raw, meta)
                    print(f"{member}: {meta['records']:,} cumulative records", flush=True)
    source_info = {"source_sha256": sha256(source), "source_parts": part_info}
    after = source.stat()
    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
        raise ValueError("Source changed while reading; refusing export")
    return export(out, weighted, raw, meta, source, source_info)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--out", type=Path, default=HERE / "derived")
    parser.add_argument("--chunk-size", type=int, default=200_000)
    args = parser.parse_args()
    started = time.monotonic()
    audit = build(args.source, args.out, args.chunk_size)
    print(json.dumps({"elapsed_seconds": round(time.monotonic() - started, 2),
                      "gates_passed": audit["gates"]["passed"], "metadata": audit["metadata"]}, indent=2))


if __name__ == "__main__":
    main()
