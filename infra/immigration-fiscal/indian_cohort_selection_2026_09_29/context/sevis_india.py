"""ICE SEVP 'SEVIS by the Numbers' (calendar years): India active student records and STEM OPT authorizations.
Parses pdftotext -layout output of the per-country PDFs in _cache/context/sevis; appends to context/flows_2015_2025.csv.
Records are SEVIS records (F-1 and M-1 students), not persons in a given day; calendar-year basis."""
import csv, hashlib, pathlib, re, subprocess
LANE = pathlib.Path(__file__).resolve().parents[1]
S = LANE / "_cache/context/sevis"
BASE = "https://www.ice.gov/doclib/sevis/btn/"
rows = []
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
for pdf in sorted(S.glob("*all-students-by-coc.pdf")) + sorted(S.glob("*all-coc-stem-opt.pdf")):
    txt = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    y = int(re.search(r"btn-(20\d\d)-", pdf.name).group(1))
    line = next(l for l in txt.splitlines() if re.match(r"\s*INDIA\s+[\d,]+\s*$", l))
    v = int(re.search(r"([\d,]+)\s*$", line).group(1).replace(",", ""))
    series = "sevis_active_student_records" if "all-students" in pdf.name else "sevis_stem_opt_authorized_records"
    rows.append(["ICE SEVIS by the Numbers (by-country PDF)", y, series, v, "SEVIS records, citizens of India, calendar year",
                 f"_cache/context/sevis/{pdf.name}", line.strip(), BASE + pdf.name, sha(pdf)])
p24 = S / "25_0605_2024-sevis-btn.pdf"
t24 = subprocess.run(["pdftotext", "-layout", str(p24), "-"], capture_output=True, text=True, check=True).stdout
l = next(x for x in t24.splitlines() if re.match(r"\s*India\s+422,335\s*$", x))
rows.append(["ICE SEVIS by the Numbers 2024 report", 2024, "sevis_active_student_records", 422335, "SEVIS records, citizens of India, calendar year",
             f"_cache/context/sevis/{p24.name}", l.strip(), BASE + p24.name, sha(p24)])
rows.append(["ICE SEVIS by the Numbers 2024 report (derived)", 2024, "sevis_stem_opt_participants_derived", round(0.480 * 165524),
             "students, India share x total (derived)", f"_cache/context/sevis/{p24.name}",
             "STEM OPT extension were from India (48.0%) or China (20.4%), with 165,524 foreign students participating in STEM OPT in 2024.",
             BASE + p24.name, sha(p24)])
with open(LANE / "context/flows_2015_2025.csv", "a", newline="") as fh:
    csv.writer(fh, lineterminator="\n").writerows(rows)
for r in rows: print(r[1], r[2], r[3])
