# IQ Sex Differences - Early-School Intake

**Date:** 2026-03-05
**Purpose:** lock the first executable path for the early-school-emergence node so Stage 2 starts from concrete local assets rather than generic dataset names.

This note is an intake memo, not a results memo.

---

## Verdict

The early-school order is now historical rather than prospective:

1. `NLSCYA` first
2. `ECLS-K:2011` second
3. `ECLS-K` third

Reason:

1. `NLSCYA` is the only staged early-school dataset that already gives the repo both a direct `csv` payload and a local SAS/R dictionary. [SOURCE: `sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip`]
2. `ECLS-K:2011` was blocked only by missing layout metadata; the official public-use dictionary is now local. [SOURCE: `sources/iq-sex-diff/data/ecls_k2011/ECLSK2011_K5PUF.dct`; <https://nces.ed.gov/ecls/data/2019/ECLSK2011_K5PUF.dct>]
3. the older `ECLS-K` path was the slowest because the local archive needed refreshed NCES split parts plus a concatenation-based extraction path before the full ASCII could be parsed. [SOURCE: `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`; `sources/iq-sex-diff/data/ecls_k/refresh/childk8p.dat`; <https://nces.ed.gov/ecls/dataproducts.asp>] [INFERENCE]

---

## NLSCYA

### Why it goes first

`NLSCYA` is immediately analysis-grade enough for an intake pass because it ships:

1. `nlscya_all_1979-2020.csv`
2. `nlscya_all_1979-2020.sas`
3. `nlscya_all_1979-2020.R`

[SOURCE: `sources/iq-sex-diff/data/nlscya/nlscya_all_1979-2020.zip`]

The repo now has a focused variable map at:

- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv`
- `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`

[SOURCE: `sources/iq-sex-diff/map_nlscya_early_school.py`; `sources/iq-sex-diff/build_nlscya_early_school_extract.py`; `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv`; `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`]

### Exact intake surface already identified

The map currently gives the core spine:

1. child ID: `C0000100` / `CPUBID_XRND`
2. sex: `C0005400` / `CSEX_XRND`
3. birth year: `C0005700` / `CYRB_XRND`
4. first survey year after birth: `C0005200` / `FSTYRAFT_XRND`
5. child age at child supplement assessment: `1986` through `2014`
6. `PIAT` math raw score: identified at least in `1986` and `1992`
7. `PPVT` raw and standard scores: identified repeatedly from `1986` through `2014`

[SOURCE: `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv`]

### What this means

`NLSCYA` is already good enough to do two useful things:

1. build the repeated-wave early-school scaffolding cleanly
2. test whether early broad-score movement looks different from the later `Math Knowledge / transcript / labels` family

Constraint:

- the quick intake map shows denser repeated `PPVT` coverage than repeated `PIAT` math coverage, so the first pass should not overclaim dense annual math trajectories until the broader PIAT family is fully mapped. [SOURCE: `sources/iq-sex-diff/data/nlscya/nlscya_early_school_variable_map.tsv`] [INFERENCE]

Current artifact:

- the compact extract now contains `11,551` child rows and `46` selected early-school columns

[SOURCE: `sources/iq-sex-diff/data/nlscya/nlscya_early_school_extract.tsv.gz`] [INFERENCE from local row and column count]

---

## ECLS-K:2011

### Why it went second

`ECLS-K:2011` is now viable for a first extract because the public-use Stata dictionary is local:

- `sources/iq-sex-diff/data/ecls_k2011/ECLSK2011_K5PUF.dct`

[SOURCE: `sources/iq-sex-diff/data/ecls_k2011/ECLSK2011_K5PUF.dct`]

The shortest viable first-pass field set is:

1. `CHILDID`
2. `X_CHSEX_R`
3. `X1MSCALK5` through `X9MSCALK5`
4. optionally `X1MTHETK5` through `X9MTHETK5`
5. wave weights such as `W1C0` and `W12AC0`

[SOURCE: `sources/iq-sex-diff/data/ecls_k2011/ECLSK2011_K5PUF.dct`]

This made `ECLS-K:2011` the cleanest replication target once the `NLSCYA` intake was complete.

---

## ECLS-K

### Why it stayed third

The older `ECLS-K` local payload originally staged only:

- `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`

That archive is multipart, and the local copy alone was not enough to treat the dataset as ready. [SOURCE: `sources/iq-sex-diff/data/ecls_k/Childk8p.zip`] [INFERENCE]

The resolution path turned out to be:

1. refresh the NCES split parts
2. concatenate the multipart archive directly
3. extract the full ASCII from that concatenated archive
4. parse the public-use Stata dictionary with `_line(n)` awareness

[SOURCE: <https://nces.ed.gov/ecls/dataproducts.asp>; `sources/iq-sex-diff/data/ecls_k/refresh/childk8p.dat`; `sources/iq-sex-diff/extract_eclsk_early_school.py`] [INFERENCE]

That means the older cohort is now locally usable rather than just recoverable.

---

## Immediate Execution Order

1. Use the three current result memos as the early-school baseline:
   - `research/iq-sex-differences-nlscya-early-school-first-pass.md`
   - `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`
   - `research/iq-sex-differences-eclsk-early-school-first-pass.md`
2. Move next to score-family alignment across `NLSCYA` and the two `ECLS` cohorts.
3. Only after that, decide whether another child cohort would reduce uncertainty more than transcript or item-family work.

That is now the shortest honest route through Stage 2. [SOURCE: `research/iq-sex-differences-execution-plan.md`; `research/iq-sex-differences-nlscya-early-school-first-pass.md`; `research/iq-sex-differences-eclsk2011-early-school-first-pass.md`; `research/iq-sex-differences-eclsk-early-school-first-pass.md`]
