# Lane brief: how much of Germany's PISA decline is immigration, and do natives fall where immigrant shares rise?

Date 2026-09-27, 23:58 JST. Parent session immigration-research-1c. The operator: "germany just had the worse
PISA results since PISA was created because of immigrants."

## Questions

1. **Germany.** From primary sources, collect PISA 2012, 2015, 2018 and 2022 means for students with and
   without an immigrant background (first and second generation separately where published). Collect the
   group shares too. Sources:
   - the OECD *PISA 2022 Results* volumes and their tables;
   - the German national report (Lewalter et al. 2023, *PISA 2022: Analyse der Bildungsergebnisse in
     Deutschland*);
   - the IQB-Bildungstrend 2021/2022 reports, which decompose composition.
   Then decompose each decline into the change within groups and the change in composition (shift-share,
   both weightings). Report how much of the 2018→2022 and 2012→2022 declines is composition. Quote each input
   in `reads/`.
2. **Did native-background students fall too, and by how much?** Separate the pandemic years from the trend
   where the sources allow.
3. **Across countries.** Take OECD countries with published splits. Relate the change in the immigrant-background
   share to the change in non-immigrant students' scores, 2012→2022 (and 2006→2022 if available). This is
   the system-level test that within-country peer designs cannot give. Report the slope with its SE, and the
   outliers.
4. **The European peer-effect literature.** For each of Brunello–Rocco, Schneeweis, Jensen–Rasmussen,
   Ohinata–van Ours, Geay–McNally–Telhaj, Ballatore et al., Tonello and Frattini–Meschi, give the design, the
   outcome measure (relative or absolute) and the effect on natives per 10 points of share.
5. **Verdict.** Is "because of immigrants" true, partly true or false for Germany's decline, and by how much?
   Steel-man it before testing it.

## Rules

- Work only in `infra/immigration-fiscal/pisa_germany_2026_09_27/`. Write `RESULT.md` first with
  `**Verdict:** pending` and append after each check, so a cut-off loses nothing.
- Verify every number against the primary text or table and quote it. The corpus is `~/Projects/corpus`; use the
  research MCP's `corpus_lookup` / `fetch_paper`. Firecrawl is out of credits: use Exa or direct HTTP, with no
  personal identifier in any request.
- Tag every number. Do not commit, stage or stash; the checkout is shared.
- Final message: the RESULT path and at most ten lines.
