#!/usr/bin/env python3
"""Arm A check: does the white comparison group change when "third-plus
generation" is used instead of "US-born"?

The ACS has no parental birthplace, so arm A compares against all US-born
non-Hispanic whites. The CPS ASEC does carry parental nativity (PEFNTVTY,
PEMNTVTY), so this script rebuilds the same creative-employment rate on ASEC
March 2025 for four groups:

  white_usborn     US-born, non-Hispanic, white
  white_3plus      US-born with both parents US-born, non-Hispanic, white
  mex_2nd          US-born, Mexican origin, at least one parent born in Mexico
  mex_3plus        US-born, Mexican origin, both parents US-born
  mexborn          born in Mexico

Occupation: PEIOOCC, the CPS main-job occupation code. The creative set is
read from the API's own value labels (the "ENT-" prefix), not assumed to match
the ACS OCCP numbering. The ASEC API serves this table by state, not us:*.

Caveat stated in the memo: this extract carries only the ASEC person weight,
not the 160 replicate weights, so the figures here are point estimates with
unweighted counts and no design-based SE. They are a direction check on the
group definition, not a replacement for the ACS estimates.

Output: derived/arm_a_cps_generation_check.csv
"""
import os
import sys
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "cps"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)

API = "https://api.census.gov/data/2025/cps/asec/mar"
VARS = ["PEIOOCC", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PEHSPNON", "PRDTHSP",
        "PRDTRACE", "A_AGE", "A_HGA", "A_SEX", "MARSUPWT", "PEMLR"]

# The CPS occupation frame is close to the ACS one but not identical, so the
# creative codes are taken from the API's own value labels ("ENT-" prefix)
# rather than assumed. Athletes, coaches and umpires are excluded, as in arm A.
SPORTS_WORDS = ("ATHLETE", "COACH", "UMPIRE", "SCOUT", "SPORTS OFFICIAL")


def creative_codes(key: str) -> set:
    r = requests.get(f"{API}/variables.json", timeout=300)
    r.raise_for_status()
    items = r.json()["variables"]["PEIOOCC"]["values"]["item"]
    codes = set()
    for code, label in items.items():
        up = label.upper()
        if up.startswith("ENT-") and not any(w in up for w in SPORTS_WORDS):
            codes.add(int(code))
    return codes
MEXICO = 303          # CPS nativity code for Mexico, same frame as ACS POBP
US_CODES = set(range(57, 100)) | {57}   # US states/DC/outlying areas < 100


def main() -> None:
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        sys.exit("CENSUS_API_KEY not set; source config.local.env")
    CREATIVE_INT = creative_codes(key)
    print(f"creative PEIOOCC codes: {len(CREATIVE_INT)}", flush=True)
    if len(CREATIVE_INT) < 20:
        sys.exit(f"FAIL only {len(CREATIVE_INT)} creative codes resolved")
    raw = CACHE / "asec_2025_occ_extract.csv"
    if raw.exists():
        df = pd.read_csv(raw)
    else:
        try:
            r = requests.get(API, params={"get": ",".join(VARS), "for": "state:*",
                                          "key": key}, timeout=600)
            r.raise_for_status()
        except requests.HTTPError as exc:
            # never surface the request URL: it carries the API key
            sys.exit(f"FAIL ASEC request returned "
                     f"{exc.response.status_code if exc.response else '?'}")
        if not r.text.lstrip().startswith("["):
            sys.exit(f"FAIL non-JSON body: {r.text[:200]!r}")
        rows = r.json()
        df = pd.DataFrame(rows[1:], columns=rows[0])
        for c in VARS:
            df[c] = pd.to_numeric(df[c], errors="coerce")
        df.to_csv(raw, index=False)
    print(f"ASEC rows={len(df):,}", flush=True)
    if len(df) < 100_000:
        sys.exit(f"FAIL only {len(df):,} ASEC rows, expected ~140,000")

    d = df[(df.A_AGE >= 25) & (df.A_AGE <= 64)].copy()
    d["us_born"] = d["PENATVTY"] < 100
    d["mother_us"] = d["PEMNTVTY"] < 100
    d["father_us"] = d["PEFNTVTY"] < 100
    d["hisp"] = d["PEHSPNON"] == 1
    d["white"] = d["PRDTRACE"] == 1
    d["mex_origin"] = d["PRDTHSP"] == 1          # Mexican detailed Hispanic
    d["employed"] = d["PEMLR"].isin([1, 2])
    d["creative"] = d["employed"] & d["PEIOOCC"].isin(CREATIVE_INT)
    d["w"] = d["MARSUPWT"]

    groups = {
        "white_usborn": d.us_born & ~d.hisp & d.white,
        "white_3plus": (d.us_born & ~d.hisp & d.white & d.mother_us
                        & d.father_us),
        "mex_2nd": (d.us_born & d.mex_origin
                    & ((d.PEMNTVTY == MEXICO) | (d.PEFNTVTY == MEXICO))),
        "mex_3plus": d.us_born & d.mex_origin & d.mother_us & d.father_us,
        "mexborn": d.PENATVTY == MEXICO,
    }
    out = []
    for name, mask in groups.items():
        sub = d[mask]
        pop_w = sub["w"].sum()
        creat_w = sub.loc[sub.creative, "w"].sum()
        emp_w = sub.loc[sub.employed, "w"].sum()
        out.append({
            "group": name,
            "n_unweighted": len(sub),
            "n_creative_unweighted": int(sub.creative.sum()),
            "weighted_pop": round(float(pop_w), 1),
            "creative_per_1k_pop": round(float(creat_w / pop_w * 1000), 3),
            "creative_per_1k_emp": round(float(creat_w / emp_w * 1000), 3),
            "ba_plus_share": round(float(
                sub.loc[sub.A_HGA >= 43, "w"].sum() / pop_w), 4),
        })
    res = pd.DataFrame(out)
    base = res.loc[res.group == "white_usborn", "creative_per_1k_pop"].iloc[0]
    res["ratio_to_white_usborn"] = (res["creative_per_1k_pop"] / base).round(4)
    res.to_csv(DER / "arm_a_cps_generation_check.csv", index=False)
    print(res.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
