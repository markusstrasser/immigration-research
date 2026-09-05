-- requires: context
-- backs: immigration-federal-distribution-findings-2026-06-15.md §IV
-- Employee OASDI/HI proxy minus allocated SNAP/TANF and individual SSI.
-- These are matched ACS adults; donor weights do not count target adults.
SELECT
  'mexico_origin' AS group_label,
  education_bucket,
  ROUND(SUM(weighted_adults)) AS weighted_adults,
  ROUND(SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults)
    / NULLIF(SUM(weighted_adults), 0), 0) AS payroll_less_benefits_per_adult
FROM acs_origin_person_payroll_transfer_microsim_2023
WHERE origin_label = 'Mexico'
  AND donor_person_weight IS NOT NULL
GROUP BY 1, 2
ORDER BY weighted_adults DESC;

SELECT
  'nh_white_usborn' AS group_label,
  education_bucket,
  ROUND(SUM(weighted_adults)) AS weighted_adults,
  ROUND(SUM(payroll_less_allocated_benefits_proxy_annual * weighted_adults)
    / NULLIF(SUM(weighted_adults), 0), 0) AS payroll_less_benefits_per_adult
FROM acs_nh_white_person_payroll_transfer_microsim_2023
WHERE donor_person_weight IS NOT NULL
GROUP BY 1, 2
ORDER BY weighted_adults DESC;
