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
 * Since 2026-09-29 (sept29, main_case_2026_09_29, candidate v4 adopted) the capital case is general in what a payload
 * adds. The key lines come from the payload's components (keyLines), a part_rekeyed key included; spec_costs.csv
 * records every entry of a specification's line_responses (13 in sept29); line_targets.csv leaves a receipt line the
 * uncorrected model lacks empty before the payload, as it does a synthetic spending line. A payload that rescales a
 * line's national total (sept29: housing_subsidies, enterprise_surplus, remaining_production_property) changes the
 * derivative per unit of amount of a line keyed over that total, so such a case writes each model's own derivatives
 * (kcoef_uncorrected_<line>, kcoef_<case>_<line>); the gate is that they differ only through those national totals
 * (1e-12). A payload with a production grid also writes each model's production-term sampling SE at the
 * specification's production cell (production_se_uncorrected_bn, production_se_<case>_bn), and one with national-scale
 * edits writes benefit_factors.csv's national_scale: the factor by which the payload rescales a benefit line after its
 * benefit shift (gate: every national-scale edit on the line follows every cell edit on it).
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
      rows.push(["receipt", line.id, ref, a, before ? before.cells[ref][a].target_bn : "", line.cells[ref][a].target_bn]);
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
// a line-keyed component's key is its numerator lines' group amounts over the denominator's national amount, a
// part_rekeyed component's key is its parent line's amount over the parent's national amount plus its correction
// line's amount over the part's national total (part_national_bn), and an enterprise component's key is the
// enterprise receipt's share, so the derivatives below are exact.
// The key lines of a case's components, in the order the components first name them (September 27: education_services,
// school_reprice, college_rekey, public_order_safety, health_services, general_public_services,
// economic_affairs_services, recreation_culture); the enterprise receipt's share is kcoef_enterprise_share.
function keyLines(components, enterpriseLine) {
  const out = [];
  const add = (id) => { if (!out.includes(id)) out.push(id); };
  for (const c of components) {
    const k = c.key;
    if (k.kind === "lines_amount_over_national") k.numerator_lines.forEach(add);
    else if (k.kind === "part_rekeyed") { add(k.parent_line); add(k.correction_line); }
    else if (!(k.kind === "receipt_amount_over_national" && k.line === enterpriseLine)) {
      throw new Error(`[BLOCKED] capital key kind ${k.kind} (component ${c.id}) has no derivative here`);
    }
  }
  return out;
}
// A line response's column: response_<line>, or response_receipt_<line> for a receipt's ("receipt:<line>").
const responseColumn = (id) => (id.startsWith("receipt:") ? `response_receipt_${id.slice("receipt:".length)}` : `response_${id}`);
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
  const components = PC.componentsFor(null);
  const defs = Object.fromEntries(components.map((c) => [c.id, c]));
  const KLINES = keyLines(components, PC.ENTERPRISE_LINE);
  // Every line response a specification sets, in its order (September 27: the two long-run lines, rental assistance
  // and the enterprise receipt).
  const RESP = Object.keys(PC.MAIN_SPECS[0].line_responses);
  gate(`${name}: every specification sets the same line responses`,
    PC.MAIN_SPECS.every((spec) => JSON.stringify(Object.keys(spec.line_responses)) === JSON.stringify(RESP)), `${RESP.length} entries`);
  // A payload that rescales a line's national total gives the lines keyed over it a derivative per unit of amount
  // that differs between the two models, so each model's own is written.
  const scaled = payload.edits.some((e) => e.national_bn !== undefined);
  const grid = Boolean(payload.production);
  let coefGap = 0, modelGap = 0, rebuildGap = 0, responseGap = 0, transferGap = 0;
  const moved = new Set();
  for (const [i, s] of rows.entries()) {
    const spec = PC.MAIN_SPECS[i];
    const evals = Object.fromEntries(Object.entries(models).map(([c, m]) => [c, PC.evaluateFull(m, spec, PC.MAIN_PROFILE)]));
    // The return's derivatives on evaluation r: per unit of each key line's group amount, with the national totals
    // of evaluation n, and per unit of the enterprise receipt's share.
    const derivatives = (r, n) => {
      const national = (id) => n.evaluation.spending.find((l) => l.id === id).national_bn;
      const k = Object.fromEntries(KLINES.map((id) => [id, 0]).concat([["enterprise_share", 0]]));
      for (const comp of r.capital.components) {
        const rule = defs[comp.id].key, unit = comp.stock_charged_bn * spec.rate * comp.response;
        if (rule.kind === "receipt_amount_over_national" && rule.line === PC.ENTERPRISE_LINE) k.enterprise_share += unit;
        else if (rule.kind === "lines_amount_over_national") {
          for (const id of rule.numerator_lines) k[id] += unit / national(rule.denominator_line);
        } else if (rule.kind === "part_rekeyed") {
          k[rule.parent_line] += unit / national(rule.parent_line);
          k[rule.correction_line] += unit / rule.part_national_bn;
        } else throw new Error(`[BLOCKED] capital key kind ${rule.kind} has no derivative here`);
      }
      return k;
    };
    const ks = {};
    for (const [c, r] of Object.entries(evals)) {
      const line = (id) => r.evaluation.spending.find((l) => l.id === id);
      const receipt = (id) => r.evaluation.receipts.find((l) => l.id === id);
      const k = derivatives(r, r);
      ks[c] = k;
      const es = receipt(PC.ENTERPRISE_LINE);
      const rebuilt = KLINES.reduce((a, id) => a + k[id] * line(id).amount_bn, 0) + k.enterprise_share * es.amount_bn / es.national_bn;
      rebuildGap = Math.max(rebuildGap, Math.abs(rebuilt - r.capital.total_bn));
      s[c] = r.cost_bn;
      s[`capital_${c}`] = r.capital.total_bn;
      for (const id of RESP) {
        const got = id.startsWith("receipt:") ? receipt(id.slice("receipt:".length)).response : line(id).response;
        s[responseColumn(id)] = got;
        responseGap = Math.max(responseGap, Math.abs(got - spec.line_responses[id]));
      }
      for (const id of TRANSFER_LINES) transferGap = Math.max(transferGap, Math.abs(line(id).response - 1));
      if (grid) s[`production_se_${c}`] = r.evaluation.sampling_se_bn;
    }
    // The derivatives depend on the model only through the national totals: on the uncorrected evaluation with the
    // case's national totals they are the case's.
    const kAt = derivatives(evals.uncorrected, evals[name]);
    coefGap = Math.max(coefGap, ...Object.keys(kAt).map((id) => Math.abs(kAt[id] - ks[name][id])));
    for (const id of Object.keys(ks[name])) {
      const d = Math.abs(ks[name][id] - ks.uncorrected[id]);
      modelGap = Math.max(modelGap, d);
      if (d >= 1e-12) moved.add(id);
    }
    if (scaled) for (const c of Object.keys(models)) for (const id of Object.keys(ks[c])) s[`kcoef_${c}_${id}`] = ks[c][id];
    else for (const id of Object.keys(ks.uncorrected)) s[`kcoef_${id}`] = ks.uncorrected[id];
  }
  gate(`${name}: each line takes its specification's response (engine rows)`, responseGap === 0,
    `${rows.length} specifications, ${RESP.length} line responses`);
  gate(`${name}: the benefit keys' transfer lines respond fully (engine rows)`, transferGap === 0, TRANSFER_LINES.join(", "));
  if (scaled) {
    gate(`${name}: the derivatives rebuild the capital return on both models (1e-9) and differ between them only through the national totals the payload rescales (1e-12)`,
      rebuildGap < 1e-9 && coefGap < 1e-12, `rebuild ${rebuildGap.toExponential(1)}, national totals ${coefGap.toExponential(1)}; ` +
      `moved: ${[...moved].join(", ") || "none"} (max ${modelGap.toExponential(2)})`);
  } else {
    gate(`${name}: the derivatives rebuild the capital return on both models (1e-9) and do not depend on the model (1e-12)`,
      rebuildGap < 1e-9 && modelGap < 1e-12, `rebuild ${rebuildGap.toExponential(1)}, models ${modelGap.toExponential(1)}`);
  }
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
    RESP.map(responseColumn));
  const kcols = (prefix) => KLINES.concat(["enterprise_share"]).map((id) => [`${prefix}${id}`, `${prefix}${id}`]);
  const costCols = [["cost_uncorrected_bn", "uncorrected"], [`cost_${name}_bn`, name],
    ["capital_uncorrected_bn", "capital_uncorrected"], [`capital_${name}_bn`, `capital_${name}`]]
    .concat(scaled ? kcols("kcoef_uncorrected_").concat(kcols(`kcoef_${name}_`)) : kcols("kcoef_"))
    .concat(grid ? [["production_se_uncorrected_bn", "production_se_uncorrected"], [`production_se_${name}_bn`, `production_se_${name}`]] : []);
  return { name, rows, targets: lineTargets(models[name]), dims, costCols, benefits: benefitFactors(name, PC, payload) };
}
// The administrative benefit keys in a case's payload: the package's benefitShifts, the producer's central change
// on each line times the CPS stack's factor on that line, as the methods' mean. propagate.py varies the change on
// the CPS replicates jointly with the account. Gates: the case uses the central package with no deviation, each
// transfer line responds fully (checked in capitalCase's rows through TRANSFER_LINES), and each shift over its
// change equals stackFactor (the definition the conceptual audit's probe uses, 1e-12). A payload with national-scale
// edits adds national_scale: the factor by which it rescales the line's national total, and so the shift, after
// every cell edit on the line (sept29: housing_subsidies, candidate v4 item 1); 1 on a line it does not rescale.
const TRANSFER_LINES = ["snap", "other_state_welfare", "family_and_general_assistance", "unemployment"];
function nationalScales(PC, payload) {
  // A payload with the lineage (oct05) appends the added people's cell edits after September 29's; they are not
  // benefit shifts and no scale edit follows them, so the gate reads the edits before them (meta.lineage.edits.first).
  const edits = payload.meta.lineage ? payload.edits.slice(0, payload.meta.lineage.edits.first) : payload.edits;
  const scales = edits.map((e, i) => [e, i]).filter(([e]) => e.national_bn !== undefined);
  if (!scales.length) return null;
  return (line) => {
    const own = scales.filter(([e]) => e.side === "spending" && e.line === line);
    if (!own.length) return 1;
    const lastCell = Math.max(-1, ...edits.map((e, i) => (e.line === line && e.national_bn === undefined ? i : -1)));
    gate(`${line}: every national-scale edit follows every cell edit on the line, so it scales the benefit shift`,
      own.every(([, i]) => i > lastCell), `cell edits up to ${lastCell}, scale edits at ${own.map(([, i]) => i).join(", ")}`);
    return own[own.length - 1][0].national_bn / PC.MODEL.spending.lines.find((l) => l.id === line).national_bn;
  };
}
function benefitFactors(name, PC, payload) {
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
  const scaleOf = nationalScales(PC, payload);
  if (scaleOf) {
    const scale = Object.fromEntries([...new Set(rows.map((r) => r.line))].map((line) => [line, scaleOf(line)]));
    for (const r of rows) r.national_scale = scale[r.line];
  }
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
    const cols = ["line", "allocation", "delta_bn", "stack_factor", "shift_bn"].concat("national_scale" in c.benefits[0] ? ["national_scale"] : []);
    fs.writeFileSync(path.join(__dirname, "derived", c.name, "benefit_factors.csv"),
      [cols.join(",")].concat(c.benefits.map((r) => cols.map((k) => num(r[k])).join(","))).join("\n") + "\n");
  }
}
console.log("all gates passed");
