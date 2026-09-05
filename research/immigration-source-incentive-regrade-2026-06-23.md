# Source-incentive regrade — an uncalibrated review heuristic

**Date:** 2026-06-23; interpretation corrected 2026-09-05.

**Verdict:** The source-incentive formula is a reproducible prioritization heuristic, not a calibrated truth probability, information weight, bias correction or validation of the immigration conclusions. An official source can accurately report a limited estimand; an advocacy source can report valid data. Claims still require source/method/population review. [SOURCE: local `build_source_incentive_grades.py`; INFERENCE]

## Historical rule, preserved exactly

```
base_weight  : govt_nonpartisan 1.0 | academic 0.8 | think_tank 0.6 | advocacy 0.4
against_interest      : restrictionist source → benefit finding,  OR  expansionist → cost finding
with_interest_advocacy: advocacy outlet whose finding confirms its own prior
adj_weight = min(1.0, base × (1.5 if against_interest else 0.7 if with_interest_advocacy else 1.0))
```

The weights and 1.5/0.7 multipliers have not been calibrated against held-out true/false claims or measured source error rates. Whether a finding is against a source’s interest is itself an interpretation. Contrary-to-prior publication may be informative under a specified selection model, but its evidential value is not supplied by these multipliers. [INFERENCE]

The implementation consults source stance and finding direction to classify against-interest results; calling it literally direction-blind was inaccurate. Symmetric treatment of political labels is a design choice, not proof of unbiased source selection or reliable conclusions. Equal mean weights would not prove unbiasedness, and the historical 0.63 cost versus 0.76 benefit means do not measure the literature’s true evidence balance. [SOURCE: local builder; INFERENCE]

## Historical table output (not probabilities or current claim verification)

| adj | source | finding | why |
|----:|--------|---------|-----|
| **1.0** | NAS 2016/17 panel | mixed | establishment panel publishing the <HS cost *and* the 2nd-gen benefit |
| **1.0** | CBO federal (surge cut deficit) | benefit | nonpartisan |
| **1.0** | CBO state-local cost | cost | nonpartisan |
| **1.0** | **Borjas — immigration surplus +** | benefit | **against-interest**: the field's skeptic deriving a positive aggregate |
| **1.0** | NAS — 2nd-gen contribution | benefit | nonpartisan panel |
| 0.8 | Borjas — low-skill wage harm | cost | academic, with-interest (standard weight) |
| 0.8 | Razin-Wahba — fiscal leakage | cost | academic, with-interest |
| 0.8 | Card/Peri, Clemens, Colas-Sachs, Cortes, AJKM, Ottaviano-Peri | benefit | academic, with-interest |
| **0.28** | **ITEP** — immigrants pay $X tax | benefit | expansionist advocacy confirming its prior |
| **0.28** | **Cato** — immigration benefits | benefit | expansionist advocacy |
| **0.28** | **FAIR** — high fiscal cost | cost | restrictionist advocacy confirming its prior |
| **0.28** | **CIS/Camarota** — welfare-use cost | cost | restrictionist advocacy |

## What can and cannot be concluded

The displayed 0.28 for an advocacy source is the arithmetic `0.4×0.7`; it does not mean 28% credibility or 72% probability of falsehood. A score of1.0 is not certainty. The arithmetic remains unchanged so the previous output is inspectable; its interpretation is corrected. [RECALCULATION; INFERENCE]

The table cannot establish that media claims are advocacy-inflated, that an aggregate benefit survives empirical disconfirmation, or that a wage-loss estimate is real. Borjas’s positive immigration-surplus result is a model result under its assumptions, not a welfare theorem over every omitted channel. NAS age/education fiscal cells, CBO projections and academic wage estimates concern different populations and outcomes. [INFERENCE]

CBO60165 projects approximately $897B lower federal deficits over2024–2034 for its surge counterfactual, covering revenues, mandatory spending and net interest. Discretionary appropriations and state/local budgets are excluded; the approximately $0.2T discretionary illustration is a scenario. This is not realized all-government or incumbent-welfare evidence. [SOURCE: https://www.cbo.gov/publication/60165]

Use the heuristic to select claims for closer review and expose judgments about incentives. Do not use it to average incompatible estimates, aggregate “truth scores,” certify coverage or stop disconfirmation. The parent is correcting builder/output labels while retaining the formula. [INFERENCE]

## Reproduction scope

The historical table was `source_incentive_grades`. Check the current warehouse path/schema before running the old SQL; an unchanged numeric formula does not validate the source labels or conclusions. No warehouse rebuild or formula change was performed in this memo repair.

## Revisions

- **2026-09-05 — Separated reproducible heuristic scores from evidential validity.** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Earlier dated revision entries describe the historical state, including superseded conclusions.
