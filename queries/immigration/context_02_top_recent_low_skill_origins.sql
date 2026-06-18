-- requires: context
-- backs: immigration-verified-findings-report-2026-04-10.md §Executive verdict #3
-- Universe: foreign-born adults 25-64, SCHL<16, YOEP>=2014
SELECT
  origin_label,
  ROUND(weighted_adults) AS weighted_adults
FROM acs_origin_national_2023
ORDER BY weighted_adults DESC
LIMIT 15;
