# Counter-Review: Adversarial Pushback on Gemini's Corrections

**Models:** Claude Sonnet 4.6 (adversarial role), Perplexity Reasoning Pro (web-grounded verification)
**Date:** 2026-03-04
**Purpose:** Stress-test the three corrections Gemini 3.1 Pro proposed

## The Three Contested Claims

### CLAIM 1: "No sex difference in latent g" (Johnson & Bouchard 2007)

**Gemini said:** No g difference, only visualization. We should have mentioned this.

**Counter-evidence (Sonnet + Perplexity):**
- **Irwing (2012) found a male g advantage of d=0.19-0.22 on US WAIS-III standardization data** — directly contradicts J&B. [SOURCE: Perplexity, citing gwern.net/doc/iq/2012-irwing.pdf]
- J&B used ONE battery (Project Talent). Not robustly replicated.
- **Battery composition determines g extraction** — if verbal/memory dominated, g absorbs female strengths. If spatial-heavy, g absorbs male strengths. (Sonnet)
- Brain volume: males ~10% larger corrected for body size, brain-IQ correlation r≈0.3-0.4. This creates a biological prior that "no g difference" has to explain. (Sonnet)
- Sonnet probability: **25%** that "no g difference" is correct.

**My assessment:** Gemini oversold this as settled. The evidence is genuinely contested. Irwing (2012) is a direct empirical counter using better data (US standardization sample vs Project Talent). **Correct action: present both J&B and Irwing, note the disagreement, don't claim settled.**

### CLAIM 2: "Female processing speed d=0.4-0.6 globally, Italian data is outlier"

**Gemini said:** Roivainen (2011) shows global female PS advantage. Italy is the outlier, not Netherlands.

**Counter-evidence (Sonnet):**
- Italian WAIS-IV is a nationally representative standardization sample — dismissing it as "outlier" is circular (keeps data that agrees, removes data that disagrees)
- Cross-national variation (d=0.02 to d=0.71) is **signal, not noise** — suggests cultural/educational mediation, not biological universal
- WAIS PS subtests confounded by fine motor speed and clerical training — reaction time paradigms show smaller/inconsistent sex differences
- Sonnet estimate of "true" cross-nationally stable effect: **d≈0.2-0.3**, not 0.4-0.6
- Sonnet probability: **35%** that d=0.4-0.6 is the right number

**My assessment:** Sonnet is partly right. The Italian data shouldn't be dismissed without a principled criterion. But Roivainen (2011) and US WAIS-IV data both show substantial female PS advantages. **Correct action: report the range honestly (d=0.02-0.71), cite the Roivainen global review (d≈0.4-0.6), note Italy as a discrepant finding requiring explanation, don't call either an "outlier."**

### CLAIM 3: "DIF-free subtests → 0-1 IQ points"

**Gemini/Flash said:** Restrict to Vocabulary, Similarities, Matrix Reasoning → gap vanishes.

**Counter-evidence (Sonnet — strongest attack):**
- **DIF analysis is circular in this application:** It removes items where males outperform *after controlling for the latent trait*. But if males genuinely have higher ability, DIF flags those items as "biased" by assumption. You remove the differences, then conclude there are no differences.
- Borsboom (2006) argued DIF cannot distinguish genuine ability differences from bias without an independent criterion — which we lack.
- The three subtests chosen (Vocab, Sim, MR) are **not representative** — they're specifically the subtests with smallest sex differences. This is post-hoc cherry-picking rationalized through DIF.
- Measurement invariance ≠ equal latent means. Configural/metric invariance is compatible with real mean differences.
- Sonnet probability: **15%** that restricting to DIF-free subtests reflects reality

**My assessment:** This is the most devastating counter-argument. The circularity critique (Borsboom) is valid and important. DIF analysis **assumes** equal latent means to detect bias. If the latent means actually differ, DIF will incorrectly flag genuinely differentiating items as "biased." **Correct action: present DIF findings but acknowledge the circularity problem. Don't claim DIF-restriction gives the "true" answer.**

## Revised Confidence After Both Rounds

| Claim | Gemini confidence | After adversarial review | Status |
|-------|------------------|------------------------|--------|
| No g difference | HIGH (adopted) | **CONTESTED** — Irwing 2012 directly contradicts. Battery-dependent. | Downgrade to presenting both sides |
| Female PS d=0.4-0.6 | HIGH (adopted) | **MODERATE** — Real effect but Sonnet right that d=0.2-0.3 may be more defensible cross-nationally | Widen the range, don't call Italy outlier |
| DIF-free → 0-1 pts | MEDIUM (adopted) | **WEAK** — Circularity problem is real. This is a philosophical argument about construct validity, not an empirical finding | Flag circularity explicitly |
| Male FSIQ advantage 2-4 pts | MEDIUM | **STABLE** — Neither round seriously challenged the manifest FSIQ direction | Keep |
| Greater male variability | HIGH | **STABLE** — Nobody challenged this | Keep |

## Net Assessment After Both Review Rounds

The truth is messier than either Gemini or the adversarial review suggests:

1. **There may or may not be a sex difference in latent g** — it depends on the battery and the extraction method. Irwing (2012) says yes (d=0.19-0.22). Johnson & Bouchard (2007) says no. This is genuinely unresolved.

2. **Female PS advantage is real but the magnitude is uncertain** (d=0.2-0.6 depending on country, test version, and motor confounds).

3. **DIF analysis cannot settle whether subtests are "biased" or "genuinely differentiating"** without an independent criterion. Both interpretations are logically defensible.

4. **Manifest FSIQ: males ~2-4 points higher** — this is the most stable finding, replicated across multiple countries and WAIS versions.

5. **The composition of the test determines the answer** — this was the original insight and it survives all rounds of review.
