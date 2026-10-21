"""Q3 Switzerland case: origin composition and skill mix of the foreign resident population.

Inputs:
- BFS (FSO) SAKE/ESPA table "Selon différentes nationalités: Degré de formation de la population résidante
  permanente et des personnes actives occupées selon le sexe" (asset 35367255), sheet Population_Annuel,
  first block (both sexes), thousands of persons. Downloaded to _cache/ if absent.
- STATPOP composition by nationality at end-2024, thousands, copied from the BFS page
  bfs.admin.ch/.../auslaendische-bevoelkerung/zusammensetzung.html (table "Ständige ausländische
  Wohnbevölkerung nach Staatsangehörigkeit (am Jahresende, in Tausend)").

Outputs: derived/q3_switzerland_education.csv, derived/q3_switzerland_composition.csv
"""
import csv
import pathlib
import urllib.request

import pandas as pd

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache"
DERIVED = LANE / "derived"
EDU_URL = "https://dam-api.bfs.admin.ch/hub/api/dam/assets/35367255/master"
LEVELS = ["Degré secondaire I", "Degré secondaire II", "Degré tertiaire", "Sans indication"]
YEARS = [2010, 2024]
# BFS STATPOP end-2024, thousands (page table, column 2024).
STATPOP_2024 = {
    "Total foreign": 2479.9, "EU/EFTA": 1561.1, "Germany": 329.9, "France": 171.1, "Italy": 342.4,
    "Austria": 48.0, "Portugal": 257.3, "Spain": 99.0, "Other Europe (non-EU/EFTA)": 481.4,
    "Kosovo": 116.4, "North Macedonia": 70.5, "Turkiye": 78.3, "Ukraine": 68.3, "Africa": 127.7,
    "Americas": 91.7, "Asia": 210.8, "Oceania": 4.4, "Stateless/unknown": 2.7,
}


def edu_table():
    path = CACHE / "bfs_edu_nat.xlsx"
    if not path.exists():
        CACHE.mkdir(exist_ok=True)
        urllib.request.urlretrieve(EDU_URL, path)
    v = pd.read_excel(path, sheet_name="Population_Annuel", header=None)
    header = v.iloc[4].tolist()
    col = {int(float(h)): i for i, h in enumerate(header) if str(h).replace(".0", "").isdigit()}
    labels = [str(x).strip() for x in v.iloc[:, 0].fillna("").tolist()]
    out, level, seen = {}, None, set()
    for r, lab in enumerate(labels):
        if lab.startswith("1)"):  # footnotes close the first block
            break
        if lab in LEVELS + ["Total"] and r > 4:
            if lab in seen:  # first block only (both sexes)
                break
            level = lab
            seen.add(lab)
            continue
        if level and lab not in ("nan", ""):
            key = lab.split(" ")[0] if lab.startswith("UE/AELE") else lab
            out[(level, key)] = {y: num(v.iat[r, col[y]]) for y in YEARS}
    return out


def num(x):
    """BFS marks '(n)' for estimates from fewer than 50 observations and 'X' for fewer than 5."""
    s = str(x).strip().strip("()")
    return float("nan") if s in ("X", "", "nan") else float(s)


def main():
    t = edu_table()
    groups = ["Suisses", "Etrangers", "Allemagne", "France", "Italie", "Autriche", "Espagne", "Portugal",
              "Autres", "UE/AELE", "Etats tiers"]
    DERIVED.mkdir(exist_ok=True)
    with open(DERIVED / "q3_switzerland_education.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["group", "year", "total_thousands", "share_secondary_I", "share_tertiary"])
        for g in groups:
            for y in YEARS:
                tot = t[("Total", g)][y]
                w.writerow([g, y, f"{tot:.1f}", f"{t[('Degré secondaire I', g)][y] / tot:.3f}",
                            f"{t[('Degré tertiaire', g)][y] / tot:.3f}"])
                print(g, y, round(tot), round(t[('Degré secondaire I', g)][y] / tot, 3),
                      round(t[('Degré tertiaire', g)][y] / tot, 3))
    total = STATPOP_2024["Total foreign"]
    with open(DERIVED / "q3_switzerland_composition.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["nationality_group", "thousands_end2024", "share_of_foreign"])
        for k, x in STATPOP_2024.items():
            w.writerow([k, x, f"{x / total:.3f}"])


if __name__ == "__main__":
    main()
