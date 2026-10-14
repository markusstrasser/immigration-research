**Verdict:** The primary departure correction locates **517,863 biological children inside the existing latent-loss definition**. Remove these children in the survivor calculation, subtract their old **$0.080993bn** crossing-credit projection once (SE $0.009493bn), and retain the fixed 42.75M priced lineage. The broad biological-child departure arm has 853,468 children; 335,604 lie outside the existing loss definition, so this broader mask requires a separate own-cost rebase before adoption. Reject a blanket −$1.033bn duplicate-credit correction: the traced duplicate is the subset's $0.081bn projection, not the claimant's credit merely being on a union record. [CALCULATION: `membership.py`, `derived/membership.json`, `derived/membership_replicates.csv`]

## Membership and conservation

Children leave when a type-1 biological parent is a lineage member. A type-2 step parent alone does not make a child leave. The primary subset also requires the child to be a native civilian under 18, not report Mexican origin, have both parent-birthplace fields in US areas, and have at least one actual native biological member-parent record. This is the existing 3.04M addition's multiplier universe, rather than an extra population added on top of it. [SOURCE: [Census ASEC 2025 public-use dictionary](https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf), PEPAR1TYP/PEPAR2TYP; DATA: `main_case_lineage_2026_10_05/population.py`, existing case's lineage metadata]

| Located group | Persons | Treatment |
|---|---:|---|
| All additional biological native civilian children | 853,468; SE 75,514 | Broad departure arm only |
| Primary latent-loss subset | 517,863 | Substitute for part of the existing latent count |
| G3-rate child loss: biological G2 member parent | 250,290 | Existing (1−C3) G3+ / C3 white price blend |
| Later loss: biological G3+ member parent | 267,574 | Existing G3+ pricing |
| Roster subset priced G3+ / white | 378,527 / 139,336 | Split fixed C3=0.5567; no observed economic reclassification |
| Unlocated added pool priced G3+ / white | 1,578,471 / 943,385 | Residual pool for transport |
| Outside current latent-loss definition | 335,604 | No silent own-cost inclusion |
| Included above: contradictory parent fields | 42,996 across 17 records | Child says two US parents, linked member parent is Mexico-born; exclude from latent pool |
| Step-parent-only children | 74,754; SE 15,659 | Stay |

[CALCULATION: `derived/membership.json`]

The original union, located latent subset, and unlocated latent residual are disjoint accounting compartments. Located+unlocated equals the existing 3,039,720 addition in every full/replicate column; no population or own fiscal cost is added. R3′ membership changes survivor tax/benefit eligibility and crossing credits only. Native children excluded from the latent definition are shown separately and never declared absorbed by the invisible aggregate. Parent-generation classification and the unchanged C3 price blend are assumptions about the case's pricing classes, not a person-level match to previously invisible records. [CALCULATION: membership gates; ASSUMPTION]

`expanded_context(c,x,d,case,latent_only=True)` rebuilds R's member/dependent counts and generations, with original row order, spouse order and dependent-return links gated unchanged. It preserves original baseline amounts, item5b component arrays, national keys and all 161 weights. Rebuild gates are captured separately so the original positive-control gate count stays unchanged. `latent_mask(d,union,civ)` is the shared definition for standalone health and SNAP frames. [CALCULATION]

## Credits and D

| Diagnostic or correction, $bn | Full sample | Replicate SE | Recommendation |
|---|---:|---:|---|
| R3→R3′ broad equal-child reverse-credit reclassification | +0.575422 | 0.096799 | Diagnostic; replace with nonlinear joint tax solve |
| Its B nonrefundable / care / ACTC / EITC | +0.336948 / 0.015454 / 0.093794 / 0.122820 | In replicate file | Diagnostic only |
| Its Cr status | +0.006406 | 0.003787 | Diagnostic; exact filing-status solve supersedes pro rata split |
| Primary roster's existing item5b projection removed | **−0.080993** | **0.009493** | Measurement/accounting correction inside primary arm |
| Original D transported to full added G3-priced count | +0.358805 | 0.307362 | Original control; not adopted |
| Original D transported to residual added G3-priced count | +0.289404 | 0.247589 | Control; use corrected jointly solved D instead |
| Union-head credit exposure for primary identity-loss children | +0.697894 | 0.109542 | Exposure diagnostic; not a demonstrated duplicate |

[CALCULATION: `derived/membership.json`, all component 3×161 vectors in `membership_replicates.csv`]

The review's 0.359M dependents is not reproduced under the stated biological rule: the broad mask contains 278,493 linked dependents claimed by nonmembers; the primary latent mask contains 205,069. These counts use DEP_STAT's actual tax claimant and the child's own biological links. The $0.593/$0.107 reverse estimates are also not exact outputs under this rule: the simple diagnostic has B $0.569016bn and Cr $0.006406bn. Proportional credit allocation does not solve nonlinear child-count and filing-status effects; the parent's jointly solved M6 uses expanded-minus-original tax/credit returns and supersedes these diagnostics. Do not add them again. [CALCULATION; INFERENCE]

The frozen personal account puts qualifying-child credits on the actual claimant's record. Located latent children themselves carry zero observed CTC/ACTC/EITC credit records (gated). The added-age-mix personal refundable key has zero support at ages 0–14; its ages 15–19 key is the actual filing/claimant record's age, not the qualifying child's age. Therefore a union parent's credit and an added child's full own-person cost are not the same carrier. This does not validate all aggregate age transport; it falsifies treating the entire head-record exposure as an observed duplicate. The added item5b projection is genuinely overlapping once the same latent roster's crossing credits are recomputed, so that specific projection is subtracted. [DATA: `added_age_mix_2026_10_07/derived/g3_age_keys.json`; CALCULATION: `located_latent_children_own_credit_records_zero`]

`transport_added(case, corrected_D, remaining_added_g3)` transports only the corrected union G3+ joint-return D vector to the residual unlocated G3-priced pool. Both original-D diagnostics retain all 160 replicate covariances; corrected D remains an assumed per-member transport. White-priced added people carry zero crossing credits and D under the existing case rule. The review's ≤$0.25bn white-credit range is an illustrative sensitivity, not an empirically verified bound on white D. Reject presenting zero or that ceiling as measured. [ASSUMPTION]

All current-year credit corrections apply equally to the set and cash at the personal low/high specifications; receipt scenario scaling must follow the parent's exact frozen item5b subtraction. No M6 own pension/health/tax cost is added again to the already priced latent population. The unified removal result is produced by `round2.py` using these exact masks, projection subtraction, nonlinear federal/state solve, and residual D transport. [CALCULATION]

## Validation and paths

Six tests cover biological versus step/adoptive links, second-parent lineage, conflicting parent nativity, all-column G3 transport, pension dual entitlement, and immutable-input drift rejection. Standalone builds pass all 12 membership and three pension gates; pension cached baseline relative error is zero. Rebuild is **IDENTICAL: 4/4** for owned derived files, exit 0; timed source build is 12.972s, peak RSS 1,540,292,608 bytes, measured with Python `perf_counter`/`getrusage`. `inputs/membership_pension_pins.json` hashes 11 reused source/grid/person-cache/case/age-key files; the register is written only if absent and every subsequent compute verifies it before work. A stale input blocks instead of refreshing its hash; the regression test verifies register bytes remain unchanged after drift. All source-lane inputs are read only; no Git metadata was changed. [CALCULATION]

Changed paths owned by this worker: `membership.py`, `pensions.py`, `test_membership.py`, `test_pensions.py`, `membership-result.md`, `pensions-result.md`, `derived/membership.json`, `derived/membership_replicates.csv`, `derived/pensions.json`, `derived/pensions_replicates.csv`, `inputs/membership_pension_pins.json`. Scratch driver `/private/tmp/run_membership_probe.py` and its log are untracked verification artifacts outside the lane.
