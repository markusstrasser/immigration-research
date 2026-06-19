-- requires: context
-- optional: needs ACS PUMS + stage5 rebuild
-- backs: KFF immigrant uninsured-rate disconfirmation (ACS substitute)
SELECT
  state_fips,
  ROUND(100 * MAX(CASE WHEN nativity_group = 'foreign_born' THEN uninsured_rate END), 1) AS foreign_born_uninsured_pct,
  ROUND(100 * MAX(CASE WHEN nativity_group = 'us_native' THEN uninsured_rate END), 1) AS native_uninsured_pct,
  ROUND(100 * MAX(CASE WHEN nativity_group = 'foreign_born' THEN public_coverage_rate END), 1) AS foreign_born_public_pct
FROM acs_immigrant_health_state_summary_2023
GROUP BY 1
HAVING foreign_born_uninsured_pct IS NOT NULL
ORDER BY foreign_born_public_pct DESC NULLS LAST
LIMIT 12;
