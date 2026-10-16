**Verdict:** The public SIPP files can validate a bounded cohort of observed adult residential separations and measure the remaining adults' reported work around them. The cleanest events require both adults to remain individually observed, the focal adult to remain at the old address, and the other adult to move to a different address. This does not identify deportation or an exogenous household loss. Three coding issues materially matter: partial-month employment is `RMESR=4–5`, missing job earnings/hours are not automatically zero, and unpaid family workers can be employed with no paid-job earnings.

Scope: official 2025 SIPP Users' Guide, official 2025 data dictionary, and full public schema; no outcome estimates or new dataset search. Prepared 2026-10-16. Guide page references are printed page numbers; dictionary page references are its printed pages.

## Sources and coverage

- [2025 SIPP Users' Guide](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2025_SIPP_Users_Guide.pdf), local `sources/immigration-fiscal/data/external/stage3/census/sipp_2025/2025_SIPP_Users_Guide.pdf`. Read sections 2.3–2.6, 3.2.4–3.5.7, 4.1.11, 4.2.3, 4.7.1 and 7.2–7.3. Local cover July 15, 2026, document history contains August 2026 revision.
- [2025 data dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf), local `.scratch/clarity-next-20260905/admission/sipp2025_dictionary.pdf`. Relevant entries extracted below; full text derived in this folder as `dictionary.txt`.
- [2025 schema](https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/pu2025_schema.json), local `.scratch/clarity-next-20260905/admission/pu2025_schema.json`. Verified actual exposed names, including suppressed job 7 and absent job 8 date/hour fields.
- Existing `notes/v9-household-response-evidence-2026-10-16/data.md` was consulted only to locate the earlier unresolved missing-earnings diagnostic after forming the definitions from primary docs. No earlier outcome estimate was adopted.
- Skipped: raw adult outcome re-estimation (parent's lane); multi-year panel construction; external departure studies; fiscal model and figures. These cannot improve this definition audit and are outside ownership.

Current source SHA256 checks (read-only, 2026-10-16): guide `0f0bfbc9bbd0de97d8cfd07ec3128925159c9696d259893e04aa1e6f5d17ba41`; dictionary `571e53b4ec3ebb11bebddbb7190fc1084f5364b8a1ec5fbd7ca8e2f69e7cc752`; schema `6cdc23c537ba1431540e62994f0c05e05e62920e785384872bf5b7c23fe8c241`.

## Identity, residence and event timing

`SSUID` remains with original sample people and new people who join them even after a split to a spawned household. `PNUM` is unique within `SSUID` and unchanged across the panel. In the 2025 file the last two SSUID digits indicate panel year; `SPANEL` can be retained as a consistency check, but the guide explicitly identifies `(SSUID,PNUM)` as person identity. Monthly residence is `(SSUID,ERESIDENCEID)`; never equate residence numbers across different SSUIDs. Interview address identifiers (`EHRESIDENCID`, `SHHADID`) are not substitutes for monthly residence. [Guide pp33–35.]

`ERESIDENCEID` is a six-digit monthly address ID, with flag `ARESIDENCEID`. A month-to-month change denotes a residence change. The first digit marks first wave of address appearance, not chronological order within a person's history. `ERH_BMONTH`, `ERH_EMONTH` delimit the residence spell (flags `ARH_BMONTH`, `ARH_EMONTH`). `TMOVER=1` means same house; 2–7 different US house by geography; its `AMOVER` flag reports imputation. `TMOVER` identifies the first month in the new residence. [Dictionary pp1237, 3240, 3242–3243; guide pp34,60–62.]

Residence history and mover flags are edited for consistency, but the guide explicitly permits a small number of ID-change/`TMOVER` disagreements: respondents may say they have always lived at the new address (`EEHC_WHY=15`). Therefore requiring mover corroboration produces a stricter sensitivity cohort; a disagreement alone is not proof the ID-based event is false. Describe/count disagreements instead of silently fixing them. [Guide p62.]

`EEHC_WHY` describes the move **into the residence on that person's spell**, so read it on the departing adult's new residence, not the stayer's old residence. Codes: 1 marital/relationship change; 2 own apartment/house; 3 other family; 4 new job/transfer; 5 look for work/lost job; 6 closer to work/school; 7 other job; 8 own rather than rent; 9 better housing; 10 better neighborhood; 11 cheaper housing; 12 other housing/neighborhood; 13 disaster; 14 eviction/foreclosure; 15 always lived here; 16 other. There is no deportation code. Job-related causes are explicit evidence of endogeneity. [Dictionary p3244.]

`THHLDSTATUS` is person-level, not a monthly exit indicator: 1 returning household member; 2 new household member; 3 partial-reference-year member (examples death, institution, active duty, abroad); 4 mover; 5 listed in error prior wave; 6 inactive in household. `RIN_UNIV` is the monthly in-frame indicator: 1 in universe, 2 out. Event validation should require monthly in-frame observations and not treat statuses 3 or 4 alone as evidence of a departure date/cause. [Dictionary pp1245–1246.]

SIPP attempts to follow original sample movers. It does not interview people abroad, military-barracks residents, or institutionalized people. New household members are interviewed only while living with an original sample person. Consequently, a cohort requiring both adults' observed post-departure addresses selects domestic, observed separations; it cannot estimate effects of foreign departure or incarceration/deportation from those rows. Temporary absence with a usual residence retained is not a move. [Guide pp19–21.]

### Recommended event contract [INFERENCE from definitions]

1. Retain unique person-month keys, nonmissing monthly addresses, positive selected cohort weights, and valid adult ages. Require both adults in-frame and co-resident in the pre-event months.
2. Define event month `t` as the first month in which the other adult's ID differs from the old shared address while the focal adult keeps the old address. Require the departing adult's new address to differ from the focal adult's address. A whole-household move does not qualify.
3. Corroborate against month-matched RREL person-ID sets, residence-spell boundaries, and `TMOVER`; report agreement and exceptions. These checks share source information and are internal consistency checks, not external verification.
4. For a persistent separation cohort require the focal adult to stay at the old address and the other adult to remain elsewhere over the post window. Report temporary separations/returns separately rather than silently recoding them. Require available pre/post windows independent of outcome values.
5. Group simultaneous other-adult departures into one focal-person event; report how many departed. Avoid treating two departing people as two independent copies of the same stayer's work response. Either select one predeclared event per focal adult or account for repeated events.
6. Describe other simultaneous entrances/departures and relationship type. A strict stable-roster sensitivity is useful, but restricting it defines a narrower cohort rather than magically removing confounding.

## Type-2 people and relationship slots

Type-2 people lived with a respondent during the reference year but are absent at interview. They have no own person-record; respondents provide proxy information. Up to ten are assigned PNUM 60–69. Fields are populated only in months of co-residence. `ET2_LNO1=60`, `ET2_LNO2=61`, ..., `ET2_LNO10=69`; thus the field value is a slot-specific person-number marker, not an arbitrary permanent ID. The guide does not establish that a Type-2 code has stable identity across waves or all respondents/addresses. [Guide p41; dictionary pp3262–3271.]

The relationship vectors **must be joined by their `RREL_PNUMx` values each month**, never by x-position. The official guide p39 example shows that when person102 leaves, person103 moves from `RREL_PNUM3` to `RREL_PNUM2` for the remaining person101. Thus a disappearing relationship position is not evidence of an actual person exit. [Guide pp38–39.]

For an ancillary within-year Type-2 cohort, compare sets of Type-2 person IDs rather than nonmissing slot counts; check age/sex/relationship consistency, no offsetting slot identity replacement, stable focal address, and no reappearance in the post window. Report it separately from tracked adult departures because the missing person's destination/cause and independent post-departure presence cannot be validated. The strongest initial result should use individually tracked departures rather than needing to combine channels.

## Work measurement and defensible zeros

| Variable | Official definition and universe | Coding implication |
|---|---|---|
| `RMESR` / `AMESR` | Monthly employment status, age15+. 1 job all month/worked all weeks; 2 job all month/unpaid absence not layoff; 3 job all month/unpaid absence due to layoff; 4 job some but not all weeks/no layoff or search; 5 job some weeks plus layoff/search; 6 no job/on layoff or search all weeks; 7 no job/some layoff or search; 8 no job/no layoff or search. Dictionary p2489. | `RMESR in 1:5` = any employment in month; `1:3` = with job all month, a distinct sensitivity outcome. `6:8` = no job throughout month. All other/missing values stay unknown. Do not drop partial-month jobs. |
| `RMWKWJB` / `AMWKWJB` | Number of weeks with a job in month, 0–5, age15+. Dictionary p2486. | Useful corroboration of employment and zero rules; not independent source validation. |
| `TMWKHRS` / `AMWKHRS` | Average hours worked per week across all jobs held during month; universe at least one job on lines1–7; allowed0–99.99. Dictionary p2579. | Already an aggregate; do not sum it across jobs or mistake it for total monthly hours. Numeric zero is valid, including unpaid absence. Missing for a genuine no-job month may be structural zero; missing for an employed person remains unresolved. |
| `TPEARN` / `APEARN` | Earnings plus profits/losses across jobs, varies with days in month; universe job lines1–8. Dictionary p2581. | Preserve negatives, numeric zeros, and reported numeric values even when employment status differs. Do not restrict to positive earners or silently zero unresolved missing employed rows. |
| `TPEARN_ALT` / `APEARN_ALT` | Same earnings components/universe; removes variation from month length. Dictionary p2631; guide126–127. | Prefer this as main comparable monthly earnings outcome; TPEARN is the calendar-dollar sensitivity. It includes wages, salaries, bonuses, commissions, overtime, tips, self-employment income/profits and unpaid absence adjustments. |

The public schema exposes job1–6 `EJBn_BMONTH` / `EJBn_EMONTH` fields. Job7 date fields are explicitly suppressed; job8 dates are absent. The guide says additional-job summary information enters employment and earnings recodes without appearing directly on the edited file (p72). Therefore lack of a public active job1–6 spell does **not**, by itself, establish no work. Use the official aggregate outcomes and status flags before reconstructing from incomplete job lines.

### Unpaid family work is an important exception

Official employment includes people working at least15 hours unpaid in a related household member's family business/farm. `ENJ_UPDWKYN=1` and `ENJ_NOWRK11=1` can identify this channel; their flags are `ANJ_UPDWKYN` and `ANJ_NOWRK`. The former is asked during no-paid-job weeks when another household member age15+ exists; the latter is a reported reason for no paid job. These variables do not mean that the person never had paid work in other weeks of the same month. [Guide p73; dictionary pp2745,2747.]

**Missing with `RMESR=1` is not necessarily contradictory:** the employment definition can include unpaid family work outside paid-job earnings/hours universes. For a row with blank earnings, earnings flag0, explicit unpaid-family work and no corroborated paid job, a zero earnings interpretation is supportable; keep that branch separately counted and report the exact rule. A blank hours value for such a person cannot be filled with zero if the outcome is *total work*: the source says at least15 unpaid hours. Either label the outcome paid-job hours or leave total hours unknown. Mere absence of visible job1–6 dates is insufficient evidence because public job coverage is incomplete.

Recommended conservative rule: retain any numeric aggregate amount as provided; fill missing hours/earnings with zero only for `RIN_UNIV=1`, `RMESR in 6:8`, corresponding allocation flag0, and no conflicting active public job spell. Keep missing employed rows unknown pending row-level resolution. The optional explicit unpaid-family earnings branch should be separately shown; never assume its missing total hours are zero. Cross-tab outcomes by employment, flags and job-spell agreement before applying this rule, and show exclusions by outcome. [INFERENCE, intentionally more conservative than unconditional missing-to-zero.]

### Allocation and recall

For all these flags: 0 not in universe; 1 reported; 2 hot-deck; 3 logical; 4 model-based; 5 cold-deck; 6 imputed from range; 7 reported plus imputed components; 8 imputed components; 9 inspect component flags. A9 is not “reported” or “missing.” If an aggregate is mostly A9, an A1-only restriction is not a meaningful no-imputation sensitivity; inspect underlying components or label the limitation. Residence flag9 also cannot simply be assumed to mean unallocated. [Guide p32.]

Exact public component names are saved in `component_flags.json`, generated by `extract_components.py` from the full original schema, retaining only non-suppressed fields. Its `names` array contains393 flags: timing46, hours37, unpaid absence44, earnings235, and nonemployment31. Hours' raw values are `TJBn_JOBHRS1/2/3` with `AJBn_JOBHRS1/2/3`; timing of changes is `CHHOUR`, `CHHOMN`, `CHHOWK`. Earnings include pay types/rates and their changes, bonuses/commissions/tips/overtime, business profits/losses, salary to owners, and other business income. Recoded job-level `AJBn_MSUMALT`, `AJBn_MWKHRS`, or `AJBn_WKSUM` can themselves be9 and do not by themselves resolve provenance. A sensitivity requiring visible raw component flags in `{0,1}` should be called **no flagged allocation in the visible components**; the public fields cannot prove every suppressed/undisclosed component was unallocated. This is a conservative screen of relevant public inputs, not a replicated official derivation of every aggregate.

SIPP hours are recalled usual/average weekly hours, with up to two changes per job spell; wage/salary rates similarly allow two changes. Earnings and hours are derived monthly records from those spell reports, not payroll timecards. Overlapping job/nonwork spells can occur (`ROVERLAPMN`). This limits claims about tiny short-lived adjustments. Treating imputed values as observed understates variance; a no/low-allocation sensitivity and allocation shares are warranted if substantial. [Guide pp70–74,156.]

## Weights and uncertainty

For a cohort observed within calendar2024, the guide **recommends** December `WPFINWGT` as the calendar-year weight. It does not prescribe an additional multi-year weight for a six-month within-year contrast. The target must be explicit: December-covered people with the event and valid comparison window. FINYR2/3/4 apply to reference2023–24 /2022–24 /2021–24, respectively; they are needed if the target crosses those year spans, not because the outcome has several monthly observations. [Guide pp156–160, Table7-1; dictionary3256–3258.]

A baseline-month weighted estimate is a permissible sensitivity for a baseline-defined population but does not inherit the documented annual/longitudinal attrition adjustment. Neither December nor baseline weights automatically repair selection from requiring both adults' post-move observations, available outcomes or an enduring separation. State that selection limit rather than claiming a representative causal effect of all departures. [INFERENCE from guide's population/duration rule and following rules.]

Use the **same December full/replicate weight per person** for both sides of a within-person contrast. Build one person-event pre/post difference, then its weighted mean; separately weighted pre/post cross-sections can change composition. Merge monthly replicates on SSUID,PNUM,MONTHCODE before selecting December. Recompute the complete nonlinear statistic (including any fixed matching/normalization) under each replicate. [INFERENCE applying official weight method.]

2025 has240 replicates and Census recommends Fay modified BRR with k=.5:

`Var(theta) = sum_r (theta_r - theta_full)^2 / [240 * (1 - .5)^2]`.

Use the full-sample estimate as the center (`mse` convention), not mean replicate estimate. The guide also provides `GVARSTR` strata and `GHLFSAM` variance units as an alternative design specification. Do not bootstrap person-months independently. Repeated stayers/family members share design clusters; the replicate weights propagate that sampling dependence. These are design-based sampling intervals, not full uncertainty about event validity, imputation or causal attribution. [Guide pp153–156.]

## Interpretation and remaining gaps

Leading interpretation: measured trajectories describe the selected observed domestic-separation cohort. Top alternative to a response caused by departure is joint determination: relationship changes, job changes or financial pressure can move both residence and work. Discriminating evidence includes pre-event trajectories, calendar-month comparison trajectories, cause-specific descriptive rows and unchanged-address/no-departure checks. They can expose inconsistency or background trends, but do not by themselves establish causal identification.

Decision impact: proceed with a bounded descriptive estimate after the contracts above. Preserve nulls and imprecise effects. A numerically nonzero change is not a deportation elasticity or a v9 update.

[GAP] The raw selected cohort's allocation distributions and employment/earnings discrepancies are not resolved in this definitions subtask; parent must count/inspect them before estimation.
[GAP] Public docs do not establish Type-2 identity permanence across waves. Do not infer it from a constant slot code.
[GAP] The guide describes construction but does not supply source code for the exact RMESR/aggregate-income derivation. Remaining inconsistent paid-job rows should stay unresolved, rather than repaired by guessing.

Suggested follow-up only if a material ambiguity remains: inspect the exact selected discrepant rows using `ENJ_UPDWKYN`, `ENJ_NOWRK11`, job dates, `RMWKWJB`, earnings/hours/status flags; consult the official instrument for the specific branch. No broader dataset acquisition is required to execute the currently authorized within-year test.

## 2026-10-16 appended raw component-allocation diagnostic

**Verdict:** The underlying public component flags support a reproducible allocation sensitivity. The direct aggregate-flag-1 test is invalid. This is a full-file measurement diagnostic, not a departure-cohort effect estimate.

Ran `probe_component_allocation.py` once against the original archived 2025 CSV in chunks of 20,000 rows; exit 0, 63.113 seconds. It read 393 exact component flags from `component_flags.json`, three key columns, and the three aggregate outcome/flag pairs solely to verify recode flag use. It wrote reduced row summaries and discarded raw component values each chunk. All 379,215 rows have unique, nonmissing `(SSUID, PNUM, MONTHCODE)` keys; output has 84 columns, 19 row groups, and occupies 1,438,925 bytes. A separate readback checked row count, unique keys and all 12 reference months.

The diagnostic does not select adults or estimate work trajectories. The following denominators are **all person-months, including children and inapplicable job fields**; they must not be quoted as adult job imputation rates.

| Screen | Exact component groups | Flag count | Person-months with any flag 2–8 | Person-months with all visible flags 0/1 |
|---|---|---:|---:|---:|
| Employment | Job presence/timing + nonemployment | 77 | 67,522 | 311,693 |
| Hours | Job presence/timing + hours + unpaid absence | 127 | 55,829 | 323,386 |
| Earnings | Job presence/timing + hours + unpaid absence + earnings | 362 | 113,164 | 266,051 |
| All visible | All five base groups | 393 | 130,328 | 248,887 |

No selected component flag was missing or equal to 9 anywhere in this release. Thus `observed_clean` and `complete_clean` happen to coincide; the output preserves both and missing/unresolved counts so a later source change cannot silently change their meanings. A component flag 0 means not in universe, not a reported work value. The clean label means **no flagged allocation in these visible components**, not proof that suppressed/undisclosed inputs were unallocated.

All nonmissing `RMESR` outcomes (326,099 rows) have `AMESR=9`; all numeric `TMWKHRS` outcomes (172,730) have `AMWKHRS=9`; all numeric `TPEARN_ALT` outcomes (172,755) have `APEARN_ALT=9`. The remaining rows have corresponding flag 0. No flag-1 aggregate row exists. These counts independently reproduce the parent's observed flag-9 issue from the original archive.

Files: `probe_component_allocation.py`; `component_allocation_totals.json`; `component_allocation_receipt.json`; ignored `component_allocation.parquet`. The local `.gitignore` ignores Parquet and Python bytecode. Receipt records the raw SHA256, exact definitions SHA256, script SHA256, category membership, semantics, timing, output SHA256 and status. Raw ZIP SHA256 remains `570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed`; Parquet SHA256 is `02bfda8cefa9379c57c10a7f653895cbb773248a2aa39c36afefe01130a3a447`.

No repeated full scan was needed: runtime stayed below two minutes. No existing project source, raw dataset, model, figure or effect estimate was changed. [GAP] The parent still needs to join these row diagnostics to the selected departure cohort and summarize allocation/exclusions there; full-file counts cannot substitute for that cohort check.
