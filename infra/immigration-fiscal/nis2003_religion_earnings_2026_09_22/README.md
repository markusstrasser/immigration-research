# NIS-2003 Round 1 — religion, employment and earnings

Descriptive lane over the New Immigrant Survey 2003 cohort, baseline round
(ICPSR 38031 v3). It fills the gap flagged in
`research/immigration-muslim-origins-funding-outcomes-2026-09-21.md` §2, which lists
NIS 2003 as "not reached" for religion together with earnings.

**Population**: 8,573 adults granted US legal permanent residence in 2003, interviewed
June 2003 – June 2004, on average about four months after admission. Not a sample of the
foreign-born population, and not a sample of the US population.

## Reproduce

```sh
cd /Users/alien/Projects/immigration-research
# one-off: stage the datasets this lane reads (about 170 MB) into the git-ignored cache
Z=sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip
L=infra/immigration-fiscal/nis2003_religion_earnings_2026_09_22
for d in 0002 0003 0006 0007 0011 0012 0013 0017 0053 0054; do
  unzip -o -q "$Z" "ICPSR_38031/DS$d/38031-$d-Data.tsv" -d "$L/_cache/"
done

OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/analysis.py
uv run --no-project python3 -m pytest $L/ -q
```

`analysis.py` takes about two minutes, almost all of it the 500-draw bootstrap. It verifies
the source zip hash itself and stops if the cache is missing. No extra wheels are needed
beyond the main checkout's `.venv` (pandas, numpy, pytest).

## Datasets read

| Dataset | Section | What it supplies |
|---|---|---|
| DS0002 | CIS preload | design weight, sampling stratum, class of admission, country of birth, adjustee flag |
| DS0003 | A Demographics | sex, year born, years of school, interview year |
| DS0006 | C Employment | current employment status, usual hours, weeks per year, pay basis, salary unit |
| DS0007 | C (cleaned) | salary and hourly wage in US current prices, PPP adjusted |
| DS0011 | G Income | wage and salary receipt, financial-respondent flag |
| DS0012 | G (cleaned) | wage and salary income over the last twelve months, PPP adjusted |
| DS0013 | H Assets | housing tenure, used only for the home-ownership anchor |
| DS0017 | J Social | religion, English-speaking ability |
| DS0053, DS0054 | G, spouse path | the sampled immigrant's wage report when the spouse answered Section G |

Every code is taken from the questionnaires, public picklists and P.I. codebooks inside the
zip, never from memory; `derived/audit.json` prints each code list with its labels and names
the PDF it came from, plus the codebook label of every recoded variable.

## Method

**Religion** is `J30_1MO`, the first religious tradition mentioned (RELPICK1). Catholic,
Orthodox Christian and Protestant are pooled into a Christian reference group for model A;
model B splits them with Catholic as the reference. Refusals, don't-knows and non-response
(417 cases) are excluded.

**Employment** is `C1 == 1` ("working now"), asked of the sampled immigrant directly, so it
carries no financial-respondent selection.

**Earnings** are built two ways, because the survey measures two different things.

- `earn_annual` annualises the pay rate on the job held at interview: salary times the unit
  factor from `C48A2_1` for salaried, piecework and other pay, or hourly wage times usual
  hours times weeks per year for hourly pay. `earn_ft` restricts it to 30 or more usual hours.
- `wage_12m` is wage and salary income actually received over the last twelve months. Sections
  G, H and I go to whichever spouse is most knowledgeable about household finances, so when
  the spouse answered, the sampled immigrant's amount is read from the spouse questionnaire
  (`G16PPP`) and linked on the four-digit case id. That recovers 840 reports; the ceiling is
  set by the G13 skip, not by the file.

**Estimation** is weighted by the NIS design weight. Log-earnings and employment gaps come
from WLS and a linear probability model on religion dummies plus, in the adjusted
specifications, age band interacted with sex, years of school in six bands, English-speaking
ability, class of admission, adjustee status and either region of birth (`adj`) or the full
28-category country-of-birth scheme (`adj_origin`).

**Standard errors** are a 500-draw respondent bootstrap, seeded, resampling within the 32
stratum-by-replicate design cells. Those cells are recovered from the distinct design-weight
values because the public file carries no PSU identifier, so no Taylor-linearised design
variance is available. This is stated wherever an SE is reported.

## Outputs

- `derived/anchors.csv` — every published figure tested, with the reproduced value.
- `derived/religion_cells.csv` — weighted and unweighted cell sizes per religion, per outcome.
- `derived/earnings_gaps.csv` — every estimate, SE, cell size and a `reported` flag that is
  false where a cell falls below 50 observations.
- `derived/audit.json` — hashes, gates, code lists with sources, verified variable labels,
  earnings definitions, and the five results that looked wrong on first inspection with the
  diagnostics that resolved each one.

`RESULT.md` holds the tables and the limits.
