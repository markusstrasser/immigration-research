**Verdict:** None of the 29 new papers moves a number in the main case. 26 check one of our results, assumptions or methods, 3 are context, and none matches the case's population, horizon and outcome. They do supply about a dozen reusable methods, one premise to correct (the crash lane's "licensing does not change crash frequency"), and three arithmetic or table defects in the papers themselves.

# Full reads of the 2026-10-20 literature scout's new papers

Frame: the scout (`notes/immigration-literature-scout-2026-10-20.md`) found 37 rows, 36 papers, that the repo had
not read. For each one, a Sol worker (GPT-6.1 Sol, five lanes) read the whole parsed text, including notes, appendices
and recovered supplements. Each read records the estimand, data, identification, headline results with
uncertainty, footnotes, levers, relevance and misuse risk. The worker checked each against the INDEX, FAQ, ladder and
lane RESULTs it names. One file per paper sits beside this README. The comparisons were made against main case v8
(oct15), which was live when the reads ran; v9 was adopted the same day, and each file carries a dated notice.
[DATA: per-paper files; `_index.tsv`]

`_index.tsv` columns: DOI, parse quality (FULL / PARTIAL), relevance (MOVES / CHECKS / CONTEXT), characters read,
footnote count, datasets the paper uses that the repo lacks, one-line reason.

## Coverage

- **Read: 29.** 6 FULL; 23 PARTIAL. PARTIAL means the whole text was read, but some equations or tables came through
  garbled, or a supplement was missing; each file lists what was recovered from the layout and what was not.
- **Unavailable: 7** (no legitimately public full text; routes tried are in the hunt manifest):
  - Santos et al. 2025, JAMA IM 10.1001/jamainternmed.2025.0604;
  - Zhao 2025, JPAM 10.1002/pam.70053 (its replication package is public, so it is being reproduced instead:
    `infra/immigration-fiscal/zhao_licenses_crashes_2026_10_20/`);
  - Watts & Evans 2022;
  - Orrenius & Zavodny 2022;
  - Kesler 2025;
  - Ramos & Alaniz 2022;
  - LeRoy 2025.
- **Parses:** Marker 2 on Modal with GPT-6 Luna (OpenRouter) as the cleanup model, after the Gemini key hit its
  spend cap; each parse logged 0 LLM errors. Two figures were checked by hand against the paper text:
  - Santos (JAMA 2025): emergency Medicaid is 0.4% (SD 0.5%) of reporting states' Medicaid spending.
  - Ommerborn (2022): the payer cells (+13.7 Medicare, +10.2 Medicaid, +39.3 private, −4.9 uncompensated) add to
    $58.3bn, and 89.0% of that is the undocumented share. Both match. [DATA: corpus parses]

## What they check, ranked by use to the repo

1. **Selective ethnic attrition in later generations** (Antman, Duncan & Trejo 2023, JEP). Self-identified
   G3+ Hispanic attainment is biased downward by ethnic attrition. This agrees with the case, which already counts
   descendants who stopped reporting (arm b, C3), and it supplies no new size. (FAQ 19; ladder 280.)
2. **Health financing: the payer is not the cost.** Three JAMA-family papers:
   - Ommerborn 2022: a 2017 health-insurance surplus of +$58.3bn for all immigrants;
   - Haro-Ramos 2026: after the 2018 public-charge announcement, LA DHS visits shifted from Medicaid to self-pay;
   - Martinez-Cardoso 2026: Illinois's state coverage is followed by lower hospital bad debt, with randomization
     p > .05.
   All three agree with the lower-use mechanism in the pooled MEPS lane and the use-keyed uncompensated care (ladder
   192, 206). None prices total government health spending for the lineage. Lever: one encounter must never be
   charged both as Medicaid and as uncompensated care. Santos 2025's 0.4% is a state-mean share of one program, so it
   is not a national balance.
3. **Crime measurement.**
   - Riaz 2026 (BJPolS) shows how an aggregate null can hide a large group-rate gap: separate the inflow effect θ
     from the rate gap r, and report what the confidence interval excludes on the group's own scale. This applies to
     the causal-execution lane's Chalfin replay.
   - Orrick et al. 2020 (Texas homicide custody) has numerator and denominator inconsistencies, so its rate ratios
     cannot be reused.
   - Ramos et al. 2025 finds Mexican county coefficients imprecise.
   - Churchill et al. 2021 finds that E-Verify lowers Hispanic property crime.
   - Spelman 2021 (age-period-cohort decomposition) identifies no immigrant offending.
   None changes FAQ 12.
4. **Schools.**
   - Novicoff, Reardon & Johnson 2025: kindergarten English learners followed as a fixed cohort narrow their gaps,
     while snapshots of current English learners widen. Lever: define membership as "ever English learner" before
     reading progress (ladder 248, 252).
   - Rauscher 2020: frozen Kansas grants plus enrollment growth lower scores locally. This supports harm when
     funding lags and leaves the full-cost long-run school charge as it is.
   - Bifulco & Souders 2024: actual spending on Hispanic pupils is higher and needs-adjusted spending lower. Their
     parity arithmetic is wrong: 0.868 needs +15.2%, not 13.2%; 0.750 needs +33.3%, not "roughly 25%".
   - Kirksey 2024 (attendance after raids) and Antman & Cortes 2023 (desegregation) are mechanisms outside the
     resident-stock account.
5. **Fiscal frameworks abroad.** Christl et al. 2022 (EU), Boffi et al. 2026 (EU-SILC), Fiaschi & Tealdi 2026
   (Italy), Baechli & Glitz 2024 (Switzerland) and Allen et al. 2025 (review). Their sign turns on age and the child
   attribution rule. The case already offers both: common-age comparisons and the parents' allocation. Fiaschi &
   Tealdi's goods-price gain may be another face of the surplus already in the production term, so check for
   overlap before adding it.
6. **Labour and welfare models.**
   - Chassamboulli & Liu 2024: a search model's job-creation channel, whose fiscal sign depends on the spending
     assumption.
   - Saha & Rubini 2024: welfare from variety, calibrated to shock counts that are not observed low-skill
     deportations.
   - Borjas & Edo 2026: a wage elasticity, which must not be inverted into the nest's ε.
   - Ma et al. 2025: population projections; aggregate GDP rises while GDP per capita lags.
   - Borjas & Breznau 2024: a researcher's ideology predicts the effect size they submit.
   None is a matched update.
7. **Identity and attainment.**
   - Hadah 2024: children's Hispanic reporting tracks local attitudes.
   - Hadah 2025: a surname or family-configuration gap.
   - Kim et al. 2026: a mid-life income decomposition.
   - Thiede et al. 2021: child poverty by generation.
   All are measurement checks on the generation and identity lanes. One test is feasible on held data: rebuild Hadah
   2025's HW/WH families in the ASEC for 1994–2019.

## The premise to correct

The crash lane (`road_crash_externality_2026_09_28/RESULT.md`, licensing paragraph) leaves licensing out of the
involvement factor because Lueders, Hainmueller & Lawrence (2017) found that California's AB60 licences changed
neither crashes nor fatal crashes. Zhao 2025's abstract reports the opposite for fatal crashes, about +5% across the
licensing states. The case charges the group's crash involvement as measured in FARS, and the licences in force are
already inside that measurement. So no number is expected to move, but the premise sentence is contested. The
reproduction lane reports the size and drafts the dated correction. [SOURCE: Zhao abstract; DATA: crash lane RESULT]
[INFERENCE]

## Datasets the papers use that the repo lacks

Each appears once, so none is a recurring gap. Grouped by domain (full list per paper in `_index.tsv`):

- **Health:** RAND hospital panel 2017–23; LA DHS encounter and billing panel; NHIS–MEPS linkage; FY2022 state
  emergency-Medicaid worksheet.
- **Crime:** TDCJ March 2018 individual extract; Texas UCR county four-wave panel; NIBRS/UCR 2004–15 balanced
  panels; German Refugee Registry 2014–16; Riaz Dataverse FJFWEI.
- **Schools:** CDE restricted longitudinal panel (CELDT); KSDE scores; NERD$ 2018–19; CRDC 2017; SEDA exact
  releases; two anonymous districts' student-week attendance.
- **Labour and identity:** HS&B 1980 linked to 1992/2021; NLSY79 raw panel; Project Implicit skin-tone IAT; 1940
  full-count exposure (the repo has IPUMS, but not this extract).
- **Abroad:** EU-SILC 2007–18, EUROMOD, Italian RCFL, INSEE census and LFS, Swiss STATPOP/ZEMIS, UN Migrant Stock.

None would change the case's 2024 national account. The restricted ones (CDE, TDCJ, LA DHS) would serve only as
checks on a lane.

## Reusable methods, gathered

- Pair a program share with dollars per resident, and keep the weighting rule straight: Σ/Σ against the mean of
  ratios.
- Use fixed cohort membership (ever treated, ever English learner) before reading progress.
- Use Gelbach decomposition, which does not depend on the order covariates enter, rather than coefficient
  attenuation, and show both the absolute residual and both denominators.
- Separate θ from r before reading a null, and report what the interval excludes.
- Keep payer shifts distinct from resource cost.
- Keep tax-base responses distinct from discretionary tax policy, and gross distribution distinct from net.
- Report labour-price effects separately from variety and entry effects.
- Separate age, period and cohort; birth cohort ≠ arrival cohort ≠ generation.

These attach to the lanes named in each file; none has been run.
