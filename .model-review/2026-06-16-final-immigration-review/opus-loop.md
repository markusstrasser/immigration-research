Reviewer C — agent-loop/process review. Closed-book against the packet (no external facts). Files cited by basename: `delta` = `immigration-knowledge-delta-agent-loop-2026-06-16.md`, `audit` = `immigration-thesis-generator-audit-2026-06-16.md`, `cookbook` = `immigration-lifetime-synthesis-diverge-cookbook.md`, `protocol` = `immigration-lifetime-sweep-protocol.md`, `gen` = `immigration-lifetime-fiscal-generators.md`, `fixes` = `immigration-conclusion-audit-running-fixes.md`.

## CONFIRMED findings

**C1 — Four overlapping loop specs, no declared canonical one; the stated ownership split is contradicted by content; the INDEX sweep-route omits two of the four.**
There are four full/partial process loops: `delta:112–178` (10-step), `audit:151–217` (10-step), `cookbook:13–33` (3-phase), `protocol:7–13` (5-step). `audit:5–6` asserts "this memo owns generator and XDISC divergence only" and that `delta` "owns full claim inventory, probe, adversarial review, and commit routing" — but `audit:151–217` then ships a complete load→classify→generate→probe→mine→converge→audit→update→RSI loop, i.e. exactly the steps it disclaims. Compounding it, `INDEX:143` (Quick Start 6, "How do I run the next fiscal/generator sweep?") routes cookbook → audit → fixes and omits both `delta` (the memo whose stated job is the full loop) and `protocol` (the "mandatory post-sweep workflow"). An agent told to "run the loop" cannot mechanically decide which loop. This is the core risk for a system meant to *replace* human steering, and it directly violates the single-definition invariant the project enforces elsewhere.
*Fix:* declare one canonical umbrella loop (`delta:112–178` is the natural one); demote `cookbook`/`protocol`/`audit`-flowchart to named sub-procedures that say "this expands step N of the canonical loop"; rewrite `INDEX:143` to enter the canonical loop first.

**C2 — Provenance-tag taxonomy drift across the two loop docs and the corpus.**
`delta:117` instructs tagging claims `SOURCE / INFERENCE / UNVERIFIED`; `audit:186` instructs `SOURCE / DATA / INFERENCE / FRAMING-SENSITIVE`. The corpus actually applies `SOURCE/DATA/INFERENCE/FRAMING-SENSITIVE/LIMIT` (e.g. `claims-evolution-ledger:25,49,61`) plus a one-off `[DATABASE:]` at `fixes:2521`. Neither loop lists `LIMIT`; `UNVERIFIED` is applied nowhere; `[DATA]` vs `[DATABASE:]` is unreconciled. The loops' own "tag every load-bearing claim" step therefore points at three different vocabularies — the exact tag-drift-across-enforcers failure the project treats as a correctness bug.
*Fix:* single-source the tag set in one file, have both loops reference it rather than re-list, drop orphan `UNVERIFIED`, fold `[DATABASE:]` into `[DATA]`.

**C3 — The two canonical loops disagree on the terminal condition (the "hand back to human" hinge).**
`audit:215`: "STOP after 2 consecutive sweeps with zero adopted outputs." `delta:171–178`: RSI Close → choose next frontier by VOI → REPEAT, with no stop. So on a dry sweep one loop halts and the other switches frontier and continues indefinitely. For a loop whose thesis is "replace constant human steering," when the human re-enters is undefined.
*Fix:* reconcile to a two-level rule — dry sweep ⇒ switch frontier (`delta`); K dry frontier-switches or budget cap ⇒ stop and escalate to human (`audit`).

**C4 — The RSI/yield-accounting step is non-executable as written; it depends on state the audit explicitly defers.**
Both loops' step 10 (`delta:171–176`; `audit:208–215`) require per-generator fired/adopted/dry/retire state and a separate adoption judge. But `audit:53` states there is "no machine-readable state," `audit:210` requires adoption be "judged by a separate pass … not the generator author alone" (unbuilt), and `audit:268` defers the "DuckDB lifecycle migration … it needs a build-path change, not prose-only edits." The self-correction mechanism that would let the loop run unsupervised is precisely the deferred part, yet both flowcharts present it as a live step.
*Fix:* mark step 10 as "not yet operational — manual until lifecycle sidecar lands" in both flowcharts; don't describe the loop as autonomous until the schema at `audit:225–244` exists.

**C5 — Stale auto-generated knowledge-index footers in `immigration-INDEX.md` and `CYCLE.md`.**
`INDEX:145–150` is stamped `generated: 2026-04-19`, `table_claims: 97`, `hash: 25555c17344c`, but the file carries 2026-06-16 rows (`INDEX:21,46,54,55,56,82`). `CYCLE.md:47–52` is likewise stamped `2026-04-19`, yet `CYCLE.md:29` carries the June-16 E-Verify nonsignificance edit (`t=-1.40, p≈0.16`). Any regenerator or consumer trusting those stamps/counts will mis-state coverage — a stale-route risk the loop's own "Narrative / grepable stale phrase" frontier (`delta:195`) is supposed to catch.
*Fix:* regenerate both footers (or delete them if no tool consumes them).

**C6 — Generator-registry header label is stale.** `gen:4` titles the file "(rounds A–P)" while `gen:6` adds clusters Q,R,S (19 clusters). Trivial but it's the precise "grepable stale label in a routing surface" the loop claims to remove.
*Fix:* "(rounds A–S)".

**C7 — "Replace constant human steering" overclaims relative to the memos' own admissions.**
`delta:197` declares "The agent replaces constant human steering by forcing every cycle through this table"; `audit:149` says the loop must "mechanize those jobs." But the same memos concede the human-dependent parts remain: `audit:34` (missing non-fiscal generators and the cross-disciplinary self-prompt — i.e. the divergence axes a human supplied); `audit:210` (adoption needs a separate judge); `audit:212` ("if a human correction repeats, turn it into a generator…" presumes human corrections still arrive); `delta:82,209` (every finding "needs local verification," "accept nothing from reviewers without repo/data evidence"). The defensible claim is mechanizing the *cadence* and capturing *recurrence*, not replacing the steering.
*Fix:* scope the claim — "mechanizes the divergence/convergence cadence and converts recurring corrections into guards; net-new search axes and adoption judgment remain human / separate-pass." Apply at `delta:3,197` and `audit:147–149`.

## Speculative / preferences

**S1 — Divergence budget is internally contradictory.** `delta:135,205` require "5+" kill paths (no ceiling); `audit:168` caps "at most 8 generators/sweep"; `audit:170` then mandates "DS-01 on every load-bearing number," which alone can exceed 8. Reader can't tell generator-*type* from *invocation*. *Fix:* state the cap in types, exempt blocking checks (DS-01/DS-02) from it.

**S2 — "Next concrete run" presupposes deferred infrastructure.** `audit:246–252` tells the next agent to run XDISC-URB/PE/PSY/etc., but those are "not yet loaded" (`audit:59`), partly source-unverified (`audit:270`), and the lifecycle table they'd be scored in is deferred (`audit:223,268`). *Fix:* prefix the run-list with the prerequisite ("load net-new XDISC behind the dedup gate + stand up the sidecar first").

**S3 — Load-bearing federal scalar travels without its scope.** `~$1,519/adult/yr` recurs at `delta:33,91` and `mexico-npv:38,91,118` labeled only "federal annual proxy," while its real definition (payroll/FICA minus SNAP/TANF/SSI, *not* income tax/Medicare/EITC/all-government) lives at `fixes:2498`. By the loop's own "no scalar export" frontier (`delta:189–190`) the scope tag should ride with the number. *Fix:* attach the payroll-minus-3-transfers scope wherever the figure appears.

**S4 — "epoch" vs "sweep" never distinguished.** `INDEX:56`/`delta` route by "research epoch"; `INDEX:143`/`cookbook`/`protocol` route by "sweep." Same loop family, two undefined nouns — feeds the C1 routing ambiguity. *Fix:* define one as the outer unit and the other as the inner, once.

## Verified consistent (do not "fix")
The load-bearing scalars are numerically coherent across surfaces — `436,819` / `322,539.5` / `8,496,334` / `$1,519` / `+$45,631` / `+$387.7B` / `t=-1.40, p≈0.16` / `+2.4pp` agree across `delta:26–55`, `mexico-npv`, `fixes`, and `CYCLE.md:29`. The convergence/cleanup pass achieved cross-surface consistency on these; the residual issues above are loop-design and routing, not number drift.

---
Out-of-scope housekeeping (one line): the SessionStart hook reports a peer `claude` session sharing this checkout — since the review packet dir is untracked and main is ahead 156, isolate before committing anything to avoid mis-stamped commits.
