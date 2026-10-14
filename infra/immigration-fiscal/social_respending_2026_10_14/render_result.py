"""Re-derive round-2 findings while preserving the earlier research record."""
import json
from pathlib import Path

from respending import read_csv, verify_bundle, hard_gate, verify_pins
from stack import one

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
verify_pins()
stack_generation = verify_bundle("stack")
respending_generation = verify_bundle("respending")
stacks = read_csv(D / "conditional_stacks.csv")
integration = json.loads((D / "integration.json").read_text())


def pair(crash_arm, valuation="uniform", rate="0"):
    values = []
    for end in ("low", "high"):
        row = one(stacks,end=end,spending_denominator="PCE",mortality_valuation=valuation,
                  real_discount_rate=rate,crash_arm=crash_arm,volunteering_proxy="primary_food",
                  displacement="0.0",market_demand_arm="False",pm_crash_recipient_boundary="identified_union")
        values.append(f"{float(row['stack_pairing_bn']):.3f}")
    return " / ".join(values)


path = HERE / "RESULT.md"
marker = "## Round-2 corrections"
prior = path.read_text()
old, _, previous_section = prior.partition(marker)
execution_log = ""
if "### Execution log" in previous_section:
    execution_log = "\n\n### Execution log" + previous_section.split("### Execution log",1)[1]
section = [
    marker, "",
    "2026-10-15 JST. Earlier sections/logs above remain the round-1 record. Source sender/receiver quantities and H retain the frozen v7 producer frame; road capacity uses the native oct15 key. The Sept24 consumer applies the oct15 resource account and complete denominator. [CALCULATION: producer tables; Sept24 consumer]",
    "",
    "- Denominator: CE central → PCE central. CE is a labelled units sensitivity. Both standalone stack execution and consumers require the complete source-pin registry and matching funding/denominator accounting bases.",
    f"- Crash rule: all-density → multivehicle-only. On PCE, uniform DOT VSL, zero incoming displacement and the identified-union PM/crash receiver boundary: {pair('all_density')} → {pair('multivehicle_only')}bn. These named producer scenarios retain their declared frozen social quantities; the native oct15 road capacity and all-channel crime valuation are applied.",
    "- PM mortality: total plume deaths are reweighted for receptor mortality before membership shares. Nonfatal illness retains exposure dollars. The source lane's dated correction records the before/after deaths and harm; national source attribution and local reference-mixture assumptions remain explicit.",
    "- One mortality basis: crime, PM and crashes use uniform DOT VSL centrally. Life-year readings apply to all three together and preserve nonmortality dollars. The PM-only life-year pseudo-pairings are removed. The registry fails on a missing channel, mixed basis or discount rate.",
    f"- All-channel life-year producer scenarios beside: {pair('multivehicle_only','VSLY','0')}bn at 0%, {pair('multivehicle_only','VSLY','0.03')}bn at 3%. These are alternatives to the uniform scenario, never added to it.",
    "- Re-spending funding: the consumer moves frozen v7 H to v8 resource arithmetic under an explicit current-resource treatment of unclassified cash amounts. Completion production lacks separate P/F. Resource alternatives add capital and subtract signed private production income plus city earnings/taxes, deferring promises or adding the set-minus-cash bridge as wealth-equivalent promises. Fixed labour supply makes native private WTP equal included after-tax market income; other timing/spendability assumptions remain conditional.",
    "- One joint pairing: the consumer joins crime, PM, crash capacity, congestion and volunteering replacements, with accounting interaction closure ≤1e-9bn and with/without round-1 readings. The producer's pre-round-1 crime replacement and the consumer's already-corrected P7 delta are separate fields, preventing double counting. Behavioural cross-channel interactions are unmeasured.",
    "- Publication: outputs are staged before rename; readers verify generation hash receipts before and after loading. Interrupted multi-file publication fails closed. Scientific gates raise explicitly under python -O.",
    "",
    "Below-bar log only: CPI-only fear WTP versus income-updated VSL; shared descendant exposure; within-age mortality; PM-only re-spending; government mirror both ends and legacy .55; outsider source–receptor bound; saving/propensities; SO2 cap offset. No extra central adjustment is made. [DATA: round-2 review packets]",
    "",
    f"[CALCULATION: derived/integration.json; {integration['counts']['conditional_stack_rows']} conditional rows; derived/conditional_stacks.csv. Reproduce with the commands above and this lane's full pytest suite.]",
]
hard_gate(stack_generation == verify_bundle("stack"), "stable stack generation through rendering")
hard_gate(respending_generation == verify_bundle("respending"), "stable spending generation through rendering")
path.write_text(old.rstrip()+"\n\n"+"\n".join(section)+execution_log.rstrip()+"\n")
