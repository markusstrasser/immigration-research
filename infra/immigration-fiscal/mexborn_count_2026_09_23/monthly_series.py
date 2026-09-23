"""Mexico-born count on every CPS basic monthly file held in _cache/basic/ (fetch_basic.sh).

Fixed-width public-use records; the positions below are identical in the 2024, May 2024, 2025
and 2026 record layouts (_cache/layout/). PWSSWGT is the final weight with 4 implied decimals,
controlled to state, origin-sex-age and age-race-sex totals; PRPERTYP 1-2 are civilians
(armed-forces adults carry no weight). Mexico-born = PENATVTY 303 and PRCITSHP 4/5, the audit's
definition. Writes derived/monthly_series.csv.
"""
from __future__ import annotations

import re
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
BASIC = HERE / "_cache/basic"
# name: (first column, last column), 1-based inclusive, from the record layouts
LAYOUT = {
    "HRMONTH": (16, 17), "HRYEAR4": (18, 21), "HRINTSTA": (57, 58), "HRMIS": (63, 64),
    "GESTFIPS": (93, 94), "PRTAGE": (122, 123), "PRDTHSP": (141, 142), "PEHSPNON": (157, 158),
    "PRPERTYP": (161, 162), "PENATVTY": (163, 165), "PRCITSHP": (172, 173), "PRCITFLG": (174, 175),
    "PRINUYER": (176, 177), "PUSLFPRX": (178, 179), "PWSSWGT": (613, 622), "PXNATVTY": (675, 676),
}
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
CA_TX = [6, 48]


def read_month(path: Path) -> pd.DataFrame:
    with zipfile.ZipFile(path) as z:
        member = [n for n in z.namelist() if n.endswith(".dat")][0]
        df = pd.read_fwf(z.open(member), colspecs=[(a - 1, b) for a, b in LAYOUT.values()],
                         names=list(LAYOUT), header=None, dtype="int64")
    df["w"] = df.PWSSWGT / 1e4
    return df[df.PRPERTYP.isin([1, 2, 3])]


def summarize(df: pd.DataFrame) -> dict:
    mex = df.PENATVTY.eq(303) & df.PRCITSHP.isin([4, 5])
    fb = df.PRCITSHP.isin([4, 5])
    hisp = df.PEHSPNON.eq(1)

    def m(mask: pd.Series) -> float:
        return round(df.w[mask].sum() / 1e6, 6)

    return dict(
        year=int(df.HRYEAR4.iloc[0]), month=int(df.HRMONTH.iloc[0]),
        n_persons=int(df.w.gt(0).sum()), n_mexborn=int((mex & df.w.gt(0)).sum()),
        n_mexborn_other=int((mex & df.w.gt(0) & ~df.GESTFIPS.isin(CA_TX)).sum()),
        population_m=m(df.w.gt(0)), hispanic_m=m(hisp), mexican_selfid_m=m(df.PRDTHSP.eq(1)),
        foreign_born_m=m(fb), hispanic_fb_m=m(fb & hisp),
        mexborn_m=m(mex), mexborn_catx_m=m(mex & df.GESTFIPS.isin(CA_TX)),
        mexborn_other_m=m(mex & ~df.GESTFIPS.isin(CA_TX)),
        mexborn_natz_m=m(mex & df.PRCITSHP.eq(4)), mexborn_noncit_m=m(mex & df.PRCITSHP.eq(5)),
        # PRINUYER 27-28 = entered 2020 or later in every 2024-2026 code list
        mexborn_entry2020plus_m=m(mex & df.PRINUYER.isin([27, 28])),
        mexborn_self_resp_m=m(mex & df.PRTAGE.ge(16) & df.PUSLFPRX.eq(1)),
        mexborn_16plus_m=m(mex & df.PRTAGE.ge(16)),
        mexborn_nat_allocated_m=m(mex & df.PXNATVTY.ge(10)),
        mexborn_share_of_hisp_fb=round(df.w[mex].sum() / df.w[fb & hisp].sum(), 6),
    )


def main() -> None:
    rows = []
    files = sorted(BASIC.glob("*pub.zip"), key=lambda p: (int(p.name[3:5]), MONTHS.index(p.name[:3])))
    for path in files:
        if not re.fullmatch(r"[a-z]{3}\d\dpub\.zip", path.name):
            continue
        rows.append(summarize(read_month(path)))
        print(rows[-1]["year"], rows[-1]["month"], rows[-1]["mexborn_m"], flush=True)
    t = pd.DataFrame(rows)
    t.to_csv(HERE / "derived/monthly_series.csv", index=False)
    print(t.to_string(index=False))


if __name__ == "__main__":
    main()
