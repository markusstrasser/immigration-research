"""The pension lane's accrual on the 2026 Trustees Reports' payable paths (lane pension_tr2026_2026_10_06).

Question (team-lead brief, 2026-10-06): the pension lane (pension_accrual_2026_09_28, central since 9ea1beb, the
commit the main case pins) values the Social Security (OASDI) and Medicare Part A promises the group's 2024 work
earns at payable benefits, from SSA Actuarial Note 2025.7 and the 2025 Trustees Reports. The 2026 reports project
lower payable benefits. How much does moving the payable path to the 2026 reports change the accrual?

Steps (a failed gate stops with [BLOCKED] before anything is written to derived/):
  1. Paths: the share of scheduled benefits payable by year, from each report's tables.
     OASDI: payroll tax / (cost - taxation of benefits), Tables IV.B1 and IV.B2 (intermediate, % of taxable payroll),
     since the income from taxing benefits falls with the cut. In the depletion year it is (reserves at the start of
     the year + payroll tax) / (cost - taxation of benefits), from the trust fund ratio table (TR 2026 Table IV.B5,
     TR 2025 Table IV.B4). Values fall linearly between the table's years, are 1 before depletion and flat after 2100.
     HI: non-interest income / cost from Table III.B7, and in the depletion year the start-of-year assets
     (Table III.B6) plus income / cost, capped at 1, with the same interpolation.
     Gates: each path reproduces every payable share its report (and, for 2025, Note 2025.7) prints, within the
     rounding of the table entries it is computed from. Table IV.B3 (% of GDP) gives income / cost only, which does
     not reproduce the printed shares; it is a cross-check on Table IV.B1.
  2. Positive control: the pension lane's central through its own code, imported read-only with nothing written
     beside it. The control computes the model grid only at the central's (rate, mortality) run and Note 2025.7's
     basis, which is all the central reads. It must reproduce, from the lane's derived files: the OASDI accrual per
     tax dollar for the union and each generation, the future benefit-tax shares, ratio_net, every row of
     hi_arms.csv, the case on accrual at both ends, and the model's payable haircut on Note 2025.7's cells.
  3. Arms: the OASDI accrual is Note 2025.7 Table 3 (payable, on the 2025 path) times the lifetime model's factor
     k(person) / mwr(Note 2025.7's basis). A new path enters the factor's numerator, while the denominator stays on
     the 2025 path that Table 3 carries. So the published level moves by the model's ratio of the two paths, and the
     arm equals the central when the paths are equal. Swapping the path in both, as `payable_path` alone would, cancels
     in the ratio. Part A reads its path directly. The timing of the benefit tax follows each arm's OASDI path.
       control         the lane's own paths (Note 2025.7's three anchors, the Medicare TR 2025's three)
       tables_2025     both 2025 paths year by year from the 2025 tables: the construction check
       tr2026          both 2026 paths year by year from the 2026 tables (the headline arm; ungated against a 2026
                       money's-worth note, which SSA has not published: the Note 7 index ends at 2025.7)
       tr2026_oasdi    the 2026 OASDI path, Part A on the 2025 tables (a part of tr2026)
       tr2026_hi       Part A on the 2026 path, OASDI on the 2025 tables (the other part)
       anchors_2026    the 2026 paths in the lane's own form (three anchors, linear between)
  4. Beside. The trust funds kept separate, as current law has them (the combined reading "implicitly assumes that the
     law will have been changed to permit the transfer of funds between OASI and DI"): OASI's payable share on OASI's
     cost and DI's full benefits on DI's, weighted by cost, on each report (separate_funds_2025 against tables_2025,
     separate_funds against tr2026). Then 2026 changes the swap does not apply, each on top of tr2026: the 2026
     report's tax-on-benefits path; its new-issue interest rates; Note
     2026.3's wage index (AWI) path; Table V.C1's COLAs and contribution bases; its mortality decline rates; its HI
     cost per beneficiary; and the last six together, on the combined and the separate reading (all_2026_inputs,
     all_2026_inputs_separate_funds). Not read: Note 2026.3's scaled factors (the
     preliminary factors 0.22% lower over a career, the four adjustments 0.1-0.2% higher; the final sets move by under
     0.1%).
Outputs: derived/paths.csv, path_points.csv, path_gates.csv, haircut_check.csv, arms.csv, case_beside.csv,
summary.json (read by case_tr2026.cjs).

Run from the repository root (about a minute):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/pension_tr2026_2026_10_06/pension_tr2026.py
"""
from __future__ import annotations

import json
import sys
from contextlib import contextmanager
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
sys.path.insert(0, str(HERE))
import sources_tr2026 as T  # noqa: E402  (puts the pension lane on sys.path)
import pension_accrual as PA  # noqa: E402  the pension lane, read-only
L, S, ss = PA.L, PA.S, PA.ss

PENSION_DERIVED = PA.OUT
G = (PA.CENTRAL["rate"], PA.CENTRAL["mortality"])     # the central's model run: new-issue rates, general mortality
BASE = PA.BASE                                         # Note 2025.7's own basis: trust-fund rates, general mortality
GROUPS = ["union", "G1", "G2", "G3plus"]
YEARS = np.arange(L.Y0, L.Y1 + 1)
BT_MAPPING = PA.BT_CENTRAL["bt_mapping"]
# the payable shares each path must reproduce: (path, label, year, stated value, its rounding half-width)
PUBLISHED = [
    ("oasdi_2025", "Note 2025.7 p. 2 (reserves at the start of 2034 plus income)", 2034, 0.902, 0.0005),
    ("oasdi_2025", "Note 2025.7 p. 2", 2035, 0.807, 0.0005),
    ("oasdi_2025", "Note 2025.7 p. 2", 2099, 0.719, 0.0005),
    ("oasdi_2025", "TR 2025 sec. II.D, the rest of 2034 after depletion", "2034_after", 0.81, 0.005),
    ("oasdi_2025", "TR 2025 sec. II.D", 2099, 0.72, 0.005),
    ("oasdi_2026", "TR 2026 sec. II.D and Table IV.B5, the rest of 2034 after depletion", "2034_after", 0.83, 0.005),
    ("oasdi_2026", "TR 2026 sec. II.D and Table IV.B5", 2100, 0.65, 0.005),
    ("oasi_2025", "TR 2025 sec. II.D and Table IV.B4, the rest of 2033 after depletion", "2033_after", 0.77, 0.005),
    ("oasi_2026", "TR 2026 sec. II.D and Table IV.B5, the rest of 2032 after depletion", "2032_after", 0.78, 0.005),
    ("oasi_2026", "TR 2026 sec. II.D and Table IV.B5", 2100, 0.62, 0.005),
    ("hi_2025", "Medicare TR 2025 sec. II (income / cost, the year of depletion)", "2033_after", 0.89, 0.005),
    ("hi_2025", "Medicare TR 2025 sec. II", 2049, 0.86, 0.005),
    ("hi_2025", "Medicare TR 2025 sec. II (about 100 percent)", 2099, 1.00, 0.005),
    ("hi_2026", "Medicare TR 2026 sec. II.E (income / cost, the year of depletion)", "2033_after", 0.89, 0.005),
    ("hi_2026", "Medicare TR 2026 sec. II.E", 2050, 0.85, 0.005),
    ("hi_2026", "Medicare TR 2026 sec. II.E (about 93 percent)", 2100, 0.93, 0.005),
]


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


@contextmanager
def patched(obj, name, value):
    """Replace a module attribute for the duration (an in-memory substitution; no file of the other lane changes)."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


# ------------------------------------------------------------------ 1. paths
def on_index(points: dict) -> np.ndarray:
    """A path on lifetime_model's year index: 1 before the first point, linear between points, flat after the last."""
    s = pd.Series(points).sort_index()
    out = np.interp(YEARS, s.index.to_numpy(float), s.to_numpy(float))
    out[YEARS < s.index.min()] = 1.0
    return out


def oasdi_points(doc: str, fund: str = "oasdi") -> tuple[dict, dict]:
    """A fund's payable share at its table's years from depletion on, with its inputs and the interval their rounding
    allows (rates to 0.005 of payroll, the trust fund ratio to 0.5 percent): `after` is the share once the reserves
    are gone, `share` the year's (in the depletion year, reserves at its start plus income)."""
    r = T.oasdi_rates(doc).set_index("year")
    tfr = T.trust_fund_ratios(doc).set_index("year")[fund]
    if not tfr.isna().any() or not tfr.loc[tfr.index[tfr.isna()].min():].isna().all():
        blocked(f"{doc} {fund}: the reserves are not depleted for good within the table")
    dep = int(tfr.index[tfr.isna()].min()) - 1
    if dep not in tfr.index or not tfr[dep] > 0:
        blocked(f"{doc} {fund}: no reserve ratio at the start of the depletion year {dep}")
    P, C, X = r[f"{fund}_payroll"], r[f"{fund}_cost"], r[f"{fund}_tob"]
    info = {}
    for y in r.index[r.index >= dep]:
        after = P[y] / (C[y] - X[y])
        lo, hi = (P[y] - 0.005) / (C[y] + 0.005 - (X[y] - 0.005)), (P[y] + 0.005) / (C[y] - 0.005 - (X[y] + 0.005))
        rec = dict(kind="table", payroll=P[y], cost=C[y], tob=X[y], after=after, after_lo=lo, after_hi=hi,
                   share=min(1.0, after), share_lo=min(1.0, lo), share_hi=min(1.0, hi))
        if y == dep:
            f = tfr[y] / 100
            rec.update(kind="depletion_year", trust_fund_ratio=tfr[y], share=min(1.0, (f * C[y] + P[y]) / (C[y] - X[y])),
                       share_lo=min(1.0, ((f - 0.005) * (C[y] + 0.005) + P[y] - 0.005) / (C[y] + 0.005 - (X[y] - 0.005))),
                       share_hi=min(1.0, ((f + 0.005) * (C[y] - 0.005) + P[y] + 0.005) / (C[y] - 0.005 - (X[y] + 0.005))))
        info[int(y)] = rec
    return {y: v["share"] for y, v in info.items()}, dict(depletion_year=dep, points=info)


def hi_points(doc: str) -> tuple[dict, dict]:
    """HI's covered share at its table's years from depletion on: non-interest income / cost, and in the depletion
    year (the last year Table III.B6 shows assets) the start-of-year assets plus that, capped at 1; with the interval
    the rounding of the entries allows (rates to 0.005, the asset ratio to 0.5 percent)."""
    r = T.hi_rates(doc).set_index("year")
    a = T.hi_asset_ratios(doc)
    dep = int(a.index.max())
    if dep not in r.index:
        blocked(f"{doc}: the depletion year {dep} is not in Table III.B7")
    info = {}
    for y in r.index[r.index >= dep]:
        I, C = r.income[y], r.cost[y]
        after, lo, hi = I / C, (I - 0.005) / (C + 0.005), (I + 0.005) / (C - 0.005)
        rec = dict(kind="table", income=I, cost=C, after=after, after_lo=lo, after_hi=hi,
                   share=min(1.0, after), share_lo=min(1.0, lo), share_hi=min(1.0, hi))
        if y == dep:
            rec.update(kind="depletion_year", asset_ratio=a[y], share=min(1.0, a[y] / 100 + after),
                       share_lo=min(1.0, (a[y] - 0.5) / 100 + lo), share_hi=min(1.0, (a[y] + 0.5) / 100 + hi))
        info[int(y)] = rec
    return {y: v["share"] for y, v in info.items()}, dict(depletion_year=dep, points=info)


def separate_points(doc: str, oasi: dict) -> dict:
    """OASDI's payable share with the trust funds kept separate, as current law has them: OASI's share on OASI's
    scheduled cost and full benefits on DI's, weighted by each fund's cost in the year (Tables IV.B1 and IV.B2). Both
    reports project DI's reserves positive to the end of their projection (QUOTES; the trust fund ratio table shows no
    depletion). The combined reading, the reports' headline and Note 2025.7's, assumes a law permitting transfers."""
    if T.trust_fund_ratios(doc).di.isna().any():
        blocked(f"{doc}: DI's reserves are depleted within the table")
    r = T.oasdi_rates(doc).set_index("year")
    return {y: float((r.oasi_cost[y] * s + (r.oasdi_cost[y] - r.oasi_cost[y])) / r.oasdi_cost[y]) for y, s in oasi.items()}


def build_paths(econ) -> tuple[dict, dict]:
    """Every path on the year index, and the points and inputs behind the table-built ones."""
    o25, i_o25 = oasdi_points("tr2025")
    o26, i_o26 = oasdi_points("tr2026")
    a25, i_a25 = oasdi_points("tr2025", "oasi")
    a26, i_a26 = oasdi_points("tr2026", "oasi")
    h25, i_h25 = hi_points("mtr2025")
    h26, i_h26 = hi_points("mtr2026")
    hq = T.quotes()["mtr2026_hi_payable"]["value"]
    paths = {
        "oasdi_lane_2025": PA.payable_path(econ),
        "oasdi_2025": on_index(o25),
        "oasdi_2026": on_index(o26),
        # the lane's form on the 2026 report: the depletion year, the next year, linear to the last year, flat after
        "oasdi_2026_anchors": on_index({2034: o26[2034], 2035: o26[2035], 2100: o26[2100]}),
        "oasi_2025": on_index(a25),
        "oasi_2026": on_index(a26),
        "separate_2025": on_index(separate_points("tr2025", a25)),
        "separate_2026": on_index(separate_points("tr2026", a26)),
        "hi_lane_2025": PA.hi_payable(econ),
        "hi_2025": on_index(h25),
        "hi_2026": on_index(h26),
        # the lane's form on the 2026 report's three printed shares (2033, the 25th projection year, the last)
        "hi_2026_anchors": on_index({2033: hq["2033"], 2050: hq["2050"], 2100: hq["2100"]}),
    }
    info = {"oasdi_2025": i_o25, "oasdi_2026": i_o26, "oasi_2025": i_a25, "oasi_2026": i_a26, "hi_2025": i_h25,
            "hi_2026": i_h26}
    for y in ("2025", "2026"):
        sep, oasi = paths[f"separate_{y}"], paths[f"oasi_{y}"]
        if not (np.all(sep >= oasi - 1e-12) and np.all(sep <= 1.0)):
            blocked(f"the separate-funds path {y} is not between OASI's and full payment")
        if not np.all(sep[YEARS < info[f"oasi_{y}"]["depletion_year"]] == 1.0):
            blocked(f"the separate-funds path {y} cuts before OASI's depletion")
    return paths, info


def value_at(inf: dict, year: int, key: str = "share") -> tuple[float, float, float]:
    """A table-built path's value at a year (`share`, or `after` the reserves are gone) and its rounding interval,
    linear between the table's years as the path is."""
    pts = inf["points"]
    if year in pts:
        p = pts[year]
        return p[key], p[f"{key}_lo"], p[f"{key}_hi"]
    j, k = max(y for y in pts if y < year), min(y for y in pts if y > year)
    w = (year - j) / (k - j)
    return tuple((1 - w) * pts[j][f] + w * pts[k][f] for f in (key, f"{key}_lo", f"{key}_hi"))


def path_gates(paths: dict, info: dict) -> pd.DataFrame:
    """Each printed payable share against the path: the interval the table entries' rounding allows must meet the
    printed value's own rounding interval. "YYYY_after" is the share once the reserves are gone within that year."""
    rows = []
    for path, label, year, stated, half in PUBLISHED:
        after = isinstance(year, str)
        y = int(str(year)[:4])
        val, lo, hi = value_at(info[path], y, "after" if after else "share")
        if not after and abs(val - paths[path][y - L.Y0]) > 1e-12:
            blocked(f"{path} at {y}: the path is not its table point")
        rows.append(dict(path=path, source=label, year=str(year), stated=stated, computed=val, computed_lo=lo,
                         computed_hi=hi, passed=bool(lo <= stated + half and hi >= stated - half)))
    t = pd.DataFrame(rows)
    if not t.passed.all():
        blocked(f"payable shares not reproduced:\n{t[~t.passed].to_string()}")
    # the lane's own anchors are Note 2025.7's printed values
    q = S.quotes()
    lane = paths["oasdi_lane_2025"]
    for y, k in ((2034, "note_payable_2034"), (2035, "note_payable_2035"), (2099, "note_payable_2099")):
        if abs(lane[y - L.Y0] - q[k]["value"]) > 1e-12:
            blocked(f"the lane's OASDI path at {y} is not Note 2025.7's {q[k]['value']}")
    return t


def gdp_cross_check() -> dict:
    """Table IV.B3's OASDI income / cost (% of GDP) against Table IV.B1's (% of taxable payroll), TR 2026: the same
    ratio up to rounding. It cannot give the payable share, which needs the taxation-of-benefits component."""
    b1 = T.oasdi_rates("tr2026").set_index("year")
    b3 = T.oasdi_gdp_rates("tr2026").set_index("year")
    r1 = b1.oasdi_income / b1.oasdi_cost
    r3 = b3.oasdi_income_gdp / b3.oasdi_cost_gdp
    gap = float((r1 - r3).abs().max())
    if gap > 0.006:
        blocked(f"TR 2026 Tables IV.B1 and IV.B3 disagree on income / cost by {gap:.4f}")
    pay = b1.oasdi_payroll / (b1.oasdi_cost - b1.oasdi_tob)
    return dict(max_gap_income_over_cost=gap, income_over_cost_2100_b1=float(r1[2100]), income_over_cost_2100_b3=float(r3[2100]),
                payable_share_2100=float(pay[2100]))


# ------------------------------------------------------------------ the lifetime model on a path
def grid(econ, prelim, pay: np.ndarray, gs: list) -> dict:
    """The pension lane's model_grid on a path, at the given (rate, mortality) runs only (the grid's runs are
    independent, so each run's values equal the full grid's)."""
    with patched(PA, "GRID", list(gs)):
        return PA.model_grid(econ, prelim, pay)


def hybrid(num: dict, den: dict) -> dict:
    """A grid whose factor is num's k over den's value on Note 2025.7's basis."""
    return dict(k=num["k"], mwr={**num["mwr"], BASE: den["mwr"][BASE]}, fams=num["fams"])


def haircut_check(econ, prelim, paths: dict) -> pd.DataFrame:
    """The model's payable / scheduled ratio against Note 2025.7 Table 3 / Table 1 on the lane's validation cells
    (pension_accrual.validate_model), on the lane's path and on the 2025 tables' path."""
    t1, t3 = S.mwr_table(1), S.mwr_table(3)
    names = {"Very Low": "very_low", "Low": "low", "Medium": "medium", "High": "high"}
    rows = []
    for b in [1964, 1973, 1985, 1997, 2004]:
        for lev, key in names.items():
            for fam in L.FAMILY_SEXES:
                w = L.worker(b, L.LEVEL_ADJ[key], 21, fam, econ, prelim)
                sel = (t1.birth_year == b) & (t1.earnings_level == lev)
                note = float(t3[sel][fam].iloc[0]) / float(t1[sel][fam].iloc[0])
                row = dict(birth_year=b, level=key, family=fam, note_payable_over_scheduled=note)
                for name in ("oasdi_lane_2025", "oasdi_2025", "oasdi_2026"):
                    wp = L.worker(b, L.LEVEL_ADJ[key], 21, fam, econ, prelim, payable=paths[name])
                    row[f"model_{name}"] = wp["mwr"] / w["mwr"]
                rows.append(row)
    t = pd.DataFrame(rows)
    lane = pd.read_csv(PENSION_DERIVED / "model_check_mwr.csv")
    if len(lane) != len(t) or (lane.model_payable_over_scheduled - t.model_oasdi_lane_2025).abs().max() > 5.1e-5:
        blocked("the lane's payable haircut (model_check_mwr.csv) does not reproduce")
    return t


# ------------------------------------------------------------------ 2-4. the central under an arm
def lane_case() -> dict:
    """The pension lane's derived/case.json (the September 27 case's per-method costs), with pension_accrual.gate_inputs'
    checks except its engine hash. engine.js changed after the lane's last run (db5840f6), so that gate stops;
    case_lines_check.cjs (run first) re-evaluated the case on today's engine and found the lane's case_lines.csv and
    per-method costs unchanged. Here: that record is current, it agrees with case.json, and every other frozen file
    keeps case.json's hash; the Note 2025.7 parser equals the 09-18 lane's."""
    mine, theirs = S.mwr_table(1), ss.parse_mwr()
    if not mine.reset_index(drop=True).equals(theirs[mine.columns].reset_index(drop=True)):
        blocked("sources.mwr_table(1) differs from the 09-18 lane's parse_mwr()")
    case = json.loads((PENSION_DERIVED / "case.json").read_text())
    now_file = OUT / "case_now.json"
    if not now_file.exists():
        blocked("derived/case_now.json is missing: run case_lines_check.cjs first")
    now = json.loads(now_file.read_text())
    if not (all(case["gates"].values()) and all(now["gates"].values())):
        blocked(f"case gates: lane {case['gates']}, today {now['gates']}")
    if now["per_method"] != case["per_method"] or now["case_bn"] != case["case_bn"]:
        blocked("case_now.json's costs are not the pension lane's case.json's")
    for rec in (case["frozen_files"], now["frozen_files"]):
        moved = [f["file"] for f in rec if PA.hashlib.sha256((PA.FISCAL.parents[1] / f["file"]).read_bytes()).hexdigest() != f["sha256"]]
        if rec is now["frozen_files"] and moved:
            blocked(f"files changed since case_lines_check.cjs ran: {moved}")
        if rec is case["frozen_files"] and moved != ["infra/immigration-fiscal/assumption_explorer_2026_09_21/engine.js"]:
            blocked(f"frozen files changed since the pension lane's case.json, beyond engine.js: {moved}")
    for end in ["low", "high"]:
        got = np.mean([r["cost_bn"] for r in case["per_method"] if r["end"] == end])
        if not PA.near(got, case["case_bn"][end]):
            blocked(f"case.json per-method costs give {got} at {end}, not {case['case_bn'][end]}")
    return case


class Lane:
    """The pension lane's inputs, loaded once through its own code."""

    def __init__(self):
        q = S.quotes()
        self.u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
        self.u_2000 = q["note151_eligible_share"]["value"]["age62_in_2000"]
        self.p = PA.frame()
        self.econ = L.Economy()
        self.prelim = S.scaled_factors().preliminary.to_numpy()
        self.share_tr2025 = PA.tob_share_path() * (1 + PA.hi_over_oasdi_tob())
        self.share_central = self.share_tr2025 * PA.obbba_factor()      # the central's path, after the 2025 tax law
        self.bt = PA.benefit_tax_inputs(pd.read_csv(PENSION_DERIVED / "case_lines.csv"))
        self.case = lane_case()
        self.comp = PA.case_components(self.p)
        self.q = self.p[self.p.union & (self.p.tax_oasdi > 0)].reset_index(drop=True)
        self.fam = ss.family_vector(self.q, "observed_family")
        self.rel = self.bt["relative_rate"][BT_MAPPING]


def run_arm(lane: Lane, oasdi_grid: dict, oasdi_path: np.ndarray, hi_path, *, econ=None, share=None,
            hi_full: bool = False) -> dict:
    """The central's OASDI accrual on a grid (its factor's numerator on oasdi_path), the benefit tax's timing on that
    path, and Part A on hi_path (None: the lane's own hi_payable); the results by group and the case beside."""
    econ = econ or lane.econ
    share = lane.share_central if share is None else share
    with patched(PA, "payable_path", lambda _e: oasdi_path):
        tau = PA.tob_timing(econ, lane.prelim, share, runs=[(G, "payable")])
    acc, tob = PA.central_accrual(lane.q, {"payable": oasdi_grid}, lane.u_long, tau, lane.fam)
    w, tax, gen = lane.q.w.to_numpy(), lane.q.tax_oasdi.to_numpy(), lane.q.gen.to_numpy()
    out = dict(groups={})
    for g in GROUPS:
        m = np.ones(len(w), bool) if g == "union" else gen == g
        per = float((w * acc)[m].sum() / (w * tax)[m].sum())
        timing = float((w * acc * tob)[m].sum() / (w * acc)[m].sum())
        out["groups"][g] = dict(tax_bn=float((w * tax)[m].sum() / 1e9), accrual_bn=float((w * acc)[m].sum() / 1e9),
                                per_tax_dollar=per, timing=timing, future_share_own_rate=lane.rel[g] * timing,
                                net_own_rate=per * (1 - lane.rel[g] * timing))
    u = out["groups"]["union"]
    out["future_share_group"] = lane.rel["union"] * u["timing"]
    out["ratio_net"] = u["per_tax_dollar"] * (1 - out["future_share_group"])
    rates = None if hi_full else ["new_issue"]
    hp = (lambda _e: hi_path) if hi_path is not None else PA.hi_payable
    with patched(PA, "hi_payable", hp), patched(PA, "RATES", PA.RATES if rates is None else rates):
        hi, hi_info = PA.hi_accrual(lane.p, econ, lane.u_long, lane.u_2000)
    sel = (hi.rate == G[0]) & (hi.scenario == "payable") & (hi.mortality == G[1]) & ~hi.spouse.astype(bool) & \
        (hi.unauthorized == PA.CENTRAL["unauthorized"])
    for g in GROUPS:
        r = hi[sel & (hi.group == g)]
        if len(r) != 1:
            blocked(f"{len(r)} central Part A rows for {g}")
        r = r.iloc[0]
        out["groups"][g].update(part_a_bn=float(r.accrual_bn), hi_tax_bn=float(r.hi_tax_bn),
                                covered_workers_m=float(r.covered_workers_m),
                                part_a_per_covered_worker_usd=float(r.accrual_bn / r.covered_workers_m * 1e3),
                                part_a_per_hi_tax_dollar=float(r.accrual_bn / r.hi_tax_bn))
    out["part_a_bn"] = out["groups"]["union"]["part_a_bn"]
    out["part_a_pv_at_2024_payable"] = hi_info["part_a_pv_at_2024_payable"]
    out["case"] = case_on_accrual(lane, out["ratio_net"] / (1 - out["future_share_group"]), out["future_share_group"],
                                  out["part_a_bn"])
    out["_hi"], out["_acc"] = hi, acc
    return out


def case_on_accrual(lane: Lane, ratio: float, share: float, hi_acc: float) -> dict:
    """The September 27 case on accrual, net, at each end: pension_accrual.case_beside's formula for one arm."""
    out = {}
    for end in ["low", "high"]:
        c = lane.comp[lane.comp.end == end]
        cost = float(np.mean([r["cost_bn"] for r in lane.case["per_method"] if r["end"] == end]))
        tax, ss_cash, part_a = float(c.oasdi_tax_bn.mean()), float(c.ss_benefits_bn.mean()), float(c.part_a_bn.mean())
        receipt = lane.bt["current_receipt_bn"][BT_MAPPING][end]
        d_net = ratio * tax * (1 - share) - ss_cash + receipt
        d_hi = hi_acc - part_a
        out[end] = dict(case_bn=cost, oasdi_tax_bn=tax, oasdi_accrual_net_bn=ratio * tax * (1 - share),
                        delta_oasdi_net_bn=d_net, delta_part_a_bn=d_hi, case_on_accrual_net_bn=cost + d_net + d_hi)
    return out


def gate_control(c: dict) -> dict:
    """The control against the pension lane's derived files (its summary.json at 9ea1beb's content, hi_arms.csv,
    case_beside.csv)."""
    s = json.loads((PENSION_DERIVED / "summary.json").read_text())
    per = s["oasdi_per_tax_dollar_central_by_generation"]
    own = s["benefit_tax"]["future_share_by_generation_own_rate"]
    bad = []
    for g in GROUPS:
        if not PA.near(c["groups"][g]["per_tax_dollar"], per[g], 1e-12):
            bad.append(("per_tax_dollar", g, c["groups"][g]["per_tax_dollar"], per[g]))
        if g != "union" and not PA.near(c["groups"][g]["future_share_own_rate"], own[g], 1e-12):
            bad.append(("future_share_own_rate", g, c["groups"][g]["future_share_own_rate"], own[g]))
    for k, want in (("future_share_group", s["benefit_tax"]["future_share_group"]), ("ratio_net", s["ratio_net"]),
                    ("part_a_bn", s["central_decomposition"]["low"]["part_a_accrual_bn"])):
        if not PA.near(c[k], want, 1e-12):
            bad.append((k, "union", c[k], want))
    for e in ["low", "high"]:
        if not PA.near(c["case"][e]["case_on_accrual_net_bn"], s["case_on_accrual_net_bn"][e], 1e-12):
            bad.append(("case_on_accrual_net_bn", e, c["case"][e]["case_on_accrual_net_bn"], s["case_on_accrual_net_bn"][e]))
    # every row of the lane's hi_arms.csv, from the full Part A run
    mine = c["_hi"].copy()
    theirs = pd.read_csv(PENSION_DERIVED / "hi_arms.csv")
    key = ["rate", "scenario", "mortality", "spouse", "unauthorized", "group"]
    mine["rate"] = mine.rate.astype(str)
    theirs["rate"] = theirs.rate.astype(str)
    j = theirs.merge(mine, on=key, suffixes=("_lane", "_here"), how="outer", indicator=True)
    worst = float(max((j[f"{v}_lane"] - j[f"{v}_here"]).abs().max() for v in ("covered_workers_m", "hi_tax_bn", "accrual_bn")))
    if (j._merge != "both").any() or worst > 5.1e-7:
        bad.append(("hi_arms.csv", "all rows", worst, "<= 5e-7 (six decimals)"))
    beside = pd.read_csv(PENSION_DERIVED / "case_beside.csv")
    cen = beside[beside.arm == "central"].set_index("end")
    for e in ["low", "high"]:
        if abs(c["case"][e]["case_on_accrual_net_bn"] - cen.loc[e, "case_on_accrual_net_bn"]) > 5.1e-7:
            bad.append(("case_beside.csv central", e, c["case"][e]["case_on_accrual_net_bn"], cen.loc[e, "case_on_accrual_net_bn"]))
    if bad:
        blocked(f"the control does not reproduce the pension lane's central: {bad}")
    print(f"[control] the pension lane's central reproduced: {c['groups']['union']['per_tax_dollar']:.6f} per tax dollar, "
          f"ratio_net {c['ratio_net']:.6f}, Part A {c['part_a_bn']:.4f}bn, case {c['case']['low']['case_on_accrual_net_bn']:.4f} / "
          f"{c['case']['high']['case_on_accrual_net_bn']:.4f}bn; hi_arms.csv {len(theirs)} rows (worst {worst:.1e})")
    return dict(per_tax_dollar_rel_tol=1e-12, hi_arms_rows=int(len(theirs)), hi_arms_worst_abs=worst,
                lane_summary_sha256=PA.hashlib.sha256((PENSION_DERIVED / "summary.json").read_bytes()).hexdigest())


# ------------------------------------------------------------------ beside: 2026 inputs the swap does not apply
def economy_2026(*, rates: bool = False, wages: bool = False, parameters: bool = False) -> "L.Economy":
    """lifetime_model's Economy with any of three 2026 inputs:
      rates       TR 2026 Table V.B2's new-issue rates (history through 2025, its projection after);
      wages       Note 2026.3 Table 7's AWI path (actual through 2024, the 2026 intermediate path to 2061, its 2060-61
                  growth after; the contribution base after 2034 indexed to it, as the Economy does);
      parameters  TR 2026 Table V.C1's COLAs and contribution bases (2025 and 2026 actual, intermediate through 2034;
                  from 2035 the Economy's 2.4% CPI, which TR 2026's COLAs also reach, and its indexed base).
    The tax rates, the trust funds' effective rates (Note 2025.7 Table B) and Note 2025.3's scaled factors stay 2025's."""
    with patched(S, "awi_path", T.awi_path_2026 if wages else S.awi_path), \
            patched(S, "program_parameters_v_c1", (lambda: T.program_parameters_v_c1("tr2026")) if parameters
                    else S.program_parameters_v_c1):
        e = L.Economy()
    if rates:
        v = T.new_issue_rates("tr2026")
        a = pd.Series(np.nan, index=YEARS)
        a.loc[v.index] = v.values
        e.new_issue_nominal = a.to_numpy()
        e._disc = {}
    return e


def gate_economy_inputs() -> dict:
    """The copied V.C1 parser reproduces the pension lane's on TR 2025; TR 2026 V.C1's AWI is Note 2026.3 Table 7's
    (both the 2026 intermediate path); TR 2026's COLAs reach the lane's 2.4% CPI before 2035, where the Economy takes over."""
    mine, lane = T.program_parameters_v_c1("tr2025"), S.program_parameters_v_c1()
    if not mine.equals(lane):
        blocked("the copied Table V.C1 parser does not reproduce the pension lane's on TR 2025")
    c1, awi = T.program_parameters_v_c1("tr2026").set_index("year"), T.awi_path_2026()
    gap = float(max(abs(c1.awi[y] - awi[y]) for y in c1.index))
    if gap > 0.005:
        blocked(f"TR 2026 Table V.C1's AWI differs from Note 2026.3 Table 7's by {gap}")
    cpi = S.value("tr_cpi_ultimate")
    if not np.allclose(c1.cola.loc[2027:2035], cpi, rtol=0, atol=1e-12):
        blocked(f"TR 2026's COLAs for 2027-2035 are not the Economy's ultimate CPI {cpi}")
    return dict(v_c1_parser_reproduces_tr2025=True, v_c1_awi_vs_note_2026_3_max_gap=gap, cola_2027_2035=cpi,
                cola_2025_2026={"tr2025": [float(lane.set_index("year").cola[y]) for y in (2025, 2026)],
                                "tr2026": [float(c1.cola[y]) for y in (2025, 2026)]},
                base_tr2026_over_tr2025={str(y): float(c1.base[y] / lane.set_index("year").base[y])
                                         for y in (2026, 2030, 2034)})


def hi_cost_path_tr2026(_econ) -> np.ndarray:
    """HI incurred cost per beneficiary: Medicare TR 2026 Table V.D1 for 2015-2035, then its ultimate rate (3.5%, the
    same as 2025's), as pension_accrual.hi_cost_path builds the 2025 path."""
    v = T.hi_per_beneficiary("mtr2026")
    g = T.quotes()["mtr2026_hi_growth_ultimate"]["value"]
    out = np.full(len(YEARS), np.nan)
    for yy, val in v.items():
        out[yy - L.Y0] = val
    for k in range(2036 - L.Y0, len(YEARS)):
        out[k] = out[k - 1] * (1 + g)
    return out


def tob_share_tr2026() -> np.ndarray:
    """The national tax-on-benefits share from TR 2026 Tables IV.B1/IV.B2 (OASDI taxation of benefits over cost, which
    carries the 2025 tax law), plus HI at the lane's 2024 ratio to OASDI, on the year index as tob_share_path builds
    the 2025 one."""
    r = T.oasdi_rates("tr2026")
    s = pd.Series((r.oasdi_tob / r.oasdi_cost).to_numpy(), index=r.year.to_numpy()).reindex(YEARS).interpolate(
        limit_area="inside").ffill().bfill().to_numpy()
    return s * (1 + PA.hi_over_oasdi_tob())


# ------------------------------------------------------------------ outputs
def arm_rows(name: str, a: dict, role: str) -> list[dict]:
    return [dict(arm=name, role=role, group=g, oasdi_tax_bn=v["tax_bn"], oasdi_accrual_bn=v["accrual_bn"],
                 per_tax_dollar=v["per_tax_dollar"], timing=v["timing"],
                 future_share=a["future_share_group"] if g == "union" else v["future_share_own_rate"],
                 net_per_tax_dollar=a["ratio_net"] if g == "union" else v["net_own_rate"],
                 part_a_bn=v["part_a_bn"], hi_tax_bn=v["hi_tax_bn"], covered_workers_m=v["covered_workers_m"],
                 part_a_per_covered_worker_usd=v["part_a_per_covered_worker_usd"],
                 part_a_per_hi_tax_dollar=v["part_a_per_hi_tax_dollar"]) for g, v in a["groups"].items()]


def main() -> None:
    T.quotes()
    economy_gates = gate_economy_inputs()
    lane = Lane()
    econ, prelim = lane.econ, lane.prelim
    paths, info = build_paths(econ)
    gates = path_gates(paths, info)
    gdp = gdp_cross_check()
    hc = haircut_check(econ, prelim, paths)
    print(f"[paths] {int(gates.passed.sum())}/{len(gates)} printed payable shares reproduced; model haircut vs Note 2025.7 "
          f"Table 3, max gap: lane path {(hc.model_oasdi_lane_2025 - hc.note_payable_over_scheduled).abs().max():.4f}, "
          f"2025 tables {(hc.model_oasdi_2025 - hc.note_payable_over_scheduled).abs().max():.4f}")

    grids = {"lane": grid(econ, prelim, paths["oasdi_lane_2025"], [G, BASE]),
             "t25": grid(econ, prelim, paths["oasdi_2025"], [G, BASE])}
    for k in ("oasdi_2026", "oasdi_2026_anchors", "separate_2025", "separate_2026"):
        grids[k] = grid(econ, prelim, paths[k], [G])
    control = run_arm(lane, grids["lane"], paths["oasdi_lane_2025"], None, hi_full=True)
    control_gates = gate_control(control)
    arms = {
        "control": control,
        "tables_2025": run_arm(lane, grids["t25"], paths["oasdi_2025"], paths["hi_2025"]),
        "tr2026": run_arm(lane, hybrid(grids["oasdi_2026"], grids["t25"]), paths["oasdi_2026"], paths["hi_2026"]),
        "tr2026_oasdi": run_arm(lane, hybrid(grids["oasdi_2026"], grids["t25"]), paths["oasdi_2026"], paths["hi_2025"]),
        "tr2026_hi": run_arm(lane, grids["t25"], paths["oasdi_2025"], paths["hi_2026"]),
        "anchors_2026": run_arm(lane, hybrid(grids["oasdi_2026_anchors"], grids["lane"]), paths["oasdi_2026_anchors"],
                                paths["hi_2026_anchors"]),
    }
    # the swap is exact when nothing changes: the hybrid on equal paths is the grid itself
    same = run_arm(lane, hybrid(grids["t25"], grids["t25"]), paths["oasdi_2025"], paths["hi_2025"])
    if same["ratio_net"] != arms["tables_2025"]["ratio_net"] or same["part_a_bn"] != arms["tables_2025"]["part_a_bn"]:
        blocked("the hybrid factor on equal paths is not the grid's own")
    # beside, one change each on top of tr2026
    h26 = hybrid(grids["oasdi_2026"], grids["t25"])
    beside = {
        # the trust funds kept separate (current law): on the 2025 reports against tables_2025, on the 2026 against tr2026
        "separate_funds_2025": run_arm(lane, hybrid(grids["separate_2025"], grids["t25"]), paths["separate_2025"],
                                       paths["hi_2025"]),
        "separate_funds": run_arm(lane, hybrid(grids["separate_2026"], grids["t25"]), paths["separate_2026"],
                                  paths["hi_2026"]),
        "benefit_tax_path_tr2026": run_arm(lane, h26, paths["oasdi_2026"], paths["hi_2026"], share=tob_share_tr2026())}
    for name, flags in (("interest_tr2026", dict(rates=True)), ("wage_index_tr2026", dict(wages=True)),
                        ("program_parameters_tr2026", dict(parameters=True))):
        e = economy_2026(**flags)
        beside[name] = run_arm(lane, hybrid(grid(e, prelim, paths["oasdi_2026"], [G]), grids["t25"]),
                               paths["oasdi_2026"], paths["hi_2026"], econ=e)
    mort = T.quotes()["tr2026_mortality_decline"]["value"]
    L.survival.cache_clear()
    with patched(L, "_decline", lambda: (mort["65plus"], mort["total"])):
        beside["mortality_tr2026"] = run_arm(lane, hybrid(grid(econ, prelim, paths["oasdi_2026"], [G]), grids["t25"]),
                                             paths["oasdi_2026"], paths["hi_2026"])
        L.survival.cache_clear()
    L.survival.cache_clear()
    with patched(PA, "hi_cost_path", hi_cost_path_tr2026):
        beside["hi_costs_tr2026"] = run_arm(lane, h26, paths["oasdi_2026"], paths["hi_2026"])
    # the six together: every 2026 input this lane reads, on top of tr2026, on each reading of the trust funds
    ea = economy_2026(rates=True, wages=True, parameters=True)
    for name, key in (("all_2026_inputs", "oasdi_2026"), ("all_2026_inputs_separate_funds", "separate_2026")):
        L.survival.cache_clear()
        with patched(L, "_decline", lambda: (mort["65plus"], mort["total"])), \
                patched(PA, "hi_cost_path", hi_cost_path_tr2026):
            beside[name] = run_arm(lane, hybrid(grid(ea, prelim, paths[key], [G]), grids["t25"]), paths[key],
                                   paths["hi_2026"], econ=ea, share=tob_share_tr2026())
            L.survival.cache_clear()
    L.survival.cache_clear()
    check = run_arm(lane, h26, paths["oasdi_2026"], paths["hi_2026"])
    if check["ratio_net"] != arms["tr2026"]["ratio_net"] or check["part_a_bn"] != arms["tr2026"]["part_a_bn"]:
        blocked("the patched runs left state behind: tr2026 does not reproduce after the beside arms")

    OUT.mkdir(exist_ok=True)
    show = range(2025, 2111)
    pd.DataFrame({"year": list(show), **{k: [float(v[y - L.Y0]) for y in show] for k, v in paths.items()}}).to_csv(
        OUT / "paths.csv", index=False, float_format="%.6f", lineterminator="\n")
    pts = [dict(path=k, year=y, **{f: r.get(f) for f in ("kind", "payroll", "tob", "income", "cost", "trust_fund_ratio",
                                                          "asset_ratio", "after", "share", "share_lo", "share_hi")})
           for k, inf in info.items() for y, r in sorted(inf["points"].items())]
    pd.DataFrame(pts).to_csv(OUT / "path_points.csv", index=False, float_format="%.6f", lineterminator="\n")
    gates.to_csv(OUT / "path_gates.csv", index=False, float_format="%.6f", lineterminator="\n")
    hc.to_csv(OUT / "haircut_check.csv", index=False, float_format="%.6f", lineterminator="\n")
    rows = [r for k, a in arms.items() for r in arm_rows(k, a, "arm")] + \
        [r for k, a in beside.items() for r in arm_rows(k, a, "beside")]
    pd.DataFrame(rows).to_csv(OUT / "arms.csv", index=False, float_format="%.9f", lineterminator="\n")
    cb = [dict(arm=k, role=role, end=e, **v) for role, d in (("arm", arms), ("beside", beside)) for k, a in d.items()
          for e, v in a["case"].items()]
    cb = pd.DataFrame(cb)
    cb["change_from_control_bn"] = cb.case_on_accrual_net_bn - cb.end.map({e: control["case"][e]["case_on_accrual_net_bn"] for e in ["low", "high"]})
    cb.to_csv(OUT / "case_beside.csv", index=False, float_format="%.6f", lineterminator="\n")

    def brief(a: dict) -> dict:
        g3 = a["groups"]["G3plus"]
        return dict(ratio_net=a["ratio_net"], per_tax_dollar=a["groups"]["union"]["per_tax_dollar"],
                    future_share_group=a["future_share_group"], part_a_bn=a["part_a_bn"],
                    part_a_per_covered_worker_usd=a["groups"]["union"]["part_a_per_covered_worker_usd"],
                    g3plus_net_own_rate=g3["net_own_rate"], g3plus_part_a_per_hi_tax_dollar=g3["part_a_per_hi_tax_dollar"],
                    case_on_accrual_net_bn={e: v["case_on_accrual_net_bn"] for e, v in a["case"].items()},
                    part_a_pv_at_2024_payable=a["part_a_pv_at_2024_payable"])

    summary = dict(
        question="the pension lane's accrual (central at 9ea1beb) with the payable paths of the 2026 Trustees Reports",
        central=PA.CENTRAL, control_gates=control_gates,
        construction=("OASDI: Note 2025.7 Table 3 x k_path(person) / mwr_2025path(Note 2025.7's basis), the lifetime "
                      "model's ratio of the two paths on the published level; Part A on the path directly; the benefit "
                      "tax's timing on the arm's OASDI path"),
        headline_arm="tr2026", headline_basis=("both reports' paths year by year from their tables, the same "
                                               "construction; ungated against a 2026 money's-worth note (none published)"),
        arms={k: brief(a) for k, a in arms.items()}, beside={k: brief(a) for k, a in beside.items()},
        depletion={k: v["depletion_year"] for k, v in info.items()},
        path_gates_passed=int(gates.passed.sum()), path_gates=len(gates), gdp_cross_check=gdp,
        haircut_vs_note_2025_7=dict(
            lane_path_max_gap=float((hc.model_oasdi_lane_2025 - hc.note_payable_over_scheduled).abs().max()),
            lane_path_mean_abs_gap=float((hc.model_oasdi_lane_2025 - hc.note_payable_over_scheduled).abs().mean()),
            tables_2025_max_gap=float((hc.model_oasdi_2025 - hc.note_payable_over_scheduled).abs().max()),
            tables_2025_mean_abs_gap=float((hc.model_oasdi_2025 - hc.note_payable_over_scheduled).abs().mean()),
            tables_2026_over_2025_mean=float((hc.model_oasdi_2026 / hc.model_oasdi_2025).mean())),
        rates_tr2026_minus_tr2025={str(y): float(T.new_issue_rates("tr2026")[y] - S.new_issue_rates_v_b2()[y])
                                   for y in (2025, 2026, 2030, 2035, 2040, 2045, 2100)},
        hi_cost_tr2026_over_tr2025={str(y): float(T.hi_per_beneficiary("mtr2026")[y] / S.hi_per_beneficiary()[y])
                                    for y in (2024, 2025, 2030, 2034)},
        awi_note2026_3_over_note2025_3={str(y): float(T.awi_path_2026()[y] / S.awi_path()[y])
                                        for y in (2023, 2024, 2025, 2030, 2035, 2045, 2061)},
        economy_inputs=economy_gates,
        quotes={k: dict(doc=v["doc"], value=v["value"]) for k, v in T.QUOTES.items()},
        documents=T.provenance(),
    )
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True, default=float) + "\n")
    pd.set_option("display.width", 250)
    print(cb.pivot_table(index=["role", "arm"], columns="end", values=["case_on_accrual_net_bn", "change_from_control_bn"],
                         sort=False).round(3).to_string())
    print(pd.DataFrame(rows)[lambda d: d.group == "union"][["arm", "per_tax_dollar", "future_share", "net_per_tax_dollar",
                                                            "part_a_bn", "part_a_per_covered_worker_usd"]].round(5).to_string(index=False))
    print(f"[written] {', '.join(sorted(x.name for x in OUT.iterdir()))}")


if __name__ == "__main__":
    main()
