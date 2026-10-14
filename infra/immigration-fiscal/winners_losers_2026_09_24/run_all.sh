#!/bin/sh
# Imported execution coverage: p7_frames.py p7_cohorts.py p7_credits.py p7_nest.py.
# Directory pytest covers test_winners_losers.py and test_p7_frames.py.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONUNBUFFERED=1
lane=infra/immigration-fiscal/winners_losers_2026_09_24
uv run --no-project python3 "$lane/measured_run.py" node "$lane/specs.cjs" --case oct14
uv run --no-project python3 "$lane/measured_run.py" node "$lane/p7_inputs.cjs"
if [ -n "${P7_PROFILE_OUT:-}" ]; then
    uv run --no-project python3 "$lane/measured_run.py" uv run --no-project python3 -m cProfile -o "$P7_PROFILE_OUT" "$lane/winners_losers.py" --case oct14
else
    uv run --no-project python3 "$lane/measured_run.py" uv run --no-project python3 "$lane/winners_losers.py" --case oct14
fi
uv run --no-project python3 -m pytest "$lane/" -q -o "cache_dir=$lane/_cache/pytest_cache"
uv run --no-project python3 "$lane/p7_document.py"
