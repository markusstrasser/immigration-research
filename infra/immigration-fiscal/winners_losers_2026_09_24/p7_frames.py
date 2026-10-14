"""P7 incidence fixes beside the frozen hybrid positive control.

Native-First: reuse the lane's allocation engine and primary case outputs. No
fiscal headline is re-estimated. New tables identify financing, sharing, payer
population and channel coverage separately. All new national closures use an
absolute 1e-9bn gate. The original files retain the hybrid calculation record.
"""
from __future__ import annotations

import itertools
import ast
import json
import types
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
GATES = {}
PINS = {}
CUT_CACHE = {}


def require(name, ok, **detail):
    GATES[name] = dict(passed=bool(ok), **detail)
    if not ok:
        raise RuntimeError(f"[BLOCKED] P7 {name}: {detail}")


def pin(path, wl):
    path = Path(path).resolve()
    key = str(path.relative_to(wl.ROOT))
    value = wl.file_sha(path)
    require(f"within_run_pin_{key}",key not in PINS or PINS[key]==value,path=key)
    manifest = HERE / "inputs/pins.json"
    if manifest.exists():
        expected = json.loads(manifest.read_text())["sha256"]
        require(f"pin_{key}", key in expected and expected[key] == value, path=key)
    PINS[key] = value
    return path


def pin_generated(path, logical_key, wl):
    value=wl.file_sha(path)
    manifest=HERE/"inputs/pins.json"
    if manifest.exists():
        expected=json.loads(manifest.read_text())["sha256"]
        require(f"pin_{logical_key}",expected.get(logical_key)==value)
    PINS[logical_key]=value
    return Path(path)


def total(x, weights):
    return float(np.dot(x, weights) / 1e9)


def weighted_frame(d, weights):
    """Replace only the weight column; never duplicate the complete microdata."""
    out = d.copy(deep=False)
    out["pw"] = weights
    return out


def check_total(name, x, weights, target):
    got = total(x, weights)
    require(name, abs(got - target) < 1e-9, got_bn=got, target_bn=float(target))


def pooler(d, weights, include=None):
    """Weighted pooling; preserve the mass of exactly the declared population."""
    codes, _ = pd.factorize(d.SPM_ID)
    use = d.other.to_numpy() if include is None else include
    w = np.where(use, weights, 0.0)
    den = np.bincount(codes, weights=w)

    def pool(x):
        num = np.bincount(codes, weights=w * x, minlength=len(den))
        mean = np.divide(num, den, out=np.zeros_like(num), where=den > 0)
        return np.where(use, mean[codes], 0.0)
    return pool


def unequal_wages(d, wages, weights, retention):
    """Each person retains s; the residual is shared among the other unit members.

    This is a transfer rule, not a convex combination of the person/pooled net
    counts. With unequal survey weights, transfer weighted dollars, conserving
    each unit's total. Singleton members retain their complete wage change.
    """
    other = d.other.to_numpy()
    codes, _ = pd.factorize(d.SPM_ID)
    w = np.where(other, weights, 0.0)
    den = np.bincount(codes, weights=w)[codes] - w
    transfer = np.divide((1 - retention) * w * wages, den,
                         out=np.zeros(len(d)), where=other & (den > 0))
    received = np.bincount(codes, weights=transfer)[codes] - transfer
    out = np.where(den > 0, retention * wages + received, wages)
    return np.where(other, out, 0.0)


def lineage_payers(d, weights, lineage, wl):
    """Remove added descendants from matching G3+ nonmember five-year cells.

    Their state, income and household assignments within a cell are unidentified;
    proportional thinning is a declared proxy. Removed mass is carried into the
    member pool at the case's identified G3+ age records, never discarded.
    """
    other = d.other.to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    third = native & d.PEMNTVTY.isin(wl.US_AREAS).to_numpy() & d.PEFNTVTY.isin(wl.US_AREAS).to_numpy()
    nb = len(lineage["age_mix"]["bands"])
    band = np.minimum(d.A_AGE.to_numpy() // 5, nb - 1)
    counts = lineage["counts"]
    mix = lineage["age_mix"]["mixes"]
    added = counts["at_g3_rate"] * np.array(mix["g3_rate"]) + counts["later_losses"] * np.array(mix["later"])
    out = weights.copy()
    rows = []
    for b, amount in enumerate(added):
        m = other & third & (band == b)
        base = weights[m].sum()
        require(f"lineage_payer_cell_{b}_has_mass", base >= amount and (base > 0 or amount == 0),
                available=float(base), removed=float(amount))
        factor = 1 - amount / base if base else 1
        out[m] *= factor
        rows.append(dict(age_band=lineage["age_mix"]["bands"][b], eligible_other=float(base),
                         removed=float(amount), retained_factor=float(factor)))
    require("payer_removed_count", abs((weights - out)[other].sum() - counts["added"]) < 1e-6,
            removed=float((weights - out)[other].sum()), added=float(counts["added"]))
    require("payer_nonnegative_and_only_other_g3_moves", bool(np.all(out >= 0)) and
            not np.any((out != weights) & ~(other & third)))
    return out, pd.DataFrame(rows)


def transport(x, old_weights, new_weights, d, by_state=True):
    """Preserve each signed channel's national totals, and state totals if asked.

    Reweighting the payer population changes who bears a fixed national channel.
    Positive and negative wage/rent arms are conserved separately; scaling a tiny
    net wage total would destroy its economically important gross transfers.
    """
    out = np.zeros(len(d))
    other = d.other.to_numpy()
    groups = np.unique(d.st[other]) if by_state else [None]
    for state in groups:
        m = other if state is None else other & d.st.eq(state).to_numpy()
        for positive in (True, False):
            sign = x > 0 if positive else x < 0
            active = m & sign
            old, new = np.dot(old_weights[active], x[active]), np.dot(new_weights[active], x[active])
            if old == 0:
                continue
            require(f"transport_has_mass_{state}_{positive}", new != 0)
            out[active] = x[active] * old / new
    check_total("transport_total", out, new_weights, total(x, old_weights))
    return out


def state_wages(d, weights, wage, wl, group_weights=None):
    """Conserve each nativity/skill gross wage change; concentrate it by group LF.

    State shock shares are the group's weighted earnings in each skill cell,
    normalized nationally, then dollars follow other workers' own earnings in
    the same state/nativity/skill cell. This is incidence, not a local CES solve.
    A state with group labour but no matching recipient is a hard failure.
    """
    other, target = d.other.to_numpy(), d.target.to_numpy()
    earn = d.earn.to_numpy()
    rows, out = [], np.zeros(len(d))
    for low in (True, False):
        skill = (d.A_HGA.to_numpy() <= 39) if low else (d.A_HGA.to_numpy() > 39)
        gw=weights if group_weights is None else group_weights
        labour = np.where(target & skill, gw * earn, 0.0)
        group_state = pd.Series(labour).groupby(d.st).sum()
        require(f"state_wage_group_labour_{low}", group_state.sum() > 0)
        shares = group_state / group_state.sum()
        for native in (True, False):
            m = other & skill & (d.native.to_numpy() == native)
            amount = total(np.where(m, wage, 0.0), weights)
            for state, fraction in shares.items():
                if fraction == 0:
                    continue
                r = m & d.st.eq(state).to_numpy()
                den = np.dot(weights[r], earn[r])
                require(f"state_wage_recipients_{low}_{native}_{state}", den > 0)
                out[r] = amount * 1e9 * fraction * earn[r] / den
                rows.append(dict(skill="hs_or_less" if low else "above_hs", nativity="native" if native else "foreign",
                                 state=int(state), group_labor_share=float(fraction), wage_bn=amount * fraction))
            check_total(f"state_wage_cell_{low}_{native}", np.where(m, out, 0), weights, amount)
    check_total("state_wage_national", out, weights, total(wage, weights))
    return out, pd.DataFrame(rows)


def extra_fields(d, B):
    fields = ["PTOTVAL", "SS_VAL", "SSI_VAL", "UC_VAL", "PAW_VAL", "ED_VAL", "MCAID", "MCARE",
              "SPM_SNAPSUB", "SPM_SCHLUNCH", "SPM_WICVAL", "SPM_ENGVAL", "SPM_CAPHOUSESUB",
              "WC_VAL","VET_VAL","DIS_VAL1","DIS_VAL2","ACTC_CRD","EIT_CRED","A_ENRLW","A_HSCOL"]
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", *fields])
    require("extra_person_join", np.array_equal(d[["PH_SEQ", "PPPOS"]], p[["PH_SEQ", "PPPOS"]]))
    for field in fields:
        d[field] = p[field].to_numpy()


def receipt_keys(d):
    """Receipt-of-programmes proxy, declared rather than tax/per-capita cuts.

    Cash benefits plus SPM noncash allocations, health enrollment and pupil-year
    indicators at fixed survey-wide prices. Government general services have no
    measured person receipt, so equal person receipt is explicitly used there.
    Components are reported, and the full key is held fixed across case ends.
    """
    n = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    cash = sum(np.maximum(d[x].to_numpy(float), 0) for x in ["SS_VAL", "SSI_VAL", "UC_VAL", "PAW_VAL", "ED_VAL"])
    noncash = sum(np.maximum(d[x].to_numpy(float), 0) / n for x in
                  ["SPM_SNAPSUB", "SPM_SCHLUNCH", "SPM_WICVAL", "SPM_ENGVAL", "SPM_CAPHOUSESUB"])
    return cash + noncash


def responding_programme_key(d,weights,programmes):
    """Current receipts valued at each responding programme's national budget.

    Cash/noncash data identify direct recipients. Health uses enrollment; K12
    uses school age and college uses current enrollment after 18. The remaining
    general services have no person receipt field: equal service-use proxy is
    reported programme by programme. No arbitrary health/school dollar price.
    """
    other=d.other.to_numpy()
    n=d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    def raw(name):
        return np.maximum(d[name].to_numpy(float),0)
    def spm(name):
        return raw(name)/n
    keys={"social_security":raw("SS_VAL"),"ssi":raw("SSI_VAL"),"unemployment":raw("UC_VAL"),
          "snap":spm("SPM_SNAPSUB"),"housing_subsidies":spm("SPM_CAPHOUSESUB"),"energy_assistance":spm("SPM_ENGVAL"),
          "medicare":d.MCARE.eq(1).to_numpy(float),"medicaid_and_chip_other_medical":d.MCAID.eq(1).to_numpy(float),
          "education_k12":d.A_AGE.between(5,17).to_numpy(float),
          "education_college_other":(d.A_ENRLW.eq(1)&d.A_HSCOL.eq(2)).to_numpy(float),
          "education_benefits":raw("ED_VAL"),"workers_compensation":raw("WC_VAL"),
          "veterans_pension_disability":raw("VET_VAL"),"temporary_disability":raw("DIS_VAL1")+raw("DIS_VAL2"),
          "family_and_general_assistance":raw("PAW_VAL"),"refundable_tax_credits":raw("ACTC_CRD")+raw("EIT_CRED")}
    key=np.zeros(len(d))
    table=[]
    for p in programmes:
        k=keys.get(p["id"],np.ones(len(d)))
        basis="survey receipt/enrollment proxy" if p["id"] in keys else "[ASSUMPTION] universal service receipt; programme has no CPS person field"
        den=np.dot(weights[other],k[other])
        require(f"receipt_key_{p['id']}",den>0)
        amount=p["national_bn"]*p["response"]
        key+=amount*1e9*np.where(other,k,0)/den
        table.append(dict(programme=p["id"],responding_national_bn=amount,key=basis))
    check_total("responding_receipt_key_national",key,weights,sum(p["national_bn"]*p["response"] for p in programmes))
    return key,table


def property_key(d, I, B, weights):
    """ACS state × income-percentile property-value margins on CPS owner cells."""
    owners = d.other.to_numpy() & d.H_TENURE.eq(1).to_numpy()
    key = np.zeros(len(d))
    cell = B.bins(np.nan_to_num(I["R_spm"]["p_other"]), 100)
    geo = I["acs_geo"][("central", "national_uniform")]["value_cell_state"]
    missing = []
    for state, raw in geo.items():
        margins = np.asarray(raw).reshape(100, 10).sum(axis=1)
        m = owners & d.st.eq(state).to_numpy()
        den = np.bincount(cell[m], weights=weights[m], minlength=100)
        # CPS and ACS rank frames differ: preserve the state's total value with
        # nearest populated CPS owner percentile for an empty ACS-priced cell.
        have = np.flatnonzero(den > 0)
        require(f"property_state_has_owners_{state}", len(have) > 0 or margins.sum() == 0)
        for c in np.flatnonzero((margins > 0) & (den == 0)):
            nearest = int(have[np.argmin(abs(have - c))])
            margins[nearest] += margins[c]
            margins[c] = 0
            missing.append(dict(state=int(state), from_cell=int(c), to_cell=nearest))
        rates = np.divide(margins, den, out=np.zeros(100), where=den > 0)
        key[m] = rates[cell[m]]
        require(f"property_margin_{state}", abs(np.dot(weights[m], key[m]) - raw.sum()) < max(1, raw.sum()) * 1e-12)
    require("property_no_renter_burden", not np.any(key[~owners]))
    return key, missing


def social_channels(wl, d, I, ch, meta, weights, population, rule, ctx):
    """Allocate every row of the authoritative live social set or fail closed."""
    source = pin(HERE/"inputs/social_oct14.json",wl)
    data = json.loads(source.read_text())
    primary = data["lineage_social_rows"]
    state_share = {wl.POSTAL[k]: v for k, v in meta["group_state_share"].items()}
    ones = np.ones(len(d))
    crimekey = I["keys_rank"]["serious"] * I["serious_share"] + I["keys_rank"]["simple"] * (1-I["serious_share"])
    # Place proxies describe victims, not where emissions happened: interstate
    # transport of pollution and production emissions are unidentified here.
    place_key = np.ones(len(d))
    pupils = d.A_AGE.between(5, 17).to_numpy(float)
    earn = d.earn.to_numpy()
    consumer = np.maximum(d.resources_pc.to_numpy(float), 0)
    adult = d.A_AGE.ge(16).to_numpy(float)
    places = pd.read_csv(pin(wl.FISCAL / "congestion_2026_09_23/derived/ua_exposure.csv",wl))
    places = places[places.in_scope & places.state.isin(wl.POSTAL)]
    drive_state = places.groupby("state").acs_group_vehicle_minutes.sum()
    drive_state = {wl.POSTAL[s]:float(v/drive_state.sum()) for s,v in drive_state.items()}
    pupils_by_state = pd.Series(d.pw.to_numpy()*d.target.to_numpy()*pupils).groupby(d.st).sum()
    pupil_state = (pupils_by_state/pupils_by_state.sum()).to_dict()
    air_source=pin(wl.FISCAL/"air_pollution_2026_09_28/air_items.py",wl)
    air_ast=ast.parse(air_source.read_text())
    arms=next(node.value for node in air_ast.body if isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=="ARMS" for t in node.targets))
    local_fraction=ast.literal_eval(next(v for k,v in zip(arms.keys,arms.values) if isinstance(k,ast.Constant) and k.value=="L"))[1]
    keys = {
        "fear_avoidance": (crimekey, "crime victim risk within group states"),
        "private_security": (crimekey, "crime victim risk within group states; signed net may be a benefit"),
        "school_disruption": (pupils, "ages 5-17 in group states; school type unavailable"),
        "pm25_consumption": (place_key, "35% local group-state resident exposure, 65% national residents; assumed dispersion"),
        "road_crash_externality": (d.metro_worker.to_numpy(float), "state group vehicle-minutes by urban area, receiving metro workers; driving proxy"),
        "restaurant_variety_market_size": (consumer, "SPM resources within group states, consumption proxy"),
        "formal_volunteering_outside_group": (place_key, "all other residents nationally; beneficiary location unobserved"),
        "total_consumer_scale": (consumer, "national SPM resources, consumption proxy"),
        "total_trade_travel_fdi": (consumer, "national SPM resources, consumption proxy"),
    }
    existing = {"victims": "crime_victims", "property_crime": "property_crime",
                "unreimbursed_care": "unreimbursed_care", "congestion": "congestion"}
    arrays, table, values = {}, [], {}
    dd = weighted_frame(d,weights)
    for row in primary["rows"]:
        item = row["item"]
        amount = {L: -(row[f"union_{L}_bn"] + (row[f"added_{L}_bn"] if population == "lineage" else 0))
                  for L in ("low", "high")}
        amount["central"] = (amount["low"] + amount["high"]) / 2
        arrs = {}
        if item in existing:
            original = ch[existing[item]]
            for L in wl.LEVELS:
                # Congestion can have gains and losses: preserve its state sign
                # profile while scaling to the live end's social amount.
                old = original["central"]
                den = total(old, weights)
                require(f"social_{item}_seed", den != 0)
                arrs[L] = old * amount[L] / den
            key_name = f"live total on existing {existing[item]} incidence"
        elif item == "housing_gain":
            # Retain gross rent transfers, scale their net to each published
            # housing arm. Do not allocate a positive net only to landlords.
            key_name = "gross renter/landlord arrays, live central metro-local at low; national-uniform at high"
            for L in ("low", "high"):
                suffix = "" if L == "low" else "_national_uniform"
                x = ch["renters" + suffix]["central"] + ch["landlords" + suffix]["central"]
                arrs[L] = x * amount[L] / total(x, weights)
            arrs["central"] = (arrs["low"] + arrs["high"]) / 2
        elif item == "scale_net_earnings":
            key_name = "earnings by scale-lane metro states plus induced receipts by financing rule"
            private_share = meta["scale"]["private_share"]
            for L in wl.LEVELS:
                fiscal_key = ctx["tax_fed"] + ctx["tax_sl"] if rule == "a" else ctx["programme_receipts"] if rule == "c" else ones
                arrs[L] = wl.alloc_states(dd, earn, {s: amount[L] * private_share * v for s, v in meta["scale"]["state_share"].items()},
                                             notes={}) + wl.alloc(dd, fiscal_key, amount[L] * (1-private_share))
        elif item in keys:
            key, key_name = keys[item]
            for L in wl.LEVELS:
                if item == "pm25_consumption":
                    arrs[L] = wl.alloc_states(dd,key,{s:amount[L]*local_fraction*v for s,v in state_share.items()},notes={}) + wl.alloc(dd,key,amount[L]*(1-local_fraction))
                elif item in ("formal_volunteering_outside_group","total_consumer_scale","total_trade_travel_fdi"):
                    arrs[L] = wl.alloc(dd,key,amount[L])
                else:
                    shares = drive_state if item == "road_crash_externality" else pupil_state if item == "school_disruption" else state_share
                    arrs[L] = wl.alloc_states(dd, key, {s: amount[L] * v for s, v in shares.items()}, notes={})
        else:
            raise RuntimeError(f"[BLOCKED] adopted social channel has no allocation/exclusion declaration: {item}")
        arrays[item], values[item] = arrs, amount
        for L in wl.LEVELS:
            check_total(f"social_{population}_{rule}_{item}_{L}", arrs[L], weights, amount[L])
        table.append(dict(item=item, status="allocated", excluded_reason="", population=population,
                          financing=rule, key=key_name, **{f"{L}_bn": amount[L] for L in wl.LEVELS}))
    require("social_coverage_unique_complete", len(arrays) == len(primary["rows"]) and len(set(arrays)) == len(arrays))
    adopted={r["item"] for r in data["social_items_in_the_social_rows"]["items"]}
    require("adopted_declaration_covered",adopted<=set(arrays),missing=sorted(adopted-set(arrays)))
    # The source serializes individual union rows at six decimals but stores
    # their aggregate separately. Carry its sub-$1,000 rounding difference as an
    # explicit row rather than relax a closure tolerance.
    rounding={}
    for L in ("low","high"):
        expected=-(primary["union_social_bn"][L]+(primary["added_social_bn"][L] if population=="lineage" else 0))
        rounding[L]=expected-sum(values[k][L] for k in values)
        require(f"social_source_rounding_{L}",abs(rounding[L])<=1e-6+1e-12,rounding_bn=rounding[L])
    rounding["central"]=(rounding["low"]+rounding["high"])/2
    arrays["source_rounding"]={L:wl.alloc(dd,np.ones(len(d)),rounding[L]) for L in wl.LEVELS}
    values["source_rounding"]=rounding
    table.append(dict(item="source_rounding",status="allocated",excluded_reason="",population=population,
                      financing=rule,key="national persons; explicit serialized source-row rounding",**{f"{L}_bn":rounding[L] for L in wl.LEVELS}))
    for L in ("low","high"):
        check_total(f"social_primary_{L}",sum(arrays[k][L] for k in arrays),weights,
                    -(primary["union_social_bn"][L]+(primary["added_social_bn"][L] if population=="lineage" else 0)))
    # Mobility remains beside the published fiscal-plus-social total; retain a
    # separate supplemental view, never silently add it to this channel set.
    return arrays, values, pd.DataFrame(table)


def landlord_split(wl, d, weights, landlords):
    p = pin(wl.FISCAL / "housing_transfer_2026_09_23/derived/inputs_rhfs.csv", wl)
    ownership = pd.read_csv(p)
    individual = float(ownership.loc[ownership.OWNENT.eq(1), "units_share_reported"].iloc[0])
    corporate = float(ownership.loc[ownership.OWNENT.isin([6, 7]), "units_share_reported"].sum())
    ambiguous = 1 - individual - corporate
    require("owner_type_shares", min(individual, corporate, ambiguous) >= 0 and abs(individual+corporate+ambiguous-1) < 1e-12)
    # LLC/LP/trust/nonprofit/unreported cannot be identified as corporation or
    # individual from OWNENT alone. Report it and bracket the unresolved part.
    dd = weighted_frame(d,weights)
    all_gain = total(landlords, weights)
    capital_key = np.maximum(d.capital.to_numpy(float), 0)
    central = individual * landlords + wl.alloc(dd, capital_key, all_gain * (corporate + ambiguous))
    broad_individual = (individual + ambiguous) * landlords + wl.alloc(dd, capital_key, all_gain * corporate)
    check_total("owner_type_rent_conserved", central, weights, all_gain)
    check_total("owner_type_rent_ambiguous_arm_conserved", broad_individual, weights, all_gain)
    table = ownership.assign(assignment=np.where(ownership.OWNENT.eq(1), "individual landlord",
                              np.where(ownership.OWNENT.isin([6, 7]), "corporate/REIT capital income", "unresolved entity")))
    return central, broad_individual, table, dict(individual=individual, corporate_reit=corporate,
                                                 unresolved=ambiguous, proxy="reported rental-unit shares proxy rent shares")


def summary_row(d, weights, x, **tags):
    other = d.other.to_numpy()
    w, a = weights[other], x[other]
    return dict(**tags, persons_m=float(w.sum()/1e6), total_bn=total(a, w),
                winners_share=float(w[a > 0].sum()/w.sum()), losers_share=float(w[a < 0].sum()/w.sum()),
                mean_usd=float(np.dot(a,w)/w.sum()))


def cut_rows(d, weights, x, tags, cuts):
    rows = []
    other = d.other.to_numpy()
    # These person vectors are identical for every demographic cut. Repeating
    # boolean slices, products and the national dot product dominated profiling.
    w,a=weights[other],x[other]
    dollars=w*a
    winner_weights=w*(a>0)
    loser_weights=w*(a<0)
    expected_total=total(a,w)
    for cut in cuts:
        cache_key=(id(d),id(weights),cut)
        if cache_key not in CUT_CACHE:
            codes,groups=pd.factorize(d.loc[other,cut],sort=True)
            people=np.bincount(codes,weights=w,minlength=len(groups))
            resources=np.bincount(codes,weights=w*d.resources_pc.to_numpy()[other],minlength=len(groups))
            CUT_CACHE[cache_key]=(codes,groups,people,resources)
        codes,groups,people,resources=CUT_CACHE[cache_key]
        bn=np.bincount(codes,weights=dollars,minlength=len(groups))/1e9
        wins=np.bincount(codes,weights=winner_weights,minlength=len(groups))
        loses=np.bincount(codes,weights=loser_weights,minlength=len(groups))
        for i,group in enumerate(groups):
            if people[i]<=0:
                continue
            rows.append(dict(**tags,cut=cut,group=group,persons_m=float(people[i]/1e6),
                             total_bn=float(bn[i]),mean_usd=float(bn[i]*1e9/people[i]),
                             winners_share=float(wins[i]/people[i]),losers_share=float(loses[i]/people[i]),
                             pct_of_resources=float(100*bn[i]*1e9/resources[i]) if resources[i] else np.nan))
        require(f"cut_closure_{cut}",abs(bn.sum()-expected_total)<1e-9)
    return rows


def replicate_weights(d, B, chunk_size=10000):
    names = [f"pwwgt{i}" for i in range(1, 161)]
    wanted = pd.MultiIndex.from_frame(d[["PH_SEQ", "PPPOS"]])
    require("replicate_wanted_unique",wanted.is_unique)
    # Preserve the original person-major layout and the exact input order;
    # avoid holding the full CSV parser, source frame and joined copy together.
    joined=np.empty((len(d),160),dtype=float)
    covered=np.zeros(len(d),dtype=np.int32)
    seen=set()
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        for number,r in enumerate(pd.read_csv(z.open("asec_csv_repwgt_2025.csv"),
                usecols=["h_seq", "PPPOS", *names],chunksize=chunk_size)):
            keys=list(zip(r.h_seq.to_numpy(),r.PPPOS.to_numpy()))
            unique=set(keys)
            require(f"replicate_source_unique_{number}",len(unique)==len(keys) and not seen.intersection(unique))
            seen.update(unique)
            index=pd.MultiIndex.from_frame(r[["h_seq","PPPOS"]])
            at=wanted.get_indexer(index)
            keep=at>=0
            joined[at[keep],:]=r.loc[keep,names].to_numpy(float)
            covered[at[keep]]+=1
    require("replicate_person_join",bool(np.all(covered==1)))
    return joined.T


def run(namespace, B, d, I, ch, totals, meta, fin, ctx, nets, pnets):
    wl = types.SimpleNamespace(**namespace)
    GATES.clear()
    PINS.clear()
    CUT_CACHE.clear()
    out = wl.DERIVED
    w = d.pw.to_numpy().copy()
    other = d.other.to_numpy()
    # Compare actual arrays to the committed live control, not rounded numbers
    # in the review or a newly generated summary.
    baseline = pd.read_csv(__import__("io").BytesIO(wl.git_show(
        "infra/immigration-fiscal/winners_losers_2026_09_24/derived/oct14/net_shares.csv", "2204a2bc")))
    controls = []
    for rule in ("a", "b"):
        for unit, arrays in (("person", nets), ("spm_unit_pooled", pnets)):
            row = summary_row(d,w,arrays[(f"net_social_{rule}","central")], financing=rule, sharing=unit)
            target = baseline[(baseline.net == f"net_social_{rule}") & (baseline["stack"] == "central") & (baseline.unit == unit)].iloc[0]
            require(f"hybrid_positive_control_{rule}_{unit}", abs(row["winners_share"]-target.winners_share)<5e-11
                    and abs(row["total_bn"]-target.total_bn)<5e-8,
                    winners_share=row["winners_share"], total_bn=row["total_bn"])
            controls.append(row)
    wl.write_csv(pd.DataFrame(controls), "p7_positive_control.csv")
    extra_fields(d,B)
    payload_path = pin(wl.FISCAL / wl.CASE["lane"] / "derived/corrections.json", wl)
    payload = json.loads(payload_path.read_text())
    lineage = payload["meta"]["lineage"]
    trust_path = pin_generated(out / "p7_trust_inputs.json", "generated:p7_trust_inputs.json",wl)
    exported=json.loads(trust_path.read_text())
    trust = exported["rows"]
    programmes=exported["programmes"]
    trust["central"] = {k: (trust["low"][k]+trust["high"][k])/2 for k in trust["low"]}
    # The authoritative model paths and microdata are pinned, not downloads or
    # hand-entered primary-table values.
    for name in ["corrections_cash.json", "summary.json"]:
        pin(wl.FISCAL / wl.CASE["lane"] / "derived" / name, wl)
    pin(B.PATHS["cps"],wl)
    adjusted, payer_cells = lineage_payers(d,w,lineage,wl)
    wl.write_csv(payer_cells,"p7_payer_cells.csv")
    from p7_cohorts import cohort_keys
    member_weights, member_info = wl.lineage_group_weights(B,d)
    union_weights, _ = wl.row4_group_weights(B,d)
    cohort = cohort_keys(d,wl,trust["central"],group_weights=union_weights)
    for path in cohort["pins"]:
        pin(path,wl)
    from p7_credits import crossing_credit_arrays
    credits = crossing_credit_arrays(d)
    credit_meta = credits["metadata"]
    for path in credit_meta["source_paths"]:
        pin(path,wl)
    # Source calibrated vectors use the same other-resident survey weights.
    check_total("forward_credit_union",credits["forward"],w,credit_meta["forward"]["total_bn"])
    require("forward_credit_carriers_are_nonmembers", not np.any(credits["forward"][~other]))
    # Apply the case's existing G3+ per-member extrapolation separately to the
    # recovered gross forward filer vector. White-priced added people take zero,
    # as in item 5b. Filer location remains a labelled surrogate assignment.
    added_credit_factor=lineage["members"]["g3plus"]/lineage["counts"]["identified_g3plus"]
    added_forward_credit_bn=added_credit_factor*credit_meta["forward_g3plus"]["total_bn"]
    summaries, cuts, coverage, channels_rows, sharing_recon = [],[],[],[],[]
    arrays_for_se = []
    for pair in ("state3|edu_nativity","edu_nativity|tenure","state3|tenure","decile|tenure"):
        a,b=pair.split("|")
        d[pair]=d[a].astype(str)+"|"+d[b].astype(str)
    cutnames = wl.CUT_COLUMNS+["state3|edu_nativity","edu_nativity|tenure","state3|tenure","decile|tenure"]
    member_resources = d.PTOTVAL.to_numpy(float) - d.FEDTAX_AC.to_numpy(float) - d.STATETAX_A.to_numpy(float) - d.FICA.to_numpy(float)
    member_resources += sum(d[x].to_numpy(float) for x in ["SPM_SNAPSUB","SPM_SCHLUNCH","SPM_WICVAL","SPM_ENGVAL","SPM_CAPHOUSESUB"]) / d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    member_resources = np.where(d.target.to_numpy(),member_resources,0)
    owner_meta = {}
    grid_rows = []
    cached = {}
    programme_key_rows=[]
    reweighted_channels = {k:{L:transport(v[L],w,adjusted,d) for L in wl.LEVELS} for k,v in ch.items()}
    cohorts = {"identified_union":cohort,"lineage":cohort_keys(weighted_frame(d,adjusted),wl,trust["central"],group_weights=member_weights)}

    def context_for(population, rule):
        key = (population,rule)
        if key in cached:
            return cached[key]
        weights = w if population == "identified_union" else adjusted
        dd = weighted_frame(d,weights)
        channels = reweighted_channels if population == "lineage" else ch
        pool = pooler(d,weights)
        kf, ks = (ctx["tax_fed"],ctx["tax_sl"]) if rule == "a" else (np.ones(len(d)),np.ones(len(d)))
        if rule == "c":
            low,rlow=responding_programme_key(dd,weights,programmes["low"])
            high,rhigh=responding_programme_key(dd,weights,programmes["high"])
            kf=ks=(low+high)/2
            programme_key_rows.extend(dict(population=population,level=L,**r) for L,rs in (("low",rlow),("high",rhigh)) for r in rs)
        social_ctx=dict(ctx,programme_receipts=kf)
        soc, social_totals, cov = social_channels(wl,dd,I,channels,meta,weights,population,rule,social_ctx)
        coverage.extend(cov.to_dict("records"))
        pkey, property_missing = property_key(d,I,B,weights)
        gross_owner = {}
        for L in ("low","high"):
            suffix = "" if L == "low" else "_national_uniform"
            rent = channels["renters"+suffix]["central"]
            land = channels["landlords"+suffix]["central"]
            scale = total(soc["housing_gain"][L],weights)/total(rent+land,weights)
            gross_owner[L] = land*scale
        gross_owner["central"] = (gross_owner["low"]+gross_owner["high"])/2
        owners, owner_broad = {},{}
        for L in wl.LEVELS:
            owners[L], owner_broad[L], owner_table, ownmeta = landlord_split(wl,d,weights,gross_owner[L])
        owner_meta[population] = dict(ownmeta, property_empty_cell_transfers=property_missing)
        owner_table["population"] = population
        wl.write_csv(owner_table,f"p7_owner_types_{population}.csv")
        statew = {}
        for L in wl.LEVELS:
            statew[L], swtable = state_wages(dd,weights,channels["wages"][L],wl,
                                            group_weights=union_weights if population=="identified_union" else member_weights)
            swtable["level"],swtable["population"] = L,population
            if rule == "a":
                channels_rows.extend(swtable.to_dict("records"))
        credit = credits["forward"].copy()
        if population == "lineage":
            # Fixed measured union credit is reallocated across surviving filers
            # proportional to the source per-filer amount after payer thinning.
            credit+=added_credit_factor*credits["forward_g3plus"]
            credit *= (credit_meta["forward"]["total_bn"]+added_forward_credit_bn) / total(credit,weights)
        social_sum = {L:sum(soc[k][L] for k in soc) for L in wl.LEVELS}
        result = dict(weights=weights,dd=dd,ch=channels,social=soc, social_sum=social_sum,pool=pool,cohort=cohorts[population],
                      kf=kf,ks=ks,property_key=pkey,statew=statew,credit=credit,
                      owner_gain=owners,owner_gain_broad=owner_broad, gross_owner=gross_owner)
        cached[key] = result
        return result

    def net_of(cx,frame,L,channel_set,credit=False,wage_geo=False,cap_geo=False,owner_type=False):
        weights,dd = cx["weights"],cx["dd"]
        f = meta["fiscal"][L]
        # All cases price the live lineage headline. The identified-union payer
        # frame is a population sensitivity, not a new union-only fiscal case.
        today_cost = f["federal_today"]
        future = f["future"]
        keyf = cx["kf"]
        if frame == "hybrid":
            fedarr = -wl.alloc(dd,keyf,today_cost)
        elif frame == "stationary":
            fedarr = -wl.alloc(dd,keyf,today_cost+future)
            future = 0.0
        elif frame.startswith("cohort"):
            # First take the complete trust block out of today's cash split.
            # Current payroll surplus must not stay on today's taxpayer key.
            tr = trust[L]
            cash_block = tr["cash_benefits_bn"]-tr["payroll_bn"]
            debt_of_trust = meta["deficit"]["share"]*cash_block
            remainder_today = today_cost-(1-meta["deficit"]["share"])*cash_block
            remainder_borrowing = f["future_borrowing"]-debt_of_trust
            # Projected keys are recomputed for each recipient frame's weights.
            ck = cx["cohort"]
            trust_key = np.asarray(ck["keys"]["trust"],float)
            debt_key = np.asarray(ck["keys"]["borrowing30" if frame=="cohort30" else "borrowing10"],float)
            trust_share = ck["living_shares"]["trust"]
            debt_share = ck["living_shares"]["borrowing30" if frame=="cohort30" else "borrowing10"]
            fedarr = -wl.alloc(dd,keyf,remainder_today) - wl.alloc(dd,trust_key,tr["trust_cost_bn"]*trust_share) \
                     - wl.alloc(dd,debt_key,remainder_borrowing*debt_share)
            future = tr["trust_cost_bn"]*(1-trust_share)+remainder_borrowing*(1-debt_share)
        else:
            raise RuntimeError(f"unknown financing frame {frame}")
        keysl = cx["property_key"] if cap_geo else cx["ks"]
        state_share = {wl.POSTAL[k]:v for k,v in meta["group_state_share"].items()}
        slarr = -wl.alloc_states(dd,keysl,{s:f["state_local"]*v for s,v in state_share.items()},notes={})
        if cap_geo:
            require("capitalization_renters_zero", not np.any(slarr[d.H_TENURE.ne(1).to_numpy()]))
        wages = cx["statew"][L] if wage_geo else cx["ch"]["wages"][L]
        account = fedarr+slarr+wages+cx["ch"]["displaced_beneficiaries"][L]
        head = -(fin[wl.CASE["model"]]["ends"]["low" if L=="low" else "high"]["cost_bn"] if L!="central" else
                 (fin[wl.CASE["model"]]["ends"]["low"]["cost_bn"]+fin[wl.CASE["model"]]["ends"]["high"]["cost_bn"])/2)
        # Old f uses debt CSV rounded to 1e-6; correct its visible residual on
        # federal key, once, so new computations close to exact case totals.
        rounding = head-(total(account,weights)-future)
        require("frozen_rounding_small",abs(rounding)<1e-3,rounding_bn=rounding)
        account += wl.alloc(dd,keyf,rounding)
        check_total("account_exact_case_closure",account,weights,head+future)
        if channel_set=="legacy":
            social = sum(cx["ch"][p][L] for p in wl.SOCIAL)
        else:
            social = cx["social_sum"][L]
        x = account+social
        if credit:
            x += cx["credit"]
        if owner_type:
            # Replace each gross rent receiver, holding renters and the national
            # housing net fixed. Central housing blends two geographic readings.
            if channel_set == "legacy":
                old = cx["ch"]["landlords"][L]
                central,broad,_,_=landlord_split(wl,d,weights,old)
                replacement = (broad if owner_type == "broad" else central)-old
            else:
                replacement = cx["owner_gain_broad" if owner_type == "broad" else "owner_gain"][L]-cx["gross_owner"][L]
            x += replacement
            check_total("owner_type_net_total_conserved",replacement,weights,0.0)
        return x,wages,future,account

    def record(population,rule,arm,frame,channel_set,credit=False,wage_geo=False,cap_geo=False,owner_type=False,all_sharing=True):
        cx=context_for(population,rule)
        weights=cx["weights"]
        for L in wl.LEVELS:
            x,wages,future,account=net_of(cx,frame,L,channel_set,credit,wage_geo,cap_geo,owner_type)
            sharing={"person":x,"pooled":cx["pool"](x)}
            if all_sharing:
                shared_nonwage=cx["pool"](x-wages)
                sharing.update({f"retains_{s}":shared_nonwage+unequal_wages(d,wages,weights,s) for s in (.5,.8)})
                # Money resources contributed by actual members, before their
                # removal, are a household-boundary transfer, not a new social
                # benefit. All group-only units remain in the conservation gate.
                mw=union_weights if population=="identified_union" else member_weights
                combined_weights=np.where(d.target.to_numpy(),mw,weights)
                both=d.target.to_numpy()|other
                combined=x+member_resources
                mixed=pooler(d,combined_weights,both)(combined)
                check_total("mixed_unit_total_conserved",mixed,combined_weights,total(combined,combined_weights))
                sharing["mixed_unit"]=np.where(other,mixed,0)
                sharing_recon.append(dict(population=population,financing=rule,arm=arm,frame=frame,level=L,
                     other_before_bn=total(x,weights),other_after_bn=total(sharing["mixed_unit"],weights),
                     member_resource_bn=total(member_resources,mw),group_after_bn=total(np.where(d.target,mixed,0),mw)))
            for share,a in sharing.items():
                if share!="mixed_unit":
                    check_total(f"sharing_{share}",a,weights,total(x,weights))
                tags=dict(population=population,financing=rule,arm=arm,frame=frame,channel_set=channel_set,
                          level=L,sharing=share,future_bn=float(-future))
                summaries.append(summary_row(d,weights,a,**tags))
                cuts.append(pd.DataFrame(cut_rows(d,weights,a,tags,cutnames)))
                # Replicate prevalence needs signs, not another full priced
                # float array. Both fiscal ends and central values need SEs.
                arrays_for_se.append((len(summaries)-1,population,a>0))
            if arm=="complete_social":
                for name,arrs in cx["social"].items():
                    a=arrs[L]
                    coverage_row=dict(population=population,financing=rule,frame=frame,level=L,channel=name,
                                      total_bn=total(a,weights),receivers_m=float(weights[other & (a!=0)].sum()/1e6))
                    coverage_row["per_receiver_usd"]=coverage_row["total_bn"]*1000/coverage_row["receivers_m"] if coverage_row["receivers_m"] else 0
                    social_channel_rows.append(coverage_row)
            if channel_set=="complete":
                landlord=cx["owner_gain_broad" if owner_type=="broad" else "owner_gain"][L] if owner_type else cx["gross_owner"][L]
                pieces={"fiscal_today":account-wages,
                        "wages_positive":np.maximum(wages,0),"wages_negative":np.minimum(wages,0),
                        "renters":cx["social"]["housing_gain"][L]-cx["gross_owner"][L],
                        "landlords":landlord}
                pieces.update({k:v[L] for k,v in cx["social"].items() if k!="housing_gain"})
                if credit:
                    pieces["crossing_credits"]=cx["credit"]
                check_total("complete_channel_table_closure",sum(pieces.values()),weights,total(x,weights))
                for name,a in pieces.items():
                    receivers=float(weights[other & (a!=0)].sum()/1e6)
                    channel_table_rows.append(dict(population=population,financing=rule,arm=arm,frame=frame,level=L,
                        channel=name,total_bn=total(a,weights),receivers_m=receivers,
                        per_receiver_usd=total(a,weights)*1000/receivers if receivers else 0))
                channel_table_rows.append(dict(population=population,financing=rule,arm=arm,frame=frame,level=L,
                    channel="future_cohorts",total_bn=-future,receivers_m=np.nan,per_receiver_usd=np.nan))

    social_channel_rows=[]
    channel_table_rows=[]
    # One fix from live central; matched frames differ in exactly the named arm.
    for rule in ("a","b","c"):
        for population in ("identified_union","lineage"):
            for frame in ("hybrid","stationary","cohort30","cohort10"):
                record(population,rule,"financing_only",frame,"legacy")
            record(population,rule,"complete_social","stationary","complete")
            record(population,rule,"social_coverage_only","hybrid","complete")
            record(population,rule,"crossing_credit_only","hybrid","legacy",credit=True)
            record(population,rule,"state_wages_only","hybrid","legacy",wage_geo=True)
            record(population,rule,"capitalization_only","hybrid","legacy",cap_geo=True)
            record(population,rule,"owner_type_only","hybrid","legacy",owner_type=True)
            record(population,rule,"owner_type_broad_only","hybrid","legacy",owner_type="broad")
        record("lineage",rule,"payer_pool_only","hybrid","legacy")
        record("lineage",rule,"recommended","stationary","complete",credit=True)
        record("lineage",rule,"recommended_state_wages","stationary","complete",credit=True,wage_geo=True)
        record("lineage",rule,"recommended_capitalization","stationary","complete",credit=True,cap_geo=True)
        for frame in ("stationary","cohort30","cohort10"):
            record("lineage",rule,"stack",frame,"complete",credit=True,wage_geo=True,cap_geo=True,owner_type=True)

    # Enumerated share extrema are a separate objective from dollar extrema.
    # Grid: 2 fiscal ends × 2 wage incidences × 2 capitalization arms ×
    # 3 coherent housing levels. Nonhousing social follows the same case end
    # at each item's central model setting; exact credit rule is fixed.
    for rule in ("a","b","c"):
        cx=context_for("lineage",rule)
        for L,wage_geo,cap_geo,housing in itertools.product(("low","high"),(False,True),(False,True),wl.LEVELS):
            x,wages,future,_=net_of(cx,"stationary",L,"complete",True,wage_geo,cap_geo,False)
            old=cx["social"]["housing_gain"][L]
            h=cx["ch"]["renters"][housing]+cx["ch"]["landlords"][housing]
            x=x-old+h
            for sharing,a in (("person",x),("pooled",cx["pool"](x))):
                tags=dict(financing=rule,level=L,wage_geography="state" if wage_geo else "national",
                          capitalization=cap_geo,housing_level=housing,sharing=sharing)
                grid_rows.append(summary_row(d,cx["weights"],a,**tags))
    grid=pd.DataFrame(grid_rows)
    extrema=[]
    for (rule,sharing),g in grid.groupby(["financing","sharing"],sort=True):
        for label,col,fn in (("share_minimum","winners_share","idxmin"),("share_maximum","winners_share","idxmax"),
                             ("dollar_minimum","total_bn","idxmin"),("dollar_maximum","total_bn","idxmax")):
            r=g.loc[getattr(g[col],fn)()].to_dict()
            extrema.append(dict(extreme=label,**r))
    # Conditional prevalence SE: fixed priced amounts and assignments, varied
    # official survey weights. This excludes model, key and pooling uncertainty.
    reps=replicate_weights(d,B)
    lineage_reps=reps.copy()
    third=d.PRCITSHP.isin([1,2,3]).to_numpy() & d.PEMNTVTY.isin(wl.US_AREAS).to_numpy() & d.PEFNTVTY.isin(wl.US_AREAS).to_numpy() & other
    bands=np.minimum(d.A_AGE.to_numpy()//5,len(payer_cells)-1)
    for b,row in payer_cells.iterrows():
        mask=third & (bands==b)
        den=lineage_reps[:,mask].sum(axis=1)
        require(f"replicate_lineage_mass_{b}",bool(np.all(den>row.removed)))
        lineage_reps[:,mask]*=(1-row.removed/den)[:,None]
    # Population denominators do not depend on the scenario's winner mask.
    # Compute them twice, rather than materializing a large slice 1305 times.
    replicate_denominators={"identified_union":reps[:,other].sum(axis=1),
                            "lineage":lineage_reps[:,other].sum(axis=1)}
    for index,population,ahead in arrays_for_se:
        W=lineage_reps if population=="lineage" else reps
        ratios=W[:,other & ahead].sum(axis=1)/replicate_denominators[population]
        point=summaries[index]["winners_share"]
        summaries[index]["winners_share_conditional_se"]=float(np.sqrt(4/160*np.square(ratios-point).sum()))
    # Every one-fix delta is matched by population, level and sharing to legacy
    # hybrid; dollar bar describes incidence reassignment, never headline drift.
    results=pd.DataFrame(summaries)
    for population in ("identified_union","lineage"):
        for arm in ("financing_only","complete_social","social_coverage_only","crossing_credit_only",
                    "state_wages_only","capitalization_only","owner_type_only","owner_type_broad_only"):
            cells=results[(results.population==population)&(results.arm==arm)]
            require(f"scenario_population_coverage_{population}_{arm}",
                    set(zip(cells.financing,cells.level,cells.sharing))==
                    set(itertools.product(("a","b","c"),wl.LEVELS,
                        ("person","pooled","retains_0.5","retains_0.8","mixed_unit"))))
    matched=results[(results.arm=="financing_only") & (results.frame=="hybrid")]
    results=results.merge(matched[["population","financing","level","sharing","total_bn","winners_share"]].rename(columns={
        "total_bn":"payer_pool_hybrid_total_bn","winners_share":"payer_pool_hybrid_winners_share"}),
        on=["population","financing","level","sharing"],validate="many_to_one")
    results["within_payer_pool_delta_today_bn"]=results.total_bn-results.payer_pool_hybrid_total_bn
    results["within_payer_pool_delta_ahead_pp"]=100*(results.winners_share-results.payer_pool_hybrid_winners_share)
    ref=results[(results.arm=="financing_only") & (results.frame=="hybrid") & (results.population=="identified_union")]
    results=results.merge(ref[["financing","level","sharing","total_bn","winners_share","future_bn"]].rename(columns={
        "total_bn":"hybrid_total_bn","winners_share":"hybrid_winners_share","future_bn":"hybrid_future_bn"}),
        on=["financing","level","sharing"],validate="many_to_one")
    results["delta_today_bn"]=results.total_bn-results.hybrid_total_bn
    results["delta_ahead_pp"]=100*(results.winners_share-results.hybrid_winners_share)
    results["over_5bn_incidence_bar"]=results.delta_today_bn.abs()>=5
    results["all_cohorts_resource_delta_bn"]=results.delta_today_bn+results.future_bn-results.hybrid_future_bn
    results["frozen_main_case_file_change_bn"]=0.0
    source_doc=json.loads((HERE/"inputs/social_oct14.json").read_text())
    exclusions=pd.DataFrame([
        dict(item="source never-added rows",status="excluded",reason=source_doc["social_items_in_the_social_rows"]["never_added"]),
        dict(item="mobility",status="supplemental",reason="beside published total; retained in legacy positive control, excluded from complete adopted set"),
        dict(item="preferences",status="proposed",reason="attribution arm, not adopted in the published social set"),
        dict(item="consumer prices and care earnings",status="excluded",reason="overlap wage/private production channels"),
        dict(item="debt legacy interest",status="excluded",reason="historical capitalization object, not new annual borrowing")])
    for table,name in [(results,"p7_net_shares.csv"),(pd.concat(cuts,ignore_index=True),"p7_cuts.csv"),
                       (pd.DataFrame(coverage),"p7_channel_coverage.csv"),(pd.DataFrame(channels_rows),"p7_state_wage_cells.csv"),
                       (pd.DataFrame(social_channel_rows),"p7_social_channel_table.csv"),
                       (pd.DataFrame(channel_table_rows),"p7_channel_table.csv"),
                       (pd.DataFrame(sharing_recon),"p7_mixed_reconciliation.csv"),(grid,"p7_enumerated_grid.csv"),
                       (exclusions,"p7_excluded_channels.csv"),
                       (pd.DataFrame(programme_key_rows),"p7_programme_receipt_keys.csv"),
                       (pd.DataFrame(extrema),"p7_grid_extrema.csv")]:
        wl.write_csv(table,name)
    # Current memo tables are all available on the live run. A specific map
    # prevents the docs worker substituting the September-24 retained record.
    mappings=[("§2 all channels","p7_channel_table.csv","complete_social/recommended/stack; select population,financing,frame,level; gross wages/rents, fiscal today/future, every social row"),
              ("§2 social detail","p7_social_channel_table.csv","complete_social; select financing/frame/level/population"),
              ("§2 prior inside/beside channel table","winners_losers_table.csv","live oct14 retained hybrid record; current channel set is p7_channel_table.csv"),
              ("§3 cuts","p7_cuts.csv","state3,edu_nativity,tenure,age3,industry5,race5,sex; select full model tags"),
              ("§3 quintiles and income","p7_cuts.csv","quintile or decile; pct_of_resources"),
              ("§3 two-way winning cells","p7_cuts.csv","state3|edu_nativity,edu_nativity|tenure,state3|tenure,decile|tenure"),
              ("§4 sensitivities","p7_net_shares.csv","one arm at a time plus stack; exact financing/sharing tags"),
              ("§4 account-only/proposed/national-state-local/alternate-housing/crime variants","net_shares.csv","live oct14 legacy hybrid variants; exact net,stack,unit; retained comparison, not corrected verdict"),
              ("§4 enumerated extrema","p7_grid_extrema.csv","share extrema and dollar extrema separately"),
              ("§4 pooling moves","pooling_moves.csv","live oct14 legacy hybrid calculation record"),
              ("§5 group resources","group_frame.csv","live 42.75M; p7_mixed_reconciliation.csv for boundary transfer"),
              ("§6 excluded roles","p7_excluded_channels.csv","source exclusions and supplemental/proposed channels; role_table.csv preserves source roles"),
              ("§1 financing","p7_trust_inputs.json","exact set/cash trust-fund amounts; p7_net_shares future_bn")]
    wl.write_csv(pd.DataFrame(mappings,columns=["memo_table","file","selection"]),"p7_table_map.csv")
    credit_meta={k:v for k,v in credit_meta.items() if k not in ("wall_seconds","peak_memory_bytes","source_paths")}
    info=dict(case="oct14",recommended="stationary; complete adopted social set; corrected lineage payer pool; state wage and capitalization arms beside",
              channel_set="all 15 lineage_social_rows rows; mobility supplemental outside the adopted published total",
              source_frame="identified_union is an alternative payer pool for the live lineage case, not a 39.71M fiscal rerun",
              group_incidence_weights="audit row4 for identified union; payload age-band G3+ surrogate for the added lineage people; same weights feed state labor and cohort payout proxies",
              social_vintage="adopted v7 at c392d356; inputs/social_oct14.json; excludes concurrent unadopted peer source refresh",
              cohort={k:v for k,v in cohort.items() if k not in ("keys","component_keys","pins","years","profiles")},
              lineage_cohort_living_shares=cohorts["lineage"]["living_shares"],
              credits=credit_meta, added_descendant_forward_credit=dict(total_bn=added_forward_credit_bn,
                rule="[ASSUMPTION] item5b's added G3+-priced people per identified G3+ member on measured G3+ gross forward filer vector; white-priced added people zero"),
              mixed_resources="CPS personal cash income minus own taxes/FICA plus per-capita SPM noncash benefits; observed resources proxy, no removal behavioral response",
              owner_types=owner_meta,replicate_se="160 official SDR weights; conditional on fixed allocations, sharing assignments and model; not total estimation uncertainty",
              union_population=member_info["row4_members_m"],lineage_population=member_info["members_m"],
              instrument="LLM implementation; deterministic closure and signed, matched sensitivity arms are the verification evidence")
    (out/"p7_inputs.json").write_text(json.dumps(info,indent=1,default=float)+"\n")
    if "years" in cohort:
        wl.write_csv(pd.DataFrame(cohort["years"]),"p7_cohort_years.csv")
    if "profiles" in cohort:
        wl.write_csv(pd.DataFrame(cohort["profiles"]),"p7_cohort_profiles.csv")
    for path,digest in PINS.items():
        actual=out/"p7_trust_inputs.json" if path=="generated:p7_trust_inputs.json" else wl.ROOT/path
        require(f"final_source_pin_{path}",wl.file_sha(actual)==digest)
    (out/"p7_gates.json").write_text(json.dumps(GATES,indent=1,default=float)+"\n")
    manifest=HERE/"inputs/pins.json"
    if not manifest.exists():
        manifest.parent.mkdir(exist_ok=True)
        manifest.write_text(json.dumps(dict(sha256=PINS),indent=1)+"\n")
    # Clear the obsolete proposed status without rewriting the hybrid arrays.
    registry=pd.read_csv(out/"channels.csv")
    registry.loc[registry.id.eq("scale"),["status","in_net","note"]]=[
        "adopted","p7 complete social", "adopted 2026-09-28; live valued row in p7_channel_coverage.csv; hybrid retains historical channel set"]
    live_rows=pd.DataFrame(coverage)
    live_rows=live_rows[live_rows.population.eq("lineage")&live_rows.financing.eq("a")]
    scale=live_rows[live_rows.item.eq("scale_net_earnings")].iloc[0]
    registry.loc[registry.id.eq("scale"),["bn_low","bn_central","bn_high"]]=[scale.low_bn,scale.central_bn,scale.high_bn]
    registry.loc[registry.id.eq("scale"),"source_lane"]="inputs/social_oct14.json at c392d356; full lineage"
    new_rows=[]
    for r in live_rows.itertuples():
        if r.item=="scale_net_earnings":
            continue
        new_rows.append(dict(id=f"p7_social_{r.item}",label=r.item,bn_low=r.low_bn,bn_central=r.central_bn,bn_high=r.high_bn,
                            who=r.key,relation="beside",in_net="p7 complete social",counterfactual=wl.counterfactual(),
                            source_lane="inputs/social_oct14.json at c392d356; full lineage",ladder="",status="adopted",
                            date=wl.CASE["date"],note="fixed declared social set; low/high are case-end allocations, not uncertainty endpoints"))
    registry=registry[~registry.id.str.startswith("p7_social_")]
    registry=pd.concat([registry,pd.DataFrame(new_rows)],ignore_index=True)
    require("scale_registry_matches_allocated_recipient_sign",np.array_equal(
        registry.loc[registry.id.eq("scale"),["bn_low","bn_central","bn_high"]].iloc[0].to_numpy(float),
        np.array([scale.low_bn,scale.central_bn,scale.high_bn])))
    wl.write_csv(registry,"channels.csv")
    (out/"p7_gates.json").write_text(json.dumps(GATES,indent=1,default=float)+"\n")
    print(f"[P7] {len(results)} net rows; {sum(len(c) for c in cuts)} cut rows; {len(GATES)} gates passed",flush=True)
