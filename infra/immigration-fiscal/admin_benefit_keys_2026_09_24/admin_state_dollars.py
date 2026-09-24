"""Administrative dollars by state for the programmes whose ethnicity tables count people.

The WIC and TANF characteristics reports give each state's Hispanic share of participants or
recipients, and ETA 203 gives claimant counts; the account's keys are dollars. These state dollar
totals weight the states the way the dollars fall (UI benefits paid come from ETA 5159 in
admin_ui.py).

- TANF: ACF, "TANF and MOE Financial Data, FY 2024" (page
  https://www.acf.hhs.gov/ofa/data/tanf-financial-data-fy-2024), Table B "Total Federal TANF and
  State MOE Expenditures", column 6.a "Basic Assistance (excluding Relative Foster Care
  Maintenance Payments and Adoption/Guardianship Subsidies)", all funds (federal TANF plus state
  MOE in TANF and in separate state programmes).
  Gates: the 51 state rows add to the U.S. TOTAL row and to Table A.1's all-funds figure.
- WIC: FNS, "WIC Program: State Agency Data, FY 2024" (wicagencies2024ytd-9.xlsx, sheet "Food
  Costs", column "Cumulative Cost", October 2023 to September 2024). Indian Tribal Organizations
  are assigned to the state in their name; territories are dropped.
  Gates: agency rows add to the regional rows and the regional rows to the TOTAL row.
Also pins the FNS national monthly WIC workbook (37wic-monthly-9.xlsx) that compare.py reads.

Writes derived/admin_state_dollars.csv. Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy --with openpyxl python3 \
      infra/immigration-fiscal/admin_benefit_keys_2026_09_24/admin_state_dollars.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import warnings
from pathlib import Path

import pandas as pd

warnings.filterwarnings("ignore", message="Cannot parse header or footer")
HERE = Path(__file__).resolve().parent
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
FNS = "https://www.fns.usda.gov/sites/default/files/resource-files/"
SOURCES = {
    "tanf_fin/fy-2024-tanf-moe-financial-data.xlsx":
        "https://acf.gov/sites/default/files/documents/ofa/fy-2024-tanf-moe-financial-data.xlsx",
    "wic_cost/wicagencies2024ytd-9.xlsx": FNS + "wicagencies2024ytd-9.xlsx",
    "wic_cost/37wic-monthly-9.xlsx": FNS + "37wic-monthly-9.xlsx",
}
ABBR = {"Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
        "Connecticut": "CT", "Delaware": "DE", "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA",
        "Hawaii": "HI", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
        "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA",
        "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
        "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
        "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
        "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD",
        "Tennessee": "TN", "Texas": "TX", "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY"}
TERRITORIES = {"Puerto Rico", "Virgin Islands", "Guam", "American Samoa", "Northern Marianas"}


def sha(path: Path) -> str:
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def fetch():
    for rel, url in SOURCES.items():
        path = HERE / "_cache" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        pins_path = path.parent / "SOURCE_PINS.json"
        pins = json.loads(pins_path.read_text()) if pins_path.exists() else {}
        if not path.exists():
            subprocess.run(["curl", "-sS", "--fail", "-L", "-m", "300", "-A", UA, "-o", str(path), url], check=True)
        digest = sha(path)
        if path.name in pins and pins[path.name]["sha256"] != digest:
            raise SystemExit(f"[BLOCKED] {path.name} changed since it was pinned")
        pins.setdefault(path.name, {"url": url, "retrieved": "2026-09-24", "sha256": digest})
        pins_path.write_text(json.dumps(pins, indent=1) + "\n")


def tanf():
    book = HERE / "_cache/tanf_fin/fy-2024-tanf-moe-financial-data.xlsx"
    b = pd.read_excel(book, "B. Total Expenditures", header=None)
    head = [str(x).strip() for x in b.iloc[1]]
    col = [j for j, x in enumerate(head) if x.startswith("6.a. Basic Assistance")]
    if len(col) != 1 or not str(b.iloc[0, 1]).startswith("B.: Total Federal TANF and State MOE Expenditures"):
        raise SystemExit("[GATE FAIL] TANF Table B layout changed")
    names = b.iloc[:, 0].astype("string").str.strip()
    total = float(b.loc[(names == "U.S. TOTAL").fillna(False), col[0]].iloc[0])
    rows = b[(names.notna() & ~names.isin(["STATE", "U.S. TOTAL"])).to_numpy(bool)]
    states = rows.iloc[:, 0].astype(str).str.strip().str.title().replace({"Dist.Of Columbia": "District of Columbia"})
    s = pd.Series(pd.to_numeric(rows.iloc[:, col[0]]).to_numpy(float), index=states.map(ABBR).to_numpy())
    if s.index.isna().any() or len(s) != 51:
        raise SystemExit(f"[GATE FAIL] TANF Table B states: {list(states[states.map(ABBR).isna()])}")
    a1 = pd.read_excel(book, "A.1 Fed & State by Category", header=None)
    lab = a1.iloc[:, 0].astype(str).str.strip()
    a1_total = float(a1.loc[lab.str.startswith("Basic Assistance (excluding Relative"), 3].iloc[0])
    if abs(s.sum() - total) > 1 or abs(total - a1_total) > 1:
        raise SystemExit(f"[GATE FAIL] TANF basic assistance: states {s.sum():,.0f}, U.S. {total:,.0f}, A.1 {a1_total:,.0f}")
    return s, f"[gate] TANF basic assistance FY2024: 51 states ${s.sum() / 1e9:.3f}bn = U.S. TOTAL = Table A.1"


def wic():
    f = pd.read_excel(HERE / "_cache/wic_cost/wicagencies2024ytd-9.xlsx", "Food Costs", header=None)
    if str(f.iloc[0, 0]).strip() != "WIC PROGRAM -- FOOD COSTS" or str(f.iloc[1, 0]).strip() != "FISCAL YEAR 2024" \
            or str(f.iloc[4, 13]).strip() != "Cumulative Cost":
        raise SystemExit("[GATE FAIL] WIC food cost sheet layout changed")
    lab = f.iloc[:, 0].astype(str).str.strip()
    val = pd.to_numeric(f.iloc[:, 13], errors="coerce")
    region = lab.str.endswith("Region") | lab.eq("Mountain Plains")
    total = float(val[lab == "TOTAL"].iloc[0])
    agency = val.notna() & ~region & lab.ne("TOTAL")
    # The Northeast Region row exceeds its listed agencies by $31,443 (0.0006% of the total); the
    # other six regions add exactly.
    gap = total - val[agency].sum()
    if not 0 <= gap < 1e-4 * total or abs(val[region].sum() - total) > 1 or region.sum() != 7:
        raise SystemExit(f"[GATE FAIL] WIC agency rows do not add to regions and TOTAL (gap {gap:,.0f})")
    state = lab.map(ABBR)
    ito = lab.str.extract(r",\s*([A-Z]{2})$")[0]
    state = state.fillna(ito)
    unmapped = agency & state.isna() & ~lab.isin(TERRITORIES)
    if unmapped.any():
        raise SystemExit(f"[GATE FAIL] WIC agencies without a state: {list(lab[unmapped])}")
    keep = agency & state.notna()
    s = val[keep].groupby(state[keep]).sum()
    if len(s) != 51:
        raise SystemExit(f"[GATE FAIL] WIC food costs cover {len(s)} states")
    return s, (f"[gate] WIC food costs FY2024: regions = TOTAL ${total / 1e9:.3f}bn, agencies short by ${gap:,.0f}; "
               f"50 states + DC (tribal agencies included) ${s.sum() / 1e9:.3f}bn")


def main():
    fetch()
    t, t_msg = tanf()
    w, w_msg = wic()
    out = pd.concat([
        pd.DataFrame(dict(programme="tanf", state=t.index, dollars_bn=t.to_numpy() / 1e9, year="FY2024",
                          source="ACF TANF and MOE Financial Data FY2024, Table B, col. 6.a basic assistance, all funds")),
        pd.DataFrame(dict(programme="wic", state=w.index, dollars_bn=w.to_numpy() / 1e9, year="FY2024",
                          source="FNS WIC State Agency Data FY2024, Food Costs, cumulative")),
    ])
    out.to_csv(HERE / "derived/admin_state_dollars.csv", index=False, lineterminator="\n")
    for prog, s in [("tanf", t), ("wic", w)]:
        share = (s / s.sum()).reindex(["CA", "TX", "AZ", "NM", "NV", "NY"]).round(4).to_dict()
        print(prog, share)
    print(t_msg)
    print(w_msg)


if __name__ == "__main__":
    main()
