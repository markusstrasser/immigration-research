-- requires: union
-- backs: immigration-school-burden-per-adult-2026-06-15.md, immigration-conclusion-audit-running-fixes.md
-- NOTE: origin school/net rows may be NULL after June 2026 same-universe guard
SELECT
  population_group,
  ROUND(federal_per_adult) AS federal_per_adult,
  ROUND(school_per_adult) AS school_per_adult,
  ROUND(net_crude_per_adult) AS net_crude_per_adult,
  ROUND(weight_adults) AS weight_adults
FROM v_three_layer_annual
ORDER BY population_group;
