#!/usr/bin/env python3
"""District cost-to-serve differential (item D) from Census F-33 x NCES CCD.

Joins the Census F-33 FY2024 district finance file (NCESID) to the NCES CCD
LEA membership-by-race file for school year 2023-24 (LEAID), computes each
district's per-pupil current spending, and asks a single question per state:
what per-pupil current spending does the average Hispanic pupil face, compared
with the average white non-Hispanic pupil and with the average pupil?

The differential is a *cost-to-serve* composition effect, not a cost of the
pupil: it says whether Hispanic pupils sit in higher- or lower-spending
districts than the state average, holding the state's own spending fixed.

Writes `derived/district_differential_by_state.csv` and adds a `district`
group to the parameter file.

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ledger_absolute_2026_09_17/district_differential.py \
      --params infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
EXTERNAL = Path.home() / "research-data/immigration-fiscal/data/external"
F33 = EXTERNAL / "census_f33_district/elsec24t.txt"
CCD = EXTERNAL / "nces_ccd/ccd_lea_052_2324_l_1a_073124.csv"

# Plausibility band on district per-pupil current spending, per the brief.
PP_MIN, PP_MAX = 3_000.0, 80_000.0
COVERAGE_TOLERANCE = 0.10

TOTAL_INDICATOR_TOTAL = "Derived - Education Unit Total minus Adult Education Count"
TOTAL_INDICATOR_RACE = ("Derived - Subtotal by Race/Ethnicity and Sex "
                        "minus Adult Education Count")
RACE_HISPANIC = "Hispanic/Latino"
RACE_WHITE = "White"

FIPS_TO_NAME = {
    1: "Alabama", 2: "Alaska", 4: "Arizona", 5: "Arkansas", 6: "California",
    8: "Colorado", 9: "Connecticut", 10: "Delaware", 11: "District of Columbia",
    12: "Florida", 13: "Georgia", 15: "Hawaii", 16: "Idaho", 17: "Illinois",
    18: "Indiana", 19: "Iowa", 20: "Kansas", 21: "Kentucky", 22: "Louisiana",
    23: "Maine", 24: "Maryland", 25: "Massachusetts", 26: "Michigan",
    27: "Minnesota", 28: "Mississippi", 29: "Missouri", 30: "Montana",
    31: "Nebraska", 32: "Nevada", 33: "New Hampshire", 34: "New Jersey",
    35: "New Mexico", 36: "New York", 37: "North Carolina", 38: "North Dakota",
    39: "Ohio", 40: "Oklahoma", 41: "Oregon", 42: "Pennsylvania",
    44: "Rhode Island", 45: "South Carolina", 46: "South Dakota",
    47: "Tennessee", 48: "Texas", 49: "Utah", 50: "Vermont", 51: "Virginia",
    53: "Washington", 54: "West Virginia", 55: "Wisconsin", 56: "Wyoming",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def read_f33() -> pd.DataFrame:
    """District per-pupil current spending. TCURSPND is in THOUSANDS."""
    d = pd.read_csv(F33, dtype={"NCESID": str, "FIPST": str},
                    usecols=["FIPST", "NAME", "SCHLEV", "NCESID", "ENROLL",
                             "TCURSPND", "TCAPOUT", "TINTRST"])
    d["LEAID"] = d.NCESID.str.strip().str.zfill(7)
    d["fips"] = pd.to_numeric(d.FIPST, errors="coerce")
    d["enroll_f33"] = pd.to_numeric(d.ENROLL, errors="coerce")
    d["current_spending"] = pd.to_numeric(d.TCURSPND, errors="coerce") * 1000.0
    d["per_pupil"] = d.current_spending / d.enroll_f33.where(d.enroll_f33 > 0)
    return d


def read_ccd() -> pd.DataFrame:
    """District membership: total, Hispanic/Latino and White, from the long file.

    STUDENT_COUNT is blank when DMS_FLAG says Missing; blank is missing, not
    zero. TOTAL_INDICATOR must be filtered or every pupil is counted many times.
    """
    cols = ["FIPST", "LEAID", "RACE_ETHNICITY", "SEX", "STUDENT_COUNT",
            "TOTAL_INDICATOR"]
    keep_total, keep_hisp, keep_white = [], [], []
    rows_read = 0
    for chunk in pd.read_csv(CCD, usecols=cols, chunksize=1_000_000,
                             dtype={"LEAID": str, "FIPST": str}):
        rows_read += len(chunk)
        ti = chunk.TOTAL_INDICATOR
        tot = chunk[ti == TOTAL_INDICATOR_TOTAL]
        if len(tot):
            keep_total.append(tot[["FIPST", "LEAID", "STUDENT_COUNT"]])
        race = chunk[ti == TOTAL_INDICATOR_RACE]
        if len(race):
            h = race[race.RACE_ETHNICITY == RACE_HISPANIC]
            w = race[race.RACE_ETHNICITY == RACE_WHITE]
            if len(h):
                keep_hisp.append(h[["LEAID", "STUDENT_COUNT"]])
            if len(w):
                keep_white.append(w[["LEAID", "STUDENT_COUNT"]])
    print(f"[ccd] {rows_read:,} rows scanned", flush=True)

    def agg(parts, label):
        d = pd.concat(parts, ignore_index=True)
        d["STUDENT_COUNT"] = pd.to_numeric(d.STUDENT_COUNT, errors="coerce")
        out = d.groupby("LEAID", as_index=False).STUDENT_COUNT.sum(min_count=1)
        out = out.rename(columns={"STUDENT_COUNT": label})
        return out

    total = agg(keep_total, "pupils_total")
    fipst = pd.concat(keep_total, ignore_index=True)[["LEAID", "FIPST"]] \
        .drop_duplicates("LEAID")
    total = total.merge(fipst, on="LEAID", how="left")
    total["LEAID"] = total.LEAID.str.strip().str.zfill(7)
    hisp = agg(keep_hisp, "pupils_hispanic")
    hisp["LEAID"] = hisp.LEAID.str.strip().str.zfill(7)
    white = agg(keep_white, "pupils_white")
    white["LEAID"] = white.LEAID.str.strip().str.zfill(7)
    d = total.merge(hisp, on="LEAID", how="left").merge(white, on="LEAID", how="left")
    return d


def build(params_path: Path) -> pd.DataFrame:
    params = json.loads(params_path.read_text())
    f33_state_pp_entry = params["k12"]["f33_per_pupil_current_spending_by_state"]
    if str(f33_state_pp_entry.get("status", "")).lower() != "verified":
        raise SystemExit("[BLOCKED] k12.f33_per_pupil_current_spending_by_state "
                         "is not verified; the coverage gate cannot be run")
    f33_state_pp = {k.strip(): float(v) for k, v in f33_state_pp_entry["value"].items()}

    print("[stage] reading the Census F-33 district finance file", flush=True)
    fin = read_f33()
    print(f"[f33] {len(fin):,} district rows", flush=True)
    print("[stage] reading the NCES CCD LEA membership file (long, 648 MB)", flush=True)
    mem = read_ccd()
    print(f"[ccd] {len(mem):,} districts with a membership total", flush=True)

    d = fin.merge(mem.drop(columns=["FIPST"]), on="LEAID", how="inner")
    joined = len(d)
    print(f"[join] {joined:,} districts matched on NCESID = LEAID", flush=True)

    d["pupils_total"] = pd.to_numeric(d.pupils_total, errors="coerce")
    d["pupils_hispanic"] = pd.to_numeric(d.pupils_hispanic, errors="coerce").fillna(0.0)
    d["pupils_white"] = pd.to_numeric(d.pupils_white, errors="coerce").fillna(0.0)

    missing_pp = d.per_pupil.isna() | d.pupils_total.isna() | (d.pupils_total <= 0)
    implausible = (~missing_pp) & ((d.per_pupil < PP_MIN) | (d.per_pupil > PP_MAX))
    drop_counts = dict(joined=joined,
                       dropped_missing=int(missing_pp.sum()),
                       dropped_implausible=int(implausible.sum()),
                       dropped_implausible_low=int((implausible & (d.per_pupil < PP_MIN)).sum()),
                       dropped_implausible_high=int((implausible & (d.per_pupil > PP_MAX)).sum()),
                       f33_rows=len(fin), ccd_districts=len(mem),
                       f33_not_in_ccd=int(len(fin) - joined))
    keep = d[~(missing_pp | implausible)].copy()
    drop_counts["kept"] = int(len(keep))
    print(f"[filter] kept {len(keep):,}; dropped {drop_counts['dropped_missing']:,} "
          f"missing and {drop_counts['dropped_implausible']:,} implausible "
          f"(<${PP_MIN:,.0f} or >${PP_MAX:,.0f} per pupil)", flush=True)

    rows = []
    for fips, name in sorted(FIPS_TO_NAME.items()):
        block = keep[keep.fips == fips]
        if not len(block):
            raise SystemExit(f"[BLOCKED] no surviving districts in {name}")
        pp = block.per_pupil.to_numpy()
        n_all = block.pupils_total.to_numpy()
        n_h = block.pupils_hispanic.to_numpy()
        n_w = block.pupils_white.to_numpy()
        mean_all = float((pp * n_all).sum() / n_all.sum())
        mean_h = float((pp * n_h).sum() / n_h.sum()) if n_h.sum() > 0 else float("nan")
        mean_w = float((pp * n_w).sum() / n_w.sum()) if n_w.sum() > 0 else float("nan")
        state_pp = f33_state_pp.get(name)
        if state_pp is None:
            raise SystemExit(f"[BLOCKED] no F-33 state summary per-pupil figure for {name}")
        ratio = mean_all / state_pp
        rows.append(dict(
            state_fips=fips, state=name, districts=int(len(block)),
            pupils_total=float(n_all.sum()), pupils_hispanic=float(n_h.sum()),
            pupils_white=float(n_w.sum()),
            hispanic_share=float(n_h.sum() / n_all.sum()),
            white_share=float(n_w.sum() / n_all.sum()),
            all_pupil_mean_per_pupil=mean_all,
            hispanic_mean_per_pupil=mean_h, white_mean_per_pupil=mean_w,
            hispanic_minus_all=mean_h - mean_all, white_minus_all=mean_w - mean_all,
            f33_state_summary_per_pupil=state_pp, coverage_ratio=ratio,
            coverage_gate_passed=bool(abs(ratio - 1.0) <= COVERAGE_TOLERANCE)))
    table = pd.DataFrame(rows)

    failed = table[~table.coverage_gate_passed]
    print("\n[gate] all-pupil weighted mean over the F-33 state summary per-pupil "
          f"figure, tolerance {COVERAGE_TOLERANCE:.0%}", flush=True)
    for _, r in table.iterrows():
        mark = "PASS" if r.coverage_gate_passed else "FAIL"
        print(f"  {mark}  {r.state:<22} {r.coverage_ratio:6.4f}  "
              f"(${r.all_pupil_mean_per_pupil:,.0f} vs "
              f"${r.f33_state_summary_per_pupil:,.0f})", flush=True)
    # A state that fails the coverage gate keeps its measured means in the CSV
    # but contributes a differential of zero, so no charge rests on a district
    # universe the gate could not confirm. Vermont and Michigan are the shape of
    # this failure: supervisory unions and intermediate districts report current
    # spending against zero enrolment, so they carry no weight in any of the
    # three means and the surviving level sits below the state summary.
    zeroed = sorted(failed.state.tolist())
    table["differential_charged"] = table.coverage_gate_passed
    table["hispanic_minus_all_charged"] = table.hispanic_minus_all.where(
        table.coverage_gate_passed, 0.0)
    table["white_minus_all_charged"] = table.white_minus_all.where(
        table.coverage_gate_passed, 0.0)
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    table.to_csv(out / "district_differential_by_state.csv", index=False)
    if zeroed:
        print(f"\n[gate] {len(zeroed)} state(s) failed the {COVERAGE_TOLERANCE:.0%} "
              f"coverage gate and are charged a differential of zero: {zeroed}", flush=True)

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    sources = [dict(path=str(F33), sha256=sha256(F33),
                    source_url="https://www2.census.gov/programs-surveys/school-finances/"
                               "tables/2024/secondary-education-finance/elsec24t.txt"),
               dict(path=str(CCD), sha256=sha256(CCD),
                    source_url="https://nces.ed.gov/ccd/Data/zip/"
                               "ccd_lea_052_2324_l_1a_073124.zip")]
    quote = ("Census F-33 elsec24t.txt columns NCESID, FIPST, ENROLL, TCURSPND "
             "(dollars in thousands; per-pupil current spending = TCURSPND*1000/ENROLL); "
             "NCES CCD ccd_lea_052_2324_l_1a_073124.csv columns LEAID, RACE_ETHNICITY, "
             "SEX, STUDENT_COUNT, TOTAL_INDICATOR, with TOTAL_INDICATOR="
             f"\"{TOTAL_INDICATOR_TOTAL}\" for district totals and "
             f"\"{TOTAL_INDICATOR_RACE}\" with RACE_ETHNICITY in "
             f"(\"{RACE_HISPANIC}\", \"{RACE_WHITE}\") summed over SEX for the race groups")
    notes = (f"DERIVED by district_differential.py from the two staged files. "
             f"{drop_counts['kept']:,} of {joined:,} joined districts kept; "
             f"{drop_counts['dropped_missing']:,} dropped for a missing per-pupil or "
             f"membership value and {drop_counts['dropped_implausible']:,} for a per-pupil "
             f"value outside ${PP_MIN:,.0f}-${PP_MAX:,.0f}. Enrolment-weighted over CCD "
             f"membership within state. CCD \"White\" is already non-Hispanic: the CCD "
             f"race/ethnicity categories are mutually exclusive and Hispanic/Latino is "
             f"its own category. A differential is a composition effect across districts, "
             f"not a per-pupil cost of the pupil. States failing the "
             f"{COVERAGE_TOLERANCE:.0%} coverage gate carry a differential of zero: "
             f"{zeroed or 'none'}.")

    def entry(value, unit):
        return dict(value=value, unit=unit,
                    fiscal_year="FY2024 finance x SY2023-24 membership",
                    source_url=sources[0]["source_url"], sources=sources,
                    quote=quote, fetched=now, status="verified", notes=notes)

    params["district"] = dict(
        hispanic_minus_all_by_state=entry(
            {r.state: round(float(r.hispanic_minus_all_charged), 4)
             for _, r in table.iterrows()}, "dollars per pupil"),
        white_minus_all_by_state=entry(
            {r.state: round(float(r.white_minus_all_charged), 4)
             for _, r in table.iterrows()}, "dollars per pupil"),
        all_pupil_mean_by_state=entry(
            {r.state: round(float(r.all_pupil_mean_per_pupil), 4) for _, r in table.iterrows()},
            "dollars per pupil"),
        coverage_ratio_by_state=entry(
            {r.state: round(float(r.coverage_ratio), 6) for _, r in table.iterrows()},
            "ratio, all-pupil weighted mean over the F-33 state summary per-pupil figure"),
    )
    params["district"]["coverage_ratio_by_state"]["notes"] += (
        f" Gate: every state within {COVERAGE_TOLERANCE:.0%} of the F-33 state summary "
        f"figure in k12.f33_per_pupil_current_spending_by_state.")
    params["_district_build"] = dict(
        counts=drop_counts, tolerance=COVERAGE_TOLERANCE,
        per_pupil_band=[PP_MIN, PP_MAX], built=now,
        min_coverage_ratio=float(table.coverage_ratio.min()),
        max_coverage_ratio=float(table.coverage_ratio.max()),
        states_failing_coverage_gate=zeroed,
        states_charged=int(table.differential_charged.sum()),
        sources=sources)
    params_path.write_text(json.dumps(params, indent=2, default=float,
                                      allow_nan=False) + "\n")
    print(f"\n[params] wrote the `district` group into {params_path}", flush=True)
    print(f"[params] coverage ratios run {table.coverage_ratio.min():.4f} to "
          f"{table.coverage_ratio.max():.4f} over 51 jurisdictions", flush=True)
    for s in ["California", "Texas", "Illinois", "Arizona"]:
        r = table[table.state == s].iloc[0]
        print(f"[{s}] hispanic-minus-all ${r.hispanic_minus_all:+,.0f}, "
              f"white-minus-all ${r.white_minus_all:+,.0f}, "
              f"all-pupil mean ${r.all_pupil_mean_per_pupil:,.0f}", flush=True)
    return table


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--params", type=Path, required=True)
    args = ap.parse_args()
    build(args.params)
    print("PASS: district differential built")


if __name__ == "__main__":
    main()
