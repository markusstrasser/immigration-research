# IQ Sex Differences - Independent Verification

**Date:** 2026-03-05
**Question:** Does `research/iq-sex-differences-test-construction.md` accurately represent the literature on male-female differences in intelligence?
**Scope note:** The underlying literature is almost entirely about male/female **sex-coded** samples, not "gender" in the broader contemporary sense. This report therefore uses **sex** unless a source explicitly studies gendered social factors.

---

## Summary Verdict

The repo's **main conclusion is broadly correct**: the literature does **not** establish a single stable, battery-independent sex difference in general intelligence `g`. Different batteries and latent models produce **null**, **small male-favoring**, and occasionally **female-favoring** estimates. [SOURCE: Colom et al. 2002, doi:10.1017/S1138741600005801; Deary et al. 2007, doi:10.1016/J.INTELL.2006.09.003; Irwing 2012, doi:10.1016/J.PAID.2011.05.001; Keith et al. 2008, doi:10.1016/J.INTELL.2007.11.001; Reynolds et al. 2022, https://gwern.net/doc/iq/2022-reynolds.pdf; Giofre et al. 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/]

The repo is also on strong ground that the **most replicable differences are domain-specific**, not a universal overall-intelligence gap:

- males tend to score higher on spatial / visual-mechanical tasks [SOURCE: Johnson and Bouchard 2007, doi:10.1016/J.INTELL.2006.03.012; Lemos et al. 2013, doi:10.1016/J.INTELL.2012.10.009; Reynolds et al. 2022, https://gwern.net/doc/iq/2022-reynolds.pdf]
- females tend to score higher on pencil-and-paper processing speed tasks [SOURCE: Keith et al. 2008, doi:10.1016/J.INTELL.2007.11.001; Giofre et al. 2022, doi:10.1007/s10648-022-09705-1; Giofre et al. 2024, https://hdl.handle.net/11577/3536106]
- education can explain substantially more variance than sex in at least some WAIS-IV samples [SOURCE: Daseking et al. 2017, doi:10.1016/J.PAID.2017.04.003]

Several **stronger subclaims should be downgraded**:

1. "Greater male variability ... across all studies" is too strong. Some studies do show greater male variability in composite scores, but it is not universal across latent-`g` analyses or across all domains. [SOURCE: Irwing 2012, doi:10.1016/J.PAID.2011.05.001; Giofre et al. 2024, https://hdl.handle.net/11577/3536106]
2. The precise "fair baseline" estimate of `d ~= -0.085` or "0 to 3 IQ points favoring males" is **exploratory**, not a high-confidence conclusion. It depends on local pooling choices that do not fully solve non-independence or construct heterogeneity. [SOURCE: `sources/iq-sex-diff/meta_analysis.py`]
3. The memo should use **sex** rather than **gender** unless it is explicitly discussing socialization, schooling, teacher expectations, or identity. [INFERENCE]

---

## Evidence Reviewed

### Studies supporting the core repo conclusion

1. **Colom et al. 2002 (Spanish WAIS-III)** found male advantages on some manifest IQ composites but no sex difference in latent `g` using their modeling approach. [SOURCE: doi:10.1017/S1138741600005801]
2. **Deary et al. 2007 (opposite-sex sibling design, ASVAB)** found a very small male-favoring `g` difference (`d` around 0.06 to 0.07) with stronger male overrepresentation in the upper tail. This is not evidence for a large general-intelligence gap. [SOURCE: doi:10.1016/J.INTELL.2006.09.003]
3. **Keith et al. 2008 (WJ-III, ages 6 to 59)** found female advantages in latent processing speed and, for adults, latent `g`, while finding no latent fluid-reasoning advantage for males. This is one of the clearest examples that the estimated direction depends on battery content and structure. [SOURCE: doi:10.1016/J.INTELL.2007.11.001]
4. **Savage-McGlynn 2012 (Raven's SPM+, representative UK sample)** found no significant mean or variance sex difference. [SOURCE: doi:10.1016/j.paid.2011.06.013]
5. **Giofre et al. 2024 (Leiter-3)** again found no general-intelligence difference while still observing some specific task differences. [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/]
6. **Reynolds et al. 2022** summarize the recent literature as showing no meaningful sex difference in general intelligence, but stable differences in some specifics such as female processing speed and male visual processing. [SOURCE: https://gwern.net/doc/iq/2022-reynolds.pdf]

### Studies that justify caution rather than a stronger null

1. **Irwing 2012 (US WAIS-III standardization sample)** found a small male advantage in latent `g`, roughly `d = 0.19` to `0.22`, depending on the model. This is one of the strongest mainstream arguments against a strict null. [SOURCE: doi:10.1016/J.PAID.2011.05.001]
2. **Lemos et al. 2013 (BPR, Brazilian sample)** found a male advantage in latent `g` that grew with age, plus very large male advantages in mechanical reasoning that were only partly attributable to `g`. [SOURCE: doi:10.1016/J.INTELL.2012.10.009]

These papers do **not** overturn the repo's main conclusion. They show that the literature is mixed and that a blanket "there is definitely no male advantage in `g`" would also be too strong. [INFERENCE]

### Studies relevant to specific-ability claims

1. **Johnson and Bouchard 2007** found that `g` can mask larger sex differences in residual ability dimensions, especially male-favoring spatial rotation and female-favoring verbal-memory style dimensions. [SOURCE: doi:10.1016/J.INTELL.2006.03.012]
2. **Giofre et al. 2022** found that WISC batteries show small overall differences, with visual and crystallized abilities tending to favor males, fluid ability differences often negligible, and processing speed favoring females. [SOURCE: doi:10.1007/s10648-022-09705-1]
3. **Hirnstein et al. 2023** found female advantages in phonemic fluency and verbal-episodic memory, which supports the repo's narrower memory / retrieval claim better than the broader `g` literature does. [SOURCE: https://pubmed.ncbi.nlm.nih.gov/35867343/]
4. **Daseking et al. 2017** found that education had a much larger association with WAIS-IV outcomes than sex did in the German sample. [SOURCE: doi:10.1016/J.PAID.2017.04.003]

---

## Claims That Hold Up

1. **There is no settled battery-independent answer for sex differences in `g`.** The literature is mixed in a pattern that tracks battery content and modeling choices more than it tracks a single universal direction. [SOURCE: Colom et al. 2002, doi:10.1017/S1138741600005801; Keith et al. 2008, doi:10.1016/J.INTELL.2007.11.001; Irwing 2012, doi:10.1016/J.PAID.2011.05.001; Reynolds et al. 2022, https://gwern.net/doc/iq/2022-reynolds.pdf]
2. **Male spatial / visual-mechanical advantages are real and robust.** [SOURCE: Johnson and Bouchard 2007, doi:10.1016/J.INTELL.2006.03.012; Lemos et al. 2013, doi:10.1016/J.INTELL.2012.10.009]
3. **Female pencil-and-paper processing-speed advantages are real.** [SOURCE: Keith et al. 2008, doi:10.1016/J.INTELL.2007.11.001; Giofre et al. 2022, doi:10.1007/s10648-022-09705-1]
4. **Education can swamp sex effects in some datasets.** [SOURCE: Daseking et al. 2017, doi:10.1016/J.PAID.2017.04.003]

---

## Claims That Should Be Revised

### 1. Greater male variability

The source memo currently treats greater male variability as nearly universal. That is too aggressive.

- **Irwing 2012** found no significant sex difference in latent-`g` variability in the WAIS-III models he estimated. [SOURCE: doi:10.1016/J.PAID.2011.05.001]
- **Giofre et al. 2024** found male-greater variability in some broad domains and composite scores, but female-greater variability in processing speed. [SOURCE: https://hdl.handle.net/11577/3536106]

**Recommended wording:** greater male variability is **common in several composite and domain measures**, and often matters for tail ratios, but it is **not universal across all latent-`g` analyses or all cognitive domains**. [INFERENCE]

### 2. Exact "fair baseline" IQ-point estimate

The local script `sources/iq-sex-diff/meta_analysis.py` usefully explores how results shift when different subtests are excluded, but it should not be treated as establishing a precise causal or psychometric baseline.

Problems:

- it explicitly notes unresolved non-independence among effect sizes [SOURCE: `sources/iq-sex-diff/meta_analysis.py`, lines 12-15]
- it mixes `FSIQ` and `AFQT/ASVAB`-style composites under a single broad bucket [SOURCE: `sources/iq-sex-diff/meta_analysis.py`]
- its "without knowledge / DIF-biased subtests" result is a defensible sensitivity analysis, not a validated gold-standard construct [SOURCE: `sources/iq-sex-diff/meta_analysis.py`]

**Recommended wording:** the script suggests that removing some knowledge-heavy or suspected DIF-heavy measures pushes the pooled estimate toward a **small male advantage**, but the exact value should be labeled **exploratory** rather than definitive. [INFERENCE]

### 3. "Gender" vs "sex"

The memo should stop saying "gender and intelligence" unless it is explicitly discussing gendered environments, socialization, or identity. The psychometric literature reviewed here is about sex-coded samples and measured test performance. [INFERENCE]

---

## Causal Check

**Observation:** Estimates of male-female difference in latent `g` vary from female-favoring to null to small male-favoring, while sex differences in specific domains such as spatial ability and processing speed are more stable. [SOURCE: Keith et al. 2008, doi:10.1016/J.INTELL.2007.11.001; Irwing 2012, doi:10.1016/J.PAID.2011.05.001; Reynolds et al. 2022, https://gwern.net/doc/iq/2022-reynolds.pdf]

**Null:** If the true overall sex difference in general intelligence is near zero or small, then batteries that weight speed, fluency, spatial, or mechanical content differently should produce different latent-`g` estimates without requiring a large underlying population gap. [INFERENCE]

**Residual after null:** Some batteries still lean male and some composite scores still show male overrepresentation in the upper tail, so a strict universal null remains unproven. [SOURCE: Irwing 2012, doi:10.1016/J.PAID.2011.05.001; Deary et al. 2007, doi:10.1016/J.INTELL.2006.09.003]

**Most likely cause (70%):** battery composition plus latent-model specification are the main drivers of why the literature points in different directions. [INFERENCE]

**Top alternative (20%):** there is a true small male advantage in `g`, and null or female-favoring findings mostly reflect batteries that overweight processing speed / fluency or under-measure the highest `g` spatial-fluid tasks. This alternative is weaker because it does not explain the full spread of null results on Raven's, Leiter-3, and some balanced batteries. [SOURCE: Savage-McGlynn 2012, doi:10.1016/j.paid.2011.06.013; Giofre et al. 2024, https://pmc.ncbi.nlm.nih.gov/articles/PMC11541283/]

**Falsifier:** a preregistered, representative, measurement-invariant, multi-battery study that finds the same sex gap direction and magnitude across balanced batteries and across alternative factor models. [INFERENCE]

**Decision impact:** keep the repo's core claim that there is **no settled battery-independent gap**, but soften the variability language, downgrade the exact IQ-point estimate, and use **sex** rather than **gender**. [INFERENCE]

---

## Recommended Edits to the Source Memo

1. Keep the central conclusion, but rephrase it as: "The literature does not establish a battery-independent sex difference in general intelligence."
2. Replace the universal variability claim with a narrower statement that greater male variability is common but not universal.
3. Re-label the local pooled `d ~= -0.085` result as exploratory.
4. Replace "gender" with "sex" unless the memo is explicitly about socialization or educational environment.
5. Preserve the domain-specific findings on spatial ability, processing speed, and memory / fluency, which are better supported than any single headline claim about `g`.

---

## Related Next Question

The popular-culture argument the memo does **not** answer is:

1. how much of these observed differences are caused by schooling, practice, and socialization rather than latent ability
2. whether small subability differences, especially in processing speed, have any meaningful relationship to productivity, earnings, or long-run life outcomes

That is a separate causal and criterion-validity question. See `notes/iq-sex-differences-context-open-questions.md`. [INFERENCE]
