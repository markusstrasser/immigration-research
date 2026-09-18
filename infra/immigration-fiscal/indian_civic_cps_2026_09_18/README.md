# Lane: turnout, volunteering and giving by birthplace (CPS supplements, 2026-09-18)

India-born and second-generation Indian-origin adults against China-born, Mexico-born, all
other foreign-born, US-born non-Hispanic whites and all US-born, from two CPS supplements.

## Inputs

| source | what | where |
|---|---|---|
| `api.census.gov/data/<y>/cps/voting/nov` | Nov Voting & Registration Supplement, 2016 2018 2020 2022 2024 | `_cache/cps_voting_<y>.json` |
| `api.census.gov/data/<y>/cps/volunteer/sep` | Sep Volunteering & Civic Life Supplement, 2019 2021 2023 | `_cache/cps_volunteer_<y>.json` |
| `api.census.gov/data/<y>/cps/asec/mar` | ASEC persons+supp (pulled 2026-09-16 by `../cps_generation_welfare_2026_09_16/pull_cps_asec.sh`) | `$PNY_DATA_ROOT/external/cps/asec/` |
| `www2.census.gov/.../p20/585/table01.xlsx` | published 2020 turnout, the gate anchor | `_cache/p20_585_table01.xlsx` |

`CENSUS_API_KEY` comes from `../acquire/config.local.env` and is never printed.

## Run

```bash
bash scripts/pull.sh                       # ~45 min, 8 parallel nohup'd workers, resumable
UV="uv run --no-project --with pandas>=2 --with numpy>=2"
$UV python3 scripts/analyze_voting.py      # also runs the P20 gate; exits 3 if it fails
$UV python3 scripts/analyze_volunteer.py
$UV python3 scripts/asec_entry.py
$UV --with statsmodels python3 scripts/regressions.py
bash scripts/verify.sh                     # reruns everything and cmp's derived/
```

`scripts/pull.sh` requests **one state per call**. A nationwide `for=state:*` CPS supplement
query returns HTTP 200 with a body truncated mid-record (0.3–2.8 MB of a ~13 MB payload),
under HTTP/2 and `--http1.1` alike — observed 2026-09-18. Each per-state body is asserted to
end in `]]` before it is kept, parts are cached under `_cache/parts/<tag>/`, and the run
resumes from whatever is already complete.

## Outputs (`derived/`)

| file | contents |
|---|---|
| `gate_2020_turnout.txt` | lane vs Census P20-585 published 2020 citizen turnout |
| `voting_rates.csv` | registration and turnout by group, pooled and by year, both non-response conventions |
| `voting_arms.csv` | all-adults, BA+, naturalized-only, self-respondent-only, age 25–54 |
| `naturalization.csv` | naturalized share of the foreign-born by group and age band |
| `asec_naturalization_by_entry.csv` | naturalized share by years since entry (ASEC, the only CPS instrument carrying `PEINUSYR`) |
| `volunteer_rates.csv` | volunteering, giving, group membership, official contact, neighbourliness |
| `volunteer_arms.csv` | self-respondent-only, BA+, citizens-only, age 25–54, income $100k+ |
| `volunteer_hours.csv` | annual volunteer hours, mean/median among volunteers and mean over all adults |
| `regression_turnout.csv`, `regression_civic.csv` | raw vs adjusted birthplace coefficients (LPM, HC1; logit AME alongside) |

Cells with fewer than 50 unweighted observations are suppressed (rate and SE set to NaN;
`n` is still shown).

## Measurement notes

- **Turnout conventions.** `turnout_census_convention` counts item non-response to `PES1` as
  not voting and keeps it in the denominator — this is what the published P20 tables do, and
  it is what the gate checks. `turnout_reported_only` drops non-response from the denominator.
  `vote_item_nonresponse` reports how large that block is per group, because it differs by group
  and therefore moves the gap between the two conventions.
- **SEs** are a Kish design-effect approximation, `n_eff = (Σw)²/Σw²`, `SE = √(p(1−p)/n_eff)`.
  This captures weight variation only, not CPS clustering or stratification, so it is a lower
  bound. The November voting supplement ships no replicate weights; the September supplement
  does (`sep21nrrep.csv`, `sep23nrrep.csv`).
- **No year of entry.** `PEINUSYR` is absent from both supplements — the API rejects it as an
  unknown variable and the public-use file carries only the allocation flag `PXINUSYR`. Years
  in the US is therefore not a control in the regressions and the "recent arrivals excluded"
  arm is run as "naturalized citizens only" instead. `scripts/asec_entry.py` supplies the
  years-since-entry picture from the ASEC, a different month and weight.
- **Giving is a yes/no with no threshold.** The pre-2017 supplement asked about donations of
  $25 or more; the redesigned `PES18` has no threshold and no amount follow-up, so amounts
  cannot be reported and the rates are not comparable to pre-2017 published figures.
- **September 2017 is not on the API** (`2017/cps/volunteer/sep` → 404), so the civic series
  is 2019/2021/2023.
