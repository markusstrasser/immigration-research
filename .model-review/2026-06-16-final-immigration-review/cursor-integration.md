# Cursor Reviewer D — Post-cleanup drift audit

Reviewed the June 16 context packet only. Findings below cite **embedded file:line** from the packet (repo paths, not `context.md` line numbers).

---

## Confirmed

### 1. Evolution ledger claim #4 contradicts June verified-surface refresh
**`research/immigration-claims-evolution-ledger-2026-04-23.md:23-25`** still says the repo federal microsim is untrustworthy and the federal number is unresolved (CPS recode). **`research/immigration-conclusion-audit-running-fixes.md`** (packet excerpt ~2504–2509) says verified-findings and the ladder were refreshed with the June **narrow SIPP-style `mexico_origin` proxy (~$1,519/adult/yr)** and withheld origin school/net rows.

The ledger got a 2026-06-16 status note at **:7**, but claim #4 body was not revised in the legacy-alignment fix (**running-fixes ~2589–2592** only names labor/backlash + Mexico synthesis).

**Minimal fix:** Revise claim #4: April CPS prototype = historical/unresolved; June `mexico_origin` proxy = live but narrow (not income tax / Medicaid / lifetime NPV). Add `## Revisions` row.

---

### 2. INDEX Quick Start still routes “what do we know?” through April snapshot
**`research/immigration-INDEX.md:1496-1497`** → start with `immigration-verified-findings-report-2026-04-10.md`. **`:1371`** labels that file “Current verified findings snapshot” with no June caveat.

Contrasts with **`:1501-1502`**, which correctly routes sweeps through running-fixes, and with **`immigration-knowledge-delta-agent-loop-2026-06-16.md:116-119`** (load index + running fixes + what changed).

**Minimal fix:** Quick Start #1 → `immigration-knowledge-delta-agent-loop-2026-06-16.md` → `immigration-conclusion-audit-running-fixes.md` → `immigration-confidence-ladder.md` → verified-findings (with date/scoped read). Downgrade **`:1371`** row text.

---

### 3. INDEX causal row still advertises “Card-vs-Borjas verdict”
**`research/immigration-INDEX.md:1460`** routes `immigration-causal-synthesis-2026-04-18.md` as “Card-vs-Borjas **verdict**.”

**`research/immigration-conclusion-audit-running-fixes.md`** (~2414–2422) explicitly narrowed E-Verify to mandate-margin, nonsignificance-scoped reads and rejected global Card/Borjas verdict language.

**Minimal fix:** Change index consult text to “observed E-Verify mandate-margin wage read; not global Card/Borjas verdict.”

---

### 4. Generator retrodiction still treats `$771/yr` as live
**`research/immigration-lifetime-fiscal-generators.md:778`** (`G-LIF-R02`): retrodiction cites “current-HH school burden **($771/yr)**” without supersession.

Contradicts **`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:699-700`** (withheld) and disconfirmation **`:713-714`**.

**Minimal fix:** Append “(superseded 2026-06-16; withheld pending same-universe rebuild).”

---

### 5. Generator cross-walk mislabels federal proxy population
**`research/immigration-lifetime-fiscal-generators.md:116`** (`G-LIF-C01`): “+$1,519/yr **Mexico <HS**.”

Live row is **`mexico_origin` full microsim** per **`immigration-knowledge-delta-agent-loop-2026-06-16.md:91`** and warehouse table **`immigration-mexico-npv-population-synthesis-2026-06-15.md:698-699`**.

**Minimal fix:** Replace with `mexico_origin` + proxy scope tag (payroll/FICA − SNAP/TANF/SSI only).

---

### 6. Mexico synthesis illustrative stack may double-count state/local
Same file **`:29-30`** says NAS benchmark includes “Federal + some state/local inside NAS cell.” **`:625-627`** subtracts “CBO state/local surge annuitized ($657/yr)” in the illustrative band **`:627`**.

**Minimal fix:** Mark CBO row “overlap-adjusted / not additive to NAS cell” or move it to a separate non-NAS local-shock column.

---

### 7. Cookbook converge prompt omits June guardrail surfaces
**`notes/immigration-lifetime-synthesis-diverge-cookbook.md:189-207`** “Read first” lists unified theory + generators + DuckDB only.

**`notes/immigration-lifetime-sweep-protocol.md:13`** mandates XDISC packet **before** next downloads. Running-fixes is the live overclaim ledger per **INDEX :1379-1380**.

**Minimal fix:** Add `immigration-conclusion-audit-running-fixes.md` and `immigration-thesis-generator-audit-2026-06-16.md` (XDISC) to converge read-first; add withheld-row check to verifiable-anchors step.

---

### 8. Thesis-generator audit points at stale review packet
**`research/immigration-thesis-generator-audit-2026-06-16.md:255`** → `.model-review/2026-06-16-immigration-thesis-generator-audit/`.

Packet git status (**context task block ~31**) shows only `?? .model-review/2026-06-16-final-immigration-review/` untracked.

**Minimal fix:** Update path to final packet; add INDEX row under Core State or infra for `.model-review/*` audit packets.

---

### 9. Running-fixes school entry still reads like open CSV hazard
**`research/immigration-conclusion-audit-running-fixes.md:15`** (2026-06-15 section): “stale exported CSV **still supported**” the −$13.5k conclusion.

**`:2952-2954`** regenerated `three_layer_annual_2023.csv` from live view, but the 2026-06-15 issue text is not closed out with “CSV now matches withheld view.”

**Minimal fix:** One line under 2026-06-16 origin-school entry: staged CSV regenerated; grep rule for pre-guard exports.

---

### 10. Sweep 13–22 index warning weaker than 23–32
**`research/immigration-INDEX.md:1403`** marks 13–22 “superseded by 23–32” but **`:1404`** adds explicit “do not cite `$771/+748`” only for 23–32.

Given 13–22 built the rushed school pass (same cleanup narrative, running-fixes ~2517), agents can still mine stale rows from the earlier memo.

**Minimal fix:** Mirror the `$771/+748` / withheld-origin warning on the 13–22 row, or demote it from “Post-sweep thesis burst” routing.

---

### 11. Economist rhetorical-failures steel-man still overreads county panel
**`research/immigration-economist-rhetorical-failures-2026-04-22.md:1161`** cites `immigration-county-outcome-panel-2026-04-21.md` for “broad job collapse rhetoric is too crude” without E-Verify margin scope.

Status note **`:7`** scopes capacity/surge; labor bullet was not symmetrically narrowed (contrast evolution ledger claim #8 at **`:786`**).

**Minimal fix:** Cite E-Verify QWI margin + “descriptive county screen,” not county panel alone.

---

### 12. Open process debt the cleanup acknowledged but did not close
| Issue | Packet cite |
|-------|-------------|
| MD 106 vs DuckDB 104 generator rows | `immigration-lifetime-fiscal-generators.md:6`, thesis audit `:288-289` |
| No lifecycle fields in DuckDB | thesis audit `:291`, `:324`, deferred `:538-539` |
| XDISC-DS-01/02 not run on verified/ladder | thesis audit `:250-251` |
| Loop still fiscal-monoculture | thesis audit `:278`, `:305-306` |

**Minimal fix:** One running-fixes “process” entry listing open items; don’t automate on generator counts until reconciled.

---

## Speculative (plausible; not fully evidenced in packet)

| Issue | Why speculative | Minimal fix if true |
|-------|-----------------|---------------------|
| **Causal reading stack unrouted** | Commit `f42dfea` in packet header; no file body or INDEX row in packet | Locate artifact; add INDEX row |
| **`immigration-lifetime-unified-theory-2026-06-15.md` not June-patched** | Referenced everywhere; full file not in packet | Grep for `$771`, `+$748`, Card/Borjas verdict; add revisions table |
| **`immigration-sweep-cycles-13-22-2026-06-15.md` still has live stale numbers** | Inferred from INDEX + running-fixes narrative; file not in packet | Same supersession block as 23–32 |
| **Agent loop replaces human search-space shaping** | thesis audit `:278` says not yet; lifecycle deferred | Treat as assisted loop, not autonomous replacement, until XDISC + yield accounting ship |

---

## Verdict

June cleanup **did** land on high-reuse fiscal surfaces (Mexico synthesis warehouse table, running-fixes chain, public economist status notes). Remaining damage is mostly **routing and second-order synthesis**: evolution ledger claim #4, INDEX Quick Start #1, generator retrodictions (`$771`, `Mexico <HS`), cookbook/protocol mismatch, and unintegrated `.model-review` artifacts.

**Highest-value next patches (3):**
1. Evolution ledger claim #4 + INDEX Quick Start #1  
2. `G-LIF-R02:778` and `G-LIF-C01:116` population/scalar labels  
3. Reviewer-packet path + track/commit `.model-review/2026-06-16-final-immigration-review/`
