/* The adopted main case (main_case_schools_full_2026_09_26) specification by specification, for
 * capital_return.py. Prints one JSON document to stdout and writes nothing.
 *
 * For each fill-in method and each of the 64 specifications it records the case's cost from the
 * package's cost(), and, from that same engine evaluation, every spending line's group amount, national
 * amount, allocation rule and response, and the same for the enterprise-surplus receipt line (where the
 * NIPAs put government enterprises' operating results). Engine.evaluate is wrapped only to keep the evaluation that
 * cost() makes; cost() itself runs unchanged. The models are built as main_case.cjs builds them for
 * its per-specification gates, so the two fill-in methods' bands average to the published case.
 *
 * It also evaluates the published derived/corrections.json at the same specifications, with the
 * responses set from its meta.responses, as an independent path for the gates.
 */
"use strict";
const fs = require("fs");
const path = require("path");

const FISCAL = path.join(__dirname, "..");
const P = require(path.join(FISCAL, "main_case_schools_full_2026_09_26", "package.cjs"));
const { P26, Engine, MODEL, STACKS, METHODS, MAIN_SPECS, MAIN_PROFILE } = P;

// Keep the evaluation cost() makes.
const evaluate = Engine.evaluate;
let last = null;
Engine.evaluate = (m, s) => { last = evaluate(m, s); return last; };
function costAndLines(model, spec) {
  last = null;
  const cost = P.cost(model, spec, MAIN_PROFILE);
  if (!last || Math.abs(-last.welfare_bn - cost) > 1e-12) throw new Error("[BLOCKED] cost() did not evaluate once through Engine.evaluate");
  const lines = {};
  for (const l of last.spending) {
    lines[l.id] = { amount_bn: l.amount_bn, national_bn: l.national_bn, key: l.key, response: l.response };
  }
  const ent = last.receipts.filter((r) => r.id === "enterprise_surplus");
  if (ent.length !== 1) throw new Error("[BLOCKED] expected one enterprise_surplus receipt line");
  const enterprise = { amount_bn: ent[0].amount_bn, national_bn: ent[0].national_bn, key: ent[0].key,
    response: ent[0].response, group: ent[0].group };
  return { cost_bn: cost, lines, enterprise };
}

// The models of main_case.cjs (its per-specification gates): the September 26 build, central case, per method.
const models = METHODS.map((m) => P26.build(P26.packageShifts(STACKS[`row4+status_state_aware|central|${m}`], "central", m,
  P26.CENTRAL), P26.CENTRAL));
const perMethod = Object.fromEntries(METHODS.map((m, i) => [m, MAIN_SPECS.map((spec) => costAndLines(models[i], spec))]));

// The published payload at the same specifications. cost() sets the general-government response from
// the specification and the school response through the specification's school field; both must equal
// meta.responses, which capital_return.py gates.
const payload = JSON.parse(fs.readFileSync(path.join(FISCAL, "main_case_schools_full_2026_09_26", "derived", "corrections.json"), "utf8"));
const payloadModel = Engine.applyCorrections(MODEL, { lines: payload.lines, edits: payload.edits });
const payloadCosts = MAIN_SPECS.map((spec) => costAndLines(payloadModel, spec).cost_bn);
Engine.evaluate = evaluate;

const inventory = MODEL.spending.lines.map((l) => ({ id: l.id, family: l.family, national_bn: l.national_bn,
  response_class: l.response_class, preferred_key: l.preferred_key, label: l.label || null }));

process.stdout.write(JSON.stringify({
  source: "main_case_schools_full_2026_09_26/package.cjs",
  methods: METHODS, profile: MAIN_PROFILE, profile_def: P.PROFILES[MAIN_PROFILE],
  specs: MAIN_SPECS, central: P.central({}), responses: P.RESPONSES, payload_meta_responses: payload.meta.responses,
  delayed_lines: MODEL.service.delayed, synthetic_lines: P.SYN_LINES,
  inventory, per_method: perMethod, payload_costs: payloadCosts,
}) + "\n");
