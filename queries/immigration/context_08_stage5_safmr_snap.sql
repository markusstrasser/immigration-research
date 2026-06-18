-- requires: context
-- optional: needs setup-net-negative.sh + stage5 rebuild (SAFMR/SNAP columns)
-- backs: stage5 SAFMR + SNAP panels (post 2026-06-18 build)
SELECT
  state_fips,
  ROUND(safmr_2br_median_2025, 0) AS safmr_2br_median,
  ROUND(snap_persons_avg, 0) AS snap_persons_avg_fy2023,
  ROUND(snap_benefits_usd / 1e9, 2) AS snap_benefits_billions_fy2023
FROM state_stage5_context_2023
WHERE snap_persons_avg IS NOT NULL
ORDER BY snap_benefits_usd DESC NULLS LAST
LIMIT 12;
