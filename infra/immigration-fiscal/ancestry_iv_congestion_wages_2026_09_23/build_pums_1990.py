"""1990-2000 pre-period panel on a 1990-identifiable footprint, for the pre-trend placebo.

MET2013 is not offered for the 1990 5% sample and 1990 PUMAs have no crosswalk in the repo, so a
metro's 1990 value comes from the counties IPUMS identifies in 1990 (COUNTYFIP > 0; large
counties whose PUMA boundaries coincide with county lines), mapped to the February-2013 CBSAs.
The 2000 comparison value is rebuilt on exactly the same counties from build_pums.py's 2000
county sums (_cache/pums_county_2000.csv), so each metro's 1990-2000 change holds its footprint.
Definitions (education, wage sample, composition cells, commute) are build_pums.py's, imported;
1990 dollars (1989 incomes) are deflated to 1999 dollars for the trim only.

County code changes between 1990 and the 2013 delineation: Dade FL 12025 became Miami-Dade 12086.

Writes derived/pums_metro_1990fp.csv (samples 199001 and 200001 on the 1990 footprint, plus the
share of the CBSA's 2000 SF1 population the footprint covers).
"""
import json
import pathlib
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_pums as bp  # noqa: E402

HERE = bp.HERE
RENAME = {"12025": "12086"}


def main():
    src = bp.CACHE / "ipums" / "pre.csv.gz"
    cols = bp.USECOLS + ["COUNTYFIP"]
    dtypes = {c: "int32" for c in cols if c != "PERWT"}
    dtypes["PERWT"] = "float64"
    d = pd.read_csv(src, usecols=cols, dtype=dtypes)
    d = bp.prepare(d)
    d["res_week"] = bp.residualize(d, "lnweek", "ftfy")
    d["res_hour"] = bp.residualize(d, "lnhour", "wage_ok")
    ident = d.COUNTYFIP > 0
    share_ident = float(d.PERWT[ident].sum() / d.PERWT.sum())
    key = d.STATEFIP.to_numpy(dtype=np.int64) * 1000 + d.COUNTYFIP.to_numpy(dtype=np.int64)
    s = bp.puma_sums(d[ident], key=key[ident.to_numpy()])
    s["cofips"] = s.key.astype(int).astype(str).str.zfill(5).replace(RENAME)
    num = [c for c in s.columns if c not in ("STATEFIP", "PUMA", "key", "cofips")]
    _, cb = bp.load_geo()
    j90 = s.merge(cb, on="cofips", how="inner")
    counties = sorted(j90.cofips.unique())
    g90 = j90.groupby("cbsa")[num].sum().reset_index()
    g90["sample"] = 199001
    c00 = pd.read_csv(bp.CACHE / "pums_county_2000.csv", dtype={"cofips": str})
    c00 = c00[c00.cofips.isin(counties)].merge(cb, on="cofips", how="inner")
    g00 = c00.groupby("cbsa")[num].sum().reset_index()
    g00["sample"] = 200001
    # coverage: the footprint's share of each CBSA's 2000 population (SF1 county counts)
    sf1 = pd.DataFrame.from_dict(json.loads((HERE / "_cache" / "census" / "sf1_2000_county.json").read_text()),
                                 orient="index")
    sf1.index.name = "cofips"
    sf1 = sf1.reset_index().merge(cb, on="cofips", how="inner")
    tot = sf1.groupby("cbsa").P001001.sum()
    fp = sf1[sf1.cofips.isin(counties)].groupby("cbsa").P001001.sum()
    cov = (fp / tot).rename("fp_pop_share").reset_index()
    out = pd.concat([g90, g00], ignore_index=True).merge(cov, on="cbsa", how="left")
    out.to_csv(bp.DERIVED / "pums_metro_1990fp.csv", index=False)
    print(f"1990 rows {len(d):,}; weight share in identified counties {share_ident:.3f}; "
          f"identified counties in 2013 metros {len(counties)}; CBSAs {g90.cbsa.nunique()}")
    print(cov.fp_pop_share.describe().round(3).to_string())


if __name__ == "__main__":
    main()
