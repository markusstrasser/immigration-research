# Brief: the debt legacy of past federal gaps — interest paid in 2024

Operator, 2026-09-23 18:24: "since the 2T deficit is 2024 ... i guess we add the interest on it and
previous spending on the populations ledger in total ... mexicans are like integral over money of
the last 20 years or so idk what a good model is here ... we did the work already".

## Why and what (parent's framing — follow it)
The adopted main case ($203.2–249.6bn, `main_case_2026_09_23/RESULT.md`) is a stationary 2024
comparison: it counts no interest (interest on existing debt is at zero response). The 20-year
back-cast (`historical_backcast_2026_09_20`, memo `research/immigration-historical-backcast-2026-09-20.md`:
$3.0–4.6tn over 2005–2024 on the adopted anchor, **without interest**) is a stock of past gaps.
Past **federal** gaps were borrowed; 2024 taxpayers pay interest on that debt. Past **state and
local** gaps were paid in the year they arose (balanced-budget rules: other residents' taxes or
service cuts), so they carry no interest legacy. The model:

- F_t = federal part of year t's **fiscal** gap (direct + induced receipts F; exclude the production
  term P, which is private income and never touches the debt), in nominal dollars of year t
  (back-cast values are 2024 dollars: convert with the GDP deflator in the back-cast inputs).
- Attributable debt D = Σ_{t=2005}^{2023} F_t × Π_{s=t+1}^{2024} (1 + r_s), r_s = effective federal
  rate that fiscal year (net interest ÷ average debt held by the public; OMB Historical Tables 3.1/3.2
  and 7.1 — cached copies at `ledger_residual_agg_2026_09_16/_cache/omb_hist03z1_fy2027.xlsx`,
  `projection_backtest_2026_09_19/derived/omb-hist07z1.xlsx`; ladder 137 used 3.22% for FY2024 =
  $879.9bn over the average of $26,330bn and $28,307bn).
- Legacy interest in 2024 = r_2024 × D (report the 2024 gap's own part-year interest separately; it
  is small and belongs to the flow).
- Report the stock D ($tn, and as a share of debt held by the public) and the flow ($bn/yr, per group
  member, per other resident). Never add the stock and the flow together, and never add the 20-year
  sum to the annual account.

## The federal share (the input that matters most)
Rebuild the federal vs state-local split of the adopted main case's fiscal gap from the executed
model (`main_case_2026_09_23/derived/model.json`, `inputs.json`; the complete account's rows in
`research/immigration-complete-annual-account-2026-09-20.md` and its lanes), by the government that
pays or collects each row (federal income and payroll taxes, federal share of Medicaid/CHIP by
FMAP, SNAP, EITC/CTC, SSI, Medicare, Social Security, federal K-12 aid; state-local K-12, general
government, justice, etc.). The superseded incidence memo
(`research/immigration-fiscal-gap-incidence-who-pays-2026-09-18.md`) found 10.7–50.9% federal on the
old anchor — read its method and its correctional-payer sensitivity, then redo the split on the
adopted main case. Carry the split back per year with the back-cast's category series
(`derived/backcast_categories_annual.csv`) where it has one; otherwise hold the 2024 split and say so.
The federal side may be near zero or positive for a young group (payroll taxes above benefits):
report the sign honestly.

## Specifications (compute all; central first)
- back-cast rules: every rule in `backcast_windows.csv` on the adopted anchor (low/high), and the
  programme-by-programme version if it can be run;
- windows: 2005–2024 (central, the operator's "last 20 years"), 2010–, 2015–; say what pre-2005
  would add qualitatively (the ACS series starts in 2005);
- rates: actual effective rate path (central); constant 3.22%; 10-year Treasury path;
- financing: all federal gaps borrowed (central); half borrowed, half offset (ladder 137's variant);
- federal share: central rebuild, low and high payer conventions.

## Overlap and symmetry
- The legacy line is the group-attributable part of "interest on existing debt"; if adopted it
  enters the main case as that row's response (give the row share: legacy interest ÷ FY2024 net
  interest). Check whether the "every service proportional" benchmark already allocates interest per
  head; if it does, the legacy line must not be added to that benchmark.
- Symmetry (rule 5): induced receipts and any past fiscal benefit already inside the back-cast
  reduce F_t; social benefits beside the account never touch the debt. Say so.
- Forward counterpart: the 2024 federal flow adds to debt in 2025+; rebuild ladder 137's forward
  path on the adopted numbers in one short table (it used the superseded −$263bn).
- Do not edit fingerprinted `.py` files of `ledger_absolute_2026_09_17` or `gen_ledger_extension_2026_09_16`
  (read only).

## Deliverable
`RESULT.md` opening with `**Verdict:**` (stock, 2024 legacy interest, per member, central and range,
and the federal share it rests on), then method, every specification, overlap ruling, limits.
Scripts in this directory, `derived/*.csv` aggregates, raw pulls in `_cache/`. Run with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root; rerun and check
byte-identical outputs (stop on the first nonzero rc before comparing). Write only in this
directory. Do not commit. Reply with the RESULT path and ≤10 lines; model self-report on the last line.
