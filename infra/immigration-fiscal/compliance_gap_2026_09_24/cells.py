"""Industry cells shared by the ACS and QCEW builders: one partition of private employment.

Each cell names the ACS INDNAICS codes it takes (exact codes, or prefixes ending in '*') and the
QCEW private-ownership NAICS codes that make it up, as (sign, code) terms. The partition covers
every private NAICS sector except public administration. The detail cells are the brief's focus
industries at the finest level where the ACS and QCEW codes line up:

- construction is one ACS code (23), so specialty trades 2381-2389 are QCEW outcomes only;
- landscaping (ACS 56173 = NAICS 561730) and the other services to buildings (ACS 5617Z = 5617
  less 561730, which holds janitorial 561720);
- restaurants and other food services (ACS 722Z = NAICS 722 less drinking places 7224; restaurants
  7225, or 7221 + 7222 before NAICS 2012, are QCEW outcomes);
- private households (814), crop (111) and animal production (112), support for agriculture (115).
"""
from __future__ import annotations

CELLS: dict[str, dict] = {
    "c111": {"label": "Crop production", "acs": ["111"], "qcew": [(1, "111")]},
    "c112": {"label": "Animal production", "acs": ["112"], "qcew": [(1, "112")]},
    "c115": {"label": "Support activities for agriculture", "acs": ["115"], "qcew": [(1, "115")]},
    "c11r": {"label": "Forestry, logging, fishing", "acs": ["1133", "113M", "114"],
             "qcew": [(1, "113"), (1, "114")]},
    "c21": {"label": "Mining", "acs": ["21*"], "qcew": [(1, "21")]},
    "c22": {"label": "Utilities", "acs": ["22*"], "qcew": [(1, "22")]},
    "c23": {"label": "Construction", "acs": ["23"], "qcew": [(1, "23")]},
    "c31": {"label": "Manufacturing", "acs": ["31*", "32*", "33*", "3MS"], "qcew": [(1, "31-33")]},
    "c42": {"label": "Wholesale trade", "acs": ["42*"], "qcew": [(1, "42")]},
    "c44": {"label": "Retail trade", "acs": ["44*", "45*", "4M", "4MS"], "qcew": [(1, "44-45")]},
    "c48": {"label": "Transportation and warehousing", "acs": ["48*", "49*"], "qcew": [(1, "48-49")]},
    "c51": {"label": "Information", "acs": ["51*"], "qcew": [(1, "51")]},
    "c52": {"label": "Finance and insurance", "acs": ["52*"], "qcew": [(1, "52")]},
    "c53": {"label": "Real estate and rental", "acs": ["53*"], "qcew": [(1, "53")]},
    "c54": {"label": "Professional and technical services", "acs": ["54*"], "qcew": [(1, "54")]},
    "c55": {"label": "Management of companies", "acs": ["55"], "qcew": [(1, "55")]},
    "c56173": {"label": "Landscaping services", "acs": ["56173"], "qcew": [(1, "561730")]},
    "c5617z": {"label": "Services to buildings except landscaping (janitorial)", "acs": ["5617Z"],
               "qcew": [(1, "5617"), (-1, "561730")]},
    "c56r": {"label": "Other administrative, support and waste services",
             "acs": ["5613", "5614", "5615", "5616", "561M", "562"],
             "qcew": [(1, "56"), (-1, "5617")]},
    "c61": {"label": "Educational services (private)", "acs": ["61*"], "qcew": [(1, "61")]},
    "c62": {"label": "Health care and social assistance (private)", "acs": ["62*"], "qcew": [(1, "62")]},
    "c71": {"label": "Arts, entertainment and recreation", "acs": ["71*"], "qcew": [(1, "71")]},
    "c721": {"label": "Accommodation", "acs": ["7211", "721M"], "qcew": [(1, "721")]},
    "c722z": {"label": "Restaurants and other food services", "acs": ["722Z"],
              "qcew": [(1, "722"), (-1, "7224")]},
    "c7224": {"label": "Drinking places", "acs": ["7224"], "qcew": [(1, "7224")]},
    "c81r": {"label": "Repair, personal and membership services", "acs": ["811*", "812*", "813*"],
             "qcew": [(1, "81"), (-1, "814")]},
    "c814": {"label": "Private households", "acs": ["814"], "qcew": [(1, "814")]},
}
FOCUS = ["c23", "c56173", "c5617z", "c722z", "c814", "c111", "c112", "c115"]
# QCEW outcome series for the focus cells, beyond the cell itself (state level, private)
OUTCOMES = {
    "q238": [(1, "238")],
    **{f"q{c}": [(1, c)] for c in ["2381", "2382", "2383", "2389"]},
    "q561720": [(1, "561720")],
    "q7225": [(1, "7225")],          # NAICS 2012 on
    "q7221_2": [(1, "7221"), (1, "7222")],  # the same restaurants before NAICS 2012
}


def acs_cell(indnaics: str) -> str | None:
    code = (indnaics or "").strip()
    for cell, spec in CELLS.items():
        for pat in spec["acs"]:
            if pat.endswith("*") and code.startswith(pat[:-1]):
                return cell
            if code == pat:
                return cell
    return None


def acs_case_sql(col: str = "INDNAICS") -> str:
    """A SQL CASE expression mapping INDNAICS to the cell id (exact codes before prefixes)."""
    exact, prefix = [], []
    for cell, spec in CELLS.items():
        for pat in spec["acs"]:
            (prefix if pat.endswith("*") else exact).append((pat, cell))
    parts = [f"WHEN {col} = '{p}' THEN '{c}'" for p, c in exact]
    parts += [f"WHEN {col} LIKE '{p[:-1]}%' THEN '{c}'" for p, c in prefix]
    return "CASE " + " ".join(parts) + " ELSE NULL END"
