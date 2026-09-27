# Brief: the sponsored-parent channel in the century lineage

Operator question (2026-09-27): the lineage model (`lineage_cost_2026_09_19`, memo
`research/immigration-lineage-cost-century-2026-09-19.md`) starts one Mexico-born founder at 25 and
follows descendants for a century. It omits the family-admission channel: a US-citizen member of the
lineage petitions for parents (IR-5), who arrive or legalize late in life. Add that channel as arms.

## Inputs (read-only)

- `lineage_cost_2026_09_19/lineage.py`, `inputs.py`, `senior_states.py`, `senior_pricing_inputs.json`
  (import or copy; do not edit — the lineage lane and the ledger loaders it reads verify hashes).
- IR-5 flows, ages at admission, the adjusters' share and the per-admission values:
  `late_arrival_tail_2026_09_27/derived/` (`ir5_flow.csv`, `ir5_age_nis2003.csv`,
  `mexico_ir_new_vs_adjust.csv`, `per_admission.csv`).
- Law on who can adjust and the 10-year bar: ladder 187 and `research/immigration-INDEX.md`'s legalization
  entries; `ir5_fraud_and_cohorts_2026_09_27/` is running and will add statute text — read it if present.

## Arms (preregister them in RESULT.md before running)

1. **Founder legalized by a US-born child at 21.** The founder, unauthorized at 25, has a US-born child
   (the model's fertility timing); at the child's 21st birthday the founder becomes an LPR through IR-5,
   (a) if eligible to adjust (lawful entry), or (b) after consular processing and the 10-year bar. Apply
   the statutory senior rules already priced in the lineage lane (the 2026-09-26 priced senior rule).
   Compare with the lineage lane's never-legalized and legalized-at-year-10 arms.
2. **Founder sponsors own parents.** Once the founder naturalizes (5 years after LPR, at the lane's
   naturalization rate — the origin-attachment lane measured 61.9% of eligible Mexican LPRs naturalized),
   a probability p of petitioning for one or two parents aged 55–65 at admission. Price the parents'
   remaining life with the per-admission profile (new arrival) and with the eligibility-change-only
   variant (parent already resident). Calibrate p from IR-5 flows against the stock of naturalized
   Mexico-born citizens and US-born adult children of Mexico-born parents; report p = 0, the calibrated
   value, and 1.
3. **Attribution.** State who owns the sponsored parents' cost in a lineage account (the lineage that
   petitioned) and report the gap with and without them. [FRAMING-SENSITIVE]

## Outputs

- `RESULT.md` opening `**Verdict:**` (stub first, append): the lineage gap under each arm vs the lineage
  lane's central −$1.30M (undiscounted) and −$515k (3%), and the share of the gap from the channel.
- Scripts here; `derived/arms.csv`; `verify.py` that reproduces the lineage lane's central case to 1e-6
  before any new arm runs.
- `.gitignore` with `_cache/`.

## Conventions

- `uv run --no-project python3 …` from the repo root; `--with <pkg>` literally; stop on the first nonzero
  exit code.
- `csv.writer(..., lineterminator="\n")`. Source tags per `CLAUDE.md`.
- Do not commit; do not edit outside this directory. Return RESULT.md path and ≤10 lines.
