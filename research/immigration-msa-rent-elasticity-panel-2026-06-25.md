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
