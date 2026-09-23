"""Scale, human-capital composition and innovation spillovers from the Mexican-origin group to
other US residents, 2024, area by area.

Frame: the complete annual account's stationary 2024 comparison with and without the 40,896,574 CPS
Mexican-origin residents; effects on all other residents; 2024 dollars. Group counts from the ACS
are scaled to the CPS union (x 40.896574 / 39.429519) and the difference is taken out of other
residents, as the housing and congestion lanes do.

Every channel is a change in other residents' log earnings, "without minus with":
  dpsi = sum of elasticity x (change in a regressor if the group were absent),
and the gain from the group's presence is E x (1 - exp(dpsi)), E being other residents' 2024
earnings in the area (split by education where the elasticity is). Scale regressors are log size
(ln(1 - s) with s the group's share of workers or persons); composition regressors are schooling
measures of the area's workers. A negative gain is a cost of presence.

Uncertainty: delta method with central differences at one standard error per parameter, with the
reported covariance where one regression gives both parameters, else independence.

Geographies: 1990 commuting zones (Card, Rothstein & Yi's units; central), 2023 CBSAs (areas
outside CBSAs as state remainders), and one national area.

Run from the repository root after tabulate.py, fetch.py and sample_weights.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/arms.py
"""
from __future__ import annotations

import hashlib
import json
import pathlib

import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
XW_COUNTY = ROOT / "infra/immigration-fiscal/employment_entry_2026_09_18/_cache/xwalk_puma22.csv"
XW_CBSA = CACHE / "xwalk_puma22_cbsa23.csv"
CZ_DORN = CACHE / "cw_cty_czone" / "cw_cty_czone.dta"
CRY = CACHE / "L3_czeffects.dta"
GAZ_CBSA = CACHE / "2023_Gaz_cbsa_national.txt"

CPS_UNION = 40_896_574
ACS_GROUP = 39_429_519
SCALE = CPS_UNION / ACS_GROUP
TAX = {"hsless": 0.384, "more": 0.426}   # account's marginal rates by skill cell (matched_benefits)
Z95 = 1.959964

# Counties in the 2020-based PUMA crosswalk that the 1990 CZ file codes differently.
COUNTY_FIX = {12086: 12025, 46102: 46113, 8014: 8013}
CT_PLANNING = range(9110, 9200)          # all eight 1990 Connecticut counties are CZ 20901
CT_CZ = 20901
ALASKA_CZ = 99999                        # Card-Rothstein-Yi pool Alaska into one CZ

ITEMS = ["persons", "adults25", "adults25_yrs", "adults25_ba", "workers", "workers_yrs",
         "workers_collyrs", "workers_hsyrs", "earnings", "wages", "earners", "ft3065_lc",
         "ft3065_ba", "workers_lths", "earnings_lths", "workers_hs", "earnings_hs", "workers_sc",
         "earnings_sc", "workers_ba", "earnings_ba", "workers_grad", "earnings_grad"]

# ---------------------------------------------------------------- published parameters
# Card, Rothstein & Yi (2023, w31587): pooled CZ place effect on log CZ size 0.034 (0.003) and on
# the share with some college or more 0.664 (0.099) (Table 3/9 col 2-3); by education (Table 10)
# 0.020 (0.002) high school or less, 0.043 (0.003) some college or more.
CRY_PAPER = {"lnsize": (0.034, 0.003), "frachighed": (0.664, 0.099),
             "size_hsless": (0.020, 0.002), "size_more": (0.043, 0.003)}
# Weight of the more-educated in the pooled place effect implied by Table 10 and Table 3:
# pooled = (1 - m) x 0.020 + m x 0.043. Its SE treats the three estimates as independent, which
# overstates it if, as is likely, they covary positively (overlapping samples).
_P, _L, _H = CRY_PAPER["lnsize"], CRY_PAPER["size_hsless"], CRY_PAPER["size_more"]
CRY_M = (_P[0] - _L[0]) / (_H[0] - _L[0])
CRY_M_SE = float(np.sqrt((_P[1] / (_H[0] - _L[0])) ** 2
                         + (_L[1] * (_P[0] - _H[0]) / (_H[0] - _L[0]) ** 2) ** 2
                         + (_H[1] * (_P[0] - _L[0]) / (_H[0] - _L[0]) ** 2) ** 2))

# Moretti (2004, J. Econometrics) Table 5: coefficients of the city share of college graduates on
# log wages of lths / hs / some college / college+ (entries per unit share; SE).
MORETTI_T5 = {
    "col 3 (2SLS age structure, 1980-90)": ([2.22, 2.08, 1.66, 0.86], [0.51, 0.45, 0.42, 0.35], "1980-1990"),
    "col 4 (2SLS age structure, Katz-Murphy, 1980-90)": ([1.91, 1.67, 1.24, 0.47], [0.52, 0.45, 0.42, 0.37], "1980-1990"),
    "col 6 (2SLS land grant, 1990)": ([0.77, 0.84, 0.94, 0.55], [0.20, 0.18, 0.18, 0.19], "1990"),
    "col 8 (2SLS land grant, 1980)": ([0.58, 0.74, 0.63, 0.45], [0.17, 0.14, 0.14, 0.17], "1980"),
}
# Moretti (2004) Table 2, NLSY 1979-94, pooled over education: col 6 base case (individual x city
# effects, city controls, Katz-Murphy) 1.27 (0.33); col 4 individual x city effects only 1.08 (0.32).
MORETTI_NLSY = {"base case (Table 2 col 6)": (1.27, 0.33), "individual x city effects (col 4)": (1.08, 0.32)}

# Rosenthal & Strange (2008, JUE) Table 4, OLS, log wage on counts of full-time workers aged 30-65
# within 0-5 and 5-25 miles of the workplace (coefficient, t-ratio), by the worker's education.
RS = {"lc": {"ba05": (4.79e-07, 1.75), "ba525": (2.57e-07, 3.27), "lc05": (-1.34e-07, -0.38), "lc525": (-1.26e-07, -2.23)},
      "ba": {"ba05": (1.19e-06, 3.49), "ba525": (1.59e-07, 1.49), "lc05": (-8.00e-07, -2.01), "lc525": (-6.71e-08, -0.79)},
      "all": {"ba05": (7.80e-07, 2.73), "ba525": (2.20e-07, 2.52), "lc05": (-3.97e-07, -1.12), "lc525": (-1.04e-07, -1.54)}}
RING05, RING525 = np.pi * 5 ** 2, np.pi * (25 ** 2 - 5 ** 2)    # square miles

# Burchardi, Chaney, Hassan, Tarquinio & Terry (w27075, Nov 2021), Table 9. Units: $100 of the
# five-year change in a county's average annual real wage (2010 $) per 1,000 adult (25+) migrants;
# patents per 100,000 residents.
BCHTT = {
    "wage_all_adults": (0.240, 0.084), "wage_level": (0.269, 0.048), "wage_x_years": (0.199, 0.045),
    "wage_low_tercile": (-0.184, 0.242), "wage_mid_tercile": (0.181, 0.055), "wage_high_tercile": (1.161, 0.425),
    "pat_all_adults": (0.239, 0.093), "pat_level": (0.257, 0.094), "pat_x_years": (0.235, 0.129),
    "pat_low_tercile": (2.023, 3.628), "pat_mid_tercile": (0.141, 0.081), "pat_high_tercile": (1.180, 0.695),
    "mean_years": 10.88,                                # Table 1, adult migrants, SD 3.65
    "structural_wage_gain": 0.05,                       # section 6.3: post-1965 immigration, by 2010
    "structural_pop_share_of_growth": 0.16,
}
US_POP_1965, US_POP_2010 = 194.30e6, 309.33e6          # Census resident population


# ---------------------------------------------------------------- geography
def load_cells():
    cells = pd.read_csv(DERIVED / "pums_puma_cells.csv", dtype={"STATE": str, "PUMA": str})
    cells["grp"] = np.where(cells["label"] == "other", "other", "group")
    wide = cells.groupby(["STATE", "PUMA", "grp"])[ITEMS].sum().unstack("grp", fill_value=0)
    wide.columns = [f"{g}_{v}" for v, g in wide.columns]
    mex = cells[cells.label == "mexborn"].set_index(["STATE", "PUMA"])[ITEMS].add_prefix("mexborn_")
    wide = wide.join(mex, how="left").fillna(0).reset_index()
    for v in ITEMS:                     # scale to the CPS union, difference out of others
        g = wide[f"group_{v}"].copy()
        wide[f"group_{v}"] = SCALE * g
        wide[f"other_{v}"] = wide[f"other_{v}"] - (SCALE - 1) * g
        wide[f"mexborn_{v}"] = SCALE * wide[f"mexborn_{v}"]
    return wide


def allocate(wide, alloc, key):
    """Spread PUMA cells over areas by population allocation factors, preserving national totals."""
    alloc = alloc.copy()
    alloc["afact"] = alloc["afact"] / alloc.groupby(["state", "puma"])["afact"].transform("sum")
    merged = wide.merge(alloc, left_on=["STATE", "PUMA"], right_on=["state", "puma"], how="left",
                        validate="one_to_many")
    if merged[key].isna().any():
        raise ValueError(f"PUMAs without allocation rows: {merged[merged[key].isna()][['STATE', 'PUMA']].head()}")
    values = [c for c in wide.columns if c not in ("STATE", "PUMA")]
    merged[values] = merged[values].mul(merged["afact"], axis=0)
    areas = merged.groupby(key)[values].sum()
    for c in values:
        if not np.isclose(areas[c].sum(), wide[c].sum(), rtol=1e-9):
            raise ValueError(f"allocation lost {c}")
    return areas


def cz_areas(wide):
    xw = pd.read_csv(XW_COUNTY, dtype=str)
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["state"], xw["puma"] = xw["state"].str.zfill(2), xw["puma22"].str.zfill(5)
    cty = xw["county"].astype(int).replace(COUNTY_FIX)
    dorn = pd.read_stata(CZ_DORN)
    cz_of = dict(zip(dorn["cty_fips"].astype(int), dorn["czone"].astype(int)))
    cz = cty.map(cz_of)
    cz[cty.isin(CT_PLANNING)] = CT_CZ
    cz[cty // 1000 == 2] = ALASKA_CZ
    if cz.isna().any():
        raise ValueError(f"counties without CZ: {sorted(cty[cz.isna()].unique())}")
    xw["cz"] = cz.astype(int)
    alloc = xw.groupby(["state", "puma", "cz"], as_index=False)["afact"].sum()
    return allocate(wide, alloc, "cz")


def cbsa_areas(wide):
    xw = pd.read_csv(XW_CBSA, dtype=str)
    xw = xw[xw["state"].str.fullmatch(r"\d{2}")]
    xw["afact"] = pd.to_numeric(xw["afact"])
    xw["puma"] = xw["puma22"].str.zfill(5)
    xw["area"] = np.where(xw["cbsa23"] == "99999", "nonCBSA_" + xw["state"], xw["cbsa23"])
    names = xw[xw["cbsa23"] != "99999"].drop_duplicates("cbsa23").set_index("cbsa23")["CBSAName23"]
    alloc = xw.groupby(["state", "puma", "area"], as_index=False)["afact"].sum()
    gaz = pd.read_csv(GAZ_CBSA, sep="\t", dtype={"GEOID": str})
    gaz.columns = [c.strip() for c in gaz.columns]
    land = gaz.set_index("GEOID")["ALAND_SQMI"]
    areas = allocate(wide, alloc, "area")
    missing = [a for a in areas.index if not a.startswith("nonCBSA") and a not in land.index]
    if missing:
        raise ValueError(f"CBSAs without gazetteer land area: {missing[:5]}")
    return areas, names, land


def national_area(wide):
    values = [c for c in wide.columns if c not in ("STATE", "PUMA")]
    return pd.DataFrame([wide[values].sum()], index=["US"])


# ---------------------------------------------------------------- area measures
def measures(a, land=None):
    m = pd.DataFrame(index=a.index)
    g = lambda v: a[f"group_{v}"]          # noqa: E731
    o = lambda v: a[f"other_{v}"]          # noqa: E731
    for v in ("persons", "workers", "earnings"):
        m[f"group_{v}"], m[f"other_{v}"] = g(v), o(v)
    m["mexborn_persons"] = a["mexborn_persons"]
    w_all = g("workers") + o("workers")
    m["s_persons"] = g("persons") / (g("persons") + o("persons"))
    m["s_workers"] = g("workers") / w_all
    gba, oba = g("workers_ba") + g("workers_grad"), o("workers_ba") + o("workers_grad")
    gsc, osc = g("workers_sc") + gba, o("workers_sc") + oba
    m["s_ba_workers"] = gba / (gba + oba)
    # Others' earnings by cell: CRY and the account split at high school; Moretti, Rosenthal-Strange
    # and the BA-split CES at the bachelor's degree.
    for k in ("lths", "hs", "sc", "ba", "grad"):
        m[f"E_{k}"] = o(f"earnings_{k}")
    m["E_hsless"] = m["E_lths"] + m["E_hs"]
    m["E_more"] = m["E_sc"] + m["E_ba"] + m["E_grad"]
    m["E_baplus"] = m["E_ba"] + m["E_grad"]
    m["E_nonba"] = m["E_hsless"] + m["E_sc"]
    # Schooling measures with and without the group; d* = without - with.
    m["dSC"] = osc / o("workers") - (gsc + osc) / w_all
    m["dBA"] = oba / o("workers") - (gba + oba) / w_all
    m["dYRS"] = o("workers_yrs") / o("workers") - (g("workers_yrs") + o("workers_yrs")) / w_all
    m["dCOLLY"] = o("workers_collyrs") / o("workers") - (g("workers_collyrs") + o("workers_collyrs")) / w_all
    m["dHSY"] = o("workers_hsyrs") / o("workers") - (g("workers_hsyrs") + o("workers_hsyrs")) / w_all
    # Iranzo-Peri's variables: years of schooling of workers with some college or more (all their
    # years), and of workers with at most a high school diploma, each divided by all workers.
    ip_coll = lambda who_sc, who_coll: 12 * who_sc + who_coll       # noqa: E731
    ip_c_with = (ip_coll(gsc, g("workers_collyrs")) + ip_coll(osc, o("workers_collyrs"))) / w_all
    ip_c_without = ip_coll(osc, o("workers_collyrs")) / o("workers")
    ip_h_with = (g("workers_yrs") + o("workers_yrs")) / w_all - ip_c_with
    ip_h_without = o("workers_yrs") / o("workers") - ip_c_without
    m["dIPCOLL"], m["dIPHS"] = ip_c_without - ip_c_with, ip_h_without - ip_h_with
    # Adults' BA share and log population (Glaeser-Resseger's regressors).
    m["ba25_with"] = (g("adults25_ba") + o("adults25_ba")) / (g("adults25") + o("adults25"))
    m["dBA25"] = o("adults25_ba") / o("adults25") - m["ba25_with"]
    m["lnpop_with"] = np.log(g("persons") + o("persons"))
    # Rosenthal-Strange counts of the group's full-time workers aged 30-65.
    m["group_ft_lc"], m["group_ft_ba"] = g("ft3065_lc"), g("ft3065_ba")
    if land is not None:
        area = pd.Series(m.index.map(lambda k: land.get(k, np.nan)), index=m.index, dtype=float)
        m["land_sqmi"] = area
        m["f05"] = np.minimum(1.0, RING05 / area)
        m["f525"] = np.minimum(1.0, (RING05 + RING525) / area) - m["f05"]
    return m.replace([np.inf, -np.inf], np.nan).fillna({c: 0.0 for c in m.columns if c not in ("land_sqmi", "f05", "f525")})


# ---------------------------------------------------------------- building blocks
def gain_parts(m, dpsi_by_cell):
    """dpsi_by_cell: {earnings column: dpsi series}. Returns gain and induced receipts (both $)."""
    gain, receipts = 0.0, 0.0
    for col, dpsi in dpsi_by_cell.items():
        d = m[col] * (1 - np.exp(dpsi))
        gain = gain + d
        # Tax rates are by the account's high-school split; BA-split cells use their mix.
        if col in ("E_hsless", "E_lths", "E_hs"):
            receipts = receipts + TAX["hsless"] * d
        elif col in ("E_more", "E_sc", "E_ba", "E_grad", "E_baplus"):
            receipts = receipts + TAX["more"] * d
        elif col == "E_nonba":
            share = (m["E_hsless"] / m["E_nonba"]).fillna(1.0)
            receipts = receipts + (TAX["hsless"] * share + TAX["more"] * (1 - share)) * d
        else:                                            # all others' earnings
            share = (m["E_hsless"] / (m["E_hsless"] + m["E_more"])).fillna(0.0)
            receipts = receipts + (TAX["hsless"] * share + TAX["more"] * (1 - share)) * d
    return float(np.sum(gain)), float(np.sum(receipts))


def lnsize(m, measure):
    s = {"workers": m["s_workers"], "persons": m["s_persons"], "ba_workers": m["s_ba_workers"]}[measure]
    return np.log1p(-s)                      # ln(1 - s): change in log size without the group


def ces_term(theta, s, m_weight, sigma):
    """Part of a pooled college-share gradient that a two-skill CES produces with no externality:
    d(weighted mean log wage)/ds = (theta - m) / (sigma s (1 - s)); zero when sigma is infinite."""
    if np.isinf(sigma):
        return 0.0
    return (theta - m_weight) / (sigma * s * (1 - s))


def delta_ci(fn, params, cov=None):
    """fn(params) -> (gain_bn, receipts_bn); params: list of (value, se). Central, low, high."""
    values = np.array([p[0] for p in params], float)
    ses = np.array([0.0 if p[1] is None else p[1] for p in params], float)
    central, receipts = fn(values)
    grad = np.zeros(len(values))
    for k in range(len(values)):
        if ses[k] == 0:
            continue
        up, dn = values.copy(), values.copy()
        up[k] += ses[k]
        dn[k] -= ses[k]
        grad[k] = (fn(up)[0] - fn(dn)[0]) / (2 * ses[k])
    v = np.diag(ses ** 2) if cov is None else np.asarray(cov, float)
    sd = float(np.sqrt(grad @ v @ grad))
    return central, receipts, central - Z95 * sd, central + Z95 * sd, sd


# ---------------------------------------------------------------- specifications
def scale_specs(ctx):
    """Each spec: name, unit, params [(value, se)], fn(m, p) -> {cell: dpsi}, source, population."""
    k_cond = ctx["cry_joint"]["lnsize"] / CRY_PAPER["lnsize"][0]      # conditional / pooled ratio
    specs = [
        ("CRY place effect by education, conditional on college share [central]",
         "log CZ workers; 0.020/0.043 x (conditional/pooled 0.0254/0.034)",
         [(ctx["cry_joint"]["lnsize"], ctx["cry_joint"]["lnsize_se"])],
         lambda m, p: {"E_hsless": CRY_PAPER["size_hsless"][0] * p[0] / CRY_PAPER["lnsize"][0] * lnsize(m, "workers"),
                       "E_more": CRY_PAPER["size_more"][0] * p[0] / CRY_PAPER["lnsize"][0] * lnsize(m, "workers")},
         "Card-Rothstein-Yi 2023 Table 10, scaled by this lane's joint regression on the public CZ file",
         "US, 691 CZs, LEHD 2010-2018 [INFERENCE: equal proportional conditioning by education]"),
        ("CRY place effect, pooled, conditional on college share", "log CZ workers",
         [(ctx["cry_joint"]["lnsize"], ctx["cry_joint"]["lnsize_se"])],
         lambda m, p: {"E_all": p[0] * lnsize(m, "workers")},
         "this lane's WLS of CRY psi_acspredict on log size and share with some college (HC1)",
         "US, 691 CZs, LEHD 2010-2018"),
        ("CRY place effect by education, unconditional", "log CZ workers",
         [CRY_PAPER["size_hsless"], CRY_PAPER["size_more"]],
         lambda m, p: {"E_hsless": p[0] * lnsize(m, "workers"), "E_more": p[1] * lnsize(m, "workers")},
         "Card-Rothstein-Yi 2023 Table 10 cols 1, 3", "US, 691 CZs, LEHD 2010-2018"),
        ("CRY place effect, pooled, unconditional", "log CZ workers", [CRY_PAPER["lnsize"]],
         lambda m, p: {"E_all": p[0] * lnsize(m, "workers")},
         "Card-Rothstein-Yi 2023 Table 3 col 2", "US, 691 CZs, LEHD 2010-2018"),
        ("CRY raw earnings gradient (sorting not removed)", "log CZ workers", [(0.075, 0.008)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "workers")},
         "Card-Rothstein-Yi 2023 Table 3 col 2 row 1", "US, 691 CZs, LEHD 2010-2018"),
        ("A&P recommended density elasticity (+-1.96 SD of estimates)", "log density = log persons at fixed area",
         [(0.04, 0.04)], lambda m, p: {"E_all": p[0] * lnsize(m, "persons")},
         "Ahlfeldt-Pietrostefani 2019 Table 6; SD 0.04 across 47 estimates (a spread, not an SE)",
         "347 estimates, mostly high-income countries; area-based, includes sorting"),
        ("A&P net of sorting (half), fixed area", "log persons at fixed area", [(0.02, None)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "persons")},
         "A&P 2019: 'net of selection effects, elasticity estimates about halve'; Combes-Gobillon 2015 ~0.02",
         "worker fixed-effect studies, France, Spain, Italy, UK, Netherlands"),
        ("A&P density with area scaling (0.04 x 0.43)", "log persons, density elasticity to size 0.43",
         [(0.04 * 0.43, None)], lambda m, p: {"E_all": p[0] * lnsize(m, "persons")},
         "A&P 0.04 x their city-size elasticity of density 0.43", "[INFERENCE: area shrinks with population]"),
        ("A&P net of sorting with area scaling (0.02 x 0.43)", "log persons", [(0.02 * 0.43, None)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "persons")}, "0.02 x 0.43", "[INFERENCE]"),
        ("De la Roca-Puga static plus seven years' learning", "log persons", [(0.049, None)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "persons")},
         "Combes-Gobillon 2015 p. 53, De la Roca-Puga", "Spain, worker panel"),
        ("Ciccone-Peri scale term, Table 4 col 2", "log city employment", [(0.081, 0.027)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "workers")},
         "Ciccone-Peri 2006 REStud Table 4 col 2 (2SLS, constant-composition wages)", "163 US cities, 1970-1990"),
        ("Ciccone-Peri scale term, Table 4 col 1", "log city employment", [(0.16, 0.06)],
         lambda m, p: {"E_all": p[0] * lnsize(m, "workers")},
         "Ciccone-Peri 2006 Table 4 col 1", "163 US cities, 1970-1990"),
        ("Glaeser-Resseger size effect varying with BA share", "log population; 0.022 + 0.196 (BA share - mean)",
         [(0.022, 0.012), (0.196, 0.113)],
         lambda m, p: {"E_all": (p[0] + p[1] * (m["ba25_with"] - ctx["gr_bbar"][id(m)])) * lnsize(m, "persons")},
         "Glaeser-Resseger 2010 Table 1 col 3 (individual log income, education controls)",
         "US MSAs, 2000 census [INFERENCE: demeaned at 2024 population-weighted mean]"),
        ("CRY pooled on the group's share of BA workers only", "log BA+ workers", [CRY_PAPER["lnsize"]],
         lambda m, p: {"E_all": p[0] * lnsize(m, "ba_workers")},
         "0.034 applied to the group's share of BA+ workers", "[INFERENCE: only skilled mass agglomerates]"),
    ]
    return specs


def comp_specs(ctx):
    w = ctx["weights"]
    specs = []
    for name, coef, source, pop in (
            ("Ciccone-Peri city, Table 4 col 2", (-0.004, 0.017), "Ciccone-Peri 2006 Table 4 col 2 (2SLS)", "163 US cities, 1970-1990"),
            ("Ciccone-Peri city, Table 4 col 1", (0.014, 0.03), "Ciccone-Peri 2006 Table 4 col 1", "163 US cities, 1970-1990"),
            ("Ciccone-Peri city, Table 4 col 4 (experience control)", (-0.01, 0.018), "Ciccone-Peri 2006 Table 4 col 4", "163 US cities, 1970-1990"),
            ("Ciccone-Peri city, white males, Table 5 col 2", (-0.001, 0.021), "Ciccone-Peri 2006 Table 5 col 2", "163 US cities, 1970-1990"),
            ("Acemoglu-Angrist state IV (QOB, CA and CL)", (0.004, 0.035), "Acemoglu-Angrist 1999 (w7444) Table 6 col 3", "US states, white men 40-49, 1960-80"),
            ("Acemoglu-Angrist state IV (QOB and CA)", (0.017, 0.043), "Acemoglu-Angrist 1999 Table 6 col 2", "US states, white men 40-49, 1960-80")):
        specs.append((name, "per year of workers' mean schooling", [coef],
                      lambda m, p: {"E_all": p[0] * m["dYRS"]}, source, pop))
    for name, c, h, source, pop in (
            ("Iranzo-Peri basic, Table 8 col 1", (0.06, 0.025), (-0.01, 0.01), "Iranzo-Peri 2009 (w12440) Table 8 col 1 (2SLS)", "US states, 1970-2000"),
            ("Iranzo-Peri 1980-2000, Table 8 col 5", (0.12, 0.04), (0.01, 0.03), "Iranzo-Peri 2009 Table 8 col 5", "US states, 1980-2000"),
            ("Iranzo-Peri sector-demand control, Table 9 col 4", (0.11, 0.04), (-0.01, 0.02), "Iranzo-Peri 2009 Table 9 col 4", "US states, 1970-2000")):
        specs.append((name, "per year of schooling of SC+ (HS-or-less) workers per worker, their definition",
                      [c, h], lambda m, p: {"E_all": p[0] * m["dIPCOLL"] + p[1] * m["dIPHS"]}, source, pop))
    specs.append(("Iranzo-Peri basic, read as years beyond 12 per worker", "per year beyond 12 (up to 12) per worker",
                  [(0.06, 0.025), (-0.01, 0.01)], lambda m, p: {"E_all": p[0] * m["dCOLLY"] + p[1] * m["dHSY"]},
                  "Iranzo-Peri 2009 Table 8 col 1, the reading their text compares with Moretti",
                  "[INFERENCE: not their variable; their Table 6 first stages imply ~17 years per college worker]"))
    for col, (b, se, period) in MORETTI_T5.items():
        specs.append((f"Moretti college graduates' own, {col}", "per unit BA+ share of workers (lower bound on spillover)",
                      [(b[3], se[3])], lambda m, p: {"E_all": p[0] * m["dBA"]},
                      f"Moretti 2004 JoE Table 5 {col}", f"282 US MSAs, {period}"))
        for wlabel in (period, "2024 others"):
            wv = w[wlabel]
            g = float(np.dot(wv, b))
            s = float(np.dot(wv, se))                    # perfect correlation across groups: widest
            specs.append((f"Moretti earnings-weighted, {col}, {wlabel} weights",
                          "per unit BA+ share (constant-composition externality)", [(g, s)],
                          lambda m, p: {"E_all": p[0] * m["dBA"]},
                          f"Moretti 2004 Table 5 {col}, averaged with {wlabel} income shares (Ciccone-Peri identification)",
                          f"282 US MSAs, {period}; SE assumes perfectly correlated group estimates"))
    for tfp in (0.5, 0.7):
        specs.append((f"Moretti plant productivity {tfp} per unit college share, as wages at labour share 0.7",
                      "per unit BA+ share (TFP / 0.7)", [(tfp / 0.7, None)], lambda m, p: {"E_all": p[0] * m["dBA"]},
                      "Moretti 2004 AER (w9316) sec. 6: 'a one percentage point increase in city college share is "
                      "associated with a 0.5-0.7 percent increase in productivity'; his own wage-to-productivity factor 0.7",
                      "US manufacturing plants, 1982-1992 [INFERENCE: applied economy-wide]"))
    for label, (b, se) in MORETTI_NLSY.items():
        for sigma in (2.0, 1.5, 2.5):
            corr = ces_term(ctx["shares"]["ba_1980_90"]["theta"], ctx["shares"]["ba_1980_90"]["s"],
                            ctx["shares"]["ba_1980_90"]["s"], sigma)
            specs.append((f"Moretti NLSY {label}, net of CES sigma {sigma:g}", "per unit BA+ share",
                          [(b - corr, se)], lambda m, p: {"E_all": p[0] * m["dBA"]},
                          f"Moretti 2004 Table 2/3; CES term {corr:.3f} at 1980-90 BA shares",
                          "NLSY79 workers in 201 MSAs, 1979-1994"))
    cry = ctx["cry_joint"]
    for weight_label, mw in (("CRY-implied weights", "cry"), ("employment weights", "s")):
        for sigma in (2.0, 1.5, 2.5, np.inf):
            sh = ctx["shares"]["sc_cry"]
            corr = ces_term(sh["theta"], sh["s"], CRY_M if mw == "cry" else sh["s"], sigma)
            tag = "[central]" if (mw == "cry" and sigma == 2.0) else ""
            sig = "no CES term (upper bound)" if np.isinf(sigma) else f"sigma {sigma:g}"
            if np.isinf(sigma) and mw == "s":
                continue
            specs.append((f"CRY college gradient net of CES, {sig}, {weight_label} {tag}".strip(),
                          "per unit share of workers with some college or more",
                          [(cry["frachighed"] - corr, cry["frachighed_se"])],
                          lambda m, p: {"E_all": p[0] * m["dSC"]},
                          f"this lane's CRY joint regression 0.326 less CES term {corr:.3f}",
                          "US, 691 CZs, LEHD 2010-2018"))
    sc_sh = ctx["shares"]["sc_cry"]
    specs.append(("CRY college gradient net of CES, sigma 2, CRY-implied weights, weight's SE included",
                  "per unit share of workers with some college or more; m sampled",
                  [(cry["frachighed"], cry["frachighed_se"]), (CRY_M, CRY_M_SE)],
                  lambda m, p, sh=sc_sh: {"E_all": (p[0] - ces_term(sh["theta"], sh["s"], p[1], 2.0)) * m["dSC"]},
                  f"as the central, with m = {CRY_M:.3f} ({CRY_M_SE:.3f}) from CRY Tables 3 and 10 (independence)",
                  "US, 691 CZs, LEHD 2010-2018"))
    for sigma in (2.0, np.inf):
        sh = ctx["shares"]["ba_2000"]
        corr = ces_term(sh["theta"], sh["s"], sh["s"], sigma)
        sig = "no CES term" if np.isinf(sigma) else f"net of CES sigma {sigma:g}"
        specs.append((f"Glaeser-Resseger BA share, {sig}", "per unit adults' BA share; 0.411 + 0.196 (log pop - mean)",
                      [(0.411, 0.122), (0.196, 0.113)],
                      (lambda corr: lambda m, p: {"E_all": (p[0] + p[1] * (m["lnpop_with"] - ctx["gr_pbar"][id(m)])) * m["dBA25"]
                                                  - corr * m["dBA"]})(corr),
                      f"Glaeser-Resseger 2010 Table 1 col 3; CES term {corr:.3f} at 2000 BA shares",
                      "US MSAs, 2000 census"))
    return specs


def evaluate(specs, m, geo, channel):
    rows = []
    for name, unit, params, fn, source, pop in specs:
        def f(p, fn=fn):
            return gain_parts(m, fn(m, p))
        c, rec, lo, hi, sd = delta_ci(f, params)
        has_se = any(p[1] is not None for p in params)
        rows.append({"channel": channel, "geography": geo, "spec": name, "unit": unit,
                     "parameters": "; ".join(f"{p[0]:.4g}" + ("" if p[1] is None else f" ({p[1]:.3g})") for p in params),
                     "gain_bn": c / 1e9, "gain_low_bn": lo / 1e9 if has_se else np.nan,
                     "gain_high_bn": hi / 1e9 if has_se else np.nan, "sd_bn": sd / 1e9 if has_se else np.nan,
                     "induced_receipts_bn": rec / 1e9, "private_bn": (c - rec) / 1e9,
                     "source": source, "population": pop})
    return rows


# ---------------------------------------------------------------- joint specifications (one regression)
def joint_specs(ctx):
    cry = ctx["cry_joint"]
    sh = ctx["shares"]["sc_cry"]
    specs = []
    for sigma in (2.0, 1.5, 2.5, np.inf):
        corr = ces_term(sh["theta"], sh["s"], CRY_M, sigma)
        sig = "no CES term" if np.isinf(sigma) else f"sigma {sigma:g}"
        def fn(m, p, corr=corr):
            size = lnsize(m, "workers")
            comp = (p[1] - corr) * m["dSC"]
            return {"E_hsless": CRY_PAPER["size_hsless"][0] / CRY_PAPER["lnsize"][0] * p[0] * size + comp,
                    "E_more": CRY_PAPER["size_more"][0] / CRY_PAPER["lnsize"][0] * p[0] * size + comp}
        specs.append((f"CRY joint: scale by education + college gradient net of CES ({sig}, CRY weights)"
                      + (" [central]" if sigma == 2.0 else ""),
                      [(cry["lnsize"], cry["lnsize_se"]), (cry["frachighed"], cry["frachighed_se"])], cry["cov"], fn,
                      "one regression on the CRY public file; covariance from the fit"))
    def fn_m(m, p):
        size = lnsize(m, "workers")
        comp = (p[1] - ces_term(sh["theta"], sh["s"], p[2], 2.0)) * m["dSC"]
        return {"E_hsless": CRY_PAPER["size_hsless"][0] / CRY_PAPER["lnsize"][0] * p[0] * size + comp,
                "E_more": CRY_PAPER["size_more"][0] / CRY_PAPER["lnsize"][0] * p[0] * size + comp}
    cov3 = np.zeros((3, 3))
    cov3[:2, :2] = np.asarray(cry["cov"])
    cov3[2, 2] = CRY_M_SE ** 2
    specs.append(("CRY joint central, weight m's SE included (independence)",
                  [(cry["lnsize"], cry["lnsize_se"]), (cry["frachighed"], cry["frachighed_se"]), (CRY_M, CRY_M_SE)],
                  cov3, fn_m, f"m = {CRY_M:.3f} ({CRY_M_SE:.3f}) from CRY Tables 3 and 10"))
    for label, (b_s, se_s), (b_y, se_y) in (("Table 4 col 2", (0.081, 0.027), (-0.004, 0.017)),
                                             ("Table 4 col 1", (0.16, 0.06), (0.014, 0.03)),
                                             ("Table 4 col 4", (0.11, 0.04), (-0.01, 0.018))):
        specs.append((f"Ciccone-Peri joint, {label}: scale + average schooling",
                      [(b_s, se_s), (b_y, se_y)], None,
                      lambda m, p: {"E_all": p[0] * lnsize(m, "workers") + p[1] * m["dYRS"]},
                      "Ciccone-Peri 2006; covariance not reported (independence)"))
    gsh = ctx["shares"]["ba_2000"]
    gcorr = ces_term(gsh["theta"], gsh["s"], gsh["s"], 2.0)
    def gr(m, p, corr=gcorr):
        bdev = m["ba25_with"] - ctx["gr_bbar"][id(m)]
        pdev = m["lnpop_with"] - ctx["gr_pbar"][id(m)]
        dp, db = lnsize(m, "persons"), m["dBA25"]
        return {"E_all": p[0] * dp + p[1] * db + p[2] * (dp * bdev + pdev * db + dp * db) - corr * m["dBA"]}
    specs.append(("Glaeser-Resseger joint, Table 1 col 3, BA term net of CES sigma 2",
                  [(0.022, 0.012), (0.411, 0.122), (0.196, 0.113)], None, gr,
                  "Glaeser-Resseger 2010; covariance not reported (independence)"))
    return specs


def rs_spec(m, variant):
    """Rosenthal-Strange rings with the group's full-time 30-65 workers spread uniformly over the CBSA."""
    keys = ["ba05", "ba525", "lc05", "lc525"]
    groups = {"by_education": (("E_nonba", "lc"), ("E_baplus", "ba")), "full_sample": (("E_all", "all"),)}[variant]
    params, index = [], []
    for col, sample in groups:
        for k in keys:
            b, t = RS[sample][k]
            params.append((b, abs(b / t)))
            index.append((col, k))
    inside = m["f05"].notna()
    x = {"ba05": m["group_ft_ba"] * m["f05"], "ba525": m["group_ft_ba"] * m["f525"],
         "lc05": m["group_ft_lc"] * m["f05"], "lc525": m["group_ft_lc"] * m["f525"]}
    def fn(mm, p):
        out = {}
        for (col, k), v in zip(index, p):
            out[col] = out.get(col, 0.0) + np.where(inside, -v * x[k].fillna(0.0), 0.0)
        return out
    return params, fn


def evaluate_joint(specs, m, geo):
    rows = []
    for name, params, cov, fn, note in specs:
        def f(p, fn=fn):
            return gain_parts(m, fn(m, p))
        c, rec, lo, hi, sd = delta_ci(f, params, cov)
        rows.append({"geography": geo, "spec": name, "gain_bn": c / 1e9, "gain_low_bn": lo / 1e9,
                     "gain_high_bn": hi / 1e9, "sd_bn": sd / 1e9, "induced_receipts_bn": rec / 1e9,
                     "private_bn": (c - rec) / 1e9, "note": note})
    return rows


# ---------------------------------------------------------------- innovation
def innovation(nat_table, other_earn):
    t = nat_table
    y = float(t[(t.label == "mexborn") & (t.item == "mean_years_adults25")].estimate.iloc[0])
    adults = float(t[(t.label == "mexborn") & (t.item == "adults25")].estimate.iloc[0]) * SCALE
    persons = float(t[(t.label == "mexborn") & (t.item == "persons")].estimate.iloc[0]) * SCALE
    removed = BCHTT["structural_pop_share_of_growth"] * (US_POP_2010 - US_POP_1965)
    base = BCHTT["structural_wage_gain"] * persons / removed        # average-migrant effect, share of E
    rows = []
    for out, lvl, slope, avg, tercile in (("patents", "pat_level", "pat_x_years", "pat_all_adults", "pat_low_tercile"),
                                          ("wages", "wage_level", "wage_x_years", "wage_all_adults", "wage_low_tercile")):
        a, sa = BCHTT[lvl]
        b, sb = BCHTT[slope]
        eff = a + b * (y - BCHTT["mean_years"])
        se = np.sqrt(sa ** 2 + ((y - BCHTT["mean_years"]) * sb) ** 2)     # covariance not reported
        for spec, e, s, denom in (("linear in migrants' years (Table 9 col 2)", eff, se, a),
                                  ("bottom tercile of migrant schooling (Table 9 col 5)", BCHTT[tercile][0],
                                   BCHTT[tercile][1], BCHTT[avg][0])):
            ratio, rlo, rhi = e / denom, (e - Z95 * s) / denom, (e + Z95 * s) / denom
            rows.append({"outcome_ratio": out, "spec": spec, "mexborn_mean_years_25plus": y,
                         "mexborn_adults25": adults, "mexborn_persons": persons,
                         "effect_per_1000": e, "se": s, "ratio_to_average_migrant": ratio,
                         "ratio_low": rlo, "ratio_high": rhi,
                         "structural_share_of_E_average_migrant": base,
                         "gain_bn": base * ratio * other_earn / 1e9,
                         "gain_low_bn": base * rlo * other_earn / 1e9,
                         "gain_high_bn": base * rhi * other_earn / 1e9})
    return pd.DataFrame(rows), removed


# ---------------------------------------------------------------- CRY regressions
def cry_regressions():
    df = pd.read_stata(CRY)
    out, fits = [], {}
    for ycol in ("psi_acspredict", "cz_effects_m1"):
        for xs in (["lnsize"], ["frachighed"], ["lnsize", "frachighed"]):
            fit = sm.WLS(df[ycol], sm.add_constant(df[xs]), weights=df["wcount"]).fit(cov_type="HC1")
            fits[(ycol, "+".join(xs))] = fit
            for x in xs:
                out.append({"outcome": ycol, "regressors": "+".join(xs), "term": x,
                            "coef": fit.params[x], "se_hc1": fit.bse[x], "r2": fit.rsquared, "n": int(fit.nobs)})
    out = pd.DataFrame(out)
    g1 = fits[("psi_acspredict", "lnsize")].params["lnsize"]
    g2 = fits[("psi_acspredict", "frachighed")].params["frachighed"]
    if not (abs(g1 - CRY_PAPER["lnsize"][0]) < 0.0005 and abs(g2 - CRY_PAPER["frachighed"][0]) < 0.0005):
        raise SystemExit(f"[POSITIVE CONTROL FAILED] CRY Table 3 not reproduced: {g1:.4f}, {g2:.4f}")
    # The public premiums are best linear predictions from ACS data, so regression SEs on them are
    # too small; inflate by the ratio of the paper's SE to the SE on the public file (never below 1).
    infl = {x: max(1.0, CRY_PAPER[x][1] / fits[("psi_acspredict", x)].bse[x]) for x in ("lnsize", "frachighed")}
    jf = fits[("psi_acspredict", "lnsize+frachighed")]
    cov = jf.cov_params().loc[["lnsize", "frachighed"], ["lnsize", "frachighed"]].to_numpy()
    d = np.diag([infl["lnsize"], infl["frachighed"]])
    joint = {"lnsize": float(jf.params["lnsize"]), "frachighed": float(jf.params["frachighed"]),
             "lnsize_se": float(jf.bse["lnsize"] * infl["lnsize"]),
             "frachighed_se": float(jf.bse["frachighed"] * infl["frachighed"]),
             "cov": (d @ cov @ d).tolist(), "inflation": infl,
             "corr": float(cov[0, 1] / np.sqrt(cov[0, 0] * cov[1, 1])),
             "s_sc_cry_sample": float((df["frachighed"] * df["wcount"]).sum() / df["wcount"].sum())}
    return out, joint, (g1, g2)


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def main():
    DERIVED.mkdir(exist_ok=True)
    cry_table, cry_joint, (g1, g2) = cry_regressions()
    cry_table.to_csv(DERIVED / "cry_gradient.csv", index=False)
    assert abs(cry_joint["lnsize"] - 0.0254) < 0.0005 and abs(cry_joint["frachighed"] - 0.3264) < 0.0005

    wide = load_cells()
    nat_table = pd.read_csv(DERIVED / "pums_national.csv")
    cz = measures(cz_areas(wide))
    cb_raw, names, land = cbsa_areas(wide)
    cb = measures(cb_raw, land)
    nat = measures(national_area(wide))
    for m in (cz, cb, nat):
        m["E_all"] = m["other_earnings"]
    cz.to_csv(DERIVED / "area_measures_cz.csv")
    cb.assign(name=cb.index.map(lambda k: names.get(k, k))).to_csv(DERIVED / "area_measures_cbsa.csv")

    # Shares for the CES terms. CRY sample: its size-weighted college share; the earnings share
    # follows from the 2024 ratio of earnings per worker, some college+ to high school or less.
    sw = pd.read_csv(DERIVED / "sample_weights.csv").set_index(["year", "cell"])
    ws = lambda yr, col: np.array([sw.loc[(yr, c), col] for c in ("lths", "hs", "sc", "ba")])  # noqa: E731
    all_w = nat_table[nat_table.label == "all"].set_index("item")["estimate"]
    w_more = all_w["workers_sc"] + all_w["workers_ba"] + all_w["workers_grad"]
    e_more = all_w["earnings_sc"] + all_w["earnings_ba"] + all_w["earnings_grad"]
    rel = (e_more / w_more) / ((all_w["earnings"] - e_more) / (all_w["workers"] - w_more))
    s_cry = cry_joint["s_sc_cry_sample"]
    theta_cry = s_cry * rel / (s_cry * rel + 1 - s_cry)
    ba = lambda yrs: {"s": float(np.mean([sw.loc[(y, "ba"), "worker_share"] for y in yrs])),   # noqa: E731
                      "theta": float(np.mean([sw.loc[(y, "ba"), "income_share"] for y in yrs]))}
    others_w = np.array([float(nat[f"E_{k}"].iloc[0]) for k in ("lths", "hs", "sc")] + [float(nat["E_baplus"].iloc[0])])
    ctx = {"cry_joint": cry_joint,
           "shares": {"sc_cry": {"s": s_cry, "theta": float(theta_cry), "earnings_ratio_2024": float(rel)},
                      "ba_1980_90": ba((1980, 1990)), "ba_2000": ba((2000,))},
           "weights": {"1980-1990": (ws(1980, "income_share") + ws(1990, "income_share")) / 2,
                       "1990": ws(1990, "income_share"), "1980": ws(1980, "income_share"),
                       "2024 others": others_w / others_w.sum()},
           "gr_bbar": {}, "gr_pbar": {}}
    for m in (cz, cb, nat):
        pw = m["group_persons"] + m["other_persons"]
        keep = ~m.index.astype(str).str.startswith("nonCBSA")
        ctx["gr_bbar"][id(m)] = float((m["ba25_with"] * pw)[keep].sum() / pw[keep].sum())
        ctx["gr_pbar"][id(m)] = float((m["lnpop_with"] * pw)[keep].sum() / pw[keep].sum())

    geos = (("CZ 1990", cz), ("CBSA 2023", cb), ("national", nat))
    sc_rows, co_rows, jo_rows = [], [], []
    for geo, m in geos:
        sc_rows += evaluate(scale_specs(ctx), m, geo, "scale")
        co_rows += evaluate(comp_specs(ctx), m, geo, "composition")
        jo_rows += evaluate_joint(joint_specs(ctx), m, geo)
    for variant in ("by_education", "full_sample"):
        params, fn = rs_spec(cb, variant)
        jo_rows += evaluate_joint([(f"Rosenthal-Strange rings, OLS, {variant.replace('_', ' ')}, uniform within CBSA",
                                    params, None, fn, "R&S 2008 Table 4 OLS; SE = coef / t; independence")],
                                  cb, "CBSA 2023")
    others = float(nat["other_persons"].iloc[0])
    frames = {}
    for label, rows in (("scale_grid", sc_rows), ("composition_grid", co_rows), ("joint_grid", jo_rows)):
        df = pd.DataFrame(rows)
        df["per_group_member"] = df["gain_bn"] * 1e9 / CPS_UNION
        df["per_other_resident"] = df["gain_bn"] * 1e9 / others
        df.to_csv(DERIVED / f"{label}.csv", index=False)
        frames[label] = df

    # Every scale x composition pairing on the central geography (independent errors).
    s_c = frames["scale_grid"][frames["scale_grid"].geography == "CZ 1990"]
    c_c = frames["composition_grid"][frames["composition_grid"].geography == "CZ 1990"]
    net = s_c[["spec", "gain_bn", "sd_bn", "induced_receipts_bn"]].merge(
        c_c[["spec", "gain_bn", "sd_bn", "induced_receipts_bn"]], how="cross", suffixes=("_scale", "_composition"))
    net["net_bn"] = net["gain_bn_scale"] + net["gain_bn_composition"]
    net["net_sd_bn"] = np.sqrt(net["sd_bn_scale"].fillna(0) ** 2 + net["sd_bn_composition"].fillna(0) ** 2)
    net["net_receipts_bn"] = net["induced_receipts_bn_scale"] + net["induced_receipts_bn_composition"]
    net["net_per_group_member"] = net["net_bn"] * 1e9 / CPS_UNION
    net.to_csv(DERIVED / "net_grid.csv", index=False)

    other_earn = float(nat["other_earnings"].iloc[0])
    inn, removed = innovation(nat_table, other_earn)
    inn.to_csv(DERIVED / "innovation_bchtt.csv", index=False)

    # Distribution of the central joint specification over CBSAs.
    corr = ces_term(ctx["shares"]["sc_cry"]["theta"], ctx["shares"]["sc_cry"]["s"], CRY_M, 2.0)
    k = cry_joint["lnsize"] / CRY_PAPER["lnsize"][0]
    dist = cb.copy()
    dist["name"] = dist.index.map(lambda a: names.get(a, a))
    size = lnsize(dist, "workers")
    dist["scale_bn"] = (dist["E_hsless"] * (1 - np.exp(CRY_PAPER["size_hsless"][0] * k * size))
                        + dist["E_more"] * (1 - np.exp(CRY_PAPER["size_more"][0] * k * size))) / 1e9
    dist["composition_bn"] = dist["E_all"] * (1 - np.exp((cry_joint["frachighed"] - corr) * dist["dSC"])) / 1e9
    dist["net_bn"] = dist["scale_bn"] + dist["composition_bn"]
    for c in ("scale_bn", "composition_bn", "net_bn"):
        dist[c.replace("_bn", "_per_other_resident")] = dist[c] * 1e9 / dist["other_persons"]
    cols = ["name", "other_persons", "group_persons", "s_workers", "s_persons", "dSC", "dBA", "other_earnings",
            "scale_bn", "composition_bn", "net_bn", "scale_per_other_resident", "composition_per_other_resident",
            "net_per_other_resident"]
    dist.sort_values("other_earnings", ascending=False)[cols].to_csv(DERIVED / "metro_distribution.csv")

    params = []
    for spec in scale_specs(ctx) + comp_specs(ctx):
        params.append({"spec": spec[0], "unit": spec[1], "parameters": "; ".join(f"{p[0]:.4g} ({p[1]})" for p in spec[2]),
                       "source": spec[4], "population": spec[5]})
    for key, v in BCHTT.items():
        params.append({"spec": f"BCHTT {key}", "unit": "$100 per 1,000 adult migrants (5-yr change), patents per 100,000, or as named",
                       "parameters": str(v), "source": "Burchardi et al. w27075 Tables 1, 9; section 6.3",
                       "population": "US counties, 1975-2010"})
    pd.DataFrame(params).to_csv(DERIVED / "parameters.csv", index=False)

    rs_excluded = float(cb.loc[cb["f05"].isna(), "other_earnings"].sum() / cb["other_earnings"].sum())
    acs_all = float(all_w["persons"])
    if not (np.isclose(nat["group_persons"].iloc[0], CPS_UNION, rtol=1e-9)
            and np.isclose(nat["group_persons"].iloc[0] + others, acs_all, rtol=1e-9)):
        raise SystemExit("[GATE FAILED] CPS scaling does not conserve the ACS population")
    # The brief's first-order formula, E x elasticity x ln(1/(1-s)), for the central scale spec.
    size_cz = -lnsize(cz, "workers")
    brief_linear = float(((cz["E_hsless"] * CRY_PAPER["size_hsless"][0] + cz["E_more"] * CRY_PAPER["size_more"][0])
                          * k * size_cz).sum() / 1e9)
    central_scale = frames["scale_grid"].query("geography == 'CZ 1990'").iloc[0]
    assert central_scale["spec"].endswith("[central]")
    if abs(brief_linear / central_scale["gain_bn"] - 1) > 0.01:
        raise SystemExit(f"[GATE FAILED] exponential and linear scale forms differ by more than 1%: {brief_linear}")

    # Headline rows quoted in RESULT.md.
    pick = [("scale_grid", "CZ 1990", "CRY place effect by education, conditional on college share [central]"),
            ("composition_grid", "CZ 1990", "CRY college gradient net of CES, sigma 2, CRY-implied weights [central]"),
            ("joint_grid", "CZ 1990", "CRY joint: scale by education + college gradient net of CES (sigma 2, CRY weights) [central]"),
            ("joint_grid", "CBSA 2023", "CRY joint: scale by education + college gradient net of CES (sigma 2, CRY weights) [central]"),
            ("joint_grid", "national", "CRY joint: scale by education + college gradient net of CES (sigma 2, CRY weights) [central]")]
    summary = pd.concat([frames[f][(frames[f].geography == g) & (frames[f].spec == s)].assign(table=f)
                         for f, g, s in pick], ignore_index=True)
    inn_rows = inn[inn.spec.str.startswith("linear")].assign(
        table="innovation_bchtt", geography="national",
        spec=lambda d: "BCHTT structural transport, " + d["outcome_ratio"] + " gradient at Mexico-born schooling")
    inn_rows["per_group_member"] = inn_rows["gain_bn"] * 1e9 / CPS_UNION
    inn_rows["per_other_resident"] = inn_rows["gain_bn"] * 1e9 / others
    summary = pd.concat([summary, inn_rows], ignore_index=True)
    summary[["table", "geography", "spec", "gain_bn", "gain_low_bn", "gain_high_bn", "induced_receipts_bn",
             "private_bn", "per_group_member", "per_other_resident"]].to_csv(DERIVED / "summary.csv", index=False)
    checks = {
        "cps_scale": SCALE, "group_persons_scaled": float(nat["group_persons"].iloc[0]),
        "other_persons": others, "other_earnings_bn": other_earn / 1e9,
        "national": {k: float(nat[k].iloc[0]) for k in ("s_persons", "s_workers", "s_ba_workers", "dSC", "dBA",
                                                          "dYRS", "dCOLLY", "dHSY", "dIPCOLL", "dIPHS", "dBA25")},
        "cz_count": int(len(cz)), "cbsa_area_count": int(len(cb)),
        "earnings_weighted_s_workers": {geo: float((m["s_workers"] * m["other_earnings"]).sum() / m["other_earnings"].sum())
                                        for geo, m in geos},
        "cry_table3_reproduced": {"lnsize": float(g1), "frachighed": float(g2)},
        "cry_joint": {k: v for k, v in cry_joint.items()},
        "cry_pooled_weight_on_more_educated": CRY_M,
        "ces_shares": ctx["shares"],
        "moretti_weights": {k: list(np.round(v, 4)) for k, v in ctx["weights"].items()},
        "glaeser_resseger_means": {geo: {"ba25": ctx["gr_bbar"][id(m)], "lnpop": ctx["gr_pbar"][id(m)]} for geo, m in geos},
        "rs_excluded_share_of_other_earnings_outside_cbsas": rs_excluded,
        "central_scale_brief_linear_formula_bn": brief_linear,
        "central_scale_exponential_form_bn": float(central_scale["gain_bn"]),
        "bchtt_structural_removed_population": removed,
        "reused_inputs_sha256": {"employment_entry xwalk_puma22.csv": sha(XW_COUNTY)[:12]},
    }
    (DERIVED / "checks.json").write_text(json.dumps(checks, indent=1, default=float))
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 90)
    show = ["spec", "gain_bn", "gain_low_bn", "gain_high_bn", "induced_receipts_bn"]
    for label in ("scale_grid", "composition_grid", "joint_grid"):
        df = frames[label]
        print(f"\n[{label}] CZ 1990" if label != "joint_grid" else f"\n[{label}]")
        sel = df if label == "joint_grid" else df[df.geography == "CZ 1990"]
        cols = (["geography"] if label == "joint_grid" else []) + show
        print(sel[cols].round(2).to_string(index=False))
    print("\n[innovation]")
    print(inn[["outcome_ratio", "spec", "ratio_to_average_migrant", "ratio_low", "ratio_high", "gain_bn",
               "gain_low_bn", "gain_high_bn"]].round(3).to_string(index=False))
    print(json.dumps({k: checks[k] for k in ("national", "earnings_weighted_s_workers", "ces_shares",
                                             "cry_pooled_weight_on_more_educated", "rs_excluded_share_of_other_earnings_outside_cbsas")},
                     indent=1, default=float))


if __name__ == "__main__":
    main()
