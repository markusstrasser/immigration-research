"""Recompute the CE 2024 Hispanic vs income-bracket comparison with column-aligned brackets.

The first pass of this lane read income from the $70,000-$99,999 column of Table 1203 but every
other 'matched' figure from the $100,000-$149,999 column. This script parses both spreadsheets and
prints Hispanic shares against (a) the income-matched bracket $70-100k and (b) the size-matched
bracket $100-150k, plus the non-Hispanic 'white, Asian and all other races' column of Table 2200.
Run: uv run --with openpyxl python3 ce_income_matched.py
"""
import csv, pathlib, warnings
import openpyxl
warnings.filterwarnings("ignore")
HERE = pathlib.Path(__file__).resolve().parent
ITEMS = ["Food at home", "Food away from home", "Alcoholic beverages", "Housing", "Apparel and services",
         "Transportation", "Vehicle purchases (net outlay)", "Healthcare", "Entertainment",
         "Personal care products and services", "Reading", "Education",
         "Tobacco products and smoking supplies", "Miscellaneous", "Cash contributions",
         "Personal insurance and pensions", "Life and other personal insurance"]
HEADERS = ["Income before taxes", "Average annual expenditures", "People", "Homeowner"]


def load(fn):
    ws = openpyxl.load_workbook(HERE / fn, read_only=True).active
    return [list(r) for r in ws.iter_rows(values_only=True)]


def pick(rows, label, kind):
    """First row whose first cell equals label; return the following 'Share'/'Mean' row, or the row itself."""
    for i, r in enumerate(rows):
        if r and isinstance(r[0], str) and r[0].strip() == label:
            if kind == "self":
                return [float(x) for x in r[1:] if x not in (None, "n.a.")]
            for j in range(i + 1, i + 4):
                if rows[j] and rows[j][0] == kind:
                    return [float(x) for x in rows[j][1:] if x is not None]
    raise KeyError(label)


lat, inc = load("latino_2024.xlsx"), load("income_2024.xlsx")
# Table 2200 columns: All | Hispanic | Not Hispanic total | NH white, Asian, other | NH Black
# Table 1203 columns: All | <15k | 15-30k | 30-40k | 40-50k | 50-70k | 70-100k | 100-150k | 150-200k | 200k+
H, NHW = 1, 3
B70, B100 = 6, 7
hdr = {}
for lab in HEADERS:
    kind = "Mean" if lab in ("Income before taxes", "Average annual expenditures") else "self"
    a, b = pick(lat, lab, kind), pick(inc, lab, kind)
    hdr[lab] = (a[H], a[NHW], b[B70], b[B100])
    print(f"{lab:30}{a[H]:>12,.1f}{a[NHW]:>12,.1f}{b[B70]:>12,.1f}{b[B100]:>12,.1f}")
print(f"{'':30}{'Hispanic':>12}{'NH wh/As/oth':>12}{'$70-100k':>12}{'$100-150k':>12}")
out = [["item", "hisp_share", "nhw_share", "b70_100_share", "b100_150_share", "h_over_nhw", "h_over_b70", "h_over_b100"]]
print(f"\n{'item':40}{'H%':>6}{'NHW%':>6}{'70k%':>6}{'100k%':>6}{'H/NHW':>7}{'H/70k':>7}{'H/100k':>7}")
for it in ITEMS:
    a, b = pick(lat, it, "Share"), pick(inc, it, "Share")
    h, w, b7, b1 = a[H], a[NHW], b[B70], b[B100]
    r = lambda x, y: round(x / y, 2) if y else None
    out.append([it, h, w, b7, b1, r(h, w), r(h, b7), r(h, b1)])
    print(f"{it:40}{h:6.1f}{w:6.1f}{b7:6.1f}{b1:6.1f}{r(h,w) or 0:7.2f}{r(h,b7) or 0:7.2f}{r(h,b1) or 0:7.2f}")
tot = hdr["Average annual expenditures"]
print(f"\nTotal expenditure $: Hispanic {tot[0]:,.0f}  NHW {tot[1]:,.0f}  $70-100k {tot[2]:,.0f}  $100-150k {tot[3]:,.0f}")
print(f"Hispanic / $70-100k = {tot[0]/tot[2]:.3f};  Hispanic / $100-150k = {tot[0]/tot[3]:.3f}")
with open(HERE / "ce_income_matched.csv", "w", newline="") as f:
    csv.writer(f).writerows(out)
