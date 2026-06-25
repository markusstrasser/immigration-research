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

### A. The 1/10 MSA rent panel is READY to build (Zillow acquired) — green-light the analysis phase
This is the single highest-value next step and supersedes the old item 2 below. **Zillow ZORI/ZHVI
metro panels are acquired** (`setup-urban-housing.sh`, 739 metros monthly 2015-2026). The 1/10 build =
Zillow/ACS rent × ACS foreign-born-share by CBSA × Saiz elasticity, regress Δrent on Δfb-share —
replicates Wilson-Zhou (2026) +2.2%/+1.4% at ~zero cost; delivers the housing-incidence ledger both
red-team models flagged as missing. **Honest friction:** the joins have vintage-mismatch crosswalks
(Zillow-RegionID↔CBSA; Saiz-1999-MSA↔2020-CBSA) — the existing `saiz_decomposition.py` / Saiz×ACS
merge already solved the Saiz side, so the build reuses it. It's a real analysis phase (~1hr), so I
checkpointed here rather than compound it onto the research pass. **Say "build the panel" and I run it.**

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

### 3. CONFIRMED unit bug — needs a denominator-modeling decision (your call)
The new data-integrity gate (`reproduce.sh audit`) **confirmed** it: `lifetime.origin_fiscal_scenario_2023.avg_medicaid_total_computable` reaches **$299B** in a column named "avg." Trace: it's `AVG(medicaid_total_computable)` — a plain mean of per-PUMA *totals*, sitting next to siblings (`avg_federal_net`, …) that are properly *weighted per-adult* (`SUM(x·adults)/SUM(adults)`). So it's genuinely inconsistent. **Blast radius is low** — it's carried as a context column, not fed into a headline fiscal calc (only `compose_scenario_ledger` + the verdict memo read it). The fix isn't a clean rename: it needs the right per-capita **denominator** for a Medicaid-per-adult figure consistent with its siblings — a modeling decision I didn't want to rush. Say go and I'll make it weighted-per-adult.

### 4. Re-specify 3 theories (CHEAP, your judgment on intent)
Three repaired tests now *run* but don't *adjudicate* their stated claim: **A#4** (no recent-arrival table exists — tests stock-weighted NPV instead), **K#0** (CORR = 1.0 is a provenance tautology — same NCES source on both sides), **K#2** (lists RPP, doesn't test the border-vs-gateway differential). They need the intended comparison clarified. Details: `research/immigration-theory-verdicts-2026-06-25.md`.
