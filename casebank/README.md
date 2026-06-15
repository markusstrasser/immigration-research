# Case banks — markdown files of specific cases

A case bank is a **markdown file**, one per type of thing, holding specific **verbatim** cases (the
actual example, not a summary) + provenance, plus an induced-**principles** section. Nothing fancier —
the only consumer is a model *reading* the file to induce principles, and markdown is what it reads
best. No schema, no jsonl, no tooling.

The two that already exist are the templates:
- `evals/critique_replay/cases.md` — review / defect traps
- `anim-workbench/docs/reports/3b1b-reference-bank.md` — capability targets

## The loop (why a bank is generative, not an archive)

Cases (concrete) → **induce a principle that compresses them** — explains many cases more cheaply than
listing them (up the ladder) → the principle predicts **new search directions** in regions not yet
looked at (down the ladder) → new finds get added → repeat. This is wake-sleep / DreamCoder; the
`Dreamer` reads the principles to generate, the `Heretic` attacks them.

**The one guard:** a principle earns its place only if it *compresses* the bank. A "principle" over 2–3
cases that just relabels them is a coincidence — the Heretic's job is to kill it (does it predict cases
it should *exclude*?). Collect cases cheaply, abstract only on compression, gate adversarially.

## Shape (the only convention)

Each bank file:
- `## Cases` — each: verbatim excerpt + provenance (`[SOURCE: …]` / `capture: verbatim|reconstructed`) + a one-line payload.
- `## Induced principles` — each: the principle + the cases it compresses + a falsifiable prediction.
- `## Revisions` — append-only; the history of belief change is calibration data.

`example-bank.md` shows it. Research grows its own banks per topic as real cases accumulate.
