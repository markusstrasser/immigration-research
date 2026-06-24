# Path to `-$200k` per Person — Scenario Audit

**Question:** What would it take to get to a `-$200k` lifetime fiscal/social cost per unauthorized immigrant without presupposing the result?
**Date:** 2026-03-13
**Purpose:** This memo is adversarial. It does not assume `-$200k` is wrong. It asks what arithmetic and what assumptions are required to get there.

---

## 1. The Arithmetic Hurdle

To reach `-$200k` NPV per person, the implied **annual net deficit** has to be:

| Horizon | 0% | 3% | 7% |
|---|---:|---:|---:|
| 10 years | `-$20,000` | `-$23,446` | `-$28,476` |
| 25 years | `-$8,000` | `-$11,486` | `-$17,162` |
| 75 years | `-$2,667` | `-$6,734` | `-$14,088` |

These are the bars any `-$200k` story must clear. If a proposed channel stack does not add up to those annual deficits, the scenario fails arithmetically.

---

## 2. What the Source-Backed Annual Numbers Actually Look Like

### State and local

CBO's 2025 report on the post-2021 surge gives:

- direct net state/local cost: about `-$2,140` per person in 2023, [SOURCE: https://www.cbo.gov/publication/61256]
- potential net state/local cost: about `-$2,279` per person in 2023, [SOURCE: https://www.cbo.gov/publication/61256]
- direct state/local spending: about `$4,488` per person, [SOURCE: https://www.cbo.gov/publication/61256]
- potential state/local spending: about `$6,651` per person. [SOURCE: https://www.cbo.gov/publication/61256]

### Taxes

ITEP's all-unauthorized estimate gives:

- taxes paid per person: about `$8,889` per year, [SOURCE: `research/immigration-fiscal-impact-unauthorized-memo.md`] [SOURCE: https://itep.org/undocumented-immigrants-taxes-2024/]
- pessimistic case: about `$7,927` per year. [SOURCE: https://itep.org/undocumented-immigrants-taxes-2024/]

### Federal

CBO's 2024 federal report says the immigration surge **reduced** the federal deficit over 2024-2034. [SOURCE: https://www.cbo.gov/publication/60569]

That means a `-$200k` scenario must overcome not just state/local negative effects, but also the fact that the federal side is not negative in the baseline CBO accounting.

---

## 3. First Pass: What If We Use Only Observed Negative Flows?

Using annual negative flows and ignoring all offsets:

| Annual flow used as if it persisted | 25y @ 3% NPV | 75y @ 3% NPV | Status |
|---|---:|---:|---|
| CBO direct net state/local cost `-$2,140` | `-$37k` | `-$64k` | Sourced |
| CBO potential net state/local cost `-$2,279` | `-$40k` | `-$68k` | Sourced |
| CBO potential state/local spending `-$6,651` treated as net cost | `-$116k` | `-$198k` | **Mis-specified** |

This table shows something important:

- If you use **net** state/local costs, you do **not** get close to `-$200k`.
- You get near `-$200k` only if you use **gross spending** (`$6,651`) as though it were **net cost**, and persist it for 75 years.

That is not a neutral move. It throws away taxes and other offsets.

---

## 4. The Main Paths to `-$200k`

### Path A: Gross-spending-only path

**Mechanism**

1. Take CBO potential state/local spending per person (`$6,651`).
2. Treat it as if it were net annual loss.
3. Ignore taxes paid and federal positive effects.
4. Persist it for 75 years at 3%.

**Result**

Roughly `-$198k`, which is effectively the target.

**Audit**

| Component | Status |
|---|---|
| CBO spending number | **Sourced** |
| Recasting spending as net loss | **Invented / invalid accounting move** |
| Ignoring taxes paid | **One-sided assumption** |
| 75-year persistence | **Inference** |

**Verdict**

Arithmetically viable, but only because it confuses spending with net cost.

---

### Path B: Heritage-style household path

Heritage is summarized in the repo memo as roughly `$20,000/year` net cost **per illegal-immigrant household**. [SOURCE: `research/immigration-fiscal-impact-unauthorized-memo.md`]

At 25 years and 3%, `$20,000/year` implies about `-$348k` NPV **per household**.

To turn that into `-$200k per person`, you are implicitly assuming about `1.74 persons per household`.

**Audit**

| Component | Status |
|---|---|
| Heritage household figure | **Sourced in repo memo; needs primary-source verification before reuse** |
| Household-to-person conversion | **Inference** |
| Average-cost public goods allocation | **Methodological choice, sourced as a category** |
| Child-cost-only accounting | **Methodological choice, one-sided if child contributions omitted** |

**Verdict**

This is the cleanest rhetorical route to `-$200k`, but it leans heavily on unit conversion plus one-sided accounting choices.

---

### Path C: Average-cost plus child-cost-only path

This is the classic restrictionist route:

1. allocate average public goods per capita,
2. include citizen-child K-12 and transfer costs,
3. exclude children's adult tax contributions,
4. use a short or medium horizon,
5. do not credit macro federal offsets.

The repo's fiscal memo identifies this as the combination that most strongly drives negative results. [SOURCE: `research/immigration-fiscal-impact-unauthorized-memo.md`]

**Audit**

| Component | Status |
|---|---|
| Average vs marginal public-goods choice is outcome-determining | **Sourced** |
| One-sided child accounting flips sign | **Sourced** |
| Exact per-person annual amount needed to hit `-$200k` | **Not in current documents** |

**Verdict**

Conceptually plausible as a path to very negative numbers. But the current source set still does not give a clean sourced per-person route to `-$200k`.

---

### Path D: Full-spectrum pessimistic stack

This is the strongest non-advocacy attempt to reach `-$200k`:

1. start from CBO potential net state/local cost (`-$2,279/year`), [SOURCE: https://www.cbo.gov/publication/61256]
2. haircut taxes toward the pessimistic ITEP case, [SOURCE: https://itep.org/undocumented-immigrants-taxes-2024/]
3. add language-access overhead, court friction, housing/code-enforcement burden, and informal-economy tax erosion,
4. add political backlash / redistribution effects.

The problem is arithmetic. At 25 years and 3%, you need `-$11,486/year`.

If you start at `-$2,279/year`, you still need an extra `-$9,207/year`.

That extra negative flow has to come from channels that are mostly **real but not cleanly monetized** in the current evidence base.

**Audit**

| Component | Status |
|---|---|
| CBO potential net state/local cost | **Sourced** |
| ITEP pessimistic taxes | **Sourced** |
| Language-access per-person national annual cost | **Not in documents** |
| Court-friction per-person annual cost | **Not in documents** |
| Housing/code enforcement per-person annual cost | **Not in documents** |
| Informal-economy tax erosion per-person annual cost | **Not in documents** |
| Redistribution backlash dollarization | **Invented unless separately modeled** |

**Verdict**

This path is not ruled out, but the numbers required are much larger than the source-backed add-on channels currently justify.

---

## 5. What a Neutral Reader Should Conclude

### Strong conclusions

- `-$200k` is **arithmetically possible**.
- It is **not** reachable from the cleanest observed net-cost numbers alone.
- To get there, you must do at least one of the following:
  - treat gross spending as net loss,
  - convert household figures to person figures,
  - use average-cost public goods and one-sided child accounting,
  - add large partially measured or unmeasured long-tail costs.

### Weak conclusions

- You cannot currently say `-$200k` is the **best estimate** from the source-backed evidence.
- You also cannot say it is literally impossible.

The right summary is:

`-$200k` is a **scenario with a heavy assumption stack**, not a number that falls directly out of the measured data.

---

## 6. Assumption Ledger

| Assumption | Type | Needed for `-$200k`? | Comment |
|---|---|---|---|
| State/local direct and potential net costs are negative | Sourced | Yes, but insufficient alone | Real base layer |
| Federal budget effects are net positive | Sourced | Yes, as an obstacle | Must be offset or ignored |
| Taxes are well below ITEP pessimistic case for the target population | Inference | Often | Possible, but not yet observed cleanly for unauthorized Mexicans specifically |
| Average public-goods allocation is the right framework | Methodological choice | Usually | Legitimate as a scenario, not neutral default |
| Citizen children's costs belong in the immigrant ledger | Methodological choice | Usually | Reasonable if paired with child lifetime contributions |
| Citizen children's contributions can be omitted | One-sided assumption | Usually | This is the major distortion |
| Language access, court backlog, and housing strain are large enough to add several thousand dollars per year per person | Mostly unmeasured | Often | Real channels, weak current dollarization |
| Political backlash and trust effects can be monetized per immigrant | Invented unless modeled | Sometimes | Weakest part of aggressive negative scenarios |

---

## Best Current Judgment

If you want to argue for `-$200k`, the intellectually honest way is:

1. call it a **pessimistic scenario**,
2. show the annual hurdle,
3. state which channels are sourced, inferred, and invented,
4. admit that the number depends more on accounting choices and weakly measured long-tail channels than on direct observation.

That does not make the scenario useless. It makes it what it is: a high-negative stress test, not an unbiased estimate.
