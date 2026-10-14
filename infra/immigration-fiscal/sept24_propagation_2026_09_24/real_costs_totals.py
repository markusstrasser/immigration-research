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
unrounded rows. Gate: every September 23 figure the memo's first version printed (the memo7 and
memo7b constants; since 2026-09-29 the memo keeps the totals in its earlier-totals table) is
reproduced by one of the two methods, and the method is recorded. The figures of the adopted cases
are exact sums.

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
Later on September 28 (decision 2026-09-28-social-items-pollution-crashes) the same cases also add the union's
PM2.5 harm to other residents from its consumption (air_pollution_2026_09_28, pm25_consumption) and its road-crash
externality charged by fault (road_crash_externality_2026_09_28, road_crash_externality_fault_based), both at
their absolute (with against without) figures, in the same way. Their normalized figures, against as many
average residents, are reported beside and never added; so is the crash lane's but-for row, an alternative.
Later still (decision 2026-09-28-social-items-scale-benefits) the matching benefits of scale join the same rows as
negative costs: the scale lane's joint earnings effect (CZ 1990: bigger cities net of the group's schooling mix;
its normalized figure is the schooling-mix part, which remains against average residents) and restaurant market
size (disease_food_2026_09_28). Section 7b keeps only the cost items in its social rows, because its last column
adds the scale net itself. Three more benefits join the same way (decision 2026-09-28-social-items-more-benefits):
formal volunteering for people outside the group, consumer-side scale (network fixed costs, grocery variety and mix,
cross-group media) and trade, travel and FDI ties with Mexico.
On September 29 (decision 2026-09-29-crash-item-with-against-without) the crash item became the lane's but-for row
(road_crash_externality: other residents with against without the group's traffic, at traffic elasticities graded
from evidence plus the composition term). The fault-based row, damage in crashes the group's drivers cause, sits
beside and is never added.

Per-member rows divide by the population each column prices (September 29, population_basis_2026_09_29). The
September 23 case priced the published CPS union (band_variants.json target_population, 40,896,574); the adopted
cases price audit row 4's union (39,712,493; main_case_decomposition_2026_09_29/derived/headcount.csv). Their social
rows stay on the lanes' published union, except in column pairing_on_priced_count: the population lane's restatement
of the case's pairing with every row on row 4's count and the crash and congestion rows' NHTS ratios on persons aged
5+ (restated_pairing.csv, section pairing_5plus), after gates that the lane started from this script's own pairing
and divided by the same count.

September 29 (sept29, main_case_2026_09_29, candidate v4 adopted; derived/sept29/). The social rows are the
September 27 case's: the same items, and the long-run congestion figures, which the adopted lane flags as not
recomputed since v4 keyed roads by vehicle miles (summary.json beside_the_account.congestion.not_recomputed; the flag
is carried into the notes). The fiscal rows are the case's, from band_variants.cjs: its Hispanic footing re-prices the
state-priced justice line on the raw-coded key. Column pairing_on_priced_count takes the population lane's restated
social rows (section pairing_5plus less its fiscal row, which is the September 27 case's) and adds the case's own
fiscal rows, after gates that the lane's fiscal rows are the September 27 bands and its published social rows are this
script's social rows for the case. The cash set (the pension switch off) runs beside the case, with its own pairing on
the priced count, never in the central total.

October 5 (oct05, main_case_2026_10_05, v5 adopted; derived/oct05/). The fiscal rows price the lineage of 42.75M: the
union plus 3.04M descendants who no longer report Mexican origin. The pairing on the priced count adds their social
rows: each of the population lane's restated rows (the September 27 rows on audit row 4's union, crash and congestion
on the 5+ basis) times the added people's share of the engine key the row scales with, at the band end's
specification (band_variants.json lineage_social_keys: their amount over the union's on that key, priced at G3+
members' and third-plus whites' cells as the case prices them). The keys are in LINEAGE_ROW_KEYS [ASSUMPTION]: crime
rows on the justice key of each end's footing (raw coding at the low end, the custody key at the high end),
unreimbursed care on the uninsured-use key, congestion and crashes on the road key, PM2.5, consumer scale and trade on
the consumption key, schools on the K-12 operating key, volunteering on the adults key, housing and the scale net on
the head count, and restaurant variety, which the population lane found carries no head count, at 0. Gate: the
restated rows add to the restated social rows (2e-6). Every per-member figure of the case divides by the lineage
population (meta.lineage). The record-basis rows of section 7 (the lanes' published social rows) carry the union's
social rows only; the pairing on the priced count is the case's figure.

October 7 (oct07, main_case_2026_10_07, v6; derived/oct07/). v5 plus the items of meta.items: the pension accrual on
the 2026 Trustees paths, retiree health on accrual, the added people at their measured age mix and, where the case
carries it, user fees and the education keys. The script reads it as October 5's: the fiscal rows are the case's (the
band file prices every item), the social rows the population lane's restated ones, and the added people's social rows
take their key shares from band_variants.json, which reads them on the item base (the September 29 payload with the
lineage item's edits): the age mix moves the shares, the edit sets do not [ASSUMPTION, gated there on every share an edit
set only scales]. Per member divides by the lineage population of the case's summary.json v6.per_member_usd.

Inputs: DIR/band_variants.csv (node band_variants.cjs --case CASE: engine bands on the September 23 case,
September 24 and the case) and the channel lanes' derived files (PATHS). Reads only; writes
DIR/real_costs_totals.csv and .json. Run from the repository root, after band_variants.cjs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py [--case sept24|sept26|sept26_schools|sept27|sept29|oct05|oct07] [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import sys
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from types import SimpleNamespace

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "scripts"))
from memory_budget import require_within_budget
sys.path.insert(0, str(FISCAL / "social_respending_2026_10_14"))
from respending import spending_basis_gate, verify_bundle
from valuation_registry import mortality_registry
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
    headcount=FISCAL / "main_case_decomposition_2026_09_29/derived/headcount.csv",
)
# Each case's main-case lane and default output directory (None: --out-dir only), as in band_variants.cjs.
LANES = dict(sept24="main_case_2026_09_24", sept26="main_case_2026_09_26",
             sept26_schools="main_case_schools_full_2026_09_26", sept27="main_case_long_run_2026_09_27",
             sept29="main_case_2026_09_29", oct05="main_case_2026_10_05", oct07="main_case_2026_10_07",
             oct14="main_case_2026_10_14", oct15="main_case_2026_10_15")
OUT_DIRS = dict(sept24=HERE / "derived", sept26=None, sept26_schools=FISCAL / "sept26_propagation_2026_09_26" / "derived",
                sept27=FISCAL / "sept27_propagation_2026_09_27" / "derived", sept29=HERE / "derived" / "sept29",
                oct05=HERE / "derived" / "oct05", oct07=HERE / "derived" / "oct07", oct14=HERE / "derived" / "oct14",
                oct15=HERE / "derived" / "oct15")
# Cases whose roads respond: congestion beside the account is the response lane's, by band end.
LONG_RUN = dict(sept27=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json",
                sept29=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json",
                oct05=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json",
                oct07=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json",
                oct14=FISCAL / "service_response_long_run_2026_09_27/derived/net_change.json")
# Cases whose social rows carry added social items for the union: (lane items.csv, item ids, decision, kind) per
# source. A source with a `measure` column adds its absolute rows and reports its normalized rows beside. Benefits
# are negative costs; the scale lane's summary is read through scale_rows().
SOCIAL_ITEMS = dict(sept27=(
    (FISCAL / "social_costs_unpriced_2026_09_28/derived/items.csv",
     ("fear_avoidance", "private_security", "school_disruption"), "decisions/2026-09-28-social-items-fear-security-schools.md",
     "cost"),
    (FISCAL / "air_pollution_2026_09_28/derived/items.csv", ("pm25_consumption",),
     "decisions/2026-09-28-social-items-pollution-crashes.md", "cost"),
    (FISCAL / "road_crash_externality_2026_09_28/derived/items.csv", ("road_crash_externality",),
     "decisions/2026-09-29-crash-item-with-against-without.md", "cost"),
    (PATHS["scale"], ("scale_net_earnings",), "decisions/2026-09-28-social-items-scale-benefits.md", "benefit"),
    (FISCAL / "disease_food_2026_09_28/derived/items.csv", ("restaurant_variety_market_size",),
     "decisions/2026-09-28-social-items-scale-benefits.md", "benefit"),
    (FISCAL / "benefits_inventory_2026_09_28/derived/items.csv", ("formal_volunteering_outside_group",),
     "decisions/2026-09-28-social-items-more-benefits.md", "benefit"),
    (FISCAL / "consumer_scale_2026_09_28/derived/items.csv", ("total_consumer_scale",),
     "decisions/2026-09-28-social-items-more-benefits.md", "benefit"),
    (FISCAL / "trade_networks_2026_09_28/derived/items.csv", ("total_trade_travel_fdi",),
     "decisions/2026-09-28-social-items-more-benefits.md", "benefit"),
))
SOCIAL_ITEMS["sept29"] = SOCIAL_ITEMS["sept27"]
SOCIAL_ITEMS["oct05"] = SOCIAL_ITEMS["sept27"]
SOCIAL_ITEMS["oct07"] = SOCIAL_ITEMS["sept27"]
SOCIAL_ITEMS["oct14"] = SOCIAL_ITEMS["sept27"]
SOCIAL_ITEMS["oct15"] = SOCIAL_ITEMS["sept27"]
LONG_RUN["oct15"] = LONG_RUN["oct14"]
# Cases whose published pairing is restated on the priced count (population_basis_2026_09_29).
RESTATED = dict(sept27=FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv",
                sept29=FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv",
                oct05=FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv",
                oct07=FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv",
                oct14=FISCAL / "population_basis_2026_09_29/derived/restated_pairing.csv")
# A case whose social rows the population lane restated on another case's pairing: that case. The restated social
# rows (pairing less its fiscal row) then carry over, and the case adds its own fiscal rows.
RESTATED["oct15"] = RESTATED["oct14"]
RESTATED_BASE = dict(sept29="sept27", oct05="sept27", oct07="sept27", oct14="sept27", oct15="sept27")
# Cases that carry the lineage (October 5 on). Each restated social row prices the added people at their share of one
# engine key (band_variants.json lineage_social_keys), at the low end and at the high end; None: not priced (0).
# [ASSUMPTION] the row scales with the key at the margin, and the added people's amount on the key is the case's.
LINEAGE_CASES = ("oct05", "oct07", "oct14", "oct15")
# The summary.json block whose per_member_usd.population is the lineage case's per-member divisor.
PER_MEMBER_BLOCK = dict(oct05="v5", oct07="v6", oct14="v7", oct15="v8")
CRIME = ("justice_use_raw_coding", "justice_use")   # the low end's footing (raw coding), the high end's (custody)
LINEAGE_ROW_KEYS = dict(
    victims=CRIME, property_crime=CRIME, fear_avoidance=CRIME, private_security=CRIME,
    unreimbursed_care=("uninsured_use", "uninsured_use"),
    congestion=("road", "road"), road_crash_externality=("road", "road"),
    housing_gain=("head_count", "head_count"), scale_net_earnings=("head_count", "head_count"),
    school_disruption=("pupils", "pupils"),
    pm25_consumption=("consumption", "consumption"), total_consumer_scale=("consumption", "consumption"),
    total_trade_travel_fdi=("consumption", "consumption"),
    formal_volunteering_outside_group=("adults", "adults"),
    restaurant_variety_market_size=(None, None),   # the population lane: no head count in the item (factor 1)
)
UNION = ("mexican_origin", "union")  # the lanes' labels for the same 40.9m group
# Consumer declarations are explicit even where a producer predates typed rows. They
# describe the adopted reading, not a default inferred from a missing column.
SOCIAL_CONTRACTS = {
    "victims": ("crime_victim_cost_2026_09_23", "victim_harm_active_vsl", ("fear_avoidance",)),
    "property_crime": ("crime_victim_cost_2026_09_23", "victim_resource_loss", ("private_security",)),
    "unreimbursed_care": ("uncompensated_care_2026_09_23", "unreimbursed_resource_cost", ("fiscal_health",)),
    "congestion": ("service_response_long_run_2026_09_27", "value_of_time", ("road_crash_externality",)),
    "housing_gain": ("housing_transfer_2026_09_23", "net_resident_welfare", ("capitalized_crime", "school_disruption")),
    "fear_avoidance": ("social_costs_unpriced_2026_09_28", "wtp_residual", ("victims", "private_security")),
    "private_security": ("social_costs_unpriced_2026_09_28", "resource_spending", ("fear_avoidance",)),
    "school_disruption": ("social_costs_unpriced_2026_09_28", "earnings_pv", ("school_violence",)),
    "pm25_consumption": ("air_pollution_2026_09_28", "dot_vsl_plus_morbidity", ("mortality",)),
    "road_crash_externality": ("road_crash_externality_2026_09_28", "crash_resource_and_harm", ("mortality", "road_congestion")),
    "scale_net_earnings": ("scale_spillovers_2026_09_23", "earnings_including_receipts", ("production",)),
    "restaurant_variety_market_size": ("disease_food_2026_09_28", "consumer_surplus", ("consumer_scale",)),
    "formal_volunteering_outside_group": ("benefits_inventory_2026_09_28", "replacement_wage", ("informal_care",)),
    "total_consumer_scale": ("consumer_scale_2026_09_28", "consumer_surplus", ("restaurant_variety", "trade")),
    "total_trade_travel_fdi": ("trade_networks_2026_09_28", "mixed_resource_and_surplus", ("consumer_scale",)),
}


def social_contract(path, row, historical=False):
    """Fail closed on an undeclared source, comparator, recipient or valuation.

    historical=True is solely for reproducing the frozen pre-P7 control; its rows
    cannot be used as the adopted P7 crime rows.
    """
    item = row["item"]
    if item not in SOCIAL_CONTRACTS:
        raise ValueError(f"[BLOCKED] no consumer declaration for {item}")
    source, valuation, overlaps = SOCIAL_CONTRACTS[item]
    owner = path.parent.parent.name
    if path.name == "baseline_social_items.csv":
        owner = "social_costs_unpriced_2026_09_28"
    if owner != source:
        raise ValueError(f"[BLOCKED] {item}: undeclared source {path}")
    contract = dict(comparator="with_without", beneficiary_population="residents_outside_union",
                    valuation_basis=valuation, overlap_set=list(overlaps))
    if historical and item == "private_security":
        contract["comparator"] = "equal_population"
    measure = row.get("measure")
    if measure is not None and measure not in ("absolute", "normalized"):
        raise ValueError(f"[BLOCKED] {item}: unknown measure {measure}")
    if item == "private_security" and measure == "normalized" and not historical:
        raise ValueError("[BLOCKED] equal-population security cannot enter a with/without total")
    for key, expected in contract.items():
        supplied = row.get(key)
        if supplied is not None:
            if key == "overlap_set" and isinstance(supplied, str):
                supplied = json.loads(supplied)
            if supplied != expected:
                raise ValueError(f"[BLOCKED] {item}: incompatible {key}: {supplied!r} != {expected!r}")
    # A legacy security producer explicitly describes an equal-population price.
    if item == "private_security" and not historical and "offending share - population share" in str(row.get("method_note", "")):
        raise ValueError("[BLOCKED] equal-population security cannot enter a with/without total")
    return contract
# Runs of band_variants.cjs beside a case, never in its band (the case's column; the row label, its note).
BESIDE = dict(capital_at_7pct=("capital_at_7pct", "the return on public capital at the reported 7% on every component; "
                               "beside the central total, never in it"),
              enterprises_out_option_a=("enterprises_out_option_a", "option A: no enterprise capital, the enterprise "
                                        "surplus receipt at 0; beside the central total, never in it"))
# The runs beside each case (BESIDE's entries, plus the cash set from September 29).
BESIDE_RUNS = dict(sept27=BESIDE, sept29=dict(BESIDE, cash_set=(
    "cash_set", "the cash set: the pension switch off, social security and Medicare's Part A at the group's current "
    "benefits (main_case_2026_09_29 band row cash_set); beside the central total, never in it")))
BESIDE_RUNS["oct05"] = dict(BESIDE, cash_set=(
    "cash_set", "the cash set: the pension switch off, social security and Medicare's Part A at the group's current "
    "benefits (main_case_2026_10_05 band row cash_set); beside the central total, never in it"))
BESIDE_RUNS["oct07"] = dict(BESIDE, cash_set=(
    "cash_set", "the cash set: the pension switch off, social security and Medicare's Part A at the group's current "
    "benefits (main_case_2026_10_07 band row cash_set); beside the central total, never in it"))
# Beside runs whose pairing is also restated on the priced count.
BESIDE_RUNS["oct14"] = dict(BESIDE, cash_set=(
    "cash_set", "the cash set: benefits when paid (main_case_2026_10_14 band row cash_set); beside the central total"))
RESTATED_BESIDE = dict(sept29=("cash_set",), oct05=("cash_set",), oct07=("cash_set",), oct14=("cash_set",))
BESIDE_RUNS["oct15"] = dict(BESIDE, cash_set=(
    "cash_set", "benefits when paid (main_case_2026_10_15 cash_set); beside the central total"))
RESTATED_BESIDE["oct15"] = ("cash_set",)
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


def scale_rows(path):
    """The scale lane's summary as items.csv rows, gains as negative costs. The joint row (CZ 1990, as channels()
    reads it) is the absolute item. Against as many average residents the size part cancels and the schooling-mix
    part remains, so the composition row is its normalized figure."""
    s = pd.read_csv(path)
    rows = []
    for measure, table in (("absolute", "joint_grid"), ("normalized", "composition_grid")):
        r = one(s, (s.table == table) & (s.geography == "CZ 1990"), f"scale {table}, CZ 1990")
        rows.append(dict(item="scale_net_earnings", group="mexican_origin", measure=measure, low_bn=-float(r.gain_high_bn),
                         central_bn=-float(r.gain_bn), high_bn=-float(r.gain_low_bn)))
    return pd.DataFrame(rows)


def social_items(sources, historical=False):
    """The union's added social items from their lanes' items.csv: (central, stacked low, stacked high) summed over
    all items and over the cost items, $bn, and one record per item with its normalized figure where the lane
    reports one (beside, never added)."""
    detail = []
    for path, ids, decision, kind in sources:
        frame = scale_rows(path) if path == PATHS["scale"] else pd.read_csv(path)
        union = frame[frame.group.isin(UNION) & frame["item"].isin(ids)]
        declarations = {i: social_contract(path, r.to_dict(), historical=historical) for i, r in union.iterrows()}
        # Missing producer `measure` is resolved only by the authoritative registry.
        measure = union["measure"] if "measure" in union.columns else pd.Series(
            {i: "absolute" for i in declarations}, index=union.index)
        absolute, normalized = union[measure == "absolute"], union[measure == "normalized"]
        gate(f"social items: one absolute row per added item for the union ({rel(path)})",
             sorted(absolute["item"]) == sorted(ids), f"{len(absolute)} rows")
        for index, row in absolute.iterrows():
            r = SimpleNamespace(**row.to_dict())
            n = normalized[normalized["item"] == r.item]
            # Lanes label their arms low/high by evidence, not always by cost (trade: low = the small gain); the
            # stacked span needs the least and most costly values, so order them and require the central inside.
            lo, hi = sorted((float(r.low_bn), float(r.high_bn)))
            gate(f"social items: {r.item} central inside its range", lo <= float(r.central_bn) <= hi)
            nlo, nhi = (None, None) if n.empty else sorted((float(n.low_bn.iloc[0]), float(n.high_bn.iloc[0])))
            detail.append(dict(item=r.item, kind=kind, source=rel(path), decision=decision, central_bn=float(r.central_bn),
                               low_bn=lo, high_bn=hi, contract=declarations[index],
                               normalized_bn=None if n.empty else dict(
                                   central=float(n.central_bn.iloc[0]), low=nlo, high=nhi)))
    gate("social items: no item added twice", len({d["item"] for d in detail}) == len(detail))
    gate("social items: every benefit is a gain at its central", all(d["central_bn"] < 0 for d in detail if d["kind"] == "benefit"))
    sums = lambda ds: tuple(sum(d[k] for d in ds) for k in ("central_bn", "low_bn", "high_bn"))  # noqa: E731
    return sums(detail), sums([d for d in detail if d["kind"] == "cost"]), detail


def lineage_recipient_shares(lineage, frame_path):
    """Added people among each row's former outsiders, not among its senders.

    [ASSUMPTION] exchangeable exposure within the stated recipient age range;
    fractional five-year bins are uniform within bin. This does not identify U→D.
    """
    counts = {r["count"]: float(r["row4"]) for r in csv.DictReader(frame_path.open())}
    mixes = lineage["age_mix"]["mixes"]
    parts = ((lineage["counts"]["at_g3_rate"], mixes["g3_rate"]),
             (lineage["counts"]["later_losses"], mixes["later"]))
    weights = {
        "all": [1.0] * 17,
        "12_plus": [0.0, 0.0, 3 / 5] + [1.0] * 14,
        "18_plus": [0.0] * 3 + [2 / 5] + [1.0] * 13,
        "5_17": [0.0, 1.0, 1.0, 3 / 5] + [0.0] * 13,
    }
    shares = {}
    for age, w in weights.items():
        added = sum(n * sum(p * a for p, a in zip(mix, w)) for n, mix in parts)
        outsiders = counts[f"cps_all_civilian|{age}"] - counts[f"union|{age}"]
        share = added / outsiders
        if not 0 <= share < 1:
            raise ValueError(f"[BLOCKED] lineage recipients {age}: {share}")
        shares[age] = share
    return {item: shares["5_17" if item == "school_disruption" else
                         "18_plus" if item == "formal_volunteering_outside_group" else "all"]
            for item in LINEAGE_ROW_KEYS}


def lineage_social_rows(path, keys, restated_social, recipient_shares=None):
    """The added people's social rows (October 5 on): each row of the population lane's restatement on audit row 4's
    union (section row; crash and congestion from row_5plus, the pairing's 5+ basis) times the added people's share of
    its key (LINEAGE_ROW_KEYS) at each band end. Gates: every row has a key, and the rows add to the restated social
    rows (2e-6: six printed decimals per row). Returns (detail, (low, high))."""
    union = {}
    for r in csv.DictReader(path.open()):
        if r["section"] == "row" and r["item"] != "fiscal":
            union.setdefault(r["item"], {})[r["end"]] = float(r["restated"])
    for r in csv.DictReader(path.open()):
        if r["section"] == "row_5plus":
            gate(f"lineage social rows: the 5+ row {r['item']} replaces a restated row at its end", r["end"] in union.get(r["item"], {}))
            union[r["item"]][r["end"]] = float(r["restated"])
    gate("lineage social rows: every restated social row has a key, and every key a row",
         sorted(union) == sorted(LINEAGE_ROW_KEYS), f"{len(union)} rows")
    detail, totals = [], [0.0, 0.0]
    for item, by_end in union.items():
        rec = dict(item=item, keys=dict(zip(("low", "high"), LINEAGE_ROW_KEYS[item])))
        for i, end in enumerate(("low", "high")):
            v = by_end.get(end, by_end.get("both"))
            key = LINEAGE_ROW_KEYS[item][i]
            share = 0.0 if key is None else (keys["head_count"] if key == "head_count" else keys[f"{end}_end"][key])
            gross = 0.0 if key is None else v * share
            receiver_share = (recipient_shares or {}).get(item, 0.0)
            # U→D and D→D both leave the outsider side. Signed benefits obey
            # the identical boundary rule; they are not subtracted as harms.
            boundary = -(v + gross) * receiver_share
            amount = gross + boundary
            rec[f"recipient_share_{end}"], rec[f"gross_added_{end}_bn"] = receiver_share, gross
            rec[f"union_to_added_{end}_bn"], rec[f"added_to_added_{end}_bn"] = v * receiver_share, gross * receiver_share
            rec[f"boundary_change_{end}_bn"] = boundary
            rec[f"union_{end}_bn"], rec[f"share_{end}"], rec[f"added_{end}_bn"] = v, share, amount
            totals[i] += amount
        detail.append(rec)
    for i, end in enumerate(("low", "high")):
        s = sum(d[f"union_{end}_bn"] for d in detail)
        gate(f"lineage social rows: the restated rows add to the restated social rows ({end}, 2e-6)",
             abs(s - restated_social[i]) < 2e-6, f"{s:.6f} / {restated_social[i]:.6f}")
    return detail, tuple(totals)


def priced_count(path):
    """(audit row 4's union, the published CPS union): the adopted cases price the first."""
    row = next(r for r in csv.DictReader(path.open()) if r["cut"] == "all" and r["group"] == "union")
    return float(row["row4"]), float(row["published"])


def half_up(x, places):
    # Rounding to 9 places first removes float noise from sums of one-decimal rows (57.8 - 0.65).
    return float(Decimal(repr(round(float(x), 9))).quantize(Decimal(1).scaleb(-places), ROUND_HALF_UP))


def apply_p7_crime(rows, doc, case="oct14"):
    """Adopt only the owned crime payload, retaining all noncrime producer rows.

    The original record-basis tables remain historical controls. The priced
    pairing and full span are the current readings; their provenance is explicit.
    """
    lane = FISCAL / "social_costs_unpriced_2026_09_28"
    payload_path, items_path = lane / "derived/p7_payload.json", lane / "derived/p7_items.csv"
    p = json.loads(payload_path.read_text())
    for name, digest in p["sources_sha256"].items():
        source = FISCAL.parent.parent / name
        if not source.exists() or hashlib.sha256(source.read_bytes()).hexdigest() != digest:
            raise ValueError(f"[BLOCKED] missing or stale P7 crime source: {name}")
    if p.get("case") != "oct14" or p.get("vsl_standard") != "dot_uniform":
        raise ValueError("[BLOCKED] incompatible P7 case or valuation")
    items = list(csv.DictReader(items_path.open()))
    expected = {(item, end) for item in ("fear_avoidance", "private_security") for end in ("low", "high")}
    if {(r["item"], r["end"]) for r in items} != expected or len(items) != 4:
        raise ValueError("[BLOCKED] P7 crime item coverage")
    for r in items:
        social_contract(items_path, r)
        if r["measure"] != "absolute" or r["vsl_standard"] != p["vsl_standard"]:
            raise ValueError("[BLOCKED] incompatible P7 row measure or mortality setting")
        if not float(r["low_bn"]) <= float(r["central_bn"]) <= float(r["high_bn"]):
            raise ValueError("[BLOCKED] P7 crime central outside its range")
        if abs(float(r["central_bn"]) - p["union_crime_rows"][r["end"]][r["item"]]) > 1e-9:
            raise ValueError("[BLOCKED] P7 item/payload mismatch")
    delta = [p["pairing_bn"][i] - p["baseline_pairing_bn"][i] for i in (0, 1)]
    pairing = [next(r for r in rows if r["column"] == "pairing_on_priced_count" and r["item"] == f"published pairing ({e})") for e in ("low", "high")]
    original_pairing = [r[case] for r in pairing]
    if case == "oct15":
        doc["without_round1_social_fixes_bn"] = dict(zip(("low", "high"), original_pairing))
    for i, r in enumerate(pairing):
        if case == "oct14" and abs(r[case] - p["baseline_pairing_bn"][i]) > 2e-6:
            raise ValueError("[BLOCKED] P7 frozen baseline no longer matches the reconstructed pairing")
    lineage = doc["lineage_social_rows"]
    original_social = [lineage["union_social_bn"][end] + lineage["added_social_bn"][end]
                       for end in ("low", "high")]
    if {d["item"] for d in lineage["rows"]} != set(SOCIAL_CONTRACTS):
        raise ValueError("[BLOCKED] every adopted social row needs exactly one consumer declaration")
    union_sums, added_sums = [0.0, 0.0], [0.0, 0.0]
    for d in lineage["rows"]:
        recipient = p["recipient_shares"][d["item"]]
        for i, end in enumerate(("low", "high")):
            value = p["union_crime_rows"][end].get(d["item"], d[f"union_{end}_bn"])
            share = d[f"share_{end}"]
            d[f"union_before_boundary_{end}_bn"] = value
            d[f"union_to_added_{end}_bn"] = value * recipient
            d[f"added_to_added_{end}_bn"] = value * share * recipient
            d[f"recipient_share_{end}"] = recipient
            d[f"union_{end}_bn"] = value * (1-recipient)
            d[f"added_{end}_bn"] = value * share * (1-recipient)
            if d["item"] in p["lineage_crime_rows"][end]:
                # Security's forward offending and reverse consumption keys are
                # distinct, so evaluate the full lineage before differencing.
                d[f"union_{end}_bn"] = p["union_crime_rows_outside_lineage"][end][d["item"]]
                d[f"added_{end}_bn"] = p["lineage_crime_rows"][end][d["item"]] - d[f"union_{end}_bn"]
                before = p["lineage_crime_rows_before_boundary"][end][d["item"]]
                d[f"gross_added_{end}_bn"] = before-value
                d[f"union_to_added_{end}_bn"] = value-d[f"union_{end}_bn"]
                d[f"added_to_added_{end}_bn"] = before-p["lineage_crime_rows"][end][d["item"]]-d[f"union_to_added_{end}_bn"]
            union_sums[i] += d[f"union_{end}_bn"]
            added_sums[i] += d[f"added_{end}_bn"]
    lineage["union_social_bn"] = dict(zip(("low", "high"), union_sums))
    lineage["added_social_bn"] = dict(zip(("low", "high"), added_sums))
    if case == "oct15":
        delta = [union_sums[i] + added_sums[i] - original_social[i] for i in (0, 1)]
    lineage["rule"] = "active crime rows; every signed row has U→D and D→D removed [ASSUMPTION: exchangeable recipients within age scope]"
    for r in rows:
        if r.get(case) is None:
            continue
        value = None
        for i, end in enumerate(("low", "high")):
            if r["column"].startswith("pairing_on_priced_count") and r["item"] in (
                    f"published pairing ({end})", f"published pairing per group member ({end})"):
                if r["column"] == "pairing_on_priced_count":
                    value = p["pairing_bn"][i] if case == "oct14" else r[case] + delta[i]
                    if "per group" in r["item"]:
                        value = (p["pairing_bn"][i] if case == "oct14" else original_pairing[i] + delta[i]) / doc["per_member_population_m"][case]
                else:
                    value = r[case] + delta[i] / (doc["per_member_population_m"][case] if "per group" in r["item"] else 1)
            if r["column"] == "full_span" and r["item"] in (f"{end} end", f"per group member, {end}"):
                baseline_path = lane / "inputs/baseline_totals_oct14.csv"
                baseline_rows = list(csv.DictReader(baseline_path.open()))
                old_full = next(float(x["oct14"]) for x in baseline_rows if x["column"] == "full_span" and x["item"] == f"{end} end")
                value = p["full_span_bn"][i] if case == "oct14" else r[case] + p["full_span_bn"][i] - old_full
                if "per group" in r["item"]:
                    own_full = next(x[case] for x in rows if x["column"] == "full_span" and x["item"] == f"{end} end")
                    value = (p["full_span_bn"][i] if case == "oct14" else own_full) / doc["per_member_population_m"][case]
            if r["column"] == "pairing_on_priced_count":
                if r["item"] == f"social rows on the priced count ({end})":
                    value = union_sums[i]
                elif r["item"] == f"the added people's social rows ({end})":
                    value = added_sums[i]
            if r["column"].startswith("lineage_social_") and r["item"] == f"added people ({end})":
                item = r["column"].removeprefix("lineage_social_")
                value = next(d[f"added_{end}_bn"] for d in lineage["rows"] if d["item"] == item)
        if value is not None:
            r[case] = value
            r["change"] = None if r["sept24"] is None else value - r["sept24"]
            r["note"] += "; P7 owned crime rows; U→D and D→D removed under exchangeable-recipient assumption; dot_uniform"
        if r["column"] in ("social_item_fear_avoidance", "social_item_private_security", "social_items_2026_09_28"):
            r["column"] = "historical_control_" + r["column"]
            r["note"] += "; pre-P7 control, never adopted; current crime rows are endpoint-specific"
    template = dict(rows[0])
    for item in items:
        for statistic in ("low", "central", "high"):
            record = {key: None for key in template}
            record.update(section="7", column=f"social_item_{item['item']}", item=f"{statistic}, {item['end']} footing, row4 union",
                          unit="bn", sept23=None, sept24=None, change=None,
                          note="P7 with/without; current personal payment key; dot_uniform; outsiders of union before separate lineage boundary")
            record[case] = float(item[f"{statistic}_bn"])
            rows.append(record)
    doc["p7_crime"] = p
    doc["p7_crime"]["adopted_items"] = items
    doc["p7_crime"]["consumer_contracts"] = {
        item: social_contract(FISCAL / source / "derived/items.csv", dict(item=item))
        for item, (source, _, _) in SOCIAL_CONTRACTS.items()}
    doc["p7_crime"]["beneficiary_after_boundary"] = "residents_outside_lineage"
    doc["social_items_in_the_social_rows"]["status"] = "historical record-basis control; current priced pairing uses p7_crime"
    doc["sources_sha256"].update({rel(payload_path): hashlib.sha256(payload_path.read_bytes()).hexdigest(),
                                  rel(items_path): hashlib.sha256(items_path.read_bytes()).hexdigest()})


def parse_args():
    ap = argparse.ArgumentParser(description="Real-costs totals (memo §7, §7b) on an adopted main case.")
    ap.add_argument("--case", choices=tuple(LANES), default="oct15",
                    help="oct15: main case v8 (default); oct14: historical v7; oct07: main case v6 (main_case_2026_10_07); "
                         "oct05: the main case adopted 2026-10-05; "
                         "sept29: the main case adopted 2026-09-29; "
                         "sept26_schools: schools at full average cost; sept26: the one-year scenario (--out-dir only); "
                         "sept24: the committed September 24 run")
    ap.add_argument("--out-dir", type=Path, default=None,
                    help="the directory band_variants.cjs wrote this case's bands to; the outputs go there too")
    ap.add_argument("--v8-social-transport", choices=("fixed_v7_source_keys",), default="fixed_v7_source_keys",
                    help="explicit transport: retain committed P7 sender/receiver quantities; v8 resource funding; new completion/coverage social effects are unpriced")
    args = ap.parse_args()
    args.out_dir = args.out_dir or OUT_DIRS[args.case]
    if args.out_dir is None:
        ap.error(f"--case {args.case} writes only to --out-dir DIR")
    args.out_dir = args.out_dir.resolve()
    return args


def apply_v8_environment(rows, doc, bands_meta, summary, transport):
    """Replace owned PM/crash/volunteering rows, retaining their declared frame.

    Sender/receiver quantities retain frozen v7 keys. Funding reads v8's complete
    typed resource arithmetic; spendability of unclassified net cash amounts is
    conditional. New people's social quantities are not measured here.
    This explicit switch is the recommended branch pending a producer transport
    rule. Government, carbon and life-year valuations remain beside.
    """
    if transport != "fixed_v7_source_keys":
        raise ValueError("[BLOCKED] undeclared v8 social transport")
    lane = FISCAL / "social_respending_2026_10_14"
    stack_generation = verify_bundle("stack", lane / "derived")
    respending_generation = verify_bundle("respending", lane / "derived")
    stack_path = lane / "derived/conditional_stacks.csv"
    integration_path = lane / "derived/integration.json"
    source_rows = list(csv.DictReader(stack_path.open()))
    integration = json.loads(integration_path.read_text())
    congestion_path = FISCAL / "service_response_long_run_2026_09_27/derived/net_change_oct15.json"
    live_congestion = json.loads(congestion_path.read_text())
    crime_mortality_path = FISCAL / "social_costs_unpriced_2026_09_28/derived/oct15/mortality_pairing_rows.csv"
    crime_mortality_rows = list(csv.DictReader(crime_mortality_path.open()))
    if not all(integration["gates"].values()) or integration["counts"]["conditional_stack_rows"] != len(source_rows):
        raise ValueError("[BLOCKED] social environment producer gates/row count")
    source_baseline = doc["p7_crime"]["baseline_pairing_bn"]
    detail = doc["lineage_social_rows"]["rows"]
    before = {end: next(r["oct15"] for r in rows if r["column"] == "pairing_on_priced_count"
                        and r["item"] == f"published pairing ({end})") for end in ("low", "high")}
    population = doc["per_member_population_m"]["oct15"]

    def amount(item, end, gross=False):
        d = next(d for d in detail if d["item"] == item)
        if gross:
            return d[f"union_before_boundary_{end}_bn"] * (1 + d[f"share_{end}"])
        return d[f"union_{end}_bn"] + d[f"added_{end}_bn"]

    def selected(end, denominator="PCE", valuation="uniform", rate="0", displacement="1.0", crash_arm="multivehicle_only"):
        chosen = [r for r in source_rows if r["end"] == end and r["spending_denominator"] == denominator
                  and r["mortality_valuation"] == valuation and r["real_discount_rate"] == rate
                   and r["crash_arm"] == crash_arm and r["volunteering_proxy"] == "primary_food"
                  and r["displacement"] == displacement and r["market_demand_arm"] == "False"
                  and r["pm_crash_recipient_boundary"] == "lineage_exchangeable"]
        if len(chosen) != 1:
            raise ValueError(f"[BLOCKED] social environment named stack missing/ambiguous: {end}/{denominator}/{valuation}/{rate}/{displacement}")
        r = chosen[0]
        index = ("low", "high").index(end)
        if abs(float(r["baseline_bn"]) - source_baseline[index]) > 1e-9:
            raise ValueError("[BLOCKED] environment/crime frozen baselines disagree")
        source_terms = ("mortality_delta_bn", "respending_bn", "government_mirror_bn", "crash_delta_bn",
                        "volunteering_delta_bn", "market_demand_delta_bn", "city_tax_increment_bn", "crime_mortality_delta_bn")
        if not all(math.isfinite(float(r[k])) for k in (*source_terms, "baseline_bn", "stack_delta_bn", "stack_pairing_bn", "budget_saving_at_pairing_bn")):
            raise ValueError("[BLOCKED] nonfinite social source amount")
        if abs(sum(float(r[k]) for k in source_terms) - float(r["stack_delta_bn"])) > 1e-9 or abs(
                float(r["stack_pairing_bn"]) - float(r["baseline_bn"]) - float(r["stack_delta_bn"])) > 1e-9:
            raise ValueError("[BLOCKED] social environment source stack does not close")
        # Replace levels from the exact producer boundary. Its historical
        # delta baseline uses different sender keys from the legacy consumer;
        # transplanting those deltas would preserve that baseline discrepancy.
        terms = dict(
            pm_mortality=float(r["pm_gross_replacement_bn"]) - amount("pm25_consumption", end),
            pm_respending=float(r["respending_bn"]),
            crash_capacity=float(r["crash_replacement_bn"]) - amount("road_crash_externality", end),
            incoming_volunteering=float(r["volunteering_delta_bn"]),
            # The producer's baseline still has pre-round-1 victims, while
            # this consumer has already applied P7. Use its separate delta
            # against current P7, so uniform mortality is not counted twice.
            crime_mortality=float(r["crime_delta_from_current_P7_bn"]),
        )
        registry = json.loads(r["mortality_registry_json"])
        basis = "dot_uniform" if valuation == "uniform" else "dot_life_years"
        mortality_registry(basis,rate,registry["channels"])
        crime = [x for x in crime_mortality_rows if x["end"]==end and x["valuation"]==basis
                 and float(x["real_discount_rate"])==float(rate)]
        if len(crime)!=1 or abs(float(crime[0]["baseline_lineage_victim_bn"])-amount("victims",end))>1e-9:
            raise ValueError("[BLOCKED] crime mortality baseline does not match selected pairing")
        if abs(float(crime[0]["lineage_victim_delta_bn"])-terms["crime_mortality"])>1e-9:
            raise ValueError("[BLOCKED] crime mortality delta differs across source/stack")
        con = live_congestion["pairing_by_end"][end]
        if abs(con["baseline_lineage_congestion_bn"]-amount("congestion",end)) > 1e-9:
            raise ValueError("[BLOCKED] live congestion baseline does not match selected pairing")
        terms["congestion_capacity"] = con["lineage_congestion_delta_bn"]
        if abs(con["replacement_lineage_congestion_bn"]-con["baseline_lineage_congestion_bn"]-terms["congestion_capacity"]) > 1e-9:
            raise ValueError("[BLOCKED] congestion replacement does not close")
        funding = bands_meta["social_resource_account"]["ends"][end]
        if not all(math.isfinite(funding[k]) for k in ("current_H_bn", "capital_return_bn", "net_accrual_timing_bridge_bn",
                                                      "private_wtp_bn", "cash_cost_bn", "set_cost_bn")):
            raise ValueError("[BLOCKED] nonfinite v8 social resource account")
        if funding["accounting_basis"] != "national_accounts" or r["funding_accounting_basis"] != funding["accounting_basis"]:
            raise ValueError("[BLOCKED] social funding accounting basis mismatch")
        spending_basis_gate(funding["accounting_basis"], r["denominator_accounting_basis"],
                            units_sensitivity=denominator == "CE")
        old_H = float(r["budget_saving_at_pairing_bn"])
        if old_H <= 0:
            raise ValueError("[BLOCKED] source re-spending denominator H must be positive")
        unit = -float(r["respending_bn"]) / old_H
        terms["pm_respending"] = -funding["current_H_bn"] * unit
        return r, terms, unit, funding

    contract = dict(comparator="with_without", beneficiary_population="residents_outside_v7_lineage",
                     valuation_basis="dot_uniform_plus_morbidity; multivehicle_only_crashes; volunteer_replacement_wage",
                     overlap_set=["pm25_consumption", "road_crash_externality", "formal_volunteering_outside_group", "victims", "congestion"],
                    population_transport=transport,
                     assumptions="frozen v7 sender/receiver keys; v8 current cash resource funding; primary-food incoming hours proxy; full incoming displacement for named central stack")
    variants = {}
    for name, denominator, valuation, rate, displacement, government, crash_arm, timing in (
            ("central", "PCE", "uniform", "0", "1.0", False, "multivehicle_only", "current_cash"),
            ("without_incoming_displacement", "PCE", "uniform", "0", "0.0", False, "multivehicle_only", "current_cash"),
            ("government_mirror", "PCE", "uniform", "0", "1.0", True, "multivehicle_only", "current_cash"),
            ("CE_units_sensitivity", "CE", "uniform", "0", "1.0", False, "multivehicle_only", "current_cash"),
            ("all_density", "PCE", "uniform", "0", "1.0", False, "all_density", "current_cash"),
            ("resource_promises_deferred", "PCE", "uniform", "0", "1.0", False, "multivehicle_only", "resource_deferred"),
            ("resource_wealth_equivalent", "PCE", "uniform", "0", "1.0", False, "multivehicle_only", "resource_wealth"),
            ("life_years_r0", "PCE", "VSLY", "0", "1.0", False, "multivehicle_only", "current_cash"),
            ("life_years_r003", "PCE", "VSLY", "0.03", "1.0", False, "multivehicle_only", "current_cash")):
        values, parts = {}, {}
        for end in ("low", "high"):
            source, terms, unit, funding = selected(end, denominator, valuation, rate, displacement, crash_arm)
            city_income_lost = -amount("scale_net_earnings", end)
            market_income_lost = city_income_lost + funding["private_wtp_bn"]
            spending_base = funding["current_H_bn"]
            if timing != "current_cash":
                spending_base += funding["capital_return_bn"] - market_income_lost
                if timing == "resource_wealth":
                    spending_base += funding["net_accrual_timing_bridge_bn"]
                full_cost = funding["set_cost_bn"] if timing == "resource_wealth" else funding["cash_cost_bn"]
                if abs(spending_base - (full_cost-city_income_lost)) > 1e-9:
                    raise ValueError("[BLOCKED] resource spending must close to complete cost minus city market income")
                terms["pm_respending"] = -spending_base * unit
            if government:
                terms["government_mirror"] = float(source["government_mirror_bn"])
            delta = sum(terms.values())
            values[end] = before[end] + delta
            parts[end] = dict(terms=terms, delta_bn=delta, source_budget_saving_bn=float(source["budget_saving_at_pairing_bn"]),
                               current_H_bn=funding["current_H_bn"],spending_base_bn=spending_base,resource_account=funding,
                               market_income_lost_bn=market_income_lost,city_income_lost_bn=city_income_lost,
                               private_production_income_lost_bn=funding["private_wtp_bn"],pm_unit_harm_per_bn_spent=unit,
                              pm_replacement_bn=amount("pm25_consumption", end) + terms["pm_mortality"] + terms["pm_respending"],
                               crash_replacement_bn=amount("road_crash_externality", end) + terms["crash_capacity"],
                               crime_victim_replacement_bn=amount("victims",end)+terms["crime_mortality"],
                               congestion_replacement_bn=amount("congestion",end)+terms["congestion_capacity"],
                              volunteering_replacement_bn=amount("formal_volunteering_outside_group", end) + terms["incoming_volunteering"])
            if abs(values[end] - before[end] - delta) > 1e-9:
                raise ValueError("[BLOCKED] social environment row closure")
        variants[name] = dict(pairing_bn=values, parts=parts,
                              contract=dict(contract, valuation_basis=valuation, denominator=denominator,
                                             incoming_displacement=float(displacement), government_mirror=government,
                                             crash_arm=crash_arm,timing=timing,units_sensitivity=denominator=="CE"))
    # Preserve the exact crime-only pairing beside before replacing central.
    template = dict(rows[0])

    def append(column, item, value, unit="bn", note=""):
        row = {key: None for key in template}
        row.update(section="7", column=column, item=item, unit=unit, oct15=value, note=note)
        rows.append(row)

    for end in ("low", "high"):
        append("pairing_on_priced_count_without_social_env", f"published pairing ({end})", before[end],
               note="P7 crime live; PM/crash/volunteering prior rows retained; explicit fixed v7 social source frame")
        append("pairing_on_priced_count_without_social_env", f"published pairing per group member ({end})", before[end] / population, "$k")
    central = variants["central"]
    current_social_rows = []
    for record in detail:
        item = record["item"]
        values = {end: record[f"union_{end}_bn"] + record[f"added_{end}_bn"] for end in ("low", "high")}
        replacement_field = {"pm25_consumption": "pm_replacement_bn", "road_crash_externality": "crash_replacement_bn",
                             "formal_volunteering_outside_group": "volunteering_replacement_bn",
                             "victims":"crime_victim_replacement_bn", "congestion":"congestion_replacement_bn"}.get(item)
        if replacement_field:
            values = {end: central["parts"][end][replacement_field] for end in ("low", "high")}
        current_social_rows.append(dict(item=item, total_by_end_bn=values,
                                       contract=contract if replacement_field else doc["p7_crime"]["consumer_contracts"][item]))
    current_social = {end: sum(record["total_by_end_bn"][end] for record in current_social_rows) for end in ("low", "high")}
    joint = {}
    for end in ("low", "high"):
        baseline = doc["without_round1_social_fixes_bn"][end]
        crime_delta = before[end] - baseline
        environment_delta = central["parts"][end]["delta_bn"]
        combined = central["pairing_bn"][end]
        interaction = combined - baseline - crime_delta - environment_delta
        prior_social = sum(amount(record["item"], end) for record in detail)
        fiscal = before[end] - prior_social
        if abs(interaction) > 1e-9 or abs(fiscal + current_social[end] - combined) > 1e-9:
            raise ValueError("[BLOCKED] joint crime/environment interaction or row closure")
        joint[end] = dict(without_round1_social_fixes_bn=baseline,crime_delta_bn=crime_delta,
                          environment_delta_bn=environment_delta,with_round1_social_fixes_bn=combined,
                           round2_crime_mortality_delta_bn=central["parts"][end]["terms"]["crime_mortality"],
                           round2_congestion_delta_bn=central["parts"][end]["terms"]["congestion_capacity"],
                          interaction_residual_bn=interaction,fiscal_pairing_bn=fiscal,
                          social_rows_bn=current_social[end])
        append("pairing_without_round1_social_fixes", f"published pairing ({end})", baseline,
               note="v8 fiscal account; preserved pre-round1 social source rows; conditional source-key transport")
    for end in ("low", "high"):
        append("pairing_on_priced_count", f"social rows after environmental replacements ({end})", current_social[end],
               note="signed owned row replacements; government mirror, carbon and life-years excluded; v7 social frame held")
    for row in rows:
        if row.get("oct15") is None or not row["column"].startswith("pairing_on_priced_count"):
            continue
        if row["column"] == "pairing_on_priced_count_without_social_env":
            continue
        for end in ("low", "high"):
            if row["item"] in (f"published pairing ({end})", f"published pairing per group member ({end})"):
                per_member = "per group" in row["item"]
                row["oct15"] += central["parts"][end]["delta_bn"] / (population if per_member else 1)
                row["change"] = None if row["sept24"] is None else row["oct15"] - row["sept24"]
                row["note"] += "; conditional PCE uniform-VSL, multivehicle-only crashes, incoming primary-food volunteering at displacement 1; government/CO2/life-years beside; frozen v7 social keys, v8 current funding"
    for name, variant in variants.items():
        for end in ("low", "high"):
            if name != "central":
                append(f"pairing_social_env_{name}_beside", f"published pairing ({end})", variant["pairing_bn"][end],
                       note="conditional alternative; never add to central; " + json.dumps(variant["contract"], sort_keys=True))
            for item, value in variant["parts"][end]["terms"].items():
                append(f"social_env_{name}_{item}", f"replacement delta ({end})", value,
                       note=json.dumps(variant["contract"], sort_keys=True))
    carbon_path = lane / "derived/co2_beside.csv"
    for source in csv.DictReader(carbon_path.open()):
        if source["population_basis"] == "lineage" and source["spending_denominator"] == "PCE":
            append("co2_source_frame_beside", f"{source['valuation']} ({source['end']})", float(source["other_us_damage_bn"]),
                   note="frozen v7 source quantities; never added; carbon valuation alternative")
    doc["v8_social_environment"] = dict(transport=transport, contract=contract,
        status="conditional named stack; added completion/coverage social effects unpriced, not zero measured effects",
        without_environment_pairing_bn=before, variants=variants,
         changed_rows_from_oct14=["fiscal account and divisor", "PM mortality/exposure and PCE re-spending", "multivehicle-only crashes on the live road key", "live road-key congestion", "incoming volunteering", "all-channel mortality arms; uniform crime central already corrected by P7"],
        held_source_population=42752212.92438524, current_fiscal_population=summary["v8"]["population"]["with_coverage"],
        government_mirror="beside", carbon="beside", life_years="beside", full_span="P7 crime-only range; conditional environment grid is not a confidence interval")
    doc["v8_social_environment"]["current_social_rows"] = current_social_rows
    doc["v8_social_environment"]["current_social_by_end_bn"] = current_social
    doc["joint_social_stack"] = dict(ends=joint,interaction_closure_tolerance_bn=1e-9,
        interaction_closure_gate=True,
        scope="accounting closure of selected row replacements; behavioural crime/pollution interactions unmeasured",
        funding="same exact v8 H for crime-plus-environment pairing; capital and promise timing priced beside")
    doc["lineage_social_rows"]["status"] = "P7 source-frame row decomposition before environment; current total rows in v8_social_environment.current_social_rows"
    for path in (stack_path, integration_path, carbon_path, congestion_path, crime_mortality_path):
        doc["sources_sha256"][rel(path)] = hashlib.sha256(path.read_bytes()).hexdigest()
    if stack_generation != verify_bundle("stack", lane / "derived") or respending_generation != verify_bundle("respending", lane / "derived"):
        raise ValueError("[BLOCKED] social producer generation changed during pairing")


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
        paths.update({f"social_items_{p.parent.parent.name}": p for p, *_ in SOCIAL_ITEMS[case]})
    if case in RESTATED:
        paths["restated"] = RESTATED[case]
    bands = pd.read_csv(paths["bands"]).set_index(["case", "variant"])
    meta = json.loads(paths["bands_meta"].read_text())
    summaries = dict(sept24=json.loads(paths["main24"].read_text()))
    if later:
        summaries[case] = json.loads(paths["main_case"].read_text())
    pop_m = meta["target_population"] / 1e6
    priced, published_union = priced_count(paths["headcount"])
    pop = dict(sept23=pop_m, **{k: priced / 1e6 for k in adopted})  # the population each column prices, millions
    lineage_keys, lineage_doc = None, None
    if case in LINEAGE_CASES:
        # The case prices the lineage: the union (audit row 4) plus the added people (meta.lineage, through the band file).
        counts, lineage_keys = meta["lineage"]["counts"], meta["lineage_social_keys"]
        divisor = (summaries[case]["v8"]["population"]["with_coverage"] if case == "oct15" else
                   summaries[case][PER_MEMBER_BLOCK[case]]["per_member_usd"]["population"])
        source_population = counts["lineage_population"]
        if case == "oct15":
            payload_meta = json.loads(paths["case_corrections"].read_text())["meta"]
            complete = payload_meta["union_completion"]["counts"]["total"]
            coverage = payload_meta["coverage"]["net_missing_people"]
            gate("v8 population adds union completion and coverage exactly (1e-6 people)",
                 abs(source_population + complete + coverage - divisor) < 1e-6)
            gate("the v8 per-member fiscal dollars use that same divisor (1e-9 dollars)",
                 all(abs(b * 1e9 / divisor - v) < 1e-9 for b, v in zip(
                     summaries[case]["main_case"], summaries[case]["v8"]["per_member_usd"]["set"])))
        gate("the lineage population is the union (row 4) plus the added people, and the case's per-member population",
             abs(counts["account_union"] - priced) < 1e-3 and abs(counts["lineage_population"] - priced - counts["added"]) < 1e-3
             and (case == "oct15" or abs(counts["lineage_population"] - divisor) < 1e-3), f"{counts['lineage_population']:,.1f} = {priced:,.1f} + {counts['added']:,.1f}")
        gate("the band file's head-count share is the added people over the union",
             abs(lineage_keys["head_count"] - counts["added"] / priced) < 1e-12, f"{lineage_keys['head_count']:.6f}")
        gate("the lineage case's pairing is restated on another case's social rows (RESTATED_BASE)", case in RESTATED_BASE)
        pop[case] = divisor / 1e6
    band = lambda k, v:(float(bands.loc[(k, v), "cost_low_bn"]), float(bands.loc[(k, v), "cost_high_bn"]))  # noqa: E731
    print("[inputs]")
    c = channels()
    care24 = -meta["care_constant_bn"]
    gate("care constant is the package's -4.15 and the lane's total rounds to it", care24 == 4.15 and round(c["care"], 2) == 4.15,
         f"{care24} / {c['care']:.4f}")
    gate(f"band file is the {case} run", meta.get("case", "sept24") == case, rel(paths["bands_meta"]))
    gate("the headcount's published union is the band file's target population, and row 4 prices fewer people",
         abs(published_union - meta["target_population"]) < 1 and 39e6 < priced < published_union,
         f"{published_union:,.1f} / {meta['target_population']:,.1f}; row 4 {priced:,.1f}")
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
        for run in BESIDE_RUNS[case]:
            gate(f"band file has the {case}_{run} run beside the case", (f"{case}_{run}", "adopted") in bands.index)
    # A case whose summary flags its congestion figure as carried over, not recomputed (September 29: roads by miles).
    stale_congestion = (summaries[case].get("beside_the_account", {}).get("congestion", {}).get("not_recomputed")
                        if later else None)
    if stale_congestion:
        gate("the flagged congestion figure is the one this case uses", cong[case] == (
            summaries[case]["beside_the_account"]["congestion"]["low_end"]["congestion_bn"],
            summaries[case]["beside_the_account"]["congestion"]["high_end"]["congestion_bn"]), stale_congestion)
    # The added social items by case: (central, stacked low, stacked high); zero before September 28.
    # §7 carries every added item; §7b's social rows carry the cost items only (its last column adds the scale net).
    items = {k: (0.0, 0.0, 0.0) for k in cols}
    cost_items = {k: (0.0, 0.0, 0.0) for k in cols}
    item_detail = []
    if case in SOCIAL_ITEMS:
        # Reproduce the original record as a positive control before the live
        # oct14 correction below. Historical security is never adopted here.
        items[case], cost_items[case], item_detail = social_items(SOCIAL_ITEMS[case], historical=True)
        scale = [d for d in item_detail if d["item"] == "scale_net_earnings"]
        gate("the scale item is the scale net §7b adds", all(abs(d["central_bn"] + c["scale_net"]) < 1e-9 for d in scale),
             f"{[d['central_bn'] for d in scale]} / {c['scale_net']:.4f}")

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
    per_member = lambda vals: {k: v / pop[k] for k, v in vals.items()}  # noqa: E731
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
        note = ("the union's added social items, costs and benefits (negative), in every §7 social row above: "
                + ", ".join(d["item"] for d in item_detail) + "; property values stay out; normalized figures and the "
                "crash lane's fault-based row sit beside, never added; decisions 2026-09-28 and 2026-09-29")
        for label, v in zip(("central, both ends", "stacked low, full span", "stacked high, full span"), items[case]):
            add("7", "social_items_2026_09_28", label, {case: v}, note=note)
        for d in item_detail:
            for label, key in (("central, both ends", "central_bn"), ("low, full span", "low_bn"), ("high, full span", "high_bn")):
                add("7", f"social_item_{d['item']}", label, {case: d[key]}, note=f"{d['source']}; {d['decision']}")
            for end, v in (d["normalized_bn"] or {}).items():
                add("7", f"social_item_{d['item']}", f"normalized {end}, beside", {case: v},
                    note="against as many average residents; never added")
    if case in LONG_RUN:
        # The case's runs beside it: the same social items (the case's congestion), never in the central total.
        # The published pairing is the case's: decision 4's victims on the Hispanic footing at the low end, the
        # custody footing at the high end.
        print("[§7: variants beside the central total]")
        for run, (column, note) in BESIDE_RUNS[case].items():
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
                add("7", column, f"published pairing per group member ({end})", {case: pairing[i] / pop[case]}, unit="$k", note=note)
    if case in RESTATED:
        # The pairing on the population the account prices: the population lane restates each row, then divides.
        print("[§7: the pairing on the priced count]")
        own_social = (socm[case][0], social(c, victims["custody"], congestion=cong[case], items=items[case][0])[1])
        own = (fiscal[case]["hispanic"][0] + own_social[0], fiscal[case]["custody"][1] + own_social[1])
        lane = {(r["section"], r["end"]): r for r in csv.DictReader(paths["restated"].open())}
        note = (f"{rel(paths['restated'])} section pairing_5plus: every row on audit row 4's count, the crash and "
                "congestion rows' NHTS ratios on persons aged 5+; low end Hispanic footing with decision 4's mixed-group "
                "victims, high end custody footing")
        base = RESTATED_BASE.get(case)
        if base is None:
            for i, end in enumerate(("low", "high")):
                p5, m5 = lane[("pairing_5plus", end)], lane[("per_member_5plus", end)]
                gate(f"the population lane restated this script's own pairing ({end})",
                     abs(float(p5["published"]) - own[i]) < 1e-6, f"{p5['published']} / {own[i]:.6f}")
                gate(f"the population lane divided by the priced count ({end})",
                     abs(float(m5["restated"]) - float(p5["restated"]) / pop[case]) < 1e-6, f"{m5['restated']} $k")
                add("7", "pairing_on_priced_count", f"published pairing ({end})", {case: float(p5["restated"])}, note=note)
                add("7", "pairing_on_priced_count", f"published pairing per group member ({end})",
                    {case: float(p5["restated"]) / pop[case]}, unit="$k", note=note)
        else:
            # The lane restated the base case's pairing. Its fiscal row is the base case's band (factor 1), so the
            # pairing less that row is the restated social rows, which this case shares; the case adds its own fiscal
            # rows. Tolerance 2e-6: the lane prints six decimals, and each social figure is a difference of two.
            by_item = {(r["section"], r["item"], r["end"]): r for r in csv.DictReader(paths["restated"].open())}
            paths["restated_base_bands"] = OUT_DIRS[base] / "band_variants.csv"
            base_bands = pd.read_csv(paths["restated_base_bands"]).set_index(["case", "variant"])
            base_fiscal = (float(base_bands.loc[(base, "justice_raw_coding"), "cost_low_bn"]),
                           float(base_bands.loc[(base, "adopted"), "cost_high_bn"]))
            restated_social = []
            for i, end in enumerate(("low", "high")):
                p5, fr = lane[("pairing_5plus", end)], by_item[("row", "fiscal", end)]
                gate(f"the population lane's fiscal row is the {base} case's band, unrestated ({end})",
                     abs(float(fr["published"]) - base_fiscal[i]) < 1e-6 and fr["restated"] == fr["published"],
                     f"{fr['published']} / {base_fiscal[i]:.6f}")
                soc_published = float(p5["published"]) - float(fr["published"])
                gate(f"the population lane's published social rows are this case's social rows ({end}, 2e-6)",
                     abs(soc_published - own_social[i]) < 2e-6, f"{soc_published:.6f} / {own_social[i]:.6f}")
                restated_social.append(float(p5["restated"]) - float(fr["restated"]))
            note_case = (f"the case's fiscal rows (band_variants.csv: justice_raw_coding low, adopted high) plus the "
                         f"social rows of {rel(paths['restated'])} section pairing_5plus less its fiscal row (the {base} "
                         "case's): every social row on audit row 4's count, the crash and congestion rows' NHTS ratios on "
                         "persons aged 5+; low end Hispanic footing with decision 4's mixed-group victims, high end custody "
                         "footing")
            # October 5 on: the added people's social rows join the pairing (lineage_social_rows()).
            added = (0.0, 0.0)
            if lineage_keys:
                lineage_detail, added = lineage_social_rows(paths["restated"], lineage_keys, restated_social)
                note_case += ("; plus the added people's social rows, each restated row times their share of its engine key "
                              "(band_variants.json lineage_social_keys); per member on the lineage population")
                lineage_doc = dict(
                    rule=("each restated social row (population lane, audit row 4's union, 5+ basis) times the added people's "
                          "share of the engine key it scales with at the band end's specification [ASSUMPTION]; restaurant "
                          "variety carries no head count and is not priced"),
                    keys=lineage_keys, rows=lineage_detail, union_social_bn=dict(zip(("low", "high"), restated_social)),
                    added_social_bn=dict(zip(("low", "high"), added)),
                    record_basis_rows="the section 7 rows on the lanes' published social rows carry the union's social rows only")
            for i, end in enumerate(("low", "high")):
                total = own[i] - own_social[i] + restated_social[i]
                if lineage_keys:
                    total += added[i]
                add("7", "pairing_on_priced_count", f"published pairing ({end})", {case: total}, note=note_case)
                add("7", "pairing_on_priced_count", f"published pairing per group member ({end})", {case: total / pop[case]},
                    unit="$k", note=note_case)
                add("7", "pairing_on_priced_count", f"social rows on the priced count ({end})", {case: restated_social[i]},
                    note=f"{rel(paths['restated'])} pairing_5plus less row fiscal, {end}")
                if lineage_keys:
                    add("7", "pairing_on_priced_count", f"the added people's social rows ({end})", {case: added[i]},
                        note="the 3.04M at their share of each row's engine key; lineage_social_* rows below")
            if lineage_keys:
                for d in lineage_detail:
                    for end in ("low", "high"):
                        add("7", f"lineage_social_{d['item']}", f"added people ({end})", {case: d[f"added_{end}_bn"]},
                            note=f"restated union row {d[f'union_{end}_bn']:.6f} x share {d[f'share_{end}']:.6f} "
                                 f"({d['keys'][end] or 'not priced: no head count in the item'})")
            held = (case, "justice_raw_coding_state_price_held")
            if held in bands.index:
                # The alternative to band_variants.cjs's re-pricing: the state-priced justice line held at the case's key.
                low_held = band(*held)[0] + restated_social[0]
                if lineage_keys:
                    low_held += added[0]
                note_held = ("alternative, beside: the low end with the state-priced justice line held at the case's use-key "
                             "amount (band_variants.csv justice_raw_coding_state_price_held); the central re-prices it on the "
                             "raw-coded key")
                add("7", "pairing_on_priced_count_state_price_held", "published pairing (low)", {case: low_held}, note=note_held)
                add("7", "pairing_on_priced_count_state_price_held", "published pairing per group member (low)",
                    {case: low_held / pop[case]}, unit="$k", note=note_held)
            for run in RESTATED_BESIDE.get(case, ()):
                k, (column, note_run) = f"{case}_{run}", BESIDE_RUNS[case][run]
                f_run = (band(k, "justice_raw_coding")[0], band(k, "adopted")[1])
                for i, end in enumerate(("low", "high")):
                    t_run = f_run[i] + restated_social[i]
                    if lineage_keys:
                        t_run += added[i]
                    add("7", f"pairing_on_priced_count_{column}", f"published pairing ({end})",
                        {case: t_run}, note=f"{note_run}; the social rows as in pairing_on_priced_count")
                    add("7", f"pairing_on_priced_count_{column}", f"published pairing per group member ({end})",
                        {case: t_run / pop[case]}, unit="$k", note=note_run)

    print("[§7b: custody footing, benefits priced]")
    soc = {k: social(c, c["victims_custody"], congestion=cong[k], items=cost_items[k][0]) for k in cols}
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
    shas = {rel(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths.values()}
    doc = dict(channels=c, target_population_m=pop_m, per_member_population_m=pop, care_constant_bn=care24,
               sources_sha256=shas)
    if later:
        doc = dict(case=case, columns=list(cols), **doc)
    if case in LONG_RUN:
        doc["congestion_by_band_end_bn"] = dict(
            case=case, central=dict(zip(("low_end", "high_end"), cong[case])),
            full_span=dict(zip(("low_end_lowest", "high_end_highest"), cong_span[case])),
            earlier_cases=dict(central=c["congestion"], full_span=[c["congestion_low"], c["congestion_high"]]),
            source=rel(LONG_RUN[case]))
        doc["beside_the_central_total"] = {f"{case}_{run}": note for run, (column, note) in BESIDE_RUNS[case].items()}
        if stale_congestion:
            doc["congestion_by_band_end_bn"]["not_recomputed"] = stale_congestion
        for flag in ("not_recomputed_v5", "not_recomputed_v6"):
            stale = summaries[case].get("beside_the_account", {}).get("congestion", {}).get(flag)
            if stale:
                doc["congestion_by_band_end_bn"][flag] = stale
    if lineage_doc:
        doc["lineage_social_rows"] = lineage_doc
    if case in SOCIAL_ITEMS:
        doc["social_items_in_the_social_rows"] = dict(
            case=case, central_bn=items[case][0], stacked_low_bn=items[case][1], stacked_high_bn=items[case][2],
            cost_items_bn=dict(zip(("central", "stacked_low", "stacked_high"), cost_items[case])),
            items=item_detail, never_added=("property values; each item's normalized figure; the crash lane's "
                                            "fault-based row; CO2, ozone and government-services emissions; disease, food "
                                            "safety and the cuisine mix"))
    if case in ("oct14", "oct15"):
        apply_p7_crime(rows, doc, case)
    if case == "oct15":
        apply_v8_environment(rows, doc, meta, summaries[case], args.v8_social_transport)
    require_within_budget("real-costs totals")
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    (out_dir / "real_costs_totals.json").write_text(json.dumps(doc, indent=1) + "\n")
    print("\n[result]")
    fmt = lambda v: "" if v is None else f"{v:9.3f}"  # noqa: E731
    for r in rows:
        print(f"  {r['section']:>4} {r['column']:<30} {r['item']:<42} {str(r['memo_printed'] or ''):>6} "
              f"{str(r['memo_method'] or ''):<12} " + " -> ".join(f"{fmt(r[k]):>9}" for k in cols) + f" {r['unit']}")
    print(f"all gates passed; {len(rows)} rows -> {rel(out)}")


if __name__ == "__main__":
    main()
