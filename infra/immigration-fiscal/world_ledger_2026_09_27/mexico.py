"""Mexico side of the world ledger: earnings, employment and hours in Mexico by schooling, sex and age
(ENIGH 2024, cross-checked on ENOE 2024 Q1-Q2), and the intergenerational schooling transition
(ESRU-EMOVI 2017). Case-independent. Inputs are the public files acquire.py stores in _cache/mexico/.

ENIGH records pay as received, after withholding (reads/enigh_2024_questionnaire.md); US earnings are gross.
Pay from formal jobs (subordinate, with SAR or AFORE) is grossed up by the 2024 statutory withholding (income
tax, employee IMSS contributions, the worker's retirement-account deposit), reproducing OECD's rates at the
average wage (gate); the withheld tax is kept as a Mexican tax the person would pay.

Consumption taxes: each person's gross labor income bears the IVA and IEPS their household's income decile pays
as a share of its autonomous income, as SHCP measures them for 2024 on the same survey (reads/shcp_2026_incidence.md),
plus the fuel excise, which SHCP's incidence leaves out, spread by SHCP's own proxy for fuel taxes (SHCP_FUEL_SHARE).

Outputs (derived/):
- mexico_earnings_cells.csv: sex x age band x schooling category; persons, employment, formal share, weekly
  hours; annual labor income per person as received ('income'), gross, withheld tax, retirement deposit and
  consumption taxes ('ctax'), in pesos and in PPP dollars.
- mexico_transition.csv: P(own schooling category | parents' schooling category, sex, birth cohort).
- mexico_enoe_check.csv: ENIGH against ENOE, mean monthly labor income per employed by category.

Schooling categories follow CEEY's six (Informe Movilidad Social 2019, p. 26, reads/emovi_mmsi_...):
0 none, 1 primaria incompleta (1-5 years), 2 primaria (6-8), 3 secundaria (9-11), 4 preparatoria
(12-15), 5 profesional (16+). Levels are converted to years of schooling first, in every survey.
"""
import csv
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "mexico"
DERIVED = HERE / "derived"
CATS = ["none", "primaria_incompleta", "primaria", "secundaria", "preparatoria", "profesional"]
AGE_BANDS = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 200]
# ENIGH 2024 ingresos claves that make up the concentrado's labor income (ingtrab = trabajo + negocio +
# otros_trab), identified by exact household-level reconstruction: sueldos = P001 P002 P011 P014 P018 P067;
# negocio = P068-P081; otros_trab = P021 P022; the other remunerations are P003-P009 P013 P015 P016 P035
# P036. P012, P019 and P023-P031 are property income (rentas) and are excluded. [CALCULATION: see RESULT]
LABOR_CLAVES = ({f"P{k:03d}" for k in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 18, 21, 22, 35, 36, 67]}
                | {f"P{k:03d}" for k in range(68, 82)})
# Pay of a subordinate job: P001-P009 for the main job, P014-P016 for a secondary one (questionnaire Apartado 2.2
# and Sección IV; reads/enigh_2024_questionnaire.md). ENIGH records it as received, after withholding.
MAIN_PAY = {f"P{k:03d}" for k in range(1, 10)}
SECOND_PAY = {"P014", "P015", "P016"}
# 2024 withholding on formal wages, from OECD Taxing Wages 2025's Mexico chapter (reads/oecd_taxing_wages_2025_
# mexico.md): the annual schedule, the credit table in force to April, the May 2024 decree's credit of 11.82% of
# the monthly UMA up to MXN 9,081 a month of taxable pay, employee IMSS contributions, and the worker's 1.125%
# deposit to the retirement account (withheld, but the worker's own saving, not a tax). Pay up to a full year at
# the general minimum wage (with the statutory aguinaldo and holiday premium) is not withheld from (LISR art. 96;
# LSS art. 36).
UMA = 108.57
UMA_YEAR = UMA * 30.4 * 12
ISR_SCHEDULE = np.array([[0.01, 0.00, 0.0192], [8952.50, 171.88, 0.0640], [75984.56, 4461.94, 0.1088],
                         [133536.08, 10723.55, 0.1600], [155229.81, 14194.54, 0.1792], [185852.58, 19682.13, 0.2136],
                         [374837.89, 60049.40, 0.2352], [590796.00, 110842.74, 0.3000],
                         [1127926.85, 271981.99, 0.3200], [1503902.47, 392294.17, 0.3400],
                         [4511707.38, 1414947.85, 0.3500]])
OLD_CREDIT = np.array([[0.0, 4884.24], [21227.53, 4881.96], [31840.57, 4879.44], [41674.09, 4713.24],
                       [42454.45, 4589.52], [53353.81, 4250.76], [56606.17, 3898.44], [64025.05, 3535.56],
                       [74696.05, 3042.48], [85366.81, 2611.32], [88587.97, 0.0]])
NEW_CREDIT, NEW_CREDIT_MAX = 4681.47, 9081.0 * 12
SSC_RATE, SSC_RATE_SUR, AFORE_RATE = 0.0125, 0.0040, 0.01125
MW_YEAR = 248.93 * (30.4 * 12 + 15 + 12 * 0.25)
OECD_AW, OECD_AW_TAX, OECD_AW_SSC = 199946.714, 0.108, 0.014    # Taxing Wages 2025, Table 1.3
# Consumption taxes by household decile, % of the household's autonomous income (before taxes and government
# transfers), deciles I-X of households ordered by monetary current income per capita, 2024 (SHCP 2026, "Distribución
# del pago de impuestos ... Resultados para el año 2024", on ENIGH 2024; reads/shcp_2026_incidence.md): IVA from
# Tabla 2.8 (with the formality adjustment), IEPS Otros from Gráfica 2.10 (IEPS / Ingreso). ISAN is left out.
SHCP_IVA = (6.2, 6.9, 7.2, 7.3, 7.7, 7.9, 8.2, 8.5, 8.9, 8.0)
SHCP_IEPS = (1.2, 1.3, 1.4, 1.5, 1.4, 1.4, 1.4, 1.4, 1.4, 1.0)
# The fuel excise (IEPS on gasoline and diesel) is outside SHCP's incidence, which covers "el IEPS diferente a
# gasolinas y diésel" (p. 8). It is added by SHCP's own proxy for fuel taxes: the 2024 revenue, MXN 403,583.9m (SHCP,
# Información de Finanzas Públicas enero-diciembre de 2024, table II.3), spread over the deciles as SHCP spreads the
# fossil-fuel IEPS, by ENIGH gasoline and diesel spending (Tabla 2.9), and divided by each decile's income on SHCP's
# base, which its IVA shares and rates imply (Tabla 2.8: income_d = IVA revenue x share_d / rate_d; the same table
# II.3 gives IVA at MXN 1,407,982.5m, Tabla 2.1's 1,407,983). Import duties (MXN 137,821.6m) and ISAN are left out.
SHCP_IVA_SHARE = (2.2, 4.0, 5.0, 6.2, 7.5, 8.8, 10.2, 12.7, 15.8, 27.7)
SHCP_IVA_AVERAGE = 8.0
SHCP_FUEL_SHARE = (2.5, 4.1, 5.0, 6.1, 7.8, 9.2, 10.9, 13.6, 16.7, 24.1)
IVA_2024_MXN_M, FUEL_IEPS_2024_MXN_M, IMPORT_DUTIES_2024_MXN_M = 1_407_982.5, 403_583.9, 137_821.6


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def fuel_ieps_by_decile():
    """The fuel excise by household decile, % of income on SHCP's base (see SHCP_FUEL_SHARE), and the decile incomes
    (MXN m) that SHCP's IVA shares and rates imply."""
    iva, share, fuel = (np.array(x, dtype=float) for x in (SHCP_IVA, SHCP_IVA_SHARE, SHCP_FUEL_SHARE))
    gate("shcp_decile_shares_add_to_100", abs(share.sum() - 100) < 0.25 and abs(fuel.sum() - 100) < 0.25,
         iva=float(share.sum()), fuel=float(fuel.sum()))
    income = IVA_2024_MXN_M * share / iva
    # The shares and rates are rounded to one decimal; together they must still give SHCP's printed average rate.
    gate("shcp_iva_shares_and_rates_imply_its_average", abs(100 * IVA_2024_MXN_M / income.sum() - SHCP_IVA_AVERAGE)
         < 0.1, implied=float(100 * IVA_2024_MXN_M / income.sum()))
    return FUEL_IEPS_2024_MXN_M * fuel / income, income


def years_to_cat(y):
    """Years of schooling to the six categories; NaN or negative (unknown) stays -1, never "none"."""
    y = np.asarray(y, float)
    return np.select([np.isnan(y) | (y < 0), y == 0, y <= 5, y <= 8, y <= 11, y <= 15], [-1, 0, 1, 2, 3, 4], 5)


def age_band(a):
    a = np.asarray(a, float)
    i = np.searchsorted(AGE_BANDS, a, side="right") - 1
    lab = np.array([f"{lo}-{hi - 1}" if hi < 200 else f"{lo}+" for lo, hi in zip(AGE_BANDS[:-1], AGE_BANDS[1:])])
    return np.where((i >= 0) & (i < len(lab)), lab[np.clip(i, 0, len(lab) - 1)], "")


def ppp():
    out = {}
    for ind in ("PA.NUS.PPP", "PA.NUS.PRVT.PP", "PA.NUS.FCRF"):
        rows = json.load(open(CACHE / f"wdi_{ind}.json"))[1]
        v = [r["value"] for r in rows if r["country"]["id"] == "MX" and r["date"] == "2024"]
        gate(f"wdi_{ind}_2024", len(v) == 1 and v[0], found=v)
        out[ind] = float(v[0])
    return out


# ------------------------------------------------------------------ withholding on formal wages, 2024
def mx_withholding(g):
    """Annual income tax, employee IMSS contributions and retirement-account deposit withheld from gross formal
    pay g (pesos a year), by OECD's 2024 equations. The credit in force to April (a third of the year) was paid
    in cash where it exceeded the tax; the decree's credit (two thirds) cannot take the tax below zero."""
    g = np.asarray(g, float)
    allow = np.minimum(g, np.minimum(g * 12 / 365 * 0.25, UMA * 15) + np.minimum(g * 15 / 365, UMA * 30))
    ti = np.maximum(g - allow, 0.0)
    lo, fixed, rate = ISR_SCHEDULE[np.clip(np.searchsorted(ISR_SCHEDULE[:, 0], ti, side="right") - 1, 0, None)].T
    isr = np.where(ti > 0, fixed + rate * np.maximum(ti - lo, 0.0), 0.0)
    old = OLD_CREDIT[np.clip(np.searchsorted(OLD_CREDIT[:, 0], ti, side="right") - 1, 0, None), 1]
    new = np.where(ti <= NEW_CREDIT_MAX, NEW_CREDIT, 0.0)
    tax = (isr - old) / 3 + np.maximum(isr - new, 0.0) * 2 / 3
    cap = 25 * UMA_YEAR
    ssc = np.minimum(g, cap) * SSC_RATE + np.clip(g - 3 * UMA_YEAR, 0.0, 22 * UMA_YEAR) * SSC_RATE_SUR
    afore = np.minimum(g, cap) * AFORE_RATE
    exempt = g <= MW_YEAR
    return tuple(np.where(exempt, 0.0, x) for x in (tax, ssc, afore))


def gross_from_net(net):
    """Gross formal pay from take-home pay: the smallest gross pay on the grid (5 pesos to MXN 2m) whose take-home
    pay reaches it. Take-home pay dips where withholding starts (the minimum wage) and where the decree's credit
    ends; an amount inside a dip gets the gross pay below the dip."""
    grid = np.concatenate([np.arange(0.0, 2e6, 5.0), np.geomspace(2e6, 1e9, 20001)[1:]])
    t, s, a = mx_withholding(grid)
    take = np.maximum.accumulate(grid - t - s - a)
    net = np.asarray(net, float)
    return np.where(net <= MW_YEAR, net, grid[np.minimum(np.searchsorted(take, net, side="left"), len(grid) - 1)])


# ------------------------------------------------------------------ ENIGH 2024
def household_deciles():
    """Each ENIGH household's decile as SHCP orders them: 10% of households each (by expansion factor), ascending in
    monetary current income per capita, which is current income less its non-monetary parts (imputed rent,
    remuneration in kind, transfers in kind from households and institutions). A household takes the decile that
    holds the midpoint of its weight; ties are ordered by folio."""
    c = pd.read_csv(CACHE / "enigh" / "concentradohogar.csv", dtype={"folioviv": str, "foliohog": str},
                    usecols=["folioviv", "foliohog", "factor", "tot_integ", "ing_cor", "ingtrab", "rentas", "transfer",
                             "estim_alqu", "otros_ing", "remu_espec", "transf_hog", "trans_inst"], low_memory=False)
    gate("enigh_current_income_adds_up",
         bool(np.allclose(c.ing_cor, c.ingtrab + c.rentas + c.transfer + c.estim_alqu + c.otros_ing, atol=0.01)))
    c["monetary_pc"] = (c.ing_cor - c.estim_alqu - c.remu_espec - c.transf_hog - c.trans_inst) / c.tot_integ
    c = c.sort_values(["monetary_pc", "folioviv", "foliohog"], kind="mergesort")
    mid = (c.factor.cumsum() - c.factor / 2) / c.factor.sum()
    c["decile"] = np.minimum((mid * 10).astype(int) + 1, 10)
    share = c.groupby("decile").factor.sum() / c.factor.sum()
    gate("household_deciles_hold_a_tenth_each", len(share) == 10 and (share - 0.1).abs().max() < 0.002,
         shares=share.round(4).to_dict())
    return c.set_index(["folioviv", "foliohog"]).decile


def enigh_years(niv, grado, antec):
    niv = pd.to_numeric(niv, errors="coerce").to_numpy()
    g = pd.to_numeric(grado, errors="coerce").fillna(0).to_numpy()
    an = pd.to_numeric(antec, errors="coerce").to_numpy()
    base_tech = np.select([an == 1, an == 2, an == 3], [6, 9, 12], np.nan)   # normal / técnica: by prerequisite
    y = np.select([np.isin(niv, [0, 1]), niv == 2, niv == 3, niv == 4, np.isin(niv, [5, 6]), niv == 7,
                   np.isin(niv, [8, 9]), niv == 10],
                  [0, g, 6 + g, 9 + g, base_tech + g, 12 + g, 16 + g, 18 + g], np.nan)
    return y


def load_enigh():
    z = CACHE / "enigh"
    pb = pd.read_csv(z / "poblacion.csv", dtype=str, low_memory=False,
                     usecols=["folioviv", "foliohog", "numren", "sexo", "edad", "nivelaprob", "gradoaprob",
                              "antec_esc", "trabajo_mp", "madre_id", "padre_id", "factor"])
    inc = pd.read_csv(z / "ingresos.csv", dtype={"folioviv": str, "foliohog": str, "numren": str, "clave": str},
                      usecols=["folioviv", "foliohog", "numren", "clave", "ing_tri"], low_memory=False)
    tr = pd.read_csv(z / "trabajos.csv", dtype=str, low_memory=False,
                     usecols=["folioviv", "foliohog", "numren", "id_trabajo", "subor", "pres_8", "htrab"])
    key = ["folioviv", "foliohog", "numren"]
    lab = (inc[inc.clave.isin(LABOR_CLAVES)].groupby(key).ing_tri.sum() * 4).rename("labor_mxn")
    hrs = tr.assign(h=pd.to_numeric(tr.htrab, errors="coerce")).groupby(key).h.sum().rename("hours")
    # Formal pay: a subordinate job with SAR or AFORE among its benefits (pres_8 "08") is withheld from.
    formal = tr[tr.subor.eq("1") & tr.pres_8.eq("08")]
    pay = {}
    for job, claves in (("1", MAIN_PAY), ("2", SECOND_PAY)):
        jobs = formal[formal.id_trabajo.eq(job)].set_index(key).index
        s = inc[inc.clave.isin(claves)].groupby(key).ing_tri.sum() * 4
        pay[job] = s[s.index.isin(jobs)]
    fnet = pay["1"].add(pay["2"], fill_value=0.0).rename("formal_net_mxn")
    d = pb.join(lab, on=key).join(hrs, on=key).join(fnet, on=key)
    d["labor_mxn"] = d.labor_mxn.fillna(0.0)
    d["formal_net_mxn"] = d.formal_net_mxn.fillna(0.0)
    fg = np.where(d.formal_net_mxn > 0, gross_from_net(d.formal_net_mxn), 0.0)
    t, s, a = mx_withholding(fg)
    d["withheld_tax_mxn"] = t + s                      # income tax and employee contributions: Mexican taxes
    d["afore_mxn"] = a                                 # the worker's own retirement saving
    d["formal_gross_mxn"] = fg
    d["gross_mxn"] = d.labor_mxn + (fg - d.formal_net_mxn)
    miss = (fg - t - s - a) - d.formal_net_mxn
    gate("gross_up_closes", ((miss >= 0) & (miss <= 10 + 5e-4 * d.formal_net_mxn)).all(),
         worst=float(miss.abs().max()))
    # Consumption taxes: gross labor income at the household decile's IVA, IEPS and fuel-excise rate (SHCP 2026).
    d = d.join(household_deciles(), on=["folioviv", "foliohog"])
    gate("every_person_has_a_household_decile", bool(d.decile.notna().all()), missing=int(d.decile.isna().sum()))
    rate = (np.array(SHCP_IVA) + np.array(SHCP_IEPS) + fuel_ieps_by_decile()[0]) / 100
    d["ctax_rate"] = rate[d.decile.to_numpy(int) - 1]
    d["ctax_mxn"] = d.gross_mxn * d.ctax_rate
    d["w"] = d.factor.astype(float)
    d["age"] = d.edad.astype(float)
    d["sex"] = np.where(d.sexo == "1", "male", "female")
    d["years"] = enigh_years(d.nivelaprob, d.gradoaprob, d.antec_esc)
    d["cat"] = years_to_cat(d.years.fillna(-1))
    d["employed"] = (d.trabajo_mp == "1") | (d.labor_mxn > 0)
    d["hours"] = np.where(d.employed, d.hours, np.nan)
    # Co-resident parents' schooling (madre_id / padre_id give the parent's numren; '&' and blank: none).
    hh = d.folioviv + "|" + d.foliohog + "|"
    cat_of = pd.Series(d.cat.to_numpy(), index=hh + d.numren.astype(int).astype(str))
    def parent(col):
        pid = pd.to_numeric(d[col], errors="coerce")
        k = hh + pid.fillna(-1).astype(int).astype(str)
        return np.where(pid.notna(), k.map(cat_of).fillna(-1).to_numpy(), -2)   # -2 no co-resident parent
    mo, fa = parent("madre_id"), parent("padre_id")
    d["parent_cat"] = np.maximum(mo, fa)              # -2 none co-resident, -1 co-resident but unknown
    # Gate: the person-level claves reproduce the concentrado's monetary labor income (remuneration in kind,
    # remu_espec, sits in a table this lane does not read and is the only gap).
    c = pd.read_csv(z / "concentradohogar.csv", usecols=["ingtrab", "remu_espec", "factor"], low_memory=False)
    target = ((c.ingtrab - c.remu_espec) * c.factor).sum() * 4
    got = (d.labor_mxn * d.w).sum()
    gate("enigh_labor_claves_reproduce_concentrado", abs(got / target - 1) < 1e-6, got=got, target=target)
    return d


def young_by_parent(d, rates):
    """Mexicans aged 15-24 by their co-resident parents' schooling (the more-schooled parent): the Mexico side
    for second-generation members still of school age, whose own final schooling is not yet observed."""
    y = d[(d.age >= 15) & (d.age <= 24)].copy()
    y["band"] = np.where(y.age <= 19, "15-19", "20-24")
    y["coresident"] = y.parent_cat >= -1
    rows = []
    for (sex, band), s in y.groupby(["sex", "band"]):
        share = (s.w * s.coresident).sum() / s.w.sum()
        k = s[s.parent_cat >= 0]
        for pc, t in k.groupby("parent_cat"):
            per = {m: (t.w * t[col]).sum() / t.w.sum() for m, col in MONEY.items()}
            emp = (t.w * t.employed).sum() / t.w.sum()
            hn = t.employed & t.hours.notna()
            hrs = (t.w * t.hours.fillna(0))[hn].sum() / t.w[hn].sum() if hn.any() else np.nan
            rows.append(dict(sex=sex, band=band, parent_cat=int(pc), parent_cat_name=CATS[int(pc)], n=len(t),
                             persons=t.w.sum(), coresident_share_of_band=share, employment_rate=emp,
                             weekly_hours_employed=hrs, income_per_person_mxn=per["income"],
                             **{f"{m}_per_person_mxn": per[m] for m in ("gross", "withheld", "afore", "ctax")}))
    out = pd.DataFrame(rows)
    add_ppp(out, rates)
    return out


def add_ppp(t, rates):
    """PPP-dollar columns for every per-person peso column: GDP PPP (central) and private-consumption PPP."""
    for m in ("income", "gross", "withheld", "afore", "ctax"):
        t[f"{m}_per_person_ppp_gdp"] = t[f"{m}_per_person_mxn"] / rates["PA.NUS.PPP"]
        t[f"{m}_per_person_ppp_consumption"] = t[f"{m}_per_person_mxn"] / rates["PA.NUS.PRVT.PP"]


MONEY = {"income": "labor_mxn", "gross": "gross_mxn", "withheld": "withheld_tax_mxn", "afore": "afore_mxn",
         "ctax": "ctax_mxn"}


def cells(d, weight_col="w"):
    """Sex x age band x schooling cells: take-home labor income ('income', as ENIGH records it), gross pay,
    withheld income tax and employee contributions, the retirement-account deposit, and the consumption taxes on
    gross pay at the household decile's rate ('ctax'), per person."""
    d = d[(d.age >= 15) & (d.cat >= 0)].copy()
    d["band"] = age_band(d.age)
    for k, col in MONEY.items():
        d[f"w_{k}"] = d[weight_col] * d[col]
    d["we"] = d[weight_col] * d.employed
    d["weh"] = d[weight_col] * d.employed * d.hours.fillna(0)
    d["weh_n"] = d[weight_col] * d.employed * d.hours.notna()
    d["wf"] = d[weight_col] * (d.formal_net_mxn > 0)
    g = d.groupby(["sex", "band", "cat"])
    out = pd.DataFrame({"n": g.size(), "persons": g[weight_col].sum(),
                        **{f"{k}_sum": g[f"w_{k}"].sum() for k in MONEY}, "employed": g.we.sum(),
                        "formal": g.wf.sum(), "hours_sum": g.weh.sum(), "hours_n": g.weh_n.sum()}).reset_index()
    out["employment_rate"] = out.employed / out.persons
    out["formal_share_of_employed"] = out.formal / out.employed.replace(0, np.nan)
    out["weekly_hours_employed"] = out.hours_sum / out.hours_n.replace(0, np.nan)
    out["income_per_person_mxn"] = out.income_sum / out.persons
    out["income_per_employed_mxn"] = out.income_sum / out.employed.replace(0, np.nan)
    for k in ("gross", "withheld", "afore", "ctax"):
        out[f"{k}_per_person_mxn"] = out[f"{k}_sum"] / out.persons
    return out


# ------------------------------------------------------------------ ENOE 2024 Q1-Q2 (cross-check)
def load_enoe():
    frames = []
    for q in (1, 2):
        with zipfile.ZipFile(CACHE / f"enoe_2024_trim{q}_csv.zip") as z:
            name = f"ENOE_SDEMT{q}24.csv"
            f = pd.read_csv(z.open(name), encoding="latin-1", low_memory=False,
                            usecols=["r_def", "c_res", "sex", "eda", "anios_esc", "clase2", "hrsocup", "ingocup",
                                     "ing7c", "fac_tri"])
        frames.append(f)
    e = pd.concat(frames, ignore_index=True)
    e = e[(pd.to_numeric(e.r_def, errors="coerce") == 0) & e.c_res.isin([1, 3])].copy()
    e["age"] = pd.to_numeric(e.eda, errors="coerce")
    e["w"] = pd.to_numeric(e.fac_tri, errors="coerce") / 2          # two quarters pooled
    yrs = pd.to_numeric(e.anios_esc, errors="coerce")
    e["cat"] = years_to_cat(np.where(yrs.between(0, 30), yrs, -1))
    e["sex"] = np.where(e.sex == 1, "male", "female")
    e["employed"] = e.clase2 == 1
    e["hours"] = np.where(e.employed, pd.to_numeric(e.hrsocup, errors="coerce"), np.nan)
    ing = pd.to_numeric(e.ingocup, errors="coerce")
    # ing7c 7 = income not specified: missing at random within the cell, so it drops out of the mean;
    # 6 = no income (unpaid): zero.
    e["monthly_mxn"] = np.where(e.employed & (e.ing7c != 7), ing, np.nan)
    return e[e.age >= 15]


# ------------------------------------------------------------------ ESRU-EMOVI 2017 transitions
def emovi_years(level, grade):
    lv = pd.to_numeric(level, errors="coerce").to_numpy()
    g = pd.to_numeric(grade, errors="coerce").fillna(0).to_numpy()
    # EMOVI p13 / p43 levels: 1 preescolar, 2 primaria, 3-4 secundaria, 5-6 preparatoria, 7 técnica con
    # secundaria, 8 técnica con preparatoria, 9 normal básica, 10 normal de licenciatura, 11 profesional,
    # 12 posgrado, 97 none, 98 does not know.
    # Secundaria and preparatoria have three grades; a recorded 4th-6th grade there is capped at 3.
    g3 = np.minimum(g, 3)
    y = np.select([np.isin(lv, [1, 97]), lv == 2, np.isin(lv, [3, 4]), np.isin(lv, [5, 6]), lv == 7, lv == 8, lv == 9,
                   np.isin(lv, [10, 11]), lv == 12],
                  [0, np.minimum(g, 6), 6 + g3, 9 + g3, 9 + g, 12 + g, 9 + g, 12 + g, 16 + g], np.nan)
    return y


def load_emovi():
    p = CACHE / "emovi" / "ESRU-EMOVI 2017 Entrevistado.dta"
    with pd.io.stata.StataReader(p) as r:
        d = r.read(convert_categoricals=False, columns=["p05", "p06", "p13", "p14", "p42", "p43", "p44", "p42m",
                                                          "p43m", "p44m", "factor"])
    d["age"] = pd.to_numeric(d.p05, errors="coerce")
    d["sex"] = np.where(d.p06 == 1, "male", "female")
    d["own_years"] = emovi_years(d.p13, d.p14)
    fy = np.where(d.p42 == 2, 0.0, emovi_years(d.p43, d.p44))       # did not attend school -> none
    my = np.where(d.p42m == 2, 0.0, emovi_years(d.p43m, d.p44m))
    fy = np.where(d.p43 == 98, np.nan, fy)
    my = np.where(d.p43m == 98, np.nan, my)
    d["parent_years"] = np.fmax(fy, my)                              # the more-schooled parent; NaN if both unknown
    d["own_cat"] = years_to_cat(np.nan_to_num(d.own_years, nan=-1))
    d["parent_cat"] = years_to_cat(np.nan_to_num(d.parent_years, nan=-1))
    d["birth_year"] = 2017 - d.age
    d["cohort"] = pd.cut(d.birth_year, [1952, 1962, 1972, 1982, 1992], labels=["1953-62", "1963-72", "1973-82",
                                                                             "1983-92"]).astype(str)
    d["w"] = pd.to_numeric(d.factor, errors="coerce")
    return d


def transitions(d):
    ok = (d.own_cat >= 0) & (d.parent_cat >= 0) & d.cohort.ne("nan")
    t = d[ok].groupby(["sex", "cohort", "parent_cat", "own_cat"]).agg(n=("w", "size"), w=("w", "sum")).reset_index()
    tot = t.groupby(["sex", "cohort", "parent_cat"]).w.transform("sum")
    t["share"] = t.w / tot
    t["cell_n"] = t.groupby(["sex", "cohort", "parent_cat"]).n.transform("sum")
    return t, ok.mean(), d[ok].w.sum() / d.w.sum()


def wdi(ind, year):
    rows = json.load(open(CACHE / f"wdi_{ind}.json"))[1]
    v = [r["value"] for r in rows if r["country"]["id"] == "MX" and r["date"] == str(year) and r["value"] is not None]
    gate(f"wdi_{ind}_{year}", len(v) == 1, found=v)
    return float(v[0])


# ENIGH claves for government cash transfers (the concentrado's bene_gob, identified with the labor claves above)
# and for pensions paid inside Mexico (P032; P033 is pensions from abroad).
BENE_GOB = {"P043", "P045", "P048"} | {f"P{k:03d}" for k in range(101, 109)}
PENSION_MX = {"P032"}


def comparators(rates):
    """What Mexico's budget would spend on a person of each age, for the group's alternative world: public
    school places (ENIGH attendance at public schools by age, priced at public education spending per public
    student), government cash transfers and domestic pensions per person by age (ENIGH), and per-head government
    health spending and other government consumption (WDI)."""
    z = CACHE / "enigh"
    pb = pd.read_csv(z / "poblacion.csv", dtype=str, low_memory=False,
                     usecols=["folioviv", "foliohog", "numren", "edad", "asis_esc", "tipoesc", "factor"])
    inc = pd.read_csv(z / "ingresos.csv", dtype={"folioviv": str, "foliohog": str, "numren": str, "clave": str},
                      usecols=["folioviv", "foliohog", "numren", "clave", "ing_tri"], low_memory=False)
    key = ["folioviv", "foliohog", "numren"]
    tr = (inc[inc.clave.isin(BENE_GOB)].groupby(key).ing_tri.sum() * 4).rename("transfers_mxn")
    pe = (inc[inc.clave.isin(PENSION_MX)].groupby(key).ing_tri.sum() * 4).rename("pension_mxn")
    d = pb.join(tr, on=key).join(pe, on=key).fillna({"transfers_mxn": 0.0, "pension_mxn": 0.0})
    d["w"] = d.factor.astype(float)
    d["age"] = d.edad.astype(int)
    # asis_esc 1 = attends school; tipoesc 1 = public school (ENIGH 2024 codes; checked against the attendance
    # rates below: near-universal at 6-14, and public schools the large majority).
    d["public_student"] = (d.asis_esc == "1") & (d.tipoesc == "1")
    d["student"] = d.asis_esc == "1"
    gdp_ppp = wdi("NY.GDP.MKTP.PP.CD", 2024)
    edu_share = wdi("SE.XPD.TOTL.GD.ZS", 2022)          # latest year published
    public_students = (d.w * d.public_student).sum()
    per_student = edu_share / 100 * gdp_ppp / public_students
    by_age = d.groupby(d.age.clip(upper=90)).apply(lambda s: pd.Series({
        "persons": s.w.sum(), "student_rate": (s.w * s.student).sum() / s.w.sum(),
        "public_student_rate": (s.w * s.public_student).sum() / s.w.sum(),
        "transfers_ppp_per_person": (s.w * s.transfers_mxn).sum() / s.w.sum() / rates["PA.NUS.PPP"],
        "pension_ppp_per_person": (s.w * s.pension_mxn).sum() / s.w.sum() / rates["PA.NUS.PPP"]}),
        include_groups=False).reset_index().rename(columns={"age": "age"})
    gate("enigh_attendance_6_14", by_age[(by_age.age >= 6) & (by_age.age <= 14)].student_rate.min() > 0.85,
         rates=by_age[(by_age.age >= 6) & (by_age.age <= 14)].student_rate.round(3).tolist())
    gate("enigh_public_share", 0.8 < public_students / (d.w * d.student).sum() < 0.95,
         share=public_students / (d.w * d.student).sum())
    gov_cons = wdi("NE.CON.GOVT.ZS", 2024)
    health_pc = wdi("SH.XPD.GHED.PP.CD", 2023)
    health_gdp = wdi("SH.XPD.GHED.GD.ZS", 2023) if (CACHE / "wdi_SH.XPD.GHED.GD.ZS.json").exists() else None
    pop = wdi("SP.POP.TOTL", 2024)
    # Other government consumption per head: final consumption less health and education, both at their
    # own shares of GDP (an approximation: the education share includes capital spending).
    health_share = health_pc * pop / gdp_ppp * 100
    other_pc = (gov_cons - health_share - edu_share) / 100 * gdp_ppp / pop
    meta = dict(gdp_ppp_2024=gdp_ppp, population_2024=pop, education_share_gdp_2022=edu_share,
                public_students_m=public_students / 1e6, education_per_public_student_ppp=per_student,
                gov_consumption_share_gdp_2024=gov_cons, health_per_capita_ppp_2023=health_pc,
                health_share_gdp_implied=health_share, other_gov_consumption_per_capita_ppp=other_pc,
                transfers_total_ppp_bn=float((d.w * d.transfers_mxn).sum() / rates["PA.NUS.PPP"] / 1e9),
                pensions_total_ppp_bn=float((d.w * d.pension_mxn).sum() / rates["PA.NUS.PPP"] / 1e9))
    return by_age, meta


def main():
    DERIVED.mkdir(exist_ok=True)
    rates = ppp()
    # The withholding model must reproduce OECD's own rates for the single worker at the average wage.
    aw_tax, aw_ssc, _ = (float(x[0]) / OECD_AW for x in mx_withholding(np.array([OECD_AW])))
    gate("withholding_reproduces_oecd_table_1_3", abs(aw_tax - OECD_AW_TAX) < 5e-4 and abs(aw_ssc - OECD_AW_SSC) < 5e-4,
         tax=aw_tax, ssc=aw_ssc)
    en = load_enigh()
    c = cells(en)
    add_ppp(c, rates)
    c["income_per_employed_ppp_gdp"] = c.income_per_employed_mxn / rates["PA.NUS.PPP"]
    c["cat_name"] = [CATS[i] for i in c.cat]
    cols = ["sex", "band", "cat", "cat_name", "n", "persons", "employment_rate", "formal_share_of_employed",
            "weekly_hours_employed", "income_per_person_mxn", "income_per_employed_mxn", "income_per_person_ppp_gdp",
            "income_per_person_ppp_consumption", "income_per_employed_ppp_gdp", "gross_per_person_mxn",
            "withheld_per_person_mxn", "afore_per_person_mxn", "ctax_per_person_mxn"] + [
            f"{m}_per_person_ppp_{p}" for m in ("gross", "withheld", "afore", "ctax") for p in ("gdp", "consumption")]
    c[cols].to_csv(DERIVED / "mexico_earnings_cells.csv", index=False, lineterminator="\n", float_format="%.6g")
    gate("enigh_persons_15plus", 95e6 < c.persons.sum() < 110e6, persons=c.persons.sum())
    yp = young_by_parent(en, rates)
    yp.to_csv(DERIVED / "mexico_young_by_parent.csv", index=False, lineterminator="\n", float_format="%.6g")
    gate("enigh_young_coresident", yp.coresident_share_of_band.min() > 0.5, shares=yp.coresident_share_of_band.unique())

    eo = load_enoe()
    eo["band"] = age_band(eo.age)
    rows = []
    for k, s in eo[eo.cat >= 0].groupby("cat"):
        m = s.monthly_mxn.notna()
        rows.append(dict(cat=k, cat_name=CATS[k],
                         enoe_employment=(s.w * s.employed).sum() / s.w.sum(),
                         enoe_income_nonresponse=1 - (s.w * m).sum() / (s.w * s.employed).sum(),
                         enoe_monthly_per_employed=(s.w * s.monthly_mxn.fillna(0))[m].sum() / s.w[m].sum()))
    ch = pd.DataFrame(rows)
    ig = en[(en.age >= 15) & (en.cat >= 0)]
    ch["enigh_employment"] = [(ig.w * ig.employed)[ig.cat == k].sum() / ig.w[ig.cat == k].sum() for k in ch.cat]
    ch["enigh_monthly_per_employed"] = [(ig.w * ig.labor_mxn)[ig.cat == k].sum() / (ig.w * ig.employed)[ig.cat == k].sum()
                                        / 12 for k in ch.cat]
    ch["ratio_enigh_to_enoe"] = ch.enigh_monthly_per_employed / ch.enoe_monthly_per_employed
    ch.to_csv(DERIVED / "mexico_enoe_check.csv", index=False, lineterminator="\n", float_format="%.6g")

    em = load_emovi()
    t, share_ok, wshare_ok = transitions(em)
    t["cat_name"] = [CATS[i] for i in t.own_cat]
    t.to_csv(DERIVED / "mexico_transition.csv", index=False, lineterminator="\n", float_format="%.6g")
    gate("emovi_rows", len(em) == 17665, rows=len(em))
    formal = en.formal_net_mxn > 0
    meta = dict(ppp_2024=rates, enigh_persons_15plus=float(c.persons.sum()),
                enigh_labor_income_mxn_bn=float((en.labor_mxn * en.w).sum() / 1e9),
                enigh_labor_income_gross_mxn_bn=float((en.gross_mxn * en.w).sum() / 1e9),
                withholding=dict(
                    formal_workers_m=float(en.w[formal].sum() / 1e6),
                    formal_take_home_mxn_bn=float((en.formal_net_mxn * en.w).sum() / 1e9),
                    withheld_tax_mxn_bn=float((en.withheld_tax_mxn * en.w).sum() / 1e9),
                    afore_mxn_bn=float((en.afore_mxn * en.w).sum() / 1e9),
                    exempt_minimum_wage_share_of_formal=float(en.w[formal & (en.formal_gross_mxn <= MW_YEAR)].sum()
                                                              / en.w[formal].sum()),
                    oecd_average_wage_check=dict(tax=aw_tax, ssc=aw_ssc)),
                emovi_respondents=int(len(em)), emovi_share_with_both_schooling=float(share_ok),
                emovi_weighted_share_with_both_schooling=float(wshare_ok),
                consumption_tax=dict(
                    source="SHCP 2026, Distribución del pago de impuestos ... Resultados para el año 2024: IVA Tabla "
                           "2.8, IEPS Otros Gráfica 2.10, % of autonomous income by household decile; the fuel "
                           "excise from SHCP's 2024 revenue (Información de Finanzas Públicas enero-diciembre 2024, "
                           "table II.3) spread by Tabla 2.9's fuel column over the incomes Tabla 2.8 implies",
                    iva_pct_by_decile=list(SHCP_IVA), ieps_pct_by_decile=list(SHCP_IEPS),
                    fuel_ieps_pct_by_decile=[float(x) for x in fuel_ieps_by_decile()[0]],
                    fuel_ieps_revenue_mxn_m=FUEL_IEPS_2024_MXN_M, iva_revenue_mxn_m=IVA_2024_MXN_M,
                    implied_income_base_mxn_m=float(fuel_ieps_by_decile()[1].sum()),
                    import_duties_left_out_mxn_m=IMPORT_DUTIES_2024_MXN_M,
                    import_duties_if_spread_like_iva_pct=float(SHCP_IVA_AVERAGE * IMPORT_DUTIES_2024_MXN_M
                                                               / IVA_2024_MXN_M),
                    gross_labor_income_weighted_rate=float((en.w * en.ctax_mxn).sum() / (en.w * en.gross_mxn).sum()),
                    gross_labor_income_weighted_rate_without_fuel=float(
                        (en.w * en.gross_mxn * (np.array(SHCP_IVA) + np.array(SHCP_IEPS))[en.decile.to_numpy(int) - 1]
                         / 100).sum() / (en.w * en.gross_mxn).sum()),
                    gross_labor_income_share_by_decile={int(k): float(v) for k, v in (
                        (en.w * en.gross_mxn).groupby(en.decile).sum() / (en.w * en.gross_mxn).sum()).items()}))
    ca, cmeta = comparators(rates)
    ca.to_csv(DERIVED / "mexico_comparators_by_age.csv", index=False, lineterminator="\n", float_format="%.6g")
    meta["comparators"] = cmeta
    json.dump(meta, open(DERIVED / "mexico_meta.json", "w"), indent=1, sort_keys=True)
    print(json.dumps(meta, indent=1), file=sys.stderr)


if __name__ == "__main__":
    main()
