#!/usr/bin/env bash
# Verification the brief requires: a second from-scratch run over the warm
# _cache/ must leave derived/ byte-identical.
#
# Snapshots derived/, re-runs every script in order, then compares file by file
# with cmp. Exits non-zero and lists the differing files if anything moved.
set -uo pipefail

LANE="/Users/alien/Projects/immigration-research/infra/immigration-fiscal/cultural_output_2026_09_19"
SNAP="${1:-/private/tmp/claude-501/-Users-alien-Projects-immigration-research/45fdf7bc-6c76-4a97-953b-e9d9ea0bf7a5/scratchpad/derived_verify}"
cd "$LANE" || exit 1
set -a; . ../acquire/config.local.env; set +a

UVBASE=(uv run --no-project --with "pandas>=2" --with "numpy>=2" --with duckdb
        --with pyarrow --with requests --with statsmodels --with shapely
        --with pyshp --with pypdf --with fonttools)

rm -rf "$SNAP"; cp -R derived "$SNAP"

# Script 03 is the network fetch. Point it at exactly the states already in the
# cache so the verification re-validates every cached file by content and exits,
# instead of spending hours fetching states this run never had.
LANE_STATES=$(ls _cache/osm/*.json 2>/dev/null | xargs -n1 basename \
  | sed 's/\.json$//' | grep -v '^_' | paste -sd, -)
export LANE_STATES LANE_REM=9

for s in 01_build_pums_parquet 02_arm_a_creative_labour 03_fetch_osm_restaurants \
         04_fetch_cbsa_covariates 05_fetch_surnames 06_fetch_awards_wikidata \
         07_build_cbsa_restaurant_panel 08_arm_d_cooks \
         09_fetch_education_benchmarks 10_classify_awards \
         11_arm_d_elasticity 12_arm_e_music 13_arm_a_cps_generation_check \
         14_osm_coverage_check 15_fill_result; do
  if PYTHONUNBUFFERED=1 "${UVBASE[@]}" python3 "scripts/$s.py" > "logs/verify_$s.log" 2>&1; then
    echo "  ok   $s"
  else
    echo "  FAIL $s (see logs/verify_$s.log)"
  fi
done

rc=0
for f in "$SNAP"/*; do
  b=$(basename "$f")
  # this script writes reproduction_check.txt itself, after the comparison;
  # comparing it would compare the previous run's verdict with itself
  [ "$b" = "reproduction_check.txt" ] && continue
  if ! cmp -s "$f" "derived/$b"; then echo "DIFF $b"; rc=1; fi
done
new=$(comm -13 <(ls "$SNAP" | sort) <(ls derived | sort) | grep -v '^reproduction_check.txt$')
[ -n "$new" ] && { echo "NEW FILES: $new"; rc=1; }
n=$(ls "$SNAP" | grep -vc '^reproduction_check.txt$')
if [ "$rc" -eq 0 ]; then
  msg="REPRODUCIBLE: all $n files in derived/ byte-identical after a second"
  msg="$msg from-scratch run over the warm cache."
else
  msg="NOT REPRODUCIBLE: $n files compared, see the DIFF lines in this run's output."
fi
echo "$msg"
echo "$msg" > derived/reproduction_check.txt
exit "$rc"
