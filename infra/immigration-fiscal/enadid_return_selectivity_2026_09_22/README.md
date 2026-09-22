# ENADID return-migrant selectivity (2018 and 2023)

Mexico-side check on two assumptions the fiscal and lineage work currently carries without
measurement: that return migration from the United States is negatively selected on
education, and that the rising education of recent Mexico-born arrivals in US surveys is
not produced by return selection.

## Reproduce

From the repository root:

```sh
uv run --no-project python3 infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/enadid_selectivity.py
uv run --no-project python3 -m pytest infra/immigration-fiscal/enadid_return_selectivity_2026_09_22/ -q
```

Inputs are the two frozen open-data bundles already acquired and validated in
[`enadid_2026_09_20/`](../enadid_2026_09_20/). Nothing is downloaded. Both bundle SHA256
values are checked against that lane's `sources.json` before a byte is parsed, and the four
table members are checked against its `derived/validation.json` hashes. No file outside this
lane directory is written.

## The two objects, and why they are not subtracted

`TSDem` is the resident person table. It locates a **US-to-Mexico endpoint transition**:
someone living in a sampled Mexican household today who reported living in the United
States five years earlier. It includes people who left the US after a long stay and misses
people who died, who moved again, or who are back in the US at survey time.

`TMigrante` is the household-reported **departure** table: people a sampled household says
left to live abroad during the five-year window, flagged by whether they have returned. Its
returnees left *and* came back inside the same window, so they are short-duration migrants
by construction, and its coverage misses households that left in their entirety.

These are different populations over different clocks. A departure count minus a returnee
count is not net migration, and this lane produces no net quantity. A test enforces that.

## Field mapping, by wave

Question numbers drift between the waves; each column below was read from that wave's own
DDI dictionary inside the bundle, and every category label from that wave's own catalog
files. Nothing is carried across by assumption.

| Construct | 2018 | 2023 | Dictionary label (quoted) |
|---|---|---|---|
| Birthplace | `p3_7` | `p3_10` | "En qué estado de la República Mexicana o país nació (NOMBRE)?" |
| Residence five years before | `p3_19` | `p3_24` | 2018: "Hace cinco años, en agosto de 2013, ¿en qué estado de la República Mexicana o país vivía (NOMBRE)?"; 2023: same wording, "en agosto de 2018" |
| Schooling level | `niv` | `niv` | "¿Cuál es el último año o grado que aprobó (NOMBRE) en la escuela? (Nivel)" |
| Schooling grade | `gra` | `gra` | same question, "(Grado)" |
| Grouped schooling | absent | `niv_esc` | "Nivel de escolaridad (agrupada)" |
| Years approved | `esco_acum` | `esco_acum` | "Escolaridad acumulada (años aprobados)" / "(grados aprobados)" |
| Age | `edad` | `edad` | "¿Cuántos años cumplidos tiene (NOMBRE)?" |
| Sex | `sexo` | `sexo` | "(NOMBRE) es hombre o mujer" |
| Resident weight | `fac_viv` | `fac_viv` | "Factor de expansión a nivel vivienda" |
| Migrant weight | `fac_viv` | `fac_hog` | 2023: "Factor de expansión a nivel hogar" |
| Departure destination | `p4_11` | `p4_11` | "¿A qué país se fue (NOMBRE) la última vez?" |
| Return status | `cond_resid` | `cond_resid` | "Condición de retorno a México" |
| Age at departure | `p4_8`, `p4_8_ag2` | same | "La última vez que (NOMBRE) se fue, ¿cuántos años cumplidos tenía?" |
| Household re-entry link | `p4_20_1`, `p4_20_2` | same | "¿(NOMBRE) actualmente forma parte de este hogar?" + "Número de renglón de la lista de personas" |
| Design | `est_dis`, `upm_dis` | same | "Estrato de diseño muestral", "Unidad Primaria de Muestreo" |

Category codes come from the bundles' `catalogos/` members and are identical across waves
where used here: birthplace and prior residence both read `1` "Aquí, en este estado",
`2` "En otro estado", `3` "En Estados Unidos de América", `4` "En otro país";
`p4_11` reads `1` "Estados Unidos de América"; `cond_resid` reads `1` "Retornó",
`2` "No retornó", `9` not specified; `sexo` reads `1` "Hombre", `2` "Mujer".

**Dictionary discrepancy worth recording.** The 2018 data dictionary states the range of
`upm_dis` as `00001-10376`; the file actually carries values up to `15226` across 15,216
distinct PSUs. The documented range is wrong. The script does not rely on it: it checks
empirically that no `upm_dis` value spans two strata, which holds in both waves, so the
identifier is a national PSU key rather than a within-stratum sequence.

## Schooling bands

The four bands are built from INEGI's own grouped variable, not from a hand-written rule.
The 2023 file ships both `niv`/`gra` and `niv_esc`, so the 63-cell `niv × gra → niv_esc`
mapping is read off the 2023 microdata, checked to be a function, and then applied to 2018,
which ships no `niv_esc`. A gate re-derives the 2023 bands through the crosswalk and fails
unless they reproduce `niv_esc` exactly.

| Band | `niv_esc` codes | Catalog labels |
|---|---|---|
| `lt_lower_secondary` | 1, 2, 3, 4 | Sin escolaridad, Primaria incompleta, Primaria completa, Secundaria incompleta |
| `lower_secondary` | 5 | Secundaria completa |
| `upper_secondary` | 6 | Medio superior (includes normal básica and carrera técnica con secundaria terminada) |
| `tertiary` | 7 | Superior (includes carrera técnica con bachillerato terminado, licenciatura, especialidad, maestría, doctorado) |

`niv_esc` 9 ("No especificado") is excluded from band denominators. It is 12 of 218,250
cases in the 2018 universe and 2 of 208,877 in 2023.

## Standard errors

Every proportion and mean is a domain ratio, estimated with Taylor linearization over
strata `est_dis` and PSUs `upm_dis`, with-replacement. Domain indicators are carried on the
full wave frame so that every PSU contributes to the variance, which is the correct form
for a small domain. Differences between returnees and non-migrants are linearized jointly,
so the reported difference SE keeps the covariance between the two domains rather than
adding two variances.

2023 has 56 single-PSU strata (2018 has none). These are handled by centring the singleton
contribution on the sample-wide PSU mean, the conservative option. `audit.json` records the
alternative treatment as well; the two agree to five decimal places on the validated cell.

**Validation against a bootstrap.** The tertiary share among returnees was recomputed with
1,000 bootstrap replicates resampling PSUs with replacement inside strata. A bootstrap
resamples a singleton stratum to itself, so it is the analogue of the zero-contribution
treatment, and it is compared against that variant.

| Wave | Estimate | Taylor (conservative) | Taylor (zero-contribution) | Bootstrap, 1,000 reps | Gap |
|---|---|---|---|---|---|
| 2018 | 0.11178 | 0.014606 | 0.014606 | 0.014054 | 3.8% |
| 2023 | 0.15479 | 0.018368 | 0.018367 | 0.017616 | 4.1% |

A gate fails the run if the gap exceeds 6%.

## Gates

The script raises and stops on any of: a bundle hash that does not match the frozen
manifest; a table member hash that does not match the acquisition lane's validation record;
a row or column count that does not reproduce (385,978 × 93 and 2,611 × 55 for 2018;
359,018 × 103 and 3,660 × 52 for 2023); a non-unique or blank record key; a weight that is
not strictly positive; a `upm_dis` value spanning two strata; a `niv × gra` cell mapping to
more than one `niv_esc`; a derived 2023 band that disagrees with `niv_esc`; a published
anchor missed by more than 0.06 percentage points; a bootstrap-versus-Taylor gap above 6%;
an empty domain denominator.

## Anchors

The run reproduces four published ENADID figures per wave before reporting anything else.
Both come from the acquired `resultados_enadid23.pdf`. See `derived/anchor.csv`.

## Outputs

| File | Contents |
|---|---|
| `derived/anchor.csv` | Published figure, reproduction, SE and gap, both waves |
| `derived/return_migrants_by_schooling.csv` | TSDem: schooling bands and mean years by wave, group, sex, age band, with SEs, plus the returnee-minus-non-migrant differences. 18 slices, 540 rows |
| `derived/departures_by_schooling.csv` | TMigrante: weighted counts, sex, age at departure by return status; plus schooling recovered through the household link, returnees only |
| `derived/audit.json` | Input hashes, gate results, wave-by-wave variable map, schooling crosswalk, design validation |

## Known limits

Carried in full in `RESULT.md`. The short form: `TMigrante` has no schooling variable in
either wave, so the departure cohort's education is unmeasured except for returnees who
rejoined the household; household-reported departures miss whole-household moves; the two
returnee definitions describe different populations; the windows are five-year, not annual;
and schooling is measured at the survey, not at departure.
