-- requires: context
-- optional: needs OHSS state_immigration_data in setup.sh
SELECT
  state_fips,
  State AS state_name,
  refugees_total,
  asylees_total,
  new_arrivals_total,
  lpr_total
FROM ohss_state_immigration_2023
ORDER BY refugees_total + asylees_total DESC NULLS LAST
LIMIT 12;
