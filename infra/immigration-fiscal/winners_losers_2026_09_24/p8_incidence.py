"""Round-two incidence corrections and explicit v7 ablations.

Native-First: reuse the frozen lane's person frame, allocators and priced arrays.
No solver or source account is replaced. Fix switches exist only to identify
isolated effects; the joint model uses every authorized correction.
"""
from __future__ import annotations

import json
import ast
import types
from pathlib import Path

import numpy as np
import pandas as pd

import p7_frames as p7

HERE = Path(__file__).resolve().parent
ALL_FIXES = frozenset(range(1, 13))
EXISTING = dict(victims="crime_victims", property_crime="property_crime",
                unreimbursed_care="unreimbursed_care", congestion="congestion")
EXTRA_FIELDS = ["PEN_SC1", "PEN_SC2", "PEN_VAL1", "PEN_VAL2", "SUR_SC1", "SUR_SC2",
                "SUR_VAL1", "SUR_VAL2", "DIS_SC1", "DIS_SC2", "VET_TYP4", "VET_TYP5", "MIL", "CHAMPVA"]


def frozen_module(wl, name):
    """Load the checkpoint's unchanged source as the ablation oracle."""
    path = HERE / f"{name}.py"
    module = types.ModuleType(f"frozen_{name}")
    module.__file__ = str(path)
    checkpoint = "f3148023f0e339368880c526c0cbbf7051a45c43"
    body = wl.git_show(str(path.relative_to(wl.ROOT)), checkpoint)
    exec(compile(body, str(path) + "@" + checkpoint, "exec"), module.__dict__)
    return module


def own_resources(d):
    n = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    cash = d.PTOTVAL.to_numpy(float) - d.FEDTAX_AC.to_numpy(float)
    cash -= d.STATETAX_A.to_numpy(float) + d.FICA.to_numpy(float)
    return cash + sum(d[k].to_numpy(float) / n for k in (
        "SPM_SNAPSUB", "SPM_SCHLUNCH", "SPM_WICVAL", "SPM_ENGVAL", "SPM_CAPHOUSESUB"))


def programme_keys(wl, d, weights, programmes, notes):
    """Separate programme authority from the exporter’s retained funding shares.

    Component exclusions concern programmes, not the people receiving them: a
    person can use a state service and also receive a federal benefit.
    """
    n = d.groupby("SPM_ID").SPM_ID.transform("size").to_numpy()
    raw = lambda name: np.maximum(d[name].to_numpy(float), 0)
    spm = lambda name: raw(name) / n
    rail = sum(np.where(d[f"PEN_SC{i}"].eq(7), raw(f"PEN_VAL{i}"), 0) +
               np.where(d[f"SUR_SC{i}"].eq(5), raw(f"SUR_VAL{i}"), 0) +
               np.where(d[f"DIS_SC{i}"].eq(6), raw(f"DIS_VAL{i}"), 0) for i in (1, 2))
    disability = lambda code: sum(np.where(d[f"DIS_SC{i}"].eq(code),raw(f"DIS_VAL{i}"),0) for i in (1,2))
    keys = {"social_security": raw("SS_VAL"), "ssi": raw("SSI_VAL"),
            "unemployment": raw("UC_VAL"), "snap": spm("SPM_SNAPSUB"),
            "housing_subsidies": spm("SPM_CAPHOUSESUB"), "energy_assistance": spm("SPM_ENGVAL"),
            "medicare": d.MCARE.eq(1).to_numpy(float),
            "medicaid_and_chip_other_medical": d.MCAID.eq(1).to_numpy(float),
            "education_k12": d.A_AGE.between(5, 17).to_numpy(float),
            "education_college_other": (d.A_ENRLW.eq(1) & d.A_HSCOL.eq(2)).to_numpy(float),
            "education_benefits": raw("ED_VAL"), "workers_compensation": raw("WC_VAL"),
            "veterans_pension_disability": raw("VET_VAL"),
            "temporary_disability": disability(9), "black_lung": disability(8),
            "family_and_general_assistance": raw("PAW_VAL"),
            "refundable_tax_credits": raw("ACTC_CRD") + raw("EIT_CRED"),
            "railroad_retirement": rail,
            "veterans_readjustment": d.VET_TYP4.eq(1).to_numpy(float),
            "veterans_other": d.VET_TYP5.eq(1).to_numpy(float),
            "military_medical": (d.MIL.eq(1) | d.CHAMPVA.eq(1)).to_numpy(float)}
    authority_keys = {"federal": np.zeros(len(d)), "state_local": np.zeros(len(d))}
    table = []
    forbidden = {"federal": {"education_k12", "education_college_other", "public_order_safety"},
                 "state_local": {"social_security", "medicare", "ssi", "snap", "refundable_tax_credits"}}
    for row in programmes:
        item = row["id"]
        k = keys.get(item, np.ones(len(d)))
        basis = "CPS receipt/enrollment" if item in keys else "[ASSUMPTION] universal service receipt; no separate CPS programme field"
        for jurisdiction, key in authority_keys.items():
            fraction = row["jurisdiction"][jurisdiction]
            p7.require(f"programme_authority_{jurisdiction}_{item}", 0 <= fraction <= 1)
            p7.require(f"programme_exclusion_{jurisdiction}_{item}", item not in forbidden[jurisdiction] or fraction == 0)
            amount = row["national_bn"] * row["response"] * fraction
            # Cash trust flows get a separate recipient key; Social Security is
            # not available for general-fund programme cuts. Medicare remains
            # a proxy for non-Part-A health receipt in the general-fund key.
            if item == "social_security" and jurisdiction == "federal":
                amount = 0.
            if amount:
                key += wl.alloc(d, k, amount)
            table.append(dict(programme=item, jurisdiction=jurisdiction,
                              responding_national_bn=amount, key=basis,
                              funding_federal_share=row["federal_share"],
                              jurisdiction_basis=row["jurisdiction_basis"]))
        if item not in keys:
            notes.setdefault("unmapped_programmes", []).append(dict(programme=item, basis=basis))
    return authority_keys["federal"], authority_keys["state_local"], table


def credit_policy(case, payload, legacy_active):
    """Prevent item 5b and its replacement from entering the same direct gain."""
    if case == "oct14":
        p7.require("credits_v7_legacy_only", legacy_active and "mixed_unit_removal" not in payload["meta"])
        return "item5b"
    meta = payload["meta"].get("mixed_unit_removal")
    p7.require("credits_v8_replacement_only", not legacy_active and meta is not None)
    p7.require("credits_v8_end_parts_exist", all("by_generation_bn" in meta["by_end"][e] for e in ("low", "high")))
    return "item11"


class Incidence:
    def __init__(self, wl, B, d, I, ch, meta, fin, ctx, payload, trust,
                 programmes, credits, old_cohort, new_cohort, nest_old, nest_new):
        self.wl, self.B, self.d, self.I = wl, B, d, I
        self.ch, self.meta, self.fin, self.ctx = ch, meta, fin, ctx
        self.payload, self.lineage, self.trust = payload, payload["meta"]["lineage"], trust
        self.programmes, self.credits = programmes, credits
        self.cohort_old, self.cohort_new = old_cohort, new_cohort
        self.nest_old, self.nest_new = nest_old, nest_new
        self.w = d.pw.to_numpy().copy()
        self.other = d.other.to_numpy(bool)
        self.mw, _ = wl.lineage_group_weights(B, d)
        self.uw, _ = wl.row4_group_weights(B, d)
        self.resources = own_resources(d)
        if wl.CASE["case"] == "oct15":
            from p8_social import source
            self.source = source(wl)
        else:
            self.source = json.loads((HERE / "inputs/social_oct14.json").read_text())
        self.details, self.notes = [], {}
        self.cache = {}
        self.state_cache = {}
        self.allocation_cache = {}
        self.epsilon_cache = {}
        self.state_masks = {int(s): d.st.eq(s).to_numpy() for s in d.st.unique()}

    def configure(self, fixes):
        self.fixes = frozenset(fixes)
        self.cache.clear()
        self.state_cache.clear()
        self.allocation_cache.clear()
        self.epsilon_cache.clear()
        self.notes = {}
        p7.CUT_CACHE.clear()
        if self.wl.CASE.get("case") == "oct15":
            from p8_membership import payer_weights
            self.weights, self.payer_cells, self.payer_audit = payer_weights(
                self.d, self.w, self.lineage, self.wl, geographic=10 in self.fixes)
        elif 10 in self.fixes:
            from p8_recipient_keys import lineage_payers_state_age
            self.weights, self.payer_cells = lineage_payers_state_age(self.d, self.w, self.lineage, self.wl)
        else:
            self.weights, self.payer_cells = p7.lineage_payers(self.d, self.w, self.lineage, self.wl)
        self.dd = p7.weighted_frame(self.d, self.weights)
        self.channels = {k: {L: p7.transport(v[L], self.w, self.weights, self.d,
                             source_other=self.d.other_oct14.to_numpy() if "other_oct14" in self.d else None)
                             for L in self.wl.LEVELS} for k, v in self.ch.items()}
        self.pool = p7.pooler(self.d, self.weights)

    def context(self, rule):
        if rule in self.cache:
            return self.cache[rule]
        wl, d, weights = self.wl, self.dd, self.weights
        kf, ks = (self.ctx["tax_fed"], self.ctx["tax_sl"]) if rule == "a" else (np.ones(len(d)), np.ones(len(d)))
        table = []
        if rule == "c":
            if 2 in self.fixes:
                ends = [programme_keys(wl, d, weights, self.programmes[e], self.notes) for e in ("low", "high")]
                kf, ks = ((ends[0][j] + ends[1][j]) / 2 for j in (0, 1))
                table = [dict(level=e, **row) for e, values in zip(("low", "high"), ends) for row in values[2]]
            else:
                keys = [p7.responding_programme_key(d, weights, self.programmes[e])[0] for e in ("low", "high")]
                kf = ks = sum(keys) / 2
        if wl.CASE["case"] == "oct15":
            from p8_social import allocate
            soc, values, cov = allocate(wl, d, self.I, self.channels, self.meta,
                weights, rule, dict(self.ctx, programme_receipts=kf), self.notes)
        else:
            soc, values, cov = p7.social_channels(wl, d, self.I, self.channels, self.meta,
                weights, "lineage", rule, dict(self.ctx, programme_receipts=kf),notes=self.notes)
        if 4 in self.fixes:
            from p8_recipient_keys import air_mortality_key, crash_victim_key
            health_items = [("pm25_consumption", air_mortality_key), ("road_crash_externality", crash_victim_key)]
            if wl.CASE["case"] == "oct15":
                health_items += [("pm25_respending", air_mortality_key), ("pm25_government_side", air_mortality_key)]
            for item, helper in health_items:
                key, audit = helper(d, weights, wl.FISCAL)
                if item.startswith("pm25_"):
                    # The helper's age margins are normalized inside states.
                    # Restore population-weighted national exposure, plus the
                    # producer's local fraction, retaining both its age margin
                    # and the lane's declared dispersion geography.
                    counts = pd.Series(weights * d.other.to_numpy()).groupby(d.st).sum()
                    key *= d.st.map(counts).to_numpy()
                    tree = ast.parse((wl.FISCAL / "air_pollution_2026_09_28/air_items.py").read_text())
                    declaration = next(n.value for n in tree.body if isinstance(n, ast.Assign) and
                        any(isinstance(t, ast.Name) and t.id == "ARMS" for t in n.targets))
                    fraction = ast.literal_eval(next(v for k, v in zip(declaration.keys, declaration.values)
                        if isinstance(k, ast.Constant) and k.value == "L"))[1]
                    states = {wl.POSTAL[s]: v for s, v in self.meta["group_state_share"].items()}
                    soc[item] = {L: wl.alloc_states(d, key, {s: values[item][L]*fraction*v for s,v in states.items()},
                        notes=self.notes, label="air_age_mortality") + wl.alloc(d,key,values[item][L]*(1-fraction)) for L in wl.LEVELS}
                else:
                    soc[item] = {L: wl.alloc(d, key, values[item][L]) for L in wl.LEVELS}
                self.details.append(dict(kind=item, financing=rule, audit=audit))
                if item.startswith("pm25_"):
                    old = d.A_AGE.ge(65).to_numpy()
                    share = abs(p7.total(np.where(old, soc[item]["central"], 0), weights) / values[item]["central"])
                    target = audit["expected_age65_share"]
                    p7.require("air_old_recipient_death_share", abs(share - target) <= .01, allocated_share=share, source_share=target)
            if wl.CASE.get("case") == "oct15":
                for L in wl.LEVELS:
                    a, b = "pm25_government_side", "pm25_respending"
                    error = np.max(np.abs(soc[a][L]*values[b][L] - soc[b][L]*values[a][L]))
                    p7.require("budget_pm_pair_same_receptors_"+L, error < 1e-6, max_scaled_dollar_error=float(error))
        if 7 in self.fixes:
            from p8_recipient_keys import property_key_with_rentals
            pkey, missing = property_key_with_rentals(d, self.I, self.B, weights, wl.FISCAL)
        else:
            pkey, missing = p7.property_key(d, self.I, self.B, weights)
        statew = {L: p7.state_wages(d, weights, self.channels["wages"][L], wl, group_weights=self.mw)[0] for L in wl.LEVELS}
        factor = self.lineage["members"]["g3plus"] / self.lineage["counts"]["identified_g3plus"]
        if wl.CASE["case"] == "oct15":
            credit_policy(wl.CASE["case"], self.payload, False)
            credit = self.credits["by_end"]
        else:
            credit_policy(wl.CASE["case"], self.payload, True)
            credit = self.credits["forward"] + factor * self.credits["forward_g3plus"]
            amount = self.credits["metadata"]["forward"]["total_bn"] + factor * self.credits["metadata"]["forward_g3plus"]["total_bn"]
            credit = credit * amount / p7.total(credit, weights)
        result = dict(kf=kf, ks=ks, social=soc, social_values=values, property_key=pkey,
                      statew=statew, credit=credit, programme_table=table, property_audit=missing)
        if wl.CASE.get("case") == "oct15":
            result["credit_attribution"] = self.credits.get("by_end_attribution", credit)
        self.cache[rule] = result
        return result

    def social_vector(self, cx, level, setting, coverage_only=False):
        arrays = {k: v[level] for k, v in cx["social"].items()}
        if coverage_only and 6 in self.fixes:
            for item, channel in EXISTING.items():
                arrays[item] = self.channels[channel][level]
            arrays["housing_gain"] = self.channels["renters"][level] + self.channels["landlords"][level]
            # The source-rounding delta is not coverage, and legacy mobility is
            # supplemental. Keep it fixed in the matched comparator.
            arrays["source_rounding"] = np.zeros(len(self.d))
            arrays["mobility_supplemental"] = self.channels["mobility"][level]
            return arrays
        if 5 not in self.fixes or setting == "central":
            return arrays
        if self.wl.CASE.get("case") == "oct15":
            from p8_social import uncertainty_ratio
            return {item: vector * uncertainty_ratio(self.source, item, setting,
                    self.channels, self.weights) for item, vector in arrays.items()}
        producers = {r["item"]: r for r in self.source["social_items_in_the_social_rows"]["items"]}
        for item, vector in list(arrays.items()):
            if item == "source_rounding":
                continue
            if item in producers:
                row = producers[item]
                p7.require(f"social_producer_range_{item}", row["low_bn"] <= row["central_bn"] <= row["high_bn"])
                seed = row["central_bn"]
                p7.require(f"social_range_nonzero_seed_{item}", seed != 0)
                arrays[item] = vector * row[f"{setting}_bn"] / seed
            elif item in EXISTING:
                channel = EXISTING[item]
                numerator = p7.total(self.channels[channel][setting], self.weights)
                denominator = p7.total(self.channels[channel]["central"], self.weights)
                arrays[item] = vector * numerator / denominator
            elif item == "housing_gain":
                # Gross rent changes travel together in each producer arm.
                ratio = self.lineage["counts"]["added"] / self.lineage["counts"]["identified"] if "identified" in self.lineage["counts"] else self.source["lineage_social_rows"]["keys"]["head_count"]
                arrays[item] = (self.channels["renters"][setting] + self.channels["landlords"][setting]) * (1 + ratio)
            else:
                raise RuntimeError(f"[BLOCKED] no social uncertainty declaration: {item}")
        return arrays

    def evaluate(self, rule, frame, level, arm="recommended", social_setting="central", epsilon=None):
        wl, d, weights = self.wl, self.dd, self.weights
        cx = self.context(rule)
        fiscal, tr = self.meta["fiscal"][level], self.trust[level]
        today, future = fiscal["federal_today"], fiscal["future"]
        cash_trust = tr["cash_benefits_bn"] - tr["payroll_bn"]
        borrowing = fiscal["future_borrowing"]
        p7.require("capital_is_resource_cost_never_borrowing", abs(fiscal["future"] - borrowing - fiscal["accrual"]) < 1e-9,
                   resource_federal_bn=fiscal["resource_federal"], future_borrowing_bn=borrowing)
        share = self.meta["deficit"]["share"]
        trust_recipient = np.maximum(d.SS_VAL.to_numpy(float), 0) + d.MCARE.eq(1).to_numpy(float) * tr["cash_benefits_bn"] * 1e9 / max(1., np.dot(weights, d.MCARE.eq(1)))
        general_today = today
        direct_trust = np.zeros(len(d))
        if 2 in self.fixes and rule == "c":
            general_today -= (1 - share) * cash_trust
            direct_trust = -wl.alloc(d, trust_recipient, (1 - share) * cash_trust)
        pieces = {}
        if frame == "hybrid":
            pieces["general_federal"] = -wl.alloc(d, cx["kf"], general_today)
            pieces["current_trust_cash"] = direct_trust
        elif frame == "stationary":
            if 3 in self.fixes:
                from p7_cohorts import payroll_key
                key = payroll_key(d, tr["hi_payout_fraction"])
                pieces["trust_accrual"] = -wl.alloc(d, key, tr["accrual_bn"])
                p7.require("trust_accrual_covered_earnings_only", not np.any(pieces["trust_accrual"][key == 0]))
                pieces["general_federal"] = -wl.alloc(d, cx["kf"], general_today + future - tr["accrual_bn"])
            else:
                pieces["general_federal"] = -wl.alloc(d, cx["kf"], general_today + future)
            pieces["current_trust_cash"] = direct_trust
            future = 0.
        elif frame.startswith("cohort"):
            ck = (self.cohort_new if 3 in self.fixes else self.cohort_old)[10 in self.fixes]
            horizon = "borrowing30" if frame == "cohort30" else "borrowing10"
            debt_share, trust_share = ck["living_shares"][horizon], ck["living_shares"]["trust"]
            if 3 in self.fixes:
                # Current cash remains on its 2024 incidence. Only accrual is
                # deferred; current borrowing retains the ordinary debt key.
                pieces["general_federal"] = -wl.alloc(d, cx["kf"], general_today)
                pieces["current_trust_cash"] = direct_trust
                pieces["trust_accrual"] = -wl.alloc(d, np.asarray(ck["keys"]["trust"]), tr["accrual_bn"] * trust_share)
                pieces["borrowing_service"] = -wl.alloc(d, np.asarray(ck["keys"][horizon]), borrowing * debt_share)
                future = tr["accrual_bn"] * (1 - trust_share) + borrowing * (1 - debt_share)
            else:
                pieces["general_federal"] = -wl.alloc(d, cx["kf"], today - (1 - share) * cash_trust)
                pieces["trust_whole_block"] = -wl.alloc(d, np.asarray(ck["keys"]["trust"]), tr["trust_cost_bn"] * trust_share)
                remaining = borrowing - share * cash_trust
                pieces["borrowing_service"] = -wl.alloc(d, np.asarray(ck["keys"][horizon]), remaining * debt_share)
                future = tr["trust_cost_bn"] * (1 - trust_share) + remaining * (1 - debt_share)
        else:
            raise RuntimeError(f"[BLOCKED] select financing frame explicitly: {frame}")
        state = {wl.POSTAL[s]: v for s, v in self.meta["group_state_share"].items()}
        if 10 in self.fixes:
            from p8_recipient_keys import state_spending_shares
            for end in ("low", "high"):
                if end not in self.state_cache:
                    shares, audit = state_spending_shares(d, self.mw, self.programmes[end], wl.FISCAL, end)
                    self.state_cache[end] = {s: self.meta["fiscal"][end]["state_local"]*v for s,v in shares.items()}
                    self.details.append(dict(kind="state_local_spending", level=end, audit=audit))
                    for notice in audit.get("notices", []):
                        self.notes.setdefault("state_spending_notices",[]).append(f"{end}: {notice}")
                        print(f"{p7.GATE_SCOPE}/{end}: {notice}",flush=True)
        geography = arm in ("stack", "capitalization")
        keysl = cx["property_key"] if geography else cx["ks"]
        state_amounts = {s: fiscal["state_local"] * v for s, v in state.items()}
        if 10 in self.fixes:
            state_amounts = ({s: (self.state_cache["low"][s]+self.state_cache["high"][s])/2 for s in self.state_cache["low"]}
                             if level == "central" else self.state_cache[level])
            p7.require("state_local_end_pairing", abs(sum(state_amounts.values())-fiscal["state_local"]) < 1e-9)
        allocation_key = (rule, level, geography)
        if allocation_key not in self.allocation_cache:
            self.allocation_cache[allocation_key] = -wl.alloc_states(d,keysl,state_amounts,notes=self.notes,
                label=f"state-local/{level}/property={geography}/{rule}; reused across financing frames and epsilon arms")
        pieces["state_local"] = self.allocation_cache[allocation_key]
        if self.wl.CASE.get("case") == "oct15":
            pieces["unlocated_fiscal"] = -wl.alloc(d, np.ones(len(d)), fiscal.get("unlocated", 0.))
        for state_code, amount in state_amounts.items():
            mask = self.state_masks[state_code]
            p7.check_total(f"state_local_geography_{state_code}", pieces["state_local"][mask], weights[mask], -amount)
        wages = cx["statew"][level] if arm == "stack" else self.channels["wages"][level]
        pieces["wages_positive"], pieces["wages_negative"] = np.maximum(wages, 0), np.minimum(wages, 0)
        pieces["displaced_beneficiaries"] = self.channels["displaced_beneficiaries"][level]
        head = -((self.fin[wl.CASE["model"]]["ends"]["low"]["cost_bn"] + self.fin[wl.CASE["model"]]["ends"]["high"]["cost_bn"]) / 2 if level == "central" else self.fin[wl.CASE["model"]]["ends"][level]["cost_bn"])
        residual = head + future - p7.total(sum(pieces.values()), weights)
        p7.require("fiscal_rounding_only", abs(residual) < 1e-3, residual_bn=residual)
        pieces["fiscal_source_rounding"] = wl.alloc(d, cx["kf"], residual)
        p7.check_total("exact_fiscal_case", sum(pieces.values()), weights, head + future)
        if epsilon:
            from p7_nest import transport_wage_delta
            nest = (self.nest_new if 9 in self.fixes else self.nest_old)[epsilon]
            epsilon_key = (epsilon, level, arm == "stack")
            if epsilon_key not in self.epsilon_cache:
                change = transport_wage_delta(d, nest["delta_wages"][level], self.w, weights, p7.require)
                if arm == "stack":
                    change = p7.state_wages(d, weights, change, wl, group_weights=self.mw)[0]
                self.epsilon_cache[epsilon_key] = change
            change = self.epsilon_cache[epsilon_key]
            replacement = wages + change
            pieces["wages_positive"], pieces["wages_negative"] = np.maximum(replacement, 0), np.minimum(replacement, 0)
            pieces["epsilon_induced_receipts"] = wl.alloc(d, cx["kf"], nest["delta_f"][level])
        pieces.update(self.social_vector(cx, level, social_setting, coverage_only=arm == "coverage"))
        if arm != "coverage":
            if wl.CASE.get("case") == "oct15":
                ends = ("low", "high") if level == "central" else (level,)
                credits = cx["credit_attribution"] if arm == "item11_attribution" else cx["credit"]
                components = set().union(*(credits[end] for end in ends))
                for component in sorted(components):
                    pieces["item11_stayers_" + component] = sum(credits[end][component] for end in ends) / len(ends)
                p7.require("credits_no_5b_beside_item11", "crossing_credits" not in pieces)
            else:
                pieces["crossing_credits"] = cx["credit"]
        if arm == "stack":
            gross = []
            for end in (("low", "high") if level == "central" else (level,)):
                suffix = "_national_uniform" if end == "high" else ""
                land = self.channels["landlords" + suffix]["central"]
                rent = self.channels["renters" + suffix]["central"]
                gross.append(land * cx["social_values"]["housing_gain"][end] / p7.total(land + rent, weights))
            land = sum(gross) / len(gross)
            if 5 in self.fixes and social_setting != "central":
                # Gross landlord transfer follows the same parameter arm as
                # the coherent housing net, not a net-only multiplier.
                if wl.CASE.get("case") == "oct15":
                    from p8_social import uncertainty_ratio
                    land = land * uncertainty_ratio(self.source, "housing_gain", social_setting,
                                                    self.channels, weights)
                else:
                    ratio = self.source["lineage_social_rows"]["keys"]["head_count"]
                    land = self.channels["landlords"][social_setting] * (1 + ratio)
            if 10 in self.fixes:
                from p8_recipient_keys import landlord_split_by_state
                replacement, _, _, _ = landlord_split_by_state(wl, d, weights, land)
            else:
                replacement, _, _, _ = p7.landlord_split(wl, d, weights, land)
            pieces["housing_gain"] = pieces["housing_gain"] + replacement - land
        x = sum(pieces.values())
        sharing = dict(person=x, pooled=self.pool(x))
        recon = {}
        if 1 in self.fixes:
            sharing["mixed_unit"], recon = p7.mixed_resource_change(d, weights, self.mw, self.resources, x)
        else:
            cw = np.where(d.target.to_numpy(), self.mw, weights)
            mixed = p7.pooler(d, cw, d.target.to_numpy() | self.other)(x + np.where(d.target, self.resources, 0))
            sharing["mixed_unit"] = np.where(self.other, mixed, 0)
        pieces["mixed_boundary"] = sharing["mixed_unit"] - sharing["pooled"]
        return sharing, pieces, future, recon
