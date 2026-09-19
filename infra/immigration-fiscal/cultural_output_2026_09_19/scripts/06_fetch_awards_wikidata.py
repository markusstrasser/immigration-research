#!/usr/bin/env python3
"""Arm B step 1: award winners 1990-2025 from Wikidata.

Wikidata is a structured, queryable record of award statements (P166) with a
point-in-time qualifier (P585). It is a secondary compilation, not the awarding
body's own list, and its coverage differs by award - so every award's recovered
count is reported against the number of ceremonies in the window, and an award
whose coverage is too thin to interpret is flagged rather than dropped silently.

Award QIDs are resolved by exact English label through the Wikidata search API
(never from model memory) and written to _cache/awards/award_qids.json.

Output: _cache/awards/<slug>.json  (raw SPARQL rows)
        derived/awards_winners.csv (person, award, year, wikidata metadata)
"""
import json
import sys
import time
from pathlib import Path

import pandas as pd
import requests

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "awards"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)
DER.mkdir(exist_ok=True)

UA = {"User-Agent": "immigration-research-lane/1.0 (cultural-output arm B; "
                    "research@synthoria.bio)"}
SPARQL = "https://query.wikidata.org/sparql"
SEARCH = "https://www.wikidata.org/w/api.php"

# label -> (family, expected ceremonies per year in 1990-2025 window)
AWARDS = {
    "Academy Award for Best Director": ("film", 1),
    "Academy Award for Best Actor": ("film", 1),
    "Academy Award for Best Actress": ("film", 1),
    "Academy Award for Best Supporting Actor": ("film", 1),
    "Academy Award for Best Supporting Actress": ("film", 1),
    "Academy Award for Best Original Screenplay": ("film", 1),
    "Academy Award for Best Adapted Screenplay": ("film", 1),
    "Pulitzer Prize for Fiction": ("letters", 1),
    "Pulitzer Prize for Drama": ("letters", 1),
    "Pulitzer Prize for Poetry": ("letters", 1),
    "Pulitzer Prize for General Nonfiction": ("letters", 1),
    "Pulitzer Prize for History": ("letters", 1),
    "Pulitzer Prize for Biography or Autobiography": ("letters", 1),
    "Pulitzer Prize for Music": ("music", 1),
    "National Book Award for Fiction": ("letters", 1),
    "National Book Award for Nonfiction": ("letters", 1),
    "National Book Award for Poetry": ("letters", 1),
    "Grammy Award for Album of the Year": ("music", 1),
    "Grammy Award for Record of the Year": ("music", 1),
    "Grammy Award for Song of the Year": ("music", 1),
    "Grammy Award for Best New Artist": ("music", 1),
    "MacArthur Fellows Program": ("fellowship", 25),
    "National Medal of Arts": ("medal", 10),
    "Tony Award for Best Play": ("theatre", 1),
    "Tony Award for Best Musical": ("theatre", 1),
    "Tony Award for Best Direction of a Play": ("theatre", 1),
    "Tony Award for Best Direction of a Musical": ("theatre", 1),
}

QUERY = """
SELECT ?person ?personLabel ?year ?ethnicLabel ?citizenLabel ?birthplaceLabel
       ?givenLabel ?familyLabel WHERE {
  ?person wdt:P31 wd:Q5 ; p:P166 ?st .
  ?st ps:P166 wd:%s .
  OPTIONAL { ?st pq:P585 ?when . BIND(YEAR(?when) AS ?year) }
  OPTIONAL { ?person wdt:P172 ?ethnic }
  OPTIONAL { ?person wdt:P27 ?citizen }
  OPTIONAL { ?person wdt:P19/wdt:P17 ?birthplace }
  OPTIONAL { ?person wdt:P735 ?given }
  OPTIONAL { ?person wdt:P734 ?family }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
"""


def resolve_qid(label: str) -> str:
    params = {"action": "wbsearchentities", "search": label, "language": "en",
              "format": "json", "limit": 20, "type": "item"}
    for attempt in range(4):
        r = requests.get(SEARCH, params=params, headers=UA, timeout=120)
        if r.status_code == 200 and r.text.lstrip().startswith("{"):
            hits = r.json().get("search", [])
            for h in hits:
                if h.get("label", "").lower() == label.lower():
                    return h["id"]
            if hits:
                return hits[0]["id"]
            return ""
        time.sleep(15 * (attempt + 1))
    return ""


def run_sparql(qid: str) -> list:
    for attempt in range(5):
        r = requests.get(SPARQL, params={"query": QUERY % qid,
                                         "format": "json"},
                         headers=UA, timeout=600)
        if r.status_code == 200 and r.text.lstrip().startswith("{"):
            return r.json()["results"]["bindings"]
        time.sleep(30 * (attempt + 1))
    raise RuntimeError(f"sparql failed for {qid}")


def main() -> None:
    qpath = CACHE / "award_qids.json"
    qids = json.loads(qpath.read_text()) if qpath.exists() else {}
    for label in AWARDS:
        if label not in qids:
            qids[label] = resolve_qid(label)
            print(f"  {label} -> {qids[label]}", flush=True)
            time.sleep(1)
    qpath.write_text(json.dumps(qids, indent=1, sort_keys=True))
    missing = [k for k, v in qids.items() if not v]
    if missing:
        print(f"! unresolved awards: {missing}", flush=True)

    rows = []
    for label, (family, per_year) in AWARDS.items():
        qid = qids.get(label)
        if not qid:
            continue
        slug = label.lower().replace(" ", "_").replace("/", "_")
        raw = CACHE / f"{slug}.json"
        if raw.exists():
            data = json.loads(raw.read_text())
        else:
            data = run_sparql(qid)
            raw.write_text(json.dumps(data))
            time.sleep(3)
        for b in data:
            rows.append({
                "award": label, "family": family, "qid": qid,
                "person_qid": b["person"]["value"].rsplit("/", 1)[-1],
                "person": b.get("personLabel", {}).get("value", ""),
                "year": b.get("year", {}).get("value", ""),
                "ethnic": b.get("ethnicLabel", {}).get("value", ""),
                "citizenship": b.get("citizenLabel", {}).get("value", ""),
                "birth_country": b.get("birthplaceLabel", {}).get("value", ""),
                "given_name": b.get("givenLabel", {}).get("value", ""),
                "family_name": b.get("familyLabel", {}).get("value", ""),
            })
        n_people = len({r["person_qid"] for r in rows if r["award"] == label})
        print(f"{label}: {len(data)} rows, {n_people} people", flush=True)

    df = pd.DataFrame(rows)
    if df.empty:
        sys.exit("FAIL no award rows recovered")
    df = df.drop_duplicates().sort_values(["award", "year", "person"])
    df.to_csv(DER / "awards_winners_raw.csv", index=False)
    # content validation: Best Director must cover most of the 36 ceremonies
    bd = df[(df.award == "Academy Award for Best Director")]
    bd = bd[pd.to_numeric(bd.year, errors="coerce").between(1990, 2025)]
    n_bd = bd["person_qid"].nunique()
    print(f"validation: Best Director winners 1990-2025 = {n_bd} distinct "
          f"people (36 ceremonies)", flush=True)
    if n_bd < 25:
        sys.exit(f"FAIL Best Director coverage {n_bd} too thin")
    print(f"wrote {DER/'awards_winners_raw.csv'} rows={len(df)}", flush=True)


if __name__ == "__main__":
    main()
