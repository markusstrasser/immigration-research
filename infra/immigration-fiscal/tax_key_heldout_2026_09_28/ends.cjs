// Translate a change in the income-tax key's share into the adopted main case (main_case_long_run_2026_09_27).
//
// Reads the share changes heldout.py computes (argv[2]) and writes the case's numbers (argv[3]). For each fill-in
// method it takes the corrected model's final union federal income tax per allocation, checks that it is the
// tax-records stack's factor times the CBO-reweighted share times the national line, and applies each variant's
// change as a receipt edit of stack factor x national x share change. It then reruns every specification: the
// band is each method's minimum and maximum, averaged over the methods, as the case computes it.
//
//   node ends.cjs derived/translation_inputs.json derived/main_case_translation.json
"use strict";
const fs = require("fs");
const path = require("path");

const P = require(path.join(__dirname, "..", "main_case_long_run_2026_09_27", "package.cjs"));
const LINE = "federal_income_tax";
const [inPath, outPath] = process.argv.slice(2);
const input = JSON.parse(fs.readFileSync(inPath, "utf8"));
const oo = P.withCentral({});
const specs = P.MAIN_SPECS;
const ENDS = { low: 48, high: 11 };
const ALLOC = { low: "shared", high: "personal" };

function costs(m) {
  return specs.map((spec) => P.cost(m, spec, P.MAIN_PROFILE));
}
function ends(c) {
  let lo = 0;
  let hi = 0;
  c.forEach((x, i) => { if (x < c[lo]) lo = i; if (x > c[hi]) hi = i; });
  return { low: c[lo], high: c[hi], low_spec: lo, high_spec: hi };
}

const methods = {};
for (const method of P.METHODS) {
  const m = P.modelFor("central", method, oo);
  const line = m.receipts.lines.find((l) => l.id === LINE);
  const cells = line.cells[m.receipts.reference];
  const stack = P.stackFactor(P.STACKS[`row4+status_state_aware|central|${method}`], "receipt", LINE);
  const base = costs(m);
  const out = { national_bn: line.national_bn, reference_scenario: m.receipts.reference, allocations: {}, band: ends(base),
    variants: {} };
  for (const a of ["personal", "shared"]) {
    const target = cells[a].target_bn;
    out.allocations[a] = { final_union_tax_bn: target, final_share: target / line.national_bn, stack_factor: stack[a],
      stack_times_reweighted_bn: stack[a] * line.national_bn * input.reweighted_share[a] };
  }
  for (const [name, v] of Object.entries(input.share_change)) {
    const by = Object.fromEntries(["personal", "shared"].map((a) => [a, stack[a] * line.national_bn * v[a]]));
    const m2 = P.Engine.applyCorrections(m, { lines: [], edits: P.expand([{ side: "receipt", line: LINE, by }]) });
    const c = costs(m2);
    out.variants[name] = { union_tax_change_bn: by, band: ends(c),
      change_at_case_ends_bn: { low: c[ENDS.low] - base[ENDS.low], high: c[ENDS.high] - base[ENDS.high] } };
  }
  // The evaluation charges the cell at each end: spec 48 is shared, spec 11 personal.
  out.evaluated_union_tax_at_ends_bn = {};
  for (const [end, i] of Object.entries(ENDS)) {
    const r = P.evaluateFull(m, specs[i], P.MAIN_PROFILE).evaluation.receipts.find((l) => l.id === LINE);
    out.evaluated_union_tax_at_ends_bn[end] = { spec: i, allocation: specs[i].allocation, amount_bn: r.amount_bn,
      response: r.response };
  }
  methods[method] = out;
}
const mean = (f) => P.METHODS.reduce((s, meth) => s + f(methods[meth]), 0) / P.METHODS.length;
const result = { case: "main_case_long_run_2026_09_27", profile: P.MAIN_PROFILE, ends: ENDS, allocation_at_end: ALLOC,
  methods, band: { low: mean((x) => x.band.low), high: mean((x) => x.band.high) }, variants: {} };
for (const name of Object.keys(input.share_change)) {
  result.variants[name] = {
    band: { low: mean((x) => x.variants[name].band.low), high: mean((x) => x.variants[name].band.high) },
    change_at_case_ends_bn: { low: mean((x) => x.variants[name].change_at_case_ends_bn.low),
      high: mean((x) => x.variants[name].change_at_case_ends_bn.high) },
    union_tax_change_at_case_ends_bn: { low: mean((x) => x.variants[name].union_tax_change_bn[ALLOC.low]),
      high: mean((x) => x.variants[name].union_tax_change_bn[ALLOC.high]) },
    end_specs: P.METHODS.map((meth) => `${methods[meth].variants[name].band.low_spec}/${methods[meth].variants[name].band.high_spec}`),
  };
}
fs.writeFileSync(outPath, JSON.stringify(result, null, 1) + "\n");
