# Reproduction of the @tomaspueyo "immigration & crime in Europe" thread (2026-09-15)

Thread text and the 16 charts: `source_thread/`. Four lanes, each with its own `RESULT.md` opening with a verdict, raw pulls, request bodies, scripts and tidy CSVs:

| Lane | Charts | Verdict |
|---|---|---|
| `denmark/` | violent crime by origin (raw and age-sex-adjusted), 12 crime types by origin, ft.dk cohort chart | 3 of 4 reproduce exactly; the adjusted chart cannot be built from open tables; ft.dk chart is cumulative conviction prevalence, not convictions per arrest |
| `germany/` | PKS 2025 ranking, GDP scatter with Muslim premium | Ranking reproduces exactly; immigration-law offences and non-resident suspects inflate the top; +48% premium reproduces on his sample only |
| `nordic/` | Finland sexual offences, Sweden Brå B6, Norway charges | Sweden and Norway exact; Norway chart is men 15–24 in Oslo over 4 years; Finland not reproducible from StatFin |
| `south_uk/` | Spain population and prisons, Italy ISTAT, London and England & Wales FOI, Eurostat index | Spain and Eurostat reproduce; Italy partly; London arithmetic reproduces but denominators are APS nationality, not census |

Files over 2 MB are gitignored (listed in `.gitignore`) and re-fetchable with each lane's pull script. Synthesis: `research/immigration-mexican-origin-generation-incarceration-2026-09-16.md` §10.
