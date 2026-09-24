#!/usr/bin/env python3
"""Career cost to non-Hispanic white natives of race- and ethnicity-based preferences.

Accounting scenarios, not causal estimates of a single policy. Each channel multiplies a
measured count (IPEDS fall 2023 first-year enrollment, USAspending FY2022-FY2024 contract
obligations, CPS ASEC 2025 earnings) by published effect sizes that are page-cited in
PARAMS below. Every assumed (not published) value is tagged [INFERENCE] in its note.

Inputs (all local; no network):
  _cache/ipeds/{HD2023,adm2023,ef2023a}.csv          IPEDS fall 2023
  _cache/dt_306_10_d24.html                           NCES Digest 2024 Table 306.10
  _cache/usaspending/*.json                           USAspending spending_over_time pulls
  ../gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip   CPS ASEC 2025 (income 2024)

Outputs: derived/calc_output.txt, derived/channels.csv, derived/ipeds_tiers.csv
Run:     OPENBLAS_NUM_THREADS=1 uv run --no-project --with lxml python3 \
             infra/immigration-fiscal/affirmative_action_cost_2026_09_24/calc.py
"""
from __future__ import annotations

import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
ASEC = HERE.parent / "gen_ledger_extension_2026_09_16" / "_cache" / "asecpub25csv.zip"

LCH = ("low", "central", "high")

# ---------------------------------------------------------------------------------------------
# Published parameters. (low, central, high) triples; notes carry the page citation or the
# [INFERENCE] reason. Central = midpoint or mean of the cited values unless the note says so.
# ---------------------------------------------------------------------------------------------
AKR = dict(  # Arcidiacono-Kinsler-Ransom, "What the SFFA cases reveal", Duke version 2023, Table 11 p. 62
    harvard=dict(white=(2704, 3195), black=(1163, 324), hisp=(1188, 581), asian=(2013, 2812)),
    unc_oos=dict(white=(6954, 8878), black=(1605, 208), hisp=(1821, 738), asian=(2698, 3260)),
    unc_in=dict(white=(18865, 19889), black=(2374, 1532), hisp=(1470, 1212), asian=(3223, 3370)),
)
EC = dict(white=(5134, 5256), black=(899, 326), hisp=(792, 381), asian=(2369, 3141))  # Espenshade-Chung 2005 Table 2 p. 299
HINRICHS = dict(  # Hinrichs 2012 Table 5 p. 717: ban effects (pp) and Table 4 bases; signs from text p. 717
    t2t_public=dict(black=-1.1778, hisp=-1.2213, aian=-0.1397, white=1.7790, asian=0.9158,
                    base_black=5.76, base_hisp=6.36),
    top50_public=dict(black=-1.7429, hisp=-2.0332, aian=-0.4660, white=2.9268, asian=1.4298,
                      base_black=5.79, base_hisp=7.38),
)


def red(pair):
    before, after = pair
    return 1 - after / before


def white_share_of_freed(d):
    lost = (d["black"][0] - d["black"][1]) + (d["hisp"][0] - d["hisp"][1])
    return (d["white"][1] - d["white"][0]) / lost


def tri(vals):
    v = sorted(vals)
    return (v[0], float(np.mean(v)), v[-1])


# Elite tier: proportional loss of URM seats and white share of freed seats.
RED_E = dict(black=tri([red(EC["black"]), red(AKR["harvard"]["black"])]),
             hisp=tri([red(EC["hisp"]), red(AKR["harvard"]["hisp"])]))
W_E = tri([white_share_of_freed(EC), white_share_of_freed(AKR["harvard"])])
# Selective tier: Hinrichs ban effects (with institutional response) and AKR UNC in-state (without).
RED_S = dict(
    black=tri([-HINRICHS["t2t_public"]["black"] / HINRICHS["t2t_public"]["base_black"],
               -HINRICHS["top50_public"]["black"] / HINRICHS["top50_public"]["base_black"],
               red(AKR["unc_in"]["black"])]),
    hisp=tri([-HINRICHS["t2t_public"]["hisp"] / HINRICHS["t2t_public"]["base_hisp"],
              -HINRICHS["top50_public"]["hisp"] / HINRICHS["top50_public"]["base_hisp"],
              red(AKR["unc_in"]["hisp"])]),
)


def hin_white_share(d):
    return d["white"] / -(d["black"] + d["hisp"] + d["aian"])


W_S = tri([hin_white_share(HINRICHS["t2t_public"]), hin_white_share(HINRICHS["top50_public"]),
           white_share_of_freed(AKR["unc_in"]), white_share_of_freed(AKR["unc_oos"])])

CPI_2007, CPI_2024 = 207.342, 313.689  # CPI-U annual averages [TRAINING-DATA; BLS series CUUR0000SA0]
PARAMS = dict(
    # admissions earnings effects (proportional loss for a white student moved down one notch)
    r_elite=((0.0, 0.115, 0.23),
             "low: Dale-Krueger w17159 p.25 selection-adjusted return ~0; high: Chetty-Deming-Friedman "
             "w31492 p.37 mean proportional Ivy-Plus vs flagship effect 23%; central: half of 23% because "
             "the displaced applicant's next-best is above a flagship (CDF p.30) [INFERENCE]"),
    r_sel=((0.0, 0.03, 0.10),
           "low: Bleemer QJE Fig. VIII p.36 Berkeley RD log wages -0.10 (0.11), DK selection-adjusted ~0; "
           "high: Hoekstra 2009 via DK p.2, +20% men, 0 women -> 10% average; central: half of DK p.25 "
           "basic-model 6% per 100 school-SAT points [INFERENCE]"),
    elite_earn_2007=(139698, "Dale-Krueger w17159 Table 1 p.29: 1989-cohort mean 2007 earnings, C&B colleges"),
    career_years=(40, "entry cohorts aged 22-61 in the stock year [INFERENCE: career span]"),
    discount=(0.03, "real discount rate for per-cohort present values [INFERENCE]"),
    # employment
    contractor_share=(0.25, "Miller 2017 AEJ Applied p.153: contractors employ about a quarter of the "
                            "US workforce (OFCCP 2013)"),
    shift_pp=((0.032, 1.0, 2.0),
              "pp of contractor employment moved from whites to preferred groups. low: Kurtulus 2016 "
              "Table 4 p.53 white female -0.122 + white male +0.090; central: Miller 2017 p.153 Black "
              "+0.8 pp at 5 years plus Hispanic +0.2 [INFERENCE: fn 1 says 'qualitatively similar', "
              "Kurtulus finds Hispanic shares fell]; high: Miller's +0.8 plus +0.8 persistence, Hispanic "
              "+0.4 [INFERENCE]"),
    r_emp=((0.0, 0.05, 0.10),
           "earnings loss of a displaced white worker relative to the next job. low: pure reshuffling "
           "across employers (mechanism in Leonard 1990 and Smith-Welch as summarized by Holzer-Neumark "
           "w7323 p.37) [INFERENCE: zero loss]; central/high [INFERENCE: Holzer-Neumark p.37 expect some "
           "loss because sector wage levels differ, but no cited paper measures it]"),
    hisp_share_emp=((0.0, 0.2, 0.5),
                    "Hispanic share of the employment shift. low: Kurtulus Table 4 Hispanic men -0.058; "
                    "central 0.2/1.0 [INFERENCE]; high: Hispanic effect equal to Black (Miller fn 1)"),
    # contracting
    share_shifted_8a=((0.5, 0.75, 1.0),
                      "share of 8(a)-restricted dollars that non-8(a) firms would otherwise win [INFERENCE]"),
    margin=((0.03, 0.06, 0.10), "economic profit margin on a federal contract [INFERENCE]"),
    dbe_awards_fy2020=(6.2e9, "CRS IF12055 v3: FY2020 nationwide DBE awards and commitments ~$6.2bn"),
    dbe_minority_share=(7.0 / (7.0 + 5.8), "Marion 2007 WP p.12: 1993-99 MBE 7.0% vs WBE 5.8% of "
                                            "federal-aid highway dollars [dated]"),
    dbe_pref_caused=((4.3 / 12.6, 0.5, 0.8),
                     "share of DBE dollars caused by goals. low: Marion 2007 WP p.4 10pp goal -> +4.3pp "
                     "utilization over 12.6% average participation (p.11); high: 'nearly one-for-one' "
                     "without state trends (p.4) [INFERENCE: 0.8]; central midpoint [INFERENCE]"),
    dbe_participation=(0.126, "Marion 2007 WP p.11: 12.6% of federal-aid contract dollars to MBEs/WBEs"),
    premium_dbe=((0.0, 0.028, 0.056), "Marion 2009 REStat abstract p.503: state-funded prices -5.6% after "
                                      "Prop 209 (full text paywalled); central half [INFERENCE]"),
    premium_8a=((0.0, 0.0, 0.056), "no causal estimate for 8(a); high borrows Marion's 5.6% [INFERENCE]"),
    dbe_2024_scale=((1.0, 1.0, 1.35), "FY2024 DBE dollars relative to FY2020 [INFERENCE: IIJA raised "
                                      "federal-aid obligations; national total not published]"),
)

BAN_STATES = {"CA", "WA", "FL", "MI", "NE", "AZ", "NH", "OK", "ID"}  # public-university bans before 2023
TERRITORIES = {"PR", "GU", "VI", "AS", "MP", "FM", "MH", "PW"}
RACE = dict(white="EFWHITT", black="EFBKAAT", hisp="EFHISPT", aian="EFAIANT", asian="EFASIAT",
            nhpi="EFNHPIT", two="EF2MORT", unknown="EFUNKNT", nonres="EFNRALT", total="EFTOTLT")


def p(key):
    return PARAMS[key][0]


# ---------------------------------------------------------------------------------------------
def read_ipeds_csv(name):
    d = pd.read_csv(CACHE / "ipeds" / name, encoding="latin-1", low_memory=False)
    d.columns = [c.replace("﻿", "").replace("ï»¿", "").strip() for c in d.columns]
    return d


def ipeds_tiers(log):
    hd = read_ipeds_csv("HD2023.csv")[["UNITID", "INSTNM", "STABBR", "CONTROL", "ICLEVEL", "HBCU"]]
    adm = read_ipeds_csv("adm2023.csv")
    ef = read_ipeds_csv("ef2023a.csv")
    ef = ef[ef.EFALEVEL == 4][["UNITID"] + list(RACE.values())]
    for c in ["APPLCN", "ADMSSN", "SATVR50", "SATMT50", "ACTCM50"]:
        adm[c] = pd.to_numeric(adm[c], errors="coerce")
    adm = adm[["UNITID", "APPLCN", "ADMSSN", "SATVR50", "SATMT50", "ACTCM50"]]
    d = hd.merge(adm, on="UNITID", how="inner").merge(ef, on="UNITID", how="inner")
    d = d[(d.ICLEVEL == 1) & (d.HBCU != 1) & (d.APPLCN >= 1000) & ~d.STABBR.isin(TERRITORIES)].copy()
    d["admit"] = d.ADMSSN / d.APPLCN
    d["sat50"] = d.SATVR50 + d.SATMT50
    high_scores = (d.sat50 >= 1200) | (d.ACTCM50 >= 26)
    banned_public = (d.CONTROL == 1) & d.STABBR.isin(BAN_STATES)
    broad_scores = (d.sat50 >= 1250) | (d.ACTCM50 >= 27)
    d["tier"] = np.where(d.admit < 0.15, "E", np.where((d.admit < 0.50) & high_scores, "S", np.where(
        (d.admit < 0.70) & broad_scores, "B", "N")))
    d.loc[banned_public, "tier"] = "ban"
    for uid, name, tier in [(166027, "Harvard", "E"), (199120, "UNC Chapel Hill", "S"),
                            (110662, "UCLA", "ban")]:
        got = d.loc[d.UNITID == uid, "tier"]
        if got.empty or got.iloc[0] != tier:
            raise SystemExit(f"[BLOCKED] tier gate failed for {name}: {got.tolist()}")
    rows = []
    for tier in ["E", "S", "B"]:
        t = d[d.tier == tier]
        row = dict(tier=tier, institutions=len(t), private_share=float((t.CONTROL != 1).mean()))
        row.update({k: float(t[v].sum()) for k, v in RACE.items()})
        rows.append(row)
    tiers = pd.DataFrame(rows).set_index("tier")
    tiers.to_csv(OUT / "ipeds_tiers.csv", float_format="%.1f")
    log("IPEDS fall 2023 first-time degree-seeking (EFALEVEL 4), four-year, >=1000 applicants, no HBCUs;")
    log("  public universities in pre-2023 ban states excluded; E = admit rate <15%;")
    log("  S = admit 15-50% and SAT median >=1200 or ACT median >=26; B (high scenario only) = admit")
    log("  50-70% and SAT median >=1250 or ACT median >=27; territories excluded")
    for tier, r in tiers.iterrows():
        log(f"  tier {tier}: {r.institutions:.0f} institutions ({r.private_share:.0%} private), first-year "
            f"{r.total:,.0f}: white {r.white:,.0f}, Black {r.black:,.0f}, Hispanic {r.hisp:,.0f}, "
            f"AIAN {r.aian:,.0f}, Asian {r.asian:,.0f}, nonresident {r.nonres:,.0f}")
    return tiers


def digest_ramp(log):
    """Mean over entry cohorts of URM enrollment share relative to 2023 (NCES Digest 2024 Table 306.10)."""
    t = pd.read_html(CACHE / "dt_306_10_d24.html")[2]
    labels = t.iloc[:, 0].astype(str)
    years = [1976, 1980, 1990, 2000, 2013, 2018, 2019, 2020, 2021, 2022, 2023]
    if labels.iloc[6] != "Black" or labels.iloc[7] != "Hispanic":
        raise SystemExit(f"[BLOCKED] Digest layout changed: {labels.iloc[6]}, {labels.iloc[7]}")
    shares = {g: t.iloc[i, 12:23].astype(float).to_numpy() for g, i in [("black", 6), ("hisp", 7)]}
    log("NCES Digest 2024 Table 306.10, % of resident enrollment: "
        + "; ".join(f"{g} " + ", ".join(f"{y}:{v:.1f}" for y, v in zip(years, s)) for g, s in shares.items()))

    def ramp(g, stock_year):
        entry = np.arange(stock_year - 43, stock_year - 3)  # ages 22-61 in stock year, entered at 18
        return float(np.mean(np.interp(entry, years, shares[g]) / shares[g][-1])), entry

    out = {}
    for yr in (2022, 2024):
        for g in ("black", "hisp"):
            out[(yr, g)], entry = ramp(g, yr)
        log(f"  stock {yr}: entry cohorts {entry[0]}-{entry[-1]}; mean share relative to 2023: "
            f"Black {out[(yr, 'black')]:.3f}, Hispanic {out[(yr, 'hisp')]:.3f}")
    return out


def cps(log):
    cols = ["A_AGE", "PRCITSHP", "PEHSPNON", "PRDTRACE", "PRDTHSP", "MARSUPWT", "PEARNVAL", "A_HGA",
            "A_CLSWKR", "FEDTAX_AC", "FICA", "STATETAX_A", "PEFNTVTY", "PEMNTVTY"]
    with zipfile.ZipFile(ASEC) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=cols)
    w = d.MARSUPWT / 100
    nhw = d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)
    native = d.PRCITSHP.isin([1, 2, 3])
    hisp = d.PEHSPNON.eq(1)
    mex = d.PRDTHSP.eq(1)
    earner = d.PEARNVAL > 0
    ba = d.A_HGA >= 43
    age = d.A_AGE
    inc_se = d.A_CLSWKR.eq(5)
    us_area = [57, 60, 66, 69, 73, 78]  # same parent-birthplace coding as disability_gen_2026_09_17
    gen12 = ~native | ~(d.PEFNTVTY.isin(us_area) & d.PEMNTVTY.isin(us_area))

    def wsum(mask, v=None):
        return float((w[mask] * (1 if v is None else v[mask])).sum())

    wn = nhw & native
    c = dict(
        n_wn_workers=wsum(wn & earner),
        n_all_workers=wsum(earner),
        e_wn_worker=wsum(wn & earner, d.PEARNVAL) / wsum(wn & earner),
        e_wn_ba=wsum(wn & earner & ba & age.between(25, 64), d.PEARNVAL)
        / wsum(wn & earner & ba & age.between(25, 64)),
        emp_wn_ba=wsum(wn & ba & age.between(22, 61) & earner) / wsum(wn & ba & age.between(22, 61)),
        nat_ba=wsum(wn & ba & age.between(22, 40)) / wsum(nhw & ba & age.between(22, 40)),
        nat_w=wsum(wn & earner) / wsum(nhw & earner),
        white_of_nonpref=wsum(nhw & earner)
        / wsum(earner & ~hisp & ~(d.PEHSPNON.eq(2) & d.PRDTRACE.eq(2))),
        mex_ba=wsum(hisp & mex & ba & age.between(22, 40)) / wsum(hisp & ba & age.between(22, 40)),
        mex_w=wsum(hisp & mex & earner) / wsum(hisp & earner),
        mex_se=wsum(hisp & mex & inc_se) / wsum(hisp & inc_se),
        g12_ba=wsum(hisp & gen12 & ba & age.between(22, 40)) / wsum(hisp & ba & age.between(22, 40)),
        g12_w=wsum(hisp & gen12 & earner) / wsum(hisp & earner),
        g12_se=wsum(hisp & gen12 & inc_se) / wsum(hisp & inc_se),
        se_wn=wsum(wn & inc_se & earner, d.PEARNVAL) / wsum(inc_se & earner, d.PEARNVAL),
    )
    tax = d.FEDTAX_AC.clip(lower=0) + d.FICA.clip(lower=0) + d.STATETAX_A.clip(lower=0)
    c["tax_wn"] = wsum(wn, tax) / wsum(pd.Series(True, index=d.index), tax)
    for k, lo, hi in [("n_wn_workers", 5e7, 1.5e8), ("n_all_workers", 1.2e8, 2.2e8),
                      ("e_wn_ba", 5e4, 2e5), ("nat_ba", 0.8, 1.0), ("mex_ba", 0.3, 0.8),
                      ("tax_wn", 0.4, 0.9), ("se_wn", 0.4, 0.95)]:
        if not lo <= c[k] <= hi:
            raise SystemExit(f"[BLOCKED] CPS gate {k}={c[k]} outside [{lo}, {hi}]")
    log("CPS ASEC 2025 (income year 2024), weights MARSUPWT/100:")
    log(f"  non-Hispanic white native workers (earnings>0): {c['n_wn_workers']/1e6:,.1f}m of "
        f"{c['n_all_workers']/1e6:,.1f}m; mean earnings ${c['e_wn_worker']:,.0f}")
    log(f"  NH-white-native BA+ aged 25-64 mean earnings ${c['e_wn_ba']:,.0f}; share with earnings, "
        f"ages 22-61: {c['emp_wn_ba']:.3f}; native share of NH-white BA+ 22-40: {c['nat_ba']:.3f}; "
        f"native share of NH-white workers: {c['nat_w']:.3f}; NH-white share of earners who are neither "
        f"Hispanic nor non-Hispanic Black: {c['white_of_nonpref']:.3f}")
    log(f"  Mexican share of Hispanics: BA+ aged 22-40 {c['mex_ba']:.3f}; workers {c['mex_w']:.3f}; "
        f"incorporated self-employed {c['mex_se']:.3f}")
    log(f"  foreign-born or foreign-born parent (generations 1-2) share of Hispanics: BA+ aged 22-40 "
        f"{c['g12_ba']:.3f}; workers {c['g12_w']:.3f}; incorporated self-employed {c['g12_se']:.3f}")
    log(f"  NH-white-native share of income+payroll+state income tax {c['tax_wn']:.3f}; of incorporated "
        f"self-employed earnings {c['se_wn']:.3f}")
    return c


def usaspending(log):
    def get(prefix, name, fy):
        j = json.loads((CACHE / "usaspending" / f"{prefix}_{name}_FY{fy}.json").read_text())
        return float(j["results"][0]["Contract_Obligations"])

    u = {}
    for fy in (2022, 2023, 2024):
        u[fy] = dict(all=get("sot", "ALL", fy), sdb=get("sot", "self_certified_small_disadvanted_business", fy),
                     p8a=get("sot", "8a_program_participant", fy),
                     minority=get("sot", "minority_owned_business", fy),
                     hisp=get("sot", "hispanic_american_owned_business", fy),
                     sa8a=get("sa8a", "ALL", fy), sa8a_hisp=get("sa8a", "hispanic_american_owned_business", fy))
    log("USAspending contract obligations ($bn; award types A-D; set-aside codes 8A+8AN for 8(a)-restricted):")
    for fy, v in u.items():
        log(f"  FY{fy}: all {v['all']/1e9:,.2f}; self-certified SDB {v['sdb']/1e9:,.2f}; 8(a) participants "
            f"{v['p8a']/1e9:,.2f}; minority-owned {v['minority']/1e9:,.2f}; Hispanic-owned {v['hisp']/1e9:,.2f}; "
            f"8(a)-restricted {v['sa8a']/1e9:,.2f} (Hispanic-owned {v['sa8a_hisp']/1e9:,.2f} = "
            f"{v['sa8a_hisp']/v['sa8a']:.1%})")
    return u


# ---------------------------------------------------------------------------------------------
def admissions(tiers, ramp, c, log):
    """Annual earnings loss of the working stock, and PV per entering cohort."""
    res = {}
    crossings = {}
    for i, lvl in enumerate(LCH):
        tot = {}
        for yr in (2022, 2024):
            tot[yr] = dict(black=0.0, hisp=0.0)
        pv_flow = dict(black=0.0, hisp=0.0)
        by_bound = {}
        # boundary E: URM seats lost in tier E; boundary S: URM seats lost from tiers E+S together
        bounds = [("E", tiers.loc[["E"]], RED_E, W_E, p("r_elite")[i],
                   p("elite_earn_2007") * CPI_2024 / CPI_2007),
                  ("S", tiers.loc[["E", "S", "B"] if lvl == "high" else ["E", "S"]], RED_S, W_S,
                   p("r_sel")[i], c["e_wn_ba"])]
        for name, t, redd, ws, r, earn in bounds:
            for g in ("black", "hisp"):
                urm = t[g].sum() + (t["aian"].sum() if g == "hisp" else 0.0)  # AIAN at Hispanic rates
                x = urm * redd[g][i] * ws[i] * c["nat_ba"]  # white-native up-crossings per cohort
                crossings[(lvl, name, g)] = x
                per_worker = c["emp_wn_ba"] * earn * r
                for yr in (2022, 2024):
                    tot[yr][g] += x * p("career_years") * ramp[(yr, g)] * per_worker
                by_bound[name] = by_bound.get(name, 0.0) + x * p("career_years") * ramp[(2024, g)] * per_worker
                years = np.arange(4, 4 + p("career_years"))
                pv_flow[g] += x * per_worker * float(np.sum((1 + p("discount")) ** -years))
        res[lvl] = dict(stock2022=tot[2022], stock2024=tot[2024], pv_flow=pv_flow, by_bound=by_bound,
                        per_worker={b[0]: c["emp_wn_ba"] * b[5] * b[4] for b in bounds})
    log("Admissions: white-native up-crossings per entering cohort (seats freed x white share x native share):")
    for lvl in LCH:
        log(f"  {lvl:7s} " + "; ".join(f"boundary {b} {g} {crossings[(lvl, b, g)]:,.0f}"
                                      for b in ("E", "S") for g in ("black", "hisp"))
            + f"; total {sum(v for k, v in crossings.items() if k[0] == lvl):,.0f}")
    for lvl in LCH:
        r = res[lvl]
        log(f"  {lvl:7s} 2024 stock cost by boundary: E ${r['by_bound']['E']/1e9:.2f}bn "
            f"(loss per affected worker-year ${r['per_worker']['E']:,.0f}), S ${r['by_bound']['S']/1e9:.2f}bn "
            f"(${r['per_worker']['S']:,.0f})")
    return res


def employment(c):
    out = {}
    for i, lvl in enumerate(LCH):
        displaced = c["n_all_workers"] * p("contractor_share") * p("shift_pp")[i] / 100
        cost = displaced * c["white_of_nonpref"] * c["nat_w"] * c["e_wn_worker"] * p("r_emp")[i]
        out[lvl] = dict(displaced=displaced * c["white_of_nonpref"] * c["nat_w"], cost=cost)
    return out


def contracting(u, c):
    out = {}
    for i, lvl in enumerate(LCH):
        m = p("margin")[i]
        row = {}
        for tag, fy, dbe_scale in (("pre2023", 2022, 1.0), ("y2024", 2024, p("dbe_2024_scale")[i])):
            a8 = u[fy]["sa8a"] if lvl != "high" else u[fy]["p8a"]
            profit_8a = a8 * p("share_shifted_8a")[i] * m * c["se_wn"]
            dbe = p("dbe_awards_fy2020") * dbe_scale
            profit_dbe = dbe * p("dbe_minority_share") * p("dbe_pref_caused")[i] * m * c["se_wn"]
            base = dbe / p("dbe_participation")
            prem_dbe = base * p("premium_dbe")[i] * p("dbe_minority_share") * c["tax_wn"]
            prem_8a = a8 * p("premium_8a")[i] * c["tax_wn"]
            row[tag] = dict(profit_8a=profit_8a, profit_dbe=profit_dbe, prem_dbe=prem_dbe, prem_8a=prem_8a,
                            hisp_8a=u[fy]["sa8a_hisp"] / u[fy]["sa8a"],
                            hisp_minority=u[fy]["hisp"] / u[fy]["minority"])
        out[lvl] = row
    return out


# ---------------------------------------------------------------------------------------------
def main():
    OUT.mkdir(exist_ok=True)
    lines = []
    log = lines.append
    log("AFFIRMATIVE ACTION COST TO NON-HISPANIC WHITE NATIVES - accounting scenarios")
    log("=" * 94)
    log("Derived published parameters:")
    log(f"  elite URM seat loss (E&C Table 2, AKR Harvard Table 11): Black {RED_E['black'][0]:.3f}-"
        f"{RED_E['black'][2]:.3f}, Hispanic {RED_E['hisp'][0]:.3f}-{RED_E['hisp'][2]:.3f}; white share of "
        f"freed seats {W_E[0]:.3f}-{W_E[2]:.3f}")
    log(f"  selective URM seat loss (Hinrichs Table 5, AKR UNC in-state): Black {RED_S['black'][0]:.3f}/"
        f"{RED_S['black'][1]:.3f}/{RED_S['black'][2]:.3f}, Hispanic {RED_S['hisp'][0]:.3f}/{RED_S['hisp'][1]:.3f}/"
        f"{RED_S['hisp'][2]:.3f}; white share of freed seats {W_S[0]:.3f}/{W_S[1]:.3f}/{W_S[2]:.3f}")
    tiers = ipeds_tiers(log)
    ramp = digest_ramp(log)
    c = cps(log)
    u = usaspending(log)
    adm = admissions(tiers, ramp, c, log)
    emp = employment(c)
    con = contracting(u, c)

    rows = []

    def add(channel, pre, y24, hisp, mex, grade, note):
        rows.append(dict(channel=channel, **{f"pre2023_{k}": pre[i] / 1e9 for i, k in enumerate(LCH)},
                         **{f"y2024_{k}": y24[i] / 1e9 for i, k in enumerate(LCH)},
                         hisp_share=hisp, mex_share=mex, grade=grade, note=note))

    # admissions
    pre = [sum(adm[l]["stock2022"].values()) for l in LCH]
    y24 = [sum(adm[l]["stock2024"].values()) for l in LCH]
    hs = adm["central"]["stock2024"]["hisp"] / sum(adm["central"]["stock2024"].values())
    add("1 Admissions, undergraduate (earnings of working stock)", pre, y24, hs, hs * c["mex_ba"], "C",
        "stock of pre-SFFA cohorts; 2024 flow of new displacement not measured")
    pv = [sum(adm[l]["pv_flow"].values()) for l in LCH]
    hs_pv = adm["central"]["pv_flow"]["hisp"] / sum(adm["central"]["pv_flow"].values())
    # employment
    e = [emp[l]["cost"] for l in LCH]
    add("2 Employment, federal contractors (EO 11246)", e, e, p("hisp_share_emp")[1],
        p("hisp_share_emp")[1] * c["mex_w"], "C-/D", "in force through Jan 2025")
    # contracting
    for key, label, grade in (("profit_8a", "3a Contracting, 8(a) lost profits", "C"),
                              ("profit_dbe", "3b Contracting, DOT DBE lost profits (minority part)", "C-"),
                              ("prem_dbe", "3c Contracting, DBE price premium (taxpayers)", "B-/C"),
                              ("prem_8a", "3d Contracting, 8(a) price premium (taxpayers)", "D")):
        pre = [con[l]["pre2023"][key] for l in LCH]
        y24 = [con[l]["y2024"][key] for l in LCH]
        hsh = con["central"]["y2024"]["hisp_8a"] if "8a" in key else con["central"]["y2024"]["hisp_minority"]
        add(label, pre, y24, hsh, hsh * c["mex_se"], grade,
            "8(a) presumption ended July 2023; FY2024 dollars rose" if "8a" in key else
            "DBE presumption ended Oct 2025; 2024 unchanged")
    tab = pd.DataFrame(rows)
    tot = tab[[c_ for c_ in tab.columns if c_.startswith(("pre2023_", "y2024_"))]].sum()
    hisp_bn = float((tab.y2024_central * tab.hisp_share).sum())
    mex_bn = float((tab.y2024_central * tab.mex_share).sum())
    tab.to_csv(OUT / "channels.csv", index=False, float_format="%.4f")

    log("")
    log("CHANNEL TABLE, $bn per year (pre-2023 = 2022 stock / FY2022 contracting; 2024 = 2024 stock / FY2024)")
    log(f"{'channel':58s} {'pre-2023 L/C/H':>22s} {'2024 L/C/H':>22s} {'Hisp':>6s} {'Mex':>6s} grade")
    for _, r in tab.iterrows():
        log(f"{r.channel:58s} {r.pre2023_low:6.2f}/{r.pre2023_central:6.2f}/{r.pre2023_high:6.2f}  "
            f"{r.y2024_low:6.2f}/{r.y2024_central:6.2f}/{r.y2024_high:6.2f} {r.hisp_share:6.1%} {r.mex_share:6.1%} {r.grade}")
    log(f"{'TOTAL priced channels':58s} {tot.pre2023_low:6.2f}/{tot.pre2023_central:6.2f}/{tot.pre2023_high:6.2f}  "
        f"{tot.y2024_low:6.2f}/{tot.y2024_central:6.2f}/{tot.y2024_high:6.2f}")
    career = tab[tab.channel.str.match(r"^(1|2|3a|3b) ")]
    taxp = tab[tab.channel.str.match(r"^(3c|3d) ")]
    for lab, sub in (("  career loss (rows 1, 2, 3a, 3b)", career), ("  taxpayer premium (rows 3c, 3d)", taxp)):
        log(f"{lab:58s} {sub.pre2023_low.sum():6.2f}/{sub.pre2023_central.sum():6.2f}/{sub.pre2023_high.sum():6.2f}  "
            f"{sub.y2024_low.sum():6.2f}/{sub.y2024_central.sum():6.2f}/{sub.y2024_high.sum():6.2f}")
    log(f"  of which Hispanic beneficiaries (2024 central): ${hisp_bn:.2f}bn ({hisp_bn/tot.y2024_central:.1%}); "
        f"Mexican-origin ${mex_bn:.2f}bn ({mex_bn/tot.y2024_central:.1%})")
    for i, lvl in enumerate(LCH):
        h_adm = adm[lvl]["stock2024"]["hisp"]
        h_emp = emp[lvl]["cost"] * p("hisp_share_emp")[i]
        y = con[lvl]["y2024"]
        h_con = (y["profit_8a"] + y["prem_8a"]) * y["hisp_8a"] + (y["profit_dbe"] + y["prem_dbe"]) * y["hisp_minority"]
        h = h_adm + h_emp + h_con
        mx = h_adm * c["mex_ba"] + h_emp * c["mex_w"] + h_con * c["mex_se"]
        g12 = h_adm * c["g12_ba"] + h_emp * c["g12_w"] + h_con * c["g12_se"]
        log(f"  2024 {lvl:7s}: Hispanic ${h/1e9:.2f}bn (admissions {h_adm/1e9:.2f}, employment {h_emp/1e9:.2f}, "
            f"contracting {h_con/1e9:.2f}); Mexican-origin ${mx/1e9:.2f}bn; generations 1-2 ${g12/1e9:.2f}bn")
    per_worker = {k: tot[f"y2024_{k}"] * 1e9 / c["n_wn_workers"] for k in LCH}
    log(f"  per NH-white-native worker, 2024: ${per_worker['low']:,.0f} / ${per_worker['central']:,.0f} / "
        f"${per_worker['high']:,.0f}; central as share of their mean earnings "
        f"{per_worker['central']/c['e_wn_worker']:.3%}")
    log("")
    log(f"Admissions flow: PV (3% real) of lifetime losses per entering cohort, pre-SFFA: "
        f"${pv[0]/1e9:.2f}bn / ${pv[1]/1e9:.2f}bn / ${pv[2]/1e9:.2f}bn; Hispanic share {hs_pv:.1%}")
    log(f"Employment: white-native workers displaced from contractor jobs {emp['low']['displaced']:,.0f} / "
        f"{emp['central']['displaced']:,.0f} / {emp['high']['displaced']:,.0f}")
    log("")
    log("Parameter notes:")
    for k, (v, note) in PARAMS.items():
        log(f"  {k} = {v}: {note}")
    (OUT / "calc_output.txt").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
