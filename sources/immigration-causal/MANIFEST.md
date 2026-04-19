# Data manifest — immigration-causal

Per-dataset provenance, retrieval date, size, SHA256, licence, and gotchas.
All retrieval dates are **2026-04-18** unless noted.

`data/` is gitignored. Re-acquire with `bash setup.sh`. Hand-compiled CSVs
under `data/everify/` and `data/sanctuary/` are checked into git separately
(or shipped alongside this manifest) because they cannot be downloaded.

## External datasets (re-acquired by setup.sh)

| # | Dataset | Source URL | Path | Bytes | SHA256 | Licence | Retrieved |
|---|---------|------------|------|-------|--------|---------|-----------|
| 1 | Saiz 2010 MSA housing supply elasticity | https://web.mit.edu/asaiz/www/data/saiz_2010_msa_elasticity.dta (MIT Urban Economics Lab; mirrored from Saiz 2010 QJE replication archive) | `data/saiz/saiz_2010_msa_elasticity.dta` | 32 800 | `8699efc85e76322494b804d9695727c0f6bd916a6a80ef2341e537c9a8520807` | Author-distributed (academic use; cite Saiz 2010 QJE) | 2026-04-18 |
| 2 | BEA Supply-Use Framework, Summary, 1997-2023 (zip bundle) | https://apps.bea.gov/industry/iTables%20Static%20Files/AllTablesSUP.zip | `data/bea_io/AllTablesSUP.zip` | 20 439 248 | `fe60d189c01b89df331209977b644c7c4a18d48fee307d7b9e9c3a80cc912de3` | US Govt work, public domain | 2026-04-18 |
| 2a | BEA Use Tables Summary 1997-2023 (extracted) | (extracted from #2) | `data/bea_io/Use_Tables_Supply-Use_Framework_1997-2023_Summary.xlsx` | 1 119 194 | `3c9818a61e7b11017270e49af1c0cb106122ca49d4d7058667b23805d6749ed9` | US Govt work | 2024-09-06 (vintage) |
| 2b | BEA Use Detail 2017 (extracted) | (extracted from #2) | `data/bea_io/Use_SUT_Framework_2017_DET.xlsx` | 2 121 639 | `07aa2a21151e78ec1462c8f48142d274c153d90aff07bd797e07c6bc8486911e` | US Govt work | 2024-09-25 (vintage) |
| 3 | IRS SOI county-to-county migration inflows 2022-23 | https://www.irs.gov/pub/irs-soi/countyinflow2223.csv | `data/internal_migration/county_inflow_2022_23.csv` | 4 571 970 | `813ba2ef550c6a598a5121ccf98edcc79f61f1af69eb495bf44cd830b1586745` | US Govt work, public domain | 2026-04-18 |
| 4 | IRS SOI county-to-county migration outflows 2022-23 | https://www.irs.gov/pub/irs-soi/countyoutflow2223.csv | `data/internal_migration/county_outflow_2022_23.csv` | 4 584 439 | `364dba518f0db092515ccde03dda987815f6e54bcc8859640001e9185d4c106e` | US Govt work, public domain | 2026-04-18 |
| 5 | Clemens 2011 JEP "Economics and Emigration: Trillion-Dollar Bills on the Sidewalk?" | https://www.aeaweb.org/articles/pdf/doi/10.1257/jep.25.3.83 | `data/clemens/clemens_2011.pdf` | 676 648 | `0448c8e89eca40e9db5458ff5bad01c16324481840ef7eda94c3ea3d4d8f2786` | AEA — fair-use reference; reader should fetch from AEA | 2026-04-18 |

## Live-pulled datasets (fetched by analysis scripts on first run)

| Dataset | Source | Path | Bytes | SHA256 (this snapshot) | Pulled by |
|---------|--------|------|-------|------------------------|-----------|
| QWI state panel 2003Q1-2023Q4, 9 industries × 4 educations | Census QWI timeseries API `api.census.gov/data/timeseries/qwi/se` | `data/lehd/qwi_state_panel.parquet` | 1 996 623 | `0f1712703decadd2655364e63ff32145e2c4e40146f1c16166f6b97f24227507` | `scripts/pull_qwi_state_panel.py` |
| ACS 1-yr state immigrant share 2005-2023 (B05002) | Census ACS 1-yr API `api.census.gov/data/{year}/acs/acs1` | `data/lehd/acs_state_immigrant_share.parquet` | 25 827 | `be2b07d6c8fbf54ceb94c029a03aadca7783ce279a574f4cfd193c638c8454f7` | `scripts/pull_acs_state_immigrant_share.py` |

These checksums will drift across vintages (Census revises QWI quarterly; ACS
1-yr 2024 release will add a new year). They document THIS snapshot for
forensic comparison; they are NOT validated by `setup.sh`.

## Hand-compiled panels (in repo, not re-acquired)

### `data/everify/everify_state_mandates.csv`
- **SHA256:** `f8b1966f4cf3c856baf311d8052bd5d8fc4c275dc2deafdb3f8e212164a9aef3`
- **Bytes:** 1 862
- **Provenance:** Compiled from state legislative texts and the National
  Conference of State Legislatures' E-Verify tracker. Each row records the
  state FIPS, mandate scope (`all_employers`, `15plus_employees`, `public_only`,
  `none`), and effective date. Keyed to the Bohn-Lofstrom-Raphael (2014) and
  Orrenius-Zavodny (2015) coding conventions where they overlap.
- **Licence:** Author-compiled; CC0.

### `data/sanctuary/sanctuary_state_panel.csv`
- **SHA256:** `c9b9090439b49712cd3f11296655c0caecafae4df489ec4cc7b42de2dac42036`
- **Bytes:** 3 184
- **Provenance:** Compiled from primary legal sources (state statutes,
  governors' executive orders) — the **ILRC sanctuary policy tracker is not
  downloadable** as a flat dataset, so each row was hand-coded from the
  underlying law. Anti-sanctuary entries cite e.g. TX SB 4 (2017),
  FL SB 168 (2019), AL HB 56 (2011), AZ SB 1070 (2010); pro-sanctuary
  entries cite e.g. CA SB 54 (2017), IL TRUST Act (2017), OR ORS 181A.820
  (1987). Columns: `state_fips`, `policy_type` ∈
  {`pro_sanctuary`, `anti_sanctuary`, `neutral`}, `effective_date`,
  `citation`.
- **Licence:** Author-compiled; CC0.

### `data/daca/daca_timeline_and_design.md`
- **SHA256:** `9e22dc7c1b23185dac086a5d1b0a58bcefa0309fbad2dfa720b8ed775d2857b7`
- **Bytes:** 4 591
- **Provenance:** Notes file documenting DACA timeline (2012 announcement,
  2017 rescission, 2020 SCOTUS, 2021 reopening, 2025 ruling). For future
  RD/event-study designs; not consumed by current analysis scripts.
- **Licence:** Author notes; CC0.

### `data/clemens/open_borders_calibration_baseline.json`
- **SHA256:** `f4715f2e276f01ecebdf1aa802209942a1aea92215e060d638c549c726c4c91a`
- **Bytes:** 4 987
- **Provenance:** Generated by `scripts/open_borders_baseline.py` from the
  Clemens 2011 Place Premium parameters embedded in the script. Re-deriving
  is deterministic. Listed here for hash continuity.

## Gotchas

- **WRLURI 2018: dead link.** The Wharton Residential Land Use Regulatory
  Index 2018 wave's canonical URL
  (`real-estate.wharton.upenn.edu/wp-content/uploads/.../WRLURI-2018.zip`) has
  been intermittently 404 since early 2025 and was not retrievable on
  2026-04-18. `setup.sh` skips it with an explanatory message. The Saiz 2010
  `.dta` already contains 2008-vintage `WRLURI` and `unaval` columns, which
  is what `saiz_decomposition.py` actually consumes. The 2018 refresh is
  desirable for sensitivity analysis but not required to reproduce current
  findings.

- **BEA AllTablesSUP.zip vs the two extracted .xlsx files.** The repo carries
  the unzipped Summary and Detail .xlsx files because BEA renames the inner
  paths between vintages. `setup.sh` downloads the zip and unzips both targets
  by exact filename; if BEA renames again, the unzip will fail loudly.

- **Census API anonymous limits.** ACS and QWI calls work without an API key
  at the volumes here (~36 QWI calls + 18 ACS calls per full run). If you hit
  the anonymous quota you'll see HTTP 200 with empty JSON. Set
  `CENSUS_API_KEY` (free, https://api.census.gov/data/key_signup.html) if so.

- **2020 ACS 1-yr withdrawn** (COVID data quality). `pull_acs_state_immigrant_share.py`
  silently skips that year; downstream code expects the gap.

- **QWI vintage drift.** Census refreshes QWI cells quarterly. The
  `qwi_state_panel.parquet` SHA256 above is for the 2026-04-18 pull. A fresh
  pull on a later date will not match. Numerical findings should be stable
  to ±1% across nearby vintages; if you see >5% drift, investigate.

- **Stata `.dta` reading.** `saiz_decomposition.py` and
  `merge_saiz_rent_immigrant.py` use `pd.read_stata()`, which is built into
  pandas. No extra dependency needed.

- **Clemens 2011 PDF.** Shipped for reader convenience only. AEA is the
  authoritative source. If reproducing without network access to AEA, the
  computational pipeline (`open_borders_baseline.py`) does not need the PDF —
  only the parameters embedded in the script.

<!-- knowledge-index
generated: 2026-04-19T04:21:14Z
hash: 85c0b6cd8823


end-knowledge-index -->
