"""Fiscal-plus-beside totals of the real-costs memo (sections 7 and 7b) on the September 23 and
September 24 cases.

Definitions: research/immigration-real-fiscal-and-social-costs-2026-09-23.md.
  §7   fiscal main case + crime victims' harm + property crime + unreimbursed hospital care
       + road congestion - housing net gain, on two crime footings: Mexican-origin rates equal to
       Hispanic (justice keyed on raw census codes, victims' equal-rate arm) and the custody ratio
       carried over (the adopted justice key, victims' ACS-institutional-ratio arm). Central values;
       the low end pairs the fiscal low end with the low social rows. The full span stacks the justice
       grid's low end, uncompensated care at 0.7x use, the victim envelope, congestion's range and the
       housing range, then the opposite ends.
  §7b  custody footing, three columns: costs only; with care and mobility (care leaves the fiscal row,
       mobility the social row); adding the proposed scale net to the fiscal row.
On September 24 care is inside the adopted case (decision 3, the package's care constant), so its
"costs only" column adds the constant back and its "with care" column is the adopted band.

The memo summed its table rows as printed (one decimal, halves rounded up); its full span used
unrounded rows. Gate: every September 23 figure the memo prints is reproduced by one of the two
methods, and the method is recorded. The September 24 figures are exact sums.

Inputs: derived/band_variants.csv (node band_variants.cjs, engine bands on both cases) and the channel
lanes' derived files (PATHS). Reads only; writes derived/real_costs_totals.csv and .json.
Run from the repository root, after band_variants.cjs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py
"""
from __future__ import annotations

import csv
import hashlib
import json
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
PATHS = dict(
    bands=HERE / "derived" / "band_variants.csv",
    bands_meta=HERE / "derived" / "band_variants.json",
    main24=FISCAL / "main_case_2026_09_24/derived/summary.json",
    crime_offence=FISCAL / "crime_victim_cost_2026_09_23/derived/cost_by_offence_central.csv",
    crime_arms=FISCAL / "crime_victim_cost_2026_09_23/derived/arms.csv",
    crime_property=FISCAL / "crime_victim_cost_2026_09_23/derived/property_proxy.csv",
    crime_mixed=FISCAL / "crime_ratio_direction_2026_09_24/derived/dollar_effects.csv",
    uncompensated=FISCAL / "uncompensated_care_2026_09_23/derived/added_cost_arms.csv",
    congestion=FISCAL / "congestion_2026_09_23/derived/arms_summary.csv",
    housing=FISCAL / "housing_transfer_2026_09_23/derived/arms_summary.csv",
    care=FISCAL / "care_household_services_2026_09_23/derived/summary.csv",
    mobility=FISCAL / "labor_mobility_insurance_2026_09_23/derived/insurance_summary.json",
    scale=FISCAL / "scale_spillovers_2026_09_23/derived/summary.csv",
)
MIXED_METHOD = ("theta 0.4977 of each group attributed Hispanic "
                "(NIBRS TX+AZ mean Hispanic fraction of mixed groups)")
FAILURES: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}")
    if not ok:
        FAILURES.append(label)


def one(frame, mask, label):
    rows = frame[mask]
    gate(f"one row: {label}", len(rows) == 1, f"{len(rows)} rows")
    return rows.iloc[0]


def channels():
    """Every social row and benefit the memo uses, read from its lane."""
    off = pd.read_csv(PATHS["crime_offence"]).set_index("offence")
    arms = pd.read_csv(PATHS["crime_arms"]).set_index("arm")
    prop = pd.read_csv(PATHS["crime_property"]).groupby("price_set").cost.sum() / 1e9
    mixed = pd.read_csv(PATHS["crime_mixed"])
    unc = pd.read_csv(PATHS["uncompensated"])
    cong = pd.read_csv(PATHS["congestion"])
    hous = pd.read_csv(PATHS["housing"])
    care = pd.read_csv(PATHS["care"]).set_index("channel")
    mob = json.loads(PATHS["mobility"].read_text())
    scale = pd.read_csv(PATHS["scale"])
    b1 = one(cong, cong.approach == "B1 population elasticity, lanes fixed", "congestion B1")
    net = one(hous, (hous.arm == "long_run") & (hous.metric == "net_other_residents_welfare_bn"), "housing long-run net")
    joint = one(scale, (scale.table == "joint_grid") & (scale.geography == "CZ 1990"), "scale joint grid, CZ 1990")
    out1, out7 = unc[unc.use_intensity == 1.0].outside_accounts_bn, unc[unc.use_intensity == 0.7].outside_accounts_bn
    c = dict(
        victims_equal=float(off.loc["Total", "cost_full"]) / 1e9,
        victims_custody=float(arms.loc["scaling: ACS institutional ratio 1.118 (generic reallocated)", "full_bn"]),
        victims_envelope_low=float(arms.loc["ENVELOPE low, miller2021", "full_bn"]),
        victims_envelope_high=float(arms.loc["ENVELOPE high, miller2021_dot_vsl", "full_bn"]),
        victims_equal_mixed_group=float(one(mixed, mixed.method == MIXED_METHOD, "mixed-group correction").full_bn),
        property_low=float(prop["miller2021"]), property_high=float(prop["mccollister2010"]),
        unreimbursed_low=float(out1.min()), unreimbursed_high=float(out1.max()),
        unreimbursed_07_low=float(out7.min()), unreimbursed_07_high=float(out7.max()),
        congestion=float(b1.central_bn), congestion_low=float(b1.min_bn), congestion_high=float(b1.max_bn),
        housing_gain_metro_local=float(net.central_metro_local), housing_gain_national=float(net.central_national_uniform),
        housing_gain_max=float(net.max_ABC), housing_gain_min=float(net.min_ABC),
        care=float(care.loc["TOTAL of additive channels", "central_bn"]),
        mobility=float(mob["lane_total_present_bn"]["central"]),
        scale_net=float(joint.gain_bn),
    )
    # The sister ledger lane (winners_losers_2026_09_24, crime_inputs) scales the mixed-group
    # correction to the custody footing by the custody arm's ratio; the victim lane has not computed it.
    c["victims_custody_mixed_scaled"] = c["victims_equal_mixed_group"] * c["victims_custody"] / c["victims_equal"]
    return c


def social(c, victims, printed=False):
    """§7's social rows at the low and high end of the central values (low end: largest housing gain)."""
    if printed:
        r = lambda x: float(Decimal(repr(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))  # noqa: E731
        return (r(victims) + r(c["property_low"]) + r(c["unreimbursed_low"]) + r(c["congestion"])
                - r(c["housing_gain_metro_local"]),
                r(victims) + r(c["property_high"]) + r(c["unreimbursed_high"]) + r(c["congestion"])
                - r(c["housing_gain_national"]))
    return (victims + c["property_low"] + c["unreimbursed_low"] + c["congestion"] - c["housing_gain_metro_local"],
            victims + c["property_high"] + c["unreimbursed_high"] + c["congestion"] - c["housing_gain_national"])


def span_ends(c, low_fiscal, high_fiscal):
    low = (low_fiscal + c["victims_envelope_low"] + c["property_low"] + c["unreimbursed_07_low"]
           + c["congestion_low"] - c["housing_gain_max"])
    high = (high_fiscal + c["victims_envelope_high"] + c["property_high"] + c["unreimbursed_high"]
            + c["congestion_high"] - c["housing_gain_min"])
    return low, high


def half_up(x, places):
    # Rounding to 9 places first removes float noise from sums of one-decimal rows (57.8 - 0.65).
    return float(Decimal(repr(round(float(x), 9))).quantize(Decimal(1).scaleb(-places), ROUND_HALF_UP))


def main():
    bands = pd.read_csv(PATHS["bands"]).set_index(["case", "variant"])
    meta = json.loads(PATHS["bands_meta"].read_text())
    main24 = json.loads(PATHS["main24"].read_text())
    pop_m = meta["target_population"] / 1e6
    band = lambda case, v: (float(bands.loc[(case, v), "cost_low_bn"]), float(bands.loc[(case, v), "cost_high_bn"]))  # noqa: E731
    print("[inputs]")
    c = channels()
    care24 = -meta["care_constant_bn"]
    gate("care constant is the package's -4.15 and the lane's total rounds to it", care24 == 4.15 and round(c["care"], 2) == 4.15,
         f"{care24} / {c['care']:.4f}")
    gate("band file's adopted September 24 band equals main_case summary.json",
         all(abs(a - b) < 1e-9 for a, b in zip(band("sept24", "adopted"), main24["main_case"])))

    rows = []

    def add(section, column, item, s23, s24, memo=None, method=None, unit="bn", note=""):
        rows.append(dict(section=section, column=column, item=item, unit=unit, memo_printed=memo,
                         memo_method=method, sept23=s23, sept24=s24, change=None if s23 is None or s24 is None else s24 - s23,
                         note=note))

    def check(label, exact, printed_rows, memo, places):
        """Which method reproduces the memo's printed figure (exact first)."""
        if half_up(exact, places) == memo:
            return "exact"
        if printed_rows is not None and half_up(printed_rows, places) == memo:
            return "printed rows"
        gate(f"memo figure reproduced: {label}", False, f"memo {memo}, exact {exact:.4f}, printed rows {printed_rows}")
        return None

    fiscal = {case: {"hispanic": band(case, "justice_raw_coding"), "custody": band(case, "adopted")}
              for case in ("sept23", "sept24")}
    victims = {"hispanic": c["victims_equal"], "custody": c["victims_custody"]}
    memo7 = {"hispanic": dict(fiscal=(198.9, 245.4), total=(248, 300), per=(6.1, 7.3)),
             "custody": dict(fiscal=(203.2, 249.6), total=(256, 307), per=(6.3, 7.5))}
    print("[§7: central values on two footings]")
    for col in ("hispanic", "custody"):
        soc = social(c, victims[col])
        soc_p = social(c, victims[col], printed=True)
        f23, f24 = fiscal["sept23"][col], fiscal["sept24"][col]
        for i, end in enumerate(("low", "high")):
            m = memo7[col]
            fp = half_up(f23[i], 1)
            add("7", col, f"fiscal main case ({end})", f23[i], f24[i], m["fiscal"][i], check(f"§7 {col} fiscal {end}", f23[i], None, m["fiscal"][i], 1))
            t23, t24, tp = f23[i] + soc[i], f24[i] + soc[i], fp + soc_p[i]
            add("7", col, f"total at central values ({end})", t23, t24, m["total"][i], check(f"§7 {col} total {end}", t23, tp, m["total"][i], 0))
            add("7", col, f"per group member ({end})", t23 / pop_m, t24 / pop_m, m["per"][i],
                check(f"§7 {col} per member {end}", t23 / pop_m, tp / pop_m, m["per"][i], 1), unit="$k")
        mv = {"hispanic": 28.9, "custody": 32.3}[col]
        add("7", col, "victims' harm, full cost", victims[col], victims[col], mv, check(f"§7 {col} victims", victims[col], None, mv, 1))
    # Hispanic footing with ladder 218's mixed-group correction (decision 4 quotes $30.9bn beside the account).
    socm = social(c, c["victims_equal_mixed_group"])
    for i, end in enumerate(("low", "high")):
        f = fiscal["sept24"]["hispanic"][i]
        add("7", "hispanic_mixed_group", f"total at central values ({end})", None, f + socm[i],
            note="victims 30.93 (ladder 218 mixed-group correction); decision 4's figure")
        add("7", "hispanic_mixed_group", f"per group member ({end})", None, (f + socm[i]) / pop_m, unit="$k")
    # Custody footing with the sister lane's scaled mixed-group victims.
    socs = social(c, c["victims_custody_mixed_scaled"])
    for i, end in enumerate(("low", "high")):
        f = fiscal["sept24"]["custody"][i]
        add("7", "custody_mixed_scaled", f"total at central values ({end})", None, f + socs[i],
            note="victims 34.58 = 30.93 x 32.34/28.92 (winners_losers_2026_09_24 crime_inputs; not a lane arm)")

    print("[§7: full span]")
    lo23, hi23 = span_ends(c, band("sept23", "justice_grid_low_and_uncompensated_use_0.7")[0], band("sept23", "justice_grid_high")[1])
    lo24, hi24 = span_ends(c, band("sept24", "justice_grid_low_and_uncompensated_use_0.7")[0], band("sept24", "justice_grid_high")[1])
    add("7", "full_span", "low end", lo23, lo24, 212, check("§7 full span low", lo23, None, 212, 0))
    add("7", "full_span", "high end", hi23, hi24, 340, check("§7 full span high", hi23, None, 340, 0))
    add("7", "full_span", "per group member, low", lo23 / pop_m, lo24 / pop_m, 5.2, check("§7 span per member low", lo23 / pop_m, None, 5.2, 1), unit="$k")
    add("7", "full_span", "per group member, high", hi23 / pop_m, hi24 / pop_m, 8.3, check("§7 span per member high", hi23 / pop_m, None, 8.3, 1), unit="$k")
    # The adopted case's own component range ($172.3-276.1bn) stacked as well; its justice component
    # (row 7 year, booking factor) shares the arrest-ratio dimension with the grid, so this may double count.
    rng = main24["range"]["overall"]
    a24 = band("sept24", "adopted")
    lo_r, hi_r = span_ends(c, rng[0] + band("sept24", "justice_grid_low_and_uncompensated_use_0.7")[0] - a24[0],
                           rng[1] + band("sept24", "justice_grid_high")[1] - a24[1])
    add("7", "full_span_with_package_range", "low end", None, lo_r, note="adds main_case_2026_09_24 range; may double count the arrest ratio")
    add("7", "full_span_with_package_range", "high end", None, hi_r, note="adds main_case_2026_09_24 range; may double count the arrest ratio")

    print("[§7b: custody footing, benefits priced]")
    soc = social(c, c["victims_custody"])
    soc_p = social(c, c["victims_custody"], printed=True)
    f23, f24 = fiscal["sept23"]["custody"], fiscal["sept24"]["custody"]
    r1 = lambda x: half_up(x, 1)  # noqa: E731
    cols = {
        # column: (fiscal 23 exact, fiscal 24 exact, fiscal 23 printed, social shift exact, social shift printed)
        "costs_only": (f23, (f24[0] + care24, f24[1] + care24), (r1(f23[0]), r1(f23[1])), 0.0, 0.0),
        "with_care_and_mobility": ((f23[0] - c["care"], f23[1] - c["care"]), f24,
                                   (r1(f23[0]) - r1(c["care"]), r1(f23[1]) - r1(c["care"])), c["mobility"], 0.65),
        "adding_scale_net": ((f23[0] - c["care"] - c["scale_net"], f23[1] - c["care"] - c["scale_net"]),
                             (f24[0] - c["scale_net"], f24[1] - c["scale_net"]),
                             (r1(f23[0]) - r1(c["care"]) - r1(c["scale_net"]), r1(f23[1]) - r1(c["care"]) - r1(c["scale_net"])),
                             c["mobility"], 0.65),
    }
    memo7b = {"costs_only": dict(fiscal=(203.2, 249.6), social=(52.5, 57.8), total=(256, 307), per=(6.3, 7.5)),
              "with_care_and_mobility": dict(fiscal=(199.1, 245.5), social=(51.9, 57.2), total=(251, 303), per=(6.1, 7.4)),
              "adding_scale_net": dict(fiscal=(185.2, 231.6), social=(51.9, 57.2), total=(237, 289), per=(5.8, 7.1))}
    for col, (x23, x24, xp, sh, shp) in cols.items():
        m = memo7b[col]
        for i, end in enumerate(("low", "high")):
            s_ex, s_pr = soc[i] - sh, soc_p[i] - shp
            add("7b", col, f"fiscal main case ({end})", x23[i], x24[i], m["fiscal"][i], check(f"§7b {col} fiscal {end}", x23[i], xp[i], m["fiscal"][i], 1))
            add("7b", col, f"social items beside the account ({end})", s_ex, s_ex, m["social"][i], check(f"§7b {col} social {end}", s_ex, s_pr, m["social"][i], 1))
            t23, t24, tp = x23[i] + s_ex, x24[i] + s_ex, xp[i] + s_pr
            add("7b", col, f"total at central values ({end})", t23, t24, m["total"][i], check(f"§7b {col} total {end}", t23, tp, m["total"][i], 0))
            add("7b", col, f"per group member ({end})", t23 / pop_m, t24 / pop_m, m["per"][i], check(f"§7b {col} per member {end}", t23 / pop_m, tp / pop_m, m["per"][i], 1), unit="$k")
    om23, om24 = c["care"] + c["mobility"], c["mobility"]
    add("7b", "omitted_benefits", "without the scale net", om23, om24, 4.8, check("§7b omitted", om23, None, 4.8, 1),
        note="September 24: care is inside the account, mobility alone remains")
    add("7b", "omitted_benefits", "with the scale net", om23 + c["scale_net"], om24 + c["scale_net"], 18.7, check("§7b omitted with scale", om23 + c["scale_net"], None, 18.7, 1))
    add("7b", "omitted_benefits", "share of main case, low (%)", 100 * om23 / f23[1], 100 * om24 / f24[1], 2, check("§7b share low", 100 * om23 / f23[1], None, 2, 0), unit="%")
    add("7b", "omitted_benefits", "share of main case, high (%)", 100 * (om23 + c["scale_net"]) / f23[0],
        100 * (om24 + c["scale_net"]) / f24[0], 9, check("§7b share high", 100 * (om23 + c["scale_net"]) / f23[0], None, 9, 0), unit="%")
    # The memo's 2026-09-24 revision: "about $253-304bn [200.9 + 51.9; 246.3 + 57.2]".
    rev = [f24[i] + soc[i] - c["mobility"] for i in (0, 1)]
    add("revision_2026_09_24", "with_care_and_mobility", "total, low", None, rev[0], 253, None, note="memo: 200.9 + 51.9")
    add("revision_2026_09_24", "with_care_and_mobility", "total, high", None, rev[1], 304, None, note="memo: 246.3 + 57.2 (printed rows)")

    unmatched = [r for r in rows if r["memo_printed"] is not None and r["sept23"] is not None and r["memo_method"] is None]
    gate("every September 23 figure the memo prints is reproduced", not unmatched, f"{len(unmatched)} unmatched")
    if FAILURES:
        raise SystemExit(f"[BLOCKED] {len(FAILURES)} gate(s) failed: {FAILURES}")

    out = HERE / "derived" / "real_costs_totals.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    shas = {str(p.relative_to(FISCAL)): hashlib.sha256(p.read_bytes()).hexdigest() for p in PATHS.values()}
    (HERE / "derived" / "real_costs_totals.json").write_text(json.dumps(
        dict(channels=c, target_population_m=pop_m, care_constant_bn=care24, sources_sha256=shas), indent=1) + "\n")
    print("\n[result]")
    for r in rows:
        s23 = "" if r["sept23"] is None else f"{r['sept23']:9.3f}"
        print(f"  {r['section']:>4} {r['column']:<30} {r['item']:<42} {str(r['memo_printed'] or ''):>6} "
              f"{str(r['memo_method'] or ''):<12} {s23:>9} -> {r['sept24']:9.3f} {r['unit']}")
    print(f"all gates passed; {len(rows)} rows -> {out.relative_to(HERE.parents[2])}")


if __name__ == "__main__":
    main()
