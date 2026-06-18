-- requires: context
-- backs: immigration-verified-findings-report-2026-04-10.md §Executive verdict #5
-- Origins with highest PUMA median rent vs their state average (large groups)
WITH state_rent AS (
  SELECT state_fips, AVG(median_gross_rent) AS state_avg_rent
  FROM origin_puma_context_2023
  WHERE median_gross_rent IS NOT NULL
  GROUP BY 1
),
origin_puma AS (
  SELECT
    c.origin_label,
    c.state_fips,
    c.puma_code,
    c.weighted_adults,
    c.median_gross_rent,
    s.state_avg_rent,
    c.median_gross_rent - s.state_avg_rent AS rent_premium
  FROM origin_puma_context_2023 c
  JOIN state_rent s ON c.state_fips = s.state_fips
  WHERE c.median_gross_rent IS NOT NULL
),
origin_agg AS (
  SELECT
    origin_label,
    SUM(weighted_adults) AS adults,
    SUM(rent_premium * weighted_adults) / NULLIF(SUM(weighted_adults), 0) AS wtd_rent_premium
  FROM origin_puma
  GROUP BY 1
  HAVING SUM(weighted_adults) > 50000
)
SELECT
  origin_label,
  ROUND(adults) AS weighted_adults,
  ROUND(wtd_rent_premium, 0) AS rent_premium_vs_state_avg_usd
FROM origin_agg
ORDER BY wtd_rent_premium DESC
LIMIT 10;
