/* Rebuild only v7's layer through its item API. Cells/parts stay fixed; item 6's
 * receipt responses follow the selected horizon. Run through engine_breaks_sept29.cjs. */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const F = path.join(__dirname, "..");
const clone = (x) => JSON.parse(JSON.stringify(x));
const MODES = ["fixed_capital", "whole", "corporate_only", "off"];
const block = (why) => { throw new Error(`[BLOCKED] first-year item 6: ${why}`); };

function calibration() {
  const c = JSON.parse(fs.readFileSync(path.join(__dirname, "derived/first_year_calibration.json"), "utf8"));
  const sha = crypto.createHash("sha256").update(fs.readFileSync(path.join(F, c.source))).digest("hex");
  if (sha !== c.sha256 || !(c.labor_share > 0 && c.labor_share < 1)
      || c.alpha !== 1 - c.labor_share || c.first_year_multiplier !== c.labor_share) {
    block("missing or stale production calibration; run first_year_calibration.py");
  }
  return c;
}

function multiplier(line, mode, c) {
  if (!MODES.includes(mode)) block(`unknown response mode ${mode}`);
  if (mode === "whole") return 1;
  if (mode === "off" || line === "remaining_production_property") return 0;
  if (mode === "corporate_only") return line.startsWith("corporate_") ? 1 : 0;
  return c.first_year_multiplier;
}

function packages(P, mode, c) {
  const B = P.OCT07;
  const ctx = { B, DETAIL: B.ITEM_DETAIL, LINEAGE_ITEM: B.LINEAGE_ITEM,
    Engine: P.Engine, MODEL: P.MODEL, METHODS: P.METHODS, readJson: P.readJson };
  const built = P.NEW_IDS.map((id) => {
    const item = P.REGISTRY.find((r) => r.id === id);
    if (item.kind === "allocation") return { item, arm: null };
    const build = (which) => {
      const x = item.build(ctx, null, which);
      if (id === "job_capital_taxes") {
        const m = x.meta.job_capital_taxes;
        m.first_year = { mode, calibration: clone(c), long_run_responses: clone(x.responses) };
        for (const [line, r] of Object.entries(x.responses)) {
          const factor = multiplier(line, mode, c);
          r.low *= factor;
          r.high *= factor;
          r.rule = `First-year ${mode}: ${factor} times the long-run response. ${r.rule}`;
          x.record.responses[line] = { low: r.low, high: r.high };
        }
        for (const line of Object.values(m.lines)) {
          const r = x.responses[line.model_lines[0]];
          line.response = { low: r.low, high: r.high };
        }
        for (const reading of ["low", "high"]) for (const a of ["personal", "shared"]) {
          const effect = Object.values(m.lines).reduce((t, l) => t + l.response[reading] * l.group_after_bn[a], 0);
          m.effect_at_reference_bn[reading][a] = effect;
          x.record.effect_at_reference_bn[reading][a] = effect;
        }
      }
      return P.checkBuilt7(item, x, which === "set" ? B : B.CASH, which);
    };
    return { item, arm: null, set: build("set"), cash: build("cash") };
  });
  const set = P.forItems7(B, built, "set", "variant", null, "personal");
  const cash = P.forItems7(B.CASH, built, "cash", "variant", null, "personal");
  return { set, cash, built };
}

module.exports = { MODES, calibration, multiplier, packages };
