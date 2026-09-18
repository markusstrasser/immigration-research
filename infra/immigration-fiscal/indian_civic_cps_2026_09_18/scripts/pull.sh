#!/usr/bin/env bash
# Pull CPS supplement microdata for the Indian civic-participation lane.
#   - November Voting & Registration Supplement: 2016 2018 2020 2022 2024  (weight PWSSWGT)
#   - September Volunteering & Civic Life Supplement: 2019 2021 2023       (weight PWNRWGT)
#
# api.census.gov silently TRUNCATES large CPS supplement responses: HTTP 200 with the body
# cut mid-record, under HTTP/2 and --http1.1 alike (observed 2026-09-18: a nationwide
# for=state:* query cut at 0.3-2.8 MB of ~13 MB; California cut repeatedly at 0.3-0.8 MB).
# So each request is scoped to ONE STATE and to PRTAGE=18:99 (the analysis universe anyway),
# every body is asserted to end in "]]", and a state that still fails is re-fetched in four
# age bands. Parts are cached per state so an interrupted run resumes.
#
# Writes <lane>/_cache/cps_<supp>_<year>.json, a single JSON array with the header row first.
# Note: the API echoes the predicate variable, so PRTAGE comes back twice; the duplicate
# trailing column is dropped at concatenation.
# Key from infra/immigration-fiscal/acquire/config.local.env; never printed.
set -uo pipefail
LANE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$LANE/../acquire/config.local.env"
KEY="${CENSUS_API_KEY:-}"
if [[ -z "$KEY" && -f "$CFG" ]]; then
  KEY=$(rg -o '^\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*"?([^"\s#]+)"?' -r '$1' "$CFG" | head -1 || true)
fi
[[ -n "$KEY" ]] || { echo "[DEGRADED] no CENSUS_API_KEY" >&2; exit 2; }
OUT="$LANE/_cache"; LOG="$OUT/pull_logs"; PARTS="$OUT/parts"; mkdir -p "$OUT" "$LOG" "$PARTS"

STATES=(01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 \
        31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56)
BANDS=(18:29 30:44 45:59 60:99)

DEMO="PENATVTY,PEFNTVTY,PEMNTVTY,PRCITSHP,PRTAGE,PESEX,PEEDUCA,HEFAMINC,GTMETSTA,PRDASIAN,PEHSPNON,PTDTRACE,PRPERTYP,HURESPLI,PULINENO"
VOTE_VARS="PES1,PES2,PWSSWGT,$DEMO"
VOL_VARS="PES16,PTS16E,PES17,PES18,PES13,PES15,PES4,PES6,PES7,PRSUPVOL,PWNRWGT,PWSSWGT,PUSLFPRX,$DEMO"

get () {  # get <url> <dest> <tries> <tag-label>  -> 0 if a complete "]]" body landed
  local url="$1" dest="$2" tries="$3" lab="$4" code n
  for ((try = 1; try <= tries; try++)); do
    code=$(curl -s --http1.1 --speed-limit 2000 --speed-time 45 --max-time 600 \
      -o "$dest.tmp" -w "%{http_code}" "$url")
    n=$(wc -c < "$dest.tmp" 2>/dev/null || echo 0)
    if [[ "$code" == "200" ]] && tail -c 8 "$dest.tmp" | rg -q '\]\]'; then
      mv "$dest.tmp" "$dest"; echo "$lab ok try$try ($n B)"; return 0
    fi
    echo "$lab retry $try http=$code bytes=$n"
  done
  rm -f "$dest.tmp"; return 1
}

worker_body () {  # worker_body <tag> <url-path> <vars>
  local tag="$1" path="$2" vars="$3" dir="$PARTS/$1" out="$OUT/cps_$1.json"
  local base="https://api.census.gov/data/$path?get=$vars&for=state:"
  mkdir -p "$dir"
  local st f b bf
  for st in "${STATES[@]}"; do
    f="$dir/$st.json"
    [[ -s "$f" ]] && tail -c 8 "$f" | rg -q '\]\]' && continue
    if get "$base$st&PRTAGE=18:99&key=$KEY" "$f" 3 "[$tag] state $st"; then continue; fi
    echo "[$tag] state $st whole-state failed, splitting into age bands"
    for b in "${BANDS[@]}"; do
      bf="$dir/${st}_${b/:/_}.json"
      [[ -s "$bf" ]] && tail -c 8 "$bf" | rg -q '\]\]' && continue
      get "$base$st&PRTAGE=$b&key=$KEY" "$bf" 6 "[$tag] state $st band $b" || {
        echo "[$tag] state $st band $b FAILED"; echo 1 > "$LOG/$tag.done"; return 1; }
    done
  done
  python3 - "$dir" "$out" <<'PY'
import json, sys, pathlib
d, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
parts = sorted(p for p in d.glob("*.json"))
hdr, rows = None, []
for p in parts:
    a = json.loads(p.read_text())
    h = a[0]
    # the API echoes the predicate variable (PRTAGE) as a trailing duplicate column
    keep = [i for i, c in enumerate(h) if c not in h[:i]]
    h = [h[i] for i in keep]
    if hdr is None:
        hdr = h
    assert h == hdr, f"header mismatch in {p}: {h} != {hdr}"
    rows.extend([[r[i] for i in keep] for r in a[1:]])
out.write_text(json.dumps([hdr] + rows, separators=(",", ":")))
print(f"[concat] {out.name}: {len(rows)} rows from {len(parts)} parts")
PY
  local rc=$?
  echo $rc > "$LOG/$tag.done"
  return $rc
}

if [[ "${1:-}" == "--worker" ]]; then worker_body "$2" "$3" "$4"; exit $?; fi

launch () {  # launch <tag> <url-path> <vars>
  local out="$OUT/cps_$1.json"
  if [[ -s "$out" ]] && tail -c 8 "$out" | rg -q '\]\]'; then echo "[cached] $1 ($(wc -c < "$out") B)"; return 0; fi
  rm -f "$LOG/$1.done"
  nohup bash "$0" --worker "$1" "$2" "$3" > "$LOG/$1.log" 2>&1 &
  disown
  echo "[launched] $1 pid=$!"
}

for y in 2016 2018 2020 2022 2024; do launch "voting_$y" "$y/cps/voting/nov" "$VOTE_VARS"; done
for y in 2019 2021 2023; do launch "volunteer_$y" "$y/cps/volunteer/sep" "$VOL_VARS"; done
echo "[pull] launched; markers $LOG/*.done (0=ok), logs $LOG/*.log"
