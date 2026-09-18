**Verdict:** India-born citizens vote at **parity** with US-born non-Hispanic whites (65.1% vs 64.7% pooled over five elections, raw LPM coefficient **0.0 ± 1.2 points**) and **above** all US-born citizens (60.7%) — but the parity is bought entirely by education and income: adjust for age, sex, education, family income and metro and the coefficient goes to **−10.3 ± 1.2**, and among BA-holders only they run **9.9 points below** comparable natives. On non-electoral civic life the first generation is well behind on *formal* participation (organisational membership 16.2% vs 32.0%, contacting an official 4.6% vs 12.5%) while being **above** natives on informal neighbourhood action (31.0% vs 22.8%). The second generation closes almost all of it. The binding constraint on India-born political weight is not willingness but **eligibility**: only 45.3% of India-born adults are citizens, and they naturalise later than any other group before ending higher than any other group (7.6% naturalised at 5–9 years since entry, 96.7% at 30+).

Both mandatory verifications **PASS**: the P20 gate reproduces the published 2020 turnout to −0.03 points with the weighted citizen population matching 231,593 thousand exactly, and `derived/` reproduces byte-identically on a second full run (12/12 `cmp OK`).

---

## Verification

**Required gate — PASS.** `derived/gate_2020_turnout.txt`:

```
  all citizens 18+      turnout lane 66.77%  published 66.8%  delta -0.03  PASS (tol 0.5)
                        registered   72.67%            72.7%        -0.03
                        weighted   231,593k         231,593k         -0k   (n=81,898)
  native-born citizens  turnout      67.38%            67.4%        -0.02  (n=75,746)
  naturalized citizens  turnout      60.82%            60.8%        +0.02  (n=6,152)
  native-born NH white  turnout      71.16%            71.2%        -0.04  (n=58,070)
```
[SOURCE: Census P20-585 Table 1 and Table 11, cached `_cache/p20_585_table01.xlsx`,
`_cache/p20_585_table11.xlsx`.] Four independent cells reproduce to within 0.05 points and every
weighted population matches the published thousand exactly. That validates the weight
(`PWSSWGT`), the universe (adult household members 18+), the citizenship recode and the
non-response convention simultaneously.

**Second gate, civic supplement.** `derived/gate_civic_rates.txt`, lane 18+ against the published
16+ national rates [SOURCE: AmeriCorps Open Data "2017-2023 CEV Findings", `data.americorps.gov/d/rhng-qtzw`,
cached `_cache/americorps_cev_national.csv`]: organisational membership matches to **0.0 points**
in all three years (27.1 / 23.8 / 24.9), contacting an official +0.2 / +0.3 / +0.2, charitable
giving +1.0 / +1.1 / +1.1, formal volunteering −2.7 / −2.1 / −3.1. The volunteering gap is the
16+/18+ universe difference (16–17-year-olds volunteer heavily through school); its constancy
across years is what a universe offset looks like, not a coding error.

**Reproducibility — PASS.** `bash scripts/verify.sh`: every script re-run from scratch, all twelve
files in `derived/` `cmp`-identical. Run twice (before and after the rank fix below), PASS both times.

**A real bug the verification caught.** The adjusted regressions were initially fit on a
rank-deficient design — when a restricted arm empties the reference education or income category,
the surviving dummies sum to the intercept. statsmodels pseudo-inverted it silently and returned
coefficients that were not uniquely determined; they moved by up to **4.2 points** (Mexico-born
adjusted turnout −13.5 → −10.0) once the reference category was chosen from categories actually
present. `scripts/regressions.py` now picks an occupied reference and **raises** if
`matrix_rank(X) < ncols`. All 20 specifications pass that guard. Every adjusted number below is
post-fix.

## Data

442,868 adult records across five November supplements (2016, 2018, 2020, 2022, 2024) and 140,761
across three September supplements (2019, 2021, 2023), all 51 states, pulled from
`api.census.gov`. Weighted rates with Kish design-effect SEs; cells under 50 unweighted
observations suppressed.

**Route deviations, all stated:**

1. **September 2017 is not on the API** (`2017/cps/volunteer/sep` → 404 while 2019/2021/2023 →
   200), so the civic series is 2019–2023, not the 2017–2023 the brief assumed.
2. **`PEINUSYR` (year of entry) does not exist in either supplement** — the API rejects it as an
   unknown variable and the public-use file carries only the allocation flag `PXINUSYR` (verified
   in `nov20pub.csv`'s 400-field header). So years-in-US is **not** a regression control and the
   "<10 years since arrival excluded" arm could not be built as written. Substitutes actually run:
   a naturalised-citizens-only arm, naturalisation share by birthplace and age band, and a
   years-since-entry table from the **CPS ASEC**, the one CPS instrument carrying `PEINUSYR`.
3. **Giving has no dollar threshold and no amount.** The pre-2017 instrument asked about
   donations of $25 or more; redesigned `PES18` is yes/no with no follow-up. Amounts cannot be
   reported and these rates are not comparable to pre-2017 published giving rates.
4. **SEs are a Kish approximation** (`n_eff=(Σw)²/Σw²`), which captures weight variation only and
   is a lower bound on the true SE. Replicate weights ship for September (`sep21nrrep.csv`,
   `sep23nrrep.csv`) but **not** for the November voting supplement. Quantifying the understatement
   from the 81 MB September replicate file was started and **abandoned** — the host was delivering
   ~1 MB/min under contention — and the brief permits a stated approximation.
5. **`api.census.gov` silently truncates large CPS responses**: HTTP 200 with the body cut
   mid-record, at 0.3–2.8 MB of a ~13 MB nationwide payload, under HTTP/2 *and* `--http1.1`, and
   California cut repeatedly even as a single-state request. `scripts/pull.sh` requests one state
   at a time with `PRTAGE=18:99`, asserts each body ends in `]]`, and falls back to four age-band
   sub-requests for a state that still fails. Without that check the analysis would have run on
   silently partial data.

---

## Draft memo section

### Indian-origin civic and electoral participation: parity on the ballot, a deficit in the institutions

**Frame.** This measures resident groups, not admission policy, and the comparison that carries
the weight is against same-age, same-education US-born non-Hispanic whites, not against an
absolute standard. Every turnout and civic number here is **self-reported** in a household
survey; the CPS is known to overstate turnout and the Census non-response convention interacts
with that [SOURCE: Hur & Achen, "Coding Voter Turnout Responses in the Current Population
Survey", *Public Opinion Quarterly* 2013, doi:10.1093/POQ/NFT042; Ansolabehere & Hersh,
"Validation: What Big Data Reveal About Survey Misreporting and the Real Electorate",
*Political Analysis* 2012, doi:10.1093/pan/mps023]. Whether over-reporting differs between
India-born and native-born respondents is **not** testable in this data and is the largest
unquantified threat to the turnout comparison [UNVERIFIED].

**Turnout is at parity, and the parity is real across conventions.** [CALCULATION: CPS November
supplements 2016–2024, citizens 18+, weight `PWSSWGT`, Census convention — item non-response
counted as not voting and kept in the denominator.]

| group | turnout % | SE | n |
|---|---|---|---|
| India-born | **65.1** | 1.21 | 1,748 |
| China-born | 42.5 | 1.43 | 1,364 |
| Mexico-born | 42.9 | 0.73 | 5,242 |
| other foreign-born | 53.6 | 0.36 | 23,476 |
| Indian 2nd gen (parent birthplace) | 57.0 | 1.89 | 833 |
| **US-born non-Hispanic white** | **64.7** | 0.10 | 290,492 |
| all US-born | 60.7 | 0.09 | 378,284 |
| Indian 2nd gen (self-ID, `PRDASIAN`) | 48.0 | 1.74 | 960 |
| US-born Asian, any origin | 45.4 | 0.64 | 8,238 |

Two checks say this is not a convention artefact. Item non-response to the vote question is
**14.0%** for the India-born against **13.9%** for US-born whites — indistinguishable — so the
Census coding rule does not fall differently on the two groups. Under the alternative convention
that drops non-response from the denominator the ranking is unchanged (India-born 75.7%,
US-born whites 75.1%). Registration is likewise at parity (75.2% vs 74.7%).

This is **not** a generic immigrant or generic Asian pattern. China-born citizens sit 22 points
below US-born whites and US-born Asians of any origin sit 19 points below. India-born
distinctiveness, not immigrant status, is doing the work.

**The parity is a presidential-year phenomenon.** [CALCULATION: same source, by election.]

| group | 2016 | 2018 | 2020 | 2022 | 2024 |
|---|---|---|---|---|---|
| India-born | 66.0 | 53.6 | **78.7** | 47.0 | **76.4** |
| US-born NH white | 65.6 | 57.8 | 71.2 | 58.0 | 70.8 |
| all US-born | 62.1 | 54.2 | 67.4 | 53.4 | 66.2 |

India-born citizens out-voted US-born whites by 7.5 points in 2020 and 5.6 in 2024, and
under-voted them by 4.2 in 2018 and 11.0 in 2022. Their presidential-to-midterm drop-off is
roughly 29 points against 13 for US-born whites. Per-year cells carry SEs near 2.7–2.9 points, so
the pattern is larger than sampling noise in every year. Read as high-salience-election
participation rather than habitual participation.

**Adjustment reverses the sign of the finding.** [CALCULATION: weighted LPM, HC1 robust SEs,
reference US-born non-Hispanic white, year fixed effects; adjusted adds age, age², sex, education
in six levels, family income in five brackets and metropolitan status. n=323,155. Measurement,
not model output, for the rates; model output for these coefficients. Years in the US is **not**
among the controls — see route deviation 2.]

| group | raw | adjusted |
|---|---|---|
| India-born | **0.0** (1.18) | **−10.3** (1.17) |
| China-born | −21.9 (1.42) | −23.3 (1.36) |
| Mexico-born | −21.7 (0.73) | −10.0 (0.73) |
| other foreign-born | −11.0 (0.37) | −12.0 (0.36) |
| Indian 2nd gen | −8.7 (1.88) | −4.8 (1.86) |

India-born and Mexico-born are mirror images. For the India-born, composition is the *whole*
of the parity: 79% of India-born citizens in this sample hold a BA against 37% of US-born whites,
and conditioning on that turns a zero into a 10-point deficit. For the Mexico-born, composition
*conceals* participation: conditioning halves their deficit from 21.7 to 10.0 points. Which of
these is the interesting number is a framing judgement, not a data question
[FRAMING-SENSITIVE]. The unconditional number answers "how much does this group vote"; the
conditional one answers "does this group vote like others with its resources". They point
opposite ways for the India-born and both are correctly computed.

**The disconfirmation arms.** [CALCULATION: `derived/voting_arms.csv`, turnout %, India-born vs
US-born NH white.]

| arm | India-born | US-born NH white | gap |
|---|---|---|---|
| citizens 18+ (headline) | 65.1 | 64.7 | +0.4 |
| **BA-holders only** | **68.0** | **77.6** | **−9.6** |
| age 25–54 | 63.1 | 61.3 | +1.8 |
| self-respondent only (no proxy) | 69.5 | 68.0 | +1.5 |
| **all adults incl. non-citizens** | **29.5** | **64.7** | **−35.2** |

The education-matched arm is the one that moves the headline, and it agrees with the regression:
matched on a BA, India-born citizens vote about ten points less than comparable natives. The
proxy-response and prime-age arms do not move it, which rules out two mundane explanations.
The all-adults arm is not a participation result — it is an eligibility result, and it is the
largest number on the page.

**Eligibility, not willingness, is the binding constraint.** Only **45.3%** of India-born adults
are US citizens, against 50.5% China-born, 58.1% other foreign-born and 32.8% Mexico-born
[CALCULATION: November supplements pooled, foreign-born 18+]. The ASEC, the only CPS instrument
carrying year of entry, shows why: the India-born naturalise later than anyone and then more
completely than anyone.

| years since entry | India-born | China-born | Mexico-born | other foreign-born |
|---|---|---|---|---|
| 0–4 | 3.8 | 4.2 | 10.4 | 8.2 |
| 5–9 | **7.6** | 14.3 | 15.2 | **24.7** |
| 10–19 | 38.1 | 31.8 | 21.7 | 62.2 |
| 20–29 | 81.9 | 69.0 | 23.9 | 70.4 |
| 30+ | **96.7** | 89.0 | 60.6 | 84.1 |

[CALCULATION: CPS ASEC 2024, weight `MARSUPWT`, foreign-born adults 18+; band midpoints parsed
from that year's own `PEINUSYR` value labels. ASEC 2025 reproduces the shape: 5.4 / 31.4 / 86.7 /
93.6.] A group whose median member is still years from a green card cannot register a
cross-sectional turnout rate; the employment-based backlog is a plausible mechanism for the
5–9-year trough but is **not tested here** [INFERENCE]. The 96.7% terminal rate is the number to
carry: conditional on time, India-born naturalisation is close to universal, and higher than for
any comparison group.

**Non-electoral civic life splits sharply between informal and formal.** [CALCULATION: CPS
September supplements 2019/2021/2023 pooled, adults 18+, weight `PWNRWGT`, respondents only.]

| measure | India-born | Indian 2nd gen | China-born | Mexico-born | other FB | US-born NH white |
|---|---|---|---|---|---|---|
| did something to improve the neighbourhood | **31.0** | 24.8 | 18.0 | 11.2 | 17.4 | **22.8** |
| donated to a non-political organisation | 51.1 | 55.7 | 37.0 | 30.2 | 41.5 | 57.8 |
| volunteered through an organisation | 21.5 | **33.7** | 16.1 | 8.8 | 15.7 | 29.8 |
| did favours for neighbours monthly+ | 35.8 | 30.5 | 22.6 | 30.0 | 26.1 | 40.4 |
| belongs to a group or association | **16.2** | 29.2 | 14.3 | 7.4 | 15.4 | **32.0** |
| contacted a public official | **4.6** | 10.4 | 3.2 | 1.7 | 3.8 | **12.5** |
| donated to a political organisation | 6.1 | 10.3 | 4.3 | 2.1 | 5.4 | 10.5 |

India-born adults are **8.2 points above** US-born whites on informal neighbourhood action and
**15.8 points below** on organisational membership, with official contact at roughly a third the
native rate. The gradient runs by formality, not by engagement. Volunteer hours point the same
way: India-born volunteers report a mean of 53.5 and median of 20 annual hours against 80.8 and
35 for US-born whites, so the shortfall is in both the rate and the intensity of *organised*
volunteering.

**The second generation converges, and the convergence is the least certain result here.**
Indian 2nd-generation adults volunteer at 33.7% against 29.8% for US-born whites, give at 55.7%
vs 57.8%, belong to organisations at 29.2% vs 32.0% and contact officials at 10.4% vs 12.5%.
Adjusted, the second-generation civic coefficients are −2.8, −1.3, −6.9 and −2.7 points, against
−19.4, −17.4, −26.2 and −12.9 for the first generation. On turnout under the reported-only
convention the adjusted second-generation coefficient is **−0.1 ± 1.9** — indistinguishable from
native parity.

Two reasons to hold this loosely. The cells are small (n=240–833). More seriously, the result is
**definition-sensitive**: defining the second generation by parent birthplace gives 57.0% pooled
turnout, while defining it by self-identified Asian Indian race among the native-born gives
**48.0%** — a nine-point spread, with item non-response of 21.4% vs 31.2%. The two definitions
capture different people (the self-ID group includes third-generation and mixed-parentage
Indians, and skews younger), and no evidence here adjudicates between them. Any second-generation
claim should carry that range rather than a point estimate [FRAMING-SENSITIVE].

**What would overturn this.** Validated-vote data showing India-born respondents over-report
turnout more than natives would eliminate the parity finding; the CPS cannot test it. A
years-since-naturalisation control — unavailable in any CPS instrument — would separate "recently
naturalised" from "India-born" in the adjusted deficit, and given the naturalisation timing above
it plausibly accounts for a substantial share of the −10.3.

---

## Files

Outputs in `derived/`: `gate_2020_turnout.txt`, `gate_civic_rates.txt`, `voting_rates.csv`,
`voting_arms.csv`, `naturalization.csv`, `asec_naturalization_by_entry.csv`,
`volunteer_rates.csv`, `volunteer_arms.csv`, `volunteer_hours.csv`, `regression_turnout.csv`,
`regression_civic.csv`, `summary.txt` (a digest of all of the above).

Scripts in `scripts/`: `pull.sh`, `fetch.sh`, `common.py`, `analyze_voting.py`,
`analyze_volunteer.py`, `asec_entry.py`, `regressions.py`, `summary.py`, `verify.sh`.
Run commands and measurement notes in `README.md`.

**Covered:** all five November supplements 2016–2024 and all three September supplements
2019–2023, 51 states each; the ASEC years-since-entry arm for 2024 and 2025.
**Skipped and why:** September 2017 (not served by the API, 404); year-of-entry controls and the
recent-arrival exclusion arm (`PEINUSYR` absent from both supplements); replicate-weight SEs
(abandoned on download throughput, approximation stated); giving amounts (not collected
post-2017). Nothing under `research/` was touched and nothing was committed.
