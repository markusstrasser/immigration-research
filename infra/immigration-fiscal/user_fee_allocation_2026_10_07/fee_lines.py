"""Assemble the fee terms the brief asks for and the key terms found beside them, line by line, for case.cjs.

Fee term (the question). For a NIPA sales line R, the group's true net subsidy is s_U G - s_R R, with G = N + R the
gross cost, s_U the group's share of use (of the gross service) and s_R its share of the fees paid. The account charges
s_K N, s_K the key it applies to the net N. The difference splits exactly as
    s_U G - s_R R - s_K N = (s_U - s_R) R + (s_U - s_K) N,
the fee term and the key term. The brief's form (s_C - s_R) R, with s_C the account's key, is the fee term measured at
s_K instead of s_U; it is the whole difference only when the key is right (s_K = s_U). It is reported beside.

Lines with R >= $20bn (NIPA T3.10.5, 2024): S&L tuition and related educational charges ($103.9bn), S&L health and
hospital charges ($364.1bn) and S&L other sales ($215.8bn); federal sales are $12.0bn. Government enterprises sit
outside consumption: the account holds their current surplus as a receipt, so fares, tolls and utility bills are
netted inside it and their key is the receipt's.

  - Tuition: s_U and s_R from higher_ed.py (IPEDS x ACS), carried to the account's union by phi = union / ACS group
    [ASSUMPTION: the union members the ACS does not see use and pay as those it sees]. The account's key on the
    higher-education part of its education line is the ledger's item P as the case implements it: row 6's re-blend
    at weight W on the school key and 1 - W on P, at the line's row-4 factor f, so P_eff = hf x f x Tp/Np. Gate: the
    case's row-6 college edit is reproduced from W, hf, f and the components.
  - Health: health.py's MEPS shares by payer and the payers' cost shares and payment-to-cost ratios give the fee term
    on the insured payers and the residual sum_p a_p (s_p - s_K) (fee and key terms together); the uninsured term is
    the uncompensated care the case charges by use. MEPS shares go on the union's frame by the ratio of its population
    share to MEPS's [central; raw shares an arm]; s_K is the union's health key in the case.
  - Other sales: not measured; parking, parks, solid waste, school lunches and college auxiliaries are paid per use,
    so the fee term is taken as zero. derived/other_sales.csv gives the composition.

Key terms beside the question (each changes the same education or enterprise block):
  - key_higher_ed: (U - P_eff) x the line's higher-education dollars.
  - key_k12_weight: the case re-blends at W = 0.795; BEA's government-wide K-12 is 0.775 of the line (T3.16 line 31
    over T3.17 line 9, the audit's own 0.77; its 0.82 takes the education benefits out of a consumption line that
    already excludes them). Arms: the S&L mix 0.777, federal education consumption all non-K-12 (0.769) or all K-12
    (0.779). Post-engine (case.cjs), because the
    case's K-12 key depends on the specification's school fraction s: n x (w_K - W) x (K_eff(s) - P_eff).
  - capital keys by part: the return on college and on K-12 structures both take the whole line's blend as their key.
    The college stock's use key is kappa U + (1 - kappa) P_eff, kappa the higher-education share of non-K-12
    education investment; the K-12 stock's is the case's K-12 key at the school price. Post-engine.
  - key_pell: Pell grants sit in other_federal_benefits (T3.12 l26, note 7: "aid to students"), keyed by CPS cash
    income; the group's Pell share from higher_ed.py.
  - key_transit: the transit loss (T3.8 l14) inside the enterprise-surplus receipt is keyed by population; the group's
    share of transit commuters (acs_transit.py) stands in for rides. Operating here; capital post-engine.

Union reads: model.json's cell plus the payload's edits before the lineage's (meta.lineage.edits.first), applied as
engine.js applies them; case.cjs checks every read against the engine. The lineage's 3.04M added people carry no fee or
key term [ASSUMPTION]; case.cjs reports the per-member scaling arm.

Writes derived/fee_lines.csv, derived/higher_ed_terms.csv, derived/health_terms.csv, derived/other_sales.csv and
derived/fee_lines.json. Run from the repository root after acs_college.py, acs_transit.py, higher_ed.py and health.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/fee_lines.py
"""
import hashlib
import itertools
import json
from pathlib import Path

import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = REPO / "infra/immigration-fiscal"
OUT = HERE / "derived"
BEA = REPO / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
COG = FISCAL / "ledger_residual_agg_2026_09_16/_cache/22slsstab1.xlsx"
COG_SHA = "4dd123c5ad520e33d9692f622d389a020e2d3a7e6e782763663854dd84643b9b"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
PAYLOAD = FISCAL / "main_case_2026_10_05/derived/corrections.json"
COMPONENTS = FISCAL / "school_enrollment_2026_09_20/derived/updated_account_components.csv"
ENGINE_BASE = FISCAL / "school_cost_where_enrolled_2026_09_24/derived/engine_base.json"
ALLOCS = ["personal", "shared"]
ROW6_W = (0.77, 0.82)       # the case's re-blend weights, averaged (main_case_2026_09_24/package.cjs CENTRAL w "avg")
PELL_BN = 31.264            # [SOURCE: CRS IF12780 (2024-10-09) Table 2, Pell aid awarded FY2023, ED FY2025 budget justification]
PELL_PUBLIC = {"central": 0.68, "low": 0.58, "high": 0.75}            # [ASSUMPTION] public institutions' share of Pell
PELL_PRIVATE_RELATIVE = {"central": 0.75, "low": 0.5, "high": 1.0}   # [ASSUMPTION] group share at private / at public
BOUND_GAP = 0.01            # the other-sales sensitivity: a 0.01 gap between use and fee shares
CENTRAL_WEIGHTS = "consolidated"   # the education line's K-12 / higher / other split (arms: sl_mix, federal_*)


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def bea():
    if sha(BEA) != BEA_SHA:
        raise SystemExit("[BLOCKED] the BEA workbook is not the pinned vintage")
    b = openpyxl.load_workbook(BEA, read_only=True, data_only=True)
    out = {}
    for sheet in ["T31005-A", "T31700-A", "T31600-A", "T31505-A", "T30800-A", "T31200-A"]:
        rows = list(b[sheet].values)
        hdr = [r for r in rows if r[0] == "Line"][0]
        j = [i for i, x in enumerate(hdr) if str(x) == "2024"][0]
        out[sheet] = {int(r[0]): (r[1].strip(), r[j] / 1000) for r in rows if r[0] and str(r[0]).isdigit()
                      and isinstance(r[j], (int, float))}
    b.close()
    return out


def cell(t, sheet, line, label):
    lab, v = t[sheet][line]
    if not lab.startswith(label):
        raise SystemExit(f"[BLOCKED] {sheet} line {line} is {lab!r}, not {label!r}")
    return v


def census_charges():
    if sha(COG) != COG_SHA:
        raise SystemExit("[BLOCKED] the Census 2022 finance table is not the pinned file")
    ws = openpyxl.load_workbook(COG, read_only=True, data_only=True).active
    return {r[0]: (str(r[1]).strip(), r[2] / 1e6) for r in ws.values if isinstance(r[0], int) and r[2] is not None}


def union_spending(model, payload, line, key, alloc):
    """The union's amount on a spending line and key, and the line's national total."""
    first = payload["meta"]["lineage"]["edits"]["first"]
    if any(x["id"] == line for x in payload["lines"]):
        target, national = 0.0, 0.0
    else:
        x = next(x for x in model["spending"]["lines"] if x["id"] == line)
        target, national = x["keys"][key][alloc]["target_bn"], x["national_bn"]
    for e in payload["edits"][:first]:
        if e.get("side") != "spending" or e.get("line") != line:
            continue
        if "national_bn" in e:
            target *= e["national_bn"] / national
            national = e["national_bn"]
        elif e["key"] == key:
            target += e["by"][alloc]
    return target, national


def union_receipt(model, payload, line, alloc):
    """The union's amount on a receipt line at the reference incidence rule, and the line's national total."""
    first = payload["meta"]["lineage"]["edits"]["first"]
    scenario = model["receipts"]["reference"]
    x = next(x for x in model["receipts"]["lines"] + payload.get("receipt_lines", []) if x["id"] == line)
    target, national = x["cells"][scenario][alloc]["target_bn"], x["national_bn"]
    for e in payload["edits"][:first]:
        if e.get("side") != "receipt" or e.get("line") != line:
            continue
        if "national_bn" in e:
            target *= e["national_bn"] / national
            national = e["national_bn"]
        elif e["scenario"] == scenario:
            target += e["by"][alloc]
    return target, national


def union_edits(payload, line, key):
    first = payload["meta"]["lineage"]["edits"]["first"]
    return [e for e in payload["edits"][:first] if e.get("side") == "spending" and e.get("line") == line
            and e.get("key") == key]


def main():
    t = bea()
    R_tuition = cell(t, "T31005-A", 58, "Tuition and related educational charges")
    R_health = cell(t, "T31005-A", 59, "Health and hospital charges")
    R_other = cell(t, "T31005-A", 60, "Other sales")
    R_sl = cell(t, "T31005-A", 57, "Less: Sales to other sectors")
    R_fed = cell(t, "T31005-A", 22, "Less: Sales to other sectors")
    if abs(R_tuition + R_health + R_other - R_sl) > 0.002:
        raise SystemExit("[BLOCKED] S&L sales do not add to their parts")
    n_edu = cell(t, "T31700-A", 9, "Education")             # all-government education consumption: the line
    sl_edu = cell(t, "T31700-A", 30, "Education")            # S&L education consumption
    if abs(cell(t, "T31700-A", 21, "State and local") - cell(t, "T31005-A", 47, "State and local consumption")) > 0.002:
        raise SystemExit("[BLOCKED] T3.17 line 21 is not S&L consumption")
    sl_ben = cell(t, "T31200-A", 40, "Education")            # S&L education social benefits
    sub = {k: cell(t, "T31600-A", n, k) for n, k in [(106, "Education"), (107, "Elementary and secondary"),
                                                     (108, "Higher"), (109, "Libraries and other")]}
    gross = {k: cell(t, "T31505-A", n, k) for n, k in [(109, "Education"), (110, "Elementary and secondary"),
                                                       (111, "Higher"), (112, "Libraries and other")]}
    # S&L education current expenditure (T3.16) is consumption plus the education social benefits; the benefits sit
    # in "libraries and other", the only placement that leaves every subfunction's gross investment (T3.15.5 less
    # consumption) non-negative.
    if abs(sub["Education"] - sl_edu - sl_ben) > 0.002:
        raise SystemExit("[BLOCKED] T3.16 S&L education is not consumption plus education benefits")
    cons = {"k12": sub["Elementary and secondary"], "higher": sub["Higher"], "libother": sub["Libraries and other"] - sl_ben}
    invest = {"k12": gross["Elementary and secondary"] - cons["k12"], "higher": gross["Higher"] - cons["higher"],
              "libother": gross["Libraries and other"] - cons["libother"]}
    if min(invest.values()) < 0 or gross["Libraries and other"] - sub["Libraries and other"] >= 0:
        raise SystemExit("[BLOCKED] the benefits' placement no longer follows from the investment sign")
    fed_edu = n_edu - sl_edu
    # Government-wide K-12 (T3.16 line 31, consolidated, so federal grants to S&L drop out) less S&L K-12 is federal
    # K-12, taken as consumption; the rest of federal education consumption splits like S&L's non-K-12 parts.
    if cell(t, "T31600-A", 30, "Education") <= sub["Education"]:
        raise SystemExit("[BLOCKED] T3.16 line 30 is not government-wide education")
    fed_k12 = cell(t, "T31600-A", 31, "Elementary and secondary") - cons["k12"]
    if not 0 <= fed_k12 <= fed_edu:
        raise SystemExit("[BLOCKED] government-wide K-12 less S&L K-12 is not inside federal education consumption")
    fed_rest = fed_edu - fed_k12
    non_k12 = cons["higher"] + cons["libother"]
    weights = {   # shares of the line's dollars (K-12, higher, libraries and other)
        "consolidated": {"k12": (cons["k12"] + fed_k12) / n_edu,
                         "higher": (cons["higher"] + fed_rest * cons["higher"] / non_k12) / n_edu,
                         "libother": (cons["libother"] + fed_rest * cons["libother"] / non_k12) / n_edu},
        "sl_mix": {k: v / sl_edu for k, v in cons.items()},
        "federal_non_k12": {"k12": cons["k12"] / n_edu, "higher": cons["higher"] / n_edu,
                            "libother": (cons["libother"] + fed_edu) / n_edu},
        "federal_k12": {"k12": (cons["k12"] + fed_edu) / n_edu, "higher": cons["higher"] / n_edu,
                        "libother": cons["libother"] / n_edu},
    }
    kappa = invest["higher"] / (invest["higher"] + invest["libother"])
    transit_loss = -cell(t, "T30800-A", 14, "Public transit")

    model = json.loads(MODEL.read_text())
    p = json.loads(PAYLOAD.read_text())
    L = p["meta"]["lineage"]
    union, lineage = L["counts"]["account_union"], L["counts"]["lineage_population"]
    resident = model["meta"]["resident_population"]
    acs = json.loads((OUT / "acs_population.json").read_text())
    phi = union / acs["mexican_origin"]
    hf = json.loads(ENGINE_BASE.read_text())["household_fraction"]
    edu = next(x for x in model["spending"]["lines"] if x["id"] == "education_services")
    if abs(edu["national_bn"] - n_edu) > 1e-9:
        raise SystemExit("[BLOCKED] the education line's national total is not T3.17 line 9")

    # The case's education key, as implemented: T0 x f + s x school edit + (1 - s) x college edit
    # = n hf f [W (s k + 1 - s) Ts/Ns + (1 - W) Tp/Np].
    c = pd.read_csv(COMPONENTS)
    W = sum(ROW6_W) / len(ROW6_W)
    he = n_edu * hf
    key = {}
    for a in ALLOCS:
        x = c[c.allocation == a].pivot(index="component", columns="group", values="spending_bn")
        Ts, Ns = x.loc["school", "mexican_observed_total"], x.loc["school", "national_civilian"]
        Tp, Np = x.loc["P", "mexican_observed_total"], x.loc["P", "national_civilian"]
        cell0 = edu["keys"]["education_mix"][a]
        if abs(cell0["share"] - (Ts + Tp) / (Ns + Np)) > 1e-8:
            raise SystemExit(f"[BLOCKED] the components do not give the model's education_mix share ({a})")
        T0 = cell0["target_bn"]
        if abs(T0 - he * (Ts + Tp) / (Ns + Np)) > 1e-6:
            raise SystemExit(f"[BLOCKED] hf does not give the model's education_mix target ({a})")
        row4 = union_edits(p, "education_services", "education_mix")
        school, college = union_edits(p, "school_reprice", "k"), union_edits(p, "college_rekey", "k")
        if len(row4) != 1 or len(school) != 1 or len(college) != 1:
            raise SystemExit("[BLOCKED] the union's education edits are not one row-4 edit and one re-blend pair")
        f = (T0 + row4[0]["by"][a]) / T0
        Kc, Pc = Ts / Ns, Tp / Np
        want = f * (he * (W * Kc + (1 - W) * Pc) - T0)
        if abs(want - college[0]["by"][a]) > 1e-9:
            raise SystemExit(f"[BLOCKED] row 6's college edit is not f (n hf (W K + (1 - W) P) - T0) ({a}): "
                             f"{want} vs {college[0]['by'][a]}")
        k = ((school[0]["by"][a] / f + T0) / he - (1 - W) * Pc) / (W * Kc)
        key[a] = dict(T0=T0, f=f, K_cps=Kc, P_cps=Pc, k=k, P_eff=hf * f * Pc, K_eff_unpriced=hf * f * Kc,
                      union_education_bn=T0 + row4[0]["by"][a], school_edit_bn=school[0]["by"][a],
                      college_edit_bn=college[0]["by"][a])
    if abs(key["personal"]["f"] - key["shared"]["f"]) > 1e-6 or abs(key["personal"]["P_eff"] - key["shared"]["P_eff"]) > 1e-9:
        raise SystemExit("[BLOCKED] the row-4 factor or P differs by allocation")
    P_eff = key["personal"]["P_eff"]
    benefits = next(x for x in model["spending"]["lines"] if x["id"] == "education_benefits")
    if abs(benefits["keys"]["postsecondary"]["personal"]["share"] - key["personal"]["P_cps"]) > 1e-8:
        raise SystemExit("[BLOCKED] the education benefits' postsecondary key is no longer item P")

    # Tuition: the fee term, the brief's form at the account's key, and the key term on the line's college dollars.
    he_json = json.loads((OUT / "higher_ed.json").read_text())
    U, sR = he_json["central"]["s_U"] * phi, he_json["central"]["s_R"] * phi
    w = weights[CENTRAL_WEIGHTS]
    higher_dollars = w["higher"] * n_edu
    fee_tuition = (U - sR) * R_tuition
    key_higher = (U - P_eff) * higher_dollars
    arms = pd.read_csv(OUT / "higher_ed_shares.csv")
    arms["U_union"] = arms.s_U * phi
    arms["sR_union"] = arms.s_R * phi
    arms["fee_term_bn"] = (arms.U_union - arms.sR_union) * R_tuition
    arms["fee_term_at_account_key_bn"] = (P_eff - arms.sR_union) * R_tuition
    arms["key_term_bn"] = (arms.U_union - P_eff) * higher_dollars
    arms["operating_block_bn"] = arms.fee_term_bn + arms.key_term_bn
    central_row = arms[(arms.cost == he_json["central"]["cost"]) & (arms.fee == he_json["central"]["fee"])
                       & (arms.grad_cost == he_json["central"]["grad_cost"]) & (arms.theta == he_json["central"]["theta"])
                       & (arms.pell_intensity == he_json["central"]["pell_intensity"])]
    if len(central_row) != 1 or max(abs(central_row.s_U.iloc[0] - he_json["central"]["s_U"]),
                                    abs(central_row.s_R.iloc[0] - he_json["central"]["s_R"])) > 5e-7:
        raise SystemExit("[BLOCKED] the arms table does not hold the central row once (the CSV keeps six decimals)")
    arms.to_csv(OUT / "higher_ed_terms.csv", index=False, lineterminator="\n", float_format="%.6f")

    # The K-12 weight (post-engine): n (w_K - W) (K_eff(s) - P_eff) = A + B s by allocation.
    k12_weight = {}
    for name, ww in weights.items():
        k12_weight[name] = {a: dict(A=n_edu * (ww["k12"] - W) * (key[a]["K_eff_unpriced"] - P_eff),
                                    B=n_edu * (ww["k12"] - W) * (key[a]["k"] - 1) * key[a]["K_eff_unpriced"])
                            for a in ALLOCS}
    # College capital (post-engine): the union's key in the case is (its education amount + its college edit) / n.
    U_capital = kappa * U + (1 - kappa) * P_eff
    college_key_union = {a: (key[a]["union_education_bn"] + key[a]["college_edit_bn"]) / n_edu for a in ALLOCS}
    # K-12 capital (post-engine): keyed in the case by (the education amount + the school edit) / n, the whole line's
    # blend at the school price; its use key is the K-12 key at that price, hf f k Ts/Ns.
    k12_capital_target = {a: key[a]["k"] * key[a]["K_eff_unpriced"] for a in ALLOCS}
    k12_key_union = {a: (key[a]["union_education_bn"] + key[a]["school_edit_bn"]) / n_edu for a in ALLOCS}

    # Pell: the group's share of all Pell against the union's cash-income key on other_federal_benefits.
    pell_pub = he_json["pell_share_public"]
    allcash = {a: union_spending(model, p, "other_federal_benefits", "all_cash", a) for a in ALLOCS}
    s_cash = {a: v[0] / v[1] for a, v in allcash.items()}

    def pell_share(intensity="mid", public="central", private="central"):
        return pell_pub[intensity] * phi * (PELL_PUBLIC[public] + (1 - PELL_PUBLIC[public]) * PELL_PRIVATE_RELATIVE[private])

    key_pell = {a: (pell_share() - s_cash[a]) * PELL_BN for a in ALLOCS}
    pell_arms = [dict(intensity=i, public=u, private=v, share=pell_share(i, u, v),
                      term_personal_bn=(pell_share(i, u, v) - s_cash["personal"]) * PELL_BN,
                      term_shared_bn=(pell_share(i, u, v) - s_cash["shared"]) * PELL_BN)
                 for i, u, v in itertools.product(pell_pub, PELL_PUBLIC, PELL_PRIVATE_RELATIVE)]

    # Transit: rides at the group's commuter share relative to its population share; the union's receipt key.
    tr = json.loads((OUT / "acs_transit.json").read_text())
    r_transit = tr["transit_commuter_share"] / tr["population_share"]
    ent = {a: union_receipt(model, p, "enterprise_surplus", a) for a in ALLOCS}
    s_ent = {a: v[0] / v[1] for a, v in ent.items()}
    rekey = p["meta"]["capital_return"]["enterprise_option"]["receipt_rekey"]["share"]
    if any(abs(s_ent[a] - rekey[a]) > 1e-9 for a in ALLOCS):
        raise SystemExit(f"[BLOCKED] the union's enterprise-surplus share {s_ent} is not the case's rekeyed share {rekey}")
    key_transit = {a: (r_transit - 1) * s_ent[a] * transit_loss for a in ALLOCS}
    # Mode arms: the loss as if it followed bus commuters only, or rail commuters only (subway, commuter and light rail).
    modes = {int(k): v for k, v in tr["by_mode"].items()}
    mode_ratio = {"bus": modes[2]["group_share"] / tr["population_share"],
                  "rail": sum(modes[m]["group_share"] * modes[m]["commuters"] for m in (3, 4, 5))
                  / sum(modes[m]["commuters"] for m in (3, 4, 5)) / tr["population_share"]}
    transit_arms = {k: dict(ratio=v, operating_term_bn=(v - 1) * s_ent["personal"] * transit_loss) for k, v in mode_ratio.items()}

    # Health: fee term and residual on the insured payers, on the union's frame and key.
    hl = json.loads((OUT / "health.json").read_text())
    sh, se = hl["meps_shares"], hl["meps_se"]
    frame = (union / resident) / sh["persons"]
    hs = {a: union_spending(model, p, "health_services", "health_other", a) for a in ALLOCS}
    sp = {a: union_spending(model, p, "state_price_health_services", "k", a)[0] for a in ALLOCS}
    s_K_health = {a: (hs[a][0] + sp[a]) / hs[a][1] for a in ALLOCS}
    payers = {"medicare": "MEDICARE", "medicaid": "MEDICAID", "private_other": "PRIVATE_OTHER"}

    def health(mix, pcr, s, s_k, g):
        cost = {q: g * mix[q] for q in mix}
        pay = {q: cost[q] * pcr[q] for q in mix}
        use = sum(cost[q] * s[q] for q in mix) / sum(cost.values())
        paid = sum(pay[q] * s[q] for q in mix) / sum(pay.values())
        fee = (use - paid) * sum(pay.values())
        residual = sum((cost[q] - pay[q]) * (s[q] - s_k) for q in mix)
        return dict(s_U=use, s_R=paid, fee_term_bn=fee, key_term_bn=residual - fee, residual_bn=residual,
                    R_insured_bn=sum(pay.values()), G_insured_bn=sum(cost.values()), g_bn=g)

    def levels(v):   # the central value and its range
        return sorted({v[0], *v[1]})

    mix0 = {q: v[0] for q, v in hl["mix"].items()}
    pcr0 = {q: v[0] for q, v in hl["pcr"].items()}
    rows = []
    for a in ALLOCS:
        for fr, g in itertools.product(["union", "meps"], ["census", "nipa_charges"]):
            for mm, mc, rm, rc, rp in itertools.product(levels(hl["mix"]["medicare"]), levels(hl["mix"]["private_other"]),
                                                        levels(hl["pcr"]["medicare"]), levels(hl["pcr"]["medicaid"]),
                                                        levels(hl["pcr"]["private_other"])):
                for dev in itertools.product([-1, 0, 1], repeat=3):
                    s = {q: (sh[m] + d * se[m]) * (frame if fr == "union" else 1.0) for (q, m), d in zip(payers.items(), dev)}
                    mix = {"medicare": mm, "medicaid": mix0["medicaid"], "private_other": mc}
                    pcr = {"medicare": rm, "medicaid": rc, "private_other": rp}
                    gg = hl["g_bn"] if g == "census" else R_health / sum(mix[q] * pcr[q] for q in mix)
                    rows.append(dict(allocation=a, frame=fr, g=g, mix_medicare=mm, mix_private_other=mc, pcr_medicare=rm,
                                     pcr_medicaid=rc, pcr_private_other=rp, dev_medicare=dev[0], dev_medicaid=dev[1],
                                     dev_private_other=dev[2], s_K=s_K_health[a],
                                     **health(mix, pcr, s, s_K_health[a], gg)))
    ht = pd.DataFrame(rows)
    ht.to_csv(OUT / "health_terms.csv", index=False, lineterminator="\n", float_format="%.6f")

    def hcentral(a, fr="union", g="census"):
        r = ht[(ht.allocation == a) & (ht.frame == fr) & (ht.g == g) & (ht.mix_medicare == mix0["medicare"])
               & (ht.mix_private_other == mix0["private_other"]) & (ht.pcr_medicare == pcr0["medicare"])
               & (ht.pcr_medicaid == pcr0["medicaid"]) & (ht.pcr_private_other == pcr0["private_other"])
               & (ht.dev_medicare == 0) & (ht.dev_medicaid == 0) & (ht.dev_private_other == 0)]
        if len(r) != 1:
            raise SystemExit("[BLOCKED] the health table does not hold the central row once")
        return r.iloc[0]

    fee_health = {a: float(hcentral(a).fee_term_bn) for a in ALLOCS}
    key_health = {a: float(hcentral(a).key_term_bn) for a in ALLOCS}

    lines = [
        dict(line="S&L tuition and related educational charges", nipa="T3.10.5 l58", R_bn=R_tuition,
             account_line="education_services (row 6: 1 - W of the line at item P)", s_U=U, s_R=sR, s_K=P_eff,
             fee_term_bn=fee_tuition, fee_term_at_account_key_bn=(P_eff - sR) * R_tuition,
             key_term_bn=key_higher, status="measured: IPEDS FY2023 x ACS 2024"),
        dict(line="S&L health and hospital charges", nipa="T3.10.5 l59", R_bn=R_health,
             account_line="health_services at health_other (+ state-price line)",
             s_U=float(hcentral("personal").s_U), s_R=float(hcentral("personal").s_R), s_K=s_K_health["personal"],
             fee_term_bn=float(hcentral("personal").fee_term_bn),
             fee_term_at_account_key_bn=float((s_K_health["personal"] - hcentral("personal").s_R) * hcentral("personal").R_insured_bn),
             key_term_bn=float(hcentral("personal").key_term_bn),
             status="insured payers measured (MEPS 2024 x government hospitals' payer mix); uninsured care charged by use in the case"),
        dict(line="S&L other sales", nipa="T3.10.5 l60", R_bn=R_other, account_line="several (by function)",
             s_U=None, s_R=None, s_K=None, fee_term_bn=0.0, fee_term_at_account_key_bn=None, key_term_bn=None,
             status="not measured: paid per use; about $41bn is federal R&D purchases from S&L universities"),
        dict(line="Federal sales to other sectors", nipa="T3.10.5 l22", R_bn=R_fed, account_line="federal lines",
             s_U=None, s_R=None, s_K=None, fee_term_bn=0.0, fee_term_at_account_key_bn=None, key_term_bn=None,
             status="below $20bn; not sized"),
        dict(line="Government enterprises (transit, utilities, tolls, airports, liquor)", nipa="T3.8 (surplus)",
             R_bn=None, account_line="enterprise_surplus receipt (population key) + enterprise capital",
             s_U=None, s_R=None, s_K=s_ent["personal"], fee_term_bn=0.0, fee_term_at_account_key_bn=None,
             key_term_bn=key_transit["personal"],
             status="fees per use, netted in the surplus; transit's loss keyed by population (key term: transit, operating)"),
    ]
    pd.DataFrame(lines).to_csv(OUT / "fee_lines.csv", index=False, lineterminator="\n", float_format="%.6f")

    cog = census_charges()
    comp = []
    for n, nipa_class in [(25, "tuition; auxiliaries (dorms, dining) in other sales"), (26, "other sales"),
                          (27, "health and hospital charges"), (28, "toll facilities are enterprises; the rest other sales"),
                          (29, "enterprise: air and water terminals"), (30, "enterprise (other)"),
                          (31, "enterprise: air and water terminals"), (32, "other sales"), (33, "other sales"),
                          (34, "enterprise: housing and urban renewal"), (35, "enterprise: water and sewerage"),
                          (36, "other sales"), (37, "other sales")]:
        lab, v = cog[n]
        comp.append(dict(census_line=n, label=lab, fy2022_bn=v, nipa_treatment=nipa_class))
    lab, v = cog[24]
    comp.append(dict(census_line=24, label=lab + " (all; less lines 25-26 = other education)", fy2022_bn=v,
                     nipa_treatment="tuition + other sales"))
    comp.append(dict(census_line=None, label="IPEDS FY2023 federal operating grants and contracts, public institutions",
                     fy2022_bn=he_json["ipeds_public_f1a_totals_bn"]["F1B02"],
                     nipa_treatment="other sales: federal purchases of R&D from S&L (T3.10.5 note 5)"))
    pd.DataFrame(comp).to_csv(OUT / "other_sales.csv", index=False, lineterminator="\n", float_format="%.6f")
    other_persons = R_other - he_json["ipeds_public_f1a_totals_bn"]["F1B02"]

    by_both = lambda v: {a: v for a in ALLOCS}  # noqa: E731
    out = dict(
        frames=dict(union=union, lineage=lineage, resident=resident, acs_group=acs["mexican_origin"], phi=phi,
                    household_fraction=hf, meps_frame=frame, lineage_scale=lineage / union),
        nipa=dict(tuition_bn=R_tuition, health_bn=R_health, other_bn=R_other, federal_bn=R_fed, sl_sales_bn=R_sl,
                  education_line_bn=n_edu, sl_education_consumption_bn=sl_edu, sl_education_benefits_bn=sl_ben,
                  consumption_bn=cons, implied_investment_bn=invest, federal_education_bn=fed_edu, weights=weights,
                  kappa=kappa, transit_loss_bn=transit_loss),
        education_key=dict(W=W, by_allocation=key, P_eff=P_eff),
        higher_ed=dict(U=U, s_R=sR, s_U_acs=he_json["central"]["s_U"], s_R_acs=he_json["central"]["s_R"],
                       higher_dollars_bn=higher_dollars, fee_term_bn=fee_tuition,
                       fee_term_at_account_key_bn=(P_eff - sR) * R_tuition, key_term_bn=key_higher,
                       ranges_bn={k: [float(arms[k].min()), float(arms[k].max())] for k in
                                  ["fee_term_bn", "fee_term_at_account_key_bn", "key_term_bn", "operating_block_bn"]},
                       U_capital=U_capital, college_key_union=college_key_union),
        health=dict(s_K=s_K_health, central={a: {k: float(v) for k, v in hcentral(a).items() if k not in ("allocation", "frame", "g")}
                                             for a in ALLOCS},
                    fee_term_at_account_key_bn={a: float((s_K_health[a] - hcentral(a).s_R) * hcentral(a).R_insured_bn)
                                                for a in ALLOCS},
                    meps_frame_raw={a: float(hcentral(a, "meps").residual_bn) for a in ALLOCS},
                    nipa_charges_g={a: float(hcentral(a, "union", "nipa_charges").residual_bn) for a in ALLOCS},
                    ranges_bn={k: [float(ht[k].min()), float(ht[k].max())] for k in ["fee_term_bn", "residual_bn"]}),
        pell=dict(total_bn=PELL_BN, share_public_acs=pell_pub, share=pell_share(), s_cash_union=s_cash,
                  term_bn=key_pell, range_bn=[min(min(r["term_personal_bn"], r["term_shared_bn"]) for r in pell_arms),
                                              max(max(r["term_personal_bn"], r["term_shared_bn"]) for r in pell_arms)],
                  arms=pell_arms),
        transit=dict(ratio=r_transit, s_ent_union=s_ent, operating_term_bn=key_transit, mode_arms=transit_arms),
        other_sales=dict(paid_by_persons_and_business_bn=other_persons, per_001_gap_bn=BOUND_GAP * other_persons),
        engine_lines={
            "fee_tuition": dict(response_class="service", parent="education_services", by=by_both(fee_tuition),
                label="Public colleges: tuition the group pays short of its use (user-fee lane; candidate)"),
            "fee_health": dict(response_class="service", parent="health_services", by=fee_health,
                label="Public hospitals: fees the group's insured care pays short of its use (user-fee lane; candidate)"),
            "key_health": dict(response_class="service", parent="health_services", by=key_health,
                label="Public hospitals: the insured net keyed by use, not the health key (user-fee lane; candidate)"),
            "key_higher_ed": dict(response_class="service", parent="education_services", by=by_both(key_higher),
                label="Public colleges keyed by measured use, not item P (user-fee lane; candidate)"),
            "key_pell": dict(response_class="household_transfer", parent="other_federal_benefits", by=key_pell,
                label="Pell grants keyed by the group's Pell share, not cash income (user-fee lane; candidate)"),
            "key_transit": dict(response_class="service", parent_receipt="enterprise_surplus", by=key_transit,
                label="Transit loss keyed by the group's transit share, not population (user-fee lane; candidate)"),
        },
        post_engine={
            "key_k12_weight": dict(rule="A + B x school fraction, at the education line's response", central=CENTRAL_WEIGHTS,
                                   by_weights=k12_weight),
            "college_capital": dict(component="college", key_target=by_both(U_capital), key_union=college_key_union,
                                    rule="stock x rate x response x (key_target - key_union)"),
            "k12_capital": dict(component="k12", key_target=k12_capital_target, key_union=k12_key_union,
                                rule="stock x rate x response x (key_target - key_union)"),
            "transit_capital": dict(component="ent_transit_sl", key_shift={a: (r_transit - 1) * s_ent[a] for a in ALLOCS},
                                    rule="stock x rate x response x key_shift"),
        },
        union_reads={
            "spending:education_services/education_mix": {a: key[a]["union_education_bn"] for a in ALLOCS},
            "spending:school_reprice/k": {a: key[a]["school_edit_bn"] for a in ALLOCS},
            "spending:college_rekey/k": {a: key[a]["college_edit_bn"] for a in ALLOCS},
            "spending:other_federal_benefits/all_cash": {a: allcash[a][0] for a in ALLOCS},
            "spending:health_services/health_other": {a: hs[a][0] for a in ALLOCS},
            "spending:state_price_health_services/k": sp,
            "receipt:enterprise_surplus": {a: ent[a][0] for a in ALLOCS},
        },
    )
    (OUT / "fee_lines.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    show = dict(phi=phi, P_eff=P_eff, U=U, s_R=sR, fee_tuition=fee_tuition, at_account_key=(P_eff - sR) * R_tuition,
                key_higher=key_higher, k12_weight=k12_weight[CENTRAL_WEIGHTS], weights=weights, U_capital=U_capital,
                k12_capital_target=k12_capital_target, k12_key_union=k12_key_union,
                college_key_union=college_key_union, health_fee=fee_health, health_key=key_health, health_s_K=s_K_health,
                health_residual={a: float(hcentral(a).residual_bn) for a in ALLOCS}, pell=key_pell, s_cash=s_cash,
                pell_share=pell_share(), transit=key_transit, r_transit=r_transit, s_ent=s_ent)
    print(json.dumps(show, indent=1))


if __name__ == "__main__":
    main()
