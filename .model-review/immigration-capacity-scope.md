## Scope
- Target users: personal research now, but intended as reusable public-argument and policy-analysis artifacts
- Scale: currently county-level U.S. immigration panel with 2,390 counties plus small receiver-node panel; designed-for scale is repeated topic updates rather than production serving
- Rate of change: new research memos and analysis scripts arrive in bursts; underlying public datasets update annually or episodically

## Review target
Review the new immigration capacity falsification tranche for bugs, overclaims, silent semantic failures, and mismatches between code outputs and memo claims.
Focus on:
- whether the county panel rebuild in `build_county_outcome_panel.py` correctly materializes both clean pre-COVID windows (`2017–2018` and `2018–2019`), marks `2020`-touching windows as contaminated/descriptive only, and handles QCEW nondisclosure rows defensibly
- permutation / placebo / threshold-search-holdout logic in `analyze_capacity_falsification.py`
- whether the new memos still overstate causal confidence after the `2017` extension, especially around wage identification, threshold stability, and the quarantined IRS domestic-migration channel
- whether the newcomer-comparison layer still overstates what IRS `Total Migration-US` and ACS `Moved from abroad` can identify
- whether the reasoning-evolution doc accurately reflects the actual artifact sequence
