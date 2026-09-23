"""SES-expected enlistment from neighbourhood income: DoD accession shares by home-tract income
quintile, applied to each group's distribution across the same quintiles.

DoD source (verified from the primary PDF, not a summary): *Population Representation in the
Military Services*, FY23 and FY22, Appendix B Table B-41, non-prior-service active-component
enlisted accessions by the median household income of the home-of-record CENSUS TRACT. The
brief said "home ZIP"; the table is by tract. Quintile cut-points split all US households into
fifths (2019-2023 ACS for FY23, 2018-2022 for FY22). This script rebuilds the FY23 cut-points
from ACS 2019-2023 tract data as a gate, then counts each group's population, youth and
households by quintile.

Relative propensity per young person in quintile q = accession share_q / (15-17 share_q); the
15-17-year-olds live at the parental address that becomes the home of record. 18-24-year-olds
(college dormitories sit in low-income tracts) and households (DoD's own base) are shown too.
A group's SES-expected index = sum_q (group share_q x propensity_q), scaled so that the US-born
non-Hispanic white index is 1. It is the ratio to the white rate the group would show if only
home-tract income mattered. Group counts are all ages (tract tables have no age detail for
Mexican or Indian origin); youth-age versions for non-Hispanic whites, Hispanics and Asians show
how much that matters. US-born Mexican origin = Mexican Hispanic origin minus Mexico-born; US-born
Asian Indian = Asian Indian alone minus India-born (clipped at zero), both tract approximations.

Reads CENSUS_API_KEY from the environment and never prints it. Writes `_cache/tracts/*.json` and
`derived/neighborhood_quintiles.csv`, `derived/neighborhood_expected.csv`.
"""
import csv
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19",
          "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35",
          "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53",
          "54", "55", "56"]
VARIABLES = {
    "median_income": "B19013_001E", "households": "B11001_001E", "population": "B01001_001E",
    "native": "B05012_002E", "india_born": "B05006_060E", "mexico_born": "B05006_160E",
    "mexican_origin": "B03001_004E", "asian_indian": "B02015_021E", "nh_white": "B03002_003E",
    "youth_m18_19": "B01001_007E", "youth_m20": "B01001_008E", "youth_m21": "B01001_009E",
    "youth_m22_24": "B01001_010E", "youth_f18_19": "B01001_031E", "youth_f20": "B01001_032E",
    "youth_f21": "B01001_033E", "youth_f22_24": "B01001_034E",
    "nhw_m18_19": "B01001H_007E", "nhw_m20_24": "B01001H_008E", "nhw_f18_19": "B01001H_022E",
    "nhw_f20_24": "B01001H_023E",
    "hisp_m18_19": "B01001I_007E", "hisp_m20_24": "B01001I_008E", "hisp_f18_19": "B01001I_022E",
    "hisp_f20_24": "B01001I_023E",
    "asian_m18_19": "B01001D_007E", "asian_m20_24": "B01001D_008E", "asian_f18_19": "B01001D_022E",
    "asian_f20_24": "B01001D_023E",
    # 15-17-year-olds still live at the parental address that becomes the home of record
    "teen_m15_17": "B01001_006E", "teen_f15_17": "B01001_030E",
    "nhwteen_m15_17": "B01001H_006E", "nhwteen_f15_17": "B01001H_021E",
    "hispteen_m15_17": "B01001I_006E", "hispteen_f15_17": "B01001I_021E",
    "asianteen_m15_17": "B01001D_006E", "asianteen_f15_17": "B01001D_021E",
}
# Table B-41, NPS active-component enlisted accessions, total DoD: upper cut-points of quintiles
# 1-4 and the count of accessions in each quintile. [SOURCE: _cache/poprep_fy23_appendix_b.pdf
# p. 245 (report p. 275); _cache/poprep_fy22_b41.pdf p. 1 (report p. 284)]
POPREP = {
    "FY23": {"cuts": [54754, 70266, 86937, 113181], "accessions": [22636, 35526, 30573, 25097, 12746],
             "households": 126554189, "acs": "2019-2023"},
    "FY22": {"cuts": [52160, 67119, 83211, 108779], "accessions": [21917, 33067, 29758, 26359, 14860],
             "households": 124972054, "acs": "2018-2022"},
}
GROUPS = {
    "all_population": lambda t: t["population"],
    "us_born_all": lambda t: t["native"],
    "us_born_nh_white": lambda t: t["nh_white"],  # NH white alone, any nativity (~96% US-born)
    "mexican_origin_all": lambda t: t["mexican_origin"],
    "mexico_born": lambda t: t["mexico_born"],
    "us_born_mexican_origin": lambda t: np.clip(t["mexican_origin"] - t["mexico_born"], 0, None),
    "india_born": lambda t: t["india_born"],
    "asian_indian_all": lambda t: t["asian_indian"],
    "us_born_asian_indian": lambda t: np.clip(t["asian_indian"] - t["india_born"], 0, None),
    "youth_18_24_all": lambda t: sum(t[k] for k in VARIABLES if k.startswith("youth_")),
    "youth_18_24_nh_white": lambda t: sum(t[k] for k in VARIABLES if k.startswith("nhw_")),
    "youth_18_24_hispanic": lambda t: sum(t[k] for k in VARIABLES if k.startswith("hisp_")),
    "youth_18_24_asian": lambda t: sum(t[k] for k in VARIABLES if k.startswith("asian_")),
    "teen_15_17_all": lambda t: sum(t[k] for k in VARIABLES if k.startswith("teen_")),
    "teen_15_17_nh_white": lambda t: sum(t[k] for k in VARIABLES if k.startswith("nhwteen_")),
    "teen_15_17_hispanic": lambda t: sum(t[k] for k in VARIABLES if k.startswith("hispteen_")),
    "teen_15_17_asian": lambda t: sum(t[k] for k in VARIABLES if k.startswith("asianteen_")),
    "households": lambda t: t["households"],
}
# Denominators for "accessions per young person": 15-17-year-olds (primary: they live at the
# parental address), 18-24-year-olds (includes students in dormitory tracts), households (DoD's own).
BASES = {"per_teen_15_17": "teen_15_17_all", "per_youth_18_24": "youth_18_24_all", "per_household": "households"}


def fetch_state(state, key):
    target = CACHE / "tracts" / f"acs5_2023_{state}.json"
    if target.exists():
        return json.loads(target.read_text())
    url = (f"https://api.census.gov/data/2023/acs/acs5?get={','.join(VARIABLES.values())}"
           f"&for=tract:*&in=state:{state}&key={key}")
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=180) as response:
                payload = json.loads(response.read().decode())
            target.write_text(json.dumps(payload))
            return payload
        except Exception as error:  # the message can carry the key: report the class only
            print(f"  ! state {state}: {type(error).__name__} (attempt {attempt + 1})", flush=True)
            time.sleep(4)
    raise SystemExit(f"[BLOCKED] tract pull for state {state} failed four times")


def load_tracts():
    key = os.environ.get("CENSUS_API_KEY")
    (CACHE / "tracts").mkdir(parents=True, exist_ok=True)
    if not key and not all((CACHE / "tracts" / f"acs5_2023_{s}.json").exists() for s in STATES):
        raise SystemExit("[BLOCKED] CENSUS_API_KEY is not set")
    columns = {name: [] for name in VARIABLES}
    count = 0
    for state in STATES:
        header, *rows = fetch_state(state, key)
        index = {code: header.index(code) for code in VARIABLES.values()}
        for row in rows:
            for name, code in VARIABLES.items():
                value = row[index[code]]
                value = float(value) if value not in (None, "") else np.nan
                columns[name].append(np.nan if value < -1e8 else value)  # -666666666 = no estimate
        count += len(rows)
    tracts = {name: np.array(values) for name, values in columns.items()}
    for name in VARIABLES:
        if name != "median_income":
            tracts[name] = np.nan_to_num(tracts[name])
    return tracts, count


def weighted_cuts(values, weights, probabilities):
    order = np.argsort(values, kind="stable")
    cumulative = np.cumsum(weights[order]) / weights.sum()
    return [float(values[order][np.searchsorted(cumulative, p)]) for p in probabilities]


def main():
    DERIVED.mkdir(exist_ok=True)
    tracts, count = load_tracts()
    income = tracts["median_income"]
    has_income = ~np.isnan(income)
    households = tracts["households"]
    print(f"  ✓ {count:,} tracts; {has_income.sum():,} with a median income; households "
          f"{households.sum():,.0f} all, {households[has_income].sum():,.0f} in tracts with a median")
    mine = weighted_cuts(income[has_income], households[has_income], [0.2, 0.4, 0.6, 0.8])
    gate = POPREP["FY23"]
    print("  gate: household-weighted tract quintile cut-points, ACS 2019-2023, lane vs DoD FY23")
    for lane, dod in zip(mine, gate["cuts"]):
        print(f"    lane {lane:>9,.0f}   DoD {dod:>9,}   {lane / dod - 1:+.2%}")
    print(f"    households in tracts with a median: lane {households[has_income].sum():,.0f}, "
          f"DoD {gate['households']:,} ({households[has_income].sum() / gate['households'] - 1:+.2%})")

    quintile_rows, expected_rows = [], []
    for fy, table in POPREP.items():
        bins = np.digitize(income, np.array(table["cuts"]) + 0.5)  # cut-points are inclusive upper bounds
        bins = np.where(has_income, bins, -1)
        accessions = np.array(table["accessions"], float)
        accession_share = accessions / accessions.sum()
        shares = {}
        for group, count_fn in GROUPS.items():
            counts = np.asarray(count_fn(tracts), float)
            by_q = np.array([counts[bins == q].sum() for q in range(5)])
            shares[group] = by_q / by_q.sum()
            quintile_rows.append({"fiscal_year": fy, "group": group, "in_matched_tracts": round(by_q.sum()),
                                  "unmatched_share": round(counts[bins < 0].sum() / counts.sum(), 5),
                                  **{f"q{q + 1}_share": round(shares[group][q], 5) for q in range(5)}})
        quintile_rows.append({"fiscal_year": fy, "group": "dod_nps_accessions", "in_matched_tracts": int(accessions.sum()),
                              "unmatched_share": "", **{f"q{q + 1}_share": round(accession_share[q], 5) for q in range(5)}})
        for basis, denominator in BASES.items():
            propensity = accession_share / shares[denominator]
            white = float(shares["us_born_nh_white"] @ propensity)
            white_teen = float(shares["teen_15_17_nh_white"] @ propensity)
            for group in GROUPS:
                if group == "households":
                    continue
                index = float(shares[group] @ propensity)
                expected_rows.append({"fiscal_year": fy, "propensity_basis": basis, "group": group,
                                      "index_vs_denominator": round(index / float(shares[denominator] @ propensity), 5),
                                      "expected_ratio_to_nh_white": round(index / white, 5),
                                      "expected_ratio_to_nh_white_teens": round(index / white_teen, 5),
                                      **{f"propensity_q{q + 1}": round(propensity[q], 5) for q in range(5)}})
    for name, rows in (("neighborhood_quintiles.csv", quintile_rows), ("neighborhood_expected.csv", expected_rows)):
        with open(DERIVED / name, "w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
    print("\n  FY23, expected ratio to US-born NH white (all ages), by propensity denominator")
    print(f"    {'group':26s} " + " ".join(f"{basis:>16s}" for basis in BASES))
    for group in GROUPS:
        cells = [r["expected_ratio_to_nh_white"] for r in expected_rows
                 if r["fiscal_year"] == "FY23" and r["group"] == group]
        if cells:
            print(f"    {group:26s} " + " ".join(f"{c:16.3f}" for c in cells))
    leaked = [p.name for p in (CACHE / "tracts").glob("*.json") if "key=" in p.read_text()]
    assert not leaked, leaked


if __name__ == "__main__":
    sys.exit(main())
