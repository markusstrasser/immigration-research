"""Render P7 numbers from executed outputs; preserve the original dated result.

Native-First: text and CSV rendering only. No recomputation or source acquisition.
"""
import csv
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
SCRATCH = Path("/private/tmp/claude-501/-Users-alien-Projects-immigration-research/75b08f57-63cc-4e3d-96dc-60050327b5c1/scratchpad/p7/lanes")
MARKER = "## Historical September 28 result (superseded for the live crime rows)"


def read(name):
    with (HERE / "derived" / name).open() as handle:
        return list(csv.DictReader(handle))


def main():
    changes = read("p7_changes.csv")
    final = next(r for r in changes if r["scenario"] == "stacked_dot")
    standards = json.loads((FISCAL / "crime_victim_cost_2026_09_23/derived/vsl_standard.json").read_text())
    payload = json.loads((HERE / "derived/p7_payload.json").read_text())
    body = [f"**Verdict:** P7's corrected crime rule gives **${float(final['pairing_low_bn']):.2f}–{float(final['pairing_high_bn']):.2f}bn/year** "
            f"at the current v7 personal endpoints: **+${float(final['delta_low_bn']):.3f} / +${float(final['delta_high_bn']):.3f}bn**, "
            "below the review's $5bn bar at both ends under the stated recipient-exposure assumption. The arrest-footed high alternative clears it. "
            "These are modeled fiscal-plus-social removals for other US residents, 2024 dollars; the fiscal case remains frozen. "
            "[CALCULATION: `p7_crime.py` → `derived/p7_changes.csv`; `real_costs_totals.py --case oct14`] [ASSUMPTION]",
            "", "## Per-fix changes and totals", "",
            "Each isolated row changes the named rule from the executed pre-P7 control; stacked rows combine them. Security's isolated row also removes its forward spending from the fear budget, an inseparable overlap correction. "
            "Victims and fear are always paired on the selected incident/unit-price arm. The low fiscal footing is the existing raw-coded justice reading; the high is the existing custody reading, at personal specifications 16 / 11. "
            "No new pollution, crash or benefit producer rows join. [DATA: `inputs/baseline_totals_oct14.*`; `derived/payment_keys.json`]",
            "", "| Rule | Δ union social, low/high | Δ lineage pairing, low/high | Lineage pairing | Lineage full span* | $5bn bar |",
            "|---|---:|---:|---:|---:|---|"]
    for r in changes:
        body.append(f"| `{r['scenario']}` | {float(r['delta_union_low_bn']):+.3f} / {float(r['delta_union_high_bn']):+.3f} | "
                    f"{float(r['delta_low_bn']):+.3f} / {float(r['delta_high_bn']):+.3f} | "
                    f"{float(r['pairing_low_bn']):.3f} / {float(r['pairing_high_bn']):.3f} | "
                    f"{float(r['full_span_low_bn']):.3f} / {float(r['full_span_high_bn']):.3f} | {r['review_bar_5bn']} |")
    body += ["", "[CALCULATION: `derived/p7_changes.csv`] All table values are $bn/year. Union changes are the 39.71M union's social rows; lineage changes include the 3.04M added people on the existing justice sender keys and their own consumption payment key. "
             "The `union_social_only_*` CSV columns hold the full lineage fiscal row fixed and include only the union's social sender rows; they are **not a union-only fiscal counterfactual**. "
             "The complete-account union-only removal changes service responses and is not substituted here.",
             "", "*Full spans are model envelopes, not confidence intervals. The first gate reproduces the published-union pre-P7 span byte-precision values; the displayed baseline then puts social rows on row4 and adds D. "
             "PM/crash endpoints use their already-executed priced-count grids. Other noncrime span ends retain their existing central population factors [APPROXIMATION], rather than a newly executed full nonlinear grid. "
             "Every noncrime source/union row is held unchanged across the fixes. The old printed span and this population-consistent baseline are distinct objects. "
             "The arrest high beside value changes the central arrest footing; it does not invent an arrest uncertainty envelope.",
             "", "## Security, fear and the beneficiary boundary", "",
             "`response()` is the one rule: household security attributable to offending against outsiders has no population subtraction. Businesses/nonprofits pass security costs through to purchasers; the net subtracts the group's payment toward security against other offenders. "
             "Government customer receipts remain in national closure but are excluded from the private response [ASSUMPTION: exact fiscal overlap not identified]. The Census customer split is measured; crime-driven shares, source-bridging the EC payer mix to SAS revenue, nonprofit pass-through, in-house coverage and equipment payer mix remain assumptions. "
             "[SOURCE: Census 2022 `ecnclcust` and `ecnnapcsind`, URLs/pins in `inputs/security_pins.json`; DATA: `derived/security_inputs.json`; see `security-inputs.md`.]",
             "", "The current business payment key is extracted from v7's personal general-sales-tax cells, with the **on-case moved consumption lineage share** taking precedence over the old item-base share. "
             "An offender-footing change cannot change that payment share. Security and fear are evaluated again for U+D with the lineage's payment share and its separate justice sender multiplier; their net is not multiplied by a single key. "
             "[CALCULATION: `payment_keys.cjs`; `derived/payment_keys.json`; `derived/p7_payload.json` `response_parameters`.]",
             "", "Fear uses WTP minus the active victim harm on the same outsider counts. Its residual removes **positive forward security spending before phi**, floors at zero, and never removes the reverse payment credit as if it were spending. "
             "This deliberately prevents security from being counted a second time inside fear; the overlap premise is conservative, not empirically identified. The original equal-population security and fixed-Miller fear figures are preserved beside in `inputs/baseline_social_items.csv` and historical `derived/items.csv`, never adopted as the live P7 crime rows. "
             "[CALCULATION: `crime_responses()`; `derived/p7_security_spending.csv`; ASSUMPTION.]",
             "", "U→D and D→D harms **and benefits** leave the outsider side. The central assumes the added people have average former-outsider exposure in each recipient age range; school uses their measured age mix with uniform within-bin interpolation. "
             "It is not an observed geographic or victim-level allocation. Zero and twice the average exposure are reported as sensitivity endpoints, not statistical bounds; they cross the $5bn review threshold on the high side. "
             "[DATA: frozen v7 lineage age mix, `frame_counts.csv`; CALCULATION: `lineage_recipient_shares()`, `derived/p7_changes.csv`; ASSUMPTION.]",
             "", "## Common mortality standard and matched victim/fear rows", "",
             f"Setting **`vsl_standard`**: `dot_uniform` = **${standards['dot_vsl_2024usd']/1e6:.1f}m (2024 dollars)**. "
             f"`dot_life_years` uses the same base at reference age **{standards['reference_age']}**, **{standards['reference_remaining_years']:.6f}** undiscounted remaining life-years "
             f"on the common NVSS 2024 period table; the 3% sensitivity base is **{standards['reference_remaining_years_r3']:.6f}** years. Age calibration is an assumption. "
             "Shared API and values: `../crime_victim_cost_2026_09_23/vsl_standard.py` and `derived/vsl_standard.json` in that lane. "
             "[SOURCE: pinned DOT primary table and NVSS workbook, crime lane `inputs/pins.json`.]",
             "", "The pollution worker can read the same setting/API. A common life-year total needs pollution's mortality age mix or an explicit remaining-year range; this lane does not invent it. "
             "The life-year pairing/span rows hold pollution/crashes at their existing DOT valuation and are explicitly **crime-only sensitivities, not uniform life-year totals**. "
             "The live P7 payload uses `dot_uniform`, matching existing PM2.5. [GAP: pollution age-specific mortality; ownership boundary.]",
             "", "| Standard / end | Sender population and recipient boundary | Victims | Fear after security overlap | Victims + fear | Security |",
             "|---|---|---:|---:|---:|---:|"]
    for r in read("p7_joint_valuation.csv"):
        body.append(f"| `{r['vsl_standard']}` / {r['end']} | {r['population']} | {float(r['victims_bn']):.3f} | {float(r['fear_bn']):.3f} | {float(r['victims_plus_fear_bn']):.3f} | {float(r['security_bn']):.3f} |")
    body += ["", "[CALCULATION: `derived/p7_joint_valuation.csv`] Mortality earnings/QoL are replaced, not added on top of DOT. Crime ages come from primary SHR 2024 known-Hispanic-first-offender victims, with explicit selection/unknown-age sensitivities; see `../crime_victim_cost_2026_09_23/p7-victim-result.md`.",
             "", "## Contract, gates and uncertainty", "",
             "The consumer registry declares comparator, beneficiary population, valuation basis and overlap set for all 15 adopted social rows. Unknown sources/items, incompatible producer declarations, equal-population security, missing/stale payload sources and mismatched item/payload values stop before outputs are written. "
             "A historical mode exists solely to reconstruct the executed pre-P7 control; the live P7 rows are validated separately. The regression injects equal-population security through the actual consumer and stops it. "
             "[CALCULATION: `../sept24_propagation_2026_09_24/real_costs_totals.py`; `test_p7_contract.py`.]",
             "", "National security totals close within 1e-6bn; customer fractions within 1e-12. Victim mixed-attribution changes conserve national victim-row incidents and matched cost/count/unit products. "
             "Baseline pairing and full-span positive controls pass; every noncrime union span row is byte-equivalent across scenarios. The output comparison permits only the priced pairing, full span and lineage-detail corrections. Old fear/security/aggregate item controls are explicitly relabeled historical, and twelve endpoint-specific fear/security rows are appended; every other exported row stays byte-identical. "
             "[CALCULATION: `derived/p7_gates.csv`; primary parser checks; test suites.]",
             "", "No joint live-key replicate SE is identified. Available partial sampling information is reported separately:",
             "", "| Component / footing | Population and conditioning | SE, $bn |",
             "|---|---|---:|"]
    for r in read("p7_sampling.csv"):
        body.append(f"| {r['component']} / {r['footing']} | {r['population']} | {float(r['se_bn']):.6f} |")
    body += ["", "[CALCULATION: `derived/p7_sampling.csv`] Security/fear SE is exact affine propagation of the existing payment key's 160-replicate CPS SDR SE on the **published union**, other inputs held; it is not the row4/lineage/joint crime SE. "
             "Victim SE is the existing understated independent-cell NCVS generalized-variance delta method on row4, not a replicate SE. Neither covers uncertainty in phi, offending measurement, demographic transport, mortality age selection, Census customer mix or the beneficiary boundary.",
             "", "## Report-only checks and review", "",
             "`report_checks.md` reports geography, state custody reallocation, ICE overlap and the arrest high. Geography already enters one NIBRS transfer and is not an omitted new adjustment; transporting the NCVS mixed-group theta is explicitly a sensitivity. "
             "State-by-state custody reassignment is below $5bn. Contract-only annual ICE/ACS overlap is unidentified; the reported stock stresses are not matched survey corrections. "
             "The high victim footing uses an ACS institutional multiplier, which cannot be called observed ordinary offending; the arrest alternative remains a charging proxy. "
             "[CALCULATION: `derived/report_checks_*`; SOURCE: custody/crime measurement rule and reused detention audit.]",
             "", "`p7-code-review.md` records the independent source review and corrected findings: all-row contract coverage, principal moved payment key, shared API payment independence, and direct lineage security/fear evaluation. "
             "LLM instrument limitations remain: response/transport and welfare assumptions are labeled; modeled attribution is not a measured causal effect.",
             "", "## Reproduction and fixed scope", "", "```sh",
             "node infra/immigration-fiscal/social_costs_unpriced_2026_09_28/payment_keys.cjs",
             "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/security_inputs.py --check",
             "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/p7_crime.py",
             "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/sept24_propagation_2026_09_24/real_costs_totals.py --case oct14",
             "uv run --no-project python3 infra/immigration-fiscal/social_costs_unpriced_2026_09_28/render_p7.py",
             "```", "", "The final validation receipts and every changed path are appended in the parent result file. Historical source outputs remain records; no frozen-case, research-document or independent producer edits. "
             "`social_spans_priced_count_2026_09_29` is read-only: it contains PM/crash grids, no crime-driven security producer; its original priced grid is pinned here. "
             "No git metadata writes. This result is ready for the parent's adoption/integration decision."]
    receipt = json.loads((HERE / "inputs/validation_receipt.json").read_text())
    body += ["", "## Completed validation log", "", f"{receipt['closed_at']}: {receipt['tests']}. "
             f"Social producer {receipt['social_rerun']}; totals {receipt['totals_rerun']}; "
             f"victims {receipt['victim_rerun']}; population {receipt['population_rerun']}. "
             f"Warm P7 computation {receipt['p7_warm_seconds']:.3f}s / {receipt['p7_peak_rss_bytes']/1e6:.1f}MB peak RSS; "
             f"largest victim producer {receipt['victim_peak_rss_bytes']/1e9:.3f}GB, below the lane limit. "
             f"{receipt['measurement']}. Source/consumer regressions and independent review pass. "
             "[CALCULATION: `inputs/validation_receipt.json`; rerun logs in /private/tmp.]",
             "", "Every changed path is listed in `social-crime-changed-paths.txt` beside the parent result file. Raw inputs/caches are listed separately from git-visible source/output changes; runtime caches are not commit paths."]
    text = "\n".join(body) + "\n"
    old = (HERE / "RESULT.md").read_text()
    if MARKER in old:
        old = old.split(MARKER, 1)[1].lstrip("\n")
    (HERE / "RESULT.md").write_text(text + "\n" + MARKER + "\n\n" + old)
    (SCRATCH / "social-crime-result.md").write_text(text)
    root = FISCAL.parent.parent
    scopes = [FISCAL / n for n in ("social_costs_unpriced_2026_09_28", "crime_victim_cost_2026_09_23",
                                  "population_basis_2026_09_29", "sept24_propagation_2026_09_24")]
    status = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=all", "--", *map(str,scopes)],
                            check=True, capture_output=True, text=True).stdout
    changed = {root / line[3:] for line in status.splitlines()}
    changed |= set((HERE / "inputs").glob("security*")) | set((HERE / "_cache").glob("security*"))
    changed |= set((HERE / "inputs").glob("baseline*"))
    changed |= set((FISCAL / "crime_victim_cost_2026_09_23/inputs").glob("*"))
    manifest = SCRATCH / "social-crime-changed-paths.txt"
    changed |= {manifest, SCRATCH / "social-crime-result.md"}
    # Interpreter cache changes are incidental to verification. Identify their
    # actual write window from the parent's dated brief, rather than listing old
    # caches as new work. Temporary rerun backup trees are tool-owned snapshots.
    after = (SCRATCH / "brief_social_crime.md").stat().st_mtime
    runtime = {p for scope in scopes for p in (scope / "__pycache__").glob("*") if p.stat().st_mtime >= after}
    runtime |= {p for p in (root / ".pytest_cache").rglob("*") if p.is_file() and p.stat().st_mtime >= after}
    logs = {Path("/private/tmp") / n for n in ("p7-social-baseline.log", "p7-social-live.log", "p7-crime-final.log",
            "p7-social-rerun.log", "p7-totals-rerun.log", "p7-victim-arms.log")}
    manifest.write_text("Every source, input, output and result path changed (absolute paths):\n" +
                        "\n".join(str(p) for p in sorted(changed) if p.is_file()) +
                        "\n\nIncidental interpreter caches and diagnostic logs (not commit paths):\n" +
                        "\n".join(str(p) for p in sorted(runtime | logs) if p.is_file()) +
                        "\n\nTool-owned rerun backup trees are verification snapshots, excluded from source/output inventory.\n")


if __name__ == "__main__":
    main()
