"""Step 2: the September 27 case distributed over the union's households, conventions A and B.

Input: _cache/lines.json from export_lines.cjs (each generation's corrected lines at the case's two band ends:
specification 48, shared allocation, the low end; specification 11, personal allocation, the high end).
Rule: within each generation, each line's corrected amount is spread over that generation's persons in
proportion to the line's own key vector at the end's allocation (the account's definitions: the CPS, MEPS and
school keys that generation_account_2026_09_24/keys.py rebuilds and gates, imported read-only). This keeps each
generation's total, and so the union's, exactly; within a generation it is first order: a correction that in
truth falls on a subset (the SSN rule on credits, status-based compliance) is spread over the whole key.
  - public order by use: the generation's amount splits into its per-head part and its custody, arrest and ICE
    part in the proportions of the use key's components (generation_key_shares.json meta.use_parts, convention
    a); per head over all members, the rest over members aged 18-64 (the key's own base; the incarcerated are
    outside the household frame, so within a generation "use" cannot follow individuals);
  - Medicaid with uninsured use: the Medicaid-key part and the uninsured part in the proportions of the
    generation's uncorrected cells (model_G*.json), the first by the MEPS Medicaid key, the second by uninsured
    person-years (NOCOV_CYR 3 = 1, 2 = 0.5, keys.py's exposure);
  - the capital return: each component by its own key rule, i.e. by the persons' amounts of its numerator lines
    (the enterprise components by the enterprise_surplus receipt, per head);
  - the production term (P + F): by positive earnings (the specification's proxy) within the skill cells, the
    generation lane's Aumann-Shapley attribution (production.py) carried down to the worker; the cell parts are
    solved from the three generations' terms and gated;
  - the lane constants (care work, shelter, audit rows 8-10; no person-level rule): not assigned, reported as
    the residual.
Convention A: everything assigned. Convention B: taxes (every receipt but the enterprise surplus) against
transfers keyed to the household's own benefit receipt (CPS benefit amounts and SPM unit benefits, including the
income-security services line keyed to cash assistance and housing subsidies), health (MEPS use cells, Medicaid
with uninsured use, Medicare), K-12 schools
(the school part of education plus the school reprice) and justice by use (the non-per-head part); general
government, public order per head, roads and parks, other per-head services and transfers keyed per head or by
age, college and other education, the capital return, the enterprise surplus and the production term are left out.
Standard errors: the 160 ASEC replicate weights (successive difference, 4/160), re-running the within-generation
spread and every statistic per replicate with the engine's line totals held fixed.
Weights (--weights): `published`, the default, spreads over the ASEC person weights (union 40,896,574). `row4`
spreads over audit row 4's weights, the count the case prices (union 39,712,493): the Mexico-born naturalized
and noncitizen persons outside CA+TX scaled to their ACS 2024 cells by cps_imputation_keys_2026_09_23/
combine_onbooks_lane.py weight_arms, arm "row4", called as population_basis_2026_09_29/frame_counts.py calls it
but on all 161 columns (every step acts column by column, so the replicates come from the same call). Beyond the
weights, two generation-level inputs follow the count: the per-head part of public order moves with each
generation's share of the civilian frame, as the engine's row-4 correction moves it; the production term keeps
the generation lane's attribution on the published weights, as the case keeps the term at its published value.
Gates (exit 1, nothing written): the union count reproduces main_case_decomposition_2026_09_29/derived/
headcount.csv (1 person); key totals reproduce generation_keys.csv by generation (1e-9 relative; on row 4, G2
and G3+ there, whose weights row 4 leaves, and the union the decomposition lane's row-4 age_bins.csv);
production cell parts close (1e-6 bn); every generation's assigned amounts plus its residual equal its cost
(1e-6 bn); households plus the residual reproduce the case at both ends (1e-6 bn); on row 4, the per-head
part's change reproduces the engine's (stack_by_generation.json, 1e-6 bn) and every per-head line charges each
generation the same per member (1e-9 relative); one reference person per household; the status imputation
reproduces its published Mexico-born 25-64 counts (on the published weights: the flag does not use weights).
Sensitivity A_schools_per_head: convention A with the school dollars spread per head over the union instead of
charged to the pupils' households.
Writes derived/net_positive_shares.csv, concentration.csv, household_balance_quantiles.csv, control.csv,
category_means.csv, line_scaling.csv and _cache/households.parquet; the row-4 run writes the same files to
derived/row4/ and _cache/row4/. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --weights row4
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import argparse
import csv
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
GENLANE = FISCAL / "generation_account_2026_09_24"
sys.path.insert(0, str(GENLANE))
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import keys as K  # noqa: E402
from impute_status import impute  # noqa: E402
import combine_onbooks_lane as L  # noqa: E402  last: it puts two more lanes at the front of sys.path

C = F.C
OUT = HERE / "derived"
CACHE = HERE / "_cache"
DECOMP = FISCAL / "main_case_decomposition_2026_09_29/derived"
GENS = F.GENS
ENDS = ["low", "high"]
PUBLISHED_MEX_25_64 = {"borjas_paper_rules": 3.9170610819750302, "no_medicaid_rule": 4.778136460024849}
PER_HEAD_KEYS = {"population", "resident_population"}
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def sdr(values):
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


# Category of every assigned piece; B keeps the first five.
B_CATS = ["taxes", "transfers", "health", "schools", "justice_use"]
A_ONLY = ["enterprise", "transfers_per_head", "education_other", "justice_per_head", "general_government",
          "roads_parks", "other_shared", "capital", "production"]
# Spending lines are classed by their key: keyed to the household's own benefit receipt (CPS amounts, SPM unit
# benefits) = transfers; MEPS use cells = health; keyed per head or by age = per-head transfers or other shared.
HEALTH_KEYS = {"medicare", "medicaid", "health_other", "tricare", "va_medical"}
OWN_RECEIPT_KEYS = {"cash_assistance", "social_security", "ssi", "unemployment", "veterans", "workers_comp", "snap",
                    "energy", "wic", "housing_support", "refundable_credits", "all_cash"}
ROADS_PARKS = {"economic_affairs_services", "recreation_culture"}


def spending_category(row):
    i, k = row["id"], row["key"]
    if i == "general_public_services":
        return "general_government"
    if i in ROADS_PARKS:
        return "roads_parks"
    if k in HEALTH_KEYS:
        return "health"
    if k in OWN_RECEIPT_KEYS:
        return "transfers"
    if row["response_class"] == "household_transfer":
        return "transfers_per_head"
    return "other_shared"


def main(arm):
    print(f"[frame] weights: {arm}", flush=True)
    lines = json.loads((CACHE / "lines.json").read_text())
    d = F.load()
    civ, union, gens = F.masks(d)
    W_pub = d[F.REPS].to_numpy(float)
    W = W_pub
    if arm == "row4":
        print("[row 4 weights]", flush=True)
        arms, info = L.weight_arms(d, W_pub, L.acs_cells())
        W = arms["row4"]
        del arms
        print(f"  row-4 factors: naturalized {info['factor_natz']:.6f}, noncitizen {info['factor_noncit']:.6f}", flush=True)
    w0 = W[:, 0]
    w_pub = W_pub[:, 0]
    out_dir, cache_dir = (OUT, CACHE) if arm == "published" else (OUT / arm, CACHE / arm)
    index = C.spm_index(d)
    age = d.A_AGE.to_numpy()
    lab = F.label(gens, len(d))
    heads = pd.read_csv(DECOMP / "headcount.csv").query("cut == 'all' and group == 'union'")
    n_union, want = float(w0[union].sum()), float(heads[arm].iloc[0])
    gate(f"union count reproduces headcount.csv, column {arm} (1 person)", abs(n_union - want) <= 1.0,
         f"{n_union:,.3f} vs {want:,.3f}")

    print("[key vectors]", flush=True)
    rk = C.receipt_keys(d, index)
    sk = C.spending_vectors(d, index)
    _, params = K.owner_property(d)
    medical, _, _, _ = K.meps_keys(d)
    edu = K.school_keys(d, civ, params)
    exposure_py = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    vec = {}
    for a in ("personal", "shared"):
        v = {("receipt", k): x for k, x in rk[a].items()}
        v[("receipt", "resident_population")] = np.ones(len(d))
        v.update({("spending", k): x for k, x in sk[a].items()})
        v.update({("spending", k): x for k, x in medical.items()})
        v[("spending", "school_part")] = edu[a]["school"]
        v[("spending", "P_part")] = edu[a]["P"]
        v[("spending", "postsecondary")] = edu[a]["P"]
        v[("spending", "school_operating")] = edu[a]["school"]
        vec[a] = v
    pub = pd.read_csv(GENLANE / "derived/generation_keys.csv").query("convention == 'a'")
    # Row 4 moves no weight in G2 or G3+, so their rows keep generation_keys.csv; the union's row-4 totals are the
    # decomposition lane's age bins (the same key vectors under the same weight_arms call), which pins G1 as well.
    by_gen, union_ref = GENS, None
    if arm != "published":
        by_gen = GENS[1:]
        union_ref = pd.read_csv(DECOMP / "age_bins.csv").query("weights == @arm").groupby(["allocation", "key"])["union"].sum()
    worst, checked = 0.0, 0

    def pin(r, x):
        nonlocal worst, checked
        for g in by_gen:
            want = getattr(r, g)
            worst = max(worst, abs(float(x[gens[g]] @ w0[gens[g]]) - want) / max(abs(want), 1.0))
        if union_ref is not None:
            want = float(union_ref[("both", "extra|pop") if r.key == "resident_population"
                                   else (r.allocation, f"{r.side}|{r.key}")])
            worst = max(worst, abs(float(x[union] @ w0[union]) - want) / max(abs(want), 1.0))
        checked += 1

    for r in pub.itertuples():
        key = (r.side, r.key)
        if r.allocation not in vec or key not in vec[r.allocation]:
            continue
        pin(r, vec[r.allocation][key])
    mix = {a: vec[a][("spending", "school_part")] + vec[a][("spending", "P_part")] for a in vec}
    for r in pub.query("key == 'education_mix'").itertuples():
        pin(r, mix[r.allocation])
    ref = ("generation_keys.csv by generation" if union_ref is None
           else "G2 and G3+ generation_keys.csv, the union age_bins.csv")
    gate(f"{checked} key rows reproduce their {arm} totals: {ref} (1e-9 relative)", worst < 1e-9, f"worst {worst:.1e}")
    gaps = {"key totals (relative)": worst}

    shares = json.loads((GENLANE / "derived/generation_key_shares.json").read_text())
    use_parts = shares["meta"]["use_parts"]["a"]
    models = {g: json.loads((GENLANE / f"derived/model_{g}.json").read_text()) for g in GENS}

    # The use key's per-head part is a per-head rate times each generation's population (keys.py); the engine's row-4
    # correction moves it with the generation's share of the civilian frame. The factor is 1 on the published weights.
    pop = np.array([w0[gens[g]].sum() for g in GENS])
    pop_pub = np.array([w_pub[gens[g]].sum() for g in GENS])
    per_head_factor = pop / pop_pub * (w_pub[civ].sum() / w0[civ].sum())
    if arm != "published":
        comp = json.loads((GENLANE / "derived/stack_by_generation.json").read_text())["components"]["C_row4_weights"]["a"]
        engine = np.array([comp[g]["spending"]["public_order_safety"]["population"]["personal"] for g in GENS])
        moved = np.array(use_parts["per_head"]) * (per_head_factor - 1)
        gap = float(np.abs(moved - engine).max())
        gate("row 4 moves public order's per-head part as the engine does (C_row4_weights, 1e-6 bn)", gap < 1e-6,
             f"{', '.join(f'{g} {x:+.6f}' for g, x in zip(GENS, moved))} bn; max |diff| {gap:.1e}")
    # Per-head lines: the case prices them for the row-4 count, so on its weights every generation pays the same per
    # member; on the published weights the first generation pays less.
    spread = 0.0
    for end in ENDS:
        rows_g = {g: {r["id"]: r for r in lines["generations"][g][end]["rows"]} for g in GENS}
        for i, r in rows_g["G1"].items():
            per_member = np.array([rows_g[g][i]["cost_bn"] for g in GENS]) * 1e9 / pop
            if r["key"] in PER_HEAD_KEYS and np.any(per_member != 0):
                spread = max(spread, float(np.ptp(per_member) / np.abs(per_member).max()))
    if arm == "published":
        print(f"  · per-head lines per member across generations: widest relative spread {spread:.2%}", flush=True)
    else:
        gate("every per-head line charges each generation the same per member (1e-9 relative)", spread < 1e-9,
             f"widest spread {spread:.1e}")
    gaps["per-head lines' spread (relative)"] = spread

    # Production: cell parts AS_s solved from the three generations' terms and their cell labor shares. The case keeps
    # the term at its published value and the generation lane attributes it on the published weights, so the parts are
    # solved there on both arms; each part is then spread over its cell's workers at the arm's weights.
    print("[production cells]", flush=True)
    prod_parts = {}
    for end in ENDS:
        dims = lines["union"][end]["production"]["dims"]
        cut = 39 if dims["split"] == "hs_or_less" else 42
        earn = np.maximum(d[dims["proxy"]].to_numpy(float), 0)
        cells = [d.A_HGA.between(31, cut).to_numpy(), d.A_HGA.between(cut + 1, 46).to_numpy()]
        labor = np.array([[float((earn * w_pub)[gens[g] & c].sum()) for c in cells] for g in GENS])
        A = labor / labor.sum(axis=0)
        y = np.array([lines["generations"][g][end]["production"]["cost_bn"] for g in GENS])
        AS, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = float(np.abs(A @ AS - y).max())
        gate(f"production {end}: cell parts reproduce the three generations' terms", resid < 1e-6,
             f"AS = {AS.round(4).tolist()} bn, max residual {resid:.1e}")
        prod_parts[end] = dict(earn=earn, cells=cells, part=A * AS)  # generation x cell, $bn

    # Pieces: (generation, category, amount_bn, vector restricted to the generation).
    print("[pieces]", flush=True)
    pieces, residual, scaling = {e: [] for e in ENDS}, {e: {} for e in ENDS}, []
    for end in ENDS:
        for g in GENS:
            G = lines["generations"][g][end]
            a = G["allocation"]
            m = gens[g]
            amount = {}

            def add(cat, bn, x, pid):
                x = np.where(m, x, 0.0)
                pieces[end].append(dict(g=g, cat=cat, bn=bn, x=x, id=pid))

            def line_parts(row):
                """[(category, vector)] whose sum is the line's key vector."""
                k, i = row["key"], row["id"]
                if row["side"] == "receipt":
                    return [("enterprise" if i == "enterprise_surplus" else "taxes", vec[a][("receipt", k)])]
                if i == "education_services":
                    return [("schools", vec[a][("spending", "school_part")]),
                            ("education_other", vec[a][("spending", "P_part")])]
                if i == "school_reprice":
                    return [("schools", vec[a][("spending", "school_part")])]
                if i == "college_rekey":
                    return [("education_other", vec[a][("spending", "P_part")])]
                return [(spending_category(row), vec[a][("spending", k)])]

            def line_split(row):
                """[(category, share of the line, vector)] for one line of this generation."""
                i = row["id"]
                if i == "public_order_safety":
                    j = GENS.index(g)
                    ph = use_parts["per_head"][j] * per_head_factor[j]
                    rest = use_parts["custody"][j] + use_parts["arrest_like_custody"][j] + use_parts["ice_interior"][j]
                    f = ph / (ph + rest)
                    return [("justice_per_head", f, np.ones(len(d))),
                            ("justice_use", 1 - f, ((age >= 18) & (age <= 64)).astype(float))]
                if row["key"].startswith("uninsured_use"):
                    line = next(x for x in models[g]["spending"]["lines"] if x["id"] == i)
                    med = line["keys"]["medicaid"][a]["target_bn"] / line["keys"][row["key"]][a]["target_bn"]
                    return [("health", med, vec[a][("spending", "medicaid")]), ("health", 1 - med, exposure_py)]
                parts = line_parts(row)
                # One coefficient per line: split the line by the parts' shares of its key total.
                total = sum(float(np.where(m, x, 0) @ w0) for _, x in parts)
                return [(cat, float(np.where(m, x, 0) @ w0) / total if total else 0.0, x) for cat, x in parts]

            for row in G["rows"]:
                i, bn = row["id"], row["cost_bn"]
                amount[i] = row["amount_bn"]
                if bn == 0:
                    continue
                if i == "lane_constants":
                    residual[end][g] = residual[end].get(g, 0.0) + bn
                    continue
                for cat, share, x in line_split(row):
                    add(cat, bn * share, x, i)
                # Scaling diagnostic: corrected amount over the uncorrected generation cell.
                ml = models[g]["receipts" if row["side"] == "receipt" else "spending"]["lines"]
                line0 = next((x for x in ml if x["id"] == i), None)
                if line0 is not None:
                    cell0 = (line0["cells"][row["scenario"]][a] if row["side"] == "receipt"
                             else line0["keys"][row["key"]][a])["target_bn"]
                    scaling.append(dict(end=end, generation=g, side=row["side"], line=i, key=row["key"], allocation=a,
                                        uncorrected_bn=cell0, corrected_bn=row["amount_bn"],
                                        ratio=(row["amount_bn"] / cell0 if cell0 else float("nan"))))
            for c in G["capital"]:
                rule = c["rule"]
                if rule["kind"] == "receipt_amount_over_national":
                    add("capital", c["cost_bn"], np.ones(len(d)), c["id"])
                    continue
                nums = rule["numerator_lines"]
                den = sum(amount[n] for n in nums)
                for n in nums:
                    row = next(r for r in G["rows"] if r["id"] == n)
                    for _, share, x in line_split(row):
                        add("capital", c["cost_bn"] * amount[n] / den * share, x, c["id"])
            pp = prod_parts[end]
            for s, cell in enumerate(pp["cells"]):
                add("production", pp["part"][GENS.index(g), s], pp["earn"] * cell, "production")
            # Gate: the generation's pieces plus its residual equal its cost.
            got = sum(p["bn"] for p in pieces[end] if p["g"] == g) + residual[end].get(g, 0.0)
            gaps["generation pieces vs cost (bn)"] = max(gaps.get("generation pieces vs cost (bn)", 0.0),
                                                         abs(got - G["cost_bn"]))
            gate(f"{g} {end}: pieces plus residual equal the generation's cost", abs(got - G["cost_bn"]) < 1e-6,
                 f"{got:.6f} vs {G['cost_bn']:.6f}")

    # Person amounts per replicate, by category: coefficient = bn * 1e9 / (x . w_r) within the generation.
    print("[person amounts]", flush=True)
    rows_u = np.flatnonzero(union)
    Wu = W[rows_u]
    cats = B_CATS + A_ONLY
    amt = {e: {c: np.zeros((len(rows_u), W.shape[1])) for c in cats} for e in ENDS}
    unassigned = {e: np.zeros(W.shape[1]) for e in ENDS}
    for end in ENDS:
        for p in pieces[end]:
            x = p["x"][rows_u]
            k = x @ Wu  # 161
            if not np.any(x) or np.any(k == 0):
                unassigned[end] += p["bn"]
                if p["bn"] != 0:
                    print(f"  · unassignable piece {p['g']} {p['id']} {p['bn']:.6f} bn")
                continue
            amt[end][p["cat"]] += np.outer(x, p["bn"] * 1e9 / k)
    for end in ENDS:
        tot = sum((amt[end][c] * Wu).sum(axis=0) for c in cats) / 1e9
        res = sum(residual[end].values()) + unassigned[end][0]
        case = lines["union"][end]["cost_bn"]
        gap_case, gap_reps = abs(tot[0] + res - case), float(np.abs(tot - tot[0]).max())
        gaps["households + residual vs the case (bn)"] = max(gaps.get("households + residual vs the case (bn)", 0.0), gap_case)
        gaps["replicates vs full sample (bn)"] = max(gaps.get("replicates vs full sample (bn)", 0.0), gap_reps)
        gate(f"{end}: persons' assigned amounts plus the residual reproduce the case (full sample)",
             gap_case < 1e-6, f"{tot[0]:.6f} + {res:.6f} = {tot[0] + res:.6f} vs {case:.6f}, gap {gap_case:.1e}")
        gate(f"{end}: every replicate's assigned total equals the full sample's (line totals held)",
             gap_reps < 1e-6, f"max |diff| {gap_reps:.1e} bn")
        # Sensitivity: the same school dollars spread per head over the union instead of charged to the pupils.
        school_total = (amt[end]["schools"] * Wu).sum(axis=0)
        amt[end]["schools_per_head"] = np.tile(school_total / Wu.sum(axis=0), (len(rows_u), 1))

    print("[households]", flush=True)
    du = d.iloc[rows_u].reset_index(drop=True)
    hh_code, hh_ids = pd.factorize(du.PH_SEQ, sort=True)
    H = len(hh_ids)
    members = np.bincount(hh_code).astype(float)
    Wh = np.stack([np.bincount(hh_code, weights=Wu[:, r]) for r in range(Wu.shape[1])], axis=1) / members[:, None]
    ref = d.A_EXPRRP.isin([1, 2]).to_numpy()
    nref = pd.Series(ref.astype(int)).groupby(d.PH_SEQ.to_numpy()).sum()
    gate("one reference person per household (A_EXPRRP 1, 2)", bool((nref == 1).all()), f"{int((nref != 1).sum())} exceptions")
    # Head: the reference person when a union member, else the oldest union adult, else the oldest union member.
    ua = du.assign(row=rows_u, code=hh_code, ref=ref[rows_u], adult=du.A_AGE.ge(18))
    ua = ua.sort_values(["code", "ref", "adult", "A_AGE", "PPPOS"], ascending=[True, False, False, False, True])
    head_rows = ua.drop_duplicates("code").sort_values("code").row.to_numpy()
    refrow = pd.Series(np.flatnonzero(ref), index=d.PH_SEQ.to_numpy()[ref])
    ref_rows = refrow.reindex(hh_ids).to_numpy()
    ref_in_union = union[ref_rows]
    # A household whose union members are all minors takes its head's attributes from the reference person, who is
    # then outside the union (generation and status "outside_union").
    minor_only = age[head_rows] < 18
    head_rows = np.where(minor_only, ref_rows, head_rows)
    head_is_ref = ref[head_rows]
    head_lab = lab[head_rows]

    s_status = {}
    dd = d.assign(state=d.GESTFIPS)
    hh = d[["H_SEQ", "HPUBLIC", "HLORENT"]].drop_duplicates("H_SEQ")
    mex = d.PENATVTY.eq(303).to_numpy() & d.PRCITSHP.isin([4, 5]).to_numpy()
    for name, use_med in (("borjas_paper_rules", True), ("no_medicaid_rule", False)):
        s = impute(dd, hh, use_medicaid_rule=use_med)
        un = np.asarray(s["unauthorized"], bool)
        sel = mex & un & (age >= 25) & (age <= 64)
        got = w_pub[sel].sum() / 1e6
        gate(f"status ({name}) reproduces the published Mexico-born 25-64 count", abs(got - PUBLISHED_MEX_25_64[name]) < 1e-9,
             f"{got:.6f}M" + ("" if arm == "published" else f"; {w0[sel].sum() / 1e6:.6f}M on the {arm} weights"))
        s_status[name] = un

    hga = d.A_HGA.to_numpy()[head_rows]
    edu_lab = np.select([hga <= 38, hga == 39, hga <= 42], ["below_high_school", "high_school", "some_college"],
                        "bachelor_plus")
    hage = age[head_rows]
    age_lab = np.select([hage < 30, hage < 45, hage < 65], ["under_30", "30_44", "45_64"], "65_plus")
    st = d.GESTFIPS.to_numpy()[head_rows]
    state_lab = np.select([st == 6, st == 48], ["CA", "TX"], "other")
    gen_lab = np.where(head_lab >= 0, np.array(GENS)[np.maximum(head_lab, 0)], "outside_union")
    kids = np.bincount(hh_code, weights=(du.A_AGE.lt(18)).to_numpy(float))
    kid_lab = np.select([kids == 0, kids <= 2], ["none", "1_2"], "3_plus")
    status_lab = {}
    for name, un in s_status.items():
        lab_s = np.where(head_lab == 0, np.where(un[head_rows], "unauthorized", "legal_immigrant"),
                         np.where(head_lab > 0, "us_born", "outside_union"))
        status_lab[name] = lab_s
    head_breaks = {"all": np.full(H, "all"), "head_education": edu_lab, "head_generation": gen_lab, "head_age": age_lab,
                   "state_group": state_lab, "children_in_household": kid_lab,
                   "head_status_borjas_rules": status_lab["borjas_paper_rules"],
                   "head_status_no_medicaid_rule": status_lab["no_medicaid_rule"]}
    own_gen = np.array(GENS)[lab[rows_u]]

    conv_cats = {"A": cats, "B": B_CATS, "A_schools_per_head": [c for c in cats if c != "schools"] + ["schools_per_head"]}
    mean_rows = []
    for end in ENDS:
        for name, labels in list(head_breaks.items()) + [("own_generation", None)]:
            lab_p = own_gen if labels is None else labels[hh_code]
            for cell in sorted(set(lab_p)):
                sel = lab_p == cell
                wsel = Wu[sel]
                for c in cats + ["schools_per_head"]:
                    mean = (amt[end][c][sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                    mean_rows.append(dict(end=end, breakdown=name, cell=cell, category=c, in_B=c in B_CATS,
                                          net_cost_per_member_usd=mean[0], se=sdr(mean)))
    npos_rows, conc_rows, q_rows, ctrl_rows = [], [], [], []
    hh_out = pd.DataFrame({"PH_SEQ": hh_ids, "union_members": members, "weight": Wh[:, 0], **{k: v for k, v in head_breaks.items() if k != "all"},
                           "head_is_reference_person": head_is_ref, "reference_person_in_union": ref_in_union})
    for conv, cs in conv_cats.items():
        for end in ENDS:
            person = sum(amt[end][c] for c in cs)  # n_u x 161, $ per person
            hcost = np.stack([np.bincount(hh_code, weights=person[:, r], minlength=H) for r in range(person.shape[1])], axis=1)
            hweighted = np.stack([np.bincount(hh_code, weights=person[:, r] * Wu[:, r], minlength=H) for r in range(person.shape[1])], axis=1)
            per_member = hcost / members[:, None]
            hh_out[f"{conv}_{end}_household_cost_usd"] = hcost[:, 0]
            hh_out[f"{conv}_{end}_per_member_usd"] = per_member[:, 0]
            for c in cs:
                hh_out[f"{conv}_{end}_{c}_usd"] = np.bincount(hh_code, weights=amt[end][c][:, 0], minlength=H)
            npos_p = hcost[hh_code] < 0  # members in net-contributor households, per replicate
            total = hweighted.sum(axis=0) / 1e9
            # Net-positive shares by breakdown (members weighted by their person weights).
            breaks = dict(head_breaks)
            for name, labels in list(breaks.items()) + [("own_generation", None)]:
                lab_p = own_gen if labels is None else labels[hh_code]
                for cell in sorted(set(lab_p)):
                    sel = lab_p == cell
                    wsel = Wu[sel]
                    share = (npos_p[sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                    mean_pm = (person[sel] * wsel).sum(axis=0) / wsel.sum(axis=0)
                    hsel = np.zeros(H, bool)
                    hsel[np.unique(hh_code[sel])] = True
                    hshare = ((hcost[hsel] < 0) * Wh[hsel]).sum(axis=0) / Wh[hsel].sum(axis=0)
                    cell_bn = (person[sel] * wsel).sum(axis=0) / 1e9
                    npos_rows.append(dict(convention=conv, end=end, breakdown=name, cell=cell, records=int(sel.sum()),
                                          households=int(hsel.sum()), members_m=wsel[:, 0].sum() / 1e6,
                                          share_members_net_positive=share[0], se=sdr(share),
                                          share_households_net_positive=hshare[0], se_households=sdr(hshare),
                                          net_cost_per_member_usd=mean_pm[0], se_per_member=sdr(mean_pm),
                                          cell_net_cost_bn=cell_bn[0], se_cell_bn=sdr(cell_bn),
                                          small_cell=bool(sel.sum() < 200)))
            # Concentration: households ranked by household net cost, counted by household weight.
            stats = {k: np.zeros(W.shape[1]) for k in ("top10_share_of_total", "top20_share_of_total",
                                                        "top10_members_share", "top20_members_share",
                                                        "net_cost_households_bn", "net_contributor_households_bn",
                                                        "share_households_net_positive")}
            for r in range(W.shape[1]):
                order = np.argsort(-hcost[:, r], kind="stable")
                cw = np.cumsum(Wh[order, r]) / Wh[:, r].sum()
                contrib = hweighted[order, r]
                mem = (members * Wh[:, r])[order]
                for p, key in ((0.1, "10"), (0.2, "20")):
                    full = cw <= p
                    j = int(full.sum())
                    prev = cw[j - 1] if j else 0.0
                    frac = (p - prev) / (cw[j] - prev) if j < H else 0.0
                    stats[f"top{key}_share_of_total"][r] = (contrib[full].sum() + frac * contrib[j]) / contrib.sum()
                    stats[f"top{key}_members_share"][r] = (mem[full].sum() + frac * mem[j]) / mem.sum()
                stats["net_cost_households_bn"][r] = hweighted[hcost[:, r] > 0, r].sum() / 1e9
                stats["net_contributor_households_bn"][r] = hweighted[hcost[:, r] < 0, r].sum() / 1e9
                stats["share_households_net_positive"][r] = Wh[hcost[:, r] < 0, r].sum() / Wh[:, r].sum()
            stats["total_bn"] = total
            for k, v in stats.items():
                conc_rows.append(dict(convention=conv, end=end, statistic=k, value=v[0], se=sdr(v)))
            # Quantiles: per member (members weighted by person weights) and per household (household weights).
            for unit, vals, wts in (("per_member", per_member[hh_code], Wu), ("household", hcost, Wh)):
                for q in (0.1, 0.25, 0.5, 0.75, 0.9):
                    qs = np.zeros(W.shape[1])
                    for r in range(W.shape[1]):
                        o = np.argsort(vals[:, r], kind="stable")
                        cwq = np.cumsum(wts[o, r]) / wts[:, r].sum()
                        qs[r] = vals[o, r][min(int(np.searchsorted(cwq, q)), len(o) - 1)]
                    q_rows.append(dict(convention=conv, end=end, unit=unit, quantile=q, net_cost_usd=qs[0], se=sdr(qs)))
            if conv == "A":
                case = lines["union"][end]["cost_bn"]
                for c in cs:
                    ctrl_rows.append(dict(end=end, item=c, bn=float((amt[end][c][:, 0] * Wu[:, 0]).sum() / 1e9),
                                          assigned=True))
                for g in GENS:
                    ctrl_rows.append(dict(end=end, item=f"lane_constants_{g}", bn=residual[end].get(g, 0.0), assigned=False))
                ctrl_rows.append(dict(end=end, item="unassignable_pieces", bn=float(unassigned[end][0]), assigned=False))
                ctrl_rows.append(dict(end=end, item="households_sum", bn=float(total[0]), assigned=True))
                ctrl_rows.append(dict(end=end, item="case", bn=case, assigned=None))
                ctrl_rows.append(dict(end=end, item="households_sum_plus_residual_minus_case",
                                      bn=float(total[0]) + sum(residual[end].values()) + float(unassigned[end][0]) - case,
                                      assigned=None))

    print(f"  households: {H:,} with {len(rows_u):,} union person records; reference person outside the union: "
          f"{int((~ref_in_union).sum())} households; union members all minors (head = reference person): {int(minor_only.sum())}")
    gate("every head is an adult", bool((age[head_rows] >= 15).all()), f"youngest head {int(age[head_rows].min())}")
    print(f"  worst gaps ({arm}): " + "; ".join(f"{k} {v:.1e}" for k, v in gaps.items()), flush=True)
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed, nothing written: {FAILS}")
        sys.exit(1)

    out_dir.mkdir(parents=True, exist_ok=True)

    def write(name, rows):
        df = pd.DataFrame(rows)
        for c in df.columns:
            if df[c].dtype == float:
                df[c] = df[c].round(6)
        df.to_csv(out_dir / name, index=False, lineterminator="\n", quoting=csv.QUOTE_MINIMAL)

    write("net_positive_shares.csv", npos_rows)
    write("concentration.csv", conc_rows)
    write("household_balance_quantiles.csv", q_rows)
    write("control.csv", ctrl_rows)
    write("category_means.csv", mean_rows)
    write("line_scaling.csv", scaling)
    cache_dir.mkdir(parents=True, exist_ok=True)
    hh_out.to_parquet(cache_dir / "households.parquet", index=False)
    print(f"  ✓ all household gates passed; wrote {out_dir.relative_to(HERE)}/ and {cache_dir.relative_to(HERE)}/households.parquet")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="The September 27 case spread over the union's households.")
    parser.add_argument("--weights", choices=["published", "row4"], default="published",
                        help="published: ASEC person weights (derived/); row4: audit row 4's weights (derived/row4/)")
    main(parser.parse_args().weights)
