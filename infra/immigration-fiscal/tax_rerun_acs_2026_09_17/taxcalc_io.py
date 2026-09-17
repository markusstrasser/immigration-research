"""Thin wrapper around the Policy Simulation Library Tax-Calculator.

One calculator, one call signature, used identically by the CPS and the ACS
arm so that any cross-survey difference comes from the data, not the model.

Nothing here is a hand-written tax formula: every liability comes from
`taxcalc.Calculator`. If taxcalc is unavailable the import fails loudly.
"""
from __future__ import annotations

import json
import pathlib

import numpy as np
import pandas as pd

import taxcalc  # fail loudly if missing
from taxcalc import Calculator, Policy, Records

TAX_YEAR = 2024
CHUNK = 400_000  # returns per Calculator pass; taxcalc allocates ~250 arrays

OUTPUTS = ["iitax", "payrolltax", "ptax_was", "setax", "ptax_amc",
           "c00100", "eitc", "c07220", "c11070", "standard", "c04470"]


def _varinfo() -> dict:
    p = pathlib.Path(taxcalc.__file__).parent / "records_variables.json"
    return json.loads(p.read_text())


def usable_vars() -> set[str]:
    return set(_varinfo()["read"].keys())


def check_columns(df: pd.DataFrame) -> None:
    bad = sorted(set(df.columns) - usable_vars())
    if bad:
        raise SystemExit(f"[BLOCKED] columns not readable by taxcalc Records: {bad}")


def run(df: pd.DataFrame, year: int = TAX_YEAR, chunk: int = CHUNK) -> dict[str, np.ndarray]:
    """Run current-law taxcalc on one tax-unit frame.

    `df` must carry RECID plus any subset of the usable input variables.
    Returns per-unit output arrays in the input row order.
    """
    if "RECID" not in df.columns:
        raise SystemExit("[BLOCKED] RECID missing")
    frame = df.copy()
    frame["FLPDYR"] = year
    if "s006" not in frame.columns:
        frame["s006"] = 1.0
    check_columns(frame)

    parts: list[dict[str, np.ndarray]] = []
    n = len(frame)
    for start in range(0, n, chunk):
        piece = frame.iloc[start:start + chunk].reset_index(drop=True)
        recs = Records(data=piece, start_year=year, gfactors=None, weights=None,
                       adjust_ratios=None, exact_calculations=False)
        calc = Calculator(policy=Policy(), records=recs, verbose=False)
        calc.calc_all()
        parts.append({k: np.asarray(calc.array(k), dtype=float) for k in OUTPUTS})
        del calc, recs
    out = {k: np.concatenate([p[k] for p in parts]) for k in OUTPUTS}
    if len(out["iitax"]) != n:
        raise SystemExit("[BLOCKED] taxcalc returned the wrong number of rows")
    # Employee-side payroll comparable to the Census ASEC FICA field, which
    # carries the employee half on wages plus BOTH halves of self-employment
    # contributions (gen_ledger_extension_2026_09_16/extend_ledger.py:188-190).
    out["payroll_employee_equiv"] = (0.5 * out["ptax_was"] + out["setax"] + out["ptax_amc"])
    return out


def version() -> str:
    return taxcalc.__version__
