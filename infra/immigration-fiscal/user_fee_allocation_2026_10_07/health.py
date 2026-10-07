"""Public hospitals: what is left of the fee term once the case charges uncompensated care by use.

S&L health and hospital charges are $364.091bn in 2024 (NIPA T3.10.5 line 59; T3.17 nets $364.544bn from S&L
health). The account charges S&L health consumption, the net, at the health_services key (6.8% of the line at main
case v5 with its state-price line and the lineage). A public hospital's net is sum_p (1 - r_p) C_p over payers p: the cost C_p of the care each payer
covers and the payment-to-cost ratio r_p. The group's net is sum_p (1 - r_p) C_p^g. Charging the group s_K of the
national net instead leaves
    residual = sum_p (1 - r_p) C_p (s_p - s_K),  s_p = the group's share of payer p's hospital care.
The uninsured term (r near 0, s_0 = 25.7% of uninsured person-years) is the uncompensated care the case already charges
by use (uncompensated_care_2026_09_23; decision 2026-09-23, the uninsured-use key on the Medicaid line), so it is left
out here. This script sizes the insured terms: Medicare, Medicaid, and private and other payers.

Inputs:
  - s_p from MEPS 2024 (HC-256, the account's MEPS file): the group (HISPNCAT 1, Mexican) share of hospital facility
    payments (inpatient, outpatient, emergency) by payer, with design-based standard errors (VARSTR/VARPSU, Taylor
    linearisation of a ratio of totals). MEPS has no hospital ownership, so the shares are for all hospitals
    [ASSUMPTION: the group's payer-specific share of care is the same at government hospitals].
  - Government hospitals' payer mix and payment-to-cost ratios [SOURCE: Milliman, "Policy considerations for designing
    hospital payment systems for Medicaid programs", Nov 2024, HCRIS 2021: Medicaid 20.1% of services at
    government-owned hospitals, payments 95.4% of cost; AHA Chartbook 2018 Table 4.4, community hospitals 2016:
    Medicare 86.8%, Medicaid 88.1%, private 144.8% of cost]. Medicare's and private payers' shares of government
    hospitals' costs are not in those sources: 0.35 and 0.36 central, with ranges [ASSUMPTION].
  - G, government hospitals' gross cost in 2024: Census 2022 S&L hospital current spending ($261.2bn less $11.2bn
    capital) scaled by NIPA's S&L health gross over Census hospital plus health spending [APPROX], $295.6bn. NIPA's
    charges ($364.1bn) exceed it: Census books state Medicaid payments to local hospitals as intergovernmental
    revenue, not charges [INFERENCE], so fee_lines.py also prices G = the charges over the payers' ratio (an arm).
The pricing (s_K, the union's frame, the arms) is in fee_lines.py.

Writes derived/health_meps_shares.csv and derived/health.json. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/health.py
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = REPO / "infra/immigration-fiscal"
sys.path.insert(0, str(FISCAL / "build"))
from public_mvp_io import parse_meps_sas_fields  # noqa: E402

MEPS = REPO / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip"
SU = MEPS.with_name("h256su.txt")
PINS = {MEPS: None, SU: None}   # filled from the spending lane's SOURCE_PINS.json, which pins both
OUT = HERE / "derived"
PAYERS = ["SLF", "MCR", "MCD", "PRV", "VA", "TRI", "OFD", "STL", "WCP", "OSR"]
EVENTS = ["IPF", "OPF", "ERF"]
NIPA_HEALTH_CHARGES_BN = 364.091   # T3.10.5 line 59
# Government hospitals' gross cost, 2024 [APPROX]: Census of Governments 2022 Table 1 lines 81-82 (hospitals $261.242bn,
# capital outlay $11.246bn) x NIPA 2024 S&L health gross (T3.17 line 27, $491.383bn) over Census 2022 hospitals plus
# health ($261.242bn + $154.261bn).
G_BN = (261.242 - 11.246) * 491.383 / (261.242 + 154.261)
MIX = {  # cost shares of government hospitals' care by payer, central and range; uninsured is the rest
    "medicare": (0.35, [0.30, 0.42]),
    "medicaid": (0.201, [0.201]),
    "private_other": (0.36, [0.30, 0.42]),
}
PCR = {  # payment-to-cost ratios
    "medicare": (0.868, [0.82, 0.90]),
    "medicaid": (0.954, [0.90, 1.00]),
    "private_other": (1.448, [1.30, 1.50]),
}


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def verify():
    pins = json.loads((FISCAL / "full_account_spending_2026_09_20/SOURCE_PINS.json").read_text())
    by_name = {Path(p["name"]).name: p["sha256"] for p in pins["sources"]}
    for path in [MEPS, SU]:
        if by_name.get(path.name) != sha(path):
            raise SystemExit(f"[BLOCKED] {path} is not the MEPS file the account pins")


def read_meps():
    layout = parse_meps_sas_fields(SU)
    fields = ["HISPNCAT", "PERWT24F", "VARSTR", "VARPSU", "INSCOV24", "AGE24X"] + \
        [f"{e}{p}24" for e in EVENTS for p in PAYERS + ["EXP", "TCH"]]
    missing = [f for f in fields if f not in layout]
    if missing:
        raise SystemExit(f"[BLOCKED] MEPS layout lacks {missing}")
    rows = []
    with zipfile.ZipFile(MEPS) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".dat")]
        for line in z.open(names[0]):
            t = line.decode("ascii")
            rows.append([float(t[layout[k][0]:sum(layout[k])]) for k in fields])
    d = pd.DataFrame(rows, columns=fields)
    if len(d) != 19140:
        raise SystemExit("[BLOCKED] MEPS record count is not the codebook's 19,140")
    d = d[d.PERWT24F > 0].copy()
    money = [c for c in fields if c[:3] in EVENTS]
    if (d[money] < 0).any().any():
        raise SystemExit("[BLOCKED] a reserved negative code in a MEPS amount")
    for p in PAYERS + ["EXP", "TCH"]:
        d[p] = sum(d[f"{e}{p}24"] for e in EVENTS)
    if not np.allclose(d[PAYERS].sum(axis=1), d.EXP, atol=2.0 * len(EVENTS)):
        raise SystemExit("[BLOCKED] facility payments by payer do not add to the total")
    d["group"] = d.HISPNCAT.eq(1).astype(float)
    return d


def ratio_se(d, y):
    """Group share of a total, sum(w g y) / sum(w y), and its Taylor-linearised design SE."""
    w = d.PERWT24F
    Y = float((w * d[y]).sum())
    R = float((w * d.group * d[y]).sum()) / Y
    z = w * d[y] * (d.group - R) / Y
    t = pd.DataFrame({"h": d.VARSTR, "j": d.VARPSU, "z": z}).groupby(["h", "j"]).z.sum().reset_index()
    var = 0.0
    for _, g in t.groupby("h"):
        n = len(g)
        if n > 1:
            var += n / (n - 1) * float(((g.z - g.z.mean()) ** 2).sum())
    return R, var ** 0.5, Y / 1e9


def main():
    verify()
    d = read_meps()
    d["MEDICARE"] = d.MCR
    d["MEDICAID"] = d.MCD
    d["PRIVATE_OTHER"] = d.EXP - d.MCR - d.MCD - d.SLF   # private, TRICARE, VA, other federal, S&L, WC, other
    rows = []
    for y in ["MEDICARE", "MEDICAID", "PRIVATE_OTHER", "PRV", "SLF", "EXP", "TCH"]:
        r, se, tot = ratio_se(d, y)
        rows.append(dict(measure=y, group_share=r, se=se, national_meps_bn=tot,
                         group_records_with_amount=int(((d.group == 1) & (d[y] > 0)).sum())))
    d["UNINS"] = d.INSCOV24.eq(3).astype(float)
    d["ONE"] = 1.0
    for y in ["UNINS", "ONE"]:
        r, se, tot = ratio_se(d, y)
        rows.append(dict(measure="persons_uninsured" if y == "UNINS" else "persons", group_share=r, se=se,
                         national_meps_bn=tot, group_records_with_amount=int(((d.group == 1) & (d[y] > 0)).sum())))
    t = pd.DataFrame(rows)
    t.to_csv(OUT / "health_meps_shares.csv", index=False, lineterminator="\n", float_format="%.6f")
    s = t.set_index("measure").group_share
    se = t.set_index("measure").se

    # The all-hospital check: charges as a use measure against payments, insured and uninsured together.
    out = dict(g_bn=G_BN, meps_shares={k: float(v) for k, v in s.items()},
               meps_se={k: float(v) for k, v in se.items()},
               charges_vs_payments=dict(group_share_charges=float(s.TCH), group_share_payments=float(s.EXP),
                                        ratio=float(s.EXP / s.TCH)),
               nipa_health_charges_bn=NIPA_HEALTH_CHARGES_BN,
               mix=MIX, pcr=PCR,
               group_definition="MEPS HISPNCAT 1 (Mexican, Mexican American, Chicano; no other Hispanic group)")
    (OUT / "health.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(t.to_string(index=False))
    print(json.dumps({k: out[k] for k in ["g_bn", "charges_vs_payments"]}, indent=1))


if __name__ == "__main__":
    main()
