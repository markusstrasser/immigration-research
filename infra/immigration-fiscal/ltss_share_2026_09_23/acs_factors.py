"""ACS 2024 shares and Hispanic-to-union translation factors for Medicaid LTSS populations.

The union is approximated in the ACS as Mexican origin (HISP = 02) or Mexico-born (POBP = 303);
the ACS has no parental birthplace, so second-generation members who do not report Mexican
origin are missed (small). For each LTSS proxy population the script reports the union's share,
the Hispanic share, and the union-per-Hispanic ratio `f` that turns a Hispanic dollar share into
a union dollar share, nationally and by state:
  inst65     institutional group quarters (RELSHIPP 37), age 65+  -> nursing facilities
  inst65_mcd the same, reporting Medicaid (HINS4 = 1)              -> check on TAF's NF users
  comm_adl   community residents on Medicaid (HINS4 = 1) with a self-care or independent-living
             difficulty (DDRS or DOUT)                            -> HCBS
  comm_adl_u65 / comm_adl_65  the same split at 65                -> HCBS age variants
  comm_cog_u65  community residents under 65 on Medicaid with a cognitive difficulty (DREM)
                                                                   -> ICF/IID, mental-health facilities
  all65, all  every resident 65+, every resident                  -> fallbacks
Also reproduces the medical-ethnicity lane's 65+ institutional ceiling (union / (natives +
Mexico-born) = 3.20%) and gives the full-denominator share, with the generic "Other Hispanic"
(HISP 24) excess spread over named origins as a variant (integrity audit acs.md F4).
Replicate-weight SEs (80 successive-difference replicates); GQ-based SEs should be read as
about sqrt(2) too small (audit acs.md F1).
Writes derived/acs_shares_2024.csv and derived/acs_state_factors_2024.csv.
Run from the repo root after acs_extract_ltss.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ltss_share_2026_09_23/acs_factors.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REP = [f"PWGTP{i}" for i in range(1, 81)]


def load():
    d = pd.read_parquet(HERE / "_cache/acs2024_ltss.parquet")
    r = pd.read_parquet(HERE / "_cache/acs2024_ltss_rep.parquet")
    d = d.merge(r, on=["SERIALNO", "SPORDER"], how="left", validate="one_to_one")
    d["union"] = d.HISP.eq(2) | d.POBP.eq(303)
    d["hisp"] = d.HISP.gt(1)
    d["mex"] = d.HISP.eq(2)
    d["mexborn"] = d.POBP.eq(303)
    d["generic"] = d.HISP.eq(24)
    inst, comm = d.RELSHIPP.eq(37), ~d.RELSHIPP.eq(37)
    adl = d.HINS4.eq(1) & (d.DDRS.eq(1) | d.DOUT.eq(1))
    pops = {"inst65": inst & d.AGEP.ge(65),
            "inst65_mcd": inst & d.AGEP.ge(65) & d.HINS4.eq(1),
            "comm_adl": comm & adl,
            "comm_adl_u65": comm & adl & d.AGEP.lt(65),
            "comm_adl_65": comm & adl & d.AGEP.ge(65),
            "comm_cog_u65": comm & d.HINS4.eq(1) & d.DREM.eq(1) & d.AGEP.lt(65),
            "all65": d.AGEP.ge(65),
            "all": pd.Series(True, index=d.index)}
    return d, pops


def shares(d, mask, weights):
    """Union, Hispanic and union-per-Hispanic among `mask`, for each weight column."""
    w = d.loc[mask, weights].to_numpy(float)
    sub = d.loc[mask]
    tot = w.sum(axis=0)
    out = {"persons": tot}
    for g in ("union", "hisp", "mex", "mexborn", "generic"):
        out[g] = (w * sub[g].to_numpy()[:, None]).sum(axis=0) / tot
    out["f_union_per_hisp"] = out["union"] / out["hisp"]
    return out


def main():
    d, pops = load()
    weights = ["PWGTP"] + REP
    rows = []
    for name, mask in pops.items():
        has_rep = name not in ("all", "comm_cog_u65") or d.loc[mask, REP[0]].notna().all()
        w = weights if has_rep and d.loc[mask, REP[0]].notna().all() else ["PWGTP"]
        s = shares(d, mask, w)
        for k, v in s.items():
            se = float(np.sqrt(4 / 80 * ((v[1:] - v[0]) ** 2).sum())) if len(w) > 1 else np.nan
            rows.append(dict(population=name, quantity=k, value=float(v[0]), se=se, records=int(mask.sum())))
    # Reproduce the medical-ethnicity lane's ceiling: union = Mexico-born + US-born HISP 02, 65+,
    # institutional; denominator = all natives + Mexico-born (other foreign-born omitted).
    m = pops["inst65"]
    wt = d.PWGTP
    med_union = float(wt[m & (d.mexborn | (d.NATIVITY.eq(1) & d.mex))].sum())
    med_denom = float(wt[m & (d.NATIVITY.eq(1) | d.mexborn)].sum())
    full_denom = float(wt[m].sum())
    rows += [dict(population="inst65", quantity="med_lane_union_persons", value=med_union),
             dict(population="inst65", quantity="med_lane_denominator_persons", value=med_denom),
             dict(population="inst65", quantity="med_lane_share_ceiling", value=med_union / med_denom),
             dict(population="inst65", quantity="med_lane_union_over_full_denominator", value=med_union / full_denom)]
    # Generic "Other Hispanic" excess among 65+ institutional residents, spread over named origins
    # in proportion to their institutional counts (audit acs.md F4 method), for the union.
    a65 = pops["all65"]
    named = d.hisp & ~(d.generic & ~d.mexborn)
    generic = d.generic & ~d.mexborn
    rate_named = wt[m & named].sum() / wt[a65 & named].sum()
    excess = max(0.0, wt[m & generic].sum() - rate_named * wt[a65 & generic].sum())
    u_inst = wt[m & d.union].sum()
    u_adj = u_inst + excess * wt[m & d.union & named].sum() / wt[m & named].sum()
    rows += [dict(population="inst65", quantity="generic_hisp_excess_persons", value=float(excess)),
             dict(population="inst65", quantity="union_share_generic_spread", value=float(u_adj / full_denom)),
             dict(population="inst65", quantity="f_union_per_hisp_generic_spread",
                  value=float(u_adj / wt[m & d.hisp].sum()))]
    out = pd.DataFrame(rows)
    (HERE / "derived").mkdir(exist_ok=True)
    out.to_csv(HERE / "derived/acs_shares_2024.csv", index=False)
    pd.set_option("display.width", 200)
    print(out.pivot_table(index="quantity", columns="population", values="value").round(4).to_string())

    # State factors: union-per-Hispanic by population, with unweighted Hispanic record counts.
    st = []
    for name in ("inst65", "inst65_mcd", "comm_adl", "comm_adl_u65", "comm_adl_65", "comm_cog_u65", "all65", "all"):
        sub = d[pops[name]]
        g = sub.assign(u=sub.union * sub.PWGTP, h=sub.hisp * sub.PWGTP, n=sub.hisp.astype(int)) \
            .groupby("STATE")[["u", "h", "n", "PWGTP"]].sum()
        g["population"] = name
        g["f"] = g.u / g.h
        g["hisp_share"] = g.h / g.PWGTP
        g["union_share"] = g.u / g.PWGTP
        st.append(g.reset_index().rename(columns={"u": "union_persons", "h": "hisp_persons",
                                                  "n": "hisp_records", "PWGTP": "persons"}))
    st = pd.concat(st, ignore_index=True)
    st.to_csv(HERE / "derived/acs_state_factors_2024.csv", index=False)
    print(st[st.STATE.isin([6, 48, 36, 12, 4, 17, 35, 34])].pivot(index="STATE", columns="population", values="f")
          .round(3).to_string())


if __name__ == "__main__":
    main()
