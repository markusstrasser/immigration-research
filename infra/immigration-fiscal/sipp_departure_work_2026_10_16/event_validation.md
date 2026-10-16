**Verdict:** The candidate separations are internally consistent survey-record departures, not observed slot-reindexing artifacts. After reconciling the baseline-age rule, the parent's predeclared three-month pre-co-residence / first-eligible-event rule retains **149 tracked focal adults** and **278 Type-2 focal adults** before outcome availability. Every parent pair flag was independently reproduced. These are household separation samples, not identified deportations. Composition and return patterns materially limit transport to the v9 household-removal question. No employment, hours, or earnings effect was examined in this audit.

## Scope and instrument

Read the official 2025 SIPP dictionary and guide first, then independently reconstruct candidates from the prior selected extract, joining new identity/household/allocation fields directly from the original public raw archive. All work remained in this ignored scratch directory. No pre-existing files edited; no commits. Public microdata identifiers appear only in ignored CSV/Parquet files, not this memo.

Sources:

- [2025 SIPP guide](https://www2.census.gov/programs-surveys/sipp/tech-documentation/methodology/2025_SIPP_Users_Guide.pdf), printed pp.19–21, 34–35, 41, 53–54, 60. Local text: `.model-review/household-response-evidence-2026-10-16/data/sipp2025-guide.txt`, lines780–844,1398–1427,1723–1740,2292–2311,2574–2608.
- [2025 dictionary](https://www2.census.gov/programs-surveys/sipp/tech-documentation/data-dictionaries/2025/2025_SIPP_Data_Dictionary.pdf), printed pp.6,875,1237,1245–1246,3240,3244,3262–3263,3282. Local `dictionary.txt` contains exact extracted text with variable anchors.
- [Original raw archive](https://www2.census.gov/programs-surveys/sipp/data/datasets/2025/pu2025_csv.zip), local `sources/immigration-fiscal/data/external/stage3/census/sipp_2025/pu2025_csv.zip`; earlier source receipt SHA256 `570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed`.

Authoritative definitions:

1. PNUM stays fixed through a panel and is unique within SSUID. ERESIDENCEID identifies a monthly address, unique within SSUID; a change records a move. Movers are followed, but persons abroad, institutionalized, or in military barracks are not interviewed.
2. THHLDSTATUS is a **person-level** household-status field:1 returning,2 new,3 partial reference year (including death, institutionalization, active duty, or abroad),4 mover,5 prior-wave listing error,6 inactive. **RIN_UNIV**, not THHLDSTATUS alone, establishes the monthly survey-frame universe.
3. Type-2 people never have interviewed person records in the release. The 2025 dictionary constrains ET2_LNO1 to60, ET2_LNO2 to61, etc. Values populate only when that Type-2 person is co-resident that month. Thus the columns are fixed identities within the respondent's roster, not compacting array positions.
4. RREL19 means **other nonrelative**. RREL is constructed from residence, interview relationship, spouse/partner/parent pointers, and other family records. There is no RREL-specific allocation flag. It is not an independently reported roommate response. Relationships should be reciprocal.
5. Allocation flag1 is as reported;3 is logical imputation. The residence flags encountered here were1 or3. Logical allocation is not proof that the move is false.

## Independently reproduced candidates

`audit_events.py` reproduced the prior tracked totals exactly:286 directed focal–departing-adult pairs,232 focal event-months,214 focal adults,160 departing-adult/month combinations. The tracked definition requires both adults at the same address at t−1, both observed at t, the focal remaining at the old address and the other changing address at t; focal age18–64.

The Type-2 identity-set difference reproduced **599 focal event-months /544 focal adults**, representing745 directed focal–Type-2 disappearances after excluding final-status5/6. The prior600/545 screen included one invalid household-status candidate.

Checks against alternative explanations:

- All286 tracked pairs: departing identity present in the focal's RREL_PNUM array at t−1 and absent at t. All745 Type-2 pairs pass the analogous check. These are internal consistency checks using related survey recodes, not independent external confirmation.
- All282 tracked raw pairs where the departing adult is in the monthly universe have TMOVER2–7; all283 in-universe focal records have TMOVER1. The remaining raw cases have missing mover recodes/out-of-universe status and do not enter the main valid-universe sample.
- Zero Type-2 slot-vs-set disagreements; zero values inconsistent with slot1=60,slot2=61,etc.; zero interviewed PNUMs below100.
- Across **2,019 focal-person /Type-2 identity histories**, zero changes in recorded Type-2 age or sex during2024. This gives no observed evidence of identity reuse or shifting within a respondent's annual roster.
- No unique-person claim is made for a Type-2 ID shared by different focal respondents. Cross-focal Type-2 linkage is not established by this audit; use focal event counts for that sample.

## Initial reconstruction of the primary timing rule

`refine_protocol.py` applies the timing rule independently: t in April–October; focal and departing adult co-resident for t−3,t−2,t−1; focal stays at t; valid survey-frame records through t; focal age18–64 and other adult throughout the pre-window; first eligible event per focal. This initial pass inherited the prior candidate screen's age18–64 restriction at t as well. The final reconciliation below removes that unintended extra restriction; the table is retained as the audit trail. Later focal moves and returns are retained. Post outcomes have not been read or used for selection.

| Sequential rule | Tracked pairs /focal event-months /adults | Type-2 pairs /focal event-months /adults |
|---|---:|---:|
| Original candidates |286 /232 /214|745 /599 /544|
| Event April–October |217 /182 /171|582 /454 /423|
| Three prior records |217 /182 /171|582 /454 /423|
| Three prior co-resident months |194 /161 /151|350 /285 /280|
| Valid survey universe through t |191 /158 /148|348 /283 /278|
| Pre-window adult-age rules |191 /158 /148|348 /283 /278|
| First eligible event per focal |**180 /148 /148**|**343 /278 /278**|

The first-event samples span78 and145 SSUIDs respectively. Multiple departing adults at the same focal event remain represented in the pair files; do not count the focal adult's outcome twice.

Post observation diagnostics only:

- Tracked:147 of148 focal adults have all three post records;146 have all three post records in-universe. Actual outcome-specific availability is the parent's task.
- Type-2:277 of278 focal adults have all three post records, all in-universe.
- Among first-event samples,41 tracked focal adults and14 Type-2 focal adults have a later reunion before year-end. These counts are descriptive, not exclusions in the primary rule.
- Requiring three separated post months and both observed/in-universe where applicable leaves128 tracked and274 Type-2 first-event adults. This is a persistence sensitivity, with selection on future residence/survey observation.
- Requiring **all pre-through-t residence IDs as reported** leaves91 tracked and232 Type-2 focal adults. Do not call the omitted logical-imputation records fabricated moves.

For comparison only, screening for persistence *before choosing first events* yields130 tracked and274 Type-2 adults. This differs from choosing the first primary event and then checking persistence (128/274). Parent should keep its first-event rule fixed across sensitivities.

## Composition and transport (initial148 tracked-adult subset)

`composition.py` reads ESEX,SHHADID,EHRESIDENCID,ERELRPE and ARELRP from the original archive. It computes no labor outcomes.

Among180 tracked directed pairs at the148 first events:

-131 are coded other nonrelative;20 biological parent/child;11 other relative;5 biological sibling;5 unmarried partner;2 grandparent/grandchild;2 stepparent/child;2 spouse;1 adopted parent/child;1 other sibling.
- The nonrelative coding persists in the as-reported-residence subset:69 of94 pairs. It also appears in130 pairs with both persons' interview relationship flags as reported. This does not validate every constructed historical RREL value.
- Every pair's relationship is reciprocal. One tracked pair changes relationship during the three pre months; two Type-2 pairs do. There are no tracked pairs with the same interview-address ID but different SHHADID (the guide's rare shared-address/multiple-household exception).
- Focal ages:39 aged18–24,32 aged25–44,77 aged45–64;79 male,69 female. Among98 tracked departing identity-events,51 aged18–24,32 aged25–44,11 aged45–64,4 aged65+;43 male,55 female.
- This older-stayer/younger-mover composition should prevent casually translating RREL19 into 'roommate departures.' The code is explicit, but family-history construction is not externally validated here.
- Among98 departing identity-events, stated reasons:15 relationship change,15 other family reason,14 closer to work/school,11 other,9 own apartment/house,9 other housing/neighborhood,8 own rather than rent,6 cheaper housing,5 new job/transfer,3 better neighborhood,1 lost job/job search,1 eviction/foreclosure,1 better-quality home.97 of98 reasons are as reported. These remain potentially endogenous moves.
- All98 departing identity-events have domestic TMOVER2–7:43 same county,33 different county within state,22 interstate.

Among343 Type-2 directed pairs at278 first events,92 biological parent/child,81 other nonrelative,73 other relative,17 parent/child-in-law,17 stepparent/child,16 unmarried partner,13 other sibling,10 grandparent/grandchild,8 aunt/uncle/niece/nephew,5 sibling-in-law,5 spouse,2 half-sibling,2 adopted parent/child,1 adopted sibling,1 biological sibling. Focal ages:63 aged18–24,93 aged25–44,122 aged45–64;134 male,144 female. Departing-person destination/reason is unavailable in this Type-2 route. The interview timing and proxy-history selection differs from tracked movers; report separately.

## Concurrent changes and remaining gaps

- In the tracked sample, household size falls for141 of148 focal events, stays level for5 and increases for2. Two focal events have interviewed-person arrivals and five have Type-2 arrivals. An actual departure can coexist with arrivals; the focal's change is not necessarily the response to one person's loss alone.
- In the Type-2 sample, household size falls for271 of278 focal events and stays level for7. Four have interviewed-person arrivals and six Type-2 arrivals; these sets can overlap.
- [GAP] The survey's retrospective monthly histories and deterministic recodes are not external address verification. No raw interview recording or administrative address linkage is available here.
- [GAP] RREL19 has no separate allocation flag; no primary source inspected here documents whether unknown historical relationships can fall into19. It must be described as the released code, without treating all as proven roommates or all as imputation artifacts.
- [GAP] The Type-2 departure reason, destination, true date, and cross-focal identity linkage cannot be independently confirmed from these fields. The data give retrospective co-residence histories, not confirmed deportation dates.
- [GAP] Selective follow-up, moves abroad/institutionalization and interview-time household selection remain substantive sample limitations. Validity of the within-person descriptive outcome calculation belongs to the parent analysis and is not established by these identity checks.

## Files and handoff

- `audit_events.py` / `audit.json`: independent baseline reconstruction and strict-window sensitivities; `identity_extract.parquet` is an outcome-blinded raw-data join.
- `refine_protocol.py` / `protocol_audit.json`: exact parent timing rule and sequential exclusions.
- `tracked_primary_first_pairs.csv` / `type2_primary_first_pairs.csv`: ignored person-level keys for parent's reconciliation, not public output.
- `composition.py` / `composition.json`: demographics, relationship/move-source consistency, concurrent arrivals.
- `type2_identity_stability.json`: within-focal age/sex consistency diagnostics.
- Covered: original2025 archive identity fields, selected2025 extract, official2025 guide/dictionary. Skipped:2023/2024 data (not needed for within2024 measurement validation), all work outcomes (explicit blinding), causal estimation and papers (outside assigned scope).

## Final reconciliation with parent (2026-10-16)

`reconcile_parent.py` reads only identity/event fields from the parent's `_cache/pairs.parquet`; no work outcomes are loaded. Comparison against the independently reconstructed key sets and the original identity extract establishes:

- Tracked parent181 pairs /149 focal adults versus initial audit180 pairs /148 adults: **exactly one** extra pair/adult, no audit-only pairs. This adult is64 in each of the three pre months and turns65 at t. All pre co-residence, focal-stay, other-move and universe checks pass. Under the parent's declared **baseline** working-age rule this is correctly included. No source anomaly.
- Type-2 parent343 pairs /278 adults: exact identity-set agreement. Canonicalization of parent zero-padded IDs060 vs audit60 is required; after canonicalization no unmatched pairs remain.
- All524 parent directed-pair `reported_residence`, `persistent`, and `returned` flags independently reproduce, with **zero disagreements**. All181 tracked pairs also meet the raw residence-spell boundary: departing adult's new spell begins t and former spell ends t−1.
- Event-level aggregation uses **all departing pairs** for reported/persistent flags, and **any pair** for returned. This is stricter than retaining a focal if merely one of multiple departure pairs passes. The parent's reported rule requires residence-ID **and** spell-start **and** spell-end allocation flags to be1 across the pre-through-t records; the earlier ID-only91/232 counts are not comparable.

| Final event definition /sensitivity | Tracked | Type-2 |
|---|---:|---:|
| Primary first eligible event |149|278|
| All relevant residence and spell flags as reported |61|223|
| All departure pairs remain apart in t,t+1,t+2 |129|274|
| Any departure pair reunites in t,t+1,t+2 |18|3|

The earlier41/14 return counts used any reunion through the end of the year, and the initial tracked-age screen. They are not the final three-month-return sensitivity. Final reconciliation output: `parent_reconciliation.json`. Parent owns the final composition/outcome tables; the exploratory initial148-adult composition above is explicitly retained as an audit record rather than silently relabeled149.

Leading explanation: these are **survey-recorded household separations** with many short spells/returns and a mixed relationship composition. Main alternative: errors or deterministic reconstruction in retrospective residence/relationship histories, rather than slot movement. External address/person linkage would distinguish them. Decision impact: proceed with a descriptive, outcome-specific analysis, separate tracked and Type-2 routes, retain the primary first-event set across sensitivity analyses, and do not calibrate v9 as a deportation response.
