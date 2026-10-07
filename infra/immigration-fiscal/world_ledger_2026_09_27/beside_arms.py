"""Beside arms (operator, 2026-10-07): three side scenarios on the world ledger's central for main case v6 (oct07), on
its own lineage basis (42,752,213 members). Each tests one objection to a measure the central uses; none replaces it.

1. Best domestic alternative. The group's Mexican counterfactual in Mexico's three big metropolitan labor markets
   (Valle de Mexico, Guadalajara, Monterrey: the municipalities INEGI's ENOE 2024 samples as cities 1-3) instead of the
   nation. Pay: ENIGH 2024 pay per person in the metro over the national cell of the same sex, age band and schooling,
   by sex x schooling (age-standardized; pooled across sex below 100 records), applied to every national cell; the
   15-24-year-olds' cells by sex x age band. G2's own schooling: ESRU-EMOVI 2017 respondents who lived in those
   municipalities at 14. Prices: metro pay is divided by the metro price level P = 1 + s_h (R - 1), where R is a
   hedonic rent index (renters' monthly rent on dwelling characteristics and area, ENIGH 2024 dwellings) over the
   national person-weighted mean and s_h the national housing share of consumption (rent paid and owners' imputed
   rent over monetary spending plus imputed rent); other prices are taken as national [ASSUMPTION]. Checks: owners'
   estimated rents, controls for size only, the same index weighted by the metro's own basket (Paasche), CONEVAL's
   urban over national basket cost (August 2024). Variants: Mexico City alone (entidad 09; EMOVI residence at 14 in
   Mexico City), Guadalajara and Monterrey alone, localities of 100,000+ (ENIGH tam_loc 1; EMOVI's perceived city of
   100,000+), metro pay with national schooling, metro pay before prices, metro pay at CONEVAL's ratio. Moving inside
   Mexico is not free, and no metro could absorb the group's workers at its present pay, so this is an upper bound on
   the domestic option's value [INFERENCE]. Mexico's budget rows stay national.
2. US regional prices. Each member's US earnings at national US prices: divided by BEA's 2024 RPP (all items) of the
   household's state (CPS ASEC 2025 GESTFIPS). The PPP converts pesos at the US national price level, so this puts
   both sides on it. Check: the metropolitan area's RPP where the CPS identifies it (GTCBSA), else the state's
   metropolitan or nonmetropolitan portion. Variant: the group's US budget valuation divided by its person-weighted
   state RPP as well. Remittances stay nominal: the generation split of the measured total is the central's.
3. Services below US cost. Cash stays at $1 per $1 and schooling at 0 (its return is in the premium).
   (a) US health services (Medicaid, Medicare, public health and hospitals, and care received without pay) at the
       cost of the same quantity at Mexico's relative prices: V = G x r_health, r_health = ICP 2021 PPP for actual
       health over GDP PPP (0.8137); social services (income_security_services) at r_social, the PPP of individual
       consumption by government over GDP PPP (0.3974). The state-price overlay keeps its quantity share (V x r).
       Mexico's own public health, already at Mexican prices, at its cost (V/G = 1) [ASSUMPTION: the same rule].
   (b) Public goods at their responsive cost to others (the lane's response_only convention). Check: at their average
       cost times the ICP price ratio for collective government services over GDP (0.5994), Mexico's at average cost.
   (c) Beside: the Medicaid class at Finkelstein-Hendren-Luttmer's WTP per $1 of G (0.395, range 0.220-0.465), with
       the rows the lane couples to it (care received without pay, Mexico's public health).
   Central of the arm: (a) + (b). Range: health and social services both at 0.3974 or both at US cost.
Combined: arms 1 + 2 + 3(a) + 3(b).

Every row and weight is world_ledger.py's; an arm swaps its inputs (the premium table, the valuation lines) and the
two health row families it reprices. Gates: the staged sources' sha256; the central and the response_only central
equal world_ledger_oct07.csv; the national ENIGH cells equal mexico.py's; the premium table recomputed on national
cells equals g2_premium_lineage.csv; the row recomputations equal build_rows' at the lane's inputs. Sanity checks in
the meta: US/Mexico pay per worker against CMP's Ro, ENIGH's Mexico City pay by schooling against ENOE's, the price
levels.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/beside_arms.py
Outputs (derived/): beside_arms_oct07.csv (scenario x weighting x party, the central scenario), beside_arms_summary_oct07.csv
(per scenario at equal weights, lambda 1.16 and lambda_h), beside_arms_ratios.csv (metro pay ratios), beside_arms_meta_oct07.json.
"""
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

import g2_premium as G
import mexico as MX
import world_ledger as W

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
STAGE = REPO / "sources/immigration-fiscal/data/external/stage3"
CASE, BASIS = "oct07", "lineage"
MEMBERS = 42_752_213                      # the lineage (main case v5 on), per-member figures divide by it
# Staged with an ACQUIRED.md beside each (acquire_beside.py fetches a missing one): path, sha256, URL.
SOURCES = {
    "bea_sarpp": (STAGE / "bea/rpp_2024/SARPP.zip", "38713c6224c4c26ae020ffecd4549b82dca84f43d34f93dfdb43f4070cf011da",
                  "https://apps.bea.gov/regional/zip/SARPP.zip"),
    "bea_marpp": (STAGE / "bea/rpp_2024/MARPP.zip", "5dbf2e6ac2af222cc9abc205586c9b480344d89392752eb689c3ec823a34c83e",
                  "https://apps.bea.gov/regional/zip/MARPP.zip"),
    "bea_parpp": (STAGE / "bea/rpp_2024/PARPP.zip", "eb1378571316b22d5e7557b5565019cbe01fe1b5ea7dcdfcd979fc5751764f79",
                  "https://apps.bea.gov/regional/zip/PARPP.zip"),
    "icp2021": (STAGE / "worldbank/icp2021/icp2021_mex_usa.json",
                "996c9fc3425e89e132b7730c4936bc5f253141018dca0d4d9a955044fa1f2b9c",
                "https://api.worldbank.org/v2/sources/90/country/MEX;USA/series/1000000;9080000;1300000;1400000;9270000;"
                "9020000/classification/PPPGlob;PX.WL;EXR/time/YR2021/data?format=json&per_page=500"),
    "enigh_viviendas": (STAGE / "inegi/enigh2024_viviendas/enigh2024_ns_viviendas_csv.zip",
                        "ac1a56ed6e23b9feec952a28cb757fc0baa9a06fa303579996db9156553758cf",
                        "https://www.inegi.org.mx/contenidos/programas/enigh/nc/2024/microdatos/"
                        "enigh2024_ns_viviendas_csv.zip"),
    "coneval_lp": (STAGE / "coneval/lineas_pobreza_2024/Lineas_de_Pobreza_por_Ingresos_ago_2024.pdf",
                   "b73d6213944da1e1871a2f1aba1fe668f51115737e3eb0b2d047758aacb39cdd",
                   "https://www.coneval.org.mx/Medicion/Documents/Lineas_de_Pobreza_por_Ingresos/"
                   "Lineas_de_Pobreza_por_Ingresos_ago_2024.pdf"),
}
# CONEVAL, Lineas de Pobreza por Ingresos, agosto 2024, Cuadro 1, pesos per person per month: the poverty line (food
# and non-food basket) and the extreme-poverty line (food basket); rural is localities under 2,500.
CONEVAL_LPI = dict(urban=4564.96, rural=3296.89)
CONEVAL_FOOD = dict(urban=2354.65, rural=1800.55)
# Finkelstein, Hendren and Luttmer (JPE 2019), Table 3: recipients' WTP gamma(1) per recipient-year, by approach, against
# G = $3,600 (reads/finkelstein_hendren_luttmer_2019.md quotes 11-12). The middle approach is the central.
FHL_G, FHL_WTP = 3600.0, (793.0, 1421.0, 1675.0)
# ICP 2021 series (World Bank source 90): GDP, actual health, individual and collective consumption by government.
ICP_GDP, ICP_HEALTH, ICP_GOV_IND, ICP_GOV_COLL = "1000000", "9080000", "1300000", "1400000"
MIN_RATIO_N = 100                        # records behind a metro pay ratio before it pools across sex
CITIES = {1: "valle_de_mexico", 2: "guadalajara", 3: "monterrey"}
HEALTH_CLASSES = ("medicaid", "medicare", "health_services")
SOCIAL_LINES = ("income_security_services",)
WEIGHTINGS = ("equal", "equal_lambda_1.16", "equal_lambda_hendren_a")
MONEY = dict(inc="gross", net="income", tax="withheld", ctax="ctax")   # g2_premium's cell keys -> mexico.py's columns


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def check_sources():
    out = {}
    for k, (p, sha, url) in SOURCES.items():
        gate(f"source_{k}_present", p.is_file(), path=str(p), fetch="acquire_beside.py")
        got = sha256(p)
        gate(f"source_{k}_sha256", got == sha, path=str(p), got=got)
        out[k] = dict(path=str(p.relative_to(REPO)), sha256=sha, bytes=p.stat().st_size, url=url)
    return out


def as_written(df):
    """The table as g2_premium.py writes and world_ledger.py reads it back (%.6g), so an arm on national inputs
    reproduces the lane's central exactly."""
    return pd.read_csv(io.StringIO(df.to_csv(index=False, lineterminator="\n", float_format="%.6g")))


def max_diff(a, b):
    """Largest absolute difference; infinite when only one side is missing."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if (np.isnan(a) ^ np.isnan(b)).any():
        return np.inf
    d = np.abs(a - b)[~np.isnan(a)]
    return float(d.max()) if d.size else 0.0


# ------------------------------------------------------------------ Mexico: where the metro is
def metro_municipalities():
    """(entidad, municipio) -> city 1-3: every municipality ENOE 2024 Q1-Q2 samples under the self-representing
    cities 1 (Valle de Mexico), 2 (Guadalajara) and 3 (Monterrey), cd_a."""
    frames = []
    for q in (1, 2):
        with zipfile.ZipFile(MX.CACHE / f"enoe_2024_trim{q}_csv.zip") as z:
            frames.append(pd.read_csv(z.open(f"ENOE_SDEMT{q}24.csv"), encoding="latin-1", low_memory=False,
                                      usecols=["r_def", "c_res", "ent", "mun", "cd_a"]))
    e = pd.concat(frames, ignore_index=True)
    e = e[(pd.to_numeric(e.r_def, errors="coerce") == 0) & e.c_res.isin([1, 3])]
    e = pd.DataFrame({"cd": pd.to_numeric(e.cd_a, errors="coerce"), "ent": pd.to_numeric(e.ent, errors="coerce"),
                      "mun": pd.to_numeric(e.mun, errors="coerce")})
    m = e[e.cd.isin(CITIES) & e.mun.notna()].drop_duplicates().astype(int)
    gate("metro_municipality_in_one_city", not m.duplicated(["ent", "mun"]).any())
    states = {int(k): sorted(int(x) for x in s.unique()) for k, s in m.groupby("cd").ent}
    counts = {int(k): int(n) for k, n in m.groupby("cd").size().items()}
    # Mexico City's 16 alcaldias and 30 of the State of Mexico's municipalities; 8 in Jalisco; 13 in Nuevo Leon.
    gate("metro_cities_are_the_three_metros", states == {1: [9, 15], 2: [14], 3: [19]}
         and counts == {1: 46, 2: 8, 3: 13}, states=states, counts=counts)
    return {(r.ent, r.mun): r.cd for r in m.itertuples()}, dict(municipalities=counts)


def enigh_persons(munis):
    en = MX.load_enigh()
    geo = pd.read_csv(MX.CACHE / "enigh/concentradohogar.csv", dtype={"folioviv": str, "foliohog": str, "ubica_geo": str},
                      usecols=["folioviv", "foliohog", "ubica_geo", "tam_loc"])
    en = en.merge(geo, on=["folioviv", "foliohog"], how="left", validate="many_to_one")
    gate("enigh_every_person_located", bool(en.ubica_geo.notna().all()), missing=int(en.ubica_geo.isna().sum()))
    en["ent"] = en.ubica_geo.str[:2].astype(int)
    en["mun"] = en.ubica_geo.str[2:].astype(int)
    en["city"] = [munis.get(k, 0) for k in zip(en.ent, en.mun)]
    return en


def national_cells_gate(en, rates):
    """mexico.py's cells, recomputed from the same persons, equal its derived files (as written, %.6g)."""
    c = MX.cells(en)
    MX.add_ppp(c, rates)
    c["income_per_employed_ppp_gdp"] = c.income_per_employed_mxn / rates["PA.NUS.PPP"]
    for name, mine, keys in (("mexico_earnings_cells.csv", c, ["sex", "band", "cat"]),
                             ("mexico_young_by_parent.csv", MX.young_by_parent(en, rates), ["sex", "band", "parent_cat"])):
        ref = pd.read_csv(DERIVED / name)
        num = [x for x in ref.columns if x not in keys and pd.api.types.is_numeric_dtype(ref[x])]
        gate(f"national_cells_columns_{name}", set(num) <= set(mine.columns), missing=sorted(set(num) - set(mine.columns)))
        m = ref[keys + num].merge(as_written(mine[keys + num]), on=keys, suffixes=("", "_mine"), validate="one_to_one")
        diff = max(max_diff(m[x], m[f"{x}_mine"]) for x in num)
        gate(f"national_cells_reproduce_{name}", len(m) == len(ref) and diff == 0.0, rows=[len(m), len(ref)],
             max_abs_diff=diff)


def pay_ratios(en, sel, nat, young_nat):
    """The area's pay per person over the national cell of the same sex, age band and schooling, by sex x schooling
    (15+) and by sex x age band (15-24 by co-resident parents' schooling), for each money column, employment and
    weekly hours. Below MIN_RATIO_N records a cell pools across sex, then across all."""
    out = []
    for kind in ("adult", "young"):
        if kind == "adult":
            a = en[(en.age >= 15) & (en.cat >= 0)].copy()
            a["band"] = MX.age_band(a.age)
            ref, keys, by = nat.set_index(["sex", "band", "cat"]), ["sex", "band", "cat"], "cat"
        else:
            a = en[(en.age >= 15) & (en.age <= 24) & (en.parent_cat >= 0)].copy()
            a["band"] = np.where(a.age <= 19, "15-19", "20-24")
            a["parent_cat"] = a.parent_cat.astype(int)
            ref, keys, by = young_nat.set_index(["sex", "band", "parent_cat"]), ["sex", "band", "parent_cat"], "band"
        idx = pd.MultiIndex.from_frame(a[keys])
        cols = {k: f"{k}_per_person_mxn" for k in ("gross", "withheld", "ctax")} | {"income": "income_per_person_mxn"}
        for k, c in cols.items():
            a[f"num_{k}"] = a.w * a[MX.MONEY[k]]
            a[f"den_{k}"] = a.w * ref[c].reindex(idx).to_numpy()
        a["num_emp"] = a.w * a.employed
        a["den_emp"] = a.w * ref.employment_rate.reindex(idx).to_numpy()
        hn = (a.employed & a.hours.notna()).to_numpy()
        a["num_hrs"] = np.where(hn, a.w * a.hours.fillna(0), 0.0)
        a["den_hrs"] = np.where(hn, a.w * ref.weekly_hours_employed.reindex(idx).fillna(0).to_numpy(), 0.0)
        gate(f"pay_ratio_national_cells_found_{kind}", bool(np.isfinite(a[[c for c in a if c.startswith("den_")]]
                                                                         ).all().all()))
        s = a[sel(a)]
        parts = list(cols) + ["emp", "hrs"]
        sums = lambda t: pd.Series({"n": len(t), **{f"{p}_{x}": t[f"{x}_{p}"].sum() for p in parts
                                                     for x in ("num", "den")}})
        full = s.groupby(["sex", by]).apply(sums, include_groups=False)
        pooled = s.groupby(by).apply(sums, include_groups=False)
        everyone = sums(s)
        levels = sorted(a[by].unique())
        for sex in ("female", "male"):
            for b in levels:
                r, level = (full.loc[(sex, b)], "sex") if (sex, b) in full.index else (None, None)
                if r is None or r.n < MIN_RATIO_N:
                    r, level = (pooled.loc[b], "pooled_sex") if b in pooled.index else (None, None)
                if r is None or r.n < MIN_RATIO_N:
                    r, level = everyone, "all"
                out.append(dict(kind=kind, sex=sex, key=b, n=int(full.loc[(sex, b)].n) if (sex, b) in full.index else 0,
                                n_used=int(r.n), level=level,
                                **{f"R_{p}": float(r[f"{p}_num"] / r[f"{p}_den"]) for p in parts}))
    return pd.DataFrame(out)


def area_cells(ppp, ratios, price):
    """g2_premium's lookup dicts for one PPP, every money column scaled by the area's pay ratio and divided by its
    price level, employment (capped at 1) and hours by theirs."""
    nat = G.mexico_cells(ppp)
    rat = {(r.kind, r.sex, r.key): r for r in ratios.itertuples()}
    out = {}
    for pre, kind, pos in (("", "adult", 2), ("y", "young", 1)):
        rk = lambda k: rat[(kind, k[0], k[pos])]
        for m, col in MONEY.items():
            out[pre + m] = {k: v * getattr(rk(k), f"R_{col}") / price for k, v in nat[pre + m].items()}
        out[pre + "emp"] = {k: min(v * rk(k).R_emp, 1.0) for k, v in nat[pre + "emp"].items()}
        out[pre + "hrs"] = {k: v * rk(k).R_hrs for k, v in nat[pre + "hrs"].items()}
    return out


def transition_dict(t, fallback=None):
    """g2_premium.transitions() on a given EMOVI table: P(own | parents, sex, cohort), pooled to the cohort, then to
    all, below g2_premium's 30 cases. A parents' category with too few cases even pooled takes the fallback's."""
    out, used = {}, {}
    levels = [("sex", "cohort"), ("cohort",), ()]
    for sex in ("male", "female"):
        for coh in ("1953-62", "1963-72", "1973-82", "1983-92"):
            for pc in range(6):
                for lev in levels:
                    s = t[t.parent_cat.eq(pc)]
                    if "sex" in lev:
                        s = s[s.sex.eq(sex)]
                    if "cohort" in lev:
                        s = s[s.cohort.eq(coh)]
                    if s.n.sum() >= G.MIN_N:
                        v = s.groupby("own_cat").w.sum()
                        out[(sex, coh, pc)] = (v.reindex(range(6), fill_value=0) / v.sum()).to_numpy()
                        used[(sex, coh, pc)] = "+".join(lev) or "all"
                        break
                else:
                    gate(f"transition_fallback_exists_{pc}", fallback is not None)
                    out[(sex, coh, pc)] = fallback[(sex, coh, pc)]
                    used[(sex, coh, pc)] = "national"
    return out, used


def emovi_with_residence(munis):
    em = MX.load_emovi()
    with pd.io.stata.StataReader(MX.CACHE / "emovi" / "ESRU-EMOVI 2017 Entrevistado.dta") as r:
        x = r.read(convert_categoricals=False, columns=["p23", "p23_1", "p24"])
    gate("emovi_residence_rows_align", len(x) == len(em) == 17665, rows=[len(x), len(em)])
    # p23_1 is the municipality at 14 as state x 1000 + municipality; p23 the state; p24 the perceived locality size
    # (1 metropolis over 500,000, 2 city of 100,000-500,000).
    code = x.p23_1.fillna(-1).astype(int).to_numpy()
    em["city14"] = [munis.get((c // 1000, c % 1000), 0) if c > 0 else 0 for c in code]
    em["cdmx14"] = (x.p23 == 9).to_numpy()
    em["city100k14"] = x.p24.isin([1, 2]).to_numpy()
    return em


# ------------------------------------------------------------------ Mexico: what the metro costs
def dwellings(munis):
    with zipfile.ZipFile(SOURCES["enigh_viviendas"][0]) as z:
        v = pd.read_csv(z.open("viviendas.csv"), dtype=str, low_memory=False)
    num = lambda c: pd.to_numeric(v[c].str.strip(), errors="coerce")
    v["ent"] = v.ubica_geo.str[:2].astype(int)
    v["mun"] = v.ubica_geo.str[2:].astype(int)
    v["city"] = [munis.get(k, 0) for k in zip(v.ent, v.mun)]
    v["tam"] = num("tam_loc")
    v["area"] = np.select([v.ent.eq(9) & v.city.eq(1), v.city.eq(1), v.city.eq(2), v.city.eq(3), v.tam.eq(1),
                           v.tam.eq(2), v.tam.eq(3)], ["cdmx", "vdm_edomex", "guadalajara", "monterrey", "other_100k",
                                                       "loc_15k_100k", "loc_2500_15k"], "rural")
    v["w"] = num("factor")
    v["persons"] = v.w * num("tot_resid")
    v["ten"] = num("tenencia")
    v["rent"] = num("renta")
    v["est"] = num("estim_pago")
    X = pd.DataFrame(index=v.index)
    for c, cap in (("num_cuarto", 10), ("cuart_dorm", 6), ("bano_comp", 4), ("focos", 30)):
        X[c] = num(c).clip(upper=cap).fillna(0.0)
    age = num("antiguedad")
    X["age"] = age.fillna(age.median()).clip(upper=80)
    X["age2"] = X.age ** 2 / 100
    X["age_missing"] = age.isna().astype(float)
    for c in ("tipo_viv", "mat_pared", "mat_techos", "mat_pisos", "agua_ent", "drenaje", "excusado", "disp_elect",
              "cocina", "lugar_coc", "combus", "eli_basura"):
        X = X.join(pd.get_dummies(v[c].str.strip().replace("", "na"), prefix=c, drop_first=True, dtype=float))
    return v, X


AREAS = ["cdmx", "vdm_edomex", "guadalajara", "monterrey", "other_100k", "loc_15k_100k", "loc_2500_15k", "rural"]


def hedonic(v, X, y, mask):
    """Weighted least squares of log monthly rent on area dummies and dwelling characteristics; the areas' rent
    levels exp(beta) over their national person-weighted mean."""
    A = pd.get_dummies(v.area, dtype=float)[AREAS]
    Xm = pd.concat([A[mask], X[mask]], axis=1)
    Xm = Xm.loc[:, (Xm.std() > 0) | Xm.columns.isin(AREAS)]
    w = v.w[mask].to_numpy(float)
    ly = np.log(y[mask].to_numpy(float))
    b, *_ = np.linalg.lstsq(Xm.to_numpy(float) * np.sqrt(w)[:, None], ly * np.sqrt(w), rcond=None)
    lvl = pd.Series(np.exp(b[:len(AREAS)]), index=AREAS)
    pop = v.groupby("area").persons.sum().reindex(AREAS)
    R = lvl / ((lvl * pop).sum() / pop.sum())
    res = ly - Xm.to_numpy(float) @ b
    r2 = 1 - np.average(res ** 2, weights=w) / np.average((ly - np.average(ly, weights=w)) ** 2, weights=w)
    return R, dict(n=int(mask.sum()), r2=float(r2), regressors=int(Xm.shape[1]))


def price_levels(munis, en):
    v, X = dwellings(munis)
    gate("dwellings_cover_every_household", set(v.folioviv) >= set(en.folioviv), missing=len(set(en.folioviv) - set(v.folioviv)))
    renters = v.ten.eq(1) & v.rent.gt(0)
    owners = v.ten.isin([3, 4]) & v.est.gt(0)
    R, fit = hedonic(v, X, v.rent, renters)
    Ro, fit_o = hedonic(v, X, v.est, owners)
    # Check: controls for size only (rooms, bedrooms, bathrooms). The full set also holds water, drainage and
    # materials fixed, which metro dwellings have more of; part of that may be the place, not the dwelling.
    Rs, fit_s = hedonic(v, X[["num_cuarto", "cuart_dorm", "bano_comp"]], v.rent, renters)
    c = pd.read_csv(MX.CACHE / "enigh/concentradohogar.csv", dtype={"folioviv": str},
                    usecols=["folioviv", "tam_loc", "factor", "tot_integ", "alquiler", "estim_alqu", "gasto_mon"])
    c = c.merge(v[["folioviv", "area"]], on="folioviv", how="left", validate="many_to_one")
    gate("households_have_an_area", bool(c.area.notna().all()))
    c["hous"], c["cons"] = c.alquiler + c.estim_alqu, c.gasto_mon + c.estim_alqu
    share = lambda t: float((t.factor * t.hous).sum() / (t.factor * t.cons).sum())
    s_h = share(c)
    gate("housing_share_plausible", 0.1 < s_h < 0.3, s_h=s_h)
    # Each variant's rent level: its persons' mean of their area's index; the large-localities variant takes the
    # index of the area each tam_loc-1 dwelling sits in.
    v["R"], v["Ro"], v["Rs"] = v.area.map(R), v.area.map(Ro), v.area.map(Rs)
    sets = {"metros": v.city.gt(0), "cdmx": v.ent.eq(9), "guadalajara": v.city.eq(2), "monterrey": v.city.eq(3),
            "large_localities": v.tam.eq(1)}
    hh = {"metros": c.area.isin(AREAS[:4]), "cdmx": c.area.eq("cdmx"), "guadalajara": c.area.eq("guadalajara"),
          "monterrey": c.area.eq("monterrey"), "large_localities": c.tam_loc.eq(1)}
    urban = float((c.factor * c.tot_integ)[c.tam_loc.isin([1, 2, 3])].sum() / (c.factor * c.tot_integ).sum())
    coneval = CONEVAL_LPI["urban"] / (urban * CONEVAL_LPI["urban"] + (1 - urban) * CONEVAL_LPI["rural"])
    out = dict(housing_share_national=s_h, rent_index_renters=R.to_dict(), rent_index_owners=Ro.to_dict(),
               rent_index_renters_size_only=Rs.to_dict(), hedonic_renters=fit, hedonic_owners=fit_o,
               hedonic_renters_size_only=fit_s, urban_person_share=urban, coneval_urban_over_national=coneval,
               coneval_food_urban_over_national=CONEVAL_FOOD["urban"] / (urban * CONEVAL_FOOD["urban"]
                                                                        + (1 - urban) * CONEVAL_FOOD["rural"]),
               variants={})
    for k, m in sets.items():
        rr, ro, rs = (float(np.average(v[x][m], weights=v.persons[m])) for x in ("R", "Ro", "Rs"))
        s_m = share(c[hh[k]])
        out["variants"][k] = dict(rent_index=rr, rent_index_owners=ro, rent_index_size_only=rs,
                                  price_level=1 + s_h * (rr - 1), price_level_owners=1 + s_h * (ro - 1),
                                  price_level_size_only=1 + s_h * (rs - 1), housing_share_own=s_m,
                                  price_level_paasche=1 / (s_m / rr + (1 - s_m)))
    return out


# ------------------------------------------------------------------ US: where the group lives
def bea_2024(key, member):
    with zipfile.ZipFile(SOURCES[key][0]) as z:
        t = pd.read_csv(z.open(member), dtype={"GeoFIPS": str}, skipinitialspace=True, encoding="latin-1")
    t = t[pd.to_numeric(t.LineCode, errors="coerce").eq(1)]
    out = {f.strip(): float(x) for f, x in zip(t.GeoFIPS, t["2024"])}
    gate(f"bea_{key}_us_is_100", out.get("00000") == 100.0)
    return out


def residence_prices(d):
    """Each CPS record's 2024 RPP: the state's (central), and the metropolitan area's where identified, else the
    state's metropolitan or nonmetropolitan portion (check)."""
    spec = G.importlib.util.spec_from_file_location("dist_base", G.FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = G.importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS", "GTCBSA", "GTMETSTA"])
    h = h.set_index("H_SEQ")
    gate("cps_households_found", bool(d.PH_SEQ.isin(h.index).all()))
    st = h.GESTFIPS.reindex(d.PH_SEQ).to_numpy()
    cbsa = h.GTCBSA.reindex(d.PH_SEQ).to_numpy()
    met = h.GTMETSTA.reindex(d.PH_SEQ).to_numpy()
    sa, ma, pa = bea_2024("bea_sarpp", "SARPP_STATE_2008_2024.csv"), bea_2024("bea_marpp", "MARPP_MSA_2008_2024.csv"), \
        bea_2024("bea_parpp", "PARPP_PORT_2008_2024.csv")
    state = np.array([sa.get(f"{s:02d}000", np.nan) for s in st])
    gate("every_state_has_an_rpp", bool(np.isfinite(state).all()))
    metro, how = [], []
    for s, c, m, sv in zip(st, cbsa, met, state):
        if c > 0 and f"{c:05d}" in ma:
            metro.append(ma[f"{c:05d}"]), how.append("msa")
        elif m in (1, 2) and f"{s:02d}{998 if m == 1 else 999}" in pa:
            metro.append(pa[f"{s:02d}{998 if m == 1 else 999}"]), how.append("portion")
        else:
            metro.append(sv), how.append("state")
    return state, np.array(metro), np.array(how)


# ------------------------------------------------------------------ the premium table
def premium_table(d, parents, trans, cells_by_ppp):
    """The g2_premium.csv rows world_ledger.premium_rows reads (and the CMP check's), recomputed on the given US
    earnings (d.earn), Mexico cells and EMOVI transitions, as g2_premium.main builds them."""
    rows = []
    for ppp in ("gdp", "consumption"):
        cells = cells_by_ppp[ppp]
        g1 = d[d.gen.eq("G1")]
        for scope, sub in (("all_ages", g1), ("25_64_arrived_20plus", g1[g1.A_AGE.between(25, 64)
                                                                         & (g1.arrival_age >= 20)])):
            e = G.mexico_own_schooling(sub, cells, 0.25, False)
            for sel, delta in G.G1_SELECTION.items():
                rows.append(G.summarize("G1", f"own_schooling_{scope}", sub, e, delta,
                                        dict(ppp=ppp, diploma_reread=0.25, mishra=False, selection=sel)))
        g2 = d[d.gen.eq("G2")]
        e = G.mexico_rearing(g2, parents, trans, cells, 0.25, False)
        for sel, delta in G.G2_INHERITED.items():
            rows.append(G.summarize("G2", "rearing", g2, e, delta,
                                    dict(ppp=ppp, diploma_reread=0.25, mishra=False, selection=sel)))
        if ppp != "gdp":
            continue
        tmp = g2.assign(**{f"mx_{m}": v for m, v in e.items()}, band=np.where(g2.A_AGE < 15, "0-14", G.band_of(g2.A_AGE)))
        ratio = {m: {} for m in G.MONEY}
        for (sx, b), s in tmp[tmp.A_AGE >= 15].groupby(["sex", "band"]):
            for m in G.MONEY:
                ratio[m][(sx, b)] = (s.pw * s[f"mx_{m}"]).sum() / max((s.pw * s.earn).sum(), 1.0)
        e2 = G.mexico_own_schooling(g2, cells, 0.0, False)
        for sel, delta in G.G2_INHERITED.items():
            rows.append(G.summarize("G2", "own_us_schooling", g2, e2, delta,
                                    dict(ppp=ppp, diploma_reread=0.0, mishra=False, selection=sel)))
        g3 = d[d.gen.eq("G3+")]
        e3 = {m: np.array([ratio[m].get((sx, b), np.nan) if a >= 15 else 0.0
                           for sx, b, a in zip(g3.sex, G.band_of(g3.A_AGE), g3.A_AGE)]) * g3.earn.to_numpy()
              for m in G.MONEY}
        e3["emp"] = e3["hw"] = np.zeros(len(g3))
        rows.append(G.summarize("G3+", "bound_upper_g2_ratio", g3, e3, 0.0,
                                dict(ppp=ppp, diploma_reread=0.25, mishra=False, selection="none")))
    return as_written(pd.DataFrame(rows))


def premium_table_gate(table):
    ref = pd.read_csv(DERIVED / "g2_premium_lineage.csv")
    keys = ["generation", "convention", "ppp", "diploma_reread", "mishra", "selection"]
    m = table.merge(ref, on=keys, suffixes=("", "_ref"), how="left", validate="one_to_one", indicator=True)
    num = [c for c in table.columns if c not in keys and pd.api.types.is_numeric_dtype(table[c])]
    diff = max(max_diff(m[c], m[f"{c}_ref"]) for c in num)
    gate("premium_table_reproduces_g2_premium_lineage", bool(m._merge.eq("both").all()) and diff == 0.0, rows=len(m),
         max_abs_diff=diff)


# ------------------------------------------------------------------ the rows an arm reprices
def health_rows(rows, I, pgc, care_vg=None, mexico_health_vg=None):
    """build_rows' two health row families at other V/G: care received without pay (uncompensated_received_*) and
    Mexico's budget forgone (mexico_budget_lost_*, its health part); None keeps the lane's (health_vg)."""
    rows = rows.copy().set_index("row")
    hv = I["health_vg"]
    cv, mv = care_vg or hv, mexico_health_vg or hv
    unc = I["ch"].loc["unreimbursed_care"]
    pop = W.population_shares(I)["pop"]
    mx = I["mxb"]
    for g in W.GENS:
        rows.loc[f"uncompensated_received_{g}", ["low", "central", "high"]] = [
            min(-unc.bn_low, -unc.bn_high) * cv[0] * pop[g], -unc.bn_central * cv[1] * pop[g],
            max(-unc.bn_low, -unc.bn_high) * cv[2] * pop[g]]
        s = mx[mx.generation == g].set_index("item")
        he = float(s.filter(like="health", axis=0).bn.iloc[0])
        cash = float(s[s.cls == "cash"].bn.sum())
        pg = float(s[s.cls == "public_good"].bn.iloc[0])
        pg_val = pg if pgc == "average_cost" else pg * W.MEXICO_PUBLIC_RESPONSE[1]
        rows.loc[f"mexico_budget_lost_{g}", ["low", "central", "high"]] = [
            -(he * mv[2] + cash + pg_val), -(he * mv[1] + cash + pg_val), -(he * mv[0] + cash + pg_val)]
    return rows.reset_index()


def services_at_prices(vgen, r_health, r_social, medicaid_vg=None):
    """valuation_by_generation's lines with US health at V = G x r_health (the state-price overlay keeps its quantity
    share, V x r_health), social services at G x r_social; medicaid_vg, if given, prices the Medicaid class at its
    WTP per $1 of G instead."""
    v = vgen.copy()
    vcols = ["V_low_bn", "V_central_bn", "V_high_bn"]
    health = v.cls.isin(HEALTH_CLASSES)
    overlay = v.line.str.startswith("state_price_")
    for c in vcols:
        v.loc[health & ~overlay, c] = v.loc[health & ~overlay, "G_bn"] * r_health
        v.loc[health & overlay, c] = v.loc[health & overlay, c] * r_health
        v.loc[v.line.isin(SOCIAL_LINES), c] = v.loc[v.line.isin(SOCIAL_LINES), "G_bn"] * r_social
    if medicaid_vg is not None:
        for c, x in zip(vcols, medicaid_vg):
            v.loc[v.cls.eq("medicaid"), c] = v.loc[v.cls.eq("medicaid"), "G_bn"] * x
    return v


def public_goods_at_prices(vgen, r):
    """The check beside 3(b): US public goods at their average cost times Mexico's price ratio for collective
    government services (Mexico's own stay at average cost)."""
    v = vgen.copy()
    m = v.cls.eq("public_good")
    for c in ("V_low_bn", "V_central_bn", "V_high_bn"):
        v.loc[m, c] = v.loc[m, c] * r
    return v


def cmp_cell(d, cells):
    """Near CMP's own cell (a 35-year-old urban man with nine years of schooling, arrived at 20 or older): men born in
    Mexico aged 30-44 with nine to eleven years (secundaria) who arrived at 20 or older (35-39 alone has 22 records).
    US earnings per worker over Mexico's gross pay per employed person in their cells, at p56."""
    s = d[d.gen.eq("G1") & d.sex.eq("male") & d.A_AGE.between(30, 44) & d.own_cat.eq(3) & (d.arrival_age >= 20)]
    e = G.mexico_own_schooling(s, cells, 0.25, False)
    w = s.pw.to_numpy()
    us = float((w * s.earn).sum() / (w * s.works).sum())
    mx = float((w * e["inc"]).sum() * (1 + G.G1_SELECTION["p56"]) / (w * e["emp"]).sum())
    return dict(records=int(len(s)), us_per_worker=us, mexico_per_worker=mx, ratio=us / mx)


def evaluate(I, fac, pgc="average_cost", care_vg=None, mexico_health_vg=None, remit_rows=None, budget_deflator=None):
    rows, prem, _ = W.build_rows(I, pgc)
    if care_vg is not None or mexico_health_vg is not None:
        rows = health_rows(rows, I, pgc, care_vg, mexico_health_vg)
    if remit_rows is not None:
        # Remittances are a measured dollar total; the split by generation stays the central's (nominal G2 earnings).
        rows = rows.set_index("row")
        rows.loc[remit_rows.index, ["low", "central", "high"]] = remit_rows[["low", "central", "high"]]
        rows = rows.reset_index()
    if budget_deflator is not None:
        for g, f in budget_deflator.items():
            m = rows.row.eq(f"us_budget_value_{g}")
            rows.loc[m, ["low", "central", "high"]] = rows.loc[m, ["low", "central", "high"]] / f
    t = W.totals(rows, prem, I, "central", fac, I["pos"])
    return rows, prem, t


def summary_row(name, arm, label, rows, t, base):
    out = []
    piv = t.set_index(["weighting", "party"]).bn
    c = rows.set_index("row").central
    for wt in WEIGHTINGS:
        g = lambda p: float(piv[(wt, p)])
        out.append(dict(scenario=name, arm=arm, label=label, weighting=wt,
                        premium_G1_bn=c["premium_G1"], premium_G2_bn=c["premium_G2"], premium_G3plus_bn=c["premium_G3+"],
                        premium_bn=sum(c[f"premium_{x}"] for x in W.GENS),
                        us_budget_value_bn=sum(c[f"us_budget_value_{x}"] for x in W.GENS),
                        group_total_bn=g("group_total"), others_today_bn=g("others_today"),
                        future_taxpayers_bn=g("future_taxpayers"), mexico_residents_bn=g("mexico_residents"),
                        world_total_bn=g("world_total"), us_residents_incl_group_bn=g("us_residents_total") + g("group_total"),
                        group_per_member_usd=g("group_total") * 1e9 / MEMBERS, breakeven_w=g("breakeven_w"),
                        breakeven_w_us_only=g("breakeven_w_us_only"),
                        world_change_bn=g("world_total") - base[(wt, "world_total")]))
    return out


def main():
    srcs = check_sources()
    I = W.load(CASE, BASIS)
    fac = W.channel_factors(I, "money")
    fac["_lambda"] = {f"equal_lambda_{k}": v for k, v in W.LAMBDAS.items()}
    fac["_lambda"]["equal_lambda_hendren_a"] = fac["fiscal_a"]["inv_g"]

    # ---- the lane's central and response_only central, reproduced
    ref = pd.read_csv(DERIVED / f"world_ledger_{CASE}.csv")
    ref = ref[(ref.mexico_taxes == "withheld_consumption") & (ref.scenario == "central_g3_zero")]
    rows0, _, t0 = evaluate(I, fac)
    _, _, t0b = evaluate(I, fac, "response_only")
    for pgc, t in (("average_cost", t0), ("response_only", t0b)):
        r = ref[ref.pg_convention == pgc]
        m = t.merge(r, on=["weighting", "party"], suffixes=("", "_ref"), validate="one_to_one")
        diff = max_diff(m.bn, m.bn_ref)
        gate(f"central_reproduces_world_ledger_{pgc}", len(m) == len(t) == len(r) > 0 and diff < 1e-6,
             rows=[len(m), len(t), len(r)], max_abs_diff=diff)
    rh = health_rows(rows0, I, "average_cost")
    gate("health_rows_reproduce_build_rows", bool(np.allclose(rh[["low", "central", "high"]], rows0[["low", "central",
                                                                                                    "high"]], atol=1e-12)))
    base = t0.set_index(["weighting", "party"]).bn
    remit0 = rows0.set_index("row").loc[["remit_G1", "remit_G2"]]

    # ---- inputs: the US records, Mexico's persons, cells, transitions and prices
    d = G.load_asec(BASIS)
    persons = float(d.pw[d.gen.ne("")].sum())
    gate("members_are_the_lineage", abs(persons - MEMBERS) < 1.0, persons=persons)
    parents, _ = G.parents_schooling()
    trans_nat = G.transitions()
    nat_cells = {p: G.mexico_cells(p) for p in ("gdp", "consumption")}
    tab0 = premium_table(d, parents, trans_nat, nat_cells)
    premium_table_gate(tab0)
    munis, munis_meta = metro_municipalities()
    en = enigh_persons(munis)
    rates = MX.ppp()
    national_cells_gate(en, rates)
    nat = pd.read_csv(DERIVED / "mexico_earnings_cells.csv")
    nat_y = pd.read_csv(DERIVED / "mexico_young_by_parent.csv")
    em = emovi_with_residence(munis)
    tr_check, _ = transition_dict(pd.read_csv(DERIVED / "mexico_transition.csv"))
    gate("transition_dict_reproduces_g2_premium", all(np.array_equal(tr_check[k], trans_nat[k]) for k in trans_nat))
    prices = price_levels(munis, en)
    variants = {   # area selection on ENIGH persons, EMOVI residence at 14, price variant
        "metros": (lambda a: a.city.gt(0).to_numpy(), em.city14.gt(0), "metros"),
        "cdmx": (lambda a: a.ent.eq(9).to_numpy(), em.cdmx14, "cdmx"),
        "guadalajara": (lambda a: a.city.eq(2).to_numpy(), em.city14.eq(2), "guadalajara"),
        "monterrey": (lambda a: a.city.eq(3).to_numpy(), em.city14.eq(3), "monterrey"),
        "large_localities": (lambda a: a.tam_loc.eq(1).to_numpy(), em.city100k14, "large_localities"),
    }
    ratios, trans, used = {}, {}, {}
    for k, (sel, emask, _) in variants.items():
        ratios[k] = pay_ratios(en, sel, nat, nat_y)
        tt, _, _ = MX.transitions(em[emask.to_numpy()])
        trans[k], used[k] = transition_dict(tt, fallback=trans_nat)
    state_rpp, metro_rpp, how = residence_prices(d)
    d["rpp_state"], d["rpp_metro"], d["rpp_how"] = state_rpp, metro_rpp, how
    d_state = d.assign(earn=d.earn / (d.rpp_state / 100))
    d_metro = d.assign(earn=d.earn / (d.rpp_metro / 100))
    grp = d[d.gen.ne("")]
    rpp_by_gen = {g: dict(persons=float(np.average(s.rpp_state, weights=s.pw)),
                          earnings=float(np.average(s.rpp_state, weights=s.pw * s.earn)),
                          persons_metro=float(np.average(s.rpp_metro, weights=s.pw)),
                          earnings_metro=float(np.average(s.rpp_metro, weights=s.pw * s.earn)))
                  for g, s in grp.groupby("gen")}
    icp = {}
    for x in json.load(open(SOURCES["icp2021"][0]))["source"]["data"]:
        v = {y["concept"]: y["id"] for y in x["variable"]}
        icp[(v["Country"], v["Series"], v["Classification"])] = x["value"]
    ppp_icp = lambda s: icp[("MEX", s, "PPPGlob")]
    r_health = ppp_icp(ICP_HEALTH) / ppp_icp(ICP_GDP)
    r_social = ppp_icp(ICP_GOV_IND) / ppp_icp(ICP_GDP)
    r_public = ppp_icp(ICP_GOV_COLL) / ppp_icp(ICP_GDP)
    gate("icp_ratios_plausible", 0.2 < r_social < r_public < r_health < 1.0, r_health=r_health, r_social=r_social,
         r_public=r_public)
    fhl = tuple(x / FHL_G for x in FHL_WTP)

    # ---- the scenarios
    def cells_for(k, deflate=True, price=None):
        p = price if price is not None else (prices["variants"][variants[k][2]]["price_level"] if deflate else 1.0)
        return {pp: area_cells(pp, ratios[k], p) for pp in ("gdp", "consumption")}

    tables = {
        "arm1_metros": premium_table(d, parents, trans["metros"], cells_for("metros")),
        "arm1_metros_nominal": premium_table(d, parents, trans["metros"], cells_for("metros", deflate=False)),
        "arm1_metros_coneval": premium_table(d, parents, trans["metros"],
                                             cells_for("metros", price=prices["coneval_urban_over_national"])),
        "arm1_metros_national_schooling": premium_table(d, parents, trans_nat, cells_for("metros")),
        "arm1_cdmx": premium_table(d, parents, trans["cdmx"], cells_for("cdmx")),
        "arm1_guadalajara": premium_table(d, parents, trans["guadalajara"], cells_for("guadalajara")),
        "arm1_monterrey": premium_table(d, parents, trans["monterrey"], cells_for("monterrey")),
        "arm1_large_localities": premium_table(d, parents, trans["large_localities"], cells_for("large_localities")),
        "arm2_state_rpp": premium_table(d_state, parents, trans_nat, nat_cells),
        "arm2_metro_rpp": premium_table(d_metro, parents, trans_nat, nat_cells),
        "combined": premium_table(d_state, parents, trans["metros"], cells_for("metros")),
        "combined_cdmx": premium_table(d_state, parents, trans["cdmx"], cells_for("cdmx")),
    }
    v3a = services_at_prices(I["vgen"], r_health, r_social)
    hcare, hmx = (r_health,) * 3, (1.0,) * 3
    S = []   # (name, arm, label, I, kwargs)
    S.append(("baseline", "central", "the lane's central (oct07, lineage, average cost, withheld + consumption taxes)",
              I, {}))
    labels1 = dict(arm1_metros="three metros, metro schooling, hedonic price level (central)",
                   arm1_metros_nominal="three metros before the price level",
                   arm1_metros_coneval="three metros at CONEVAL's urban/national basket ratio (check)",
                   arm1_metros_national_schooling="three metros' pay, national schooling transitions",
                   arm1_cdmx="Mexico City alone", arm1_guadalajara="Guadalajara alone (check)",
                   arm1_monterrey="Monterrey alone (check)", arm1_large_localities="localities of 100,000+ (check)")
    for k, lab in labels1.items():
        S.append((k, "1", lab, dict(I, g2=tables[k]), {}))
    S.append(("arm2_state_rpp", "2", "US earnings at national prices, state RPP (central)",
              dict(I, g2=tables["arm2_state_rpp"]), dict(remit_rows=remit0)))
    S.append(("arm2_metro_rpp", "2", "US earnings at national prices, metro RPP where identified (check)",
              dict(I, g2=tables["arm2_metro_rpp"]), dict(remit_rows=remit0)))
    S.append(("arm2_state_rpp_budget", "2", "state RPP on earnings and on the group's US budget valuation",
              dict(I, g2=tables["arm2_state_rpp"]),
              dict(remit_rows=remit0, budget_deflator={g: rpp_by_gen[g]["persons"] / 100 for g in W.GENS})))
    S.append(("arm3a", "3", "US health at Mexican relative prices, social services at government prices",
              dict(I, vgen=v3a), dict(care_vg=hcare, mexico_health_vg=hmx)))
    S.append(("arm3a_mexico_health_lane", "3", "3a with Mexico's public health at the lane's V/G",
              dict(I, vgen=v3a), dict(care_vg=hcare)))
    S.append(("arm3b", "3", "public goods at their responsive cost (the lane's response_only)", I,
              dict(pgc="response_only")))
    S.append(("arm3", "3", "3a + 3b (central)", dict(I, vgen=v3a),
              dict(pgc="response_only", care_vg=hcare, mexico_health_vg=hmx)))
    S.append(("arm3b_icp", "3", f"public goods at average cost x the ICP collective-government ratio {r_public:.4f} "
              "(check on 3b)", dict(I, vgen=public_goods_at_prices(I["vgen"], r_public)), {}))
    S.append(("arm3_icp", "3", "3a + the ICP check on 3b", dict(I, vgen=public_goods_at_prices(v3a, r_public)),
              dict(care_vg=hcare, mexico_health_vg=hmx)))
    for lo_hi, rr in (("low", r_social), ("high", 1.0)):
        S.append((f"arm3_{lo_hi}", "3", f"3a + 3b with health and social services at {rr:.4f} of US cost",
                  dict(I, vgen=services_at_prices(I["vgen"], rr, rr)),
                  dict(pgc="response_only", care_vg=(rr,) * 3, mexico_health_vg=hmx)))
    S.append(("arm3c_fhl", "3", "3a + 3b with the Medicaid class at FHL's WTP (check)",
              dict(I, vgen=services_at_prices(I["vgen"], r_health, r_social, medicaid_vg=(fhl[1],) * 3)),
              dict(pgc="response_only", care_vg=(fhl[1],) * 3, mexico_health_vg=(fhl[1],) * 3)))
    for lo_hi, x in (("low", fhl[0]), ("high", fhl[2])):
        S.append((f"arm3c_fhl_{lo_hi}", "3", f"3c at FHL's {lo_hi} WTP, {x:.3f}",
                  dict(I, vgen=services_at_prices(I["vgen"], r_health, r_social, medicaid_vg=(x,) * 3)),
                  dict(pgc="response_only", care_vg=(x,) * 3, mexico_health_vg=(x,) * 3)))
    S.append(("combined", "combined", "arms 1 + 2 + 3a + 3b (central)", dict(I, g2=tables["combined"], vgen=v3a),
              dict(pgc="response_only", care_vg=hcare, mexico_health_vg=hmx, remit_rows=remit0)))
    S.append(("combined_cdmx", "combined", "the combination with Mexico City as arm 1",
              dict(I, g2=tables["combined_cdmx"], vgen=v3a),
              dict(pgc="response_only", care_vg=hcare, mexico_health_vg=hmx, remit_rows=remit0)))
    S.append(("combined_icp", "combined", "the combination with the ICP check in place of 3b",
              dict(I, g2=tables["combined"], vgen=public_goods_at_prices(v3a, r_public)),
              dict(care_vg=hcare, mexico_health_vg=hmx, remit_rows=remit0)))

    long, summ, detail = [], [], {}
    for name, arm, label, Ia, kw in S:
        rows, prem, t = evaluate(Ia, fac, **kw)
        if name == "baseline":
            gate("baseline_is_the_central", float((t.bn - t0.bn).abs().max()) == 0.0)
        if name == "arm3b":
            gate("arm3b_is_the_response_only_central", float((t.bn - t0b.bn).abs().max()) == 0.0)
        long.append(t.assign(case=CASE, scenario=name, arm=arm))
        summ += summary_row(name, arm, label, rows, t, base)
        detail[name] = dict(e_mx_central_bn={g: prem[g]["e_mx"]["central"] for g in W.GENS},
                            e_us_bn={g: prem[g]["e_us"] for g in W.GENS},
                            mexico_taxes_central_bn={g: prem[g]["tax"]["central"] + prem[g]["ctax"]["central"]
                                                     for g in W.GENS})
    res = pd.concat(long)[["case", "scenario", "arm", "weighting", "party", "bn", "unknown_rows"]]
    summary = pd.DataFrame(summ)
    # The combination's parts: each arm's change at equal weights, beside the combination's (they interact).
    eq = summary[summary.weighting == "equal"].set_index("scenario").world_change_bn
    parts = {k: float(eq[k]) for k in ("arm1_metros", "arm2_state_rpp", "arm3")}
    # Arm 3(b) by line: the group's valuation of each US public good falls from its average cost to its responsive
    # cost (the central's mean of the two band ends); Mexico's public goods forgone fall to 0.725 of their cost.
    pg = I["vgen"][I["vgen"].cls.eq("public_good")]
    by_line = (pg.G_bn - pg.V_central_bn).groupby([pg.line, pg.end]).sum().groupby(level="line").mean()
    mx_pg = float(I["mxb"][I["mxb"].cls.eq("public_good")].bn.sum())
    arm3b = dict(us_public_goods_by_line_bn=by_line.sort_values().to_dict(), us_total_bn=float(by_line.sum()),
                 mexico_public_goods_bn=mx_pg, mexico_change_bn=mx_pg * (1 - W.MEXICO_PUBLIC_RESPONSE[1]))
    gate("arm3b_parts_add_to_its_world_change", abs(arm3b["us_total_bn"] + arm3b["mexico_change_bn"]
                                                   - float(eq["arm3b"])) < 1e-6,
         parts=arm3b["us_total_bn"] + arm3b["mexico_change_bn"], change=float(eq["arm3b"]))

    # ---- sanity checks
    def cmp_check(tab):
        r = tab[(tab.generation == "G1") & (tab.convention == "own_schooling_25_64_arrived_20plus") & (tab.ppp == "gdp")
                & (tab.selection == "p56")].iloc[0]
        return dict(per_person=float(r.ratio_us_to_mexico),
                    per_worker=float(r.ratio_us_to_mexico * r.employment_mx_15plus / r.employment_us_15plus))
    cmp = {k: cmp_check(v) for k, v in [("baseline", tab0)] + list(tables.items())}
    cells_cmp = {"baseline": (d, nat_cells["gdp"]), "arm2_state_rpp": (d_state, nat_cells["gdp"]),
                 "combined": (d_state, cells_for("metros")["gdp"]),
                 **{f"arm1_{k}": (d, cells_for(k)["gdp"]) for k in variants}}
    cmp_cells = {k: cmp_cell(dd, cc) for k, (dd, cc) in cells_cmp.items()}
    enoe = enoe_cdmx_check(en)

    ratios_out = pd.concat([r.assign(variant=k) for k, r in ratios.items()])[
        ["variant", "kind", "sex", "key", "n", "n_used", "level", "R_gross", "R_income", "R_withheld", "R_ctax", "R_emp",
         "R_hrs"]]
    ratios_out.to_csv(DERIVED / "beside_arms_ratios.csv", index=False, lineterminator="\n", float_format="%.6f")
    res.to_csv(DERIVED / f"beside_arms_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    summary.to_csv(DERIVED / f"beside_arms_summary_{CASE}.csv", index=False, lineterminator="\n", float_format="%.6f")
    a = en[(en.age >= 15) & (en.cat >= 0)]
    persons_by_area = {k: float(a.w[sel(a)].sum() / 1e6) for k, (sel, _, _) in variants.items()}
    meta = dict(case=CASE, basis=BASIS, members=MEMBERS, sources=srcs, metro_definition=munis_meta,
                enigh_persons_15plus_m=persons_by_area,
                emovi_respondents_at_14={k: int(m.sum()) for k, (_, m, _) in variants.items()},
                transitions_pooling={k: pd.Series(u).value_counts().to_dict() for k, u in used.items()},
                prices=prices, rpp_by_generation=rpp_by_gen,
                rpp_assignment=pd.Series(how[d.gen.ne("").to_numpy()]).value_counts().to_dict(),
                icp2021=dict(ppp_gdp=ppp_icp(ICP_GDP), ppp_actual_health=ppp_icp(ICP_HEALTH),
                             ppp_individual_government=ppp_icp(ICP_GOV_IND),
                             ppp_collective_government=ppp_icp(ICP_GOV_COLL), r_health=r_health, r_social=r_social,
                             r_public=r_public,
                             price_level_mexico_over_us={s: icp[("MEX", s, "PX.WL")] / icp[("USA", s, "PX.WL")]
                                                         for s in (ICP_GDP, ICP_HEALTH, ICP_GOV_IND, ICP_GOV_COLL)}),
                fhl_wtp_per_dollar=fhl, lane_medicaid_vg=list(I["health_vg"]), scenario_detail=detail,
                combined_parts_equal_bn=parts, arm3b_decomposition=arm3b,
                cmp_check=dict(cmp_ro=G.CMP_RO, cmp_re=G.CMP_RE, ratios=cmp, cmp_cell=cmp_cells),
                enoe_cdmx_check=enoe)
    json.dump(meta, open(DERIVED / f"beside_arms_meta_{CASE}.json", "w"), indent=1, sort_keys=True, default=float)
    show = summary[summary.weighting == "equal"].set_index("scenario")[
        ["premium_bn", "us_budget_value_bn", "group_total_bn", "world_total_bn", "us_residents_incl_group_bn",
         "group_per_member_usd", "breakeven_w", "breakeven_w_us_only"]]
    print(show.round(3).to_string(), file=sys.stderr)


def enoe_cdmx_check(en):
    """ENIGH's monthly labor income per employed person in Mexico City (entidad 09) for each schooling category, beside
    ENOE 2024 Q1-Q2's, and the same nationally. ENOE lets a worker answer with a minimum-wage bracket only (ing7c 1-5
    with ingocup 0): 'amounts' drops those answers and 'not specified' (ing7c 7) as missing within the cell and keeps
    'no income' (ing7c 6) at zero; 'as_lane' is mexico.py's reading, which drops only ing7c 7 and so counts the
    bracket-only answers as zero income."""
    frames = []
    for q in (1, 2):
        with zipfile.ZipFile(MX.CACHE / f"enoe_2024_trim{q}_csv.zip") as z:
            frames.append(pd.read_csv(z.open(f"ENOE_SDEMT{q}24.csv"), encoding="latin-1", low_memory=False,
                                      usecols=["r_def", "c_res", "ent", "eda", "anios_esc", "clase2", "ingocup", "ing7c",
                                               "fac_tri"]))
    e = pd.concat(frames, ignore_index=True)
    e = e[(pd.to_numeric(e.r_def, errors="coerce") == 0) & e.c_res.isin([1, 3])].copy()
    e = e[pd.to_numeric(e.eda, errors="coerce") >= 15]
    yrs = pd.to_numeric(e.anios_esc, errors="coerce")
    e["cat"] = MX.years_to_cat(np.where(yrs.between(0, 30), yrs, -1))
    e["w"] = pd.to_numeric(e.fac_tri, errors="coerce")
    e["inc"] = pd.to_numeric(e.ingocup, errors="coerce")
    emp = e.clase2 == 1
    as_lane = emp & (e.ing7c != 7)
    amounts = emp & ((e.ing7c == 6) | ((e.ing7c <= 5) & (e.inc > 0)))
    out = {}
    for scope, me, mn in (("cdmx", e.ent.eq(9), en.ent.eq(9)), ("national", e.ent.gt(0), en.ent.gt(0))):
        s = e[me & emp]
        out[f"{scope}_enoe_shares_of_employed"] = dict(
            not_specified=float(s.w[s.ing7c == 7].sum() / s.w.sum()),
            bracket_only=float(s.w[(s.ing7c <= 5) & (s.inc == 0)].sum() / s.w.sum()),
            no_income=float(s.w[s.ing7c == 6].sum() / s.w.sum()))
        for k in range(6):
            t = en[mn & (en.age >= 15) & en.cat.eq(k) & en.employed]
            enigh_m = float((t.w * t.labor_mxn).sum() / t.w.sum() / 12) if len(t) else np.nan
            row = dict(enigh_monthly_mxn=enigh_m, enigh_n=int(len(t)))
            for how, ok in (("amounts", amounts), ("as_lane", as_lane)):
                s = e[me & ok & e.cat.eq(k)]
                row[f"enoe_monthly_mxn_{how}"] = float(np.average(s.inc, weights=s.w)) if len(s) else np.nan
                row[f"enoe_n_{how}"] = int(len(s))
                row[f"ratio_enigh_to_enoe_{how}"] = enigh_m / row[f"enoe_monthly_mxn_{how}"]
            out[f"{scope}_{MX.CATS[k]}"] = row
    return out


if __name__ == "__main__":
    main()
