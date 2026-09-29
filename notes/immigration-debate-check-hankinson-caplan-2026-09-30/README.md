# Debate check: Hankinson v Caplan, Soho Forum (June 2026)

Date: 2026-09-30. Status: **cursory**, at the operator's request. It records which of the debate's
checkable claims the repo answers. It does not report new research results.

Source: ReasonTV, "Should ICE deport all illegal aliens?" (https://www.youtube.com/watch?v=giyRpB66wSM,
uploaded 2026-06-09). The resolution was that ICE should deport all illegal aliens. Simon Hankinson
(Heritage) argued for it and Bryan Caplan (GMU) against. The auto-caption transcript is not stored.

## How it was made

- The claims list (`debate-claims.md`) was read from the full transcript.
- Four agents (claude-opus-5-5) mapped each claim to repo passages and graded it, one file per
  cluster. They were stopped early to save tokens, and some external checks are single-source.
- The parent re-checked three repo-derived figures:
  - the keyhole split: `c6_split.py` was rerun, and its line figures match;
  - border release shares: recomputed from
    `infra/immigration-fiscal/unauthorized_population_size_2026_09_19/derived/stock_flow_dispositions.csv`
    as 25/38/56/71% released or paroled in FY2021–24, and 36/50/69/86% if every transfer to ICE was released;
  - ladder 24's `mass_deportation_sim.py`: absent from disk, so its $1.45T output figure cannot be rerun.
- Cluster A reports two "scratch checks": SCAAP state shares and Texas homicide arrests by legal status.
  They are agent calculations, not repo results.

## Tally

| Grade | Count |
|---|---:|
| Answered | 10 |
| Partial | 27 |
| Gap | 4 |
| Out of scope | 4 |
| **Total** | **45** |

The normative arguments were not graded: rule of law, what "all" means in the resolution, and
property rights.

## Main finding

The repo answers the fiscal *concepts* well:
- non-rival spending (FAQ 2);
- payroll taxes paid on invalid SSNs (FAQ 3);
- comparisons at equal schooling (FAQ 7);
- the skill gradient;
- specialisation (FAQ 14).

It also answers the European crime claims from register data. Its executed numbers, though, cover
the Mexican-origin stock, 72% of it US-born citizens. The debate is about the unauthorized of all
origins, and the repo has no account for them. It also has no cost per removal and no count of
citizens caught up in enforcement.

## Keyhole split (C6)

`c6_split.py` prints two totals:
- the main case, with the pension accrual: $371.4–434.8bn;
- the cash set, with benefits counted when paid: $294.7–361.8bn.

Remove means-tested aid and Medicaid, and $130/198bn remains on the main case, or $53/125bn on the
cash set. Remove schools as well, and the result turns into a gain: −$60/−3bn on the main case,
−$137/−76bn on the cash set. Quote the pair, and add that no immigrant-only keyhole reaches the
US-born majority.

## Files

- `debate-claims.md`: the 45 checkable claims, with transcript timestamps.
- `cluster-A.md`: US crime and public safety.
- `cluster-B.md`: Europe, crime and fiscal.
- `cluster-C.md`: US fiscal, benefits, labour and economics.
- `cluster-D.md`: enforcement, border, assimilation and cohesion.
- `c6_split.py`: the keyhole split from the September 29 decomposition lines.
