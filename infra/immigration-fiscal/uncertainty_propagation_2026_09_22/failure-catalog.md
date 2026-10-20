# Executed consumer failures

- 2026-10-20, adoption preflight: the prepared oct16 exporter required
  `meta.adopted=2026-10-16`, rejecting the adopted October 20 payload. The
  preflight now checks the actual adoption stamp, adopted status and explicit
  non-STUB flag before loading the expensive case/generation modules.
  `test_adopted_payload_preflight_is_cheap_and_rejects_stale_stamps` covers the
  adopted stamp plus stale, candidate, missing-stamp and STUB failures, each
  with a five-second timeout. No source hash is manually edited.

- 2026-10-20, item15 fixed-key vector: the first full build stopped because
  multiplication by the calibrated CPS civilian-total vector introduced
  2.80e-11bn of summation noise into the 199.570140402539bn education line.
  In the live retained core, fixed education keys now use the central calibrated
  population scalar explicitly. The helper first rejects any population-share
  drift above relative1e-12; the monetary1e-9 gates and exact-zero item15 vector
  checks are unchanged. The regression checks exact fixed vectors and rejects
  a material population change. Historical output files are preserved.

- 2026-10-20, cash oracle scope: the prepared retained-core exporter indexed
  a32-row personal cash source oracle with all64 personal/shared control rows,
  crashing at row32. It now requires exact ordered coverage of all32 personal
  specifications and compares those exported uncertainty rows at the unchanged
  1e-9 cost/capital tolerance. Set still checks all64 against both saved methods.
  Shared cash uncertainty is outside the published personal-account estimator;
  no shared cash oracle is invented. The live vector/owner regression checks
  every published cash row against its principal source record.

  Follow-up: cash's numeric evaluator does not carry the enclosing package's
  profile, row4 details or stack metadata. The consumer composes shared package
  context with cash's own numeric API and uses cash row4 inputs. Allocation comes
  from `meta.allocation.group_total`, not the response profile. The source gate
  requires exactly64 finite cost/capital comparisons across32 personal rows;
  missing source rows, empty personal support and null monetary values reject.
  These cases have cheap executable regressions in `test_oct16.py`.

- 2026-10-20, item21 source boundary: the final producer has two coverage
  builds, `cov` at source rates and `cov_v9` at the selected common rate. The
  prepared adapter expected one call and failed closed. Its AST boundary now
  verifies exactly those two ordered assignments and returns before the first;
  source-dollar and write-denial guards remain. The regression executes a prefix
  without defining either coverage or its writer, and rejects a changed second
  assignment.

- 2026-10-20, sampler source stability: tightening cash-oracle validation while
  the set sampler was running changed its pinned adapter dependency. The sampler
  reached its final source-stability check and rejected publication. This was an
  executor scheduling error. Numeric-run dependencies are frozen during retries;
  no stale hash is edited or mutation exception introduced. The existing live
  source-hash regression and end-of-run stability guard remain mandatory.

- Performance evidence, 2026-10-20: exporter CPU profile94.31s attributes
  28.13s self time to protected v8 cloning,17.10s to engine cloning,7.29s to
  hashing. Cash core profile91.20s attributes45.47s cumulatively to the protected
  job-capital reconstruction (24.38s group wage cells),14.14s to raw CPS loading
  and12.30s to the own account adapter. The earlier set phase125.94s crossed
  two minutes under concurrent load; source optimization is outside this lane's
  ownership and was reported to the parent. Physical-memory guards are retained.

- 2026-10-20 review: the 12 MB all-specification source intermediate now lives
  in ignored `_cache/oct16/spec_sources.json`; its tracked manifest pins path,
  bytes and sha256. Python and JS consumers reject missing or changed cache
  content. Regression covers missing/same-size-mutated payloads. Case-declared
  set/cash endpoints replace fixed indices; different method ends and duplicate
  or absent source anchors fail closed. AST extraction preserves top-level
  conditional declarations and removes only the `__main__` entry point.

- 2026-10-20, relative profiling entry point: `cProfile` preserves a relative
  `__file__`, so a dependency's `relative_to(ROOT)` failed before the sampler
  ran. The new sampler and pooled-ratio producer now resolve their own source
  paths before recording hashes. Both relative profiled set/cash negative
  probes must reach the intended `require_own` rejection within ten seconds;
  stale-source and source-stability guards are unchanged. Coverage receipts
  are rebuilt because their pinned sampler source changed.
  Paths: `oct16_sampling.py`, `pooled21.py`, `test_oct16.py`.

- 2026-10-20, coincident effective-rate specifications: assembly joined retained
  scalar rows by four coordinates, matching both raw-rate specifications after
  item20 made their effective rates equal. `propagate.py` now exports the stable
  specification ID on live retained-core rows. `oct16_sampling.py` requires all32
  unique IDs and cross-checks normalization, school share/response, government
  response, medical and justice coordinates before its existing1e-9 monetary
  gate. `test_oct16.py` preserves coincident numeric specifications and rejects
  duplicate IDs and coordinate drift. No specification is dropped. Health21's
  dependency list also pins the actual `propagate.py` donor-covariance helper.

- Performance continuation, 2026-10-20: both successful profiled sampler runs
  completed in81.327/80.296s (set/cash), physical1.650/1.640GB. Set profile80.904s:
  item21 gradients36.740s,101 protected source evaluations28.605s cumulatively,
  hashing15.759s, subprocesses14.590s. The failed137.745s set run had a dependency
  mutation under concurrent work; the stable successful runs are below two
  minutes. Profiles remain in the worker's prop9 scratch directory. The earlier
  protected exporter/job-capital hotspots are retained above as deferred work.

- 2026-10-20, item21 source boundary: the final producer has two coverage
  builds, `cov` at source rates and `cov_v9` at the selected common rate. The
  prepared adapter expected one call and failed closed. Its AST boundary now
  verifies exactly those two ordered assignments and returns before the first;
  all source-dollar and write-denial guards remain. The regression executes a
  prefix without defining either coverage or its writer, and rejects a changed
  second assignment.

- Performance evidence, 2026-10-20: exporter CPU profile94.31s attributes
  28.13s self time to protected v8 cloning,17.10s to engine cloning,7.29s to
  hashing. Cash core profile91.20s attributes45.47s cumulatively to the protected
  job-capital reconstruction (24.38s group wage cells),14.14s to raw CPS loading
  and12.30s to the own account adapter. The earlier set phase125.94s crossed
  two minutes under concurrent load; source optimization is outside this lane's
  ownership and was reported to the parent. Physical-memory guards are retained.
