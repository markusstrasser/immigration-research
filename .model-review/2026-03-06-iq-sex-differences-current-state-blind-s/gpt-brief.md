# Focused Review Brief

Question: What are the strongest statistical and causal blind spots in the current project state?

Established local findings:
- Literature does not establish a single battery-independent sex difference in g.
- NLSY79: same-sample schooling attenuates some female verbal/clerical edges but does not collapse male quantitative/mechanical patterns.
- PIAAC adult numeracy is male-leaning across countries, education groups, age bands, and broad occupations.
- TIMSS broad math is not one thing: Grade 4 male-leaning, Grade 8 near parity/slightly female, TIMSS Advanced male-leaning again.
- HSLS: girls near parity at baseline math and slightly below on later standardized math, but clearly above on transcript math GPA; wedge persists within common highest-math ladders.
- NLSY97 overlap: PIAT Math slightly male/near null, Arithmetic Reasoning slightly male/near null, Math Knowledge clearly female-leaning. Current interpretation: school-knowledge / Math Knowledge-heavy wedge, not broad female quantitative edge.
- Early-school: raw NLSCYA PIAT Math looked female-leaning, but after aligning math to same-wave reading and explicit age-matching, NLSCYA and ECLS-K:2011 are both male-leaning on math-minus-reading; remaining disagreement is magnitude, not sign.

Current PISA 2018 findings:
- Raw item/process pass: broad math male-leaning; 43/60 items male-leaning.
- Framework-proxy pass: raw content-family ordering is space_shape most male-leaning, uncertainty_data closest to parity.
- DIF-style proxy pass conditions each item on within-country average of PV1MATH..PV10MATH.
- In that pass, raw content gaps shrink a lot after conditioning:
  - space_shape raw -0.061 -> conditioned -0.015
  - change_relationships raw -0.053 -> conditioned -0.011
  - quantity raw -0.036 -> conditioned -0.006
  - uncertainty_data raw -0.023 -> conditioned ~0.000
- Current project read: much of raw geometry is ability-surface, but a residual content-family pattern survives, strongest in space_shape.
- Current explicit caveat: conditioning uses plausible values that likely contain target-item information, so the pass is a proxy, not formal DIF.

Existing live risks already tracked locally:
- grades/honors/course placement are contaminated mechanism surfaces, not clean latent-ability controls
- PISA conditioned-item pass may suffer from target-item contamination
- early-school reading-anchor bridge may be an imperfect psychometric bridge

What I want from GPT-5.4:
1. strongest logical/statistical blind spots, prioritized
2. whether the PISA proxy pass is useful-but-fragile or actually misleading
3. whether the early-school math-minus-reading bridge changes the estimand too much
4. whether the school-surface wedge is under-modeled because of behavior / effort / stakes variables
5. the best next 3 analyses by uncertainty reduction per unit effort
