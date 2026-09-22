# Return migration from the US is negatively selected on schooling, among men: ENADID 2018 and 2023

Date: 2026-09-22. [DATA / CALCULATION] Calculation record on Mexico's national demographic
survey; narrative authorship remains operator-owned.

**Verdict:** Mexico-born adults aged 20–64 who lived in the United States five years before
the survey and in Mexico at the survey hold about one year less schooling than Mexico-born
adults who stayed in Mexico: **−1.22 ± 0.18 years in 2018 and −1.03 ± 0.20 in 2023**, with
a tertiary deficit of **13.8 ± 1.5 and 12.3 ± 1.8 points**. The whole effect is male
(men −1.59 ± 0.19 and −1.33 ± 0.21 years; women −0.08 ± 0.39 and +0.05 ± 0.55). The
returnee excess at the bottom of the distribution halved between the waves (+10.1 to +4.8
points) while the tertiary deficit held. A second returnee population runs the other way:
people who left and came back inside the same five-year window are **22–28% tertiary**
against 11–15% for the endpoint returnees, so one attrition parameter cannot serve both
movements. The schooling of departures is unmeasurable in ENADID; the departure table
shows only that returnees left older and are more male. Eight published ENADID figures
reproduce within 0.05 points before any of this is computed.
[CALCULATION: [`enadid_return_selectivity_2026_09_22`](../infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/RESULT.md)]

## 1. Object

ENADID is INEGI's national demographic survey; the 2018 and 2023 waves were acquired and
validated on September 20 (`enadid_2026_09_20`). Two tables are used and never subtracted.
`TSDem` is the resident roster with residence five years before the interview: a returnee
is a Mexico-born resident aged 20–64 who lived in the US at that fixed point; a non-migrant
lived in Mexico. `TMigrante` is the household-reported list of people who left to live
abroad in the window, with a flag for those who came back; it carries no schooling variable,
which was checked against all 55 and 52 dictionary fields, so only the returnees among them
can be linked to a schooling record. Standard errors are Taylor linearizations on the
survey's strata and primary sampling units, validated against a 1,000-draw PSU bootstrap
within 4%. [DATA: `enadid_2026_09_20/README.md` field map; `derived/audit.json`]

## 2. Returnees against non-migrants

Mexico-born, aged 20–64, schooling as recorded at the survey. [DATA:
`derived/return_migrants_by_schooling.csv`]

| Wave | Group | n | Less than lower secondary | Lower secondary | Upper secondary | Tertiary | Mean years |
|---|---|---:|---:|---:|---:|---:|---:|
| 2018 | Returnee from the US | 969 | 38.2 | 30.5 | 20.2 | 11.2 | 8.89 |
| 2018 | Non-migrant | 217,171 | 28.1 | 25.6 | 21.3 | 25.0 | 10.11 |
| 2018 | Difference (± SE) | | +10.1 ± 2.1 | +4.8 ± 1.9 | −1.2 ± 1.5 | −13.8 ± 1.5 | −1.22 ± 0.18 |
| 2023 | Returnee from the US | 647 | 28.0 | 32.2 | 24.3 | 15.5 | 9.56 |
| 2023 | Non-migrant | 208,155 | 23.2 | 26.0 | 23.0 | 27.8 | 10.59 |
| 2023 | Difference (± SE) | | +4.8 ± 2.1 | +6.2 ± 2.3 | +1.3 ± 2.1 | −12.3 ± 1.9 | −1.03 ± 0.20 |

By sex, the mean-years difference is −1.59 ± 0.19 (men, 2018), −1.33 ± 0.21 (men, 2023),
−0.08 ± 0.39 (women, 2018) and +0.05 ± 0.55 (women, 2023); women are 18–19% of the weighted
returnee population. The tertiary deficit is negative in every ten-year age band of both
waves. [DATA: same file, slices `sex:*`, `age:*`]

## 3. Two returnee populations

Restricted to Mexico-born aged 20–64, the returnees in the departure table (left and came
back within the window; n = 602 and 528) are 28.1 ± 2.5% tertiary in 2018 and 22.6 ± 2.3%
in 2023, against 11.2 ± 1.5% and 15.5 ± 1.8% for the endpoint returnees above. The
difference between the two definitions exceeds the difference between returnees and
non-migrants. Departures who returned left older than those still abroad (mean age at
departure 33.3 vs 30.6 in 2018, 35.9 vs 30.5 in 2023) and are more male (74% vs 72%; 85% vs
80%). [DATA: `derived/departures_by_schooling.csv`]

## 4. What it settles for the repo's assumptions

- **Return selection on education.** Supported for longer-stay returns, the movement a
  resident-stock account treats as exit: about one year of schooling, a 12–14 point
  tertiary deficit, men only. Not supported for short circular moves, where selection is
  absent or positive. The [projection back-tests](immigration-projection-backtest-2026-09-19.md)
  found no universally favorable exit direction; this supplies the sign for
  education-selective exit among men, for two five-year windows. [FRAMING-SENSITIVE]
- **Rising education of recent arrivals in US surveys.** The direction of the bias is as
  the concern supposes: because departers who come back are less educated than those who
  stay, a US survey of people still present overstates an arrival cohort's education as it
  departed. ENADID cannot size it, because departures are unmeasured on schooling, and it
  covers only 2013–2023, over which the selection became less negative at the bottom. The
  [arrival-cohort series](immigration-mexican-arrival-cohorts-2026-09-18.md) is quoted for
  orientation only and is not tested here.
- **Lifetime profiles.** The lifetime present values assume no outmigration. Exit that
  removes less-educated men leaves a resident stock more favorable than the arrival cohort;
  a lifetime account with exit would need this selection, in this direction, not a neutral
  attrition rate.

## 5. Limits

Household-reported departures miss whole-household moves. The two returnee populations are
different objects. Five-year windows, not a trend from 1975. Schooling is measured at the
survey, so schooling completed in the US or after return is inside it. No US-side comparator
is computed; the returnee distributions are not comparable to a US-stock distribution
without harmonizing universe, age and timing. Cells under about 150 unweighted cases
(women by age, ages 60–64) carry errors wide enough that only the sign is informative. The
2018 dictionary's documented PSU range is wrong (actual maximum 15,226); national PSU
uniqueness was verified empirically instead. A second, design-naive cut of the same
question exists uncommitted in `enadid_2026_09_20/selectivity.py` from another session and
is not reconciled here.

## 6. Sources

[DATA: INEGI ENADID 2018 and 2023 open-data bundles, DDI dictionaries and *ENADID 2023.
Resultados*, pinned in `infra/immigration-fiscal/enadid_2026_09_20/sources.json`]
[CALCULATION: `infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/enadid_selectivity.py`,
gates in `derived/audit.json`, `test_enadid_selectivity.py` (23 tests)]

## Revisions

- 2026-09-22: created. Ladder 174.
