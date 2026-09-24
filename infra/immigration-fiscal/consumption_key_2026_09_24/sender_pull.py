"""Pull CPS Unbanked/Underbanked supplement person records (2011-2019) from the Census API.

Run from the repository root:
    set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/consumption_key_2026_09_24/sender_pull.py

Writes _cache/senders/unbank_<year>.json (API list-of-lists). Never prints the key; curl errors
are printed with the key redacted.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "_cache" / "senders"
KEY = os.environ.get("CENSUS_API_KEY", "")

COMMON = [
    "HRHHID", "HRHHID2", "PULINENO", "PERRP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
    "PRDTHSP", "PEHSPNON", "PRCITSHP", "PRTAGE", "HHSUPWGT", "PWSUPWGT", "PRSUPINT",
    "HRINTSTA", "HURESPLI", "GESTFIPS", "HEFAMINC", "HRMIS",
]
YEARS = {
    2011: ("jun", ["HES20", "HES21", "HES22"]),
    2013: ("jun", ["HES20", "HES21", "HES22"]),
    2015: ("jun", ["HES130", "HES131", "HES133", "PRINUYER"]),
    2017: ("jun", ["HES130", "HES1351", "HES1352", "HES1353", "PRINUYER"]),
    2019: ("jun", ["HENBRM10", "HENBRM15", "PRINUYER"]),
}


def fetch(year: int, month: str, cols: list[str]) -> list:
    url = f"https://api.census.gov/data/{year}/cps/unbank/{month}?get={','.join(cols)}&key={KEY}"
    r = subprocess.run(["curl", "-sS", "--fail", "-L", url], capture_output=True, text=True)
    if r.returncode != 0:
        msg = (r.stderr or "").replace(KEY, "<redacted>")
        raise RuntimeError(f"{year}: curl rc={r.returncode} {msg[:300]}")
    body = r.stdout
    if not body.lstrip().startswith("[["):
        raise RuntimeError(f"{year}: non-JSON body: {body[:300].replace(KEY, '<redacted>')}")
    return json.loads(body)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for year, (month, extra) in YEARS.items():
        out = OUT / f"unbank_{year}.json"
        if out.exists():
            print(year, "cached", out.name)
            continue
        if not KEY:
            sys.exit("[BLOCKED] CENSUS_API_KEY not set")
        rows = fetch(year, month, COMMON + extra)
        out.write_text(json.dumps(rows))
        print(year, "rows", len(rows) - 1, "cols", len(rows[0]))


if __name__ == "__main__":
    main()
