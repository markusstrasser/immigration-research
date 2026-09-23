# Spending-side dataset integrity audit

**Verdict:** The two largest defects both make the Mexican-origin group look worse, and they share a
sign. (1) The whole BEA refundable-credit line ($228.8bn) is keyed by CPS EITC+ACTC, although about
half of it is ACA premium tax credits. Re-keying that half moves **−$12.0bn to −$14.4bn** off the
target, and the main case falls by about as much because the line responds fully. The Census tax
model also gives EITC/ACTC to filers who cannot legally claim them; together the two corrections
reach −$15.1bn to −$18.4bn. (2) The Medicaid total ($954.2bn) is spread by a MEPS community-only key,
so institutional and home-based long-term care for the aged and disabled is charged to the target
at 12.3% instead of an estimated 4–8%. That moves **−$3.6bn to −$15bn** (bounded, not measured).
Smaller items run the other way: household rental assistance filed as a fixed "business subsidy"
(up to +$7.5bn if it responded), and unallocable state/local spending given the administration
elasticity (+$2.0bn). No unit, scaling or intergovernmental double-count error was found in the
files that feed the main case.
Provenance: [CALCULATION] from the probe scripts in this directory; [SOURCE] tags inline; bounds
are marked [INFERENCE].

## Files traced (followed through the scripts)

| File | Feeds |
|---|---|
| `/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx` (Tables 3.1, 3.12, 3.13, 3.16, 3.17; CY2024) | Every national spending total in `full_account_spending_2026_09_20` → `full_account_2026_09_20` → main case ($203.2–249.6bn); the school share in `service_response.py`; the general-government composite in `assumption_explorer_2026_09_21/scaling_check.py` |
| CPS ASEC 2025 `asecpub25csv.zip` (`EIT_CRED`, `ACTC_CRD`, `SS_VAL`, `SSI_VAL`, `PAW_VAL`, `UC_VAL`, `VET_VAL`, `WC_VAL`, SPM SNAP/WIC/energy/housing, `MCAID`) | Every benefit incidence key in `full_account_spending_2026_09_20/builder.py` |
| MEPS 2024 `h256dat.zip`, `h256su.txt` | Medicare, Medicaid, VA, TRICARE and other-health keys (5 age bands × US/not-US birth) |
| `school_enrollment_2026_09_20/derived/updated_account_components.csv` ← CPS October 2024 + Census ASSF FY2024 Table 8 per-pupil (`gen_ledger_extension_2026_09_16/state_parameters.csv`) | `school_operating`, `postsecondary` and `education_mix` keys (education services: target $199.6bn) |
| Census 2022 State & Local Finance Table 1 (`assumption_explorer_2026_09_21/_cache/slf2022.xlsx`) | General-government response 0.59–0.84 (adopted change 1, +$28.5–40.6bn) |
| F-33 FY2024 district file `elsec24t.txt` × NCES CCD 2023–24 LEA membership | District differential D (generation-split ledger only; not in the complete account) |
| `ledger_absolute_2026_09_17/params/params.json` (OMB historical tables, F-33 capital/interest/membership, DHS/DOJ budgets) | Generation split (`ledger_absolute_2026_09_17`) |

Not in the main-case chain: SIPP 2024/2025 (only `sipp_lineage_2026_09_20` checks and the lifetime
warehouse) and English-learner counts (`service_response.py` states "No … ELL add-on"; the `ell`
parameter block has no consumer in the ledger code).

## Defect table

Effects are on the main case in $bn a year; negative means the published cost to other residents is
too high.

| # | File · item | Check | Finding | Grade | Effect | Status |
|---|---|---|---|---|---|---|
| 1 | BEA 3.12 line 25 · refundable credits keyed by CPS EITC+ACTC | Key vs line contents | About $100–120bn of the $228.8bn is premium tax credits. The target's share of subsidized-marketplace persons is 10.9%; its EITC+ACTC share is 23.0% | A | −12.0 to −14.4 | measured |
| 2 | CPS `EIT_CRED`/`ACTC_CRD` · tax-model eligibility | Legal status | 43.8% of the target's credit dollars sit on noncitizen Mexico-born records. At a 40–60% unauthorized share, the key falls from 0.230 to 0.193–0.206 on the non-PTC part | B | −2.6 to −4.7 here; the CPS family's status-lane figure on the same non-PTC base is −3.0 to −4.0 (`cps.md` row 1, at 44–75% on-books). Jointly with #1: −15.0 to −18.4 | measured; the CPS family's figure supersedes this assumed unauthorized fraction. The CPS receipt-side change (−8.5 to −20.4 in receipts, raising the cost) is separate |
| 3 | MEPS key × BEA Medicaid/Medicare · coverage | Universe vs total | MEPS covers 38% of BEA Medicaid and 67% of Medicare. Institutional and uncaptured home-based LTSS go to the target at 12.3% | B | −3.6 to −15 (Medicare SNF about −1 more) | bounded |
| 4 | MEPS · donor filter | Sentinels | 207 positive-weight records dropped (157 `AGE24X=-1`, 84 `BORNUSA<0`). They carry 3.0% of Medicare and 3.7% of Medicaid dollars (mean age 60) | C | 0 to −2 | bounded |
| 5 | Education mix · K–12/higher weights | Key vs BEA split | Key weights K–12 at 93%. BEA Table 3.16 gives 77–82% (E&S $946bn, higher $277bn less about $64bn of student aid) | B | −2.2 to −4.8 (allocation −3.5 to −4.8) | measured |
| 6 | BEA 3.13 housing subsidies · response class | Classification | $60.3bn of federal rental assistance to low-income households is classed "subsidy" and held fixed with business subsidies; the target key gives it $7.54bn | C (framing) | 0 now; +7.5 if it responded fully | measured |
| 7 | `scaling_check.py` · S&L "Other" general public service ($168.7bn) | Function mapping | BEA footnote 7: "unallocable state and local government expenditures". This is spending of every kind, but it is given the administration elasticity 0.842; direct general expenditure has 0.962 | C | +2.0 | measured |
| 8 | `scaling_check.py` · S&L executive and legislative | Intergovernmental | Derived as total minus federal ($54.93bn); BEA line 82 gives $59.30bn. Federal grants of $4.36bn are counted as federal, which is fixed at the low end | D | +0.4 at the low end | measured |
| 9 | BEA 3.12 line 39 · "Other" state welfare keyed by WIC (22.9%) | Key vs line contents | Footnote 11: WIC food plus foster care, adoption assistance and payments to nonprofit welfare institutions | C | −1 to −2 | bounded |
| 10 | BEA 3.1 line 28 · domestic interest | Definition | Footnote 2: the line includes interest accrued on government DB-pension actuarial liabilities, which is imputed rather than debt interest | C | 0 (legacy interest is fixed); inflates the per-capita-F presentation | not measured |
| 11 | F-33 × CCD · NYC | Join | NYC (F-33 NCESID 3620580, 845,509 pupils) drops out of the join; NY covers 1.50m pupils. The coverage gate still passes (0.964) | D | ≈0 (D is ledger-only, NY Mexican-origin pupils are few) | measured |
| 12 | Income-security consumption ($167.8bn) keyed by CPS `PAW_VAL` (16.7%) | Thin key | 1.67m positive-key persons nationally; the line is mostly social services and administration | C (key choice) | −7.5 vs population key; −20 vs all-cash key | measured; not a data error |
| 13 | BEA units | Scaling | Millions → bn reproduces $10,061.458bn; Table 3.16/3.17 subtotals reconcile | — | none | checked |
| 14 | Intergovernmental double count | Consolidation | BEA 3.16/3.17 are consolidated (footnote 1); SLF line 66 is direct expenditure | — | none | checked |
| 15 | ASSF FY2024 Table 8 per-pupil | Definitions | Column 2 is "Total" current spending per pupil (US $17,619; CA $20,791; TX $12,895); it excludes capital, interest and payments to other governments (TX recapture $2.69bn) | — | none | checked |
| 16 | F-33 capital/interest (thousands) | Units | Converted ×1000 in `absolute_ledger.py`; the target's K is $26.8bn, not $26.8k | — | none | checked |
| 17 | SLF Table 1 line codes and columns | Row/column labels | Lines 66, 73, 92–94, 106–109 match their labels; the first column per state is the state-and-local amount | — | none | checked |
| 18 | MEPS weights and payer sentinels | Anchors | The reader gates record counts, published population anchors and negative payer codes | — | none | checked |

Details on the main items:

**#1 Premium tax credits.** BEA: "Because these transactions are administered as refundable tax
credits … they are classified in the NIPAs as social benefits rather than as subsidies" [SOURCE: BEA,
*The Affordable Care Act and the NIPAs*, SCB June 2014,
https://apps.bea.gov/scb/pdf/2014/06%20June/0614_affordable_care_act_and_the_nipas.pdf]. CBO put
FY2024 premium tax credit and related outlays at $103bn [SOURCE: House Budget Committee release quoting
CBO, https://budget.house.gov/download/cbo-joint-committee-on-taxation-letter&download=1; secondary].
EITC ≈ $64bn, the refundable CTC ≈ $33bn and the premium tax credit ≈ $100–120bn together fit the
$228.8bn line. Adding the non-refundable CTC as well would overshoot it, so it is probably not in the
line [INFERENCE]. The target's share of marketplace persons is a person count; premium tax credit per
enrollee rises with age, so its dollar share is lower still. 36% of the target's `MRKS` reports are
allocated, against 30% for others. [CALCULATION: `spending_credit_keys.py`] The receipts side keys
federal income tax by `FEDTAX_BC`, which is before credits, so the credit is not also netted out of
receipts. This is a key error, not a double count.

**#2 Eligibility.** EITC requires SSNs for the filer, the spouse and qualifying children, and ACTC
requires a child SSN. The Census tax model does not see legal status. The 0.4–0.6 unauthorized share
among noncitizen Mexico-born holders is assumed here. [CALCULATION: `spending_eitc_status.py`] The
CPS family's `cps_status_keys.py` applies the status lane's corrections to the whole $52.14bn line.
Combining rule: apply the status correction only to the non-premium-tax-credit part (about $109–129bn
of the line), or #1 and #2 double count.

**#3 Long-term care.** Medicaid LTSS in 2022 was $200.4bn: $71.0bn institutional and $129.4bn home and
community-based [SOURCE: Mathematica for CMS,
https://www.mathematica.org/publications/medicaid-long-term-services-and-supports-users-and-expenditures-by-service-category-2022;
search summary, PDF table not opened]. The four-checks memo uses $82.74bn institutional for 2023.
The target is 5.1% of CPS people aged 65+ and holds 8.2% of CPS SSI dollars. The outside-CPS pool,
which includes nursing-home residents, gets 0.99% of Medicaid at the average per-person cost. The bound
assumes a true target share of 4–8%, $83–87bn of institutional LTSS, and that MEPS misses 0–70% of
home-based LTSS. Mexican-origin LTSS use is not held locally, so this is not measured. [INFERENCE]
Counterweight: the target is 19.6% of CPS people who report Medicaid coverage but gets 12.4% under
the age × nativity key. Per-enrollee spending by ethnicity belongs to
`medical_ethnicity_pooled_2026_09_23`.

**#5 Education mix.** From BEA 3.16: elementary and secondary $946.2bn, higher $277.4bn, libraries
and other $129.9bn. The education consumption line (3.17, $1,221.2bn) excludes about $64.5bn of
education social benefits. The key's school/postsecondary weights ($857.8bn/$63.5bn) put 93% on K–12.
The corrected share is 0.1622–0.1605 against 0.1651. [CALCULATION: BEA probe
`spending_bea_probe.py`; key shares from `incidence_keys.csv`]

## Contradictions kept

Items #6, #7 and #8 make the group look better than the data support. #6 is the largest: household
rental assistance is treated as a fixed business subsidy. Holding it fixed can be defended because
voucher funding is capped by appropriation, but the label hides that it is a household benefit. The
Medicaid-coverage contrast under #3 also runs the other way. All the large measured defects (#1, #2,
#5) overstate the target's cost.

## What prior audits covered

- `research/immigration-administrative-checks-2026-09-19.md`: survey-to-administrative totals for SNAP,
  Social Security, SSI and UI, and the SNAP duplication check. Not repeated here.
- `research/immigration-four-fiscal-checks-2026-09-20.md`: MEPS versus CMS Medicaid scale, the
  institutional LTSS stress test and the 141 records without end-year age. That memo says "no
  national healthcare residual is assigned to the target". The complete account does assign it,
  because it spreads the whole BEA Medicaid line by the MEPS key. Finding #3 is the consequence.
- `school_enrollment_2026_09_20` README: October CPS pupil counts versus CDE/TEA, and the CA/TX
  held-out transport checks.

## Not checked, and why

- Line-by-line SNAP/SSI/UI survey reporting by group: `cps_imputation_keys_2026_09_23` owns CPS
  benefit imputation, and the administrative totals are already done.
- MEPS/MCBS ethnicity ratios: owned by `medical_ethnicity_pooled_2026_09_23`.
- OMB function totals in the generation-split ledger (net Medicare after premiums versus BEA gross):
  units are flagged per field in `params.json`, but each consumer's conversion was not traced. The
  ledger is not the main-case chain.
- The CTC composition of BEA line 25 is inferred from magnitudes, not from a BEA underlying table.
  NIPA Table 3.12U would settle it.
- SIPP 2024/2025 and EL/ELL definitions are outside the main-case chain (see the trace).

Scripts: `spending_bea_probe.py`, `spending_credit_keys.py`, `spending_meps_file.py`,
`spending_eitc_status.py` (run with `OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with openpyxl python3 <script>` from the repo root; the first takes sheet names as arguments).

Model: claude-opus-5-5 (Opus 5.5), reasoning effort as configured by the parent session.
