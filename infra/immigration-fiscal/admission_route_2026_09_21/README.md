# Admission route against origin religion: a cross-birthplace test

**Status:** design written 2026-09-21 before the route shares were downloaded or joined. The
outcome proxies for 68 birthplaces (`high_skill_origin_screen_2026_09_21/derived/acs_origin_screen.csv`)
HAD been seen; the predictors had not. Results go in `RESULT.md`.

## Question

Ladder 168 found that a degree converts into very different fiscal balances by birthplace
(India-born +$7.5k against native degree holders, Pakistan/Bangladesh-born −$12.9k). The law
chooses admission routes, not origins. Two readings of the origin differences compete:

- **Route:** outcomes follow how people were admitted (employment, family, diversity lottery,
  refugee or asylee). Origins differ because their route mix differs.
- **Origin religion:** Muslim-majority origins do worse at a given education and route mix.

## Data

- **Routes:** DHS Yearbook of Immigration Statistics, Table 10 (persons obtaining lawful permanent
  resident status by broad class of admission and country of birth), every year FY2004–FY2023,
  pooled. Shares: employment-based; family (family-sponsored preferences plus immediate relatives);
  diversity; refugees and asylees; other. Suppressed cells are dropped from numerator and total and
  counted in the audit file.
- **Outcomes:** ACS 2024 one-year PUMS through the Census tabulate API, foreign-born residents who
  entered in 2000 or later, by birthplace.
  - P1: Medicaid rate among degree holders aged 25–64.
  - P2: share with personal income of $100,000 or more among degree holders aged 25–64.
  - S1–S3: Medicaid rate (all), poverty rate, employment at 25–64, all education levels.
- **Origin religion:** Muslim share of the origin country's population in 2010, Pew Research
  Center, *The Future of World Religions* country table. Continuous share in the main run; a
  majority indicator as a check.
- **Units:** birthplaces with at least 100,000 foreign-born residents in ACS 2024 that match a
  DHS country row (UK components merged; unmatched units listed in the audit file).

## Specification (fixed in advance)

OLS across birthplaces, one observation each, HC3 standard errors; population-weighted as a check.

1. outcome ~ Muslim share
2. outcome ~ Muslim share + employment share + refugee/asylee share + diversity share
   (family and other are the omitted routes); S1–S3 also take the birthplace's degree share.
3. As 2, excluding Mexico and the Central American origins, whose residents are largely outside
   the LPR flow.

**Decision rule.** "Route accounts for it": the Muslim-share coefficient falls by more than half
from model 1 to model 2 and its 95% interval spans zero in both P1 and P2. "An origin-religion
penalty persists": the coefficient keeps its sign with an interval excluding zero in both P1 and
P2 under model 2. Anything else is reported as not settled by this design.

## Limits known before running

- Ecological: about 60 birthplaces, not people. It cannot show that any person's route caused an
  outcome.
- LPR flows leave out temporary workers and students (large for India and China) and unauthorized
  residents; model 3 addresses only the second.
- Emigrants are not a religious cross-section of their country. Iran-, Egypt-, Lebanon- and
  Nigeria-born residents of the US include large non-Muslim shares [TRAINING-DATA]; the Muslim
  share here measures the origin country, not the residents.
- Route shares describe FY2004–2023 green cards; residents who entered since 2000 include people
  who never adjusted status.
- Medicaid eligibility differs by route by law (refugees are eligible on arrival; most other
  routes wait five years), so P1 partly measures the rule, not behaviour. P2 does not share this.

## Run

```sh
cd infra/immigration-fiscal/admission_route_2026_09_21
uv run --no-project --with openpyxl --with xlrd python3 acquire.py      # yearbook workbooks → _cache/
uv run --no-project --with openpyxl --with xlrd python3 class_mix.py    # → derived/lpr_class_mix.csv
set -a; . ../acquire/config.local.env; set +a
uv run --no-project python3 acs_outcomes.py                             # → derived/acs_route_outcomes.csv
uv run --no-project --with numpy python3 analyze.py                     # → derived/route_models.csv
```
