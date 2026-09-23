"""Fetch INEGI census education tabulations (national, sex x age x level/grade) into _cache/inegi
and pin URL, size and sha256 in sources.json.

INEGI drops long transfers mid-way (the 2015 workbook first arrived at 5.6 of 11.4 MB), so each
file is fetched over HTTP/1.1 with byte-range resume until its size matches Content-Length, and
the payload's magic bytes are checked (INEGI answers unknown paths with a 2 KB HTML page and 200).

The 2020 workbook is read from the repository's staged copy (see arrival_cohorts_2026_09_18/ACQUIRED.md)
and only hashed here.

  uv run --no-project python3 infra/immigration-fiscal/schooling_selection_position_2026_09_23/fetch_inegi.py
"""
import hashlib
import json
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE = HERE / "_cache" / "inegi"

B2010 = "https://www.inegi.org.mx/contenidos/programas/ccpv/2010/tabulados/Basico/"
FILES = [
    ("cpv2000/CPyV2000_NAL_Caracteristicas_educativas.pdf",
     "https://www.inegi.org.mx/contenidos/programas/ccpv/2000/tabulados/CPyV2000_NAL_Caracteristicas_educativas.pdf",
     "XII Censo 2000 tabulados basicos, national: Educacion 5 (primaria grades), 7 (secundaria and "
     "tecnico con primaria grades), 8 (media superior grades, parts 1-2), 9 (profesional grades)"),
    ("cpv2010/07_08B_ESTATAL.xls", B2010 + "07_08B_ESTATAL.xls",
     "Censo 2010 cuestionario basico Educacion 8: 3+ by entidad, sex, 5-year age; primaria grades"),
    ("cpv2010/07_10B_ESTATAL.xls", B2010 + "07_10B_ESTATAL.xls",
     "Educacion 10: 12+ by entidad, sex, 5-year age; secundaria and tecnico con primaria grades"),
    ("cpv2010/07_11B_ESTATAL.xls", B2010 + "07_11B_ESTATAL.xls",
     "Educacion 11: 15+ by entidad, sex, age; media superior grades"),
    ("cpv2010/07_12B_ESTATAL.xls", B2010 + "07_12B_ESTATAL.xls",
     "Educacion 12: 18+ by entidad, sex, age; tecnico con preparatoria and profesional grades"),
    ("cpv2010/07_14B_ESTATAL.xls", B2010 + "07_14B_ESTATAL.xls",
     "Educacion 14: 15+ by entidad, sex, 5-year age; nivel de escolaridad and grado promedio (anchor)"),
    ("eic2015/06_educacion.xls",
     "https://www.inegi.org.mx/contenidos/programas/intercensal/2015/tabulados/06_educacion.xls",
     "Encuesta Intercensal 2015 tabulados, Educacion 7-11 (survey estimates: percentages with standard "
     "errors). Not used: for five-year age groups primaria is one total and media superior and superior "
     "have no grade detail, so the C1/C2 and C3/C4 boundaries cannot be drawn by birth cohort"),
]
STAGED_2020 = ("sources/immigration-fiscal/data/external/stage3/inegi/cpv_educacion/cpv2020_b_eum_07_educacion.xlsx",
               "https://www.inegi.org.mx/contenidos/programas/ccpv/2020/tabulados/cpv2020_b_eum_07_educacion.xlsx",
               "Censo 2020 cuestionario basico, Educacion 11 (levels and grades by sex and age) and 13 (ISCED)")
MAGIC = {".pdf": b"%PDF", ".xls": bytes.fromhex("d0cf11e0"), ".xlsx": b"PK"}


def content_length(url: str) -> int:
    out = subprocess.run(["curl", "-sI", "--http1.1", "--max-time", "60", url], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.lower().startswith("content-length:"):
            return int(line.split(":", 1)[1])
    raise SystemExit(f"[FAILED] no Content-Length for {url}")


def fetch(rel: str, url: str) -> Path:
    dest = CACHE / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    want = content_length(url)
    for attempt in range(1, 11):
        if dest.exists() and dest.stat().st_size == want:
            break
        if dest.exists() and dest.stat().st_size > want:
            dest.unlink()
        subprocess.run(["curl", "-s", "--http1.1", "--max-time", "600", "-C", "-", "-o", str(dest), url])
        time.sleep(2)
    if not dest.exists() or dest.stat().st_size != want:
        raise SystemExit(f"[FAILED] {rel}: size {dest.stat().st_size if dest.exists() else 0} != {want}")
    if not dest.read_bytes()[:4].startswith(MAGIC[dest.suffix][:4]):
        raise SystemExit(f"[FAILED] {rel}: payload is not a {dest.suffix} file")
    return dest


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    rows = []
    for rel, url, note in FILES:
        p = fetch(rel, url)
        rows.append({"file": f"_cache/inegi/{rel}", "url": url, "bytes": p.stat().st_size,
                     "sha256": sha(p), "fetched": time.strftime("%Y-%m-%d"), "content": note})
        print(f"{rel}: {p.stat().st_size} bytes {rows[-1]['sha256'][:16]}")
    p = ROOT / STAGED_2020[0]
    rows.append({"file": STAGED_2020[0], "url": STAGED_2020[1], "bytes": p.stat().st_size, "sha256": sha(p),
                 "fetched": "2026-09-22 (arrival_cohorts_2026_09_18/ACQUIRED.md)", "content": STAGED_2020[2]})
    (HERE / "sources.json").write_text(json.dumps(rows, indent=2) + "\n")
    print(f"wrote sources.json ({len(rows)} files)")


if __name__ == "__main__":
    main()
