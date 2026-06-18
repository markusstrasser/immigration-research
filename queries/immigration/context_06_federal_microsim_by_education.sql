-- requires: context
-- backs: immigration-federal-distribution-findings-2026-06-15.md §IV
-- Narrow federal proxy: FICA minus SNAP/TANF/SSI (not full federal ledger)
SELECT
  'mexico_origin' AS group_label,
  education_bucket,
  ROUND(SUM(donor_household_weight)) AS weighted_adults,
  ROUND(SUM(federal_net_proxy_annual * donor_household_weight)
    / NULLIF(SUM(donor_household_weight), 0), 0) AS federal_net_per_adult
FROM acs_origin_household_federal_microsim_2023
WHERE origin_label = 'Mexico'
  AND donor_household_weight IS NOT NULL
GROUP BY 1, 2
ORDER BY weighted_adults DESC;

SELECT
  'nh_white_usborn' AS group_label,
  education_bucket,
  ROUND(SUM(donor_household_weight)) AS weighted_adults,
  ROUND(SUM(federal_net_proxy_annual * donor_household_weight)
    / NULLIF(SUM(donor_household_weight), 0), 0) AS federal_net_per_adult
FROM acs_nh_white_federal_microsim_2023
WHERE donor_household_weight IS NOT NULL
GROUP BY 1, 2
ORDER BY weighted_adults DESC;
