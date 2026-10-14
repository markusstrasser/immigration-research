**Verdict:** The implemented arithmetic is coherent as a conditional construction sensitivity. One material provenance defect remains: the pricing cache does not identify the complete inputs and code that produced its person profiles. No confirmed current numerical error was found.

Review was read-only except this artifact. Applied the bounded scout/validation route of the code-review skill; no further model dispatch, upstream writes, or Git metadata writes. Independently ran the two scoped test files with bytecode and pytest cache writes disabled: **48 passed**, exit 0, 1.78 seconds.

## Confirmed finding

**MEDIUM — incomplete pricing dependency identity permits silent stale profiles.** `export_pricing.py:32-41` checks only entries carrying `repo_path` in `inputs/pins.json`. That list omits the executed `generation_account_2026_09_24/keys.py`, among other transitive dependencies. The adapter imports `households.py`, which imports that module at `households.py:163` and calls its owner, medical and school key constructors at `households.py:488-490`. Those constructors consume additional unpinned inputs, e.g. `keys.py:52`, `keys.py:64-66`, and `keys.py:89`. `coverage_bound.py:203-209` subsequently compares only the two adapter hashes and cache bytes. The export audit at `export_pricing.py:209-218` does not bind a digest of the input manifest to the cache either.

Concrete counterexample: change `keys.py`'s within-generation medical age profile while preserving its weighted generation totals, or refresh a pinned source and its expected hash without rebuilding the cache. The first change leaves every listed pin and both adapter hashes unchanged; the second passes the new pins but has no cache-versus-manifest comparison. The cached run therefore accepts old person prices. A fresh export can yield different age-priced coverage despite exactly identical generation and case totals: with equal weights, prices `[1,3]` versus `[2,2]` both total 4, but coverage factors `[0,.1]` imply .3 versus .2. The existing total closure checks cannot identify this failure class.

Fix: record the complete pricing dependency manifest (executed local modules and source data, or a canonical upstream manifest with equivalent coverage) and its digest in `pricing_audit.json`; require the same manifest digest when loading `pricing.npz`. Include a regression that changes an upstream profile dependency while retaining aggregate totals and verifies that cache loading stops. Do not merely add `keys.py`: its raw inputs and downstream helpers form the same affected class.

Confidence: **high** that dependency and manifest/cache binding are absent; **medium** about practical impact because no such upstream drift was observed in this review. A demonstrated complete upstream fingerprint checked by this exact cache-read path would remove the finding. Project-specific reconciliation: a deliberately immutable, self-contained frozen pricing artifact could instead make live dependency checks unnecessary, but then its complete build provenance must be stored and it must not claim freshness against the live upstream implementation.

## Coverage and limits

Covered all requested files: `coverage_bound.py`, `export_pricing.py`, `source_tables.py`, `acquire.py`, `national_keys.py`, `inputs/controls/compare_base.py`, `test_coverage.py`, and `test_national_keys.py`. Also inspected `inputs/pins.json` and the relevant construction, splitting, and key-building portions of upstream `households.py` and `keys.py`.

Checked the March 15 to April 1 birth mixture, negative historical ages, arrival-code eligibility, signed correction algebra, DA residual versus base ratios, replicate formula, uncertainty labels, added-person calibration, actual-driver reconstruction, tenant national-mass override, and denominator numerator/dilution accounting. No additional material implementation defect was confirmed. The denominator arm is a conditional driver-mass calculation, not a recomputed engine counterfactual; the output states that limitation. PES shifts move cells together and are labelled construction sensitivity, not a confidence interval.

Skipped external source authentication, independent scientific validation of Hispanic-to-Mexican transfer assumptions, and complete raw upstream dependency execution: this was a bounded implementation review with pinned local tables. Did not rerun output-producing builders or modify the source data. Final RESULT prose was still being completed by the parent and was outside this review.

## Remediation verified by the parent, 2026-10-14

Confirmed the upstream `keys.py` call and repaired the affected class with `dependency_manifest.py`.
The explicit initial capture records actual read paths and imported research modules; normal exports hash-check
the complete manifest before executing the pricing construction and block any new unpinned read. Numerical
runtime versions and the environment lock are included. `pricing_audit.json` binds the input manifest, adapter,
national-key helper and price-cache digests; the consumer checks that binding before loading the prices.
Regression checks stop on a same-size upstream source edit, an unpinned transitive read, a duplicate manifest,
and a changed input manifest or price cache even with unchanged account totals. No gate was loosened.
The finding is resolved subject to those reproducible checks; the original review above is retained.
