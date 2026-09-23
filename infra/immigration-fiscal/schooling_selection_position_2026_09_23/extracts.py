"""Submit, poll and download this lane's IPUMS extracts.

  ipumsi       Mexico census and Conteo/Intercensal samples 1970-2020, residents aged 18+: the
               origin-side attainment distribution by birth year and sex. Refused on 2026-09-23
               (HTTP 401: the account is not registered to IPUMS International).
  usa          #3: Mexico-born (BPL 200) records from the 1980/1990/2000 5% censuses and every
               single-year ACS 2005-2024: the migrant side, with SEX (the held panel has none).
  usa_acs0004  #12: the same records from the ACS 2000-2004 (instrument check).
  usa_qeduc    #13: the education allocation flag QEDUC for every record of #3 and #12.

Extract numbers are recorded in _cache/extracts.json. Data land in _cache/ (git-ignored).

  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/extracts.py submit
  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/extracts.py status
  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/extracts.py wait --max-minutes 45
  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/extracts.py download
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ipums_api as api  # noqa: E402

REG = HERE / "_cache" / "extracts.json"

MX_SAMPLES = ["mx1970a", "mx1990a", "mx1995a", "mx2000a", "mx2005a", "mx2010a", "mx2015a", "mx2020a"]
MX_VARS = ["AGE", "SEX", "NATIVITY", "YRSCHOOL", "EDATTAIN", "EDUCMX", "SCHOOL", "PERWT"]

US_SAMPLES = ["us1980a", "us1990a", "us2000a"] + [f"us{y}a" for y in range(2005, 2025)]
US_VARS = ["PERWT", "STRATA", "CLUSTER", "GQ", "SEX", "AGE", "BIRTHYR", "BPL", "YRIMMIG",
           "CITIZEN", "EDUC", "SCHOOL", "GRADEATT"]

ACS0004_SAMPLES = ["us2000d", "us2001a", "us2002a", "us2003a", "us2004a"]

SPECS = {
    "ipumsi": ("mx_origin", "schooling selection lane: Mexico residents 18+, schooling by birth year and sex",
               MX_SAMPLES, MX_VARS, {"AGE": [f"{a:03d}" for a in range(18, 101)]}),
    "usa": ("us_mexborn", "schooling selection lane: Mexico-born, 1980-2000 censuses and ACS 2005-2024",
            US_SAMPLES, US_VARS, {"BPL": ["200"]}),
    # Instrument diagnostic: the 2000-2004 ACS observe the 1995-99 cohort at the same time as the
    # 2000 census long form.
    "usa_acs0004": ("us_mexborn_acs0004", "schooling selection lane: Mexico-born, ACS 2000-2004",
                    ACS0004_SAMPLES, US_VARS, {"BPL": ["200"]}),
    # Allocation diagnostic: the Census Bureau imputes education for a share of Mexican-born
    # respondents from donors not matched on nativity. QEDUC flags allocated values.
    "usa_qeduc": ("us_mexborn_qeduc", "schooling selection lane: Mexico-born, education allocation flag",
                  US_SAMPLES + ACS0004_SAMPLES, ["BPL", "EDUC"], {"BPL": ["200"]}),
}
# Variables whose IPUMS data-quality flag (QEDUC etc.) the extract requests.
FLAGS = {"usa_qeduc": ["EDUC"]}
COLLECTION = {"ipumsi": "ipumsi", "usa": "usa", "usa_acs0004": "usa", "usa_qeduc": "usa"}


def body(collection: str) -> dict:
    _, desc, samples, variables, cases = SPECS[collection]
    v = {name: {} for name in variables}
    for name, codes in cases.items():
        v[name] = {"caseSelections": {"general": codes}}
    for name in FLAGS.get(collection, []):
        v[name]["dataQualityFlags"] = True
    return {"description": desc, "dataStructure": {"rectangular": {"on": "P"}}, "dataFormat": "csv",
            "samples": {s: {} for s in samples}, "variables": v}


def load() -> dict:
    return json.loads(REG.read_text()) if REG.exists() else {}


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("command", choices=["submit", "status", "wait", "download"])
    p.add_argument("--only", choices=list(SPECS))
    p.add_argument("--max-minutes", type=int, default=45)
    a = p.parse_args()
    reg = load()
    colls = [a.only] if a.only else list(SPECS)
    if a.command == "submit":
        for c in colls:
            if c in reg:
                print(f"{c}: already submitted as #{reg[c]}")
                continue
            reg[c] = api.submit(COLLECTION[c], body(c))
            REG.parent.mkdir(exist_ok=True)
            REG.write_text(json.dumps(reg, indent=2))
            print(f"{c}: submitted #{reg[c]}")
    elif a.command == "status":
        for c in colls:
            if c in reg:
                print(c, reg[c], api.status(COLLECTION[c], reg[c]).get("status"))
    elif a.command == "wait":
        for c in colls:
            if c in reg:
                print(c, api.wait(COLLECTION[c], reg[c], a.max_minutes * 60))
    else:
        for c in colls:
            if c in reg and api.status(COLLECTION[c], reg[c]).get("status") == "completed":
                print(c, api.download(COLLECTION[c], reg[c], SPECS[c][0]))
            elif c in reg:
                print(c, "not completed")


if __name__ == "__main__":
    main()
