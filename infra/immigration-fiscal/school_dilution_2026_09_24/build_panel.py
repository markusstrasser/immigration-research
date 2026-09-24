"""District-year F-33 finance panel, FY2000-FY2024, split by function.

Reads the Census Annual Survey of School System Finances all-items files fetched by acquire.py.
Money is reported in thousands of dollars; this panel stores dollars. Function groups (F-33 item codes
from the FY2015 technical documentation, `_cache/f33/school15doc.pdf`, "All Data Items"):

  instruction         TCURINST = E13 + J13 + J12 + J14
  pupil_support       E17 + J17
  instr_staff         E07 + J07 (curriculum, training, libraries)
  gen_admin           E08 + J08
  school_admin        E09 + J09
  business            V90 + J90 (business, central and other support services)
  om                  V40 + J40 (operation and maintenance of plant)
  transport           V45 + J45
  support_other       V85 + J11 + J96 (nonspecified support; retirement transfers not split)
  other_elsec         TCUROTH = E11 + V60 + V65 + J10 + J97 (food service, enterprise, other)
  current             TCURELSC = instruction + TCURSSVC + other_elsec
  capital_outlay      TCAPOUT
  interest            I86

State FIPS comes from the NCES ID (its first two digits). Enrollment is V33, fall membership.
Writes _cache/panel.parquet (all units and years) and derived/panel_coverage.csv. The gate compares
the national current spending per pupil (systems with pupils) with Census's published Table 8 for
FY2015 and FY2019; FY2005, FY2010, FY2023 and FY2024 are reported beside them.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with pyarrow --with xlrd --with openpyxl \
      python3 infra/immigration-fiscal/school_dilution_2026_09_24/build_panel.py
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from acquire import unit_file_name  # noqa: E402

F33 = HERE / "_cache" / "f33"
OUT = HERE / "derived"
YEARS = range(2000, 2025)
MONEY = ["TOTALREV", "TFEDREV", "TSTREV", "TLOCREV", "T06", "C01", "C05", "C06", "C07", "C14", "B11", "C15", "C25",
         "C38", "C39", "TCURELSC", "TCURINST", "TCURSSVC", "TCUROTH", "E17", "J17", "E07", "J07", "E08", "J08", "E09",
         "J09", "V40", "J40", "V45", "J45", "V90", "J90", "V85", "J11", "J96", "NONELSEC", "TCAPOUT", "F12", "G15",
         "K09", "K10", "K11", "I86", "L12", "M12", "Q11", "Z33", "V10", "AE1"]
FUNCTIONS = {
    "instruction": ["TCURINST"], "pupil_support": ["E17", "J17"], "instr_staff": ["E07", "J07"],
    "gen_admin": ["E08", "J08"], "school_admin": ["E09", "J09"], "business": ["V90", "J90"], "om": ["V40", "J40"],
    "transport": ["V45", "J45"], "support_other": ["V85", "J11", "J96"], "other_elsec": ["TCUROTH"],
    "current": ["TCURELSC"], "capital_outlay": ["TCAPOUT"], "interest": ["I86"],
}
# Census Table 8, "Per Pupil Amounts for Current Spending", United States row, column "Total"
PUBLISHED_PP = {2005: ("elsec05_sttables.xls", 8701.055071), 2010: ("elsec10_sttables.xls", 10600.056589),
                2015: ("elsec15_sttables.xls", 11391.787405), 2019: ("elsec19_sumtables.xls", 13187.346733),
                2023: ("elsec23_sumtables.xlsx", 16525.876827), 2024: ("elsec24_sumtables.xlsx", 17619.389028)}


def read_year(y):
    path = F33 / unit_file_name(y)
    # Data rows carry one trailing empty field beyond the header: index_col=False keeps columns aligned.
    d = pd.read_csv(path, dtype=str, index_col=False, encoding="latin-1", keep_default_na=False)
    keep = ["STATE", "NCESID", "NAME", "SCHLEV", "YRDATA", "V33"] + [c for c in MONEY if c in d.columns]
    d = d[keep].copy()
    for c in MONEY:
        d[c] = pd.to_numeric(d[c], errors="coerce") * 1000.0 if c in d.columns else np.nan
    d["V33"] = pd.to_numeric(d.V33, errors="coerce")
    d["year"] = y
    d["NCESID"] = d.NCESID.str.strip()
    d["leaid"] = np.where(d.NCESID.str.fullmatch(r"\d{7}"), d.NCESID, "")
    d["fips"] = pd.to_numeric(d.leaid.str[:2], errors="coerce")
    return d


def published_pp(y):
    f, value = PUBLISHED_PP[y]
    t = pd.read_excel(F33 / f, sheet_name="8", header=None)
    row = [i for i in range(len(t)) if str(t.iloc[i, 0]).strip().startswith("United States")][0]
    got = float(t.iloc[row, 2])
    if abs(got - value) > 1e-3:
        raise SystemExit(f"[BLOCKED] {f} Table 8 US total reads {got}, transcribed {value}")
    return got


def cpi_fiscal_year():
    """CPI-U mean over each school fiscal year, July (t-1) to June (t)."""
    c = pd.read_csv(HERE / "_cache" / "cpiaucsl_monthly.csv", parse_dates=["observation_date"])
    c["fy"] = c.observation_date.dt.year + (c.observation_date.dt.month >= 7).astype(int)
    fy = c.groupby("fy").CPIAUCSL.agg(["mean", "size"])
    fy = fy[fy["size"] == 12]["mean"]
    return fy


def main():
    frames = [read_year(y) for y in YEARS]
    d = pd.concat(frames, ignore_index=True)
    # Census STATE codes are alphabetical, not FIPS; units without an NCES ID take their state's FIPS
    # from the units that have one. The map must be one-to-one.
    smap = d[d.leaid.ne("")].groupby("STATE").fips.agg(lambda s: s.mode().iloc[0])
    if smap.duplicated().any() or len(smap) != 51:
        raise SystemExit(f"[BLOCKED] STATE -> FIPS map is not one-to-one over 51 states: {smap.to_dict()}")
    d["fips"] = d.fips.fillna(d.STATE.map(smap))
    for name, items in FUNCTIONS.items():
        d[name] = d[items].fillna(0.0).sum(axis=1)
    d["support_total"] = d.TCURSSVC
    d["support_named"] = d[["pupil_support", "instr_staff", "gen_admin", "school_admin", "business", "om",
                            "transport", "support_other"]].sum(axis=1)
    cpi = cpi_fiscal_year()
    d["defl_2024"] = cpi[2024] / d.year.map(cpi)

    # Identity checks on units with current spending: the named parts must rebuild the published totals.
    live = d[d.TCURELSC.gt(0)]
    gap_support = (live.support_named - live.TCURSSVC).abs() / live.TCURSSVC.clip(lower=1)
    gap_current = (live.instruction + live.TCURSSVC + live.other_elsec - live.TCURELSC).abs() / live.TCURELSC
    checks = {"support_parts_max_rel_gap": float(gap_support.max()),
              "support_parts_share_rows_gap_over_0.1pct": float((gap_support > 1e-3).mean()),
              "current_parts_max_rel_gap": float(gap_current.max()),
              "current_parts_share_rows_gap_over_0.1pct": float((gap_current > 1e-3).mean())}

    cov, gate = [], []
    for y, g in d.groupby("year"):
        regular = g[g.SCHLEV.isin(["01", "02", "03"]) & g.leaid.ne("") & g.V33.gt(0) & g.TCURELSC.gt(0)]
        # Table 8 divides the current spending of systems that report pupils by their pupils; spending of
        # systems with no membership (service agencies, nonoperating systems) is left out of both.
        enrolled = g[g.V33.gt(0)]
        pp_all = enrolled.TCURELSC.sum() / enrolled.V33.sum()
        cov.append({"fiscal_year": y, "rows": len(g), "rows_with_ncesid": int(g.leaid.ne("").sum()),
                    "regular_districts_with_pupils_and_spending": len(regular), "pupils_all_units": g.V33.sum(),
                    "pupils_regular": regular.V33.sum(), "current_spending_all_units_bn": g.TCURELSC.sum() / 1e9,
                    "current_pp_all_units": pp_all, "cpi_fy": cpi.get(y, np.nan)})
        if y in PUBLISHED_PP:
            pub = published_pp(y)
            gate.append({"fiscal_year": y, "computed_pp": pp_all, "published_pp": pub,
                         "rel_diff": pp_all / pub - 1, "pass_0.5pct": abs(pp_all / pub - 1) <= 0.005})
    cov, gate = pd.DataFrame(cov), pd.DataFrame(gate)
    OUT.mkdir(exist_ok=True)
    cov.to_csv(OUT / "panel_coverage.csv", index=False, lineterminator="\n", float_format="%.4f")
    gate.to_csv(OUT / "gate_national_pp.csv", index=False, lineterminator="\n", float_format="%.6f")
    (OUT / "panel_identity_checks.json").write_text(json.dumps(checks, indent=1) + "\n")
    cols = ["year", "leaid", "fips", "STATE", "NAME", "SCHLEV", "V33", "defl_2024"] + MONEY + list(FUNCTIONS) + [
        "support_total", "support_named"]
    d[cols].to_parquet(HERE / "_cache" / "panel.parquet", index=False)
    print(gate.to_string(index=False))
    print(json.dumps(checks, indent=1))
    # Hard gate on FY2015 and FY2019. Before FY2015 the file's V33 still counts pupils that Table 8 leaves
    # out (its FY2010 note: private charter schools, state facilities, federal systems), so FY2005 and
    # FY2010 sit about 1% below the published figure; derived/gate_national_pp.csv keeps those rows.
    passed = gate[gate.fiscal_year.isin([2015, 2019])]["pass_0.5pct"]
    if len(passed) != 2 or not passed.all():
        raise SystemExit("[GATE FAIL] national current spending per pupil off Census Table 8 by more than 0.5%")


if __name__ == "__main__":
    main()
