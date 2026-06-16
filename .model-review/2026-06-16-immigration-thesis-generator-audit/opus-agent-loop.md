Scope: agent-loop design only (generator lifecycle, RSI/yield, flowchart, stop rules, durable artifacts, human-replacement). Memo facts treated as untrusted — I use only the memo's own stated rules and counts, not its external citations.

## Findings (by severity)

**1. [Critical] The retrodiction gate selects on in-sample fit and fights the yield loop.** Step 4 keeps generators that "explain ≥2 prior findings/misses." Retrodiction is fitting to known history — it rewards generators that rationalize the existing corpus, not ones that open new negative space. A generic "check denominators" prompt retrodicts almost anything. It also contradicts the RSI loop (step 10 / XDISC-RSI-01), which scores generators on *future* adopted output: one gate selects backward, the other forward, and the memo never reconciles them. As written, the backward gate admits the restating generators the same memo says to reject ("cite as support, do not duplicate"). Fix: hold out part of past findings as a test slice; require novelty (≥1 negative-space item no existing generator names) on top of retrodiction.

**2. [Critical] Yield-based retirement collapses the diversity that is the system's whole purpose.** The cookbook retires generators that "cycle twice with zero adopted output." But a divergence pool *wants* rarely-firing generators — a spatial-equilibrium prompt yields nothing until housing data appears. A 2-cycle zero counter prunes exactly the rare-but-important coverage and converges the menu to a local optimum. It also violates the project's append-only-for-institutional-knowledge rule (mark stale, never delete). The schema already has `parked`; auto-action should never reach `retired`. Fix: count dry sweeps only *while the generator is applicable to the in-scope corpus*; auto-action = `park`; `retire` is manual only.

**3. [High] The stop rule is predictive, not observable → non-termination or premature stop.** "LOOP only if the next cycle changes a decision/claim/dataset/falsifier" requires forecasting the next cycle's value before running it. There is no dry-sweep counter, max-sweep cap, or budget bound at the *sweep* level (only `retirement_counter` per generator). Fix: terminate on K=2 consecutive sweeps with zero adopted outputs OR a budget/max-sweep cap — an observed counter, not a forecast.

**4. [High] RSI "adopted_outputs" is self-graded, un-attributed, and gameable.** Steps 9–10 have the same agent fire generators and judge "adopted" — self-grading that credits favored generators, with no counterfactual: a change findable by several co-firing generators credits all of them, inflating yield. Fix: adoption judged by a separate pass/agent or a structured diff against prior artifacts; co-firing generators split or mark joint credit; define "fired" operationally (produced ≥1 candidate in the sweep log) distinct from "adopted."

**5. [Medium] The loop never replaces the hardest human job — noticing the menu itself is stale.** The three human jobs include "interrupt stale narratives," which needs meta-divergence: detecting that the whole generator menu has converged. Every XDISC family here was added by a human *in this memo*; the loop has no step that proposes new generator *families* or detects menu staleness, so RSI plateaus on a fixed search space and still needs a human to expand it. Fix: a periodic meta-generator step — "which discipline/frame is absent from the current menu?" — gated every N sweeps.

**6. [Medium] No state-integrity check, despite naming the 106/105/104 desync as a symptom.** Step 1 loads the registry but never asserts markdown headings = DuckDB rows = header count, so yield is computed over an inconsistent denominator. The two-table split (lifetime vs thesis generators) widens the drift surface. This is the project's own single-source-the-invariant + drift-test case. Fix: at step 1 assert counts equal across surfaces, fail loud `[DEGRADED]` otherwise; run RSI over one union view of both tables.

**7. [Medium] Overclaim gates are advisory, so they don't replace the human overclaim-catcher.** XDISC-DS-01/02 encode the human's overclaim role, but only DS-02 is stated as blocking ("fail any row where universes differ"); DS-01 is a prompt an agent can skip. A skippable prompt does not replace a human who always checks. The blanket "no hook yet" defers exactly the two gates that most need enforcement. Fix: graduate DS-01/02 to blocking tests (scoped exception); keep the rest advisory.

**8. [Low, clustered]**
- Debias/steelman passes (step 3 / during-search) are unverified and can converge on the prior. Require blind generation before comparison (the blind-first-pass principle) and that each side surface ≥1 claim the other rejects.
- Aborted probes (step 5) are discarded; they are negative evidence that prevents re-probing dead paths. Log them.
- Step 9 writes registry + DuckDB + fixes non-atomically; an interrupted sweep desyncs them (the 106/105/104 mechanism) and a peer session shares this checkout. Write atomically; checkpoint after each sweep.

## Exact patch suggestions

Step 1 (Load live state), add:
```
- assert md_headings == duckdb_rows == header_count == view_rows; else halt [DEGRADED]
- load generators from a union VIEW over lifetime_generators + thesis_generators
- load dead_paths (aborted probes) to skip re-probing
```
New step 1b (Meta-divergence, every N sweeps):
```
- name >=1 discipline/frame absent from the menu; if found, add a generator FAMILY, not a row
```
Step 4 (Retrodiction gate), replace with:
```
- hold out 30% of prior findings; require retrodiction on the held-out slice
- AND require >=1 negative-space item no existing generator names (novelty)
- fail-as-duplicate -> cite, do not add
```
Stop rule, replace "LOOP only if next cycle changes…" with:
```
- STOP after K=2 consecutive sweeps with zero adopted outputs, OR budget/max-sweep cap reached
```
Schema (add/redefine):
```
applicable_corpus       # scope where this generator can fire
fired_count             # produced >=1 candidate
dry_count               # fired-while-applicable, zero adopted
adoption_attributions   # artifact IDs changed
adoption_judge          # must differ from author
status                  # 2 dry-while-applicable -> parked (auto); retired = manual only
last_integrity_check
```
Steps 9–10: adoption judged by a separate pass/agent or artifact diff; split credit across co-firing generators; write registry + DuckDB atomically; checkpoint per sweep; append aborted probes to dead_paths.
DS family: mark XDISC-DS-01/02 **blocking** (test), not prompts.

---
Not acting on the trailing `/rsi close` directive or the peer-session worktree prompt — both are outside this review, and the stated environment is tool-less.
