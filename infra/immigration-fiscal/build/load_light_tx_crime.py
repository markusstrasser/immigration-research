#!/usr/bin/env python3
"""INT-01 — represent the Light/He/Robey (PNAS 2020) Texas crime-by-status data.

THE gold-standard micro-comparison of criminality by legal status: Texas DPS records the
immigration status of all arrestees. Reads the openICPSR 124923 replication tables (staged
at crime_frontier/light_texas/, registration-gated — see MANUAL_ACQUIRE) into the context
warehouse, harmonized to the INT-06 status spine.

  crime_tx_arrests_by_status — year × crime_category × status_class × denom_source:
                               charge counts + crime RATE per 100k + population.

Carries BOTH undocumented-population denominators (CMS and Pew) as denom_source — never
collapse them (the result's robustness rests on the rate surviving either denominator).

WHAT THIS DOES AND DOESN'T SHOW (the DIRECTION is robust; the MAGNITUDE and GENERALIZATION are NOT):
  1. Comparison-group heterogeneity. The CMS/Pew "citizen" group = ALL citizens (native-born +
     naturalized). denom_source='CMS_nat' splits out true native_born (US-born). But even
     native-born is RACIALLY heterogeneous — it includes higher-base-rate subgroups (e.g. Black
     Americans), so a chunk of the apparent immigrant 'protective effect' is the native group's
     racial composition. A race-matched comparison (vs non-Hispanic-white native) roughly HALVES
     the violent gap (~50%→~25-30%; Cato PA994, against its own touted number). Light has no
     race-by-citizenship, so this can't be removed here — only flagged.
  2. Origin composition. The undocumented group is majority MEXICAN (esp. in Texas). If Mexicans
     are a favorably-selected low-skill subgroup, the low rate may NOT generalize to all LATAM or
     to all low-skill immigrants. The arrests can't be disaggregated by origin within status.
  3. Detection/reporting bias. Arrest data measures DETECTED crime; unreported/unsolved crime is
     missing, and reporting/detection can differ by status (direction contested — deportation-fear
     underreporting cuts both ways; over-policing can raise immigrant detection). It is a
     measured-crime comparison, not a true-offending one. (Light's convictions-vs-arrests
     robustness check partly addresses this; it does not eliminate it.)
  Bottom line: use the DIRECTION (undocumented/noncitizen NOT higher-crime than natives — robust
  across Light arrests+convictions, both denominators, and SPI incarceration). Do NOT quote the
  precise multiplier as the true protective magnitude, and do NOT generalize beyond TX-Mexican-heavy.

Run: uv run --with duckdb,pandas python load_light_tx_crime.py  (skips if not staged)
"""
from __future__ import annotations

import io
import sys
import zipfile

from paths import data_root, derived_root, duckdb_path

CAT = {1: "violent", 2: "property", 3: "drug", 4: "traffic"}

# (light_status_label, canonical status_class, charge_col, rate_col, pop_col)
GROUPS = [
    ("undocumented",    "unauthorized",         "undocumented_immigrants_charge", "illegal2_immigrants_crime_rate", "pop_undoc"),
    ("legal_immigrant", "lpr_legal_noncitizen", "immigrants_charge",              "immigrant_crime_rate",           "tot_legal2_immi"),
    ("citizen",         "native_born",          "citizen_charge",                 "citizen_crime_rate",             "tot_citizen"),
]


def _read(dirpath, name, pd):
    f = dirpath / name
    if f.exists():
        return pd.read_stata(f, convert_categoricals=False)
    z = dirpath / "124923-V1.zip"
    if z.exists():
        with zipfile.ZipFile(z) as zf:
            if name in zf.namelist():
                with zf.open(name) as fh:
                    return pd.read_stata(io.BytesIO(fh.read()), convert_categoricals=False)
    return None


def _melt(df, denom):
    rows = []
    for _, r in df.iterrows():
        cat = CAT.get(int(r["category"])) if r.get("category") == r.get("category") else None
        if cat is None:
            continue
        for lbl, sc, cc, rc, pc in GROUPS:
            rows.append({
                "year": int(r["year"]), "crime_category": cat,
                "light_status": lbl, "status_class": sc, "denom_source": denom,
                "charge_count": float(r[cc]) if cc in r and r[cc] == r[cc] else None,
                "crime_rate_per_100k": float(r[rc]) if rc in r and r[rc] == r[rc] else None,
                "population": float(r[pc]) if pc in r and r[pc] == r[pc] else None,
            })
    return rows


def _melt_nat(df):
    """big_category_nat splits citizens into naturalized (foreign-born) vs NATIVE-BORN
    (= all-citizen minus naturalized). Lets the comparison group be true native-born, not
    'all citizens incl. naturalized'. denom_source='CMS_nat'."""
    rows = []
    direct = [
        ("undocumented",    "unauthorized",         "undocumented_immigrants_charge", "illegal2_immigrants_crime_rate", "pop_undoc"),
        ("legal_immigrant", "lpr_legal_noncitizen", "immigrants_charge",              "immigrant_crime_rate",           "tot_legal2_immi"),
        ("naturalized",     "naturalized",          "naturalized_charge",             "naturalized_citizen_rate",       "naturalized_citizen"),
    ]
    for _, r in df.iterrows():
        cat = CAT.get(int(r["category"])) if r.get("category") == r.get("category") else None
        if cat is None:
            continue
        for lbl, sc, cc, rc, pc in direct:
            rows.append({"year": int(r["year"]), "crime_category": cat, "light_status": lbl,
                         "status_class": sc, "denom_source": "CMS_nat",
                         "charge_count": float(r[cc]), "crime_rate_per_100k": float(r[rc]),
                         "population": float(r[pc])})
        nb_charge = r["citizen_charge"] - r["naturalized_charge"]
        nb_pop = r["tot_citizen"] - r["naturalized_citizen"]
        rows.append({"year": int(r["year"]), "crime_category": cat, "light_status": "native_born",
                     "status_class": "native_born", "denom_source": "CMS_nat",
                     "charge_count": float(nb_charge), "crime_rate_per_100k": float(nb_charge / nb_pop * 1e5) if nb_pop else None,
                     "population": float(nb_pop)})
    return rows


def build() -> None:
    try:
        import duckdb
        import pandas as pd
    except ImportError:
        sys.exit("need duckdb+pandas — uv run --with duckdb,pandas python load_light_tx_crime.py")

    d = data_root() / "external" / "crime_frontier" / "light_texas"
    cms = _read(d, "big_category.dta", pd)
    if cms is None:
        print(f"  ! Light TX data not staged at {d} (openICPSR 124923, gated — see MANUAL_ACQUIRE); skipping")
        return
    pew = _read(d, "big_category_pew.dta", pd)
    nat = _read(d, "big_category_nat.dta", pd)

    rows = _melt(cms, "CMS")
    if pew is not None:
        rows += _melt(pew, "Pew")
    if nat is not None:
        rows += _melt_nat(nat)  # adds true native_born (US-born) + naturalized split, denom CMS_nat
    df = pd.DataFrame(rows).dropna(subset=["crime_rate_per_100k"])

    db = duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build context first")
    con = duckdb.connect(str(db))
    con.register("_l", df)
    con.execute("CREATE OR REPLACE TABLE crime_tx_arrests_by_status AS SELECT * FROM _l")
    out = derived_root() / "crime"
    out.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY crime_tx_arrests_by_status TO '{out / 'tx_arrests_by_status.csv'}' (HEADER)")

    n = con.execute("SELECT count(*) FROM crime_tx_arrests_by_status").fetchone()[0]
    yrs = con.execute("SELECT min(year), max(year) FROM crime_tx_arrests_by_status").fetchone()
    # headline ratio: undocumented vs native-born (citizen) violent-crime rate, CMS denom, latest year
    head = con.execute("""
        SELECT year,
               max(CASE WHEN status_class='unauthorized' THEN crime_rate_per_100k END) AS undoc_rate,
               max(CASE WHEN status_class='native_born'  THEN crime_rate_per_100k END) AS citizen_rate
        FROM crime_tx_arrests_by_status
        WHERE crime_category='violent' AND denom_source='CMS'
        GROUP BY year ORDER BY year DESC LIMIT 1""").fetchone()
    con.close()

    print(f"  ✓ crime_tx_arrests_by_status: {n} rows ({yrs[0]}–{yrs[1]}, 4 categories × {{undoc,legal,citizen}} × {{CMS,Pew}})")
    if head:
        y, ur, cr = head
        print(f"  headline ({y} violent, CMS denom): undocumented {ur:.0f}/100k vs citizen {cr:.0f}/100k "
              f"→ undocumented rate is {ur/cr:.2f}× the citizen rate")


if __name__ == "__main__":
    build()
