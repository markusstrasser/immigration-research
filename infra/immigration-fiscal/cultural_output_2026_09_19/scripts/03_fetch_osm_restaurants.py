#!/usr/bin/env python3
"""Arm D step 1: fetch every OSM restaurant / fast-food feature in the 50 states
plus DC from the Overpass API, one state at a time, into _cache/osm/.

Each state file is validated by content: it must parse as JSON, carry an
`elements` list, and contain at least a floor number of features for that state
(1 per 20,000 residents is a loose floor; a truncated body fails it).

Output: _cache/osm/<ST>.json   (raw Overpass JSON, gitignored)
        _cache/osm/_manifest.json
"""
import json
import os
import sys
import time
from pathlib import Path

import requests

LANE = Path(__file__).resolve().parent.parent
OUT = LANE / "_cache" / "osm"
OUT.mkdir(parents=True, exist_ok=True)

# kumi.systems accepted connections but never answered (observed 2026-09-19),
# so the main endpoint is used alone with slot polling and retries
ENDPOINTS = ["https://overpass-api.de/api/interpreter"]
# kumi.systems answers /api/status with an empty body, so only the main
# endpoint is slot-polled (checked 2026-09-19)
STATUS = {
    "https://overpass-api.de/api/interpreter": "https://overpass-api.de/api/status",
}
# a browser UA is rejected by overpass-api.de with HTTP 406; a descriptive
# research UA is accepted (checked 2026-09-19)
HEADERS = {"User-Agent": "immigration-research-lane/1.0 (cultural-output arm D)"}


def wait_for_slot(url: str, tries: int = 20) -> None:
    """Poll the Overpass status endpoint until a query slot is free.

    Mirrors that answer /api/status with an empty body carry no slot
    information; for those we go straight to the query rather than spin.
    """
    if url not in STATUS:
        return
    for _ in range(tries):
        try:
            r = requests.get(STATUS[url], headers=HEADERS, timeout=60)
            txt = r.text
        except Exception:  # noqa: BLE001
            time.sleep(20)
            continue
        if "available now" in txt:
            return
        if "Rate limit" not in txt:      # unparseable/empty status: just try
            return
        wait = 30
        for line in txt.splitlines():
            if "Slot available after" in line:
                tail = line.rsplit("in", 1)[-1].strip().rstrip(" seconds.")
                if tail.isdigit():
                    wait = min(300, max(10, int(tail) + 5))
                break
        print(f"  waiting {wait}s for a slot", flush=True)
        time.sleep(wait)

STATES = ["AL", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA",
          "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
          "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX",
          "UT", "VT", "VA", "WA", "WV", "WI", "WY", "AK"]

# Alaska's admin_level=4 area query does not return inside the Overpass time
# limit (observed 2026-09-19), so it is fetched by bounding box instead. The
# boxes spill into Canada; those points fall outside every US CBSA polygon and
# are dropped at the assignment step, so the spill cannot inflate any count.
BBOX = {"AK": [(51.0, -180.0, 72.0, -129.0), (51.0, 172.0, 56.0, 180.0)]}

BBOX_QUERY = """[out:json][timeout:900][maxsize:1073741824];
(
{clauses}
);
out center;
"""

# loose per-state floors on feature count; a truncated response fails these
FLOOR = {"DC": 500, "WY": 300, "VT": 300, "AK": 300, "ND": 300, "SD": 300,
         "DE": 300, "RI": 300, "MT": 300, "NH": 300, "ME": 300, "HI": 400}
DEFAULT_FLOOR = 800

QUERY = """[out:json][timeout:900][maxsize:1073741824];
area["ISO3166-2"="US-{st}"][admin_level=4]->.a;
nwr["amenity"~"^(restaurant|fast_food)$"](area.a);
out center;
"""


def query_for(st: str) -> str:
    if st in BBOX:
        clauses = "\n".join(
            'nwr["amenity"~"^(restaurant|fast_food)$"]'
            f"({s},{w},{n},{e});" for s, w, n, e in BBOX[st])
        return BBOX_QUERY.format(clauses=clauses)
    return QUERY.format(st=st)


def fetch_state(st: str) -> dict:
    last = None
    for attempt in range(6):
        url = ENDPOINTS[attempt % len(ENDPOINTS)]
        wait_for_slot(url)
        try:
            r = requests.post(url, data={"data": query_for(st)},
                              headers=HEADERS, timeout=1000)
            if r.status_code in (429, 504, 502, 503):
                last = f"HTTP {r.status_code}"
                time.sleep(60 * (attempt + 1))
                continue
            r.raise_for_status()
            data = r.json()
            if "elements" not in data:
                last = "no elements key"
                time.sleep(20)
                continue
            n = len(data["elements"])
            floor = FLOOR.get(st, DEFAULT_FLOOR)
            if n < floor:
                last = f"only {n} elements (floor {floor}) - likely truncated"
                time.sleep(30)
                continue
            return data
        except Exception as exc:  # noqa: BLE001
            last = repr(exc)[:200]
            print(f"  {st} attempt {attempt} error {last}", flush=True)
            time.sleep(60 * (attempt + 1))
    raise RuntimeError(f"{st}: {last}")


def cached_ok(p: Path, st: str) -> int:
    """A cached state file counts only if its CONTENT still validates."""
    if not p.exists():
        return 0
    try:
        data = json.loads(p.read_text())
    except Exception:  # noqa: BLE001
        return 0
    n = len(data.get("elements", []))
    return n if n >= FLOOR.get(st, DEFAULT_FLOOR) else 0


def main() -> None:
    # two workers can split the list: LANE_MOD=2 with LANE_REM=0 and 1. Each
    # writes its own manifest so the two never race on the same file.
    mod = int(os.environ.get("LANE_MOD", "1"))
    rem = int(os.environ.get("LANE_REM", "0"))
    manifest = {}
    mpath = OUT / f"_manifest_{rem}of{mod}.json"
    if mpath.exists():
        manifest = json.loads(mpath.read_text())
    todo = [s for i, s in enumerate(STATES) if i % mod == rem]
    # LANE_STATES overrides the partition: used to prioritise the states that
    # carry the high end of the Mexican-origin share regressor (TX, NM, NV, UT)
    explicit = os.environ.get("LANE_STATES", "").strip()
    if explicit:
        todo = [s.strip().upper() for s in explicit.split(",") if s.strip()]
        mpath = OUT / f"_manifest_explicit_{rem}.json"
        manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    print(f"worker {rem}/{mod}: {len(todo)} states", flush=True)
    for st in todo:
        p = OUT / f"{st}.json"
        n_cached = cached_ok(p, st)
        if n_cached:
            manifest[st] = {"ok": True, "n": n_cached, "cached": True}
            print(f"{st} cached n={n_cached}", flush=True)
            continue
        t0 = time.time()
        try:
            data = fetch_state(st)
        except RuntimeError as exc:
            print(f"{st} FAILED {exc}", flush=True)
            manifest[st] = {"ok": False, "error": str(exc)}
            mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True))
            continue
        # atomic write: two workers may reach the same state, and a partial
        # file would silently truncate that state's counts
        tmp = p.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(data))
        os.replace(tmp, p)
        n = len(data["elements"])
        manifest[st] = {"ok": True, "n": n, "secs": round(time.time() - t0, 1)}
        mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True))
        print(f"{st} n={n} {manifest[st]['secs']}s", flush=True)
        time.sleep(5)
    bad = [s for s, v in manifest.items() if not v.get("ok")]
    print(f"done ok={sum(1 for v in manifest.values() if v.get('ok'))} "
          f"failed={bad}", flush=True)
    if bad:
        sys.exit(1)


if __name__ == "__main__":
    main()
