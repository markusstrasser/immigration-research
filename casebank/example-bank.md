# Example bank — plan-premise defects (illustrative)

> Shape demo only; cases quoted verbatim from `evals/critique_replay/cases.md`. A real research bank
> collects cases from its own domain (immigration, IQ, …).

## Cases

**C5 — phantom join** · `capture: reconstructed` · `[SOURCE: evals/critique_replay/cases.md]`
> substrate-closure plan §5.4 proposed compile-gate aggregation "via produces_refs"; that field indexes
> reference databases, not claims — the join doesn't exist. Gold: the named join field cannot join the
> named entities.

Payload: a plan asserts a join over a field whose real semantics don't support it.

**C6 — dead conversion target** · `capture: reconstructed` · `[SOURCE: evals/critique_replay/cases.md]`
> evo behavior-tables plan proposed converting `:smart-split`'s 8 variants; its only references were its
> own plugin + docstring examples — the real dispatch was `:context-aware-enter`. Gold: the conversion
> target has zero production dispatch sites; the plan should be "delete", not "convert".

Payload: a plan proposes work on code whose only "callers" are self-references.

## Induced principles

**P1 — a plan asserts a world-state the primary source contradicts.** In both cases the plan's claim (a
join exists / a function is live) is false against the actual schema / dispatch table. Compresses C5 + C6
— and predicts C1 (a gate-claim that doesn't reproduce) and C2 (an inventory count that's wrong) in the
source bank are the *same shape*. Detection rule: check the **primary artifact**, name the contradiction.
**Invention-trap (the seductive wrong read): accept the plan's frame** — estimate effort for
impossible/dead work instead of rejecting the premise.

- Falsifiable prediction: a reviewer given only the plan packet (no repo access) misses these ~half the
  time; one told "verify every asserted join/dispatch against the schema" catches them. (Borne out: C6
  was missed by 3 packet-only reviewers, caught by the repo-access axis.)

## Revisions
- 2026-06-15 — created (illustrative; C5 + C6 → P1).
