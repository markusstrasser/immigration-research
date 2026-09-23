"""Crime family: race coding of Hispanic arrestees in NIBRS (TX, AZ, CA 2022-2023).

The repo's non-Hispanic-white arrest counts (crime_cost_2026_09_16 route B, nibrs_arrests_2026_09_16)
are constructed as White arrests minus all Hispanic arrests, assuming every Hispanic arrestee is
coded racially White. This counts Hispanic arrestees (Group A and B) by recorded race.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/crime_nibrs_arrestee_race.py
"""
import io, pathlib, zipfile
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE.parent / "offender_ethnicity_nibrs_2026_09_23" / "_cache"
rows = []
for st in ("TX", "AZ", "CA"):
    for yr in (2022, 2023):
        z = zipfile.ZipFile(CACHE / f"{st}-{yr}.zip")
        names = {pathlib.Path(n).name.upper(): n for n in z.namelist()}
        rd = lambda k: pd.read_csv(io.BytesIO(z.read(names[k])), low_memory=False)
        race = rd("REF_RACE.CSV")
        eth = rd("NIBRS_ETHNICITY.CSV")
        race.columns = race.columns.str.lower(); eth.columns = eth.columns.str.lower()
        for tbl, grp in (("NIBRS_ARRESTEE.CSV", "A"), ("NIBRS_ARRESTEE_GROUPB.CSV", "B")):
            a = rd(tbl); a.columns = a.columns.str.lower()
            a = a.merge(race[["race_id", "race_desc"]], on="race_id", how="left")
            a = a.merge(eth[["ethnicity_id", "ethnicity_name"]], on="ethnicity_id", how="left")
            adult = a[pd.to_numeric(a.age_num, errors="coerce") >= 18] if "age_num" in a else a
            t = adult.groupby(["ethnicity_name", "race_desc"], dropna=False).size().rename("n").reset_index()
            t["state"], t["year"], t["group"] = st, yr, grp
            rows.append(t)
out = pd.concat(rows)
out.to_csv(HERE / "derived" / "crime_nibrs_arrestee_race_by_ethnicity.csv", index=False)
h = out[out.ethnicity_name.astype(str).str.contains("Hispanic", case=False)
        & ~out.ethnicity_name.astype(str).str.contains("Not", case=False)]
s = h.groupby(["state", "race_desc"]).n.sum().unstack(fill_value=0)
print((s.div(s.sum(axis=1), axis=0)).round(3).to_string())
print(out.ethnicity_name.unique())
