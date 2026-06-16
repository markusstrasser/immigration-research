# Adversarial review: immigration thesis generator audit

## Critical

**1. Registry sync is broken; yield scoring is fiction until reconciled.**  
Audit correctly flags 106 MD headings vs 104 DuckDB rows, but never names the delta. Generators load from `.mining/*.json`, not the MD file (`build_lifetime_evidence_warehouse.py`). Automation on MD counts will misfire.

*Patch:* Add reconciliation section: `comm -3 <(rg '^### G-LIF' MD | sort) <(SELECT generator_id FROM lifetime_generators ORDER BY 1)`. Log orphans in `generator_yield_log`. Block XDISC load until G-LIF delta is zero.

**2. XDISC largely duplicates G-LIF without a dedup map — will inflate "fired" counts.**

| XDISC | Existing overlap |
|-------|------------------|
| ECO-02 | G-LIF-C01, O01, K01 |
| MIC-01 | G-LIF-B01, B04, F02 |
| URB-02 | G-LIF-E01 (+ partial E03) |
| DS-02 | G-LIF-Q01–Q06, N cluster, K01 |
| INST-01 | G-LIF-C02, P02, J cluster |

*Patch:* Before loading XDISC, add `supersedes` / `duplicates` column. Only net-new IDs: MIC-02, MAC-01/02, URB-01/03/04, PSY-01–03, POL-01, NAR-01/02, DS-01, RSI-01.

**3. Retirement rule is unenforceable.**  
Cookbook A5: "retire generators that cycle twice with zero adopted output." DuckDB has no `status`, `last_fired`, `adopted_outputs`. No sweep log links `generator_id → artifact`.

*Patch:* Move lifecycle schema to DuckDB/sidecar (audit lines 186–198). Add `sweep_generator_log(sweep_id, generator_id, fired_at, output_path, adopted_bool)`. Wire RSI-01 to that table, not prose.

**4. Phantom artifact in two-day delta.**  
Line 23 cites a "knowledge-delta agent loop memo" — no such file in repo; only appears in this audit. `[DATA]` tag is wrong.

*Patch:* Delete reference or name path. Retag: `[UNVERIFIED]` until file exists.

---

## High

**5. "Fiscal monoculture" overstates the gap.**  
Clusters O (political), S (15 restrictionist steelmen), E (housing), C (capacity), J/P (admin) already cover much of what XDISC adds. Real gaps: symmetric open-borders steelman, causal/DAG identification, survey/legal-status measurement, pipeline invariants.

*Patch:* Rewrite weakness §1: "narrative/frame generators thin relative to fiscal ledger generators (~85:15), not absent." Add missing families:

- **XDISC-CAU-01** — DAG/confounder gate (from `immigration-costs-causal-analysis.md`)
- **XDISC-ADV-01** — Clemens/open-borders steelman (mirror of S cluster)
- **XDISC-MEAS-01** — ACS/CPS legal-status & YOEP measurement error
- **XDISC-PIPE-01** — view/unit drift (F-33, withheld rows per running-fixes)

**6. XDISC prompts too vague to mechanize.**  
Most lack pass/fail, output schema, or DuckDB probe ("annotate one memo", "draw 3-period table"). G-LIF entries are tighter: named papers, warehouse tables, numeric bands.

*Patch:* Every XDISC row needs: `negative_space`, `retrodiction≥2` with repo file pointers, `first_probe` as SQL or grep command, `fail_condition`. Example for DS-02: `FAIL IF numerator_population != denominator_population AND ratio lacks universe_label`.

**7. Verdict bundles inference with data evidence.**  
Line 5: `[SOURCE: DuckDB query]` adjacent to "materially better than two days ago" — DuckDB does not establish temporal improvement.

*Patch:* Split tags. Comparative verdict → `[INFERENCE]` only. DuckDB → count/schema facts only.

---

## Medium

**8. Memo duplicates durable artifacts.**  
Self-prompt (lines 87–109), flowchart (117–176), and minimum schema (184–199) overlap cookbook + sweep-protocol. Three copies will drift.

*Patch:* Move to canonical homes:
- Self-prompt → `notes/immigration-lifetime-sweep-protocol.md` §Pre-sweep
- Flowchart → cookbook diagram (replace ASCII duplicate)
- Schema → DuckDB migration + one-line index stub
- Audit memo → verdict + XDISC net-new table + dedup map only

**9. Citation errors in XDISC table.**  
PSY-01 tags "Alesina et al. 2018" for threat-vs-load; sources section has AMS w24733 (misperception/redistribution), not Quillian threat mechanism. POL-01 "Title 42/CHNV timing errors" attributed to Kingdon is `[INFERENCE]` at best.

*Patch:* PSY-01 → `[SOURCE: Quillian 1995]`. AMS → PSY-03 only. POL-01 retrodictions → `[SOURCE: running-fixes entries naming Title 42/CHNV]` or downgrade.

**10. Flowchart step 3 lacks selection rule.**  
"Run fiscal, micro, macro, urban, psych, political generators" — no minimum set, cluster map, or cap. With 106+ G-LIF + 20 XDISC, agent will cherry-pick.

*Patch:* Bind: `≥1 from {Q,R} denominators`, `≥1 from {E,C} local`, `≥1 from S or ADV`, `≥1 from {NAR,POL,PSY}`, `DS-01 on every load-bearing number`. Max 8 generators/sweep.

**11. Running-fixes not wired to generator birth.**  
Audit says fixes should "also log process fixes" but no generator maps repeated human corrections → new G-LIF (school universe mismatch should have spawned PIPE-01).

*Patch:* Running-fixes template: `generator_spawned: G-LIF-??? | none`. RSI-01 reads that field.

---

## Low

**12. Header still says "100+ generators" while body says 106.**  
*Patch:* Single canonical count with `as_of` date and reconciliation status.

**13. Urbanism critique partially wrong.**  
E01–E05 already go beyond rent elasticity (WRLURI, remittance, VMT). Gap is Tiebout/Roback/Moretti multipliers, not "only Saiz."

*Patch:* Line 47: "E cluster covers rent/supply; missing Tiebout sorting, Roback welfare decomposition, Moretti multipliers."

---

## Exact patch suggestions (priority order)

1. **`research/immigration-thesis-generator-audit-2026-06-16.md` L23** — Remove or path-link "knowledge-delta agent loop memo"; retag `[UNVERIFIED]`.
2. **Same file, XDISC table** — Add `duplicates_g_lif` column; drop or merge ECO-02, MIC-01, URB-02, DS-02, INST-01.
3. **`infra/immigration-fiscal/build/`** — Migration adding `generator_yield_log` + lifecycle columns; reconciliation script MD↔JSON↔DuckDB.
4. **`research/immigration-lifetime-fiscal-generators.md`** — New cluster `T_thesis_crossdisc` only for net-new XDISC; full G-LIF field template.
5. **`notes/immigration-lifetime-sweep-protocol.md`** — Absorb self-prompt + generator selection rule; delete from audit.
6. **`research/immigration-conclusion-audit-running-fixes.md`** — Add `generator_spawned` field to template.
7. **New generators:** XDISC-CAU-01, XDISC-ADV-01, XDISC-MEAS-01, XDISC-PIPE-01 with retrodiction pointers to school-universe and ICE-docket fixes.

**Bottom line:** Audit diagnoses the right disease (fiscal-native loop, no yield accounting) but overclaims novelty, duplicates ~40% of existing G-LIF in XDISC, and leaves the retirement rule as prose. First move is reconcile counts, dedup XDISC, then load lifecycle schema — not run another sweep.
