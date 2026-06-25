# HUMAN.md — what needs you (autonomous-run escalation)

The loop's non-blocking human-outbox. Items here need an operator action or decision that an
autonomous run cannot resolve itself. Newest first.

## 2026-06-25 — after the test/red-team/spec/harness-repair run

Everything doable without you is done and committed. Four things need you:

### 1. Pull two gated extracts → unblocks the deepest open tests (HIGH value, LOW effort)
Both are spec'd and the analysis code is already built + wired (skips until the data lands).
- **IPUMS-CPS** (your IPUMS account) → unblocks the **V02 2nd-generation-by-origin** cultural-transmission test (the real cross-generational decay, which IPUMS-USA can't do). Exact extract recipe: `research/immigration-gated-data-specs-2026-06-25.md` §1. Stage the CSV at `<data_root>/external/cps/cps_2ndgen.csv`; `load_cps_second_gen.py` runs automatically on the next `build context`.
- **openICPSR 120490** (free login) → Abramitzky-Boustan immigrant intergenerational-mobility data (rank-rank by origin). Spec §3. File manifest is `[UNVERIFIED]` (the page 403s automated fetch) — open it in a browser.

### 2. Decide: build the housing/rent panel? (MEDIUM effort, needs a go-ahead)
4 E-cluster theories are PENDING-DATA: they need an **MSA-joined rent + immigrant panel** (PUMA→CBSA crosswalk + rent-burden + foreign-born-share + the Saiz elasticity×WRLURI panel). None exists in the warehouse. This is a real build — say the word and I scope it. It's the missing housing-incidence ledger both red-team models flagged as a gap.

### 3. CONFIRMED unit bug — needs a denominator-modeling decision (your call)
The new data-integrity gate (`reproduce.sh audit`) **confirmed** it: `lifetime.origin_fiscal_scenario_2023.avg_medicaid_total_computable` reaches **$299B** in a column named "avg." Trace: it's `AVG(medicaid_total_computable)` — a plain mean of per-PUMA *totals*, sitting next to siblings (`avg_federal_net`, …) that are properly *weighted per-adult* (`SUM(x·adults)/SUM(adults)`). So it's genuinely inconsistent. **Blast radius is low** — it's carried as a context column, not fed into a headline fiscal calc (only `compose_scenario_ledger` + the verdict memo read it). The fix isn't a clean rename: it needs the right per-capita **denominator** for a Medicaid-per-adult figure consistent with its siblings — a modeling decision I didn't want to rush. Say go and I'll make it weighted-per-adult.

### 4. Re-specify 3 theories (CHEAP, your judgment on intent)
Three repaired tests now *run* but don't *adjudicate* their stated claim: **A#4** (no recent-arrival table exists — tests stock-weighted NPV instead), **K#0** (CORR = 1.0 is a provenance tautology — same NCES source on both sides), **K#2** (lists RPP, doesn't test the border-vs-gateway differential). They need the intended comparison clarified. Details: `research/immigration-theory-verdicts-2026-06-25.md`.
