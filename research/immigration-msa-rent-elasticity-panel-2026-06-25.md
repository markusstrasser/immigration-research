# MSA rents and elasticity: descriptive correlations with an incomplete crosswalk

**Current assessment — 2026-09-05.** The built tables are useful descriptive joins. Near-zero bivariate correlations do not establish equivalence, follow necessarily from a national shock, or prove which missing variable caused the null. The later foreign-born stock-share correlation likewise does not identify immigration's rent effect. [INFERENCE]

## Supply and demand

The reported 168 matched metros have rent-growth/elasticity correlation −0.034 and house-value-growth/elasticity correlation −0.062, with Q1 versus Q4 annual rent growth 4.98% versus 4.88%. These are near-zero sample associations and a **0.10-point annual growth spread**, not a tested equivalence result. The original warehouse table was not queried or reproduced in this pass. The raw files and both [supply](../infra/immigration-fiscal/build/build_msa_rent_elasticity_panel.py) and [stock-share](../infra/immigration-fiscal/build/build_msa_fb_rent_panel.py) builders were inspected. [SOURCE: historical outputs and tracked code; GAP]

The previous explanation that a broad national demand shock makes the correlation “expected” to be null is incorrect. In a simple market with demand shift `d`, supply elasticity `εs`, and demand elasticity magnitude `εd`, the price response is `d/(εs+εd)`. Even a **common** positive demand shift can produce larger price rises in less elastic markets. Heterogeneous shocks, correlated amenities/growth, time-varying supply, measurement error, or a poor crosswalk can obscure that relation; this correlation cannot choose among them. [DERIVATION; INFERENCE]

## The stock-share extension

The reported ACS 2023 foreign-born-share/rent-level correlation is +0.687, while the correlation with 2016–2025 rent growth is −0.174. An end-period stock share is not the same exposure as immigration during the growth window. Neither correlation establishes that immigration caused high rent levels or did not contribute to rent growth. The positive level correlation can coexist with sorting and many other mechanisms. [SOURCE: historical outputs; INFERENCE]

Correlations of 0.74 versus 0.35/0.47 in elasticity terciles also do not estimate a causal interaction; correlations vary with within-group variances, composition, and measurement. A difference in coefficients with defined units and uncertainty would still need identification. [INFERENCE]

Wilson–Zhou's local effect uses unauthorized **worker inflows relative to initial employment**, not a change in total foreign-born population share. Another ACS year would enable a difference in the latter measure, but would not supply the same treatment or validate a causal design. An instrument requires its own relevance, exclusion, and timing justification; replication of a given magnitude is not guaranteed. [SOURCE: [Wilson–Zhou Table 6](https://www.dallasfed.org/~/media/documents/research/papers/2026/wp2607.pdf); INFERENCE]

## Matching and reproducibility

The code selects first-city/state matches, keeps the largest record on collisions, and filters observations lacking endpoint rents. It does not implement a historical-PMSA-to-modern-CBSA boundary crosswalk. Missing 38% of the historical observations and collapsing names can alter the sample and estimates in either direction. The claim that perfect matching could not reveal a gradient is unsupported, and “crosswalk proven” is withdrawn. [SOURCE: supply builder join/deduplication/filter code; INFERENCE]

The raw Zillow header uses RegionID and names. ACS B25064 is median **gross rent**. The staged key-free ACS bulk files already show that an API key is not a necessary condition for another year's aggregate table, contrary to the old gated-status text. Source acquisition does not provide causal identification, however. [SOURCE: inspected raw headers, tracked bulk-file reader; INFERENCE]

The builders also contained inference-bearing correlation labels and null-to-zero display fallbacks; those confirmed code findings were reported to the parent task for repair. This memo does not treat code-generated interpretive messages as evidence. Its current scope is descriptive matching and correlations, with causal and crosswalk validation open. [GAP; INFERENCE]

## Revisions

- **2026-09-05:** Corrected the common-shock/null rationale, stock-versus-flow treatment, correlation/interaction inference, and unsupported matching and guaranteed-replication claims. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# MSA Rent-Trajectory × Supply-Elasticity Panel — built, with an honest null (2026-06-25)

**What this is.** The first deliverable off the acquired Zillow rent panel: a metro-level join of
**Zillow ZORI/ZHVI rent & home-value trajectories (2016-2025)** to the in-warehouse **Saiz (2010)
housing-supply elasticity**. It is the *supply-moderator* leg of the Wilson-Zhou (2026, Dallas Fed
WP2607) mechanism — and a crosswalk proof for the larger MSA panel. Build: `build/build_msa_rent_elasticity_panel.py`
→ table `msa_rent_elasticity_panel` (context warehouse). Local DuckDB compute; **0 LLM tokens**.

**The crosswalk (the friction I flagged).** Zillow uses modern multi-city CBSA names
("Miami-Fort Lauderdale, FL"); Saiz uses 1999 single-city PMSA names ("Miami, FL (PMSA)"). Joined on a
**(first principal city, first state) key** → "miami|fl" both sides. **Match rate 168/269 Saiz metros
(62%).** `[LIMITATION]` the unmatched 38% are metros whose first-city differs across vintages (e.g. a
1999 PMSA whose lead city isn't Zillow's lead city) — a clean Geocorr/CBSA-code crosswalk would lift this;
the name key is a 1/10 expedient, honestly bounded.

## The result — a NULL bivariate, and why that is the informative finding

| Elasticity quartile (Q1 = most inelastic) | n | avg elasticity | rent growth %/yr | home-value Δlog |
|---|---|---|---|---|
| Q1 | 42 | 1.10 | 4.98 | 0.591 |
| Q2 | 42 | 1.77 | 5.39 | 0.611 |
| Q3 | 42 | 2.45 | 5.27 | 0.614 |
| Q4 (most elastic) | 42 | 3.87 | 4.88 | 0.563 |

- **corr(rent growth, elasticity) = −0.034; corr(home-value growth, elasticity) = −0.062.** Both ≈ **zero.**
- Most-inelastic vs most-elastic rent growth: **4.98 vs 4.88 %/yr — a 0.1 pp/yr spread (null).**

**This is NOT a refutation of the Saiz/Wilson-Zhou supply mechanism — and it is NOT laundered as a
confirmation either** (an earlier cut of this script over-claimed a −0.046 corr as "confirms"; corrected).
The honest reading, and the reason it matters:

> **Supply elasticity MODERATES a demand shock; it does not drive rent growth on its own.** Over 2016-2025
> the dominant rent shock was the **2021-22 national run-up** (interest rates, COVID/remote-work demand) —
> a *broad* shock not strongly differentiated across metros by housing-supply elasticity. So a bivariate
> elasticity↔rent-growth correlation is *expected* to be ≈ null. Wilson-Zhou's positive result is
> specifically the **immigration demand shock × inelastic supply** — which requires a *metro-differentiated*
> demand variable (Δ foreign-born share) to interact with elasticity.

**So the null is the empirical justification that the gated fb-share treatment is load-bearing, not
optional.** "Get the elasticity data and rents will line up" is false; you need the demand shock. This
converts the case for pulling metro fb-share from "nice to have" into "the result is unidentified without it."

## Update (2026-06-25, later) — the demand treatment is BUILT, with NO API key (ACS summary file)

The fb-share treatment did NOT need the gated Census API: the bulk **ACS 2023 summary-file tables are
key-free.** `build_msa_fb_rent_panel.py` joins **B05002 (foreign-born) + B25064 (rent) by CBSA** (no-key
`.dat` from census.gov) via the **no-key Census gazetteer** (CBSA code→name) onto the Zillow×Saiz panel →
table `msa_fb_rent_panel`, **168 metros, zero API key**. Fully reproducible — `setup-urban-housing.sh`
auto-fetches all three (verified by a remove-and-re-fetch test). 0 LLM tokens (local DuckDB).

**Result (cross-sectional, ACS 2023 LEVEL):**
- **corr(fb-share, rent LEVEL) = +0.687** — strong: immigrants concentrate in high-rent metros (Miami 43% fb/$1914, San Jose 41%/$2773, LA 33%/$1993, SF 33%/$2397, NYC 30%/$1764).
- **Amplified where supply is inelastic:** the fb-share↔rent-level corr is **0.74 in the inelastic tercile** vs 0.35 (mid) / 0.47 (elastic) — consistent with the Wilson-Zhou incidence mechanism (inelastic metros can't absorb demand, so the immigrant-rent link is tighter).
- **BUT corr(fb-share, rent GROWTH 2016-25) = −0.174** — null-to-negative: immigrant share did NOT drive recent rent growth (matches the JCHS / Yale-Budget-Lab disconfirmation that the 2021-25 run-up wasn't immigration-timed).

**Honest bound — this is NOT the causal estimate. [FRAMING-SENSITIVE]** The +0.69 level correlation is
**sorting-confounded**: immigrants *choose* high-amenity, high-cost, supply-constrained metros (the classic
Borjas area-studies critique, ladder entry 50 / urbanism §2b). So it shows immigrants *live where rents are
high and supply is tight*, NOT that they *caused* it. The causal magnitude (Wilson-Zhou +1.4% rents per
1%-of-employment inflow) still needs the **IV/Δ** design — a shift-share instrument + a 2nd ACS year (only
2023 is staged; add another `acsdt1yYYYY-b05002.dat` to close it). The growth-margin null is the more
causal-relevant signal and it is weak. Net: the cross-section is consistent with the incidence story but
cannot separate sorting from causation; the panel now holds the demand variable for the IV once a 2nd year lands.

## What's built vs gated
- **Built (acquired data):** Zillow ZORI/ZHVI × Saiz elasticity, 168 metros, rent/home-value trajectory by
  elasticity quartile. Crosswalk proven (62%). Table flows into the unified warehouse.
- **GATED (the causal result):** `Δ rent ~ Δ fb-share × elasticity` needs **metro foreign-born share over
  time** — Census API (key-gated; the keyless route closed in 2026 — confirmed this session) **or** the
  Geocorr PUMA↔CBSA crosswalk to derive it from ACS PUMS. Both are operator actions (HUMAN.md item A/B).
  When that lands, the regression replicates Wilson-Zhou's +2.2%/+1.4% at metro scale.

## Provenance / honesty notes
- Saiz elasticity: `lifetime.saiz_msa_elasticity` (269 MSAs, 1999 OMB definitions). `[SOURCE: Saiz 2010 QJE]`
- Zillow ZORI/ZHVI: acquired 2026-06-25, `external/urban_housing/zillow/` (739 metros, monthly 2015-2026).
- The null is robust to the 62% match quality (corr ≈ 0 and quartile means are flat/non-monotone — even
  perfect matching would not produce a strong gradient).
- Confidence-ladder relation: this is the supply-leg companion to entries 18/20/38 (Saiz descriptive) and 50
  (Wilson-Zhou causal); it neither confirms nor refutes the immigration→rent claim — it shows the claim is
  *unidentified at the bivariate-supply level* and needs the demand treatment.

</details>
<!-- historical-snapshot:end -->
