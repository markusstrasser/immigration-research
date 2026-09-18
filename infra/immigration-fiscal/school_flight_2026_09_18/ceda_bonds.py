"""California school bond and parcel-tax ballot measures against district Hispanic share.

Source: California Elections Data Archive (CEDA), the Secretary of State / CSU Sacramento
joint archive of every local ballot measure, compiled yearly. Files taken from the
justindbk/ceda mirror of the CSUS portal. JUR=3 is a school or community-college district.

Outcome  PERCENT, the yes share (threshold-independent), and a pass indicator with the
         required-majority category (M / F=55% / T=two-thirds) as a control, since
         Proposition 39 (November 2000) cut the school-bond threshold from 2/3 to 55%.
Treatment the district's Hispanic enrolment share in the nearest panel wave.

Districts are matched from the CEDA PLACE string to the CCD lea_name for California by a
normalised exact match first, then a conservative fuzzy match (difflib ratio >= 0.93).
The match rate is reported and unmatched measures are listed, not dropped silently.
"""
import difflib, pathlib, re, sys
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
CEDA = HERE / "_cache" / "ceda"
DERIVED = HERE / "derived"
YEARS = range(1998, 2025)
STRIP = re.compile(r"\b(SCHOOL DISTRICT|SCHOOL DIST|DISTRICT|DIST|SCH DIST|SCHOOLS|"
                   r"SCHOOL|JOINT|COUNTY OFFICE OF EDUCATION)\b")
PUNCT = re.compile(r"[^A-Z0-9 ]+")


def norm(s):
    s = PUNCT.sub(" ", str(s).upper())
    s = STRIP.sub(" ", s)
    return " ".join(s.split())


def load_ceda():
    rows = []
    for f in sorted(CEDA.glob("CEDA*Data.xls*")):
        y = int(re.search(r"(\d{4})", f.name).group(1))
        if y not in YEARS:
            continue
        try:
            x = pd.ExcelFile(f)
        except Exception as e:
            print(f"skip {f.name}: {e}")
            continue
        sh = [s for s in x.sheet_names if s.lower().startswith("measure")]
        if not sh:
            print(f"skip {f.name}: no measures sheet ({x.sheet_names})")
            continue
        d = pd.read_excel(f, sheet_name=sh[0])
        d.columns = [str(c).strip() for c in d.columns]
        d["src_year"] = y
        rows.append(d)
    if not rows:
        sys.exit("no CEDA files parsed")
    d = pd.concat(rows, ignore_index=True)
    print(f"CEDA measures loaded: {len(d):,} rows, {d.src_year.min()}-{d.src_year.max()}")
    return d


def main():
    d = load_ceda()
    d["JUR"] = pd.to_numeric(d.get("JUR"), errors="coerce")
    d = d[d.JUR == 3].copy()
    tn = d.get("RECTYPENAME", pd.Series(index=d.index, dtype=object)).astype(str).str.upper()
    d["is_bond"] = tn.str.contains("BOND")
    d["is_tax"] = tn.str.contains("TAX")
    d = d[d.is_bond | d.is_tax].copy()
    d["pct"] = pd.to_numeric(d.get("PERCENT"), errors="coerce")
    d.loc[d.pct > 1.5, "pct"] = d.loc[d.pct > 1.5, "pct"] / 100.0
    pf = d.get("PASSFAIL", pd.Series(index=d.index, dtype=object)).astype(str).str.upper()
    d["passed"] = pf.str.startswith("PASS").astype(float)
    d.loc[~pf.str.contains("PASS|FAIL", regex=True), "passed"] = np.nan
    d["req"] = d.get("REQ", pd.Series(index=d.index, dtype=object)).astype(str).str.upper().str[0]
    d["year"] = pd.to_numeric(d.get("YEAR"), errors="coerce").fillna(d.src_year).astype(int)
    d["total"] = pd.to_numeric(d.get("TOTAL"), errors="coerce")
    d["key"] = d.PLACE.map(norm)
    print(f"school-district bond/tax measures: {len(d):,} "
          f"({int(d.is_bond.sum()):,} bond, {int(d.is_tax.sum()):,} tax)")

    panel = pd.read_csv(DERIVED / "district_panel.csv", dtype={"leaid": str})
    ca = panel[panel.fips == 6].copy()
    ca["key"] = ca.lea_name.map(norm)
    lut = ca.drop_duplicates("key").set_index("key")
    keys = list(lut.index)

    exact = d.key.isin(lut.index)
    print(f"exact name match: {exact.mean():.3f}")
    fuzzy = {}
    for k in d.loc[~exact, "key"].unique():
        m = difflib.get_close_matches(k, keys, n=1, cutoff=0.93)
        if m:
            fuzzy[k] = m[0]
    d["mkey"] = np.where(exact, d.key, d.key.map(fuzzy))
    matched = d.mkey.notna()
    print(f"matched after fuzzy (cutoff 0.93): {matched.mean():.3f} "
          f"({int(matched.sum()):,} of {len(d):,})")
    print("unmatched examples:", sorted(d.loc[~matched, "key"].unique())[:12])

    d = d[matched].copy()
    # attach the district's Hispanic share from the nearest panel wave
    waves = sorted(ca.year.unique())
    cak = ca.set_index(["key", "year"])
    def near(row):
        yy = min(waves, key=lambda w: abs(w - row.year))
        for w in sorted(waves, key=lambda w: abs(w - row.year)):
            if (row.mkey, w) in cak.index:
                r = cak.loc[(row.mkey, w)]
                r = r.iloc[0] if isinstance(r, pd.DataFrame) else r
                return pd.Series({"hisp_share": r.hisp_share, "white_share": r.white_share,
                                  "elf": r.elf, "pupils": r.pupils, "share65": r.share65,
                                  "pp_current": r.pp_current, "wave": w, "leaid": r.name[0]
                                  if isinstance(r.name, tuple) else None})
        return pd.Series({k: np.nan for k in ("hisp_share", "white_share", "elf", "pupils",
                                              "share65", "pp_current", "wave", "leaid")})
    att = d.apply(near, axis=1)
    d = pd.concat([d.reset_index(drop=True), att.reset_index(drop=True)], axis=1)
    d = d.dropna(subset=["hisp_share", "pct"])
    print(f"estimation sample: {len(d):,} measures, "
          f"{d.mkey.nunique():,} districts, {d.year.min()}-{d.year.max()}")
    d.to_csv(DERIVED / "ca_bond_measures.csv", index=False)

    out = []
    def ols(y, X, names, w, label, cluster):
        sw = np.sqrt(w)
        Xw, yw = X * sw[:, None], y * sw
        b = np.linalg.solve(Xw.T @ Xw, Xw.T @ yw)
        e = yw - Xw @ b
        A = np.linalg.inv(Xw.T @ Xw)
        meat = np.zeros((X.shape[1], X.shape[1]))
        for _, ix in pd.Series(range(len(cluster))).groupby(np.asarray(cluster)).groups.items():
            ix = np.asarray(ix)
            s = Xw[ix].T @ e[ix]
            meat += np.outer(s, s)
        G = len(set(cluster))
        V = A @ meat @ A * (G / max(G - 1, 1)) * ((len(y) - 1) / max(len(y) - X.shape[1], 1))
        se = np.sqrt(np.diag(V))
        for i, nm in enumerate(names):
            if nm == "_const" or nm.startswith("fe_"):
                continue
            out.append(dict(spec=label, outcome="yes vote share" if label.startswith("pct")
                            else label, treatment=nm, n=len(y), coef=float(b[i]),
                            se=float(se[i]), t=float(b[i] / se[i])))
            print(f"{label:34s} {nm:14s} n={len(y):5d} coef={b[i]:+.4f} "
                  f"se={se[i]:.4f} t={b[i]/se[i]:+.2f}", flush=True)

    for outcome, oname in (("pct", "yes vote share"), ("passed", "passed (LPM)")):
        s = d.dropna(subset=[outcome]).copy()
        yv = s[outcome].to_numpy(float)
        yrfe = pd.get_dummies(s.year, prefix="fe_yr", drop_first=True).to_numpy(float)
        reqfe = pd.get_dummies(s.req, prefix="fe_req", drop_first=True).to_numpy(float)
        one = np.ones(len(s))
        w = s.total.fillna(s.total.median()).to_numpy(float)
        for treat in ("hisp_share", "elf"):
            X = np.column_stack([s[treat].to_numpy(float), yrfe, reqfe, one])
            nm = [treat] + [f"fe_{i}" for i in range(yrfe.shape[1] + reqfe.shape[1])] + ["_const"]
            ols(yv, X, nm, w, f"{outcome}: {oname}, year+threshold FE", s.mkey.to_numpy())
        X = np.column_stack([s.hisp_share.to_numpy(float), s.share65.fillna(
            s.share65.median()).to_numpy(float), yrfe, reqfe, one])
        nm = ["hisp_share", "share65"] + \
             [f"fe_{i}" for i in range(yrfe.shape[1] + reqfe.shape[1])] + ["_const"]
        ols(yv, X, nm, w, f"{outcome}: {oname}, + elderly share", s.mkey.to_numpy())

    pd.DataFrame(out).to_csv(DERIVED / "estimates_bonds.csv", index=False)
    print(f"\nwrote {DERIVED/'estimates_bonds.csv'}")


if __name__ == "__main__":
    main()
