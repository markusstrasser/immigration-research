## Verdict (Reviewer E)

**Not operational enough to replace human steering.** The two flowcharts are a strong process spec with real guardrails, but they lack persisted state, enforceable stop/yield machinery, and consistent routing. The packet itself flags the gaps (`context.md:278`, `context.md:305`, `context.md:247`, `context.md:3119`).

---

## Knowledge-delta loop (`immigration-knowledge-delta-agent-loop`)

### Confirmed — what works

| Item | Evidence |
|------|----------|
| 10-step loop (inventory → weakest-link → divergence → probe → converge → review) | `context.md:147-214` |
| Frontier table with per-axis **Ask** + **Stop rule** | `context.md:222-232` |
| Parent-controlled epochs (dispatch → verify → patch → redispatch) | `context.md:247` |
| Cheap-probe-before-build discipline | `context.md:181-184` |

### Confirmed — blockers

| Gap | Evidence | Minimal fix |
|-----|----------|-------------|
| **No epoch stop rule** — ends `REPEAT` with no cap or zero-yield halt | `context.md:213`, `context.md:178` | Add same STOP as thesis flowchart: 2 dry sweeps or budget cap |
| **No persisted state** — “list live claims,” “identify what changed” have no path/schema | `context.md:156-159`, `context.md:122-125` | One `claims_inventory.yaml` or running-fixes subsection: claim_id, status, layer, universe |
| **No yield attribution** — no fired/adopted linkage | (absent from loop) | Step 10: log `claim_id → probe → artifact_diff → adopted?` |
| **No dead-path store** — thesis flowchart has it; this loop does not | `context.md:430` vs absent in `context.md:147-214` | Step 1 load + Step 5 write `dead_paths.md` on probe abort |
| **No handoff to XDISC/thesis-generator** — companion split declared but not wired in flowchart | `context.md:276` | Step 4: “run XDISC packet from thesis-generator audit before search” |
| **Stop rules are qualitative** — “exact row-level reconciliation passes” is not machine-checkable | `context.md:227-230` | Tie each frontier row to a grep/SQL predicate (e.g. DS-02 universe twin) |

### Speculative

- Frontier table alone may cover ~70% of human “narrative drift” catches if claim inventory is automated — but adoption still needs a judge (`context.md:481`).
- “Replace constant human steering” at `context.md:232` overstates readiness given `parent-controlled epochs` at `context.md:247`.

---

## Thesis-generator flowchart (`immigration-thesis-generator-audit`)

### Confirmed — what works

| Item | Evidence |
|------|----------|
| Explicit **STOP**: 2 consecutive zero-adoption sweeps or budget cap | `context.md:486`, `context.md:215` |
| Registry integrity gate: MD == DuckDB or `[DEGRADED]` | `context.md:429`, `context.md:158` |
| **Dead-path / aborted-probe** load at start | `context.md:430`, `context.md:159` |
| Generator mix quota (≤8/sweep, steelman + narrative + DS-01) | `context.md:438-441`, `context.md:168-170` |
| Yield step: fired / adopted / false-lead / retired; adoption judged separately | `context.md:479-482`, `context.md:208-211` |
| Proposed lifecycle schema | `context.md:498-514`, `context.md:227-244` |
| XDISC dedup-before-load gate | `context.md:370-381`, `context.md:99-111` |

### Confirmed — blockers

| Gap | Evidence | Minimal fix |
|-----|----------|-------------|
| **Lifecycle not implemented** — no `status`, `last_fired`, `adopted_outputs` in DuckDB | `context.md:289-290`, `context.md:324`, `context.md:537-539` | Manual YAML sidecar for one sweep per `context.md:494` |
| **Count drift blocks yield** — 106 MD / 104 DB; MD-only `G-LIF-Q06`, `G-LIF-S15` | `context.md:289`, `context.md:3107` | Reconcile before any automated retirement (`context.md:522`) |
| **`max-sweep cap` undefined** | `context.md:486` | Set numeric cap in sweep memo frontmatter |
| **XDISC memo-only, not registry** | `context.md:330`, `context.md:59` | Expected; enforce “run packet” via checklist, not DB |
| **Routing conflict: XDISC timing** | Sweep protocol: XDISC **after** converge (`context.md:1867`); flowchart + index: **before** search (`context.md:438`, `context.md:1501`, `context.md:1835`) | Canonical order: **XDISC before diverge/search**; drop step 5 placement in sweep-protocol |
| **Stale repeated prompts** — cookbook subagent template is fiscal-only, no XDISC/DS-01/estimand | `context.md:1605-1619` | Prefix template with self-prompt packet (`context.md:390-414`) + “skip if in dead_paths” |

### Speculative

- Retrodiction gate (`context.md:450-456`) may over-filter without held-out slice enforcement — packet already flags this (`context.md:533`).
- Two dry sweeps → park is workable only after lifecycle sidecar exists (`context.md:481`, `context.md:211`).

---

## Cross-loop integration

### Confirmed

| Issue | Evidence |
|-------|----------|
| **Two loops, one human parent** — knowledge-delta owns claim/review/commit; thesis-generator owns XDISC only | `context.md:276` |
| **Cookbook still fiscal-center-of-gravity** despite XDISC routing | `context.md:288`, `context.md:1513-1533` |
| **Verdict: fiscal-only sweeps should stop** | `context.md:3119`, `context.md:2486` |

### Minimal integration fix (3 lines of routing)

1. **Epoch start:** knowledge-delta steps 1–2 (load + claim inventory).
2. **Diverge:** thesis-generator steps 1–5 (state + XDISC + retrodiction + probe).
3. **Close:** knowledge-delta steps 6–10 (evidence → review → commit → RSI) + thesis-generator step 10 (yield).

---

## Stale-prompt audit

| Prompt surface | Stale risk | Evidence |
|----------------|------------|----------|
| Cookbook A4 subagent JSON | High — repeats fiscal frame every cluster mine | `context.md:1605-1619` |
| Cookbook Phase B converge | Medium — no generator-yield or XDISC rows | `context.md:1698-1749` |
| Thesis self-prompt packet | Low — covers cross-discipline + stop-on-no-change | `context.md:390-414`, `context.md:404` |
| Knowledge-delta loop | Medium — no reference to dead_paths or generator registry | `context.md:147-214` |

---

## Bottom line

| Loop | Replace human steering? | Why |
|------|-------------------------|-----|
| Knowledge-delta | **No** | No STOP, no persisted claims, no yield, no XDISC wire-in |
| Thesis-generator | **No** | Lifecycle deferred, count drift, routing conflict, prompts still fiscal-default |
| **Together** | **Partial spec** | Human still needed for: parent dispatch, adoption judge, registry reconcile, XDISC-before-search enforcement |

**Highest-leverage minimal fixes (ordered):**

1. Resolve XDISC timing conflict (`context.md:1867` vs `context.md:438`).
2. Add lifecycle sidecar + reconcile `G-LIF-Q06`/`G-LIF-S15` (`context.md:289`, `context.md:498-514`).
3. Add STOP + dead_paths to knowledge-delta loop (`context.md:213` vs `context.md:486`).
4. Patch cookbook A4 template with self-prompt + dead_paths (`context.md:1605-1619`, `context.md:390-414`).
