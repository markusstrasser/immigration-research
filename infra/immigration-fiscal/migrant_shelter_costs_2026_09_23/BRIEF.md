# Brief: migrant shelter and emergency response costs — budgets, our finance files, and who was served

Operator, 2026-09-23 20:58, after the California Medi-Cal finding: "Find it in other places ... if
we have the data ... sherlock". The largest local outlays tied to recent arrivals in 2022–2025 were
shelter and emergency response. They are reported in city and state budgets, not in the national
programs our account itemizes.

## Tasks

1. **Budgets.** For New York City, New York State, Massachusetts (Emergency Assistance family
   shelter), Chicago/Illinois, Denver/Colorado and Washington DC, give spending on migrants and
   asylum seekers by fiscal year from FY2023 to FY2026: shelter, food, health, education and legal
   services. Split local, state and federal (FEMA Shelter and Services Program, EFSP). Sources are
   the NYC Office of Management and Budget, the NYC Comptroller, NYS DOB, MA EOHLC and the MA
   Inspector General or State Auditor, Chicago's OBM, Illinois DHS, Denver's OFM, DC's CFO, and
   FEMA award data. Include each city's peak shelter census of migrants.
2. **Who.** Countries of origin of the sheltered or served populations where the city publishes them
   (NYC and Chicago did at times), and whether Mexican nationals are a material share.
3. **Sherlock in our data.** Test whether these outlays show up in the Census Annual Survey of
   State and Local Government Finances individual-unit files we hold. The 2021–2023 files are at
   `../local_spending_composition_2026_09_18/_cache/indunit_<year>.zip`; the 2024 file is at
   `../detention_reconciliation_2026_09_20/_cache/census_2024_units.zip` (see that lane's
   `LOCAL_FINDINGS.md` for layout). For NYC, Chicago, Denver and the Massachusetts state government,
   compare 2021/2022 with 2023/2024 on public welfare, housing and community development, health,
   and "other/unallocable". Contrast them with peer governments of similar size. Report which
   functions carry the jump and whether its size matches the budget figures. Say whether
   annual-survey sampling limits the comparison (non-census years are samples; large cities are
   certainty units).
4. **Account implication.** The complete account spreads state and local spending over BEA
   categories through national keys (population, CPS public assistance and others; see
   `../full_account_spending_2026_09_20/` and `../dataset_integrity_2026_09_23/spending.md`). Find
   which BEA category and key these outlays most likely fall under. Estimate how much of them the
   account charges to the Mexican-origin union through that key, against the union's share of the
   people actually served. State whether the account over- or under-charges the union here, and
   by roughly how much [CALCULATION with stated assumptions].

## Rules

- Primary documents for every number.
- Fetch with `curl` through `subprocess` or plain curl with a browser User-Agent. Python urllib
  fails TLS here. Use the Wayback `id_` route for blocked sites.
- Keep PDFs in `_cache/`; quote with page numbers.
- Never take a number from an LLM extraction or a news summary without the primary document; tag
  news-only figures `[SECONDARY]`.
- Tag every figure.
- Run from the repository root with `OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3`.
- Stay within about 12 research turns for task 1–2. Task 3 is a data task: give it a script and
  `derived/` tables, rerun once, and confirm the output is byte-identical.

## Output

`RESULT.md` in this directory, opening with `**Verdict:**`, with:
- the budget table;
- origin of those served;
- the Census-file test;
- the account implication;
- gaps.

Do not commit. Do not edit outside this directory. Reply to the lead with the path and at most 10
lines.
