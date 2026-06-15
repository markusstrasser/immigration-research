# /improve maintain — tick report (2026-06-15)

Run inline (not subagent: 15/15 claude-process ceiling blocked Agent spawn; Tier-2 dispatch
also gated off by the loop's own `CLAUDE_PROCS >= 5` rule).

## SWEEP (health visibility)
- `just hooks-smoke`: **green** — `intentional_block=1, pass=250`, exit 0. No silently-dead hooks.
- DB freshness (from live-state preamble): ClinVar 44d, gnomAD 44d (>30d → stale flag; both are
  genomics-repo, not research-repo concerns).

## What the loop found — 67 ranked cross-repo priorities (headline output)

Top tier (the actionable picks):
| # | Class | Item | Repo |
|---|-------|------|------|
| 1 | broken-tool | Recurring missing-dep failures, 17 modules, 222 fails/8d (duckdb, edgar, PIL, numpy…) | fleet |
| 2 | broken-tool | `remove-ai-watermarks` CLI — missing `remove_ai_watermarks.cli` (4 fails/1d) | skills |
| 3–5 | broken-tool | `corpus` CLI — missing `weasyprint`, `modal`, `corpus_core.cli` | skills/corpus |
| 6 | doctor | `test-health:phenome` — suite timeout, did not complete | phenome |
| 7 | open-finding | SHADOW risky-diff-review probe — promote/cut ~2026-06-21 | agent-infra |
| 8–56 | open-finding | 49 behavioral/infra findings (mostly subagent-discipline, hook-FP, dead-infra) | fleet |
| 57 | doctor | `global:orphan-generators` — `commit_gateway.py` candidate orphan | agent-infra |
| 58–66 | stale-plan | 9 plans untouched 7–14d (genomic-phenotype-linking, rsi-loop-closure, …) | agent-infra |

Full list: `cd ~/Projects/agent-infra && uv run python3 scripts/top_priorities.py --top 67`.

[obs] 2026-06-15 — /rsi close VERIFIED: `top_priorities.py --top 67` → 67 items, class
breakdown {open-finding:50, stale-plan:10, broken-tool:5, doctor:2}; grep for
research-content tokens (citation|disconfirm|falsif|unsourced|IQ sex|immigration|steel-man|
framing-sensitive) = **0 hits**. The RSI loop, run from the research repo, has zero input
channels onto the repo's terminal objective (claims→truth). Input-coverage gap, not a
ranking bug — confirms M1 (proxy-only anchor) at the input boundary.

## The pick + routing
**Pick:** broken-tool cluster (#1–6) is the highest-leverage actionable tier.
**Routing verdict:** ROUTE, do not execute this tick. Reasons:
1. All top actionable items are **shared-infra in OTHER repos** (skills/corpus, phenome,
   agent-infra) — boundary-crossing relative to this research-repo session; not safe to blind-fix.
2. **15/15 process ceiling** — the loop's own rate-limit gate forbids dispatch; blind dep-installs
   into the wrong venv at saturation is exactly the failure mode to avoid.
3. The missing-dep cluster (#1) is already partially guarded (bare/uvx-python guard since 2026-06-14);
   residual is uv-run-missing-dep + wrong-cwd — needs per-module diagnosis, not a sweep fix.

**Action taken:** none (route-only tick). Headline digest is the deliverable; broken-tool tier
should be planned in agent-infra/skills, not patched from here.

## What the sweep STRUCTURALLY did NOT cover
This is the load-bearing observation, expanded in the /leverage missing pass below: **every one of
the 67 items is infra/tooling/behavioral. ZERO concern the research-repo's actual subject matter**
(IQ sex differences, immigration findings — unsourced claims, stale citations, disconfirmation gaps,
cross-memo contradictions, instrument bias). The loop is an infra conductor pointed at agent-infra;
run from a research repo it is blind to the thing the research repo exists to do.
