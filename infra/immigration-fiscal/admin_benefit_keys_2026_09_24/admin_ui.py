"""DOL ETA 203 "Characteristics of the Insured Unemployed": Hispanic share of UI claimants, 2024.

Source: https://oui.doleta.gov/unemploy/csv/ar203.csv (one row per state and report month). The
column map is the ETA data map (ET Handbook 402 data map, table ar203, PDF p. 5): c1 sample or
population flag, c2/c3/c4 male/female/sex not available, c40/c41/c42 Hispanic or Latino / not
Hispanic or Latino / ethnicity not available, c43-c48 race. Counts are claimants in the report
week of each month.

State weights in dollars: ETA 5159 "Claims and Payment Activities"
(https://oui.doleta.gov/unemploy/csv/ar5159.csv; data map table ar5159, PDF p. 58), item 302,
column 14 (c45): amount compensated, all weeks, state UI program. ETA 203 has no dollars, so the
Hispanic share within a state stays a claimant share.

Gates: the ethnicity columns and the sex columns add to the same total in every 2024 row used, and
all 50 states plus DC report every month of 2024 on both reports.

Writes derived/admin_ui_eta203.csv: calendar-2024 sums of the twelve monthly counts, nationally
and by state, with the Hispanic share of all claimants and of claimants with known ethnicity, and
the state's 2024 state-UI benefits paid (benefits_paid_bn).
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_ui.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/ui"
URL = "https://oui.doleta.gov/unemploy/csv/ar203.csv"
URL_5159 = "https://oui.doleta.gov/unemploy/csv/ar5159.csv"
MAP_URL = "https://oui.doleta.gov/dmstree/handbooks/402/402_4/4024c6/4024c6.pdf"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH "
             "NJ NM NY NC ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY".split())


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    pins_path = CACHE / "SOURCE_PINS.json"
    pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    for name, url in [("ar203.csv", URL), ("ar5159.csv", URL_5159), ("eta_datamap_4024c6.pdf", MAP_URL)]:
        path = CACHE / name
        if not path.exists():
            subprocess.run(["curl", "-sS", "--fail", "-L", "-m", "300", "-A", UA, "-o", str(path), url], check=True)
        digest = sha(path)
        if name in pins and pins[name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {name} changed since it was pinned")
        pins.setdefault(name, {"url": url, "retrieved": "2026-09-24", "sha256": digest})
    pins_path.write_text(json.dumps(pins, indent=1) + "\n")
    text = subprocess.run(["pdftotext", "-layout", str(CACHE / "eta_datamap_4024c6.pdf"), "-"],
                          capture_output=True, text=True, check=True).stdout
    block = text[text.index("TABLE ar203"):][:2500]
    for token in ("CHARACTERISTICS OF THE INSURED UNEMPLOYED", "Hispanic", "c40", "c41", "c42", "INA"):
        if token not in block:
            raise SystemExit(f"[GATE FAIL] data map no longer shows {token} in table ar203")
    block = text[text.index("TABLE ar5159"):][:6000]
    for token in ("ETA 5159 - CLAIMS AND PAYMENT ACTIVITIES", "PAYMENT ACTIVITIES", "All Weeks", "Amount", "c45"):
        if token not in block:
            raise SystemExit(f"[GATE FAIL] data map no longer shows {token} in table ar5159")


def main():
    fetch()
    d = pd.read_csv(CACHE / "ar203.csv")
    d["rptdate"] = pd.to_datetime(d.rptdate)
    y = d[(d.rptdate.dt.year == 2024) & d.st.isin(STATES)].copy()
    months = y.groupby("st").rptdate.nunique()
    if set(months.index) != STATES or not months.eq(12).all():
        raise SystemExit(f"[GATE FAIL] incomplete 2024 reporting: {months[months.ne(12)].to_dict()}")
    eth = y[["c40", "c41", "c42"]].sum(axis=1)
    sex = y[["c2", "c3", "c4"]].sum(axis=1)
    bad = y[eth.ne(sex)]
    if len(bad):
        raise SystemExit(f"[GATE FAIL] ethnicity and sex totals differ in {len(bad)} rows")
    g = y.groupby("st")[["c40", "c41", "c42"]].sum()
    g.loc["US"] = g.sum()
    g = g.rename(columns={"c40": "hispanic", "c41": "not_hispanic", "c42": "ethnicity_na"})
    g["total"] = g.sum(axis=1)
    g["hisp_share_all"] = g.hispanic / g.total
    g["hisp_share_known"] = g.hispanic / (g.hispanic + g.not_hispanic)
    g["na_share"] = g.ethnicity_na / g.total
    p = pd.read_csv(CACHE / "ar5159.csv", usecols=["st", "rptdate", "c45"])
    p["rptdate"] = pd.to_datetime(p.rptdate)
    p = p[(p.rptdate.dt.year == 2024) & p.st.isin(STATES)]
    pm = p.groupby("st").rptdate.nunique()
    if set(pm.index) != STATES or not pm.eq(12).all() or p.c45.isna().any() or (p.c45 < 0).any():
        raise SystemExit("[GATE FAIL] ETA 5159: incomplete or negative 2024 state UI amounts")
    paid = p.groupby("st").c45.sum() / 1e9
    paid.loc["US"] = paid.sum()
    g["benefits_paid_bn"] = paid.reindex(g.index)
    samples = y.groupby("st").c1.agg(lambda s: "".join(sorted(set(s.astype(str)))))
    g["c1_sample_or_population"] = samples.reindex(g.index).fillna("all")
    g.index.name = "geography"
    g.reset_index().to_csv(HERE / "derived/admin_ui_eta203.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 200)
    print(g.loc[["US", "TX", "CA", "AZ", "NM", "NV", "FL", "NY", "IL"]].round(4).to_string())
    print(f"[gate] 51 jurisdictions x 12 months of 2024; ethnicity totals equal sex totals in all {len(y)} rows; "
          f"ETA 5159 state UI paid ${paid.loc['US']:.2f}bn in 2024 (50 states + DC)")


if __name__ == "__main__":
    main()
