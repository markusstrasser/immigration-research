-- requires: context
-- backs: immigration-verified-findings-report-2026-04-10.md §Executive verdict #4
-- Linked-household child exposure (WGTP-corrected), not full-stock school burden
SELECT
  origin_label,
  ROUND(linked_mean_hh_school_age_children, 3) AS mean_school_age_children_per_linked_hh,
  ROUND(linked_share_households_with_school_age_children_pct, 1) AS pct_hh_with_school_age
FROM acs_origin_household_national_2023
WHERE linked_household_wgt > 1000
ORDER BY linked_mean_hh_school_age_children DESC
LIMIT 12;
