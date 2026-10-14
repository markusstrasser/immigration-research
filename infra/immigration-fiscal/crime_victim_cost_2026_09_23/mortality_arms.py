"""P7 mortality and mixed-offender arms; preserve every historical victim output.

Reuses the victim model unchanged. Central footings: equal (Hispanic per-capita
footing without mixed adjustment), mixed (adopted NCVS mixed-group correction),
custody (same correction times the institutional-residence ratio), and arrest
(victim lane's national 2019 adult-arrest footing; no NCVS mixed adjustment).
Native envelopes are available with and without the mixed adjustment, so the
consumer can isolate a fear-arm change from an offender-attribution change.
All are with/without outsider harms, despite the historical footing name equal.
Life-year ages come from primary SHR 2024, conditional on a known Hispanic first
offender and the same victim ethnicity. Missing ages are bounded at 0/100; these
are mortality assumptions, not observed counterfactual life spans.
"""
from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import resource
import sys
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FISCAL / "offender_ethnicity_nibrs_2026_09_23"))
sys.path.insert(0, str(FISCAL / "homicide_cost_2026_09_18"))
sys.path.insert(0, str(FISCAL / "crime_ratio_direction_2026_09_24"))
import victim_cost_rerun as original
import shr_analysis as shr
import vsl_standard as valuation
import dollar_effects as mixed_source

OUT = HERE / "derived"
FOOTINGS = ("equal", "mixed", "custody", "arrest", "envelope_low", "envelope_high",
            "envelope_low_unmixed", "envelope_high_unmixed")


def gate(name, ok):
    if not ok:
        raise ValueError(f"[BLOCKED] {name}")
    print(f"PASS {name}")


@lru_cache(maxsize=1)
def context():
    valuation.check_pins()
    vc = original.load_victim_lane()
    setup = original.setup(vc)
    return vc, setup


@lru_cache(maxsize=1)
def mixed_theta() -> float:
    primary = mixed_source.mixed_theta()
    theta = float(primary.set_index("offence").loc["All five", "mean_hispanic_fraction"])
    held = pd.read_csv(FISCAL / "crime_ratio_direction_2026_09_24/derived/nibrs_mixed_group_hispanic_fraction.csv")
    gate("exact NIBRS mixed fraction reproduces persisted six-decimal fraction", round(theta, 6) == float(
        held.set_index("offence").loc["All five", "mean_hispanic_fraction"]))
    mixed_source.nibrs_df.cache_clear()
    return theta


def mixed_matrix(matrix: pd.DataFrame) -> pd.DataFrame:
    lane = FISCAL / "crime_ratio_direction_2026_09_24/derived"
    factors = pd.read_csv(lane / "ncvs_victimization_factor.csv").set_index("victim")
    theta = mixed_theta()
    changed = matrix.copy()
    for victim in ("White", "Black", "Hispanic", "Other"):
        row = factors.loc[victim]
        excess = row.select_victimizations / row.lane_row_ratio - row.hispanic_offender_incidents
        changed.loc[victim, "Hispanic"] += theta * excess
        changed.loc[victim, "Other"] -= theta * excess
    gate("mixed groups conserve every victim-row incident total",
         np.max(np.abs(changed.sum(axis=1) - matrix.sum(axis=1))) < 1e-8)
    gate("mixed groups leave nonnegative incident cells", (changed >= 0).all().all())
    return changed


@lru_cache(maxsize=1)
def victim_age_profile() -> pd.DataFrame:
    cols = ["Year", "Solved", "Homicide", "Circumstance", "VicAge", "VicRace", "VicEthnic", "OffEthnic"]
    pieces = []
    for chunk in pd.read_csv(shr.RAW, usecols=cols, chunksize=100_000, low_memory=False):
        selected = chunk[chunk.Year.eq(2024) & chunk.Solved.eq("Yes")
                         & chunk.Homicide.eq("Murder and non-negligent manslaughter")
                         & ~chunk.Circumstance.isin(shr.JUSTIFIABLE)
                         & chunk.OffEthnic.eq("Hispanic origin")].copy()
        selected["victim_group"] = shr.ethnicity(selected.VicRace, selected.VicEthnic)
        selected["age"] = pd.to_numeric(selected.VicAge, errors="coerce")
        pieces.append(selected[["victim_group", "age"]])
    selected = pd.concat(pieces, ignore_index=True)
    table = valuation.life_table()
    records = []
    held = pd.read_csv(OUT / "shr_p_offender_given_victim.csv", dtype={"window": str})
    held = held[held.window.eq("2024")].set_index("victim")
    for group, label in {"hispanic": "Hispanic", "nh_white": "White", "nh_black": "Black", "nh_other": "Other"}.items():
        ages = selected[selected.victim_group.eq(group)].age
        known = ages[ages.between(0, 120)]
        gate(f"primary SHR 2024 age profile matches Hispanic-first-offender count, {group}",
             len(ages) == int(held.loc[group, "off_hispanic"]) and len(known) > 0)
        # 100+ uses the primary table's open final interval, rather than an invented age.
        known = known.clip(upper=100).astype(int)
        for rate in (0.0, 0.03):
            values = np.array([valuation.remaining_years(int(age), rate, table) for age in known])
            reference = valuation.remaining_years(valuation.REFERENCE_AGE, rate, table)
            low = (values.sum() + (len(ages) - len(known)) * valuation.remaining_years(100, rate, table)) / len(ages)
            high = (values.sum() + (len(ages) - len(known)) * valuation.remaining_years(0, rate, table)) / len(ages)
            records.append(dict(victim=label, real_discount_rate=rate, known_age_records=len(known),
                                all_records=len(ages), missing_age_records=len(ages) - len(known),
                                mean_known_age=float(known.mean()), remaining_years=float(values.mean()),
                                missing_age_low_years=low, missing_age_high_years=high,
                                reference_years=reference,
                                age_source="SHR 2024 known Hispanic first offender; same victim ethnicity",
                                assumption="Age distribution transferred to unresolved/nonreporting homicides within victim ethnicity"))
    return pd.DataFrame(records)


def active_victim_detail(footing="mixed", vsl_standard="legacy", real_discount_rate=0.0,
                         missing_age_arm="central") -> pd.DataFrame:
    if footing not in FOOTINGS or vsl_standard not in valuation.STANDARDS:
        raise ValueError("[BLOCKED] unknown footing or vsl_standard")
    vc, setup = context()
    nc, base = dict(setup["nc"]), dict(setup["base"])
    if footing in ("mixed", "custody", "envelope_low", "envelope_high"):
        nc["I"] = mixed_matrix(nc["I"])
    if footing == "custody":
        # The victim lane's ratio declaration owns its source and naming.
        ratios = vc.institutional_ratio()
        base["ratio"] = ratios["ratio_generic_reallocated"]
    if footing == "arrest":
        base["nonfatal_source"] = "arrests_2019"
    if footing in ("envelope_low", "envelope_low_unmixed"):
        base.update(unknown="known_only", victimisations=False,
                    ratio=vc.institutional_ratio()["ratio_generic_kept"], m="none",
                    hom_scope="cleared_only", k="k_floor")
    if footing in ("envelope_high", "envelope_high_unmixed"):
        base.update(ratio=vc.institutional_ratio()["ratio_generic_reallocated"], m="county",
                    hom_dist="joint_imputed", ncvs_year="2024", pop_basis="rate_x_target")
    if footing == "envelope_high":
        # The mixed correction is measured on pooled 2022–2024 cells. Transfer
        # its victim-row multiplier to the 2024-only envelope as an explicit
        # sensitivity, preserving that envelope's national row totals.
        multiplier = nc["I"].Hispanic / setup["nc"]["I"].Hispanic
        nc["I2024"] = nc["I2024"].copy()
        move = nc["I2024"].Hispanic * (multiplier - 1)
        nc["I2024"]["Hispanic"] += move
        nc["I2024"]["Other"] -= move
        gate("envelope high preserves 2024 victim-row totals", np.max(np.abs(
            nc["I2024"].sum(axis=1) - setup["nc"]["I2024"].sum(axis=1))) < 1e-8)
        gate("envelope high has nonnegative cells", (nc["I2024"] >= 0).all().all())
    result = vc.run(base, setup["P"][base["k"]], nc, setup["hom"], setup["s_pop"], setup["m_geo"])["detail"].copy()
    if vsl_standard != "legacy":
        ages = victim_age_profile()
        ages = ages[ages.real_discount_rate.eq(real_discount_rate)].set_index("victim")
        gate("life-year discount rate is declared", len(ages) == 4)
        for index, row in result[result.offence.eq("Murder")].iterrows():
            profile = ages.loc[row.victim]
            key = {"central": "remaining_years", "low": "missing_age_low_years", "high": "missing_age_high_years"}[missing_age_arm]
            result.loc[index, "unit_full"] = valuation.mortality_value(
                vsl_standard, remaining_years=float(profile[key]), reference_years=float(profile.reference_years))
    result["cost_full"] = result.outside_victims * result.unit_full
    result["footing"] = footing
    result["vsl_standard"] = vsl_standard
    result["real_discount_rate"] = real_discount_rate
    result["missing_age_arm"] = missing_age_arm
    return result


def main():
    started = time.perf_counter()
    vc, setup = context()
    held = pd.read_csv(OUT / "arms.csv").set_index("arm")
    equal = active_victim_detail("equal")
    gate("positive control central rounds to the original output", round(equal.cost_full.sum() / 1e9, 4) == held.loc["central", "full_bn"])
    dot = active_victim_detail("equal", "dot_uniform")
    gate("positive control DOT rounds to the original arm", round(dot.cost_full.sum() / 1e9, 4) == held.loc["price: Miller 2021 non-fatal + DOT 2024 VSL for murder", "full_bn"])
    for footing, standard, historical in (
            ("envelope_low_unmixed", "legacy", "ENVELOPE low, miller2021"),
            ("envelope_high_unmixed", "dot_uniform", "ENVELOPE high, miller2021_dot_vsl")):
        unchanged = active_victim_detail(footing, standard)
        gate(f"positive control {footing} reproduces its native historical price arm",
             round(unchanged.cost_full.sum() / 1e9, 4) == held.loc[historical, "full_bn"])
    frames, totals = [], []
    sampling = pd.read_csv(vc.NCVS / "derived/matrix_pooled_2022_2024.csv")
    sampling = sampling[sampling.offender.eq("Hispanic")].set_index("victim").se
    for footing in FOOTINGS:
        for standard in valuation.STANDARDS:
            scenarios = [(0.0, "central")]
            if standard == "dot_life_years":
                scenarios += [(0.03, "central"), (0.0, "low"), (0.0, "high")]
            for rate, age_arm in scenarios:
                detail = active_victim_detail(footing, standard, rate, age_arm)
                frames.append(detail)
                total = float(detail.cost_full.sum() / 1e9)
                conditional_se = np.nan
                se_scope = "Not calculated: arrest normalization or single-year envelope needs its own covariance"
                if footing not in ("arrest", "envelope_high", "envelope_high_unmixed"):
                    incident_matrix = setup["nc"]["I"]
                    if footing in ("mixed", "custody", "envelope_low"):
                        incident_matrix = mixed_matrix(incident_matrix)
                    nonfatal = detail[detail.offence.ne("Murder")].groupby("victim").cost_full.sum()
                    conditional_se = float(np.sqrt(sum((sampling[v] * nonfatal[v] /
                        incident_matrix.loc[v, "Hispanic"]) ** 2 for v in nonfatal.index)) / 1e9)
                    se_scope = "Understated NCVS GVP delta-method SE, cells independent, mixed correction/unknown distribution/prices fixed; not a replicate SE"
                totals.append(dict(footing=footing, vsl_standard=standard, real_discount_rate=rate,
                                   missing_age_arm=age_arm, full_bn=total,
                                   nonfatal_conditional_se_bn=conditional_se, se_scope=se_scope,
                                   outsider_homicides=float(detail[detail.offence.eq("Murder")].outside_victims.sum()),
                                   mortality_bn=float(detail[detail.offence.eq("Murder")].cost_full.sum() / 1e9)))
    details = pd.concat(frames, ignore_index=True)
    gate("victim costs reconstruct from matching outsider counts and unit costs",
         np.max(np.abs(details.cost_full - details.outside_victims * details.unit_full)) < 1e-6)
    details.to_csv(OUT / "mortality_detail.csv", index=False, float_format="%.10f", lineterminator="\n")
    totals = pd.DataFrame(totals)
    totals.to_csv(OUT / "mortality_arms.csv", index=False, float_format="%.10f", lineterminator="\n")
    victim_age_profile().to_csv(OUT / "mortality_age_profile.csv", index=False, float_format="%.10f", lineterminator="\n")
    (OUT / "vsl_standard.json").write_text(json.dumps(valuation.settings(), indent=2) + "\n")
    print(totals.to_string(index=False))
    print(f"Elapsed seconds: {time.perf_counter() - started:.3f}; peak RSS bytes: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
