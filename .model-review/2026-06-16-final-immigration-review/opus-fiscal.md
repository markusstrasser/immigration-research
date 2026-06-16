## Reviewer A — Fiscal ledger / denominator / NPV / arithmetic review

Scope: fiscal ledger, denominator/base-rate, NAS vs current-stock NPV, school/federal universe, scalar exports, arithmetic/logical consistency. All arithmetic below is reproducible from the packet so the coordinator can verify locally.

---

## CONFIRMED FINDINGS

### A-1 (highest impact). The "illustrative lifetime stack" band `−$37k to +$28k` silently reintroduces the withheld `$771/yr` school number — same file, same table, that marks school "unresolved"

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:44-48` and revisions row `:159`.

The table lists:

```
NAS benchmark              +$45,631
− school annuitized        unresolved            (line 45)
− state/local ($657/yr)    −$15,300              (line 46)
− enforcement ($2,100/yr)  −$49,000              (line 47)
Band                       −$37k to +$28k        (line 48)
```

With school treated as unresolved (excluded), the band reproducible from the *listed* rows is:
- upper (subtract state/local only): `45,631 − 15,300 = +30,331`
- lower (state/local + enforcement): `45,631 − 15,300 − 49,000 = −18,669`

i.e. **≈ −$19k to +$30k**, not the published **−$37k to +$28k**. The `−$37k` floor is unreachable from the non-withheld rows. It is only reproducible by adding back the withheld school cost:

`45,631 − 17,964(=$771/yr × 23.3) − 15,300 − 49,000 = −36,633 ≈ −$37k`.

So the band's lower endpoint bakes in exactly the `$771/adult/yr` school figure that this document's warehouse-layer table (`:120-122`) and the running-fixes ledger (`immigration-conclusion-audit-running-fixes.md:64, 70, 74-95`) withdraw as a universe-mismatch artifact. The warehouse table was corrected on 2026-06-16; **the illustrative stack in the same file was not** — this is the one surface where the withheld number still drives an exported result.

Minimal fix: recompute the band from live rows only and relabel (≈ −$19k to +$30k with school excluded), or, if the stack is meant to show the full ledger, restore school as an explicitly illustrative row (not "unresolved") and state it is not live. The current state — "unresolved" in the row but present in the floor — is a direct internal contradiction.

### A-2. Subtracted layers are annuitized at a convention that contradicts the NAS 3%/75-yr basis they are subtracted from; rate/horizon/price-base are unstated

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:33, 46-47`.

The benchmark `+$45,631` is explicitly NAS Table 8-13 on a **2012$, 3%, 75-yr** basis (`:33`). The subtracted streams imply annuity factors:
- `15,300 / 657 = 23.29`
- `49,000 / 2,100 = 23.33`

Both ≈ **23.3**, consistent with ~75 yr @ ~4% or ~40 yr @ 3%. The NAS 3%/75-yr factor is `[1−1.03⁻⁷⁵]/0.03 = 29.70`. So the cost streams are discounted ~27% harder than the benchmark they net against. Harmonized to 29.70 the rows would be `657 × 29.70 = −$19,514` and `2,100 × 29.70 = −$62,374`. Separately, the streams are recent-year dollars (CBO 2025, ICE FY25) while the benchmark is 2012$ — no deflation is applied.

(Charitable reading: the streams may be intended over the stock's *remaining* life (~40 yr), which is defensible given the stock is 53.2% age 45-64 (`:64`). But then the `+$45,631` benchmark — a full 75-yr-from-age-25 figure — must also be put on a remaining-life basis; it isn't. The mismatch holds either way.)

Minimal fix: state the discount rate and horizon for the annuitization and put benchmark and streams on the same rate/horizon/price-base. This is the repo's own G-LIF-A04 / G-LIF-M01 unit-harmonizer requirement (`immigration-lifetime-fiscal-generators.md:34-41, 562-568`).

### A-3. Base-population mismatch: nationwide per-unauthorized-stock costs applied per Mexico-birthplace adult

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:46-47, 33, 68, 76`; derivation anchor `immigration-lifetime-fiscal-generators.md:786` (`$29.5B / 14M ≈ $2.1k/yr`).

The stack's denominator is **8.5M Mexico birthplace adults** (`:68`), of which only **~4.3M are unauthorized** (`:76`, Pew). But the subtracted enforcement `$2,100/yr` is a **nationwide per-unauthorized average** (`$29.5B ÷ 14M`, per G-LIF-R03), and `$657/yr` state/local is likewise a per-added-resident/stock average. Applying a per-unauthorized-stock cost to *every* Mexico-birthplace adult over-attributes by roughly the authorized share — ~49% of the 8.5M are not unauthorized. This is the same denominator class the document polices elsewhere (`G-LIF-Q03` birthplace ≠ legal status, `:730-736`; `:71` "≠ 4.3M Mexico-unauthorized").

Minimal fix: scale the enforcement/state-local rows by the unauthorized share of the stack (~4.3M/8.5M ≈ 0.51) before subtracting from a per-Mexico-birthplace benchmark, or rebuild the stack on a single declared population universe. Note `:50` already flags enforcement as `[FRAMING-SENSITIVE]` for fixed-vs-marginal, but the base-population mismatch is a separate, unflagged defect.

### A-4. State/local subtracted on top of a benchmark that already contains "some state/local," before the overlap matrix the document says is required

`research/immigration-mexico-npv-population-synthesis-2026-06-15.md:32, 46, 80`.

`:32` states the NAS cell includes "Federal + some state/local inside NAS cell." The stack then subtracts CBO state/local surge (`:46`) without netting against the state/local already inside the NAS cell. The document itself lists `v_full_fiscal_stack` "+ overlap matrix" as an unbuilt priority (`:80`, G-LIF-R05). So the band is computed before the overlap reconciliation the doc says is needed — risk of partial double-subtraction (magnitude depends on how much state/local NAS already booked, which the packet does not quantify).

Minimal fix: state that the subtracted state/local is incremental to the NAS-cell state/local, or defer the band until the overlap matrix exists.

---

## SPECULATIVE / LOWER-CONFIDENCE

### S-1. Pew/CIS net-stock "band" conflates different windows
`immigration-mexico-npv-population-synthesis-2026-06-15.md:75, 92, 135`: `+3.5M (2021→23, Pew, 2-yr)` and `+5.6M (2021→25, CIS, 4-yr)` are presented as one band "+3.5M to +5.6M." Different end years make this not a like-for-like range. Fix: label each window on the band rather than implying a same-period spread.

### S-2. A generator retrodiction still cites the withheld `$771/yr` as fact
`immigration-lifetime-fiscal-generators.md:779` (G-LIF-R02): "current-HH school burden ($771/yr)" with no "(now withheld)" caveat, unlike G-LIF-M02 (`:574`) and G-LIF-K01 (`:484-486`) which were corrected. Low priority (descriptive text, not a live export). Fix: add the withheld marker for consistency.

### S-3. Federal proxy scope not restated at point of use
`immigration-mexico-npv-population-synthesis-2026-06-15.md:38, 91, 119` cite `+$1,519/adult/yr` as "federal annual proxy"; the binding scope (payroll/FICA minus SNAP/TANF/SSI only — not income tax, Medicare/Medicaid, EITC, capital/corporate) lives only in `immigration-conclusion-audit-running-fixes.md:2498`. Labeled "proxy," so minor, but a reader of this file alone could read it as all-federal. Fix: one-line scope footnote where the number first appears.

---

## Checked and found CONSISTENT (no action)
- NAS multiply-out (`:54-60`): row products, share/N consistency, and total `+$387.7B` all reconcile; `+$387.7B / 8,496,334 = $45,631/adult` ✓; correctly guarded as synthetic age-25 benchmark, not stock NPV (`:64`, G-LIF-Q06).
- School universe-mismatch arithmetic (`running-fixes:82`): `322,540 × 0.9718 = 313k`; `313k/8.5M = 0.037` ✓; the `−$13.5k → +$748` flip and the same-universe withholding are arithmetically sound and correctly resolved.
- `federal − school = 747.993` (`running-fixes:31`) ✓; `$1,519 × 436,819 = $664M`, `× 8.5M = $12.9B` (G-LIF-M02 `:574`) ✓.
- Generator counts: 106 MD headings (recounted by cluster), 104 DuckDB, MD-only Q06/S15, 19 clusters, 563 parameter_claims — internally consistent across `generators.md:6`, `thesis-generator-audit:18`, `INDEX:54`; the stale "105" was fixed.
- Mass-deportation `$1.5T–$2.3T ≈ 5–8% GDP` (`claims-evolution:97`) ✓.

The single most important item is **A-1**: the corrected withholding did not propagate to the illustrative lifetime band in the same file, so a withdrawn school number still produces a quotable `−$37k` figure.
