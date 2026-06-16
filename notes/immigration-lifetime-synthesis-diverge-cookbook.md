# Synthesis ↔ Diverge cookbook (immigration lifetime fiscal)

**Purpose:** Reusable prompt template for the loop that worked in rounds 1–10: **diverge** (data + generators + angles) → **converge** (unified theory + formal multi-model critique) → repeat with a sharper thesis.

**Instance memos:** `research/immigration-lifetime-unified-theory-2026-06-15.md`, `notes/immigration-lifetime-sweep-protocol.md`

**Principle:** Data does not automatically kill a good explanation — it kills bad **scalar exports** and unnamed **layer laundering**. Synthesis names the object; divergence hunts what the current frame excludes.

---

## The loop (one sweep)

```
┌─────────────────────────────────────────────────────────────┐
│  CARRY: prior thesis burst + generator menu + DuckDB state  │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  DIVERGE (expand surface)                                   │
│  1. Denial cascade / constraint inversion brainstorm        │
│  2. Probe URLs → setup-lifetime.sh → rebuild warehouse      │
│  3. Parallel mine clusters → .mining/*.json → generators MD │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  CONVERGE (sharpen thesis)                                  │
│  4. Unified theory (central object, 3-sentence thesis)      │
│  5. Five formal models + critique matrix                      │
│  6. Thesis burst (revise in place) + 3 disconfirmation hunts  │
└───────────────────────────┬─────────────────────────────────┘
                            ▼
                    next sweep (N+1)
```

**Rule:** Never start diverge round N+1 until converge for round N is written.

---

## Non-negotiables (immigration fiscal instance)

| Do | Don't |
|----|-------|
| Model **education × arrival × state × legal path × time × ledger layer** | Publish "Mexican lifetime NPV" |
| Tag every load-bearing number: DuckDB table or `[SOURCE:]` | Float claims from paper memory |
| Separate **federal annual**, **lifetime NPV**, **local episodic** | Prove layer A → conclude layer B |
| Mine **generators** (mechanical prompts + retrodiction) | Mine only parameter lists |
| Steel-man each model before killing it | Debate authors |

**Central object (template):**

```
cell  = {dimensions of the population slice}
layer = {which ledger: federal_annual | lifetime_npv | state_local | local_episodic | private_transfer | admin}
sign  = F(cell, layer, t)   # often opposite-signed across layer
```

---

## Phase A — Diverge procedure

### A1. Brainstorm perturbation (15 min, in-conversation)

Run three passes; write bullets to sweep memo (`research/immigration-lifetime-dataset-brainstorm-*.md`):

1. **Denial cascade** — "If microdata never arrives, what still bounds the answer?"
2. **Domain forcing** — map domains (demography, labor, housing, health, legal, admin) → dataset → lifetime lever
3. **Constraint inversion** — "What if we only had aggregates / only had annual / only had local?"

Output: 8–12 **angles**, each with: what it bounds, what it cannot say, acquire path (automated / copy / manual).

### A2. URL probe batch (script, not hope)

```bash
# Pattern: curl first 120KB, pdftotext page 1, grep immigration keywords
# Keep only if title matches; skip NBER ID fishing without title check
```

Add winners to `infra/immigration-fiscal/acquire/setup-lifetime.sh` + `DOWNLOAD_MANIFEST.tsv`.

**Copy layer:** derived CSVs, admin PDFs, and sibling-stack files often beat new PDF hunts.

### A3. Acquire + warehouse

```bash
cd infra/immigration-fiscal && bash acquire/setup-lifetime.sh
bash rebuild_lifetime_warehouse.sh   # loads .mining/*.json into DuckDB
```

### A4. Parallel mine (subagent prompt template)

Dispatch **3–4 clusters** per sweep (not one mega-agent). Each cluster = 3–8 sources max.

```
You are mining corpus cluster {CLUSTER_ID} for lifetime fiscal immigration research.

**Frame (non-negotiable):**
- No scalar "Mexican lifetime NPV."
- Model: education_bucket × age_at_arrival × state × legal_status_path × descendants.
- Distinguish ledger layers: federal_annual vs lifetime_npv vs local_episodic.

**Sources (read with pdftotext / pandas for CSV):**
{LIST_PATHS}

**Cross-read:** research/immigration-lifetime-unified-theory-2026-06-15.md (current thesis)
**Avoid duplicating generators in:** research/immigration-lifetime-fiscal-generators.md

**Output JSON:** research/.mining/immigration-lifetime-cluster-{slug}.json

{
  "cluster": "{CLUSTER_NAME}",
  "mined_at": "YYYY-MM-DD",
  "parameter_claims": [
    {
      "claim_id": "X-001",
      "source_rel_path": "external/lifetime/...",
      "parameter_name": "...",
      "value_numeric": null,
      "unit": "...",
      "population": "...",
      "unnamed_assumption": true,
      "page_ref": "pdftotext p.N",
      "notes": "..."
    }
  ],
  "generators": [
    {
      "id": "G-LIF-{X}01",
      "name": "...",
      "prompt": "Mechanical question an agent can run without creativity...",
      "retrodiction": "Would have surfaced findings A and B before we had them because...",
      "negative_space": "What the standing frame excludes",
      "unnamed_assumptions_surfaced": ["..."],
      "topics": ["..."],
      "source_rel_paths": ["..."]
    }
  ],
  "theories_tested": [
    {
      "theory": "...",
      "prediction": "...",
      "duckdb_test": "SQL against life.* or ctx.* tables",
      "falsifier": "..."
    }
  ]
}

**Targets per cluster:** 6–10 claims, 4–5 generators (retrodiction required), 3 theories with SQL.
Return brief summary only.
```

**Cluster menu (reuse / extend):**

| ID | Theme | Example sources |
|----|-------|-----------------|
| A | NPV / generational / NAS critique | NAS, Clemens, Colas-Sachs, Lee-Miller |
| B | Labor / Mariel / wages | Borjas, Card, Peri, Foged-Peri |
| C | Local / welfare / capacity | CBO 61256, Gould, magnets, crime |
| D | Composition / descendants | Hanson, Abramitzky, Duncan-Trejo |
| E | Housing / Saiz | elasticity .dta, FRBSF, VMT |
| F | High-skill / H-1B | Bound w23153, Ottaviano w12497 |
| G | Legal / tax floor | ITEP, Pew, border enforcement |
| H | Refugee / mortality | IZA refugee, CDC life tables |
| I | Return migration | Duleep-Regets IZA |
| J | Admin / enforcement | CBP/ICE budgets, LPR xlsx |
| K | Incidence bridge | stage2/5 derived CSVs |
| L | OECD / health bridge | Ortega-Peri, MEPS cells |

After mining: rebuild DuckDB, regenerate `research/immigration-lifetime-fiscal-generators.md`.

### A5. Generator quality gate

From `leverage/references/generators.md`:

1. **Cluster** miss-patterns into abstract moves (not one generator per paper).
2. **Retrodiction:** each generator must retrodict ≥2 prior findings.
3. **Negative space:** name what the frame excludes.
4. **Consumption:** every generator links to DuckDB test or explicit data gap.
5. **Retire** generators that cycle twice with zero adopted output.

---

## Phase B — Converge procedure (synthesis prompt)

Run **after** diverge, **before** next downloads. Paste into main agent or dedicated synthesis pass.

```
You are writing the post-sweep CONVERGE pass for immigration lifetime fiscal research.

**Read first:**
- research/immigration-lifetime-unified-theory-2026-06-15.md (prior thesis burst)
- research/immigration-lifetime-fiscal-generators.md (new generators)
- Query DuckDB:
  ATTACH 'warehouse/immigration_context.duckdb' AS ctx (READ_ONLY);
  ATTACH 'warehouse/immigration_lifetime_evidence.duckdb' AS life (READ_ONLY);
  -- key tables: origin_fiscal_scenario_2023, npv_education_benchmarks,
  -- acs_foreign_born_education_bucket_totals_2023, parameter_claims, lifetime_generators

**Write / update:** research/immigration-lifetime-unified-theory-2026-06-15.md

## I. Unified theory
- Name the central object (tensor / cell × layer × time — NOT a scalar).
- 3-sentence thesis: what is compatible, what only looks contradictory, why politics fights over layers.
- Table: layer → best instrument → what it is NOT.
- Verifiable anchors table (number | value | DuckDB/SOURCE).

## II. Five formal models
For M1–M5 (mechanisms, not authors):
- Grammar (ledger rules)
- Core prediction
- Falsifiers
- Unnamed assumptions
- Data status (strong / medium / gap)

Use the five-model menu unless the sweep surfaced a better split:
  M1 NAS accountant | M2 GE offset | M3 Local incidence | M4 Borjas pessimist | M5 Dynamic composition

## III. Cross-model critique matrix
Rows = questions (lifetime sign, annual federal, rent, shelter, descendants).
Columns = M1–M5.
Mark irreconcilables as frame fights vs data fights.
State explicitly: "What data cannot kill" (coherent stories in wrong layer).

## IV. Disconfirmation
Three active hunts that would flip thesis sign on some layer.

## V. Thesis burst
Paste prior sweep thesis verbatim, then revise in place:
- Sharper than last sweep
- Killed
- Survived despite weak data

## Revisions table
| Date | Sweep | What changed and why |

**Constitution tags:** [SOURCE:] [INFERENCE] [FRAMING-SENSITIVE] on load-bearing claims.
**Quant gate:** notes/quant-bias-checklist.md for numbers doing argumentative work.
```

---

## Phase B2 — Five-model critique (standalone mini-prompt)

Use when you only need formal adversarial structure without full memo rewrite.

```
Given thesis T and datasets D, produce five MECHANISM models (not people):

For each model Mi:
1. State variables and ledger (what enters the sum)
2. Prediction for cell = <HS, recent arrival, Mexico-weighted> on layers {federal_annual, lifetime_npv, local}
3. One empirical fact from D that supports Mi
4. One fact from D that threatens Mi
5. One unnamed assumption Mi smuggles in

Then:
- 5×5 matrix: models vs {lifetime, annual, local, housing, descendants}
- List disagreements that are DATA-resolvable vs FRAME-resolvable
- One paragraph: "Data cannot kill X because ..."

Do not pick a winner. Name what each model is for.
```

---

## Phase B3 — Thesis burst (carry-forward template)

Paste at top of `## V. Thesis burst` every sweep:

```markdown
### Sweep {N-1} thesis (verbatim)
> {paste previous 3 sentences}

### Sweep {N} revision
> {new 3 sentences}

**Sharper:** ...
**Killed:** ...
**Survived (weak data):** ...
**New falsifier:** ...
```

---

## Artifact checklist (per sweep)

| Artifact | Path | Done? |
|----------|------|-------|
| Brainstorm angles | `research/immigration-lifetime-dataset-brainstorm-*.md` | ☐ |
| Manifest rows | `infra/immigration-fiscal/DOWNLOAD_MANIFEST.tsv` | ☐ |
| Staged files | `external/lifetime/` | ☐ |
| Mining JSON | `research/.mining/immigration-lifetime-cluster-*.json` | ☐ |
| Generators registry | `research/immigration-lifetime-fiscal-generators.md` | ☐ |
| DuckDB rebuild | `bash rebuild_lifetime_warehouse.sh` | ☐ |
| **Unified theory** | `research/immigration-lifetime-unified-theory-*.md` | ☐ |
| Index row | `research/immigration-INDEX.md` | ☐ |

---

## Anti-patterns (learned the hard way)

| Anti-pattern | Fix |
|--------------|-----|
| NBER ID fishing without `pdftotext` title check | Probe → title → then acquire |
| Scalar "Mexico NPV" | Composition weights on education cells only |
| Download without synthesis | Converge memo before round N+1 |
| Generators without retrodiction | Reject; cluster into abstract moves |
| Wage paper → fiscal verdict | Generator: "wage effect ≠ fiscal effect" |
| Layer laundering | Matrix: which layer each model owns |
| Ignoring unit bugs ($21 per-pupil) | Incidence-bridge generator + disconfirmation hunt |
| One mega subagent for all PDFs | 3–4 clusters × 4–5 generators |

---

## One-liner prompts (quick invoke)

| Intent | Prompt |
|--------|--------|
| Full sweep diverge | `brainstorm more angles → probe → acquire → mine 4 clusters → rebuild DuckDB` |
| Full sweep converge | `run converge pass per notes/immigration-lifetime-synthesis-diverge-cookbook.md Phase B` |
| Generators only | `mine cluster {X}; retrodiction-test; append to generators MD` |
| Theory only | `update unified theory + 5 models; thesis burst; 3 falsifiers` |
| Negative space | `what layer is the current thesis silently exporting? name 5 unnamed assumptions` |

---

## Adapting to other topics

Replace:

- `cell` dimensions (e.g. genotype × tissue × time for bio)
- `layer` ledgers (e.g. molecular vs clinical vs population)
- Five-model menu (mechanisms native to the field)
- DuckDB attach paths
- Cluster source lists

Keep the **loop order**: diverge → converge → repeat. The fruitful part was never volume alone — it was **synthesis forcing the thesis to get sharper while divergence hunted what the thesis could not yet see**.
