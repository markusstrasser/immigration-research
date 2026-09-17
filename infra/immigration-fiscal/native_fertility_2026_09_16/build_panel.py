"""Assemble the CBSA-level native-fertility / foreign-born-share panel from cached ACS JSON."""
import json, pathlib
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"


def load(dataset, year, group, tag="cbsa"):
    p = CACHE / f"{dataset}_{year}_{group}_{tag}.json"
    d = json.loads(p.read_text())
    hdr = list(d[0])
    seen = set()
    for i, c in enumerate(hdr):          # `get=NAME,group(X)` emits NAME twice
        if c in seen:
            hdr[i] = f"{c}__dup{i}"
        seen.add(c)
    df = pd.DataFrame(d[1:], columns=hdr)
    keep = [c for c in df.columns if c.endswith("E") and c.startswith(group)]
    geo = "metropolitan statistical area/micropolitan statistical area"
    idcols = ["NAME", geo] if geo in df.columns else ["NAME"]
    out = df[idcols + keep].copy()
    for c in keep:
        out[c] = pd.to_numeric(out[c], errors="coerce")
    out.loc[:, keep] = out[keep].mask(out[keep] < -1e8)  # Census null sentinels
    if geo in df.columns:
        out = out.rename(columns={geo: "cbsa"})
    return out


def merge(dataset, year, groups):
    dfs = [load(dataset, year, g) for g in groups]
    out = dfs[0]
    for d in dfs[1:]:
        out = out.merge(d.drop(columns=["NAME"]), on="cbsa", how="outer")
    return out


def women_age_windows(df):
    """B01001 female ages 20–34 and 15–50; age 50 is approximated within 50–54."""
    f = {i: df[f"B01001_{i:03d}E"] for i in range(30, 41)}
    return sum(f[i] for i in range(32, 37)), sum(f[i] for i in range(30, 40)) + 0.2 * f[40]


def derive(df, educ_group):
    d = pd.DataFrame({"cbsa": df["cbsa"], "name": df["NAME"]})
    nat_births = df["B13008_004E"] + df["B13008_007E"]
    nat_women = nat_births + df["B13008_011E"] + df["B13008_014E"]
    fb_births = df["B13008_005E"] + df["B13008_008E"]
    fb_women = fb_births + df["B13008_012E"] + df["B13008_015E"]
    d["native_births"] = nat_births
    d["native_women_15_50"] = nat_women
    d["native_birth_rate"] = nat_births / nat_women * 1000
    d["fb_births"] = fb_births
    d["fb_women_15_50"] = fb_women
    d["fb_birth_rate"] = fb_births / fb_women * 1000
    d["all_birth_rate"] = df["B13008_002E"] / df["B13008_001E"] * 1000
    d["pop"] = df["B05012_001E"]
    d["fb_share"] = df["B05012_003E"] / df["B05012_001E"] * 100
    d["median_rent"] = df["B25064_001E"]
    d["median_hh_income"] = df["B19013_001E"]
    d["black_share"] = df["B03002_004E"] / df["B03002_001E"] * 100
    d["hisp_share"] = df["B03002_012E"] / df["B03002_001E"] * 100
    d["ownership_rate"] = df["B25003_002E"] / df["B25003_001E"] * 100
    d["median_age_native_female"] = df["B05004_006E"]
    if educ_group == "B15003":
        ba = df[[f"B15003_{i:03d}E" for i in (22, 23, 24, 25)]].sum(axis=1)
        d["ba_plus_share"] = ba / df["B15003_001E"] * 100
    else:  # B15002: sex-split, male 15-18 = BA..doctorate, female 32-35
        ba = df[[f"B15002_{i:03d}E" for i in (15, 16, 17, 18, 32, 33, 34, 35)]].sum(axis=1)
        d["ba_plus_share"] = ba / df["B15002_001E"] * 100
    # women 20-34 as a share of women 15-50 (age structure of the fertility window)
    w20_34, w15_50 = women_age_windows(df)
    d["share_women_20_34"] = w20_34 / w15_50 * 100
    d["women_15_50_all"] = w15_50
    return d


def national(dataset, year):
    b = load(dataset, year, "B13008", "us")
    n = load(dataset, year, "B05012", "us")
    nb = b["B13008_004E"] + b["B13008_007E"]
    nw = nb + b["B13008_011E"] + b["B13008_014E"]
    return dict(native_birth_rate=float((nb / nw * 1000).iloc[0]),
                native_births=int(nb.iloc[0]),
                fb_share=float((n["B05012_003E"] / n["B05012_001E"] * 100).iloc[0]))


SPECS = {
    "acs1_2023": ("acs_acs1", "2023", ["B13008", "B05012", "B25064", "B19013", "B03002",
                                       "B25003", "B01001", "B15003", "B05004"], "B15003"),
    "acs1_2010": ("acs_acs1", "2010", ["B13008", "B05012", "B25064", "B19013", "B03002",
                                       "B25003", "B01001", "B15002", "B05004"], "B15002"),
    "acs5_2019": ("acs_acs5", "2019", ["B13008", "B05012", "B25064", "B19013", "B03002",
                                       "B25003", "B01001", "B15003", "B05004"], "B15003"),
}


def build(spec):
    ds, yr, groups, educ = SPECS[spec]
    return derive(merge(ds, yr, groups), educ)


if __name__ == "__main__":
    for spec in SPECS:
        ds, yr, _, _ = SPECS[spec]
        d = build(spec)
        nat = national(ds, yr)
        agg_rate = d["native_births"].sum() / d["native_women_15_50"].sum() * 1000
        # metro aggregation covers only CBSAs published at this vintage; compare rate not level
        err = (agg_rate - nat["native_birth_rate"]) / nat["native_birth_rate"] * 100
        print(f"[GATE-a] {spec}: metro-agg native birth rate {agg_rate:.2f} vs "
              f"national B13008 {nat['native_birth_rate']:.2f} -> {err:+.2f}% "
              f"({'PASS' if abs(err) < 3 else 'FAIL'})")
        for code, nm in (("31080", "Los Angeles"), ("26420", "Houston")):
            row = d[d.cbsa == code]
            if len(row):
                print(f"         {nm} fb_share={row.fb_share.iloc[0]:.2f}  "
                      f"native_birth_rate={row.native_birth_rate.iloc[0]:.2f}")
        d.to_csv(HERE / f"panel_{spec}.csv", index=False)
