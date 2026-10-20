// Check the row-4 measurement's remaining residual on the live oct16 case.
// First: node row4_oct07.cjs --export-row4 derived/row4_oct16_inputs.json
// Then: node row4_oct16.cjs
// An adopted row4_frame is subtracted from the independently measured cell
// shifts before pricing: applying the measurement a second time is forbidden.
"use strict";
const fs = require("fs");
const path = require("path");
const childProcess = require("child_process");
const F = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const P = require(path.join(F, "main_case_2026_10_16/package.cjs"));
const J = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const S = J(path.join(F, "main_case_2026_10_16/derived/summary.json"));
const I = J(path.join(OUT, "row4_oct16_inputs.json"));
const declaredEnds = S.v9.end_specifications;
const tolerance = 1e-9;
const gates = [];
function gate(name, pass, detail = "") {
  gates.push({ name, pass: Boolean(pass), detail });
  console.log(`GATE ${pass ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!pass) throw new Error(`[BLOCKED] ${name}: ${detail}`);
}
gate("measurement export passed every source gate", I.gates_failed === 0);
gate("v9 methods declare matching end specifications", ["set", "cash"].every((w) =>
  Array.isArray(declaredEnds[w]) && declaredEnds[w].length === P.METHODS.length
  && declaredEnds[w].every((pair) => Array.isArray(pair) && pair.length === 2
    && pair.every((i, end) => Number.isInteger(i) && i === declaredEnds[w][0][end]))));
const caseEnds = Object.fromEntries(["set", "cash"].map((w) => [w, declaredEnds[w][0]]));
gate("v9 ends are two personal specifications per set", ["set", "cash"].every((w) => Array.isArray(caseEnds[w]) && caseEnds[w].length === 2
  && caseEnds[w].every((i) => P.MAIN_SPECS[i] && P.MAIN_SPECS[i].allocation === "personal")));
const [header, ...csvRows] = fs.readFileSync(path.join(F, "main_case_2026_10_16/derived/main_case_bands.csv"), "utf8")
  .trim().split("\n").map((x) => x.split(","));
gate("case band CSV has its declared columns", ["profile", "variant", "cost_low_bn", "cost_high_bn"].every((k) => header.includes(k)));
const bands = Object.fromEntries(csvRows.filter((r) => r[header.indexOf("profile")] === P.MAIN_PROFILE).map((r) => {
  const x = Object.fromEntries(header.map((k, i) => [k, r[i]]));
  return [x.variant, [Number(x.cost_low_bn), Number(x.cost_high_bn)]];
}));
// Headers are discovered rather than assumed; fail loudly on a contract change.
const keyOf = (e) => `${e.side}|${e.line}|${e.side === "receipt" ? e.scenario : e.key}`;
function aggregate(edits) {
  const out = new Map();
  for (const e of edits) {
    gate(`cell-shift measurement ${keyOf(e)}`, ["receipt", "spending"].includes(e.side)
      && e.by && !Object.hasOwn(e, "national_bn") && ["personal", "shared"].every((a) => Number.isFinite(e.by[a])));
    const k = keyOf(e);
    if (!out.has(k)) out.set(k, { ...e, by: { personal: 0, shared: 0 } });
    for (const a of ["personal", "shared"]) out.get(k).by[a] += e.by[a];
  }
  return out;
}
const result = { case: "oct16", end_specifications: caseEnds, tolerance_bn: tolerance, sets: {} };
for (const [which, api, filename, bandRow] of [["set", P, "corrections.json", "adopted"],
  ["cash", P.CASH, "corrections_cash.json", "cash_set"]]) {
  const ends = caseEnds[which];
  const payload = J(path.join(F, "main_case_2026_10_16/derived", filename));
  gate(`${which}: adopted oct16 payload`, P.STATUS === "adopted" && P.ADOPTED
    && payload.meta.adopted === P.ADOPTED
    && payload.meta.allocation.group_total === "personal");
  const item = payload.meta.items.find((x) => x.id === "row4_frame");
  const expected = aggregate(I.edits[which]);
  let applied = new Map();
  if (item && item.applied) {
    gate(`${which}: registered row4_frame is an edit set`, item.kind === "edit_set"
      && Number.isInteger(item.edits.first) && Number.isInteger(item.edits.count)
      && item.edits.first >= 0 && item.edits.first + item.edits.count <= payload.edits.length);
    applied = aggregate(payload.edits.slice(item.edits.first, item.edits.first + item.edits.count));
  }
  const residual = [];
  for (const k of new Set([...expected.keys(), ...applied.keys()])) {
    const e = expected.get(k), a = applied.get(k);
    residual.push({ ...(e || a), by: Object.fromEntries(["personal", "shared"].map((alloc) =>
      [alloc, (e ? e.by[alloc] : 0) - (a ? a.by[alloc] : 0)])) });
  }
  const maxCellResidual = Math.max(0, ...residual.flatMap((e) => Object.values(e.by).map(Math.abs)));
  if (item && item.applied) gate(`${which}: adopted row4_frame exhausts the measured cell shifts (1e-9)`, maxCellResidual <= tolerance,
    maxCellResidual.toExponential(3));
  const model = api.payloadModel();
  const baseline = ends.map((i) => api.evaluateFull(model, api.MAIN_SPECS[i]).cost_bn);
  const oracle = which === "set" ? S.main_case : S.cash_set.band_bn;
  gate(`${which}: live total matches the full-precision case band (1e-9)`, baseline.every((v, i) => Math.abs(v - oracle[i]) <= tolerance));
  gate(`${which}: live total matches main_case_bands.csv (5e-5: four decimal places)`, bands[bandRow]
    && baseline.every((v, i) => Number.isFinite(bands[bandRow][i]) && Math.abs(v - bands[bandRow][i]) <= 5e-5),
    `${baseline.join(" / ")}; row ${bandRow}`);
  const measured = P.Engine.applyCorrections(model, { lines: [], edits: residual });
  const cost = ends.map((i) => api.evaluateFull(measured, api.MAIN_SPECS[i]).cost_bn);
  const move = cost.map((v, i) => v - baseline[i]);
  if (item && item.applied) gate(`${which}: measured residual on oct16 is zero (1e-9)`, move.every((v) => Math.abs(v) <= tolerance), move.join(" / "));
  result.sets[which] = { absorbed: Boolean(item && item.applied), baseline_bn: baseline, residual_bn: move,
    residual_cost_bn: cost, maximum_cell_residual_bn: maxCellResidual, residual_edits: residual };
}
result.gates = gates;
const memory = JSON.parse(childProcess.execFileSync("uv", ["run", "--no-project", "python3",
  path.join(F, "main_case_2026_10_16/memory_for_pid.py"), String(process.pid),
  String(process.resourceUsage().maxRSS)], { encoding: "utf8" }));
gate("principal lifetime physical footprint is within the canonical budget", memory.pass === true);
console.log(`[memory] ${memory.metric}: ${memory.peak_bytes} bytes; limit ${memory.limit_bytes}`);
fs.writeFileSync(path.join(OUT, "row4_oct16.json"), JSON.stringify(result, null, 1) + "\n");
const rows = ["case,set,end,spec,baseline_bn,residual_bn,residual_cost_bn"];
for (const [which, r] of Object.entries(result.sets)) for (let i = 0; i < 2; i++)
  rows.push(["oct16", which, ["low", "high"][i], caseEnds[which][i], r.baseline_bn[i], r.residual_bn[i], r.residual_cost_bn[i]].join(","));
fs.writeFileSync(path.join(OUT, "row4_oct16.csv"), rows.join("\n") + "\n");
console.log(`[written] row4_oct16.json, row4_oct16.csv; ${gates.length} gates PASS`);
