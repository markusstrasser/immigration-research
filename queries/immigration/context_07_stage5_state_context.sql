-- requires: context
-- backs: immigration-net-negative-dataset-frontier-2026-06-15.md (stage5 local cost)
-- After standard build with setup-net-negative: includes SAFMR + SNAP columns
SELECT
  state_fips,
  ROUND(rpp_all_items_2023, 2) AS rpp_2023,
  ROUND(medicaid_total_computable / 1e9, 2) AS medicaid_billions,
  ROUND(lep_count_reported) AS lep_district_count_2018
FROM state_stage5_context_2023
WHERE rpp_all_items_2023 IS NOT NULL
ORDER BY medicaid_total_computable DESC NULLS LAST
LIMIT 12;
