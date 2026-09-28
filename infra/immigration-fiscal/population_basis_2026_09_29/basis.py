"""The population basis of every row of the September 27 fiscal-plus-social pairing, and the factor that puts
the row on the adopted account's own count (audit row 4: 39,712,493 people in a civilian frame of 335,543,722).

One record per row and pairing end where the row's value differs by end. The pairing
($416.19-490.74bn) is the Hispanic footing with decision 4's mixed-group victims at the low end and the
custody footing at the high end (sept24_propagation_2026_09_24/real_costs_totals.py:433); every added social
item enters both ends at its central value.

Factors come from three places, named in `factor_method`:
  frame_counts.csv  rows that are linear in a CPS count: the ratio of that count (or share) under the row-4
                    and the published weights
  reeval.csv        rows whose lane function is not linear in the count: the lane's own code re-evaluated here
                    on the row-4 counts, after a positive control reproduces its published figure
  none              rows with no CPS count in them (factor 1)
The trade row's factor is first order: the account's raw consumption key moved under row 4, applied to the
lane's saving-corrected key.

Gates (exit 1, nothing written): the published shares rebuilt from frame_counts.csv equal the ones the lanes
used (victim lane s, uninsured share, the volunteering 16+ count, the consumption key share); every reeval row
the table names exists. Writes basis.csv. Run from the repository root after frame_counts.py and reeval.py:
  uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/basis.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "basis.csv"
FAILS: list[str] = []
FIELDS = ["row", "end", "lane", "source_file", "population_basis", "scales_with_headcount", "factor", "evidence",
          "note", "sign", "value_ref", "factor_method"]


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def read_csv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def main():
    k = {r["count"]: (float(r["published"]), float(r["row4"])) for r in read_csv(HERE / "derived" / "frame_counts.csv")}
    re = {r["row"]: float(r["factor"]) for r in read_csv(HERE / "derived" / "reeval.csv")}
    ratio = lambda num, den: (k[num][1] / k[den][1]) / (k[num][0] / k[den][0])  # noqa: E731
    n0, n4 = k["union|all"]

    print("[published shares rebuilt from the frame]")
    s0 = k["union|12_plus"][0] / k["cps_hispanic_civilian|12_plus"][0]
    scaling = {r["item"]: float(r["value"]) for r in
               read_csv(FISCAL / "crime_victim_cost_2026_09_23" / "derived" / "scaling_hispanic_to_mexican.csv")}
    gate("victim lane's s = union 12+ / CPS Hispanic 12+", abs(s0 - scaling["population share, within CPS (central)"]) < 1e-6,
         f"{s0:.6f}")
    f_s = ratio("union|12_plus", "cps_hispanic_civilian|12_plus")
    f_s_moved = k["union|12_plus"][1] / k["union|12_plus"][0]      # if row 4's weight went to other Hispanics
    unc = json.loads((FISCAL / "uncompensated_care_2026_09_23" / "derived" / "summary.json").read_text())
    py0 = k["union|uninsured_person_years"][0] / k["cps_all_civilian|uninsured_person_years"][0]
    gate("uncompensated-care lane's share of uninsured person-years", abs(py0 - unc["target_share"]) < 1e-9, f"{py0:.6f}")
    f_py = ratio("union|uninsured_person_years", "cps_all_civilian|uninsured_person_years")
    adult16 = [k["union|18_plus"][i] + k["union|12_17"][i] / 3 for i in (0, 1)]
    vol = [r for r in read_csv(FISCAL / "benefits_inventory_2026_09_28" / "derived" / "items.csv")
           if r["item"] == "formal_volunteering_outside_group" and r["measure"] == "absolute"][0]
    gross = adult16[0] * 0.169 * 4.99e9 / 75.7e6 * 167.2e9 / 4.99e9 / 1e9          # build_tables.py:110-112
    gate("volunteering central rebuilds from the union's 16+ count", abs(round(-0.55 * gross, 4) - float(vol["central_bn"])) < 1e-9,
         f"16+ {adult16[0]:,.1f}; {-0.55 * gross:.4f}")
    f_vol = adult16[1] / adult16[0]
    bins = pd.read_csv(FISCAL / "main_case_decomposition_2026_09_29" / "derived" / "age_bins.csv")
    cons = bins[(bins.key == "receipt|consumption") & (bins.allocation == "personal")]
    c = {w: cons[cons.weights == w].union.sum() / cons[cons.weights == w].national.sum() for w in ("published", "row4")}
    specs = {r["spec"]: float(r["key_share"]) for r in read_csv(FISCAL / "consumption_key_2026_09_24" / "derived" / "key_specs.csv")}
    gate("the account's raw consumption key is the consumption lane's raw key", abs(c["published"] - specs["raw"]) < 1e-9,
         f"{c['published']:.6f}")
    gcs = specs["saving_central"]
    f_trade = (1 - gcs * c["row4"] / c["published"]) / (1 - gcs)
    for name in ("pm25_consumption", "congestion_low_end", "congestion_high_end", "road_crash_externality",
                 "housing_gain_low_end", "housing_gain_high_end", "fear_avoidance", "private_security",
                 "school_disruption", "scale_net_earnings", "total_consumer_scale"):
        gate(f"reeval.csv has {name}", name in re)

    crime_basis = "40.90M CPS union: its 12+ share of CPS Hispanic 12+ (published weights), applied to NCVS Hispanic-offender incidents"
    hisp_removed = (k["cps_hispanic_civilian|all"][0] - k["cps_hispanic_civilian|all"][1]) / (n0 - n4)
    pop_share = ratio("union|all", "cps_all_civilian|all")
    crime_note = (f"Linear in s. Row 4 takes {(n0 - n4) / 1e6:.2f}M Mexico-born people, {hisp_removed:.1%} of them Hispanic, "
                  f"out of both the union and the CPS "
                  f"Hispanic count, so s falls {1 - f_s:.2%} ({s0:.6f} -> {s0 * f_s:.6f}), not 2.9%. Had row 4 moved "
                  f"their weight to other Hispanics (arm row4_other_hispanic), s would fall {1 - f_s_moved:.2%}.")
    rows = [
        dict(row="fiscal", end="low", lane="main_case_long_run_2026_09_27",
             source_file="sept27_propagation_2026_09_27/derived/band_variants.csv (sept27, justice_raw_coding)",
             population_basis="39.71M row 4 (the case's stack)", scales_with_headcount="yes; already on the row-4 count",
             factor=1.0, sign=1, value_ref="csv:hispanic|fiscal main case (low)", factor_method="none: already on the row-4 count",
             evidence="sept24_propagation_2026_09_24/band_variants.cjs:121 (raw-coding variant), :162 (run on the case's "
                      "corrected model, which applies audit row 4), :214 (the variant moves every specification by the same "
                      "amount on the uncorrected and corrected model); main_case_decomposition_2026_09_29/RESULT.md:130-134, "
                      ":248-256",
             note="The adopted band plus the raw-coding shift, -4.339204bn, which is identical on both weight sets by gate; "
                  "the stack holds the justice line's administrative keyed amount fixed across weight sets "
                  "(decomposition RESULT.md:182), so the shift carries no row-4 term [INFERENCE]."),
        dict(row="fiscal", end="high", lane="main_case_long_run_2026_09_27",
             source_file="sept27_propagation_2026_09_27/derived/band_variants.csv (sept27, adopted)",
             population_basis="39.71M row 4 (the case's stack)", scales_with_headcount="yes; already on the row-4 count",
             factor=1.0, sign=1, value_ref="csv:custody|fiscal main case (high)", factor_method="none: already on the row-4 count",
             evidence="band_variants.cjs:120,162; main_case_decomposition_2026_09_29/RESULT.md:248-256 (lead-verified)",
             note="The per-member division by 40.90M enters downstream: band_variants.cjs:232 writes the uncorrected "
                  "model's target_population, which real_costs_totals.py:292,355 divides by."),
        dict(row="victims", end="low", lane="crime_ratio_direction_2026_09_24",
             source_file="crime_ratio_direction_2026_09_24/derived/dollar_effects.csv (theta 0.4977, NIBRS TX+AZ)",
             population_basis=crime_basis, scales_with_headcount="yes, linear in s", factor=f_s, sign=1,
             value_ref="json:channels.victims_equal_mixed_group", factor_method="exact: linear in s; frame_counts.csv",
             evidence="crime_victim_cost_2026_09_23/victim_cost.py:432 (s), :324, :332, :368 (incidents x s); "
                      "offender_ethnicity_nibrs_2026_09_23/victim_cost_rerun.py:78,87 (the rerun keeps cps_share); "
                      "crime_ratio_direction_2026_09_24/dollar_effects.py:108,117 (theta moves incidents; s unchanged)",
             note=crime_note),
        dict(row="victims", end="high", lane="crime_victim_cost_2026_09_23",
             source_file="crime_victim_cost_2026_09_23/derived/arms.csv (ACS institutional ratio 1.118, generic reallocated)",
             population_basis=crime_basis, scales_with_headcount="yes, linear in s", factor=f_s, sign=1,
             value_ref="json:channels.victims_custody", factor_method="exact: linear in s; frame_counts.csv",
             evidence="victim_cost.py:432, :324 (s x ratio), :527 (custody arm: the ACS ratio on the same s)",
             note="The ACS institutional ratio 1.118 is an ACS measure and does not move; " + crime_note),
        dict(row="property_crime", end="low", lane="crime_victim_cost_2026_09_23",
             source_file="crime_victim_cost_2026_09_23/derived/property_proxy.csv (miller2021)",
             population_basis=crime_basis, scales_with_headcount="yes, linear in s", factor=f_s, sign=1,
             value_ref="json:channels.property_low", factor_method="exact: linear in s; frame_counts.csv",
             evidence="victim_cost.py:571 (property proxy takes s cps_share), :652 (victimisations x Hispanic arrest share x s)",
             note="Linear in s, as the victims row."),
        dict(row="property_crime", end="high", lane="crime_victim_cost_2026_09_23",
             source_file="crime_victim_cost_2026_09_23/derived/property_proxy.csv (mccollister2010)",
             population_basis=crime_basis, scales_with_headcount="yes, linear in s", factor=f_s, sign=1,
             value_ref="json:channels.property_high", factor_method="exact: linear in s; frame_counts.csv",
             evidence="victim_cost.py:571, :652", note="Linear in s, as the victims row."),
    ]
    care = dict(lane="uncompensated_care_2026_09_23",
                population_basis="40.90M CPS union: its share of CPS civilian uninsured person-years (published weights)",
                scales_with_headcount="yes, linear in the uninsured share", sign=1,
                factor_method="exact: linear in the uninsured share; frame_counts.csv",
                evidence="uncompensated_care_2026_09_23/uncompensated.py:45 (canonical 40.90M target), :62,68 (share of "
                         "civilian uninsured person-years), :130,141 (outside the accounts = (1 - g) x share x national)",
                note=f"Row 4 removes mostly noncitizens, many uninsured: the union's uninsured person-years fall "
                     f"{1 - k['union|uninsured_person_years'][1] / k['union|uninsured_person_years'][0]:.1%}, so the share "
                     f"falls {1 - f_py:.1%} ({py0:.6f} -> {py0 * f_py:.6f}).")
    rows += [dict(care, row="unreimbursed_care", end="low", factor=f_py, value_ref="json:channels.unreimbursed_low",
                  source_file="uncompensated_care_2026_09_23/derived/added_cost_arms.csv (use 1.0, 2017 offsets, 2020 prices)"),
             dict(care, row="unreimbursed_care", end="high", factor=f_py, value_ref="json:channels.unreimbursed_high",
                  source_file="uncompensated_care_2026_09_23/derived/added_cost_arms.csv (use 1.0, 2013 offsets, 2024 prices)")]
    cong = dict(lane="service_response_long_run_2026_09_27",
                population_basis="40.90M CPS union: the ACS group (39.43M) scaled up to it within UMR urban areas",
                scales_with_headcount="yes, not linear (ln(1 - s), free-flow cap), net of a lane cut held at the "
                                      "adopted case's key share", sign=1,
                factor_method="exact: lane function re-evaluated here (reeval.csv)",
                evidence="congestion_2026_09_23/arms.py:59 (TARGET 40.896574m), :240-242, :288 (ACS group scaled up), "
                         ":471, :494; service_response_long_run_2026_09_27/congestion.py:63,80 (same scale), :139,145 "
                         "(lane cut from the long-run case's key share on the corrected account)",
                note="The lane cut uses the economic-affairs key share of the corrected account (0.0806), already on the "
                     "row-4 count, and is held; only the group's local traffic shares move.")
    rows += [dict(cong, row="congestion", end="low", factor=re["congestion_low_end"],
                  value_ref="json:congestion_by_band_end_bn.central.low_end",
                  source_file="service_response_long_run_2026_09_27/derived/net_change.json (by_band_end.low)"),
             dict(cong, row="congestion", end="high", factor=re["congestion_high_end"],
                  value_ref="json:congestion_by_band_end_bn.central.high_end",
                  source_file="service_response_long_run_2026_09_27/derived/net_change.json (by_band_end.high)")]
    hous = dict(lane="housing_transfer_2026_09_23", scales_with_headcount="yes, not linear (rent path in s)", sign=-1,
                factor_method="exact: lane function re-evaluated here (reeval.csv)",
                evidence="housing_transfer_2026_09_23/arms.py:61 (TARGET), :154-155 (metro shares scaled to the CPS "
                         "union), :200 (national-uniform share TARGET / RESIDENTS)",
                note="A gain to other residents, subtracted in the pairing; group rents stay ACS amounts, only the "
                     "group's population share moves.")
    rows += [dict(hous, row="housing_gain", end="low", factor=re["housing_gain_low_end"],
                  value_ref="json:channels.housing_gain_metro_local",
                  population_basis="40.90M CPS union: the ACS group scaled up to it within CBSAs",
                  source_file="housing_transfer_2026_09_23/derived/arms_summary.csv (long run, central_metro_local)"),
             dict(hous, row="housing_gain", end="high", factor=re["housing_gain_high_end"],
                  value_ref="json:channels.housing_gain_national",
                  population_basis="40.90M CPS union: share 40.90M / 340.11M ACS residents, everywhere",
                  source_file="housing_transfer_2026_09_23/derived/arms_summary.csv (long run, central_national_uniform)")]
    item = lambda i: f"csv:social_item_{i}|central, both ends"  # noqa: E731
    rows += [
        dict(row="fear_avoidance", end="both", lane="social_costs_unpriced_2026_09_28",
             source_file="social_costs_unpriced_2026_09_28/derived/items.csv", population_basis=crime_basis + " (the victim lane's central)",
             scales_with_headcount="yes, linear in s", factor=re["fear_avoidance"], sign=1, value_ref=item("fear_avoidance"),
             factor_method="exact: lane function re-evaluated here (reeval.csv)",
             evidence="social_costs_unpriced_2026_09_28/items.py:51 (victim cost by offence from the victim lane's "
                      "central), :81 (phi x WTP excess x victim cost)",
             note="Scales exactly with the victims row's s."),
        dict(row="private_security", end="both", lane="social_costs_unpriced_2026_09_28",
             source_file="social_costs_unpriced_2026_09_28/derived/items.csv",
             population_basis="40.90M CPS union: offending shares through the victim lane's s, less the population "
                              "share 40.90M / 336.73M",
             scales_with_headcount="partly: the difference of two headcount-based shares", factor=re["private_security"],
             sign=1, value_ref=item("private_security"), factor_method="exact: lane function re-evaluated here (reeval.csv)",
             evidence="items.py:34,37,39 (population share), :128,136 (offending shares from the victim lane), :143 "
                      "(excess = offending share - population share), :171",
             note=f"A small difference of two shares: the offending share falls {1 - f_s:.1%}, the population share "
                  f"{1 - pop_share:.1%}, so the gain shrinks {1 - re['private_security']:.0%}."),
        dict(row="school_disruption", end="both", lane="social_costs_unpriced_2026_09_28",
             source_file="social_costs_unpriced_2026_09_28/derived/items.csv",
             population_basis="8.487M group pupils on the published CPS weights (the 40.90M union); outsider exposure "
                              "from ACS tracts",
             scales_with_headcount="weakly: through the group's pupil count", factor=re["school_disruption"], sign=1,
             value_ref=item("school_disruption"),
             factor_method="re-evaluated here (reeval.csv); pupils moved with the union aged 5-17 [proxy]",
             evidence="items.py:206 (pupil share 8.487m / (8.487m + 39.45m)), :224; school_dilution_2026_09_24/price.py:54 "
                      "(the account's transported CPS count); school_cost_where_enrolled_2026_09_24/account_pupils.py:51,54 "
                      "(published person weights x K-12 rates)",
             note=f"Row 4 removes few children (the union aged 5-17 falls {1 - k['union|5_17'][1] / k['union|5_17'][0]:.1%}). "
                  "The exact pupil count needs the school-cost lane on row-4 weights."),
        dict(row="pm25_consumption", end="both", lane="air_pollution_2026_09_28",
             source_file="air_pollution_2026_09_28/derived/items.csv",
             population_basis="40.90M CPS union / 336.73M CPS civilian frame",
             scales_with_headcount="yes, near-linear in the population share", factor=re["pm25_consumption"], sign=1,
             value_ref=item("pm25_consumption"), factor_method="exact: lane function re-evaluated here (reeval.csv)",
             evidence="air_pollution_2026_09_28/air_items.py:29,31 (n and frame), :107 (s = n / frame), :113-114 (the "
                      "self-share sigma and the base both in s)",
             note=f"The share falls {1 - pop_share:.2%} (to {n4 / k['cps_all_civilian|all'][1]:.6f}, the account's own "
                  f"per-head share); a smaller group breathes less of its own pollution, so the item falls "
                  f"{1 - re['pm25_consumption']:.1%}."),
        dict(row="road_crash_externality", end="both", lane="road_crash_externality_2026_09_28",
             source_file="road_crash_externality_2026_09_28/derived/items.csv",
             population_basis="40.90M CPS union / 336.73M CPS civilian frame; q from the congestion lane's 40.90M-scaled "
                              "exposures", scales_with_headcount="yes, near-linear in the traffic share",
             factor=re["road_crash_externality"], sign=1, value_ref=item("road_crash_externality"),
             factor_method="exact: lane function re-evaluated here (reeval.csv)",
             evidence="road_crash_externality_2026_09_28/crash_model.py:84,91-92 (union, frame, union share of Hispanic "
                      "residents), :109 (q from the congestion exposures), :160,162-163",
             note=f"The traffic share falls about {1 - pop_share:.1%}, but q (the chance the other party is a group "
                  f"member) falls too, which raises the outsider share of each crash; net "
                  f"-{1 - re['road_crash_externality']:.1%}."),
        dict(row="scale_net_earnings", end="both", lane="scale_spillovers_2026_09_23",
             source_file="scale_spillovers_2026_09_23/derived/summary.csv (joint_grid, CZ 1990)",
             population_basis="40.90M CPS union: the ACS group (39.43M) scaled up to it, 1990 commuting zones",
             scales_with_headcount="yes, not linear (ln(1 - s) and the schooling composition)",
             factor=re["scale_net_earnings"], sign=1, value_ref=item("scale_net_earnings"),
             factor_method="exact: lane function re-evaluated here (reeval.csv)",
             evidence="scale_spillovers_2026_09_23/arms.py:45-47 (CPS_UNION / ACS_GROUP), :121 (group counts scaled), "
                      ":257 (ln(1 - s))",
             note=f"A gain (negative cost); it shrinks {1 - re['scale_net_earnings']:.1%}, less than the count, "
                  "because the size and composition terms move in opposite directions."),
        dict(row="restaurant_variety_market_size", end="both", lane="disease_food_2026_09_28",
             source_file="disease_food_2026_09_28/derived/items.csv",
             population_basis="not headcount-based: an assumed share parameter", scales_with_headcount="no",
             factor=1.0, sign=1, value_ref=item("restaurant_variety_market_size"),
             factor_method="none: no CPS count in the item (factor 1)",
             evidence="disease_food_2026_09_28/price_items.py:163 (psi 0.05, [INFERENCE]), :179,183 (E x ((1 - psi)^"
                       "(-1/(sigma - 1)) - 1)); :19 (N_G divides only the per-member column)",
             note=f"The group's size enters only through the assumed psi (a spending share of 0.10 discounted). "
                  f"Scaled with the union count it would be x{n4 / n0:.6f}."),
        dict(row="formal_volunteering_outside_group", end="both", lane="benefits_inventory_2026_09_28",
             source_file="benefits_inventory_2026_09_28/derived/items.csv",
             population_basis="40.90M CPS union: persons 16+ (18+ plus a third of 12-17, 30.25M)",
             scales_with_headcount="yes, linear in the 16+ count", factor=f_vol, sign=1,
             value_ref=item("formal_volunteering_outside_group"),
             factor_method="exact: linear in the 16+ count; frame_counts.csv",
             evidence="benefits_inventory_2026_09_28/build_tables.py:18-19 (16+ count from the CPS file), :112 (gross = "
                      "16+ count x rate x hours x value)",
             note=f"A gain; row 4 removes adults, so the 16+ count falls {1 - f_vol:.1%} "
                  f"({adult16[0] / 1e6:.2f}M -> {adult16[1] / 1e6:.2f}M)."),
        dict(row="total_consumer_scale", end="both", lane="consumer_scale_2026_09_28",
             source_file="consumer_scale_2026_09_28/derived/items.csv",
             population_basis="40.90M CPS union: CE spending per person x the count; CBSA shares from the scale lane's "
                              "scaled areas", scales_with_headcount="yes, mostly linear; ln(1 - s) terms",
             factor=re["total_consumer_scale"], sign=1, value_ref=item("total_consumer_scale"),
             factor_method="exact: lane main() rerun here with its outputs redirected (reeval.csv)",
             evidence="consumer_scale_2026_09_28/price_items.py:90 (n_group), :114,117,127 (CBSA shares), :157 (media), "
                      ":185 (network costs = spending per person x n_group)",
             note="A net gain of four items with mixed signs; items.csv rounds to 4 dp."),
        dict(row="total_trade_travel_fdi", end="both", lane="trade_networks_2026_09_28",
             source_file="trade_networks_2026_09_28/derived/items.csv",
             population_basis="not headcount-based: a literature network elasticity on measured US-Mexico flows; the "
                              "beneficiaries' share uses the CPS consumption key (published weights)",
             scales_with_headcount="no; inversely through the beneficiaries' share", factor=f_trade, sign=1,
             value_ref=item("total_trade_travel_fdi"),
             factor_method="first order: the raw consumption key's row-4 move applied to the lane's saving-corrected key",
             evidence="trade_networks_2026_09_28/price_trade_networks.py:60 (central s_first, not a headcount), :147 "
                      "(others' share = 1 - 0.0889), :157,171 (visits and FDI from measured flows)",
             note=f"Others receive 1 - {gcs:.4f} of the gain; the group's consumption share falls "
                  f"{1 - c['row4'] / c['published']:.2%} under row 4, so others' share rises {f_trade - 1:.2%}."),
    ]
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    with OUT.open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({**r, "factor": f"{r['factor']:.9f}"})
    for r in rows:
        print(f"  {r['row']:34s} {r['end']:5s} x{r['factor']:.6f}  {r['factor_method']}")
    print(f"  wrote {len(rows)} rows -> {OUT.relative_to(FISCAL)}; union {n0:,.1f} -> {n4:,.1f}")


if __name__ == "__main__":
    main()
