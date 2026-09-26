"""Finite-removal responses r = [1 - (1 - s)^b] / s for the main case's elasticity-derived responses.

The main case uses cross-state elasticities b as the share of average cost that a removal saves.
For a power-law cost C(N) = aN^b, removing a share s saves r of the proportional cost, and only an
infinitesimal change gives r = b (immigration-service-scaling-test-2026-09-20.md). Writes
derived/r_values.json.
"""
import json
from pathlib import Path

FISCAL = Path(__file__).resolve().parents[1]
sc = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/scaling_check.json").read_text())
model = json.loads((FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())
pupils = json.loads((FISCAL / "school_cost_where_enrolled_2026_09_24/derived/account_embedded_price.json").read_text())
el = {e["function"]: e["elasticity"] for e in sc["elasticities"] if e["scope"] == "50 states"}
b_admin = el["Governmental administration (financial, judicial, buildings, other)"]
b_fin = el["Financial administration"]
b_all = el["Direct general expenditure"]
comp = sc["general_public_service_2024_bn"]
total = sum(comp.values())
sl = comp["state_local_executive_legislative"] + comp["state_local_tax_financial"] + comp["state_local_other"]
ft = comp["federal_tax_financial"]
gps = next(l for l in model["spending"]["lines"] if l["id"] == "general_public_services")


def r(b, s):
    return (1 - (1 - s) ** b) / s


# National target share as quoted in the service-scaling memo (40.896574m of 340.110988m), and the
# share the engine's population key actually charges on this line.
shares = {"national_memo": 40.896574 / 340.110988,
          "engine_population_key": gps["keys"]["population"]["personal"]["share"]}
out = {"b_admin": b_admin, "b_fin": b_fin, "b_all": b_all, "composition_bn": comp, "total_bn": total,
       "state_local_bn": sl, "federal_tax_bn": ft,
       "gg_low_b_unrounded": (sl * b_admin + ft * b_fin) / total, "gg_high_b": b_admin,
       "engine_gg_stored": [sc["composite_low"], sc["composite_high"]],
       "gps_line": {"national_bn": gps["national_bn"],
                    "target_full_response_bn": gps["keys"]["population"]["personal"]["target_bn"]}}
for name, s in shares.items():
    out[f"s_{name}"] = s
    # The federal executive and legislature stay fixed (response 0) at the low end.
    out[f"gg_low_r_{name}"] = (sl * r(b_admin, s) + ft * r(b_fin, s)) / total
    out[f"gg_high_r_{name}"] = r(b_admin, s)
    # Dataset-audit row 8 charges unallocable state-local spending at b_all instead of b_admin.
    out[f"row8_factor_{name}"] = (r(b_all, s) - r(b_admin, s)) / (b_all - b_admin)
s_pupil = pupils["target_pupils"] / pupils["national_pupils"]
out["s_pupil"] = s_pupil
out["pupils"] = {"target": pupils["target_pupils"], "national": pupils["national_pupils"]}
# CBO's 0.63 (growth) and 0.66 (decline) are 1 - 0.37 and 1 - 0.34 from a growth-rate regression:
# first-order elasticities (full_account_2026_09_20/service_response.py school_response_derivation).
for b in (0.63, 0.66):
    out[f"school_r_{b}"] = r(b, s_pupil)
    for sp in (0.16, 0.18):
        out[f"school_r_{b}_s{sp}"] = r(b, sp)
(Path(__file__).parent / "derived" / "r_values.json").write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: v for k, v in out.items() if not isinstance(v, dict)}, indent=1))
