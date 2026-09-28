# Streets of Gold — corrected assessment of mobility and assimilation claims

**Current assessment: 2026-09-05.** The earlier memo did not establish its claimed refutations of the mobility research. It treated different estimands as contradictions, applied sample-bias claims without establishing that the study used the affected design, and attributed a universal “everyone succeeds” claim without checking the book's full text. The core empirical finding survives; its policy scope remains limited. [INFERENCE]

## The finding and its target population

Abramitzky, Boustan, Jácome, and Pérez compare intergenerational mobility among children of immigrant and US-born parents, including comparisons conditional on parental economic position. The authors' 2024 synthesis describes evidence from historical linked censuses and modern tax records, reports substantial upward mobility, and acknowledges exceptions and coverage limits. [SOURCE: https://doi.org/10.1257/aer.20191586; https://doi.org/10.1093/pnasnexus/pgae344]

The published AER paper also directly analyzes income-score gaps before its conditional rank analysis. It therefore does not supply only a rank statistic with no evidence about convergence. Its introduction reports a pooled **5–6 percentile-point** advantage for children raised at the same 25th parental percentile. [SOURCE: https://elisajacome.github.io/Jacome/ImmigrantMobility_AER.pdf, pp.581–582]

This is evidence about the families and cohorts observed. It is not a randomized estimate of what would happen to any arbitrarily selected person if permitted to immigrate, nor a direct estimate of a future admission policy's fiscal or housing effects. Those are different questions. [INFERENCE]

## Equal starting rank defeats the “more room to rise” objection

The comparison conditions on the **same parental rank**—for example, the 25th percentile—for immigrant and US-born parents. Both comparison groups therefore have the same rank distance available above them. The earlier claim that immigrant children win this comparison simply because they start lower was wrong. [INFERENCE from the stated comparison]

A higher expected adult rank is substantive evidence of better relative economic position conditional on that starting point. It does not identify the dollar magnitude of the advantage, mean income under a nonlinear rank-to-income mapping, unconditional parity across origin groups, or every individual's success. These are limits of the estimand, not defects in using rank. [INFERENCE]

## Unconditional earnings gaps can coexist with conditional mobility

A group can start poorer, experience strong upward mobility relative to equally poor peers, and retain an unconditional earnings gap. There is no mathematical contradiction. It is legitimate to report both outcomes. A persistent gap also does not by itself demonstrate downward mobility or identify racialization as its causal mechanism. [INFERENCE]

The 2024 review explicitly discusses Villarreal–Tamborini's evidence on persistent earnings gaps. Its distinction between such gaps and mobility conditional on parental status is analytically relevant; the earlier claim that this distinction was necessarily evasive “coordinate-switching” is withdrawn. The same review acknowledges limits concerning measurement age and undocumented-parent coverage. [SOURCE: https://doi.org/10.1093/pnasnexus/pgae344, economic outcomes and notes]

Policy or welfare evaluation may care about unconditional gaps as well as mobility. Giving those outcomes weight is a framing choice; it does not invalidate the authors' chosen conditional comparison. [FRAMING-SENSITIVE] [INFERENCE]

## Nativity classification and ethnic attrition: apply them to the actual design

US-born children can be classified as native-born in a simple nativity tabulation while being identified as children of immigrants in a parental-birthplace or linked-family analysis. Birthplace and citizenship are also different variables. The second generation is the object of this mobility comparison; it has not disappeared merely because its members were born in the United States. [INFERENCE]

The ethnic-attrition concern described in this repo is that more-assimilated descendants can stop reporting an ethnic identity, making later-generation samples based on that identity understate progress. That direction contradicts the old memo's heading that both biases push measured progress upward. More fundamentally, that mechanism cannot be assigned to a parental-birthplace/linkage design without showing where self-identification determines inclusion. No such bias was established here. [SOURCE: immigration-sociology-frontier-2026-06-25.md, Duncan–Trejo entry; methodological mechanism only] [INFERENCE]

Linkage can select traceable families. To demonstrate bias one must examine match rates, false links, representativeness, and the study's robustness checks. The mere existence of linked records establishes neither the sign nor material size of bias. The former label “selection on the dependent variable” is therefore withdrawn as a finding about this paper. [INFERENCE]

## Selection and historical differences are boundaries, not refutations

A descriptive claim about observed immigrants can be correct even if migration is selective. Selection is an obstacle when using the comparison to estimate migration's causal treatment effect or to predict a differently selected future population. Geographic sorting can be one route to better outcomes; identifying it does not contradict the observation that those families did well. [INFERENCE]

The historical and modern cohorts differ in institutions and composition. That makes a replicated outcome informative across different conditions; it does not prove identical mechanisms or unrestricted transfer to today's entrants. Conversely, listing differences does not show that the observed modern result is false. The categorical claims that historical fiscal burdens could not arise because there was “no welfare state,” and that housing was universally elastic because there was “no zoning,” were not established and are withdrawn from this argument. [INFERENCE]

The tax-record exclusion must not be extended to every modern dataset in the paper: the AER study also uses a smaller GSS sample that includes some children of undocumented immigrants. It reports modern geographic comparisons as well—an immigrant mobility advantage about 25% smaller within the average county than nationally. Limited household-level geographic data constrain identification; they do not mean no modern evidence exists. [SOURCE: https://elisajacome.github.io/Jacome/ImmigrantMobility_AER.pdf, pp.582–583]

The review itself marks recent undocumented entry and asylum-system outcomes as requiring further research. Its coverage limitation therefore supports a narrower target population; it does not establish failed integration of the excluded group. [SOURCE: https://doi.org/10.1093/pnasnexus/pgae344, conclusion] [INFERENCE]

## What this audit can say about the book and policy

**[GAP] The book's full text has not been read for this repair.** Its title is not evidence that the authors promise universal success or conceal adverse outcomes. The previous inference that the trade book was unlikely to be more careful than the journal review is withdrawn. A criticism of the book's omissions requires checking its actual passages and counterexamples. [INFERENCE]

Likewise, studies of restriction and native employment address those labor-market outcomes. They do not directly settle budgets or rents, but that difference does not make their employment conclusions wrong. A finding that a restriction did not improve employment is also not automatically proof that every restriction harms natives. No complete benefit-cost verdict follows without specifying outcomes, affected populations, alternatives, and horizon. [INFERENCE]

## Current conclusion

The conditional mobility result is meaningful and survives the objections made here. Universal causal transfer, every-group convergence, and a complete policy-welfare conclusion do not follow automatically. The earlier memo repeatedly converted those limits into refutations without establishing the requisite error or even the attributed universal claim; those verdicts are withdrawn. [INFERENCE]

## Revisions

### 2026-09-05 — repair estimands and unsupported bias allegations

[Material inference repair decision](../decisions/2026-09-05-material-inference-repair.md): correct equal-parent-rank logic and dataset-specific coverage; recognize the paper's income-gap and modern-geography analyses; distinguish conditional mobility from unconditional gaps; withdraw unsupported ethnic-attrition/linkage bias and book-level universal-claim allegations; treat selection and cohort differences as scope limits. Original quotations and prose remain verbatim below.

### 2026-09-29 — remove the superseded analysis

[Cleanup decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md): the verbatim pre-repair analysis that followed this section was removed; recover it with `git show 36c4477:research/immigration-dismantle-streets-of-gold-2026-06-25.md`.
