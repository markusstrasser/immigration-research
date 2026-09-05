-- requires: union
-- backs: immigration-federal-distribution-findings-2026-06-15.md, immigration-europe-caucasian-fiscal-findings-2026-06-15.md
SELECT
  education_bucket,
  ROUND(n_mex) AS mexico_adults,
  ROUND(n_white) AS native_white_adults,
  ROUND(payroll_transfer_mex) AS mexico_payroll_transfer_per_adult,
  ROUND(payroll_transfer_white) AS native_white_payroll_transfer_per_adult,
  comparison_notes
FROM v_education_matched_payroll_transfer
ORDER BY education_bucket;
