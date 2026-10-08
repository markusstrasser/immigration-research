/* Builds src/generated/figures.json for the figures page.
 *
 * The complete-account figures run main case v6 (adopted 2026-10-07) through its package on the case's
 * payload model (account.cjs): each staircase step and matrix cell is one evaluation per specification,
 * with every response set explicitly. The other figures read lane files, among them the white-reference
 * ledger with item T, the income tax the survey misses (decision 2026-10-07-ledger-item-t-income-tax-keys).
 * Nothing is typed in: the gates reproduce the case's files and the published figures before the file is
 * written, and figures.json lists every input with the sha256 of the bytes read.
 *
 * Run from this directory: node build_data.cjs
 */
"use strict";
const A = require("./account.cjs");
const {
  fs, path, HERE, FISCAL, readJson, readCsv, inputs, P, Engine, model, SPECS, CBO_SCHOOL, SUMMARY, MAIN, CASH, BANDS,
  GG, ENDS, NONE, CASE_CHOICE, costAt, evaluate, RECEIPTS, RECEIPT_MOVES, withReceipts, PROD_SPAN, saneProduction,
  JUSTICE_KEYS, UC_KEYS, S24, PAIRS, withCase, gate, failures, near, round, span,
} = A;

// One row of a lane table, by its fields; a missing or doubled row stops the build.
function one(rows, where, what) {
  const hit = rows.filter((r) => Object.entries(where).every(([k, v]) => r[k] === v));
  if (hit.length !== 1) throw new Error(`${what}: ${hit.length} rows for ${JSON.stringify(where)}`);
  return hit[0];
}
const num = (x) => {
  const v = Number(x);
  if (x === "" || x === undefined || !Number.isFinite(v)) throw new Error(`not a number: ${x}`);
  return v;
};
const atEnds = (xs) => ENDS.map((i) => xs[i]);
const BREAK = path.join(FISCAL, "break_conditions_2026_09_29", "derived");

/* ---------------------------------------------------------------- staircase ----------------- */

/* From the tally commentators quote to the main case, one line at a time, then beyond it. Each step adds
 * its choice to the ones before; every bar is the range over the case's 64 specifications. */
console.log("\n[staircase]");
const pct = (x) => Math.round(100 * x);
const STEPS = [
  { id: "tally", label: "Taxes paid minus benefits received", note: "pension promises counted as they are earned", c: {} },
  { id: "property", label: "Property taxes, as tax bases grow", note: "the long-run share", c: { property: true } },
  { id: "production", label: "Gain from their work", note: "wages, profits and the taxes on them", c: { production: true } },
  { id: "schools", label: "Schools at their full cost per pupil", note: "at the prices of the states they live in", c: { schools: 1 } },
  { id: "colleges", label: "Public colleges, fees and Pell grants", note: "charged by use", c: { colleges: 1 } },
  { id: "police", label: "Police, courts and prisons", note: "charged by use", c: { police: 1 } },
  { id: "health", label: "Public health services", c: { health: 1 } },
  { id: "welfare", label: "Welfare administration, housing, community", c: { welfare: 1 } },
  { id: "constants", label: "Care work, shelter and audit corrections", note: "counted in full", c: { constants: true } },
  { id: "gg", label: `General administration, ${GG.map((g) => g.toFixed(2)).join("–")}`,
    note: "how far administration grows with the population", c: { gg: "case" } },
  { id: "roads", label: "Roads, transport and parks, long run", note: "as their budgets adjust over decades",
    c: { roads: "long_run", parks: "long_run" } },
  { id: "rental", label: "Rental assistance", note: "grows one for one", c: { rental: true } },
  { id: "enterprise", label: "Public enterprises’ losses", note: "transit, utilities, public housing", c: { enterprise: true } },
  { id: "capital", label: `Return on public capital, ${pct(P.RATES.low)}–${pct(P.RATES.high)}%`,
    note: "the cost of the buildings and roads their services use", c: { capital: "D" }, main: true },
  { id: "full", label: "Roads, transport and parks in full", note: "grow one for one", c: { roads: "full", parks: "full" }, beyond: true },
];
const trajectories = SPECS.map(() => []);
{
  let c = { ...NONE };
  for (const step of STEPS) {
    c = { ...c, ...step.c };
    SPECS.forEach((s, i) => trajectories[i].push(costAt(i, c)));
  }
  gate("the case's choices end the main-case step", JSON.stringify(c.capital) === JSON.stringify(CASE_CHOICE.capital)
    && Object.keys(CASE_CHOICE).every((k) => k === "roads" || k === "parks" || c[k] === CASE_CHOICE[k]));
}
const staircase = STEPS.map((step, k) => {
  const total = span(trajectories.map((t) => t[k]));
  const delta = k ? span(trajectories.map((t) => t[k] - t[k - 1])) : null;
  return { id: step.id, label: step.label, note: step.note || null, main: !!step.main, beyond: !!step.beyond,
    total: total.map((x) => round(x)), step: delta && delta.map((x) => round(x)) };
});
const stepAt = (id) => STEPS.findIndex((s) => s.id === id);
const ends = (id) => atEnds(trajectories.map((t) => t[stepAt(id)]));
{
  // The tally is the break-conditions lane's C2 tally: direct receipts less household transfers at the case's
  // ends, on accrual (c2_tally_oct07.csv, four decimals).
  const c2 = readCsv(path.join(BREAK, "c2_tally_oct07.csv"));
  const want = ["low_end_48", "high_end_11"].map((end) => -num(one(c2, { model: "case_accrual", end }, "c2_tally").tally_bn));
  const t = ends("tally");
  gate("tally = the C2 tally on accrual at the band's ends (c2_tally_oct07.csv, 1e-4)",
    ENDS.join() === "48,11" && t.every((x, j) => near(x, want[j], 1e-4)), `${t.map((x) => x.toFixed(4)).join(" / ")}`);
  let worst = 0;
  SPECS.forEach((s, i) => {
    const ev = evaluate(i, NONE).evaluation;
    worst = Math.max(worst, Math.abs(ev.classes.household_transfer.responsive_bn - ev.classes.direct_receipts.responsive_bn - trajectories[i][0]));
  });
  gate("tally = household transfers less direct receipts at every specification (1e-9)", worst < 1e-9, worst.toExponential(1));
  // Each step is its own line: production's is the evaluation's production gain, capital's the return.
  let prodGap = 0, capGap = 0;
  SPECS.forEach((s, i) => {
    const r = evaluate(i, CASE_CHOICE);
    prodGap = Math.max(prodGap, Math.abs(trajectories[i][stepAt("production")] - trajectories[i][stepAt("property")] + r.evaluation.production_gain_bn));
    capGap = Math.max(capGap, Math.abs(trajectories[i][stepAt("capital")] - trajectories[i][stepAt("enterprise")] - r.capital.total_bn));
  });
  gate("the production step is the case's production gain, the capital step its return on public capital (1e-9)",
    prodGap < 1e-9 && capGap < 1e-9, `${prodGap.toExponential(1)} / ${capGap.toExponential(1)}`);
  const w = span(trajectories.map((t) => t[stepAt("enterprise")]));
  gate("the enterprises row = the case without its capital return (summary.json, 1e-9)",
    near(w[0], BANDS.withoutCapital[0], 1e-9) && near(w[1], BANDS.withoutCapital[1], 1e-9), w.map((x) => x.toFixed(4)).join(" to "));
  const m = staircase.find((s) => s.main);
  const mm = span(trajectories.map((t) => t[stepAt("capital")]));
  gate("main-case row = the adopted band (summary.json, 1e-9)", near(mm[0], MAIN[0], 1e-9) && near(mm[1], MAIN[1], 1e-9), `${m.total[0]} to ${m.total[1]}`);
  const p = staircase.at(-1).total;
  gate("last row = the proportional reference (main_case_bands.csv, 1e-4)",
    near(p[0], BANDS.proportional[0], 1e-4) && near(p[1], BANDS.proportional[1], 1e-4), `${p[0]} to ${p[1]}`);
  for (const s of staircase) console.log(`    ${s.label.padEnd(52)} ${s.total.map((x) => x.toFixed(1)).join(" to ")}`);
}

/* The cash reading: pension benefits counted when they are paid (the case's cash set), its tally and band. */
const cashTally = (() => {
  const c2 = readCsv(path.join(BREAK, "c2_tally_oct07.csv"));
  return ["low_end_48", "high_end_11"].map((end) => -num(one(c2, { model: "cash_set", end }, "c2_tally").tally_bn));
})();
{
  const PC = P.CASH, mc = PC.payloadModel();
  const costs = PC.MAIN_SPECS.map((s) => PC.evaluateFull(mc, s).cost_bn);
  gate("the cash package reproduces the cash set (summary.json, 1e-9)",
    near(Math.min(...costs), CASH[0], 1e-9) && near(Math.max(...costs), CASH[1], 1e-9), `${Math.min(...costs).toFixed(4)}–${Math.max(...costs).toFixed(4)}`);
  const t = ENDS.map((i) => {
    const cls = PC.evaluateFull(mc, PC.MAIN_SPECS[i]).evaluation.classes;
    return cls.household_transfer.responsive_bn - cls.direct_receipts.responsive_bn;
  });
  gate("the cash tally = c2_tally_oct07.csv's cash set (1e-4)", t.every((x, j) => near(x, cashTally[j], 1e-4)), t.map((x) => x.toFixed(4)).join(" / "));
}

/* ---------------------------------------------------------------- matrix -------------------- */

/* Every combination of the service choices × general administration. Rental assistance, care work and the
 * audit items, the long-run property taxes, the enterprises and the return on public capital stay as the
 * case has them in every cell. The inner range is the case's own specifications; the outer adds every executed
 * tax-incidence rule, justice and uncompensated-care key, and the production grid with private capital
 * adjusted and no capital owners excluded. */
console.log("\n[matrix]");
gate("sane production grid: 432 scenarios on the case's grid", saneProduction.length === 432, `${PROD_SPAN[0].toFixed(3)} to ${PROD_SPAN[1].toFixed(3)}`);
const ALWAYS = { property: true, constants: true, rental: true, enterprise: true, capital: "D", production: true };
const GG_COLS = [0, GG[0], GG[1], 1];
const ROWS = [{ id: "frozen", schools: 0, colleges: 0, roads: "fixed", frozen: true }];
for (const schools of ["cbo", 1]) for (const colleges of [0, 1]) for (const roads of ["fixed", "long_run", "full"]) {
  ROWS.push({ id: `s${schools}_c${colleges}_${roads}`, schools, colleges, roads });
}
// The outer range's specifications: one per allocation, share, reading and September 24 school response; the
// normalization moves only production, which the grid replaces, and the keys are set below.
const OUTER = SPECS.map((s, i) => i).filter((i) => SPECS[i].normalization === SPECS[0].normalization && SPECS[i].uc === SPECS[0].uc);
gate("the outer range's specifications cover allocation, share, reading and the September 24 school response",
  OUTER.length === 16 && new Set(OUTER.map((i) => [SPECS[i].allocation, SPECS[i].share, SPECS[i].reading, CBO_SCHOOL[i]].join())).size === 16, `${OUTER.length}`);
const choiceOf = (row, g) => ({
  ...NONE, ...ALWAYS, schools: row.schools, colleges: row.colleges, roads: row.roads, parks: row.roads,
  police: row.frozen ? 0 : 1, health: row.frozen ? 0 : 1, welfare: row.frozen ? 0 : 1, gg: g,
});
const matrix = ROWS.map((row) => {
  const cells = GG_COLS.map((g) => {
    const c = choiceOf(row, g);
    const inner = span(SPECS.map((s, i) => costAt(i, c)));
    // welfare = production + the rest, and production depends only on the grid's scenario, so the envelope
    // of the sum is the sum of the envelopes.
    const direct = [];
    for (const sc of RECEIPTS) withReceipts(sc, () => {
      for (const i of OUTER) for (const justice of JUSTICE_KEYS) for (const uc of UC_KEYS) {
        direct.push(costAt(i, { ...c, production: false, justice, uc }));
      }
    });
    const d = span(direct);
    return { gg: g, inner: inner.map((x) => round(x)), outer: [d[0] - PROD_SPAN[1], d[1] - PROD_SPAN[0]].map((x) => round(x)) };
  });
  return { ...row, cells };
});
const rowOf = (schools, colleges, roads) => matrix.find((r) => !r.frozen && r.schools === schools && r.colleges === colleges && r.roads === roads);
const caseCells = (r) => [r.cells[1].inner[0], r.cells[2].inner[1]];
{
  const check = (label, r, want, tol) => {
    const u = caseCells(r);
    gate(label, near(u[0], want[0], tol) && near(u[1], want[1], tol), `${u[0]} to ${u[1]}`);
  };
  check("main-case row at the case's general administration = the adopted band (1e-4)", rowOf(1, 1, "long_run"), MAIN, 1e-4);
  check("colleges-fixed row = long_run_non_school_fixed, adopted (1e-4)", rowOf(1, 0, "long_run"), BANDS.fixedColleges, 1e-4);
  check("roads-and-parks-fixed row = the September 24 profile with rental aid, capital and enterprises (1e-4)",
    rowOf(1, 1, "fixed"), BANDS.roadsFixed, 1e-4);
  check("all-full row = the proportional reference (1e-4)", rowOf(1, 1, "full"), BANDS.proportional, 1e-4);
  const g0 = rowOf(1, 1, "long_run").cells[0].inner;
  gate("main-case row with general administration fixed = general_government_fixed (1e-4)",
    near(g0[0], BANDS.ggFixed[0], 1e-4) && near(g0[1], BANDS.ggFixed[1], 1e-4), `${g0[0]} to ${g0[1]}`);
  gate("outer contains inner in every cell", matrix.every((r) => r.cells.every((x) => x.outer[0] <= x.inner[0] + 1e-9 && x.outer[1] >= x.inner[1] - 1e-9)));
  for (const r of matrix) {
    console.log(`    ${r.id.padEnd(16)} ${r.cells.map((x) => `${x.inner.map((v) => v.toFixed(0)).join("–")} (${x.outer.map((v) => v.toFixed(0)).join("–")})`).join("   ")}`);
  }
}

/* The sign-reversal figures (main_case_2026_10_07/derived/sign_reversal.csv, oct07): reproduced here with the
 * definition inside the case, and the frozen row checked against that definition at s = 0. */
console.log("\n[break-even]");
const signRows = readCsv(path.join(A.CASE, "derived", "sign_reversal.csv"));
const sign = (measure) => {
  const r = one(signRows, { measure }, "sign_reversal.csv");
  return [num(r.oct07_low), num(r.oct07_high)];
};
const breakEven = {
  personal: sign("service_break_even_personal__enterprises_at_s"), shared: sign("service_break_even_shared__enterprises_at_s"),
  personalAt1: sign("service_break_even_personal"), sharedAt1: sign("service_break_even_shared"),
  frozenCapitalFixed: sign("frozen_services_capital_fixed_welfare_bn_cbo_preferred__enterprises_at_s"),
  frozenCapitalFixedAt1: sign("frozen_services_capital_fixed_welfare_bn_cbo_preferred"),
};
{
  const fx = (x) => x.toFixed(4);
  let ok = true;
  const got = [];
  for (const [variant, suffix] of [["enterprises_at_1", ""], ["enterprises_at_s", "__enterprises_at_s"]]) withCase(variant, () => {
    for (const allocation of ["personal", "shared"]) {
      const b = S24.breakEven(model, allocation, PAIRS), want = one(signRows, { measure: `service_break_even_${allocation}${suffix}` }, "sign");
      ok = ok && fx(b[0]) === want.oct07_low && fx(b[1]) === want.oct07_high;
      got.push(`${allocation}${suffix ? " at s" : ""} ${fx(b[0])}/${fx(b[1])}`);
    }
    const f = S24.frozen(model, PAIRS), want = one(signRows, { measure: `frozen_services_capital_fixed_welfare_bn_cbo_preferred${suffix}` }, "sign");
    ok = ok && fx(f[0]) === want.oct07_low && fx(f[1]) === want.oct07_high;
  });
  gate("the sign-reversal definition inside the case reproduces sign_reversal.csv's oct07 columns (four decimals)", ok, got.join("; "));
  // The frozen row at the case's general administration is that definition at s = 0 with the specification's
  // production (private capital adjusted), at every specification.
  // The row's costs come first: withCase wraps the engine, so nothing else may evaluate inside it.
  const frozenRow = matrix.find((r) => r.frozen);
  const own = SPECS.map((s, i) => costAt(i, choiceOf(frozenRow, "case")));
  let worst = 0;
  withCase("enterprises_at_1", () => SPECS.forEach((s, i) => {
    const pair = { end: s.gg === GG[0] ? "least" : "most", g: s.gg, uc: s.uc };
    const production = Object.assign({}, Engine.defaultState(model).production, { normalization: s.normalization });
    const w = S24.welfare(model, s.allocation, 0, pair, production, s.share);
    worst = Math.max(worst, Math.abs(-w - own[i]));
  }));
  gate("the frozen row = the sign-reversal definition at s = 0, every specification (1e-9)", worst < 1e-9, worst.toExponential(1));
  console.log(`    break-even, enterprises with services: personal ${breakEven.personal.map((x) => (100 * x).toFixed(2)).join(" / ")}%, shared ${breakEven.shared.map((x) => (100 * x).toFixed(2)).join(" / ")}%`);
}

/* ---------------------------------------------------------------- who pays ------------------ */

console.log("\n[who pays]");
const DIST = path.join(FISCAL, "distribution_weights_2026_09_23", "derived", "oct07");
const distInputs = readJson(path.join(DIST, "inputs.json"), "distribution");
const quintiles = readCsv(path.join(DIST, "channel_by_quintile.csv"), "distribution").filter((r) => r.measure === "spm");
const CHANNELS = [
  { id: "fiscal_a", label: "Fiscal cost, paid in proportion to taxes" },
  { id: "fiscal_b", label: "Fiscal cost, paid as equal cuts per person" },
  { id: "displaced_beneficiaries", label: "Capped aid others go without" },
  { id: "wages", label: "Wages, after tax" },
  { id: "housing_net", label: "Housing: renters pay, landlords receive" },
  { id: "crime", label: "Crime victims’ harm" },
  { id: "unreimbursed_care", label: "Unpaid hospital care" },
];
const OUTSIDE = ["wages", "housing_net", "crime", "unreimbursed_care"];
const quint = (channel, k) => one(quintiles, { channel, quintile: String(k) }, "channel_by_quintile.csv");
const whoPays = CHANNELS.map((c) => ({
  ...c,
  quintiles: [1, 2, 3, 4, 5].map((k) => {
    const row = quint(c.id, k);
    return { bn: round(num(row.bn), 3), pct: round(num(row.pct_of_resources), 3), perPerson: Math.round(num(row.usd_per_person)) };
  }),
  totalBn: round(num(quint(c.id, 0).bn), 2),
}));
const landlordsTop = num(quint("landlords", 5).bn) / num(quint("landlords", 0).bn);
{
  const a = distInputs.fiscal.adopted;
  gate("who-pays runs on main case v6 (inputs.json fiscal.case oct07, band = summary.json, 1e-9)",
    distInputs.fiscal.case === "oct07" && near(a.band[0], MAIN[0], 1e-9) && near(a.band[1], MAIN[1], 1e-9),
    `${distInputs.fiscal.case}: ${a.band.map((v) => v.toFixed(4)).join("–")}`);
  // The fiscal channel is the budget's part, A_mid plus the capped programmes (their eligible non-recipients'
  // channel), plus the central induced receipts F; the capped programmes are their own channel.
  const D = Object.values(a.capped_programs).reduce((t, v) => t + (v[0] + v[1]) / 2, 0);
  const fa = whoPays.find((c) => c.id === "fiscal_a"), db = whoPays.find((c) => c.id === "displaced_beneficiaries");
  gate("fiscal cost total = A_mid + capped programmes + F, and the capped programmes' channel = −capped (0.01)",
    near(fa.totalBn, a.A_mid + D + distInputs.production.central_F, 0.01) && near(db.totalBn, -D, 0.01),
    `${fa.totalBn} vs ${(a.A_mid + D + distInputs.production.central_F).toFixed(2)}; ${db.totalBn}`);
  gate("each channel's fifths add to its total (1e-6)", CHANNELS.every((c) => near([1, 2, 3, 4, 5].reduce((t, k) => t + num(quint(c.id, k).bn), 0), num(quint(c.id, 0).bn), 1e-6)));
  const channelsSum = ["fiscal_a", "displaced_beneficiaries"].concat(OUTSIDE).reduce((t, id) => t + num(quint(id, 0).bn), 0);
  gate("the channels add to the lane's total (TOTAL_a, 1e-6)", near(channelsSum, num(quint("TOTAL_a", 0).bn), 1e-6), channelsSum.toFixed(3));
  const sumQ = (ks) => OUTSIDE.reduce((t, id) => t + ks.reduce((u, k) => u + num(quint(id, k).bn), 0), 0);
  const bottom = sumQ([1, 2, 3, 4]), top = sumQ([5]);
  gate("outside the budget: bottom four fifths −80.3, top fifth +45.4 (FAQ 4, INDEX; ladder 194)",
    near(bottom, -80.3, 0.05) && near(top, 45.4, 0.05), `${bottom.toFixed(2)} / ${top.toFixed(2)}`);
  gate("landlords' extra receipts: 77% to the top fifth", Math.round(100 * landlordsTop) === 77, (100 * landlordsTop).toFixed(1) + "%");
}

/* ---------------------------------------------------------------- by percentile ------------- */

console.log("\n[by percentile]");
const pctRows = readCsv(path.join(DIST, "channel_by_percentile.csv"), "distribution").filter((r) => r.measure === "spm");
const pctSeries = (channel) => {
  const rows = pctRows.filter((r) => r.channel === channel).sort((x, y) => num(x.percentile) - num(y.percentile));
  if (rows.length !== 100 || rows.some((r, i) => num(r.percentile) !== i + 1)) throw new Error(`channel_by_percentile.csv: ${channel} lacks 100 percentiles`);
  return rows;
};
const TOP1 = ["wages", "housing_net", "crime", "unreimbursed_care", "displaced_beneficiaries"];
const byPercentile = { totalBn: null, series: {}, top1: {} };
for (const conv of ["a", "b"]) {
  const rows = pctSeries(`TOTAL_${conv}`);
  const sums = [0, 1, 2, 3, 4].map((k) => rows.slice(20 * k, 20 * k + 20).reduce((s, r) => s + num(r.bn), 0));
  gate(`percentiles sum to the quintiles, TOTAL_${conv}`, sums.every((s, k) => near(s, num(quint(`TOTAL_${conv}`, k + 1).bn), 1e-6)),
    sums.map((s) => s.toFixed(2)).join(" / "));
  const total = sums.reduce((s, x) => s + x, 0);
  gate(`percentiles sum to the total, TOTAL_${conv}`, near(total, num(quint(`TOTAL_${conv}`, 0).bn), 1e-6), total.toFixed(2));
  byPercentile.totalBn = round(total, 2);
  byPercentile.series[conv] = rows.map((r) => Math.round(num(r.usd_per_person)));
  byPercentile.top1[conv] = Object.fromEntries([["fiscal", "fiscal_" + conv]].concat(TOP1.map((ch) => [ch, ch]))
    .map(([k, ch]) => [k, Math.round(num(pctSeries(ch)[99].usd_per_person))]));
}
{
  const persons = pctSeries("TOTAL_a").reduce((s, r) => s + num(r.persons_m), 0);
  gate("percentiles hold the 295.83m other residents in households", near(persons, 295.83, 0.01), persons.toFixed(3) + "m");
  byPercentile.personsM = round(persons, 2);
  const a = byPercentile.series.a, b = byPercentile.series.b;
  const a99 = a.slice(0, 99);
  let cross = 100;
  while (cross > 1 && b[cross - 2] > 0) cross -= 1;
  byPercentile.stats = {
    aBelowTop: [Math.max(...a99), Math.min(...a99)], aTop: a[99],
    bBottom60: Math.round(b.slice(0, 60).reduce((s, x) => s + x, 0) / 60), bAheadFrom: cross, bTop: b[99],
  };
  gate("top 1% under tax shares sums its channels", near(Object.values(byPercentile.top1.a).reduce((s, x) => s + x, 0), a[99], 3),
    JSON.stringify(byPercentile.top1.a));
  gate("under per-person cuts, the ahead percentiles are the top ones only", b.slice(cross - 1).every((x) => x > 0) &&
    b.slice(0, cross - 1).every((x) => x <= 0), `ahead from percentile ${cross}`);
  // Person by person (winners_losers_2026_09_24, oct07): the share of other residents ahead, pooled in households.
  const WL = path.join(FISCAL, "winners_losers_2026_09_24", "derived", "oct07");
  const wlIn = readJson(path.join(WL, "inputs.json"));
  const shares = readCsv(path.join(WL, "net_shares.csv"));
  const ahead = ["a", "b"].map((k) => num(one(shares, { net: `net_social_${k}`, stack: "central", unit: "spm_unit_pooled" }, "net_shares.csv").winners_share));
  const wlCase = wlIn.case.case === "oct07" && wlIn.published_totals.custody_fiscal.every((x, j) => near(x, MAIN[j], 1e-6));
  gate("person by person: 17.5% / 16.8% ahead (INDEX, ladder 226), on main case v6 (inputs.json case oct07, its band = summary.json)",
    ahead.map((x) => (100 * x).toFixed(1)).join("/") === "17.5/16.8" && wlCase, ahead.map((x) => (100 * x).toFixed(2) + "%").join(" / "));
  byPercentile.aheadShare = ahead.map((x) => round(x, 4));
  console.log(`    tax shares: ${a99[0]} … ${a[98]}, top 1% ${a[99]}; per-person cuts: ${b[0]} … ahead from ${cross}, top 1% ${b[99]}`);
}

/* ---------------------------------------------------------------- crime --------------------- */

console.log("\n[crime]");
const rates = readCsv(path.join(FISCAL, "offender_ethnicity_nibrs_2026_09_23", "derived", "rates_by_spec.csv"));
const OFFENCES = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"];
const crime = OFFENCES.map((offence) => {
  const c = one(rates, { spec: "central", offence }, "rates_by_spec.csv"), b = one(rates, { spec: "alloc=b", offence }, "rates"),
    k = one(rates, { spec: "alloc=c", offence }, "rates");
  return {
    offence,
    victimisations: Math.round(num(c.victimisations)),
    per100k: { hispanic: round(100 * num(c.rate_H), 2), white: round(100 * num(c.rate_NHW), 2), all: round(100 * num(c.rate_all), 2) },
    // Unknown offenders all non-Hispanic (b) or all Hispanic (c).
    hispanicBounds: [round(100 * num(b.rate_H), 2), round(100 * num(k.rate_H), 2)],
    vsWhite: [b.RR_H_NHW, c.RR_H_NHW, k.RR_H_NHW].map((x) => round(num(x), 3)),
    vsAll: [b.RR_H_all, c.RR_H_all, k.RR_H_all].map((x) => round(num(x), 3)),
  };
});
{
  const m = crime[0], r = crime[2];
  gate("murder 2.30 (1.53–3.93) vs white, 1.00 vs all", near(m.vsWhite[1], 2.30, 0.005) && near(m.vsWhite[0], 1.53, 0.005) &&
    near(m.vsWhite[2], 3.93, 0.005) && near(m.vsAll[1], 1.00, 0.005), m.vsWhite.join(" / "));
  gate("robbery 4.22 vs white, 0.92 vs all", near(r.vsWhite[1], 4.22, 0.005) && near(r.vsAll[1], 0.92, 0.005));
}
// US-born Mexican-origin men 18–39 in institutional group quarters against native non-Hispanic white men (ACS).
const inst = readCsv(path.join(FISCAL, "acs_institutional_2026_09_16", "acs_institutional_rates.csv"));
const custodyYears = [...new Set(inst.map((r) => num(r.year)))].sort((x, y) => x - y);
const instRate = (year, group, col) => num(one(inst, { year: String(year), group, nativity: "native",
  block: group === "Mexican" ? "hispanic_origin" : "nh_race" }, "acs_institutional_rates.csv")[col]);
const custody = {
  years: custodyYears,
  // Six decimals: the page prints two, and a ratio stored at three can sit on an exact half.
  ratio: custodyYears.map((y) => round(instRate(y, "Mexican", "pct") / instRate(y, "NH White", "pct"), 6)),
  reallocated: custodyYears.map((y) => round(instRate(y, "Mexican", "pct_adj_generic_hispanic") / instRate(y, "NH White", "pct_adj_generic_hispanic"), 6)),
};
gate("custody 2.56× (2010), 1.91×, 1.72×, 1.94× (2024); 2.10–2.23× reallocated since 2019 (FAQ 12)",
  JSON.stringify(custodyYears) === "[2010,2019,2023,2024]" && custody.ratio.map((x) => x.toFixed(2)).join() === "2.56,1.91,1.72,1.94"
  && custody.reallocated.slice(1).map((x) => x.toFixed(2)).join() === "2.10,2.11,2.23", custody.ratio.join(" / "));
// Victims' harm from the group's offending against other residents, on the account's 39.71M (FAQ 12).
const pairing = readCsv(path.join(FISCAL, "population_basis_2026_09_29", "derived", "restated_pairing.csv"));
const victims = ["low", "high"].map((end) => num(one(pairing, { section: "row", item: "victims", end }, "restated_pairing.csv").restated));
gate("victims' harm $30.5–31.9bn (FAQ 12)", victims.map((x) => x.toFixed(1)).join() === "30.5,31.9", victims.map((x) => x.toFixed(3)).join(" / "));

/* ---------------------------------------------------------------- origins ------------------- */

console.log("\n[origins]");
const ORIGIN_DIR = path.join(FISCAL, "high_skill_origin_screen_2026_09_21", "derived");
const nativeAges = readCsv(path.join(ORIGIN_DIR, "origin_screen_native_ages.csv"));
const screen = readCsv(path.join(ORIGIN_DIR, "origin_screen.csv"))
  .filter((r) => r.education === "all" && r.account === "expanded_excluding_N" && r.allocation === "personal");
const NAMES = {
  mexico_born: "Mexico", india: "India", china_mainland: "China", taiwan_hong_kong: "Taiwan, Hong Kong",
  korea: "Korea", japan: "Japan", philippines: "Philippines", venezuela: "Venezuela",
  pakistan_bangladesh: "Pakistan, Bangladesh", nigeria: "Nigeria", egypt: "Egypt", iran: "Iran",
  russia_ukraine_ussr: "Russia, Ukraine", former_ussr: "Former USSR", poland: "Poland", germany: "Germany",
  united_kingdom: "United Kingdom", canada: "Canada", brazil: "Brazil",
  all_native: "All natives", third_plus_nh_white: "Third-plus whites",
};
const origins = screen.map((s) => {
  const at = (allocation) => one(nativeAges, { origin: s.origin, allocation }, "origin_screen_native_ages.csv");
  const p = at("personal"), sh = at("shared");
  if (!NAMES[s.origin]) throw new Error("unnamed origin " + s.origin);
  return {
    id: s.origin, name: NAMES[s.origin], n: num(s.raw_n_25_64), ba: round(num(s.ba_plus_share_25_64), 4),
    reference: s.origin === "all_native" || s.origin === "third_plus_nh_white",
    personal: { v: Math.round(num(p.native_age_mix)), se: Math.round(num(p.native_age_mix_se_approx)) },
    shared: { v: Math.round(num(sh.native_age_mix)), se: Math.round(num(sh.native_age_mix_se_approx)) },
  };
});
{
  const mx = origins.find((o) => o.id === "mexico_born"), ind = origins.find((o) => o.id === "india");
  gate("Mexico-born −5,360 and India +24,258 per adult at native ages, with item T (the screen's RESULT)",
    mx.personal.v === -5360 && ind.personal.v === 24258, `${mx.personal.v} / ${ind.personal.v}`);
  gate("every origin in the screen has both allocations", origins.length === 21, String(origins.length));
}
// Mexico-born adults 25–64 against natives with the same schooling, common ages, expanded account with item T.
const EDU = readCsv(path.join(FISCAL, "education_origin_fiscal_2026_09_19", "derived", "comparisons.csv"));
const eduRow = (allocation, education, reference_education) => one(EDU, {
  allocation, account: "expanded_excluding_N", origin: "mexico_born", education, entry: "stock", reference: "all_native",
  reference_education, metric: "common_age_gap_per_person", selected_bands: "25-34,35-44,45-54,55-64" }, "comparisons.csv");
const EDU_ROWS = [["lt_hs", "lt_hs"], ["hs_only", "hs_only"], ["lt_hs", "all"]];
const education = EDU_ROWS.map(([e, r]) => {
  const x = eduRow("shared", e, r);
  return { education: e, reference: r, v: Math.round(num(x.estimate)), lo: Math.round(num(x.ci95_low)), hi: Math.round(num(x.ci95_high)) };
});
{
  const personal = EDU_ROWS.map(([e, r]) => Math.round(num(eduRow("personal", e, r).estimate)));
  gate("schooling comparisons with item T: shared +1,908 [+40, +3,777] (education memo), personal +1,779 / −2,950 / −18,792 (the lane's RESULT)",
    education[0].v === 1908 && education[0].lo === 40 && education[0].hi === 3777 && personal.join() === "1779,-2950,-18792",
    `${education.map((x) => x.v).join(" / ")}; personal ${personal.join(" / ")}`);
}

/* ---------------------------------------------------------------- generation ledger --------- */

/* The white-reference ledger (ledger_absolute_2026_09_17), expanded account with item T, shared allocation:
 * age profiles, the categories at two age structures, the generation gaps and lifetime values. */
console.log("\n[ledger]");
const LEDGER = path.join(FISCAL, "ledger_absolute_2026_09_17", "derived");
const audit = readJson(path.join(LEDGER, "audit.json"));
{
  const crypto = require("crypto");
  const got = crypto.createHash("sha256").update(fs.readFileSync(path.join(LEDGER, "age_profiles.csv"))).digest("hex");
  gate("age_profiles.csv (ignored) is the export the tracked audit.json fingerprints", got === audit.age_profile_export.files["age_profiles.csv"], got.slice(0, 8));
}
const profiles = readCsv(path.join(LEDGER, "age_profiles.csv"));
const BANDS_AGE = ["0–17", "18–24", "25–34", "35–44", "45–54", "55–64", "65–74", "75+"];
const profileOf = (group) => {
  const rows = BANDS_AGE.map((b, k) => one(profiles, { allocation: "shared", account: "expanded", group, band: String(k) }, "age_profiles.csv"));
  return { pop: rows.map((r) => round(num(r.population), 4)), rate: rows.map((r) => round(num(r.net_per_person), 4)),
    total: rows.reduce((t, r) => t + num(r.net_total), 0) / 1e9 };
};
const mexicanAges = profileOf("mexican_observed_total"), whiteAges = profileOf("third_plus_nh_white");
const CATS = readCsv(path.join(LEDGER, "age_normalizations_by_category.csv"));
const CATEGORY_LABELS = {
  public_medical: "Public medical", cash_transfers_incl_social_security: "Social Security and other cash",
  k12_schooling: "Schools", institutions: "Institutions", rest_of_federal_budget: "Rest of federal budget",
  sales_excise_property_tax: "Sales, excise, property tax", corporate_tax_incidence: "Corporate tax",
  state_local_services_capital: "State and local services", income_payroll_tax: "Income and payroll tax", noncash_aid: "Noncash aid",
};
const catTotal = (structure, category) => num(one(CATS, { allocation: "shared", structure, group: "mexican_observed_total", category },
  "age_normalizations_by_category.csv").total_bn);
const categories = Object.entries(CATEGORY_LABELS).map(([id, label]) => ({
  id, label, own: round(catTotal("own_ages_today", id), 2), white: round(catTotal("white_ages_today", id), 2) }));
const NORMS = readCsv(path.join(LEDGER, "age_normalizations.csv"));
const norm = (allocation, structure, group) => one(NORMS, { allocation, structure, group }, "age_normalizations.csv");
const STRUCTURES = ["own_ages_today", "white_ages_today", "union_ages_today", "stationary_life_course"];
const ageGaps = Object.fromEntries(STRUCTURES.map((st) => [st, Math.round(num(norm("shared", st, "mexican_observed_total").net_gap_vs_white))]));
{
  const sum = (xs) => xs.reduce((t, x) => t + x, 0);
  const all = (st) => sum(Object.keys(CATS.reduce((o, r) => Object.assign(o, { [r.category]: 1 }), {})).map((c) => catTotal(st, c)));
  gate("the ten categories are every nonzero one (the rest is enforcement, defense and interest at 0)",
    Math.abs(all("own_ages_today") - sum(categories.map((c) => c.own))) < 0.01 && Math.abs(all("white_ages_today") - sum(categories.map((c) => c.white))) < 0.01);
  const pop = sum(mexicanAges.pop);
  const atWeights = (w) => sum(mexicanAges.rate.map((r, i) => r * w[i])) * pop / 1e9;
  const shW = whiteAges.pop.map((p) => p / sum(whiteAges.pop));
  gate("the age profiles give the categories' totals at their own ages and at white ages (0.05)",
    near(mexicanAges.total, all("own_ages_today"), 0.05) && near(atWeights(shW), all("white_ages_today"), 0.05),
    `${mexicanAges.total.toFixed(2)} / ${atWeights(shW).toFixed(2)} against ${all("own_ages_today").toFixed(2)} / ${all("white_ages_today").toFixed(2)}`);
  gate("the gap at own ages −5,276 and at white ages −8,236 (FAQ 5, with item T)", ageGaps.own_ages_today === -5276 && ageGaps.white_ages_today === -8236,
    JSON.stringify(ageGaps));
}
// The gap on any common age structure (white ages, the union's, a stationary life course), and what the group's
// young structure hides: the common gap less the gap at its own ages.
const commonGap = span(["white_ages_today", "union_ages_today", "stationary_life_course"].map((st) => ageGaps[st]));
const youngHides = [ageGaps.own_ages_today - commonGap[1], ageGaps.own_ages_today - commonGap[0]];
const GEN_GROUPS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"];
const generations = Object.fromEntries(["shared", "personal"].map((allocation) => {
  const rows = GEN_GROUPS.map((g) => norm(allocation, "white_ages_today", g));
  return [allocation, {
    // Spending is negative on the ledger, so a group that receives less than whites has a positive gap.
    receipts: rows.map((r) => Math.round(num(r.receipts_gap_vs_white))),
    spending: rows.map((r) => Math.round(num(r.spending_gap_vs_white))),
    net: rows.map((r) => Math.round(num(r.net_gap_vs_white))),
  }];
}));
{
  gate("generation gaps at white ages: shared −8,791 / −8,420 / −7,039, personal −9,180 / −7,609 / −7,074 (FAQ 5)",
    generations.shared.net.join() === "-8791,-8420,-7039" && generations.personal.net.join() === "-9180,-7609,-7074",
    `${generations.shared.net.join(" / ")}; ${generations.personal.net.join(" / ")}`);
  gate("each generation's net is its taxes less its benefits gap (±1 for rounding)",
    ["shared", "personal"].every((a) => generations[a].net.every((n, k) => Math.abs(n - (generations[a].receipts[k] + generations[a].spending[k])) <= 1)));
}
// Lifetime values from birth at 3%, personal allocation (the lifetime lane's primary), from the ignored
// period_profiles.csv, which must agree with the tracked stationary life-course rows at 0%.
const LIFE = readCsv(path.join(LEDGER, "lifetime", "period_profiles.csv"));
const lifeRow = (allocation, group, rate) => one(LIFE, { allocation, account: "expanded", group, survival: "common_total", mortality_table: "total",
  horizon: "full_100plus", start_age: "0", real_discount_rate: rate }, "period_profiles.csv");
const LIFE_GROUPS = ["mexican_second_gen", "mexican_third_plus_selfid", "third_plus_nh_white"];
const lifetime = LIFE_GROUPS.map((g) => Math.round(num(lifeRow("personal", g, "0.03").period_profile_npv)));
{
  let worst = 0;
  for (const allocation of ["shared", "personal"]) for (const g of GEN_GROUPS.concat(["mexican_observed_total", "third_plus_nh_white", "all_native"])) {
    const r = lifeRow(allocation, g, "0.0");
    worst = Math.max(worst, Math.abs(num(r.period_profile_npv) / num(r.discounted_person_years) - num(norm(allocation, "stationary_life_course", g).net_per_person)));
  }
  gate("lifetime values at 0% per person-year = the tracked stationary life course (age_normalizations.csv, $0.01)", worst < 0.01, `max |diff| $${worst.toFixed(4)}`);
  gate("lifetime from birth at 3%: −$267k, −$215k, −$68k (FAQ 5)", lifetime.map((x) => Math.round(x / 1000)).join() === "-267,-215,-68", lifetime.join(" / "));
}
// The complete account's own split by generation (generation_account_2026_09_24, oct07): no reference group,
// children counted with their parents (b) or in their own generation (a). Not the gaps above, rescaled.
const GENACC = readCsv(path.join(FISCAL, "generation_account_2026_09_24", "derived", "generation_results_oct07.csv"));
const caseSplit = Object.fromEntries(["a", "b"].map((conv) => [conv, ["G1", "G2", "G3plus"].map((g) =>
  ["low", "high"].map((band_end) => round(num(one(GENACC, { convention: conv, generation: g, band_end }, "generation_results_oct07.csv").cost_bn), 3)))]));
gate("the case's generation split adds to the case at both ends, under both conventions (1e-5)",
  ["a", "b"].every((conv) => [0, 1].every((j) => near(GENACC.filter((r) => r.convention === conv && r.band_end === ["low", "high"][j])
    .reduce((t, r) => t + num(r.cost_bn), 0), MAIN[j], 1e-5))), JSON.stringify(caseSplit));

/* ---------------------------------------------------------------- places -------------------- */

/* The union against local third-plus non-Hispanic whites, shared all-age ledger with item T, $ per standardized
 * person (ledger_stress and metro_match, *_T.csv, ignored). Each value is checked against its lane's RESULT. */
console.log("\n[places]");
const STATE = readCsv(path.join(FISCAL, "ledger_stress_2026_09_17", "derived", "state_matched_T.csv"));
const METRO = readCsv(path.join(FISCAL, "metro_match_2026_09_17", "derived", "metro_matched_T.csv"));
const placeRow = (rows, cells, reference) => one(rows, { scenario: "all_age_shared", target: "mexican_observed_total", reference, cells,
  metric: "standardized_gap_per_person" }, "places");
const shares = readCsv(path.join(FISCAL, "political_trajectory_county_2026_09_19", "derived", "ca_tx_series.csv"));
const share2024 = (st) => num(one(shares, { state: st, year: "2024" }, "ca_tx_series.csv").mex_share_pop_pp);
const PLACES = [
  { name: "Los Angeles", rows: METRO, cells: "los_angeles_age_4" },
  { name: "California", rows: STATE, cells: "CA_age", state: "CA" },
  { name: "Chicago", rows: METRO, cells: "chicago_age_4" },
  { name: "Dallas–Fort Worth", rows: METRO, cells: "dallas_age_4" },
  { name: "Riverside–San Bernardino", rows: METRO, cells: "riverside_age_4" },
  { name: "Texas", rows: STATE, cells: "TX_age", state: "TX" },
  { name: "Houston", rows: METRO, cells: "houston_age_4" },
  { name: "Phoenix", rows: METRO, cells: "phoenix_age_4" },
  { name: "National, age only", rows: METRO, cells: "age_4", national: true },
];
const places = PLACES.map((p) => {
  const w = placeRow(p.rows, p.cells, "third_plus_nh_white"), n = placeRow(p.rows, p.cells, "all_native");
  return {
    name: p.name, v: Math.round(num(w.estimate)), lo: Math.round(num(w.ci95_low)), hi: Math.round(num(w.ci95_high)),
    vsNatives: Math.round(num(n.estimate)), peopleM: round(num(w.population) / 1e6, 2),
    share: p.state ? round(share2024(p.state), 1) : null, national: !!p.national, state: p.state || null,
  };
});
const tConc = readCsv(path.join(FISCAL, "ledger_stress_2026_09_17", "derived", "t_concentration.csv"));
const topTenShare = Object.fromEntries(["CA", "TX"].map((st) => [st, round(num(one(tConc, { cell: `${st}|third_plus_nh_white` }, "t_concentration.csv").top10_units_share), 3)]));
{
  const at = (name) => places.find((p) => p.name === name);
  const pub = (p, v, lo, hi) => p.v === v && p.lo === lo && p.hi === hi;
  gate("with item T: California −15,228 [−18,291, −12,164], Texas −9,267 [−12,530, −6,004] (ledger_stress RESULT)",
    pub(at("California"), -15228, -18291, -12164) && pub(at("Texas"), -9267, -12530, -6004));
  gate("Los Angeles −21,083 [−27,783, −14,383], Riverside −11,944 [−23,967, +79], age only −6,910 [−7,765, −6,055] (metro_match RESULT)",
    pub(at("Los Angeles"), -21083, -27783, -14383) && pub(at("Riverside–San Bernardino"), -11944, -23967, 79) && pub(at("National, age only"), -6910, -7765, -6055));
  gate("the ten largest white households carry 67% of California whites' item T and 98% of Texas whites' (ledger_stress RESULT)",
    Math.round(100 * topTenShare.CA) === 67 && Math.round(100 * topTenShare.TX) === 98, JSON.stringify(topTenShare));
  gate("California and Texas are both about 32% Mexican-origin in 2024", Math.round(at("California").share) === 32 && Math.round(at("Texas").share) === 32,
    `${at("California").share}% / ${at("Texas").share}%`);
}

/* ---------------------------------------------------------------- sentences ----------------- */

console.log("\n[back-cast]");
// The whole-budget back-cast of main case v6: each year is the envelope of the flat, ratio and income rules at
// the band's two ends; flat carries the 2024 level. 2024 is the measured account; earlier years are a model.
const BACKCAST = path.join(FISCAL, "historical_backcast_2026_09_20", "derived", "oct07");
const CONCEPT = "net_cost_cbo_informed_oct07";
const annual = readCsv(path.join(BACKCAST, "backcast_annual.csv"), "backcast");
const RULES = ["low", "high"].flatMap((end) => ["flat", "ratio", "income"].map((rule) => `${CONCEPT}_${end}__${rule}`));
const PER_MEMBER = ["low", "high"].flatMap((end) => ["ratio", "income"].map((rule) => `${CONCEPT}_${end}__${rule}__per_lineage_member_usd`));
for (const c of RULES.concat(PER_MEMBER, ["lineage_millions"])) if (!(c in annual[0])) throw new Error("no back-cast column " + c);
const backcast = annual.map((row) => {
  const v = RULES.map((c) => num(row[c])), pm = PER_MEMBER.map((c) => num(row[c]));
  return { year: num(row.year), lo: round(Math.min(...v), 1), hi: round(Math.max(...v), 1),
    perMember: [Math.round(Math.min(...pm)), Math.round(Math.max(...pm))] };
});
{
  const y24 = one(annual, { year: "2024" }, "backcast_annual.csv");
  const ends24 = ["low", "high"].map((e) => num(y24[`${CONCEPT}_${e}__flat`]));
  gate("back-cast 2024 = the adopted band (4 decimals)", near(ends24[0], MAIN[0], 1e-4) && near(ends24[1], MAIN[1], 1e-4), ends24.join(" to "));
  const pm = PER_MEMBER.map((c) => num(y24[c]));
  const want = SUMMARY.v6.per_member_usd.set;
  gate("2024 per lineage member = the case's per-member figure (summary.json v6, $0.01)",
    near(Math.min(...pm), want[0], 0.01) && near(Math.max(...pm), want[1], 0.01) && near(num(y24.lineage_millions), SUMMARY.v6.per_member_usd.population / 1e6, 1e-4),
    `${pm.map((x) => x.toFixed(2)).join(" / ")}`);
  gate("back-cast covers 2005–2024", backcast.length === 20 && backcast[0].year === 2005 && backcast.at(-1).year === 2024);
}
const windows = readCsv(path.join(BACKCAST, "backcast_windows.csv"), "backcast").filter((r) => r.concept.startsWith(CONCEPT + "_"));
const win = (col) => span(windows.map((r) => num(r[col]))).map((x) => round(x, 3));
const backcastWindows = { ten: win("10y_2015_2024"), fifteen: win("15y_2010_2024"), twenty: win("20y_2005_2024") };
gate("back-cast windows: six rules and ends, the 2024 anchor's", windows.length === 6, backcastWindows.ten.join(" to ") + " $tn over ten years");

console.log("\n[sentences]");
// Real national spending per resident, 2024 = 1, five programmes.
const PROG = readCsv(path.join(FISCAL, "historical_backcast_2026_09_20", "derived", "national_programme_index.csv"));
const programmeYears = Object.keys(PROG[0]).filter((k) => /^\d{4}$/.test(k)).map(Number);
const PROGRAMMES = { refundable_tax_credits: "Credits", medicaid_and_chip_other_medical: "Medicaid", medicare: "Medicare", school: "Schools", public_order_safety: "Police, courts" };
const programmes = Object.entries(PROGRAMMES).map(([id, name]) => {
  const r = one(PROG, { programme: id }, "national_programme_index.csv");
  return { id, name, v: programmeYears.map((y) => num(r[String(y)])) };
});
gate("programme index: every series is 1 in 2024", programmes.every((p) => p.v[programmeYears.indexOf(2024)] === 1), programmeYears.join(" "));
// Recent arrivals, ages 25–54, within five years of arrival: the share without a high-school diploma (IPUMS).
const ENTRY = readCsv(path.join(FISCAL, "arrival_cohorts_2026_09_18", "derived", "entry_quality_fixed_duration_ipums.csv"))
  .filter((r) => r.worker_def === "emp" && r.max_ysm === "5").sort((x, y) => num(x.survey_year) - num(y.survey_year));
// "1975-1980" prints as "1975–80", "1995-2000" as "1995–2000".
const windowLabel = (w) => {
  const [a, b] = w.split("-");
  if (!/^\d{4}$/.test(a) || !/^\d{4}$/.test(b)) throw new Error("arrival window " + w);
  return `${a}–${a.slice(0, 2) === b.slice(0, 2) ? b.slice(2) : b}`;
};
const schooling = ENTRY.map((r) => ({ year: num(r.survey_year), window: windowLabel(r.arrival_window), lths: round(100 * num(r.sh_lths), 1) }));
gate("arrivals without a diploma 82.5% (1975–80) to 33.3% (2018–23)", schooling[0].lths === 82.5 && schooling.at(-1).lths === 33.3 && schooling.length === 5
  && schooling.map((x) => x.window).join() === "1975–80,1985–90,1995–2000,2005–10,2018–23",
  schooling.map((s) => s.lths).join(" / "));
// The partial account with item T, common-age gap per standardized person against whites, by arrival window.
const WIN = readCsv(path.join(FISCAL, "arrival_window_fiscal_2026_09_18", "derived", "window_estimates.csv"));
const winGap = (window) => Math.round(num(one(WIN, { window, reference: "third_plus_nh_white", matching: "common_support",
  metric: "partial_plus_T_common_age_gap_per_person_common_support" }, "window_estimates.csv").estimate));
const fiscalWindows = { recent: winGap("w5_2016_2025"), older: span(["w1_pre1990", "w2_1990_1999", "w3_2000_2009", "w4_2010_2015"].map(winGap)) };
gate("arrival windows with item T: 2016–2025 −5,498; older −7,013 to −6,615 (the lane's RESULT)",
  fiscalWindows.recent === -5498 && fiscalWindows.older.join() === "-7013,-6615", JSON.stringify(fiscalWindows));
// Mexican-origin income against the national figure (ACS), the back-cast's income input.
const ACS = readCsv(path.join(FISCAL, "historical_backcast_2026_09_20", "inputs", "acs_mexican_origin.csv"))
  .filter((r) => r.per_capita_income_mexican !== "");
const ratio = (r, a, b) => round(num(r[a]) / num(r[b]), 4);
const incomeRatios = {
  years: ACS.map((r) => num(r.year)),
  perCapita: ACS.map((r) => ratio(r, "per_capita_income_mexican", "per_capita_income_total")),
  household: ACS.map((r) => ratio(r, "median_household_income_mexican", "median_household_income_total")),
  men: ACS.map((r) => ratio(r, "median_earnings_ftyr_male_mexican", "median_earnings_ftyr_male_total")),
};
gate("income per person 0.52 (2008) to 0.61 (2024) of the national figure; household 0.78 to 0.91",
  incomeRatios.years[0] === 2008 && incomeRatios.years.at(-1) === 2024 && incomeRatios.perCapita[0].toFixed(2) === "0.52"
  && incomeRatios.perCapita.at(-1).toFixed(2) === "0.61" && incomeRatios.household[0].toFixed(2) === "0.78" && incomeRatios.household.at(-1).toFixed(2) === "0.91",
  `${incomeRatios.years.length} years`);
// India-born earnings gap against US-born non-Hispanic whites, by occupation (ACS 2023).
const KIT = readCsv(path.join(FISCAL, "indian_generation_2026_09_21", "derived", "occ_kitagawa.csv"));
const DETAILED = "software+other_computer+cis_manager+computer_hardware+math+physician+other_healthcare+other_engineer+other_manager+rest";
const kit = (focal) => {
  const r = one(KIT, { source: "acs2023_employed_25_64", focal, ref: "us_born_nh_white", bins: DETAILED }, "occ_kitagawa.csv");
  return { gap: Math.round(num(r.raw_gap)), mix: Math.round(num(r.mix)), within: Math.round(num(r.within)), interaction: Math.round(num(r.interaction)) };
};
const kitagawa = { india: kit("india_born"), recent: kit("india_born_recent_noncit") };
gate("India-born $48,056 above whites: $24,785 from occupations, $22,825 within them", kitagawa.india.gap === 48056 && kitagawa.india.mix === 24785
  && kitagawa.india.within === 22825 && kitagawa.recent.mix > kitagawa.recent.gap);
// The September 19 per-person ledger's convention hulls, with item T (ledger_recut_2026_09_22).
const HULLS = readCsv(path.join(FISCAL, "ledger_recut_2026_09_22", "derived", "hulls.csv"));
const hull = (id) => { const r = one(HULLS, { hull: id }, "hulls.csv"); return [num(r.low_bn), num(r.high_bn), num(r.central_bn)].map((x) => round(x, 2)); };
const hulls = { practitioner: hull("practitioner"), design: hull("design_grid") };
gate("the union balance (the hulls' central) is the categories' total at own ages, −$203.5bn with item T (0.05)",
  near(hulls.practitioner[2], categories.reduce((t, c) => t + c.own, 0), 0.05) && near(hulls.practitioner[2], -203.52, 0.005),
  `practitioner ${hulls.practitioner.join(" / ")}; design ${hulls.design.join(" / ")}`);

/* ---------------------------------------------------------------- the page's sentences ------ */

// Claims the figures' text makes in words. A rebuild that would leave a sentence false stops here.
console.log("\n[claims in the text]");
{
  const at = (id) => staircase[stepAt(id)].total;
  const first = staircase.findIndex((s) => s.total[0] > 0);
  gate("staircase: the tally's range crosses zero; property taxes and the gain from their work leave everyone else better off; "
    + "schools are the first row worse off at every choice, and every row after them is", at("tally")[0] < 0 && at("tally")[1] > 0
    && at("property")[1] < 0 && at("production")[1] < 0 && staircase[first].id === "schools" && staircase.slice(first).every((s) => s.total[0] > 0));
  const services = matrix.filter((r) => !r.frozen).flatMap((r) => r.cells);
  const frozen = matrix.find((r) => r.frozen).cells;
  gate("matrix: every combination that charges for services is worse off over every executed alternative",
    services.every((c) => c.outer[0] > 0), `outer ${round(Math.min(...services.map((c) => c.outer[0])), 1)} to ${round(Math.max(...services.map((c) => c.outer[1])), 1)}`);
  gate("matrix: with every service frozen, everyone else is better off only with general administration fixed too (inner ranges)",
    frozen[0].inner[1] < 0 && frozen.slice(1).every((c) => c.inner[0] > 0), frozen.map((c) => c.inner.map((x) => x.toFixed(1)).join(" to ")).join("; "));
  gate("matrix: FAQ 2's frozen services leave everyone else from better off to worse off (enterprises with services, capital fixed)",
    breakEven.frozenCapitalFixed[0] < 0 && breakEven.frozenCapitalFixed[1] > 0);
  gate("break-even: the most adverse end is worse off at every service response, the least adverse better off only below a small share",
    breakEven.personal[0] < 0 && breakEven.shared[0] < 0 && breakEven.personal[1] > 0 && breakEven.shared[1] > 0 && Math.max(breakEven.personal[1], breakEven.shared[1]) < 0.1);
  gate("ages: at every working age (18–64) the group's net falls short of the white one",
    [1, 2, 3, 4, 5].every((i) => mexicanAges.rate[i] < whiteAges.rate[i]));
  gate("generations: the second generation's tax gap is over $3,000 smaller than the first's, its benefit-use advantage under a quarter of it, "
    + "and every generation's net gap exceeds $7,000", ["shared", "personal"].every((a) => {
    const g = generations[a];
    return g.receipts[1] - g.receipts[0] > 3000 && g.spending[1] < g.spending[0] / 4 && g.net.every((n) => n < -7000);
  }));
  const printed = (conv, j) => caseSplit[conv].map((g) => Math.round(10 * g[j]) / 10);
  gate("the case's generation split printed to one decimal adds to the case's printed ends",
    ["a", "b"].every((conv) => [0, 1].every((j) => near(printed(conv, j).reduce((t, x) => t + x, 0), Math.round(10 * MAIN[j]) / 10, 1e-9))),
    ["a", "b"].map((conv) => [0, 1].map((j) => printed(conv, j).join(" + ")).join(" | ")).join("; "));
  gate("the long-run responses the matrix names for roads and parks are the specifications' own",
    [["economic_affairs_services", "low"], ["economic_affairs_services", "high"], ["recreation_culture", "low"], ["recreation_culture", "high"]]
      .every(([id, r]) => SPECS.some((s) => s.reading === r && s.line_responses[id] === P.LINE_RESPONSES[id][r]))
    && SPECS.every((s) => ["economic_affairs_services", "recreation_culture"].every((id) => s.line_responses[id] === P.LINE_RESPONSES[id][s.reading])));
  const p = (name) => places.find((x) => x.name === name);
  gate("places: California's gap exceeds Texas's and Los Angeles's exceeds Houston's", p("California").v < p("Texas").v && p("Los Angeles").v < p("Houston").v,
    `CA/TX ${(p("California").v / p("Texas").v).toFixed(2)}, LA/Houston ${(p("Los Angeles").v / p("Houston").v).toFixed(2)}`);
  const edge = p("California").hi - p("Texas").lo;
  gate("places: California's and Texas's intervals overlap only at their edges (by under $1,000, neither estimate inside the other's interval)",
    edge > 0 && edge < 1000 && p("California").v < p("Texas").lo && p("Texas").v > p("California").hi, `$${edge}`);
  gate("percentiles: about one person in six is ahead counted person by person, under both financing rules",
    byPercentile.aheadShare.every((x) => x > 0.15 && x < 0.185), byPercentile.aheadShare.join(" / "));
  gate("back-cast: everyone else is worse off in every year, at every rule and end", backcast.every((b) => b.lo > 0),
    `lowest ${Math.min(...backcast.map((b) => b.lo))}`);
  gate("who pays: the capped programmes' cost falls mostly on the bottom fifth",
    whoPays.find((c) => c.id === "displaced_beneficiaries").quintiles[0].bn / whoPays.find((c) => c.id === "displaced_beneficiaries").totalBn > 0.7);
}

if (failures()) {
  console.error(`\nFAIL: ${failures()} gate(s); nothing written`);
  process.exit(1);
}
const out = {
  generatedBy: "build_data.cjs",
  account: {
    case: A.CASE_LANE, main: MAIN, cash: CASH, perMember: SUMMARY.v6.per_member_usd.set, lineageM: round(SUMMARY.v6.per_member_usd.population / 1e6, 2),
    gg: GG, rates: [P.RATES.low, P.RATES.high], ends: ENDS, bands: BANDS, tally: { accrual: ends("tally").map((x) => round(x)), cash: cashTally },
    shares: [...new Set(SPECS.map((s) => s.share))].sort((a, b) => a - b),
    longRun: Object.fromEntries([["roads", "economic_affairs_services"], ["parks", "recreation_culture"]]
      .map(([k, id]) => [k, [P.LINE_RESPONSES[id].low, P.LINE_RESPONSES[id].high]])),
    breakEven,
  },
  staircase,
  matrix: { columns: GG_COLS, productionSpan: PROD_SPAN.map((x) => round(x, 2)), receipts: RECEIPTS, receiptMoves: RECEIPT_MOVES,
    justiceKeys: JUSTICE_KEYS, ucKeys: UC_KEYS, rows: matrix },
  whoPays, landlordsTopFifth: round(landlordsTop, 3),
  byPercentile,
  crime, custody, victims,
  origins, education,
  ledger: { bands: BANDS_AGE, mexican: { pop: mexicanAges.pop, rate: mexicanAges.rate }, white: { pop: whiteAges.pop, rate: whiteAges.rate },
    categories, gaps: ageGaps, commonGap, youngHides, unionBalance: hulls.practitioner[2] },
  generations: { ...generations, lifetime, caseSplit },
  places, topTenShare,
  sentences: { backcast, backcastWindows, programmeYears, programmes, schooling, fiscalWindows, incomeRatios, kitagawa, hulls },
  inputs: inputs(),
};
fs.mkdirSync(path.join(HERE, "src", "generated"), { recursive: true });
fs.writeFileSync(path.join(HERE, "src", "generated", "figures.json"), JSON.stringify(out, null, 1) + "\n");
console.log(`\nwrote src/generated/figures.json (${out.inputs.length} inputs); all gates passed`);
