**Verdict:** The four follow-up lanes' reported headline quantities reconcile with
their saved outputs. The code review identified guard/provenance improvements,
not a change to the reported empirical ordering. No complete-counterfactual
validation follows from these checks.

September 28, 2026. Review covers the new `validation_schools`, `validation_medical`,
`validation_fiscal_years` and `validation_mariel` lanes, all dated `2026_09_28`.

- Cursor Composer's patterns scout reviewed nine Python files in four bounded
  directory packets: 43 findings (one high, 32 medium, ten low). The parent's
  triage rejects the high school-support finding: the documented availability
  amendment excludes unsupported New Jersey rows from every prediction arm,
  reports them with `[DEGRADED]`, and retains them in observed resource tables.
  Prediction itself fails on unknown states. This is a disclosed population
  restriction, not a silent fallback.
- Confirmed: Python `assert` must not disable fiscal source/identity guards under
  optimized execution; CMS2022 acquisition and analysis pins need one definition;
  Mariel scoring should reject a nonpositive normalization level. All three were
  repaired and regression-tested. Explicit NumPy testing calls remain active
  under optimization. None changes the measured numerical outputs.
- Rejected as defects: alternative price bases across separately labelled school
  panels; common bootstrap draws across outcomes; differing parser paths for
  different file layouts; different exception types for optimizer versus input
  failures; absolute normalization for signed budget balances; and the alleged
  unpinned school panel (already fingerprinted by `load_joint`, with end-of-run
  integrity verification). Style-only and hypothetical refactors were not applied.
- A separate read-only claim check recalculated the headline tables directly from
  CSV/JSON, including school weighting alternatives, medical gaps/decomposition,
  fiscal shares and IRS scores, and Mariel annual gaps/placebo ranks. It verified
  the medical institutional-exclusion correction against the pinned CMS guide.
  It did not rerun raw builders or substitute for the code review.

The final synthesis retains failed alternatives and labels conditional inputs,
overlapping outcomes, incomplete population alignment and unsupported causal
translations. Reproduction and lane-specific tests are in each result/README.
Raw-data reconstruction outside these new lanes, prospective new-year validation,
and validation of final calibrated national keys remain outside this review.
