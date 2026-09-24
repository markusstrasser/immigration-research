# Outside checks, combined

**Verdict:** Run once through the explorer engine on the adopted main case, the three outside checks of
2026-09-24 give **$215.6–261.0bn** (+$12.35bn at the low end, +$11.32bn at the high end), against the
adopted $203.2–249.6bn. The changes add without interaction. This is a proposal: nothing here is adopted.
[CALCULATION: `combine.cjs` → `derived/combined_bands.csv`]

| Specification | Main case, $bn | Change, $bn |
|---|---|---|
| Adopted | 203.21–249.64 | — |
| Schools priced where the group enrolls (ladder 215) | 206.59–252.67 | +3.38 / +3.03 |
| Benefit keys from administrative records (ladder 217) | 205.47–251.81 | +2.27 / +2.17 |
| CBO income gradients, Medicaid excluded (ladder 216) | 213.77–259.08 | +10.56 / +9.44 |
| Treasury credit shares (ladder 216) | 198.65–245.33 | −4.55 / −4.31 |
| **All three, administrative change on overlapping lines** | **215.56–260.95** | **+12.35 / +11.32** |
| All three, CBO also applied on overlapping lines | 214.86–259.97 | +11.65 / +10.33 |

Overlap rule: the benefit-keys lane and CBO's bundle both re-key SNAP, WIC and cash assistance. The
combination keeps the administrative change on those three lines and drops CBO's, because CBO's
translation holds the group's share within each income group fixed, which is what the administrative
records test. Applying both double-adjusts those lines by about $0.7–1.0bn.

Scope: relative to the adopted main case only. The audit package (`dataset_integrity_2026_09_23`) is not
in the engine, and its rows 3, 6 and 13 overlap the income-tax, school and benefit corrections, so the
two cannot be combined by addition. Combining them needs the audit's rows in the engine first.

Gates: with no change the script reproduces `main_case_2026_09_23/derived/main_case_bands.csv`
(203.2070–249.6400) to 1e-4; each lane's change alone reproduces that lane's published figure to 1e-3.

```sh
node infra/immigration-fiscal/outside_checks_combined_2026_09_24/combine.cjs   # all gates must pass
```
