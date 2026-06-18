-- requires: context
-- backs: immigration-federal-distribution-findings-2026-06-15.md §III–IV
-- Foreign-born all ages 25-64 education mix (ACS weighted)
SELECT
  education_bucket,
  ROUND(weighted_adults) AS all_fb_adults
FROM acs_foreign_born_education_bucket_totals_2023
WHERE education_bucket != 'other'
ORDER BY all_fb_adults DESC;

-- NH white by nativity (1=US-born, 2=foreign-born)
SELECT
  CASE nativity WHEN 1 THEN 'nh_white_usborn' WHEN 2 THEN 'nh_white_fborn' ELSE CAST(nativity AS VARCHAR) END AS group_label,
  education_bucket,
  ROUND(weighted_adults) AS adults
FROM acs_nh_white_education_by_nativity_2023
WHERE education_bucket != 'other'
ORDER BY group_label, adults DESC;
