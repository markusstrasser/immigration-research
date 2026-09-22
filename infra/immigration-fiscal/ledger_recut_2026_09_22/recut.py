"""Recut the Mexican-origin union's annual expanded balance into a practitioner range.

Object: `ledger_absolute_2026_09_17`, income-year 2024, household-shared allocation,
the union of the three Mexican-origin target groups (40.9m civilian household
residents). Everything here is a linear combination of that lane's published
per-item replicate vectors (`derived/replicates.npz`, 161 entries: the full
weight and 160 replicate weights). Nothing is re-estimated from microdata and no
fingerprinted upstream script is touched.

Steps, each gated:

1. Rebuild the 63 admissible cells of `arms_matrix.csv` and the marginality curve
   from the replicate vectors, to the dollar and to the published standard error.
2. Price every switch one at a time against the central cell (the tornado), with
   its source and the class of modeler that runs it.
3. Add the switches the grid does not hold: enforcement charged to the enforced
   with R central (netted, not stacked), the F item split into defense, net
   interest and general government, a measured response on general government,
   cross-state function elasticities on the general-services item, state-local
   interest on general debt treated like federal interest, a within-district
   school response on the K-12 capital and district items, and corporate tax
   borne by consumers.
4. Assemble the named cells, the practitioner hull, the design hull and the
   second object (public goods per capita), with the gross flows behind the net.

Standard errors use the ledger's own rule, 4/160 x sum of squared replicate
deviations, applied to the same replicate vectors, so a cell's SE and a
difference's SE are both exact for the survey part of the uncertainty. They say
nothing about the conventions, which is the point of the exercise.

Run from the repository root:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ledger_recut_2026_09_22/recut.py
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
LEDGER = FISCAL / "ledger_absolute_2026_09_17"
SCALING = FISCAL / "scaling_test_2026_09_20"
COG_XLSX = FISCAL / "ledger_residual_agg_2026_09_16" / "_cache" / "22slsstab1.xlsx"

UNION = "mexican_observed_total"
BN = 1e9

# Central arms of the pinned September 19 build (audit.json `central_arms`).
CENTRAL = {"G": "deflated2024", "K": "central", "P": "net_of_item_G", "D": "central",
           "U": "central", "I": "central", "M": "central", "E": "zero",
           "C": "wage25_capital75", "X": "per_capita", "R": "central", "F": "zero",
           "S": "all_inside_meps"}
GRID_ITEMS = ("F", "E", "C", "R")
DIALLED = ("G", "K", "P", "D", "F")            # plus the per-capita part of R

# 2022 Census of Governments Table 1, US total column, functional lines 69..112.
# Item G is line 66 less education (69), public welfare (77), hospitals (81),
# health (83) and correction (94); every other functional line stays inside G.
COG_EXCLUDED = {69: "education", 77: "public welfare", 81: "hospitals", 83: "health",
                94: "correction"}
COG_RETAINED = {
    76: "libraries", 84: "employment security administration", 85: "veterans' services",
    86: "highways", 88: "air transportation", 89: "parking facilities",
    90: "sea and inland port facilities", 92: "police protection", 93: "fire protection",
    96: "protective inspection and regulation", 97: "natural resources",
    99: "parks and recreation", 101: "housing and community development",
    102: "sewerage", 104: "solid waste management", 106: "financial administration",
    107: "judicial and legal", 108: "general public buildings",
    109: "other governmental administration", 110: "interest on general debt",
    111: "miscellaneous commercial activities", 112: "other and unallocable",
}
# Scaling-test function -> Census lines it measures (state_analyze.py FUNCTIONS).
ELASTICITY_LINES = {"police": [92], "fire": [93], "highways_nontoll": [86],
                    "parks": [99], "libraries": [76], "admin": [106, 108, 109]}
COG_LINE_INTEREST = 110


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def se_of(v: np.ndarray) -> float:
    """The ledger's replicate rule: 4/160 x sum over the 160 replicates."""
    return float(np.sqrt(4.0 / 160.0 * np.sum((v[1:] - v[0]) ** 2)))


def cell(v: np.ndarray) -> dict:
    return dict(union_absolute_bn=v[0] / BN, se_bn=se_of(v) / BN)


class Ledger:
    """Published replicate vectors of the pinned ledger, by item and arm."""

    def __init__(self, derived: Path):
        self.derived = derived
        self.z = np.load(derived / "replicates.npz")
        self.audit = json.loads((derived / "audit.json").read_text())
        self.items = pd.read_csv(derived / "items_by_group.csv")
        self.arms = pd.read_csv(derived / "arms_matrix.csv")
        self.curve = pd.read_csv(derived / "marginality_curve.csv")
        self.profiles = pd.read_csv(derived / "age_profiles.csv")
        self.components = pd.read_csv(derived / "age_profile_components.csv")
        if self.audit["central_arms"] != CENTRAL:
            raise SystemExit(f"[BLOCKED] central arms moved: {self.audit['central_arms']}")
        if self.audit["items_switched_off"]:
            raise SystemExit("[BLOCKED] the published ledger run has items switched off")
        n_row = self.items[(self.items.item == "N") & (self.items.group == UNION)]
        if len(n_row) != 1 or not bool(n_row.external.iloc[0]):
            raise SystemExit("[BLOCKED] item N is not the single external add expected")
        self.n_external = float(n_row.total_bn.iloc[0]) * BN   # scalar, no replicates

    def rep(self, item: str, arm: str) -> np.ndarray:
        key = f"{item}|{arm}|{UNION}"
        if key not in self.z:
            raise SystemExit(f"[BLOCKED] replicate vector missing: {key}")
        return self.z[key].astype(float)

    @property
    def base(self) -> np.ndarray:
        return self.z[f"base|{UNION}"].astype(float)

    def meta(self, item: str, arm: str) -> dict:
        return self.audit["item_metadata"][f"{item}|{arm}"]

    def fixed_non_grid(self) -> np.ndarray:
        """base + every central non-F/E/C/R item, N as a scalar (the builder's `fixed`)."""
        v = self.base.copy()
        for item, arm in CENTRAL.items():
            if item in GRID_ITEMS:
                continue
            v = v + self.rep(item, arm)
        return v + self.n_external

    def grid_cell(self, fa: str, ea: str, ca: str, ra: str) -> np.ndarray:
        return (self.fixed_non_grid() + self.rep("F", fa) + self.rep("E", ea)
                + self.rep("C", ca) + self.rep("R", ra))

    def central(self) -> np.ndarray:
        return self.grid_cell(*(CENTRAL[i] for i in GRID_ITEMS))

    def marginal_and_fixed(self) -> tuple[np.ndarray, np.ndarray]:
        """The builder's dial: G, K, P, D, F and the per-capita part of R move with m."""
        marginal = np.zeros(161)
        fixed = self.base.copy() + self.n_external
        for item, arm in CENTRAL.items():
            vec = self.rep(item, arm)
            if item == "R":
                part = self.rep("R", "central_marginal_part")
                marginal = marginal + part
                fixed = fixed + (vec - part)
            elif item in DIALLED:
                marginal = marginal + vec
            else:
                fixed = fixed + vec
        return marginal, fixed


def read_cog_composition() -> pd.DataFrame:
    """National composition of item G by Census function, 2022 dollars."""
    import openpyxl
    if not COG_XLSX.exists():
        raise SystemExit(f"[BLOCKED] Census of Governments cache missing: {COG_XLSX}")
    ws = openpyxl.load_workbook(COG_XLSX, read_only=True, data_only=True)["2022_US_WY"]
    rows = [[("" if c is None else c) for c in r] for r in ws.iter_rows(values_only=True)]
    by_line = {int(r[0]): r for r in rows if isinstance(r[0], (int, float)) and r[0]}
    if str(rows[8][2]).strip() != "United States Total":
        raise SystemExit("[BLOCKED] Census table layout changed: US total not in column 2")

    def amount(line: int) -> float:
        v = by_line[line][2]
        if not isinstance(v, (int, float)):
            raise SystemExit(f"[BLOCKED] Census line {line} has no US total")
        return float(v) * 1000.0

    residual = amount(66) - sum(amount(ln) for ln in COG_EXCLUDED)
    retained = {ln: amount(ln) for ln in COG_RETAINED}
    total = sum(retained.values())
    if abs(total - residual) / residual > 5e-4:
        raise SystemExit(f"[BLOCKED] retained functional lines {total:,.0f} do not "
                         f"reproduce line 66 less the five excluded functions {residual:,.0f}")
    comp = pd.DataFrame([dict(line=ln, function=COG_RETAINED[ln], dollars_2022=d,
                              share=d / total) for ln, d in retained.items()])
    return comp


def read_elasticities() -> dict:
    est = pd.read_csv(SCALING / "derived" / "state" / "estimates.csv")
    est = est[(est.model == "year_fe") & (est["sample"] == "all")].set_index("function")
    out = {}
    for fn in ELASTICITY_LINES:
        if fn not in est.index:
            raise SystemExit(f"[BLOCKED] scaling-test estimate missing for {fn}")
        out[fn] = dict(beta=float(est.loc[fn, "beta"]),
                       se=float(est.loc[fn, "se_cluster_state_CR1"]),
                       ci_low=float(est.loc[fn, "ci_low"]), ci_high=float(est.loc[fn, "ci_high"]))
    school = pd.read_csv(SCALING / "derived" / "school_estimates.csv")
    sch = school[(school["sample"] == "existing_screen") & (school.outcome == "log_current")
                 & (school.spec == "within_district_state_year")]
    if len(sch) != 2:
        raise SystemExit("[BLOCKED] expected two within-district school rows (weighted, unweighted)")
    for _, r in sch.iterrows():
        tag = "school_within_pupil_weighted" if bool(r.weighted) else "school_within_unweighted"
        out[tag] = dict(beta=float(r.beta), se=float(r.se), ci_low=float(r.low95),
                        ci_high=float(r.high95))
    return out


def read_params() -> dict:
    p = json.loads((LEDGER / "params" / "params.json").read_text())

    def val(group: str, key: str) -> float:
        e = p[group][key]
        if e.get("status") != "verified":
            raise SystemExit(f"[BLOCKED] parameter {group}/{key} not verified")
        return float(e["value"])
    return dict(defense=val("omb", "func_050_national_defense") * 1e6,
                net_interest=val("omb", "func_900_net_interest") * 1e6,
                general_government=val("omb", "func_800_general_government") * 1e6)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = ap.parse_args()
    out: Path = args.out_dir
    out.mkdir(parents=True, exist_ok=True)

    L = Ledger(LEDGER / "derived")
    gates: dict[str, dict] = {}

    # ---- 1. reproduce the published grid and curve ---------------------------
    worst_value = worst_se = 0.0
    for _, r in L.arms.iterrows():
        v = L.grid_cell(r.F_arm, r.E_arm, r.C_arm, r.R_arm)
        worst_value = max(worst_value, abs(v[0] / BN - r.union_absolute_bn))
        worst_se = max(worst_se, abs(se_of(v) / BN - r.se_bn))
    inadmissible = sum(1 for _, r in L.arms.iterrows() if r.E_arm != "zero" and r.R_arm != "all_zero")
    gates["grid_reproduced"] = dict(cells=int(len(L.arms)), worst_abs_diff_bn=worst_value,
                                    worst_se_diff_bn=worst_se, inadmissible_rows=inadmissible,
                                    passed=len(L.arms) == 63 and worst_value < 1e-6
                                    and worst_se < 1e-6 and inadmissible == 0)
    marginal, fixed = L.marginal_and_fixed()
    m_star = float(-fixed[0] / marginal[0])
    worst_curve = 0.0
    for _, r in L.curve.iterrows():
        v = fixed + r.m * marginal
        worst_curve = max(worst_curve, abs(v[0] / BN - r.union_absolute_bn),
                          abs(se_of(v) / BN - r.se_bn))
    gates["curve_reproduced"] = dict(points=int(len(L.curve)), worst_abs_diff_bn=worst_curve,
                                     m_star=m_star, published_m_star=float(L.curve.break_even_m_star.iloc[0]),
                                     passed=worst_curve < 1e-6
                                     and abs(m_star - float(L.curve.break_even_m_star.iloc[0])) < 1e-9)
    central = L.central()
    gates["central_is_grid_cell"] = dict(value_bn=central[0] / BN,
                                         passed=abs(central[0] / BN - float(L.arms[
                                             (L.arms.F_arm == "zero") & (L.arms.E_arm == "zero")
                                             & (L.arms.C_arm == "wage25_capital75")
                                             & (L.arms.R_arm == "central")].union_absolute_bn.iloc[0])) < 1e-9)
    for name, g in gates.items():
        print(f"[gate] {name}: {'PASS' if g['passed'] else 'FAIL'} {json.dumps({k: v for k, v in g.items() if k != 'passed'})}")
        if not g["passed"]:
            raise SystemExit(f"[BLOCKED] gate failed: {name}")

    # ---- 2. carriers for the new switches ----------------------------------
    x_pc = L.rep("X", "per_capita")
    x_nat = float(L.meta("X", "per_capita")["national_dollars"])
    share = x_pc / x_nat                       # the union's headcount share, replicate by replicate
    pop_ratio = float(L.audit["civilian_household_population"]) / float(L.audit["us_resident_population"])
    gates["headcount_share_carrier"] = dict(
        share_full=float(share[0]), expected=float(L.profiles[(L.profiles.allocation == "shared")
                                                              & (L.profiles.account == "expanded")
                                                              & (L.profiles.group == UNION)].population.sum())
        / float(L.audit["us_resident_population"]),
        passed=True)
    gates["headcount_share_carrier"]["passed"] = abs(gates["headcount_share_carrier"]["share_full"]
                                                     - gates["headcount_share_carrier"]["expected"]) < 1e-9

    c_nat = float(L.meta("C", "wage25_capital75")["national_dollars"])
    c_consumption = L.rep("X", "consumption_proxy") * (c_nat / x_nat)

    e_stock = L.rep("E", "stock")
    e_nat = float(L.meta("E", "stock")["national_dollars"])
    e_targeted_delta = e_stock + share * e_nat        # charge the Mexico share to the enforced, refund its per-capita slice

    prm = read_params()
    f_pc = L.rep("F", "per_capita")
    f_nat = float(L.meta("F", "per_capita")["national_dollars"])
    tricare = float(L.meta("F", "per_capita")["tricare_already_priced"])
    f_gross = prm["defense"] + prm["net_interest"] + prm["general_government"]
    gates["f_split_reconciles"] = dict(gross=f_gross, tricare=tricare, national=f_nat,
                                       passed=abs(f_gross - tricare - f_nat) < 1.0)
    f_parts = {"defense_net_of_tricare": f_pc * ((prm["defense"] - tricare) / f_nat),
               "net_interest": f_pc * (prm["net_interest"] / f_nat),
               "general_government": f_pc * (prm["general_government"] / f_nat)}

    el = read_elasticities()
    comp = read_cog_composition()
    g_deflated = L.rep("G", "deflated2024")
    deflator = float(L.meta("G", "deflated2024")["deflator"])
    g_gross = L.rep("G", "nominal2022") * deflator      # per-capita gross services, 2024 prices
    g_fees = g_deflated - g_gross                        # mapped user fees credited (positive)
    gates["g_gross_and_fees"] = dict(gross_bn=g_gross[0] / BN, fees_bn=g_fees[0] / BN,
                                     net_bn=g_deflated[0] / BN, passed=g_fees[0] > 0 and g_gross[0] < 0)
    line_to_fn = {ln: fn for fn, lines in ELASTICITY_LINES.items() for ln in lines}
    comp["elasticity_source"] = comp.line.map(lambda ln: line_to_fn.get(ln, "none (held at 1)"))
    comp["elasticity"] = comp.line.map(lambda ln: el[line_to_fn[ln]]["beta"] if ln in line_to_fn else 1.0)
    comp["elasticity_se"] = comp.line.map(lambda ln: el[line_to_fn[ln]]["se"] if ln in line_to_fn else np.nan)
    m_g_functions = float((comp.share * comp.elasticity).sum())
    interest_share = float(comp.loc[comp.line == COG_LINE_INTEREST, "share"].iloc[0])
    m_g_interest_zero = 1.0 - interest_share
    m_g_both = m_g_functions - interest_share
    g_functions_delta = g_gross * (m_g_functions - 1.0)
    g_interest_delta = g_gross * (m_g_interest_zero - 1.0)
    g_both_delta = g_gross * (m_g_both - 1.0)
    comp.to_csv(out / "g_composition.csv", index=False)

    k_rep, d_rep = L.rep("K", "central"), L.rep("D", "central")
    school_w = el["school_within_pupil_weighted"]["beta"]
    school_u = el["school_within_unweighted"]["beta"]
    school_delta_w = (k_rep + d_rep) * (school_w - 1.0)
    school_delta_u = (k_rep + d_rep) * (school_u - 1.0)

    admin_beta = el["admin"]["beta"]
    gg_response_delta = f_parts["general_government"] * admin_beta   # cost, negative

    base_school = float(L.components[(L.components.allocation == "shared") & (L.components.account == "expanded")
                                     & (L.components.group == UNION) & (L.components.component == "school")]
                        .signed_total.sum())
    personal = float(L.profiles[(L.profiles.allocation == "personal") & (L.profiles.account == "expanded")
                                & (L.profiles.group == UNION)].net_total.sum())

    # ---- 3. the tornado: every switch one at a time against the central -----
    def grid_switch(item: str, arm: str) -> np.ndarray:
        arms: dict[str, str] = {i: CENTRAL[i] for i in GRID_ITEMS}
        arms[item] = arm
        if item == "E":
            return L.grid_cell(arms["F"], arm, arms["C"], "all_zero") - L.grid_cell(arms["F"], "zero", arms["C"], "all_zero")
        return L.grid_cell(arms["F"], arms["E"], arms["C"], arms["R"]) - central

    switches = [
        # id, item, label, delta vector, source, who runs it, side, in practitioner set
        ("R_all_zero", "R", "rest of federal budget: all functions zero", grid_switch("R", "all_zero"),
         "ledger arms_matrix", "nobody: zeroes veterans' cash, federal pensions and justice, which are records-based, not public goods",
         "lenient", False),
        ("R_all_per_capita", "R", "rest of federal budget: every netted function per capita, seven zero-in-central functions per capita",
         grid_switch("R", "all_per_capita"), "ledger arms_matrix",
         "average-cost budget shops that spread every non-entitlement federal function per head", "strict", True),
        ("R_housing_by_reported_subsidy", "R", "housing assistance (604) by reported SPM housing subsidy instead of per capita",
         grid_switch("R", "central_housing_by_reported_subsidy"), "ledger arms_matrix",
         "records-based allocation of one subfunction; a refinement of the central", "strict", True),
        ("C_all_capital", "C", "corporate income tax 100% to capital income", grid_switch("C", "all_capital"),
         "ledger arms_matrix", "the older incidence convention; still a defended arm", "strict", True),
        ("C_per_capita", "C", "corporate income tax per capita", grid_switch("C", "per_capita"),
         "ledger arms_matrix", "nobody: headcount is not an incidence theory", "lenient", False),
        ("C_consumption", "C", "corporate income tax proportional to the consumption proxy (borne by consumers)",
         c_consumption - L.rep("C", "wage25_capital75"), "this lane: C national x union consumption share from item X",
         "minority incidence view used in some state tax-incidence studies; disclosed, outside the set", "lenient", False),
        ("F_per_capita", "F", "defense, net interest and general government per capita",
         grid_switch("F", "per_capita"), "ledger arms_matrix",
         "the average-cost public-goods scenario; a different object (assigned share of fixed federal costs), reported separately",
         "strict", False),
        ("F_proportional_to_federal_tax", "F", "defense, net interest and general government in proportion to federal taxes paid",
         grid_switch("F", "proportional_to_federal_tax"), "ledger arms_matrix",
         "benefit-principle variant of the same second object", "strict", False),
        ("F_defense_per_capita", "F", "defense only, net of TRICARE, per capita", f_parts["defense_net_of_tricare"],
         "this lane: F per capita x OMB 050 share", "part of the second object", "strict", False),
        ("F_net_interest_per_capita", "F", "net interest only, per capita", f_parts["net_interest"],
         "this lane: F per capita x OMB 900 share", "part of the second object", "strict", False),
        ("F_general_government_per_capita", "F", "federal general government (function 800) only, per capita",
         f_parts["general_government"], "this lane: F per capita x OMB 800 share", "average-cost treatment of the smallest F part",
         "strict", False),
        ("F_general_government_response", "F", f"federal general government at the cross-state administration elasticity {admin_beta:.3f}",
         gg_response_delta, "this lane: F(800) per capita x scaling-test admin elasticity (year effects)",
         "the measured-response arm the repo proposes for the complete account; small here because state-local administration sits inside G",
         "strict", True),
        ("E_stock_only_with_R_zero", "E", "enforcement (ICE ERO, EOIR, appropriated USCIS) x Mexico share, only admissible with R all zero",
         grid_switch("E", "stock"), "ledger arms_matrix", "CIS-style targeted enforcement charge; the grid admits it only when federal justice is zeroed",
         "strict", False),
        ("E_stock_plus_flow_only_with_R_zero", "E", "enforcement plus Border Patrol x Mexico share of encounters, only admissible with R all zero",
         grid_switch("E", "stock_plus_flow"), "ledger arms_matrix", "same, with the border flow", "strict", False),
        ("E_targeted_with_R_central", "E", "enforcement (Mexico share) charged to Mexico-born noncitizens and removed from the per-capita justice charge",
         e_targeted_delta, "this lane: E stock less the union's headcount slice of the same dollars",
         "the netted version of the CIS arm; the cell the admissibility rule removed", "strict", True),
        ("G_function_elasticities", "G", f"general services at cross-state function elasticities (police {el['police']['beta']:.3f}, fire {el['fire']['beta']:.3f}, highways {el['highways_nontoll']['beta']:.3f}, parks {el['parks']['beta']:.3f}, libraries {el['libraries']['beta']:.3f}, administration {admin_beta:.3f}; other functions held at 1)",
         g_functions_delta, "this lane: G gross x national function shares x scaling-test year-effect elasticities",
         "a modeler who lets service budgets follow the measured cross-state size gradient; descriptive, not causal (2026-09-20 decision)",
         "lenient", True),
        ("G_interest_like_federal", "G", "state-local interest on general debt at zero, the convention item F already applies to federal interest",
         g_interest_delta, "this lane: G gross x Census line 110 share",
         "consistency arm: legacy interest is fixed at both levels or at neither", "lenient", True),
        ("K_D_school_within_pupil_weighted", "K,D", f"K-12 capital, school-debt interest and district differential at the within-district pupil-weighted school elasticity {school_w:.3f}",
         school_delta_w, "this lane: (K + D) x scaling-test within-district elasticity",
         "the CBO-type school response applied to the school items this ledger holds on its dial", "lenient", True),
        ("K_D_school_within_unweighted", "K,D", f"same at the unweighted within-district elasticity {school_u:.3f}",
         school_delta_u, "this lane: (K + D) x scaling-test within-district elasticity", "same, lower bound", "lenient", False),
    ]
    tornado = pd.DataFrame([dict(id=i, item=it, label=lb, delta_bn=v[0] / BN, se_bn=se_of(v) / BN,
                                 cell_bn=(central[0] + v[0]) / BN, source=src, who_runs_it=who, side=side,
                                 in_practitioner_set=ok) for i, it, lb, v, src, who, side, ok in switches])
    tornado.to_csv(out / "switch_moves.csv", index=False)

    # ---- 4. named cells ------------------------------------------------------
    pess_grid = L.grid_cell("zero", "zero", "all_capital", "all_per_capita")
    pess_full = pess_grid + e_targeted_delta + gg_response_delta
    opt_full = central + g_both_delta + school_delta_w
    opt_functions_only = central + g_functions_delta + school_delta_w
    m63 = fixed + 0.63 * marginal
    m66 = fixed + 0.66 * marginal
    m0 = fixed.copy()
    wishful = L.grid_cell("zero", "zero", "per_capita", "all_zero")
    stacked = L.grid_cell("per_capita", "zero", "all_capital", "all_per_capita")
    f_on_central = L.grid_cell("per_capita", "zero", "wage25_capital75", "central")
    f_tax_on_central = L.grid_cell("proportional_to_federal_tax", "zero", "wage25_capital75", "central")

    named = [
        ("central", "F 0, E 0 (inside R750), C 25/75, R central; D and P on", central, "grid", "central"),
        ("practitioner_pessimistic_grid", "R all per capita, C all capital (grid cell)", pess_grid, "grid", "strict bound, grid part"),
        ("practitioner_pessimistic", "R all per capita, C all capital, enforcement targeted (netted), federal general government at the administration elasticity",
         pess_full, "grid + this lane", "strict bound of the practitioner set"),
        ("practitioner_optimistic_functions_only", "central with G at cross-state function elasticities and K, D at the within-district school elasticity",
         opt_functions_only, "this lane", "lenient bound without the interest consistency arm"),
        ("practitioner_optimistic", "central with G at cross-state function elasticities, state-local interest at zero like federal interest, K and D at the within-district school elasticity",
         opt_full, "this lane", "lenient bound of the practitioner set"),
        ("stretch_school_m_0_63_on_all_dialled", "m = 0.63 on G, K, P, D and the per-capita part of R (the school coefficient applied to police, fire, highways and federal functions)",
         m63, "marginality curve", "disclosed stretch, outside the set"),
        ("stretch_school_m_0_66_on_all_dialled", "m = 0.66 on the same", m66, "marginality curve", "disclosed stretch, outside the set"),
        ("wishful_corner", "R all zero, C per capita (least negative grid cell)", wishful, "grid", "dropped: two arms nobody runs"),
        ("no_congestible_services", "m = 0: taxes and transfers only, every dialled service free", m0, "marginality curve", "dropped: the convention commentators use, not a modeler's"),
        ("second_object_public_goods_on_central", "F per capita on the central", f_on_central, "grid", "second object: assigned share of fixed federal costs"),
        ("second_object_public_goods_by_federal_tax", "F in proportion to federal taxes paid, on the central", f_tax_on_central, "grid", "second object, benefit-principle variant"),
        ("second_object_stacked_corner", "F per capita on the pessimistic grid cell (most negative grid cell)", stacked, "grid", "second object, strict corner"),
    ]
    cells = pd.DataFrame([dict(id=i, definition=d, **cell(v), source=s, role=r) for i, d, v, s, r in named])
    # two point-only rows: base school spending has no saved replicates
    cells = pd.concat([cells, pd.DataFrame([
        dict(id="stretch_plus_cbo_school_on_base_school", definition="m = 0.63 on all dialled items plus 0.63 on base school current spending, which is not on the dial",
             union_absolute_bn=(m63[0] + (1 - 0.63) * (-base_school)) / BN, se_bn=np.nan, source="marginality curve + age_profile_components",
             role="disclosed stretch, point only: base school replicates are not saved"),
        dict(id="personal_source_allocation", definition="the same account under the personal-source allocation (published)",
             union_absolute_bn=personal / BN, se_bn=np.nan, source="age_profiles.csv", role="orientation: a different allocation of the same account, not a switch"),
    ])], ignore_index=True)
    cells.to_csv(out / "named_cells.csv", index=False)

    hulls = pd.DataFrame([
        dict(hull="practitioner", low_bn=pess_full[0] / BN, high_bn=opt_full[0] / BN, central_bn=central[0] / BN,
             members="strict: R all per capita, C all capital, E targeted (netted), F general government at the admin elasticity; lenient: G at cross-state function elasticities, state-local interest like federal interest, K and D at the within-district school elasticity",
             note="conventions a named class of modeler runs; not a confidence interval"),
        dict(hull="design_grid", low_bn=float(L.arms.union_absolute_bn.min()), high_bn=float(L.arms.union_absolute_bn.max()), central_bn=central[0] / BN,
             members="all 63 admissible F x E x C x R cells", note="hull of the switch design, grows with every arm added"),
        dict(hull="design_with_dial", low_bn=min(float(L.arms.union_absolute_bn.min()), stacked[0] / BN), high_bn=m0[0] / BN, central_bn=central[0] / BN,
             members="the grid plus the marginality dial from 0 to 1", note="the widest thing the lane can produce; +41 is taxes and transfers only"),
        dict(hull="second_object_public_goods", low_bn=(pess_full + f_pc)[0] / BN, high_bn=(opt_full + f_pc)[0] / BN, central_bn=f_on_central[0] / BN,
             members="the practitioner hull with F per capita added", note="assigned share of defense, net interest and general government; a different question"),
    ])
    hulls.to_csv(out / "hulls.csv", index=False)

    comp_u = L.components[(L.components.allocation == "shared") & (L.components.account == "expanded") & (L.components.group == UNION)]
    by_component = comp_u.groupby("component").signed_total.sum() / BN
    receipts = float(by_component[by_component > 0].sum())
    outlays = float(by_component[by_component < 0].sum())
    flows = pd.DataFrame([dict(line="gross receipts", bn=receipts), dict(line="gross outlays", bn=outlays),
                          dict(line="net", bn=receipts + outlays),
                          dict(line="20% of gross outlays", bn=0.2 * abs(outlays)),
                          dict(line="20% of gross receipts", bn=0.2 * receipts),
                          dict(line="20% of the net", bn=0.2 * abs(receipts + outlays)),
                          dict(line="replicate standard error of the central", bn=se_of(central) / BN)])
    flows.to_csv(out / "gross_flows.csv", index=False)
    gates["gross_flows_reproduce_central"] = dict(net_bn=receipts + outlays, central_bn=central[0] / BN,
                                                  passed=abs(receipts + outlays - central[0] / BN) < 1e-6)
    gates["practitioner_hull_ordered"] = dict(low=pess_full[0] / BN, central=central[0] / BN, high=opt_full[0] / BN,
                                              passed=pess_full[0] < central[0] < opt_full[0] < 0)
    gates["stretch_outside_hull"] = dict(passed=m63[0] > opt_full[0] and wishful[0] > opt_full[0])
    for name in ("headcount_share_carrier", "f_split_reconciles", "g_gross_and_fees",
                 "gross_flows_reproduce_central", "practitioner_hull_ordered", "stretch_outside_hull"):
        g = gates[name]
        print(f"[gate] {name}: {'PASS' if g['passed'] else 'FAIL'} {json.dumps({k: v for k, v in g.items() if k != 'passed'})}")
        if not g["passed"]:
            raise SystemExit(f"[BLOCKED] gate failed: {name}")

    audit = dict(
        object="ledger_absolute_2026_09_17, Mexican-origin union, income-year 2024, household-shared allocation, expanded partial account",
        ledger_build_params_sha256=L.audit["params_sha256"],
        inputs={str(p.relative_to(ROOT)): sha256(p) for p in [
            LEDGER / "derived" / "replicates.npz", LEDGER / "derived" / "arms_matrix.csv",
            LEDGER / "derived" / "marginality_curve.csv", LEDGER / "derived" / "items_by_group.csv",
            LEDGER / "derived" / "audit.json", LEDGER / "derived" / "age_profiles.csv",
            LEDGER / "derived" / "age_profile_components.csv", LEDGER / "params" / "params.json",
            SCALING / "derived" / "state" / "estimates.csv", SCALING / "derived" / "school_estimates.csv",
            COG_XLSX]},
        gates=gates,
        elasticities=el,
        g_dial=dict(m_functions=m_g_functions, interest_share=interest_share, m_interest_zero=m_g_interest_zero,
                    m_both=m_g_both, composition="national 2022 Census of Governments shares, not the union's state mix"),
        f_split_dollars=dict(defense=prm["defense"], tricare_netted=tricare, net_interest=prm["net_interest"],
                             general_government=prm["general_government"]),
        e_targeted=dict(mexico_share_dollars=e_nat, union_headcount_share=float(share[0]),
                        delta_bn=e_targeted_delta[0] / BN),
        base_school_shared_bn=base_school / BN,
        pop_ratio_civilian_household_to_resident=pop_ratio,
        interpretation="convention hulls over a published accounting scenario; not a confidence interval, not a marginal immigration effect",
    )
    (out / "audit.json").write_text(json.dumps(audit, indent=2, default=float))

    print()
    print(cells[["id", "union_absolute_bn", "se_bn"]].to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print()
    print(hulls[["hull", "low_bn", "central_bn", "high_bn"]].to_string(index=False, float_format=lambda x: f"{x:,.1f}"))
    print()
    print(tornado[["id", "delta_bn", "se_bn", "in_practitioner_set"]].to_string(index=False, float_format=lambda x: f"{x:,.2f}"))
    print(f"\nwritten to {out}")


if __name__ == "__main__":
    sys.exit(main())
