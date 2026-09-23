"""Use-weighted allocation of BEA public order and safety (Table 3.17 line 4) to the CPS Mexican-origin target.

The complete annual account charges line 4 ($519.153bn) per head: target share 0.120245 of the national
total, $62.425bn. This script splits line 4 into BEA's sublines, keys each subline by use, and reports the
change. Every use key is written as the target's share of a national use count:

    share = (target people in the relevant ages) x (use per person, Mexican-origin) / (national use)

Keys, with the per-head key kept as the reference:
  fire                    per head
  prisons                 ACS institutional residence 18-64 (raw, generic-Hispanic adjusted), BJS check
  police (non-border)     offending (FBI 2019 adult arrests), half offending / half per head,
                          victimization (NCVS 2022-2024 violent victimizations); NCVS perceived-offender
                          rate reported as a disconfirmation arm
  law courts              criminal share c by the arrest key, civil share per head, c in {0.5, 0.6, 0.75}
  ICE custody (in police) interior (ICE-arrest) bed-days by Mexico's share; border-arrest custody per head
  CBP (in police)         per head in every set: border spending follows entry flows, not resident use

Run from the repository root (after acs_pull.py):
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cj_use_allocation_2026_09_23/allocate.py
Outputs in derived/: cj_allocation.csv, key_sets.csv, key_inputs.csv, summary.json.
"""
import ast, csv, importlib.util, itertools, json, pathlib, re, subprocess, sys, zipfile

import openpyxl
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
DERIVED = HERE / "derived"
BEA = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
ALLOC = FISCAL / "full_account_spending_2026_09_20/derived/allocations.csv"
KEYS = FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv"
CASES = FISCAL / "full_account_2026_09_20/derived/service_response_summary.csv"
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CRIME = FISCAL / "crime_cost_2026_09_16/crime_cost.py"
NCVS = FISCAL / "ncvs_victim_offender_2026_09_18/derived/rates_by_victim_and_offender_2022_2024.csv"
BJS_PRISON = FISCAL / "acs_institutional_2026_09_16/bjs_p22st_extract.txt"
BJS_JAIL = HERE / "_cache/bjs/ji23stt05.csv"
DET = FISCAL / "detention_evidence_2026_09_20"
ICE_XLSX = DET / "_cache/ice_fy2024_yearend.xlsx"
ICE_PDF = DET / "_cache/ice_fy2024_annual.pdf"
ICE_OUTLAYS = DET / "actual_spending_fy2024_source.json"
OHSS = HERE / "_cache/ohss/ohss_monthly_tables_nov2024.xlsx"
FILE_A = FISCAL / "detention_reconciliation_2026_09_20/_cache/dhs_fy2024_fileab.zip"
ACS = DERIVED / "acs_hisp_nativity_gq.csv"
ACS19 = DERIVED / "acs2019_adults.csv"

RESIDENT = 340_110_988            # full resident control used by the complete account
ERO_ALL_VINTAGES = 5_262_842_692.98  # detention_reconciliation README: ICE ERO direct program activity, all funding years
CBO_BAND = ("cbo_category_lag_non_school_full", 165.12, 197.38)
COURT_CRIMINAL = {"low": 0.50, "central": 0.60, "high": 0.75}   # [ASSUMPTION] no source pins it; see RESULT.md

GATES = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append((name, ok, detail))
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def load_builder():
    spec = importlib.util.spec_from_file_location("spending_builder", FISCAL / "full_account_spending_2026_09_20/builder.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------- BEA sublines
def bea_cells(builder) -> dict:
    gate("BEA workbook is the pinned vintage", builder.sha(BEA) == builder.BEA_SHA, builder.BEA_SHA[:12])
    wb = openpyxl.load_workbook(BEA, read_only=True, data_only=True)

    def lines(sheet):
        rows = list(wb[sheet].iter_rows(values_only=True))
        col = list(rows[7]).index("2024")
        return {str(r[0]): (str(r[1]).strip(), r[col]) for r in rows if r[0] and str(r[0]).isdigit()}

    t16, t17, t155 = lines("T31600-A"), lines("T31700-A"), lines("T31505-A")
    want16 = {"8": "Public order and safety", "9": "Police", "10": "Fire", "11": "Law courts", "12": "Prisons"}
    for ln, lab in want16.items():
        gate(f"T3.16 line {ln} label", t16[ln][0] == lab, f"{t16[ln][0]} = {t16[ln][1]:,}")
    gate("T3.17 line 4 label", t17["4"][0] == "Public order and safety", f"{t17['4'][1]:,}")
    gate("T3.17 line 34 label", t17["34"][0] == "Public order and safety", f"social benefits {t17['34'][1]:,}")
    subs = {k: t16[n][1] for k, n in (("police", "9"), ("fire", "10"), ("law_courts", "11"), ("prisons", "12"))}
    gate("T3.16 sublines sum to T3.16 public order and safety", sum(subs.values()) == t16["8"][1],
         f"{sum(subs.values()):,} = {t16['8'][1]:,}")
    resid = t16["8"][1] - t17["4"][1] - t17["34"][1]
    gate("T3.16 total minus T3.17 line 4 is social benefits plus a small residual", abs(resid) < 100,
         f"{t16['8'][1]:,} - {t17['4'][1]:,} - {t17['34'][1]:,} = {resid:,} ($m)")
    gate("T3.15.5 POS = T3.17 consumption + gross investment", abs(t155["7"][1] - t17["4"][1] - t17["108"][1]) <= 1,
         f"{t155['7'][1]:,} vs {t17['4'][1]:,} + {t17['108'][1]:,}")
    line4 = t17["4"][1] / 1e3
    scale = t17["4"][1] / t16["8"][1]
    scaled = {k: v * scale / 1e3 for k, v in subs.items()}
    gate("scaled sublines sum to line 4", abs(sum(scaled.values()) - line4) < 1e-9, f"{sum(scaled.values()):.6f} bn")
    ci = {k: t155[n][1] for k, n in (("police", "8"), ("fire", "9"), ("law_courts", "10"), ("prisons", "11"))}
    return {"line4_bn": line4, "scale": scale, "t316_m": subs, "t316_total_m": t16["8"][1],
            "t3155_m": ci, "t3155_total_m": t155["7"][1], "scaled_bn": scaled,
            "social_benefits_m": t17["34"][1], "residual_m": resid}


# ---------------------------------------------------------------- reference and positive control
def reference(builder) -> dict:
    a = pd.read_csv(ALLOC)
    r = a[(a.scenario_id == "complete_preferred_F_per_capita") & (a.allocation == "personal")
          & (a.category == "public_order_safety")].iloc[0]
    k = pd.read_csv(KEYS)
    k = k[k.allocation == "personal"].set_index("key")
    pop = k.loc["population"]
    key_share = pop.target_key_total / pop.national_key_total
    pool = pop.national_key_total / RESIDENT
    target = 519.153 * pool * key_share
    gate("positive control: key share 0.121453", abs(key_share - 0.121453) < 5e-7 and abs(key_share - r.target_key_share) < 1e-12,
         f"{key_share:.6f}")
    gate("positive control: $62.425bn", abs(target - 62.425) < 5e-4 and abs(target - r.target_bn) < 1e-9, f"{target:.6f}")
    s = pd.read_csv(CASES).set_index("profile").loc[CBO_BAND[0]]
    gate("CBO-informed band is 165.12-197.38", abs(-s.max_welfare_bn - CBO_BAND[1]) < 0.01 and abs(-s.min_welfare_bn - CBO_BAND[2]) < 0.01,
         f"{-s.max_welfare_bn:.2f}-{-s.min_welfare_bn:.2f}")
    return {"target_bn": float(r.target_bn), "share_national": float(r.target_share_national), "key_share": float(key_share),
            "pool": float(pool), "target_pop": float(pop.target_key_total), "cps_pop": float(pop.national_key_total),
            "adults_target": float(k.loc["adults"].target_key_total), "adults_cps": float(k.loc["adults"].national_key_total),
            "band_low": -float(s.max_welfare_bn), "band_high": -float(s.min_welfare_bn)}


# ---------------------------------------------------------------- CPS target composition
def cps_target(builder) -> dict:
    gate("CPS ASEC 2025 archive is the pinned file", builder.sha(CPS_ZIP) == builder.CPS_SHA, builder.CPS_SHA[:12])
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP"]
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    civ, target = builder.canonical_target(d)
    wt = d.pwwgt0.to_numpy(float)
    total = float(wt[target].sum())
    gate("canonical target = 40,896,574.15", abs(total - 40_896_574.15235156) < 0.01, f"{total:,.2f}")
    mexborn = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy()
    age = d.A_AGE.to_numpy()
    out = {}
    for lab, m in (("mexico_born", target & mexborn), ("us_born", target & ~mexborn), ("cps_civilian", civ)):
        out[lab] = {"all": float(wt[m].sum()), "12up": float(wt[m & (age >= 12)].sum()),
                    "18_64": float(wt[m & (age >= 18) & (age <= 64)].sum()), "18up": float(wt[m & (age >= 18)].sum())}
    gate("target nativity parts add up", abs(out["mexico_born"]["all"] + out["us_born"]["all"] - total) < 0.01,
         f"Mexico-born {out['mexico_born']['all']:,.0f} + US-born {out['us_born']['all']:,.0f}")
    return out


# ---------------------------------------------------------------- ACS custody
def acs_custody(cps: dict) -> dict:
    a = pd.read_csv(ACS, dtype={"hisp": str, "ages": str})
    res = {}
    for product in ("acs1_2024", "acs5_2024"):
        g = a[(a["product"] == product) & (a.ages == "1864")]
        tot_all = a[(a["product"] == product) & (a.ages == "all")]["total"].sum()
        if product == "acs1_2024":
            gate("ACS 2024 all-age total equals the resident control", abs(tot_all / RESIDENT - 1) < 1e-4, f"{tot_all:,}")
        I_all = g.inst.sum()
        by = {}
        for nat in ("native", "foreign_born"):
            gn = g[g.nativity == nat]
            mex, gen = gn[gn.hisp == "02"].iloc[0], gn[gn.hisp == "24"].iloc[0]
            named = gn[~gn.hisp.isin(["01", "24"])]
            base = gn.inst.sum() / gn.total.sum()
            excess = max(0.0, gen.inst - base * gen.total)
            by[nat] = {"I_mex": float(mex.inst), "HH_mex": float(mex.hh), "P_mex": float(mex.total),
                       "I_hisp": float(gn[gn.hisp != "01"].inst.sum()), "P_hisp": float(gn[gn.hisp != "01"].total.sum()),
                       "I_gen": float(gen.inst), "P_gen": float(gen.total), "base": base, "excess": excess,
                       "mex_share_named_pop": float(mex.total / named.total.sum()),
                       "mex_share_named_inst": float(mex.inst / named.inst.sum())}
            by[nat]["I_mex_adj"] = by[nat]["I_mex"] + excess * by[nat]["mex_share_named_pop"]
            by[nat]["I_mex_adj_inst"] = by[nat]["I_mex"] + excess * by[nat]["mex_share_named_inst"]
        I_M = sum(v["I_mex"] for v in by.values())
        I_H = sum(v["I_hisp"] for v in by.values())
        P_M = sum(v["P_mex"] for v in by.values())
        P_H = sum(v["P_hisp"] for v in by.values())
        HH_M = sum(v["HH_mex"] for v in by.values())
        tmap = {"foreign_born": "mexico_born", "native": "us_born"}
        out = {"I_all": float(I_all), "I_mex": I_M, "I_hisp": I_H, "P_mex": P_M, "P_hisp": P_H, "HH_mex": HH_M, "by": by,
               "m_raw": I_M / I_H, "m_adj": sum(v["I_mex_adj"] for v in by.values()) / I_H,
               "m_adj_inst": sum(v["I_mex_adj_inst"] for v in by.values()) / I_H,
               "p_mex_of_hisp": P_M / P_H, "hisp_share_inst": I_H / I_all}
        for arm, col in (("raw", "I_mex"), ("adj", "I_mex_adj"), ("adj_inst", "I_mex_adj_inst")):
            parts = {tmap[n]: cps[tmap[n]]["18_64"] * by[n][col] / by[n]["HH_mex"] for n in by}
            out[f"custody_{arm}"] = {"count": sum(parts.values()), "share": sum(parts.values()) / I_all,
                                     "parts": {k: v / I_all for k, v in parts.items()}}
        res[product] = out
    return res


def ice_bound(acs: dict, cps: dict, ice: dict) -> dict:
    """Bound on the effect of ICE detainees inside ACS institutional counts (not a corrected rate)."""
    by = acs["acs1_2024"]["by"]
    fb = by["foreign_born"]
    i_fb = max(0.0, fb["I_mex_adj"] - ice["mex_detained"])
    parts = {"mexico_born": cps["mexico_born"]["18_64"] * i_fb / fb["HH_mex"],
             "us_born": cps["us_born"]["18_64"] * by["native"]["I_mex_adj"] / by["native"]["HH_mex"]}
    denom = acs["acs1_2024"]["I_all"] - ice["detained_total"]
    return {"share": sum(parts.values()) / denom, "parts": {k: v / denom for k, v in parts.items()}}


# ---------------------------------------------------------------- BJS custody by Hispanic origin
def bjs_custody() -> dict:
    txt = BJS_PRISON.read_text()
    t3 = txt[txt.index("TABLE 3\nSentenced prisoners"):]
    row = next(l for l in t3.splitlines() if l.startswith("2022"))
    nums = [int(x.replace(",", "")) for x in row.split()[1:]]
    total, hisp = nums[0], nums[7]
    gate("BJS 2022 sentenced prisoners parsed", total == 1_185_648 and hisp == 273_900, f"total {total:,}, Hispanic {hisp:,}")
    raw = BJS_JAIL.read_bytes().decode("latin-1")
    jrow = next(l for l in raw.splitlines() if l.startswith("2023"))
    fields = next(csv.reader([jrow]))
    jtotal, jhisp = int(fields[1].replace(",", "")), int(fields[7].replace(",", ""))
    gate("BJS midyear 2023 jail inmates parsed", jtotal == 664_200 and jhisp == 95_700, f"total {jtotal:,}, Hispanic {jhisp:,}")
    return {"prison_total": total, "prison_hisp": hisp, "jail_total": jtotal, "jail_hisp": jhisp,
            "hisp_share": (hisp + jhisp) / (total + jtotal)}


# ---------------------------------------------------------------- arrests and NCVS
def arrests() -> dict:
    tree = ast.parse(CRIME.read_text())
    t43 = next(ast.literal_eval(n.value) for n in tree.body
               if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "T43C_TOTAL")
    eth_total, eth_hisp = t43[2], t43[3]
    a = pd.read_csv(ACS19).set_index("group")
    share_arrest = eth_hisp / eth_total
    share_pop = a.loc["hispanic", "adult18"] / a.loc["all", "adult18"]
    gate("FBI 2019 adult arrests, ethnicity panel", (eth_total, eth_hisp) == (5_492_557, 1_031_548),
         f"Hispanic {eth_hisp:,} of {eth_total:,} = {share_arrest:.4f}")
    return {"eth_total": eth_total, "eth_hisp": eth_hisp, "hisp_share_arrests": share_arrest,
            "hisp_share_adults_2019": share_pop, "rr_hisp": share_arrest / share_pop,
            "adults_2019": float(a.loc["all", "adult18"]), "hisp_adults_2019": float(a.loc["hispanic", "adult18"])}


def ncvs() -> dict:
    r = pd.read_csv(NCVS).set_index(["group", "side"])
    vic = r.xs("victim", level="side")
    off = r.xs("offender", level="side")
    rv = (vic.loc["Hispanic", "incidents"] / vic.loc["Hispanic", "person_years"]) / (vic.incidents.sum() / vic.person_years.sum())
    ro = (off.loc["Hispanic", "incidents"] / off.loc["Hispanic", "person_years"]) / (off.incidents.sum() / off.person_years.sum())
    gate("NCVS pooled person-years identical on both sides", abs(vic.person_years.sum() - off.person_years.sum()) < 1,
         f"{vic.person_years.sum():,.0f}")
    return {"rr_victim_hisp": float(rv), "rr_offender_hisp": float(ro),
            "hisp_victim_rate": float(vic.loc["Hispanic", "rate_per_1000"]),
            "all_victim_rate": float(vic.incidents.sum() / vic.person_years.sum() * 1000)}


# ---------------------------------------------------------------- ICE and CBP
def ice() -> dict:
    wb = openpyxl.load_workbook(ICE_XLSX, read_only=True, data_only=True)
    rows = [[v for v in r if v is not None] for r in wb["Detention FY24"].iter_rows(values_only=True)]
    at = next(j for j, r in enumerate(rows) if r and str(r[0]).startswith("ICE Currently Detained by Criminality and Arresting Agency"))
    det = next(r for r in rows[at:] if r[:1] == ["Total"])
    gate("ICE EOFY2024 detained by arresting agency sums to total", det[1] + det[3] == det[5], f"ICE {det[1]:,} + CBP {det[3]:,} = {det[5]:,}")
    adp_cbp = next(r for r in rows if r and r[0] == "CBP Average")[-1]
    adp_ice = next(r for r in rows if r and str(r[0]).strip() == "ICE Average")[-1]
    adp_all = next(r for r in rows if r and str(r[0]).strip() == "Average")[-1]
    gate("ICE FY2024 ADP by arresting agency sums to total", abs(adp_cbp + adp_ice - adp_all) < 0.01,
         f"ICE {adp_ice:,.1f} + CBP {adp_cbp:,.1f} = {adp_all:,.1f}")
    txt = subprocess.run(["pdftotext", "-layout", str(ICE_PDF), "-"], capture_output=True, text=True, check=True).stdout
    sec = txt[txt.index("Country of Citizenship                          Detained"):]
    mex_det = int(re.search(r"Mexico\s+([\d,]+)", sec).group(1).replace(",", ""))
    rem = re.search(r"\nMexico\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)", txt)
    mex_rem = int(rem.group(6).replace(",", ""))
    tot_rem = int(re.search(r"Total\s+267,258\s+185,884\s+59,011\s+72,177\s+142,580\s+([\d,]+)", txt).group(1).replace(",", ""))
    gate("ICE annual report Mexico rows parsed", (mex_det, mex_rem, tot_rem) == (5089, 87298, 271484),
         f"detained EOFY {mex_det:,}; removals {mex_rem:,} of {tot_rem:,}")
    o = openpyxl.load_workbook(OHSS, read_only=True, data_only=True)

    def fy(sheet):
        rs = [[v for v in r if v is not None] for r in o[sheet].iter_rows(values_only=True)]
        hdr = next(r for r in rs if r[:3] == ["Fiscal Year", "Month", "Total"])
        row = next(r for r in rs if r[:2] == [2024, "Total"])
        return dict(zip(hdr[2:], row[2:]))

    ero, book, bookloc, rr = fy("ERO Arrests by Citizenship"), fy("ICE Book-Ins by Citizenship"), \
        fy("ICE Book-Ins by Arrest Loc"), fy("ICE ERO R&R by Citizenship")
    gate("OHSS FY2024 removals agree with the ICE report within rounding", abs(rr["Total"] - tot_rem) <= 10 and abs(rr["Mexico"] - mex_rem) <= 10,
         f"{rr['Mexico']:,}/{rr['Total']:,}")
    gate("OHSS book-ins agree with ICE workbook total 277,913 within rounding", abs(book["Total"] - 277_913) <= 10, f"{book['Total']:,}")
    outlays = json.loads(ICE_OUTLAYS.read_text())["outlays_usd"] / 1e9
    b_m, d_m, a_m = book["Mexico"] / book["Total"], mex_det / det[5], ero["Mexico"] / ero["Total"]
    los_ratio = (d_m / (1 - d_m)) / (b_m / (1 - b_m))
    q_central = a_m * los_ratio / (a_m * los_ratio + 1 - a_m)
    return {"custody_outlays_bn": outlays, "adp_ice": adp_ice, "adp_cbp": adp_cbp, "adp_all": adp_all,
            "interior_share": adp_ice / adp_all, "detained_total": det[5], "detained_ice_arrest": det[1],
            "detained_cbp_arrest": det[3], "mex_detained": mex_det, "share_detained": d_m,
            "share_bookins": b_m, "share_removals": mex_rem / tot_rem, "share_ero_arrests": a_m,
            "bookins_interior": bookloc["Interior"], "bookins_border": bookloc["Border"],
            "los_ratio_mex": los_ratio, "q_central": q_central, "q_low": d_m, "q_high": mex_det / det[1],
            "ero_noncustody_bn": ERO_ALL_VINTAGES / 1e9 - outlays}


def cbp() -> dict:
    with zipfile.ZipFile(FILE_A) as z:
        name = next(n for n in z.namelist() if "AccountBalances" in n)
        df = pd.read_csv(z.open(name), low_memory=False)
    f = df[df.budget_subfunction == "Federal law enforcement activities"]
    c = f[f.federal_account_name.str.contains(r"Customs and Border|U\.S\. Customs|USCS", regex=True)]
    inv = c.federal_account_name.str.contains("Procurement, Construction|Border Security Fencing|Automation Modernization", regex=True)
    ice_os = f[f.federal_account_symbol == "070-0540"].gross_outlay_amount.sum() / 1e9
    gate("ICE O&S sits in subfunction 751 in File A", abs(ice_os - 9.856177507) < 1e-6, f"{ice_os:.6f} bn")
    return {"cbp_751_bn": c.gross_outlay_amount.sum() / 1e9, "cbp_751_excl_invest_bn": c[~inv].gross_outlay_amount.sum() / 1e9}


# ---------------------------------------------------------------- allocation
def main() -> None:
    print("[gates]")
    builder = load_builder()
    bea = bea_cells(builder)
    ref = reference(builder)
    cps = cps_target(builder)
    acs = acs_custody(cps)
    bjs = bjs_custody()
    arr = arrests()
    vic = ncvs()
    ic = ice()
    cb = cbp()

    S = ref["share_national"]
    outside = RESIDENT - ref["cps_pop"]          # outside-CPS residents, nearly all adults
    t_adults = cps["mexico_born"]["18up"] + cps["us_born"]["18up"]
    t_12 = cps["mexico_born"]["12up"] + cps["us_born"]["12up"]
    A_T = t_adults / (cps["cps_civilian"]["18up"] + outside)
    V_T = t_12 / (cps["cps_civilian"]["12up"] + outside)
    gate("target adults match the account's adults key", abs(t_adults - ref["adults_target"]) < 1, f"{t_adults:,.0f}")
    fb_share = cps["mexico_born"]["all"] / (cps["mexico_born"]["all"] + cps["us_born"]["all"])
    a1 = acs["acs1_2024"]
    p = a1["p_mex_of_hisp"]

    shares = {"per_head": S}
    notes = {}
    # offending: Hispanic adult arrest rate relative to all adults, times Mexican/Hispanic custody ratio
    for arm in ("raw", "adj"):
        f_m = a1[f"m_{arm}"] / p
        shares[f"arrest_{arm}"] = A_T * arr["rr_hisp"] * f_m
        shares[f"ncvs_offender_{arm}"] = V_T * vic["rr_offender_hisp"] * f_m
    shares["victimization"] = V_T * vic["rr_victim_hisp"]
    shares["victimization_all_ages"] = S * vic["rr_victim_hisp"]
    for arm in ("raw", "adj", "adj_inst"):
        shares[f"custody_acs_{arm}"] = a1[f"custody_{arm}"]["share"]
        shares[f"custody_acs5_{arm}"] = acs["acs5_2024"][f"custody_{arm}"]["share"]
    tau = (cps["mexico_born"]["18_64"] + cps["us_born"]["18_64"]) / a1["HH_mex"]
    for arm in ("raw", "adj"):
        shares[f"custody_bjs_{arm}"] = bjs["hisp_share"] * a1[f"m_{arm}"] * tau
    ib = ice_bound(acs, cps, ic)
    shares["custody_acs_adj_minus_ice"] = ib["share"]

    # police partition: CBP and ICE custody carved out of the police subline
    P = bea["scaled_bn"]["police"]
    D = ic["custody_outlays_bn"]
    C = cb["cbp_751_excl_invest_bn"]
    police_pool = P - C - D
    i = ic["interior_share"]
    ice_q = {"central": ic["q_central"], "low": ic["q_low"], "high": ic["q_high"]}

    rows = []

    def add(subline, part, key, national, share, split=None, basis="", note=""):
        split = split or {}
        rows.append({"subline": subline, "part": part, "key": key, "national_bn": national, "target_share": share,
                     "target_bn": national * share, "other_bn": national * (1 - share),
                     "mexico_born_bn": national * split["mexico_born"] if "mexico_born" in split else None,
                     "us_born_bn": national * split["us_born"] if "us_born" in split else None,
                     "split_basis": basis, "note": note})

    ph_split = {"mexico_born": S * fb_share, "us_born": S * (1 - fb_share)}
    for sub, nat in bea["scaled_bn"].items():
        add(sub, "whole", "per_head", nat, S, ph_split, "CPS target nativity", "reference: complete-account key")
    for arm in ("raw", "adj", "adj_inst"):
        c = a1[f"custody_{arm}"]
        add("prisons", "whole", f"custody_acs_{arm}", bea["scaled_bn"]["prisons"], c["share"], c["parts"],
            "ACS institutional 18-64 by nativity", "institutional residence, not correctional custody alone")
    for arm in ("raw", "adj"):
        add("prisons", "whole", f"custody_bjs_{arm}", bea["scaled_bn"]["prisons"], shares[f"custody_bjs_{arm}"], None, "",
            "BJS prisons+jails Hispanic share x ACS Mexican/Hispanic institutional ratio x target/ACS scaling")
    add("prisons", "whole", "custody_acs_adj_minus_ice", bea["scaled_bn"]["prisons"], ib["share"], ib["parts"],
        "ACS institutional 18-64 by nativity", "bound: all 5,089 Mexican ICE detainees and all 37,684 detainees removed")
    add("police", "cbp_border", "per_head", C, S, ph_split, "CPS target nativity",
        "CBP subfunction-751 FY2024 gross outlays excl. investment; border spending follows entry flows")
    add("police", "ice_custody_border_arrest", "per_head", D * (1 - i), S, ph_split, "CPS target nativity",
        "CBP-arrest share of FY2024 ICE ADP; treated like CBP")
    add("police", "cbp_border", "zero", C, 0.0, {"mexico_born": 0.0, "us_born": 0.0}, "none",
        "boundary variant: border spending held fixed with respect to the resident stock")
    add("police", "ice_custody_border_arrest", "zero", D * (1 - i), 0.0, {"mexico_born": 0.0, "us_born": 0.0}, "none",
        "boundary variant: border-arrest custody held fixed with respect to the resident stock")
    for lab, q in ice_q.items():
        add("police", "ice_custody_interior", f"ice_interior_{lab}", D * i, q, {"mexico_born": q, "us_born": 0.0},
            "Mexican nationals", "ICE-arrest share of FY2024 ADP x Mexico share of interior bed-days")
    for lab, q in (("detained", ic["share_detained"]), ("bookins", ic["share_bookins"]), ("removals", ic["share_removals"])):
        add("police", "ice_custody_all", f"ice_all_{lab}", D, q, {"mexico_born": q, "us_born": 0.0}, "Mexican nationals",
            "brief's literal option: all custody outlays by Mexico's FY2024 share")
    for key in ("arrest_raw", "arrest_adj", "victimization", "victimization_all_ages", "ncvs_offender_raw", "ncvs_offender_adj"):
        add("police", "non_border", key, police_pool, shares[key], None, "not identified by nativity")
    for arm in ("raw", "adj"):
        add("police", "non_border", f"half_arrest_{arm}", police_pool, 0.5 * shares[f"arrest_{arm}"] + 0.5 * S, None,
            "not identified by nativity", "patrol half per head")
    for lab, c in COURT_CRIMINAL.items():
        for arm in ("raw", "adj"):
            add("law_courts", "whole", f"criminal{int(c*100)}_arrest_{arm}", bea["scaled_bn"]["law_courts"],
                c * shares[f"arrest_{arm}"] + (1 - c) * S, None, "not identified by nativity",
                f"criminal share {c:.2f} by arrests, civil per head")
    add("police", "ero_noncustody_sensitivity", "ero_arrest_share", ic["ero_noncustody_bn"], ic["share_ero_arrests"],
        {"mexico_born": ic["share_ero_arrests"], "us_born": 0.0}, "Mexican nationals",
        "sensitivity only: ERO all-vintage program activity less identified custody, not in any key set")
    alloc = pd.DataFrame(rows)
    alloc.to_csv(DERIVED / "cj_allocation.csv", index=False, float_format="%.6f")

    # key sets over the whole of line 4
    def lookup(sub, part, key):
        r = alloc[(alloc.subline == sub) & (alloc.part == part) & (alloc.key == key)]
        assert len(r) == 1, (sub, part, key)
        return r.iloc[0]

    police_keys = {"offending": "arrest_{m}", "half": "half_arrest_{m}", "victimization": "victimization",
                   "ncvs_offender": "ncvs_offender_{m}"}
    prison_keys = ["custody_acs_raw", "custody_acs_adj", "custody_bjs_raw", "custody_bjs_adj"]
    sets = []
    for pk, prk, (clab, c), qlab, marm, cbt in itertools.product(police_keys, prison_keys, COURT_CRIMINAL.items(),
                                                               ("central", "low", "high"), ("adj", "raw"),
                                                               ("per_head", "zero")):
        parts = [lookup("fire", "whole", "per_head"),
                 lookup("prisons", "whole", prk),
                 lookup("law_courts", "whole", f"criminal{int(c*100)}_arrest_{marm}"),
                 lookup("police", "cbp_border", cbt),
                 lookup("police", "ice_custody_border_arrest", cbt),
                 lookup("police", "ice_custody_interior", f"ice_interior_{qlab}"),
                 lookup("police", "non_border", police_keys[pk].format(m=marm))]
        tgt = sum(x.target_bn for x in parts)
        nat = sum(x.national_bn for x in parts)
        split_ok = all(pd.notna(x.mexico_born_bn) for x in parts)
        sets.append({"police_key": pk, "prisons_key": prk, "court_criminal_share": c, "ice_interior": qlab,
                     "mexican_hispanic_scaling": marm, "cbp_border": cbt, "national_bn": nat, "target_bn": tgt,
                     "target_share": tgt / nat, "change_bn": tgt - ref["target_bn"],
                     "band_low": ref["band_low"] + tgt - ref["target_bn"], "band_high": ref["band_high"] + tgt - ref["target_bn"],
                     "mexico_born_bn": sum(x.mexico_born_bn for x in parts) if split_ok else None})
    ks = pd.DataFrame(sets)
    gate("every key set spends exactly line 4", (ks.national_bn - bea["line4_bn"]).abs().max() < 1e-9, f"{bea['line4_bn']:.3f}")
    ks.to_csv(DERIVED / "key_sets.csv", index=False, float_format="%.6f")
    is_central = ((ks.prisons_key == "custody_acs_adj") & (ks.court_criminal_share == 0.6) & (ks.ice_interior == "central")
                  & (ks.mexican_hispanic_scaling == "adj") & (ks.cbp_border == "per_head"))
    central = ks[is_central & (ks.police_key == "half")].iloc[0]
    by_police = ks[is_central].set_index("police_key").change_bn.to_dict()
    main = ks[(ks.police_key != "ncvs_offender") & (ks.cbp_border == "per_head")]
    main_adj = main[(main.mexican_hispanic_scaling == "adj") & main.prisons_key.isin(["custody_acs_adj", "custody_bjs_adj"])]
    one_at_a_time = {
        "central": ks[is_central & (ks.police_key == "half")].change_bn.iloc[0],
        **{f"prisons_{k}": ks[(ks.police_key == "half") & (ks.prisons_key == k) & (ks.court_criminal_share == 0.6)
                             & (ks.ice_interior == "central") & (ks.mexican_hispanic_scaling == "adj")
                             & (ks.cbp_border == "per_head")].change_bn.iloc[0] for k in prison_keys},
        **{f"courts_{c}": ks[(ks.police_key == "half") & (ks.prisons_key == "custody_acs_adj") & (ks.court_criminal_share == c)
                            & (ks.ice_interior == "central") & (ks.mexican_hispanic_scaling == "adj")
                            & (ks.cbp_border == "per_head")].change_bn.iloc[0] for c in COURT_CRIMINAL.values()},
        **{f"ice_{q}": ks[(ks.police_key == "half") & (ks.prisons_key == "custody_acs_adj") & (ks.court_criminal_share == 0.6)
                         & (ks.ice_interior == q) & (ks.mexican_hispanic_scaling == "adj")
                         & (ks.cbp_border == "per_head")].change_bn.iloc[0] for q in ("low", "central", "high")},
        "scaling_raw": ks[(ks.police_key == "half") & (ks.prisons_key == "custody_acs_raw") & (ks.court_criminal_share == 0.6)
                          & (ks.ice_interior == "central") & (ks.mexican_hispanic_scaling == "raw")
                          & (ks.cbp_border == "per_head")].change_bn.iloc[0],
        "cbp_zero": ks[(ks.police_key == "half") & (ks.prisons_key == "custody_acs_adj") & (ks.court_criminal_share == 0.6)
                       & (ks.ice_interior == "central") & (ks.mexican_hispanic_scaling == "adj")
                       & (ks.cbp_border == "zero")].change_bn.iloc[0],
    }

    # sensitivities outside the grid, each applied to the central set
    cc = COURT_CRIMINAL["central"]
    courts_bn, prisons_bn = bea["scaled_bn"]["law_courts"], bea["scaled_bn"]["prisons"]
    s_arr = shares["arrest_adj"]
    rr_m = arr["rr_hisp"] * a1["m_adj"] / p

    def arrest_delta(new):
        return 0.5 * (new - s_arr) * police_pool + cc * (new - s_arr) * courts_bn

    by = a1["by"]
    nat_rate = {}
    acs_rows = pd.read_csv(ACS, dtype={"hisp": str, "ages": str})
    for n in ("foreign_born", "native"):
        g = acs_rows[(acs_rows["product"] == "acs1_2024") & (acs_rows.ages == "1864") & (acs_rows.nativity == n)]
        nat_rate[n] = g.inst.sum() / g.hh.sum()
    cust_tau = 0.0
    for n, t in (("foreign_born", "mexico_born"), ("native", "us_born")):
        T_n, hh = cps[t]["18_64"], by[n]["HH_mex"]
        rate_m = by[n]["I_mex_adj"] / hh
        cust_tau += min(T_n, hh) * rate_m + max(0.0, T_n - hh) * nat_rate[n]
    cust_tau /= a1["I_all"]
    arr_tau = s_arr * (1 / tau + (1 - 1 / tau) / rr_m)
    s_half = 0.5 * s_arr + 0.5 * S
    rate = {"police": s_half - S, "prisons": shares["custody_acs_adj"] - S,
            "law_courts": cc * s_arr + (1 - cc) * S - S, "fire": 0.0}
    w155 = {k: v / bea["t3155_total_m"] * bea["line4_bn"] for k, v in bea["t3155_m"].items()}
    sensitivity = {
        "arrest_rr_hispanic_1": arrest_delta(A_T * 1.0 * a1["m_adj"] / p),
        "tau_extra_at_national_rates": (cust_tau - shares["custody_acs_adj"]) * prisons_bn + arrest_delta(arr_tau),
        "ero_noncustody_by_ero_arrest_share": ic["ero_noncustody_bn"] * (ic["share_ero_arrests"] - s_half),
        "cbp_keyed_like_police_half": C * (s_half - S),
        "bea_t3155_subline_shares": sum((w155[k] - bea["scaled_bn"][k]) * rate[k] for k in rate),
        "victimization_all_ages_police": (shares["victimization_all_ages"] - shares["victimization"]) * police_pool,
    }

    # central split by nativity, with unsplit parts reported separately
    cparts = {"fire": lookup("fire", "whole", "per_head"), "prisons": lookup("prisons", "whole", "custody_acs_adj"),
              "law_courts": lookup("law_courts", "whole", "criminal60_arrest_adj"),
              "police_cbp": lookup("police", "cbp_border", "per_head"),
              "police_ice_border": lookup("police", "ice_custody_border_arrest", "per_head"),
              "police_ice_interior": lookup("police", "ice_custody_interior", "ice_interior_central"),
              "police_non_border": lookup("police", "non_border", "half_arrest_adj")}
    split_rows = []
    for name, r in cparts.items():
        ref_bn = r.national_bn * S
        if pd.notna(r.mexico_born_bn):
            split_rows.append({"component": name, "national_bn": r.national_bn, "per_head_bn": ref_bn, "use_bn": r.target_bn,
                               "mexico_born_bn": r.mexico_born_bn, "us_born_bn": r.us_born_bn, "unsplit_bn": 0.0})
        elif name == "police_non_border":
            half_ph = 0.5 * r.national_bn * S
            split_rows.append({"component": name, "national_bn": r.national_bn, "per_head_bn": ref_bn, "use_bn": r.target_bn,
                               "mexico_born_bn": half_ph * fb_share, "us_born_bn": half_ph * (1 - fb_share),
                               "unsplit_bn": r.target_bn - half_ph})
        else:  # law courts: civil part per head is splittable, criminal (arrest) part is not
            civil = (1 - COURT_CRIMINAL["central"]) * r.national_bn * S
            split_rows.append({"component": name, "national_bn": r.national_bn, "per_head_bn": ref_bn, "use_bn": r.target_bn,
                               "mexico_born_bn": civil * fb_share, "us_born_bn": civil * (1 - fb_share),
                               "unsplit_bn": r.target_bn - civil})
    split = pd.DataFrame(split_rows)
    # [INFERENCE] proxy only: arrest-keyed parts split by nativity as the target's ACS custody splits
    fb_custody = cparts["prisons"].mexico_born_bn / cparts["prisons"].target_bn
    split["proxy_mexico_born_bn"] = split.mexico_born_bn + split.unsplit_bn * fb_custody
    split["proxy_us_born_bn"] = split.us_born_bn + split.unsplit_bn * (1 - fb_custody)
    split.to_csv(DERIVED / "central_split.csv", index=False, float_format="%.6f")

    inputs = [
        ("reference_share_national", S, "allocations.csv population key x pool fraction"),
        ("target_adults_share", A_T, "CPS target 18+ / (CPS civilian 18+ + outside-CPS residents)"),
        ("target_12up_share", V_T, "CPS target 12+ / (CPS civilian 12+ + outside-CPS residents)"),
        ("target_mexico_born_share", fb_share, "CPS ASEC 2025 canonical target, PRCITSHP 4-5 and PENATVTY 303"),
        ("fbi2019_hisp_share_adult_arrests", arr["hisp_share_arrests"], "FBI CIUS 2019 Table 43C ethnicity panel via crime_cost.py"),
        ("acs2019_hisp_share_adults", arr["hisp_share_adults_2019"], "ACS 2019 B01001/B01001I"),
        ("rr_arrest_hispanic", arr["rr_hisp"], "ratio of the two above"),
        ("acs_hisp_share_inst_1864", a1["hisp_share_inst"], "ACS 2024 1-year PUMS TYPEHUGQ=2"),
        ("bjs_hisp_share_custody", bjs["hisp_share"], "BJS sentenced prisoners 2022 + jail inmates midyear 2023"),
        ("m_raw_mex_share_of_hisp_inst", a1["m_raw"], "ACS 2024 1-year 18-64"),
        ("m_adj_mex_share_of_hisp_inst", a1["m_adj"], "generic-Hispanic excess reallocated by population share"),
        ("m_adj_inst_mex_share_of_hisp_inst", a1["m_adj_inst"], "generic excess reallocated by institutional share"),
        ("m_raw_acs5", acs["acs5_2024"]["m_raw"], "ACS 2020-2024 5-year 18-64"),
        ("m_adj_acs5", acs["acs5_2024"]["m_adj"], "ACS 2020-2024 5-year 18-64"),
        ("p_mex_share_of_hisp_pop_1864", p, "ACS 2024 1-year 18-64"),
        ("tau_target_over_acs_mex_hh_1864", tau, "CPS target 18-64 / ACS Mexican household 18-64"),
        ("ncvs_rr_victim_hispanic", vic["rr_victim_hisp"], "NCVS 2022-2024 pooled violent incidents per resident 12+"),
        ("ncvs_rr_offender_hispanic", vic["rr_offender_hisp"], "NCVS 2022-2024 perceived offender, known single-group"),
        ("ice_custody_outlays_bn", D, "DHS execution report FY2024, two Custody Operations rows"),
        ("ice_interior_share_adp", i, "ICE FY2024 ADP by arresting agency"),
        ("ice_mex_share_detained_eofy", ic["share_detained"], "ICE FY2024 annual report Fig 15 / workbook total"),
        ("ice_mex_share_bookins", ic["share_bookins"], "OHSS monthly tables Nov 2024, FY2024"),
        ("ice_mex_share_removals", ic["share_removals"], "ICE FY2024 annual report appendix"),
        ("ice_mex_share_ero_arrests", ic["share_ero_arrests"], "OHSS monthly tables Nov 2024, FY2024"),
        ("ice_mex_los_ratio", ic["los_ratio_mex"], "odds(detained share)/odds(book-in share)"),
        ("ice_mex_interior_bedday_central", ic["q_central"], "ERO arrest share with the Mexican LOS ratio [INFERENCE]"),
        ("ice_mex_interior_bedday_high", ic["q_high"], "5,089 / 13,633 ICE-arrest detainees at EOFY2024"),
        ("cbp_751_excl_invest_bn", C, "USAspending File A FY2024 gross outlays"),
        ("police_pool_bn", police_pool, "police subline less CBP and ICE custody"),
    ]
    with open(DERIVED / "key_inputs.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["input", "value", "source"])
        for n, v, s in inputs:
            w.writerow([n, f"{v:.6f}", s])

    summary = {"reference_bn": ref["target_bn"], "reference_share": S, "line4_bn": bea["line4_bn"],
               "sublines_bn": bea["scaled_bn"], "central": central.to_dict(),
               "range_change_bn": [float(main.change_bn.min()), float(main.change_bn.max())],
               "range_change_adj_bn": [float(main_adj.change_bn.min()), float(main_adj.change_bn.max())],
               "one_at_a_time_change_bn": one_at_a_time, "sensitivity_delta_bn": sensitivity,
               "change_by_police_key_bn": by_police, "shares": shares, "ice": ic, "cbp": cb, "bjs": bjs, "arrests": arr,
               "ncvs": vic, "acs_m": {k: a1[k] for k in ("m_raw", "m_adj", "m_adj_inst", "p_mex_of_hisp", "hisp_share_inst")},
               "band": [ref["band_low"], ref["band_high"]], "gates": [g[0] for g in GATES],
               "central_split": {"identified": split[["mexico_born_bn", "us_born_bn", "unsplit_bn"]].sum().to_dict(),
                                 "proxy": split[["proxy_mexico_born_bn", "proxy_us_born_bn"]].sum().to_dict(),
                                 "per_head": {"mexico_born_bn": ref["target_bn"] * fb_share,
                                              "us_born_bn": ref["target_bn"] * (1 - fb_share)},
                                 "custody_mexico_born_fraction": fb_custody}}
    (DERIVED / "summary.json").write_text(json.dumps(summary, indent=1, default=float))

    print("\n[shares of the national subline, reference 0.120245]")
    for k, v in shares.items():
        print(f"  {k:30s} {v:.4f}")
    print("\n[sublines, $bn]")
    for k, v in bea["scaled_bn"].items():
        print(f"  {k:12s} {v:8.3f}")
    print(f"  police pool after CBP {C:.3f} and ICE custody {D:.3f}: {police_pool:.3f}")
    print("\n[key sets, change from the per-head $62.425bn]")
    print(f"  central (police half, prisons ACS adj, courts 0.6, ICE interior central): {central.target_bn:.3f} bn, "
          f"change {central.change_bn:+.3f}, band {central.band_low:.1f}-{central.band_high:.1f}")
    for k, v in by_police.items():
        print(f"  police {k:14s} change {v:+.3f}")
    print(f"  range over {len(main)} main sets: {main.change_bn.min():+.3f} to {main.change_bn.max():+.3f}; "
          f"adjusted scaling only: {main_adj.change_bn.min():+.3f} to {main_adj.change_bn.max():+.3f}")
    for k, v in one_at_a_time.items():
        print(f"  one at a time {k:28s} {v:+.3f}")
    for k, v in sensitivity.items():
        print(f"  sensitivity delta {k:36s} {v:+.3f}")
    print(f"\n{len(GATES)} gates passed")


if __name__ == "__main__":
    main()
