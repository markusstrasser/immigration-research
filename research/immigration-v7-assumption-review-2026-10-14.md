# Assumption review of main case v7, 2026-10-14

[2026-10-15: rounds 2–4 are under "Later rounds" below; the case converged at round 3.]
[2026-10-15 09:59 JST: the convergence claim is withdrawn; see the last correction under "Later rounds".]

**Verdict:** Round 1 found four corrections to the case over its $5bn bar, each executed in its own lane: US tax on
foreign-source income sat in item 6's corporate lines; the union's reporting rule dropped US-born reporters with one
US-born parent; the non-members who stay in mixed units were only partly recomputed; and the Census undercount was
kept beside on a premise the population controls contradict. They are the items of main case v8. Round 1 also
corrected every consumer model it reviewed: the world ledger's incidence, the comparators' symmetry, who wins, the
social pairing's crime and environment rows, the back-cast's rules and the generation split's routing. Round 2 runs
on those fixes; v8's items get their own round-2 packet.

## What ran

- **Bar** (the operator, 16:18: "until it's mostly nitpicks or +- 5B$"): a finding counts if it plausibly moves either
  end of the headline by $5bn or more, flips a stated claim, or invalidates a method. For the consumer lanes the same
  bar applies to their own stated claims (the share of other residents ahead, the back-cast's cumulative range, the
  fiscal-plus-social pairing).
- **Six packets** (critique skill, `model-review.py`, preset cross4 from triage, each with a repo-reading premise
  scout on GPT-6 Astra at low effort). Each carried the v7 decision, the CLAUDE.md headline block and the v6 review's
  dispositions, with the instruction not to re-raise a recorded rejection without new evidence.
  - A, taxes on job capital (item 6), 99 KB: the item lane's RESULT, the v6 review's finding 2, decisions 09-27 and
    09-29, FAQ 4 and 14.
  - B, who is counted (items 5, 5b, the coverage bound, the union rule), 115 KB: the case's items and approximations,
    the child-credit and coverage lanes, the v6 review's findings 1 and 3, decision 10-05, FAQ "Before combining"
    and 19.
  - C, the generation split and the comparators, 81 KB.
  - D, the world ledger, 74 KB.
  - E, who wins and who loses, and the back-cast, 60 KB.
  - S, social costs and crime, 74 KB.
- **Axes:** Gemini 4 Argon at high effort on structure and gaps (paid API); GPT-6 Astra at medium on correctness and
  contracts (subscription); Opus 5.5 at max (subscription). Served models are recorded in each axis's `meta.json`.
- **Tokens** (llmx usage log, `~/.claude/llmx-usage.jsonl`):

  | Packets | Model | Calls | Input (cached) | Output | Reasoning |
  |---|---|---:|---:|---:|---:|
  | A–D | Opus 5.5 | 5 | 28.65M (27.71M) | 484k | 414k |
  | A–D | GPT-6 Astra | 28 | 2.62M (1.68M) | 63k | 2k |
  | A–D | Gemini 4 Argon | 9 | 247k | 39k | 89k |
  | E, S | Opus 5.5 | 3 | 10.50M (10.06M) | 215k | 181k |
  | E, S | GPT-6 Astra | 14 | 1.47M (1.07M) | 35k | 1k |
  | E, S | Gemini 4 Argon | 5 | 84k | 18k | 35k |

  Argon cost about $2.5 at its $2 / $10 per million rates; the subscription lanes bill nothing per call.
- **Findings:** 347 extracted (A 49, B 71, C 51, D 56, E 64, S 56), every one disposed of below. The extraction's
  automatic verification was mostly inconclusive; each finding that drives an action was checked at its source (code,
  derived file or primary document) before it was acted on.
- **Fix lanes** ran on GPT-6.1 Sol at high effort (`lane run --worker codex`), each writing only its own directory;
  the parent reran every one with `scripts/rerun_lane.py` (IDENTICAL) before committing it.
- **Limits of the review.** The critics read packets; none reran code, so every rerun receipt here is the parent's. The Opus axis shares a model family with the author of most of the work under review, so it does not give an independent failure profile; the Argon and Astra axes do.
- **Artifacts:** ignored and kept locally under `.model-review/2026-10-14-assumptions-v7-r1-*` (each axis's output, coverage.json, findings.json) with the per-finding map, `.model-review/2026-10-14-assumptions-v7-r1-dispositions.md` (every one of the 347 findings, once); the packets are `.model-review/assumptions-v7-r1-*.md`.

## For the operator

The calls below are in `HUMAN.md` with the evidence; the work proceeds on each recommendation unless he says
otherwise.

- The Census undercount in v8's central (recommended: yes, switchable).
- The mixed-unit removal in v8's central (recommended: yes; the lane advised an arm).
- Item 6's low end: keep corporate taxes at response 1 and correct the stated premise to mobile capital with
  replacement returns (recommended); fixed-rent and vanishing-rent arms beside.
- The value of a death: uniform DOT VSL with life-years beside (recommended).
- The winners verdict: stationary financing, cohort beside (recommended).
- The world ledger's public-goods willingness to pay: report-only (recommended).
- The evidence map, explorer and figures page to v8 once its docs pass is done, and the push (recommended: yes).

## Acted on

| Finding(s) | What was wrong | Fix | Commit |
|---|---|---|---|
| A07, A11 | The first-year arm kept item 6 at its whole long-run size | Item 6 at its first-year part; first year $273–326bn, $198–251bn cash; C1 holds | cfb7df47, 425a29fe |
| C21 | FAQ 10 quoted the shared allocation for a group total | Personal: −$224bn → −$322bn | 63ced0a3 |
| S27, S29 | The real-costs memo described the September 23 justice key as current | States FBI 2024 arrests with the booking correction | c88af8e0 |
| A19 | "Within industries" described a pooled comparison | 2.6 of the 7.5-point small-firm gap is within cells | c88af8e0 |
| A02, A06, A10, A13, A28, A46, A12, A25, A27, A40, A49, A34, A35, A43, A44, A14, A15, A31, A42, A17, A37, C43, A21, A24, A26, A30, A47 | Item 6's keys and responses | Refinement lane: K2 (foreign-source tax out) +$3.77 / 1.40bn recommended; K1, K3–K7, network, land as arms; joint outer range $330.6–432.3bn | fb667a55, c90b0e32 |
| A16, A36 | Business-serving services keyed to households | Location keys: −$1.12bn at both ends; keep v7's central | 2b712e1a |
| B10, B24 | The union's generation rule drops US-born reporters with one US-born parent | Completion: +$2.89 / 3.76bn central, +$5.56 / 6.75bn counting every omitted reporter | 25d88a0a |
| B01–B05, B08, B11, B12, B14, B16, B19–B23, B25, B26, B28, B33–B35, B38, B40–B53, B55, B56, B58, B60, B63, B65, B66, B70, B71 | The removal left the surviving non-members' taxes, credits, benefits and consumption partly computed | Mixed-unit removal: tax +$6.77bn (SE $4.08bn), stack +$10.08bn; extension running | 1ee34b6f |
| B (coverage cluster) | v7 called the coverage figure an upper bound partly absorbed by the 2024 controls; the V2024 base keeps the Census Hispanic total | Re-derived as a two-sided sensitivity: +$11.09 / 14.83bn central construction, −$16 to +$26bn across constructions | 69f7ba9d |
| D (incidence cluster) | The world ledger debited employer payroll and item 6 to the group, valued remittances at nominal rates, and held G3+ at its zero bound | Corrected: R1 world +$472.3 / 354.7bn at the G3+ zero bound; other US residents −$357.0 / −490.2bn at every reading | 951fdcd7 |
| C (comparators cluster) | The white and Black comparators lacked own production, own mortality and all-origin status keys | Black $400.0 / 478.6bn on its own count (was $422.7 / 501.1bn); the lineage's gap to the same number of whites $541.0 / 512.4bn | 9b5cd748 |
| S (crime cluster) | Security compared unlike populations, fear took a fixed victim baseline, the mixed-offender fix sat at one end, and the lineage's own harms counted as outsiders' | The P7 crime rule: pairing $440.05–537.45bn (+$0.6 / 4.6bn); arrest footing beside | 8380cfd5 |
| S (environment cluster) | PM2.5 counted the group's consumption but not what others buy with the transfers saved; exposure stood in for deaths; crashes and volunteering ran one way | Named stack $428.4 / 514.1bn against $439.4 / 532.8bn; CO2 and life-years beside | cafedafc |
| E (back-cast cluster) | The low end's capital return at 2% against decision 09-27; a whole-budget base; income scaling on part of the carried parts | Corrected stack $2.85–4.02tn over 2015–2024 (was $3.0–4.0tn), live with v8 | 74ce1f67 |
| E (winners cluster) | The pension accrual and borrowing allocated to no one; sharing rules called bounds; the added people in the payer pool; channels incomplete; tables on September 24 | Stationary financing, complete channels, corrected payer pool: 4.6% / 8.4% of other residents ahead (was 19.6% / 18.7%); a minority ahead at every grid point | 95f151e5 |
| E31 | Perfect within-cell substitution uncalibrated | Literature ε 8.7 / 17.9 arms: shares ahead move under 0.5 points; the native vs earlier-immigrant wage split flips sign with ε (stated as undetermined); ∞ stays central | 323586e2 |
| B (mixed-unit cluster, round 2) | The first pass left benefits, health takeup and survivors' records partly computed | Unified removal replacing item 5b and D once: +$10.7 / 14.5bn (SE $4.4bn), adopted in v8 | 1c3ecb87 |
| A01, A05, A08, A18, A38 | The low end's premise described as rents scaling with the market | The payload's rule is mobile capital with replacement returns; wording corrected in v8; φ unmeasured, fixed-rent (+φ × $28.4bn) and vanishing-rent (to −$13.8bn) arms beside | 63862fb9 |
| C20, C32, C34 | No check that living prose cites the live case | `live_case.json` and `citation_freshness.py`; four flags for the v8 docs pass | b6af3c66 |
| D18 | The world ledger said fix 6b leaves Mexico's row fixed | Dated correction: its world delta runs +$6.9bn (equal weights) to −$2.2bn (λ 1.5), under the bar | 1ed6fd8b |

## Open: unmeasured, each needing the evidence its row names

None of these is a confirmed correction of the size a reviewer proposed; the per-finding map has each row.

- **The case:** a joint guard on receipts, private income and source taxes under one counterfactual (A04); pass-through
  owners' rents, which matter only under a vanishing-rent premise (A41); depreciation timing in the industry tax
  shares (A48); descendants of families resident before 1848 who report Mexican origin, in the union by its
  definition and uncounted (B36).
- **Comparators:** the nonlinear row-13 imputation and the mixed-unit child-credit crossings for the comparison
  groups (C16, C26, C38, C46, C51); FAQ 7's education cells sit on a different ledger (C15, a scope note).
- **World ledger:** the G2 cohort counterpart to the stationary schooling rule (D33, D49), bilateral employer benefits
  (D34), industry-matched Mexican pay (D45), terminal-cohort transport (D48), Mexico's welfare and revenue-cost
  parameters (D50, D55), the same offenders' harm in Mexico (D54), remittance-financed spending in Mexico's
  consumption-tax rates (D56).
- **Who wins:** the education split on the corrected frame (E29), pre-2019 medical eligibility (E30, E34, E57),
  state incidence (E53), joint migration, wage and rent adjustment (E59), historical payable benefits (E61).
- **Social side:** school composition (S09), urban and production overlap (S23), marginal binding caps (S24), the
  added people's behaviour proxies (S39, S51), the distribution's payer frame (S40), owner incidence (S44), ICE
  overlap (S46, S56), care mortality (S49), spatial marginal pollution damage (S53).

## Disposition counts

The per-finding map disposes of 258 findings, packets C, D, E and S and the 31 A and B findings not in the rows
above:

| Disposition | Findings |
|---|---:|
| Acted on | 100 |
| Arm | 39 |
| Below the bar | 7 |
| Rejected | 4 |
| Repeat of a recorded ruling | 23 |
| Docs | 31 |
| Open | 38 |
| For the operator | 16 |
| **Total** | **258** |

The other 89 A and B findings are in the rows above (acted on) and the list below (rejected).

## Rejected

- **A29** (the added descendants as scaled cells rather than person keys): they are unobservable in the survey by
  construction; the case prices them on the identified third-plus members' records at their measured ages.
- **A39** (small-open-economy premise untested): the long-run premise is a steady state with a fixed time preference,
  in which the capital stock adjusts fully whatever the economy's size; the small-open case gives the same answer.
- **A45** (missing known-leads file): a packet artifact.
- **A33**: agrees with the item lane's own reading.
- **B13, B18** (the added descendants' age mix) and **B29** (later losses at C3): repeats of v6's rulings with no new
  evidence. The data do not choose between the co-resident and cohort-at-birth mixes; the measurement that would settle
  it (ages among adults living apart from their parents) is named in the v6 review. Later losses stay beside
  (−$3.8 / 5.0bn) because v5 rests on co-resident fourth-generation adults' measured C (−0.35 to −0.86).
- **B31** (whole-person removal as the dominant framing): the operator's v5 choice; the ancestry-share reading stays
  beside.
- **B37** (probes without sampling error): the lanes that acted on the probes report replicate SEs.
- **B57** (a CSV alias changes meaning): no UI or consumer reads the alias; `case_ends.cjs` and `row4_oct14.cjs` intend
  the live case.
- **B64** (static household responses): no direction or size was offered; the account is a static allocation
  throughout.
- **C13** (distribution comparisons lose the shared specifications): `case_ends.cjs` gates `MAIN_SPECS`, the 32
  personal specifications, by design.
- **C19** (uncertainty uses legacy variance keys for item 6): `propagate.py` carries `job_capital_replicates`
  (lines 504–540, 984–986, 1356, 1394).
- **C44** (legacy index 48): specification 48 is addressed only in historical lanes (v5's lineage case, the receipt
  probe, candidate lanes).
- **C47** (generation misclassification extrapolated from co-resident adults): unverified; no alternative source.
- **D32** (Mexican fiscal savings lack a financing constraint): a misreading; the Mexico rows are the budget's own
  balance at Mexico's rules.
- **D46** (descendants' existence and Mexico's equilibrium): the same-person ruling stands.
- **E04, E22, E39, E42** (the back-cast range drops rules): a packet artifact; the memo, README and FAQ 8 quote
  $3.0–4.0tn across rules.
- **E07** (the capital return financed as a current tax): the return is what holding the group's share of public
  capital costs in the year it is held, financed then by taxes or borrowing; rules (a) and (b) allocate it as they
  allocate any other cost.
- **E36** (owner-occupied housing flows): in an annual flow ledger an owner-occupier's imputed rent cost and imputed
  rent income cancel; asset windfalls are a stock effect outside it.
- **S02 as stated** (crashes on fixed roads, +$18–25bn): the direction is reversed. With roads that grow with traffic,
  density with and without the group is the same and other residents' risk per mile does not change, as decision
  09-29 says; the consistent row is smaller. The lane recomputes it on the case's road response.
- [2026-10-15: reversed in S3, under "Later rounds"] **S04** (the pairing's low end uses $334.8bn silently): §7 of the real-costs memo and the FAQ's "Before combining"
  say so.
- **S05** (all Hispanic victims treated as Mexican-origin): `victim_cost.py:435–458` splits Hispanic victims by the
  Mexican share of the group's tract-level exposure; "all in-group" is the labelled lower-bound arm.
- **S11** (progressive taxes on the wage shift go uncredited): `distribute.py` taxes each skill cell's wage change at
  the nest's rates (0.384 / 0.426), and gates after-tax wages to P and the taxes to the induced receipts the fiscal
  account credits (lines 586, 1120).
- **S18, S52** (PM2.5 traffic refill): refill needs fixed roads, which the case's long-run road response rules out;
  binding caps are checked in the lane.

## Later rounds, 2026-10-14 to 2026-10-15

**Verdict:** The case converged. Round 3, on v8's four items, found nothing over the bar and one method error, which
was corrected in place (−$3.2bn at every end): v8 is $365.8–456.0bn. The two companions are still moving. Round 3 on
the social side found two corrections over the bar, which put the fiscal-plus-social pairing at $477.7–573.4bn.
Rounds 3 and 4 on the comparators each found corrections over the bar, and round 4's are still being executed.

### What ran

| Round | Started (JST) | Packets | Findings | Axes |
|---|---|---|---:|---|
| 2 | 10-14 23:40 | C2 generation split and comparators (49), D2 world ledger (49), E2 who wins and back-cast (51), S2 social (56) | 205 | Argon, Astra, Opus, premise scout |
| 3 | 10-15 02:04 | v8's items 9–12 | 53 | Argon, Astra, Opus, premise scout |
| C3 | 10-15 04:18 | the comparators on v8 | 44 | Argon, Astra, Opus, premise scout |
| S3 and C4 | 10-15 08:38 | the social pairing on v8; the comparators after C3's fixes | 12 and 16 disposition rows | Argon and Opus only (the Codex plan was exhausted); no extraction |

Each finding was disposed of once. Round 2's routing is in the parent's scratch notes. The other rounds' maps are
`.model-review/2026-10-15-assumptions-v8-r3-dispositions.md`, `…-r3-c3-dispositions.md`, `…-r3-s3-dispositions.md`
and `…-r4-c4-dispositions.md`; all are ignored and kept locally. Every finding that drives an action was checked at
its source.

Tokens come from the llmx usage log, counting this repo's rows in each round's window. Opus's output count includes
its reasoning.

| Round | Model | Calls | Input (cached) | Output | Reasoning |
|---|---|---:|---:|---:|---:|
| 2 | Opus 5.5 | 4 | 26.53M (25.49M) | 515k | 453k |
| 2 | GPT-6 Astra | 21 | 4.13M (3.01M) | 48k | 4k |
| 2 | Gemini 4 Argon | 8 | 251k | 42k | 214k |
| 3 | Opus 5.5 | 1 | 9.10M (8.79M) | 168k | 154k |
| 3 | GPT-6 Astra | 4 | 804k (526k) | 7k | 0.5k |
| 3 | Gemini 4 Argon | 2 | 82k | 10k | 24k |
| C3 | Opus 5.5 | 1 | 5.46M (5.25M) | 112k | 95k |
| C3 | GPT-6 Astra | 3 | 648k (504k) | 6k | 0.5k |
| C3 | Gemini 4 Argon | 2 | 54k | 10k | 34k |
| S3, C4 | Opus 5.5 | 2 | 17.06M (16.56M) | 269k | 233k |
| S3, C4 | Gemini 4 Argon | 4 | 152k | 19k | 88k |

### Round 2: round 1's fixes

| Packet | What was wrong | Fix | Commit |
|---|---|---|---|
| C2 (R2C02) | The gaps differenced the exact case lineage against rough-engine comparators | Both sides on the rough engine, with the case bridged line by line | 8525b3da |
| C2 (R2C19, R2C21, R2C30) | One status scalar moved receipts into unaffected brackets; pension ratios on one payroll multiplied another | Each CBO × pooled-AGI cell's pre-status total restored; same-payroll ratios | 8525b3da |
| C2 (R2C40) | Item 11 on the lineage side only | Measured for both comparators at their own count (whites −$35.4 / −17.8bn, SE $12.1bn; Black −$2.33 / +0.65bn) | 0dec6a29, 2abbd628 |
| C2 (R2C01, R2C16, R2C27, R2C46) | The gaps mixed group-specific and whole-population mortality | Every row carries its mortality convention; the lineage's own mortality measured (+$3.5bn, beside the headline); a guard refuses a stated claim built on a mixed pair | 6d124dea, 8525b3da |
| C2 (R2C18, R2C22, R2C24, R2C31, R2C41) | All 809,760 added G3-rate minors went to G2 parents by assumption | Their linked parents' birth records measure the share (s = 0.3365, SE 0.045); moves money between G2 and G3+ only | b78a05a1 |
| C2 (R2C03, R2C11, R2C13–15, R2C20, R2C44) | The G2-adult figure was a residual carrying minor-equivalents; per-adult figures had no contents or SE | A direct age cell; numerators by rule with replicate SEs | b78a05a1 |
| S2 (R2S11 and the mortality cluster) | Plume deaths priced at exposure; three mortality bases across crime, PM2.5 and crashes | Deaths reweighted for receptor mortality (outsiders' harm $74.43 → 73.90bn); one basis | 3fc2b913, e8edda58 |
| S2 (re-spending, crashes, roads) | Re-spending on CE units; crashes counted single-vehicle deaths; congestion on a stale road key | PCE central (CE beside); multivehicle crashes only; the live highway key (matched congestion relief $12.95 / 10.22bn) | 053fe5be, e269bcb8 |
| S2 (joint) | — | Pairing on corrected v8: $462.2–561.6bn; 20 findings below the bar, logged | 3ce8f5bb |
| E2 (back-cast) | Rate leg, income rules and programme parts as in the packet's findings | Fixed returns at 2 / 3%, per-part income rules, programmes measured on the live case: $3,729–4,468bn over 2015–2024 | 997047de |
| E2 (who wins), D2 (world) | Pooling one way across mixed units, rule (c) without jurisdiction, accrual through general funds, health harms per head; Mexican payroll deposits taxed, mixed price bases, G3+ bounds, the capital-source row, arm 6b | Measured on v7's inputs: stationary shares of other residents ahead 3.34% / 5.50% / 9.74% under rules a / b / c; world R1's low end +$472.3bn → +$420.5bn under the operator's price rule (no US prices for services abroad). Their v8 runs are in progress; outcomes and commits will be appended when they land | — |

### Round 3: v8's items

| Finding | What was wrong | Fix | Commit |
|---|---|---|---|
| R3-12 | Coverage charged the 1.68M missed adults a share of the lineage's custody, arrest and ICE costs. Those group totals are administratively complete: each is a survey count times a rate with an administrative numerator over the survey-controlled population, so the undercount cancels | Missed people take zero on use-keyed lines with administrative totals; the per-head part (+$1.59bn) stays; −$3.155bn at every end in both sets | d1a24d47 |
| R3-03 | A missing live coverage file silently loaded the historical stub | `coverage.cjs` stops `[BLOCKED]` unless a fixture asks for the stub | b8b23c76 |
| R3-05 | The first-year, school-within-district and shared-allocation readings carried items 11 and 12 at their central long-run amounts | Each prices them under its own rules (first year $294.4–351.7bn) | d1a24d47, cb1aea1d |
| R3-01, R3-04, R3-06 | Item 11's consumption and owner-property parts (M5, +$5.51bn) were called mechanical; "every pair measured" overstated the interaction table; K1 was called a stipulated response | M5 rests on the stayers keeping their propensity to spend out of their own resources (central kept, v7's equal split beside, −$5.51bn); item 12's row holds its interaction with items 9–11 (+$0.91 / 1.03bn); K1 is a conditional key, and K7 brackets v8 as an arm | cb1aea1d |
| R3-14 | The switch from demographic analysis to the PES at age 5 was not argued | Criterion stated: DA where it agrees with the PES or the PES understates the young-child undercount, the PES where they diverge (2.9 SE at 10–17, 9.6 SE at 18–29). DA through 17 beside: $363.2–453.1bn | d1a24d47, cb1aea1d |

**Rejected.** R3-02 (demographic analysis through age 29 instead of the PES from age 5): no age is counted twice, and
the central reproduces the PES's all-age Hispanic undercount (an implied 5.12% against 4.99%, SE 0.53). DA through 29
implies 2.42%, 4.8 SE away, so it stays beside at $362.0–450.2bn. R3-08 (item 6's high end contradicts its low end's
premise): the ends are the two premises the band spans. R3-09 (coverage breaks national key conservation): the PES's
national error is −0.24% (SE 0.25). R3-13 (item 10's reporters double count justice use): the union's share is its
count times the Mexican-coded rate, and v7's count excluded the reporters.

**Beside or framing.** Item 11 is [FRAMING-SENSITIVE] (R3-15). It rests on the whole-person static removal with no
re-partnering, the operator's v5 frame. A re-matching arm is unpriced; a reviewer's estimate of −$6 to −10bn was not
computed. The spousal pension proxy (R3-16, +$2.75bn, range 0–13.9) stays beside because only one direction is
measured. The rest fell below the bar, each under $2bn, and are listed in the map.

### C3: the comparators on v8

All five findings over the bar sat on the comparator side, and one rule now applies to all three groups (4548e70f;
consumers 608fc28f):
- members' biological minor children depart and count as members (whites +6.11M, Black +1.21M, the lineage's block
  0.341M);
- each comparator carries its own 2020 PES coverage (whites' is a net overcount, −2.28M; Black residents are missed by
  1.10M);
- every group's K-12 is priced on its own cell at state spending per pupil;
- group survival moves only the retirement share of the accrual;
- A3 and A4 take A1's item 11, reweighted.

On the central (own mortality), the lineage costs $545.0 / 520.1bn more than as many whites (was $571.3 / 542.6bn),
and Black residents cost $63.9 / 57.4bn more than the lineage at their own count, $76.7 / 72.6bn at the lineage's.
The children rule moves the most (−$38.7 / 35.2bn on the white gap). Not computed: the household-type split of item
11.

### S3: the social pairing on v8

| Finding | What was wrong | Fix | Commit |
|---|---|---|---|
| O-F1, A-arch-F1, A-gaps-2 | Re-spending of the budget saving was central, while the PM2.5 from the public purchases the same response removes sat beside | Both central, as a declared counterflow pair: the removed public consumption (417.42 / 444.50bn) at government-average PM per dollar | 7342b331 |
| O-F2, A-arch-F4, A-gaps-x1 | The low end priced the fiscal row on the raw-coded justice key ($334.8bn on v7) | The case at both ends ($365.8bn low); victims on the equal footing; the matched footing beside. This reverses round 1's S04: the raw key is unstable because of a residual "Other Hispanic" code (`cj_use_allocation_2026_09_23/RESULT.md:55`) | 7342b331 |
| O-F3, A-arch-F3, A-gaps-1 | v8's 0.52M completion and 1.96M coverage people carried no social rows | Priced at their own keys, with item 11's consumption shift (−4.16% of the union's consumption-keyed rows); crime rows zero for them; net +$1.5 / 1.7bn | 7342b331 |

Pairing: $477.7–573.4bn (was $462.2–561.6bn). Three findings were rejected (re-spending on the set, netting M5 out
of the saving, and a fiscal–social overlap in injury costs) and six fell below the bar; all are in the map.

### C4: the comparators after C3

Three findings over the bar are being executed in one lane, with results to be appended:
- the children rule hands 1.443M lineage members to A1 (Black 0.215M), so lineage precedence becomes the central;
- the case's school price differential sits on the lineage only, so each group gets its own district differential;
- A2–A4 and the all-residents slice never moved to C3's rules.

Black's demographic-analysis coverage range (missed people 0.40–0.52M against the PES's 1.12M) goes beside; it is
at the bar. Two claims were rejected:
- Argon's 0.5 weight for a mixed child is the ancestry-share frame the operator declined for v5, and the rule is
  symmetric.
- Its claim that the people the Census misses earn much less cites NBER WP 31231, which is Baqaee, Burstein, Duprez
  and Farhi's "Consumer Surplus from Suppliers".

### Corrections to round 1's record

- D18: fix 6b's world delta runs +$6.9bn (equal weights) to −$2.2bn (λ 1.5), so it is over the bar at equal weights.
  The world ledger's RESULT carries the same correction (04357abf), and round 2 dropped 6b (D2 fix 5).
- S04: reversed in S3, above.

### Correction, 2026-10-15 09:59 JST: the case has not been shown to converge

This section's verdict says the case converged. The evidence does not support that. Round 3 reviewed only v8's
four new items. The two whole-case reviews so far each moved the headline by $25–50bn: the v6 review's findings
became v7 ($389.1–461.5bn → $339.6–423.6bn, −$49.5 / −37.9bn), and round 1 on v7 became v8 (+$26.2 / +32.4bn).
Whether the case has converged needs a whole-case review of v8. Round 5 runs one: the frame (F), the consumer
lanes no round had reviewed (U1, U2), and whole-case packets on receipts, spending and who is counted.

## Round 5, 2026-10-15: whole-case and frame review of main case v8

**Verdict:** Round 5 did not converge. The whole-case review found material rate and military-service corrections.
They become items of v9, with the smaller measured refinements below. `main_case_2026_10_16` is a candidate under
review. The frame review found no new headline correction. It corrected explanatory claims and added a matched
average-resident comparison to the social lane's build. The consumer reviews corrected companion claims without
changing the headline. This does not reinstate the convergence claim withdrawn above.

### What ran

The whole-case packets covered receipts (W-A), spending and responses (W-B), and who is counted (W-C). U1 covered
distribution weights, within-group households and uncertainty propagation; U2 covered debt and pension stocks,
closed-budget, legacy, Indian and late-arrival comparisons. F reviewed the frame and reader-facing claims. The
bar remained $5bn at either end, a stated-claim reversal, or a method failure; consumer findings were judged
against their own claims.

The W and U verifiers read the five outputs for each packet: the architecture and gaps reviews labelled Argon,
Opus, the Astra premise scout, and the separate Astra-max review. F had an anchored packet and an F-blind packet.
The anchored packet had Argon architecture/gaps and Astra scout/max outputs; anchored Opus produced no output
after a transport failure. The blind arm had Opus, Astra scout/max, and two architecture/gaps runs actually served
by Astra after Argon rate-limit fallbacks. The first blind architecture/gaps run received the blind scout; the
second did not. These were different contexts, not a controlled repeat. Only F's steering header was blinded;
the common body retained the decisions and prior rejections. [SOURCE: WA/WB/WC/U1/U2 coverage sections; F
“Anchored versus blind, model by model”]

Every finding below has a disposition. The verification records retain the reviewer labels, source traces,
calculations, disagreements and limits. Their classes describe the verification at that point; the later measured
lanes and the parent's final dispositions govern the v9 selections. They are kept beside the raw reviews, in the ignored `.model-review/` directory:

- **WA:** [receipts verification](../.model-review/2026-10-15-assumptions-v8-r5-WA-verification.md).
- **WB:** [spending verification](../.model-review/2026-10-15-assumptions-v8-r5-WB-verification.md).
- **WC:** [counting verification](../.model-review/2026-10-15-assumptions-v8-r5-WC-verification.md).
- **U1:** [distribution and uncertainty verification](../.model-review/2026-10-15-assumptions-v8-r5-U1-verification.md).
- **U2:** [stocks and comparators verification](../.model-review/2026-10-15-assumptions-v8-r5-U2-verification.md).
- **F:** [frame verification](../.model-review/2026-10-15-assumptions-v8-r5-F-verification.md).

These are LLM-assisted reviews of a politically charged question. Reviewer agreement does not identify an effect.
The checks below establish source behavior and conditional arithmetic; the choice of counterfactual remains
explicit. [INFERENCE; FRAMING-SENSITIVE]

### Measured for v9

Amounts are annual $bn of net cost to other US residents. Positive raises cost. Low/high denotes the fixed v8
personal specifications 16/11, averaged across its two methods. “Set” retains earned pension promises; “cash”
switches members' OASDI/Part A to paid benefits and retains the account's other imputed/accrued costs. These are
conditional changes on v8, not independently additive corrections or newly optimized v9 endpoints.

| Finding | v9 item and selected rule | Change on v8, low / high | Evidence |
|---|---|---:|---|
| WB01 | **20, one rate:** Trustees' path for both legs at both ends, one-rate arm B | **+1.58 / −19.70**, set and cash | `one_rate_2026_10_15/RESULT.md`, arm B and “Rate definitions” |
| WB02 | **13, military service costs:** response 0 for service compensation, the three direct VA medical accounts, GI Bill, life insurance and TRICARE, with defense fixed | **−18.9 / −18.9**, set and cash | `spending_keys_r5_2026_10_15/RESULT.md`, step 3 |
| WB06 | **14, administration:** retirement block only | **−0.30 / −0.30**, set and cash | `spending_keys_r5_2026_10_15/RESULT.md`, item 14 and its incomplete-program bridge |
| WB07 | **15, colleges:** block response 0.886 | **−4.1 / −4.3**, set and cash | `spending_keys_r5_2026_10_15/RESULT.md`, item 15 |
| WC01; W14 | **16 and 17, native-minor calibration and missed people's tenure:** joint, fixed-count selection | **−0.44 / −0.95 set; −0.03 / −0.54 cash** | `count_composition_r5_2026_10_15/RESULT.md`, joint row and selected-item contract |
| W02, W03 | **18, household taxable basket only** | **+0.26 / +0.26**, set and cash | `consumption_tax_bases_r5_2026_10_15/RESULT.md`, household-only joint proxy |
| W04, W05 | **19, pass-through source taxes:** national immediate-individual-owner proxy | **−3.4 / −0.7**, set and cash | `passthrough_source_tax_r5_2026_10_15/RESULT.md`, final handoff |

The rate selection follows the operator's 11:47 note that 3% exceeds the roughly 2% market/Trustees basis. Arm B
retains the pension path and uses its 2.0811% level-real-perpetuity equivalent for capital. It does not revalue
externally booked public-employee normal costs. The alternative flat-rate arm A (+$1.79 / −36.70bn set) stays
separate. [SOURCE: parent's disposition; CALCULATION: one-rate RESULT, arms and rate inventory]

Item 13's displayed parts close at the displayed precision: compensation −$10.1bn, service-benefit extensions
−$2.9bn and direct VA medical −$5.9bn, total −$18.9bn. The medical mass is a declared fiscal-to-calendar-year
approximation from VA's three direct accounts, not an observed NIPA decomposition or group-specific use estimate.
Community care is a transfer and is excluded from that consumption mass. This uses L1 **through “L1 STEP 3 DONE”**;
its earlier medical exclusion is superseded. [SOURCE/CALCULATION: `spending_keys_r5_2026_10_15/RESULT.md`, step 3]

Item 14 does not adopt the −$12.7bn population-key screen. The current key sits between SNAP and Medicaid caseload
shares; the complete program bridge remains unmeasured. Item 16 is survey-weight calibration with household
identities and generation masks fixed. Its −$6.74 / −7.27bn fixed-G2-price screen was not the final measured effect.
The joint 16/17 row includes their interaction; adding their standalone rows would give a different answer.
[SOURCE: parent's disposition; `spending_keys_r5_2026_10_15/RESULT.md`; `count_composition_r5_2026_10_15/RESULT.md`]

Item 18's business-purchase arm (+$12.1bn) stays beside: it keys input taxes to production, against CBO's consumption
incidence. Item 19 is an explicitly conditional proxy. Its full-FTC diagnostic (−$5.02 / −1.19bn) and W09's extended
compliance/legal-form arm (+$3.40 / +1.26bn) stay beside. Neither supplies an identified replacement-investment
allocation. These selections do not certify the unmeasured ownership, coverage or mixed-unit interactions.
[SOURCE: parent's disposition; `consumption_tax_bases_r5_2026_10_15/RESULT.md`; `passthrough_source_tax_r5_2026_10_15/RESULT.md`]

### Whole-case findings kept beside, below the bar, or refuted

Each ID refers to its row in WA, WB or WC. Sizes below are $bn, low/high where available. **Screen** means held-fixed
arithmetic; **estimate** means a reviewer's unmeasured amount. Neither is a booked correction. Cash is distinguished
where it differs. Recorded findings retain their unresolved limits.

| ID | Claim | Disposition and size | Evidence anchor |
|---|---|---|---|
| W01, W15 | Top federal/state tax shares are overstated | **Measured below bar:** pooled federal +0.25; with California +1.84, each end/set. Tail truth remains unidentified; the old +$7.9 / +13.2 screens are not corrections | `top_income_share_2026_10_15/RESULT.md`, pooled arms; 0dfd6376 |
| W06 | US corporate tax on replacement foreign investment offsets source taxes | **RECORDED:** cost up if it raises absence receipts; review's 1–3 estimate has no measured high end | WA W06; R3-11 |
| W07, W08, W10 | B/D timing mismatch; unauthorized accrual unadjusted; personal-tax compliance absent | **REFUTED:** 0 from each alleged omission. B/D stay cash, status scales accrual, and baseline compliance adjusts both income taxes | WA W07/W08/W10 source callers |
| W09 | Joint corporate compliance/legal-form correction | **RECORDED-NEW; arm beside:** measured extended proxy +3.40 / +1.26, both sets; already-adopted K2 cannot be added again | WA W09; L3b final W09 arm |
| W11, W12 | M5 disposable-income, rank, size and remittance feedback | **RECORDED:** signed direct-tax loss 8.62 is exposure; removing M5 gives −5.51, an existing alternative. Behavioral correction unmeasured | WA W11/W12; R3-01 |
| W13 | Identical survivor tax in set/cash mishandles SS taxability | **CONFIRMED-BELOW implementation premise:** 0.5–1.5 estimate, sign unmeasured; no established boundary violation | WA W13, SS-tax diagnostic |
| W16 | Future-law companion omits tariffs and business expensing | **Companion scope correction; headline 0.** Legacy break-even lead withdrawn for a subset statement. FY2028 expensing +4.23 / +1.57 and historical CY2025 customs −16.93 are different objects, not a net total | WA W16; L3a companion |
| W17 | Business current transfers should respond | **CONFIRMED-BELOW:** response-1 exposure −4.12 on packet pricing, not a verified missing tax | WA W17 |
| W18 | Personal transfers need a payer key rather than retail spending | **CONFIRMED-BELOW:** +1.5–3 estimate, direction unproven | WA W18 |
| W19 | Other contributions need program/uncapped-SDI keys | **CONFIRMED-BELOW:** cost-down up to 2 estimate, net sign unmeasured | WA W19 |
| W20 | Additional Medicare Tax needs its threshold key | **CONFIRMED-BELOW:** 1.76 positive-component exposure, not measured over-allocation | WA W20 |
| W21, WC08 | Near-zero headcount error does not prove zero fiscal-key error | **RECORDED-NEW:** receipt-only screen +2.23 / +2.17 set; full omissions-only arm −3.01 / −3.48 set, −2.18 / −2.64 cash. These are overlapping alternatives | WA W21; WC08 |
| W22 | Fixed mining output with higher replacement wages need not leave profit fixed | **RECORDED-NEW:** historical corporate exposure about 1.6 / 0.6; wage shock unmeasured | WA W22 |
| WB03 | Equipment/IP capital returns omitted | **RECORDED:** original variant +0.68 / +1.16; current-order 0.8 / 1.3 estimate | WB03; capital RESULT |
| WB04 | General mortality ignores the closer lineage measure | **RECORDED:** existing own-lineage arm about +3.53 on v7; cash 0, no new v8 run here | WB04; lineage-mortality RESULT |
| WB05 | Office capital uses pooled government response | **RECORDED:** current-base +0.59 / 0 estimate | WB05 |
| WB08 | BEA's education weight never reached the case | **REFUTED:** 0; weight already in cells, distinct from response | WB08; user-fee adapter |
| WB09 | EL/poverty funding must be added | **RECORDED:** +20.4–30.6 estimate unmeasured; observed district spending already contains grants | WB09; school decision |
| WB10 | B/D eligibility makes all subsidies earned by work | **RECORDED-NEW:** +30–35 not established; alternative entitlement frame is F08 | WB10; pension boundary/CMS trace |
| WB11 | Payable paths must be recomputed after removal | **RECORDED:** sign/size unknown; −32.5 to −34.4 not a derived path | WB11; v6 open probe |
| WB12 | Added people necessarily dilute every national key | **RECORDED:** −8.5 to −14.2 estimate unsupported; fiscal-key question remains W21/WC08 | WB12 |
| WB13, WB14, WB15 | Benefit-tax duplicate; LTSS still uses community MEPS; medical pooling omitted | **REFUTED:** 0 established additional correction in each; relevant removals/replacements already operate | WB13–WB15 callers |
| WB16 | Enterprise key/response must change | **RECORDED:** roughly −5 to −6 / −5.3 estimates, no new elasticity evidence | WB16; v6 rejection 10 |
| WB17 | Missing matched state/function/asset prices | **UNSETTLED:** screen −2 to +6 / −3 to +9, sign and embedded-price overlap unresolved | WB17 geography trace |
| WB18, WB19 | Prison prices ignore custody rates; highway capital still uses resources | **REFUTED:** 0; prison use and VMT keys are active | WB18/WB19 current keys |
| WB20 | Border response should be zero | **RECORDED:** historical −3.11; current 3.3–3.8 downward estimate | WB20; justice arm |
| WB21 | Finite-removal share lags additions | **CONFIRMED-BELOW:** base GPS screen +0.019 / +0.027; full linked effect not rerun | WB21 arithmetic |
| WB22 | Health-capital key should follow uninsured care | **CONFIRMED-BELOW:** +1.4 / +2.1 estimate, net increment unmeasured | WB22; fee/capital offsets |
| WB23 | Pooled medical ratio predates Medi-Cal expansion | **CONFIRMED-BELOW:** +2–4 estimate; 2024-only effect unmeasured | WB23, dated state sources |
| WB24 | Capital transfers/student-loan discharges absent | **RECORDED:** +1–4 estimate under a different account scope | WB24; annual-account boundary |
| WB25 | Synthetic repricing never reaches additions | **REFUTED:** 0 blanket omission; WB21's frozen response is separate | WB25; union/coverage adapters |
| WB26 | Residual state welfare retains a thin WIC key | **RECORDED:** audit benchmark −1 to −2, no new program measurement | WB26 |
| WB27 | Missed people may take up fewer means-tested benefits | **RECORDED-NEW:** stipulated 50% shortfall gives −5.00 / −5.06; no measured shortfall, taxes may offset | WB27 source block |
| WC02, WC05 | Latent children also stay; all admin-labelled coverage costs cancel | **REFUTED:** no supported −3–8 or blanket −2.7–4.8 correction. Actual latent-removal caller operates; national pots are not complete group numerators | WC02/WC05 |
| WC03, WC04 | Items 10/11 not jointly solved; credit term on old 5b basis | **RECORDED:** full interaction unknown. Signed footprint −1.21 / −0.87 and absolute 3.85 / 3.64 are not bounds; stale term +0.33 cannot simply be removed | WC03/WC04; R3-07/R3-18 |
| WC06 | Narrow administrative subcomponents may cancel | **UNSETTLED:** whole-line exposure up to 9.98 / 10.09 is not a correction | WC06 component trace |
| WC07 | Coverage transports item-11 consequences | **RECORDED:** deleting direct parts −0.43 / −0.60; recalibration −0.53 / −0.71, not identified bias | WC07; export_pricing caller |
| WC09 | White C3 blend needs matched geography | **UNSETTLED:** joint +3–5.5 estimate not isolated or signed | WC09 white-profile trace |
| WC10 | Early attriters' descendants inherit selectivity | **RECORDED-NEW:** beta=0.4 screen +3.38 / +3.27 set, +3.42 / +3.32 cash; beta unmeasured | WC10 |
| WC11 | BA+ closure stands in for every fiscal outcome | **RECORDED-NEW:** C3 lower by 0.35 gives +6.01 / +5.82 set, +6.09 / +5.90 cash; fiscal closure unmeasured | WC11 |
| WC12 | Return to Mexican identification/both-parent paths omitted | **RECORDED-NEW:** stipulated r=0.5 screen −7.84 / −9.05 set, −6.73 / −7.93 cash; r not estimated | WC12 |
| WC13 | Nonreporter anchor also inherits undercoverage | **RECORDED:** frozen-ratio +1.07 / +1.34 set, +0.80 / +1.08 cash; joint origin/count refit needed | WC13 |
| WC14 | Non-Mexican reporters are necessarily non-Hispanic | **CONFIRMED premise failure; text corrected, no item.** Later own-age/sex minor proxy +0.20 / +0.22 set/cash stays beside; latent-adult transport unidentified | WC14; L2 origin diagnostic |
| WC15, WC16 | All-age child transport; broader reporters excluded | **RECORDED arms:** incremental +1.05 / +1.53 and +2.67 / +3.00 set; +0.68 / +1.16 and +2.40 / +2.73 cash. Full alternative totals overstate remaining increments | WC15/WC16 |
| WC17, WC18 | Children missed by parent-origin rule; linked-parent birthplace conflict | **CONFIRMED-BELOW:** conditional set +0.28 / +0.30 and +0.90 / +0.96, cash +0.28 / +0.30 and +0.89 / +0.95. Birthplace/data-quality reconciliation still needed | WC17/WC18 |
| WC19 | Residual added people lack non-federal survivor transport | **CONFIRMED-BELOW:** G3-only extension screen +0.72 both ends/sets; other components unmeasured | WC19 |
| WC20 | Missed G1 status/earnings differ | **RECORDED:** +1–3 estimate, sign unknown after benefits and receipts | WC20; C4 record |
| WC21 | Missed children's complex-household profiles differ within age/sex cells | **UNSETTLED beyond item 17's tenure sensitivity:** no identified signed price correction for the broader profile | WC21; L2 fixed-profile limits |
| WC22 | Post-engine adapters obscure contracts | **RECORDED:** no standalone dollar effect; concrete mechanisms are the other WC rows | WC22; R3-22 |

WA-PACKET, WB-PACKET and WC-PACKET are presentation findings, with no demonstrated headline change. The receipts
table used the v7 base and omitted responsive/source-part labels; the spending table omitted $45.47 / $47.12bn
already carried in completion/coverage spending and confused split shares with responses. The counting packet
mixed historical ages/coverage epochs with the active case. Missing display rows were not missing engine amounts.
[SOURCE: each verifier's PACKET row and closure checks]

### U1: distribution, households and uncertainty

All these are companion findings; none changes the headline. IDs are prefixed U1 to distinguish them from U2.
Dollar sizes are $bn; share movements are percentage points (pp). A confirmed distinction can be correctly labelled
in the current producer and still require correction when summarized.

| ID | Claim | Disposition, size and corrected reading | Evidence anchor |
|---|---|---|---|
| U1-D1 | Financing determines regressivity | **CONFIRMED:** central Q1 charge rises 68.29 under a→b; this is stipulated financing, aggregate change 0 | U1 D1, current quintiles |
| U1-D2 | Fiscal row is a current cash bill | **CONFIRMED distinction:** that reading overstates current financing by 123.74 / 149.15; capital/accrual remain separate | U1 D2, financing bridge |
| U1-D3, U1-D4, U1-D6 | Capital must mean congestion; production denominator invalid; winners contradict stationary financing | **REFUTED:** no demonstrated amount error; opportunity cost, pinned production and current stationary rule traced | U1 D3/D4/D6 |
| U1-D5 | National tax mix substitutes for level-matched financing | **CONFIRMED sensitivity:** Q5 costs fall 24.04 / 27.29 set, 29.33 / 32.58 cash-style. Aggregate 0; source-level residual prevents treating it as a corrected point | U1 D5; native tax-mix probe |
| U1-D7 | Outside-budget channels retain old population | **CONFIRMED-BELOW:** proportional stress about +3.5 central; not a measured population correction | U1 D7 |
| U1-H1 | Flat item-11 placement identifies household incidence | **UNSETTLED:** redistribution changes aggregate 0; contributor-share sign/size unidentified. Deletion effect 0.52 / 0.58pp is not a reassignment bound | U1 H1 |
| U1-H2 | Located shares describe the whole lineage | **CONFIRMED boundary:** whole-population personal bounds 17.85–22.18% / 14.36–18.69% set; 26.05–30.38% / 22.80–27.13% cash | U1 H2, population arithmetic |
| U1-H3 | Contributor shares are basis-independent | **CONFIRMED:** cash personal shares higher by 8.57 / 8.82pp; shared by 8.04 / 8.40pp | U1 H3 |
| U1-H4 | Member shares equal household or full-family balances | **CONFIRMED distinction:** household-minus-member 7.73 / 6.94pp set, 9.32 / 9.01pp cash; nonmember accounts are absent | U1 H4 |
| U1-H5 | Personal/shared contrast changes attribution alone | **CONFIRMED:** set shares +2.07 / +1.78pp; item-11 exclusion contributes about 0.52 / 0.58pp in the earlier comparison | U1 H5 |
| U1-H6 | Identifying donors identify nonreporters' household placement | **UNSETTLED:** assumed 10–15pp donor difference yields only 0.70–1.05pp overall; actual difference unmeasured | U1 H6 |
| U1-H7 | Original children with newly classified parents retain old routing | **CONFIRMED-BELOW:** six records, 13,312 weighted people; no demonstrated material share change | U1 H7 |
| U1-H8 | Displayed parent paragraph switches accrual arm | **CONFIRMED-BELOW:** flat→onbooks +0.64 / +1.05pp | U1 H8 |
| U1-H9 | School allocation can move contributor shares materially | **CONFIRMED existing arm:** personal per-head allocation lowers shares 4.90 / 4.36pp set, 4.26 / 4.80pp cash | U1 H9, current school rows |
| U1-H10 | First-order credit/service keys identify dependent incidence | **UNSETTLED:** aggregate 0 under redistribution; threshold effect unsized | U1 H10 |
| U1-H11, U1-H12, U1-H13 | Weight scaling creates physical members; shared exclusion violates rule; upstream item 11 never computed | **REFUTED:** statistical weights do not rerun thresholds; shared companion deliberately excludes item 11; upstream solve exists | U1 H11–H13 |
| U1-U1 | Conditional interval includes all uncertainty | **CONFIRMED distinction:** represented positive-covariance envelope widens edges −16.59 / +16.68; count arms+C3 −15.41 / +17.92. Central C3 alone only −1.47 / +1.42 | U1 U1, stored intervals |
| U1-U2 | Sampling still dominates specification spread | **CONFIRMED reversal if old claim reused:** span 90.19 versus conditional sampling width 43.67–44.86; current source marks old verdict historical | U1 U2 |
| U1-U3 | Model-range quadrature supplies missing confidence limits | **RECORDED-NEW:** school arm −32.12 / −29.26 demonstrates material model choice; pseudo −21 / +10 edge extension is not a CI | U1 U3 |
| U1-U4 | Joint pooled-medical translator uncertainty omitted | **UNSETTLED:** replacement stress widens edges 2.90 / 2.97; independent-append stress 4.98 / 5.09 is unjustified with shared donors | U1 U4 |
| U1-U5 | Base education sampling error missing | **CONFIRMED-BELOW:** hypothetical independent SE 2.4 widens edges about 0.49 / 0.50; existing correction SE already included | U1 U5 |
| U1-U6 | Endpoint-vector transport cannot change interior envelope | **UNSETTLED:** native endpoints unchanged; revalued interiors could cross, effect unsized | U1 U6 |
| U1-U7 | Scalar PES shock measures age/sex covariance | **UNSETTLED:** current scalar SE 1.02 / 1.42 set, 0.57 / 0.98 cash; replacing its shape can widen or narrow | U1 U7 |
| U1-U8 | Cash-basis propagated interval exists | **CONFIRMED-BELOW absence:** generic pension-key sensitivity shifts set edges about 2.15 / 2.10; it is not a cash CI | U1 U8 |
| U1-U9 | Hash reconstruction bypasses integrity | **REFUTED:** exact native replay/schema/cache/economic-parity gates operate, otherwise blocked | U1 U9 |
| U1-U10 | Blocked uncertainty branches invalidate current conditional result | **RECORDED:** no current interval delta; unexecuted branches are not live results | U1 U10 |
| U1-PACKET | Old distribution checkpoint is live drift | **PACKET:** old displayed endpoints differ 3.20 / 3.22; live outputs reconcile, current error 0 | U1 PACKET |

The companion corrections are therefore about financing, basis, denominator, allocation and uncertainty scope.
They do not turn redistribution into a headline correction or a conditional envelope into an unconditional CI.
H1/H6/H10 and U4/U6/U7 remain unmeasured, with the required probes named in the verifier. [SOURCE: U1]

### U2: stocks and comparisons

U2 used committed dispatch snapshot `c2249ce8` because comparator peers were editing their lanes. Its figures
establish the stated vintage's claims; F's later comparator snapshot is separate. Stocks, annual interest,
current cash and annual removal costs are not interchangeable.

| ID | Claim | Disposition, size and corrected reading | Evidence anchor |
|---|---|---|---|
| U2-D1 | Federal current cash is a cost at every corner | **CONFIRMED claim reversal:** low-payer −9.43 / +29.62; central +21.61 / +60.80. Headline change 0 | U2 D1, committed source-part sum |
| U2-D2 | Classified cash measures borrowing | **RECORDED boundary:** identified all-government cash 229.73 / 290.97, unlocated 2.95 / 6.91; Treasury bridge absent | U2 D2 |
| U2-C1 | Closed result lies between headline and smaller deficit-sharing limit | **CONFIRMED false ordering:** limit-minus-central +63.77 / −48.17; limit is an account extrapolation, not actual federal deficit closure | U2 C1 |
| U2-C2 | Cash future OASI cuts need a second group credit | **UNSETTLED:** roughly −13.6 to −14.0 at each end under today's share, not a measured future-benefit share; set unchanged | U2 C2, time-interpretation distinction |
| U2-C3 | Mixed/coverage residual baskets are omitted | **RECORDED:** category arm difference up to −8.89 in archived receipt; household central already has offset | U2 C3 |
| U2-C4, U2-C5, U2-C6 | Coverage placement; national denominator; national-fix offset exceeds low federal cash | **RECORDED:** placement unsized; omissions-only +0.15 household / +0.26 per-person scenarios; 12.19 excess offset is sharing, not repayment of own borrowing | U2 C4–C6 |
| U2-P1 | Pension coverage enters divisor only | **REFUTED:** service numerator now attributed | U2 P1 |
| U2-P2 | Static service intensity/vintage choices | **RECORDED arms:** simple stock +102.54 / +107.78, interest +5.07 / +5.30; increments stock −66.68 / −70.50, interest −3.25 / −3.42; historical bias unidentified | U2 P2 |
| U2-P3 | Military pensions must respond | **RECORDED alternative:** all-average stock +313.94 / +290.29, interest +12.78 / +11.73; changes more than military | U2 P3 |
| U2-P4 | Absolute pension stock equals comparator excess | **RECORDED distinction:** absolute 484.13 / 507.78; rough-minus-white 118.55 / 112.94, interest 6.18 / 5.94 | U2 P4 |
| U2-L1 | Current v8 historical stock exists | **RECORDED absence:** no identified stock; annual diagnostic is not one | U2 L1 |
| U2-L2 | Capitalized accrual is observed debt | **RECORDED hypothetical:** cash switch changes historical interest gap −61.10 and stock −1,889.78 at both ends; distinct bases | U2 L2 |
| U2-L3 | Benefit-series carry differs from payroll carry | **RECORDED arm:** payroll-minus-benefit interest −8.93, stock −276.19 at both ends; cash unaffected | U2 L3 |
| U2-L4 | White benefit accrual is negative from retiree drawdown | **REFUTED:** SS accrual +155.07; cited negatives are net federal balances | U2 L4 |
| U2-L5, U2-L6 | Historical comparator asymmetry; second annual white gap | **RECORDED:** historical rules declared; base-minus-central +11.75 / +8.34 set is a different specification, not duplicate estimates | U2 L5/L6 |
| U2-L7 | Monkey-patched imported function hides a wrong number | **CONFIRMED-BELOW caller hazard:** no demonstrated numerical error | U2 L7 |
| U2-L8 | All-NH-white ACS path proxies third-plus whites | **RECORDED:** path difference 0.36%; true third-plus bias unmeasured | U2 L8 |
| U2-I1 | Indian social/full account unavailable | **RECORDED stop:** fiscal −118.78 / −95.12 set, −148.3 / −124.7 cash; no current combined total | U2 I1 |
| U2-I2 | Indian top tail is omitted | **REFUTED:** central already credits 12.35 versus CPS-only; proportional tail only −3.58 further | U2 I2 |
| U2-I3 | Own Indian mortality missing | **RECORDED gap:** direction to test is higher set accrual; size unknown, cash unaffected. NH-Asian tables are not Indian-specific | U2 I3 |
| U2-I4 | Indian benefit jump proves error | **RECORDED migration:** v4→v8 set −45.79 / −30.46, cash −45.03 / −29.70; source-tax item 9 alone +5.92 / +2.19 | U2 I4 |
| U2-I5 | Union-at-white-ages adjustment is spurious | **RECORDED traced diagnostic:** same identified count changes −5.64 / −6.38; cannot subtract full-lineage rows | U2 I5 |
| U2-I6 | Indian item 11 is measured zero | **UNSETTLED:** intentionally unmeasured, numerical 0; sign/size unknown at both ends/bases | U2 I6 |
| U2-I7, U2-I8 | Indian G1+G2 equals full lineage; justice reference stale | **RECORDED:** boundaries differ; reference already corrected −3.20 / −3.22, not a new correction | U2 I7/I8 |
| U2-A1 | Late-arrival slice identifies admission/lifetime effect | **RECORDED boundary:** slice 3.10 / 3.72 set, 4.54 / 5.16 cash; no adult-18–49 result | U2 A1 |
| U2-A2 | Late-arriving seniors always cost less | **CONFIRMED basis reversal:** set +$3,068 / +$2,957 per head versus earlier arrivals, cash −$880 / −$995; matched descriptive comparison | U2 A2 |
| U2-A3, U2-A4 | Flat adult justice/school allocation; arrival-age coverage placement | **RECORDED approximations:** no new measured correction or sign; old $2,549 schooling illustration is not current personal cost | U2 A3/A4 |
| U2-A5 | Convention/grouping changes late-arrival slice | **CONFIRMED-BELOW:** b−a +1.28 / +1.35 set, +1.29 / +1.36 cash | U2 A5 |
| U2-A6 | Senior medical coverage edits need repricing | **RECORDED:** historical −0.18 set / −0.31 cash proposal; no new v8 amount | U2 A6 |
| U2-X1 | Federal financing and pension legacy can be summed | **RECORDED non-additivity:** exact overlap unmeasured; 24–25 interest total is not an overlap bound | U2 X1 |
| U2-X2, U2-X3 | Legacy interest already inside main case; whole closed-budget/debt amount duplicated | **REFUTED:** main interest response 0; closed budget has a negative national-fix credit. Joint-path bridge still required | U2 X2/X3 |
| U2-X4 | Indian combined, Mexican fiscal, slices and stocks can be added | **RECORDED boundaries:** combined Indian withheld, late slice already included, closed account replaces headline, stocks not flows | U2 X4 |
| U2-PACKET | Excerpts establish current government scope/completion/age claims | **PACKET:** federal label overstates by 208.12 / 230.17, national offset −33.81 each end; live arithmetic unchanged | U2 PACKET |

### F: frame and explanatory claims

The parent kept **no new headline correction** from F. F01's literal tax/service-use decomposition label is wrong
and is fixed in v9's docs. The factors include earned pension spending, mixed-unit effects and assigned population
additions. Reclassifying them changes the explanation, not the total. F09 becomes a build in the social lane on v9:
the joint figure compared with equal-count average residents under matched rules. It is a comparison beside the
absolute account. F27, financing excess burden, went to the operator as an ask. [SOURCE: parent's dispositions; F]

| ID | Claim | Final disposition and size | Evidence anchor |
|---|---|---|---|
| F01 | Literal same-age tax/use split | **Docs fix, headline 0:** set population contributions +13.37 / +11.91 assigned to use, and −43.55 pension spending inside receipt factor | F01 source-factor trace |
| F02 | Shapley order dependence hidden | **RECORDED:** set age spans 57.99–121.22 / 51.40–110.74; six orders already exported, total unchanged | F02 |
| F03 | Cash label implies all benefits/payments are cash | **RECORDED boundary:** pension switch −84.04 both ends; capital 39.07 / 64.31 and employee accrual remain | F03 |
| F04 | First-year response read as next-year cash saving | **Wording fix:** 294.38 / 351.75 set versus 210.34 / 267.71 pension-cash, not a new cash-flow estimate | F04 |
| F05 | Whole people violate fractional-ancestry conservation | **RECORDED operator frame:** selected fractional envelope lower by 127.45 / 89.75 set, 103.81 / 75.21 cash; alternative question | F05 |
| F06 | Youth/accrual comparison establishes omitted future taxes | **RECORDED-NEW:** cash switch changes excess by −106.74 and age attribution by −94.03 at both ends; missing tax receipt not proved | F06 |
| F07 | Replacement footnote covers only added descendants | **Wording fix:** broader scope unpriced; old footnote −6.91 / −10.56 is not all-lineage correction | F07 |
| F08 | Broader B/D entitlement account required | **Alternative, not omission:** net companion unmeasured; +20–40 review estimate unsupported | F08; WB10 |
| F09 | Joint figure lacks matched average-resident comparison | **Build in social lane at v9:** live comparison unmeasured by this review; historical PM-only −116.19 is not its total | F09 |
| F10 | Fiscal excess plus absolute social is incoherent | **Discarded under echo rule; premise refuted:** both compare presence with absence, headline 0 | F10 |
| F11 | Black comparison lacks equal-count/own-coverage symmetry | **RECORDED, already available:** later committed equal-minus-own gap +14.43 / +17.09 set, +14.51 / +17.16 cash, not headline changes | F11, later committed snapshot |
| F12 | White comparison identifies causal ancestry/replacement | **RECORDED boundary:** old white-minus-average 149.2 / 146.1 is benchmark change; age-standardized companion exists | F12 |
| F13 | Fractional companion is point-identified | **RECORDED bounds:** G3 ancestry share 0.30458–0.66650; missing grandparents explicitly bounded | F13 |
| F14 | Ancestry weights removal-only item 11 | **Wording fix:** national allocation not reconciled; deleting weighted delta gives −2.62 / −9.86 selected-envelope exposure, not a proven repair | F14 |
| F15 | B64 “static throughout” justifies fixed families | **Record new argument:** fixed families coexist with adjustable capital; item-11 exposure 10.74 / 14.53 does not price rematching | F15 |
| F16 | M5 equal-split arm newly removes 11.02 | **RECORDED:** actual direct switch −5.51 both ends, holding coverage; no doubled swing | F16 |
| F17 | Rematching cuts item 11 by 6–10 | **RECORDED:** estimate uncomputed, actual sign unknown | F17 |
| F18 | Spousal pensions should automatically enter | **RECORDED:** one direction +2.75 set, 0 cash; 0–13.9 proxy range not a net bound | F18 |
| F19 | First-year keeps full long-run corporate credit | **REFUTED:** no supported +18–38 correction; first-year response already applied | F19 |
| F20 | Combined social scope needs private-return/7% rate | **Record new argument:** stored 7% fiscal arm +95.44 / +83.74 set, already beside; no new adoption evidence | F20; capital source trace |
| F21 | Immobile rents invalidate low corporate response | **RECORDED arm:** normal-only +26.23 / 0 before explicit coverage repricing; immobile-rent fraction unmeasured | F21 |
| F22 | Tight 2024 cycle proves downward structural bias | **Discarded under echo rule:** old modeled +17.4–27.0 or +22.5–35.0 are not live corrections | F22 |
| F23 | Endpoints are full uncertainty bounds | **RECORDED boundary:** coverage alternatives −25.22 / −29.52 or +12.42 / +12.47 set, beside; not a CI | F23 |
| F24 | Full school response must change | **RECORDED:** within-district arm −30.37 / −27.87 both sets; no new causal evidence | F24 |
| F25 | First-year school dilution absent | **RECORDED:** historical 45–58 potential burden, not measured v8 endpoints | F25 |
| F26 | Flat VSL is erroneous relative to life-years | **RECORDED choice:** 0% life-year arm −46.95 / −45.23 in joint figure, already beside | F26 |
| F27 | Financing distortions omitted | **Operator ask:** assumed m=0.25 on current cash base gives +60.49 / +76.79 before overlap; m=0 gives 0. No measured preferred value | F27 |
| F28 | E07 calls imputed capital return current tax/borrowing finance | **Record new argument:** rationale conflicts with boundary; exposure 39.07 / 64.31, current social financing excludes it, no verified numeric failure | F28 |
| F29 | Displaced aid necessarily means public budget saving | **Wording fix:** housing exclusion stress +0.24 both ends; broad screen +0.96; public-consumption mirror has no rental-transfer bug | F29 |
| F30 | Public land omitted | **RECORDED:** inherited later-key 10% screen +3.66 / +6.02, not a measured full-v8 own-price correction | F30 |
| F31 | Government-average PM and omitted investment emissions identified | **Wording fix:** exposed mirror +9.50 / +10.12; alternative intensity/investment effect unmeasured | F31 |
| F32 | Traffic-share parameter stale | **RECORDED:** +0.9–1.3 estimate at affected social ends, cash not run | F32 |
| F33 | Cash-PCE alternative | **RECORDED:** −2 to −3 estimate, end split unpriced | F33 |
| F34 | Government-paid health overlaps PCE | **RECORDED unverified:** +2–3 suggestion, needs primary reconciliation | F34 |
| F35 | Fear valuation includes justice spending | **RECORDED unverified:** −1–3 suggestion, no new source quotation | F35 |
| F36 | Items 10/11 not jointly solved | **RECORDED:** footprint −1.21 / −0.87; absolute 3.85 / 3.64 is not a nonlinear bound | F36; WC03 |
| F37 | Re-spending/public mirror still one-sided | **RECORDED, repaired:** both central; removing both raises social +2.86 / +5.58, fiscal unchanged | F37 |
| F38 | Services/complementarity gross estimates are additive offsets | **RECORDED:** live net unsized; 21.8 and 26.8–80.4 not reconciled additive amounts | F38 |
| F39 | Co-resident ages identify independent adults' ages | **RECORDED limitation:** no new evidence against age-mix ruling; net effect unknown | F39 |
| F40 | Old paragraphs above dated corrections are live errors | **RECORDED history:** old difference 3.20 / 3.22, current outputs unchanged | F40 |
| F41 | Post-engine design proves closure failure | **RECORDED:** no standalone total error; F01/F14 are concrete consequences | F41 |
| F-PACKET (PACKET-2 included) | Stale comparator snapshot, reversed endpoint pairing, cash/causal labels and infinity/no-native-loss premise | **Wording fixes, headline 0:** pair excess at specs 16/11, do not sort into an unproved range; ε=∞ does not imply zero native wage losses | F PACKET, source nest and snapshot checks |

### Anchoring incident and convergence

F's first packet carried the parent's own candidate list. The F-blind packet was built and run after that was
noticed. The echo rule was applied: a finding matching a parent candidate counts only if the blind arm finds it
or it supplies new evidence. F10 and F22 were discarded under that rule. F01's source-label failure, F09's matched
comparison and the blind financing/rationale arguments survive on their stated evidence. Blinding the header
does not make the shared body, scout-fed reviews or model-family outputs independent. [SOURCE: F, anchored/blind
comparison and parent dispositions]

Round 5 therefore rejects convergence. Material findings became measured v9 items; smaller measured refinements
and companion-claim corrections were retained with their limits. A checked lane and a candidate case do not
establish that the whole revised case has converged. Its review remains open. [SOURCE: parent's dispositions;
CALCULATION: measured lanes above; INFERENCE: convergence status]
