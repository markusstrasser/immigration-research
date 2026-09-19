# Education and origin annual results — 2026-09-19

**Verdict:** Below-HS and HS-only Mexico-born residents have materially different
accounts. Among ages 25–64, the personal allocation yields about −$1,951 per
below-HS resident and +$522 per HS-only resident annually before external
institutional costs N or additional average public-goods F. Sharing household
costs yields −$5,558 and −$3,541. These are descriptive 2024-price fiscal balances,
not causal admission effects or complete-government-budget estimates.
[SOURCE: `derived/annual_estimates.csv`, reproduced by `builder.py`; CPS ASEC2025,
MEPS2024, and repaired fiscal inputs listed in `derived/manifest.json`]

## Working-age annual account

Personal allocation, expanded excluding N, ages 25–64, current residents of all
entry durations. Positive means receipts exceed attributed spending. Dollar
intervals are conditional sampling intervals under fixed modeling and calibration
assumptions, not uncertainty bounds on the policy effect.

| Origin | Education | Raw n | Population | Balance/person | Conditional 95% interval |
|---|---|---:|---:|---:|---:|
| Mexico | Below HS | 1,771 | 3.886m | −$1,951 | −$3,413 to −$488 |
| Mexico | HS only | 1,543 | 3.355m | +$522 | −$610 to +$1,655 |
| Other Central America | Below HS | 665 | 1.499m | −$940 | −$3,030 to +$1,149 |
| Other Central America | HS only | 470 | 1.067m | +$1,696 | −$1,294 to +$4,685 |
| Caribbean | Below HS | 180 | 0.520m | −$5,161 | −$7,389 to −$2,932 |
| Caribbean | HS only | 433 | 1.209m | +$3,762 | −$2,458 to +$9,982 |
| South America | Below HS | 91 | 0.245m | −$726 | −$3,052 to +$1,600 |
| South America | HS only | 385 | 0.937m | +$2,365 | −$317 to +$5,046 |
| Southeast Asia | Below HS | 115 | 0.263m | −$2,748 | −$7,708 to +$2,212 |
| Southeast Asia | HS only | 316 | 0.594m | +$5,139 | −$204 to +$10,482 |
| All native | Below HS | 2,601 | 6.207m | −$4,976 | −$6,451 to −$3,502 |
| All native | HS only | 15,060 | 36.486m | +$2,434 | +$1,548 to +$3,320 |

[SOURCE: `derived/annual_estimates.csv`, account `expanded_excluding_N`, allocation
`personal`, entry `stock`, metric `net_per_person`.]

South America below-HS has three unsupported working-age bands and Southeast Asia
below-HS two, under the declared n≥30/ESS≥20 rule. The unstandardized totals above
retain all residents, with that warning; they do not justify fine-grained age
comparisons. SEA and Caribbean aggregates also conceal important country mix.
[SOURCE: `derived/support.csv` and `annual_estimates.csv`.]

## The comparator changes the substantive claim

At the same fixed age distribution, Mexico-born below-HS residents have a **+$2,709**
per-person balance advantage over below-HS natives (conditional 95% interval +$880
to +$4,539), despite their negative absolute account. Mexico-born HS-only residents
have a **−$2,122** gap against HS-only natives (−$3,511 to −$733). Against natives
of all education levels, the corresponding gaps are −$16,519 and −$14,288.
All four comparisons have complete working-age support.
[SOURCE: `derived/comparisons.csv`, personal/expanded_excluding_N/stock,
`common_age_gap_per_person`, all-native reference.]

These answer distinct descriptive questions. Comparing immigrants to the national
all-education average includes education composition differences. Comparing within
education does not identify whether removing or admitting immigrants would replace
them one-for-one with natives of that education. [INFERENCE]

## Support for the next step

Mexico-born below-HS and HS-only stock profiles pass the support threshold in all
six adult age bands. Mexico-born some-college and BA+ profiles do not. Every
recent-entry profile fails at least one adult band, and no recent-entry lifetime
forecast should be presented as observed data. Current attained education and
cross-sectional age profiles do not identify education at admission, life-cycle
progress, descendants, or selective emigration.
[SOURCE: `derived/support.csv`; interpretation limits in `README.md`.]

The run produced 360 age profiles, 720 annual estimates, and 2,592 comparator rows.
The old Mexico adult account, before generalizing school-cost attribution, was
reproduced within $0.000032 in total dollars for every adult band under both
allocation conventions. All education partitions conserve populations, balances,
and medical gradients in every replicate. Eight synthetic tests passed.
[SOURCE: successful builder/test execution, `derived/manifest.json`.]

## Scope limits

Institutional N is excluded and must be shown as a separate matched ACS domain
sensitivity. Medical costs are transported from age×US-birth donor cells; current
education/origin differences in medical behavior are not directly observed here.
Expanded M is jointly propagated with base medical spending rather than treated
as fixed or independent. Model parameters and most fitted allocation coefficients
remain conditioned on; medical/cross-survey transport error is not in the interval.
District D is an observed-ethnicity/state proxy and a D=0 account is available.

This instrument is an LLM-assisted accounting implementation; its political and
framing dispositions are addressed by explicit opposing comparisons, primary
codebook verification, and independently reproducible tables, not assumed away.
[SOURCE: `notes/llm-bias-caveat.md`; computational details in `README.md`.]
