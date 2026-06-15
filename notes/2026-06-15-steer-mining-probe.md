# Steer-mining probe — Cursor/Composer 2.5 over the transcript corpus (2026-06-15)

**$5 budget probe.** Can a cheap parallel agent (Composer 2.5) mine the full Claude Code
transcript corpus for Markus's steers + related interaction signals, cheaply and correctly?
**Yes.** Scaffold + raw data in `/tmp/steer-trial/` (scratch — promote if kept).

## Method
`mine_steers.py`: extract transcript (collapse tool noise) → **free human-turn pre-filter** (skip
sessions with <2 user-prose turns) → Composer 2.5 ask-mode (parallel) → JSONL signals → **scanned
ledger** keyed by `(vendor, session_id)` for idempotent/incremental re-runs. Source of truth for the
session universe: `~/.claude/agentlogs.db`.

## Cost (corrected — my early ~$0.02/session estimate was 4× low)
- Real interactive sessions are big → **~$0.085/session** (Composer $0.50/M in, $2.50/M out; cacheRead
  billed at full input rate = conservative).
- This probe: **$4.77 total**, ~50 sessions scanned across 2 stages.
- Full interactive backfill (~400 billable of 581 May–Jun claude sessions) ≈ **~$35**, ~40 min.
- Incremental (per new session, continuous hook) ≈ **$0.085** — pennies/day.
- 6 parallel workers overshoot the budget cap by ~$0.5–0.8 (in-flight calls); use ≤3 workers or a
  lower cap. The hard cap held both runs under $5.

## Coverage / corpus shape
- Interactive claude sessions are **May–June only, 581 total** (149 May, 432 June). ~30% of sampled
  sessions are autonomous (no human) → skipped free by the pre-filter.
- **Early-vs-late: inconclusive at this N.** Stage 1 (steers-only) hinted May denser (7.05 vs 5.64
  steers/session); Stage 2 (all-signal, n=5 June) reversed it. Both periods very dense; no reliable
  trend — don't claim one.

## Three signal streams (one read, ~free marginal per extra extraction)
| Stream | Yield (n=17 multi) | Feeds |
|---|---|---|
| **steers** | 98 (~5.8/sess) | preference vectors → GOALS |
| **agent_miss** | 94 (~5.5/sess) | `/observe` anti-patterns + **which hooks to build** |
| **confirmation** | 21 | the **+** preference signal + the autonomy *boundary* |

## Induced preference vectors (steers, clustered; ✓ already in CLAUDE.md, ★ GOALS candidate)
1. ✓ Autonomy by default — act on obvious/reversible steps, own judgment calls, no permission menus.
2. ★ **Durable/systemic only** — root-cause, high-leverage; reject band-aids, nagware, noise. (Dominant at session-closeout.)
3. ✓ Full scope, no partial / no top-N triage.
4. ✓ Verify against primary source before asserting; provenance-tag; "done" = verified.
5. ✓ Adversarial cross-model critique before consequential builds.
6. ✓ Break & single-source; delete legacy, no compat cruft.
7. ✓ Terse, decision-first output; name failure modes; calibrate to audience.
8. ★ **Bias to execution; stop deferring** behind probe-first/offer-mode.
9. ✓ Tier compute by stakes; frontier default for core decisions.
10. ★ **Agent-agnostic** (Codex/llmx-accessible), long-term ergonomics.

**Headline:** clustered steers reproduce **~80% of CLAUDE.md from behavior alone.** Confirmations
independently re-confirm the same vectors AND sharpen the autonomy *boundary* — "autonomous EXCEPT
expensive/irreversible" (e.g. "explicit approval required before expensive Modal dispatch", "citation-
verify before registry mutation").

## agent_miss → violated-rule map (the highest-value new signal)
The misses cluster onto *existing* CLAUDE.md rules being violated in practice — i.e. rules that need
**hook enforcement**, not more prose (the pair-rule, now data-driven):
- claimed completion without verification → **verify-before-claim** (rules 10/12)
- edited from a stale model / announced fix without reading file top → **read-before-edit** (17)
- trial-and-error on blocked channels vs simplest route → **probe-before-build** (8)
- brute-forced past guardrails → **acknowledge-guardrails-don't-route-around** (18)
- attempted Write before preflighting against hooks → **write-preflight**
- anchored on recent artifact without checking other repo → **inventory-before-dispatch**

A full backfill gives per-rule violation *frequencies* → ranks which hooks to build first.

## Placement / fit (proposed)
- **Reactor** (the miner) = `/observe`-family: a full-corpus, multi-signal miner that the recent-window
  `/observe` structurally can't be → `skills/observe/scripts/`. Its state is `agentlogs.db` + the ledger.
- **Outputs:** raw `signals.jsonl` (rederivable machine output) → induced **`preferences.md`** (GOALS
  candidates, human-gated) · agent_miss → `/observe failures` + hook proposals · confirmations → preference **+**.
- **The integrating insight:** one full-corpus pass is an **empirical audit of the constitution** —
  steer-clusters = revealed preferences (→ GOALS), agent_miss = rules violated despite being written
  (→ hooks), CLAUDE.md rules with zero steers = possibly dead/over-cautious. It front-ends GOALS, the
  hook fleet, `/observe`, and the case bank from ONE read instead of each tool's incomplete window.

## Next (human-gated where noted)
- Promote scaffold `/tmp/steer-trial/mine_steers.py` → `skills/observe/scripts/` if keeping.
- Propose the ★ vectors (#2, #8, #10) to **GOALS.md** (human-gated — not auto-written).
- Full ~$35 backfill → ranked hook candidates from agent_miss frequencies.
