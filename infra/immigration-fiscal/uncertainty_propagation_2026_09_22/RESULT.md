**Verdict:** [2026-09-27: `propagate.py` now defaults to the main case of that day (`--case sept27`, `derived/sept27/`). Its CPS block carries the administrative benefit keys jointly with the account, on the same replicates (conceptual audit, section A). They correlate at −0.43 to −0.40, so the per-case SE is $10.6–10.7bn, against $11.0–11.1bn with their SE appended as if independent. The 64 specifications' 95% intervals together run $301–408bn ($286–422bn at the correlated upper bound). The capital return's own CPS part is $0.20–0.35bn. The SE is a partial sampling approximation whose net error is unresolved: the covariances still omitted can go either way. See "The September 27 case" below.] [2026-09-26, later: `propagate.py` now defaults to the main case with schools at full cost (`--case sept26_schools`, `derived/sept26_schools/`). The per-case SE is $10.9–11.0bn, and the 64 specifications' 95% intervals together run $237–313bn. `--case sept26` (`derived/sept26/`) gives the one-year scenario, $10.8–11.0bn and $179–267bn.] [2026-09-25: `propagate.py --case sept24` carries the same sources through the main case adopted September 24: per-case SE $10.8–10.9bn, the 64 specifications' 95% intervals $180–268bn together; most corrections carry ranges, not sampling errors, and are outside the SE (`derived/sept24/summary.json`; wording revised 2026-09-27, see Revisions). The September 20 outputs this text describes are unchanged. See `../sept24_propagation_2026_09_24/RESULT.md`.] The complete annual account's headline cases have a statistical standard error of about **$12bn** ($12.0–12.3bn across the 60 executed cases, sampling plus donor error, assuming the sources are independent). If every source were perfectly positively correlated, the standard error would be **$17.5–20.3bn**. For the main CBO-informed band of **$165–197bn**, the 95% sampling intervals of its 16 cases together run from **$141bn to $221bn** ($127–235bn at the correlated upper bound). The expected finding holds only in part. **Within** one response construction the statistical interval is wider than the arm spread. The main band spans $32bn, against a 95% interval width of $48bn per case (ratio 0.67). The education-fixed band gives 0.82 and the proportional benchmark 0.39. **Across** constructions the arms dominate: 3.5× the interval width across the three headline constructions ($121–289bn); 2.0× across the proportional receipt, spending and production grid; 7.0× across ownership endpoints; and 9.7× across the service/capital capacity path, which crosses zero. CPS sampling of the incidence keys supplies about two thirds of the variance and MEPS donor means about 31%. The production term and the school correction together supply about 2–4%. At ε = 5 or 7, the nest lowers the main band to $157–192bn or $159–194bn. Those rows are sensitivities only; no headline changed. The formula audit reproduces all 73 published headline values to within 1e-13. The ledger and the complete account do **not** use opposite arithmetic signs for general services: both book costs as negative. They differ in treatment. The ledger charges state-local general administration (about $15bn) and interest on general debt (about $12bn) at full cost inside item G. The complete account holds general public services ($48.3bn assigned) and domestic interest ($134.5bn assigned) at zero response.

Date: 2026-09-22. Status: [CALCULATION] on published derived outputs and the pinned CPS ASEC 2025 and MEPS 2024 files; [MODEL] because every interval is conditional on the account's declared assumptions. This work was not committed; the parent integrates it.

## Files

- `propagate.py` rebuilds every CPS incidence key used by the headline under all 161 CPS ASEC 2025 weights. It checks replicate 0 against both producers and carries the replicate spread through the headline formula. It also builds the MEPS payer-mean covariance and combines the error sources.
- `audit.py` runs the formula-chain audit, the ledger replicate check, the ε sensitivity, the comparison of arms with sampling error, the SE catalog and the general-services comparison.
- `test_uncertainty.py` holds 10 tests, all passing (14 since 2026-09-27, with one per later case and the capital return): `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/uncertainty_propagation_2026_09_22/ -q --import-mode=importlib`.
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

## The September 27 case (2026-09-27)

`node sept24_specs.cjs` costs the case through its own package (`main_case_long_run_2026_09_27/package.cjs`,
`evaluateFull`) on its 64 specifications, on the uncorrected model and on the model with its payload. The
payload model gives the mean of the two fill-in methods in the case lane's `per_spec.csv` at every
specification, in cost and in capital return (1e-9), and the costs span `main_case` ($321.82–387.37bn) and
`uncorrected_at_adopted_responses` ($332.75–398.31bn) exactly (1e-9). `derived/sept27/spec_costs.csv` carries
the capital return in its own columns and its derivative with respect to each key line's group amount
(`kcoef_<line>`, and `kcoef_enterprise_share` for the enterprise receipt's share); the derivatives rebuild the
return on both models (1e-9).

`propagate.py --case sept27` rebuilds each uncorrected specification from its September 20 case (1e-6), now
with the long-run responses of economic affairs and recreation, rental assistance, the enterprise receipt and
the capital return, and carries the errors through them:

- **CPS.** Economic affairs and recreation are service lines this lane replicates; they enter at their long-run
  responses. Rental assistance is replicated on its account key (`housing_support`), the enterprise receipt on
  the group's population share (general government's per-head key). Each key line's weight adds the capital
  return's derivative, so the return's error moves with its keys.
- **MEPS.** Health services' payer gradient adds the derivative of the health capital.
- **School correction.** The K-12 and college returns ($12.4–19.1bn) scale with the education lines' relative SE.
  A test pins them to the case lane's `capital_k12_bn + capital_college_bn`.

**The benefit keys, jointly (parent note, 2026-09-27; conceptual audit, section A).** The administrative
benefit keys re-key SNAP, WIC, TANF, UI and rental assistance with factors computed from the same 160 CPS
replicate weights as the account, so their error is not independent of the account's. `propagate.py` now
rebuilds the producer's central factors on every replicate (`benefit_replicates()`; each change and its
replicate SE equal `admin_benefit_keys_2026_09_24/derived/program_keys.csv` to 1e-8), multiplies each line's
change by the case payload's stack factor (`sept24_specs.cjs` → `derived/sept27/benefit_factors.csv`, the
methods' mean, gated against `stackFactor` to 1e-12) and by the line's response (transfers 1; rental
assistance 1 in this case, so its re-keying now counts), and adds the signed deviation to the account's
receipts-minus-spending deviation before taking the variance. That joint CPS error is the primary CPS block;
every combined column and interval uses it. The published method (the account's combined SE with
`package_se.csv` appended as if independent) stays beside it in `se_with_benefit_keys_bn`; that file leaves out
rental assistance, which every earlier case held at response 0.

Positive control: the same code, forced on for the schools case in scratch, reproduces the audit's
`probe_uncertainty.py` on all 64 specifications to 5e-15 (account CPS SE, benefit SE, correlation,
independent append, joint first order, joint with the factor product, combined), and its account-only and
appended columns equal this lane's published schools-case columns exactly. Two `sept27` runs are
byte-identical, and the older cases rerun with no tracked change.

| $bn | Schools case | September 27 |
|---|---:|---:|
| **Per-case SE, sources independent, CPS block joint with the benefit keys** | 10.60–10.71 (audit probe) | **10.55–10.66** |
| Per-case SE, benefit keys' SE appended as if independent (the published method) | 10.99–11.09 | 10.98–11.07 |
| Per-case SE, sources independent, without the benefit keys | 10.93–11.03 | 10.92–11.00 |
| Per-case SE, all positively correlated (joint CPS block from September 27) | 17.96–18.39 | 17.65–18.09 |
| CPS block, joint | 8.54–8.67 (audit probe) | 8.42–8.57 |
| CPS keys of the account alone | 8.95–9.06 | 8.87–8.99 |
| of which the capital return's own CPS part | — | 0.20–0.35 |
| of which rental assistance and the enterprises | — | 0.44–0.46 |
| Benefit keys' own replicate SE | 1.11–1.15 (rental assistance at 0) | 1.20–1.23 |
| Their correlation with the account's CPS deviation | −0.42 to −0.40 | −0.43 to −0.40 |
| The two appended as if independent | 9.02–9.13 | 8.96–9.08 |
| Joint, with the factor-product term (the change's level on the replicate) | 8.54–8.67 | 8.42–8.57 |
| School correction | 1.94–2.09 | 2.07–2.29 |
| 95% intervals of the 64 specifications, union | 236.9–313.4 | 300.9–408.1 |
| At the correlated upper bound | 222.5–327.2 | 286.5–422.1 |
| With the benefit keys appended as if independent, union | 236.8–313.5 | 300.1–408.9 |
| Uncorrected model at the adopted responses, SE (control; no benefit keys) | 12.27–12.34 | 12.26–12.33 |

[CALCULATION: `propagate.py` → `derived/sept27/case_uncertainty.csv`, `derived/sept27/summary.json`; the
schools case's published columns in `derived/sept26_schools/`, its joint values from the audit's probe; the
row without the benefit keys is the account's CPS block combined with the other three sources.]

The joint CPS SE is $0.50–0.53bn below the two appended as if independent, and $0.42–0.45bn below the
account's alone; the combined SE falls $0.40–0.42bn against the published method. A likely reason for the
negative sign: each factor divides an administrative rebuild of the union's share by the same rebuild on CPS
shares, so a replicate with more CPS Hispanic receipt raises the account's key and lowers the factor, and the
corrected amount leans less on the survey. [INFERENCE]

The account's CPS error falls slightly although more lines respond. The added spending lines' replicate
deviations move with the receipts' (correlation 0.30 on the shared allocation), so charging more of them
offsets part of the receipts' deviation (scratch check: the receipts' SDR of $8.40bn falls to $8.21bn net of
the three added lines).

**No error model here:** the BEA net stocks the return charges (no published SE), the rate (2% or 3%, an arm of
the case), the long-run responses (arms) and the enterprises' national operating result (a BEA total).

**Not a bound in either direction.** The SE is a partial sampling approximation whose net error is
unresolved. An omitted covariance can leave it too high or too low: the benefit keys' was negative, so leaving it
out overstated the SE. Still omitted: the
production term's and the school supplement's with the CPS keys, and the pooled medical translator's. The
translator's five-line p99.5 correction has an $8.039bn SE before LTSS and package scaling
(`medical_ethnicity_pooled_2026_09_23/derived/translation_account.csv`, row `winsor_p995`, all five medical
lines). Its 2024 MEPS donors overlap the donor base whose error this lane already carries, and the case scales
the old gradient by the corrected dollar level without the ratio's derivative. Adding that SE independently
would double count the shared donors and ignore their covariance, so it is not added; the medical bridge's
joint error is unresolved.

## v4 case (sept29), 2026-09-29

claude-opus-5-5 (the v4 consumer lane; its fork B began this section and stopped at the usage limit, and the lane
finished it). **Verdict:** on the main case adopted 2026-09-29 (`../main_case_2026_09_29/`, $371.41–434.84bn at
specifications 48 / 11), the per-case SE is **$9.41–9.59bn** (sources independent, CPS block joint with the benefit
keys), and the 95% intervals of the 64 specifications span **$352.6–453.3bn** ($339.4–466.1bn at the correlated upper
bound). The SE is $1.1bn below September 27's $10.55–10.66bn for two reasons. The pension accrual moves with the
payroll taxes that buy it, and Part A's accrual replaces a Medicare amount that carried MEPS error. Both follow from
rules this section had to design; the alternatives are beside them.

`node sept24_specs.cjs` costs the case through the adopted package (`main_case_2026_09_29/package.cjs`,
`evaluateFull`) on its 64 specifications. It uses two models: the uncorrected model with the payload's synthetic lines
at zero (`withSyntheticLines`), and the model with its payload. The payload model gives the methods' mean of the case
lane's `per_spec.csv` at every specification, in cost and capital return (max |diff| 1.7e-13). The costs span
`main_case` ($371.4146–434.8410bn) and `uncorrected_at_adopted_responses` ($313.2581–378.9158bn) exactly (1e-9).
Every specification sets the case's 13 line responses, and each engine row takes its specification's. The script
gains three things:

- **Each model's own capital derivatives.** The payload rescales rental assistance's national total by 0.9127
  (public housing split out), so the return's derivative on that line differs between the models, by up to 0.020.
  `spec_costs.csv` carries `kcoef_<model>_<line>` for both, and each rebuilds its model's return (2.8e-14).
- **The production term's SE on each model's grid** (`production_se_<model>_bn`). The payload's production grid
  uses the account's row-4 weights; the uncorrected model's SE equals the published CES scenario's (1e-9).
- **Line targets for the payload's new receipt lines, and a national-scale column in `benefit_factors.csv`.**
  Rental assistance's benefit shift is scaled by the same 0.9127, because every national-scale edit on the line
  follows its cell edits (gated).

`propagate.py --case sept29` is now the default, as the last entry of `later_cases.json`. It rebuilds each uncorrected
specification from its September 20 case (1e-6), with the receipt responses added, and carries the errors through
four rules this section designed:

1. **The pension switch.** The payload defines Social Security's group amount as ratio_net (0.9737) times the
   group's OASDI receipts: employee and employer OASDI, plus 0.8035 of the self-employment tax. On each replicate the
   line therefore deviates by ratio_net times those receipts' deviation, in place of its own key's, and the group's
   payroll taxes and the promises they buy move together. A gate checks the rule on the payload's targets (1e-9).
   Beside it: the accrual held fixed (CPS SE $8.15–8.47bn, combined $9.85–10.10bn), and the lane's generic rule,
   social_security's own key scaled like every corrected line ($8.94–9.05bn, combined $10.51–10.59bn).
2. **Part A's accrual carries no error.** The payload swaps Part A's share of the Medicare line (0.3751) for a fixed
   $41.14bn, which the pension lane counts from covered workers, not from Medicare use
   (`pension_accrual_2026_09_28/RESULT.md`). The Medicare line's CPS and MEPS errors scale with the rest of its
   amount. A gate checks that the line less the accrual is 0.6249 of the cash set's (the candidate's
   `corrections_v4_cash.json`, which the adopted lane reads for its cash row), to 1e-9. Beside it, in a scratch run
   that is not a lane output: if the accrual carried the line's MEPS error in proportion to its amount, the MEPS SE
   would be $7.13bn, the combined SE $10.80–10.94bn and the 95% union $350.0–456.0bn. The accrual's own sampling
   error, in the count of covered workers, is not modelled.
3. **Receipt responses.** The case sets responses on four receipt lines besides the enterprises. Personal property
   tax sits on the account's capital-income key, which this lane replicates, and carries that key's spread ($0.07–0.08bn
   of SE). Public housing's operating result (`housing_enterprise_surplus`, national −$45.56bn, a payload line) sits at
   rental assistance's key share (gated to 1e-12) and moves with it. Owner-occupied and tenant-occupied property taxes
   sit on keys this lane does not replicate (the modeled owner-property key and renters' contract rent) and carry none.
4. **Correction lines with no amount on the uncorrected model** (roads by miles and the three state prices) enter the
   cost at their responses and carry no sampling error; their ranges are the package's. A gate checks that none has an
   amount on the uncorrected model.

Two `sept29` runs are byte-identical, and the older cases rerun with no tracked change. A test pins the production
term's SE to each model's grid and the pension alternatives' combination with the other sources
(`test_payload_production_grid_and_pension_switch`).

| $bn | September 27 | September 29 (v4) |
|---|---:|---:|
| **Per-case SE, sources independent, CPS block joint with the benefit keys** | 10.55–10.66 | **9.41–9.59** |
| Per-case SE, benefit keys' SE appended as if independent (the published method) | 10.98–11.07 | 9.86–10.00 |
| Per-case SE, all positively correlated | 17.65–18.09 | 15.89–16.36 |
| CPS block, joint | 8.42–8.57 | 7.62–7.86 |
| CPS keys of the account alone | 8.87–8.99 | 8.08–8.27 |
| of which the capital return's own CPS part | 0.20–0.35 | 0.20–0.34 |
| of which rental assistance and the enterprises | 0.44–0.46 | 0.75–0.78 |
| of which the receipt responses | — | 0.07–0.08 |
| Benefit keys' own replicate SE | 1.20–1.23 | 1.34–1.38 |
| Their correlation with the account's CPS deviation | −0.43 to −0.40 | −0.42 to −0.37 |
| Production term | 0.74–1.12 | 0.68–1.03 |
| School correction | 2.07–2.29 | 2.07–2.29 |
| MEPS donors | 5.88–5.89 | 4.98–4.99 |
| Pension accrual held fixed, combined (CPS block) | — | 9.85–10.10 (8.15–8.47) |
| Generic rule on social_security's own key, combined (CPS block) | — | 10.51–10.59 (8.94–9.05) |
| 95% intervals of the 64 specifications, union | 300.9–408.1 | 352.6–453.3 |
| At the correlated upper bound | 286.5–422.1 | 339.4–466.1 |
| With the benefit keys appended as if independent, union | 300.1–408.9 | 351.8–454.2 |
| Uncorrected model at the adopted responses, SE (control; no benefit keys) | 12.26–12.33 | 12.27–12.34 |

[CALCULATION: `sept24_specs.cjs` → `derived/sept29/spec_costs.csv`, `line_targets.csv`, `benefit_factors.csv`;
`propagate.py --case sept29` → `derived/sept29/case_uncertainty.csv`, `derived/sept29/summary.json`; the September 27
column from `derived/sept27/`; the Part A alternative from a scratch copy of `propagate.py` with no fixed dollars on
the Medicare line.]

The CPS block falls $0.7–0.8bn against September 27. On social_security's own key (the generic rule) it would be
$8.94–9.05bn, $0.5bn above September 27; the accrual rule takes $1.2–1.3bn off that, and holding the accrual fixed takes
$0.6–0.8bn. With the accrual at ratio_net of the receipts, about 3% of the employee and employer OASDI receipts'
deviation survives on the replicates. The MEPS SE falls $0.9bn because 37.5% of the Medicare line leaves the
MEPS-keyed amount; the scratch run above shows that this rule decides it. The rental and enterprise part rises
because rental assistance's key now also carries public housing's operating deficit (0.828 of the line's national
total) and its capital derivative (0.153–0.229). Its weight on the replicates is 1.98–2.06 against September 27's 1,
and the benefit keys' rental change carries the same weight.

**No error model here:** the Part A accrual's count of covered workers; the state-price lines' key shares (each line
is a national gap times the parent line's key share, and that share's replicate error is not carried; the parent
line's own error is); roads by miles (a mileage key); the payload's constants (ratio_net, part_a_share, the accrual,
the benefit tax); and everything the September 27 section lists. The same caveat holds: the SE is a partial sampling
approximation, not a bound in either direction.

Log (times from `date`):
- 2026-09-29 17:03 JST: brief read; stub written. Files in scope: `sept24_specs.cjs`, `later_cases.json`,
  `propagate.py`, `test_uncertainty.py`, this section, `derived/sept29/` (new).
- 2026-09-29 17:13 JST: gate 1 baseline (run before any edit): `rerun_lane.py` with `node {lane}/sept24_specs.cjs`,
  `propagate.py --case sept24|sept26|sept26_schools|sept27` and `audit.py`: IDENTICAL, 38/38 files, rc 0 (61 s).
- 2026-09-29 21:09 JST (the lane, resumed after the machine rebooted at about 20:51). Fork B stopped at the usage
  limit partway through `propagate.py`. Before the reboot the lane finished that edit (the rebuild block and the
  per-case deviation block, as the four rules above describe) and wrote this section; its final gates were running
  when the machine went down, and their logs were lost, so every gate was rerun and printed. The five pre-reboot files
  in `derived/sept29/` all parse. A fresh `sept24_specs.cjs` and `propagate.py --case sept29` (21:04) wrote all five
  byte-identical to them. The run's own gates pass: the payload model rebuilds the case lane's `per_spec.csv`, and
  the specifications span `main_case` $371.4146–434.8410bn exactly (1e-9). Gate 1: the old commands above,
  IDENTICAL 43/43, rc 0; the five more files than the 17:13 baseline are `derived/sept29/`. Gate 4: two passes with
  `propagate.py --case sept29` added, IDENTICAL 43/43, rc 0 each (21:04–21:09). No tracked file in `derived/`
  differs from HEAD. pytest: 17 passed. Every figure in the table above matches the fresh outputs.

## Coverage: what carries uncertainty and what does not

**Carries sampling or donor error:**

- **CPS sampling on 30 receipt keys and 52 spending keys, plus the household pool fraction, jointly.** This covers every direct-receipt row, every household-transfer row and six of the seven service categories.
- **MEPS donor error on the five payer means** that split Medicare, Medicaid/CHIP, VA, TRICARE and health services.
- **The published CPS SE of the production term** (P + F).
- **The published sampling error of the school-enrollment correction**, applied to the education key as a relative error.
- **From the September 27 case, the administrative benefit keys' re-keying factors** (SNAP, WIC, TANF, UI and rental assistance), on the same CPS replicates as the account and jointly with it.

**Does not carry uncertainty, and why:**

- **The education-mix and postsecondary keys ($199.6bn / $193.4bn of education services, $9.0bn of education benefits) carry only partial sampling error.** These keys come from an aggregate school/postsecondary export. Only the enrollment correction's SE is published, so sampling error in the base school incidence is missing. If that base had a relative SE like the age-5–24 key (1.2%), it would add about $2.4bn at full response. [INFERENCE; not added]
- **BEA national totals are fixed.** They are administrative accounts; revision risk is not sampling error, and none was invented.
- **The outside-CPS residents' equal-cost closure** (0.99005 pool fraction) is an assumption with no error model.
- **The key-choice arms are not given an error model:** preferred versus alternative spending keys, receipt conventions and the high-AGI federal allocation. These are model uncertainty with no probability distribution, and they are shown as spans in §4.
- **The response parameters are arms:** CBO 0.63/0.66, the school share 0.715/0.865, delayed and non-school responses, and the capacity path. CBO's coefficient SEs are not in the repository.
- **CES parameters (σ, labor share), hours response, capital-tax retention and ownership** are arms. ε is a sensitivity only.
- **The covariance between the production term and the fiscal keys, and between the school supplement and ASEC, is unknown.** The ρ = +1 envelope bounds the represented sources' combined SE from above, taking each source's SE as given. The independent result can sit above the true SE as well as below it: a negative covariance lowers the SE, as the benefit keys' does (September 27 section). [Revised 2026-09-27; see Revisions.]
- **The pooled medical translator's sampling error** ($8.039bn before LTSS and package scaling) shares 2024 MEPS donors with the donor base carried here. It is neither added independently nor modelled jointly; the medical bridge's error is unresolved (September 27 section).
- **Nonsampling error** is not propagated: survey underreporting and coverage bias, MEPS age/birth transport to Mexican-origin people, and missing capital gains. It is bias, not variance.
- **Lifetime, lineage and ledger SEs** measure other objects and are catalogued in `se_catalog.csv`, not combined.

[FRAMING-SENSITIVE] Every interval here is conditional on the account's beneficiary definition (other US residents, β = 1) and on the stationary with-versus-without comparison. It is a sampling interval for a conditional model quantity, not a confidence interval for a causal policy effect. This analysis was produced by an LLM on a politically charged topic; see `notes/llm-bias-caveat.md`.

## Revisions

- **2026-09-27 — the sampling SE is an approximation, not a bound.** The conceptual audit (research/immigration-conceptual-audit-2026-09-27.md,
  section A) showed that one omitted source, the administrative benefit keys, is computed from the same CPS
  replicates as the account and correlates with it at about −0.4, so an omitted covariance can leave the SE too
  high as well as too low. The 2026-09-25 verdict bracket called the September 24 SE "a floor since most corrections carry
  ranges"; the coverage section said the unknown covariances were "bracketed by the independent result and the
  ρ = +1 envelope". Both are withdrawn: the SE is a partial sampling approximation whose net error is unresolved.
  From `sept27` the CPS block carries the benefit keys jointly (September 27 section); the files of earlier cases are
  unchanged and keep the independent append. Parent note of 2026-09-27, 23:40.
