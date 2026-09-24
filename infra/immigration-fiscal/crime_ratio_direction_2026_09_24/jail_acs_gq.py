"""Arm 4, task 2: Hispanic share of the ACS adult correctional facilities population.

National: ACS subject table S2603 ("Characteristics of the group quarters population by group quarters
type (5 types)"), column "Adult correctional facilities", 1-year 2021-2024 and 5-year 2019, 2023, 2024.
S2603 carries no state values (the API returns nulls), so states come from S2602 (3 types), which the
Census Bureau publishes for states in the 5-year files only. State adult (18+) Hispanic shares come from
B01001/B01001I for the same vintages. Variable IDs are resolved from each vintage's labels because subject
table row numbers move between years.

Raw JSON goes to _cache/jail/, the tidy table to derived/jail_acs_gq.csv.

Run from the repository root (the Census key must be exported; it is never printed):
    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/jail_acs_gq.py 2>&1 | sed 's/key=[^&]*/key=REDACTED/g'
"""
import json, os, pathlib, re, subprocess, sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache/jail"
DERIVED = HERE / "derived"
KEY = os.environ.get("CENSUS_API_KEY", "")

# wanted rows of the "Adult correctional facilities" column: name -> label suffix after the column name
ROWS = {
    "count": "!!Total population",
    "under18": "!!Total population!!SEX AND AGE!!Under 18 years",  # a count in S2602/S2603
    "pct_white_alone": "!!Total population!!RACE AND HISPANIC ORIGIN OR LATINO ORIGIN!!One race!!White",
    "pct_black_alone": "!!Total population!!RACE AND HISPANIC ORIGIN OR LATINO ORIGIN!!One race!!Black or African American",
    "pct_some_other_race": "!!Total population!!RACE AND HISPANIC ORIGIN OR LATINO ORIGIN!!One race!!Some other race",
    "pct_hispanic": "!!Total population!!RACE AND HISPANIC ORIGIN OR LATINO ORIGIN!!Hispanic or Latino (of any race)",
    "pct_nh_white": "!!Total population!!RACE AND HISPANIC ORIGIN OR LATINO ORIGIN!!White alone, Not Hispanic or Latino",
    "foreign_born": "!!PLACE OF BIRTH, NATIVITY AND CITIZENSHIP STATUS, AND YEAR OF ENTRY!!Total population!!Foreign born",  # count
    "noncitizen": "!!PLACE OF BIRTH, NATIVITY AND CITIZENSHIP STATUS, AND YEAR OF ENTRY!!Total population!!Foreign born!!Not a U.S. citizen",  # count
}
NATIONAL = [("acs1", 2021), ("acs1", 2022), ("acs1", 2023), ("acs1", 2024), ("acs5", 2019), ("acs5", 2023), ("acs5", 2024)]
STATE = [("acs5", 2019), ("acs5", 2023), ("acs5", 2024)]
ADULTS_ONLY = [("acs1", 2010)]  # state adult Hispanic shares for the 2010 census comparison
# adults 18+: B01001 male 007-025 and female 031-049; B01001I male 007-016 and female 022-031
B01001_ADULT = [f"B01001_{i:03d}E" for i in list(range(7, 26)) + list(range(31, 50))]
B01001I_ADULT = [f"B01001I_{i:03d}E" for i in list(range(7, 17)) + list(range(22, 32))]


def redact(s: str) -> str:
    return re.sub(r"key=[^&\s]*", "key=REDACTED", s)


def curl_json(url: str, out: pathlib.Path, keyed: bool = True):
    if out.exists():
        return json.loads(out.read_text())
    full = url + (f"&key={KEY}" if keyed and KEY else "")
    r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "180", full], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(redact(f"curl rc={r.returncode}: {r.stderr[:300]}"))
    data = json.loads(r.stdout)
    out.write_text(json.dumps(data))
    return data


def resolve(table: str, ds: str, year: int) -> dict:
    """name -> (estimate var, moe var) for the adult correctional column, matched on full labels."""
    meta = curl_json(f"https://api.census.gov/data/{year}/acs/{ds}/subject/groups/{table}.json",
                     CACHE / f"{table}_groups_{ds}_{year}.json", keyed=False)["variables"]
    col = "Estimate!!Adult correctional facilities"
    out = {}
    for name, suffix in ROWS.items():
        hits = [k for k, v in meta.items() if k.endswith("E") and v["label"] == col + suffix]
        if len(hits) != 1:
            raise RuntimeError(f"{table} {ds} {year}: {name} matched {hits}")
        out[name] = (hits[0], hits[0][:-1] + "M")
    return out


def pull(table: str, ds: str, year: int, geo: str, tag: str) -> pd.DataFrame:
    ids = resolve(table, ds, year)
    vars_ = [v for pair in ids.values() for v in pair]
    g = geo.replace(":", "%3A").replace("*", "%2A")
    data = curl_json(f"https://api.census.gov/data/{year}/acs/{ds}/subject?get=NAME,{','.join(vars_)}&for={g}",
                     CACHE / f"{table}_{ds}_{year}_{tag}.json")
    hdr = data[0]
    rows = []
    for rec in data[1:]:
        d = dict(zip(hdr, rec))
        row = {"table": table, "product": ds, "year": year, "geo": "us" if tag == "us" else d["state"], "name": d["NAME"]}
        for name, (e, m) in ids.items():
            row[name] = float(d[e]) if d[e] not in (None, "") else float("nan")
            row[name + "_moe"] = float(d[m]) if d[m] not in (None, "") else float("nan")
        rows.append(row)
    return pd.DataFrame(rows)


def adults(ds: str, year: int) -> pd.DataFrame:
    rows = []
    for geo, tag in (("us:1", "us"), ("state:*", "state")):
        g = geo.replace(":", "%3A").replace("*", "%2A")
        a = curl_json(f"https://api.census.gov/data/{year}/acs/{ds}?get=NAME,{','.join(B01001_ADULT)}&for={g}",
                      CACHE / f"b01001_adult_{ds}_{year}_{tag}.json")
        h = curl_json(f"https://api.census.gov/data/{year}/acs/{ds}?get=NAME,{','.join(B01001I_ADULT)}&for={g}",
                      CACHE / f"b01001i_adult_{ds}_{year}_{tag}.json")
        gate(f"B01001 headers {ds} {year} {tag}", a[0][1:1 + len(B01001_ADULT)] == B01001_ADULT
             and h[0][1:1 + len(B01001I_ADULT)] == B01001I_ADULT, "adult cells in order")
        ha = {r[-1]: sum(float(x) for x in r[1:1 + len(B01001I_ADULT)]) for r in h[1:]}
        for r in a[1:]:
            rows.append({"product": ds, "year": year, "geo": "us" if tag == "us" else r[-1],
                         "adults": sum(float(x) for x in r[1:1 + len(B01001_ADULT)]), "hisp_adults": ha[r[-1]]})
    return pd.DataFrame(rows)


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'ok ' if ok else 'FAIL'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def main() -> None:
    if not KEY:
        sys.exit("[BLOCKED] CENSUS_API_KEY not exported")
    frames = [pull("S2603", ds, y, "us:1", "us") for ds, y in NATIONAL]
    frames += [pull("S2602", ds, y, "us:1", "us") for ds, y in STATE]
    frames += [pull("S2602", ds, y, "state:*", "state") for ds, y in STATE]
    df = pd.concat(frames, ignore_index=True)
    df = df[df.geo != "72"].reset_index(drop=True)
    ad = pd.concat([adults(ds, y) for ds, y in sorted(set(NATIONAL) | set(ADULTS_ONLY))], ignore_index=True)
    ad = ad[ad.geo != "72"].reset_index(drop=True)
    ad["adult_hisp_share"] = ad.hisp_adults / ad.adults
    df = df.merge(ad, on=["product", "year", "geo"], how="left")
    df["hisp_count"] = df["count"] * df["pct_hispanic"] / 100
    df["adult_hisp_share"] = df["hisp_adults"] / df["adults"]
    for (ds, y), g in df[df.table == "S2603"].groupby(["product", "year"]):
        us = g.iloc[0]
        gate(f"S2603 {ds} {y} national", 0 < us.pct_hispanic < 100 and us.pct_hispanic_moe < 5 and us["count"] > 1e6,
             f"adult correctional {us['count']:,.0f} (MOE {us.count_moe:,.0f}), Hispanic {us.pct_hispanic:.1f}% "
             f"(MOE {us.pct_hispanic_moe:.1f}), adults Hispanic {us.adult_hisp_share:.4f}")
    for ds, y in STATE:
        s = df[(df.table == "S2602") & (df["product"] == ds) & (df.year == y)]
        us, st = s[s.geo == "us"].iloc[0], s[~s.geo.isin(["us", "72"])]  # Puerto Rico is outside the nation
        n3 = df[(df.table == "S2603") & (df["product"] == ds) & (df.year == y)].iloc[0]
        gate(f"S2602 {ds} {y} states sum to nation", abs(st["count"].sum() / us["count"] - 1) < 0.005
             and len(st) == 51 and st["count"].notna().all(), f"{st['count'].sum():,.0f} vs {us['count']:,.0f}")
        gate(f"S2602 = S2603 nationally {ds} {y}", us["count"] == n3["count"] and us.pct_hispanic == n3.pct_hispanic,
             f"{us['count']:,.0f} / {us.pct_hispanic}")
        hs = (st["count"] * st.pct_hispanic / 100).sum() / st["count"].sum() * 100
        gate(f"S2602 {ds} {y} state Hispanic counts rebuild the national share", abs(hs - us.pct_hispanic) < 0.15,
             f"{hs:.2f}% vs {us.pct_hispanic}%")
    DERIVED.mkdir(exist_ok=True)
    df.to_csv(DERIVED / "jail_acs_gq.csv", index=False, lineterminator="\n")
    ad.to_csv(DERIVED / "jail_acs_adults.csv", index=False, lineterminator="\n")
    cols = ["table", "product", "year", "count", "count_moe", "pct_hispanic", "pct_hispanic_moe", "hisp_count",
            "pct_nh_white", "foreign_born", "noncitizen", "under18", "adult_hisp_share"]
    print(df[df.geo == "us"][cols].to_string(index=False))


if __name__ == "__main__":
    main()
