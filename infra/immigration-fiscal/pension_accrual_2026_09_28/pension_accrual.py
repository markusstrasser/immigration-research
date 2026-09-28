"""The September 27 case with Social Security (OASDI) and Medicare Part A on an accrual basis, beside the case.

Steps, each gated (a failed gate stops with [BLOCKED] before anything is written to derived/):
  1. Reproduce the 09-18 timing lane's union row (lifetime_longevity_sstiming_2026_09_18/derived/ss_timing_group.csv,
     mexican_observed_total) with its own code, imported read-only: accruals() and parse_mwr() on its cached frame.
  2. The case: derived/case.json (case_lines.cjs) is current against the package chain, and its per-method costs
     reproduce the case; this lane's Note 2025.7 parser equals the 09-18 lane's; every quote is in its document.
  3. Rebuild the 09-18 frame through its own stage() (a hook keeps the CPS person keys), gate that it equals the
     cached parquet exactly, and attach the case's state-aware unauthorized flag (cps_ca_status.status_sets,
     imported), year of entry and Medicare coverage.
  4. Validate the lifetime model (lifetime_model.py) against TR 2025 Table V.C7 and Note 2025.7 Tables 1 and 3;
     compute its grid of ratio factors (discount rate, mortality, career start, attribution); gate that the factor
     is 1 on Note 2025.7's own basis and that the attributions add up to lifetime benefits.
  5. OASDI accrual per dollar of the group's on-books OASDI tax under every combination of arms.
  6. Part A accrual per covered worker-year from the Part A present value at 65 (Medicare TR 2025 per-beneficiary
     costs, NVSS 2024 survival) and the probability of qualifying.
  7. Steady-state cross-check: the group's 2024 OASDI and Part A cash flows at stationary age structures (NVSS
     2024 Hispanic and total person-years) and at the white reference's ages.
  8. The case beside at specifications 48 and 11 (derived/case_lines.csv from case_lines.cjs), every arm.

Run from the repository root, after case_lines.cjs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/pension_accrual_2026_09_28/pension_accrual.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
CACHE = HERE / "_cache"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(FISCAL / "lifetime_longevity_sstiming_2026_09_18"))
sys.path.insert(0, str(FISCAL / "california_medical_status_2026_09_23"))
sys.path.insert(0, str(FISCAL / "ledger_absolute_2026_09_17"))

import sources as S  # noqa: E402
import lifetime_model as L  # noqa: E402
import ss_timing as ss  # noqa: E402  the 09-18 lane: parse_mwr, accruals, mwr_interpolate, family_vector, stage
import cps_ca_status as ca  # noqa: E402  the case's state-aware status flag
from lifetime import read_life_table  # noqa: E402  NVSS 2024 life tables as the ledger reads them

UNION = ss.MEXICAN                      # mexico_born, mexican_second_gen, mexican_third_plus_selfid
GEN = dict(zip(UNION, ["G1", "G2", "G3plus"]))
WHITE = "third_plus_nh_white"
BANDS = ss.BAND_LABEL
STORED_UNION = dict(population=40896574.15235186, tax_pp=2997.6099450490483, benefit_pp=1253.323060287263,
                    accrual_only_bn=-188.13650797305468, cash_to_accrual_bn=-136.87988850116403)
ONBOOKS_FILE = FISCAL / "onbooks_share_2026_09_23/derived/onbooks_split.csv"
ENTRY_CODES = FISCAL / "indian_civic_cps_2026_09_18/_cache/asec_2025_PEINUSYR.json"
SE_OASDI, SE_HI = 0.124, 0.029          # statutory self-employment rates [SOURCE: TR 2025 Table V.C6; MTR 2025 sec. II]
MEDIUM_CAREER = 66_223.0 / 66_621.80    # Note 2025.7 Table A: medium career average / AWI 2023 (0.994)
MODEL_LEVELS = np.array([0.25, 0.45, 1.00, 1.60])   # career level of Note 2025.3's four scaled sets (x AWI)
# discount rates: the Trustees' new-issue path (TR Table V.B2), the trust funds' effective rates (Note 2025.7
# Table B), constant real rates, and the AWI's growth (r = g, for the steady-state comparison)
RATES = ["new_issue", "tf", 0.02, 0.023, 0.03, "awi"]
GRID = [(r, "general") for r in RATES] + [("new_issue", "hispanic")]   # (discount rate, mortality) model runs
BASE = ("tf", "general")                   # Note 2025.7's own basis: trust-fund rates, the Trustees' mortality
ENTRIES = list(range(21, 61, 3))           # career start (US covered work) for the Mexico-born, floored to this grid
BIRTHS = list(range(1950, 2008, 2))        # the model needs the AWI from age 21 (Note 2025.3 starts in 1970)


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def near(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(1.0, abs(b))


# ------------------------------------------------------------------ 1. the 09-18 union row
def gate_union_row() -> dict:
    p = pd.read_parquet(ss.OUT / "cps_ss_stage.parquet")
    mwr = ss.parse_mwr()
    acc = ss.accruals(p, mwr, "observed_family", "individual", True, 1.0)
    tax = (p.oasdi_wage + p.oasdi_se).to_numpy()
    ben = p.ss_benefit.to_numpy()
    m = np.zeros(len(p), bool)
    for g in UNION:
        m |= p[g].to_numpy()
    w = p.w.to_numpy()[m]
    got = dict(population=float(w.sum()), tax_pp=float(np.average(tax[m], weights=w)),
               benefit_pp=float(np.average(ben[m], weights=w)),
               accrual_only_bn=float((-acc[m] * w).sum() / 1e9),
               cash_to_accrual_bn=float(((-acc + ben)[m] * w).sum() / 1e9))
    got["accrual_per_tax_dollar"] = float((acc[m] * w).sum() / (tax[m] * w).sum())
    bad = {k: (got[k], v) for k, v in STORED_UNION.items() if not near(got[k], v, 1e-9)}
    if bad:
        blocked(f"the 09-18 union row does not reproduce: {bad}")
    print(f"[gate 1] 09-18 union row reproduced: accrual {got['accrual_only_bn']:.4f}bn, cash-to-accrual "
          f"{got['cash_to_accrual_bn']:.4f}bn, {got['accrual_per_tax_dollar']:.4f} per tax dollar")
    return got


# ------------------------------------------------------------------ 2. the frame with status and entry
def entry_midpoints() -> dict:
    items = json.loads(ENTRY_CODES.read_text())["values"]["item"]
    out = {}
    for code, label in items.items():
        code = int(code)
        if code == 0:
            continue
        if label.startswith("Before"):
            out[code] = 1945.0
        else:
            lo, hi = (int(x) for x in label.split("-"))
            hi = min(hi, 2025)
            out[code] = (lo + hi + 1) / 2 if hi > lo else lo + 0.5
    return out


def stage_frame() -> pd.DataFrame:
    """The 09-18 frame with the case's status flags, cached under a key of the code that builds it (the 09-18
    stage, its extension builder and the case's status imputation): an edit to any of them rebuilds the cache."""
    key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (ss.__file__, ss.ext.__file__, ca.__file__)))
    cache = CACHE / f"stage_{key.hexdigest()[:16]}.parquet"
    if cache.exists():
        return pd.read_parquet(cache)
    hold = {}
    orig = ss.ext.build

    def hooked(ns):
        st = orig(ns)
        hold["d"] = st["d"]
        return st

    ss.ext.build = hooked
    try:
        p = ss.stage()
    finally:
        ss.ext.build = orig
    ref = pd.read_parquet(ss.OUT / "cps_ss_stage.parquet")
    if not p.reset_index(drop=True).equals(ref.reset_index(drop=True)):
        blocked("the 09-18 stage() no longer reproduces its cached cps_ss_stage.parquet")
    d = hold["d"]
    p["PH_SEQ"] = d.PH_SEQ.to_numpy()
    p["A_LINENO"] = d.A_LINENO.to_numpy()
    p["se"] = (d.SEMP_VAL.clip(lower=0) + d.FRSE_VAL.clip(lower=0)).to_numpy(dtype=float)
    cd, hh = ca.load()
    sets = ca.status_sets(cd, hh)
    st = cd[["PH_SEQ", "A_LINENO", "PEINUSYR", "MCARE", "PENATVTY", "PRCITSHP"]].copy()
    st["unauth_state_aware"] = sets["state_aware_verified_states"]["unauthorized"]
    st["unauth_paper"] = sets["borjas_paper_rules"]["unauthorized"]
    m = p[["PH_SEQ", "A_LINENO"]].merge(st, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    if m.PEINUSYR.isna().any():
        blocked("CPS persons without a status record")
    for c in ["PEINUSYR", "MCARE", "PENATVTY", "PRCITSHP", "unauth_state_aware", "unauth_paper"]:
        p[c] = m[c].to_numpy()
    CACHE.mkdir(exist_ok=True)
    p.to_parquet(cache, index=False)
    return p


def frame() -> pd.DataFrame:
    p = stage_frame()
    ref = pd.read_parquet(ss.OUT / "cps_ss_stage.parquet")
    if not p[ref.columns].reset_index(drop=True).equals(ref):
        blocked("the cached stage differs from the 09-18 parquet")
    union = np.zeros(len(p), bool)
    for g in UNION:
        union |= p[g].to_numpy()
    p["union"] = union
    p["gen"] = ""
    for g in UNION:
        p.loc[p[g], "gen"] = GEN[g]
    split = pd.read_csv(ONBOOKS_FILE).set_index("kind")
    s_mex = float(split.loc["evidence_central", "s_mex"])
    p["unauth"] = p.unauth_state_aware.astype(bool) & p.mexico_born
    p["onbooks"] = np.where(p.unauth, s_mex, 1.0)
    # the case's OASDI and HI tax bases (unauthorized at the on-books share, as the case's status stack)
    p["tax_oasdi"] = (p.oasdi_wage + p.oasdi_se) * p.onbooks
    p["hi_se"] = SE_HI * ss.SECA_FACTOR * p.se
    p["tax_hi"] = (2 * 0.0145 * p.wage + p.hi_se) * p.onbooks
    mid = entry_midpoints()
    entry_year = p.PEINUSYR.map(mid)
    p["arrival_age"] = np.where(p.mexico_born & entry_year.notna(), p.age - (2024.5 - entry_year), np.nan)
    p.attrs["s_mex"] = s_mex
    return p


# ------------------------------------------------------------------ 3. the lifetime model
def payable_path(econ: L.Economy) -> np.ndarray:
    """Share of scheduled OASDI benefits paid by year: Note 2025.7's 90.2% (2034), 80.7% (2035), linear to
    71.9% (2099), flat after."""
    y = np.arange(L.Y0, L.Y1 + 1)
    p = np.ones(len(y))
    p[y == 2034] = S.value("note_payable_2034")
    a, z = S.value("note_payable_2035"), S.value("note_payable_2099")
    mid = (y >= 2035) & (y <= 2099)
    p[mid] = a + (z - a) * (y[mid] - 2035) / (2099 - 2035)
    p[y > 2099] = z
    return p


def validate_model(econ, prelim) -> tuple[pd.DataFrame, pd.DataFrame]:
    v = S.benefit_amounts_v_c7()
    v["model_pct"] = [100 * L.replacement_at_65(r.year_65 - 65, L.LEVEL_ADJ[r.level], econ, prelim) for _, r in v.iterrows()]
    v["gap_pp"] = v.model_pct - v.at65_pct
    if v.gap_pp.abs().max() > 0.25:
        blocked(f"the benefit formula misses TR Table V.C7 by {v.gap_pp.abs().max():.2f} points")
    t1, t3 = S.mwr_table(1), S.mwr_table(3)
    pay = payable_path(econ)
    names = {"Very Low": "very_low", "Low": "low", "Medium": "medium", "High": "high"}
    rows = []
    for b in [1964, 1973, 1985, 1997, 2004]:
        for lev, key in names.items():
            for fam in L.FAMILY_SEXES:
                w = L.worker(b, L.LEVEL_ADJ[key], 21, fam, econ, prelim)
                wp = L.worker(b, L.LEVEL_ADJ[key], 21, fam, econ, prelim, payable=pay)
                sel = (t1.birth_year == b) & (t1.earnings_level == lev)
                n1, n3 = float(t1[sel][fam].iloc[0]), float(t3[sel][fam].iloc[0])
                rows.append(dict(birth_year=b, level=key, family=fam, note_scheduled=n1, model_scheduled=w["mwr"],
                                 model_over_note=w["mwr"] / n1, note_payable_over_scheduled=n3 / n1,
                                 model_payable_over_scheduled=wp["mwr"] / w["mwr"]))
    t = pd.DataFrame(rows)
    gap = (t.model_payable_over_scheduled - t.note_payable_over_scheduled).abs().max()
    if gap > 0.06:
        blocked(f"the model's payable haircut misses Note 2025.7 Table 3 by {gap:.3f}")
    return v, t


def model_grid(econ, prelim) -> dict:
    """k[method][g] (family, entry, birth, level, age): accrual per PV-dollar of tax at that age; mwr[g]
    (family, entry, birth, level): the lifetime money's-worth ratio; g = (discount rate, mortality) from GRID.
    mwr[BASE][..., entry 21, ...] normalizes."""
    fams = list(L.FAMILY_SEXES)
    shape = (len(fams), len(ENTRIES), len(BIRTHS), len(MODEL_LEVELS))
    k = {m: {g: np.full(shape + (121,), np.nan) for g in GRID} for m in L.METHODS}
    mwr = {g: np.full(shape, np.nan) for g in GRID}
    adj = [L.LEVEL_ADJ[x] for x in ["very_low", "low", "medium", "high"]]
    for fi, fam in enumerate(fams):
        for ei, entry in enumerate(ENTRIES):
            for bi, b in enumerate(BIRTHS):
                for li, a in enumerate(adj):
                    for g in GRID:
                        w = L.worker(b, a, entry, fam, econ, prelim, arm=g[0], population=g[1])
                        mwr[g][fi, ei, bi, li] = w["mwr"]
                        for mth in L.METHODS:
                            k[mth][g][fi, ei, bi, li] = w["per_tax"][mth]
    return dict(k=k, mwr=mwr, fams=fams)


def interp_weights(x: np.ndarray, knots: np.ndarray, log=False):
    """Lower index and weight for linear (or log-linear) interpolation, flat outside the knots."""
    xs = np.log(knots) if log else knots.astype(float)
    xv = np.log(np.clip(x, knots[0], knots[-1])) if log else np.clip(x, knots[0], knots[-1])
    j = np.clip(np.searchsorted(xs, xv, side="right") - 1, 0, len(xs) - 2)
    wgt = (xv - xs[j]) / (xs[j + 1] - xs[j])
    return j, wgt


def model_factor(grid, method, g, fam, entry, birth, level, age) -> np.ndarray:
    """k_method(age | family, entry, birth, level, g) / mwr_BASE(family, entry 21, birth, level): the lane's
    adjustment to Note 2025.7's ratio for one person. Entry is floored to the grid (the run must have covered
    work at the person's age); birth year linear and level log-linear between grid points. Ages under 21 take
    21; ages 65 and over (no earnings in the model) take the lifetime ratio of run g."""
    fams = grid["fams"]
    fi = np.array([fams.index(f) for f in fam])
    ent = np.array(ENTRIES)
    ei = np.clip(np.searchsorted(ent, np.maximum(entry, 21), side="right") - 1, 0, len(ent) - 1)
    bj, bw = interp_weights(birth, np.array(BIRTHS, float))
    lj, lw = interp_weights(level, MODEL_LEVELS, log=True)
    a = np.clip(age, 21, 64).astype(int)
    old = age >= 65
    kk, mm = grid["k"][method][g], grid["mwr"][g]
    m0 = grid["mwr"][BASE]
    num = np.zeros(len(fi))
    den = np.zeros(len(fi))
    for db, wb in ((0, 1 - bw), (1, bw)):
        for dl, wl in ((0, 1 - lw), (1, lw)):
            v = np.where(old, mm[fi, ei, bj + db, lj + dl], kk[fi, ei, bj + db, lj + dl, a])
            if np.isnan(v).any():
                blocked(f"model grid has no value for {int(np.isnan(v).sum())} persons ({method}, {g})")
            num += wb * wl * v
            den += wb * wl * m0[fi, 0, bj + db, lj + dl]
    return num / den


# ------------------------------------------------------------------ 4. OASDI accrual arms
MAPPINGS = ["individual_raw", "individual_age_adjusted", "group_career_mean"]
UNAUTH = {"none": 0.0, "note151_long_run": None, "note151_2000_cohort": None, "full": 1.0}


def career_levels(p: pd.DataFrame, mapping: str) -> np.ndarray:
    """Career-average covered earnings over the AWI, the axis of Note 2025.7's tables.
    individual_raw: this year's wage over the 2024 AWI (the 09-18 lane's mapping);
    individual_age_adjusted: this year's covered earnings over the medium scaled worker's earnings at the same
        age (Note 2025.3 Table 6), times the medium worker's career average (0.994 of the AWI);
    group_career_mean: each generation's mean covered earnings at 21-64, zeros included (SSA's scaled-worker
        concept), for every member."""
    covered = np.minimum(p.wage.to_numpy(), ss.ext.OASDI_CAP_2024) + ss.SECA_FACTOR * p.se.to_numpy()
    taxed = p.tax_oasdi.to_numpy() > 0
    if mapping == "individual_raw":
        return np.where(taxed, p.wage.to_numpy() / ss.AWI_2024, 1.0)
    if mapping == "individual_age_adjusted":
        f = S.scaled_factors().set_index("age").preliminary
        fa = f.reindex(np.clip(p.age.to_numpy(), 21, 64)).to_numpy()
        return np.where(taxed, covered / ss.AWI_2024 * MEDIUM_CAREER / (L.LEVEL_ADJ["medium"] * fa), 1.0)
    if mapping == "group_career_mean":
        out = np.ones(len(p))
        pool = p.age.between(21, 64).to_numpy() & p.civilian.to_numpy()
        w = p.w.to_numpy()
        for g in UNION:
            m = p[g].to_numpy()
            out[m] = np.average(covered[m & pool], weights=w[m & pool]) / ss.AWI_2024
        return out
    raise ValueError(mapping)


def note_mwr(p: pd.DataFrame, table: pd.DataFrame, level: np.ndarray, fam: np.ndarray) -> np.ndarray:
    """Note 2025.7 ratios per person through the 09-18 lane's interpolation (imported)."""
    birth = (ss.INCOME_YEAR - p.age.to_numpy()).astype(float)
    out = np.zeros(len(p))
    for f in ss.FAMILY:
        m = fam == f
        if m.any():
            out[m] = ss.mwr_interpolate(table, f, birth[m], level[m])
    return out


def oasdi_arms(p: pd.DataFrame, grid: dict, u_long: float, u_2000: float) -> pd.DataFrame:
    """Accrual per dollar of the group's on-books OASDI tax, for every combination of arms, overall and by
    generation. The model factor is 1 at EAN, trust-fund rates and full careers (Note 2025.7's own ratio)."""
    q = p[p.union & (p.tax_oasdi > 0)].reset_index(drop=True)
    fam = ss.family_vector(q, "observed_family")
    tables = {"scheduled": S.mwr_table(1), "payable": S.mwr_table(3)}
    w, tax = q.w.to_numpy(), q.tax_oasdi.to_numpy()
    birth_m = np.clip(ss.INCOME_YEAR - q.age.to_numpy(), BIRTHS[0], BIRTHS[-1]).astype(float)
    arr = np.where(q.mexico_born & q.arrival_age.notna(), q.arrival_age.fillna(21), 21.0)
    unauth = q.unauth.to_numpy()
    gens = q.gen.to_numpy()
    shares = {"none": 0.0, "note151_long_run": u_long, "note151_2000_cohort": u_2000, "full": 1.0}
    rows = []
    for mapping in MAPPINGS:
        level = career_levels(q, mapping)
        lvl_m = np.clip(level, MODEL_LEVELS[0], MODEL_LEVELS[-1])
        base = {s: note_mwr(q, t, level, fam) for s, t in tables.items()}
        for method in L.METHODS:
            for g in GRID:
                for entry_on in (True, False):
                    entry = arr if entry_on else np.full(len(q), 21.0)
                    fac = model_factor(grid, method, g, fam, entry, birth_m, lvl_m, q.age.to_numpy().astype(float))
                    for scen, mwr in base.items():
                        for uname, u in shares.items():
                            acc = tax * mwr * fac * np.where(unauth, u, 1.0)
                            for grp in ["union", "G1", "G2", "G3plus"]:
                                m = np.ones(len(q), bool) if grp == "union" else gens == grp
                                rows.append(dict(mapping=mapping, method=method, rate=str(g[0]), mortality=g[1],
                                                 career_start=entry_on, scenario=scen, unauthorized=uname, group=grp,
                                                 tax_bn=float((w * tax)[m].sum() / 1e9),
                                                 accrual_bn=float((w * acc)[m].sum() / 1e9),
                                                 per_tax_dollar=float((w * acc)[m].sum() / (w * tax)[m].sum())))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ 5. Part A
def hi_payable(econ: L.Economy) -> np.ndarray:
    """Share of HI costs covered after depletion (Medicare TR 2025): 89% from 2033, linear to 86% in 2049 and
    to 100% in 2099."""
    path = S.quotes()["mtr_hi_payable_path"]["value"]
    y = np.arange(L.Y0, L.Y1 + 1)
    out = np.ones(len(y))
    a, b, c = path["2033"], path["2049"], path["2099"]
    m1 = (y >= 2033) & (y <= 2049)
    out[m1] = a + (b - a) * (y[m1] - 2033) / (2049 - 2033)
    m2 = (y > 2049) & (y <= 2099)
    out[m2] = b + (c - b) * (y[m2] - 2049) / (2099 - 2049)
    return out


def hi_cost_path(econ: L.Economy) -> np.ndarray:
    """HI incurred cost per beneficiary by year: Table V.D1 for 2015-2034, then the ultimate 3.5% a year."""
    v = S.hi_per_beneficiary()
    g = S.value("mtr_hi_growth_ultimate")
    y = np.arange(L.Y0, L.Y1 + 1)
    out = np.full(len(y), np.nan)
    for yy, val in v.items():
        out[yy - L.Y0] = val
    for k in range(2035 - L.Y0, len(y)):
        out[k] = out[k - 1] * (1 + g)
    return out


def part_a_pv(age: np.ndarray, sex: np.ndarray, econ: L.Economy, rate, scenario: str,
              population: str = "general") -> np.ndarray:
    """PV at 2024 of Part A costs from 65 for a person of this age and sex alive in 2024: the average HI cost per
    beneficiary each year (no age gradient), NVSS 2024 survival by sex improved at the TR rates."""
    cost = hi_cost_path(econ)
    pay = hi_payable(econ) if scenario == "payable" else np.ones(len(cost))
    disc = econ.discount(rate)
    out = np.zeros(len(age))
    cache = {}
    for i, (a, s) in enumerate(zip(age.astype(int), sex)):
        key = (a, s)
        if key not in cache:
            b = 2024 - a
            if a >= 65:
                cache[key] = 0.0
            else:
                surv = L.survival(b, population, "male" if s == 1 else "female", a)
                c = econ.at(cost, b) * econ.at(pay, b) * econ.at(disc, b)
                cache[key] = float((surv * c)[65:].sum())
        out[i] = cache[key]
    return out


def hi_accrual(p: pd.DataFrame, econ: L.Economy, u_long: float, u_2000: float) -> tuple[pd.DataFrame, dict]:
    """Part A accrual per covered worker-year: P(qualify) x PV(Part A from 65) / expected covered years, for the
    worker and, in a one-earner couple, the spouse who qualifies on the worker's record."""
    u = p[p.union].copy()
    w = u.w.to_numpy()
    covered = (u.tax_hi > 0).to_numpy()
    # probability of qualifying: the share of the generation's 65+ (lawfully present) covered by Medicare
    info = {}
    pq = np.zeros(len(u))
    for g in ["G1", "G2", "G3plus"]:
        m = (u.gen == g).to_numpy() & (u.age >= 65).to_numpy() & ~u.unauth.to_numpy()
        share = float(np.average((u.MCARE == 1).to_numpy()[m], weights=w[m]))
        info[f"p_qualify_{g}"] = share
        pq[(u.gen == g).to_numpy()] = share
    # expected covered years from career start to 64: the generation's share with HI-covered earnings by age
    cov = {}
    for g in ["G1", "G2", "G3plus"]:
        m = (u.gen == g).to_numpy()
        wt = pd.Series(w[m]).groupby(u.age.to_numpy()[m]).sum()
        num = pd.Series(covered[m] * w[m]).groupby(u.age.to_numpy()[m]).sum()
        cov[g] = (num / wt).reindex(range(0, 91)).fillna(0.0).to_numpy()
    start = np.where(u.mexico_born & u.arrival_age.notna(), np.maximum(u.arrival_age.fillna(21), 21), 21).astype(int)
    n_years = np.array([cov[g][s:65].sum() for g, s in zip(u.gen, start)])
    info["expected_covered_years"] = {g: float(cov[g][21:65].sum()) for g in cov}
    one_earner = (u.married & (u.spouse_wage <= 0)).to_numpy()
    # an unauthorized worker-year is covered only on the books (the case's on-books share), and credited only
    # with the legalization probability of the arm
    onbooks = u.onbooks.to_numpy()
    shares = {"none": 0.0, "note151_long_run": u_long, "note151_2000_cohort": u_2000, "full": 1.0}
    runs = [(r, sc, "general") for r in RATES for sc in ["scheduled", "payable"]] + [("new_issue", "scheduled", "hispanic")]
    rows = []
    for rate, scen, pop in runs:
        own = part_a_pv(u.age.to_numpy(), u.sex.to_numpy(), econ, rate, scen, pop)
        spouse = part_a_pv(u.age.to_numpy(), np.where(u.sex.to_numpy() == 1, 2, 1), econ, rate, scen, pop)
        for fam_on in (True, False):
            value = own + (spouse if fam_on else 0) * one_earner
            base = np.where(covered & (u.age < 65).to_numpy() & (n_years > 0), pq * value / np.maximum(n_years, 1e-9), 0.0)
            for uname, uu in shares.items():
                acc = base * onbooks * np.where(u.unauth.to_numpy(), uu, 1.0)
                for g in ["union", "G1", "G2", "G3plus"]:
                    m = np.ones(len(u), bool) if g == "union" else (u.gen == g).to_numpy()
                    rows.append(dict(rate=str(rate), scenario=scen, mortality=pop, spouse=fam_on, unauthorized=uname,
                                     group=g, covered_workers_m=float((w * covered)[m].sum() / 1e6),
                                     hi_tax_bn=float((w * u.tax_hi.to_numpy())[m].sum() / 1e9),
                                     accrual_bn=float((w * acc)[m].sum() / 1e9)))
    info["part_a_pv_at_2024"] = {f"{s}_age_{a}": float(part_a_pv(np.array([a]), np.array([k]), econ, "new_issue", "scheduled")[0])
                                 for s, k in (("male", 1), ("female", 2)) for a in (25, 45, 64)}
    return pd.DataFrame(rows), info


# ------------------------------------------------------------------ 6. steady state
def band_structures(p: pd.DataFrame) -> dict:
    """Age-band shares (the 09-18 bands): the union's own, the white reference's (CPS), and the stationary
    populations of the NVSS 2024 Hispanic and total life tables (person-years by band)."""
    out = {}
    for name, m in (("own", p.union.to_numpy()), ("white_ages", p[WHITE].to_numpy())):
        s = np.bincount(p.band.to_numpy()[m], weights=p.w.to_numpy()[m], minlength=8)
        out[name] = s / s.sum()
    edges = [0] + ss.BAND_EDGES + [101]
    for name, key in (("stationary_hispanic", "hispanic"), ("stationary_total", "total")):
        t = read_life_table(S.FISCAL.parents[1], key)
        yrs = np.array([t.Lx.to_numpy()[lo:hi].sum() for lo, hi in zip(edges[:-1], edges[1:])])
        out[name] = yrs / yrs.sum()
    return out


def steady_state(p: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Per-person band profiles of the union's OASDI and HI cash flows, reweighted to each structure: the
    factor by which each line's 2024 total would change at that age mix."""
    u = p.union.to_numpy()
    w, band = p.w.to_numpy()[u], p.band.to_numpy()[u]
    pop = np.bincount(band, weights=w, minlength=8)
    flows = {"oasdi_tax": p.tax_oasdi.to_numpy()[u], "ss_benefit": p.ss_benefit.to_numpy()[u],
             "hi_tax": p.tax_hi.to_numpy()[u], "medicare_covered": (p.MCARE.to_numpy()[u] == 1).astype(float)}
    pp = {k: np.bincount(band, weights=w * v, minlength=8) / pop for k, v in flows.items()}
    structs = band_structures(p)
    rows = []
    for name, s in structs.items():
        for k, v in pp.items():
            rows.append(dict(structure=name, flow=k, per_person=float((s * v).sum()),
                             factor=float((s * v).sum() / (structs["own"] * v).sum())))
    shares = pd.DataFrame({k: v for k, v in structs.items()}, index=BANDS)
    return pd.DataFrame(rows), dict(band_shares=shares.round(6).to_dict(), per_person_by_band={k: v.round(4).tolist() for k, v in pp.items()})


# ------------------------------------------------------------------ 7. the case beside
def case_components(p: pd.DataFrame) -> pd.DataFrame:
    """The case's pension lines per method and end (derived/case_lines.csv), with the self-employment receipt
    split into its OASDI and HI parts by the group's own CPS split, and Part A at the national HI share of
    Medicare benefits (Medicare TR 2025 Table II.B1)."""
    lines = pd.read_csv(OUT / "case_lines.csv")
    u = p.union.to_numpy()
    w = p.w.to_numpy()[u]
    se_oasdi = float((w * (p.oasdi_se * p.onbooks).to_numpy()[u]).sum())
    se_hi = float((w * (p.hi_se * p.onbooks).to_numpy()[u]).sum())
    share = se_oasdi / (se_oasdi + se_hi)
    ben = S.quotes()["mtr_benefits_2024_bn"]["value"]
    part_a = ben["hi"] / ben["total"]
    rows = []
    for (method, end), g in lines.groupby(["method", "end"]):
        x = g.set_index("line").amount_bn
        rows.append(dict(method=method, end=end, spec=int(g.spec.iloc[0]),
                         oasdi_tax_bn=x.employee_oasdi + x.employer_oasdi + share * x.self_employment_oasdi_hi,
                         hi_tax_bn=x.employee_hi + x.employer_hi + (1 - share) * x.self_employment_oasdi_hi,
                         ss_benefits_bn=x.social_security, railroad_bn=x.railroad_retirement,
                         medicare_bn=x.medicare, part_a_bn=part_a * x.medicare))
    out = pd.DataFrame(rows)
    out.attrs.update(se_oasdi_share=share, part_a_share=part_a)
    return out


CENTRAL = dict(mapping="individual_age_adjusted", method="EAN", rate="new_issue", mortality="general",
               career_start=True, scenario="scheduled", unauthorized="note151_long_run", spouse=True)
# The central and one change each. OASDI reads mapping, method, rate, mortality, career start, scenario and
# unauthorized; Part A reads rate, mortality, scenario, unauthorized and spouse. A rate given per end applies at
# that end (the case's own 2% / 3% return on public capital). Bridges are not candidates for the central and
# stay out of the range.
ARMS = {
    "central": {},
    "payable": dict(scenario="payable"),
    "rate_trust_fund_effective": dict(rate="tf"),
    "rate_real_2.3_flat": dict(rate="0.023"),
    "rate_real_2": dict(rate="0.02"),
    "rate_real_3": dict(rate="0.03"),
    "rate_case_2_3": dict(rate={"low": "0.02", "high": "0.03"}),
    "unauthorized_none": dict(unauthorized="none"),
    "unauthorized_2000_cohort": dict(unauthorized="note151_2000_cohort"),
    "unauthorized_full": dict(unauthorized="full"),
    "attribution_puc": dict(method="PUC"),
    "attribution_abo": dict(method="ABO"),
    "mapping_raw_wage": dict(mapping="individual_raw"),
    "mapping_group_mean": dict(mapping="group_career_mean"),
    "career_start_off": dict(career_start=False),
    "hispanic_mortality": dict(mortality="hispanic"),
    "part_a_spouse_off": dict(spouse=False),
    "bridge_rate_wage_growth": dict(rate="awi"),
    "bridge_sept18": dict(mapping="individual_raw", rate="tf", career_start=False, unauthorized="full"),
}
OASDI_KEYS = ["mapping", "method", "rate", "mortality", "career_start", "scenario", "unauthorized"]
HI_KEYS = ["rate", "mortality", "scenario", "unauthorized", "spouse"]


def arm_spec(name: str, end: str) -> dict:
    spec = {**CENTRAL, **ARMS[name]}
    if isinstance(spec["rate"], dict):
        spec["rate"] = spec["rate"][end]
    return spec


def pick(df: pd.DataFrame, spec: dict, keys: list[str], group: str = "union") -> pd.Series:
    sel = (df.group == group).to_numpy().copy()
    for k in keys:
        sel &= (df[k] == spec[k]).to_numpy()
    if sel.sum() != 1:
        blocked(f"{int(sel.sum())} rows for {group} {({k: spec[k] for k in keys})}")
    return df[sel].iloc[0]


def case_beside(comp: pd.DataFrame, oasdi: pd.DataFrame, hi: pd.DataFrame, case: dict) -> pd.DataFrame:
    """Each arm at each end, the two fill-in methods averaged: the case; its OASDI taxes and the accrual they earn
    (the group's accrual per dollar of on-books OASDI tax x the case's OASDI tax); the 2024 Social Security
    benefits the accrual replaces; the Part A accrual of the group's covered workers and the 2024 Part A benefits
    it replaces. Railroad retirement, Parts B and D and every receipt stay as the case has them."""
    rows = []
    for end in ["low", "high"]:
        c = comp[comp.end == end]
        cost = float(np.mean([r["cost_bn"] for r in case["per_method"] if r["end"] == end]))
        tax, ss_cash, part_a = float(c.oasdi_tax_bn.mean()), float(c.ss_benefits_bn.mean()), float(c.part_a_bn.mean())
        for name in ARMS:
            spec = arm_spec(name, end)
            ratio = float(pick(oasdi, spec, OASDI_KEYS).per_tax_dollar)
            hi_acc = float(pick(hi, spec, HI_KEYS).accrual_bn)
            d_oasdi, d_hi = ratio * tax - ss_cash, hi_acc - part_a
            rows.append(dict(arm=name, bridge=name.startswith("bridge_"), end=end, spec=int(c.spec.iloc[0]),
                             case_bn=cost, oasdi_tax_bn=tax, accrual_per_tax_dollar=ratio, oasdi_accrual_bn=ratio * tax,
                             ss_benefits_removed_bn=ss_cash, delta_oasdi_bn=d_oasdi, hi_tax_bn=float(c.hi_tax_bn.mean()),
                             part_a_accrual_bn=hi_acc, part_a_removed_bn=part_a, delta_part_a_bn=d_hi,
                             delta_bn=d_oasdi + d_hi, case_on_accrual_bn=cost + d_oasdi + d_hi))
    return pd.DataFrame(rows)


def elderly_receipt(p: pd.DataFrame) -> pd.DataFrame:
    """Social Security receipt and Medicare coverage at 65 and over, by generation and for the white reference:
    what the steady-state route inherits from today's elderly."""
    old = (p.age >= 65).to_numpy()
    w, ben, mc = p.w.to_numpy(), p.ss_benefit.to_numpy(), (p.MCARE == 1).to_numpy()
    groups = {**{GEN[g]: p[g].to_numpy() for g in UNION}, "union": p.union.to_numpy(), "white": p[WHITE].to_numpy()}
    rows = []
    for name, m in groups.items():
        m = m & old
        rec = ben[m] > 0
        rows.append(dict(group=name, persons=int(m.sum()), population_m=w[m].sum() / 1e6,
                         receiving_share=(w[m] * rec).sum() / w[m].sum(),
                         benefit_per_recipient=(w[m] * ben[m])[rec].sum() / w[m][rec].sum(),
                         medicare_share=(w[m] * mc[m]).sum() / w[m].sum()))
    return pd.DataFrame(rows)


def coverage_check(lines: pd.DataFrame, se_oasdi_share: float) -> dict:
    """The case's national OASDI receipts against the Trustees' 2024 net payroll tax contributions: the case is
    already on the Trustees' covered base, so the 09-18 lane's coverage scale (CPS / Trustees) has no role in a
    ratio applied to the case's own OASDI taxes."""
    x = lines[(lines.method == lines.method.iloc[0]) & (lines.end == "low")].set_index("line").national_bn
    nat = float(x.employee_oasdi + x.employer_oasdi + SE_OASDI / (SE_OASDI + SE_HI) * x.self_employment_oasdi_hi)
    tr = S.value("tr_oasdi_payroll_tax_2024_bn")
    return dict(case_national_oasdi_bn=nat, trustees_net_payroll_tax_2024_bn=tr, ratio=nat / tr,
                group_se_oasdi_share=se_oasdi_share)


def steady_state_case(comp: pd.DataFrame, st: pd.DataFrame) -> pd.DataFrame:
    """The group's 2024 OASDI and Part A cash balance on the case's lines at each age structure: benefits x
    (factor - 1) less taxes x (factor - 1), the two methods averaged. Part A scales with Medicare coverage by age
    band (no cost gradient within a band)."""
    f = st.pivot_table(index="structure", columns="flow", values="factor")
    rows = []
    for end in ["low", "high"]:
        c = comp[comp.end == end]
        tax, ben = float(c.oasdi_tax_bn.mean()), float(c.ss_benefits_bn.mean())
        hi_tax, part_a = float(c.hi_tax_bn.mean()), float(c.part_a_bn.mean())
        for s in [x for x in f.index if x != "own"]:
            d_o = ben * (f.loc[s, "ss_benefit"] - 1) - tax * (f.loc[s, "oasdi_tax"] - 1)
            d_h = part_a * (f.loc[s, "medicare_covered"] - 1) - hi_tax * (f.loc[s, "hi_tax"] - 1)
            rows.append(dict(structure=s, end=end, delta_oasdi_bn=d_o, delta_part_a_bn=d_h, delta_bn=d_o + d_h))
    return pd.DataFrame(rows)


# ------------------------------------------------------------------ gates on inputs and the model
def gate_inputs() -> dict:
    """The Note 2025.7 parser equals the 09-18 lane's; case.json is current and its costs reproduce the case."""
    mine, theirs = S.mwr_table(1), ss.parse_mwr()
    if not mine.reset_index(drop=True).equals(theirs[mine.columns].reset_index(drop=True)):
        blocked("sources.mwr_table(1) differs from the 09-18 lane's parse_mwr()")
    case = json.loads((OUT / "case.json").read_text())
    if not all(case["gates"].values()):
        blocked(f"case.json gates {case['gates']}")
    root = FISCAL.parents[1]
    stale = [f["file"] for f in case["frozen_files"]
             if hashlib.sha256((root / f["file"]).read_bytes()).hexdigest() != f["sha256"]]
    if stale:
        blocked(f"case.json predates changes to {stale}; rerun case_lines.cjs")
    for end in ["low", "high"]:
        got = np.mean([r["cost_bn"] for r in case["per_method"] if r["end"] == end])
        if not near(got, case["case_bn"][end]):
            blocked(f"case.json per-method costs give {got} at {end}, not {case['case_bn'][end]}")
    print(f"[gate 2] case.json current ({len(case['frozen_files'])} frozen files); the case "
          f"{case['case_bn']['low']:.4f} / {case['case_bn']['high']:.4f}bn; Note 2025.7 parser = the 09-18 lane's")
    return case


def gate_model(grid: dict, econ, prelim) -> dict:
    """The factor is 1 on Note 2025.7's basis (EAN, trust-fund rates, entry 21), and EAN, PUC and ABO each add up
    to the lifetime present value of benefits."""
    n = 64
    fam = np.array(grid["fams"] * (n // len(grid["fams"])))
    rng = np.linspace(0, 1, n)
    birth = BIRTHS[0] + rng * (BIRTHS[-1] - BIRTHS[0])
    level = np.exp(np.log(MODEL_LEVELS[0]) + rng[::-1] * np.log(MODEL_LEVELS[-1] / MODEL_LEVELS[0]))
    age = np.clip(2024 - birth, 21, 74)
    f = model_factor(grid, "EAN", BASE, fam, np.full(n, 21.0), birth, level, age)
    if np.abs(f - 1).max() > 1e-12:
        blocked(f"the EAN factor on Note 2025.7's basis is not 1 (max gap {np.abs(f - 1).max():.2e})")
    worst = 0.0
    for fam_i in L.FAMILY_SEXES:
        for b, adj, entry, g in ((1964, 1.221, 21, BASE), (1985, 0.549, 33, ("0.03", "general")),
                                 (2000, 1.953, 45, ("new_issue", "hispanic"))):
            rate = float(g[0]) if g[0][0].isdigit() else g[0]
            w = L.worker(b, adj, entry, fam_i, econ, prelim, arm=rate, population=g[1])
            for m in ("EAN", "PUC", "ABO"):
                worst = max(worst, abs(w["acc"][m].sum() / w["pv_ben"] - 1))
    if worst > 1e-9:
        blocked(f"accruals do not add up to lifetime benefits (worst {worst:.2e})")
    print(f"[gate 4] model factor = 1 on Note 2025.7's basis; EAN/PUC/ABO add up to lifetime benefits (worst {worst:.1e})")
    return dict(factor_one_max_gap=float(np.abs(f - 1).max()), adding_up_worst=worst)


def summarize(beside, st_case, arms, hi, hi_info, v, t, union_row, case, gates, p) -> dict:
    """The central, the range across the one-change arms, and every combination of the non-bridge settings
    (MARG, which does not add up, and r = g, a bridge, left out)."""
    cand = beside[~beside.bridge]
    cen = beside[beside.arm == "central"].set_index("end")
    rng = {end: dict(min=float(g.case_on_accrual_bn.min()), max=float(g.case_on_accrual_bn.max()),
                     min_arm=g.loc[g.case_on_accrual_bn.idxmin(), "arm"], max_arm=g.loc[g.case_on_accrual_bn.idxmax(), "arm"])
           for end, g in cand.groupby("end")}
    fact = arms[(arms.group == "union") & (arms.method != "MARG") & (arms.rate != "awi")]
    hfact = hi[(hi.group == "union") & (hi.rate != "awi")]
    env = {}
    for end in ["low", "high"]:
        c = cen.loc[end]
        base = c.case_bn - c.ss_benefits_removed_bn - c.part_a_removed_bn
        env[end] = dict(min=float(base + fact.per_tax_dollar.min() * c.oasdi_tax_bn + hfact.accrual_bn.min()),
                        max=float(base + fact.per_tax_dollar.max() * c.oasdi_tax_bn + hfact.accrual_bn.max()),
                        per_tax_dollar=[float(fact.per_tax_dollar.min()), float(fact.per_tax_dollar.max())],
                        part_a_accrual_bn=[float(hfact.accrual_bn.min()), float(hfact.accrual_bn.max())])
    return dict(
        case_bn=case["case_bn"], ends=case["ends"],
        central=CENTRAL,
        central_on_accrual_bn={e: float(cen.loc[e, "case_on_accrual_bn"]) for e in ["low", "high"]},
        central_decomposition={e: {k: float(cen.loc[e, k]) for k in
                                   ["oasdi_tax_bn", "accrual_per_tax_dollar", "oasdi_accrual_bn", "ss_benefits_removed_bn",
                                    "delta_oasdi_bn", "hi_tax_bn", "part_a_accrual_bn", "part_a_removed_bn",
                                    "delta_part_a_bn", "delta_bn"]} for e in ["low", "high"]},
        range_across_arms_bn=rng,
        every_combination_bn=env,
        steady_state_bn={f"{r.structure}_{r.end}": dict(delta_oasdi_bn=r.delta_oasdi_bn, delta_part_a_bn=r.delta_part_a_bn,
                                                         delta_bn=r.delta_bn) for r in st_case.itertuples()},
        oasdi_per_tax_dollar_central_by_generation={g: float(pick(arms, CENTRAL, OASDI_KEYS, g).per_tax_dollar)
                                                    for g in ["union", "G1", "G2", "G3plus"]},
        part_a=hi_info,
        unauthorized=dict(onbooks_share_mexico_born=p.attrs["s_mex"],
                          note151_long_run=CENTRAL["unauthorized"] == "note151_long_run"),
        model_checks=dict(v_c7_max_gap_points=float(v.gap_pp.abs().max()),
                          model_over_note_table1=[float(t.model_over_note.min()), float(t.model_over_note.max())],
                          payable_haircut_max_gap=float((t.model_payable_over_scheduled - t.note_payable_over_scheduled).abs().max())),
        gate_union_row=union_row, gates=gates,
    )


def main() -> None:
    OUT.mkdir(exist_ok=True)
    q = S.quotes()
    union_row = gate_union_row()
    case = gate_inputs()
    p = frame()
    econ = L.Economy()
    prelim = S.scaled_factors().preliminary.to_numpy()
    v, t = validate_model(econ, prelim)
    print(f"[gate 3] benefit formula vs TR V.C7 (64 cells): max gap {v.gap_pp.abs().max():.3f} points; model / Note "
          f"2025.7 Table 1: {t.model_over_note.min():.3f}-{t.model_over_note.max():.3f}; payable haircut gap "
          f"{(t.model_payable_over_scheduled - t.note_payable_over_scheduled).abs().max():.3f}")
    grid = model_grid(econ, prelim)
    gates = dict(model=gate_model(grid, econ, prelim), quotes_verified=len(q))
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    u_2000 = q["note151_eligible_share"]["value"]["age62_in_2000"]
    arms = oasdi_arms(p, grid, u_long, u_2000)
    hi, hi_info = hi_accrual(p, econ, u_long, u_2000)
    st, st_info = steady_state(p)
    comp = case_components(p)
    beside = case_beside(comp, arms, hi, case)
    st_case = steady_state_case(comp, st)
    named = []
    for name in ARMS:
        spec = arm_spec(name, "low")
        for g in ["union", "G1", "G2", "G3plus"]:
            r = pick(arms, spec, OASDI_KEYS, g)
            named.append(dict(arm=name, group=g, tax_bn=r.tax_bn, accrual_bn=r.accrual_bn, per_tax_dollar=r.per_tax_dollar))
    union = arms[arms.group == "union"].drop(columns="group")
    union.to_csv(OUT / "oasdi_arms.csv", index=False, float_format="%.6f", lineterminator="\n")
    pd.DataFrame(named).to_csv(OUT / "oasdi_by_generation.csv", index=False, float_format="%.6f", lineterminator="\n")
    hi.to_csv(OUT / "hi_arms.csv", index=False, float_format="%.6f", lineterminator="\n")
    st.to_csv(OUT / "steady_state.csv", index=False, float_format="%.6f", lineterminator="\n")
    st_case.to_csv(OUT / "steady_state_case.csv", index=False, float_format="%.6f", lineterminator="\n")
    comp.to_csv(OUT / "case_components.csv", index=False, float_format="%.6f", lineterminator="\n")
    beside.to_csv(OUT / "case_beside.csv", index=False, float_format="%.6f", lineterminator="\n")
    v.to_csv(OUT / "model_check_v_c7.csv", index=False, float_format="%.4f", lineterminator="\n")
    t.to_csv(OUT / "model_check_mwr.csv", index=False, float_format="%.4f", lineterminator="\n")
    summary = summarize(beside, st_case, arms, hi, hi_info, v, t, union_row, case, gates, p)
    summary["steady_state_structures"] = st_info
    summary["case_components_attrs"] = comp.attrs
    summary["coverage_check"] = coverage_check(pd.read_csv(OUT / "case_lines.csv"), comp.attrs["se_oasdi_share"])
    er = elderly_receipt(p)
    er.to_csv(OUT / "elderly_receipt.csv", index=False, float_format="%.6f", lineterminator="\n")
    summary["elderly_receipt"] = er.set_index("group").to_dict(orient="index")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True, default=float) + "\n")
    (OUT / "gate_union_row.json").write_text(json.dumps(union_row, indent=1, sort_keys=True) + "\n")
    (OUT / "sources.json").write_text(json.dumps(dict(documents=S.provenance(), quotes=sorted(q)), indent=1,
                                                 sort_keys=True) + "\n")
    pd.set_option("display.width", 250)
    show = beside[["arm", "end", "accrual_per_tax_dollar", "delta_oasdi_bn", "part_a_accrual_bn", "delta_part_a_bn",
                   "case_on_accrual_bn"]]
    print(show.pivot_table(index="arm", columns="end", values=["accrual_per_tax_dollar", "delta_oasdi_bn",
                                                              "delta_part_a_bn", "case_on_accrual_bn"], sort=False).round(2).to_string())
    print(st_case.round(2).to_string(index=False))
    print(f"[written] {', '.join(sorted(x.name for x in OUT.iterdir()))}")


if __name__ == "__main__":
    main()
