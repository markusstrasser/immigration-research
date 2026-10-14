// Oct15's remaining W-on-the-case-income-tax-keys residual, independently
// measured by the white lane. The historical held-out translation supplies the
// key's definition; its frozen files are inputs, never regenerated here.
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const F = path.resolve(__dirname, "..");
const OUT = path.join(__dirname, "derived");
const P = require(path.join(F, "main_case_2026_10_15/package.cjs"));
const J = (p) => JSON.parse(fs.readFileSync(p, "utf8"));
const S = J(path.join(F, "main_case_2026_10_15/derived/summary.json"));
const SOURCE = "white_replacement_2026_09_28/derived/income_tax_keys_oct15_meta.json";
const W = J(path.join(F, SOURCE));
const declaredEnds = S.v8.end_specifications;
const tolerance = 1e-9;
// Item 7 is inherited from frozen v7 at six decimals. Only its measured-vs-carried
// comparison admits half a final decimal unit; all engine/closure gates stay 1e-9.
const item7RoundingTolerance = 5e-7;
const item7RoundingReason = "Frozen v7 item 7 is carried at six decimals; half a final decimal unit is 5e-7bn.";
const gates = [];
function gate(name, pass, detail = "") {
  gates.push({ name, pass: Boolean(pass), detail });
  console.log(`GATE ${pass ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!pass) throw new Error(`[BLOCKED] ${name}: ${detail}`);
}
gate("raw key measurement is live oct15 at personal allocation", W.case === "oct15" && W.allocation === "personal");
for (const [relative, expected] of Object.entries({ ...W.inputs_sha256, ...W.csv_sha256 }))
  gate(`raw key source hash: ${relative}`, crypto.createHash("sha256").update(fs.readFileSync(path.join(F, relative))).digest("hex") === expected);
gate("raw W movement is the sum of its receipt parts (1e-12)", Number.isFinite(W.raw_move_bn)
  && W.parts_bn && Math.abs(Object.values(W.parts_bn).reduce((s, v) => s + v, 0) - W.raw_move_bn) <= 1e-12);
gate("v8 methods declare matching end specifications", ["set", "cash"].every((w) =>
  Array.isArray(declaredEnds[w]) && declaredEnds[w].length === P.METHODS.length
  && declaredEnds[w].every((pair) => Array.isArray(pair) && pair.length === 2
    && pair.every((i, end) => Number.isInteger(i) && i === declaredEnds[w][0][end]))));
const caseEnds = Object.fromEntries(["set", "cash"].map((w) => [w, declaredEnds[w][0]]));
gate("case ends are two personal specifications per set", ["set", "cash"].every((w) => Array.isArray(caseEnds[w]) && caseEnds[w].length === 2
  && caseEnds[w].every((i) => P.MAIN_SPECS[i] && P.MAIN_SPECS[i].allocation === "personal")));
const [header, ...csvRows] = fs.readFileSync(path.join(F, "main_case_2026_10_15/derived/main_case_bands.csv"), "utf8")
  .trim().split("\n").map((x) => x.split(","));
gate("case CSV has its declared columns", ["profile", "variant", "cost_low_bn", "cost_high_bn"].every((k) => header.includes(k)));
const bands = Object.fromEntries(csvRows.filter((r) => r[header.indexOf("profile")] === P.MAIN_PROFILE).map((r) => {
  const x = Object.fromEntries(header.map((k, i) => [k, r[i]]));
  return [x.variant, [Number(x.cost_low_bn), Number(x.cost_high_bn)]];
}));
const result = { case: "oct15", ends: caseEnds, allocation_at_end: { low: "personal", high: "personal" },
  source: SOURCE, tolerance_bn: tolerance, zero_residual_tolerance_bn: tolerance,
  item7_rounding_tolerance_bn: item7RoundingTolerance, item7_rounding_reason: item7RoundingReason, sets: {} };
for (const [which, basis, api, filename, bandRow] of [["set", "accrual", P, "corrections.json", "adopted"],
  ["cash", "cash", P.CASH, "corrections_cash.json", "cash_set"]]) {
  const ends = caseEnds[which];
  const payload = J(path.join(F, "main_case_2026_10_15/derived", filename));
  gate(`${which}: adopted oct15 payload`, payload.meta.adopted === "2026-10-15" && payload.meta.allocation.group_total === "personal");
  const item = payload.meta.items.find((x) => x.id === "white_end_tax_keys");
  if (item && item.applied) gate(`${which}: white_end_tax_keys is a registered edit set`, item.kind === "edit_set"
    && Number.isInteger(item.edits.first) && Number.isInteger(item.edits.count)
    && item.edits.first >= 0 && item.edits.first + item.edits.count <= payload.edits.length);
  gate(`${which}: raw W count is the case's W count (1e-9)`, Number.isFinite(W.source_count)
    && Math.abs(W.source_count - payload.meta.lineage.members.white) <= tolerance);
  const applied = item && item.applied ? payload.meta.white_end_tax_keys.move_bn.personal : 0;
  gate(`${which}: measurement subtracts the actual adopted item (1e-12)`, W.applied_move_bn
    && Math.abs(W.applied_move_bn[basis] - applied) <= 1e-12);
  const residual = W.white_end_tax_keys_residual && W.white_end_tax_keys_residual[basis];
  gate(`${which}: white measurement gives full-precision residuals`, residual
    && ["low", "high"].every((e) => Number.isFinite(residual[e])));
  gate(`${which}: residual equals raw movement minus applied item (1e-12)`, ["low", "high"].every((e) => Math.abs(residual[e] - (W.raw_move_bn - applied)) <= 1e-12));
  const model = api.payloadModel();
  const baseline = ends.map((i) => api.evaluateFull(model, api.MAIN_SPECS[i]).cost_bn);
  const oracle = which === "set" ? S.main_case : S.cash_set.band_bn;
  gate(`${which}: total matches the full-precision case (1e-9)`, baseline.every((v, i) => Math.abs(v - oracle[i]) <= tolerance));
  gate(`${which}: total matches main_case_bands.csv (5e-5: four decimal places)`, bands[bandRow]
    && baseline.every((v, i) => Number.isFinite(bands[bandRow][i]) && Math.abs(v - bands[bandRow][i]) <= 5e-5));
  if (item && item.applied) gate(`${which}: measured item-7 movement matches six-decimal carried value (5e-7bn)`,
    ["low", "high"].every((e) => Math.abs(residual[e]) <= item7RoundingTolerance),
    `${residual.low} / ${residual.high}; ${item7RoundingReason}`);
  const cost = ends.map((i, j) => {
    const move = residual[["low", "high"][j]];
    const edited = P.Engine.applyCorrections(model, { lines: [], edits: P.expand([
      { side: "receipt", line: "federal_income_tax", by: { personal: -move, shared: 0 } },
    ]) });
    return api.evaluateFull(edited, api.MAIN_SPECS[i]).cost_bn;
  });
  const priced = cost.map((v, i) => v - baseline[i]);
  gate(`${which}: engine prices the remaining receipt shift exactly (1e-9)`, priced.every((v, i) => Math.abs(v - residual[["low", "high"][i]]) <= tolerance));
  if (item && item.applied) gate(`${which}: priced residual beyond the declared item-7 rounding is zero (1e-9bn)`,
    priced.every((v) => Math.abs(v - (W.raw_move_bn - applied)) <= tolerance));
  result.sets[which] = { absorbed: Boolean(item && item.applied), baseline_bn: baseline, measured_residual_bn: residual,
    residual_bn: priced, residual_cost_bn: cost };
}
result.gates = gates;
fs.writeFileSync(path.join(OUT, "main_case_translation_oct15.json"), JSON.stringify(result, null, 1) + "\n");
const rows = ["case,set,end,spec,allocation,baseline_bn,residual_bn,residual_cost_bn"];
for (const [which, r] of Object.entries(result.sets)) for (let i = 0; i < 2; i++)
  rows.push(["oct15", which, ["low", "high"][i], caseEnds[which][i], "personal", r.baseline_bn[i], r.residual_bn[i], r.residual_cost_bn[i]].join(","));
fs.writeFileSync(path.join(OUT, "main_case_change_oct15.csv"), rows.join("\n") + "\n");
console.log(`[written] oct15 translation and residual CSV; ${gates.length} gates PASS`);
