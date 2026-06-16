# Immigration — Verification Handoff

Use this file when another agent needs to verify commentator or economist claims against this repo and the local data stack.

## First principle

Do not verify "immigration" as one object.

Distinguish at minimum:

1. `legal low-skill immigration`
2. `unauthorized immigration`
3. `recent asylum / surge inflows`
4. `high-skill immigration`

If a writer slides between those categories, flag `CATEGORY SLIP`.

## Repo map by claim type

### 1. Wage and labor-market claims

Use first:

1. `research/fiscal-impact-unauthorized-immigration-research-memo.md`
2. `research/immigration-economist-effects-matrix.md`
3. `research/immigration-evidence-base-audit.md`

What these can support:

1. the Borjas vs Peri range
2. the point that many pro-immigration papers are channel-specific, not full ledgers
3. the distinction between wage effects, task complementarity, and total welfare

What they cannot settle cleanly:

1. one final universal elasticity for "low-skill immigration"
2. exact effect sizes for every origin and destination pair

## 2. Federal vs state/local fiscal claims

Use first:

1. `research/fiscal-impact-unauthorized-immigration-research-memo.md`
2. `research/full-spectrum-costs-unauthorized-immigration-research-memo.md`
3. `research/immigration-unified-scenarios-memo.md`
4. `sources/immigration-fiscal/fiscal_impact_synthesis_gpt54.md`

What these can support:

1. federal-positive / state-local-negative splits
2. the child-attribution dispute
3. the effect of average-cost vs marginal-cost accounting
4. the point that local congestion and adaptation costs are real
5. the point that the repo still does not have a defensible bucket-specific lifetime `NPV` for `<HS`, `HS / GED`, and `some college / associate`

What they cannot settle cleanly:

1. a single exact per-person lifetime NPV with high confidence
2. a clean unauthorized-specific national number free of modeling assumptions
3. a finished lifetime number by the three broad education buckets unless an agent explicitly builds and validates that scenario layer

## 3. Local burden, housing, and school-pressure claims

Use first:

1. `research/immigration-local-burden-puma-layer.md`
2. `research/immigration-household-weighted-correction.md`
3. `research/state-local-cost-examples-ny-ca-tx.md`
4. `research/immigration-verified-findings-report-2026-04-10.md`

What these can support:

1. burden heterogeneity by origin and destination
2. why state averages can hide PUMA-level differences
3. why household-normalized child burden matters

What they cannot settle cleanly:

1. exact city-level causal effects without further local data
2. a national scalar for "housing harm"

## 4. "Economists agree" or Substack-writer claims

Use first:

1. `research/immigration-economist-effects-matrix.md`
2. `research/immigration-clark-respondent-audit.md`
3. `research/immigration-evidence-base-audit.md`

What these can support:

1. whether a cited economist is talking about wages, prices, firms, or a full welfare ledger
2. whether the evidence base is partial rather than wrong
3. whether a commentator is overstating the scope of a paper

## Datasets by question

### If the claim is about current composition, origin mix, household structure, language, commute, or education

Use:

1. `ACS 2023 PUMS`
2. origin tables in `immigration_context.duckdb`
3. `research/immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md`

Local assets:

1. `sources/immigration-fiscal/data/census/acs_pums_2023_person.zip`
2. `sources/immigration-fiscal/data/census/acs_pums_2023_household.zip`
3. `sources/immigration-fiscal/data/derived/immigration_context.duckdb`
4. `sources/immigration-fiscal/data/derived/origin/`

Best for:

1. who the low-education groups are
2. where they live
3. household child intensity
4. rent exposure and local context
5. broad three-bucket stock and state-share cuts for foreign-born adults ages `25-64`

Not good for:

1. undocumented status identification
2. lifetime trajectories
3. bucket-specific lifetime fiscal values

### If the claim is about taxes paid by unauthorized immigrants

Use:

1. `ITEP 2024`
2. `SSA actuarial note`
3. IRS context tables as secondary anchors

Local assets:

1. `sources/immigration-fiscal/data/itep/ITEP-Tax-Payments-by-Undocumented-Immigrants-2024.pdf`
2. `sources/immigration-fiscal/data/itep/itep_table_*.tsv`
3. `sources/immigration-fiscal/data/ssa/actuarial_note_151.pdf`
4. `sources/immigration-fiscal/data/irs/24dbs01t02nr.xlsx`

Best for:

1. tax-side contribution claims
2. state-by-state tax comparisons

Not good for:

1. full spending-side burden

### If the claim is about public spending or local congestion

Use:

1. `CBO 2025 state/local report`
2. `NCES per-pupil spending`
3. school-finance and local context overlays
4. `research/immigration-frontier-data-acquisition-2026-04-11.md`
5. `research/immigration-school-service-complexity-2026-04-11.md`

Local assets:

1. `sources/immigration-fiscal/data/cbo/61256-immigration-state-local.pdf`
2. `sources/immigration-fiscal/data/nces/tabn236.10.xlsx`
3. `sources/immigration-fiscal/data/external/census_school_finance_2023.txt`
4. `sources/immigration-fiscal/data/derived/stage2/school_finance_county_2023.csv`
5. `sources/immigration-fiscal/data/external/stage4/saipe/`
6. `sources/immigration-fiscal/data/external/stage4/courts/`
7. `sources/immigration-fiscal/data/external/stage4/nces/`
8. `sources/immigration-fiscal/data/derived/stage4/school_service_complexity_district_2023.csv`
9. `sources/immigration-fiscal/data/derived/stage4/school_service_complexity_state_2023.csv`
10. `sources/immigration-fiscal/data/derived/stage4/nces_elsi_district_english_columns_probe_2026-04-11.json`

Best for:

1. school and shelter burden
2. local capacity and crowding claims
3. district child-intensity overlays
4. court and interpreter operating-cost context

Not good for:

1. a complete welfare model by origin
2. current district `English learner` counts unless the NCES route is separately validated

### If the claim is about health-cost incidence

Use:

1. `research/immigration-public-mvp-meps-module-2026-04-11.md`
2. `MEPS HC-251`
3. the full-spectrum memo for interpretation

Local assets:

1. `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.csv`
2. `sources/immigration-fiscal/data/derived/stage3_proto/meps_health_cost_module_2023.meta.json`
3. `sources/immigration-fiscal/data/external/stage3/ahrq/meps/`
4. `research/full-spectrum-costs-unauthorized-immigration-research-memo.md`

Best for:

1. payer incidence
2. medical spending context
3. checking whether a commentator is smuggling in a crude high-cost assumption for foreign-born adults

Not good for:

1. unauthorized-specific clean estimates by itself

### If the claim is about program participation and household transitions

Use:

1. `SIPP 2024`
2. `SIPP 2023`

Local assets:

1. `sources/immigration-fiscal/data/external/stage3/census/sipp/pu2024_csv.zip`
2. `sources/immigration-fiscal/data/external/stage2/census/sipp/pu2023_csv.zip`
3. `sources/immigration-fiscal/data/derived/stage2/sipp_foreign_low_skill_calibration_2023.csv`

Best for:

1. monthly program participation
2. household composition changes
3. transfer-incidence scaffolding

Not good for:

1. true lifetime modeling
2. strong unauthorized identification

### If the claim is about federal microsimulation or long-run lifetime trajectories

Use cautiously:

1. `research/immigration-lifetime-fiscal-data-stack-2026-04-10.md`
2. `research/immigration-public-data-acquisition-2026-04-11.md`
3. `research/immigration-prototype-progress.md`

Current blocker:

1. the repo does not yet have a trustworthy federal microsimulation prototype for headline use

Do not let another agent pretend otherwise.

## Disciplines to consult

This topic is not just labor economics.

### Essential disciplines

1. `labor economics`
   use for wages, substitution, task complementarity, firm response
2. `public finance`
   use for taxes, transfers, child attribution, intergovernmental splits
3. `urban economics`
   use for rents, housing incidence, congestion, local public-goods crowding
4. `demography`
   use for composition, age structure, household formation, descendants
5. `education finance`
   use for K-12 burden and district/state cost structure
6. `political economy`
   use for backlash, redistribution support, legitimacy, policy churn

### Secondary disciplines

1. `health economics`
   for emergency care, payer incidence, delayed-care channels
2. `law / administrative state`
   for asylum rules, enforcement burdens, court backlogs

## Paper families to search or reuse

### For wage effects

1. `Borjas`
2. `Peri`
3. `Card`
4. wage-effect meta-analyses

Question to ask:

1. are they estimating close substitutes, average natives, or firms?

### For positive channels beyond wages

1. `Cortes and Tessada`
2. `Clemens and Lewis`
3. `Colas and Sachs`

Question to ask:

1. are they showing a real positive channel, or claiming a complete welfare verdict?

### For fiscal baselines

1. `NAS 2017`
2. `CBO 2024 federal`
3. `CBO 2025 state/local`
4. `ITEP 2024`
5. `Orrenius / Viard / Zavodny`

Question to ask:

1. which ledger, horizon, and government level are they pricing?

### For descendants and intergenerational mobility

1. `Abramitzky et al.`
2. `Duncan and Trejo`

Question to ask:

1. are descendant gains being assumed away, or assumed to fully cancel costs without evidence?

### For housing and local incidence

1. `Saiz`
2. housing-incidence / local-public-finance papers
3. property-value and local-tax-base papers

Question to ask:

1. is higher rent being treated as pure aggregate loss instead of incidence?

## What not to do

1. Do not use `ACS alone` to make lifetime fiscal claims.
2. Do not use `CPS level changes` as clean evidence of recent immigration-population shifts without checking fixed controls.
3. Do not use `ITEP` as if it were a full spending-and-tax ledger.
4. Do not use `CBO surge reports` as if they describe all immigration equally.
5. Do not use vague "social cohesion" claims unless they are decomposed into operational mechanisms.
6. Do not let high-skill evidence silently answer low-skill questions.

## Recommended verification output format

For each commentator claim:

1. `Claim`
2. `Category`: legal low-skill / unauthorized / surge / high-skill / mixed
3. `Classification`: supported / partial / contradicted / unresolved / out-of-scope
4. `Repo evidence`
5. `Dataset or paper family that should be checked next`
6. `Notes on category slip or scope inflation`
