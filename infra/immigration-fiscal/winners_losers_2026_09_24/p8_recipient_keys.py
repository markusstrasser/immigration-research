"""Source-backed P8 recipient and jurisdiction keys; no channel totals estimated.

All returned person keys integrate against the caller's survey weights. Geographic
allocations conserve source amounts within states; absent recipient cells fail.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def _require(ok, message):
    if not bool(ok):
        raise ValueError(f"[BLOCKED] P8 recipient key: {message}")


def _allocate(mask, key, weights, amount):
    den = np.dot(weights[mask], key[mask])
    _require(den > 0 or amount == 0, "nonzero amount without eligible recipient mass")
    return np.where(mask, key * amount / den, 0.0) if den else np.zeros(len(weights))


def air_mortality_key(d, weights, fiscal, population="row4"):
    """Common NCHS mortality-rate key, calibrated to air lane's other-death ages.

    Central Orellano CRF includes all ages in mortality_items.py (i_crf=1).
    Preserve the source's 65+ fraction separately in every recipient state, so
    the caller's local/national exposure mix cannot change its age-mortality key.
    CPS age profiles within each side of 65 retain measured NCHS mortality rates.
    """
    lane = Path(fiscal) / "air_pollution_2026_09_28"
    rates_path = lane / "derived/mortality_rates.csv"
    context_path = lane / "derived/mortality_age_contexts.csv"
    infant_path = lane / "_cache/lt2024_Table01.xlsx"
    rates = np.zeros(101)
    for row in pd.read_csv(rates_path).itertuples():
        rates[int(row.age_low):int(row.age_high) + 1] = row.mortality_rate
    raw = pd.read_excel(infant_path, header=None)
    infant = raw[raw[0].astype(str).str.replace("–", "-", regex=False).str.match(r"^0\s*-\s*1")].iloc[0]
    age1 = raw[raw[0].astype(str).str.replace("–", "-", regex=False).str.match(r"^1\s*-\s*2")].iloc[0]
    rates[0] = (float(infant[2]) - float(age1[2])) / float(infant[4])
    contexts = pd.read_csv(context_path)
    contexts = contexts[contexts.population_basis.eq(population)].set_index("minimum_recipient_age")
    fraction = float(contexts.loc[65, "other_expected_baseline_deaths"] / contexts.loc[0, "other_expected_baseline_deaths"])
    ages = np.clip(d.A_AGE.to_numpy(int), 0, 100)
    other = d.other.to_numpy(bool)
    key = np.zeros(len(d))
    rows = []
    for state in sorted(d.loc[other, "st"].unique()):
        mask = other & d.st.eq(state).to_numpy()
        for old, share in ((False, 1 - fraction), (True, fraction)):
            key += _allocate(mask & ((ages >= 65) == old), rates[ages], weights, share)
        got = float(np.dot(weights[mask & (ages >= 65)], key[mask & (ages >= 65)]))
        _require(abs(got - fraction) < 1e-12, f"air age65 share in state {state}")
        rows.append(dict(state=int(state), age65_share=got))
    return key, dict(source_paths=[str(rates_path), str(context_path), str(infant_path)],
                     expected_age65_share=fraction, state_audit=rows,
                     assumption="common NCHS age rates; air-lane national recipient age margin held within each state; exposure dispersion remains caller's assumption")


def crash_victim_key(d, weights, fiscal):
    """FARS 2023 all fatal victims by five-year age and road-user role.

    CPS has no crash-victim role. Each role's age margin is distributed to all
    other residents of that age (an explicit exposure proxy), then roles sum.
    Nonfatal injury age/role incidence is unobserved here: fatal victims proxy it.
    Unknown ages are distributed in the observed age proportions, never dropped.
    """
    path = Path(fiscal) / "road_crash_externality_2026_09_28/_cache/fars2023/FARS2023NationalCSV/person.csv"
    source = pd.read_csv(path, usecols=["AGE", "PER_TYP", "INJ_SEV"], encoding="latin1")
    dead = source[source.INJ_SEV.eq(4)].copy()
    _require(len(dead) > 0, "FARS has no fatalities")
    return crash_key_from_victims(d, weights, dead, source_path=str(path))


def crash_key_from_victims(d, weights, victims, source_path="provided FARS fixture"):
    other = d.other.to_numpy(bool)
    bands = np.minimum(d.A_AGE.to_numpy(int) // 5, 17)
    known = victims.AGE.between(0, 120)
    measured = victims.loc[known].copy()
    measured["band"] = np.minimum(measured.AGE.to_numpy(int) // 5, 17)
    counts = measured.groupby(["PER_TYP", "band"]).size()
    _require(len(measured) > 0, "no known FARS victim ages")
    out = np.zeros(len(d))
    rows = []
    for (role, band), count in counts.items():
        # Age-unknown victims retain all source mass; their role-specific age
        # distributions use that role's observed ages, with national age proxy
        # only if the role has no measured ages (reported below).
        role_known = int((measured.PER_TYP == role).sum())
        role_all = int((victims.PER_TYP == role).sum())
        mass = count * role_all / role_known
        mask = other & (bands == band)
        out += _allocate(mask, np.ones(len(d)), weights, mass)
        rows.append(dict(role=int(role), age_band=int(band), victims=float(mass), known_age_victims=int(count)))
    absent_roles = sorted(set(victims.PER_TYP) - set(measured.PER_TYP))
    for role in absent_roles:
        number = int((victims.PER_TYP == role).sum())
        for band, count in measured.groupby("band").size().items():
            mass = number * count / len(measured)
            out += _allocate(other & (bands == band), np.ones(len(d)), weights, mass)
            rows.append(dict(role=int(role), age_band=int(band), victims=float(mass), known_age_victims=0))
    got = float(np.dot(weights, out))
    _require(abs(got - len(victims)) < 1e-8, "all crash victims conserved")
    return out, dict(source_paths=[source_path], fatal_victims=len(victims), assigned_victims=got,
                     unknown_age_victims=int((~known).sum()), roles_without_known_ages=[int(x) for x in absent_roles],
                     children_victims=int(victims.AGE.between(0, 17).sum()),
                     old_victims=int(victims.AGE.between(65, 120).sum()),
                     pedestrian_victims=int(victims.PER_TYP.eq(5).sum()), age_role_rows=rows,
                     assumption="FARS fatal-victim age/role mix proxies injury dollars; CPS has no road-user-role field; within-age national recipient proxy")


def lineage_payers_state_age(d, weights, lineage, wl, added_weights=None):
    """Thin native G3+ payers in the case's actual added state × age cells.

    Case places each age band's added people proportionally on its identified
    Mexican G3+ records. A caller can provide exactly those added record weights.
    Within a state-age cell payer identity remains a proportional survey proxy.
    """
    other = d.other.to_numpy(bool)
    third = d.PRCITSHP.isin([1, 2, 3]).to_numpy() & d.PEMNTVTY.isin(wl.US_AREAS).to_numpy() & d.PEFNTVTY.isin(wl.US_AREAS).to_numpy()
    nb = len(lineage["age_mix"]["bands"])
    bands = np.minimum(d.A_AGE.to_numpy(int) // 5, nb - 1)
    if added_weights is None:
        targets = d.target.to_numpy(bool) & third & d.PRDTHSP.eq(1).to_numpy()
        counts, mix = lineage["counts"], lineage["age_mix"]["mixes"]
        added = counts["at_g3_rate"] * np.array(mix["g3_rate"]) + counts["later_losses"] * np.array(mix["later"])
        added_weights = np.zeros(len(d))
        for band, amount in enumerate(added):
            added_weights += weights * _allocate(targets & (bands == band), np.ones(len(d)), weights, amount)
    added_weights = np.asarray(added_weights, dtype=float)
    _require(np.all(added_weights >= 0), "negative added-member targets")
    targets = pd.DataFrame(dict(state=d.st.to_numpy(int), band=bands, amount=added_weights)).groupby(["state", "band"]).amount.sum()
    out = weights.copy()
    rows = []
    for (state, band), amount in targets.items():
        mask = other & third & d.st.eq(state).to_numpy() & (bands == band)
        base = float(weights[mask].sum())
        _require(base >= amount and (base > 0 or amount == 0), f"state-age payer cell {state}/{band}: {amount} exceeds {base}")
        factor = 1 - amount / base if base else 1.0
        out[mask] *= factor
        got = float((weights - out)[mask].sum())
        _require(abs(got - amount) < 1e-7, f"state-age thinning {state}/{band}")
        rows.append(dict(state=int(state), age_band=lineage["age_mix"]["bands"][band], eligible_other=base, removed=float(amount), retained_factor=factor))
    _require(abs((weights - out).sum() - lineage["counts"]["added"]) < 1e-6, "removed lineage count")
    _require(not np.any((weights != out) & ~(other & third)), "only native G3+ nonmembers thin")
    return out, pd.DataFrame(rows)


def property_key_with_rentals(d, I, B, weights, fiscal):
    """Owner-occupied value plus rental value, assigned to property owners.

    Rental-value anchor is Fed Z.1 noncorporate residential market value, grossed
    up by RHFS reported corporate/REIT unit share (equal unit values assumed).
    State rental stock follows ACS exposed rent dollars, not owner-home values.
    CPS absolute HRNTVAL per household proxies landlords, including net losses.
    """
    owner = d.other.to_numpy(bool) & d.H_TENURE.eq(1).to_numpy()
    key = np.zeros(len(d))
    cell = B.bins(np.nan_to_num(I["R_spm"]["p_other"]), 100)
    geo = I["acs_geo"][("central", "national_uniform")]
    moved = []
    for state, raw in geo["value_cell_state"].items():
        margins = np.asarray(raw, dtype=float).reshape(100, 10).sum(axis=1).copy()
        mask = owner & d.st.eq(state).to_numpy()
        den = np.bincount(cell[mask], weights=weights[mask], minlength=100)
        have = np.flatnonzero(den > 0)
        _require(len(have) > 0 or margins.sum() == 0, f"state {state} owner recipients")
        for c in np.flatnonzero((margins > 0) & (den == 0)):
            nearest = int(have[np.argmin(abs(have - c))])
            margins[nearest] += margins[c]
            margins[c] = 0
            moved.append(dict(state=int(state), from_cell=int(c), to_cell=nearest))
        rates = np.divide(margins, den, out=np.zeros(100), where=den > 0)
        key[mask] = rates[cell[mask]]
    lane = Path(fiscal) / "housing_transfer_2026_09_23/derived"
    stock_path, types_path = lane / "inputs_land_foreign.csv", lane / "inputs_rhfs.csv"
    stock = pd.read_csv(stock_path).set_index("quarter").loc["2024:Q4"]
    types = pd.read_csv(types_path)
    corporate = float(types.loc[types.OWNENT.isin([6, 7]), "units_share_reported"].sum())
    ratio = float(stock.nc_resid_market / stock.hh_owner_occ_market / (1 - corporate))
    rental_total = float(np.dot(weights, key) * ratio)
    rent_state = {int(k): float(v) for k, v in geo["rent_state"].items()}
    den = sum(rent_state.values())
    _require(den > 0, "ACS rental stock state exposure")
    landlord = np.abs(d.HRNTVAL.to_numpy(float)) / d.n_other_hh.to_numpy(float)
    other = d.other.to_numpy(bool)
    rows = []
    rental = np.zeros(len(d))
    for state, amount in sorted(rent_state.items()):
        dollars = rental_total * amount / den
        mask = other & d.st.eq(state).to_numpy() & (landlord > 0)
        rental += _allocate(mask, landlord, weights, dollars)
        rows.append(dict(state=state, rental_value_key=float(dollars)))
    _require(not np.any(rental[~(other & (landlord > 0))]), "rental capitalization only landlords")
    return key + rental, dict(source_paths=[str(stock_path), str(types_path)],
                             owner_value_key=float(np.dot(weights, key)), rental_value_key=rental_total,
                             rental_owner_stock_ratio=ratio, state_rental_rows=rows,
                             property_empty_cell_transfers=moved,
                             assumption="Fed noncorporate residential stock plus RHFS corporate unit gross-up; equal value per owner type; ACS exposed rent state shares; landlord residence proxies property state; HRNTVAL includes royalties/estates/trusts")


def landlord_split_by_state(wl, d, weights, landlords):
    """RHFS owner types redistributed to capital holders within each state."""
    path = wl.FISCAL / "housing_transfer_2026_09_23/derived/inputs_rhfs.csv"
    ownership = pd.read_csv(path)
    individual = float(ownership.loc[ownership.OWNENT.eq(1), "units_share_reported"].iloc[0])
    corporate = float(ownership.loc[ownership.OWNENT.isin([6, 7]), "units_share_reported"].sum())
    ambiguous = 1 - individual - corporate
    _require(min(individual, corporate, ambiguous) >= 0, "RHFS owner shares")
    central, broad = individual * landlords, (individual + ambiguous) * landlords
    key = np.maximum(d.capital.to_numpy(float), 0)
    other = d.other.to_numpy(bool)
    rows = []
    for state in sorted(d.loc[other, "st"].unique()):
        mask = other & d.st.eq(state).to_numpy()
        amount = float(np.dot(weights[mask], landlords[mask]))
        central += _allocate(mask, key, weights, amount * (corporate + ambiguous))
        broad += _allocate(mask, key, weights, amount * corporate)
        for label, result in (("central", central), ("broad", broad)):
            got = float(np.dot(weights[mask], result[mask]))
            _require(abs(got - amount) / 1e9 < 1e-9, f"{label} landlord state {state} conservation")
        rows.append(dict(state=int(state), landlord_bn=amount / 1e9))
    ownership = ownership.assign(assignment=np.where(ownership.OWNENT.eq(1), "individual landlord", np.where(ownership.OWNENT.isin([6, 7]), "corporate/REIT capital income", "unresolved entity")))
    return central, broad, ownership, dict(individual=individual, corporate_reit=corporate, unresolved=ambiguous,
                                           source_paths=[str(path)], state_audit=rows,
                                           proxy="reported rental-unit shares proxy rent shares; corporate owners assigned to same-state capital holders")


def state_spending_shares(d, group_weights, programmes, fiscal, level):
    """Case S&L spending by programme's use key and producer state prices.

    Returns spending proportions only. Receipts do not inherit these proportions
    without an explicit incidence assumption by the consumer.
    """
    price_path = Path(fiscal) / "state_priced_services_2026_09_29/derived/state_per_capita.csv"
    prices = pd.read_csv(price_path)
    prices = prices[prices.year.eq(2024) & prices.basis.eq("direct")]
    price = prices.pivot(index="fips", columns="function", values="relative")
    populations = prices.groupby("fips").population.first()
    _require(prices.groupby("fips").population.nunique().eq(1).all()
             and populations.gt(0).all(), "state price population denominators")
    corrections_path = Path(fiscal) / "state_priced_services_2026_09_29/derived/corrections.csv"
    prison_path = Path(fiscal) / "state_priced_services_2026_09_29/derived/prison_cost_by_state.csv"
    school_path = Path(fiscal) / "school_cost_where_enrolled_2026_09_24/derived/state_breakdown.csv"
    corrections = pd.read_csv(corrections_path)
    central = corrections[corrections.candidate.astype(str).str.lower().eq("true")]
    prison = pd.read_csv(prison_path).set_index("fips")
    school = pd.read_csv(school_path).set_index("fips")
    source_paths = [str(price_path), str(corrections_path), str(prison_path), str(school_path)]
    notices = []
    state = d.st.to_numpy(int)
    age = d.A_AGE.to_numpy(int)
    group = np.asarray(group_weights, float) * d.target.to_numpy(bool)
    ones = np.ones(len(d))
    keys = {"education_k12": (age >= 5) & (age <= 17),
            "education_college_other": d.A_ENRLW.eq(1).to_numpy() & d.A_HSCOL.eq(2).to_numpy(),
            "medicaid_and_chip_other_medical": d.MCAID.eq(1).to_numpy()}
    keys["school_reprice"] = keys["education_k12"]
    keys["college_rekey"] = keys["education_college_other"]
    aggregate = {int(s): 0.0 for s in sorted(np.unique(state))}
    rows = []
    component_rows = []
    for item in programmes:
        _require("state_local_bn" in item and "id" in item, "programme jurisdiction fields missing")
        amount = float(item["state_local_bn"])
        if amount == 0:
            continue
        name = item["id"]
        base_name = name.removeprefix("state_price_")
        key = np.asarray(keys.get(base_name, ones), float)
        by = pd.Series(group * key).groupby(state).sum()
        function = None
        if name.startswith("state_price_"):
            frame = central[central.line.eq(base_name)]
            _require(len(frame) > 0, f"missing central state-price package {name}")
            _require(by.sum() > 0, f"state spending key empty {name}")
            geography = by / by.sum()
            correction = pd.Series(0.0, index=by.index)
            for part in frame.itertuples():
                if part.function == "corrections_per_inmate":
                    # Producer state_price.py:313-326,489-521: normalize the
                    # imprisonment-rate geography before applying per-inmate
                    # relative prices. DC has no state prisoners (federal).
                    active = by.index[by.gt(0) & (by.index != 11)]
                    _require(prison.reindex(active).relative.notna().all()
                             and prison.reindex(active).prisoners.notna().all()
                             and populations.reindex(active).notna().all(),
                             f"missing state imprisonment input {name}")
                    rate = prison.prisoners.div(populations).reindex(by.index)
                    rate.loc[rate.index == 11] = 0.0
                    rate = rate.fillna(0.0)
                    _require(rate.ge(0).all(), f"negative imprisonment rate {name}")
                    use = geography * rate
                    _require(use.sum() > 0, f"state prison use key empty {name}")
                    use /= use.sum()
                    rel = prison.relative.reindex(by.index).fillna(1.0)
                    rule = "group share × state imprisonment rate (normalized)"
                else:
                    rel = price[part.function].reindex(by.index)
                    _require(not ((by > 0) & rel.isna()).any(),
                             f"missing state price for {name}/{part.function}")
                    rel = rel.fillna(1.0)
                    use = geography
                    rule = "group programme use share"
                # Jails remain national-priced: no corrections-per-resident
                # arm enters this candidate package. Negative state parts stay.
                value = part.sl_amount_bn * use * (rel - 1)
                correction += value
                component_rows.extend(dict(programme=name, function=part.function,
                                           state=int(s), correction_mass=float(mass),
                                           use_share=float(use.loc[s]), rule=rule)
                                      for s, mass in value.items())
            by = correction
            function = "producer central subfunction signed price correction"
        elif base_name in ("education_k12", "school_reprice"):
            if base_name == "school_reprice":
                import json
                within_path = school_path.parent / "within_district.json"
                if str(within_path) not in source_paths:
                    source_paths.append(str(within_path))
                factor = json.loads(within_path.read_text())["TCURELSCS"]["factor_all_districts"]
                # The source preferred correction reweights states to the admin
                # pupil mix without changing the total number of group pupils.
                # Its published state vector is only the preferred one. Keep
                # the case's actual scalar amount at each end, and report this
                # spatial proxy rather than claim every arm was re-executed.
                count_ratio = school.account_group_pupils.sum() / school.admin_group_pupils.sum()
                corrected = (school.group_spending_per_pupil
                             * school.group_pupils_admin_over_account * count_ratio * factor)
                rel = (corrected - school.assf_per_pupil).reindex(by.index)
                notices.append("[DEGRADED] school_reprice geography uses preferred administrative-state/district spatial proxy at all ends; actual case scalar preserved; end-specific district prices and K-12/postsecondary mixture correction lack a producer state-component vector")
                function = "preferred school corrected-minus-embedded state price (spatial proxy)"
            else:
                rel = school.assf_per_pupil.reindex(by.index)
                function = "embedded ASSF state-average school price"
            # Several states have zero group pupils and no matched district.
            _require(not ((by > 0) & rel.isna()).any(), f"missing state school price {name}")
            by *= rel.fillna(0)
        den = float(by.sum())
        _require(den != 0, f"state spending key empty {name}")
        for s, mass in by.items():
            dollars = amount * float(mass) / den
            aggregate[int(s)] += dollars
            rows.append(dict(level=level, programme=name, state=int(s), cost_bn=dollars,
                             key="survey programme use" if base_name in keys else "case group persons; no state use field",
                             price=function or "national price"))
    total = sum(aggregate.values())
    _require(total > 0 and min(aggregate.values()) >= -1e-10, "state spending aggregate must be positive")
    shares = {s: v / total for s, v in aggregate.items()}
    _require(abs(sum(shares.values()) - 1) < 1e-12, "state spending shares close")
    return shares, dict(source_paths=source_paths, level=level, spending_bn=total,
                        programme_state_rows=rows,
                        price_component_state_rows=component_rows,
                        notices=notices,
                        assumption="synthetic corrections use producer normalized geography × (relative price - 1); prisons normalize group share × state imprisonment rate; jails remain national; schools split embedded ASSF prices from a declared preferred corrected-minus-embedded spatial proxy; other unpriced lines use group programme use, otherwise persons; spending geography does not identify receipt geography")
