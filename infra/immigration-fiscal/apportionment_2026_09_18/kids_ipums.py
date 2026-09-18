"""Arm 4 input: Mexico-born persons plus their US-born children under 18, by state.

Local IPUMS USA panel (ACS), read-only. The panel carries no parent pointer (no MOMLOC/POPLOC),
so 'their children' is a household proxy: a US-born person under 18 living in the same household
as a Mexico-born person at least 15 years older. That slightly overstates (unrelated household
members) and slightly understates (children living apart from a Mexico-born parent).
[INFERENCE] — labelled as an estimate, cross-checked against a CPS ASEC parent-birthplace
calculation in kids_cps.py.
"""
from pathlib import Path
import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
DB = "/Users/alien/research-data/immigration-fiscal/derived/immigration_microdata.duckdb"
YEARS = (2010, 2023)  # the only ACS vintages in the local panel; interpolated to 2020

FIPS_NAME = {
    1: "Alabama", 2: "Alaska", 4: "Arizona", 5: "Arkansas", 6: "California", 8: "Colorado",
    9: "Connecticut", 10: "Delaware", 11: "District of Columbia", 12: "Florida", 13: "Georgia",
    15: "Hawaii", 16: "Idaho", 17: "Illinois", 18: "Indiana", 19: "Iowa", 20: "Kansas",
    21: "Kentucky", 22: "Louisiana", 23: "Maine", 24: "Maryland", 25: "Massachusetts",
    26: "Michigan", 27: "Minnesota", 28: "Mississippi", 29: "Missouri", 30: "Montana",
    31: "Nebraska", 32: "Nevada", 33: "New Hampshire", 34: "New Jersey", 35: "New Mexico",
    36: "New York", 37: "North Carolina", 38: "North Dakota", 39: "Ohio", 40: "Oklahoma",
    41: "Oregon", 42: "Pennsylvania", 44: "Rhode Island", 45: "South Carolina",
    46: "South Dakota", 47: "Tennessee", 48: "Texas", 49: "Utah", 50: "Vermont", 51: "Virginia",
    53: "Washington", 54: "West Virginia", 55: "Wisconsin", 56: "Wyoming",
}

SQL = f"""
with p as (
  select YEAR, SAMPLE, SERIAL, STATEFIP, AGE, BPL, PERWT
  from ipums_usa_borjas_panel
  where YEAR in {YEARS} and GQ in (1, 2)
),
mex_adult as (
  select YEAR, SAMPLE, SERIAL, max(AGE) as max_mex_age
  from p where BPL = 200 and AGE >= 15 group by 1, 2, 3
),
kids as (
  select p.YEAR, p.STATEFIP, sum(p.PERWT) as us_born_kids_with_mex_adult
  from p join mex_adult m
    on p.YEAR = m.YEAR and p.SAMPLE = m.SAMPLE and p.SERIAL = m.SERIAL
  where p.BPL < 150 and p.AGE < 18 and m.max_mex_age >= p.AGE + 15
  group by 1, 2
),
mexborn as (
  select YEAR, STATEFIP, sum(PERWT) as mexico_born from p where BPL = 200 group by 1, 2
)
select b.YEAR, b.STATEFIP,
       b.mexico_born as mexico_born_ipums,
       coalesce(k.us_born_kids_with_mex_adult, 0) as us_born_kids_ipums
from mexborn b left join kids k on b.YEAR = k.YEAR and b.STATEFIP = k.STATEFIP
order by 1, 2
"""

if __name__ == "__main__":
    con = duckdb.connect(DB, read_only=True)
    d = con.execute(SQL).df()
    d["state_name"] = d["STATEFIP"].map(FIPS_NAME)
    d = d[d["state_name"].notna() & (d["state_name"] != "District of Columbia")]
    d["kids_per_mexborn"] = d["us_born_kids_ipums"] / d["mexico_born_ipums"]
    wide = d.pivot(index="state_name", columns="YEAR",
                   values=["mexico_born_ipums", "us_born_kids_ipums", "kids_per_mexborn"])
    W = 10.0 / 13.0  # April 2020 sits 10/13 of the way from the 2010 to the 2023 ACS
    out = pd.DataFrame({
        "state_name": wide.index,
        "kids_per_mexborn_2010": wide[("kids_per_mexborn", 2010)].values,
        "kids_per_mexborn_2023": wide[("kids_per_mexborn", 2023)].values,
    })
    out["kids_per_mexborn_2020_interp"] = (1 - W) * out.kids_per_mexborn_2010 + W * out.kids_per_mexborn_2023
    out.to_csv(DERIVED / "kids_ipums_ratio.csv", index=False)
    for yr in YEARS:
        sub = d[d.YEAR == yr]
        print(f"{yr}: Mexico-born {sub.mexico_born_ipums.sum():,.0f} | US-born under-18 in a "
              f"household with a Mexico-born adult 15+ years older {sub.us_born_kids_ipums.sum():,.0f} "
              f"| national ratio {sub.us_born_kids_ipums.sum()/sub.mexico_born_ipums.sum():.3f}")
    print(f"states={len(out)}")
    print(out.sort_values('kids_per_mexborn_2020_interp', ascending=False).head(6).to_string(index=False))
