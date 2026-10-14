# Lineage mortality on the v7 pension accrual

Read [RESULT.md](RESULT.md) for the decision and [salmon-evidence.md](salmon-evidence.md) for the bounded return-migration search. This lane imports the comparator and pension routes read-only. It writes no upstream files or git metadata.

Reproduce from the repository root (pinned inputs must already exist):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/lineage_mortality_2026_10_14/prepare_sources.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/lineage_mortality_2026_10_14/measured_run.py mortality.py
OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/lineage_mortality_2026_10_14/test_mortality.py -q
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/lineage_mortality_2026_10_14 \
  "uv run --no-project python3 {lane}/prepare_sources.py" \
  "uv run --no-project python3 {lane}/measured_run.py mortality.py" \
  "uv run --no-project python3 -m pytest -p no:cacheprovider {lane}/test_mortality.py -q" \
  "uv run --no-project python3 {lane}/final_paths.py"
```

`prepare_sources.py` uses installed Poppler `pdftotext -layout`. It deterministically re-extracts Fenelon Tables 3/4 and Turra Table 4 from pinned primary PDF bytes. `--pin` and `--pin-salmon` were one-time inspected acquisitions; repeating them fails closed. The parser verifies DOI/title/table identity; expected-cell regression tests were independently checked against rendered Fenelon PDF pages 6/7. Publisher copies are archived, not LLM table extractions. The primary Van Hook HTML is an exact copy of the repo's existing acquisition, with that provenance in the evidence note.

During verification, a concurrent peer migrated comparator entrypoints to oct15. `--freeze-route` therefore archived the **exact originally pinned v7 bytes** of `mortality_comparators.py`, `accrual_white.py`, `accrual_black.py`, `tr2026_path.py` and the white input-pins inventory. Every archived SHA256 equals its original pin; no analytical input was repinned to a new value. `inputs/pins.json:route_archives` explicitly declares this frozen oct14 route. The loader executes those bytes with the original module `__file__`/spec metadata, preserving the admitted relative input paths while excluding migrated CLI entrypoints. The `.py.txt` archives are immutable evidence consumed by the loader, not standalone scripts. All remaining pension code/data still have executable byte pins. Repeating `--freeze-route` fails closed.

`pytest.ini` disables the shared cache writer even in a default pytest invocation; a session fixture fails if that plugin is re-enabled. Two early runs preceded this guard and updated the root's ignored `nodeids`/`lastfailed`; those paths are preserved and included in `changed-paths.txt`. The manifest is a historical handoff record and includes ignored diagnostics and the removed rejected challenge-page acquisition.

`mortality.py` reproduces general and pooled-Hispanic controls before any new mortality tables, then uses the imported `mortality_comparators` table context, row-4 frame and output-row route; the same white/Black helpers and `tr2026_path` build and price the accrual. Each synthetic table replaces only the requested numerator population. Note 2025.7's original general denominator remains byte-identical. The existing actuarial model closes survival at age 100; qx is stored through age 120 to match that API.

`derived/hazard_ratios.csv` preserves all 16 Mexican primary sex/nativity/model HR/CI cells and their exact source rows. `mortality_qx.csv` contains every constructed table. `reproduced_ratios.csv` and `pooled_control.csv` are executed controls. `accrual_ratios.csv` prices each identified generation and three added profiles. `generation_changes.csv`, `generation_changes_cash.csv`, `added_profiles.csv` and `case_changes.csv` attribute the marginal mortality change and its added-profile bound. `comparisons.csv` substitutes only that lineage change into committed comparator rows. `audit.json` records closure and denominator checks. Cash costs are held fixed analytically; this is a mortality-only accrual experiment, not a fresh cash-engine execution.

Python `time.perf_counter` and `resource.getrusage` measure time/RSS; the imported `memory_budget.require_within_budget` gates physical footprint inside the calculation process at 2.5 GB. `measured_run.py mortality.py --profile` adds a cProfile diagnostic. Nondeterministic logs/timings and rendered PDF checks live only in ignored `_cache/`. No `/usr/bin/time`, `ps` or `sysctl` is used.

All dollar changes are modeled billions per income-year-2024 annual account, payable and net of future benefit taxes, at v7 personal specifications 16/11. They are neither observed historical contributions nor current cash/debt flows. National annual payroll bases, monetary inputs, benefits qualification and all non-pension lines are held fixed. The generation split is a split of this marginal change, not a substitute for the complete case's generation account.
