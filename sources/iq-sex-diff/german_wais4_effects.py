"""
Compute Cohen's d from German WAIS-IV standardization (Daseking et al. 2017).
N=1425 (679 males, 746 females), ages 16-90, census-matched.
Data from Table 3 of the paper.
"""
import math

def cohens_d(m1, sd1, m2, sd2):
    """Cohen's d = (M_male - M_female) / SD_pooled. Negative = male advantage."""
    pooled_sd = math.sqrt((sd1**2 + sd2**2) / 2)
    return -(m1 - m2) / pooled_sd  # negative = male advantage convention

# Index scores (IQ metric: M=100, SD=15)
indices = {
    "FSIQ":  {"m_m": 101.61, "m_sd": 15.35, "f_m": 98.45, "f_sd": 14.56},
    "GAI":   {"m_m": 102.09, "m_sd": 15.22, "f_m": 98.02, "f_sd": 14.61},
    "VCI":   {"m_m": 101.75, "m_sd": 14.97, "f_m": 98.41, "f_sd": 14.77},
    "PRI":   {"m_m": 102.12, "m_sd": 15.18, "f_m": 98.15, "f_sd": 14.50},
    "WMI":   {"m_m": 102.62, "m_sd": 15.72, "f_m": 97.64, "f_sd": 13.98},
    "PSI":   {"m_m": 98.26, "m_sd": 14.71, "f_m": 101.55, "f_sd": 15.06},
}

# Subtest scores (scaled score metric: M=10, SD=3)
subtests = {
    "Block Design":       {"m_m": 10.38, "m_sd": 3.13, "f_m": 9.83, "f_sd": 2.97, "type": "spatial"},
    "Similarities":       {"m_m": 10.13, "m_sd": 3.06, "f_m": 9.96, "f_sd": 3.01, "type": "verbal_reasoning"},
    "Digit Span":         {"m_m": 10.17, "m_sd": 3.12, "f_m": 9.83, "f_sd": 2.82, "type": "working_memory"},
    "Matrix Reasoning":   {"m_m": 10.28, "m_sd": 3.07, "f_m": 9.81, "f_sd": 2.90, "type": "fluid_reasoning"},
    "Vocabulary":         {"m_m": 10.28, "m_sd": 3.20, "f_m": 9.90, "f_sd": 3.02, "type": "verbal_memory"},
    "Arithmetic":         {"m_m": 10.77, "m_sd": 3.11, "f_m": 9.37, "f_sd": 2.73, "type": "numerical_reasoning"},
    "Symbol Search":      {"m_m": 9.82, "m_sd": 2.99, "f_m": 10.14, "f_sd": 2.94, "type": "processing_speed"},
    "Visual Puzzles":     {"m_m": 10.45, "m_sd": 3.06, "f_m": 9.53, "f_sd": 2.77, "type": "spatial"},
    "Information":        {"m_m": 10.65, "m_sd": 2.88, "f_m": 9.42, "f_sd": 2.92, "type": "crystallized_knowledge"},
    "Coding":             {"m_m": 9.53, "m_sd": 2.88, "f_m": 10.38, "f_sd": 3.08, "type": "processing_speed"},
    "Letter-Number":      {"m_m": 10.26, "m_sd": 3.25, "f_m": 9.91, "f_sd": 2.82, "type": "working_memory"},
    "Figure Weights":     {"m_m": 10.37, "m_sd": 3.05, "f_m": 9.50, "f_sd": 2.89, "type": "fluid_reasoning"},
    "Comprehension":      {"m_m": 10.37, "m_sd": 3.15, "f_m": 9.87, "f_sd": 2.89, "type": "verbal_reasoning"},
    "Cancellation":       {"m_m": 9.92, "m_sd": 3.14, "f_m": 10.13, "f_sd": 2.88, "type": "processing_speed"},
    "Picture Completion":  {"m_m": 10.16, "m_sd": 2.80, "f_m": 9.82, "f_sd": 3.08, "type": "visual_perception"},
}

print("=" * 80)
print("GERMAN WAIS-IV Sex Differences (Daseking et al. 2017, N=1425)")
print("Negative d = male advantage, positive d = female advantage")
print("=" * 80)
print()

print("INDEX SCORES:")
print(f"{'Index':<25} {'Male M(SD)':<18} {'Female M(SD)':<18} {'Diff':>6} {'d':>7} {'Dir':>8}")
print("-" * 85)
for name, data in indices.items():
    d = cohens_d(data["m_m"], data["m_sd"], data["f_m"], data["f_sd"])
    diff = data["m_m"] - data["f_m"]
    direction = "MALE" if d < -0.05 else ("FEMALE" if d > 0.05 else "~NONE")
    print(f"{name:<25} {data['m_m']:.1f} ({data['m_sd']:.1f}){'':<5} {data['f_m']:.1f} ({data['f_sd']:.1f}){'':<5} {diff:>+6.1f} {d:>+7.3f} {direction:>8}")

print()
print("SUBTEST SCORES:")
print(f"{'Subtest':<25} {'Male M(SD)':<18} {'Female M(SD)':<18} {'Diff':>6} {'d':>7} {'Type':<25} {'Dir':>8}")
print("-" * 110)

by_type = {}
for name, data in subtests.items():
    d = cohens_d(data["m_m"], data["m_sd"], data["f_m"], data["f_sd"])
    diff = data["m_m"] - data["f_m"]
    direction = "MALE" if d < -0.05 else ("FEMALE" if d > 0.05 else "~NONE")
    tp = data["type"]
    by_type.setdefault(tp, []).append((name, d))
    print(f"{name:<25} {data['m_m']:.2f} ({data['m_sd']:.2f}){'':<4} {data['f_m']:.2f} ({data['f_sd']:.2f}){'':<4} {diff:>+6.2f} {d:>+7.3f} {tp:<25} {direction:>8}")

print()
print("BY DOMAIN (for meta-analysis input):")
for tp, items in sorted(by_type.items()):
    ds = [d for _, d in items]
    avg = sum(ds) / len(ds)
    print(f"  {tp}: mean d = {avg:+.3f}  subtests: {', '.join(f'{n} ({d:+.2f})' for n, d in items)}")

print()
print("KEY FINDINGS:")
d_fsiq = cohens_d(indices["FSIQ"]["m_m"], indices["FSIQ"]["m_sd"],
                   indices["FSIQ"]["f_m"], indices["FSIQ"]["f_sd"])
d_psi = cohens_d(indices["PSI"]["m_m"], indices["PSI"]["m_sd"],
                  indices["PSI"]["f_m"], indices["PSI"]["f_sd"])
print(f"  FSIQ male advantage: d = {d_fsiq:+.3f} ({indices['FSIQ']['m_m'] - indices['FSIQ']['f_m']:.1f} IQ points)")
print(f"  PSI female advantage: d = {d_psi:+.3f} ({indices['PSI']['f_m'] - indices['PSI']['m_m']:.1f} IQ points)")
d_ar = cohens_d(subtests["Arithmetic"]["m_m"], subtests["Arithmetic"]["m_sd"],
                 subtests["Arithmetic"]["f_m"], subtests["Arithmetic"]["f_sd"])
d_in = cohens_d(subtests["Information"]["m_m"], subtests["Information"]["m_sd"],
                 subtests["Information"]["f_m"], subtests["Information"]["f_sd"])
d_cd = cohens_d(subtests["Coding"]["m_m"], subtests["Coding"]["m_sd"],
                 subtests["Coding"]["f_m"], subtests["Coding"]["f_sd"])
print(f"  Largest male: Arithmetic d = {d_ar:+.3f}, Information d = {d_in:+.3f}")
print(f"  Largest female: Coding d = {d_cd:+.3f}")
print(f"  Education effect >> sex effect: omega2(EDL) = 0.264 vs omega2(sex) = 0.005 for FSIQ")
