#!/usr/bin/env python3
"""Lane-local EITC repair and canonical survivor federal high-AGI recomputation.

The high-AGI receipt arm retains the adopted split: observed positive federal
liability and a fixed positive BEA residual, the latter on unadjusted liability
of AGI >= $500,000 returns. It is not an IRS-raked liability scenario.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
INPUTS = LANE / "inputs"
OUT = LANE / "derived"
PDF = INPUTS / "tax_corrections_irs_p596_2024.pdf"
TEXT = INPUTS / "tax_corrections_irs_p596_2024.txt"
TABLE = INPUTS / "tax_corrections_eitc_table_2024.csv"
PINS = INPUTS / "tax_corrections_pins.json"
URL = "https://www.irs.gov/pub/irs-prior/p596--2024.pdf"
EITC = {
    0: (.0765, 632., .0765, 10330., 17250.),
    1: (.34, 4213., .1598, 22720., 29640.),
    2: (.40, 6960., .2106, 22720., 29640.),
    3: (.45, 7830., .2106, 22720., 29640.),
}


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def parse_irs_table(text):
    """Parse both physical table halves, retaining PDF page and original row."""
    rows = []
    for page, section in enumerate(text.split("\f"), 1):
        if "Earned Income Credit (EIC)" not in section or "Your credit is" not in section:
            continue
        for line in section.splitlines():
            tokens = line.split()
            if len(tokens) not in (10, 20) or not all(re.fullmatch(r"[\d,]+|\*{1,2}", t) for t in tokens):
                continue
            values = [int(t.replace(",", "")) if t not in ("*", "**") else t for t in tokens]
            for start in range(0, len(values), 10):
                half = values[start:start + 10]
                lower, upper = half[:2]
                if not (upper > lower and upper - lower <= 50):
                    raise ValueError("[BLOCKED] malformed IRS EITC table income interval")
                for joint in (False, True):
                    for kids in range(4):
                        credit = half[2 + 4 * int(joint) + kids]
                        if isinstance(credit, str):
                            # Eight terminal cells direct to income-dependent
                            # page footnotes; preserve them in the source text.
                            # They cannot be represented as one constant credit
                            # on the table's $50 interval and are not used as
                            # continuous-midpoint regression observations.
                            continue
                        rows.append({"income_at_least": lower, "income_less_than": upper,
                                     "joint": int(joint), "kids": kids,
                                     "credit": credit,
                                     "pdf_page": page, "source_row": line.strip()})
    frame = pd.DataFrame(rows).sort_values(["income_at_least", "joint", "kids"])
    if len(frame) < 10000 or frame.duplicated(["income_at_least", "joint", "kids"]).any():
        raise ValueError("[BLOCKED] incomplete or duplicated IRS EITC table")
    return frame


def register_sources(refresh_parsed=False):
    """Explicit registration only; runtime never silently renews a source pin."""
    if PINS.exists() and not refresh_parsed:
        raise ValueError("[BLOCKED] source pins already exist; verify rather than replace")
    previous = verify_sources() if PINS.exists() else None
    if not PDF.exists() or not TEXT.exists():
        raise ValueError("[BLOCKED] download IRS Pub 596 (2024) and pdftotext -layout first")
    frame = parse_irs_table(TEXT.read_text())
    frame.to_csv(TABLE, index=False, lineterminator="\n")
    write_json(PINS, {"primary_url": URL, "tax_year": 2024,
                      "locator": "Publication 596 (2024), EIC table, printed pp. 28-38",
                      "parsed_rows": len(frame),
                      "omitted_cells": "eight starred terminal cells refer to within-interval footnotes; original rows and footnotes preserved in primary PDF/text",
                      "prior_parsed_pin": previous,
                      "files": {p.name: sha(p) for p in (PDF, TEXT, TABLE)}})


def verify_sources():
    pins = json.loads(PINS.read_text())
    for name, digest in pins["files"].items():
        if sha(INPUTS / name) != digest:
            raise ValueError(f"[BLOCKED] stale tax correction source: {name}")
    return pins


def corrected_eitc(kids, earned, agi, joint, investment, age_ok):
    """Section 32: min(phase-in credit, maximum less phase-out), floored at 0.

    This is the continuous statutory schedule; IRS tables use income intervals
    and whole-dollar rounding. The regression uses interval midpoints and
    separately tests low earnings / high AGI, where the former formula fails.
    """
    kids, earned, agi, joint, investment, age_ok = np.broadcast_arrays(
        np.minimum(np.asarray(kids, int), 3), np.asarray(earned, float),
        np.asarray(agi, float), np.asarray(joint, bool),
        np.asarray(investment, float), np.asarray(age_ok, bool))
    result = np.zeros(earned.shape)
    for n, (pin, maximum, pout, single_start, joint_start) in EITC.items():
        phase_in = np.minimum(pin * np.maximum(earned, 0), maximum)
        threshold = np.where(joint, joint_start, single_start)
        phase_out = maximum - pout * np.maximum(np.maximum(earned, agi) - threshold, 0)
        credit = np.maximum(np.minimum(phase_in, phase_out), 0)
        if n == 0:
            credit = np.where(age_ok, credit, 0)
        result = np.where(kids == n, credit, result)
    return np.where(investment > 11600, 0, result)


def corrected_taxcalc_compute(module, agi, earned, investment, status, kids17,
                              kids19, other_dep, aged, head_age):
    """Keep frozen simplified tax/ACTC, replace only its defective EITC operator."""
    original = getattr(module, "_tax_corrections_original_compute", module.compute)
    fed, _, actc = original(agi, earned, investment, status, kids17, kids19,
                            other_dep, aged, head_age)
    credit = corrected_eitc(kids19, earned, agi, np.asarray(status) == "joint",
                            investment, (np.asarray(head_age) >= 25) & (np.asarray(head_age) <= 64))
    return fed, credit, actc


def install_eitc_fix(module):
    """In-memory patch for callers using frozen taxcalc; never edits that source."""
    if not hasattr(module, "_tax_corrections_original_compute"):
        module._tax_corrections_original_compute = module.compute
        module.compute = lambda *args, **kwargs: corrected_taxcalc_compute(module, *args, **kwargs)
    return module


def assert_eitc_used(tax_module):
    """Fail-loud probe of the actual survivor kernel against the pinned IRS table.

    The fixture has earned income well below the maximum-credit earnings level,
    and AGI above phase-out start. The bad subtraction formula is over $300 low;
    the correct result is the smaller of the two IRS table lookups. TAXSIM's
    continuous schedule differs from table interval rounding by only $0.50.
    """
    verify_sources()
    frame = pd.DataFrame({"year": [2024], "mstat": [1], "statefip": [6],
                          "page": [40], "sage": [0], "depx": [1], "dep13": [1],
                          "dep17": [1], "dep18": [1], "pwages": [5025.],
                          "swages": [0], "psemp": [0], "ssemp": [0],
                          "dividends": [0], "intrec": [0], "ltcg": [0],
                          "otherprop": [0], "pensions": [20000.], "gssi": [0],
                          "pui": [0], "sui": [0]})
    output = tax_module.run_taxsim(frame)
    table = pd.read_csv(TABLE)
    earnings_credit = table.query("income_at_least == 5000 and joint == 0 and kids == 1").credit.item()
    agi_credit = table.query("income_at_least == 25000 and joint == 0 and kids == 1").credit.item()
    expected = min(earnings_credit, agi_credit)
    actual = float(output.v25.iloc[0])
    if abs(actual - expected) > .51:
        raise ValueError(f"[BLOCKED] actual survivor kernel EITC fails IRS table: {actual} vs {expected}")
    return {"passed": True, "IRS_table_credit_usd": int(expected),
            "kernel_credit_usd": actual, "table_rounding_difference_usd": actual - expected,
            "source": URL, "earnings": 5025., "AGI": float(output.v10.iloc[0])}


def high_agi_delta(after_liability, after_agi, after_factor, after_live, after_weights,
                   before_liability, before_agi, before_factor, before_live, before_weights,
                   owner, national_liability_bn, national_ruled_key, national_high_key,
                   national_line_bn, booked_item_receipts):
    """3 x 161 cost delta, subtracting the already-booked item exactly once.

    Only the old item's subtraction uses its frozen booked scenario scaling.
    Both newly simulated flows are recomputed on the survivor's own return.
    The adopted high-AGI key is unadjusted by on-books flags; its liability part
    uses the survivor's own factor, matching the audited row-3 decomposition.
    """
    national_ruled_key = np.asarray(national_ruled_key, float)
    national_high_key = np.asarray(national_high_key, float)
    if np.any(national_ruled_key <= 0) or np.any(national_high_key <= 0):
        raise ValueError("[BLOCKED] federal high-AGI arm nonpositive national key")
    residual_bn = national_line_bn - national_liability_bn
    if residual_bn < 0:
        raise ValueError("[BLOCKED] federal high-AGI arm requires positive national residual")
    after_raw = np.asarray(after_liability) * after_live
    before_raw = np.asarray(before_liability) * before_live
    after_liab = after_raw * after_factor
    before_liab = before_raw * before_factor
    after_high = after_raw * (np.asarray(after_agi) >= 500000)
    before_high = before_raw * (np.asarray(before_agi) >= 500000)
    nold = len(before_raw)
    weighted = lambda values, own, weights: np.stack([(values * own[g]) @ weights for g in range(3)])
    liab_change = (weighted(after_liab, owner, after_weights)
                   - weighted(before_liab, owner[:, :nold], before_weights))
    high_change = (weighted(after_high, owner, after_weights)
                   - weighted(before_high, owner[:, :nold], before_weights))
    result = (national_liability_bn * liab_change / national_ruled_key
              + residual_bn * high_change / national_high_key - booked_item_receipts)
    direct = (national_liability_bn * (after_liab @ after_weights - before_liab @ before_weights)
              / national_ruled_key + residual_bn * (after_high @ after_weights - before_high @ before_weights)
              / national_high_key - booked_item_receipts.sum(axis=0))
    closure = float(np.max(np.abs(result.sum(axis=0) - direct)))
    if closure > 1e-6:
        raise ValueError(f"[BLOCKED] federal high-AGI generation closure: {closure}")
    return result, {"national_observed_liability_bn": float(national_liability_bn),
                    "national_positive_residual_bn": float(residual_bn),
                    "generation_closure_bn": closure,
                    "liability_delta_bn": float((national_liability_bn * liab_change / national_ruled_key).sum(axis=0)[0]),
                    "high_AGI_residual_delta_bn": float((residual_bn * high_change / national_high_key).sum(axis=0)[0]),
                    "booked_item_subtraction_bn": float(booked_item_receipts.sum(axis=0)[0])}


def federal_high_agi(c, x, d, federal, *, after_output=None, removal_module=None):
    """Integration hook after removal.federal_removal; returns M1_high_agi.

    Required federal fields are the shared canonical after_input, after_federal,
    afterR, own, owner. It never recreates dependent membership or care inputs.
    """
    if removal_module is None:
        removal_module = load(LANE / "removal.py", "tax_corrections_removal_hook")
    tax = load(LANE / "state_tax.py", "tax_corrections_state_hook")
    after = tax.run_taxsim(federal["after_input"]) if after_output is None else after_output
    R, W, civ, union = (x[k] for k in ("R", "W", "civ", "union"))
    h = R.row.to_numpy(int)
    own = np.asarray(federal["own"], int)
    safe = np.maximum(own, 0)
    live = (own >= 0) & civ[safe]
    live[:len(R)] &= x["civ_ok"]
    # Continuing claimants retain their published AGI residual, just as M1
    # retains their published liability residual. Removing dependents changes
    # credits/status, not that claimant's own reported income. Only re-filed
    # mixed spouses and newly created claimant returns receive kernel AGI.
    spouse = R.spouse.to_numpy(int)
    joint_mixed = (spouse >= 0) & (union[h] != union[np.maximum(spouse, 0)])
    anchored = np.zeros(len(own), bool)
    anchored[:len(R)] = ~union[h] & ~joint_mixed
    after_agi = after.v10.to_numpy().copy()
    after_agi[anchored] = x["base"].agi[anchored[:len(R)]]
    factor = np.where(x["flag"], x["onbooks"]["central"], 1.)
    raw = d.FEDTAX_BC.to_numpy(float)
    high = raw * d.AGI.ge(500000).to_numpy()
    national_observed = float(raw[civ] @ W[civ, 0]) / 1e9
    # Keep original row-3 benchmark pools; each key's sampling denominator varies
    # with the same replicate as its numerator, as in combine_onbooks_lane.
    nliab = (raw[civ] * factor[civ]) @ W[civ]
    nhi = high[civ] @ W[civ]
    line = next(v for v in x["model"]["receipts"]["lines"] if v["id"] == "federal_income_tax")
    reference = x["model"]["receipts"]["reference"]
    # This factor is only the already-recorded item, not survivor recomputation.
    booked_scale = (line["cells"]["federal_gap_high_agi"]["personal"]["target_bn"]
                    / line["cells"][reference]["personal"]["target_bn"])
    item = removal_module.original_item_parts(x)["receipts"] * booked_scale
    result, details = high_agi_delta(
        federal["after_federal"], after_agi, factor[safe], live, W[safe],
        x["base"].fedbc, x["base"].agi, x["f_other"], (~union[h]) & x["civ_ok"], x["wr"],
        np.asarray(federal["owner"]), national_observed, nliab, nhi,
        line["national_bn"], item)
    details.update({"booked_item_scenario_scale": float(booked_scale),
                    "recommendation": "arm", "scope": "identified union; added-person extension is external",
                    "rule": "raw liability plus positive BEA gap on AGI>=500k; own survivor return and factors; unruled high key retained",
                    "replicates": 160, "status": "conditional TAXSIM re-filing; baseline subtraction exact"})
    return {"M1_high_agi": result, "details": details, "after_agi": after_agi}


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_results(c, federal, high, kernel_gate):
    """Serialize the shared computed result without rerunning the CPS account."""
    rows = []
    vectors = {"M1_IRS": federal["M1"], "M3": federal["M3"],
               "M1_high_agi": high["M1_high_agi"],
               "M1_high_agi_vs_scalar": high["M1_high_agi"] - federal["M1"] * high["details"]["booked_item_scenario_scale"]}
    for name, v in vectors.items():
        for i, gen in enumerate(("G1", "G2", "G3+", "all")):
            a = v.sum(axis=0) if gen == "all" else v[i]
            rows.append({"component": name, "generation": gen, "delta_bn": float(a[0]), "replicate_se_bn": c.sdr(a)})
    pd.DataFrame(rows).to_csv(OUT / "tax_corrections_results.csv", index=False, lineterminator="\n")
    pd.DataFrame([{"component": n, "generation": g, **{f"r{k}": float(v[i, k]) for k in range(161)}}
                  for n, v in vectors.items() for i, g in enumerate(("G1", "G2", "G3+"))]).to_csv(
                      OUT / "tax_corrections_replicates.csv", index=False, lineterminator="\n")
    high["details"].update({"IRS_M1_details": federal["details"], "source_pins": verify_sources(),
                            "survivor_EITC_primary_table_gate": kernel_gate})
    write_json(OUT / "tax_corrections_audit.json", high["details"])
    return rows


def run():
    verify_sources()
    start = time.perf_counter()
    removal = load(LANE / "removal.py", "tax_corrections_removal")
    tax = load(LANE / "state_tax.py", "tax_corrections_eitc_kernel")
    kernel_gate = assert_eitc_used(tax)
    c, x = removal.positive_control()
    d = removal.add_fields(x["d"], c)
    federal = removal.federal_removal(c, x, d)
    high = federal_high_agi(c, x, d, federal, removal_module=removal)
    rows = write_results(c, federal, high, kernel_gate)
    print(json.dumps({"results": rows, "seconds": time.perf_counter() - start,
                      "self_maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
                      "child_maxrss_bytes": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--register-sources", action="store_true")
    parser.add_argument("--refresh-parsed", action="store_true")
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    if args.register_sources:
        register_sources()
    elif args.refresh_parsed:
        register_sources(refresh_parsed=True)
    elif args.run:
        run()
    else:
        print(json.dumps(verify_sources(), indent=2))
