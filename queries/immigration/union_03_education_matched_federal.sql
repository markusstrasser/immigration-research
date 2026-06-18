-- requires: union
-- backs: immigration-federal-distribution-findings-2026-06-15.md, immigration-europe-caucasian-fiscal-findings-2026-06-15.md
SELECT
  education_bucket,
  ROUND(n_mex) AS mexico_adults,
  ROUND(fed_mex) AS mexico_fed_per_adult,
  ROUND(fed_white) AS white_fed_per_adult,
  ROUND(ratio_mex_to_white_adj, 2) AS ratio_mex_to_white,
  cell_verdict
FROM v_education_matched_federal
WHERE n_mex > 100000
ORDER BY education_bucket;
