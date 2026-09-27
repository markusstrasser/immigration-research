# OECD, Taxing Wages 2025, Mexico chapter and Table 1.3; DOF decree of 1 May 2024

Used for: the statutory gross-up of ENIGH take-home pay to gross pay, and the income tax and employee social
security contributions withheld from formal wages in Mexico (mexico.py `mx_withholding`, `gross_from_net`).

Sources:
- OECD (2025), *Taxing Wages 2025*, Mexico chapter,
  https://www.oecd.org/en/publications/taxing-wages-2025_b3a95829-en/full-report/mexico_98ddd565.html
  (fetched 2026-09-27 through Exa web_fetch).
- OECD (2025), *Taxing Wages 2025*, chapter 1 (Overview), Table 1.3,
  https://www.oecd.org/en/publications/taxing-wages-2025_b3a95829-en/full-report/overview_715add19.html
- DOF 01/05/2024, "DECRETO que otorga el subsidio para el empleo",
  https://dof.gob.mx/nota_detalle.php?codigo=5725287&fecha=01/05/2024

## Quotes

1. Average wage (Mexico chapter): "The national currency is the peso (MXN). In 2024, MXN 18.31 were equal to
   USD 1. That year, the estimated earnings of the average worker are MXN 199 946 (Secretariat estimate)."
   The parameter table gives "Average earnings/yr Ave_earn 199 946 714", read as MXN 199,946.714.

2. Employment subsidy credit (Mexico chapter): "By Presidential Decree of May 1, 2024, the employment subsidy
   credit table was replaced by a monthly amount equivalent to 11.82% of the monthly value of the UMA,
   applicable uniformly to all workers whose monthly taxable income for salary does not exceed MXN 9 081, this
   will be applied against their income tax of the corresponding calendar month. In cases in which the tax
   payable by the employee is less than the monthly employment subsidy credit, the difference cannot be carried
   forward or refunded." And: "Until April 30, 2024 the employment subsidy credit was decreasing on workers'
   income and was assigned based on a table of income brackets. For monthly income higher than MXN 7 382 no
   employment subsidy credit was given. Employees with an income tax lower than the credit received in cash the
   difference along with their salary."

3. The DOF decree (Artículo Segundo): "Se otorga un subsidio para el empleo mensual a los trabajadores ... cuyos
   ingresos mensuales que sirvan de base para calcular el impuesto sobre la renta correspondiente al mes de
   calendario de que se trate, no excedan de $9,081.00 ... hasta por la cantidad que resulte de multiplicar el
   valor mensual de la Unidad de Medida y Actualización por 11.82%." Recital: "para el ejercicio fiscal de 2024,
   el porcentaje de 11.82% representa un monto mensual de $390.00". Transitorio Primero: "El presente decreto
   entra en vigor el 1 de mayo de 2024."

4. Annual tax schedule 2024 (Mexico chapter, "Tax schedule"): lower limit / fixed quota / rate on the excess:
   0.01 / 0.00 / 1.92%; 8 952.50 / 171.88 / 6.40%; 75 984.56 / 4 461.94 / 10.88%; 133 536.08 / 10 723.55 /
   16.00%; 155 229.81 / 14 194.54 / 17.92%; 185 852.58 / 19 682.13 / 21.36%; 374 837.89 / 60 049.40 / 23.52%;
   590 796.00 / 110 842.74 / 30.00%; 1 127 926.85 / 271 981.99 / 32.00%; 1 503 902.47 / 392 294.17 / 34.00%;
   4 511 707.38 / 1 414 947.85 / 35.00%.

5. The pre-May credit table (annual; lower limit / credit): 0.0 / 4 884.24; 21 227.53 / 4 881.96; 31 840.57 /
   4 879.44; 41 674.09 / 4 713.24; 42 454.45 / 4 589.52; 53 353.81 / 4 250.76; 56 606.17 / 3 898.44;
   64 025.05 / 3 535.56; 74 696.05 / 3 042.48; 85 366.81 / 2 611.32; 88 587.97 / 0.00. Parameter
   "Basic_crd_2024 4 681.47"; "UMA 108.57".

6. Employee contributions (Mexico chapter): "For sickness and maternity insurance, 0.625% of the workers monthly
   wage, plus 0.40% of the amount in excess of 3 UMAs. For disability and life insurance, 0.625% of the monthly
   wage. In 2024, a ceiling of 25 UMAs applies to the salary that is used to calculate the social security
   contributions." Parameters "SSC_rate 0.0125", "SSC_rate_sur 0.0040".

7. Contributions to the private individual accounts, excluded from OECD's tax measures but withheld from pay
   (Mexico chapter, "Main employees' and employers' contributions to private pension, health, etc. schemes"):
   "Employees' contributions — Discharge and old age insurance — 1.125" (% of workers' monthly wage).

8. The 2024 tax equations (Mexico chapter): "Allowances tax_al B MIN(earn, MIN(earn*(12/365)*0.25, UMA*15)+
   MIN(earn*(15/365), UMA*30))"; "CG taxable income tax_inc B Positive(earn-tax_al)"; "Tax credits tax_cr B
   1/3*VLOOKUP(tax_inc, Basic_crd, 2) +2/3*IF(tax_inc<max_inc_tc,Basic_crd24,0)"; "Employees' soc security SSC
   B MIN(earn*ssc_rate, UMA*25*30.4*12*ssc_rate)+MIN(Positive(earn-(3*30.4*12*UMA))*ssc_rate_sur,
   UMA*(25-3)*30.4*12*ssc_rate_sur)".

9. The check the code must reproduce (chapter 1, Table 1.3, "Income tax plus employee social security
   contributions, 2024, As % of gross wage earnings", single worker at the average wage): "Mexico 12.2 10.8 1.4
   20 297" (total, income tax, employee SSC, gross wage in USD PPP). The text: "The lowest personal average tax
   rates were in Mexico (12.2%), Costa Rica (10.7%), Chile (7.2%) and Colombia (0.0%)."

10. The minimum wage (Mexico chapter, note 1): "For 2024, the value of the UMA is 108.57, mean while the general
    minimum wage is 248.93 and 374.89 in the northern border region."

11. Minimum-wage earners are not withheld from. LISR art. 96, first paragraph (text as reproduced by
    mexico.justia.com and mley.mx; primary: diputados.gob.mx/LeyesBiblio/pdf/LISR.pdf): "Quienes hagan pagos
    por los conceptos a que se refiere este Capítulo están obligados a efectuar retenciones y enteros mensuales
    que tendrán el carácter de pagos provisionales a cuenta del impuesto anual. No se efectuará retención a las
    personas que en el mes únicamente perciban un salario mínimo general correspondiente al área geográfica del
    contribuyente." LSS art. 36 (diputados.gob.mx/LeyesBiblio/pdf/LSS.pdf): "Corresponde al patrón pagar
    íntegramente la cuota señalada para los trabajadores, en los casos en que éstos perciban como cuota diaria
    el salario mínimo."

## How the lane uses them

- `max_inc_tc` is not printed in the parameter table; the lane uses the decree's MXN 9,081 a month, 108,972 a
  year, on taxable income, as the chapter's text states.
- The pre-May credit (a third of the year) may exceed the tax and was paid in cash; the post-May credit (two
  thirds) may not. The lane floors only the post-May part at zero, where OECD's single equation floors neither.
- The withheld amount that counts as a Mexican tax is income tax plus the employee contributions of item 6.
  The 1.125% of item 7 goes to the worker's own retirement account: it is part of gross pay, but not a tax.
- Gross pay up to a full year at the general minimum wage with the statutory aguinaldo (15 days) and holiday
  premium (25% of 12 days), 248.93 x (364.8 + 15 + 3), carries no withholding (items 10-11). The northern
  border's higher minimum is not applied.
- ISSSTE (federal employees) charges higher employee contributions than IMSS; the lane applies the IMSS rules
  to every formal worker, so it understates the gross pay and withholding of public employees.
