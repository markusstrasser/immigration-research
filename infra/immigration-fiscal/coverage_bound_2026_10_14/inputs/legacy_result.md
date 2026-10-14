claude-opus-5-5

**Verdict:** If the 2020 Post-Enumeration Survey's Hispanic net undercount (4.99%) still sits in the population
controls, the US-born members are undercounted by 1.67M and the main case (v7) understates the cost by **$15.2bn at the
low end and $18.4bn at the high end**: $354.8–442.0bn in place of $339.6–423.6bn. It is an upper bound stated beside
the headline, never added to it: how much of the 2020 undercount the Vintage 2024 controls already absorb is not
measured. [CALCULATION: `coverage_bound.py` → `derived/coverage_bound.json`]

## What it bounds

CPS weights are poststratified to the Census Bureau's population controls by age, sex and Hispanic origin, so the
survey's own Hispanic coverage shortfall (a pre-poststratification ratio of 0.81–0.83) is already corrected and must
not be applied again. What remains is error in the controls, bounded by the 2020 PES Hispanic net undercount of 4.99%,
"a partly absorbed upper bound" [SOURCE: `research/immigration-mexican-origin-population-total-2026-09-19.md` §3; 2020
PES Table B]. Audit row 4 replaces the CPS count of the Mexico-born with the account's 39.71M frame, so the bound
applies to the US-born members only: G2 and G3+ under the generation account's convention a (own and parents'
birthplace). The 3.04M added descendants are in G3+ and are included, because the lineage count derives them from
identity-loss rates on the identified population.

| $bn a year, personal allocation | Low end (spec 16) | High end (spec 11) |
|---|---:|---:|
| G2 cost (14.333M) | 138.0 | 165.5 |
| G3+ cost (17.382M) | 151.6 | 184.7 |
| US-born cost (31.716M) | 289.6 | 350.2 |
| Bound, × (1 / (1 − 0.0499) − 1) = × 0.052521 | 15.2 | 18.4 |
| Main case v7 | 339.6 | 423.6 |
| **Main case with the bound** | **354.8** | **442.0** |

[DATA: `generation_account_2026_09_24/derived/generation_results_oct14.csv`, convention a; the three generations add to
the case's ends within 1e-6bn, a gate in the script] [CALCULATION: G2 and G3+ bound parts in `derived/coverage_bound.csv`]

## What it holds fixed

- The missed members cost what the counted members of their generation do on average (proportional scaling). The
  bound adds 1.666M people at the counted members' average cost.
- It is not an engine run: the group-size responses (general government, roads, parks) and the production term would
  move slightly with a larger group; those moves are not priced.
- The Mexico-born are held at audit row 4's frame. The population memo's wider schemes (PES plus a decay or CMS
  adjustment on the unauthorized, ×1.057–1.076 on everyone) concern the Mexico-born count that row 4 already sets.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/coverage_bound.py
```

Reads the generation account's `oct14` results and `main_case_2026_10_14/derived/summary.json` (`main_case`); writes
`derived/coverage_bound.csv` and `derived/coverage_bound.json`. Stops `[BLOCKED]` if the generation file is missing or
its generations do not add to the case.
