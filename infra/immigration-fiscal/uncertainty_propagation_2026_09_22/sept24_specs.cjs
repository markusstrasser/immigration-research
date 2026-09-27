/* Inputs for propagate.py --case sept24 and each later case: the adopted main cases, specification by
 * specification, from the explorer engine.
 *
 * Writes derived/sept24/spec_costs.csv (the 64 main specifications of main_case_2026_09_24/package.cjs,
 * each costed on the September 23 frame and on the corrected model) and derived/sept24/line_targets.csv
 * (the group's target on every receipt line at the reference incidence rule and on every spending line
 * and key, before and after main_case_2026_09_24/derived/corrections.json; the synthetic correction
 * lines appear only after). Gates (exit 1, nothing written): the two sets of costs span the published
 * September 23 and September 24 bands (main_case_2026_09_24/derived/summary.json, 1e-9).
 *
 * Since 2026-09-26 it also writes derived/<case>/ for each later case in later_cases.json (case -> main-case
 * lane; sept26, CBO's one-year school response, then sept26_schools, schools at full average cost): the
 * same 64 specifications with that case's responses (engine state, read from the lane's
 * derived/corrections.json meta.responses; school_sept24 and gg_sept24 keep the September 24 values each
 * replaced), costed on the uncorrected model and on the model with that payload, and the line targets
 * before and after the payload. Gates: the mapped specifications equal that lane's package.cjs MAIN_SPECS,
 * and the costs span its uncorrected_at_adopted_responses and main_case bands (summary.json, 1e-9). The
 * files of earlier cases do not change.
 *
 * Since 2026-09-27 a case whose package exports evaluateFull (sept27: long-run responses, rental assistance,
 * government enterprises and the return on public capital) is costed through that package, on its own
 * specifications, with the capital return in its own columns. spec_costs.csv also carries each specification's
 * reading, rate, enterprise option and line responses, and the return's derivative with respect to each key
 * line's group amount (kcoef_<line>) and to the enterprise receipt's key share (kcoef_enterprise_share), for
 * propagate.py. Extra gates: the payload model gives the mean of the methods in the lane's per_spec.csv at every
 * specification, in cost and in capital return (1e-9); the derivatives rebuild the return on both models (1e-9).
 * Such a case also writes derived/<case>/benefit_factors.csv: the administrative benefit keys' shift on each line
 * (the producer's central change times the CPS stack's factor, the methods' mean), which propagate.py varies on
 * the CPS replicates jointly with the account (conceptual audit 2026-09-27, section A).
 *
 * Run from anywhere: node sept24_specs.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const P26 = require(path.join(__dirname, "..", "main_case_2026_09_26", "package.cjs"));
const { Engine, MODEL, FISCAL, MAIN_SPECS, ALLOCS, cost, span, readJson } = P;

const corrected = Engine.applyCorrections(MODEL, readJson("main_case_2026_09_24/derived/corrections.json"));
const summary = readJson("main_case_2026_09_24/derived/summary.json");
let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

const specs = MAIN_SPECS.map((s) => ({ ...s, sept23: cost(MODEL, s), sept24: cost(corrected, s) }));
for (const [c, want] of [["sept23", summary.adopted_2026_09_23], ["sept24", summary.main_case]]) {
  const b = span(specs.map((s) => s[c]));
  gate(`${c} specifications span the published band`, Math.abs(b[0] - want[0]) < 1e-9 && Math.abs(b[1] - want[1]) < 1e-9,
    `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
}

// The group's target on every executed cell of `after`, beside the uncorrected model's.
function lineTargets(after) {
  const ref = MODEL.receipts.reference;
  const rows = [];
  for (const line of after.receipts.lines) {
    const before = MODEL.receipts.lines.find((l) => l.id === line.id);
    for (const a of ALLOCS) {
      rows.push(["receipt", line.id, ref, a, before.cells[ref][a].target_bn, line.cells[ref][a].target_bn]);
    }
  }
  for (const line of after.spending.lines) {
    const before = MODEL.spending.lines.find((l) => l.id === line.id);
    for (const [key, k] of Object.entries(line.keys)) {
      for (const a of ALLOCS) {
        rows.push(["spending", line.id, key, a, before ? before.keys[key][a].target_bn : "", k[a].target_bn]);
      }
    }
  }
  return rows;
}
const targets = lineTargets(corrected);

// Later cases (later_cases.json: case -> main-case lane, one line each): responses from that lane's
// payload, each September 24 value replaced by its adopted counterpart.
const { GG24, SCHOOL24 } = P26;
const swap = (v, old, now) => (v === old[0] ? now[0] : v === old[1] ? now[1] : NaN);

// A case with the return on public capital: its package's specifications and evaluateFull, on the uncorrected
// model and on the model with its payload. The return is sum over components of stock x rate x key x response;
// a line-keyed component's key is its numerator lines' group amounts over the denominator's national amount,
// and an enterprise component's key is the enterprise receipt's share, so the derivatives below are exact.
const KLINES = ["education_services", "school_reprice", "college_rekey", "public_order_safety", "health_services",
  "general_public_services", "economic_affairs_services", "recreation_culture"];
const RLINES = ["economic_affairs_services", "recreation_culture", "housing_subsidies"];
const EXTRA = ["reading", "rate", "long_run", "enterprises", "line_responses"];
function csvRows(rel) {
  const [head, ...rows] = fs.readFileSync(path.join(FISCAL, rel), "utf8").trim().split("\n").map((l) => l.split(","));
  return rows.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}
function capitalCase(name, lane, PC, payload, sum) {
  const R = payload.meta.responses;
  const models = { uncorrected: PC.MODEL, [name]: Engine.applyCorrections(PC.MODEL, payload) };
  const rows = MAIN_SPECS.map((s, i) => ({ ...s,
    gg: swap(s.gg, GG24, [R.general_government.low, R.general_government.high]),
    school: swap(s.school, SCHOOL24, [R.school.growth, R.school.decline]),
    school_sept24: s.school, gg_sept24: s.gg,
    reading: PC.MAIN_SPECS[i].reading, rate: PC.MAIN_SPECS[i].rate, enterprises: PC.MAIN_SPECS[i].enterprises }));
  gate(`${name}: adopted responses replace the September 24 ones one for one (${lane}/package.cjs MAIN_SPECS)`,
    rows.length === PC.MAIN_SPECS.length && rows.every((s, i) => Object.keys(MAIN_SPECS[0]).every((k) => s[k] === PC.MAIN_SPECS[i][k])
      && Object.keys(PC.MAIN_SPECS[i]).every((k) => k in MAIN_SPECS[0] || EXTRA.includes(k))),
    `general government ${R.general_government.low.toFixed(4)}/${R.general_government.high.toFixed(4)}, ` +
    `schools ${R.school.growth.toFixed(4)}/${R.school.decline.toFixed(4)}, readings ${rows.filter((s) => s.reading === "low").length} low`);
  const defs = Object.fromEntries(PC.componentsFor(null).map((c) => [c.id, c]));
  let coefGap = 0, rebuildGap = 0, responseGap = 0, transferGap = 0;
  for (const [i, s] of rows.entries()) {
    const spec = PC.MAIN_SPECS[i];
    const coefs = {};
    for (const [c, m] of Object.entries(models)) {
      const r = PC.evaluateFull(m, spec, PC.MAIN_PROFILE);
      const line = (id) => r.evaluation.spending.find((l) => l.id === id);
      const receipt = (id) => r.evaluation.receipts.find((l) => l.id === id);
      const k = Object.fromEntries(KLINES.map((id) => [id, 0]).concat([["enterprise_share", 0]]));
      for (const comp of r.capital.components) {
        const rule = defs[comp.id].key, unit = comp.stock_charged_bn * spec.rate * comp.response;
        if (rule.kind === "receipt_amount_over_national" && rule.line === PC.ENTERPRISE_LINE) k.enterprise_share += unit;
        else if (rule.kind === "lines_amount_over_national") {
          for (const id of rule.numerator_lines) {
            if (!(id in k)) throw new Error(`[BLOCKED] capital key line ${id} is not in KLINES`);
            k[id] += unit / line(rule.denominator_line).national_bn;
          }
        } else throw new Error(`[BLOCKED] capital key kind ${rule.kind} has no derivative here`);
      }
      const es = receipt(PC.ENTERPRISE_LINE);
      const rebuilt = KLINES.reduce((a, id) => a + k[id] * line(id).amount_bn, 0) + k.enterprise_share * es.amount_bn / es.national_bn;
      rebuildGap = Math.max(rebuildGap, Math.abs(rebuilt - r.capital.total_bn));
      if (c === "uncorrected") Object.assign(coefs, k);
      else coefGap = Math.max(coefGap, ...Object.keys(k).map((id) => Math.abs(k[id] - coefs[id])));
      s[c] = r.cost_bn;
      s[`capital_${c}`] = r.capital.total_bn;
      for (const id of RLINES) {
        s[`response_${id}`] = line(id).response;
        responseGap = Math.max(responseGap, Math.abs(line(id).response - spec.line_responses[id]));
      }
      s.response_receipt_enterprise_surplus = es.response;
      responseGap = Math.max(responseGap, Math.abs(es.response - spec.line_responses[PC.ENTERPRISE_RECEIPT]));
      for (const id of TRANSFER_LINES) transferGap = Math.max(transferGap, Math.abs(line(id).response - 1));
    }
    for (const id of Object.keys(coefs)) s[`kcoef_${id}`] = coefs[id];
  }
  gate(`${name}: each line takes its specification's response (engine rows)`, responseGap === 0, `${rows.length} specifications`);
  gate(`${name}: the benefit keys' transfer lines respond fully (engine rows)`, transferGap === 0, TRANSFER_LINES.join(", "));
  gate(`${name}: the derivatives rebuild the capital return on both models (1e-9) and do not depend on the model (1e-12)`,
    rebuildGap < 1e-9 && coefGap < 1e-12, `rebuild ${rebuildGap.toExponential(1)}, models ${coefGap.toExponential(1)}`);
  for (const [c, want] of [["uncorrected", sum.uncorrected_at_adopted_responses], [name, sum.main_case]]) {
    const b = span(rows.map((s) => s[c]));
    gate(`${name}: ${c} specifications span the published band`,
      Math.abs(b[0] - want[0]) < 1e-9 && Math.abs(b[1] - want[1]) < 1e-9, `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
  }
  const per = csvRows(`${lane}/derived/per_spec.csv`);
  const methodMean = (i, col) => {
    const xs = per.filter((r) => Number(r.spec) === i).map((r) => Number(r[col]));
    if (xs.length !== 2) throw new Error(`[BLOCKED] per_spec.csv has ${xs.length} rows for specification ${i}`);
    return (xs[0] + xs[1]) / 2;
  };
  const gap = Math.max(...rows.flatMap((s, i) => [Math.abs(s[name] - methodMean(i, "cost_bn")),
    Math.abs(s[`capital_${name}`] - methodMean(i, "capital_total_bn"))]));
  gate(`${name}: the payload model gives the methods' mean of per_spec.csv at every specification, cost and capital return (1e-9)`,
    gap < 1e-9, `max |diff| ${gap.toExponential(1)}`);
  const dims = Object.keys(MAIN_SPECS[0]).concat(["school_sept24", "gg_sept24", "reading", "rate", "enterprises"],
    RLINES.map((id) => `response_${id}`), ["response_receipt_enterprise_surplus"]);
  const costCols = [["cost_uncorrected_bn", "uncorrected"], [`cost_${name}_bn`, name],
    ["capital_uncorrected_bn", "capital_uncorrected"], [`capital_${name}_bn`, `capital_${name}`]]
    .concat(KLINES.concat(["enterprise_share"]).map((id) => [`kcoef_${id}`, `kcoef_${id}`]));
  return { name, rows, targets: lineTargets(models[name]), dims, costCols, benefits: benefitFactors(name, PC) };
}
// The administrative benefit keys in a case's payload: the package's benefitShifts, the producer's central change
// on each line times the CPS stack's factor on that line, as the methods' mean. propagate.py varies the change on
// the CPS replicates jointly with the account. Gates: the case uses the central package with no deviation, each
// transfer line responds fully (checked in capitalCase's rows through TRANSFER_LINES), and each shift over its
// change equals stackFactor (the definition the conceptual audit's probe uses, 1e-12).
const TRANSFER_LINES = ["snap", "other_state_welfare", "family_and_general_assistance", "unemployment"];
function benefitFactors(name, PC) {
  const oo = PC.withCentral({});
  gate(`${name}: the payload's benefit keys are the producer's central package`,
    oo.benefits === "package_central" && !oo.benefitsDev, `${oo.benefits}, deviation ${oo.benefitsDev}`);
  const deltas = readJson("admin_benefit_keys_2026_09_24/derived/line_deltas.json").deltas[oo.benefits];
  const acc = {};
  let factorGap = 0;
  for (const m of PC.METHODS) {
    const p = PC.STACKS[`row4+status_state_aware|central|${m}`];
    for (const s of PC.P24.benefitShifts(p, oo.benefits)) {
      const f = PC.P24.stackFactor(p, "spending", s.line, null);
      for (const a of ALLOCS) {
        factorGap = Math.max(factorGap, Math.abs(s.by[a] / deltas[s.line][a] - f[a]));
        const k = `${s.line}|${a}`;
        acc[k] = acc[k] || { line: s.line, allocation: a, delta_bn: deltas[s.line][a], stack_factor: 0, shift_bn: 0 };
        acc[k].stack_factor += f[a] / PC.METHODS.length;
        acc[k].shift_bn += s.by[a] / PC.METHODS.length;
      }
    }
  }
  const rows = Object.values(acc);
  gate(`${name}: each benefit shift is the central change times the stack factor (1e-12)`,
    factorGap < 1e-12 && rows.length === 2 * Object.keys(deltas).length,
    `${rows.length / 2} lines, max |diff| ${factorGap.toExponential(1)}`);
  return rows;
}
const later = Object.entries(JSON.parse(fs.readFileSync(path.join(__dirname, "later_cases.json"), "utf8")))
  .map(([name, lane]) => {
    const PC = require(path.join(__dirname, "..", lane, "package.cjs"));
    const payload = readJson(`${lane}/derived/corrections.json`);
    const sum = readJson(`${lane}/derived/summary.json`);
    const R = payload.meta.responses;
    gate(`${name}: payload responses equal summary.json responses`, JSON.stringify(R) === JSON.stringify(sum.responses));
    if (PC.evaluateFull) return capitalCase(name, lane, PC, payload, sum);
    const rows = MAIN_SPECS.map((s) => ({ ...s,
      gg: swap(s.gg, GG24, [R.general_government.low, R.general_government.high]),
      school: swap(s.school, SCHOOL24, [R.school.growth, R.school.decline]),
      school_sept24: s.school, gg_sept24: s.gg }));
    gate(`${name}: adopted responses replace the September 24 ones one for one (${lane}/package.cjs MAIN_SPECS)`,
      rows.length === PC.MAIN_SPECS.length &&
      rows.every((s, i) => Object.entries(PC.MAIN_SPECS[i]).every(([k, v]) => s[k] === v)),
      `general government ${R.general_government.low.toFixed(4)}/${R.general_government.high.toFixed(4)}, ` +
      `schools ${R.school.growth.toFixed(4)}/${R.school.decline.toFixed(4)}`);
    const model = Engine.applyCorrections(MODEL, payload);
    for (const s of rows) { s.uncorrected = cost(MODEL, s); s[name] = cost(model, s); }
    for (const [c, want] of [["uncorrected", sum.uncorrected_at_adopted_responses], [name, sum.main_case]]) {
      const b = span(rows.map((s) => s[c]));
      gate(`${name}: ${c} specifications span the published band`,
        Math.abs(b[0] - want[0]) < 1e-9 && Math.abs(b[1] - want[1]) < 1e-9, `${b[0].toFixed(4)}–${b[1].toFixed(4)}`);
    }
    return { name, rows, targets: lineTargets(model) };
  });

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
const num = (x) => (typeof x === "number" ? x.toPrecision(15) : x);
function write(dir, dims, costCols, rows, targetCols, targetRows) {
  const out = path.join(__dirname, "derived", dir);
  fs.mkdirSync(out, { recursive: true });
  fs.writeFileSync(path.join(out, "spec_costs.csv"), [dims.concat(costCols.map(([name]) => name)).join(",")]
    .concat(rows.map((s) => dims.map((d) => s[d]).concat(costCols.map(([, c]) => s[c].toPrecision(15))).join(",")))
    .join("\n") + "\n");
  fs.writeFileSync(path.join(out, "line_targets.csv"), [["side", "line", "key", "allocation"].concat(targetCols).join(",")]
    .concat(targetRows.map((r) => r.map(num).join(","))).join("\n") + "\n");
  console.log(`${rows.length} specifications, ${targetRows.length} line targets -> ${path.relative(FISCAL, out)}`);
}
const dims = Object.keys(MAIN_SPECS[0]);
write("sept24", dims, [["cost_sept23_bn", "sept23"], ["cost_sept24_bn", "sept24"]], specs,
  ["target_sept23_bn", "target_sept24_bn"], targets);
for (const c of later) {
  write(c.name, c.dims || dims.concat(["school_sept24", "gg_sept24"]),
    c.costCols || [["cost_uncorrected_bn", "uncorrected"], [`cost_${c.name}_bn`, c.name]], c.rows,
    ["target_uncorrected_bn", `target_${c.name}_bn`], c.targets);
  if (c.benefits) {
    const cols = ["line", "allocation", "delta_bn", "stack_factor", "shift_bn"];
    fs.writeFileSync(path.join(__dirname, "derived", c.name, "benefit_factors.csv"),
      [cols.join(",")].concat(c.benefits.map((r) => cols.map((k) => num(r[k])).join(","))).join("\n") + "\n");
  }
}
console.log("all gates passed");
