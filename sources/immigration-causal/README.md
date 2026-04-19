# immigration-causal — reproducible analysis bundle

This directory contains the data acquisition + analysis pipeline behind the
April 2026 "immigration causal" research cycle in
`research/immigration-causal-*`. Everything here is meant to be reproduced from
scratch by an outside reader.

## What this cycle does

Five mini-investigations sharing the same panel infrastructure:

1. **Card vs Borjas (E-Verify wages).** TWFE on QWI state × industry × education
   panel, 2003-2023. Test whether tighter unauthorized labor supply (E-Verify
   mandates) raises native low-skill wages (Borjas) or has null/negative effect
   (Card). Companion regression on employment quantities to separate the two
   margins. Scripts: `analyze_everify_wages.py`, `analyze_everify_employment.py`.

2. **Saiz × rent.** Merge Saiz (2010, QJE) MSA housing-supply elasticities with
   ACS 2022 median rent and foreign-born share. Tests whether immigrant rent
   burden concentrates in inelastic MSAs. Decomposes elasticity into
   topography (`unaval`) vs regulation (`WRLURI`) channels to determine
   whether zoning reform is a viable lever. Scripts:
   `merge_saiz_rent_immigrant.py`, `saiz_decomposition.py`.

3. **Sanctuary DiD.** Two-sided design — pro-sanctuary states (CA, IL, OR…) vs
   anti-sanctuary states (TX SB 4, FL SB 168, AL HB 56, AZ SB 1070…) on QWI
   wages. Cross-checks the E-Verify wage finding via a different policy axis.
   Script: `analyze_sanctuary_wages.py`. Sanctuary panel hand-compiled from
   primary legal sources (state codes, executive orders) — see MANIFEST.

4. **Mass-deportation calibration.** Partial-equilibrium industry-by-industry
   shock from 100% removal of unauthorized workers. Uses BEA Use Tables (labor
   share, output) × Pew/CMS unauthorized employment shares × literature labor
   demand elasticities (-0.3 to -0.5). Order-of-magnitude bounds, not a
   forecast. Script: `mass_deportation_sim.py`.

5. **Open-borders sensitivity.** Clemens (2011) Place Premium parameters into a
   scenario table: world stocks, rich-quartile absorption capacity, transition
   horizons. The script does the arithmetic; the binding-constraint reasoning
   lives in the memo. Script: `open_borders_baseline.py`.

6. **(Cross-cut) Internal vs immigrant newcomers.** IRS SOI county inflow
   (native US filers) joined to ACS B05005 (recent foreign-born) so the
   reader can ask "is the policy-relevant unit the immigrant or the newcomer
   in general?" Script: `analyze_internal_vs_immigrant_newcomers.py`.

Findings memos summarising results live under
`../../research/immigration-causal-*.md`. The verdicts there cite the analysis
parquets/CSVs that this pipeline produces in `data/analysis/`.

## Quickstart

```bash
# 1. clone the parent research repo, then:
cd sources/immigration-causal

# 2. acquire all external datasets (~50 MB total)
bash setup.sh

# 3. run the analysis pipeline end-to-end
bash run_all.sh
```

Outputs land in `data/analysis/` (parquet, CSV, JSON, plain-text logs).

## Requirements

- **Python 3.11+**
- **uv** (https://github.com/astral-sh/uv) — every script is invoked via
  `uv run --with <deps> python3 …` so dependencies are resolved per script;
  no `pip install` step needed.
- **Disk:** ~50 MB raw data, ~5 MB analysis outputs.
- **Network:** scripts hit
  - `api.census.gov` (ACS 1-yr, 5-yr; QWI timeseries) — no API key required
    for the volumes used here (well below the 500 calls/day anonymous limit)
  - `apps.bea.gov` (BEA Supply-Use tables, public)
  - `irs.gov` (SOI county inflow/outflow CSVs, public)
  - `web.mit.edu` (Saiz 2010 MSA elasticity .dta, hosted on Albert Saiz's
    MIT Urban Economics Lab page)

  No authenticated APIs. Run from a network that doesn't block these hosts.

## Data acquisition order

`setup.sh` fetches in this order; each step is independent:

1. Saiz 2010 MSA elasticity (.dta) → `data/saiz/`
2. BEA Supply-Use Summary 1997-2023 (.xlsx, in AllTablesSUP.zip) → `data/bea_io/`
3. IRS SOI county inflow + outflow 2022-23 (.csv) → `data/internal_migration/`
4. Clemens (2011, JEP) Place Premium PDF → `data/clemens/`  *(reference only)*
5. WRLURI 2018 → **SKIPPED**: the canonical Wharton link
   (`real-estate.wharton.upenn.edu/wp-content/uploads/2024/.../WRLURI-2018.zip`)
   has been intermittently dead since early 2025. The Saiz 2010 .dta already
   ships with `WRLURI` and `unaval` columns from the original 2008 build, which
   is what `saiz_decomposition.py` actually uses. The 2018 refresh is desirable
   for sensitivity but not required.

The QWI state panel and ACS state-level immigrant share are fetched live by the
analysis scripts themselves (`pull_qwi_state_panel.py`,
`pull_acs_state_immigrant_share.py`) on first run. They cache as parquet under
`data/lehd/`. The QWI pull takes ~5-10 minutes (36 batched API calls).

The hand-compiled `everify_state_mandates.csv` and `sanctuary_state_panel.csv`
ship with the repo (small, source-cited in MANIFEST.md). They are not
re-acquired by `setup.sh`.

## Layout

```
scripts/                     analysis + acquisition Python
data/                        gitignored; populated by setup.sh + run_all.sh
  saiz/                      Saiz 2010 MSA elasticity (.dta)
  bea_io/                    BEA Use/Supply tables (.xlsx)
  lehd/                      QWI state panel + ACS state immigrant share
  everify/                   hand-compiled E-Verify mandate panel (in repo)
  sanctuary/                 hand-compiled sanctuary state panel (in repo)
  internal_migration/        IRS SOI county inflow/outflow
  clemens/                   Clemens 2011 PDF + open-borders calibration JSON
  daca/                      DACA timeline notes (in repo)
  wrluri/                    intentionally empty — see MANIFEST gotcha
  foged_peri/                placeholder for future Foged-Peri replication
  analysis/                  outputs from run_all.sh
MANIFEST.md                  per-dataset provenance + checksums
setup.sh                     re-acquire all external data
run_all.sh                   run analysis pipeline in dependency order
```

## Reproducibility caveats

- ACS API 2020 1-yr was withdrawn (COVID). The puller skips that year.
- QWI release cadence: cells are refreshed quarterly; numbers will shift
  slightly across vintages. This snapshot is dated 2026-04-18.
- Census API will return HTTP 200 with empty JSON if you exceed the daily
  anonymous quota — re-run the puller with an API key
  (`CENSUS_API_KEY` env var, free) if you hit this.
- All hand-compiled panels (E-Verify, sanctuary) document their primary
  sources in MANIFEST.md. They are append-only; corrections add a row, not
  edit one.

## Licence / attribution

Code: same licence as parent repo. Data: each dataset retains its source
licence (see MANIFEST.md). Memos in `research/` are author-owned analysis;
attribute as "Strasser, immigration-causal cycle 2026-04-18" if cited.

<!-- knowledge-index
generated: 2026-04-19T04:19:20Z
hash: 3ad1a955a1ff

cross_refs: research/immigration-causal-*.md

end-knowledge-index -->
