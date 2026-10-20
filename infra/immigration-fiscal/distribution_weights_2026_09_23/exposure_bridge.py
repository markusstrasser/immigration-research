"""Channel exposure measurement, imported by distribute.py; never rebuilds coverage.

Own CPS uninsured and age-12+ drivers measure completion/calibration. Latent
and omitted people have source donor profiles, not observed identities. Those
profiles are a switched diagnostic; custody and precise metro exposures remain
unidentified and are never replaced with a universal lineage count multiplier.
"""
from __future__ import annotations

import json
import numpy as np
import pandas as pd


def digest(path):
    import hashlib
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def build(d, fiscal, path, policy="measured"):
    if policy == "require_own":
        raise SystemExit("[BLOCKED] own metro/tenure/ownership and custody/victim-overlap keys for latent/coverage people are unidentified")
    root = path.parent
    payload = json.loads((root / "main_case_2026_10_16/derived/corrections.json").read_text())
    meta = payload["meta"]
    raw = d.pw_production.to_numpy(float)
    calibrated = d.pw.to_numpy(float)
    original = d.target.to_numpy(bool)
    observed = ~d.other.to_numpy(bool) & d.civ.to_numpy(bool)
    completion = observed & ~original
    # The completed source roster carries original row-4 weights. These own
    # donor weights are read from its pinned cache, with source receipt checked.
    source = root / "coverage_bound_2026_10_14"
    audit = json.loads((source / "derived/pricing_audit_oct15_final_routing_set.json").read_text())
    cache = source / "_cache/oct15_final_routing/set/pricing.npz"
    receipt = audit["pricing_cache_sha256"]
    cache_hash = digest(cache)
    if cache_hash != receipt:
        raise SystemExit("[BLOCKED] exposure donor cache hash differs from source receipt")
    with np.load(cache) as z:
        donor_keys = pd.MultiIndex.from_arrays([z["person_ph_seq"], z["person_pppos"]])
        gen = z["generation"].copy()
        added_raw = z["added_weights"][:, 0].copy()
        weights = z["weights"][:, 0].copy()
    keys = pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]])
    idx = keys.get_indexer(donor_keys)
    if np.any(idx < 0):
        raise SystemExit("[BLOCKED] outside-channel donor not in CPS roster")
    original_donors = original[idx]
    row4_people = float(weights[original_donors].sum())
    if abs(row4_people-meta["lineage"]["counts"]["account_union"])>1e-3:
        raise SystemExit("[BLOCKED] exposure row4 original union count differs from the account")
    added = added_raw.copy()
    # Original added people remain unlocated: normalize their own source donor
    # shape to the case's admitted count, never to the entire lineage.
    added_count = meta["lineage"]["counts"]["added"]
    # added_weights also carries completed nonreporters; source completion has
    # its own observed identities and is counted separately here.
    donor_completed = completion[idx]
    added[donor_completed] = 0.
    if abs(added.sum()-added_count) > 1e-3:
        raise SystemExit("[BLOCKED] original-descendant donor count does not close after completion removal")
    missing = np.zeros(len(idx))
    counts = meta["native_minor_calibration"]["coverage_counts_by_generation"]
    for i, g in enumerate(("G1", "G2", "G3plus")):
        m = gen == i
        mass = weights[m] * d.central_member_factor.to_numpy()[idx[m]]
        missing[m] = mass / mass.sum() * counts[g]
    population = meta["population_v9"]
    missing_count = population["with_coverage"]-population["without_coverage"]
    if abs(missing.sum()-missing_count)>1e-3:
        raise SystemExit("[BLOCKED] calibrated coverage generation counts do not close")
    drivers = {
        "unreimbursed_care": (d.NOCOV_CYR.eq(3).to_numpy(float)+.5*d.NOCOV_CYR.eq(2).to_numpy(float),
            "uninsured person-years: full-year + half part-year; AHA source price and private offset fraction retained"),
        "crime": (d.A_AGE.ge(12).to_numpy(float),
            "source NCVS offender-ethnicity allocation uses Hispanic age12+; custody multiplier retained, not a new custody estimate"),
        "housing_net": (np.ones(len(d)),
            "population dose screen only, not incremental housing exposure; ACS reporter-or-Mexico-birth source already contains reporting completion; own metro/tenure/ownership counterfactual unavailable"),
    }
    rows, factors = [], {}
    for channel, (key, rule) in drivers.items():
        base = float((raw*original*key).sum())
        row4 = float(((weights-raw[idx])*original_donors*key[idx]).sum())
        complete = float((raw*completion*key).sum())
        calibration = float(((calibrated-raw)*observed*key).sum())
        latent = float(added@key[idx])
        covered = float(missing@key[idx])
        measured = (row4+complete+calibration)/base
        conditional = (row4+complete+calibration+latent+covered)/base
        national_raw = float((raw*d.civ.to_numpy(bool)*key).sum())
        national_calibrated = float((calibrated*d.civ.to_numpy(bool)*key).sum())+row4
        denominator_measured = 0.
        denominator_conditional = 0.
        if channel=="unreimbursed_care":
            # Source prices share of all uninsured person-years, not just its
            # target numerator. Completion/latent ancestry already exist in
            # the national roster; only constructed coverage adds denominator.
            measured_factor=(base+row4+complete+calibration)/base*national_raw/national_calibrated
            conditional_factor=(base+row4+complete+calibration+latent+covered)/base*national_raw/(national_calibrated+covered)
            denominator_measured=measured_factor-1-measured
            denominator_conditional=conditional_factor-1-conditional-denominator_measured
            measured=measured_factor-1
            conditional=conditional_factor-1
        # Housing's nonlinear metro dose and crime's victim/offender overlap are
        # not identified by a population or 12+ increment. Keep their central
        # source totals; report the priced exposure as a conditional diagnostic.
        admitted = measured if channel=="unreimbursed_care" else 0.
        if policy=="source_profile" and channel=="unreimbursed_care":
            admitted = conditional
        factors[channel] = 1+admitted
        for component, exposure, status in (
            ("row4_frame", row4, "measured original-union source donor weights minus published CPS weights"),
            ("completion", complete, "measured CPS source driver"),
            ("calibration", calibration, "measured CPS source driver on fixed rosters"),
            ("added", latent, "conditional source donor profile; unlocated"),
            ("coverage", covered, "conditional calibrated generation donor profile; tenure correlation unmeasured")):
            rows.append(dict(channel=channel, component=component, base_exposure=base,
                own_key_exposure=exposure, relative_change=exposure/base, status=status,
                central_admitted=(channel=="unreimbursed_care" and (component in ("row4_frame","completion","calibration") or policy=="source_profile")),
                central_multiplier=factors[channel],
                rule=rule))
        if channel=="unreimbursed_care":
            for component,relative,status,admit in (
                ("national_denominator_measured",denominator_measured,"measured all-civilian calibrated uninsured denominator, including numerator interaction",True),
                ("national_denominator_conditional",denominator_conditional,"conditional coverage uninsured denominator and numerator interaction",policy=="source_profile")):
                rows.append(dict(channel=channel,component=component,base_exposure=national_raw,
                    own_key_exposure=national_calibrated-national_raw+(covered if component.endswith("conditional") else 0.),
                    relative_change=relative,status=status,central_admitted=admit,central_multiplier=factors[channel],
                    rule="AHA national spending/private offset fraction held; reprice the source uninsured share with its own denominator"))
    for channel in drivers:
        selected=sum(r["relative_change"] for r in rows if r["channel"]==channel and r["central_admitted"])
        if abs(selected-(factors[channel]-1))>1e-12:
            raise SystemExit("[BLOCKED] own-key exposure components do not close: "+channel)
    rows.append(dict(channel="wages", component="all", base_exposure=np.nan,
        own_key_exposure=np.nan, relative_change=0., status="case-grid own P/F and reporter/coverage parts already priced; production denominator retained",
        central_admitted=True, rule="no additional scalar; exposure is wages by production skill/nativity cells"))
    return rows, factors, dict(policy=policy,status="[DEGRADED] partial exposure migration; housing/crime own counterfactual remains unmeasured", donor_cache=str(cache.relative_to(root)),
        donor_cache_sha256=cache_hash,
        native_factor_sha256=digest(root/"count_composition_r5_2026_10_15/derived/native_person_factors.parquet"),
        limitations=["Housing metro/tenure/owner counterfactual and crime custody/victim-overlap bridge remain unmeasured; priced source-driver screens are not estimates or bounds.",
          "Latent and coverage uninsured profiles conditional; AHA spending and private offset fraction held at source; observed national uninsured denominator recalibrated.",
          "Military replacement private surplus remains unidentified; gross fiscal service benefits are not net welfare."],
        population=population, missing_people=missing_count, original_added_people=added_count,
        row4_original_union_people=row4_people,published_source_original_union_people=float(raw[original].sum()))


def price(rows, tables):
    weighted = pd.DataFrame(tables["weighted"])
    out=[]
    for r in rows:
        if r["channel"]=="wages":
            continue
        # Exactly the lane's eta and equal-split normalization, same gain/loss
        # profile for each channel. This is explicit profile transport.
        frame=weighted[weighted.channel.eq(r["channel"])]
        for w in frame.to_dict("records"):
            out.append({**r,"measure":w["measure"],"eta":w["eta"],
                "delta_unweighted_bn":w["unweighted_bn"]*r["relative_change"]/r["central_multiplier"],
                "delta_person_p5_bn":w["person_p5"]*r["relative_change"]/r["central_multiplier"],
                "delta_equal_split_bn":w["equal_split_p5"]*r["relative_change"]/r["central_multiplier"],
                "recipient_profile":"source channel income profile held; same eta and normalization"})
    return pd.DataFrame(out)
