# Immigration public MVP MEPS module — 2026-04-11

## Purpose

This memo records the first real `MEPS` health-cost module for the public-use immigration MVP.

It replaces the earlier profiling-only state with a reusable derived table:

- [meps_health_cost_module_2023.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv)
- [meps_health_cost_module_2023.meta.json](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json)
- builder: [build_public_mvp_meps_module.py](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_public_mvp_meps_module.py)
- bridge input to the downstream scenario engine after the `SIPP` join:
- [sipp_meps_expected_health_cost_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv)
- [sipp_meps_bridge_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv)
- bridge builder: [build_public_mvp_sipp_meps_bridge_2024.py](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/build_public_mvp_sipp_meps_bridge_2024.py)

## What was built

The module is a compact descriptive table at the cell:

1. `age band`
2. `nativity`
3. `insurance category`

Each cell includes:

1. weighted person mass
2. normalized `nativity_group` and `insurance_group` join keys alongside the official MEPS code labels
3. weighted mean total spending
4. weighted mean self/family spending
5. weighted mean Medicare spending
6. weighted mean Medicaid spending
7. weighted mean private-insurance spending
8. weighted mean other state/local spending
9. positive-spending shares for each payer
10. top `YRSINUS` categories inside foreign-born cells

## Method

Source files:

1. [h251dat.zip](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip)
2. [h251su.txt](/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt)

Build details:

1. The builder streams the official fixed-width `h251.dat` payload from the zip archive. [SOURCE: `sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251dat.zip`]
2. Field positions and value labels come from the official SAS setup file `h251su.txt`. [SOURCE: `sources/immigration-fiscal/data/external/stage3/ahrq/meps/h251su.txt`]
3. Codes are normalized before label lookup so MEPS internal zero-padded values like `01` and `05` resolve to the documented labels `1 YES` and `5 15 YEARS OR MORE`. [SOURCE: `sources/immigration-fiscal/data/derived/build_public_mvp_meps_module.py`]
4. The output contains `81` cells built from `18,919` MEPS person rows. [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json`]

Engineering choice:

1. This pass uses the official fixed-width layout instead of the `.dta` file because the environment did not have a Stata reader installed, while the fixed-width path was already verified against the official setup file. [SOURCE: `sources/immigration-fiscal/data/derived/build_public_mvp_meps_module.py`] [SOURCE: `sources/immigration-fiscal/data/derived/profile_public_mvp_inputs.py`]

## Verified findings

### 1. The `MEPS` module is now a real derived asset, not just a profiler

1. The CSV exists at [meps_health_cost_module_2023.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv). [SOURCE: local file]
2. The metadata file records source paths, parsed value labels, row counts, and module notes. [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json`]
3. A downstream bridge uses this module as the payer-incidence source: [sipp_meps_bridge_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.csv) and [sipp_meps_expected_health_cost_cells_2024.csv](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_expected_health_cost_cells_2024.csv). [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.meta.json`]

Interpretation:

1. The public MVP now has a reusable health-cost / payer-incidence input table. [INFERENCE]

### 2. Working-age foreign-born adults still look cheaper on observed annual spending than U.S.-born adults within comparable insurance buckets

For ages `25-64` with `any private` coverage:

1. U.S.-born mean total spending is about `$8,084`. [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv`]
2. Foreign-born mean total spending is about `$5,522`. [SOURCE: same]

For ages `25-64` with `public only` coverage:

1. U.S.-born mean total spending is about `$10,200`. [SOURCE: same]
2. Foreign-born mean total spending is about `$5,185`. [SOURCE: same]

For ages `25-64` while `uninsured`:

1. U.S.-born mean total spending is about `$1,451`. [SOURCE: same]
2. Foreign-born mean total spending is about `$782`. [SOURCE: same]

Interpretation:

1. The earlier profiler signal survives the real module build. [INFERENCE]
2. The public MVP should not hard-code a story where foreign-born working-age adults are mechanically more expensive in observed annual medical spending. [INFERENCE]

### 3. Insurance status matters more than nativity for the spending gradient inside working ages

Within foreign-born ages `55-64`:

1. `public only` mean total spending is about `$11,711`. [SOURCE: same]
2. `any private` mean total spending is about `$6,839`. [SOURCE: same]
3. `uninsured` mean total spending is about `$1,147`. [SOURCE: same]

Within foreign-born ages `45-54`:

1. `public only` mean total spending is about `$3,917`. [SOURCE: same]
2. `any private` mean total spending is about `$5,713`. [SOURCE: same]
3. `uninsured` mean total spending is about `$869`. [SOURCE: same]

Interpretation:

1. The public MVP should treat insurance mix as a first-order health-cost branch, not a cosmetic covariate. [INFERENCE]

### 4. Foreign-born cells retain tenure-in-U.S. structure through `YRSINUS`

1. The module carries top `YRSINUS` codes inside foreign-born cells rather than dropping tenure information entirely. [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv`]
2. This preserves a coarse arrival-tenure signal without pretending `YRSINUS` is literal years. [SOURCE: `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json`]

Interpretation:

1. The next bridge can use tenure-sensitive health-cost scenarios without reparsing the raw MEPS file. [INFERENCE]

## What this module does not do

1. It does not identify undocumented status. [SOURCE: `research/immigration-public-mvp-readiness-2026-04-11.md`]
2. It does not produce a lifetime fiscal estimate by itself. [SOURCE: same]
3. It does not replace linked admin data or `NAS`. [SOURCE: same]
4. It does not convert annual observed medical spending into welfare or net social value. [FRAMING-SENSITIVE]

## Best next step

1. Consume `sipp_meps_expected_health_cost_cells_2024.csv` in the public MVP scenario engine so each `SIPP` transition cell maps to an expected annual health-cost profile with bridge provenance preserved. [INFERENCE]
