# Acquisition Gaps — datasets, narratives, papers (what's left worth getting)

**Question:** Any more datasets, narratives, or papers worth acquiring for the immigration fiscal/crime topic?
**Tier:** Standard | **Date:** 2026-06-24
**Ground truth:** Datasets saturated at 57 (both batch-5 finders returned VEIN: SATURATED). Crime domain built (INT-01/02/03/06). The cluster-T benefit-side generator bank (8 lenses) was authored 2026-06-23 explicitly as "the benefit-side acquisition list that balances the cost frontier" — its `source_rel_paths` point at papers **not yet in the corpus**. The ledger-map's "Honest residual": the *reasoning* is symmetric (S↔T) but the *evidence base* is cost-heavy.

## Headline

The dataset vein is dry; **the real open frontier is PAPERS, not data.** The corpus holds the two crime primaries (Light 2020 PNAS; the homicide-incarceration companion) and the full restrictionist/cost side (Borjas cluster, Gould, NAS benchmarks) — but **0 of the 6 named benefit-side (cluster-T) papers are saved.** The ledger is built to argue both sides and has the evidence for only one. That asymmetry — not a missing dataset — is the highest-value thing to close.

## Claims Table

| # | Claim | Evidence | Conf | Source | Status |
|---|-------|----------|------|--------|--------|
| 1 | Datasets are saturated; no new *discovery* gap | Both batch-5 finders independently → SATURATED; remaining candidates nativity-blind/enclave/advocacy | HIGH | `memory/2026-06-24.md`, batch-5 roadmaps | VERIFIED |
| 2 | 0 of 6 cluster-T benefit papers are in the corpus | `list_corpus` + filesystem scan of `~/Projects/corpus` | HIGH | [DATA] this session | VERIFIED |
| 3 | T02 Place Premium — exists, OA | Clemens-Montenegro-Pritchett, 279 cites | HIGH | DOI 10.2139/SSRN.1211427 → `doi_10_2139_ssrn_1211427` | **ACQUIRED** (216K chars) |
| 4 | T03 Consumer surplus — exists | Cortés 2008 JPE, 566 cites | HIGH | DOI 10.1086/589756 → `doi_10_1086_589756` | **ACQUIRED** (143K chars) |
| 5 | T04 Immigrant founders — exists | Azoulay-Jones-Kim-Miranda, AER:Insights 2022 (w27778), 100 cites | HIGH | DOI 10.1257/aeri.20200588 → `doi_10_1257_aeri_20200588` | **ACQUIRED** (91K chars) |
| 6 | T06 GE wage restoration — exists, **CONTESTED** | Ottaviano-Peri 2012 JEEA — disputed by Borjas-Grogger-Hanson on elasticity of substitution | HIGH | DOI 10.1111/j.1542-4774.2011.01052.x (verified on fetch) → `doi_10_1111_j_1542_4774_2011_01052_x` | **ACQUIRED** (164K chars) |
| 7 | T07 Positive selection — exists, **CONTESTED** | Chiswick 1999 AER, 769 cites — opposed by Borjas Roy-model *negative* selection for high-inequality origins (Mexico) | HIGH | DOI 10.1257/AER.89.2.181 → `doi_10_1257_aer_89_2_181` | **ACQUIRED** (20K chars) |
| 8 | T05 PAYG — govt report, not an S2 paper | SSA OACT / OASDI Trustees immigration-sensitivity tables | MED | web source (save_source, not save_paper) | NOT YET (web) |
| 9 | Mobility/2nd-gen is the biggest *narrative* gap; canonical survey exists, OA | Abramitzky-Boustan, JEL 2017, 299 cites | HIGH | DOI 10.1257/jel.20151189 → `doi_10_1257_jel_20151189` | **ACQUIRED** (139K chars) |

## Key Findings

### Papers — the cluster-T benefit-side gap (acquire these)
Six lenses, six load-bearing sources, none in corpus. Five are journal papers (acquirable now); T05 is a government report (web-archive instead). T01 and T08 are pure framing lenses with no external paper (they test against our own IPUMS panel). Acquiring these makes the warehouse's benefit-side claims *cited*, not asserted — closing the documented asymmetry.

**Two are actively CONTESTED, and that's a feature, not a bug.** T06 (Ottaviano-Peri GE wage restoration) is the pro-immigration pole of the elasticity-of-substitution debate that Borjas-Grogger-Hanson (already in cluster-S) anchors on the other side. T07 (Chiswick positive selection) is directly opposed by Borjas's Roy-model *negative* selection for high-inequality origins — which is exactly the **"Mexican overweighting → can't generalize"** concern raised about the crime finding. Acquiring T06/T07 doesn't tilt the ledger pro-immigration; it puts **both poles of two live debates** in the corpus, where the S-side is already represented. That is the honest move.

### Narratives — genuine in-scope frame gaps
1. **Intergenerational mobility / 2nd-generation convergence (Abramitzky-Boustan, "Streets of Gold").** The strongest missing frame. It reframes the static first-gen fiscal cost: immigrants' children historically matched/exceeded native upward mobility, and the dynasty ledger flips positive. Partially present as the *dynasty* row in the ledger-map, but absent as a represented narrative + modern data. The modern micro-data for this is the **already-known gated item** (openICPSR 120490, the Abramitzky mobility rebuild). The JEL survey (claim 9) is the acquirable anchor now.
2. **Crime: victimization + enforcement-spillover (the two missing crime narratives).** Current crime work is entirely *offending rates by status*. Missing: (a) immigrants as crime **victims** and deportation-fear **underreporting** — the user's own "unreported → undercount" point, currently only a caveat, has a literature (e.g., the effect of Secure Communities / sanctuary policy on crime *reporting*); (b) whether immigration **enforcement** raises or lowers public safety. Both are within the fiscal/crime boundary and unrepresented.

**Out-of-scope flag (surfaced, not pursued):** the largest frame *outside* the fiscal/crime boundary is **social cohesion / generalized trust** (Putnam, "E Pluribus Unum" — diversity ↓ short-run trust). It's a serious restrictionist welfare channel but neither fiscal nor crime; logging it so the boundary is a choice, not an oversight.

### Datasets — saturated for discovery; one build-target remains
No new discovery gap (claim 1). Two non-discovery items: (a) the T03 consumer-surplus channel needs a **local immigrant-intensive service-price index** by metro/PUMA — a *build* target (BLS area-CPI / service-price proxy), not a discovery gap, flagged in the T03 lens itself; (b) the known gated items (NIBRS, ICE dashboard export, openICPSR 120490) remain operator-blocked, unchanged.

## Disconfirmation
- Searched for the contra-pole on the two contested lenses: Borjas Roy-model negative selection (vs Chiswick T07) and the BGH elasticity dispute (vs Ottaviano-Peri T06) — both confirmed live, both already represented on the S-side of the corpus. No claim here that the benefit-side papers "settle" anything; they balance the citation base.
- No contradictory evidence found against claim 2 (corpus genuinely lacks all six); verified by two independent methods (MCP `list_corpus` + filesystem scan).

## Acquired this session (done)
6 papers fetched to the shared corpus with full text, all `quality.vetoed=false`, none retracted: T02 Place Premium, T03 Cortés, T04 AJKM, T06 Ottaviano-Peri, T07 Chiswick, + Abramitzky-Boustan (mobility anchor). The cluster-T benefit-side citation gap is now closed for the 5 lenses that have an external paper (T01/T08 are framing-only; T05 is a govt report). The Ottaviano-Peri DOI, flagged `[UNVERIFIED]` pre-fetch, resolved correctly to the real 2012 JEEA paper — now verified.

## What's uncertain / next steps (NOT done — separate efforts)
- **Wire T-papers into the warehouse** the way the S-cluster papers are mined (`mine_*` reads corpus-by-SHA). The 6 PDFs are in the corpus but the cluster-T generators' `source_rel_paths` still point at un-mined placeholder paths. This is a *build*, not research — greenlight separately.
- **T05 SSA Trustees** immigration-sensitivity tables — web-archive (`save_source`), not the paper pipeline.
- **Two crime narratives** (victimization/deportation-fear underreporting; enforcement→public-safety) — need their own paper sweep; flagged here, not pursued.
- **openICPSR 120490** (Abramitzky mobility micro-data, gated) remains operator-blocked — the JEL survey acquired here is the readable anchor, not the rebuild dataset.
