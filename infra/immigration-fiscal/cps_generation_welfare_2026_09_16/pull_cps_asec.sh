#!/usr/bin/env bash
# Pull CPS ASEC person microdata (all states) from the Census API for the welfare-by-generation memo.
# Writes $PNY_DATA_ROOT/external/cps/asec/asec_<year>_{persons,supp}.json (raw, read-only afterwards).
# Needs CENSUS_API_KEY (env or acquire/config.local.env); the key is never printed. ~4 min per year.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CFG="$ROOT/acquire/config.local.env"
KEY="${CENSUS_API_KEY:-}"
if [[ -z "$KEY" && -f "$CFG" ]]; then
  KEY=$(rg -o '^\s*(?:export\s+)?CENSUS_API_KEY\s*=\s*"?([^"\s#]+)"?' -r '$1' "$CFG" | head -1 || true)
fi
[[ -n "$KEY" ]] || { echo "[DEGRADED] no CENSUS_API_KEY (env or $CFG); api.census.gov rejects keyless calls" >&2; exit 2; }
ROOT_DATA="${PNY_DATA_ROOT:-$(rg -o '^\s*(?:export\s+)?PNY_DATA_ROOT\s*=\s*"?([^"\s#]+)"?' -r '$1' "$CFG" | head -1 || true)}"
[[ -n "$ROOT_DATA" ]] || { echo "[DEGRADED] PNY_DATA_ROOT unset" >&2; exit 2; }
OUT="$ROOT_DATA/external/cps/asec"; mkdir -p "$OUT"
PERSONS=PENATVTY,PEFNTVTY,PEMNTVTY,PRCITSHP,A_AGE,PERRP,HFOODSP,PAW_YN,SSI_YN,MCAID,CAID,WICYN,HPUBLIC,HLORENT,HHOTLUN,HENGAST,EIT_CRED,MARSUPWT,HSUP_WGT,H_SEQ,PPPOS,PEHSPNON,PRDTRACE,A_HGA,H_NUMPER,HUNDER18,HTOTVAL,PTOTVAL,H_HHTYPE,SPM_SNAPSUB,SPM_EITC,SPM_WICVAL,SPM_SCHLUNCH,SPM_CAPHOUSESUB,GESTFIPS
SUPP=H_SEQ,PPPOS,HFLUNCH,HFLUNNO,HHOTNO,A_SEX,A_MARITL,PRDISFLG,PEIO1COW,A_LFSR,HRHTYPE,H_TENURE,FTOTVAL,PEINUSYR
for y in "${@:-2025 2024}"; do
  for part in persons supp; do
    vars=$PERSONS; [[ $part == supp ]] && vars=$SUPP
    out="$OUT/asec_${y}_${part}.json"
    if [[ -s "$out" ]] && tail -c 8 "$out" | rg -q '\]\]'; then echo "[$y/$part] exists, keep $out"; continue; fi
    tmp="$out.building"
    code=$(curl -s --max-time 900 -o "$tmp" -w "%{http_code}" "https://api.census.gov/data/$y/cps/asec/mar?get=$vars&for=state:*&key=$KEY")
    if [[ "$code" == "200" ]] && tail -c 8 "$tmp" | rg -q '\]\]'; then mv "$tmp" "$out"; echo "[$y/$part] ok $(wc -c < "$out") bytes"
    else echo "[DEGRADED] [$y/$part] http=$code: $(head -c 200 "$tmp" | sed "s/$KEY/KEY/g")" >&2; rm -f "$tmp"; exit 1; fi
  done
done
