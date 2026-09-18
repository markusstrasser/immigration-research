#!/usr/bin/env python3
"""Parse every cached source into tidy CSVs under derived/.

Sources parsed
  1. BJS Criminal Victimization annual data tables (cv18..cv24), for
       - the victim x offender race/Hispanic origin matrix of violent incidents,
       - the same excluding simple assault (2018, 2019 only),
       - the offender-side marginal and the NCVS population,
  2. BJS N-DASH static file: victimisation rate and count by victim race/Hispanic
     origin and crime type, 1993-2024,
  3. BJS NCJ 250747 (2012-15 special report), transcribed from the PDF text and
     gated against it token by token.

Run:
  cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/ncvs_victim_offender_2026_09_18
  PYTHONUNBUFFERED=1 uv run --no-project --with "pandas>=2" --with "numpy>=2" python3 build.py
"""
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

FAILS: list[str] = []


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"[{name}] {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        FAILS.append(name)


def clean(s: str) -> str:
    """Strip the non-ASCII typography BJS embeds in its CSVs."""
    return "".join(ch for ch in s if ch == "\t" or 32 <= ord(ch) < 127).strip()


NUM = re.compile(r"^-?[\d,]+(?:\.\d+)?$")


def numeric_tokens(cells: list[str]) -> list[tuple[float, str]]:
    """Every cell that is a number, in order, with a flag for suppressed cells.

    BJS marks a not-applicable cell with "~"; it holds a column position and is
    emitted as NaN so that positional alignment with the estimate table survives.
    """
    out: list[tuple[float, str]] = []
    for c in cells:
        t = clean(c).replace("%", "").strip()
        if not t:
            continue
        if t == "~":
            out.append((float("nan"), "na"))
            continue
        if t.startswith("<"):
            out.append((float(t[1:]) / 2.0, "lt"))  # "<0.1" -> 0.05, flagged
            continue
        if NUM.match(t):
            out.append((float(t.replace(",", "")), ""))
    return out


def read_rows(path: Path) -> list[list[str]]:
    with path.open(newline="", encoding="utf-8", errors="replace") as f:
        return [[clean(c) for c in row] for row in csv.reader(f)]


def label_of(cell: str) -> str:
    """'White/b' -> 'White'; '"Other/a,c"' -> 'Other'."""
    return re.sub(r"/[a-z](,[a-z])*$", "", clean(cell)).strip()


# ---------------------------------------------------------------------------
# 1. The victim x offender matrices
# ---------------------------------------------------------------------------
# year -> (estimate file, se file, measure, offender columns in order,
#          expected victim rows, note)
CV_MATRIX = {
    2018: ("cv18/cv18t14.csv", "cv18/cv18at19.csv", "percent",
           ["White", "Black", "Hispanic", "Asian", "Other", "MultipleVarious"],
           ["White", "Black", "Hispanic", "Asian"], "violent"),
    2019: ("cv19/cv19t15.csv", "cv19/cv19at18.csv", "count",
           ["White", "Black", "Hispanic", "Other"],
           ["White", "Black", "Hispanic"], "violent"),
    2021: ("cv21/cv21t13.csv", "cv21/cv21at14.csv", "count",
           ["White", "Black", "Hispanic", "Other", "Unknown"],
           ["White", "Black", "Hispanic"], "violent"),
    2022: ("cv22/cv22t13.csv", "cv22/cv22at14.csv", "count",
           ["White", "Black", "Hispanic", "Other", "Unknown"],
           ["White", "Black", "Hispanic", "Other"], "violent"),
    2023: ("cv23/cv23t13.csv", "cv23/cv23at14.csv", "count",
           ["White", "Black", "Hispanic", "Other", "Unknown"],
           ["White", "Black", "Hispanic", "Other"], "violent"),
    2024: ("cv24/cv24t13.csv", "cv24/cv24at14.csv", "count",
           ["White", "Black", "Hispanic", "Other", "Unknown"],
           ["White", "Black", "Hispanic", "Other"], "violent"),
}

# Violent incidents EXCLUDING simple assault (serious violent), same shape.
CV_MATRIX_SERIOUS = {
    2018: ("cv18/cv18st14a.csv", "cv18/cv18stat19a.csv", "percent",
           ["White", "Black", "Hispanic", "Other"],
           ["White", "Black", "Hispanic"], "violent_excl_simple"),
    2019: ("cv19/cv19t28.csv", "cv19/cv19at31.csv", "count",
           ["White", "Black", "Hispanic", "Other"],
           ["White", "Black", "Hispanic"], "violent_excl_simple"),
}


def parse_matrix(spec: dict) -> pd.DataFrame:
    rows = []
    for year, (est_f, se_f, measure, off_cols, vic_rows, scope) in spec.items():
        est = read_rows(CACHE / est_f)
        se = read_rows(CACHE / se_f)

        def body(tab: list[list[str]]) -> dict[str, list[tuple[float, str]]]:
            out: dict[str, list[tuple[float, str]]] = {}
            started = False
            for r in tab:
                if not r:
                    continue
                head = clean(r[0])
                if head.lower().startswith("victim race"):
                    started = True
                    continue
                if not started:
                    continue
                lab = label_of(head)
                if lab in vic_rows:
                    out[lab] = numeric_tokens(r[1:])
                elif lab and not lab.startswith(("Note", "~", "!", "*", "Source", "Difference")):
                    continue
            return out

        eb, sb = body(est), body(se)
        gate(
            f"matrix_rows_{scope}_{year}",
            set(eb) == set(vic_rows) and set(sb) == set(vic_rows),
            f"est rows {sorted(eb)}, se rows {sorted(sb)}",
        )
        for v in vic_rows:
            e, s = eb[v], sb[v]
            # estimate row: [total, then one per offender column]; percent tables
            # additionally carry a literal "100" total column.
            n = len(off_cols)
            if measure == "percent":
                # total column is the incident NUMBER, then "100", then n percents
                gate(f"matrix_tokencount_{scope}_{year}_{v}", len(e) == n + 2,
                     f"{len(e)} numeric cells, expected {n + 2}")
                total, cells = e[0][0], e[2:]
            else:
                gate(f"matrix_tokencount_{scope}_{year}_{v}", len(e) == n + 1,
                     f"{len(e)} numeric cells, expected {n + 1}")
                total, cells = e[0][0], e[1:]
            gate(f"matrix_setokencount_{scope}_{year}_{v}", len(s) == n + 1,
                 f"{len(s)} SE cells, expected {n + 1}")
            se_cells = s[1:]
            for j, o in enumerate(off_cols):
                rows.append(
                    {
                        "year": year,
                        "scope": scope,
                        "measure": measure,
                        "victim": v,
                        "offender": o,
                        "row_total": total,
                        "row_total_se": s[0][0],
                        "value": cells[j][0],
                        "value_se": se_cells[j][0],
                        "flag": cells[j][1],
                    }
                )
    return pd.DataFrame(rows)


# ---------------------------------------------------------------------------
# 2. Offender marginal + population (table 11 / table 12 / table 13 family)
# ---------------------------------------------------------------------------
# year -> (file, [(row label in file, canonical group)])
CV_T11 = {
    2021: "cv21/cv21t11.csv",
    2022: "cv22/cv22t11.csv",
    2023: "cv23/cv23t11.csv",
    2024: "cv24/cv24t11.csv",
}
GROUP_MAP = {
    "White": "White",
    "Black": "Black",
    "Hispanic": "Hispanic",
    "Asian/Native Hawaiian/Other Pacific Islander": "Asian",
    "Other": "Other",
    "Multiple offenders of various races": "MultipleVarious",
}


def parse_t11() -> pd.DataFrame:
    rows = []
    for year, f in CV_T11.items():
        tab = read_rows(CACHE / f)
        in_race = False
        for r in tab:
            if not r:
                continue
            c0, c1 = clean(r[0]), clean(r[1]) if len(r) > 1 else ""
            if c0.lower().startswith("race/hispanic origin"):
                in_race = True
                continue
            if in_race and c0.lower().startswith("age"):
                break
            if not in_race:
                continue
            lab = label_of(c1)
            g = GROUP_MAP.get(lab)
            if g is None:
                continue
            tok = numeric_tokens(r[2:])
            # population, victim incidents, offender incidents, then percents
            if lab == "Multiple offenders of various races":
                # "~" occupies the population and victim columns, so the offender count
                # is the third positional token, not the first numeric one.
                gate(f"t11_tokens_{year}_{g}", len(tok) >= 3, f"{len(tok)} numeric cells")
                rows.append({"year": year, "group": g, "population": float("nan"),
                             "victim_incidents": float("nan"),
                             "offender_incidents": tok[2][0]})
            else:
                gate(f"t11_tokens_{year}_{g}", len(tok) >= 3, f"{len(tok)} numeric cells")
                rows.append({"year": year, "group": g, "population": tok[0][0],
                             "victim_incidents": tok[1][0],
                             "offender_incidents": tok[2][0]})
    return pd.DataFrame(rows)


# Population of persons age 12 or older, by race/Hispanic origin.
POP_FILES = {
    "cv18/cv18at26.csv": [2014, 2015, 2016, 2017, 2018],
    "cv19/cv19at34.csv": [2015, 2016, 2017, 2018, 2019],
    "cv21/cv21at19.csv": [2017, 2018, 2019, 2020, 2021],
    "cv24/cv24at19.csv": [2020, 2021, 2022, 2023, 2024],
}


def parse_population() -> pd.DataFrame:
    rows = []
    for f, years in POP_FILES.items():
        tab = read_rows(CACHE / f)
        in_race = False
        for r in tab:
            if not r:
                continue
            c0 = clean(r[0])
            c1 = clean(r[1]) if len(r) > 1 else ""
            if c0.lower().startswith("race/hispanic origin") or c0.lower().startswith("race"):
                in_race = True
                continue
            if in_race and c0 and not c0.lower().startswith("race"):
                break
            if not in_race:
                continue
            g = GROUP_MAP.get(label_of(c1))
            if g is None:
                continue
            tok = numeric_tokens(r[2:])
            if len(tok) != len(years):
                gate(f"pop_tokens_{Path(f).stem}_{g}", False,
                     f"{len(tok)} values for {len(years)} years")
                continue
            for y, (v, _) in zip(years, tok):
                rows.append({"source": Path(f).name, "year": y, "group": g, "population": v})
    df = pd.DataFrame(rows)
    # Consistency check across the overlapping vintages.
    # White / Black / Hispanic are defined identically in every vintage and must agree
    # exactly.  Asian and Other are NOT: CV2018 carries "Asian" while CV2021 onward carries
    # "Asian/Native Hawaiian/Other Pacific Islander", moving NHOPI out of Other.
    core = df[df.group.isin(["White", "Black", "Hispanic"])]
    piv = core.pivot_table(index=["year", "group"], columns="source", values="population")
    ov = piv.dropna(thresh=2)
    if len(ov):
        rel = (ov.max(axis=1) - ov.min(axis=1)) / ov.min(axis=1)
        gate("pop_vintage_agreement_core", rel.max() < 1e-9,
             f"max relative spread across vintages {rel.max():.2e} on {len(ov)} "
             "overlapping White/Black/Hispanic cells")
    noncore = df[df.group.isin(["Asian", "Other"])]
    pv2 = noncore.pivot_table(index=["year", "group"], columns="source", values="population")
    ov2 = pv2.dropna(thresh=2)
    rel2 = ((ov2.max(axis=1) - ov2.min(axis=1)) / ov2.min(axis=1)).max() if len(ov2) else 0.0
    print(f"[note] Asian/Other population differs across vintages by up to {rel2:.1%} "
          "(NHOPI category change); those groups are not used in the headline.")
    # Prefer the latest vintage for each year.
    order = {"cv18at26.csv": 0, "cv19at34.csv": 1, "cv21at19.csv": 2, "cv24at19.csv": 3}
    df["rank"] = df["source"].map(order)
    df = df.sort_values("rank").groupby(["year", "group"], as_index=False).last()
    return df[["year", "group", "population", "source"]]


# ---------------------------------------------------------------------------
# 3. N-DASH: rate and count by victim race/Hispanic origin and crime type
# ---------------------------------------------------------------------------
def parse_ndash() -> pd.DataFrame:
    d = pd.read_csv(CACHE / "nd_person_race_all.csv")
    d.columns = [c.strip().lstrip("﻿") for c in d.columns]
    keep = [
        "year", "crimeType", "levelDesc1", "rate", "rateSE", "rateLB", "rateUB",
        "count", "countSE", "countLB", "countUB", "sampleSizeUnwt",
        "countFlag", "rateFlag",
    ]
    d = d[keep].rename(columns={"levelDesc1": "victim_race"})
    gate("ndash_groups", set(d.victim_race.unique()) == {"White", "Black", "Hispanic", "Other"},
         f"{sorted(d.victim_race.unique())}")
    gate("ndash_years", d.year.min() == 1993 and d.year.max() == 2024,
         f"{d.year.min()}-{d.year.max()}, {len(d)} rows")
    return d.sort_values(["year", "crimeType", "victim_race"])


# ---------------------------------------------------------------------------
# 4. BJS NCJ 250747, 2012-15.  Transcribed from the PDF and gated against it.
# ---------------------------------------------------------------------------
# Table 1: percent of violent victimisations by victim (row) and offender (col).
RHOVO_T1 = {
    #  victim: (avg annual number, White, Black, Hispanic, Other, TwoPlus, MixedGroup, Unknown)
    "Total":   (5833800, 43.8, 22.7, 14.4, 2.2, 6.0, 2.8, 8.0),
    "White":   (3679410, 56.6, 14.7, 11.0, 1.7, 6.1, 2.1, 7.9),
    "Black":   (850720, 10.9, 63.2, 6.6, 0.5, 7.4, 4.0, 7.4),
    "Hispanic": (846520, 20.0, 20.5, 40.3, 2.5, 5.7, 3.3, 7.8),
    "Other":   (198320, 29.6, 18.9, 9.7, 17.5, 3.6, 6.1, 14.5),
}
# Table 2: offender race, total / single-offender / multiple-offender victimisations.
RHOVO_T2 = {
    "Total":    (5833800, 100.0, 4490640, 100.0, 1150090, 100.0),
    "White":    (2557910, 43.8, 2208850, 49.2, 349060, 30.4),
    "Black":    (1324270, 22.7, 1039920, 23.2, 284340, 24.7),
    "Hispanic": (841500, 14.4, 563060, 12.5, 278450, 24.2),
    "Other":    (127070, 2.2, 120730, 2.7, 6340, 0.6),
}
# Table 3: rate per 1,000 by victim/offender pair and crime type.
RHOVO_T3 = {
    ("White", "White"): (12.0, 3.7, 8.4),
    ("White", "Black"): (3.1, 1.2, 1.9),
    ("White", "Hispanic"): (2.4, 0.9, 1.4),
    ("Black", "White"): (2.8, 0.8, 2.0),
    ("Black", "Black"): (16.5, 6.7, 9.8),
    ("Black", "Hispanic"): (1.7, 0.5, 1.2),
    ("Hispanic", "White"): (4.1, 1.4, 2.7),
    ("Hispanic", "Black"): (4.2, 2.1, 2.1),
    ("Hispanic", "Hispanic"): (8.3, 3.2, 5.1),
}
# Table 6: percent of violent victimisations reported to police, by pair.
RHOVO_T6 = {
    ("White", "White"): (2081520, 45.9),
    ("White", "Black"): (540350, 47.2),
    ("White", "Hispanic"): (406450, 45.1),
    ("Black", "White"): (92810, 57.4),
    ("Black", "Black"): (537470, 51.7),
    ("Black", "Hispanic"): (55790, 47.0),
    ("Hispanic", "White"): (169040, 42.6),
    ("Hispanic", "Black"): (173120, 55.0),
    ("Hispanic", "Hispanic"): (341420, 48.2),
}
# Table 8: percent of violent victimisations involving victim injury, by pair.
RHOVO_T8 = {
    ("White", "White"): (2081520, 27.0),
    ("White", "Black"): (540360, 20.9),
    ("White", "Hispanic"): (406450, 30.7),
    ("Black", "White"): (92810, 11.4),
    ("Black", "Black"): (537470, 32.7),
    ("Black", "Hispanic"): (55790, 23.4),
    ("Hispanic", "White"): (169040, 26.2),
    ("Hispanic", "Black"): (173120, 26.3),
    ("Hispanic", "Hispanic"): (341420, 24.7),
}


def rhovo_text() -> str:
    txt = CACHE / "rhovo1215.txt"
    if not txt.exists():
        subprocess.run(
            ["pdftotext", "-layout", str(CACHE / "rhovo1215.pdf"), str(txt)], check=True
        )
    return txt.read_text(errors="replace")


def gate_rhovo(text: str) -> None:
    """Every transcribed number must appear verbatim in the extracted PDF text."""
    missing: list[str] = []
    checked = 0
    def token(v: float) -> str:
        if float(v).is_integer():
            return f"{int(v):,}" if abs(v) >= 1000 else f"{int(v)}"
        return f"{v}"
    for tab, vals in (
        ("T1", [x for row in RHOVO_T1.values() for x in row]),
        ("T2", [x for row in RHOVO_T2.values() for x in row]),
        ("T3", [x for row in RHOVO_T3.values() for x in row]),
        ("T6", [x for row in RHOVO_T6.values() for x in row]),
        ("T8", [x for row in RHOVO_T8.values() for x in row]),
    ):
        for v in vals:
            t = token(v)
            checked += 1
            if t not in text:
                missing.append(f"{tab}:{t}")
    gate("rhovo_transcription", not missing,
         f"{checked} transcribed values, {len(missing)} not found in the PDF text"
         + (f": {missing[:8]}" if missing else ""))


def write_rhovo() -> None:
    with (DERIVED / "rhovo_t1_victim_offender_percent.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["victim", "avg_annual_number", "White", "Black", "Hispanic",
                    "Other", "TwoOrMoreRaces", "MixedOffenderGroup", "Unknown"])
        for k, v in RHOVO_T1.items():
            w.writerow([k, *v])
    with (DERIVED / "rhovo_t2_offender_by_offender_count.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["offender", "total_n", "total_pct", "single_n", "single_pct",
                    "multiple_n", "multiple_pct"])
        for k, v in RHOVO_T2.items():
            w.writerow([k, *v])
    with (DERIVED / "rhovo_t3_rate_by_pair_and_crime.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["victim", "offender", "rate_total_violent", "rate_serious_violent",
                    "rate_simple_assault"])
        for (v, o), r in RHOVO_T3.items():
            w.writerow([v, o, *r])
    with (DERIVED / "rhovo_t6_reported_to_police.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["victim", "offender", "avg_annual_number", "pct_reported_to_police"])
        for (v, o), r in RHOVO_T6.items():
            w.writerow([v, o, *r])
    with (DERIVED / "rhovo_t8_injury.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["victim", "offender", "avg_annual_number", "pct_injured"])
        for (v, o), r in RHOVO_T8.items():
            w.writerow([v, o, *r])


def main() -> None:
    m = parse_matrix(CV_MATRIX)
    m.to_csv(DERIVED / "cv_matrix_violent.csv", index=False)
    print(f"[out] cv_matrix_violent.csv ({len(m)} rows)")

    ms = parse_matrix(CV_MATRIX_SERIOUS)
    ms.to_csv(DERIVED / "cv_matrix_violent_excl_simple.csv", index=False)
    print(f"[out] cv_matrix_violent_excl_simple.csv ({len(ms)} rows)")

    t11 = parse_t11()
    t11.to_csv(DERIVED / "cv_offender_marginal.csv", index=False)
    print(f"[out] cv_offender_marginal.csv ({len(t11)} rows)")

    pop = parse_population()
    pop.to_csv(DERIVED / "cv_population_12plus.csv", index=False)
    print(f"[out] cv_population_12plus.csv ({len(pop)} rows)")

    nd = parse_ndash()
    nd.to_csv(DERIVED / "ndash_rate_by_victim_race.csv", index=False)
    print(f"[out] ndash_rate_by_victim_race.csv ({len(nd)} rows)")

    gate_rhovo(rhovo_text())
    write_rhovo()
    print("[out] rhovo_*.csv (5 files)")

    if FAILS:
        raise SystemExit("integrity gates failed: " + ", ".join(FAILS))
    print("[done] build.py")


if __name__ == "__main__":
    sys.exit(main())
