"""Tract-level exposure of residents outside each group to the group (ACS 2020-2024 5-year).

Exposure of outsiders to group g = sum_t (pop_t - g_t) * (g_t / pop_t) / sum_t (pop_t - g_t):
the average share of group-g residents in the tract of a person outside the group.

Mexican-origin: B03001_004E from crime_victim_cost_2026_09_23's cached tract pulls (read-only).
Non-Hispanic Black alone: B03002_004E, pulled here per state into _cache/ (key read from
acquire/config.local.env and never printed; errors are redacted).
"""
import json
import os
import re
import sys
import urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
CACHE = LANE / "_cache"
MEX_CACHE = FISCAL / "crime_victim_cost_2026_09_23" / "_cache"
OUT = LANE / "derived" / "exposure.csv"
BASE = "https://api.census.gov/data/2024/acs/acs5"


def key():
    env = FISCAL / "acquire" / "config.local.env"
    for line in env.read_text().splitlines():
        m = re.match(r"\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*['\"]?([^'\"\s]+)", line)
        if m:
            return m.group(1)
    return os.environ.get("CENSUS_API_KEY", "")


def redact(s, k):
    return s.replace(k, "REDACTED") if k else s


def pull_black(states, k):
    for st in states:
        out = CACHE / f"acs5_2024_b03002_tract_{st}.json"
        if out.exists() and out.stat().st_size > 100:
            continue
        url = f"{BASE}?get=B03002_001E,B03002_004E&for=tract:*&in=state:{st}&key={k}"
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                out.write_bytes(r.read())
        except Exception as e:  # noqa: BLE001
            raise SystemExit(f"[BLOCKED] B03002 pull failed for state {st}: {redact(str(e), k)}")


def exposure(rows, tot_col, g_col):
    num = den = gtot = ptot = 0.0
    for r in rows:
        try:
            p, g = float(r[tot_col]), float(r[g_col])
        except (TypeError, ValueError):
            continue
        if p <= 0 or g < 0:
            continue
        out = p - g
        num += out * (g / p)
        den += out
        gtot += g
        ptot += p
    return num / den, gtot / ptot, ptot


def load(path):
    data = json.loads(path.read_text())
    hdr = data[0]
    return [dict(zip(hdr, r)) for r in data[1:]]


def main():
    mex_files = sorted(MEX_CACHE.glob("acs5_2024_b03001_tract_*.json"))
    states = [f.stem.rsplit("_", 1)[1] for f in mex_files]
    if len(states) != 51:
        sys.exit(f"[BLOCKED] expected 51 cached B03001 state files, found {len(states)}")
    mex_rows = [r for f in mex_files for r in load(f)]
    k = key()
    if not k:
        sys.exit("[BLOCKED] no Census key found")
    pull_black(states, k)
    blk_rows = [r for st in states for r in load(CACHE / f"acs5_2024_b03002_tract_{st}.json")]
    e_mex, s_mex, p_mex = exposure(mex_rows, "B03001_001E", "B03001_004E")
    e_blk, s_blk, p_blk = exposure(blk_rows, "B03002_001E", "B03002_004E")
    lines = ["group,outsider_exposure_share,national_share,tracts,population",
             f"mexican_origin_b03001,{e_mex:.5f},{s_mex:.5f},{len(mex_rows)},{p_mex:.0f}",
             f"nh_black_alone_b03002,{e_blk:.5f},{s_blk:.5f},{len(blk_rows)},{p_blk:.0f}"]
    OUT.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
