# Build brief — native–immigrant nest inside the production term

Owner: the build agent. Files owned: everything under
`infra/immigration-fiscal/production_nativity_nest_2026_09_22/` except `SPEC.md` and this
file. Nothing outside this directory is edited. No commits; the parent commits.

Follow `SPEC.md` exactly. Where this brief and the spec differ, this brief wins.

## Decisions already taken (do not re-open)

1. `sigma_NI` grid: `{1.3, 3, 4.6, 5, 7, 20, inf}`; write `sigma_NI_sourced=false` on 5 and 7.
2. Build Option A (`A_by_nativity`) and Option B (`B_target_branch`). Build `B_deep_cravino`
   (natives vs foreign at ε, then union-G1 vs other foreign at σ_FT = 14) only after both pass
   every gate; if it is skipped, `audit.json` says why.
3. Option B removal is exact: drop the target term from the aggregate and set its
   counterfactual pay to 0. The `δ` floor of SPEC §3.3 is a convergence *check* (report the
   δ = 1e-6, 1e-9, 1e-12 results agree to 1e-9 relative), not the estimator.
4. `ε = inf` is its own code path with κ = 1 (linear aggregate); never approximate it with a
   large number.
5. Tracked outputs: `derived/nest_headline.csv`, `derived/branch_composition.csv`,
   `derived/audit.json`. Ignored: `derived/nest_scenarios.csv` (write a lane `.gitignore`
   containing exactly that path). Everything in RESULT.md must be readable from the tracked files.
6. Sign convention as the existing code: with target minus without. Positive = other residents
   gain from the union's presence.

## Verification commands (run all, paste the tail of each into RESULT.md)

```sh
cd /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project \
  --with numpy --with pandas python3 -m unittest discover \
  -s infra/immigration-fiscal/production_nativity_nest_2026_09_22 -p 'test_*.py' -v
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline \
  --no-project --with numpy --with pandas --with openpyxl --with pyreadstat --with duckdb \
  python3 infra/immigration-fiscal/production_nativity_nest_2026_09_22/builder.py \
  --source-root /Users/alien/Projects/immigration-research
uv run --no-project python3 -c "import json;a=json.load(open('infra/immigration-fiscal/production_nativity_nest_2026_09_22/derived/audit.json'));print({k:v for k,v in a['gates'].items()})"
```

Timing: run the builder synchronously first with `time`. If it exceeds 4 minutes wall, rerun
it through `~/Projects/skills/bin/bgrun nest-build -- <same command>` and poll the `.done`
marker; never pipe it through `tail`.

## Gate anchors (verified by the parent on 2026-09-22 against the live files)

- `benefit_scenarios.csv` row `ces_0086_owner000` (PEARNVAL, hs_or_less, gdp, s=.65, σ=2, adj=1,
  η=0, retention=1, owner=0): `private_after_tax_wtp_bn=-0.23592432475743744`,
  `induced_current_receipts_bn=13.558522244013947`, `private_plus_receipts_bn=13.32259791925651`.
- Row `ces_0248_owner000` (same, cash): `-0.15566955604694444`, `8.946297252512256`,
  `8.790627696465311`.
- `skill_composition.csv` (PEARNVAL, hs_or_less): target 0 = 482,524,920,302.81; target 1 =
  567,059,391,429.60; national 0 = 2,706,191,503,630.51; national 1 = 9,859,381,493,300.32.
- The scenario id sits in column 9 of `benefit_scenarios.csv`, not column 1.

## RESULT.md contract

Opens with `**Verdict:**` (one paragraph: the headline cases by ε and option, in $bn, with the
perfect-substitution reproduction stated first). Then: the `nest_headline.csv` table; the gross
sides (native gain, other-immigrant loss) so the netting is visible; the gate table (G1–G9,
pass/fail, tolerance reached); files covered and skipped with reasons; limits copied from
SPEC §7 without softening. Every number carries `[CALCULATION: derived/<file>]`. No number from
memory. A gate failure stops the build and is reported as the verdict; do not weaken an
assertion to pass.

Return: the path of RESULT.md and at most 10 lines.
