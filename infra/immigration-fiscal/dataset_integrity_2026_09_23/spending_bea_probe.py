"""Spending audit probe: dump BEA NIPA Table 3.12 and 3.1 rows for 2024 from the pinned workbook."""
import sys
import pandas as pd

WB = "/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
xl = pd.ExcelFile(WB)
for sheet in sys.argv[1:]:
    df = xl.parse(sheet, header=None)
    # locate year header row
    hdr = None
    for i in range(12):
        row = [str(x) for x in df.iloc[i].tolist()]
        if any(c.strip() in ("2024", "2024.0") for c in row):
            hdr = i
            break
    cols = [str(x).replace(".0", "") for x in df.iloc[hdr].tolist()]
    want = [j for j, c in enumerate(cols) if c in ("2019", "2022", "2023", "2024")]
    print("==", sheet, "header row", hdr)
    for i in range(0, len(df)):
        vals = [df.iat[i, j] for j in want]
        print(i, str(df.iat[i, 0])[:6], str(df.iat[i, 1])[:70], vals)
