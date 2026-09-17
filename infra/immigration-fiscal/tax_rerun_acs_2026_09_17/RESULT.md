**Verdict:** With one federal calculator (Tax-Calculator 6.8.2, tax year 2024, current law) run on tax units built from both surveys, the ACS federal income-tax gap per standardized person is 0.96 of the CPS one for the Mexico-born and 0.97 for US-born Mexican self-ID, and the payroll-tax gaps match at 0.99 and 1.01; the calculator reproduces the Census tax model on CPS with an income-tax ratio of 1.062 for the union of Mexican-origin targets and 0.986 for native non-Hispanic whites (gate band 0.85–1.15, **PASS**) and a payroll ratio of 1.000 and 1.004.

[REPLICATION] CPS ASEC 2025 and ACS 2024 1-year PUMS, both computed in this lane with one calculator.

The earlier lane found ACS total-income gaps about 10% narrower than CPS and flagged
that an income-tax leg built on ACS "would be correspondingly smaller". Running the
tax model says otherwise: the tax gap is 3 to 4% narrower, not 10%. The CPS income
supplement's extra detail sits mostly in sources that are untaxed or lightly taxed,
so it widens the measured income gap without widening the tax gap.

## Headline: common-age gap per standardized person versus native non-Hispanic whites

Reference age shares are the white group's own full-weight shares within that survey.
`iitax` is federal income tax after refundable credits, so a negative gap means the
group pays that much less per standardized person. Intervals are replicate-only
(ACS 4/80, CPS 4/160). "Same mapping" is the CPS run restricted to the income blocks
the ACS questionnaire actually has, which is the like-for-like comparison.

| Group | Measure | ACS $ (SE) | CPS same mapping $ (SE) | ACS/CPS | CPS full mapping $ (SE) |
|---|---|---|---|---|---|
| Mexico-born | federal income tax | -4,964 (46) | -5,174 (192) | 0.96 | -5,111 (190) |
| Mexico-born | payroll tax | -1,130 (11) | -1,142 (43) | 0.99 | -1,142 (43) |
| US-born Mexican self-ID | federal income tax | -2,948 (48) | -3,034 (256) | 0.97 | -2,982 (255) |
| US-born Mexican self-ID | payroll tax | -649 (12) | -640 (47) | 1.01 | -640 (47) |
| All natives | federal income tax | -685 (8) | -689 (44) | 0.99 | -680 (44) |
| All natives | payroll tax | -191 (2) | -186 (9) | 1.03 | -186 (9) |

CPS-only categories, which the ACS cannot form because it carries no parent
birthplace, full CPS income mapping:

| Group | Federal income tax $ (SE) | Payroll tax $ (SE) |
|---|---|---|
| Mexican second generation | -3,037 (469) | -704 (76) |
| Mexican third-plus self-ID | -2,997 (229) | -619 (55) |
| Third-plus NH white (the ledger's own reference) | -39 (19) | -12 (4) |

Treating the two surveys as independent, every one of the six headline contrasts has
overlapping 95% intervals; the largest standardized difference is 1.06, for the
Mexico-born income-tax gap (`derived/acs_cps_tax_difference.csv`).

| Group | Measure | ACS minus CPS $ | SE | z |
|---|---|---|---|---|
| Mexico-born | federal income tax | 209 | 197 | 1.06 |
| Mexico-born | payroll tax | 12 | 45 | 0.28 |
| US-born Mexican self-ID | federal income tax | 86 | 261 | 0.33 |
| US-born Mexican self-ID | payroll tax | -9 | 48 | -0.19 |
| All natives | federal income tax | 4 | 45 | 0.09 |
| All natives | payroll tax | -6 | 9 | -0.64 |

## Gate 1: does the calculator reproduce the Census tax model on CPS?

Full-weight totals over the civilian household population, $bn, CPS full mapping.

| Group | taxcalc iitax | Census FEDTAX_AC | ratio | taxcalc payroll | Census FICA | ratio |
|---|---|---|---|---|---|---|
| mexico_born | 26.1 | 22.5 | 1.159 | 29.6 | 29.7 | 0.998 |
| mexican_second_gen | 32.9 | 31.7 | 1.038 | 25.4 | 25.4 | 1.001 |
| mexican_third_plus_selfid | 37.4 | 36.6 | 1.023 | 25.3 | 25.2 | 1.001 |
| usborn_mexican_selfid | 70.7 | 68.3 | 1.035 | 50.3 | 50.2 | 1.001 |
| third_plus_nh_white | 1,181.0 | 1,194.7 | 0.989 | 505.5 | 503.7 | 1.004 |
| native_nh_white | 1,250.1 | 1,268.1 | 0.986 | 534.2 | 532.3 | 1.004 |
| all_native | 1,586.0 | 1,596.9 | 0.993 | 728.3 | 725.8 | 1.003 |
| **union_of_targets** | **96.4** | **90.8** | **1.062** | **80.3** | **80.3** | **1.000** |

The gate is on the union of the three Mexican-origin targets (1.062) and on the white
reference (0.986). Both are inside 0.85–1.15, so the ACS results are **not** marked
conditional. Payroll tax reproduces almost exactly, which matters because payroll is
the leg the ledger's attribution leans on hardest.

**Where the income-tax residual sits.** The one group above 1.15 in isolation is
Mexico-born (1.159). Part is the allocation rule rather than the calculator: putting
the Census `FEDTAX_AC` through the same proportional-to-own-earnings allocation moves
the Mexico-born total from 22.5 to 23.7 $bn, which alone takes the ratio to 1.100.
The rest is refundable credits, where taxcalc is systematically less generous than the
Census model:

| Group | EITC taxcalc $bn | EITC Census $bn | ACTC taxcalc $bn | ACTC Census $bn |
|---|---|---|---|---|
| mexico_born | 4.8 | 5.8 | 2.4 | 2.6 |
| usborn_mexican_selfid | 3.0 | 4.1 | 1.9 | 2.3 |
| native_nh_white | 11.1 | 13.9 | 6.7 | 7.5 |
| all_native | 21.8 | 28.2 | 12.9 | 14.9 |

taxcalc awards between 17% and 30% less EITC than the Census model in every group. Because the
EITC is concentrated in low-income households, a proportional shortfall costs the
Mexico-born group more of its (small) tax base than it costs the white reference, which
is the whole of the remaining spread between 1.10 and 0.99. Two candidate causes were
tested rather than assumed: extending the EITC qualifying-child test from "under 19" to
the statutory "under 19, or under 24 and a student" moved the union ratio only from
1.068 to 1.062 (arm `full_eic18` retains the narrow test); and offering the Census
modelled state income tax as a deductible SALT amount changed nothing at all, because
zero returns itemize without mortgage-interest or charity data. The residual is not
diagnosed further here.

**Swapping calculators barely moves the CPS gap.** Using the Census `FEDTAX_AC`
directly with this lane's own gap estimator instead of taxcalc:

| Group | taxcalc iitax $ | Census FEDTAX_AC as recorded $ | Census FEDTAX_AC reallocated $ |
|---|---|---|---|
| Mexico-born | -5,111 | -5,419 | -5,312 |
| US-born Mexican self-ID | -2,982 | -3,090 | -3,069 |
| All natives | -680 | -685 | -691 |
| Mexican second generation | -3,037 | -3,114 | -3,207 |
| Mexican third-plus self-ID | -2,997 | -3,111 | -3,010 |

taxcalc gives a 2 to 6% narrower Mexican-origin gap than the Census model. The ledger's
choice of tax model is therefore not what produces the shortfall it reports.

## Age-matched aggregate gap, $bn

`Σ_b [Y_gb − (N_gb/N_rb) Y_rb]`, reference schedule recomputed in every replicate.

| Group | Measure | ACS $bn | CPS same mapping $bn | CPS full mapping $bn |
|---|---|---|---|---|
| Mexico-born | federal income tax | -77.2 | -92.6 | -91.7 |
| Mexico-born | payroll tax | -19.2 | -21.9 | -21.9 |
| US-born Mexican self-ID | federal income tax | -49.0 | -56.5 | -55.9 |
| US-born Mexican self-ID | payroll tax | -13.2 | -13.6 | -13.6 |
| All natives | federal income tax | -177.8 | -180.9 | -178.7 |
| All natives | payroll tax | -51.9 | -50.8 | -50.8 |

The Mexico-born aggregates differ by more than the per-person gaps because the ACS
counts a 6.8% smaller Mexico-born household population, the unreconciled discrepancy
the earlier lane reported as its Gate 2. Nothing here adjusts for it.

Per-person amounts by the eight age bands, for both surveys and every group, are in
`derived/tables.md` and `derived/taxcalc_gaps.csv`.

## Tax units

One module (`units.py`) assembles returns from a person schema both surveys fill in, so
the two arms never differ in how returns are counted, split or allocated.

**CPS.** Returns are keyed by the Census tax-unit identifier `TAX_ID`. Inside a
`TAX_ID` the non-dependent persons number 0, 1 or 2 and share one `FILESTAT`
(1/2/3 means two persons filing jointly, 4/5/6 one person), and no `TAX_ID` mixes a
filer with a non-filing non-dependent; all three facts are asserted at run time rather
than assumed. `FILESTAT` 1/2/3 maps to `MARS` 2, 4 to `MARS` 4, and 5 or 6 to `MARS` 1.
Dependents are `DEP_STAT > 0`. 80,340 returns from 142,125 persons.

**ACS.** No tax-unit identifier and no parent pointer exist, so units are approximated:
the householder (`RELSHIPP` 20) heads the household's first return; a person coded as
the householder's spouse (`RELSHIPP` 21 or 23, both confirmed against
`PUMS_Data_Dictionary_2024.csv` lines 1628-1647) with `MAR` 1 joins it, and no
spouse-coded person in the file failed that marital test; unmarried partners
(`RELSHIPP` 22 or 24, 85,549 persons) file separately; a dependent is a child of the
householder (`RELSHIPP` 25, 26, 27, 30, 35) under 19 or under 24 and enrolled
(`SCH` 2 or 3); every remaining person aged 18 or over heads his own single return.
1,931,024 returns from 3,239,682 persons in 1,348,408 households.

Two ACS rules deserve to be named because they are approximations, not readings of the
data. A non-householder adult's own children cannot be identified in the public file,
so qualifying children are attached to the householder's return. And any person under
18 who is not the householder, a spouse or a relationship-coded child is still treated
as a dependent of the householder (22,263 persons), so that every person lands on
exactly one return.

**Both surveys.** A dependent with positive own earnings files a separate single return
with `DSI` = 1 and is still claimed as a dependent on the return that claims him. This
keeps a working dependent's payroll tax inside the account. On CPS the rule agrees with
the Census model's own dependent-filer flag on 99.55% of persons (3,688 own returns
against the Census model's 3,300). A dependent without earnings contributes no income
to any return, so a dependent's unearned income is untaxed in both surveys.

Each return's `iitax` and payroll tax are allocated back to its members in proportion to
own positive earnings, equal shares when the return has no positive earnings. The
allocation is asserted to conserve every return's dollars exactly.

## Income mapping

`e00200` wages, `e00900` business, `e02100` farm, `e00300` taxable interest, `e00600`
and `e00650` ordinary and qualified dividends, `e02000` Schedule E, `e01500` and
`e01700` pensions, `e02400` gross social security, `e02300` unemployment compensation.

| Source field | taxcalc variable | Note |
|---|---|---|
| CPS `WSAL_VAL` / ACS `WAGP` | `e00200`, split head/spouse | |
| CPS `SEMP_VAL` / ACS `SEMP` | `e00900`, split head/spouse | ACS `SEMP` includes farm; CPS `FRSE_VAL` goes to `e02100` separately in the full mapping |
| CPS `INT_VAL` | `e00300` | full mapping only |
| CPS `DIV_VAL` | `e00600`, and 0.75 of it to `e00650` | the qualified share is an assumption; ASEC reports one combined dividend amount |
| CPS `RNT_VAL` | `e02000` | full mapping only |
| CPS `INT_VAL`+`DIV_VAL`+`RNT_VAL` | positive part `e00300`, negative part `e02000` | the ACS-aligned CPS mapping |
| ACS `INTP` | positive part `e00300`, negative part `e02000` | ACS combines interest, dividends **and** net rental income in one field, so no qualified-dividend rate can apply on the ACS side |
| CPS `PNSN_VAL`+`ANN_VAL` / ACS `RETP` | `e01500` and `e01700` | treated as fully taxable; neither survey separates the untaxed portion |
| CPS `SS_VAL` / ACS `SSP` | `e02400` | taxcalc computes the taxable share |
| CPS `UC_VAL` | `e02300` | full CPS mapping only; no ACS counterpart exists |
| ACS `OIP` | **unmapped** | "all other income" mixes unemployment compensation, alimony, child support and veterans' payments with no way to separate the taxable part |
| CPS `SSI_VAL`, `PAW_VAL`, `VET_VAL`; ACS `SSIP`, `PAP` | **unmapped** | not taxable |
| itemized deductions, child-care expenses, capital gains, IRA distributions | **unmapped** | neither survey carries them |

Because the CPS supplement has blocks the ACS lacks, every ACS-versus-CPS comparison in
this file uses the CPS `acsmap` arm. The CPS `full` arm is reported beside it: the two
differ by at most 1.8% in any headline gap, so the extra CPS detail is not what drives
the comparison either way.

## Scope limits

- **Federal only.** No state or local income tax is computed on either survey. The CPS
  ledger's modelled account also carries `STATETAX_A`; nothing here replaces it.
- **ACS tax units are approximate.** The two rules named above (children attached to the
  householder, residual minors treated as the householder's dependents) have no ACS
  evidence behind them. A married non-householder couple inside someone else's household
  files as two singles here.
- **Both surveys are self-reported.** This compares two instruments with different
  frames, reference periods and questionnaires. An error common to both would not show
  up. It tests survey-specific measurement, not self-report bias in general.
- **Reference periods differ.** ACS asks about the twelve months before a rolling
  interview date across 2024; `ADJINC` (1.015250 for 2024) was applied to every mapped
  ACS dollar. CPS ASEC 2025 asks about calendar 2024.
- **Standard errors are replicate-only.** No model, coverage, undercount or
  nonresponse-adjustment error is included. The ACS intervals are four to five times
  tighter purely because the sample is about twenty times larger.
- **No itemizers.** Without mortgage-interest, charity or property-tax data, zero returns
  itemize in either survey. This overstates tax at the top of the distribution, which
  falls mainly on the white reference group and therefore narrows the measured gaps.
- **Survey totals fall below published receipts.** The whole ACS household population
  carries $1,789bn of federal income tax here and all CPS natives $1,586bn; published
  federal individual income-tax receipts for 2024 are materially higher, chiefly because
  neither survey carries capital gains and both top-code high incomes. [UNVERIFIED] The
  receipts figure was not fetched in this lane.
- **Population counts are not reconciled.** ACS counts 11.44M Mexico-born against the
  CPS 12.22M. Per-person gaps are unaffected; aggregates are not.
- **Group definitions.** `usborn_mexican_selfid` pools second, third and later
  generations in both surveys and is not either of the ledger's lineage categories; the
  CPS-only split is reported separately. The ACS carries no parent birthplace.

## Files covered

All paths under
`/Users/alien/Projects/immigration-research/infra/immigration-fiscal/tax_rerun_acs_2026_09_17/`.

| File | Role |
|---|---|
| `taxcalc_io.py` | the only calculator call; chunked `Records`/`Calculator`, employee-share payroll |
| `units.py` | returns, counts, income splitting, allocation, structural guards |
| `cps_tax.py` | CPS tax units, four arms, the Census anchor |
| `acs_tax.py` | ACS tax units from relationship, marital status, age, enrolment |
| `shared.py` | cells, common-age and age-matched gaps, anchor table |
| `make_tables.py` | assembles the deliverables |
| `derived/taxcalc_gaps.csv` | both surveys' gaps, every group and variable |
| `derived/anchor_ratios.csv` | CPS totals against the Census tax model |
| `derived/audit.json` | hashes, taxcalc version, mappings, unit rules, diagnostics |
| `derived/tables.md` | rendered tables including per-person amounts by age band |
| `derived/acs_cps_tax_difference.csv` | ACS minus CPS with z and interval overlap |
| `derived/cps_tax_cells.csv`, `derived/cps_tax_gaps.csv`, `derived/cps_anchor.csv`, `derived/cps_audit.json` | CPS arm |
| `derived/acs_tax_cells.csv`, `derived/acs_tax_gaps.csv`, `derived/acs_totals.csv`, `derived/acs_audit.json` | ACS arm |

Read, not modified: `all_age_ledger_2026_09_17/README.md`,
`acs_earnings_replication_2026_09_17/{RESULT.md,README.md,acs_gaps.py,cps_gaps.py,common.py}`,
`gen_ledger_extension_2026_09_16/extend_ledger.py`, `build/analyze_cps_fiscal_2025.py`.
`common.py` and `cps_gaps.build_groups` are imported from the ACS lane so the estimators
and group definitions are literally the same code.

Sources: CPS ASEC 2025 public use file, sha256 in `derived/cps_audit.json`; ACS 2024
1-year person PUMS, sha256
`afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894`; ACS PUMS data
dictionary fetched to `_cache/PUMS_Data_Dictionary_2024.csv`.

## Skipped and why

- **State income tax on ACS.** taxcalc is a federal calculator. Nothing state-level was
  attempted on either survey, so this lane cannot re-do the ledger's `STATETAX_A` leg.
- **CA and TX subdomains.** The earlier lane reported state cuts; the brief asked for
  national common-age gaps by eight age bands, and the ACS tax-unit construction is
  weakest exactly where household composition is unusual, so no state cut is published.
- **The EITC residual.** Diagnosed to refundable credits and quantified above, with two
  candidate causes tested and rejected. Not chased further, because the gate passes and
  the direction of the residual (taxcalc taxes low-income groups slightly more) makes
  the measured Mexican-origin gaps conservative rather than inflated.
- **Reconciling the 6.8% Mexico-born population difference.** Out of scope here, as in
  the earlier lane.
- **Unpinned taxcalc.** The brief's plain `--with taxcalc` resolve did not terminate in
  15 minutes against an index where taxcalc ships only a source distribution. The
  version is pinned to 6.8.2 in the reproduce commands; `taxcalc.__version__` is recorded
  in every audit file.
