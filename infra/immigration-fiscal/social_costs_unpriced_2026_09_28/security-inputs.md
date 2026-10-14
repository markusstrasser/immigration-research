**Verdict:** Primary Census customer shares identify household and business payers in all five security-service industries. Use those shares on the retained SAS revenue base, keep government purchases separately excluded, and declare nonprofit pass-through as an assumption. Residential product categories describe buildings and must not replace the customer split. In-house guards and direct equipment still require allocation assumptions. [CALCULATION: `security_inputs.py` → `derived/security_inputs.json`] [ASSUMPTION]

Scope: NAICS 561611, 561612, 561613, 561621 and 561622. Own new `security_inputs.py`, `inputs/security*`, `_cache/security*`, `derived/security_inputs*`, and this note. Existing producers and peer work were not edited.

## Primary evidence and schema

The [2022 Economic Census security questionnaire](https://bhs.econ.census.gov/ombpdfs2022/export/2022_AS-56160_mu.pdf), item 20 (PDF page 14), asks for operating-receipt shares by business firms/farms, nonprofits, federal government, state/local government, and household consumers/individuals. Sole proprietors belong to firms. This identifies the payer rather than a residential versus nonresidential building. Item 22 (PDF pages 16–18) separately identifies residential/nonresidential monitoring and installation/repair products. [SOURCE: linked questionnaire]

Downloaded primary tables, exact source bytes pinned in `inputs/security_pins.json`:

- [`2022/ecnclcust`](https://api.census.gov/data/2022/ecnclcust.html): `NAICS2022`, `CLASSCUST`, `CLASSCUST_LABEL`, `RCPTOT`, `RCPTOT_DIST`, their flags, and `CLASSCUST_COV/F`. National `us:1`, all operations `TYPOP=00`, all tax statuses `TAXSTAT=00`. `CLASSCUST=001` is the total; `5045` households, `514` firms, `570` nonprofits, `515` federal, `516` state/local. The individual-class `RCPTOT` values are not applicable (flag `X`): their zero placeholders are never treated as actual dollar revenue. Parse `RCPTOT_DIST` to allocate the total. [SOURCE: primary API schema and downloaded rows]
- [`2022/ecnnapcsind`](https://api.census.gov/data/2022/ecnnapcsind.html): `NAPCS2022`, `NAPCS2022_LABEL`, `NAPCSDOL/F`, `NAPCSDOL_CV`, `NAPCSDOL_IMP`, `LINEALL_PCT`, `LINEALL_PCT_SE`. Dollars are thousands of nominal 2022 dollars. All-industry product totals equal customer-table industry totals. Selected distinct product codes: residential monitoring `7000550000`, residential installation/repair `7000575000`, nonresidential monitoring `7007475000`, nonresidential installation/repair `7007500000`. Other products remain unclassified for building type. [SOURCE: primary API schema and downloaded rows]
- Retained revenue: existing Census SAS files distributed by [FRED](https://fred.stlouisfed.org/series/REVEF561612ALLEST), `REVEF<NAICS>ALLEST`, exactly the `2022-01-01` row. Copies are separately pinned; values are parsed from those CSVs. The Economic Census revenue totals are exposed beside the SAS totals and are not substituted. Applying the Economic Census payer mix to the SAS base is an explicit source-bridge assumption. [DATA: `inputs/security_fred_*.csv`] [ASSUMPTION]

The query parameters, without the credential, are recorded in the pin manifest. Each industry is requested separately: an initial comma-separated industry query returned a non-JSON response. The credential and exception URLs are redacted. The old `ec2022_5616.json` was not used. [CALCULATION: acquisition log]

## Import API and accounting boundary

`load_security_inputs()` returns a dict keyed by the six-digit NAICS string. Every entry includes `revenue_m_2022`, `ec_revenue_m_2022`, `residential_share`, `commercial_share`, `business_share`, `nonprofit_share`, `federal_share`, `state_local_share`, `government_share`, and `private_share`. All shares use **total industry receipts** as denominator. `residential_share` means household/individual payer. `commercial_share = business_share + nonprofit_share`; the nonprofit pass-through premise is separately tagged and callers can instead use `business_share` alone. `private_share = residential_share + commercial_share`. [CALCULATION: `security_inputs.py:load_security_inputs`]

Split conservation is `residential + commercial + government = original SAS revenue`; government is retained as its own record, not silently renormalized out. Excluding government purchases from private-security costs prevents an assumed overlap with security purchases in the fiscal account. This acquisition does not audit which exact fiscal lines contain those purchases. [CALCULATION] [ASSUMPTION] [GAP: exact fiscal overlap not identified]

Each record also exposes `residential_product_m_2022`, `nonresidential_product_m_2022`, their shares of the Economic Census industry total, the product codes actually published, and the unclassified product remainder. Those products are monitoring and installation/repair, not all revenue and not payer classes. [DATA: `derived/security_inputs_ecnnapcsind.csv`]

In-house guards lie outside this contracted-service customer inquiry. Direct purchases of equipment also lack an identified household/business split here. The JSON marks both as `[ASSUMPTION REQUIRED]`; it supplies no measured split for either. These sources do not measure which payer's spending is crime-induced or by which offender group. [GAP] [ASSUMPTION]

## Gates and limits

Five industries close to their original national SAS totals at `1e-6bn` or tighter; all customer fractions close to one at `1e-12`; product and customer Economic Census totals agree at `1e-9` million dollars. Every normal load verifies all 17 SHA-256 pins. Schema, scope, duplicate keys, suppression flags, missing categories and negative/nonfinite values fail closed. [CALCULATION: `security_inputs.py --check`]

Ten failure regressions cover HTML under a `.json` name, non-table JSON, bad row widths, contradictory duplicate columns, wrong NAICS, `X/D/N` flagged estimates, a usable published small-product estimate (`s`), and stale input hashes. Only temporary copies are mutated by these checks. [CALCULATION: `security_inputs.py:check_failures`]

Customer percentages have no published sampling-error estimate in this table according to the [2022 Economic Census methodology](https://www.census.gov/programs-surveys/economic-census/year/2022/technical-documentation/methodology.html), section “Sample-based estimates with no associated measurement of sampling error,” EC2200CLCUST. No replicate SE is manufactured. The coverage values contain coded flags rather than exact percentages; raw flags are retained and the placeholder zeros become JSON null. [SOURCE: methodology] [DATA: `customer_coverage_flag`]

## Reproduction and log

Normal, offline computation: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/security_inputs.py --check`.

Fresh acquisition: run the same script with `--probe`, then `--acquire --pin-inputs`. This deliberately refreshes the source manifest; normal computation never repins changed bytes. Fresh acquisition needs the Census credential in the existing acquisition config; no key is written to any artifact.

Successful customer/product acquisition took 4.858 seconds and 36,847,616 bytes peak RSS; the checked offline build took 0.018 seconds and 30,670,848 bytes peak RSS, measured with `time.perf_counter` and `resource.getrusage`. [CALCULATION: process receipts]

Parent owns the full lane `rerun_lane.py` check, including the security command above. No merge, stage, commit, source deletion or changes outside assigned paths occurred.

Closeout clock: 2026-10-14 21:37:17 JST (`date`). The checked command exited 0; source compilation also passed. All table numbers below are mechanically rendered from the derived JSON.

## Parsed customer shares and retained revenues

Percent of all receipts; revenue in million nominal 2022 dollars. [DATA: `derived/security_inputs.csv`]

| NAICS | SAS revenue | EC revenue | Household | Firms | Nonprofit | Government |
|---|---:|---:|---:|---:|---:|---:|
| 561611 | 7,850.000 | 6,154.657 | 3.5% | 75.6% | 4.9% | 16.0% |
| 561612 | 32,222.000 | 37,044.039 | 3.7% | 68.8% | 4.1% | 23.4% |
| 561613 | 4,162.000 | 3,605.043 | 1.1% | 95.9% | 1.8% | 1.2% |
| 561621 | 28,295.000 | 31,313.513 | 55.3% | 34.9% | 2.6% | 7.2% |
| 561622 | 2,701.000 | 2,626.866 | 29.3% | 51.7% | 8.9% | 10.1% |

## Every changed path

- `__pycache__/security_inputs.cpython-313.pyc`
- `_cache/security_ecnclcust_2022.json`
- `_cache/security_ecnclcust_561611_2022.json`
- `_cache/security_ecnclcust_561612_2022.json`
- `_cache/security_ecnclcust_561613_2022.json`
- `_cache/security_ecnclcust_561621_2022.json`
- `_cache/security_ecnclcust_561622_2022.json`
- `_cache/security_ecnclcust_variables.json`
- `_cache/security_ecnnapcsind_2022.json`
- `_cache/security_ecnnapcsind_561611_2022.json`
- `_cache/security_ecnnapcsind_561612_2022.json`
- `_cache/security_ecnnapcsind_561613_2022.json`
- `_cache/security_ecnnapcsind_561621_2022.json`
- `_cache/security_ecnnapcsind_561622_2022.json`
- `_cache/security_ecnnapcsind_variables.json`
- `derived/security_inputs.csv`
- `derived/security_inputs.json`
- `derived/security_inputs_ecnclcust.csv`
- `derived/security_inputs_ecnnapcsind.csv`
- `inputs/security_ecnclcust_561611_2022.json`
- `inputs/security_ecnclcust_561612_2022.json`
- `inputs/security_ecnclcust_561613_2022.json`
- `inputs/security_ecnclcust_561621_2022.json`
- `inputs/security_ecnclcust_561622_2022.json`
- `inputs/security_ecnclcust_variables.json`
- `inputs/security_ecnnapcsind_561611_2022.json`
- `inputs/security_ecnnapcsind_561612_2022.json`
- `inputs/security_ecnnapcsind_561613_2022.json`
- `inputs/security_ecnnapcsind_561621_2022.json`
- `inputs/security_ecnnapcsind_561622_2022.json`
- `inputs/security_ecnnapcsind_variables.json`
- `inputs/security_fred_REVEF561611ALLEST.csv`
- `inputs/security_fred_REVEF561612ALLEST.csv`
- `inputs/security_fred_REVEF561613ALLEST.csv`
- `inputs/security_fred_REVEF561621ALLEST.csv`
- `inputs/security_fred_REVEF561622ALLEST.csv`
- `inputs/security_pins.json`
- `security-inputs.md`
- `security_inputs.py`
