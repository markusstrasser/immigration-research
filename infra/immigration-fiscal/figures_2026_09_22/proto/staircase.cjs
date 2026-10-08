/* Prototype data: the staircase the prototypes page opens with, for comparison. It is the figures page's
 * staircase as it stood on the September 24 case; that page has since moved to main case v6, and these
 * prototypes stay on September 24. The rows come from that page's figures.json at its last September 24
 * commit (account_sept24.cjs PINS.page). Gates: the main-case row is A.MAIN and the last row
 * A.PROPORTIONAL, the September 24 bands this account reproduces.
 */
"use strict";

function build(A) {
  const { gate, near, MAIN, PROPORTIONAL, pinned, path, HERE } = A;
  const fig = JSON.parse(pinned("page", path.join(HERE, "src", "generated", "figures.json")));
  const main = fig.staircase.find((s) => s.main).total, last = fig.staircase.at(-1).total;
  gate("main-case row = the September 24 band", near(main[0], MAIN[0], 1e-4) && near(main[1], MAIN[1], 1e-4), `${main[0]} to ${main[1]}`);
  gate("last row = the September 24 proportional band", near(last[0], PROPORTIONAL[0], 1e-4) && near(last[1], PROPORTIONAL[1], 1e-4),
    `${last[0]} to ${last[1]}`);
  return { staircase: fig.staircase, account: { breakEven: fig.account.breakEven, bySide: fig.account.bySide } };
}

module.exports = { build };
