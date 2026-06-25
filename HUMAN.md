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

### 3. Verify-then-fix candidate: a suspected sibling unit bug (correctness risk)
The remittance forensic audit flagged that `origin_fiscal_scenario_2023` **mixes total and per-adult columns** — `avg_medicaid_total_computable` ≈ $109B for Mexico looks like a *total* mislabeled as an *average*. If so, any theory/memo reading it as per-adult is wrong. Not yet confirmed (needs a column-level trace). Want me to audit + fix the whole table's units?

### 4. Re-specify 3 theories (CHEAP, your judgment on intent)
Three repaired tests now *run* but don't *adjudicate* their stated claim: **A#4** (no recent-arrival table exists — tests stock-weighted NPV instead), **K#0** (CORR = 1.0 is a provenance tautology — same NCES source on both sides), **K#2** (lists RPP, doesn't test the border-vs-gateway differential). They need the intended comparison clarified. Details: `research/immigration-theory-verdicts-2026-06-25.md`.
