"""Render the adopted v9 headline from computed tables; retain dated history."""
import gzip
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived/oct16"
MARKER = "## v9 case (oct16)"


def main():
    with gzip.open(OUT / "p7_gates.json.gz", "rt") as stream:
        gates = json.load(stream)
    if not gates or not all(v["passed"] for v in gates.values()):
        raise SystemExit("[BLOCKED] v9 document requires all computation gates")
    shares = pd.read_csv(OUT / "p7_net_shares.csv")
    selected = shares[(shares.frame == "stationary") & (shares.sharing == "pooled") &
        (shares.level == "central") & (shares.arm == "recommended") & (shares.epsilon == "infinite")].set_index("financing")
    if set(selected.index) != {"a", "b", "c"}:
        raise SystemExit("[BLOCKED] headline requires one central stationary pooled row per financing rule")
    audit = json.loads((OUT / "p7_inputs.json").read_text())
    headline = ("**Verdict:** On adopted v9, stationary financing, the paired social stack and household pooling, "
        + " / ".join(f"{100*selected.loc[r, 'winners_share']:.4f}%" for r in "abc")
        + f" of other residents are ahead under rules a/b/c; their central annual net is ${selected.loc['a', 'total_bn']:.6f}bn. "
        + "Cohort financing is beside. [MODEL / FRAMING-SENSITIVE; CALCULATION: derived/oct16/p7_net_shares.csv]")
    path = HERE / "RESULT.md"
    old = path.read_text()
    history = old.split("\n", 1)[1]
    if MARKER in history:
        history = history.split(MARKER)[0].rstrip()+"\n"
    section = [MARKER, "", headline, "",
        f"The complete calibrated lineage contains {audit['population']['with_coverage']:.8f} people; "
        f"{audit['population']['without_coverage']:.8f} are placed on observed/proxy records and "
        f"{audit['population']['coverage']:.8f} remain unlocated. Native-minor calibration changes only observed member weights; "
        "the original unreported descendants retain their measured age proxy. Coverage is excluded from payer households. "
        "[DATA: derived/oct16/p7_inputs.json population; main-case meta.population_v9]", "",
        "The full set/cash typed source ledger carries selected military, retirement administration, college, joint count/tenure, "
        "taxable-basket, common capital-rate and health-key components. Capital is an imputed resource cost, outside borrowing. "
        "Item19/W09 remain beside. Per-item isolated and leave-one-out ablations are not computed for v9: they need a per-item "
        "effects export for items 13-21, which does not exist. Financing and attribution scenarios are computed on oct16. "
        "[DATA: derived/oct16/p8_channel_ledger.csv; p7_trust_inputs.json; p7_net_shares.csv]", "",
        "Reporter/count combined production is retained as an explicit unlocated carrier. The distribution source consumer "
        "uses assumed generation P/F shares for the same carriers; their declared difference is reconciled at1e-9 before "
        "pricing. No private-income split is inferred here. [CALCULATION: fiscal_one_definition; fiscal_specs.csv; p7_gates.json.gz]", "",
        "Upstream oct16 consumers are explicit SHA256 worktree snapshots because this worker cannot commit. Every used source hash "
        "is checked before and after pricing; changes stop the run. Allocation keys and household pooling are modeled incidence, "
        "not measured winners. [DATA: inputs/p9_pins_oct16.json; derived/oct16/p7_inputs.json source_pins]", "",
        "Run `sh infra/immigration-fiscal/winners_losers_2026_09_24/run_all.sh`. "
        "Explicit acquisition after reviewing upstream changes: `uv run --no-project python3 "
        "infra/immigration-fiscal/winners_losers_2026_09_24/p8_phase_b.py --prepare-pins` "
        "(use --revise-pins for an existing snapshot). Normal pricing never changes source pins.", ""]
    path.write_text(headline+"\n"+history.rstrip()+"\n\n"+"\n".join(section))
    print("[document] oct16 headline rendered; prior case sections retained")


if __name__ == "__main__":
    main()
