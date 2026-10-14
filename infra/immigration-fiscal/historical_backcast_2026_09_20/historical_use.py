#!/usr/bin/env python3
"""Measure historical school-age and Medicaid relative-use keys from pinned local ASEC.

Year is survey year minus one, matching the back-cast convention. School age is
age at survey, a demographic proxy rather than observed pupil attendance. Medicaid
MCAID=1 is prior-calendar-year Medicaid/PCHIP/other means-tested coverage, not
medical spending. IPUMS school rows use all ASEC records and 2014 half weights;
public-use Medicaid rows use the account's canonical civilian union. No missing
year is filled. Added non-identifying descendants are unobserved: g3plus rows
provide the identified G3+ path, not a measurement of those added people.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
POOLED = FISCAL / "g3_identity_pooled_2026_10_05/_cache/asec_pooled.csv.gz"
POOLED_PIN = "59e1c80d8738f8f3938b235db66f1656bce480b3cee276fcb1ed6ba748822e7e"
COLS = ["YEAR", "ASECFLAG", "ASECWT", "AGE", "BPL", "MBPL", "FBPL", "HISPAN"]
YEARS = list(range(2005, 2025))
MEX_HISPAN = [100, 102, 103, 104, 108, 109]


def pandemic_module():
    spec = importlib.util.spec_from_file_location(
        "historical_use_pandemic", FISCAL / "backcast_pandemic_measured_2026_09_28/measure_shares.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verified_source(path: Path, pin: str) -> dict:
    with path.open("rb") as stream:
        digest = hashlib.file_digest(stream, "sha256").hexdigest()
    if digest != pin:
        raise ValueError(f"[BLOCKED] source changed: {path}")
    return dict(path=str(path.relative_to(ROOT)), sha256=digest, bytes=path.stat().st_size)


def relative_use(national: float, group: float, national_key: float, group_key: float) -> tuple:
    values = np.asarray([national, group, national_key, group_key], float)
    if not np.isfinite(values).all() or (values <= 0).any():
        raise ValueError("[BLOCKED] nonpositive or missing key denominator/population")
    if group > national or group_key > national_key or national_key > national or group_key > group:
        raise ValueError("[BLOCKED] key populations do not nest")
    pop_share, key_share = group / national, group_key / national_key
    return pop_share, key_share, key_share / pop_share


def partition_gate(weight: np.ndarray, group: np.ndarray, national: np.ndarray) -> None:
    if not np.isfinite(weight).all() or np.any(group & ~national):
        raise ValueError("[BLOCKED] invalid weights or group outside national universe")
    total = np.sum(weight[national], axis=0)
    parts = np.sum(weight[group], axis=0) + np.sum(weight[national & ~group], axis=0)
    if np.any(total <= 0) or not np.allclose(parts, total, rtol=1e-12, atol=1e-6):
        raise ValueError("[BLOCKED] group and other weights do not partition the national total")


def school_sums(chunk: pd.DataFrame) -> pd.DataFrame:
    d = chunk[chunk.ASECFLAG.eq(1) & chunk.YEAR.between(2006, 2025)]
    if d[COLS].isna().any().any():
        raise ValueError("[BLOCKED] missing IPUMS measurement field")
    w = d.ASECWT.to_numpy(float) * np.where(d.YEAR.eq(2014), 0.5, 1.0)
    native = d.BPL.lt(15000)
    g3 = native & d.MBPL.lt(15000) & d.FBPL.lt(15000) & d.HISPAN.isin(MEX_HISPAN)
    union = d.BPL.eq(20000) | (native & (d.MBPL.eq(20000) | d.FBPL.eq(20000))) | g3
    kids = d.AGE.between(5, 17).to_numpy()
    national = np.ones(len(d), bool)
    if len(d):
        partition_gate(w, union.to_numpy(), national)
    rows = dict(year=d.YEAR - 1, national_population=w, national_key_population=w * kids)
    for name, group in (("union", union), ("g3plus", g3)):
        rows[f"{name}_population"] = w * group.to_numpy()
        rows[f"{name}_key_population"] = w * kids * group.to_numpy()
    return pd.DataFrame(rows).groupby("year").sum()


def row(year: int, key: str, group: str, frame: str, national: float, targeted: float,
        national_key: float, target_key: float, se: float, reps: int, source: str) -> dict:
    pop, share, use = relative_use(national, targeted, national_key, target_key)
    return dict(year=year, survey_year=year + 1, key=key, group=group, frame=frame,
                national_population=national, group_population=targeted,
                national_key_population=national_key, group_key_population=target_key,
                population_share=pop, key_share=share, relative_use=use,
                relative_use_se=se, replicates=reps, source=source)


def school_measure(path: Path = POOLED) -> list[dict]:
    chunks = [school_sums(c) for c in pd.read_csv(path, usecols=COLS, chunksize=500_000)]
    sums = pd.concat(chunks).groupby(level=0).sum()
    if sorted(sums.index) != YEARS:
        raise ValueError(f"[BLOCKED] missing school years: {sorted(set(YEARS) - set(sums.index))}")
    rows = []
    for year, r in sums.iterrows():
        for group in ("union", "g3plus"):
            rows.append(row(year, "school_age_5_17", group, "IPUMS_all_ASEC", r.national_population,
                            r[f"{group}_population"], r.national_key_population,
                            r[f"{group}_key_population"], np.nan, 0, str(path.relative_to(ROOT))))
    return rows


def coverage_row(d: pd.DataFrame, weights: np.ndarray, group: np.ndarray, civ: np.ndarray,
                 year: int, name: str, source: str, replicate_rows: list | None = None) -> dict:
    partition_gate(weights, group, civ)
    key = d.MCAID.eq(1).to_numpy()
    sums = [weights[mask].sum(axis=0) for mask in (civ, group, civ & key, group & key)]
    if any(not np.isfinite(v).all() or np.any(v <= 0) for v in sums):
        raise ValueError("[BLOCKED] missing/empty coverage replicate denominator")
    use = (sums[3] / sums[2]) / (sums[1] / sums[0])
    se = float(np.sqrt(4 / 160 * np.square(use[1:] - use[0]).sum()))
    result = row(year - 1, "medicaid_covered", name, "Census_canonical_civilian",
                 *(float(v[0]) for v in sums), se, 160, source)
    if abs(use[0] - result["relative_use"]) > 1e-12:
        raise ValueError("[BLOCKED] replicate 0 differs from the central relative-use key")
    if replicate_rows is not None:
        replicate_rows.extend(dict(year=year - 1, group=name, replicate=i, relative_use=float(value))
                              for i, value in enumerate(use))
    return result


def medicaid_measure(module) -> tuple[list[dict], list[dict], list[dict]]:
    rows, sources, replicate_rows = [], [], []
    fields = ["PH_SEQ", "PPPOS", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP",
              "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "MCAID"]
    for year, (path, pin) in module.SOURCES.items():
        sources.append(verified_source(path, pin))
        with zipfile.ZipFile(path) as archive:
            d = pd.read_csv(archive.open(f"pppub{year % 100}.csv"), usecols=fields)
            w = pd.read_csv(archive.open(f"asec_csv_repwgt_{year}.csv"),
                            usecols=["h_seq", "PPPOS", *module.REPS])
        d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"],
                    how="left", validate="one_to_one")
        if d.isna().any().any():
            raise ValueError(f"[BLOCKED] missing fields or replicate joins: ASEC {year}")
        np.testing.assert_allclose(d.MARSUPWT / 100, d.pwwgt0, rtol=0, atol=.01)
        civ, union = module.canonical_target(d)
        g3 = union & d.PRCITSHP.isin([1, 2, 3]).to_numpy() & d.PEFNTVTY.isin(module.US_BIRTH).to_numpy() \
            & d.PEMNTVTY.isin(module.US_BIRTH).to_numpy() & d.PRDTHSP.eq(1).to_numpy()
        weights = d[module.REPS].to_numpy(float)
        for name, group in (("union", union), ("g3plus", g3)):
            rows.append(coverage_row(d, weights, group, civ, year, name, str(path.relative_to(ROOT)), replicate_rows))
        del d, w, weights
    return rows, sources, replicate_rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived/p7")
    args = parser.parse_args()
    started = time.perf_counter()
    sources = [verified_source(POOLED, POOLED_PIN)]
    rows = school_measure()
    medicaid, public_sources, replicate_rows = medicaid_measure(pandemic_module())
    rows += medicaid
    sources += public_sources
    table = pd.DataFrame(rows).sort_values(["key", "group", "year"])
    if len(table) != 52 or table.duplicated(["key", "group", "year"]).any():
        raise ValueError("[BLOCKED] incomplete or duplicate historical-use grid")
    replicas = pd.DataFrame(replicate_rows).sort_values(["year", "group", "replicate"])
    if len(replicas) != 1932 or not replicas.groupby(["year", "group"]).replicate.apply(
            lambda values: list(values) == list(range(161))).all():
        raise ValueError("[BLOCKED] incomplete Medicaid replicate grid")
    central = table[table.key.eq("medicaid_covered")].set_index(["year", "group"]).relative_use
    rep0 = replicas[replicas.replicate.eq(0)].set_index(["year", "group"]).relative_use
    if (central - rep0).abs().max() > 1e-12:
        raise ValueError("[BLOCKED] Medicaid replicate 0 does not match the central grid")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    table.to_csv(args.out_dir / "historical_use.csv", index=False, lineterminator="\n", float_format="%.15g")
    replicas.to_csv(args.out_dir / "historical_use_replicates.csv", index=False,
                   lineterminator="\n", float_format="%.15g")
    manifest = dict(sources=sources, available_years={"school_age_5_17": YEARS,
                    "medicaid_covered": list(range(2019, 2025))}, school_replicates=False,
                    medicaid_replicates=160, school_year_timing="survey age in income year+1",
                    medicaid_year_timing="prior-calendar-year coverage", school_2014_weight_factor=0.5,
                    gaps="Medicaid 2005–2018 and full-sample school replicates unavailable in local extracts",
                    lineage="identified G3+ proxy; added non-identifiers unobserved")
    (args.out_dir / "use_source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"PASS: {len(table)} rows; union/other weight closure and complete available-year grids")
    print(f"seconds={time.perf_counter()-started:.3f}; peak_rss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
