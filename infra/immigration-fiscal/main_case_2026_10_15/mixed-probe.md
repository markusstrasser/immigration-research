**Verdict:** Item11 is integrated as the brief's end-keyed post-engine delta, and the joined dollar footprint has been executed. The conservative original-source footprint including all unlocated D is3.849023320131/3.643434434298bn; it is not a formal bound on the nonlinear joint-counterfactual change. See the executed intersection section and current `derived/mixed_overlap.json`.

## Historical initial verdict (superseded for execution status)

Item 11 can be integrated exactly as an end-keyed post-engine delta on v7; preserve v7's child-credit edits and add the source's bounded row once. The engine's existing correction schema cannot express end-keyed fixed shifts on the affected existing lines. The item-10 records are joinable; measuring the dollar overlap requires exposing source per-unit flows, which are not present in the saved aggregate outputs.

## Replacement and exact input rows

`mixed_unit_removal_2026_10_14/round2.py:93–96,128–161,183–190` constructs the bounded rows as deltas relative to v7. `removal.py:338–346` already subtracts the union's item-5b receipt and spending vectors inside M1/M3; `round2.py:54–58` replaces the located latent children's crossing-credit projection with their joint nonlinear return effect; `round2.py:71–73` adds corrected D only on residual unlocated G3-priced descendants. The original D controls are not added. Consequently, using a bounded row on unchanged v7 is correct; disabling v7 `child_credits` and then adding that delta subtracts item 5b twice. `tax_replacement_item5b_and_D` is explicitly a replacement amount and is not the item-11 delta.

Authoritative central rows in `mixed_unit_removal_2026_10_14/derived/round2_summary.json`, filtered by `method`, `end`, `component`:

| v8 reading | Source component | Delta bn | SE bn | G1 bn | G2 bn | G3+ bn |
|---|---|---:|---:|---:|---:|---:|
| low | bounded_low | 10.740016272701766 | 4.4167858647167995 | -2.0311962220637065 | 1.2233035172461966 | 11.547908977519276 |
| high | bounded_high | 14.531690197973518 | 4.405052930817506 | -1.3109090555178016 | 2.3835397451969715 | 13.459059508294349 |

Set and cash use the same current-flow deltas. Low source arm is `Medicaid_low|ACA_low|SNAP_zero_observed_high_takeup`; high source arm is `Medicaid_high|ACA_high|SNAP_cap_observed_low_takeup`. Each component is available at both frozen v7 ends, with these totals identical across those ends. The pension companion uses `bounded_high_plus_pension_model` = 28.47779184344573bn (SE 4.514915890134994), set only, not the central delta; its increment beyond bounded_high is 13.946101645472211bn.

The bounded formula is M1 + M2 + M3 + M5 consumption + M5 owner-property (at the end's owner response) + M5 SNAP key + M5 housing + M6 + D residual + selected latent SNAP + selected latent Medicaid + selected latent ACA - M5 SNAP key. The SNAP reallocation cancels exactly. Do not add `bounded_*_membership_benefit_interaction` again: it is already inside the selected latent health/SNAP terms. Do not add the weight artifact (+1.443594bn), original D, diagnostic reverse-credit terms or all-biological child arm.

## Engine route and metadata

`main_case_2026_10_14/package.cjs:135–143` validates exact fixed-shift shapes `{side,line,scenario/key,by:{personal,shared}}`, or a national amount; there is no reading/end field. Its response API (`149–153`) permits new receipt responses only when the receipt has no pre-existing override and the metadata key is new. Item 11 touches existing federal income tax, refundable credits, state income tax, consumption receipts, owner property, SNAP, housing, Medicaid and ACA/PTC; parts vary by policy envelope and are not a scalar response on a single existing line. Fabricating a receipt line for the delta would misrepresent these components. Use the brief's authorized post-engine fallback and state it under For the parent.

Implement an item registry entry with zero engine edits, `kind`/record explicitly identifying post-engine application, and per-set/per-reading metadata containing the total, generation parts, generation SEs, source component/arm and source hashes. Add the delta in every `evaluateFull` / `viaCandidate` route and derived cost/band API; raw `Engine.evaluate` consumers must apply `meta.mixed_unit_removal` just as they apply capital return/coverage. Preserve item 11 off as exactly v7's 5b plus no D extension. Avoid a payload that changes the engine cost invisibly without declaring the post-engine amount.

Saved replicate schema is `round2_replicates.csv`: columns `method,end,component,generation,r0,…,r160`, generation labels `G1`,`G2`,`G3+`. Route the matching bounded component's three generation rows and preserve all signed columns. Total SE = sqrt((4/160) × sum over r1…r160 of (sum_g r_g - sum_g r0_g)^2); never sum generation SEs or use quadrature. Store the total stack plus each generation stack in item metadata or a referenced derived file. Executed read-only checks reproduced both source SEs to <3e-15bn; generation totals close exactly and CSV central sums differ by <5e-14bn.

## D scaling for companions

`membership.py:112–122` defines D transport = corrected union G3 vector × residual added-G3 count / identified G3 count, with white-priced people at zero. `membership.py:150–164` gives central added G3 = 1,956,998.369115257 people; located roster G3 = 378,527.12458407826 people, leaving 1,578,471.2445311788 residual G3 people. Central D residual is +0.5454107092728235bn (SE 0.25923672744404685), all in G3+.

The brief says only D changes under lineage options, scaling with each option's added G3-priced count. Literal implementation: `bounded(option) = bounded(central) + D(central) * (option_added_g3 / central_added_g3 - 1)`, applied to every r column, all generation change in G3+. This follows the brief's requested transport; document it explicitly. A stricter reconstruction of the source's residual rule would instead scale by `(option_added_g3 - option_roster_g3)/(central_added_g3 - central_roster_g3)`, rebuilding roster_g3 at the option's C3. These differ when the count or C3 moves. For the parent: recommend the literal brief rule behind a named switch, with the residual-rule alternative exposed and its difference printed. Neither rule rescales the other fixed survivor components.

## Union-completion intersection: keys and implementable bound

The person keys are available and joinable, so claiming they cannot join is unwarranted. `removal.py:96–111` joins on `(PH_SEQ, PPPOS)` with `validate='one_to_one'`; `credits.py:219–227` loads the same pinned CPS archive, joins the 161 weights on those keys and sorts them. `removal.py:468–470` independently gates a bijection to the consumption frame's `(ph_seq, pppos)` keys.

Reconstruct the exact completion masks with `union_completion_2026_10_14/completion.py:masks` (95–102): central reporters = civilian, native, Mexican reporter, outside old union, exactly one US-area-born parent. Its `siblings` (105–126), biological arm, non-Mexican reporters complement gives the observed nonreporting children. `initial_counts:194–202` supplies their grandparent/later-loss classification. These differ from mixed lane latent children, which require both child parent-birthplace fields to be US areas (`membership.py:65–79`).

For a conservative overlap footprint, find every original household `PH_SEQ`, SPM unit `SPM_ID`, and linked tax return/family containing any item-10 person; count membership and join closure separately. Keep original calibration/donor populations, union mask and national denominators fixed, and sum only component flows in those affected units. Do not subset the frame or change calibration: that would estimate another quantity. For taxes include all before/after returns and transferred dependents linked into affected households; the `survivor_registry` ownership and `original_item_parts(x, scope=…)` allow consistent removal of the corresponding 5b footprint. Household-level containment is conservative when transfers bridge tax units.

Source hooks for exact dollar footprint:

- federal/refunds: `removal.py:federal_removal`, before aggregation lines 341–346; mask before and after return flows by their household, subtract scoped original 5b once. Include the analogous expanded-context difference used by M6 and its scoped old projection;
- state: `state_tax.py:compute` after per-return tax difference and before generation aggregation, matching original/after household scope;
- consumption: `removal.py:consumption_removal` lines 500–521, scope person movement to intersecting SPMs while retaining full `raw` denominator; its returned `lines` already separates receipt lines but only after global aggregation;
- owner/housing: `resource_keys.py:compute` lines 75–91, scope `move` by intersecting `PH_SEQ`/`SPM_ID`, retain full `group`; SNAP key and its baseline interaction cancel;
- SNAP: intercept `benefits.py:attribute(change,unit,…,mixed)` (267–285) to retain/sum the relevant SPM events; `snap_arm.py:compute` (139–141) supplies complete arms and already-fixed full-frame takeup/conversion;
- health: intercept `health.py:attribute(person_change,d,W,union,gen)` (406–422) and sum events in the intersecting SPMs, retaining all original donor rates. The latent membership mask is already passed to health without changing generation ownership.

Report both signed overlap and sum of absolute component/unit contributions at the selected low/high readings, with the latter as the conservative footprint bound and its share of item 11. The residual unlocated D has no observed unit key: disclose that its joint overlap is unlocated rather than allocating it by record count. A zero observed overlap does not identify a zero causal interaction. The saved arrays and CSVs contain generation aggregates only, so they cannot produce this dollar footprint by themselves. No dollar intersection was executed in this read-only probe; source adaptation under the v8 lane is necessary.

## Covered / skipped

Covered: brief in full; mixed round2 integration and authoritative results/replicates; mixed membership/projection/D functions; federal and consumption aggregation; own-resource key aggregation; SNAP/health attribution APIs; union-completion membership masks/keys; v7 item edit/response validation and evaluation hooks. Read-only arithmetic checks of exact chosen totals, generation closure and replicate SEs passed. Memory registry search for these new lane names had no hits.

Skipped: scientific re-adjudication of adopted source assumptions (settled by brief); full source reruns (would write old lanes and exceed this read-only assignment); implementing the main package, overlap computation or new derived files (parent owns them); git writes/commits (prohibited).

## Executed intersection, 2026-10-15

The original read-only probe above is superseded for dollar coverage. The lane-local `mixed_overlap.py` instruments the unchanged kernels without writing their lanes. Its full-frame component checks match the authoritative bounded totals before accepting the household-superset intersection. `derived/mixed_overlap.json` reports signed -1.206979343944 / -0.872377009391bn, absolute component-by-household 3.303612610858 / 3.098023725025bn, and conservative bounds including all unlocated D of 3.849023320131 / 3.643434434298bn. These are exposure bounds, not the joint membership counterfactual; the brief's expected sub-$1bn footprint is contradicted.
