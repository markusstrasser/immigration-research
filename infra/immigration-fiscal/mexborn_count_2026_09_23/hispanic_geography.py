"""Where the CPS puts Hispanics, against the ACS (which is weighted to county Hispanic totals).

The CPS controls Hispanic origin only nationally, by age and sex; its state controls are by broad
race (Black / other), three age groups and sex (cpsmar25, "Estimation Procedure"). The ACS weights
to the Census population estimates by county, age, sex, race and Hispanic origin. So the ACS pins
the Hispanic total in every state and the CPS does not. If the CPS carries too many Hispanics
outside California and Texas, part of the Mexico-born excess there is geographic misallocation.

Compares ASEC 2025 (MARSUPWT) with ACS 2024 PUMS households, and with the CPS basic monthly 2024
average (PWSSWGT), for Hispanics, Mexican self-ID, Mexico-born, and Mexico-born as a share of
Hispanics, in CA+TX and the other states. Writes derived/hispanic_geography.csv.
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import pandas as pd

from monthly_series import BASIC, CA_TX, read_month

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ACS = FISCAL / "mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet"
ASEC25 = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"


def asec() -> pd.DataFrame:
    with zipfile.ZipFile(ASEC25) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PENATVTY", "PRCITSHP", "PEHSPNON", "PRDTHSP", "MARSUPWT"])
        h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"])
    p = p.merge(h.rename(columns={"H_SEQ": "PH_SEQ"}), on="PH_SEQ", validate="many_to_one")
    return pd.DataFrame({"w": p.MARSUPWT / 100, "catx": p.GESTFIPS.isin(CA_TX), "hisp": p.PEHSPNON.eq(1),
                         "mexid": p.PRDTHSP.eq(1), "mexborn": p.PENATVTY.eq(303) & p.PRCITSHP.isin([4, 5])})


def acs() -> pd.DataFrame:
    a = pd.read_parquet(ACS, columns=["SERIALNO", "PWGTP", "POBP", "NATIVITY", "STATE", "HISP"])
    a = a[~a.SERIALNO.str.contains("GQ")]
    return pd.DataFrame({"w": a.PWGTP.astype(float), "catx": a.STATE.isin(CA_TX), "hisp": a.HISP.gt(1),
                         "mexid": a.HISP.eq(2), "mexborn": a.POBP.eq(303) & a.NATIVITY.eq(2)})


def monthly_2024() -> pd.DataFrame:
    parts = []
    for path in sorted(BASIC.glob("*24pub.zip")):
        d = read_month(path)
        parts.append(pd.DataFrame({"w": d.w / 12, "catx": d.GESTFIPS.isin(CA_TX), "hisp": d.PEHSPNON.eq(1),
                                   "mexid": d.PRDTHSP.eq(1), "mexborn": d.PENATVTY.eq(303) & d.PRCITSHP.isin([4, 5])}))
    assert len(parts) == 12, len(parts)
    return pd.concat(parts, ignore_index=True)


def tab(d: pd.DataFrame, source: str) -> list[dict]:
    rows = []
    for region, m in [("CA+TX", d.catx), ("other states", ~d.catx), ("US", pd.Series(True, index=d.index))]:
        x = d[m]
        rows.append(dict(source=source, region=region, population_m=x.w.sum() / 1e6,
                         hispanic_m=x.w[x.hisp].sum() / 1e6, mexican_selfid_m=x.w[x.mexid].sum() / 1e6,
                         mexborn_m=x.w[x.mexborn].sum() / 1e6,
                         non_mexican_hispanic_m=x.w[x.hisp & ~x.mexid].sum() / 1e6,
                         mexborn_share_of_hispanic=x.w[x.mexborn].sum() / x.w[x.hisp].sum(),
                         hispanic_share_of_population=x.w[x.hisp].sum() / x.w.sum()))
    return rows


def main() -> None:
    t = pd.DataFrame(tab(acs(), "ACS 2024 households") + tab(monthly_2024(), "CPS monthly 2024 average")
                     + tab(asec(), "CPS ASEC 2025")).round(6)
    t.to_csv(HERE / "derived/hispanic_geography.csv", index=False)
    with pd.option_context("display.width", 220):
        print(t.to_string(index=False))


if __name__ == "__main__":
    main()
