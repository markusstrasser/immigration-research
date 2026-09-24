"""Arm 4, task 5: jail systems that publish their population by Hispanic origin, against adult parity.

Sources (raw pulls cached in _cache/jail/, re-used when present):
  Connecticut DOC, "Accused Pretrial Inmates in Correctional Facilities" (data.ct.gov b674-jy6w): daily
    snapshot, RACE carries HISPANIC as a category (one combined item, like the BJS jail form).
  Delaware DOC, offender population by month (data.delaware.gov vnau-c4rn): separate ETHNICITY field;
    rows with type_of_institution = Prison and sentence_type = Detentioner (pretrial, held in DOC prisons).
  Colorado, "Summary of County Jail Data Pursuant to House Bill 19-1297" (Sept 2020): statewide county
    jail snapshot shares; parsed from the saved text with page gates.
  New York City DOC, "Daily Inmates In Custody" (data.cityofnewyork.us 7479-ugqb): race code only.
CT and DE run unified state systems, so they are outside the BJS jail surveys; Colorado's county jails are
inside them (Census of Jails 2019 Table 7 gives Colorado 23.7%). Adult (18+) Hispanic shares come from
derived/jail_acs_adults.csv (jail_acs_gq.py). State arrest shares by ethnicity are not in the repo.

Output: derived/jail_jurisdictions.csv.

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/jail_jurisdictions.py
"""
import json, pathlib, re, subprocess, sys, urllib.parse

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache/jail"
DERIVED = HERE / "derived"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
CT = "https://data.ct.gov/resource/b674-jy6w.json"
DE = "https://data.delaware.gov/resource/vnau-c4rn.json"
NYC = "https://data.cityofnewyork.us/resource/7479-ugqb.json"
NYC_META = "https://data.cityofnewyork.us/api/views/7479-ugqb.json"
CO_PDF = "https://cdpsdocs.state.co.us/ORS/Docs/Reports/2020_HB19-1297_Jail_Data_Rpt.pdf"
# expected counts, checked against every pull (content, not status)
CT_EXPECT = {"2019-06-28": (894, 3261), "2023-06-30": (1008, 3485), "2024-06-28": (1140, 3709)}
DE_EXPECT = {2019: (52, 809), 2023: (95, 1163), 2024: (99, 1077)}


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def socrata(url: str, params: dict, out: pathlib.Path):
    if out.exists():
        return json.loads(out.read_text())
    q = url + ("?" + urllib.parse.urlencode(params, safe="$(),'*") if params else "")
    r = subprocess.run(["curl", "-sS", "--fail", "--max-time", "120", "-A", UA, q], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"curl rc={r.returncode}: {r.stderr[:300]}")
    data = json.loads(r.stdout)
    out.write_text(json.dumps(data))
    return data


def adult_share(ad: pd.DataFrame, product: str, year: int, geo: str) -> float:
    r = ad[(ad["product"] == product) & (ad.year == year) & (ad.geo == geo)]
    if len(r) != 1:
        raise RuntimeError(f"adult share {product} {year} {geo}: {len(r)} rows")
    return float(r.adult_hisp_share.iloc[0])


def main() -> None:
    ad = pd.read_csv(DERIVED / "jail_acs_adults.csv", dtype={"geo": str})
    rows = []
    print("[Connecticut DOC accused pretrial inmates, RACE includes HISPANIC]")
    for d, (acs_p, acs_y) in {"2019-06-28": ("acs5", 2019), "2023-06-30": ("acs1", 2023), "2024-06-28": ("acs1", 2024)}.items():
        data = socrata(CT, {"$select": "race,count(*)", "$where": f"download_date='{d}T00:00:00.000'", "$group": "race"},
                       CACHE / f"ct_pretrial_race_{d}.json")
        c = {r["race"]: int(r["count"]) for r in data}
        h, n = c.get("HISPANIC", 0), sum(c.values())
        gate(f"CT {d}", (h, n) == CT_EXPECT[d], f"Hispanic {h:,} of {n:,} ({h / n:.4f}); categories {sorted(c)}")
        a = adult_share(ad, acs_p, acs_y, "09")
        rows.append({"jurisdiction": "Connecticut (unified DOC)", "population": "accused pretrial inmates, daily snapshot",
                     "date": d, "hispanic": h, "total": n, "jail_H_share": h / n, "adult_H_share": a,
                     "adult_source": f"ACS {acs_p} {acs_y} B01001/B01001I 18+", "ratio_to_adult": h / n / a,
                     "bjs_jail_comparator": "", "recording": "one combined race item with HISPANIC as a category",
                     "source": f"{CT} ($where download_date='{d}', $group race)"})
    print("[Delaware DOC detentioners in prisons, separate ETHNICITY field]")
    for y, (acs_p, acs_y) in {2019: ("acs5", 2019), 2023: ("acs1", 2023), 2024: ("acs1", 2024)}.items():
        data = socrata(DE, {"$select": "ethnicity,race,sum(offender_count)",
                            "$where": f"year='{y}' AND month='06 - Jun' AND type_of_institution='Prison' "
                                      "AND sentence_type='Detentioner'", "$group": "ethnicity,race", "$limit": "100"},
                       CACHE / f"de_detention_{y}.json")
        eth = {}
        for r in data:
            eth[r["ethnicity"]] = eth.get(r["ethnicity"], 0) + int(float(r["sum_offender_count"]))
        h, n = eth.get("Hispanic", 0), sum(eth.values())
        gate(f"DE June {y}", (h, n) == DE_EXPECT[y] and set(eth) == {"Hispanic", "Non - Hispanic"},
             f"Hispanic {h:,} of {n:,} ({h / n:.4f})")
        a = adult_share(ad, acs_p, acs_y, "10")
        rows.append({"jurisdiction": "Delaware (unified DOC)", "population": "detentioners held in DOC prisons, monthly",
                     "date": f"{y}-06", "hispanic": h, "total": n, "jail_H_share": h / n, "adult_H_share": a,
                     "adult_source": f"ACS {acs_p} {acs_y} B01001/B01001I 18+", "ratio_to_adult": h / n / a,
                     "bjs_jail_comparator": "", "recording": "separate ethnicity field",
                     "source": f"{DE} (year {y}, month 06, Prison, Detentioner)"})
    print("[Colorado county jails, HB19-1297 report, Sept 2020]")
    txt = (CACHE / "co_hb1297_2020_report.txt").read_text()
    pages = txt.split("\f")
    pg = lambda pat: next(i + 1 for i, p in enumerate(pages) if re.search(pat, p))
    m_snap = re.search(r"percent of Hispanics also increased from (\d+)% on January 1 to (\d+)% on July 1", txt)
    m_n = re.search(r"number of inmates.*?declined by 28% \(([\d,]+) to ([\d,]+)\).*?15% \(([\d,]+) to ([\d,]+)\)", txt, re.S)
    m_ad = re.search(r"Hispanics comprise (\d+)%", txt)
    m_adp = re.search(r"Hispanics increased from (\d+)% to (\d+)%\.", txt)
    caveat = "Many agencies did not provide this break out" in txt
    gate("CO report passages", bool(m_snap and m_n and m_ad and m_adp and caveat)
         and (m_snap.groups(), m_ad.group(1), m_adp.groups()) == (("22", "31"), "22", ("17", "19"))
         and (m_n.group(1), m_n.group(4)) == ("11,698", "7,196"),
         f"snapshot 22%→31% p. {pg(m_snap.re.pattern)}, 18+ 22% p. {pg(r'Hispanics comprise')}, "
         f"ADP 17%→19% p. {pg(r'Hispanics increased from 17%')}, caveat p. {pg('Many agencies did not provide')}")
    a19 = adult_share(ad, "acs5", 2019, "08")
    for date, share, n in (("2020-01-01", 0.22, 11_698), ("2020-07-01", 0.31, 7_196)):
        rows.append({"jurisdiction": "Colorado (county jails, statewide)", "population": "inmates on day 1 of quarter",
                     "date": date, "hispanic": "", "total": n, "jail_H_share": share, "adult_H_share": a19,
                     "adult_source": "ACS acs5 2019 B01001/B01001I 18+ (report's own 2020 SDO forecast: 22%, p. 12 Table 3)",
                     "ratio_to_adult": share / a19, "bjs_jail_comparator": "COJ 2019 Table 7 Colorado 23.7%",
                     "recording": "counties report totals and a gender/race/ethnicity breakout; many omitted the breakout, "
                                  "so shares of the total are lower bounds [INFERENCE from p. 5]",
                     "source": f"{CO_PDF} p. 17 (Figure 11 text); p. 5 caveat; total 11,698 / 7,196 p. 17"})
    print("[New York City DOC daily inmates in custody]")
    meta = socrata(NYC_META, {}, CACHE / "nyc_doc_meta.json")
    race_col = [c for c in meta["columns"] if c["fieldName"] == "race"]
    cols = sorted(c["fieldName"] for c in meta["columns"])
    counts = socrata(NYC, {"$select": "race,count(*)", "$group": "race"}, CACHE / "nyc_doc_race_counts.json")
    rc = {r.get("race", "(null)"): int(r["count"]) for r in counts}
    n = sum(rc.values())
    gate("NYC DOC has no ethnicity field", not any("ethnic" in c or "hisp" in c for c in cols) and len(race_col) == 1,
         f"columns {cols}; race description: {race_col[0].get('description', '')[:160]!r}")
    gate("NYC DOC race codes", n > 3000 and "O" in rc, ", ".join(f"{k} {v:,}" for k, v in sorted(rc.items(), key=lambda kv: -kv[1])))
    rows.append({"jurisdiction": "New York City DOC", "population": "daily inmates in custody (snapshot at pull)",
                 "date": pd.to_datetime(meta.get("rowsUpdatedAt", 0), unit="s").strftime("%Y-%m-%d"),
                 "hispanic": rc.get("H", 0), "total": n, "jail_H_share": rc.get("H", 0) / n, "adult_H_share": "",
                 "adult_source": "", "ratio_to_adult": "", "bjs_jail_comparator": "",
                 "recording": f"race code only, no ethnicity field; 'O' {rc.get('O', 0) / n:.3f} of the file; "
                              "Hispanic origin not identifiable [the 'H' share is not a Hispanic share]",
                 "source": f"{NYC} ($group race); {NYC_META}"})
    out = pd.DataFrame(rows)
    DERIVED.mkdir(exist_ok=True)
    out.to_csv(DERIVED / "jail_jurisdictions.csv", index=False, lineterminator="\n", float_format="%.4f")
    print(out[["jurisdiction", "date", "hispanic", "total", "jail_H_share", "adult_H_share", "ratio_to_adult"]].to_string(index=False))
    print(f"\nwrote derived/jail_jurisdictions.csv ({len(out)} rows)")


if __name__ == "__main__":
    main()
