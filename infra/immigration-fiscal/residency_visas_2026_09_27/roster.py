"""Map the RGH internal-medicine roster to school countries and count the groups RESULT.md quotes.

Input: `_cache/rgh_im_current.txt`, the text of
https://education.rochesterregional.org/residencies/rgh-internal/current-residents/ (fetched 2026-09-28),
made by `strip_html.py _cache/rgh_im_current.html > _cache/rgh_im_current.txt`.
Outputs: `derived/roster_by_school_country.csv` (one row per listed resident, page order, no names) and
`derived/roster_counts.txt`.

School country is where the school is, not the resident's citizenship; the page states neither visa
nor citizenship. Weill Cornell Medicine-Qatar graduates are IMGs (WCM-Q admissions FAQ), so they sit
under Qatar. The flagged countries are those whose test centers NBME's agreement analysis covered:
Jordan, Nepal, Pakistan and India (Giri v. NBME, D.D.C. 1:24-cv-00410, Doc. 15-2 paras 6 and 9).
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

LANE = Path(__file__).resolve().parent
SRC = LANE / "_cache" / "rgh_im_current.txt"
OUT = LANE / "derived"
SECTIONS = {"Chief Residents": "Chief", "PGY3 Residents": "PGY3", "PGY2 Residents": "PGY2", "PGY1 Residents": "PGY1"}
END = "© Rochester Regional Health"
FLAGGED = {"Jordan", "Nepal", "Pakistan", "India"}
CARIBBEAN = {"Saba (Caribbean Netherlands)", "Caribbean (Ross University)", "Antigua and Barbuda"}

# (school country, pattern on the school string); every school must match exactly one country.
RULES = [
    ("United States", r"Lake Erie College of Osteopathic Medicine"),
    ("Saba (Caribbean Netherlands)", r"Saba University"),
    ("Caribbean (Ross University)", r"Ross University"),
    ("Antigua and Barbuda", r"American University of Antigua"),
    ("India", r"Lokmanya Tilak|Seth G\.S\.|Christian Medical College, Vellore|N\.H\.L\.|Ramaiah|Sri Ramachandra"
              r"|Government Medical College|Medical College Baroda|Gandhi Medical College|B\.J\. Medical College"
              r"|All India Institute of Medical Sciences|Bangalore Medical College|K\.S\. Hegde"
              r"|Academy of Medical Sciences|Vydehi|Medical College Thiruvananthapuram"),
    ("Pakistan", r"King Edward Medical University|Dow Medical College|Allama Iqbal Medical College"
                 r"|Rawalpindi Medical College|Chandka Medical College"),
    ("Sudan", r"University of Khartoum|Ahfad University"),
    ("Nepal", r"Tribhuvan|B\.P\. Koirala|Kathmandu Medical College|Patan Academy"),
    ("Egypt", r"Ain Shams|Cairo University"),
    ("United Arab Emirates", r"University of Sharjah"),
    ("Qatar", r"Weill Cornell Medical College in Qatar"),
    ("Ethiopia", r"Addis Ababa University"),
    ("China", r"Peking University|Zhejiang University"),
    ("Jordan", r"University of Jordan"),
    ("Iran", r"Tehran University"),
    ("Brazil", r"Universidade Cidade de Sao Paulo"),
    ("Spain", r"Universidad de Navarra"),
    ("Ukraine", r"Kharkiv National Medical University"),
    ("United Kingdom", r"Imperial College London"),
    ("Nigeria", r"University of Nigeria"),
    ("Indonesia", r"Universitas Gadjah Mada"),
    ("Bangladesh", r"Chittagong Medical College"),
    ("Morocco", r"Sidi Mohammed Ben Abdellah"),
    ("State of Palestine", r"Al-Quds University"),
    ("Algeria", r"Constantine 3"),
]


def parse(lines):
    """Return [(class_year, school)] from the roster text; stop loudly if its structure changed."""
    lines = [l.strip() for l in lines if l.strip()]
    missing = [h for h in list(SECTIONS) + [END] if h not in lines]
    if missing:
        sys.exit(f"[BLOCKED] roster headings missing from {SRC.name}: {missing}")
    body = lines[lines.index("Chief Residents"):lines.index(END)]
    rows, year, i = [], None, 0
    while i < len(body):
        if body[i] in SECTIONS:
            year = SECTIONS[body[i]]
            i += 1
            continue
        if i + 1 >= len(body) or body[i + 1] in SECTIONS:
            sys.exit(f"[BLOCKED] name without a school line near {body[i]!r}")
        rows.append((year, body[i + 1]))
        i += 2
    return rows


def country(school):
    hits = {c for c, rx in RULES if re.search(rx, school)}
    if len(hits) != 1:
        sys.exit(f"[BLOCKED] school maps to {len(hits)} countries {sorted(hits)}: {school!r}")
    return hits.pop()


def main():
    rows = [(y, s, country(s)) for y, s in parse(SRC.read_text(encoding="utf-8").splitlines())]
    group = lambda c: "US" if c == "United States" else "Caribbean" if c in CARIBBEAN else "elsewhere"
    OUT.mkdir(exist_ok=True)
    with open(OUT / "roster_by_school_country.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["class_year", "school", "school_country", "group", "nbme_flagged_country"])
        for y, s, c in rows:
            w.writerow([y, s, c, group(c), "yes" if c in FLAGGED else "no"])

    n = len(rows)
    by_year = Counter(y for y, _, _ in rows)
    by_group = Counter(group(c) for _, _, c in rows)
    elsewhere = Counter(c for _, _, c in rows if group(c) == "elsewhere")
    small = {c: k for c, k in elsewhere.items() if k <= 2}
    flagged = sum(c in FLAGGED for _, _, c in rows)
    nepal = elsewhere["Nepal"]
    pct = lambda k: f"{k} of {n} ({k / n:.1%})"
    out = [f"names listed  {n}"]
    out += [f"  {y:6s} {by_year[y]}" for y in SECTIONS.values()]
    out += [f"group {g:10s} {pct(by_group[g])}" for g in ("US", "Caribbean", "elsewhere")]
    out += ["elsewhere by school country:"]
    out += [f"  {c:22s} {k}" for c, k in sorted(elsewhere.items(), key=lambda t: (-t[1], t[0]))]
    out += [f"elsewhere countries with 1-2 residents  {len(small)} countries, {sum(small.values())} residents",
            f"Nepal school  {pct(nepal)}",
            f"NBME flagged-analysis countries (Jordan, Nepal, Pakistan, India)  {pct(flagged)}"]
    (OUT / "roster_counts.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
