# Brief: dataset-level integrity audit of the inputs behind the headline numbers

Operator, 2026-09-23 18:18: "Did we ever look at issues with the datasets itself? Just formatting
errors, bad columns, weird statistics that can't be real given real world knowledge and taste? Bad
political ways to categorize etc?" Until now this was done piecemeal (traps found inside lanes); no
dataset-by-dataset sweep of the account's raw inputs exists. This lane is that sweep, one file per
dataset family.

## Target
The adopted main case, $203.2–249.6bn (`main_case_2026_09_23/RESULT.md`), its complete account
(`research/immigration-complete-annual-account-2026-09-20.md`, lanes it cites), the generation
split (`ledger_absolute_2026_09_17`), and the crime/custody comparisons. First trace which of YOUR
family's files actually feed those numbers (follow the scripts, not the memo prose), then audit those.

## Checks, per input file actually used
1. **Format and columns:** mislabeled or shifted columns, wrong units (thousands vs dollars,
   monthly vs annual), sentinel codes read as values (9999999, -1, blank, "N/A" = 0), top-codes and
   swap values, duplicated or double files (e.g. CPS 2014 ASEC's two samples), vintage mismatches.
   Verify in the held raw file and the codebook, not the memo.
2. **Implausible statistics:** compare group-level totals and rates with an independent real-world
   anchor (administrative totals, published tables, other surveys, demographic common sense —
   e.g. age heaping, impossible combinations, rates that jump between years with no event).
3. **Imputation and allocation:** the share of the group's (and the reference group's) values that
   are imputed/allocated for each item that matters (birthplace, parents' birthplace, citizenship,
   year of entry, Hispanic origin, education, earnings, benefits), and the donor rule. Say the sign on
   the group-vs-reference gap. (The 2000 census gave most institutionalized Mexican-origin men an
   allocated US birthplace — `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md`
   Revisions — that is the kind of defect we want found BEFORE it bites.)
4. **Categories:** who is "Mexican-origin", "white", "native", "second/third generation", "Hispanic";
   self-identification attrition across generations; race-vs-ethnicity coding (Hispanic counted as
   white); category changes inside the window (2020 race/Hispanic questions, ACS 2020 experimental
   weights); residual categories renamed; ethnicity not recorded. Sign on the repo's ratios.
5. For each defect: grade A–D, measured / real-but-unmeasured / not found, and the **effect on a repo
   number** ($bn on the main case or ratio on a comparison) — compute it where the data are local;
   otherwise bound it. Defects with no effect are still listed in one line.

Lens: `~/.claude/skills/analyze/lenses/measurement-pipeline.md`; checklist
`~/.claude/skills/research/references/quant-bias-checklist.md` items 1–33 (and 34–52 for agency
tables). Keep contradictions: a defect that makes the group look BETTER is as important as one that
makes it look worse.

## Already covered — do not redo; cite and say what is left
- Crime categorization and counting mechanisms: `research/immigration-crime-statistics-bias-mechanisms-2026-09-16.md`.
- Survey totals against administrative totals: `research/immigration-administrative-checks-2026-09-19.md`,
  `research/immigration-four-fiscal-checks-2026-09-20.md`, `research/immigration-fiscal-reality-checks-2026-09-19.md`.
- External studies' integrity: `research/immigration-study-integrity-audit-2026-09-23.md`.
- Running lanes (do not duplicate; you may read their RESULT.md): CPS ASEC hot-deck imputation of
  income/benefits (`cps_imputation_keys_2026_09_23`), MEPS/MCBS medical ratios by ethnicity
  (`medical_ethnicity_pooled_2026_09_23`), NIBRS offender ethnicity (`offender_ethnicity_nibrs_2026_09_23`).
- Dataset register limitations: `research/immigration-dataset-register.md`; memory traps: BJS 2010→2011
  restatement, NCVS ×3, CPS 2014 HFLAG double file, Census API truncation, Firecrawl-fabricated SSA table.

## Rules
Data: `rg --files --no-ignore` to locate raw files (`sources/`, lane `_cache/`, `~/research-data`).
Census key: `infra/immigration-fiscal/acquire/config.local.env` — source with `set -a; . …; set +a`,
never print it, pipe URL-bearing output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project [--with pkg] python3 <script>` from the repo
root; scripts over 10 lines go in a `.py` file in this directory (prefix with your family name).
Write ONLY in `infra/immigration-fiscal/dataset_integrity_2026_09_23/`; ignored raw pulls in `_cache/`.
Do not edit other lanes, memos or the ladder. Do not commit.

## Deliverable
`<family>.md` in this directory, opening with `**Verdict:**` (the two largest defects and their
effect on repo numbers, and whether they share a sign), then: files traced (path → which repo number
it feeds), a defect table (file · item · check · finding · grade · effect · measured/unmeasured),
what prior audits covered, what was not checked and why. Reply with the path and ≤10 lines.
Include your model self-report on the last line.
