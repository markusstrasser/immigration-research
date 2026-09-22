"""Independent re-derivation of the Option A headline rows (published case: PEARNVAL,
hs_or_less, s = .65, sigma = 2, adj = 1, eta = 0, retention = 1, owner = 0) from
derived/branch_composition.csv alone. Shares no code with nest_model.py or builder.py;
written by the parent session as the pre-commit check of the lane's core numbers.

Run from the repository root:
  UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with numpy --with pandas \
    python3 infra/immigration-fiscal/production_nativity_nest_2026_09_22/independent_check.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
GDP_BN, S, SIGMA, TAU = 29298.0, 0.65, 2.0, np.array([.384, .426])
EPS = [1.3, 3.0, 4.6, 5.0, 7.0, 8.7, 9.0, 17.9, 20.0, np.inf]


def main():
    bc = pd.read_csv(HERE / "derived" / "branch_composition.csv")
    bc = bc[(bc.proxy == "PEARNVAL") & (bc.split == "hs_or_less")]
    piv = bc.pivot(index="branch", columns="skill", values="earnings_estimate")
    cell = piv.sum(axis=0).to_numpy()
    a = cell / cell.sum()
    share = piv / cell
    nn, uus = share.loc["native_non_union"].to_numpy(), share.loc["union_us_born"].to_numpy()
    ofb, ug1 = share.loc["other_foreign_born"].to_numpy(), share.loc["union_mexico_born"].to_numpy()
    head = pd.read_csv(HERE / "derived" / "nest_headline.csv")
    head = head[(head.normalization == "gdp") & (head.nest_option == "A_by_nativity")].set_index("sigma_NI")
    rho = 1 - 1 / SIGMA
    worst = 0.0
    for eps in EPS:
        kappa = 1 - 1 / eps if np.isfinite(eps) else 1.0
        b = nn + uus
        n, f = 1 - uus / b, 1 - ug1 / (ofb + ug1)
        x = (b * n ** kappa + (1 - b) * f ** kappa) ** (1 / kappa)
        q = (a @ x ** rho) ** (1 / rho)
        w_n = q ** (1 - rho) * x ** (rho - kappa) * n ** (kappa - 1)
        w_f = q ** (1 - rho) * x ** (rho - kappa) * f ** (kappa - 1)
        lg_nn, lg_ofb = S * a * nn * (1 - w_n), S * a * ofb * (1 - w_f)
        mine = {
            "native_production_gain_bn": ((1 - TAU) * lg_nn).sum() * GDP_BN,
            "other_immigrant_production_gain_bn": ((1 - TAU) * lg_ofb).sum() * GDP_BN,
            "induced_current_receipts_bn": (TAU * (lg_nn + lg_ofb)).sum() * GDP_BN,
            "private_plus_receipts_bn": (lg_nn + lg_ofb).sum() * GDP_BN,
            "wage_pct_native_cell0": 100 * (w_n[0] - 1), "wage_pct_native_cell1": 100 * (w_n[1] - 1),
            "wage_pct_other_fb_cell0": 100 * (w_f[0] - 1), "wage_pct_other_fb_cell1": 100 * (w_f[1] - 1),
        }
        row = head.loc[eps]
        for key, value in mine.items():
            dev = abs(value - float(row[key]))
            worst = max(worst, dev)
            if dev > 1e-6:
                raise SystemExit(f"MISMATCH eps={eps} {key}: independent {value:.8f} vs lane {float(row[key]):.8f}")
        print(f"  ✓ eps={eps:>4}: P+F {mine['private_plus_receipts_bn']:9.4f}bn  natives {mine['native_production_gain_bn']:9.4f}  "
              f"other FB {mine['other_immigrant_production_gain_bn']:9.4f}  (8 quantities match the lane)")
    print(f"Independent re-derivation matches all Option A gdp headline rows; worst absolute deviation {worst:.2e} bn")


if __name__ == "__main__":
    main()
