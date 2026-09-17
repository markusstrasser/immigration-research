# NLSY97: recovered biological-parent history and bounded crime comparisons

**Verdict:** Public NLSY97 parent interviews and corrected roster IDs recover much more reported biological-parent birthplace information than the supplemental-only classifier. Like-for-like strict-generation unresolved cases fall from **7,759 to 3,266 of 8,984**. The recovered Mexican/Chicano male incarceration point estimates do **not** increase monotonically across G2/G3/G4+. This is not a parity, null-effect, or causal conclusion.

Reproducible evidence: [analysis](../infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/analyze_family.py), [source-level and arithmetic verifier](../infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/verify_family.py), [audit](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/nlsy_family/family_audit.json), [outcome table](../infra/immigration-fiscal/new_datasets_2026_09_17/derived/nlsy_family/linked_exact_outcomes.csv). Data and derived outputs remain local and ignored.

## Definition and source priority

**These are reported family-history categories, not fully harmonized legal immigration generations, country-specific Mexican lineage, or genetic ancestry.** Own/grandparent questions explicitly include US territories and Puerto Rico. Parent questions say United States without the same explicit expansion. Public data do not resolve this wording discrepancy. The parent/GP country-region created variables are geocode-restricted. [SOURCE: primary codebook; [NLS parent characteristics](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/family-background/parent-characteristics).]

Use source-tagged descriptions: reports US/territory/PR birth; one biological parent reports non-US birth; both biological parents report US birth; known foreign-born grandparent; all four grandparents report US/territory/PR birth; branch unknown. Keep Mexican/Chicano self-identification separate. One reported Mexican-origin grandparent would be genealogy; this dataset does not establish that country for the grandparent and does not measure a genetic fraction. [INFERENCE from available items.]

Primary identity choice follows the [official household guide](https://www.nlsinfo.org/content/cohorts/nlsy97/topical-guide/household/household-composition), particularly its Linking the rosters section: use **R0735000 for the responding parent**, but **corrected YOUTH biological-parent IDs rather than PARYOUTH**. HHI2 spouse/partner variables locate the responding parent's spouse. Stored IDs are explicitly matched; they are never assumed equal to array positions. The correct-ID PARYOUTH/PARHHI derivation remains a sensitivity. [SOURCE: official guide and stored-ID codebook marginals.]

## Exact mapping

| Component | Fields and acceptance rule |
|---|---|
| Responding parent | R0551500 birthplace; R0735000 respondent-parent ID; require equality to corrected biological parent ID and PARYOUTH relationship R0734800=3 mother/4 father. Disagreement stays unknown for this source. |
| Resident biological mother/father | Corrected YOUTH_MOMID R0533600 / YOUTH_DADID R0532300; positive IDs only. |
| Nonresident biological mother/father | Corrected YOUTH_NRMOMID R0535100 / YOUTH_NRDADID R0535000; namespace chosen using nonresponding parent's residence flag. |
| Responding parent's spouse | Match R0735000 to stored HHI2_ID R1101000–R1102500; lookup HHI2_SPOUSEID R1155700–R1157200 and PARTNERID R1113800–R1115300 at that record. Accept a unique positive candidate only if it equals the corrected biological parent ID; then use birthplace R0555000. |
| Nonresponding parent 1 | R0733400 identity, R0733500 residence, R0733700 sex; R0559500 birthplace. Require positive ID equality in correct residence namespace and matching mother/father sex. |
| Nonresponding parent 2 | R0733900 identity, R0734000 residence, R0734200 sex; R0559600 birthplace. Same rule. |
| Youth supplement | Z0501800 mother / Z0502000 father, asked when no parent interview. |
| Parent-roster sensitivity | Resident R0733200/R0731900; nonresident R0734600/R0734500. Spouse lookup first matches stored PARHHI_ID R0703700–R0704500, then reads PARHHI_SPOPARID R0729600–R0730400. |

Each accepted birthplace has a row in `parent_nativity_sources.csv` with its mapping, source and parent. Step/adoptive/guardian identities do not become biological identities merely because that adult completed the parent interview. Negative values and unresolved links remain missing. Contradictory binary reports make the parent unknown. [SOURCE: `parent_linkage_codebook.txt`, `analyze_family.py`.]

## Coverage and conflicts

| Original cohort, unweighted n | Supplemental only | Corrected linked + supplemental |
|---|---:|---:|
| Maternal birthplace known | 963 | 8,430 |
| Paternal birthplace known | 955 | 6,897 |
| Strict G1/G2/G3/G4+ unresolved, same definition as prior | 7,759 | 3,266 |
| Coarse G1/G2/G3+ unresolved | 7,600 | 2,221 |

Strict missingness includes 2,221 cases lacking required own/parent information and 1,045 known-US-parent cases without enough grandparent information. The prior strict count similarly included 7,600 and 159. Thus 4,493 additional strict classifications and 5,379 additional coarse classifications are like-for-like gains. [SOURCE: `family_audit.json`.]

The primary corrected derivation retains **0 maternal and 3 paternal** conflicting birthplace records as unknown. Five own-birthplace conflicts are unchanged; the retained grandparent waves have zero conflicts. Source linkage issue counts are in the audit (instances, not necessarily distinct youths): `{"nonresponding_1_birth_unlinked": 181, "responding_parent_relationship_ID_disagreement": 120, "nonresponding_2_birth_unlinked": 32}`. Rejecting a source does not establish its reported birthplace is wrong. [SOURCE: audit and `linkage_issues.csv`.]

Stored-ID checks found nonordinal PARHHI IDs in 59 records and one nonordinal HHI2 entry. An initial positional draft was therefore rejected; both final derivations join stored IDs. The exact codebook marginals and accepted source links are checked by the verifier. [SOURCE: raw roster and independent review; the temporary draft was never committed.]

## Outcome descriptions

Men with Mexican/Chicano ASVAB self-identification, positive round-21 U6365400 weight and valid outcomes. G labels abbreviate the reported-nativity definition above. Outcomes are cumulative **reported arrest and jail/adult-correctional-facility incarceration** through the 1997–2023 release: not crime incidence, conviction, current incarceration, or an age 18+ filter. Official sampling frame: 1980–1984 births resident in the US at 1997 screening. Foreign-born cohort members were childhood/adolescent residents, not representative contemporary adult immigrant inflows. [SOURCE: selected outcome codebook and [NLS sample design](https://www.nlsinfo.org/content/cohorts/nlsy97/intro-to-the-sample/sample-design-screening-process).]

| Category | Valid n | Arrest events / weighted % | Incarceration events / weighted % |
|---|---:|---:|---:|
| G1 | 28 | 13 / 44.29% | 5 / 19.34% |
| G2 | 113 | 50 / 41.73% | 19 / 16.67% |
| G3 | 46 | 22 / 49.20% | 9 / 17.30% |
| G4+ | 46 | 23 / 49.52% | 8 / 14.57% |
| Own/parent generation unresolved | 64 | 38 / 60.55% | 15 / 24.32% |
| US-born parents; grandparents unresolved | 19 | 11 / 57.49% | 4 / 17.36% |

These 316 retained men have no missing outcome; the baseline Mexican/Chicano male self-ID sample contains 452. Outcome descriptions still condition on observed self-identification and final-wave survey retention. Coarsely classified men have 16.63% weighted incarceration versus 24.32% in the unresolved category. That is measured selection across observed categories, not proof of the bias direction for unobserved people. [SOURCE: `family_analysis_rows.csv`, `classification_selection.csv`.]

Arrests and incarceration do not have the same descriptive pattern. Small cells and few events prohibit a precise generational trajectory or equivalence claim; all tables retain women, other self-identifiers and missing self-ID. Kish effective n is a weight-concentration diagnostic, not survey-design degrees of freedom. [INFERENCE from tables.]

| Parent-source sensitivity | G2 incarceration % (events/n) | G3 | G4+ |
|---|---:|---:|---:|
| Corrected YOUTH/HHI2 plus supplemental | 16.67% (19/113) | 17.30% (9/46) | 14.57% (8/46) |
| Corrected YOUTH/HHI2, without supplement | 17.88% (16/94) | 18.70% (9/42) | 15.12% (8/45) |
| PARYOUTH/PARHHI, correctly joined by stored ID | 16.37% (19/114) | 17.30% (9/46) | 14.53% (8/46) |

Supplemental-only male G3/G4+ cells had n=4/n=1. Additional history therefore changes the usable sample substantially. `linked_exact_outcomes.csv` also supplies exclusion of incomplete-history flags as a sensitivity; this is selection, not a corrected truth estimate. No survey-design standard error or causal model is claimed. [SOURCE: generated tables.]

## Analyze contract

Pipeline: parent/youth recollection → main parent interview or no-parent-interview supplement → released corrected roster IDs → explicitly linked biological-parent sources → conflicts/missingness retained → fixed prior own/grandparent waves → reported cumulative outcome → positive round-21 weighted denominator. NLS controls collection, routing, release and weights; the analysis controls mapping and residual categories. [SOURCE: codebooks and scripts.]

Leading explanation: previous extreme parent missingness was principally a questionnaire-branch mismatch. Z05018/Z05020 are the no-parent-interview branch; the main parent interview supplies much of the missing information. [INFERENCE supported by verified coverage.]

Top alternative: remaining missingness partly reflects unavailable family contact, later corrections or later own/grandparent items. Differences across categories can reflect family-history/identity/retention selection rather than an assimilation mechanism. [INFERENCE; causality untested.]

Weakest links: questionnaire geography harmonization, unresolved family history, selection and small event cells. Falsifier: a primary definition or independently corrected identity crosswalk that changes who supplied accepted birthplaces, or restricted country-region data materially changing the generation assignment. The stored-ID and corrected-YOUTH checks already killed the first draft's positional assumption. [METHOD.]

Decision impact: replace the supplemental-only descriptive table; retire the inference that most public parent nativity is unavailable. Do not promote monotonic worsening, parity, null, genotype or Mexican-genealogical claims. Next action: integrate the verified scripts and source-tagged categories; design-based inference and territory harmonization are needed before stronger claims. [INFERENCE.]

LLM bias check: both contradictory outcome patterns and the high-outcome unresolved group are retained. The evidence does not license selecting the result most congenial to either assimilation or worsening. Primary field semantics and independent reconstruction anchor the result. [METHOD.]

## Verification and files

Verification **PASS**: 31,106 accepted source records across both mappings, all four birthplace marginals, 16 HHI2-ID marginals, exact reproduction of the old supplemental classifier and unchanged outcome values; **792 weighted cells across 9 tables** independently re-tabulated. A separate agent rebuilt corrected parent values and exact categories for all 8,984 records from the raw selected fields and reproduced the key weighted rates.

Source archive: `/Users/alien/Projects/iq-sex-differences/data/nlsy/nlsy97_all_1997-2023.zip`, 475,462,343 bytes, registered SHA256 `8c513e4804e5b07fce0e6b913258747dcf8707c73bb9ae54cce88dbff6d23c28`. Streamed 104 selected fields for 8,984 PUBIDs; four non-ID fields overlap and exactly match the prior 98-field extract. No raw archive changed. [SOURCE: extraction and prior baseline provenance.]

From the repository root, run the following. Extraction verifies the full archive SHA-256 before selecting fields. Outputs default to the lane's ignored `derived/nlsy_family/`; extraction accepts `--archive` and `--output-dir`, and analysis/verifier also accept `--lane-dir`.

```bash
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/extract_family.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/analyze_family.py
uv run python3 infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/verify_family.py
```

The [104-field basket](../infra/immigration-fiscal/new_datasets_2026_09_17/nlsy/parent_linkage_fields.NLSY97) records the additional linkage inputs. All are already held; no further browser export is necessary. Final independent reconstruction covered all8,984 classifications, including the nonordinal HHI2 record: its main parent interview is absent, its parent values come from supplements, and the stored-ID correction changes no final rates.

Covered: existing full archive selected fields, prior 98-field data/codebook, prior outcome rows and all new tables. Other datasets are covered in the [collection synthesis](immigration-organized-surveys-analysis-2026-09-17.md). Restricted geocodes remain unavailable; later own/GP waves were held fixed to isolate parent reconstruction; causal/design-based significance models are outside this measurement repair.
