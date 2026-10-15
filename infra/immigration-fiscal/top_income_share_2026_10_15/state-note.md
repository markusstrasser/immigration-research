**Verdict:** A California-only administrative income-distribution correction lowers the union's national state-income-tax key from 5.004426% to 4.636048%. Replacing California's upper-bin union shares with pooled shares then raises it to 4.671005%. This is a covered-state sensitivity with explicit transport assumptions, not a measured national correction. [CALCULATION: `state_correction.py`; `derived/state_arms.json`]

Validation: exact raw CPS state share agrees with the case's rounded personal key within 1e-9; four tests pass; both state outputs reproduce byte for byte with LF endings. The state process took 0.140 seconds and peaked at 34,553,856 bytes by Python `resource.getrusage` on the successful reproduction. Log: 2026-10-15 11:01:09 JST (`date`).

Covered: `state_correction.py`, `test_state_correction.py`, `derived/state_arms.json`, `derived/state_ftb_extract.csv`, and this note. Skipped: nationwide state administrative raking, state replicate SEs, and direct identification of California AGI on CPS. The federal machinery and final case translation belong to the parent task.

The primary source is the [California FTB Department of Finance Spring 2025 exhibits](https://publish.data.ca.gov/dataset/1555a2c4-740a-4b1c-adf1-1ab7721e90b3/resource/ee16e82e-c2cf-4900-b6c6-121ded321241/download/dof_spring_2025_odp.pdf), PDF page 15, Exhibit A-10 page 5 of 5, resident returns, TY2023 preliminary statistical sample. Its table labels the amounts as millions of dollars. `derived/state_ftb_extract.csv` preserves each extracted source row, including the total. The source bytes are pinned by SHA-256 `8d1aaffd9e4a1f7dc63c4dd9d11781a7f1a1b840d67aedfe0495f27bb104f9a9`; the script checks the hash, table identity, row count and $97,083m sum. [SOURCE: linked FTB exhibit]

| California AGI class | TY2023 liability, $m | Share of California liability |
|---|---:|---:|
| Under $20k, including losses | 40 | 0.0412% |
| $20k–50k | 1,126 | 1.1598% |
| $50k–100k | 6,272 | 6.4605% |
| $100k–200k | 15,956 | 16.4354% |
| $200k–500k | 26,145 | 26.9306% |
| $500k–1M | 14,950 | 15.3992% |
| $1M+ | 32,594 | 33.5733% |

[SOURCE: FTB exhibit; CALCULATION: each amount / $97,083m. Printed percentages are rounded.]

The case's state key uses positive `STATETAX_A`, on each personal carrier, with published CPS weights. The baseline union share is 0.050044257862512154, matching `assumption_explorer_2026_09_21/derived/model.json`'s personal `state_local_income_tax` key, 0.050044258. California accounts for 18.595362% of raw national CPS state liability. This California national mass stays fixed; all other states' total and union contributions stay fixed. The national NIPA line stays $536.167bn. The parent applies the case's own stack and endpoint machinery to the changes in shares. [DATA: `derived/cps_state_bins.csv`; `derived/state_arms.json`; model receipt line]

The correction replaces California's within-state bin masses with FTB's liability shares. California CPS federal AGI is used as a proxy for California AGI; California resident-return liabilities proxy its residence-based CPS liability distribution. These bridges are assumptions. They do not identify the distribution of nonresident liabilities, local income taxes, or all-state PIT. The TY2023 administrative shape is also transported to the case's income year 2024. The source is a preliminary tax-return sample, not a full final return census. [SOURCE: FTB exhibit and B-3 dictionary; INFERENCE: transport assumptions]

There are no CPS positive California state-liability dollars under $10k in either the baseline or pooled sample. The script therefore pools under-$20k classes explicitly. It fails on any unsupported remaining class; it does not invent the missing under-$10k union share. This coarse pooling affects only $40m of the source's $97,083m. Below $200k, all arms retain the baseline union shares within the resulting common classes. [DATA: `derived/cps_state_bins.csv`; CALCULATION: `state_correction.py`]

| Arm | National key, % | Change from raw national key, percentage points | Change from CA admin control, percentage points |
|---|---:|---:|---:|
| current, raw CPS | 5.004426 | 0 | +0.368378 |
| current_CA_admin | 4.636048 | −0.368378 | 0 |
| carry_500k | 4.825060 | −0.179366 | +0.189012 |
| fixed_1_5pct | 4.456857 | −0.547568 | −0.179190 |
| pooled_top_only | 4.770919 | −0.233506 | +0.134872 |
| pooled_unconstrained | 4.671005 | −0.333421 | +0.034957 |
| pooled_monotone_central | 4.671005 | −0.333421 | +0.034957 |

[CALCULATION: `derived/state_arms.json`; no stack multiplier applied here.]

California's current upper-bin union shares are 10.3067%, 7.3978%, and 4.3702%; the pooled real-2023 shares are 9.0409%, 6.1223%, and 6.5306%. The last bin has only 2 union liability records in the baseline and 22 across pooled years. This contradicts any claim that pooling necessarily lowers the state top share. Pooling also mixes years, tax rules, composition and sampling variation; it is not an identified population trend. [DATA: `derived/cps_state_bins.csv`; CALCULATION: `derived/state_arms.json`]

The central arm fits the pooled shares above $200k to a non-increasing sequence with administrative liability weights: 9.0409%, 6.4022%, 6.4022%. Weighted isotonic fitting preserves the weighted mean of every merged block, so its aggregate matches the unconstrained pooled arm exactly. This equality is an accounting property, not independent empirical confirmation. `carry_500k` carries California's baseline $500k–1M share to $1M+; the 1.5% arm is imposed on California's $1M+ state-liability share. Federal and state union shares are estimated separately. [CALCULATION: `state_correction.py`; `derived/state_arms.json`]

The [B-3 public CSV](https://publish.data.ca.gov/dataset/b-3-adjusted-gross-income-with-accumulated-percentages) was inspected but rejected as the central administrative shape: its download filename begins `2023`, yet the newest taxable year actually present is 2022. Its dictionary confirms California AGI and resident-return liability as the objects. IRS Historic Table 2 federal liabilities and capped itemized SALT deductions are not used as state tax liabilities. [SOURCE: `_cache/state/ftb_b3.csv`; `_cache/state/ftb_b3_dictionary.pdf`; linked official dataset]

Reproduce after `pool_cps.py` has generated `derived/cps_state_bins.csv`:

```sh
uv run --no-project python3 infra/immigration-fiscal/top_income_share_2026_10_15/state_correction.py --fetch
uv run --no-project python3 -m pytest infra/immigration-fiscal/top_income_share_2026_10_15/test_state_correction.py -q
```

`--fetch` only downloads a missing pinned PDF (under 1MB); an existing source with different bytes fails. `pdftotext` must be installed. `--out-dir <scratch>` writes reproducible state outputs elsewhere. Timing and physical-memory readings are printed to stdout, excluded from derived outputs.
