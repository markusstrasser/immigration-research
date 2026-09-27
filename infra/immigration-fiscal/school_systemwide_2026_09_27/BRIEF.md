# Lane brief: can system-wide school degradation hide from the measures the peer-effect literature uses?

Date 2026-09-27, 23:58 JST. Parent session immigration-research-1c. The operator doubts the null-to-small
classroom effects and suspects the measures:

> schools have incentives ... I think they will just lower requirements but give same grades. Colleges and
> schools might also use grading curves that relativize ... not absolute competence ... What about curriculum
> degradation? I mean think like a shifty politician or admin.

## The identification point to test first

The main designs compare natives across schools, classrooms or siblings within a state and year, often with
test scores standardized within grade and year. That includes Figlio–Giuliano–Özek–Sapienza (sibling FE),
Diette–Oyelere and Hunt, in ladder 81. Such designs identify local exposure differences. They cannot see a shift
common to every school in a state: lower cut scores, a thinner curriculum, laxer grading norms or exit exams
dropped statewide. Only comparisons between states (or systems) over time on absolute, low-stakes measures can
see that. Borgschulte et al. 2025 (ladder 91) is city-level and sees part of it.

## What exists (read first)

- `decisions/2026-09-20-school-quality-unpriced.md` and `research/immigration-school-capacity-harms-2026-09-20.md`.
- Ladder 81 (superseded as a zero) and 91 (`research/immigration-confidence-ladder.md`).
- `infra/immigration-fiscal/school_dilution_2026_09_24/RESULT.md`: resources only; peer effects are unpriced. It
  gives a CFR/JM mapping from learning to earnings.
- The ECLS-K checks (INDEX, "Mixed classroom associations").
- Local NCES CCD 2023–24 files, with English-learner counts by district:
  `sources/immigration-fiscal/data/external/nces_ccd/`, `stage2/nces/`.

## Tests

1. **The design table.** For each study the repo cites, and the main European ones (Brunello–Rocco, Ohinata–van
   Ours, Geay–McNally–Telhaj, Ballatore et al., Tonello, Frattini–Meschi, Jensen–Rasmussen), record:
   - the outcome measure: grades, standardized-within-year scores or absolute scale;
   - the comparison: within school, within state or between systems.
   Then say which designs could detect a statewide shift.
2. **NAEP, absolute and low-stakes.** Take state NAEP grades 4 and 8, math and reading, 2003–2024, for white
   students and for non-English-learner students.
   - Regress the within-state change on the change in the English-learner, Hispanic or immigrant share of
     enrollment, with state and year fixed effects and SEs clustered by state.
   - Report per 10-point change, in NAEP points and SD.
   - Test pre-trends. Put the 2020–2024 pandemic years in a separate specification.
3. **Lowered standards.** Use NCES *Mapping State Proficiency Standards onto the NAEP Scales* (2005–2019): the
   NAEP-equivalent cut scores by state and year. Do states whose English-learner or Hispanic share grew more
   lower their cut scores more? This is the operator's "lower requirements, same grades" mechanism, measured
   on an absolute scale.
4. **Exclusion.** Do NAEP exclusion rates for English learners (by state and year) move with the English-learner
   share? Quote the ESSA exemption for recently arrived English learners from primary text.
5. **Credential inflation.** Does the ACGR graduation rate diverge from NAEP grade 8 four years earlier more where
   the share grew? Check exit exams dropped, with their state and year, against the share.
6. **Optional, if downloadable without an account.** SEDA's NAEP-linked district scores for white students against
   the district's Hispanic or English-learner share, within districts, 2009–2019.
7. **Verdict.**
   - Does a system-wide effect show on absolute measures?
   - Do cut scores, exclusions or credentials move with the share?
   - If anything is non-null, price it in SD and in lifetime earnings with the dilution lane's mapping.
   - Name what would falsify the operator's hypothesis, and whether the data do.

## Rules

- Work only in `infra/immigration-fiscal/school_systemwide_2026_09_27/`. Do not edit other lanes, `research/`,
  `decisions/`, INDEX, FAQ, ladder or `CLAUDE.md`.
- The checkout is shared: no commits, and no `git add`, `stash`, `checkout` or `reset`.
- Raw downloads go in an ignored `_cache/`, with a `.gitignore` in the lane. The NAEP Data Service API and NCES
  files are public. Firecrawl is out of credits: use Exa or direct HTTP with a generic User-Agent, and no
  personal identifier in any request.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root. Write
  CSVs with `lineterminator="\n"`. Two runs must be byte-identical.
- Tag every number: [SOURCE], [DATA], [CALCULATION], [INFERENCE] or [TRAINING-DATA]. Steel-man both the
  operator's hypothesis and the null before testing.
- Stub `RESULT.md` with `**Verdict:** pending` first and append as you go.
- Final message: the RESULT path and at most ten lines.
