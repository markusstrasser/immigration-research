# Admission route against origin religion: result

Model self-report: claude-fable-5-1. 2026-09-21. Design fixed in [`README.md`](README.md) (commit
6df195d) before the route shares were downloaded.

**Verdict:** By the pre-specified decision rule the test is **not settled**: neither "route
accounts for it" nor "an origin-religion penalty persists" is met. The parts are clearer than the
rule. Across 66 birthplaces, among degree holders aged 25–64 who entered since 2000, the share
admitted through employment is the strongest predictor of how a degree converts: an origin at
50% employment-route against one at 10% has about 29 points more degree holders earning $100,000
or more (coefficient +73.6, 95% interval +54.5 to +92.7) and about 11 points fewer on Medicaid
(−28.7, −40.8 to −16.6). The Muslim share of the origin country carries **no earnings penalty**
among degree holders, raw (−1.8, −8.7 to +5.1) or at equal route mix (+2.7, −2.2 to +7.6). Its
raw Medicaid difference among degree holders (+8.7, +1.0 to +16.5) falls by 45% at equal route
mix and can no longer be told from zero (+4.8, −4.5 to +14.2). One difference does not move with
route: employment at ages 25–64 is 6 points lower (−6.1, −11.4 to −0.8), and an exploratory split
shows it is entirely women (−17.1, −26.2 to −8.0; men +1.9, −2.1 to +6.0).
[CALCULATION: `derived/route_models.csv`, `derived/route_verdict.json`]

## Muslim share of origin country: coefficient by model

Percentage points, an origin at 100% Muslim against one at 0%; OLS, HC3, one observation per
birthplace, n = 66 (model 3: 59). Model 1: Muslim share only. Model 2: adds employment,
refugee/asylee and diversity shares (family and other omitted), and the birthplace's degree share
for S and X outcomes. Model 3: model 2 without Mexico and Central America.

| Outcome | Model 1 | Model 2 | Model 3 |
|---|---|---|---|
| P1 Medicaid, degree holders 25–64 | +8.7 (+1.0, +16.5) | +4.8 (−4.5, +14.2) | +4.9 (−4.4, +14.2) |
| P2 income ≥ $100k, degree holders 25–64 | −1.8 (−8.7, +5.1) | +2.7 (−2.2, +7.6) | +1.9 (−3.1, +6.8) |
| S1 Medicaid, all | +16.9 (+5.0, +28.9) | +12.1 (−1.5, +25.7) | +11.9 (−1.7, +25.6) |
| S2 poverty | +6.5 (−0.9, +13.9) | +7.8 (−0.2, +15.9) | +7.4 (−1.2, +16.1) |
| S3 employed 25–64 | −6.1 (−10.7, −1.5) | −6.1 (−11.4, −0.8) | −6.3 (−11.8, −0.7) |
| X employed men 25–64 (exploratory) | −0.3 (−3.5, +2.8) | +1.9 (−2.1, +6.0) | +1.4 (−2.9, +5.6) |
| X employed women 25–64 (exploratory) | −13.2 (−21.3, −5.1) | −17.1 (−26.2, −8.0) | −16.6 (−26.5, −6.8) |

Route coefficients in model 2 (family and other omitted): for P2, employment +73.6 (+54.5,
+92.7), diversity +28.6 (+11.6, +45.6), refugee/asylee +2.6 (−9.1, +14.2); for P1, employment
−28.7 (−40.8, −16.6), refugee/asylee +0.7 (−11.4, +12.8), diversity +14.9 (−25.8, +55.7).

## Selected birthplaces (entered 2000 or later)

| Birthplace | Origin Muslim share | Employment route | Degree share 25–64 | Degree holders ≥ $100k | Degree holders on Medicaid | Men employed | Women employed |
|---|---:|---:|---:|---:|---:|---:|---:|
| India | 14% | 49% | 88% | 53% | 3% | 94% | 69% |
| United Kingdom | 5% | 44% | 68% | 56% | 3% | 87% | 74% |
| Korea | 0% | 57% | 76% | 34% | 7% | 87% | 64% |
| China | 2% | 27% | 61% | 43% | 6% | 86% | 74% |
| Iran | 100% | 15% | 69% | 40% | 10% | 88% | 70% |
| Turkey | 98% | 27% | 71% | 36% | 6% | 91% | 59% |
| Egypt | 95% | 9% | 69% | 28% | 21% | 87% | 63% |
| Pakistan | 96% | 18% | 64% | 28% | 12% | 86% | 54% |
| Bangladesh | 90% | 8% | 50% | 20% | 23% | 88% | 52% |
| Nigeria | 49% | 10% | 69% | 25% | 9% | 87% | 80% |
| Philippines | 6% | 21% | 58% | 25% | 7% | 86% | 80% |
| Venezuela | 0% | 24% | 48% | 12% | 8% | 86% | 72% |
| Iraq | 99% | 3% | 35% | 26% | 21% | 82% | 50% |
| Afghanistan | 100% | 1% | 30% | 17% | 42% | 87% | 37% |
| Mexico | 0% | 6% | 13% | 19% | 9% | 89% | 57% |

[DATA: `derived/route_units.csv`; routes `derived/lpr_class_mix.csv` from DHS Yearbook Table 10,
FY2005–2023, country rows reconciled to each year's published total; Muslim share Pew 2010]

## Deviations from the design, and what was added afterwards

- FY2004 is left out: that yearbook's table has a different layout and class split. Nineteen of
  the twenty named years are pooled.
- One unit dropped: "Africa" (unspecified) has no DHS or Pew row. UK components are merged.
- The employment-by-sex rows (X) were added after the pre-specified run showed S3 not moving
  with route. They are exploratory and sit outside the decision rule.

## Reading, with its limits

- The origin differences in how a degree converts go mostly with how people were admitted. That
  is the policy-relevant finding: the law sets routes. It is an association across 66 birthplaces;
  the employment route selects on a job offer, so part of it is selection by construction.
- A Muslim-majority origin predicts neither lower earnings among degree holders nor, once route
  is held equal, distinguishable extra Medicaid use. It predicts lower employment of women by 13–17
  points, which route, refugee share and education do not explain, and which lowers household
  taxes and raises means-tested eligibility [INFERENCE]. Mexico-born women (57%) sit in the same
  range, so the pattern is not specific to Muslim-majority origins.
- Ecological. The Muslim share describes the origin country, not the residents: Iran-, Egypt- and
  Nigeria-born residents of the US include large non-Muslim shares [TRAINING-DATA]. Green-card
  flows leave out temporary workers and students (so India's and China's employment route is
  understated) and unauthorized residents. Afghan and Iraqi special immigrant visas sit under
  "other", which the models omit with family.
- P1 partly measures eligibility rules (refugees qualify on arrival). P2 does not.
- Intervals are HC3 on 66 points with a few influential origins. The population-weighted check
  (in `route_models.csv`, not used for the rule) agrees in sign and size: employment route +73.9
  (+49.4, +98.4) for P2; Muslim share +6.5 (−0.0, +13.1) for P2, +6.9 (−3.0, +16.8) for P1,
  −21.8 (−30.4, −13.2) for women's employment. It differs on poverty, where the weighted
  coefficient excludes zero (+9.2, +1.0 to +17.4).

[INSTRUMENT] LLM-conducted on a charged topic; the design was fixed before the predictors were
seen so that the reading could not be tuned. See `notes/llm-bias-caveat.md`.
