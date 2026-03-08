# 2026-03-05: Adopt explicit causal DAG discipline for all regression specifications

## Context
The project accumulated multiple regression tables across NLSY79, NLSY97, PIAAC, and PISA that mixed nuisance controls, mediators, and descendants of treatment in the same models. The external review correctly identified that Stage A coefficients were being read as causal mediation when they were actually robustness checks with bad controls.

## Alternatives considered
1. **Continue observational attenuation tables** — Keep running "sex gap after controlling for X" regressions and interpret coefficient movement as suggestive. Pro: standard in the literature. Con: produces estimand confusion; coefficient movement from adding descendants is not identified mediation.
2. **Adopt DAG-first protocol** — Freeze a master causal graph, classify every variable as pre-treatment, mediator, or descendant, and only run admissible adjustment sets. Pro: prevents bad-control errors structurally. Con: slower, forces explicit causal commitment before running code.
3. **Switch to purely descriptive surface mapping** — Drop all causal language and only report stratified descriptive gaps. Pro: honest about what observational data can say. Con: gives up too much — some causal structure is identifiable.

## Decision
Option 2. Created three artifacts: analysis protocol (sign convention + frozen estimands), decisive causal tree (falsifiable node structure), and master DAG (ASCII causal graph with admissibility annotations). All future regression specifications must reference the DAG. The mediator-design memo explicitly freezes four distinct estimands (total effect, decomposition, direct effect, mechanism) to prevent slippage.

## Evidence
- Review-1 audit identified Stage A bad-control problem as the immediate trigger
- Master DAG forced time-slice acyclicity discipline
- Node table assigns kill/harden status and probability to each causal node
- Mediator-design memo: P(estimand confusion is main problem) = 0.86

Commits: decisive-causal-tree, analysis-protocol, master-dag, mediator-design (all 2026-03-05 to 2026-03-06)

## Revisit if
A natural experiment or RCT makes the DAG structure unnecessary for identification.

## Supersedes
None (previous work was implicitly observational).
