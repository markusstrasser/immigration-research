"""Shared attainment scale for placing Mexico-born US migrants in Mexico's schooling distribution.

Both sides are mapped onto one ordinal scale of highest level completed. A source category is an
interval [lo, hi] on this scale; a US census bin such as "grade 5-8" or an INEGI bin such as
"primaria 1 a 5 grados" spans several levels. Ridits are computed on the finest partition whose
cut points exist on BOTH sides, so no within-bin split is ever assumed for the ridit.

Index  Label  Meaning (US grade equivalent; Mexican level)
  0    L0     no schooling or preschool only
  1-5  L1-L5  grades 1-5 (primaria 1-5)
  6    L6     grade 6 (primaria completa)
  7-8  L7-L8  grades 7-8 (secundaria 1-2; tecnico/comercial con primaria 1-2)
  9    L9     grade 9 (secundaria completa; tecnico con primaria 3+)
 10-11 L10-11 grades 10-11 (media superior 1-2: preparatoria, tecnico con secundaria, normal basica)
 12    L11b   US "12th grade, no diploma" (no Mexican analogue; Mexico has zero mass here)
 13    L12    upper secondary completed (US diploma/GED, "some college <1 year";
              preparatoria 3+, tecnico con secundaria 3+, normal basica 3+)
 14    L13a   1-3 approved years of tertiary without a credential (US "1+ years of college, no
              degree"; licenciatura 1-3 grados)
 15    L13b   short-cycle tertiary credential (US associate degree; tecnico con preparatoria)
 16    L16    4+ years of tertiary (US bachelor's or higher; licenciatura 4+ grados, posgrado)
"""
N_LEVELS = 17
LABELS = ["L0", "L1", "L2", "L3", "L4", "L5", "L6", "L7", "L8", "L9", "L10", "L11", "L11b",
          "L12", "L13a", "L13b", "L16"]

# Brief's five categories: none/primary incomplete, primary, lower secondary, upper secondary,
# tertiary. Main convention ("attended"): any approved tertiary year is tertiary, matching INEGI's
# nivel de escolaridad. US "12th grade, no diploma" counts as lower secondary (no credential).
FIVE = {"c1_none_primary_incomplete": (0, 5), "c2_primary": (6, 8), "c3_lower_secondary": (9, 12),
        "c4_upper_secondary": (13, 13), "c5_tertiary": (14, 16)}
# Credential convention: tertiary years without a credential count as upper secondary (as in
# INEGI's ISCED 2011 attainment table, sheet 13 of the 2020 workbook).
FIVE_CREDENTIAL = {"c1_none_primary_incomplete": (0, 5), "c2_primary": (6, 8), "c3_lower_secondary": (9, 12),
                   "c4_upper_secondary": (13, 14), "c5_tertiary": (15, 16)}
FIVE_NAMES = list(FIVE)

# Approximate completed years at each level, only for mean-years anchors against INEGI's
# published grado promedio (not used in any ridit or share).
YEARS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 12, 14, 14, 16.5]
