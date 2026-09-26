**Verdict:** Split by generation, the main case with schools at full average cost ($258.5–292.0bn a
year) leaves all three Mexican-origin generations as net costs to other US residents, at every one of
its 64 specifications and under both ways of counting children. Counted in their own generation, the
Mexico-born cost others $57–78bn a year ($4.7–6.4k per member), the second generation $105–117bn
($7.3–8.2k) and the third-plus $76–118bn ($5.3–8.2k). Counted with their parents, as the National
Academies count them, they cost $136–155bn ($11.6–13.3k per adult), $66–68bn ($7.4–7.6k) and
$55–71bn ($6.7–8.6k). Against the September 24 split, schools at full cost add $62.1bn (low end) and
$48.5bn (high end), and where the children are counted decides who carries it. Under (a) the second
and third-plus generations carry 76–91% of it; under (b) the Mexico-born carry 43–44%.
[FRAMING-SENSITIVE] [CALCULATION: `run_generations.cjs` → `derived/generation_summary.json`,
`change_from_sept24`]

## Schools at full average cost (2026-09-26)

The operator adopted schools at full average cost per pupil as the main case
(`main_case_schools_full_2026_09_26`, $258.4885–291.9548bn; decision
`2026-09-26-main-case-schools-full-cost`). It is the September 26 case (finite-removal responses, row 8
at 0.949, the consumption key) with the school response at 1. `derived/` holds this case.
`--case sept26` reproduces the one-year scenario ($200.9180–245.6949bn), and `--case sept24`
reproduces the September 24 record below byte for byte. Model self-report: claude-opus-5-5.
Propagation report: [RESULT_generation.md](../sept26_propagation_2026_09_26/RESULT_generation.md).

These figures are net costs to other US residents, $bn a year, 2024. Schools respond at 1 at both ends.
The low end is the shared allocation with GDP normalization, school share 0.715 and general government
at 0.6000. The high end is the personal allocation with cash normalization, school share 0.865 and
general government at 0.8504. At a school response of 1 the school-share bound flips, so the ends are
specifications 48 and 11, not September 24's 56 and 7.

| (a) Children in their own generation | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1, born in Mexico | 77.6 | 56.9 | 49.3–85.4 | 6,354 / 4,657 | 6,651 / 4,875 |
| G2, US-born, a parent born in Mexico | 105.0 | 117.5 | 105.0–117.5 | 7,326 / 8,195 | 11,778 / 13,176 |
| G3+, US-born of US-born parents | 75.8 | 117.6 | 75.8–117.6 | 5,288 / 8,198 | 9,268 / 14,369 |
| All three (the main case) | 258.5 | 292.0 | 258.5–292.0 | 6,321 / 7,139 | 8,984 / 10,147 |

| (b) Minors with their parents (NAS 2017) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|
| G1 | 135.6 | 155.4 | 135.6–155.4 | 8,043 / 9,218 | 11,612 / 13,309 |
| G2 | 67.9 | 66.1 | 60.9–73.0 | 5,562 / 5,411 | 7,617 / 7,410 |
| G3+ | 55.0 | 70.5 | 55.0–70.5 | 4,650 / 5,960 | 6,723 / 8,617 |

Members and adults do not change with the case: 40.90m and 28.77m in all. [CALCULATION:
`run_generations.cjs` → `derived/generation_results.csv`]

**The move from September 24.** Each generation's move splits exactly into five parts, $bn a year at
the low / high end. The responses act at September 24's band-end specification, and "band end" then
moves the end to the new specification. The parts add to the move within 1.5e-13bn
(`generation_summary.json` → `change_from_sept24`).

| $bn, low / high | Sept 24 | Schools at 1 | General government | Band end | Row 8 at 0.949 | Consumption key | Schools case | Move |
|---|---|---|---|---|---|---|---|---|
| (a) G1 | 63.79 / 53.56 | +14.87 / +4.14 | +0.13 / +0.14 | −0.18 / +0.04 | −0.03 / −0.03 | −0.93 / −0.93 | 77.65 / 56.91 | +13.85 / +3.35 |
| (a) G2 | 81.74 / 95.12 | +24.68 / +23.02 | +0.17 / +0.18 | −0.32 / +0.41 | −0.04 / −0.04 | −1.23 / −1.23 | 105.00 / 117.46 | +23.26 / +22.34 |
| (a) G3+ | 55.34 / 97.64 | +22.54 / +21.32 | +0.17 / +0.18 | −0.29 / +0.37 | −0.04 / −0.04 | −1.89 / −1.89 | 75.84 / 117.58 | +20.50 / +19.95 |
| (b) G1 | 110.22 / 134.76 | +26.91 / +21.46 | +0.19 / +0.19 | −0.35 / +0.37 | −0.04 / −0.04 | −1.36 / −1.36 | 135.56 / 155.38 | +25.34 / +20.62 |
| (b) G2 | 50.18 / 52.96 | +18.62 / +13.53 | +0.15 / +0.15 | −0.24 / +0.22 | −0.03 / −0.03 | −0.77 / −0.77 | 67.90 / 66.06 | +17.72 / +13.10 |
| (b) G3+ | 40.47 / 58.60 | +16.56 / +13.50 | +0.14 / +0.15 | −0.20 / +0.22 | −0.03 / −0.03 | −1.92 / −1.92 | 55.02 / 70.52 | +14.55 / +11.92 |
| Union | 200.88 / 246.32 | +62.08 / +48.49 | +0.47 / +0.49 | −0.79 / +0.81 | −0.10 / −0.10 | −4.05 / −4.05 | 258.49 / 291.95 | +57.61 / +45.64 |

The responses are engine state, so each generation's model responds on its own lines. They come from
the package's `MAIN_SPECS`, gated against `corrections.json` → `meta.responses`. Row 8's change splits
as the lane splits row 8, by population.

The order decides how the move splits between schools and the band end, not their sum. At the case's
own end specifications, schools add $51.3bn / $63.8bn to the union and the end move +$10.0bn /
−$14.5bn. Either way the two together are +$61.3bn / +$49.3bn. The order above is the brief's:
matched specifications first, then the range ends move.

**The school line by generation.** The table gives what the case charges each generation for
schools at the band end: its cost at a school response of 1 less its cost at 0
(`school_line_at_case_bn`). A generation's share of this line is also its share of the "Schools at 1"
column above, because both scale the same school costs under the same allocation.

| $bn, low / high | School line | Share of the union's |
|---|---|---|
| (a) G1 | 33.22 / 14.74 | 24% / 9% |
| (a) G2 | 55.15 / 81.90 | 40% / 47% |
| (a) G3+ | 50.36 / 75.84 | 36% / 44% |
| (b) G1 | 60.13 / 76.34 | 43% / 44% |
| (b) G2 | 41.60 / 48.11 | 30% / 28% |
| (b) G3+ | 37.00 / 48.02 | 27% / 28% |
| Union | 138.73 / 172.47 | 100% |

Under (a) the line falls on the generations that hold the pupils, the second and third-plus. At the
shared low end, parents carry part of it through the SPM unit's equal split, so the Mexico-born take
24% there against 9% at the personal high end. Under (b) minors count with their parents, and the
first generation takes 43–44%. [FRAMING-SENSITIVE]

**The consumption key, split exactly.** The consumption lane's CPS frame matches this one person for
person: the same records, all 161 weights and the generation masks (gate). `consumption_split.py`
recomputes each generation's key with the lane's saving ratio and corridor outflow. From the
generation totals it rebuilds the lane's 40 union edits with a maximum difference of 0.0. At the
union's stack factor, the group pays $9.30bn more from saving and $5.24bn less from remittances:

| $bn of receipts, at the union's stack factor | Saving | Remittances | Net | Key share: old → corrected |
|---|---|---|---|---|
| (a) G1 | +4.37 | −3.03 | +1.34 | 2.204% → 2.377% |
| (a) G2 | +2.91 | −1.87 | +1.04 | 2.654% → 2.798% |
| (a) G3+ | +2.02 | −0.34 | +1.67 | 3.246% → 3.423% |

The lane's rule for every ratio-type correction then applies. Each generation's saving part takes its
own stack factor on the consumption key (0.85, 0.98 and 0.99 under (a), against the union's 0.9497).
The corridor's dollars are not scaled, and the $0.31bn remainder goes to the generations in proportion
to their consumption-tax cells after the stack. Cells with no main-case weight take the union's edit
times the generation's share of the change in the key share. [CALCULATION: `consumption_split.py` →
`derived/consumption_key_by_generation.json`]

| Consumption key, $bn of cost | Own factor (central) | Union's factor | Old key's shares (brief's fallback) |
|---|---|---|---|
| (a) G1 / G2 / G3+ | −0.93 / −1.23 / −1.89 | −1.34 / −1.04 / −1.67 | −1.10 / −1.33 / −1.62 |
| (b) G1 / G2 / G3+ | −1.36 / −0.77 / −1.92 | −1.72 / −0.61 / −1.72 | −1.39 / −1.25 / −1.40 |

Both alternatives run as sensitivities: the union's factor inside `stack_scaling_by_union_factor`, and
the old key's shares as `consumption_key_by_old_key_shares`. The saving ratio comes from income rank
alone. CE has no parents' birthplace, so the ratio cannot differ by generation at the same income.

**Other figures, updated** (September 24 in brackets):
- Moving minors to their parents' generation shifts $58–98bn onto the first generation ($46–81bn).
- Under (a), the household allocation rule shifts $28–36bn between the first and third-plus
  generations ($19–32bn).
- The eight alternative split rules (the seven below plus the old key's shares) move no generation by
  more than $3.7bn, and none turns a cost negative. The largest is still the literal fill-in rule.
- Under (b), a second-generation adult with their minor children costs others 56–66% of what a
  Mexico-born adult does (51–60%).
- Against the uncorrected model at the case's responses, the corrections move (a) G1 by +$4.8 / +4.1bn,
  G2 by −$5.9 / −7.5bn and G3+ by −$6.1 / −3.4bn. They move (b) G1 by −$2.0 / −2.3bn, G2 by
  −$3.5 / −3.6bn and G3+ by −$1.7 / −0.8bn.
- At the shared end, the account now gives −$6,354, −$7,326 and −$5,288 per person, against the
  September 19 ledger's own balances of −$5,929, −$5,881 and −$4,223. With schools and other
  education at average cost, the main profile's marginal responses take off only the delayed
  services (economic affairs, recreation and culture at zero response), $967–1,172 per person. So
  the direct lines at the responses sit $751–2,025 below the ledger's balances; on September 24 they
  were within $71–481. At the low end the corrections add $396 per person to the first generation
  and take $411 and $422 from the second and third-plus. Under the personal allocation, G3+ and G2
  are within $3 per person of each other. [CALCULATION: `compare_ledger.py` →
  `derived/ledger_comparison.csv`]

**Gates.** Both full runs pass every gate (186 gate lines each), and the second run is byte-identical
to the first in all 20 derived files.
- The corrected union reproduces $258.4885–291.9548bn, and the uncorrected union reproduces
  $265.5903–298.6797bn.
- The three generations add to the union in all 64 specifications under both conventions: 1.4e-12bn
  corrected, 1.1e-13bn uncorrected.
- The netted generation edits add to `corrections.json` in all 270 cells (1.4e-12bn).
- `corrections.json` is the package's payload (deep-equal), and the specifications carry
  `meta.responses`: general government 0.6000/0.8504, schools 1/1.
- The move from September 24 splits exactly (1.5e-13bn), and the generations' school parts add to the
  union's.
- `--case sept24` reproduces the four case-dependent outputs of ba12f3c byte for byte. `--case sept26`
  passes its 27 gates and reproduces $200.9180–245.6949bn.

**Reproduce.** `bash run_all.sh` runs every step and ends with
`main_case_schools_full_2026_09_26/main_case.cjs`. For the other cases, run
`node run_generations.cjs --case sept26|sept24 --out-dir DIR`, then `compare_ledger.py --out-dir DIR`.
Headline cell: `derived/generation_results.csv`, row `a,G1,low`, `cost_bn` 77.645780.

## September 24 record (superseded 2026-09-26)

**September 24 verdict:** Split by generation, the adopted main case ($200.9–246.3bn a year) leaves all three
Mexican-origin generations as net costs to other US residents. That holds at every one of the main
case's 64 specifications and under both ways of counting children. Where children are counted
decides the order. Counted in their own generation, the Mexico-born cost others $54–64bn a year
($4.4–5.2k per member), the US-born second generation $82–95bn ($5.7–6.6k) and the third-plus
$55–98bn ($3.9–6.8k). Counted with their parents, as the
National Academies count them, the Mexico-born cost $110–135bn ($9.4–11.5k per adult), the second
generation $50–53bn ($5.6–5.9k per adult) and the third-plus $40–59bn ($4.9–7.2k per adult).
[FRAMING-SENSITIVE] [CALCULATION: `run_generations.cjs` → `derived/generation_summary.json`]

Moving minors to their parents' generation shifts $46–81bn onto the first generation. Under
convention (a), the household allocation rule shifts $19–32bn between the first and third-plus
generations. The alternative split rules for the 270 corrections, run at the two ends, move no
generation by more than $3.7bn, and none turns a generation's cost negative. Compared with the
September 19 ledger, its gaps (−$7,584, −$7,521 and −$6,195 per person) are measured against
third-plus non-Hispanic whites, who are net contributors at these ages. The groups' own balances in
that ledger (−$5,929, −$5,881 and −$4,223) are close to this account's −$5,220, −$5,703 and −$3,859
under the same allocation. They get there through offsetting differences, so the closeness validates
neither. This is one year's account of the people alive in 2024. It cannot say what today's children
will pay as adults.

Lane: `infra/immigration-fiscal/generation_account_2026_09_24/`, brief [BRIEF.md](BRIEF.md),
2026-09-24/25. Model self-report: `claude-opus-5-5[1m]`. Not committed (the parent re-runs and
commits). No shared module needed a change, and no other lane was written.

## Results

These figures are the net cost to other US residents in $bn a year for income year 2024, at the two
ends of the adopted main case:

- **Low end:** shared allocation, GDP normalization, school share 0.865 at response 0.63, general
  government 0.59 and low uncompensated care.
- **High end:** personal allocation, cash normalization, school share 0.715 at response 0.66,
  general government 0.84 and high uncompensated care.

They are model output: CPS allocations are measured, while service responses and the production term
are assumed. Per member divides by the people counted in the generation under the chosen convention.
Per adult divides by those aged 18 and over. The own range is the generation's lowest and highest
cost over the 64 specifications.

| (a) Children in their own generation | Members (m) | Adults (m) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|---|---|
| G1, born in Mexico | 12.22 | 11.67 | 63.8 | 53.6 | 44.7–74.8 | 5,220 / 4,383 | 5,464 / 4,588 |
| G2, US-born, a parent born in Mexico | 14.33 | 8.91 | 81.7 | 95.1 | 81.7–95.1 | 5,703 / 6,636 | 9,169 / 10,670 |
| G3+, US-born of US-born parents | 14.34 | 8.18 | 55.3 | 97.6 | 55.3–97.6 | 3,859 / 6,808 | 6,763 / 11,931 |
| All three (the adopted main case) | 40.90 | 28.77 | 200.9 | 246.3 | 200.9–246.3 | 4,912 / 6,023 | 6,981 / 8,561 |

| (b) Minors with their parents (NAS 2017) | Members (m) | Adults (m) | $bn, low end | $bn, high end | Own range, $bn | $ per member, low / high | $ per adult, low / high |
|---|---|---|---|---|---|---|---|
| G1 | 16.86 | 11.67 | 110.2 | 134.8 | 110.2–134.8 | 6,539 / 7,995 | 9,441 / 11,543 |
| G2 | 12.21 | 8.91 | 50.2 | 53.0 | 44.0–59.3 | 4,110 / 4,338 | 5,629 / 5,941 |
| G3+ | 11.83 | 8.18 | 40.5 | 58.6 | 40.5–58.6 | 3,420 / 4,952 | 4,945 / 7,160 |

[CALCULATION: `run_generations.cjs` → `derived/generation_results.csv`] At every specification and
under both conventions, the three generations add to the adopted main case to within $1.5e-12bn;
the brief's gate is $0.01bn.

Per adult under (a) is not a per-parent figure. It divides children's costs by the adults of another
generation: 5.4m of the second generation are minors, and 4.3m of them count with a Mexico-born
parent under (b). [DATA: `mixed_units.py` → `derived/minors_convention_b.csv`] Under (b),
a second-generation adult, with their minor children, costs others 51–60% of what a Mexico-born adult
does. The third-plus cost less than the second generation at the low end and more at the high end.
None of these figures is age-standardized. Second-generation adults average 34.7 years, against 40.8
for the third-plus and 48.2 for the Mexico-born. [DATA: `mixed_units.py` → `derived/mixed_units.csv`]

**The household allocation rule matters as much as the convention for the third-plus.** The shared
rule splits every key equally within the SPM unit (`cps_imputation_keys_2026_09_23/common.py`
`unit_equal`). Parents therefore carry part of their children's costs even under (a). Units that
include people outside the union also pass costs and taxes across its boundary. In the table below,
each end keeps its other settings and only the allocation changes. [FRAMING-SENSITIVE]

| $bn a year | Low end (shared) | Low end, personal instead | High end (personal) | High end, shared instead |
|---|---|---|---|---|
| (a) G1 | 63.8 | 44.7 | 53.6 | 74.8 |
| (a) G2 | 81.7 | 82.6 | 95.1 | 93.0 |
| (a) G3+ | 55.3 | 86.1 | 97.6 | 65.6 |
| (b) G1 | 110.2 | 119.2 | 134.8 | 125.5 |
| (b) G2 | 50.2 | 44.0 | 53.0 | 59.3 |
| (b) G3+ | 40.5 | 50.2 | 58.6 | 48.6 |

[CALCULATION: `run_generations.cjs` → `generation_summary.json` `allocation_swap`] Of third-plus
members, 36% live in an SPM unit with someone outside the union (41% of third-plus minors). The
figures are 18% for the second generation and 10% for the first. On average, 13% of a third-plus
member's unit lies outside the union. Under the shared rule these members take in part of those
people's taxes, and under the personal rule they carry their own costs in full.
[DATA: `mixed_units.py` → `derived/mixed_units.csv`]

**What the corrections do by generation.** Relative to the September 23 case at the same
specifications, under (a):

- The corrections raise the first generation's cost by $6.0bn (low end) and $4.3bn (high end).
- They lower the second generation's by $4.2bn and $6.1bn, and the third-plus's by $4.2bn and $1.6bn.

Under (b), they move the first generation by only +$0.4bn and −$0.7bn. The children's shares of the
premium-credit re-key and pooled medical join their parents' there, and the resulting −$9–10bn and
−$6.3bn offset the tax-records stack's +$16–18bn. [CALCULATION: `generation_summary.json` `lanes`]

## Plan and gate status

| Step | What | Gate | Status |
|---|---|---|---|
| 0 | Generation masks on the account's frame; how the CPS records parents' birthplaces | counts equal `generation_split_2026_09_20/derived/cps_generation_split.csv` | **passed** (`test_masks.py`, 3 tests) |
| 1 | Every allocation key restricted to each generation, both allocations | three generations sum to the group's key total, 1e-9 relative | **passed** (`keys.py`: 30 receipt and 52 spending keys, plus the education, owner-property, federal-gap, justice-use and uninsured-use keys) |
| 2 | `derived/model_G1.json`, `model_G2.json`, `model_G3plus.json`, plus `model_b_*` for (b) | summed line by line, they reproduce `model.json` | **passed** (`build_models.py`: every cell to 5.7e-14 bn and the production arrays to 1.1e-13 bn, both conventions) |
| 3 | Production term P and F by generation, as a first-order attribution | three sum to the group's in all 3,888 scenarios | **passed** (`production.py`: 1.1e-13 bn) |
| 4 | The 270 correction edits split by generation, one written rule per source lane | split edits sum to `corrections.json` | **passed** (`stack_split.py`, `external_split.py`, `correction_rules.py`; every lane's union figure is rebuilt from its own outputs, and the netted generation edits add to all 270 cells to 1.4e-12 bn under both conventions) |
| 5 | Engine per generation over `MAIN_SPECS`, conventions (a) and (b) | three sum to the main case at every specification, $0.01bn; linearity | **passed** (`run_generations.cjs`: the corrected union reproduces $200.8752–246.3184bn; the generations add to 1.5e-12 bn corrected and 1.4e-13 bn uncorrected, in all 64 specifications and both conventions) |
| 6 | Comparison with the September 19 ledger | ledger read through its own loader; same populations; eight-band gaps within 2% of the published ones | **passed** (`compare_ledger.py`) |
| — | `node ../main_case_2026_09_24/main_case.cjs` | still passes; lane unchanged | **passed** (last step of `run_all.sh`; `git status` on that lane is clean) |

A full rebuild with `run_all.sh` passed every gate and rewrote all 19 derived files byte for byte.

## Step 4: how each correction is split

The union column gives each source lane's contribution, including the package's stack-factor
interaction, so the rows add to the correction: −$2.33bn at the low end and −$3.32bn at the high end.
They differ from the package's "alone" figures, which leave that interaction out. "Exact" means the
lane's own computation was re-run for each generation.

| Source lane | Union, $bn low / high | Rule | Kind |
|---|---|---|---|
| Tax-records stack: status rules, the state-aware status flag, ACS row-4 weights, Census fill-ins | +19.9 / +21.2 | The CPS lane's own functions, with each generation's mask in place of the union's; ten hot-deck runs (five seeds, union-matched and pooled-donor), each reproducing the lane's stored shares to 3e-15 | exact |
| CBO incidence and category re-key | +9.3 / +8.4 | Each generation's share of the re-keyed receipt keys (the external lane's CBO arm) | exact |
| Treasury OTA income-tax key (outside checks) | −0.4 / −0.3 | The same with the OTA arm and the SSN rule, which splits by each generation's income position | exact |
| Premium credits keyed as EITC (audit row 1) | −14.2 / −14.2 | The audit's formula (credits × pool fraction × (Marketplace share − credit share)) per generation | exact |
| Pooled MEPS medical and long-term care | −16.8 / −16.8 | Medical: the lane's age × US-birth cell ratios on each generation's own cells. LTSS: by the users' generation | medical exact; LTSS users partly inferred |
| Schools priced where enrolled, college line (row 6) | +0.7 / −0.5 | Each generation's own pupils (school key) and students (postsecondary key) | the brief's rule |
| Administrative benefit keys | +2.2 / +2.0 | As each line's uncorrected key splits | flagged |
| Justice booking factor and audit row 7 | +2.0 / +2.0 | As the arrest-keyed parts of the use key split (like custody) | flagged |
| Lane constants: rows 8–10, small items, shelter, care work | −5.1 / −5.1 | Row 8 and small items by population; row 9 as the Medicaid and Medicare keys; row 10 as the WIC key; shelter by use to recent arrivals (G1) net of the keyed charge; care work by the workers' generation | shelter and care by the brief's rule; rows 9–10 and small items flagged |

[CALCULATION: `correction_rules.py` → `derived/correction_rules.json`; `stack_split.py` →
`derived/stack_by_generation.json`; `external_split.py` → `derived/external_by_generation.json`]

**Where the exact split departs from the brief's literal wording.** The brief assigns status-based
corrections to "the first generation, or its unauthorized subset". The exact re-run agrees on who
triggers them. It then spreads their effect as each allocation does: under the shared rule, a
Mexico-born worker's taxes are split with the unit's US-born children. The brief assigns Census
fill-ins "by the generation make-up of the imputed records". The exact re-run measures each
generation's change in key share under the fill-in method, where the literal rule would split by
imputed dollars. Both literal rules are run as sensitivities below.

Within the pooled medical correction, the long-term-care rule takes the Mexico-born share of users
from ACS 2024 proxy populations in each TAF age group. The US-born part is split as the union's
Medicaid enrollees are in the CPS. [INFERENCE: the ACS has no parents' birthplace.] The college part
of row 6 moves 18–23% of the education line onto the postsecondary key. Under the personal
allocation and (a), the first generation holds 29.0% of that key but only 5.6% of the school key.
That is why education adds $3.6bn to the first generation at the high end. [DATA:
`derived/generation_key_shares.json`]

**Sensitivities of the flagged and literal rules** ($bn a year; central, then the lowest and highest
of seven alternatives):

- benefits all to G1;
- benefits all to the US-born;
- justice per adult;
- foster care by children;
- the status rules all to G1;
- fill-ins by imputed dollars;
- stack scaling by the union's factor.

| | (a) low end | (a) high end | (b) low end | (b) high end |
|---|---|---|---|---|
| G1 | 63.8 (60.7–65.5) | 53.6 (50.3–54.9) | 110.2 (107.2–111.6) | 134.8 (131.8–135.9) |
| G2 | 81.7 (80.2–83.7) | 95.1 (94.4–98.8) | 50.2 (48.8–53.3) | 53.0 (52.3–56.5) |
| G3+ | 55.3 (54.5–56.5) | 97.6 (97.1–98.1) | 40.5 (39.9–40.9) | 58.6 (58.0–59.1) |

[CALCULATION: `generation_summary.json` `sensitivities`] The most influential alternative is the
literal fill-in rule. It lowers the first generation's cost by $2.9–3.3bn and raises the second's by
$2.0–3.7bn. I keep the exact split because it is the change the fill-in method actually makes to each
generation's key share. On the evidence-symmetry rule 4, the lean of the central rules is mixed.
Under (a), at the low end, five of the seven alternatives would raise the first generation's cost (by
up to $1.7bn) and two would lower it (by up to $3.1bn). At the high end the count is four and three.
Under (b) it is four and three at the low end and three and four at the high end. The central rules
sit inside every band.
The ratio-type lanes are scaled by each generation's own stack factor. That leaves a non-additive
remainder of at most $0.43bn, which is spread by the generations' cells after the stack.

**Lane contributions by generation**, $bn a year, low / high:

| Lane | (a) G1 | (a) G2 | (a) G3+ | (b) G1 | (b) G2 | (b) G3+ |
|---|---|---|---|---|---|---|
| Tax-records stack | +15.1 / +18.1 | +2.6 / −0.2 | +2.2 / +3.2 | +16.1 / +18.2 | +1.3 / −0.2 | +2.5 / +3.2 |
| CBO re-key | +1.1 / +1.0 | +5.1 / +3.9 | +3.0 / +3.5 | +1.6 / +0.7 | +3.9 / +4.0 | +3.9 / +3.6 |
| OTA re-key | −0.1 / −0.1 | −0.2 / −0.1 | −0.1 / −0.1 | −0.1 / −0.1 | −0.2 / −0.1 | −0.1 / −0.1 |
| Premium credits (row 1) | −4.0 / −11.4 | −6.5 / −2.2 | −3.7 / −0.6 | −8.9 / −10.3 | −3.5 / −2.9 | −1.8 / −1.0 |
| Pooled medical and LTSS | −5.5 / −5.5 | −5.3 / −5.3 | −6.1 / −6.1 | −6.3 / −6.3 | −5.1 / −5.1 | −5.4 / −5.4 |
| Schools and college | +1.0 / +3.6 | −0.6 / −2.6 | +0.3 / −1.5 | −0.5 / −1.3 | +0.3 / +0.4 | +0.9 / +0.4 |
| Benefit keys | +0.5 / +0.7 | +0.9 / +0.8 | +0.8 / +0.6 | +0.7 / +0.7 | +0.9 / +0.8 | +0.6 / +0.5 |
| Justice | +0.5 / +0.5 | +0.8 / +0.8 | +0.7 / +0.7 | +0.5 / +0.5 | +0.8 / +0.8 | +0.7 / +0.7 |
| Lane constants | −2.6 / −2.6 | −1.1 / −1.1 | −1.3 / −1.4 | −2.8 / −2.8 | −1.1 / −1.1 | −1.2 / −1.2 |
| Total correction | +6.0 / +4.3 | −4.2 / −6.1 | −4.2 / −1.6 | +0.4 / −0.7 | −2.7 / −3.4 | −0.0 / +0.7 |

The CPS lane prints `[DEGRADED] impute_status: Medicaid clause …` whenever its status function runs.
The warning describes the uncorrected status rule. The adopted stack's state-aware flag is its
repair, and this split carries that flag by generation.

## Step 6: the September 19 ledger beside the account

The ledger's groups keep children in their own generation, so they match convention (a). Their
populations equal this lane's to the person; the ledger and this lane use the same CPS ASEC 2025
frame. Every figure below is a net balance in $ per person a year (negative means the group costs
others). Each row is computed in its own object, and nothing is scaled from one object onto the other.
[CALCULATION: `compare_ledger.py` → `derived/ledger_comparison.csv`; the ledger is read through
`lifetime.load_age_profiles`, which verifies its hashes]

| $ per person a year | G1 shared | G2 shared | G3+ shared | G1 personal | G2 personal | G3+ personal |
|---|---|---|---|---|---|---|
| Ledger: published gap to third-plus NH whites, at the whites' ages | −7,584 | −7,521 | −6,195 | — | — | — |
| Ledger: the same gap from its eight age bands | −7,525 | −7,443 | −6,116 | −7,830 | −6,799 | −6,018 |
| Ledger: gap at the group's own ages | −9,806 | −9,820 | −6,685 | −12,394 | −6,166 | −4,598 |
| Ledger: the whites' own balance at the group's ages | +3,877 | +3,940 | +2,461 | +8,963 | −633 | −2,365 |
| Ledger: the group's own balance | −5,929 | −5,881 | −4,223 | −3,431 | −6,798 | −6,963 |
| Account: direct lines at average cost, before corrections | −7,635 | −8,882 | −7,015 | −5,751 | −9,804 | −9,689 |
| Account: the same lines at the adopted responses | −5,448 | −6,165 | −4,294 | −4,505 | −7,171 | −7,014 |
| Account: plus the production term (September 23 case) | −4,726 | −5,996 | −4,149 | −4,028 | −7,059 | −6,919 |
| Account: plus the corrections (adopted main case) | −5,220 | −5,703 | −3,859 | −4,383 | −6,636 | −6,808 |

The published gaps come from the shared allocation, and the eight-band recomputation lands within
0.8–1.3% of them.

- **Reference group.** The published figure is a gap to third-plus non-Hispanic whites, weighted to
  the whites' ages. At the Mexican-origin groups' own ages, those whites are net contributors under
  the shared allocation: +$2.5k to +$3.9k per person. A gap therefore exceeds the group's own
  balance. The groups' own balances are 22–32% smaller than the published gaps. Age weighting moves
  the gap too. Under the shared allocation it is larger at the groups' own ages than at the whites'.
- **Object.** The ledger charges services at average cost, charges pure public goods nothing and has
  no production term. The account differs in its line set, receipt rules and keys. At average
  cost (the package's proportional reference), it charges these people $1.7k to $3.0k per person more
  than the ledger. Pricing services at the adopted marginal responses then takes off $2.2k to $2.7k
  at the shared end ($1.2k to $2.7k at the personal end). That brings the direct lines to within
  $71–481 per person of the ledger's balance at the shared end. The first of these two differences
  is not decomposed here, so the near-agreement confirms neither object. The production term takes
  off a further $722, $169 and $144 per person at the low end.
- **Corrections.** The ledger carries none of the 270 corrections. At the low end they add $494 per
  person to the first generation and take $293 and $291 from the second and third-plus.
- **Order.** Both objects put the third-plus lowest under the shared allocation and the first
  generation lowest under the personal one. Under shared, the ledger has the first and second
  generations within $50 of each other, while the account puts the second $480 above the first.
  Under personal, both put G3+ about $170 above G2, with G1 well below.

The ledger answers how a group compares with third-plus whites of the same age. This split answers
what each generation alive in 2024 costs everyone else under the adopted account. Neither is a test
of "their children pay it back", which concerns future taxes and needs a cohort account with the
corrections carried into it. [INFERENCE] The FAQ rule holds here: the ledger's generation gaps must
not be scaled onto the $201–246bn, and this lane computes the split directly on the account.

## Sources and method notes

**National Academies convention (step 5b).** Verified in the local copy of the report
(`sources/immigration-fiscal/data/external/nas_2016/23550.pdf`), chapter 8, printed pages 387–388:
"The first group consists of first generation immigrants (the foreign-born) ages 18 and older, plus
their dependent first and second generation children (see Box 8-2). The second group consists of
independent individuals (those ages 18 and older) in the second generation plus their dependents
(who typically are third generation by nativity status)." Footnote 12: "For all three groups,
dependent children—identified at the individual level in the CPS data—are included in their
parents' generational group." Page 388: "Dependent children are assigned to the parental generation
if one or more independent parents are present in the household. If there are no parents in the
household, then the generational group of the oldest co-resident independent relative is assigned.
Defining generational groups in this way attributes the costs to governments associated with
dependent children—most notably, in terms of magnitude, public expenditures on education—to the
generation of a parent or relative responsible for raising the child." Footnote 13 assigns a child
whose parents are in different generations at random, half to the mother's generation and half to
the father's. Box 8-2 (printed page 377) defines dependents more widely than minors: anyone under 18,
18–21-year-olds in high school full time, 18–23-year-olds in school with income below half the
one-person poverty level, and some low-income single 18–23-year-olds living with a parent.
[SOURCE: National Academies of Sciences, Engineering, and Medicine (2017), *The Economic and Fiscal
Consequences of Immigration*, pp. 377, 387–388, doi:10.17226/23550]

Convention (b) here follows the brief's wording, minors only. A minor goes to the generation of the
co-resident parents in the union, split 50/50 if they are in two generations. Failing that, the
minor goes to the oldest union adult relative in the family, and otherwise stays in their own
generation. The split 50/50 replaces the NAS random draw with its expectation. Dependents aged 18–23
stay in their own generation, which leaves some college costs with the second generation that NAS
would move to the first. [INFERENCE]

**How the CPS records parents' birthplaces (step 0).** The household roster asks every member "What
is his/her mother's country of birth?" and "... father's country of birth?" (items MNTVT and FNTVT).
The questions are asked in the first month in sample and for members added later. The answers are
reported for the person, not copied from a linked parent record. [SOURCE: Census Bureau, *Current
Population Survey Design and Methodology*, Technical Paper 77 (2019), Table 3-2.5 part 2, p. 123;
ASEC 2025 data dictionary, PEMNTVTY/PEFNTVTY universe "All Persons"]

In the union, 54% of members (75% of adults) live without a linked parent, and their generation rests
on these reported items alone. The items are allocated for 4.8% of those members, against 2.7% of
members who live with a parent. Where a biological parent lives in the household, the member's report
agrees with that parent's own birthplace 96.4% of the time (G1 98.8%, G2 97.0%, G3+ 95.2%).
[CALCULATION: `parents_check.py` → `derived/parent_birthplace_check.csv`] A disagreement rate of at
least 3–5% therefore likely applies to the non-co-resident majority as well, whose answers cannot be
checked. The G2/G3+ boundary carries that error. [INFERENCE] The same mismatch shows under (b): 0.35m
third-plus minors live with a Mexico-born parent, so they count with the first generation.
[DATA: `derived/minors_convention_b.csv`] That parent is a step- or adoptive parent, or the minor's
reported parents' birthplaces disagree with the parent's own. [INFERENCE]

**Production term (step 3).** The account's CES production block is not linear in the union's
labor, so it has no unique generation split. I attribute it along the proportional removal path
(Aumann–Shapley: the path integral splits P and F exactly across the two skill cells). Within each
cell, the split follows each generation's share of the union's positive earnings there. **This is a
first-order attribution, not a counterfactual.** At the model's reference scenario:

| $bn a year, P + F | Union | G1 | G2 | G3+ |
|---|---|---|---|---|
| Attribution, cash normalization (high end), (a) | 8.79 | 5.82 | 1.60 | 1.37 |
| Attribution, GDP normalization (low end), (a) | 13.32 | 8.82 | 2.43 | 2.07 |
| Remove this generation alone, cash (does not add up) | — | 3.69 | 0.25 | 0.18 |
| Split by total labor income, cash | 8.79 | 3.17 | 2.82 | 2.80 |

[CALCULATION: `production.py` → `derived/production_by_generation.json` `reference`] The term is
almost entirely induced receipts: at the cash reference, F is +$8.95bn and P is −$0.16bn. Its positive
part comes from the high-school-or-less cell (+$12.7bn), while the other cell is −$3.9bn. The first
generation earns 53% of the union's labor income in the first cell and 22% in the second, so it
carries two thirds of the term. Removing one generation alone gives much less than its attribution,
because P + F rises faster than linearly in the removed share. Splitting by total labor income would
raise the first generation's cost by $2.7–4.0bn and lower the other two by $1.2–2.2bn each.

## Would change it

- **Flagged rules.** A measured generation split of the flagged corrections, meaning benefit receipt
  and justice use by parents' birthplace, would replace the proportional rules. Each moves a
  generation by $2bn or less.
- **Production term.** A counterfactual production model would replace the first-order attribution.
  The first generation's share runs from $3.2bn (labor-income split, cash) to $8.8bn (attribution,
  GDP).
- **Future taxes.** A cohort account of today's children would be needed to test "their children pay
  it back".
- **Main case.** A change to the main case itself (service responses, the production term) would move
  every generation. The convention and allocation choices stay framing.

## Reproduce

`bash infra/immigration-fiscal/generation_account_2026_09_24/run_all.sh` runs every step in
dependency order, stops at the first failed gate, and ends by re-running
`main_case_2026_09_24/main_case.cjs`. Headline cell: `derived/generation_results.csv`, row `a,G1,low`,
`cost_bn` 63.793787.

The steps can also be run one at a time from the repository root with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`, in this order: `test_masks.py`
(through `-m pytest … -p no:cacheprovider`), `parents_check.py`, `mixed_units.py`, `keys.py`,
`production.py`, `build_models.py`, `stack_split.py`, `external_split.py` (add `--with openpyxl`),
`correction_rules.py`, `node run_generations.cjs`, `compare_ledger.py`. The scripts set
`sys.dont_write_bytecode`, so they leave no bytecode beside the lanes they import. `_cache/` holds the
CPS frame parquet (ignored); `frame.load()` rebuilds it from the hash-checked ASEC zip.

Covered: every input the brief names, through `model.json`'s reproduction (step 2), and every lane in
`package.cjs` `packageShifts` (step 4). Skipped: none. Derived outputs total 3.7 MB, of which
`production_by_generation.json` (0.9 MB, all 3,888 scenarios) is the largest.
