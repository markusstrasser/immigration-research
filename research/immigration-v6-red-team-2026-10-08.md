# Outside red team of main case v6 and its docs, 2026-10-08

**Verdict:** No finding moves the headline. The case stays at $389.1–461.5bn. Four claims in the docs were
stronger than their evidence and are corrected:
- FAQ 19's "count it twice" defense of whole-person counting was false.
- FAQ 14 read an occupation-overlap sketch as an estimate of the production elasticity, and carried an earlier
  case's sensitivity to v6 without a replay.
- FAQ 11 read Lee and Scafidi's long differences as an adjustment path.
- FAQ 17's sign claim was unscoped.

One fail-open path in the payload consumer is closed (a4daa2ca). Every other attack is already answered by a FAQ
entry, a ladder entry or a decision, or falls below the bar, and the review gave no reason to reopen it.

## What ran

- **Bar** (set before dispatch, 2026-10-08 00:19 JST): a finding counts only if it plausibly moves the headline by
  $10bn or more, flips a stated qualitative claim, or invalidates a method.
- **Two packets** (critique skill, `model-review.py`, preset cross4, each with a repo-reading premise scout):
  - A: the v6 decision, the main-case RESULT through its arms, the INDEX headline section and the ladder's live
    entries (first 160 characters each), 101 KB.
  - B: the v6 decision and the objections FAQ, 94 KB, both on the working tree after the item-T pass.
- **Axes:** two on GPT-6 Astra (correctness, contracts; subscription) and two on Gemini 3.8 Flash (structure, gaps;
  paid API).
- **Tokens:**
  - Gemini: prompt 31–36k, output 2.8–3.2k and reasoning 3.4–23.7k per axis.
  - The subscription transport records no usage for the GPT axes.
  - Scouts (GPT-6 Astra, low effort): 607k and 697k input, mostly cached; 3.0k and 5.2k output.
- **Findings:** 22 extracted from A and 35 from B, after deduplication.
- **Artifacts:** ignored and kept locally under `.model-review/2026-10-08-v6-red-team-*` (coverage.json,
  findings.json, every axis output).

## Acted on

| Finding | Axes | Check | Change |
|---|---|---|---|
| FAQ 19: an ancestry share "would count it twice" because a mixed person's other ancestry already lowers their measured cost | B: all four | A member's measured cost and the share of it attributed to an origin are separate quantities. Half shares of a $6,000 member give $3,000 + $3,000, and nothing is counted twice. Confirmed. | FAQ 19 now says the readings answer different questions: whole people asks what the members who exist cost others; the share is the allocation to use when origin accounts must add to a national total. Dated correction in decision 2026-10-05 (alternative 2 carried the same argument). |
| FAQ 14: "the jobs put that elasticity near 6" | B: three | The memo's harmonic sketch chooses both component elasticities and measures only the overlap, 0.644 (`immigration-production-term-nativity-nest-2026-09-22.md:175–198`). Confirmed. | The direct estimates (8.7, 17.9) and the meta-analysis (8.2 national, 16.9 regional) carry the conclusion; the sketch is called an illustration. Also changed in the INDEX at L167, L427 and L570. |
| FAQ 14: the ε = 3 shift "carries to the adopted one" | B: two | It was computed on the September 20 band and never replayed on v6. Confirmed. | The FAQ now says it was not replayed. |
| FAQ 11: "twenty years after enrollment falls, districts still keep about 70% of the money" | B: GPT correctness; both Gemini axes on a related point | The paper estimates 20-year long differences across districts by OLS, with no district, state or year effects (`immigration-recent-papers-2026-10-06.md:93–98`). Confirmed: an association, not a tracked path. | Restated as long differences, also in the literature memo. That budgets shrink slowly stands; the timing claim is gone. |
| FAQ 17: "No combination changes the sign" | B: GPT correctness | The sentence follows the outer range of corrections and components; FAQ 2's frozen-services row runs from −$60.8bn to +$44.3bn and does change the sign. Confirmed as a scoping gap. | Scoped to the combinations it moved, with a pointer to entry 2. |
| The payload consumer returns zero capital when `meta.capital_return` is missing | A: GPT correctness, Gemini structure | The probe reproduced it. A v6 payload stripped of its capital block, or with an empty component list, gave $352.5–400.4bn and kept its adopted-v6 stamp. Confirmed. The stored payload is complete, so the headline was never affected. | a4daa2ca: a payload stamped as adopted on or after 2026-09-27 now stops `[BLOCKED]` without capital components. Generation payloads and earlier cases are unaffected; the v6 lane reruns IDENTICAL 27/27. |

## Rejected

These are grouped by attack. Each group ends with the entry that answers it and the reason the review gave no
grounds to reopen it.

1. **The capital return double-counts depreciation** (A1, A14, A18; B8, B17).
   - NIPA government consumption charges depreciation and no return on the money tied up. The case adds a 2–3% net
     return, and the two together are the user cost of capital (decision 2026-09-27, alternative 1;
     `capital_return_services_2026_09_27/RESULT.md` §5).
   - Gemini's own fix, operating cost − depreciation + (r + δ)K, reduces to operating cost + rK, which is the case.
   - Whether an imputed return belongs in a budget account was the operator's call: "it's the honest value of the
     thing", 2026-09-27. The cash set is beside.
   - The private side's capital deepening is the production term's: capital is paid its rental rate and adjusts
     (FAQ 4).
2. **Accrual pensions against a cash federal budget, and closing the budget** (A5, A8; B10, B11, B13, B35).
   - Both follow current law. Trust funds cannot borrow, so payable benefits; the general fund can, and current law
     schedules no closure (FAQ 20, ladder 282, memory `immigration-current-law-first`).
   - The closed-budget arm, $357.1–429.5bn, and the cash set, $307.4–385.4bn, are stated beside the headline.
3. **Whole people against ancestry shares, mixed parentage and replacement children** (A6, A9; B6, B14, B23, B31,
   B34).
   - The frame is the operator's (decision 2026-10-05). The ancestry share, $274.9–374.8bn, and full replacement,
     $383.4–450.7bn on v5, are stated.
   - What changed is the argument for whole people, above. The reviewers' point that whole-person accounts by origin
     overlap is now said in FAQ 19.
4. **Schools charged at full cost against stickiness on the way down** (B2, B12, B25).
   - The case's response is the stationary relation across districts: 1.004 scaling, with 0.836 within districts on
     the low side.
   - Lee and Scafidi's decline side describes a transition. FAQ 11 keeps the stationary comparison apart from the
     savings of an actual removal, and the first-year budget response ($289–336bn) is stated.
   - The reviewers' $42–99bn is that transition reading.
5. **The 1.09M fourth-plus attriters priced from co-resident adults** (A3).
   - The comparison is symmetric: fourth-plus adults are measured against co-resident whites
     (`generation_carryover_2026_09_27/RESULT.md`, the co-residence row).
   - The direct measure is noisy (c = −0.86, SE 1.28). Its plausible alternative, later losses converging like
     third-generation attriters, is $3.8–5.0bn on v5 (decision 2026-10-07, alternative 6), below the bar.
   - The reviewer's $10–15bn needs fourth-plus attriters at full parity with whites, which nothing measures.
6. **Adult convergence applied to children** (B15).
   - The blend weights age-specific profiles: 44% of an identified third-plus member's cost plus 56% of a third-plus
     white's at the same age (FAQ 19). A child takes children's costs from both, so no adult tax key is charged to
     a minor.
   - That the weight comes from adults is a stated assumption (ladder 280).
7. **General services from cross-state scaling** (B9).
   - FAQ 2 states the one within-state test, 0.47 (95% interval −0.72 to 1.66), beside the cross-state rates of
     0.59–0.84 that the finite removal turns into the case's 0.60–0.85 (decisions 2026-09-23 and 2026-09-26). The
     review added nothing to either.
8. **Below the bar or already recorded:**
   - the residual on the attriters' income-tax keys, about $2bn (A13; ladder 298);
   - Pell keyed through the education line, $0.1bn (B28);
   - stale presentation layers (B24): the map is on v6 at the operator's request, and the explorer and figures page
     are pinned by design;
   - property-tax incidence and municipal distress (A15; B32): the long-run property-tax response is ladder 253;
   - remittances in the sales-tax base (A22): ladder 90, under $10bn by the reviewer's own figure;
   - school debt service (A17): the interest row responds at 0, and the capital-return lane's §5 gates the overlap;
   - legacy debt and pensions (B18): debt_legacy and public_pension_legacy are stated beside, not removed with the
     group.
9. **Untested, with no defect shown:**
   - independent replication of the actuarial inputs and direct validation of the non-identifiers' fiscal profiles
     (A12, A20, A21; B29). The detection threshold on the 3.04M added people is $3,289 a person for $10bn;
   - general-equilibrium tax feedback (A10, A19; B27): the production term is the account's GE term, and its nest
     sensitivity is FAQ 14's;
   - caller coverage, consumer schemas and the oct05/oct07 joins (A11, A16; B26, B33): `api_check.cjs` runs 99
     API checks, and the v4 consumer the case imports is now fail-loud on capital;
   - carrier lines as an architecture smell (A14): an engine refactor, not a number;
   - the broader elasticity distribution (B16): the meta-analysis is cited;
   - population absence conflated with an actionable removal policy (B30): FAQ 11.
10. **Parameter stacking** (A7). Each fork was chosen on its own record, and its alternative is stated beside the
    headline. The review named no fork whose choice was wrong.

## Revisions

- 2026-10-08: written after the review. Concept affected: the defense of whole-person counting; the evidence on the
  production elasticity; school-budget timing; FAQ 17's sign claim; the payload consumer's capital guard.
