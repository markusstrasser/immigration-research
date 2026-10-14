// Isolated row-4 contract probe; no live inputs or outputs are read or written.
"use strict";
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");
const source = fs.readFileSync(path.join(__dirname, "row4_oct15.cjs"), "utf8");

function replay(measured, methodMismatch = false) {
  const edit = (v) => ({ side: "receipt", line: "modeled_owner_property", scenario: "cbo_collective",
    by: { personal: v, shared: v } });
  const input = { gates_failed: 0, edits: { set: [edit(measured)], cash: [edit(measured)] } };
  const payload = { meta: { adopted: "2026-10-15", allocation: { group_total: "personal" },
    items: [{ id: "row4_frame", applied: true, kind: "edit_set", edits: { first: 0, count: 1 } }] },
    edits: [edit(0.1)] };
  const specs = [{ allocation: "personal", end: 0 }, { allocation: "personal", end: 1 }];
  const api = { MAIN_SPECS: specs, METHODS: ["one", "two"], MAIN_PROFILE: "central",
    payloadModel: () => ({ move: 0 }),
    evaluateFull: (m, s) => ({ cost_bn: [100, 200][s.end] + m.move }),
    Engine: { applyCorrections: (m, p) => ({ move: m.move - p.edits[0].by.personal }) } };
  api.CASH = api;
  const summary = { v8: { end_specifications: {
    set: [[0, 1], methodMismatch ? [1, 0] : [0, 1]], cash: [[0, 1], [0, 1]],
  } }, main_case: [100, 200], cash_set: { band_bn: [100, 200] } };
  const writes = [];
  const fakeFs = {
    readFileSync(filename) {
      const name = path.basename(filename);
      if (name === "summary.json") return JSON.stringify(summary);
      if (name === "row4_oct15_inputs.json") return JSON.stringify(input);
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
        if (name === "path") return path;
        throw new Error(`unexpected require: ${name}`);
      },
    }, { filename: "row4_oct15.cjs" });
  } catch (error) { failure = error; }
  return { failure, writes };
}

const exact = replay(0.1);
assert.equal(exact.failure, undefined);
assert.equal(exact.writes.length, 2);
const result = JSON.parse(exact.writes[0].content);
assert.equal(result.tolerance_bn, 1e-9);
for (const set of Object.values(result.sets)) assert.deepEqual(set.residual_bn, [0, 0]);

const nonzero = replay(0.100000193243434);
assert.match(nonzero.failure?.message || "", /exhausts the measured cell shifts \(1e-9\)/);
assert.equal(nonzero.writes.length, 0, "failed cell gate must write no residual outputs");
const mismatch = replay(0.1, true);
assert.match(mismatch.failure?.message || "", /methods declare matching end specifications/);
assert.equal(mismatch.writes.length, 0, "method mismatch must write no oct15 outputs");
console.log("PASS: exact zero, nonzero cell rejection, method-end mismatch rejection; no live I/O");
