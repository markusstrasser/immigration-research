"""Brief part B: what the group values the US budget's services and transfers at, next to what they cost other
residents, line by line, and what Mexico's budget would have spent on the same people.

Five columns per line, never merged (brief correction 1): G, the resource cost to other residents (the line's
effect in the account); V, the group's valuation; third-party value; fiscal feedback F; net cost. V/G is applied
to the account's gross lines only; no MVPF is used as a value per dollar.

Value basis (a judgment call per class, stated in CLASSES):
- rival transfers and services: V = (V/G) x effect, since only what the group's presence adds is theirs;
- public goods and general services: V = the group's attributed amount at average cost (the brief's
  convention), whatever the response, since a non-rival good costs others only its response;
- schooling: V = 0 on this side. Its investment return is inside the second generation's place premium
  (g2_premium.py), and its custodial value exists in both places. Stationary-flow argument: today's school
  spending on today's pupils stands in for past spending on today's adults, whose premium is counted. The group's
  pupil cohort is larger than the cohorts now of working age, so today's spending overstates the past spending
  behind today's premium; the bias is against the group.
- offender processing and enforcement: V = 0 for the group.
Third-party value: Finkelstein-Hendren-Luttmer's external transfer, about $0.60 per $1 of Medicaid, exists only
against a US-uninsured alternative (uncompensated care the group would otherwise have received in the US).
Against the Mexico alternative there is no US implicit insurance, so it is zero there; it is reported for
reference. Fiscal feedback: 0 per line; the account's receipts are observed and already contain it. The
account's induced receipts F are a separate row in world_ledger.py.

By generation: the generation lane's own split of the same lines (generation_lines.cjs: its models and payloads,
convention (a), each person in their own generation, evaluated at the case's band-end specifications) is valued
line by line with the same classes. Gates: the three generations add to the case's lines, line by line, and each
generation's net cost plus its production term equals generation_results.csv, to 1e-6.

Inputs are read at pinned commits (PINS), so peers' uncommitted reruns never leak in.
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/valuation.py
Every case with pins is valued. Outputs: derived/valuation.csv, derived/valuation_by_class.csv,
derived/valuation_by_generation.csv and derived/valuation_meta.json (one block per case of SHARED_OUTPUTS; each
later case writes the same four files with a _<case> suffix), derived/mexico_budget.csv,
derived/mexico_budget_row4.csv and derived/mexico_budget_lineage.csv (case-independent; the group on the cps, row4
and lineage population bases, population_basis.py).
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from population_basis import BASES, suffixed

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
FISCAL_REL = "infra/immigration-fiscal"
# Pinned inputs per case (pins.json, shared with world_ledger.py): the commits holding each case's files.
PINS = {k: v for k, v in json.load(open(HERE / "pins.json")).items() if not k.startswith("_")}
# Where each pinned lane keeps a case's files: its derived/ under the default case's names, unless the case's pins
# name another directory ("dirs") or rename a file ("files": lane -> {default name: the case's name}). From sept29 the
# lanes write the case beside their default case's files, in a subdirectory or under a _<case> name.
# split_residual.py and world_ledger.py import lane_file; generation_lines.cjs reads the same two entries.
LANE_DIRS = {"winners": f"{FISCAL_REL}/winners_losers_2026_09_24/derived",
             "distribution": f"{FISCAL_REL}/distribution_weights_2026_09_23/derived",
             "generation": f"{FISCAL_REL}/generation_account_2026_09_24/derived"}
for _case, _pin in PINS.items():
    _unknown = (set(_pin.get("dirs", {})) | set(_pin.get("files", {}))) - set(LANE_DIRS)
    if _unknown:          # a misspelt lane would silently read the default case's file at the new pin
        raise SystemExit(f"[BLOCKED] pins.json {_case}: unknown lanes {sorted(_unknown)} in dirs or files")
    if _pin.get("basis", "cps") not in BASES:
        raise SystemExit(f"[BLOCKED] pins.json {_case}: unknown basis {_pin['basis']!r}")


def basis_of(case):
    """The population a case's person-based rows are counted on (population_basis.py): its pins' "basis", else cps."""
    return PINS[case].get("basis", "cps")


def lane_file(case, lane, name):
    """A pinned lane's file for a case, as a path in the repository (read at the case's pin for that lane)."""
    pin = PINS[case]
    return f"{pin.get('dirs', {}).get(lane, LANE_DIRS[lane])}/{pin.get('files', {}).get(lane, {}).get(name, name)}"


# Cases whose rows share the lane's multi-case files (valuation*.csv, valuation_meta.json, world_ledger.csv,
# world_ledger_rows.csv, generation_split_check.csv), as tracked. Every later case writes the same files with a
# _<case> suffix, so adding a case leaves those files byte for byte (the v4 consumer brief, 2026-09-29).
# world_ledger.py imports case_path, so both scripts read one definition.
SHARED_OUTPUTS = ("sept26_schools", "sept27")


def case_path(name, case, basis=None):
    """Where a multi-case output holds a case: the shared file, or <stem>_<case><suffix> for a later case. A case
    run on the other population basis beside its own (world_ledger.py --basis) writes <stem>_<case>_<basis>."""
    p = DERIVED / name
    if basis is not None and basis != basis_of(case):
        return p.with_name(f"{p.stem}_{case}_{basis}{p.suffix}")
    return p if case in SHARED_OUTPUTS else p.with_name(f"{p.stem}_{case}{p.suffix}")


# Justice use by component, central split (cj_use_allocation_2026_09_23/derived/central_split.csv, use_bn):
# protection is fire, the per-head half of non-border police, civil courts and CBP; offender processing and
# enforcement is prisons, the arrest-keyed half of police, criminal courts (the unsplit part of law courts) and ICE.
JUSTICE = dict(fire=9.640327, police_per_head=27.540691 - 14.873448, civil_courts=10.649463 - 6.792708,
               cbp=2.870475, prisons=17.216835, police_arrest=14.873448, criminal_courts=6.792708,
               ice=0.214229 + 0.237015)
PROTECTION = ("fire", "police_per_head", "civil_courts", "cbp")
PROTECTION_SHARE = sum(JUSTICE[k] for k in PROTECTION) / sum(JUSTICE.values())
# The same split function by function, for the public-order state-price gap, whose mix of functions is not the
# line's (the lead, 2026-09-29): fire is all protection; police, and protective inspection with it (NIPA's POS has no
# subline for inspection, and the state-pricing lane reads it inside police), take police's per-head share; the courts
# their civil share; state prisons are offender processing.
_POLICE_PER_HEAD = JUSTICE["police_per_head"] / (JUSTICE["police_per_head"] + JUSTICE["police_arrest"])
JUSTICE_FUNCTION_SHARE = {"fire": 1.0, "police": _POLICE_PER_HEAD, "protective_inspection": _POLICE_PER_HEAD,
                          "judicial": JUSTICE["civil_courts"] / (JUSTICE["civil_courts"] + JUSTICE["criminal_courts"]),
                          "corrections_per_inmate": 0.0}

# class: (basis, V/G low, central, high, source). basis 'effect' values what the group's presence adds,
# 'amount' values the attributed amount at average cost, 'none' values nothing.
CLASSES = {
    "cash": ("effect", 1.0, 1.0, 1.0, "envelope theorem on observed flows: 'individuals are willing to pay for the "
             "mechanical cost' (HSK 2020 p.20); behavioral costs are already in observed earnings [INFERENCE]"),
    "snap": ("effect", 0.65, 1.0, 1.0, "low: Whitmore (2002) trade value 'at least 65%' (HSK fn 38); central/high: "
             "inframarginal, cash-equivalent [INFERENCE]"),
    "housing_voucher": ("effect", 0.83, 1.0, 1.0, "HSK Table II: HCV Chicago Lottery WTP 0.83, HCV RCT to Welfare 1.00 "
                        "per $1"),
    "medicaid": ("effect", 0.76, 0.92, 1.08, "FHL JPE 2019 (author manuscript): willingness to pay if the uninsured "
                 "had no implicit insurance, $2,749-3,875 per G = $3,600 (0.76-1.08), the midpoint central; their "
                 "(gamma + 0.6G)/G bridge gives 0.8-1.1. The Mexico alternative has no US implicit insurance "
                 "[INFERENCE on the bridge]"),
    "medicare": ("effect", 1.0, 1.0, 1.0, "convention at cost; HSK's Medicare Intro WTP 2.00 per $1 includes insurance "
                 "value and is not used [INFERENCE]"),
    "health_services": ("effect", 1.0, 1.0, 1.0, "public health and hospitals at cost (convention)"),
    "services": ("effect", 1.0, 1.0, 1.0, "social services at cost (convention)"),
    "education": ("none", 0.0, 0.0, 0.0, "investment; its return is in the G2 premium; custodial value in both places"),
    "public_good": ("amount", 1.0, 1.0, 1.0, "average cost, the brief's convention for public goods and general "
                    "services [FRAMING-SENSITIVE]"),
    "justice": ("split", None, None, None, f"protection share {PROTECTION_SHARE:.4f} at average cost, the rest "
                "(offender processing, enforcement) at 0; cj_use_allocation central split"),
    "not_a_service": ("none", 0.0, 0.0, 0.0, "interest, business subsidies, foreign lines: no service to the group"),
    "correction": ("none", 0.0, 0.0, 0.0, "account correction rows (care-work taxes, shelter, audit constants)"),
}
LINES = {
    "cash": ["social_security", "ssi", "unemployment", "refundable_tax_credits", "family_and_general_assistance",
             "veterans_pension_disability", "veterans_readjustment", "veterans_life_insurance", "railroad_retirement",
             "workers_compensation", "temporary_disability", "other_federal_benefits", "other_state_benefits",
             "pension_guaranty", "black_lung", "energy_assistance", "other_state_welfare"],
    "snap": ["snap"],
    "housing_voucher": ["housing_subsidies"],
    "medicaid": ["medicaid_and_chip_other_medical"],
    "medicare": ["medicare"],
    "health_services": ["health_services", "military_medical", "veterans_other", "state_price_health_services"],
    "services": ["income_security_services"],
    "education": ["education_services", "school_reprice", "college_rekey", "education_benefits",
                  "employment_training"],
    "public_good": ["general_public_services", "defense", "economic_affairs_services", "recreation_culture",
                    "housing_community_services", "roads_vmt_sl", "roads_vmt_fed", "state_price_recreation_culture"],
    "justice": ["public_order_safety", "state_price_public_order_safety"],
    "not_a_service": ["domestic_interest", "foreign_interest", "agricultural_subsidies", "other_subsidies",
                      "transport_subsidies", "foreign_territory_social_benefits", "other_foreign_current_transfers"],
    "correction": ["lane_constants", "source_rounding"],
}
# The sept29 case's synthetic lines (main_case_candidate_v4_2026_09_29 payload `lines`), classed before any sept29
# number was seen: each re-keys or re-prices part of one parent line and takes the parent's class, as school_reprice
# and college_rekey take education's. roads_vmt_sl / roads_vmt_fed move the S&L and federal highway parts of
# economic_affairs_services to the road key (vehicle miles and freight), a change in the quantity attributed to the
# group, so public goods at average cost. state_price_<parent> is the parent's gap between the price where the group
# lives and the national price. The lead's ruling (2026-09-29): only the gap's quantity part is valued, at the
# parent's class; its wage part buys the group the same service at a higher price and is worth 0 to it.
# value_line multiplies such a line's value by its quantity share (state_price_quantity.py, from the state-pricing
# lane's wage demarcation), with justice's class applied function by function (JUSTICE_FUNCTION_SHARE). The two
# extremes, the parent's class on the whole gap and V = 0, are reported beside it in RESULT.md and in the case's
# valuation_meta (state_price_value_bn).
STATE_PRICE_LINES = ("state_price_public_order_safety", "state_price_health_services",
                     "state_price_recreation_culture")
# Receipts are taxes the group pays, which it loses at $1 per $1 ('tax'), except a negative receipt that pays for a
# service to the group. From sept29 public housing's enterprise deficit is its own receipt line at the rental line's
# key: below-market rent to public-housing tenants, valued as a housing voucher like rental assistance and the return
# on public housing's capital (ent_housing_sl); the lead accepted it on 2026-09-29. The alternative, $1 per $1 as the
# enterprise_surplus receipt that held it before, is reported beside it in RESULT.md.
RECEIPT_CLASS = {"housing_enterprise_surplus": "housing_voucher"}
# The Sept 27 case's return on public capital, by component of main_case_long_run_2026_09_27's
# meta.capital_return (f3031ab), classed before any sept27 number was seen (RESULT.md, "When the sept27 pins
# arrive"): a function's capital takes that function's class, enterprise capital is a service at cost, and public
# housing is a housing voucher. A line named capital_<id> or capital_return_<id> takes its component's class.
CAPITAL_COMPONENTS = {
    "education": ["k12", "college"],
    "justice": ["pos_sl", "pos_fed"],
    "health_services": ["health_sl", "health_fed"],
    "public_good": ["gps_sl", "gps_fed", "hwy_sl", "hwy_fed", "air_fed", "rec_sl", "rec_fed"],
    "housing_voucher": ["ent_housing_sl"],
    "services": ["ent_transit_sl", "ent_airports_sl", "ent_ports_sl", "ent_power_sl", "ent_water_sl", "ent_sewer_sl",
                 "ent_tolls_sl", "ent_power_fed", "ent_other_sl", "ent_other_fed"],
}
LINE_CLASS = {line: cls for cls, lines in LINES.items() for line in lines}
for _cls, _ids in CAPITAL_COMPONENTS.items():
    for _id in _ids:
        LINE_CLASS[f"capital_{_id}"] = LINE_CLASS[f"capital_return_{_id}"] = _cls
FHL_EXTERNAL = 2152 / 3600          # N / G per recipient-year (FHL JPE 2019, author manuscript: N $2,152, G $3,600)


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def pinned_csv(commit, rel):
    out = subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{rel}"], capture_output=True, check=True)
    return pd.read_csv(io.BytesIO(out.stdout))


_STATE_PRICE = {}


def state_price_functions(line):
    """A state-price line's functions (derived/state_price_quantity.csv): each one's gap and quantity part, $bn."""
    if line not in _STATE_PRICE:
        path = DERIVED / "state_price_quantity.csv"
        gate("state_price_quantity_present", path.exists(), path=str(path))
        q = pd.read_csv(path)
        q = q[(q.line == line) & (q.function != "all")].set_index("function")
        gate(f"state_price_functions_{line}", len(q) > 0, line=line)
        _STATE_PRICE[line] = q[["gap_bn", "quantity_bn"]]
    return _STATE_PRICE[line]


def state_price_value(r, cls, v, part):
    """A state-price line valued at its class on a part of its gap: 'quantity_bn' (the rule) or 'gap_bn' (the whole
    gap, an extreme reported beside). The part's share of the gap scales the class's value; justice's protection
    split applies function by function."""
    q = state_price_functions(r.line)
    if CLASSES[cls][0] == "split":
        gate(f"justice_functions_have_a_share_{r.line}", set(q.index) <= set(JUSTICE_FUNCTION_SHARE),
             functions=sorted(q.index))
        return [r.amount_bn * sum(JUSTICE_FUNCTION_SHARE[f] * q.loc[f, part] for f in q.index) / q.gap_bn.sum()] * 3
    return [x * q[part].sum() / q.gap_bn.sum() for x in v]


def value_line(r, part="quantity_bn"):
    cls = RECEIPT_CLASS.get(r.line) if r.side == "receipt" else LINE_CLASS.get(r.line)
    if cls is None:
        raise SystemExit(f"[BLOCKED] unclassified {r.side} line {r.line!r}: add it to LINES before valuing")
    basis, lo, mid, hi, _ = CLASSES[cls]
    cost = -r.effect_bn                                # cost to other residents (spending effects are negative)
    if basis == "effect":
        v = [x * cost for x in (lo, mid, hi)]
    elif basis == "amount":
        v = [x * r.amount_bn for x in (lo, mid, hi)]
    elif basis == "split":
        v = [PROTECTION_SHARE * r.amount_bn] * 3
    else:
        v = [0.0, 0.0, 0.0]
    if r.line in STATE_PRICE_LINES:                    # only the gap's quantity part is worth anything to the group
        v = state_price_value(r, cls, v, part)
    third = FHL_EXTERNAL * cost if cls == "medicaid" else 0.0
    return cls, cost, v, third


def value_case(case):
    pin = PINS[case]
    if not pin["winners"]:
        raise SystemExit(f"[BLOCKED] no pins for case {case}; the parent sends them (brief: 'The case')")
    f = pinned_csv(pin["winners"], lane_file(case, "winners", "fiscal_lines_band_ends.csv"))
    f = f[f.case == pin["model"]]
    gate("case_present", len(f) > 0, case=case, model=pin["model"])
    rows = []
    for r in f.itertuples():
        if r.side == "receipt" and r.line not in RECEIPT_CLASS:
            # A tax the group pays: a transfer to other residents; the group loses it at $1 per $1.
            rows.append(dict(case=case, end=r.end, side="receipt", line=r.line, cls="tax", amount_bn=r.amount_bn,
                             response=r.response, G_bn=-r.effect_bn, V_low_bn=-r.effect_bn, V_central_bn=-r.effect_bn,
                             V_high_bn=-r.effect_bn, third_party_bn=0.0, F_bn=0.0, net_cost_bn=-r.effect_bn))
            continue
        cls, cost, v, third = value_line(r)
        # The capital return's components (side capital_return) are costs, like spending lines.
        rows.append(dict(case=case, end=r.end, side="receipt" if r.side == "receipt" else "spending", line=r.line,
                         cls=cls, amount_bn=r.amount_bn, response=r.response, G_bn=cost, V_low_bn=v[0],
                         V_central_bn=v[1], V_high_bn=v[2], third_party_bn=third, F_bn=0.0, net_cost_bn=cost))
    out = pd.DataFrame(rows)
    # Gate: the lines reproduce the account's direct response A at each end (spending less receipts), as the
    # winners lane's fiscal_specs states it.
    sp = pinned_csv(pin["winners"], lane_file(case, "winners", "fiscal_specs.csv"))
    sp = sp[(sp.case == pin["model"]) & sp.band_end.notna()].drop_duplicates("band_end").set_index("band_end")
    for end, s in out.groupby("end"):
        A = s.net_cost_bn.sum()
        gate(f"lines_reproduce_A_{end}", abs(A + sp.loc[end, "A_bn"]) < 1e-3, lines=A, A_bn=sp.loc[end, "A_bn"])
    # The state-price lines' central value under the rule, with its two extremes beside (the whole gap at the class;
    # 0), for the case's meta. Empty for a case without them.
    extremes = {}
    for r in f[f.line.isin(STATE_PRICE_LINES)].itertuples():
        e = extremes.setdefault(r.end, dict(quantity_bn=0.0, whole_gap_bn=0.0, zero_bn=0.0))
        e["quantity_bn"] += value_line(r)[2][1]
        e["whole_gap_bn"] += value_line(r, part="gap_bn")[2][1]
    return out, extremes


def value_generations(case, union):
    """The generation lane's split of the case's lines (derived/generation_lines_<case>.csv, from
    generation_lines.cjs), valued line by line with the union's classes. The capital return's components are
    costs, like spending lines."""
    path = DERIVED / f"generation_lines_{case}.csv"
    gate(f"generation_lines_{case}_present", path.exists(), path=str(path))
    g = pd.read_csv(path)
    g["generation"] = g.generation.replace({"G3plus": "G3+"})
    tot = g[g.side == "total"].pivot_table(index=["band_end", "generation"], columns="line", values="effect_bn")
    lines = g[g.side != "total"].assign(side=lambda d: d.side.replace({"capital": "spending"}))
    # Gate: the three generations add to the case's lines, line by line (the same line set, the same amounts).
    s = lines.groupby(["band_end", "side", "line"])[["amount_bn", "effect_bn"]].sum()
    u = union.set_index(["end", "side", "line"])
    u = pd.DataFrame({"amount_bn": u.amount_bn, "effect_bn": -u.net_cost_bn})
    gate("generation_lines_match_the_case_lines", s.index.sort_values().equals(u.index.sort_values()),
         only_generations=sorted(set(s.index) - set(u.index))[:5], only_case=sorted(set(u.index) - set(s.index))[:5])
    d = (s - u.reindex(s.index)).abs().max()
    gate("generations_add_to_the_case_lines", bool((d < 1e-6).all()), max_abs_diff=d.to_dict())
    rows = []
    for r in lines.itertuples():
        head = dict(case=case, end=r.band_end, generation=r.generation, side=r.side, line=r.line, amount_bn=r.amount_bn)
        if r.side == "receipt" and r.line not in RECEIPT_CLASS:
            rows.append(dict(head, cls="tax", G_bn=-r.effect_bn, V_low_bn=-r.effect_bn, V_central_bn=-r.effect_bn,
                             V_high_bn=-r.effect_bn, third_party_bn=0.0, net_cost_bn=-r.effect_bn))
            continue
        cls, cost, v, third = value_line(r)
        rows.append(dict(head, cls=cls, G_bn=cost, V_low_bn=v[0], V_central_bn=v[1], V_high_bn=v[2],
                         third_party_bn=third, net_cost_bn=cost))
    out = pd.DataFrame(rows)
    # Gate: each generation's net cost plus its production term is the generation lane's cost (convention (a)).
    pin = PINS[case]["generation"]
    res = pinned_csv(pin, lane_file(case, "generation", "generation_results.csv"))
    res = res[res.convention == "a"].assign(generation=lambda d: d.generation.replace({"G3plus": "G3+"}))
    res = res.set_index(["band_end", "generation"]).cost_bn
    net = out.groupby(["end", "generation"]).net_cost_bn.sum()
    worst = max(abs(net[k] + tot.loc[k, "production"] - res[k]) for k in res.index)
    gate("generation_net_costs_equal_generation_results", worst < 1e-6, max_abs_diff=worst, pin=pin)
    return out


def mexico_budget(basis="cps"):
    """The group's alternative world: what Mexico's budget would spend on the same people, by class, at the
    group's own ages (CPS ASEC 2025; 40.9m on the cps basis, the account's 39.71m on row4, main case v5's 42.75m on
    lineage), priced with Mexico's 2024 per-person spending (mexico.py). Case-independent."""
    ages = pd.read_csv(suffixed(DERIVED / "group_ages.csv", basis))
    comp = pd.read_csv(DERIVED / "mexico_comparators_by_age.csv").set_index("age")
    meta = json.load(open(DERIVED / "mexico_meta.json"))["comparators"]
    # Taxes: the income tax and employee contributions withheld from formal pay are a measured lower bound, in the
    # central premium scenario (g2_premium.csv). world_ledger adds IVA, IEPS and the fuel excise at the household
    # decile's rate (SHCP 2026) in its central and bounds all taxes above. G3+ has bounds only.
    g2 = pd.read_csv(suffixed(DERIVED / "g2_premium.csv", basis))
    g2 = g2[g2.ppp.eq("gdp") & g2.diploma_reread.eq(0.25) & ~g2.mishra]
    withheld = {"G1": g2[g2.convention.eq("own_schooling_all_ages") & g2.selection.eq("p56")].mexico_withheld_tax_bn.item(),
                "G2": g2[g2.convention.eq("rearing")].mexico_withheld_tax_bn.mean(), "G3+": np.nan}
    rows = []
    for gen, s in ages.groupby("generation"):
        a = s.set_index("age").persons
        c = comp.reindex(np.minimum(a.index.to_numpy(), 90)).set_axis(a.index)
        students = (a * c.public_student_rate).sum()
        rows += [
            dict(generation=gen, cls="education", item="public school places at Mexico's cost per public student",
                 bn=students * meta["education_per_public_student_ppp"] / 1e9, basis="[DATA: ENIGH attendance; WDI "
                 "SE.XPD.TOTL.GD.ZS 2022 x GDP PPP 2024]", students_m=students / 1e6),
            dict(generation=gen, cls="health", item="government health spending per head",
                 bn=a.sum() * meta["health_per_capita_ppp_2023"] / 1e9, basis="[DATA: WDI SH.XPD.GHED.PP.CD 2023]"),
            dict(generation=gen, cls="cash", item="government cash transfers by age (ENIGH bene_gob claves)",
                 bn=(a * c.transfers_ppp_per_person).sum() / 1e9, basis="[DATA: ENIGH 2024]"),
            dict(generation=gen, cls="cash", item="pensions paid in Mexico by age (ENIGH P032)",
                 bn=(a * c.pension_ppp_per_person).sum() / 1e9, basis="[DATA: ENIGH 2024]"),
            dict(generation=gen, cls="public_good", item="other government consumption per head",
                 bn=a.sum() * meta["other_gov_consumption_per_capita_ppp"] / 1e9,
                 basis="[CALCULATION: WDI NE.CON.GOVT.ZS 2024 less health and education shares; approximate]"),
            dict(generation=gen, cls="tax", item="taxes the group would pay in Mexico: withheld from formal pay "
                 "(lower bound)", bn=withheld[gen],
                 basis="[CALCULATION: 2024 statutory withholding, mexico.py; consumption taxes in world_ledger's "
                       "central, all taxes its upper bound]" if gen != "G3+" else "[GAP: bounds only, world_ledger]"),
        ]
    return pd.DataFrame(rows)


def value_block(cases, mx):
    """Value a block of cases and write its four files: the shared files for the SHARED_OUTPUTS cases, a set of
    _<case> files for one later case."""
    vals, bys, gens = [], [], []
    # medicaid_vg is the one definition world_ledger.py applies to health care outside the account.
    meta = dict(protection_share=PROTECTION_SHARE, pins={c: PINS[c] for c in cases}, cases={}, generations={},
                medicaid_vg=list(CLASSES["medicaid"][1:4]))
    for case in cases:
        v, extremes = value_case(case)
        if extremes:
            meta.setdefault("state_price_value_bn", {})[case] = extremes
        vals.append(v)
        vg = value_generations(case, v)
        gens.append(vg)
        meta["generations"][case] = {f"{end}|{g}": dict(net_cost_bn=float(s.net_cost_bn.sum()),
                                                       V_central_bn=float(s.V_central_bn.sum()))
                                     for (end, g), s in vg.groupby(["end", "generation"])}
        by = v.groupby(["end", "side", "cls"])[["amount_bn", "G_bn", "V_low_bn", "V_central_bn", "V_high_bn",
                                                "third_party_bn", "net_cost_bn"]].sum().reset_index()
        by.insert(0, "case", case)
        by["source"] = [CLASSES[c][4] if c in CLASSES else "tax paid, $1 per $1" for c in by.cls]
        bys.append(by)
        meta["cases"][case] = {end: dict(A_bn=float(s.net_cost_bn.sum()), V_low_bn=float(s.V_low_bn.sum()),
                                         V_central_bn=float(s.V_central_bn.sum()), V_high_bn=float(s.V_high_bn.sum()))
                               for end, s in v.groupby("end")}
    at = lambda name: case_path(name, cases[0])
    pd.concat(vals).to_csv(at("valuation.csv"), index=False, lineterminator="\n", float_format="%.6f")
    pd.concat(gens).to_csv(at("valuation_by_generation.csv"), index=False, lineterminator="\n", float_format="%.9f")
    by = pd.concat(bys)
    by.to_csv(at("valuation_by_class.csv"), index=False, lineterminator="\n", float_format="%.6f")
    meta["mexico_budget_bn_known"] = float(mx[mx.cls.ne("tax")].bn.sum(skipna=True))
    json.dump(meta, open(at("valuation_meta.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps(meta["cases"], indent=1), file=sys.stderr)
    print(by[by.end == "low"].drop(columns=["source"]).round(2).to_string(), file=sys.stderr)


def main():
    DERIVED.mkdir(exist_ok=True)
    cases = [c for c, pin in PINS.items() if pin["winners"]]
    # Mexico's budget on every basis (g2_premium.py runs on each first); world_ledger.py reads the one it runs on.
    mxs = {b: mexico_budget(b) for b in BASES}
    for b, mx in mxs.items():
        mx.to_csv(suffixed(DERIVED / "mexico_budget.csv", b), index=False, lineterminator="\n", float_format="%.6f")
    for block in [[c for c in cases if c in SHARED_OUTPUTS]] + [[c] for c in cases if c not in SHARED_OUTPUTS]:
        if block:
            value_block(block, mxs[basis_of(block[0])])
    print(mxs["cps"].groupby(["cls"]).bn.sum().round(2).to_string(), file=sys.stderr)


if __name__ == "__main__":
    main()
