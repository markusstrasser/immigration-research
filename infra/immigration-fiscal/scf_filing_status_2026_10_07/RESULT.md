claude-opus-5-5

**Verdict:** On married couples filing jointly, the SCF's Hispanic/white income-tax ratio matches Treasury's tax-record ratio: **0.329** (SCF 2022, taxcalc under 2023 law, Hispanic = respondent answers yes to X7004) against OTA's **0.331** ($9,477 / $28,664, TY2023). The SCF does not tilt toward Hispanic couples the way the account's CPS model does (CPS 0.48). Its levels run about 1.55× Treasury for both groups ($14,614 Hispanic, $44,388 white). That is a common scale factor: the SCF reaches the top tail better than OTA's microsimulation sample, and my tax inputs are approximate. It is not a Hispanic-specific bias. On TPC's race definition (X6809 = 3, Hispanic picked as the first race) the ratio is 0.214. Treasury's Hispanic level ($9,505 vs $9,477) is matched only by coincidence, because white couples are still 1.55× too high on that definition. The sample is thin: n = 310 Hispanic and 1,594 white joint-filing households per implicate. [CALCULATION: `scf_joint.py` → `derived/scf_vs_ota.csv`] [INFERENCE]

## What was compared

- Universe: SCF 2022 households that filed or expect to file a 2021 federal return (X5744 ∈ {1, 6}) jointly (X5746 = 1). Variable numbers come from the codebook text (`codebk2022.txt`, X5744/X5746 near line 31610, X7004/X6809 near line 32061). [DATA: `sources/immigration-fiscal/data/external/stage3/frb/scf2022/`]
- Groups: Hispanic = X7004 = 1, any race. This is the closest match to OTA's Hispanic primary filer. TPC variant = X6809 = 3 (Gale, Hall & Sabelhaus code respondents this way). White = X6809 = 1 and X7004 = 5. Each is the designated respondent's answer.
- Estimation: each statistic is computed within each of the 5 implicates with X42001 and then averaged across them. Pooled counts use X42001/5.
- Tax: Tax-Calculator, 2023 law, MFJ. Inputs are the 2021 SCF family income components X5702–X5724, scaled by the SSA AWI ratio 66,621.80/60,575.07. Social Security and pensions (X5722) are coded as Social Security at age ≥ 62 and as taxable pensions below 62. Children for the CTC and EITC = summary-extract KIDS. Comparator: OTA WP-124 Table 3 Total rows [SOURCE: https://home.treasury.gov/system/files/131/WP-124.pdf, local `external_benchmarks_2026_09_24/_cache/arm2/WP-124.txt` lines 735, 825].

| Joint filers (SCF 2022, 2023 $) | n / implicate | units (M) | mean income | median income | mean tax | median tax |
|---|---:|---:|---:|---:|---:|---:|
| Hispanic (X7004) | 310 | 6.7 | 131,970 | 94,805 | 14,614 | 3,851 |
| Hispanic (TPC, X6809=3) | 258 | 5.8 | 113,856 | 89,965 | 9,505 | 2,997 |
| White non-Hispanic | 1,594 | 42.2 | 239,293 | 120,540 | 44,388 | 7,721 |
| All joint | 2,253 | 55.4 | 223,604 | 116,801 | 40,113 | 7,202 |

[DATA: `derived/scf_joint_filers.csv`]. Ratios are in `derived/scf_vs_ota.csv`. The Hispanic/white mean-income ratio is 0.552 and the median ratio 0.786.

| Ratio of mean tax, Hispanic / white | Value |
|---|---:|
| SCF, X7004 definition | 0.329 |
| SCF, TPC definition | 0.214 |
| OTA tax records (BIFSG-imputed) | 0.331 |
| Account's CPS model (benchmark lane arm 2) | 0.477 |

## Implication for FAQ 17

The SCF's survey-based Hispanic ratio agrees with Treasury. Survey data in general are not the problem. The CPS model's 0.48 has two sources: CPS top-coding cuts white incomes (audit row 3), and the CPS overstates Hispanic couples by about 11% (audit rows 2 and 13). The SCF fixes the first through its list-sample oversample of the wealthy. [INFERENCE]

## Limits

- Sample size: 310 Hispanic joint households per implicate. The implicate SD of the Hispanic mean tax is $381, but that is imputation variance only. I did not run the 999 replicate weights, so the true SE is larger, probably ±10–15% on the Hispanic mean [UNVERIFIED].
- The wealthy oversample drives the white mean, and the mean the ratio rests on. Medians are far apart from means.
- Tax-calc inputs are approximate. The unit is the SCF primary economic unit, not the tax unit. Children are counted at any age with KIDS, so CTC eligibility is overstated. All capital gains are treated as long term. The Social Security/pension split is by age. The 1.55× level gap mixes coverage and these approximations.
- Race is self-reported by the designated respondent (who can be the spouse, X8000). OTA imputes the primary filer's race by BIFSG. The definitions differ, and the SCF ratio is sensitive to them (0.33 vs 0.21).
- OTA publishes no counts or AGI distribution by race in Table 3, so no unit-count comparison is made.

## Reproduce

```sh
uv run --no-project --with taxcalc python3 infra/immigration-fiscal/scf_filing_status_2026_10_07/scf_joint.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/scf_filing_status_2026_10_07 "uv run --no-project --with taxcalc python3 {lane}/scf_joint.py"
```

Inputs: `sources/immigration-fiscal/data/external/stage3/frb/scf2022/ACQUIRED.md` (scf2022s.zip, scfp2022s.zip, codebk2022.txt with sha256).

## Log

- Wed Oct 7 10:43:21 JST 2026: downloaded and hashed the SCF 2022 Stata files and the codebook.
- Wed Oct 7 10:44:48 JST 2026: first run of `scf_joint.py`.
- Wed Oct 7 10:46:14 JST 2026: wrote RESULT; rerun check follows.
- Wed Oct 7 10:46:41 JST 2026: rerun_lane.py ran 1/1 rc=0 and reported IDENTICAL: 4/4.
