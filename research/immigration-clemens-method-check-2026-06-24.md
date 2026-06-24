# Clemens Method Check — GE vs Partial-Equilibrium? (2026-06-24)

**Scope:** Verify ONE claim. Repo labels Clemens's <HS lifetime-NPV adjustment (−$109k → +$128k) as "general-equilibrium / capital-tax GE." A conviction-review flagged this as WRONG, claiming the adjustment is actually a **fixed-price partial-equilibrium capital-income-tax accounting correction**. Verified against Clemens's actual method (primary PDF text extracted).

**Status:** RESOLVED — conviction-review is CORRECT. Relabel warranted.

## VERDICT

**The "GE / general-equilibrium" label is WRONG.** The −$109k → +$128k flip is driven by a **fixed-price, partial-equilibrium capital-income-tax accounting correction**, NOT a general-equilibrium model. Clemens explicitly, repeatedly, and in his own words denies it is a GE effect. Factor prices/wages do **not** adjust endogenously — the entire point of the adjustment is that it holds factor prices fixed (the same fixed-price assumption used by the cash-flow accounting it corrects) and merely credits the immigrant with the capital-income taxes paid on the complementary capital that profit-maximizing firms must hire alongside the new worker. Confidence: **0.97** (primary-source verbatim, the author states the negation three separate times).

## EVIDENCE (verbatim, from the CGD Working Paper 632, Feb 2023 = CESifo WP 9464 / IZA DP 15592)

Three independent statements of the negation in Clemens's own text [SOURCE: https://www.cgdev.org/sites/default/files/fiscal-effect-immigration-reducing-bias-influential-estimates.pdf]:

1. **Abstract:** "A simple adjustment greatly reduces bias … conservatively accounting for capital taxes paid by the employers of immigrant labor. The adjustment is required by firms' profit-maximizing behavior, **unconnected to general equilibrium effects**."

2. **Introduction:** "It is to include conservative estimates of tax revenue from capital income caused by an immigrant worker's presence in the economy. **This is not a general equilibrium effect of immigration, because the effect occurs under the assumption of fixed prices** used by the fiscal flow accounting that currently dominates policy analysis. Rather, it is an important effect omitted by those influential, static estimates."

3. **The decisive sentence, immediately after equation (3) — the formula that produces the flip:** "The fiscal impact (3) **is not a macroeconomic long-run, general-equilibrium effect. It is an instantaneous static effect at partial equilibrium (fixed factor prices and productivity)**, an effect required by employers' profit maximization."

**Mechanism (also verbatim):** profit-maximizing firms that hire an additional worker "had not hired additional capital would have given up profit … buying an additional computer or renting additional retail space for the worker to use. That additional capital must generate additional capital income … This yields bounds on the consequent capital tax revenue caused by the worker's employment." NAS/Blau et al. (2017) implicitly assumed a capital share of zero (no complementary capital → no capital tax) and so omitted this revenue.

**The flip, verbatim:** "For the typical, marginal recent immigrant without a high school education, the adjustment changes the sign of lifetime net fiscal impact: from –$109,000 to at least +$128,000 without including children and grandchildren." And: "The corresponding estimate by Blau et al. (2017), omitting capital tax revenue, is –$109,000. That is, the bias induced by assuming a capital share of zero in equation (3) is sufficient to change the sign of the net impact."

**Why this is the OPPOSITE of GE — Clemens's own framing of the literature:** he positions his adjustment as a *third option* explicitly distinct from GE modeling: "methods based on **general equilibrium modeling** address bias with limited precision and transparency"; "The usual remedy in the literature, **general equilibrium models** of indirect effects, addresses bias at the cost of imprecision … sensitive to untestable assumptions. This paper proposes a third option, a simple adjustment …" The whole selling point is that it gets a bias correction *without* paying the GE price (untestable price-adjustment assumptions). Labeling it "GE" inverts the paper's central methodological claim.

**Note — the error cuts in the finding's FAVOR.** A fixed-price PE accounting correction rests on *fewer and weaker* assumptions than a GE estimate (it needs only firm profit-maximization + a capital reservation price, not an endogenous factor-price model). So calling it "GE" understated the result's robustness, not overstated it. The relabel makes the +$128k cell *more* defensible, not less.

**Distinguish from genuinely-GE neighbors in the same repo cell.** Colas & Sachs (2020/2024, "Indirect Fiscal Benefits of Low-Skilled Immigration," AEJ: Policy) — which the repo bundles into the same "M2 GE stack" — *is* a wage-structure/general-equilibrium channel (immigrants shift the native wage distribution → indirect fiscal effect). That one is correctly "GE." Clemens is a separate, fixed-price mechanism and must not be merged with it under one "GE" label. Peri's complementarity work is likewise a different (price-adjusting) channel. The repo's `immigration-lifetime-unified-theory-2026-06-15.md` §M2 currently fuses "Clemens / Colas-Sachs / Peri" into one "General-equilibrium offset" node — that fusion is the source of the mislabel.

## EXACT RELABEL PHRASE

Replace **"GE / general-equilibrium" (and "capital-tax GE")** for the Clemens adjustment with:

> **fixed-price partial-equilibrium capital-income-tax accounting correction**

Compact inline form where space is tight: **"partial-equilibrium capital-tax correction (Clemens, fixed factor prices)"**. Never "GE." If a one-word tag is needed, use **"PE-capital-tax"**, not "GE."

## CONTESTED STATUS — "published-but-contested," not settled

- **Publication tier:** Working paper, not peer-reviewed journal. Appears as CGD WP 632 (Feb 2023), CESifo WP 9464 (2021), IZA DP 15592 (2022). The author is pro-immigration (CGD), producing a pro-immigration result → source-incentive caution applies; cap confidence on the *magnitude* well below 0.95. [SOURCE: https://ideas.repec.org/p/ces/ceswps/_9464.html] [SOURCE: https://docs.iza.org/dp15592.pdf]
- **AEI rebuttal (Orrenius & Viard, "The Fiscal Impact of Immigration: An Update," Sept 2025):** finds overall immigrant fiscal impact positive **but driven by high-skilled immigrants**, with **low-skilled immigrants imposing a net fiscal cost** (like their US-born counterparts). They acknowledge indirect effects of low-skilled immigration are positive and "partly offset" the negative direct impact — i.e. they do **not** adopt Clemens's sign-flip to net-positive for the <HS cell. This is a direct, recent, substantive challenge to the +$128k conclusion. [SOURCE: https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf]
- **Direction is over-determined negative absent this one rule:** the +$128k is produced by Clemens's single adjustment applied to one NAS scenario; the NAS <HS fan and restrictionist estimates run negative. Accurate framing: "assumption-dependent; flips positive under a defensible fixed-price capital-tax rule, but that rule is published-but-contested (AEI 2025)."

## FILES IN REPO TO CORRECT (where the "GE" mislabel appears)

- `research/immigration-fiscal-welfare-ledger-map.md:26` — "flips to +$128k under capital-tax **GE** (Clemens)" → relabel.
- `research/immigration-lifetime-unified-theory-2026-06-15.md` §M2 (lines ~104–108, 177) — "**General-equilibrium** offset (Clemens / Colas-Sachs / Peri stack)" and "GE inclusion — M1 vs M2"; **split Clemens (PE) out of the GE node** (Colas-Sachs/Peri can stay GE).
- `research/immigration-interpreted-insights-2026-06-24.md:55,190` — already flags the mislabel and prescribes the same relabel; this check independently confirms it from primary source.
- Sweep any other "capital-tax GE" / "GE offset (Clemens)" occurrences (`rg -i "GE|general.equilibrium" research/ | rg -i clemens`).
