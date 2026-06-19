-- requires: context
-- optional: needs SAIPE + ACS school-age panels in stage5 rebuild
-- backs: EDFacts EL substitute — foreign-born school-age + SAIPE poverty pressure
SELECT
  s.state_fips,
  ROUND(a.foreign_born_school_age_weighted) AS fb_school_age_wgt,
  ROUND(100 * sp.saipe_school_poverty_rate, 1) AS school_age_poverty_pct,
  ROUND(n.per_pupil_current_expenditure_usd) AS per_pupil_usd
FROM state_stage5_context_2023 s
LEFT JOIN acs_foreign_born_school_age_state_2023 a USING (state_fips)
LEFT JOIN saipe_state_school_poverty_2023 sp USING (state_fips)
LEFT JOIN census_state_per_pupil_2023 n USING (state_fips)
WHERE a.foreign_born_school_age_weighted IS NOT NULL
ORDER BY fb_school_age_wgt DESC NULLS LAST
LIMIT 12;
