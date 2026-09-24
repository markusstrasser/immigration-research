"""Arm 4, task 3: decennial census group-quarters counts by Hispanic origin and correctional type.

2010 SF1 PCT20 / PCT20H / PCT20I publish the detailed correctional types by Hispanic origin (federal
detention centers 101, federal prisons 102, state prisons 103, local jails and other municipal confinement
104, correctional residential 105, military disciplinary 106). The 2020 DHC publishes Hispanic origin only
for the major type "correctional facilities for adults" (PCT18H, by sex x age) and the detailed types
without race (PCT19). For 2020 the local-jail Hispanic share is therefore estimated on counties whose adult
correctional population is all local jail (no 101-103, 105-106 residents), which identifies the jail share
without a race-by-type table.

Pulls nation, states and counties; raw JSON to _cache/jail/, tidy output to derived/jail_census_gq.csv
(2010 by type and geography) and derived/jail_census2020_counties.csv (2020 county file).

Run from the repository root:
    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/jail_census_gq.py 2>&1 | sed 's/key=[^&]*/key=REDACTED/g'
"""
import json, os, pathlib, re, subprocess, sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache/jail"
DERIVED = HERE / "derived"
KEY = os.environ.get("CENSUS_API_KEY", "")
TYPES = {"101": "federal_detention", "102": "federal_prisons", "103": "state_prisons", "104": "local_jails",
         "105": "correctional_residential", "106": "military_disciplinary"}


def redact(s: str) -> str:
    return re.sub(r"key=[^&\s]*", "key=REDACTED", s)


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def curl_json(url: str, out: pathlib.Path, keyed: bool = True):
    if out.exists():
        return json.loads(out.read_text())
    full = url + (f"&key={KEY}" if keyed and KEY else "")
    r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "300", full], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(redact(f"curl rc={r.returncode}: {r.stderr[:300]}"))
    data = json.loads(r.stdout)
    out.write_text(json.dumps(data))
    return data


def fetch(base: str, vars_: list, geo: str, out: pathlib.Path) -> pd.DataFrame:
    g = geo.replace(":", "%3A").replace("*", "%2A").replace(" ", "%20")
    data = curl_json(f"{base}?get=NAME,{','.join(vars_)}&for={g}", out)
    df = pd.DataFrame(data[1:], columns=data[0])
    for v in vars_:
        df[v] = pd.to_numeric(df[v])
    return df


# ------------------------------------------------------------------ 2010 SF1
def sf1_2010() -> pd.DataFrame:
    base = "https://api.census.gov/data/2010/dec/sf1"
    meta = {g: json.loads((CACHE / f"sf1_2010_{g}_vars.json").read_text())["variables"] for g in ("PCT20", "PCT20H", "PCT20I")}
    cols = {}
    for g, prefix in (("PCT20", "PCT020"), ("PCT20H", "PCT020H"), ("PCT20I", "PCT020I")):
        for code, name in list(TYPES.items()) + [("all", "adult_correctional")]:
            want = "Correctional facilities for adults (101-106)" + ("" if code == "all" else f"!!")
            hits = [k for k, v in meta[g].items() if k.startswith(prefix) and k[len(prefix):].isdigit()
                    and v["label"].split("!!")[-1] == (want if code == "all" else v["label"].split("!!")[-1])
                    and (v["label"].endswith("Correctional facilities for adults (101-106)") if code == "all"
                         else v["label"].endswith(f"({code})") and "Correctional facilities for adults" in v["label"])]
            if len(hits) != 1:
                raise RuntimeError(f"{g} {code}: {hits}")
            cols[(g, name)] = hits[0]
    rows = []
    for geo, tag in (("us:1", "us"), ("state:*", "state"), ("county:*", "county")):
        parts = []
        for g in ("PCT20", "PCT20H", "PCT20I"):
            vs = [cols[(g, n)] for n in list(TYPES.values()) + ["adult_correctional"]]
            parts.append(fetch(base, vs, geo, CACHE / f"sf1_2010_{g}_{tag}.json"))
        keys = [c for c in parts[0].columns if c in ("us", "state", "county")]
        m = parts[0].merge(parts[1], on=keys + ["NAME"]).merge(parts[2], on=keys + ["NAME"])
        if "state" in m.columns:
            m = m[m["state"] != "72"]  # Puerto Rico is outside the national total
        for _, r in m.iterrows():
            geo_id = "us" if tag == "us" else (r["state"] if tag == "state" else r["state"] + r["county"])
            for n in list(TYPES.values()) + ["adult_correctional"]:
                rows.append({"year": 2010, "level": tag, "geo": geo_id, "name": r["NAME"], "type": n,
                             "total": r[cols[("PCT20", n)]], "hispanic": r[cols[("PCT20H", n)]],
                             "nh_white": r[cols[("PCT20I", n)]]})
    df = pd.DataFrame(rows)
    us = df[(df.level == "us")].set_index("type")
    gate("2010 SF1 detailed correctional types add to the adult correctional total",
         us.loc[list(TYPES.values()), "total"].sum() == us.loc["adult_correctional", "total"],
         f"{us.loc['adult_correctional', 'total']:,}")
    gate("2010 SF1 Hispanic types add up", us.loc[list(TYPES.values()), "hispanic"].sum() == us.loc["adult_correctional", "hispanic"],
         f"{us.loc['adult_correctional', 'hispanic']:,}")
    for lvl in ("state", "county"):
        s = df[df.level == lvl].groupby("type")[["total", "hispanic"]].sum()
        gate(f"2010 {lvl} rows sum to the nation", (s.loc[us.index, ["total", "hispanic"]].values ==
                                                    us[["total", "hispanic"]].values).all(), f"{len(df[df.level == lvl]) // 7} units")
    return df


# ------------------------------------------------------------------ 2020 DHC
def dhc_2020() -> pd.DataFrame:
    base = "https://api.census.gov/data/2020/dec/dhc"
    mh = json.loads((CACHE / "dhc2020_PCT18H_vars.json").read_text())["variables"]
    m18 = json.loads((CACHE / "dhc2020_P18_vars.json").read_text())["variables"]
    m19 = json.loads((CACHE / "dhc2020_PCT19_vars.json").read_text())["variables"]
    corr = "Correctional facilities for adults (101-106)"
    hisp = sorted(k for k, v in mh.items() if k.endswith("N") and v["label"].endswith(corr))
    allr = sorted(k for k, v in m18.items() if k.endswith("N") and v["label"].endswith(corr))
    det = {code: sorted(k for k, v in m19.items() if k.endswith("N") and v["label"].endswith(f"({code})")
                        and "Correctional facilities for adults" in v["label"]) for code in TYPES}
    gate("2020 DHC variables resolved", len(hisp) == 6 and len(allr) == 6 and all(len(v) == 6 for v in det.values()),
         f"PCT18H {len(hisp)}, P18 {len(allr)}, PCT19 {[len(v) for v in det.values()]}")
    out = []
    for geo, tag in (("us:1", "us"), ("state:*", "state"), ("county:*", "county")):
        a = fetch(base, allr, geo, CACHE / f"dhc2020_P18corr_{tag}.json")
        h = fetch(base, hisp, geo, CACHE / f"dhc2020_PCT18Hcorr_{tag}.json")
        d = fetch(base, [v for vs in det.values() for v in vs], geo, CACHE / f"dhc2020_PCT19corr_{tag}.json")
        keys = [c for c in a.columns if c in ("us", "state", "county")] + ["NAME"]
        m = a.merge(h, on=keys).merge(d, on=keys)
        if "state" in m.columns:
            m = m[m["state"] != "72"].copy()  # Puerto Rico is outside the national total
        m["adult_correctional"] = m[allr].sum(axis=1)
        m["hispanic_adult_correctional"] = m[hisp].sum(axis=1)
        for code, name in TYPES.items():
            m[name] = m[det[code]].sum(axis=1)
        m["level"] = tag
        m["geo"] = "us" if tag == "us" else (m["state"] if tag == "state" else m["state"] + m["county"])
        out.append(m[["level", "geo", "NAME", "adult_correctional", "hispanic_adult_correctional"] + list(TYPES.values())])
    df = pd.concat(out, ignore_index=True)
    us = df[df.level == "us"].iloc[0]
    gate("2020 DHC detailed types add to the adult correctional total", us[list(TYPES.values())].sum() == us.adult_correctional,
         f"{us.adult_correctional:,}")
    for lvl in ("state", "county"):
        s = df[df.level == lvl][["adult_correctional", "hispanic_adult_correctional"]].sum()
        gate(f"2020 {lvl} rows sum to the nation", s.adult_correctional == us.adult_correctional
             and s.hispanic_adult_correctional == us.hispanic_adult_correctional, f"{(df.level == lvl).sum()} units")
    return df


def main() -> None:
    if not KEY:
        sys.exit("[BLOCKED] CENSUS_API_KEY not exported")
    DERIVED.mkdir(exist_ok=True)
    s10 = sf1_2010()
    s10.to_csv(DERIVED / "jail_census_gq.csv", index=False, lineterminator="\n")
    us10 = s10[s10.level == "us"].set_index("type")
    us10["hisp_share"] = us10.hispanic / us10.total
    print("\n[2010 SF1, United States, April 1 2010]")
    print(us10[["total", "hispanic", "nh_white", "hisp_share"]].to_string())
    d20 = dhc_2020()
    d20.to_csv(DERIVED / "jail_census2020_counties.csv", index=False, lineterminator="\n")
    us20 = d20[d20.level == "us"].iloc[0]
    print("\n[2020 DHC, United States, April 1 2020]")
    print(f"  adult correctional {us20.adult_correctional:,}, Hispanic {us20.hispanic_adult_correctional:,} "
          f"({us20.hispanic_adult_correctional / us20.adult_correctional:.4f})")
    print("  " + ", ".join(f"{n} {us20[n]:,}" for n in TYPES.values()))


if __name__ == "__main__":
    main()
