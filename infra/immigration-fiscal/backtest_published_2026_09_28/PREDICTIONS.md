claude-opus-5-5

# Frozen predictions: three published figures from the adopted account (Phase 1)

Written 2026-09-28, before any target figure was opened. `predict.py` builds every number below from the
adopted September 27 account's frame (CPS ASEC 2025, income year 2024) and keys. It imports the
account's builders and gates every key it uses against `model.json` to 1e-9: 430 receipt cells and
178 spending cells, the Mexico-born shares under convention (b), and the group's share of uninsured
person-years. Two runs of `scripts/rerun_lane.py` are byte-identical.

Frozen files:
- `derived/predictions.csv`: every scored number, with baselines and SDR standard errors;
- `derived/tolerances.json`: the scoring rules with their numeric bounds;
- detail tables: `derived/nae_quantities.csv`, `nae_states.csv`, `nas_ratios.csv`, `hcris_states.csv`;
- `derived/inputs.json`: input hashes, the NIPA splits, the bridge and power figures.

Each table below gives the personal / shared allocation where the two differ. All numbers are
[CALCULATION: `predict.py`] unless tagged otherwise.

| Check | Target | Blind? |
|---|---|---|
| 1 | NAE 2021, undocumented Mexican households, 2019; shared method, so only a disagreement counts | Yes for the Mexico figures (details below) |
| 2 | NAS 2017 Table 8-1, first generation and dependents, 2013; a disclosed comparison, not a pre-registered test | No: 0.79 and 0.90 are known |
| 3 | CMS HCRIS Worksheet S-10, uncompensated care by state | Yes |

## Check 1. NAE/AIC: Mexican undocumented households, 2019 (shared method)

**This is a shared-method comparison, not an independent test.** NAE and the account share the two steps
that matter most here.
- Both impute legal status with a Borjas-style residual: NAE's 2019 rules (reads Q6) and the account's
  `status_impute_2026_09_16`.
- Both take federal taxes from CBO. NAE applies CBO's 2017 average rates by income group (reads Q3). The
  account allocates federal taxes by CBO's incidence rules and re-keys the federal income tax with CBO's
  income-tax gradient.

Agreement therefore cannot validate the account; only a disagreement is informative. Each item scores
"finding" or "no finding", never "hit". The parent approved the retarget on these terms and asked for
three items whose disagreement would count: income per household, the state distribution and the
payroll share. The tax ratios are reported with the direction their conventions predict.

**Target.** AIC publishes no tax or spending-power figure for all Mexico-born immigrants. The only AIC/NAE
publication with Mexico-born figures is New American Economy's "Examining the Economic Contributions of
Undocumented Immigrants by Country of Origin" (8 March 2021, now hosted by AIC; ACS 2019 1-year).
- Its Table 4 (United States row and leading states) and Table 5 (Mexico row) cover "Mexican
  undocumented households". They give household income, federal income taxes, state and local taxes,
  spending power, and Social Security and Medicare contributions.
- Its text gives the number of Mexican immigrants lacking legal status.

[SOURCE: `reads/aic_methodology.md`, a firewalled read of the methods only]

**Blindness.** The predicting agent has not opened the report; the raw copy sits unread in `_cache/aic/`.
A count-only search found no repository file that pairs Mexico with AIC, NAE or "spending power". The
agent recalls no NAE figure for Mexico. It recalls, vaguely, the order of magnitude of AIC's
all-immigrant headlines [TRAINING-DATA], and it saw ITEP's July 2024 totals for all undocumented
immigrants in `external_benchmarks_2026_09_24/unauthorized_arm.py`. Both differ from this target in
population, year and method.

**Definitions matched.**
- Unit: households whose reference person is Mexico-born and imputed unauthorized, with every member's
  income and taxes. NAE's rule is "a household is defined as a foreign-born household if the household
  head is foreign-born"; applying it to Mexican undocumented households is [INFERENCE].
- Status: the account's imputation with the adopted tax block's state-aware flag. The flag stops
  treating Medicaid as proof of legal status in status-blind states such as California in 2024. NAE's
  2019 rules treated Medicaid as proof everywhere, and California did not yet cover undocumented adults
  in 2019, so the flag brings the 2024 frame closer to NAE's coding.
- Weights: audit row 4 (Mexico-born outside CA and TX scaled to their ACS 2024 levels).
- Taxes: the `model.json` keys, with the audit's status rule (row 2) applied household by household.
  - On-books shares apply to income-tax liabilities, wages, payroll and the FICA-worker count: 0.526
    for the Mexico-born (range 0.415–0.635) and 0.550 for other Latin-American-born. EITC is zeroed and
    ACTC is scaled. [DATA: `onbooks_share_2026_09_23/derived/onbooks_split.csv`]
  - The account's other union-level tax corrections are left out, because they cannot be applied
    household by household. These are the CPS fill-in drift (audit row 13) and CBO's income-tax
    gradient, carried as edits in `main_case_long_run_2026_09_27/derived/corrections.json`.
- Federal and state-local splits: NIPA 2024. Federal corporate is $491.66bn of $663.69bn, federal excise
  $99.96bn of $371.26bn, and federal other production taxes $1.58bn of $145.26bn. [DATA: BEA NIPA flat
  file, series B075RC, W025RC, B234RC, LA000239, LA000237, LA000357]
- NAE's "federal income taxes" is ambiguous (reads Q3). Reading A (primary) is CBO's scope: individual
  income tax, payroll (employee and employer), corporate and excise. Reading B is individual income tax
  only.
- Spending power = household income − federal − state and local taxes, as NAE defines it.
- Payroll, NAE's standard rule (reads Q3): 12.4% up to the taxable maximum and 2.9% on each member's
  wages, or on self-employment income for the self-employed.
  - The cap is the 2024 maximum, $168,600, because the frame's earnings are 2024's [SOURCE: the same cap in
    `research/immigration-lifetime-longevity-and-social-security-timing-2026-09-18.md`]. It barely binds
    for this group.
  - S is that statutory payroll over household income. NAE may have halved it with its filing discount
    (reads, unanswered 5).
- Year: ratios need no bridge. Income per household needs one, declared now.
- Bridge, 2024 → 2019, income only (no count enters): SSA's average wage index 2019/2024 = 0.7746
  [SOURCE: SSA AWI, cached in `external_benchmarks_2026_09_24/_cache/arm3b/awi_plain.html`] × ACS/CPS
  income 0.95 (0.90–1.00) [INFERENCE] × the group's 2019/2024 wage ratio relative to the index, 1.0
  (0.95–1.05) [INFERENCE]. Central 0.736, range 0.662–0.813.

**The three items that can yield a finding.** All values are [CALCULATION: `predict.py`].

| Item | Account (SE) | No finding if NAE is inside | Naive baseline |
|---|---:|---:|---:|
| Income per household, 2019 $ | $60,570 (bridged range $54,513–66,946); 2024: $82,316 ($3,201) | $48,456–75,713 | $90,050 (national mean per household) |
| Income per Mexican undocumented immigrant, 2019 $ | $24,243 ($21,818–26,794); 2024: $32,946 ($1,348) | $19,394–30,303 | $35,946 (national mean per person) |
| Payroll (Social Security + Medicare) / income | S = 0.1405 (0.0022); halved 0.0703 | 0.119–0.162 or 0.060–0.081 | 0.102 (national average) |
| State shares of household income | table below | D ≤ 0.08 and below the baseline's D | all Mexico-born persons |

- **Income per household.** NAE publishes household income but, as far as the methods read shows, no
  household count.
  - The scored figure is NAE's household income over its household count if the report states one.
    Otherwise it is over NAE's count of Mexican immigrants lacking legal status, against the account's
    value on that denominator.
  - Finding if the figure falls outside 0.80–1.25 × the account's value at the central bridge. The
    bridge alone spans 0.90–1.105 of central. The rest of the band covers sampling (SE 4%) and the
    account's own variants: paper rules instead of the state-aware flag +3.7%, published weights instead
    of row 4 −0.9% on the per-person figure.
- **Payroll share.** No finding if NAE's (Social Security + Medicare) / household income, United States
  row, is within ±15% of S (NAE's standard rule) or of S/2 (the same rule halved); otherwise a finding.
  - A value between the two bands is a finding: neither declared convention produces it.
  - Two values are recorded now, before scoring, so that Phase 2 can name a convention without fitting
    one: the unauthorized members' own statutory payroll over household income, 0.110, and the mixed
    rule that halves only theirs, S − 0.110/2 = 0.085.
  - The frame's earnings are 0.949 of the group's household income (SE 0.006).
- **State shares.** D is the total variation distance over NAE's listed states plus one "rest" cell,
  comparing NAE's shares of its United States row with the account's. No finding if D ≤ 0.08 and D is
  below the baseline's D; finding if D > 0.15 or D is not below the baseline's; otherwise partial.

**The tax ratios: directions set by convention.** Personal / shared allocation:

| Ratio to household income | Account | NAE expected | Finding only if NAE is | National average rate |
|---|---:|---|---|---:|
| Federal, reading A | 0.163 / 0.165 (SE 0.005) | lower | above 0.206 | 0.284 |
| Federal, reading B | 0.057 / 0.057 (0.004) | lower | reported only | 0.146 |
| State and local | 0.103 / 0.104 (0.003) | lower | above 0.129 | 0.154 |
| Spending power A | 0.734 / 0.732 (0.008) | higher | below 0.702 | 0.562 |
| Social Security, Medicare (account's on-books rule) | 0.069 / 0.070, 0.019 / 0.019 | (payroll item) | | |

- NAE applies CBO's and ITEP's average rates for the group's income groups, which are low for
  low-income households, and then halves the taxes (reads Q4, Q6). The account charges consumption and
  property taxes in full and scales only the wage-based taxes by the on-books share.
- NAE should therefore come in lower on taxes and higher on spending power. A gap in that direction
  reflects the conventions and says nothing about the account.
- A gap the other way beyond the band would mean the account attributes less tax to this group than
  CBO's and ITEP's schedules do. That would be a finding.
- The federal column may be reading A or B and the report cannot settle which (reads Q3), so reading
  A's bound decides.

The account's own choices move these ratios as follows:
- On-books share low / high: federal A 0.142 / 0.184, state and local 0.101 / 0.105, spending power A
  0.757 / 0.711.
- Without the status rule, with every CPS wage on the books: federal A 0.251, state and local 0.112,
  spending power A 0.637.

**State shares of the group's household income.** All 51 states are in `nae_states.csv`.

| State | Account (SE) | Baseline: all Mexico-born persons |
|---|---:|---:|
| CA | 0.280 (0.022) | 0.356 |
| TX | 0.193 (0.018) | 0.215 |
| GA | 0.052 (0.012) | 0.023 |
| IL | 0.048 (0.009) | 0.051 |
| SC | 0.047 (0.023) | 0.011 |
| CO | 0.041 (0.015) | 0.024 |
| NC | 0.040 (0.008) | 0.027 |
| AZ | 0.035 (0.010) | 0.048 |
| FL | 0.028 (0.007) | 0.027 |
| WA | 0.028 (0.009) | 0.025 |

**Descriptive only, not scored** (`nae_quantities.csv`):
- 1.844m households (SE 0.058m) with 7.03m persons;
- 4.61m Mexico-born imputed unauthorized (SE 0.14m);
- household income $151.8bn (SE $7.2bn), in 2024.

**What a finding would mean.**
- Income per household. The frame's income for these households (CPS 2024) differs from NAE's ACS 2019
  figure by more than the year and survey gap allows. Both sides impute status the same way, so the
  likely sources are the frame's income measurement, the state-aware flag or row 4. The account's
  receipts for the group rest on this income base.
- Payroll share. The frame's earnings share of household income differs from ACS's, and the payroll keys
  rest on it; or NAE used a convention its methods do not state.
- State shares. The geography of the imputed households is wrong, most likely through the state-aware
  flag in California or through row 4 outside CA and TX.
- A tax ratio the other way. The account under-taxes the group relative to CBO's and ITEP's schedules.

## Check 2. NAS 2017 Table 8-1 (not blind; a disclosed comparison)

**Target.** First-generation immigrants and their dependents, 2013 [SOURCE: NAS 2017, p. 389, Table 8-1,
local PDF `sources/immigration-fiscal/data/external/nas_2016/23550.pdf`]:
- receipts $10,887 and outlays $15,908 per capita;
- 0.79 and 0.90 of the average across the three groups;
- scenario 1: public goods and interest per capita.

**Not blind.** These values were known, and the account's ratios below were computed before this file
was written. The ±0.05 tolerance was chosen before the run but written down after it, so the only record of it
postdates the run. The check is therefore scored as a disclosed comparison, not a pre-registered test:
a description of where the methods agree.

**Construction.**
- Groups follow NAS pp. 387–388 over every resident of the CPS civilian universe:
  - independents (18 and over) are in their own generation;
  - minors take their co-resident parents' generation, half and half when the parents differ, else the
    oldest co-resident adult relative's;
  - first generation = foreign-born, excluding those born abroad to US parents;
  - second generation = US-born with a parent born outside the US.
- The first generation and dependents number 67.19m of 336.73m (20.0%). In 2013 NAS counted 55.5m of
  316.1m. [CALCULATION; SOURCE: NAS p. 389]
- Ratios are receipts or outlays per person relative to the civilian universe's average, on the
  account's national 2024 line totals and executed keys.
- Construction B is the report's scenario 1, reached from the account's conventions (A0) one step at a
  time.

| Step | Receipts ratio | Outlays ratio |
|---|---:|---:|
| A0 the account's keys and conventions | 0.856 / 0.850 | 0.900 / 0.893 |
| A1 receipts limited to taxes and social contributions | 0.858 / 0.851 | 0.900 / 0.893 |
| A2 economic affairs and subsidies per capita | 0.858 / 0.851 | 0.907 / 0.899 |
| A3 interest paid abroad and transfers abroad per capita | 0.858 / 0.851 | 0.911 / 0.903 |
| A4 corporate tax 80/20 (NAS) | 0.856 / 0.850 | 0.911 / 0.903 |
| **B = A5 one national per-pupil cost** | **0.856 / 0.850** (SE 0.015 / 0.014) | **0.903 / 0.896** (SE 0.004) |
| Baseline: income-proportional receipts, per capita outlays | 0.880 | 1.000 |
| NAS 2013 | 0.79 | 0.90 |

**The conventions move little.** They shift the receipts ratio by at most 0.002 and the outlays ratio
by at most 0.011. Any gap that remains must come from elsewhere:
- the eleven years between 2013 and 2024;
- the dependent definition: NAS also counts some people aged 18–23 as dependents;
- NAS's inclusion of institutionalized persons;
- the receipt keys themselves.

For the Mexico-born and their dependents under convention (b), 16.86m people, B gives receipts 0.430 /
0.435 and outlays 0.920 / 0.902. The adopted key overrides move this group's outlays by −$3.26bn for
justice use, and by +$4.20bn / +$2.72bn for uninsured use. NAS publishes no figure for this group.

**Tolerance.** Hit if NAS lies within ±0.05 of construction B at both allocations: receipts 0.806–0.900
and outlays 0.853–0.946.

**What a miss would mean.** A receipts ratio above NAS's means one of two things:
- relative tax payments rose between 2013 and 2024;
- the account's status-blind tax keys credit the non-Mexican foreign-born with more taxes. The account
  corrects this only for the Mexican-origin union.

An outlays gap would point at aging (Social Security and Medicare) or at the program keys.

## Check 3. CMS HCRIS Worksheet S-10: uncompensated care by state

**Target.** Worksheet S-10 line 30, "cost of uncompensated care" (charity care at cost plus non-Medicare
and non-reimbursable Medicare bad debt at cost), summed by provider state over the 50 states and DC.
[TRAINING-DATA: the CMS-2552-10 line layout; Phase 2 quotes the form's instructions before scoring.]
- Year: the latest cost-report year whose report count is at least 95% of the year before. The counts
  are read before any state total is formed.
- Source: CMS's Hospital Provider Cost Report (data.cms.gov), with the HCRIS raw files (worksheet S-10,
  line 30, column 1) as the fallback.
- Cleaning:
  - drop reports with a negative line 30, or with line 30 above the report's total costs;
  - sum a provider's reports within the year;
  - report both counts.
- Blind: no S-10 figure is in the repository, and the agent recalls none. It knows in general that
  non-expansion states report more uncompensated care [TRAINING-DATA].

**Prediction.**
- The adopted key (`uninsured_use_low/high`, r = 1) gives each state a share equal to its share of
  uninsured person-years: full-year uninsured plus half of part-year uninsured, CPS ASEC 2025. The group
  is 25.74% of those person-years nationally (the gate).
- In Phase 2 the shares are multiplied by the national S-10 total.
- The alternative arm r = 0.7 weights the group's person-years by 0.7.

| State | Account r = 1 (SE) | r = 0.7 | Baseline: full-year uninsured | Baseline: population | Group share of the state's uninsured (SE) | Not expanded in 2023 |
|---|---:|---:|---:|---:|---:|---|
| TX | 0.1737 (0.0058) | 0.1618 | 0.1810 | 0.0920 | 0.467 (0.021) | yes |
| CA | 0.0820 (0.0038) | 0.0753 | 0.0810 | 0.1169 | 0.507 (0.023) | no |
| FL | 0.0805 (0.0039) | 0.0844 | 0.0856 | 0.0696 | 0.108 (0.021) | yes |
| GA | 0.0469 (0.0040) | 0.0474 | 0.0514 | 0.0329 | 0.221 (0.042) | yes |
| NC | 0.0400 (0.0039) | 0.0406 | 0.0413 | 0.0321 | 0.208 (0.033) | yes |
| NY | 0.0367 (0.0027) | 0.0383 | 0.0351 | 0.0580 | 0.122 (0.029) | no |
| IL | 0.0365 (0.0029) | 0.0350 | 0.0360 | 0.0375 | 0.382 (0.034) | no |
| PA | 0.0326 (0.0026) | 0.0347 | 0.0319 | 0.0381 | 0.059 (0.019) | no |
| AZ | 0.0303 (0.0025) | 0.0276 | 0.0315 | 0.0224 | 0.534 (0.053) | no |

All 51 states, the row 4 variant and the year-matched ACS 2021–2024 variants are in `hcris_states.csv`.
The ACS variants cover the uninsured at interview and the group's share of them (Mexico-born or of
Mexican origin).

How far apart the predictions sit, as total variation distance:
- the account and population: 0.146;
- the account and r = 0.7: 0.025;
- the account and the full-year count: 0.024;
- CPS and ACS 2023: 0.064.

The level test can therefore separate uninsured exposure from population. It cannot separate r = 1
from r = 0.7; the slope test is built for that.

**Medicaid expansion.** A state counts as not expanded if it had not implemented expansion by 1 July of
the year:
- 2021: AL, FL, GA, KS, MS, MO, NC, SC, SD, TN, TX, WI and WY;
- 2022: MO drops out of the list;
- 2023: SD drops out as well;
- 2024: NC drops out as well.

[TRAINING-DATA: KFF's tracker. Phase 2 checks the dates against KFF before scoring, and KFF's dates govern.]

**Tolerances** (`tolerances.json`):
- Level: TVD between the S-10 shares and the account's.
  - Hit if TVD ≤ 0.15 and TVD ≤ 0.8× the population baseline's.
  - Miss if TVD > 0.25, or if TVD is not below the population baseline's.
  - Otherwise partial.
- Group use rate. Regress ln(S-10 share / account share) on the group's share of each state's uninsured,
  with weights equal to the account share and HC1 errors. The primary model includes the expansion
  indicator for year Y; the fit without it is reported beside. The null (the adopted key, r = 1) is a
  slope of 0. The alternative (r = 0.7) is −0.329 weighted and −0.325 unweighted. Verdicts by the 95%
  interval:
  - contains 0 and excludes −0.329: consistent with the adopted key;
  - contains −0.329 and excludes 0: favors 0.7;
  - contains both: no power;
  - excludes both: miss.
- Prior power. For a residual SD of 0.2 / 0.3 / 0.4 per state, the slope's standard error would be
  0.17 / 0.25 / 0.33 weighted, and 0.20 / 0.31 / 0.41 unweighted. Separating the two hypotheses needs an
  SE near 0.12, so **"no power" is the expected outcome** unless states scatter less than 0.14 in logs.
- National: hit if the S-10 national line 30 is within 0.8–1.25× the account's input for that year.
  That input is AHA's $42.67bn for 2020 times the account's 1.20 uplift, geometric by year: $44.66bn in
  2021, $46.74bn in 2022, $48.92bn in 2023 and $51.20bn in 2024.

**Definitional gaps, named now.**
- Line 30 includes insured patients' charity care and bad debt (deductibles). The key assumes that
  uncompensated care follows uninsured person-years.
- Cost-to-charge ratios and hospital prices vary by state.
- State indigent-care pools and public hospital systems vary by state.
- Maryland sets all-payer rates.
- The S-10 year differs from the CPS exposure year of 2024.
- CPS state samples are noisy; the SEs are in the table.

**What a miss would mean.**
- Level miss: uncompensated care does not follow uninsured exposure across states, so the key's premise
  fails. The group's 25.7% of person-years would then misstate its share of hospitals' uncompensated
  care.
- Negative slope that excludes 0: the group's uninsured use less charity care per person-year than
  others. That supports the 0.7 arm and cuts the adopted uninsured-use addition from $3.65–5.75bn to
  $2.12–3.51bn [DATA: `uncompensated_care_2026_09_23/derived/summary.json`]. A positive slope means the
  key under-charges.
- National miss: the account's national input N is off. The inside-account under-charge g × (s − k) × N
  scales in proportion.

## Phase 2 procedure (after the parent's go)

1. Fetch each primary document, hash it into `derived/sources.json` and quote the used cells in
   `reads/`:
   - the NAE 2021 report (Tables 4 and 5, the person count, and any household count);
   - the CMS S-10 data for the year the rule selects;
   - KFF's expansion dates.
2. `score.py` reads `predictions.csv` and `tolerances.json` unchanged. It writes one verdict per scored
   item and explains every gap by the definitional differences named above, or marks it unexplained.
