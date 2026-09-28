---
date: 2026-09-29
concepts: [repo-organization, provenance, supersession]
status: adopted
supersedes: []
relations:
  - revises: decisions/2026-09-05-material-inference-repair.md
evidence: doc inventory (session 95a94bd8 scratchpad `doc_inventory/RESULT.md`, pinned at f1f2001; reruns byte-identical)
---

# 2026-09-29: Delete superseded and cruft documents; rewrite living documents to current (adopted)

## Context

Since the September 5 repair, superseded memos stayed in `research/` with their bodies kept below a
`historical-snapshot` marker, and the INDEX listed them in a Historical table. Living documents (the INDEX, the
objections FAQ, the register, topic memos) grew by stacking dated brackets and earlier cases above the current one.
Readers and agents kept picking up stale numbers from both.

The operator asked on 2026-09-29: "Also you can delete cruft or like overturned assumptions in memos ... I guess
it's still in github anyways? Like what's the best organization of the repo / system etc". The constitution lists
"delete research files" under "Never without human"; this is the human's go for this cleanup.

## Alternatives considered

1. **Keep marking and routing** (the September 5 rule). Nothing is lost, but readers still land on superseded
   bodies, and the INDEX keeps a 47-row Historical table.
2. **Move superseded files to an archive folder.** Links still resolve, but the archive is a second tree that
   search tools and agents read as current.
3. **Delete superseded and cruft files, keep records, rewrite living documents** (chosen).

## Decision

- **Documents fall into three kinds.**
  - Living documents state the current position (INDEX, FAQ, register, topic memos, map). They are rewritten to
    current, with a Revisions footer for claim changes.
  - Records (decision records, ladder entries, lane RESULTs, dated audits and dated findings that still stand) are
    never rewritten or deleted.
  - Superseded and cruft documents are deleted.
- **This cleanup deletes 59 files** (14 cruft, 45 superseded; 14,369 lines). Each one's living links are
  repointed in the same change.
- **A tombstone table closes the dead links.** The INDEX lists each deleted path with its last commit and
  successor. Records that link to a deleted file keep the dead link; the table resolves it with
  `git show <last commit>:<path>`.
- **Three superseded files stay.** Two are builder specs that code cites (`verified-findings-report-2026-04-10`,
  `net-negative-dataset-frontier-2026-06-15`), and a HUMAN.md link holds `theory-verdicts-2026-06-25`.
- **Six snapshot memos are trimmed** to the corrected assessment above their marker, in a separate change.
- **Nothing is lost from GitHub.** Every deleted file's last version is byte-identical on origin/main (9a73476),
  checked with `git rev-parse` for all 59.

## Evidence

The inventory classified all 341 in-scope documents at f1f2001 and counted, for each file:
- living links, record links and review-artifact links;
- agent reads from agentlogs;
- code that opens or names it.

No deleted file is opened by code. Comments and SQL `-- backs:` headers that name one are repointed to the git
revision.

## Revisit if

- A deleted file turns out to be opened by code or cited as current by a living document.
- The operator wants deleted records restored.

## Open

The constitution (CLAUDE.md "Never without human") and GOALS.md ("Deletion of research files") still carry the old
rule. Changing them is the operator's call; new wording is proposed to him, not edited.
