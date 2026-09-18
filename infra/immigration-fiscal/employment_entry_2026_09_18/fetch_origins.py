"""Fetch the ingredients of a MULTI-ORIGIN shift-share instrument.

A single-origin (Mexico-only) instrument cannot implement the Jaeger-Ruist-Stuhler
correction: the current and lagged predicted inflows are then both the same metro base
share times a scalar, so they are nearly collinear across metros and the two-endogenous /
two-instrument system is not identified in practice. JRS's own fix is variation from
CHANGES IN THE NATIONAL ORIGIN MIX, which requires many origin groups.

  base shares  : Census 2000 SF3 PCT019, all leaf country/region categories, county level
  national shifts: ACS 1-year B05006 (place of birth for the foreign-born), US total, per year
"""
import json, os, pathlib, urllib.parse, urllib.request, time

HERE = pathlib.Path(__file__).parent
CACHE = HERE / "_cache"
KEY = os.environ.get("CENSUS_API_KEY", "")
# Only the window endpoints are needed for the shift-share national shifts.
YEARS = [int(y) for y in os.environ.get(
    "PUMS_YEARS", "2005,2008,2010,2013,2015,2018,2023").split(",")]


def get(url, tries=4):
    for t in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception as e:
            if t == tries - 1:
                raise
            time.sleep(5 * (t + 1))


def leaf_vars(group_json, prefix):
    """Keep only leaf categories (no other label extends this one).

    SF3 labels read 'Total!!Americas!!...'; ACS labels read 'Estimate!!Total!!Americas!!...'
    and also carry 'Margin of Error!!' twins, so the ACS prefix is stripped and the margin
    rows dropped before the leaf test.
    """
    lab = {}
    for k, v in group_json["variables"].items():
        if not k.startswith(prefix):
            continue
        l = v["label"]
        if l.startswith("Margin of Error!!") or k.endswith("M"):
            continue
        if l.startswith("Estimate!!"):
            l = l[len("Estimate!!"):]
        # later ACS vintages punctuate every non-leaf level with a trailing colon
        l = l.replace(":!!", "!!").rstrip(":")
        if not l.startswith("Total!!"):
            continue
        lab[k] = l
    vals = set(lab.values())
    return {k: l for k, l in lab.items()
            if not any(o != l and o.startswith(l + "!!") for o in vals)}


def main():
    # ---- 2000 base, county level ----
    out_base = CACHE / "sf3_2000_county_origins.json"
    g = get("https://api.census.gov/data/2000/dec/sf3/groups/PCT019.json")
    leaves = leaf_vars(g, "PCT019")
    json.dump(leaves, open(CACHE / "pct019_leaves.json", "w"), indent=1)
    print("SF3 leaf origin categories:", len(leaves))
    if not out_base.exists():
        names = sorted(leaves)
        merged, header = {}, None
        for i in range(0, len(names), 45):
            chunk = names[i:i + 45]
            q = {"get": ",".join(chunk), "for": "county:*"}
            if KEY:
                q["key"] = KEY
            d = get("https://api.census.gov/data/2000/dec/sf3?" + urllib.parse.urlencode(q))
            h = d[0]
            si, ci = h.index("state"), h.index("county")
            for row in d[1:]:
                k = row[si].zfill(2) + row[ci].zfill(3)
                rec = merged.setdefault(k, {})
                for name in chunk:
                    rec[name] = int(row[h.index(name)])
            print("  county chunk", i, "vars", len(chunk), flush=True)
        json.dump(merged, open(out_base, "w"))
        print("wrote", out_base, len(merged), "counties")

    # ---- national stocks by origin, per ACS year ----
    out_nat = CACHE / "acs_b05006_national.json"
    if out_nat.exists():
        print("skip", out_nat.name); return
    partial = CACHE / "acs_b05006_partial.json"
    nat = json.load(open(partial)) if partial.exists() else {}
    for y in YEARS:
        if str(y) in nat and nat[str(y)]:
            print("have", y, len(nat[str(y)])); continue
        gj = None
        for attempt in range(8):
            try:
                gj = get(f"https://api.census.gov/data/{y}/acs/acs1/groups/B05006.json", tries=1)
                if leaf_vars(gj, "B05006"):
                    break
                gj = None
            except Exception:
                gj = None
            time.sleep(3 * (attempt + 1))
        if gj is None:
            print(f"SKIP {y}: group metadata would not download intact")
            continue
        lv = {k: v for k, v in leaf_vars(gj, "B05006").items() if k.endswith("E")}
        if not lv:
            print(f"SKIP {y}: no leaf categories parsed"); continue
        names = sorted(lv)
        vals = {}
        for i in range(0, len(names), 45):
            chunk = names[i:i + 45]
            q = {"get": ",".join(chunk), "for": "us:1"}
            if KEY:
                q["key"] = KEY
            d = get(f"https://api.census.gov/data/{y}/acs/acs1?" + urllib.parse.urlencode(q))
            h, row = d[0], d[1]
            for name in chunk:
                v = row[h.index(name)]
                vals[lv[name]] = int(v) if v not in (None, "", "null") else 0
        nat[str(y)] = vals
        json.dump(nat, open(partial, "w"))
        print("B05006", y, "categories", len(vals), flush=True)
    json.dump(nat, open(out_nat, "w"))
    print("wrote", out_nat, "years", sorted(nat))


if __name__ == "__main__":
    main()
