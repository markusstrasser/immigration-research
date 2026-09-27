#!/usr/bin/env python3
"""Who adjusts: parents of US citizens (IR-5) in the New Immigrant Survey 2003, new arrivals vs adjusters.

Inputs (read-only): ICPSR 38031 v3 zip (NIS-2003 Round 1, adult sample, n = 8,573):
  DS0002 administrative preload: CISADJUST (1 = adjusting status, 0 = new arrival), VISACATMO
         (3 = "Parent of U.S. Citizen"), CISCOBINSMO (135 = Mexico), CISADMYER/CISADMMON (LPR date),
         NISTEMPVISA (status at adjustment, admin record), CISNIMMYER (date of nonimmigrant visa),
         NISWGTSAMP1 (sampling weight).
  DS0003 Section A: A7 birth year.
  DS0004 Section B: B74 worked since coming to the US to live, B75 year first worked.
  DS0018 Section K migration history: every move of 60+ days (K3 month, K4 year, K6 country,
         218 = United States; K10 had a visa or entry document, 2 = no; K11 kind of document,
         26 = no documents), K18B currently lives in the last country named, K19/K20 arrival in the
         country of current residence.
Codes are quoted from the P.I. codebooks (DS0002, DS0018) in the lane's RESULT.

Definitions:
  spell       years from the start of the current US residence to the LPR date. The start is the
              last K-move to the United States when the respondent still lives in the last country
              named (K18B = 1), otherwise the K19/K20 arrival. A move is any stay of 60+ days, so a
              two-month trip home restarts the spell (stricter than SSA's six-month rule for Medicare).
  first_us    years from the first K-move to the United States to the LPR date.
  ewi_ever    any US move made without a visa or entry document (K10 = 2 or K11 = 26).
  worked_us   B74 = 1 and a first US work year (B75) before the LPR year.
  pre1996     spell start before 22 August 1996 (the date in 8 U.S.C. 1613(a)).
Estimates are weighted by NISWGTSAMP1. Standard errors use the Kish effective sample size,
n_eff = (sum w)^2 / sum w^2, with the binomial or weighted-variance formula; they ignore the
survey's clustering.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ir5_adjusters_2026_09_27/nis_adjusters.py
"""
from __future__ import annotations

import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
NIS_ZIP = ROOT / "sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip"
OUT = HERE / "derived"

US = 218
MEXICO = 135
PARENT = 3  # VISACATMO "Parent of U.S. Citizen"
N_MOVES = 40
TEMPVISA = {1: "entered_without_inspection", 2: "exchange_visitor", 3: "fiance", 4: "intracompany",
            5: "life_act", 6: "refugee_asylee_parolee", 7: "student", 8: "visitor_business",
            9: "visitor_pleasure", 10: "temporary_worker", 11: "unknown", 12: "other"}
SPELL_BINS = ((0, 1), (1, 2), (2, 5), (5, 10), (10, 20), (20, 28), (28, 200))
AGE_BINS = ((0, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 75), (75, 200))
PRE1996 = 1996 + (8 - 1 + 21.5 / 31) / 12  # 22 August 1996 as a decimal year
# Adjuster types by years of residence before the green card, cut where eligibility changes:
# under 2 years a recent entrant; 5+ years clears Medicare's residence test at adjustment; 28+ years
# would, for an FY2024 adjustment, mean residence since before 22 August 1996.
TYPES = (("T0_recent", -50, 2), ("T1_settling", 2, 5), ("T2_long", 5, 28), ("T3_pre1996", 28, 200))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s.astype(str).str.strip(), errors="coerce")


def load() -> pd.DataFrame:
    with zipfile.ZipFile(NIS_ZIP) as z:
        rd = lambda name, **kw: pd.read_csv(io.BytesIO(z.read(name)), sep="\t", dtype=str, **kw)
        d2 = rd("ICPSR_38031/DS0002/38031-0002-Data.tsv")
        d3 = rd("ICPSR_38031/DS0003/38031-0003-Data.tsv", usecols=["PU_ID", "A7"])
        d4 = rd("ICPSR_38031/DS0004/38031-0004-Data.tsv", usecols=["PU_ID", "B74", "B75"])
        k = rd("ICPSR_38031/DS0018/38031-0018-Data.tsv")
    k = k[[c for c in k.columns if c == "PU_ID" or c.startswith("K")]]
    d = d2.merge(d3, on="PU_ID", validate="1:1").merge(d4, on="PU_ID", how="left", validate="1:1")
    d = d.merge(k, on="PU_ID", how="left", validate="1:1")
    assert len(d) == 8573, len(d)
    for c in d.columns:
        if c != "NISTEMPVISA":
            d[c] = num(d[c])
    d["NISTEMPVISA"] = num(d["NISTEMPVISA"])
    d = d[d.VISACATMO == PARENT].copy()
    assert len(d) == 995, len(d)  # P.I. codebook DS0002: 995 parents of US citizens
    return d


def valid_year(y) -> bool:
    return pd.notna(y) and 1900 <= y <= 2004


def dec(y, m) -> float:
    m = m if pd.notna(m) and 1 <= m <= 12 else 6.5
    return float(y) + (float(m) - 0.5) / 12


def histories(d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for r in d.itertuples(index=False):
        r = r._asdict()
        moves = []
        for x in range(1, N_MOVES + 1):
            c, y = r.get(f"K6_{x}MO"), r.get(f"K4_{x}")
            if pd.isna(c) and pd.isna(y):
                break
            moves.append({"country": c, "year": y, "month": r.get(f"K3_{x}"),
                          "doc": r.get(f"K10_{x}"), "kind": r.get(f"K11_{x}NU")})
        us = [m for m in moves if m["country"] == US]
        start = np.nan
        if moves and moves[-1]["country"] == US and r["K18B"] == 1 and valid_year(moves[-1]["year"]):
            start = dec(moves[-1]["year"], moves[-1]["month"])
        elif r["K18B"] == 2 and valid_year(r["K20"]):
            start = dec(r["K20"], r["K19"])
        first = next((dec(m["year"], m["month"]) for m in us if valid_year(m["year"])), np.nan)
        lpr = dec(r["CISADMYER"], r["CISADMMON"])
        rows.append({
            "PU_ID": r["PU_ID"],
            "spell": lpr - start if pd.notna(start) else np.nan,
            "spell_start": start,
            "first_us": lpr - first if pd.notna(first) else np.nan,
            "n_us_moves": len(us),
            "ewi_ever": float(any(m["doc"] == 2 or m["kind"] == 26 for m in us)) if us else 0.0,
            "k_missing": float(not moves),
        })
    h = pd.DataFrame(rows)
    out = d.merge(h, on="PU_ID", validate="1:1")
    out["age"] = np.where(out.A7 > 1800, out.CISADMYER - out.A7, np.nan)
    out["worked_us"] = ((out.B74 == 1) & (out.B75 >= 1900) & (out.B75 < out.CISADMYER)).astype(float)
    out["years_worked_before"] = np.where(out.worked_us == 1, out.CISADMYER - out.B75, 0.0)
    out["pre1996"] = np.where(out.spell_start.notna(), (out.spell_start < PRE1996).astype(float), np.nan)
    out["group"] = np.where(out.CISCOBINSMO == MEXICO, "mexico", "other")
    out["channel"] = np.where(out.CISADJUST == 1, "adjust", "new")
    out["tempvisa"] = out.NISTEMPVISA.map(TEMPVISA).fillna("missing")
    out["nimm_years"] = np.where(out.CISNIMMYER > 1900, out.CISADMYER - out.CISNIMMYER, np.nan)
    return out


def kish(w: np.ndarray) -> float:
    return float(w.sum() ** 2 / (w ** 2).sum()) if len(w) else 0.0


def wmean(x: pd.Series, w: pd.Series) -> tuple[float, float, int, float]:
    m = x.notna()
    x, w = x[m].to_numpy(float), w[m].to_numpy(float)
    if not len(x):
        return np.nan, np.nan, 0, 0.0
    mu = float((w * x).sum() / w.sum())
    var = float((w * (x - mu) ** 2).sum() / w.sum())
    ne = kish(w)
    return mu, float(np.sqrt(var / ne)) if ne > 1 else np.nan, len(x), ne


def wquantile(x: pd.Series, w: pd.Series, q: float) -> float:
    m = x.notna()
    x, w = x[m].to_numpy(float), w[m].to_numpy(float)
    o = np.argsort(x, kind="stable")
    x, w = x[o], w[o]
    c = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(c, q)])


def summarise(p: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    stats, bins = [], []
    groups = {"mexico": p.group == "mexico", "other": p.group == "other", "all": p.group.notna()}
    for g, gm in groups.items():
        sub = p[gm]
        w_all = sub.NISWGTSAMP1
        for ch in ("new", "adjust", "both"):
            s = sub if ch == "both" else sub[sub.channel == ch]
            w = s.NISWGTSAMP1

            def add(stat, x, ww=w):
                mu, se, n, ne = wmean(x, ww)
                stats.append({"group": g, "channel": ch, "stat": stat, "estimate": round(mu, 6),
                              "se": round(se, 6) if pd.notna(se) else np.nan, "n_unweighted": n,
                              "n_eff": round(ne, 1)})

            if ch != "both":
                add("share_of_group_ir5", (sub.channel == ch).astype(float), w_all)
            add("age_at_lpr_mean", s.age)
            for lo, hi in AGE_BINS:
                add(f"age_{lo}_{hi - 1 if hi < 200 else 'plus'}", s.age.between(lo, hi - 1).astype(float).where(s.age.notna()))
            add("age_55plus", (s.age >= 55).astype(float).where(s.age.notna()))
            add("age_65plus", (s.age >= 65).astype(float).where(s.age.notna()))
            add("spell_years_mean", s.spell)
            add("first_us_years_mean", s.first_us)
            add("spell_5plus", (s.spell >= 5).astype(float).where(s.spell.notna()))
            add("spell_lt2", (s.spell < 2).astype(float).where(s.spell.notna()))
            add("pre1996_continuous", s.pre1996)
            add("ewi_ever", s.ewi_ever.where(s.k_missing == 0))
            add("worked_us_before_lpr", s.worked_us.where(s.B74.isin([1, 2])))
            add("years_worked_before_mean", s.years_worked_before.where(s.B74.isin([1, 2])))
            add("worked_10plus_years_before", (s.years_worked_before >= 10).astype(float).where(s.B74.isin([1, 2])))
            add("nonimmigrant_date_known", (s.CISNIMMYER > 1900).astype(float))
            add("years_since_nonimmigrant_entry_mean", s.nimm_years)
            if ch == "adjust":
                for code in list(TEMPVISA.values()) + ["missing"]:
                    add(f"status_at_adjustment_{code}", (s.tempvisa == code).astype(float))
            for q in (0.1, 0.25, 0.5, 0.75, 0.9):
                if s.spell.notna().any():
                    stats.append({"group": g, "channel": ch, "stat": f"spell_q{int(q * 100)}",
                                  "estimate": round(wquantile(s.spell, w, q), 3), "se": np.nan,
                                  "n_unweighted": int(s.spell.notna().sum()),
                                  "n_eff": round(kish(w[s.spell.notna()].to_numpy(float)), 1)})
            sp = s[s.spell.notna()]
            for lo, hi in SPELL_BINS:
                m = (sp.spell >= lo) & (sp.spell < hi) if lo > 0 else (sp.spell < hi)
                bins.append({"group": g, "channel": ch,
                             "spell_bin": f"{lo}-{hi}" if hi < 200 else f"{lo}plus",
                             "weighted_share": round(float(sp.NISWGTSAMP1[m].sum() / sp.NISWGTSAMP1.sum()), 6),
                             "n_unweighted": int(m.sum())})
    return stats, bins


def adjuster_types(p: pd.DataFrame) -> list[dict]:
    """Mexican IR-5 adjusters with a measured spell, by type; 'no_ewi' drops anyone who ever entered
    without documents, since after April 2001 such a parent can adjust only under grandfathered
    245(i) or parole."""
    a = p[(p.group == "mexico") & (p.channel == "adjust") & p.spell.notna()]
    rows = []
    for sample, s in (("all", a), ("no_ewi", a[a.ewi_ever == 0])):
        wt = s.NISWGTSAMP1.sum()
        for name, lo, hi in TYPES:
            t = s[(s.spell >= lo) & (s.spell < hi)]
            w = t.NISWGTSAMP1
            rec = {"sample": sample, "type": name, "n_unweighted": len(t),
                   "weighted_share": round(float(w.sum() / wt), 6),
                   "mean_age": round(float(np.average(t.age, weights=w)), 3),
                   "mean_spell": round(float(np.average(t.spell, weights=w)), 3),
                   "worked_us_before_lpr": round(float(np.average(t.worked_us, weights=w)), 6),
                   "mean_years_worked_before": round(float(np.average(t.years_worked_before, weights=w)), 3),
                   "ewi_ever": round(float(np.average(t.ewi_ever, weights=w)), 6)}
            for lo_a, hi_a in AGE_BINS:
                m = t.age.between(lo_a, hi_a - 1)
                rec[f"age_{lo_a}_{hi_a - 1 if hi_a < 200 else 'plus'}"] = round(float(w[m].sum() / w.sum()), 6)
            rows.append(rec)
    return rows


def main() -> None:
    OUT.mkdir(exist_ok=True)
    p = histories(load())
    stats, bins = summarise(p)
    pd.DataFrame(stats).to_csv(OUT / "nis_ir5_channels.csv", index=False, lineterminator="\n")
    pd.DataFrame(bins).to_csv(OUT / "nis_ir5_spells.csv", index=False, lineterminator="\n")
    pd.DataFrame(adjuster_types(p)).to_csv(OUT / "nis_ir5_adjuster_types.csv", index=False,
                                          lineterminator="\n")
    prov = {"nis_zip": {str(NIS_ZIP.relative_to(ROOT)): sha256(NIS_ZIP)},
            "parents": int(len(p)), "mexico_parents": int((p.group == "mexico").sum()),
            "mexico_adjusters": int(((p.group == "mexico") & (p.channel == "adjust")).sum())}
    (OUT / "nis_provenance.json").write_text(json.dumps(prov, indent=1, sort_keys=True) + "\n")
    s = pd.DataFrame(stats)
    key = s[(s.group == "mexico") & s.stat.isin(["share_of_group_ir5", "age_at_lpr_mean", "age_55plus",
                                                  "spell_5plus", "spell_lt2", "spell_q50",
                                                  "pre1996_continuous", "ewi_ever",
                                                  "worked_us_before_lpr"])]
    print(key.to_string())
    print(pd.DataFrame(bins).query("group == 'mexico' and channel == 'adjust'").to_string())


if __name__ == "__main__":
    main()
