"""Where is the CPS ASEC 2025 Mexico-born excess over ACS 2024 households? By citizenship and
state, plus the same count on ASEC 2026 (income year 2025). Writes derived/cps_mexico_born_gap.csv.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FISCAL = ROOT / "infra/immigration-fiscal"
ACS = FISCAL / "mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet"
CPS25 = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS26 = FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip"
COLS = ["A_AGE", "PENATVTY", "PRCITSHP", "MARSUPWT", "GESTFIPS", "PEINUSYR", "PRDTHSP", "PEHSPNON"]


def cps(path: Path, member: str) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        hh_member = [n for n in z.namelist() if n.startswith("hhpub")][0]
        p = pd.read_csv(z.open(member), usecols=[c for c in COLS if c != "GESTFIPS"] + ["PH_SEQ"])
        h = pd.read_csv(z.open(hh_member), usecols=["H_SEQ", "GESTFIPS"])
    p = p.merge(h.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", how="left", validate="many_to_one")
    p["w"] = p.MARSUPWT / 100
    return p


def main() -> None:
    a = pd.read_parquet(ACS, columns=["SERIALNO", "PWGTP", "CIT", "POBP", "NATIVITY", "STATE", "HISP"])
    a = a[~a.SERIALNO.str.contains("GQ")]
    c = cps(CPS25, "pppub25.csv")
    c6 = cps(CPS26, "pppub26.csv")
    am = a.POBP.eq(303) & a.NATIVITY.eq(2)
    cm = c.PENATVTY.eq(303) & c.PRCITSHP.isin([4, 5])
    c6m = c6.PENATVTY.eq(303) & c6.PRCITSHP.isin([4, 5])
    rows = []
    for lab, acit, ccit in [("naturalized", 4, 4), ("noncitizen", 5, 5)]:
        rows.append(dict(cut="citizenship", level=lab, acs_hh_m=a.PWGTP[am & a.CIT.eq(acit)].sum() / 1e6,
                         cps25_m=c.w[cm & c.PRCITSHP.eq(ccit)].sum() / 1e6,
                         cps26_m=c6.w[c6m & c6.PRCITSHP.eq(ccit)].sum() / 1e6))
    for lab, fips in [("California", 6), ("Texas", 48), ("Illinois", 17), ("Arizona", 4)]:
        rows.append(dict(cut="state", level=lab, acs_hh_m=a.PWGTP[am & a.STATE.eq(fips)].sum() / 1e6,
                         cps25_m=c.w[cm & c.GESTFIPS.eq(fips)].sum() / 1e6,
                         cps26_m=c6.w[c6m & c6.GESTFIPS.eq(fips)].sum() / 1e6))
    rest_a = ~a.STATE.isin([6, 48, 17, 4])
    rows.append(dict(cut="state", level="all other", acs_hh_m=a.PWGTP[am & rest_a].sum() / 1e6,
                     cps25_m=c.w[cm & ~c.GESTFIPS.isin([6, 48, 17, 4])].sum() / 1e6,
                     cps26_m=c6.w[c6m & ~c6.GESTFIPS.isin([6, 48, 17, 4])].sum() / 1e6))
    rows.append(dict(cut="total", level="Mexico-born FB", acs_hh_m=a.PWGTP[am].sum() / 1e6,
                     cps25_m=c.w[cm].sum() / 1e6, cps26_m=c6.w[c6m].sum() / 1e6))
    rows.append(dict(cut="total", level="Mexican self-ID", acs_hh_m=a.PWGTP[a.HISP.eq(2)].sum() / 1e6,
                     cps25_m=c.w[c.PRDTHSP.eq(1)].sum() / 1e6, cps26_m=c6.w[c6.PRDTHSP.eq(1)].sum() / 1e6))
    rows.append(dict(cut="total", level="All Hispanic", acs_hh_m=a.PWGTP[a.HISP.gt(1)].sum() / 1e6,
                     cps25_m=c.w[c.PEHSPNON.eq(1)].sum() / 1e6, cps26_m=c6.w[c6.PEHSPNON.eq(1)].sum() / 1e6))
    rows.append(dict(cut="total", level="All foreign-born", acs_hh_m=a.PWGTP[a.NATIVITY.eq(2)].sum() / 1e6,
                     cps25_m=c.w[c.PRCITSHP.isin([4, 5])].sum() / 1e6, cps26_m=c6.w[c6.PRCITSHP.isin([4, 5])].sum() / 1e6))
    rows.append(dict(cut="total", level="Population", acs_hh_m=a.PWGTP.sum() / 1e6,
                     cps25_m=c.w.sum() / 1e6, cps26_m=c6.w.sum() / 1e6))
    t = pd.DataFrame(rows)
    t["cps25_over_acs"] = t.cps25_m / t.acs_hh_m
    t.to_csv(HERE / "derived/cps_mexico_born_gap.csv", index=False)
    print(t.round(3).to_string())


if __name__ == "__main__":
    main()
