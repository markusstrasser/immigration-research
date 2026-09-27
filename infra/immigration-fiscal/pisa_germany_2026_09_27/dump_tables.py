"""Dump header rows and the Germany/OECD rows of the PISA 2022 Vol I annex workbooks (chapter 7 and 5)."""
import openpyxl, sys

def dump(path, sheets, rows=("Germany", "OECD average"), maxhdr=14):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    for sh in sheets:
        ws = wb[sh]
        data = [list(r) for r in ws.iter_rows(values_only=True)]
        print(f"=== {path} :: {sh}")
        for r in data[:maxhdr]:
            vals = [str(v).replace("\n", " ") for v in r if v is not None]
            if vals:
                print("  HDR |", " | ".join(vals)[:900])
        for r in data:
            name = next((str(v).strip() for v in r[:3] if v is not None), "")
            if name in rows:
                print("  ROW |", name, "|", " | ".join("" if v is None else (f"{v:.2f}" if isinstance(v, float) else str(v)) for v in r[1:])[:1400])

if __name__ == "__main__":
    dump("_cache/statlink_qmuad8.xlsx", sys.argv[1].split(","), maxhdr=int(sys.argv[2]) if len(sys.argv) > 2 else 14)
