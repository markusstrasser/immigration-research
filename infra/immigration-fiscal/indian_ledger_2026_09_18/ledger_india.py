#!/usr/bin/env python3
"""India-origin residents on the repo's annual partial fiscal ledger.

Reuses, without editing, the two upstream lanes the brief names:
  * infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py   (prepare/allocate/estimate)
  * gen_ledger_extension_2026_09_16/extend_ledger.py            (employer payroll, sales,
                                                                 property, K-12 extension)
  * cps_generation_welfare_2026_09_16/lifecycle_ledger_by_generation.py (MEPS public-paid
                                                                 health donor model pattern)

`extend_ledger.build()` is imported and called as-is; only the group masks, the universes,
the arms and the reporting are new here. Nothing in another lane is written.

Groups added: India-born (PENATVTY=210, verified against the March 2025 CPS data dictionary,
Appendix J), US-born with at least one India-born parent (PEFNTVTY/PEMNTVTY = 210), native
self-identified Asian Indian (PRDASIAN=1), China-born (207/209/240 variants), plus the repo's
same-age third-plus non-Hispanic white reference and Mexico-born/Mexican-second-generation
for continuity with the published ledger.

Run: uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 ledger_india.py
"""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths


import argparse
import hashlib
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
INFRA = HERE.parent
sys.path.insert(0, str(INFRA / "build"))
sys.path.insert(0, str(INFRA / "gen_ledger_extension_2026_09_16"))

import analyze_cps_fiscal_2025 as base  # noqa: E402
import extend_ledger as ext  # noqa: E402  (appends WSAL_VAL/SPM_RESOURCES to base.PERSON)

from analyze_cps_fiscal_2025 import allocate, estimate  # noqa: E402

# Extra person fields this lane needs on top of what base + extend_ledger read.
for _f in ["PRDASIAN", "PEPAR1", "PEPAR2"]:
    if _f not in base.PERSON:
        base.PERSON.append(_f)

INDIA = 210
CHINA_MAINLAND = 207
CHINA_BROAD = [207, 209, 240]   # mainland China, Hong Kong, Taiwan
MEXICO = 303
US_AREA = [57, 60, 66, 69, 73, 78]

REFERENCE = "third_plus_nh_white"
GROUP_ORDER = [
    "third_plus_nh_white",
    "all_native",
    "india_born",
    "india_born_recent_noncit",
    "india_born_settled",
    "india_second_gen",
    "asian_indian_native_selfid",
    "china_born",
    "china_born_broad",
    "all_foreign_born",
    "mexico_born",
    "mexican_second_gen",
]

# Attendance ratio: the India groups are not Mexico-born, so the base case uses the repo's
# measured native-household public-pupil-per-child ratio for every group, exactly as the
# upstream base variant does. The flat-0.90 arm is reported as a sensitivity.
RATIO_BASE = ext.PUPIL_RATIO_NATIVE_ACS
RATIO_FLAT = ext.PUPIL_RATIO_FLAT

BANDS_25_64 = [(25, 34), (35, 44), (45, 54), (55, 64)]

# Upstream published white-reference figures (gen_ledger_extension_2026_09_16,
# extended_ledger_by_generation.csv). The gate script re-reads them from that CSV;
# these are only for the printed header.
UPSTREAM_WHITE_BALANCE = 11784.661700
UPSTREAM_WHITE_EXTENDED = 15984.424821


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def sdr(values: np.ndarray) -> tuple[float, float]:
    values = np.asarray(values, dtype=float)
    return float(values[0]), float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def resolve_cps(explicit: Path | None) -> Path:
    if explicit is not None:
        if not explicit.exists():
            raise SystemExit(f"[BLOCKED] --cps-zip not found: {explicit}")
        return explicit
    for c in [INFRA / "gen_ledger_extension_2026_09_16" / "_cache" / "asecpub25csv.zip",
              HERE / "_cache" / "asecpub25csv.zip"]:
        if c.exists():
            return c
    return ext.resolve_cps_zip(None)


def health_person_means(d: pd.DataFrame, meps_zip: Path, meps_sas: Path) -> dict[str, np.ndarray]:
    """MEPS public-paid medical dollars per person, donor model, as the peer lanes use it."""
    from meps_health_transport_2024 import donor_model, read_meps
    medical, anchors = read_meps(meps_zip, meps_sas)
    alive = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    out = {}
    for insured, label in ((False, "health_age_birth"), (True, "health_age_birth_ins")):
        cells, codes, _cov = donor_model(medical, d, insured)
        out[label] = cells.mean_public_paid.to_numpy()[codes] * alive
    out["_anchors"] = anchors
    return out


def build_groups(d: pd.DataFrame) -> dict[str, np.ndarray]:
    native = d.PRCITSHP.isin([1, 2, 3])
    foreign = d.PRCITSHP.isin([4, 5])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_india = d.PEFNTVTY.eq(INDIA) | d.PEMNTVTY.eq(INDIA)
    parent_mexico = d.PEFNTVTY.eq(MEXICO) | d.PEMNTVTY.eq(MEXICO)
    return {
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy(),
        "all_native": native.to_numpy(),
        "india_born": (foreign & d.PENATVTY.eq(INDIA)).to_numpy(),
        # Temporary-visa proxy: CPS observes no visa class, so a noncitizen who entered in 2018
        # or later (PEINUSYR >= 26) stands in for the H-1B/H-4/F-1-OPT population.
        "india_born_recent_noncit": (foreign & d.PENATVTY.eq(INDIA) & d.PRCITSHP.eq(5)
                                     & d.PEINUSYR.ge(26)).to_numpy(),
        "india_born_settled": (foreign & d.PENATVTY.eq(INDIA)
                               & ~(d.PRCITSHP.eq(5) & d.PEINUSYR.ge(26))).to_numpy(),
        "india_second_gen": (native & parent_india).to_numpy(),
        "asian_indian_native_selfid": (native & d.PRDASIAN.eq(1)).to_numpy(),
        "china_born": (foreign & d.PENATVTY.eq(CHINA_MAINLAND)).to_numpy(),
        "china_born_broad": (foreign & d.PENATVTY.isin(CHINA_BROAD)).to_numpy(),
        "all_foreign_born": foreign.to_numpy(),
        "mexico_born": (foreign & d.PENATVTY.eq(MEXICO)).to_numpy(),
        "mexican_second_gen": (native & parent_mexico).to_numpy(),
    }


def per_person_metrics(state, allocation: str, health: dict | None) -> dict[str, np.ndarray]:
    """Allocate every unit total under one allocation rule and form the composites."""
    totals, index, n_units = state["totals"], state["index"], state["n_units"]
    eligible = state["allocations"][allocation]
    per = {k: allocate(v, index, eligible, n_units) for k, v in totals.items()}
    per["state_local_total"] = (per["state_after_credits"] + per["sales_tax_share35"]
                                + per["property_tax_owner"])
    per["k12_charged"] = RATIO_BASE * per["k12_cost_at_full_attendance"]
    per["k12_charged_flat090"] = RATIO_FLAT * per["k12_cost_at_full_attendance"]
    per["extended_balance_base"] = (per["cash_noncash_tax_balance"] + per["employer_payroll"]
                                    + per["sales_tax_share35"] + per["property_tax_owner"]
                                    - per["k12_charged"])
    per["extended_balance_flat090"] = (per["extended_balance_base"] + per["k12_charged"]
                                       - per["k12_charged_flat090"])
    per["extended_balance_renter"] = (per["extended_balance_base"]
                                      + per["property_tax_renter_proxy"])
    per["extended_balance_sales_itep"] = (per["extended_balance_base"]
                                          - per["sales_tax_share35"] + per["sales_tax_itep"])
    if health is not None:
        for label in ("health_age_birth", "health_age_birth_ins"):
            unit_total = np.bincount(index, weights=health[label], minlength=n_units)
            per[label] = allocate(unit_total, index, eligible, n_units)
        per["extended_balance_after_health"] = per["extended_balance_base"] - per["health_age_birth"]
        per["extended_balance_after_health_ins"] = (per["extended_balance_base"]
                                                    - per["health_age_birth_ins"])
    return per


METRICS = [
    "modeled_tax_total", "payroll", "federal_after_refundable", "state_after_credits",
    "employer_payroll", "sales_tax_share35", "sales_tax_itep", "property_tax_owner",
    "property_tax_renter_proxy", "state_local_total",
    "selected_cash_total", "selected_noncash_total", "social_security", "snap",
    "cash_noncash_tax_balance", "children_5_17", "k12_cost_at_full_attendance",
    "k12_charged", "k12_charged_flat090",
    "extended_balance_base", "extended_balance_flat090", "extended_balance_renter",
    "extended_balance_sales_itep",
    "health_age_birth", "health_age_birth_ins",
    "extended_balance_after_health", "extended_balance_after_health_ins",
]


def group_replicates(per, metrics, use, weights) -> dict[str, np.ndarray]:
    values = np.stack([per[m][use] for m in metrics])
    return dict(zip(metrics, estimate(values, weights[use])))


def age_standardised_replicates(per, metrics, use, weights, age, std_share):
    """Direct standardisation of each replicate mean to the reference age distribution."""
    out = {m: np.zeros(weights.shape[1]) for m in metrics}
    for (lo, hi), share in zip(BANDS_25_64, std_share):
        sel = use & (age >= lo) & (age <= hi)
        if sel.sum() == 0:
            return None
        reps = group_replicates(per, metrics, sel, weights)
        for m in metrics:
            out[m] = out[m] + share * reps[m]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cps-zip", type=Path, default=None)
    ap.add_argument("--meps-zip", type=Path,
                    default=_data_paths.data_root(require_exists=False) / 'external/stage3/ahrq/meps_2024/h256dat.zip')
    ap.add_argument("--meps-sas", type=Path,
                    default=_data_paths.data_root(require_exists=False) / 'external/stage3/ahrq/meps_2024/h256su.txt')
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    cps = resolve_cps(args.cps_zip)
    print(f"[1/6] CPS ASEC 2025: {cps.name}", flush=True)
    build_args = argparse.Namespace(cps_zip=cps)
    state = ext.build(build_args)
    d = state["d"]
    print(f"      person rows {len(d):,}  SPM units {state['n_units']:,}", flush=True)

    print("[2/6] group masks", flush=True)
    groups = build_groups(d)
    state["group"] = groups

    health = None
    if args.meps_zip.exists() and args.meps_sas.exists():
        print("[3/6] MEPS 2024 public-paid donor model", flush=True)
        health = health_person_means(d, args.meps_zip, args.meps_sas)
    else:
        print("[3/6] MEPS files absent — health component SKIPPED", flush=True)

    metrics = list(METRICS) if health is not None else [m for m in METRICS if "health" not in m]

    age = d.A_AGE.to_numpy()
    civ = d.PRPERTYP.eq(2).to_numpy()
    universes = {
        "adults_25_64": civ & (age >= 25) & (age <= 64),
        "all_ages": civ | (age < 15),
    }
    weightings = {
        "person": d[base.REPS].to_numpy(),
        "resource_unit_head": None,   # filled below (head weights broadcast to members)
    }
    # Head weights broadcast to unit members: the base script's "resource_unit_head" weighting.
    head_reps = state["d"].loc[state["d"].SPM_HEAD.eq(1)].sort_values("SPM_ID")[base.REPS].to_numpy()
    weightings["resource_unit_head"] = head_reps[state["index"]]

    # Arm masks (applied on top of universe x group).
    resources = d.SPM_RESOURCES.to_numpy(dtype=float)
    w0 = d.MARSUPWT.to_numpy(dtype=float)
    adults = universes["adults_25_64"]
    order = np.argsort(resources[adults], kind="stable")
    cum = np.cumsum(w0[adults][order]) / w0[adults].sum()
    thresh = float(resources[adults][order][np.searchsorted(cum, 0.99)])
    top1 = resources > thresh
    noncitizen = d.PRCITSHP.eq(5).to_numpy()
    recent = d.PEINUSYR.ge(26).to_numpy()          # entered 2018 or later
    temp_proxy = noncitizen & recent                # temporary-visa proxy, stated as such
    arms = {
        "raw": np.ones(len(d), dtype=bool),
        "exclude_top1_income": ~top1,
        "exclude_recent_noncitizen": ~temp_proxy,
    }

    print("[4/6] estimating", flush=True)
    rows = []
    for allocation in ("equal_all_members", "equal_adults_18plus"):
        per = per_person_metrics(state, allocation, health)
        for uname, umask in universes.items():
            # Reference age distribution for the standardisation arm.
            ref_use = umask & groups[REFERENCE] & arms["raw"]
            std_share = None
            if uname == "adults_25_64":
                shares = np.array([w0[ref_use & (age >= lo) & (age <= hi)].sum()
                                   for lo, hi in BANDS_25_64])
                std_share = shares / shares.sum()
            for wname, weights in weightings.items():
                for aname, amask in arms.items():
                    if wname == "resource_unit_head" and aname != "raw":
                        continue
                    ref = group_replicates(per, metrics, umask & groups[REFERENCE] & amask, weights)
                    for g in GROUP_ORDER:
                        use = umask & groups[g] & amask
                        n = int(use.sum())
                        if n == 0:
                            continue
                        reps = group_replicates(per, metrics, use, weights)
                        for m in metrics:
                            est, se = sdr(reps[m])
                            dest, dse = sdr(reps[m] - ref[m])
                            rows.append({"universe": uname, "allocation": allocation,
                                         "weighting": wname, "arm": aname, "group": g,
                                         "metric": m, "n_unweighted": n,
                                         "weighted_persons": float(weights[use, 0].sum()),
                                         "estimate": est, "se_sdr": se,
                                         "diff_vs_white": dest, "se_sdr_diff": dse})
                # Age-standardised arm, person weighting only, adults 25-64 only.
                if std_share is not None and wname == "person":
                    ref = age_standardised_replicates(per, metrics,
                                                      umask & groups[REFERENCE] & arms["raw"],
                                                      weights, age, std_share)
                    for g in GROUP_ORDER:
                        use = umask & groups[g] & arms["raw"]
                        reps = age_standardised_replicates(per, metrics, use, weights, age, std_share)
                        if reps is None:
                            continue
                        for m in metrics:
                            est, se = sdr(reps[m])
                            dest, dse = sdr(reps[m] - ref[m])
                            rows.append({"universe": uname, "allocation": allocation,
                                         "weighting": wname, "arm": "age_standardised",
                                         "group": g, "metric": m, "n_unweighted": int(use.sum()),
                                         "weighted_persons": float(weights[use, 0].sum()),
                                         "estimate": est, "se_sdr": se,
                                         "diff_vs_white": dest, "se_sdr_diff": dse})

    # Own-person descriptive metrics (not allocated): earnings, own payroll, coverage, entry.
    person_weights = weightings["person"]
    own = {"earnings": d.PEARNVAL.to_numpy(dtype=float),
           "own_modeled_payroll": d.FICA.to_numpy(dtype=float),
           "medicaid_coverage_share": d.MCAID.eq(1).to_numpy(dtype=float),
           "medicare_coverage_share": d.MCARE.eq(1).to_numpy(dtype=float),
           "noncitizen_share": noncitizen.astype(float),
           "recent_entrant_noncitizen_share": temp_proxy.astype(float)}
    for uname, umask in universes.items():
        ref_use = umask & groups[REFERENCE]
        ref = {k: estimate(v[ref_use][None, :], person_weights[ref_use])[0] for k, v in own.items()}
        for g in GROUP_ORDER:
            use = umask & groups[g]
            if use.sum() == 0:
                continue
            for k, v in own.items():
                r = estimate(v[use][None, :], person_weights[use])[0]
                est, se = sdr(r)
                dest, dse = sdr(r - ref[k])
                rows.append({"universe": uname, "allocation": "own_person", "weighting": "person",
                             "arm": "raw", "group": g, "metric": k, "n_unweighted": int(use.sum()),
                             "weighted_persons": float(person_weights[use, 0].sum()),
                             "estimate": est, "se_sdr": se,
                             "diff_vs_white": dest, "se_sdr_diff": dse})

    frame = pd.DataFrame(rows).sort_values(
        ["universe", "allocation", "weighting", "arm", "group", "metric"], kind="stable")
    out_csv = args.out / "india_ledger_long.csv"
    frame.to_csv(out_csv, index=False, float_format="%.6f")
    print(f"[5/6] wrote {out_csv.name} ({len(frame):,} rows)", flush=True)

    print("[6/6] report", flush=True)
    lines = report(frame, cps, health, thresh)
    (args.out / "india_ledger_result.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def cell(frame, universe, allocation, weighting, arm, group, metric, field="estimate"):
    q = frame.query("universe == @universe and allocation == @allocation and "
                    "weighting == @weighting and arm == @arm and group == @group and "
                    "metric == @metric")
    if len(q) != 1:
        return float("nan")
    return float(q[field].iloc[0])


def report(frame, cps, health, thresh) -> list[str]:
    L = []
    def out(t=""):
        L.append(t)

    out("India-origin residents on the repo's annual partial fiscal ledger")
    out("CPS ASEC 2025 (income year 2024), SPM resource units, 160-replicate SDR standard errors.")
    out(f"CPS source: {cps.name}  sha256 {sha256(cps)}")
    out(f"MEPS 2024 public-paid health donor model: {'INCLUDED' if health else 'SKIPPED'}")
    out(f"Top-1% income threshold (SPM resources, adults 25-64, weighted): {thresh:,.0f}")
    out("Country codes verified against cpsmar25.pdf Appendix J: India 210, China 207,")
    out("Hong Kong 209, Taiwan 240, Mexico 303, US areas 057/060/066/069/073/078.")
    out()

    display = [
        ("Modeled taxes (payroll+fed+state)", "modeled_tax_total"),
        ("  of which federal income (after refundable)", "federal_after_refundable"),
        ("  of which personal payroll (FICA)", "payroll"),
        ("  of which state income (after credits)", "state_after_credits"),
        ("State-local total (income+sales+property)", "state_local_total"),
        ("Selected cash transfers", "selected_cash_total"),
        ("Selected non-cash transfers", "selected_noncash_total"),
        ("= Taxes minus selected transfers", "cash_noncash_tax_balance"),
        ("+ Employer payroll tax", "employer_payroll"),
        ("+ Sales/excise tax (0.35 share)", "sales_tax_share35"),
        ("+ Property tax (owner-occupied)", "property_tax_owner"),
        ("- K-12 public schooling", "k12_charged"),
        ("= EXTENDED BALANCE", "extended_balance_base"),
        ("- MEPS public-paid health", "health_age_birth"),
        ("= EXTENDED BALANCE AFTER HEALTH", "extended_balance_after_health"),
        ("(memo) children 5-17 per person", "children_5_17"),
    ]
    for universe in ("adults_25_64", "all_ages"):
        for allocation in ("equal_all_members", "equal_adults_18plus"):
            out("=" * 170)
            out(f"== universe={universe}  allocation={allocation}  weighting=person  arm=raw ==")
            out(f"== annual $ per person per year, 2024 income year (SDR se in parentheses) ==")
            out("=" * 170)
            gs = [g for g in GROUP_ORDER
                  if not np.isnan(cell(frame, universe, allocation, "person", "raw", g,
                                       "cash_noncash_tax_balance"))]
            out(f"{'row':44s}" + "".join(f"{g[:19]:>17s}" for g in gs))
            out(f"{'n unweighted':44s}" + "".join(
                f"{cell(frame, universe, allocation, 'person', 'raw', g, 'cash_noncash_tax_balance', 'n_unweighted'):>17,.0f}"
                for g in gs))
            out(f"{'weighted persons (millions)':44s}" + "".join(
                f"{cell(frame, universe, allocation, 'person', 'raw', g, 'cash_noncash_tax_balance', 'weighted_persons') / 1e6:>17,.2f}"
                for g in gs))
            for label, metric in display:
                if metric not in set(frame.metric):
                    continue
                fmt = ",.3f" if metric == "children_5_17" else ",.0f"
                cells = ""
                for g in gs:
                    e = cell(frame, universe, allocation, "person", "raw", g, metric)
                    s = cell(frame, universe, allocation, "person", "raw", g, metric, "se_sdr")
                    cells += (f"{e:>10{fmt}} ({s:{fmt}})" if not np.isnan(e) else "—").rjust(17)
                out(f"{label:44s}{cells}")
            out()
            out(f"{'difference from 3rd+ NH white (se)':44s}" + "".join(f"{g[:19]:>17s}" for g in gs))
            for label, metric in display:
                if metric not in set(frame.metric):
                    continue
                fmt = ",.3f" if metric == "children_5_17" else ",.0f"
                cells = ""
                for g in gs:
                    if g == REFERENCE:
                        cells += "—".rjust(17)
                        continue
                    e = cell(frame, universe, allocation, "person", "raw", g, metric, "diff_vs_white")
                    s = cell(frame, universe, allocation, "person", "raw", g, metric, "se_sdr_diff")
                    cells += (f"{e:>10{fmt}} ({s:{fmt}})" if not np.isnan(e) else "—").rjust(17)
                out(f"{label:44s}{cells}")
            out()

    out("=" * 170)
    out("== ARMS: extended balance and its gap to the white reference, adults 25-64, equal_all_members ==")
    out("=" * 170)
    arm_specs = [("raw", "person", "raw"),
                 ("age_standardised", "person", "age_standardised"),
                 ("household (resource-unit-head) weighted", "resource_unit_head", "raw"),
                 ("exclude top 1% income", "person", "exclude_top1_income"),
                 ("exclude recent noncitizen entrants", "person", "exclude_recent_noncitizen")]
    for metric in ("cash_noncash_tax_balance", "extended_balance_base",
                   "extended_balance_after_health"):
        if metric not in set(frame.metric):
            continue
        out(f"\n-- {metric} --")
        out(f"{'arm':42s}" + "".join(f"{g[:19]:>17s}" for g in
                                     ["third_plus_nh_white", "india_born", "india_second_gen",
                                      "china_born", "mexico_born"]))
        for label, wname, aname in arm_specs:
            cells = ""
            for g in ["third_plus_nh_white", "india_born", "india_second_gen",
                      "china_born", "mexico_born"]:
                e = cell(frame, "adults_25_64", "equal_all_members", wname, aname, g, metric)
                cells += (f"{e:>17,.0f}" if not np.isnan(e) else "—".rjust(17))
            out(f"{label:42s}{cells}")
            gaps = ""
            for g in ["third_plus_nh_white", "india_born", "india_second_gen",
                      "china_born", "mexico_born"]:
                e = cell(frame, "adults_25_64", "equal_all_members", wname, aname, g, metric,
                         "diff_vs_white")
                s = cell(frame, "adults_25_64", "equal_all_members", wname, aname, g, metric,
                         "se_sdr_diff")
                gaps += ("—".rjust(17) if g == REFERENCE or np.isnan(e)
                         else f"{e:>10,.0f} ({s:,.0f})".rjust(17))
            out(f"{'    gap vs white (se)':42s}{gaps}")

    out()
    out("=" * 170)
    out("== SENSITIVITY on the extended balance (adults 25-64, equal_all_members, person) ==")
    out("=" * 170)
    for metric in ("extended_balance_base", "extended_balance_flat090",
                   "extended_balance_renter", "extended_balance_sales_itep"):
        cells = ""
        for g in ["third_plus_nh_white", "india_born", "india_second_gen", "china_born", "mexico_born"]:
            e = cell(frame, "adults_25_64", "equal_all_members", "person", "raw", g, metric)
            cells += f"{e:>17,.0f}"
        out(f"{metric:42s}{cells}")

    out()
    out("== own-person descriptives, adults 25-64 (person weights) ==")
    for metric in ["earnings", "own_modeled_payroll", "medicaid_coverage_share",
                   "medicare_coverage_share", "noncitizen_share",
                   "recent_entrant_noncitizen_share"]:
        cells = ""
        for g in GROUP_ORDER:
            e = cell(frame, "adults_25_64", "own_person", "person", "raw", g, metric)
            cells += (f"{e:>17,.3f}" if not np.isnan(e) else "—".rjust(17))
        out(f"{metric:42s}{cells}")
    out(f"{'(groups)':42s}" + "".join(f"{g[:19]:>17s}" for g in GROUP_ORDER))
    return L


if __name__ == "__main__":
    main()
