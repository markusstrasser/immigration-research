"""DOL OFLC LCA disclosure data: prevailing-wage-level (I-IV) shares of certified H-1B LCAs,
India-heavy IT outsourcers vs all other employers.

Usage: python lca_wage_levels.py <label> <xlsx> [<xlsx> ...]   (quarterly files of one FY are pooled)
Appends to context/lca_wage_levels.csv. Units: LCA cases and requested worker positions
(LCAs are employer filings, not hires/petitions/persons).
"""
import csv, hashlib, pathlib, re, sys, time
import polars as pl
LANE = pathlib.Path(__file__).resolve().parents[1]
OUT = LANE / "context/lca_wage_levels.csv"
GROUPS = {  # regex on upper-cased EMPLOYER_NAME
    "infosys": r"\bINFOSYS\b", "tcs": r"TATA CONSULTANCY", "cognizant": r"\bCOGNIZANT\b",
    "wipro": r"\bWIPRO\b", "hcl": r"\bHCL (AMERICA|TECHNOLOGIES|GLOBAL)", "tech_mahindra": r"TECH MAHINDRA",
}
def pick(cols, *pats):
    for p in pats:
        for c in cols:
            if re.fullmatch(p, c, re.I): return c
    raise SystemExit(f"[BLOCKED] no column matching {pats} in {cols}")
label, files = sys.argv[1], sys.argv[2:]
frames = []
for f in files:
    t0 = time.time()
    cols = pl.read_excel(f, engine="calamine", infer_schema_length=0, read_options={"n_rows": 1}).columns
    st = pick(cols, "CASE_STATUS", "STATUS"); vc = pick(cols, "VISA_CLASS", "VISA_TYPE")
    em = pick(cols, "EMPLOYER_NAME", "LCA_CASE_EMPLOYER_NAME")
    wl = pick(cols, "PW_WAGE_LEVEL", "PW_WAGE_LEVEL_1", "WAGE_LEVEL", "PW_LEVEL", "PREVAILING_WAGE_LEVEL")
    tw = pick(cols, "TOTAL_WORKER_POSITIONS", "TOTAL_WORKERS", "TOTAL WORKERS", "TOTAL_WORKERS_1")
    df = pl.read_excel(f, engine="calamine", infer_schema_length=0, columns=[st, vc, em, wl, tw])
    print(f, "cols:", st, vc, em, wl, tw, "rows", df.height, f"{time.time()-t0:.0f}s", "sha256",
          hashlib.sha256(pathlib.Path(f).read_bytes()).hexdigest(), file=sys.stderr)
    frames.append(df.select(pl.col(st).alias("status"), pl.col(vc).alias("visa"), pl.col(em).alias("emp"),
                            pl.col(wl).alias("lvl"), pl.col(tw).alias("workers")))
d = pl.concat(frames)
print("status values:", d["status"].value_counts().sort("count", descending=True).head(8).rows(), file=sys.stderr)
print("visa values:", d["visa"].value_counts().sort("count", descending=True).head(6).rows(), file=sys.stderr)
print("level values:", d["lvl"].value_counts().sort("count", descending=True).head(10).rows(), file=sys.stderr)
d = d.filter(pl.col("status").str.to_uppercase().str.strip_chars() == "CERTIFIED")
d = d.filter(pl.col("visa").str.to_uppercase().str.contains("H-1B|H1B") & ~pl.col("visa").str.to_uppercase().str.contains("H-1B1"))
up = pl.col("emp").fill_null("").str.to_uppercase()
grp = pl.lit("other")
for g, rx in GROUPS.items():
    grp = pl.when(up.str.contains(rx)).then(pl.lit(g)).otherwise(grp)
lv = pl.col("lvl").fill_null("").str.to_uppercase().str.replace_all(r"LEVEL\s*", "").str.strip_chars()
d = d.with_columns(grp.alias("grp"), lv.alias("lv"),
                   pl.col("workers").cast(pl.Float64, strict=False).fill_null(1).alias("w"))
d = d.with_columns(pl.col("lv").replace({"1": "I", "2": "II", "3": "III", "4": "IV"}).alias("lv"))
d = d.with_columns(pl.when(pl.col("lv").is_in(["I", "II", "III", "IV"])).then(pl.col("lv")).otherwise(pl.lit("missing")).alias("lv"))
def summarize(sub, name):
    n = sub.height; wsum = sub["w"].sum()
    row = {"label": label, "group": name, "lca_certified_h1b": n, "worker_positions": int(wsum)}
    known = sub.filter(pl.col("lv") != "missing"); kn = known.height; kw = known["w"].sum()
    row["level_missing_share_cases"] = round(1 - kn / n, 4) if n else None
    for L in ["I", "II", "III", "IV"]:
        s = known.filter(pl.col("lv") == L)
        row[f"lvl_{L}_share_cases"] = round(s.height / kn, 4) if kn else None
        row[f"lvl_{L}_share_workers"] = round(s["w"].sum() / kw, 4) if kw else None
    return row
rows = [summarize(d, "all_employers"), summarize(d.filter(pl.col("grp") != "other"), "six_outsourcers"),
        summarize(d.filter(pl.col("grp") == "other"), "all_other_employers")]
rows += [summarize(d.filter(pl.col("grp") == g), g) for g in GROUPS]
new = not OUT.exists()
with open(OUT, "a", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
    if new: w.writeheader()
    w.writerows(rows)
for r in rows: print(r)
