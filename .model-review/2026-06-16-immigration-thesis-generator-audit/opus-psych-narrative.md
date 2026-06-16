Scope: psychology, political economy, framing, agenda-setting, narrative self-prompts only. I treated the memo as untrusted and did not rely on its factual specifics. Because I have no tools here, every author/citation I propose is tagged "(verify)" — confirm at primary source before writing any into the registry.

## Findings (severity-ordered)

**F1 (HIGH) — "Political economy" is in scope but there is no PE generator.** Every POL/PSY row is either agenda *process* (Kingdon) or individual *attitudes*. Missing: coalitions, interest groups, median voter, the diversity–redistribution tradeoff. The memo's own weakness list names "political economy," then ships psychology + agenda-setting and calls it done. Distributive PE — employers/capital vs native low-skill labor, concentrated losers vs diffuse winners, protection-for-sale logic — is the largest family gap in this scope.

**F2 (HIGH) — Missing sociotropic/egocentric split.** XDISC-PSY-01 splits *material vs perceived* threat but not *personal vs national/collective*, nor *economic vs cultural*. The dominant attitudes finding is that immigration opinion is sociotropic, not pocketbook; a "material burden" axis without a collective axis will mis-attribute mechanism (verify: Hainmueller–Hopkins).

**F3 (HIGH) — Agenda-setting collapsed into Kingdon/MSF.** The scope explicitly names agenda-setting; the memo gives only MSF, which is near-unfalsifiable (any outcome relabels the three streams post hoc). Missing: agenda-setting proper (what-to-think-about), second-level/attribute framing, priming (evaluation criteria), issue ownership (which party), and elite-cue/RAS (perceived share may be *downstream* of messaging). By the memo's own XDISC-DS-01, MSF claims are "narrative" and must be tagged, not used causally.

**F4 (HIGH) — Source-mapping error in XDISC-PSY-03.** "Insert a belief-mediator row" implies fix-perception → fix-attitude. The cited Alesina–Miano–Stantcheva work points the other way: correcting innumeracy often did *not* raise redistribution support, and an anecdote moved people more than numbers (verify). The generator as written licenses the exact naive inference the paper refutes. Separately, Alesina 2018 is cited for *two* different generators (PSY-01 threat, PSY-03 misperception) without distinguishing the claims — one paper doing double duty.

**F5 (HIGH) — The memo never runs its own frame audit on itself; the generator set is opposition-tilted.** Retrodiction/negative-space columns recur on "overload," "system collapse," "surge-era," "receiver-node." Per Entman (which the memo invokes), those illustrations *do framing work* — a burden frame is smuggled into the examples. Structurally there is a rich psychology-of-opposition (threat) but a thin psychology-of-support (one contact row); no solidarity/humanitarian/economic-dynamism/national-self-image generator. Asymmetric generators bias divergence before any search runs.

**F6 (MED) — Motivated reasoning / identity-protective cognition absent.** The repo's premise is better-evidence → better-conclusion. On identity-expressive issues, more numeracy can *widen* partisan gaps (verify: Kahan). Without this generator the loop cannot model why its own outputs may fail to move beliefs.

**F7 (MED) — Steelman symmetry asserted, not operationalized.** "one pro / one restrictionist steelman" appears in prose only (flowchart + Q6); no generator, no schema field, no fail condition. Given the memo's stated selection worry, make it enforceable.

**F8 (MED) — NAR-01/NAR-02 unfalsifiable; PSY-01 over-bundled.** Frame analysis can always "find" a frame — no fail condition, no requirement to name the *absent* frame. PSY-01 bundles distinct theories (realistic vs symbolic threat; group-conflict; authoritarian-predisposition×threat) on one axis, which blocks the disconfirmation the memo wants.

**F9 (LOW) — Cross-link/clustering/citation hygiene.** Contact (PSY-02) ignores selection/reverse-causation though Manski reflection (MIC-02) already exists — cross-apply it; MIC-02's real use is political-response, so it is mis-clustered. "Kingdon/MSF literature" is the only sourceless citation. Each PSY/NAR row rests on one contested literature — require a named leading critique.

**F10 (LOW) — Framing/narrative refinements missing.** Episodic vs thematic (responsibility attribution; verify: Iyengar), competitive/strong-vs-weak framing (single-frame effects overstate; Chong–Druckman), moral reframing (Feinberg–Willer), and deservingness (van Oorschot CARIN) — the last bridges PSY+PE+narrative and retrodicts the deserving-refugee/undeserving-economic-migrant split.

## Exact patch suggestions

**Add rows** (memo table format: ID | Family | Prompt | Retrodicts / first probe):

- `XDISC-PE-01 | Distributive PE | Name winning/losing coalitions and the policy equilibrium for each recommendation: capital/employers, native low- vs high-skill labor, taxpayers, incumbents; who lobbies, who is unorganized, median voter vs organized minority. | Retrodicts why fiscally-positive inflows still draw opposition (concentrated losers, diffuse winners). Probe: 3 coalitions per recommendation. (verify: Grossman–Helpman; Freeman)`
- `XDISC-PE-02 | Diversity–redistribution | Ask whether heterogeneity lowers support for redistribution/public goods, separately from fiscal cost. | Retrodicts the "progressive's dilemma." Probe: tag each welfare claim cost-channel vs solidarity-channel. (verify: Alesina–Glaeser; Putnam)`
- `XDISC-PSY-04 | Sociotropic vs egocentric | Split personal/pocketbook from national/collective, and economic from cultural. Fail any attitude claim inferring personal self-interest from a group-level correlation. | Retrodicts why low-skill natives near immigrants aren't reliably more opposed. Probe: classify one finding on both axes. (verify: Hainmueller–Hopkins)`
- `XDISC-PSY-05 | Motivated reasoning | Ask whether the belief is identity-expressive; if so, predict better evidence widens, not narrows, partisan gaps. | Retrodicts why prior fixes may not move opinion. Probe: mark each claim accuracy- vs identity-driven. (verify: Kahan)`
- `XDISC-AGS-01 | Agenda-setting/priming | Separate salience, attribute/second-level framing, priming (judgment criteria), and issue ownership; ask whether perceived share is bottom-up or an elite-cue artifact. | Retrodicts salience shifts with no ground-condition change. Probe: decompose one "why salient now." (verify: McCombs–Shaw; Zaller; Petrocik)`
- `XDISC-NAR-03 | Deservingness | Score implicit deservingness criteria (control, attitude, reciprocity, identity, need) per migrant category; ask which the narrative activates. | Retrodicts refugee-vs-economic-migrant policy splits. Probe: tag one public paragraph. (verify: van Oorschot)`
- `XDISC-NAR-04 | Steelman symmetry | Each sweep emits one pro and one restrictionist steelman the other side would accept as fair; fail convergence if either is missing or strawmanned. | Retrodicts selection toward house frame. Probe: store both steelmen as rows.`

**Edit existing rows:**
- PSY-01: replace the bundled list with explicit theory tags — realistic / symbolic / group-conflict / authoritarian×threat — and require naming which theory is under test.
- PSY-02: append "apply XDISC-MIC-02 — is contact causal or selected?"
- PSY-03: change "insert a belief-mediator row" → "...AND test whether correcting the belief changes the attitude; do not assume it does — cited evidence shows correction can fail or reverse."
- NAR-01/02: add fail condition — "name the absent frame and one observation distinguishing frame-effect from null; a frame you cannot fail is not a finding."
- POL-01: rename "Problem stream" → "Agenda process (MSF)"; add "tag MSF as narrative per XDISC-DS-01, not causal."

**Citations:** give "Kingdon/MSF" a specific work+year; stop reusing Alesina 2018 across PSY-01 and PSY-03 — cite the threat anchor (e.g. Quillian) separately from the misperception anchor.

**Schema:** add `theory_anchor`, `leading_critique` (force ≥1 named counter-literature), and `steelman_side` (pro|restrictionist|n/a).

**Self-application:** run XDISC-NAR-02 on the memo's *own* retrodiction/negative-space columns; pair each "overload/collapse/surge" illustration with a support-side example, or neutralize it.
