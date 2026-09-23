"""Census 1980-2000 allocation rates (IPUMS Q flags, any nonzero code) for men 18-40, by group and
institutional residence, from the IPUMS store view usa_00004_q. Weighted by PERWT.
Writes derived/acs_census_qflags.csv."""
from pathlib import Path
import duckdb
HERE = Path(__file__).resolve().parent
DB = HERE.parents[2] / "sources/immigration-fiscal/derived/ipums_usa_extracts.duckdb"
q = """
with t as (
  select YEAR, GQ = 3 as inst, PERWT, QBPL, QCITIZEN, QYRIMM, QEDUC,
    case when HISPAN = 1 and BPL < 100 then 'usborn_mexican_hispan'
         when BPL = 200 then 'mexico_born'
         when HISPAN = 0 and RACE = 1 and BPL < 100 then 'native_nh_white'
         else null end as grp
  from usa_00004_q where GQ in (1, 2, 3, 5))
select YEAR, grp, inst, count(*) n,
  sum(PERWT * (QBPL > 0)::int) / sum(PERWT) qbpl,
  sum(PERWT * (QCITIZEN > 0)::int) / sum(PERWT) qcitizen,
  sum(PERWT * (QYRIMM > 0)::int * (grp = 'mexico_born')::int) / sum(PERWT) qyrimm,
  sum(PERWT * (QEDUC > 0)::int) / sum(PERWT) qeduc
from t where grp is not null group by all order by grp, inst, YEAR
"""
d = duckdb.connect(str(DB), read_only=True).sql(q).df()
d.to_csv(HERE / "derived" / "acs_census_qflags.csv", index=False)
print(d.round(3).to_string(index=False))
