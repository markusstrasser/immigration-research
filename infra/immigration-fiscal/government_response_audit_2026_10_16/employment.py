#!/usr/bin/env python3
"""Independent administrative staffing/payroll cross-section; never causal.

--data-root is the repository holding pinned original sources, not a raw folder.
Actual full-time employees and their March payroll are primary. FTE is modeled
by Census since 2019 and is retained only as a secondary comparison.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from raw_finance import dump_json, fit_hc3, parse_population, sha256, write_csv


SOURCE_DIR = "sources/immigration-fiscal/data/external/stage3/census/aspep_2022"
SOURCES = {
    "states": (f"{SOURCE_DIR}/aspep2022-state-ft-api.json", "bcd7b8f1cacd504a0dd867a149ffd3d165a46fbad102f927c609d33162a1c1a9"),
    "national": (f"{SOURCE_DIR}/aspep2022-national-ft-api.json", "61bf2438f069ec7356d2798da4bca2467ef90273a659e0230370c09bfe9895ad"),
    "population": ("sources/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv", "b8b50bd345d8a5f33d5c8a28c95aeaa0a50971356f000d9b48276a65fd9022a7"),
    "methodology": (f"{SOURCE_DIR}/22_methodology.pdf", "f08593fe7bcf2fe27f3cd4c69140b6844c119aff60c02ef20f604da952fd063b"),
    "technical_documentation": (f"{SOURCE_DIR}/2022 COG-E Individual Unit File Tech Doc.pdf", "445bc3d598aa68b1592061f7479954179ff11c424dd414670c0284b36745af23"),
    "classification": (f"{SOURCE_DIR}/2006_classification_manual.pdf", "5dcda9efc6fcab9dd10cfcc500995cb1f5b29b977aaf2b124f127ab3fb92d429"),
}
FUNCTIONS = {"EP0045": "Financial Administration", "EP0085": "Other Government Administration"}
FIELDS = {"FT_EMP": "ft_employees", "FT_PAY": "ft_payroll_march_dollars", "PT_EMP": "pt_employees",
          "PT_PAY": "pt_payroll_march_dollars", "FTE": "fte_modeled"}
OUTCOMES = ["ft_employees", "ft_payroll_march_dollars", "ft_pay_per_employee_march_dollars", "fte_modeled"]
METHOD = {
    "estimand": "Cross-state association of population with administrative full-time staffing and March payroll, not a causal population-removal response.",
    "year": 2022,
    "population": "Census Vintage2024 July2022 estimate; March staffing is not simultaneous with July population.",
    "primary": "Employer-defined full-time employee count and 31-day March full-time gross payroll in current dollars. Reported records subject to Census editing and nonresponse imputation; not universally unimputed direct observations.",
    "secondary": "FTE is modeled since2019 from historical 2014-18 relationships and current full-/part-time counts; do not label it an independent measured hours quantity.",
    "baskets": "Finance (EP0045, manual function23) and finance+other administration (EP0045+EP0085, functions23+29). Exclude judiciary and unallocable; building staff cannot be separately identified.",
    "fits": "Intercept plus log population, all50 and lower48, equal-state and population weights; log FT count, log FT payroll, log FT payroll/count, and log modeled FTE. No trimming. Population weights change descriptive emphasis and are not inverse-variance weights.",
    "uncertainty": "HC3 WLS sandwich, t(N-2) intervals; model uncertainty, not Census sampling error or causal-transport uncertainty. 2022 is a census year.",
    "decomposition": "With identical rows/design/weights, payroll beta equals staffing beta plus pay-per-worker beta. Pay per worker includes occupational mix, hours/overtime and bonuses and is not a constant-quality wage index.",
    "limits": "No employer benefit costs, contractors, purchased services or capital in payroll. Full-time definitions vary by employer. Some nonresponse imputation scales donors by population. State organization, outsourcing, service choices and geography remain confounders.",
    "total_checks": "Published state/DC aggregate sums versus national and combined versus state+local. Employee counts exact; dollar payroll allows <=52 dollars for 51 rounded state totals; modeled FTE permits 52 persons across states and 2 within state.",
}


def load_api(path: Path) -> list[dict]:
    table = json.loads(path.read_text())
    if not isinstance(table, list) or len(table) < 2 or not isinstance(table[0], list):
        raise ValueError("[BLOCKED] Census API did not return a nonempty table")
    header, records = table[0], []
    required = {"NAME", "AGG_DESC", "AGG_DESC_LABEL", "GOVTYPE", "GOVTYPE_LABEL", "YEAR", "time", *FIELDS}
    if not required <= set(header):
        raise ValueError("[BLOCKED] API fields missing")
    for values in table[1:]:
        if len(values) != len(header):
            raise ValueError("[BLOCKED] API row width differs from header")
        record = {}
        for key, value in zip(header, values):
            if key in record and record[key] != value:
                raise ValueError(f"[BLOCKED] duplicate API header disagrees: {key}")
            record[key] = value
        if record["YEAR"] != "2022" or record["time"] != "2022":
            raise ValueError("[BLOCKED] wrong API year")
        records.append(record)
    return records


def integer(value: str) -> int:
    if not isinstance(value, str) or not value.isdigit():
        raise ValueError(f"[BLOCKED] missing/flagged/negative employment amount: {value!r}")
    return int(value)


def parse_employment(state_path: Path, national_path: Path, populations: dict) -> tuple[list[dict], list[dict]]:
    states, national = load_api(state_path), load_api(national_path)
    state_rows, us_rows = {}, {}
    for rows, index, geography in [(states, state_rows, "state"), (national, us_rows, "us")]:
        for row in rows:
            if row["AGG_DESC"] not in FUNCTIONS:
                continue
            if row["AGG_DESC_LABEL"] != FUNCTIONS[row["AGG_DESC"]]:
                raise ValueError("[BLOCKED] function label changed")
            expected_label = {"001": "State and Local", "002": "State", "003": "Local"}.get(row["GOVTYPE"])
            if row["GOVTYPE_LABEL"] != expected_label or geography not in row:
                raise ValueError("[BLOCKED] government/geography mapping changed")
            if geography == "us" and (row["us"] != "1" or row["NAME"] != "United States"):
                raise ValueError("[BLOCKED] national geography changed")
            key = (row[geography], row["GOVTYPE"], row["AGG_DESC"])
            if key in index:
                raise ValueError("[BLOCKED] duplicate employment geography/function")
            index[key] = {**row, **{field: integer(row[field]) for field in FIELDS}}
    if len(state_rows) != 304 or len(us_rows) != 6:
        raise ValueError("[BLOCKED] incomplete employment state/government/function frame")
    expected_fips = {r["state_fips"] for r in populations.values()}
    checks = []

    def check(name, residual, tolerance):
        checks.append({"identity": name, "residual": residual, "tolerance": tolerance})
        if abs(residual) > tolerance:
            raise ValueError(f"[BLOCKED] {name}: residual {residual} exceeds {tolerance}")

    for function in FUNCTIONS:
        for gov in ["001", "002", "003"]:
            selected = [r for (state, g, f), r in state_rows.items() if g == gov and f == function]
            wanted = expected_fips - ({"11"} if gov == "002" else set())
            if {r["state"] for r in selected} != wanted:
                raise ValueError("[BLOCKED] state FIPS frame changed")
            for field in FIELDS:
                tolerance = 52 if field in {"FT_PAY", "PT_PAY", "FTE"} else 0
                check(f"{function} gov{gov} {field}: states/DC minus US", sum(r[field] for r in selected) - us_rows[("1", gov, function)][field], tolerance)
        for fips in sorted(expected_fips):
            combined = state_rows[(fips, "001", function)]
            local = state_rows[(fips, "003", function)]
            state = state_rows.get((fips, "002", function))
            for field in FIELDS:
                tolerance = 2 if field in {"FT_PAY", "PT_PAY", "FTE"} else 0
                check(f"{fips} {function} {field}: combined minus state minus local", combined[field] - local[field] - (state[field] if state else 0), tolerance)
    records = []
    for name, pop in sorted(populations.items()):
        fips = pop["state_fips"]
        for basket, codes in [("finance", ["EP0045"]), ("finance_and_other_admin", list(FUNCTIONS))]:
            parts = [state_rows[(fips, "001", code)] for code in codes]
            if any(r["NAME"] != name for r in parts):
                raise ValueError("[BLOCKED] population/employment state name mismatch")
            values = {label: sum(r[field] for r in parts) for field, label in FIELDS.items()}
            if any(values[key] <= 0 for key in ["ft_employees", "ft_payroll_march_dollars", "fte_modeled"]):
                raise ValueError("[BLOCKED] nonpositive log outcome")
            values["ft_pay_per_employee_march_dollars"] = values["ft_payroll_march_dollars"] / values["ft_employees"]
            records.append({"state": name, **pop, "basket": basket, **values})
    return records, checks


def estimate(records: list[dict]) -> tuple[list[dict], list[dict]]:
    fits, decompositions = [], []
    for basket in ["finance", "finance_and_other_admin"]:
        for sample, excluded in [("all50", {"11"}), ("lower48", {"02", "11", "15"})]:
            selected = [r for r in records if r["basket"] == basket and r["state_fips"] not in excluded]
            expected_n = 50 if sample == "all50" else 48
            if len(selected) != expected_n:
                raise ValueError("[BLOCKED] wrong regression sample size")
            pop = np.array([r["population_2022"] for r in selected])
            for weighting, weights in [("equal_state", np.ones(len(pop))), ("population", pop)]:
                slopes = {}
                for outcome in OUTCOMES:
                    result = fit_hc3(np.log([r[outcome] for r in selected]), np.log(pop), weights)
                    fits.append({"basket": basket, "sample": sample, "weight": weighting, "outcome": outcome,
                                 "evidence": "secondary_modeled_FTE" if outcome == "fte_modeled" else "primary_reported_edited_imputed", **result})
                    slopes[outcome] = result["beta"]
                residual = slopes["ft_payroll_march_dollars"] - slopes["ft_employees"] - slopes["ft_pay_per_employee_march_dollars"]
                if abs(residual) > 1e-10:
                    raise ValueError("[BLOCKED] payroll/staff/pay-per-worker decomposition failed")
                decompositions.append({"basket": basket, "sample": sample, "weight": weighting,
                                       "payroll_beta": slopes["ft_payroll_march_dollars"], "staffing_beta": slopes["ft_employees"],
                                       "pay_per_worker_beta": slopes["ft_pay_per_employee_march_dollars"], "residual": residual})
    return fits, decompositions


def run(data_root: Path, out_dir: Path) -> None:
    provenance = {}
    for key, (relative, expected) in SOURCES.items():
        path = data_root / relative
        if not path.is_file() or sha256(path) != expected:
            raise ValueError(f"[BLOCKED] missing/stale original {relative}")
        provenance[key] = {"path": relative, "sha256": expected}
    populations, pop_checks = parse_population(data_root / SOURCES["population"][0])
    records, checks = parse_employment(data_root / SOURCES["states"][0], data_root / SOURCES["national"][0], populations)
    fits, decomposition = estimate(records)
    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "employment_states.csv", records)
    write_csv(out_dir / "employment_fits.csv", fits)
    write_csv(out_dir / "employment_decomposition.csv", decomposition)
    dump_json(out_dir / "employment_checks.json", pop_checks + checks)
    dump_json(out_dir / "employment_sources.json", provenance)
    dump_json(out_dir / "employment_method.json", METHOD)
    print(f"Validated 51 state/DC source totals; wrote {len(fits)} descriptive fits and {len(decomposition)} exact payroll decompositions.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    run(args.data_root.resolve(), args.out_dir.resolve())
