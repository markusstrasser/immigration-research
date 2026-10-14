/* Coverage input contract fixtures; never changes the parent's input file. */
"use strict";
const fs = require("fs"), path = require("path"), Module = require("module");
const file = path.join(__dirname, "coverage.cjs");
const source = fs.readFileSync(file, "utf8");
const original = JSON.parse(fs.readFileSync(path.join(__dirname, "_stub/coverage_bound_oct15.json"), "utf8"));
const clone = x => JSON.parse(JSON.stringify(x));
function fixture(data, live) {
  const bytes = JSON.stringify(data), mod = new Module(file, module);
  mod.filename = file;
  const req = mod.require.bind(mod);
  mod.require = id => id === "fs" ? {
    existsSync: p => live || String(p).includes("/_stub/"),
    readFileSync: () => bytes,
  } : req(id);
  mod._compile(source, file);
  return mod.exports;
}
const checks = [];
function check(name, fn) {
  fn(); checks.push({ name, pass: true }); console.log("PASS " + name);
}
function rejects(name, data, live, which, pattern) {
  check(name, () => {
    let error;
    try { fixture(data, live).get(which, "central", { stub: !live }); } catch (e) { error = e; }
    if (!error || !pattern.test(String(error))) throw Error("[BLOCKED] " + name + ": " + error);
  });
}
check("all ten original stub constructions retain generation/count closure", () => {
  for (const which of ["set", "cash"]) for (const arm of ["central", "da_middle", "da_low", "da_high", "pes_only"]) {
    const c = fixture(original, false).get(which, arm, { stub: true });
    if (!c.stub || !Number.isFinite(c.net_missing_people)) throw Error("[BLOCKED] stub fixture");
    for (const e of Object.values(c.by_end)) if (Math.abs(Object.values(e.by_generation).reduce((a,b)=>a+b,0)-e.total_bn)>1e-9) throw Error("[BLOCKED] generation closure");
  }
});
check("a missing live input stops both sets unless a fixture asks for the stub", () => {
  for (const w of ["set", "cash"]) {
    let error;
    try { fixture(original, false).get(w); } catch (e) { error = e; }
    if (!error || !/is absent/.test(String(error))) throw Error("[BLOCKED] implicit stub served for " + w + ": " + error);
  }
});
const live = { key: "oct15", sets: { set: clone(original), cash: clone(original) } };
check("explicit set/cash live schema accepted", () => {
  for (const w of ["set", "cash"]) if (fixture(live, true).get(w).stub) throw Error("[BLOCKED] live schema");
});
check("source decomposition retained with whole-case total explicitly scoped", () => {
  const data = clone(live), e = data.sets.set.scenarios.central.ends.low;
  e.decomposition = { total_cost_bn: e.total_bn ?? e.coverage_bn, line_parts: [{ source_side: "receipt", coverage_bn: -1 }] };
  e.case_with_coverage_bn = 123; e.cps_replicate_se_bn = 0.1;
  const got = fixture(data, true).get("set").by_end.low;
  if (JSON.stringify(got.decomposition) !== JSON.stringify(e.decomposition) || got.source_case_with_coverage_bn !== 123 || got.cps_replicate_se_bn !== 0.1 || Object.hasOwn(got,"case_with_coverage_bn")) throw Error("[BLOCKED] source part/provenance transport");
});
rejects("live case key required", { ...live, key: "oct14" }, true, "set", /not oct15/);
rejects("live cash prices required", { key: "oct15", sets: { set: original } }, true, "cash", /explicit cash prices/);
rejects("unknown accounting set rejected", original, false, "unknown", /unknown coverage accounting set/);
const failed = clone(original); failed.gates = { producer_control: false };
rejects("failed source control rejected", failed, false, "set", /failed gate/);
const badDecomposition = clone(original); badDecomposition.scenarios.central.ends.low.decomposition = {};
rejects("nonfinite decomposition total rejected", badDecomposition, false, "set", /decomposition does not close/);
for (const kind of ["extra_total", "missing_generation", "nonfinite_count"]) {
  const bad = clone(original), c = bad.scenarios.central.implied_net_missing_people;
  if (kind === "extra_total") c.total = Object.values(c).reduce((a,b)=>a+b,0);
  if (kind === "missing_generation") delete c.G2;
  if (kind === "nonfinite_count") c.G2 = null;
  rejects(kind, bad, false, "set", /count keys|count nonfinite/);
}
const mismatch = clone(original);
mismatch.scenarios.central.parts.low.G2.coverage_bn += 1;
rejects("generation dollars must close", mismatch, false, "set", /generation closure/);
fs.writeFileSync(path.join(__dirname, "derived/coverage_check.json"), JSON.stringify({ pass: true, checks }, null, 1)+"\n");
console.log(`coverage input PASS ${checks.length} checks; maxRSS ${process.resourceUsage().maxRSS} KiB`);
