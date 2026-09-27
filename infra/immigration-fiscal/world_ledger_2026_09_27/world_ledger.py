"""Brief parts C-E: the world ledger. One row per effect, each with its beneficiary, initial state, alternative
state, time window and kind (quantity or transfer); then party totals under each weighting and the break-even
weight on the group.

Initial state: 2024 as measured, the group (12.22m born in Mexico, 14.33m with a Mexico-born parent, 14.34m
third-plus generation) in the US. Alternative state, for every row: the same people in Mexico, the US-born
raised there by parents with the same schooling who stayed (controlled rearing, not a no-migration history),
and the US without them as the account removes them. Window: one year, 2024, a stationary cross-section.
Long run on both sides: the US account's wage channel is its long-run one (capital adjusts), so Mexico's
average wage is left unchanged centrally; Mishra's short-run wage effects are a sensitivity.
Pay is gross on both sides (CPS; ENIGH grossed up for the 2024 withholding on formal jobs), so the taxes the
group would pay in Mexico are a transfer to Mexico's residents, bounded below by the withheld income tax and
contributions ('withheld') and above by all taxes in proportion to labor income ('proportional'). The central
('withheld_consumption') adds IVA and IEPS on gross pay at the household decile's rate, as SHCP measures them for
2024, and the 2024 fuel excise, which SHCP's incidence leaves out, spread by SHCP's fuel-spending proxy, to the
withheld taxes, since the group's US row subtracts its US sales and excise taxes.

Weightings (columns):
- equal: $1 is $1 for every party.
- equal_lambda_L: other residents' and future taxpayers' fiscal cost, and Mexico's budget savings, carry the
  marginal cost of public funds L (1.16, 1.5), and L_h, the one Hendren's g(y) implies under tax shares.
- hendren_a / hendren_b: Hendren's inverse-optimum weights g(y) (Figure 6, digitized) at each party's position
  on the US money-income scale. Under tax-share financing (a) a payer's weighted loss equals the revenue raised
  (the loss is R/g, weighted by g); under per-person cuts (b) the cut is weighted by g. Mexico's residents: 1.15,
  assumed (the weights are US-specific).
- log_a / log_b: log income, money-metric at other residents' mean household money income per head. Other
  residents' channels are weighted by reference income per head over each person's household income per head
  (floored at the 5th percentile), on the distribution lane's percentile bins; Mexico's residents by the same
  reference over their median income per head (ENIGH, PPP). The group's rows are finite changes of log
  consumption, in the order: Mexico's budget lost, the place premium log(E_US/E_MX), the US budget valued,
  remittances sent, in-group victimization and uncompensated care.
- break-even w: the moral weight on the group at which W = N + wM = 0.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/world_ledger.py
     [--case sept26_schools|sept27]
Outputs: derived/world_ledger.csv (party x weighting, per scenario), derived/world_ledger_rows.csv (row detail),
derived/world_ledger_meta_<case>.json, derived/generation_split_check.csv (this lane's generation split beside the
generation lane's).
"""
import argparse
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
PINS = {k: v for k, v in json.load(open(HERE / "pins.json")).items() if not k.startswith("_")}
GENS = ["G1", "G2", "G3+"]
PARTIES = ["others_today", "future_taxpayers", "G1", "G2", "G3+", "mexico_residents"]
GROUP = ["G1", "G2", "G3+"]
LAMBDAS = {"1.16": 1.16, "1.5": 1.5}
G_MEXICO = 1.15                          # assumed (weights.py)
MEXICO_PUBLIC_RESPONSE = (0.60, 0.725, 0.85)   # assumed: the US account's general-government range
# Remittances by generation. The total is Banxico's 2024 flow from the US (winners lane group frame). The
# repo's "$3.7bn cap on US-born senders" was withdrawn on 2026-09-17 as circular (remit_leak_2026_09_16/RESULT.md,
# correction; research/immigration-aggregate-and-generation-audit-2026-09-17.md). Second-generation rates are
# scenarios, not measurements: 0 (low), 1.6% (central) and 5.2% (high) of G2 earnings, the remit_leak arms.
G2_REMIT_RATE = (0.0, 0.016, 0.052)
# Mishra (IMF WP/06/86, p. 4; reads/mishra_2007.md quotes 4 and 6): emigrants were 16% of Mexico's labor force in
# 2000; stayer workers gained 5.9% of GDP, owners of fixed factors lost 6.4%, a net loss of 0.5%.
MISHRA = dict(shock=0.16, stayers_gain=0.059, owners_loss=0.064, net_loss=0.005)
# Claim 2's productive-use reading: the payers would have saved part of what they pay. They value the dollar at $1
# whatever its use (envelope theorem), so their saving matters to others only through the tax on its forgone
# return. Saving rates by wealth group (Mian, Straub and Sufi 2025; reads/mian_straub_sufi_2025.md): top 1% 54%
# (1983-2019), next 9% 20%, 51st-90th percentile 12%, bottom 50% zero; applied to the payers' income percentiles.
# Tax on the return to a marginal investment: CRS 9.3% (economy-wide, 2024) to CBO 29% (business capital, 2014 law).
# m, the pre-tax return over the discount rate on the forgone revenue: 1 at OMB's 7%, 3.5 at the main case's 2% real
# cost of government funds (reads/capital_tax_wedge.md).
MSS_SAVING = ((1, 50, 0.0), (51, 90, 0.12), (91, 99, 0.20), (100, 100, 0.54))
CAPITAL_TAX = (0.093, 0.29)
RETURN_OVER_DISCOUNT = (1.0, 3.5)


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def git_show(commit, rel):
    return subprocess.run(["git", "-C", str(REPO), "show", f"{commit}:{rel}"], capture_output=True,
                          check=True).stdout


def pinned_csv(commit, rel):
    return pd.read_csv(io.BytesIO(git_show(commit, rel)))


# ------------------------------------------------------------------ inputs
def load(case):
    pin = PINS[case]
    if not pin["winners"]:
        raise SystemExit(f"[BLOCKED] no pins for case {case}; the parent sends them")
    w = f"{FISCAL_REL}/winners_losers_2026_09_24/derived"
    ch = pinned_csv(pin["winners"], f"{w}/channels.csv").set_index("id")
    specs = pinned_csv(pin["winners"], f"{w}/fiscal_specs.csv")
    specs = specs[(specs.case == pin["model"]) & specs.band_end.notna()].drop_duplicates("band_end").set_index("band_end")
    gf = pinned_csv(pin["winners"], f"{w}/group_frame.csv")
    dist = pinned_csv(pin["distribution"], f"{FISCAL_REL}/distribution_weights_2026_09_23/derived/channel_by_percentile.csv")
    gen = pinned_csv(pin["generation"], f"{FISCAL_REL}/generation_account_2026_09_24/derived/generation_results.csv")
    val = pd.read_csv(DERIVED / "valuation.csv")
    val = val[val.case == case]
    gate("valuation_has_case", len(val) > 0, case=case)
    vgen = pd.read_csv(DERIVED / "valuation_by_generation.csv")
    vgen = vgen[vgen.case == case]
    gate("valuation_by_generation_has_case", len(vgen) > 0, case=case)
    glines = pd.read_csv(DERIVED / f"generation_lines_{case}.csv").replace({"generation": {"G3plus": "G3+"}})
    return dict(ch=ch, specs=specs, gf=gf, dist=dist, gen=gen, val=val, vgen=vgen, glines=glines,
                g2=pd.read_csv(DERIVED / "g2_premium.csv"), ages=pd.read_csv(DERIVED / "group_ages.csv"),
                mxb=pd.read_csv(DERIVED / "mexico_budget.csv"), gtab=pd.read_csv(DERIVED / "hendren_g.csv"),
                pos=pd.read_csv(DERIVED / "income_positions.csv"),
                wmeta=json.load(open(DERIVED / "weights_meta.json")),
                # The Medicaid class (valuation.py), applied to hospital care received and Mexico's public health.
                health_vg=tuple(json.load(open(DERIVED / "valuation_meta.json"))["medicaid_vg"]))


def lh(lo, mid, hi):
    return dict(low=float(lo), central=float(mid), high=float(hi))


# ------------------------------------------------------------------ the group's rows
def premium_rows(I, short_run=False, g3_central="zero"):
    """Place premium per generation, $bn, low/central/high, gross pay on both sides. Central: ENIGH 2024 at GDP
    PPP, diploma re-read 0.25, Mexico's wage as observed (long run). G1 selection p56 (range p70-p50); G2 rearing
    with inherited selection at the midpoint (range: own US schooling with all of it - rearing with none, at
    consumption PPP). 'tax' is the income tax and employee contributions withheld from the Mexican pay of the
    same scenario; 'home' is the take-home pay left after them and the retirement deposit; 'ctax' is the IVA and
    IEPS on gross pay at the household decile's rate (SHCP 2026, mexico.py). G3+ has bounds only; its central takes
    the lower ('zero') or upper bound."""
    g = I["g2"]
    mis = short_run

    def pick(gen, conv, ppp, f, sel):
        r = g[(g.generation == gen) & (g.convention == conv) & (g.ppp == ppp) & (g.diploma_reread == f)
              & (g.mishra == mis) & (g.selection == sel)]
        gate(f"premium_row_{gen}_{conv}_{ppp}_{f}_{sel}_{mis}", len(r) == 1, n=len(r))
        return r.iloc[0]

    c1 = pick("G1", "own_schooling_all_ages", "gdp", 0.25, "p56")
    lo1 = pick("G1", "own_schooling_all_ages", "gdp", 0.25, "p70")
    hi1 = pick("G1", "own_schooling_all_ages", "consumption", 0.25, "p50")
    a2, n2 = pick("G2", "rearing", "gdp", 0.25, "all"), pick("G2", "rearing", "gdp", 0.25, "none")
    lo2 = pick("G2", "own_us_schooling", "gdp", 0.0, "all")
    hi2 = pick("G2", "rearing", "consumption", 0.25, "none")
    out = {
        "G1": dict(gain=lh(lo1.gain_bn, c1.gain_bn, hi1.gain_bn),
                   e_us=c1.us_earnings_bn, e_mx=lh(lo1.mexico_earnings_bn, c1.mexico_earnings_bn,
                                                 hi1.mexico_earnings_bn),
                   tax=lh(lo1.mexico_withheld_tax_bn, c1.mexico_withheld_tax_bn, hi1.mexico_withheld_tax_bn),
                   home=lh(lo1.mexico_take_home_bn, c1.mexico_take_home_bn, hi1.mexico_take_home_bn),
                   ctax=lh(lo1.mexico_consumption_tax_bn, c1.mexico_consumption_tax_bn, hi1.mexico_consumption_tax_bn),
                   persons=c1.persons_m),
        "G2": dict(gain=lh(lo2.gain_bn, (a2.gain_bn + n2.gain_bn) / 2, hi2.gain_bn),
                   e_us=a2.us_earnings_bn, e_mx=lh(lo2.mexico_earnings_bn, (a2.mexico_earnings_bn
                                                                           + n2.mexico_earnings_bn) / 2,
                                                   hi2.mexico_earnings_bn),
                   tax=lh(lo2.mexico_withheld_tax_bn, (a2.mexico_withheld_tax_bn + n2.mexico_withheld_tax_bn) / 2,
                          hi2.mexico_withheld_tax_bn),
                   home=lh(lo2.mexico_take_home_bn, (a2.mexico_take_home_bn + n2.mexico_take_home_bn) / 2,
                           hi2.mexico_take_home_bn),
                   ctax=lh(lo2.mexico_consumption_tax_bn,
                           (a2.mexico_consumption_tax_bn + n2.mexico_consumption_tax_bn) / 2,
                           hi2.mexico_consumption_tax_bn), persons=a2.persons_m),
    }
    g3 = g[(g.generation == "G3+")].iloc[0]
    up = dict(gain=g3.gain_bn, e_mx=g3.mexico_earnings_bn, tax=g3.mexico_withheld_tax_bn, home=g3.mexico_take_home_bn,
              ctax=g3.mexico_consumption_tax_bn)
    # No premium: in Mexico they would earn what they earn in the US, withheld and taxed on consumption at the upper
    # bound's rates [INFERENCE: proportional; the income-tax schedule is progressive, so this understates the
    # withheld tax; the consumption-tax rate is nearly flat above decile III (8.6-10.3%)].
    scale = g3.us_earnings_bn / g3.mexico_earnings_bn
    zero = dict(gain=0.0, e_mx=g3.us_earnings_bn, tax=g3.mexico_withheld_tax_bn * scale,
                home=g3.mexico_take_home_bn * scale, ctax=g3.mexico_consumption_tax_bn * scale)
    mid = {"zero": zero, "upper": up}[g3_central]
    out["G3+"] = dict(**{k: lh(zero[k], mid[k], up[k]) for k in ("gain", "e_mx", "tax", "home", "ctax")},
                      e_us=g3.us_earnings_bn, persons=g3.persons_m)
    return out


def population_shares(I):
    """Each generation's share of the group's persons (CPS ASEC 2025, derived/group_ages.csv), for the rows the
    account does not split by generation: care received and in-group victims."""
    s = I["ages"].groupby("generation").persons.sum().reindex(GENS, fill_value=0)
    return dict(pop=(s / s.sum()).to_dict())


def fiscal_group_rows(I, pg_convention):
    """The US budget as each generation values it, $bn (low/central/high over both account ends and the V/G
    ranges): the generation lane's own split of the case's lines (convention (a), each person in their own
    generation; the band ends' allocations, shared at the low end and personal at the high end), valued line by
    line with the union's classes (valuation.py value_generations). pg_convention 'average_cost' (the brief's)
    values public goods at average cost; 'response_only' values them at what they cost others (V = G).
    The three generations take each outer span at one account end: the end where the group's valued total is
    lowest (low, at V_low) or highest (high, at V_high). Each generation's own minimum would mix the two ends'
    allocations, which move children's flows between generations, and would publish a split that is neither end's.
    The central is the mean of the two ends."""
    v = I["vgen"].copy()
    if pg_convention == "response_only":
        m = v.cls.eq("public_good")
        for c in ("V_low_bn", "V_central_bn", "V_high_bn"):
            v.loc[m, c] = v.loc[m, "G_bn"]
    sh = population_shares(I)
    by = v.groupby(["end", "generation"])[["V_low_bn", "V_central_bn", "V_high_bn"]].sum()
    tot = by.groupby(level="end").sum()
    lo_end, hi_end = tot.V_low_bn.idxmin(), tot.V_high_bn.idxmax()
    out = {gname: dict(value=lh(by.loc[(lo_end, gname), "V_low_bn"],
                                np.mean([by.loc[(e, gname), "V_central_bn"] for e in ("low", "high")]),
                                by.loc[(hi_end, gname), "V_high_bn"]))
           for gname in GENS}
    return out, sh


def generation_split_check(I, case):
    """The reconciliation behind the generation rows: at each band end, each generation's valued lines (their net
    cost) plus its production term beside the generation lane's cost (generation_results.csv, convention (a)).
    Gate: equal to 1e-6."""
    v, gl = I["vgen"], I["glines"]
    gr = I["gen"][I["gen"].convention == "a"]
    rows = []
    for end in ("low", "high"):
        for g in GENS:
            lane = gr[(gr.band_end == end) & (gr.generation == g.replace("+", "plus"))]
            prod = gl[(gl.band_end == end) & (gl.generation == g) & (gl.side == "total") & (gl.line == "production")]
            gate(f"generation_lane_rows_{end}_{g}", len(lane) == 1 and len(prod) == 1, n=[len(lane), len(prod)])
            lines = float(v[(v.end == end) & (v.generation == g)].net_cost_bn.sum())
            mine = lines + float(prod.effect_bn.item())
            rows.append(dict(case=case, band_end=end, allocation=lane.allocation.item(), generation=g,
                             lines_bn=lines, production_bn=float(prod.effect_bn.item()), this_lane_bn=mine,
                             generation_lane_bn=float(lane.cost_bn.item()),
                             difference_bn=mine - float(lane.cost_bn.item())))
    out = pd.DataFrame(rows)
    gate("generation_rows_reproduce_the_generation_lane", bool((out.difference_bn.abs() < 1e-6).all()),
         max_abs_diff=float(out.difference_bn.abs().max()))
    return out


# ------------------------------------------------------------------ the rows
def wdi_mexico_2024(ind):
    rows = json.load(open(HERE / f"_cache/mexico/wdi_{ind}.json"))[1]
    v = [r["value"] for r in rows if r["country"]["id"] == "MX" and r["date"] == "2024"]
    gate(f"wdi_{ind}_mexico_2024", len(v) == 1 and v[0] is not None, found=v)
    return v[0]


def mexico_consumption_tax_rate():
    """A check on the central's consumption taxes, not used in the rows: Mexico's taxes on goods and services
    (central government: IVA, IEPS and the rest) over household final consumption, 2024 (WDI GC.TAX.GSRV.CN /
    NE.CON.PRVT.CN), the average tax on a peso of household spending. The central takes SHCP's measured incidence
    by household decile instead (mexico.py), which already handles zero-rating, informal purchases and saving."""
    tax, cons = wdi_mexico_2024("GC.TAX.GSRV.CN"), wdi_mexico_2024("NE.CON.PRVT.CN")
    rate = tax / cons
    gate("mexico_consumption_tax_rate_plausible", 0.03 < rate < 0.15, rate=rate)
    return rate, dict(taxes_on_goods_services_mxn_bn=tax / 1e9, household_consumption_mxn_bn=cons / 1e9)


def mexico_tax_bound(I, prem):
    """Upper bound on the Mexican taxes each generation would pay in the alternative world: Mexico's central-
    government tax revenue (WDI GC.TAX.TOTL.GD.ZS 2024 x GDP PPP) in proportion to the generation's share of
    Mexico's gross labor income (ENIGH 2024, grossed up), as if every tax fell on labor income; per scenario end."""
    tax_share = wdi_mexico_2024("GC.TAX.TOTL.GD.ZS") / 100
    meta = json.load(open(DERIVED / "mexico_meta.json"))
    gdp = meta["comparators"]["gdp_ppp_2024"] / 1e9
    labor = meta["enigh_labor_income_gross_mxn_bn"] / meta["ppp_2024"]["PA.NUS.PPP"]
    return ({g: {e: tax_share * gdp * prem[g]["e_mx"][e] / labor for e in ("low", "central", "high")} for g in GROUP},
            dict(tax_share=tax_share, gdp_ppp_bn=gdp, labor_income_gross_ppp_bn=labor))


# Every row's basis. The ledger is on the output basis: pay is gross on both sides, and each country's taxes on the
# group appear once, as a transfer between the group and that country's residents (US: us_budget_value against
# fiscal_others; Mexico: mexico_taxes_avoided against mexico_taxes_lost). A row id without a basis stops the run.
BASIS = (("premium_", "output: gross pay in both places, PPP"),
         ("us_budget_value_", "fiscal, US: services received as valued less the group's taxes (the account's receipt "
                              "effects)"),
         ("fiscal_", "fiscal, US: the account, crediting the group's US taxes"),
         ("induced_receipts", "fiscal, US: the account's induced receipts"),
         ("displaced_beneficiaries", "fiscal, US: capped programs, paid for by eligible households that go without"),
         ("mexico_budget_", "fiscal, Mexico: services"),
         ("mexico_taxes_", "fiscal, Mexico: taxes on the group (bound or central, column mexico_taxes)"),
         ("remit_", "private transfer"),
         ("uncompensated_received_", "care received in the US, valued"),
         ("ingroup_victims_", "harm, quantity"),
         ("crime_victims", "harm, quantity"), ("property_crime", "harm, quantity"),
         ("congestion", "harm, quantity"), ("unreimbursed_care", "resource cost, quantity"),
         ("wages", "market, the account's channel"), ("renters", "market, the account's channel"),
         ("landlords", "market, the account's channel"), ("mobility", "market, the account's channel"))


def row_basis(rid):
    for prefix, basis in BASIS:
        if rid.startswith(prefix):
            return basis
    raise SystemExit(f"[BLOCKED] row {rid!r} has no basis label")


def build_rows(I, pg_convention="average_cost", short_run=False, mexico_taxes="withheld_consumption",
               g3_central="zero"):
    rows = []

    def add(rid, label, party, kind, vals, **meta):
        rows.append(dict(row=rid, label=label, party=party, kind=kind, basis=row_basis(rid), **vals, **meta))

    alt = "the same people in Mexico (descendants raised there by parents who stayed); the US without them"
    health_vg = I["health_vg"]
    prem = premium_rows(I, short_run, g3_central)
    for gname in GENS:
        p = prem[gname]
        add(f"premium_{gname}", f"{gname} place premium: US earnings less the same person's in Mexico", gname,
            "quantity", p["gain"], initial="in the US, 2024 earnings (CPS ASEC 2025)", alternative=alt,
            window="2024, one year", comparator="measured" if gname != "G3+" else "bounded (two moves removed)",
            weight="group_premium", tag="[CALCULATION: g2_premium.py]")
    fis, shares = fiscal_group_rows(I, pg_convention)
    for gname in GENS:
        add(f"us_budget_value_{gname}", f"{gname}: US taxes paid and services and transfers received, as valued",
            gname, "transfer (valued)", fis[gname]["value"], initial="US budget flows attributed to the group",
            alternative="no US budget flows", window="2024", comparator="measured (account lines x V/G)",
            weight="group_fiscal", tag="[CALCULATION: valuation.py; FRAMING-SENSITIVE: V/G and public goods]")
    # Other residents: the account's channels, at the pinned winners commit.
    ch, sp = I["ch"], I["specs"]
    A = {e: -sp.loc[e, "A_bn"] for e in ("low", "high")}          # direct response, positive = cost to others
    F = {e: sp.loc[e, "F_bn"] for e in ("low", "high")}
    fut = ch.loc["future_taxpayers"]
    fisc = ch.loc["fiscal"]
    # Capped programs (rental assistance and LIHEAP, from the Sept 27 case on) are paid for by the eligible
    # households that go without them, not by taxpayers; the winners lane's fiscal channel then leaves them out.
    disp = ch.loc["displaced_beneficiaries"] if "displaced_beneficiaries" in ch.index else None
    D = {e: 0.0 if disp is None else -disp[f"bn_{e}"] for e in ("low", "high")}   # positive = cost to them
    # The winners lane's fiscal channel is the direct response less the displaced part, plus induced receipts
    # (A - D + F, signed).
    gate("fiscal_channel_is_A_less_displaced_plus_F",
         np.isclose(fisc.bn_low, -(A["low"] - D["low"] - F["low"]), atol=1e-3)
         and np.isclose(fisc.bn_high, -(A["high"] - D["high"] - F["high"]), atol=1e-3),
         fiscal=[fisc.bn_low, fisc.bn_high], A=A, D=D, F=F)
    T = {e: A[e] - D[e] for e in ("low", "high")}               # the part taxpayers finance
    add("fiscal_others", "Other residents today: the direct fiscal cost less the borrowed federal part", "others_today",
        "transfer", lh(-(T["high"]) - fut.bn_high, -np.mean(list(T.values())) - fut.bn_central,
                       -(T["low"]) - fut.bn_low), initial="with the group", alternative="without the group",
        window="2024", comparator="measured (account)", weight="others:fiscal", tag="[DATA: winners channels]")
    add("fiscal_future", "Future taxpayers: the federal part financed by borrowing (FY2024 deficit / outlays)",
        "future_taxpayers", "transfer", lh(fut.bn_high, fut.bn_central, fut.bn_low), initial="with the group",
        alternative="without the group", window="2024 flow, paid later", comparator="measured (account)",
        weight="future", tag="[DATA: winners channels]")
    add("induced_receipts", "Other residents: induced receipts F (taxes on the production gain)", "others_today",
        "transfer", lh(min(F.values()), np.mean(list(F.values())), max(F.values())), initial="with the group",
        alternative="without the group", window="2024", comparator="measured (account)",
        weight="others:fiscal", tag="[DATA: winners fiscal_specs]")
    if disp is not None:
        vals = [disp.bn_low, disp.bn_central, disp.bn_high]
        add("displaced_beneficiaries", "Eligible households that go without capped programs (rental assistance, "
            "LIHEAP)", "others_today", "transfer", lh(min(vals), disp.bn_central, max(vals)),
            initial="with the group", alternative="without the group", window="2024",
            comparator="measured (account; incidence on eligible non-recipients)",
            weight="others:displaced_beneficiaries", tag="[DATA: winners channels; distribution lane capped_programs]")
    for cid, label, wkey in [("wages", "Other residents' wages after tax, long run", "others:wages"),
                             ("renters", "Renters' extra rent", "others:renters"),
                             ("landlords", "Landlords' extra rent receipts", "others:landlords"),
                             ("crime_victims", "Crime victims' harm (full cost)", "others:crime"),
                             ("property_crime", "Property crime", "others:mean"),
                             ("unreimbursed_care", "Unreimbursed hospital care outside budgets", "others:unreimbursed_care"),
                             ("congestion", "Road congestion", "others:mean"),
                             ("mobility", "Mobility: local-shock insurance", "others:mean")]:
        r = ch.loc[cid]
        # The winners lane's ends are scenario arms, not always around the central (renters, landlords):
        # the outer span takes the smallest and largest of the three.
        vals = [r.bn_low, r.bn_central, r.bn_high]
        add(cid, label, "others_today", "quantity" if cid in ("crime_victims", "property_crime", "congestion",
                                                              "unreimbursed_care") else "transfer",
            lh(min(vals), r.bn_central, max(vals)), initial="with the group", alternative="without the group",
            window="2024", comparator="measured (account)" if cid not in ("crime_victims", "property_crime")
            else "US measured; the harm the same offenders would do in Mexico is unknown (a gain to Mexico's "
                 "residents here, not zero)", weight=wkey, tag="[DATA: winners channels]")
    # The group's side of those channels.
    unc = ch.loc["unreimbursed_care"]
    pop = shares["pop"]
    for gname in GENS:
        add(f"uncompensated_received_{gname}", f"{gname}: unreimbursed hospital care received, as valued", gname,
            "transfer (valued)", lh(min(-unc.bn_low, -unc.bn_high) * health_vg[0] * pop[gname],
                                    -unc.bn_central * health_vg[1] * pop[gname],
                                    max(-unc.bn_low, -unc.bn_high) * health_vg[2] * pop[gname]),
            initial="care received in the US", alternative="none (Mexico's care is in the Mexico budget row)",
            window="2024", comparator="measured", weight="group_fiscal",
            tag="[CALCULATION: channel x Medicaid V/G; INFERENCE]")
    victims = float(I["gf"].set_index("item").filter(like="victims inside", axis=0).bn_central.iloc[0])
    for gname in GENS:
        add(f"ingroup_victims_{gname}", f"{gname}: victimization by the group's own offenders in the US", gname,
            "quantity", lh(victims * pop[gname], victims * pop[gname], victims * pop[gname]),
            initial="in the US", alternative="victimization in Mexico: unknown (Mexico's 2023 homicide rate is 24.9 "
            "per 100,000 against 5.8 in the US)", window="2024", comparator="unknown counterpart (not zero)",
            weight="group_fiscal", tag="[DATA: winners group frame; WDI VC.IHR.PSRC.P5]")
    # Remittances.
    remit = float(I["gf"].set_index("item").filter(like="remittances received", axis=0).bn_central.iloc[0])
    # The split is held at its central scenario at every end: it moves money between G1 and G2 only.
    g2r = prem["G2"]["e_us"] * G2_REMIT_RATE[1]
    add("remit_G1", "G1: remittances sent to Mexico", "G1", "transfer", lh(-(remit - g2r), -(remit - g2r),
                                                                          -(remit - g2r)),
        initial="sent", alternative="not sent", window="2024",
        comparator="measured total; generation split a scenario (G2 0-5.2% of earnings)", weight="group_remit",
        tag="[DATA: Banxico via winners; INFERENCE: split]")
    add("remit_G2", "G2: remittances sent to Mexico (1.6% of earnings, scenario)", "G2", "transfer",
        lh(-g2r, -g2r, -g2r), initial="sent", alternative="not sent", window="2024",
        comparator="scenario (0-5.2% of earnings)", weight="group_remit", tag="[INFERENCE: remit_leak arms]")
    add("remit_mexico", "Mexico's residents: remittances received", "mexico_residents", "transfer",
        lh(remit, remit, remit), initial="received", alternative="not received", window="2024",
        comparator="measured", weight="mexico_recipients", tag="[DATA: Banxico via winners]")
    # Mexico's budget in the alternative world: the group loses its value, Mexico's residents save its cost.
    mx = I["mxb"]
    for gname in GENS:
        s = mx[mx.generation == gname].set_index("item")
        ed = float(s.filter(like="school", axis=0).bn.iloc[0])
        he = float(s.filter(like="health", axis=0).bn.iloc[0])
        cash = float(s[s.cls == "cash"].bn.sum())
        pg = float(s[s.cls == "public_good"].bn.iloc[0])
        pg_val = pg if pg_convention == "average_cost" else pg * MEXICO_PUBLIC_RESPONSE[1]
        add(f"mexico_budget_lost_{gname}", f"{gname}: Mexico's health, cash and public services forgone, as valued",
            gname, "transfer (valued)", lh(-(he * health_vg[2] + cash + pg_val), -(he * health_vg[1] + cash + pg_val),
                                           -(he * health_vg[0] + cash + pg_val)),
            initial="not in Mexico", alternative="Mexico's budget per person at the group's ages",
            window="2024", comparator="measured (ENIGH, WDI)", weight="group_mexico_budget",
            tag="[CALCULATION: valuation.py mexico_budget]")
        add(f"mexico_budget_saved_{gname}", f"Mexico's residents: budget not spent on {gname} (schools, health, cash, "
            "public services)", "mexico_residents", "transfer", lh(ed + he + cash + pg * MEXICO_PUBLIC_RESPONSE[0],
                                                                    ed + he + cash + pg * MEXICO_PUBLIC_RESPONSE[1],
                                                                    ed + he + cash + pg * MEXICO_PUBLIC_RESPONSE[2]),
            initial="not spent", alternative="spent on the group", window="2024", comparator="measured (ENIGH, WDI)",
            weight="mexico_budget", tag="[CALCULATION; INFERENCE: public services respond 0.60-0.85]")
    # Mexican taxes the group would pay, bounded on both sides (the premium is gross, so they are a transfer from
    # the group to Mexico's residents in the alternative world). 'withheld', the lower bound: the income tax and
    # employee contributions withheld from formal pay (2024 statute), with no consumption or other taxes.
    # 'withheld_consumption', the central: those plus IVA, IEPS and the fuel excise on gross pay at the household
    # decile's rate (SHCP 2026), the counterpart of the US sales and excise taxes the group's US row subtracts.
    # 'proportional', the upper bound: all central-government taxes in proportion to gross labor income.
    if mexico_taxes == "withheld":
        tb = {g: prem[g]["tax"] for g in GROUP}
        how, tag = "lower bound: withheld from formal pay", "[CALCULATION: mexico.py statutory withholding; lower bound]"
    elif mexico_taxes == "withheld_consumption":
        tb = {g: {e: prem[g]["tax"][e] + prem[g]["ctax"][e] for e in ("low", "central", "high")} for g in GROUP}
        how = "central: withheld, plus IVA, IEPS and the fuel excise at the household decile's rate"
        tag = ("[CALCULATION: mexico.py withholding + SHCP 2026 IVA and IEPS incidence and the 2024 fuel excise by "
               "household decile x gross pay]")
    elif mexico_taxes == "proportional":
        tb, _ = mexico_tax_bound(I, prem)
        how, tag = "upper bound: proportional to labor income", "[CALCULATION: WDI tax share x ENIGH gross labor-income share; upper bound]"
    else:
        raise SystemExit(f"[BLOCKED] unknown mexico_taxes {mexico_taxes!r}")
    comp = f"{'estimated' if mexico_taxes == 'withheld_consumption' else 'bounded'} ({how})"
    for gname in GROUP:
        t = tb[gname]
        add(f"mexico_taxes_avoided_{gname}", f"{gname}: Mexican taxes not paid ({how})", gname, "transfer",
            lh(t["low"], t["central"], t["high"]), initial="not paid", alternative="paid in Mexico", window="2024",
            comparator=comp, weight="group_mexico_budget", tag=tag)
        add(f"mexico_taxes_lost_{gname}", f"Mexico's residents: taxes {gname} would have paid ({how})",
            "mexico_residents", "transfer", lh(-t["low"], -t["central"], -t["high"]), initial="not received",
            alternative="received", window="2024", comparator=comp, weight="mexico_budget", tag=tag)
    if short_run:
        rows += mishra_rows(I, prem)
    return pd.DataFrame(rows), prem, shares


def mishra_rows(I, prem):
    return []   # the short-run block is a sensitivity in the meta (short_run_block), never in the tables


def short_run_block(I):
    """Short run (capital fixed), a sensitivity beside the long-run tables. Mishra (IMF WP/06/86) finds the
    1970-2000 outflow, 16% of Mexico's labor force in 2000, raised stayers' wages 8% on average; stayer workers
    gained 5.9% of GDP and owners of fixed factors lost 6.4%, a net loss of 0.5% (p. 4). The alternative world here
    adds the whole group's workers to Mexico, a shock m. The wage effect and the stayers' gain scale with m/0.16, and
    the net triangle with its square; the owners lose both, so the three add up at any m [INFERENCE: linear demand].
    The group's own premium rises as Mexico's wage falls: g2_premium's Mishra variant (category effects of the 2000
    shock) scaled by the same ratio."""
    g = I["g2"]
    sel = lambda gen, conv, mis, sel_, ppp="gdp", f=0.25: g[(g.generation == gen) & (g.convention == conv)
                                                           & (g.ppp == ppp) & (g.diploma_reread == f)
                                                           & (g.mishra == mis) & (g.selection == sel_)].iloc[0]
    c = pd.read_csv(DERIVED / "mexico_earnings_cells.csv")
    mx_employed = float((c.persons * c.employment_rate).sum())
    w1 = sel("G1", "own_schooling_all_ages", False, "p56")
    w2 = sel("G2", "rearing", False, "none")
    workers = (w1.persons_15plus_m * w1.employment_mx_15plus + w2.persons_15plus_m * w2.employment_mx_15plus) * 1e6
    g3 = g[g.generation == "G3+"].iloc[0]
    workers_g3 = g3.persons_15plus_m * 1e6 * w2.employment_mx_15plus
    gdp = json.load(open(DERIVED / "mexico_meta.json"))["comparators"]["gdp_ppp_2024"] / 1e9
    out = {}
    for label, wk in (("G1_G2", workers), ("G1_G2_G3", workers + workers_g3)):
        m = wk / mx_employed
        k = m / MISHRA["shock"]
        d1 = sel("G1", "own_schooling_all_ages", True, "p56").gain_bn - w1.gain_bn
        d2 = sel("G2", "rearing", True, "none").gain_bn - w2.gain_bn
        gain, net = MISHRA["stayers_gain"] * gdp * k, -MISHRA["net_loss"] * gdp * k ** 2
        out[label] = dict(workers_m=wk / 1e6, mexico_employed_m=mx_employed / 1e6, shock_m=m, scale=k,
                          premium_rise_G1_bn=d1 * k, premium_rise_G2_bn=d2 * k,
                          stayer_workers_gain_bn=gain, fixed_factor_owners_loss_bn=net - gain, mexico_net_bn=net)
    # At Mishra's own shock (k = 1) the owners lose his 6.4% of GDP.
    gate("short_run_owners_loss_reproduces_mishra",
         abs(MISHRA["stayers_gain"] + MISHRA["net_loss"] - MISHRA["owners_loss"]) < 1e-12)
    return out


def hours_beside(I):
    """Beside the tables: the group works fewer hours in the US; at Mexico's wage, the hours not worked are worth
    E_MX x (1 - h_US/h_MX) among workers [INFERENCE: leisure valued at the forgone wage]."""
    g = I["g2"]
    out = {}
    for gen, conv, sel_ in (("G1", "own_schooling_all_ages", "p56"), ("G2", "rearing", "none")):
        r = g[(g.generation == gen) & (g.convention == conv) & (g.ppp == "gdp") & (g.diploma_reread == 0.25)
              & (g.mishra == False) & (g.selection == sel_)].iloc[0]
        out[gen] = dict(hours_us=r.weekly_hours_us_workers, hours_mx=r.weekly_hours_mx_workers,
                        employment_us=r.employment_us_15plus, employment_mx=r.employment_mx_15plus,
                        leisure_value_bn=r.mexico_earnings_bn * (1 - r.weekly_hours_us_workers
                                                                 / r.weekly_hours_mx_workers))
    return out


# ------------------------------------------------------------------ weights
def channel_factors(I, measure):
    """Per channel of other residents: the ratio of the weighted to the unweighted sum over percentiles, for
    Hendren's g and for log-income weights (distribution lane, pinned)."""
    d = I["dist"][I["dist"].measure == measure]
    g = np.interp(d.percentile, I["gtab"]["quantile"], I["gtab"]["g"])
    # Log weights per percentile: reference income per head over each person's household income per head
    # (weights.py log_weights_by_percentile.csv, on the distribution lane's own bins).
    lwt = pd.read_csv(DERIVED / "log_weights_by_percentile.csv").set_index("percentile")
    lwp = lwt.log_weight_pc
    lw = d.percentile.map(lwp).to_numpy()
    gate("log_weight_bins_complete", np.isfinite(lw).all())
    # weights.py builds its bins with the distribution lane's loader from the working tree; the pinned channels must
    # sit on the same bins (persons per percentile, to the 6 significant digits the bin file keeps).
    fa = d[d.channel == "fiscal_a"].set_index("percentile").persons_m
    gate("log_weight_bins_match_pinned_channels", len(fa) == 100
         and bool(np.allclose(fa, lwt.persons_m.reindex(fa.index), rtol=1e-5, atol=0)),
         max_rel_diff=float((fa / lwt.persons_m.reindex(fa.index) - 1).abs().max()))
    out = {}
    for c, s in d.assign(g=g, lw=lw).groupby("channel"):
        tot = s.bn.sum()
        # A channel whose percentile values change sign (wages, housing net) nets to a small sum, so a ratio of
        # weighted to unweighted sums is meaningless; it gets the additive reweighting instead.
        mixed = bool((s.bn > 0).any() and (s.bn < 0).any())
        out[c] = dict(unweighted=tot, mixed=mixed, g=(s.bn * s.g).sum() / tot, inv_g=(s.bn / s.g).sum() / tot,
                      log=(s.bn * s.lw).sum() / tot, add_g=(s.bn * s.g).sum() - tot, add_log=(s.bn * s.lw).sum() - tot)
    persons = d[d.channel == "fiscal_a"]
    pw = persons.persons_m.to_numpy()
    out["mean"] = dict(g=float(np.average(np.interp(persons.percentile, I["gtab"]["quantile"], I["gtab"]["g"]),
                                          weights=pw)),
                       log=float(np.average(persons.percentile.map(lwp), weights=pw)), inv_g=1.0, mixed=False)
    return out


def saving_leak(I, rows, res, measure="money"):
    """Claim 2's productive-use reading, as a leak per dollar the payers lose: theta x s_p x tau x m, reported at
    theta = 1 (every forgone dollar of saving would have been domestic capital) and the group saving none of what
    it receives, both the reading's most favourable case. s_p weights MSS_SAVING by the payers' shares of the
    fiscal channel under tax shares (a) and per-person cuts (b) (distribution lane, pinned). At equal weights in
    the central scenario (rows: build_rows' default; res: the case's totals), each leak is also given in dollars on
    the tax-financed rows, the ones λ scales, and as the US-only break-even w it implies."""
    d = I["dist"][I["dist"].measure == measure]
    tax = float(rows[rows.weight.isin(["others:fiscal", "future"])].central.sum())
    t = res[(res.pg_convention == "average_cost") & (res.mexico_taxes == "withheld_consumption")
            & (res.scenario == "central_g3_zero") & (res.weighting == "equal")].set_index("party").bn
    gate("saving_leak_central_totals", len(t) > 0 and t.group_total > 0 and tax < 0)
    out = dict(inputs=dict(saving_by_percentile=MSS_SAVING, capital_tax=CAPITAL_TAX,
                           return_over_discount=RETURN_OVER_DISCOUNT, theta=1.0, group_saving=0.0),
               tax_financed_central_bn=tax, breakeven_w_us_only_equal=float(-t.us_residents_total / t.group_total))
    for conv in ("a", "b"):
        s = d[d.channel == f"fiscal_{conv}"].set_index("percentile").bn
        rate = pd.Series(np.nan, index=s.index)
        for lo, hi, r in MSS_SAVING:
            rate[(s.index >= lo) & (s.index <= hi)] = r
        gate(f"saving_rates_cover_payers_{conv}", len(s) == 100 and bool(rate.notna().all()))
        gate(f"payers_all_lose_{conv}", bool((s <= 0).all()), gains=float(s[s > 0].sum()))
        sp = float((s * rate).sum() / s.sum())
        leaks = {f"tau_{x}_m_{m}": sp * x * m for x in CAPITAL_TAX for m in RETURN_OVER_DISCOUNT}
        out[conv] = dict(payer_saving_rate=sp, leak_per_dollar=leaks,
                         leak_bn={k: v * tax for k, v in leaks.items()},
                         breakeven_w_us_only_equal={k: float(-(t.us_residents_total + v * tax) / t.group_total)
                                                    for k, v in leaks.items()})
    return out


def generation_breakeven(I, rows, res):
    """Each generation alone, at equal weights in the central scenario: the weight on it at which its row equals the
    net fiscal cost it puts on other residents (the generation lane's cost, convention (a), the mean of the two band
    ends, as the central fiscal rows take it). The other residents' non-fiscal channels (wages, rents, crime,
    congestion) are not split by generation and are left out; their central total is reported beside (rows:
    build_rows' default). G3+ is given at both bounds of its premium."""
    gr = I["gen"][I["gen"].convention == "a"]
    c = res[(res.pg_convention == "average_cost") & (res.mexico_taxes == "withheld_consumption")
            & (res.weighting == "equal")]
    others = rows[rows.party == "others_today"]
    out = dict(others_nonfiscal_central_bn=float(others[~others.weight.eq("others:fiscal")].central.sum()))
    for g in GENS:
        cost = gr[gr.generation == g.replace("+", "plus")].cost_bn
        gate(f"generation_cost_at_two_ends_{g}", len(cost) == 2, n=len(cost))
        out[g] = dict(fiscal_cost_ends_bn=sorted(float(x) for x in cost), fiscal_cost_central_bn=float(cost.mean()))
        for b in ("zero", "upper") if g == "G3+" else ("zero",):
            row = float(c[(c.scenario == f"central_g3_{b}") & (c.party == g)].bn.item())
            gate(f"generation_row_positive_{g}_{b}", row > 0, row=row)
            key = f"_g3_{b}" if g == "G3+" else ""
            out[g][f"row_equal_central_bn{key}"] = row
            out[g][f"breakeven_w_fiscal_only{key}"] = float(cost.mean()) / row
            # The bound if every non-fiscal channel were charged to this generation alone.
            out[g][f"breakeven_w_all_nonfiscal_on_it{key}"] = (float(cost.mean())
                                                             - out["others_nonfiscal_central_bn"]) / row
    return out


def row_weight(r, col, fac, pos, I, prem, conv):
    """Multiplier on a row's dollars for weighting column col (conv: 'a' tax shares, 'b' per-person cuts)."""
    w = r.weight
    if col == "equal":
        return 1.0
    if col.startswith("equal_lambda"):
        # Revenue other residents (today and later) must raise, and Mexico's budget savings and lost taxes, carry
        # lambda.
        lam = fac["_lambda"][col]
        budget = (r.row in ("fiscal_others", "fiscal_future", "induced_receipts")
                  or r.row.startswith(("mexico_budget_saved", "mexico_taxes_lost")))
        return lam if budget else 1.0
    kind = "g" if col.startswith("hendren") else "log"
    if w.startswith("others:"):
        c = w.split(":")[1]
        if c == "fiscal":
            c = "fiscal_a" if conv == "a" else "fiscal_b"
            if kind == "g" and conv == "a":
                return 1.0                         # tax financing: weighted loss equals revenue
        if c == "mean":
            return fac["mean"][kind]
        return fac[c][kind]
    if w == "future":
        return 1.0 if kind == "g" else fac["fiscal_a"]["log"]     # assumed: financed like today's taxes
    if w.startswith("mexico"):
        if kind == "g":
            return G_MEXICO
        mx = I["wmeta"]["mexico"]                   # income per head, PPP (weights.py)
        y = mx["remittance_households_median_y"] if w == "mexico_recipients" else mx["median_y"]
        return I["wmeta"]["us_reference"]["per_capita"]["y_ref_other_mean"] / y
    # the group's rows
    gname = r.party
    p = pos[(pos.measure == "money") & (pos.party == gname)].iloc[0]
    if kind == "g":
        return p.mean_g
    return None                                   # log: finite changes, computed per generation


def group_log(rows, prem, I, end):
    """Money-metric of the group's rows under log utility: finite changes of per-person consumption, in the
    order Mexico's budget lost -> premium -> US budget valued -> remittances -> victims and care."""
    yref = I["wmeta"]["us_reference"]["per_capita"]["y_ref_other_mean"]
    out = {}
    for gname in GROUP:
        p = prem[gname]
        n = p["persons"] * 1e6
        e_us = p["e_us"] * 1e9 / n
        e_mx = p["e_mx"][end] * 1e9 / n if np.isfinite(p["e_mx"][end]) else np.nan
        g = rows[rows.party == gname].set_index("row")
        per = lambda rid: g.loc[rid, end] * 1e9 / n
        m = -per(f"mexico_budget_lost_{gname}")
        if f"mexico_taxes_avoided_{gname}" in g.index:
            m -= per(f"mexico_taxes_avoided_{gname}")      # taxes paid in Mexico lower the alternative's consumption
        v = per(f"us_budget_value_{gname}")
        rem = -per(f"remit_{gname}") if f"remit_{gname}" in g.index else 0.0
        vic = per(f"ingroup_victims_{gname}") + per(f"uncompensated_received_{gname}")
        steps = {}
        if not np.isfinite(e_mx):
            out[gname] = {k: np.nan for k in g.index}
            continue
        c = e_mx + m
        chain = [(f"mexico_budget_lost_{gname}", e_mx), (f"premium_{gname}", e_us), (f"us_budget_value_{gname}", e_us + v),
                 (f"remit_{gname}", e_us + v - rem), ("_vic", e_us + v - rem + vic)]
        for rid, nxt in chain:
            steps[rid] = yref * n * (np.log(nxt) - np.log(c)) / 1e9 if nxt > 0 and c > 0 else np.nan
            c = nxt
        steps[f"ingroup_victims_{gname}"] = steps.pop("_vic")
        steps[f"uncompensated_received_{gname}"] = 0.0          # folded into the victims step above
        if f"mexico_taxes_avoided_{gname}" in g.index:
            steps[f"mexico_taxes_avoided_{gname}"] = 0.0         # folded into the Mexico-budget step
        out[gname] = steps
    return out


def totals(rows, prem, I, end, fac, pos):
    cols = ["equal"] + list(fac["_lambda"]) + ["hendren_a", "hendren_b", "log_a", "log_b"]
    res = []
    glog = group_log(rows, prem, I, end)
    for col in cols:
        conv = "b" if col.endswith("_b") else "a"
        party_tot = {p: 0.0 for p in PARTIES}
        unknown = {p: [] for p in PARTIES}
        for r in rows.itertuples():
            x = getattr(r, end)
            if not np.isfinite(x):
                unknown[r.party].append(r.row)
                continue
            if col.startswith("log") and r.party in GROUP:
                val = glog[r.party].get(r.row, np.nan)
                if not np.isfinite(val):
                    unknown[r.party].append(r.row)
                    continue
                party_tot[r.party] += val
                continue
            c = r.weight.split(":")[1] if r.weight.startswith("others:") else None
            if c in fac and fac[c].get("mixed") and not col.startswith("equal"):
                party_tot[r.party] += x + fac[c]["add_g" if col.startswith("hendren") else "add_log"]
                continue
            party_tot[r.party] += x * row_weight(r, col, fac, pos, I, prem, conv)
        N = sum(party_tot[p] for p in PARTIES if p not in GROUP)
        N_us = party_tot["others_today"] + party_tot["future_taxpayers"]
        M = sum(party_tot[p] for p in GROUP)
        for p in PARTIES:
            res.append(dict(weighting=col, party=p, bn=party_tot[p], unknown_rows=";".join(unknown[p])))
        res.append(dict(weighting=col, party="non_group_total", bn=N, unknown_rows=""))
        res.append(dict(weighting=col, party="group_total", bn=M, unknown_rows=""))
        res.append(dict(weighting=col, party="world_total", bn=N + M, unknown_rows=""))
        res.append(dict(weighting=col, party="breakeven_w", bn=(-N / M) if (M > 0 and N < 0) else np.nan,
                        unknown_rows="" if (M > 0 and N < 0) else "none: the non-group parties gain"))
        res.append(dict(weighting=col, party="us_residents_total", bn=N_us, unknown_rows=""))
        res.append(dict(weighting=col, party="breakeven_w_us_only", bn=(-N_us / M) if (M > 0 and N_us < 0) else np.nan,
                        unknown_rows="Mexico's residents left out of N"))
    return pd.DataFrame(res)


def write_case(path, new, case):
    """Replace one case's rows in a file holding several cases, keeping the others, cases in sorted order and
    columns in this code's order, so a rebuild and a first build agree. A first write takes the new rows alone:
    concatenating a column-only frame would change the dtypes and the format."""
    if path.exists():
        old = pd.read_csv(path)
        new = pd.concat([old[old.case != case], new]).sort_values("case", kind="mergesort")[list(new.columns)]
    new.to_csv(path, index=False, lineterminator="\n", float_format="%.6f")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="sept26_schools", choices=sorted(PINS))
    args = ap.parse_args()
    I = load(args.case)
    pos = I["pos"]
    out, detail = [], []
    for measure in ("money",):
        fac = channel_factors(I, measure)
        gate("displaced_channel_distributed", "displaced_beneficiaries" not in I["ch"].index
             or "displaced_beneficiaries" in fac)
        fac["_lambda"] = {f"equal_lambda_{k}": v for k, v in LAMBDAS.items()}
        fac["_lambda"]["equal_lambda_hendren_a"] = fac["fiscal_a"]["inv_g"]
        for pgc in ("average_cost", "response_only"):
            for mtx in ("withheld", "withheld_consumption", "proportional"):
                # G3+ has bounds only: the central scenario is reported at each bound; the outer spans take the
                # lower bound at their low end and the upper at their high end, whichever central is built.
                for g3 in ("zero", "upper"):
                    rows, prem, shares = build_rows(I, pgc, mexico_taxes=mtx, g3_central=g3)
                    detail.append(rows.assign(case=args.case, pg_convention=pgc, mexico_taxes=mtx, g3_central=g3))
                    for end in ("low", "central", "high") if g3 == "zero" else ("central",):
                        scen = {"low": "low_outer", "high": "high_outer", "central": f"central_g3_{g3}"}[end]
                        out.append(totals(rows, prem, I, end, fac, pos).assign(
                            case=args.case, pg_convention=pgc, mexico_taxes=mtx, scenario=scen))
    res = pd.concat(out)[["case", "pg_convention", "mexico_taxes", "scenario", "weighting", "party", "bn",
                          "unknown_rows"]]
    write_case(DERIVED / "world_ledger.csv", res, args.case)
    write_case(DERIVED / "world_ledger_rows.csv", pd.concat(detail), args.case)
    write_case(DERIVED / "generation_split_check.csv", generation_split_check(I, args.case), args.case)
    rows_c, prem_c, _ = build_rows(I)
    rate, rate_inputs = mexico_consumption_tax_rate()
    meta = dict(case=args.case, pins=PINS[args.case], channel_factors=channel_factors(I, "money"),
                lambda_hendren_tax_shares=channel_factors(I, "money")["fiscal_a"]["inv_g"],
                generation_shares=shares, short_run_block=short_run_block(I), hours_beside=hours_beside(I),
                saving_leak=saving_leak(I, rows_c, res), generation_breakeven=generation_breakeven(I, rows_c, res),
                mexico_tax_bound=dict(zip(("by_generation_bn", "inputs"), mexico_tax_bound(I, prem_c))),
                mexico_withheld_tax_bn={g: prem_c[g]["tax"] for g in GROUP},
                mexico_consumption_tax=dict(
                    by_generation_bn={g: prem_c[g]["ctax"] for g in GROUP},
                    source="SHCP 2026 IVA and IEPS incidence plus the 2024 fuel excise, by household decile x gross "
                           "pay (mexico.py)",
                    wdi_check=dict(rate=rate, inputs=rate_inputs, basis="rate x take-home pay", by_generation_bn={
                        g: {e: rate * prem_c[g]["home"][e] for e in ("low", "central", "high")} for g in GROUP})))
    json.dump(meta, open(DERIVED / f"world_ledger_meta_{args.case}.json", "w"), indent=1, sort_keys=True,
              default=float)
    show = res[(res.pg_convention == "average_cost") & (res.mexico_taxes == "withheld_consumption")
               & res.party.isin(PARTIES + ["world_total", "breakeven_w", "breakeven_w_us_only"])]
    print(show.pivot_table(index=["scenario", "party"], columns="weighting", values="bn", sort=False).round(1)
          .to_string(), file=sys.stderr)


if __name__ == "__main__":
    main()
