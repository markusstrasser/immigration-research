# Steven Camarota / CIS (2024) Testimony Audit

**Question:** Is Steven Camarota's January 11, 2024 testimony, "The Cost of Illegal Immigration to Taxpayers", propaganda or legitimate evidence?
**Date:** 2026-03-13

---

## Verdict

Best classification: **advocacy testimony with some legitimate evidence, not a neutral fiscal estimate**. [INFERENCE]

That means:

- **not fabricated**: it cites real data sources, uses a recognizable fiscal mechanism, and flags some of its own caveats. [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf]
- **not neutral**: it was prepared for a House hearing explicitly framed around the costs of illegal immigration, and CIS openly describes itself as pursuing a `pro-immigrant, low-immigration vision`. [SOURCE: https://docs.house.gov/Committee/Calendar/ByEvent.aspx?EventID=116727] [SOURCE: https://cis.org/Center-For-Immigration-Studies-Background]
- **not cleanly admissible as a baseline number**: its biggest claims are constructed from model choices, status imputations, and a restrictionist attribution frame rather than direct government measurement. [SOURCE: https://www.ssa.gov/policy/docs/ssb/v85n2/v85n2p1.html] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC9107075/] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC12439705/] [SOURCE: https://doi.org/10.24149/wp1704]

## What is legitimate in it

### 1. The core mechanism is mainstream

The testimony's central causal story is that lower education tends to imply lower earnings, lower tax payments, and higher use of some means-tested programs. That part is legitimate and consistent with mainstream immigration-fiscal work. [SOURCE: https://doi.org/10.24149/wp1704] [SOURCE: https://www.nap.edu/catalog/23550/the-economic-and-fiscal-consequences-of-immigration]

### 2. Local burden examples are real

New York, Chicago, Denver, and Massachusetts really did report large recent shelter and related costs. Those examples are not invented, though the testimony selects the most stressed jurisdictions. CBO's 2025 state/local report independently supports the broader point that recent surge costs were real and concentrated in education, shelter, and border-response categories. [SOURCE: https://www.cbo.gov/publication/61256]

### 3. It admits some uncertainty

The testimony explicitly says some population estimates are preliminary and that some benefit-cost numbers are rough approximations. That makes it better than pure slogan material. [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf]

## What is advocacy or model-dependent in it

### 1. The `$68,390` lifetime drain is **not** a National Academies estimate

This is the single biggest problem. Camarota says he takes the National Academies' education-specific fiscal scenarios, averages all eight scenarios, then applies CIS legality adjustments. That makes the result his constructed estimate, not a National Academies estimate for illegal immigrants. It should never be cited as if NAS itself found `-$68k` per illegal immigrant. [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf] [SOURCE: https://www.nap.edu/catalog/23550/the-economic-and-fiscal-consequences-of-immigration]

### 2. It uses a broad, loaded definition of `illegal immigrant`

Camarota counts many parolees and people with pending asylum cases as illegal immigrants because they were not formally admitted and remain deportable. That is a restrictionist legal framing, not a neutral statistical convention. CBO's recent surge work instead uses the mixed-status category `other foreign nationals`, explicitly noting that some had permission to enter or remain and some did not. [SOURCE: https://www.cbo.gov/publication/60165]

### 3. It counts costs of U.S.-born children as costs of illegal immigration

That is a defensible local-budget-incidence frame, but it is not the only legitimate frame. It is also the largest swing factor in immigration fiscal analysis. If you count K-12 and welfare costs of U.S.-born children against the immigrant parent, but do not symmetrically count those children's later tax contributions, the result becomes much more negative. That issue is central in NAS, Orrenius, and later debates. [SOURCE: https://doi.org/10.24149/wp1704] [SOURCE: https://www.urban.org/sites/default/files/publication/90796/state_and_local_fiscal_effects_of_immigration.pdf]

### 4. Its welfare estimates are imputation-heavy

The `59.4%` welfare-use figure and the `$42B` welfare-cost estimate depend on CIS assigning illegal status probabilistically in SIPP, then approximating program costs from recipient shares. That is not an official government estimate. It is a model output built on inferred status and rough allocation. Recent methods papers explain why this is fragile. [SOURCE: https://www.ssa.gov/policy/docs/ssb/v85n2/v85n2p1.html] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC9107075/] [SOURCE: https://pmc.ncbi.nlm.nih.gov/articles/PMC12439705/]

### 5. Its tax estimates depend on dated compliance assumptions

The testimony's tax totals rely in part on the assumption that about `55%` of illegal-immigrant earnings are taxed "on the books", a CIS assumption with a long lineage in Camarota's work. That makes the tax numbers plausible as rough estimates, but not clean measurement. [SOURCE: https://www.congress.gov/118/meeting/house/116727/witnesses/HHRG-118-JU01-Wstate-CamarotaS-20240111.pdf]

### 6. The GDP paragraph is rhetorically sharper than the literature

The testimony says almost all added GDP goes to illegal immigrants themselves. That is too strong as a general economics statement. Immigration can also affect prices, complementary labor, returns to capital, and the tax base. The aggregate-GDP-versus-fiscal-impact distinction is valid, but the closing rhetoric overshoots. [SOURCE: https://www.nap.edu/catalog/23550/the-economic-and-fiscal-consequences-of-immigration] [SOURCE: https://doi.org/10.24149/wp1704]

## Claim Triage

| Claim in testimony | Repo verdict | Why |
|---|---|---|
| Low education is the main mechanism behind net fiscal cost claims | **Green** | Consistent with mainstream literature |
| Recent local shelter and school burdens are real | **Green** | Supported by CBO and locality reporting |
| `12.8M` illegal immigrants in Oct. 2023 | **Yellow** | Preliminary, residual/imputation dependent |
| `59.4%` of illegal-headed households use welfare | **Yellow** | CIS-built status assignment and cost allocation |
| `$42B` in welfare costs | **Yellow** | Rough approximation, not direct measurement |
| `$68.1B` in school costs | **Yellow** | Arithmetically fair as current gross local incidence if child attribution is accepted, but incomplete as fiscal balance |
| `$68,390` lifetime drain per illegal immigrant | **Red** | CIS synthetic estimate, not a neutral or official finding |

## How this repo should use the testimony

Use it for:

- the strongest structured restrictionist framing,
- examples of cost categories and jurisdictional stress,
- citations worth checking independently.

Do not use it for:

- a baseline estimate of the fiscal impact of unauthorized immigration,
- quoting the `$68k` figure as if it were an official or consensus result,
- any claim that ignores the federal/state-local split, public-goods allocation choice, or uncertainty in unauthorized-population denominators.

## Bottom line

The right way to read Camarota is: **not bullshit, not neutral, and not clean enough to anchor the repo's estimate stack**. [INFERENCE]
