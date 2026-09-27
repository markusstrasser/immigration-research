# Joint Mariel school-budget validation

Fixed September 28 before calculating new joint fits. The earlier separate fits
and outcomes were already inspected; this is retrospective validation.

- **Construct:** can one donor-weight vector predict Dade school finances across
  several endpoints and preserve the revenue/expenditure identities? Does it
  improve pretreatment prediction versus a simple donor-growth rule?
- **Input:** existing reviewed GFD school panels. Primary: 29 districts with
  consistently observed June30 fiscal dates (Dade plus28 donors). Secondary:
  source-year full pool, with its unresolved calendar caveat. Existing donor
  eligibility excludes Dade, Broward/Palm Beach and colleges.
- **Fit:** nonnegative weights summing to one, shared across seven primitive
  components: own-source revenue, federal/state/local transfers, operating
  expenditure, capital outlay and interest. Each component is divided by its
  treated training mean, floored at1% of treated training total revenue to prevent
  a near-zero component dominating. No post-training value enters fitting/scales.
- **Sensitivity:** fit every primitive in a common total-revenue unit instead of
  equal relative component units. This changes importance weights explicitly.
  No winning specification is selected after scoring.
- **Budget:** reported revenue and expenditure totals are predicted with the same
  weights. Carry reported-minus-sum residuals separately, including negative
  residuals. Revenue-minus-expenditure is a school financing balance, not an
  all-government fiscal effect. A dollar of outside grants is revenue locally,
  not a national saving. Source units are nominal thousands in each fiscal year;
  ratios and within-year differences avoid summing different price years.
- **Temporal test:** fit1970–76; score1977–79 before the1980 event. Baseline freezes
  the target's1976 component mix and scales all components by the equal-weight
  mean donor total-expenditure growth since1976. All methods may observe donor
  outcomes in the scored year, as synthetic controls do. None observes the scored
  target outcome when fitting or predicting.
- **Scores:** endpoint RMSE and signed mean error as percentages of that endpoint's
  mean observed training level, with the same1%-revenue floor. Primary comparison:
  average squared normalized error over reported revenue, expenditure, operating,
  own revenue and federal/state transfers. Also retain absolute dollar errors
  and budget-balance errors. Improvement is descriptive; no population or
  randomized-assignment test is claimed.
- **Historical event diagnostic:** refit the same rules on1970–79, omit1980,
  report every1981–90 annual gap. These values cannot be described as observed
  causal effects merely because a preperiod predicts well.
- **Stress checks:** delete the largest donor; apply the same joint fit to each
  donor as a placebo with Dade always excluded. Preserve all placebos and their
  fit quality; rank total-expenditure post/pre RMSPE only as a conditional
  diagnostic. No formal multiplicity-adjusted causal inference is attempted.
- **Eligibility:** require complete finite primitive/reported endpoints on the
  named years, never select by postperiod effect size. Report any removed units.
  Source completeness/calendar screens already inspect later records; they are
  not an untouched prospective design. Annual source discrepancies are retained.
- **Guards:** finite arrays, unique district-years, no treated placebo donor,
  convex weights, budget identities, test-outcome mutation invariance, and a
  hand-constructed convex-mixture recovery. Fail on optimizer failure.
- **Stop:** execute these fixed alternatives once; fix implementation defects,
  never tune to a desired effect or score. No new national account estimate.
