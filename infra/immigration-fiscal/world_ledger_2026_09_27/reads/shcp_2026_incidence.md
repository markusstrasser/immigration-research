# SHCP (2026), Distribución del pago de impuestos y recepción del gasto público por deciles de hogares y personas. Resultados para el año 2024

Used for: the consumption taxes (IVA, IEPS and the fuel excise) the group would pay in Mexico, the central
Mexican-tax scenario (mexico.py `SHCP_IVA`, `SHCP_IEPS`, `SHCP_IVA_SHARE`, `SHCP_FUEL_SHARE`, `fuel_ieps_by_decile`,
`household_deciles`).

Source: Secretaría de Hacienda y Crédito Público, report to Congress under article 26 of the Ley de Ingresos de la
Federación 2026, https://www.finanzaspublicas.hacienda.gob.mx/work/models/Finanzas_Publicas/docs/congreso/infoanual/2026/ig_2026.pdf
(fetched 2026-09-28 by direct HTTP with a generic User-Agent; 153 pages, 3,132,077 bytes, sha256
2769a9ae97cd2316e85e37527b2a55e86cdc13b37e00cffd91af47a2efea93e4; text in `_cache/reads/shcp_ig_2026.txt`, page 30
rendered to `_cache/reads/shcp_p30-030.png`). The 2024 edition (results for 2022) is `_cache/reads/shcp_ig_2024.pdf`,
kept for reference only.

## Quotes

1. Survey and year (p. 3): "la información más reciente corresponde a la contenida en la Encuesta Nacional de
   Ingresos y Gastos de los Hogares (ENIGH) 2024, publicada por el Instituto Nacional de Estadística y Geografía
   (INEGI) en julio de 2025. El análisis del presente documento se enfoca en el efecto distributivo de las
   políticas tributarias y de gasto público implementadas en 2024."

2. Deciles (p. 4, fn. 2): "Los deciles de hogares o de población son datos agrupados en subconjuntos de igual
   tamaño, 10.0% de los hogares o de la población total cada uno, ordenados ascendentemente en función del
   ingreso". The ordering (p. 9): "El indicador de bienestar utilizado para ordenar los hogares en deciles es el
   ingreso corriente monetario per cápita, es decir, no se incorporan los ingresos no monetarios, ni aquellos que
   representen un cambio en la composición de la riqueza del hogar. Asimismo, para realizar los cálculos de
   incidencia se utiliza el ingreso autónomo del hogar."

3. The income in the incidence ratios (p. 4, fn. 1): "El ingreso autónomo es el ingreso antes del pago de
   impuestos, aportaciones de seguridad social y transferencias gubernamentales." Table 2.2's note (p. 12): "El
   ingreso bruto es el ingreso antes del pago de impuestos, aportaciones de seguridad social y transferencias
   gubernamentales. No se incluyen los ingresos por transferencias ni percepciones financieras." Income and
   spending are both adjusted to the national accounts (pp. 11, 21).

4. Informal purchases pay no IVA (p. 21): "se establece el supuesto de que el gasto realizado en localidades de
   menos de 2,500 habitantes, en mercados y tianguis, y el efectuado en "el comercio ambulante" no paga
   impuestos". And (p. 24): "El cálculo de la distribución de la carga fiscal se realiza excluyendo el gasto
   etiquetado como informal. Para los primeros seis deciles la incidencia respecto al ingreso es mayor que
   respecto al gasto. Ello se explica porque para estos grupos de hogares el ingreso monetario es menor a su
   gasto."

5. **IVA, Tabla 2.8** (p. 25), "Contribución porcentual a la recaudación del IVA e incidencia del impuesto,
   Escenario con ajuste por formalidad, Deciles de hogares ordenados por ingreso per cápita", column "Incidencia,
   % del ingreso, Total", deciles I to X: **6.2, 6.9, 7.2, 7.3, 7.7, 7.9, 8.2, 8.5, 8.9, 8.0**; "Total o
   promedio" 8.0. (Tasa general 5.8 ... 7.8, exentos 0.4 ... 0.3; % del gasto, total, 3.8 ... 10.4.) The same
   table's "Contribución a la recaudación %, Total", deciles I to X: **2.2, 4.0, 5.0, 6.2, 7.5, 8.8, 10.2, 12.7,
   15.8, 27.7**; total 100.0.

6. **IEPS Otros, Gráfica 2.10** (p. 30), "Incidencia del IEPS Otros, Deciles de hogares ordenados por ingreso
   per cápita", the data labels of the series "IEPS / Ingreso", deciles I to X: **1.2, 1.3, 1.4, 1.5, 1.4, 1.4,
   1.4, 1.4, 1.4, 1.0** (read from the rendered page; "IEPS / Gasto" is 0.7, 1.0, 1.1, 1.4, 1.3, 1.4, 1.4, 1.4,
   1.5, 1.3). Text (p. 28): "La proporción del ingreso y del gasto de los hogares que se destina a pagar este
   impuesto es reducida en todos los deciles, ubicándose en un nivel máximo de 1.5%." Coverage (p. 27): "El IEPS
   Otros incluye tabacos labrados, bebidas alcohólicas, cervezas, bebidas energetizantes, bebidas saborizadas,
   alimentos no básicos con alta densidad calórica, redes públicas de telecomunicaciones y combustibles fósiles".

7. ISAN, left out here (p. 31): "El ISAN, por su estructura y base gravable, es un impuesto que se concentra en
   la población de mayores ingresos. En 2024 los vehículos con un valor de hasta 328,965.21 pesos estaban exentos
   del impuesto." Decile X pays 63.2% of it (Gráfica 2.11).

8. Method (p. 9): "la metodología consiste en distribuir entre los diferentes deciles de ingreso el pago de
   impuestos y aplicar a estas distribuciones la recaudación efectivamente observada", with "que la incidencia
   del impuesto al consumo recae completamente sobre los consumidores".

9. **The fuel excise is outside the incidence** (p. 8): "se calcula la incidencia del ISR, el IVA, el IEPS
   diferente a gasolinas y diésel, y el Impuesto sobre Automóviles Nuevos (ISAN)". Tabla 2.1 (p. 8), "Ingresos
   Tributarios del Gobierno Federal, Millones de pesos", 2024: IVA **1,407,983**; IEPS **628,364**; Importación
   **137,822**; source "Cuenta de la Hacienda Pública Federal de 2022, 2023 y 2024". The 2022 IEPS was 117,533.

10. **SHCP's own fuel proxy** (p. 28): "IEPS a combustibles fósiles: dado que la mayor parte de la recaudación por
    este concepto se concentra en gasolinas y diésel, se utiliza como aproximación la información que reporta la
    ENIGH del gasto en estos bienes." **Tabla 2.9** (p. 29), "Contribución porcentual a la recaudación del IEPS
    Otros por impuesto", column "Combustibles fósiles", deciles I to X: **2.5, 4.1, 5.0, 6.1, 7.8, 9.2, 10.9,
    13.6, 16.7, 24.1**; total 100.0. "Fuente: Cálculos con base en la ENIGH 2024."

## SHCP (2025), Información de Finanzas Públicas y Deuda Pública, enero–diciembre de 2024 (30 January 2025)

Source: https://www.finanzaspublicas.hacienda.gob.mx/work/models/Finanzas_Publicas/docs/congreso/fp/2024/FP_202412.pdf
(fetched 2026-09-28 by direct HTTP with a generic User-Agent; 2,274,280 bytes, sha256
d3ff3307f164f5f98c5b46fac82974941755d9e1063e0dd2270b971c5d8523c5; text in `_cache/reads/shcp_fp_202412.txt`).

11. **Table II.3** (PDF p. 8), "Ingresos presupuestarios del sector público (Millones de pesos)", Enero–Diciembre
    2024 (preliminary): Impuesto al valor agregado **1,407,982.5**; Impuesto especial sobre producción y
    servicios **628,364.1**, of which "IEPS gasolinas y diésel" **403,583.9** and "IEPS distinto de gasolinas y
    diésel" 224,780.2; Impuestos a la importación **137,821.6**. The 2023 column gives IEPS gasolinas y diésel
    230,082.9 and IEPS distinto de gasolinas y diésel 215,019.0.

## How the lane uses it

Each ENIGH person's gross labor income bears their household's decile rate, IVA plus IEPS Otros as a share of
autonomous income. The households are ordered as SHCP orders them: monetary current income per capita, which is
the concentrado's `ing_cor` less imputed rent, remuneration in kind and transfers in kind (`estim_alqu`,
`remu_espec`, `transf_hog`, `trans_inst`). Deciles hold 10% of households each. Each cell's consumption tax is
carried like the withheld tax.

The fuel excise is added to each decile's rate, since SHCP's incidence leaves it out (quote 9). The 2024 fuel IEPS
(quote 11) is split over the deciles by SHCP's own fuel-spending shares (quote 10). Each decile's income is backed
out of Tabla 2.8, IVA revenue × the decile's share of IVA ÷ its IVA rate; the ten incomes sum to MXN 17.66tn and
reproduce the 8.0% average (a gate). The fuel rate is the decile's fuel excise over that income: 2.0–2.7%,
2.3% on average. [CALCULATION: mexico.py `fuel_ieps_by_decile`] Import duties (quote 11) and ISAN (quote 7) are
left out; spread like IVA, the duties would add about 0.8 points.

Four differences from SHCP's own ratio, none measured here [INFERENCE]:
- the base is ENIGH's gross labor income, not income adjusted to the national accounts;
- the low deciles' ratio includes spending out of transfers and remittances;
- IEPS was read from a chart's data labels, to one decimal;
- the fuel excise follows households' own fuel spending; the diesel burned in freight reaches all prices.
