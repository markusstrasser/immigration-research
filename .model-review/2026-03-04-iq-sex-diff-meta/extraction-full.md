# Extraction: All Claims from Cross-Model Review

## Gemini 3.1 Pro (Pattern/Architecture Review)

G1. Processing Speed conclusion is backward — Dutch d=0.71 is NOT the outlier; Italian d=0.02 IS. Roivainen (2011) shows global female PS advantage d≈0.40-0.60. US WAIS-IV shows d≈0.53.
G2. "Verbal=female" over-extrapolation — WAIS Vocabulary ≠ all verbal ability. Female advantage is in writing, reading comprehension, verbal fluency (Hedges & Nowell 1995; Halpern 2012).
G3. Maturational confound is too clean — gray/white matter volume trajectories don't map linearly to g_f maturation.
G4. Flynn cross-national data missed — in high gender-egalitarian nations, adult women match or exceed men on Raven's (Flynn 2012).
G5. Latent g vs manifest scores missed — Johnson & Bouchard (2007) found no sex difference in latent g, only in visualization factor.
G6. Gender-Equality Paradox ignored — Italy and Netherlands have vastly different gender-equity profiles, likely explaining heterogeneity.
G7. US WAIS-IV standardization data excluded — N=2,200, females score higher on PS (d≈0.53).
G8. Fixed-effects model invalid across heterogeneous populations — must use random-effects.
G9. Pooled correlated errors — 36 subtests from 3 samples treated as 36 independent studies. Subtests correlated r≈0.3-0.7. CIs artificially narrow.
G10. Cannot average d across subtests — must weight by g-loading. Averaging Matrix Reasoning with Cancellation warps measurement.
G11. Replace with random-effects (DerSimonian-Laird or REML).
G12. Use Robust Variance Estimation for correlated data.
G13. Add US WAIS-IV data to resolve processing speed discrepancy.
G14. Use MG-CFA on latent g, not manifest FSIQ.
G15. Audit Lynn & Irwing (2004) exclusion criteria against Flynn (2012).
G16. Separate spatial/visualization advantage from strict fluid reasoning (g_f).
G17. Self-doubt: Gemini biased AGAINST biological essentialism by post-training. May over-weight environmental/methodological explanations.
G18. Self-doubt: Cannot run MG-CFA independently. Relying on other researchers' summaries.
G19. Self-doubt: "No g difference" defense may be irrelevant if intelligence = manifest real-world skills (where spatial/numerical matter).

## Gemini Flash (Quantitative Audit)

F1. Unit-of-analysis error: 36 effects from 3 samples treated as independent. SE artificially shrunk.
F2. True precision likely 3-4x lower than reported.
F3. Fixed-effects invalid — Q=70 for processing speed explicitly rejects the assumption.
F4. Random-effects CI for processing speed would likely cross zero.
F5. "Outlier" is a narrative label with N=2 countries — not statistically justified.
F6. If Italian data (larger N) is more representative, no female PS advantage existed to balance against.
F7. DIF on Information means it measures something other than g — including it guarantees male advantage.
F8. Removing Information eliminated VCI sex difference in Dutch study.
F9. Maturational hypothesis is a just-so story — needs longitudinal ages 20-50 to falsify.
F10. If gap grows after 25, maturation is false. If shrinks historically (WAIS-R vs IV), environment.
F11. Arithmetic is most "schooled" subtest — confounded by math education, STEM exposure.
F12. Arithmetic gap narrowing (WAIS-R d=-0.57 → WAIS-IV d=-0.47) correlates with educational convergence.
F13. FSIQ male advantage exists ONLY because WAIS includes biased Information + Arithmetic while PS vanished.
F14. Restricting to DIF-free subtests (Vocabulary, Similarities, Matrix Reasoning) drops gap to ≈0-1 pts.
F15. "Males would score 5 pts higher" is statistically fragile.
F16. Sex difference in IQ is a residual of weighting choices — change weights, change the gap.

## Disposition Table

| ID | Claim (short) | Disposition | Reason |
|----|--------------|-------------|--------|
| G1 | Processing speed: Italian is outlier, not Dutch | **INCLUDE — CRITICAL** | Roivainen (2011) + US data cited. MUST VERIFY. Overturns a key finding. |
| G2 | WAIS Vocabulary ≠ all verbal ability | **INCLUDE** | Valid — our memo over-extrapolated from IQ subtests to "verbal ability" broadly |
| G3 | Maturational confound too clean | **INCLUDE** | Fair — we labeled it [INFERENCE] but could hedge more |
| G4 | Flynn: women match men on Raven's in egalitarian nations | **INCLUDE — VERIFY** | If true, undermines Lynn's 5-point adult advantage. Must check source. |
| G5 | Johnson & Bouchard: no latent g difference | **INCLUDE — VERIFY** | Critical finding we missed. g vs manifest FSIQ is the key distinction. |
| G6 | Gender-Equality Paradox as confound | **INCLUDE** | Valid — we pooled Italy and Netherlands without addressing cultural differences |
| G7 | Add US WAIS-IV data | **INCLUDE — ACTION** | Most scrutinized dataset in the world, we excluded it |
| G8 | Fixed-effects invalid | **INCLUDE — CRITICAL** | Both reviewers flagged independently. Must fix meta-analysis code. |
| G9 | Correlated subtests treated as independent | **INCLUDE — CRITICAL** | Both reviewers flagged. CIs are wrong. |
| G10 | Must weight by g-loading not simple average | **INCLUDE** | Valid methodological point |
| G11 | Use random-effects | **INCLUDE — ACTION** | Fix the code |
| G12 | Use RVE for correlated data | **INCLUDE — ACTION** | Fix the code |
| G13 | Add US WAIS-IV data | **MERGE WITH G7** | Same recommendation |
| G14 | Use MG-CFA on latent g | **DEFER** | Requires raw data, not just published effect sizes |
| G15 | Audit Lynn vs Flynn | **INCLUDE** | Good research direction |
| G16 | Separate spatial from fluid reasoning | **INCLUDE** | Valid — Raven's loads on both |
| G17 | Gemini biased against biological explanations | **INCLUDE — META** | Important self-awareness. Flag in synthesis. |
| G18 | Cannot run MG-CFA independently | **INCLUDE — META** | Limitation of review |
| G19 | Manifest skills may matter more than latent g | **INCLUDE** | Valid philosophical counterpoint |
| F1 | Unit-of-analysis error | **MERGE WITH G9** | Same finding |
| F2 | Precision 3-4x lower | **INCLUDE** | Quantifies the impact of G9 |
| F3 | Fixed-effects invalid (Q=70) | **MERGE WITH G8** | Same finding |
| F4 | Random-effects PS CI crosses zero | **INCLUDE** | Important quantitative prediction |
| F5 | "Outlier" unjustified with N=2 | **INCLUDE** | Valid — we were too confident |
| F6 | No PS advantage to balance against | **INCLUDE** | Logical consequence if Italian data representative |
| F7 | DIF means Information measures non-g | **INCLUDE** | Strengthens our DIF finding |
| F8 | Removing Information eliminates VCI gap | Already in memo | |
| F9 | Maturational hypothesis = just-so story | **INCLUDE** | Harsh but fair. Needs falsification criteria. |
| F10 | Falsification: gap after 25, historical trend | **INCLUDE** | Concrete prediction |
| F11 | Arithmetic confounded by education | **INCLUDE** | Critical alternative explanation we missed |
| F12 | Arithmetic narrowing = educational convergence | **INCLUDE** | Evidence FOR education confound |
| F13 | FSIQ male adv = biased subtests | **INCLUDE** | Strong counter-argument |
| F14 | DIF-free subtests → ≈0-1 pts | **INCLUDE — KEY** | This is the strongest counter-finding |
| F15 | "5 pts higher" is fragile | **INCLUDE** | Agrees with our hedged conclusion |
| F16 | Gap is a residual of weighting | Already in memo | We said this |

## Coverage
- Total extracted: 35 unique (after merges)
- INCLUDE: 27
- MERGE: 4 (→ deduplicated)
- DEFER: 1 (MG-CFA requires raw data)
- Already in memo: 2
- META (self-awareness): 3
