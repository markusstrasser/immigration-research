# LLM Bias Caveat

This project uses frontier LLMs (primarily Claude) as the research instrument. The instrument is not neutral. This document describes the known biases and the mitigations applied.

## The mechanism

LLM post-training (RLHF, RLAIF, constitutional AI) is shaped by human annotators and preference models. The annotator pool skews young, educated, urban, and politically progressive. The model inherits those preferences — not as explicit rules but as soft priors on:

- What counts as "misleading" vs "differently framed"
- Which institutions get charitable vs adversarial interpretation
- Which claims are "conspiracy theories" vs "structural analysis"
- How eagerly to rate a claim FALSE when it comes from the political right vs left

This is not speculation. It is a documented property of RLHF pipelines across all frontier labs.

## Where it matters

The bias is **strongest** on topics where progressive and conservative framings diverge on the same underlying facts:

- Feminism, gender roles, family structure
- Race, policing, criminal justice
- Immigration policy
- Economic inequality and its causes
- Religion in public life
- Trans issues, gender identity
- Historical narratives about Western civilization

The bias is **weakest** on:

- Hard numerical claims (BLS data, NCES statistics, dates, quotes)
- Natural science, engineering, mathematics
- Programming, technical architecture
- Topics where left/right don't have competing frames

## How it manifests in practice

1. **Asymmetric "misleading" flags.** When a conservative speaker presents a real fact in a conservative frame, the model's instinct is "misleading" or "lacks context." When a progressive speaker does the same, the model's instinct is "true" or "well-established." The facts are identical; the frame triggers the rating.

2. **Asymmetric "conspiracy" labeling.** Network-based historical claims from the right ("elites coordinated these reforms") get labeled conspiratorial. Equivalent structural claims from the left ("systemic racism operates through institutional networks") do not. Both describe diffuse coordination among ideologically aligned actors.

3. **Benefit-of-the-doubt asymmetry.** Progressive institutions (academia, Planned Parenthood, civil rights organizations, the UN) get charitable readings by default. Conservative or traditionalist institutions (churches, anti-suffrage movements, traditional family structures) get adversarial readings by default.

4. **Eagerness asymmetry on FALSE.** When right-coded numbers are wrong, the model reaches for FALSE quickly. When left-coded numbers are equally squishy (wage gap formulations, "80% consumer spending," systemic racism statistics), the model defaults to MIXED or adds qualifiers.

5. **Tone policing as fact-checking.** The model sometimes rates a claim as false or misleading based on the speaker's *tone* or *implied conclusion* rather than the specific factual content. A blunt or inflammatory statement of a true fact gets downgraded; a diplomatically stated falsehood gets upgraded.

## Mitigations applied in this project

1. **`[⚠ FRAMING-SENSITIVE]` flag.** Any verdict that depends on framing interpretation rather than hard data gets flagged. The reader can then apply their own judgment about whose frame is more appropriate.

2. **Bias audit pass.** After initial fact-checking, a second pass reviews all verdicts for directional bias. Adjustments are documented with before/after ratings.

3. **Separate hard data from interpretation.** The epistemic standards (CLAUDE.md) require distinguishing empirical fact from contested evidence from opinion. This forces the model to separate "the number is wrong" (checkable) from "the framing is misleading" (judgment call).

4. **Steel-man requirement.** Before criticizing any position, present its strongest version. This counteracts the model's instinct to straw-man right-coded claims.

5. **Name the frame.** State whose perspective is being presented. Don't treat the progressive reading as the unmarked default.

## What this does NOT mean

- It does not mean the model's fact-checks are useless. Hard data verdicts are reliable.
- It does not mean every conservative claim is secretly correct. Many are genuinely wrong.
- It does not mean progressive claims are secretly wrong. Many are genuinely correct.
- It means: on the subset of claims where the verdict depends on *whose frame you trust*, this instrument has a thumb on one side of the scale. Weight accordingly.
