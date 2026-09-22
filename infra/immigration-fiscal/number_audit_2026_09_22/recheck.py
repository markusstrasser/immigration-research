"""Re-derive every MISMATCH / STALE value in AUDIT.md from the repo's source files.

Run from anywhere:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/number_audit_2026_09_22/recheck.py
Read-only. Prints quoted value against re-derived value for each flagged item.
"""
import csv
import sys
sys.dont_write_bytecode = True
import subprocess
from pathlib import Path

import pandas as pd

REPO = Path("/Users/alien/Projects/immigration-research")
R = REPO / "infra/immigration-fiscal"


def show(tag, quoted, derived):
    print(f"{tag:<34} quoted: {quoted:<34} re-derived: {derived}")


def elder_care():
    """FAQ:27, FAQ:233, FAQ:237, INDEX:69-70 — numerators must be foreign-born like the denominators."""
    lane = R / "mr_leads_papers_2026_09_21"
    sys.path.insert(0, str(lane))
    import elder_care_bound as e  # uses only derived/acs_care_inputs.csv for acs()
    t = e.acs()
    wa, ta = t("wa_pop_by_nativity"), t("wa_lowed_by_nativity", NATIVITY="2")
    cf, elderly = t("care_by_nativity", NATIVITY="2"), t("age65_by_gq_nativity", NATIVITY="1")
    pub = {(r["coefficient"], r["weighting"]): r for r in csv.DictReader(open(lane / "derived/elder_care_bound.csv"))}
    per_resident = float(pub[("preferred", "labour_share")]["medicaid_bn"]) * 1e9 / int(pub[("preferred", "labour_share")]["fewer_institutionalized"])
    out = {}
    for label, tm, cm in (("published", t("wa_lowed_mexico_born"), t("care_mexico_born")),
                          ("foreign-born only", t("wa_lowed_mexico_born", NATIVITY="2"), t("care_mexico_born", NATIVITY="2"))):
        share, mech = tm / wa, (cm / cf) / (tm / ta)
        bn = {(n, w): c * share * f * elderly * per_resident / 1e9
              for n, c in e.COEFFICIENTS.items() for w, f in (("labour_share", 1.0), ("care_workforce", mech))}
        out[label] = (cm / cf, tm / ta, min(bn.values()), max(bn.values()), bn[("preferred", "care_workforce")])
    p, f = out["published"], out["foreign-born only"]
    show("FAQ:233 care-worker share", f"14.9% (script {p[0]:.1%})", f"{f[0]:.1%}")
    show("FAQ:234 treatment share", f"38.5% (script {p[1]:.1%})", f"{f[1]:.1%}")
    show("FAQ:237/INDEX:69 bound $bn", f"2.3–14.9 (script {p[2]:.2f}–{p[3]:.2f})", f"{f[2]:.2f}–{f[3]:.2f}")
    show("FAQ:237/INDEX:70 preferred $bn", f"5.8 (script {p[4]:.2f})", f"{f[4]:.2f}")


def institutions_by_age():
    """FAQ:195 — under-65 institutional cost change when the union takes white ages (shared)."""
    d = R / "ledger_absolute_2026_09_17/derived"
    c, p = pd.read_csv(d / "age_profile_components.csv"), pd.read_csv(d / "age_profiles.csv")
    s = c[(c.allocation == "shared") & (c.account == "expanded") & (c.component == "N")]
    pp = p[(p.allocation == "shared") & (p.account == "expanded")]
    m = s[s.group == "mexican_observed_total"].set_index("band").signed_total
    mp = pp[pp.group == "mexican_observed_total"].set_index("band").population
    wp = pp[pp.group == "third_plus_nh_white"].set_index("band").population
    change = (m / mp * wp / wp.sum() * mp.sum() - m) / 1e9  # negative = cost rises
    show("FAQ:195 under-65 cost falls", "$1.4bn", f"${change[change.index < 6].sum():.2f}bn")
    show("FAQ:195 65+ nursing rises", "$9.2bn", f"${-change[change.index >= 6].sum():.2f}bn")


def attriters():
    """FAQ:98, INDEX:201 — attriter adjustment on the Sept 17 all-age base vs the Sept 19 ledger."""
    a = pd.read_csv(R / "mexican_origin_population_total_2026_09_19/derived/arm5_fiscal_implication.csv")
    row = a[a.population_assumption.str.startswith("4th-plus identifies at the measured")
            & a.attriter_characteristics.str.startswith("Duncan-Trejo")].iloc[0]
    g = pd.read_csv(R / "ledger_absolute_2026_09_17/derived/complete_gaps.csv")
    r = g[g.reference == "third_plus_nh_white"].set_index("group").complete_common_age_gap_per_person
    base, g3 = r["mexican_observed_total"], r["mexican_third_plus_selfid"]
    factor = 1 - 0.76 / (14.384 - 13.335)  # education gap closed by attriters, arm5_education_selectivity.csv
    pop, added = row.population_before, row.attriters_added
    new = (base * pop + added * g3 * factor) / (pop + added)
    show("FAQ:98/INDEX:201 lane value", "−6,864", f"{row.gap_per_person_after:,.0f} on base {row.gap_per_person_before:,.0f} (Sept 17 all-age ledger)")
    show("FAQ:98/INDEX:201 Sept 19 ledger", "—", f"{new:,.0f} on base {base:,.0f}")
    show("INDEX:228 Sept 19 G2 same-age gap", "−$8.3k to −$8.9k (Sept 16)", f"{r['mexican_second_gen']:,.0f}")


def nest():
    """FAQ:256, INDEX:50 — headline move at eps=3 against the direct estimates of ladder 181."""
    n = pd.read_csv(R / "production_nativity_nest_2026_09_22/derived/nest_headline.csv")
    a = n[(n.nest_option == "A_by_nativity") & (n.split == "hs_or_less")]
    v = {(x.normalization, float(x.sigma_NI)): x.private_plus_receipts_bn for x in a.itertuples()}
    s = pd.read_csv(R / "full_account_2026_09_20/derived/service_response_summary.csv").set_index("profile")
    lo, hi = -s.loc["cbo_category_lag_non_school_full", "max_welfare_bn"], -s.loc["cbo_category_lag_non_school_full", "min_welfare_bn"]
    for eps in (3.0, 8.7, 17.9):
        dg, dc = v[("gdp", eps)] - v[("gdp", float("inf"))], v[("cash", eps)] - v[("cash", float("inf"))]
        show(f"FAQ:256/INDEX:50 eps={eps}", "$9–14bn; band $151–188bn" if eps == 3 else "(not quoted)",
             f"move {dc:.1f}–{dg:.1f}bn; band {lo - dg:.0f}–{hi - dc:.0f}bn")


def index_table_rows():
    """INDEX:242, 243, 277 — worker C's items."""
    d = pd.read_csv(R / "housing_supply_ca_tx_2026_09_22/derived/state_supply.csv")
    p = d.pivot(index="year", columns="name", values="permits_per_1000_residents")
    ratio = p["Texas"] / p["California"]
    show("INDEX:242 TX/CA permits", "2.2–2.5× every year",
         f"annual {ratio.min():.2f}–{ratio.max():.2f}; period mean {p['Texas'].mean() / p['California'].mean():.2f}; mean of annual {ratio.mean():.2f}")
    m = pd.read_csv(R / "housing_supply_ca_tx_2026_09_22/derived/metro_regressions.csv")
    for x in m[m.term == "d_mex_share_pp"].itertuples():
        show(f"INDEX:242 metro {x.spec}", "+0.030 on 168 metros", f"{x.coef:+.4f} on n={x.n}")
    e = pd.read_csv(R / "housing_causal_2000_2010_2026_09_22/derived/estimates.csv").set_index(["outcome", "estimator"])
    for o in ("dlog_rent", "dlog_value"):
        show(f"INDEX:243 settlement/ancestry {o}", "2–5×",
             f"{e.loc[(o, 'IV with Z'), 'coef'] / e.loc[(o, 'IV with Z2'), 'coef']:.1f}×")
    reg = subprocess.run(["git", "-C", str(REPO), "show", "HEAD:research/immigration-dataset-register.md"],
                         capture_output=True, text=True).stdout
    show("INDEX:277 roadmap", "12 datasets we don't have",
         f"register mentions {[k for k in ('SCAAP', 'Light/He/Robey', 'SPI2016', 'USSC 2024') if k in reg]}")


if __name__ == "__main__":
    for step in (elder_care, institutions_by_age, attriters, nest, index_table_rows):
        print(f"--- {step.__name__}")
        step()
