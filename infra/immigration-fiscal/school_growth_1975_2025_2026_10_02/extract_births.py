"""Extract the published Pew table from cached HTML; --fetch acquires it first."""
import argparse
import csv
from pathlib import Path
from bs4 import BeautifulSoup
import requests

HERE = Path(__file__).resolve().parent
URL = "https://www.pewresearch.org/chart/sr_26-04-31_birthrightscotus/"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    cache = HERE / "_cache/pew_births.html"
    if args.fetch:
        if cache.exists():
            raise SystemExit("[BLOCKED] raw source already exists; preserve it")
        response = requests.get(URL, timeout=60)
        response.raise_for_status()
        cache.parent.mkdir(exist_ok=True)
        cache.write_text(response.text)
    soup = BeautifulSoup(cache.read_text(), "html.parser")
    tables = [t for t in soup.find_all("table")
              if "All births to unauthorized immigrant mothers" in t.get_text()]
    assert len(tables) == 1, "[BLOCKED] missing or ambiguous source table"
    rows = [[c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"])]
            for tr in tables[0].find_all("tr")]
    assert len(rows) == 35 and rows[1] == ["2023", "300", "245"]
    assert rows[-1] == ["1990", "120", "95"]
    (HERE / "inputs").mkdir(exist_ok=True)
    with (HERE / "inputs/pew_births.csv").open("w", newline="") as handle:
        csv.writer(handle, lineterminator="\n").writerows(rows)
    print("PASS: 34 published birth estimates, units thousands")


if __name__ == "__main__":
    main()
