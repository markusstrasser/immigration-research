**Confirmed Issues**

1. **Non-significant employment effect is still written as a realized drop**

Evidence:
- `research/immigration-causal-everify-card-vs-borjas.md:11`: “stable W-2 employment ... fell ~6% post-treatment (t=-1.40, marginal).”
- `research/immigration-causal-everify-card-vs-borjas.md:80`: E1 employment `t=-1.40`
- `research/immigration-causal-everify-card-vs-borjas.md:87`: “E1 stable-employment ... fell ~6%”
- `CYCLE.md:29`: “E-Verify mandates show a ~6% drop ... (marginal).”

Why invalid/too strong:
`t=-1.40` is not conventionally significant and “marginal” is doing too much. The design supports a negative point estimate, not a confirmed employment drop.

Minimal fix:
Replace “fell ~6%” / “show a ~6% drop” with “had a negative, statistically nonsignificant point estimate of about −6%” and avoid treating it as a measured employment decline.

2. **Causal synthesis still says E-Verify-style labor-supply contraction**

Evidence:
- `research/immigration-causal-synthesis-2026-04-18.md:30`: “large Borjas-style native wage gains from E-Verify-style labor-supply contraction”
- But the source memo says QWI does not directly observe total unauthorized labor supply:
  - `research/immigration-causal-everify-card-vs-borjas.md:110`: QWI cannot distinguish true labor-supply contraction from cash work, hours, composition, etc.
  - `research/immigration-causal-everify-card-vs-borjas.md:130`: cash-economy substitution weakens interpretation of QWI E1 drop as full labor-supply contraction.

Why invalid/too strong:
The synthesis reintroduces a measured-labor-supply-contraction framing that the source memo explicitly walked back. The observed treatment is mandate timing, not measured labor supply contraction.

Minimal fix:
Change line 30 to “large Borjas-style native wage gains under observed E-Verify mandate variation.”

3. **E-Verify memo still labels comparison-study signs as “Card” / “Anti-Borjas” too globally**

Evidence:
- `research/immigration-causal-everify-card-vs-borjas.md:162`: this analysis sign = “Card”
- `research/immigration-causal-everify-card-vs-borjas.md:163`: Foged-Peri sign = “Anti-Borjas”
- `research/immigration-causal-everify-card-vs-borjas.md:166`: later caveat says these designs do not identify one shared mechanism or rule out small effects.

Why invalid/too strong:
The table’s “Sign” column compresses heterogeneous designs into debate labels, while the surrounding text says the evidence is bounded and not global. “Anti-Borjas” especially overstates a distinct Danish dispersal design as a verdict against the Borjas family.

Minimal fix:
Rename column to `Directional reading in this design`; replace “Card” with “no detected adverse/positive large native wage effect” and “Anti-Borjas” with “cuts against large native loss in that setting.”

4. **Caplan audit still uses a near-global “American workers” conclusion from partial evidence**

Evidence:
- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md:52`: “Immigration restrictions are not necessary to protect American workers” verdict “Too broad”
- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md:109`: constrained counties show slower wage growth.
- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md:111`: “better-developed concern is ... slower wage progression in constrained places.”
- `research/immigration-bryan-caplan-claims-audit-2026-04-21.md:306`: “admitting wage-growth pressure in constrained places.”

Why too strong:
The underlying evidence is county association and projections, not a clean worker-protection necessity test. “Admitting wage-growth pressure” reads as established pressure rather than a supported concern/signal in constrained places.

Minimal fix:
Change “wage-growth pressure” to “evidence consistent with wage-growth pressure” or “a constrained-place wage-growth concern.”

5. **Capacity frontier bottom line says “cleaner signal” without enough descriptive qualifier**

Evidence:
- `research/immigration-capacity-frontier-2026-04-21.md:10`: “For wage growth, employment growth, and native net migration, the cleaner signal is not stock share. It is recent immigrant flow relative to local permit capacity.”
- `research/immigration-capacity-frontier-2026-04-21.md:62`: scope note says table patterns are not clean causal effects.
- `research/immigration-capacity-frontier-2026-04-21.md:283`: causal identification still needs stronger counterfactual design.

Why too strong:
“Cleaner signal” is not wrong statistically, but in the bottom line it can read like the correct explanatory variable rather than the strongest descriptive model predictor.

Minimal fix:
Change to “the cleaner descriptive model signal” or “the strongest current descriptive signal.”

6. **Crime memo still overstates Lott critique by saying “fundamental data classification error” in narrative**

Evidence:
- `research/immigration-crime-rates-unauthorized-vs-native-born.md:13`: “has been criticized for a fundamental data classification error”
- `research/immigration-crime-rates-unauthorized-vs-native-born.md:102`: “The study has been criticized for a fundamental data classification error”
- But the corrected status is narrower:
  - `research/immigration-crime-rates-unauthorized-vs-native-born.md:207`: “SUPPORTED CRITIQUE — not independent reanalysis”
  - `research/immigration-conclusion-audit-running-fixes.md:1374`: critiques are not independent verification.

Why too strong:
The memo’s current table correctly downgrades the claim, but the narrative still presents the classification error as if established. The evidence supports “serious unresolved classification critique,” not verified flaw.

Minimal fix:
Replace “criticized for a fundamental data classification error” with “criticized for a serious possible immigration-status classification problem.”

**Speculative / Lower Priority**

- `research/immigration-confidence-ladder.md:92` still includes “welfare implication for rent burden” in the title, although line 94 narrows it to renter-incidence and says aggregate welfare loss is unmeasured. This is mostly a heading hazard; a safer title is “renter-incidence implication.”
- `research/immigration-causal-surge-2021-2024.md:221` says “flows were real and large (~50K/month sustained 2023-2024),” but the corrected table elsewhere uses Total-CBP values in the 145K-302K range. This may be a universe mismatch, not necessarily wrong, but the line should name which flow series the 50K/month refers to.
