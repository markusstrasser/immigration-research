**Verdict:** Demographic transport improves average later CPS component-share prediction modestly, but loses on three transfer programs and does not resolve a large independent IRS distribution mismatch. See [RESULT.md](RESULT.md) and the pre-score [DESIGN.md](DESIGN.md).

# Reproduction

Run from the main checkout so `uv --no-project` can use its dependencies. During isolated development, pass the absolute managed-worktree script path; once integrated, use:

```sh
OPENBLAS_NUM_THREADS=1 \
uv run --no-project --with xlrd python3 \
  infra/immigration-fiscal/validation_fiscal_years_2026_09_28/analysis.py \
  --source-root /Users/alien/Projects/immigration-research

OPENBLAS_NUM_THREADS=1 \
uv run --no-project python3 -m pytest \
  infra/immigration-fiscal/validation_fiscal_years_2026_09_28/test_analysis.py -q
```

Inputs are read-only official ASEC2022–2025 ZIPs already held by the latam-comparison, matched-year-tax and canonical source lanes; income2022/2023 IRS table1.2 XLS files; existing source hash locks; and the ASEC2022 dictionary for the pandemic tax identity. No raw pulls, API keys or calibration downloads.

The script independently reconstructs actual annual selected component accounts. It predicts later allocation shares conditional on later population composition; observed later national component totals only convert share errors to conditional dollars. It does not manufacture historical full-government balances or validate their national scale.

Ignored `derived/` outputs:

- `annual_components.csv`: four years × four disjoint groups × eight outcomes, with SDR SEs.
- `support.csv`: all32 age/sex/generation cells each year, raw counts and two exposure conventions.
- `scores.csv`: every split, component and arm, signed/absolute share errors, conditional dollar errors and separate training/test uncertainty.
- `paired_scores.csv`: same-replicate absolute-error improvement against frozen shares.
- `irs_distribution.csv`: all19 AGI-bin residuals for frozen CPS/IRS and same-year CPS diagnostics.
- `audit.json`: source, script, design and output SHA256 plus source conservation/identity checks.

Update 2026-09-28: these `derived/` outputs are now tracked in git.

Tests cover stable-rate exact prediction, changed-rate falsification, unsupported training-cell failure, negative net-tax retention, the SDR coefficient, pandemic-specific tax identity and missing-reader failure before source work. Malformed SPM units, invalid composition codes and altered IRS sources are also rejected in actual `python -O` subprocesses; IRS year and column metadata have separate malformed-layout checks. Runtime source guards use explicit exceptions and NumPy testing functions, so optimization cannot disable them. Integrated raw-data guards cover joins, SPM totals and weighting.

Native-First: read official CSV ZIP/XLS files with pandas and perform Census SDR calculations with NumPy; use no synthetic historical national totals, modeled missing outcomes, or silent fallbacks.
