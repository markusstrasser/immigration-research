/* Price the v9 case's item arms in bounded child processes.
 *
 * Each arm is the whole adopted case with one item at that arm (package.cjs caseOf), priced on the case's
 * canonical cached route. That route keeps every variant base it builds; pricing all 81 arms in one process
 * peaked above 2.7 GB physical footprint on 2026-10-21, over the 2.5 GB budget. The uncached bounded route
 * (V9_CASE_CACHE=0) stays within memory but its correctionsPayload() differs from derived/corrections.json in
 * item 13's part metadata, so the engine's payload-identity gate rejects it. Children price a batch each on
 * the canonical route, check their own footprint and return exact doubles as JSON (round-trip exact).
 */
"use strict";
const path = require("path"), { spawnSync } = require("child_process");
const BATCH = 10;

function priceInChildren(pairs, log = () => {}) {
  const out = {};
  for (let at = 0; at < pairs.length; at += BATCH) {
    const batch = pairs.slice(at, at + BATCH), started = performance.now();
    const env = { ...process.env };
    delete env.V9_CASE_CACHE;      // the canonical cached route in every child
    const r = spawnSync(process.execPath, [__filename, ...batch.map(([item, arm]) => `${item}:${arm}`)],
      { env, encoding: "utf8", maxBuffer: 1 << 26 });
    if (r.status !== 0) throw Error(`[BLOCKED] item-arm child failed (${r.status}): ${(r.stderr || "").slice(-2000)}`);
    const lines = r.stdout.trim().split("\n"), prices = JSON.parse(lines[lines.length - 1]);
    for (const [item, arm] of batch) {
      const p = prices[`${item}:${arm}`];
      if (!p || ![p.band_bn, p.cash_bn].every((b) => Array.isArray(b) && b.length === 2 && b.every(Number.isFinite)))
        throw Error(`[BLOCKED] item-arm child returned no finite bands for ${item}:${arm}`);
      out[`${item}:${arm}`] = p;
    }
    log(`  item-arm child ${at / BATCH + 1}: ${batch.length} arms; wall ${((performance.now() - started) / 1000).toFixed(3)}s`);
  }
  return out;
}
module.exports = { priceInChildren, BATCH };

if (require.main === module) {
  const P = require("../main_case_2026_10_16/package.cjs"), out = {};
  if (process.env.V9_CASE_CACHE === "0") throw Error("[BLOCKED] item-arm child must use the canonical cached route");
  for (const token of process.argv.slice(2)) {
    const [item, arm] = token.split(":");
    if (!P.REGISTRY.find((x) => x.id === item)?.arms?.[arm]) throw Error(`[BLOCKED] unknown item arm ${token}`);
    const Q = P.caseOf(P.OCT05, P.CANDIDATE, { [item]: arm });
    out[token] = { band_bn: Q.central({}), cash_bn: Q.CASH.central({}) };
  }
  require("../main_case_2026_10_16/memory_guard.cjs").requireWithinBudget("break item-arm child");
  process.stdout.write(JSON.stringify(out) + "\n");
}
