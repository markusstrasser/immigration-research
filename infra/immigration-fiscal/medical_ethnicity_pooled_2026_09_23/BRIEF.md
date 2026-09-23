# Pooled MEPS: does the account charge the group the right public medical dollars?

Date: 2026-09-23. Operator: "Any other in our analysis we could get a better answer on (not
rounding errors but actual bigger conceptual wrongtakes?)"

## Why

The generation ledger and the complete annual account charge each CPS record the weighted mean
public-payer medical spending of MEPS donors in its age band × US-birth cell
(`donor_model(medical, d, False)` in `ledger_absolute_2026_09_17/absolute_ledger.py`). The
account's preferred Medicaid/CHIP/other medical charge to the group is $116.91bn
(`research/immigration-complete-annual-account-2026-09-20.md`, "The largest spending move"). The
cell ignores ethnicity. Evidence so far:

- MEPS 2024 alone (`meps_mexican_origin_medical_2026_09_22`, ladder 175): Mexican-origin people
  draw 0.69 (SE 0.10) of their cell's public dollars at 18–64 and 0.89 (0.15) at 65+. One child
  record carried 68% of the 0–17 Mexican-origin mean, so no all-ages translation exists, and two
  of ten cells exclude one in opposite directions.
- MCBS 2023 (`mcbs_elderly_medical_2026_09_22`, ladder 173): Hispanic 65+ public payments are
  1.27× whites'.
- Keying Medicaid by reported coverage instead of expected dollars adds $68.7bn.

The sign and size of the ethnicity dimension are open, and it is worth tens of billions either
way.

## Task

1. **Pool MEPS full-year consolidated files 2016–2024** (HC-192, 201, 209, 216, 224, 233, 243,
   251, 256). 2023 and 2024 are held under `sources/immigration-fiscal/data/external/stage3/ahrq/`;
   fetch the rest from meps.ahrq.gov into the lane's `_cache/` and pin URL, size and sha256. Use
   the ledger's public-payer definition, age bands and US-birth split exactly. Before pooling,
   reproduce the 2024 lane's ratios as a gate. Deflate to 2024 dollars and name the index. For
   pooled variance use MEPS's pooled linkage file (HC-036 or its successor) and divide weights by
   the number of years.
2. **Ratios by cell.** For each transport cell, the Mexican-origin mean divided by the all-donor
   mean. Verify the Hispanic-category codes year by year (`HISPNCAT` or its predecessor). Compute
   it three ways: plain weighted means; means winsorized within cell at the 99.5th and 99.9th
   percentiles; and a two-part model (any public spending × mean when positive). Report by payer
   (Medicare, Medicaid, other public), with year-by-year stability; flag 2020–21.
3. **Translate onto the union's cells.** Give the change in the ledger's public medical charge
   and in the complete account's preferred Medicaid/CHIP/other medical ($116.91bn) and Medicare
   lines, in $bn with SEs. Use the account's own allocation files
   (`full_account_spending_2026_09_20/derived/allocations.csv`, the benefits builder), and say
   which account line each payer maps to.
4. **Reconcile 65+ with MCBS.** MEPS is Mexican-origin and community-dwelling; MCBS is Hispanic
   and includes facility stays in its cost supplement design. Say how the account charges
   nursing-home Medicaid, and whether leaving institutions out of MEPS biases the ratio.
5. **Disconfirmation.** State the strongest case that the group draws more than its cell:
   Medicaid coverage of 26% against 12% at 65+, uninsured use, and emergency Medicaid for the
   unauthorized, which MEPS may miss. Say whether the pooled data rule it out.

## Rules

- Do not edit any fingerprinted `.py` in `ledger_absolute_2026_09_17` or
  `gen_ledger_extension_2026_09_16`; their consumers verify hashes and stop with `[BLOCKED]`.
  Import or copy logic into the lane instead.
- **Deliverables.** `RESULT.md` opening with `**Verdict:**`, containing:
  - the per-cell table with SEs;
  - the $bn translation for the ledger and the account, with SEs;
  - every specification computed;
  - limits.
- Scripts and `derived/*.csv` aggregates only; raw files go in `_cache/` (add a `.gitignore`
  with `_cache/`).
- Run with `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root.
- Write only in the lane directory. Do not commit.
