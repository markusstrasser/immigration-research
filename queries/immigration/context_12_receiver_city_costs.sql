-- requires: context
-- optional: needs receiver city CSV (fixture or immigration-causal)
SELECT
  city,
  fiscal_year,
  total_spending_usd_M,
  peak_shelter_census,
  baseline_shelter_census
FROM receiver_city_migrant_costs
ORDER BY total_spending_usd_M DESC NULLS LAST
LIMIT 12;
