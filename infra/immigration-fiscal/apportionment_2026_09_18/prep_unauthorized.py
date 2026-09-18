"""Parse Pew (1990-2023) and CMS (2010-2019) unauthorized-population-by-state tables into tidy CSVs."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DERIVED.mkdir(exist_ok=True)

DROP = {"U.S. total", "District of Columbia", "Puerto Rico", "Total", "U.S. Total"}


def clean_val(v):
    """Pew censors small cells as '<5,000' / '<10,000'; take the stated ceiling's midpoint-free
    conservative reading: use the threshold itself (e.g. '<5,000' -> 2500 midpoint 0..5000)."""
    if isinstance(v, str):
        s = v.strip().replace(",", "")
        if s.startswith("<"):
            return float(s[1:]) / 2.0  # midpoint of (0, threshold)
        if s in ("", "-", "NA"):
            return float("nan")
        return float(s)
    return float(v)


def pew():
    d = pd.read_excel(CACHE / "pew_state_trends.xlsx", sheet_name="States 1990-2023", header=None)
    hdr = d.index[d[1].astype(str).str.strip() == "State"][0]
    years = {}
    for col in range(2, 25):
        lab = str(d.iat[hdr, col]).strip()
        if lab.startswith("'"):
            yy = int(lab[1:])
            years[col] = 1900 + yy if yy >= 30 else 2000 + yy
    moe_cols = {}
    for col in range(26, 48):
        lab = str(d.iat[hdr, col]).strip()
        if lab.startswith("'"):
            yy = int(lab[1:])
            moe_cols[col] = 1900 + yy if yy >= 30 else 2000 + yy
    moe_by_year = {yr: col for col, yr in moe_cols.items()}
    rows = []
    for i in range(hdr + 1, len(d)):
        name = d.iat[i, 1]
        if not isinstance(name, str) or not name.strip() or name.strip() not in STATE50:
            continue
        for col, yr in years.items():
            mcol = moe_by_year.get(yr)
            rows.append({"state_name": name.strip(), "year": yr,
                         "unauth_pew": clean_val(d.iat[i, col]),
                         "moe90_pew": clean_val(d.iat[i, mcol]) if mcol else float("nan")})
    out = pd.DataFrame(rows)
    out = out[out["state_name"].isin(STATE50)]
    assert out["state_name"].nunique() == 50, out["state_name"].nunique()
    out.to_csv(DERIVED / "unauthorized_pew_by_state.csv", index=False)
    return out


def cms():
    d = pd.read_excel(CACHE / "cms_undoc_state_2010_2019.xlsx", sheet_name="Data", header=None)
    hdr = d.index[d[0].astype(str).str.strip() == "State"][0]
    b = d.loc[hdr + 1:, [0, 1, 2]].copy()
    b.columns = ["state_name", "year", "unauth_cms"]
    b = b.dropna(subset=["state_name"])
    b["state_name"] = b["state_name"].astype(str).str.strip()
    b = b[b["state_name"].isin(STATE50)]
    b["year"] = b["year"].astype(int)
    b["unauth_cms"] = b["unauth_cms"].map(clean_val)
    assert b["state_name"].nunique() == 50, b["state_name"].nunique()
    b.to_csv(DERIVED / "unauthorized_cms_by_state.csv", index=False)
    return b


STATE50 = {
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming",
}

if __name__ == "__main__":
    p = pew()
    c = cms()
    for yr in (2010, 2019, 2021, 2023):
        sub = p[p.year == yr]
        if len(sub):
            print(f"Pew {yr}: 50-state sum {sub.unauth_pew.sum():,.0f}")
    for yr in (2010, 2019):
        sub = c[c.year == yr]
        print(f"CMS {yr}: 50-state sum {sub.unauth_cms.sum():,.0f}")
