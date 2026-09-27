"""Gates for the carry-over identity lane. Run after cps_identity.py (both labels), acs_ancestry.py and
corrected_step.py. Reads the other lanes read-only. Exit code 1 on any failed check."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
D = HERE / "derived"
CARRY = FISCAL / "generation_carryover_2026_09_27"
FAIL = []


def check(ok, msg):
    print(("  ✓ " if ok else "  ✗ ") + msg)
    if not ok:
        FAIL.append(msg)


# 1. Every group the carry-over lane published reproduces from this lane's own gap tables.
pairs = {("pop", "G2"): "G2", ("pop", "G3plus_all"): "G3plus_all", ("cores_one", "G2"): "G2",
         ("cores_one", "G3anc_id"): "G3_obs", ("cores_both", "G3anc_id"): "G3_obs",
         ("cores_both", "G4par_id"): "G4plus_obs", ("cores_both", "G2"): "G2"}
for label in ("CPS_ASEC_2022_2025", "CPS_ASEC_2022_2026"):
    mine = pd.read_csv(D / f"cps_identity_gaps_{label}.csv").query("reference == 'white3plus'")
    pub = pd.read_csv(CARRY / "derived" / f"cps_gaps_{label}.csv")
    worst, cells = 0.0, 0
    for (frame, grp), gen in pairs.items():
        a = mine[(mine.frame == frame) & (mine.generation == grp)].set_index("measure")
        b = pub[(pub.frame == frame) & (pub.generation == gen)].set_index("measure")
        for m in b.index:
            worst = max(worst, abs(a.gap[m] - b.gap[m]), abs(a.se[m] - b.se[m]), abs(a.n[m] - b.n[m]))
            cells += 1
    check(worst < 1e-9 and cells >= 50, f"{label}: {cells} published carry-over cells reproduced (max diff {worst:.1e})")

# 2. The published ratios the correction starts from are the carry-over lane's.
co = pd.read_csv(CARRY / "derived/carryover.csv")
cs = pd.read_csv(D / "corrected_step.csv")
for m in ("ba_plus", "earnings_worker_mean", "ledger_partial_per_adult"):
    r_pub = co[(co.source == "CPS_ASEC_2022_2025") & (co.frame == "pop") & (co.measure == m)
               & (co.generation == "G2->G3plus_all")].rho.iloc[0]
    r_me = cs[(cs.source == "CPS_ASEC_2022_2025") & (cs.measure == m)].rho_published.unique()
    check(len(r_me) == 1 and abs(r_me[0] - r_pub) < 1e-12, f"published rho {m} {r_pub:.4f} matches carryover.csv")

# 3. The corrected ratio is rho (1 - a c) on every single-value row.
single = cs[cs.kind != "composite"]
err = (single.rho_corrected - single.rho_published * (1 - single.hidden_share * single.closing_share)).abs().max()
check(err < 1e-12, f"rho_corrected = rho (1 - a c) on {len(single)} rows (max err {err:.1e})")
comp = cs[cs.kind == "composite"]
err = (comp.rho_corrected - comp.rho_published * (1 - comp.hidden_share * comp.closing_share)).abs().max()
check(err < 1e-12, f"composite rows equal rho (1 - a c_effective) on {len(comp)} rows (max err {err:.1e})")

# 4. Hidden shares are the upstream values, not retyped.
pa = pd.read_csv(FISCAL / "identity_loss_propagation_2026_09_27/derived/population_arms.csv")
b = pa[(pa.arm == "b_one_step")].hidden_share_of_third_plus.iloc[0]
c = pa[(pa.arm == "c_compound") & (pa.rho == 0.5)].hidden_share_of_third_plus.iloc[0]
a_used = sorted(cs.hidden_share.unique())
check(abs(a_used[1] - b) < 5e-5 and abs(a_used[2] - c) < 5e-5, f"hidden shares {a_used[1]}/{a_used[2]} = propagation {b:.4f}/{c:.4f}")
dec = pd.read_csv(FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_dt_decomposition.csv")
vals = dec.select_dtypes("number").to_numpy().ravel()
check(any(abs(v - 28.25) < 0.01 for v in vals) and any(abs(v - 11.19) < 0.01 for v in vals),
      "11.19% and 28.25% bracket rates appear in the population lane's decomposition")

# 5. NLSY97 constants against the paper text (Tables 12 and 13, PDF pp.56-57).
txt = (CARRY / "_cache/dp12704.txt").read_text()
t12 = txt[txt.index("Table 12: Rates of Hispanic"):txt.index("Table 13: Educational Attainment")]
t13 = txt[txt.index("Table 13: Educational Attainment"):txt.index("Table 14: Average Years")]
for v in ("94.63", "79.38", "97.37", "86.97", "(1.82)", "(4.58)", "(0.82)", "(2.71)"):
    check(v in t12, f"Table 12 contains {v}")
row = lambda s: re.findall(r"\(?\d+\.\d+\)?", s)
id_line = [l for l in t13.splitlines() if l.strip().startswith("Identified as Hispanic")][0]
nid_line = [l for l in t13.splitlines() if l.strip().startswith("Not identified as Hispanic")][0]
check(row(id_line)[:4] == ["13.58", "85.50", "51.96", "23.01"], f"Table 13 identifiers {row(id_line)[:4]}")
check(row(nid_line)[:4] == ["14.22", "82.07", "49.26", "29.17"], f"Table 13 non-identifiers {row(nid_line)[:4]}")
for v in ("(5.18)", "(13.70)", "(4.85)", "(1.16)", "24.28", "13.70"):
    check(v in t13, f"Table 13 contains {v}")

# 6. Duncan-Trejo 2017 Table 8 Mexico row (the source of the years convention).
dt = (FISCAL / "mexican_origin_population_total_2026_09_19/_cache/papers/dt2017_ilr.txt").read_text()
mex = [l for l in dt.splitlines() if l.strip().startswith("Mexico") and "0.76" in l]
check(len(mex) == 1 and re.findall(r"\d+\.\d+", mex[0]) == ["12.75", "0.76", "0.43", "13.07", "0.57", "0.90"],
      "DT 2017 Table 8 Mexico row: 12.75 0.76 0.43 13.07 0.57 0.90")
sel = pd.read_csv(FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm5_education_selectivity.csv")
gap = sel[sel.quantity == "education gap to be closed"].value.iloc[0]
check(abs(0.76 / gap - 0.7244) < 5e-4 and abs(0.57 / gap - 0.5433) < 5e-4, f"54.3%/72.4% = 0.57/0.76 over {gap} years")

# 7. ACS: shares and sample sizes are sane; the reference excludes Mexican ancestry by construction.
ag = pd.read_csv(D / "acs_ancestry_gaps.csv")
ac = pd.read_csv(D / "acs_ancestry_contrasts.csv")
sh = ac[ac.contrast.str.startswith("share not Mexican")].value
check(sh.between(0.03, 0.08).all(), f"ACS non-identifier share of Mexican-ancestry US-born {sh.min():.3f}-{sh.max():.3f}")
check((ag.n > 500).all(), f"ACS cells n >= 500 (min {ag.n.min()})")
audit = (D / "acs_ancestry_audit.txt").read_text()
check("sha256" in audit and "ADJINC" in audit, "ACS audit records source hash and ADJINC")

# 8. Co-resident adult non-identification rates sit near the children's 11.2% (G3) and a one-step G4 rate.
for label in ("CPS_ASEC_2022_2025", "CPS_ASEC_2022_2026"):
    c = pd.read_csv(D / f"cps_identity_contrasts_{label}.csv")
    g3 = c[(c.frame == "cores_one") & (c.reference == "white3plus") & (c.contrast == "G3anc: share not Mexican")].value
    check(g3.between(0.08, 0.16).all(), f"{label}: co-resident G3 adults not Mexican {g3.min():.3f}-{g3.max():.3f}")

if FAIL:
    print(f"FAIL: {len(FAIL)} check(s)")
    sys.exit(1)
print("PASS")
