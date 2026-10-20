"""F09: source-native social costs of an equal-count random average-resident group.

The average group removes the same fraction of every national person, source,
receiver and geographic cell. Ethnicity-specific offending, consumption, tenure,
schooling and exposure ratios do not transfer. All source assumptions and dollar
vintages remain. This conditional benchmark is not an observed removal effect.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ENDS = ("low", "high")


def require(condition, message):
    if not condition:
        raise ValueError("[BLOCKED] average social: " + message)


class Sources:
    """Read-only native formula loading, with every file we directly use pinned."""
    def __init__(self, root):
        self.root = Path(root)
        self.pins = {}

    def path(self, relative):
        path = self.root / relative
        require(path.exists(), "missing primary/staged input " + str(path))
        self.pins[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
        return path

    def table(self, relative):
        return pd.read_csv(self.path(relative))

    def document(self, relative):
        return json.loads(self.path(relative).read_text())

    def native(self, relative, *, stop_before_rows=False):
        sys.dont_write_bytecode = True
        path = self.path(relative)
        spec = importlib.util.spec_from_file_location("average_social_" + path.parent.name + "_" + path.stem, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        # The food producer writes at import. Execute its definitions before its
        # explicit output-row assembly; preserve original AST and source paths.
        if stop_before_rows:
            tree = ast.parse(path.read_text(), filename=str(path))
            body = []
            for node in tree.body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "rows" for t in node.targets):
                    break
                body.append(node)
            require(len(body) < len(tree.body), "food output boundary missing")
            exec(compile(ast.Module(body=body, type_ignores=[]), str(path), "exec"), module.__dict__)
        else:
            spec.loader.exec_module(module)
        return module


def crime_sources(src, share):
    sc = src.native("social_costs_unpriced_2026_09_28/items.py")
    p7 = src.native("social_costs_unpriced_2026_09_28/p7_crime.py")
    national = src.table("black_comparator_rough_2026_09_28/derived/victim_cost_by_offence.csv")
    national = national[national.arm.eq("national_all_offenders")].groupby("offence").n.sum()
    active = src.table("crime_victim_cost_2026_09_23/derived/mortality_detail.csv")
    active = active[active.footing.eq("mixed") & active.vsl_standard.eq("dot_uniform")
                    & active.real_discount_rate.eq(0) & active.missing_age_arm.eq("central")]
    units = {}
    for offence, rows in active.groupby("offence"):
        values = rows.unit_full.unique()
        require(len(values) == 1, "uniform mortality has multiple unit prices: " + offence)
        units[offence] = float(values[0])
    require(set(sc.OFFENCES).issubset(national.index) and set(sc.OFFENCES).issubset(units),
            "national incidence/active units missing an offence")
    count = {o: float(national[o]) * share * (1 - share) for o in sc.OFFENCES}
    victims = sum(count[o] * units[o] for o in sc.OFFENCES) / 1e9
    payer = src.document("social_costs_unpriced_2026_09_28/derived/security_inputs.json")["industries"]
    spending, _ = p7.security_spending(sc, payer, "central")
    security = p7.response(spending, share, 1 - share, share)
    wtp = 0.
    for o in sc.OFFENCES:
        unit = units[o]
        if o in ("Murder", "Rape/sexual assault", "Aggravated assault"):
            residual = max(0., sc.to2024(sc.WTP2000[o], 2000) - unit)
        elif o == "Robbery":
            residual = min(unit, max(0., sc.ARMED_SHARE * (sc.to2024(sc.WTP2000["Armed robbery"], 2000) - unit)))
        else:
            residual = 0.
        wtp += count[o] * residual / 1e9
    forward = security["residential_forward_bn"] + security["commercial_forward_bn"]
    fear = sc.PHI["central"] * max(0., wtp - forward)
    prop = src.table("crime_victim_cost_2026_09_23/derived/property_proxy.csv")
    property_cost = {}
    for end, price in (("low", "miller2021"), ("high", "mccollister2010")):
        rows = prop[prop.price_set.eq(price)]
        require(len(rows) > 0, "property source price " + price)
        property_cost[end] = float((rows.victimisations_2024 * rows.unit_victim_cost).sum()) / 1e9 * share * (1 - share)
    return dict(victims={e: victims for e in ENDS}, fear_avoidance={e: fear for e in ENDS},
                private_security={e: security["total_bn"] for e in ENDS}, property_crime=property_cost,
                school_disruption={e: 0. for e in ENDS})


def housing_source(src, share):
    h = src.native("housing_transfer_2026_09_23/arms.py")
    areas, _ = h.load_areas()
    # Same rent path/integral and foreign-owner assumption. Random membership
    # preserves every area's housing tenure and beneficial-owner distribution.
    for field in ("renter_rent", "renter_households", "owner_value"):
        total = areas["group_" + field] + areas["other_" + field]
        areas["group_" + field], areas["other_" + field] = total * share, total * (1 - share)
    areas["group_share"] = share
    h.TARGET = share * h.RESIDENTS  # native national_uniform reads this scalar
    foreign = h.OWN["central"]["foreign"]
    h.OWN["average"] = dict(group_of_other=share * (1 - foreign), group_of_group=share * (1 - foreign), foreign=foreign)
    amounts = {end: h.evaluate(areas, "long_run", "central", "A", geography, "average")["net_other_residents_welfare_bn"]
               for end, geography in (("low", "metro_local"), ("high", "national_uniform"))}
    for rel in ("housing_transfer_2026_09_23/derived/pums_puma_cells.csv",):
        src.path(rel)
    return {end: -float(amounts[end]) for end in ENDS}


def consumption_sources(src, share, people):
    c = src.native("consumer_scale_2026_09_28/price_items.py")
    ce = src.table("consumer_scale_2026_09_28/derived/ce_spending.csv").set_index("category")
    pp = ce.per_person_all_usd
    others = people * (1 - share)
    grocery = c.P["hw_beta"][1] * pp["food_home"] * others * -math.log1p(-share) / 1e9
    networks = sum(-c.P[k][1] * pp[cat] * people * share / 1e9 for cat, k in
                   (("electricity", "fixed_share_energy"), ("natural_gas", "fixed_share_energy"),
                    ("telephone", "fixed_share_telecom"), ("internet", "fixed_share_telecom"),
                    ("cable_satellite_tv", "fixed_share_telecom")))
    media = -pp["reading"] * others * ((1 - share) ** (-1 / (c.P["media_sigma"][1] - 1)) - 1) / 1e9
    food = src.native("disease_food_2026_09_28/price_items.py", stop_before_rows=True)
    # Random customers supply their population share of every cuisine/market;
    # no ethnic spending or consumption-segregation multiplier transfers.
    restaurant = food.scale(share, food.sig["central"], (1 - share) * food.E_722["central"]) / 1e9
    trade = src.native("trade_networks_2026_09_28/price_trade_networks.py")
    a = trade.ARMS["central"]
    info = trade.us_gain(trade.info_cuts(a["s_first"], scale_all=share), a["eps"]) * (1 - share)
    mx = share * a["vfr_attrib"] * trade.VFR_SHARE_ALL_INBOUND * trade.IN["us_travel_exports_mx"]
    rest = share * a["vfr_attrib"] * trade.VFR_SHARE_ALL_INBOUND * (trade.IN["us_travel_exports_all"] - trade.IN["us_travel_exports_mx"])
    visits = (trade.us_gain({(trade.U, trade.M): mx, (trade.U, trade.R): rest}, a["eps"]) + a["tax"] * (mx + rest)) * (1 - share)
    fdi = share * a["fdi_s"] * (trade.IN["usdia_position_all"] - trade.IN["usdia_holding_all"]) * a["fdi_excess"] * (1 - share)
    return dict(total_consumer_scale={e: float(grocery + networks + media) for e in ENDS},
                restaurant_variety_market_size={e: float(restaurant) for e in ENDS},
                total_trade_travel_fdi={e: -float(info + visits + fdi) for e in ENDS})


def scale_source(src, share):
    tree = ast.parse(src.path("scale_spillovers_2026_09_23/arms.py").read_text())
    declarations = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "CRY_PAPER" for t in node.targets)]
    require(len(declarations) == 1, "authoritative CRY_PAPER declaration")
    paper = declarations[0]
    fit = src.table("scale_spillovers_2026_09_23/derived/cry_gradient.csv")
    fit = fit[fit.outcome.eq("psi_acspredict") & fit.regressors.eq("lnsize+frachighed") & fit.term.eq("lnsize")]
    require(len(fit) == 1, "executed conditional CRY coefficient")
    nat = src.table("scale_spillovers_2026_09_23/derived/pums_national.csv")
    nat = nat[nat.label.eq("all")].set_index("item").estimate
    hs = float(nat["earnings_lths"] + nat["earnings_hs"]) * (1 - share)
    more = float(nat["earnings"] - nat["earnings_lths"] - nat["earnings_hs"]) * (1 - share)
    ratio = float(fit.coef.iloc[0]) / paper["lnsize"][0]
    gain = sum(earnings * (1 - math.exp(paper[key][0] * ratio * math.log1p(-share)))
               for key, earnings in (("size_hsless", hs), ("size_more", more))) / 1e9
    # Native gain includes tax receipts, rather than adding receipts twice.
    return {e: -float(gain) for e in ENDS}


def volunteering_source(src, share):
    receipts = src.native("benefits_inventory_2026_09_28/social_receipts.py")
    src.path("benefits_inventory_2026_09_28/build_tables.py")
    constants = receipts.legacy_constants()
    supply = src.table("benefits_inventory_2026_09_28/derived/volunteering_supply.csv")
    national = supply[supply.group.eq("national")]
    require(len(national) == 1, "national CEV supply")
    value = float(national.volunteers.iloc[0]) * constants["VALUE"] / constants["VOLS"] / 1e9
    # Reuse the native task definition on all national volunteers. Its only
    # origin-dependent input is the membership mask; an empty mask makes the
    # native outside-union estimator the national estimator, without file writes.
    receipts.union = lambda d: np.zeros(len(d), dtype=bool)
    with np.errstate(invalid="ignore"):
        _, mix = receipts.organization_mix()  # the intentionally empty union's unused reporting row is0/0
    task = mix["primary_food"]
    require(math.isfinite(task) and 0 <= task <= 1, "national primary-food volunteer task share")
    src.path("benefits_inventory_2026_09_28/_cache/sep15pub.dat.gz")
    src.path("benefits_inventory_2026_09_28/_cache/cpssept15.pdf")
    outward = value * share * (1 - share)
    incoming = value * (1 - share) * task * share  # displacement1, as the central stack
    return {e: -outward + incoming for e in ENDS}


def transport_sources(src, share, fiscal, *, congestion_state=None):
    if congestion_state is None:
        congestion = src.native("service_response_long_run_2026_09_27/congestion.py")
        state = congestion.setup()
    else:
        src.path("service_response_long_run_2026_09_27/congestion.py")
        congestion, state = congestion_state
    _, _, _, vots, exposures, _ = state
    ex = exposures["2017 southwest"].copy()
    ex["s"], ex["phi_commute_route"] = share, share
    ex["group_persons"], ex["other_persons"] = ex.persons * share, ex.persons * (1 - share)
    hours = src.table("congestion_2026_09_23/derived/nhts_hours_by_urbansize.csv")
    for year in (2017, 2022):
        rows = hours[hours.survey.eq(year)].copy()
        rows["weighted"] = rows.persons_5plus * rows.pov_hours_per_person
        avg = rows.groupby("urbansize").weighted.sum() / rows.groupby("urbansize").persons_5plus.sum()
        ex[f"h_other_{year}"] = ex.urbansize.map(avg)
    scope = ex.in_scope.to_numpy()
    crash = src.native("road_crash_externality_2026_09_28/crash_model.py")
    crash.P_SHARE, crash.VMT_RATIO_OTHERS["central"] = share, 1.
    crash.HISP_PED, crash.MEX_OF_HISP = share, 1.
    levels = crash.x_levels_evidence()
    p = {k: v[1] for k, v in crash.FACTORS.items()}
    p["x_nonfatal"], p["x_fatal"] = levels["x_nonfatal"][1], levels["x_fatal"][1]
    p["r_c"], p["q_mult"], p["liab"] = 1., 0., (p["liab"][0], crash.INS_OTHER)
    result = crash.evaluate_split(*[p[k] for k in crash.FACTORS], r_nf=(1., 1.), composition=True)
    congestion_values, crashes = {}, {}
    for end in ENDS:
        response = fiscal[end]["highway_response"]
        cut = response * share
        require(0 <= cut < 1, "average retained road capacity")
        congestion_values[end] = congestion.arm(ex, scope, share, congestion.A.POP_FIXED_LANES["central"],
            congestion.A.LANES_COEF_T10, cut, share, vots["central"], 2022, 1.)
        residual = 1 - (1 - share) / (1 - cut)
        density = share * (1 - share) * (crash.BASE["mv_nonfatal"] * p["x_nonfatal"] + crash.BASE["mv_fatal"] * p["x_fatal"])
        crashes[end] = result["total"] + density * (residual / share - 1)
    return dict(congestion=congestion_values, road_crash_externality=crashes)


def average_components(national_fiscal, *, population_people, national_people, fiscal_dir=FISCAL,
                       congestion_state=None):
    """Return native average social parts; fiscal[end] supplies own cash H/G/roads.

    Required per end: current_H_bn, government_consumption_removed_bn,
    government_consumption_national_bn, highway_response. H is signed current cash
    spending minus lost taxes, with capital/private production/pension accrual out.
    """
    require(0 < population_people < national_people, "population boundary")
    share = population_people / national_people
    src = Sources(fiscal_dir)
    sys.dont_write_bytecode = True
    values = crime_sources(src, share)
    values["housing_gain"] = housing_source(src, share)
    values.update(consumption_sources(src, share, national_people))
    values["scale_net_earnings"] = scale_source(src, share)
    values["formal_volunteering_outside_group"] = volunteering_source(src, share)
    values.update(transport_sources(src, share, national_fiscal, congestion_state=congestion_state))
    un = src.table("uncompensated_care_2026_09_23/derived/added_cost_arms.csv")
    un = un[un.use_intensity.eq(1.)]
    private = un.national_bn * (1 - un.gov_offset_share)
    values["unreimbursed_care"] = dict(low=float(private.min()) * share * (1 - share), high=float(private.max()) * share * (1 - share))
    air = src.native("air_pollution_2026_09_28/air_items.py")
    deaths = air.national_deaths_2024(air.ARMS["crf"][1], air.ARMS["trend"][1])[0]
    harm = deaths * air.VSL_DOT_2024 * air.ARMS["morbidity"][1] / 1e9
    pce = src.table("social_respending_2026_10_14/derived/spending_components.csv")
    pce = pce[pce.spending_denominator.eq("PCE")].national_spending_bn.unique()
    require(len(pce) == 1 and pce[0] > 0, "national PCE denominator")
    values["pm25_consumption"], values["pm25_government_side"] = {}, {}
    for end in ENDS:
        f = national_fiscal[end]
        require(all(math.isfinite(float(f[k])) for k in ("current_H_bn", "government_consumption_removed_bn", "government_consumption_national_bn", "highway_response")), "nonfinite own national fiscal source")
        require(f["government_consumption_national_bn"] > 0, "public consumption denominator")
        direct = harm * air.THETA_CONSUMPTION * share * (1 - share)
        respending = -f["current_H_bn"] * harm * air.THETA_CONSUMPTION / pce[0] * (1 - share)
        values["pm25_consumption"][end] = direct + respending
        values["pm25_government_side"][end] = harm * air.THETA_GOVERNMENT * f["government_consumption_removed_bn"] / f["government_consumption_national_bn"] * (1 - share)
    sys.path.insert(0, str(FISCAL / "scripts"))
    from memory_budget import require_within_budget
    require_within_budget("equal-count average social source evaluation")
    return values, dict(population=population_people, national_population=national_people, fraction=share,
        mortality_valuation="dot_uniform", real_discount_rate=0., source_sha256=src.pins,
        source_pin_scope="Direct native modules/tables and explicitly consumed inputs; native source lanes retain their own transitive provenance contracts.",
        assumptions=["Equal-count random removal pro rata in each age, skill, geography, source and receiver cell.",
            "Native central source coefficients and national dollar vintages retained; CE per-person spending uses its published source table at cent precision; no Mexican social-dollar scaling.",
            "Crime/fear/security use common active DOT units, P7 forward/reverse payments and WTP-security overlap rule.",
            "School discipline gap is zero for a random average group under the native excess-discipline formula.",
            "Housing native rent path/integral uses random domestic landlord membership and the same foreign-owner share.",
            "Volunteering uses national CEV supply and random receivers; only the same primary-food incoming proxy at displacement1 is priced.",
            "Roads use national-average traffic/hours and the comparator's own retained capacity; crash capacity acts on multivehicle density only.",
            "PM uses uniform DOT mortality plus morbidity, national-average source intensity and random receptors; public consumption uses government-average intensity; public investment emissions omitted.",
            "PCE re-spending uses own current cash balance, including a signed negative balance; capital resource charges and promise accrual are not re-spent."])


def component_bridge(absolute_rows, average, absolute_fiscal, average_fiscal):
    rows, totals = [], {}
    absolute = {r["item"]: r["total_by_end_bn"] for r in absolute_rows}
    require(len(absolute) == len(absolute_rows), "duplicate absolute social item")
    require(set(absolute) == set(average), "source component mismatch: missing=" + str(sorted(set(absolute)-set(average))) + "; extra=" + str(sorted(set(average)-set(absolute))))
    for end in ENDS:
        parts = [("fiscal", float(absolute_fiscal[end]), float(average_fiscal[end]))]
        parts += [(item, float(absolute[item][end]), float(average[item][end])) for item in sorted(absolute)]
        require(all(math.isfinite(a) and math.isfinite(b) for _, a, b in parts), "unavailable/nonfinite component")
        rows += [dict(end=end, component=item, absolute_bn=a, average_resident_bn=b, excess_bn=a-b) for item,a,b in parts]
        a, b, gap = (sum(r[key] for r in rows if r["end"] == end) for key in ("absolute_bn", "average_resident_bn", "excess_bn"))
        require(abs(a-b-gap) < 1e-9, "joint component closure")
        totals[end] = dict(absolute_bn=a, equal_count_average_bn=b, joint_social_excess_vs_average_bn=gap)
    return dict(ends=totals, component_bridge=rows, closure_tolerance_bn=1e-9)


def build_average_social(absolute_rows, national_fiscal_states, *, absolute_fiscal_by_basis,
                         population_people, national_people, fiscal_dir=FISCAL, congestion_state=None):
    """Build both timing sets from own national fiscal states and current source rows.

    national_fiscal_states[basis][end] adds fiscal_cost_bn to average_components'
    contract. Absolute social rows can be a basis->rows mapping or the common
    current-2024-flow rows. Promises differ in the fiscal leg; both social legs use
    their own current-cash H, which must coincide between the accounting sets.
    """
    require(set(national_fiscal_states) == {"set", "cash"}, "both accounting sets required")
    result = dict(case="oct16", comparator="equal_count_average_residents_random_pro_rata", sets={},
                  timing_match="2024 current cash social flows in both sets; pension promises accrue in set and benefits when paid in cash; no capital charge or accrual timing re-spending")
    for end in ENDS:
        for key in ("current_H_bn", "government_consumption_removed_bn", "government_consumption_national_bn", "highway_response"):
            require(abs(national_fiscal_states["set"][end][key] - national_fiscal_states["cash"][end][key]) < 1e-9,
                    "social timing differs; provide matched current-cash funding/physical rules in both sets: " + key)
    avg, receipt = average_components(national_fiscal_states["cash"], population_people=population_people,
                                      national_people=national_people, fiscal_dir=fiscal_dir,
                                      congestion_state=congestion_state)
    for basis in ("set", "cash"):
        fiscal = national_fiscal_states[basis]
        absolute = absolute_rows[basis] if isinstance(absolute_rows, dict) else absolute_rows
        bridge = component_bridge(absolute, avg, absolute_fiscal_by_basis[basis], {end:fiscal[end]["fiscal_cost_bn"] for end in ENDS})
        result["sets"][basis] = dict(bridge, average_social_components=avg, source_receipt=receipt)
    return result
