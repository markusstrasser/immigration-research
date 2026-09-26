/* The main case adopted on 2026-09-26 as importable definitions: the September 24 package
 * (../main_case_2026_09_24/package.cjs, imported unchanged) with the two corrections the operator
 * adopted together on 2026-09-26 (decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md):
 *
 *   227  Finite-removal responses (finite_response_2026_09_26/derived/r_values.json). A removal of a
 *        group that is 12% of residents and 17.5% of pupils saves r = [1 - (1 - s)^b] / s of average
 *        cost under a power-law cost, more than the elasticity b. General government responds at
 *        0.6000/0.8504 instead of the composite elasticities 0.59/0.84 (computed per component, the
 *        fixed federal part staying at zero), schools at 0.6522/0.6813 instead of CBO's 0.63/0.66, and
 *        audit row 8's increment shrinks to 0.949 of itself.
 *   225  The consumption key corrected for saving and remittances (consumption_key_2026_09_24, spec
 *        both_corridor_net_h2): that lane's cell edits, measured on the September 24 corrections and
 *        applied after them.
 *
 * The responses are data. They are engine state, not cell edits, so corrections.json carries them in
 * meta.responses and consumers set the engine's general-government and school responses from there,
 * not from scaling_check.json or 0.63/0.66. main_case.cjs runs the gates and writes the bands;
 * sign_reversal.cjs and page builders import this file, so there is one package.
 */
"use strict";
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const { Engine, MODEL, FISCAL, SYN, SYN_LINES, METHODS, STACKS, CONSTANTS, readJson, both, span, mean2 } = P;

const HERE = __dirname;
const R = readJson("finite_response_2026_09_26/derived/r_values.json");
const CK = readJson("consumption_key_2026_09_24/derived/payloads.json");
const SEPT24 = readJson("main_case_2026_09_24/derived/corrections.json");
const scaling = readJson("assumption_explorer_2026_09_21/derived/scaling_check.json");
const GG24 = [scaling.composite_low, scaling.composite_high];
const SCHOOL24 = [0.63, 0.66];
if (!(GG24[0] === 0.59 && GG24[1] === 0.84)) throw new Error("[BLOCKED] scaling_check.json composite is not 0.59/0.84");
if (!P.MAIN_SPECS.every((s) => GG24.includes(s.gg) && SCHOOL24.includes(s.school))) {
  throw new Error("[BLOCKED] the September 24 specifications use responses other than 0.59/0.84 and 0.63/0.66");
}

// ---------------------------------------------------------------------------------------------------
// Responses. o.finite: false (the September 24 elasticities), "all", "gg" or "school"; o.gg_s:
// "national_memo" (adopted) or "engine_population_key"; o.school_s: "" (the pupil share, adopted),
// "_s0.16" or "_s0.18".
function responsesFor(o) {
  const ggOn = o.finite === "all" || o.finite === "gg", schoolOn = o.finite === "all" || o.finite === "school";
  const gs = o.gg_s || "national_memo", ss = o.school_s || "";
  return {
    rule: o.finite ? "finite removal, r = [1 - (1 - s)^b] / s per component (finite_response_2026_09_26)" : "elasticity as response",
    general_government: ggOn
      ? { low: R[`gg_low_r_${gs}`], high: R[`gg_high_r_${gs}`], elasticity: [R.gg_low_b_unrounded, R.gg_high_b], s: R[`s_${gs}`] }
      : { low: GG24[0], high: GG24[1], elasticity: GG24, s: null },
    school: schoolOn
      ? { growth: R[`school_r_0.63${ss}`], decline: R[`school_r_0.66${ss}`], elasticity: SCHOOL24,
        s: ss ? Number(ss.slice(2)) : R.s_pupil }
      : { growth: SCHOOL24[0], decline: SCHOOL24[1], elasticity: SCHOOL24, s: null },
    row8_factor: ggOn ? R[`row8_factor_${gs}`] : 1,
  };
}
// The September 24 specifications with the responses replaced value for value.
function specsFor(o) {
  const r = responsesFor(o);
  return P.MAIN_SPECS.map((s) => ({ ...s,
    gg: s.gg === GG24[0] ? r.general_government.low : r.general_government.high,
    school: s.school === SCHOOL24[0] ? r.school.growth : r.school.decline }));
}
const bandFor = (m, profile, specs) => span(specs.map((spec) => P.cost(m, spec, profile)));
// Audit row 8 is a constant at the all-spending elasticity; under finite removal its increment
// scales by row8_factor (finite_response_2026_09_26 RESULT, "Dependent constant").
const row8Shifts = (o) => {
  const f = responsesFor(o).row8_factor;
  return f === 1 ? [] : [{ side: "spending", line: SYN.constants, key: "k", by: both(CONSTANTS.row8.c * (f - 1)) }];
};

// ---------------------------------------------------------------------------------------------------
// Consumption key. o.ck: a spec of consumption_key_2026_09_24/derived/payloads.json, or null.
if (CK.meta.composes_with !== "main_case_2026_09_24/derived/corrections.json") {
  throw new Error("[BLOCKED] the consumption-key edits do not compose with the September 24 corrections");
}
const ckEdits = (o) => {
  if (!o.ck) return [];
  if (!CK.specs[o.ck]) throw new Error("no consumption-key spec " + o.ck);
  return CK.specs[o.ck].edits;
};
const CK_SPECS = Object.keys(CK.specs).filter((k) => CK.specs[k].family === "both");

// ---------------------------------------------------------------------------------------------------
// The package.
const CENTRAL = Object.assign({}, P.CENTRAL, { finite: "all", gg_s: "national_memo", school_s: "", ck: "both_corridor_net_h2" });
const withCentral = (o) => Object.assign({}, CENTRAL, o);
const build = (shifts, o) => Engine.applyCorrections(MODEL, { lines: SYN_LINES, edits: P.expand(shifts).concat(ckEdits(withCentral(o))) });
function packageShifts(p, caseName, method, o) {
  return P.packageShifts(p, caseName, method, o).concat(row8Shifts(o));
}
function evalPackage(caseName, method, o) {
  const oo = withCentral(o);
  return bandFor(build(packageShifts(STACKS[`row4+status_state_aware|${caseName}|${method}`], caseName, method, oo), oo),
    oo.profile, specsFor(oo));
}
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
const MAIN_SPECS = specsFor(CENTRAL);
const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);
const RESPONSES = responsesFor(CENTRAL);

// The adopted package as the engine's corrections payload: the September 24 payload (its central case,
// the two fill-in methods averaged), plus row 8's finite factor and the consumption key's edits, one
// net edit per cell. meta.responses carries the responses every consumer must set.
const cellId = (e) => [e.side, e.line, e.side === "receipt" ? e.scenario : e.key].join("|");
function correctionsPayload(o) {
  const oo = withCentral(o);
  const base = P.correctionsPayload();
  const net = new Map(base.edits.map((e) => [cellId(e), { ...e, by: { ...e.by } }]));
  for (const e of P.expand(row8Shifts(oo)).concat(ckEdits(oo))) {
    const id = cellId(e);
    if (net.has(id)) net.get(id).by = P.plus(net.get(id).by, e.by); else net.set(id, { ...e, by: { ...e.by } });
  }
  return {
    meta: { source: "main_case_2026_09_26/package.cjs", adopted: "2026-09-26",
      decision: "decisions/2026-09-26-main-case-finite-removal-and-consumption-key.md",
      case: `${base.meta.case}; finite-removal responses; consumption key ${oo.ck}`,
      builds_on: base.meta, responses: responsesFor(oo) },
    lines: base.lines, edits: [...net.values()],
  };
}

module.exports = Object.assign({}, P, {
  HERE, P24: P, R, CK, SEPT24, GG24, SCHOOL24, CK_SPECS, CENTRAL, RESPONSES, MAIN_SPECS,
  responsesFor, specsFor, bandFor, row8Shifts, ckEdits, build, packageShifts, evalPackage, central, band,
  correctionsPayload, cellId,
});
