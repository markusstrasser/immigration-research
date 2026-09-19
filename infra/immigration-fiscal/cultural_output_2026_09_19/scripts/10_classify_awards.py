#!/usr/bin/env python3
"""Arm B step 3: classify award winners 1990-2025 by Hispanic / Mexican origin
and compare the share against the population benchmark.

Classification, in priority order:
  1. documented  - Wikidata ethnic group (P172) matching Hispanic/Latino/
     Chicano/Mexican, or citizenship (P27) / country of birth (P19->P17) Mexico.
  2. imputed     - Census 2010 surname file: pcthispanic >= 70 (primary),
     with 50 and 90 reported as sensitivity.
  3. unmatched   - surname absent from the Census file (<100 US bearers in
     2010, or a non-US name); counted and reported, never silently zeroed.

Foreign nationals are separated from US citizens: Mexican directors winning
Academy Awards are not members of the US resident Mexican-origin population
whose fiscal cost the repo prices, and mixing them inflates the "canon" share.

Input : derived/awards_winners_raw.csv, derived/surname_hispanic_lookup.csv,
        derived/education_benchmarks.csv
Output: derived/awards_classified.csv, derived/awards_shares.csv
"""
import re
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"

HISP_PAT = re.compile(r"hispanic|latino|latina|chicano|chicana|mexican|"
                      r"tejano|nuyorican", re.I)
MEX_PAT = re.compile(r"mexican|chicano|chicana|tejano", re.I)
SUFFIX = {"JR", "JR.", "SR", "SR.", "II", "III", "IV", "MD", "PHD"}


QID = re.compile(r"^Q\d+$")


def surname_of(row) -> str:
    """Pick one surname per person.

    Wikidata can carry several family-name statements (birth name and married
    name, for instance), which the SPARQL collapse joins with "|", and the
    label service sometimes returns a bare QID. Taking the joined string whole
    produced a surname that could never match the Census file for 4% of people,
    so: prefer the candidate that actually appears in the person's display
    name, else fall back to the last token of that name.
    """
    label = str(row.get("person") or "").strip()
    label_toks = {t.upper().strip(".,") for t in re.split(r"[\s-]+", label) if t}
    fam = str(row.get("family_name") or "").strip()
    cands = [c.strip() for c in fam.split("|") if c.strip() and not QID.match(c.strip())]
    for c in cands:
        tok = c.split()[-1].upper().strip(".,")
        if tok in label_toks:
            return tok
    if len(cands) == 1:
        return cands[0].split()[-1].upper().strip(".,")
    toks = [t for t in re.split(r"\s+", label) if t]
    while toks and toks[-1].upper().strip(".,") in SUFFIX:
        toks.pop()
    tail = toks[-1].upper().strip(".,") if toks else ""
    return "" if QID.match(tail) else tail


def main() -> None:
    raw = pd.read_csv(DER / "awards_winners_raw.csv", dtype=str)
    sn = pd.read_csv(DER / "surname_hispanic_lookup.csv")
    sn["name"] = sn["name"].str.upper()
    sn_map = dict(zip(sn["name"], sn["pcthispanic"]))

    raw["year_n"] = pd.to_numeric(raw["year"], errors="coerce")
    n_all = len(raw)
    no_year = raw["year_n"].isna().sum()
    df = raw[raw["year_n"].between(1990, 2025)].copy()

    # collapse the SPARQL cross-product to one row per person
    def agg(s):
        return "|".join(sorted({x for x in s.dropna().astype(str) if x}))

    people = df.groupby("person_qid").agg(
        person=("person", "first"),
        family_name=("family_name", agg),
        ethnic=("ethnic", agg),
        citizenship=("citizenship", agg),
        birth_country=("birth_country", agg),
    ).reset_index()
    people["surname"] = people.apply(surname_of, axis=1)
    people["pcthispanic"] = people["surname"].map(sn_map)
    people["surname_matched"] = people["pcthispanic"].notna()
    # Wikidata's English label for the country is "United States"
    people["us_citizen"] = people["citizenship"].str.contains(
        r"United States", na=False)
    people["mexico_linked"] = (
        people["citizenship"].str.contains(r"\bMexico\b", na=False)
        | people["birth_country"].str.contains(r"\bMexico\b", na=False))
    people["hisp_documented"] = (
        people["ethnic"].str.contains(HISP_PAT, na=False)
        | people["mexico_linked"])
    people["mex_documented"] = (
        people["ethnic"].str.contains(MEX_PAT, na=False)
        | people["mexico_linked"])
    for thr in (50, 70, 90):
        people[f"hisp_imputed_{thr}"] = (
            people["pcthispanic"].fillna(0) >= thr)
    people["hispanic_any"] = (people["hisp_documented"]
                              | people["hisp_imputed_70"])

    winner_years = df[["award", "family", "year_n", "person_qid"]].drop_duplicates()
    wy = winner_years.merge(people, on="person_qid", how="left")
    wy["period"] = np.where(wy["year_n"] < 2015, "1990-2014", "2015-2025")
    wy.to_csv(DER / "awards_classified.csv", index=False)

    def block(sub: pd.DataFrame, label: str, scope: str) -> dict:
        n = len(sub)
        if n == 0:
            return {}
        return {
            "scope": scope,
            "group": label,
            "winner_years": n,
            "distinct_people": sub["person_qid"].nunique(),
            "surname_unmatched_share": round(1 - sub["surname_matched"].mean(), 4),
            "hispanic_share": round(sub["hispanic_any"].mean(), 4),
            "hispanic_documented_share": round(sub["hisp_documented"].mean(), 4),
            "hispanic_imputed_only_share": round(
                (sub["hispanic_any"] & ~sub["hisp_documented"]).mean(), 4),
            "hispanic_share_thr50": round(
                (sub["hisp_documented"] | sub["hisp_imputed_50"]).mean(), 4),
            "hispanic_share_thr90": round(
                (sub["hisp_documented"] | sub["hisp_imputed_90"]).mean(), 4),
            # upper bound: if the winners whose surname is absent from the
            # Census file were Hispanic at the same rate as the matched ones
            "hispanic_share_upper_bound": round(float(
                sub.loc[sub["surname_matched"], "hispanic_any"].mean()
                if sub["surname_matched"].any() else 0.0), 4),
            "mexico_linked_share": round(sub["mexico_linked"].mean(), 4),
            "mexican_documented_share": round(sub["mex_documented"].mean(), 4),
            "us_citizen_share": round(sub["us_citizen"].mean(), 4),
        }

    out = []
    for scope, sel in (("all_winners", wy),
                       ("us_citizens_only", wy[wy["us_citizen"]])):
        out.append(block(sel, "ALL", scope))
        for per in sorted(sel["period"].dropna().unique()):
            out.append(block(sel[sel["period"] == per], f"period {per}", scope))
        for fam in sorted(sel["family"].dropna().unique()):
            out.append(block(sel[sel["family"] == fam], f"family {fam}", scope))
            for per in sorted(sel["period"].dropna().unique()):
                out.append(block(
                    sel[(sel["family"] == fam) & (sel["period"] == per)],
                    f"family {fam} {per}", scope))
        for aw in sorted(sel["award"].dropna().unique()):
            out.append(block(sel[sel["award"] == aw], f"award {aw}", scope))
    shares = pd.DataFrame([r for r in out if r])
    shares.to_csv(DER / "awards_shares.csv", index=False)

    # per-award year coverage: an award whose P585 qualifiers are largely
    # missing contributes only its dated winners and is flagged, not dropped
    cov = raw.assign(has_year=raw["year_n"].notna()).groupby("award").agg(
        rows=("award", "size"), year_coverage=("has_year", "mean")).round(3)
    cov["in_window_winner_years"] = (
        wy.groupby("award").size().reindex(cov.index).fillna(0).astype(int))
    cov.to_csv(DER / "awards_year_coverage.csv")

    bm = pd.read_csv(DER / "education_benchmarks.csv")
    print(f"rows={n_all} year-missing={no_year} in-window winner-years={len(wy)} "
          f"people={people['person_qid'].nunique()}", flush=True)
    print("\nper-award year coverage (worst 6):", flush=True)
    print(cov.sort_values("year_coverage").head(6).to_string(), flush=True)
    print(shares[shares.group.isin(["ALL", "period 1990-2014", "period 2015-2025"])]
          .to_string(index=False), flush=True)
    print("\nbenchmark (ACS): hispanic share of BA+ adults", flush=True)
    print(bm[["year", "hispanic_share_25plus", "hispanic_share_ba_plus"]]
          .to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
