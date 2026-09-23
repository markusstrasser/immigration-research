"""Education shares of workers and of income in the 1980, 1990 and 2000 censuses, the sample
periods of Moretti (2004) and Glaeser-Resseger (2010).

Why: the Ciccone-Peri constant-composition reading of Moretti's Table 5 averages his four
education-group coefficients with the earnings shares of his own sample, and the CES term netted
from pooled college-share coefficients needs that period's employment and earnings shares.

Input: the local IPUMS USA extract (1980 and 1990 5% state samples, 2000 5%) in
~/research-data/immigration-fiscal/derived/immigration_microdata.duckdb (outside the repository).
The extract has total personal income (INCTOT), not earnings, so income shares stand in for
earnings shares [INFERENCE: INCTOT includes transfers and capital income].
Sample: employed (EMPSTAT 1), ages 25-70 (Moretti's census sample), positive INCTOT, not N/A.
Education (IPUMS EDUCD): lths below grade 12 (1980) or through "12th grade, no diploma" (061,
1990 and 2000); hs grade 12 (060, 065 in 1980) or diploma/GED (062); ba+ 100 and above; sc the rest
(1-3 years of college, some college, associate degrees).

Output: derived/sample_weights.csv (year, cell, worker share, income share).
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project --with duckdb python3 infra/immigration-fiscal/scale_spillovers_2026_09_23/sample_weights.py
"""
from __future__ import annotations

import pathlib

import duckdb
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
DB = pathlib.Path.home() / "research-data/immigration-fiscal/derived/immigration_microdata.duckdb"

QUERY = """
select YEAR as year,
       case when (YEAR = 1980 and EDUCD < 60) or (YEAR > 1980 and EDUCD <= 61) then 'lths'
            when (YEAR = 1980 and EDUCD in (60, 65)) or (YEAR > 1980 and EDUCD = 62) then 'hs'
            when EDUCD >= 100 then 'ba' else 'sc' end as cell,
       sum(PERWT) as workers, sum(PERWT * INCTOT) as income
from ipums_usa_borjas_panel
where YEAR in (1980, 1990, 2000) and EMPSTAT = 1 and AGE between 25 and 70
  and INCTOT > 0 and INCTOT < 9999998
group by 1, 2
"""


def main():
    con = duckdb.connect(str(DB), read_only=True)
    df = con.execute(QUERY).df()
    df["worker_share"] = df["workers"] / df.groupby("year")["workers"].transform("sum")
    df["income_share"] = df["income"] / df.groupby("year")["income"].transform("sum")
    order = {"lths": 0, "hs": 1, "sc": 2, "ba": 3}
    df = df.sort_values(["year", "cell"], key=lambda c: c.map(order) if c.name == "cell" else c)
    df.to_csv(HERE / "derived" / "sample_weights.csv", index=False)
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
