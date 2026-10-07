claude-opus-5-5

**Verdict:** Van Hook & Bachmeier's table, transferred at face value, would raise main case v5 by $23.0–31.8bn, to
**$413.31–493.02bn**. On the cash set the rise is $16.6–27.3bn, to $323.96–410.66bn. This uses arm (i): the account's
measured G3 rate times VHB's fourth-plus/third step, 0.888 × 0.687 = 0.610. It adds 5.90M people against arm b's
3.04M. I recommend that it **not** replace arm b's "held for G5+" central. Print it beside, as a face-value upper
sensitivity.

On every generation that both VHB and today's CPS can see, VHB's levels run 9–17 points lower and its steps are
steeper. VHB's G3 rate of 74.2% belongs with the older measurements: Duncan–Trejo's 1994–2006 rate of 71.8% and the
1970 reinterview's 73.0%. Today's CPS measures 88.8%. Scaling VHB's step to today's lower loss gives p4 0.732–0.777
and $390.79–468.86bn (+$0.5–7.6bn). That range runs from arm b to just over half-way to arm c. The CPS also measures
today's step directly, at 0.880 (ladder 233); arm b already uses it. [CALCULATION: `derived/vhb_bands.csv`,
`derived/arms_vhb.csv`, `derived/cps_benchmark.csv`; INFERENCE for the recommendation]

## 1. Evidence: what VHB measure

**The table, verified first-hand.** Supplemental Table 2.1 reports the share of Mexican-ancestry adults who identify
as Mexican and as Hispanic, by generation. [SOURCE: Van Hook & Bachmeier, *Texas-Style Exclusion*, Russell Sage 2024,
online supplement, Supplemental Table 2.1; page image `.claude/scratch/litscan-2026-10-06/verify/vhb_img3-000.png`,
sha256 d99b81e0…; PDF `vhb_supp.pdf`, sha256 9ec19488…; transcribed in `derived/vhb_table_2_1.csv`]

| Generation | % Mexican | % Hispanic |
|---|---|---|
| First | 86.8 | 90.7 |
| Second | 83.8 | 91.2 |
| 2.5th | 72.3 | 80.0 |
| Third | 74.2 | 84.6 |
| Fourth-or-higher | 51.0 | 82.8 |

- **Population.** IGENS-20 linked files cover adults 20+ in the CPS, the 2000 Census or the ACS. Each has at least one
  parent, grandparent or great-grandparent born in Mexico (N = 10,500). The families are those whose 1940 parents
  reported Mexico as their birthplace; 87% of those parents arrived before 1920. Descendants are found by record
  linkage, not self-report, so the denominator is linked ancestry. [SOURCE: supplement §2.1–2.2 and the table note]
- **Generations.** G2.5 has one Mexican-immigrant parent and one non-immigrant parent. G3 has no immigrant parent and
  at least one Mexico-born grandparent. G4+ has "no Mexican immigrant parents or grandparents" [SOURCE: §2.2]. The
  sample stops at great-grandparents, so VHB's G4+ is the fourth generation only. It says nothing about G5+.
  [INFERENCE from the table note]
- **No standard errors and no cell sizes** are printed.
- **Linkage.** About 70% of the 1940 children received a linkage key; the rate in the 2000 Census and ACS is about
  90%. Inverse-probability weights adjust for observed selection. [SOURCE: §2.3]

**Signs that VHB's levels do not transfer.** I put CPS ASEC 2025 adults 20+ on VHB's generation definitions, with
the same items (Mexican is PRDTHSP 1; Hispanic is PEHSPNON 1). [CALCULATION: `derived/cps_benchmark.csv`, SDR SEs
there]

| Generation | VHB % Mexican | CPS 2025 % Mexican | VHB % Hispanic | CPS 2025 % Hispanic |
|---|---|---|---|---|
| G1 (Mexico-born) | 86.8 | 96.3 (SE 0.4) | 90.7 | 98.4 |
| G2 (both parents born abroad, at least one in Mexico) | 83.8 | 94.4 (0.6) | 91.2 | 98.3 |
| G2.5 (one Mexico-born parent, the other US-born) | 72.3 | 89.3 (1.5) | 80.0 | 94.4 |
| G3 | 74.2 | 88.8 (p3; children linked to co-resident parents) | 84.6 | — |

- **VHB's G1 is the clearest sign.** 9.3% of VHB's linked Mexico-born adults do not report Hispanic at all, against
  1.6% in the CPS. That points to false links, or to people born in Mexico who are not of Mexican origin. Either would
  lower every VHB level. If the error grows with each added link, it also steepens VHB's steps. [INFERENCE]
- **VHB's steps are steeper wherever the CPS can check them.**

  | Step | VHB | CPS today |
  |---|---|---|
  | G2 → G2.5 | 0.863 | 0.946 |
  | G2 → G3 | 0.885 | 0.940 |
  | G1 → G3 | 0.855 | 0.922 |

  [CALCULATION: ratios of the table above]
- **VHB's G3 sits with the older regime.** The 1970 reinterview gives 98.7 / 83.3 / 73.0 / 44.4% Hispanic
  identification for G1–G4 (n 77 / 90 / 89 / 27), so its G4/G3 is 0.608. Duncan–Trejo's 1994–2006 third generation
  is 71.8%. On the same design the 2025 CPS gives 88.8% for the third generation. Its fourth-plus children with an
  identifying parent rose too, from 70.8% to 88.3% (a censored measure). [SOURCE:
  `mexican_origin_population_total_2026_09_19/RESULT.md` §3.3–3.5, `derived/arm3_dt_table8_replication.csv`] The
  period rise lifted every generation the design sees. Nothing says the G3 → G4 step was spared. [INFERENCE]

**Step 5's claim tested.** VHB's G3/G2 (0.885) does nearly equal the account's G3 rate (0.888), but the two are not
like for like. p3 is a level against ancestry. VHB's G3/G2 is a ratio between generations. The like-for-like CPS
ratio is p3 / CPS G2 = 0.940, or 0.955 on the account's any-parent G2. The like-for-like level is VHB's 74.2%
against 88.8%. So the match is a coincidence, and it does not support transfer. [CALCULATION]

**The counter-case: is today's G4+ VHB's population?** Partly yes. Today's adult fourth-plus descend mostly from the
same 1900–1930 migrants as VHB's linked families, in the same Southwest [INFERENCE]. Two things differ.

1. **The identity regime.** Under VHB, 65% of fourth-generation adults who no longer report Mexican still report
   Hispanic ((82.8 − 51.0) / 49.0). That is the old Tejano/Hispano "Spanish/Hispanic" label pattern. In today's CPS
   only 25% of children of G3+ parents who are not reported Mexican are still reported Hispanic (9.0% / 12.0% loss;
   `civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv`). Take arm (i) with VHB's own retention: 3.32M
   hidden fourth-plus would still report Hispanic but not Mexican. The CPS counts only 1.92M third-plus "Other
   Hispanic" of any ancestry (Hispanos included). So VHB's whole regime does not fit today's survey. Arm (i) with
   today's retention needs 1.29M, which fits. [CALCULATION: `derived/hispanic_channel.csv`,
   `derived/cps_third_plus_hispanic_detail.csv`]
2. **Today's step is measured.** Ladder 233 measures child-stage loss for children of G1, G2 and G3+ parents at 7.8,
   15.1 and 12.0%. The last gives arm b's relative step of 0.880. Ladder 158 finds G3 identification flat by age
   today, so the regime applies to the adult stock as well. Two caveats: the step is reported by parents and seen
   only through identified parents. VHB's 0.687 is self-reported, on true ancestry, in an older sample.

## 2. Arms

Each arm sets the effective fourth-plus identification rate p4 (the population lane's `DT_4TH_PLUS_ID` slot). All
arms are flat, held for G5+ as arm b is, except (v). [CALCULATION: `derived/arms_vhb.csv`]

| Arm | Rule | p4 | Step from p3 |
|---|---|---|---|
| b (v5 central) | p3 × (1 − 0.1204), CPS child-stage loss | 0.7812 | 0.8796 |
| (i) relative | p3 × (G4+/G3)_VHB | 0.6104 | 0.6873 |
| (ii) G1-normalised | (G4+/G1)_VHB; implies G3 0.855 against the measured 0.888 | 0.5876 | 0.6616 |
| (ii) G2-normalised | (G4+/G2)_VHB | 0.6086 | 0.6853 |
| (iii) Hispanic | p3 × (G4+/G3)_VHB on Hispanic; not the account's construct | 0.8692 | 0.9787 |
| (iv) calibrated, CPS | p3 × 0.687^k, k = ln(p3/G1_CPS) / ln(G3_VHB/G1_VHB) = 0.515 | 0.7321 | 0.8243 |
| (iv) calibrated, DT | p3 × 0.687^k, k = ln(p3) / ln(p3_DT) = 0.358 | 0.7765 | 0.8743 |
| (v) VHB step compounded, ρ 0.5 (beside) | p_eff of compounding 0.687 | 0.4650 | 0.5236 |

**Which arm is right.** Arm (i) is the correct way to use VHB's number on the account's frame, if you use it:

- It keeps the account's own measured G3 rate.
- It uses only what VHB add, the G3 → G4 step.
- It equals assuming that VHB's shortfall against the CPS at G3 carries to G4 unchanged.
- (ii) G1-normalised overrides the measured p3. (ii) G2-normalised lands on (i), because VHB's G3/G2 ≈ p3.
- (iii) counts exits from any Hispanic identity, but the account counts Mexican-origin reports, so (iii)
  understates the hidden people.

I would not adopt (i), for the reasons in §1:

- VHB's levels and steps belong to the older regime.
- VHB's whole regime fails the CPS's "Other Hispanic" cap.
- Today's step is measured directly, and arm b already uses it.

The calibrated arms (iv) assume VHB's excess loss scales in logs from the G1 → G3 span, or from the period shift, to
the G3 → G4 step [ASSUMPTION]. They put VHB's evidence at p4 0.73–0.78: arm b up to just over half-way to arm c.
That supports b as a central near the low end of what VHB allow, not as an understatement of it. [INFERENCE]

## 3. Pricing on main case v5

**Method.** `arms.py` runs each arm through `propagate.run_population`, then through the lineage lane's
`population.py main()` (account frame, factor 0.997189). `lineage_case.cjs` is the lineage lane's engine script
unchanged except for input paths; its 349 gates pass, including the band ends staying at specifications 48 / 11 for
every arm.

**Positive controls.**

- Arms b and c (ρ 0.5) rerun equal `population_arms.csv` in every column.
- Floor, a, b and c on the account's frame equal the lineage lane's `population.json` exactly (arm b 3,039,719.6).
- Every band row of floor, a, b, c and v4 equals `main_case_lineage_2026_10_05/derived/v5_bands.csv`, max |diff| 0.
- The central payload is byte-identical apart from its `source` string.

[CALCULATION: `derived/gates_arms.json`, `derived/gates.json`, `derived/gates_compare.json`]

| Arm | Added (M) | At G3 rate / later (M) | Set ($bn) | Change from v5 | Per member | Cash set ($bn) | Change from v5 |
|---|---|---|---|---|---|---|---|
| a | 1.81 | 1.81 / 0 | 380.37 / 447.55 | −9.92 / −13.69 | $9,161 / 10,779 | 300.22 / 371.66 | −7.16 / −11.75 |
| **b (v5)** | 3.04 | 1.94 / 1.09 | **390.29 / 461.24** | — | $9,129 / 10,789 | 307.38 / 383.41 | — |
| c (ρ 0.5) | 4.27 | 2.08 / 2.19 | 400.21 / 474.93 | +9.92 / +13.69 | $9,099 / 10,797 | 314.52 / 395.15 | +7.14 / +11.74 |
| **(i) VHB relative** | 5.90 | 2.27 / 3.64 | **413.31 / 493.02** | **+23.02 / +31.78** | $9,061 / 10,808 | 323.96 / 410.66 | +16.58 / +27.25 |
| (ii) G1-normalised | 6.41 | 2.32 / 4.09 | 417.40 / 498.67 | +27.11 / +37.43 | $9,049 / 10,811 | 326.91 / 415.51 | +19.53 / +32.10 |
| (ii) G2-normalised | 5.94 | 2.27 / 3.67 | 413.62 / 493.45 | +23.33 / +32.21 | $9,060 / 10,808 | 324.19 / 411.04 | +16.81 / +27.63 |
| (iii) Hispanic | 2.00 | 1.83 / 0.17 | 381.95 / 449.73 | −8.34 / −11.51 | $9,156 / 10,781 | 301.36 / 373.53 | −6.02 / −9.88 |
| (iv) calibrated, CPS | 3.73 | 2.02 / 1.70 | 395.81 / 468.86 | +5.52 / +7.62 | $9,112 / 10,794 | 311.35 / 389.94 | +3.97 / +6.53 |
| (iv) calibrated, DT | 3.10 | 1.95 / 1.15 | 390.79 / 461.93 | +0.50 / +0.69 | $9,128 / 10,789 | 307.73 / 383.99 | +0.35 / +0.58 |
| (v) compounded (beside) | 10.00 | 2.72 / 7.28 | 446.16 / 538.40 | +55.87 / +77.16 | $8,975 / 10,830 | 347.61 / 449.58 | +40.23 / +66.17 |

[CALCULATION: `derived/vhb_bands.csv`, `derived/v5_bands.csv`]

- Changes are differences of the printed bands.
- Per member divides by 39,712,493 plus the added people (arm (i): 45.62M).
- The per-member figure barely moves because an added person costs a little less than the average member.

**Later losses carry the arm.** Under VHB most added people are later losses (3.64M of 5.90M in (i)). v5 prices
later losses as identified G3+ members, who close none of the gap. VHB themselves find that non-identification rises
with schooling (supplement §2.2, figure 2.2). So the table below adds a sensitivity in which every added person
closes C3 (0.557), as G3-rate attriters do:

| Arm, later losses closing C3 | Set ($bn) | Change from v5 | Cash set ($bn) | Change from v5 |
|---|---|---|---|---|
| b | 386.47 / 456.21 | −3.82 / −5.03 | 303.98 / 378.37 | −3.40 / −5.04 |
| (i) VHB relative | 400.61 / 476.28 | +10.32 / +15.04 | 312.67 / 393.90 | +5.29 / +10.49 |
| (iv) calibrated, CPS | 389.86 / 461.02 | −0.43 / −0.22 | 306.07 / 382.09 | −1.31 / −1.32 |

Arm (i)'s rise is therefore about half the "later losses close nothing" rule. Taken with that rule, VHB at face value
compounds two upward choices. [CALCULATION; INFERENCE]

The other v5 sensitivities (C3 0 and 1, replacement, fractional attriters only, whites at their own ages) are in
`derived/v5_bands.csv` for every arm. For example, arm (i) at r = 1 replacement is $399.94–472.59bn.

## 4. Limits

- **Period.** VHB pool generations observed in different surveys: the CPS from 1973, the 2000 Census and the ACS. G1
  and G2 are observed earlier than G4 by construction. The table cannot separate period from generation, and the
  direction of that bias is not known.
- **Linkage error is not quantified.** The 7.7-point Hispanic shortfall of VHB's G1 against the CPS is the only
  handle.
- **The calibration exponents are assumptions.** They assume VHB's excess loss scales in logs; they are not
  estimates.
- **No sampling error.** VHB print no SE or G4 cell size. The CPS benchmark SEs are in `cps_benchmark.csv`; none is
  propagated to the bands.
- **The population machinery is inherited.** It divides the CPS self-identified fourth-plus (8.02M, including
  Hispano and Tejano families with no immigrant ancestor) by p4. VHB's sample excludes those families, so every arm
  that lowers p4 also inflates the pre-1848 lineages. Sizing that needs the ACS ancestry lane.
- **Pricing rules are v5's.** Costs are linear in members, the added people take the G3+ age mix, and only the
  group-size responses see the larger group.

## 5. Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/benchmark.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/arms.py
node infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/lineage_case.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/compare.py
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/vhb_fourth_plus_2026_10_07 \
  "uv run --no-project python3 {lane}/benchmark.py" "uv run --no-project python3 {lane}/arms.py" \
  "node {lane}/lineage_case.cjs" "uv run --no-project python3 {lane}/compare.py"
```

- **Inputs, all read-only.** `benchmark.py` reads the population lane's ignored
  `_cache/cps_asec2025_person_subset.parquet`. `arms.py` imports `identity_loss_propagation_2026_09_27/propagate.py`
  and `main_case_lineage_2026_10_05/population.py`, pointing their output paths at this lane's `_cache/` and
  `derived/`.
- **Redundant outputs.** `lineage_payload*.json` here duplicate the lineage lane's (arm b), apart from the source
  string.

## Log
- 2026-10-07 10:42 JST: stub written; brief read (worker model claude-opus-5-5). New files only, in this directory; nothing committed.
- 2026-10-07 10:45 JST: VHB Supplemental Table 2.1 verified first-hand from the image of the online supplement
  (`.claude/scratch/litscan-2026-10-06/verify/vhb_img3-000.png`, sha256 d99b81e0…; text `vhb.txt` from `vhb_supp.pdf`,
  sha256 9ec19488…). Numbers match the brief: Mexican 86.8 / 83.8 / 72.3 / 74.2 / 51.0, Hispanic 90.7 / 91.2 / 80.0 /
  84.6 / 82.8. The table note restricts the sample to adults 20+ "with at least 1 parent, grandparent, or
  great-grandparent born in Mexico" (N = 10,500), so the deepest generation observable is G4: "fourth-or-higher" is
  in practice the great-grandchildren of a Mexico-born ancestor, not a G4/G5+ mix [SOURCE: table note; INFERENCE on
  the depth]. Ancestry is fixed by record linkage from 1940 Mexican-born parents, not by self-report.
- 2026-10-07 10:50 JST: `benchmark.py` run. CPS ASEC 2025 adults 20+ on VHB's generation definitions identify as Mexican
  at 96.3% (G1), 94.4% (G2, both parents born abroad, one or both in Mexico), 89.3% (G2.5); VHB report 86.8 / 83.8 /
  72.3. VHB's G3 (74.2) is 14.6 points below the account's p3 0.888 and sits with the older measurements: Duncan–Trejo
  1994–2006 third generation 71.8%, 1970 reinterview 73.0%. Third-plus "Other Hispanic" (PRDTHSP 8) in the CPS: 1.92M
  all ages. [CALCULATION: `derived/cps_benchmark.csv`, `derived/cps_third_plus_hispanic_detail.csv`]
- 2026-10-07 10:50 JST: `arms.py` run. Controls pass: arms b and c (ρ 0.5) rerun through `propagate.run_population`
  equal `population_arms.csv` in every column; floor, a, b, c on the account's frame equal the lineage lane's
  `population.json` exactly (arm b 3,039,719.6). Arm (i) p4 0.6104 adds 5.90M on the account's frame (2.27M at the G3
  rate, 3.64M later). [CALCULATION: `derived/population.json`, `derived/gates_arms.json`]
- 2026-10-07 10:54 JST: `lineage_case.cjs` (copy, input paths only) and `compare.py` run; positive control max |diff| 0 on every
  floor/a/b/c/v4 band row. Added the later-losses-close-C3 sensitivity (`<arm>_later_c3` in `arms.py`); 349 engine
  gates pass. RESULT sections 1–5 written; verdict: keep arm b central, VHB (i) $413.31–493.02bn beside.
- 2026-10-07 10:54 JST: `rerun_lane.py` with the four commands: IDENTICAL 25/25 files, exit 0, at 10:54:58. Upstream
  lanes untouched (`git status` shows only this directory new among the lanes it reads).
