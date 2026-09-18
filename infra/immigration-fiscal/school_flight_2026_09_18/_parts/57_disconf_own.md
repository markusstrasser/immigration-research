### 5.5 The count coefficient reverses sign once metro growth is held fixed

This is the most important disconfirmation in the memo, and it kills the headline that the
count specification appears to deliver.

Regressing the change in US-born non-Hispanic white private enrolment on the change in
Hispanic public enrolment, both per 100 base-year pupils, gives about **+0.10** at every
level: roughly one white native child into private school per ten Hispanic children added
to the public schools. It is highly significant and it looks like a smaller version of
Betts & Fairlie's one-per-four.

It is an artefact of metro growth. A metro whose child population is growing adds Hispanic
public pupils and white private pupils in the same years, for the same reason. Adding the
metro's total enrolment change as a control flips the sign:

| level | raw | with total enrolment growth controlled |
|---|---|---|
| elementary | +0.101 (0.028) | **−0.127 (0.041)** |
| secondary | +0.103 (0.016) | **−0.117 (0.031)** |
| all ages 5–17 | +0.113 (0.021) | **−0.135 (0.039)** |

Conditional on how fast the metro's child population grew, a metro that added more
Hispanic public pupils added **fewer** white native private pupils. The same control turns
the foreign-born count coefficient from −0.075 to −0.355 at elementary level. Any "natives
per immigrant" ratio computed from these data without a growth control is measuring
population growth, not substitution.

### 5.6 The foreign-born share has the wrong sign; the Hispanic association is with the second generation

Three results in §3.1 point the same way, and all three cut against an immigration-driven
flight story specifically.

- **The foreign-born share of enrolled children carries a negative coefficient**, −0.284
  at elementary and −0.305 for all ages (the latter significant at 5%). Metros where the
  foreign-born share of children rose faster saw the white native private share rise
  *less*, not more.
- **Entered together, it is the US-born Hispanic share that predicts, not the foreign-born
  Hispanic share**: +0.208 (0.094) against −0.129 (0.245) at elementary. Betts & Fairlie
  found the opposite — that flight responds almost purely to non-English-speaking
  immigrants. Whatever the association here is, it is not a response to immigrant arrival.
- **The Asian share carries a negative coefficient throughout**, −0.323 at elementary and
  −0.424 for all ages. So this is not a general response to non-white composition, and a
  "diversity" reading of it fails its own falsification test in the opposite direction from
  the one the brief anticipated.

### 5.7 The share-based association does not survive the full metro sample

On the corrected 334-metro panel the share specification is **not statistically
significant at any level**: +0.154 (0.095) at elementary, +0.078 (0.073) at secondary,
+0.137 (0.083) for all ages. An earlier run on a 291-metro sample, which had dropped every
metro spanning a state line, gave +0.218 (0.084) at elementary and was significant. The
difference is the sample, not the method: restoring New York, Chicago, Washington,
Philadelphia, Kansas City, Charlotte, Memphis and Portland weakens the coefficient by a
third and widens its standard error.

The reverse-timing placebo is clean — the 2008–2010 change in the private share does not
move with the 2010–2023 change in the Hispanic share, +0.018 (0.058) at elementary — so
what is there is not a pre-trend. Dropping the five largest metros or all of California
leaves the secondary coefficient at +0.080 and +0.065, so it is not driven by a few places
either. There is simply not much there.

The instrumented estimates add nothing. The 2000-base shift-share instrument gives
coefficients from −0.28 to +0.30 with standard errors of 0.4 to 2.3, and one first-stage F
of 0.38, which is a degenerate first stage rather than a weak one. Ladder entry 136 already
recorded that this instrument dies after 2008 and that is what the first stages show.

### 5.8 District spending does not fall — state equalisation absorbs the local decline

The brief anticipated that many states send more money to high-English-learner districts,
so the sign on spending might be positive. That is close to what happens, and the
decomposition by revenue source shows the mechanism cleanly. Within a state and year, per
unit of Hispanic enrolment share:

| flow | coefficient, 2020 dollars per pupil | per 10 points of Hispanic share |
|---|---|---|
| local revenue | −4,472 (687) | −$447 |
| local property-tax revenue | −3,693 (664) | −$369 |
| state revenue | +2,809 (704) | +$281 |
| total revenue | −1,063 (1,093) | −$106, not significant |
| current spending | −1,109 (636) | −$111, marginal |
| instructional spending | −597 (309) | −$60 |

The local decline is large and precise; state aid offsets roughly 60% of it; total revenue
and spending are statistically indistinguishable from unchanged. The repo's own FY2024
cross-section pointed the same way: Hispanic pupils sit in districts spending **$474 per
pupil above** their state's mean, white pupils **$624 below** it.

Three further checks:

- **Pre-trend.** The 2000–2010 change in spending does not move with the 2010–2019 change
  in the Hispanic share, −$30 (854). For local revenue the placebo coefficient is −$1,254
  (769), against a contemporaneous −$3,336 (579) in the same window, so most of the
  local-revenue result is contemporaneous rather than a pre-existing trend, but not all of
  it.
- **Poterba's direction fails here.** The county elderly share carries a *positive*
  coefficient on per-pupil spending, +$4,917 (1,768), and its interaction with the Hispanic
  share is insignificant, +$5,954 (6,622). There is no demographic-mismatch effect in this
  panel.
- **Fractionalisation does not reproduce the Hispanic pattern.** The index gives −$474
  (265) on spending and **+$1,155 (475)** on local revenue, the opposite sign to the
  Hispanic share. That is exactly the collinearity problem Kustov & Pardelli describe in
  §5.2: in US data, "diversity" and "minority share" are different variables only in the
  places where they disagree, and where they disagree these two give different answers.

### 5.9 California districts with more Hispanic pupils vote *more* for school taxes

Across 2,954 matched school-district bond and parcel-tax measures from 1998 to 2024, the
Hispanic enrolment share is **positively** associated with the yes vote share: +0.043
(0.019), significant at 5%, with year and required-threshold fixed effects. The pass
indicator moves the same way, +0.088 (0.058), not significant. Adding the county elderly
share does not change it. The fractionalisation index is flat, +0.007 (0.037).

A ten-point higher Hispanic share goes with a 0.43-point higher yes share. That is small,
and it is a between-district comparison carrying every difference between high- and
low-Hispanic districts, so it is not a causal estimate. But the diversity-discount
prediction is that this coefficient is negative, and in the largest available US archive of
local school tax elections it is positive.

