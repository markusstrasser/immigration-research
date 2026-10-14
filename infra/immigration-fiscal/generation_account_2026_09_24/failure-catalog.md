# Generation propagation failures

- 2026-10-15: the reporter covariance pass cloned the full model once per carrier,
  generation and endpoint; set/cash runs took 151.408/149.650s. CPU profiles of
  30 unit perturbations identify model cloning as the main cost. The replacement
  uses Engine.evaluate's exact spending derivative, fiscal_weight × response,
  with declared-carrier/capital-independence guards, representative single-unit
  controls, two joint replicate perturbations and fixed-source conservation.
  All 161 results are compared against the original numerical pass at 1e-9bn.
- 2026-10-15: the first capital-independence guard extracted strings with a JSON
  regex; a quoted BEA source note triggered SyntaxError before publication.
  Traverse the parsed object's string leaves. The quoted-note regression and
  full adopted-case runs exercise the fix; missing/unknown carrier references
  still stop before any output is written.
- 2026-10-15: the30-policy audit took356.151s; a67.960s two-policy CPU profile
  spent51.736s in Engine.clone. Its1.4MB correction provenance was copied before
  Engine.applyCorrections immediately replaced it with payload.meta. New v8-only
  step/zero-padding wrappers omit that discarded copy and restore complete
  metadata. All12 real final models must exactly match original engine steps
  and original API zero-padding, with source immutability and all-spec independent
  API-cost gates retained. P7's routing implementation is unchanged.
- 2026-10-15: concurrent reporter-profile publication exposed an incomplete
  file and the downstream SHA guard stopped. Household producer ownership
  repaired the complete JSON/NPZ writer class with sibling staging and rename,
  physical gates before publication, exact-array/NPZ equality, and failed-budget
  regressions. Generation CSV/JSON outputs now also rename complete siblings;
  serialization failure preserves published bytes. No hash guard is loosened.
- 2026-10-15: the household16-command rerun succeeded but its system-temp
  comparison lost39 snapshots. Backup copies inherited stale source access
  times; disappearance exactly matched the installed03:35/three-day dirhelper
  schedule. Process attribution is an inference (OS logs sandbox-blocked).
  Protected lane-owned TMPDIR prevents recurrence in this task. Global harness
  metadata/diagnostic regression repair is handed to the parent, outside this
  worker's permitted lane scope; `scratchpad/prop8/repro-temp-cause.md` traces
  the callers and retained evidence. The failed comparison is not a PASS.
