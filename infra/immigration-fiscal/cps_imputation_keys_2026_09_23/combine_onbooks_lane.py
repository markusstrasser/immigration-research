"""Steps 5d and 5e: the audit's status rules at the on-books lane's shares, alone and with this lane's
methods (5d), and their interaction with audit rows 3 and 4 and a state-aware status flag (5e).

Step 5d. `onbooks_share_2026_09_23` puts the 2024 on-books share of the Latin-American-born imputed
unauthorized's CPS dollars at 0.415 / 0.526 / 0.635 for the Mexico-born (PENATVTY 303) and
0.401 / 0.550 / 0.683 for other Latin-American-born, low / central / high (its
`derived/onbooks_split.csv`, rows evidence_*). The lane frame carries PENATVTY, so each of the
audit's unauthorized gets the share of their origin; the on-books lane's uniform equivalents
(0.416 / 0.524 / 0.631) run as a check. For each case combine_status.status_vectors applies the
audit's rules to the published file (audit row 2 on the account's keys) and to the same frame as
each of this lane's eight methods. Key changes on the refundable line apply to its non-PTC part
only, $110.46bn of $228.809bn (Treasury MTS, `dataset_integrity_2026_09_23/derived/
spending_mts_credits.json`); the premium tax credits keep the published key.

Step 5e found that the first translation looked account keys up by name in the lane's single key
namespace: the Medicare spending line followed MCARE coverage (the premium receipt's key) instead of
MEPS payer means, and the shared motor-vehicle receipt the person count instead of unit-split adults.
translate.KEYS now resolves each account key explicitly. The "medicare_key_fix" arm records the fix:
every step-5d stack against the same stack under translate.AS_PUBLISHED, the first lookup. Every
other 5e arm is measured against the fixed stacks.
Audit row 3 (`dataset_integrity_2026_09_23/cps.md` §2). The receipts lane's `federal_gap_high_agi`
arm gives the target its CPS-modelled liability plus the BEA gap (BEA federal income tax minus the
allocation's national CPS liability) times its share of FEDTAX_BC x (AGI >= $500,000)
(`full_account_receipts_2026_09_20/builder.py`, derive_keys and conditional_rows). The published
split is held: the CPS part moves with a stack's liability share, the gap part with its high-AGI share.
Audit row 4 (`mexborn_count_2026_09_23`). All 161 weights of Mexico-born naturalized and noncitizen
persons outside CA+TX are scaled, per replicate, to the ACS 2024 level of their cell (IPUMS USA
extract 3, households plus noninstitutional GQ; state from STRATA, checked against the PUMS).
Sensitivities: the removed weight goes to other Hispanic origins in the same state x sex x age cell;
and native-born Mexican-origin persons outside CA+TX are also scaled, to their ACS 2024 level moved
to 15 March 2025 at the 2023-24 pace (PUMS 2023, 2024). Every CPS-weighted input of the adopted case
is recomputed under the new weights: the lane's keys; the account's MEPS payer keys (medicaid,
health_other, tricare, va_medical, medicare; `full_account_spending_2026_09_20/builder.py`); the
school lane's keys, by proxy (the union's share of persons 5-24 or 18-24); the per-head part of the
justice use key (`cj_use_allocation_2026_09_23` central set, 46.9% of line 4; arrests, custody and
ICE bed-days are not CPS-weighted); and the uninsured-use share behind the uncompensated-care shift
(`uncompensated_care_2026_09_23/uncompensated.py`). Hot-deck frames keep their values; only the
weights change, and the MEPS and school keys use the published frame. The household pool fraction
and the production term stay at their published values.
State-aware status flag (`california_medical_status_2026_09_23/cps_ca_status.py`, imported
read-only): the status lane's paper rules run on a copy of the status frame with MCAID set to "No" at
the state-ages of STATUS_BLIND_2024 (all listed states, or California alone), so Medicaid stops
signalling legal status where 2024 coverage ignored status. The audit's rules then apply to that
flag, alone and with the row-4 weights.
Step 5e's band changes use each line's adopted response (engine.js::spendingResponse under
main_case.js's CBO-lag profiles; the shared allocation sets the low end, the personal the high end),
checked against Node for every stack.

Gates, each stopping with [BLOCKED]:
1. without the rules every method's key shares equal the stored ones (ipw_key_shares.npz;
   hotdeck_key_shares.npz per seed and as seed means), and the between-seed spread of the
   whole-line change equals derived/hotdeck_seed_spread.csv;
2. at a uniform 0.44 with the old non-PTC range the combinations reproduce step 5c
   (derived/status_combination_components.csv): (b) +20.7 / +20.1 shared, +23.4 / +22.8 personal;
3. the Node translation equals the component or line-response arithmetic at both ends of the adopted
   band for every stack, before the long runs for the stacks without methods and at the end for all;
4. row 3: the published arm reproduces $128.46bn (shared) and $118.62bn (personal);
5. row 4: the ACS cells reproduce the Mexico-born lane's ACS 2024 totals and the PUMS; with scale
   factors of 1 the weights are bit-identical and every step-5d figure reproduces;
6. status: the variant path with no listed state-ages returns the paper flag bit for bit and
   reproduces every step-5d figure; the state-aware flags reproduce the California lane's union
   counts (5.2265M, 5.1589M);
7. the MEPS keys, the unit-split adults, the justice use target and the uncompensated-care shift
   reproduce the account's published values.
Replicate SEs are paired; for the hot decks the seed spread enters by Rubin's rule,
T = W + (1 + 1/M) B.
Outputs: derived/status_combination_onbooks_lane.csv (all stacks; column arm) and
derived/status_combination_onbooks_lane_row4_lines.csv (rows 3 and 4 alone, by line);
Node payloads and bands in _cache/.
Run from the repository root (after ipw.py, run_hotdeck.py and combine_status.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/cps_imputation_keys_2026_09_23/combine_onbooks_lane.py
`--inputs-only` stops after the input gates and the Node check of the stacks without methods
(writes _cache/ only).
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports: nothing written beside the imported scripts

import json  # noqa: E402
import zipfile  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import combine_status as cs  # noqa: E402
import common as c  # noqa: E402
import hotdeck  # noqa: E402
import ipw  # noqa: E402
import run_hotdeck  # noqa: E402
import translate  # noqa: E402

sys.path.insert(0, str(c.FISCAL / "build"))
from meps_health_transport_2024 import donor_model, read_meps  # noqa: E402  the spending builder's transport

sys.path.insert(0, str(c.FISCAL / "california_medical_status_2026_09_23"))
from cps_ca_status import CALIFORNIA, STATUS_BLIND_2024, blind_mask  # noqa: E402  the state-aware rule set

ONBOOKS = c.FISCAL / "onbooks_share_2026_09_23/derived"
MTS = c.FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json"
RECEIPTS = c.FISCAL / "full_account_receipts_2026_09_20/derived"
MEXBORN = c.FISCAL / "mexborn_count_2026_09_23/derived/annual_series.csv"
IPUMS = c.ROOT / "sources/immigration-fiscal/derived/ipums_usa/usa_00003_census1980-2000+acs2005-2024_mexborn.parquet"
PUMS = str(c.FISCAL / "dataset_integrity_2026_09_23/_cache/acs_person_{}.parquet")
MEPS = c.ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
MAIN_INPUTS = c.FISCAL / "main_case_2026_09_23/derived/inputs.json"
CJ = c.FISCAL / "cj_use_allocation_2026_09_23/derived"
UC = c.FISCAL / "uncompensated_care_2026_09_23/derived/summary.json"
CA_COUNTS = c.FISCAL / "california_medical_status_2026_09_23/derived/cps_counts_by_rules.csv"
REFUNDABLE = "refundable_tax_credits"
FEDERAL = "federal_income_tax"
MEDICAID_LINE = "medicaid_and_chip_other_medical"
ALLOC = ["personal", "shared"]
CASES = ("low", "central", "high")
GATE = ("gate", "uniform_0.44")
ORIGIN = [("origin", case) for case in CASES]
IPW = {"a_ipw_brief_cells": ("a_brief_cells", "material_5pct"),
       "a_ipw_plus_labor_force": ("a_plus_labor_force", "material_5pct"),
       "a_ipw_brief_cells_derived_material_1pct": ("a_brief_cells", "material_1pct"),
       "a_ipw_brief_cells_derived_any_flag": ("a_brief_cells", "any_flag")}
HOTDECK = ["b_hotdeck_union_matched", "b_matched_over_pooled", "b_hotdeck_union_matched_all_items",
           "b_matched_over_pooled_all_items"]
ENDS = [("shared", "low"), ("personal", "high")]
CA_TX = [6, 48]
AGE_EDGES = [5, 15, 25, 35, 45, 55, 65]  # 0-4, 5-14, 15-24, ..., 65+
MEPS_KEYS = {"medicare": ["TOTMCR24"], "medicaid": ["TOTMCD24"], "va_medical": ["TOTVA24"], "tricare": ["TOTTRI24"],
             "health_other": ["TOTVA24", "TOTTRI24", "TOTOFD24", "TOTSTL24"]}
SCHOOL_PROXY = {"education_mix": "age5_24", "school_operating": "age5_24", "postsecondary": "age18_24"}
SCHOOL_BAND = (0.63, 0.66)  # main_case_translate.js PROFILES, both CBO-lag profiles
WEIGHT_SETS = ["row4_identity", "row4", "row4_other_hispanic", "row4_usborn"]
FLAGS = {"paper_rerun": [], "state_aware_verified_states": STATUS_BLIND_2024,
         "state_aware_california": [e for e in STATUS_BLIND_2024 if e[0] == CALIFORNIA]}
# Variant name -> (weights, status flag). The identity variants are gates only.
VARIANTS = {"row4_identity": ("row4_identity", "paper"), "row4": ("row4", "paper"),
            "row4_other_hispanic": ("row4_other_hispanic", "paper"), "row4_usborn": ("row4_usborn", "paper"),
            "status_identity": ("published", "paper_rerun"),
            "status_state_aware": ("published", "state_aware_verified_states"),
            "status_state_aware_ca": ("published", "state_aware_california"),
            "row4+status_state_aware": ("row4", "state_aware_verified_states"),
            "row4+status_state_aware_ca": ("row4", "state_aware_california")}
IDENTITY = ["row4_identity", "status_identity"]
ARMS = ["medicare_key_fix", "row3", "row4", "row4_other_hispanic", "row4_usborn", "status_state_aware",
        "status_state_aware_ca", "row4+status_state_aware", "row4+status_state_aware_ca"]
LINE_ARMS = ["row3", "row4", "row4_other_hispanic", "row4_usborn"]
# cj_use_allocation_2026_09_23 central key set: the part of each component still charged per head
# (police half per head, courts' civil 40%, fire, border policing); the rest follows arrests, ACS
# custody or ICE bed-days, which the CPS does not weight.
PER_HEAD_PART = {"fire": 1.0, "police_cbp": 1.0, "police_ice_border": 1.0, "law_courts": 0.4,
                 "police_non_border": 0.5, "prisons": 0.0, "police_ice_interior": 0.0}
# uncompensated_care_2026_09_23/uncompensated.py: government offsets ($bn) and the uncompensated care
# they offset, VA and IHS removed from both (Coughlin et al. 2014 Table 4; KFF-Urban 2021 Table 1).
UC_OFFSETS = {
    2013: dict(total_uc=84.9 - 8.1 - 2.1, programs={"medicaid": 13.5, "medicare": 8.0,
               "state_local": 9.8 + 7.3 + 3.0 + 1.5 + 0.1}),
    2017: dict(total_uc=42.4 - 10.3 - 2.3, programs={"medicaid": 9.8, "state_local": 9.9 + 1.3}),
}
UC_KEYS = {"medicaid": "medicaid", "medicare": "meps_medicare", "health_other": "health_other",
           "per_head": "population"}


# ---------------------------------------------------------------------------------------------
# Shares
# ---------------------------------------------------------------------------------------------
def share_configs(d):
    """Per-person on-books shares, {(share_type, case): array}; only the audit's unauthorized use them."""
    split = pd.read_csv(ONBOOKS / "onbooks_split.csv").set_index("kind")
    built = json.loads((ONBOOKS / "onbooks_inputs.json").read_text())["construction"]["shares"]
    mex = d.PENATVTY.eq(303).to_numpy()
    configs, labels = {}, {}
    for case in CASES:
        r = split.loc[f"evidence_{case}"]
        if max(abs(r.s_mex - built[case][0]), abs(r.s_oth - built[case][1])) > 1e-12:
            raise SystemExit(f"[BLOCKED] on-books split and inputs disagree for the {case} case")
        configs[("origin", case)] = np.where(mex, r.s_mex, r.s_oth)
        labels[("origin", case)] = (r.s_mex, r.s_oth)
        configs[("uniform", case)] = np.full(len(d), r.uniform_equivalent)
        labels[("uniform", case)] = (r.uniform_equivalent, r.uniform_equivalent)
    configs[GATE] = np.full(len(d), 0.44)
    labels[GATE] = (0.44, 0.44)
    return configs, labels


def state_aware_flag(s, hh, d, entries):
    """cps_ca_status.status_sets: the paper rules on a copy of the status frame with MCAID "No" at
    the listed (state, first age, last age) entries; aligned to d's rows like cs.unauthorized."""
    state = s.PH_SEQ.map(d.drop_duplicates("PH_SEQ").set_index("PH_SEQ").GESTFIPS)
    if state.isna().any():
        raise SystemExit("[BLOCKED] status record without a household state")
    sm = s.assign(state=state.astype(int))
    sm.loc[blind_mask(sm, entries), "MCAID"] = 2
    return cs.unauthorized(sm.drop(columns="state"), hh, d)


def frame_vectors(frame, unauth, s, index, keys=None):
    """combine_status.status_vectors merged per allocation (spending names win, as in key_shares)."""
    rk, sk = cs.status_vectors(frame, unauth, s, index)
    out = {}
    for a in ALLOC:
        merged = {**rk[a], **sk[a]}
        out[a] = merged if keys is None else {k: merged[k] for k in keys}
    return out


def weigh(vectors, Wc, Wu, civ, union, keys=None, plain=None):
    """Union shares of `keys` (all when None) under one set of weights; other keys from `plain`."""
    out = dict(plain) if plain is not None else {}
    for a in ALLOC:
        for k in (vectors[a] if keys is None else keys):
            v = vectors[a][k]
            if np.any(v < 0):
                raise ValueError(f"Negative proxy {k}")
            out[(a, k)] = (v[union] @ Wu) / (v[civ] @ Wc)
    return out


def ipw_rule_shares(d, vec_d, W, civ, union, stored):
    """Each step-4a method with the audit's rules on the reweighted file: {method: {cfg: shares}}.
    Keys the rules touch are recomputed under the method's weights; the rest keep the stored shares.
    cfg None applies no rules (gated against the stored shares)."""
    cv = c.cell_vars(d)
    cv["union"] = union.astype(int)
    status = {rule: c.key_status(d, thr)[0] for rule, thr in ipw.THRESHOLDS.items()}
    out = {}
    for name, (spec, rule) in IPW.items():
        frames = [cv[cols] for cols in ipw.SPECS[spec]]
        res = {cfg: dict(stored[name]) for cfg in vec_d}
        groups = {}
        for a in ALLOC:
            for k in cs.STATUS_KEYS:
                if (a, k) not in stored[name]:
                    continue
                # ipw.py: the 1% and any-flag rules re-cut derived keys only; other keys keep 5%.
                derived = k in c.TAX_KEYS or k in ("consumption", "resources")
                imputed = status[rule if derived else "material_5pct"][a][k]
                groups.setdefault((a, imputed.tobytes()), []).append(k)
        for (a, sig), keys in groups.items():
            print(f"[onbooks] reweighting {name} {a} {', '.join(keys)}", flush=True)
            Wa = ipw.ipw_weights(W, ~np.frombuffer(sig, dtype=bool), civ, frames)[0]
            Wu, Wc = Wa[union], Wa[civ]
            for cfg in vec_d:
                for k in keys:
                    v = vec_d[cfg][a][k]
                    res[cfg][(a, k)] = (v[union] @ Wu) / (v[civ] @ Wc)
        out[name] = res
    return out


def hotdeck_rule_shares(d, flags, configs, W, weights, civ, union, index, hd):
    """Per (spec, variant): one {variant: {cfg: shares}} per seed. "published" holds every rule
    configuration under the published weights and paper flag (cfg None: no rules, gated per seed);
    each VARIANTS entry holds None and the origin cases on the same frames."""
    Wc, Wu = weights["published"]
    runs = {}
    for spec, (item_property, seeds) in run_hotdeck.SPECS.items():
        for seed in seeds:
            for variant, cells in [("matched", hotdeck.BASE), ("pooled", [])]:
                print(f"[onbooks] hot deck {spec} seed {seed} {variant}", flush=True)
                new, _ = hotdeck.run(d, seed=seed, verbose=False, base=cells, item_property=item_property)
                if not (new[["PH_SEQ", "PPPOS"]].to_numpy() == d[["PH_SEQ", "PPPOS"]].to_numpy()).all():
                    raise SystemExit("[BLOCKED] hot-deck frame rows do not align with the lane frame")
                plain = cs.key_shares(new, flags["paper"], None, W, civ, union, index)
                gap = max(np.abs(plain[k] - hd[f"{spec}|{variant}@{seed}|{k[0]}|{k[1]}"]).max() for k in plain)
                if gap > 1e-12:
                    raise SystemExit(f"[BLOCKED] hot-deck shares not reproduced for {spec} seed {seed} {variant}: {gap:.2e}")
                vecs = {"paper": {cfg: frame_vectors(new, flags["paper"], s, index, cs.STATUS_KEYS)
                                  for cfg, s in configs.items()}}
                for flag in FLAGS:
                    vecs[flag] = {cfg: frame_vectors(new, flags[flag], configs[cfg], index, cs.STATUS_KEYS)
                                  for cfg in ORIGIN}
                entry = {"published": {None: plain, **{cfg: weigh(vecs["paper"][cfg], Wc, Wu, civ, union,
                                                                  cs.STATUS_KEYS, plain) for cfg in configs}}}
                everything = frame_vectors(new, flags["paper"], None, index)
                plain_w = {"published": plain, **{w: weigh(everything, *weights[w], civ, union) for w in WEIGHT_SETS}}
                for name, (wname, flag) in VARIANTS.items():
                    p_v = plain_w[wname]
                    entry[name] = {None: p_v, **{cfg: weigh(vecs[flag][cfg], *weights[wname], civ, union,
                                                            cs.STATUS_KEYS, p_v) for cfg in ORIGIN}}
                runs.setdefault((spec, variant), []).append(entry)
        for variant in ["matched", "pooled"]:
            m = cs.mean_shares([r["published"][None] for r in runs[(spec, variant)]])
            gap = max(np.abs(m[k] - hd[f"{spec}|{variant}|{k[0]}|{k[1]}"]).max() for k in m)
            print(f"[onbooks] hot deck {spec} {variant}: seed means reproduced, max share difference {gap:.2e}", flush=True)
            if gap > 1e-12:
                raise SystemExit(f"[BLOCKED] hot-deck seed means not reproduced for {spec} {variant}")
    return runs


def hotdeck_label(spec, kind):
    return ("b_hotdeck_union_matched" if kind == "matched" else "b_matched_over_pooled") + \
        ("" if spec == "main" else f"_{spec}")


def assemble(V, cfg, audit, base, runs, ipw_res=None):
    """Methods' key shares under variant V with the rules at cfg (cfg None: the methods alone).
    The reweighting methods run under the published weights and paper flag only."""
    ref = base[V] if cfg is None else audit[V][cfg]
    methods = {name: ipw_res[name][cfg] for name in IPW} if ipw_res is not None else {}
    for spec in run_hotdeck.SPECS:
        m = cs.mean_shares([r[V][cfg] for r in runs[(spec, "matched")]])
        p = cs.mean_shares([r[V][cfg] for r in runs[(spec, "pooled")]])
        methods[hotdeck_label(spec, "matched")] = m
        methods[hotdeck_label(spec, "net")] = {k: ref[k] * m[k] / p[k] for k in ref}
    return methods


def seed_method_shares(V, cfg, audit, base, runs):
    """Each seed's key shares per hot-deck label, under variant V and rules cfg."""
    ref = base[V] if cfg is None else audit[V][cfg]
    out = {}
    for spec, (_, seeds) in run_hotdeck.SPECS.items():
        for i in range(len(seeds)):
            m = runs[(spec, "matched")][i][V][cfg]
            p = runs[(spec, "pooled")][i][V][cfg]
            out.setdefault(hotdeck_label(spec, "matched"), []).append(m)
            out.setdefault(hotdeck_label(spec, "net"), []).append({k: ref[k] * m[k] / p[k] for k in ref})
    return out


# ---------------------------------------------------------------------------------------------
# Step-5d translation (component arithmetic, as in step 5c)
# ---------------------------------------------------------------------------------------------
def band_reps(model, base, method, hf, fracs):
    """Change in the adopted band's cost ($bn, 161 replicates) per allocation: `whole` keys the whole
    refundable line as adopted; each named fraction applies the key change to that part of it only."""
    rows = translate.line_deltas(model, base, method, hf)
    comps = translate.components(rows, 0.0)  # CBO-lag profiles: economic affairs delayed at 0
    out = {}
    for a in ALLOC:
        refund = sum((x["reps"] for x in rows if x["allocation"] == a and x["preferred"] and x["line"] == REFUNDABLE),
                     np.zeros(161))
        net = comps[a]["net_cost_change"]
        out[a] = {"whole": net, "refund": refund, **{name: net - refund * (1 - f) for name, f in fracs.items()}}
    return out


def seed_points(model, base, hf, fracs, cfg, audit, runs):
    """Per (hot-deck label, allocation, convention): each seed's full-sample band change."""
    out = {}
    for label, per_seed in seed_method_shares("published", cfg, audit, base, runs).items():
        for shares in per_seed:
            for a, conv in band_reps(model, base["published"], shares, hf, fracs).items():
                for name, reps in conv.items():
                    out.setdefault((label, a, name), []).append(float(reps[0]))
    return out


def payload_from_rows(rows):
    """translate.translate's Node payload (point estimates); rows on one cell add up."""
    out = {"receipts": {}, "spending": {}}
    for x in rows:
        point = float(x["reps"][0])
        cell = (out["receipts"].setdefault(x["line"], {}) if x["side"] == "receipts"
                else out["spending"].setdefault(x["line"], {}).setdefault(x["key"], {}))
        cell[x["allocation"]] = cell.get(x["allocation"], 0.0) + point
    return out


def payload_for(model, base, method, hf, f):
    """Node payload for one method, the refundable line scaled to its non-PTC part."""
    return payload_from_rows([dict(x, reps=x["reps"] * (f if x["line"] == REFUNDABLE else 1.0))
                              for x in translate.line_deltas(model, base, method, hf)])


# ---------------------------------------------------------------------------------------------
# Step 5e inputs
# ---------------------------------------------------------------------------------------------
def row3_partition(d, W, civ, index, base, model):
    """The receipts lane's federal_gap_high_agi arm in share terms: target = s_liab x L + s_high x G,
    L the allocation's national CPS liability, G = BEA federal income tax - L."""
    rk = c.receipt_keys(d, index)
    p3 = next(x for x in model["receipts"]["lines"] if x["id"] == FEDERAL)["national_bn"]
    keys = pd.read_csv(RECEIPTS / "allocation_keys.csv").set_index(["allocation", "allocation_key"])
    cats = pd.read_csv(RECEIPTS / "category_allocations.csv")
    cats = cats[cats.category.eq(FEDERAL)].drop_duplicates(["scenario_id", "allocation"]).set_index(
        ["scenario_id", "allocation"]).target_bn
    part = {}
    for a in ALLOC:
        L = float(rk[a]["federal_liability"][civ] @ W[civ, 0]) / 1e9
        s_l, s_h = base[(a, "federal_liability")][0], base[(a, "federal_high_agi")][0]
        arm, cbo = s_l * L + s_h * (p3 - L), p3 * s_l
        print(f"[row3] {a}: CPS liability {L:.3f}bn, gap {p3 - L:.3f}bn, liability share {s_l:.5f}, high-AGI share "
              f"{s_h:.5f}; arm {arm:.4f} (published {cats[('federal_gap_high_agi', a)]:.4f}), liability-keyed "
              f"{cbo:.4f} (published {cats[('cbo_collective', a)]:.4f})", flush=True)
        errors = [abs(L - keys.loc[(a, "federal_liability"), "national_key_total"] / 1e9),
                  abs(s_h - keys.loc[(a, "federal_high_agi"), "target_key_share"]),
                  abs(arm - cats[("federal_gap_high_agi", a)]), abs(cbo - cats[("cbo_collective", a)])]
        if max(errors) > 1e-6:
            raise SystemExit(f"[BLOCKED] row 3 arm not reproduced for {a}: {errors}")
        part[a] = dict(L=L, G=p3 - L)
    return part


def row3_federal(rows, shares, base, part):
    """The federal income tax line under row 3: CPS part keyed by liability, gap part by high AGI,
    against the published liability-keyed line (so row 3's own change is included)."""
    out = []
    for x in rows:
        if x["side"] == "receipts" and x["line"] == FEDERAL:
            a, p = x["allocation"], part[x["allocation"]]
            liab, high = (a, "federal_liability"), (a, "federal_high_agi")
            x = dict(x, reps=p["L"] * shares[liab] + p["G"] * shares[high] - (p["L"] + p["G"]) * base[liab],
                     source="row 3: liability + BEA gap by high AGI")
        out.append(x)
    return out


def acs_cells():
    """ACS 2024 Mexico-born outside CA+TX by citizenship (IPUMS USA extract 3), and native-born
    Mexican-origin outside CA+TX (PUMS 2023, 2024), in the CPS universe: households plus
    noninstitutional group quarters."""
    lane = pd.read_csv(MEXBORN).set_index("year").loc[2024]
    a = pd.read_parquet(IPUMS, columns=["YEAR", "STRATA", "GQ", "PERWT", "BPL", "CITIZEN"], filters=[("YEAR", "==", 2024)])
    a = a[a.BPL.eq(200) & a.CITIZEN.isin([2, 3, 4, 5]) & a.GQ.isin([1, 2, 4, 5])]
    natz = a.CITIZEN.eq(2)
    totals = [(a.PERWT.sum(), lane.acs_mexborn_noninst_m), (a.PERWT[natz].sum(), lane.acs_mexborn_natz_noninst_m),
              (a.PERWT[~natz].sum(), lane.acs_mexborn_noncit_noninst_m)]
    if max(abs(got / 1e6 - ref) for got, ref in totals) > 1e-6:
        raise SystemExit("[BLOCKED] IPUMS extract 3 does not reproduce the Mexico-born lane's ACS 2024 totals")
    outside = ~(a.STRATA % 100).isin(CA_TX)  # IPUMS ACS strata end in the state FIPS code
    cells = {"natz": float(a.PERWT[outside & natz].sum()), "noncit": float(a.PERWT[outside & ~natz].sum())}
    p = pd.read_parquet(PUMS.format(2024), columns=["ST", "RELSHIPP", "POBP", "CIT", "PWGTP"])
    p = p[p.RELSHIPP.ne(37) & p.POBP.eq(303) & p.CIT.isin([4, 5]) & ~p.ST.isin(CA_TX)]
    check = {"natz": float(p.PWGTP[p.CIT.eq(4)].sum()), "noncit": float(p.PWGTP[p.CIT.eq(5)].sum())}
    if max(abs(cells[k] - check[k]) for k in cells) > 0.5:
        raise SystemExit(f"[BLOCKED] IPUMS state decoding disagrees with the PUMS: {cells} vs {check}")
    for y in (2023, 2024):
        p = pd.read_parquet(PUMS.format(y), columns=["ST", "RELSHIPP", "NATIVITY", "HISP", "PWGTP"])
        cells[f"native_mexican_{y}"] = float(p.PWGTP[p.RELSHIPP.ne(37) & p.NATIVITY.eq(1) & p.HISP.eq(2)
                                                     & ~p.ST.isin(CA_TX)].sum())
    # ACS years are centred on 1 July; 15 March 2025 is 8.5 months on (mexborn lane, annual_series.py).
    cells["native_mexican_projected"] = cells["native_mexican_2024"] + 8.5 / 12 * (
        cells["native_mexican_2024"] - cells["native_mexican_2023"])
    print(f"[row4] ACS 2024 Mexico-born outside CA+TX: naturalized {cells['natz'] / 1e6:.6f}M, noncitizen "
          f"{cells['noncit'] / 1e6:.6f}M (IPUMS = PUMS); native Mexican-origin outside CA+TX "
          f"{cells['native_mexican_2023'] / 1e6:.6f}M (2023), {cells['native_mexican_2024'] / 1e6:.6f}M (2024), "
          f"{cells['native_mexican_projected'] / 1e6:.6f}M at 15 March 2025", flush=True)
    return cells


def scale_cell(W, mask, target):
    """Scale the cell's weights so each of the 161 columns sums to target."""
    out = W.copy()
    factor = target / W[mask].sum(axis=0)
    out[mask] = W[mask] * factor
    return out, factor


def reassign_other_hispanic(d, W, W4, scaled):
    """Give each state x sex x age cell's removed Mexico-born weight to its other-Hispanic residents
    (not Mexican origin, not Mexico-born) in proportion to their weights, replicate by replicate.
    A cell without such residents in every replicate collapses to state x sex, then state."""
    removed = W - W4
    rec = d.PEHSPNON.eq(1).to_numpy() & d.PRDTHSP.between(2, 8).to_numpy() & ~d.PENATVTY.eq(303).to_numpy()
    st, sex = d.GESTFIPS.to_numpy(), d.A_SEX.to_numpy()
    age = np.digitize(d.A_AGE.to_numpy(), AGE_EDGES)
    out = W4.copy()
    pending = scaled.copy()
    for name, key in [("state x sex x age", st * 1000 + sex * 100 + age), ("state x sex", st * 1000 + sex * 100),
                      ("state", st * 1000)]:
        codes, inv = np.unique(key, return_inverse=True)
        rec_tot = np.zeros((len(codes), W.shape[1]))
        np.add.at(rec_tot, inv[rec], W[rec])
        ok = (rec_tot > 0).all(axis=1)
        take = pending & ok[inv]
        moved = np.zeros((len(codes), W.shape[1]))
        np.add.at(moved, inv[take], removed[take])
        share = np.divide(moved, rec_tot, out=np.zeros_like(moved), where=rec_tot > 0)
        out[rec] = out[rec] + W[rec] * share[inv[rec]]
        print(f"[row4] other-Hispanic reassignment at {name}: {W[take, 0].sum() / 1e6:.4f}M scaled persons, "
              f"{moved[:, 0].sum() / 1e6:.4f}M weight moved; largest recipient factor "
              f"{1 + share[:, 0].max():.3f}", flush=True)
        pending &= ~take
    if pending.any():
        raise SystemExit("[BLOCKED] removed Mexico-born weight left without other-Hispanic recipients")
    if np.abs(out.sum(axis=0) - W.sum(axis=0)).max() > 1e-3:
        raise SystemExit("[BLOCKED] other-Hispanic reassignment does not conserve the weight totals")
    return out


def weight_arms(d, W, cells):
    catx = d.GESTFIPS.isin(CA_TX).to_numpy()
    mb = d.PENATVTY.eq(303).to_numpy() & ~catx
    groups = {"natz": mb & d.PRCITSHP.eq(4).to_numpy(), "noncit": mb & d.PRCITSHP.eq(5).to_numpy()}
    arms, info = {}, {}
    ident = W
    for m in groups.values():
        ident, _ = scale_cell(ident, m, W[m].sum(axis=0))
    if not np.array_equal(ident, W):
        raise SystemExit("[BLOCKED] scale factors of 1 do not return the published weights bit for bit")
    print("[gate] row 4 with scale factors of 1: weights bit-identical to the published ones", flush=True)
    arms["row4_identity"] = ident
    W4 = W
    for g, m in groups.items():
        W4, f = scale_cell(W4, m, cells[g])
        info[f"factor_{g}"] = float(f[0])
        print(f"[row4] Mexico-born {g} outside CA+TX: ASEC {W[m, 0].sum() / 1e6:.6f}M (n {m.sum()}) -> ACS "
              f"{cells[g] / 1e6:.6f}M, factor {f[0]:.4f} (replicates {f[1:].min():.4f}-{f[1:].max():.4f})", flush=True)
    arms["row4"] = W4
    arms["row4_other_hispanic"] = reassign_other_hispanic(d, W, W4, groups["natz"] | groups["noncit"])
    nm = d.PRCITSHP.isin([1, 2, 3]).to_numpy() & d.PRDTHSP.eq(1).to_numpy() & ~catx
    W4u, f = scale_cell(W4, nm, cells["native_mexican_projected"])
    info["factor_native_mexican"] = float(f[0])
    print(f"[row4] native Mexican-origin outside CA+TX: ASEC {W[nm, 0].sum() / 1e6:.6f}M (n {nm.sum()}) -> "
          f"{cells['native_mexican_projected'] / 1e6:.6f}M, factor {f[0]:.4f}", flush=True)
    arms["row4_usborn"] = W4u
    return arms, info


def meps_vectors(d):
    """full_account_spending_2026_09_20/builder.py::build_keys: MEPS 2024 public payer means by age band x
    US/not-US birth, transported to every CPS person with a coverage record."""
    md, _ = read_meps(MEPS, MEPS.with_name("h256su.txt"))
    cells, codes, _ = donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid]
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    if d.loc[~exposure, "A_AGE"].gt(0).any():
        raise SystemExit("[BLOCKED] MEPS reference exclusion includes a noninfant")
    out = {}
    for name, cols in MEPS_KEYS.items():
        sums = sample.assign(wx=sample[cols].sum(axis=1) * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
        mean = (sums / pop).reindex(index)
        if mean.isna().any():
            raise SystemExit("[BLOCKED] unmatched MEPS payer cell")
        out[name] = mean.to_numpy()[codes] * exposure
    return out


def lane_of(side, key, allocation):
    """translate.KEYS: the lane key that measures an account key."""
    return translate.lane_key(translate.KEYS, side, key, allocation)


def extra_shares(meps, adults_unit, ages, Wc, Wu, civ, union, published_ages, school):
    """Account keys outside the lane's step-4 set, under one set of weights, named as translate.KEYS."""
    out = {}
    for name, v in meps.items():
        s = (v[union] @ Wu) / (v[civ] @ Wc)
        for a in ALLOC:
            out[(a, lane_of("spending", name, a))] = s
    out[("shared", lane_of("receipts", "adults", "shared"))] = (adults_unit[union] @ Wu) / (adults_unit[civ] @ Wc)
    for key, age_key in SCHOOL_PROXY.items():
        v = ages[age_key]
        ratio = ((v[union] @ Wu) / (v[civ] @ Wc)) / published_ages[age_key]
        for a in ALLOC:
            out[(a, key)] = school[(a, key)] * ratio
    return out


def justice_per_head_fraction(model):
    """Share of line 4 that the adopted use key still charges per head (so moves with the CPS)."""
    s = json.loads((CJ / "summary.json").read_text())
    split = pd.read_csv(CJ / "central_split.csv").set_index("component")
    central = s["central"]
    if (central["police_key"], central["court_criminal_share"], central["cbp_border"]) != ("half", 0.6, "per_head") \
            or set(split.index) != set(PER_HEAD_PART):
        raise SystemExit("[BLOCKED] the justice lane's central key set changed")
    head = s["shares"]["per_head"]
    use = {"law_courts": s["shares"]["arrest_adj"], "police_non_border": s["shares"]["arrest_adj"],
           "prisons": s["shares"]["custody_acs_adj"], "police_ice_interior": s["ice"]["q_central"]}
    rebuilt = sum(r.national_bn * (PER_HEAD_PART[k] * head + (1 - PER_HEAD_PART[k]) * use.get(k, head))
                  for k, r in split.iterrows())
    national = next(x for x in model["spending"]["lines"] if x["id"] == "public_order_safety")["national_bn"]
    frac = sum(r.national_bn * PER_HEAD_PART[k] for k, r in split.iterrows()) / national
    print(f"[justice] use target rebuilt {rebuilt:.4f}bn (lane {central['target_bn']:.4f}); per-head part "
          f"{frac:.4f} of line 4", flush=True)
    if abs(rebuilt - central["target_bn"]) > 1e-4 or abs(split.national_bn.sum() - national) > 1e-4:
        raise SystemExit("[BLOCKED] the justice use target is not reproduced")
    return frac


def uninsured_exposure(d):
    """uncompensated_care_2026_09_23: full-year uninsured + half of part-year (NOCOV_CYR 3, 2)."""
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        e = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "NOCOV_CYR"])
    e = d[["PH_SEQ", "PPPOS"]].merge(e, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if e.NOCOV_CYR.isna().any():
        raise SystemExit("[BLOCKED] NOCOV_CYR does not align with the lane frame")
    return e.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * e.NOCOV_CYR.eq(2).to_numpy(float)


def undercharged(summary, s, ratios):
    """inside_undercharged_bn at equal use (r = 1): min and max over the lane's arms, per replicate.
    s: the union's share of uninsured person-years; ratios: each account key's share over its
    published share."""
    aha, uplift = summary["aha_national_bn"], summary["uplift_2024"]
    keys = {p: summary["account_key_shares"][p] * ratios[p] for p in UC_KEYS}
    values = []
    for spec in UC_OFFSETS.values():
        total_off = sum(spec["programs"].values())
        g = total_off / spec["total_uc"]
        for state_local_key in ("health_other", "per_head"):
            k = sum(v / total_off * keys[state_local_key if p == "state_local" else p] for p, v in spec["programs"].items())
            for n in (aha, aha * uplift):
                values.append(g * (s - k) * n)
    values = np.array(values)
    return values.min(axis=0), values.max(axis=0)


def line_response(model, line, end, gg, school_bounds):
    """engine.js::spendingResponse under main_case.js's CBO-lag profiles. The low end of the adopted
    band is its least-cost corner (general government at its low response, the largest school share
    at the lower school response), the high end the most-cost corner."""
    rc = line["response_class"]
    if rc == "household_transfer":
        return 1.0
    if rc == "public_goods":
        return gg[end] if line["id"] == "general_public_services" else 0.0
    if rc == "service":
        if line["id"] == "education_services":
            share, r = (school_bounds[1], SCHOOL_BAND[0]) if end == "low" else (school_bounds[0], SCHOOL_BAND[1])
            return share * r + (1 - share)  # other education responds at 1 in the adopted profile
        return 0.0 if line["id"] in model["service"]["delayed"] else 1.0
    return 0.0  # interest, subsidies, foreign flows, rounding


def band_ends(rows, coef):
    """Cost change at each end of the adopted band (161 replicates): shared = low end, personal = high."""
    out = {"low": np.zeros(161), "high": np.zeros(161)}
    for x in rows:
        end = "low" if x["allocation"] == "shared" else "high"
        if x["side"] == "receipts":
            k = -1.0 if x["direct"] else 0.0
        else:
            k = coef[(x["line"], end)] if x["preferred"] else 0.0
        out[end] = out[end] + k * x["reps"]
    return out


def rubin(se, values):
    m = len(values)
    return (se ** 2 + (1 + 1 / m) * float(np.var(values, ddof=1))) ** 0.5


def node_bands(payload, stem):
    deltas, bands = c.CACHE / f"{stem}_line_deltas.json", c.CACHE / f"{stem}_translation.csv"
    deltas.write_text(json.dumps(payload, indent=1) + "\n")
    translate.run_node(deltas, bands)
    return pd.read_csv(bands).query("profile == 'cbo_category_lag_non_school_full'").set_index("method")


def main():
    inputs_only = "--inputs-only" in sys.argv[1:]
    d = c.load_frame()
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    Wc, Wu = W[civ], W[union]
    index = c.spm_index(d)
    s_in, hh = cs.status_inputs()
    unauth = cs.unauthorized(s_in, hh, d)
    mex = d.PENATVTY.eq(303).to_numpy()
    w0 = W[:, 0]
    for label, g in [("Mexico-born", unauth & mex), ("other Latin-American-born", unauth & ~mex)]:
        print(f"[onbooks] audit's unauthorized, {label}: {w0[g].sum() / 1e6:.3f}M, "
              f"in the union {w0[g & union].sum() / 1e6:.3f}M", flush=True)
    configs, labels = share_configs(d)
    model = json.loads(translate.MODEL.read_text())
    mts = json.loads(MTS.read_text())
    line = next(x for x in model["spending"]["lines"] if x["id"] == REFUNDABLE)
    if abs(line["national_bn"] - mts["bea_line25_cy2024_bn"]) > 1e-6:
        raise SystemExit("[BLOCKED] the model's refundable line is not the BEA line of the MTS split")
    f_new = mts["non_ptc_remainder_bn"] / line["national_bn"]
    print(f"[onbooks] non-PTC fraction {mts['non_ptc_remainder_bn']} / {line['national_bn']} = {f_new:.5f}", flush=True)
    fracs = {"non_ptc": f_new}
    hf = translate.household_fraction(d)

    # Gate 1: published shares and the rules' fast path.
    stored_base, stored_ipw = translate.ipw_methods()
    base = cs.key_shares(d, unauth, None, W, civ, union, index)
    gap = max(np.abs(base[k] - stored_base[k]).max() for k in stored_base)
    vec_d = {None: frame_vectors(d, unauth, None, index, cs.STATUS_KEYS)}
    vec_d.update({cfg: frame_vectors(d, unauth, s, index, cs.STATUS_KEYS) for cfg, s in configs.items()})
    audit = {cfg: weigh(vec_d[cfg], Wc, Wu, civ, union, cs.STATUS_KEYS, base) for cfg in configs}
    full = cs.key_shares(d, unauth, configs[GATE], W, civ, union, index)
    gap = max(gap, max(np.abs(audit[GATE][k] - full[k]).max() for k in full))
    print(f"[onbooks] published shares and rule-only path reproduced, max share difference {gap:.2e}", flush=True)
    if gap > 1e-12:
        raise SystemExit("[BLOCKED] published shares or the rule-only path not reproduced")

    # Step 5e inputs, gated before the long runs. Status flags first.
    flags = {"paper": unauth, **{name: state_aware_flag(s_in, hh, d, entries) for name, entries in FLAGS.items()}}
    if not np.array_equal(flags["paper_rerun"], unauth):
        raise SystemExit("[BLOCKED] the state-aware path without listed state-ages does not return the paper flag")
    counts = pd.read_csv(CA_COUNTS).query("region == 'US' and group == 'union'").set_index("rules").unauthorized_millions
    worst = 0.0
    for name, lane_rules in [("paper", "borjas_paper_rules"), ("state_aware_verified_states", "state_aware_verified_states"),
                             ("state_aware_california", "state_aware_california")]:
        got = w0[flags[name] & union].sum() / 1e6
        worst = max(worst, abs(got - counts[lane_rules]))
        print(f"[status] {name}: audit's unauthorized {w0[flags[name]].sum() / 1e6:.3f}M, in the union {got:.4f}M "
              f"(California lane {counts[lane_rules]:.4f}M)", flush=True)
    print("[gate] status variant without listed state-ages: flag bit-identical to the paper rules", flush=True)
    if worst > 5.1e-5:
        raise SystemExit("[BLOCKED] the state-aware flags do not reproduce the California lane's union counts")
    # Who the state-aware flag adds, and where the union's unauthorized live (row 4 acts outside CA+TX).
    aware = flags["state_aware_verified_states"]
    ca, catx, young = (d.GESTFIPS.eq(CALIFORNIA).to_numpy(), d.GESTFIPS.isin(CA_TX).to_numpy(),
                       d.A_AGE.lt(19).to_numpy())
    per_person = {"federal liability": d.FEDTAX_BC.to_numpy(float), "wages": d.WSAL_VAL.to_numpy(float),
                  "EITC": d.EIT_CRED.to_numpy(float)}
    print(f"[status] union members the state-aware flag reclassifies as legal: {w0[unauth & ~aware & union].sum():.0f}",
          flush=True)
    for label, g in [("paper-rule unauthorized", unauth & union), ("added by the state-aware flag", aware & ~unauth & union)]:
        n = w0[g].sum()
        means = ", ".join(f"{k} ${(w0[g] @ v[g]) / n:,.0f}" for k, v in per_person.items())
        print(f"[status] union, {label}: {n / 1e6:.4f}M; California {w0[g & ca].sum() / n:.1%}, outside CA+TX "
              f"{w0[g & ~catx].sum() / n:.1%}, under 19 {w0[g & young].sum() / n:.1%}; per person {means}", flush=True)
    part = row3_partition(d, W, civ, index, base, model)
    high = d.AGI.ge(500000).to_numpy()
    print(f"[row3] audit's unauthorized with AGI >= $500k: {w0[unauth & high].sum() / 1e3:.1f}k persons, "
          f"{(w0 * d.FEDTAX_BC.to_numpy(float))[unauth & high].sum() / 1e9:.3f}bn liability; in the union "
          f"{w0[unauth & high & union].sum() / 1e3:.1f}k, "
          f"{(w0 * d.FEDTAX_BC.to_numpy(float))[unauth & high & union].sum() / 1e9:.3f}bn", flush=True)
    rv, (imputed, _, _) = c.receipt_vectors(d), c.key_status(d, 0.05)
    for key in ["federal_liability", "federal_high_agi"]:
        v, imp = rv[key], imputed["personal"][key]
        print(f"[row3] union {key}: {int((union & (v > 0)).sum())} records with a positive value; imputed tax units "
              f"(5% rule) carry {(w0 * v)[union & imp].sum() / (w0 * v)[union].sum():.1%} of the dollars", flush=True)
    # The audit's rules leave the high-AGI key alone. Sensitivity: scale it too, at the central shares.
    hv = rv["federal_high_agi"]
    scaled = hv * np.where(unauth, configs[("origin", "central")], 1.0)
    for a in ALLOC:
        h0, h1 = (hv, scaled) if a == "personal" else (c.unit_equal(hv, index), c.unit_equal(scaled, index))
        s0, s1 = [(h[union] @ w0[union]) / (h[civ] @ w0[civ]) for h in (h0, h1)]
        if abs(s0 - base[(a, "federal_high_agi")][0]) > 1e-12:
            raise SystemExit("[BLOCKED] the union's high-AGI share is not reproduced")
        print(f"[row3] {a}: union high-AGI share {s0:.5f}, {s1:.5f} if the rules also scaled that key at the "
              f"central shares; row 2 under row 3 would then cost {part[a]['G'] * (s0 - s1):.3f}bn more", flush=True)
    cells = acs_cells()
    arms_w, arm_info = weight_arms(d, W, cells)
    weights = {"published": (Wc, Wu), **{name: (Wv[civ], Wv[union]) for name, Wv in arms_w.items()}}
    for name, (wname, flag) in VARIANTS.items():
        Wv = arms_w.get(wname, W)
        print(f"[variant] {name}: civilians {Wv[civ, 0].sum() / 1e6:.3f}M, union {Wv[union, 0].sum() / 1e6:.3f}M, "
              f"audit's unauthorized in the union {Wv[flags[flag] & union, 0].sum() / 1e6:.3f}M "
              f"(all audit's unauthorized {Wv[flags[flag] & civ, 0].sum() / 1e6:.3f}M)", flush=True)
    del arms_w
    everything = frame_vectors(d, unauth, None, index)
    plain_w = {"published": base, **{w: weigh(everything, *weights[w], civ, union) for w in WEIGHT_SETS}}
    vec_flag = {"paper": vec_d, **{f: {cfg: frame_vectors(d, flags[f], configs[cfg], index, cs.STATUS_KEYS)
                                       for cfg in ORIGIN} for f in FLAGS}}
    base_all, audit_all = {"published": base}, {"published": audit}
    for name, (wname, flag) in VARIANTS.items():
        base_all[name] = plain_w[wname]
        audit_all[name] = {cfg: weigh(vec_flag[flag][cfg], *weights[wname], civ, union, cs.STATUS_KEYS, plain_w[wname])
                           for cfg in ORIGIN}
    for name in IDENTITY:
        worst = max(np.abs(base_all[name][k] - base[k]).max() for k in base)
        worst = max(worst, max(np.abs(audit_all[name][cfg][k] - audit[cfg][k]).max()
                               for cfg in ORIGIN for k in audit[cfg]))
        print(f"[gate] {name}: shares equal the published ones, max difference {worst:.1e}", flush=True)
        if worst > 1e-15:
            raise SystemExit(f"[BLOCKED] {name} does not reproduce the published shares")

    meps = meps_vectors(d)
    rk_pub = c.receipt_keys(d, index)
    ages = {k: c.spending_vectors(d, index)["personal"][k] for k in ["age5_24", "age18_24"]}
    published_ages = {k: (v[union] @ Wu) / (v[civ] @ Wc) for k, v in ages.items()}
    lines_by_id = {x["id"]: x for x in model["spending"]["lines"]}
    receipts_by_id = {x["id"]: x for x in model["receipts"]["lines"]}
    school = {(a, k): lines_by_id[ln]["keys"][k][a]["share"] for ln, k in
              [("education_services", "education_mix"), ("education_services", "school_operating"),
               ("education_benefits", "postsecondary")] for a in ALLOC}
    extra_w = {w: extra_shares(meps, rk_pub["shared"]["adults"], ages, *weights[w], civ, union, published_ages, school)
               for w in weights}
    checks = [(extra_w["published"][(a, lane_of("spending", n, a))][0],
               lines_by_id[ln]["keys"][n][a]["share"]) for a in ALLOC for n, ln in
              [("medicare", "medicare"), ("medicaid", MEDICAID_LINE), ("health_other", "health_services"),
               ("tricare", "military_medical"), ("va_medical", "veterans_other")]]
    checks.append((extra_w["published"][("shared", lane_of("receipts", "adults", "shared"))][0],
                   receipts_by_id["personal_motor_vehicle"]["cells"]["cbo_collective"]["shared"]["share"]))
    worst = max(abs(x - y) for x, y in checks)
    print(f"[gate] MEPS payer keys and unit-split adults reproduce the account's shares, max difference {worst:.1e}",
          flush=True)
    if worst > 1e-6:
        raise SystemExit("[BLOCKED] MEPS payer keys or unit-split adults not reproduced")
    po_fraction = justice_per_head_fraction(model)
    uc = json.loads(UC.read_text())
    adopted_uc = json.loads(MAIN_INPUTS.read_text())["uncompensated_inside_bn"]
    exposure = uninsured_exposure(d)

    def uc_ends(wname):
        Wc_v, Wu_v = weights[wname]
        s = (exposure[union] @ Wu_v) / (exposure[civ] @ Wc_v)
        ratios = {p: extra_w[wname][("personal", k)] / extra_w["published"][("personal", k)] if k != "population"
                  else plain_w[wname][("personal", "population")] / base[("personal", "population")]
                  for p, k in UC_KEYS.items()}
        return s, undercharged(uc, s, ratios)

    s_pub, (uc_low, uc_high) = uc_ends("published")
    print(f"[uc] union share of uninsured person-years {s_pub[0]:.5f} (lane {uc['target_share']:.5f}); "
          f"inside under-charge {uc_low[0]:.4f}-{uc_high[0]:.4f}bn (adopted {adopted_uc['equal_low']:.4f}-"
          f"{adopted_uc['equal_high']:.4f})", flush=True)
    if max(abs(s_pub[0] - uc["target_share"]), abs(uc_low[0] - adopted_uc["equal_low"]),
           abs(uc_high[0] - adopted_uc["equal_high"])) > 1e-9:
        raise SystemExit("[BLOCKED] the uncompensated-care shift is not reproduced")
    uc_rows = {}
    for wname in WEIGHT_SETS:
        s_v, (lo, hi) = uc_ends(wname)
        uc_rows[wname] = [dict(side="spending", line=MEDICAID_LINE, key="medicaid", allocation=a, preferred=True,
                               direct=False, response_class="household_transfer", target_bn=pub[0], reps=new - pub,
                               source="uncompensated-care shift (uninsured use)")
                          for a, new, pub in [("shared", lo, uc_low), ("personal", hi, uc_high)]]
        print(f"[uc] {wname}: uninsured share {s_v[0]:.5f}, under-charge {lo[0]:.4f}-{hi[0]:.4f}bn "
              f"(change {lo[0] - uc_low[0]:+.4f} / {hi[0] - uc_high[0]:+.4f})", flush=True)

    gg = json.loads(MAIN_INPUTS.read_text())["general_government_response"]
    school_bounds = (min(p["school_share"] for p in model["service"]["profiles"] if p["school_share"] > 0),
                     max(p["school_share"] for p in model["service"]["profiles"] if p["school_share"] > 0))
    coef = {(ln["id"], end): line_response(model, ln, end, gg, school_bounds)
            for ln in model["spending"]["lines"] for end in ["low", "high"]}
    base_fixed = {**base, **extra_w["published"]}
    # Every key of a responsive line or direct receipt must be recomputed under the weight arms.
    used = [("spending", ln["preferred_key"], a) for ln in model["spending"]["lines"] for a in ALLOC
            if max(coef[(ln["id"], e)] for e in ["low", "high"]) > 0]
    used += [("receipts", x["cells"]["cbo_collective"][a]["key"], a) for x in model["receipts"]["lines"]
             for a in ALLOC if x["cells"]["cbo_collective"][a]["direct"]]
    uncovered = sorted({(side, key) for side, key, a in used if (a, lane_of(side, key, a)) not in base_fixed})
    print(f"[gate] responsive keys without a recomputed share: {uncovered or 'none'}", flush=True)
    if uncovered:
        raise SystemExit("[BLOCKED] a responsive key of the adopted case is not recomputed")
    weights_of = {"published": "published", **{v: w for v, (w, _) in VARIANTS.items()}}

    def stack(shares, V, row3=False, f=None):
        """Line deltas of one stack against the published account (the refundable line at f)."""
        f = f_new if f is None else f
        wname = weights_of[V]
        rows = translate.line_deltas(model, base_fixed, {**shares, **extra_w[wname]}, hf)
        rows = [dict(x, source="account key (MEPS medicare or unit-split adults)")
                if lane_of(x["side"], x["key"], x["allocation"]) != x["key"] else x for x in rows]
        rows = [dict(x, reps=x["reps"] * po_fraction, source="per-head part of the justice use key")
                if x["side"] == "spending" and x["line"] == "public_order_safety" and x["key"] == "population"
                else x for x in rows]
        if wname != "published":
            rows = rows + uc_rows[wname]
        rows = [dict(x, reps=x["reps"] * f) if x["line"] == REFUNDABLE else x for x in rows]
        return row3_federal(rows, shares, base, part) if row3 else rows

    def ends(shares, V, row3=False, f=None):
        return band_ends(stack(shares, V, row3, f), coef)

    def ref_ends(shares, mkf):
        """A stack under the published weights; for the key-fix arm, as steps 5-5d were first
        translated (translate.AS_PUBLISHED)."""
        if not mkf:
            return ends(shares, "published")
        rows = translate.line_deltas(model, base, shares, hf, translate.AS_PUBLISHED)
        return band_ends([dict(x, reps=x["reps"] * f_new) if x["line"] == REFUNDABLE else x for x in rows], coef)

    # Gate 3 (first pass): Node against the line-response arithmetic for the stacks without methods.
    early, early_payload = [], {}
    for arm in ["published_zero", "row3", *VARIANTS]:
        V = arm if arm in VARIANTS else "published"
        for cfg in [None, *ORIGIN]:
            shares = base_all[V] if cfg is None else audit_all[V][cfg]
            rows = stack(shares, V, arm == "row3")
            key = f"{arm}|{'none' if cfg is None else cfg[1]}"
            early_payload[key] = payload_from_rows(rows)
            e = band_ends(rows, coef)
            early += [dict(stack_id=key, allocation=a, band_end=end, change_bn=e[end][0], se_bn=c.sdr(e[end]))
                      for a, end in ENDS]
            if arm == "published_zero":
                break
    node = node_bands(early_payload, "onbooks_lane_inputs")
    early = pd.DataFrame(early)
    early["node_bn"] = [node.loc[k, f"change_{end}_bn"] for k, end in zip(early.stack_id, early.band_end)]
    worst = (early.node_bn - early.change_bn).abs().max()
    print(early.round(4).to_string(index=False), flush=True)
    print(f"[gate] Node band = line-response arithmetic for {len(early)} stack ends without methods, "
          f"max difference {worst:.1e} bn", flush=True)
    if worst > 1e-3 or early.loc[early.stack_id.eq("published_zero|none"), "change_bn"].abs().max() > 0:
        raise SystemExit("[BLOCKED] the Node band does not equal the line-response arithmetic")
    if inputs_only:
        print(json.dumps(arm_info), flush=True)
        return

    # Methods: gate 1 continued.
    ipw_res = ipw_rule_shares(d, vec_d, W, civ, union, stored_ipw)
    for name in IPW:
        gap = max(np.abs(ipw_res[name][None][k] - stored_ipw[name][k]).max() for k in stored_ipw[name])
        print(f"[onbooks] {name} reproduced without the rules, max share difference {gap:.2e}", flush=True)
        if gap > 1e-12:
            raise SystemExit(f"[BLOCKED] {name} shares not reproduced")
    hd = np.load(c.CACHE / "hotdeck_key_shares.npz")
    runs = hotdeck_rule_shares(d, flags, configs, W, weights, civ, union, index, hd)
    for name in IDENTITY:
        worst = max(np.abs(r[name][cfg][k] - r["published"][cfg][k]).max()
                    for key in runs for r in runs[key] for cfg in [None, *ORIGIN] for k in r["published"][cfg])
        print(f"[gate] {name}: hot-deck shares equal the published ones, max difference {worst:.1e}", flush=True)
        if worst > 1e-15:
            raise SystemExit(f"[BLOCKED] {name} does not reproduce the hot-deck shares")
    alone = assemble("published", None, audit_all, base_all, runs, ipw_res)
    stored_hd = translate.hotdeck_methods()
    for name, method in alone.items():
        ref = stored_ipw[name] if name in stored_ipw else stored_hd[name]
        gap = max(np.abs(method[k] - ref[k]).max() for k in ref)
        if gap > 1e-12:
            raise SystemExit(f"[BLOCKED] {name} method shares not reproduced: {gap:.2e}")
    alone_seeds = seed_points(model, base_all, hf, fracs, None, audit_all, runs)
    spread = pd.read_csv(c.OUT / "hotdeck_seed_spread.csv").query("component == 'net_cost_change'")
    gap = max(abs(np.std(alone_seeds[(r.method, r.allocation, "whole")], ddof=1) - r.between_seed_sd_bn)
              for r in spread.itertuples())
    print(f"[onbooks] seed spread reproduced, max difference {gap:.2e} bn", flush=True)
    if gap > 1e-9:
        raise SystemExit("[BLOCKED] between-seed spread not reproduced")

    # Gate 2: step 5c at a uniform 0.44 under the old non-PTC range.
    old = dict(zip(["non_ptc_low", "non_ptc_high"], cs.NON_PTC_FRACTION))
    step5c = pd.read_csv(c.OUT / "status_combination_components.csv").set_index(["method", "allocation"])
    at44 = assemble("published", GATE, audit_all, base_all, runs, ipw_res)
    worst = 0.0
    for name, shares in [("status_0.44", audit[GATE]),
                         ("a_ipw_brief_cells+status_0.44", at44["a_ipw_brief_cells"]),
                         ("b_hotdeck_union_matched+status_0.44", at44["b_hotdeck_union_matched"]),
                         ("b_matched_over_pooled+status_0.44", at44["b_matched_over_pooled"])]:
        br = band_reps(model, base, shares, hf, old)
        for a, _ in ENDS:
            r = step5c.loc[(name, a)]
            pairs = [(br[a]["whole"][0], r.change_bn), (c.sdr(br[a]["whole"]), r.se_bn),
                     (br[a]["non_ptc_low"][0], r.net_cost_change_non_ptc_low_bn),
                     (br[a]["non_ptc_high"][0], r.net_cost_change_non_ptc_high_bn)]
            worst = max(worst, max(abs(x - y) for x, y in pairs))
            print(f"[gate] {name:38s} {a:8s} whole {br[a]['whole'][0]:+.2f}, old non-PTC "
                  f"{br[a]['non_ptc_high'][0]:+.2f} to {br[a]['non_ptc_low'][0]:+.2f}", flush=True)
    print(f"[gate] step 5c reproduced at uniform 0.44, max difference {worst:.2e} bn", flush=True)
    if worst > 1e-6:
        raise SystemExit("[BLOCKED] step 5c not reproduced at uniform 0.44")

    # Step 5d: the on-books lane's cases, origin-specific and uniform.
    alone_br = {name: band_reps(model, base, m, hf, fracs) for name, m in alone.items()}
    rows, payload = [], {f"alone|{n}": payload_for(model, base, m, hf, f_new) for n, m in alone.items()}
    for cfg in [k for k in configs if k != GATE]:
        stype, case = cfg
        print(f"[onbooks] translating {stype} {case}", flush=True)
        combined = assemble("published", cfg, audit_all, base_all, runs, ipw_res)
        seeds = seed_points(model, base_all, hf, fracs, cfg, audit_all, runs)
        payload[f"{stype}|{case}|audit_rules_alone"] = payload_for(model, base, audit[cfg], hf, f_new)
        audit_br = band_reps(model, base, audit[cfg], hf, fracs)
        brs = {}
        for name, shares in combined.items():
            payload[f"{stype}|{case}|{name}"] = payload_for(model, base, shares, hf, f_new)
            brs[name] = band_reps(model, base, shares, hf, fracs)
        for a, end in ENDS:
            head = dict(share_type=stype, case=case, s_mexico=labels[cfg][0], s_other_latin=labels[cfg][1],
                        allocation=a, band_end=end)
            A = audit_br[a]["non_ptc"]
            rows.append(dict(head, method="audit_rules_alone", change_bn=A[0], change_se_bn=c.sdr(A),
                             change_total_se_bn=c.sdr(A), whole_line_change_bn=audit_br[a]["whole"][0],
                             refundable_nonptc_bn=audit_br[a]["refund"][0] * f_new))
            for name, br in brs.items():
                C = br[a]["non_ptc"]
                inc = C - A
                se, se_inc, total, total_inc, m = c.sdr(C), c.sdr(inc), None, None, np.nan
                if (name, a, "non_ptc") in seeds:
                    values = seeds[(name, a, "non_ptc")]
                    m, b = len(values), float(np.var(values, ddof=1))
                    total, total_inc = (se ** 2 + (1 + 1 / m) * b) ** 0.5, (se_inc ** 2 + (1 + 1 / m) * b) ** 0.5
                lane = alone_br[name][a]["non_ptc"][0]
                rows.append(dict(head, method=name, change_bn=C[0], change_se_bn=se,
                                 change_total_se_bn=se if total is None else total,
                                 increment_bn=inc[0], increment_se_bn=se_inc,
                                 increment_total_se_bn=se_inc if total_inc is None else total_inc,
                                 lane_alone_bn=lane, interaction_bn=inc[0] - lane, seeds=m,
                                 whole_line_change_bn=br[a]["whole"][0],
                                 refundable_nonptc_bn=br[a]["refund"][0] * f_new))
    out = pd.DataFrame(rows)

    # Gates 5 and 6 (figures): the identity variants reproduce the step-5d (b) stacks.
    for variant in IDENTITY:
        worst = 0.0
        for cfg in ORIGIN:
            comb_i = assemble(variant, cfg, audit_all, base_all, runs)
            R2 = ends(audit_all[variant][cfg], variant)
            ref = out[(out.share_type == "origin") & (out.case == cfg[1])].set_index(["allocation", "method"])
            for a, end in ENDS:
                worst = max(worst, abs(R2[end][0] - ref.loc[(a, "audit_rules_alone"), "change_bn"]))
                for name in HOTDECK:
                    M = ends(comb_i[name], variant)
                    worst = max(worst, abs(M[end][0] - ref.loc[(a, name), "change_bn"]),
                                abs(c.sdr(M[end] - R2[end]) - ref.loc[(a, name), "increment_se_bn"]))
        print(f"[gate] {variant} reproduces the step-5d figures, max difference {worst:.1e} bn", flush=True)
        if worst > 1e-9:
            raise SystemExit(f"[BLOCKED] {variant} does not reproduce step 5d")

    # Step 5e.
    arm_rows, line_rows = [], []
    pub_seeds = {cfg: seed_method_shares("published", cfg, audit_all, base_all, runs) for cfg in [None, *ORIGIN]}
    reference = {}

    def ref_stack(cfg, name, mkf):
        """The same stack under the published weights, paper flag and liability keying; for the key
        fix, as first translated."""
        key = (cfg, name, mkf)
        if key not in reference:
            if name == "audit_rules_alone":
                shares = audit[cfg]
            elif cfg is None:
                shares = alone[name]
            else:
                shares = assemble("published", cfg, audit_all, base_all, runs, ipw_res)[name]
            reference[key] = ref_ends(shares, mkf)
        return reference[key]

    for arm in ARMS:
        V = arm if arm in VARIANTS else "published"
        row3, mkf = arm == "row3", arm == "medicare_key_fix"
        methods = list(IPW) + HOTDECK if V == "published" else HOTDECK
        print(f"[5e] {arm}", flush=True)
        rows_A = stack(base_all[V], V, row3)
        A0 = band_ends(rows_A, coef)
        if not mkf:
            payload[f"{arm}|none|arm_alone"] = payload_from_rows(rows_A)
            A0w = ends(base_all[V], V, row3, f=1.0)
            for a, end in ENDS:
                arm_rows.append(dict(arm=arm, share_type="", case="none", allocation=a, band_end=end,
                                     method="arm_alone", change_bn=A0[end][0], change_se_bn=c.sdr(A0[end]),
                                     change_total_se_bn=c.sdr(A0[end]), whole_line_change_bn=A0w[end][0],
                                     arm_increment_bn=A0[end][0], arm_increment_se_bn=c.sdr(A0[end]),
                                     arm_increment_total_se_bn=c.sdr(A0[end])))
        if arm in LINE_ARMS:
            for x in rows_A:
                if x["side"] == "receipts" or x["preferred"]:
                    endx = "low" if x["allocation"] == "shared" else "high"
                    k = (-1.0 if x["direct"] else 0.0) if x["side"] == "receipts" else coef[(x["line"], endx)]
                    # The premium receipt's "medicare" is the lane's MCARE coverage key, not a MEPS key.
                    meps = x["side"] == "spending" and x["key"] in MEPS_KEYS
                    source = x.get("source", "MEPS payer key" if meps else
                                   "school proxy (age share)" if x["key"] in SCHOOL_PROXY else "lane CPS key")
                    line_rows.append(dict(arm=arm, side=x["side"], line=x["line"], key=x["key"],
                                          allocation=x["allocation"], band_end=endx, response=k,
                                          published_target_bn=x["target_bn"], target_change_bn=float(x["reps"][0]),
                                          target_change_se_bn=c.sdr(x["reps"]), band_change_bn=k * float(x["reps"][0]),
                                          source=source))
        ipw_v = ipw_res if V == "published" else None
        lane_alone = assemble(V, None, audit_all, base_all, runs, ipw_v)
        for cfg in [None, *ORIGIN]:
            case = "alone" if cfg is None else cfg[1]
            head = dict(arm=arm, share_type="" if cfg is None else cfg[0], case=case,
                        s_mexico=np.nan if cfg is None else labels[cfg][0],
                        s_other_latin=np.nan if cfg is None else labels[cfg][1])
            R2 = A0
            if cfg is not None:
                shares = audit_all[V][cfg]
                rows_R = stack(shares, V, row3)
                R2 = band_ends(rows_R, coef)
                R2_ref = ref_stack(cfg, "audit_rules_alone", mkf)
                R2w = ends(shares, V, row3, f=1.0)
                if not mkf:
                    payload[f"{arm}|{case}|audit_rules_alone"] = payload_from_rows(rows_R)
                for a, end in ENDS:
                    inc2, arm_inc = R2[end] - A0[end], R2[end] - R2_ref[end]
                    arm_rows.append(dict(head, allocation=a, band_end=end, method="audit_rules_alone",
                                         change_bn=R2[end][0], change_se_bn=c.sdr(R2[end]),
                                         change_total_se_bn=c.sdr(R2[end]), whole_line_change_bn=R2w[end][0],
                                         increment_bn=inc2[0], increment_se_bn=c.sdr(inc2),
                                         increment_total_se_bn=c.sdr(inc2), arm_increment_bn=arm_inc[0],
                                         arm_increment_se_bn=c.sdr(arm_inc), arm_increment_total_se_bn=c.sdr(arm_inc),
                                         overlap_bn=np.nan if mkf else R2_ref[end][0] - inc2[0]))
            combined = lane_alone if cfg is None else assemble(V, cfg, audit_all, base_all, runs, ipw_v)
            seeds_v = seed_method_shares(V, cfg, audit_all, base_all, runs)
            for name in methods:
                rows_M = stack(combined[name], V, row3)
                M = band_ends(rows_M, coef)
                Mw = ends(combined[name], V, row3, f=1.0)
                M_ref = ref_stack(cfg, name, mkf)
                ref_inc = M_ref if cfg is None else {e: M_ref[e] - ref_stack(cfg, "audit_rules_alone", mkf)[e]
                                                     for _, e in ENDS}
                payload[f"{arm}|{case}|{name}"] = payload_from_rows(rows_M)
                pts = refs = None
                if name in seeds_v:
                    pts = {e: [float(ends(s, V, row3)[e][0]) for s in seeds_v[name]] for _, e in ENDS}
                    refs = {e: [float(ref_ends(s, mkf)[e][0]) for s in pub_seeds[cfg][name]] for _, e in ENDS}
                lane = ends(lane_alone[name], V, row3) if cfg is not None else None
                for a, end in ENDS:
                    inc, arm_inc = M[end] - R2[end], M[end] - M_ref[end]
                    se, se_inc, se_arm = c.sdr(M[end]), c.sdr(inc), c.sdr(arm_inc)
                    total, total_inc, total_arm, nseeds = se, se_inc, se_arm, np.nan
                    if pts is not None:
                        total, total_inc = rubin(se, pts[end]), rubin(se_inc, pts[end])
                        total_arm = rubin(se_arm, [p - r for p, r in zip(pts[end], refs[end])])
                        nseeds = len(pts[end])
                    row = dict(head, allocation=a, band_end=end, method=name, change_bn=M[end][0], change_se_bn=se,
                               change_total_se_bn=total, whole_line_change_bn=Mw[end][0], increment_bn=inc[0],
                               increment_se_bn=se_inc, increment_total_se_bn=total_inc, seeds=nseeds,
                               arm_increment_bn=arm_inc[0], arm_increment_se_bn=se_arm,
                               arm_increment_total_se_bn=total_arm,
                               overlap_bn=np.nan if mkf else ref_inc[end][0] - inc[0])
                    if lane is not None:
                        row.update(lane_alone_bn=lane[end][0] - A0[end][0],
                                   interaction_bn=inc[0] - (lane[end][0] - A0[end][0]))
                    arm_rows.append(row)
    arm_out = pd.DataFrame(arm_rows)

    # Gate 3 (final): Node against the arithmetic for every stack.
    node = node_bands(payload, "onbooks_lane")
    key = out.share_type + "|" + out.case + "|" + out.method
    out["node_change_bn"] = [node.loc[k, "change_low_bn" if a == "shared" else "change_high_bn"]
                             for k, a in zip(key, out.allocation)]
    for name, br in alone_br.items():
        for a, end in ENDS:
            got = node.loc[f"alone|{name}", f"change_{end}_bn"]
            if abs(got - br[a]["non_ptc"][0]) > 1e-3:
                raise SystemExit(f"[BLOCKED] Node band differs for {name} alone ({a}): {got} vs {br[a]['non_ptc'][0]}")
    worst = (out.node_change_bn - out.change_bn).abs().max()
    print(f"[gate] Node band = component arithmetic at both ends (5d), max difference {worst:.1e} bn", flush=True)
    if worst > 1e-3:
        raise SystemExit("[BLOCKED] the Node band does not equal the component arithmetic (allocation order?)")
    arm_key = arm_out.arm + "|" + arm_out.case + "|" + arm_out.method
    arm_out["node_change_bn"] = [node.loc[k, f"change_{e}_bn"] if k in node.index else np.nan
                                 for k, e in zip(arm_key, arm_out.band_end)]
    checked = arm_out.node_change_bn.notna()
    worst = (arm_out.node_change_bn - arm_out.change_bn)[checked].abs().max()
    unchecked = arm_out[~checked]
    print(f"[gate] Node band = line-response arithmetic for {int(checked.sum())} of {len(arm_out)} step-5e stack ends "
          f"(unchecked: {len(unchecked)} key-fix rules rows, unchanged by the fix), max difference {worst:.1e} bn",
          flush=True)
    if worst > 1e-3 or not (unchecked.arm.eq("medicare_key_fix") & unchecked.method.eq("audit_rules_alone")).all():
        raise SystemExit("[BLOCKED] the Node band does not equal the line-response arithmetic")

    out.insert(0, "arm", "5d")
    columns = [*out.columns.drop("arm"), "arm", "arm_increment_bn", "arm_increment_se_bn",
               "arm_increment_total_se_bn", "overlap_bn"]
    result = pd.concat([out, arm_out], ignore_index=True)[columns]
    result.to_csv(c.OUT / "status_combination_onbooks_lane.csv", index=False)
    pd.DataFrame(line_rows).to_csv(c.OUT / "status_combination_onbooks_lane_row4_lines.csv", index=False)

    pd.set_option("display.width", 250)
    show = out[out.method.isin(["audit_rules_alone", "a_ipw_brief_cells", "b_hotdeck_union_matched",
                                "b_matched_over_pooled"])].copy()
    show["value"] = np.where(show.method.eq("audit_rules_alone"), show.change_bn, show.increment_bn)
    show["se"] = np.where(show.method.eq("audit_rules_alone"), show.change_se_bn, show.increment_total_se_bn)
    print(show.pivot_table(index=["share_type", "case", "allocation"], columns="method",
                           values=["value", "se"], sort=False).round(2).to_string(), flush=True)
    o = out[out.share_type.eq("origin")].set_index(["case", "allocation", "method"])
    u = out[out.share_type.eq("uniform")].set_index(["case", "allocation", "method"])
    diff = (o[["change_bn", "increment_bn"]] - u[["change_bn", "increment_bn"]]).abs().groupby("method").max()
    print("[check] origin-specific minus uniform-equivalent shares, largest absolute difference by method ($bn):",
          flush=True)
    print(diff.round(3).to_string(), flush=True)
    cols = ["arm", "case", "allocation", "method", "change_bn", "change_total_se_bn", "increment_bn",
            "increment_total_se_bn", "arm_increment_bn", "arm_increment_total_se_bn", "overlap_bn"]
    focus = arm_out[arm_out.method.isin(["arm_alone", "audit_rules_alone", "b_hotdeck_union_matched",
                                         "b_matched_over_pooled"]) & arm_out.case.isin(["none", "alone", "central"])]
    print(focus[cols].round(2).to_string(index=False), flush=True)
    lines = pd.DataFrame(line_rows)
    lines["group"] = np.where(lines.side.eq("receipts"), "receipts",
                              np.where(lines.source.ne("lane CPS key"), lines.source,
                                       lines.line.map(lambda i: lines_by_id.get(i, {}).get("response_class", ""))))
    print(lines.groupby(["arm", "band_end", "group"]).band_change_bn.sum().round(2).to_string(), flush=True)
    print(json.dumps(arm_info), flush=True)


if __name__ == "__main__":
    main()
