"""Fetch only the pinned USDA workbook; refuse upstream revision without review."""
import hashlib
import json
from pathlib import Path
import urllib.request

here=Path(__file__).resolve().parent
source=json.loads((here/"source_cells.json").read_text())["snap"]
data=urllib.request.urlopen(source["url"],timeout=30).read()
actual=hashlib.sha256(data).hexdigest()
if actual!=source["sha256"]:
    raise SystemExit(f"Source changed, requires review: {actual}")
dest=here/"_cache/snap-monthly.xlsx"
dest.parent.mkdir(parents=True,exist_ok=True)
dest.write_bytes(data)
print(dest)
