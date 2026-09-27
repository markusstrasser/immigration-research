**Verdict:** The CEEY *Informe Movilidad Social en México 2019* (ESRU-EMOVI 2017; men and women aged 25–64) does **not** print the full schooling transition matrix. It points to an online statistical annex. It prints two rows: children of parents with no schooling and children of parents with professional studies, over six schooling levels. Both rows are recovered below and reconcile with the report's prose. On access, CEEY's EMOVI page links the 2017 "BASES DE DATOS" to a Google Drive share link, and I saw no registration form on the page; I did not test the Drive file itself. INEGI MMSI 2016 served curl a JS or bot page, so neither its results nor its microdata URL were verified.

Source: Centro de Estudios Espinosa Yglesias (CEEY), *Informe Movilidad Social en México 2019: Hacia la igualdad regional de oportunidades*, 83 pages. URL: https://ceey.org.mx/wp-content/uploads/2019/05/Informe-Movilidad-Social-en-M%C3%A9xico-2019..pdf (the double dot is in the published file name). Local file `_cache/reads/ceey_informe_movilidad_2019.pdf`, sha256 `b2317381d92a933fc634e69fde214c28e523dbb928b2b1133125781507fb58bb`. Text via `pdftotext -layout` (`ceey_informe_movilidad_2019.txt`, with page tags in `ceey_paged.txt`). Page numbers are PDF pages.

## Quotes

1. PDF p. 15, population: "información de hombres y mujeres con edades entre 25 y 64 años, a través de" [the line continues in the report]. PDF p. 37, chart note: "Nota: La esru-emovi 2017 es representativa de hombres y mujeres entre 25 y 64 años a nivel nacional, para la" [continues]

2. PDF p. 26 (printed p. 25), categories: "Para obtener información sobre los tres temas antes mencionados, en la esru-emovi 2017 se entrevistó a adultos de los hogares sobre su situación actual y de origen, es decir, sobre sus padres y los hogares en los que habitaron con ellos. Para saber si ha habido o no movilidad social entre generaciones, se utilizan las siguientes categorías: • Educación. Son seis las categorías: a) sin estudios, b) primaria incompleta, c) primaria, d) secundaria, e) preparatoria y f) estudios de nivel profesional."

3. PDF p. 28, chart title and note: "Gráfica 2.1 Movilidad educativa entre dos generaciones: población con padres que no asistieron a la escuela frente a población con padres con estudios universitarios (% de personas)". Note: "(1) La clasificación de educación considera, a partir de primaria, grados completos de estudio. Para consultar la matriz de movilidad educativa, véase anexo estadístico en línea en: www.ceey.org.mx. (2) Los resultados pueden variar por el redondeo de cifras. Fuente: Estimaciones propias con base en la esru-emovi 2017."

4. PDF p. 28, prose: "Esto significa que hijos de padres sin estudios o con apenas primaria, han logrado permanecer más tiempo en la escuela; sin embargo, no es suficiente para que esta educación realmente impacte en su futuro. Nueve de cada diez de estas personas alcanzan un nivel mayor al que alcanzaron sus padres, pero, el 52 % de ellos no concluyeron la educación secundaria (Gráfica 2.1)." [Footnote marker 1 points to "Gráfica A3.3 del anexo estadístico en línea"]

5. PDF p. 29, prose: "Solo 5 % de los hijos de padres sin escolaridad logran estudiar una licenciatura, en comparación con 64 % de los hijos de padres con estudios universitarios. Hijos cuyos padres cuentan con esta educación, alcanzan la formación profesional a una tasa doce veces mayor que quienes provienen de padres sin escolaridad."

## Gráfica 2.1 as a two-row table

**[ASSIGNED BY TEXT-LAYER X-POSITION: verify against the figure]** The chart's twelve data labels are in the PDF text layer: 64, 30, 27, 26, 16, 13, 8, 8, 5, 2, 0 and 0 per cent. I assigned each label to a category and a series by its column position under the axis labels "Sin estudios / Primaria incompleta / Primaria / Secundaria / Preparatoria / Profesional". The left bar of each pair is the parents-without-schooling series.

| Child's schooling → | Sin estudios | Primaria incompleta | Primaria | Secundaria | Preparatoria | Profesional | Row sum |
|---|---|---|---|---|---|---|---|
| Parents without schooling | 8% | 16% | 27% | 30% | 13% | 5% | 99% |
| Parents with professional studies | 0% | 0% | 2% | 8% | 26% | 64% | 100% |

Consistency checks against the prose:
- The "5 %" and "64 %" for licenciatura match (quote 5).
- Below secundaria for the no-schooling row is 8 + 16 + 27 = 51%, against the prose's 52%; the report notes rounding.
- The share reaching a higher level than parents is 100 − 8 = 92%, against the prose's "Nueve de cada diez".

**[NOT FOUND in the Informe 2019 PDF]:**
- The four middle origin rows (primaria incompleta, primaria, secundaria, preparatoria).
- Whether "padres" means the father, the mother or the higher of the two.
- The sample size.

The full matrix is in the online "anexo estadístico" (quote 3).

## Access terms (observed 2026-09-27; nothing downloaded, no registration)

- The CEEY EMOVI page is https://ceey.org.mx/contenido/que-hacemos/emovi/. Its ESRU-EMOVI 2017 block links each item to a Google Drive "view?usp=sharing" URL:
  - "BASES DE DATOS": https://drive.google.com/file/d/1hko58nfnlexpw5kiB1K0kqeXlOPAaGyr/view?usp=sharing
  - "ANEXO ESTADÍSTICO": https://drive.google.com/file/d/1hCxa_qUniH0c5pbSLoW1zy5Bl8hXElXZ/view?usp=sharing (this is where the full matrix should be)
  - "CUESTIONARIO": https://drive.google.com/file/d/1hqRpLy2BYWLG84hMbqOt7RNv3cHggE5B/view?usp=sharing
  - "ÍNDICES Y PROGRAMAS DE CÁLCULO": https://drive.google.com/file/d/1hLDOZt_ZUr71PUX4w26uVNoqgf1umRDd/view?usp=sharing
  - "DOCUMENTOS METODOLÓGICOS": https://drive.google.com/file/d/1Wc3TgygPuY2S7m2xbQLrhyISSCvWeB9w/view?usp=sharing

  Labels and URLs were parsed from the page HTML. The page's visible text shows no registration or personal-details form for these links; the only "registrar" string is a CSS comment about a login-page button. I did not open the Drive files, so whether they are public is untested.
- INEGI MMSI 2016: https://www.inegi.org.mx/programas/mmsi/2016/ returned a 2,726-byte page to curl, a JS or bot shell with no content. The guessed microdata URLs `https://www.inegi.org.mx/contenidos/programas/mmsi/2016/microdatos/mmsi2016_bd_{csv,dbf,sav,dta}.zip` each returned HTTP 200 as a 2,263-byte text/html page, not a zip. **[NOT VERIFIED]:** the INEGI MMSI 2016 microdata download URL, and the published MMSI 2016 results tables.

## Corrections to the brief's figures

- No figures were given. The brief expected a published table; only two of its six origin rows are printed in the Informe 2019, and the full matrix is in the online annex, which I did not download.
- The EMOVI 2017 microdata appear to be an open Google Drive link, not a registration form; this is untested.
