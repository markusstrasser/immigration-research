**Verdict:** Urban scaling supplies a falsifiable mechanism and a useful sensitivity, but does not derive a universal 70–75% public-spending response. The relevant idealized network-volume exponent is 5/6, not the biological 3/4. Under a homogeneous, reversible power-law cost function and a 12% population removal, 5/6 implies an **84.21%** incremental-cost share. A 70–75% response requires stronger economies or a mixture of fixed, delayed and responsive services. Neither is established merely by invoking complexity theory. [MODEL DERIVATION; primary-source evidence below]

## Scope and strongest case

The question is whether population sharing of urban networks can lower the annual incremental cost attributed to Mexican-origin residents in the existing fiscal model. This note covers primary theory, empirical disconfirmation and the mathematical bridge. It does not estimate a Mexican-origin causal effect or perform local regressions; those belong to the parent analysis. The welfare ledger remains effects on other US residents, not aggregate resident welfare. [FRAMING-SENSITIVE]

The strongest case for scaling: larger, denser populations can reuse network infrastructure and reduce physical input per person. A finite population counterfactual should then use the integral of marginal costs, rather than assign every person the current average. That mechanism is real enough to test, but its size must be measured for the relevant service, geography and horizon. [INFERENCE]

## What the theory actually predicts

Bettencourt (2013), *The Origins of Scaling in Cities*, derives spatial and network relationships from mixing populations, incremental network growth, bounded individual effort, and interaction-dependent output. In the simple two-dimensional case, its predictions differ by object: network volume 5/6; network length 2/3; interaction-dependent output and network power dissipation 7/6. Its 2006 US lane-mile fit is 0.849 ± 0.038 (95% interval; 415 urban areas), supporting a physical-network pattern rather than an annual-budget coefficient. See paper pp.1438–1440, Fig.1 and Table1. [SOURCE: https://www.colorado.edu/socialreactors/sites/default/files/attached-files/bettencourt_2013_science.pdf ; DOI https://doi.org/10.1126/science.1235823]

The concise network derivation is: with city land area A proportional to N^(2/3), average inter-person spacing d proportional to (A/N)^(1/2), and incremental network volume V proportional to Nd, V is proportional to N^(5/6). The value therefore depends on the geometry and connecting assumptions. It is not a free-standing biological analogy. [DERIVATION of the preceding model]

To translate physical scale to money, define annual cost C = pQ, where Q is the physical service input and p its unit price. Then beta_C = beta_Q + beta_p. Even if beta_Q=5/6, rising urban wages, land prices, service standards or congestion can erase some savings. Moreover, teachers, care hours and transfer payments need not obey the exponent for roads. [IDENTITY / INFERENCE]

## Exact bridge to the fiscal response parameter

Let N be the current service population and C(N)=aN^beta its annual cost, with a, quality and population composition fixed. Let target share s=n/N. Current proportional allocation to the target is sC(N). The incremental cost of having the target population present, relative to an otherwise comparable smaller population, is:

\[
\Delta C=C(N)-C((1-s)N)=C(N)[1-(1-s)^\beta].
\]

Thus the response fraction relative to assigned average costs is:

\[
r(\beta,s)=\frac{1-(1-s)^\beta}{s}.
\]

For infinitesimal changes r tends to beta, matching C'(N)/(C(N)/N)=beta. For 0<beta<1 and finite removals, r>beta: smaller populations have higher marginal costs along the integration path. This is not the same experiment as adding 12% to the current population, which has a different base. [EXACT MODEL DERIVATION]

At an illustrative s=0.12 (not a newly measured sample share):

| Assumed cost exponent | Exact response fraction |
|---|---:|
| 0.63 | 64.48% |
| 0.66 | 67.42% |
| 0.70 | 71.33% |
| 0.75 | 76.19% |
| 0.80 | 81.01% |
| 5/6 | 84.21% |
| 0.85 | 85.80% |
| 1 | 100.00% |
| 7/6 | 115.46% |

The inverse is beta=ln(1-rs)/ln(1-s). At s=.12, response r=.20 requires beta=.1900; r=.70 requires beta=.6864; r=.75 requires beta=.7378. The roughly 20% fiscal break-even threshold is therefore far below the physical network prediction. This says nothing about other omitted fiscal or welfare channels. [CALCULATION]

For heterogeneous services and locations the correct aggregate is sum_j DeltaC_j / sum_j assignedC_j, with local service-user shares s_j and category-specific exponents. School-pupil shares cannot silently be replaced by the national population share. If an assigned category is not proportional to that service-user share, first reconcile its denominator before using the formula. [DERIVATION / measurement requirement]

For C=F+aN^beta, where F truly remains fixed in the counterfactual, the ratio relative to proportional total-cost allocation is [aN^beta/(F+aN^beta)] r(beta,s). Thus a 70% total response can coexist with 5/6 scaling if part of assigned spending is genuinely fixed. But applying such a discount to an account that already excludes fixed goods double counts the saving. Likewise, multiplying a CBO short-run response by a scaling response requires evidence that they identify separate components rather than the same partial adjustment. [DERIVATION / INFERENCE]

## Disconfirming and qualifying primary evidence

1. **England and Wales: weak universality.** Arcaute et al., *Constructing cities, deconstructing scaling laws*, use ward data and vary density, commuting and population thresholds. Many indicators are approximately linear; nonlinear exponents are sensitive to boundaries. Road/path area does not robustly follow the predicted sublinear regime. This directly challenges importing one exponent across countries and administrative definitions. It does not prove all urban economies absent. Read main text, Data and Results. [SOURCE: https://arxiv.org/pdf/1301.1674 ; peer-reviewed DOI https://doi.org/10.1098/rsif.2014.0745]

2. **France: even the scaling regime can change.** Cottineau et al., *Paradoxical Interpretations of Urban Scaling Laws*, systematically vary city definitions. Table4 gives road-length exponents across definitions from .664 to1.202; the official urban-unit and urban-area versions are .903 and .888. SectionIV shows how low population cutoffs and broad commuter peripheries can produce superlinearity. The range is construction sensitivity, not a sampling confidence interval. The inspected version is the 2015 preprint; its published successor is *Diverse cities or the systematic paradox of Urban Scaling Laws* (2017). [SOURCE: https://arxiv.org/pdf/1507.07878 ; publication record https://discovery.ucl.ac.uk/id/eprint/1501438/]

3. **Temporal changes differ from cross-sections.** Xu et al. examine 275 Chinese cities during2000–2016. Built area is sublinear across cities while many individual-city trajectories are superlinear; Chinese road-length mean exponents differ across-space versus over-time as well. The authors also examine101 US cities' congestion delay during1982–2014. These are descriptive results with outlier trimming, not causal estimates. They falsify the automatic equation of a cross-sectional slope with a temporal response. [SOURCE: https://arxiv.org/pdf/1910.06732 , sections Results and Methods]

4. **A favorable scaling study still does not find universal budget savings.** Meirelles et al., *Evolution of urban scaling: Evidence from Brazil* (2018), reports sublinear roads and school counts but linear aggregate budget and deviations for sewage and health infrastructure. It starts from5565 municipalities and uses a density-filtered88-municipality main sample, acknowledging these are not exact functional cities. The dependence on public investment/access is part of its proposed mechanism. Physical school counts are not teacher-hours or school expenditure. [SOURCE: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0204574 , Methods and Results]

An important pro-theory reply is Bettencourt et al. (2020), *The interpretation of urban scaling analysis in time*: temporal slopes mix scale with independent time growth and can diverge when population growth approaches zero. Only its abstract/search-indexed material was accessible here; do not treat this note as a full-text review. Independently, the identity log C_it=log a_t+beta log N_it+u_it yields temporal slope beta + (Delta log a_t + Delta u_it)/Delta log N_it. A divergent raw temporal slope alone therefore does not refute a scale mechanism. Time effects and composition must be separated. [SOURCE LIMIT: https://pmc.ncbi.nlm.nih.gov/articles/PMC7061707/ ; independently derived identity]

## Analysis verdict and discriminating test

- **Leading explanation:** lower physical network requirements are a credible component of economies of scale; public spending combines them with labor, service demand, prices and policy. A category mixture is more defensible than a universal exponent. [INFERENCE]
- **Top alternative:** the observed low short-run budget response reflects fixed appropriations or worse service quality, with little durable efficiency. Composition, sorting and grants also explain cross-sectional slopes. [HYPOTHESES]
- **Falsifier/discriminating evidence:** category-specific real-spending panels with stable boundaries, service-user counts, regional input prices and quality measures; compare cross-section with within-place changes and multiple horizons. A robust subunit response that survives these checks supports fiscal scale savings. A slope moving to one after wage/quality adjustment or catching up over time supports prices/budget lags instead. This is a test specification, not identification from controls alone.
- **Decision impact:** retain a labeled 5/6 theoretical sensitivity and use exact finite-change arithmetic. Do not replace the CBO-informed scenario, add a second discount, or book additional GDP/agglomeration benefits from this theory without matched evidence and overlap checks.
- **Next action:** evaluate available US service-level data and carry the construction-sensitive result into the overall model. Do not claim that either .75 or5/6 was empirically estimated for Mexican-origin marginal spending.

## Coverage and reproducibility

Covered: Bettencourt2013 main paper/theory tables; Arcaute et al.2014 preprint main results; Cottineau et al.2015 preprint sensitivity/Table4; Xu et al.2019 preprint results; Meirelles et al.2018 full article. Skipped: reviewing every source's supplemental data, reproducing their regressions, and any current US causal estimation (parent owns);2020 full text was retrieval-blocked. The local topic index had no scaling/Bettencourt/West/Cottineau match, which is a search result rather than proof the entire corpus lacks it.

Numerical calculations were executed with Python standard-library `math`; for each beta evaluate `(1-(1-.12)**beta)/.12`; inverse `log(1-r*.12)/log(1-.12)`. The default uv cache was sandbox-blocked; rerun succeeded with `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run python3`. No private data were sent externally. The Princeton transportation paper was inspected as a search lead but not used because it did not address spending. Search terms that worked: “Bettencourt 2013 origins scaling cities infrastructure 5/6 network derivation”, “urban scaling temporal cross sectional Cottineau Arcaute”, “urban scaling government expenditure”. Retrieved2026-09-20. LLM interpretation remains subject to the project's instrument-bias caveat; empirical claims above are linked to primary sources and model claims are explicitly separated.
