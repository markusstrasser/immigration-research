# Case bank — specific ground-truth cases, not summaries

> **Why this exists.** When agents brainstorm a domain (NASA life-detection, recruitment, fiscal
> impact) and then read the actual papers/datasets, the *specific case examples* are the signal — and
> they are exactly what a summary smooths over. An LLM reasons from cases, not from gists. This store
> is the durable home for those cases: the **verbatim** example + its **provenance** + the
> **payload** (what the case seeds). One entry per line in `cases.jsonl`, append-only.

## The contract (the part to sign off)

A case has three load-bearing parts:

1. **`verbatim`** — the actual excerpt/quote/artifact, preserved. The schema enforces `minLength: 80`
   as an anti-summary guard: a one-line gist is rejected. Store the decisive passage verbatim; point
   to the full source via `provenance.source_ref`.
2. **`provenance`** — `source` (URL / citation / repo-path+commit), `tag` (a **canonical** provenance
   token — see below), `capture` (`verbatim` | `reconstructed`).
3. **`payload`** — what to DO with the case: the lesson, trap, capability, or pattern. This is what
   makes it a *bank* and not an *archive*.

Genre-independent core + a `genre` discriminator + an open `extension` for genre-specific structure.
Genres at v1: `ground-truth-exemplar` (the primary research use), `defect-trap` (eval/detection gold),
`capability-target` (target patterns from an external gold corpus), `failure-mode`, `generator-seed`.

Full field list + validation: `casebank.v1.schema.json` (JSON Schema, draft 2020-12).

## Provenance tags are loaded, not restated

`provenance.tag` is validated against the **canonical** taxonomy at
`~/Projects/skills/references/provenance-tags.md` (enforced regex: `hooks/provenance_tags.re`). `cb.py`
loads that regex at runtime — this file does **not** re-enumerate the tags, by design (single-source
invariant; a copied tag list is the drift bug). Cases may cite a corpus `source_id` in
`provenance.source_ref`, but **a case is not a corpus document** — the corpus stores source bytes;
this stores generative exemplars/traps, often internal-to-our-repos.

## Scope honesty — what this IS and ISN'T (read before promoting)

This is built for **research** (the one consumer with an unmet need — there is no general case home
here today). It is **NOT** a cross-repo substrate platform, on purpose:

- `evals/critique_replay/cases.md` (defect-trap genre) and `anim-workbench/docs/reports/3b1b-reference-bank.md`
  (capability-target genre) are **mature native banks** in their own shapes. Forcing them onto this
  schema is the **union-extraction trap** that the 2026-06-13 RSI-loop ADR was just burned by
  (`agent-infra/decisions/2026-06-13-rsi-outer-loop-skill.md`, FINDING 5: *"run the who-loads-this /
  do-consumers-already-do-it-natively probe at DECIDE-time"*).
- So the schema is written to **substrate/schemas conventions** (SchemaVer, `conformsTo`,
  content-addressed id) so it CAN promote to `substrate/schemas/v1/casebank.v1.json` — but only when a
  **second repo actually adopts the core**. Until then it lives here, research-local. The genres are
  the *intersection* the two existing banks share (verbatim + provenance + payload), not a forced
  superset. **Promotion is earned by a 2nd loader, not assumed.**

## Usage

```bash
# add the worked example cases (idempotent — content-addressed id dedupes)
uv run python3 ~/Projects/research/casebank/cb.py seed

# validate every row against the schema + canonical provenance tags
uv run python3 ~/Projects/research/casebank/cb.py validate

# list what's in the bank
uv run python3 ~/Projects/research/casebank/cb.py list
```

To add a case programmatically: `from cb import add_case; add_case({...})` (computes `case_id`, stamps
`recorded_at`, validates, appends; returns the id, skips if already present).

## Open questions for sign-off
- **Home:** keep research-local (current) vs. promote the *schema* to `substrate/schemas/v1` now (the
  schema is cheap/shareable even if the store isn't). Recommendation: keep local until a 2nd consumer.
- **Genre set:** are the 5 genres right, or collapse to 3 (exemplar / defect / target)?
- **`verbatim` floor:** 80 chars — too low? Too high for terse data cases?
- **Migration:** pull the 7 `evals` defect-traps + the `3b1b` capability rows in now, or leave them
  native and only bank *new* research cases here?
