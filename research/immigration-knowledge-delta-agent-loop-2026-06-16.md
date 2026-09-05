# Immigration knowledge delta and autonomous research loop (2026-06-16)

**2026-09-05 scope correction:** This is a June knowledge/loop record, not a current causal or data-validity certificate. The old Mexico annual fiscal numbers are withdrawn; raw data are now available at the canonical drive path. QWI monthly earnings cannot identify native-born wage effects, and synthetic arrival cohorts are repeated cross-sections, not a person panel. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).

**Question:** What do we know now that we did not know two days ago, and what loop should an agent run to reduce constant human steering of search space and narrative?

**Comparison baseline:** state before the 2026-06-15 fiscal sweeps and the 2026-06-16 conclusion audit. At that point, the repo already had the April wage/housing/capacity/crime/surge analyses and the 2026-06-11 CHNV/receiver-election correction, but not the June 15-16 fiscal tensor, denominator audit, or model-review cleanup pass.

**Canonical status:** this memo is the umbrella loop. `research/immigration-thesis-generator-audit-2026-06-16.md` expands steps 3-5 for generator/XDISC divergence; `notes/immigration-lifetime-synthesis-diverge-cookbook.md` and `notes/immigration-lifetime-sweep-protocol.md` are sub-procedures for sweep execution.

---

## 1. Historical June knowledge change, with current corrections

### A. The fiscal story moved from scalar debate to ledger tensor

Two days ago, the live fight could still collapse into "Mexico positive or negative?" or "immigrants pay in or drain?" The current state is stricter:

- `federal_annual` is one layer, not a verdict.
- NAS Table 8-13 is a synthetic age-at-arrival-25 education-mix benchmark, not current-stock lifetime NPV.
- school burden, state/local surge, admin/enforcement, courts, and episodic shelter are separate layers.
- any single "Mexico net" without layer tags is now a known error class.

**New knowledge:** the correct object is a tensor: `population/group x layer x time horizon x effect order x population universe`.

### B. The Mexico fiscal result became less certain but more true

The June 15 loop first found a plausible correction: the old `-$13.5k/adult` school result used the scenario-subset denominator. That briefly made the crude annual `federal - school` row positive (`+$748/adult`).

The June 16 Opus review then caught the mirror-image bug: the school numerator still came from the scenario household universe, while the denominator was changed to the full microsim stock. We verified this in DuckDB:

- scenario adults: `436,819`
- scenario linked household weight: `322,539.5`
- full microsim adults: `8,496,334`
- current guarded `v_three_layer_annual` now withholds origin `school_per_adult` and `net_crude_per_adult`.

**Current correction (2026-09-05):** The earlier school sign changes exposed a universe mismatch. The remaining ~$1,519/adult federal annual proxy was subsequently found invalid too: household/person allocation and education coding require rebuilding. No old Mexico fiscal scalar remains validated by that June exercise. [SOURCE: ../decisions/2026-09-05-material-inference-repair.md]

### C. The NAS Mexico headline was relabeled

`+$45,631/adult` and `+$387.7B` are now known to be current education mix times NAS age-25 cells. They block a crude "all Mexico-origin adults are `<HS` NAS negatives" export, but they do not measure remaining-lifetime NPV of the current Mexico-born stock.

**New knowledge:** education mix matters, but age-at-arrival/current-age lifecycle remains a missing dimension.

### D. E-Verify became a bounded wage-margin result, not a Card/Borjas verdict

Two days ago, short forms still overread E-Verify as a broad Card-side or Borjas-rejection result. Current wording:

- the June model reported no statistically significant positive QWI monthly-earnings estimate; the outcome contains all covered stable employees, with no nativity split;
- the June exposed-industry confidence interval/MDE concern that monthly-earnings outcome and the fitted design, not native-born hourly pay;
- native-born wage gains are not identified by this QWI outcome; heterogeneous-treatment and other design checks cannot create a missing nativity dimension;
- small effects and scaled-shock Borjas benchmarks are not ruled out;
- the E1 employment point estimate is negative but nonsignificant (`t=-1.40`, `p≈0.16`);
- adjustment channels remain hypotheses, not measured mechanisms.

**Current interpretation:** This is a policy-margin analysis of the recorded QWI earnings/employment outcomes, with remaining design limits. It does not identify native-born wages or transfer automatically to a surge, mass deportation or open-borders counterfactual. [INFERENCE]

### E. The surge/capacity evidence became descriptive rather than causal

Receiver-city gross loads are real and large. The 2024 receiver election association survives the Hispanic-share kill-test at about `+2.4pp`, but it is still correlational. Capacity/load county models are useful screens, but:

- wage-model ranking gaps are thin;
- permit denominators may proxy local economic vitality;
- q90 threshold weakness may be a power artifact;
- native sorting is association until counterfactual identification exists.

**New knowledge:** capacity is still a promising search frontier, but it should be framed as descriptive stress-screening plus open causal work.

### F. Crime conclusion got cleaner

The observed-rate conclusion survives, but it is now explicitly:

- observed arrest/conviction/incarceration rates, not true offending;
- aggregate Texas ratios, with demographic standardization a distinct question;
- Lott classification critique as serious unresolved critique, not independently verified flaw.

**New knowledge:** the pro-immigration crime conclusion remains strong directionally, but the estimand is narrower.

### G. Model review was useful because it found drift, not because it supplied facts

The llmx Opus/GPT and Cursor passes were most valuable at finding internal contradictions:

- Opus found the school numerator/denominator universe mismatch.
- Multiple reviewers independently flagged E-Verify employment nonsignificance.
- Reviewers surfaced stale synthesis phrases after source memos had been fixed.

**Process knowledge:** frontier review should be used as adversarial pressure on internal coherence; every finding still needs local verification against data, code, or exact file text.

---

## 2. Updated interpretation of the June claims

The interpretation after the September measurement corrections is:

1. **No scalar verdict.** Immigration fiscal effects are layer-specific and universe-specific.
2. **Withdrawn numerical result (2026-09-05):** The earlier +$1,519/adult, +$12.9B annual Mexico result and derived native comparison are invalid pending correction of household-to-person allocation and education codes. They must not be consumed as a current fiscal estimate. See the September decision. [SOURCE: ../decisions/2026-09-05-material-inference-repair.md]
3. **School/full-stock origin row:** unresolved after same-universe guard.
4. **NAS benchmark:** Mexico education mix looks positive under age-25 NAS cells, but that is not current-stock lifetime NPV.
5. **Earnings:** the QWI E-Verify analysis does not identify native-born wages; its monthly-earnings estimate and confidence interval apply only to its measured population and fitted policy design.
6. **Capacity/surge:** receiver gross load and county load/capacity screens are real descriptive signals; mechanisms and welfare signs remain open.
7. **Crime:** lower observed justice-system rates remain supported; true-offending and subgroup generalization remain lower confidence.

This is less rhetorically satisfying than two days ago. It is better research.

---

## 3. Autonomous Agent Loop

The human was doing three jobs:

1. choosing where to look next;
2. noticing when the narrative had outrun the evidence;
3. forcing divergence when the current frame became too comfortable.

The agent loop has to mechanize those jobs.

```text
START
  |
  v
1. Load Constitution + Current Frontier
  - read topic index, current synthesis, running fixes, last decisions
  - list live claims with canonical provenance tags from notes/provenance-tags.md
  - identify what changed since last run
  |
  v
2. Claim Inventory
  - split every narrative into atomic claims
  - attach layer, population universe, time horizon, denominator, evidence level
  - mark each claim as live / superseded / unresolved / historical
  |
  v
3. Weakest-Link Audit
  - find claims whose conclusion depends on one fragile bridge:
    denominator, scalar export, causal verb, significance, proxy, stale table
  - rank by decision impact, not by ease
  |
  v
4. Divergence
  - generate 5+ different kill paths:
    data bug, denominator mismatch, rival estimand, omitted layer,
    alternative causal mechanism, external-validity boundary, value-frame shift
  - run the XDISC/generator packet from immigration-thesis-generator-audit
  - search by functionality and claim structure, not filenames
  |
  v
5. Cheap Probe
  - one SQL query, one grep, one table checksum, one 10-row sample,
    one coefficient check, or one source quote
  - if probe fails, fix conclusion before building more machinery
  |
  v
6. Evidence Build
  - acquire or rebuild only the minimum dataset needed
  - preserve raw data; derived outputs are rebuildable
  - record exact command and output rows for load-bearing numbers
  |
  v
7. Convergence
  - update source memo, synthesis memo, ladder, index/frontier surfaces
  - append running-fixes entry: issue, evidence, fix, unresolved remainder
  - delete/mark stale scalar exports; do not leave both versions live
  |
  v
8. Adversarial Review
  - llmx Opus/GPT + Cursor lanes on exact packet
  - require file:line findings and minimal fixes
  - verify every finding locally before accepting
  |
  v
9. Commit + Diff Audit
  - commit exact paths per logical fix
  - grep for stale phrases and superseded claims
  - check worktree for unrelated/untracked artifacts
  |
  v
10. RSI Close / Next Frontier
  - verify one load-bearing claim from this loop
  - compare knowledge state to previous baseline
  - promote one process guard if recurrence is hookable
  - choose the next frontier by value of information
  - after 2 consecutive dry sweeps or a budget/max-sweep cap, stop and escalate to human
  |
  v
REPEAT only if a frontier remains live and the stop rule has not fired
```

---

## 4. The Search-Space Shaping Heuristic

Each cycle should maintain a frontier table:

| Frontier | Ask | Stop rule |
|---|---|---|
| Denominator | Are numerator and denominator the same population/time/unit? | exact row-level reconciliation passes |
| Layer | Which ledger layer does this claim live in? | claim has layer tag and no scalar export |
| Margin | What policy/data variation identifies the claim? | no extrapolation beyond named margin |
| Mechanism | Is the mechanism measured or inferred? | causal verbs removed unless design identifies |
| Significance | Is non-significance being read as zero or as effect? | wording distinguishes point estimate, CI, MDE |
| Counterfactual | What would falsify the current narrative? | explicit kill path or unresolved label |
| Narrative | What slogan would a reader wrongly quote? | grepable stale phrase removed or marked historical |

The loop reduces constant human steering by forcing every cycle through this table before and after evidence work. It does not fully replace human judgment until claim inventory, dead-path logging, generator-yield state, and adoption judging are persisted.

---

## 5. Divergence and Convergence Rhythm

Use a fixed cadence:

1. **Diverge hard:** at least five mechanism-distinct ways current conclusions could be wrong.
2. **Probe cheap:** test one high-impact weak link first.
3. **Converge narrowly:** patch only conclusions the evidence actually changes.
4. **Review adversarially:** outside models search for drift and contradiction.
5. **Verify locally:** accept nothing from reviewers without repo/data evidence.
6. **RSI:** capture one durable process improvement or next frontier, not a broad retrospective.

The key is not "more agents." It is parent-controlled epochs: dispatch, read, verify, patch, then redispatch only if the frontier actually changed.

---

## 6. Next High-Value Frontiers

1. **Same-universe origin school burden rebuild.**
   Build a full-stock household school numerator or keep the row null. This is the biggest live fiscal blocker.

2. **Current-stock lifetime NPV.**
   Age-at-arrival x current-age x education x return migration. The age-25 benchmark is useful but not enough.

3. **Capacity causal design.**
   Show load adds signal beyond permit level and local growth, or demote load/capacity from frontier to descriptive screen.

4. **Receiver-city synthetic controls.**
   Gross load is measured; vote/fiscal mechanism needs better counterfactuals.

5. **Crime subgroup/time heterogeneity.**
   Preserve observed-rate conclusion while testing whether recent-surge origin mix or second-generation patterns change any local claims.

The next loop should start with frontier 1, because it gates several fiscal narratives and has a concrete denominator invariant.

## Current interpretation and acquisition status (2026-09-05)

The canonical data root is `/Volumes/2TBPNY/research-data/immigration-fiscal/data`; current raw-data access supersedes June statements that the old `sources` symlink proves the data absent. A completed build or populated table is not scientific validation. The fiscal allocation/education rebuild must precede using its derived Mexico annual estimate or native ratio. [SOURCE: current filesystem inspection and September decision]

The QWI sex-by-education API has no nativity/citizenship dimension. `EarnS` is average monthly earnings of stable/full-quarter employees, not an hourly wage. Consequently the June loop’s E-Verify result cannot establish a native-born wage null. Non-significance on its actual outcome also does not prove zero or exclude an economically important effect without an interval and design assessment. [SOURCE: https://api.census.gov/data/timeseries/qwi/se/variables.html; INFERENCE]

`build_immigrant_assimilation_profile.py` follows origin×arrival-decade cells across independent census/ACS samples with a changing age-25–64 composition and positive-income conditioning. This reduces one cross-cohort mixing problem but does not remove all cohort-quality, age, period or selective-migration differences; it does not observe within-person assimilation. CPS parental birthplace supports a distinct second-generation comparison and should not be confused with ACS ancestry self-identification. [SOURCE: local builders; INFERENCE]

CBO 60165 projects a roughly $897B reduction in covered federal deficits over 2024–2034; it includes mandatory spending/net interest and excludes discretionary appropriations and state/local budgets. Its roughly $0.2T discretionary illustration is a scenario, not a verified bound. The projection, NAS fiscal NPVs and an annual local ledger cannot be combined without matching population, horizon and counterfactual. [SOURCE: https://www.cbo.gov/publication/60165; INFERENCE]


## Revisions

- **2026-09-05 — Separated historical loop results from corrected measurement and current data status** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Historical revision entries above describe the earlier state, including conclusions superseded here.
