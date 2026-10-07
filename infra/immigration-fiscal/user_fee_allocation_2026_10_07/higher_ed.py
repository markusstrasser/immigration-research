"""Public higher education: the group's share of gross cost (use) and its share of tuition paid.

The account charges public higher education at NIPA consumption, gross output less sales, of which S&L tuition and
related educational charges are $103.911bn in 2024 (T3.10.5 line 58). If the group's share of tuition paid (s_R)
falls short of its share of the gross cost it uses (s_U), the account under-charges it (s_U - s_R) x R.

Both shares come from IPEDS institution data (FY2023 finance, fall 2023 enrollment by race), with each
institution's Hispanic students turned into Mexican-origin students at the ACS 2024 share of Hispanic public college
students who are Mexican in the institution's state and level (acs_college.py):
  - use: s_U = sum_u m_u x Cost_u / sum_u Cost_u, with m_u the group's share of the unit's FTE, graduate FTE weighted
    by a cost ratio c to undergraduate FTE (arms 1, 2 central, 3);
  - fees: s_R = sum_u f_u x Fee_u / sum_u Fee_u, with f_u the group's share of the unit's tuition: its FTE share, with
    graduate FTE weighted by the unit's graduate-to-undergraduate in-state tuition ratio, and undergraduates adjusted
    for residency. Out-of-state and foreign students pay kappa_u times the in-state rate (IC2023_AY); a share o_u of
    the unit's first-time undergraduates come from out of state or abroad (EF2022C, a required year). The group's
    out-of-state rate is theta x o_u (theta 0: all in-state; 0.5 central; 1: as everyone else, no adjustment).
Finance units: parent/child finance reporting (FLAGS2023 PRCH_F 2, IDX_F) moves a child's enrollment to its parent.
Public institutions reporting under FASB (no F1A record) and outlying areas are outside the universe; the FTE they
hold is reported.

Writes derived/higher_ed_shares.csv (every arm), derived/higher_ed.json (central, totals, coverage, state table).
Run from the repository root after acs_college.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/higher_ed.py
"""
import hashlib
import itertools
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
STAGE = REPO / "sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/x"
CACHE = REPO / "infra/immigration-fiscal/affirmative_action_cost_2026_09_24/_cache/ipeds"
OUT = HERE / "derived"
PINS = {
    CACHE / "HD2023.csv": "d779a92d637e122c90009112e284ab5c75bc2b3d26774a29746800f522aace0f",
    CACHE / "ef2023a.csv": "527ba4696abe0168e086fbc437587008fbfa89fbf1062f95fc3d33652977a2ea",
}
ZIPS = {   # the staged archives (ACQUIRED.md); the extracted CSVs are checked against their members
    "f2223_f1a.csv": "beabdb0384f000a2fa487e7083512f880013c897d8e10bab9682f4c836687de9",
    "ic2023_ay.csv": "42d3ee39a107d69b6da02df2ffa934ebe3bb76657568fb9efb7027b6ce0d69ee",
    "ef2022c_rv.csv": "0ba1829cb0cb7fc775c8b7e7cca37eb74432ab07be25a24ba1bfae3db6509792",
    "Flags2023.csv": "df763ac04b15821bbcaa1dac238cbea9c2d88a5ae1b3532e2d1cd90489c8e3d3",
}
ARCHIVE = {"f2223_f1a.csv": "F2223_F1A.zip", "ic2023_ay.csv": "IC2023_AY.zip", "ef2022c_rv.csv": "EF2022C.zip",
           "Flags2023.csv": "FLAGS2023.zip"}
NIPA_TUITION_2024_BN = 103.911       # T3.10.5 line 58, pinned Section3All (sha 69b5c7ae...)
# IPEDS FTE convention for part-time students at public institutions (EF FTE estimate): undergraduates at
# four-year 0.403543, at two-year and less 0.335737; graduates 0.361702.
PT_FACTOR = {("UG", 4): 0.403543, ("UG", 2): 0.335737, ("UG", 1): 0.335737, ("GR", 4): 0.361702}
COSTS = {
    "education_and_related": ["F1C011", "F1C051", "F1C061", "F1C071"],
    "all_less_hospital_auxiliary_aid": "F1C191 - F1C121 - F1C111 - F1C131 - F1C101",
    "all_less_hospital_aid": "F1C191 - F1C121 - F1C131 - F1C101",
}
FEES = {
    "net_tuition": ["F1B01"],
    "net_tuition_plus_pell": ["F1B01", "F1E01"],
    "gross_tuition": ["F1B01", "F1E08"],
    "net_tuition_plus_auxiliary": ["F1B01", "F1B05"],
}
# NPSAS:20 First Look (NCES 2023-466), tables A-5 and A-6, all undergraduates: Pell receipt 49.5% Hispanic vs 40.2%
# all, average award $4,200 vs $4,100 -> Pell dollars per student 1.26x. All sectors: an upper end for the
# within-institution intensity, which excludes the part due to where Hispanic students enroll. The central takes the
# midpoint of 1 and that ratio [ASSUMPTION].
PELL_HISPANIC_RATIO = (0.495 * 4200) / (0.402 * 4100)
PELL = {"none": 1.0, "mid": (1.0 + PELL_HISPANIC_RATIO) / 2, "npsas": PELL_HISPANIC_RATIO}
CENTRAL = dict(cost="education_and_related", fee="net_tuition_plus_pell", grad_cost=2.0, theta=0.5, pell_intensity="mid")
ARMS = dict(cost=list(COSTS), fee=list(FEES), grad_cost=[1.0, 2.0, 3.0], theta=[0.0, 0.5, 1.0],
            pell_intensity=list(PELL))


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def read(path, **kw):
    d = pd.read_csv(path, encoding="latin-1", low_memory=False, **kw)
    d.columns = [c.replace("ï»¿", "").replace("﻿", "").strip() for c in d.columns]
    return d


def num(d, cols):
    for c in cols:
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0.0)
    return d


def verify():
    for path, want in PINS.items():
        if sha(path) != want:
            raise SystemExit(f"[BLOCKED] {path} is not the pinned file")
    import zipfile
    for name, want in ZIPS.items():
        z = STAGE.parent / ARCHIVE[name]
        if sha(z) != want:
            raise SystemExit(f"[BLOCKED] {z} is not the archive ACQUIRED.md pins")
        with zipfile.ZipFile(z) as zz:
            if zz.read(name) != (STAGE / name).read_bytes():
                raise SystemExit(f"[BLOCKED] {STAGE / name} differs from its archive member")


def expr(f, spec):
    if isinstance(spec, list):
        return f[spec].sum(axis=1)
    terms = spec.replace("-", " - ").split()
    total, sign = 0.0, 1.0
    for t in terms:
        if t == "-":
            sign = -1.0
        else:
            total = total + sign * f[t]
            sign = 1.0
    return total


def load():
    hd = read(CACHE / "HD2023.csv")[["UNITID", "INSTNM", "STABBR", "FIPS", "SECTOR", "CONTROL", "ICLEVEL"]]
    pub = hd[hd.CONTROL.eq(1) & hd.FIPS.between(1, 56)].copy()
    fl = read(STAGE / "Flags2023.csv")[["UNITID", "PRCH_F", "IDX_F", "FORM_F"]]
    pub = pub.merge(fl, on="UNITID", how="left", validate="one_to_one")
    pub["finance_unit"] = np.where(pub.PRCH_F.eq(2), pub.IDX_F, pub.UNITID).astype(int)

    ef = read(CACHE / "ef2023a.csv")
    ef = num(ef, ["EFTOTLT", "EFHISPT", "EFNRALT"])
    lv = {22: ("UG", "FT"), 42: ("UG", "PT"), 32: ("GR", "FT"), 52: ("GR", "PT")}
    ef = ef[ef.EFALEVEL.isin(lv)].copy()
    ef["level"] = ef.EFALEVEL.map(lambda x: lv[x][0])
    ef["att"] = ef.EFALEVEL.map(lambda x: lv[x][1])
    ef = ef.merge(pub[["UNITID", "ICLEVEL", "STABBR", "FIPS", "finance_unit"]], on="UNITID", how="inner")
    lvl4 = ef.ICLEVEL.map({1: 4, 2: 2, 3: 1})
    factor = np.where(ef.att.eq("FT"), 1.0, [PT_FACTOR.get((l, 4 if l == "GR" else i), 0.335737)
                                               for l, i in zip(ef.level, lvl4)])
    ef["fte"] = ef.EFTOTLT * factor
    ef["fte_hisp"] = ef.EFHISPT * factor
    ef["fte_nra"] = ef.EFNRALT * factor

    acs = pd.read_csv(OUT / "acs_public_college_by_state.csv")
    acs["level"] = acs.level.map({"undergraduate": "UG", "graduate": "GR"})
    pooled = acs.groupby("STATE")[["hispanic", "hispanic_mexican", "records"]].sum()
    acs = acs.merge(pooled.rename(columns=lambda c: c + "_pooled"), left_on="STATE", right_index=True)
    # Thin graduate cells (fewer than 100 ACS records of public graduate students in the state) take the state's
    # pooled undergraduate-and-graduate ratio.
    acs["ratio"] = np.where(acs.records >= 100, acs.mexican_share_of_hispanic,
                            acs.hispanic_mexican_pooled / acs.hispanic_pooled)
    ef = ef.merge(acs[["STATE", "level", "ratio"]], left_on=["FIPS", "level"], right_on=["STATE", "level"],
                  how="left")
    if ef.ratio.isna().any():
        raise SystemExit("[BLOCKED] an institution's state and level have no ACS ratio")
    ef["fte_mex"] = ef.fte_hisp * ef.ratio

    f = read(STAGE / "f2223_f1a.csv")
    cols = sorted({c for v in list(COSTS.values()) + list(FEES.values()) for c in
                   (v if isinstance(v, list) else v.replace("-", " ").split())})
    f = num(f, cols)
    f = f[f.UNITID.isin(pub.UNITID)].copy()

    ic = read(STAGE / "ic2023_ay.csv")
    ic = num(ic, ["TUITION1", "FEE1", "TUITION2", "FEE2", "TUITION3", "FEE3", "TUITION6", "FEE6"])
    ic["t_in"] = ic.TUITION2 + ic.FEE2
    ic["t_out"] = ic.TUITION3 + ic.FEE3
    ic["t_gr_in"] = ic.TUITION6 + ic.FEE6

    res = read(STAGE / "ef2022c_rv.csv")
    res = num(res, ["EFRES01"])
    res = res.merge(pub[["UNITID", "FIPS"]], on="UNITID", how="inner")
    tot = res[res.LINE.eq(99)].set_index("UNITID").EFRES01
    instate = res[res.LINE.eq(res.FIPS)].set_index("UNITID").EFRES01
    unknown = res[res.LINE.isin([57, 98])].groupby("UNITID").EFRES01.sum()
    known = (tot - unknown.reindex(tot.index).fillna(0)).clip(lower=0)
    o = (1 - instate.reindex(tot.index).fillna(0) / known).where(known > 0)
    return pub, ef, f, ic, o.rename("o").clip(0, 1)


def units(pub, ef, f, ic, o):
    """One row per finance unit: FTE by level (all, Hispanic, group), costs, fees, residency and tuition ratios."""
    g = ef.groupby(["finance_unit", "level"])[["fte", "fte_hisp", "fte_mex", "fte_nra"]].sum().unstack(fill_value=0.0)
    g.columns = [f"{a}_{b}" for a, b in g.columns]
    for c in ["fte_UG", "fte_GR", "fte_hisp_UG", "fte_hisp_GR", "fte_mex_UG", "fte_mex_GR", "fte_nra_UG", "fte_nra_GR"]:
        if c not in g:
            g[c] = 0.0
    u = f.set_index("UNITID").join(g, how="left").fillna({c: 0.0 for c in g.columns})
    # Residency and tuition ratios: the unit's own, else an FTE-weighted mean of its members', else the
    # state-and-sector median, else the sector median.
    mem = pub[["UNITID", "finance_unit", "SECTOR", "STABBR"]].merge(ic[["UNITID", "t_in", "t_out", "t_gr_in"]],
                                                                     on="UNITID", how="left")
    mem = mem.merge(o.reset_index(), on="UNITID", how="left")
    w = ef.groupby("UNITID").fte.sum()
    mem["w"] = mem.UNITID.map(w).fillna(0.0)
    mem["kappa"] = (mem.t_out / mem.t_in).where((mem.t_in > 0) & (mem.t_out > 0))
    mem["grad_ratio"] = (mem.t_gr_in / mem.t_in).where((mem.t_in > 0) & (mem.t_gr_in > 0))
    for c in ["kappa", "grad_ratio", "o"]:
        med_ss = mem.groupby(["STABBR", "SECTOR"])[c].transform("median")
        med_s = mem.groupby("SECTOR")[c].transform("median")
        mem[c + "_filled"] = mem[c].fillna(med_ss).fillna(med_s)
    def wmean(x, c):
        ww = x.w.where(x.w > 0, 1.0)
        return float(np.average(x[c + "_filled"], weights=ww))
    agg = mem.groupby("finance_unit").apply(lambda x: pd.Series({c: wmean(x, c) for c in ["kappa", "grad_ratio", "o"]}),
                                            include_groups=False)
    sector = pub.set_index("UNITID").SECTOR
    u = u.join(agg, how="left")
    u["SECTOR"] = sector.reindex(u.index)
    u["STABBR"] = pub.set_index("UNITID").STABBR.reindex(u.index)
    for c in ["kappa", "grad_ratio", "o"]:
        u[c] = u[c].fillna(u.groupby("SECTOR")[c].transform("median"))
    u["kappa"] = u.kappa.clip(lower=1.0)
    return u


def shares(u, cost, fee, grad_cost, theta, pell_intensity):
    u = u[(u.fte_UG + u.fte_GR) > 0]   # system offices and units without students: no use to share out
    C = expr(u, COSTS[cost]).clip(lower=0)
    ug, gr = u.fte_UG, u.fte_GR
    den_c = ug + grad_cost * gr
    m_use = ((u.fte_mex_UG + grad_cost * u.fte_mex_GR) / den_c).where(den_c > 0, 0.0)
    # Fees: undergraduate tuition per FTE relative to the unit's average, for the group: in-state at its out-of-state
    # rate theta x o; graduates at the unit's graduate in-state rate, no residency adjustment.
    o, k = u.o, u.kappa
    avg = 1 - o + o * k
    grp = 1 - theta * o + theta * o * k
    r_ug = grp / avg
    gw = u.grad_ratio
    den_f = ug + gw * gr
    m_fee = ((u.fte_mex_UG * r_ug + gw * u.fte_mex_GR) / den_f).where(den_f > 0, 0.0)
    parts = FEES[fee]
    F = u[parts].sum(axis=1).clip(lower=0)
    group_fee = (u[parts[0]] * m_fee)
    if len(parts) > 1:
        extra = u[parts[1]]
        if parts[1] == "F1E01":   # Pell: undergraduates only, at the group's within-unit intensity
            m_pell = ((u.fte_mex_UG / ug).where(ug > 0, 0.0) * PELL[pell_intensity]).clip(upper=1.0)
            group_fee = group_fee + extra * m_pell
        else:
            group_fee = group_fee + extra * m_fee
    s_U = float((m_use * C).sum() / C.sum())
    s_R = float(group_fee.sum() / F.sum())
    return dict(cost=cost, fee=fee, grad_cost=grad_cost, theta=theta, pell_intensity=pell_intensity,
                cost_total_bn=float(C.sum()) / 1e9, fee_total_bn=float(F.sum()) / 1e9, s_U=s_U, s_R=s_R,
                rho=s_R / s_U)


def main():
    verify()
    pub, ef, f, ic, o = load()
    u = units(pub, ef, f, ic, o)
    # Coverage: FTE at public institutions in the 50 states and DC, inside and outside the F1A finance universe.
    fte_all = float(ef.fte.sum())
    fte_in = float(ef[ef.finance_unit.isin(u.index)].fte.sum())
    unmatched = ef[~ef.finance_unit.isin(u.index)].groupby("UNITID").fte.sum().sort_values(ascending=False)
    rows = []
    for cost, fee, gc, th, pi in itertools.product(*[ARMS[k] for k in ["cost", "fee", "grad_cost", "theta",
                                                                          "pell_intensity"]]):
        if pi != "none" and fee != "net_tuition_plus_pell":
            continue
        rows.append(shares(u, cost, fee, gc, th, pi))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "higher_ed_shares.csv", index=False, lineterminator="\n", float_format="%.6f")
    c = shares(u, CENTRAL["cost"], CENTRAL["fee"], CENTRAL["grad_cost"], CENTRAL["theta"], CENTRAL["pell_intensity"])
    # The group's share of Pell dollars at public institutions, for the Pell key beside the lane (not a fee term).
    uu = u[(u.fte_UG + u.fte_GR) > 0]
    m_ug = (uu.fte_mex_UG / uu.fte_UG).where(uu.fte_UG > 0, 0.0)
    pell_share = {k: float(((m_ug * v).clip(upper=1.0) * uu.F1E01).sum() / uu.F1E01.sum()) for k, v in PELL.items()}
    fte_ug, fte_gr = float(u.fte_UG.sum()), float(u.fte_GR.sum())
    enrol = dict(
        mexican_fte_share=float((u.fte_mex_UG.sum() + u.fte_mex_GR.sum()) / (fte_ug + fte_gr)),
        mexican_fte_share_ug=float(u.fte_mex_UG.sum() / fte_ug), mexican_fte_share_gr=float(u.fte_mex_GR.sum() / fte_gr),
        hispanic_fte_share_ug=float(u.fte_hisp_UG.sum() / fte_ug), hispanic_fte_share_gr=float(u.fte_hisp_GR.sum() / fte_gr),
        nonresident_alien_fte_share=float((u.fte_nra_UG.sum() + u.fte_nra_GR.sum()) / (fte_ug + fte_gr)),
        fte_ug=fte_ug, fte_gr=fte_gr)
    sect = u.assign(two_year=u.SECTOR.eq(4)).groupby("two_year").apply(lambda x: pd.Series(dict(
        units=len(x), fte=float(x.fte_UG.sum() + x.fte_GR.sum()),
        mexican_fte_share=float((x.fte_mex_UG.sum() + x.fte_mex_GR.sum()) / (x.fte_UG.sum() + x.fte_GR.sum())),
        er_cost_bn=float(expr(x, COSTS["education_and_related"]).sum()) / 1e9,
        net_tuition_bn=float(x.F1B01.sum()) / 1e9, pell_bn=float(x.F1E01.sum()) / 1e9)), include_groups=False)
    f = num(f, ["F1B02"])
    totals = {k: float(f[k].sum()) / 1e9 for k in ["F1B01", "F1B02", "F1B05", "F1B26", "F1E01", "F1E08", "F1C011",
                                                    "F1C191", "F1C121", "F1C111"]}
    state = u.groupby("STABBR").apply(lambda x: pd.Series(dict(
        fte=float(x.fte_UG.sum() + x.fte_GR.sum()), mexican_fte=float(x.fte_mex_UG.sum() + x.fte_mex_GR.sum()),
        er_cost_bn=float(expr(x, COSTS["education_and_related"]).sum()) / 1e9,
        net_tuition_bn=float(x.F1B01.sum()) / 1e9)), include_groups=False)
    state["er_cost_per_fte"] = state.er_cost_bn * 1e9 / state.fte
    state["net_tuition_per_fte"] = state.net_tuition_bn * 1e9 / state.fte
    top = state.sort_values("mexican_fte", ascending=False).head(8).round(4)
    out = dict(central=c, central_spec=CENTRAL, enrollment=enrol, pell_share_public=pell_share, pell_intensity=PELL, ipeds_public_f1a_totals_bn=totals,
               nipa_tuition_2024_bn=NIPA_TUITION_2024_BN, pell_hispanic_ratio=PELL_HISPANIC_RATIO,
               coverage=dict(finance_units=int(len(u)), fte_public_50_dc=fte_all, fte_in_f1a=fte_in,
                             fte_share_in_f1a=fte_in / fte_all,
                             largest_outside=[{"unitid": int(k), "fte": float(v)} for k, v in unmatched.head(5).items()]),
               by_sector={("two_year" if k else "four_year_and_other"): {kk: float(vv) for kk, vv in v.items()}
                          for k, v in sect.iterrows()},
               top_states={k: {kk: float(vv) for kk, vv in v.items()} for k, v in top.iterrows()},
               arms_range=dict(s_U=[float(t.s_U.min()), float(t.s_U.max())], s_R=[float(t.s_R.min()), float(t.s_R.max())],
                               rho=[float(t.rho.min()), float(t.rho.max())]))
    (OUT / "higher_ed.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ["central", "enrollment", "coverage", "arms_range", "by_sector"]}, indent=1))
    print(top.to_string())


if __name__ == "__main__":
    main()
