# Immigration lifetime fiscal — sweep protocol

**Purpose:** After every acquisition/mining sweep (round N), force synthesis before the next download burst. Data does not automatically kill good explanations — but unexplained predictions should.

**Full prompt templates:** `notes/immigration-lifetime-synthesis-diverge-cookbook.md`

## After each sweep (mandatory order)

1. **Unified theory** — one memo section answering: *What is the single best story that holds all layers together?* Name the central object (not a scalar), the dimensions, what is compatible vs contradictory, and the current thesis in ≤3 sentences.
2. **Five-model formal critique** — state five competing models (not authors — *mechanisms*). For each: core equation/ledger, predictions, data that would falsify, unnamed assumptions exposed.
3. **Thesis burst (carry-forward)** — paste the prior sweep's thesis; revise it in place. Mark what got sharper, what got killed, what survived despite weak data.
4. **Disconfirmation pass** — three active hunts for evidence that would flip the thesis sign on any layer.
5. **Only then** — run `research/immigration-thesis-generator-audit-2026-06-16.md` XDISC packet, then brainstorm round N+1 downloads, generators, DuckDB loads.

## Output locations

| Artifact | Path |
|----------|------|
| Living unified theory + 5 models | `research/immigration-lifetime-unified-theory-YYYY-MM-DD.md` (update in place; add `## Revisions` at bottom per sweep) |
| Generators / claims | `research/.mining/` → DuckDB rebuild |
| Sweep brainstorm | `research/immigration-lifetime-dataset-brainstorm-*.md` |

## Central object (do not collapse)

**Fiscal incidence tensor** — not "Mexican lifetime NPV."

```
(cell) = education_bucket × age_at_arrival × state/PUMA × legal_status_path × cohort_time
(layer) = federal_annual | lifetime_npv | state_local_flow | local_episodic | private_transfer | admin_enforcement
```

Mexico enters only as **ACS composition weights** on cells, never as a single number.

## Five-model menu (reuse every sweep)

| Model | Mechanism | Typical sign for `<HS` recent surge |
|-------|-----------|--------------------------------------|
| **M1 NAS accountant** | Education-age lifetime NPV; public goods excluded | Negative individual NPV |
| **M2 GE offset** | Capital tax + labor complementarity + indirect fiscal | Positive or flipped NPV |
| **M3 Local incidence** | Inelastic housing + schools + shelter episodics | Negative local / renter welfare |
| **M4 Borjas pessimist** | Substitution, welfare assimilation, spatial attenuation | Negative wages → negative fiscal |
| **M5 Dynamic composition** | Time-varying weights, return migration, legal-status selection | Sign depends on horizon & attrition |

Critique = where these agree, where they talk past each other, and which disagreements are **data-resolvable** vs **frame-resolvable**.

## Quant gate

Before committing numbers in the unified theory memo: load-bearing figures must cite DuckDB table or `[SOURCE:]` tag. See `notes/quant-bias-checklist.md`.
