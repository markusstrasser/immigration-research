claude-opus-5-5

**Verdict:** Moving the payable paths (OASDI and HI) from Note 2025.7 and the 2025 Trustees Reports to the 2026 reports lowers the accrual. OASDI falls from 0.974 to 0.951 per on-books tax dollar, net of the income tax on benefits (−2.4%), and Part A from $2,004 to $1,935 per covered worker-year (−3.4%). Main case v5 moves from $390.29–461.24bn to $385.93–457.09bn (−$4.36 / −4.15bn, by an engine run), and the cash set stays at $307.38–383.41bn. The same reports also raise wage growth and HI costs. Taking every 2026 input the lane can read gives −$1.73 / −1.63bn instead ($388.56–459.61bn). Keeping the trust funds separate, as current law does, lowers the case by a further $1.0–1.2bn on either report. All gates pass, the rerun is IDENTICAL 17/17 (exit 0) and the 6 tests pass. [CALCULATION: derived/case_oct05.json, summary.json]

# Pension accrual on the 2026 Trustees payable path

Status: complete on 2026-10-07 (third worker, after two restarts). Files were created in this lane only, and nothing is
committed. Every figure below is computed from the staged primary tables. The model values are modelled, with their
inputs stated in "Construction".

## Answer

The headline arm `tr2026` swaps only the payable paths, as the brief asks. It keeps Note 2025.7's Table 3 level and the
2025 report's other parameters. All figures are for the union of the pension lane's frame. The per-dollar measures do
not depend on the case frame; the case figures are main case v5 at its ends (specifications 48 and 11).

| Measure | 2025 reports (adopted) | 2026 payable paths | Change |
|---|---:|---:|---:|
| OASDI accrual per on-books tax dollar, gross | 1.018378 | 0.994203 | −2.37% |
| Net of the income tax on benefits (`ratio_net`) | 0.973667 | 0.950603 | −2.37% |
| Part A accrual per covered worker-year | $2,003.59 | $1,935.11 | −3.42% |
| Part A accrual per HI tax dollar | 1.4609 | 1.4110 | −3.42% |
| Part A accrual, union | $41.137bn | $39.731bn | −$1.406bn |
| Main case v5, low / high | $390.29 / 461.24bn | $385.93 / 457.09bn | −$4.36 / −4.15bn |
| Pension accrual in the case (set − cash), low / high | $82.91 / 77.83bn | $78.55 / 73.68bn | −$4.36 / −4.15bn |
| Per member of the 42.75M lineage | $9,129–10,789 | $9,027–10,692 | −$102 / −97 |
| Cash set (no accrual) | $307.38–383.41bn | $307.38–383.41bn | 0 |

[CALCULATION: derived/arms.csv, case_oct05.json] The table uses controlled rounding: five figures sit $0.01bn from
their own rounding, so that its rows and columns add. Unrounded, the 2026 case is $385.936–457.097bn and the pension
accrual $82.918 / 77.834bn on the 2025 reports and $78.560 / 73.688bn on the 2026 paths.

The change differs by generation, because the cut falls on benefits paid late in the century.

| Generation | OASDI per tax dollar, gross | Part A per covered worker-year |
|---|---|---|
| G1 | 1.0771 → 1.0644 | $1,575 → $1,538 |
| G2 | 0.9730 → 0.9398 | $2,316 → $2,219 |
| G3+ | 1.0108 → 0.9852 | $2,232 → $2,152 |

G2 is the youngest group and loses the most. Its tax-weighted mean age is 36, against 40 for G3+ and 46 for G1.
[CALCULATION: derived/arms.csv; the pension lane's frame]

**What moves the case.** At the low and high ends, the change splits into four parts:

- the union's OASDI: −$2.59 / −2.43bn;
- the union's Part A: −$1.41 / −1.41bn;
- the lineage's 3.04M added people, OASDI: −$0.24 / −0.21bn;
- the lineage's 3.04M added people, Part A: −$0.12 / −0.10bn.

By source, the change is exactly additive:

- building the 2025 paths year by year from the tables, instead of the lane's anchors (`tables_2025`): −$0.19 / −0.19bn,
  nearly all of it HI;
- the 2026 OASDI path: −$2.83 / −2.64bn (`tr2026_oasdi` less `tables_2025`);
- the 2026 HI path: −$1.34 / −1.32bn (`tr2026_hi` less `tables_2025`).

[CALCULATION: derived/case_oct05.csv] Both lists are rounded by largest remainder so that they add to the printed
change. The high end's −0.21 and −2.64 are −0.204 and −2.634 unrounded.

**Engine run, not scaling.** `case_tr2026.cjs` evaluates the v5 payload with two edits per arm (social_security and
medicare) at all 64 specifications, through candidate v4's package-free consumer. Both lines respond at 1 and enter the
cost linearly, so the engine's change equals the edits' sum to 1.1e-13bn. First-order scaling would give the same
numbers.

**The cash set is unchanged by construction.** Its payloads carry no pension block (gated), so no path enters it.

**Why the path cut is larger than the depletion dates suggest.** OASDI still depletes in 2034 and HI in 2033 in both
reports. The 2026 OASDI path is higher than the 2025 one in 2035–2047 (0.827 against 0.808 in 2035). From 2048 it is
lower: 0.677 against 0.713 in 2070, and 0.654 against 0.719 in 2100. Workers of 2024 draw most of their benefits from
the 2040s to the 2080s. [INFERENCE: the frame's ages] HI is lower throughout: 0.930 against 0.968 in the depletion year, 0.856 against 0.865 in 2050
and 0.928 against 0.998 in 2100. [CALCULATION: derived/paths.csv]

## What the payable swap leaves out

Each row adds one 2026 input to `tr2026`. The effect is on main case v5, low / high.

| 2026 input not applied in `tr2026` | 2025 → 2026 | Effect | Arm |
|---|---|---:|---|
| Tax-on-benefits path. TR 2026 Tables IV.B1/B2 already carry the 2025 tax law; the lane uses TR 2025 × the OCACT letter's factors | future share taxed 4.39% → 4.57% | −$0.23 / −0.21bn | `benefit_tax_path_tr2026` |
| New-issue interest rates, Table V.B2 | +0.1 pt in 2025–26, −0.2 pt in 2035, ultimate unchanged | +$0.55 / +0.52bn | `interest_tr2026` |
| Wage index, Note 2026.3 Table 7 | AWI 2024 (actual) +0.54% over the 2025 projection, +2.4% by 2035, +2.9% by 2061; real earnings growth 2025–35 1.72% against 1.44% | +$1.18 / +1.10bn | `wage_index_tr2026` |
| COLAs and contribution bases, Table V.C1 | COLA 2.8% (Dec 2025) and 2.7% (2026) against 2.7% / 2.5%; base +0.5% in 2026, +2.0% in 2034 | +$0.04 / +0.03bn | `program_parameters_tr2026` |
| Mortality decline, 2025–2100 | 65+: 0.68% → 0.69% a year; all ages: 0.74% → 0.73% | +$0.14 / +0.14bn | `mortality_tr2026` |
| HI cost per beneficiary, MTR Table V.D1 | −1.0% (2024), −1.3% (2025), +0.7% (2030), +1.4% (2034) | +$0.94 / +0.93bn | `hi_costs_tr2026` |
| **All six, run jointly** (not the rows' sum) | | **+$2.63 / +2.52bn** | `all_2026_inputs` |

[SOURCE: tr2026 Tables IV.B1, IV.B2, V.B2, V.C1, sec. V.A; an2026-3 Table 7; mtr2026 Table V.D1;
CALCULATION: derived/case_oct05.json]

With all six, the case is **$388.56–459.61bn**: −$4.36 / −4.15bn from `tr2026`, plus the joint +$2.63 / +2.52bn, gives
−$1.73 / −1.63bn from the adopted case.

- **Interactions are negligible.** The rows add to +$2.62 / +2.51bn, within $0.01bn of the joint run.
- **Signs.** Faster wage growth raises the wage-indexed benefits that 2024's earnings buy. Higher HI costs raise the
  value of Part A. Lower mid-2030s rates raise present values. The 2026 report's benefit-tax path takes slightly more
  back.

Not applied, and not quantified:

- **Note 2026.3's scaled earnings factors.** The preliminary factors are 0.22% lower over a career, and the four
  adjustments are 0.1–0.2% higher (medium 1.221 → 1.223). The final sets therefore move by less than 0.1%, a negligible
  effect. [CALCULATION: an2025-3 against an2026-3 Table 6; INFERENCE for the size]
- **Assumptions that act only through the payable path, which `tr2026` applies.** These include the 75-year actuarial
  deficit (4.42% of payroll, against 3.82%), the lower ultimate fertility (1.75 against 1.90) and the other demographic
  assumptions. [SOURCE: tr2026, quoted in sources_tr2026.QUOTES]
- **Note 2025.7's Table 3 level.** SSA has not published a 2026 money's-worth note: the Note 7 index ends at 2025.7. The
  level therefore stays on 2025 assumptions, and the model's ratio of the two paths moves it. A 2026 Note 7 would let
  SSA's own cells replace that ratio. Its sign beyond the arms here is unknown.

## The separate-funds reading [FRAMING-SENSITIVE]

The combined reading follows the Trustees' headline, Note 2025.7 and the adopted lane. It is a convention that assumes
legislation. The Trustees write that full payment until the combined reserves are depleted "implicitly assumes that the
law will have been changed to permit the transfer of funds between OASI and DI as needed". TR 2025 has the same
sentence. [SOURCE: tr2026 sec. II.D; tr2025 sec. II.D]

Current law keeps the funds separate:

- **2026 report.** OASI is depleted in the fourth quarter of 2032. It then pays 78% of scheduled benefits, falling to
  62% by 2100. DI pays full benefits through 2100. [SOURCE: tr2026 Highlights and sec. II.D]
- **2025 report.** OASI is depleted in 2033 and then pays 77%. DI pays in full through 2099. [SOURCE: tr2025 sec. II.D]

**Construction.** The separate-funds path puts OASI's payable share on OASI's scheduled cost and full payment on DI's,
weighted by each fund's cost in the year (Tables IV.B1/B2).
- It is applied to all benefits, as Note 2025.7 applies the combined path. Note 2025.7's cells include disability
  benefits: "We consider all types of retirement, disability, and survivor benefits".
- [APPROX] The national cost weights stand in for each worker's own mix of OASI and DI benefits.
- The path stays between OASI's and full payment, and equals 1 before OASI's depletion (gated). It differs from the
  combined path mostly in 2032–2035, when OASI is cut before the combined fund would be.

| Reading | 2025 reports | 2026 payable paths | 2026, all six inputs |
|---|---|---|---|
| Combined (adopted convention) | $390.10–461.05bn (`tables_2025`) | $385.93–457.09bn (`tr2026`) | $388.56–459.61bn |
| Separate funds (current law) | $388.89–459.93bn | $384.82–456.06bn | $387.44–458.57bn |
| Separate less combined | −$1.21 / −1.12bn | −$1.11 / −1.03bn | −$1.12 / −1.04bn |

[CALCULATION: derived/case_oct05.json] The bands are the adopted case's printed $390.29–461.24bn plus each arm's
printed change, so that the differences hold. Five figures sit $0.01bn from their own rounding.

OASDI per tax dollar, gross, under separate funds: 1.0079 on the 2025 reports and 0.9846 on the 2026 paths.

**Superseded draft.** An earlier version of this arm put OASI's path on every benefit, DI's included. It gave
−$9.9 / −9.3bn. That overstated the cut, because current law pays DI in full and Note 2025.7's level includes
disability benefits. The arm was replaced before anything was reported (see the log).

## Recommendations

1. **The answer to the brief is `tr2026`: −$4.36 / −4.15bn.**
2. **When the case moves to the 2026 reports, take all six inputs together** (`all_2026_inputs`, −$1.73 / −1.63bn). The
   payable path alone mixes the 2026 report's benefit cuts with the 2025 report's wages, rates and HI costs. Within the
   same report, faster wage growth and higher HI costs offset most of the cut. The change is 0.4% of the headline, so I
   recommend folding it into the next case revision rather than revising for it alone. It changes the headline, so it
   waits for the operator's go.
3. **I recommend the separate-funds reading as the current-law central at that revision, with the combined reading as
   an arm.** It costs about $1.0–1.2bn more on either report, which is −$2.85 / −2.67bn from the adopted case on all
   six inputs. The reason is the operator's rule: current law leads, and readings that assume legislation go beside as
   arms. The Trustees state that the combined reading assumes such legislation. The case for keeping combined is that
   SSA's money's-worth notes and the Trustees' headline use it, so a reader comparing with SSA's figures sees the
   convention they know. The separate-funds path also rests on national cost weights [APPROX].

## Construction

**Why a naive swap shows almost nothing.** The OASDI accrual is Note 2025.7 Table 3's payable ratio, times the lifetime
model's factor k(person) / mwr(Note 2025.7's basis). Both parts of that factor are computed on the same path, so
swapping `payable_path` alone cancels in the ratio. Each arm instead uses Table 3 × k_new / mwr_base_2025:
- the numerator is on the new path, at the central's valuation (new-issue rates, general mortality);
- the denominator stays on the 2025 path that Table 3 carries, at Note 2025.7's own basis.

The arm equals the central exactly when the two paths are equal (gated). Part A reads its path directly. The timing of
the benefit tax follows each arm's OASDI path.

**The payable share.**
- **OASDI** is payroll tax / (cost − taxation of benefits), from Tables IV.B1/B2, because the income from taxing
  benefits falls with the cut. Income / cost does not reproduce the printed shares: for 2100 it gives 0.672, against
  0.65 printed.
- **The OASDI depletion year** blends in the reserves at its start (Table IV.B5 / IV.B4).
- **HI** is non-interest income / cost (Table III.B7). Its depletion year adds the start-of-year assets (Table III.B6),
  capped at 1.
- **Between and beyond table years.** Values are linear between the table's years, 1 before depletion and flat after
  2100.
- **Both reports use the same construction** (`tables_2025` against `tr2026`). The pension lane's own path, three
  Note 2025.7 anchors with straight lines between them, misses the 2025 path's dip to 0.695 in 2080. `anchors_2026`
  shows what the lane's form gives on the 2026 report: −$2.97 / −2.84bn. That understates the cut, because a straight
  line from 2035 to 2100 misses the 2026 path's deeper cuts in 2055–2095.

**The case.** `pension_tr2026.py` reproduces the pension lane's numbers on its own frame (the September 27 case). That
gives the per-dollar measures. `case_tr2026.cjs` carries them to v5 with two edits per arm:

- **social_security.** (ratio_net_arm − ratio_net) × the union's OASDI receipts ($112.37bn shared, $105.53bn personal),
  plus (f_ss − 1) × the added people's Social Security ($9.58 / 8.09bn).
- **medicare.** The change in Part A, plus (f_pa − 1) × the added people's Part A accrual ($3.32 / 2.86bn).

f_ss and f_pa are G3+'s net accrual per tax dollar and its Part A per HI tax dollar, each arm over control.

## Gates (every one stops the run with [BLOCKED])

- **Staged sources.** The staged PDFs and text layers match ACQUIRED.md's sha256: tr2026 fb4e1556…, mtr2026 ffa56b91…,
  an2026-3 25bf13bd…. The text layers are byte-identical to a fresh `pdftotext -layout`.
- **Quotes.** 15 quotes are verbatim in their documents.
- **Positive control, through the pension lane's code.** Exact to 1e-12 for:
  - the OASDI accrual per tax dollar for the union and each generation;
  - the own-rate benefit-tax shares, `ratio_net`, the Part A accrual and the case on accrual
    ($399.0961 / 460.9765bn).
  All 448 rows of `hi_arms.csv` reproduce to 5.0e-7, and so does `case_beside.csv`'s central. The model haircut
  reproduces `model_check_mwr.csv`.
- **Printed shares and parsers.**
  - 16 of 16 printed payable shares are reproduced within the rounding of their table entries, and the lane's path
    equals Note 2025.7's anchors.
  - Table IV.B3 (% of GDP) agrees with IV.B1 to 0.0011.
  - The copied Table V.C1 parser reproduces the lane's on TR 2025.
  - TR 2026 V.C1's AWI equals Note 2026.3 Table 7's exactly, and the 2027–35 COLAs equal the 2.4% CPI.
- **The patched runs.** The swap on equal paths equals the grid's own exactly. Every patched run leaves no state
  behind: `tr2026` reproduces exactly after them.
- **`case_lines_check.cjs`.** The pension lane's frozen September 27 case lines and per-method costs reproduce byte for
  byte on today's engine, and only engine.js's hash has moved.
- **`case_tr2026.cjs`, 13 gates.**
  - The consumer reproduces the case and the cash set (1e-9), with their ends at 48 / 11.
  - The per-member divisor is summary.json's 42.75M.
  - The cash payloads have no pension block.
  - The v5 payload extends the September 29 payload.
  - The payload's pension block is the lane's at 9ea1beb.
  - The union's social_security is ratio_net × its OASDI receipts, and its Part A is part_a_accrual_bn (1e-9).
  - The added people's Social Security is the lineage lane's (5e-6).
  - The control equals the payload's pension block exactly.
  - The control arm reproduces the case at all 64 specifications exactly.
- **Tests and rerun.** `test_pension_tr2026.py`: 6 passed. `rerun_lane.py`: IDENTICAL 17/17, exit 0.

## Limits

- The 2026 arms are ungated against a 2026 money's-worth note, because none exists.
- **The model's haircut against Note 2025.7 Table 3.** It differs by up to 0.056 per cell on the lane's path, and by
  0.071 on the 2025 tables' path. The mean absolute gaps are 0.020 and 0.023.
  - The cause is that the model omits disability, young-survivor benefits and the family maximum.
  - The arms use only the model's ratio of two paths. The level error therefore cancels to first order, but the ratio
    carries the model's benefit mix. [INFERENCE]
- [APPROX] The added people's factors use G3+'s ratio for both parts of their blend: G3+ members and the white part,
  which is priced at G3+ ages. The added people carry about 8% of the change.
- [APPROX] The separate-funds path weights the funds by national cost in each year.

## For the pension lane (outside this lane, not done)

`pension_accrual.py` at HEAD stops on a rerun with `[BLOCKED] case.json predates changes to
['infra/immigration-fiscal/assumption_explorer_2026_09_21/engine.js']; rerun case_lines.cjs`. Engine.js moved in
db5840f6 ("Engine takes new receipt lines and scale edits — v4 payload"). The frozen case lines still reproduce byte for
byte on today's engine (`case_lines_check.cjs` here), so its outputs stand. Rerunning its own `case_lines.cjs` would
refresh the recorded hash.

Update 2026-10-08: ec59a377 (2026-10-07 02:38, three minutes after this lane's 8cefec37) did refresh the hash, and the
pension lane reruns again. This lane's two guards (`pension_tr2026.py` `lane_case` and `case_lines_check.cjs` gate 4)
required that exactly engine.js had moved, so after the refresh both stopped `[BLOCKED]` with an empty list. They now
accept that nothing moved as well. `derived/case_now.json` records `hash_moved_since_lane_case_json: []`, and the 16
other outputs reran identical. A second rerun gives IDENTICAL 17/17.

## Reproduce

Run from the repository root (one to two minutes in all, mostly `pension_tr2026.py`; peak memory 0.52 GB):

```sh
node infra/immigration-fiscal/pension_tr2026_2026_10_06/case_lines_check.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/pension_tr2026_2026_10_06/pension_tr2026.py
node infra/immigration-fiscal/pension_tr2026_2026_10_06/case_tr2026.cjs
PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/pension_tr2026_2026_10_06/test_pension_tr2026.py -q -p no:cacheprovider
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/pension_tr2026_2026_10_06 \
  "node {lane}/case_lines_check.cjs" "uv run --no-project python3 {lane}/pension_tr2026.py" \
  "node {lane}/case_tr2026.cjs" \
  "PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 -m pytest {lane}/test_pension_tr2026.py -q -p no:cacheprovider" \
  --allow-unrun infra/immigration-fiscal/pension_tr2026_2026_10_06/sources_tr2026.py
```

`sources_tr2026.py` is a module that `pension_tr2026.py` imports, hence `--allow-unrun`.

Files in `derived/`:

| File | Contents |
|---|---|
| `paths.csv` | every path by year, 2025–2110 |
| `path_points.csv` | the table points and inputs behind the paths |
| `path_gates.csv` | the 16 printed shares |
| `haircut_check.csv` | the model's haircut on Note 2025.7's cells |
| `arms.csv` | every arm by group |
| `case_beside.csv` | the September 27 case on accrual, per arm |
| `summary.json` | read by `case_tr2026.cjs` |
| `case_lines_now.csv`, `case_now.json` | the pension lane's frozen case, re-read on today's engine |
| `case_oct05.csv`, `case_oct05.json` | main case v5, per arm and end |

## Log

- started: reading CLAUDE.md, pension_accrual_2026_09_28, main_case_2026_10_05.
- 2026-10-06 16:23 JST. Staged the 2026 OASDI Trustees Report (`tr2026.pdf`), the 2026 Medicare Trustees Report
  (`mtr2026.pdf`), Note 2026.3 and the Note 7 index under `sources/immigration-fiscal/data/external/stage3/ssa/trustees_2026/`
  and `.../cms/trustees_2026/`, each with ACQUIRED.md (ssa.gov answers plain curl with 403; curl_cffi works).
  No 2026 money's-worth note exists: the Note 7 index ends at 2025.7 (December 2025) and `an2026-7.pdf` is 404.
  Read so far [SOURCE: tr2026.pdf Table II.A1, Highlights, Table IV.B5]: OASDI reserves depleted in the third
  quarter of 2034; 83% of scheduled benefits payable at depletion, falling to 65% in 2100; 75-year deficit 4.42% of
  payroll (3.82% in 2025). [SOURCE: mtr2026.pdf section II.E] HI depleted in 2033 (second quarter); non-interest
  income covers 89% of expenditures in 2033, 85% in 2050 and about 93% in 2100 (2025 report: 89%, 86% in 2049,
  about 100% in 2099). The morning lane's figures are confirmed.
- resumed 2026-10-07 01:03 JST by claude-opus-5-5 (second worker, after the machine restart). PROBE IN PROGRESS [UNVERIFIED]: reading
  the pension lane and the main case's consumption of it before planning the swap.
- 2026-10-07 01:31 JST, third worker (claude-opus-5-5), after the second restart. Staged PDFs match ACQUIRED.md's sha256
  (tr2026 fb4e1556…, mtr2026 ffa56b91…, an2026-3 25bf13bd…). The pension lane is unchanged since 9ea1beb, the commit
  the main case pins. Plan, from reading the code [INFERENCE]:
  - **A naive swap would show almost nothing.** The OASDI accrual's level is Note 2025.7 Table 3, which carries the 2025
    payable path. The lifetime model enters only as a factor, k(person) / mwr(Note 2025.7's basis), both computed on
    the same path. Swapping `payable_path` inside the model alone cancels in that ratio. The arm therefore keeps the
    denominator on the 2025 path and puts the 2026 path in the numerator: Table 3 x k_2026 / mwr_base_2025. It
    reproduces the central exactly when the two paths are equal.
  - **The Trustees' payable share is payroll / (cost − tax on benefits).** Taxation-of-benefits income falls with the
    cut. Income / cost does not reproduce the published shares: for 2100 it gives 67.2%, against the 65% the report
    prints. [CALCULATION: TR 2026 Tables IV.B1/IV.B2, 2100: 12.39 / (20.02 − 1.07) = 0.654; TR 2025, 2035:
    12.38 / (16.23 − 0.90) = 0.808, against Note 2025.7's 80.7%]
  - **The lane's straight line from 2035 to 2099 misses the dip in the 2025 path.** The year-by-year path bottoms at
    0.695 in 2080. The headline arm therefore builds both reports' paths the same way, year by year from their tables.
    It keeps the lane's anchor form as a check.
  - **The main case's pension items** are `social_security` = ratio_net x the union's OASDI receipts, plus a fixed
    Part A accrual of $41.14bn on `medicare` (`main_case_2026_10_05/derived/corrections.json` `meta.pension_accrual`).
    The lineage's 3.04M added people carry their own accrual through the G3+ and white rules. The engine run edits the
    v5 payload and evaluates it with candidate v4's package-free `consumer.cjs`.
- 2026-10-07 02:00 JST, third worker. Confirmed and written to `derived/` (pension_tr2026.py 51 s, 0.49 GB peak; the two
  node scripts a few seconds each). Positive control passes: the pension lane's central reproduces through its own code
  (1.018378 per tax dollar, ratio_net 0.973667, Part A $41.1371bn, its case $399.0961 / 460.9765bn, all 448 rows of
  hi_arms.csv to 5.0e-7). The paths reproduce all 15 printed payable shares (path_gates.csv). The headline arm, tr2026,
  moves main case v5 from $390.29–461.24bn to $385.94–457.10bn (−4.36 / −4.15bn) by an engine run that equals
  first-order scaling to 1.1e-13bn. The cash set is unchanged at $307.38–383.41bn. Added the wage-index arm (Note 2026.3's
  AWI, −3.18 / −3.05) and a combined arm with all five unapplied inputs (−1.76 / −1.66). Fixed a bug in case_tr2026.cjs:
  the per-member divisor read a missing payload field and printed NaN. It now reads `meta.lineage.counts` and is gated
  against summary.json's $9,129–10,789.
- 2026-10-07 02:24 JST, third worker. Five changes since 02:00:
  - **New arm for COLAs and bases.** Added `program_parameters_tr2026`, TR 2026 Table V.C1's COLAs and contribution
    bases. Its parser is a copy of the lane's, gated against the lane's own parser on TR 2025 and against Note 2026.3's
    AWI.
  - **The joint arm covers six inputs.** It replaces the five-input arm: −1.73 / −1.63bn on v5, where the five-input
    arm gave −1.76 / −1.66bn.
  - **Separate funds rebuilt.** The arm that put OASI's path on every benefit gave −9.92 / −9.33bn. It overstated the
    cut, because current law pays DI in full and Note 2025.7's level includes disability benefits. It is replaced by a
    cost-weighted separate-funds path on both reports: −1.11 / −1.04bn against `tr2026`, and −1.21 / −1.13bn against
    `tables_2025`.
  - **Quotes and gates.** Added three verbatim quotes (DI in both reports, OASI in TR 2025) and the TR 2025 OASI gate,
    which brings the printed shares to 16/16.
  - **Tests.** Wrote `test_pension_tr2026.py`, covering the positive control, the swap's identity, the paths, the
    engine gates, additivity and line endings: 6 passed.

  `pension_tr2026.py` ran in 123 s wall (73 s CPU, the machine shared) with a 0.52 GB peak. Verdict set, and the
  PROGRESS stub removed.
- 2026-10-07 02:27 JST, third worker. Final rerun: the four commands above, with `--allow-unrun` for `sources_tr2026.py`, end
  `IDENTICAL: 17/17 files unchanged`, exit 0 (the pytest ran inside it, 6 passed). Done; nothing committed.
- 2026-10-07 02:30 JST, third worker. Re-printed the body's figures with controlled rounding, so that printed parts add to printed
  totals (the captions name the moved figures). The mortality row is corrected to +0.14 / +0.14bn (0.145 unrounded).
  No script or output changed.
