"""Per-year ratio stability for the categories that drive the cost weighting."""
import pandas as pd
from pathlib import Path
C = Path(__file__).resolve().parent / "_cache" / "light_texas"
d = pd.read_stata(C / "detailed_category.dta"); d["category"] = d["category"].astype("string").fillna("NA")
d["undoc_rate"] = d.undocumented_immigrants_charge / d.pop_undoc * 1e5
d["legal_rate"] = d.immigrants_charge / d.tot_legal2_immi * 1e5
d["cit_rate"] = d.citizen_charge / d.tot_citizen * 1e5
for cat in ["homicide", "sexual_assault", "sexual offsenses", "assault", "Traffic", "kidnapping"]:
    x = d[d.category == cat].set_index("year")
    print(cat, "legal/cit:", (x.legal_rate / x.cit_rate).round(2).tolist(), " undoc/cit:", (x.undoc_rate / x.cit_rate).round(2).tolist())
