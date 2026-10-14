// Isolated contract probe: only frozen item-7 rounding admits 5e-7bn.
// All engine/closure gates stay 1e-9. No live I/O.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "ends_oct15.cjs"), "utf8");

function replay(raw, adopted = "2026-10-15") {
  const applied = 1.08644;
  const item = { id: "white_end_tax_keys", applied: true, kind: "edit_set",
    edits: { first: 0, count: 1 } };
  const payload = { meta: { adopted, allocation: { group_total: "personal" },
    items: [item], lineage: { members: { white: 1 } },
    white_end_tax_keys: { move_bn: { personal: applied } } }, edits: [{}] };
  const white = { case: "oct15", allocation: "personal", inputs_sha256: {}, csv_sha256: {},
    source_count: 1, raw_move_bn: raw, parts_bn: { federal_income_tax: raw },
    applied_move_bn: { accrual: applied, cash: applied },
    white_end_tax_keys_residual: Object.fromEntries(["accrual", "cash"].map((basis) =>
      [basis, { low: raw - applied, high: raw - applied }])) };
  const specs = [{ allocation: "personal", end: 0 }, { allocation: "personal", end: 1 }];
  const api = { MAIN_SPECS: specs, METHODS: ["one", "two"], MAIN_PROFILE: "central",
    payloadModel: () => ({ move: 0 }),
    evaluateFull: (m, s) => ({ cost_bn: [100, 200][s.end] + m.move }),
    expand: (edits) => edits,
    Engine: { applyCorrections: (m, p) => ({ move: m.move - p.edits[0].by.personal }) } };
  api.CASH = api;
  const summary = { v8: { end_specifications: { set: [[0, 1], [0, 1]], cash: [[0, 1], [0, 1]] } },
    main_case: [100, 200], cash_set: { band_bn: [100, 200] } };
  const writes = [];
  const fakeFs = {
    readFileSync(filename) {
      const name = path.basename(filename);
      if (name === "summary.json") return JSON.stringify(summary);
      if (name === "income_tax_keys_oct15_meta.json") return JSON.stringify(white);
      if (name === "main_case_bands.csv") return "profile,variant,cost_low_bn,cost_high_bn\n"
        + "central,adopted,100.0000,200.0000\ncentral,cash_set,100.0000,200.0000\n";
      if (["corrections.json", "corrections_cash.json"].includes(name)) return JSON.stringify(payload);
      throw new Error(`unexpected read: ${filename}`);
    },
    writeFileSync: (filename, content) => writes.push({ filename, content }),
  };
  let failure;
  try {
    vm.runInNewContext(source, {
      __dirname, console: { log() {} },
      require(name) {
        if (name === "fs") return fakeFs;
        if (name.endsWith("main_case_2026_10_15/package.cjs")) return api;
        if (["path", "crypto"].includes(name)) return require(name);
        throw new Error(`unexpected require: ${name}`);
      },
    }, { filename: "ends_oct15.cjs" });
  } catch (error) { failure = error; }
  return { failure, writes };
}

const exact = replay(1.08644);
assert.equal(exact.failure, undefined);
assert.equal(exact.writes.length, 2);
const result = JSON.parse(exact.writes[0].content);
assert.equal(result.zero_residual_tolerance_bn, 1e-9);
for (const set of Object.values(result.sets)) assert.deepEqual(set.residual_bn, [0, 0]);

const rounded = replay(1.086440193243434);
assert.equal(rounded.failure, undefined);
const roundingResult = JSON.parse(rounded.writes[0].content);
assert.equal(roundingResult.item7_rounding_tolerance_bn, 5e-7);
assert.equal(roundingResult.zero_residual_tolerance_bn, 1e-9);
const tooLarge = replay(1.0864406);
assert.match(tooLarge.failure?.message || "", /six-decimal carried value \(5e-7bn\)/);
assert.equal(tooLarge.writes.length, 0, "failed rounding gate must write no translation outputs");
const stale = replay(1.08644, "2026-10-14");
assert.match(stale.failure?.message || "", /adopted oct15 payload/);
assert.equal(stale.writes.length, 0, "stale case must write no oct15 outputs");
console.log("PASS: exact zero, six-decimal rounding acceptance, larger remainder rejection, stale-case rejection; no live I/O");
