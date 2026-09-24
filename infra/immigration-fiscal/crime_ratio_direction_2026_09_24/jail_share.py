"""Arm 4, tasks 4 and 6: corrected Hispanic share of local-jail inmates, midyear 2023.

BJS *Jail Inmates in 2023* Table 5 records 95,700 Hispanic of 664,200 (14.41%). The ASJ asks each jail
for counts in one combined race/Hispanic item, drops "not known"/"other" and scales the known
distribution up, and applies no self-report adjustment (unlike prisons, which BJS adjusts with SPI).
This script estimates the share by several methods and writes derived/jail_share_estimates.csv:

  survey_or_*          BJS's own self-report surveys of jail inmates (SILJ 1989/1996/2002, NIS-2 2008-09,
                       NIS-3 2011-12) against the ASJ count of the same year; the odds ratio is applied
                       to the 2023 ASJ share (the logic BJS uses for prisons with SPI 2016)
  prison_adjustment_*  BJS's 2023 prison adjustment (adjusted Table 3 vs administrative appendix table 1)
                       transferred to jails
  census2010_*         2010 census local-jail counts (SF1 PCT20H) against ASJ midyear 2010, nationally and
                       state by state on the 2019 Census of Jails weights
  acs_residual_*       ACS adult correctional facilities (S2603) less BJS prisons, by universe variant
  arrest_share_*       FBI Table 43C adult Hispanic arrest share (the audit's bound)
  benchmark_*          reference points that are not estimates (state-composition parity)

It also writes derived/jail_acs_record_ratio.csv: f = recorded / self-identified Hispanic share of
correctional residents, for the ACS (by jail share and universe variant) and for the 2010 census prisons.

Every input is read from a saved primary file and gated against the number quoted in ARM4_RESULT.md.
Run from the repository root after jail_acs_gq.py and jail_census_gq.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/jail_share.py
"""
import csv, io, json, pathlib, re, sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
C = HERE / "_cache/jail"
DERIVED = HERE / "derived"
P23 = ROOT / ".scratch/clarity-next-20260905/conduct-race/p23st.txt"   # Prisoners in 2023 text (held copy)
ARRESTS = FISCAL / "nibrs_arrests_2026_09_16/arrests_by_ethnicity_2023.csv"
ROWS = []


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def odds(p: float) -> float:
    return p / (1 - p)


def share(o: float) -> float:
    return o / (1 + o)


def add(method: str, kind: str, s: float, source: str, note: str) -> None:
    ROWS.append({"method": method, "kind": kind, "jail_H_share": s, "source": source, "note": note})


def row_numbers(path: pathlib.Path, pattern: str) -> list:
    txt = path.read_text(errors="ignore")
    m = re.search(pattern, txt, re.M)
    if not m:
        sys.exit(f"[BLOCKED] pattern not found in {path.name}: {pattern}")
    return [float(x.replace(",", "")) for x in re.findall(r"\d[\d,]*\.?\d*", m.group(0))]


# ------------------------------------------------------------------ BJS 2023 jail count
def bjs_2023() -> float:
    raw = (C / "ji23st_csv/ji23stt05.csv").read_bytes().decode("latin-1")
    row = next(csv.reader([next(l for l in raw.splitlines() if l.startswith("2023"))]))
    tot, h = int(row[1].replace(",", "")), int(row[7].replace(",", ""))
    gate("Jail Inmates in 2023 Table 5: 95,700 Hispanic of 664,200", (tot, h) == (664_200, 95_700), f"{h / tot:.5f}")
    return h / tot


# ------------------------------------------------------------------ self-report surveys vs ASJ
def surveys(j23: float) -> None:
    pairs = []
    # SILJ 2002 and 1996 (Profile of Jail Inmates 2002, Table 1: 2002 total ... 1996 total)
    n = row_numbers(C / "pji02.txt", r"^\s+Hispanic\s+18\.5\s+18\.5\s+19\.6\s+16\.6\s+18\.5\s*$")
    silj02, silj96 = n[0] / 100, n[4] / 100
    # SILJ 1989 (Profile of Jail Inmates 1989, Table 3: convicted, unconvicted, total 1989, total 1983)
    n = row_numbers(C / "pji89.txt", r"^\s+Hispanic\s+17\.5\s+16\.7\s+17\.4\s+14,3\s*$")
    silj89 = n[2] / 100
    # ASJ 1995, 2000, 2001, 2002 (Prison and Jail Inmates at Midyear 2002, Table 10)
    n = row_numbers(C / "pjim02.txt", r"Hispanic\s+14\.7\s+15\.1\s+14\.7\s+14\.7")
    asj02 = n[3] / 100
    # ASJ 1990-1996 (Prison and Jail Inmates at Midyear 1996, Table 7)
    n = row_numbers(C / "pjimy96.txt", r"Hispanic\s+--\s+14\.3\s+14\.2\s+14\.5\s+15\.1\s+15\.4\s+14\.7\s+15\.6")
    asj90, asj96 = n[0] / 100, n[6] / 100
    # ASJ midyear 2008 (Jail Inmates at Midyear 2010, Table 6) and 2011 (Jail Inmates at Midyear 2011, Table 6)
    h = row_numbers(C / "jim10st.txt", r"Hispanic/Latino\s+94,100\s+111,900\s+119,200\s+125,500\s+128,500\s+124,000\s+118,100")
    t = row_numbers(C / "jim10st.txt", r"^\s+Total\s+621,149\s+747,529\s+765,819\s+780,174\s+785,533\s+767,434\s+748,728")
    asj08, asj10 = h[4] / t[4], h[6] / t[6]
    h11 = row_numbers(C / "jim11st.txt", r"Hispanic/Latino\s+94,100\s+111,900\s+119,200\s+125,500\s+128,500\s+124,000\s+118,100\s+113,900")[7]
    m11 = row_numbers(C / "jim11st.txt", r"^\s+Male\s+550,162\s+652,958\s+666,819\s+679,654\s+685,862\s+673,728\s+656,360\s+642,300")[7]
    f11 = row_numbers(C / "jim11st.txt", r"^\s+Female\s+70,987\s+94,571\s+99,000\s+100,520\s+99,670\s+93,706\s+92,368\s+93,300")[7]
    asj11 = h11 / (m11 + f11)
    # NIS-2 (2008-09) and NIS-3 (2011-12) jail inmates by race/Hispanic origin (weighted counts, 18+)
    nis2 = row_numbers(C / "svpjri0809.txt", r"Hispanic\s+304,400\s+1\.4\s+2\.4\*\*\s+158,500")[3]
    nis2_tot = sum([271_900, 279_000, 158_500, 17_300, 43_000])
    for lab, v in (("White", 271_900), ("Black", 279_000), ("Other", 17_300)):
        gate(f"NIS-2 jail {lab} count present", str(f"{v:,}") in (C / "svpjri0809.txt").read_text(errors="ignore"), f"{v:,}")
    nis3 = row_numbers(C / "svpjri1112.txt", r"Hispanic\s+339,800\s+1\.6\s+2\.2\s+159,300")[3]
    nis3_tot = sum([240_500, 239_200, 159_300, 18_900, 54_300])
    for lab, v in (("White", 240_500), ("Black", 239_200), ("Two or more", 54_300)):
        gate(f"NIS-3 jail {lab} count present", str(f"{v:,}") in (C / "svpjri1112.txt").read_text(errors="ignore"), f"{v:,}")
    gate("survey and ASJ inputs parsed", tuple(round(x, 4) for x in (silj02, silj96, silj89, asj02, asj90, asj96, nis2, nis3)) ==
         (0.185, 0.185, 0.174, 0.147, 0.143, 0.156, 158_500, 159_300),
         f"SILJ 89/96/02 {silj89}/{silj96}/{silj02}; ASJ 90/96/02 {asj90}/{asj96}/{asj02}; "
         f"ASJ 2008 {asj08:.4f}, 2010 {asj10:.4f}, 2011 {asj11:.4f}")
    pairs = [
        ("survey_or_silj1989", silj89, asj90, "SILJ 1989 (pji89 Table 3) vs ASJ 1990 (pjimy96 Table 7); 1989 ASJ not in hand"),
        ("survey_or_silj1996", silj96, asj96, "SILJ 1996 (pji02 Table 1) vs ASJ midyear 1996 (pjimy96 Table 7, all persons under jail supervision)"),
        ("survey_or_silj2002", silj02, asj02, "SILJ 2002 (pji02 Table 1) vs ASJ midyear 2002 (pjim02 Table 10)"),
        ("survey_or_nis2_2008", nis2 / nis2_tot, asj08, "NIS-2 2008-09 jail inmates 18+ (svpjri0809 Table 6) vs ASJ midyear 2008 (jim10st Table 6)"),
        ("survey_or_nis3_2011", nis3 / nis3_tot, asj11, "NIS-3 2011-12 jail inmates 18+ (svpjri1112 Table 7) vs ASJ midyear 2011 (jim11st Table 6)"),
    ]
    ors = {}
    print("\n[self-report surveys vs ASJ]")
    for m, s_self, s_adm, src in pairs:
        o = odds(s_self) / odds(s_adm)
        ors[m] = o
        est = share(odds(j23) * o)
        print(f"  {m:22s} self {s_self:.4f} admin {s_adm:.4f} gap {100 * (s_self - s_adm):+.1f}pp  OR {o:.3f} -> 2023 {est:.4f}")
        add(m, "estimate", est, src, f"self {s_self:.4f} vs admin {s_adm:.4f}; odds ratio {o:.3f} applied to the 2023 ASJ odds")
    post = [ors[k] for k in ("survey_or_silj2002", "survey_or_nis2_2008", "survey_or_nis3_2011")]
    mean_or = sum(post) / len(post)
    add("survey_or_mean_post2000", "central", share(odds(j23) * mean_or),
        "mean odds ratio of SILJ 2002, NIS-2, NIS-3", f"mean OR {mean_or:.3f}")
    # NIS-3 house effect: its prison Hispanic share against BJS's SPI-adjusted 2013 prison share (Table 3)
    nis3_prison = 339_800 / sum([430_000, 507_900, 339_800, 38_200, 108_300])
    adj13 = 343_100 / 1_520_403
    gate("NIS-3 prison Hispanic count and BJS 2013 adjusted Hispanic count present",
         "339,800" in (C / "svpjri1112.txt").read_text(errors="ignore") and "343,100" in P23.read_text(errors="ignore"),
         f"NIS-3 prisons {nis3_prison:.4f}; BJS adjusted 2013 {adj13:.4f}")
    house = odds(nis3_prison) / odds(adj13)
    add("survey_or_nis3_less_prison_house_effect", "estimate", share(odds(j23) * ors["survey_or_nis3_2011"] / house),
        "NIS-3 jail OR divided by NIS-3's prison excess over BJS adjusted 2013",
        f"NIS-3 prisons {nis3_prison:.4f} vs BJS adjusted 2013 {adj13:.4f}: house OR {house:.3f}")
    return {"asj10": asj10, "ors": ors, "mean_or": mean_or, "house": house}


# ------------------------------------------------------------------ prisons: adjusted vs administrative, 2023
def prison_adjustment(j23: float) -> None:
    txt = P23.read_text(errors="ignore")
    block = txt[txt.index("APPENDIX TABLE 1\n"):]
    block = block[:block.index("Note: Jurisdiction refers")]
    tot = hisp = n = 0
    reported = []
    for line in block.splitlines():
        tok = line.split()
        if len(tok) < 12 or not re.match(r"^[\d,]+$", tok[-11]):
            continue
        vals = tok[-11:]
        name = " ".join(tok[:-11])
        t = int(vals[0].replace(",", ""))
        h = vals[3]
        hv = int(h.replace(",", "")) if re.match(r"^[\d,]+$", h) else 0
        tot += t
        hisp += hv
        n += 1
        reported.append((name, t, hv, h))
    gate("appendix table 1 parsed: federal + 50 states", n == 51 and tot == 1_254_224,
         f"{n} rows, total {tot:,}, Hispanic {hisp:,}")
    admin = hisp / tot
    adjusted = 282_700 / 1_210_308
    o = odds(adjusted) / odds(admin)
    print(f"\n[prisons 2023] administrative Hispanic {admin:.4f} (PA not reported, AL 0) vs adjusted {adjusted:.4f}: OR {o:.3f}")
    add("prison_adjustment_transfer_2023", "estimate", share(odds(j23) * o),
        "Prisoners in 2023 appendix table 1 (administrative) vs Table 3 (SPI-adjusted)",
        f"prison admin {admin:.4f} vs adjusted {adjusted:.4f}; OR {o:.3f} applied to jails [INFERENCE: same recording gap]")
    return admin


# ------------------------------------------------------------------ 2010 census, national and by state
def census2010(j23: float, asj10: float) -> None:
    c = pd.read_csv(DERIVED / "jail_census_gq.csv", dtype={"geo": str})
    us = c[(c.level == "us") & (c.type == "local_jails")].iloc[0]
    s10 = us.hispanic / us.total
    gate("census 2010 local jails 117,690 of 682,043", (us.hispanic, us.total) == (117_690, 682_043), f"{s10:.4f}")
    o = odds(s10) / odds(asj10)
    add("census2010_national_or", "estimate", share(odds(j23) * o),
        "2010 SF1 PCT20H local jails (Apr 1) vs ASJ midyear 2010 (jim10st)",
        f"census {s10:.4f} vs ASJ {asj10:.4f}; OR {o:.3f}; census counts are largely facility records, so a floor")
    add("census2010_hispanic_count_on_bjs_total", "estimate", share(odds(j23) * odds(us.hispanic / 748_728) / odds(asj10)),
        "census 2010 Hispanic jail count over the BJS midyear 2010 total",
        "puts the census's 117,690 Hispanic inmates on BJS's 748,728 total (the census jail universe is 9% smaller)")
    # state by state on the 2019 Census of Jails weights
    raw = (C / "cj0519st_csv/cj0519stt07.csv").read_bytes().decode("latin-1")
    rows = list(csv.reader(io.StringIO(raw)))
    coj = {}
    for r in rows:
        if len(r) > 8 and r[0] == "" and r[1] and r[1] != "U.S. total" and re.match(r"^[\d,]+$", r[2] or ""):
            coj[r[1].strip()] = (int(r[2].replace(",", "")), float(r[7]) / 100 if r[7] not in ("^", "") else 0.0)
    gate("COJ 2019 Table 7 parsed: 44 states + DC + Alaska's 15 jails", len(coj) == 46
         and coj["Arizona"] == (13_540, 0.204) and coj["Texas"] == (68_770, 0.311),
         f"{len(coj)} rows; national {sum(n * s for n, s in coj.values()) / sum(n for n, _ in coj.values()):.4f}")
    ad = pd.read_csv(DERIVED / "jail_acs_adults.csv", dtype={"geo": str})
    h10 = ad[(ad["product"] == "acs1") & (ad.year == 2010)].set_index("geo").adult_hisp_share
    h19 = ad[(ad["product"] == "acs5") & (ad.year == 2019)].set_index("geo").adult_hisp_share
    st = c[(c.level == "state") & (c.type == "local_jails")].set_index("name")
    num_raw = num_adj = num_coj = num_par = den = 0.0
    detail = []
    for name, (n19, s_coj) in coj.items():
        r = st.loc[name]
        geo = r.geo
        c10 = r.hispanic / r.total if r.total > 0 else s_coj
        adj = share(odds(c10) * odds(h19[geo]) / odds(h10[geo])) if 0 < c10 < 1 else c10
        num_raw += n19 * c10
        num_adj += n19 * adj
        num_coj += n19 * s_coj
        num_par += n19 * h19[geo]
        den += n19
        detail.append({"state": name, "coj2019_jail_inmates": n19, "coj2019_hisp": s_coj, "census2010_local_jail_hisp": c10,
                       "census2010_local_jail_n": r.total, "adult_hisp_2010": h10[geo], "adult_hisp_2015_19": h19[geo],
                       "census2010_growth_adjusted_2019": adj})
    coj_nat, raw_nat, adj_nat, par_nat = num_coj / den, num_raw / den, num_adj / den, num_par / den
    # Table 7's state rows rebuild 14.78%, its regional rows 14.6%: the South's states give 9.7% against a
    # published 9.3% (Mississippi's 11.8% alone is +0.35 pp of the South). Comparisons below use the state rows
    # on both sides, so the ratio is internally consistent. [DATA: cj0519stt07.csv]
    gate("COJ 2019 state rows rebuild the national 14.6% within 0.25 pp", abs(coj_nat - 0.146) < 0.0025, f"{coj_nat:.4f}")
    print(f"\n[2019 jail weights] COJ {coj_nat:.4f}; census-2010 coding {raw_nat:.4f}; growth-adjusted {adj_nat:.4f}; "
          f"adult parity {par_nat:.4f}")
    add("census2010_state_coding_on_coj2019_weights", "estimate", share(odds(j23) * odds(raw_nat) / odds(coj_nat)),
        "state 2010 census local-jail shares weighted by COJ 2019 state jail counts, vs COJ 2019",
        f"census-coded {raw_nat:.4f} vs COJ {coj_nat:.4f} (2019 weights, no growth adjustment)")
    add("census2010_state_coding_growth_adjusted", "estimate", share(odds(j23) * odds(adj_nat) / odds(coj_nat)),
        "as above, each state's census share moved by its 2010-2015/19 change in adult Hispanic odds",
        f"growth-adjusted {adj_nat:.4f} vs COJ {coj_nat:.4f}")
    add("benchmark_state_parity_2019", "benchmark", par_nat,
        "COJ 2019 state jail counts x ACS 2015-19 adult Hispanic share (jails at each state's adult share)",
        "not an estimate: the national jail share if each state's jails held Hispanics at their adult share")
    pd.DataFrame(detail).to_csv(DERIVED / "jail_state_comparison_2019.csv", index=False, lineterminator="\n",
                                float_format="%.5f")
    return {"coj_nat": coj_nat, "raw_nat": raw_nat, "adj_nat": adj_nat, "par_nat": par_nat}


# ------------------------------------------------------------------ ACS residual
def acs_residual(j23: float, prison_admin: float) -> dict:
    a = pd.read_csv(DERIVED / "jail_acs_gq.csv", dtype={"geo": str})
    acs = {(r["product"], r.year): r for _, r in a[(a.table == "S2603") & (a.geo == "us")].iterrows()}
    p_jur, held, home = 1_254_224, 65_552, 5_371
    txt = P23.read_text(errors="ignore")
    gate("Prisoners in 2023: jurisdiction 1,254,224, held in jails 65,552, federal home confinement 5,371",
         "1,254,224" in txt and "65,552" in txt and "(5,371)" in txt, "found")
    P = p_jur - held - home                    # physically in prisons (incl. private and federal RRC)
    hP = 282_700 / 1_210_308                   # SPI-adjusted sentenced share applied to all prisoners
    J = 664_200
    # correctional GQ residents outside NPS custody and the ASJ: ICE and USMS detainees in dedicated or
    # contract detention (census type 101 beyond BOP), halfway houses outside NPS. [ASSUMPTION, bounded]
    D_lo, D_c, D_hi, hD_lo, hD_c, hD_hi = 30_000, 50_000, 70_000, 0.45, 0.60, 0.75
    R, hR = 50_000, 0.15
    for (prod, yr), lab in ((("acs1", 2023), "2023"), (("acs1", 2024), "2024_on_bjs2023"), (("acs5", 2023), "5yr_2019_23")):
        r = acs[(prod, yr)]
        s, moe = r.pct_hispanic / 100, r.pct_hispanic_moe / 100
        for var, extra, hx in (("bjs_universe", 0, 0.0), ("with_federal_detention", D_c + R, hD_c * D_c + hR * R)):
            U = P + J + extra
            est = (s * U - hP * P - hx) / J
            lo = ((s - moe) * U - hP * P - hx) / J
            hi = ((s + moe) * U - hP * P - hx) / J
            add(f"acs_residual_{lab}_{var}", "disconfirmation", est,
                f"ACS {prod} {yr} S2603 adult correctional Hispanic {s:.3f} (MOE {moe:.3f}) less BJS prisons",
                f"ACS share on universe {U:,.0f}; prisons {P:,.0f} at {hP:.4f}"
                + (f"; + {D_c:,} federal/ICE detainees at {hD_c:.0%} and {R:,} residential at {hR:.0%}" if extra else "")
                + f"; ACS MOE range {lo:.4f}-{hi:.4f}; assumes ACS records Hispanic origin without the admin gap")
    # prisons' own race recording: if the ACS codes prison residents as the NPS administrative records do
    # (appendix table 1, 17.86%) rather than at the SPI-adjusted 23.36%, the same arithmetic gives the jail
    # share the ACS implies on that coding. Reported as a sensitivity of the method, not an estimate.
    for (prod, yr), lab in ((("acs1", 2023), "2023"), (("acs5", 2023), "5yr_2019_23")):
        s = acs[(prod, yr)].pct_hispanic / 100
        for var, extra, hx in (("bjs_universe", 0, 0.0), ("with_federal_detention", D_c + R, hD_c * D_c + hR * R)):
            U = P + J + extra
            add(f"acs_residual_{lab}_{var}_prisons_admin_coded", "acs_prison_coding", (s * U - prison_admin * P - hx) / J,
                f"ACS {prod} {yr} S2603 Hispanic {s:.3f} less prisons at the NPS administrative share {prison_admin:.4f}",
                "sensitivity of the ACS residual to how the ACS records prison residents; not an estimate")
    # universe bounds around the 2023 with-federal-detention variant
    r = acs[("acs1", 2023)]
    s = r.pct_hispanic / 100
    ests = []
    for D, hD in ((D_lo, hD_lo), (D_hi, hD_hi), (D_lo, hD_hi), (D_hi, hD_lo)):
        U = P + J + D + R
        ests.append((s * U - hP * P - hD * D - hR * R) / J)
    print(f"\n[ACS residual 2023] universe-bound range {min(ests):.4f}-{max(ests):.4f}")
    # what the survey central implies for ACS coding: the ACS/true ratio f at a given jail share
    return {"P": P, "hP": hP, "J": J, "D": D_c, "hD": hD_c, "R": R, "hR": hR, "acs23": s, "univ_range": (min(ests), max(ests)),
            "hP_admin": prison_admin, "j23": j23}


def acs_record_ratio(ac: dict, out: pd.DataFrame) -> pd.DataFrame:
    """f = recorded / self-identified Hispanic share of correctional residents, for the ACS and the 2010 census.

    ACS rows: f = ACS S2603 share / T, with T the share implied by BJS's SPI-adjusted prisons, a jail share and
    the universe variant. Census row: 2010 SF1 state + federal prisons against BJS's self-report-adjusted
    yearend 2010 sentenced prisoners (Prisoners in 2010, Appendix Table 12)."""
    est = out.set_index("method").jail_H_share
    surveys = out[out.method.str.startswith("survey_or_")].set_index("method").jail_H_share
    jails = {"bjs_published_2023": est["bjs_published_2023"], "survey_min": surveys.min(),
             "survey_or_mean_post2000": est["survey_or_mean_post2000"], "survey_max": surveys.max()}
    univ = {"bjs_universe": (0, 0.0, 0, 0.0), "fed_detention_central": (ac["D"], ac["hD"], ac["R"], ac["hR"]),
            "fed_detention_low": (30_000, 0.45, ac["R"], ac["hR"]), "fed_detention_high": (70_000, 0.75, ac["R"], ac["hR"])}
    a = pd.read_csv(DERIVED / "jail_acs_gq.csv", dtype={"geo": str})
    acs = {(r["product"], r.year): r.pct_hispanic / 100 for _, r in a[(a.table == "S2603") & (a.geo == "us")].iterrows()}
    rows = []
    for (prod, yr) in (("acs1", 2023), ("acs5", 2023)):
        s = acs[(prod, yr)]
        for jn, jc in jails.items():
            for un, (D, hD, R, hR) in univ.items():
                T = (ac["hP"] * ac["P"] + jc * ac["J"] + hD * D + hR * R) / (ac["P"] + ac["J"] + D + R)
                rows.append({"instrument": f"ACS {prod} {yr} S2603 adult correctional", "jail_method": jn, "jail_H_share": jc,
                             "universe": un, "recorded_share": s, "self_id_share": T, "record_ratio_f": s / T})
    p10 = (C / "p10.txt").read_text(errors="ignore")
    m = re.search(r"\n2010c\s+([\d,]+)\s+[\d,]+\s+[\d,]+\s+([\d,]+)\s+([\d,]+)\s+[\d,]+\s+[\d,]+\s+([\d,]+)", p10)
    vals = tuple(int(x.replace(",", "")) for x in m.groups()) if m else None
    gate("Prisoners in 2010 App. Table 12, 2010: men 1,446,000 (Hispanic 327,200), women 104,600 (18,700)",
         vals == (1_446_000, 327_200, 104_600, 18_700), f"{vals}")
    bjs10 = (vals[1] + vals[3]) / (vals[0] + vals[2])
    c = pd.read_csv(DERIVED / "jail_census_gq.csv", dtype={"geo": str})
    us = c[c.level == "us"].set_index("type")
    cen10 = us.loc[["state_prisons", "federal_prisons"], "hispanic"].sum() / us.loc[["state_prisons", "federal_prisons"], "total"].sum()
    gate("census 2010 state+federal prisons 252,092 of 1,420,187",
         us.loc[["state_prisons", "federal_prisons"], "hispanic"].sum() == 252_092, f"{cen10:.4f} vs BJS adjusted {bjs10:.4f}")
    rows.append({"instrument": "Census 2010 SF1 PCT20H state+federal prisons", "jail_method": "", "jail_H_share": float("nan"),
                 "universe": "prisons only; BJS sentenced yearend 2010 (SISFCF/NIS-adjusted)", "recorded_share": cen10,
                 "self_id_share": bjs10, "record_ratio_f": cen10 / bjs10})
    # reference: the share a purely administrative coding would show (prisons at the NPS appendix share, jails at
    # the ASJ share, detention and residential as assumed) against the self-identified composition at the central
    U = ac["P"] + ac["J"] + ac["D"] + ac["R"]
    t_admin = (ac["hP_admin"] * ac["P"] + ac["j23"] * ac["J"] + ac["hD"] * ac["D"] + ac["hR"] * ac["R"]) / U
    t_self = (ac["hP"] * ac["P"] + jails["survey_or_mean_post2000"] * ac["J"] + ac["hD"] * ac["D"] + ac["hR"] * ac["R"]) / U
    rows.append({"instrument": "reference: all components administratively coded (NPS appendix, ASJ)",
                 "jail_method": "survey_or_mean_post2000", "jail_H_share": jails["survey_or_mean_post2000"],
                 "universe": "fed_detention_central", "recorded_share": t_admin, "self_id_share": t_self,
                 "record_ratio_f": t_admin / t_self})
    df = pd.DataFrame(rows)
    df.to_csv(DERIVED / "jail_acs_record_ratio.csv", index=False, lineterminator="\n", float_format="%.6f")
    return df


def main() -> None:
    print("[inputs]")
    j23 = bjs_2023()
    add("bjs_published_2023", "published", j23, "BJS Jail Inmates in 2023, Table 5", "administrative, no self-report adjustment")
    sv = surveys(j23)
    admin = prison_adjustment(j23)
    st = census2010(j23, sv["asj10"])
    ac = acs_residual(j23, admin)
    arr = pd.read_csv(ARRESTS, dtype=str)
    for yr in ("2023", "2024"):
        r = arr[(arr.year == yr) & (arr.offence == "ALL_OFFENCES")].iloc[0]
        s = float(r.eth_panel_hispanic) / float(r.eth_panel_total)
        add(f"arrest_share_fbi{yr}", "bound", s, f"FBI CIUS {yr} Table 43C adult ethnicity panel",
            "the audit's bound: jail stock at the adult arrest share")
    out = pd.DataFrame(ROWS)
    DERIVED.mkdir(exist_ok=True)
    out.to_csv(DERIVED / "jail_share_estimates.csv", index=False, lineterminator="\n", float_format="%.7f")
    # implied ACS under-recording factor at the survey central
    jc = out.set_index("method").loc["survey_or_mean_post2000", "jail_H_share"]
    U = ac["P"] + ac["J"] + ac["D"] + ac["R"]
    T = (ac["hP"] * ac["P"] + jc * ac["J"] + ac["hD"] * ac["D"] + ac["hR"] * ac["R"]) / U
    print(f"\n[ACS consistency] at the survey central {jc:.4f} the true correctional share is {T:.4f}; "
          f"ACS 2023 {ac['acs23']:.3f} would then record {ac['acs23'] / T:.3f} of Hispanic residents")
    json.dump({"acs_implied_record_ratio_at_survey_central": ac["acs23"] / T, "true_correctional_share_at_central": T,
               "acs_universe_bound_range_2023": ac["univ_range"], "state": st, "survey_mean_or": sv["mean_or"],
               "nis3_house_or": sv["house"]}, open(DERIVED / "jail_share_summary.json", "w"), indent=1)
    print("\n" + out[["method", "kind", "jail_H_share"]].to_string(index=False))
    rr = acs_record_ratio(ac, out)
    print("\n[recorded / self-identified Hispanic share of correctional residents, f]")
    print(rr[["instrument", "jail_method", "universe", "recorded_share", "self_id_share", "record_ratio_f"]].to_string(index=False))


if __name__ == "__main__":
    main()
