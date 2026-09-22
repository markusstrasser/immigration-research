# ENADID 2018 and 2023 — schooling of Mexico-born return migrants from the United States

**Verdict:** Return migration from the United States is negatively selected on education,
and the selection is almost entirely a male phenomenon. Among Mexico-born adults aged 20–64
resident in Mexico, those who lived in the United States five years earlier hold 8.89 ± 0.18
years of schooling in 2018 against 10.11 ± 0.02 for those who lived in Mexico, a gap of
−1.22 ± 0.18 years; in 2023 the figures are 9.56 ± 0.20 against 10.59 ± 0.02, a gap of
−1.03 ± 0.20 [CALCULATION: enadid_selectivity.py; DATA: derived/return_migrants_by_schooling.csv].
The deficit is concentrated at the top of the distribution and is stable across the two
waves: returnees are 13.8 ± 1.5 points less likely to hold a tertiary qualification in 2018
and 12.3 ± 1.8 points less likely in 2023, while the excess at the bottom band shrank from
+10.1 ± 2.1 to +4.8 ± 2.1 points. Splitting by sex, men returnees run −1.59 ± 0.19 years
(2018) and −1.33 ± 0.21 (2023) below non-migrant men, whereas women returnees are
statistically indistinguishable from non-migrant women in both waves (−0.08 ± 0.39 and
+0.05 ± 0.55). The comparison against **recent departures cannot be made on schooling**:
`TMigrante` carries no schooling variable in either wave, and the only route to one, the
household person link, exists by construction only for people who came back, so that branch
stops as the brief directs. What the departure table does show is that returnees left older
than those still abroad (mean age at departure 33.3 ± 0.7 against 30.6 ± 0.5 in 2018;
35.9 ± 0.7 against 30.5 ± 0.3 in 2023) and are more male. A second, sharper result falls out
of the two returnee definitions: short-duration returnees, who left and came back inside the
same five-year window, are **not** negatively selected at all, holding 28.1 ± 2.5 percent
tertiary in 2018 and 22.6 ± 2.3 in 2023 against 11.2 ± 1.5 and 15.5 ± 1.8 for the
longer-stay endpoint definition. "Return migrant" is not one population, and which one is
meant changes the sign of the selectivity finding.

All four published anchors reproduce before any number above was computed. No net-migration
quantity is produced anywhere in this lane.

## Anchors reproduced first

[DATA: derived/anchor.csv] [SOURCE: INEGI, *ENADID 2023. Resultados*, acquired as
`enadid_2026_09_20/_cache/resultados_enadid23.pdf`, prior-residence and destination-country
charts]

| Wave | Published figure | Published | Reproduced | SE | Gap (pp) |
|---|---|---:|---:|---:|---:|
| 2018 | Population 5+, lived in same state five years before | 96.6 | 96.646 | 0.069 | +0.046 |
| 2018 | Population 5+, lived in another state | 2.9 | 2.913 | 0.065 | +0.013 |
| 2018 | Population 5+, lived in another country | 0.4 | 0.442 | 0.021 | +0.042 |
| 2018 | International emigrants whose destination was the US | 84.8 | 84.842 | 1.130 | +0.042 |
| 2023 | Population 5+, lived in same state five years before | 96.7 | 96.684 | 0.066 | −0.016 |
| 2023 | Population 5+, lived in another state | 3.0 | 2.971 | 0.064 | −0.029 |
| 2023 | Population 5+, lived in another country | 0.3 | 0.345 | 0.016 | +0.045 |
| 2023 | International emigrants whose destination was the US | 87.9 | 87.917 | 0.782 | +0.017 |

The largest gap is 0.046 pp against figures the source prints to one decimal, so every
anchor is inside its own rounding. The prior-residence anchor validates the exact variable
this lane's main result rests on (`p3_19` in 2018, `p3_24` in 2023).

Two further weighted totals reproduce the independently validated examples in the
acquisition lane [DATA: enadid_2026_09_20/RESULT.md]: US-destination departures of 645,458
(2018) and 1,072,331 (2023), and returnees within those cohorts of 220,218 and 215,021.

## Returnees against non-migrants, Mexico-born aged 20–64

[DATA: derived/return_migrants_by_schooling.csv, slice `all`] [CALCULATION: enadid_selectivity.py]

Returnee means resident in the United States five years before the survey; non-migrant
means resident in Mexico five years before. People who lived in a third country are in
neither group. Schooling is measured at the survey.

**2018** — returnees n = 969 (weighted 270,023); non-migrants n = 217,171 (weighted 70,883,813)

| Band | Returnee % | SE | Non-migrant % | SE | Difference (pp) | SE |
|---|---:|---:|---:|---:|---:|---:|
| Less than lower secondary | 38.22 | 2.09 | 28.11 | 0.18 | +10.11 | 2.09 |
| Lower secondary | 30.45 | 1.86 | 25.62 | 0.15 | +4.83 | 1.86 |
| Upper secondary | 20.16 | 1.51 | 21.30 | 0.15 | −1.15 | 1.52 |
| Tertiary | 11.18 | 1.46 | 24.97 | 0.19 | −13.79 | 1.46 |
| Mean years of schooling | 8.89 | 0.18 | 10.11 | 0.02 | −1.22 | 0.18 |

**2023** — returnees n = 647 (weighted 202,515); non-migrants n = 208,155 (weighted 75,474,634)

| Band | Returnee % | SE | Non-migrant % | SE | Difference (pp) | SE |
|---|---:|---:|---:|---:|---:|---:|
| Less than lower secondary | 28.02 | 2.13 | 23.22 | 0.19 | +4.80 | 2.13 |
| Lower secondary | 32.25 | 2.31 | 26.03 | 0.16 | +6.22 | 2.31 |
| Upper secondary | 24.26 | 2.08 | 22.99 | 0.15 | +1.26 | 2.08 |
| Tertiary | 15.48 | 1.84 | 27.75 | 0.21 | −12.28 | 1.85 |
| Mean years of schooling | 9.56 | 0.20 | 10.59 | 0.02 | −1.03 | 0.20 |

Both groups gained schooling between the waves. The returnee gain is larger, which closes
the bottom-band excess by about half while leaving the tertiary deficit roughly where it
was; the two tertiary differences are within one standard error of each other, so the
change at the top is not resolved by these data.

### By sex

[DATA: derived/return_migrants_by_schooling.csv, slices `sex:men`, `sex:women`]

| Wave | Group | n | Mean-years difference | SE | Tertiary difference (pp) | SE |
|---|---|---:|---:|---:|---:|---:|
| 2018 | Men | 788 | −1.59 | 0.19 | −15.79 | 1.59 |
| 2018 | Women | 181 | −0.08 | 0.39 | −8.53 | 3.70 |
| 2023 | Men | 520 | −1.33 | 0.21 | −14.70 | 1.96 |
| 2023 | Women | 127 | +0.05 | 0.55 | −2.71 | 4.78 |

On mean years, women returnees are indistinguishable from non-migrant women in both waves.
The women's tertiary difference is negative in both waves but only clears twice its standard
error in 2018. Men carry the whole aggregate result. Women are 18.6 percent of the weighted
2018 returnee population and 17.7 percent of the 2023 one, so the pooled figure sits close
to the male one.

### By age band

[DATA: derived/return_migrants_by_schooling.csv, slices `age:*`] Differences, returnee minus
non-migrant. The full file also carries every sex-by-age cell.

| Wave | Age | n | Mean years | SE | Tertiary (pp) | SE |
|---|---|---:|---:|---:|---:|---:|
| 2018 | 20–29 | 155 | −0.84 | 0.33 | −11.92 | 4.31 |
| 2018 | 30–39 | 336 | −1.44 | 0.24 | −16.96 | 2.24 |
| 2018 | 40–49 | 292 | −1.40 | 0.32 | −11.89 | 2.55 |
| 2018 | 50–59 | 144 | −1.08 | 0.59 | −9.72 | 4.26 |
| 2018 | 60–64 | 42 | +0.29 | 0.67 | −7.22 | 4.87 |
| 2023 | 20–29 | 85 | −0.94 | 0.32 | −17.92 | 4.81 |
| 2023 | 30–39 | 196 | −0.91 | 0.36 | −13.13 | 3.31 |
| 2023 | 40–49 | 164 | −0.74 | 0.42 | −5.61 | 3.86 |
| 2023 | 50–59 | 139 | −1.10 | 0.36 | −11.81 | 2.79 |
| 2023 | 60–64 | 63 | −0.60 | 0.77 | −7.97 | 5.40 |

The tertiary deficit is negative in every age band of both waves. The oldest band is thin
and its mean-years estimate is not resolved.

## Departures to the United States, by return status

[DATA: derived/departures_by_schooling.csv] Weights are `fac_viv` for 2018 and `fac_hog`
for 2023, per the acquisition lane's mapping. Departure windows are August 2013 to the 2018
interview and August 2018 to the 2023 interview.

| Wave | Group | n | Weighted | Men % | SE | Mean age at departure | SE |
|---|---|---:|---:|---:|---:|---:|---:|
| 2018 | Returned | 778 | 220,218 | 74.01 | 2.01 | 33.31 | 0.72 |
| 2018 | Still abroad | 1,492 | 419,882 | 71.86 | 1.55 | 30.61 | 0.50 |
| 2018 | All US departures | 2,289 | 645,458 | 72.65 | 1.21 | 31.55 | 0.41 |
| 2023 | Returned | 679 | 215,021 | 84.66 | 1.59 | 35.89 | 0.68 |
| 2023 | Still abroad | 2,558 | 850,752 | 79.68 | 1.03 | 30.49 | 0.27 |
| 2023 | All US departures | 3,259 | 1,072,331 | 80.69 | 0.87 | 31.55 | 0.26 |

Returned and still-abroad do not sum to all: `cond_resid` is unspecified for the remainder.

Age at departure in INEGI's own grouping (`p4_8_ag2`), share within each group:

| Wave | Group | 0–17 | 18–29 | 30–59 | 60+ |
|---|---|---:|---:|---:|---:|
| 2018 | Returned | 5.48 ± 1.21 | 41.20 ± 2.32 | 46.89 ± 2.19 | 6.43 ± 1.13 |
| 2018 | Still abroad | 5.46 ± 0.87 | 52.27 ± 1.61 | 38.39 ± 1.46 | 3.89 ± 0.69 |
| 2023 | Returned | 4.16 ± 1.05 | 34.51 ± 2.17 | 52.93 ± 2.38 | 8.40 ± 1.38 |
| 2023 | Still abroad | 5.34 ± 0.54 | 50.40 ± 1.22 | 42.17 ± 1.22 | 2.09 ± 0.32 |

### Schooling of the departure cohort: not measurable, and why

`TMigrante` has no schooling variable in either wave. This was checked against the complete
data dictionary for each wave, all 55 fields in 2018 and 52 in 2023, not a keyword search
[DATA: enadid_2018_csv.zip and enadid_2023_csv.zip, `diccionario_de_datos/` members]. Per the
brief, that branch stops.

One partial route exists and is reported separately because it cannot answer the comparison.
Question P4.20 asks whether the departed person is now a household member and, if so, records
their row number, which links into `TSDem` and therefore to a schooling record. By
construction only returnees can link: 0 of the still-abroad rows link in either wave, against
91.8 percent of 2018 returnees and 91.3 percent of 2023 returnees. The linked distribution is
a second measurement of returnees, not of departures, and the file never presents it as one.

Restricted to the same universe as the resident table, Mexico-born and aged 20–64 at survey
(n = 602 in 2018, n = 528 in 2023):

| Band | 2018 % | SE | 2023 % | SE |
|---|---:|---:|---:|---:|
| Less than lower secondary | 26.81 | 2.19 | 22.16 | 2.32 |
| Lower secondary | 24.08 | 2.15 | 32.59 | 2.55 |
| Upper secondary | 20.98 | 1.90 | 22.67 | 2.23 |
| Tertiary | 28.13 | 2.46 | 22.58 | 2.34 |

Set against the resident-table returnees in the same wave, 11.18 ± 1.46 percent tertiary in
2018 and 15.48 ± 1.84 in 2023, these short-duration returnees are far better educated. In
2018 their tertiary share of 28.13 ± 2.46 also runs above the non-migrant population's
24.97 ± 0.19, though by only about 1.3 standard errors, so that particular ordering is not
resolved. The difference between the two returnee definitions is larger than the difference
between returnees and non-migrants.

## What this does and does not settle for the two assumptions

**Assumption 1: return migration is negatively selected on education.** Supported for the
endpoint definition, which is the one the lineage and lifetime work implicitly uses when it
treats attrition as a loss from the resident stock. The magnitude is roughly one year of
schooling and a 12-to-14-point tertiary deficit, and it is a male result. It is not supported
for short-duration circular migration, where selection runs the other way or is absent.
Anyone applying a single attrition parameter across both kinds of movement is applying the
wrong sign to one of them. [FRAMING-SENSITIVE]

**Assumption 2: rising education of recent Mexico-born arrivals in US surveys is not an
artefact of return selection.** ENADID cannot settle this, and the honest statement of what
it contributes is narrow. The direction is as the concern supposes: because departers who
come back are less educated than those who stay away, a US survey of people still present
will over-state the education of an arrival cohort relative to the cohort as it departed.
ENADID cannot size that bias, because the departure cohort's schooling is unmeasured. It
also cannot speak to a trend running from 1975, since it supplies two five-year windows
covering 2013–2018 and 2018–2023. Within those two windows the selection became *less*
negative at the bottom of the distribution, which pushes against, rather than for, an
artefact story over that span. The US-side arrival figures quoted in the brief
(less-than-high-school share among new Mexico-born arrivals falling from 82 to 33 percent
since 1975, BA+ rising from 3 to 22 percent) are carried here for orientation only and are
not recomputed or tested by this lane. [DATA: quoted from the repository's arrival-cohort
memo, not from ENADID]

## Limits

- **Household-reported departures miss whole-household moves.** `TMigrante` is reported by
  households still present in Mexico. A household that emigrated entirely is not represented,
  so the departure cohort is undercounted in a way that is plausibly correlated with
  education and family structure.
- **The two returnee populations are different objects.** `TSDem` returnees lived in the US
  at a fixed point five years before the interview and in Mexico at interview. `TMigrante`
  returnees departed *and* returned within the same five-year window. The tables above show
  they differ sharply. Neither is "the" return migrant.
- **Five-year windows, not annual flows.** 2013–2018 and 2018–2023. Nothing here supports an
  annual series, and the two windows are not a trend.
- **Schooling is measured at the survey, not at departure.** `TSDem` records the last level
  approved at interview. Schooling completed in the United States, or in Mexico after
  returning, is inside the measurement. There is no departure-time schooling variable in
  either table.
- **`TSDem` misses people who died, who moved again, or who are back in the US at
  interview,** and the prior-residence question does not cover children under five.
- **No US-side comparator is computed here.** The lane makes no use of ACS or any other US
  survey, and no figure in it is comparable to a US-stock or US-arrival distribution without
  further harmonisation of universe, age and timing.
- **No net migration.** Departures and returns are different objects on different clocks and
  are never subtracted. A test enforces that no output carries a net quantity.
- **Design.** 2023 contains 56 single-PSU strata, handled by the conservative centring option;
  the alternative changes the validated cell's SE in the sixth decimal place. Cells below
  roughly 150 unweighted cases, which includes the women-by-age cells and the 60–64 band,
  carry standard errors wide enough that only the sign is informative.
- **Instrument bias.** The measurement here is arithmetic on public microdata and is not
  subject to the model's dispositions in the way a synthesis would be; the framing of which
  comparison matters is not, and is flagged above [see notes/llm-bias-caveat.md].
