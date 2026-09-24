"""Render every computed specification as Markdown tables for RESULT.md (appendix), from derived/.

Writes derived/spec_tables.md. Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/vending_restaurants_2026_09_24/render_tables.py
"""
import pandas as pd

from lib import DERIVED


def pct(x: float) -> str:
    return "" if pd.isna(x) else f"{100 * x:+.1f}"


def se(x: float) -> str:
    return "" if pd.isna(x) else f"({100 * x:.1f})"


def p(x: float) -> str:
    return "" if pd.isna(x) else f"{x:.2f}"


def table(df: pd.DataFrame, cols: list, heads: list) -> str:
    out = ["| " + " | ".join(heads) + " |", "|" + "|".join("---" for _ in heads) + "|"]
    for _, r in df.iterrows():
        out.append("| " + " | ".join(str(f(r)) for f in cols) + " |")
    return "\n".join(out)


def pre_periods() -> str:
    """Every pre-2018 event-study coefficient (SE) for the headline specifications, one row each."""
    specs = [
        ("county_event_coefs.csv", dict(source="qcew", naics="7225", var="emp", pool="P1", weight="none"),
         "(a) QCEW 7225 employment, P1, unweighted"),
        ("county_event_coefs.csv", dict(source="cbp", naics="722511", var="emp", pool="P2", weight="none"),
         "(a) CBP full-service employment, P2, unweighted"),
        ("county_triple_coefs.csv", dict(naics="722511", var="estab", exposure="hisp_share", weight="none"),
         "(a2) full-service establishments, Hispanic share, unweighted"),
        ("county_triple_coefs.csv", dict(naics="722513", var="emp", exposure="hisp_share", weight="pop"),
         "(a2) limited-service employment, Hispanic share, pop-weighted"),
        ("zip_event_coefs.csv", dict(naics="722511", exposure="hisp_share", outcome="log_estab"),
         "(b) LA ZIPs full-service, Hispanic share"),
        ("zip_event_coefs.csv", dict(naics="722513", exposure="hisp_share", outcome="log_estab"),
         "(b) LA ZIPs limited-service, Hispanic share"),
        ("zip_event_coefs.csv", dict(naics="722511", exposure="arrests", outcome="log_estab"),
         "(b) City ZIPs full-service, arrests"),
        ("zip_event_coefs.csv", dict(naics="722511", exposure="arrests", outcome="estab_poisson"),
         "(b) City ZIPs full-service, arrests, Poisson"),
        ("sales_event_coefs.csv", dict(level="city", exposure="hisp_share", outcome="l_c08", weight="none"),
         "sales: LA County cities C08, unweighted"),
        ("sales_event_coefs.csv", dict(level="county", exposure="hisp_share", outcome="l_c08", weight="pop"),
         "sales: counties C08, pop-weighted"),
    ]
    years = list(range(2012, 2018))
    out = ["| specification | " + " | ".join(str(y) for y in years) + " |", "|---|" + "---|" * len(years)]
    for fname, keys, label in specs:
        d = pd.read_csv(DERIVED / fname, dtype={"naics": str})
        for k, v in keys.items():
            d = d[d[k].astype(str) == v]
        d = d.set_index("year")
        if d.empty or d.index.duplicated().any():
            raise SystemExit(f"[FAILED] pre-period rows for {label}: {len(d)} rows")
        cells = [f"{pct(d.loc[y, 'coef'])} {se(d.loc[y, 'se'])}" if y in d.index else "" for y in years]
        out.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(out)


def main() -> None:
    parts = ["### A0. Pre-period coefficients of the headline specifications\n\nLog points x 100 (SE), 2018 = 0; "
             "per 10 points of the share or per log point of arrests. QCEW starts in 2014 and CDTFA in 2015. "
             "Every other specification's pre-period coefficients are in the `derived/*_coefs.csv` files.\n",
             pre_periods(), "\n\n"]
    s = pd.read_csv(DERIVED / "county_event_summary.csv", dtype={"naics": str})
    parts.append("### A1. California against other states' counties (design a), every specification\n\n"
                 "Log points x 100 (about percent). b2019 is the 2019 coefficient with its county-clustered SE; "
                 "b2022-23 the mean of 2022 and 2023; pre p the joint test of 2012-2017 (QCEW 2014-2017); perm p "
                 "the placebo-state rank p-value (P1 only).\n")
    parts.append(table(s, [lambda r: r["source"], lambda r: r["naics"], lambda r: r["var"], lambda r: r["pool"],
                           lambda r: r["weight"], lambda r: f"{r['n_ca']}/{r['n_control']}",
                           lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}", lambda r: pct(r["b2020_21"]),
                           lambda r: pct(r["b2022_23"]), lambda r: p(r["p_pretrend"]),
                           lambda r: p(r.get("perm_p_b2019")), lambda r: p(r.get("perm_p_b2022_23"))],
                       ["source", "NAICS", "outcome", "pool", "weight", "CA/controls", "b2019 (SE)", "b2020-21",
                        "b2022-23", "pre p", "perm p 2019", "perm p 2022-23"]))
    t = pd.read_csv(DERIVED / "county_triple_summary.csv", dtype={"naics": str})
    parts.append("\n\n### A2. Triple difference (design a2), every specification\n\nPer 10 points of the exposure "
                 "share; state x year fixed effects.\n")
    parts.append(table(t, [lambda r: r["naics"], lambda r: r["var"], lambda r: r["exposure"], lambda r: r["weight"],
                           lambda r: f"{r['n_ca']}/{r['n_other']}", lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}",
                           lambda r: pct(r["b2020_21"]), lambda r: pct(r["b2022_23"]), lambda r: p(r["p_pretrend"])],
                       ["NAICS", "outcome", "exposure", "weight", "CA/other counties", "d2019 (SE)", "d2020-21",
                        "d2022-23", "pre p"]))
    tp = pd.read_csv(DERIVED / "triple_placebo_summary.csv", dtype={"naics": str})
    parts.append("\n\n### A3. Triple difference, California against placebo states (Hispanic share)\n\n"
                 "p10/p90 are the 10th and 90th percentiles of the same coefficient with each other state "
                 "(20+ counties) in California's place.\n")
    parts.append(table(tp, [lambda r: r["naics"], lambda r: r["var"], lambda r: r["weight"],
                            lambda r: r["placebo_states"], lambda r: pct(r["ca_d2019"]),
                            lambda r: f"{pct(r['placebo_p10_d2019'])} to {pct(r['placebo_p90_d2019'])}",
                            lambda r: p(r["perm_p_d2019"]), lambda r: pct(r["ca_d2022_23"]),
                            lambda r: f"{pct(r['placebo_p10_d2022_23'])} to {pct(r['placebo_p90_d2022_23'])}",
                            lambda r: p(r["perm_p_d2022_23"])],
                        ["NAICS", "outcome", "weight", "placebo states", "CA d2019", "placebo p10-p90",
                         "perm p", "CA d2022-23", "placebo p10-p90", "perm p"]))
    z = pd.read_csv(DERIVED / "zip_event_summary.csv", dtype={"naics": str})
    parts.append("\n\n### A4. Los Angeles County ZIPs (design b), every specification\n\nPer 10 points of the "
                 "share, or per log point of 2010-2016 LAPD vending arrests (City of LA ZIPs). The employment "
                 "index rows are invalid (size classes suppressed from 2017) and are shown only because they "
                 "were computed.\n")
    parts.append(table(z, [lambda r: r["naics"], lambda r: r["exposure"], lambda r: r["outcome"],
                           lambda r: r["n_zips"], lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}",
                           lambda r: pct(r["b2020_21"]), lambda r: pct(r["b2022_23"]), lambda r: p(r["p_pretrend"]),
                           lambda r: "invalid" if isinstance(r.get("note"), str) and r["note"] else ""],
                       ["NAICS", "exposure", "outcome", "ZIPs", "b2019 (SE)", "b2020-21", "b2022-23", "pre p",
                        "note"]))
    tr = pd.read_csv(DERIVED / "zip_trend_adjusted.csv", dtype={"naics": str})
    parts.append("\n\n### A4b. Los Angeles County ZIPs, trend-adjusted (added after the pre-trend tests failed)\n\n"
                 "Exposure x linear trend estimated on 2012-2018; dev = deviation from that trend.\n")
    parts.append(table(tr, [lambda r: r["naics"], lambda r: r["exposure"], lambda r: r["outcome"],
                            lambda r: r["n_zips"], lambda r: f"{pct(r['pre_trend_per_year'])} {se(r['pre_trend_se'])}",
                            lambda r: f"{pct(r['dev2019'])} {se(r['dev2019_se'])}",
                            lambda r: f"{pct(r['dev2022_23'])} ({100 * r['dev2022_se']:.1f}, {100 * r['dev2023_se']:.1f})"],
                        ["NAICS", "exposure", "outcome", "ZIPs", "pre-trend per year (SE)", "dev2019 (SE)",
                         "dev2022-23 (SE 2022, 2023)"]))
    dt = pd.read_csv(DERIVED / "zip_arrests_no_downtown.csv", dtype={"naics": str})
    parts.append("\n\n### A4c. City of LA ZIPs by 2010-2016 vending arrests, with and without downtown (added after "
                 "seeing results)\n\nPer log point of arrests. Downtown = ZCTAs 90012, 90013, 90014, 90015, 90017, "
                 "90021 (90071 is already out, under 1,000 residents). Implied = coefficient x sum over ZIPs of "
                 "exposure x 2018 establishments: establishments against an arrest-free ZIP.\n")
    parts.append(table(dt, [lambda r: r["naics"], lambda r: r["sample"], lambda r: r["outcome"],
                            lambda r: r["n_zips"], lambda r: r["estab_2018"],
                            lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}", lambda r: pct(r["b2022_23"]),
                            lambda r: p(r["p_pretrend"]), lambda r: f"{pct(r['dev2022_23'])}",
                            lambda r: f"{r['implied_estab_2019']:+.0f} ({r['implied_estab_2019_lo']:+.0f} to "
                                      f"{r['implied_estab_2019_hi']:+.0f})",
                            lambda r: f"{r['implied_estab_2022_23']:+.0f}"],
                        ["NAICS", "sample", "outcome", "ZIPs", "estab 2018", "b2019 (SE)", "b2022-23", "pre p",
                         "trend-adjusted dev2022-23", "implied estab 2019 (95%)", "implied estab 2022-23"]))
    try:
        zp = pd.read_csv(DERIVED / "zip_placebo_summary.csv", dtype={"naics": str})
        parts.append("\n\n### A5. ZIP design in placebo counties (same specification)\n")
        parts.append(table(zp, [lambda r: r["area"], lambda r: r["naics"], lambda r: r["exposure"],
                                lambda r: r["outcome"], lambda r: r["n_zips"],
                                lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}", lambda r: pct(r["b2022_23"]),
                                lambda r: pct(r["b2012"]), lambda r: p(r["p_pretrend"])],
                            ["county", "NAICS", "exposure", "outcome", "ZIPs", "b2019 (SE)", "b2022-23", "b2012",
                             "pre p"]))
    except FileNotFoundError:
        pass
    ss = pd.read_csv(DERIVED / "sales_event_summary.csv")
    parts.append("\n\n### A6. Taxable sales (CDTFA), every specification\n\nPer 10 points of the share. l_c08 food "
                 "services and drinking places; l_c04 food and beverage stores (placebo); l_diff their "
                 "difference; l_permits C08 seller's permits (cities: outlets) in Q4.\n")
    parts.append(table(ss, [lambda r: r["level"], lambda r: r["exposure"], lambda r: r["outcome"],
                            lambda r: r["weight"], lambda r: r["n_units"],
                            lambda r: f"{pct(r['b2019'])} {se(r['se2019'])}", lambda r: pct(r["b2020_21"]),
                            lambda r: pct(r["b2022_23"]), lambda r: pct(r["b2024_25"]), lambda r: p(r["p_pretrend"])],
                        ["level", "exposure", "outcome", "weight", "units", "b2019 (SE)", "b2020-21", "b2022-23",
                         "b2024-25", "pre p"]))
    (DERIVED / "spec_tables.md").write_text("\n".join(parts) + "\n")
    print("wrote derived/spec_tables.md")


if __name__ == "__main__":
    main()
