"""Read, gate and pool the MEPS full-year consolidated files 2016-2024.

One harmonized person-year frame goes to `_cache/pooled.parquet`, with the
HC-036 pooled variance structure (STRA9624/PSU9624) attached by DUPERSID+PANEL
and every payment column deflated to 2024 dollars. Nothing here estimates a
ratio; `pooled_ratios.py` and `translate.py` read the frame.

Payer harmonization. Before 2019 MEPS moved "Medicaid payments reported for
persons who were not reported to be enrolled in the Medicaid program at any time
during the year" into a separate Other Public (OPU) column, and private payments
for persons without private coverage into Other Private (OPR) [h192doc.pdf
C-111]. "Beginning in 2019, this step is removed ... The two source of payment
categories, Other Private and Other Public, are no longer available" [h216doc.pdf
C-105]. So from 2019 those dollars sit inside TOTMCD/TOTPRV. The harmonized
Medicaid column is TOTMCD + TOTOPU in 2016-2018 and TOTMCD afterwards; the
transport's verbatim public list (which never names OPU) is kept beside it.

Deflator: CPI-U Medical care, U.S. city average, not seasonally adjusted,
annual average, BLS series CUUR0000SAM (primary); CPI-U All items CUUR0000SA0 is
carried for a sensitivity. Both come from the BLS public API response pinned in
`_cache/bls_cpi_medical_allitems.json`.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/meps_pool.py
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
HELD = Path("/Users/alien/research-data/immigration-fiscal/data/external/stage3/ahrq")

YEARS = {2016: "192", 2017: "201", 2018: "209", 2019: "216", 2020: "224",
         2021: "233", 2022: "243", 2023: "251", 2024: "256"}
OPU_YEARS = {2016, 2017, 2018}
BLS_JSON = CACHE / "bls_cpi_medical_allitems.json"
HC036 = CACHE / "h36u24dat.zip"
HC036_SU = CACHE / "h36u24su.txt"

# Transport's public list, `build/meps_health_transport_2024.py::PUBLIC_PAYERS`, year-free.
PUBLIC_PAYERS = ["TOTMCR", "TOTMCD", "TOTVA", "TOTTRI", "TOTOFD", "TOTSTL"]
PAYERS_ALL = ["TOTSLF", "TOTMCR", "TOTMCD", "TOTPRV", "TOTVA", "TOTTRI", "TOTOFD", "TOTSTL",
              "TOTWCP", "TOTOSR"]
PLAIN = ["BORNUSA", "YRSINUS", "HISPANX", "HISPNCAT", "RACEV1X", "RACETHX", "VARSTR", "VARPSU"]
SUFFIXED = ["INSURC", "MCDEV", "MCREV", "UNINS", "POVCAT", "TOTEXP"] + PAYERS_ALL


def _ok(msg):
    print(f"  ✓ {msg}", flush=True)


def _warn(msg):
    print(f"  ! {msg}", flush=True)


def _header(s):
    print(f"\n[{s}]", flush=True)


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr, flush=True)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def paths_for(year: int) -> dict[str, Path]:
    hc = YEARS[year]
    base = CACHE if year < 2023 else HELD / ("meps" if year == 2023 else "meps_2024")
    return {k: base / f"h{hc}{k}" for k in ("dat.zip", "su.txt", "cb.pdf", "doc.pdf")}


def parse_sas_layout(su_path: Path) -> dict[str, tuple[int, int, bool]]:
    """`@start NAME [$]width` lines -> (0-based start, width, is_char).

    Follows `build/public_mvp_io.py::parse_meps_sas_fields`, extended to the `$`
    character formats so that DUPERSID can be read as text."""
    out: dict[str, tuple[int, int, bool]] = {}
    for line in su_path.read_text(encoding="latin-1", errors="replace").splitlines():
        m = re.match(r"\s*(?:INPUT\s+)?@(\d+)\s+(\w+)\s+(\$?)([\d.]+)", line)
        if m:
            out[m.group(2)] = (int(m.group(1)) - 1, int(float(m.group(4))), m.group(3) == "$")
    return out


def codebook_text(cb_pdf: Path) -> str:
    txt = CACHE / (cb_pdf.stem + ".txt")
    if not txt.exists():
        subprocess.run(["pdftotext", "-layout", str(cb_pdf), str(txt)], check=True)
    return txt.read_text(encoding="utf-8", errors="replace")


def codebook_frequencies(text: str, var: str) -> dict[int, tuple[str, int, int]]:
    """Frequency table of one variable from a pdftotext'd MEPS codebook.

    Two layouts occur: 2016-2019 print `VAR  DESCRIPTION ... Num start end` on
    one line; 2020-2024 print `Name: VAR` on its own line."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if re.match(rf"^\s*Name:\s+{var}\s*$", line) or \
           re.match(rf"^{var}\s+\S.*\b(?:NUM|Num)\s+\d+\s+\d+\s*$", line):
            start = i
            break
    if start is None:
        fail(f"codebook entry for {var} not found")
    table: dict[int, tuple[str, int, int]] = {}
    for line in lines[start + 1:start + 80]:
        if re.search(r"\bTOTAL\b", line, flags=re.I):
            break
        # HC-036's codebook prints unweighted counts only, so the weighted column is optional
        m = re.match(r"^\s*(-?\d+)\s+(\S.*?)\s{2,}([\d,]+)(?:\s+([\d,]+))?\s*$", line)
        if m:
            table[int(m.group(1))] = (m.group(2).strip(), int(m.group(3).replace(",", "")),
                                      int(m.group(4).replace(",", "")) if m.group(4) else None)
    if not table:
        fail(f"no frequency rows parsed for {var}")
    return table


def read_year(year: int) -> pd.DataFrame:
    yy = str(year)[2:]
    p = paths_for(year)
    layout = parse_sas_layout(p["su.txt"])
    fields = (["DUPERSID", "PANEL", f"AGE{yy}X", f"PERWT{yy}F"] + PLAIN
              + [f + yy for f in SUFFIXED]
              + ([f"TOTOPR{yy}", f"TOTOPU{yy}"] if year in OPU_YEARS else []))
    absent = [f for f in fields if f not in layout]
    if absent:
        fail(f"{year}: fields absent from {p['su.txt'].name}: {absent}")
    with zipfile.ZipFile(p["dat.zip"]) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".dat")]
        if len(names) != 1:
            fail(f"{year}: expected one .dat member, got {names}")
        raw = z.read(names[0]).decode("ascii").splitlines()
    cols = {}
    for f in fields:
        s, w, is_char = layout[f]
        vals = [line[s:s + w] for line in raw]
        cols[f] = [v.strip() for v in vals] if is_char else np.array([float(v) for v in vals])
    d = pd.DataFrame(cols)
    ren = {f"AGE{yy}X": "AGE", f"PERWT{yy}F": "PERWT"}
    ren.update({f + yy: f for f in SUFFIXED})
    ren.update({f"TOTOPR{yy}": "TOTOPR", f"TOTOPU{yy}": "TOTOPU"})
    d = d.rename(columns=ren)
    if year not in OPU_YEARS:
        d["TOTOPR"] = 0.0
        d["TOTOPU"] = 0.0
    d["year"] = year
    d["DUPERSID"] = d["DUPERSID"].astype(str)
    d["PANEL"] = d["PANEL"].astype(int)
    return d


def gate_year(d: pd.DataFrame, year: int, cb: str) -> dict:
    g = {"year": year}
    hisp = codebook_frequencies(cb, "HISPNCAT")
    n_total = sum(v[1] for v in hisp.values())
    if len(d) != n_total:
        fail(f"{year}: {len(d)} records vs codebook HISPNCAT total {n_total}")
    g["records"] = len(d)
    tab = d.groupby("HISPNCAT").agg(n=("PERWT", "size"), w=("PERWT", "sum"))
    for code, (label, n_exp, w_exp) in hisp.items():
        if code not in tab.index:
            fail(f"{year}: HISPNCAT {code} absent")
        n_got, w_got = int(tab.loc[code, "n"]), float(tab.loc[code, "w"])
        if n_got != n_exp or abs(w_got - w_exp) > 1:
            fail(f"{year}: HISPNCAT {code} {label}: {n_got}/{w_got:,.0f} vs codebook {n_exp}/{w_exp:,}")
    if set(tab.index) != set(hisp):
        fail(f"{year}: HISPNCAT codes in data {sorted(tab.index)} vs codebook {sorted(hisp)}")
    if not re.search(r"MEXICAN", hisp[1][0]):
        fail(f"{year}: HISPNCAT code 1 label is {hisp[1][0]!r}, not Mexican")
    g["hispncat"] = {str(k): {"label": v[0], "unweighted": v[1], "weighted": v[2]} for k, v in hisp.items()}
    g["mexican_label"] = hisp[1][0]

    born = codebook_frequencies(cb, "BORNUSA")
    for code, (label, n_exp, w_exp) in born.items():
        m = d.BORNUSA.eq(code)
        if int(m.sum()) != n_exp or abs(float(d.loc[m, "PERWT"].sum()) - w_exp) > 1:
            fail(f"{year}: BORNUSA {code} {label}: {int(m.sum())} vs {n_exp}")
    g["bornusa"] = {str(k): {"label": v[0], "unweighted": v[1], "weighted": v[2]} for k, v in born.items()}

    # nh_white is the codebook's own RACETHX == 2 ("NON-HISPANIC WHITE ONLY"). The 2024
    # lane's equivalent HISPANX == 2 & RACEV1X == 1 matches it exactly in 2024 but not in
    # every year (2023 differs by 3 records), so the difference is recorded, not gated.
    rt = codebook_frequencies(cb, "RACETHX")
    nhw = d.RACETHX.eq(2)
    if int(nhw.sum()) != rt[2][1] or abs(float(d.loc[nhw, "PERWT"].sum()) - rt[2][2]) > 1:
        fail(f"{year}: RACETHX==2 {int(nhw.sum())} vs codebook {rt[2][1]}")
    alt = d.HISPANX.eq(2) & d.RACEV1X.eq(1)
    g["nh_white"] = {"unweighted": rt[2][1], "weighted": rt[2][2], "label": rt[2][0],
                     "records_where_hispanx_racev1x_definition_differs": int((alt != nhw).sum())}
    if year == 2024 and int((alt != nhw).sum()) != 0:
        fail("2024: the lane's HISPANX/RACEV1X nh_white definition no longer equals RACETHX==2")

    pay = PAYERS_ALL + ["TOTOPR", "TOTOPU"]
    if (d[pay + ["TOTEXP"]] < 0).any().any():
        fail(f"{year}: negative/reserved payment value; no silent zero substitution")
    resid = (d.TOTEXP - d[pay].sum(axis=1)).abs()
    if resid.max() > 12:
        fail(f"{year}: TOTEXP differs from the sum of its payers by up to {resid.max()}")
    g["totexp_identity_max_abs_residual"] = float(resid.max())
    g["totexp_identity_records_off"] = int(resid.gt(0.5).sum())

    design = d.loc[d.PERWT.gt(0), ["VARSTR", "VARPSU"]].drop_duplicates()
    per = design.groupby("VARSTR").size()
    if (per < 2).any():
        fail(f"{year}: lonely annual PSU strata {per[per < 2].index.tolist()}")
    g["annual_design"] = {"strata": int(len(per)), "psus": int(len(design))}
    g["positive_weight"] = int(d.PERWT.gt(0).sum())
    g["population"] = float(d.PERWT.sum())
    g["mcdev_codes"] = sorted(int(x) for x in d.MCDEV.unique())
    return g


def read_hc036() -> pd.DataFrame:
    layout = parse_sas_layout(HC036_SU)
    want = ["DUPERSID", "PANEL", "STRA9624", "PSU9624"] + [f"INH{hc}" for hc in YEARS.values()]
    absent = [f for f in want if f not in layout]
    if absent:
        fail(f"HC-036 fields absent: {absent}")
    with zipfile.ZipFile(HC036) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".dat")]
        raw = z.read(names[0]).decode("ascii").splitlines()
    cols = {}
    for f in want:
        s, w, is_char = layout[f]
        vals = [line[s:s + w] for line in raw]
        cols[f] = [v.strip() for v in vals] if is_char else np.array([int(v) for v in vals])
    h = pd.DataFrame(cols)
    if len(h) != 483346:
        fail(f"HC-036 has {len(h):,} records, documentation says 483,346 [h36u24doc.pdf C-2]")
    return h


def cpi_factors() -> dict[str, dict[int, float]]:
    js = json.loads(BLS_JSON.read_text())
    if js.get("status") != "REQUEST_SUCCEEDED":
        fail("BLS API response did not succeed")
    out = {}
    for s in js["Results"]["series"]:
        ann = {int(x["year"]): float(x["value"]) for x in s["data"] if x["period"] == "M13"}
        if not all(y in ann for y in YEARS):
            fail(f"{s['seriesID']}: annual averages missing for {sorted(set(YEARS) - set(ann))}")
        out[s["seriesID"]] = {y: ann[2024] / ann[y] for y in YEARS}
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    audit = {"inputs": {}, "years": {}}
    frames = []
    _header("read and gate each year")
    for i, year in enumerate(YEARS, 1):
        p = paths_for(year)
        for k, path in p.items():
            audit["inputs"][path.name] = {"path": str(path), "sha256": sha256(path)}
        d = read_year(year)
        g = gate_year(d, year, codebook_text(p["cb.pdf"]))
        audit["years"][str(year)] = g
        frames.append(d)
        _ok(f"[{i}/{len(YEARS)}] {year} HC-{YEARS[year]}: {len(d):,} records, "
            f"{g['hispncat']['1']['unweighted']:,} Mexican-origin ({g['mexican_label']}), "
            f"codebook HISPNCAT/BORNUSA/RACETHX reproduce; TOTEXP identity max residual "
            f"${g['totexp_identity_max_abs_residual']:.0f}")
    pool = pd.concat(frames, ignore_index=True)

    _header("attach HC-036 pooled variance structure")
    h = read_hc036()
    audit["inputs"][HC036.name] = {"path": str(HC036), "sha256": sha256(HC036)}
    audit["inputs"][HC036_SU.name] = {"path": str(HC036_SU), "sha256": sha256(HC036_SU)}
    # DUPERSID was 8 characters through 2017 and 10 from 2018; HC-036 carries each Panel 22
    # person twice, once under each ID, flagged for both years [h36u24doc.pdf C-2]. The
    # INHnnn counts therefore match the codebook, and the year's own records only once the
    # ID format of that year is applied.
    cb36 = codebook_text(CACHE / "h36u24cb.pdf")
    idlen = h.DUPERSID.str.len()
    inh_gate = {}
    for year, hc in YEARS.items():
        n_flag = int(h[f"INH{hc}"].eq(1).sum())
        n_cb = codebook_frequencies(cb36, f"INH{hc}")[1][1]
        if n_flag != n_cb:
            fail(f"HC-036 INH{hc}==1 count {n_flag:,} != its codebook {n_cb:,}")
        n_fmt = int((h[f"INH{hc}"].eq(1) & idlen.eq(8 if year <= 2017 else 10)).sum())
        n_year = int(pool.year.eq(year).sum())
        if n_fmt != n_year:
            fail(f"HC-036 INH{hc}==1 with the {year} ID format: {n_fmt:,} != {year} records {n_year:,}")
        inh_gate[str(year)] = {"inh_flag_count": n_flag, "codebook": n_cb, "same_id_format": n_fmt}
    p22 = h[h.PANEL.eq(22) & h.INH201.eq(1) & h.INH209.eq(1)]
    a = p22[p22.DUPERSID.str.len().eq(8)].groupby(["STRA9624", "PSU9624"]).size()
    b = p22[p22.DUPERSID.str.len().eq(10)].groupby(["STRA9624", "PSU9624"]).size()
    if not a.equals(b):
        fail("Panel 22 duplicate records do not carry the same stratum/PSU distribution")
    audit["hc036_gates"] = {"inh": inh_gate, "panel22_duplicates_same_design_cells": int(len(a)),
                            "panel22_persons_in_both_2017_and_2018": int(a.sum())}
    _ok(f"HC-036 INH counts match its codebook; with each year's ID format they equal that year's "
        f"records; Panel 22's {int(a.sum()):,} two-ID persons sit in identical design cells under both IDs")
    key = ["DUPERSID", "PANEL"]
    if h.duplicated(key).any():
        fail("HC-036 DUPERSID+PANEL not unique")
    pool = pool.merge(h[key + ["STRA9624", "PSU9624"] + [f"INH{hc}" for hc in YEARS.values()]],
                      on=key, how="left", validate="many_to_one")
    if pool.STRA9624.isna().any():
        fail(f"{int(pool.STRA9624.isna().sum())} person-years unmatched to HC-036")
    flag_ok = np.ones(len(pool), bool)
    for year, hc in YEARS.items():
        m = pool.year.eq(year).to_numpy()
        flag_ok[m] = pool.loc[m, f"INH{hc}"].eq(1).to_numpy()
    if not flag_ok.all():
        fail(f"{int((~flag_ok).sum())} person-years matched to an HC-036 record not flagged for that year")
    pool = pool.drop(columns=[f"INH{hc}" for hc in YEARS.values()])
    design = pool.loc[pool.PERWT.gt(0), ["STRA9624", "PSU9624"]].drop_duplicates()
    per = design.groupby("STRA9624").size()
    if (per < 2).any():
        fail(f"lonely pooled PSU strata {per[per < 2].index.tolist()}")
    audit["pooled_design"] = {"strata": int(len(per)), "psus": int(len(design)),
                              "min_psu_per_stratum": int(per.min()), "max_psu_per_stratum": int(per.max())}
    _ok(f"all {len(pool):,} person-years matched by DUPERSID+PANEL; pooled design "
        f"{len(per)} strata, {len(design)} PSUs, min {per.min()} PSU/stratum")
    multi = pool.groupby(key).size()
    audit["persons_in_more_than_one_year"] = int((multi > 1).sum())
    audit["unique_persons"] = int(len(multi))

    _header("harmonize payers and deflate")
    pool["public_transport"] = pool[PUBLIC_PAYERS].sum(axis=1)
    pool["medicaid"] = pool.TOTMCD + pool.TOTOPU
    pool["public"] = pool.public_transport + pool.TOTOPU
    pool["other_public"] = pool[["TOTVA", "TOTTRI", "TOTOFD", "TOTSTL"]].sum(axis=1)
    pool["private"] = pool.TOTPRV + pool.TOTOPR
    opu_share = {int(y): float((g.TOTOPU * g.PERWT).sum() / (g.medicaid * g.PERWT).sum())
                 for y, g in pool[pool.year.isin(OPU_YEARS)].groupby("year")}
    audit["opu_share_of_harmonized_medicaid"] = opu_share
    _ok("OPU share of harmonized Medicaid dollars: " +
        ", ".join(f"{y} {s:.1%}" for y, s in opu_share.items()))
    factors = cpi_factors()
    audit["deflators"] = {"primary": "CUUR0000SAM CPI-U Medical care, U.S. city average, NSA, annual average (BLS)",
                          "sensitivity": "CUUR0000SA0 CPI-U All items, U.S. city average, NSA, annual average (BLS)",
                          "factor_to_2024": factors,
                          "source": str(BLS_JSON), "sha256": sha256(BLS_JSON)}
    audit["inputs"][BLS_JSON.name] = {"path": str(BLS_JSON), "sha256": sha256(BLS_JSON)}
    pool["defl_med"] = pool.year.map(factors["CUUR0000SAM"]).astype(float)
    pool["defl_all"] = pool.year.map(factors["CUUR0000SA0"]).astype(float)
    _ok("2024-dollar factors, medical care: " +
        ", ".join(f"{y} {f:.4f}" for y, f in factors["CUUR0000SAM"].items()))

    CACHE.mkdir(exist_ok=True)
    pool.to_parquet(CACHE / "pooled.parquet", index=False)
    (DERIVED / "pool_audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    rows = []
    for y, g in audit["years"].items():
        rows.append(dict(year=int(y), hc=f"HC-{YEARS[int(y)]}", records=g["records"],
                         positive_weight=g["positive_weight"], population=g["population"],
                         mexican_origin_n=g["hispncat"]["1"]["unweighted"],
                         mexican_origin_weighted=g["hispncat"]["1"]["weighted"],
                         mexican_label=g["mexican_label"],
                         us_born_weighted=g["bornusa"]["1"]["weighted"],
                         foreign_born_weighted=g["bornusa"]["2"]["weighted"],
                         nh_white_n=g["nh_white"]["unweighted"],
                         annual_strata=g["annual_design"]["strata"], annual_psus=g["annual_design"]["psus"],
                         totexp_identity_max_abs_residual=g["totexp_identity_max_abs_residual"],
                         opu_share_of_medicaid=opu_share.get(int(y), 0.0),
                         deflator_medical_care=factors["CUUR0000SAM"][int(y)],
                         deflator_all_items=factors["CUUR0000SA0"][int(y)]))
    pd.DataFrame(rows).to_csv(DERIVED / "gates_by_year.csv", index=False)
    _ok(f"pooled.parquet: {len(pool):,} person-years; gates_by_year.csv and pool_audit.json written")


if __name__ == "__main__":
    main()
