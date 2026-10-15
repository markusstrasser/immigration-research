#!/usr/bin/env python3
"""Own-race district spending differentials, F-33 FY2024 x CCD SY2023-24.

Imports the fingerprinted ledger's reader/constants without changing its files.
The charge is a composition effect across districts, not a causal cost of race.
Vermont fails the ledger's 10% state-level coverage gate and has a zero charge.
Other NH races are explicitly unmeasured (zero); no parent's race is assigned to
an added child. The lineage remains on the case's own bridge.

Run before the comparator re-key:
  uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/district_prices_oct15.py
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
LEDGER = HERE.parent / "ledger_absolute_2026_09_17"
OUT = HERE / "derived/district_prices_oct15.json"
GROUPS = {"hispanic": "Hispanic/Latino", "nh_white": "White", "black": "Black or African American"}


def require(ok, why):
    if not ok:
        raise SystemExit(f"[BLOCKED] district prices: {why}")


def ledger_reader():
    spec = importlib.util.spec_from_file_location("ledger_district_oct15", LEDGER / "district_differential.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def membership(source, reader, chunksize=100_000):
    """Same indicator/sex aggregation as the ledger, with Black added.

    Chunked selection bounds memory; missing race counts become zero only after
    sum(min_count=1), exactly as in the published Hispanic/white construction.
    """
    parts = {"total": [], **{g: [] for g in GROUPS}}
    cols = ["LEAID", "RACE_ETHNICITY", "SEX", "STUDENT_COUNT", "TOTAL_INDICATOR"]
    for chunk in pd.read_csv(source, usecols=cols, chunksize=chunksize, dtype={"LEAID": str}):
        total = chunk.TOTAL_INDICATOR.eq(reader.TOTAL_INDICATOR_TOTAL)
        race = chunk.TOTAL_INDICATOR.eq(reader.TOTAL_INDICATOR_RACE)
        for group, mask in [("total", total)] + [
                (g, race & chunk.RACE_ETHNICITY.eq(label)) for g, label in GROUPS.items()]:
            selected = chunk.loc[mask, ["LEAID", "STUDENT_COUNT"]].copy()
            if len(selected):
                parts[group].append(selected)
    result = None
    for group, blocks in parts.items():
        require(bool(blocks), f"no CCD records for {group}")
        d = pd.concat(blocks, ignore_index=True)
        d["STUDENT_COUNT"] = pd.to_numeric(d.STUDENT_COUNT, errors="coerce")
        d = d.groupby("LEAID", as_index=False).STUDENT_COUNT.sum(min_count=1)
        d["LEAID"] = d.LEAID.str.strip().str.zfill(7)
        d = d.rename(columns={"STUDENT_COUNT": f"pupils_{group}"})
        result = d if result is None else result.merge(d, on="LEAID", how="left", validate="one_to_one")
    return result


def state_table(fin, mem, state_pp, reader):
    d = fin.merge(mem, on="LEAID", how="inner", validate="one_to_one")
    joined = len(d)
    missing = d.per_pupil.isna() | d.pupils_total.isna() | (d.pupils_total <= 0)
    implausible = ~missing & ~d.per_pupil.between(reader.PP_MIN, reader.PP_MAX)
    d = d.loc[~(missing | implausible)].copy()
    for group in GROUPS:
        d[f"pupils_{group}"] = d[f"pupils_{group}"].fillna(0.0)
    rows = []
    for fips, name in sorted(reader.FIPS_TO_NAME.items()):
        block = d.loc[d.fips.eq(fips)]
        require(len(block) > 0, f"no surviving districts in {name}")
        n = block.pupils_total.to_numpy()
        pp = block.per_pupil.to_numpy()
        mean = float(pp @ n / n.sum())
        ratio = mean / state_pp[name]
        passed = abs(ratio - 1) <= reader.COVERAGE_TOLERANCE
        row = dict(state=name, state_fips=fips, districts=len(block), pupils_total=float(n.sum()),
                   all_pupil_mean_per_pupil=mean, coverage_ratio=ratio, coverage_gate_passed=passed)
        for group in GROUPS:
            pupils = block[f"pupils_{group}"].to_numpy()
            require(pupils.sum() > 0, f"no {group} pupils in {name}")
            delta = float(pp @ pupils / pupils.sum() - mean)
            row.update({f"pupils_{group}": float(pupils.sum()), f"{group}_minus_all": delta,
                        f"{group}_minus_all_charged": delta if passed else 0.0})
        rows.append(row)
    counts = dict(joined=joined, dropped_missing=int(missing.sum()),
                  dropped_implausible=int(implausible.sum()), kept=len(d))
    return pd.DataFrame(rows), counts


def validate_ledger(table):
    """Require exact-method parity against all stored states, not a rounded quote."""
    old = pd.read_csv(LEDGER / "derived/district_differential_by_state.csv").set_index("state_fips")
    new = table.set_index("state_fips")
    for group, original in (("hispanic", "hispanic"), ("nh_white", "white")):
        for a, b in ((f"pupils_{group}", f"pupils_{original}"),
                     (f"{group}_minus_all", f"{original}_minus_all"),
                     (f"{group}_minus_all_charged", f"{original}_minus_all_charged")):
            require(np.allclose(new[a], old[b], atol=1e-7, rtol=0), f"stored ledger parity: {a}")
    require(np.array_equal(new.coverage_gate_passed, old.coverage_gate_passed), "coverage flags match ledger")


def build():
    reader = ledger_reader()
    params = json.loads((LEDGER / "params/params.json").read_text())
    entry = params["k12"]["f33_per_pupil_current_spending_by_state"]
    require(entry["status"] == "verified", "state summary prices are not verified")
    table, counts = state_table(reader.read_f33(), membership(reader.CCD, reader), entry["value"], reader)
    validate_ledger(table)
    national = {g: {arm: float(table[f"pupils_{g}"] @ table[f"{g}_minus_all{suffix}"] /
                                    table[f"pupils_{g}"].sum())
                       for arm, suffix in (("raw", ""), ("charged", "_charged"))} for g in GROUPS}
    sources = [reader.F33, reader.CCD, LEDGER / "district_differential.py",
               LEDGER / "params/params.json", LEDGER / "derived/district_differential_by_state.csv"]
    result = dict(case="oct15", vintage="F-33 FY2024 x CCD SY2023-24", counts=counts,
                  national_dollars_per_pupil=national, states=table.to_dict(orient="records"),
                  sources={str(p): reader.sha256(p) for p in sources},
                  unmeasured="NH other race differential and comparator school-level premium: zero, beside as asymmetries",
                  prose_anchor="RESULT_extension.md:40 reports charged national means (Vermont zeroed)")
    OUT.write_text(json.dumps(result, indent=1, sort_keys=True, allow_nan=False) + "\n")
    return result


def load():
    stored = json.loads(OUT.read_text())
    require(stored["case"] == "oct15", "wrong case")
    return stored


def per_pupil_rates(state_fips, race_groups, stored=None):
    """Own race's additive dollars per public pupil; zero for declared NH other.

    Accepted race groups follow members_coverage_oct15.race_group: hispanic,
    nh_white, black, nh_other. Unknown labels and states fail loudly.
    """
    stored = load() if stored is None else stored
    states, groups = np.asarray(state_fips), np.asarray(race_groups)
    require(states.shape == groups.shape and states.ndim == 1, "state/race vectors must align")
    require(set(groups) <= set(GROUPS) | {"nh_other"}, "unsupported race group")
    by_state = {int(r["state_fips"]): r for r in stored["states"]}
    require(set(states) <= set(by_state), "unsupported or missing state FIPS")
    return np.array([0.0 if g == "nh_other" else by_state[int(s)][f"{g}_minus_all_charged"]
                     for s, g in zip(states, groups)], dtype=float)


def adjustment_bn(state_fips, race_groups, pupil_indicator, weights, stored=None):
    """Additive spending in billions at own scenario weights and public-pupil rates.

    pupil_indicator is the October cell's public-enrollment probability (not the
    state's dollar-valued K-12 exposure). Pass replicate weights as n x r to get
    the paired replicate vector; no re-normalization is done here.
    """
    rates = per_pupil_rates(state_fips, race_groups, stored)
    pupils, weight = np.asarray(pupil_indicator, float), np.asarray(weights, float)
    require(pupils.shape == rates.shape and weight.ndim in (1, 2) and weight.shape[0] == len(rates),
            "pupil/weight vectors must align")
    require(np.isfinite(pupils).all() and ((pupils >= 0) & (pupils <= 1)).all(), "invalid pupil probability")
    require(np.isfinite(weight).all() and (weight >= 0).all(), "invalid scenario weights")
    return (pupils * rates) @ weight / 1e9


if __name__ == "__main__":
    result = build()
    print("PASS: 51-state Hispanic/white parity; own Black district differential")
    print(json.dumps(result["national_dollars_per_pupil"], sort_keys=True))
