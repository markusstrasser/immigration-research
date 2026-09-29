/* The legal-status calibration arm, step 3: each arm priced through the adopted package, beside the case (not adopted).
 *
 * The adopted case (../main_case_2026_09_29/package.cjs) reads its status inputs from three files:
 *   - the status stacks, vendored by the September 24 package (main_case_2026_09_24/derived/stack_line_deltas.json,
 *     drift-checked against cps_imputation_keys_2026_09_23/_cache/onbooks_lane_line_deltas.json): the case takes
 *     row4+status_state_aware|central|<method> for both fill-in methods, directly and through every stack factor
 *     (CBO's re-key, the medical and school shifts, the IRS income-tax key, the payroll items);
 *   - the pension summary at 9ea1beb (candidate v4's pensionNet, through git): ratio_net, the Part A accrual and the
 *     self-employment OASDI share;
 *   - the payroll-compliance ratios (candidate v3's PAY, payroll_compliance_2026_09_28/derived/items.json): item 6a's
 *     items.all.central r_cal_raw per receipt line and allocation.
 * A child process per arm (`node price.cjs --arm <name>`) loads the package unchanged with those two reads answered
 * from this lane: the stacks of calibrate.py (derived/stacks.json) in place of the three central row4+status_state_aware
 * payloads, pension.py's numbers (derived/pension.json) in the pinned summary, and payroll.py's ratios
 * (derived/payroll.json) in items.all.central. The CPS lane's cache is reported
 * absent to that process, so the package reads the vendored copy, and every fs write stops it: nothing outside this
 * lane is read differently or written. The child prints each method's cost at every specification of the set and of
 * the cash set (pension4 "cash"), and the lines at 48 and 11.
 *
 * Gates (the parent; [BLOCKED] before anything is written):
 *   1. the adopted flag, through the rebuilt stacks and pension numbers, reproduces the case: 371.4146 / 434.8410
 *      and the cash set 294.7011 / 361.8175 at 1e-4, with the ends at 48 / 11 in both methods;
 *   2. the child for the adopted arm with no substitution at all (--arm none) reproduces the same numbers, so the
 *      hooks change nothing by themselves;
 *   3. every substituted arm reads each of the three files once, and its substitution reaches the model: its federal
 *      income tax receipt differs from the adopted one.
 * Writes derived/arm_bands.csv, derived/arm_lines.csv and derived/summary.json.
 *   node infra/immigration-fiscal/status_calibration_2026_09_30/price.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const ROOT = path.resolve(FISCAL, "..", "..");
const CPS_CACHE = path.join(FISCAL, "cps_imputation_keys_2026_09_23", "_cache", "onbooks_lane_line_deltas.json");
const STACK_FILE = path.join(FISCAL, "main_case_2026_09_24", "derived", "stack_line_deltas.json");
const PENSION_REF = "9ea1beb:infra/immigration-fiscal/pension_accrual_2026_09_28/derived/summary.json";
const PAYROLL_FILE = path.join(FISCAL, "payroll_compliance_2026_09_28", "derived", "items.json");
const STACK_KEY = (k) => `row4+status_state_aware|central|${k}`;
const STACK_NAMES = ["b_hotdeck_union_matched", "b_matched_over_pooled", "audit_rules_alone"];
const ENDS = [48, 11];
const CASE = { set: [371.4146, 434.8410], cash: [294.7011, 361.8175] };
const LINES = { receipts: ["federal_income_tax", "state_local_income_tax", "employee_oasdi", "employer_oasdi", "employee_hi",
  "employer_hi", "self_employment_oasdi_hi", "other_domestic_social_contributions", "general_sales_tax"],
spending: ["social_security", "medicare", "refundable_tax_credits", "medicaid_and_chip_other_medical", "snap"] };

// ---------------------------------------------------------------------------------------------------
// Child: one arm.
function child(arm) {
  const stacks = arm === "none" ? null : JSON.parse(fs.readFileSync(path.join(HERE, "derived", "stacks.json"), "utf8")).stacks[arm];
  const pension = arm === "none" ? null : JSON.parse(fs.readFileSync(path.join(HERE, "derived", "pension.json"), "utf8")).arms[arm];
  const payroll = arm === "none" ? null : JSON.parse(fs.readFileSync(path.join(HERE, "derived", "payroll.json"), "utf8")).arms[arm];
  if (arm !== "none" && (!stacks || !pension || !payroll)) throw new Error(`[BLOCKED] no stacks, pension numbers or payroll ratios for ${arm}`);
  const readFileSync = fs.readFileSync.bind(fs), existsSync = fs.existsSync.bind(fs), execFileSync = cp.execFileSync;
  const same = (p, q) => typeof p === "string" && path.resolve(p) === q;
  const hits = { stack: 0, pension: 0, payroll: 0 };
  fs.existsSync = (p, ...r) => (same(p, CPS_CACHE) ? false : existsSync(p, ...r));
  const answer = (text, r) => { const enc = typeof r[0] === "string" ? r[0] : r[0] && r[0].encoding; return enc ? text : Buffer.from(text); };
  fs.readFileSync = (p, ...r) => {
    if (stacks && same(p, STACK_FILE)) {
      const v = JSON.parse(readFileSync(p, "utf8"));
      for (const k of STACK_NAMES) {
        if (!v.payloads[STACK_KEY(k)]) throw new Error(`[BLOCKED] the vendored stacks have no ${STACK_KEY(k)}`);
        v.payloads[STACK_KEY(k)] = stacks[k];
      }
      hits.stack += 1;
      return answer(JSON.stringify(v, null, 1) + "\n", r);
    }
    if (payroll && same(p, PAYROLL_FILE)) {
      const v = JSON.parse(readFileSync(p, "utf8"));
      const lines = v.items.all.central.lines;
      if (Object.keys(lines).sort().join() !== Object.keys(payroll.r_cal_raw).sort().join()) throw new Error("[BLOCKED] payroll.json's lines are not items.all.central's");
      for (const [id, byA] of Object.entries(payroll.r_cal_raw)) for (const [a, x] of Object.entries(byA)) lines[id][a].r_cal_raw = x;
      hits.payroll += 1;
      return answer(JSON.stringify(v), r);
    }
    return readFileSync(p, ...r);
  };
  cp.execFileSync = (file, args, ...r) => {
    const out = execFileSync(file, args, ...r);
    if (!pension || file !== "git" || !Array.isArray(args) || args[args.length - 1] !== PENSION_REF) return out;
    const J = JSON.parse(out.toString("utf8"));
    J.ratio_net = pension.ratio_net;
    for (const e of ["low", "high"]) {
      J.central_decomposition_net[e].accrual_per_tax_dollar_net = pension.ratio_net;
      J.central_decomposition[e].part_a_accrual_bn = pension.part_a_accrual_bn;
    }
    J.case_components_attrs.se_oasdi_share = pension.se_oasdi_share;
    hits.pension += 1;
    return Buffer.from(JSON.stringify(J));
  };
  for (const f of ["writeFileSync", "appendFileSync", "renameSync", "mkdirSync", "rmSync", "unlinkSync", "copyFileSync", "createWriteStream"]) {
    fs[f] = () => { throw new Error(`[BLOCKED] fs.${f} while pricing an arm`); };
  }
  const P = require(path.join(FISCAL, "main_case_2026_09_29", "package.cjs"));
  const run = (o) => {
    const specs = P.specsFor(o);
    return P.METHODS.map((m) => {
      const model = P.modelFor("central", m, P.withCentral(o));
      return specs.map((s) => P.evaluateFull(model, s, P.MAIN_PROFILE));
    });
  };
  const out = { arm, hits, methods: P.METHODS, set: null, cash: null };
  for (const [name, o] of [["set", {}], ["cash", { pension4: "cash" }]]) {
    const rs = run(o);
    const lines = {};
    for (const side of ["receipts", "spending"]) {
      for (const id of LINES[side]) {
        lines[`${side}:${id}`] = ENDS.map((i) => rs.map((xs) => {
          const row = xs[i].evaluation[side].find((l) => l.id === id);
          if (!row) throw new Error(`[BLOCKED] no ${side} line ${id}`);
          return { amount_bn: row.amount_bn, effect_bn: row.effect_bn };
        }));
      }
    }
    const all = {};
    for (const side of ["receipts", "spending"]) {
      for (const row of rs[0][ENDS[0]].evaluation[side]) {
        all[`${side}:${row.id}`] = ENDS.map((i) => rs.map((xs) => xs[i].evaluation[side].find((l) => l.id === row.id).effect_bn));
      }
    }
    all["capital_return"] = ENDS.map((i) => rs.map((xs) => xs[i].capital.total_bn));
    all["production_gain"] = ENDS.map((i) => rs.map((xs) => xs[i].evaluation.production_gain_bn));
    out[name] = { costs: rs.map((xs) => xs.map((r) => r.cost_bn)), lines, effects: all };
  }
  process.stdout.write(JSON.stringify(out) + "\n");
}

// ---------------------------------------------------------------------------------------------------
// Parent: every arm, the gates, the outputs.
const mean = (xs) => xs.reduce((a, b) => a + b, 0) / xs.length;
function csvRows(file) {
  const [head, ...rows] = fs.readFileSync(file, "utf8").trim().split("\n");
  const keys = head.split(",");
  return rows.map((r) => Object.fromEntries(r.split(",").map((c, i) => [keys[i], c])));
}
function price(arm) {
  const text = execChild(arm);
  const last = text.trim().split("\n").pop();
  return JSON.parse(last);
}
function execChild(arm) {
  return cp.execFileSync(process.execPath, [__filename, "--arm", arm], { maxBuffer: 1 << 28, encoding: "utf8",
    stdio: ["ignore", "pipe", "inherit"] });
}
function parent() {
  const arms = csvRows(path.join(HERE, "derived", "arms.csv"));
  const pension = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "pension.json"), "utf8")).arms;
  const payroll = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "payroll.json"), "utf8")).arms;
  const blocked = (msg) => { console.error(`[BLOCKED] ${msg}`); process.exit(1); };
  const at = (r, which) => ENDS.map((i) => mean(r[which].costs.map((xs) => xs[i])));
  const band = (r, which) => [mean(r[which].costs.map((xs) => Math.min(...xs))), mean(r[which].costs.map((xs) => Math.max(...xs)))];
  const endsOf = (r, which) => r[which].costs.map((xs) => [xs.indexOf(Math.min(...xs)), xs.indexOf(Math.max(...xs))]);
  const fit = (r) => mean(r.set.lines["receipts:federal_income_tax"][0].map((x) => x.amount_bn));

  const none = price("none");
  const results = Object.fromEntries(arms.map((a) => [a.arm, price(a.arm)]));
  const adopted = results.adopted;
  const gates = [];
  const gate = (name, ok, detail) => { gates.push({ gate: name, pass: ok, detail }); console.log(`  ${ok ? "PASS" : "FAIL"} ${name} — ${detail}`); };
  for (const [label, r] of [["rebuilt inputs (adopted flag)", adopted], ["no substitution (--arm none)", none]]) {
    for (const which of ["set", "cash"]) {
      const x = at(r, which), b = band(r, which), e = endsOf(r, which);
      gate(`${label}: the ${which} at 48 / 11 is the case's ${CASE[which].join(" / ")} (1e-4), ends 48 / 11 in both methods`,
        [0, 1].every((k) => Math.abs(x[k] - CASE[which][k]) < 1e-4 && Math.abs(b[k] - x[k]) < 1e-12) && e.every((ij) => ij[0] === 48 && ij[1] === 11),
        `${x.map((v) => v.toFixed(6)).join(" / ")}`);
    }
  }
  const once = (h) => h.stack === 1 && h.pension === 1 && h.payroll === 1;
  gate("the hooks reached the package in every substituted arm (one stack, pension and payroll read each)",
    arms.every((a) => once(results[a.arm].hits)) && Object.values(none.hits).every((x) => x === 0),
    arms.map((a) => `${a.arm} ${Object.values(results[a.arm].hits).join("/")}`).join(", "));
  const diffAdopted = Math.max(...["set", "cash"].flatMap((w) => adopted[w].costs.flatMap((xs, m) => xs.map((v, i) => Math.abs(v - none[w].costs[m][i])))));
  gate("the rebuilt inputs give the adopted case at every specification of both sets (1e-9)", diffAdopted < 1e-9, `max |diff| ${diffAdopted.toExponential(1)}`);
  const moved = arms.filter((a) => a.arm !== "adopted").map((a) => [a.arm, fit(results[a.arm]) - fit(adopted)]);
  gate("every other arm moves the group's federal income tax receipt", moved.every(([, d]) => Math.abs(d) > 1e-6),
    moved.map(([n, d]) => `${n} ${d.toFixed(4)}`).join(", "));
  if (gates.some((g) => !g.pass)) blocked("a gate failed");

  // Outputs.
  const rows = [], lineRows = [];
  const f6 = (x) => (Number.isFinite(x) ? x.toFixed(6) : "");
  for (const a of arms) {
    const r = results[a.arm];
    for (const which of ["set", "cash"]) {
      const x = at(r, which), x0 = at(adopted, which), b = band(r, which), e = endsOf(r, which);
      rows.push([a.arm, a.rule, which, f6(Number(a.total) / 1e6), f6(x[0]), f6(x[1]), f6(x[0] - x0[0]), f6(x[1] - x0[1]),
        (x[0]).toFixed(1) + "–" + (x[1]).toFixed(1), f6(b[0]), f6(b[1]), e.map((ij) => ij.join("/")).join(" "),
        P_METHOD_COSTS(r, which)].join(","));
    }
    for (const [key, byEnd] of Object.entries(r.set.effects)) {
      const d = byEnd.map((ms, k) => mean(ms) - mean(adopted.set.effects[key][k]));
      if (Math.abs(d[0]) > 1e-9 || Math.abs(d[1]) > 1e-9) lineRows.push([a.arm, key, f6(d[0]), f6(d[1])].join(","));
    }
  }
  function P_METHOD_COSTS(r, which) { return r[which].costs.map((xs) => ENDS.map((i) => xs[i].toFixed(6)).join("/")).join(" "); }
  fs.writeFileSync(path.join(HERE, "derived", "arm_bands.csv"), ["arm,rule,which,unauthorized_m,cost_48_bn,cost_11_bn,move_48_bn,move_11_bn,printed,band_low_bn,band_high_bn,ends_by_method,by_method_48_11"].concat(rows).join("\n") + "\n");
  fs.writeFileSync(path.join(HERE, "derived", "arm_lines.csv"), ["arm,line,move_48_bn,move_11_bn"].concat(lineRows).join("\n") + "\n");
  const amounts = (r) => Object.fromEntries(Object.entries(r.set.lines).map(([k, byEnd]) => [k, byEnd.map((ms) => mean(ms.map((x) => x.amount_bn)))]));
  const summary = {
    case: CASE, ends: ENDS, gates,
    arms: Object.fromEntries(arms.map((a) => [a.arm, {
      rule: a.rule, unauthorized_m: Number(a.total) / 1e6,
      set_at_48_11_bn: at(results[a.arm], "set"), cash_at_48_11_bn: at(results[a.arm], "cash"),
      set_move_bn: at(results[a.arm], "set").map((v, k) => v - at(adopted, "set")[k]),
      cash_move_bn: at(results[a.arm], "cash").map((v, k) => v - at(adopted, "cash")[k]),
      set_band_bn: band(results[a.arm], "set"), cash_band_bn: band(results[a.arm], "cash"),
      group_amounts_at_48_11_bn: amounts(results[a.arm]),
      pension: pension[a.arm],
      payroll_largest_ratio_change: payroll[a.arm].largest_change,
    }])),
    note: "beside the case, not adopted: status re-assigned among the group's Mexico-born noncitizens to external totals",
  };
  fs.writeFileSync(path.join(HERE, "derived", "summary.json"), JSON.stringify(summary, null, 1) + "\n");
  console.log(["arm,rule,which,unauthorized_m,cost_48,cost_11,move_48,move_11"].concat(rows.map((r) => r.split(",").slice(0, 8).join(","))).join("\n"));
}

if (process.argv[2] === "--arm") child(process.argv[3]);
else parent();
