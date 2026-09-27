# INEGI, ENIGH 2024, Cuestionario para personas de 12 o más años

Used for: the income concept of Mexican earnings (take-home pay, grossed up in mexico.py), the labor-income
claves, and the formal-job flag (SAR or AFORE among the job's benefits).

Source: INEGI, Encuesta Nacional de Ingresos y Gastos de los Hogares 2024, Cuestionario para personas de 12 o
más años (2025). Local copy `_cache/reads/enigh2024_cuest_personas_mayores.pdf`, text in
`_cache/reads/enigh2024_cuest_personas_mayores.txt` (line numbers below).

## Quotes

1. The income concept (Apartado 2.2, "Ingresos monetarios del trabajo principal para subordinados", lines
   226-229; the instruction is line 228): "Ahora le voy a preguntar acerca de sus ingresos. Si le están descontando algún préstamo recibido,
   pagos que hace porque la empresa le prestó dinero para comprar su casa, pago que realiza si adquirió un
   seguro voluntario, por favor incluya ese monto en su ingreso." The question (line 237): "1. ¿Cuánto dinero
   recibió por ...?" Only voluntary deductions are added back; income tax and social-security withholding are
   not, so the recorded amount is take-home pay. The same instruction precedes the secondary job's income
   (line 608).

2. Main job, subordinate workers (lines 240-272): "Sueldos, salarios o jornal P001", "Destajo P002",
   "Comisiones y propinas P003", "Horas extras P004", "Incentivos, gratificaciones o premios P005", "Bono,
   percepción adicional o sobresueldo P006", "Primas vacacionales y otras prestaciones en dinero P007",
   "Reparto de utilidades del ejercicio 2023 P008", "Aguinaldo del ejercicio 2023 P009".

3. Secondary job, subordinate workers (lines 617-644): "1. ¿Cuánto dinero recibió por este trabajo en...?
   Entrevistador: Sume todos los ingresos monetarios reportados. P014"; "Reparto de utilidades del ejercicio
   2023 P015"; "Aguinaldo del ejercicio 2023" (P016).

4. Benefits of the job (line 151; the secondary job repeats it at line 536): "1. ¿En este trabajo le dieron las siguientes prestaciones, aunque no ...";
   option (line 170; line 553 for the secondary job) "SAR o AFORE ... 08". In the microdata this is `trabajos.pres_8` = "08".

5. For contrast, CMP's ENIGH 2002 question asked for gross pay: "Cuánto recibió el mes pasado por sueldos,
   salarios y jornales en el mes pasado? (declare su ingreso bruto)" (reads/clemens_montenegro_pritchett_2009.md,
   quote 6).

## How the lane uses them

- Labor income is the concentrado's monetary labor income (the 36 claves in mexico.py LABOR_CLAVES; gate
  `enigh_labor_claves_reproduce_concentrado`).
- A job is formal when it carries SAR or AFORE (pres_8) and the worker is subordinate (subor 1). Its pay
  (P001-P009 for the main job, P014-P016 for a secondary job) is grossed up by the 2024 statutory withholding
  (reads/oecd_taxing_wages_2025_mexico.md). Informal pay, independent work and business income are taken as
  received.
