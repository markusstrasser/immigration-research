# Immigration next data upgrades

Date: 2026-04-10

## Objective

Replace the two assumptions that are currently doing the most inferential work:
1. the `federal-side proxy ledger`
2. the `coarse local burden bridge`

## Upgrade 1: Federal microsimulation layer

### Problem to solve

The current origin ranking uses ACS income and selected benefit proxies to guess whether a cell is more likely to be `federally better` or `federally worse`.

That is not good enough.

### Target

Build a household federal tax-and-transfer layer keyed to the same ACS origin-household cells already in the warehouse.

### Datasets

1. `SIPP 2023 PUF`
Path: `/Users/alien/Projects/research/sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip`
2. `ACS PUMS person + housing`
Already in use.
3. `OHSS` admission-channel files
Already staged in the origin stack.
4. `ORR` refugee/admin files
Add if admission-channel separation becomes important.

### Build logic

1. Create ACS household cells by:
   - `origin`
   - `state or PUMA`
   - `education band`
   - `age band`
   - `family type`
   - `school-age child structure`
   - `earnings band`
2. Create SIPP donor cells on matching household keys.
3. Reweight or hot-deck SIPP households onto ACS origin-household cells.
4. Compute first-pass federal components:
   - payroll tax
   - federal income tax
   - refundable credits
   - SNAP
   - SSI
   - TANF-like cash
   - Medicaid / CHIP proxy amounts
5. Materialize a new table:
   - `acs_origin_household_federal_microsim_2023`

### Why this kills the assumption

It replaces `income plus Medicaid/public-assistance flags` with an actual household tax-transfer estimate.

### What it still will not solve

1. Unauthorized-status identification stays partial.
2. General-equilibrium indirect effects remain outside the microsim.
3. Descendant lifetime fiscal effects remain a separate long-horizon problem.

### Memory-safe execution

1. Do not fully unzip or fully load SIPP in memory.
2. Use DuckDB or chunked `uv run python3` pipelines.
3. Materialize donor-cell summaries early and discard row-level intermediates.
4. Keep every step restartable to avoid rerunning large ingestion.

## Upgrade 2: Tract-and-district-weighted local context

### Problem to solve

The current local side mixes:
1. state school spending,
2. PUMA median rent,
3. area-weighted county CHAS and IRS overlays.

This is enough for descriptive heterogeneity, not for a clean local-burden estimate.

### Target

Replace land-area bridging with tract and district weighting, then rebuild PUMA context on relevant population weights.

### Datasets

1. `NCES CCD district spine`
2. `Census F-33 school finance`
3. `EDFacts` district enrollment and ELL / migrant counts
4. `ACS tract tables`
   - renter share
   - overcrowding
   - rent burden
   - school-age population
5. `HUD CHAS`
6. `HUD SAFMR`
7. `AHS`
8. Census tract-to-PUMA relationship files

### Build logic

1. Build a tract scaffold.
2. Attach tract population, school-age population, renter households, and low-income renter households.
3. Attach district finance and ELL/migrant context through tract-to-district mapping.
4. Aggregate to PUMA using:
   - school-age population weights for school context
   - renter-household weights for housing context
5. Rebuild:
   - `puma_school_context_2023`
   - `puma_housing_context_2023`
   - `origin_puma_household_stage3_context_2023`

### Why this kills the assumption

It replaces `land area` with weights that match the phenomena we care about: people, children, and renter households.

### What it still will not solve

1. It still does not identify immigrant-caused marginal burden directly.
2. It still will not fully price owner gains, supply response, or native relocation.
3. It still will not replace a causal design if we want effect sizes rather than pressure exposure.

### Memory-safe execution

1. Stage tract tables in narrow column sets.
2. Persist tract-level parquet partitions by state.
3. Aggregate to PUMA before joining back to origin cells.
4. Avoid full national tract-wide pandas frames.

## Upgrade 3: Optional but high-value

### Admission-channel and legal-status structure

Reason:
Origin alone hides real heterogeneity.

Datasets:
1. `OHSS`
2. `ORR`
3. possibly `TRAC` or other admin context if needed

Value:
1. separates refugee-like from labor-oriented from family-based inflows
2. improves both fiscal and political-economy interpretation

## Execution order

1. `Federal microsim layer`
2. `Tract-and-district-weighted local context`
3. `Admission-channel overlay`
4. only after those: revisit scalar claims

## Success test

The upgrade pass succeeds if it lets us replace these sentences:
1. `proxy-federal positive`
2. `state-local negative under coarse local proxies`

with these sentences:
1. `federal household microsim estimate`
2. `district-and-tract-weighted local capacity estimate`
