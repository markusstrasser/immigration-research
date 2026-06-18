-- requires: context
-- backs: immigration-verified-findings-report-2026-04-10.md (warehouse inventory)
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'main'
ORDER BY table_name;
