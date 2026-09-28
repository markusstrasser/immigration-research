# Card–Peri wage evidence — corrected assessment

**Current assessment: 2026-09-05.** The earlier critique overstated what a null identifies, applied a national native-migration estimate to Mariel without identifying that magnitude there, and used obsolete working-paper wage estimates as if they were the published 2012 result. These errors affect its substantive conclusions. The narrower questions about distribution, adjustment, and external validity remain legitimate. [INFERENCE]

## Current evidence, with versions separated

| Evidence | What it supports | What it does not establish |
|---|---|---|
| Card (1990), Mariel | Little detectable adverse wage or employment response in the studied Miami groups after a large local inflow. | Exact zero effect, an equivalence bound for all groups, or an identified nationwide effect. |
| Ottaviano–Peri (2012), published JEEA model | For immigration over **1990–2006**, about **+0.6% average native wages** and **−6.7% for previous immigrants** in the long run, under the preferred model. | A directly observed wage change caused solely by immigration, or the old draft's −19% as the final estimate. |
| Task substitution and capital adjustment | Mechanisms that can change wage incidence and the response over time. | No competition, a fixed universal elasticity, or identical adjustment in every setting. |
| The repo's QWI E-Verify coefficient | An uncertain estimate for monthly earnings of covered stable workers under that design's assumptions. | A native-born hourly-wage estimate: QWI's cited series has no nativity/citizenship variable. It cannot validate Card–Peri's native-wage or task mechanism. |

[SOURCE: https://davidcard.berkeley.edu/papers/mariel-impact.pdf; https://doi.org/10.1111/j.1542-4774.2011.01052.x; https://api.census.gov/data/timeseries/qwi/se/variables.html] [INFERENCE]

**Version correction:** The original NBER w12497 quotes reporting **−19%**, **−24%**, and **−1.1%** were kept verbatim in a historical section, removed 2026-09-29 (recover with `git show 36c4477:research/immigration-dismantle-card-peri-2026-06-25.md`). They are not current 2012-publication benchmarks. The final publisher abstract and LSE record report the revised period and estimates above. They describe a specification-dependent small effect on workers without a high-school degree. The old draft's negative figure cannot establish that even the final paper's favorable specification necessarily harms that group. [SOURCE: https://academic.oup.com/jeea/article-abstract/10/1/152/2182016; https://researchonline.lse.ac.uk/id/eprint/42175/]

**[GAP]** The final paper's full tables were not obtained in this repair; the headline values are publisher-abstract verified. Do not invent a corresponding final −24% subgroup result or treat the old table as the new one. No final-model re-estimation was performed.

## Mariel: a local null and adjustment, not a contradiction of economics

A labor-demand curve describes an effect holding other determinants fixed. Immigration can change product demand, capital, tasks, and location choices. A small observed wage response therefore does not “break” the theory; it tests a much more restrictive all-else-fixed application of it. Statistical insignificance also does not prove exact zero. The size of effects excluded by the design depends on its uncertainty. [INFERENCE]

Card discusses endogenous location choice and domestic migration on the first page and in the conclusion. He considers reduced net migration into Miami as a possible adjustment and explicitly warns that Miami's prior immigration and industry mix limit generalization. The earlier accusation that this issue was simply waved away is withdrawn. [SOURCE: https://davidcard.berkeley.edu/papers/mariel-impact.pdf, pp.245,255–257]

Borjas's w11610 estimate that native migration can explain 40–60% of a national/local estimate difference concerns that study's setting. It is not an estimated correction factor for Card's Mariel coefficient, not 40–60% of a wage loss, and not proof that a known Mariel loss was exported elsewhere. [SOURCE: https://www.nber.org/papers/w11610] [INFERENCE]

Domestic migration can transmit an effect to comparison locations, creating an identification issue. Capital moving **toward** an inflow can instead reduce competitive pressure through real adjustment. Those mechanisms are not interchangeable, and describing both as natives and capital “fleeing” was incorrect. A local null alone does not select between them. [INFERENCE]

Clemens–Hunt's sample-composition critique is relevant to the robustness of the claimed large dropout-wage fall. It does not turn the remaining estimates into an equivalence test or establish that every subgroup's true effect is zero. [SOURCE: https://doi.org/10.3386/w23433] [INFERENCE]

## Native averages, previous immigrants, and welfare are different estimands

The final model's negative effect on **previous immigrants** matters for incumbent-worker welfare. It does not logically refute a proposition explicitly restricted to **native-born workers**, because previous immigrants are outside that group. It would refute an unqualified claim that no incumbent worker loses under that model. That scope must be stated instead of calling a native-specific average a concealed contradiction. [INFERENCE]

Nor is the positive native average necessarily a zero-sum transfer from the previous-immigrant wage loss. The model changes output and factor returns; worker counts and wage bases differ. Establishing a gain of X for one group does not establish an equal loss of X for another. Complementarity and adverse distributional effects can coexist. [INFERENCE]

A small average never implies that every native benefits. But the earlier memo tried to establish the particular native losers using an obsolete draft. The current conclusion is that distribution requires current, group-specific estimates—not that an average itself proves hidden losses. [INFERENCE]

Similarly, failing to reject perfect substitution in a competing specification is not proof of perfect substitution. Differences between CES estimates concern identification, aggregation, samples, and structural assumptions. A null in an unrelated enforcement regression does not settle that elasticity dispute. [INFERENCE]

## What transfers to a later national inflow?

Mariel is a large local shock; Ottaviano–Peri explicitly studies a **national** immigration episode. The earlier description of the entire canon as marginal/local variation with no national analogue was wrong. A raw arrival count does not establish that a new episode lies beyond every earlier study: compare labor-force shares, skill composition, speed, locations, and adjustment horizons. [SOURCE: Card 1990 and Ottaviano–Peri 2012, above] [INFERENCE]

None of those studies directly estimates the identical 2021–2024 counterfactual. The evidence informs a prior, with uncertainty about transfer. Being out of sample does not itself show a larger negative effect or invalidate a mechanism. A surge-specific verdict requires a suitable comparison and an identified migration response; a repo ledger's “unrun” status is not evidence that nobody has studied the question. [INFERENCE]

## Current conclusion

The literature discussed here does not justify a universal wage-harm or no-harm proposition. The published OP model predicts a small positive native average and a meaningful prior-immigrant loss; Card provides evidence against a large detectable local response in his studied setting. Preserve those estimands, model conditions, and uncertainty. The older three “kills” do not survive in their original form. [INFERENCE]

## Revisions

### 2026-09-05 — repair source version, null, and population comparisons

[Material inference repair decision](../decisions/2026-09-05-material-inference-repair.md): replace obsolete draft benchmarks as current evidence; withdraw the imported Mariel attenuation factor and the claim that Card ignored adjustment; distinguish natives from all incumbents, average effects from subgroup effects, and external-validity uncertainty from demonstrated failure. Earlier quotations and prose are preserved verbatim below.

### 2026-09-29 — remove the superseded analysis

[Cleanup decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md): the verbatim pre-repair analysis that followed this section was removed; recover it with `git show 36c4477:research/immigration-dismantle-card-peri-2026-06-25.md`.
