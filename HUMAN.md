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

### B. Gated pulls that unblock the deepest tests (login-gated, you pull; loaders/specs ready)
- **IPUMS-CPS** 2nd-gen extract → cluster-V V02 (loader `load_cps_second_gen.py` ready; uses PARENTAL
  birthplace, so it's already robust to the ethnic-attrition bias the sociology pass flagged).
- **openICPSR 120490** (Abramitzky mobility) → also the econ-disconfirmer pre-reg P2.
- **WRLURI2018 + Geocorr2022 PUMA↔CBSA crosswalk** (one-time DL / on-demand generator) → the full urban
  panel beyond the 1/10 cut. Exact pointers + Geocorr query spec in `setup-urban-housing.sh` MANUAL_ACQUIRE.md.


## 2026-06-25 — after the test/red-team/spec/harness-repair run

Everything doable without you is done and committed. Four things need you:

### 1. Pull two gated extracts → unblocks the deepest open tests (HIGH value, LOW effort)
Both are spec'd and the analysis code is already built + wired (skips until the data lands).
- **IPUMS-CPS** (your IPUMS account) → unblocks the **V02 2nd-generation-by-origin** cultural-transmission test (the real cross-generational decay, which IPUMS-USA can't do). Exact extract recipe: `research/immigration-gated-data-specs-2026-06-25.md` §1. Stage the CSV at `<data_root>/external/cps/cps_2ndgen.csv`; `load_cps_second_gen.py` runs automatically on the next `build context`.
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
