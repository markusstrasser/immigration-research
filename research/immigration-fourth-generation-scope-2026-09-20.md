# Fourth-generation scope: evidence index

Date: 2026-09-20. [MEASUREMENT / ACCOUNTING] No new population or fiscal estimate.

**Finding:** The current 40.896574m Mexican-origin annual-account population already includes self-identified fourth and later generations within G3+. Adding a separate G4 population would double-count those residents. Separating G3 from G4+ is useful for studying assimilation, but requires better ancestry measurement than the current CPS adult records provide.

## Current executable definition

The classifier defines `mexican_third_plus_selfid` using native birth, two parents born in US areas, and Mexican identification. It applies no grandparent cutoff. The current account combines this group with Mexico-born residents and the US-born second generation, restricting to civilian-household residents. Identifying G4+ residents therefore already contribute both receipts and spending. [SOURCE: [classifier](../infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py), group masks; [current receipt builder](../infra/immigration-fiscal/full_account_receipts_2026_09_20/builder.py), `derive_keys`; [current account](immigration-complete-annual-account-2026-09-20.md), population definition.]

## What a later-generation comparison can establish

[SOURCE A2: [Duncan, Grogger, Leon and Trejo, IZA DP12704](https://docs.iza.org/dp12704.pdf), sections 2–3 and 5–6, Tables 13 and 16.] Their NLSY97 analysis separates G3 using Mexican-born grandparents, while G4+ still depends on respondent or parental Mexican identification. It finds progress hidden by pooling G3 and G4+. Selective loss of ethnic identification can bias later-generation attainment downward; it does not establish that every persistent gap is an artifact. The adult nonidentifier sample is small, and measured geographic/family controls do not eliminate the observed G3/G4+ education gap.

[MEASUREMENT] Exact G4 requires a Mexican-born great-grandparent and the relevant nearer-generation birth histories. Native-born grandparents alone identify a possible G4+ category, not exact G4. Public CPS adult records lack the required history. Our public NLSY97 reconstruction also lacks the detailed grandparent-origin fields needed for an exact Mexican lineage classification. Unknown ancestry stays unknown. [SOURCE: [parent linkage](immigration-nlsy97-parent-linkage-2026-09-17.md); [conclusion audit](immigration-new-conclusions-audit-2026-09-17.md), family-history measurement.]

[SOURCE B2: [Pew ancestry-screen methodology](https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/).] An ancestry screen including people who no longer identify as Hispanic helps test selection. This pan-Hispanic survey is not a Mexican G4 fiscal dataset.

## Use in the account

- **Present residents:** retain observed G3+; a G4 breakdown changes description, not the population total.
- **Assimilation:** separate generations where measured, show age/cohort, location and mixed parentage, and test identity selection. Cross-sectional generation gaps are not changes observed within the same families.
- **Missing remote descendants:** model their population and outcomes together. Adding people while assigning the identifying subgroup's disadvantage to all of them is unsupported.
- **Arrival-to-descendants projections:** following G4 is legitimate under a declared horizon and counterfactual, carrying both taxes and costs. Attribution across mixed lineages must avoid counting a person repeatedly. A whole person's descriptive membership does not establish full causal attribution to one ancestral arrival. [INFERENCE / FRAMING-SENSITIVE]

[GAP] No exact-G4 national fiscal estimate or observed fiscal profile of all nonidentifying remote descendants was established. Earlier population-uplift scenarios cannot be imported mechanically into the current account. This note clarifies coverage; it changes no model result.
