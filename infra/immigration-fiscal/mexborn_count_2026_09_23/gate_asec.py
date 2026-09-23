"""Gate and decomposition on the held CPS ASEC files.

1. Gate: reproduce the audit's Mexico-born counts (PENATVTY 303, PRCITSHP 4/5, MARSUPWT):
   12.231M on ASEC 2025 and 11.109M on ASEC 2026 (dataset_integrity_2026_09_23/cps.md §3).
2. Split each file into the March basic sample (A_FNLWGT > 0, "CPS variable pwsswgt") and the
   additional supplement sample (A_FNLWGT = 0: the Hispanic and CHIP oversamples), and count the
   Mexico-born on each with MARSUPWT and, for the March basic records, with A_FNLWGT.

Writes derived/asec_gate.csv and derived/asec_sample_split.csv.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
FILES = {
    2025: (FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip", "pppub25.csv", "hhpub25.csv"),
    2026: (FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip", "pppub26.csv", "hhpub26.csv"),
}
AUDIT = {2025: 12.231213890000001, 2026: 11.10894712}
PCOLS = ["PH_SEQ", "A_AGE", "PENATVTY", "PRCITSHP", "PEHSPNON", "PRDTHSP", "MARSUPWT", "A_FNLWGT"]
CA_TX = [6, 48]


def load(year: int) -> pd.DataFrame:
    path, pmem, hmem = FILES[year]
    with zipfile.ZipFile(path) as z:
        p = pd.read_csv(z.open(pmem), usecols=PCOLS)
        h = pd.read_csv(z.open(hmem), usecols=["H_SEQ", "GESTFIPS", "H_MIS"])
    p = p.merge(h.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", how="left", validate="many_to_one")
    p["w"] = p.MARSUPWT / 100
    p["wb"] = p.A_FNLWGT / 100
    p["basic"] = p.A_FNLWGT.gt(0)
    p["mex"] = p.PENATVTY.eq(303) & p.PRCITSHP.isin([4, 5])
    return p


def cuts(p: pd.DataFrame) -> dict[str, pd.Series]:
    return {
        "Mexico-born": p.mex,
        "Mexico-born CA+TX": p.mex & p.GESTFIPS.isin(CA_TX),
        "Mexico-born other states": p.mex & ~p.GESTFIPS.isin(CA_TX),
        "Mexico-born naturalized": p.mex & p.PRCITSHP.eq(4),
        "Mexico-born noncitizen": p.mex & p.PRCITSHP.eq(5),
        "All foreign-born": p.PRCITSHP.isin([4, 5]),
        "All Hispanic": p.PEHSPNON.eq(1),
        "Population": pd.Series(True, index=p.index),
    }


def main() -> None:
    gate, split = [], []
    for year in FILES:
        p = load(year)
        got = p.w[p.mex].sum() / 1e6
        ok = abs(got - AUDIT[year]) < 5e-4
        gate.append(dict(asec=year, audit_m=round(AUDIT[year], 6), reproduced_m=round(got, 6), pass_=ok))
        for lab, m in cuts(p).items():
            b, s = m & p.basic, m & ~p.basic
            split.append(dict(
                asec=year, cut=lab,
                n_basic=int(b.sum()), n_supp=int(s.sum()),
                marsupwt_all_m=round(p.w[m].sum() / 1e6, 6),
                marsupwt_basic_m=round(p.w[b].sum() / 1e6, 6),
                marsupwt_supp_m=round(p.w[s].sum() / 1e6, 6),
                fnlwgt_basic_m=round(p.wb[b].sum() / 1e6, 6),
            ))
    g = pd.DataFrame(gate).rename(columns={"pass_": "pass"})
    s = pd.DataFrame(split)
    g.to_csv(HERE / "derived/asec_gate.csv", index=False)
    s.to_csv(HERE / "derived/asec_sample_split.csv", index=False)
    print(g.to_string(index=False))
    print(s.to_string(index=False))
    if not g["pass"].all():
        raise SystemExit("[GATE FAIL] audit counts not reproduced")


if __name__ == "__main__":
    main()
