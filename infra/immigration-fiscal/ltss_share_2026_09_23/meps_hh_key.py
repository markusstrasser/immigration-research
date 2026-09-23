"""The account's MEPS Medicaid key with and without home-health dollars.

Carving HCBS out of the Medicaid line leaves the rest keyed by MEPS. MEPS records Medicaid home
health (agency HHAMCD24, non-agency HHNMCD24), which is part of HCBS, so the key for the remainder
should not carry it. This rebuilds the builder's `medicaid` key (MEPS 2024 age-band x US/not-US
birth cell means of TOTMCD24 on the CPS ASEC 2025 civilian population, exposure rule as in
full_account_spending_2026_09_20/builder.py), gates it against incidence_keys.csv, then recomputes
it without home health and for home health alone. Also reports MEPS's national Medicaid and
Medicaid home-health totals.
Writes derived/meps_hh_key.json. Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ltss_share_2026_09_23/meps_hh_key.py
"""
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
sys.path.insert(0, str(FISCAL / "build"))
sys.path.insert(0, str(FISCAL / "full_account_spending_2026_09_20"))
import builder  # noqa: E402
import meps_health_transport_2024 as transport  # noqa: E402

HH = ["HHAMCD24", "HHNMCD24"]


def main():
    archive = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
    if builder.sha(archive) != builder.CPS_SHA:
        raise SystemExit("[BLOCKED] CPS source changed")
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
              "PRDTHSP", "PUB", "PRIV", "MIL", "CHAMPVA"]
    with zipfile.ZipFile(archive) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]) \
            .rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    civ, target = builder.canonical_target(d)
    weight = d.pwwgt0.to_numpy(float)
    transport.FIELDS = list(dict.fromkeys(transport.FIELDS + HH))
    meps = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
    md, _ = transport.read_meps(meps, meps.with_name("h256su.txt"))
    if (md[HH] < 0).any().any():
        raise SystemExit("[BLOCKED] reserved code in home-health payer fields")
    cells, codes, _ = transport.donor_model(md, d, False)
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    sample = md.loc[valid].copy()
    sample["hh_mcd"] = sample[HH].sum(axis=1)
    sample["mcd_ex_hh"] = sample.TOTMCD24 - sample.hh_mcd
    index = pd.MultiIndex.from_frame(cells[["age_band", "born"]])
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    pop = sample.groupby(["age_band", "born"]).PERWT24F.sum()
    out = {}
    for name, col in [("medicaid", "TOTMCD24"), ("medicaid_ex_home_health", "mcd_ex_hh"),
                      ("home_health_only", "hh_mcd")]:
        sums = sample.assign(wx=sample[col] * sample.PERWT24F).groupby(["age_band", "born"]).wx.sum()
        v = (sums / pop).reindex(index).to_numpy()[codes] * exposure
        out[name] = float(v[target] @ weight[target] / (v[civ] @ weight[civ]))
    keys = pd.read_csv(FISCAL / "full_account_spending_2026_09_20/derived/incidence_keys.csv")
    published = float(keys[(keys.allocation == "personal") & (keys.key == "medicaid")].target_share.iloc[0])
    gate = abs(out["medicaid"] - published) < 1e-12
    pos = md.PERWT24F.gt(0)
    res = dict(key_share=out, published_medicaid_key=published, gate_reproduces_published_key=bool(gate),
               meps_national_medicaid_bn=float((md.loc[pos, "TOTMCD24"] * md.loc[pos, "PERWT24F"]).sum() / 1e9),
               meps_national_medicaid_home_health_bn=float((md.loc[pos, HH].sum(axis=1) * md.loc[pos, "PERWT24F"]).sum() / 1e9))
    (HERE / "derived").mkdir(exist_ok=True)
    (HERE / "derived/meps_hh_key.json").write_text(json.dumps(res, indent=1) + "\n")
    for k, v in res.items():
        print(f"  {k}: {v}")
    if not gate:
        raise SystemExit("✗ key does not reproduce incidence_keys.csv")
    print("  ✓ medicaid key reproduced")


if __name__ == "__main__":
    main()
