"""Raw CBP growth before any model: California, the rest of the US and Los Angeles County.

Sums county establishments and employment from the CBP panel (fetch_cbp.py) for 2016, 2018, 2019 and
2023 and reports percent growth 2016-2018, 2018-2019 and 2018-2023. Puerto Rico is excluded.
Suppressed county employment is stored as 0, so employment sums are approximate for small counties;
2017 onward CBP drops some small cells, so the 2016-2018 column mixes publication rules.

Writes derived/descriptive_ca_us.csv. Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/descriptive.py
"""
import pandas as pd

from lib import CACHE, DERIVED

YEARS = (2016, 2018, 2019, 2023)
CODES = ("7225", "722511", "722513", "722330", "445110")


def main() -> None:
    p = pd.read_csv(CACHE / "cbp_county_panel.csv", dtype={"naics": str, "fips": str})
    p["fips"] = p["fips"].str.zfill(5)
    p = p[~p["fips"].str.startswith("72") & p["year"].isin(YEARS) & p["naics"].isin(CODES)]
    areas = {"CA": p["fips"].str.startswith("06"), "rest of US": ~p["fips"].str.startswith("06"),
             "LA County": p["fips"] == "06037"}
    rows = []
    for code in CODES:
        for area, mask in areas.items():
            for var in ("estab", "emp"):
                s = p[mask & (p["naics"] == code)].groupby("year")[var].sum()
                if s.index.nunique() != len(YEARS):
                    raise SystemExit(f"[FAILED] {code} {area} {var}: years {sorted(s.index)}")
                r = {"naics": code, "area": area, "var": var, **{f"y{y}": int(s[y]) for y in YEARS}}
                r["g1618"] = round(100 * (s[2018] / s[2016] - 1), 1)
                r["g1819"] = round(100 * (s[2019] / s[2018] - 1), 1)
                r["g1823"] = round(100 * (s[2023] / s[2018] - 1), 1)
                rows.append(r)
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "descriptive_ca_us.csv", index=False, lineterminator="\n")
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
