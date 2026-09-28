"""State-priced police, courts, health and administration (lane state_priced_services_2026_09_29).

Question: if the state-and-local portion of three engine lines were priced at the per-resident spending of the
states where the group lives, rather than at the national average, how much would the group's charge change?
The federal portion stays national and each line keeps its within-line key; the state index only rescales the
price per unit, as the school line already does with per-pupil cost (school_cost_where_enrolled_2026_09_24).

    index_f = sum_s w_s * pc_{f,s} / pc_{f,US}
    correction_f = S&L amount_f * group share_f * (index_f - 1)   [times the line's response at each band end]

Inputs (all local, hashed into derived/manifest.json):
  - CPS ASEC 2025 person, household and replicate-weight files: the canonical group (full_account_spending's
    canonical_target) by hhpub25 GESTFIPS, weighted by pwwgt0; replicate weights give the sampling SE.
  - Census Annual Survey of State and Local Government Finances, state-by-level files FY2024 (main) and FY2023
    (stability), level 1 (state and local combined), $000.
  - Census Vintage 2024 state population estimates (NST-EST2024-ALLDATA), mean of July 1 of the two calendar years
    a fiscal year spans.
  - BLS QCEW 2023 annual by industry: state + local government average pay by function (wage demarcation).

Writes derived/group_population_by_state.csv, state_per_capita.csv, indexes.csv, decomposition.csv,
wage_demarcation.csv, corrections.csv, manifest.json. Run from anywhere:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 state_price.py [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
FIN = {2024: (FISCAL / "detention_reconciliation_2026_09_20/_cache/census_2024_units.zip",
              "2024_Individual_Unit_Files/24statetypepu.txt"),
       2023: (FISCAL / "local_spending_composition_2026_09_18/_cache/indunit_2023.zip",
              "2023_Individual_Unit_Files/23statetypepu.txt")}
POP = ROOT / "sources/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv"
QCEW = ROOT / "sources/immigration-fiscal/data/bls/qcew_2023_annual_by_industry.zip"
BUILDER = FISCAL / "full_account_spending_2026_09_20/builder.py"
STATE_POP_CHECK = FISCAL / "ledger_stress_2026_09_17/derived/state_populations.csv"
ADMIN_PANEL = FISCAL / "administration_response_2026_09_20/derived/panel.csv"
MEX_GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]
TARGET_N = 40896574.15235156

STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL",
          13: "GA", 15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA",
          23: "ME", 24: "MD", 25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE",
          32: "NV", 33: "NH", 34: "NJ", 35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK",
          41: "OR", 42: "PA", 44: "RI", 45: "SC", 46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT",
          51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}

# Census function codes (E = current operation, F = construction; the file carries no G codes, so direct
# expenditure by function is E + F). `minus` subtracts a revenue item (hospital charges A36) for the net arm.
FUNCTIONS = {
    "police": dict(codes=["62"], naics=["922120"]),
    "judicial": dict(codes=["25"], naics=["922110", "922130"]),
    "fire": dict(codes=["24"], naics=["922160"]),
    "corrections": dict(codes=["04", "05"], naics=["922140", "922150"]),
    "protective_inspection": dict(codes=["66"], naics=["922190"]),
    "health": dict(codes=["32"], naics=["923120"]),
    "hospitals": dict(codes=["36"], naics=["622"]),
    "health_and_hospitals": dict(codes=["32", "36"], naics=["923120", "622"]),
    "health_and_net_hospitals": dict(codes=["32", "36"], minus=["A36"], naics=["923120", "622"]),
    "administration": dict(codes=["23", "29", "31"], naics=["921"]),
    "administration_ex_e23": dict(codes=["29", "31"], naics=["921"]),
    "housing_community": dict(codes=["50"], naics=["925"]),
    "parks_libraries": dict(codes=["61", "52"], naics=["10"]),
}
POS_PARTS = ["police", "judicial", "fire", "corrections", "protective_inspection"]

# Engine lines (main case of 2026-09-27, main_case_long_run_2026_09_27; shares and responses read from the adopted
# models at the band's end specifications 48 / 11 by probe_engine.cjs -> derived/engine_lines.json).
SL_BN = {"public_order_safety": 440.090, "health_services": 126.839, "general_public_services": 304.538,
         "housing_community_services": 11.773, "recreation_culture": 48.901}
SAPCE = HERE / "_cache/SAPCE.zip"   # https://apps.bea.gov/regional/zip/SAPCE.zip, fetched 2026-09-29
SAPCE_SHA = "d93e91e178bf35c1448fd2692deb4b08c6e3953d83a2c430595787822515a9b1"
# Receipt lines keyed at a national rate, priced by state: Census tax codes, the base the rate is taken per, the
# group weights, and the S&L part of the NIPA line (3.5/20 general sales; 3.5/23 of 3.5/4+23; 3.4/10).
BJS = HERE / "_cache/p23st.pdf"   # BJS Prisoners in 2023 Statistical Tables (NCJ 310197), https://bjs.ojp.gov/document/p23st.pdf
BJS_SHA = "22a4cbe8ee0ff6156db97b4825db60907d53f0a345d02166b8484e0ac307b2e9"
NAME_FIPS = {"Alabama": 1, "Alaska": 2, "Arizona": 4, "Arkansas": 5, "California": 6, "Colorado": 8, "Connecticut": 9,
             "Delaware": 10, "Florida": 12, "Georgia": 13, "Hawaii": 15, "Idaho": 16, "Illinois": 17, "Indiana": 18,
             "Iowa": 19, "Kansas": 20, "Kentucky": 21, "Louisiana": 22, "Maine": 23, "Maryland": 24,
             "Massachusetts": 25, "Michigan": 26, "Minnesota": 27, "Mississippi": 28, "Missouri": 29, "Montana": 30,
             "Nebraska": 31, "Nevada": 32, "New Hampshire": 33, "New Jersey": 34, "New Mexico": 35, "New York": 36,
             "North Carolina": 37, "North Dakota": 38, "Ohio": 39, "Oklahoma": 40, "Oregon": 41, "Pennsylvania": 42,
             "Rhode Island": 44, "South Carolina": 45, "South Dakota": 46, "Tennessee": 47, "Texas": 48, "Utah": 49,
             "Vermont": 50, "Virginia": 51, "Washington": 53, "West Virginia": 54, "Wisconsin": 55, "Wyoming": 56}
# The central package prices every S&L sub-function of a line the bar opens (any of its functions clears +-2%); a
# line none of whose functions clears stays national. GPS is the exception: its functions clear in opposite
# directions depending on E23, so the sign is not identified and the line stays national. Health uses E32 only
# (hospital arms beside). Corrections is priced per state prisoner, not per resident.
CENTRAL = {"public_order_safety": ["police", "judicial", "fire", "corrections_per_inmate", "protective_inspection"],
           "health_services": ["health"], "recreation_culture": ["parks_libraries"]}
NARROW = ["police", "health"]
RECEIPTS = {
    "general_sales_tax": dict(codes=["T09"], base="pce", weights="group", sl_bn=602.430),
    "excise_selective_sales": dict(codes=["T10", "T11", "T12", "T13", "T14", "T15", "T16", "T19"], base="pce",
                                   weights="group", sl_bn=271.298),
    "personal_motor_vehicle": dict(codes=["T24"], base="population", weights="group_adults", sl_bn=26.125),
}
FED_BN = {"public_order_safety": 79.064, "health_services": 179.700, "general_public_services": 97.070}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_target_fn():
    spec = importlib.util.spec_from_file_location("full_account_builder", BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if sha(CPS) != mod.CPS_SHA:
        raise ValueError("[BLOCKED] CPS archive differs from the builder's pin")
    return mod.canonical_target


def group_by_state():
    """Group and civilian weights by state, with the 160 replicate weights for the group's state shares."""
    canonical_target = canonical_target_fn()
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PTOTVAL", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP"]
    with zipfile.ZipFile(CPS) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        rep_cols = ["h_seq", "PPPOS", "pwwgt0"] + [f"pwwgt{i}" for i in range(1, 161)]
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=rep_cols).rename(columns={"h_seq": "PH_SEQ"})
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(h, on="PH_SEQ", validate="many_to_one", how="left")
    if d[["pwwgt0", "GESTFIPS"]].isna().any().any():
        raise ValueError("[BLOCKED] unmatched CPS keys")
    civ, target = canonical_target(d)
    n = float(d.pwwgt0[target].sum())
    if abs(n - TARGET_N) > 0.01:
        raise ValueError(f"[BLOCKED] group total {n} != {TARGET_N}")
    d = d.assign(target=target, civ=civ, adult=d.A_AGE.ge(18))
    reps = [f"pwwgt{i}" for i in range(1, 161)]
    g = d[d.target]
    by = pd.DataFrame({
        "group": g.groupby("GESTFIPS").pwwgt0.sum(),
        "group_adults": g[g.adult].groupby("GESTFIPS").pwwgt0.sum(),
        "group_income_bn": (g.pwwgt0 * g.PTOTVAL.clip(lower=0)).groupby(g.GESTFIPS).sum() / 1e9,
        "group_records": g.groupby("GESTFIPS").size(),
        "civilian_cps": d[d.civ].groupby("GESTFIPS").pwwgt0.sum(),
    }).fillna(0)
    rep = g.groupby("GESTFIPS")[reps].sum().reindex(by.index).fillna(0)
    rep_adults = g[g.adult].groupby("GESTFIPS")[reps].sum().reindex(by.index).fillna(0)
    if set(by.index) != set(STATES):
        raise ValueError("[BLOCKED] CPS states differ from the 51-state list")
    return by, rep, rep_adults


def read_finance(year: int) -> pd.DataFrame:
    zpath, member = FIN[year]
    with zipfile.ZipFile(zpath) as z:
        lines = z.read(member).decode("latin-1").splitlines()
    t = pd.DataFrame([{"state": int(s[0:2]), "level": int(s[2]), "item": s[4:7], "amount_k": float(s[8:20]),
                       "yy": s[33:35]} for s in lines if s.strip()])
    if not t.yy.eq(f"{year % 100:02d}").all():
        raise ValueError(f"[BLOCKED] {member}: survey-year field is not {year}")
    return t[t.level.eq(1)].pivot_table(index="state", columns="item", values="amount_k", aggfunc="sum").fillna(0)


def function_amounts(fin: pd.DataFrame, basis: str) -> pd.DataFrame:
    """$ by state and function; basis 'direct' = E + F, 'current' = E only (net arm subtracts charges on direct)."""
    out = {}
    for f, spec in FUNCTIONS.items():
        pref = ["E", "F"] if basis == "direct" else ["E"]
        cols = [p + c for c in spec["codes"] for p in pref]
        v = sum(fin.get(c, 0) for c in cols)
        for m in spec.get("minus", []):
            v = v - fin.get(m, 0)
        out[f] = v * 1e3
    return pd.DataFrame(out)


def populations(year: int) -> pd.Series:
    p = pd.read_csv(POP, dtype={"STATE": int})
    p = p[p.SUMLEV.eq(40) & p.STATE.isin(STATES)].set_index("STATE")
    # A fiscal year FY runs mostly across calendar years FY-1 and FY (41 states end June 30): mean of the two
    # July 1 estimates.
    return (p[f"POPESTIMATE{year - 1}"] + p[f"POPESTIMATE{year}"]) / 2


def qcew_wage_index() -> tuple[pd.DataFrame, dict]:
    """State + local government average annual pay by function, relative to the US, from QCEW 2023.

    A state's cell falls back to all state+local government pay (NAICS 10, own 2+3) when the function's cells
    are suppressed; fallbacks are counted per function."""
    wanted = sorted({n for s in FUNCTIONS.values() for n in s["naics"]} | {"10"})
    frames = []
    with zipfile.ZipFile(QCEW) as z:
        names = {n.split("/")[-1].split(" ")[1]: n for n in z.namelist() if n.endswith(".csv")}
        for code in wanted:
            t = pd.read_csv(z.open(names[code]), dtype={"area_fips": str, "industry_code": str})
            t = t[t.own_code.isin([2, 3]) & (t.area_fips.str.endswith("000")) & t.industry_code.eq(code)]
            t = t[t.area_fips.isin([f"{s:02d}000" for s in STATES] + ["US000"])]
            frames.append(t[["area_fips", "own_code", "industry_code", "disclosure_code", "annual_avg_emplvl",
                             "total_annual_wages"]])
    q = pd.concat(frames)
    q = q[q.disclosure_code.isna() | q.disclosure_code.ne("N")]
    agg = q.groupby(["industry_code", "area_fips"])[["annual_avg_emplvl", "total_annual_wages"]].sum()
    pay = (agg.total_annual_wages / agg.annual_avg_emplvl.replace(0, np.nan)).unstack(0)
    us = pay.loc["US000"]
    rel = pay.drop(index="US000") / us
    rel.index = [int(a[:2]) for a in rel.index]
    rel = rel.reindex(sorted(STATES))
    out, fallbacks = {}, {}
    for f, spec in FUNCTIONS.items():
        # Employment-weighted pay across the function's industries: combine wages and employment.
        sub = agg.loc[spec["naics"]].groupby(level="area_fips").sum()
        p = sub.total_annual_wages / sub.annual_avg_emplvl.replace(0, np.nan)
        r = (p.drop(index="US000", errors="ignore") / p.get("US000", np.nan))
        r.index = [int(a[:2]) for a in r.index]
        r = r.reindex(sorted(STATES))
        missing = r.isna()
        fallbacks[f] = [STATES[s] for s in r.index[missing]]
        out[f] = r.where(~missing, rel["10"])
    return pd.DataFrame(out), fallbacks


def admin_panel_arm(w: pd.Series) -> pd.DataFrame:
    """Administration index by year, 2012-2023, current operations (E only), from the administration_response
    lane's panel (50 states; DC absent, so the group weights are renormalized over the 50). Dates the E23 break's
    effect on the index: FY2021 and earlier sit before it."""
    p = pd.read_csv(ADMIN_PANEL)
    p = p[p.level.eq(1)]
    rows = []
    for year, t in p.groupby("year"):
        t = t.set_index("state")
        ww = w.reindex(t.index)
        ww = ww / ww.sum()
        for f, cols in (("administration", ["E23", "E29", "E31"]), ("administration_ex_e23", ["E29", "E31"])):
            amt = t[cols].sum(axis=1)
            rel = (amt / t.population) / (amt.sum() / t.population.sum())
            rows.append(dict(year=year, basis="current", function=f, index=float((ww * rel).sum()),
                             all_residents=float((t.population / t.population.sum() * rel).sum()),
                             e23_us_bn=float(t.E23.sum() / 1e6), dc_weight_dropped=float(w.get(11, 0))))
    return pd.DataFrame(rows)


def pce(year: int) -> pd.Series:
    """BEA SAPCE1 line 1, personal consumption expenditures by state ($), mean of calendar years year-1 and year."""
    if sha(SAPCE) != SAPCE_SHA:
        raise ValueError("[BLOCKED] SAPCE.zip differs from its pin")
    with zipfile.ZipFile(SAPCE) as z:
        t = pd.read_csv(z.open("SAPCE1__ALL_AREAS_1997_2024.csv"), dtype={"GeoFIPS": str}, encoding="latin-1")
    t = t[t.LineCode.eq(1)].copy()
    t["fips"] = t.GeoFIPS.str.strip().str.strip('"').str[:2].astype(int)
    t = t[t.GeoFIPS.str.strip().str.strip('"').str.endswith("000") & t.fips.isin(STATES)].set_index("fips")
    v = (t[str(year - 1)].astype(float) + t[str(year)].astype(float)) / 2
    if len(v) != 51:
        raise ValueError("[BLOCKED] SAPCE does not give 51 states")
    return v * 1e6


def bjs_prisoners() -> pd.DataFrame:
    """BJS Prisoners in 2023, Table 2: prisoners under state jurisdiction, 31 Dec 2022 and 2023, parsed with
    pdftotext -layout. Six integrated states (AK CT DE HI RI VT) include jail inmates. DC has none (federal)."""
    if sha(BJS) != BJS_SHA:
        raise ValueError("[BLOCKED] p23st.pdf differs from its pin")
    text = subprocess.run(["pdftotext", "-layout", str(BJS), "-"], check=True, capture_output=True,
                          text=True).stdout
    start = text.index("TABLE 2\nPrisoners under the jurisdiction of state or federal correctional authorities, by sex")
    block = text[start:text.index("TABLE 3", start)]
    rows = {}
    pat = re.compile(r"^\s*([A-Z][A-Za-z ]*[A-Za-z])\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s")
    for line in block.splitlines():
        m = pat.match(line)
        if not m:
            continue
        name = m.group(1)
        if name not in NAME_FIPS and name[-1] in "abcd" and name[:-1] in NAME_FIPS:
            name = name[:-1]   # footnote letter glued to the name ("Alaskab")
        if name in NAME_FIPS:
            rows[NAME_FIPS[name]] = dict(state=STATES[NAME_FIPS[name]], prisoners_2022=int(m.group(2).replace(",", "")),
                                         prisoners_2023=int(m.group(5).replace(",", "")))
    t = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    if len(t) != 50 or t.prisoners_2022.sum() != 1_070_834 or t.prisoners_2023.sum() != 1_097_597:
        raise ValueError(f"[BLOCKED] BJS Table 2 parse: {len(t)} states, {t.prisoners_2023.sum()}")
    t.index.name = "fips"
    return t


def prison_per_inmate(gp, w_rep):
    """State prison cost per state prisoner (Census level 2) relative to the US, over the group's states.

    Weights: the group's population share (primary: its custody geography is not local) and an arm that locates
    the group's prisoners by each state's own imprisonment rate (w_s * rate_s). Jails (level 3) have no local
    inmate counts by state."""
    bjs = bjs_prisoners()
    rows, arms = [], []
    for year in (2024, 2023):
        t = pd.DataFrame([{"state": int(s[0:2]), "level": int(s[2]), "item": s[4:7], "amount_k": float(s[8:20])}
                          for s in zipfile.ZipFile(FIN[year][0]).read(FIN[year][1]).decode("latin-1").splitlines()
                          if s.strip()])
        lv = t.pivot_table(index=["level", "state"], columns="item", values="amount_k", aggfunc="sum").fillna(0)
        pris = bjs[f"prisoners_{year - 1}"]   # 31 Dec of year-1 is mid FY year
        pop = populations(year).reindex(pris.index)
        for spec, cols in (("institutions", ["E04", "F04"]), ("all_corrections", ["E04", "F04", "E05", "F05"])):
            st = lv.loc[2][cols].sum(axis=1).reindex(pris.index) * 1e3
            cost = st / pris
            rel = cost / (st.sum() / pris.sum())
            w = gp.group_share.reindex(pris.index)
            w = w / w.sum()
            wr = w * (pris / pop)
            wr = wr / wr.sum()
            wreps = w_rep.reindex(pris.index)
            wreps = wreps / wreps.sum()
            wreps_r = wreps.mul(pris / pop, axis=0)
            wreps_r = wreps_r / wreps_r.sum()
            reps = {"group": wreps, "group_x_state_imprisonment": wreps_r}
            for wname, ww in (("group", w), ("group_x_state_imprisonment", wr), ("all_prisoners", pris / pris.sum())):
                ix = float((ww * rel).sum())
                se = float(np.sqrt(4 / 160 * ((rel @ reps[wname]) - ix).pow(2).sum())) if wname in reps else np.nan
                c = ww * (rel - 1)
                rows.append(dict(year=year, spec=spec, weights=wname, index=ix, index_se=se, CA=c[6], TX=c[48],
                                 rest=c.drop([6, 48]).sum(), CA_cost=cost[6], TX_cost=cost[48],
                                 us_cost=st.sum() / pris.sum(), CA_relative=rel[6], TX_relative=rel[48]))
            if year == 2024 and spec == "institutions":
                arms = pd.DataFrame({"state": [STATES[f] for f in pris.index], "prisoners": pris, "state_cost_bn": st / 1e9,
                                     "cost_per_prisoner": cost, "relative": rel})
        l1 = lv.loc[1][["E04", "F04", "E05", "F05"]].sum(axis=1).loc[0]
        l2 = lv.loc[2][["E04", "F04", "E05", "F05"]].sum(axis=1).loc[0]
        rows.append(dict(year=year, spec="state_level_share_of_sl", weights="-", index=l2 / l1))
    return pd.DataFrame(rows), arms, bjs


def receipt_indexes(gp, w_rep, w_rep_adults):
    """Effective S&L tax rate by state relative to the US, averaged over the group's states."""
    rows = []
    for year in (2024, 2023):
        fin = read_finance(year).reindex(sorted(STATES))
        bases = {"pce": pce(year), "population": populations(year)}
        for r, spec in RECEIPTS.items():
            tax = sum(fin.get(c, 0) for c in spec["codes"]) * 1e3
            base = bases[spec["base"]]
            rate = tax / base
            rel = rate / (tax.sum() / base.sum())
            weights = {"group": gp.group_share, "group_adults": gp.group_adult_share,
                       "group_income": gp.group_income_bn / gp.group_income_bn.sum(),
                       "all_residents_base": base / base.sum(), "all_residents_pep": populations(year) / populations(year).sum()}
            reps = {"group": w_rep, "group_adults": w_rep_adults}
            for wname, w in weights.items():
                ix = float((w * rel).sum())
                se = np.nan
                if wname in reps:
                    se = float(np.sqrt(4 / 160 * ((rel @ reps[wname]) - ix).pow(2).sum()))
                c = w * (rel - 1)
                rows.append(dict(year=year, receipt=r, codes="+".join(spec["codes"]), base=spec["base"],
                                 weights=wname, index=ix, index_se=se, CA=c[6], TX=c[48],
                                 rest=c.drop([6, 48]).sum(), CA_relative=rel[6], TX_relative=rel[48],
                                 us_tax_bn=tax.sum() / 1e9, us_rate=tax.sum() / base.sum()))
    return pd.DataFrame(rows)


def indexes(w: pd.Series, pc_rel: pd.DataFrame) -> pd.Series:
    return (pc_rel.mul(w, axis=0)).sum()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(HERE / "derived"))
    out = Path(ap.parse_args().out_dir)
    out.mkdir(parents=True, exist_ok=True)
    wcsv = lambda name, df: df.to_csv(out / name, lineterminator="\n", float_format="%.10g")

    by, rep, rep_adults = group_by_state()
    by.index.name = "fips"
    engine = json.loads((HERE / "derived/engine_lines.json").read_text())

    # --- group population by state (reusable) and its checks
    gp = by.assign(state=[STATES[s] for s in by.index], group_share=by.group / by.group.sum(),
                   group_adult_share=by.group_adults / by.group_adults.sum(),
                   civilian_share=by.civilian_cps / by.civilian_cps.sum())
    w_rep = rep / rep.sum()
    gp["group_share_se"] = np.sqrt(4 / 160 * ((w_rep.sub(gp.group_share, axis=0)) ** 2).sum(axis=1))
    wcsv("group_population_by_state.csv",
         gp[["state", "group", "group_share", "group_share_se", "group_records", "group_adults", "group_adult_share",
             "civilian_cps", "civilian_share"]])
    chk = pd.read_csv(STATE_POP_CHECK)
    checks = {"group_total": float(by.group.sum()), "target": TARGET_N,
              "CA_m": float(by.group[6] / 1e6), "TX_m": float(by.group[48] / 1e6),
              "ledger_stress_m": chk[chk.group.isin(MEX_GROUPS) & chk.state_group.isin(["CA", "TX"])]
              .groupby("state_group").population.sum().div(1e6).to_dict()}
    for st, fips in (("CA", 6), ("TX", 48)):
        if abs(checks["ledger_stress_m"][st] - by.group[fips] / 1e6) > 1e-6:
            raise ValueError(f"[BLOCKED] {st} disagrees with ledger_stress state_populations")

    # --- per-resident spending by state, FY2024 and FY2023, direct and current
    rows, idx_rows, dec_rows = [], [], []
    rel_store = {}
    for year in (2024, 2023):
        fin = read_finance(year)
        pop = populations(year)
        for basis in ("direct", "current"):
            amt = function_amounts(fin, basis).reindex(sorted(STATES))
            if amt.isna().any().any():
                raise ValueError(f"[BLOCKED] a state is missing from FY{year} finance")
            pc = amt.div(pop, axis=0)
            pc_us = amt.sum() / pop.sum()
            rel = pc / pc_us
            rel_store[(year, basis)] = rel
            # Check against the file's own US row (state 00)
            us_row = function_amounts(fin.loc[[0]], basis).iloc[0]
            gap = (amt.sum() - us_row).abs() / us_row
            if (gap > 1e-6).any():
                raise ValueError(f"[BLOCKED] FY{year} {basis}: states do not sum to the US row: {gap.max()}")
            for s in sorted(STATES):
                for f in FUNCTIONS:
                    rows.append(dict(year=year, basis=basis, fips=s, state=STATES[s], function=f,
                                     amount_bn=amt.at[s, f] / 1e9, population=pop[s], per_resident=pc.at[s, f],
                                     relative=rel.at[s, f]))
            weights = {
                "group": gp.group_share,
                "group_adults": gp.group_adult_share,
                "all_residents_pep": pop / pop.sum(),
                "all_civilians_cps": gp.civilian_share,
            }
            for wname, w in weights.items():
                ix = indexes(w, rel)
                se = {}
                if wname == "group":
                    reps_ix = rel.T.dot(w_rep)  # function x replicate
                    se = np.sqrt(4 / 160 * reps_ix.sub(ix, axis=0).pow(2).sum(axis=1)).to_dict()
                for f in FUNCTIONS:
                    idx_rows.append(dict(year=year, basis=basis, weights=wname, function=f, index=ix[f],
                                         index_se=se.get(f, np.nan)))
            # CA / TX / rest decomposition of (index - 1) on group weights
            for f in FUNCTIONS:
                c = gp.group_share * (rel[f] - 1)
                dec_rows.append(dict(year=year, basis=basis, function=f,
                                     CA=c[6], TX=c[48], rest=c.drop([6, 48]).sum(), total=c.sum(),
                                     CA_weight=gp.group_share[6], TX_weight=gp.group_share[48],
                                     CA_relative=rel.at[6, f], TX_relative=rel.at[48, f]))
    pd.DataFrame(rows).to_csv(out / "state_per_capita.csv", index=False, lineterminator="\n", float_format="%.10g")
    ix = pd.DataFrame(idx_rows)
    ix.to_csv(out / "indexes.csv", index=False, lineterminator="\n", float_format="%.10g")
    pd.DataFrame(dec_rows).to_csv(out / "decomposition.csv", index=False, lineterminator="\n", float_format="%.10g")

    # Positive control: population-weighted index of every function is 1 by construction.
    pc_ctrl = ix[ix.weights.eq("all_residents_pep")]["index"]
    if (pc_ctrl - 1).abs().max() > 1e-12:
        raise ValueError("[BLOCKED] all-resident index differs from 1")

    # --- wage demarcation: divide each state's relative spending by its relative S&L pay in the function
    wage, fallbacks = qcew_wage_index()
    wd = []
    for (year, basis), rel in rel_store.items():
        real = rel / wage
        for f in FUNCTIONS:
            nominal = float((gp.group_share * rel[f]).sum())
            deflated = float((gp.group_share * real[f]).sum())
            # the all-resident deflated index is not 1; report the group's relative to it
            base = float(((populations(year) / populations(year).sum()) * real[f]).sum())
            wd.append(dict(year=year, basis=basis, function=f, index=nominal, wage_level_index=float(
                (gp.group_share * wage[f]).sum()), real_index_raw=deflated, real_index_all_residents=base,
                real_index=deflated / base, wage_share_of_gap=(nominal - deflated / base) / (nominal - 1)
                if abs(nominal - 1) > 1e-9 else np.nan, qcew_fallback_states=";".join(fallbacks[f])))
    wdf = pd.DataFrame(wd)
    arm = admin_panel_arm(gp.group_share)
    if (arm.all_residents - 1).abs().max() > 1e-12:
        raise ValueError("[BLOCKED] admin panel all-resident index differs from 1")
    arm.to_csv(out / "admin_by_year.csv", index=False, lineterminator="\n", float_format="%.10g")
    wdf.to_csv(out / "wage_demarcation.csv", index=False, lineterminator="\n", float_format="%.10g")

    # --- corrections
    main_ix = ix[(ix.year == 2024) & (ix.basis == "direct") & (ix.weights == "group")].set_index("function")
    fin24 = function_amounts(read_finance(2024), "direct").reindex(sorted(STATES)).sum()
    pos_total = fin24[POS_PARTS].sum()
    lines = engine["lines"]
    corr = []

    pix, prison_states, bjs = prison_per_inmate(gp, w_rep)
    pix.to_csv(out / "prison_per_inmate.csv", index=False, lineterminator="\n", float_format="%.10g")
    prison_states.to_csv(out / "prison_cost_by_state.csv", lineterminator="\n", float_format="%.10g")
    ctrl = pix[pix.weights.eq("all_prisoners")]["index"]
    if (ctrl - 1).abs().max() > 1e-12:
        raise ValueError("[BLOCKED] prisoner-weighted per-inmate index differs from 1")
    # Central: the group's prisoners located as each state imprisons its own residents (Texas imprisons at about
    # twice California's rate); the group's population share is the high arm.
    pmain = pix[(pix.year == 2024) & (pix.spec == "institutions") & (pix.weights == "group_x_state_imprisonment")].iloc[0]
    pvar = pix[pix.weights.isin(["group", "group_x_state_imprisonment"]) & pix.spec.isin(["institutions", "all_corrections"])]
    state_share = float(pix[(pix.year == 2024) & (pix.spec == "state_level_share_of_sl")]["index"].iloc[0])

    def add(line, function, sl_amount, note, index=None, index_se=None, var=None):
        share = lines[line]["share"]
        r_lo, r_hi = lines[line]["response_low"], lines[line]["response_high"]
        if index is None:
            index = float(main_ix.at[function, "index"])
            index_se = float(main_ix.at[function, "index_se"])
            var = ix[(ix.weights == "group") & (ix.function == function)]["index"]
        pre = sl_amount * share * (index - 1)
        corr.append(dict(line=line, function=function, sl_amount_bn=sl_amount, group_share=share, index=index,
                         index_se=index_se,
                         correction_low_bn=pre * r_lo, correction_high_bn=pre * r_hi,
                         pre_response_bn=pre, response_low=r_lo, response_high=r_hi,
                         index_min_variants=float(var.min()), index_max_variants=float(var.max()),
                         clears_2pct=bool(abs(index - 1) > 0.02),
                         candidate=function in CENTRAL.get(line, []), narrow=function in NARROW, note=note))

    for f in POS_PARTS:
        amt = SL_BN["public_order_safety"] * fin24[f] / pos_total
        add("public_order_safety", f, amt,
            f"NIPA S&L POS {SL_BN['public_order_safety']}bn split by Census FY2024 direct shares; "
            f"{f} {fin24[f] / pos_total:.4f}" + ("; per-resident price, arm only: the custody key already counts "
                                                 "incarceration" if f == "corrections" else ""))
        if f == "corrections":
            add("public_order_safety", "corrections_per_inmate", amt * state_share, "state prisons (Census level 2, "
                f"{state_share:.4f} of S&L corrections) priced per state prisoner (BJS p23st Table 2), group located by w_s x state imprisonment rate (population-share arm 1.31); jails "
                "(the rest) stay national: no local jail counts by state", index=float(pmain["index"]),
                index_se=float(pmain["index_se"]), var=pvar["index"])
    add("health_services", "health", SL_BN["health_services"],
        "E32+F32 (health, excl. hospitals) prices NIPA S&L health net of sales; hospitals arms beside")
    for f in ("health_and_net_hospitals", "health_and_hospitals"):
        add("health_services", f, SL_BN["health_services"], "arm: hospital spending in the index")
    add("general_public_services", "administration", SL_BN["general_public_services"],
        "E23+E29+E31; E23 carries the FY2022 level break")
    add("general_public_services", "administration_ex_e23", SL_BN["general_public_services"],
        "E29+E31 only, clear of the E23 level break; sign not identified across years")
    add("housing_community_services", "housing_community", SL_BN["housing_community_services"],
        "E50 housing and community development; population key, same per-head logic as fire")
    add("recreation_culture", "parks_libraries", SL_BN["recreation_culture"],
        "E61 parks and recreation + E52 libraries; population key, same per-head logic as fire")
    cdf = pd.DataFrame(corr)
    cdf.to_csv(out / "corrections.csv", index=False, lineterminator="\n", float_format="%.10g")

    # --- receipts: S&L taxes keyed at a national rate
    w_rep_adults = rep_adults / rep_adults.sum()
    rix = receipt_indexes(gp, w_rep, w_rep_adults)
    ctrl = rix[rix.weights.eq("all_residents_base")]["index"]
    if (ctrl - 1).abs().max() > 1e-12:
        raise ValueError("[BLOCKED] all-resident receipt index differs from 1")
    rix.to_csv(out / "receipt_indexes.csv", index=False, lineterminator="\n", float_format="%.10g")
    rec = engine["receipts"]
    rrows = []
    for r, spec in RECEIPTS.items():
        m = rix[(rix.year == 2024) & (rix.receipt == r) & (rix.weights == spec["weights"])].iloc[0]
        var = rix[(rix.receipt == r) & rix.weights.isin(["group", "group_adults", "group_income"])]["index"]
        e = rec[r]
        gain = {end: spec["sl_bn"] * e[f"share_{end}"] * (m["index"] - 1) * e[f"response_{end}"] for end in ("low", "high")}
        rrows.append(dict(line=r, tax_codes=m["codes"], base=spec["base"], weights=spec["weights"],
                          sl_amount_bn=spec["sl_bn"], national_bn=e["national_bn"], group_share_low=e["share_low"],
                          group_share_high=e["share_high"], index=m["index"], index_se=m["index_se"],
                          receipt_gain_low_bn=gain["low"], receipt_gain_high_bn=gain["high"],
                          cost_effect_low_bn=-gain["low"], cost_effect_high_bn=-gain["high"],
                          response_low=e["response_low"], response_high=e["response_high"],
                          index_min_variants=float(var.min()), index_max_variants=float(var.max()),
                          clears_2pct=bool(abs(m["index"] - 1) > 0.02), candidate=bool(abs(m["index"] - 1) > 0.02),
                          note=f"S&L part of the NIPA line; rate = Census {m['codes']} per $ of "
                               f"{'BEA SAPCE PCE' if spec['base'] == 'pce' else 'resident'}"))
    NO_CORRECTION = {
        "state_local_income_tax": "key state_liability = CPS STATETAX_A, already each state's own tax",
        "other_personal_tax": "key state_liability, already state-specific",
        "modeled_owner_property": "owner model = each state's effective property tax rate x reported home value "
                                  "(gen_ledger_extension state_parameters); response 0",
        "personal_property_tax": "key capital, response 0: no effect on the account; capital incidence is not by residence",
        "remaining_production_property": "business property, key capital, response 0: no effect; incidence not by residence",
        "other_production_taxes": "key capital (business licences, severance, special assessments), response 0: no effect",
        "personal_current_transfers": "fines, fees and donations (federal + S&L), not a tax rate; left national",
        "customs_duties": "federal",
    }
    for r, why in NO_CORRECTION.items():
        e = rec[r]
        rrows.append(dict(line=r, national_bn=e["national_bn"], group_share_low=e["share_low"],
                          group_share_high=e["share_high"], response_low=e["response_low"],
                          response_high=e["response_high"], receipt_gain_low_bn=0.0, receipt_gain_high_bn=0.0,
                          cost_effect_low_bn=0.0, cost_effect_high_bn=0.0, candidate=False, note=why))
    rdf = pd.DataFrame(rrows)
    rdf.to_csv(out / "receipts_corrections.csv", index=False, lineterminator="\n", float_format="%.10g")

    # --- net state correction on the cost (spending up, receipts down), at each band end
    for line, funcs in CENTRAL.items():   # a line in the central package must have a function that clears the bar
        opened = cdf[(cdf.line == line) & cdf.clears_2pct & cdf.function.isin(funcs)]
        if opened.empty:
            raise ValueError(f"[BLOCKED] central line {line} has no function clearing the bar")
    rc = rdf[rdf.candidate]
    net = []
    for name, sp in (("narrow_police_health", cdf[cdf.narrow]), ("central_all_sl_subfunctions", cdf[cdf.candidate])):
        for end in ("low", "high"):
            s_bn = float(sp[f"correction_{end}_bn"].sum())
            r_bn = float(rc[f"receipt_gain_{end}_bn"].sum())
            net.append(dict(package=name, end=end, spending_bn=s_bn, receipts_gain_bn=r_bn, net_cost_bn=s_bn - r_bn,
                            functions="+".join(sp.function)))
    ndf = pd.DataFrame(net)
    ndf.to_csv(out / "net_state_correction.csv", index=False, lineterminator="\n", float_format="%.10g")

    inputs = [CPS, BUILDER, SAPCE, BJS, POP, QCEW, STATE_POP_CHECK, ADMIN_PANEL, HERE / "derived/engine_lines.json", Path(__file__)] + \
             [z for z, _ in FIN.values()]
    manifest = {"checks": checks,
                "inputs": {str(p.relative_to(ROOT)): sha(p) for p in inputs},
                "qcew_fallback_states": fallbacks}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
    print(json.dumps(checks, indent=1))
    print(cdf[["line", "function", "sl_amount_bn", "group_share", "index", "index_se", "correction_low_bn",
               "correction_high_bn", "index_min_variants", "index_max_variants", "clears_2pct"]]
          .to_string(float_format=lambda v: f"{v:.4f}"))
    print(rdf[rdf.candidate][["line", "index", "index_se", "receipt_gain_low_bn", "receipt_gain_high_bn",
                              "index_min_variants", "index_max_variants", "clears_2pct"]]
          .to_string(float_format=lambda v: f"{v:.4f}"))
    print(ndf.to_string(float_format=lambda v: f"{v:.3f}"))


if __name__ == "__main__":
    main()
