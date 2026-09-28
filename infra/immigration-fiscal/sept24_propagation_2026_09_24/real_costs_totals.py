"""Fiscal-plus-beside totals of the real-costs memo (sections 7 and 7b) on the September 23 case and
the adopted cases since.

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
From September 24 on care is inside the adopted case (decision 3, the package's care constant), so
the "costs only" column adds the constant back and the "with care" column is the adopted band.

The memo summed its table rows as printed (one decimal, halves rounded up); its full span used
unrounded rows. Gate: every September 23 figure the memo prints is reproduced by one of the two
methods, and the method is recorded. The figures of the adopted cases are exact sums.

Cases (--case, as in band_variants.cjs). sept24 writes the September 23 and September 24 columns to
derived/ (the committed run). sept26 (the one-year scenario; --out-dir DIR only), sept26_schools
(schools at full average cost; ../sept26_propagation_2026_09_26/derived/) and sept27 (the main case; the
default, ../sept27_propagation_2026_09_27/derived/) add the case's column, and `change` is then the case
minus September 24. The rows the memo prints only for September 24 (the mixed-group victims, the
package's own range) are computed on every adopted case; the memo's 2026-09-24 revision note stays a
September 24 figure.

September 27: roads respond in the long run, so road congestion beside the account is re-derived with the
network following spending (the response lane's net_change.json, which the payload's
meta.beside_the_account.congestion quotes): $13.99bn at the low band end and $12.02bn at the high end in
place of the congestion lane's $19.16bn, and in the full span each end's own range (2.01 at the low end,
30.83 at the high end) in place of 8.05-35.25. Every earlier case keeps the congestion lane's figures. The
case's fiscal row includes the return on public capital (band_variants.cjs). Rows `capital_at_7pct` and
`enterprises_out_option_a` in section 7 are variants beside the central total, never in it: the fiscal
band at the reported 7% on every component, and option A (enterprises out), each with the case's social
items.

September 28 (decision 2026-09-28-social-items-fear-security-schools): the cases in SOCIAL_ITEMS add the
union's fear and avoidance, private security and school disruption (social_costs_unpriced_2026_09_28,
derived/items.csv) to the social rows, their central sum at both ends of the central values and their stacked
low and high at the ends of the full span. Property values stay out. Earlier cases keep their rows.

Inputs: DIR/band_variants.csv (node band_variants.cjs --case CASE: engine bands on the September 23 case,
September 24 and the case) and the channel lanes' derived files (PATHS). Reads only; writes
DIR/real_costs_totals.csv and .json. Run from the repository root, after band_variants.cjs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py [--case sept24|sept26|sept26_schools|sept27] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
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
# Each case's main-case lane and default output directory (None: --out-dir only), as in band_variants.cjs.
LANES = dict(sept24="main_case_2026_09_24", sept26="main_case_2026_09_26",
             sept26_schools="main_case_schools_full_2026_09_26", sept27="main_case_long_run_2026_09_27")
OUT_DIRS = dict(sept24=HERE / "derived", sept26=None, sept26_schools=FISCAL / "sept26_propagation_2026_09_26" / "derived",
                sept27=FISCAL / "sept27_propagation_2026_09_27" / "derived")
# Cases whose roads respond: congestion beside the account is the response lane's, by band end.
LONG_RUN = dict(sept27=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json")
# Cases whose social rows carry the union's three added social items (decision 2026-09-28).
SOCIAL_ITEMS = dict(sept27=FISCAL / "social_costs_unpriced_2026_09_28/derived/items.csv")
SOCIAL_ITEM_IDS = ("fear_avoidance", "private_security", "school_disruption")
# Runs of band_variants.cjs beside a case, never in its band (the case's column; the row label, its note).
BESIDE = dict(capital_at_7pct=("capital_at_7pct", "the return on public capital at the reported 7% on every component; "
                               "beside the central total, never in it"),
              enterprises_out_option_a=("enterprises_out_option_a", "option A: no enterprise capital, the enterprise "
                                        "surplus receipt at 0; beside the central total, never in it"))
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


def social(c, victims, printed=False, congestion=None, items=0.0):
    """§7's social rows at the low and high end of the central values (low end: largest housing gain).
    congestion: (low end, high end), the case's own when its roads respond; default the lane's central.
    items: the added social items' central sum, at both ends (0 for cases before September 28)."""
    if printed:
        r = lambda x: float(Decimal(repr(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))  # noqa: E731
        return (r(victims) + r(c["property_low"]) + r(c["unreimbursed_low"]) + r(c["congestion"])
                - r(c["housing_gain_metro_local"]),
                r(victims) + r(c["property_high"]) + r(c["unreimbursed_high"]) + r(c["congestion"])
                - r(c["housing_gain_national"]))
    cong_low, cong_high = congestion or (c["congestion"], c["congestion"])
    return (victims + c["property_low"] + c["unreimbursed_low"] + cong_low - c["housing_gain_metro_local"] + items,
            victims + c["property_high"] + c["unreimbursed_high"] + cong_high - c["housing_gain_national"] + items)


def span_ends(c, low_fiscal, high_fiscal, congestion=None, items=(0.0, 0.0)):
    """congestion: (lowest at the low end, highest at the high end); default the lane's range.
    items: the added social items' stacked (low, high), 0 for cases before September 28."""
    cong_low, cong_high = congestion or (c["congestion_low"], c["congestion_high"])
    low = (low_fiscal + c["victims_envelope_low"] + c["property_low"] + c["unreimbursed_07_low"]
           + cong_low - c["housing_gain_max"] + items[0])
    high = (high_fiscal + c["victims_envelope_high"] + c["property_high"] + c["unreimbursed_high"]
            + cong_high - c["housing_gain_min"] + items[1])
    return low, high


def social_items(path):
    """The union's added social items from the lane's items.csv: (central, stacked low, stacked high), $bn."""
    items = pd.read_csv(path)
    rows = items[(items.group == "mexican_origin") & items["item"].isin(SOCIAL_ITEM_IDS)]
    gate("social items: one row per added item for the union", sorted(rows["item"]) == sorted(SOCIAL_ITEM_IDS),
         f"{len(rows)} rows")
    return float(rows.central_bn.sum()), float(rows.low_bn.sum()), float(rows.high_bn.sum())


def half_up(x, places):
    # Rounding to 9 places first removes float noise from sums of one-decimal rows (57.8 - 0.65).
    return float(Decimal(repr(round(float(x), 9))).quantize(Decimal(1).scaleb(-places), ROUND_HALF_UP))


def parse_args():
    ap = argparse.ArgumentParser(description="Real-costs totals (memo §7, §7b) on an adopted main case.")
    ap.add_argument("--case", choices=tuple(LANES), default="sept27",
                    help="sept27: the main case (default); sept26_schools: schools at full average cost; sept26: the "
                         "one-year scenario (--out-dir only); sept24: the committed September 24 run")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="the directory band_variants.cjs wrote this case's bands to; the outputs go there too")
    args = ap.parse_args()
    args.out_dir = args.out_dir or OUT_DIRS[args.case]
    if args.out_dir is None:
        ap.error(f"--case {args.case} writes only to --out-dir DIR")
    args.out_dir = args.out_dir.resolve()
    return args


def rel(p: Path) -> str:
    return str(p.relative_to(FISCAL)) if p.is_relative_to(FISCAL) else str(p)


def main():
    args = parse_args()
    case, out_dir = args.case, args.out_dir
    later = case != "sept24"
    cols = ("sept23", "sept24") + ((case,) if later else ())   # `change` is the last column minus the one before
    adopted = cols[1:]                                         # the cases with a corrections payload
    paths = dict(PATHS, bands=out_dir / "band_variants.csv", bands_meta=out_dir / "band_variants.json")
    if later:
        paths["main_case"] = FISCAL / LANES[case] / "derived" / "summary.json"
    if case in LONG_RUN:
        paths.update(case_corrections=FISCAL / LANES[case] / "derived" / "corrections.json", congestion_long_run=LONG_RUN[case])
    if case in SOCIAL_ITEMS:
        paths["social_items"] = SOCIAL_ITEMS[case]
    bands = pd.read_csv(paths["bands"]).set_index(["case", "variant"])
    meta = json.loads(paths["bands_meta"].read_text())
    summaries = dict(sept24=json.loads(paths["main24"].read_text()))
    if later:
        summaries[case] = json.loads(paths["main_case"].read_text())
    pop_m = meta["target_population"] / 1e6
    band = lambda k, v: (float(bands.loc[(k, v), "cost_low_bn"]), float(bands.loc[(k, v), "cost_high_bn"]))  # noqa: E731
    print("[inputs]")
    c = channels()
    care24 = -meta["care_constant_bn"]
    gate("care constant is the package's -4.15 and the lane's total rounds to it", care24 == 4.15 and round(c["care"], 2) == 4.15,
         f"{care24} / {c['care']:.4f}")
    gate(f"band file is the {case} run", meta.get("case", "sept24") == case, rel(paths["bands_meta"]))
    for k in adopted:
        gate(f"band file's adopted {k} band equals {LANES[k]} summary.json",
             all(abs(a - b) < 1e-9 for a, b in zip(band(k, "adopted"), summaries[k]["main_case"])))
    # Road congestion beside the account: (low end, high end) for the central values and for the full span.
    # None keeps the congestion lane's central and range; a case whose roads respond takes the response
    # lane's figures by band end.
    cong = {k: None for k in cols}
    cong_span = {k: None for k in cols}
    if case in LONG_RUN:
        nc = json.loads(paths["congestion_long_run"].read_text())
        quoted = json.loads(paths["case_corrections"].read_text())["meta"]["beside_the_account"]["congestion"]
        e = nc["by_band_end"]
        cong[case] = (e["low"]["congestion_bn"], e["high"]["congestion_bn"])
        cong_span[case] = (e["low"]["congestion_range_bn"][0], e["high"]["congestion_range_bn"][1])
        gate("the payload quotes the response lane's congestion at both band ends",
             (quoted["low_end_bn"], quoted["high_end_bn"]) == cong[case] and quoted["before_bn"] == nc["b1_lanes_fixed_bn"],
             f"{cong[case][0]:.4f} / {cong[case][1]:.4f}")
        gate("the response lane starts from the congestion lane's B1 central and range",
             abs(nc["b1_lanes_fixed_bn"] - c["congestion"]) < 1e-9
             and all(abs(a - b) < 1e-9 for a, b in zip(nc["b1_factorial_bn"], (c["congestion_low"], c["congestion_high"]))),
             f"{nc['b1_lanes_fixed_bn']:.4f}, {nc['b1_factorial_bn'][0]:.4f}-{nc['b1_factorial_bn'][1]:.4f}")
        for run in BESIDE:
            gate(f"band file has the {case}_{run} run beside the case", (f"{case}_{run}", "adopted") in bands.index)
    # The added social items by case: (central, stacked low, stacked high); zero before September 28.
    items = {k: (0.0, 0.0, 0.0) for k in cols}
    if case in SOCIAL_ITEMS:
        items[case] = social_items(paths["social_items"])

    rows = []

    def add(section, column, item, vals, memo=None, method=None, unit="bn", note=""):
        """vals: {case: value}; a case it leaves out is blank."""
        v = [vals.get(k) for k in cols]
        rows.append(dict(section=section, column=column, item=item, unit=unit, memo_printed=memo, memo_method=method,
                         **dict(zip(cols, v)), change=None if v[-1] is None or v[-2] is None else v[-1] - v[-2], note=note))

    def check(label, exact, printed_rows, memo, places):
        """Which method reproduces the memo's printed figure (exact first)."""
        if half_up(exact, places) == memo:
            return "exact"
        if printed_rows is not None and half_up(printed_rows, places) == memo:
            return "printed rows"
        gate(f"memo figure reproduced: {label}", False, f"memo {memo}, exact {exact:.4f}, printed rows {printed_rows}")
        return None

    fiscal = {k: {"hispanic": band(k, "justice_raw_coding"), "custody": band(k, "adopted")} for k in cols}
    victims = {"hispanic": c["victims_equal"], "custody": c["victims_custody"]}
    memo7 = {"hispanic": dict(fiscal=(198.9, 245.4), total=(248, 300), per=(6.1, 7.3)),
             "custody": dict(fiscal=(203.2, 249.6), total=(256, 307), per=(6.3, 7.5))}
    per_member = lambda vals: {k: v / pop_m for k, v in vals.items()}  # noqa: E731
    print("[§7: central values on two footings]")
    for col in ("hispanic", "custody"):
        soc = {k: social(c, victims[col], congestion=cong[k], items=items[k][0]) for k in cols}
        soc_p = social(c, victims[col], printed=True)
        f23 = fiscal["sept23"][col]
        for i, end in enumerate(("low", "high")):
            m = memo7[col]
            fp = half_up(f23[i], 1)
            add("7", col, f"fiscal main case ({end})", {k: fiscal[k][col][i] for k in cols}, m["fiscal"][i],
                check(f"§7 {col} fiscal {end}", f23[i], None, m["fiscal"][i], 1))
            t, tp = {k: fiscal[k][col][i] + soc[k][i] for k in cols}, fp + soc_p[i]
            add("7", col, f"total at central values ({end})", t, m["total"][i], check(f"§7 {col} total {end}", t["sept23"], tp, m["total"][i], 0))
            add("7", col, f"per group member ({end})", per_member(t), m["per"][i],
                check(f"§7 {col} per member {end}", t["sept23"] / pop_m, tp / pop_m, m["per"][i], 1), unit="$k")
        mv = {"hispanic": 28.9, "custody": 32.3}[col]
        add("7", col, "victims' harm, full cost", {k: victims[col] for k in cols}, mv, check(f"§7 {col} victims", victims[col], None, mv, 1))
    # Hispanic footing with ladder 218's mixed-group correction (decision 4 quotes $30.9bn beside the account).
    socm = {k: social(c, c["victims_equal_mixed_group"], congestion=cong[k], items=items[k][0]) for k in adopted}
    for i, end in enumerate(("low", "high")):
        t = {k: fiscal[k]["hispanic"][i] + socm[k][i] for k in adopted}
        add("7", "hispanic_mixed_group", f"total at central values ({end})", t,
            note="victims 30.93 (ladder 218 mixed-group correction); decision 4's figure")
        add("7", "hispanic_mixed_group", f"per group member ({end})", per_member(t), unit="$k")
    # Custody footing with the sister lane's scaled mixed-group victims.
    socs = {k: social(c, c["victims_custody_mixed_scaled"], congestion=cong[k], items=items[k][0]) for k in adopted}
    for i, end in enumerate(("low", "high")):
        add("7", "custody_mixed_scaled", f"total at central values ({end})", {k: fiscal[k]["custody"][i] + socs[k][i] for k in adopted},
            note="victims 34.58 = 30.93 x 32.34/28.92 (winners_losers_2026_09_24 crime_inputs; not a lane arm)")

    print("[§7: full span]")
    ends = {k: span_ends(c, band(k, "justice_grid_low_and_uncompensated_use_0.7")[0], band(k, "justice_grid_high")[1],
                         congestion=cong_span[k], items=items[k][1:]) for k in cols}
    lo, hi = {k: e[0] for k, e in ends.items()}, {k: e[1] for k, e in ends.items()}
    add("7", "full_span", "low end", lo, 212, check("§7 full span low", lo["sept23"], None, 212, 0))
    add("7", "full_span", "high end", hi, 340, check("§7 full span high", hi["sept23"], None, 340, 0))
    add("7", "full_span", "per group member, low", per_member(lo), 5.2, check("§7 span per member low", lo["sept23"] / pop_m, None, 5.2, 1), unit="$k")
    add("7", "full_span", "per group member, high", per_member(hi), 8.3, check("§7 span per member high", hi["sept23"] / pop_m, None, 8.3, 1), unit="$k")
    # Each adopted case's own component range (September 24: $172.3-276.1bn) stacked as well; its justice
    # component (row 7 year, booking factor) shares the arrest-ratio dimension with the grid, so this may
    # double count.
    lo_r, hi_r = {}, {}
    for k in adopted:
        rng, a = summaries[k]["range"]["overall"], band(k, "adopted")
        lo_r[k], hi_r[k] = span_ends(c, rng[0] + band(k, "justice_grid_low_and_uncompensated_use_0.7")[0] - a[0],
                                     rng[1] + band(k, "justice_grid_high")[1] - a[1], congestion=cong_span[k],
                                     items=items[k][1:])
    note = ("adds main_case_2026_09_24 range; may double count the arrest ratio" if not later else
            f"adds each case's own range ({', '.join(LANES[k] for k in adopted)}); may double count the arrest ratio")
    add("7", "full_span_with_package_range", "low end", lo_r, note=note)
    add("7", "full_span_with_package_range", "high end", hi_r, note=note)
    if case in SOCIAL_ITEMS:
        note = ("the union's fear and avoidance, private security and school disruption (social_costs_unpriced_2026_09_28), "
                "in every social row above; property values stay out; decision 2026-09-28")
        for label, v in zip(("central, both ends", "stacked low, full span", "stacked high, full span"), items[case]):
            add("7", "social_items_2026_09_28", label, {case: v}, note=note)
    if case in LONG_RUN:
        # The case's runs beside it: the same social items (the case's congestion), never in the central total.
        # The published pairing is the case's: decision 4's victims on the Hispanic footing at the low end, the
        # custody footing at the high end.
        print("[§7: variants beside the central total]")
        for run, (column, note) in BESIDE.items():
            k = f"{case}_{run}"
            f_cust, f_hisp = band(k, "adopted"), band(k, "justice_raw_coding")
            s_cust = social(c, victims["custody"], congestion=cong[case], items=items[case][0])
            s_hisp = social(c, victims["hispanic"], congestion=cong[case], items=items[case][0])
            s_mixed = social(c, c["victims_equal_mixed_group"], congestion=cong[case], items=items[case][0])
            for i, end in enumerate(("low", "high")):
                add("7", column, f"fiscal main case ({end})", {case: f_cust[i]}, note=note)
                add("7", column, f"total at central values, custody footing ({end})", {case: f_cust[i] + s_cust[i]}, note=note)
                add("7", column, f"total at central values, Hispanic footing ({end})", {case: f_hisp[i] + s_hisp[i]}, note=note)
            pairing = (f_hisp[0] + s_mixed[0], f_cust[1] + s_cust[1])
            for i, end in enumerate(("low", "high")):
                add("7", column, f"published pairing ({end})", {case: pairing[i]},
                    note=note + ("; decision 4's victims on the Hispanic footing" if i == 0 else "; custody footing"))
                add("7", column, f"published pairing per group member ({end})", {case: pairing[i] / pop_m}, unit="$k", note=note)

    print("[§7b: custody footing, benefits priced]")
    soc = {k: social(c, c["victims_custody"], congestion=cong[k], items=items[k][0]) for k in cols}
    soc_p = social(c, c["victims_custody"], printed=True)
    f23 = fiscal["sept23"]["custody"]
    fa = {k: fiscal[k]["custody"] for k in adopted}
    r1 = lambda x: half_up(x, 1)  # noqa: E731
    cols7b = {
        # column: (fiscal by case, exact; fiscal 23 printed; social shift exact; social shift printed)
        "costs_only": (dict(sept23=f23, **{k: (f[0] + care24, f[1] + care24) for k, f in fa.items()}),
                       (r1(f23[0]), r1(f23[1])), 0.0, 0.0),
        "with_care_and_mobility": (dict(sept23=(f23[0] - c["care"], f23[1] - c["care"]), **fa),
                                   (r1(f23[0]) - r1(c["care"]), r1(f23[1]) - r1(c["care"])), c["mobility"], 0.65),
        "adding_scale_net": (dict(sept23=(f23[0] - c["care"] - c["scale_net"], f23[1] - c["care"] - c["scale_net"]),
                                  **{k: (f[0] - c["scale_net"], f[1] - c["scale_net"]) for k, f in fa.items()}),
                             (r1(f23[0]) - r1(c["care"]) - r1(c["scale_net"]), r1(f23[1]) - r1(c["care"]) - r1(c["scale_net"])),
                             c["mobility"], 0.65),
    }
    memo7b = {"costs_only": dict(fiscal=(203.2, 249.6), social=(52.5, 57.8), total=(256, 307), per=(6.3, 7.5)),
              "with_care_and_mobility": dict(fiscal=(199.1, 245.5), social=(51.9, 57.2), total=(251, 303), per=(6.1, 7.4)),
              "adding_scale_net": dict(fiscal=(185.2, 231.6), social=(51.9, 57.2), total=(237, 289), per=(5.8, 7.1))}
    for col, (x, xp, sh, shp) in cols7b.items():
        m = memo7b[col]
        for i, end in enumerate(("low", "high")):
            s_ex, s_pr = {k: soc[k][i] - sh for k in cols}, soc_p[i] - shp
            add("7b", col, f"fiscal main case ({end})", {k: v[i] for k, v in x.items()}, m["fiscal"][i],
                check(f"§7b {col} fiscal {end}", x["sept23"][i], xp[i], m["fiscal"][i], 1))
            add("7b", col, f"social items beside the account ({end})", s_ex, m["social"][i],
                check(f"§7b {col} social {end}", s_ex["sept23"], s_pr, m["social"][i], 1))
            t, tp = {k: v[i] + s_ex[k] for k, v in x.items()}, xp[i] + s_pr
            add("7b", col, f"total at central values ({end})", t, m["total"][i], check(f"§7b {col} total {end}", t["sept23"], tp, m["total"][i], 0))
            add("7b", col, f"per group member ({end})", per_member(t), m["per"][i],
                check(f"§7b {col} per member {end}", t["sept23"] / pop_m, tp / pop_m, m["per"][i], 1), unit="$k")
    om = dict(sept23=c["care"] + c["mobility"], **{k: c["mobility"] for k in adopted})
    oms = {k: v + c["scale_net"] for k, v in om.items()}
    add("7b", "omitted_benefits", "without the scale net", om, 4.8, check("§7b omitted", om["sept23"], None, 4.8, 1),
        note="September 24: care is inside the account, mobility alone remains" if not later
        else "From September 24 on care is inside the account; mobility alone remains")
    add("7b", "omitted_benefits", "with the scale net", oms, 18.7, check("§7b omitted with scale", oms["sept23"], None, 18.7, 1))
    low = {k: 100 * om[k] / fiscal[k]["custody"][1] for k in cols}
    high = {k: 100 * oms[k] / fiscal[k]["custody"][0] for k in cols}
    add("7b", "omitted_benefits", "share of main case, low (%)", low, 2, check("§7b share low", low["sept23"], None, 2, 0), unit="%")
    add("7b", "omitted_benefits", "share of main case, high (%)", high, 9, check("§7b share high", high["sept23"], None, 9, 0), unit="%")
    # The memo's 2026-09-24 revision: "about $253-304bn [200.9 + 51.9; 246.3 + 57.2]".
    rev = [fiscal["sept24"]["custody"][i] + soc["sept24"][i] - c["mobility"] for i in (0, 1)]
    add("revision_2026_09_24", "with_care_and_mobility", "total, low", dict(sept24=rev[0]), 253, None, note="memo: 200.9 + 51.9")
    add("revision_2026_09_24", "with_care_and_mobility", "total, high", dict(sept24=rev[1]), 304, None, note="memo: 246.3 + 57.2 (printed rows)")

    unmatched = [r for r in rows if r["memo_printed"] is not None and r["sept23"] is not None and r["memo_method"] is None]
    gate("every September 23 figure the memo prints is reproduced", not unmatched, f"{len(unmatched)} unmatched")
    if FAILURES:
        raise SystemExit(f"[BLOCKED] {len(FAILURES)} gate(s) failed: {FAILURES}")

    out = out_dir / "real_costs_totals.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    shas = {rel(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}
    doc = dict(channels=c, target_population_m=pop_m, care_constant_bn=care24, sources_sha256=shas)
    if later:
        doc = dict(case=case, columns=list(cols), **doc)
    if case in LONG_RUN:
        doc["congestion_by_band_end_bn"] = dict(
            case=case, central=dict(zip(("low_end", "high_end"), cong[case])),
            full_span=dict(zip(("low_end_lowest", "high_end_highest"), cong_span[case])),
            earlier_cases=dict(central=c["congestion"], full_span=[c["congestion_low"], c["congestion_high"]]),
            source=rel(LONG_RUN[case]))
        doc["beside_the_central_total"] = {f"{case}_{run}": note for run, (column, note) in BESIDE.items()}
    if case in SOCIAL_ITEMS:
        doc["social_items_in_the_social_rows"] = dict(
            case=case, items=list(SOCIAL_ITEM_IDS), central_bn=items[case][0], stacked_low_bn=items[case][1],
            stacked_high_bn=items[case][2], source=rel(SOCIAL_ITEMS[case]),
            decision="decisions/2026-09-28-social-items-fear-security-schools.md")
    (out_dir / "real_costs_totals.json").write_text(json.dumps(doc, indent=1) + "\n")
    print("\n[result]")
    fmt = lambda v: "" if v is None else f"{v:9.3f}"  # noqa: E731
    for r in rows:
        print(f"  {r['section']:>4} {r['column']:<30} {r['item']:<42} {str(r['memo_printed'] or ''):>6} "
              f"{str(r['memo_method'] or ''):<12} " + " -> ".join(f"{fmt(r[k]):>9}" for k in cols) + f" {r['unit']}")
    print(f"all gates passed; {len(rows)} rows -> {rel(out)}")


if __name__ == "__main__":
    main()
