# Homicide victim–offender distribution and the treasury cost of one homicide

Model self-report: claude-opus-5[1m] (Opus 5, 1M context). September 18, 2026.

**Verdict:** One cleared homicide costs the treasury **$1.5–1.8 million** in the repo's
period-profile frame, **91–97% of it prison**, against a $13.1m social cost and a $13.7m
value of a statistical life — a treasury share of **11.8% to 13.8%**. The victim's own
foregone lifetime balance is between **−$56k and +$75k** on the partial account and is
**negative for every group** on the complete account: a frame in which an elderly or
low-earning victim's death scores as a treasury gain is a property of the average-cost
convention, not a valuation of the life. The distribution headline is a **disconfirmation
hit**: the Hispanic-offender intra-group share is 0.717 on the 61% of cleared cases that
report ethnicity on both sides, **0.667 under a joint-pair imputation** of the missing
cases, and 0.554 under a (biased) independent per-side imputation, while the white figure
holds at 0.81. The ranking of offender groups by treasury cost is **not identified**: the
life-sentence arm spans a factor of three and reverses it.

## Headline numbers

Treasury cost of one cleared homicide by offender ethnicity, partial account, undiscounted,
life share 23.1%, no foster arm, victim distribution reweighted to CDC WONDER:

| offender | victim channel | children | offender channel | total | % of $13.1m social cost |
|---|---|---|---|---|---|
| Hispanic | −56,487 | 100,897 | 1,503,436 | **1,547,846** | 11.8% |
| NH white | +21,432 | 100,836 | 1,485,050 | **1,607,318** | 12.3% |
| NH other | +49,764 | 98,774 | 1,572,789 | **1,721,327** | 13.2% |
| NH Black | +74,546 | 96,690 | 1,640,153 | **1,811,389** | 13.8% |

Complete account: 987,595 / 1,155,063 / 1,195,435 / 1,265,071. At 3%: 1,239,937 / 1,283,836 /
1,365,532 / 1,423,963. Life share 0 → ~$1.0–1.2m; life share 1.0 → $2.8–3.4m **and the
Hispanic cell becomes the most expensive** (younger offenders serve more prisoner-years).

Distribution, SHR universe A (cleared single-victim/single-offender criminal homicide)
2019–2023, ethnicity known both sides, n = 25,675: Hispanic offender → Hispanic victim
0.717, white → white 0.809, Black → Black 0.813. Mean offender age 31.0 Hispanic vs 40.0
white; **age-standardising to a common population structure closes 62% of that gap**
(35.5 vs 38.0). Unsolved share by victim ethnicity: white 0.159, Hispanic 0.364, Black 0.414.
White offenders kill family or an intimate in 44% of cleared cases, Hispanic offenders 26%;
strangers 9% vs 19%. SHR covers **80.0%** of WONDER homicide deaths and over-represents
white victims by a fifth in the ethnicity-known cleared sample.

## Verification

```sh
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/homicide_cost_2026_09_18
UV="uv run --no-project --with pandas>=2 --with numpy>=2 --with requests python3"
$UV wonder_pull.py      # CDC WONDER D158, 6 XML calls, 16s apart (cached under _cache/)
$UV shr_analysis.py     # SHR distributions -> derived/shr_*.csv
$UV cps_parents.py      # CPS ASEC 2025 parent channel
$UV acs_bridge.py       # ACS Mexican-origin bridge (needs CENSUS_API_KEY)
$UV cost_model.py       # treasury cost per homicide
$UV disconfirm.py       # C1/C1b/C2/C3/C4
$UV tables.py           # every memo table
```

Integrity checks that were run and passed:

- **WONDER reproduces the published homicide series.** The NCHS 113-cause category
  GR113-127 returns 26,031 deaths for 2021, the figure published in *Deaths: Final Data for
  2021*. The raw ICD-10 range X85-Y09 returns 25,761 (1.0–1.4% lower every year); the lane
  uses the 113-cause list and keeps both in `derived/`.
- **SHR file integrity.** 352,107,592 bytes, sha256
  `eeedbf5e58a4a2e91d88e8078341210bd2034b57e6d42d0e2de2667020b88a12`, 929,433 rows,
  years 1976–2025, of which 905,648 are murder or non-negligent manslaughter.
- **CPS parent linkage.** 73.0m weighted children under 18; 70.3% with two resident parents,
  25.7% with one, 4.0% with none — consistent with published Census family structure.
- **Reweighting conserves mass.** 98.1% of the raw SHR cell weight survives the
  WONDER reweighting; the residual is cells WONDER suppresses.
- **Profiles reproduce the peer lane.** Victim balances are computed from
  `pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv` unmodified; the white
  third-plus lifetime from age 0 is +$399,670 undiscounted and +$230,502 at 3%, against the peer lane's stated
  +$400k and +$231k.

## Files covered

Scripts: `wonder.py` (CDC WONDER XML API helper), `wonder_pull.py`, `shr_analysis.py`,
`cps_parents.py`, `acs_bridge.py`, `cost_model.py`, `disconfirm.py`, `tables.py`, `BRIEF.md`.

`derived/` (38 CSVs plus `external_params.json`): WONDER deaths by year × Hispanic origin,
by year × origin × race, by 5-year age × origin × race × sex, by single-year age × origin ×
sex, and terrorism codes; SHR victim×offender matrices, missingness by year, clearance by
victim ethnicity, victim and offender age by ethnicity, relationship, circumstance, the
5-way joint cell file, justifiable homicides, intra-group shares; SHR-to-WONDER cell scaling;
ACS Mexican-origin bridge and the full Hispanic-origin breakdown for ages 18–64; CPS parent
channel overall and by age band; victim remaining balances by profile and by cell; the
treasury cost table across 36 arms; and the four disconfirmation outputs.

Memo: `research/immigration-homicide-victim-offender-and-treasury-cost-2026-09-18.md`.

## Files skipped, with reasons

- **FBI Crime Data Explorer NIBRS victim/offender tables.** `api.usa.gov/crime/fbi/cde/...`
  returns `API_KEY_MISSING`; the historical bulk S3 bucket returns `NoSuchBucket` and
  `cde.ucr.cjis.gov/LATEST/s3/signedurl` returns `{}`. An api.data.gov key is required. Per
  the brief the lane stops on that source. Nothing in the cost model depends on it.
- **WONDER population measure.** Rejected on the age × Hispanic-origin crossing with
  "Invalid column name 'pop'". The age-standardisation denominator in C2 comes from CPS ASEC
  2025 instead, which is the same source the ledger uses.
- **Miller et al. (2021) offence-level unit costs.** Already established as paywalled by
  `crime_cost_2026_09_16`; not re-attempted.
- **A national foster-care cost per child-year.** Child Trends' SFY2024 financing survey is
  not published; the lane uses the Texas basic rate, annualised, and states so. The arm is
  worth $8k–$10k per homicide at its maximum, so the substitution does not matter.
- **Conviction probability given clearance.** Not sourced; the cost table is therefore per
  *cleared* homicide with an identified offender, stated in the memo.

## The one thing to carry forward

The life-sentence share is a 2006 BJS parameter (23.1%, *Felony Sentences in State Courts,
2006*, the last edition published) and it is the dominant uncertainty in the entire
calculation — a factor of three, wider than every other arm combined, and it reverses the
ordering of offender groups. Any future use of this lane's cost figures needs a modern
life-sentence share first.
