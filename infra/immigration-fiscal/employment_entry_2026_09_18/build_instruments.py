"""Build the multi-origin (JRS-implementable) shift-share ingredients.

Writes:
  derived/metro_origin_base.csv     metro x origin, share of the NATIONAL 2000 stock of that origin
  derived/national_origin_stock.csv origin x ACS year, national foreign-born stock

Origin labels are matched between Census 2000 SF3 PCT019 and ACS B05006 on the leaf
country name. Categories present in one source only are dropped, and the drop is reported.
"""
import json, pathlib
import pandas as pd

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)


def leaf(label):
    return label.split("!!")[-1].strip().lower()


def load_cbsa():
    d = pd.read_excel(CACHE / "omb_delineation_2013_list1.xls", skiprows=2)
    d = d[d["Metropolitan/Micropolitan Statistical Area"] == "Metropolitan Statistical Area"]
    d = d.dropna(subset=["FIPS State Code", "FIPS County Code"])
    d["cofips"] = (d["FIPS State Code"].astype(int).astype(str).str.zfill(2)
                   + d["FIPS County Code"].astype(int).astype(str).str.zfill(3))
    d["cbsa"] = d["CBSA Code"].astype(str).str.strip()
    return d[["cofips", "cbsa"]]


def main():
    leaves = json.load(open(CACHE / "pct019_leaves.json"))          # var -> full label
    county = json.load(open(CACHE / "sf3_2000_county_origins.json"))  # cofips -> {var: n}
    natf = CACHE / "acs_b05006_national.json"
    if not natf.exists():
        natf = CACHE / "acs_b05006_partial.json"
    nat_raw = {y: v for y, v in json.load(open(natf)).items() if v}   # year -> {label: n}

    sf_leaf = {v: leaf(l) for v, l in leaves.items()}
    acs_years = sorted(int(y) for y in nat_raw)
    acs_leaf_sets = [{leaf(l) for l in nat_raw[str(y)]} for y in acs_years]
    acs_common = set.intersection(*acs_leaf_sets)
    sf_names = set(sf_leaf.values())
    common = sorted(sf_names & acs_common)
    print(f"SF3 leaves {len(sf_names)}, ACS leaves common to all years {len(acs_common)}, "
          f"matched {len(common)}")
    print("dropped from SF3:", sorted(sf_names - acs_common)[:12])

    rows = []
    for cofips, rec in county.items():
        acc = {}
        for var, n in rec.items():
            nm = sf_leaf.get(var)
            if nm in common:
                acc[nm] = acc.get(nm, 0) + n
        for nm, n in acc.items():
            rows.append((cofips, nm, n))
    cty = pd.DataFrame(rows, columns=["cofips", "origin", "n2000"])

    cbsa = load_cbsa()
    met = (cty.merge(cbsa, on="cofips", how="inner")
              .groupby(["cbsa", "origin"], as_index=False)["n2000"].sum())
    natl2000 = cty.groupby("origin")["n2000"].sum().rename("natl2000")
    met = met.merge(natl2000, on="origin", how="left")
    met["base_share"] = met["n2000"] / met["natl2000"].replace(0, pd.NA)
    met = met.dropna(subset=["base_share"])
    met.to_csv(DERIVED / "metro_origin_base.csv", index=False)
    print("metro-origin rows", len(met), "metros", met.cbsa.nunique(),
          "origins", met.origin.nunique())

    nrows = []
    for y in acs_years:
        acc = {}
        for l, n in nat_raw[str(y)].items():
            nm = leaf(l)
            if nm in common:
                acc[nm] = acc.get(nm, 0) + n
        for nm, n in acc.items():
            nrows.append((y, nm, n))
    nat = pd.DataFrame(nrows, columns=["year", "origin", "natl_stock"])
    nat.to_csv(DERIVED / "national_origin_stock.csv", index=False)
    piv = nat.pivot(index="year", columns="origin", values="natl_stock")
    print("national stock matrix", piv.shape)
    print("Mexico national stock by year:")
    print(piv["mexico"].to_string())
    tot = piv.sum(axis=1)
    print("all matched origins total by year (thousands):")
    print((tot / 1000).round(0).to_string())


if __name__ == "__main__":
    main()
