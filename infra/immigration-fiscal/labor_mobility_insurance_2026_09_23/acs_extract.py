"""Extract compact ACS 1-year person records, ages 18-64, and national mobility rates by nativity.

Reads the local ACS PUMS person zips read-only (sources/immigration-fiscal/data/external/...; the
2023 file, absent there, is downloaded into this lane's _cache/acs_raw/). Writes one Parquet per
year to _cache/acs/ (microdata stay in the ignored cache) and the national one-year mobility rates
with successive-difference replicate SEs to derived/mobility_national.csv.

Groups (Cadena-Kovak's sample: ages 18-64, not enrolled in school, not in group quarters):
  mex_fb  born in Mexico (POBP 303)
  mex_nb  US-born of Mexican origin (NATIVITY 1, HISP 02)
  oth_nb  other natives (NATIVITY 1, HISP not 02)
  oth_fb  other foreign-born
Low education = high school or less (SCHL <= 09 in 2005-2007 coding, <= 17 from 2008).

Usage, from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/labor_mobility_insurance_2026_09_23/acs_extract.py [years...]
"""
import sys
import zipfile
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.csv as pacsv

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EXT = REPO / "sources" / "immigration-fiscal" / "data" / "external"
CACHE = HERE / "_cache" / "acs"
DERIVED = HERE / "derived"

ALL_YEARS = [2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018,
             2019, 2021, 2022, 2023, 2024]
GROUPS = ["mex_fb", "mex_nb", "oth_nb", "oth_fb"]
MEASURES = ["moved_abroad", "moved_interstate", "moved_within_state", "moved_any",
            "long_distance"]


def zip_path(year: int) -> Path:
    if year == 2019:
        return EXT / "acs_pums_2019_1yr" / "csv_pus.zip"
    if year == 2024:
        return EXT / "acs_pums_2024_1yr" / "csv_pus.zip"
    if year == 2023:
        return HERE / "_cache" / "acs_raw" / "csv_pus_2023.zip"
    return EXT / "acs_pums_years" / f"csv_pus_{year}.zip"


WANT = ["SERIALNO", "ST", "STATE", "PUMA", "ADJINC", "ADJUST", "PWGTP", "AGEP", "SEX", "SCH",
        "SCHL", "ESR", "MIG", "MIGSP", "MIGPUMA", "POBP", "NATIVITY", "HISP", "YOEP", "NAICSP",
        "WAGP", "WKHP", "REL", "RELP", "RELSHIPP", "CIT"]
STRINGS = {"SERIALNO", "PUMA", "MIGPUMA", "NAICSP"}


def sector(naicsp: pd.Series) -> pd.Series:
    """NAICS sector from the PUMS NAICSP recode (first two characters, M codes folded)."""
    s = naicsp.fillna("").str.strip()
    two = s.str[:2]
    out = two.copy()
    out[two.isin(["31", "32", "33", "3M"])] = "31-33"
    out[two.isin(["44", "45", "4M"])] = "44-45"
    out[two.isin(["48", "49"])] = "48-49"
    out[s.str.startswith("9281")] = "MIL"  # armed forces
    out[s == ""] = ""
    return out


def read_year(year: int) -> tuple[pd.DataFrame, np.ndarray]:
    zp = zip_path(year)
    zf = zipfile.ZipFile(zp)
    members = sorted(n for n in zf.namelist() if n.lower().endswith(".csv"))
    frames, reps = [], []
    for m in members:
        with zf.open(m) as fh:
            header = fh.readline().decode().strip().split(",")
        rep_cols = [c for c in header if c.lower().startswith("pwgtp") and c[5:].isdigit()]
        cols = [c for c in header if c in WANT]
        types = {c: (pa.string() if c in STRINGS else pa.float64()) for c in cols}
        types.update({c: pa.float32() for c in rep_cols})
        with zf.open(m) as fh:
            # some vintages (2014) write blank fields as a single space
            t = pacsv.read_csv(fh, convert_options=pacsv.ConvertOptions(
                include_columns=cols + rep_cols, column_types=types,
                null_values=["", " "], strings_can_be_null=True))
        agep = t.column("AGEP").to_numpy(zero_copy_only=False)
        keep = (agep >= 18) & (agep <= 64)
        t = t.filter(pa.array(keep))
        df = t.select(cols).to_pandas()
        frames.append(df)
        reps.append(np.column_stack([t.column(c).to_numpy(zero_copy_only=False)
                                     for c in sorted(rep_cols, key=lambda c: int(c[5:]))]))
    df = pd.concat(frames, ignore_index=True)
    rep = np.vstack(reps).astype(np.float64)
    if rep.shape[1] != 80:
        raise SystemExit(f"[FAILED] {year}: {rep.shape[1]} replicate weights, expected 80")
    return df, rep


def build(year: int) -> pd.DataFrame:
    df, rep = read_year(year)
    st = df["ST"] if "ST" in df else df["STATE"]
    adj = df["ADJINC"] if "ADJINC" in df else df["ADJUST"]
    rel = next(df[c] for c in ("RELSHIPP", "RELP", "REL") if c in df)
    gq = rel.isin([37, 38]) if "RELSHIPP" in df else rel.isin([16, 17])
    lowed = df["SCHL"] <= (9 if year <= 2007 else 17)
    group = np.select(
        [df["POBP"] == 303, (df["NATIVITY"] == 1) & (df["HISP"] == 2), df["NATIVITY"] == 1],
        ["mex_fb", "mex_nb", "oth_nb"], default="oth_fb")
    mig, migsp = df["MIG"], df["MIGSP"]
    out = pd.DataFrame({
        "year": year, "st": st.astype("int16"), "puma": df["PUMA"].str.zfill(5),
        "serialno": df["SERIALNO"], "pwgtp": df["PWGTP"].astype("float32"),
        "agep": df["AGEP"].astype("int16"), "sex": df["SEX"].astype("int8"),
        "lowed": lowed.astype(bool), "group": group, "hisp": df["HISP"].astype("int16"),
        "employed": df["ESR"].isin([1, 2, 4, 5]), "inlf": df["ESR"].isin([1, 2, 3, 4, 5]),
        "gq": gq.astype(bool), "inschool": df["SCH"].isin([2, 3]),
        "mig": mig.fillna(0).astype("int8"), "migsp": migsp.fillna(0).astype("int16"),
        "migpuma": df["MIGPUMA"].fillna("").str.zfill(5), "yoep": df["YOEP"].fillna(0).astype("int16"),
        "sector": sector(df["NAICSP"]), "wage_real": (df["WAGP"].fillna(0) * adj / 1e6).astype("float32"),
        "wkhp": df["WKHP"].fillna(0).astype("int16"),
    })
    out["moved_abroad"] = out["mig"] == 2
    out["moved_interstate"] = (out["mig"] == 3) & (out["migsp"] >= 1) & (out["migsp"] <= 56) \
        & (out["migsp"] != out["st"])
    out["moved_within_state"] = (out["mig"] == 3) & (out["migsp"] == out["st"])
    out["moved_any"] = out["mig"].isin([2, 3])
    out["long_distance"] = out["moved_abroad"] | out["moved_interstate"]
    CACHE.mkdir(parents=True, exist_ok=True)
    out.to_parquet(CACHE / f"p{year}.parquet", index=False)
    return national_rates(year, out, rep)


def national_rates(year: int, d: pd.DataFrame, rep: np.ndarray) -> pd.DataFrame:
    """Rates in Cadena-Kovak's sample with successive-difference replicate SEs (80 replicates)."""
    s = (~d["gq"].to_numpy()) & (~d["inschool"].to_numpy())
    rows = []
    cells = [("all", None, None)] + [(g, None, None) for g in GROUPS] \
        + [(g, e, None) for g in GROUPS for e in (True, False)] \
        + [(g, e, x) for g in GROUPS for e in (True, False) for x in (1, 2)]
    w0 = d["pwgtp"].to_numpy(np.float64)
    group, lowed, sex = d["group"].to_numpy(), d["lowed"].to_numpy(), d["sex"].to_numpy()
    ys = {meas: d[meas].to_numpy(np.float64) for meas in MEASURES}
    repT = np.ascontiguousarray(rep.T)
    ests = {}
    for g, e, x in cells:
        m = s.copy()
        if g != "all":
            m &= group == g
        if e is not None:
            m &= lowed == e
        if x is not None:
            m &= sex == x
        mv = m.astype(np.float64)
        base0, baser = w0 @ mv, repT @ mv
        for meas in MEASURES:
            yv = mv * ys[meas]
            num0, numr = w0 @ yv, repT @ yv
            r0, rr = num0 / base0, numr / baser
            se = float(np.sqrt(4 / 80 * ((rr - r0) ** 2).sum()))
            ests[(g, e, x, meas)] = (r0, rr)
            rows.append({"year": year, "group": g, "lowed": "all" if e is None else ("hs_or_less" if e else "some_college_plus"),
                         "sex": "all" if x is None else ("men" if x == 1 else "women"), "measure": meas,
                         "rate": r0, "se": se, "n": int(m.sum()), "pop": base0})
    # differences against other natives, same cell, with replicate SEs
    for (g, e, x, meas), (r0, rr) in list(ests.items()):
        if g in ("mex_fb", "mex_nb", "oth_fb"):
            b0, br = ests[("oth_nb", e, x, meas)]
            rows.append({"year": year, "group": f"{g}_minus_oth_nb",
                         "lowed": "all" if e is None else ("hs_or_less" if e else "some_college_plus"),
                         "sex": "all" if x is None else ("men" if x == 1 else "women"), "measure": meas,
                         "rate": r0 - b0, "se": float(np.sqrt(4 / 80 * (((rr - br) - (r0 - b0)) ** 2).sum())),
                         "n": 0, "pop": np.nan})
    return pd.DataFrame(rows)


def main() -> None:
    years = [int(a) for a in sys.argv[1:]] or ALL_YEARS
    missing = [y for y in years if not zip_path(y).exists()]
    if missing:
        raise SystemExit(f"[BLOCKED] missing PUMS zips for {missing}")
    DERIVED.mkdir(exist_ok=True)
    with ProcessPoolExecutor(max_workers=3) as ex:
        parts = list(ex.map(build, years))
    new = pd.concat(parts, ignore_index=True)
    path = DERIVED / "mobility_national.csv"
    if path.exists():
        old = pd.read_csv(path)
        new = pd.concat([old[~old["year"].isin(years)], new], ignore_index=True)
    new.sort_values(["year", "group", "lowed", "sex", "measure"]).to_csv(path, index=False)
    print(f"wrote {path} ({len(new)} rows) for years {years}")


if __name__ == "__main__":
    main()
