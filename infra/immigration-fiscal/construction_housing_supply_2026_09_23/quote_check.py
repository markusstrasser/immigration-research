"""Re-find every quote and source number RESULT.md takes from a paper read in this lane.

Each item is (source, string). A string passes when it is a substring of the source text after
the same normalisation on both sides: Unicode NFKC (ligatures), minus signs and dashes to "-",
whitespace collapsed; for the two corpus parses (markdown) also table-cell tags, star groups and
emphasis marks removed. Number items pair a coefficient with its neighbours or its SE row as
printed, so a hit locates the table cell. Sources are the pdftotext files in _cache/papers/ and
two corpus parses. The reader files in reads/ carry their own quote checks.

Run from the repository root:
  uv run --no-project python3 infra/immigration-fiscal/construction_housing_supply_2026_09_23/quote_check.py
"""
from __future__ import annotations

import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
PAPERS = HERE / "_cache/papers"
CORPUS = pathlib.Path.home() / "Projects/corpus"
SOURCES = {
    "hwz": PAPERS / "hwz_nov2025.txt",
    "monras": CORPUS / "doi_10_1086_707764",
    "wz": CORPUS / "doi_10_24149_wp2607",
    "br": PAPERS / "bratsberg_cdp0610.txt",
    "go": PAPERS / "gonzalez_ortega_dp4333.txt",
    "cs": PAPERS / "cabral_swp2024-40.txt",
    "east": PAPERS / "east_dp11486.txt",
    "cravino": PAPERS / "cravino_w34790.txt",
    "bs": PAPERS / "bohn_santillano_ir2017.txt",
}
MARKDOWN = {"monras", "wz"}
ITEMS = [
    # Howard, Wang and Zhang (Nov 2025)
    ("hwz", "Cracking Down, Pricing Up: Housing Supply in the Wake of Mass"),
    ("hwz", "November 10, 2025"),
    ("hwz", "-0.540*** -0.519*** -0.165** -0.192***"),
    ("hwz", "(0.067) (0.066) (0.068) (0.059)"),
    ("hwz", "reduction of 5.7% relative to the pre-policy baseline rate of new"),
    ("hwz", "(2.89 units per 1,000 people)"),
    ("hwz", "0.045*** 0.048*** 0.044***"),
    ("hwz", "(0.011) (0.011) (0.010)"),
    ("hwz", "SC Activated 0.013 0.004 0.001 (0.010) (0.010) (0.011)"),
    ("hwz", "SC Activated*Bottom Quartile 0.034*** (0.009) SC Activated*2nd Quartile 0.020** (0.009)"),
    ("hwz", "SC Activated*3rd Quartile -0.010 (0.014) SC Activated*Top Quartile -0.041** (0.020)"),
    ("hwz", "-0.772*** -0.694*** -0.702*** -0.163 -1.014***"),
    ("hwz", "(0.109) (0.118) (0.135) (0.337) (0.371)"),
    ("hwz", "an estimated reduction of 299,000 construction workers—a 2.7% decline in the workforce"),
    ("hwz", "a reduction of 228,000 workers, or 2.1% of the 11 million workers"),
    ("hwz", "SC Activated*US-born -0.003 -0.006 (0.011) (0.010)"),
    ("hwz", "SC Activated*LEFB 0.042*** 0.022** (0.013) (0.011)"),
    ("hwz", "SC Activated -0.64 -0.01 -0.01 (0.44) (0.01) (0.01)"),
    ("hwz", "a decline of 77bps"),
    ("hwz", "4.59 million observations of newly constructed homes"),
    ("hwz", "300,000 people are deported under SC during our sample period"),
    ("hwz", "The phased rollout of SC between 2008 and 2013"),
    ("hwz", "undocumented labor appears to complement domestic labor"),
    # Monras (JPE 2020, accepted manuscript)
    ("monras", "Immigration and Wage Dynamics: Evidence from the Mexican Peso Crisis"),
    ("monras", "Internal relocation dissipates this shock spatially"),
    ("monras", "since Mexican immigrant workers disproportionately enter the construction sector and lower construction costs"),
    ("monras", "of Mexicans divided by low-skilled workers in the labor market of interest"),
    ("monras", "Relative Inflow of Mexicans, 1990 - 2000 -0.244 -0.548 (0.336) (0.366)"),
    ("monras", "Relative Inflow of Mexicans, 1990 - 2000 -0.284 -1.171 (0.291) (0.518)"),
    ("monras", "-0.0866 -0.780 (0.497) (0.424)"),
    ("monras", "-0.202 -1.430 (0.294) (0.704)"),
    ("monras", "First-stage F-stat 42.73"),
    ("monras", "First-stage F-stat 15.89"),
    ("monras", "-0.00831 -0.255 (0.168) (0.160)"),
    ("monras", "0.0312 -0.384 (0.103) (0.232)"),
    ("monras", "0.652 0.495 0.118 0.00268 -0.144 -0.454"),
    ("monras", "(0.101) (0.0980) (0.0776) (0.0694) (0.216) (0.213)"),
    ("monras", "0.598 0.373 0.103 -0.0197 -0.0539 -0.765"),
    ("monras", "(0.0488) (0.0551) (0.0428) (0.0453) (0.142) (0.330)"),
    ("monras", "prices should decrease by around .6*1.4=.84"),
    ("monras", "This difference in Census data for 1990 and 2000 is around 40 percent"),
    ("monras", "because they may be paid lower wages, perhaps because they are less unionized"),
    ("monras", "Relative Inflow of Mexican, 1990 - 2000 1.873 2.159 (0.446) (0.329)"),
    # Wilson and Zhou (Dallas Fed WP 2607)
    ("wz", "Working Paper 2607 March 2026"),
    ("wz", "UIWF -0.208 -0.227 0.00998 (0.213) (0.170) (0.0650)"),
    ("wz", "F Statistic 14.05 14.05 14.05"),
    ("wz", "UIWF 2.189 1.438 1.229 1.470 (0.741) (0.344) (0.529) (0.287)"),
    ("wz", "UIWF acted primarily as a housing demand shock in an environment of relatively fixed short-run housing supply"),
    # Bratsberg and Raaum (CReAM DP 06/10)
    ("br", "-.103 -.724 -.554 -.570 -.032 -.569"),
    ("br", "(.162) (.202) (.175) (.183) (.175) (.180)"),
    ("br", "-1.155 -1.028 -.763 -.387"),
    ("br", "(.214) (.231) (.163) (.088)"),
    ("br", "largely cost-based"),
    # Gonzalez and Ortega (IZA DP 4333)
    ("go", "Immigration and Housing Booms: Evidence from Spain"),
    ("go", "0.395*** 0.421*** 0.330*** 0.383*** 0.462***"),
    ("go", "[0.0447] [0.0443] [0.0473] [0.0455] [0.0329]"),
    ("go", "0.460** 0.568** 0.635** 0.635* 0.906**"),
    ("go", "[0.212] [0.227] [0.281] [0.340] [0.383]"),
    ("go", "population equal to one percent of the total population leads to an increase in house prices of 3.2%"),
    ("go", "the supply of housing would probably have been much more inelastic"),
    # Cabral and Steingress (BoC SWP 2024-40)
    ("cs", "Last updated: October 24, 2024"),
    ("cs", "1.407*** 2.920*** 3.486*** 3.026*** 1.959***"),
    ("cs", "[0.203] [0.642] [0.862] [1.042] [0.551]"),
    ("cs", "1.161** 1.377*** 1.647*** 0.678*"),
    ("cs", "[0.564] [0.487] [0.575] [0.404]"),
    ("cs", "0.611*** 1.765*** 2.041*** 1.477*** 1.208***"),
    ("cs", "[0.148] [0.327] [0.446] [0.490] [0.339]"),
    ("cs", "0.813*** 0.854*** 0.886*** 0.616***"),
    ("cs", "[0.287] [0.252] [0.253] [0.188]"),
    ("cs", "-0.472*** -0.263** -0.134** 0.027 -0.136"),
    ("cs", "[0.063] [0.119] [0.065] [0.091] [0.100]"),
    ("cs", "0.625*** 0.755*** 0.711*** 0.833*** 0.918***"),
    ("cs", "[0.054] [0.098] [0.085] [0.107] [0.110]"),
    ("cs", "IV F-Stat 43 33 19 21 23"),
    ("cs", "could be a result of outmigration of current residents or a change in preferences"),
    ("cs", "period 1985–2019"),
    # East, Luck, Mansour and Velasquez (IZA DP 11486)
    ("east", "The Labor Market Effects of Immigration Enforcement"),
    ("east", "-90.423 -64.551 -21.549 -2.401 -1.922"),
    ("east", "(25.444) (19.377) (13.183) (3.388) (1.859)"),
    ("east", "Y mean 535.78"),
    ("east", "-15.413 5.500 6.100 -12.898 -14.115"),
    ("east", "(50.579) (32.046) (29.416) (15.240) (12.676)"),
    ("east", "Y mean 3835.98"),
    # Cravino, Levchenko, Ortega and Pandalai-Nayar (NBER w34790)
    ("cravino", "THE ECONOMIC IMPACT OF MASS DEPORTATIONS"),
    ("cravino", "In 2024, 3.2% of US workers were unauthorized"),
    ("cravino", "removing 50% of all unauthorized workers (about 3.7 million)"),
    ("cravino", "long-run relative price changes are small on average"),
    ("cravino", "the relative price increases reach 0.8-0.9% in some regions"),
    ("cravino", "11% of employment and 10% of the wage"),
    ("cravino", "and some construction occupations a 0.8% increase"),
    ("cravino", "This elasticity takes a value of 3 in our baseline calibration"),
    ("cravino", "set to η = 1.6"),
    # Bohn and Santillano (Industrial Relations 2017), numbers used from reads/search_gaps.md
    ("bs", "–0.050** –0.094** –0.020 0.002"),
    ("bs", "(0.062) (0.023) (0.039) (0.016) (0.026)"),
    ("bs", "0.114*** –0.020** –0.019* –0.023** –0.008"),
    ("bs", "(0.009) (0.009) (0.010) (0.009) (0.011)"),
]
STAR_GROUP = re.compile(r"\[[∗*]+\]")


def norm(text: str, markdown: bool) -> str:
    text = unicodedata.normalize("NFKC", text)
    for dash in ("−", "–", "—"):
        text = text.replace(dash, "-")
    if markdown:
        text = STAR_GROUP.sub(" ", text.replace("<br>", " ").replace("|", " "))
        text = re.sub(r"[_*]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def load(key: str) -> str:
    path = SOURCES[key]
    if path.is_dir():
        parses = sorted(path.glob("parsed*/page.md"))
        if not parses:
            raise SystemExit(f"[BLOCKED] no corpus parse under {path}")
        path = parses[0]
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path}")
    return norm(path.read_text(errors="replace"), key in MARKDOWN)


def main() -> int:
    texts = {key: load(key) for key in SOURCES}
    missing = 0
    for key, string in ITEMS:
        hit = norm(string, key in MARKDOWN) in texts[key]
        missing += not hit
        print(f"  {'✓' if hit else '✗'} {key}: {string}")
    print(f"{len(ITEMS)} checked, {missing} missing")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
