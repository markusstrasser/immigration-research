# Brief: the Mexican-origin share of Medicaid long-term care (audit row 5)

Owner: `ltss-share` agent. Write only inside `infra/immigration-fiscal/ltss_share_2026_09_23/`.
Do not commit; the parent grades and commits. Result file: `RESULT.md`, first line
`**Verdict:** …`.

## Why

The complete account spreads BEA Medicaid ($954.2bn, CY2024) by a MEPS community-population key
(five age bands × US/not-US birth). Long-term services and supports (LTSS) are therefore charged
to the Mexican-origin group (the CPS ASEC 2025 union, 40.9M) at its community-key share, 12.3%.
MEPS covers 38% of BEA Medicaid, and it excludes nursing-home residents. The dataset integrity audit
(`dataset_integrity_2026_09_23/spending.md` #3, `README.md` row 5) bounds the error at −$3.6bn to
−$15bn, assuming a true group share of 4–8%. That bound is the largest unmeasured row in the audit.

## Question

What share of Medicaid LTSS spending (institutional and home- and community-based separately) goes
to the Mexican-origin group (or to Hispanics, translated with a stated factor) in 2022–2024? What
does charging the LTSS part at that share, instead of the community key, do to the main case of
$203.2–249.6bn?

## Method

1. **Gate.** Reproduce the audit's bound (−3.6 to −15 at 4–8%) from the account's own files:
   `full_account_spending_2026_09_20/builder.py`, its `derived/incidence_keys.csv`, and how
   Medicaid is keyed. Record the group's current dollar share of Medicaid.
2. **Published tables.** Read the primary PDFs and quote each number with its page:
   - Mathematica/CMS *Medicaid LTSS Users and Expenditures* reports (2019–2022; look for tables by
     race and ethnicity, with users and spending, institutional vs HCBS);
   - the CMS Nursing Home Data Compendium or MDS resident counts by race and ethnicity;
   - LTCFocus;
   - MACPAC or KFF LTSS by race and ethnicity.

   Record for each whether it is Hispanic or Mexican, and whether it counts users or dollars.
3. **Local measurement.** ACS 2024 1-year PUMS residents aged 65+ in institutional group quarters
   (`RELSHIPP` 37), where nursing homes dominate, by `HISP`=02 (Mexican) and `POBP`=303
   (Mexico-born), against all residents. Slim parquet extracts are in
   `dataset_integrity_2026_09_23/_cache/acs_person_20{17..24}.parquet`; the columns are listed in
   `dataset_integrity_2026_09_23/acs_extract.py`. Weight with `PWGTP`. ACS group-quarters records
   are about half whole-person donor copies (audit `acs.md` F1), so do not compute SEs from record
   counts.
4. **Translation.** Carve the LTSS dollars out of the MEPS-keyed pool. Charge institutional LTSS at
   the measured share. Charge the HCBS part MEPS misses at the measured HCBS share, or bound it if
   no share is found. Report the change in the main case, low / central / high.
5. **Coordination.** `medical_ethnicity_pooled_2026_09_23` (running, another agent) re-keys the
   account's medical lines by pooled MEPS ethnicity ratios within age × nativity cells. Do not edit
   its files. State the combining rule: its ratios apply to the community part only, and your
   correction applies to the LTSS part only. Give the joint effect if its `derived/` outputs
   already exist.

## Output

`RESULT.md` should open with the verdict: the shares, the $bn effect and its range, and the
combining rule. Follow it with:
- a source table graded by evidence level;
- the gate result;
- the translation;
- disconfirmation: what would make the share higher.

Put scripts in the lane directory and outputs in `derived/`. Tag claims `[SOURCE: …]`, `[DATA: …]`,
`[CALCULATION: …]` or `[INFERENCE]`.

## Validation

- The gate reproduces the audit bound.
- Rerun every script and show that the `derived/` outputs are byte-identical (md5 before and after).
- Every published number used in a calculation is parsed from the primary PDF or table, not from a
  search summary. Firecrawl schema extraction has fabricated tables before.

## Constraints

- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project [--with pkg] python3 <script>` from
  the repository root.
- Never print API keys. Census keys live in `infra/immigration-fiscal/acquire/config.local.env`;
  pipe any Census API output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
- Microdata stays in `_cache/` or `sources/`.
- No edits outside this directory.
- Stop after about 12 turns of source search and report what you have.
