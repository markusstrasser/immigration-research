# Quantitative Bias Checklist — Project Instance

> Slimmed 2026-06-11 (same session it was created): the 32-item general checklist
> moved to the **research skill** — `~/Projects/skills/research/references/quant-bias-checklist.md` —
> where /research (output gate), /critique verify (rubric), and /analyze (adjunct)
> all load it. This file keeps what is project-specific: the self-audit record and
> the immigration-artifact triggers. Don't re-grow a parallel list here; extend the canonical.

**The compressed rule** (inlined because it gates every commit here): every load-bearing number carries its **ledger, unit, base, window justification, gross-or-net status, and measurement-vs-model-output label**; when several constructions are defensible, the range across constructions is the headline.

## When it fires in this repo

Any commit touching `research/` where a number does argumentative work — especially: fiscal scalars (per-citizen, per-immigrant, aggregate), % changes from surge-era bases, receiver-city costs (gross outlays), TWFE/DiD coefficients promoted to ladder entries, and anything quoting NAS/CBO/Cato/MI/CIS constructions (item 29: provenance tags through every reuse).

## Self-audit record — 2026-06-11 (Cato-dispute mirror test)

Question: did this repo commit the moves the Cato $14.5T study was criticized for? Findings (all fixed via append-only downgrades; checklist item numbers refer to the canonical list):

| # | Repo instance | Item | Status |
|---|---|---|---|
| 1 | CHNV "+787%" graded *strong* while its own memo lists un-adjudicated reverse causation; ladder summary dropped the 2,598/mo base | 8, 25 | Downgraded to medium — ladder entry 30 |
| 2 | "+4.4pp swing implausibly large for non-immigration causes alone" — plausibility assertion over near-collinear Hispanic-realignment confound; controlled estimate +2.4pp, headline used raw +4.41pp | 25, 11 | Retracted as headline language — ladder entry 31 |
| 3 | Deportation calibration headlines "$1.5-2.3T" where $2.32T is the 1.6×-multiplier endpoint | 15, 4 | Presentation rule: lead first-order $1.45T — ladder entry 32 |
| 4 | Receiver-city "~$5B+/yr" is gross city outlays, not net of federal SSP reimbursement or baseline counterfactual | 10 | Scope annotation — ladder entry 33 |

Counter-evidence (moves NOT committed): welfare-weight sensitivity run honestly (open-borders bounds); falsification pass killed our own placebo result; newcomer ratio self-corrected 33x → ~20.5x "contextual, not burden"; scalar verdicts refused at headline level throughout. Directional spread of findings 1-4: two flatter restriction, one cuts against it, one neutral-sloppy — residual bias is **favorable-construction drift per claim**, not a political lean.

**Kill-test outcomes (same day, evening):** both open items were run pre-registered. (1) Swing: receiver effect *survived* the Hispanic-share control (+0.0256 → +0.0238, t≈7.2) — the morning's retraction of the assertion stands, but the decomposition restores the claim (ladder 36). (2) CHNV: the event study failed an external-anchor sanity check, exposing two parser bugs (fiscal-index dates; OFO-universe overwrite) — entry 26 *reversed*: between-port crossings collapsed 95-96% (Cuba/Nicaragua) post-program; the "+787%" was the program's own lawful channel (ladder 34, decision record 2026-06-11). Calibration lesson: the audit downgraded the right claim for the wrong reason — distrust was correct, the mechanism (reverse causation) was not; the real failure was upstream data, caught only by item-23 pre-registration plus an external-anchor check. New checklist candidate promoted to the canonical list: **anchor every series to one known published value before regressing on it.**

Remaining open work: receiver-cost netting against SSP reimbursements; USBP-universe long-run (post-June-2024) substitution picture.

**Self-audit 2026-09-16 (evening, `immigration-mexican-origin-by-generation-2026-09-16.md` §5.3):** item 3 (per-what mismatch) tripped and the operator caught it, not the gate. The fiscal generator's `equal_all_members` allocation spreads a family's children and transfers over every member, so a "per adult 25–64" table built on it carried 0.12 children per adult for white natives against a true 0.25, and the Mexican second generation's schooling line was understated by a fifth; the corrected adults-only table (commit 3e828c7) moved total benefits from "level" to +15–30%. Lesson for the gate: every per-unit table from `analyze_cps_fiscal_2025.py` must name the allocation mode in its caption, and a per-adult claim must come from `equal_adults_18plus`. Item 17 (average vs marginal cost) was handled by showing average-cost and need-weighted schooling side by side.

**Self-audit 2026-09-21 (scope pass on a second agent's ranked summary; FAQ "Before combining numbers"):** the summary, written in chat and never through this gate, tripped item 1 (generation ledger and complete account set side by side as one picture), item 6 (a resident-stock cross-section read as refuting a from-arrival NPV with descendants), item 15 in a new form (a ratio built from terms that overlap, are bounds, or cover another population), item 7 (the 2023 incarceration low point quoted alone) and item 28 (preferred-sample and preferred-specification figures without their counterparts). Repo-side, three memos had omitted specifications their lanes computed (item 23): the 935-CBSA variety fit, vote-panel S10, the education gaps under the shared allocation and against whites. Mirror test on the fixes themselves (item 30) caught three of my own: an unverified superlative ("the largest movement"), a standard-error bound stated without its independence condition, and an inference about coverage written as fact; all three corrected the same hour. The gate fires on commits; a chat summary or ranking bypasses it, so CLAUDE.md now routes summaries to the FAQ's combining rules. Canonical checklist items 15, 23 and 31 were extended for the three patterns it lacked.

## Relationship to repo machinery

- Constitution principles 1-7 = values; the canonical checklist = per-claim mechanics.
- `research/immigration-fiscal-deceptive-data-reading-pack.md` = reading OTHERS' fiscal numbers; `research/immigration-economist-rhetorical-failures-2026-04-22.md` = rhetoric-level failure modes; this gate = OUR OWN output, pre-commit.
- Hook escalation: canonical list flags items 1/8/14/15/29 as mechanically checkable — build the postwrite hook only if violations recur post-checklist (instructions first, architecture on recurrence).
- Substrate integration (deferred, propose-first): if/when quantitative claims get schema treatment in `substrate/schemas/v1/claim.v1.json`, the six fields (ledger, unit, base, window, gross_net, output_type ∈ {measurement, model}) become optional claim metadata. Trigger: next claimcore schema revision — not before; schema shape needs sign-off before consumers.
