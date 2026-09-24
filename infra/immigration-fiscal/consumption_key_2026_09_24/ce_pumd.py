"""CE Interview Survey 2024 public-use microdata: one row per quarterly interview, annualized.

Reads the five FMLI files (2024Q1x-2025Q1) and the MTBI cash-contribution UCCs from
_cache/sources/intrvw24.zip. Quarterly amounts are the interview's three-month recall
(PQ + CQ) times four; income before taxes (FINCBTXM) is already annual. Weights are FINLWT21;
INC_RANK is BLS's weighted rank of income before taxes within the quarter's file.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ZIP = HERE / "_cache" / "sources" / "intrvw24.zip"
CACHE = HERE / "_cache" / "ce_pumd_2024.csv"
FILES = ["241x", "242", "243", "244", "251"]
FMLI = ["NEWID", "FINLWT21", "INC_RANK", "FINCBTXM", "HORREF1", "HISP_REF", "AGE_REF", "FAM_SIZE",
        "TOTEXPPQ", "TOTEXPCQ", "PERINSPQ", "PERINSCQ", "CASHCOPQ", "CASHCOCQ", "SHELTPQ", "SHELTCQ",
        "HEALTHPQ", "HEALTHCQ", "EDUCAPQ", "EDUCACQ"]
# Cash-contribution UCCs (the dictionary's CASHCOPQ formula). 800861 carries CNT code 170, "Any and
# all other persons not in your CU", checked against the CNT detail file in check_gift_ucc().
CASH_UCC = [800111, 800121, 800804, 800811, 800821, 800831, 800841, 800851, 800861]
GIFT_UCC = 800861


def read() -> pd.DataFrame:
    if CACHE.exists():
        return pd.read_csv(CACHE)
    frames = []
    with zipfile.ZipFile(ZIP) as z:
        for q in FILES:
            f = pd.read_csv(z.open(f"intrvw24/fmli{q}.csv"), usecols=FMLI)
            m = pd.read_csv(z.open(f"intrvw24/mtbi{q}.csv"), usecols=["NEWID", "UCC", "COST", "PUBFLAG"])
            m = m[m.UCC.isin(CASH_UCC)]
            gifts = m[m.UCC.eq(GIFT_UCC)].groupby("NEWID").COST.sum()
            cash = m.groupby("NEWID").COST.sum()
            f["file"] = q
            f["gift_q"] = f.NEWID.map(gifts).fillna(0.0)
            f["cash_mtbi_q"] = f.NEWID.map(cash).fillna(0.0)
            frames.append(f)
    d = pd.concat(frames, ignore_index=True)
    q = lambda a, b: d[a].fillna(0) + d[b].fillna(0)
    out = pd.DataFrame({
        "newid": d.NEWID, "file": d.file, "weight": d.FINLWT21, "inc_rank": d.INC_RANK,
        "income": d.FINCBTXM, "horref1": d.HORREF1, "hispanic": d.HISP_REF.eq(1),
        "age_ref": d.AGE_REF, "fam_size": d.FAM_SIZE,
        "total": 4 * q("TOTEXPPQ", "TOTEXPCQ"), "pip": 4 * q("PERINSPQ", "PERINSCQ"),
        "cash": 4 * q("CASHCOPQ", "CASHCOCQ"), "shelter": 4 * q("SHELTPQ", "SHELTCQ"),
        "health": 4 * q("HEALTHPQ", "HEALTHCQ"), "education": 4 * q("EDUCAPQ", "EDUCACQ"),
        "gift_other_persons": 4 * d.gift_q, "cash_mtbi": 4 * d.cash_mtbi_q,
    })
    out["consumption"] = out.total - out.pip - out.cash
    out["taxable_broad"] = out.consumption - out.shelter - out.health - out.education
    out["mexican_origin"] = out.horref1.isin([1, 2, 3])
    out.to_csv(CACHE, index=False, lineterminator="\n")
    return out


def check_gift_ucc() -> dict:
    """UCC 800861 against the CNT file's code 170 ('any and all other persons not in your CU').

    The MTBI quarterly sum of 800861 and the CNT amounts coded 170 should agree CU by CU up to the
    CNT file's monthly/same-each-month convention; report the share of CUs with any 170 record that
    also carry 800861, and the reverse.
    """
    with zipfile.ZipFile(ZIP) as z:
        cnt = pd.read_csv(z.open("intrvw24/expn24/cnt24.csv"), usecols=["QYEAR", "NEWID", "CONTCODE", "CONTEXPX"])
        m = pd.concat([pd.read_csv(z.open(f"intrvw24/mtbi{q}.csv"), usecols=["NEWID", "UCC", "COST"]) for q in FILES])
    ids170 = set(cnt.loc[cnt.CONTCODE.eq(170), "NEWID"])
    ids861 = set(m.loc[m.UCC.eq(GIFT_UCC) & m.COST.ne(0), "NEWID"])
    both = ids170 & ids861
    return {"cnt_170_ids": len(ids170), "mtbi_800861_ids": len(ids861), "overlap": len(both),
            "share_170_in_861": len(both) / max(len(ids170), 1), "share_861_in_170": len(both) / max(len(ids861), 1)}


if __name__ == "__main__":
    d = read()
    print(d.shape)
    print(check_gift_ucc())
    w = d.weight
    for name, m in [("all", d.weight > 0), ("hispanic", d.hispanic), ("mexican_origin", d.mexican_origin)]:
        s = d[m]
        print(f"{name:15} n={len(s):6d}  Y={np.average(s.income, weights=s.weight):9.0f}  "
              f"E={np.average(s.total, weights=s.weight):9.0f}  C={np.average(s.consumption, weights=s.weight):9.0f}  "
              f"cash={np.average(s.cash, weights=s.weight):7.0f}  gifts_to_persons={np.average(s.gift_other_persons, weights=s.weight):7.0f}  "
              f"share_giving={np.average(s.gift_other_persons > 0, weights=s.weight):.3f}")
