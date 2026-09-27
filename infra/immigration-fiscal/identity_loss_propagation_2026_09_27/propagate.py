#!/usr/bin/env python3
"""Propagate the per-generation identity loss (civic_trajectory_mexican_2026_09_27,
`derived/identity_loss.csv`) to the two consumers of the fourth-plus identification rate:

1. `mexican_origin_population_total_2026_09_19`, arm 3 (`bounds_coverage_fiscal.py`): the
   corrected third-plus count and the union (ladder 158; 42.78M central, x1.0525 PES = 45.0M).
2. `lineage_cost_2026_09_19` (`inputs.attrition()` -> `lineage.g3plus_profile`): the G4+
   attrition-corrected mixed profile (ladder 159; arm 2a) and, by the same machinery, the
   sponsored-parent lane (ladder 241). Since 2026-09-28 arm 2a and the population lane's
   arm 5 carry the measured generation split (only G3-rate losses close any of the gap), with
   the Duncan-Trejo years convention kept as a sensitivity.

Both upstream lanes are imported read-only. The population lane's `main()` is executed
unmodified with its output directory pointed at `_cache/` here and, for an arm, one module
constant (`DT_4TH_PLUS_ID`, its third bound row) replaced by the arm's effective fourth-plus
rate. The lineage lane's `lineage()` loop is copied below with one change (the attriter share
is looked up by generation); `verify.py` proves the copy equals the original bit for bit when
the schedule is flat.

Run from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/identity_loss_propagation_2026_09_27/propagate.py
"""
from __future__ import annotations

import csv
import filecmp
import importlib.util
import json
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # imports must not leave __pycache__ in upstream lanes

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
POP_DIR = FISCAL / "mexican_origin_population_total_2026_09_19"
LIN_DIR = FISCAL / "lineage_cost_2026_09_19"
IDLOSS = FISCAL / "civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv"

sys.path.insert(0, str(LIN_DIR))
import inputs as I  # noqa: E402
import lineage as L  # noqa: E402

_spec = importlib.util.spec_from_file_location("bcf", POP_DIR / "bounds_coverage_fiscal.py")
BCF = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(BCF)

PES = 1.0525            # arm4 scheme B multiplier; the memo's 45.0M = central x this
# Lineage centrals, 0% and 3%, after audit §E (2026-09-28; the brief's were -1,297,150 / -514,635)
LIN_CENTRAL = (-1288162.0, -513398.0)
RHOS = (0.25, 0.5, 0.75)                # [ASSUMPTION] geometric generation mix of the 4th+ pool
RHO_CENTRAL = 0.5
POP_OUTPUTS = ("arm3_correction_bounds.csv", "arm3_fractional_counting.csv",
               "arm4_coverage_grid.csv", "arm5_fiscal_implication.csv",
               "arm5_education_selectivity.csv", "arm5_generation_split.csv")
# Population lane arm-5 rows: the measured generation split (central since 2026-09-28) and the
# Duncan-Trejo years convention (sensitivity).
SPLIT_ROW = "generation split, measured: G3-rate attriters close C3 0.7758"
DT_ROW = "Duncan-Trejo"
BCF_READS = ("arm3_multiplier.csv", "arm3_grandparent_counts.csv")


# ------------------------------------------------------------------ identity loss
def losses() -> dict:
    """Child-stage loss for children of self-identified G3+ parents (three couple types) and
    of G2 parents, both measures."""
    d = pd.read_csv(IDLOSS)
    d = d[d.adjustment.str.startswith("three couple types")]
    out = {}
    for meas, key in (("child-stage loss: not reported mexican", "mex"),
                      ("child-stage loss: not reported hispanic", "hisp")):
        for gen in ("mex_G2", "mex_G3plus"):
            r = d[(d.measure == meas) & (d.generation == gen)]
            if len(r) != 1:
                raise SystemExit(f"[BLOCKED] identity_loss row not unique: {meas}/{gen}")
            out[f"{key}_{gen}"] = float(r.iloc[0].estimate)
            out[f"{key}_{gen}_se"] = float(r.iloc[0].se)
    return out


def pop_p3() -> float:
    m = pd.read_csv(POP_DIR / "derived/arm3_multiplier.csv")
    q = dict(zip(m["quantity"], m["children"]))
    a_b = q["A and B: 3rd-generation identifiers"]
    return a_b / (a_b + q["B not A: 3rd-generation attriters (recoverable)"])


def schedules(p3: float, lo: dict) -> dict:
    """Cumulative identification rate r_g for generation g >= 4, given r_3 = p3.

    kind 'flat': r_4 = r_5 = ... = base * (1 - step) ** n_steps (n_steps 0 or 1).
    kind 'compound': r_g = base * (1 - step) ** (g - 3).
    """
    calib = (1.0 - p3) / lo["mex_mex_G2"]   # measured G3 loss / synthetic G2-parent step
    return {
        "a_current": {"kind": "flat", "step": 0.0,
                      "label": "(a) current: G4+ at the measured G3 rate"},
        "b_one_step": {"kind": "flat", "step": lo["mex_mex_G3plus"],
                       "label": "(b) one more step on 'not reported Mexican', held for G5+"},
        "c_compound": {"kind": "compound", "step": lo["mex_mex_G3plus"],
                       "label": "(c) G3+ parents' 'not Mexican' loss compounded each generation"},
        "d_compound_hisp": {"kind": "compound", "step": lo["hisp_mex_G3plus"],
                            "label": "(d) 'not reported Hispanic' loss compounded each generation"},
        "e_compound_calibrated": {"kind": "compound", "step": lo["mex_mex_G3plus"] * calib,
                                  "calib": calib,
                                  "label": "(e) (c) with the step scaled by measured G3 loss / "
                                           "synthetic G2-parent step"},
    }


def rate(s: dict, base: float, gen: int) -> float:
    if gen <= 3:
        return base
    if s["kind"] == "flat":
        return base * (1.0 - s["step"])
    return base * (1.0 - s["step"]) ** (gen - 3)


def p_eff(s: dict, base: float, rho: float) -> float:
    """Mean identification rate of the true 4th-plus pool when its persons fall across
    G4, G5, ... in shares (1 - rho) rho^k. Closed form of sum_k (1-rho) rho^k r_{4+k}."""
    r4 = rate(s, base, 4)
    if s["kind"] == "flat":
        return r4
    return r4 * (1.0 - rho) / (1.0 - rho * (1.0 - s["step"]))


# ------------------------------------------------------------------ population lane
def run_population(tag: str, p4: float | None) -> Path:
    """Execute bounds_coverage_fiscal.main() into _cache/pop_<tag>/. With p4 set, its third
    bound row (Duncan-Trejo 70.8%) carries p4 instead; every other row is unchanged."""
    d = CACHE / f"pop_{tag}"
    d.mkdir(parents=True, exist_ok=True)
    for f in BCF_READS:
        shutil.copyfile(POP_DIR / "derived" / f, d / f)
    BCF.DERIVED = d
    BCF.DT_4TH_PLUS_ID = 0.708 if p4 is None else p4
    rc = BCF.main()
    if rc != 0:
        raise SystemExit(f"[BLOCKED] bounds_coverage_fiscal.main() returned {rc} ({tag})")
    BCF.DT_4TH_PLUS_ID = 0.708
    return d


# ------------------------------------------------------------------ lineage lane
def lineage(profiles, tables, cfg) -> dict:
    """Copy of lineage_cost_2026_09_19/lineage.py::lineage. Changes: G3+ descendants take
    `cfg['attr_for'](gen)` when present (else `cfg['attr']`), and the mixed profile starts at
    `cfg.get('mix_from_gen', 4)`. verify.py checks equality with L.lineage on a flat schedule."""
    alloc, acct = cfg["allocation"], cfg["account"]
    tfr, attribution, gen_len = cfg["tfr"], cfg["attribution"], cfg["gen_len"]
    crime = cfg["crime"]
    mort = cfg["mortality"]
    mix_from = cfg.get("mix_from_gen", 4)
    attr_for = cfg.get("attr_for", lambda gen: cfg["attr"])

    if cfg["reference"]:
        prof_founder = I.age_vector(profiles, "third_plus_nh_white", acct, alloc)
        table_f = tables[mort["white"]]
        cr_f = crime["white"]
    else:
        barred = cfg.get("senior_barred")
        prof_founder, _ = L.founder_profile(profiles, alloc, acct, cfg["founder_status"],
                                            cfg["senior_rule"], cfg["penalty"],
                                            cfg.get("legalise_year"),
                                            barred[(alloc, acct)] if barred else None,
                                            cfg.get("senior_addback"))
        table_f = tables[mort["mexican"]]
        cr_f = crime["founder"]

    FSA = L.FOUNDER_START_AGE
    out = {}
    f, cs = L.person_stream(prof_founder, table_f, -FSA, FSA, cr_f["social"])
    _, ct = L.person_stream(prof_founder, table_f, -FSA, FSA, cr_f["tangible"])
    _, cn = L.person_stream(prof_founder, table_f, -FSA, FSA, cr_f["social"] - cr_f["corrections"])
    out["G1"] = (1.0, f, cs, ct, cn, -FSA)

    n = 1.0
    birth = gen_len - FSA
    parent_group = "third_plus_nh_white" if cfg["reference"] else "mexico_born"
    parent_table, parent_age = table_f, FSA   # births need a living parent (audit §E)
    gen = 2
    while birth <= L.HORIZON:
        lx = parent_table.lx.to_numpy()
        n *= L.multiplier(tfr[parent_group], attribution) * float(lx[gen_len] / lx[parent_age])
        if cfg["reference"]:
            prof = I.age_vector(profiles, "third_plus_nh_white", acct, alloc)
            table = tables[mort["white"]]
            cr = crime["white"]
            group = "third_plus_nh_white"
        else:
            if gen == 2:
                group = "mexican_second_gen"
                prof = I.age_vector(profiles, group, acct, alloc)
            else:
                group = "mexican_third_plus_selfid"
                conv = cfg["convergence"] if gen >= mix_from else "selfid"
                prof = L.g3plus_profile(profiles, alloc, acct, conv, attr_for(gen))
            table = tables[mort["mexican"]]
            cr = crime["descendant"]
        f, cs = L.person_stream(prof, table, birth, 0, cr["social"])
        _, ct = L.person_stream(prof, table, birth, 0, cr["tangible"])
        _, cn = L.person_stream(prof, table, birth, 0, cr["social"] - cr["corrections"])
        out[f"G{gen}"] = (n, n * f, n * cs, n * ct, n * cn, birth)
        parent_group = group
        parent_table, parent_age = table, 0
        birth += gen_len
        gen += 1
    return out


class Lin:
    """The lineage lane's main() inputs and its `run()` gap, rebuilt read-only."""

    def __init__(self):
        self.profiles = I.age_profiles()
        self.tables = I.survival()
        self.fert = I.fertility()
        self.pen = I.unauthorized_penalty()["penalty_per_adult_year"]
        crime = I.crime_rates()
        self.crime = {"founder": crime["A1_bjs_stock"]["mexican"],
                      "descendant": crime["A1_bjs_stock"]["mexican"],
                      "white": crime["A1_bjs_stock"]["white"]}
        self.attr = I.attrition()
        self.attr_years = I.attrition("years_convention")
        comps = I.age_components()
        barred = {(al, "expanded"): I.component_vector(comps, self.profiles, "mexico_born",
                                                       "expanded", al, I.STATUTORY_BARRED)
                  for al in ("personal", "shared")}
        self.statutory = {"senior_rule": "senior_statutory", "senior_barred": barred}
        vec, _ = I.senior_addback("rules_2026_new_enrollee", "central")
        self.priced_2026 = {**self.statutory, "senior_addback": vec}

    def cfg(self, **over) -> dict:
        base = {"allocation": "personal", "account": "expanded", "gen_len": L.GEN_LEN,
                "attribution": "per_capita", "founder_status": "unauthorized",
                "senior_rule": "senior_full", "convergence": "selfid",
                "mortality": {"mexican": "total", "white": "total"},
                "penalty": self.pen, "attr": self.attr, "reference": False,
                "crime": self.crime, "tfr": self.fert["low_cps2025"]}
        return {**base, **over}

    def gap(self, over: dict, rate: float, fn=None) -> tuple[float, dict]:
        fn = fn or lineage
        cfg = self.cfg(**over)
        mex_L = fn(self.profiles, self.tables, cfg)
        mex = L.summarise(mex_L, rate, 0.0)
        wht = L.summarise(fn(self.profiles, self.tables, {**cfg, "reference": True}), rate, 0.0)
        return mex["lineage_fiscal"] - wht["lineage_fiscal"], mex_L

    def attr_for(self, sched: dict, attr: dict | None = None):
        """Per-generation attrition inputs: the schedule sets the attriter share; under the
        generation split only its G3-rate part closes any of the gap."""
        attr = attr or self.attr
        base = attr["fourth_plus_identification_rate"]
        return lambda gen: {**attr, "attriter_share": 1.0 - rate(sched, base, gen)}


LIN_ARMS = {
    # name in sensitivities.csv (None: not a stored row) -> overrides
    "central, 0%": ("central (personal/expanded, unauthorized, per-capita, low fertility, 0%)", {}, 0.0),
    "central, 3%": ("central at 3%", {}, 0.03),
    "2a G4+ attrition-corrected mixed profile, 0%":
        ("2a G4+ attrition-corrected mixed profile", {"convergence": "attrition_mixed"}, 0.0),
    "2a G4+ attrition-corrected mixed profile, 3%": (None, {"convergence": "attrition_mixed"}, 0.03),
    "2b legalised year 10, 0%": ("2b founder legalised at year 10", {"legalise_year": 10}, 0.0),
    "2b legalised year 10, 3%": (None, {"legalise_year": 10}, 0.03),
    "never legalised, statutory bars, 0%":
        ("senior rule: statutory bars from 65 (no cash transfers, public medical, institutional "
         "care or noncash aid; taxes and services kept)", "statutory", 0.0),
    "never legalised, statutory + priced 2026 central, 0%":
        ("senior rule: statutory bars plus priced care, rules_2026_new_enrollee, central",
         "priced_2026", 0.0),
    "2a x 2b: mixed profile, legalised year 10, 0%":
        (None, {"convergence": "attrition_mixed", "legalise_year": 10}, 0.0),
    "supplementary: mixed profile from G3, 0%":
        (None, {"convergence": "attrition_mixed", "mix_from_gen": 3}, 0.0),
    # 2026-09-28: row 2a above is the generation split; the years convention is a sensitivity
    "2a years convention (sensitivity), 0%":
        ("2a G4+ mixed profile, years convention (every attriter keeps 0.2756 of the self-ID gap)",
         "years", 0.0),
    "2a years convention (sensitivity), 3%": (None, "years", 0.03),
}


def lin_over(lin: Lin, over) -> dict:
    if over == "statutory":
        return dict(lin.statutory)
    if over == "priced_2026":
        return dict(lin.priced_2026)
    if over == "years":
        return {"convergence": "attrition_mixed", "attr": lin.attr_years}
    return dict(over)


# ------------------------------------------------------------------ main
def main() -> int:
    CACHE.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    lo = losses()
    p3 = pop_p3()
    S = schedules(p3, lo)

    # ---- population: reproduce first
    ref = run_population("reproduce", None)
    for f in POP_OUTPUTS:
        if not filecmp.cmp(ref / f, POP_DIR / "derived" / f, shallow=False):
            raise SystemExit(f"[BLOCKED] population lane does not reproduce {f}")
    print(f"[reproduce] population lane: {len(POP_OUTPUTS)} outputs byte-identical", flush=True)
    b0 = pd.read_csv(ref / "arm3_correction_bounds.csv")
    f0 = pd.read_csv(ref / "arm5_fiscal_implication.csv")
    g0 = pd.read_csv(ref / "arm5_generation_split.csv")
    old = b0.iloc[1]                     # "4th-plus identifies at the measured 3rd-generation rate"
    if not old.assumption.startswith("4th-plus identifies at the measured"):
        raise SystemExit("[BLOCKED] arm 3 central row moved")

    def arm5_rows(f: pd.DataFrame, g: pd.DataFrame, assumption: str):
        """The bound's Duncan-Trejo row, its central generation-split row and that row's split."""
        dt = f[(f.population_assumption == assumption) & f.attriter_characteristics.str.startswith(DT_ROW)]
        sp = f[(f.population_assumption == assumption) & f.attriter_characteristics.str.startswith(SPLIT_ROW)]
        gs = g[(g.population_assumption == assumption) & g.c3_source.str.endswith("(central)")]
        if not len(dt) == len(sp) == len(gs) == 1:
            raise SystemExit(f"[BLOCKED] arm 5 rows not unique for {assumption}")
        return dt.iloc[0], sp.iloc[0], gs.iloc[0]

    old_f5, old_s5, old_g5 = arm5_rows(f0, g0, old.assumption)

    rows, pop_detail, sched_rows = [], [], []
    runs: dict[float, pd.Series] = {}
    for key, s in S.items():
        rhos = (RHO_CENTRAL,) if s["kind"] == "flat" else RHOS
        for rho in rhos:
            pe = p_eff(s, p3, rho)
            if key == "a_current":
                b_row = old
                f5, s5, g5 = old_f5, old_s5, old_g5
            else:
                tag = f"{key}_rho{rho}"
                d = run_population(tag, pe)
                bb = pd.read_csv(d / "arm3_correction_bounds.csv")
                ff = pd.read_csv(d / "arm5_fiscal_implication.csv")
                # rows 0,1,3 must be untouched by the substitution
                for i in (0, 1, 3):
                    if not bb.iloc[i].equals(b0.iloc[i]):
                        raise SystemExit(f"[BLOCKED] substitution leaked into bound row {i}")
                b_row = bb.iloc[2]
                if abs(b_row.fourth_plus_identification_rate - round(pe, 4)) > 1e-12:
                    raise SystemExit("[BLOCKED] substituted rate not carried")
                f5, s5, g5 = arm5_rows(ff, pd.read_csv(d / "arm5_generation_split.csv"), b_row.assumption)
            union = float(b_row.corrected_union)
            corr = float(b_row.corrected_third_plus)
            rec = {"arm": key, "rho": rho, "p_eff_fourth_plus": pe,
                   "corrected_third_plus_M": corr / 1e6, "union_M": union / 1e6,
                   "union_pes_M": union * PES / 1e6,
                   "added_M": float(b_row.added) / 1e6,
                   "hidden_share_of_third_plus": float(b_row.added) / corr,
                   "hidden_share_of_union": float(b_row.added) / union,
                   "gap_per_person_after": float(f5.gap_per_person_after),
                   "aggregate_gap_bn_after": float(f5.aggregate_gap_bn_after),
                   "g3_rate_attriters_M": float(g5.g3_rate_attriters) / 1e6,
                   "later_loss_attriters_M": float(g5.later_loss_attriters) / 1e6,
                   "gap_per_person_after_split": float(s5.gap_per_person_after),
                   "aggregate_gap_bn_after_split": float(s5.aggregate_gap_bn_after)}
            pop_detail.append(rec)
            if rho == RHO_CENTRAL:
                for metric, o, n in (
                        ("union_M", old.corrected_union / 1e6, rec["union_M"]),
                        ("union_pes_M (memo upper 45.0M)", old.corrected_union * PES / 1e6,
                         rec["union_pes_M"]),
                        ("added_M", old.added / 1e6, rec["added_M"]),
                        ("hidden_share_of_third_plus", old.added / old.corrected_third_plus,
                         rec["hidden_share_of_third_plus"]),
                        ("gap_per_person_after (DT selectivity)", old_f5.gap_per_person_after,
                         rec["gap_per_person_after"]),
                        ("aggregate_gap_bn_after (DT selectivity)", old_f5.aggregate_gap_bn_after,
                         rec["aggregate_gap_bn_after"]),
                        ("gap_per_person_after (generation split, C3 0.7758)",
                         old_s5.gap_per_person_after, rec["gap_per_person_after_split"]),
                        ("aggregate_gap_bn_after (generation split, C3 0.7758)",
                         old_s5.aggregate_gap_bn_after, rec["aggregate_gap_bn_after_split"])):
                    rows.append({"arm": key, "consumer": "population_total_arm3", "metric": metric,
                                 "old": float(o), "new": float(n), "delta": float(n) - float(o)})
        print(f"[population] {key:<22} " + "  ".join(
            f"rho {r['rho']}: {r['union_M']:.3f}M" for r in pop_detail if r["arm"] == key), flush=True)

    # ---- lineage: reproduce first
    lin = Lin()
    stored = pd.read_csv(LIN_DIR / "derived/sensitivities.csv").set_index("sensitivity")
    base_rate = lin.attr["fourth_plus_identification_rate"]
    for (name, (srow, over, r)) in LIN_ARMS.items():
        if srow is None:
            continue
        mine, _ = lin.gap(lin_over(lin, over), r, fn=L.lineage)
        want = float(stored.loc[srow, "gap_lineage_fiscal"])
        if abs(mine - want) > 1e-6:
            raise SystemExit(f"[BLOCKED] lineage lane does not reproduce {name}: {mine} vs {want}")
    c0, _ = lin.gap({}, 0.0, fn=L.lineage)
    c3, _ = lin.gap({}, 0.03, fn=L.lineage)
    if round(c0) != LIN_CENTRAL[0] or round(c3) != LIN_CENTRAL[1]:
        raise SystemExit(f"[BLOCKED] lineage centrals {c0}, {c3} differ from the brief")
    print(f"[reproduce] lineage central {c0:,.6f} / {c3:,.6f}; stored rows to 1e-6", flush=True)

    # poison test: on the selfid path the attrition dict is never read
    poison = {k: float("nan") for k in lin.attr}
    pc, _ = lin.gap({"attr": poison}, 0.0, fn=L.lineage)
    if pc != c0:
        raise SystemExit("[BLOCKED] selfid path reads the attrition inputs")

    lin_detail = []
    for key, s in S.items():
        for g in range(3, 9):
            sched_rows.append({"arm": key, "generation": g, "identification_pop": rate(s, p3, g),
                               "identification_lineage": rate(s, base_rate, g)})
        for name, (srow, over, r) in LIN_ARMS.items():
            o = lin_over(lin, over)
            # the supplementary row has no upstream twin: its baseline is this copy, flat schedule
            old_gap, _ = lin.gap(o, r, fn=lineage if "mix_from_gen" in o else L.lineage)
            new_gap, LL = lin.gap({**o, "attr_for": lin.attr_for(s, o.get("attr"))}, r)
            persons = sum(v[0] for v in LL.values())
            lin_detail.append({"arm": key, "lineage_row": name, "old_gap": old_gap,
                               "new_gap": new_gap, "delta": new_gap - old_gap,
                               "delta_pct_of_old": (new_gap - old_gap) / abs(old_gap) * 100,
                               "mex_persons": persons})
            rows.append({"arm": key, "consumer": "lineage_cost", "metric": f"gap_usd: {name}",
                         "old": old_gap, "new": new_gap, "delta": new_gap - old_gap})
        print(f"[lineage] {key:<22} 2a 0%: " + ", ".join(
            f"{d['old_gap']:,.0f} -> {d['new_gap']:,.0f}" for d in lin_detail
            if d["arm"] == key and d["lineage_row"].startswith("2a G4+") and d["lineage_row"].endswith("0%")),
            flush=True)

    # ---- sponsored-parent lane (entry 241): its Ctx.cfg pins convergence 'selfid'
    spon_src = (FISCAL / "lineage_sponsored_parents_2026_09_27/common.py").read_text()
    spon_arms = (FISCAL / "lineage_sponsored_parents_2026_09_27/arms.py").read_text()
    spon_selfid = '"convergence": "selfid"' in spon_src and "convergence" not in spon_arms
    if not spon_selfid:
        raise SystemExit("[BLOCKED] sponsored-parent lane may leave the selfid path; re-run it")
    for key in S:
        rows.append({"arm": key, "consumer": "lineage_sponsored_parents (entry 241)",
                     "metric": "every arm (selfid path; attrition inputs unread)",
                     "old": 0.0, "new": 0.0, "delta": 0.0})

    def w(path: Path, recs: list[dict]):
        with path.open("w", newline="") as fh:
            wr = csv.DictWriter(fh, fieldnames=list(recs[0]), lineterminator="\n")
            wr.writeheader()
            for r in recs:
                # float() first: repr of a numpy float64 would write "np.float64(...)"
                wr.writerow({k: (repr(float(v)) if isinstance(v, float) else v) for k, v in r.items()})

    w(OUT / "arms.csv", rows)
    w(OUT / "population_arms.csv", pop_detail)
    w(OUT / "lineage_arms.csv", lin_detail)
    w(OUT / "schedules.csv", sched_rows)
    meta = {"p3_population_unrounded": p3, "p3_lineage_input": base_rate, "losses": lo,
            "arms": {k: {kk: vv for kk, vv in v.items()} for k, v in S.items()},
            "rho_central": RHO_CENTRAL, "rhos": list(RHOS), "pes_multiplier": PES,
            "lineage_attrition": {"central": lin.attr, "years_convention": lin.attr_years},
            "checks": {"population_outputs_byte_identical": True,
                       "lineage_central": [c0, c3],
                       "poison_attr_selfid_unchanged": True,
                       "sponsored_lane_pins_selfid": spon_selfid}}
    (OUT / "audit.json").write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
    print("[written] derived/arms.csv population_arms.csv lineage_arms.csv schedules.csv audit.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
