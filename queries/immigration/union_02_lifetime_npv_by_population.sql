-- requires: union
-- backs: immigration-sweep-cycles-23-32-2026-06-15.md cycle 23, immigration-mexico-npv-population-synthesis-2026-06-15.md
SELECT
  population_group,
  ROUND(MAX(CASE WHEN fiscal_layer = 'lifetime_npv' THEN value_per_adult_weighted END)) AS npv_per_adult,
  ROUND(MAX(CASE WHEN fiscal_layer = 'federal_annual' THEN value_per_adult_weighted END)) AS federal_per_adult
FROM v_country_fiscal_rollup
WHERE effect_order = 1
GROUP BY 1
HAVING npv_per_adult IS NOT NULL
ORDER BY npv_per_adult;
