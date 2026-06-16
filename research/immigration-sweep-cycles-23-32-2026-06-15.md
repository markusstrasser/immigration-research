# Sweep cycles 23–32 — full protocol (2026-06-15)

**Protocol:** `notes/immigration-lifetime-sweep-protocol.md`

**Status update (2026-06-16):** Partially superseded. The NAS education-mix and federal annual proxy pieces remain useful, but the origin `school_burden_per_adult` and `net_crude` rows exported in cycles 24, 26, 30, and 32 are historical intermediate outputs. The live `v_three_layer_annual` view now withholds origin school/net rows because those rows paired a scenario-household school numerator with full-microsim adult denominators. Query run 2026-06-16 returned `NULL` school/net rows for `mexico_origin`, `mx_ca_cluster`, `eu27_origin`, `uk_origin`, and `fb_lt_hs`; `nh_white_usborn` school/net remains built. [SOURCE: `warehouse/immigration_fiscal_union.duckdb` view `v_three_layer_annual`] [SOURCE: `research/immigration-school-burden-per-adult-2026-06-15.md`]

Each cycle: diverge → acquire/mine → rebuild → analyze → synthesize.

---

## Cycle 23 — NAS Table 8-13 college+ NPV cells

**Diverge:** Without college+ NAS cells, EU/white lifetime blocked — extract from PDF.

**Paper:** `external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf` — excerpt: _The Economic and Fiscal Consequences of Immigration  PREPUBLICATION COPY, UNCORRECTED PROOFS  among the first generation. Another aspect here that mirrors patterns in earnings is the compression of the educational gradient within the first generation. Gradients across educational groups within the third-plus generation are arguably most interesting here. The largest differences between groups in t…_

**Mined claims:** `.mining/immigration-lifetime-sweep-23-nas-table-8-13.json`

**Rebuild:** lifetime, tensor

**Data:**
```json
[
  {
    "population_group": "fb_lt_hs",
    "npv": -109000.0,
    "fed": 677.0
  },
  {
    "population_group": "mx_ca_cluster",
    "npv": 42972.0,
    "fed": 1519.0
  },
  {
    "population_group": "mexico_origin",
    "npv": 45631.0,
    "fed": 1519.0
  },
  {
    "population_group": "us_foreign_born_stock",
    "npv": 212535.0,
    "fed": 3003.0
  }
]
```

**Synthesis:** Lifetime NPV now spans all education buckets; Mexico sign may flip positive on full mix [check data].

---

## Cycle 24 — Orrenius static school cost critique

**Diverge:** Static school burden overstates cost if descendant taxes omitted.

**Paper:** `external/lifetime/dallasfed/orrenius_nas_fiscal_sensitivity_wp1704.pdf` — excerpt: _New Findings on the Fiscal Impact of Immigration in the United States  Pia Orrenius  Federal Reserve Bank of Dallas Research Department Working Paper 1704  New Findings on the Fiscal Impact of Immigration in the United States *  Pia Orrenius Federal Reserve Bank of Dallas 2200 N. Pearl St. Dallas, TX 75201 214-922-5747 Pia.Orrenius@dal.frb.org  April 2017  Abstract The National Academies of Scien…_

**Data:** Historical intermediate output; do not cite as the current origin school/net surface.
```json
[
  {
    "population_group": "mexico_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 771.0,
    "crude": 748.0
  },
  {
    "population_group": "nh_white_usborn",
    "school": 6024.0,
    "crude": -3277.0
  }
]
```

**Synthesis:** Superseded for origin school/net exports. Static school-cost critique remains relevant, but current origin rows are withheld pending a same-universe school numerator.

---

## Cycle 25 — Return-migration horizon haircut

**Diverge:** Duleep-Regets selective exit shortens effective NAS horizon for LDC cells.

**Paper:** `external/lifetime/iza/iza_dp631_duleep_regets_immigrant_quality_human_capital.pdf` — excerpt: _DISCUSSION PAPER SERIES  IZA DP No. 631  The Elusive Concept of Immigrant Quality: Evidence from 1970-1990 Harriet Orcutt Duleep Mark C. Regets  November 2002  Forschungsinstitut zur Zukunft der Arbeit Institute for the Study of Labor  The Elusive Concept of Immigrant Quality: Evidence from 1970-1990 Harriet Orcutt Duleep Urban Institute, Social Security Administration and IZA Bonn  Mark C. Reget…_

**Mined claims:** `.mining/immigration-lifetime-sweep-25-return-haircut.json`

**Rebuild:** lifetime

**Data:**
```json
[
  {
    "scenario_id": "baseline_no_haircut",
    "npv_horizon_multiplier": "1.00",
    "notes": "Full 75yr NAS horizon"
  },
  {
    "scenario_id": "ldc_selective_emigration",
    "npv_horizon_multiplier": "0.75",
    "notes": "Duleep-Regets: LDC inverse growth; shorten effective years 25% [INFERENCE]"
  },
  {
    "scenario_id": "mexico_central_america",
    "npv_horizon_multiplier": "0.70",
    "notes": "IZA dp631 Central/South Am +19.9pp growth per $1k entry \u2014 exit bias [SOURCE: cluster I]"
  },
  {
    "scenario_id": "high_skill_low_exit",
    "npv_horizon_multiplier": "1.00",
    "notes": "EU/India corridor \u2014 low return probability [INFERENCE]"
  }
]
```

**Synthesis:** Query returned 4 rows; see data block.

---

## Cycle 26 — School burden microsim adult weights

**Diverge:** Scenario adult N was PUMA subset — use microsim adults for kids/adult.

**Rebuild:** tensor

**Data:** Historical intermediate output; origin and aggregate foreign-born school/net rows below are not live after the same-universe guard.
```json
[
  {
    "population_group": "nh_white_fborn",
    "school": 6537.0,
    "fed": 3898.0,
    "net": -3534.0
  },
  {
    "population_group": "nh_white_all",
    "school": 6055.0,
    "fed": 2803.0,
    "net": -3293.0
  },
  {
    "population_group": "nh_white_usborn",
    "school": 6024.0,
    "fed": 2746.0,
    "net": -3277.0
  },
  {
    "population_group": "fb_lt_hs",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 1005.0,
    "fed": 677.0,
    "net": -329.0
  },
  {
    "population_group": "mx_ca_cluster",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 1091.0,
    "fed": 1519.0,
    "net": 428.0
  },
  {
    "population_group": "mexico_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 771.0,
    "fed": 1519.0,
    "net": 748.0
  },
  {
    "population_group": "eu27_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 64.0,
    "fed": 4695.0,
    "net": 4658.0
  },
  {
    "population_group": "uk_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "school": 92.0,
    "fed": 5486.0,
    "net": 5372.0
  }
]
```

**Synthesis:** Superseded. The `$771` Mexico school/adult and `+$748` crude net rows paired a scenario-household school numerator with the full Mexico microsim adult denominator. Current conclusion: Mexico federal annual proxy remains about `$1,519/adult/yr`; Mexico school/adult and `federal - school` are withheld.

---

## Cycle 27 — FB <HS school burden row

**Diverge:** Low-skill pool school burden was NULL — fill from origin-weighted per_pupil×kids.

**Rebuild:** tensor

**Data:** Historical intermediate output; the aggregate foreign-born `<HS` school/net row below is not live after the same-universe guard.
```json
[
  {
    "population_group": "fb_lt_hs",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "federal_per_adult": 676.7904040735388,
    "school_per_adult": 1004.8071554499852,
    "net_crude_per_adult": -329.492597700376,
    "weight_adults": 7686859.0
  }
]
```

**Synthesis:** Query returned 1 rows; see data block.

---

## Cycle 28 — LPR Mexico class weights

**Diverge:** Dynamic Razin weights need structured LPR xlsx parse.

**Rebuild:** tensor

**Data:**
```json
[
  {
    "raw_row": "[UNVERIFIED: LPR xlsx missing]",
    "row_sum": null
  }
]
```

**Synthesis:** Query returned 1 rows; see data block.

---

## Cycle 29 — Akers-Boustan native child mobility

**Diverge:** Descendant fiscal attribution — native HS completion in immigrant cities.

**Paper:** `external/lifetime/nber/akers_boustan_2024_immigration_inequality_next_generation_w33961.pdf` — excerpt: _NBER WORKING PAPER SERIES  IMMIGRATION AND INEQUALITY IN THE NEXT GENERATION Mark Borgschulte Heepyung Cho Darren Lubotsky Jonathan L. Rothbaum Working Paper 33961 http://www.nber.org/papers/w33961  NATIONAL BUREAU OF ECONOMIC RESEARCH 1050 Massachusetts Avenue Cambridge, MA 02138 June 2025  We thank David Card, Ronald Lee, and Giovanni Peri, as well as audiences and discussants at NBER Cohort Stu…_

**Data:** Historical intermediate output; origin `base` and marginal rows below depend on the superseded school/net export.
```json
[]
```

**Synthesis:** Query returned 0 rows; see data block.

---

## Cycle 30 — Marginal vs average pupil (NAS congestible)

**Diverge:** NAS treats K-12 as congestible not pure public good — average cost upper bound.

**Paper:** `external/lifetime/nas/nas_2017_immigration_economic_fiscal_full.pdf` — excerpt: _The Economic and Fiscal Consequences of Immigration  PREPUBLICATION COPY, UNCORRECTED PROOFS  Readers will note that the figures in Table 8-1 translate into quite large fiscal shortfalls overall—the fiscal ratio (Receipts/Outlays columns) falls well below 1.0 for all three groups. For 2013, the 55.5 million first generation independent persons and their dependents, 23.3 million second generation i…_

**Data:**
```json
[
  {
    "population_group": "eu27_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "base": 4658.0,
    "half_marg": 4663.0
  },
  {
    "population_group": "mexico_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "base": 748.0,
    "half_marg": 1134.0
  },
  {
    "population_group": "nh_white_usborn",
    "base": -3277.0,
    "half_marg": -265.0
  }
]
```

**Synthesis:** Superseded for origin rows. Marginal-vs-average pupil costing remains a required sensitivity after a same-universe origin school row exists; it cannot rescue the stale `$771/+748` export.

---

## Cycle 31 — Saiz elasticity × school PUMA

**Diverge:** High school burden origins may land in inelastic-rent metros.

**Data:**
```json
[
  {
    "med_eps": 2.54,
    "n": 269
  }
]
```

**Synthesis:** Query returned 1 rows; see data block.

---

## Cycle 32 — Converge — three-layer + lifetime thesis

**Diverge:** Integrate sweeps 23–31 into revised thesis.

**Data:** Historical intermediate output for origin school/net rows; live 2026-06-16 `v_three_layer_annual` withholds `school` and `crude` for `eu27_origin`, `fb_lt_hs`, and `mexico_origin`.
```json
[
  {
    "population_group": "eu27_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "fed": 4695.0,
    "school": 64.0,
    "crude": 4658.0,
    "npv": null
  },
  {
    "population_group": "fb_lt_hs",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "fed": 677.0,
    "school": 1005.0,
    "crude": -329.0,
    "npv": -109000.0
  },
  {
    "population_group": "mexico_origin",
    "status": "superseded_do_not_cite_same_universe_mismatch",
    "fed": 1519.0,
    "school": 771.0,
    "crude": 748.0,
    "npv": 45631.0
  },
  {
    "population_group": "nh_white_usborn",
    "fed": 2746.0,
    "school": 6024.0,
    "crude": -3277.0,
    "npv": null
  }
]
```

**Synthesis:** Final object: federal_annual | school_burden_per_adult | net_crude | lifetime_npv — never one scalar. Current live export has `federal_annual` and synthetic NAS `lifetime_npv` for the relevant groups, but origin `school_burden_per_adult` and `net_crude` are withheld until the numerator and denominator use the same universe.

---

## Revisions

| Date | Change | Trigger |
|---|---|---|
| 2026-06-16 | Marked cycles 24, 26, 30, and 32 school/net rows as historical superseded outputs; current origin school/net rows are withheld by `v_three_layer_annual`. | DuckDB query on `warehouse/immigration_fiscal_union.duckdb` and `research/immigration-school-burden-per-adult-2026-06-15.md`. |
