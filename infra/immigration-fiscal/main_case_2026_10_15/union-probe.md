**Verdict:** Final native-child item10 passes twelve source endpoint/arm gates (maximum gap4.11e-13bn), eight option checks, native service-response regressions and twelve exact source-scope commutation checks. Credit-export memory/parity controls pass; household record routing and production are explicit. The initial implementation below is historical; later corrections replace child endpoint carriers with native cells/production and repair source scope.

## Historical initial implementation (superseded where corrected below)

Item 10 is implemented in `item_union.cjs`; all 12 source endpoint/arm gates pass within 1.3e-13bn, its parts add exactly, and eight lineage-option/set rebuilds produce finite edits. The observed CPS record map is exported for downstream household routing. This verifies the frozen source endpoints; companion interpolation and the source's pooling assumptions remain explicit approximations.

## Implemented API

`build(ctx, arm, which)` returns `{edits, editsAt(m, options), parts, spending_lines, receipt_lines, responses, meta, record, detail}`. `ctx.B` is the full v7 package or its lineage option, `ctx.DETAIL` its `ITEM_DETAIL`; `which` is `set` or `cash`. Arms: null central, `broad_report`, `all_age_extrapolation`.

The source's own-record price exports are signed, response-inclusive costs. The bridge divides out each source response and puts the raw signed amount on a transparent spending carrier with national total zero and compensating other amount. Real parent lines' national amounts do not move. There is one `k` carrier per source parent key because `Engine.applyCorrections` intentionally creates only `k` on synthetic spending lines. `meta.union_completion.carriers[id]` identifies `side`, `parent_line`, `parent_key`. The package must activate a carrier only when its parent selects that key (receipts: current receipt scenario) and copy the parent's actual evaluated response. Otherwise its response is zero. Capital, production and nonreporter carriers have explicit low/high reading responses in `responses`.

Reporter option repricing changes the original pooled G3 amount on the same observed record-key ratio. It removes item 5b from the G3 coefficient denominator and from changed option cells before transporting those differences, preventing a second extrapolation of the crossing-credit residual. Job-industry taxes retain the source's independently calculated own-record quantities when the original lineage count changes; an earlier domestic-source corporate re-key scales their corresponding raw amounts through `editsAt(m)`.

The nonreporters use the source's full engine unit-band route, loaded through a fail-loud read-only adapter of `added_band_prices.cjs`, supplied each option's package. Their observed ages stay fixed; the current option C3 blends grandparent-linked losses. The source's frozen original-lineage positive control is kept in returned source metadata and is not applied as an oracle to changed lineage options. Identical central payload edits reuse the source's verified original rates; option results are cached across equivalent fresh case packages.

Exact 5b interaction edits are applied to the actual FIT/refundable-credit lines, with the source's scenario expansion rule. The source canonical G3 per-person credit projection is removed before adding the exact joint delta. The original 3.04M modeled addition's term is left in v7. All source paired 161-element replicate vectors and SEs remain in `meta.union_completion`.

`export_union_credit_parts.py` captures the original source's account/owner vectors by generation and side before the source drops its per-arm state. It preserves the source's entire computation and original pin gates; only an AST-inserted retention field is added. Central credit changes are G1 0, G2 +0.1804476218858002bn, G3plus +0.14503669954369514bn. The receipt and spending edits are split on those exact side-specific generation amounts, never by assigning the whole +0.325bn to G3plus. Generation parts add to each cell edit exactly after the source's receipt-scenario scaling. [CALCULATION: `derived/union_credit_parts.json`]

## Source identities and counts

`export_union_people.py` imports the unchanged source `completion.masks` / `siblings`, uses the same canonical CPS frame and parent linker, and writes `derived/union_people.json`. Keys are `(PH_SEQ, PPPOS)`, not positional joins. There are 310 records: 283 broad reporters and 27 observed nonreporters; the central filters to 204 reporters plus those 27 children. Every new person routes to generation G3plus; economic classes on nonreporters are separately `g3_rate` or `later`.

- Central reporters: 456,935.87772777 people; observed nonreporters: 60,499.87946540001; total addition: 517,435.75719317. [DATA: `derived/union_people.json`, source `count_replicates.json`]
- Central reporting union: 40,169,429.20892777; lineage: 43,269,648.68157841. [CALCULATION: `item_union.cjs`, on v7 counts]
- Grandparent-linked nonreporters: 38,589.21881760; later losses: 21,910.66064780. [DATA: source `count_replicates.json`]
- Item 5b joint interaction: +0.3254843214294949bn, SE 0.1297461439433784bn. [DATA: source `credits_interaction.json`; exact stored SE is carried in the payload]

Selected `observed_records`, age counts and `record_key` are included in `meta.union_completion`. The all-age arm includes only observed reporter IDs plus its explicitly unlocated extrapolation count; it never adds the observed children again.

## Verification

`node item_union.cjs` writes `derived/union_probe_checks.json`:

| Set | Central low / high | Broad low / high | All-age low / high |
|---|---:|---:|---:|
| Set | 2.89321085491865 / 3.75461632909018 | 5.55958615496089 / 6.74987658420025 | 3.93929297961836 / 5.28497345248141 |
| Cash | 2.03126269532014 / 2.89266816949168 | 4.43398719260977 / 5.62427762184915 | 2.71143545731870 / 4.05711593018175 |

[CALCULATION: `derived/union_probe_checks.json`; costs in bn; exact source vector gate tolerance 1e-6bn]

All 12 endpoint gates pass, all edit parts add exactly, and arm_a / arm_c / c3_minus_se / c3_plus_se rebuild in both sets with finite quantities. The option C3 values are 0.5567 / 0.5567 / 0.3110 / 0.8024; child costs change accordingly. Audit-row-3 models pass `editsAt` with explicit options and with tags inferred from the model; specs are built with `api.specsFor`, preserving the existing candidate tag guards.

Exporter: exit 0, 2.01s, physical peak 1,284,982,560 bytes through the repo memory-budget check. Module check: exit 0, 14.36s, Node maxRSS 306,192 KiB. These timings are execution evidence and are excluded from deterministic derived outputs.

After the generation-parts and variant fixes, the full module check again passed all 12 source and eight option gates (26.98s, maxRSS 265,584 KiB while peer processes ran). The credit-parts exporter passed its by-generation/by-side/net closure gates for five arms in 28.30s, physical peak 2,480,966,560 bytes, within the 2.5GB limit. Explicit `capital:false` sets the reporter capital carriers to zero; an unexpected missing component fails rather than becoming a silent zero.

Reproduction, in order:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_2026_10_15/export_union_people.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_2026_10_15/export_union_credit_parts.py
node infra/immigration-fiscal/main_case_2026_10_15/item_union.cjs
```

## Approximations / For the parent

- Only the source endpoint keys have observed reporter price anchors. Other source keys transport its preferred-key own/canonical ratio; they are listed per carrier as `extrapolated_key`.
- Reporter lineage-option prices hold own-record key numerators and identified-G3 denominators fixed, changing the pooled source amount. These option prices are model calculations; the source lane provides no independent option oracle.
- Capital, production and child carriers interpolate by endpoint reading. They are rebuilt for each lineage option, but a changed school/first-year/shared companion does not independently rebuild those frozen endpoint pieces. The package's real-line reporter carriers do follow the companion's actual parent response. This limitation must remain visible in companion notes; do not describe all item-10 pieces as independently measured under those alternate responses.
- Shared reporter carriers transport the personal raw record amount; the source explicitly did not measure a new hypothetical shared boundary.
- The preserved 5b delta and SE are source-v7, fixed-lineage estimates; the source's original 3.04M crossing-credit projection stays fixed for that delta.

## Files covered and skipped

Covered source files: union completion `RESULT.md`, `completion.py`, `candidate.py`, `credits_interaction.py`, `person_adapter.py`, `job_record_key.py`, `added_band_prices.cjs`, `snapshot.cjs`; their derived candidate, pricing lines, counts/replicates, credits and unit-band prices; source set/cash snapshots; the household kernel's piece/key/response construction; v7 package and child-credit/job-capital item contracts; engine synthetic-line construction. No upstream writer was run or modified.

Skipped: complete v8 case/contract/generality/API/rerun gates (owned by the parent), item-11 mixed-unit intersection (another assigned probe), adopted prose/decision/consumer propagation (outside ownership). No git metadata was written.

Changed paths: `item_union.cjs`, `export_union_people.py`, `export_union_credit_parts.py`, `derived/union_people.json`, `derived/union_credit_parts.json`, `derived/union_probe_checks.json`, `union-probe.md`, all under `infra/immigration-fiscal/main_case_2026_10_15/`.

## Native-child correction, 2026-10-15

The earlier child-carrier limitation above is superseded. `child_records.cjs` uses the source's transformed own-age G3/white units as native original-line edits and additive P/F production; there are no child endpoint carriers. Actual service, school, public-capital and production specifications therefore apply to observed children, including first-year and frozen-service companions. Reporter capital/production retain the stated source-endpoint transport assumption. The native source reconstruction gates all twelve set/cash/arm endpoints; sign-reversal tests native child removal away from the endpoints. The focused code review and correction are recorded in `code-check.md`.

## Credit-exporter memory correction, 2026-10-15

**Verdict:** The exporter now releases each completed AST-executed arm immediately. Two complete reruns retained every source/canonical control, reproduced the existing artifact byte for byte, and stayed below 1.082GB physical footprint. Only `export_union_credit_parts.py` changed computationally; the pinned source lane is unchanged. This corrects the earlier near-limit execution receipt: the later full G5 attempt failed at 2.577GB, as preserved in `_cache/g5_base_memory_failure.log`.

The source constructs each arm with `s = dict(state)` and executes its account functions with `s` as their globals. Those functions and the dictionary form cycles retaining full per-arm arrays after the loop advances. The exporter capture adapter now injects `del s; gc.collect()` immediately after `results[label] = r`, after all account/owner terms have been retained. The source's subsequent print uses `r`, not `s`; its canonical controls, all five expansion arms, 161-column replicate calculations, source pins and closure tolerances run unchanged. The AST anchor still fails loudly unless exactly one result-assignment boundary is found.

The decimal-2.5GB physical budget guard now runs before any output-directory creation or artifact write. `--check-existing` additionally requires the newly serialized bytes to equal the existing artifact before writing. Both budget rejection and byte-parity rejection were independently injected into the actual compiled write-tail statements against a temporary sentinel artifact; both raised `[BLOCKED]` and left the prior bytes unchanged. Compile checking and an AST check of the guard's ordering also passed.

Executed twice, sequentially:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_2026_10_15/export_union_credit_parts.py --check-existing
```

| Run | Exit | Time, perf_counter | Peak physical bytes | Margin below 2.5GB | Byte parity |
|---|---:|---:|---:|---:|---|
| 1 | 0 | 69.365576s | 1,033,668,456 | 1,466,331,544 | IDENTICAL |
| 2 | 0 | 92.870130s | 1,081,624,496 | 1,418,375,504 | IDENTICAL |

Both runs produced SHA256 `b085afc90d969be813347e2704c83f5bcba7fa679bdca6238b21c0e3620b95f2`, the baseline `derived/union_credit_parts.json` hash. Timing and footprint are execution receipts and are not added to the derived bytes. [CALCULATION: the commands above; physical footprint from the repo's `memory_budget.require_within_budget`]

Files covered: this exporter, the source `credits_interaction.py` loop and its post-assignment uses, the failed G5 log, the existing derived artifact and this probe note. Skipped: full case/G5 and unrelated lane edits, as assigned. Content changed: `export_union_credit_parts.py`, `union-probe.md`; `derived/union_credit_parts.json` was regenerated with identical bytes. No git metadata was written.

## Domestic-source order correction, 2026-10-15

**Verdict:** Applying item 9 to v7's original job-tax rule now gives exactly the same bands as starting with the legacy `job_capital_taxes=foreign_source_removed` arm, with item 9 either present or absent. All twelve comparisons have zero numerical gap: central, arm a and C3+SE, each set/cash and item-9 on/off. The central candidate's bands are unchanged. [CALCULATION: `_cache/foreign_commute.log`, `COVERAGE=0`]

The reporter numerator was frozen at the source's all-source job tax, but its denominator had been reset to `currentModel` even when that model was already domestic-source. Item 9 then correctly made zero further edits while the reporter retained the all-source numerator. The resulting old-arm candidate had been lower by $0.029021833461bn / $0.01073807838bn. That discrepancy is corrected by changing the source-scope anchor, without changing the observed reporter records or source quantities.

`item_union.cjs` now loads the authoritative v7 `item_job_capital.cjs` private `newParts` function through a read-only runtime adapter. It reconstructs the all-source target using the current lineage option's own source wage shares and national line totals. Each reporter job-tax amount is therefore fixed under a change to the original descendants' count, while an actual domestic-source re-key is measured once against the same option-relative all-source anchor. This reuses v7's construction rather than copying its formula or anchoring every option to the global central model. Original receipt nationals remain unchanged.

The same source-scope rule now applies to the children's raw-unit library and its cache: domestic units are selected when either the legacy job-tax arm is domestic or item 9 requests domestic source. This also fixes the adjacent legacy-domestic/item-9-off route; it is covered by the same exact comparisons.

| Coverage-off central band, bn | Original job rule + item 9 | Legacy domestic arm, item 9 on | Legacy domestic arm, item 9 off |
|---|---:|---:|---:|
| Set | 356.9891157917939 / 443.3429994363893 | identical | identical |
| Cash | 281.00072341817486 / 367.3546070627696 | identical | identical |

[CALCULATION: `_cache/foreign_commute.log`; arm-a and C3+SE rows also have exact-zero gaps in that log]

The final `node infra/immigration-fiscal/main_case_2026_10_15/item_union.cjs` run exited 0: all twelve standalone source endpoint gates, eight lineage-option checks and native-child service-zero regressions passed (14.186572s; Node maxRSS 349,168 KiB). The expanded commutation check peaked at 588,880 KiB. Standalone item 10 still matches its frozen source to the existing 1e-6bn tolerance. [CALCULATION: `derived/union_probe_checks.json`; console execution receipts]

The payload's `union_completion.source_hashes` now includes the explicit runtime formula `main_case_2026_10_14/item_job_capital.cjs`, the unit-model algorithm `union_completion_2026_10_14/added_band_prices.cjs`, and `union_completion_2026_10_14/derived/count_replicates.json`, alongside the already listed source outputs. The parent must regenerate the payload provenance bytes; this metadata addition changes no scalar result.

Files covered: `item_union.cjs`, the v7 job-tax builder's `newParts` and lineage wage shares, item 9's arm-aware edits, the appended probe record and the requested comparisons. Skipped: full main-case/G5 and every other lane, which remain parent-owned. Content changed: `item_union.cjs`, `union-probe.md`; ignored diagnostic `_cache/foreign_commute.log` was written, and `derived/union_probe_checks.json` was regenerated by the required module checks. No git metadata was written.
