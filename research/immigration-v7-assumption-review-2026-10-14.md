# Assumption review of main case v7, 2026-10-14

[2026-10-15: rounds 2–4 are under "Later rounds" below; the case converged at round 3.]

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
