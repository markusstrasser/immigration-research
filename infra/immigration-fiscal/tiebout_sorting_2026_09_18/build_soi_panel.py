"""IRS SOI state migration flows by AGI bracket, tax-year pairs 2011-12 .. 2022-23.

Source file: `_cache/<yy><yy>inmigall.csv`, fetched by `fetch_soi.sh`, one row per state x agi_stub.
Verified on 1112 (Alabama): rows agi_stub 1..7 sum to the agi_stub=0 row; the `_0`
column suffix is the all-brackets total; `inflow_*` are in-migrants and `outflow_*`
out-migrants, both US domestic. Returns (n1) differ from the state-pair file
(`stateinflow`) by about 0.5% because the pair file suppresses small cells.
[SOURCE: irs.gov/statistics/soi-tax-stats-migration-data]

AGI brackets (SOI migration coding):
  1 $1 under $10k · 2 $10k-$25k · 3 $25k-$50k · 4 $50k-$75k
  5 $75k-$100k · 6 $100k-$200k · 7 $200k or more
Brackets are nominal and not indexed, so bracket 7's share rises mechanically over
the panel; all cross-state comparisons below are within-year.

Output: derived/soi_state_agi.csv
"""
import os, re, sys
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")
DERIVED = os.path.join(HERE, "derived")
os.makedirs(DERIVED, exist_ok=True)

FLOWS = ["inflow", "outflow", "nonmig", "total"]
MEAS = ["n1", "n2", "y1_agi", "y2_agi"]


def main():
    out = []
    for f in sorted(os.listdir(CACHE)):
        m = re.match(r"^(\d{4})inmigall\.csv$", f)
        if not m:
            continue
        tag = m.group(1)
        d = pd.read_csv(os.path.join(CACHE, f), dtype={"statefips": str})
        d.columns = [c.strip().lower() for c in d.columns]
        d["statefips"] = d["statefips"].str.zfill(2)
        keep = ["statefips", "agi_stub"] + ["%s_%s_0" % (fl, me) for fl in FLOWS for me in MEAS]
        miss = [c for c in keep if c not in d.columns]
        if miss:
            sys.stderr.write("%s missing %s\n" % (f, miss))
            continue
        d = d[keep].copy()
        d["year2"] = 2000 + int(tag[2:])      # the later tax year of the pair
        d["pair"] = tag
        out.append(d)
        print(tag, "rows", len(d), "agi_stubs", sorted(d.agi_stub.unique()), flush=True)
    if not out:
        raise SystemExit("no SOI data parsed")
    panel = pd.concat(out, ignore_index=True)
    panel.to_csv(os.path.join(DERIVED, "soi_state_agi.csv"), index=False)
    print("wrote soi_state_agi.csv", panel.shape, "pairs", sorted(panel.pair.unique()))
    cov = panel.groupby("pair")["statefips"].nunique()
    short = cov[cov < 51]
    if len(short):
        print("[WARN] IRS ships an incomplete inmigall file for:",
              dict(short), "- these pairs are dropped from the state panel")
    totals()


def totals():
    """All-bracket state totals from the state-pair files, which are complete in every
    year including 2014-15. The `y1_statefips`/`y2_statefips` code 97 is the row
    'Total Migration US' (domestic only; 98 is foreign, 96 is both)."""
    rows = []
    for f in sorted(os.listdir(CACHE)):
        m = re.match(r"^state(in|out)flow(\d{4})\.csv$", f)
        if not m:
            continue
        side, tag = m.group(1), m.group(2)
        d = pd.read_csv(os.path.join(CACHE, f), dtype=str)
        d.columns = [c.strip().lower() for c in d.columns]
        own = "y2_statefips" if side == "in" else "y1_statefips"
        oth = "y1_statefips" if side == "in" else "y2_statefips"
        d = d[d[oth] == "97"]
        for _, r in d.iterrows():
            rows.append(dict(statefips=r[own].zfill(2), pair=tag, side=side,
                             year2=2000 + int(tag[2:]),
                             n1=float(r["n1"]), n2=float(r["n2"]), agi=float(r["agi"])))
    if not rows:
        return
    t = pd.DataFrame(rows)
    w = t.pivot_table(index=["statefips", "pair", "year2"], columns="side",
                      values=["n1", "n2", "agi"]).reset_index()
    w.columns = ["%s_%s" % (a, b) if b else a for a, b in w.columns]
    w.to_csv(os.path.join(DERIVED, "soi_state_totals.csv"), index=False)
    print("wrote soi_state_totals.csv", w.shape, "pairs", w.pair.nunique(),
          "states", w.statefips.nunique())


if __name__ == "__main__":
    main()
