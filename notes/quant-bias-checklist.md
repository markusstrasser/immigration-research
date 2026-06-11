# Quantitative Bias Checklist — Pre-Publication Gate

Date: 2026-06-11
Trigger: user request after the Cato 2026 fiscal-study dispute ("did we commit some of its biases?").
Status: living checklist. Append refinements; don't silently rewrite items (calibration data).

Historical anchors are canonical cases marked [TRAINING-DATA]; verify specifics before citing them externally. Repo cross-references are [SOURCE] links to our own artifacts.

## When to run

Before committing any memo, ladder entry, or public-facing artifact that contains: a number doing argumentative work, a ranking, causal language ("caused", "refutes", "explains"), or a welfare conclusion. Answer each section or mark N/A. A violation doesn't mean "don't publish" — it means label the move explicitly or downgrade the claim grade.

This generalizes two immigration-specific packs: the deceptive-readings pack (others' failures on fiscal averages) and the rhetorical-failures memo (economists' overextension patterns FM1-7). [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md] [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md]

## A. Ledger & framing

1. **Ledger switching / equivocation.** Migrant welfare, world output, national GDP, GDP per capita, federal budget, state/local budget, and incumbent-local welfare are different objects; sliding between them is the single most common failure in the entire fiscal debate. Anchor: Cato 2026 headlined $14.5T (immigrants-alone, national cash-flow); the with-US-born-children figure was $7.9T and didn't lead. → *Name the ledger in the claim sentence. Put the adjacent ledger's number next to the headline.*
2. **Welfare weights hidden.** "Good/bad for the country" verdicts flip with the weight on each group's welfare; the choice is normative, not empirical. Anchor: our open-borders w-sensitivity — sign flips between w=0 and w≥0.25. [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md] → *State the weights or tag [FRAMING-SENSITIVE].*
3. **Per-what mismatch.** Per-person, per-household, per-worker, and per-resident denominators give different signs from the same data. Anchor: Heritage per-household vs NAS per-person; our own household-weighting correction materially changed school-burden rankings. [SOURCE: research/immigration-household-weighted-correction.md] → *State the unit; check the source's unit before reusing its number.*

## B. Counterfactual discipline

4. **Frozen-world counterfactual.** "Without X, outcome = Y" computed by deleting X and holding all behavior, policy, and prices fixed. Anchors: Cato "debt would be 205% of GDP without immigrants" (no replacement labor, no policy response); our own mass-deportation sim holds replacement hiring at zero. [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] → *List the adjustment margins held fixed, or label the output "mechanical calibration, not forecast."*
5. **Policy endogeneity / Lucas-Goodhart.** Relationships estimated under one regime break when the regime changes; metrics targeted become gamed. Anchor: 1970s Phillips-curve breakdown [TRAINING-DATA]. Repo instance: pre-2020 marginal-flow estimates do not transfer to surge regimes (our bounded-Card finding). [SOURCE: research/immigration-causal-surge-2021-2024.md] → *State the policy variation that identifies the estimate and refuse extrapolation outside it.*
6. **Static scoring presented as dynamic truth.** One-period accounting (current taxes minus current outlays) answers a different question than lifetime/dynamic accounting; each can be "the right number" only for its question. Anchor: K-12 costs now vs the same children's taxes later — both NAS-legitimate, opposite rhetorical uses. → *Say which question the accounting answers.*

## C. Windows, bases, denominators

7. **Window selection.** The start/end dates can manufacture the result. Anchors: Reinhart-Rogoff's 90% debt threshold dissolved under Herndon's re-analysis (spreadsheet exclusions + weighting) [TRAINING-DATA]; the 1998-anchored global-warming "pause" [TRAINING-DATA]; Cato's 1994-2023 window covers the fastest foreign-born growth in US history — a working-age-heavy cohort whose entitlement draw lies mostly outside the window (Cato's data-availability defense is real but doesn't remove the asymmetry). → *Justify the window by data constraint explicitly and show at least one alternative window, or state why none exists.*
8. **Low-base percentage.** Large % growth from a small base reads as an explosion. Repo instance: "CHNV encounters +787%" — true, but from a 2,598/month base; the memo discloses the base, the ladder summary didn't. [SOURCE: research/immigration-causal-surge-2021-2024.md] → *Every % change carries its absolute base inline.*
9. **Endogenous denominator.** If the denominator responds to the treatment, ratios mask the load. Repo instance: shelter PIT/HIC ratios stay flat while absolute sheltered count explodes (Chicago) — caught in our receiver-counterfactual pass. [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md] → *Report counts next to ratios when the denominator can expand under treatment.*
10. **Gross-for-net substitution.** Quoting gross outlays where the question is net burden (ignoring reimbursements, offsetting revenue, or baseline spending that would have occurred anyway). Repo instance: receiver-city cost table is gross city outlays; federal SSP reimbursements and baseline homeless-services growth are not netted. [SOURCE: sources/immigration-causal/data/bused_cities/receiver_city_costs.csv] → *Say gross or net in the claim; if gross, name the known offsets.*

## D. Aggregation & composition

11. **Simpson's paradox / composition shift.** Aggregate trend reverses within every stratum. Anchors: Berkeley 1973 admissions; pandemic-era average wages "rose" because low-wage workers exited the denominator [TRAINING-DATA]. → *Check the claim within the major strata before publishing the aggregate.*
12. **Ecological fallacy.** Area-level correlation read as person-level fact. Anchor: Robinson 1950 — state-level immigrant share correlated positively with literacy while the individual-level relation was negative [TRAINING-DATA]. Repo guard: PUMA/county exposure layers are context, not person-level burden (confidence ladder items 10-14). [SOURCE: research/immigration-confidence-ladder.md] → *Match the inference level to the data level.*
13. **Average hiding the gradient.** A favorable mean produced by one tail. Anchor: MI's own result — average immigrant +$10K federal NPV while sub-bachelor's groups are deeply negative and young graduate-degree holders are +$1M; the average is the least informative number in the distribution. → *Report the gradient whenever subgroups plausibly differ in sign.*

## E. Model-output laundering

14. **Model output presented as measurement.** A scalar that exists only inside one assumption stack quoted as observed fact. Anchors: Camarota's -$68,390 (CIS construction from NAS scenarios, routinely misattributed to NAS); Cato's $14.5T equally a construction in the other direction. Sensitivity proof: the same 22-year-old HS dropout flips -$315K → +$45K under five defensible assumption changes (Cato WP82 vs MI). → *Headline the assumption-stack sensitivity range, or don't headline the scalar.*
15. **Amplifier add-ons in the preferred direction.** Stacking a second-order modeled effect onto a first-order estimate and leading with the sum. Anchors: Cato's $3.9T "interest savings" (27% of the $14.5T headline); our own 1.6× Type-II multiplier turning $1.45T into $2.32T in the deportation calibration. [SOURCE: sources/immigration-causal/scripts/mass_deportation_sim.py] → *Lead with the first-order number; amplified figures appear only as labeled sensitivity.*
16. **Upper-bound laundering.** Stylized theoretical maxima quoted as realistic baselines ("double world GDP"). [SOURCE: research/immigration-economist-rhetorical-failures-2026-04-22.md] → *Tag bounds as bounds.*
17. **Public-goods attribution.** Average-cost vs marginal-cost allocation of defense, debt interest, and shared infrastructure is the single largest swing factor in every fiscal estimate (NAS: sign flips on this alone) — and in a deficit country, marginal-cost attribution makes any taxpayer a "fiscal asset" (MI's reductio against Cato), while average-cost attribution makes most natives a "drain" too. → *Run or cite both attributions; never present one as "what happened."*

## F. Selection & measurement

18. **Survivorship / attrition.** The sample is the survivors. Anchors: Wald's WWII bomber armor (armor where returning planes show no holes) [TRAINING-DATA]; Secrist 1933 "triumph of mediocrity" — regression to the mean misread as convergence [TRAINING-DATA]. → *Ask who exited the sample and why.*
19. **Sample-frame selection.** Anchor: Literary Digest 1936 — 2.4M responses, wrong by 19 points (frame skew beats sample size) [TRAINING-DATA]. Repo instance: every unauthorized-status estimate rides residual-method imputation, ±10-15%. [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md] → *N does not cure frame bias; state the frame.*
20. **Collider conditioning.** Conditioning on a downstream consequence manufactures correlation. Anchor: Berkson's hospital-admission paradox [TRAINING-DATA]. Repo guard: never condition on apprehension/deportation or on appearing-in-admin-data (DAG memo's two named colliders). [SOURCE: research/fiscal-impact-unauthorized-immigration-research-memo.md] → *Check every control variable against the DAG; "controls for more things" is not monotonically better.*
21. **Construct mismatch.** The measured variable is not the rhetorical category. Repo instance: our "low-skill" = SCHL<16 (less than HS diploma), narrower than the policy shorthand "non-college" — findings must not be category-inflated. [SOURCE: research/immigration-glossary.md] → *Define the operational variable next to every category word.*
22. **Silent proxy for the principal.** Exposure proxies (rent levels, stress indices) read as the welfare object itself. Repo guard: rent exposure ≠ housing welfare loss (adversarial review §2). [SOURCE: research/immigration-adversarial-review.md] → *A proxy is fine as a labeled screen, never as the verdict.*

## G. Inference discipline

23. **Garden of forking paths / p-hacking.** Many undisclosed analyst choices, one published path. Anchors: Simmons et al. 2011 "false-positive psychology"; the Wansink retractions [TRAINING-DATA]. → *Pre-register the decision rule before seeing the outcome (verify-before preregister mode); disclose the paths tried.*
24. **Multiple comparisons.** Anchor: the dead-salmon fMRI Ig Nobel [TRAINING-DATA]. Repo positive example: 1,000-draw permutation inference in the capacity falsification pass. [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] → *Permutation/null benchmarks for any scan over many cells.*
25. **Plausibility assertion doing causal work.** "Too large to be anything else" substituting for decomposition. Repo instance: "+4.4pp receiver swing implausibly large for non-immigration causes alone" — asserted while the top swing counties (Bronx, Queens, Miami-Dade, Hidalgo, El Paso) are among the most Hispanic in the country and the national Hispanic realignment was never decomposed out; the regression controls FB share but not Hispanic share. [SOURCE: research/immigration-causal-surge-2021-2024.md] → *Quantify the rival channel or mark the sentence [INFERENCE] and grade accordingly.*
26. **Spurious time-series correlation.** Trending/nonstationary series correlate by construction. Anchor: Yule 1926 nonsense correlations [TRAINING-DATA]. → *Difference, detrend, or design (event study) before claiming co-movement.*
27. **Extrapolation beyond support.** Marginal evidence answering mass-flow questions; in-sample fit answering out-of-distribution policy. Anchors: LTCM 1998; "national house prices never fall" 2008 [TRAINING-DATA]; rhetorical-failures FM3. → *State the support region of the evidence in the claim itself.*

## H. Publication & process

28. **Headline selection among defensible constructions.** When several constructions are defensible, choosing the most favorable as the lead IS the bias — each side of the Cato dispute did exactly this ($14.5T vs "extremely fiscally negative" from the same NAS-family machinery). → *Lead with the range across constructions; our unified-scenarios memo is the house pattern.* [SOURCE: research/immigration-unified-scenarios-memo.md]
29. **Advocacy-source laundering.** A number acquires false neutrality by passing through citations. Repo instances: the "-$43B to -$299B NAS range" entered via NumbersUSA; -$68,390 routinely misattributed to NAS. → *Carry provenance tags through every reuse; check the original.*
30. **Reviewer-direction asymmetry.** Hunting for flaws only in conclusions you dislike. The Cato study got a line-by-line hostile audit from MI; MI's own model had received the same from Cato (WP82) — both audits were correct. Instrument caveat: the LLM has a documented directional thumb on this topic. [SOURCE: notes/llm-bias-caveat.md] → *Run the same-intensity audit on the congenial result (blind first-pass; steel-man both).*
31. **Publication/replication base rates.** For literature claims: most published effects shrink on replication (Ioannidis 2005; OSC 2015 [TRAINING-DATA]). → *Prefer citation-stance checks (scite contrast) and pre-frontier flags; one paper is a hypothesis, not a finding.*
32. **Unlabeled adversarial artifacts.** One-sided briefs are legitimate tools only when labeled. Repo pattern: the one-pager/debate-sheet are explicitly adversarial; Camarota is classified "adversarial brief, not baseline." → *Every artifact states its mode: estimate, bound, screen, or brief.*

## Self-audit — 2026-06-11 (Cato-dispute mirror test)

Question: did this repo commit the moves the Cato study was criticized for? Full-severity findings, all fixed via dated downgrades (append-only):

| # | Repo instance | Checklist item | Status |
|---|---|---|---|
| 1 | CHNV "+787%" graded *strong* while its own memo lists un-adjudicated reverse causation (program created because flows were already rising); ladder summary dropped the 2,598/mo base | 8, 25 | Downgraded to medium, ladder addendum 2026-06-11 |
| 2 | "+4.4pp swing implausibly large for non-immigration causes alone" — plausibility assertion over near-collinear Hispanic-realignment confound; controlled estimate is +2.4pp, headline used raw +4.41pp | 25, 11 | Annotated in ladder addendum; decomposition listed as open work |
| 3 | Deportation calibration headlines "$1.5-2.3T" where $2.32T is the 1.6×-multiplier endpoint — same family as Cato's $3.9T interest add-on, opposite political direction | 15, 4 | Presentation rule added: lead first-order $1.45T |
| 4 | Receiver-city "~$5B+/yr" is gross city outlays, not net of federal SSP reimbursement or baseline-spending counterfactual | 10 | Annotated; netting listed as open work |

Counter-evidence (moves we did NOT commit): the welfare-weight sensitivity was run honestly (item 2); the falsification pass killed our own placebo result and downgraded the threshold claim; the newcomer ratio was self-corrected 33x → ~20.5x "contextual, not burden"; scalar verdicts are refused at the headline level throughout. Note the directional spread of findings 1-4: two flatter the restrictionist reading, one flatters the anti-restrictionist reading, one is neutral-sloppy — residual bias here is "favorable-construction drift" per claim, not a uniform political lean.

## Relationship to existing machinery

- Constitution principles 1-7 (sourcing, steel-man, evidence levels, disconfirmation, framing, quantification, instrument bias) are the values; this file is the per-claim mechanics.
- `immigration-fiscal-deceptive-data-reading-pack.md` = how to read OTHERS' fiscal numbers; `immigration-economist-rhetorical-failures-2026-04-22.md` = rhetoric-level failure modes; this file = pre-commit gate on OUR OWN output, cross-topic.
- Enforcement: items 1, 8, 14, 15, 29 are mechanically checkable (ledger named? base present? sensitivity range present? provenance tag present?) and are candidates for a postwrite hook if violations recur.
