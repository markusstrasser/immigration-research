**Verdict:** Two calculation failures and one reproduction-coverage declaration
failure found and repaired before handoff.

2026-10-15 — Signed sector losses rejected by a nonnegative replacement-income
helper. The IRS source extraction correctly retains losses (including S NAICS55
and partnership NAICS22/55/71). The first end-to-end run stopped rather than
producing item19. `direct_replacement_loss` now accepts signed source income under
the explicit proportional tax-shield convention; negative replacement ratios
remain errors. The CFC route separately has zero current inclusion on a loss,
without discarding the domestic loss's signed tax shield. `test_item.py` exercises
negative, zero and positive income under domestic cancellation, zero FTC and full
FTC. Loss carryover usability is not identified by this convention.

2026-10-15 — A sector's signed Schedule K allocation ratio cannot be used as an
ownership probability. Utility NAICS22 gives1983.76 and arts NAICS71 gives−0.1436.
The source extractor correctly retains these raw allocations. Integration now
uses only an explicitly named national immediate-individual allocation proxy
(636.097466 / 2551.713803), applied uniformly to sector operating income; it
does not clip the sector ratios or claim to identify ultimate owners. The
probability guard remains, and the regression checks the national proxy applied
to those two source sectors.

2026-10-15 — The reproduction runner byte-matched31/31 artifacts but exited3:
its static coverage instrument could not trace a script path assembled from a
variable list or a pytest directory target. `run.py` now declares literal Path
targets and the documented rerun command names `test_item.py` explicitly. No
`--allow-unrun` exemption is used. A successful final `rerun_lane.py` exit0 is
the regression check for script coverage.
