## Integration review — immigration thesis-generator audit bundle

### Critical

**1. Running-fixes ledger missing from index**  
`immigration-conclusion-audit-running-fixes.md` is cited by the audit memo, XDISC-DS-02, and many memo `## Revisions` entries, but has **no** `immigration-INDEX.md` row. The June 16 running-fixes entry claims the index was updated; that update omitted the ledger itself.

**Patch — `research/immigration-INDEX.md` after Core State `immigration-verification-handoff.md`:**
```markdown
| `immigration-conclusion-audit-running-fixes.md` | Live overclaim/denominator/layer fix ledger | Auditing conclusions, applying XDISC-DS-02, checking what changed on 2026-06-16 |
```

**2. Knowledge-delta memo missing from index; audit cites it without path**  
Audit §“Two-day knowledge delta” names a “knowledge-delta agent loop memo” but never links `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`. That file exists and overlaps the audit flowchart but is unrouted.

**Patch — audit line 23:**
```markdown
...a knowledge-delta agent loop memo. [SOURCE: `research/immigration-knowledge-delta-agent-loop-2026-06-16.md`] ...
```

**Patch — index after thesis-generator row:**
```markdown
| `immigration-knowledge-delta-agent-loop-2026-06-16.md` | Two-day delta + parent-controlled agent loop (claim inventory → probe → converge → review) | Starting a full immigration research epoch; pairing with generator audit |
```

**3. Generator count drift is real and now identifiable**  
Verified: Markdown **106** `G-LIF-*` headings; DuckDB **104** rows; **19** clusters. Missing from DuckDB only: **`G-LIF-Q06`**, **`G-LIF-S15`**. Docs correctly flag mismatch but don’t name the delta IDs—blocks automated yield scoring.

**Patch — `research/immigration-lifetime-fiscal-generators.md` line 6:**
```markdown
Count reconciliation pending: Markdown 106 `G-LIF-*` headings; DuckDB 104 rows. MD-only: `G-LIF-Q06`, `G-LIF-S15` (rebuild warehouse or retire from MD).
```

**Patch — audit ground-inventory row:** add “MD-only: Q06, S15”.

---

### High

**4. Broken path: `leverage/references/generators.md`**  
Cookbook A5 cites `leverage/references/generators.md`; no such path under the research repo. Canonical file: `~/Projects/skills/leverage/references/generators.md`.

**Patch — cookbook line 172:**
```markdown
From `~/Projects/skills/leverage/references/generators.md` (symlinked skills):
```

**5. Stale `179` parameter-claims count**  
Header says 179 claims; DuckDB `parameter_claims` = **563**. Index/generators header understates warehouse by ~3×.

**Patch — generators header:**
```markdown
**Totals:** 563 parameter_claims (DuckDB), 106 `G-LIF-*` headings / 104 DuckDB generator rows (Q06, S15 MD-only), 19 clusters.
```

**6. Two parallel agent loops, no hierarchy**  
`immigration-knowledge-delta-agent-loop-2026-06-16.md` (10-step claim/review loop) and `immigration-thesis-generator-audit-2026-06-16.md` (10-step generator loop) duplicate “human did three jobs” framing without cross-links. Agents may pick the wrong loop.

**Patch — audit after Purpose:**
```markdown
**Companion loop (broader):** `research/immigration-knowledge-delta-agent-loop-2026-06-16.md` — use for claim inventory, adversarial review, commits. This memo owns generator/XDISC divergence only.
```

**Patch — knowledge-delta §3 before flowchart:**
```markdown
**Generator divergence:** before step 4, run `research/immigration-thesis-generator-audit-2026-06-16.md` XDISC packet.
```

**7. Cookbook incomplete vs its own June 16 integration**  
Instance memos list thesis audit; artifact checklist does not. No `running-fixes` row. Sweep protocol (`notes/immigration-lifetime-sweep-protocol.md`) still ends at “generators, DuckDB loads” with no XDISC step.

**Patch — cookbook artifact table, add rows:**
```markdown
| Running fixes | `research/immigration-conclusion-audit-running-fixes.md` | ☐ |
| Cross-disciplinary audit | `research/immigration-thesis-generator-audit-2026-06-16.md` | ☐ |
```

**Patch — sweep protocol step 5:**
```markdown
5. **Only then** — run XDISC packet (thesis-generator audit), then brainstorm round N+1 downloads/generators/DuckDB.
```

---

### Medium

**8. Stale repo metadata**  
- `CLAUDE.md` / `AGENTS.md`: immigration file count **32**; `research/immigration-*.md` ≈ **88**.  
- Index `knowledge-index` footer: `table_claims: 12`; index has **~95** file rows.

**Patch — `CLAUDE.md` row:** `| 88 |` (or script-count).  
**Patch — index footer:** `table_claims: 95` + refresh `generated` timestamp.

**9. Ambiguous cookbook path `external/lifetime/`**  
Valid under `infra/immigration-fiscal` (`PNY_DATA_ROOT/external/lifetime`), not repo root.

**Patch — cookbook artifact row:**
```markdown
| Staged files | `infra/immigration-fiscal/external/lifetime/` (from acquire cwd) | ☐ |
```

**10. Orphan `.model-review` packet**  
`.model-review/2026-06-16-immigration-thesis-generator-audit/` exists (git untracked); `cursor-integration.md` and `opus-agent-loop.md` are **empty**. Audit doesn’t link review provenance.

**Patch — audit end:**
```markdown
## Review packet
`.model-review/2026-06-16-immigration-thesis-generator-audit/` — Opus/Cursor lanes; integration notes in `cursor-integration.md`.
```

**11. Quick Start gap**  
No route for “run next immigration sweep.”

**Patch — index Quick Start #6:**
```markdown
6. `How do I run the next fiscal/generator sweep?` Start with `../notes/immigration-lifetime-synthesis-diverge-cookbook.md`, then `immigration-thesis-generator-audit-2026-06-16.md`, then `immigration-conclusion-audit-running-fixes.md`.
```

---

### Low / pre-existing

- Index: restrictionist parse “8 PDFs” vs full-extract “9 papers” — inconsistent, predates this bundle.  
- Running-fixes §2026-06-16 still records “header said 105” — fine as history; current header correctly says `100+`.  
- Thesis audit XDISC table is proposal-only (not in DuckDB)—consistent with implementation note; no bug.

---

### What integrated cleanly

- Index row for `immigration-thesis-generator-audit-2026-06-16.md` in Data Stack.  
- Cookbook one-liner + instance memo for XDISC.  
- Generators header points to audit for reconciliation.  
- Running-fixes documents the generator-widening fix with backlink to audit.  
- Referenced paths (`unified-theory`, `sweep-protocol`, `quant-bias-checklist`, DuckDB warehouse) exist.

**Highest-value next edit:** index the two missing June 16 memos (running-fixes + knowledge-delta), name Q06/S15 in the count reconciliation, fix the broken `generators.md` path.
