---
date: 2026-09-20
concept: later-generation-population-measurement
status: adopted
provenance: user-authorized GSS/Pew/NLSY integration and PSID completeness audit
---

# 2026-09-20: Estimate aggregate generations while preserving unknown records

## Context

The partial CPS split leaves 9.399m later-generation Mexican-identifying people
without sufficiently resolved grandparent history. Adjacent annual interviews
recover few candidate histories; the user authorized survey integration and a
PSID exact-generation completeness audit.

## Alternatives considered

1. Apply a Hispanic-name classifier: wrong missing variable, and public CPS has no names.
2. Extend co-resident child proportions to all adults: selection and age mismatch.
3. Average GSS, Pew and NLSY shares: incompatible time, cohort and identity targets.
4. Age-standardize recent GSS, preserve missingness endpoints, and use historical
   sources as independent checks: executable and auditable, but conditional on transport.
5. Wait for exact PSID pedigrees: relevant for G4/G5, but access and statistical
   adequacy remain unresolved; not necessary to publish the conditional aggregate estimate.

## Decision

Adopt option4 as a separate aggregate model. Preserve canonical observed CPS
labels and fiscal outputs. Show central assumptions, missing-grandparent and
missing-age endpoints, and conditional sampling uncertainty separately. Do not
assign ancestry from income and then treat resulting outcome gaps as observed.
Prepare PSID acquisition and completeness rules without claiming unobserved counts.

## Evidence

[Executed estimates and independent checks](../research/immigration-later-generation-estimates-2026-09-20.md):
GSS central estimates are stable within a modest specification range, while
historical Pew is lower and the NLSY/GSS birth-cohort comparison is imprecise.
Neither agreement nor discrepancy justifies silently pooling the sources.

## Revisit if

Recent representative family histories, authenticated PSID extracts with
adequate linked support, or a validated source-to-target selection model become
available. Exact G4/G5 remains a different measurement question.

## Supersedes

None. Extends the observed-generation evidence without replacing its definitions.
