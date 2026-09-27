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
Every case with pins is valued. Outputs: derived/valuation.csv, derived/valuation_by_class.csv and
derived/valuation_by_generation.csv (one block per case), derived/mexico_budget.csv (case-independent),
derived/valuation_meta.json.
"""
import io
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
FISCAL_REL = "infra/immigration-fiscal"
# Pinned inputs per case (pins.json, shared with world_ledger.py): the commits holding each case's files.
PINS = {k: v for k, v in json.load(open(HERE / "pins.json")).items() if not k.startswith("_")}
# Justice use by component, central split (cj_use_allocation_2026_09_23/derived/central_split.csv, use_bn):
# protection is fire, the per-head half of non-border police, civil courts and CBP; offender processing and
# enforcement is prisons, the arrest-keyed half of police, criminal courts (the unsplit part of law courts) and ICE.
JUSTICE = dict(fire=9.640327, police_per_head=27.540691 - 14.873448, civil_courts=10.649463 - 6.792708,
               cbp=2.870475, prisons=17.216835, police_arrest=14.873448, criminal_courts=6.792708,
               ice=0.214229 + 0.237015)
PROTECTION = ("fire", "police_per_head", "civil_courts", "cbp")
PROTECTION_SHARE = sum(JUSTICE[k] for k in PROTECTION) / sum(JUSTICE.values())

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
    "health_services": ["health_services", "military_medical", "veterans_other"],
    "services": ["income_security_services"],
    "education": ["education_services", "school_reprice", "college_rekey", "education_benefits",
                  "employment_training"],
    "public_good": ["general_public_services", "defense", "economic_affairs_services", "recreation_culture",
                    "housing_community_services"],
    "justice": ["public_order_safety"],
    "not_a_service": ["domestic_interest", "foreign_interest", "agricultural_subsidies", "other_subsidies",
                      "transport_subsidies", "foreign_territory_social_benefits", "other_foreign_current_transfers"],
    "correction": ["lane_constants", "source_rounding"],
}
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


def value_line(r):
    cls = LINE_CLASS.get(r.line)
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
    third = FHL_EXTERNAL * cost if cls == "medicaid" else 0.0
    return cls, cost, v, third


def value_case(case):
    pin = PINS[case]
    if not pin["winners"]:
        raise SystemExit(f"[BLOCKED] no pins for case {case}; the parent sends them (brief: 'The case')")
    f = pinned_csv(pin["winners"], f"{FISCAL_REL}/winners_losers_2026_09_24/derived/fiscal_lines_band_ends.csv")
    f = f[f.case == pin["model"]]
    gate("case_present", len(f) > 0, case=case, model=pin["model"])
    rows = []
    for r in f.itertuples():
        if r.side == "receipt":
            # A tax the group pays: a transfer to other residents; the group loses it at $1 per $1.
            rows.append(dict(case=case, end=r.end, side="receipt", line=r.line, cls="tax", amount_bn=r.amount_bn,
                             response=r.response, G_bn=-r.effect_bn, V_low_bn=-r.effect_bn, V_central_bn=-r.effect_bn,
                             V_high_bn=-r.effect_bn, third_party_bn=0.0, F_bn=0.0, net_cost_bn=-r.effect_bn))
            continue
        cls, cost, v, third = value_line(r)
        rows.append(dict(case=case, end=r.end, side="spending", line=r.line, cls=cls, amount_bn=r.amount_bn,
                         response=r.response, G_bn=cost, V_low_bn=v[0], V_central_bn=v[1], V_high_bn=v[2],
                         third_party_bn=third, F_bn=0.0, net_cost_bn=cost))
    out = pd.DataFrame(rows)
    # Gate: the lines reproduce the account's direct response A at each end (spending less receipts), as the
    # winners lane's fiscal_specs states it.
    sp = pinned_csv(pin["winners"], f"{FISCAL_REL}/winners_losers_2026_09_24/derived/fiscal_specs.csv")
    sp = sp[(sp.case == pin["model"]) & sp.band_end.notna()].drop_duplicates("band_end").set_index("band_end")
    for end, s in out.groupby("end"):
        A = s.net_cost_bn.sum()
        gate(f"lines_reproduce_A_{end}", abs(A + sp.loc[end, "A_bn"]) < 1e-3, lines=A, A_bn=sp.loc[end, "A_bn"])
    return out


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
        if r.side == "receipt":
            rows.append(dict(head, cls="tax", G_bn=-r.effect_bn, V_low_bn=-r.effect_bn, V_central_bn=-r.effect_bn,
                             V_high_bn=-r.effect_bn, third_party_bn=0.0, net_cost_bn=-r.effect_bn))
            continue
        cls, cost, v, third = value_line(r)
        rows.append(dict(head, cls=cls, G_bn=cost, V_low_bn=v[0], V_central_bn=v[1], V_high_bn=v[2],
                         third_party_bn=third, net_cost_bn=cost))
    out = pd.DataFrame(rows)
    # Gate: each generation's net cost plus its production term is the generation lane's cost (convention (a)).
    pin = PINS[case]["generation"]
    res = pinned_csv(pin, f"{FISCAL_REL}/generation_account_2026_09_24/derived/generation_results.csv")
    res = res[res.convention == "a"].assign(generation=lambda d: d.generation.replace({"G3plus": "G3+"}))
    res = res.set_index(["band_end", "generation"]).cost_bn
    net = out.groupby(["end", "generation"]).net_cost_bn.sum()
    worst = max(abs(net[k] + tot.loc[k, "production"] - res[k]) for k in res.index)
    gate("generation_net_costs_equal_generation_results", worst < 1e-6, max_abs_diff=worst, pin=pin)
    return out


def mexico_budget():
    """The group's alternative world: what Mexico's budget would spend on the same 40.9m people, by class, at the
    group's own ages (CPS ASEC 2025), priced with Mexico's 2024 per-person spending (mexico.py). Case-independent."""
    ages = pd.read_csv(DERIVED / "group_ages.csv")
    comp = pd.read_csv(DERIVED / "mexico_comparators_by_age.csv").set_index("age")
    meta = json.load(open(DERIVED / "mexico_meta.json"))["comparators"]
    # Taxes: the income tax and employee contributions withheld from formal pay are a measured lower bound, in the
    # central premium scenario (g2_premium.csv). world_ledger adds IVA, IEPS and the fuel excise at the household
    # decile's rate (SHCP 2026) in its central and bounds all taxes above. G3+ has bounds only.
    g2 = pd.read_csv(DERIVED / "g2_premium.csv")
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


def main():
    DERIVED.mkdir(exist_ok=True)
    cases = [c for c, pin in PINS.items() if pin["winners"]]
    vals, bys, gens = [], [], []
    # medicaid_vg is the one definition world_ledger.py applies to health care outside the account.
    meta = dict(protection_share=PROTECTION_SHARE, pins={c: PINS[c] for c in cases}, cases={}, generations={},
                medicaid_vg=list(CLASSES["medicaid"][1:4]))
    for case in cases:
        v = value_case(case)
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
    pd.concat(vals).to_csv(DERIVED / "valuation.csv", index=False, lineterminator="\n", float_format="%.6f")
    pd.concat(gens).to_csv(DERIVED / "valuation_by_generation.csv", index=False, lineterminator="\n",
                           float_format="%.9f")
    by = pd.concat(bys)
    by.to_csv(DERIVED / "valuation_by_class.csv", index=False, lineterminator="\n", float_format="%.6f")
    mx = mexico_budget()
    mx.to_csv(DERIVED / "mexico_budget.csv", index=False, lineterminator="\n", float_format="%.6f")
    meta["mexico_budget_bn_known"] = float(mx[mx.cls.ne("tax")].bn.sum(skipna=True))
    json.dump(meta, open(DERIVED / "valuation_meta.json", "w"), indent=1, sort_keys=True)
    print(json.dumps(meta["cases"], indent=1), file=sys.stderr)
    print(by[by.end == "low"].drop(columns=["source"]).round(2).to_string(), file=sys.stderr)
    print(mx.groupby(["cls"]).bn.sum().round(2).to_string(), file=sys.stderr)


if __name__ == "__main__":
    main()
