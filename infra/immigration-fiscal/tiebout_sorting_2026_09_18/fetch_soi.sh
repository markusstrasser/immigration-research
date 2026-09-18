#!/bin/bash
# IRS SOI state migration data, tax-year pairs 2011-12 .. 2022-23.
# The bundled `<yy><yy>migrationdata.zip` archives (6-14 MB) time out repeatedly on
# irs.gov, so this fetches the individual CSVs (~0.1-0.4 MB) that sit beside them:
#   <yy><yy>inmigall.csv   state totals by AGI bracket, inflow/outflow/nonmigrant
#   stateinflow<yy>.csv / stateoutflow<yy>.csv   state-pair flows, all brackets pooled
set -u
CACHE="$(cd "$(dirname "$0")" && pwd)/_cache"
mkdir -p "$CACHE"
ok=0; bad=0
for y in 1112 1213 1314 1415 1516 1617 1718 1819 1920 2021 2122 2223; do
  for f in "${y}inmigall.csv" "stateinflow${y}.csv" "stateoutflow${y}.csv"; do
    p="$CACHE/$f"
    for a in 1 2 3 4; do
      if [ -s "$p" ] && head -1 "$p" | grep -qi "statefips\|y1_statefips\|y2_statefips"; then break; fi
      rm -f "$p"
      curl -sS --http1.1 --retry 3 --retry-delay 4 --max-time 180 -o "$p" \
        "https://www.irs.gov/pub/irs-soi/$f"
    done
    if [ -s "$p" ] && head -1 "$p" | grep -qi "statefips\|y1_statefips\|y2_statefips"; then
      echo "OK   $f $(stat -f%z "$p")"; ok=$((ok+1))
    else
      echo "FAIL $f"; bad=$((bad+1)); rm -f "$p"
    fi
  done
done
echo "done ok=$ok bad=$bad"
