"""Does TAF under-count LTSS dollars in states where the union is concentrated?

Compares CMS-64-based LTSS spending by state for FFY2020 (Mathematica for CMS, "Medicaid LTSS
Annual Expenditures Report: FFY2020", Appendix D table D.2, which includes managed LTSS reported
by states) with T-MSIS TAF CY2020 totals from the same contractor, for institutional services and
HCBS. Then re-runs the union share with each state's 2023 TAF dollars scaled by its 2020
CMS-64/TAF ratio (California HCBS excluded: its IHSS is added separately in translate.py).
Fiscal and calendar years differ by a quarter and the CMS-64 report has known state anomalies,
so this is a test of direction, not a correction.
Writes derived/completeness_2020.csv and derived/completeness_share_test.json.
Run from the repo root after taf_tables.py, acs_factors.py and fetch_sources.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 \
      infra/immigration-fiscal/ltss_share_2026_09_23/completeness.py
"""
import hashlib
import json
from pathlib import Path

import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
DER = HERE / "derived"
APP_D = HERE / "_cache/wayback/ltssexpenditures2020-app-d.xlsx"


def money(x):
    return float(str(x).replace("$", "").replace(",", "")) if x not in (None, "n.a.", "NA") else float("nan")


def main():
    pins = json.loads((HERE / "SOURCE_PINS.json").read_text())
    if hashlib.sha256(APP_D.read_bytes()).hexdigest() != pins[APP_D.name]["sha256"]:
        raise SystemExit("[BLOCKED] appendix D changed")
    rows = list(openpyxl.load_workbook(APP_D, read_only=True, data_only=True)["D.2 - State_Summary_Tot_LTSS"].values)
    head = rows[0]
    if not (head[0] == "State" and "Total institutional" in head[1] and "Total HCBS" in head[2]):
        raise SystemExit("[BLOCKED] D.2 header changed")
    cms = pd.DataFrame([dict(state=r[0], INST=money(r[1]) / 1e9, HCBS=money(r[2]) / 1e9)
                        for r in rows[1:] if r[0] and r[1] is not None and not str(r[0]).startswith(("Total", "United", "["))])
    taf = pd.read_csv(DER / "taf_race_ethn.csv")
    t = taf[(taf.measure == "expenditures") & taf.category.isin(["INST", "HCBS"]) & taf.group.eq("hispanic")]
    t20 = t[t.year == 2020].pivot(index="state", columns="category", values="total") / 1e9
    comp = cms.set_index("state").join(t20, rsuffix="_taf2020", how="inner")
    comp.columns = ["cms64_fy2020_inst", "cms64_fy2020_hcbs", "taf2020_hcbs", "taf2020_inst"]
    comp["ratio_inst"] = comp.cms64_fy2020_inst / comp.taf2020_inst
    comp["ratio_hcbs"] = comp.cms64_fy2020_hcbs / comp.taf2020_hcbs
    comp.to_csv(DER / "completeness_2020.csv")
    pd.set_option("display.width", 200)
    print(comp.sort_values("cms64_fy2020_hcbs", ascending=False).head(15).round(2).to_string())
    print("national sums:", comp[["cms64_fy2020_inst", "taf2020_inst", "cms64_fy2020_hcbs", "taf2020_hcbs"]].sum().round(1).to_dict())

    # Direction test: 2023 TAF Hispanic and total dollars scaled by the 2020 ratio (CA HCBS held at 1).
    fs = pd.read_csv(DER / "acs_state_factors_2024.csv")
    from translate import FIPS  # noqa: E402  (same directory)
    f_all = fs[fs.population == "comm_adl"].set_index("STATE").f
    f_inst = fs[fs.population == "inst65"].set_index("STATE").f
    t23 = taf[(taf.year == 2023) & (taf.measure == "expenditures") & taf.category.isin(["INST", "HCBS"])
              & ~taf.state.eq("National")]
    out = {}
    for c, ff, rc in [("INST", f_inst, "ratio_inst"), ("HCBS", f_all, "ratio_hcbs")]:
        h = t23[(t23.category == c) & (t23.group == "hispanic")].set_index("state")
        r = comp[rc].clip(0.5, 3.0).reindex(h.index).fillna(1.0)
        if c == "HCBS":
            r.loc["California"] = 1.0
        f = h.index.map(FIPS).map(ff).fillna(ff.median()).to_numpy()
        base = (h.value * f).sum() / h.total.sum()
        scaled = (h.value * f * r).sum() / (h.total * r).sum()
        out[c] = dict(share_unscaled=float(base), share_scaled=float(scaled), ratio=float(scaled / base))
    (DER / "completeness_share_test.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
