# Ancestry and outcomes: measured answers and remaining routes

Date: 2026-09-20. Mode: descriptive evidence update, not a national fiscal or crime estimate.

**Verdict [INFERENCE]:** Ethnic attrition can hide some educational progress, but available evidence does not justify a universal large upward correction. We can measure selected nonidentifiers and generation-specific outcomes; a current national G3/G4+ fiscal/crime total covering all Mexican descendants remains unidentified.

## New direct Pew calculation

[SOURCE: held 2015 NSL and 2015–16 non-Hispanic ancestry survey; [Pew methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/); [script](../infra/immigration-fiscal/pew_outcomes_2026_09_20/analyze.py).]

Weighted BA-or-higher percentages among adults reporting Mexican origin (`q3_combo=1`). Identifiers/nonidentifiers concern Hispanic self-identification. Window fixed by the available paired surveys. Person-level descriptive schooling measures; neither monetary gross/net flows nor fiscal proxies. Unknown origin and unspecified mixed-origin cases are not recovered.

| Scope | Identifier n | Nonidentifier n | Identifier BA+ | Nonidentifier BA+ | Calibrated pooled BA+ |
|---|---:|---:|---:|---:|---:|
| US-born, two US-born parents | 160 | 44 | 15.67% | 16.48% | 15.77% |
| G3: above, at least one foreign-born grandparent | 94 | 12 | 15.84% | 18.16% | 15.98% |
| G4+: above, four US-born grandparents | 54 | 26 | 20.71% | 18.00% | 20.15% |

These are generic birthplace generations paired with reported Mexican origin, **not verified Mexico-specific ancestral birthplaces**. Puerto Rico is grouped with foreign birthplace in the source-compatible reconstruction. Both later-generation principal groups average approximately age41; this is not an age-adjusted causal comparison. All204 principal-row respondents have valid schooling. Small sample sizes preclude asserting equivalence; no design-correct confidence intervals are claimed.

Pooling is a historical calibration: full source weights normalize to37.8m identifiers and4.9m nonidentifiers **before** Mexican-origin selection. It is not an estimate of today's attrition. The principal row's weighted nonidentifier mass is12.45%; its BA+ correction is only+0.10 percentage points. This does not rule out larger effects among descendants not reporting or knowing Mexican ancestry.

The principal no-high-school rate is12.51% for identifiers versus15.66% for nonidentifiers: this sample also contradicts assuming uniformly better schooling among nonidentifiers. Both directions are imprecise. Income cannot be cleanly pooled: NSL asks2014 **family** income, omnibus asks annual **household** income. Neither is individual earnings; no fiscal conversion performed.

Reproduce: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with pyreadstat --with pandas --with numpy python3 infra/immigration-fiscal/pew_outcomes_2026_09_20/analyze.py`. Inputs SHA256-checked, origin label and weights asserted. Principal percentages independently reproduced from the SAVs. Output CSV and audit metadata are ignored/rederivable.

## Evidence in the opposite direction

[Duncan, Grogger, Leon and Trejo](https://docs.iza.org/dp12704.pdf) use NLSY97 restricted ancestral-country fields to recover Mexican G3 independently of current identity. For the1980–84 birth cohort, completed education rises from about13.0 years in G2 to13.5 in G3, while pooling later generations masks progress. Their G3 still trails fourth-plus-generation whites by roughly0.9 schooling years. Their G4+ classification remains dependent on respondent/parent identity. This supports some hidden progress, not complete convergence or an ancestry-complete fiscal estimate. [SOURCE: paper; no local restricted-data replication.]

Existing public NLSY97 and local IIMMLA education/earnings/criminal-justice analyses remain available; see [all-age and lineage findings](immigration-all-age-and-lineage-findings-2026-09-17.md). They do not solve missing Mexico-specific lineage for all nonidentifiers. [SOURCE: checked scripts/results; outcome definitions are arrest/incarceration, not all offending.]

## Additional datasets

- **MASP: acquired.** [Author's public file](https://www.edwardtelles.com/masp), parsed1,850 rows×2,560 variables. Follows historical LA/San Antonio families and selected adult children; includes identity, birthplaces, schooling, family income and benefit fields. Family recruitment permits observing descendants who use American/Anglo/White labels. Reconstruction remains necessary, especially identity skips, row roles, parent links and codebook-version differences. [Acquisition details](../infra/immigration-fiscal/masp_2026_09_20/ACQUIRED.md). No fresh outcome estimate claimed.
- **SIPP: verified additional route, not yet executed.** [Official variable inventory](https://api.census.gov/data/2023/sipp/variables.html) has biological parents' countries (`TBIOMOMNAT/TBIODADNAT`), biological-parent pointers and earnings/benefits. [Following rules](https://www.census.gov/programs-surveys/sipp/methodology/organizing-principles.html) retain original sample people after household moves. Linking a parent's own parental country can recover selected grandchildren and preserve lineage after moving out. No guarantee of sample size, complete remote ancestors or national G4+; institutionalized people are not interviewed, limiting incarceration inference.
- **PSID: existing access gate.** Family Identification Mapping System traces relatives across generations, but birthplace completeness must be measured jointly. Authentication/data access and actual country coverage remain unresolved; an ancestor ID is not an ancestor's birthplace. [Existing access audit](../infra/immigration-fiscal/generation_estimation_2026_09_20/PSID_ACCESS.md).

**Defeater/next information:** a larger representative ancestry-screen sample measuring identity and outcomes together, or a verified linked-family sample with sufficient Mexican-country coverage, could materially change the size/direction of the correction. Do not substitute these older local/cohort results for the current national population. This LLM-produced synthesis is not an independent authority; direct files, regeneration and competing source results are the evidence.
