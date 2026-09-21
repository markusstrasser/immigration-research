# Military service among US-born men by ancestry, ACS 2024

Model self-report: claude-fable-5-1. 2026-09-21.

**Verdict:** US-born men of Asian Indian ancestry have served on active duty at about one-seventh
the rate of US-born men of English, German or Irish ancestry: 1.05% (±0.21) against 6.6–7.8% at
ages 18–49. The gap does not close at equal education (0.79% against 6.7–6.9% among degree
holders aged 25–49) or in a narrow age band (0.77% against 5.8–7.0% at 25–34). It is not an
"Asian" or a "high-income group" pattern: Korean- and Filipino-ancestry degree holders serve at or
above the white rate, while Chinese and Vietnamese ancestry sit low with the Indian figure. US-born
men of Mexican ancestry serve at about the white rate overall and above it among degree holders
(8.2% against 6.7–6.9%). Service is one costly behaviour, not a measure of patriotism.
[CALCULATION: `derived/military_service_by_ancestry.csv`]

## Table

US-born men, share ever on active duty (`MIL` 1 or 2), by first-reported ancestry (`ANC1P`).
ACS 2024 one-year PUMS through the Census tabulate API. Ancestries with under 50,000 men in a
universe are dropped (—).

| Ancestry | 18–49, all | 25–49, degree | 25–34, all | 25–34, degree |
|---|---:|---:|---:|---:|
| Puerto Rican | 8.0% | 13.3% | | |
| African American | 6.6% | 10.4% | | |
| Filipino | 9.3% | 8.6% | 9.2% | 5.7% |
| "American" | 6.9% | 9.6% | 6.9% | 5.8% |
| Irish | 7.8% | 6.9% | 7.0% | 4.3% |
| German | 7.1% | 6.7% | 6.5% | 4.4% |
| English | 6.6% | 6.9% | 5.8% | 4.5% |
| Mexican | 5.7% | 8.2% | 5.2% | 4.5% |
| Korean | 5.9% | 6.7% | 4.8% | — |
| Japanese | 6.1% | 4.1% | — | — |
| Italian | 5.6% | 4.7% | 5.2% | 3.2% |
| Russian | 3.8% | 3.6% | | |
| Vietnamese | 3.1% | 1.9% | 4.6% | — |
| Chinese | 2.5% | 1.6% | 3.0% | 1.3% |
| **Asian Indian** | **1.05%** | **0.79%** | **0.77%** | **0.15%** |

Asian Indian cells: 247,026 men aged 18–49, 131,106 degree holders aged 25–49, 82,807 aged 25–34,
72,024 degree holders aged 25–34. Approximate standard errors 0.21, 0.24, 0.30 and 0.14 points.
Blank cells were not printed by the name filter; the CSV holds every ancestry above the threshold.

## What would weaken this, and what was checked

- **Age.** US-born men of Indian ancestry are young, and "ever served" accumulates. Checked: the
  25–34 band shows the same ratio.
- **Education.** Enlistment falls with education. Checked: the gap is as large among degree
  holders, where service mostly means a commission.
- **Parental income.** Not observable in the ACS. Indian second-generation households sit in the
  top income fifth, where enlistment is lower for every group [TRAINING-DATA]. If top-fifth whites
  serve at half the white average, about 3.5%, the Indian figure is still a third of it
  [INFERENCE]. Unresolved; the Korean and Filipino rows argue against income as the whole story.
- **Geography.** Indian-ancestry residents concentrate in metros with low enlistment. Not checked;
  needs microdata with state or PUMA, not the tabulate API.
- **Ancestry reporting.** `ANC1P` is the first ancestry written in; people who write "American"
  are a selected group with high service rates, which is why that row is shown.

## Limits

One survey year. Standard errors are binomial approximations on a 1% sample, without replicate
weights, and understate the design-based ones. Men only. US-born of any generation: for Indian
ancestry that is almost entirely the second generation; for European ancestries it is the fourth
and later. Reserve or guard training only (`MIL` 3) is excluded from "ever on active duty".
[FRAMING-SENSITIVE: reading a service rate as attachment to the country is a judgment; the
number is a behaviour. The Indian-origin memo's giving, volunteering and turnout measures are
the companions.]

[INSTRUMENT] LLM-conducted on a charged topic; see `notes/llm-bias-caveat.md`.

## Run

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 infra/immigration-fiscal/civic_service_by_ancestry_2026_09_21/service.py
```
