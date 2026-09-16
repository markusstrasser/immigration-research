#!/usr/bin/env python3
"""Extend the annual partial fiscal ledger by origin-generation with the three
omitted items the peer ledger names: employer-side payroll tax, state/local
sales and excise tax, residential property tax, and the K-12 schooling cost of
the resource unit's children.

Reuses analyze_cps_fiscal_2025.py end to end: the same CPS ASEC 2025 public-use
file, the same SPM resource-unit conservation checks, the same equal-shares
allocation rules, the same 160-replicate SDR variance, the same generation group
definitions (parents' birthplace PEFNTVTY/PEMNTVTY, self-identified Mexican
origin PRDTHSP, third-plus non-Hispanic white).

Everything added here is an accounting scenario built from published aggregate
rates, not a measured payment. Run with --help for inputs.
"""
from __future__ import annotations

import os
import subprocess
import sys

# `uv run python3 extend_ledger.py` uses a bare interpreter with no project
# dependencies (this repo has no pyproject). Re-exec once through uv with the
# needed wheels so the documented verification command works as written.
if os.environ.get("_EXTEND_LEDGER_BOOTSTRAPPED") != "1":
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        env = dict(os.environ, _EXTEND_LEDGER_BOOTSTRAPPED="1")
        cmd = ["uv", "run", "--with", "numpy>=2", "--with", "pandas>=2",
               "python3", os.path.abspath(__file__), *sys.argv[1:]]
        sys.exit(subprocess.call(cmd, env=env))

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import urllib.request  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "build"))

# Extra person fields the base generator does not read. PERSON is consumed by
# prepare() as usecols at call time, so extending it here is enough.
import analyze_cps_fiscal_2025 as base  # noqa: E402

EXTRA_PERSON = ["WSAL_VAL", "SPM_RESOURCES"]
for _f in EXTRA_PERSON:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

from analyze_cps_fiscal_2025 import CASH, NONCASH, TAX, allocate, estimate, prepare, summarize  # noqa: E402

CPS_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"

GROUPS = ["third_plus_nh_white", "all_native", "all_second_gen", "mexican_second_gen",
          "mexican_third_plus_selfid", "mexico_born"]
REFERENCE = "third_plus_nh_white"

# --- published parameters -------------------------------------------------
# IRS Publication 15 (2024), p. 2: "The social security wage base limit is
# $168,600." https://www.irs.gov/pub/irs-prior/p15--2024.pdf
OASDI_CAP_2024 = 168_600.0
OASDI_RATE = 0.062          # employer share, OASDI
HI_RATE = 0.0145            # employer share, hospital insurance, uncapped

# Brief's consumption model: taxable consumption = min(income, 0.9 x income)
# x taxable share. For nonnegative income min(y, .9y) = .9y.
CONSUMPTION_OF_INCOME = 0.90
TAXABLE_SHARES = {"share25": 0.25, "share35": 0.35, "share45": 0.45}

# ITEP, Who Pays? 7th edition (Jan 2024), national sales-and-excise tax as a
# share of income: lowest 20% 7.0%, middle 20% 4.8%, top 1% 1.0% (published).
# https://itep.org/whopays-7th-edition/
# Q2, Q4 and Q5 are interpolated/extrapolated between those published anchors
# and are [INFERENCE], not ITEP figures.
ITEP_QUINTILE_RATES = np.array([0.070, 0.059, 0.048, 0.040, 0.030])

# Renter property-tax pass-through: 15% of annual contract rent, proxied by the
# state median gross rent (ACS 2023 1-year B25064) because CPS ASEC carries no
# rent amount.
RENTER_PASSTHROUGH = 0.15

# Public K-12 pupils per child aged 5-17, measured on ACS 2024 PUMS by the
# repo's own measure_acs_school_exposure_2024.py (pupil / child, equal-shares
# among all household members): native households 0.10154/0.12650 = 0.8027;
# Mexico-born households 0.16179/0.17881 = 0.9048.
PUPIL_RATIO_NATIVE_ACS = 0.10154357210318846 / 0.12650232227317687
PUPIL_RATIO_MEXICO_BORN_ACS = 0.16178869960800024 / 0.17881410371659756
PUPIL_RATIO_FLAT = 0.90
PUPIL_RATIO_DIFFERENTIAL = {
    "third_plus_nh_white": PUPIL_RATIO_NATIVE_ACS,
    "all_native": PUPIL_RATIO_NATIVE_ACS,
    "all_second_gen": PUPIL_RATIO_NATIVE_ACS,
    "mexican_second_gen": PUPIL_RATIO_MEXICO_BORN_ACS,
    "mexican_third_plus_selfid": PUPIL_RATIO_MEXICO_BORN_ACS,
    "mexico_born": PUPIL_RATIO_MEXICO_BORN_ACS,
}


def resolve_cps_zip(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.exists():
            raise SystemExit(f"[BLOCKED] --cps-zip not found: {explicit}")
        return explicit
    candidates = []
    if os.environ.get("CPS_ASEC_2025_ZIP"):
        candidates.append(Path(os.environ["CPS_ASEC_2025_ZIP"]))
    root = os.environ.get("PNY_DATA_ROOT")
    if root:
        candidates.append(Path(root) / "external/stage3/census/cps_asec_2025/asecpub25csv.zip")
    candidates.append(Path("/Volumes/2TBPNY/research-data/immigration-fiscal/data/"
                           "external/stage3/census/cps_asec_2025/asecpub25csv.zip"))
    cache = HERE / "_cache" / "asecpub25csv.zip"
    candidates.append(cache)
    for c in candidates:
        if c.exists():
            return c
    cache.parent.mkdir(parents=True, exist_ok=True)
    print(f"[stage] CPS ASEC 2025 public file not found locally; downloading {CPS_URL}", flush=True)
    urllib.request.urlretrieve(CPS_URL, cache)
    h = hashlib.sha256(cache.read_bytes()).hexdigest()
    if h != CPS_SHA:
        raise SystemExit(f"[BLOCKED] downloaded CPS zip sha256 {h} != expected {CPS_SHA}")
    return cache


def sdr(values: np.ndarray) -> tuple[float, float]:
    """Point estimate and 160-replicate SDR standard error, as the generator."""
    values = np.asarray(values, dtype=float)
    return float(values[0]), float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def weighted_quintile_codes(value: np.ndarray, weight: np.ndarray) -> np.ndarray:
    order = np.argsort(value, kind="stable")
    cum = np.cumsum(weight[order]) / weight.sum()
    code = np.empty(len(value), dtype=int)
    code[order] = np.clip((cum * 5).astype(int), 0, 4)
    return code


def build(args):
    cps = resolve_cps_zip(args.cps_zip)
    print(f"[stage] CPS ASEC 2025 source: {cps}", flush=True)
    d, heads, index, validation = prepare(cps)
    n_units = len(heads)
    units = d.groupby("SPM_ID", sort=True)

    with zipfile.ZipFile(cps) as z:
        hh = pd.read_csv(z.open("hhpub25.csv"),
                         usecols=["H_SEQ", "GESTFIPS", "H_TENURE", "HPROP_VAL"])
    merged = d[["PH_SEQ"]].merge(hh, left_on="PH_SEQ", right_on="H_SEQ",
                                 how="left", validate="many_to_one")
    if merged.H_SEQ.isna().any():
        raise ValueError("Person record without a household record")
    d = d.assign(GESTFIPS=merged.GESTFIPS.to_numpy(),
                 H_TENURE=merged.H_TENURE.to_numpy(),
                 HPROP_VAL=merged.HPROP_VAL.to_numpy())
    if not d.groupby("SPM_ID").SPM_RESOURCES.nunique().eq(1).all():
        raise ValueError("SPM_RESOURCES is not constant inside a resource unit")

    params = pd.read_csv(HERE / "state_parameters.csv").set_index("fips")
    missing = sorted(set(d.GESTFIPS.unique()) - set(params.index))
    if missing:
        raise ValueError(f"State parameters missing for FIPS {missing}")
    sales_rate = d.GESTFIPS.map(params.combined_sales_tax_rate).to_numpy(dtype=float)
    prop_rate = d.GESTFIPS.map(params.property_tax_effective_rate).to_numpy(dtype=float)
    rent_month = d.GESTFIPS.map(params.median_gross_rent_monthly).to_numpy(dtype=float)
    per_pupil = d.GESTFIPS.map(params.per_pupil_current_spending).to_numpy(dtype=float)

    # ---- baseline unit totals, identical to analyze_cps_fiscal_2025.run ----
    totals = {k: units[v].sum().to_numpy(dtype=float) for k, v in (TAX | CASH).items()}
    totals.update({k: heads[v].to_numpy(dtype=float) for k, v in NONCASH.items()})
    totals["modeled_tax_total"] = (totals["payroll"] + totals["federal_after_refundable"]
                                  + totals["state_after_credits"])
    totals["selected_cash_total"] = sum(totals[k] for k in CASH)
    totals["selected_noncash_total"] = sum(totals[k] for k in NONCASH)
    totals["cash_noncash_tax_balance"] = (totals["modeled_tax_total"] - totals["selected_cash_total"]
                                          - totals["selected_noncash_total"])

    # ---- (C) employer-side payroll tax ------------------------------------
    # Employer OASDI + HI on wage and salary earnings only. Self-employment
    # contributions already carry both halves inside the Census FICA field, so
    # SEMP/FRSE earnings are deliberately excluded to avoid double counting.
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(dtype=float)
    employer_person = OASDI_RATE * np.minimum(wage, OASDI_CAP_2024) + HI_RATE * wage
    totals["employer_payroll"] = np.bincount(index, weights=employer_person, minlength=n_units)

    # ---- (D1) sales and excise tax ----------------------------------------
    unit_resources = heads.SPM_RESOURCES.to_numpy(dtype=float).clip(min=0)
    head_order = d.loc[d.SPM_HEAD.eq(1)].sort_values("SPM_ID").index.to_numpy()
    unit_sales_rate = sales_rate[head_order]
    for name, share in TAXABLE_SHARES.items():
        totals[f"sales_tax_{name}"] = (unit_sales_rate * CONSUMPTION_OF_INCOME
                                       * unit_resources * share)
    unit_weight = heads.pwwgt0.to_numpy(dtype=float) * heads.SPM_NUMPER.to_numpy(dtype=float)
    q = weighted_quintile_codes(unit_resources, unit_weight)
    totals["sales_tax_itep"] = ITEP_QUINTILE_RATES[q] * unit_resources

    # ---- (D2) residential property tax ------------------------------------
    household_members = d.groupby("PH_SEQ").PPPOS.transform("size").to_numpy(dtype=float)
    owner = d.H_TENURE.eq(1).to_numpy()
    owner_tax_person = np.where(owner, prop_rate * d.HPROP_VAL.to_numpy(dtype=float), 0.0) / household_members
    renter = d.H_TENURE.eq(2).to_numpy()
    renter_tax_person = np.where(renter, RENTER_PASSTHROUGH * 12.0 * rent_month, 0.0) / household_members
    totals["property_tax_owner"] = np.bincount(index, weights=owner_tax_person, minlength=n_units)
    totals["property_tax_renter_proxy"] = np.bincount(index, weights=renter_tax_person, minlength=n_units)
    totals["property_tax_owner_plus_renter"] = (totals["property_tax_owner"]
                                                + totals["property_tax_renter_proxy"])

    # ---- (B) K-12 schooling cost of the unit's children -------------------
    # Children's own generation is set by THEIR parents, so a child of Mexican
    # second-generation parents is third generation. The ledger question here is
    # the cost borne by the resource unit the adults live in, so the cost is
    # attributed to the adults' group, exactly like SNAP or school lunch.
    children = d.A_AGE.between(5, 17).to_numpy(dtype=float)
    totals["children_5_17"] = np.bincount(index, weights=children, minlength=n_units)
    totals["k12_cost_at_full_attendance"] = np.bincount(
        index, weights=children * per_pupil, minlength=n_units)

    # ---- group masks, identical construction to the generator --------------
    native = d.PRCITSHP.isin([1, 2, 3])
    us_area = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area)
    parent_mexico = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    group = {
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy(),
        "all_native": native.to_numpy(),
        "all_second_gen": (native & ~parents_us).to_numpy(),
        "mexican_second_gen": (native & parent_mexico).to_numpy(),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)).to_numpy(),
        "mexico_born": (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy(),
    }
    adults_25_64 = (d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2)).to_numpy()
    person_weights = d[base.REPS].to_numpy()
    adults_18 = d.A_AGE.ge(18).to_numpy()
    n_adults = np.bincount(index, weights=adults_18, minlength=n_units)
    allocations = {
        "equal_all_members": np.ones(len(d), dtype=bool),
        "equal_adults_18plus": adults_18 | (n_adults[index] == 0),
    }
    return dict(d=d, index=index, n_units=n_units, totals=totals, group=group,
                adults_25_64=adults_25_64, person_weights=person_weights,
                allocations=allocations, validation=validation, cps=cps, params=params)


def analyse(state, args):
    d, index, n_units = state["d"], state["index"], state["n_units"]
    totals, group = state["totals"], state["group"]
    adults, weights = state["adults_25_64"], state["person_weights"]
    rows, lines = [], []

    def out(text=""):
        print(text)
        lines.append(text)

    for allocation, eligible in state["allocations"].items():
        per = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}

        # Extended-balance variants, built at person level so the SDR variance
        # of the composite is computed directly rather than summed componentwise.
        def composite(sales_key, property_key, ratio_map, add_back_lunch):
            arr = (per["cash_noncash_tax_balance"] + per["employer_payroll"]
                   + per[sales_key] + per[property_key])
            if add_back_lunch:
                arr = arr + per["school_lunch"]
            return arr

        variants = {
            "extended_balance_base": ("sales_tax_share35", "property_tax_owner",
                                      PUPIL_RATIO_NATIVE_ACS, False),
            "extended_balance_sales25": ("sales_tax_share25", "property_tax_owner",
                                         PUPIL_RATIO_NATIVE_ACS, False),
            "extended_balance_sales45": ("sales_tax_share45", "property_tax_owner",
                                         PUPIL_RATIO_NATIVE_ACS, False),
            "extended_balance_sales_itep": ("sales_tax_itep", "property_tax_owner",
                                            PUPIL_RATIO_NATIVE_ACS, False),
            "extended_balance_renter_proxy": ("sales_tax_share35", "property_tax_owner_plus_renter",
                                              PUPIL_RATIO_NATIVE_ACS, False),
            "extended_balance_pupil_ratio_090": ("sales_tax_share35", "property_tax_owner",
                                                 PUPIL_RATIO_FLAT, False),
            "extended_balance_pupil_differential": ("sales_tax_share35", "property_tax_owner",
                                                    "differential", False),
            "extended_balance_net_of_school_lunch": ("sales_tax_share35", "property_tax_owner",
                                                     PUPIL_RATIO_NATIVE_ACS, True),
        }

        reported = ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
                    "cash_noncash_tax_balance", "employer_payroll",
                    "sales_tax_share25", "sales_tax_share35", "sales_tax_share45", "sales_tax_itep",
                    "property_tax_owner", "property_tax_renter_proxy",
                    "property_tax_owner_plus_renter", "children_5_17",
                    "k12_cost_at_full_attendance"]

        replicates: dict[tuple[str, str], np.ndarray] = {}
        for g, mask in group.items():
            use = adults & mask
            w = weights[use]
            values = np.stack([per[m][use] for m in reported])
            for metric, est in zip(reported, estimate(values, w)):
                replicates[g, metric] = est
            # K-12 charged, at each attendance assumption
            for label, ratio in (("k12_charged_acs_native", PUPIL_RATIO_NATIVE_ACS),
                                 ("k12_charged_flat_090", PUPIL_RATIO_FLAT),
                                 ("k12_charged_differential", PUPIL_RATIO_DIFFERENTIAL[g])):
                replicates[g, label] = replicates[g, "k12_cost_at_full_attendance"] * ratio
            for name, (sales_key, property_key, ratio, lunch) in variants.items():
                r = ratio if ratio != "differential" else PUPIL_RATIO_DIFFERENTIAL[g]
                arr = composite(sales_key, property_key, ratio, lunch)
                replicates[g, name] = estimate(arr[use][None, :], w)[0] - r * replicates[g, "k12_cost_at_full_attendance"]

        all_metrics = reported + ["k12_charged_acs_native", "k12_charged_flat_090",
                                  "k12_charged_differential"] + list(variants)
        for g in GROUPS:
            use = adults & group[g]
            for metric in all_metrics:
                est, se = sdr(replicates[g, metric])
                diff = replicates[g, metric] - replicates[REFERENCE, metric]
                dest, dse = sdr(diff)
                rows.append({"allocation": allocation, "weighting": "person", "group": g,
                             "metric": metric, "n_adults_unweighted": int(use.sum()),
                             "weighted_adults": float(weights[use, 0].sum()),
                             "estimate": est, "se_sdr": se,
                             "difference_from_third_plus_nh_white": dest,
                             "se_sdr_difference": dse})

        out(f"\n{'=' * 150}")
        out(f"== allocation={allocation}  weighting=person  "
            f"annual $ per adult 25-64, 2024 income year (SDR se in parentheses) ==")
        out(f"{'=' * 150}")
        header = f"{'row':44s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS)
        display = [
            ("Modeled taxes (payroll+fed+state)", "modeled_tax_total", +1),
            ("Selected cash transfers", "selected_cash_total", -1),
            ("Selected non-cash transfers", "selected_noncash_total", -1),
            ("= Taxes minus selected transfers", "cash_noncash_tax_balance", +1),
            ("+ Employer payroll tax", "employer_payroll", +1),
            ("+ Sales/excise tax (0.35 share)", "sales_tax_share35", +1),
            ("+ Property tax (owner-occupied)", "property_tax_owner", +1),
            ("- K-12 public schooling", "k12_charged_acs_native", -1),
            ("= EXTENDED BALANCE", "extended_balance_base", +1),
        ]
        out(header)
        for label, metric, _sign in display:
            cells = ""
            for g in GROUPS:
                est, se = sdr(replicates[g, metric])
                cells += f"{est:>11,.0f} ({se:,.0f})".rjust(18)
            out(f"{label:44s}{cells}")
        out()
        out(f"{'difference from 3rd+ NH white':44s}" + "".join(f"{g[:20]:>18s}" for g in GROUPS))
        for label, metric, _sign in display:
            cells = ""
            for g in GROUPS:
                diff = replicates[g, metric] - replicates[REFERENCE, metric]
                est, se = sdr(diff)
                cells += ("—".rjust(18) if g == REFERENCE else f"{est:>11,.0f} ({se:,.0f})".rjust(18))
            out(f"{label:44s}{cells}")

        out()
        out("-- how each addition moves the Mexican-second-generation gap to 3rd+ NH white --")
        baseline_gap = sdr(replicates["mexican_second_gen", "cash_noncash_tax_balance"]
                           - replicates[REFERENCE, "cash_noncash_tax_balance"])[0]
        out(f"   baseline gap (taxes minus selected transfers): {baseline_gap:,.0f}")
        running = baseline_gap
        for label, metric, sign in [("employer payroll tax", "employer_payroll", +1),
                                    ("sales/excise tax (0.35 share)", "sales_tax_share35", +1),
                                    ("property tax (owner-occupied)", "property_tax_owner", +1),
                                    ("K-12 public schooling", "k12_charged_acs_native", -1)]:
            delta = sign * sdr(replicates["mexican_second_gen", metric]
                               - replicates[REFERENCE, metric])[0]
            running += delta
            frac = delta / abs(baseline_gap) * 100
            verb = "closes" if delta > 0 else "widens"
            out(f"   {label:34s} {delta:>9,.0f}  ({verb} {abs(frac):5.1f}% of the baseline gap)"
                f"   running gap {running:>9,.0f}")
        final = sdr(replicates["mexican_second_gen", "extended_balance_base"]
                    - replicates[REFERENCE, "extended_balance_base"])
        out(f"   extended gap (composite, SDR se): {final[0]:,.0f} ({final[1]:,.0f})")
        out(f"   share of the baseline gap remaining: {final[0] / baseline_gap * 100:.1f}%")

        out()
        out("-- sensitivity: extended balance and its gap to 3rd+ NH white under each assumption --")
        out(f"{'variant':44s}{'3rd+ NH white':>18s}{'Mexican 2nd gen':>18s}{'gap (se)':>22s}")
        for name in variants:
            w_est = sdr(replicates[REFERENCE, name])[0]
            m_est = sdr(replicates["mexican_second_gen", name])[0]
            g_est, g_se = sdr(replicates["mexican_second_gen", name] - replicates[REFERENCE, name])
            out(f"{name:44s}{w_est:>18,.0f}{m_est:>18,.0f}{f'{g_est:,.0f} ({g_se:,.0f})':>22s}")

        out()
        out("-- implied effective rates, calibration against published aggregates --")
        for g in GROUPS:
            inc = sdr(replicates[g, "modeled_tax_total"])[0]
            sales = sdr(replicates[g, "sales_tax_share35"])[0]
            itep = sdr(replicates[g, "sales_tax_itep"])[0]
            emp = sdr(replicates[g, "employer_payroll"])[0]
            kids = sdr(replicates[g, "children_5_17"])[0]
            out(f"   {g:28s} children 5-17 per adult {kids:5.3f}   employer payroll {emp:>8,.0f}"
                f"   sales(0.35) {sales:>7,.0f}   sales(ITEP) {itep:>7,.0f}   modeled tax {inc:>8,.0f}")

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "extended_ledger_by_generation.csv", index=False)
    (HERE / "extended_ledger_result.txt").write_text("\n".join(lines) + "\n")
    return frame


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cps-zip", type=Path, default=None,
                    help="CPS ASEC 2025 public-use CSV zip (asecpub25csv.zip). "
                         "Default: CPS_ASEC_2025_ZIP, then PNY_DATA_ROOT, then the "
                         "2TBPNY path, then a lane-local cache downloaded from census.gov.")
    args = ap.parse_args()
    state = build(args)

    head = []
    head.append("Extended annual partial fiscal ledger by origin-generation")
    head.append("CPS ASEC 2025 (income year 2024), SPM resource units, person weights,")
    head.append("160-replicate SDR standard errors. Adults 25-64, civilian household members.")
    head.append(f"CPS source: {state['cps']}")
    head.append(f"CPS validation: {json.dumps(state['validation'])}")
    head.append("")
    head.append("Baseline rows reproduce infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py")
    head.append("exactly (same prepare(), same allocate(), same group masks).")
    print("\n".join(head))

    frame = analyse(state, args)

    check = frame.query("allocation == 'equal_all_members' and group == 'mexican_second_gen' "
                        "and metric == 'cash_noncash_tax_balance'")
    gap = float(check.difference_from_third_plus_nh_white.iloc[0])
    gap_se = float(check.se_sdr_difference.iloc[0])
    repro = [
        "",
        "-- STEP A reproduction check --",
        f"Mexican 2nd gen minus 3rd+ NH white, taxes minus selected transfers,",
        f"equal_all_members allocation, person weights, adults 25-64: "
        f"{gap:,.0f} (se {gap_se:,.0f})",
        "Published in research/immigration-mexican-origin-by-generation-2026-09-16.md "
        "table 5: -6,066 (se 353)",
        f"Deviation from the published -6,066: {gap - (-6066):+,.2f}",
    ]
    text = (HERE / "extended_ledger_result.txt").read_text()
    (HERE / "extended_ledger_result.txt").write_text(
        "\n".join(head) + "\n" + text + "\n".join(repro) + "\n")
    print("\n".join(repro))
    if abs(gap - (-6066)) > 50:
        raise SystemExit(f"[BLOCKED] baseline reproduction off by more than $50: {gap:,.0f}")
    print("[reproduction check] PASS (within $50 of the published -6,066)")
    print(f"\nWrote {HERE / 'extended_ledger_by_generation.csv'}")
    print(f"Wrote {HERE / 'extended_ledger_result.txt'}")


if __name__ == "__main__":
    main()
