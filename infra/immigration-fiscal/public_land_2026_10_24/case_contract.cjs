/* Native-First: read the adopted case through its own evaluator; no second fiscal engine.
   Called by build.py, writes the supplied path. This does not change the case. */
"use strict";
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const P = require("../main_case_2026_10_16/package.cjs");
const C = require("../main_case_2026_10_16/companions.cjs");
const summary = JSON.parse(fs.readFileSync(path.join(ROOT, "main_case_2026_10_16/derived/summary.json"))).v9;
const sum = xs => xs.reduce((a, b) => a + b, 0);
const checks = [];
function gate(name, ok, detail) {
  checks.push({ name, pass: !!ok, detail });
  if (!ok) throw Error("[BLOCKED] public land case contract: " + name + ": " + JSON.stringify(detail));
}
const near = (a, b, tol = 1e-7) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= tol;
gate("adopted oct16", P.CASE_KEY === "oct16" && P.STATUS === "adopted", P.CASE_KEY);
const rate = summary.one_rate.flat_real_equivalent;
gate("required case rate", near(rate, 0.020810698764237804, 1e-15), rate);
const meta = P.capitalMeta(P.withCentral({}));
const byId = Object.fromEntries(meta.components.map(c => [c.id, c]));
const carriers = P.correctionsPayload().meta.union_completion.carriers;
const rows = [], totals = [];
// This arm changes public capital only. Its full-evaluator difference independently checks
// that the line reconstruction carries college, health, completion, coverage and count terms.
const Q7 = P.caseOf(P.OCT05, P.CANDIDATE, { one_rate: "capital_7pct" });
for (let mi = 0; mi < P.METHODS.length; mi++) {
  const method = P.METHODS[mi];
  const model = P.modelFor("central", method, P.withCentral({}));
  const model7 = Q7.modelFor("central", method, Q7.withCentral({}));
  for (let ei = 0; ei < 2; ei++) {
    const end = ["low", "high"][ei], index = summary.end_specifications.set[mi][ei];
    const spec = P.MAIN_SPECS[index], run = P.evaluateFull(model, spec);
    gate(method + "/" + end + " specification", spec.reading === end, index);
    const own = P.POST_ENGINE.coverage.by_end[end].decomposition.line_parts;
    const counts = ["native_minor_calibration", "coverage_tenure"].flatMap(id =>
      C.countParts(P.POST_ENGINE[id], end).map(q => ({ ...q, item: id })));
    const one = run.v9_post_engine.parts.one_rate;
    const col = run.v9_post_engine.parts.public_college_response || [];
    const health = run.v9_post_engine.parts.health_residual_key || [];
    const parts = [];
    for (const component of run.capital.components) {
      const id = component.id, declaration = byId[id];
      gate(method + "/" + end + "/" + id + " declared stock", !!declaration &&
        near(component.stock_charged_bn, declaration.stock_charged_bn, 1e-10), component.stock_charged_bn);
      gate(method + "/" + end + "/" + id + " engine key and response", near(component.return_bn,
        component.stock_charged_bn * component.key * component.response * spec.rate, 1e-10), component.return_bn);
      const completion = run.evaluation.spending.filter(q => carriers[q.id]?.kind === "capital" && carriers[q.id].parent_line === id);
      const engine_bn = component.return_bn * rate / spec.rate;
      const completion_bn = sum(completion.map(q => q.amount_bn * q.response)) * rate / spec.rate;
      const college_bn = sum(col.filter(q => q.kind === "college_capital" && q.source_line === id).map(q => q.delta_bn)) * rate / spec.rate;
      const coverage_bn = sum(own.filter(q => q.source_side === "capital" && q.source_line === id).map(q => q.coverage_bn));
      const count_bn = sum(counts.filter(q => q.economic_class === "capital_return" && q.source_line === id).map(q => q.value_bn));
      const health_bn = sum(health.filter(q => q.side === "capital" && q.source_line === id).map(q => q.delta_bn));
      const full_bn = engine_bn + completion_bn + college_bn + coverage_bn + count_bn + health_bn;
      gate(method + "/" + end + "/" + id + " source rate rescaling", near(
        sum(one.filter(q => q.component === "capital_engine" && q.line === id).map(q => q.delta_bn)),
        engine_bn - component.return_bn, 1e-9), engine_bn);
      const interactions = one.filter(q => ["capital_own_coverage_rate_interaction", "capital_count_interaction"].includes(q.component) && q.source_line === id);
      gate(method + "/" + end + "/" + id + " own parts at case rate", interactions.every(q => q.delta_bn === 0), interactions.length);
      const row = { method, end, specification: index, line: id, physical_line: declaration.of_component || id,
        level: component.level, group: component.group, stock_charged_bn: component.stock_charged_bn,
        key_rule: declaration.key, response_rule: declaration.response, engine_key: component.key,
        engine_response: component.response, engine_at_case_rate_bn: engine_bn, completion_bn,
        college_response_bn: college_bn, coverage_bn, count_bn, health_residual_bn: health_bn,
        full_return_at_case_rate_bn: full_bn, effective_key_times_response: full_bn / (component.stock_charged_bn * rate) };
      rows.push(row); parts.push(full_bn);
    }
    const rebuilt = sum(parts), run7 = Q7.evaluateFull(model7, Q7.MAIN_SPECS[index]);
    const from7 = (run7.cost_bn - run.cost_bn) / (0.07 / rate - 1);
    gate(method + "/" + end + " complete capital response from 7pct arm", near(rebuilt, from7, 1e-6), { rebuilt, from7 });
    totals.push({ method, end, case_cost_bn: run.cost_bn, capital_return_bn: rebuilt, rate_derivative_bn: from7 });
  }
}
const out = { case_key: P.CASE_KEY, status: P.STATUS, rate, band_bn: summary.band_bn,
  rule: "Land uses each physical component's sum of full-return coefficients; fee offsets share the land once. Completion, own coverage, selected count items, college response and health residual retained. No land depreciation.",
  rows, totals, checks };
const dest = process.argv[2];
if (!dest) throw Error("[BLOCKED] usage: node case_contract.cjs <output.json>");
fs.mkdirSync(path.dirname(dest), { recursive: true });
fs.writeFileSync(dest, JSON.stringify(out, null, 1) + "\n");
console.log("case_contract:", rows.length, "rows;", checks.length, "gates pass;", totals.map(x => x.end + "=" + x.capital_return_bn.toFixed(6)).join("; "));
