# HUMAN.md — what needs you (autonomous-run escalation)

The loop's non-blocking human-outbox. Items here need an operator action or decision that an
autonomous run cannot resolve itself. Newest first.

## 2026-06-25 — after the 5-domain frontier research+acquisition pass

Completed autonomously: a parallel scout of all 5 named domains (sociology / urbanism / policy /
economics-disconfirmers / crime), all integrated, all load-bearing citations primary-verified.
Map + synthesis: `research/immigration-research-coverage-matrix-2026-06-25.md`; confidence ladder
gained entries 44-50. **Honest bound: the literature search is now largely exhausted — economics +
crime saturated, sociology near-harvested, policy gap filled. The live frontier is urbanism, where
the bottleneck is a BUILD, not more search.** Three things for you:

### A. MSA rent panel — BOTH legs BUILT, no API key needed. ~~Census key~~ resolved.
**Done this session (no operator action needed):** the full panel, reproducibly, with **zero API key**.
- **Supply leg** (`build_msa_rent_elasticity_panel.py`, `msa_rent_elasticity_panel`): Zillow×Saiz, 168 metros. Bivariate elasticity↔rent-growth is NULL (−0.034) — supply elasticity moderates a demand shock, doesn't drive growth alone.
- **Demand treatment** (`build_msa_fb_rent_panel.py`, `msa_fb_rent_panel`): the Census API key turned out **unnecessary** — the bulk **ACS 2023 summary-file tables are key-free** (B05002 fb-share + B25064 rent by CBSA, joined via the no-key Census gazetteer). Pointed there by the operator ("use the corpus data"). Reproducible: `setup-urban-housing.sh` auto-fetches Zillow + ACS + gazetteer (verified by a remove-and-re-fetch test).
- **Result:** corr(fb-share, rent LEVEL) = **+0.69** (immigrants concentrate in high-rent metros; **+0.74 in inelastic metros** — the Wilson-Zhou incidence mechanism), but corr(fb-share, rent GROWTH) = **−0.17** (didn't drive recent growth). **Honest bound:** the level corr is **sorting-confounded** (immigrants choose expensive/inelastic metros — Borjas critique), NOT causal.
- **Remaining (autonomous, no key — flag if you want it):** the causal `Δrent ~ Δfb-share × elasticity` (Wilson-Zhou +2.2%/+1.4%) needs a **2nd ACS year** (another no-key `acsdt1yYYYY-b05002.dat`) + a shift-share IV. I can build this without you; say the word.

- 2026-09-22: the descriptive leg is executed in `housing_supply_ca_tx_2026_09_22` (ladder 180, memo `immigration-housing-supply-ca-tx-2026-09-22.md`): Δ Mexican-origin share 2010→2023 associates with 2015–2026 rent growth within state (+0.030 log points per point), the share × inverse-elasticity interaction is not separately identified, and the state permit and 2024 native-migration cuts are in. The causal `Δrent ~ Δshare × elasticity` leg stays open and is only identifiable on 2000–2010 (ladder 136/140); it is a separate build, not started. — session 87fa457f
- 2026-09-22 (evening): the causal leg is executed too, `housing_causal_2000_2010_2026_09_22` (ladder 183): 2000–2010, ancestry-prediction IV (ladder 182), rents +1.4% (SE 1.4) and values +11.6% (2.9) per point of foreign-born share, no inelastic-metro amplification on 223 Saiz-matched metros. The 'Remaining' shift-share item above is closed; what is still open is the Mexican-born version (needs a 2000 metro endpoint) and native migration by education. session: eb198c12

### B. Gated pulls that unblock the deepest tests (login-gated, you pull; loaders/specs ready)
- **IPUMS-CPS** 2nd-gen extract → cluster-V V02 (loader `load_cps_second_gen.py` ready; uses PARENTAL
  birthplace, so it's already robust to the ethnic-attrition bias the sociology pass flagged).
  consumed: 2026-09-29 — the same ask is repeated in the 2026-06-25 section below; its receipt (2026-09-22, extract staged, loader fixed in 1e62ca2) covers this one — session 95a94bd8
- **openICPSR 120490** (Abramitzky mobility) → also the econ-disconfirmer pre-reg P2.
- **WRLURI2018 + Geocorr2022 PUMA↔CBSA crosswalk** (one-time DL / on-demand generator) → the full urban
  panel beyond the 1/10 cut. Exact pointers + Geocorr query spec in `setup-urban-housing.sh` MANUAL_ACQUIRE.md.
  consumed: 2026-09-29 Geocorr — the 2022 PUMA allocation factors are held (lane `displacement_transfers_2026_09_18`; register, "Housing, labor and local economy"); WRLURI 2018 deferred: not held, listed in the register's Open leads (the 2006 index is in the Saiz file) — session 95a94bd8


## 2026-06-25 — after the test/red-team/spec/harness-repair run

Everything doable without you is done and committed. Four things need you:

### 1. Pull two gated extracts → unblocks the deepest open tests (HIGH value, LOW effort)
Both are spec'd and the analysis code is already built + wired (skips until the data lands).
- **IPUMS-CPS** (your IPUMS account) → unblocks the **V02 2nd-generation-by-origin** cultural-transmission test (the real cross-generational decay, which IPUMS-USA can't do). Exact extract recipe: `research/immigration-gated-data-specs-2026-06-25.md` §1. Stage the CSV at `<data_root>/external/cps/cps_2ndgen.csv`; `load_cps_second_gen.py` runs automatically on the next `build context`.
  consumed: 2026-09-22 extract 1 staged at `external/cps/cps_2ndgen.csv.gz` (5,721,633 rows, ASEC 1994–2025) and the loader fixed for CPS 5-digit codes (1e62ca2) — session 87fa457f
- **openICPSR 120490** (free login) → Abramitzky-Boustan immigrant intergenerational-mobility data (rank-rank by origin). Spec §3. File manifest is `[UNVERIFIED]` (the page 403s automated fetch) — open it in a browser.

### 2. Decide: build the housing/rent panel? — **SUPERSEDED by item A above (2026-06-25): now spec'd, Zillow acquired, ready to build.**
4 E-cluster theories are PENDING-DATA: they need an **MSA-joined rent + immigrant panel** (PUMA→CBSA crosswalk + rent-burden + foreign-born-share + the Saiz elasticity×WRLURI panel). The urban frontier pass fully spec'd this and acquired the Zillow rent panel — see item A.

### 3. ~~CONFIRMED unit bug~~ — RESOLVED 2026-06-25 (it was a misnaming, not a computation bug)
**Done.** Investigation revised the diagnosis: `medicaid_total_computable` is a state-level Medicaid
TOTAL (CA $299B etc.) broadcast to every PUMA, so `AVG()` over an origin's PUMAs = the mean *state-total*
Medicaid — a correct "which states does this origin concentrate in" context signal (Ireland/Denmark →
$299B = California). The **value was right; the `avg_` prefix was misleading** (implied a per-adult figure).
Fix: renamed `avg_medicaid_total_computable` → **`mean_state_medicaid_total_usd`** (compose_scenario_ledger.py,
the only code consumer), allowlisted in the audit gate with justification, propagated through lifetime→unified.
**`reproduce.sh audit` now: ✓ no integrity flags.** *Optional enhancement still open (= the per-CAPITA version
the frozen pre-reg P3 anticipated):* a true Medicaid-per-resident figure needs a **state-population denominator**
(no state-pop column in the warehouse → an ACS pull). Low-value (it's a context column); flag if you want it.

### 4. ~~Re-specify 3 theories~~ — RESOLVED 2026-06-25
All three re-spec'd honestly in the cluster `.mining` JSONs (re-run verified): **A#4 → PENDING-DATA**
(no recent-arrival-by-education aggregate; stock-only can't adjudicate "recent > stock"); **K#0 →
NOT-TESTABLE** (provenance tautology — both per-pupil series from the same NCES F-33 source; needs two
independent products); **K#2 → now ADJUDICATES** — replaced the bare RPP listing with a real
border(TX/AZ/NM)-vs-gateway(NY/NJ/MA/IL) test: **destination spread 24.6% (SUPPORTED, >15%); clean
border-gateway split only ~10% (modest — CA is a high-cost border outlier).** Details + Revisions:
`research/immigration-theory-verdicts-2026-06-25.md`.

## Open asks, 2026-09-21
session: adae2b38-fa63-4fd0-b727-08c73975b287

- **Push is blocked** by GitHub push protection on a false-positive AWS key ID in f427f43 (`mr_archive_2026_09_18/derived/mr_posts.jsonl:597`, a 2016 presigned third-party URL; nothing to rotate). Choose: open the unblock link GitHub printed and mark it a false positive, or say "rewrite" (history rewrite was rehearsed in a scratch clone, not applied; main has advanced since, so it needs a fresh rehearsal).
  consumed: 2026-09-29 f427f43 — reached origin/main in the 2026-09-22 push (4d80e5a) with no history rewrite; nothing left to do — session 95a94bd8
- **Pew 2017 Survey of US Muslims microdata** need a free Pew account (religion × nativity × income × attitudes; the only US religion-observed file we can get quickly).
  consumed: 2026-09-22 zip staged at `external/pew/Pew-2017-US-Muslims.zip`, lane `pew_muslims_2017_2026_09_22` (report reproduced within 0.5 points), ladder 177, Muslim memo §2a — session 87fa457f
- **New Immigrant Survey 2003** public-use files (ICPSR 38031, 38061; free ICPSR login): religion with earnings for new green-card holders.
  consumed: 2026-09-22 ICPSR 38031 v3 staged at `external/icpsr_nis_2003/`, lane `nis2003_religion_earnings_2026_09_22` (19/26 anchors exact), ladder 179, Muslim memo §2b; 38061 (Round 2) not downloaded, visa class stays restricted — session 87fa457f
- **Propose, not enacted (analysis protocol):** for a contested cross-unit test, commit the lane README with outcomes, models and decision rule before downloading the predictors, and record deviations in RESULT.md. Done once in `admission_route_2026_09_21` (524291c); worth making the rule?

## Open asks, 2026-09-30
session: 95a94bd8-dcdc-4501-bb8e-5f9906dddc53

- **Row-4 consistency revision (recommend: yes, next session, as one set).** Five v4 items are summed on the survey's published 40.9M weights instead of the 39.71M the account prices: owner-occupied property (+$0.34bn), the Part A accrual (−$1.03bn), the benefit-tax receipt (−$0.03bn), state pricing's indexes (+$0.37bn) and the OASDI accrual ratio (+$0.15bn). Together the case moves to $371.2–434.6bn (headline still $371–435bn) and the cash set to $295.4–362.5bn. The social channels beside the account (housing, congestion, care, victims, scale, mobility) are also on 40.9M, about $1.3bn in the winners and world lanes. Evidence: `infra/immigration-fiscal/row4_class_2026_09_29/`. Recorded, not applied.
  candidate built 2026-09-30: `infra/immigration-fiscal/main_case_candidate_v41_2026_09_30/` (1bbeae94, 44 gates); adoption needs a new adopted lane, the 15 consumer lanes and the docs, listed in its RESULT.
- **Evidence map to v4 (recommend: yes).** It still states the September 27 claims: C2 "taxes cover benefits" is false on v4 (the group's taxes fall $3.4–12.6bn short of its household transfers with pensions on accrual), C1 says $355bn (v4 midpoint $403bn) and C5 85% (v4 68%). Evidence: `infra/immigration-fiscal/break_conditions_2026_09_29/RESULT.md`, section "v4 case (sept29)".
- **Push (recommend: yes).** main is about 50 commits ahead of origin/main (01e7d0b), including the peer session's Indian-origin lanes; keyscan clean on every commit this session.
  consumed: 2026-10-15 all three asks of this section were overtaken — the row-4 revision went into v7 as item
  row4_frame (148ed1ea); the evidence map has been on v6 since 2026-10-07 at his request; pushes went out since, last
  ed8fc58b on 2026-10-14 — session 75b08f57

## Open asks, 2026-10-14
session: 75b08f57-63cc-4e3d-96dc-60050327b5c1

Context: round 1 of the critique loop on main case v7 ($339.6–423.6bn) is fixed lane by lane; main case v8 is being
built from the adopted fixes. Each ask has my recommendation; the work proceeds on it unless you say otherwise.

- **Census coverage into the central (recommend: yes; v8 is built with it on, behind a switch).** The 2020
  Post-Enumeration Survey measures a 4.99% Hispanic undercount (SE 0.53 points). The 2024 population controls keep
  the Census Hispanic total, so the survey inherits that undercount. The old reason for keeping it beside ("the
  controls absorb part of it") is false. On v7 it adds +$11.1 / 14.8bn. Every construction except the
  demographic-analysis low series is positive (range −$16bn to +$26bn), so leaving it at zero is a convention-driven
  zero. Evidence: `infra/immigration-fiscal/coverage_bound_2026_10_14/RESULT.md`.
- **Value of a death (recommend: uniform DOT VSL, $13.7m, as now; life-years beside).** Life-years would lower the
  PM2.5 row by $35.6–42.6bn, because its deaths are old, and raise the crime rows by $4.0–5.0bn, because victims are
  young. Uniform VSL is DOT and EPA practice. Evidence: `social_respending_2026_10_14/RESULT.md`,
  `social_costs_unpriced_2026_09_28/RESULT.md` (P7 sections).
- **The world ledger's public-goods valuation (recommend: keep it report-only).** Valuing the public goods the group
  receives at its own willingness to pay (−$86.7 / −89.4bn) is a welfare frame, not the fiscal account's.
- **Map, explorer and figures to v8 (recommend: yes, once v8 is adopted and its docs pass is done).** They are on v6
  by your rule.
- **Push (recommend: yes, after the v8 docs pass audits clean).** main is 22 commits ahead of origin (ed8fc58b); they
  carry new findings (the corrected world ledger, comparators, social rows, back-cast, coverage) and the repo is
  public.
- **Item 6's low end (recommend: keep corporate taxes at response 1; correct the stated premise).** The low end
  holds if the capital serving the group's jobs leaves the US base and its owners earn the same after-tax return
  elsewhere, which is the rule the payload already applies; v7's decision called it "rents scale with the market",
  which is wrong. The pure-rent share φ is unmeasured for 2024. Fixed rents would raise the low end by φ × $28.4bn
  (over $5bn once φ > 0.18); rents vanishing with demand would lower it by up to $13.8bn. Both go beside. Evidence:
  `infra/immigration-fiscal/corporate_rents_2026_10_14/RESULT.md`.
- **The mixed-unit removal in v8's central (recommend: yes, as built).** It computes what happens to the
  non-members who stay in mixed units (their own returns, state taxes, refunds, benefits, consumption, property):
  +$10.7bn at the low end, +$14.5bn at the high, SE $4.4bn, replacing item 5b and the tax recomputation D. The lane
  itself recommended keeping it as an arm; I put it in because leaving those consequences of the same removal at
  zero is a convention zero. Off, it reproduces v7's items. Evidence:
  `infra/immigration-fiscal/mixed_unit_removal_2026_10_14/RESULT.md`.
- **Who wins (recommend: the stationary financing frame as the verdict, the cohort frame beside).** With every
  channel and the corrected payer pool, 4.6% / 8.4% of other residents come out ahead under rules a / b (was 19.6% /
  18.7%); the cohort frame moves that by under 0.2 points. Evidence: `winners_losers_2026_09_24/RESULT.md` (P7).
  [answered: 2026-10-15 01:02 JST, in chat, to each of the eight asks above: "ok"]
  consumed: 2026-10-15 value of a death — kept: uniform DOT VSL in the central, life-years beside — session 75b08f57
  consumed: 2026-10-15 world ledger public goods — kept report-only — session 75b08f57
  consumed: 2026-10-15 who wins — the stationary frame stays the verdict, the cohort frame beside — session 75b08f57
  (coverage, the mixed-unit removal and item 6's wording get their receipts at v8's adoption; the UIs and the push
  after v8's docs pass.)
  consumed: 2026-10-15 Census coverage — in v8's central as item 12 (+$12.0 / 15.9bn on v8), decision
  2026-10-15-main-case-v8 — session 75b08f57
  consumed: 2026-10-15 the mixed-unit removal — in v8's central as item 11 (+$10.7 / 14.5bn) — session 75b08f57
  consumed: 2026-10-15 item 6's low end — kept at response 1; the decision states the corrected premise in the rents
  lane's wording — session 75b08f57

## Open ask, 2026-10-15 00:45 JST: the Codex weekly plan
session: 75b08f57-63cc-4e3d-96dc-60050327b5c1

- **Codex budget (recommend: the v8 case and its propagation finish on the plan; the round-2 fix lanes on beside
  readings and round 3's GPT reviewers wait for your word).** The weekly Codex plan stood at 74% at 00:39 and rose
  7–9 points an hour through the evening (5% at 01:00 on 10-14). Over the last three hours this repo used about 48%
  of the Codex tokens on this machine and genomics about 38%. At that pace the plan runs out around 03:30–04:00 JST;
  it resets 2026-10-20 14:57 JST. The account also shows prepaid credits (balance 55,113.75) that Codex may draw on
  past the limit. The critical path (coverage, v8's final build, the consumer propagation) is running now. Held
  until you answer: the who-wins lane's round-2 fixes, the comparators' own mixed-unit removal, and round 3's GPT
  reviewers. The world-ledger fix worker is already in its research phase. Your options: continue on credits, wait
  for the reset, or run the held lanes as Claude workers (you asked for Sol to save tokens).
  [answered: 2026-10-15 01:02 JST, in chat: "yeah it's fine to use a bit more ... use common sense and taste ...
  Try to use 6.1 gpt sol etc."]
  consumed: 2026-10-15 the held lanes run on GPT-6.1 Sol, kept lean: the who-wins round-2 fixes now, the comparators'
  own mixed-unit removal after v8's adoption, round 3 with its GPT axes once round 2's fixes land — session 75b08f57

## Open ask, 2026-10-15 03:35 JST: Codex past the weekly plan
session: 75b08f57-63cc-4e3d-96dc-60050327b5c1

- **Prepaid credits for four more Sol lanes (recommend: yes; I report the credit burn after each).** The weekly plan
  reached 92% at 03:32 and rises 5–13 points an hour with two or three lanes running, so it reaches 100% around
  04:15–05:00 JST; after that Codex draws the prepaid credits (balance 55,113.75), which your 01:02 answer allows
  ("fine to use a bit more"). Still needing Sol: the two running propagation lanes; round 3's one method fix to v8
  (coverage charged the missed adults a second time for prisons, arrests and ICE, about −$3.2bn at every end); and
  the world ledger and who-wins lanes on v8. I take the docs pass and the evidence map, explorer and figures updates
  myself, without Codex; the critique rounds keep their small GPT axis. If you want no credits spent, the lanes after
  100% wait for the reset (2026-10-20 14:57 JST) and v8 is pushed with its docs once the fix lands, or the remaining
  lanes run as Claude workers.
  update 2026-10-15 06:10 JST: the weekly plan reached 100% at 06:02 with no Sol lane running; no credits have been
  drawn (balance still 55,113.75). Round 3's coverage fix landed without Codex (d1a24d47: v8 is $365.8–456.0bn), and
  I reran and committed the consumer lanes myself. Waiting on your word: the comparators' fix lane (round 3 found five
  problems over the $5bn bar, all on the comparator side: Census coverage, members' children, the mortality pairing,
  the school reprice; for example the Black comparison moves +$5.9–18.8bn), then the who-wins and world-ledger lanes
  on corrected v8. **Recommend: yes to credits for those three lanes**, because each is a multi-hour build the Sol
  workers already know and the docs pass needs their numbers. Without credits I start the comparator fixes myself
  (slower, on the Claude plan) and the other two wait for the 10-20 reset.
