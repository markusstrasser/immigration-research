# Pre-Registration Ledger — frozen predictions before the gated data lands

**Purpose.** The deepest open tests (cluster-V V02 2nd-gen transmission; immigrant mobility)
are blocked on gated data not yet pulled (IPUMS-CPS, openICPSR 120490). That is a rare
chance for a *genuine out-of-sample test*: register the predicted result + falsifier **now**,
before seeing the data, so the eventual finding is a real prediction, not a post-hoc fit.
This directly guards the in-sample-proxy / Goodhart failure the project's own rules warn about
(a loop that ratchets on a dev-set proxy overfits) — you cannot overfit a prediction you froze
before the data existed.

**Instrument-bias measurement (the second purpose).** Each entry records the LLM instrument's
prior *and its known bias direction* before data. When the data lands, score (a) predicted vs
actual, and (b) how far the data moved the instrument — turning the "soft progressive prior on
immigration" caveat from prose into a measured per-claim quantity. See `notes/llm-bias-caveat.md`.

**Protocol.** Entries are APPEND-ONLY and frozen. Do NOT edit a prediction after the fact —
when data resolves it, add a dated `RESOLVED` block below the entry with actual vs predicted,
the calibration hit/miss, and the instrument-update. Resolution is evidence-triggered (when the
operator pulls the data), never self-triggered.

---

## P1 — CPS 2nd-generation-by-origin cultural transmission (cluster-V V02)
**Frozen:** 2026-06-25 · **Data:** IPUMS-CPS ASEC 1994→ (FBPL/MBPL/NATIVITY), not yet pulled · **Loader ready:** `load_cps_second_gen.py`

**Prediction (direction + magnitude):** 2nd-generation immigrants (NATIVITY=4, both parents foreign)
by parental origin will show **partial, decaying** persistence — origin differences in income and
female LFP **detectable in the 2nd gen but roughly HALF or less of the 1st-gen gap** to the 3rd+
native baseline. Concretely, the Mexican-origin 2nd-gen log-income gap to natives will be **≤ ~0.20**
(vs the ~0.30–0.70 first-gen gap the assimilation profile shows), i.e. substantial convergence but
not full closure. **Confidence 0.68.**

**Falsifiers:** (a) 2nd-gen origin gaps ≥ 1st-gen gaps (no decay → strong fixed cultural persistence,
the deep-roots V-cluster direction); (b) zero detectable 2nd-gen origin differences (full one-generation
assimilation). Either would move the cluster-V central estimate.

**Instrument-bias flag:** my prior leans toward the *assimilation-strong / persistence-weak* (pro-immigration)
reading — that is the documented bias direction. **Therefore I will weight a more-persistence (disconfirming)
result as the higher-information outcome**, and not discount it as noise.

## P2 — Immigrant intergenerational mobility (openICPSR 120490)
**Frozen:** 2026-06-25 · **Data:** Abramitzky-Boustan-Jácome-Pérez AER 2021 replication, not yet pulled

**Prediction:** immigrants' children show rank-rank upward mobility **at or above** US-born children of
similarly-poor parents, **with meaningful origin variation** (lower for some origins). **Confidence 0.72.**
Caveat: this is *weakly* out-of-sample — it's the published paper's own data, so a high prior is
warranted; the genuine test is the **origin-by-origin variation**, which the headline paper aggregates.

**Falsifier:** immigrants' children at or below native mobility across most origins.

**Instrument-bias flag:** same pro-immigration prior direction; the informative surprise is *low* mobility
for specific origins (would feed the cluster-V ethnic-capital/slow-assimilation lens, V04).

## P3 — avg_medicaid unit fix (mechanical, near-certain)
**Frozen:** 2026-06-25 · **Data:** in-warehouse (`origin_fiscal_scenario_2023`)

**Prediction:** when `avg_medicaid_total_computable` is recomputed as a proper weighted **per-adult**
figure (consistent with `avg_federal_net`), the Mexican-origin value will be in the **low thousands of
dollars/adult**, not the current $299B. **Confidence 0.95** (it's a confirmed unit bug; this is a sanity
anchor, not a discovery). Falsifier: a per-adult value still > $100k after a correct denominator.

---

## Resolution log
*(append `RESOLVED P# — YYYY-MM-DD` blocks here as data lands; never edit the predictions above)*
- (none yet)
