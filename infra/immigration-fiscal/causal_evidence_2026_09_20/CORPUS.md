# County outcome staging for future causal designs

**Verdict:** Validated descriptive inputs, not a causal estimate. The bundle copies 72.12 MB of corpus CSVs and adds official IRS codebooks; the full staged run is about 80 MB. No files are moved or deleted. The committed `SOURCES.json` pins all 23 acquired inputs. Machine-local source paths and checks are in `raw/county_outcomes/manifest.json`.

Run (macOS `textutil` plus Python/pandas):

```sh
uv run python3 stage_corpus.py --corpus-root /Volumes/2TBPNY/corpus --out raw/county_outcomes --codebooks-root raw/county_outcomes/codebooks
uv run python3 verify_corpus.py --out raw/county_outcomes
uv run python3 test_verify_corpus.py --bundle raw/county_outcomes --source-lock SOURCES.json
```

The ignored codebook directory contains all 11 official guides. On a fresh acquisition, the script can recover 2013-2022 guides from valid corpus archives; `--fetch-codebooks` retrieves the small 2011 guide if absent. Copies are hashed, existing differing bytes are rejected, HTML-as-CSV and invalid archives fail loudly, and the complete output is capped at 10 decimal GB (`--max-bytes` may lower but not raise this limit). Source CSV structure, documented units, numeric tokens and joins are validated before copying their payloads. Output CSVs are derived, not source records. Data availability depends on the external corpus or reader acquisition from the official URLs; raw files are not committed or redistributed here.

## Data and units

- BEA CAINC4: official route https://apps.bea.gov/regional/zip/CAINC4.zip. Actual table metadata says **Number of persons** for population and **Thousands of dollars** for all monetary fields used. Monetary outputs multiply by 1,000 and preserve nominal year dollars. Full source has 1969-2024 columns; this joined panel uses 2011, 2013-2022.
- IRS county income: https://www.irs.gov/statistics/soi-tax-stats-county-data. Selected data files `YYincyallnoagi.csv` have total (`AGI_STUB=0`) rows; "noagi" means no AGI-size classes, not no AGI amounts. Actual yearly `YYincydocguide.doc[x]` guides confirm money is **thousands of dollars**. `A00100` is AGI, `A00200` wage/salary income, `A06500` the recorded income-tax measure. Pre-2018 guides label A06500 "Income tax amount"; later guides explicitly label it "Income tax after credits amount". All codebook labels are retained in manifest; output uses the code-bearing neutral name `irs_income_tax_A06500_dollars`. It is not net federal revenue after refundable credits or all taxes.
- Dollar unit multiplication is separately checked against staged original values by `verify_corpus.py` (no import of staging functions).
- Source text is CP1252: BEA and IRS 2011/2013/2021/2022 have non-UTF8 characters; other selected IRS files are ASCII. Output is UTF8. This mapping is explicit, never an unreported fallback.

## Geographic/time coverage and missing values

The panel uses only 50-state/DC five-digit FIPS with a nonzero county component below 900. BEA Virginia 900-series combined county/city areas are preserved in a separate exclusion file, not incorrectly joined to individual IRS counties. Connecticut's changed county equivalents, Alaska changes and obsolete codes remain explicitly unmatched; no guessed crosswalk or interpolation is applied. `join_coverage.csv` separately reports key matches and matches with usable outcome values. An exact FIPS match is not sufficient to establish constant historical boundaries.

**2012 is missing** in the selected corpus and is not interpolated. Different variables have different suppression and coverage. BEA `(NA)` and other recognized suppression tokens become missing and are counted. Negative residence adjustment/net earnings or AGI can be meaningful and are retained; nonnegative measures fail on negative numbers. For IRS a zero amount with zero corresponding returns is flagged and conservatively left missing, because a true zero cannot be distinguished from disclosure exclusion. Positive cells can also omit protected amounts; these are published aggregates, not a complete administrative universe.

The output has no ethnic origin, nativity, legal status, policy treatment or victim/offender link. Tax-return ZIP-derived geography/filing windows differ from BEA residence/workplace/year concepts. Do not subtract transfers from tax liability and call the difference a causal fiscal cost. Total BEA transfers include government benefits and net business transfers; IRS income tax excludes several tax categories and refundable credits.

## Diagnostics and artifacts

`county_year_outcomes.csv` preserves both unmatched directions; `unmatched_geographies.csv`, `bea_combined_geographies_excluded.csv`, and `ambiguous_zero_cells.csv` explain exclusions. `national_sum_diagnostics.csv` compares all available county sums and matched-county sums with BEA national totals or same-file IRS state totals. Differences are coverage/definition diagnostics, not ethnicity effects. Summed residence adjustments may be signed and near zero; their ratios are not informative coverage rates.

In the validated run, each year has about 3,087-3,091 FIPS key matches; exact usable-value counts are in coverage. County-only BEA population sums cover ~98.9% of the published national total because combined geographies are omitted. In 2022 the matched-only population share is lower (~97.8%) because of unmatched geography. Do not claim complete national coverage.

Within `raw/county_outcomes/`, `verification.json` records hash and direct-value checks; `output_hashes.json` records derived CSV hashes. The September 20 corrected verifier passed 583,225 source value/label/flag comparisons, 590,461 missingness checks, 23 locked input hashes and six output hashes, producing 34,733 county-year rows. All raw and derived payloads remain ignored; generators and source provenance are committed.

Review exposed an incomplete earlier verifier: it could miss a deleted year, masked populations or corruption in unchecked earnings fields. The replacement independently reconstructs the entire source county-year union and checks every exported field. Ten deliberately corrupted bundles must fail, including when Python assertions are disabled; the regression runner exercises those failures without changing source bytes. Its case dictionary is the local failure catalog.

## Other corpus candidates

The bounded inventory also inspected IRS migration, older county-income archives,
QCEW, county population, CBP, LODES, mortality and EOIR files. Older IRS2005–2010
archives could supply additional pre-policy years but need separate schema work;
similarly named archives include HTML error pages. Migration flows are useful only
with a selected displacement question. Recent QCEW/LODES files add little to the
longer panels already held. Public mortality data do not supply offender identity
or the needed recent county geography. The inspected large EOIR ZIP failed its
central-directory check. None was copied speculatively. No confirmed new NCVS,
NIBRS/UCR/SHR or policy-activation file emerged from this inventory.
