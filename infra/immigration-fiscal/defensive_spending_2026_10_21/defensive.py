"""Defensive labor and spending: US vs Japan tables (Q1, Q2) and the US metro cross-section (Q4).

Run from the repository root (statsmodels and xlrd are not in the project venv):
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with statsmodels --with xlrd python3 \
        infra/immigration-fiscal/defensive_spending_2026_10_21/defensive.py

Inputs live in this lane's ignored `_cache/` (acquisition commands in RESULT.md "Reproduce").
Outputs go to `derived/`. Every hard-coded constant carries its source.
"""
import csv
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
OUT = LANE / "derived"

# ---- Constants with sources -------------------------------------------------------------------
# Japan, administrative counts
JP_GUARDS = 584_868          # NPA 令和5年における警備業の概況: 警備員数, end-2023
JP_POLICE = 2_312 + 259_595  # NPA 警察白書 R6 図表7-1: 警察庁警察官 + 地方警察官 定員, 2024-04-01
JP_PRISON_OFFICERS = 17_280  # MOJ 矯正局 pamphlet (moj.go.jp/content/001323824.pdf): 刑務官 定員 2025
JP_PRISONERS = 40_853        # same pamphlet, 刑事施設 2023 (figure label; garbled extraction) [UNVERIFIED digit read]
JP_SDF = 227_000             # [TRAINING-DATA] 自衛官 現員 c. 2023-24, ~0.22-0.23M; MOD 資料67 table is an image
JP_LAWYERS = 45_808          # JFBA 弁護士白書2024 資料1-2-22, 2024-03-31
JP_SCRIVENERS = 23_156       # same table, 司法書士 2024-04-01
JP_PATENT_ATTORNEYS = 11_745  # same table, 弁理士
JP_ADMIN_SCRIVENERS = 51_619  # same table, 行政書士 (shown beside, not added)
JP_TAX_ACCOUNTANTS = 81_280   # same table, 税理士 (shown beside, not added)
JP_POP_2023 = 124_352_000     # [TRAINING-DATA] 総務省人口推計 2023-10-01
# United States
US_LAWYERS_ABA = 1_322_649    # ABA National Lawyer Population Survey, active lawyers 2024-01-01
US_INCARCERATED = 1_852_900   # BJS CPUS 2023 table 1: prisons + local jails, yearend 2023
US_ACTIVE_DUTY = 1_273_828    # DMDC Active Duty Military Personnel by Rank/Grade, 2024-12-31
US_POP = 334_914_896          # ACS 2023 1-year B01003 (cached `acs1_2023_us.json`)
# Switzerland (plan change 1; quoted cells in sources_switzerland.md). FTE counts, so understated vs headcounts.
CH_POLICE_FTE = 18_821        # KKPKS Polizeibestände 01.01.2023, Pol I-IV incl. fedpol
CH_PRISON_SECURITY_FTE = 3_266  # BFS Justizvollzugseinrichtungen am Stichtag, "davon Sicherheit"
CH_PRIVATE_SECURITY = 23_000  # VSSU via SRF 2023-01-25, "über 23'000 Angestellte" [persons or FTE unclear]
CH_PRISONERS = 6_881          # BFS Medienmitteilung 29.4.2024, 31 Jan 2024
CH_PRO_MILITARY = 3_000       # armee.ch "rund 3'000 Berufsmilitär" (militia 146,974 not comparable; beside)
CH_LAWYERS_SAV = 11_910       # SAV/FSA Mitgliederbestand 31.12.2025
CH_POP = 8_962_300            # BFS ständige Wohnbevölkerung 31.12.2023

REGION = {  # Census regions by state postal code
    **{s: "NE" for s in "CT ME MA NH RI VT NJ NY PA".split()},
    **{s: "MW" for s in "IL IN MI OH WI IA KS MN MO NE ND SD".split()},
    **{s: "S" for s in "DE DC FL GA MD NC SC VA WV AL KY MS TN AR LA OK TX".split()},
    **{s: "W" for s in "AZ CO ID MT NV NM UT WY AK CA HI OR WA PR".split()},
}
# Gaming/tourism/federal metros dropped in the robustness arm (pre-registered by name)
DROP_KEYS = {("las vegas", "NV"), ("reno", "NV"), ("atlantic city", "NJ"), ("urban honolulu", "HI"),
             ("washington", "DC")}
# Post-hoc arm (added after the first results): metros on the Mexican border, where Border Patrol,
# port-of-entry and detention staffing sit regardless of local crime
BORDER_KEYS = {("san diego", "CA"), ("el centro", "CA"), ("yuma", "AZ"), ("tucson", "AZ"), ("sierra vista", "AZ"),
               ("las cruces", "NM"), ("el paso", "TX"), ("laredo", "TX"), ("mcallen", "TX"), ("brownsville", "TX")}


def write_csv(path, rows, fields):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return np.nan


# ---- Q1: US national guard labor and lawyers --------------------------------------------------
def q1():
    nat = pd.read_excel(CACHE / "oesm24nat/national_M2024_dl.xlsx")
    nat = nat.drop_duplicates("OCC_CODE").set_index("OCC_CODE")
    total = num(nat.loc["00-0000", "TOT_EMP"])
    groups = {
        "police_detectives": ["33-3051", "33-3052", "33-3021", "33-1012"],
        "corrections_bailiffs": ["33-3012", "33-3011", "33-1011"],
        "private_guards_detectives": ["33-9032", "33-9021", "33-9031", "33-1091"],
        "screeners_other_protective": ["33-9093", "33-9099", "33-1099"],
        "firefighters_beside": ["33-2011"],
        "lawyers": ["23-1011"],
        "paralegals_beside": ["23-2011"],
        "engineers_beside": ["17-2000"],
    }
    rows = []
    for g, codes in groups.items():
        emp = sum(num(nat.loc[c, "TOT_EMP"]) for c in codes)
        wages = sum(num(nat.loc[c, "TOT_EMP"]) * num(nat.loc[c, "A_MEAN"]) for c in codes)
        rows.append(dict(country="US", group=g, codes=" ".join(codes), persons=round(emp),
                         per_100_employed=round(100 * emp / total, 4), wage_bill_bn=round(wages / 1e9, 2),
                         basis="BLS OEWS May 2024 national, wage-and-salary jobs (no self-employed, no military)"))
    narrow_us = sum(r["persons"] for r in rows if r["group"] in
                    ("police_detectives", "corrections_bailiffs", "private_guards_detectives"))
    # Japan rows: admin counts over ILOSTAT 2023 LFS employment
    ilo = list(csv.DictReader(open(CACHE / "ilo_oc2.csv", encoding="utf-8-sig")))
    jp_emp = 1000 * float(next(r["obs_value"] for r in ilo if r["ref_area"] == "JPN" and r["time"] == "2023"
                               and r["classif1"] == "OC2_ISCO08_TOTAL"))
    jp = [("police_detectives", JP_POLICE, "NPA 警察白書 R6 police officers (定員)"),
          ("corrections_bailiffs", JP_PRISON_OFFICERS, "MOJ 刑務官 定員 2025"),
          ("private_guards_detectives", JP_GUARDS, "NPA 警備員数 end-2023")]
    for g, n, b in jp:
        rows.append(dict(country="JP", group=g, codes="", persons=n, per_100_employed=round(100 * n / jp_emp, 4),
                         wage_bill_bn="", basis=b + "; denominator LFS 2023 employment via ILOSTAT"))
    narrow_jp = JP_POLICE + JP_PRISON_OFFICERS + JP_GUARDS
    che = list(csv.DictReader(open(CACHE / "ilo_oc2_che.csv", encoding="utf-8-sig")))
    ch_emp = 1000 * float(next(r["obs_value"] for r in che if r["time"] == "2024" and r["classif1"] == "OC2_ISCO08_TOTAL"))
    ch = [("police_detectives", CH_POLICE_FTE, "KKPKS Pol I-IV FTE 2023"),
          ("corrections_bailiffs", CH_PRISON_SECURITY_FTE, "BFS prison security FTE"),
          ("private_guards_detectives", CH_PRIVATE_SECURITY, "VSSU via SRF 2023 [secondary]")]
    for g, n, b in ch:
        rows.append(dict(country="CH", group=g, codes="", persons=n, per_100_employed=round(100 * n / ch_emp, 4),
                         wage_bill_bn="", basis=b + "; denominator LFS 2024 employment via ILOSTAT"))
    narrow_ch = CH_POLICE_FTE + CH_PRISON_SECURITY_FTE + CH_PRIVATE_SECURITY
    summ = [
        dict(measure="narrow guard labor per 100 employed", US=round(100 * narrow_us / total, 3),
             JP=round(100 * narrow_jp / jp_emp, 3), CH=round(100 * narrow_ch / ch_emp, 3)),
        dict(measure="active military per 100 employed", US=round(100 * US_ACTIVE_DUTY / total, 3),
             JP=round(100 * JP_SDF / jp_emp, 3), CH="beside: professional %.3f; militia not comparable"
             % (100 * CH_PRO_MILITARY / ch_emp)),
        dict(measure="incarcerated per 100 employed", US=round(100 * US_INCARCERATED / total, 3),
             JP=round(100 * JP_PRISONERS / jp_emp, 3), CH=round(100 * CH_PRISONERS / ch_emp, 3)),
        dict(measure="narrow + military + incarcerated per 100 employed",
             US=round(100 * (narrow_us + US_ACTIVE_DUTY + US_INCARCERATED) / total, 3),
             JP=round(100 * (narrow_jp + JP_SDF + JP_PRISONERS) / jp_emp, 3),
             CH=round(100 * (narrow_ch + CH_PRO_MILITARY + CH_PRISONERS) / ch_emp, 3)),
        dict(measure="bar-admitted lawyers per 100k residents", US=round(1e5 * US_LAWYERS_ABA / US_POP, 1),
             JP=round(1e5 * JP_LAWYERS / JP_POP_2023, 1),
             CH="SAV members (independent practice) %.1f" % (1e5 * CH_LAWYERS_SAV / CH_POP)),
        dict(measure="OEWS-employed lawyers per 100k residents", US=round(1e5 * num(nat.loc["23-1011", "TOT_EMP"]) / US_POP, 1),
             JP=""),
        dict(measure="JP lawyers + judicial scriveners + patent attorneys per 100k", US="",
             JP=round(1e5 * (JP_LAWYERS + JP_SCRIVENERS + JP_PATENT_ATTORNEYS) / JP_POP_2023, 1)),
        dict(measure="JP above + administrative scriveners (beside) per 100k", US="",
             JP=round(1e5 * (JP_LAWYERS + JP_SCRIVENERS + JP_PATENT_ATTORNEYS + JP_ADMIN_SCRIVENERS) / JP_POP_2023, 1)),
        dict(measure="JP tax accountants (beside) per 100k", US="", JP=round(1e5 * JP_TAX_ACCOUNTANTS / JP_POP_2023, 1)),
    ]
    write_csv(OUT / "guard_labor_us_japan.csv", rows, list(rows[0]))
    write_csv(OUT / "guard_lawyer_summary.csv", summ, ["measure", "US", "JP", "CH"])
    # ILOSTAT ISCO-08 sub-major group 54 (protective services incl. firefighters), one survey basis
    best = {}
    for r in ilo + che:
        if r["obs_value"] == "":
            continue
        best.setdefault(r["ref_area"], {}).setdefault(r["time"], {})[r["classif1"]] = float(r["obs_value"])
    irows = []
    for c, by in sorted(best.items()):
        yrs = [t for t in by if "OC2_ISCO08_54" in by[t]]
        t = max(yrs)
        irows.append(dict(country=c, year=t, isco54_thousands=by[t]["OC2_ISCO08_54"],
                          employment_thousands=by[t]["OC2_ISCO08_TOTAL"],
                          isco54_per_100=round(100 * by[t]["OC2_ISCO08_54"] / by[t]["OC2_ISCO08_TOTAL"], 3)))
    write_csv(OUT / "ilo_isco54_shares.csv", irows, list(irows[0]))
    return total


# ---- Occupational and industry mix (plan change 1): ISCO major groups and ISIC sections ------
def mix():
    rows = []
    for fname, kind in (("ilo_oc1.csv", "ISCO-08 major group"), ("ilo_eco.csv", "ISIC rev4 section")):
        by = {}
        for r in csv.DictReader(open(CACHE / fname, encoding="utf-8-sig")):
            if r["obs_value"] and ("_ISCO08_" in r["classif1"] or "_ISIC4_" in r["classif1"]):
                by.setdefault((r["ref_area"], r["time"]), {})[r["classif1"]] = float(r["obs_value"])
        for c in ("USA", "JPN", "CHE"):
            years = [t for (cc, t), v in by.items() if cc == c and len(v) > 5]
            t = max(years)
            v = by[(c, t)]
            tot = next(x for k, x in v.items() if k.endswith("TOTAL"))
            for k, x in sorted(v.items()):
                if not k.endswith("TOTAL"):
                    rows.append(dict(country=c, year=t, classification=kind, code=k.split("_")[-1],
                                     thousands=x, share_pct=round(100 * x / tot, 2)))
    write_csv(OUT / "employment_mix_us_jp_ch.csv", rows, list(rows[0]))


# ---- Q2: COFOG defence and public order, % of GDP ---------------------------------------------
def q2():
    gdp = {(x["countryiso3code"], x["date"]): x["value"] for x in json.load(open(CACHE / "wb_gdp_lcu.json"))[1]}
    rows = []
    for x in csv.DictReader(open(CACHE / "oecd_cofog_probe.csv", encoding="utf-8-sig")):
        if x["SECTOR"] != "S13" or x["TRANSACTION"] != "OTE" or x["TIME_PERIOD"] != "2023":
            continue
        if not (x["EXPENDITURE"].startswith(("GF02", "GF03")) or x["EXPENDITURE"] == "_T"):
            continue
        val = float(x["OBS_VALUE"]) * 10 ** int(x["UNIT_MULT"])
        rows.append(dict(country=x["REF_AREA"], year=2023, cofog=x["EXPENDITURE"],
                         lcu_bn=round(val / 1e9, 1),
                         pct_gdp=round(100 * val / gdp[(x["REF_AREA"], "2023")], 3)))
    rows.sort(key=lambda r: (r["country"], r["cofog"]))
    write_csv(OUT / "cofog_defence_order_2023.csv", rows, list(rows[0]))


# ---- Q4: metro cross-section ------------------------------------------------------------------
def key(name):
    """(first principal city, first state) from an OEWS, ACS or FBI metro name."""
    name = re.sub(r"M\.S\.A\.\d*|Metro Area|Micro Area|M\.D\.\d*", "", str(name)).strip()
    city, _, states = name.partition(",")
    city = re.sub(r"\d+$", "", city.split("-")[0].strip()).lower()
    st = re.sub(r"\d", "", states.strip().split("-")[0])[:2]
    return city, st


def q4():
    m = pd.read_excel(CACHE / "oesm24ma/MSA_M2024_dl.xlsx", dtype={"AREA": str})
    m = m[m.AREA_TYPE == 4]
    wide = m.pivot_table(index=["AREA", "AREA_TITLE"], columns="OCC_CODE", values="TOT_EMP", aggfunc="first")
    codes = ["00-0000", "33-9032", "33-3051", "33-3012", "33-3021", "33-3011", "23-1011", "33-9031"]
    wide = wide[codes].map(num).reset_index()
    tot = wide["00-0000"]
    out = pd.DataFrame({"cbsa": wide.AREA.str.zfill(5), "title": wide.AREA_TITLE, "jobs": tot})
    out["guards"] = 100 * wide["33-9032"] / tot
    # public: patrol + corrections required; suppressed detectives/bailiffs counted as 0 (deviation noted)
    pub = wide["33-3051"] + wide["33-3012"]
    out["public_protective"] = 100 * (pub + wide["33-3021"].fillna(0) + wide["33-3011"].fillna(0)) / tot
    out["police_only"] = 100 * (wide["33-3051"] + wide["33-3021"].fillna(0)) / tot
    out["corrections_only"] = 100 * (wide["33-3012"] + wide["33-3011"].fillna(0)) / tot
    out["lawyers"] = 100 * wide["23-1011"] / tot
    out["gaming_surv"] = 100 * wide["33-9031"].fillna(0) / tot
    acs = json.load(open(CACHE / "acs5_2023_cbsa.json"))
    a = pd.DataFrame(acs[1:], columns=acs[0])
    a = a.rename(columns={"metropolitan statistical area/micropolitan statistical area": "cbsa"})
    for c in a.columns[1:-1]:
        a[c] = a[c].astype(float)
    a["pop"] = a.B01003_001E
    a["mex_share"] = 100 * a.B03001_004E / a.B03001_001E
    a["fb_share"] = 100 * a.B05002_013E / a.B05002_001E
    a["black_share"] = 100 * a.B03002_004E / a.B01003_001E
    a["poverty"] = 100 * a.B17001_002E / a.B17001_001E
    a["ln_income"] = np.log(a.B19013_001E)
    a["ln_pop"] = np.log(a["pop"])
    df = out.merge(a[["cbsa", "NAME", "pop", "mex_share", "fb_share", "black_share", "poverty", "ln_income",
                      "ln_pop"]], on="cbsa", how="left")
    df["key_city"], df["state"] = zip(*df.title.map(key))
    df["region"] = df.state.map(REGION)
    # FBI 2018 Table 6 violent crime rate per 100k, matched by (first city, first state)
    t = pd.read_excel(CACHE / "fbi_2018_table6.xls", header=None)
    crime, cur = {}, None
    for _, r in t.iterrows():
        if isinstance(r[0], str) and "M.S.A" in r[0]:
            cur = key(r[0])
        elif cur and str(r[1]).startswith("Rate per 100,000"):
            crime.setdefault(cur, num(r[3]))
    df["violent_rate"] = [crime.get((c, s), np.nan) for c, s in zip(df.key_city, df.state)]
    df["drop_arm"] = [((c, s) in DROP_KEYS) for c, s in zip(df.key_city, df.state)]
    df["border"] = [((c, s) in BORDER_KEYS) for c, s in zip(df.key_city, df.state)]
    df.round(5).to_csv(OUT / "metro_panel.csv", index=False, lineterminator="\n")

    base = ["ln_income", "poverty", "ln_pop", "black_share"]
    rows = []
    for y in ["guards", "public_protective", "police_only", "corrections_only", "lawyers"]:
        for x in ["mex_share", "fb_share"]:
            specs = [("bivariate", [x], False, False), ("controls+region", [x] + base, True, False),
                     ("controls+region+crime", [x] + base + ["violent_rate"], True, False),
                     ("controls+region, drop gaming/tourism/DC", [x] + base, True, True),
                     ("controls+region, drop border metros [post-hoc]", [x] + base, True, "border")]
            for label, xs, reg, drop in specs:
                d = df.dropna(subset=[y] + xs + ["region"])
                if drop == "border":
                    d = d[~d.border]
                elif drop:
                    d = d[~d.drop_arm & (d.gaming_surv < 0.1)]
                X = d[xs].copy()
                if reg:
                    X = X.join(pd.get_dummies(d.region, prefix="r", drop_first=True, dtype=float))
                X = sm.add_constant(X)
                for wt in (False, True):
                    fit = (sm.WLS(d[y], X, weights=d["pop"]) if wt else sm.OLS(d[y], X)).fit(cov_type="HC1")
                    w = d["pop"]
                    xbar = np.average(d[x], weights=w)
                    ybar = np.average(d[y], weights=w)
                    b, se = fit.params[x], fit.bse[x]
                    rows.append(dict(outcome=y, regressor=x, spec=label, weighted=wt, n=int(fit.nobs),
                                     b=round(b, 5), se=round(se, 5), p=round(fit.pvalues[x], 4),
                                     r2=round(fit.rsquared, 3), pop_wtd_mean_x=round(xbar, 2),
                                     pop_wtd_mean_y=round(ybar, 4),
                                     implied_share_linked=round(b * xbar / ybar, 4)))
    write_csv(OUT / "metro_regressions.csv", rows, list(rows[0]))
    stats = dict(oews_msas=len(out), acs_matched=int(df["pop"].notna().sum()),
                 crime_matched=int(df.violent_rate.notna().sum()),
                 guards_nonmissing=int(df.guards.notna().sum()),
                 public_nonmissing=int(df.public_protective.notna().sum()),
                 lawyers_nonmissing=int(df.lawyers.notna().sum()))
    with open(OUT / "metro_match_stats.json", "w") as f:
        json.dump(stats, f, indent=1)
        f.write("\n")
    return stats


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    q1()
    mix()
    q2()
    print(json.dumps(q4()))
