#!/usr/bin/env python3
"""Re-grade load-bearing immigration sources by source-incentive / against-interest credibility.

Operationalizes generator G-LIF-U01. SYMMETRIC by construction: down-weights advocacy
that confirms its own prior on BOTH sides; up-weights findings that cut AGAINST the
source's prior on both sides. Builds `source_incentive_grades` in the lifetime warehouse
(redistributable aggregate → flows into the unified release) + a derived CSV.

Rubric:
  base_weight by outlet  : govt_nonpartisan 1.0 | academic 0.8 | think_tank 0.6 | advocacy 0.4
  against_interest       : restrictionist source → benefit finding, OR expansionist → cost finding
  with_interest_advocacy : advocacy outlet whose finding confirms its own prior
  adj_weight = min(1.0, base × (1.5 if against_interest else 0.7 if with_interest_advocacy else 1.0))

Run: uv run --with duckdb,pandas python build_source_incentive_grades.py
"""
from __future__ import annotations

import sys

from paths import derived_root, lifetime_duckdb_path

BASE = {"govt_nonpartisan": 1.0, "academic": 0.8, "think_tank": 0.6,
        "advocacy_restrictionist": 0.4, "advocacy_expansionist": 0.4}

# (key, label, outlet, prior_lean, finding_direction, headline_role)
# prior_lean ∈ {restrictionist, expansionist, neutral}; finding ∈ {cost, benefit, neutral, mixed}
SOURCES = [
    ("nas_2017", "NAS 2016/17 fiscal panel", "govt_nonpartisan", "neutral", "mixed",
     "<HS lifetime fiscal NEGATIVE; 2nd-gen strongly POSITIVE — establishment panel publishing both"),
    ("cbo_60569", "CBO federal (surge cut deficit)", "govt_nonpartisan", "neutral", "benefit",
     "federal side positive over 2024-34"),
    ("cbo_61256", "CBO state-local cost", "govt_nonpartisan", "neutral", "cost",
     "direct net state/local cost ~-$2,140/person"),
    ("census_pew_stock", "Census/Pew unauthorized stock", "think_tank", "neutral", "neutral",
     "denominator; descriptive"),
    ("borjas_surplus", "Borjas — immigration surplus +", "academic", "restrictionist", "benefit",
     "aggregate native surplus POSITIVE — derived by the field's leading skeptic"),
    ("borjas_wage", "Borjas — low-skill wage harm", "academic", "restrictionist", "cost",
     "national skill-cell wage depression (with-interest, standard weight)"),
    ("nas_2nd_gen", "NAS — 2nd-generation contribution", "govt_nonpartisan", "neutral", "benefit",
     "descendants among top net contributors"),
    ("card_peri", "Card/Peri — small wage effect", "academic", "expansionist", "benefit",
     "local + capital + native-migration washout (with-interest)"),
    ("clemens_2023", "Clemens — capital-tax flip", "academic", "expansionist", "benefit",
     "<HS NPV -$109k→+$128k under capital-tax GE (with-interest; methodological)"),
    ("colas_sachs", "Colas-Sachs — indirect benefits", "academic", "expansionist", "benefit",
     "indirect fiscal benefits of low-skill (with-interest)"),
    ("cortes_2008", "Cortes — consumer price benefit", "academic", "expansionist", "benefit",
     "lower non-traded service prices (with-interest)"),
    ("ajkm_2022", "Azoulay et al — immigrant founders", "academic", "expansionist", "benefit",
     "net job creators (with-interest)"),
    ("ottaviano_peri", "Ottaviano-Peri — GE wage", "academic", "expansionist", "benefit",
     "imperfect substitution + capital → small/positive (with-interest)"),
    ("storesletten_2000", "Storesletten — selective fiscal", "academic", "neutral", "mixed",
     "fiscal sign depends on selection/age-at-arrival"),
    ("orrenius_nas", "Orrenius — NAS sensitivity", "academic", "neutral", "mixed",
     "dual-scenario marginal-cost sensitivity"),
    ("razin_wahba", "Razin-Wahba — fiscal leakage", "academic", "restrictionist", "cost",
     "welfare-state fiscal burden of low-skill (with-interest)"),
    ("itep_2024", "ITEP — immigrants pay $X tax", "advocacy_expansionist", "expansionist", "benefit",
     "the 'net contributor' benefit headline — with-interest advocacy"),
    ("cato_benefits", "Cato — immigration benefits", "advocacy_expansionist", "expansionist", "benefit",
     "libertarian benefit case — with-interest advocacy"),
    ("fair_cost", "FAIR — high fiscal cost", "advocacy_restrictionist", "restrictionist", "cost",
     "the high-cost restrictionist headline — with-interest advocacy"),
    ("cis_camarota", "CIS/Camarota — welfare use cost", "advocacy_restrictionist", "restrictionist", "cost",
     "restrictionist welfare-use cost — with-interest advocacy"),
]


def _grade(outlet, prior, finding):
    against = (prior == "restrictionist" and finding == "benefit") or \
              (prior == "expansionist" and finding == "cost")
    with_adv = outlet.startswith("advocacy") and (
        (prior == "restrictionist" and finding == "cost") or
        (prior == "expansionist" and finding == "benefit"))
    mult = 1.5 if against else (0.7 if with_adv else 1.0)
    adj = min(1.0, round(BASE[outlet] * mult, 3))
    return against, with_adv, BASE[outlet], mult, adj


def build() -> None:
    try:
        import duckdb
        import pandas as pd
    except ImportError:
        sys.exit("need duckdb+pandas — run via: uv run --with duckdb,pandas python build_source_incentive_grades.py")

    rows = []
    for key, label, outlet, prior, finding, role in SOURCES:
        against, with_adv, base, mult, adj = _grade(outlet, prior, finding)
        rows.append({
            "source_key": key, "label": label, "outlet_type": outlet,
            "prior_lean": prior, "finding_direction": finding,
            "against_interest": against, "with_interest_advocacy": with_adv,
            "base_weight": base, "multiplier": mult, "adj_weight": adj,
            "headline_role": role,
        })
    df = pd.DataFrame(rows).sort_values("adj_weight", ascending=False).reset_index(drop=True)

    db = lifetime_duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — run reproduce.sh build lifetime first")
    con = duckdb.connect(str(db))
    con.register("_g", df)
    con.execute("CREATE OR REPLACE TABLE source_incentive_grades AS SELECT * FROM _g")

    out = derived_root() / "lifetime" / "source_incentive_grades.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    con.execute(f"COPY source_incentive_grades TO '{out}' (HEADER)")

    # symmetry check (G-LIF-U01 theory): adj_weight should not correlate with cost/benefit direction
    cost = con.execute("SELECT avg(adj_weight) FROM source_incentive_grades WHERE finding_direction='cost'").fetchone()[0]
    ben = con.execute("SELECT avg(adj_weight) FROM source_incentive_grades WHERE finding_direction='benefit'").fetchone()[0]
    con.close()

    print(f"  ✓ source_incentive_grades: {len(df)} sources graded → {out}")
    print("  most credible (up-weighted, against-interest + nonpartisan):")
    for _, r in df.head(7).iterrows():
        flag = "↑against-interest" if r.against_interest else ""
        print(f"    {r.adj_weight:>4}  {r.label:<34} [{r.finding_direction}] {flag}")
    print("  deflated (with-interest advocacy, BOTH sides):")
    for _, r in df[df.with_interest_advocacy].iterrows():
        print(f"    {r.adj_weight:>4}  {r.label:<34} [{r.finding_direction}]")
    print(f"  symmetry check — mean adj_weight: cost={cost:.2f}  benefit={ben:.2f}  "
          f"(close ⇒ rule is not tilted toward a prior)")


if __name__ == "__main__":
    build()
