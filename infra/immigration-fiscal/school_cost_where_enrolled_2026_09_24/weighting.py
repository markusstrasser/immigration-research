"""Current spending per pupil where the Mexican-origin group's pupils enroll, district by district.

Links the Census F-33 FY2024 district file (current spending per pupil = TCURSPND / ENROLL) to NCES
CCD 2023-24 LEA membership (K-12 pupils, all and Hispanic) by NCES LEA ID, then weights districts
three ways: (i) Hispanic pupils; (ii) Hispanic pupils x the state's Mexican share of Hispanic public
K-12 pupils (ACS 2024 PUMS, acs_mexican_share.py); (iii) Hispanic pupils x the district's Mexican
share of Hispanics (ACS 2020-2024 B03001 by school district, county where no district geography),
carried to pupils with the state's child/all-age ratio and raked to the state share of (ii).

The account's education key already prices each pupil at its state's ASSF Table 8 average
(R_embedded = 0.954, account_pupils.py), so the finding is a correction factor k on the key's school
component, never R itself. Three families:
  A  the account's own (CPS) state mix and ASSF prices, times the within-state district factor f_s
     (group-weighted over all-pupil F-33 district mean in state s);
  B  the administrative state mix (CCD pupils) at ASSF prices, times f_s. Preferred;
  C  the brief's literal R: F-33 district prices in numerator and denominator. Its state level comes
     from matched districts (no ESA spending, fall-2022 enrollment), a different price source from
     the key's, so k_C = R_C / R_embedded mixes a source change into the ratio.
Pupils in districts F-33 does not cover (mostly charters held by non-governmental bodies, out of the
survey's scope, 9% of the group) cost their state's group-specific mean: state means come from
matched districts, state weights from every CCD pupil.

Robustness: current spending net of COVID-relief current spending (F-33 item AE1, ESSER/GEER/CRF,
3.5% of FY2024 current spending, allocated by Title I shares), and the within-state factor from
FY2019 spending. Other concepts (capital outlay, interest, instruction + support) use family C.
Writes derived/r_by_spec.csv, r_other_concepts.csv, state_breakdown.csv, district_match_by_state.csv,
linkage.json.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/weighting.py
"""
import json
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ccd  # noqa: E402

FISCAL = HERE.parent
CACHE = HERE / "_cache"
OUT = HERE / "derived"
F33_DIR = Path("/Users/alien/research-data/immigration-fiscal/data/external/census_f33_district")
F33 = F33_DIR / "elsec24t.txt"          # summary items (TCURSPND, ENROLL, TCAPOUT, TINTRST, ...)
F33_ALL = F33_DIR / "elsec24.txt"       # all items, for AE1 (COVID-relief current spending)
F33_19 = CACHE / "elsec19t.txt"
STATE_PARAMS = FISCAL / "gen_ledger_extension_2026_09_16/state_parameters.csv"
PP_BAND = (3_000.0, 80_000.0)          # same plausibility band as ledger district_differential.py
MIN_HISP_POP = 100                     # ACS 5-year Hispanic residents needed to use a district's own share
MONEY = ["TCURSPND", "TCAPOUT", "TINTRST", "TCURINST", "TCURSSVC"]
COUNTS = ["k12_all", "k12_hisp", "tot_all", "tot_hisp", "pk_all", "pk_hisp"]
NYC_F33 = "3620580"                    # NEW YORK CITY SCHOOL DISTRICT, one unit in F-33
WEIGHTS = {
    "all": "w_all", "hispanic": "w_hisp", "mexican_state_share": "w_mex_state",
    "mexican_state_share_broad": "w_mex_state_broad", "mexican_district_share": "w_mex_dist",
    "mexican_district_share_unraked": "w_mex_dist_unraked", "mexican_district_share_all_ages": "w_mex_dist_all_age",
}
MAIN_WEIGHTS = ["hispanic", "mexican_state_share", "mexican_district_share"]


def read_f33():
    d = pd.read_csv(F33, dtype={"NCESID": str, "FIPST": str, "SCHLEV": str, "UNIT_TYPE": str, "CONUM": str})
    d["LEAID"] = d.NCESID.str.strip().str.zfill(7)
    for c in MONEY:
        d[c] = pd.to_numeric(d[c], errors="coerce") * 1000.0     # thousands of dollars
    d["ENROLL"] = pd.to_numeric(d.ENROLL, errors="coerce")
    # The all-items file has one more field per row than header names: index_col=False keeps alignment.
    a = pd.read_csv(F33_ALL, dtype={"NCESID": str}, index_col=False, encoding="latin-1", usecols=["NCESID", "AE1", "V33"])
    a["LEAID"] = a.NCESID.str.strip().str.zfill(7)
    d = d.merge(a[["LEAID", "AE1", "V33"]], on="LEAID", how="left", validate="one_to_one")
    if not (d.V33 == d.ENROLL).all():
        raise SystemExit("[BLOCKED] elsec24.txt and elsec24t.txt disagree on enrollment: misaligned read")
    d["AE1"] = d.AE1 * 1000.0
    e = d.ENROLL.where(d.ENROLL > 0)
    d["pp"] = d.TCURSPND / e
    d["pp_ex_covid"] = (d.TCURSPND - d.AE1) / e
    d["pp_capout"] = d.TCAPOUT / e
    d["pp_interest"] = d.TINTRST / e
    d["pp_core"] = (d.TCURINST + d.TCURSSVC) / e     # instruction + support; no food services or enterprise
    old = pd.read_csv(F33_19, sep="\t", dtype={"NCESID": str, "CONUM": str})
    old = old[old.NCESID.notna()]
    old["LEAID"] = old.NCESID.str.strip().str.zfill(7)
    old = old.drop_duplicates("LEAID")
    old_pp = pd.to_numeric(old.TCURSPND, errors="coerce") * 1000 / pd.to_numeric(old.ENROLL, errors="coerce").where(lambda s: s > 0)
    d["pp_fy2019"] = d.LEAID.map(pd.Series(old_pp.to_numpy(), index=old.LEAID))
    # State COVID-relief share of current spending, all F-33 units (for ASSF prices net of relief).
    covid_share = d.groupby(d.LEAID.str[:2].astype(int)).apply(lambda g: g.AE1.sum() / g.TCURSPND.sum())
    return d, covid_share


def acs_shares():
    """ACS 2020-2024 B03001: Hispanic and Mexican residents by school district (all ages) and county."""
    frames = []
    for label in ["unified", "elementary", "secondary"]:
        rows = json.loads((CACHE / f"acs5_2024_B03001_{label}.json").read_text())
        f = pd.DataFrame(rows[1:], columns=rows[0])
        f["LEAID"] = f.state + f.iloc[:, -1]
        frames.append(f[["LEAID", "B03001_003E", "B03001_004E"]])
    dist = pd.concat(frames, ignore_index=True)
    dist = dist[~dist.LEAID.str.endswith("99999")]    # "Remainder of <state>" pseudo-districts
    if dist.LEAID.duplicated().any():
        raise SystemExit("[BLOCKED] a Census school-district GEOID appears under two district types")
    rows = json.loads((CACHE / "acs5_2024_B03001_county.json").read_text())
    cty = pd.DataFrame(rows[1:], columns=rows[0])
    cty["CONUM"] = cty.state + cty.county
    for f in (dist, cty):
        f["hisp_pop"] = pd.to_numeric(f.B03001_003E)
        f["mex_pop"] = pd.to_numeric(f.B03001_004E)
    return dist.set_index("LEAID")[["hisp_pop", "mex_pop"]], cty.set_index("CONUM")[["hisp_pop", "mex_pop"]]


def rake(h, m, target_share, cap=1.0):
    """Scale shares m so the Hispanic-weighted mean equals target_share, capping at 1."""
    m = m.copy()
    for _ in range(100):
        cur = (h * m).sum() / h.sum()
        if abs(cur - target_share) < 1e-12:
            break
        m = np.minimum(cap, m * target_share / cur)
    return m


def build():
    f33, covid_share = read_f33()
    lea = ccd.lea_2324()
    for c in COUNTS:
        lea[c] = pd.to_numeric(lea[c])
    # Hispanic K-12 missing but a Hispanic total present: scale the total by the district's K-12 share.
    fill = lea.k12_hisp.isna() & lea.tot_hisp.notna() & lea.tot_all.gt(0)
    lea.loc[fill, "k12_hisp"] = lea.tot_hisp * lea.k12_all.fillna(lea.tot_all) / lea.tot_all
    lea["k12_all"] = lea.k12_all.fillna(lea.tot_all - lea.pk_all.fillna(0))
    lea["k12_hisp"] = lea.k12_hisp.fillna(0)
    lea["fips"] = lea.LEAID.str[:2].astype(int)
    lea = lea[lea.fips.le(56)]                 # 50 states + DC; drop BIE (59) and territories
    directory = ccd.lea_directory_2324().set_index("LEAID")
    # CCD splits New York City into geographic districts; F-33 reports the city as one system.
    nyc = lea.LEAID.map(directory.LEA_NAME).fillna("").str.startswith("NEW YORK CITY GEOGRAPHIC DISTRICT")
    if nyc.sum() < 30:
        raise SystemExit(f"[BLOCKED] expected the NYC geographic districts in CCD, found {int(nyc.sum())}")
    lea.loc[nyc, "LEAID"] = NYC_F33
    lea = lea.groupby(["LEAID", "fips"], as_index=False)[COUNTS].sum(min_count=1)
    lea = lea.join(directory[["LEA_TYPE", "CHARTER_LEA"]], on="LEAID")
    lea.loc[lea.LEAID.eq(NYC_F33), "LEA_TYPE"] = "2"

    acs = pd.read_csv(OUT / "acs_state_pupils.csv").set_index("state_fips")
    dist_acs, cty_acs = acs_shares()
    d = lea.merge(f33[["LEAID", "NAME", "SCHLEV", "CONUM", "ENROLL", "pp", "pp_ex_covid", "pp_fy2019", "pp_capout",
                       "pp_interest", "pp_core"]], on="LEAID", how="left", indicator=True)
    d["matched"] = d._merge.eq("both")
    d["valid"] = d.matched & d.pp.between(*PP_BAND) & d.k12_all.gt(0)
    d["state_share"] = d.fips.map(acs.mex_share_of_hisp_pupils)
    d["state_share_broad"] = d.fips.map(acs.mex_broad_share_of_hisp_pupils)
    # District share: own Census geography if it has enough Hispanic residents, else county, else state.
    own_h, own_m = d.LEAID.map(dist_acs.hisp_pop), d.LEAID.map(dist_acs.mex_pop)
    c_h, c_m = d.CONUM.map(cty_acs.hisp_pop), d.CONUM.map(cty_acs.mex_pop)
    use_own, use_cty = own_h.ge(MIN_HISP_POP), ~own_h.ge(MIN_HISP_POP) & c_h.ge(MIN_HISP_POP)
    share = np.where(use_own, own_m / own_h, np.where(use_cty, c_m / c_h, np.nan))
    d["share_source"] = np.where(use_own, "district", np.where(use_cty, "county", "state"))
    share = np.where(np.isnan(share), d.fips.map(acs.mex_share_of_hisp_all_ages), share)
    d["dist_share_all_age"] = share
    d["dist_share_child"] = np.minimum(1.0, share * d.fips.map(acs.child_to_all_age_ratio))
    d["dist_share_raked"] = np.nan
    for fips, idx in d.groupby("fips").groups.items():
        block = d.loc[idx]
        if block.k12_hisp.sum() > 0:
            d.loc[idx, "dist_share_raked"] = rake(block.k12_hisp.to_numpy(), block.dist_share_child.to_numpy(),
                                                  float(acs.mex_share_of_hisp_pupils[fips]))
    d["dist_share_raked"] = d.dist_share_raked.fillna(d.state_share)
    d["w_all"] = d.k12_all
    d["w_hisp"] = d.k12_hisp
    d["w_mex_state"] = d.k12_hisp * d.state_share
    d["w_mex_state_broad"] = d.k12_hisp * d.state_share_broad
    d["w_mex_dist"] = d.k12_hisp * d.dist_share_raked
    d["w_mex_dist_unraked"] = d.k12_hisp * d.dist_share_child
    d["w_mex_dist_all_age"] = d.k12_hisp * d.dist_share_all_age
    return d, covid_share


def state_table(d, price):
    """State means under every weight (valid districts with a price) and state totals (all CCD pupils)."""
    v = d[d.valid & d[price].notna()]
    rows = []
    for fips, block in d.groupby("fips"):
        vb = v[v.fips == fips]
        row = {"fips": fips}
        for name, col in WEIGHTS.items():
            row[f"W_{name}"] = block[col].sum()
            row[f"Wmatched_{name}"] = vb[col].sum()
            row[f"P_{name}"] = (vb[col] * vb[price]).sum() / vb[col].sum() if vb[col].sum() > 0 else np.nan
        rows.append(row)
    t = pd.DataFrame(rows).set_index("fips")
    for name in WEIGHTS:                      # no group pupils in valid districts: all-pupil mean
        t[f"P_{name}"] = t[f"P_{name}"].fillna(t["P_all"])
    return t


def ratio(t, name, weights="W"):
    num = (t[f"{weights}_{name}"] * t[f"P_{name}"]).sum() / t[f"{weights}_{name}"].sum()
    den = (t[f"{weights}_all"] * t["P_all"]).sum() / t[f"{weights}_all"].sum()
    return num / den


def families(t, name, acct, price, factor_table=None, concept="current"):
    """k and R for families A and B at state prices `price`, within-state factor from `factor_table`."""
    ft = t if factor_table is None else factor_table
    f = (ft[f"P_{name}"] / ft.P_all).reindex(price.index).fillna(1.0)
    spend = acct.target_pupils * price
    price_acct = spend.sum() / acct.target_pupils.sum()
    nat_acct = (acct.national_pupils * price).sum() / acct.national_pupils.sum()
    w_all = t.W_all.reindex(price.index).fillna(0)
    nat_admin = (w_all * price).sum() / w_all.sum()
    wg = t[f"W_{name}"].reindex(price.index).fillna(0)
    p_state = (wg * price).sum() / wg.sum()
    p_b = (wg * price * f).sum() / wg.sum()
    k_a = (spend * f).sum() / spend.sum()
    return [
        dict(family="A", weighting=name, concept=concept, state_mix="account (CPS)", R=price_acct * k_a / nat_acct,
             R_embedded_same_concept=price_acct / nat_acct, group_price=price_acct * k_a, k_state_mix_only=1.0,
             k_within_state_only=k_a),
        dict(family="B", weighting=name, concept=concept, state_mix="CCD (admin)", R=p_b / nat_admin,
             R_embedded_same_concept=price_acct / nat_acct, group_price=p_b, k_state_mix_only=p_state / price_acct,
             k_within_state_only=p_b / p_state),
    ]


def main():
    OUT.mkdir(exist_ok=True)
    d, covid_share = build()
    embedded = json.loads((OUT / "account_embedded_price.json").read_text())
    r_emb = embedded["r_embedded_personal"]
    acct = pd.read_csv(OUT / "account_pupils_by_state.csv").set_index("fips")
    names = acct.state
    assf = pd.read_csv(STATE_PARAMS).set_index("fips").per_pupil_current_spending.reindex(acct.index)

    # --- linkage report
    valid = d.valid
    by_state = d.assign(k12_all_valid=d.k12_all.where(valid, 0), k12_hisp_valid=d.k12_hisp.where(valid, 0),
                        mex_valid=d.w_mex_dist.where(valid, 0)).groupby("fips").agg(
        ccd_leas=("LEAID", "size"), matched_leas=("matched", "sum"), valid_leas=("valid", "sum"),
        k12_all=("k12_all", "sum"), k12_hisp=("k12_hisp", "sum"), group_pupils=("w_mex_dist", "sum"),
        k12_all_valid=("k12_all_valid", "sum"), k12_hisp_valid=("k12_hisp_valid", "sum"),
        group_pupils_valid=("mex_valid", "sum")).reset_index()
    by_state["all_pupil_coverage"] = by_state.k12_all_valid / by_state.k12_all
    by_state["hisp_pupil_coverage"] = by_state.k12_hisp_valid / by_state.k12_hisp
    by_state["group_pupil_coverage"] = by_state.group_pupils_valid / by_state.group_pupils
    by_state.insert(1, "state", by_state.fips.map(names))
    by_state.to_csv(OUT / "district_match_by_state.csv", index=False, lineterminator="\n", float_format="%.6f")
    f33_rows = len(pd.read_csv(F33, usecols=["NCESID"], dtype=str))
    unmatched = d[~valid]
    linkage = dict(
        f33_rows=f33_rows, ccd_leas_50_states_dc=len(d), ccd_leas_matched_to_f33=int(d.matched.sum()),
        ccd_leas_valid=int(valid.sum()), f33_rows_matched=int(d.matched.sum()),
        k12_all=float(d.k12_all.sum()), k12_hisp=float(d.k12_hisp.sum()), group_pupils_admin=float(d.w_mex_dist.sum()),
        coverage_all=float(d.k12_all[valid].sum() / d.k12_all.sum()),
        coverage_hisp=float(d.k12_hisp[valid].sum() / d.k12_hisp.sum()),
        coverage_group=float(d.w_mex_dist[valid].sum() / d.w_mex_dist.sum()),
        uncovered_group_pupils_by_lea_type=unmatched.groupby("LEA_TYPE").w_mex_dist.sum().round(0).to_dict(),
        uncovered_group_pupils_charter_leas=float(unmatched.w_mex_dist[unmatched.LEA_TYPE.eq("7")].sum()),
        group_share_source=d.groupby("share_source").w_mex_dist.sum().round(0).to_dict(),
        dropped_matched_invalid=int((d.matched & ~valid).sum()),
    )
    (OUT / "linkage.json").write_text(json.dumps(linkage, indent=1) + "\n")

    # --- families A, B, C for current spending, and robustness concepts for A and B
    t = state_table(d, "pp")
    national_pp = (t.W_all * t.P_all).sum() / t.W_all.sum()
    rows = []
    for name in [n for n in WEIGHTS if n != "all"]:
        rows += families(t, name, acct, assf)
        r_c = ratio(t, name)
        p_state = (t[f"W_{name}"] * t.P_all).sum() / t[f"W_{name}"].sum()
        rows.append(dict(family="C", weighting=name, concept="current", state_mix="CCD (admin)", R=r_c,
                         R_embedded_same_concept=r_emb, group_price=r_c * national_pp,
                         k_state_mix_only=(p_state / national_pp) / r_emb, k_within_state_only=r_c * national_pp / p_state,
                         R_matched_only=ratio(t, name, "Wmatched")))
    t_ex = state_table(d, "pp_ex_covid")
    assf_ex = assf * (1 - covid_share.reindex(assf.index).fillna(0))
    t_19 = state_table(d, "pp_fy2019")
    for name in MAIN_WEIGHTS:
        rows += families(t_ex, name, acct, assf_ex, concept="current_ex_covid_relief")
        rows += families(t, name, acct, assf, factor_table=t_19, concept="current_within_state_factor_fy2019")
    r = pd.DataFrame(rows)
    # k: the factor on the key's school component. Family A/B: ratio of the group's share of national
    # school spending to the account's, same price concept; family C: R_C / R_embedded.
    r["k"] = r.R / r.R_embedded_same_concept
    r.insert(0, "spec", r.family + "_" + r.concept + "_" + r.weighting)
    r["R_embedded_account"] = r_emb
    r["national_price_f33"] = national_pp
    r.to_csv(OUT / "r_by_spec.csv", index=False, lineterminator="\n", float_format="%.6f")

    # --- other spending concepts under the same weights (family C: F-33 district prices throughout)
    concepts = []
    for price in ["pp", "pp_ex_covid", "pp_core", "pp_capout", "pp_interest", "pp_fy2019"]:
        tc = state_table(d, price)
        for name in MAIN_WEIGHTS:
            concepts.append(dict(concept=price, weighting=name, R=ratio(tc, name),
                                 national_per_pupil=(tc.W_all * tc.P_all).sum() / tc.W_all.sum(),
                                 group_per_pupil=(tc[f"W_{name}"] * tc[f"P_{name}"]).sum() / tc[f"W_{name}"].sum()))
    concepts = pd.DataFrame(concepts)
    concepts.to_csv(OUT / "r_other_concepts.csv", index=False, lineterminator="\n", float_format="%.6f")

    # --- state breakdown (preferred: family B, Mexican district share, current spending)
    f_pref = (t.P_mexican_district_share / t.P_all).reindex(acct.index)
    sb = pd.DataFrame({
        "state": names, "fips": acct.index,
        "account_group_pupils": acct.target_pupils, "account_all_pupils": acct.national_pupils,
        "admin_group_pupils": t.W_mexican_district_share.reindex(acct.index),
        "admin_group_pupils_in_f33_districts": t.Wmatched_mexican_district_share.reindex(acct.index),
        "ccd_hispanic_k12": t.W_hispanic.reindex(acct.index), "ccd_all_k12": t.W_all.reindex(acct.index),
        "acs_mexican_share_of_hispanic_pupils": pd.read_csv(OUT / "acs_state_pupils.csv").set_index("state_fips")
        .mex_share_of_hisp_pupils.reindex(acct.index),
        "assf_per_pupil": assf, "f33_all_pupil_per_pupil": t.P_all.reindex(acct.index),
        "f33_hispanic_per_pupil": t.P_hispanic.reindex(acct.index),
        "f33_group_per_pupil": t.P_mexican_district_share.reindex(acct.index), "within_state_factor": f_pref,
    })
    sb["group_spending_per_pupil"] = sb.assf_per_pupil * sb.within_state_factor
    sb["admin_group_share"] = sb.admin_group_pupils / sb.admin_group_pupils.sum()
    sb["account_group_share"] = sb.account_group_pupils / sb.account_group_pupils.sum()
    w_all = t.W_all.reindex(acct.index).fillna(0)
    nat_admin = (w_all * assf).sum() / w_all.sum()
    sb["contribution_to_R"] = sb.admin_group_share * sb.group_spending_per_pupil / nat_admin
    sb["group_pupils_admin_over_account"] = sb.admin_group_pupils / sb.account_group_pupils
    sb = sb.sort_values("admin_group_pupils", ascending=False)
    pref = r.set_index("spec").R["B_current_mexican_district_share"]
    if abs(sb.contribution_to_R.sum() - pref) > 1e-9:
        raise SystemExit("[BLOCKED] state contributions do not add to R")
    sb.to_csv(OUT / "state_breakdown.csv", index=False, lineterminator="\n", float_format="%.6f")
    return d, r, concepts, linkage


if __name__ == "__main__":
    d, r, concepts, linkage = main()
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 20)
    print(json.dumps(linkage, indent=1, default=float))
    print(r[["spec", "R", "R_embedded_same_concept", "k", "k_state_mix_only", "k_within_state_only", "group_price"]]
          .to_string(index=False))
    print(concepts.to_string(index=False))
