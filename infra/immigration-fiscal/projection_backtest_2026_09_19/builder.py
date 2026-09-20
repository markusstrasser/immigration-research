#!/usr/bin/env python3
"""Run historical assumption checks and labeled period-profile sensitivities."""

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import argparse
import hashlib
import json
import re
import shutil
import urllib.request
from html.parser import HTMLParser
from pathlib import Path
import openpyxl
import pandas as pd
import cohorts
import sensitivities

HERE=Path(__file__).resolve().parent
URLS={"nrc1997-ch7.html":"https://www.nationalacademies.org/read/5779/chapter/9",
      "omb-hist07z1.xlsx":"https://www.whitehouse.gov/wp-content/uploads/2026/04/hist07z1_fy2027.xlsx"}


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f,"sha256").hexdigest()


class TextParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.chunks=[]
    def handle_data(self,data):
        self.chunks.append(data)


def historical_budget(out):
    parser=TextParser(); parser.feed((out/"nrc1997-ch7.html").read_text())
    text=re.sub(r"\s+"," "," ".join(parser.chunks))
    required=["starting in 2016, the debt/GDP ratio is frozen", "No budget adjustment", "+$80,000"]
    if not all(x in text for x in required):
        raise ValueError("Primary NRC chapter no longer contains required source anchors")
    start=text.index("TABLE 7.6")
    table=text[start:start+3000]
    if not re.search(r"No budget adjustment\s+-25,000\s+\+10,000\s+-15,000",table):
        raise ValueError("NRC no-adjustment table row changed or failed extraction")
    nrc=pd.DataFrame([dict(scenario="baseline_adjust_2016",state_local=-25000,federal=105000,total=80000),
                      dict(scenario="no_budget_adjustment",state_local=-25000,federal=10000,total=-15000)])
    nrc["unit"]="1996_USD_NPV_per_immigrant_and_descendants_all_origins_original_model"
    assert (nrc.state_local+nrc.federal==nrc.total).all()
    nrc.to_csv(out/"nrc_published_scenarios.csv",index=False)
    w=openpyxl.load_workbook(out/"omb-hist07z1.xlsx",data_only=True,read_only=True)
    rows=list(w.active.values)
    if "Table 7.1" not in str(rows[0][0]) or "Held by the Public" not in str(rows[2][3]):
        raise ValueError("OMB table/header anchor failed")
    debt=[]
    for row in rows[4:]:
        if str(row[0]).strip() in {str(y) for y in range(2016,2025)}:
            debt.append(dict(fiscal_year=int(row[0]),public_debt_million=row[3],public_debt_percent_gdp=row[8],gross_debt_percent_gdp=row[6]))
    debt=pd.DataFrame(debt).sort_values("fiscal_year")
    if debt.fiscal_year.tolist()!=list(range(2016,2025)):
        raise ValueError("OMB debt history missing actual year")
    debt["frozen_2016_public_ratio"]=debt.public_debt_percent_gdp.iloc[0]
    debt["departure_pp"]=debt.public_debt_percent_gdp-debt.frozen_2016_public_ratio
    debt.to_csv(out/"nrc_budget_assumption_backtest.csv",index=False)


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source-root",type=Path,default=HERE.parents[2])
    p.add_argument("--microdata-db",type=Path,default=_data_paths.microdata_duckdb_path(require_exists=False))
    p.add_argument("--out",type=Path,default=HERE/"derived")
    p.add_argument("--fetch",action="store_true")
    p.add_argument("--source-cache",type=Path)
    a=p.parse_args(); a.out.mkdir(parents=True,exist_ok=True)
    for filename,url in URLS.items():
        dest=a.out/filename
        if a.source_cache and (a.source_cache/filename).resolve()!=dest.resolve():
            shutil.copyfile(a.source_cache/filename,dest)
        elif a.fetch:
            with urllib.request.urlopen(url,timeout=60) as r:
                dest.write_bytes(r.read())
        if not dest.exists():
            raise FileNotFoundError(f"Run --fetch or provide --source-cache for {url}")
    historical_budget(a.out)
    print("[check] NRC budget assumption and published scenario rows",flush=True)
    sources=cohorts.gss_check(a.source_root,a.out)
    print("[check] GSS disjoint birth-cohort education predictions",flush=True)
    sources+=cohorts.ipums_check(a.microdata_db,a.out)
    print("[check] IPUMS fixed birth-and-entry cohorts",flush=True)
    audit=sensitivities.run(a.source_root,a.out)
    paths=sources+[Path(x) for x in audit["input_paths"]]
    manifest=dict(date="2026-09-19",source_root=str(a.source_root),price_year=2024,
                  scope="Partial fiscal period-profile sensitivities; no causal admission effect or complete lifetime validation",
                  external_sources={str(a.out/f):dict(url=u,sha256=sha(a.out/f)) for f,u in URLS.items()},
                  raw_and_derived_inputs={str(x):sha(x) for x in paths},audit=audit,
                  implementation={str(x.name):sha(x) for x in HERE.glob("*.py")},
                  outputs={str(x.name):sha(x) for x in a.out.glob("*.csv")})
    (a.out/"manifest.json").write_text(json.dumps(manifest,indent=2)+"\n")
    print(json.dumps(dict(outputs=len(manifest["outputs"]),canonical_errors=audit["reproduced_group_max_abs_dollar_errors"])),flush=True)


if __name__=="__main__":
    main()
