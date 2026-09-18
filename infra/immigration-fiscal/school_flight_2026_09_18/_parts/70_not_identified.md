---

## 6. What is not identified here

Stated plainly, because several of these are fatal to a causal reading and the estimates
should not be quoted without them.

**The metro design has no exogenous variation after 2008.** The 2000-base shift-share
instrument is the repo's own, and ladder entry 136 already records that it is weak after
2008: the national inflow it shifts largely stopped. First-stage F statistics are reported
with every 2SLS line below. Where the F is low the 2SLS estimate is a weak-instrument
artefact and is labelled as such, not read as a causal estimate.

**Sorting is not separated from switching.** A metro's Hispanic share can rise because
immigrants arrive or because natives leave the metro entirely. Residential flight and
school flight produce the same correlation in this design. Betts & Fairlie face the same
problem and control for log native 5–18 population; this memo's metro fixed effects absorb
the level but not the change. Anything called "flight" here could be either.

**Homeschooling is inside the private share.** ACS `SCH` = 3 pools private school with
home school. Homeschooling roughly doubled around 2020-21 for reasons that have nothing to
do with immigration. Any specification whose window crosses 2020 confounds the two, and
the 2023 endpoint is the most affected observation in the panel.

**Charters are inside the public share.** See §5.1. This biases the measured flight
coefficient toward zero by an amount that grew over the window.

**The district design cannot separate a demand response from a formula response.** With
state × year fixed effects, the comparison is between districts inside the same state in
the same year, so a state's overall formula change is absorbed. But a formula that
*targets* English-learner or low-income districts moves money exactly where the Hispanic
share is rising, inside the state, in the same year. The coefficient on the Hispanic share
is then a mixture of the political-economy effect the memo is looking for and the
mechanical effect of categorical funding. The memo reports both the total and the
decomposition by revenue source (local, state, federal), which is the closest this design
gets to separating them, and it is not close enough to call causal.

**The California bond analysis is cross-sectional in the Hispanic share.** Districts are
matched to their nearest panel wave, and the identifying variation is largely between
districts, not within. It therefore carries every omitted variable that makes high-Hispanic
districts different — income, home-ownership, the age structure of the electorate. It is
reported as a description of the association, with an elderly-share control, and nothing
stronger.

**The count and share specifications answer different questions and disagree.** The count
regression is the one comparable to Betts & Fairlie's ratio, and it is the one contaminated
by metro growth; the share regression is immune to growth but is insignificant. There is no
specification here that is both comparable to the published ratio and clean. That is the
honest state of the evidence, not a result to be resolved by picking one.

**The district local-revenue result is not separated from income sorting.** Within a state
and year, a district whose Hispanic share rises is also a district whose households are
getting poorer relative to its neighbours. Local revenue per pupil falls mechanically with
the property tax base, with no change in anyone's willingness to tax themselves. The
effort measure — local revenue per pupil over county median household income — is meant to
absorb that, and it still falls, but county income is a coarse deflator for a district-level
base and cannot carry the claim on its own.

**Nothing here identifies the welfare question.** Whether the tuition in §4 is a defensive
expenditure depends on a counterfactual — what the same child would have achieved in the
public school — that no design in this memo touches. The evidence bearing on it is the
voucher literature in §5.4, which is about children who moved *with a subsidy*, from
mostly low-income families, and may not transfer to the self-paying suburban switcher who
is the subject of the flight estimates.

