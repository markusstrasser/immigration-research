## Reviewer B — numerical/denominator/base-rate audit

Scope: arithmetic, denominators/base rates, ranking strength, extrapolation. Packet is mostly *corrective* edits that narrow prior overclaims, and most extrapolation/ranking issues are already being walked back. I found **two confirmed numerical defects** — one of which (a denominator mismatch) likely reverses a headline conclusion that propagates across the memo set — plus minor items in a speculative section.

---

## Confirmed issues

### C1 — Mexico school-per-adult mixes a scenario-subset numerator with a full-stock denominator; the federal layer it's subtracted from does not

`research/immigration-conclusion-audit-running-fixes.md`, lines 29, 33–39, 62 (propagated to 170, 200–205, 922).

The "corrected" Mexico-origin crude annual layer is `net 747.993 = federal 1519.278 − school 771.285` (line 29). The two terms are normalized on **different bases**:

- **Federal** is a denominator-invariant per-adult *mean*: `$1,519.28` holds whether multiplied by the scenario subset (436,819 → `$664M`, line 119) or the full stock (8,496,334 → `$12.908B`, line 98).
- **School** is a fixed scenario-subset *dollar total* divided by whichever adult count you choose. The memo's own derivation (line 39) is `20907.09 * 0.9718 * 322540 / 8496334 = ~$771` — i.e. numerator built from the **scenario subset's** household weight (`HH weight 322,540`, line 35; = 436,819 scenario adults) but divided by the **full-stock** count (8,496,334). Divide the same ~$6.55B subset total by the *matching* subset adults and you get `$15,002/adult` (→ net `1519 − 15002 ≈ −$13.5k`, the figure line 13 discarded).

So the "fix" swapped only the school denominator (436,819 → 8,496,334) while leaving a subset-level numerator, then subtracted that from a full-stock per-adult mean. That is the bug, and it is what turns the net from negative to `+$748`.

Internal corroboration that `$771` is an undercount, not the cohort nuance line 68 suggests:
- Implied Mexico-origin school-age children = `322,540 × 0.9718 ≈ 313k` over 8.5M adults = **0.037 kids/adult** — ~10× below any plausible rate.
- Cross-check line 202 vs 205: Mexico school `$771/adult` vs **NH-white-US-born school `$6,023/adult`** (line 205). Mexico-origin households are more child-heavy, yet show ~8× *lower* per-adult school cost — demographically inverted. The NH-white row is on a full/full basis; the Mexico row is not.

**Why it matters:** `+$748/adult` and "federal-minus-school is **positive** for Mexico-origin adults" (lines 62, 170, 922) are the load-bearing result of this whole correction and are cited downstream. On a denominator-consistent basis the Mexico net is almost certainly negative.

**Minimal fix:** Recompute `school_per_adult` as a full-stock mean (full-stock school **total** ÷ 8,496,334), not (scenario-subset total ÷ 8,496,334). The exact corrected value needs the full-stock school numerator, which isn't in the packet; pending that, do **not** assert the layer is positive. At line 68 replace the cohort framing with the actual defect: the numerator covers only the ~436,819-adult scenario subset while the denominator is the full 8.5M stock, so `$771` is a mechanical undercount of order ~10×, and the federal term in the same subtraction is a full-stock mean.

### C2 — EU27-origin crude-net is internally inconsistent

`research/immigration-conclusion-audit-running-fixes.md`, line 204:

```
| EU27-origin | $4,694.65 | $63.71 | $4,657.82 |
```

`4694.65 − 63.71 = 4630.94`, not `4657.82` (off by **$26.88**). The other three rows in the same "Current `v_three_layer_annual`" table satisfy `net = federal − school` (Mexico 747.99 ✓; MX+NT 427.55 ✓ to rounding; NH-white −3277.20 ✓). EU27 is the one row that doesn't.

**Minimal fix:** Set net to `$4,630.94` to match the stated federal/school, or correct whichever of the three was mistranscribed against the live view.

---

## Speculative / weak preferences (not blocking)

1. **Wage-side ranking is too thin to assert.** `immigration-capacity-frontier-2026-04-21.md` lines 108–110: "wage-growth models load more cleanly on load-capacity than on stock or flow" rests on adj R² `0.154` vs `0.147` vs `0.144` and t `−4.08` vs `−3.97`. That Δ is within noise; soften "cleaner" to "marginally best-fitting." (The *employment* ranking, t −7.10 vs p≈0.17, is solid — leave it.)

2. **FAIR rounding.** `immigration-restrictionist-arguments-steelman-2026-06-15.md` line 98: "`$182B − $32B = $150.7B`" — the rounded inputs give $150B; the precise FAIR figures are ~$182.1B − $31.4B (and `$31.4B` rounds to `$31B`, not `$32B`). Cosmetic; it's relayed advocacy data, already labeled.

3. **MX+N.Triangle federal/adult ≈ Mexico's.** Lines 202–203: `$1,519.02` vs `$1,519.28` despite different school/demographics. Possibly a copy artifact, but it back-solves to a self-consistent ~$1,518.6/adult for the Triangle alone, so unconfirmable from the packet — worth a glance at the source.

4. **Univariate vs multivariate sign flip, unsignposted.** `immigration-causal-surge-2021-2024.md`: recent-FB inflow quintiles show a *positive* GOP gradient (lines 84–88, Q1 +1.96 → Q5 +2.39) while the regression coefficient is *negative* (line 115, −1.82). Not an error (suppression/confounding), and the text handles the negative coefficient, but a one-clause note at the quintile table would prevent a reader quoting the raw gradient against the coefficient.

5. **Sub-0.1 rounding mismatches — all benign.** Receiver mean diff (6.40−2.00=4.40 vs stated 4.41, surge line 111); decile gaps 1.57 vs 1.56 (capacity lines 211–213); native-migration gap 1.06 vs 1.07 (line 156); ratio-of-medians 4.59/0.21=21.86 vs 21.7 (line 319). Each is consistent with rounding of higher-precision underlying values; no action.

I verified the items the packet itself flags as denominator/extrapolation fixes (ICE docket numerator/denominator, line 124; race-corrected incarceration 50%→30%, lines 174–178; age-25 NPV vs current-stock, lines 76–78; E-Verify margin scoping) and they are handled correctly.
