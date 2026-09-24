#!/usr/bin/env python3
"""TANF and SSP-MOE recipient characteristics by ethnicity and citizenship, FY2022-FY2024.

Source: HHS ACF Office of Family Assistance, "Characteristics and Financial Circumstances of
TANF Recipients", one Excel workbook per fiscal year (average month of the fiscal year).
Writes derived/admin_tanf.csv. Every number is read from the workbooks; the gates below stop the
script on any inconsistency.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl \
      python3 infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_tanf.py [--refetch]
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import openpyxl
import pandas as pd

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache" / "wic_tanf"
PINS = CACHE / "SOURCE_PINS.json"
OUT = LANE / "derived" / "admin_tanf.csv"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120 Safari/537.36")
REFETCH = "--refetch" in sys.argv

PAGE = "https://acf.gov/ofa/data/characteristics-and-financial-circumstances-tanf-recipients-fiscal-year-{fy}"
SOURCES = {
    2024: "https://acf.gov/system/files/filefield_paths/fy2024-characteristics.xlsx",
    2023: "https://acf.gov/sites/default/files/documents/ofa/fy2023_characteristics.xlsx",
    2022: "https://acf.gov/sites/default/files/documents/ofa/fy2022_characteristics.xlsx",
}
INSTRUCTIONS = ("https://acf.gov/sites/default/files/documents/ofa/"
                "acf-199209-TANFSSP-data-report-instructions-valid-thru-2028-12.pdf")

POSTAL = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
    "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL",
    "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
    "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
    "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA",
    "Washington": "WA", "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "Guam": "GU", "Puerto Rico": "PR", "Virgin Islands": "VI",
}
TERRITORIES = {"GU", "PR", "VI"}
US = "United States"


# ---------------------------------------------------------------- fetch and pin
def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def load_pins() -> dict:
    return json.loads(PINS.read_text()) if PINS.exists() else {}


def save_pins(update: dict) -> None:
    pins = load_pins()  # merge: admin_wic.py writes the same file
    pins.update(update)
    PINS.write_text(json.dumps(dict(sorted(pins.items())), indent=2) + "\n")


def fetch(url: str, dest: Path, valid, pins_update: dict) -> Path:
    """Download url to dest via plain curl, browser UA, then Wayback; pin sha256 and route."""
    rel = str(dest.relative_to(CACHE))
    pin = load_pins().get(rel)
    if dest.exists() and not REFETCH:
        if pin and pin["sha256"] != sha256(dest):
            sys.exit(f"[BLOCKED] {rel}: cached file does not match its pin; source changed?")
        if not pin:
            pins_update[rel] = {"url": url, "retrieved": "unknown (pre-existing cache file)",
                                "sha256": sha256(dest), "bytes": dest.stat().st_size,
                                "route": "unknown"}
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.stem + ".part" + dest.suffix)  # keep the extension for openpyxl
    routes = [("plain curl", url, False), ("curl with browser User-Agent", url, True),
              ("Wayback Machine", "https://web.archive.org/web/2026id_/" + url, True)]
    log = []
    for name, u, ua in routes:
        cmd = ["curl", "-sS", "--fail", "-L", "--max-time", "600", "-o", str(tmp),
               "-w", "%{http_code} %{url_effective}"]
        if ua:
            cmd += ["-A", UA]
        r = subprocess.run(cmd + [u], capture_output=True, text=True)
        ok = r.returncode == 0 and tmp.exists() and tmp.stat().st_size > 0 and valid(tmp)
        log.append(f"{name}: rc={r.returncode} {r.stdout.strip()} valid={ok}")
        if ok:
            got = sha256(tmp)
            if pin and pin["sha256"] != got:
                if dest.suffix != ".html":
                    sys.exit(f"[BLOCKED] {rel}: refetched bytes differ from the pin "
                             f"({got[:12]} vs {pin['sha256'][:12]}); source changed")
                # landing pages carry per-request markup; the gates re-read their content
                print(f"! {rel}: page bytes changed since the pin; re-pinned (content re-validated)")
            shutil.move(tmp, dest)
            pins_update[rel] = {"url": url, "retrieved": dt.date.today().isoformat(),
                                "sha256": got, "bytes": dest.stat().st_size,
                                "route": f"{name} ({r.stdout.strip().split(' ', 1)[-1]})"}
            save_pins({rel: pins_update[rel]})  # pin at once, so a later crash cannot orphan the file
            print(f"fetched {rel} via {name}")
            return dest
    tmp.unlink(missing_ok=True)
    sys.exit(f"[BLOCKED] {url}: " + " | ".join(log))


def is_xlsx(p: Path) -> bool:
    if p.read_bytes()[:4] != b"PK\x03\x04":
        return False
    wb = openpyxl.load_workbook(p, read_only=True)
    return "List of Tables (R)" in wb.sheetnames or len(wb.sheetnames) > 60


def is_pdf(p: Path) -> bool:
    return p.read_bytes()[:5] == b"%PDF-" and p.stat().st_size > 50_000


def is_page(p: Path) -> bool:
    return "Characteristics and Financial Circumstances of TANF Recipients" in p.read_text(
        encoding="utf-8", errors="replace")


# ---------------------------------------------------------------- workbook parsing
def norm(s) -> str:
    return re.sub(r"\s+", " ", str(s).replace("_x000D_", " ")).strip()


def find_table(wb, title_re: str):
    """Return (table number, title, rows) of the sheet whose title row matches title_re."""
    hits = []
    for sn in wb.sheetnames:
        ws = wb[sn]
        head = [norm(c) for r in ws.iter_rows(min_row=1, max_row=4, values_only=True)
                for c in r if c is not None]
        text = " / ".join(head)
        m = re.search(r"Table\s*(\d+)\.", text)
        title = next((h for h in head if re.search(title_re, h)), None)
        if m and title:
            hits.append((int(m.group(1)), title, [list(r) for r in ws.iter_rows(values_only=True)]))
    if len(hits) != 1:
        sys.exit(f"[GATE] expected one sheet matching {title_re!r}, found {[(h[0], h[1]) for h in hits]}")
    return hits[0]


def table_rows(rows):
    """Split a sheet into (header, {geography: values}); stops at the first footnote row."""
    hi = next(i for i, r in enumerate(rows) if r and r[0] is not None and norm(r[0]).upper() == "STATE")
    header = [norm(c) if c is not None else "" for c in rows[hi]]
    data = {}
    for r in rows[hi + 1:]:
        if r[0] is None or not norm(r[0]):
            if any(c is not None for c in r):
                sys.exit(f"[GATE] unlabeled data row {r}")
            continue
        name = norm(r[0])
        if re.match(r"^(\d+\.|Note|Source|\*\*)", name):
            break
        geo = US if name.startswith("U.S.") else name
        if geo != US and geo not in POSTAL:
            sys.exit(f"[GATE] unknown geography {name!r}")
        if geo in data:
            sys.exit(f"[GATE] duplicate geography {geo!r}")
        data[geo] = r
    return header, data


def col(header, pattern, start=1, nth=0):
    idx = [i for i, h in enumerate(header) if i >= start and re.search(pattern, h, re.I)]
    if len(idx) <= nth:
        sys.exit(f"[GATE] no column matching {pattern!r} in {header}")
    return idx[nth]


def num(v):
    """Numeric cell -> float; '**' (suppressed) -> None."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = norm(v)
    if s == "**":
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        sys.exit(f"[GATE] non-numeric cell {v!r}")


# ---------------------------------------------------------------- gates
GATE_LOG: list[str] = []


def gate(ok: bool, msg: str):
    GATE_LOG.append(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        print("\n".join(GATE_LOG))
        sys.exit(f"[GATE FAILED] {msg}")


def check_distribution(fy, tno, data, cols, total_col, tol=0.5):
    """Each row's percent distribution sums to ~100 (suppressed rows skipped)."""
    worst = 0.0
    for geo, r in data.items():
        vals = [num(r[c]) for c in cols]
        if any(v is None for v in vals) or not num(r[total_col]):
            continue
        dev = abs(sum(vals) - 100)
        worst = max(worst, dev)
        gate(dev <= tol, f"FY{fy} T{tno} {geo}: distribution sums to {sum(vals):.1f}")
    return worst


def check_national(fy, tno, data, total_col, pct_cols):
    """U.S. row = sum of state rows (counts) and the count-weighted mean of state percents."""
    states = {g: r for g, r in data.items() if g != US}
    us_total = num(data[US][total_col])
    s = sum(num(r[total_col]) for r in states.values())
    tol = 0.5 * len(states) + 1
    gate(abs(s - us_total) <= tol,
         f"FY{fy} T{tno}: sum of {len(states)} state counts {s:,.0f} vs U.S. {us_total:,.0f} (tol {tol})")
    for c in pct_cols:
        w = sum(num(r[total_col]) * num(r[c]) for r in states.values()) / s
        us = num(data[US][c])
        gate(abs(w - us) <= 0.1,
             f"FY{fy} T{tno} col {c}: weighted state mean {w:.3f} vs U.S. {us} (tol 0.1)")


# ---------------------------------------------------------------- per-year extraction
def page_highlights(p: Path) -> dict:
    t = html.unescape(re.sub(r"<[^>]+>", " ", p.read_text(encoding="utf-8", errors="replace")))
    t = re.sub(r"\s+", " ", t)
    out = {}
    m = re.search(r"About ([\d,]+) adults and ([\d.]+) million children received TANF", t)
    if m:
        out["adults"] = float(m.group(1).replace(",", ""))
        out["children_m"] = float(m.group(2))
    m = re.search(r"approximately ([\d,]+) child-only families.*?accounted for ([\d.]+) percent", t)
    if m:
        out["child_only_families"] = float(m.group(1).replace(",", ""))
        out["child_only_pct"] = float(m.group(2))
    return out


def extract_year(fy: int, xlsx: Path, page: Path) -> list[dict]:
    wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
    t = {}
    specs = {
        "fam_size": r"^TANF Families by Number of Individuals in the Assistance Unit",
        "fam_adults": r"^TANF Families by Number of Adult Recipients",
        "no_adult": r"^TANF Families with No Adult Recipient by Number of Child Recipients",
        "rec_race": r"^TANF Recipients by Race/Ethnicity",
        "adult_race": r"^TANF Adult Recipients by Race/Ethnicity",
        "child_race": r"^TANF Child Recipients by Race/Ethnicity",
        "adult_cit": r"^TANF Adult Recipients by Citizenship Status",
        "child_cit": r"^TANF Child Recipients by Citizenship Status",
        "sample": r"^TANF Active Caseload, Sample Size",
        "ssp_fam": r"^SSP-MOE Families by Number of Individuals",
        "ssp_race": r"^SSP-MOE Recipients by Race/Ethnicity",
        "ssp_cit": r"^SSP-MOE Recipients by Citizenship Status",
        "ssp_ac_cit": r"^SSP-MOE Adult/Child Recipients by Citizenship Status",
    }
    for k, pat in specs.items():
        tno, title, rows = find_table(wb, pat)
        gate(f"FY{fy}" in title.replace(" ", "") or k == "sample",
             f"FY{fy} T{tno} title carries the fiscal year: {title[:70]}")
        header, data = table_rows(rows)
        t[k] = (tno, header, data)

    # --- column positions (by header text)
    def race_cols(h):
        return [col(h, r"^Hispanic"), col(h, r"^White"), col(h, r"^Black"), col(h, r"American Indian"),
                col(h, r"^Asian"), col(h, r"Native Hawaiian"), col(h, r"Multi"), col(h, r"Unknown")]

    def cit_cols(h, start=1):
        return [col(h, r"U\.S\. Citizen", start), col(h, r"Qualified", start), col(h, r"Unknown", start)]

    # --- gates on TANF tables
    for k in ("rec_race", "adult_race", "child_race"):
        tno, h, d = t[k]
        check_distribution(fy, tno, d, race_cols(h), 1)
        check_national(fy, tno, d, 1, [race_cols(h)[0], race_cols(h)[-1]])
    for k in ("adult_cit", "child_cit"):
        tno, h, d = t[k]
        check_distribution(fy, tno, d, cit_cols(h), 1)
        check_national(fy, tno, d, 1, cit_cols(h)[1:])
    tno, h, d = t["fam_adults"]
    fa_cols = [col(h, r"^0 Adult"), col(h, r"^1 Adult"), col(h, r"^2 or More Adult")]
    check_distribution(fy, tno, d, fa_cols, 1)
    check_national(fy, tno, d, 1, [fa_cols[0]])

    geos = list(t["fam_adults"][2])
    for k in t:
        if not k.startswith("ssp"):
            gate(set(t[k][2]) == set(geos), f"FY{fy} {k}: same {len(geos)} geographies as Table 3")
    gate(len(geos) == 55 and all(g in t["fam_adults"][2] for g in POSTAL),
         f"FY{fy}: U.S. + 50 states + DC + GU + PR + VI present ({len(geos)} rows)")
    for g in geos:  # cross-table identities
        fam1 = num(t["fam_size"][2][g][1])
        fam3 = num(t["fam_adults"][2][g][1])
        gate(abs(fam1 - fam3) <= 1, f"FY{fy} {g}: families T1 {fam1:,.0f} = T3 {fam3:,.0f}")
        a19, a23 = num(t["adult_race"][2][g][1]), num(t["adult_cit"][2][g][1])
        c33, c35 = num(t["child_race"][2][g][1]), num(t["child_cit"][2][g][1])
        r10 = num(t["rec_race"][2][g][1])
        gate(abs(a19 - a23) <= 1 and abs(c33 - c35) <= 1,
             f"FY{fy} {g}: adults T19=T23 ({a19:,.0f}/{a23:,.0f}), children T33=T35 ({c33:,.0f}/{c35:,.0f})")
        gate(abs(r10 - a19 - c33) <= 2, f"FY{fy} {g}: recipients T10 {r10:,.0f} = adults + children")

    # --- page highlights (the release page quotes rounded national figures)
    hl = page_highlights(page)
    us_ad = num(t["adult_race"][2][US][1])
    if "adults" in hl:
        gate(round(us_ad, -2) == hl["adults"], f"FY{fy} page: adults {hl['adults']:,.0f} = T19 {us_ad:,.0f} rounded")
        gate(round(num(t["child_race"][2][US][1]) / 1e6, 1) == hl["children_m"],
             f"FY{fy} page: children {hl['children_m']}m = T33 rounded")
    if "child_only_families" in hl:
        # The page's count equals families x the rounded share (FY2024: 839,144 x 40.9% = 343,210),
        # not Table 5 (343,034); accept a gap within the rounding of that share.
        no_ad = num(t["no_adult"][2][US][1])
        fam = num(t["fam_adults"][2][US][1])
        tol = fam * 0.0005 + 50
        gate(abs(no_ad - hl["child_only_families"]) <= tol,
             f"FY{fy} page: child-only families {hl['child_only_families']:,.0f} vs T5 {no_ad:,.1f} "
             f"(tol {tol:,.0f} = rounding of the published share)")
        gate(num(t["fam_adults"][2][US][fa_cols[0]]) == hl["child_only_pct"],
             f"FY{fy} page: child-only share {hl['child_only_pct']} = T3")
    if not hl:
        GATE_LOG.append(f"SKIP FY{fy} page carries no highlight figures")

    # --- TANF rows
    src_file = xlsx.name
    tn = {k: v[0] for k, v in t.items()}
    rows = []
    s_tno, s_h, s_d = t["sample"]
    s_n = col(s_h, r"Annual Sample")
    s_m = col(s_h, r"50%")
    for g in geos:
        rr, ar, cr = (t[k][2][g] for k in ("rec_race", "adult_race", "child_race"))
        rh, ah, ch = (race_cols(t[k][1]) for k in ("rec_race", "adult_race", "child_race"))
        acit, ccit = t["adult_cit"][2][g], t["child_cit"][2][g]
        ach, cch = cit_cols(t["adult_cit"][1]), cit_cols(t["child_cit"][1])
        adults, children, recips = num(ar[1]), num(cr[1]), num(rr[1])
        rec = {
            "fiscal_year": fy, "program": "TANF", "geography": g,
            "state_postal": "US" if g == US else POSTAL[g],
            "families": num(t["fam_adults"][2][g][1]), "adults": adults, "children": children,
            "adult_hispanic_pct": num(ar[ah[0]]), "adult_eth_unknown_pct": num(ar[ah[-1]]),
            "child_hispanic_pct": num(cr[ch[0]]), "child_eth_unknown_pct": num(cr[ch[-1]]),
            "child_only_family_pct": num(t["fam_adults"][2][g][fa_cols[0]]),
            "adult_noncitizen_pct": num(acit[ach[1]]), "child_noncitizen_pct": num(ccit[cch[1]]),
            "source_table": ";".join(f"T{tn[k]}" for k in ("fam_adults", "rec_race", "adult_race",
                                     "child_race", "adult_cit", "child_cit", "sample")),
            "source_file": src_file,
            "geography_type": "national" if g == US else ("territory" if POSTAL[g] in TERRITORIES else "state"),
            "recipients": recips, "recipient_hispanic_pct": num(rr[rh[0]]),
            "recipient_eth_unknown_pct": num(rr[rh[-1]]),
            "adult_cit_unknown_pct": num(acit[ach[2]]), "child_cit_unknown_pct": num(ccit[cch[2]]),
            "annual_sample_cases": num(s_d[g][s_n]) if g in s_d else None,
            "margin_pts_50pct_95ci": num(s_d[g][s_m]) if g in s_d else None,
            "notes": "counts are average monthly; percents published; noncitizen = 'Qualified Immigrant'",
        }
        rows.append(rec)

    # --- SSP-MOE rows (states only; no U.S. row is published)
    f_tno, f_h, f_d = t["ssp_fam"]
    r_tno, r_h, r_d = t["ssp_race"]
    c_tno, c_h, c_d = t["ssp_cit"]
    a_tno, a_h, a_d = t["ssp_ac_cit"]
    gate(set(f_d) == set(r_d) == set(c_d) == set(a_d) and US not in f_d,
         f"FY{fy} SSP-MOE tables share {len(f_d)} state rows, no U.S. row")
    ssp_race = race_cols(r_h)
    ssp_cit = cit_cols(c_h)
    ad_i = col(a_h, r"Total Adult")
    ch_i = col(a_h, r"Total Child")
    ad_cit = cit_cols(a_h, ad_i + 1)
    ch_cit = cit_cols(a_h, ch_i + 1)
    gate(ad_cit[-1] < ch_i, f"FY{fy} T{a_tno}: adult block precedes child block")
    check_distribution(fy, r_tno, r_d, ssp_race, 1)
    check_distribution(fy, c_tno, c_d, ssp_cit, 1)
    for g in f_d:
        rt, ct = num(r_d[g][1]), num(c_d[g][1])
        ad, chn = num(a_d[g][ad_i]), num(a_d[g][ch_i])
        gate(abs(rt - ct) <= 1 and abs(ad + chn - rt) <= 2,
             f"FY{fy} SSP-MOE {g}: recipients T{r_tno} {rt:,.0f} = T{c_tno} {ct:,.0f} = adults+children {ad + chn:,.0f}")
        suppressed = num(r_d[g][ssp_race[0]]) is None
        rows.append({
            "fiscal_year": fy, "program": "SSP-MOE", "geography": g, "state_postal": POSTAL[g],
            "families": num(f_d[g][1]), "adults": ad, "children": chn,
            "adult_hispanic_pct": None, "adult_eth_unknown_pct": None,
            "child_hispanic_pct": None, "child_eth_unknown_pct": None,
            "child_only_family_pct": None,
            "adult_noncitizen_pct": num(a_d[g][ad_cit[1]]), "child_noncitizen_pct": num(a_d[g][ch_cit[1]]),
            "source_table": f"T{f_tno};T{r_tno};T{c_tno};T{a_tno}", "source_file": src_file,
            "geography_type": "territory" if POSTAL[g] in TERRITORIES else "state",
            "recipients": rt, "recipient_hispanic_pct": num(r_d[g][ssp_race[0]]),
            "recipient_eth_unknown_pct": num(r_d[g][ssp_race[-1]]),
            "adult_cit_unknown_pct": num(a_d[g][ad_cit[2]]), "child_cit_unknown_pct": num(a_d[g][ch_cit[2]]),
            "annual_sample_cases": None, "margin_pts_50pct_95ci": None,
            "notes": ("SSP-MOE race/ethnicity is published for all recipients only (no adult/child split);"
                      " no zero-adult family table" + ("; distribution suppressed ('**')" if suppressed else "")),
        })
    # computed SSP-MOE total over reporting states (not published by ACF)
    ssp = [r for r in rows if r["program"] == "SSP-MOE"]
    tot = {k: sum(r[k] for r in ssp) for k in ("families", "adults", "children", "recipients")}

    def wmean(key, wkey):
        use = [r for r in ssp if r[key] is not None]
        w = sum(r[wkey] for r in use)
        return round(sum(r[key] * r[wkey] for r in use) / w, 2) if w else None

    rows.append({
        "fiscal_year": fy, "program": "SSP-MOE", "geography": "Reporting states (computed sum)",
        "state_postal": "", **tot,
        "adult_hispanic_pct": None, "adult_eth_unknown_pct": None, "child_hispanic_pct": None,
        "child_eth_unknown_pct": None, "child_only_family_pct": None,
        "adult_noncitizen_pct": wmean("adult_noncitizen_pct", "adults"),
        "child_noncitizen_pct": wmean("child_noncitizen_pct", "children"),
        "source_table": f"T{f_tno};T{r_tno};T{c_tno};T{a_tno}", "source_file": src_file,
        "geography_type": "computed_total",
        "recipient_hispanic_pct": wmean("recipient_hispanic_pct", "recipients"),
        "recipient_eth_unknown_pct": wmean("recipient_eth_unknown_pct", "recipients"),
        "adult_cit_unknown_pct": wmean("adult_cit_unknown_pct", "adults"),
        "child_cit_unknown_pct": wmean("child_cit_unknown_pct", "children"),
        "annual_sample_cases": None, "margin_pts_50pct_95ci": None,
        "notes": (f"COMPUTED by admin_tanf.py, not published: sum of {len(ssp)} SSP-MOE state rows; "
                  "percents are recipient-weighted means over unsuppressed rows"),
    })
    return rows


def main():
    pins_update: dict = {}
    fetch(INSTRUCTIONS, CACHE / "tanf" / Path(INSTRUCTIONS).name, is_pdf, pins_update)
    all_rows = []
    for fy, url in SOURCES.items():
        page = fetch(PAGE.format(fy=fy), CACHE / "tanf" / f"acf_fy{fy}_page.html", is_page, pins_update)
        xlsx = fetch(url, CACHE / "tanf" / Path(url).name, is_xlsx, pins_update)
        all_rows += extract_year(fy, xlsx, page)
    if pins_update:
        save_pins(pins_update)
    df = pd.DataFrame(all_rows)
    for k in ("adult", "child", "recipient"):
        h, u = df[f"{k}_hispanic_pct"], df[f"{k}_eth_unknown_pct"]
        df[f"{k}_hispanic_share_known"] = (h / (100 - u)).round(4)
    for c in ("families", "adults", "children", "recipients"):
        df[c] = df[c].round(1)
    OUT.parent.mkdir(exist_ok=True)
    df.to_csv(OUT, index=False, lineterminator="\n")
    (CACHE / "tanf" / "admin_tanf_gates.log").write_text("\n".join(GATE_LOG) + "\n")
    npass = sum(g.startswith("PASS") for g in GATE_LOG)
    print(f"{npass} gates passed; wrote {OUT.relative_to(LANE)} ({len(df)} rows)")
    show = df[(df.program == "TANF") & df.state_postal.isin(["US", "CA", "TX", "AZ", "NM", "NV"])]
    print(show[["fiscal_year", "state_postal", "families", "adults", "children", "adult_hispanic_pct",
                "adult_eth_unknown_pct", "child_hispanic_pct", "child_eth_unknown_pct",
                "adult_noncitizen_pct", "child_noncitizen_pct", "child_only_family_pct",
                "margin_pts_50pct_95ci"]].to_string(index=False))


if __name__ == "__main__":
    main()
