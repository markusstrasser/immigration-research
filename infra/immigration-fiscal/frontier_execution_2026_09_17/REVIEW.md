# Validation and substantive code review

**Verdict:** Three material but bounded defects were found and corrected. The main Mexican/white survey comparisons and four matching Bracero wage results survive. Failed policy replications and source-access limits remain explicit.

The default external Cursor scout was rejected by automatic approval review because it would transmit private analysis source code to that service. No code was sent. A read-only in-session review covered all 14 then-existing Python scripts, with an independent policy subreview. Primary codebooks and source tables governed triage; style/refactoring suggestions were out of scope. A fifteenth script now provides the acquisition regression check.

| Finding | Correction | Validation and effect |
|---|---|---|
| Invalid NLS first-incarceration dates could leave an observed pre-30 zero | Mask only invalid-skip `-3` plus array-zero cases; preserve positive event evidence and distinct valid-skip `-4` | 11 exclusions, seven with positive wave weights, all other/unresolved identities. Focal Mexican/white comparisons unchanged. Validator checks unknown timing is not zero; official AFQT benchmark and 632 independent scalar checks rerun. |
| Bracero employment zero-fill missed absent rows | Build a separate 46-state by detected-report-month grid before filling domestic counts; retain missing whole reports | Adds 113 state-months; N becomes 8,970. Four wage anchors and independent FWL checks still pass. Employment still fails the printed anchor, so remains a diagnostic, not evidence for the published result. |
| Valid binary PDFs were decoded as HTML and falsely marked failed | Restrict HTML-link extraction to HTML filenames | `social/swiss/verify_acquisition.py` runs the actual acquisition script with offline mocked payloads. Valid binary PDF succeeds once; HTML under a PDF filename fails loudly and retains the response. No Swiss dataset acquisition is newly claimed. |

All original source snapshots remain unchanged. No external review, inaccessible official-package identity, successful Swiss replication or new causal welfare result is claimed. The scripts retain exact joins, explicit source discrepancy flags, survey-design and covariance bounds, and separate primary versus exploratory outcomes.

The review's meaningful residual limits are the underlying data: unresolved lineage/nonresponse, small event counts, administrative follow-up gaps, policy response/survival, and unverified official employment samples. Additional cosmetic review would not close those gaps.
