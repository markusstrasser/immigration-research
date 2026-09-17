# Disability & disability income by generation — CPS ASEC 2025

**September 17 multiyear extension:** [ASEC 2024–26 execution](../frontier_execution_2026_09_17/social/RESULT.md) gives standardized disability prevalence 5.07%/8.42%/11.15% for Mexico-born/G2/G3+ self-ID. G2−Mexico-born is +3.35 pp [1.47, 5.23] with conservative cross-year covariance treatment. Neither descendant group establishes excess over the white reference. G2 Social Security with disability reason plus SSI averages $701 versus $767 for whites; private payments remain separate. No causal or administrative-expenditure claim is made.

**Superseded interpretation, 2026-09-17:** [audit §4](../../../research/immigration-new-conclusions-audit-2026-09-17.md) reproduces the rates and direct first-to-second contrast but withdraws “first-generation only,” established parity/reversal, and a CPS-derived upper bound on the true advantage. Second-generation disability-income dollars are $942 versus $1,030 for whites; the aggregate includes private payments. Original text below is preserved; consult the audit's intervals and narrower current claim.

**Verdict:** The first-generation disability advantage is a **first-generation** phenomenon
only. Age-standardised to the third-plus non-Hispanic white age distribution, disability
prevalence for adults 25–64 runs **4.5% (Mexico-born) → 8.6% (Mexican 2nd gen) → 11.3%
(Mexican 3rd+ self-ID) → 9.8% (third-plus NH white)**. The 54% first-generation advantage
is gone by the second generation (−1.2 pts, 1.4 se, not significant) and the point estimate
*reverses* by the third (+1.5 pts, 1.6 se, not significant). Disability-income receipt does
the same thing and overshoots: SSI receipt is *above* the white reference in both US-born
Mexican-origin generations (3rd+: +1.21 pts, t = 2.05). **Bier's pooled prevalence gate
FAILS on CPS for the foreign-born by 3.4 points** — CPS gives 7.7% vs his ACS 11.1%, so the
CPS instrument produces a far larger immigrant advantage than ACS does.

Model self-report: Opus 5 (1M context), model ID `claude-opus-5[1m]`.

Source: `gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip` (`pppub25.csv`, income year
2024, 142,125 persons) + `asec_csv_repwgt_2025.csv`. Generation coding copied from
`build/analyze_cps_fiscal_2025.py` (PENATVTY/PEFNTVTY/PEMNTVTY, 303 = Mexico, US-area
57/60/66/69/73/78). Full 160-replicate SDR standard errors reused, not approximated:
`se = sqrt(4/160 · Σ(est_i − est_0)²)`. Script `disability_by_generation.py`; outputs
`disability_by_generation.csv` (292 rows) and `disability_differences.csv`.
Adults 25–64, `PRPERTYP = 2`, in the `PRDISFLG` universe. Weight `MARSUPWT/100` (= `pwwgt0`,
validated to < 0.01).

[SOURCE: https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asecpub25csv.zip]

---

## 1. Gate: Bier's pooled foreign-born vs US-born prevalence — FAILS by 3.4 points

Bier (Cato/Nowrasteh Substack, 27 Aug 2026) reports **11.1% foreign-born vs 14.6% US-born**
from ACS 2024, a 24% relative advantage. CPS ASEC 2025, same `PRDISFLG`-style measure:

| Denominator | Foreign-born | US-born | Relative advantage |
|---|---|---|---|
| CPS, persons 15+ (the `PRDISFLG` universe) | 7.68% (se 0.22) | 13.75% (se 0.17) | **−44%** |
| CPS, all ages, under-15 counted as non-disabled | 7.29% | 10.96% | −33% |
| Bier, ACS 2024, all ages | 11.1% | 14.6% | −24% |

n = 20,622 foreign-born and 93,348 US-born in the 15+ universe.

The US-born figure matches within the brief's 1-point tolerance on the 15+ arm (13.75 vs
14.6, 0.85 points low). **The foreign-born figure does not: 7.68% against 11.1% is 3.4
points low, and the relative advantage nearly doubles (44% vs 24%).** CPS does not publish
disability for persons under 15 at all, so no denominator choice fixes this; forcing an
all-ages denominator makes both figures worse. The gap is an instrument difference, not an
age-composition difference — ACS and CPS ask the same six functional-limitation items, but
ACS asks them of all ages by mail and internet self-response, while CPS ASEC is
interviewer-administered with heavy household-proxy reporting, and proxy reporting for
foreign-language households plausibly under-reports functional limitation. **Everything
below is therefore a CPS-internal comparison; the absolute levels are not interchangeable
with Bier's ACS levels, and the first-generation advantage measured here is an upper bound
on the true one.** [INFERENCE: the proxy-reporting explanation is not tested here]

---

## 2. Disability prevalence by generation, adults 25–64

Age-standardised to the third-plus NH white age distribution (8 five-year bands, 25–29 …
60–64), SDR se in parentheses. Crude rates shown for contrast because the second generation
is nine years younger on average (37.9 vs 44.9) and the crude figures are badly misleading.

| | 3rd+ NH white | Mexican 2nd gen | Mexican 3rd+ (self-ID) | Mexico-born | All foreign-born | All 2nd gen |
|---|---|---|---|---|---|---|
| **n (unweighted)** | 36,287 | 2,452 | 2,477 | 4,318 | 15,203 | 6,871 |
| Any disability, **crude** | 9.82% (0.23) | 6.27% (0.52) | 9.42% (0.78) | 4.27% (0.36) | 4.05% (0.18) | 6.90% (0.37) |
| Any disability, **age-std** | 9.82% (0.23) | **8.61% (0.85)** | **11.27% (0.91)** | **4.49% (0.38)** | 4.44% (0.20) | 8.20% (0.46) |
| Difference vs white (age-std) | — | −1.20 (0.86), t = −1.41 | +1.45 (0.91), t = +1.59 | −5.32 (0.42), t = −12.7 | −5.38 (0.26) | −1.62 (0.49), t = −3.31 |
| Health problem prevents work (`DIS_HP`), age-std | 9.46% (0.20) | 9.87% (0.98) | 10.31% (0.93) | 5.89% (0.39) | 5.29% (0.23) | 8.85% (0.46) |

The six ACS-style functional items separately (age-standardised, adults 25–64):

| Item | 3rd+ NH white | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|---|
| Hearing (`PEDISEAR`) | 2.15% | 1.49% | 2.58% | 0.80% |
| Vision (`PEDISEYE`) | 1.32% | 1.28% | 2.23% | 1.24% |
| Cognitive (`PEDISREM`) | 4.36% | 3.15% | 4.74% | 1.03% |
| Ambulatory (`PEDISPHY`) | 4.40% | 4.16% | 6.02% | 2.01% |
| Self-care (`PEDISDRS`) | 1.44% | 1.69% | 2.35% | 0.86% |
| Independent living (`PEDISOUT`) | 3.16% | 3.78% | 3.86% | 1.40% |

The pattern is the same item by item. The Mexico-born are below the white reference on all
six, by a factor of 2 to 4; the Mexican 2nd generation is at or near parity on four of six
(self-care and independent living are already *above*); the Mexican 3rd+ is above white on
five of six. Cognitive and hearing are the two items where the 2nd generation stays clearly
below, and they are also the two items most exposed to proxy under-reporting.

No cell is under 100 unweighted; the smallest is the disabled Mexican-2nd-generation cell at
n = 148 (Section 4).

---

## 3. Disability-income receipt and dollars, adults 25–64

SSDI is identified as `SS_YN = 1` with `RESNSS1` or `RESNSS2 = 2`. The reason code was
validated empirically, not assumed: among Social Security recipients aged 25–54, code 2 is
826 of 1,294 cases while code 1 is 265; among recipients 67+, code 1 is 17,694 and code 2 is
532; and among 25–64 recipients with code 2, 58% carry `PRDISFLG = 1` against 24% for code
1. Code 1 = retirement, code 2 = disability. [INFERENCE: codebook not on disk; inference
rests on the three cross-tabs above]
Other disability income is `DIS_YN = 1` with `DIS_VAL1 + DIS_VAL2` (workers' comp, company
or union disability, federal/state/local government disability, VA, accident insurance).
SSI at 25–64 is disability- or blindness-based by program rule (the aged category starts at
65).

Age-standardised to the white age distribution, adults 25–64:

| | 3rd+ NH white | Mexican 2nd gen | Mexican 3rd+ | Mexico-born | All foreign-born |
|---|---|---|---|---|---|
| SSDI receipt | 3.20% (0.13) | 3.37% (0.69) | 3.37% (0.50) | 1.36% (0.23) | 1.23% (0.12) |
| SSI receipt | 1.99% (0.09) | 2.98% (0.68) | **3.20% (0.59)** | 0.86% (0.16) | 0.98% (0.10) |
| Other disability income | 1.42% (0.08) | 1.38% (0.39) | 1.64% (0.42) | 0.77% (0.17) | 0.73% (0.08) |
| **Any disability income** | 5.77% (0.17) | 6.70% (0.91) | 6.57% (0.74) | 2.82% (0.32) | 2.68% (0.16) |
| SSDI $/adult | 570 (27) | 505 (107) | 579 (104) | 214 (38) | 218 (23) |
| SSI $/adult | 229 (12) | 334 (80) | 358 (73) | 92 (19) | 109 (12) |
| Other disability $/adult | 231 (18) | 104 (30) | 214 (66) | 99 (28) | 97 (20) |
| **All disability $/adult** | **1,030 (35)** | **942 (141)** | **1,151 (159)** | **404 (53)** | 424 (32) |

Differences from the white reference (age-standardised, t = difference / SDR se):

| | Mexican 2nd gen | Mexican 3rd+ | Mexico-born |
|---|---|---|---|
| Any disability income | +0.93 pt, t = +1.03 | +0.79 pt, t = +1.05 | −2.95 pt, t = −7.95 |
| SSI receipt | +0.99 pt, t = +1.48 | **+1.21 pt, t = +2.05** | −1.13 pt, t = −6.03 |
| SSDI receipt | +0.17 pt, t = +0.25 | +0.17 pt, t = +0.33 | −1.84 pt, t = −6.68 |
| All disability $/adult | −$87, t = −0.60 | +$121, t = +0.77 | −$625, t = −9.46 |

Every first-generation line is a large, highly significant deficit. **Not one US-born
Mexican-origin line is significantly below the white reference, and SSI in the third
generation is significantly above it.** On crude (unstandardised) rates the second
generation still looks advantaged on every line (all disability dollars −$429, t = −4.66),
which is pure age composition: standardising removes the entire apparent advantage.

**Cross-check against the existing ledger.** The brief asked for the ledger's SSI line. The
extended-ledger CSV in `gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv`
carries no SSI or disability metric — it holds only the balance, tax, sales, property and
K-12 rows. The SSI line lives in `cps_generation_welfare_2026_09_16/mexican_origin_result_2025.txt`,
which gives crude `ssi%` of 0.9 / 2.0 / 2.6 / 2.0 for Mexico-born / Mexican 2nd gen /
Mexican 3rd+ / gen3+ NH white. This lane's independent crude figures are 0.86 / 2.04 / 2.59
/ 1.99 — an exact reproduction on a separately written estimator. (Adult n differs by ~8 per
cell because this lane additionally requires membership in the `PRDISFLG` universe.)

---

## 4. Conditional on being disabled: who claims

Share of *disabled* adults 25–64 receiving any disability income, crude (age-standardising a
cell of 148 is not defensible):

| | 3rd+ NH white | Mexican 2nd gen | Mexican 3rd+ | Mexico-born | All foreign-born |
|---|---|---|---|---|---|
| n (disabled, unweighted) | 3,322 | **148** | 238 | 197 | 602 |
| Any disability income | 32.8% (1.1) | 34.6% (4.7) | 34.6% (4.1) | **20.0% (3.4)** | 24.6% (2.0) |
| SSDI | 19.8% (0.9) | 14.3% (3.2) | 16.6% (2.8) | 12.8% (2.9) | 13.5% (1.7) |
| SSI | 12.5% (0.7) | 18.6% (4.3) | **21.2% (4.2)** | 6.0% (1.7) | 10.9% (1.7) |
| All disability $/disabled adult | 6,092 (232) | 4,333 (688) | 6,030 (1,018) | 3,666 (751) | 4,393 (458) |

Difference vs white: Mexico-born −12.7 pts (t = −3.61), all foreign-born −8.1 pts
(t = −3.60), Mexican 2nd gen +1.8 pts (t = 0.38), Mexican 3rd+ +1.8 pts (t = 0.44). SSI
given disabled, Mexican 3rd+ +8.6 pts (t = 2.07).

This reproduces Bier's second claim — disabled immigrants draw less disability income — and
localises it entirely to the first generation. A disabled Mexico-born adult is a third less
likely to be drawing anything than a disabled white adult, and half as likely on SSI
(eligibility rules are part of this: SSDI needs an insured work history and SSI is barred to
most non-citizens without qualifying status, so this cell mixes behaviour with statutory
ineligibility, which the prevalence result does not). By the second generation the claiming
rate is at parity, and the composition has shifted from SSDI toward SSI: the white reference
draws 60% of its claims through SSDI, the Mexican 3rd+ generation 48%, with SSI taking up
the difference. **The n = 148 cell carries a ±9-point 95% interval and cannot distinguish
parity from a 5-point gap in either direction.**

---

## 5. What the generation cut shows

**The first-generation health advantage does not survive into the second generation, let
alone the third.** The age-standardised gradient 4.5% → 8.6% → 11.3% against a white
reference of 9.8% is monotone convergence that passes the reference and keeps going. The
first-to-second-generation step is the large one (+4.1 points, 4.4 se of the second-generation
estimate); the second-to-third step is +2.7 points. Neither US-born generation differs from
the white reference at conventional significance, which is the finding: **on disability, the
US-born Mexican-origin population is an ordinary American population, not a healthy-immigrant
one, and the selection effect that makes the first generation look extraordinary is spent in
one generation.**

This is what the Hispanic-health-paradox literature predicts. Riosmena, Kuhn & Jochem (2017,
*Demography* 54:175–200, "Explaining the Immigrant Health Advantage") decompose the advantage
into health selection at migration plus the protective effect of origin-country health
behaviours, and find both erode with US duration and across generations; Hamilton & Hummer's
work on Black and Hispanic immigrant health finds the same duration and generation gradient.
The mechanism the literature names is acculturation to US diet, obesity and smoking patterns
combined with the loss of migration-stage selection, against a socioeconomic position that
does not converge as fast as the health behaviours do.
[TRAINING-DATA: both citations are from training knowledge; neither was fetched or verified
in this lane, and the exact page and volume numbers for Hamilton & Hummer are not asserted]

Three things sharpen the fiscal reading:

1. **The disability-income line is not where the Mexican second generation costs money.**
   All disability dollars per adult run $942 for the Mexican 2nd generation against $1,030 for
   the white reference, age-standardised, a difference of −$87 with se $141. Against §12's
   extended balance gap of −$8,286 per adult-year, the disability channel contributes nothing
   and if anything runs the wrong way for the restrictionist reading. **The gap remains a tax
   gap, not a transfer gap** — which is the same conclusion §12 reached on the under-reporting
   arm, reached here on a variable that arm did not touch.

2. **The composition shift toward SSI matters more than the level.** SSI is a means-tested
   federal cash program with no work-history requirement; SSDI is earned insurance. Both
   US-born Mexican-origin generations draw more SSI than whites and no more SSDI, and the
   third-generation SSI excess clears t = 2. That is consistent with the lower-earnings,
   shorter-covered-quarters profile documented in §5 of the by-generation memo, and it is the
   shape the first generation would eventually take on if statutory eligibility were not
   binding.

3. **Bier's headline is true and about a different population than the one the repo's
   question asks about.** He measures the stock of foreign-born adults now living in the US;
   the repo asks what the ledger looks like once those adults' children and grandchildren are
   the relevant population. On CPS, the foreign-born advantage (−5.4 points age-standardised,
   t = −20) is real and larger than what he reports from ACS; by the second generation it is
   −1.2 points with t = −1.4, and by the third it is +1.5 points. Projecting the first-
   generation advantage forward is the same descendant-convergence assumption §12 rejects for
   the fiscal line, and it fails here in the same direction.

---

## 6. Limitations

[UNVERIFIED]

- **The gate failed.** CPS foreign-born disability prevalence is 3.4 points below Bier's ACS
  figure and the relative advantage is nearly double. If ACS is the better instrument, the
  first-generation column in every table above is too low and the convergence measured across
  generations is too steep. Re-running §2 on ACS 2024 PUMS would settle it, but ACS has no
  parental birthplace, so the generation cut is not available there at all — that is the same
  constraint the memo's institutional-care line hit.
- **Ethnic attrition biases the third generation upward.** Third-plus Mexican origin here is
  self-identification (`PRDTHSP = 1`) among natives with two US-born parents. Duncan & Trejo
  show that intermarriage and upward mobility both reduce Mexican self-identification in later
  generations, so the self-identified third-plus cell is negatively selected on socioeconomic
  status and therefore, almost certainly, on health. **Some unknown part of the +1.45-point
  third-generation excess is attrition, not deterioration**, and the convergence story does
  not need the third-generation reversal to hold — the second-generation result carries it.
  [TRAINING-DATA: Duncan & Trejo; not re-verified in this lane]
- **Proxy reporting.** CPS ASEC collects one respondent's answers for the whole household.
  Disability under-reporting by proxy is plausibly larger in Spanish-speaking and
  foreign-born households, which would inflate the measured first-generation advantage and,
  to a lesser degree, the second-generation one. Not tested here.
- **The disabled-adult cells are small.** n = 148 (Mexican 2nd gen), 197 (Mexico-born), 238
  (Mexican 3rd+). All clear the 100 threshold, none supports age standardisation, and Section
  4's parity findings are consistent with modest differences in either direction.
- **The SSDI reason code is inferred**, not read from a codebook (Section 3). Misassignment
  would move SSDI and "any disability income" together and affect all groups alike.
- **Statutory ineligibility is not separated from non-claiming** in Section 4's
  first-generation cell; non-citizen SSI restrictions and SSDI's insured-status requirement
  are part of that −12.7-point difference.
- Institutionalised adults are outside the CPS universe entirely, and disability is
  concentrated in institutions, so every cell here understates prevalence. The direction of
  the bias by group is unknown but unlikely to be neutral.
