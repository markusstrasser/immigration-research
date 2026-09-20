# Public school-finance reconstruction

Source: Pierson, Hand and Thompson (2015),
[GFD article](https://doi.org/10.1371/journal.pone.0130119),
[official S7 ZIP](https://journals.plos.org/plosone/article/file?type=supplementary&id=10.1371/journal.pone.0130119.s007).
Acquired2026-09-20. Source lock: [SOURCES.json](SOURCES.json); complete archive
85,277,958 bytes. Publisher MD5, SHA256 and all ZIP-member CRCs checked. The CSV
remains compressed and is streamed to a selected1967–92 extract. Raw files and
rederivable outputs are under ignored `work/`; no corpus originals were modified.
The PLOS article/supplement is publicly distributed under its CC-BY terms with
author attribution; underlying Census government records are public.

Download S7 into `work/gfd-school-validated.zip` (create `work/` if needed), then
run from the repository root:

```sh
uv run python3 infra/immigration-fiscal/causal_execution_2026_09_20/mariel/prepare_panel.py
uv run python3 infra/immigration-fiscal/causal_execution_2026_09_20/mariel/build_scm_panel.py
uv run python3 infra/immigration-fiscal/causal_execution_2026_09_20/mariel/build_june_panel.py
```

Run `scm_reconstruction.py --panel <panel> --out <output-directory>
--timing-review <review>` with `uv run --with scipy python3`. All paths below
are within this folder's `work/`:

| Panel | Review | Output |
|---|---|---|
|scm-source-year-panel.csv|timing-review.json|results-source-year/|
|scm-published-pool-panel.csv|timing-review.json|results-published-pool/|
|scm-june-only-panel.csv|timing-review-june.json|results-june-only/|

Each run computes seven spending/revenue/tax/transfer endpoints, donor weights,
annual gaps, all placebo fits, one/two-sided ranks, preperiod holdout and largest
donor deletion. `test_checks.py` in the parent folder verifies the saved paths,
ranks and exclusion of actual treated Dade from every placebo donor set.

Units and scope:

- `ID` is Census government ID, not county FIPS. Dade schools are105013001;
  colleges, treated Dade and nearby Broward/Palm Beach are excluded from donors.
- `Year4` is survey year. Census surveyY covers fiscal ends July1(Y−1)–June30Y.
  ObservedJune30 schools map directly; missing dates do not prove calendar stability.
  Full-pool results remain timing diagnostics, not exact published replication.
- `Total_Current_Oper` is recurring operating spending; `Total_Current_Expend`
  is a different quantity. Monetary fields are nominal thousands of dollars.
-1980 enrollment defines the large-district pool. Historical enrollment metadata
  include substituted/unusable years; no annual per-pupil denominator is inferred.
- Ordinary simplex SCM differs from St Clair's `allsynth` bias correction.
  Zero/near-zero pre-fit denominators fail loudly; they are not silently assigned1.
  Post-treatment Dade is excluded from placebo donors. No income, nativity,
  ethnicity, class-size or child-attainment variable is inferred from fiscal data.

Timing/variable definitions were independently checked against the included2006
Census classification manual §3.2 and the official historical INDFID codebook
([Census archive](https://www2.census.gov/programs-surveys/gov-finances/datasets/historical/indfin%20school%20district%20finance%20data%20fy%201967-91.zip)).
The codebook's DD/II/BB flags mean government-provided/imputed/blank. Year4 is
not the sometimes nonnumeric `YearofData` field. Dade1979 revenue493.310million
matches the published paper's rounded493million anchor.

Results and transfer limits: [executed evidence note](../../../../research/immigration-causal-execution-2026-09-20.md).
