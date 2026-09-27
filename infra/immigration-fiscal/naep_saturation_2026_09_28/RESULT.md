claude-opus-5-5

**Verdict:** No sign that the Black share already present in 2002 hides a Hispanic, immigrant-origin or English-learner
effect on white NAEP scores. If harm saturated, the slope of white scores on the share would be negative where few Black
pupils were enrolled and flatter where many were, which makes the interaction positive. It is −0.006 (SE 0.011) SD per
10 points of Hispanic share per 10 points of baseline Black share. In the 25 states below the median Black share
(10.4%), the Hispanic slope is +0.115 (0.032), and above it +0.059 (0.064). Only the specification with state trends
gives a positive interaction, +0.036 (0.034), and it is not significant. For the immigrant-origin share the interaction
is 0.000 (0.004) with state trends.

## Question

The operator, 2026-09-28, on ladder 248's null: the US shows no statewide loss "because the damage has already been
done by blacks ... it's priced in". Harm to white pupils would then be concave in the disadvantaged share, and the
marginal Hispanic or immigrant pupil would do little where the Black share was already high.

## Design

This lane reuses `school_systemwide_2026_09_27`'s panel (`panel.build()`) and estimator (`stats_util.ols`), both
unchanged (22fd223):
- the four grade-subject cells are pooled, with scores in 2019 national SDs;
- fixed effects are cell by state and cell by year, and SEs are clustered by state;
- the years are 2003–2019.

The baseline Black share is the fall-2002 CCD share (NAEP 2003), from that lane's cached race counts. Tennessee has no
fall-2002 race counts, so 50 jurisdictions remain; without it, the lane's Hispanic slope moves from +0.087 to +0.085. The
interaction is the share times the baseline Black share less 10 points, and a second version uses the baseline nonwhite
share less 20. The lane's two robustness designs, region-by-year effects and state-by-cell trends, are applied to the
Black-share interaction.

## Results

White pupils. Slopes are per 10 points of share; interactions are the change in that slope per 10 points of baseline
share, in SDs. [CALCULATION: `derived/saturation_estimates.csv`, outcome `white`]

| Treatment | Slope at 10% Black | Interaction with Black share | Below median | Above median | Interaction, region-year | Interaction, state trends |
|---|---|---|---|---|---|---|
| Hispanic share | +0.089 (0.029) | −0.006 (0.011) | +0.115 (0.032) | +0.059 (0.064) | +0.002 (0.012) | +0.036 (0.034) |
| Immigrant-origin share, 6–17 | −0.035 (0.030) | +0.008 (0.007) | −0.032 (0.037) | −0.021 (0.039) | +0.004 (0.007) | +0.000 (0.004) |
| English-learner share | −0.038 (0.018) | +0.002 (0.011) | −0.036 (0.023) | −0.042 (0.034) | −0.009 (0.012) | −0.009 (0.012) |

- **The nonwhite version.** The baseline nonwhite share gives interactions of +0.013 (0.009), +0.013 (0.009) and
  +0.008 (0.010). These have the saturation sign, but none is significant, and the slope at 20% nonwhite is still
  positive for Hispanic share (+0.047, SE 0.041).
- **Size.** Suppose the slope went from −0.10 in an all-white state to 0 at 30% Black. That is an interaction of
  +0.033. The two-way and region-year intervals for Hispanic share exclude it, and the state-trend interval includes it.
- **Other outcomes.** `white_nonel` and `white_p10` are in the CSV.

## Limits

- A level effect of the Black share that was already in place by 2003 sits in the state fixed effects, and so does any
  national shift common to every state, such as standards or curricula. Neither is testable here.
- State shares overstate white pupils' exposure, because families sort within states. A state mean averages over moves
  within the state.
- If advantaged white families left for private schools or other states where shares rose, the white public-school
  mean would fall there. That would bias toward finding harm. The lane's control for white lunch eligibility leaves the
  Hispanic slope at +0.084.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/naep_saturation_2026_09_28/saturation.py
```
