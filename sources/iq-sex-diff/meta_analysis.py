"""
Meta-analysis of sex differences in cognitive subtests across WAIS studies.
Uses published effect sizes (Cohen's d) from:
- van der Sluis et al. 2006 (Dutch WAIS-III, N=522)
- Pezzuti et al. 2020 (Italian WAIS-IV, N=2175; Italian WAIS-R, N=2798)

Convention: negative d = male advantage, positive d = female advantage
"""

import json
import math

# ── Study data ──────────────────────────────────────────────────────────────

studies = {
    "dutch_wais3": {
        "citation": "van der Sluis et al. 2006",
        "lead_gender": "F",
        "country": "Netherlands",
        "test": "WAIS-III",
        "n_male": 228,
        "n_female": 294,
        "subtests": {
            # d convention: positive = female advantage
            "Information":      {"d": -0.66, "type": "crystallized_knowledge"},
            "Similarities":     {"d": -0.18, "type": "verbal_reasoning"},
            "Vocabulary":       {"d": -0.07, "type": "verbal_memory"},
            "Arithmetic":       {"d": -0.42, "type": "numerical_reasoning"},
            "Letter-Number":    {"d": -0.10, "type": "working_memory"},
            "Block Design":     {"d": -0.26, "type": "spatial"},
            "Matrix Reasoning": {"d": -0.20, "type": "fluid_reasoning"},
            "Picture Completion":{"d": -0.23, "type": "visual_perception"},
            "Digit-Symbol":     {"d":  0.71, "type": "processing_speed"},
            "Copying":          {"d": -0.19, "type": "processing_speed"},
        },
        "composites": {
            "Verbal IQ":      {"d": -0.44},
            "Performance IQ": {"d":  0.07},
            "Full Scale IQ":  {"d": -0.24},
        }
    },
    "italian_wais4": {
        "citation": "Pezzuti et al. 2020",
        "lead_gender": "F",
        "country": "Italy",
        "test": "WAIS-IV",
        "n_male": 1087,  # approx half of 2175
        "n_female": 1088,
        "subtests": {
            "Information":      {"d": -0.29, "type": "crystallized_knowledge"},
            "Similarities":     {"d":  0.03, "type": "verbal_reasoning"},
            "Vocabulary":       {"d":  0.04, "type": "verbal_memory"},
            "Arithmetic":       {"d": -0.47, "type": "numerical_reasoning"},
            "Digit Span":       {"d": -0.18, "type": "working_memory"},
            "Letter-Number":    {"d": -0.22, "type": "working_memory"},
            "Block Design":     {"d": -0.29, "type": "spatial"},
            "Matrix Reasoning": {"d": -0.19, "type": "fluid_reasoning"},
            "Visual Puzzles":   {"d": -0.30, "type": "spatial"},
            "Figure Weights":   {"d": -0.32, "type": "fluid_reasoning"},
            "Comprehension":    {"d": -0.14, "type": "verbal_reasoning"},
            "Symbol Search":    {"d": -0.09, "type": "processing_speed"},
            "Coding":           {"d":  0.02, "type": "processing_speed"},
            "Cancellation":     {"d":  0.01, "type": "processing_speed"},
            "Picture Completion":{"d": -0.14, "type": "visual_perception"},
        },
        "composites": {
            "Verbal Comprehension": {"d": -0.08},
            "Perceptual Reasoning": {"d": -0.31},
            "Working Memory":       {"d": -0.37},
            "Processing Speed":     {"d":  0.04},
            "Full Scale IQ":        {"d": -0.24},
        }
    },
    "italian_waisr": {
        "citation": "Pezzuti et al. 2020 (WAIS-R)",
        "lead_gender": "F",
        "country": "Italy",
        "test": "WAIS-R",
        "n_male": 1399,
        "n_female": 1399,
        "subtests": {
            "Information":      {"d": -0.39, "type": "crystallized_knowledge"},
            "Similarities":     {"d":  0.01, "type": "verbal_reasoning"},
            "Vocabulary":       {"d": -0.06, "type": "verbal_memory"},
            "Arithmetic":       {"d": -0.57, "type": "numerical_reasoning"},
            "Digit Span":       {"d": -0.28, "type": "working_memory"},
            "Comprehension":    {"d": -0.21, "type": "verbal_reasoning"},
            "Block Design":     {"d": -0.40, "type": "spatial"},
            "Picture Completion":{"d": -0.31, "type": "visual_perception"},
            "Picture Arrangement":{"d": -0.22, "type": "visual_perception"},
            "Object Assembly":  {"d": -0.19, "type": "spatial"},
            "Coding":           {"d":  0.03, "type": "processing_speed"},
        },
        "composites": {
            "Verbal IQ":      {"d": -0.30},
            "Performance IQ": {"d": -0.25},
            "Full Scale IQ":  {"d": -0.32},
        }
    },
}


# ── Fixed-effects meta-analysis ─────────────────────────────────────────────

def variance_d(d, n1, n2):
    """Variance of Cohen's d (Hedges & Olkin approximation)."""
    return (n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2))


def meta_analyze(effects):
    """
    Fixed-effects inverse-variance weighted meta-analysis.
    effects: list of (d, var_d) tuples.
    Returns: (pooled_d, se, 95% CI lower, 95% CI upper, Q statistic)
    """
    weights = [1.0 / v for _, v in effects]
    total_w = sum(weights)
    pooled = sum(w * d for (d, _), w in zip(effects, weights)) / total_w
    se = math.sqrt(1.0 / total_w)
    ci_lo = pooled - 1.96 * se
    ci_hi = pooled + 1.96 * se
    # Cochran's Q for heterogeneity
    Q = sum(w * (d - pooled)**2 for (d, _), w in zip(effects, weights))
    return pooled, se, ci_lo, ci_hi, Q


# ── Aggregate by cognitive domain ───────────────────────────────────────────

domain_effects = {}  # domain -> list of (d, var_d, study, subtest)

for study_key, study in studies.items():
    n1, n2 = study["n_male"], study["n_female"]
    for subtest, info in study["subtests"].items():
        d = info["d"]
        domain = info["type"]
        v = variance_d(d, n1, n2)
        domain_effects.setdefault(domain, []).append(
            (d, v, study["citation"], subtest)
        )

print("=" * 80)
print("META-ANALYSIS: Sex Differences by Cognitive Domain")
print("Convention: negative = male advantage, positive = female advantage")
print("=" * 80)
print()

domain_order = [
    "verbal_memory", "verbal_reasoning", "crystallized_knowledge",
    "numerical_reasoning", "working_memory", "spatial",
    "fluid_reasoning", "visual_perception", "processing_speed"
]

domain_labels = {
    "verbal_memory": "Verbal Memory (Vocabulary)",
    "verbal_reasoning": "Verbal Reasoning (Similarities, Comprehension)",
    "crystallized_knowledge": "Crystallized Knowledge (Information)",
    "numerical_reasoning": "Numerical Reasoning (Arithmetic)",
    "working_memory": "Working Memory (Digit Span, Letter-Number)",
    "spatial": "Spatial (Block Design, Visual Puzzles, Object Assembly)",
    "fluid_reasoning": "Fluid Reasoning (Matrix Reasoning, Figure Weights)",
    "visual_perception": "Visual Perception (Picture Completion/Arrangement)",
    "processing_speed": "Processing Speed (Coding, Digit-Symbol, etc.)",
}

results = []
for domain in domain_order:
    effects = [(d, v) for d, v, _, _ in domain_effects[domain]]
    pooled, se, ci_lo, ci_hi, Q = meta_analyze(effects)
    k = len(effects)
    iq_pts = pooled * 15  # convert d to IQ points

    label = domain_labels[domain]
    direction = "MALE" if pooled < -0.05 else ("FEMALE" if pooled > 0.05 else "NONE")

    results.append({
        "domain": label,
        "k": k,
        "pooled_d": round(pooled, 3),
        "se": round(se, 3),
        "ci": f"[{ci_lo:.2f}, {ci_hi:.2f}]",
        "iq_pts": round(iq_pts, 1),
        "Q": round(Q, 2),
        "direction": direction,
    })

    print(f"  {label}")
    print(f"    k={k}  pooled d = {pooled:+.3f}  SE = {se:.3f}  95% CI {ci_lo:+.2f} to {ci_hi:+.2f}")
    print(f"    IQ points: {iq_pts:+.1f}  Direction: {direction}  Q = {Q:.2f}")

    # Show individual studies
    for d, v, study, subtest in domain_effects[domain]:
        print(f"      {study}: {subtest} d = {d:+.2f}")
    print()

# ── Composite FSIQ ──────────────────────────────────────────────────────────

print("=" * 80)
print("FULL SCALE IQ — Meta-analysis across studies")
print("=" * 80)
print()

fsiq_effects = []
for study_key, study in studies.items():
    d = study["composites"]["Full Scale IQ"]["d"]
    v = variance_d(d, study["n_male"], study["n_female"])
    fsiq_effects.append((d, v, study["citation"]))
    print(f"  {study['citation']}: FSIQ d = {d:+.2f} ({d*15:+.1f} IQ pts)")

pooled, se, ci_lo, ci_hi, Q = meta_analyze([(d, v) for d, v, _ in fsiq_effects])
print()
print(f"  POOLED: d = {pooled:+.3f}  95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}]")
print(f"  IQ points: {pooled*15:+.1f}  [{ci_lo*15:+.1f}, {ci_hi*15:+.1f}]")
print(f"  Heterogeneity Q = {Q:.2f} (df={len(fsiq_effects)-1})")
print()

# ── Summary table ───────────────────────────────────────────────────────────

print("=" * 80)
print("SUMMARY TABLE")
print("=" * 80)
print()
print(f"{'Domain':<50} {'k':>3} {'d':>7} {'IQ pts':>8} {'95% CI':>16} {'Dir':>7}")
print("-" * 95)
for r in results:
    print(f"{r['domain']:<50} {r['k']:>3} {r['pooled_d']:>+7.3f} {r['iq_pts']:>+8.1f} {r['ci']:>16} {r['direction']:>7}")
print("-" * 95)
print(f"{'Full Scale IQ (composite)':<50} {len(fsiq_effects):>3} {pooled:>+7.3f} {pooled*15:>+8.1f} {'[{:.2f}, {:.2f}]'.format(ci_lo, ci_hi):>16} {'MALE':>7}")
print()
print("Negative d / IQ = male advantage. Positive = female advantage.")
print()

# ── The key question: what if we weight subtests equally? ───────────────────

print("=" * 80)
print("THOUGHT EXPERIMENT: Equal-weight composite across all domains")
print("=" * 80)
print()

all_effects = []
for domain in domain_order:
    for d, v, study, subtest in domain_effects[domain]:
        all_effects.append((d, v))

grand_pooled, grand_se, grand_lo, grand_hi, grand_Q = meta_analyze(all_effects)
print(f"  All {len(all_effects)} subtest effects pooled:")
print(f"  d = {grand_pooled:+.3f}  95% CI [{grand_lo:+.2f}, {grand_hi:+.2f}]")
print(f"  IQ points: {grand_pooled*15:+.1f}  [{grand_lo*15:+.1f}, {grand_hi*15:+.1f}]")
print()

# Without processing speed (the contested domain)
no_speed = [(d, v) for d, v, s, sub in
            [(d, v, study, subtest) for domain in domain_order if domain != "processing_speed"
             for d, v, study, subtest in domain_effects[domain]]]
ns_pooled, ns_se, ns_lo, ns_hi, ns_Q = meta_analyze(no_speed)
print(f"  Without processing speed ({len(no_speed)} effects):")
print(f"  d = {ns_pooled:+.3f}  95% CI [{ns_lo:+.2f}, {ns_hi:+.2f}]")
print(f"  IQ points: {ns_pooled*15:+.1f}  [{ns_lo*15:+.1f}, {ns_hi*15:+.1f}]")
print()

# Without Information (biased via DIF in both studies)
no_info = [(d, v) for d, v, s, sub in
           [(d, v, study, subtest) for domain in domain_order
            for d, v, study, subtest in domain_effects[domain]
            if subtest != "Information"]]
ni_pooled, ni_se, ni_lo, ni_hi, ni_Q = meta_analyze(no_info)
print(f"  Without Information subtest ({len(no_info)} effects):")
print(f"  d = {ni_pooled:+.3f}  95% CI [{ni_lo:+.2f}, {ni_hi:+.2f}]")
print(f"  IQ points: {ni_pooled*15:+.1f}  [{ni_lo*15:+.1f}, {ni_hi*15:+.1f}]")
print()

# Without Information AND processing speed
no_both = [(d, v) for d, v, s, sub in
           [(d, v, study, subtest) for domain in domain_order
            if domain != "processing_speed"
            for d, v, study, subtest in domain_effects[domain]
            if subtest != "Information"]]
nb_pooled, nb_se, nb_lo, nb_hi, nb_Q = meta_analyze(no_both)
print(f"  Without Information AND processing speed ({len(no_both)} effects):")
print(f"  d = {nb_pooled:+.3f}  95% CI [{nb_lo:+.2f}, {nb_hi:+.2f}]")
print(f"  IQ points: {nb_pooled*15:+.1f}  [{nb_lo*15:+.1f}, {nb_hi*15:+.1f}]")
