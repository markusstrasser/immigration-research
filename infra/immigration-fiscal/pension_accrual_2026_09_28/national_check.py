"""National check: the lane's machinery against the Statement of Social Insurance (SOSI) at 1 January 2025.

The parent's check of 2026-09-28 (after commit bec1cd7): apply the lane's accrual machinery to the whole covered
population in the CPS frame, on the SOSI's basis (the trust funds' effective rates, the 75 years 2025-2099,
scheduled benefits), and compare with the SOSI's closed-group rows:
  OASDI  current participants aged 15-61 at the valuation date, and those 62 and over;
  HI     current participants aged 15-64, and those 65 and over;
each the present value at 1 January 2025 of future expenditures and of future non-interest income.

The prediction (derived/national_prediction.csv) was written into RESULT.md before the published rows were opened.

OASDI 15-61, the ratio route. A person's lifetime OASDI taxes (taxes paid through 2024, accumulated at the trust
funds' rates, plus expected taxes 2025-2099) earn benefits at the lane's per-tax-dollar ratio: Note 2025.7 Table 1
through the individual age-adjusted level, the observed family, careers from arrival for the foreign-born, and the
model factor at trust-fund rates; unauthorized workers are on the books at the case's shares and credited at Note
151's 10%. The lifetime model then scales lifetime benefits to those paid in 2025-2099 to a person alive in 2025.
Taxes come from a pseudo-cohort: 2024 covered earnings by single year of age, sex and nativity (zeros included)
moved along cohort lines with the AWI, the OASDI rate of each past year, NVSS 2024 survival improved at the TR's
rates, and the trust funds' rates; the foreign-born from arrival. Each cell (nativity x sex x five-year band) takes
the tax-weighted mean ratio of its 2024 taxpayers. The formula route uses the lifetime model's own ratio instead.

OASDI 62 and over. 2024 Social Security benefits (CPS) as annuities: Table V.C1's COLAs, the same survival and
rates, 2025-2099; the survivor's step-up between linked spouses who both collect; and for those 62-69 not yet
collecting, the receipt share and benefit of 67-74-year-olds of the same sex and nativity, claimed at 67 (70 if
already 67). Income is future payroll tax (the same pseudo-cohort) plus the taxation of benefits at Tables
IV.B1/IV.B2's ratio of that income to cost, year by year, on each row's own benefits.

HI 15-64: the lane's Part A machinery (P(qualify) by nativity and sex x the PV of Part A from 65, unauthorized at
10%). HI 65 and over: current enrollees' Part A cost from 2025 at the average cost per beneficiary (no age
gradient). HI income: 2.9% payroll tax on the same pseudo-cohort, plus the HI share of the tax on benefits (its
2024 ratio to the OASDI share, Tables II.B1 of both reports).

Primary: each 2024 cash flow scaled to its Trustees total (OASDI payroll tax and benefits, HI payroll tax, HI
enrollment); the CPS frame as it is, beside. Present values at 2024 (the lane's basis) move to 1 January 2025 by
half a year at the 2024 trust-fund rate.

Score (after the freeze): the script stops unless derived/national_prediction.csv is byte-for-byte the file frozen in
RESULT.md, then scores it against the published rows (SSA's FY 2025 AFR for OASDI, CMS's FY 2025 Financial Report
for HI) on the declared tolerance: each ratio within 10%, each level within 15%; OASDI passes on its 15-61 row, HI
on its 15-64 row. Probes of the 15-61 ratio route and of the group's accrual per tax dollar at the central settings
on scheduled benefits (the lane's arm `scheduled`; its central is on payable benefits since 2026-09-28): levels shrunk
toward their cell's mean log level (the parent's convexity question), and one-earner couples priced as two-earner
couples (no spousal benefit, a bound on auxiliaries). The level distribution of 55-61-year-old taxpayers is set
beside Note 2025.3 Table 1. The Part A spouse check counts one-earner spouses with covered earnings of their own in
2024 and values the sex mix of the own term. Also: where the formula route's shortfall sits (age row, age band and,
through the model-worker check, benefit type), and the benefits earned by 2024 against OCACT's maximum transition
cost at 1 January 2025.

Run from the repository root, after pension_accrual.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/pension_accrual_2026_09_28/national_check.py
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
sys.path.insert(0, str(HERE))

import pension_accrual as pa  # noqa: E402  the lane: frame, levels, Note 2025.7 ratios, model factor, Part A
import lifetime_model as L  # noqa: E402
import sources as S  # noqa: E402

ss, ca = pa.ss, pa.ca
OUT = pa.OUT
BASE_YEAR, LAST_YEAR = 2024, 2099     # PVs at 2024 on the lane's basis; the SOSI's 75 years end in 2099
SPLIT = {"oasdi": 62, "hi": 65}       # eligibility ages that split current participants
FIRST_AGE, MAX_AGE = 15, 99           # SOSI participants are 15 and over; the spread of the 85+ code ends at 99
TOP_CODES = {80: range(80, 85), 85: range(85, MAX_AGE + 1)}   # CPS ASEC 2025 ages 80 (80-84) and 85 (85+)
MEDIUM = L.LEVEL_ADJ["medium"]
YEARS = np.arange(L.Y0, L.Y1 + 1)
# the prediction as frozen in RESULT.md (2026-09-28 10:03 JST) before any published row was opened
FROZEN_SHA256 = "b8b5c3f5ae9315a0a9a48ada1732d917c971df45edf51d68111bbfed469ed7d9"
TOLERANCE = dict(ratio=0.10, level=0.15)        # declared with the prediction
GATING = dict(oasdi="oasdi_15_61", hi="hi_15_64")
CENTRAL_G = (pa.CENTRAL["rate"], pa.CENTRAL["mortality"])
THETAS = [0.8, 0.6]                             # probe: the share of within-cell log-level variance kept


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


# ------------------------------------------------------------------ the national frame
def national_frame() -> pd.DataFrame:
    """The lane's frame with the case's status rules applied to every foreign-born person: unauthorized workers on
    the books at the case's shares (Mexico-born s_mex, others s_oth), careers from arrival for the foreign-born."""
    p = pa.frame()
    split = pd.read_csv(pa.ONBOOKS_FILE).set_index("kind")
    s_mex, s_oth = (float(split.loc["evidence_central", k]) for k in ("s_mex", "s_oth"))
    p["foreign"] = p.PRCITSHP.isin([4, 5]).to_numpy()
    p["unauth"] = p.unauth_state_aware.astype(bool).to_numpy() & p.foreign.to_numpy()
    p["onbooks"] = np.where(p.unauth & p.mexico_born, s_mex, np.where(p.unauth, s_oth, 1.0))
    p["tax_oasdi"] = (p.oasdi_wage + p.oasdi_se) * p.onbooks
    p["tax_hi"] = (2 * 0.0145 * p.wage + p.hi_se) * p.onbooks
    mid = p.PEINUSYR.map(pa.entry_midpoints())
    p["arrival_age"] = np.where(p.foreign & mid.notna(), p.age - (2024.5 - mid), np.nan)
    if p.foreign.to_numpy()[np.isnan(p.arrival_age.to_numpy())].any():
        blocked("foreign-born persons without a year of entry")
    p["nat"] = np.where(p.foreign, "foreign", "native")
    p.attrs.update(s_mex=s_mex, s_oth=s_oth)
    return p


def spread_top_codes(p: pd.DataFrame) -> pd.DataFrame:
    """Records coded 80 or 85 become one record per single year of age, weighted by the NVSS 2024 person-years of
    their sex (a stationary spread within the code)."""
    keep = p[~p.age.isin(list(TOP_CODES))]
    parts = [keep.assign(age_exact=keep.age.to_numpy())]
    for code, ages in TOP_CODES.items():
        sub = p[p.age == code]
        for sex, name in ((1, "male"), (2, "female")):
            q = L.qx_table("general", name)
            lx = np.cumprod(np.concatenate([[1.0], 1 - q[:-1]]))
            person_years = (lx[:-1] + lx[1:]) / 2
            share = person_years[list(ages)] / person_years[list(ages)].sum()
            s = sub[sub.sex == sex]
            for a, f in zip(ages, share):
                parts.append(s.assign(age_exact=a, w=s.w.to_numpy() * f))
    out = pd.concat(parts, ignore_index=True)
    if not np.isclose(out.w.sum(), p.w.sum(), rtol=1e-12):
        blocked("the top-code spread does not keep the weight")
    return out


# ------------------------------------------------------------------ year paths
class Paths:
    """Per-year factors over 1900-2200 (index = year - 1900) and survival tables by sex and 2024 age."""

    def __init__(self, econ: L.Economy):
        self.econ = econ
        self.disc = econ.discount("tf")          # to 2024; past years accumulate
        k = BASE_YEAR - L.Y0
        self.to_valuation = float((1 + econ.tf_nominal[k]) ** 0.5)   # mid-2024 to 1 January 2025
        self.awi_rel = econ.awi / econ.awi[k]
        self.cola_factor = np.ones(len(YEARS))   # benefit in year y per $1 of 2024 benefit
        for y in range(BASE_YEAR + 1, L.Y1 + 1):
            self.cola_factor[y - L.Y0] = self.cola_factor[y - 1 - L.Y0] * (1 + econ.cola[y - 1 - L.Y0])
        rates = S.oasdi_rates_iv_b()
        by_year = lambda v: pd.Series(v.to_numpy(), index=rates.year.to_numpy()).reindex(YEARS).interpolate(
            limit_area="inside").ffill().bfill().to_numpy()
        self.tob_share = pa.tob_share_path()     # the lane's one definition; the net switch reads the same path
        # payroll tax income per 12.4% of taxable payroll, 2025 on (Table IV.B2: 12.23% in 2025, 12.38% later)
        self.payroll_rate = np.where(YEARS > BASE_YEAR, by_year(rates.payroll_rate / 12.4), 1.0)
        self.in_window = ((YEARS > BASE_YEAR) & (YEARS <= LAST_YEAR)).astype(float)
        self._surv = {}

    def survival(self, sex: int, age: int) -> np.ndarray:
        """P(alive at mid-age in year y | alive at the start of age + 1, i.e. 1 January 2025), by year index."""
        key = (sex, age)
        if key not in self._surv:
            b = BASE_YEAR - age
            s = L.survival(b, "general", "male" if sex == 1 else "female", age + 1)
            out = np.zeros(len(YEARS))
            out[b - L.Y0: b - L.Y0 + 121] = s
            self._surv[key] = out
        return self._surv[key]


# ------------------------------------------------------------------ pseudo-cohort taxes
def tax_profiles(p: pd.DataFrame, col: str) -> dict:
    """Mean 2024 tax per person by (nativity, sex) and CPS age 15-85, zeros included."""
    out = {}
    for nat in ("native", "foreign"):
        for sex in (1, 2):
            m = (p.nat == nat).to_numpy() & (p.sex == sex).to_numpy()
            g = pd.DataFrame({"a": p.age.to_numpy()[m], "w": p.w.to_numpy()[m], "t": p[col].to_numpy()[m] * p.w.to_numpy()[m]})
            s = g.groupby("a")[["w", "t"]].sum()
            prof = (s.t / s.w).reindex(range(0, 86))
            if prof.loc[list(range(FIRST_AGE, 81)) + [85]].isna().any():
                blocked(f"no CPS persons at some ages for {nat} {sex}")
            out[(nat, sex)] = prof.fillna(0.0).to_numpy()
    return out


def age_code(ages: np.ndarray) -> np.ndarray:
    """CPS age codes for exact ages: 80-84 read the 80 code, 85 and over the 85 code."""
    return np.where(ages >= 85, 85, np.where(ages >= 80, 80, ages))


def future_taxes(prof: np.ndarray, sex: int, age: int, paths: Paths, oasdi: bool = True) -> np.ndarray:
    """PVs at 2024 of expected taxes 2025-2099 by the person's age (index 0-120), for this sex and 2024 age; OASDI
    at Table IV.B2's payroll tax income per 12.4% of taxable payroll."""
    ages = age + np.arange(1, LAST_YEAR - BASE_YEAR + 1)
    ages = ages[ages <= MAX_AGE]
    yi = BASE_YEAR - age + ages - L.Y0
    out = np.zeros(121)
    out[ages] = prof[age_code(ages)] * paths.awi_rel[yi] * paths.survival(sex, age)[yi] * paths.disc[yi] * \
        (paths.payroll_rate[yi] if oasdi else 1.0)
    return out


def past_taxes(prof: np.ndarray, age: int, arrival: float, paths: Paths, econ: L.Economy) -> np.ndarray:
    """Taxes paid at ages 15 to `age` (years through 2024) by age, accumulated to 2024 at the trust funds' rates;
    the foreign-born only after arrival (the year of arrival prorated); past years at that year's OASDI rate."""
    ages = np.arange(FIRST_AGE, age + 1)
    yi = BASE_YEAR - (age - ages) - L.Y0
    frac = np.clip(ages + 1 - arrival, 0.0, 1.0) if np.isfinite(arrival) else np.ones(len(ages))
    rate = np.nan_to_num(econ.tax[yi]) / 0.124
    out = np.zeros(121)
    out[ages] = prof[age_code(ages)] * paths.awi_rel[yi] * rate * paths.disc[yi] * frac
    return out


# ------------------------------------------------------------------ the lifetime model on the base run
def base_grid(econ, prelim) -> dict:
    """The lane's model grid on Note 2025.7's own basis only (trust-fund rates, general mortality): EAN per-tax
    factors and lifetime ratios over family, career start, birth year and level, as pa.model_grid builds them."""
    fams = list(L.FAMILY_SEXES)
    shape = (len(fams), len(pa.ENTRIES), len(pa.BIRTHS), len(pa.MODEL_LEVELS))
    k = np.full(shape + (121,), np.nan)
    mwr = np.full(shape, np.nan)
    adj = [L.LEVEL_ADJ[x] for x in ["very_low", "low", "medium", "high"]]
    for fi, fam in enumerate(fams):
        for ei, entry in enumerate(pa.ENTRIES):
            for bi, b in enumerate(pa.BIRTHS):
                for li, a in enumerate(adj):
                    w = L.worker(b, a, entry, fam, econ, prelim, arm=pa.BASE[0], population=pa.BASE[1])
                    mwr[fi, ei, bi, li] = w["mwr"]
                    k[fi, ei, bi, li] = w["per_tax"]["EAN"]
    return dict(k={"EAN": {pa.BASE: k}}, mwr={pa.BASE: mwr}, fams=fams)


def entry_index(entry: np.ndarray) -> np.ndarray:
    ent = np.array(pa.ENTRIES)
    return np.clip(np.searchsorted(ent, np.maximum(entry, 21), side="right") - 1, 0, len(ent) - 1)


def model_mwr(grid: dict, fam: np.ndarray, entry: np.ndarray, birth: np.ndarray, level: np.ndarray) -> np.ndarray:
    """The lifetime model's own ratio at each person's family, career start, birth year and level, interpolated
    as pa.model_factor interpolates its numerator."""
    fi = np.array([grid["fams"].index(f) for f in fam])
    ei = entry_index(entry)
    bj, bw = pa.interp_weights(birth, np.array(pa.BIRTHS, float))
    lj, lw = pa.interp_weights(level, pa.MODEL_LEVELS, log=True)
    mm = grid["mwr"][pa.BASE]
    out = np.zeros(len(fi))
    for db, wb in ((0, 1 - bw), (1, bw)):
        for dl, wl in ((0, 1 - lw), (1, lw)):
            out += wb * wl * mm[fi, ei, bj + db, lj + dl]
    return out


def window_grid(econ, prelim, paths: Paths) -> dict:
    """For a medium-level unit of each family, 2024 age 15-61 and career start on the entry grid: the ratio of
    benefits paid 2025-2099 to a unit alive on 1 January 2025 over (its lifetime ratio x its taxes paid plus
    expected), and the benefit-weighted share of taxation-of-benefits income over those years."""
    fams = list(L.FAMILY_SEXES)
    ages = list(range(FIRST_AGE, SPLIT["oasdi"]))
    adj = np.full((len(fams), len(ages), len(pa.ENTRIES)), np.nan)
    tob = np.full_like(adj, np.nan)
    for fi, fam in enumerate(fams):
        for ai, a in enumerate(ages):
            b = BASE_YEAR - a
            for ei, entry in enumerate(pa.ENTRIES):
                if entry > max(a + 1, 21):
                    continue
                life = L.worker(b, MEDIUM, entry, fam, econ, prelim, arm="tf")
                if life["pv_ben"] == 0:      # a career too short to vest earns nothing whatever the timing
                    adj[fi, ai, ei], tob[fi, ai, ei] = 1.0, 0.0
                    continue
                now = L.worker(b, MEDIUM, entry, fam, econ, prelim, arm="tf", alive_at=a + 1, last_year=LAST_YEAR)
                adj[fi, ai, ei] = now["pv_ben"] / (life["mwr"] * now["pv_tax"])
                share = econ.at(paths.tob_share, b)
                tob[fi, ai, ei] = float((now["ben_pv_by_age"] * share).sum() / now["pv_ben"])
    return dict(adj=adj, tob=tob, fams=fams, ages=ages)


# ------------------------------------------------------------------ OASDI 15-61
COHORTS = [BASE_YEAR - a for a in range(FIRST_AGE, SPLIT["oasdi"])]


def family_for(q: pd.DataFrame, family: str) -> np.ndarray:
    """The lane's observed family; "no_spouse_benefit" prices one-earner couples as two-earner couples."""
    fam = ss.family_vector(q, "observed_family")
    if family == "no_spouse_benefit":
        return np.where(fam == "one_earner_couple", "two_earner_couple", fam).astype(object)
    if family != "observed":
        raise ValueError(family)
    return fam


def shrink(level: np.ndarray, q: pd.DataFrame, theta: float, keys: list[str]) -> np.ndarray:
    """Levels with their log pulled toward the person-weighted mean log level of their cell by theta, the share of
    the within-cell variance kept as permanent; theta = 1 returns them unchanged."""
    if theta == 1.0:
        return level
    x = np.log(level)
    d = q[keys].copy()
    d["xw"], d["wt"] = x * q.w.to_numpy(), q.w.to_numpy()
    s = d.groupby(keys)[["xw", "wt"]].transform("sum")
    m = (s.xw / s.wt).to_numpy()
    return np.exp(m + theta * (x - m))


def ratio_tables(p, grid, u_long, theta: float = 1.0, family: str = "observed") -> tuple[dict, dict]:
    """The lane's per-tax-dollar ratio for today's taxpayers aged 15 and over, re-evaluated at each birth cohort of
    the 15-61 row: z[route][(nativity, sex)] is an (86 CPS ages x cohorts) table of tax-weighted means. The ratio
    route is Note 2025.7 Table 1 x the model factor (careers from arrival) x the unauthorized credit; the formula
    route is the lifetime model's own ratio x the credit. Returns the tables and the national per-tax-dollar ratios
    of 2024's taxpayers at their own cohorts. `theta` and `family` are the probes' changes (1 and "observed" leave
    the lane as it is)."""
    q = p[(p.age >= FIRST_AGE).to_numpy() & (p.tax_oasdi > 0).to_numpy()].reset_index(drop=True)
    fam = family_for(q, family)
    level = shrink(pa.career_levels(q, "individual_age_adjusted"), q, theta, ["age", "sex", "nat"])
    lvl = np.clip(level, pa.MODEL_LEVELS[0], pa.MODEL_LEVELS[-1])
    entry = np.where(q.foreign, np.nan_to_num(q.arrival_age.to_numpy(), nan=21.0), 21.0)
    credit = np.where(q.unauth, u_long, 1.0)
    wt = q.w.to_numpy() * q.tax_oasdi.to_numpy()
    ages = q.age.to_numpy()
    t1 = S.mwr_table(1)
    own_birth = np.clip(ss.INCOME_YEAR - ages, pa.BIRTHS[0], pa.BIRTHS[-1]).astype(float)
    lane = pa.note_mwr(q, t1, level, fam) * pa.model_factor(grid, "EAN", pa.BASE, fam, entry, own_birth, lvl,
                                                            ages.astype(float))
    own_lane = model_mwr(grid, fam, entry, own_birth, lvl)

    def at_cohort(b: int) -> tuple[np.ndarray, np.ndarray]:
        note = np.zeros(len(q))
        for f in ss.FAMILY:
            m = fam == f
            note[m] = ss.mwr_interpolate(t1, f, np.full(int(m.sum()), float(b)), level[m])
        bm = np.full(len(q), float(np.clip(b, pa.BIRTHS[0], pa.BIRTHS[-1])))
        own = model_mwr(grid, fam, entry, bm, lvl)
        return note * own / model_mwr(grid, fam, np.full(len(q), 21.0), bm, lvl), own

    z = {"ratio": {}, "formula": {}}
    keys = [(n, s) for n in ("native", "foreign") for s in (1, 2)]
    for route in z:
        for key in keys:
            z[route][key] = np.zeros((86, len(COHORTS)))
    worst = 0.0
    cells = [(n, s, (q.nat == n).to_numpy() & (q.sex == s).to_numpy()) for n, s in keys]
    for ci, b in enumerate(COHORTS):
        ratio, own = at_cohort(b)
        mine = (ss.INCOME_YEAR - ages) == b
        worst = max(worst, float(np.abs(ratio[mine] - lane[mine]).max(initial=0.0)),
                    float(np.abs(own[mine] - own_lane[mine]).max(initial=0.0)))
        for n, s, m in cells:
            den = np.bincount(ages[m], weights=wt[m], minlength=86)
            for route, v in (("ratio", ratio), ("formula", own)):
                num = np.bincount(ages[m], weights=wt[m] * v[m] * credit[m], minlength=86)
                z[route][(n, s)][:, ci] = np.divide(num, den, out=np.zeros(86), where=den > 0)
    if worst > 1e-12:
        blocked(f"the re-evaluated ratio at a taxpayer's own cohort differs from the lane's by {worst:.2e}")
    info = dict(taxpayers=int(len(q)),
                national_per_tax_dollar_ratio_route=float((wt * lane * credit).sum() / wt.sum()),
                national_per_tax_dollar_formula_route=float((wt * own_lane * credit).sum() / wt.sum()),
                own_cohort_gate_max_gap=worst)
    return z, info


def oasdi_working_age(p, grid, wgrid, paths, econ, u_long, theta: float = 1.0,
                      family: str = "observed") -> tuple[pd.DataFrame, dict]:
    """Per group of persons 15-61 (nativity x sex x age x arrival): the PVs of taxes paid and expected by age,
    each year's taxes earning the ratio today's taxpayers of that age carry, re-evaluated at the group's birth
    cohort (the lane's per-year accrual summed over the career); benefits then scaled by the window factor of each
    person's family and career start, and the tax on benefits by the model's timing."""
    prof = tax_profiles(p, "tax_oasdi")
    z, info = ratio_tables(p, grid, u_long, theta, family)
    x = p[p.age.between(FIRST_AGE, SPLIT["oasdi"] - 1)].reset_index(drop=True)
    fam = ss.family_vector(x, "observed_family")
    entry = np.where(x.foreign, np.nan_to_num(x.arrival_age.to_numpy(), nan=21.0), 21.0)
    fi = np.array([wgrid["fams"].index(f) for f in fam])
    adj = wgrid["adj"][fi, x.age.to_numpy() - FIRST_AGE, entry_index(entry)]
    tobw = wgrid["tob"][fi, x.age.to_numpy() - FIRST_AGE, entry_index(entry)]
    if np.isnan(adj).any():
        blocked("window grid has no value for some persons")
    x = x.assign(arr=np.where(x.foreign, x.arrival_age.round(3), -1.0), adj_w=x.w * adj, tob_w=x.w * adj * tobw)
    groups = x.groupby(["nat", "sex", "age", "arr"])[["w", "adj_w", "tob_w"]].sum()
    code = age_code(np.arange(121))
    rows = []
    for (nat, sex, a, arr), g in groups.iterrows():
        pr = prof[(nat, sex)]
        past = past_taxes(pr, a, arr if arr >= 0 else np.nan, paths, econ)
        fut = future_taxes(pr, sex, a, paths)
        ci = COHORTS.index(BASE_YEAR - a)
        row = dict(nat=nat, sex=sex, age=a, arrival=arr, w=g.w, past=g.w * past.sum(), future=g.w * fut.sum(),
                   adj=g.adj_w / g.w)
        for route in ("ratio", "formula"):
            zz = z[route][(nat, sex)][code, ci]
            earned = float((zz * (past + fut)).sum())
            row[f"ben_{route}"] = g.adj_w * earned
            row[f"tob_{route}"] = g.tob_w * earned
            row[f"ratio_{route}"] = earned / (past + fut).sum() if (past + fut).sum() > 0 else 0.0
            row[f"past_ben_{route}"] = g.adj_w * float((zz * past).sum())   # EAN: benefits earned by 2024
        rows.append(row)
    t = pd.DataFrame(rows)
    info.update(window_factor_person_weighted=float(np.average(adj, weights=x.w)))
    return t, info


# ------------------------------------------------------------------ OASDI 62 and over, HI
def spouse_links(p: pd.DataFrame) -> np.ndarray:
    """Row index of each person's spouse in p (-1 if none), from the CPS A_SPOUSE line number."""
    cd, _ = ca.load()
    sp = p[["PH_SEQ", "A_LINENO"]].merge(cd[["PH_SEQ", "A_LINENO", "A_SPOUSE"]], on=["PH_SEQ", "A_LINENO"],
                                          how="left", validate="one_to_one")
    pos = pd.Series(np.arange(len(p)), index=pd.MultiIndex.from_arrays([p.PH_SEQ.to_numpy(), p.A_LINENO.to_numpy()]))
    key = pd.MultiIndex.from_arrays([sp.PH_SEQ.to_numpy(), sp.A_SPOUSE.fillna(0).astype(int).to_numpy()])
    out = pos.reindex(key).fillna(-1).astype(int).to_numpy().copy()
    out[sp.A_SPOUSE.fillna(0).to_numpy() <= 0] = -1
    return out


def annuity(paths: Paths, sex: int, age: int, from_age: int | None = None) -> np.ndarray:
    """Per-year PV at 2024 of $1 of 2024 benefit with COLAs, paid from `from_age` (default next year) to 2099."""
    s = paths.survival(sex, age)
    start = BASE_YEAR - age + (from_age if from_age is not None else age + 1) - L.Y0
    out = paths.cola_factor * s * paths.disc * paths.in_window
    out[:start] = 0.0
    return out


def oasdi_older(p, x, paths, u_long) -> tuple[dict, pd.DataFrame]:
    """OASDI benefits of current participants 62 and over (x: the frame with top codes spread), by person-year
    PV arrays summed: annuities of 2024 benefits, the survivor step-up of linked collecting couples, and future
    claims of those 62-69 not collecting. Returns totals and the per-year benefit PV for the tax on benefits."""
    old = x[x.age_exact >= SPLIT["oasdi"]]
    per_year = np.zeros(len(YEARS))
    for (sex, a), g in old.assign(bw=old.w * old.ss_benefit).groupby(["sex", "age_exact"]):
        per_year += g.bw.sum() * annuity(paths, sex, a)
    annuities = float(per_year.sum())
    # survivor step-up: both spouses 62+ and collecting, linked in the CPS (top-coded ages at 82 and 88); the
    # survivor keeps the larger benefit; deaths independent
    link = spouse_links(p)
    i = np.flatnonzero((p.age.to_numpy() >= SPLIT["oasdi"]) & (p.ss_benefit.to_numpy() > 0) & (link >= 0))
    j = link[i]
    ok = (p.age.to_numpy()[j] >= SPLIT["oasdi"]) & (p.ss_benefit.to_numpy()[j] > 0) & \
        (p.ss_benefit.to_numpy()[j] > p.ss_benefit.to_numpy()[i])
    i, j = i[ok], j[ok]
    step = np.zeros(len(YEARS))
    code_age = {80: 82, 85: 88}
    for pi, pj in zip(i, j):
        s1 = paths.survival(int(p.sex.iat[pi]), code_age.get(int(p.age.iat[pi]), int(p.age.iat[pi])))
        s2 = paths.survival(int(p.sex.iat[pj]), code_age.get(int(p.age.iat[pj]), int(p.age.iat[pj])))
        gain = p.ss_benefit.iat[pj] - p.ss_benefit.iat[pi]
        step += p.w.iat[pi] * gain * s1 * (1 - s2) * paths.cola_factor * paths.disc * paths.in_window
    per_year += step
    # future claims of those 62-69 not collecting in 2024
    claims = np.zeros(len(YEARS))
    for (nat, sex), g in x.groupby(["nat", "sex"]):
        at = lambda lo, hi: g[(g.age_exact >= lo) & (g.age_exact <= hi)]
        ref = at(67, 74)
        eventual = float(np.average(ref.ss_benefit > 0, weights=ref.w))
        level = float(np.average(ref.ss_benefit[ref.ss_benefit > 0], weights=ref.w[ref.ss_benefit > 0]))
        for a in range(SPLIT["oasdi"], 70):
            ga = at(a, a)
            r_a = float(np.average(ga.ss_benefit > 0, weights=ga.w))
            p_claim = max(0.0, (eventual - r_a) / (1 - r_a))
            non = ga[ga.ss_benefit <= 0]
            credit = np.where(non.unauth, np.minimum(p_claim, u_long), p_claim)
            claims += float((non.w * credit).sum()) * level * annuity(paths, sex, a, from_age=67 if a < 67 else 70)
    per_year += claims
    return dict(annuities=annuities, survivor_step_up=float(step.sum()), future_claims=float(claims.sum()),
                linked_couples=int(len(i)), total=float(per_year.sum())), per_year


def part_a_rows(p, x, econ, paths, u_long: float, k_aged: float) -> dict:
    """HI 15-64: P(qualify) (lawful 65+ with Medicare, by nativity and sex; unauthorized x Note 151's share) x the
    PV of Part A from 65; HI 65+: enrollees' Part A cost from 2025; both to 2099. `young_scaled` takes P(qualify)
    times the Trustees' aged enrollment over the CPS count (at most 1). Also the disabled enrollees' cost before
    65 (a named item the lane's machinery leaves out)."""
    pq = {}
    for nat in ("native", "foreign"):
        for sex in (1, 2):
            m = (x.nat == nat) & (x.sex == sex) & (x.age_exact >= 65) & ~x.unauth
            pq[(nat, sex)] = float(np.average((x.MCARE[m] == 1), weights=x.w[m]))
    young = x[(x.age_exact >= FIRST_AGE) & (x.age_exact < SPLIT["hi"])]
    base_pq = np.array([pq[(n, s)] for n, s in zip(young.nat, young.sex)])
    credit = np.where(young.unauth, u_long, 1.0)
    pv_young = pa.part_a_pv(young.age_exact.to_numpy(), young.sex.to_numpy(), econ, "tf", "scheduled",
                            alive_next=True, last_year=LAST_YEAR)
    olds = x[x.age_exact >= SPLIT["hi"]]
    enrolled = (olds.MCARE == 1).to_numpy()
    pv_old = pa.part_a_pv(olds.age_exact.to_numpy(), olds.sex.to_numpy(), econ, "tf", "scheduled",
                          alive_next=True, last_year=LAST_YEAR)
    # disabled enrollees under 65: the average cost per beneficiary until 65
    cost = np.nan_to_num(pa.hi_cost_path(econ)) * paths.in_window
    dis = young[(young.MCARE == 1).to_numpy()]
    pv_dis = 0.0
    for r in dis[["sex", "age_exact", "w"]].itertuples(index=False):
        s = paths.survival(r.sex, r.age_exact)
        yrs = (YEARS <= BASE_YEAR - r.age_exact + 64)
        pv_dis += r.w * float((cost * s * paths.disc * yrs).sum())
    wy = young.w.to_numpy() * credit * pv_young
    return dict(p_qualify={f"{n}_{'men' if s == 1 else 'women'}": v for (n, s), v in pq.items()},
                young=float((wy * base_pq).sum()), young_scaled=float((wy * np.minimum(base_pq * k_aged, 1.0)).sum()),
                old=float((olds.w.to_numpy() * enrolled * pv_old).sum()),
                disabled_under_65=pv_dis,
                enrolled_65plus_m=float(olds.w[enrolled].sum() / 1e6),
                enrolled_under65_m=float(dis.w.sum() / 1e6))


# ------------------------------------------------------------------ the score (after the freeze)
def published_rows() -> dict:
    """The SOSI's closed-group rows at 1 January 2025, $tn: expenditures (OASDI cost) and non-interest income."""
    o, h = S.sosi_oasdi()["rows"], S.sosi_hi()["rows"]
    tn = lambda e, i: dict(expenditures_tn=e / 1e3, income_tn=i / 1e3)
    return {"oasdi_15_61": tn(o["15_61"]["cost"], o["15_61"]["income"]),
            "oasdi_62_plus": tn(o["62_plus"]["cost"], o["62_plus"]["income"]),
            "hi_15_64": tn(h["15_64"]["expenditures"], h["15_64"]["income"]),
            "hi_65_plus": tn(h["65_plus"]["expenditures"], h["65_plus"]["income"])}


def score(pub: dict) -> tuple[pd.DataFrame, dict]:
    """Each predicted row against the published one on the declared tolerance; stops unless the prediction file is
    the one frozen in RESULT.md."""
    got = hashlib.sha256((OUT / "national_prediction.csv").read_bytes()).hexdigest()
    if got != FROZEN_SHA256:
        blocked(f"derived/national_prediction.csv (sha256 {got[:12]}) is not the prediction frozen before scoring")
    pred = pd.read_csv(OUT / "national_prediction.csv")
    rows = []
    for r in pred.itertuples(index=False):
        pb = pub[r.row]
        for measure, mine, theirs, tol in (
                ("expenditures", r.expenditures_tn, pb["expenditures_tn"], TOLERANCE["level"]),
                ("income", r.income_tn, pb["income_tn"], TOLERANCE["level"]),
                ("ratio", r.ratio, pb["expenditures_tn"] / pb["income_tn"], TOLERANCE["ratio"])):
            rows.append(dict(variant=r.variant, route=r.route, row=r.row, measure=measure, predicted=mine,
                             published=theirs, gap=mine / theirs - 1, tolerance=tol,
                             passes=bool(abs(mine / theirs - 1) <= tol),
                             gating=bool(r.variant == "trustees_scaled" and r.route == "ratio" and r.row in GATING.values())))
    t = pd.DataFrame(rows)

    def ok(row: str, route: str = "ratio") -> bool:
        return bool(t[(t.variant == "trustees_scaled") & (t.route == route) & (t.row == row)].passes.all())

    verdict = dict(oasdi=ok(GATING["oasdi"]), hi=ok(GATING["hi"]), formula_route_oasdi_15_61=ok("oasdi_15_61", "formula"),
                   beside_oasdi_62_plus=ok("oasdi_62_plus"), beside_hi_65_plus=ok("hi_65_plus"))
    return t, verdict


def central_mapping(t: pd.DataFrame, cen: dict) -> dict:
    """The declared rule: if the 15-61 income passes and its ratio misses, the lane's accrual per tax dollar scales
    by published over predicted ratio; if the 15-64 expenditures miss, the Part A accrual scales by published over
    predicted. Both scalings are shown whether or not the rule applies."""
    get = lambda row, m: t[(t.variant == "trustees_scaled") & (t.route == "ratio") & (t.row == row) & (t.measure == m)].iloc[0]
    r, inc, e = get("oasdi_15_61", "ratio"), get("oasdi_15_61", "income"), get("hi_15_64", "expenditures")
    so, sh = r.published / r.predicted, e.published / e.predicted
    d = cen["central_decomposition"]
    return dict(
        oasdi=dict(rule_applies=bool(inc.passes and not r.passes), scale=so,
                   per_tax_dollar=d["low"]["accrual_per_tax_dollar"],
                   per_tax_dollar_if_scaled=d["low"]["accrual_per_tax_dollar"] * so,
                   change_if_scaled_bn={e_: d[e_]["oasdi_accrual_bn"] * (so - 1) for e_ in ("low", "high")}),
        part_a=dict(rule_applies=bool(not e.passes), scale=sh, accrual_bn=d["low"]["part_a_accrual_bn"],
                    accrual_if_scaled_bn=d["low"]["part_a_accrual_bn"] * sh,
                    change_if_scaled_bn=d["low"]["part_a_accrual_bn"] * (sh - 1)))


def central_grid(grid: dict, econ, prelim) -> dict:
    """The base grid plus the EAN factors and lifetime ratios of the lane's central run (its rate and mortality), as
    pa.model_grid builds them: what pa.model_factor needs for the group's central accrual per tax dollar."""
    shape = grid["mwr"][pa.BASE].shape
    k, mwr = np.full(shape + (121,), np.nan), np.full(shape, np.nan)
    adj = [L.LEVEL_ADJ[x] for x in ["very_low", "low", "medium", "high"]]
    for fi, fam in enumerate(grid["fams"]):
        for ei, entry in enumerate(pa.ENTRIES):
            for bi, b in enumerate(pa.BIRTHS):
                for li, a in enumerate(adj):
                    w = L.worker(b, a, entry, fam, econ, prelim, arm=CENTRAL_G[0], population=CENTRAL_G[1])
                    mwr[fi, ei, bi, li] = w["mwr"]
                    k[fi, ei, bi, li] = w["per_tax"][pa.CENTRAL["method"]]
    return dict(k={pa.CENTRAL["method"]: {**grid["k"]["EAN"], CENTRAL_G: k}}, mwr={**grid["mwr"], CENTRAL_G: mwr},
                fams=grid["fams"])


def group_ratio(p: pd.DataFrame, cgrid: dict, u_long: float, theta: float = 1.0, family: str = "observed") -> float:
    """The lane's accrual per dollar of the group's on-books OASDI tax at the central settings on scheduled benefits
    (pension_accrual.oasdi_arms, the arm `scheduled`: this check's basis; the lane's central is on payable benefits
    since 2026-09-28), with a probe's levels (shrunk within generation x age x sex) or family."""
    q = p[p.union.to_numpy() & (p.tax_oasdi > 0).to_numpy()].reset_index(drop=True)
    fam = family_for(q, family)
    level = shrink(pa.career_levels(q, pa.CENTRAL["mapping"]), q, theta, ["age", "sex", "gen"])
    lvl = np.clip(level, pa.MODEL_LEVELS[0], pa.MODEL_LEVELS[-1])
    birth = np.clip(ss.INCOME_YEAR - q.age.to_numpy(), pa.BIRTHS[0], pa.BIRTHS[-1]).astype(float)
    entry = np.where(q.mexico_born & q.arrival_age.notna(), q.arrival_age.fillna(21), 21.0)
    fac = pa.model_factor(cgrid, pa.CENTRAL["method"], CENTRAL_G, fam, entry, birth, lvl, q.age.to_numpy().astype(float))
    tax, w = q.tax_oasdi.to_numpy(), q.w.to_numpy()
    acc = tax * pa.note_mwr(q, S.mwr_table(1), level, fam) * fac * np.where(q.unauth.to_numpy(), u_long, 1.0)
    return float((w * acc).sum() / (w * tax).sum())


def level_check(p: pd.DataFrame) -> pd.DataFrame:
    """The lane's age-adjusted levels of 2024 taxpayers aged 55-61 (persons) beside Note 2025.3 Table 1 (workers
    retiring in 2019-2024): the share below each hypothetical worker's career-average earnings, men, women and all;
    and the share of all 15-61 taxpayers' OASDI tax below each level."""
    t1 = S.aime_distribution()
    cut = t1.career_average.to_numpy() * pa.MEDIUM_CAREER / float(t1.set_index("level").career_average["Medium"])
    q = p[(p.tax_oasdi > 0).to_numpy() & p.age.between(FIRST_AGE, SPLIT["oasdi"] - 1).to_numpy()]
    level = pa.career_levels(q, "individual_age_adjusted")
    w, tw = q.w.to_numpy(), q.w.to_numpy() * q.tax_oasdi.to_numpy()
    old = q.age.between(55, 61).to_numpy()
    rows = []
    for i, r in enumerate(t1.itertuples(index=False)):
        below = level < cut[i]
        share = lambda m, wt=w: float(100 * wt[m & below].sum() / wt[m].sum())
        rows.append(dict(level=r.level, cut=cut[i], below_all_table1=r.below_all,
                         below_all_lane=share(old), below_men_table1=r.below_men,
                         below_men_lane=share(old & (q.sex == 1).to_numpy()), below_women_table1=r.below_women,
                         below_women_lane=share(old & (q.sex == 2).to_numpy()),
                         tax_below_15_61_lane=share(np.ones(len(q), bool), tw)))
    return pd.DataFrame(rows)


def formula_gap(cells: pd.DataFrame, pub: dict, scale: float) -> dict:
    """Where the formula route's shortfall sits. By age row: the formula model enters only the 15-61 row, whose gap
    to the published cost splits into the formula route's distance from the ratio route (the benefits the model
    leaves out) and the ratio route's own gap. By age band within 15-61: the formula route's cost over the ratio
    route's. By benefit type: the model-worker check (derived/model_check_mwr.csv, pension_accrual.py) by family;
    Note 2025.7 gives single workers no children, so their shortfall is disability benefits and the
    earnings-graded mortality and disability incidence, and couples add children's and young survivors' benefits
    net of the family maximum."""
    band = pd.cut(cells.age, [FIRST_AGE - 1, 24, 34, 44, 54, SPLIT["oasdi"] - 1],
                  labels=["15-24", "25-34", "35-44", "45-54", "55-61"])
    g = cells.groupby(band, observed=True)[["ben_ratio", "ben_formula"]].sum()
    mwr = pd.read_csv(OUT / "model_check_mwr.csv")
    ratio_tn, formula_tn = (float(cells[c].sum()) * scale for c in ("ben_ratio", "ben_formula"))
    return dict(row_15_61=dict(published_tn=pub["oasdi_15_61"]["expenditures_tn"], ratio_route_tn=ratio_tn,
                               formula_route_tn=formula_tn, left_out_benefits_tn=ratio_tn - formula_tn,
                               common_to_both_routes_tn=pub["oasdi_15_61"]["expenditures_tn"] - ratio_tn),
                row_62_plus="the formula model is not used: both routes value CPS benefits as annuities",
                formula_over_ratio_by_age={str(b): float(r.ben_formula / r.ben_ratio) for b, r in g.iterrows()},
                model_over_note_by_family=mwr.groupby("family").model_over_note.mean().to_dict())


def stock_check(cells: pd.DataFrame, pub: dict, older: dict, tob_older: float, k: dict, cost_load: float,
                v: float, q: dict) -> dict:
    """Benefits earned by 1 January 2025 against OCACT's maximum transition cost (Note 2025.1 Table 3). The MTC is
    the present value of accrued benefit obligations less the reserves and the tax on those benefits. With the
    62+ row's published cost (less the lane's cost loading) as their accrued obligations, it implies the 15-61
    accrued obligations; each stream's tax on benefits is the prediction's own share. The lane's figure is the
    ratio route's past taxes x their ratio (entry-age normal); OCACT prorates a wage-indexed PIA as if disabled
    today by (age - 22) / 40."""
    mtc = q["note2025_1_transition_costs_2025"]["value"]["maximum_transition_cost_tn"]
    reserves = S.sosi_oasdi()["reserves"] / 1e3
    t_young = float(cells.tob_ratio.sum() / cells.ben_ratio.sum())
    t_old = tob_older / older["total"]
    old = pub["oasdi_62_plus"]["expenditures_tn"] / cost_load
    implied = (mtc + reserves - old * (1 - t_old)) / (1 - t_young)
    lane = float(cells.past_ben_ratio.sum()) * k["oasdi_tax"] * v / 1e12
    return dict(maximum_transition_cost_tn=mtc, reserves_tn=reserves, accrued_62_plus_tn=old,
                tob_share_62_plus=t_old, tob_share_15_61=t_young, implied_accrued_15_61_tn=implied,
                lane_ean_accrued_15_61_tn=lane, lane_over_implied=lane / implied,
                lane_ean_accrued_15_61_formula_route_tn=float(cells.past_ben_formula.sum()) * k["oasdi_tax"] * v / 1e12)


def spouse_check(p: pd.DataFrame, econ, u_long: float, u_2000: float) -> dict:
    """Step d, on the group's Part A accrual (pa.hi_accrual at the central settings on scheduled benefits, the arm
    `scheduled`). In 2024: covered workers flagged as
    one-earner couples (spouse without wages) whose spouse has covered self-employment earnings, and the spouse
    credit they carry (the accrual with those spouses counted as earners, less the lane's). Over a career the own
    term alone sums to every member's Part A (pa.hi_accrual's docstring), so the whole credit is a second count.
    Also the own term at the generation's sex mix instead of the worker's own sex."""
    link = spouse_links(p)
    sp = np.maximum(link, 0)
    earns = (link >= 0) & (p.tax_hi.to_numpy()[sp] > 0) & (p.spouse_wage.to_numpy() <= 0)
    alt = p.copy()
    alt["spouse_wage"] = np.where(earns, p.se.to_numpy()[sp], p.spouse_wage.to_numpy())
    pick = lambda h, spouse: float(pa.pick(h, {**pa.CENTRAL, "scenario": "scheduled", "spouse": spouse}, pa.HI_KEYS).accrual_bn)
    lane = pa.hi_accrual(p, econ, u_long, u_2000)[0]
    alt_on = pick(pa.hi_accrual(alt, econ, u_long, u_2000)[0], True)
    mix = pick(pa.hi_accrual(p, econ, u_long, u_2000, own_value="sex_mix")[0], False)
    u = p.union.to_numpy() & (p.tax_hi > 0).to_numpy() & (p.age < 65).to_numpy()
    one = u & p.married.to_numpy() & (p.spouse_wage.to_numpy() <= 0)
    w = p.w.to_numpy()
    on, off = pick(lane, True), pick(lane, False)
    return dict(one_earner_covered_workers_m=float(w[one].sum() / 1e6),
                spouse_self_employed_m=float(w[one & earns].sum() / 1e6),
                spouse_self_employed_share=float(w[one & earns].sum() / w[one].sum()),
                accrual_with_credit_bn=on, accrual_without_credit_bn=off, credit_bn=on - off,
                credit_share_of_own_term=(on - off) / off,
                credit_on_self_employed_spouses_bn=on - alt_on,
                accrual_sex_mix_bn=mix, sex_mix_minus_own_sex_bn=mix - off)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    q = S.quotes()
    u_long = q["note151_eligible_share"]["value"]["end_of_projection"]
    econ = L.Economy()
    prelim = S.scaled_factors().preliminary.to_numpy()
    paths = Paths(econ)
    p = national_frame()
    x = spread_top_codes(p[p.age >= FIRST_AGE])
    a3 = S.combined_operations_vi_a3().set_index("year").loc[2024]
    hi24 = q["mtr_hi_2024_operations"]["value"]
    w = p.w.to_numpy()
    # OASDI taxes scale to 12.4% of the Trustees' 2024 taxable payroll: 2024's payroll tax income ($1,293.3bn,
    # 12.77% of payroll in Table IV.B2) carries adjustments for prior years
    k = dict(oasdi_tax=0.124 * q["tr_taxable_payroll_2024_bn"]["value"] / ((w * p.tax_oasdi).sum() / 1e9),
             oasdi_benefits=a3.benefits / ((w * p.ss_benefit).sum() / 1e9),
             hi_tax=hi24["payroll_taxes_bn"] / ((w * p.tax_hi).sum() / 1e9),
             hi_aged=hi24["enrollment_aged_m"] / (w[(p.age >= 65).to_numpy() & (p.MCARE == 1).to_numpy()].sum() / 1e6),
             hi_disabled=hi24["enrollment_disabled_m"] / (w[(p.age < 65).to_numpy() & (p.MCARE == 1).to_numpy()].sum() / 1e6))
    cost_load = a3.cost / a3.benefits
    hi_load = hi24["total_expenditures_bn"] / hi24["benefits_bn"]
    kappa = pa.hi_over_oasdi_tob()
    print(f"[frame] {len(p)} persons, {p.w.sum() / 1e6:.2f}m; scale to Trustees 2024: " +
          ", ".join(f"{a} {b:.4f}" for a, b in k.items()))
    grid = base_grid(econ, prelim)
    wgrid = window_grid(econ, prelim, paths)
    # the net switch's timing weights (pension_accrual.tob_timing) are window_grid's: on this check's basis (trust-fund
    # rates, benefits to 2099, careers from 21) they reproduce its tax-on-benefits share at every shared cohort
    tt = pa.tob_timing(econ, prelim, paths.tob_share, runs=[(pa.BASE, "scheduled")], last_year=LAST_YEAR)[(pa.BASE, "scheduled")]
    cohorts = [(bi, BASE_YEAR - b) for bi, b in enumerate(pa.BIRTHS) if FIRST_AGE <= BASE_YEAR - b < SPLIT["oasdi"]]
    gap = max(float(np.abs(tt[:, bi] - wgrid["tob"][:, a - FIRST_AGE, 0]).max()) for bi, a in cohorts)
    if gap > 1e-12:
        blocked(f"pension_accrual.tob_timing misses window_grid's tax-on-benefits share by {gap:.2e}")
    print(f"[gate] tob_timing = window_grid on {len(cohorts)} cohorts (max gap {gap:.1e})")
    cells, info = oasdi_working_age(p, grid, wgrid, paths, econ, u_long)
    print(f"[15-61] {info['taxpayers']} taxpayers; national per tax dollar: ratio route "
          f"{info['national_per_tax_dollar_ratio_route']:.4f}, formula route {info['national_per_tax_dollar_formula_route']:.4f}")
    older, older_per_year = oasdi_older(p, x, paths, u_long)
    hi_prof = tax_profiles(p, "tax_hi")
    oasdi_prof = tax_profiles(p, "tax_oasdi")
    fut = {"oasdi_older": 0.0, "hi_young": 0.0, "hi_old": 0.0}
    g = x.groupby(["nat", "sex", "age_exact"]).w.sum()
    for (nat, sex, a), wt in g.items():
        a = int(a)
        if a >= SPLIT["oasdi"]:
            fut["oasdi_older"] += wt * future_taxes(oasdi_prof[(nat, sex)], sex, a, paths).sum()
        fut["hi_young" if a < SPLIT["hi"] else "hi_old"] += wt * future_taxes(hi_prof[(nat, sex)], sex, a, paths,
                                                                               oasdi=False).sum()
    hi = part_a_rows(p, x, econ, paths, u_long, k["hi_aged"])
    # the tax on benefits: 15-61 by the model's timing; 62+ by the annuities' years; HI's share at kappa
    tob_62_64 = 0.0
    for (sex, a), g in x[(x.age_exact >= SPLIT["oasdi"]) & (x.age_exact < SPLIT["hi"])].groupby(["sex", "age_exact"]):
        tob_62_64 += float((g.w * g.ss_benefit).sum()) * float((annuity(paths, sex, a) * paths.tob_share).sum())
    tob_older = float((older_per_year * paths.tob_share).sum())
    rows = []
    v = paths.to_valuation
    for variant in ("trustees_scaled", "cps_frame"):
        kk = k if variant == "trustees_scaled" else {c: 1.0 for c in k}
        for route in ("ratio", "formula"):
            ben_young = float(cells[f"ben_{route}"].sum()) * kk["oasdi_tax"]
            tob_young = float(cells[f"tob_{route}"].sum()) * kk["oasdi_tax"]
            fut_young = float(cells.future.sum()) * kk["oasdi_tax"]
            ben_old = older["total"] * kk["oasdi_benefits"]
            tob_old = tob_older * kk["oasdi_benefits"]
            fut_old = fut["oasdi_older"] * kk["oasdi_tax"]
            tob_hi_young = kappa * (tob_young + tob_62_64 * kk["oasdi_benefits"])
            tob_hi_old = kappa * (tob_old - tob_62_64 * kk["oasdi_benefits"])
            for row, exp_, inc in (
                    ("oasdi_15_61", ben_young * cost_load, fut_young + tob_young),
                    ("oasdi_62_plus", ben_old * cost_load, fut_old + tob_old),
                    ("hi_15_64", (hi["young_scaled"] if variant == "trustees_scaled" else hi["young"]) * hi_load,
                     fut["hi_young"] * kk["hi_tax"] + tob_hi_young),
                    ("hi_65_plus", hi["old"] * kk["hi_aged"] * hi_load, fut["hi_old"] * kk["hi_tax"] + tob_hi_old)):
                if route == "formula" and not row.startswith("oasdi_15"):
                    continue
                rows.append(dict(variant=variant, route=route, row=row, expenditures_tn=exp_ * v / 1e12,
                                 income_tn=inc * v / 1e12, net_tn=(inc - exp_) * v / 1e12, ratio=exp_ / inc))
    pred = pd.DataFrame(rows)
    pred.to_csv(OUT / "national_prediction.csv", index=False, float_format="%.6f", lineterminator="\n")
    detail = dict(
        calibration=k, cost_loading=cost_load, hi_cost_loading=hi_load, kappa_hi_over_oasdi_tob=kappa,
        to_valuation_factor=v, oasdi_15_61=dict(info, persons_m=float(cells.w.sum() / 1e6),
                                                  past_taxes_tn=float(cells.past.sum() * v / 1e12),
                                                  future_taxes_tn=float(cells.future.sum() * v / 1e12)),
        oasdi_62_plus={c: (val * v / 1e12 if isinstance(val, float) else val) for c, val in older.items()},
        oasdi_62_plus_future_taxes_tn=fut["oasdi_older"] * v / 1e12,
        hi=dict({c: (val * v / 1e12 if c in ("young", "young_scaled", "old", "disabled_under_65") else val)
                 for c, val in hi.items()}, future_taxes_young_tn=fut["hi_young"] * v / 1e12,
                future_taxes_old_tn=fut["hi_old"] * v / 1e12,
                disabled_under_65_scaled_tn=hi["disabled_under_65"] * k["hi_disabled"] * hi_load * v / 1e12),
        units="$tn at 1 January 2025 unless named otherwise; *_m millions")
    (OUT / "national_prediction.json").write_text(json.dumps(detail, indent=1, sort_keys=True, default=float) + "\n")
    cells.to_csv(OUT / "national_cells.csv", index=False, float_format="%.6f", lineterminator="\n")
    pd.set_option("display.width", 200)
    print(pred.round(4).to_string(index=False))
    print(json.dumps(detail, indent=1, default=float)[:3000])

    # ---- the score, after the freeze: nothing above reads the published rows
    pub = published_rows()
    t, verdict = score(pub)
    cen = json.loads((OUT / "summary.json").read_text())
    mapping = central_mapping(t, cen)
    sched = cen["scheduled_arm"]["decomposition"]["low"]   # the probes' comparator, on this check's scheduled basis
    pg = pa.frame()                      # the group exactly as pension_accrual.py builds it
    cgrid = central_grid(grid, econ, prelim)
    lane_ratio = group_ratio(pg, cgrid, u_long)
    if abs(lane_ratio - sched["accrual_per_tax_dollar"]) > 1e-12:
        blocked(f"the probe's group ratio {lane_ratio} does not reproduce the lane's scheduled arm")
    lane_row = pred[(pred.variant == "trustees_scaled") & (pred.route == "ratio") & (pred.row == "oasdi_15_61")].iloc[0]
    r_pub = pub["oasdi_15_61"]["expenditures_tn"] / pub["oasdi_15_61"]["income_tn"]
    probes = []
    for theta, family in [(1.0, "observed")] + [(th, "observed") for th in THETAS] + [(1.0, "no_spouse_benefit")]:
        c = cells if (theta, family) == (1.0, "observed") else \
            oasdi_working_age(p, grid, wgrid, paths, econ, u_long, theta, family)[0]
        exp_ = float(c.ben_ratio.sum()) * k["oasdi_tax"] * cost_load * v / 1e12
        inc = (float(c.future.sum()) + float(c.tob_ratio.sum())) * k["oasdi_tax"] * v / 1e12
        probes.append(dict(theta=theta, family=family, expenditures_tn=exp_, income_tn=inc, ratio=exp_ / inc,
                           ratio_gap_to_published=exp_ / inc / r_pub - 1,
                           group_per_tax_dollar=group_ratio(pg, cgrid, u_long, theta, family)))
    probes = pd.DataFrame(probes)
    if abs(probes.expenditures_tn.iloc[0] / lane_row.expenditures_tn - 1) > 1e-9:
        blocked("the probes' lane row does not reproduce the frozen 15-61 prediction")
    probes["group_change_vs_lane"] = probes.group_per_tax_dollar / lane_ratio - 1
    levels = level_check(p)
    spouse = spouse_check(pg, econ, u_long, q["note151_eligible_share"]["value"]["age62_in_2000"])
    if abs(spouse["accrual_without_credit_bn"] - sched["part_a_accrual_bn"]) > 1e-9:
        blocked("the spouse check's accrual without the credit is not the lane's scheduled Part A accrual")
    gap = formula_gap(cells, pub, k["oasdi_tax"] * cost_load * v / 1e12)
    stock = stock_check(cells, pub, older, tob_older, k, cost_load, v, q)
    t.to_csv(OUT / "national_score.csv", index=False, float_format="%.6f", lineterminator="\n")
    probes.to_csv(OUT / "national_probes.csv", index=False, float_format="%.6f", lineterminator="\n")
    levels.to_csv(OUT / "national_levels.csv", index=False, float_format="%.4f", lineterminator="\n")
    out = dict(frozen_prediction_sha256=FROZEN_SHA256, tolerance=TOLERANCE, gating_rows=GATING, published_tn=pub,
               published_sources=dict(oasdi=S.DOCS["ssa_afr2025"]["title"], hi=S.DOCS["cms_fr2025"]["title"]),
               verdict=verdict, central_mapping=mapping, part_a_spouse_check=spouse, formula_gap=gap, stock_check=stock,
               probes_note="15-61 ratio route and the group's central accrual per tax dollar; theta < 1 shrinks log "
                           "levels toward the cell mean, no_spouse_benefit prices one-earner couples as two-earner")
    (OUT / "national_score.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=float) + "\n")
    print(t[t.variant == "trustees_scaled"].round(4).to_string(index=False))
    print(json.dumps(dict(verdict=verdict, central_mapping=mapping, part_a_spouse_check=spouse, formula_gap=gap,
                          stock_check=stock), indent=1, default=float))
    print(probes.round(4).to_string(index=False))
    print(levels.round(2).to_string(index=False))


if __name__ == "__main__":
    main()
