#!/bin/sh
# Imported execution coverage: p7_frames.py p7_cohorts.py p7_credits.py p7_nest.py.
# Directory pytest covers test_winners_losers.py and test_p7_frames.py.
# It also runs test_oct15_core.py test_p8_cohorts.py test_p8_incidence.py
# test_p8_nest.py test_p8_recipient_keys.py test_p8_state_spending.py
# test_p8_social.py test_p8_membership_stayers.py test_p8_group_frame.py.
# Current directory pytest also covers test_p9_calibration.py test_p9_core.py
# test_p9_membership.py test_phase_a_output.py; these explicit names support
# the replay scanner.
set -eu
export OPENBLAS_NUM_THREADS=1 PYTHONUNBUFFERED=1
lane=infra/immigration-fiscal/winners_losers_2026_09_24
uv run --no-project python3 "$lane/measured_run.py" node "$lane/specs.cjs" --case oct16
uv run --no-project python3 "$lane/measured_run.py" node "$lane/p9_inputs.cjs"
if [ -n "${P7_PROFILE_OUT:-}" ]; then
    uv run --no-project python3 "$lane/measured_run.py" uv run --no-project python3 -m cProfile -o "$P7_PROFILE_OUT" "$lane/winners_losers.py" --case oct16
else
    uv run --no-project python3 "$lane/measured_run.py" uv run --no-project python3 "$lane/winners_losers.py" --case oct16
fi
uv run --no-project python3 -m pytest "$lane/" -q -o "cache_dir=$lane/_cache/pytest_cache"
uv run --no-project python3 "$lane/p7_document.py"
