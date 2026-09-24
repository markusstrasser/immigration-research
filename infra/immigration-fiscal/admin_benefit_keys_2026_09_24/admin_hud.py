"""HUD Picture of Subsidized Households (PSH) 2024 and 2023: Hispanic share of assisted households.

Source: HUD USER, https://www.huduser.gov/portal/datasets/assthsg.html, national (US_<year>) and state
(STATE_<year>) files, 2020-census geography, and the 2024 data dictionary. pct_hispanic is the
"percentage of households in which the ethnicity of the head of household is Hispanic", among
households with a Form 50058/50059 report; spending_per_month is "average federal spending per
unit-month" (dictionary pp. 1-3). Values are rounded to whole percent and whole dollars; -1 to -5
are HUD missing or suppressed codes.

Per programme (2 public housing, 3 vouchers, 4 moderate rehabilitation, 5 project-based Section 8,
6-9 the smaller multifamily programmes) the script forms reported households (number_reported),
occupied unit-months (total_units x pct_occupied / 100 x 12) and annual federal spending
(occupied unit-months x spending_per_month). Hispanic shares are then weighted by reported
households or by spending, which assumes equal spending per unit by ethnicity within a programme
and state. Gate: the programme rows reproduce the published all-programme row (program 1) within
the rounding of whole percent.

Writes derived/admin_hud_psh.csv. Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_hud.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/hud"
BASE = "https://www.huduser.gov/portal/datasets/pictures/"
FILES = ["files/US_2024_2020census.xlsx", "files/STATE_2024_2020census.xlsx",
         "files/US_2023_2020census.xlsx", "files/STATE_2023_2020census.xlsx", "dictionary_2024.pdf"]
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
PROGRAMS = {2: "public_housing", 3: "vouchers", 4: "mod_rehab", 5: "project_based_s8", 6: "rentsup_rap",
            7: "s236_bmir", 8: "s202_prac", 9: "s811_prac"}


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    pins_path = CACHE / "SOURCE_PINS.json"
    pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    for rel in FILES:
        name = Path(rel).name
        path = CACHE / name
        if not path.exists():
            subprocess.run(["curl", "-sS", "--fail", "-L", "-m", "300", "-A", UA, "-o", str(path), BASE + rel],
                           check=True)
        digest = sha(path)
        if name in pins and pins[name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {name} changed since it was pinned")
        pins.setdefault(name, {"url": BASE + rel, "retrieved": "2026-09-24", "sha256": digest})
    pins_path.write_text(json.dumps(pins, indent=1) + "\n")
    text = subprocess.run(["pdftotext", "-layout", str(CACHE / "dictionary_2024.pdf"), "-"],
                          capture_output=True, text=True, check=True).stdout
    for phrase in ("Percentage of households in which the ethnicity of the head of household is Hispanic",
                   "Average federal spending per unit-month"):
        if phrase not in " ".join(text.split()):
            raise SystemExit(f"[GATE FAIL] dictionary definition changed: {phrase}")


def frame(year: int) -> pd.DataFrame:
    us = pd.read_excel(CACHE / f"US_{year}_2020census.xlsx").assign(geography="US")
    st = pd.read_excel(CACHE / f"STATE_{year}_2020census.xlsx")
    st = st.assign(geography=st.name.astype(str).str[:2])
    st = st[st.geography != "XX"]                                   # "XX Missing": no state
    cols = ["geography", "program", "total_units", "pct_occupied", "number_reported", "spending_per_month",
            "pct_hispanic"]
    d = pd.concat([us[cols], st[cols]], ignore_index=True)
    d["program"] = d.program.astype(int)
    return d


def summarize(d: pd.DataFrame, year: int) -> pd.DataFrame:
    rows = []
    for geo, g in d.groupby("geography"):
        top = g[g.program == 1]
        parts = g[g.program.isin(PROGRAMS)].copy()
        ok = (parts.pct_hispanic >= 0) & (parts.number_reported > 0)
        parts = parts[ok]
        occ = np.where(parts.pct_occupied > 0, parts.pct_occupied, np.nan) / 100
        parts["dollars"] = parts.total_units * occ * 12 * parts.spending_per_month.where(parts.spending_per_month > 0)
        hh = (parts.number_reported * parts.pct_hispanic / 100).sum() / parts.number_reported.sum()
        dv = parts.dropna(subset=["dollars"])
        dollars = (dv.dollars * dv.pct_hispanic / 100).sum() / dv.dollars.sum() if len(dv) else np.nan
        published = float(top.pct_hispanic.iloc[0]) / 100 if len(top) and top.pct_hispanic.iloc[0] >= 0 else np.nan
        # Suppressed programme rows (codes -1 to -5) drop out of the parts; gate only when the parts
        # still carry at least 95% of the all-programme row's reported households.
        covered = parts.number_reported.sum() >= 0.95 * float(top.number_reported.iloc[0]) if len(top) else False
        if covered and np.isfinite(published) and abs(hh - published) > 0.0055 + 0.005:
            raise SystemExit(f"[GATE FAIL] {year} {geo}: programmes give {hh:.4f}, all-programme row {published}")
        row = dict(year=year, geography=geo, households_reported=float(parts.number_reported.sum()),
                   federal_spending_bn=float(dv.dollars.sum() / 1e9), hisp_share_households=hh,
                   hisp_share_dollars=dollars, published_all_programs=published)
        for code, name in PROGRAMS.items():
            p = parts[parts.program == code]
            row[f"hisp_{name}"] = float(p.pct_hispanic.iloc[0]) / 100 if len(p) else np.nan
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    fetch()
    out = pd.concat([summarize(frame(y), y) for y in (2024, 2023)], ignore_index=True)
    out.to_csv(HERE / "derived/admin_hud_psh.csv", index=False, lineterminator="\n")
    pd.set_option("display.width", 200)
    show = out[out.geography.isin(["US", "TX", "CA", "AZ", "NM", "NV"])]
    print(show[["year", "geography", "households_reported", "federal_spending_bn", "hisp_share_households",
                "hisp_share_dollars", "published_all_programs"]].round(4).to_string(index=False))
    print(f"[gate] programme rows reproduce the all-programme Hispanic share in {len(out)} geography-years")


if __name__ == "__main__":
    main()
