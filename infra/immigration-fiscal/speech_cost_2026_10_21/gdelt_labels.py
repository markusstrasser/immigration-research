"""Share of US English-language online news articles on immigration that carry a prejudice label, GDELT DOC 2.0.

Pre-registered (RESULT.md Q4, route 2): monthly article counts for `immigration` and for
`immigration (racist OR xenophobic OR nativist OR "white supremacist")`, US sources, from 2017-01;
ratio = share of immigration articles carrying a label term. A third query gives the same share for an unrelated
topic (`taxes`), so a rise in label use across all news is not read as an immigration-specific rise.

GDELT allows one request per 5 s from an address but throttles shared addresses harder; the script waits 60 s
between calls and retries a 429 up to six times with 60 s, 120 s, ... backoff.
Raw responses are cached in `_cache/gdelt_*.csv`; delete them to re-pull (GDELT's index is revised, so a re-pull
may differ). Co-occurrence in one article does not show that the label was applied to restrictionists.

    uv run --no-project python3 infra/immigration-fiscal/speech_cost_2026_10_21/gdelt_labels.py
"""

import collections
import csv
import io
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
OUT = LANE / "derived"
API = "https://api.gdeltproject.org/api/v2/doc/doc"
LABEL = '(racist OR xenophobic OR nativist OR "white supremacist")'
FILTER = "sourcecountry:US sourcelang:english"
QUERIES = {
    "immigration": f"immigration {FILTER}",
    "immigration_label": f"immigration {LABEL} {FILTER}",
    "taxes": f"taxes {FILTER}",
    "taxes_label": f"taxes {LABEL} {FILTER}",
}
START, END = "20170101000000", "20261001000000"


def pull(name, query):
    path = CACHE / f"gdelt_{name}.csv"
    if path.exists() and path.stat().st_size > 1000:
        return path.read_text()
    params = urllib.parse.urlencode({"query": query, "mode": "timelinevolraw", "format": "csv",
                                     "startdatetime": START, "enddatetime": END})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(f"{API}?{params}", timeout=120) as r:
                body = r.read().decode("utf-8-sig")
            if body.startswith("Date"):
                path.write_text(body)
                return body
            print(f"  ! {name}: unexpected body {body[:120]!r}")
        except urllib.error.HTTPError as e:
            print(f"  ! {name}: HTTP {e.code}, attempt {attempt + 1}")
        time.sleep(60 * (attempt + 1))
    sys.exit(f"[BLOCKED] GDELT did not return {name}")


def monthly(body):
    """timelinevolraw CSV: Date,Series,Value rows; Series 'Article Count' and 'Total Monitored Articles'."""
    counts = collections.defaultdict(lambda: [0, 0])
    for row in csv.DictReader(io.StringIO(body)):
        month = row["Date"][:7]
        if row["Series"] == "Article Count":
            counts[month][0] += int(float(row["Value"]))
        else:
            counts[month][1] += int(float(row["Value"]))
    return counts


def main():
    CACHE.mkdir(exist_ok=True)
    OUT.mkdir(exist_ok=True)
    data = {}
    for i, (name, q) in enumerate(QUERIES.items()):
        cached = (CACHE / f"gdelt_{name}.csv").exists()
        data[name] = monthly(pull(name, q))
        print(f"  ✓ {name}: {sum(v[0] for v in data[name].values())} articles")
        if not cached and i < len(QUERIES) - 1:
            time.sleep(60)
    months = sorted(set(data["immigration"]) & set(data["taxes"]))
    rows, yearly = [], collections.defaultdict(lambda: [0] * 5)
    for m in months:
        imm, lab = data["immigration"][m][0], data["immigration_label"].get(m, [0, 0])[0]
        tax, tlab = data["taxes"][m][0], data["taxes_label"].get(m, [0, 0])[0]
        total = data["immigration"][m][1]
        rows.append([m, total, imm, lab, round(lab / imm, 4) if imm else "", tax, tlab,
                     round(tlab / tax, 4) if tax else ""])
        y = yearly[m[:4]]
        for k, v in enumerate((total, imm, lab, tax, tlab)):
            y[k] += v
    header = ["period", "total_monitored", "immigration", "immigration_label", "label_share_immigration",
              "taxes", "taxes_label", "label_share_taxes"]
    with open(OUT / "gdelt_label_share_monthly.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    with open(OUT / "gdelt_label_share_yearly.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        for yr, (total, imm, lab, tax, tlab) in sorted(yearly.items()):
            w.writerow([yr, total, imm, lab, round(lab / imm, 4), tax, tlab, round(tlab / tax, 4)])
            print(f"  {yr}: immigration {imm}, labelled {lab / imm:.3f}; taxes labelled {tlab / tax:.3f}")


if __name__ == "__main__":
    main()
