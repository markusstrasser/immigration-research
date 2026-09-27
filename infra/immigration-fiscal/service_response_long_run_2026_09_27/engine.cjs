/* Step 2 of this lane (BRIEF.md): the main case's 64 specifications with long-run responses for the
 * economic-affairs and recreation lines.
 *
 * The main case (main_case_schools_full_2026_09_26/package.cjs, imported unchanged) holds both lines at
 * zero response (profile cbo_category_lag_non_school_full: delayed 0). This script sets each line's
 * response through the engine's own per-line route, state.response_override[line id], at the
 * amount-weighted blend of its subfunctions' responses (derived/responses.json, from build.py). The
 * blend is exact because every subfunction of a line shares the line's allocation key; a second path
 * splits each line into its subfunction lines in a lane-local copy of the corrected model and must
 * agree at every specification.
 *
 * Gates (exit 1 and nothing written on failure):
 * - at the old responses the lane's cost function equals the package's cost() at every specification
 *   and fill-in method, and the band is the adopted $258.4885–291.9548bn (summary.json) to 1e-6;
 * - the split-line model gives the same cost as the blended responses at every specification (1e-9),
 *   at the old, low and high responses;
 * - a third path, the package's cost() plus response x the group's amount (the engine is linear),
 *   agrees at every specification (1e-9);
 * - the cost rises with the responses, so the band's low end takes the low responses and its high end
 *   the high responses.
 *
 * The candidate band crosses the 64 specifications with the two readings (low, high): its low end is
 * the minimum at the low responses and its high end the maximum at the high responses, each averaged
 * over the two fill-in methods as the main case's central() does. Moves are reported at fixed
 * specifications, never as differences of band ends.
 *
 * Run from anywhere: node infra/immigration-fiscal/service_response_long_run_2026_09_27/engine.cjs
 * Writes derived/per_spec_costs.csv, derived/candidate_band.json, derived/gates_engine.json.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const P = require(path.join(FISCAL, "main_case_schools_full_2026_09_26", "package.cjs"));
const { P26, Engine, METHODS, STACKS, MAIN_SPECS, PROFILES, MAIN_PROFILE, SYN, ALLOCS } = P;
const RESP = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "responses.json"), "utf8"));
const SUMMARY = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_schools_full_2026_09_26", "derived", "summary.json"), "utf8"));
const LINES = ["economic_affairs_services", "recreation_culture"];
const READINGS = ["low", "high"];

const gates = [];
function gate(name, ok, detail) {
  gates.push({ gate: name, passed: !!ok, detail: detail || "" });
  console.log(`  ${ok ? "PASS" : "FAIL"} ${name}${detail ? " — " + detail : ""}`);
}
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;

// The main case's corrected model per fill-in method, exactly as main_case_schools_full_2026_09_26/main_case.cjs
// builds it (its `models`).
const MODELS = METHODS.map((m) => P26.build(P26.packageShifts(STACKS[`row4+status_state_aware|central|${m}`], "central", m,
  P26.CENTRAL), P26.CENTRAL));

// The package's cost() (main_case_2026_09_24/package.cjs), with the two lines' responses set per line.
// `extra` adds response overrides for lines that only the split model has.
function costAt(m, spec, lineResponses, extra) {
  const pr = PROFILES[MAIN_PROFILE];
  const school = pr.school === null ? spec.school : pr.school;
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = m.receipts.reference;
  s.production.normalization = spec.normalization;
  s.count_production = true;
  s.general_government_response = spec.gg;
  s.key_override = { public_order_safety: spec.justice, medicaid_and_chip_other_medical: spec.uc };
  s.response_override = {
    education_services: spec.share * school + (1 - spec.share) * pr.other,
    public_order_safety: 1, health_services: 1, income_security_services: 1,
    housing_community_services: 1, economic_affairs_services: pr.delayed, recreation_culture: pr.delayed,
    [SYN.school]: spec.share * school, [SYN.college]: (1 - spec.share) * pr.other, [SYN.constants]: 1,
  };
  if (lineResponses) for (const id of LINES) s.response_override[id] = lineResponses[id];
  Object.assign(s.response_override, extra || {});
  return -Engine.evaluate(m, s).welfare_bn;
}
const blended = (reading) => Object.fromEntries(LINES.map((id) => [id, RESP.lines[id].response[reading]]));
const OLD = Object.fromEntries(LINES.map((id) => [id, PROFILES[MAIN_PROFILE].delayed]));

// The group's amount on a line in a model: the preferred key's cell (cost() overrides keys only for
// public order and Medicaid).
const amount = (m, id, allocation) => {
  const line = m.spending.lines.find((l) => l.id === id);
  return line.keys[line.preferred_key][allocation].target_bn;
};

// Split-line copy of a corrected model: each line becomes its subfunction lines, every key cell scaled
// by the subfunction's share of the line's national amount (target and other alike, share unchanged).
function splitModel(m) {
  const c = Engine.clone(m);
  const out = [];
  for (const line of c.spending.lines) {
    if (!LINES.includes(line.id)) { out.push(line); continue; }
    for (const sf of RESP.lines[line.id].subfunctions) {
      const keys = {};
      for (const [k, cells] of Object.entries(line.keys)) {
        keys[k] = {};
        for (const a of ALLOCS) {
          keys[k][a] = { target_bn: cells[a].target_bn * sf.share_of_line, other_bn: cells[a].other_bn * sf.share_of_line, share: cells[a].share };
        }
      }
      out.push(Object.assign({}, line, { id: `${line.id}__${sf.id}`, national_bn: line.national_bn * sf.share_of_line, keys }));
    }
  }
  c.spending.lines = out;
  return c;
}
const SPLIT = MODELS.map(splitModel);
const splitOverrides = (reading) => {
  const o = {};
  for (const id of LINES) for (const sf of RESP.lines[id].subfunctions) o[`${id}__${sf.id}`] = reading === "old" ? OLD[id] : sf.response[reading];
  return o;
};

// ---------------------------------------------------------------------------------------------------
console.log("[gates: reproduction at the old responses]");
const specs = MAIN_SPECS;
gate("the main case has 64 specifications", specs.length === 64, `${specs.length}`);
const pkg = MODELS.map((m) => specs.map((spec) => P.cost(m, spec, MAIN_PROFILE)));
const old = MODELS.map((m) => specs.map((spec) => costAt(m, spec, OLD)));
gate("the lane's cost function equals the package's cost() at every specification and method (old responses)",
  old.every((xs, i) => xs.every((x, j) => x === pkg[i][j])), "exact");
const bandOf = (costs, pick) => [0, 1].map((e) => mean(costs.map((xs) => (e === 0 ? Math.min : Math.max)(...xs))));
const oldBand = bandOf(old);
const adopted = P.central({});
gate("the band at the old responses is the adopted main case (summary.json) to 1e-6",
  near(oldBand[0], SUMMARY.main_case[0], 1e-6) && near(oldBand[1], SUMMARY.main_case[1], 1e-6)
  && near(adopted[0], SUMMARY.main_case[0], 1e-6) && near(adopted[1], SUMMARY.main_case[1], 1e-6),
  `${oldBand[0].toFixed(6)} / ${oldBand[1].toFixed(6)}`);
const endIdx = (xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))];
const oldEnds = old.map(endIdx);
const pubEnds = SUMMARY.school.end_specifications.average.map((x) => [x.low_end.index, x.high_end.index]);
gate("the old end specifications are the published ones (48 and 11)", JSON.stringify(oldEnds) === JSON.stringify(pubEnds),
  JSON.stringify(oldEnds));

console.log("\n[gates: three paths agree]");
const costs = {};
for (const reading of READINGS) costs[reading] = MODELS.map((m) => specs.map((spec) => costAt(m, spec, blended(reading))));
for (const reading of ["old", ...READINGS]) {
  const split = SPLIT.map((m) => specs.map((spec) => costAt(m, spec, null, splitOverrides(reading))));
  const ref = reading === "old" ? old : costs[reading];
  const worst = Math.max(...split.flatMap((xs, i) => xs.map((x, j) => Math.abs(x - ref[i][j]))));
  gate(`split-line model = blended line responses (${reading})`, worst <= 1e-9, `max |diff| ${worst.toExponential(2)}`);
}
for (const reading of READINGS) {
  const r = blended(reading);
  const worst = Math.max(...MODELS.flatMap((m, i) => specs.map((spec, j) =>
    Math.abs(pkg[i][j] + LINES.reduce((a, id) => a + r[id] * amount(m, id, spec.allocation), 0) - costs[reading][i][j]))));
  gate(`package cost + response x group amount = engine (${reading})`, worst <= 1e-9, `max |diff| ${worst.toExponential(2)}`);
}
gate("cost rises with the responses at every specification (low < high)",
  costs.low.every((xs, i) => xs.every((x, j) => x < costs.high[i][j] && x > old[i][j])), "old < low < high");

// ---------------------------------------------------------------------------------------------------
console.log("\n[candidate]");
const lowEnds = costs.low.map(endIdx), highEnds = costs.high.map(endIdx);
const candidate = [mean(costs.low.map((xs) => Math.min(...xs))), mean(costs.high.map((xs) => Math.max(...xs)))];
const atLowOnly = bandOf(costs.low), atHighOnly = bandOf(costs.high);
// Moves at fixed specifications: each method's end specification, averaged over methods.
const moveAt = (reading, which) => mean(MODELS.map((_, i) => {
  const j = oldEnds[i][which === "low" ? 0 : 1];
  return costs[reading][i][j] - old[i][j];
}));
const move = { low_end_spec_low_responses: moveAt("low", "low"), high_end_spec_high_responses: moveAt("high", "high"),
  low_end_spec_high_responses: moveAt("high", "low"), high_end_spec_low_responses: moveAt("low", "high") };
gate("the candidate's end specifications are the main case's (48 low, 11 high)",
  JSON.stringify(lowEnds.map((x) => x[0])) === JSON.stringify(oldEnds.map((x) => x[0]))
  && JSON.stringify(highEnds.map((x) => x[1])) === JSON.stringify(oldEnds.map((x) => x[1])),
  `low ${lowEnds.map((x) => x[0])}, high ${highEnds.map((x) => x[1])}`);
gate("band move equals the move at the fixed end specifications (same end specifications)",
  near(candidate[0] - oldBand[0], move.low_end_spec_low_responses, 1e-9) && near(candidate[1] - oldBand[1], move.high_end_spec_high_responses, 1e-9));

// Contributions by subfunction at the end specifications: response x share of line x group amount,
// averaged over methods (linear, so they add to the move).
const endSpec = (which) => oldEnds.map((e) => specs[e[which === "low" ? 0 : 1]]);
const contributions = [];
for (const id of LINES) {
  for (const sf of RESP.lines[id].subfunctions) {
    const row = { line: id, id: sf.id, level: sf.level, subfunction: sf.subfunction, national_bn: sf.national_bn,
      response_low: sf.response.low, response_high: sf.response.high };
    for (const which of ["low", "high"]) {
      const amt = mean(MODELS.map((m, i) => amount(m, id, endSpec(which)[i].allocation) * sf.share_of_line));
      row[`group_amount_${which}_end_bn`] = amt;
      row[`added_${which}_end_bn`] = amt * sf.response[which];
    }
    contributions.push(row);
  }
}
const addUp = (which) => contributions.reduce((a, r) => a + r[`added_${which}_end_bn`], 0);
gate("subfunction contributions add to the move at each end", near(addUp("low"), move.low_end_spec_low_responses, 1e-9)
  && near(addUp("high"), move.high_end_spec_high_responses, 1e-9), `${addUp("low").toFixed(4)} / ${addUp("high").toFixed(4)}`);

// Sensitivities at the fixed end specifications (linear in each subfunction's response).
const sens = (fn) => ["low", "high"].map((which) => contributions.reduce((a, r) => a + r[`group_amount_${which}_end_bn`] * (fn(r, which) - r[`response_${which}`]), 0));
const bySf = Object.fromEntries(RESP.lines.economic_affairs_services.subfunctions.concat(RESP.lines.recreation_culture.subfunctions).map((s) => [s.id, s]));
const E = RESP.elasticities;
const sensitivities = {
  marginal_r_equals_b: { label: "measured responses taken as r = b instead of the finite removal (capped responses stay 1)",
    delta_bn: sens((r, which) => {
      const v = r[`response_${which}`];
      if (v === 1 || v === 0) return v;
      if (r.id.includes("general_economic")) return E.administration_general_government.b;
      if (r.id.includes("recreation")) return E.parks.across_states.b;
      return E.highways_nontoll.across_states.b;
    }) },
  within_states_uncapped: { label: "within-state readings above 1 priced at the high end (highways 1.4225, parks 1.3759): the unpriced upside",
    delta_bn: sens((r, which) => {
      if (which !== "high" || r[`response_high`] !== 1) return r[`response_${which}`];
      const e = r.id.includes("recreation") ? E.parks.within_states.b : E.highways_nontoll.within_states.b;
      return (1 - Math.pow(1 - RESP.meta.s, e)) / RESP.meta.s;
    }) },
  federal_fixed_at_high_end: { label: "federal subfunctions held fixed at the high end too",
    delta_bn: sens((r, which) => (r.level === "federal" ? 0 : r[`response_${which}`])) },
  across_states_at_high_end: { label: "S&L highways and parks at the across-state reading at the high end (no within-state reading)",
    delta_bn: sens((r, which) => {
      if (which !== "high") return r.response_low;
      if (r.id === "sl_highways" || r.id === "sl_recreation_and_culture" || r.id === "sl_transit_and_railroad") return bySf[r.id].response.low;
      if (r.level === "federal" && r.response_high === 1) {
        return r.id.includes("recreation") ? bySf.sl_recreation_and_culture.response.low : bySf.sl_highways.response.low;
      }
      return r.response_high;
    }) },
  held_at_zero_at_1: { label: "every subfunction held at 0 (water, space, agriculture, energy, natural resources, postal, commercial) at 1 instead",
    delta_bn: sens((r, which) => (r.response_low === 0 && r.response_high === 0 ? 1 : r[`response_${which}`])) },
};

// ---------------------------------------------------------------------------------------------------
const failed = gates.filter((g) => !g.passed).length;
if (failed) {
  console.error(`[BLOCKED] ${failed} gate(s) failed; nothing written`);
  process.exit(1);
}
const f = (x) => (Number.isInteger(x) ? String(x) : x.toPrecision(12));
const head = ["method", "spec", "allocation", "normalization", "share", "school", "gg", "uc", "justice",
  "cost_main_case_bn", "cost_low_bn", "cost_high_bn", "move_low_bn", "move_high_bn",
  "group_economic_affairs_bn", "group_recreation_bn"];
const csv = [head.join(",")];
MODELS.forEach((m, i) => specs.forEach((spec, j) => {
  csv.push([METHODS[i], j, spec.allocation, spec.normalization, f(spec.share), f(spec.school), f(spec.gg), spec.uc, spec.justice,
    f(old[i][j]), f(costs.low[i][j]), f(costs.high[i][j]), f(costs.low[i][j] - old[i][j]), f(costs.high[i][j] - old[i][j]),
    f(amount(m, LINES[0], spec.allocation)), f(amount(m, LINES[1], spec.allocation))].join(","));
}));
fs.writeFileSync(path.join(HERE, "derived", "per_spec_costs.csv"), csv.join("\n") + "\n");
const out = {
  main_case: { band_bn: oldBand, end_specifications: oldEnds.map((e, i) => ({ method: METHODS[i], low_end: e[0], high_end: e[1] })) },
  candidate: {
    band_bn: candidate,
    rule: "64 specifications x {low, high} responses; low end = minimum at the low responses, high end = maximum at the high responses, each averaged over the two fill-in methods",
    end_specifications: METHODS.map((m, i) => ({ method: m, low_end: Object.assign({ index: lowEnds[i][0], responses: "low" }, specs[lowEnds[i][0]]),
      high_end: Object.assign({ index: highEnds[i][1], responses: "high" }, specs[highEnds[i][1]]) })),
    line_responses: { low: blended("low"), high: blended("high") },
  },
  band_at_low_responses_throughout_bn: atLowOnly,
  band_at_high_responses_throughout_bn: atHighOnly,
  move_at_fixed_specifications_bn: move,
  contributions_at_end_specifications: contributions,
  sensitivities_at_end_specifications: sensitivities,
  group_amounts_at_end_specifications_bn: Object.fromEntries(["low", "high"].map((which) => [which,
    Object.fromEntries(LINES.map((id) => [id, mean(MODELS.map((m, i) => amount(m, id, endSpec(which)[i].allocation)))]))])),
};
fs.writeFileSync(path.join(HERE, "derived", "candidate_band.json"), JSON.stringify(out, null, 1) + "\n");
fs.writeFileSync(path.join(HERE, "derived", "gates_engine.json"), JSON.stringify({ gates }, null, 1) + "\n");

console.log("\n[result]");
console.log(`  main case (reproduced)     ${oldBand.map((x) => x.toFixed(4)).join(" – ")}`);
console.log(`  candidate                  ${candidate.map((x) => x.toFixed(4)).join(" – ")}  (end specs ${lowEnds.map((x) => x[0])} / ${highEnds.map((x) => x[1])})`);
console.log(`  low responses throughout   ${atLowOnly.map((x) => x.toFixed(4)).join(" – ")}`);
console.log(`  high responses throughout  ${atHighOnly.map((x) => x.toFixed(4)).join(" – ")}`);
console.log(`  move at fixed specs        low end ${move.low_end_spec_low_responses.toFixed(4)}  high end ${move.high_end_spec_high_responses.toFixed(4)}`);
for (const r of contributions) console.log(`    ${r.id.padEnd(42)} ${r.added_low_end_bn.toFixed(4).padStart(8)} ${r.added_high_end_bn.toFixed(4).padStart(8)}`);
for (const [k, v] of Object.entries(sensitivities)) console.log(`  sensitivity ${k.padEnd(28)} ${v.delta_bn.map((x) => x.toFixed(4)).join(" / ")}`);
console.log(`all ${gates.length} gates passed`);
