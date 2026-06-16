Scope note: reviewing only the economics / public finance / macro / micro / urban content (ECO, MIC, MAC, URB, INST rows + the loop). I deliberately skip PSY/POL/NAR/DS. The present source mappings I *can* check from the names are accurate (Tiebout 1956 JPE, Roback 1982 JPE, Saiz 2010 QJE, Diamond 2016 AER, Hsieh–Moretti 2019 AEJ:Macro, Moretti 2010, Manski 1993 RES, Tinbergen). The problems are **missing families and one weak mapping**, not false citations.

## Findings (by severity)

**H1 — The single biggest fiscal swing variable is absent: public-goods cost-assignment + the descendant boundary.** XDISC-ECO-02 splits payer/beneficiary/jurisdiction/horizon but never names the two choices that *dominate* every immigration fiscal estimate: (a) how you assign the cost of pure/congestible public goods (average vs marginal cost of defense, debt service, infrastructure), and (b) whether the accounting unit stops at the immigrant or includes US-born descendants. These two flip the sign for most groups. A system that claims to fight "layer laundering" but can't represent average-vs-marginal public-goods allocation is blind to the literature's main fault line. Anchor: National Academies (2016), *The Economic and Fiscal Consequences of Immigration* — conspicuously uncited anywhere in the memo despite being the canonical dynamic-fiscal source.

**H2 — No generator separates the *level* gain from the *distributional* shift (immigration surplus).** The core public-economics result is that natives' net efficiency gain is a second-order triangle while the first-order effect is a redistribution from competing labor to capital and complementary labor — and that the short-run wage drop largely dissolves as capital adjusts. The memo's micro rows track adjustment *margins* but nothing forces "small aggregate gain + large redistribution + horizon-dependent wage effect." This is exactly the level-vs-layer confusion the memo exists to catch, sitting unguarded in its own wheelhouse. Anchor: Borjas (1995, JEP) immigration surplus; short-run/long-run capital adjustment.

**H3 — The field's central identification tool is unnamed.** XDISC-MIC-02 invokes Manski but the workhorse of local immigration estimates — the enclave / shift-share (Bartik) instrument — and its modern critique are missing, as is the skill-cell structure and the immigrant–native substitution elasticity that drives the entire Borjas–Card wage dispute. "Annotate Borjas/Card/Saiz" (MIC-01) gestures at this without the estimator. Anchors: Card (2001, JOLE) enclave IV; Goldsmith-Pinkham, Sorkin & Swift (2020, AER) shift-share critique; Ottaviano & Peri (2012, JEEA) vs Borjas-Grogger-Hanson on elasticity.

**M1 — Weak source mapping: Ostrom CPR → schools/shelters/courts (INST-01).** Ostrom's framework governs *rivalrous, non-excludable* common-pool resources (fisheries, aquifers). Public schools and courts are excludable-by-jurisdiction and congestible — i.e., club/local public goods, not CPRs. The mapping imports the wrong appropriation/provision problem. Recast as congestion of club/local public goods. Anchors: Buchanan (1965, *Economica*) clubs; Samuelson public goods; Tiebout (already cited).

**M2 — Lifetime NPV has no discount-rate/horizon generator.** The memo repeatedly invokes "lifetime NPV" but nothing forces discount-rate and projection-horizon sensitivity, which alone flip net-positive/net-negative in NAS-style runs. This is a clean, high-yield generator.

**M3 — Urban set is demand/housing-only; high-skill agglomeration spillovers missing.** URB-01–04 cover sorting, spatial equilibrium, housing supply, and employment multipliers, but omit innovation/agglomeration externalities (the main *productivity* channel of immigration). Anchors: Kerr & Lincoln (2010, JOLE); Hunt & Gauthier-Loiselle (2010, AEJ:Macro).

**L1 — Moretti multiplier mislabeled (URB-04).** Moretti (2010) is an *employment/demand* multiplier (tradable→non-tradable jobs), not a fiscal-cost multiplier. Using it to argue "fiscal costs cannot be read from population count" is a category slip; the fiscal link is indirect (via tax base). Tighten the wording.

**L2 — MAC-01/02 are unsourced [INFERENCE].** Both are sound OLG/open-economy logic but cite nothing. Anchor MAC-01 to NAS (2016) + Auerbach-Kotlikoff OLG; MAC-02 to Clemens (2011, JEP) "Trillion-Dollar Bills" for the global-output/place-premium leg.

## Exact patch suggestions

**Patch A — extend XDISC-ECO-02 prompt:**
> Split statutory payer, economic payer, beneficiary, jurisdiction, **public-goods cost rule (average vs marginal cost of pure/congestible goods), accounting unit (immigrant only vs incl. US-born descendants),** and time horizon for every dollar claim. **Fail any net-fiscal sign claim that does not state its public-goods rule and descendant boundary.**
> Source: add `National Academies (2016), Economic and Fiscal Consequences of Immigration`.

**Patch B — new row XDISC-ECO-03 (Immigration surplus / level vs distribution):**
> Family: Public/labor economics. Prompt: For any wage or output effect, separate the aggregate efficiency change (native surplus triangle) from the redistribution between competing labor, complementary labor, and capital; state the capital-adjustment horizon (short-run drop vs long-run dissipation). Retrodicts: why a near-zero average wage effect coexists with real distributional losses. Probe: decompose one Borjas/Card claim into level vs transfer. Source: Borjas (1995, JEP).

**Patch C — new row XDISC-MIC-03 (Identification & skill structure):**
> Family: Labor micro. Prompt: For any local immigration effect, name the identification strategy (spatial correlation, enclave/shift-share IV, factor-proportions national-skill-cell), the skill cells, the immigrant–native substitution elasticity, and the leading endogeneity threat (native out-migration, enclave pull, shift-share exposure). Retrodicts: Borjas–Card divergence; receiver-city out-migration. Probe: re-derive one local estimate's instrument and its exclusion restriction. Sources: Card (2001, JOLE); Goldsmith-Pinkham, Sorkin & Swift (2020, AER); Ottaviano & Peri (2012, JEEA).

**Patch D — rewrite XDISC-INST-01:**
> Treat schools, shelters, courts, permits, and public safety as **congestible club/local public goods** with capacity, congestion, and rationing rules — not common-pool resources. Source: replace Ostrom-only with `Buchanan (1965, Economica)` + `Tiebout (1956)`; keep Ostrom only for genuinely rival-nonexcludable cases (water, open shelters at capacity).

**Patch E — new row XDISC-MAC-03 (NPV sensitivity) + source MAC-01/02:**
> Prompt: For every lifetime/NPV claim, report sensitivity to discount rate and projection horizon, and whether it dissipates under capital adjustment. Source: NAS (2016). Add to MAC-01: `Auerbach-Kotlikoff OLG`; MAC-02: `Clemens (2011, JEP)`.

**Patch F — new row XDISC-URB-05 (Agglomeration/innovation):**
> Prompt: Ask whether high-skill inflows generate innovation/agglomeration externalities (patents, entrepreneurship, knowledge spillovers) that offset congestion/housing losses, and at what spatial scale. Sources: Kerr & Lincoln (2010, JOLE); Hunt & Gauthier-Loiselle (2010, AEJ:Macro).

**Patch G — URB-04 wording:** change "Moretti local multipliers… fiscal costs" → "**employment/demand** multipliers; link to fiscal incidence only via the induced tax base, not directly."

One process note: the memo's self-prompt asks "which discipline would object first" but lists no public-finance *content* hooks (public-goods rule, surplus triangle, identification). Adding Patches A–C makes that question answerable rather than rhetorical.
