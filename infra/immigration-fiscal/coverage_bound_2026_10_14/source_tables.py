"""Parse coverage rates from pinned Census PDF tables; never transcribe estimates."""
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path

from pypdf import PdfReader

LANE = Path(__file__).resolve().parent
LABELS = ["0 to 4", "5 to 9", "10 to 17", "18 to 29 males", "18 to 29 females",
          "30 to 49 males", "30 to 49 females", "50 and over males", "50 and over females"]


def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] " + why)


def parse_row(line, label):
    require(line.strip().startswith(label), "unexpected source row")
    fields = re.findall(r"-?\d+(?:\.\d+)?|\bX\b|\bNR\b", line.strip()[len(label):])
    require(len(fields) == 14, "coverage table row shape changed: " + label)
    require(fields[-2] not in ("NR", "X") and fields[-1] not in ("NR", "X"), "missing coverage estimate")
    return {"nce_pct": float(fields[-2]), "se_pct": float(fields[-1])}


def block(page, title):
    lines = page.extract_text(extraction_mode="layout").splitlines()
    starts = [i for i, x in enumerate(lines) if x.strip().startswith(title)]
    require(len(starts) == 1, "no unique PES table group " + title)
    start = starts[0]
    result = {"all": parse_row(lines[start], title)}
    for label, line in zip(LABELS, lines[start + 1:start + 10], strict=True):
        result[label] = parse_row(line, label)
    return result


def load():
    pins = json.loads((LANE / "inputs/pins.json").read_text())
    for name in ("pes_cross.pdf", "pes_national.pdf", "da_hispanic.xlsx", "da_age.xlsx", "legacy.json",
                 "controls/base_adjustments.csv", "controls/base_adjustments_sex.csv", "controls/compare_base.py"):
        path = LANE / "inputs" / name
        require(hashlib.sha256(path.read_bytes()).hexdigest() == pins[name]["sha256"], "stale source " + name)
    reader = PdfReader(LANE / "inputs/pes_cross.pdf")
    require(len(reader.pages) == 16, "PES document version changed")
    hispanic = block(reader.pages[8], "Hispanic or Latino")
    white = block(reader.pages[6], "Non-Hispanic White Alone")
    total_line = next(x for x in reader.pages[5].extract_text(extraction_mode="layout").splitlines()
                      if x.strip().startswith("Total "))
    total = parse_row(total_line, "Total")
    # Poppler handles this report's embedded CFF fonts without a new Python dependency.
    national = subprocess.run(["pdftotext", "-layout", str(LANE / "inputs/pes_national.pdf"), "-"],
                              capture_output=True, text=True, check=True)
    candidates = [re.findall(r"-?\d+(?:\.\d+)?", x.replace("–", "-"))
                  for x in national.stdout.splitlines() if x.strip().startswith("Hispanic or Latino")]
    require(any(len(x) == 4 and float(x[0]) == hispanic["all"]["nce_pct"]
                and float(x[1]) == hispanic["all"]["se_pct"] for x in candidates),
            "PES origin marginal lacks national positive control")
    base = {}
    with (LANE / "inputs/controls/base_adjustments.csv").open() as stream:
        for r in csv.DictReader(stream):
            key = (int(r["age_2020_lo"]), int(r["age_2020_hi"]))
            require(key not in base, "duplicate base interval")
            base[key] = {k: float(v) if v else None for k, v in r.items()}
    with (LANE / "inputs/controls/base_adjustments_sex.csv").open() as stream:
        for r in csv.DictReader(stream):
            key = (int(r["age_2020_lo"]), int(r["age_2020_hi"]), int(r["sex"]))
            require(key not in base, "duplicate sex-specific base interval")
            base[key] = {k: float(v) if v else None for k, v in r.items()}
    return {"hispanic": hispanic, "nonhispanic_white": white, "total": total}, base


def main():
    rates, base = load()
    output = []
    for origin, rows in rates.items():
        for age, row in (rows.items() if origin != "total" else [("all", rows)]):
            output.append({"origin": origin, "age_sex": age, **row,
                           "pdf_page": 9 if origin == "hispanic" else 7 if origin == "nonhispanic_white" else 6,
                           "table": "C" if origin != "total" else "B"})
    with (LANE / "derived/coverage_rates.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=output[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(output)
    da_rows = []
    for (lo, hi), cell in [(k, v) for k, v in base.items() if len(k) == 2 and k[1] <= 29]:
        for series in ("low", "middle", "high"):
            estimate = cell["da_" + series]
            da_rows.append({"origin": "Hispanic", "age_2020_lo": lo, "age_2020_hi": hi,
                            "series": series, "da_population": estimate, "census_population": cell["census_hispanic"],
                            "nce_vs_census_pct": 100 * (cell["census_hispanic"] / estimate - 1),
                            "residual_vs_blended_base_pct": 100 * cell["da_residual_factor_" + series],
                            "source": "DA Table1C age counts plus Census DHC P12H and V2024 R-file base"})
    with (LANE / "derived/da_coverage.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=da_rows[0].keys(), lineterminator="\n")
        writer.writeheader()
        writer.writerows(da_rows)
    print("primary-source rates PASS; " + str(len(output)) + " parsed rows")


if __name__ == "__main__":
    main()
