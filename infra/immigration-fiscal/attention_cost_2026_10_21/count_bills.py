"""Count 118th-Congress bills (H.R. and S.) by Congress.gov policy area, from GovInfo BILLSTATUS bulk XML.

Downloads BILLSTATUS-118-{hr,s}.zip (35.5 MB + 14.4 MB) into _cache/ if absent, reads each bill's
<policyArea><name>, and flags bills whose action list records "Became Public Law".
Writes derived/bills_policy_area_118.csv (policy_area, introduced, became_law).

Run: uv run --no-project python3 infra/immigration-fiscal/attention_cost_2026_10_21/count_bills.py
"""
import collections
import csv
import pathlib
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
OUT = HERE / "derived" / "bills_policy_area_118.csv"
URL = "https://www.govinfo.gov/bulkdata/BILLSTATUS/118/{t}/BILLSTATUS-118-{t}.zip"
TYPES = ["hr", "s"]


def main() -> None:
    CACHE.mkdir(exist_ok=True)
    intro, law = collections.Counter(), collections.Counter()
    n = 0
    for t in TYPES:
        z = CACHE / f"BILLSTATUS-118-{t}.zip"
        if not z.exists():
            urllib.request.urlretrieve(URL.format(t=t), z)
        with zipfile.ZipFile(z) as zf:
            for name in zf.namelist():
                if not name.endswith(".xml"):
                    continue
                root = ET.fromstring(zf.read(name))
                bill = root.find("bill")
                pa = bill.findtext("policyArea/name") or "(none)"
                intro[pa] += 1
                n += 1
                texts = " ".join(a.findtext("text") or "" for a in bill.iter("item"))
                if "Became Public Law" in texts:
                    law[pa] += 1
    if n < 15000:
        raise SystemExit(f"[BLOCKED] only {n} bills parsed; expected ~19k H.R.+S.")
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["policy_area", "introduced", "became_law"])
        for pa, c in sorted(intro.items(), key=lambda kv: -kv[1]):
            w.writerow([pa, c, law[pa]])
        w.writerow(["TOTAL", n, sum(law.values())])
    print(f"  ✓ {n} bills; immigration {intro['Immigration']} introduced, {law['Immigration']} became law")


if __name__ == "__main__":
    main()
