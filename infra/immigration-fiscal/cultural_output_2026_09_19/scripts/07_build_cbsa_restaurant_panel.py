#!/usr/bin/env python3
"""Arm D step 3: assign OSM restaurant/fast-food features to CBSAs and build the
per-CBSA cuisine panel.

Inputs : _cache/osm/*.json                (Overpass, one file per state)
         _cache/tiger/cb_2023_us_cbsa_500k.zip
         derived/cbsa_covariates.csv      (ACS 2019-2023 5-year)
Output : derived/cbsa_restaurant_panel.csv
         derived/osm_cuisine_coverage.json

OSM caveats stated in the memo: cuisine tagging is voluntary and uneven, so the
denominator "all restaurants" includes untagged ones while "mexican" can only
count tagged ones. The tagged share is reported by state so the reader can see
the coverage gradient.
"""
import json
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
import shapefile  # pyshp
from shapely.geometry import shape, Point
from shapely.prepared import prep
from shapely.strtree import STRtree

LANE = Path(__file__).resolve().parent.parent
OSM = LANE / "_cache" / "osm"
TIGER = LANE / "_cache" / "tiger"
DER = LANE / "derived"

CUISINES = {
    "mexican": r"mexican|tex[-_ ]?mex|taco|burrito|taqueria",
    "chinese": r"chinese|szechuan|sichuan|cantonese|dim_sum",
    "italian": r"italian|pizza",
    "indian": r"indian|punjabi|tandoori",
    "thai": r"thai",
    "japanese": r"japanese|sushi|ramen",
    "vietnamese": r"vietnamese|pho",
    "korean": r"korean",
    "american": r"american|burger|steak_house|barbecue|bbq",
}
PATS = {k: re.compile(v, re.I) for k, v in CUISINES.items()}

# Independent classifier: the establishment NAME, which OSM carries far more
# often than a cuisine tag. Used to check whether the cuisine-tag count misses
# Mexican restaurants differentially across metros.
NAME_MEX = re.compile(
    r"taqueri|taco|burrito|cantina|tortill|mexic|azteca|chipotle|qdoba"
    r"|del taco", re.I)


def load_cbsa_index():
    zp = TIGER / "cb_2023_us_cbsa_500k.zip"
    with zipfile.ZipFile(zp) as z:
        z.extractall(TIGER)
    sf = shapefile.Reader(str(TIGER / "cb_2023_us_cbsa_500k"))
    fields = [f[0] for f in sf.fields[1:]]
    geoms, meta = [], []
    for sr in sf.shapeRecords():
        rec = dict(zip(fields, sr.record))
        g = shape(sr.shape.__geo_interface__)
        geoms.append(g)
        meta.append({"cbsa": rec.get("CBSAFP") or rec.get("GEOID"),
                     "name": rec.get("NAME"),
                     "lsad": rec.get("LSAD")})
    tree = STRtree(geoms)
    prepared = [prep(g) for g in geoms]
    return tree, geoms, prepared, meta


def iter_features():
    """Yield each distinct OSM feature once. Alaska is fetched by bounding box
    rather than by area, so a feature can in principle appear in more than one
    state file; dedup on (type, id) makes that harmless."""
    seen = set()
    for p in sorted(OSM.glob("*.json")):
        if p.name.startswith("_"):
            continue
        st = p.stem
        data = json.loads(p.read_text())
        for el in data["elements"]:
            key = (el.get("type"), el.get("id"))
            if key in seen:
                continue
            seen.add(key)
            if el["type"] == "node":
                lat, lon = el.get("lat"), el.get("lon")
            else:
                c = el.get("center") or {}
                lat, lon = c.get("lat"), c.get("lon")
            if lat is None or lon is None:
                continue
            tags = el.get("tags", {})
            yield (st, lat, lon, tags.get("amenity", ""),
                   tags.get("cuisine", ""), tags.get("name", ""))


def main() -> None:
    tree, geoms, prepared, meta = load_cbsa_index()
    print(f"cbsa polygons={len(geoms)}", flush=True)

    counts = defaultdict(Counter)       # cbsa -> Counter of categories
    state_tagged = Counter()
    state_total = Counter()
    n_pts = n_in = 0
    for st, lat, lon, amenity, cuisine, name in iter_features():
        n_pts += 1
        state_total[st] += 1
        if cuisine:
            state_tagged[st] += 1
        pt = Point(lon, lat)
        cbsa = None
        for idx in tree.query(pt):
            if prepared[idx].contains(pt):
                cbsa = meta[idx]["cbsa"]
                break
        if cbsa is None:
            continue
        n_in += 1
        c = counts[cbsa]
        c["all"] += 1
        if amenity == "restaurant":
            c["restaurant"] += 1
        if name:
            c["named"] += 1
            if NAME_MEX.search(name):
                c["mexican_by_name"] += 1
        if cuisine:
            c["tagged"] += 1
            for name, pat in PATS.items():
                if pat.search(cuisine):
                    c[name] += 1
        if n_pts % 100000 == 0:
            print(f"  [{n_pts:,}] points, {n_in:,} inside a CBSA", flush=True)

    print(f"points={n_pts:,} inside_cbsa={n_in:,}", flush=True)
    rows = []
    for cbsa, c in counts.items():
        row = {"cbsa": cbsa, **{k: c[k] for k in
                                ["all", "restaurant", "tagged", "named",
                                 "mexican_by_name"] + list(CUISINES)}}
        rows.append(row)
    panel = pd.DataFrame(rows)
    cov = pd.read_csv(DER / "cbsa_covariates.csv", dtype={"cbsa": str})
    panel["cbsa"] = panel["cbsa"].astype(str).str.zfill(5)
    cov["cbsa"] = cov["cbsa"].astype(str).str.zfill(5)
    panel = cov.merge(panel, on="cbsa", how="left").fillna({
        k: 0 for k in ["all", "restaurant", "tagged", "named",
                       "mexican_by_name"] + list(CUISINES)})
    # a CBSA can straddle states; it is only usable when EVERY state it spans
    # has been fetched, otherwise its restaurant count is partial
    fetched = {p.stem for p in OSM.glob("*.json") if not p.name.startswith("_")}
    def states_of(name: str) -> set:
        tail = str(name).rsplit(",", 1)[-1]
        return {t.strip() for t in re.split(r"[-\s]+", tail) if len(t.strip()) == 2}
    panel["cbsa_states"] = panel["NAME"].apply(lambda n: "+".join(sorted(states_of(n))))
    panel["all_states_fetched"] = panel["NAME"].apply(
        lambda n: bool(states_of(n)) and states_of(n) <= fetched)
    print(f"states fetched={len(fetched)} "
          f"CBSAs fully covered={int(panel['all_states_fetched'].sum())}",
          flush=True)
    panel.to_csv(DER / "cbsa_restaurant_panel.csv", index=False)

    cover = {
        "osm_points": n_pts,
        "points_inside_cbsa": n_in,
        "cuisine_tagged_share_by_state": {
            st: round(state_tagged[st] / state_total[st], 4)
            for st in sorted(state_total)
        },
        "national_tagged_share": round(sum(state_tagged.values())
                                       / max(1, sum(state_total.values())), 4),
        "cuisine_patterns": CUISINES,
        "name_classifier_pattern": NAME_MEX.pattern,
        "osm_snapshot": "Overpass API, fetched 2026-09-19",
    }
    (DER / "osm_cuisine_coverage.json").write_text(
        json.dumps(cover, indent=2, sort_keys=True) + "\n")
    print(f"wrote panel rows={len(panel)} "
          f"mexican_total={panel['mexican'].sum():,.0f}", flush=True)


if __name__ == "__main__":
    main()
