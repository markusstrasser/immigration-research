#!/usr/bin/env python3
"""How many new Mexican green-card holders had entered the US without papers, by which route, and how long it took.

Question (operator, 2026-09-23): how easy is it to get legal status?

New Immigrant Survey 2003, Round 1, adult sample (ICPSR 38031 v3): 8,573 people granted permanent
residence May-November 2003, interviewed about four months later. Section K lists every move of 60
days or more; for each move to the United States (K6_xMO == 218) it asks K10_x "For that trip, did
you have a visa or other entry document?" (1 yes, 2 no). A "no" on any US move is an entry without
papers. The measure misses visa overstays, work on a tourist visa or border-crossing card, and
undocumented visits shorter than 60 days, so it is a lower bound on prior unauthorized status.

Admission route from the CIS preload (DS0002): VISACATMO (NIS visa category) split by CLASSADMMO
(first letter of the class code; see CATEGORY), CISADJUST (1 adjusted status inside the US, 0 arrived
on an immigrant visa), CISADMYER (year of admission). Weighted by the design weight NISWGTSAMP1;
standard errors from a bootstrap of respondents within the four sampling strata (NISADULTSTR), which
ignores the replicate-by-stratum cells the religion lane uses.

Gates: codebook counts (GATE), the Mexico weighted share printed in the NIS adult handout, and a
printed comparison of the Mexican class mix with the FY2003 Yearbook (Table 8).

Stage the data first (git-ignored cache), then run from the repository root:
    Z=sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip
    L=infra/immigration-fiscal/parent_status_2026_09_23
    for d in 0002 0018; do unzip -o -q "$Z" "ICPSR_38031/DS$d/38031-$d-Data.tsv" -d "$L/_cache/"; done
    uv run --no-project python3 $L/nis_prior_undocumented.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache/ICPSR_38031"
MEXICO, USA = 135, 218                 # CISCOBINSMO / K6_xMO codes, DS0002 and DS0018 P.I. codebooks
N_MOVES = 40                           # K3_XX loop, XX = 1 to 40 (Section K questionnaire)
# DS0002 P.I. codebook: VISACATMO labels. Split below by CLASSADMMO, the first letter of the INS class code:
# "Other" is class F for 780 of 786 adults (the family preferences not listed separately: adult sons and
# daughters of citizens, married children, children of LPRs); "Legalization" is classes Z, T&W and L-N.
# 2003 Yearbook of Immigration Statistics, Table 5: Z13/Z14 cancellation of removal or suspension "subject
# to 4,000 annual limit", Z15 NACARA 203, Z33/Z66/Z83 registry; W16/W26/W36 IRCA legalization.
CATEGORY = {0: "Other", 1: "Spouse of US citizen", 2: "Spouse of LPR", 3: "Parent of US citizen",
            4: "Child of US citizen", 5: "Family fourth preference", 7: "Employment",
            9: "Diversity", 11: "Refugee/asylee/parolee", 13: "Legalization"}
# Positive controls from the P.I. codebooks: adult n; Mexico n (ciscobinsmo); K10.01 yes/no counts
GATE = {"n": 8573, "mexico": 1164, "k10_1_yes": 5702, "k10_1_no": 1488, "adjust": 4402}
DRAWS = 500
TEXT = {"CLASSADMMO"}
HANDOUT_MEXICO_WEIGHTED = 0.175        # NIS adult handout, Table 3: Mexico 17.5% weighted
# 2003 Yearbook, Table 8, Mexico row (FY2003): total and selected classes
YEARBOOK_MEXICO_2003 = {"total": 115864, "family preferences": 29664, "employment": 3261,
                        "spouses of US citizens": 42990, "children of US citizens": 14954,
                        "parents of US citizens": 20838, "cancellation of removal": 2503}
# DHS OIS, "Estimates of the Unauthorized Immigrant Population Residing in the United States: January
# 2005" (Hoefer, Rytina and Campbell 2006), Table 3, Mexico-born, thousands
UNAUTHORIZED_MEXICO = {2000.0: 4680, 2005.0: 5970}


def read(ds: str, cols: list[str]) -> pd.DataFrame:
    path = CACHE / f"DS{ds}/38031-{ds}-Data.tsv"
    if not path.exists():
        sys.exit(f"[BLOCKED] missing {path}; unzip it into _cache/ first (see the docstring)")
    d = pd.read_csv(path, sep="\t", usecols=cols, dtype=str)
    for c in cols[1:]:                 # valid skips are a single blank; ICPSR codes stay negative
        d[c] = d[c].str.strip() if c in TEXT else pd.to_numeric(d[c], errors="coerce")
    return d


def build() -> pd.DataFrame:
    pre = read("0002", ["PU_ID", "CISCOBINSMO", "CISADJUST", "CISADMYER", "VISACATMO", "CLASSADMMO",
                        "NISADULTSTR", "NISWGTSAMP1"])
    kcols = [f"{v}_{x}{s}" for x in range(1, N_MOVES + 1) for v, s in (("K4", ""), ("K6", "MO"), ("K10", ""))]
    k = read("0018", ["PU_ID"] + kcols)
    got = {"n": len(pre), "mexico": int(pre.CISCOBINSMO.eq(MEXICO).sum()),
           "k10_1_yes": int(k.K10_1.eq(1).sum()), "k10_1_no": int(k.K10_1.eq(2).sum()),
           "adjust": int(pre.CISADJUST.eq(1).sum())}
    if got != GATE:
        sys.exit(f"[BLOCKED] codebook gate failed: {got} vs {GATE}")
    mx_w = pre.NISWGTSAMP1[pre.CISCOBINSMO.eq(MEXICO)].sum() / pre.NISWGTSAMP1.sum()
    if abs(mx_w - HANDOUT_MEXICO_WEIGHTED) > 0.002:
        sys.exit(f"[BLOCKED] Mexico weighted share {mx_w:.4f} vs handout {HANDOUT_MEXICO_WEIGHTED}")
    d = pre.merge(k, on="PU_ID", how="left", validate="1:1")

    year = np.stack([d[f"K4_{x}"].to_numpy(float) for x in range(1, N_MOVES + 1)], 1)
    dest = np.stack([d[f"K6_{x}MO"].to_numpy(float) for x in range(1, N_MOVES + 1)], 1)
    doc = np.stack([d[f"K10_{x}"].to_numpy(float) for x in range(1, N_MOVES + 1)], 1)
    us = dest == USA
    valid_year = us & (year >= 1900)
    no_doc = us & (doc == 2)
    answered = us & np.isin(doc, [1, 2])

    out = pd.DataFrame({"PU_ID": d.PU_ID, "mexico": d.CISCOBINSMO.eq(MEXICO),
                        "adjusted": d.CISADJUST.eq(1), "admit_year": d.CISADMYER,
                        "category": [category(v, c) for v, c in zip(d.VISACATMO, d.CLASSADMMO)],
                        "stratum": d.NISADULTSTR,
                        "w": d.NISWGTSAMP1.astype(float)})
    out["us_moves"] = us.sum(1)
    out["answered_any"] = answered.any(1)
    out["entered_without_papers"] = no_doc.any(1)
    first = np.where(valid_year, year, np.inf).min(1)
    out["first_us_year"] = np.where(np.isfinite(first), first, np.nan)
    first_ewi = np.where(no_doc & valid_year, year, np.inf).min(1)
    out["first_no_papers_year"] = np.where(np.isfinite(first_ewi), first_ewi, np.nan)
    out["years_first_us_to_lpr"] = out.admit_year - out.first_us_year
    last = np.where(us, np.arange(N_MOVES)[None, :], -1).max(1)
    out["last_us_move_without_papers"] = (last >= 0) & (doc[np.arange(len(d)), np.maximum(last, 0)] == 2)
    return out


def category(visacat: float, klass: str) -> str:
    label = CATEGORY.get(visacat, "missing")
    if label == "Other" and klass == "F":
        return "Other family preference"
    if label == "Legalization":
        return "Cancellation of removal or registry" if klass == "Z" else "Legalization classes (W)"
    return label


FAMILY_EMPLOYMENT = {"Spouse of US citizen", "Child of US citizen", "Parent of US citizen", "Spouse of LPR",
                     "Family fourth preference", "Other family preference", "Employment"}


def route_type(r) -> str:
    """How a new LPR who had entered without papers got through, on the law in force in 2003.

    INA 245(a) requires inspection and admission or parole, so an adjustment inside the US in a family or
    employment class by someone whose last entry was without papers needed 245(i) (petition or labor
    certification filed by April 30, 2001). A documented last entry leaves 245(a) open to immediate
    relatives, so that cell is kept apart.
    """
    if r.category in ("Legalization classes (W)", "Cancellation of removal or registry"):
        return r.category
    if r.category in FAMILY_EMPLOYMENT and r.adjusted:
        return ("adjusted inside, last entry without papers: needed 245(i)" if r.last_us_move_without_papers
                else "adjusted inside, last entry documented")
    if r.category in FAMILY_EMPLOYMENT:
        return "left and returned on an immigrant visa"
    return r.category


def wshare(x: np.ndarray, w: np.ndarray) -> float:
    return float((x * w).sum() / w.sum())


def boot_se(frame: pd.DataFrame, stat, seed: int = 20260923) -> float:
    rng = np.random.default_rng(seed)
    groups = [g.index.to_numpy() for _, g in frame.groupby("stratum")]
    vals = []
    for _ in range(DRAWS):
        idx = np.concatenate([rng.choice(g, size=len(g), replace=True) for g in groups])
        vals.append(stat(frame.loc[idx]))
    return float(np.nanstd(vals, ddof=1))


def wquantiles(v: np.ndarray, w: np.ndarray, qs=(0.25, 0.5, 0.75)) -> list[float]:
    order = np.argsort(v)
    v, w = v[order], w[order]
    cum = np.cumsum(w) / w.sum()
    return [float(v[np.searchsorted(cum, q)]) for q in qs]


def annual_rate(share_ewi: float, share_abroad: float, detection: float) -> pd.DataFrame:
    """Previously undocumented Mexicans granted LPR in FY2003 per unauthorized Mexican resident.

    Numerator: FY2003 Mexican LPRs x the NIS adult share who had entered without papers, less the share who
    came back on an immigrant visa (possibly living abroad, outside the US stock); the high variant divides
    by the item's detection rate in classes where every recipient had been unlawfully present. Applying the
    adult share to children is an assumption. Denominator: DHS January 2000 and 2005 stocks, interpolated.
    """
    (y0, s0), (y1, s1) = sorted(UNAUTHORIZED_MEXICO.items())
    stock = {when: (s0 + (s1 - s0) * (t - y0) / (y1 - y0)) * 1e3 for when, t in (("Jan 2003", 2003.0),
                                                                              ("Jul 2003", 2003.5))}
    total = YEARBOOK_MEXICO_2003["total"]
    rows = []
    for variant, share in (("survey share as measured", share_ewi),
                           ("corrected for overstays missed", share_ewi / detection)):
        num = total * share * (1 - share_abroad)
        for when, den in stock.items():
            rows.append({"numerator_variant": variant, "stock_date": when, "numerator": round(num),
                         "unauthorized_mexicans": round(den), "annual_rate": round(num / den, 4)})
    return pd.DataFrame(rows)


def main():
    p = build()
    rows = []
    groups = {"Mexico": p.mexico, "All other countries": ~p.mexico, "All": p.mexico | ~p.mexico}
    for name, m in groups.items():
        f = p[m & p.answered_any].copy()
        ewi = lambda x: wshare(x.entered_without_papers.to_numpy(float), x.w.to_numpy())
        adj = lambda x: wshare(x.adjusted.to_numpy(float), x.w.to_numpy())
        rows.append({"group": name, "n": int(m.sum()), "n_with_us_move_answered": len(f),
                     "share_entered_without_papers": round(ewi(f), 4),
                     "se": round(boot_se(f, ewi), 4),
                     "share_adjusted_inside_us": round(adj(p[m]), 4),
                     "weighted_thousands": round(p.w[m].sum() / 1e3, 1)})
    summary = pd.DataFrame(rows)

    mx = p[p.mexico & p.answered_any].copy()
    cat_rows = []
    for ewi_flag, sub in mx.groupby("entered_without_papers"):
        tot = sub.w.sum()
        for cat, g in sub.groupby("category"):
            cat_rows.append({"entered_without_papers": bool(ewi_flag), "category": cat, "n": len(g),
                             "share_of_group": round(g.w.sum() / tot, 4),
                             "share_adjusted_inside_us": round(wshare(g.adjusted.to_numpy(float),
                                                                      g.w.to_numpy()), 4)})
    # Within each category, what share of Mexican new LPRs had entered without papers.
    for cat, g in mx.groupby("category"):
        cat_rows.append({"entered_without_papers": "share_within_category", "category": cat, "n": len(g),
                         "share_of_group": round(wshare(g.entered_without_papers.to_numpy(float),
                                                        g.w.to_numpy()), 4),
                         "share_adjusted_inside_us": np.nan})
    cats = pd.DataFrame(cat_rows)

    wait_rows = []
    ewi_mx = mx[mx.entered_without_papers & mx.years_first_us_to_lpr.notna() & mx.first_no_papers_year.notna()]
    for name, g in [("all routes", ewi_mx)] + list(ewi_mx.groupby("category")):
        if len(g) < 20:
            continue
        yrs_first = wquantiles(g.years_first_us_to_lpr.to_numpy(float), g.w.to_numpy())
        yrs_ewi = wquantiles((g.admit_year - g.first_no_papers_year).to_numpy(float), g.w.to_numpy())
        wait_rows.append({"route": name, "n": len(g),
                          "years_first_us_move_to_lpr_p25_p50_p75": "/".join(f"{y:.0f}" for y in yrs_first),
                          "years_first_entry_without_papers_to_lpr_p25_p50_p75": "/".join(f"{y:.0f}" for y in yrs_ewi),
                          "share_adjusted_inside_us": round(wshare(g.adjusted.to_numpy(float), g.w.to_numpy()), 4)})
    waits = pd.DataFrame(wait_rows)

    ewi_all = mx[mx.entered_without_papers].copy()
    ewi_all["route_type"] = ewi_all.apply(route_type, axis=1)
    route_rows = []
    for rt, g in ewi_all.groupby("route_type"):
        share = lambda x, rt=rt: wshare(x.route_type.eq(rt).to_numpy(float), x.w.to_numpy())
        route_rows.append({"route_type": rt, "n": len(g), "share_of_mexican_lprs_who_entered_without_papers":
                           round(share(ewi_all), 4), "se": round(boot_se(ewi_all, share), 4)})
    routes = pd.DataFrame(route_rows).sort_values("share_of_mexican_lprs_who_entered_without_papers",
                                                   ascending=False)
    known = mx[mx.category.isin(["Legalization classes (W)", "Cancellation of removal or registry"])]
    detection = wshare(known.entered_without_papers.to_numpy(float), known.w.to_numpy())
    abroad = routes.set_index("route_type").loc["left and returned on an immigrant visa",
                                                "share_of_mexican_lprs_who_entered_without_papers"]
    rate = annual_rate(float(summary.set_index("group").loc["Mexico", "share_entered_without_papers"]),
                       float(abroad), detection)

    # Check the Mexican sample's class mix against the FY2003 administrative count (adults only in the NIS,
    # so children of citizens are under-represented; admissions May-November 2003 against FY2003).
    allmx = p[p.mexico]
    groups_yb = {"family preferences": {"Spouse of LPR", "Family fourth preference", "Other family preference"},
                 "employment": {"Employment"}, "spouses of US citizens": {"Spouse of US citizen"},
                 "children of US citizens": {"Child of US citizen"}, "parents of US citizens": {"Parent of US citizen"},
                 "cancellation of removal": {"Cancellation of removal or registry"}}
    check = pd.DataFrame([{"class": k, "nis_weighted_share": round(wshare(allmx.category.isin(v).to_numpy(float),
                                                                          allmx.w.to_numpy()), 4),
                           "yearbook_fy2003_share": round(YEARBOOK_MEXICO_2003[k] / YEARBOOK_MEXICO_2003["total"], 4)}
                          for k, v in groups_yb.items()])

    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    check.to_csv(out / "nis2003_mexico_vs_yearbook.csv", index=False)
    summary.to_csv(out / "nis2003_entered_without_papers.csv", index=False)
    cats.to_csv(out / "nis2003_mexico_route_by_entry.csv", index=False)
    waits.to_csv(out / "nis2003_mexico_years_to_green_card.csv", index=False)
    routes.to_csv(out / "nis2003_mexico_route_type.csv", index=False)
    rate.to_csv(out / "nis2003_mexico_annual_legalization_rate.csv", index=False)
    pd.set_option("display.width", 220)
    print("✓ codebook gate passed; Mexico weighted share matches the handout")
    print(check.to_string(index=False))
    print()
    print(summary.to_string(index=False))
    print()
    print(cats.to_string(index=False))
    print()
    print(waits.to_string(index=False))
    print()
    print(routes.to_string(index=False))
    print(f"\nitem detection among known-unauthorized classes: {detection:.3f}")
    print(rate.to_string(index=False))


if __name__ == "__main__":
    main()
