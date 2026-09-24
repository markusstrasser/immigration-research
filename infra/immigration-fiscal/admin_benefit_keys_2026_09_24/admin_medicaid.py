"""Administrative (T-MSIS / TAF) Medicaid and CHIP enrollment by Hispanic ethnicity, national and state.

No survey comparison happens here; the lane's comparison step reads derived/admin_medicaid_taf.csv.

Sources (fetched with curl, bytes pinned in _cache/medicaid/SOURCE_PINS.json; a changed file stops the run):
  dq_*   DQ Atlas "Race and Ethnicity" topic, TAF 2019-2023 Release 1, one CSV per year: state rows with
         the DQ grade, % missing, TAF counts, % Hispanic in TAF (state-reported only, no imputation)
         and in the ACS 5-year benchmark. 2019-2020 files use the old method (shares of ALL records);
         2021+ use shares of records with non-missing race/ethnicity (methods PDF Table 4).
  rei    data.medicaid.gov race-and-ethnicity-2020-2022-01162025.csv: national counts from TAF R1 plus
         the Race/Ethnicity Imputation (REI) companion file (self-report if good, else enhanced BISG).
  wcv/mh data.medicaid.gov well-child and MH/SUD datasets: national race denominators for two
         full-year sub-populations (same REI assignment).
  brief  CMS briefs "Race and ethnicity of the national Medicaid and CHIP population in 2019/2020":
         appendix tables (rounded). 2019 is written out; 2020 is a cross-check of the rei file.
Shares are percent (0-100). "hispanic" counts from the DQ Atlas are derived: share x published count.

Writes derived/admin_medicaid_taf.csv.
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl python3 \
    infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_medicaid.py
"""
import datetime
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/medicaid"
RAW = CACHE / "raw"
PINS = CACHE / "SOURCE_PINS.json"
OUT = HERE / "derived/admin_medicaid_taf.csv"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
DQ_YEARS = [2019, 2020, 2021, 2022, 2023]
DQ_URL = ("https://www.medicaid.gov/dq-atlas/downloads/data-by-year/{y}/Release-1/"
          "TAF-DQ-Race-Ethnicity-{y}-Release-1.csv")
SOURCES = {  # local name -> (url, Wayback timestamp used only if direct and browser-UA fail)
    **{f"dq_race_{y}_r1.csv": (DQ_URL.format(y=y), "2026") for y in DQ_YEARS},
    "dq_race_methods.pdf": ("https://www.medicaid.gov/dq-atlas/downloads/background-and-methods/"
                            "TAF-DQ-Race-Ethnicity.pdf", "2026"),
    "rei_2020_2022.csv": ("https://download.medicaid.gov/data/race-and-ethnicity-2020-2022-01162025.csv",
                          "20250203230126"),
    "well-child-visits-2020-2022-01162025.csv": (
        "https://download.medicaid.gov/data/well-child-visits-2020-2022-01162025.csv", "2026"),
    "mh-and-sud-services-2020-2022-01162025.csv": (
        "https://download.medicaid.gov/data/mh-and-sud-services-2020-2022-01162025.csv", "2026"),
    "brief_2019.pdf": ("https://www.medicaid.gov/medicaid/data-and-systems/downloads/macbis/"
                       "2019-race-etncity-data-brf.pdf", "2026"),
    "brief_2020.pdf": ("https://www.medicaid.gov/sites/default/files/2023-08/2020-race-etncity-data-brf.pdf",
                       "2026"),
    "beneficiary_profile_2023.pdf": ("https://www.medicaid.gov/medicaid/quality-of-care/downloads/"
                                     "beneficiary-profile-2023.pdf", "2026"),
}
POSTAL = dict(zip(
    ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
     "District of Columbia", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa",
     "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota",
     "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
     "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon",
     "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah",
     "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
     "Puerto Rico", "Virgin Islands", "Guam"],
    ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FL", "GA", "HI", "ID", "IL", "IN", "IA",
     "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM",
     "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA",
     "WV", "WI", "WY", "PR", "VI", "GU"]))
STATES51 = [s for s, p in POSTAL.items() if p not in ("PR", "VI", "GU")]
RACES = ["White, non-Hispanic", "Black, non-Hispanic", "Hispanic", "Asian/Pacific Islander, non-Hispanic",
         "American Indian and Alaska Native, non-Hispanic", "Multiracial, non-Hispanic"]
COLS = ["year", "source", "measure", "population_definition", "geography", "state_postal", "total",
        "hispanic", "hispanic_share_known", "hispanic_share_all", "unknown_share", "imputed", "dq_grade",
        "acs_hispanic_share", "source_table", "source_page"]
FAILS = []


def gate(ok, msg):
    print(("  ok   " if ok else "  FAIL ") + msg)
    if not ok:
        FAILS.append(msg)


def fetch_all():
    RAW.mkdir(parents=True, exist_ok=True)
    pins = json.loads(PINS.read_text()) if PINS.exists() else {}
    for name, (url, snap) in SOURCES.items():
        path, route = RAW / name, None
        if not path.exists():
            tmp = path.with_suffix(path.suffix + ".part")
            routes = [("direct", url, []), ("browser-UA", url, ["-A", UA]),
                      ("wayback", f"https://web.archive.org/web/{snap}id_/{url}", [])]
            for label, u, extra in routes:
                r = subprocess.run(["curl", "-sS", "--fail", "-L", *extra, u, "-o", str(tmp)],
                                   capture_output=True, text=True)
                if r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0:
                    tmp.rename(path)
                    route = label
                    break
            else:
                sys.exit(f"[BLOCKED] {name}: {url}")
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if name in pins and pins[name]["sha256"] != digest:
            sys.exit(f"[BLOCKED] {name} bytes changed since pinned: {digest}")
        if name not in pins:
            pins[name] = dict(url=url, retrieved=datetime.date.today().isoformat(), sha256=digest,
                              bytes=path.stat().st_size, route=route)
        print(f"  pinned {name} {digest[:12]} ({pins[name]['route']})")
    PINS.write_text(json.dumps(pins, indent=1) + "\n")


def num(x):
    x = str(x).replace(",", "").strip()
    try:
        return float(x)
    except ValueError:
        return np.nan


def pdf_text(name):
    r = subprocess.run(["pdftotext", "-layout", str(RAW / name), "-"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"pdftotext failed on {name}: {r.stderr[:200]}")
    return r.stdout


# ---------------------------------------------------------------- DQ Atlas (state, self-reported)
DQ_DEF_NEW = ("TAF Annual DE file, non-dummy eligibility records (anyone with a Medicaid or CHIP eligibility "
              "record in the calendar year, all benefit scopes, all ages, Medicaid+CHIP); state-reported "
              "race/ethnicity only, no imputation; % Hispanic among records with non-missing race/ethnicity "
              "(DQ Atlas method from 2021 R1)")
DQ_DEF_OLD = DQ_DEF_NEW.replace("% Hispanic among records with non-missing race/ethnicity (DQ Atlas method from "
                                "2021 R1)", "% Hispanic of ALL records incl. missing (DQ Atlas pre-2021 method)")
assert DQ_DEF_OLD != DQ_DEF_NEW


def read_dq(year):
    rows = pd.read_csv(RAW / f"dq_race_{year}_r1.csv", header=None, dtype=str, keep_default_na=False,
                       encoding="utf-8-sig").values.tolist()
    hi = next(i for i, r in enumerate(rows) if r[0] == "State")
    gate("Race and Ethnicity" in rows[0][0], f"DQ {year}: title row names the Race and Ethnicity topic")
    df = pd.DataFrame([r for r in rows[hi + 1:] if r[0].strip()], columns=rows[hi])
    df = df.loc[:, [c for c in df.columns if c]]
    gate(set(df["Data Year"]) == {str(year)} and set(df["Data Version"]) == {"Release 1"},
         f"DQ {year}: every row is data year {year}, Release 1")
    gate(set(STATES51) <= set(df["State"]), f"DQ {year}: all 50 states + DC present ({len(df)} rows)")
    new = "# Beneficiaries with Non-Missing Race/Ethnicity Values in TAF" in df.columns
    gate(new == (year >= 2021), f"DQ {year}: method = {'non-missing denominator' if new else 'all-records'}")
    cats = (["White, Non-Hispanic", "Black, Non-Hispanic", "Asian and Hawaiian/Pacific Islander, Non-Hispanic",
             "Hispanic", "American Indian and Alaska Native, Non-Hispanic", "Multiracial, Non-Hispanic"] if new
            else ["White, Non-Hispanic", "Black, Non-Hispanic", "Asian, Non-Hispanic", "Hispanic", "All Other"])
    miss = df["% Beneficiaries with Missing Race/Ethnicity Values in TAF"].map(num)
    taf_sum = sum(df[f"% {c} Beneficiaries in TAF"].map(num) for c in cats)
    acs_sum = sum(df[f"% {c} Beneficiaries in ACS"].map(num) for c in cats)
    s51 = df["State"].isin(STATES51)
    if new:
        bad = df.loc[s51 & ((taf_sum - 100).abs() > 1.0), "State"].tolist()
        gate(not bad, f"DQ {year}: TAF category shares sum to 100 +-1 in all 51 (off: {bad})")
    else:  # pre-2021 method: flag-8 records (non-Hispanic, race unreported) are neither missing nor categorized
        resid = 100 - taf_sum - miss
        gate(bool((resid[s51] >= -1).all()), f"DQ {year}: TAF category shares + % missing <= 101 in all 51")
        big = {st: round(v, 1) for st, v in zip(df.loc[s51, "State"], resid[s51]) if v > 1}
        print(f"  info DQ {year}: uncategorized non-missing records (flag 8, methods Table 4) > 1 pt: {big}")
    bad = df.loc[s51 & ((acs_sum < 97) | (acs_sum > 100.5)), "State"].tolist()
    gate(not bad, f"DQ {year}: ACS category shares sum to 97-100.5 in all 51 (off: {bad})")
    low = {st: round(v, 1) for st, v in zip(df.loc[s51, "State"], acs_sum[s51]) if v < 99}
    print(f"  info DQ {year}: ACS categories sum < 99 (non-Hispanic 'some other race' left out): {low}")
    out = []
    for _, r in df.iterrows():
        total, m = num(r["# Beneficiaries in TAF"]), num(r["% Beneficiaries with Missing Race/Ethnicity Values in TAF"])
        h_pct, acs = num(r["% Hispanic Beneficiaries in TAF"]), num(r["% Hispanic Beneficiaries in ACS"])
        if new:
            known = num(r["# Beneficiaries with Non-Missing Race/Ethnicity Values in TAF"])
            hisp = h_pct / 100 * known
            share_known = h_pct
        else:  # known = categorized records, so flag-8 records count as unknown as under the 2021+ method
            known = total * taf_sum[_] / 100
            hisp = h_pct / 100 * total
            share_known = 100 * hisp / known if known else np.nan
            m = 100 - taf_sum[_]
        out.append(dict(year=year, source="CMS DQ Atlas, Race and Ethnicity topic (TAF R1 vs ACS 5-yr)",
                        measure="enrollees", population_definition=DQ_DEF_NEW if new else DQ_DEF_OLD,
                        geography=r["State"], state_postal=POSTAL[r["State"]], total=total, hispanic=hisp,
                        known=known, acs_total=num(r["# Beneficiaries in ACS"]),
                        hispanic_share_known=share_known,
                        hispanic_share_all=100 * hisp / total if total else np.nan, unknown_share=m,
                        imputed="no", dq_grade=r["DQ Assessment"], acs_hispanic_share=acs,
                        source_table=f"TAF-DQ-Race-Ethnicity-{year}-Release-1.csv",
                        source_page=f"row State={r['State']}; cols '% Hispanic Beneficiaries in TAF/ACS'"))
    d = pd.DataFrame(out)
    if new:  # the published non-missing count must equal total x (1 - missing%) up to rounding
        ok = d[d.geography.isin(STATES51)]
        dev = (ok.known / ok.total - (1 - ok.unknown_share / 100)).abs()
        gate(bool((dev < 0.0006).all()), f"DQ {year}: non-missing count = total x (1 - % missing), max dev "
             f"{dev.max():.5f}")
    return d


def dq_national(d, year, label, keep):
    s = d[d.geography.isin(STATES51) & keep]
    total, known, hisp = s.total.sum(), s.known.sum(), s.hispanic.sum()
    acs_h = (s.acs_total * s.acs_hispanic_share / 100).sum() / s.acs_total.sum() * 100
    return dict(year=year, source="CMS DQ Atlas state rows, summed here",
                measure="enrollees", population_definition=s.population_definition.iloc[0],
                geography=label, state_postal="US", total=total, hispanic=hisp,
                hispanic_share_known=100 * hisp / known, hispanic_share_all=100 * hisp / total,
                unknown_share=100 * (1 - known / total), imputed="no", dq_grade=f"{len(s)} states",
                acs_hispanic_share=acs_h, source_table=f"TAF-DQ-Race-Ethnicity-{year}-Release-1.csv",
                source_page="[CALCULATION] sum of state rows (hispanic = share x count; ACS weighted by "
                            "'# Beneficiaries in ACS')")


# ---------------------------------------------------------------- national REI files
REI_DEF = {
    "Medicaid and CHIP enrollees": "all Medicaid+CHIP enrollees, any scope of benefits, enrolled >=1 day in the "
                                   "year, all ages, incl. duals",
    "Comprehensive benefits": "enrollees with comprehensive benefits, enrolled >=1 day, all ages, incl. duals",
    "Limited benefits": "enrollees with limited benefits only (family planning, emergency services, Medicare "
                        "premium/cost-sharing help), enrolled >=1 day",
    "Child": "comprehensive-benefit enrollees aged 18 or younger, enrolled >=1 day",
    "Adult": "comprehensive-benefit enrollees aged 19+, enrolled >=1 day, incl. duals",
}
REI_TAIL = ("; 50 states + DC + Puerto Rico (VI, Guam, AS, MP excluded); TAF R1 + Race/Ethnicity Imputation "
            "companion file: state-reported race/ethnicity if present and good quality, else enhanced BISG "
            "(surname, geography, first name, AIAN certification; 26% of enrollees imputed in 2019-2020 briefs)")


def read_rei():
    df = pd.read_csv(RAW / "rei_2020_2022.csv", dtype=str, encoding="utf-8-sig")
    gate(len(df) == 216 and set(df.Geography) == {"National"} and set(df["Data version"]) == {"TAF Release 1"},
         f"REI: 216 national TAF R1 rows ({len(df)})")
    gate(set(df.Category) == set(RACES), "REI: six race/ethnicity categories")
    df["n"] = df["Count of enrollees"].map(num)
    df["den"] = df["Denominator count of enrollees"].map(num)
    rows = []
    for (year, topic, sub), g in df.groupby(["Year", "Subpopulation topic", "Subpopulation"], sort=False):
        g = g.set_index("Category")
        if topic == "Eligibility category":  # count = race r in category e; denominator = race r's total
            total, sum6 = g.n.sum(), g.n.sum()
            definition = (f"comprehensive-benefit enrollees in eligibility category '{sub}' (latest eligibility "
                          f"group), enrolled >=1 day")
        else:
            total, sum6 = g.den.iloc[0], g.n.sum()
            gate(g.den.nunique() == 1, f"REI {year} {sub}: one denominator across races")
            definition = REI_DEF[sub]
        h = g.loc["Hispanic", "n"]
        rows.append(dict(year=int(year), source="CMS data.medicaid.gov, Race and ethnicity of the national "
                         "Medicaid and CHIP population (TAF R1 + REI)", measure="enrollees",
                         population_definition=definition + REI_TAIL, geography="United States (50+DC+PR)",
                         state_postal="US+PR", total=total, hispanic=h, hispanic_share_known=100 * h / sum6,
                         hispanic_share_all=100 * h / total, unknown_share=100 * (1 - sum6 / total),
                         imputed="partial", dq_grade="", acs_hispanic_share=np.nan,
                         source_table="race-and-ethnicity-2020-2022-01162025.csv",
                         source_page=f"Subpopulation topic={topic}; Subpopulation={sub}; Category=Hispanic"))
        if topic == "Total enrollees":
            gate(abs(sum6 - total) <= 0.001 * total, f"REI {year}: six race counts sum to all enrollees "
                 f"({sum6:,.0f} vs {total:,.0f})")
    d = pd.DataFrame(rows)
    for year in d.year.unique():
        y = d[d.year == year].set_index("source_page")
        t = lambda sub: y.loc[[p for p in y.index if f"Subpopulation={sub};" in p][0]]
        allr, comp, lim, ch, ad = (t(s) for s in ["Medicaid and CHIP enrollees", "Comprehensive benefits",
                                                  "Limited benefits", "Child", "Adult"])
        gate(abs(comp.total + lim.total - allr.total) <= 0.001 * allr.total,
             f"REI {year}: comprehensive + limited = all enrollees")
        gate(abs(comp.hispanic + lim.hispanic - allr.hispanic) <= 0.001 * allr.hispanic,
             f"REI {year}: Hispanic comprehensive + limited = Hispanic all")
        gate(abs(ch.total + ad.total - comp.total) <= 0.01 * comp.total,
             f"REI {year}: child + adult = comprehensive within 1% ({(ch.total + ad.total) / comp.total:.4f})")
    return d


def read_sub(name, label, definition):
    df = pd.read_csv(RAW / name, dtype=str, encoding="utf-8-sig")
    df["den"] = df["Denominator count of enrollees"].map(num)
    rows = []
    for year, g in df.groupby("Year"):
        race = g[g["Subpopulation topic"] == "Race and ethnicity"]
        gate(race.groupby("Subpopulation").den.nunique().max() == 1,
             f"{label} {year}: one denominator per race across outcome categories")
        race = race.drop_duplicates("Subpopulation")
        tot = g[g["Subpopulation topic"] == "Total enrollees"].den.iloc[0]
        gate(set(race.Subpopulation) == set(RACES), f"{label} {year}: six race denominators")
        s6 = race.den.sum()
        gate(0.99 * tot <= s6 <= tot, f"{label} {year}: race denominators {s6:,.0f} within 1% below total "
             f"{tot:,.0f} (VI excluded from race rows)")
        h = race.set_index("Subpopulation").loc["Hispanic", "den"]
        rows.append(dict(year=int(year), source=f"CMS data.medicaid.gov, {label} (TAF R1 + REI)",
                         measure="enrollees", population_definition=definition + REI_TAIL.replace(
                             "Puerto Rico (VI", "Puerto Rico (race rows exclude VI;"),
                         geography="United States (50+DC+PR)", state_postal="US+PR", total=s6, hispanic=h,
                         hispanic_share_known=100 * h / s6, hispanic_share_all=100 * h / s6, unknown_share=0.0,
                         imputed="partial", dq_grade="", acs_hispanic_share=np.nan, source_table=name,
                         source_page="Subpopulation topic=Race and ethnicity; Denominator count of enrollees"))
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- CMS briefs (appendix tables, rounded)
BRIEF_COLS = ["us_pop", "all", "comprehensive", "limited", "child", "adult", "older_adult", "disability",
              "expansion", "nonexpansion", "medicaid_children", "chip", "pregnancy"]


def mval(tok):
    return float(tok.rstrip("M")) * 1e6


def read_brief(year):
    txt = pdf_text(f"brief_{year}.pdf")
    gate(f"Race and ethnicity of the national\nMedicaid and CHIP population in {year}" in txt
         or f"population in {year}" in txt[:400], f"brief {year}: title matches")
    app = txt[re.search(r"6 – Appendix\s*\n\s*Number of Medicaid", txt).start():]
    hdr = next(line for line in app.splitlines() if "(327M)" in line)
    totals = [mval(t) for t in re.findall(r"\(([\d.]+M)\)", hdr)]
    hisp = next(line for line in app.splitlines() if re.match(r"\s+Hispanic\s+[\d.]+M", line))
    hvals = [mval(t) for t in re.findall(r"([\d.]+M)", hisp)]
    gate(len(totals) == 13 and len(hvals) == 13, f"brief {year}: appendix header and Hispanic row have 13 cells")
    good = re.search(r"available and of good quality \((\d+) percent of enrollees overall\)", txt)
    imputed = 100 - int(good.group(1))
    gate(f"({imputed}" in txt and imputed == 26, f"brief {year}: {good.group(1)}% self-reported, "
         f"{imputed}% indirectly estimated (p.2)")
    return dict(zip(BRIEF_COLS, totals)), dict(zip(BRIEF_COLS, hvals))


def brief_rows(year, tot, hisp):
    defs = {"all": "Medicaid and CHIP enrollees", "comprehensive": "Comprehensive benefits",
            "limited": "Limited benefits", "child": "Child", "adult": "Adult"}
    return [dict(year=year, source=f"CMS brief, Race and ethnicity of the national Medicaid and CHIP population "
                 f"in {year} (rounded millions)", measure="enrollees",
                 population_definition=REI_DEF[v] + REI_TAIL, geography="United States (50+DC+PR)",
                 state_postal="US+PR", total=tot[k], hispanic=hisp[k],
                 hispanic_share_known=100 * hisp[k] / tot[k], hispanic_share_all=100 * hisp[k] / tot[k],
                 unknown_share=0.0, imputed="partial", dq_grade="", acs_hispanic_share=np.nan,
                 source_table=f"{year}-race-etncity-data-brf.pdf, Appendix table",
                 source_page=f"p.7, column '{v}', row Hispanic (rounded to 0.1-1M)") for k, v in defs.items()]


def main():
    print("fetch + pin")
    fetch_all()
    methods = pdf_text("dq_race_methods.pdf")
    gate("non-dummy enrollment records in the TAF DE file" in methods.replace("\n", " ").replace("non- dummy", "non-dummy")
         or "dummy enrollment records" in methods, "DQ methods PDF: universe = non-dummy DE records")
    bp = pdf_text("beneficiary_profile_2023.pdf")
    i = bp.index("Percentage of Medicaid and CHIP Beneficiaries by Race")
    gate("American Community Survey" in bp[i:i + 3000] and "T-MSIS" not in bp[i:i + 3000],
         "2023 Beneficiary Profile race chart (p.22) is ACS PUMS survey data, not TAF: excluded")
    print("DQ Atlas")
    dq = pd.concat([read_dq(y) for y in DQ_YEARS], ignore_index=True)
    nat = []
    for y in DQ_YEARS:
        d = dq[dq.year == y]
        nat.append(dq_national(d, y, "United States (50+DC), sum of DQ Atlas states", d.total.notna()))
        nat.append(dq_national(d, y, "United States (50+DC), Low/Medium-concern states only",
                               d.dq_grade.isin(["Low concern", "Medium concern"])))
    print("REI national")
    rei = read_rei()
    wcv = read_sub("well-child-visits-2020-2022-01162025.csv", "well-child visit data set",
                   "children younger than 19 on Dec 31 with comprehensive Medicaid or CHIP for all 12 months")
    mh = read_sub("mh-and-sud-services-2020-2022-01162025.csv", "MH/SUD services data set",
                  "ages 12-64 on Dec 31, not dually eligible, continuously enrolled with comprehensive benefits "
                  "12 months (no more than one gap >45 days per data set text); select states with TAF quality "
                  "issues excluded")
    print("CMS briefs")
    t19, h19 = read_brief(2019)
    t20, h20 = read_brief(2020)
    r20 = rei[rei.year == 2020].set_index("source_page")
    for k, sub in [("all", "Medicaid and CHIP enrollees"), ("comprehensive", "Comprehensive benefits"),
                   ("limited", "Limited benefits"), ("child", "Child"), ("adult", "Adult")]:
        row = r20.loc[[p for p in r20.index if f"Subpopulation={sub};" in p][0]]
        tol = 0.5e6 if t20[k] >= 10e6 else 0.05e6
        gate(abs(row.total - t20[k]) <= tol and abs(row.hispanic - h20[k]) <= (0.5e6 if h20[k] >= 10e6 else 0.05e6),
             f"brief 2020 {k}: {t20[k] / 1e6:.1f}M/{h20[k] / 1e6:.1f}M matches data file "
             f"{row.total / 1e6:.2f}M/{row.hispanic / 1e6:.2f}M")
    print("state vs national")
    for y in (2020, 2021, 2022):
        d = dq[(dq.year == y) & dq.geography.isin(STATES51 + ["Puerto Rico"])]
        n = rei[(rei.year == y) & rei.source_page.str.contains("Subpopulation=Medicaid and CHIP enrollees;")]
        ratio = d.total.sum() / n.total.iloc[0]
        gate(0.97 <= ratio <= 1.03, f"{y}: DQ Atlas 50+DC+PR records {d.total.sum():,.0f} vs REI national "
             f"{n.total.iloc[0]:,.0f} (ratio {ratio:.4f})")
    # national REI Hispanic share with Puerto Rico removed: PR count from the DQ Atlas, PR Hispanic share bounded
    ex = []
    for y in (2020, 2021, 2022):
        n = rei[(rei.year == y) & rei.source_page.str.contains("Subpopulation=Medicaid and CHIP enrollees;")].iloc[0]
        pr = dq[(dq.year == y) & (dq.geography == "Puerto Rico")].iloc[0]
        by_s = []  # 50+DC Hispanic share if PR records are s Hispanic: s = PR's TAF share of known, then 1.0
        for s in (pr.hispanic_share_known / 100, 1.0):
            h = n.hispanic - s * pr.total
            by_s.append(100 * h / (n.total - pr.total))
        r = n.to_dict()
        r.update(geography="United States (50+DC), REI national minus Puerto Rico", state_postal="US",
                 total=n.total - pr.total, hispanic=n.hispanic - pr.total,
                 hispanic_share_known=by_s[1], hispanic_share_all=by_s[1],
                 source_page=f"[CALCULATION] REI all enrollees minus PR records from DQ Atlas {y} "
                             f"({pr.total:,.0f}) at 100% Hispanic; at PR's TAF share "
                             f"{pr.hispanic_share_known:.1f}% the result is {by_s[0]:.2f}%")
        ex.append(r)
    out = pd.concat([pd.DataFrame(nat), dq, rei, pd.DataFrame(ex), wcv, mh,
                     pd.DataFrame(brief_rows(2019, t19, h19))], ignore_index=True)[COLS]
    out["total"] = out.total.round(0)
    out["hispanic"] = out.hispanic.round(0)
    for c in ["hispanic_share_known", "hispanic_share_all", "unknown_share", "acs_hispanic_share"]:
        out[c] = out[c].astype(float).round(3) + 0.0  # + 0.0 turns -0.0 into 0.0
    gate(out.duplicated(["year", "source", "geography", "population_definition"]).sum() == 0, "no duplicate keys")
    if FAILS:
        sys.exit(f"{len(FAILS)} gate(s) failed; nothing written")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(OUT, index=False, lineterminator="\n")
    print(f"wrote {OUT.relative_to(HERE)}: {len(out)} rows")
    show = out[out.state_postal.isin(["US", "US+PR", "TX", "CA", "AZ", "NM", "NV"])
               & ~out.source_page.str.contains("Eligibility category")]
    with pd.option_context("display.width", 250, "display.max_columns", 20, "display.max_rows", 200):
        print(show[["year", "source_table", "geography", "state_postal", "total", "hispanic",
                    "hispanic_share_known", "hispanic_share_all", "unknown_share", "dq_grade",
                    "acs_hispanic_share"]].to_string(index=False))


if __name__ == "__main__":
    main()
