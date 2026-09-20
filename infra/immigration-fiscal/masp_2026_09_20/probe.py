"""Inventory the author-distributed MASP file; do not estimate outcomes."""
from pathlib import Path
import hashlib
import json
import re
import zipfile
import pyreadstat

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'derived'
OUT.mkdir(exist_ok=True)
raw = ROOT / 'raw/masp_combined.dta'
assert raw.stat().st_size == 16365775, 'Incomplete or changed author file'
data, meta = pyreadstat.read_dta(raw)
assert len(data) > 0 and len(data.columns) > 0
fields = {k: v for k, v in meta.column_names_to_labels.items()
          if re.search(r'generat|ethnic|birth|educ|income|arrest|incarcer|weight', v or '', re.I)}
result = {'rows': len(data), 'columns': len(data.columns),
          'files': {p.name: {'bytes': p.stat().st_size,
                    'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
                    for p in [raw, ROOT / 'raw/codebook.zip']},
          'selected_labels': fields}
with zipfile.ZipFile(ROOT / 'raw/codebook.zip') as archive:
    assert archive.testzip() is None
    result['codebook_members'] = archive.namelist()
    for name in archive.namelist():
        if name.lower().endswith('.pdf') and not name.startswith('__MACOSX/'):
            (OUT / Path(name).name).write_bytes(archive.read(name))
(OUT / 'inventory.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result, indent=2))
