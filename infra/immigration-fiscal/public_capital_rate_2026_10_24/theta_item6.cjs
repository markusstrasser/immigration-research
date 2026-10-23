/* Item 6 leg of the theta pairing, priced on the adopted v9 package.

theta = the share of the measured private return above the safe rate that scales with capital (risk premia and
returns to unmeasured or expensed intangibles; rents and market power do not). Item 6 takes the corporate tax on the
job capital at TP-5's normal-return share, 0.37, at the high end; the paired reading counts the tax on the same
scaling share: response = 0.37 + theta * (1 - 0.37). The low end is already at 1, so only the rate moves there.

Pricing: the high-end specification (MAIN_SPECS[11]) with receipt:corporate_capital and receipt:corporate_labor
reset, through evaluateFull (engine plus every v9 post-engine term), averaged over the case's two methods. The
engine carries the union-completion corporate carriers with the override. Three post-engine pieces price
corporate receipts at the source response and are transported by response ratio here: the case's own coverage
line parts and the two selected count items' typed parts (16 and joint 16+17). Rate and corporate legs are
additive; the joint run at the 7% capital arm checks it.

Run: node infra/immigration-fiscal/public_capital_rate_2026_10_24/theta_item6.cjs
Writes derived/theta_item6.json (read by rate_model.py).
*/
"use strict";
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..");
const P = require(path.join(ROOT, "main_case_2026_10_16/package.cjs"));
const C = require(path.join(ROOT, "main_case_2026_10_16/companions.cjs"));
const sum = (a) => a.reduce((x, y) => x + y, 0);
const near = (a, b, t = 1e-6) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) < t;
const fail = (s) => { throw Error("[BLOCKED] theta item6: " + s); };
const CORP = ["corporate_capital", "corporate_labor"];
const checks = [];
const gate = (name, ok, detail) => { checks.push({ check: name, pass: !!ok }); if (!ok) fail(name + " " + JSON.stringify(detail)); };

const item6 = JSON.parse(fs.readFileSync(path.join(ROOT, "job_capital_taxes_2026_10_14/derived/item.json"), "utf8"));
const BASE = item6.lines.corporate.response;
gate("item6 corporate response is {low 1, high 0.37}", BASE.low === 1 && BASE.high === 0.37, BASE);

// Farhi & Gourio (2018), BPEA Fall, 2001-16 column of the MPK - RF spread decomposition, percentage points.
// Table 12 (baseline and capital-mismeasurement models), Table 10 (leverage; AA rate as risk-free; 10-year
// Treasury net of term premium). reads/farhi_gourio_2018.md.
const FG = {
  baseline: { rent: 5.55, risk: 5.23, mismeasurement: 0.09, source: "Table 12, baseline" },
  aa_rate_risk_free: { rent: 5.55, risk: 3.79, mismeasurement: 0, source: "Table 10, AA rate as risk-free rate" },
  term_premium_risk_free: { rent: 5.55, risk: 4.97, mismeasurement: 0, source: "Table 10, 10-year Treasury net of term premium" },
  leverage: { rent: 6.99, risk: 3.81, mismeasurement: 0, source: "Table 10, leverage" },
  bias_constant_10: { rent: 4.79, risk: 5.23, mismeasurement: 0.85, source: "Table 12, constant bias 10 percent" },
  bias_rising_10_30: { rent: 3.27, risk: 5.23, mismeasurement: 2.37, source: "Table 12, rising bias 10-30 percent" },
};
const thetaOf = (x) => (x.risk + x.mismeasurement) / (x.rent + x.risk + x.mismeasurement);
const THETA = { zero: 0, anchor_fg_baseline: thetaOf(FG.baseline) };
for (const [k, v] of Object.entries(FG)) if (k !== "baseline") THETA["fg_" + k] = thetaOf(v);
THETA.one = 1;
const responseOf = (t) => BASE.high + t * (1 - BASE.high);

function cost(X, spec) {
  return sum(P.METHODS.map((method) => X.evaluateFull(X.modelFor("central", method, X.withCentral({})), spec).cost_bn)) / P.METHODS.length;
}
function withResponse(spec, s) {
  const out = { ...spec, line_responses: { ...spec.line_responses } };
  for (const id of CORP) out.line_responses[`receipt:${id}`] = s;
  return out;
}
function leg(Q, which, end, s) {
  const X = which === "cash" ? Q.CASH : Q, spec = X.MAIN_SPECS[end === "low" ? 16 : 11], base = BASE[end];
  gate(`${which}/${end} spec reading`, spec.reading === end, spec.reading);
  for (const id of CORP) gate(`${which}/${end} spec carries ${id} at ${base}`, spec.line_responses[`receipt:${id}`] === base, spec.line_responses[`receipt:${id}`]);
  gate(`${which} item19 passthrough absent centrally`, !X.POST_ENGINE.passthrough_source_tax, null);
  const before = cost(X, spec), after = cost(X, withResponse(spec, s)), f = s / base - 1;
  const cov = (X.POST_ENGINE.coverage?.by_end[end]?.decomposition?.line_parts || []).filter((p) => p.source_side === "receipt" && CORP.includes(p.source_line));
  gate(`${which}/${end} coverage corporate parts present at source response`, cov.length > 0 && cov.every((p) => near(p.source_response, base, 1e-12)), cov.length);
  const count = [];
  for (const id of ["native_minor_calibration", "coverage_tenure"])
    for (const p of C.countParts(X.POST_ENGINE[id], end)) if (p.source_side === "receipt" && CORP.includes(p.source_line)) count.push(p);
  gate(`${which}/${end} count corporate parts typed fiscal_line at source response`, count.every((p) => p.economic_class === "fiscal_line" && near(Number(p.source_response), base, 1e-12)), count.length);
  const engine_bn = after - before, coverage_bn = sum(cov.map((p) => p.coverage_bn)) * f, count_bn = sum(count.map((p) => p.value_bn)) * f;
  return { before_bn: before, engine_bn, coverage_bn, count_bn, total_bn: engine_bn + coverage_bn + count_bn };
}

const Q = P;
const rc = JSON.parse(fs.readFileSync(path.join(ROOT, "main_case_2026_10_16/derived/rate_check.json"), "utf8"));
const out = { base_response: BASE, farhi_gourio_2001_16: {}, theta: {}, checks };
for (const [k, v] of Object.entries(FG)) out.farhi_gourio_2001_16[k] = { ...v, theta: thetaOf(v) };
for (const [name, t] of Object.entries(THETA)) {
  const s = responseOf(t), entry = { theta: t, high_end_corporate_response: s };
  for (const which of ["set", "cash"]) entry[which] = { low: { total_bn: 0, rule: "item 6 already at response 1; rate only" }, high: leg(Q, which, "high", s) };
  out.theta[name] = entry;
}
// Controls: the unmodified runs reproduce arm B; theta 0 is the identity; the corporate leg is linear in the response.
for (const which of ["set", "cash"]) {
  gate(`${which} high reproduces arm B`, near(out.theta.zero[which].high.before_bn, rc.arms.B[which][1], 1e-6), out.theta.zero[which].high.before_bn);
  gate(`${which} theta 0 is the identity`, near(out.theta.zero[which].high.total_bn, 0, 1e-9), out.theta.zero[which].high.total_bn);
  const one = out.theta.one[which].high.total_bn, a = out.theta.anchor_fg_baseline;
  gate(`${which} corporate leg linear in the response`, near(a[which].high.total_bn, one * a.theta, 1e-6), [a[which].high.total_bn, one * a.theta]);
}
// Additivity: at the 7% capital arm, the corporate leg is the same amount.
const Q7 = P.caseOf(P.OCT05, P.CANDIDATE, { one_rate: "capital_7pct" });
const at7 = leg(Q7, "set", "high", 1);
gate("7% arm reproduces rate_check", near(at7.before_bn, rc.arms.capital_7pct.set[1], 1e-6), at7.before_bn);
gate("rate and corporate legs additive (7% arm)", near(at7.total_bn, out.theta.one.set.high.total_bn, 1e-6), [at7.total_bn, out.theta.one.set.high.total_bn]);
out.additivity_at_capital_7pct = { corporate_leg_theta1_bn: at7.total_bn, at_default_rate_bn: out.theta.one.set.high.total_bn };
fs.mkdirSync(path.join(__dirname, "derived"), { recursive: true });
fs.writeFileSync(path.join(__dirname, "derived/theta_item6.json"), JSON.stringify(out, null, 1) + "\n");
for (const [k, v] of Object.entries(out.theta)) console.log(k, v.theta.toFixed(4), v.high_end_corporate_response.toFixed(4), v.set.high.total_bn.toFixed(3), v.cash.high.total_bn.toFixed(3), JSON.stringify(v.set.high));
console.log("checks", checks.length, "all pass");
