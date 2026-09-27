"""Spousal endogamy by generation and the ethnic identification of children of mixed couples,
Mexican origin (and Indian origin on the same code), CPS ASEC 2022-2025 pooled.

Inputs: the four Census public-use ASEC archives already held locally (paths and SHA-256 below;
research/immigration-dataset-register.md rows CPS-ASEC-2022-FULL, -2023-FULL, CPS ASEC 2024
March, CPS ASEC2025). Person file pppubYY.csv, household file hhpubYY.csv (GESTFIPS), and the
160 successive-difference replicate person weights asec_csv_repwgt_YYYY.csv joined on
(PH_SEQ, PPPOS) = (h_seq, PPPOS).

Origin (union definition, used for the spouse and for the parents of children):
  Mexican origin  = born in Mexico (PENATVTY 303), or a Mexico-born parent, or Hispanic origin
                    Mexican (PEHSPNON 1 & PRDTHSP 1);
  other Hispanic  = PEHSPNON 1 and not Mexican origin;
  non-Hispanic    = the rest (split NH white PRDTRACE 1 / NH other).
Ego generations (canonical masks of extend_ledger.py / generation_split analyze_cps.py):
  G1  = foreign-born (PRCITSHP 4,5) born in Mexico;
  G2  = US-born (PRCITSHP 1-3) with a Mexico-born parent;
  G3+ = US-born, both parents born in US areas, Hispanic origin Mexican.
  G3 observed / G4+ observed: generation_split_2026_09_20 grandparent linkage (co-resident
  biological parents' parental birthplaces), copied below.
Indian: G1 India-born foreign-born (PENATVTY 210); G2 US-born with an India-born parent.
Indian-origin spouse = India-born, India-born parent, or Asian Indian (PRDASIAN 1).

Married = A_MARITL 1-2 (spouse present), ages 25-54; spouse found through A_SPOUSE in the same
household. Same-sex couples are dropped (counted). Random-matching benchmark: the weighted share
of Mexican-origin people among opposite-sex married persons 25-54 in the ego's state and year.

SEs: 160 replicates; the pooled estimate sums weights over years, replicate r sums replicate r
over years, SE = sqrt(4/160 * sum (theta_r - theta)^2). Adjacent ASECs share about half their
households, so years are not independent samples; `se_conservative` is the weight-share
average of the four single-year SEs (the SE if the years were perfectly correlated).
"""
import csv
import hashlib
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
REPO = HERE.parents[2]
LATAM = HERE.parent / "latam_comparison_2026_09_17" / "_cache"
DATA = Path.home() / "research-data" / "immigration-fiscal" / "data"
ARCHIVES = {
    2022: (LATAM / "2022" / "asecpub22csv.zip", "7338011adefca16dae30a4469ddaf0c01cef579b607b26b4bceec749376e4ac9"),
    2023: (LATAM / "2023" / "asecpub23csv.zip", "d2e000250782adfbdd7f29c82b66d866591a30f0d330496698ec19f9c784ce11"),
    2024: (DATA / "census" / "cps_asec_2024_march.zip", "cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09"),
    2025: (DATA / "external/stage3/census/cps_asec_2025/asecpub25csv.zip",
           "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"),
}
US = [57, 60, 66, 69, 73, 78]
R = 161
WCOLS = [f"pwwgt{i}" for i in range(R)]
PCOLS = ["PH_SEQ", "PPPOS", "A_LINENO", "A_AGE", "A_SEX", "A_HGA", "A_MARITL", "A_SPOUSE", "PRPERTYP",
         "PRCITSHP", "PENATVTY", "PEMNTVTY", "PEFNTVTY", "PEHSPNON", "PRDTHSP", "PRDASIAN", "PRDTRACE",
         "PEPAR1", "PEPAR2", "PEPAR1TYP", "PEPAR2TYP", "PXHSPNON", "PXNATVTY", "PXMNTVTY", "PXFNTVTY",
         "PXPAR1", "PXPAR2", "PXPAR1TYP", "PXPAR2TYP", "MARSUPWT"]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while block := f.read(1 << 24):
            h.update(block)
    return h.hexdigest()


def load_year(year):
    path, digest = ARCHIVES[year]
    assert sha(path) == digest, f"{path}: SHA-256 changed"
    yy = str(year)[2:]
    with zipfile.ZipFile(path) as z:
        d = pd.read_csv(z.open(f"pppub{yy}.csv"), usecols=PCOLS)
        h = pd.read_csv(z.open(f"hhpub{yy}.csv"), usecols=["H_SEQ", "GESTFIPS"])
        w = pd.read_csv(z.open(f"asec_csv_repwgt_{year}.csv"), usecols=["h_seq", "PPPOS"] + WCOLS)
    n = len(d)
    d = d.merge(h.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", how="left", validate="many_to_one")
    d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    assert len(d) == n and d.GESTFIPS.notna().all() and d.pwwgt0.notna().all(), f"{year}: join lost rows"
    assert np.allclose(d.MARSUPWT / 100, d.pwwgt0, atol=0.011), f"{year}: pwwgt0 != MARSUPWT/100"
    assert d.set_index(["PH_SEQ", "A_LINENO"]).index.is_unique, f"{year}: duplicate person key"
    d["year"] = year
    print(f"  ✓ {year}: {n:,} persons, hash, weights and household join verified", flush=True)
    return d


def origin(d):
    native = d.PRCITSHP.isin([1, 2, 3])
    mex_parent = d.PEMNTVTY.eq(303) | d.PEFNTVTY.eq(303)
    ind_parent = d.PEMNTVTY.eq(210) | d.PEFNTVTY.eq(210)
    d["mex_origin"] = d.PENATVTY.eq(303) | mex_parent | (d.PEHSPNON.eq(1) & d.PRDTHSP.eq(1))
    d["other_hisp"] = d.PEHSPNON.eq(1) & ~d.mex_origin
    d["non_hisp"] = d.PEHSPNON.eq(2) & ~d.mex_origin
    d["nh_white"] = d.non_hisp & d.PRDTRACE.eq(1)
    d["ind_origin"] = d.PENATVTY.eq(210) | ind_parent | d.PRDASIAN.eq(1)
    d["gen"] = ""
    d.loc[~native & d.PENATVTY.eq(303), "gen"] = "mex_G1"
    d.loc[native & mex_parent, "gen"] = "mex_G2"
    d.loc[native & d.PEMNTVTY.isin(US) & d.PEFNTVTY.isin(US) & d.PEHSPNON.eq(1) & d.PRDTHSP.eq(1), "gen"] = "mex_G3plus"
    d["igen"] = ""
    d.loc[~native & d.PENATVTY.eq(210), "igen"] = "ind_G1"
    d.loc[native & ind_parent & ~mex_parent, "igen"] = "ind_G2"
    d["usb_nh_white"] = native & d.nh_white & ~mex_parent & ~ind_parent
    return d


def grandparent_split(d):
    """generation_split_2026_09_20/analyze_cps.py classify(), reported-linkage arm, per year."""
    out = pd.Series("", index=d.index)
    for _, y in d.groupby("year"):
        n = len(y)
        lookup = pd.Series(np.arange(n), index=pd.MultiIndex.from_frame(y[["PH_SEQ", "A_LINENO"]]))
        gp = np.full((n, 4), np.nan)
        consistent = np.ones(n, bool)
        for slot in (1, 2):
            line = y[f"PEPAR{slot}"].to_numpy()
            parent = lookup.reindex(pd.MultiIndex.from_arrays([y.PH_SEQ.to_numpy(), line])).fillna(-1).to_numpy(int)
            linked = (line > 0) & (parent >= 0)
            assert not np.any((line > 0) & ~linked), "broken parent link"
            bio = linked & y[f"PEPAR{slot}TYP"].eq(1).to_numpy()
            p = np.maximum(parent, 0)
            consistent &= ~bio | np.isin(y.PENATVTY.to_numpy()[p], US)
            usable = bio & np.isin(y.PENATVTY.to_numpy()[p], US)
            for j, field in enumerate(("PEMNTVTY", "PEFNTVTY")):
                gp[usable, 2 * (slot - 1) + j] = y[field].to_numpy()[p[usable]]
        base = (y.gen == "mex_G3plus").to_numpy()
        g3 = base & consistent & (gp == 303).any(axis=1)
        g4 = base & consistent & np.isin(gp, US).all(axis=1)
        lab = np.where(g3, "mex_G3_observed", np.where(g4, "mex_G4plus_observed", ""))
        out.loc[y.index] = lab
    return out


def se_sdr(theta):
    return float(np.sqrt(4.0 / 160.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def ratio(num_w, den_w):
    return num_w.sum(0) / den_w.sum(0)


def estimate(frame, y):
    """Weighted mean of y over frame, pooled replicate SE and conservative (annual-average) SE."""
    w = frame[WCOLS].to_numpy(float)
    y = np.asarray(y, float)
    theta = (w * y[:, None]).sum(0) / w.sum(0)
    annual, shares = [], []
    for year in sorted(frame.year.unique()):
        m = (frame.year == year).to_numpy()
        if m.sum() < 2:
            continue
        t = (w[m] * y[m, None]).sum(0) / w[m].sum(0)
        annual.append(se_sdr(t))
        shares.append(w[m, 0].sum())
    cons = float(np.average(annual, weights=shares)) if annual else float("nan")
    return theta, se_sdr(theta), cons


def main():
    DERIVED.mkdir(exist_ok=True)
    d = pd.concat([load_year(y) for y in ARCHIVES], ignore_index=True)
    d = origin(d)
    d["gp_split"] = grandparent_split(d)
    key = pd.MultiIndex.from_frame(d[["year", "PH_SEQ", "A_LINENO"]])
    pos = pd.Series(np.arange(len(d)), index=key)

    # ---- spouse linkage gate
    married = d[d.A_MARITL.isin([1, 2]) & d.A_AGE.between(25, 54)].copy()
    sp = pos.reindex(pd.MultiIndex.from_arrays([married.year, married.PH_SEQ, married.A_SPOUSE])).to_numpy()
    found = ~np.isnan(sp)
    gate = {"married_25_54": len(married), "spouse_found": int(found.sum()), "share": found.mean()}
    print(f"  spouse linkage: {found.sum():,} of {len(married):,} ({found.mean():.4%})", flush=True)
    assert found.mean() >= 0.99, "spouse linkage gate failed"
    married = married[found].copy()
    s = d.iloc[sp[found].astype(int)]
    back = s.A_SPOUSE.to_numpy() == married.A_LINENO.to_numpy()
    gate["reciprocal_pointer_share"] = back.mean()
    for c in ["mex_origin", "other_hisp", "non_hisp", "nh_white", "ind_origin", "A_SEX", "PENATVTY", "gen"]:
        married[f"sp_{c}"] = s[c].to_numpy()
    same_sex = married.A_SEX.eq(married.sp_A_SEX)
    gate["same_sex_dropped"] = int(same_sex.sum())
    married = married[~same_sex].copy()
    married["sp_nh_other"] = married.sp_non_hisp & ~married.sp_nh_white
    married["sp_india_born"] = married.sp_PENATVTY.eq(210)

    # random-matching benchmark: Mexican-origin share of opposite-sex married 25-54, same state and year
    pool = married.groupby(["year", "GESTFIPS", "A_SEX"]).apply(
        lambda g: np.average(g.mex_origin, weights=g.pwwgt0), include_groups=False).rename("mex_share")
    look = pool.reindex(pd.MultiIndex.from_arrays([married.year, married.GESTFIPS, 3 - married.A_SEX])).to_numpy()
    married["expected_mex"] = look
    married["excess_mex"] = married.sp_mex_origin.astype(float) - married.expected_mex

    rows = []

    def add(measure, group, frame, y, adjustment="raw", source="CPS ASEC 2022-2025"):
        theta, se, cons = estimate(frame, y)
        rows.append({"source": source, "measure": measure, "generation": group, "n": len(frame),
                     "estimate": theta[0], "se": se, "se_conservative": cons, "adjustment": adjustment})

    groups = {g: married[married.gen == g] for g in ["mex_G1", "mex_G2", "mex_G3plus"]}
    groups.update({g: married[married.gp_split == g] for g in ["mex_G3_observed", "mex_G4plus_observed"]})
    groups.update({g: married[married.igen == g] for g in ["ind_G1", "ind_G2"]})
    groups["usb_nh_white"] = married[married.usb_nh_white]
    for g, f in groups.items():
        if g.startswith("ind"):
            add("spouse_indian_origin", g, f, f.sp_ind_origin)
            add("spouse_india_born", g, f, f.sp_india_born)
            add("spouse_non_indian", g, f, ~f.sp_ind_origin)
            continue
        if g == "usb_nh_white":
            add("spouse_nh_white", g, f, f.sp_nh_white)
        add("spouse_mexican_origin", g, f, f.sp_mex_origin)
        add("spouse_other_hispanic", g, f, f.sp_other_hisp)
        add("spouse_non_hispanic", g, f, f.sp_non_hisp)
        add("spouse_nh_white_share", g, f, f.sp_nh_white)
        add("spouse_nh_other", g, f, f.sp_nh_other)
        add("expected_mexican_spouse_random", g, f, f.expected_mex)
        add("excess_mexican_spouse_over_random", g, f, f.excess_mex)
    # by sex for the three canonical generations
    for g in ["mex_G1", "mex_G2", "mex_G3plus"]:
        for sex, lab in ((1, "men"), (2, "women")):
            f = groups[g][groups[g].A_SEX == sex]
            add(f"spouse_mexican_origin_{lab}", g, f, f.sp_mex_origin)
            add(f"spouse_non_hispanic_{lab}", g, f, f.sp_non_hisp)

    # equal-SES: excess endogamy at a common covariate profile (pooled Mexican-origin married means)
    mex = married[married.gen.isin(["mex_G1", "mex_G2", "mex_G3plus"])].copy()
    educ = pd.cut(mex.A_HGA, [0, 38, 39, 42, 43, 46], labels=False)
    agec = pd.cut(mex.A_AGE, [24, 34, 44, 54], labels=False)
    ctrl = pd.concat([pd.get_dummies(educ, prefix="e", drop_first=True, dtype=float),
                      pd.get_dummies(agec, prefix="a", drop_first=True, dtype=float),
                      pd.get_dummies(mex.GESTFIPS, prefix="st", drop_first=True, dtype=float),
                      pd.get_dummies(mex.year, prefix="y", drop_first=True, dtype=float),
                      pd.DataFrame({"female": mex.A_SEX.eq(2).astype(float)}, index=mex.index)], axis=1)
    ctrl = ctrl.loc[:, ctrl.std() > 0]
    w = mex[WCOLS].to_numpy(float)
    C = ctrl.to_numpy(float)
    gens = ["mex_G1", "mex_G2", "mex_G3plus"]
    G = np.column_stack([(mex.gen == g).to_numpy(float) for g in gens])
    for outcome, yv in (("spouse_mexican_origin", mex.sp_mex_origin.to_numpy(float)),
                        ("spouse_non_hispanic", mex.sp_non_hisp.to_numpy(float)),
                        ("excess_mexican_spouse_over_random", mex.excess_mex.to_numpy(float))):
        for spec, cols in (("age_sex_educ_year", [c for c in ctrl.columns if not c.startswith("st_")]),
                           ("age_sex_educ_state_year", list(ctrl.columns))):
            Cs = ctrl[cols].to_numpy(float)
            coef = np.empty((R, 3))
            for r in range(R):
                mean = (Cs * w[:, r][:, None]).sum(0) / w[:, r].sum()
                X = np.column_stack([G, Cs - mean])
                xw = X * w[:, r][:, None]
                coef[r] = np.linalg.solve(xw.T @ X, xw.T @ yv)[:3]
            for j, g in enumerate(gens):
                rows.append({"source": "CPS ASEC 2022-2025", "measure": outcome, "generation": g,
                             "n": int(G[:, j].sum()), "estimate": coef[0, j], "se": se_sdr(coef[:, j]),
                             "se_conservative": float("nan"), "adjustment": spec + " at pooled Mexican-origin profile"})
        print(f"  ✓ adjusted {outcome}", flush=True)

    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "intermarriage.csv", index=False, float_format="%.6g", lineterminator="\n")

    # ---- children of mixed couples
    kids = d[(d.A_AGE < 18)].copy()
    par = {}
    for slot in (1, 2):
        idx = pos.reindex(pd.MultiIndex.from_arrays([kids.year, kids.PH_SEQ, kids[f"PEPAR{slot}"]])).to_numpy()
        par[slot] = idx
    two = ~np.isnan(par[1]) & ~np.isnan(par[2])
    kids = kids[two].copy()
    p1, p2 = d.iloc[par[1][two].astype(int)], d.iloc[par[2][two].astype(int)]
    bio = (kids.PEPAR1TYP.eq(1) & kids.PEPAR2TYP.eq(1)).to_numpy()
    kids["both_bio"] = bio
    a_mex, b_mex = p1.mex_origin.to_numpy(), p2.mex_origin.to_numpy()
    a_nh, b_nh = p1.non_hisp.to_numpy(), p2.non_hisp.to_numpy()
    a_oh, b_oh = p1.other_hisp.to_numpy(), p2.other_hisp.to_numpy()
    mixed = (a_mex & b_nh) | (b_mex & a_nh)
    mex_par = np.where(a_mex, 0, 1)
    pm = [p1, p2]
    kids["mex_parent_gen"] = np.where(mex_par == 0, p1.gen.to_numpy(), p2.gen.to_numpy())
    kids["mex_parent_sex"] = np.where(mex_par == 0, p1.A_SEX.to_numpy(), p2.A_SEX.to_numpy())
    kids["mex_parent_gp"] = np.where(mex_par == 0, p1.gp_split.to_numpy(), p2.gp_split.to_numpy())
    kids["nh_parent_white"] = np.where(mex_par == 0, p2.nh_white.to_numpy(), p1.nh_white.to_numpy())
    kids["couple"] = np.select([a_mex & b_mex, mixed, (a_mex & b_oh) | (b_mex & a_oh)],
                               ["both_mexican_origin", "mexican_x_non_hispanic", "mexican_x_other_hispanic"], "")
    kids["id_hispanic"] = kids.PEHSPNON.eq(1).to_numpy()
    kids["id_mexican"] = (kids.PEHSPNON.eq(1) & kids.PRDTHSP.eq(1)).to_numpy()
    kid_rows = []

    def kadd(label, gen, f):
        for m in ("id_hispanic", "id_mexican"):
            theta, se, cons = estimate(f, f[m])
            kid_rows.append({"source": "CPS ASEC 2022-2025", "measure": f"child_{m}", "generation": gen,
                             "n": len(f), "estimate": theta[0], "se": se, "se_conservative": cons,
                             "adjustment": label})

    for bio_only in (True, False):
        k = kids[kids.both_bio] if bio_only else kids
        tag = "both parents biological" if bio_only else "any parent type"
        for couple in ("both_mexican_origin", "mexican_x_other_hispanic", "mexican_x_non_hispanic"):
            kadd(f"{couple}; {tag}", "all", k[k.couple == couple])
        mixedk = k[k.couple == "mexican_x_non_hispanic"]
        for g in ["mex_G1", "mex_G2", "mex_G3plus"]:
            f = mixedk[mixedk.mex_parent_gen == g]
            kadd(f"mexican_x_non_hispanic, Mexican parent's generation; {tag}", g, f)
            if bio_only:
                for sex, lab in ((1, "father"), (2, "mother")):
                    kadd(f"mexican_x_non_hispanic, Mexican parent is the {lab}; {tag}", g,
                         f[f.mex_parent_sex == sex])
                kadd(f"mexican_x_non_hispanic, non-Hispanic parent is NH white; {tag}", g, f[f.nh_parent_white])
        if bio_only:
            for g in ["mex_G3_observed", "mex_G4plus_observed"]:
                kadd(f"mexican_x_non_hispanic, Mexican parent's generation (grandparent linkage); {tag}", g,
                     mixedk[mixedk.mex_parent_gp == g])
            for g in ["mex_G1", "mex_G2", "mex_G3plus"]:
                kadd(f"both_mexican_origin, both parents this generation; {tag}", g,
                     k[(k.couple == "both_mexican_origin") & (k.mex_parent_gen == g)])
    kout = pd.DataFrame(kid_rows)
    kout.to_csv(DERIVED / "child_identification.csv", index=False, float_format="%.6g", lineterminator="\n")

    gate_lines = [f"{k}: {v}" for k, v in gate.items()]
    (DERIVED / "gate_spouse_linkage.txt").write_text("\n".join(gate_lines) + "\n")
    print("\n".join(gate_lines))
    show = out[out.adjustment == "raw"].pivot_table(index="generation", columns="measure", values="estimate")
    print((100 * show).round(1).T.to_string())
    print(kout[["adjustment", "generation", "measure", "n", "estimate", "se"]].to_string())


if __name__ == "__main__":
    sys.exit(main())
