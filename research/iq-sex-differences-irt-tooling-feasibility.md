# IQ Sex Differences - IRT Tooling Feasibility

**Date:** 2026-03-07  
**Purpose:** record what the local environment can and cannot honestly support for the next psychometric step on the `PISA` branch.

## Bottom Line

The repo can now do strong local hybrid psychometric passes.

It cannot yet do a clean weighted joint multi-group latent-variable analysis in the current local stack without a bigger tooling change. [INFERENCE]

## What Is Locally Feasible

### 1. `girth` is viable for unweighted Rasch work

The local environment now has `girth` in the project environment. It supports at least:

- `rasch_mml`
- `rasch_jml`
- `rasch_conditional`
- `ability_eap`

[SOURCE: `sources/iq-sex-diff/pyproject.toml`; `sources/iq-sex-diff/pisa2018_dif_rasch_pass.py`; `sources/iq-sex-diff/pisa2018_dif_theta_logit_pass.py`]

That was enough to run:

- the anchored-Rasch sensitivity
- the latent-anchor `theta` DIF pass

[SOURCE: `research/iq-sex-differences-pisa2018-dif-rasch.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`]

### 2. `py-irt` is installable, but no explicit survey-weight or multi-group support surfaced in the quick probe

Local inspection showed:

- model classes like `OneParamLog`, `TwoParamLog`, `ThreeParamLog`, `FourParamLog`, `Multidim2PL`
- no obvious public package surface for survey weights
- no obvious public package surface for multiple-group invariance / DIF by group

[SOURCE: local package probe in session; `rg` over installed `py_irt` package for `weight|sample_weight|group|multigroup|country|covariate` returned no explicit survey-weight or multi-group API path]

This is a tooling observation, not a claim that `py-irt` is unusable in principle. [INFERENCE]

## What Is Not Currently Feasible Cleanly

### 1. `R`-based `mirt` / `TAM` route

`Rscript` is not installed in the current environment.

[SOURCE: local shell probe in session]

That blocks the easiest common route to richer multi-group IRT without changing the environment. [INFERENCE]

### 2. Honest weighted joint multi-group IRT in the current local stack

The local passes now cover:

- weighted fixed-effects binomial DIF
- unweighted anchored Rasch sensitivity
- weighted binomial DIF conditioned on latent anchor `theta`

They do **not** yet provide:

- one joint latent model with group structure and survey weights handled together
- a clean local replacement for the missing `TIMSS` item-response route

[SOURCE: `research/iq-sex-differences-pisa2018-dif-logit.md`; `research/iq-sex-differences-pisa2018-dif-rasch.md`; `research/iq-sex-differences-pisa2018-dif-theta-logit.md`; `research/iq-sex-differences-timss-public-item-wall.md`]

## Decision Impact

The next psychometric move is now a real tooling decision, not another analysis-script tweak.

The realistic options are:

1. install a richer IRT stack or external environment that supports weighted joint multi-group estimation
2. stop the local public `PISA` branch here and move to the restricted-data / mediator frontier

[INFERENCE]
