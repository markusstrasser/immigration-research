"""Arm 4 removal vector: Mexico-born plus their US-born children under 18, by state.

Level anchored to the published ACS 2016-2020 Mexico-born count (B05006_150E); the children
multiplier comes from the IPUMS household proxy (kids_ipums.py), shrunk toward the national ratio
for states with thin Mexican-born samples:
    r_shrunk = (n_s * r_s + K * r_national) / (n_s + K),  K = 50,000 weighted persons.
"""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
DERIVED = HERE / "derived"
K = 50_000.0

if __name__ == "__main__":
    ratio = pd.read_csv(DERIVED / "kids_ipums_ratio.csv").set_index("state_name")
    counts = pd.read_csv(DERIVED / "state_counts.csv").set_index("NAME")
    mexborn = counts["mex_born_acs2020"]
    r = ratio["kids_per_mexborn_2020_interp"].reindex(mexborn.index)
    r_nat = (r * mexborn).sum() / mexborn.sum()
    r_shrunk = (mexborn * r + K * r_nat) / (mexborn + K)
    out = pd.DataFrame({
        "state_name": mexborn.index,
        "mexico_born": mexborn.values,
        "kids_ratio_raw": r.values,
        "kids_ratio_shrunk": r_shrunk.values,
        "us_born_kids": (mexborn * r_shrunk).round().astype(int).values,
    })
    out["mexborn_plus_kids"] = out["mexico_born"] + out["us_born_kids"]
    out.to_csv(DERIVED / "mexborn_plus_uskids.csv", index=False)
    print(f"national weighted kids-per-Mexico-born ratio: {r_nat:.3f}")
    print(f"US totals: Mexico-born {out.mexico_born.sum():,} + US-born children under 18 "
          f"{out.us_born_kids.sum():,} = {out.mexborn_plus_kids.sum():,}")
    print(out.sort_values("mexborn_plus_kids", ascending=False).head(6).to_string(index=False))
