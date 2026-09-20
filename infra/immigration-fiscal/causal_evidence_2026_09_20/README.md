# Policy effects and administrative outcome data

Date: 2026-09-20. Evidence and reproducible calculations, not essay prose.

The policy estimates in `estimates.csv` have different treatments, beneficiaries,
horizons and units. They must not be pooled or added to the resident-stock fiscal
account. Run `uv run python3 audit_estimates.py` from this directory for interval
and unit arithmetic. This is primary-table verification, **not microdata
replication**. Normal intervals from rounded published SEs are approximate;
permutation p-values are never converted into invented confidence intervals.

## Primary sources

- Goncalves, Jacome and Weisburst, Census CES26-23 (April 2026), Table 2, printed
  p.40. Source: https://www2.census.gov/library/working-papers/2026/adrm/ces/CES-WP-26-23.pdf
  SHA256 `f55800314df723a24e217d7ebbd801ee8a808fcd9d569f4d59808c6aca8be221`.
  Cached PDF and text under `_cache/`. County-linked NCVS is restricted. Public
  replication record: https://doi.org/10.3886/E242546V1 . Public code does not
  make the confidential geographic records public.
- St. Clair, August 9, 2024 manuscript, Table 2 printed p.37 and Table 4 p.39:
  https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift_5.pdf .
  Full text and tables read through the web PDF reader; direct local download
  returned HTTP403. Final publication DOI `10.1016/j.regsciurbeco.2024.104053`
  confirms the qualitative result, but final numerical-table identity remains
  unverified. No source hash is invented for an unacquired PDF.
- Clemens and Lewis, published July 2026, Table 2; final institutional reprint:
  https://www.piie.com/sites/default/files/2026-07/wp26-11.pdf . Source and full
  prior verification remain in `../frontier_execution_2026_09_17/policy/`.
- CBO, https://www.cbo.gov/publication/61464 , Appendix A, school-cost method.
  The enrollment/spending relationship is an observational calibration. It does
  not independently identify a causal service-cost elasticity.
- Cullen and Steigerwald, *Effective Number of Clusters and Inference with
  Instrumental Variables*, June 2020 draft, section 5.1 and Table 3:
  https://drive.google.com/file/d/1--EQ3f2bnmSkUyunNKyxKyg7o_xh9hVQ/view .
  Cached PDF SHA256
  `982b17ea5a7b034bc759a3dfaa8d2dc91e2d98c25a677fd8256ed732de439fd1`.
  Their selected Chalfin specification has 92 nominal but 11 effective clusters;
  deleting one cluster changes |t| from 2.05 to 1.29. The inspected passage does
  not name its crime outcome; this is not evidence that every coefficient reverses.

## Crime-harm accounting contract

User instruction, 2026-09-20: crossing without enforcement resources or separate
harm receives no event-level dollar charge merely because it is an offense.

1. Immigration-only administrative/criminal offenses are excluded from the
   violent/property victim-harm outcome. A status or law violation has no unit
   victim-harm price.
2. Actual extra enforcement, court or detention resources belong in government
   costs. Attribute the policy/horizon that creates the expenditure; count once.
3. Injury, property loss and mortality risk require actual harm and a matched
   counterfactual. Causal victim-harm change is the change in incident counts
   by offense times victim-only valuations, for the declared beneficiaries.
4. Do not add police/prison spending twice, full VSL plus overlapping earnings
   losses, or a consumer-price benefit already in production surplus. Avoided
   victim harms are benefits, not a mechanically nonnegative charge.
5. A victimized person-month is not an incident count or a distinct annual victim.
   NCVS does not include homicide. Arrest changes can reflect reporting and
   enforcement. Do not price them as changes in offenses.
6. A policy design on Hispanic people does not identify Mexican-origin status,
   descendants, or the exact complement of the fiscal account's target.

## What a causal extension must establish

Specify the intervention, comparison, exposed population, adjustment horizon and
whose welfare counts before estimation. The current 40.897m stock account keeps
its assumptions; these studies do not turn it into an identified admission or
removal effect. For a new event study, first reproduce its treatment and outcome
definitions, inspect timing selection, anticipation, spillovers, reporting and
pretrends, then choose an estimator compatible with staggered treatment. A flat
pretrend alone does not prove exogeneity. Do not divide enforcement effects by
population changes without defending the exclusion restriction.

The external corpus supplies outcomes and denominators. Its county tax files do
not identify ethnicity or nativity; BEA transfers do not measure a group's public
service use. Keep these distinctions in every merge and regression.

See [CORPUS.md](CORPUS.md) for the executed 72.12 MB acquisition, unit and geographic
checks, run commands and [SOURCES.json](SOURCES.json) for pinned input hashes.
`raw/`, `derived/` and `_cache/` are ignored. The published-table extract is tracked
as source evidence; calculated intervals are regenerated.
