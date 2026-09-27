**Verdict:** The candidate's arithmetic holds, but three of its explanations do not.

**What holds.**
- Items 1 and 2 add exactly and move only their named lines.
- Item 2's factors are the account's own, bit for bit, and P + F reproduces (13.32 → 11.68, 8.79 → 7.68).
- Public pay's sign and payroll matching are right.

**What does not.**
1. **Item 1's +$0.22bn is a re-key, not a removed double count.** It moves the $5.26bn of public housing's deficit
   that the subsidy covers from the tenants' rental key (0.075) to the population key (0.117).
   - With the housing enterprise keyed by its tenants, item 1 is exactly 0, and the September 27 case falls by
     $1.69bn (candidate: $1.91bn).
   - Its "after" gate is an algebraic identity. A $1bn transfer that is not consolidated still moves the case by
     −$43m / −$41m.
2. **The fixed road stock is not unmeasured.** In the pinned Census files, highway construction scales with
   population across states at 0.79 (95% CI 0.68–0.91; 0.76 with land).
   - That excludes the −$10.5bn case, so the placement beside the range is right, for a stronger reason than the
     candidate gives.
   - The arm lacks the upward case: a stock read from construction adds $0.44–0.90bn at spec 48.
3. **Public pay double counts part of the account's own response.** On the account's shrinking public workforce it is
   $12.05–12.39bn / $7.85–8.09bn, not $13.61 / $8.95bn.

**Also.** The placement rule the candidate uses for roads, applied to the range's own long-run component, puts the
outer range at $260.61–434.22bn (from $260.52–437.37bn). The 64 specifications are 32 distinct ones, each twice; this
is inherited and harmless for the band.

Each finding below carries its probe command and verbatim output. The probes are read-only; nothing outside this
directory was written. [CALCULATION throughout; INFERENCE where marked]

## Findings (appended as probes run)

### 1. Transfer consolidation (item 1)

Probe: `node infra/immigration-fiscal/candidate_attack_2026_09_28/probe_item1_transfer.cjs` (read-only; requires the
candidate's `package.cjs`, writes nothing). Output, verbatim:

```
[A] the after-gate's two models, cell by cell
  b_hotdeck_union_matched: 44 cell values; max |diff| national 0.00e+0, cells 7.11e-15 bn (relative 1.53e-16)
  b_matched_over_pooled: 44 cell values; max |diff| national 0.00e+0, cells 7.11e-15 bn (relative 2.11e-16)
  gate formula at T = 0.001: max |cost diff| 0.00e+0 bn
  gate formula at T = 5.257811: max |cost diff| 0.00e+0 bn
  gate formula at T = 30: max |cost diff| 0.00e+0 bn
  gate formula at T = 60: max |cost diff| 0.00e+0 bn
[B] a $1bn internal transfer that the fix does not consolidate (spec 48, capital off; then 48 / 11 with capital)
  b_hotdeck_union_matched: today -43.1853m; after consolidation -43.1853m; with capital at 48 / 11 -43.1853m / -43.1853m
  b_matched_over_pooled: today -40.7509m; after consolidation -40.7509m; with capital at 48 / 11 -40.7509m / -40.7509m
[C] mutation test: the gate's formula on broken consolidate() variants (max |cost diff| over both methods, specs 48 and 11)
  correct (the candidate's)                0.00e+0 bn  PASSES the gate
  rental leg only                          1.17e-1 bn  fails the gate
  enterprise leg only                      7.64e-2 bn  fails the gate
  rental factor on both legs               7.19e-1 bn  fails the gate
  national totals only, cells untouched    3.74e-1 bn  fails the gate
  twice the amount                         4.32e-2 bn  fails the gate
  no-op                                    4.32e-2 bn  fails the gate
  pair broken alike (both helpers rental-leg only)   0.00e+0 bn  PASSES the after-gate
[D] item 1 alone against the September 27 case: what moves (all 64 specs, both methods)
  lines that move: spending:housing_subsidies (max 0.401825), receipts:enterprise_surplus (max 0.616086)
  P and F: max |diff| 0.00e+0; capital components (return and key): max |diff| 0.00e+0
[E] item 1 as a re-key of public housing's operating subsidy
  NIPA 3.8 l13 housing and urban renewal current surplus 2024: -40.298 bn (capital lane enterprise_surplus_vs_return.csv)
  spec 48: kh 0.0740/0.0764 ke 0.1172/0.1172 r_h 1 r_e 1
    item 1 as (r_e ke - r_h kh) T: 0.2207 bn
    housing enterprise keyed like its tenants (kh) instead of ke: Sept 27 -1.6912 bn; candidate -1.9119 bn
    => with that key, item 1 moves the case by -2.22e-16 bn
  spec 11: (identical to spec 48)
```

- **1a. The "after" control is an algebraic identity, not a positive control.** [CALCULATION: A, C]
  - `consolidate(withSyntheticTransfer(m, 1), T + 1)` and `consolidate(m, T)` are the same model to 7e-15bn per cell,
    because the two scale factors multiply to (n − T)/n.
  - The gate's formula returns exactly 0 at T = 0.001, 5.26, 30 and 60, so it cannot tell a right T from a wrong one.
  - It does catch a consolidate() broken on its own: one leg, the wrong factor, national totals only, twice the amount,
    or a no-op each fail by $0.04–0.72bn.
  - It passes when both helpers are broken alike (both rental-leg only). The "today" gate (kh − ke) would catch that
    pair, so the pair of gates is a sound unit test of the two helpers. It is not evidence that the account nets
    internal transfers.
- **1b. The −$43m control does not go to 0; only the consolidated dollar does.** [CALCULATION: B] A $1bn internal
  transfer that is not in T still moves the consolidated case by −$43.19m / −$40.75m. That is identical to today at
  spec 48 with capital off, and at 48 and 11 with capital on. The engine still keys the two legs differently. The
  candidate subtracts one known amount; it does not change the rule. The unpublished Section 8 paid to housing
  authorities, and any other federal-to-enterprise subsidy, keep the error at kh − ke per dollar. RESULT.md's
  "after consolidation the synthetic $1bn moves the case by exactly 0" should say "a synthetic dollar that is also
  consolidated".
- **1c. Nothing else moves (confirmed).** [CALCULATION: D] Over 64 specs and both methods, only `housing_subsidies`
  and `enterprise_surplus` move. P, F, and every capital component's return and key are unchanged to 0.
- **1d. The +$0.2207bn is a re-key of public housing's deficit.** [CALCULATION: E; INFERENCE on the right key]
  - The operating subsidy finances the housing authorities' operating deficit. It is in the housing enterprise's
    surplus: MP-5 p. II-30 and Handbook ch. 12 fn 13, as quoted in the candidate's log and the capital lane's §5
    [SOURCE, not re-read here]. NIPA 3.8 line 13 is still −$40.30bn after it.
  - Consolidating it moves $5.26bn of that deficit from the rental-assistance key (kh 0.0740 / 0.0764) to the
    population key (ke 0.1172).
  - If the housing enterprise were keyed like rental assistance, by its tenants (the capital lane already runs its
    capital that way as a variant, −$0.38 / −$0.57bn), then:
    - item 1 moves the case by exactly 0 (−2e-16);
    - a synthetic transfer to housing authorities nets to 0 whether or not it is consolidated, because both legs carry
      one key [INFERENCE: algebra, not run; the engine's enterprise line is not split by type];
    - the September 27 case itself falls by $1.69bn at both ends (candidate: −$1.91bn).
  - The candidate's +$0.22bn is therefore right only if the population key is right for public housing's deficit. That
    key question is about 8× larger than the item, and the candidate does not name it.

### 2. Production on the account's weights (item 2)

Probe: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/candidate_attack_2026_09_28/probe_production_pay.py`
(read-only; imports the account's own row-4 code, `cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`
`acs_cells()` and `weight_arms()`, without running its `main()`; `git status` of the imported lanes is unchanged
after the run). Output, sections [2a] and [2b], verbatim:

```
[row4] ACS 2024 Mexico-born outside CA+TX: naturalized 1.435577M, noncitizen 3.307120M (IPUMS = PUMS); ...
[row4] Mexico-born natz outside CA+TX: ASEC 1.677810M (n 943) -> ACS 1.435577M, factor 0.8556 (replicates 0.7952-0.9256)
[row4] Mexico-born noncit outside CA+TX: ASEC 4.250103M (n 2139) -> ACS 3.307120M, factor 0.7781 (replicates 0.7396-0.8161)
  account targets: naturalized 1,435,577.0, noncitizen 3,307,120.0 (IPUMS extract 3)
  candidate targets: naturalized 1,435,577.0, noncitizen 3,307,120.0 (PUMS)
  account factors (point) 0.855626 / 0.778127; candidate stored 0.855626 / 0.778127
  records the account reweights: 3082; 161 columns; max |W4 diff| 0.000e+00 persons, max relative 0.000e+00
  union population: published 40,896,574; account row4 39,712,493; candidate row4 39,712,493
  civilian national population: published 336,727,803; row4 335,543,722 (no national re-raking in either)
[2b] P and F on the account's weights, all 3,888 cells, against the candidate's stored row-4 grid
  published vs model.json: max |dP| 5.00e-10, max |dF| 5.00e-10 bn (3,888 cells)
  row4      vs candidate row4 grid: max |dP| 5.02e-10, max |dF| 4.99e-10 bn (3,888 cells)
  reference cell (gdp, index 1716): P+F 13.322598 -> 11.679878; cost change +1.642719
  reference cell (cash, index 1230): P+F 8.790628 -> 7.683239; cost change +1.107389
```

- **2a. The factors are the account's own, bit for bit (confirmed).** [CALCULATION]
  - The account's code (IPUMS extract 3) and the candidate's rule (ACS person file) hit the same targets to the person.
  - They give identical weights on all 3,082 reweighted records in all 161 columns (max difference 0).
  - Neither re-rakes the national total, so the candidate treats the national denominator as the account does.
- **2b. P + F reproduces (confirmed).** [CALCULATION] My own loop over all 3,888 cells on the account's weights
  matches the candidate's stored row-4 grid within 5e-10bn, the files' rounding. The reference cell gives 13.322598 →
  11.679878 (GDP) and 8.790628 → 7.683239 (cash), so the cost rises by +$1.642719 / +$1.107389bn, as claimed.
- **2c. Minor, not a defect.** Each replicate is raked to the same ACS total, so the ACS total's own sampling error
  drops out of the SE (1.1243 → 1.0350). The account's row 4 does the same, so the item is consistent with the account.
  The ACS error on a 4.7m total is small. [INFERENCE]

### 3. The road arm (item 3)

Probe: `OPENBLAS_NUM_THREADS=1 uv run --no-project --with scipy python3 infra/immigration-fiscal/candidate_attack_2026_09_28/probe_road_stock.py`
(read-only). It refits the scaling test's own state model on the same pinned Census files, now on nontoll highway
*construction* (code F44), the capital outlay that builds and replaces the stock. Output, verbatim:

```
[gate] panel 350 rows, 50 states; E44 equals the scaling test's highways_nontoll on 350/350 rows
[gate] E44, year effects: 0.726607 (the scaling test's 0.726607)
  mean over years of the 50-state sums ($bn): operations E44 79.5, construction F44 93.9
outcome                          model                              b     SE           95% CI    r(b)  n  states
operations (E44)                 year effects                   0.727  0.061 [ 0.605,  0.848]  0.7392 350 50
operations (E44)                 + log land                     0.690  0.044 [ 0.602,  0.778]  0.7038 350 50
operations (E44)                 + log land + growth 2012-23    0.690  0.040 [ 0.609,  0.771]  0.7039 350 50
operations (E44)                 state and year effects         1.464  0.488 [ 0.484,  2.445]  1.4225 350 50
construction (F44)               year effects                   0.792  0.058 [ 0.675,  0.908]  0.8022 350 50
construction (F44)               + log land                     0.758  0.046 [ 0.666,  0.850]  0.7699 350 50
construction (F44)               + log land + growth 2012-23    0.758  0.046 [ 0.665,  0.851]  0.7700 350 50
construction (F44)               state and year effects         0.575  0.781 [-0.995,  2.144]  0.5905 350 50
operations + construction        year effects                   0.762  0.050 [ 0.661,  0.863]  0.7735 350 50
operations + construction        + log land                     0.728  0.035 [ 0.658,  0.799]  0.7409 350 50
operations + construction        + log land + growth 2012-23    0.728  0.035 [ 0.659,  0.798]  0.7410 350 50
operations + construction        state and year effects         1.044  0.420 [ 0.201,  1.888]  1.0414 350 50
state means, E44                 + log land (50 obs, OLS)       0.689  0.039                   0.7030  50
state means, F44                 + log land (50 obs, OLS)       0.758  0.043                   0.7694  50
```

- **3a. The fixed stock is testable here, and local data reject it.** [CALCULATION; INFERENCE on steady state]
  - The candidate's reason for putting the fixed stock beside the range was that it "changes a premise. No measured
    response here supports it or excludes it". That is false.
  - Highway construction ($93.9bn a year, more than operations) scales with population across states at 0.792
    (95% CI 0.675–0.908). With a land control it is 0.758, and a growth control leaves it there.
  - In a steady state, replacement outlays are proportional to the stock, so the stock scales at least as operations
    do. A fixed stock (response 0) lies outside every across-state interval.
  - The within-state estimate (0.575, SE 0.78) cannot tell 0 from 1, just as the within-state operations estimate
    cannot.
  - The placement beside the range is therefore right. It hides no plausible $10bn choice: the −$10.51bn case is
    excluded by the same kind of evidence the low end rests on. The reason should say so rather than "unmeasured".
- **3b. The road arm is one-sided.** [CALCULATION from the probe and the candidate's decomposition]
  - Both alternatives only lower the cost. The construction slope is higher than the operations slope that the
    stationary network lends to the stock (r 0.8022, or 0.7699 with land, against 0.7392).
  - Reading the stock's response from construction would raise the low end. Its return plus depreciation at spec 48
    is 5.2306 + 5.2771 = $10.5077bn (all S&L; federal highways are 0 at the low end). Scaling that by
    0.8022/0.7392 or 0.7699/0.7392 gives **+$0.90bn / +$0.44bn at spec 48**. The high end is unchanged (capped at 1).
  - If a road arm is reported, this upward case belongs beside the two downward ones.
- **3c. No congestion double count in the account (confirmed by reading the code).** [DATA]
  - The candidate's `evaluateFull()` adds engine cost, capital return and public pay only. Congestion enters no cost.
  - `road_congestion.py` reprices the bridge's four rows exactly (its gates) and prices every variant from the
    package's own h and k.
  - The real-costs totals already use the case-dependent congestion, $13.99 / $12.02bn (73cc30c;
    `sept24_propagation_2026_09_24/real_costs_totals.py` lines 29–33 and 77). They therefore do not pair the
    stationary network's savings with the lanes-fixed B1.
- **3d. The placement rule is applied selectively.** [CALCULATION: `probe_item45.cjs` section 5c, below, from the
  candidate's `components.csv` and `road_arm.csv`]
  - The candidate excludes the road cases because their account move would enter the range while the dependent
    congestion move stays beside ("the dependent double error bar").
  - The range's own `long_run_response` component does exactly that. Account only, it runs −0.3339 / +12.3830 at the
    low end and −8.1246 / +15.5402 at the high end. Read jointly with congestion, the high end is −6.1987 / +12.3830.
  - Applying the rule consistently moves the outer range from $260.52–437.37bn to **$260.61–434.22bn** (+0.09 /
    −3.16).

### 4. Public pay (item 4)

Probes: `probe_production_pay.py` sections [4a] and [4b] (command above), and
`node infra/immigration-fiscal/candidate_attack_2026_09_28/probe_item45.cjs` section [4]. The codes were checked
against the ASEC 2025 data dictionary (`sources/immigration-fiscal/data/external/cps_asec_doc/ddl25.txt`: LJCW
2 federal, 3 state, 4 local; ERN_SRCE 1 wage and salary; ERN_VAL the longest job's earnings). Output, verbatim:

```
[4a] public-pay matching, record by record (incumbents: civilian, outside the group; published weight)
  public records 9461; outside both skill groups (A_HGA not 31-46): 0
  public records whose longest-job pay exceeds their own base max(PEARNVAL,0): 6, excess $0.02bn of $1507.26bn
  wage records with LJCW 1 (private): 47171; LJCW 2/3/4 with ERN_SRCE != 1: 0
  hs_or_less: public payroll $169.6bn / incumbent base $2,223.7bn = 0.0763
  more      : public payroll $1,337.7bn / incumbent base $9,292.3bn = 0.1440
[4b] P + F split by sector at the reference cell (row-4 weights); the charge is the public part
  gdp: labor gain by skill [-176.17, 187.85] (sum 11.6799); public part [-13.43, 27.04] (sum 13.6085 = charge 13.6085); private part [-162.74, 160.81] (sum -1.9287)
  cash: labor gain by skill [-115.89, 123.57] (sum 7.6832); public part [-8.84, 17.79] (sum 8.9520 = charge 8.9520); private part [-107.05, 105.78] (sum -1.2687)
[4] public pay against the account's own shrinking of government consumption (candidate, both methods averaged)
  spec 48 (gdp): consumption removed $357.83bn of $3991.8bn (8.96%); without defense 11.41%, with the school rows 11.43%
    charge 13.6085; overlap with the account's response 1.22–1.55; charge on the counterfactual workforce 12.05–12.39
  spec 11 (cash): consumption removed $384.41bn of $3991.8bn (9.63%); without defense 12.25%, with the school rows 12.27%
    charge 8.9520; overlap with the account's response 0.86–1.10; charge on the counterfactual workforce 7.85–8.09
  public-pay band 336.6313–398.3100; ends by method 32/27, 32/27
```

- **4a. The sign is right (confirmed).** [CALCULATION: 4b; INFERENCE on the economics]
  - At the reference cell capital adjusts fully, so capital's gain is 0 and P + F is exactly the incumbents' labor
    gain: −176.17 (less skilled) + 187.85 (more skilled) = 11.68 (GDP).
  - The public sector is more skilled (14.40% of the more-skilled base against 7.63%). Its share of the gain is
    therefore positive: +13.61.
  - If public output is unchanged, that part is a transfer from taxpayers to public workers, not production. Charging
    it raises the cost. With the fiscal weight at 1 (the engine default; no specification sets it), the tax on the
    raise nets out, as it should.
- **4b. The payroll matching is clean (confirmed).** [CALCULATION: 4a]
  - All 9,461 public records fall in a skill group.
  - Every public longest job is wage and salary.
  - In only 6 records does longest-job pay exceed the person's own base: $0.02bn of $1,507bn.
- **4c. No double count with P + F.** [CALCULATION: 4b]
  - The charge is exactly the public part of P + F, and P + F less the charge is the private part: −1.93 (GDP) /
    −1.27 (cash).
  - "Exceeds the whole production term" therefore means the model's net production gain at the reference cell comes
    entirely from public workers' pay. Private-sector incumbents lose on net.
  - That is a finding about the model, not an arithmetic error.
- **4d. It does overlap the account's own service responses: about $1.2–1.6bn (GDP) / $0.9–1.1bn (cash).**
  [CALCULATION: section 4; INFERENCE: consumption's removal share proxies the public workforce's]
  - The variant assumes "an unchanged public workforce". The account it is added to removes 9.0–11.4% of government
    consumption at spec 48 (9.6–12.3% at 11) with the group, defense in or out. That removal is priced at today's
    (with-group) wage.
  - The true change in public payroll is L_with·w_with − L_without·w_without. The account plus the charge prices
    ΔL·w_with + L_with·Δw, which counts ΔL·Δw twice.
  - Charged on the counterfactual workforce, the variant is **$12.05–12.39bn at spec 48 and $7.85–8.09bn at spec 11**,
    not $13.61 / $8.95bn. A uniform removal share across skill groups is an approximation. Schools, with more
    skilled staff, have above-average removal (15.7%), so the overlap is more likely larger than smaller.
- **4e. Scope notes, not defects.** [INFERENCE]
  - The GDP normalization scales the labor gain to compensation, while π is a wage share. The public sector's benefit
    share is higher, so its share of compensation, and the GDP charge, would be somewhat larger.
  - Full pass-through is an upper bound for federal pay, which is set by statute.
  - The ends move with public pay, as the candidate says: to specs 32 / 27 (27 ≡ 31) from 48 / 11, band
    $336.63–398.31bn.

### 5. Anything else

Probe: `node infra/immigration-fiscal/candidate_attack_2026_09_28/probe_item45.cjs` sections [5a]–[5c], plus a spec
listing (`node -e` over `specsFor(withCentral({}))`, command in the log below). Output, verbatim (5b abridged to the
candidate and the variants that move the ends):

```
[5a] additivity and unnamed moves (64 specs x 2 methods)
  candidate - sept27 - (item1 + item2 changes): max |diff| 0.00e+0 bn
  what moves, candidate vs sept27 (max |change|): spending:housing_subsidies 0.4018; receipts:enterprise_surplus 0.6161; private_wtp_bn 0.4592; induced_receipts_bn 1.1836
[5b] band ends and the runner-up specification
  candidate:
    hotdeck_union_matched: low 48(shared,gdp,gg 0.6000,low) 320.45 (next 52 +0.00), high 15 386.45 (next 11 -0.00)
    matched_over_pooled: low 48(shared,gdp,gg 0.6000,low) 326.92 (next 52 +0.00), high 15 390.95 (next 11 -0.00)
  cand_public_pay:
    hotdeck_union_matched: low 32(shared,cash,gg 0.6000,low) 333.40 (next 36 +0.00), high 31 396.06 (next 27 -0.00)
[5c] the outer range from components.csv
  19 components; band 323.6827–388.6981; band + sum of negative low-end extremes 260.5184; + sum of positive high-end extremes 437.3750
  outer range with the component read jointly: 260.6094–434.2178 (moves 0.0910 / -3.1572)
spec listing: specs 64 distinct (all fields incl. line_responses) 32; distinct costs 32
  b_hotdeck_union_matched 48-52: 0.000e+0  15-11: 0.000e+0 (both methods)
```

- **5a. The items add exactly, and nothing unnamed moves (confirmed).** [CALCULATION]
  - Candidate − September 27 = item 1 + item 2 to 0.0 at all 128 evaluations.
  - Only `housing_subsidies`, `enterprise_surplus`, P and F move; no other line and no capital component.
- **5b. The ends are 48 / 11, and each ties exactly with a duplicate.** [CALCULATION]
  - Spec 48 ≡ 52 and 11 ≡ 15, identical in every field and in cost.
  - The 64 specifications hold only 32 distinct ones. The school dimension (0.63 / 0.66) has been overridden to full
    cost since September 26, so every spec appears twice.
  - This is harmless for the band's minimum and maximum. Any consumer that counts or averages over "64
    specifications" double-weights each one. This is inherited, not the candidate's.
  - No other specification moves the ends under the candidate, item 1, item 2, or the road cases. Only public pay
    moves them (to 32 / 27 ≡ 31); the candidate reports that the ends move.
- **5c. The outer range reproduces (confirmed): $260.5184–437.3750bn, `summary.json`'s figure.** See 3d for the
  joint reading.

## Files covered and skipped

- **Read in full:** the candidate's `BRIEF.md`, `RESULT.md`, `package.cjs`, `main_case.cjs`, `production_row4.py` and
  `road_congestion.py`.
- **Read in part:**
  - the September 27 `package.cjs` (`capitalReturn`, `evaluateFull`, `specsFor`, `modelFor`, the re-key);
  - `conceptual_audit_2026_09_27/probe_production.py`;
  - `cps_imputation_keys_2026_09_23` `combine_onbooks_lane.py` (row 4), `common.py` and `RESULT.md` §row 4;
  - `capital_return_services_2026_09_27/RESULT.md` §§4, 5 and 8;
  - `scaling_test_2026_09_20` `state_analyze.py` and `README.md`;
  - `sept24_propagation_2026_09_24/real_costs_totals.py`.
- **Skipped:** `sign_reversal.cjs`. It only carries items 1 and 2 through the break-even definition, and those items
  are verified above at every specification. Its break-even figures (2.79–13.07%) were not re-derived.
- **Not rerun:** the candidate's own scripts. They write in place, and the brief forbids editing the candidate. Each
  probe instead imports them read-only.

## Log (append-only)

- 2026-09-28: stub written; probes in `probe_item1_transfer.cjs`, `probe_production_pay.py`, `probe_road_stock.py` and
  `probe_item45.cjs` (this directory, read-only; each runs from the repository root with the command in its section).
- Ad hoc checks, run from the repository root:
  - The spec listing and duplicates (5b): `node -e` requiring the candidate's `package.cjs`. It prints the fields of
    specs 48, 52, 11 and 15, and costs at both methods. It counts distinct specifications with
    `new Set(specs.map(JSON.stringify))` → 32, and costs → 32 distinct.
  - Consumption lines by family (4d): `node -e` listing
    `evaluateFull(modelFor("central", METHODS[0], withCentral({})), specsFor(withCentral({}))[48]).evaluation.spending`
    with `MODEL.spending.lines[].family`. Education: $191.86bn removed of $1,221.2bn (15.7%).
- After the runs, `git status --short` is empty for every lane read (candidate, September 27, September 24, explorer,
  cps_imputation_keys, matched_benefits, service_response_long_run, scaling_test, capital_return_services,
  local_spending_composition). No `__pycache__` was written by these probes: `sys.dont_write_bytecode` is set before
  every import.
- Worker: response, model claude-opus-5-5.
