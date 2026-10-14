"""P7 cohort incidence proxies; read-only imports and no output writes.

Keys are per-person densities: sum(pw * key) == 1 over other residents.
Multiply a signed component by its living_share before allocating on its key.
Every trust component uses the SAME key/share. This is an explicitly degraded
projection, not observed incidence or an estimate of legislative responses.
"""
from __future__ import annotations

import hashlib
import importlib
from pathlib import Path
import re
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
SSA = ROOT / "sources/immigration-fiscal/data/external/stage3/ssa/trustees_2026/tr2026.txt"


def population_path(path=SSA):
    """Parse historical + intermediate V.A3, interpolate annual broad ages."""
    text = Path(path).read_text()
    first = text.index("Table V.A3.—Social Security Area Population on July 1")
    block = text[first:text.index("Low-cost:", first)]
    pattern = re.compile(r"^\s*(\d{4})[a-z]?\s+[.\s]+"
                         r"([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+", re.M)
    rows = [(int(m[1]), *[float(m[k].replace(",", "")) * 1000 for k in range(2, 6)])
            for m in pattern.finditer(block)]
    t = pd.DataFrame(rows, columns=["year", "under20", "age20_64", "age65plus", "total"])
    if t.year.duplicated().any() or not {2024, 2025, 2030, 2100}.issubset(set(t.year)):
        raise ValueError("[BLOCKED] SSA V.A3 historical/intermediate parser coverage")
    if np.max(abs(t.under20 + t.age20_64 + t.age65plus - t.total)) > 1000:
        raise ValueError("[BLOCKED] SSA population broad ages do not close to printed total")
    return t.set_index("year").reindex(range(2024, 2101)).interpolate().reset_index()


def _profile(age, sex, pw, other, values):
    """Five-year age/sex means, zeros included, interpolated between cells."""
    profile = np.zeros((2, 121))
    rows = []
    for s in (1, 2):
        knots, means = [], []
        for lo in range(0, 86, 5):
            m = other & (sex == s) & (age >= lo) & (age < lo + 5)
            if np.sum(pw[m]) <= 0:
                continue
            center = float(np.average(age[m], weights=pw[m]))
            mean = float(np.average(values[m], weights=pw[m]))
            knots.append(center)
            means.append(mean)
            rows.append(dict(sex=s, age_lo=lo, population=float(pw[m].sum()),
                             age_center=center, mean=mean))
        if not knots:
            raise ValueError("[BLOCKED] no age/sex profile observations")
        profile[s - 1] = np.interp(np.arange(121), knots, means)
        profile[s - 1, 100:] = 0
    return profile, rows


def _survival(L, age, sex, years, decline):
    """Survival from mid-2024, NVSS qx improved by Trustees calendar year."""
    a = age + years - 2024
    qx = L.qx_table("general", "male" if sex == 1 else "female")
    q = qx[np.clip(a, 0, 120)] * (1 - np.where(a >= 65, decline["65plus"],
                                             decline["total"])) ** (years - 2024)
    q[a >= 100] = 1
    start = np.cumprod(np.r_[1., 1 - q[:-1]])
    return start * (1 - q / 2) / (1 - q[0] / 2)


def cohort_keys(d, wl, trust_totals, group_weights=None):
    """Return keys, living shares, year/profile tables, pins, proxies and gates.

    d is the live winners frame (pw, other, target, A_AGE, A_SEX, FICA,
    FEDTAX_AC; SS_VAL read from aligned primary CPS if absent). trust_totals maps arbitrary trust component names to
    signed dollar totals. Names borrowing10/borrowing30 use the debt keys;
    all other supplied components use the common trust key. No totals are
    inferred from an old case. wl is accepted for the caller's integration.
    """
    need = {"pw", "other", "target", "A_AGE", "A_SEX", "FICA", "FEDTAX_AC"}
    if not need.issubset(d.columns):
        raise ValueError(f"[BLOCKED] cohort frame missing {sorted(need-set(d.columns))}")
    sys.dont_write_bytecode = True
    previous_path = sys.path[:]
    sys.path.insert(0, str(FISCAL / "pension_tr2026_2026_10_06"))
    try:
        pt = importlib.import_module("pension_tr2026")
    finally:
        sys.path[:] = previous_path
    L, S = pt.L, pt.S
    primary_quotes = pt.T.quotes()  # verifies primary hashes and verbatim anchors
    pop = population_path()
    years = pop.year.to_numpy(int)
    pw = d.pw.to_numpy(float)
    age = d.A_AGE.to_numpy(int)
    sex = d.A_SEX.to_numpy(int)
    other, target = d.other.to_numpy(bool), d.target.to_numpy(bool)
    if (pw < 0).any() or not np.isin(sex, [1, 2]).all() or not ((age >= 0) & (age < 100)).all():
        raise ValueError("[BLOCKED] invalid cohort age/sex/weights")
    tax = d.FEDTAX_AC.clip(lower=0).to_numpy(float) + d.FICA.clip(lower=0).to_numpy(float)
    cps_path = None
    if "SS_VAL" in d:
        benefits = d.SS_VAL.clip(lower=0).to_numpy(float)
    else:
        # Base distribution does not stage this column; align exact person ids.
        cps_path = Path(wl.load_base()[0].PATHS["cps"])
        with zipfile.ZipFile(cps_path) as z:
            receipts = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "SS_VAL"])
        if not np.array_equal(receipts[["PH_SEQ", "PPPOS"]].to_numpy(),
                              d[["PH_SEQ", "PPPOS"]].to_numpy()):
            raise ValueError("[BLOCKED] cohort Social Security records not aligned")
        benefits = receipts.SS_VAL.clip(lower=0).to_numpy(float)
    tax_profile, tax_rows = _profile(age, sex, pw, other, tax)
    benefit_profile, benefit_rows = _profile(age, sex, pw, other, benefits)
    benefit_profile[:, :65] = 0  # retirement-only incidence proxy, not all OASDI beneficiaries
    decline = primary_quotes["tr2026_mortality_decline"]["value"]
    econ = pt.economy_2026(rates=True, wages=True, parameters=True)
    paths = pd.read_csv(FISCAL / "pension_tr2026_2026_10_06/derived/paths.csv").set_index("year")
    oasi = np.ones(len(pt.YEARS))
    hi_pay = np.ones(len(pt.YEARS))
    for y in paths.index:
        oasi[y - L.Y0] = paths.loc[y, "oasi_2026"]
        hi_pay[y - L.Y0] = paths.loc[y, "hi_2026"]
    # Published last-year shares held after 2100, only to quantify tail mass.
    oasi[2101 - L.Y0:] = oasi[2100 - L.Y0]
    hi_pay[2101 - L.Y0:] = hi_pay[2100 - L.Y0]
    prelim = S.scaled_factors().preliminary.to_numpy()
    hi_cost = pt.hi_cost_path_tr2026(econ)
    disc = econ.discount(pt.G[0])
    payout = np.zeros(len(years))
    tail = 0.
    workers = target & (age >= 21) & (age < 65) & (d.FICA.to_numpy(float) > 0)
    group_weights=pw if group_weights is None else np.asarray(group_weights,float)
    if group_weights.shape!=pw.shape or (group_weights<0).any():
        raise ValueError("[BLOCKED] invalid group payout weights")
    workers_w = group_weights * np.maximum(d.FICA.to_numpy(float), 0)
    workers_total = float(workers_w[workers].sum())
    if workers_total <= 0:
        raise ValueError("[BLOCKED] target workers have no payroll proxy mass")
    hi_fraction = float(trust_totals.get("hi_payout_fraction", 0.25))
    if not 0 <= hi_fraction <= 1:
        raise ValueError("[BLOCKED] HI payout fraction outside [0,1]")
    for a in np.unique(age[workers]):
        for s in (1, 2):
            m = workers & (age == a) & (sex == s)
            mass = float(workers_w[m].sum()) / workers_total
            if not mass:
                continue
            b = 2024 - int(a)
            family = "single_man" if s == 1 else "single_woman"
            L.survival.cache_clear()
            try:
                with pt.patched(L, "_decline", lambda: (decline["65plus"], decline["total"])):
                    work = L.worker(b, L.LEVEL_ADJ["medium"], 21, family, econ, prelim,
                                    arm=pt.G[0], payable=oasi, alive_at=int(a))
            finally:
                L.survival.cache_clear()
            yy = b + np.arange(121)
            bv = work["ben_pv_by_age"].copy()
            sv = _survival(L, int(a), s, np.arange(2024, b + 121), decline)
            hv = np.zeros(121)
            future_ages = np.arange(int(a), 121)
            hv[future_ages] = sv * hi_cost[yy[future_ages] - L.Y0] * hi_pay[yy[future_ages] - L.Y0] * disc[yy[future_ages] - L.Y0]
            hv[:65] = 0
            bv[yy <= 2024] = hv[yy <= 2024] = 0
            if bv.sum() <= 0 or hv.sum() <= 0:
                raise ValueError("[BLOCKED] worker payout profile has zero mass")
            flow = (1 - hi_fraction) * bv / bv.sum() + hi_fraction * hv / hv.sum()
            within = (yy >= 2024) & (yy <= 2100)
            payout[yy[within] - 2024] += mass * flow[within]
            tail += mass * float(flow[yy > 2100].sum())
    # Coarse population denominators preserve each broad band's 2024 CPS frame.
    band = np.select([age < 20, age < 65], [0, 1], 2)
    ratios = pop[["under20", "age20_64", "age65plus"]].to_numpy(float)
    ratios = ratios / ratios[0]
    means_tax = [float((pw * other * tax)[band == k].sum()) for k in range(3)]
    denom_tax_raw = ratios @ np.array(means_tax)
    denom_benefit_raw = ratios[:, 2] * float((pw * other * benefits * (age >= 65)).sum())
    cells = [(a, s) for a in np.unique(age[other]) for s in (1, 2)]
    counts = np.array([float(pw[other & (age == a) & (sex == s)].sum()) for a, s in cells])
    exp_tax = np.zeros((len(cells), len(years)))
    exp_ben = np.zeros_like(exp_tax)
    for k, (a, s) in enumerate(cells):
        attained = np.clip(a + years - 2024, 0, 120)
        surv = _survival(L, int(a), s, years, decline)
        exp_tax[k] = surv * tax_profile[s - 1, attained]
        exp_ben[k] = surv * benefit_profile[s - 1, attained]
    # Cross-sectional broad-band projection may undershoot the closed cohort.
    # Report every constrained year; this is a declared proxy, never silent.
    living_tax = counts @ exp_tax
    living_ben = counts @ exp_ben
    denom_tax = np.maximum(denom_tax_raw, living_tax)
    denom_ben = np.maximum(denom_benefit_raw, living_ben)
    if (denom_tax <= 0).any() or (denom_ben <= 0).any():
        raise ValueError("[BLOCKED] zero future cohort denominator")
    schedules = {"trust": payout}
    for horizon in (10, 30):
        schedules[f"borrowing{horizon}"] = ((years > 2024) & (years <= 2024+horizon)).astype(float)/horizon
    keys, shares = {}, {}
    for name, schedule in schedules.items():
        exp, den = (exp_ben, denom_ben) if name == "trust" else (exp_tax, denom_tax)
        cell_density = exp @ (schedule / den)
        density = np.zeros(len(d))
        for k, (a, s) in enumerate(cells):
            density[other & (age == a) & (sex == s)] = cell_density[k]
        living = float(np.sum(pw * density))
        if not 0 < living <= 1 + 1e-12:
            raise ValueError(f"[BLOCKED] invalid living share {name}: {living}")
        keys[name], shares[name] = density / living, living
        if abs(float(np.sum(pw * keys[name]))-1) > 1e-12:
            raise ValueError("[BLOCKED] cohort key fails weighted normalization")
    components = {k: (k if k in schedules else "trust") for k in trust_totals if k != "hi_payout_fraction"}
    for name, route in components.items():
        total = float(trust_totals[name])
        living_total = total * shares[route]
        future_total = total * (1 - shares[route])
        allocated = float(np.sum(pw * keys[route])) * living_total
        if not np.isfinite(total) or abs(allocated + future_total - total) > 1e-6:
            raise ValueError(f"[BLOCKED] cohort component fails conservation: {name}")
    if abs(float(payout.sum()) + tail - 1) > 1e-12:
        raise ValueError("[BLOCKED] payout mass including tail does not close")
    year_table = pop.copy()
    year_table["trust_payout_mass"] = payout
    for label, raw, den, living in (("tax", denom_tax_raw, denom_tax, living_tax),
                                     ("benefit", denom_benefit_raw, denom_ben, living_ben)):
        year_table[f"{label}_denominator_raw"] = raw
        year_table[f"{label}_denominator_used"] = den
        year_table[f"{label}_closed_cohort_exposure"] = living
        year_table[f"{label}_denominator_floor"] = den-raw
    profiles = pd.DataFrame([dict(kind="tax", **r) for r in tax_rows] +
                            [dict(kind="benefit", **r) for r in benefit_rows])
    pin_paths = {SSA, FISCAL/"pension_tr2026_2026_10_06/derived/paths.csv",
                 *[Path(module.__file__).resolve() for module in (pt,pt.PA,L,S,pt.T,pt.ss)],
                 *[L.TABLES[("general", s)] for s in ("male", "female")],
                 *[doc["pdf"] for doc in pt.T.DOCS.values()],
                 *[doc["pdf"] for doc in S.DOCS.values()]}
    if cps_path is not None:
        pin_paths.add(cps_path)
    pins = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(pin_paths)}
    proxies = ["[DEGRADED] SSA-area broad-age population growth applied to the other-resident CPS frame; future age/sex composition held at 2024 within broad bands.",
               "[DEGRADED] Future beneficiary cuts use SS retirement exposure from attained-age/sex cross-sectional benefits; no separate DI/child/survivor timing or specific legislative counterfactual.",
               "[DEGRADED] Worker payout timing uses medium single workers, entry 21, retirement 65; target FICA weights proxy accrual shares; HI fraction is explicit caller input (default 0.25).",
               "[DEGRADED] Living denominator is floored at closed-cohort exposure where coarse projected composition undershoots; every floor is recorded in year table.",
               "[ASSUMPTION] Borrowing service equal amounts in 2025–2034 / 2025–2054; federal income tax plus FICA age-sex profile proxies future federal taxes, with 2024 real profile fixed.",
               "[ASSUMPTION] NVSS 2024 sex survival with 2026 Trustees improvements; CPS topcoded ages treated as reported; age-profile means constant beyond last observed cell until age 100.",
               "[ASSUMPTION] Whole signed trust block uses one common payout-year incidence key; payroll/cash/accrual cannot be credited or charged to inconsistent cohorts.",
               "[DEGRADED] Payouts after 2100 are assigned wholly to future cohorts/arrivals; tail mass reported."]
    incidence={name:{label:float(np.sum(pw*key*np.where(mask,1.,0.))) for label,mask in
                    (("under18",age<18),("age18_64",(age>=18)&(age<65)),("age65plus",age>=65))} for name,key in keys.items()}
    return dict(keys=keys, living_shares=shares,living_incidence_by_current_age=incidence,component_keys={k: keys[v] for k,v in components.items()},
                component_living_shares={k: shares[v] for k,v in components.items()},
                years=year_table, profiles=profiles, pins=pins, proxies=proxies,
                gates=dict(population_closure=True, keys_normalized=True,
                           component_conservation=True,
                           payout_mass=float(payout.sum()), payout_tail=tail,
                           payout_closure=abs(float(payout.sum())+tail-1) < 1e-12,
                           tax_floor_years=int(np.sum(denom_tax>denom_tax_raw)),
                           benefit_floor_years=int(np.sum(denom_ben>denom_benefit_raw))))
