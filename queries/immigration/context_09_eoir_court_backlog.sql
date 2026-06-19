-- requires: context
-- optional: needs EOIR PDF parse in setup.sh
-- backs: TRAC court backlog substitute (EOIR pending cases)
SELECT
  fiscal_year,
  pending_cases,
  initial_receipts,
  total_completions,
  ROUND(100.0 * total_completions / NULLIF(initial_receipts, 0), 1) AS completion_pct
FROM eoir_pending_cases_fy
ORDER BY fiscal_year DESC
LIMIT 10;
