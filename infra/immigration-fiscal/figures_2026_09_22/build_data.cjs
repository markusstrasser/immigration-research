/* Builds src/generated/figures.json for the figures page.
 *
 * The complete-account figures run the explorer's evaluator (assumption_explorer_2026_09_21/
 * engine.js, gated there by test_engine.js) on its executed model and on that model with the
 * corrections adopted on 2026-09-24 (main_case_2026_09_24/package.cjs); every response is set
 * explicitly per service line, so each step of the staircase and each cell of the matrix is one
 * evaluation of the account's own formula. The other figures read lane CSVs. Nothing is typed
 * in, and the gates reproduce published figures before the file is written.
 *
 * Run from this directory: node build_data.cjs
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const EXPLORER = path.join(FISCAL, "assumption_explorer_2026_09_21");
const Engine = require(path.join(EXPLORER, "engine.js"));
const model = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "model.json"), "utf8"));
const scaling = JSON.parse(fs.readFileSync(path.join(EXPLORER, "derived", "scaling_check.json"), "utf8"));
// The data corrections adopted on 2026-09-24 (dataset audit and outside checks) as model edits. The
// two fill-in methods' shift lists are averaged into one model: the engine is linear, and the gates
// check that the averaged model reproduces the published bands.
const MAIN_CASE = path.join(FISCAL, "main_case_2026_09_24");
const Pkg = require(path.join(MAIN_CASE, "package.cjs"));
const pkgShifts = Pkg.METHODS.flatMap((meth) =>
  Pkg.packageShifts(Pkg.STACKS[`row4+status_state_aware|central|${meth}`], "central", meth, Pkg.CENTRAL)
    .map((x) => ({ ...x, by: Pkg.scale(x.by, Pkg.both(0.5)) })));
const MODELS = {
  base: model,
  taxes: Pkg.build(pkgShifts.filter((x) => x.side === "receipt")),
  adopted: Pkg.build(pkgShifts),
};

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}
const near = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;
const round = (x, d = 4) => Math.round(x * 10 ** d) / 10 ** d;

/* RFC 4180 reader: several lane files quote fields that contain commas. */
function readCsv(file) {
  const text = fs.readFileSync(file, "utf8");
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; } else quoted = false;
      } else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows.filter((r) => !(r.length === 1 && r[0] === ""));
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}

function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))),
    [{}],
  );
}
const span = (xs) => [Math.min(...xs), Math.max(...xs)];

/* ---------------------------------------------------------------- complete account ---------- */

const SHARES = Engine.schoolShareBounds(model);
const GG = [scaling.composite_low, scaling.composite_high];
const CBO_SCHOOLS = [0.63, 0.66];
const serviceLines = model.spending.lines.filter((l) => l.response_class === "service").map((l) => l.id).sort();
gate("service lines are the seven the figures set", JSON.stringify(serviceLines) === JSON.stringify([
  "economic_affairs_services", "education_services", "health_services", "housing_community_services",
  "income_security_services", "public_order_safety", "recreation_culture"]), serviceLines.join(" "));

/* One evaluation. spec: allocation, normalization, share, school, gg, uc, justice, receipts,
 * production. r: responses by service family; schools may be "cbo" (take spec.school). m: one of
 * MODELS. */
function cost(spec, r, m = MODELS.base) {
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = spec.receipts || model.receipts.reference;
  if (spec.production) Object.assign(s.production, spec.production);
  if (spec.normalization) s.production.normalization = spec.normalization;
  s.count_production = r.production;
  s.general_government_response = r.gg === "band" ? spec.gg : r.gg;
  s.key_override = {};
  if (spec.justice) s.key_override.public_order_safety = spec.justice;
  if (r.uc !== false && spec.uc) s.key_override.medicaid_and_chip_other_medical = spec.uc;
  const schools = r.schools === "cbo" ? spec.school : r.schools;
  s.response_override = {
    education_services: spec.share * schools + (1 - spec.share) * r.colleges,
    public_order_safety: r.police,
    health_services: r.health,
    income_security_services: r.other,
    housing_community_services: r.other,
    economic_affairs_services: r.delayed,
    recreation_culture: r.delayed,
    // The corrections' own lines (package.cjs SYN; absent from the base model): the school price
    // at the school response, the college re-key at the college response, lane constants in full.
    [Pkg.SYN.school]: spec.share * schools,
    [Pkg.SYN.college]: (1 - spec.share) * r.colleges,
    [Pkg.SYN.constants]: 1,
  };
  return -Engine.evaluate(m, s).welfare_bn; // positive = cost to other US residents
}

const bands = readCsv(path.join(MAIN_CASE, "derived", "main_case_bands.csv"));
const band = (profile, variant) => {
  const row = bands.find((b) => b.profile === profile && b.variant === variant);
  if (!row) throw new Error(`no band ${profile} / ${variant}`);
  return [Number(row.cost_low_bn), Number(row.cost_high_bn)];
};
const MAIN = band("cbo_category_lag_non_school_full", "adopted");
const FIXED_COLLEGES = band("cbo_category_lag_non_school_fixed", "adopted");
const PROPORTIONAL = band("proportional_reference", "adopted");
const BEFORE = band("cbo_category_lag_non_school_full", "adopted_2026_09_23");  // before the corrections
const BY_SIDE = JSON.parse(fs.readFileSync(path.join(MAIN_CASE, "derived", "summary.json"), "utf8")).by_side;

// The main case's unresolved dimensions: its published band is the envelope over these.
const MAIN_DIMS = {
  allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
  school: CBO_SCHOOLS, gg: GG, uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"],
};
const mainSpecs = product(MAIN_DIMS);

console.log("\n[positive controls]");
{
  const adopted = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };
  const got = span(mainSpecs.map((spec) => cost(spec, adopted)));
  // main_case_bands.csv carries four decimals.
  gate("base model = main case before the corrections (adopted_2026_09_23)", near(got[0], BEFORE[0], 1e-4) && near(got[1], BEFORE[1], 1e-4),
    `${got[0].toFixed(4)} to ${got[1].toFixed(4)}`);
  const pkg = span(mainSpecs.map((spec) => cost(spec, adopted, MODELS.adopted)));
  gate("corrected model = main case (adopted)", near(pkg[0], MAIN[0], 1e-4) && near(pkg[1], MAIN[1], 1e-4),
    `${pkg[0].toFixed(4)} to ${pkg[1].toFixed(4)}`);
  // Same band through the engine's own band semantics (preset repo_central_gg).
  const st = Object.assign(Engine.defaultState(model), {
    school_response: 0.63, school_response_band: CBO_SCHOOLS, other_education_response: 1, delayed_response: 0,
    general_government_response: GG[0], general_government_response_band: GG,
    key_override: { public_order_safety: "use", medicaid_and_chip_other_medical: "uninsured_use_low" },
    key_band: { medicaid_and_chip_other_medical: ["uninsured_use_low", "uninsured_use_high"] },
  });
  const eng = Engine.unresolvedRange(model, st, "welfare_bn").map((w) => -w).reverse();
  gate("per-line overrides = engine band semantics", near(eng[0], got[0]) && near(eng[1], got[1]),
    `${eng[0].toFixed(4)} to ${eng[1].toFixed(4)}`);
}

/* Staircase: from the tally commentators quote to the main case, one line at a time. */
const TALLY = { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0, gg: 0, production: false, uc: false };
const STEPS = [
  { id: "tally", label: "Taxes paid minus benefits received", note: "no services, no gain from their work", r: {} },
  { id: "production", label: "Gain from their work", note: "wages, profits and the taxes on them", r: { production: true } },
  { id: "uc", label: "Unpaid hospital care", note: "keyed to uninsured use", r: { uc: true } },
  { id: "schools", label: "Schools, 63–66% of per-pupil cost", note: "from CBO’s coefficients", r: { schools: "cbo" } },
  { id: "colleges", label: "Colleges and other education", r: { colleges: 1 } },
  { id: "police", label: "Police, courts and prisons", note: "charged by use", r: { police: 1 } },
  { id: "health", label: "Public health services", r: { health: 1 } },
  { id: "other", label: "Welfare administration, housing, community", r: { other: 1 } },
  { id: "gg", label: "General administration, 0.59–0.84", note: "cross-state scale of administration", r: { gg: "band" } },
  { id: "taxes", label: "Data corrections: taxes", note: "legal status, survey fill-ins, CBO’s income shares", model: "taxes" },
  { id: "benefits", label: "Data corrections: benefits, services", note: "credits, medical care, schools, care work",
    model: "adopted", main: true },
  { id: "delayed", label: "Roads, transport, parks and culture", note: "held fixed in the main case", r: { delayed: 1 }, beyond: true },
  { id: "schools_full", label: "Schools at the full per-pupil cost", r: { schools: 1 }, beyond: true },
];
const trajectories = mainSpecs.map(() => []);
{
  let r = { ...TALLY }, m = MODELS.base;
  for (const step of STEPS) {
    r = { ...r, ...(step.r || {}) };
    if (step.model) m = MODELS[step.model];
    mainSpecs.forEach((spec, i) => trajectories[i].push(cost(spec, r, m)));
  }
}
const staircase = STEPS.map((step, k) => {
  const total = span(trajectories.map((t) => t[k]));
  const delta = k ? span(trajectories.map((t) => t[k] - t[k - 1])) : null;
  return { id: step.id, label: step.label, note: step.note || null, main: !!step.main, beyond: !!step.beyond,
    total: total.map((x) => round(x)), step: delta && delta.map((x) => round(x)) };
});
console.log("\n[staircase]");
{
  // The tally is the explorer's convention card: service_response 0, no production, published keys.
  const conv = ["personal", "shared"].map((allocation) => {
    const s = Object.assign(Engine.defaultState(model), { allocation, service_response: 0, count_production: false });
    return -Engine.evaluate(model, s).welfare_bn;
  });
  const t = staircase[0].total;
  gate("tally = explorer convention taxes_minus_benefits", near(t[0], Math.min(...conv), 1e-3) && near(t[1], Math.max(...conv), 1e-3),
    `${t[0].toFixed(2)} to ${t[1].toFixed(2)}`);
  const g = staircase.find((s) => s.id === "gg").total;
  gate("general-administration step = main case before the corrections", near(g[0], BEFORE[0], 1e-4) && near(g[1], BEFORE[1], 1e-4),
    `${g[0]} to ${g[1]}`);
  const tx = staircase.find((s) => s.id === "taxes").total;
  gate("tax corrections = summary.json by_side.receipts", near(tx[0] - g[0], BY_SIDE.receipts[0], 1e-3) &&
    near(tx[1] - g[1], BY_SIDE.receipts[1], 1e-3), `${(tx[0] - g[0]).toFixed(3)} / ${(tx[1] - g[1]).toFixed(3)}`);
  const m = staircase.find((s) => s.main).total;
  gate("main-case step = adopted band", near(m[0], MAIN[0], 1e-4) && near(m[1], MAIN[1], 1e-4), `${m[0]} to ${m[1]}`);
  const p = staircase.at(-1).total;
  gate("last step = proportional adopted band", near(p[0], PROPORTIONAL[0], 1e-4) && near(p[1], PROPORTIONAL[1], 1e-4), `${p[0]} to ${p[1]}`);
  for (const s of staircase) console.log(`    ${s.label.padEnd(52)} ${s.total.map((x) => x.toFixed(1)).join(" to ")}`);
}

/* Matrix: every combination of the service choices × general administration. The inner range
 * is the main case's own unresolved dimensions; the outer range adds every executed tax-incidence
 * scenario, every executed justice and uncompensated-care key, and the production grid with
 * private capital adjusted and no capital owners excluded (the $6–21bn of FAQ entry 4). */
const PROD_DIMS = Engine.PRODUCTION_DIMS;
function decode(index) {
  const out = {};
  for (let k = PROD_DIMS.length - 1; k >= 0; k--) {
    const levels = model.production.dims[PROD_DIMS[k]];
    out[PROD_DIMS[k]] = levels[index % levels.length];
    index = Math.floor(index / levels.length);
  }
  return out;
}
const saneProduction = [];
for (let i = 0; i < model.production.private_wtp_bn.length; i++) {
  const d = decode(i);
  if (Engine.productionIndex(model, d) !== i) throw new Error("production index decode mismatch at " + i);
  if (d.capital_adjustment === 1 && d.excluded_capital_owner_share === 0) {
    saneProduction.push(model.production.private_wtp_bn[i] + model.production.induced_receipts_bn[i]);
  }
}
const PROD_SPAN = span(saneProduction);
console.log("\n[matrix]");
gate("sane production grid is 432 scenarios, $6–21bn", saneProduction.length === 432 &&
  near(PROD_SPAN[0], 5.98, 0.01) && near(PROD_SPAN[1], 21.08, 0.01), `${PROD_SPAN[0].toFixed(2)} to ${PROD_SPAN[1].toFixed(2)}`);

const JUSTICE_KEYS = Object.keys(model.spending.lines.find((l) => l.id === "public_order_safety").keys);
const UC_KEYS = Object.keys(model.spending.lines.find((l) => l.id === "medicaid_and_chip_other_medical").keys)
  .filter((k) => k === "medicaid" || k.startsWith("uninsured_use"));
const RECEIPTS = model.receipts.scenarios;
const GG_COLS = [0, GG[0], GG[1], 1];
const ROWS = [];
ROWS.push({ id: "frozen", schools: 0, colleges: 0, delayed: 0, frozen: true });
for (const schools of ["cbo", 1]) for (const colleges of [0, 1]) for (const delayed of [0, 1]) {
  ROWS.push({ id: `s${schools}_c${colleges}_d${delayed}`, schools, colleges, delayed });
}
const outerSpecs = product({
  allocation: ["personal", "shared"], share: SHARES, school: CBO_SCHOOLS,
  uc: UC_KEYS, justice: JUSTICE_KEYS, receipts: RECEIPTS,
});
const matrix = ROWS.map((row) => {
  const base = row.frozen
    ? { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0 }
    : { schools: row.schools, colleges: row.colleges, police: 1, health: 1, other: 1, delayed: row.delayed };
  const cells = GG_COLS.map((g) => {
    const r = { ...base, gg: g, production: true };
    const inner = span(mainSpecs.map((spec) => cost(spec, r, MODELS.adopted)));
    // Outer: fiscal part over every executed key, incidence and allocation choice, plus the
    // production span. welfare = P + F + direct, and P, F depend only on the production index,
    // so the envelope of the sum is the sum of the envelopes.
    // The corrections are measured on the reference incidence rule; package.cjs build() carries
    // them to the other rules as the same proportional change to the group's share of each line.
    const direct = span(outerSpecs.map((spec) => cost(spec, { ...r, production: false }, MODELS.adopted)));
    const outer = [direct[0] - PROD_SPAN[1], direct[1] - PROD_SPAN[0]];
    return { gg: g, inner: inner.map((x) => round(x)), outer: outer.map((x) => round(x)) };
  });
  return { ...row, cells };
});
{
  const main = matrix.find((r) => r.schools === "cbo" && r.colleges === 1 && r.delayed === 0);
  const u = [main.cells[1].inner[0], main.cells[2].inner[1]];
  gate("main-case row, gg 0.59–0.84 = adopted band", near(u[0], MAIN[0], 1e-4) && near(u[1], MAIN[1], 1e-4), `${u[0]} to ${u[1]}`);
  const fc = matrix.find((r) => r.schools === "cbo" && r.colleges === 0 && r.delayed === 0);
  const v = [fc.cells[1].inner[0], fc.cells[2].inner[1]];
  gate("colleges-fixed row = adopted non-school-fixed band", near(v[0], FIXED_COLLEGES[0], 1e-4) && near(v[1], FIXED_COLLEGES[1], 1e-4), `${v[0]} to ${v[1]}`);
  const pr = matrix.find((r) => r.schools === 1 && r.colleges === 1 && r.delayed === 1);
  const w = [pr.cells[1].inner[0], pr.cells[2].inner[1]];
  gate("all-full row = adopted proportional band", near(w[0], PROPORTIONAL[0], 1e-4) && near(w[1], PROPORTIONAL[1], 1e-4), `${w[0]} to ${w[1]}`);
  gate("outer contains inner in every cell", matrix.every((r) => r.cells.every((c) => c.outer[0] <= c.inner[0] + 1e-9 && c.outer[1] >= c.inner[1] - 1e-9)));
  for (const r of matrix) console.log(`    ${r.id.padEnd(12)} ${r.cells.map((c) => c.inner.map((x) => x.toFixed(0)).join("–")).join("   ")}`);
}

const signRows = readCsv(path.join(MAIN_CASE, "derived", "sign_reversal.csv"))
  .filter((r) => r.measure.startsWith("service_break_even"));
const breakEven = [Math.min(...signRows.map((r) => Number(r.sept24_low))), Math.max(...signRows.map((r) => Number(r.sept24_high)))];
gate("break-even read from sign_reversal.csv", near(breakEven[0], 0.0476, 1e-4) && near(breakEven[1], 0.1602, 1e-4),
  breakEven.map((x) => (100 * x).toFixed(1) + "%").join(" to "));

/* ---------------------------------------------------------------- who pays ------------------ */

console.log("\n[who pays]");
const channels = readCsv(path.join(FISCAL, "distribution_weights_2026_09_23", "derived", "channel_by_quintile.csv"))
  .filter((r) => r.measure === "spm");
const CHANNELS = [
  { id: "fiscal_a", label: "Fiscal cost, paid in proportion to taxes" },
  { id: "fiscal_b", label: "Fiscal cost, paid as equal cuts per person" },
  { id: "wages", label: "Wages, after tax" },
  { id: "housing_net", label: "Housing: renters pay, landlords receive" },
  { id: "crime", label: "Crime victims’ harm" },
  { id: "unreimbursed_care", label: "Unpaid hospital care" },
];
const whoPays = CHANNELS.map((c) => {
  const q = [1, 2, 3, 4, 5].map((k) => {
    const row = channels.find((r) => r.channel === c.id && r.quintile === String(k));
    if (!row) throw new Error(`missing ${c.id} quintile ${k}`);
    return { bn: round(Number(row.bn), 3), pct: round(Number(row.pct_of_resources), 3), perPerson: Math.round(Number(row.usd_per_person)) };
  });
  const total = channels.find((r) => r.channel === c.id && r.quintile === "0");
  return { ...c, quintiles: q, totalBn: round(Number(total.bn), 2) };
});
{
  const outside = ["wages", "housing_net", "crime", "unreimbursed_care"];
  const sumQ = (ks) => whoPays.filter((c) => outside.includes(c.id))
    .reduce((s, c) => s + ks.reduce((t, k) => t + c.quintiles[k - 1].bn, 0), 0);
  const bottom = sumQ([1, 2, 3, 4]), top = sumQ([5]);
  gate("outside the budget: bottom four fifths −80.7, top fifth +46.0 (ladder 194)",
    near(bottom, -80.7, 0.05) && near(top, 46.0, 0.05), `${bottom.toFixed(2)} / ${top.toFixed(2)}`);
  const fa = whoPays.find((c) => c.id === "fiscal_a");
  gate("fiscal cost total −227.9", near(fa.totalBn, -227.92, 0.01), String(fa.totalBn));
}

/* ---------------------------------------------------------------- crime --------------------- */

console.log("\n[crime]");
const rates = readCsv(path.join(FISCAL, "offender_ethnicity_nibrs_2026_09_23", "derived", "rates_by_spec.csv"));
const OFFENCES = ["Murder", "Rape/sexual assault", "Robbery", "Aggravated assault", "Simple assault"];
const pick = (spec, offence) => {
  const row = rates.find((r) => r.spec === spec && r.offence === offence);
  if (!row) throw new Error(`missing ${spec} / ${offence}`);
  return row;
};
const crime = OFFENCES.map((offence) => {
  const c = pick("central", offence), b = pick("alloc=b", offence), k = pick("alloc=c", offence);
  return {
    offence,
    victimisations: Math.round(Number(c.victimisations)),
    per100k: { hispanic: round(100 * c.rate_H, 2), white: round(100 * c.rate_NHW, 2), all: round(100 * c.rate_all, 2) },
    // Unknown offenders all non-Hispanic (b) or all Hispanic (c).
    hispanicBounds: [round(100 * b.rate_H, 2), round(100 * k.rate_H, 2)],
    vsWhite: [Number(b.RR_H_NHW), Number(c.RR_H_NHW), Number(k.RR_H_NHW)].map((x) => round(x, 3)),
    vsAll: [Number(b.RR_H_all), Number(c.RR_H_all), Number(k.RR_H_all)].map((x) => round(x, 3)),
  };
});
{
  const m = crime[0], r = crime[2];
  gate("murder 2.30 (1.53–3.93) vs white, 1.00 vs all", near(m.vsWhite[1], 2.30, 0.005) && near(m.vsWhite[0], 1.53, 0.005) &&
    near(m.vsWhite[2], 3.93, 0.005) && near(m.vsAll[1], 1.00, 0.005), m.vsWhite.join(" / "));
  gate("robbery 4.22 vs white, 0.92 vs all", near(r.vsWhite[1], 4.22, 0.005) && near(r.vsAll[1], 0.92, 0.005));
}

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
  const at = (allocation) => nativeAges.find((r) => r.origin === s.origin && r.allocation === allocation);
  const p = at("personal"), sh = at("shared");
  if (!p || !sh) throw new Error("no native-age row for " + s.origin);
  if (!NAMES[s.origin]) throw new Error("unnamed origin " + s.origin);
  return {
    id: s.origin, name: NAMES[s.origin], n: Number(s.raw_n_25_64), ba: round(Number(s.ba_plus_share_25_64), 4),
    reference: s.origin === "all_native" || s.origin === "third_plus_nh_white",
    personal: { v: Math.round(Number(p.native_age_mix)), se: Math.round(Number(p.native_age_mix_se_approx)) },
    shared: { v: Math.round(Number(sh.native_age_mix)), se: Math.round(Number(sh.native_age_mix_se_approx)) },
  };
});
{
  const mx = origins.find((o) => o.id === "mexico_born"), ind = origins.find((o) => o.id === "india");
  gate("Mexico-born −5,684 and India +21,832 per adult at native ages", mx.personal.v === -5684 && ind.personal.v === 21832,
    `${mx.personal.v} / ${ind.personal.v}`);
  gate("every origin in the screen has both allocations", origins.length === 21, String(origins.length));
}

/* ---------------------------------------------------------------- back-cast ----------------- */

// The whole-budget back-cast of the main case with the 2026-09-24 corrections: each year is the
// envelope of the flat, ratio and income rules at the band's two ends; flat carries the 2024 level.
// 2024 is the measured account; earlier years are a model.
console.log("\n[back-cast]");
const BACKCAST = path.join(FISCAL, "historical_backcast_2026_09_20", "derived");
const CONCEPT = "net_cost_cbo_informed_corrected";
const annual = readCsv(path.join(BACKCAST, "backcast_annual.csv"));
const RULES = ["low", "high"].flatMap((end) => ["flat", "ratio", "income"].map((rule) => `${CONCEPT}_${end}__${rule}`));
for (const c of RULES) if (!(c in annual[0])) throw new Error("no back-cast column " + c);
const backcast = annual.map((row) => {
  const v = RULES.map((c) => Number(row[c]));
  return { year: Number(row.year), lo: round(Math.min(...v), 1), hi: round(Math.max(...v), 1),
    flatLo: round(Number(row[`${CONCEPT}_low__flat`]), 1), flatHi: round(Number(row[`${CONCEPT}_high__flat`]), 1) };
});
{
  const y24 = annual.find((r) => Number(r.year) === 2024);
  const ends = [Number(y24[`${CONCEPT}_low__flat`]), Number(y24[`${CONCEPT}_high__flat`])];
  gate("back-cast 2024 = adopted band", near(ends[0], MAIN[0], 1e-3) && near(ends[1], MAIN[1], 1e-3), ends.join(" to "));
  gate("back-cast covers 2005–2024", backcast.length === 20 && backcast[0].year === 2005 && backcast.at(-1).year === 2024);
}
const windows = readCsv(path.join(BACKCAST, "backcast_windows.csv")).filter((r) => r.concept.startsWith(CONCEPT + "_"));
const win = (col) => span(windows.map((r) => Number(r[col]))).map((x) => round(x, 3));
const backcastWindows = { ten: win("10y_2015_2024"), fifteen: win("15y_2010_2024"), twenty: win("20y_2005_2024") };
gate("back-cast windows $1.7–2.4tn over ten years", windows.length === 6 && near(backcastWindows.ten[0], 1.7317, 1e-3) &&
  near(backcastWindows.ten[1], 2.4307, 1e-3), backcastWindows.ten.join(" to "));

if (failures) {
  console.error(`\nFAIL: ${failures} gate(s); nothing written`);
  process.exit(1);
}
const out = {
  generatedBy: "build_data.cjs",
  account: { main: MAIN, before: BEFORE, bySide: BY_SIDE, fixedColleges: FIXED_COLLEGES, proportional: PROPORTIONAL, gg: GG, breakEven },
  staircase,
  matrix: { columns: GG_COLS, productionSpan: PROD_SPAN.map((x) => round(x, 2)), receipts: RECEIPTS,
    justiceKeys: JUSTICE_KEYS, ucKeys: UC_KEYS, rows: matrix },
  whoPays,
  crime,
  origins,
  backcast,
  backcastWindows,
};
fs.mkdirSync(path.join(HERE, "src", "generated"), { recursive: true });
fs.writeFileSync(path.join(HERE, "src", "generated", "figures.json"), JSON.stringify(out, null, 1) + "\n");
console.log("\nwrote src/generated/figures.json; all gates passed");
