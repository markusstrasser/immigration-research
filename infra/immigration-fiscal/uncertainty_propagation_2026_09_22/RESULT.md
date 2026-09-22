**Verdict:** The complete annual account's headline cases have a statistical standard error of about **$12bn** ($12.0–12.3bn across the 60 executed cases, sampling plus donor error, assuming the sources are independent). If every source were perfectly positively correlated, the standard error would be **$17.5–20.3bn**. For the main CBO-informed band of **$165–197bn**, the 95% sampling intervals of its 16 cases together run from **$141bn to $221bn** ($127–235bn at the correlated upper bound). The expected finding holds only in part. **Within** one response construction the statistical interval is wider than the arm spread. The main band spans $32bn, against a 95% interval width of $48bn per case (ratio 0.67). The education-fixed band gives 0.82 and the proportional benchmark 0.39. **Across** constructions the arms dominate: 3.5× the interval width across the three headline constructions ($121–289bn); 2.0× across the proportional receipt, spending and production grid; 7.0× across ownership endpoints; and 9.7× across the service/capital capacity path, which crosses zero. CPS sampling of the incidence keys supplies about two thirds of the variance and MEPS donor means about 31%. The production term and the school correction together supply about 2–4%. At ε = 5 or 7, the nest lowers the main band to $157–192bn or $159–194bn. Those rows are sensitivities only; no headline changed. The formula audit reproduces all 73 published headline values to within 1e-13. The ledger and the complete account do **not** use opposite arithmetic signs for general services: both book costs as negative. They differ in treatment. The ledger charges state-local general administration (about $15bn) and interest on general debt (about $12bn) at full cost inside item G. The complete account holds general public services ($48.3bn assigned) and domestic interest ($134.5bn assigned) at zero response.

Date: 2026-09-22. Status: [CALCULATION] on published derived outputs and the pinned CPS ASEC 2025 and MEPS 2024 files; [MODEL] because every interval is conditional on the account's declared assumptions. This work was not committed; the parent integrates it.

## Files

- `propagate.py` rebuilds every CPS incidence key used by the headline under all 161 CPS ASEC 2025 weights. It checks replicate 0 against both producers and carries the replicate spread through the headline formula. It also builds the MEPS payer-mean covariance and combines the error sources.
- `audit.py` runs the formula-chain audit, the ledger replicate check, the ε sensitivity, the comparison of arms with sampling error, the SE catalog and the general-services comparison.
- `test_uncertainty.py` holds 10 tests, all passing: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/uncertainty_propagation_2026_09_22/ -q --import-mode=importlib`.
- `derived/` contains `case_uncertainty.csv` (60 cases), `component_sampling.csv`, `component_replicates.npz`, `key_replicate_check.csv`, `meps_donor_contribution.csv`, `variance_shares.csv`, `arms_vs_sampling.csv`, `epsilon_cases.csv`, `epsilon_bands.csv`, `formula_audit.csv`, `headline_recomputed.csv`, `ledger_replicate_check.csv`, `se_catalog.csv`, `general_services.csv` and `propagation_meta.json`.

Run order: `propagate.py` (about 7 s), then `audit.py`, then the tests. No existing `.py` file was edited. Upstream builders are imported or read only: the spending builder's `canonical_target`/`equal_unit_share`, and `build/meps_health_transport_2024.py`'s `read_meps`/`donor_model`.

## 1. Headline formula as the code computes it

[CALCULATION: `full_account_2026_09_20/welfare.py::response_pools/combine`, `service_response.py::export_service_response`; re-derived in `audit.py::pools/recompute_cases`]

```
welfare_bn = DR − T − Σ_c r_c · S_c − g · PG + (P + F)          (β = 1, O = 0, Z = 0, M = 0)
net cost   = −welfare_bn
```

| Term | Definition in code | Personal | Shared |
|---|---|---:|---:|
| DR, direct receipts | `cbo_collective` rows with response class `personal_income`/`household_direct`, excluding corporate labor/capital, owner property, remaining production property and personal property tax | 424.52 | 444.81 |
| Receipts with response 0 | corporate/property incidence, other business, public assets | 92.58 | 100.31 |
| T, household transfers, response 1 | `complete_preferred_F_per_capita`, `household_transfer` | 364.27 | 374.74 |
| S, services, 7 categories | `service` class; r_c = 1 except education = school share·school response + (1 − school share)·other-education response, and economic affairs/recreation = delayed response (0 in the CBO-lag profiles) | 357.76 | 353.21 |
| PG, defense + general public services, g = 0 | `public_goods` | 151.07 | 151.07 |
| Domestic interest, response 0 | `interest` | 134.54 | 134.54 |
| Business subsidies, fixed | `subsidy` | 10.29 | 10.32 |
| P + F, production term | `ces_0086_owner000` (GDP) / `ces_0248_owner000` (cash): σ = 2, labor share 0.65, full capital adjustment, no hours response, full tax retention, no excluded owners | 13.32 / 8.79 | same |

The school shares are 0.7153 and 0.8652. They come from the BEA cells T31505-A:29/30 and T31700-A:9, recomputed from `service_response_audit.json`. School responses are 0.63 and 0.66. Every target spending row equals the national BEA total × household pool fraction 0.99005 × target key share. Every receipt row equals the national total × key share.

**Recomputation.** All 60 `service_response_cases.csv` rows, the 4 `headline_cases.csv` rows and 9 `headline_summary.json` extremes were rebuilt from the category tables and the 3,888 benefit scenarios. The extremes are the core grid (262.05/356.84), the all-ownership maximum (21.31) and the six capacity-path bounds. The pools were rebuilt independently rather than read from `response_pools.csv`. The maximum absolute difference is **1.1e-13 bn**. There is no numeric discrepancy. [CALCULATION: `derived/formula_audit.csv`]

**General services, ledger compared with the complete account.** [CALCULATION: `derived/general_services.csv`; shares INFERENCE] Both objects book a cost as a negative number, so there is no sign flip. The treatment differs:

- The live ledger's item G (state-local general services, net of fees) charges the union **−$142.4bn** at m = 1. Using the 2022 gross function shares in `ledger_recut_2026_09_22/derived/g_composition.csv`, G includes state-local general administration (financial administration, public buildings and other administration: 10.6%, about **$15.1bn**) and interest on general debt (8.1%, about **$11.6bn**). [INFERENCE: this applies gross shares to the fee-netted total]
- The complete account assigns **$48.3bn** of all-level general public services and **$134.5bn** of domestic interest to the target, then gives both zero response in every headline case.
- The other G functions (police, highways, parks, housing) correspond to the complete account's public order, economic affairs, housing and recreation services ($107.0bn assigned). These respond fully in the proportional reference. In the CBO-lag profiles, economic affairs and recreation respond at zero.
- Federal defense, interest and general government have zero response in both objects (ledger item F central arm = 0).

The ledger's central estimate is therefore more pessimistic on state-local administration and debt service by roughly $27bn. [INFERENCE]

## 2. Sampling error, CPS 160-replicate SDR

[CALCULATION: `derived/key_replicate_check.csv`, `component_sampling.csv`]

**The ledger check.**

- The ledger base account's published **$7.473981bn** SE reproduces exactly from `replicates.npz`.
- The live endpoint (−$217.32bn; D and P on, E zero) reproduces its published `waterfall.csv` SE of **$8.700282bn** exactly.
- The **$8.81bn** quoted in the ledger's RESULT.md belongs to the superseded Sept 17 build (−$253.93bn). `replicates.npz` was rewritten by the Sept 18–19 rebuilds. The same arm composition now gives −$212.23bn with an SE of $8.69bn, so the $8.81bn figure cannot be reproduced from the files on disk.
- A test pins this, so the $8.81bn figure should be treated as historical. [DATA: `derived/ledger_replicate_check.csv`]

**The ledger items do not map onto the complete account, so no mapping was forced.** The complete account fixes national BEA totals. CPS sampling therefore enters only through the target's key shares (and through the household pool fraction, whose replicate SE is 1e-13 because replicate weights hit the same population controls). The keys were rebuilt from `pppub25.csv` and the replicate file:

- All 30 receipt keys and all 52 CPS-based spending keys, at replicate 0, equal the producers' exported shares to a relative 1e-9.
- The 30 rebuilt receipt-key SEs equal the published `target_share_sampling_se` to a relative 1e-6.
- The spending keys had no published SE; they now have one.
- Because each key is evaluated on the same replicate, covariance among receipts, transfers and services is carried in full.

| Component, $bn | Personal point | SE | Shared point | SE |
|---|---:|---:|---:|---:|
| Direct receipts | 424.52 | 8.22 | 444.81 | 8.40 |
| Household transfers | 364.27 | 5.46 | 374.74 | 5.59 |
| Income-security services | 27.69 | 3.61 | 29.34 | 3.59 |
| Public order and safety | 62.43 | 0.58 | 62.43 | 0.58 |
| Economic affairs | 36.26 | 0.52 | 36.26 | 0.52 |
| Health services | 23.53 | 0.27 | 23.53 | 0.27 |
| Education services (aggregate key, see §4) | 199.57 | 0 | 193.37 | 0 |
| **Net of the fiscal keys, per headline case** | | **9.76–10.00** | | **9.79–10.01** |

Receipts and transfers move together across replicates; a larger replicate target raises both. The net SE is therefore below their quadrature sum. [CALCULATION]

## 3. Donor and model-input error

**Independence assumption.** [ASSUMPTION]

- CPS ASEC March 2025 and MEPS 2024 are independent samples, so their covariance is set to zero. This is a design property, not a fitted result.
- The production term's published SE comes from the same CPS ASEC weights as the fiscal keys. Its replicate vectors were not exported, so the covariance is unknown.
- The school correction's SE comes from the October 2024 school supplement plus March exposure, which can share households with ASEC.
- The main row treats all four sources as independent. The envelope row adds the SEs linearly, which corresponds to ρ = +1 for every pair; for the school term it uses the lane's own upper envelope.

| Source | How obtained | SE, $bn | Variance share (main band) |
|---|---|---:|---:|
| CPS fiscal keys (receipts, transfers, services jointly) | this lane, 161-weight rebuild | 9.76–10.01 | 67% |
| MEPS donor means, 5 payers × 10 age/birth cells | this lane: stratified-PSU Taylor covariance; the estimator reproduces `donor_model`'s covariance to a relative 1e-10 | 6.74 | 31% |
| Enrollment correction to target school spending | published: `school_enrollment_2026_09_20/correction_effects.csv`, applied as a relative 1.05% (independent) or 1.22% (upper envelope) error on responsive education | 1.33–1.59 | 1.4% |
| Production term P + F | published: `benefit_scenarios.csv`, GDP 1.12 / cash 0.74 | 0.74–1.12 | 0.6% |
| **Combined, independent** | | **12.0–12.3** | |
| **Combined, all positively correlated** | | **17.5–20.3** | |

[CALCULATION: `derived/case_uncertainty.csv`, `variance_shares.csv`, `meps_donor_contribution.csv`]

The MEPS term is split by payer as Medicare $5.05bn, Medicaid/CHIP $4.19bn, health services $2.10bn, VA $0.39bn and TRICARE $0.07bn, for $6.74bn jointly. It is large because foreign-born cells are thin: the relative SE of the MEPS public-payer mean is 10–34% in the born-elsewhere cells. [DATA: `health_transport_sensitivity_2026_09_19/derived/donor_cells.csv`] The target is concentrated in those cells.

**What happened to the published SEs the brief named.** [DATA: `derived/se_catalog.csv`]

- **MEPS donor error of $7.71bn** (`all_age_ledger_2026_09_17/derived/estimates.csv`, `se_meps`): **not added**. In that ledger, MEPS means set the medical dollar level. In the complete account, BEA program totals are fixed and MEPS only splits them between groups. The donor error was recomputed on that split: $6.74bn, a similar size by coincidence of structure, not the same quantity.
- **Item M's donor uncertainty:** **not applicable**. Item M is the ledger's MEPS-to-NHEA coverage scaling. The complete account has no such scaling, because medical programs enter at BEA Table 3.12 totals. Item M's own donor error was never published.
- **`lineage_cost_2026_09_19` / `all_age` `estimates.csv` donor SEs** and **`period_uncertainty_2026_09_19`:** these belong to lifetime and lineage objects, not the annual account. They were catalogued and not used.
- **CBO school coefficients (−0.37/−0.34):** their standard errors are not in the repository. The two values remain arms.

## 4. Statistical interval compared with the arms

[CALCULATION: `derived/arms_vs_sampling.csv`; largest per-case combined SE $12.29bn, envelope $20.30bn]

| Arm set | Net cost, $bn | Span | Span ÷ 95% width (independent) | Span ÷ 95% width (envelope) | Span ÷ SE |
|---|---|---:|---:|---:|---:|
| Main CBO-informed band, 16 cases | 165.1–197.4 | 32.3 | **0.67** | 0.41 | 2.6 |
| Education-fixed band, 16 cases | 120.8–160.3 | 39.5 | **0.82** | 0.50 | 3.2 |
| Full proportional benchmark, 4 cases | 269.8–288.7 | 18.9 | **0.39** | 0.24 | 1.5 |
| Three headline constructions together | 120.8–288.7 | 167.9 | **3.5** | 2.1 | 13.7 |
| All 60 service-response cases | 33.7–288.7 | 255.1 | 5.3 | 3.2 | 20.7 |
| Proportional core grid (receipt, spending and production arms) | 262.1–356.8 | 94.8 | 2.0 | 1.2 | 7.7 |
| Full capital, all ownership endpoints | 21.3–356.8 | 335.5 | 7.0 | 4.2 | 27.3 |
| Capacity path (services and capital 0/.5/1) | −112.7–356.8 | 469.5 | **9.7** | 5.9 | 38.2 |

Unions of the per-case 95% intervals ([CALCULATION: `case_uncertainty.csv`]):

| Band | Independent | Envelope |
|---|---|---|
| Main band | **$141–221bn** | $127–235bn |
| Education-fixed | $97–184bn | $84–197bn |
| Proportional benchmark | $246–312bn | $231–327bn |

No headline case's interval reaches zero. [CALCULATION] The sign reverses only through the response and capacity arms.

[INFERENCE] The honest finding has two parts:

1. The response construction and the capacity path are what decide the size, and sometimes the sign, of the result. On this lane's metric the capacity path spans 38 SEs. The ledger's "a factor of fifty" compared an arms span with a single SE.
2. Within the named headline bands, the $32–40bn arm spread should not be read as the whole uncertainty. Sampling and donor error alone give ±$24bn around each case.

Quoting "$165–197bn" without the ±$24bn understates the uncertainty of the construction the band itself represents.

## 5. ε sensitivity

This section adds sensitivity rows only; the headline is unchanged. [CALCULATION: `derived/epsilon_bands.csv`, `epsilon_cases.csv`, from `production_nativity_nest_2026_09_22/derived/nest_headline.csv`, Option A] The nest replaces P + F in each case: +$21.53bn GDP / +$14.21bn cash at ε = 5, and +$19.16bn / +$12.64bn at ε = 7. The repository gives no source for either ε value, and the nest file tags both as unsourced.

| Construction, net cost $bn | ε = ∞ (headline) | ε = 7 | ε = 5 |
|---|---|---|---|
| Main CBO-informed | 165.1–197.4 | 159.3–193.5 | 156.9–192.0 |
| Education-fixed | 120.8–160.3 | 115.0–156.5 | 112.6–154.9 |
| Full proportional | 269.8–288.7 | 264.0–284.9 | 261.6–283.3 |
| Change per case | 0 | −3.9 (cash) / −5.8 (GDP) | −5.4 (cash) / −8.2 (GDP) |

The combined SE with the nest's own P + F SE is ≤ $12.35bn. The ε shift is therefore about half of one SE. This confirms the nest memo's inferred "$157–192bn / $159–194bn" by explicit recomputation. Adopting ε remains the operator's decision.

## Coverage: what carries uncertainty and what does not

**Carries sampling or donor error:**

- **CPS sampling on 30 receipt keys and 52 spending keys, plus the household pool fraction, jointly.** This covers every direct-receipt row, every household-transfer row and six of the seven service categories.
- **MEPS donor error on the five payer means** that split Medicare, Medicaid/CHIP, VA, TRICARE and health services.
- **The published CPS SE of the production term** (P + F).
- **The published sampling error of the school-enrollment correction**, applied to the education key as a relative error.

**Does not carry uncertainty, and why:**

- **The education-mix and postsecondary keys ($199.6bn / $193.4bn of education services, $9.0bn of education benefits) carry only partial sampling error.** These keys come from an aggregate school/postsecondary export. Only the enrollment correction's SE is published, so sampling error in the base school incidence is missing. If that base had a relative SE like the age-5–24 key (1.2%), it would add about $2.4bn at full response. [INFERENCE; not added]
- **BEA national totals are fixed.** They are administrative accounts; revision risk is not sampling error, and none was invented.
- **The outside-CPS residents' equal-cost closure** (0.99005 pool fraction) is an assumption with no error model.
- **The key-choice arms are not given an error model:** preferred versus alternative spending keys, receipt conventions and the high-AGI federal allocation. These are model uncertainty with no probability distribution, and they are shown as spans in §4.
- **The response parameters are arms:** CBO 0.63/0.66, the school share 0.715/0.865, delayed and non-school responses, and the capacity path. CBO's coefficient SEs are not in the repository.
- **CES parameters (σ, labor share), hours response, capital-tax retention and ownership** are arms. ε is a sensitivity only.
- **The covariance between the production term and the fiscal keys, and between the school supplement and ASEC, is unknown.** It is bracketed by the independent result and the ρ = +1 envelope.
- **Nonsampling error** is not propagated: survey underreporting and coverage bias, MEPS age/birth transport to Mexican-origin people, and missing capital gains. It is bias, not variance.
- **Lifetime, lineage and ledger SEs** measure other objects and are catalogued in `se_catalog.csv`, not combined.

[FRAMING-SENSITIVE] Every interval here is conditional on the account's beneficiary definition (other US residents, β = 1) and on the stationary with-versus-without comparison. It is a sampling interval for a conditional model quantity, not a confidence interval for a causal policy effect. This analysis was produced by an LLM on a politically charged topic; see `notes/llm-bias-caveat.md`.
