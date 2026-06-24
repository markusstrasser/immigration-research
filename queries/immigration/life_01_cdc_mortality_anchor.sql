-- requires: lifetime
-- optional: needs fetch_cdc_life_tables.sh + build-lifetime.sh
-- backs: SSA table4c6 substitute for NPV mortality anchor
SELECT
  population_group,
  table_id,
  COUNT(*) AS age_intervals,
  ROUND(MAX(ex), 2) AS life_expectancy_at_birth
FROM cdc_period_life_table_2021
WHERE age_interval = '0–1'
GROUP BY 1, 2
ORDER BY life_expectancy_at_birth DESC NULLS LAST
LIMIT 12;
