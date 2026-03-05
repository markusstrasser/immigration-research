"""
Meta-analysis of sex differences in cognitive subtests.

Datasets:
- van der Sluis et al. 2006 (Dutch WAIS-III, N=522)
- Pezzuti et al. 2020 (Italian WAIS-IV, N=2175; Italian WAIS-R, N=2798)
- Deary et al. 2007 (US ASVAB/NLSY79, N=2584 sibling pairs)

Convention: negative d = male advantage, positive d = female advantage

Statistical fixes (v2):
- Random-effects (DerSimonian-Laird) instead of fixed-effects
- ASVAB data adds a non-WAIS battery from a different country
- Known limitation: subtests within a study are correlated (r≈0.3-0.7).
  We flag this but don't apply RVE (would need R/metafor).
"""

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
            "Information":       {"d": -0.66, "type": "crystallized_knowledge"},
            "Similarities":      {"d": -0.18, "type": "verbal_reasoning"},
            "Vocabulary":        {"d": -0.07, "type": "verbal_memory"},
            "Arithmetic":        {"d": -0.42, "type": "numerical_reasoning"},
            "Letter-Number":     {"d": -0.10, "type": "working_memory"},
            "Block Design":      {"d": -0.26, "type": "spatial"},
            "Matrix Reasoning":  {"d": -0.20, "type": "fluid_reasoning"},
            "Picture Completion": {"d": -0.23, "type": "visual_perception"},
            "Digit-Symbol":      {"d":  0.71, "type": "processing_speed"},
            "Copying":           {"d": -0.19, "type": "processing_speed"},
        },
        "composites": {
            "Full Scale IQ": {"d": -0.24},
        },
    },
    "italian_wais4": {
        "citation": "Pezzuti et al. 2020",
        "lead_gender": "F",
        "country": "Italy",
        "test": "WAIS-IV",
        "n_male": 1087,
        "n_female": 1088,
        "subtests": {
            "Information":       {"d": -0.29, "type": "crystallized_knowledge"},
            "Similarities":      {"d":  0.03, "type": "verbal_reasoning"},
            "Vocabulary":        {"d":  0.04, "type": "verbal_memory"},
            "Arithmetic":        {"d": -0.47, "type": "numerical_reasoning"},
            "Digit Span":        {"d": -0.18, "type": "working_memory"},
            "Letter-Number":     {"d": -0.22, "type": "working_memory"},
            "Block Design":      {"d": -0.29, "type": "spatial"},
            "Matrix Reasoning":  {"d": -0.19, "type": "fluid_reasoning"},
            "Visual Puzzles":    {"d": -0.30, "type": "spatial"},
            "Figure Weights":    {"d": -0.32, "type": "fluid_reasoning"},
            "Comprehension":     {"d": -0.14, "type": "verbal_reasoning"},
            "Symbol Search":     {"d": -0.09, "type": "processing_speed"},
            "Coding":            {"d":  0.02, "type": "processing_speed"},
            "Cancellation":      {"d":  0.01, "type": "processing_speed"},
            "Picture Completion": {"d": -0.14, "type": "visual_perception"},
        },
        "composites": {
            "Full Scale IQ": {"d": -0.24},
        },
    },
    "italian_waisr": {
        "citation": "Pezzuti et al. 2020 (WAIS-R)",
        "lead_gender": "F",
        "country": "Italy",
        "test": "WAIS-R",
        "n_male": 1399,
        "n_female": 1399,
        "subtests": {
            "Information":        {"d": -0.39, "type": "crystallized_knowledge"},
            "Similarities":       {"d":  0.01, "type": "verbal_reasoning"},
            "Vocabulary":         {"d": -0.06, "type": "verbal_memory"},
            "Arithmetic":         {"d": -0.57, "type": "numerical_reasoning"},
            "Digit Span":         {"d": -0.28, "type": "working_memory"},
            "Comprehension":      {"d": -0.21, "type": "verbal_reasoning"},
            "Block Design":       {"d": -0.40, "type": "spatial"},
            "Picture Completion":  {"d": -0.31, "type": "visual_perception"},
            "Picture Arrangement": {"d": -0.22, "type": "visual_perception"},
            "Object Assembly":    {"d": -0.19, "type": "spatial"},
            "Coding":             {"d":  0.03, "type": "processing_speed"},
        },
        "composites": {
            "Full Scale IQ": {"d": -0.32},
        },
    },
    "us_asvab": {
        "citation": "Deary et al. 2007",
        "lead_gender": "M",
        "country": "USA",
        "test": "ASVAB (NLSY79)",
        "n_male": 1292,
        "n_female": 1292,
        "subtests": {
            "General Science":      {"d": -0.21, "type": "crystallized_knowledge"},
            "Arithmetic Reasoning": {"d": -0.17, "type": "numerical_reasoning"},
            "Word Knowledge":       {"d":  0.07, "type": "verbal_memory"},
            "Paragraph Comprehension": {"d": 0.21, "type": "verbal_reasoning"},
            "Numerical Operations": {"d":  0.27, "type": "processing_speed"},
            "Coding Speed":         {"d":  0.48, "type": "processing_speed"},
            "Auto & Shop Info":     {"d": -0.89, "type": "vocational_knowledge"},
            "Math Knowledge":       {"d":  0.00, "type": "numerical_reasoning"},
            "Mechanical Comprehension": {"d": -0.58, "type": "vocational_knowledge"},
            "Electronics Info":     {"d": -0.56, "type": "vocational_knowledge"},
        },
        "composites": {
            # AFQT percentile — not FSIQ but closest equivalent
            "Full Scale IQ": {"d": -0.02},  # AFQT standardised d
        },
    },
}


# ── Random-effects meta-analysis (DerSimonian-Laird) ─────────────────────

def variance_d(d, n1, n2):
    """Variance of Cohen's d (Hedges & Olkin approximation)."""
    return (n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2))


def meta_analyze_re(effects):
    """
    Random-effects meta-analysis (DerSimonian-Laird).
    effects: list of (d, var_d) tuples.
    Returns: (pooled_d, se, ci_lo, ci_hi, Q, tau2, I2)
    """
    k = len(effects)
    if k == 0:
        return 0, 0, 0, 0, 0, 0, 0
    if k == 1:
        d, v = effects[0]
        se = math.sqrt(v)
        return d, se, d - 1.96 * se, d + 1.96 * se, 0, 0, 0

    # Fixed-effects pooled (for Q calculation)
    w_fe = [1.0 / v for _, v in effects]
    sum_w = sum(w_fe)
    pooled_fe = sum(w * d for (d, _), w in zip(effects, w_fe)) / sum_w
    Q = sum(w * (d - pooled_fe) ** 2 for (d, _), w in zip(effects, w_fe))

    # DerSimonian-Laird tau^2
    c = sum_w - sum(w ** 2 for w in w_fe) / sum_w
    tau2 = max(0, (Q - (k - 1)) / c)

    # Random-effects weights
    w_re = [1.0 / (v + tau2) for _, v in effects]
    sum_w_re = sum(w_re)
    pooled_re = sum(w * d for (d, _), w in zip(effects, w_re)) / sum_w_re
    se_re = math.sqrt(1.0 / sum_w_re)
    ci_lo = pooled_re - 1.96 * se_re
    ci_hi = pooled_re + 1.96 * se_re

    # I^2
    I2 = max(0, (Q - (k - 1)) / Q * 100) if Q > 0 else 0

    return pooled_re, se_re, ci_lo, ci_hi, Q, tau2, I2


# ── Aggregate by cognitive domain ─────────────────────────────────────────

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

print("=" * 90)
print("META-ANALYSIS v2: Sex Differences by Cognitive Domain (Random-Effects)")
print("Convention: negative = male advantage, positive = female advantage")
print("4 datasets, 3 countries, 2 battery types (WAIS + ASVAB)")
print("=" * 90)
print()

domain_order = [
    "verbal_memory", "verbal_reasoning", "crystallized_knowledge",
    "numerical_reasoning", "working_memory", "spatial",
    "fluid_reasoning", "visual_perception", "processing_speed",
    "vocational_knowledge",
]

domain_labels = {
    "verbal_memory": "Verbal Memory (Vocabulary, Word Knowledge)",
    "verbal_reasoning": "Verbal Reasoning (Similarities, Comprehension, Para.Comp)",
    "crystallized_knowledge": "Crystallized Knowledge (Information, Gen. Science)",
    "numerical_reasoning": "Numerical Reasoning (Arithmetic, Math Knowledge)",
    "working_memory": "Working Memory (Digit Span, Letter-Number)",
    "spatial": "Spatial (Block Design, Visual Puzzles, Object Assembly)",
    "fluid_reasoning": "Fluid Reasoning (Matrix Reasoning, Figure Weights)",
    "visual_perception": "Visual Perception (Picture Completion/Arrangement)",
    "processing_speed": "Processing Speed (Coding, Digit-Symbol, Num.Ops, etc.)",
    "vocational_knowledge": "Vocational Knowledge (Auto&Shop, Mechanical, Electronics)",
}

results = []
for domain in domain_order:
    if domain not in domain_effects:
        continue
    effects = [(d, v) for d, v, _, _ in domain_effects[domain]]
    pooled, se, ci_lo, ci_hi, Q, tau2, I2 = meta_analyze_re(effects)
    k = len(effects)
    iq_pts = pooled * 15

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
        "tau2": round(tau2, 4),
        "I2": round(I2, 1),
        "direction": direction,
    })

    print(f"  {label}")
    print(f"    k={k}  pooled d = {pooled:+.3f}  SE = {se:.3f}  95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}]")
    print(f"    IQ points: {iq_pts:+.1f}  Direction: {direction}")
    print(f"    Heterogeneity: Q={Q:.2f}  tau2={tau2:.4f}  I2={I2:.0f}%")

    for d, v, study, subtest in domain_effects[domain]:
        print(f"      {study}: {subtest} d = {d:+.2f}")
    print()

# ── Composite FSIQ / AFQT ────────────────────────────────────────────────

print("=" * 90)
print("FULL SCALE IQ / AFQT — Random-effects meta-analysis across studies")
print("=" * 90)
print()

fsiq_effects = []
for study_key, study in studies.items():
    d = study["composites"]["Full Scale IQ"]["d"]
    v = variance_d(d, study["n_male"], study["n_female"])
    fsiq_effects.append((d, v, study["citation"]))
    note = " (AFQT standardised score)" if "ASVAB" in study["test"] else ""
    print(f"  {study['citation']}: d = {d:+.2f} ({d*15:+.1f} IQ pts){note}")

pooled, se, ci_lo, ci_hi, Q, tau2, I2 = meta_analyze_re(
    [(d, v) for d, v, _ in fsiq_effects]
)
print()
print(f"  POOLED (RE): d = {pooled:+.3f}  95% CI [{ci_lo:+.2f}, {ci_hi:+.2f}]")
print(f"  IQ points: {pooled*15:+.1f}  [{ci_lo*15:+.1f}, {ci_hi*15:+.1f}]")
print(f"  Heterogeneity: Q={Q:.2f}  tau2={tau2:.4f}  I2={I2:.0f}%")
print()

# FSIQ without ASVAB (WAIS-only)
fsiq_wais = [(d, v) for d, v, c in fsiq_effects if "Deary" not in c]
pw, sw, lw, hw, qw, tw, iw = meta_analyze_re(fsiq_wais)
print(f"  WAIS-only ({len(fsiq_wais)} studies): d = {pw:+.3f}  IQ = {pw*15:+.1f} pts")
print(f"    95% CI [{lw:+.2f}, {hw:+.2f}]  Q={qw:.2f}  I2={iw:.0f}%")
print()

# ── Summary table ─────────────────────────────────────────────────────────

print("=" * 90)
print("SUMMARY TABLE (Random-Effects)")
print("=" * 90)
print()
hdr = f"{'Domain':<55} {'k':>3} {'d':>7} {'IQ':>6} {'95% CI':>16} {'I2':>5} {'Dir':>7}"
print(hdr)
print("-" * len(hdr))
for r in results:
    print(f"{r['domain']:<55} {r['k']:>3} {r['pooled_d']:>+7.3f} {r['iq_pts']:>+6.1f} {r['ci']:>16} {r['I2']:>4.0f}% {r['direction']:>7}")
print("-" * len(hdr))
print(f"{'Full Scale IQ (4 studies, RE)':<55} {len(fsiq_effects):>3} {pooled:>+7.3f} {pooled*15:>+6.1f} {'[{:.2f}, {:.2f}]'.format(ci_lo, ci_hi):>16} {I2:>4.0f}% {'MALE':>7}")
print(f"{'Full Scale IQ (WAIS only, 3 studies)':<55} {len(fsiq_wais):>3} {pw:>+7.3f} {pw*15:>+6.1f} {'[{:.2f}, {:.2f}]'.format(lw, hw):>16} {iw:>4.0f}% {'MALE':>7}")
print()
print("Negative d / IQ = male advantage. Positive = female advantage.")
print()
print("CAVEATS:")
print("  1. Random-effects (DerSimonian-Laird) — accounts for between-study heterogeneity")
print("  2. Subtests within a study are correlated (r≈0.3-0.7) — CIs still somewhat too narrow")
print("     Proper fix requires robust variance estimation (RVE) in R/metafor")
print("  3. ASVAB 'vocational knowledge' subtests (Auto&Shop, Mechanical, Electronics)")
print("     are interest/exposure measures, not cognitive ability per se")
print("  4. 4 studies from 3 countries is still a small k for random-effects estimation")
print()

# ── Thought experiments ───────────────────────────────────────────────────

print("=" * 90)
print("THOUGHT EXPERIMENTS: How weighting changes the answer")
print("=" * 90)
print()

all_effects = []
for domain in domain_order:
    if domain not in domain_effects:
        continue
    for d, v, study, subtest in domain_effects[domain]:
        all_effects.append((d, v, domain, subtest))

# All subtests
ae = [(d, v) for d, v, _, _ in all_effects]
p, s, l, h, q, t, i = meta_analyze_re(ae)
print(f"  All {len(ae)} subtest effects:")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()

# Without vocational knowledge
nv = [(d, v) for d, v, dom, _ in all_effects if dom != "vocational_knowledge"]
p, s, l, h, q, t, i = meta_analyze_re(nv)
print(f"  Without vocational knowledge ({len(nv)} effects):")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()

# Without processing speed
ns = [(d, v) for d, v, dom, _ in all_effects if dom != "processing_speed"]
p, s, l, h, q, t, i = meta_analyze_re(ns)
print(f"  Without processing speed ({len(ns)} effects):")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()

# Without vocational knowledge AND processing speed
nb = [(d, v) for d, v, dom, _ in all_effects
      if dom not in ("vocational_knowledge", "processing_speed")]
p, s, l, h, q, t, i = meta_analyze_re(nb)
print(f"  Without vocational knowledge AND processing speed ({len(nb)} effects):")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()

# Without DIF-biased subtests (Information, Arithmetic) and vocational
nc = [(d, v) for d, v, dom, sub in all_effects
      if dom not in ("vocational_knowledge",)
      and sub not in ("Information", "General Science", "Arithmetic",
                      "Arithmetic Reasoning")]
p, s, l, h, q, t, i = meta_analyze_re(nc)
print(f"  Without knowledge/DIF-biased subtests ({len(nc)} effects):")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()

# Core cognitive only (spatial + fluid + verbal reasoning + working memory)
core = [(d, v) for d, v, dom, _ in all_effects
        if dom in ("spatial", "fluid_reasoning", "verbal_reasoning", "working_memory")]
p, s, l, h, q, t, i = meta_analyze_re(core)
print(f"  Core cognitive only (spatial+fluid+verbal reasoning+WM, {len(core)} effects):")
print(f"    d = {p:+.3f}  IQ = {p*15:+.1f}  CI [{l:+.2f}, {h:+.2f}]  I2={i:.0f}%")
print()
