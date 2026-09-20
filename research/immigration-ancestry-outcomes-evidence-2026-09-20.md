# Ancestry and outcomes: measured answers and remaining routes

Date: 2026-09-20. Mode: descriptive evidence update, not a national fiscal or crime estimate.

**Continuation completed later2026-09-20:** MASP is now analyzed, Pew has an age25+ sensitivity, and SIPP's advertised parental-country fields were verified to be region recodes. The earlier SIPP opportunity below is superseded. PSID has an additional explicit AI-use restriction. See the executed continuation and stopping decision below.

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

## Initial additional-dataset assessment — superseded by execution below

- **MASP: acquired.** [Author's public file](https://www.edwardtelles.com/masp), parsed1,850 rows×2,560 variables. Follows historical LA/San Antonio families and selected adult children; includes identity, birthplaces, schooling, family income and benefit fields. Family recruitment permits observing descendants who use American/Anglo/White labels. Reconstruction remains necessary, especially identity skips, row roles, parent links and codebook-version differences. [Acquisition details](../infra/immigration-fiscal/masp_2026_09_20/ACQUIRED.md). No fresh outcome estimate claimed.
- **SIPP: verified additional route, not yet executed.** [Official variable inventory](https://api.census.gov/data/2023/sipp/variables.html) has biological parents' countries (`TBIOMOMNAT/TBIODADNAT`), biological-parent pointers and earnings/benefits. [Following rules](https://www.census.gov/programs-surveys/sipp/methodology/organizing-principles.html) retain original sample people after household moves. Linking a parent's own parental country can recover selected grandchildren and preserve lineage after moving out. No guarantee of sample size, complete remote ancestors or national G4+; institutionalized people are not interviewed, limiting incarceration inference.
- **PSID: existing access gate.** Family Identification Mapping System traces relatives across generations, but birthplace completeness must be measured jointly. Authentication/data access and actual country coverage remain unresolved; an ancestor ID is not an ancestor's birthplace. [Existing access audit](../infra/immigration-fiscal/generation_estimation_2026_09_20/PSID_ACCESS.md).

**Defeater/next information:** a larger representative ancestry-screen sample measuring identity and outcomes together, or a verified linked-family sample with sufficient Mexican-country coverage, could materially change the size/direction of the correction. Do not substitute these older local/cohort results for the current national population. This LLM-produced synthesis is not an independent authority; direct files, regeneration and competing source results are the evidence.

## Executed continuation, later2026-09-20

### Pew completed-schooling sensitivity

Restricting the US-born/two-US-born-parent comparison to observed age25+ gives139 identifiers and34 nonidentifiers. Weighted BA+ is16.70% versus19.24%; the historically calibrated pooled rate is16.97%, a+0.27 percentage-point correction. Approximate weighted mean age is43.87 versus48.68, so this is an age restriction, not full age standardization. Six principal-group identifiers with unknown exact age are excluded, along with under25s. No-high-school is13.51% versus21.89%. Both schooling endpoints and the earlier all-adult result remain visible; sample size and unknown ancestry preclude a general no-difference conclusion. [DATA: updated [Pew script](../infra/immigration-fiscal/pew_outcomes_2026_09_20/analyze.py), source hashes unchanged.]

### MASP: measured historical family-descendant outcomes

The author-distributed file contains758 adult-child interviews from482 original families, surveyed1998–2002 following the1965–66 LA/San Antonio sample. All rates here are **unweighted, selected historical sample descriptions**. [SOURCE/DATA: [full reconstruction, source questions and script](../infra/immigration-fiscal/masp_2026_09_20/RESULT.md).]

| Initial ethnic self-description | Mentions Mexican/Latino/Spanish | Only Anglo/American mentions |
|---|---:|---:|
| Respondents |692|24|
| BA or higher |111/692 =16.04%|4/24 =16.67%|
| Past-year respondent/spouse receipt of SSI, public welfare or food stamps |53/690 =7.68%|2/24 =8.33%|

Another42 remain Other/unresolved, including unadjudicated text. These groups are not exhaustive yes/no Hispanic identification, and spontaneous omission is not demonstrated rejection when directly asked. Adding all66 omitted/unclear cases changes the observed-sample degree rate16.04%→16.09%. This is neither a national correction nor evidence of equivalence. Benefit receipt is respondent/couple incidence, not benefit dollars or net fiscal contribution.

The preferred-label comparison gives a different association:70 prefer Anglo/American and22.86% hold a degree, but43 of these70 also initially mention a Latino-related background. They cannot all be counted as missing Hispanics. A White response on the race-form question is also not Hispanic nonidentification:92 White respondents explicitly mentioned Latino-related backgrounds.

Labeled family-country fields recover243 Mexican-grandparent G3 cases and23 cases with US-born nearer ancestors and an observed Mexican great-grandparent. But the narrow Anglo/American-only groups have just13 generic-G3 and2 generic-G4+ respondents. Informant-country codes lacking value labels remain excluded principally; their explicitly assumed-code sensitivity changes the generation ordering. Further subgroup outcome modeling is not informative enough for the national question. The nativity convention is questionnaire country-defined; Puerto Rico/Guam in Other prevent equating it with official Census citizenship-based nativity.

Validation: primary question/value definitions checked;108 independently recomputed count/event/rate cells matched. Source hashes, source-family clustering and missingness are retained. No causal or national inference asserted.

### SIPP: the country-recovery promise fails the public codebook check

The earlier variable-label inference was wrong. `TBIOMOMNAT/TBIODADNAT` release broad regions, and own `TBORNPLACE` pools foreign birth into regions too. Primary2024/2025 dictionaries and complete2023/2024 raw support scans establish that the held public2023–2025 files cannot distinguish a Mexico-born ancestor through those fields. [SOURCE/DATA: [executed audit](../infra/immigration-fiscal/sipp_lineage_2026_09_20/RESULT.md), [2025 dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf).]

The2025 annual file covers reference2024. Among Mexican-identifying adults25–64, biological-parent reconstruction yields only28 generic-G3 and16 generic-G4+ cases (Kish weight-concentration counts19.4/12.3); restricting used birth/parent-link fields to reported values leaves23/8. These are selected, identity-dependent groups, not country-verified Mexican descendants. No earnings/benefit contrast fitted. Additional annual linkage would not restore the missing country codes, so it is deferred for this particular question.

### PSID and stopping point

PSID's current [Conditions of Use](https://simba.isr.umich.edu/U/CondUse.aspx), item5, prohibit AI/LLM use with its data. The browser also requires condition acceptance before downloading. No terms accepted or microdata acquired. Permission covering the proposed workflow or a compliant separately conducted human analysis would be needed; authentication alone does not solve this. [SOURCE: [dated access record](../infra/immigration-fiscal/generation_estimation_2026_09_20/PSID_ACCESS.md).]

Further public-data work on the national ancestry-complete correction has reached diminishing returns. The useful measurements above remain, as do the earlier published NLSY results showing some hidden progress. None identifies a national current G3/G4+ fiscal or crime correction for all Mexican descendants. This is a limit of the inspected data and access conditions, not a claim that the underlying question is unknowable.

## Revisions

- Later2026-09-20: [Stopping decision and evidence](../decisions/2026-09-20-ancestry-outcome-data-ceiling.md) supersedes the initial opportunity assessment after actual MASP/SIPP execution and PSID terms verification. Added Pew age25+ sensitivity; retained disconfirming results and historical source assessments.
