**Verdict:** The candidate `sept28_candidate` (not adopted) is **$323.68–388.70bn**, up **+$1.86bn at specification 48
and +$1.33bn at specification 11** from the September 27 case ($321.82–387.37bn); its end specifications stay 48 / 11.
Transfer consolidation adds +$0.22bn at both ends and production on the account's weights +$1.64 / +$1.11bn; the two
add exactly. The road arm keeps its September 27 setting, a smaller stationary network, inside the band. Its two other
cases, **replacement adjustment (−$5.23 / −$10.75bn) and a fixed stock (−$10.51 / −$17.97bn), belong beside the range,
not in it**: each raises the congestion item beside the account by +$5.17 / +$7.14bn, so net of congestion they move the
total by −$0.06 / −$3.60bn and −$5.34 / −$10.83bn. Public pay, a variant beside the range, raises the candidate by
**+$13.61 / +$8.95bn**, more than the whole production term. The sign break-even is **2.8–13.1%** (September 27:
2.8–13.6%), or −3.1% to 9.0% with the enterprises held at 1. The outer range is **$260.5–437.4bn** ($292.8–409.6bn in
quadrature). All 88 gates pass (20 + 10 + 43 + 15) and a second run through `scripts/rerun_lane.py` is byte-identical
(9/9 files).

## Result

Every comparison is at the fixed specifications, 48 (low end: shared allocation, GDP normalization, general government
0.6000, 2%) and 11 (high end: personal, cash, 0.8504, 3%), with the two fill-in methods averaged. None is a difference
of band ends. [CALCULATION: `main_case.cjs` → `derived/fixed_specs.csv`, `derived/candidate_bands.csv`]

### Old → new at specifications 48 / 11 ($bn)

| Item | Spec 48 | Spec 11 | Placement |
|---|---|---|---|
| September 27 case | 321.8194 | 387.3701 | adopted |
| 1. Transfer consolidation alone ($5.257811bn) | 322.0400 (+0.2207) | 387.5907 (+0.2207) | in the candidate |
| 1. Its bound, all of line 4 ($60.261bn) | 324.3484 (+2.5290) | 389.8991 (+2.5290) | beside |
| 2. Production on the row-4 weights alone | 323.4621 (+1.6427) | 388.4774 (+1.1074) | in the candidate |
| 3. Road arm: stationary network (the September 27 setting) | 321.8194 (0) | 387.3701 (0) | in the candidate |
| 3. Road arm: replacement adjustment alone | 316.5888 (−5.2306) | 376.6242 (−10.7459) | beside |
| 3. Road arm: a fixed stock alone | 311.3117 (−10.5077) | 369.3953 (−17.9748) | beside |
| **Items 1–3 together: the candidate** | **323.6827 (+1.8634)** | **388.6981 (+1.3280)** | |
| Candidate, road arm at replacement adjustment | 318.4522 (−3.3672) | 377.9522 (−9.4178) | beside |
| Candidate, road arm at a fixed stock | 313.1750 (−8.6443) | 370.7233 (−16.6467) | beside |
| 4. Public pay on the September 27 case | 336.4442 (+14.6248) | 397.0199 (+9.6499) | beside |
| 4. Public pay on the candidate (change from the candidate) | 337.2913 (+13.6085) | 397.6501 (+8.9520) | beside |

Each item moves only its own lines, and the items add exactly: the candidate and every variant row equal the sum of
their items' changes at every specification within 1.1e-13bn.

### The candidate band and the outer range

| | Band | Outer range | In quadrature |
|---|---|---|---|
| September 27 case | 321.82–387.37 | 258.65–436.05 | 290.90–408.23 |
| **Candidate** | **323.68–388.70** | **260.52–437.37** | **292.76–409.56** |
| Candidate with the road arm in the range | 313.18–388.70 | 250.01–437.37 | |

The outer range re-runs the September 27 case's 19 components on the candidate at every specification. On the
September 27 case the same code reproduces its published range exactly. The components hardly move: the tax block
narrows by $0.006bn and no other component changes by more than $0.005bn. The range therefore follows the centre.
[CALCULATION: `derived/components.csv`; `summary.json` `range`]

### Item 1: transfer consolidation

- **The rule.** The transfer leaves both legs before keying (`package.cjs` `consolidate()`). Both national totals fall
  by T: housing_subsidies from $60.261bn to $55.003bn and enterprise_surplus from −$47.46bn to −$52.72bn. Every cell
  keeps its attributed fraction, so both keys (rental 0.0740 / 0.0764 by fill-in method, mean 0.0752; enterprise 0.1172) and the
  enterprise capital key are unchanged to 1e-15.
- **The cost.** It moves by r_e·ke·T − r_h·kh·T, which is +$0.2207bn at both ends. Nothing else moves: no other line
  and no capital component.
- **The amount.** T = $5.257811bn, public housing's FY2024 operating-subsidy obligations: formula grants $5,232,640k
  plus shortfall prevention $25,171k. [SOURCE: HUD FY2026 Congressional Justification, Public Housing Fund, p. 4-2]
- **The positive control.**
  - Today a synthetic $1bn on both legs moves the case by kh − ke at every specification. At specification 48 with
    capital off, that is −$43.19m and −$40.75m by fill-in method, the audit's $40.75–43.19m (3db388d §7), reproduced.
  - After consolidation the synthetic $1bn moves the case by exactly 0 at every specification. This holds in the main
    profile, long_run_non_school_fixed, the proportional reference, with the enterprise receipt at 0.37, and on the
    candidate's production.
- **The bound.** Consolidating all of line 4 gives +$2.5290bn, the September 27 case's overlap bound.
- **What is not included.** Section 8 paid to housing authorities as landlords is unpublished detail (NIPA Handbook
  ch. 12). It lies between T and that bound.

### Item 2: production on the account's weights

- **The reproduction.** `conceptual_audit_2026_09_27/probe_production.py` reruns byte-identical.
- **The grid.** `production_row4.py` rebuilds all 3,888 production cells on both weights. On the published weights
  every cell reproduces `model.json` within 5e-10bn before rounding (within 2e-9 after both files' 1e-9 rounding).
- **The reference cell.** P+F falls from 13.3226 to 11.6799 (GDP) and from 8.7906 to 7.6832 (cash). The cost
  therefore rises by **+$1.6427 / +$1.1074bn**, the audit's figures. No line and no capital component moves.
- **The sampling SE of P+F.** It falls from 1.1243 to 1.0350 (GDP) and from 0.7374 to 0.6764 (cash).
- **The sign break-even.** The row-4 grid is also carried through the break-even's full production grid (below).
  [CALCULATION: `derived/production_row4.json`]

### Item 3: the road arm

The decision's three physical cases put operations, depreciation, the road capital return and lane capacity together.
Each case is run at every specification, with the congestion item beside the account at the same lane cut.
[CALCULATION: `derived/road_arm.csv`, `derived/road_congestion.json`]

| Case (roads) | Follows the long-run road response | Account change, 48 / 11 | Congestion beside (change) | Net |
|---|---|---|---|---|
| Stationary network (candidate) | operations, depreciation, return, lanes | 0 / 0 | 13.99 / 12.02 | 0 / 0 |
| Replacement adjustment | operations, depreciation | −5.23 / −10.75 (return) | 19.16 (+5.17 / +7.14) | −0.06 / −3.60 |
| Fixed stock | operations | −10.51 / −17.97 (return 5.23 / 10.75, depreciation 5.28 / 7.23) | 19.16 (+5.17 / +7.14) | −5.34 / −10.83 |

- **Congestion.** With lanes fixed it is the B1, $19.16bn (factorial $8.05–35.25bn). With the network following
  spending it is $13.99bn (factorial $2.01–32.05bn) and $12.02bn (−$0.92–30.83bn). These come from the response
  lane's own functions; its bridge rows reproduce first.
- **The long-run response, now varied with its congestion** (stationary network; changes at 48 / 11):

  | Long-run variant | Account | Congestion | Net |
  |---|---|---|---|
  | r = b | −0.33 / −0.04 | +0.09 / 0 | −0.24 / −0.04 |
  | within states, uncapped | 0 / +15.54 | 0 / −3.22 | 0 / +12.32 |
  | federal fixed at the high end | 0 / −6.05 | 0 / +0.07 | 0 / −5.98 |
  | across states at the high end | 0 / −8.12 | 0 / +1.93 | 0 / −6.20 |
  | held-at-zero lines at 1 | +12.38 / +12.38 | 0 / 0 | +12.38 / +12.38 |

  - Read jointly, the range component's spread at the high end is −6.20 to +12.38 against −8.12 to +15.54 for the
    account alone.
  - The range itself is unchanged, because congestion sits beside the account.
  - The two fixed-lane cases at every variant are in `road_arm.csv`.
- **Placement: beside the range.**
  1. *The pieces are dependent.* Each case's account move comes with an opposite move of the congestion item. The
     account range would take the −$10.5 / −$18.0bn while the +$5.2 / +$7.1bn stays outside it. That is the dependent
     double error bar the audit (§6) describes.
  2. *Replacement adjustment is a transition.* Capital that is not replaced shrinks toward the stationary network.
     Since 2026-09-27 the account is the long-run state. The first-year budget response sits beside it for the same
     reason.
  3. *A fixed stock changes a premise.* No measured response here supports it or excludes it: the operations
     regressions do not measure the stock. The question is whether networks adjust at all. The September 27 case
     reports premise changes beside the range (option A for the enterprises, the 7% rate).
  4. *If the operator prefers the range,* the band becomes $313.18–388.70bn and the outer range $250.01–437.37bn. The
     congestion item beside would then run from $12.02bn to $19.16bn.
- **Parks are outside the arm,** following the decision and the brief. Under a fixed park stock their capital return
  ($0.95 / $1.64bn at 48 / 11) and their depreciation would also stay.

### Item 4: public pay (beside the range)

- **The charge.** Public employers pay the production model's wage change for their workers, skill group by skill
  group. The public payroll share of incumbent earnings (CPS ASEC 2025, longest job federal, state or local) is 7.63%
  for high school or less and 14.40% for more.
- **Sign and size.** It **raises** the group's cost: **+$13.61bn at specification 48 (GDP) and +$8.95bn at 11 (cash)**
  on the candidate, and +$14.62 / +$9.65bn on the September 27 production.
  - By skill: the less skilled −13.43 / −8.84 (public employers pay them less), the more skilled +27.04 / +17.79.
  - By level: federal 3.32 / 2.18, state 5.67 / 3.73, local 4.61 / 3.03.
- **Against the production term.** The charge exceeds the whole production term: P+F less the charge is −$1.93 /
  −$1.27bn.
- **The ends move.** With public pay the band is $336.63–398.31bn, because the charge differs by normalization. The
  fixed-specification figures above are the comparison.
- **Scope.** The variant assumes full pass-through of market wages to public pay. The GDP normalization prices the
  labor gains on a compensation scale, the cash normalization on CPS earnings.

### Sign break-even

The definition is `main_case_2026_09_24/sign_reversal.cjs`'s, with the September 27 additions inside it. Each column is
the September 27 payload with the candidate's items; the road arm does not enter, because the definition sets roads at
s.

| Measure | September 27 | Item 1 | Item 2 | Candidate |
|---|---|---|---|---|
| Break-even, enterprises moving with services | 2.83–13.60% | 2.92–13.68% | 2.70–12.99% | **2.79–13.07%** |
| Break-even, enterprises held at 1 | −2.87% to 9.65% | −2.93% to 9.59% | −3.01% to 9.01% | **−3.07% to 8.95%** |
| Frozen services, capital fixed ($bn welfare) | −53.49 to 57.77 | −53.71 to 57.55 | −54.01 to 53.93 | −54.23 to 53.71 |

Each cell runs from the personal allocation's low to the shared allocation's high. Per allocation they are in
`derived/sign_reversal.csv`. [CALCULATION: `sign_reversal.cjs`]

### Validation

- **Gates.** `production_row4.py` 20, `road_congestion.py` 10, `main_case.cjs` 43 and `sign_reversal.cjs` 15, all
  passing. On a failed gate each script exits 1 and writes nothing.
- **The September 27 case.** With every item off the package reproduces it at every specification exactly, including
  its committed `per_spec.csv`, and reproduces its range and its sign-reversal csv.
- **An independent path.** The engine, `model.json`, the September 27 `corrections.json`, T and the row-4 grid give the
  candidate at every specification within 2.3e-13bn.
- **Reproducibility.** A first run in place, then a second through
  `uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/main_case_candidate_2026_09_28 "uv run --no-project python3 {lane}/production_row4.py" "uv run --no-project python3 {lane}/road_congestion.py" "node {lane}/main_case.cjs" "node {lane}/sign_reversal.cjs" --allow-unrun infra/immigration-fiscal/main_case_candidate_2026_09_28/package.cjs`
  gives IDENTICAL, 9/9 files, rc 0. `package.cjs` is a module that every command loads.
- **Output hashes (sha256).**

  | File | sha256 |
  |---|---|
  | candidate_bands.csv | `4133acb398bf13f38056897c29ecf5706b4ec6104a1e5bb4013033d0729eb1fc` |
  | components.csv | `22a476f5c7cd1f20ada9adbfa734692ea1974c88b56c524e8e702c0bffb09eb2` |
  | fixed_specs.csv | `f842b4ed59a1f9740b0a6b25a1a030e07de98aff416843f14d5c2cd988469b7e` |
  | per_spec.csv | `87fd04d3e38585cbf60f165168c46bc5cdb3f374bb523d4a7b39c1db6ff9d769` |
  | production_row4.json | `69839e58a9601363562c0884ae1f7ba9ed7c25086cb3eb545e181806704ac3ac` |
  | road_arm.csv | `7d05b3aad2bdcb48c1cd4ea6f2a57dec654be0687928b7cdfa5ea951609f4d85` |
  | road_congestion.json | `a89c7e280bc97d4b2961c6a3582bdeb81c6004b208c13ca257127c573cde6987` |
  | sign_reversal.csv | `74164ba579fb4f29bfa8168f03bf6ff181a17b0bbb7247ec8b18d990e2a9c572` |
  | summary.json | `4d8c0821fc653277098b8c94fd0732b8078ea6d867fe48694f69ff80b4c4eaea` |

### Files

- `package.cjs` holds the definitions and imports the September 27 package unchanged.
- `production_row4.py` writes `derived/production_row4.json`: the grid on both weights and the public-pay charge.
- `road_congestion.py` writes `derived/road_congestion.json`: congestion at every long-run road response.
- `main_case.cjs` writes `candidate_bands.csv`, `fixed_specs.csv`, `components.csv`, `per_spec.csv`, `road_arm.csv`
  and `summary.json`.
- `sign_reversal.cjs` writes `sign_reversal.csv`.
- Run them in that order. `_cache/` holds the NIPA and HUD primary texts and is ignored.

### For adoption (not done here; the brief forbids touching the engine and the payload)

1. **The payload cannot yet carry the candidate.** The corrections format holds national totals fixed, but
   consolidation changes two of them, and item 2 replaces the production grid. Adoption needs a payload extension (the
   two national edits and a pinned production grid) or an engine operation. Consumers that apply `corrections.json`
   would otherwise miss +$1.86 / +$1.33bn.
2. **The uncertainty lane's sampling SE should be re-run on the row-4 grid.**
3. **Consumer lanes then move once:** generations, back-cast, distribution, uncertainty and debt.
4. **The consolidated amount covers public housing's operating subsidies only.** The unpublished Section 8 part to
   housing authorities is bounded at +$2.53bn.

## Log (append-only)

- 2026-09-28: stub written after reading `BRIEF.md` (e003ea1). Case name `sept28_candidate`; imports the
  September 27 package (`main_case_long_run_2026_09_27`, f3031ab plus the uncommitted follow-up, if any).

Worker: mainbuild, model claude-opus-5-5.
- 2026-09-28 (correction to the line above): the September 27 lane is fully committed, f3031ab plus 7e94324; there is
  no uncommitted follow-up. The candidate imports that committed package.
- 2026-09-28, sources read before building (no numbers are final yet):
  - Item 2. `conceptual_audit_2026_09_27/_cache/production.json` (the probe's output of 2026-09-27 23:33) holds P+F
    13.322598 → 11.679878 (GDP) and 8.790628 → 7.683239 (cash) on the row-4 weights (naturalized × 0.8556, 943
    records; noncitizens × 0.7781, 2,139 records; 40.897m → 39.712m). The probe is rerun in this lane, not trusted
    from the cache.
  - Item 2 reaches the sign break-even too: `main_case_2026_09_24/sign_reversal.cjs` ranges over 432 production
    cells (capital adjusted) and its frozen row over 432 more (capital fixed). A reference-cell-only reweight would
    leave those cells unweighted, so this lane rebuilds the whole 3,888-cell grid on both weights and gates the
    published weights against `model.json` cell by cell first.
  - Item 1. NIPA Handbook ch. 12 (March 2022), p. 12-8: Section 8 payments go to landlords, "Estimates are provided by
    type of landlord (nonprofit, private, and state and local enterprises)", and footnote 13: "For state and local
    enterprises that provide housing, net operating income is comprised of federal subsidies and rental payments
    received by tenants, less expenses." The split by landlord is unpublished ("Aggregate of unpublished detail from
    BEA's Federal Budget Translation"). MP-5, S&L enterprises: "Estimates of subsidies paid by the Federal government
    to state and local government housing enterprises are also added, because COG/GF records these as
    intergovernmental receipts." [SOURCE: `_cache/nipa/chapter-12.pdf`; capital lane `_cache/bea_mp5_government_transactions.pdf`]
  - Item 1's documented amount: HUD FY2026 Congressional Justification, Public Housing Fund, "Summary of resources by
    program", FY2024 obligations: Public Housing Formula Grants (Operating Expenses) $5,232,640k; Shortfall
    Prevention $25,171k. [SOURCE: `_cache/hud/2026_CJ_Program_PH_Fund.pdf`, p. 4-2,
    https://www.hud.gov/sites/dfiles/CFO/documents/2026_CJ_Program_PH_Fund.pdf] HUD's TBRA justification: "rent
    partially covered by a subsidy paid directly to the landlord", so vouchers reach government enterprises only where
    a housing authority is the landlord, the unpublished part.
- 2026-09-28, item 2 reproduced (confirmed):
  - `conceptual_audit_2026_09_27/probe_production.py` rerun as its README says: exit 0, its own gates pass, and its
    output `_cache/production.json` is byte-identical to the one it wrote on 2026-09-27 (sha256 00436636…ceb4cb).
  - `production_row4.py` (this lane) rebuilds all 3,888 production cells on both weights. On the published weights
    every cell reproduces `model.json`: P and F within 5.0e-10bn, the sampling SE within 5.0e-10bn (model.json
    rounds to 1e-9). The reference cell: P+F 13.322598 → 11.679878 (GDP), 8.790628 → 7.683239 (cash), so the cost
    rises by **+$1.642719bn / +$1.107389bn**, the audit memo's figures. Row-4 factors 0.855626 / 0.778127 on the
    point weight; each replicate is raked to the same ACS total (0.795–0.926 / 0.740–0.816).
  - Reference-cell sampling SE of P+F: 1.1243 → 1.0350 (GDP), 0.7374 → 0.6764 (cash).
- 2026-09-28, item 4 computed (confirmed; the variant is not yet run through the package):
  - Public payroll share of incumbent earnings: 7.63% (high school or less), 14.40% (more than high school). CPS
    ASEC 2025 longest job federal, state or local (LJCW 2–4), wage and salary (ERN_SRCE 1): $169.6bn and $1,337.7bn.
  - Incumbent labor gain from the group's presence (row-4 weights): GDP −$176.17bn / +$187.85bn by skill; cash
    −$115.89bn / +$123.57bn. The public employers' share: GDP −13.43 + 27.04 = **+$13.61bn**; cash
    −8.84 + 17.79 = **+$8.95bn** (published weights +$14.62bn / +$9.65bn). It raises the group's cost: the public
    workers' wage gain from the group's presence is in P+F and the charge takes it back out.
- 2026-09-28, the candidate built (confirmed in scratch runs; final runs and hashes below when written):
  - `main_case.cjs`: 43 gates pass. With every item off, the candidate package is the September 27 case at every
    specification exactly (and its committed `per_spec.csv`). Candidate band **$323.6827–388.6981bn**, end
    specifications still 48 / 11 in both methods. Items at 48 / 11: consolidation +0.2207 / +0.2207, production
    +1.6427 / +1.1074, together +1.8634 / +1.3280, additive to 1e-13.
  - `road_congestion.py`: the congestion bridge's four rows, B1 and factorial ranges reproduce; congestion priced at
    every long-run variant's highway response (10 gates).
  - `sign_reversal.cjs`: 15 gates pass; the September 27 columns reproduce its committed csv.
- 2026-09-28, final: all four scripts run in place (rc 0), then again through `scripts/rerun_lane.py`: IDENTICAL,
  9/9 files. The road arm's placement (beside the range) is a recommendation; adoption is the operator's call after the
  propagation. The verdict above replaces the pending stub; the log entries above it are unchanged.
