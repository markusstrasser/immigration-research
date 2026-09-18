## 1. The literatures, verified where verification was possible

Full verification with page-level quotes: `infra/immigration-fiscal/school_flight_2026_09_18/LIT.md`.

### 1.1 Betts & Fairlie 2003 — the "one per four" figure is exactly the paper's own

[SOURCE: Betts & Fairlie, "Does immigration induce native flight from public schools into
private schools?", Journal of Public Economics 87 (2003) 987–1012, DOI
10.1016/S0047-2727(01)00164-5; PDF at
http://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf]

The abstract says it verbatim: "For every four immigrants who arrive in public high
schools, it is estimated that one native student switches to a private school." The
repo's paraphrase is accurate. Four qualifications change how much weight it carries.

**It is secondary school only.** At primary level the estimated coefficients are
*negative and insignificant* (GLS −0.794, SE 0.838). The authors: "there is no evidence
of a statistically significant link between immigration inflows and changes in native
parents' decisions about whether to send their children to private schools at the primary
level" (p. 1003). Roughly four-fifths of K-12 enrolment is below grade 9, so the channel
is switched off for most of the school system.

**The design is a two-period first-differenced metro panel, not an IV.** 1980 and 1990
Census microdata, 132 metropolitan areas, Borjas–Sueyoshi two-stage probit. The IV
robustness check gives 3.90 (SE 2.31), and the authors themselves write "The IV model is
thus not at all conclusive" (p. 1002).

**It is about non-English-speaking immigrants, and white natives.** The coefficient on the
non-English-speaking immigrant share is significant and the English-speaking one is not;
flight is "almost purely from non-English-speaking immigrants" (pp. 1003–1005). Table 5:
"the addition of one immigrant to the public school system leads 0.28 white natives to
switch from public to private schools" (p. 1006).

**The aggregate implication is small — and the authors say so.** Their own simulation:
across the 132 metros the private secondary rate would have risen from 10.29% to 10.64%
over 1980–1990, "an increase of 0.34 percentage points or 3.3%," with an arc elasticity of
0.143, and "Clearly, at the national level trends in the immigrant share are unlikely to
have led to major swings in the enrolment shares of public high schools" (p. 1008). The
metro-level predictions are where the action is: +1.34 pp in Los Angeles, +1.42 pp in San
Francisco, +2.51 pp in Miami.

One design limitation the authors flag: the native Black share is a comparison regressor
with almost no variation over 1980–1990 (+0.5 pp), so its small insignificant coefficient
is not evidence that Black composition fails to drive flight (fn. 26, p. 1002). The older
desegregation literature is the place to look for that; see §5.

### 1.2 Poterba 1997 — the elderly result holds, the racial-difference result does not

[SOURCE: Poterba, "Demographic structure and the political economy of public education,"
JPAM 16(1) 1997, 48–66; working-paper version NBER WP 5677, July 1996, read in full at
https://www.nber.org/system/files/working_papers/w5677/w5677.pdf, cached at
`_cache/poterba_w5677.pdf`. [UNVERIFIED] whether the published JPAM tables differ from the
WP tables — the numbers below are the WP's.]

Design: 48 continental states, four years only (1961, 1971, 1981, 1991), log real per-child
K-12 spending. The elderly-share result is solid: coefficient −0.276 (SE 0.121) with state
and time effects, an elasticity of about −0.25; a one-standard-deviation rise in the
elderly share (0.108 → 0.130) cuts per-pupil spending by about 5% (p. 16). It weakens and
loses significance once urban share is controlled (−0.155, SE 0.125). The school-age share
elasticity is about −1.0: a bigger child cohort does not get proportionately more money.

The racial result is weaker than its reputation. The variable is the *level* difference
(nonwhite share of ages 5–17) minus (nonwhite share of 65+), entered additively — **there
is no elderly × race interaction term in the paper**. With state and time effects the
coefficient is −0.621 (SE 0.394), which Poterba describes as "not statistically
significant at standard confidence levels" (p. 21); a one-point rise in the nonwhite share
of children cuts log per-child spending by about 0.6%. The standard deviation of the
variable is only 0.047, so identifying variation is thin. The abstract's claim that the
elderly effect is "particularly large when the elderly residents and the school-age
population are from different racial groups" rests on that insignificant additive
coefficient plus the contrast with Table 6, where the same variable predicts *higher*
non-education spending, significantly. **A memo should cite the −0.25 elderly elasticity
and must not present the racial-difference result as an estimated interaction.**

