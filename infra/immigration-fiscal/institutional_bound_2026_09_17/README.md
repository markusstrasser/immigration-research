# Institutional cost bound on the all-age fiscal gaps — September 17, 2026

Bounds how much charging public institutional costs (prisons, jails, nursing facilities) would move
the Mexican-origin fiscal gaps in `../all_age_ledger_2026_09_17/`, which covers the civilian
household population only. Findings and sources: [RESULT.md](RESULT.md).

## Reproduce

From the repository root:

```sh
uv run --no-project python3 infra/immigration-fiscal/institutional_bound_2026_09_17/pull_acs.py
uv run --no-project python3 infra/immigration-fiscal/institutional_bound_2026_09_17/compute_bound.py
```

`pull_acs.py` needs `CENSUS_API_KEY` in the environment or in `../acquire/config.local.env`, and
caches every raw API response under `_cache/`, so a re-run does no network work. `compute_bound.py`
is stdlib only. Both write only inside this directory.

Cost parameters are constants at the top of `compute_bound.py`, each with its source in RESULT.md.
