"""Derived inputs for the housing transfer arms, from the cached public files (fetch.py).

1. Land share of residential real estate, Federal Reserve Z.1: households' owner-occupied real
   estate at market value against households' residential structures at current cost (S.1M.b
   lines 4 and 48), and the same for noncorporate business residential real estate (S.11.2.b
   lines 4 and 43), which holds most individually owned rental housing. Land share of value =
   1 - structures / market value. Foreign direct investment in the noncorporate real-estate
   business (equity plus intercompany debt, S.11.2.b lines 37 and 40) over its real estate is
   the foreign-ownership anchor.
2. SCF 2022 summary extract: the Hispanic respondent share of families, of other residential
   real estate (ORESRE: 1-4 family properties other than the home, second homes, time shares)
   and of nonresidential real-estate equity (NNRESRE: commercial, larger rental buildings, net
   of debt). Shares are computed within each of the five implicates; the table reports their
   mean and range (imputation spread only, not sampling error).
3. Wilson and Zhou's regressor is unauthorized worker flow as a share of initial QCEW
   employment; converting to persons as a share of population uses their own worker share of
   all unauthorized entrants (56%, p.25) and the March 2021 QCEW-to-population ratio.

4. Rental Housing Finance Survey 2024 public-use file: rental properties and units (property
   weight x units in property) by current ownership entity.

Outputs: derived/inputs_land_foreign.csv, derived/inputs_scf.csv, derived/inputs_wz.csv,
derived/inputs_rhfs.csv.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/inputs.py
"""
from __future__ import annotations

import io
import json
import pathlib
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
QUARTERS = ["2019:Q4", "2022:Q4", "2023:Q4", "2024:Q4", "2025:Q4", "2026:Q2"]
Z1 = {
    "S1M_b": {"hh_owner_occ_market": "LM155035015.Q", "hh_resid_structures": "LM155012665.Q"},
    "S11_2_b": {"nc_real_estate_market": "LM115035005.Q", "nc_resid_market": "LM115035023.Q",
                "nc_resid_structures": "FL115012665.Q", "nc_fdi_re_equity": "LM115114103.Q",
                "nc_fdi_re_debt": "LM115114305.Q"},
}
# Wilson and Zhou (2026), Dallas Fed WP 2607: Table 6b rents 1.438 (SE 0.344), house prices
# 2.189 (SE 0.741) per UIWF equal to 1% of initial employment; "around 56% of all unauthorized
# immigrants ... are workers" (p.25); employment IV 0.507 on all flows vs 0.961 on UIWF.
WZ = {"rent": (1.438, 0.344), "price": (2.189, 0.741)}
WZ_WORKER_SHARE = {"text_56pct": 0.56, "regression_ratio": 0.507 / 0.961}


def z1_series():
    rows = []
    with zipfile.ZipFile(CACHE / "z1_csv_files.zip") as z:
        for table, series in Z1.items():
            frame = pd.read_csv(io.BytesIO(z.read(f"csv/{table}.csv")))
            frame = frame[frame["date"].isin(QUARTERS)].set_index("date")
            for name, code in series.items():
                for q, v in frame[code].items():
                    rows.append({"quarter": q, "item": name, "code": code,
                                 "millions": float(v)})
    wide = pd.DataFrame(rows).pivot(index="quarter", columns="item", values="millions")
    wide["land_share_owner_occupied"] = 1 - wide.hh_resid_structures / wide.hh_owner_occ_market
    wide["land_share_noncorp_residential"] = 1 - wide.nc_resid_structures / wide.nc_resid_market
    wide["foreign_share_noncorp_real_estate"] = (
        (wide.nc_fdi_re_equity + wide.nc_fdi_re_debt) / wide.nc_real_estate_market)
    wide["foreign_equity_share_noncorp_real_estate"] = wide.nc_fdi_re_equity / wide.nc_real_estate_market
    return wide.reset_index()


def scf_shares():
    d = pd.read_stata(CACHE / "scf/rscfp2022.dta", columns=["yy1", "y1", "wgt", "race",
                                                            "oresre", "nnresre", "houses"])
    # Y1 = case id x 10 + implicate; the Stata integer types overflow on yy1*10.
    d["implicate"] = d["y1"].astype("int64") % 10
    if sorted(d["implicate"].unique()) != [1, 2, 3, 4, 5]:
        raise ValueError("SCF implicate coding changed")
    out = []
    for imp, g in d.groupby("implicate"):
        w = g["wgt"]
        hisp = g["race"].eq(3)
        row = {"implicate": int(imp)}
        for name, x in (("families", np.ones(len(g))), ("oresre", g["oresre"]),
                        ("nnresre_positive", g["nnresre"].clip(lower=0)),
                        ("has_oresre", (g["oresre"] > 0).astype(float)),
                        ("houses", g["houses"])):
            row[f"hispanic_share_{name}"] = float((w * x)[hisp].sum() / (w * x).sum())
        # Extract weights sum to the family total across all five implicates, so one
        # implicate's weighted sum is scaled by five.
        row["aggregate_oresre_bn"] = float((w * g["oresre"]).sum() * 5 / 1e9)
        row["families_m"] = float(w.sum() * 5 / 1e6)
        out.append(row)
    per = pd.DataFrame(out)
    summary = per.drop(columns="implicate").agg(["mean", "min", "max"]).T.reset_index()
    return summary.rename(columns={"index": "item"})


RHFS_ENTITY = {1: "individual investor", 2: "trustee for estate", 3: "LLP, LP or LLC",
               4: "tenant in common", 5: "general partnership", 6: "REIT",
               7: "real estate corporation", 8: "housing cooperative", 9: "nonprofit",
               10: "other institution", -9: "not reported"}


def rhfs_entities():
    """Rental properties and units by current ownership entity, RHFS 2024 (weights WEIGHT)."""
    d = pd.read_csv(CACHE / "rhfspuf2024.csv", usecols=["OWNENT", "WEIGHT", "NUMUNITS_R"])
    d["units"] = d["WEIGHT"] * d["NUMUNITS_R"]
    out = d.groupby("OWNENT").agg(properties=("WEIGHT", "sum"), units=("units", "sum"),
                                  sample=("WEIGHT", "size")).reset_index()
    out["entity"] = out["OWNENT"].map(RHFS_ENTITY)
    reported = out["OWNENT"] != -9
    for col in ("properties", "units"):
        out[f"{col}_share_all"] = out[col] / out[col].sum()
        out[f"{col}_share_reported"] = np.where(reported, out[col] / out.loc[reported, col].sum(), np.nan)
    return out


def wz_conversion():
    qcew = pd.read_csv(CACHE / "qcew_2021q1_us.csv", dtype=str)
    row = qcew[(qcew.own_code == "0") & (qcew.industry_code == "10")].iloc[0]
    employment = float(row["month3_emplvl"])  # March 2021, all ownerships, total covered
    private = qcew[(qcew.own_code == "5") & (qcew.industry_code == "10")].iloc[0]
    population = float(json.loads((CACHE / "acs2021_us_population.json").read_text())["rows"][1][0])
    rows = []
    for denom, emp in (("total_covered", employment), ("private", float(private["month3_emplvl"]))):
        for share_name, share in WZ_WORKER_SHARE.items():
            persons_pct_pop = emp / share / population  # persons inflow per 1% of E, in % of N
            for outcome, (b, se) in WZ.items():
                rows.append({"employment_denominator": denom, "employment_march2021": emp,
                             "population_2021": population, "worker_share": share_name,
                             "worker_share_value": share, "persons_pct_pop_per_1pct_emp": persons_pct_pop,
                             "outcome": outcome, "coef_per_1pct_emp": b, "se_per_1pct_emp": se,
                             "coef_per_1pct_pop": b / persons_pct_pop,
                             "se_per_1pct_pop": se / persons_pct_pop})
    return pd.DataFrame(rows)


def main():
    DERIVED.mkdir(exist_ok=True)
    z = z1_series()
    z.to_csv(DERIVED / "inputs_land_foreign.csv", index=False)
    s = scf_shares()
    s.to_csv(DERIVED / "inputs_scf.csv", index=False)
    w = wz_conversion()
    w.to_csv(DERIVED / "inputs_wz.csv", index=False)
    r = rhfs_entities()
    r.to_csv(DERIVED / "inputs_rhfs.csv", index=False)
    print(r.round(4).to_string(index=False))
    pd.set_option("display.width", 200)
    print(z[["quarter", "land_share_owner_occupied", "land_share_noncorp_residential",
             "foreign_share_noncorp_real_estate", "foreign_equity_share_noncorp_real_estate"]])
    print(s)
    print(w[["employment_denominator", "worker_share", "outcome", "persons_pct_pop_per_1pct_emp",
             "coef_per_1pct_pop", "se_per_1pct_pop"]])


if __name__ == "__main__":
    main()
