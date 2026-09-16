#!/usr/bin/env python3
"""Re-run the origin-generation fiscal ledger on CPS ASEC 2026 (income year 2025)
and compare it side by side with CPS ASEC 2025 (income year 2024).

Reuses, without re-implementation:
  infra/immigration-fiscal/build/analyze_cps_fiscal_2025.py
      prepare() -- SPM resource-unit construction and every identity gate
      allocate(), estimate(), summarize() -- equal-shares allocation and 160-replicate SDR
  infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py
      build() -- baseline unit totals plus employer payroll, sales/excise,
                 property tax and K-12 cost, and the generation group masks

Year switching is done by remapping the zip member names that those two modules
open (pppub25.csv -> pppub26.csv, asec_csv_repwgt_2025.csv -> asec_csv_repwgt_2026.csv,
hhpub25.csv -> hhpub26.csv). No analytic code is copied or re-derived.

LAYOUT CHANGE HANDLED EXPLICITLY: SPM_BBSUBVAL (SPM broadband subsidy resource,
the Affordable Connectivity Program) is not on the ASEC 2026 public-use file --
the program lapsed on 2024-06-01. The 2026 ledger therefore runs on a four-item
non-cash set. To keep the year comparison like for like, the 2025 file is run
twice: once with the full five-item non-cash set (the published-gate run) and
once with broadband dropped (the comparison run). Nothing is substituted.

Outputs (this directory only):
  ledger_2025_vs_2026.csv
  ledger_2025_vs_2026_result.txt
"""
from __future__ import annotations

import os
import subprocess
import sys

if os.environ.get("_LEDGER_ASEC2026_BOOTSTRAPPED") != "1":
    try:
        import numpy  # noqa: F401
        import pandas  # noqa: F401
    except ModuleNotFoundError:
        env = dict(os.environ, _LEDGER_ASEC2026_BOOTSTRAPPED="1")
        cmd = ["uv", "run", "--with", "numpy>=2", "--with", "pandas>=2",
               "python3", os.path.abspath(__file__), *sys.argv[1:]]
        sys.exit(subprocess.call(cmd, env=env))

import argparse  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import types  # noqa: E402
import urllib.request  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "build"))
sys.path.insert(0, str(FISCAL / "gen_ledger_extension_2026_09_16"))

import analyze_cps_fiscal_2025 as base  # noqa: E402
import extend_ledger as ext  # noqa: E402

# extend_ledger writes its CSV/txt next to itself; point every write at this lane
# so the peer lane's published outputs are never touched.
ext.HERE = HERE

CPS25_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip"
CPS25_SHA = ext.CPS_SHA
CPS26_URL = "https://www2.census.gov/programs-surveys/cps/datasets/2026/march/asecpub26csv.zip"

GROUPS = ext.GROUPS
REFERENCE = ext.REFERENCE
BROADBAND_KEY = "broadband"
BROADBAND_FIELD = "SPM_BBSUBVAL"

# IRS Publication 15 (2024) p.2: social security wage base limit $168,600.
#   https://www.irs.gov/pub/irs-prior/p15--2024.pdf
# IRS Publication 15 (2025): "The social security wage base limit is $176,100."
#   https://www.irs.gov/pub/irs-prior/p15--2025.pdf
OASDI_CAP = {2024: 168_600.0, 2025: 176_100.0}

REPORTED = ["modeled_tax_total", "selected_cash_total", "selected_noncash_total",
            "cash_noncash_tax_balance", "employer_payroll", "sales_tax_share35",
            "property_tax_owner", "k12_cost_at_full_attendance", "children_5_17"]


def sha256_of(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def resolve_zip(kind: str, explicit: Path | None) -> Path:
    """Locate a CPS ASEC public-use zip; download into _cache only if absent."""
    cache = HERE / "_cache"
    cache.mkdir(parents=True, exist_ok=True)
    if explicit is not None:
        if not explicit.exists():
            raise SystemExit(f"[BLOCKED] --{kind}-zip not found: {explicit}")
        return explicit
    if kind == "cps25":
        for c in [Path("/Volumes/2TBPNY/research-data/immigration-fiscal/data/external/"
                       "stage3/census/cps_asec_2025/asecpub25csv.zip"),
                  FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
                  cache / "asecpub25csv.zip"]:
            if c.exists():
                return c
        target, url = cache / "asecpub25csv.zip", CPS25_URL
    else:
        c = cache / "asecpub26csv.zip"
        if c.exists():
            return c
        target, url = c, CPS26_URL
    print(f"[stage] downloading {url}", flush=True)
    urllib.request.urlretrieve(url, target)
    return target


def remap_zip(mapping: dict[str, str]):
    """A zipfile module stand-in whose ZipFile renames the members it is asked for."""
    class Z(zipfile.ZipFile):
        def open(self, name, *a, **k):  # type: ignore[override]
            if isinstance(name, str):
                name = mapping.get(name, name)
            return super().open(name, *a, **k)
    return types.SimpleNamespace(ZipFile=Z)


def zip_members(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as z:
        return sorted(z.namelist())


def csv_header(path: Path, member: str) -> list[str]:
    with zipfile.ZipFile(path) as z, z.open(member) as f:
        return f.readline().decode().strip().split(",")


def run_ledger(cps_zip: Path, year_suffix: str, drop_broadband: bool,
               oasdi_cap: float, label: str) -> dict:
    """One full ledger pass. Mutates the shared module state, then restores it."""
    saved_person = list(base.PERSON)
    saved_noncash = dict(base.NONCASH)
    saved_cap = ext.OASDI_CAP_2024
    saved_base_zip, saved_ext_zip = base.zipfile, ext.zipfile
    shim = remap_zip({
        "pppub25.csv": f"pppub{year_suffix}.csv",
        "hhpub25.csv": f"hhpub{year_suffix}.csv",
        "asec_csv_repwgt_2025.csv": f"asec_csv_repwgt_20{year_suffix}.csv",
    })
    try:
        if drop_broadband:
            if BROADBAND_FIELD in base.PERSON:
                base.PERSON.remove(BROADBAND_FIELD)
            base.NONCASH.pop(BROADBAND_KEY, None)
        ext.OASDI_CAP_2024 = oasdi_cap
        base.zipfile = shim
        ext.zipfile = shim
        print(f"\n[run] {label}: {cps_zip}", flush=True)
        print(f"[run]   non-cash items = {sorted(base.NONCASH)}", flush=True)
        print(f"[run]   employer OASDI cap = ${oasdi_cap:,.0f}", flush=True)
        state = ext.build(types.SimpleNamespace(cps_zip=cps_zip))
    finally:
        base.PERSON[:] = saved_person
        base.NONCASH.clear()
        base.NONCASH.update(saved_noncash)
        ext.OASDI_CAP_2024 = saved_cap
        base.zipfile, ext.zipfile = saved_base_zip, saved_ext_zip
    print(f"[run]   validation: {json.dumps(state['validation'])}", flush=True)
    return state


def group_replicates(state: dict) -> dict[tuple[str, str], np.ndarray]:
    """equal_all_members allocation, person weights, adults 25-64 --- the published cut.

    Metric construction mirrors extend_ledger.analyse exactly: per-person allocation
    of every unit total, then one ratio estimate per replicate.
    """
    index, n_units = state["index"], state["n_units"]
    totals, group = state["totals"], state["group"]
    adults, weights = state["adults_25_64"], state["person_weights"]
    eligible = state["allocations"]["equal_all_members"]
    per = {k: ext.allocate(v, index, eligible, n_units) for k, v in totals.items()}
    composite = (per["cash_noncash_tax_balance"] + per["employer_payroll"]
                 + per["sales_tax_share35"] + per["property_tax_owner"])

    reps: dict[tuple[str, str], np.ndarray] = {}
    for g in GROUPS:
        use = adults & group[g]
        w = weights[use]
        values = np.stack([per[m][use] for m in REPORTED])
        for metric, est in zip(REPORTED, ext.estimate(values, w)):
            reps[g, metric] = est
        reps[g, "n_adults"] = np.array([float(use.sum())])
        reps[g, "weighted_adults"] = np.array([float(w[:, 0].sum())])
        reps[g, "k12_charged"] = (ext.PUPIL_RATIO_NATIVE_ACS
                                  * reps[g, "k12_cost_at_full_attendance"])
        reps[g, "extended_balance_base"] = (ext.estimate(composite[use][None, :], w)[0]
                                            - reps[g, "k12_charged"])
    return reps


def sdr(v: np.ndarray) -> tuple[float, float]:
    return ext.sdr(v)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cps25-zip", type=Path, default=None)
    ap.add_argument("--cps26-zip", type=Path, default=None)
    ap.add_argument("--gate-only", action="store_true")
    args = ap.parse_args()

    z25 = resolve_zip("cps25", args.cps25_zip)
    z26 = resolve_zip("cps26", args.cps26_zip)
    lines: list[str] = []

    def out(text=""):
        print(text, flush=True)
        lines.append(text)

    # ---------------------------------------------------------------- layout
    m25, m26 = zip_members(z25), zip_members(z26)
    h25 = csv_header(z25, "pppub25.csv")
    person_member = "pppub26.csv"
    if person_member not in m26:
        raise SystemExit(f"[BLOCKED] {person_member} absent from {z26}; members={m26}")
    h26 = csv_header(z26, person_member)
    missing = [c for c in base.PERSON + ext.EXTRA_PERSON if c not in h26]
    added = sorted(set(h26) - set(h25))
    dropped = sorted(set(h25) - set(h26))

    out("=" * 110)
    out("CPS ASEC 2026 (income year 2025) re-run of the origin-generation fiscal ledger")
    out("=" * 110)
    out(f"ASEC 2025 file : {z25}")
    out(f"  sha256       : {sha256_of(z25)}")
    out(f"  members      : {m25}")
    out(f"ASEC 2026 file : {z26}")
    out(f"  sha256       : {sha256_of(z26)}")
    out(f"  members      : {m26}")
    out(f"  source URL   : {CPS26_URL}")
    out()
    out(f"Person-file columns dropped 2025 -> 2026 ({len(dropped)}): {dropped}")
    out(f"Person-file columns added   2025 -> 2026 ({len(added)}): {added}")
    out(f"Ledger fields absent from the 2026 person file: {missing}")
    out()
    if missing and missing != [BROADBAND_FIELD]:
        raise SystemExit(f"[BLOCKED] ledger field(s) absent from ASEC 2026 beyond the "
                         f"documented broadband drop: {missing}")

    # ------------------------------------------------- step 1: published gate
    out("-" * 110)
    out("STEP 1 GATE --- reproduce the published 2025-file numbers")
    out("-" * 110)
    s25_full = run_ledger(z25, "25", drop_broadband=False,
                          oasdi_cap=OASDI_CAP[2024], label="ASEC 2025, full 5-item non-cash")
    r25_full = group_replicates(s25_full)
    gate_rows = []
    for metric, published, name in [
            ("cash_noncash_tax_balance", -6066.0, "taxes minus selected transfers"),
            ("extended_balance_base", -8286.0, "extended balance")]:
        diff = r25_full["mexican_second_gen", metric] - r25_full[REFERENCE, metric]
        est, se = sdr(diff)
        out(f"  Mexican 2nd gen minus 3rd+ NH white, {name}: {est:,.0f} (se {se:,.0f})")
        out(f"    published: {published:,.0f}   deviation: {est - published:+,.2f}")
        gate_rows.append((name, est, se, published, est - published))
    failures = [g for g in gate_rows if abs(g[4]) > 50]
    if failures:
        out()
        out("GATE FAIL --- deviation exceeds $50; stopping before the 2026 run.")
        (HERE / "ledger_2025_vs_2026_result.txt").write_text("\n".join(lines) + "\n")
        raise SystemExit(1)
    out("  GATE PASS --- both headline numbers within $50 of the published values.")
    out()
    bb = {g: sdr(r25_full[g, "selected_noncash_total"])[0] for g in GROUPS}
    if args.gate_only:
        (HERE / "ledger_2025_vs_2026_result.txt").write_text("\n".join(lines) + "\n")
        return

    # ---------------------------------------- comparison basis: no broadband
    out("-" * 110)
    out("STEP 2 --- like-for-like basis: SPM_BBSUBVAL dropped from BOTH years")
    out("-" * 110)
    out("  SPM_BBSUBVAL (Affordable Connectivity Program broadband subsidy) is not on")
    out("  the ASEC 2026 public-use file. The program lapsed 2024-06-01. Both years are")
    out("  therefore re-run on a four-item non-cash set (SNAP, energy, WIC, school lunch)")
    out("  so the year-over-year contrast is not contaminated by the dropped item.")
    out()
    s25 = run_ledger(z25, "25", drop_broadband=True, oasdi_cap=OASDI_CAP[2024],
                     label="ASEC 2025, 4-item non-cash")
    r25 = group_replicates(s25)
    s26 = run_ledger(z26, "26", drop_broadband=True, oasdi_cap=OASDI_CAP[2024],
                     label="ASEC 2026, 4-item non-cash, 2024 tax parameters")
    r26 = group_replicates(s26)
    s26b = run_ledger(z26, "26", drop_broadband=True, oasdi_cap=OASDI_CAP[2025],
                      label="ASEC 2026, 4-item non-cash, 2025 OASDI cap sensitivity")
    r26b = group_replicates(s26b)

    out()
    for g in GROUPS:
        nc_full, nc_drop = bb[g], sdr(r25[g, "selected_noncash_total"])[0]
        out(f"  broadband share of 2025-file non-cash, {g:26s}: "
            f"{nc_full:8,.0f} -> {nc_drop:8,.0f}  (broadband {nc_full - nc_drop:6,.0f})")
    out()

    # ------------------------------------------------------- side-by-side
    display = [
        ("Modeled taxes (payroll+fed+state)", "modeled_tax_total"),
        ("Selected cash transfers", "selected_cash_total"),
        ("Selected non-cash transfers", "selected_noncash_total"),
        ("Taxes minus selected transfers", "cash_noncash_tax_balance"),
        ("Employer payroll tax", "employer_payroll"),
        ("Sales/excise tax (0.35 share)", "sales_tax_share35"),
        ("Property tax (owner-occupied)", "property_tax_owner"),
        ("K-12 charged (ACS native ratio)", "k12_charged"),
        ("EXTENDED BALANCE", "extended_balance_base"),
    ]
    rows = []
    out("=" * 132)
    out("SIDE BY SIDE --- annual $ per adult 25-64, equal_all_members allocation, person")
    out("weights, 160-replicate SDR se. 2025 file = income year 2024; 2026 file = income")
    out("year 2025. Both on the 4-item non-cash basis, both at 2024 tax/spending parameters.")
    out("=" * 132)
    for g in GROUPS:
        out()
        out(f"### {g}   n(2025)={int(r25[g, 'n_adults'][0]):,}  n(2026)={int(r26[g, 'n_adults'][0]):,}")
        out(f"{'metric':38s}{'ASEC2025 (IY2024)':>24s}{'ASEC2026 (IY2025)':>24s}"
            f"{'change':>20s}{'nominal %':>12s}")
        for lab, metric in display:
            e25, s_25 = sdr(r25[g, metric])
            e26, s_26 = sdr(r26[g, metric])
            d = e26 - e25
            pct = (d / abs(e25) * 100) if e25 else float("nan")
            out(f"{lab:38s}{f'{e25:,.0f} ({s_25:,.0f})':>24s}{f'{e26:,.0f} ({s_26:,.0f})':>24s}"
                f"{d:>20,.0f}{pct:>11.1f}%")
        for lab, metric in display:
            e25, s_25 = sdr(r25[g, metric])
            e26, s_26 = sdr(r26[g, metric])
            e26b, s_26b = sdr(r26b[g, metric])
            if g == REFERENCE:
                d25 = d26 = ds25 = ds26 = float("nan")
            else:
                d25, ds25 = sdr(r25[g, metric] - r25[REFERENCE, metric])
                d26, ds26 = sdr(r26[g, metric] - r26[REFERENCE, metric])
            rows.append({
                "group": g, "metric": metric,
                "allocation": "equal_all_members", "weighting": "person",
                "n_adults_2025": int(r25[g, "n_adults"][0]),
                "n_adults_2026": int(r26[g, "n_adults"][0]),
                "weighted_adults_2025": float(r25[g, "weighted_adults"][0]),
                "weighted_adults_2026": float(r26[g, "weighted_adults"][0]),
                "estimate_asec2025": e25, "se_asec2025": s_25,
                "estimate_asec2026": e26, "se_asec2026": s_26,
                "estimate_asec2026_oasdi2025cap": e26b, "se_asec2026_oasdi2025cap": s_26b,
                "change_2026_minus_2025": e26 - e25,
                "diff_from_ref_asec2025": d25, "se_diff_from_ref_asec2025": ds25,
                "diff_from_ref_asec2026": d26, "se_diff_from_ref_asec2026": ds26,
                "pooled_estimate": 0.5 * (e25 + e26),
                "pooled_se_independent": 0.5 * float(np.hypot(s_25, s_26)),
                "pooled_diff_from_ref": 0.5 * (d25 + d26),
                "pooled_se_diff_independent": 0.5 * float(np.hypot(ds25, ds26)),
            })

    # -------------------------------------- differences from 3rd+ NH white
    out()
    out("=" * 132)
    out("DIFFERENCE FROM 3rd+ NH WHITE, with SDR standard errors, and the pooled two-year")
    out("estimate (simple average; se = sqrt(se25^2+se26^2)/2, INDEPENDENCE ASSUMED).")
    out("=" * 132)
    for lab, metric in display:
        out()
        out(f"-- {lab}")
        out(f"{'group':28s}{'ASEC2025 diff':>22s}{'ASEC2026 diff':>22s}"
            f"{'year change':>16s}{'|change|/se':>14s}{'pooled diff':>22s}")
        for g in GROUPS:
            if g == REFERENCE:
                continue
            d25, s25_ = sdr(r25[g, metric] - r25[REFERENCE, metric])
            d26, s26_ = sdr(r26[g, metric] - r26[REFERENCE, metric])
            ch = d26 - d25
            # Year-to-year change se, treating the two samples as independent.
            ch_se = float(np.hypot(s25_, s26_))
            ratio = abs(ch) / ch_se if ch_se else float("nan")
            pooled, pooled_se = 0.5 * (d25 + d26), 0.5 * ch_se
            out(f"{g:28s}{f'{d25:,.0f} ({s25_:,.0f})':>22s}{f'{d26:,.0f} ({s26_:,.0f})':>22s}"
                f"{ch:>16,.0f}{ratio:>14.2f}{f'{pooled:,.0f} ({pooled_se:,.0f})':>22s}")

    # ------------------------------------------------------------ verdict
    out()
    out("=" * 132)
    out("HEADLINE STABILITY CHECK --- Mexican 2nd gen vs 3rd+ NH white")
    out("=" * 132)
    verdict_rows = []
    for lab, metric in [("taxes minus selected transfers", "cash_noncash_tax_balance"),
                        ("extended balance", "extended_balance_base")]:
        d25, s25_ = sdr(r25["mexican_second_gen", metric] - r25[REFERENCE, metric])
        d26, s26_ = sdr(r26["mexican_second_gen", metric] - r26[REFERENCE, metric])
        ch = d26 - d25
        ch_se = float(np.hypot(s25_, s26_))
        within = abs(ch) <= ch_se
        pooled, pooled_se = 0.5 * (d25 + d26), 0.5 * ch_se
        out(f"  {lab}")
        out(f"    ASEC 2025 (IY2024): {d25:,.0f} (se {s25_:,.0f})")
        out(f"    ASEC 2026 (IY2025): {d26:,.0f} (se {s26_:,.0f})")
        out(f"    change: {ch:+,.0f}   se of change (independent): {ch_se:,.0f}   "
            f"|change|/se = {abs(ch) / ch_se:.2f}   -> "
            f"{'WITHIN 1 se' if within else 'OUTSIDE 1 se'}")
        out(f"    pooled two-year: {pooled:,.0f} (se {pooled_se:,.0f})")
        verdict_rows.append((lab, d25, s25_, d26, s26_, ch, ch_se, within, pooled, pooled_se))
    out()
    out("  CAVEAT: consecutive March ASEC samples share roughly half their households")
    out("  through the CPS 4-8-4 rotation, so the independence assumption understates the")
    out("  pooled se and overstates the se of the year-to-year change. The 'within 1 se'")
    out("  test above is therefore the conservative (easier to pass) direction.")

    out()
    out("PARAMETER NOTE: the 2026 run keeps the 2024 parameter set --- state sales tax rates,")
    out("effective property tax rates, ACS 2023 median gross rent, FY2024 per-pupil current")
    out("spending, ITEP quintile rates and the ACS 2024 pupil ratio --- exactly as the 2025")
    out("run uses them. Only the OASDI wage-base sensitivity updates ($168,600 -> $176,100,")
    out("IRS Publication 15 2024 and 2025). Nominal income grew between the two income years")
    out("while per-pupil cost and rent are held fixed, so the K-12 and renter items are")
    out("understated in real terms on the 2026 file; the columns are labelled accordingly.")

    frame = pd.DataFrame(rows)
    frame.to_csv(HERE / "ledger_2025_vs_2026.csv", index=False)
    (HERE / "ledger_2025_vs_2026_result.txt").write_text("\n".join(lines) + "\n")
    print(f"\nWrote {HERE / 'ledger_2025_vs_2026.csv'}")
    print(f"Wrote {HERE / 'ledger_2025_vs_2026_result.txt'}")


if __name__ == "__main__":
    main()
