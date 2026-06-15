---
id: 2026-06-15-rsi-loop-generality-reconfirm
concept: rsi-outer-loop
repo: research
decision_date: 2026-06-15
recorded_date: 2026-06-15
provenance: contemporaneous
status: accepted
initial_leaning: "Re-raised as 'unify Dreamer/Heretic/dispatch into a clean bunx/uvx CLI surface so any-provider agents share one tool.' Collapsed on reading ground truth: the platform extraction was already run and principal-rejected 2026-06-13; the cross-provider surface (llmx) already exists; anim's 06-15 port confirms rather than reopens."
relations:
  - type: reconfirms
    target: 2026-06-13-rsi-outer-loop-skill   # canonical, in agent-infra/decisions/
  - type: spawns
    target: 2026-06-15-casebank-schema         # the one genuinely-new track (research/casebank/)
---

# 2026-06-15: RSI-loop generality — re-confirm "ship knowledge, not platform" (Dreamer/Heretic are general *concepts*, not a shareable *artifact*)

## Context

Re-raised this session (cross-provider/Bun framing): *"unify llmx + the skills surface; bundle the
Dreamer/Heretic / end-of-session loop into clean `bunx dreamer` / `bunx heretic` tools so any-provider
agents share one CLI instead of each looking at llmx."* Plus: *are Dreamer/Heretic general concepts or
domain-specific per repo?* Plus: build a shared case bank.

The loop-unification half is **the same extraction decided on 2026-06-13** (`agent-infra/decisions/2026-06-13-rsi-outer-loop-skill.md`), now proposed in a different runtime (Bun) and bundled with a transport claim (replace llmx). This entry does NOT re-litigate it — it records the re-raise, answers the general-vs-domain question from the canonical ADR, and checks whether new evidence since 06-13 reopens it. It does not. The case bank is split out as its own track.

## The question asked: general concepts, or domain-specific per repo?

Answered by the canonical ADR (read, not remembered). The split is sharp:

| Layer | Verdict | Evidence |
|---|---|---|
| **The pattern / vocabulary** — proposer→accept-gate→ledger→git-bus→human-gate→schedule; two-role split (Grinder/Dreamer); `BLIND→DIFF→ROTATE→EMIT` audit (Heretic); discovery/irreversible human gate; the autonomy router's intersection | **GENERAL** — recurs verbatim across hutter, anim-workbench, science/research-ops, the `/improve maintain` conductor | ADR "invariant core"; hutter + anim `HERETIC.md`/`OUTER-LOOP.md` are near-isomorphic |
| **The accept-gate / verifier + what it scores** — bit-exact compression (hutter) vs self-golden + real-Manim (anim) vs claim-vs-source synthesis (science) | **DOMAIN-SPECIFIC** and **load-bearing** (the gate, not the proposer, is the spine — PACE arXiv:2606.08106) | ADR Phase-0 reframe; `HERETIC.md` self-dealing analysis |
| **The inner loop** (compression / game / Modal pipeline / synthesis) | **DOMAIN-SPECIFIC**, irreducible | ADR alt #5: a shared `/grind` would be a hollow wrapper |
| **Verifier regime** (clean+cheap / clean+expensive / partial / principal-taste) | **THE MASTER VARIABLE** — *determines whether a standalone autonomous loop is even possible.* Clean → unsupervised auto-ratchet OK. Partial → NO standalone loop; conductor-driven + human-gated. | ADR FINDING 4 |
| **Regime-1-only machinery** (auto-ratchet, parking-lot recombination, pre-registered ΔS bands, clade-yield restart) | **MUST NOT TRAVEL** to partial-verifier repos | ADR §counterevidence; research-ops SKILL warning |

**Why the general concepts still do NOT become a shared artifact** (ADR FINDING 5, the decisive part):
the consumers *already implement the pattern natively in their own prose*; **zero code loads** the
extracted skill (`route.py` + linter have no external callers); the extracted artifact was the *union*
of three loops' rules while the genuine *intersection* is a 2-liner both already have
("boundary-crossing/irreversible/discovery → human; reversible+local+clean-accept → auto"). Union ≠
intersection, no loader → the proven-common ≥2 bar is **not met**. General as a *vocabulary*; not earned
as a *platform*.

## New evidence since 2026-06-13 — does it reopen? No.

1. **anim-workbench ported the loop 2026-06-15** (`evolver/HERETIC.md`,`OUTER-LOOP.md`, `dreamer-tick.ts`,
   `heretic-gate.ts`). It is **partial-verifier** (its own `HERETIC.md`: anim "can fake it, so it needs the
   immune system") → operating-point 3, **no new regime**. It implemented the pattern *in its own prose/TS*,
   loading no shared platform — i.e. it is a 4th instance of exactly what FINDING 5 predicted. **Confirms, not
   reopens.** The resurrection trigger ("a real *second clean-verifier standalone* loop that would load this")
   has **not** fired.
2. **"Replace llmx with a Bun dispatch CLI."** Out of scope of the loop decision and independently wrong:
   llmx *is* the unified cross-provider surface and is actively absorbing providers (cursor + MiniMax this
   week; per-provider schema normalization). The ADR's HELD rebuttal to Gemini applies — the outer loop
   **never embeds runtime transport**; it shells the repo's gate. A Bun rewrite rebuilds the working transport
   layer (rule 19: transport-failure ≠ capability value). No reopening.

## Decision

**Hold the 2026-06-13 verdict: ship the knowledge, not the platform.** No `bunx dreamer/heretic` layer, no
llmx replacement. Dreamer/Heretic/outer-loop are general *concepts* with a domain-specific *gate*; the
durable shared artifacts are already the right ones — `route.py` (the autonomy router, kept as executable
record) + the vocabulary in the ADR + the per-repo native prose. The cross-provider surface is llmx.

**Corrects my own first-pass claim this session** ("finish the outer-loop single-sourcing"): the typed
contract + ledger schema + `SKILL.md` were *deliberately pruned* (ADR FINDING 5), not left half-built —
nothing to finish.

## Evidence
- `agent-infra/decisions/2026-06-13-rsi-outer-loop-skill.md` — canonical ADR, FINDINGS 1–5, cross-lab
  critiqued, principal-approved.
- `~/Projects/skills/outer-loop/README.md` — the de-skilled executable record + resurrection trigger.
- hutter + anim `HERETIC.md` / `OUTER-LOOP.md` — near-isomorphic instances (the generality, primary-source).
- llmx git log (`a91f0f1`,`f6390dc`,`55bb5c3`) — the live unified transport.

## Revisit if
- A repo appears that is genuinely **clean-verifier + standalone** and would *load* shared loop code (the
  ADR's resurrection trigger) — not "it might be reusable."
- A 5th verifier regime appears outside the four operating points.

## Supersedes
Nothing. Stub-of / reconfirms `agent-infra/decisions/2026-06-13-rsi-outer-loop-skill.md` (canonical). The
case-bank track lives separately in `research/casebank/` (the one piece that *was* earned).
