**Verdict:** MASP provides a real family-descendant test including people who do not spontaneously name a Mexican/Latino identity, but the clean nonidentifier cell is only24 adults from23 families. Their BA completion and benefit receipt do not show a large hidden improvement relative to the692 who name a Mexican/Latino/Spanish background. The stronger advantage among70 people who *prefer* Anglo/American labels is a different construct: many also explicitly name Latino backgrounds. Fine generation-by-nonidentification cells are too small. Additional coding here has diminishing returns for a national fiscal question.

## Files and reproduction

- Script: [`analyze.py`](analyze.py); accepts `--source` and `--output-prefix`. Requires pandas, numpy, pyreadstat.
- Principal aggregates: ignored `derived/lineage-outcomes.csv`, `derived/lineage-generation-identity.csv`, `derived/lineage-audit.json`.
- Conditional informant-code sensitivity: use `--parent-source O2_plus_I_assumed_codes --output-prefix infra/immigration-fiscal/masp_2026_09_20/derived/lineage-I-sensitivity` from the repository root.
- Default run: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with pandas --with numpy --with pyreadstat python3 infra/immigration-fiscal/masp_2026_09_20/analyze.py`.

No respondent-level exports. Full actual source SHA256 checked against ACQUIRED.md;1,850×2,560 file parsed. Compile check passes. Independent direct-data arithmetic reproduces the24/692 identity cell counts and4/111 BA events, separate from the analysis script. A second independent reviewer also reproduced the benefit/income denominators and principal generation counts; the output explicitly distinguishes O2-only provenance from the conditional informant sensitivity.

Run [`verify.py`](verify.py) in the same dependency environment after the default analysis. It reads the raw source independently, compares108 aggregate count/event/rate cells and principal generation counts, and fails on any mismatch.

## Record roles and primary-source corrections

The1,850 rows represent1,574 original family IDs, with original-respondent1965 variables `_O1`, original-respondent followup `_O2`, informant `_I`, and unsuffixed adult-child interview fields. The unsuffixed child-interview universe is **758**, identified by nonmissing`v3`, with unique`(v3,prefix)` and`id=v3`;415 child1 and343 child2 interviews, covering482 original families. Own country is valid for757, which explains the preliminary757 count. Interviews occur1998–2002. The [Ortiz2005 preliminary paper](https://paa2005.populationassociation.org/papers/51444) analyzes768 children; do not silently call this an exact replication of that analytic sample. The older held ICPSR codebook's758 child count and the relevant identity/education/money marginals match the actual file.

**Corrections to ACQUIRED.md:**

1. `v25` is **not the single-response ethnicity question**. It asks *which background one feels closest to*, only after multiple initial labels (`v24=1`:206 respondents). Its552 missing values exactly match`v24=2`, so they are structural skips.
2. `v12–v23` hold original open-ended self-description mention ranks. Use these for initial self-identification; for preferred identity use the sole original label when exactly one was provided, otherwise`v25`. Five single-label-flag cases have inconsistent mention counts and remain unresolved for preferred identity. Other text remains separate rather than guessed.
3. `v26–v37` ask how one describes oneself **to other people**. These are a different question and cannot silently fill`v25`.
4. `v51` explicitly asks what one answers when Census/forms ask **white, black, Asian, American Indian or other**. It is a race-form response, not the separate Hispanic ethnicity question.111 answer white;92 of them explicitly name a Latino/Mexican/Spanish background in initial self-description. Treating white as non-Hispanic here would fabricate attrition.

Primary source: held `derived/codebook.txt` lines2752–2786(initial self-description),3209–3288(multiple-label gate/closest),3290+(description to others),4166–4191(race-form wording),2395–2416(child prefix/ID). Metadata alone missed these distinctions.

## Direct observed-descendant outcome comparison

All rates below are unweighted local selected-family descriptions; not national estimates or causal identity effects. No design confidence intervals. Spontaneous labeling is not equivalent to refusing Hispanic identification when prompted.

| Initial self-description | Any Mexican/Latino/Spanish mention | Only Anglo/American mentions | Other/unresolved |
|---|---:|---:|---:|
| Adults / original families |692/464|24/23|42/41|
| BA+ |111/692=16.04%|4/24=16.67%|7/42=16.67%|
| Couple income below$30k |197/663=29.71%|6/21=28.57%|8/37=21.62%|
| Any SSI/AFDC-or-public-welfare/food-stamp receipt |53/690=7.68%|2/24=8.33%|3/41=7.32%|
| Approximate mean age |41.73|41.04 (23 valid)|43.83|

Adding all42 unresolved and24 Anglo/American respondents to692 Latino/Mexican/Spanish mentioners changes BA16.04%→16.09% (122/758). This is the observed-sample schooling selection correction, not a national ancestry correction. Joint-valid samples for education, income, benefits and age:663/21/36. Their BA rates15.84/19.05/16.67%, benefit rates7.09/9.52/8.33%; missing outcomes shift small cells but do not produce compelling hidden convergence.

Preferred identity instead yields70 Anglo/American,420 Mexican/Chicano,219 Hispanic/Latino/Spanish,49 unresolved. Of those70,43 also initially name a Latino-related background,24 mention only Anglo/American and3 are Other/unresolved. Anglo/American preference hasBA16/70=22.86%, income below$30k11/62=17.74%, benefits2/70=2.86%; Mexican/Chicano preferredBA66/420=15.71%, below$30k124/408=30.39%, benefits31/420=7.38%. This is suggestive of selective identity salience, but not a measure of descendants absent from Hispanic counts. The preferred-label result cannot replace the any-mention result merely because it better matches the hypothesis.

Schooling comes from`v140` degree categories5–7=BA/BS or higher, fully observed; `v139` grade<12 and no-degree sensitivity are also exported. Thus sparse`c80/c94` school-history records are not necessary. Income`v348` valid1–21 measures respondent plus spouse/partner gross income bins, including pensions/assistance, not individual earnings. Codes97–99 are missing; no arbitrary midpoint mean used. The label/question says1996 even though interviews were1998–2002, so precise income-period alignment remains unresolved. Benefit questions`v338/v340/v341` ask past-year receipt by respondent and spouse/partner; yes1/no2, unknowns retained. Any-three is valid if one yes or all three known; these omit Medicaid and do not measure benefit dollars or total fiscal balance. Codebook lines20924–21076 and21268–21313 verify units/wording/codes.

## Generation recovery and limit

Principal results use labeled original-respondent followup fields only: original parent birth`v75_O2`, original parent's parents`v87_O2/v91_O2`; other parent`c19`; its parents`c28/c29` (whose Mexico/US numeric coding is **reversed** relative to v75); own`v75`. Unknown country codes remain unknown. `v98_O2–v101_O2` are original respondent's grandparents, hence the child's great-grandparents on that branch. All nearer ancestors US-born plus an observed Mexico-born great-grandparent can verify an exact MexicanG4 case, even without the other branch's great-grandparent data.

Principal generation counts:G1Mexico35,G1other3,G2=205,G3=245,G4plus38,unresolved232. There are243G3 with observed Mexico-born grandparents;38 with all four grandparents US-born, of whom23 have a directly observed Mexican-born great-grandparent on the original-parent branch. Original-parent country unavailable225, other-parent country unknown7, own unknown1;47 fully US-born-parent cases have insufficient grandparent history. Missing original-parent followup is selected and must not be called random.

Nativity convention: these are questionnaire country-defined groups. `C19 Other` includes Puerto Rico and Guam, so interpreting every Other as outside the questionnaire's US category does not reproduce the Census citizenship-based native/foreign-born classification. Country-specific Mexican-ancestor observations remain separately identified.

| Principal family-history group | n/families | BA+ | Below$30k | Any-three benefits |
|---|---:|---:|---:|---:|
| Confirmed Mexican-grandparentG3 |243/169|49/243=20.16%|65/229=28.38%|21/240=8.75%|
| All-grandparents-USG4+ |38/32|5/38=13.16%|10/38=26.32%|3/38=7.89%|
| Mexican-great-grandparent-confirmedG4 |23/17|3/23=13.04%|4/23=17.39%|1/23=4.35%|

Only-Anglo/American counts within genericG3/G4+ are13/2: generation-by-attrition outcome means suppressed for n<20. This is the binding sample limit. The default exports mean outcomes only for n≥20 but still records all cell counts.

**Conditional sensitivity, not verified principal:** `_I` informant items parallel`v75/v87/v91` but have no country value labels in the actual data or held codebook. Assuming1US/2Mexico/3other increases known original-parent country533→749, yieldsG3=353/G4+=59/unresolved83, confirmed MexicanG3=349 and unchanged confirmedMexicanG4=23. G3/G4+ BA16.43/16.95%, compared with the principal more-selected reconstruction; changing coverage materially changes the schooling ordering. Those figures show why we must not hide the coding/selection issue. Exact missing input for full use: an author questionnaire or program confirming the informant-country numeric mapping. Default does not use those numbers.

## Stop decision and coverage

The meaningful local test is complete. Further generation-by-nonidentification analysis reaches diminishing returns at13 and2 unambiguous only-Anglo/American respondents, even before outcome missingness. Reconstructing informant coding or hand-adjudicating Other ethnicity text might improve coverage but will not create a large independent sample or modern national estimates. An author mapping for `_I` is a concrete follow-up, not an invented absence of data.

Covered: ACQUIRED.md, actual raw file, relevant actual Stata value labels/frequencies, held codebook sections cited, preliminary author paper for selection and construct definitions, both identity constructs, schooling, income bins, three-benefit receipt, endpoint/joint validity, family counts, raw/verified genealogy and explicit sensitivity. Skipped: unrelated2,000+ variables and respondent text adjudication (limited yield and privacy), causal regression/variance claims (design/selection not solved), precise income-period relabeling (no original updated interview instrument), v51-as-ethnicity (invalid), full fiscal/crime inference (not measured by these endpoints).
