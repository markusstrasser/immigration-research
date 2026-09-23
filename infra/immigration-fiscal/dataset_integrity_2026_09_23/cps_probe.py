"""CPS ASEC 2025 integrity probe for the account's population spine.

Reads the pinned public-use ZIP the complete account uses and reports, by the account's own
group masks: allocation (imputation) rates for nativity, parents' birthplace, citizenship, year of
entry, Hispanic origin, race and age; nonspecific parent-birthplace codes; code contradictions;
sentinel and top-code/swap exposure in earnings; whole-supplement imputation (FL_665); weight totals.
Writes derived/cps_*.csv. Run from the repository root.
"""
from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
ZIP = ROOT / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
OUT = HERE / "derived"
US_AREA = [57, 60, 66, 69, 73, 78]
NONSPECIFIC = [166, 249, 343, 374, 399, 462, 555]  # "not specified" regions + Elsewhere

COLS = ["PH_SEQ", "PPPOS", "A_AGE", "AXAGE", "PRPERTYP", "PRCITSHP", "PRCITFLG", "PENATVTY",
        "PXNATVTY", "PEFNTVTY", "PXFNTVTY", "PEMNTVTY", "PXMNTVTY", "PEINUSYR", "PXINUSYR",
        "PEHSPNON", "PXHSPNON", "PRDTHSP", "PRDTRACE", "PXRACE1", "PEPAR1", "PEPAR2",
        "MARSUPWT", "FL_665", "ERN_VAL", "WS_VAL", "WSAL_VAL", "PEARNVAL", "SE_VAL",
        "FICA", "FEDTAX_AC", "STATETAX_A", "I_ERNVAL", "I_WSVAL", "PRWERNAL"]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def groups(d: pd.DataFrame) -> dict[str, pd.Series]:
    """The account's masks (extend_ledger.py / all_age_ledger analyze.py), civilian domain."""
    civ = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    g = {
        "mexico_born": d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303),
        "mexican_second_gen": native & parent_mex,
        "mexican_third_plus_selfid": native & parents_us & d.PRDTHSP.eq(1),
        "third_plus_nh_white": native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1),
        "all_native": native,
    }
    g["union"] = g["mexico_born"] | g["mexican_second_gen"] | g["mexican_third_plus_selfid"]
    return {k: (v & civ) for k, v in g.items()}


def allocated(flag: pd.Series) -> pd.Series:
    """Codes 10-43 (edited, longitudinal or allocated); 0/-1 = not allocated; 1-3 = blank kept."""
    return flag.between(10, 43)


def main() -> None:
    if sha(ZIP) != SHA:
        raise SystemExit("[BLOCKED] CPS ZIP hash differs from the account's pin")
    OUT.mkdir(exist_ok=True)
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS)
    w = d.MARSUPWT / 100
    g = groups(d)
    res: dict = {"records": len(d), "weight_total": float(w.sum())}

    # 1. Allocation rates by group, weighted, per item.
    items = {"nativity": "PXNATVTY", "father_birthplace": "PXFNTVTY", "mother_birthplace": "PXMNTVTY",
             "citizenship": "PRCITFLG", "year_of_entry": "PXINUSYR", "hispanic_origin": "PXHSPNON",
             "race": "PXRACE1", "age": "AXAGE"}
    rows = []
    for gname, m in g.items():
        for item, flag in items.items():
            f = d[flag]
            a = (f.eq(4) if flag == "AXAGE" else allocated(f)) & m
            longi = f.between(20, 23) & m if flag != "AXAGE" else pd.Series(False, index=d.index)
            hot = f.between(30, 43) & m if flag != "AXAGE" else a
            blank_kept = f.between(1, 3) & m if flag != "AXAGE" else pd.Series(False, index=d.index)
            rows.append(dict(group=gname, item=item, pop_m=w[m].sum() / 1e6, n=int(m.sum()),
                             any_change_pct=100 * w[a].sum() / w[m].sum(),
                             longitudinal_pct=100 * w[longi].sum() / w[m].sum(),
                             hotdeck_pct=100 * w[hot].sum() / w[m].sum(),
                             blank_kept_pct=100 * w[blank_kept].sum() / w[m].sum()))
        fl = d.FL_665.ne(1) & m
        rows.append(dict(group=gname, item="whole_asec_imputed_FL665", pop_m=w[m].sum() / 1e6,
                         n=int(m.sum()), any_change_pct=100 * w[fl].sum() / w[m].sum(),
                         longitudinal_pct=np.nan, hotdeck_pct=100 * w[fl].sum() / w[m].sum(),
                         blank_kept_pct=np.nan))
    alloc = pd.DataFrame(rows)
    alloc.to_csv(OUT / "cps_allocation_by_group.csv", index=False)
    res["fl665_values"] = d.FL_665.value_counts().sort_index().to_dict()

    # 2. Parents' birthplace for adults: co-resident parent vs not, allocation and group flow.
    adult = d.A_AGE.ge(18) & (d.PRPERTYP.eq(2))
    no_par = d.PEPAR1.le(0) & d.PEPAR2.le(0)
    par_alloc = allocated(d.PXFNTVTY) | allocated(d.PXMNTVTY)
    rows = []
    for gname in ["union", "mexico_born", "mexican_second_gen", "mexican_third_plus_selfid",
                  "third_plus_nh_white", "all_native"]:
        for lab, sub in [("adult_no_parent_in_hh", adult & no_par), ("adult_parent_in_hh", adult & ~no_par),
                         ("child_0_17", d.A_AGE.lt(18))]:
            m = g[gname] & sub
            rows.append(dict(group=gname, cut=lab, pop_m=w[m].sum() / 1e6,
                             parent_birthplace_allocated_pct=100 * w[m & par_alloc].sum() / w[m].sum(),
                             hotdeck_pct=100 * w[m & (d.PXFNTVTY.between(30, 43) | d.PXMNTVTY.between(30, 43))].sum() / w[m].sum()))
    pd.DataFrame(rows).to_csv(OUT / "cps_parent_birthplace_allocation.csv", index=False)

    # Where do records with an allocated parent birthplace land? (natives only)
    nat = d.PRCITSHP.isin([1, 2, 3]) & (d.PRPERTYP.eq(2) | d.A_AGE.lt(15))
    flows = {}
    for gname in ["mexican_second_gen", "mexican_third_plus_selfid"]:
        m = g[gname]
        flows[gname] = dict(pop_m=float(w[m].sum() / 1e6),
                            parent_alloc_m=float(w[m & par_alloc].sum() / 1e6),
                            parent_alloc_hotdeck_m=float(w[m & (d.PXFNTVTY.between(30, 43) | d.PXMNTVTY.between(30, 43))].sum() / 1e6))
    # Self-ID Mexican natives in neither G2 nor G3+: what parent codes?
    selfid = nat & d.PRDTHSP.eq(1)
    gap = selfid & ~g["mexican_second_gen"] & ~g["mexican_third_plus_selfid"]
    par_codes = pd.concat([d.loc[gap, "PEFNTVTY"], d.loc[gap, "PEMNTVTY"]])
    par_w = pd.concat([w[gap], w[gap]])
    top = par_w.groupby(par_codes).sum().sort_values(ascending=False) / 1e6
    flows["selfid_mexican_native_in_neither"] = dict(
        pop_m=float(w[gap].sum() / 1e6),
        with_nonspecific_parent_code_m=float(w[gap & (d.PEFNTVTY.isin(NONSPECIFIC) | d.PEMNTVTY.isin(NONSPECIFIC))].sum() / 1e6),
        with_allocated_parent_m=float(w[gap & par_alloc].sum() / 1e6),
        top_parent_codes_person_m={int(k): round(float(v), 3) for k, v in top.head(8).items()})
    res["parent_flows"] = flows
    res["parent_code_min"] = int(min(d.PEFNTVTY.min(), d.PEMNTVTY.min()))
    res["parent_code_nonpositive_n"] = int((d.PEFNTVTY.le(0) | d.PEMNTVTY.le(0)).sum())
    res["nonspecific_parent_code_weighted_m_all"] = float(w[d.PEFNTVTY.isin(NONSPECIFIC) | d.PEMNTVTY.isin(NONSPECIFIC)].sum() / 1e6)

    # 3. Code contradictions and sentinels.
    fb = d.PRCITSHP.isin([4, 5])
    res["contradictions"] = {
        "PENATVTY_US_area_but_foreign_born_n": int((fb & d.PENATVTY.isin(US_AREA)).sum()),
        "PENATVTY_303_but_PRCITSHP_1or2_n": int((d.PENATVTY.eq(303) & d.PRCITSHP.isin([1, 2])).sum()),
        "PENATVTY_303_PRCITSHP_3_weighted_m": float(w[d.PENATVTY.eq(303) & d.PRCITSHP.eq(3)].sum() / 1e6),
        "PRCITSHP_1_but_PENATVTY_not_57_n": int((d.PRCITSHP.eq(1) & d.PENATVTY.ne(57)).sum()),
        "foreign_born_PEINUSYR_0_n": int((fb & d.PEINUSYR.eq(0)).sum()),
        "PRDTHSP_1_but_PEHSPNON_2_n": int((d.PRDTHSP.eq(1) & d.PEHSPNON.eq(2)).sum()),
        "PEHSPNON_1_but_PRDTHSP_0_n": int((d.PEHSPNON.eq(1) & d.PRDTHSP.eq(0)).sum()),
        "mexico_born_not_hispanic_weighted_m": float(w[g["mexico_born"] & d.PEHSPNON.eq(2)].sum() / 1e6),
        "mexico_born_hispanic_not_mexican_weighted_m": float(w[g["mexico_born"] & d.PEHSPNON.eq(1) & d.PRDTHSP.ne(1)].sum() / 1e6),
        "second_gen_not_hispanic_weighted_m": float(w[g["mexican_second_gen"] & d.PEHSPNON.eq(2)].sum() / 1e6),
        "second_gen_hispanic_not_mexican_weighted_m": float(w[g["mexican_second_gen"] & d.PEHSPNON.eq(1) & d.PRDTHSP.ne(1)].sum() / 1e6),
        "age_max": int(d.A_AGE.max()), "age_85_weighted_m": float(w[d.A_AGE.eq(85)].sum() / 1e6),
        "age_80_weighted_m": float(w[d.A_AGE.eq(80)].sum() / 1e6),
    }
    sent = {}
    for c in ["ERN_VAL", "WS_VAL", "WSAL_VAL", "PEARNVAL", "SE_VAL", "FICA", "FEDTAX_AC", "STATETAX_A"]:
        v = d[c]
        sent[c] = dict(min=float(v.min()), max=float(v.max()),
                       n_9999999=int(v.isin([9999999, 99999999, 999999]).sum()),
                       n_negative=int((v < 0).sum()))
    res["sentinels"] = sent

    # 4. Top-code swap exposure: share of group wage dollars in records at/above thresholds.
    rows = []
    swapped = d.ERN_VAL.ge(458_000) | d.WS_VAL.ge(90_000) | d.SE_VAL.ge(130_000)
    for gname, m in g.items():
        tot = (w * d.WSAL_VAL)[m].sum()
        above = (w * d.WSAL_VAL)[m & swapped].sum()
        ern_imp = (w * d.WSAL_VAL)[m & d.I_ERNVAL.gt(0)].sum()
        adults = m & d.A_AGE.ge(18)
        rows.append(dict(group=gname, wage_bn=tot / 1e9, swap_zone_wage_bn=above / 1e9,
                         swap_zone_share_pct=100 * above / tot if tot else np.nan,
                         persons_in_swap_zone_pct=100 * w[m & swapped].sum() / w[m].sum(),
                         wage_dollars_on_imputed_earnings_pct=100 * ern_imp / tot if tot else np.nan,
                         adults_earnings_imputed_pct=100 * w[adults & d.I_ERNVAL.gt(0)].sum() / w[adults].sum(),
                         hi_tax_on_swap_zone_above_cap_bn=0.0145 * ((w * (d.WSAL_VAL - 168_600).clip(lower=0))[m & swapped].sum()) / 1e9))
    pd.DataFrame(rows).to_csv(OUT / "cps_topcode_exposure.csv", index=False)

    # 5. Weights: totals and Hispanic totals (civilian noninstitutional incl. armed forces in hh).
    res["weights"] = {
        "all_persons_m": float(w.sum() / 1e6),
        "civilian_domain_m": float(w[d.PRPERTYP.eq(2) | d.A_AGE.lt(15)].sum() / 1e6),
        "armed_forces_adults_m": float(w[d.PRPERTYP.eq(3)].sum() / 1e6),
        "hispanic_m": float(w[d.PEHSPNON.eq(1)].sum() / 1e6),
        "mexican_selfid_all_m": float(w[d.PRDTHSP.eq(1)].sum() / 1e6),
        "mexican_share_of_hispanic_pct": float(100 * w[d.PRDTHSP.eq(1)].sum() / w[d.PEHSPNON.eq(1)].sum()),
        "hispanic_detail_distribution_m": {int(k): round(float(v) / 1e6, 3) for k, v in w[d.PEHSPNON.eq(1)].groupby(d.PRDTHSP[d.PEHSPNON.eq(1)]).sum().items()},
        "foreign_born_m": float(w[fb].sum() / 1e6),
        "mexico_born_any_cit_m": float(w[d.PENATVTY.eq(303)].sum() / 1e6),
        "zero_weight_records": int((d.MARSUPWT <= 0).sum()),
        "group_pop_m": {k: round(float(w[v].sum() / 1e6), 4) for k, v in g.items()},
    }
    # Mexico-born by entry band: recent arrivals share (unauthorized undercount exposure).
    mb = g["mexico_born"]
    res["mexico_born_entry_2020_2024_pct"] = float(100 * w[mb & d.PEINUSYR.isin([27, 28])].sum() / w[mb].sum())
    res["foreign_born_entry_2020_2024_pct"] = float(100 * w[fb & d.PEINUSYR.isin([27, 28])].sum() / w[fb].sum())
    (OUT / "cps_probe.json").write_text(json.dumps(res, indent=1, default=float))
    print(json.dumps(res, indent=1, default=float))
    pd.set_option("display.width", 200)
    print(alloc.round(2).to_string())


if __name__ == "__main__":
    main()
