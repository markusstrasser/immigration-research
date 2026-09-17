import sys
from pypdf import PdfReader
r = PdfReader("raw/ICPSR_20520/DS0001/20520-0001-Codebook.pdf")
out = []
for i, p in enumerate(r.pages):
    try:
        t = p.extract_text() or ""
    except Exception as e:
        t = f"[[EXTRACT-FAIL {e}]]"
    out.append(f"\n===PAGE {i+1}===\n{t}")
open("cb.txt", "w").write("".join(out))
print("pages", len(r.pages))
