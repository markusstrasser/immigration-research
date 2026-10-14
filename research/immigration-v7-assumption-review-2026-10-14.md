# Assumption review of main case v7, 2026-10-14

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
- **S04** (the pairing's low end uses $334.8bn silently): §7 of the real-costs memo and the FAQ's "Before combining"
  say so.
- **S05** (all Hispanic victims treated as Mexican-origin): `victim_cost.py:435–458` splits Hispanic victims by the
  Mexican share of the group's tract-level exposure; "all in-group" is the labelled lower-bound arm.
- **S11** (progressive taxes on the wage shift go uncredited): `distribute.py` taxes each skill cell's wage change at
  the nest's rates (0.384 / 0.426), and gates after-tax wages to P and the taxes to the induced receipts the fiscal
  account credits (lines 586, 1120).
- **S18, S52** (PM2.5 traffic refill): refill needs fixed roads, which the case's long-run road response rules out;
  binding caps are checked in the lane.
