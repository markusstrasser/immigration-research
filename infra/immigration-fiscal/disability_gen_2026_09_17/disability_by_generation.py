#!/usr/bin/env python3
"""Disability prevalence and disability-income receipt by generation group.

CPS ASEC 2025 person file (income year 2024), 160-replicate SDR standard errors,
same generation coding as build/analyze_cps_fiscal_2025.py.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ZIP = Path("/Users/alien/Projects/immigration-research/infra/immigration-fiscal/"
           "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip")
OUT = Path("/Users/alien/Projects/immigration-research/infra/immigration-fiscal/"
           "disability_gen_2026_09_17")

DIS_ITEMS = ["PEDISEAR", "PEDISEYE", "PEDISREM", "PEDISPHY", "PEDISDRS", "PEDISOUT"]
COLS = (["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
         "PEMNTVTY", "PEHSPNON", "PRDTRACE", "PRDTHSP", "MARSUPWT", "PRDISFLG",
         "SS_YN", "SS_VAL", "RESNSS1", "RESNSS2", "RESNSSA", "SSI_YN", "SSI_VAL",
         "DIS_YN", "DIS_VAL1", "DIS_VAL2", "DIS_SC1", "DIS_SC2", "DIS_HP"] + DIS_ITEMS)
REPS = [f"pwwgt{i}" for i in range(161)]
US_AREA = [57, 60, 66, 69, 73, 78]
GROUPS = ["third_plus_nh_white", "mexican_second_gen", "mexican_third_plus_selfid",
          "mexico_born", "all_native", "all_foreign_born", "all_second_gen", "all_third_plus"]


def load() -> pd.DataFrame:
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS)
        r = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"))
    r = r.rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(r, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if d[REPS].isna().any().any():
        raise ValueError("Incomplete person-replicate join")
    delta = (d.MARSUPWT / 100 - d.pwwgt0).abs().max()
    if delta >= 0.01:
        raise ValueError(f"Full-weight merge validation failed: {delta}")
    return d


def groups_of(d: pd.DataFrame) -> dict[str, np.ndarray]:
    native = d.PRCITSHP.isin([1, 2, 3])
    fb = d.PRCITSHP.isin([4, 5])
    parents_us = d.PEFNTVTY.isin(US_AREA) & d.PEMNTVTY.isin(US_AREA)
    parent_mex = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    return {
        "third_plus_nh_white": (native & parents_us & d.PEHSPNON.eq(2) & d.PRDTRACE.eq(1)).to_numpy(),
        "mexican_second_gen": (native & parent_mex).to_numpy(),
        "mexican_third_plus_selfid": (native & parents_us & d.PRDTHSP.eq(1)).to_numpy(),
        "mexico_born": (fb & d.PENATVTY.eq(303)).to_numpy(),
        "all_native": native.to_numpy(),
        "all_foreign_born": fb.to_numpy(),
        "all_second_gen": (native & ~parents_us).to_numpy(),
        "all_third_plus": (native & parents_us).to_numpy(),
    }


def sdr_se(est: np.ndarray) -> float:
    return float(np.sqrt(4 / 160 * np.square(est[1:] - est[0]).sum()))


def rates(y: np.ndarray, W: np.ndarray, band: np.ndarray, nband: int,
          std_p: np.ndarray | None):
    """Return (crude 161-vector, age-standardised 161-vector or None)."""
    den = W.sum(axis=0)
    crude = (y @ W) / den
    if std_p is None:
        return crude, None
    A = np.zeros((len(y), nband))
    A[np.arange(len(y)), band] = 1.0
    num = A.T @ (W * y[:, None])
    dnm = A.T @ W
    rate = np.divide(num, dnm, out=np.zeros_like(num), where=dnm > 0)
    ok = (dnm[:, 0] > 0)
    p = std_p * ok
    p = p / p.sum()
    return crude, p @ rate


def main() -> None:
    d = load()
    W_all = d[REPS].to_numpy(dtype=np.float64)
    g = groups_of(d)
    rows = []

    # ---- Gate: Bier pooled foreign-born vs US-born disability prevalence ----
    uni = d.PRDISFLG.isin([1, 2]).to_numpy()          # CPS universe: persons 15+
    dis = d.PRDISFLG.eq(1).to_numpy().astype(float)
    for label, m in [("foreign_born", d.PRCITSHP.isin([4, 5]).to_numpy()),
                     ("us_born", d.PRCITSHP.isin([1, 2, 3]).to_numpy())]:
        for uni_label, sel in [("age15plus_universe", m & uni),
                               ("allages_undr15_as_nondisabled", m)]:
            sub = np.where(sel)[0]
            e, _ = rates(dis[sub], W_all[sub], None, 0, None)
            rows.append(dict(table="gate_bier", group=label, metric=f"prdisflg_{uni_label}",
                             standardisation="crude", estimate=e[0], se=sdr_se(e),
                             n_unweighted=len(sub), weighted=float(W_all[sub, 0].sum())))

    # ---- Adults 25-64 ----
    adult = (d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2) & d.PRDISFLG.isin([1, 2])).to_numpy()
    band = ((d.A_AGE.to_numpy() - 25) // 5).clip(0, 7)
    nband = 8
    ref = np.where(adult & g["third_plus_nh_white"])[0]
    std_p = np.bincount(band[ref], weights=W_all[ref, 0], minlength=nband)
    std_p = std_p / std_p.sum()

    ssdi = (d.SS_YN.eq(1) & (d.RESNSS1.eq(2) | d.RESNSS2.eq(2))).to_numpy()
    ssi = d.SSI_YN.eq(1).to_numpy()
    othr = d.DIS_YN.eq(1).to_numpy()
    anyinc = ssdi | ssi | othr
    ssdi_val = np.where(ssdi, d.SS_VAL.to_numpy(), 0.0)
    ssi_val = np.where(ssi, d.SSI_VAL.to_numpy(), 0.0)
    oth_val = np.where(othr, d.DIS_VAL1.to_numpy() + d.DIS_VAL2.to_numpy(), 0.0)

    metrics: dict[str, np.ndarray] = {"prdisflg_any": dis}
    for it in DIS_ITEMS:
        metrics[it.lower()] = d[it].eq(1).to_numpy().astype(float)
    metrics["dis_hp_prevents_work"] = d.DIS_HP.eq(1).to_numpy().astype(float)
    metrics["ssdi_receipt"] = ssdi.astype(float)
    metrics["ssi_receipt"] = ssi.astype(float)
    metrics["other_disability_income_receipt"] = othr.astype(float)
    metrics["any_disability_income_receipt"] = anyinc.astype(float)
    metrics["ssdi_dollars_per_adult"] = ssdi_val
    metrics["ssi_dollars_per_adult"] = ssi_val
    metrics["other_disability_dollars_per_adult"] = oth_val
    metrics["all_disability_dollars_per_adult"] = ssdi_val + ssi_val + oth_val

    for name in GROUPS:
        sel = adult & g[name]
        idx = np.where(sel)[0]
        W = W_all[idx]
        for mname, y in metrics.items():
            crude, std = rates(y[idx], W, band[idx], nband, std_p)
            rows.append(dict(table="adults25_64", group=name, metric=mname,
                             standardisation="crude", estimate=crude[0], se=sdr_se(crude),
                             n_unweighted=len(idx), weighted=float(W[:, 0].sum())))
            rows.append(dict(table="adults25_64", group=name, metric=mname,
                             standardisation="age_std_to_third_plus_nh_white",
                             estimate=std[0], se=sdr_se(std),
                             n_unweighted=len(idx), weighted=float(W[:, 0].sum())))
        # conditional on disabled
        didx = np.where(sel & (dis > 0))[0]
        Wd = W_all[didx]
        for mname, y in [("any_disability_income_given_disabled", anyinc.astype(float)),
                         ("ssdi_given_disabled", ssdi.astype(float)),
                         ("ssi_given_disabled", ssi.astype(float)),
                         ("all_disability_dollars_per_disabled_adult", ssdi_val + ssi_val + oth_val)]:
            crude, _ = rates(y[didx], Wd, None, 0, None)
            rows.append(dict(table="disabled_adults25_64", group=name, metric=mname,
                             standardisation="crude", estimate=crude[0], se=sdr_se(crude),
                             n_unweighted=len(didx), weighted=float(Wd[:, 0].sum())))

    out = pd.DataFrame(rows)
    out["flag_small_cell"] = out.n_unweighted < 100
    out.to_csv(OUT / "disability_by_generation.csv", index=False)

    # differences from the white reference, adults 25-64
    diffs = []
    for tbl, mlist in [("adults25_64", list(metrics)),
                       ("disabled_adults25_64", ["any_disability_income_given_disabled",
                                                 "ssdi_given_disabled", "ssi_given_disabled",
                                                 "all_disability_dollars_per_disabled_adult"])]:
        for std_label in (["crude", "age_std_to_third_plus_nh_white"]
                          if tbl == "adults25_64" else ["crude"]):
            for mname in mlist:
                ref_sel = adult & g["third_plus_nh_white"]
                for name in GROUPS[1:]:
                    sel = adult & g[name]
                    if tbl == "disabled_adults25_64":
                        ri, si = np.where(ref_sel & (dis > 0))[0], np.where(sel & (dis > 0))[0]
                        y = {"any_disability_income_given_disabled": anyinc.astype(float),
                             "ssdi_given_disabled": ssdi.astype(float),
                             "ssi_given_disabled": ssi.astype(float),
                             "all_disability_dollars_per_disabled_adult": ssdi_val + ssi_val + oth_val}[mname]
                        a, _ = rates(y[ri], W_all[ri], None, 0, None)
                        b, _ = rates(y[si], W_all[si], None, 0, None)
                    else:
                        ri, si = np.where(ref_sel)[0], np.where(sel)[0]
                        y = metrics[mname]
                        ac, as_ = rates(y[ri], W_all[ri], band[ri], nband, std_p)
                        bc, bs = rates(y[si], W_all[si], band[si], nband, std_p)
                        a, b = (ac, bc) if std_label == "crude" else (as_, bs)
                    dd = b - a
                    diffs.append(dict(table=tbl, group=name, metric=mname,
                                      standardisation=std_label, difference=dd[0],
                                      se_sdr=sdr_se(dd), n_unweighted=len(si)))
    pd.DataFrame(diffs).to_csv(OUT / "disability_differences.csv", index=False)
    print(out.to_string())
    print("\nWrote", OUT / "disability_by_generation.csv", "and disability_differences.csv")


if __name__ == "__main__":
    main()
