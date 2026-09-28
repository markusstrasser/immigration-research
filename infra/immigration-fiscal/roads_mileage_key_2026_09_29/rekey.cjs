/* Candidate: key the road part of economic affairs by vehicle miles (passenger) and the consumption key (freight),
 * with gasoline taxes and personal motor vehicle licences keyed by the same vehicle miles (RESULT.md).
 *
 * The adopted case charges each economic-affairs subfunction at the line's key (SPM resources) times the
 * subfunction's own long-run response (the engine applies their amount-weighted blend), and keys the road capital
 * return (hwy_sl, hwy_fed) by the same line share. Replacing the highway subfunctions' key k_old by k_road moves
 *   spending  (k_road - k_old) x [S&L highways x r_sl + federal highways x r_fed]
 *           + (k_road - k_old) x rate x [hwy_sl stock x r_sl + hwy_fed stock x r_fed]
 *   receipts  (s_vmt - k_cons) x gasoline taxes x r_excise + (s_vmt - k_adults) x licences x r_licences
 * where s_vmt is the group's share of driver VMT, k_cons the case's consumption share (excise_selective_sales) and
 * k_road = f_p x s_vmt + (1 - f_p) x k_cons with f_p the passenger share of highway cost responsibility (HCAS 1997
 * Table V-21, all levels of government). Cost change = spending - receipts.
 *
 * The same change is then run through the engine: two synthetic spending lines carry the highway delta at the
 * subfunctions' responses, receipt shifts move the two receipt lines, and a capital variant keys hwy_sl and
 * hwy_fed at k_road. Gates: (1) the probe reproduces $321.8194 / $387.3701bn; (2) the engine delta equals the line
 * arithmetic to $0.01bn; (3) every new key's group and other-resident shares sum to 1; (4) reruns are byte-identical
 * (checked by rerunning into a scratch directory).
 * Run: node rekey.cjs [--out-dir DIR]   (reads DIR/inputs.json written by inputs.py; default derived/)
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_long_run_2026_09_27", "package.cjs"));
const argv = process.argv.slice(2);
const OUT = path.resolve(argv.includes("--out-dir") ? argv[argv.indexOf("--out-dir") + 1] : path.join(__dirname, "derived"));
const IN = JSON.parse(fs.readFileSync(path.join(OUT, "inputs.json"), "utf8"));
const { Engine } = P;

const GATES = [];
function gate(name, ok, detail) {
  GATES.push({ gate: name, pass: !!ok, detail });
  console.log((ok ? "PASS " : "FAIL ") + name + ": " + detail);
}
const RATIOS = ["2017_southwest", "2017_national", "2022_national"];  // central first
const CENTRAL_RATIO = RATIOS[0];
const EA = "economic_affairs_services", EXCISE = "excise_selective_sales", LICENCES = "personal_motor_vehicle";
const SYN = { sl: "roads_vmt_sl", fed: "roads_vmt_fed" };
const HWY = { sl: { subfunction: "sl_highways", capital: "hwy_sl" }, fed: { subfunction: "fed_highways", capital: "hwy_fed" } };
const ALLOCS = ["personal", "shared"];
const r6 = (x) => Number(x.toFixed(6));

// ---------------------------------------------------------------------------------------------------
// 1. The adopted case, reproduced.
const summary = JSON.parse(fs.readFileSync(path.join(P.HERE, "derived", "summary.json"), "utf8"));
const specs = P.specsFor({});
const ends = summary.end_specifications.map((e) => [e.low_end.index, e.high_end.index]);
const models = P.METHODS.map((m) => P.modelFor("central", m, P.withCentral({})));
const base = models.map((m, i) => ends[i].map((j) => P.evaluateFull(m, specs[j])));
const band = [0, 1].map((k) => base.reduce((a, r) => a + r[k].cost_bn, 0) / base.length);
gate("(1) probe reproduces the adopted band $321.8194 / $387.3701bn",
  Math.abs(band[0] - summary.main_case[0]) < 1e-6 && Math.abs(band[1] - summary.main_case[1]) < 1e-6
  && band[0].toFixed(4) === "321.8194" && band[1].toFixed(4) === "387.3701", band.map((x) => x.toFixed(6)).join(" / "));

// ---------------------------------------------------------------------------------------------------
// 2. Inputs.
const N = { sl: P.SUBFUNCTIONS.find((s) => s.id === HWY.sl.subfunction).national_bn,
  fed: P.SUBFUNCTIONS.find((s) => s.id === HWY.fed.subfunction).national_bn };
const nipa = IN.nipa_2024;
const gasShareState = IN.state_fuel.gasoline_share_of_state_motor_fuel_tax;
const GAS = nipa.federal_gasoline_bn + nipa.sl_motor_fuel_bn * gasShareState;  // gasoline taxes inside the excise line
const LIC = nipa.personal_motor_vehicle_licences_bn;
const FP = IN.hcas_v21.passenger_share;
const U = IN.under5_share;

// Keys of a model at an allocation, read from its cells (the engine's evaluation is checked against them below).
function modelKeys(m, a) {
  const ea = m.spending.lines.find((l) => l.id === EA);
  const rec = (id) => { const l = m.receipts.lines.find((x) => x.id === id); return l.cells[m.receipts.reference][a].target_bn / l.national_bn; };
  return { k_old: ea.keys[ea.preferred_key][a].target_bn / ea.national_bn, ea_key: ea.preferred_key,
    k_cons: rec(EXCISE), k_adults: rec(LICENCES), p: P.populationShare(m)[a] };
}
// Group share of driver VMT: persons aged 5+ times the NHTS ratio per person aged 5+, against the other residents.
function vmtShares(p, ratio, ageAdjust) {
  const g = p * (ageAdjust ? 1 - U.group : 1) * ratio, o = (1 - p) * (ageAdjust ? 1 - U.others : 1);
  return { group: g / (g + o), others: o / (g + o) };
}
function keysFor(kk, ratio, opt) {
  const o = Object.assign({ ageAdjust: true, fp: FP.all_levels }, opt || {});
  const v = vmtShares(kk.p, IN.nhts_driver_vmt_ratio_per_person_5plus[ratio], o.ageAdjust);
  const road = o.fp * v.group + (1 - o.fp) * kk.k_cons;
  const roadOthers = o.fp * v.others + (1 - o.fp) * (1 - kk.k_cons);
  return { s_vmt: v.group, s_vmt_others: v.others, vmt_vs_average_resident: v.group / kk.p, k_road: road, k_road_others: roadOthers, fp: o.fp };
}

// ---------------------------------------------------------------------------------------------------
// 3. Line arithmetic at each method and band end.
function endFacts(i, k) {
  const spec = specs[ends[i][k]], ev = base[i][k].evaluation, cap = base[i][k].capital;
  const row = (side, id) => ev[side].find((l) => l.id === id);
  const sfr = P.subfunctionResponses(spec.long_run, spec.reading);
  const comps = Object.fromEntries(Object.entries(HWY).map(([lv, h]) => [lv, cap.components.find((c) => c.id === h.capital)]));
  return { spec, alloc: spec.allocation, reading: spec.reading, rate: spec.rate, ea: row("spending", EA),
    excise: row("receipts", EXCISE), licences: row("receipts", LICENCES), r: { sl: sfr[HWY.sl.subfunction], fed: sfr[HWY.fed.subfunction] }, comps };
}
function lineArithmetic(f, kk, keys, opt) {
  const o = Object.assign({ licences: true }, opt || {});
  const dk = keys.k_road - kk.k_old;
  const opex = dk * (N.sl * f.r.sl + N.fed * f.r.fed);
  const capital = dk * f.rate * (f.comps.sl.stock_charged_bn * f.comps.sl.response + f.comps.fed.stock_charged_bn * f.comps.fed.response);
  const gas = (keys.s_vmt - kk.k_cons) * GAS * f.excise.response;
  const lic = o.licences ? (keys.s_vmt - kk.k_adults) * LIC * f.licences.response : 0;
  return { opex, capital, spending: opex + capital, gasoline: gas, licences: lic, receipts: gas + lic, cost: opex + capital - gas - lic };
}

const facts = models.map((m, i) => [0, 1].map((k) => endFacts(i, k)));
const mkeys = models.map((m) => Object.fromEntries(ALLOCS.map((a) => [a, modelKeys(m, a)])));
// The evaluation's shares and responses are the model's cells and the adopted subfunction responses.
let consistent = true, detail = [];
facts.forEach((fs2, i) => fs2.forEach((f) => {
  const kk = mkeys[i][f.alloc];
  const blend = P.SUBFUNCTIONS.filter((s) => s.line === EA).reduce((a, s) => a + s.share_of_line * P.subfunctionResponses(f.spec.long_run, f.reading)[s.id], 0);
  const ok = f.ea.key === kk.ea_key && Math.abs(f.ea.amount_bn / f.ea.national_bn - kk.k_old) < 1e-12
    && Math.abs(f.excise.amount_bn / f.excise.national_bn - kk.k_cons) < 1e-12
    && Math.abs(f.licences.amount_bn / f.licences.national_bn - kk.k_adults) < 1e-12
    && Math.abs(f.ea.response - blend) < 1e-9 && f.spec.long_run === "adopted"
    && Object.values(f.comps).every((c) => Math.abs(c.key - kk.k_old) < 1e-12)
    && Math.abs(f.comps.sl.response - f.r.sl) < 1e-12 && Math.abs(f.comps.fed.response - f.r.fed) < 1e-12;
  consistent = consistent && ok;
  detail.push(`${P.METHODS[i].slice(2, 9)} ${f.reading}: k_old ${kk.k_old.toFixed(6)} (${kk.ea_key}), k_cons ${kk.k_cons.toFixed(6)}, adults ${kk.k_adults.toFixed(6)}, r_line ${f.ea.response.toFixed(4)}, r_sl ${f.r.sl.toFixed(4)}, r_fed ${f.r.fed}`);
}));
gate("evaluation shares, road capital keys and responses are the model's cells and the adopted subfunction responses", consistent, detail.join("; "));

// Gate 3: every new key partitions all residents.
let sums = true;
for (const i of [0, 1]) for (const a of ALLOCS) for (const ratio of RATIOS) for (const opt of [{}, { ageAdjust: false }, { fp: FP.state_local }, { fp: FP.federal }]) {
  const kz = keysFor(mkeys[i][a], ratio, opt);
  sums = sums && Math.abs(kz.s_vmt + kz.s_vmt_others - 1) < 1e-12 && Math.abs(kz.k_road + kz.k_road_others - 1) < 1e-12;
}
const hc = IN.hcas_v21.total_m;
gate("(3) all-resident shares sum to 1 under each new key (VMT, road blend; all ratios, allocations, methods, variants)", sums,
  `passenger + freight cost responsibility = ${(hc[3] / hc[3]).toFixed(1)} (all levels ${FP.all_levels.toFixed(4)} passenger)`);

// ---------------------------------------------------------------------------------------------------
// 4. The engine run: synthetic highway lines, receipt shifts and a capital variant at k_road.
function engineRun(i, ratio) {
  const m = models[i];
  const kz = Object.fromEntries(ALLOCS.map((a) => [a, keysFor(mkeys[i][a], ratio)]));
  const by = (f) => Object.fromEntries(ALLOCS.map((a) => [a, f(mkeys[i][a], kz[a])]));
  const edits = [
    { side: "spending", line: SYN.sl, key: "k", by: by((kk, k) => N.sl * (k.k_road - kk.k_old)) },
    { side: "spending", line: SYN.fed, key: "k", by: by((kk, k) => N.fed * (k.k_road - kk.k_old)) },
  ].concat(P.expand([
    { side: "receipt", line: EXCISE, by: by((kk, k) => GAS * (k.s_vmt - kk.k_cons)) },
    { side: "receipt", line: LICENCES, by: by((kk, k) => LIC * (k.s_vmt - kk.k_adults)) },
  ]));
  const lines = [
    { id: SYN.sl, family: "consumption", response_class: "service", label: "S&L highways re-keyed by vehicle miles and freight (candidate)" },
    { id: SYN.fed, family: "consumption", response_class: "service", label: "Federal highways re-keyed by vehicle miles and freight (candidate)" },
  ];
  const m2 = Engine.applyCorrections(m, { lines, edits });
  // National totals hold on the edited receipt cells.
  const totalsHold = [EXCISE, LICENCES].every((id) => { const l = m2.receipts.lines.find((x) => x.id === id);
    return Object.values(l.cells).every((c) => ALLOCS.every((a) => Math.abs(c[a].target_bn + c[a].other_bn - l.national_bn) < 1e-9)); });
  return [0, 1].map((k) => {
    const f = facts[i][k];
    const name = `roads_vmt|${P.METHODS[i]}|${ratio}|${f.alloc}`;
    P.CAP.variants[name] = { label: "candidate: road capital keyed at the vehicle-miles road key", overrides: [
      { component: HWY.sl.capital, key: { kind: "constant", value: kz[f.alloc].k_road } },
      { component: HWY.fed.capital, key: { kind: "constant", value: kz[f.alloc].k_road } }] };
    const spec = Object.assign({}, f.spec, { capital_variant: name,
      line_responses: Object.assign({}, f.spec.line_responses, { [SYN.sl]: f.r.sl, [SYN.fed]: f.r.fed }) });
    const run = P.evaluateFull(m2, spec);
    const syn = [SYN.sl, SYN.fed].map((id) => run.evaluation.spending.find((l) => l.id === id));
    const took = syn[0].response === f.r.sl && syn[1].response === f.r.fed
      && [HWY.sl.capital, HWY.fed.capital].every((id) => run.capital.components.find((c) => c.id === id).key === kz[f.alloc].k_road);
    return { cost: run.cost_bn, delta: run.cost_bn - base[i][k].cost_bn, totalsHold, took };
  });
}

const rows = [], results = {};
for (const ratio of RATIOS) {
  const perMethod = models.map((m, i) => [0, 1].map((k) => {
    const f = facts[i][k], kk = mkeys[i][f.alloc];
    return lineArithmetic(f, kk, keysFor(kk, ratio));
  }));
  const engine = models.map((m, i) => engineRun(i, ratio));
  const mean = (g) => [0, 1].map((k) => (g(0, k) + g(1, k)) / 2);
  const parts = ["opex", "capital", "spending", "gasoline", "licences", "receipts", "cost"];
  const line = Object.fromEntries(parts.map((q) => [q, mean((i, k) => perMethod[i][k][q])]));
  const eng = mean((i, k) => engine[i][k].delta);
  const diff = Math.max(...[0, 1].map((k) => Math.abs(eng[k] - line.cost[k])));
  gate(`(2) engine delta equals line arithmetic to $0.01bn (${ratio})`, diff < 0.01 && engine.flat().every((e) => e.totalsHold && e.took),
    `engine ${eng.map((x) => x.toFixed(6)).join(" / ")}, lines ${line.cost.map((x) => x.toFixed(6)).join(" / ")}, max |diff| ${diff.toExponential(2)}; synthetic responses and capital keys took; receipt totals hold`);
  results[ratio] = { line, engine: eng, case_bn: [0, 1].map((k) => band[k] + eng[k]) };
  for (const [k, end] of [[0, "low"], [1, "high"]]) {
    for (const i of [0, 1]) {
      const f = facts[i][k], kz = keysFor(mkeys[i][f.alloc], ratio), q = perMethod[i][k];
      rows.push([ratio, end, P.METHODS[i], f.alloc, r6(mkeys[i][f.alloc].k_old), r6(kz.k_road), r6(kz.s_vmt), r6(mkeys[i][f.alloc].k_cons),
        r6(q.opex), r6(q.capital), r6(q.spending), r6(q.gasoline), r6(q.licences), r6(q.receipts), r6(q.cost), r6(engine[i][k].delta)]);
    }
    rows.push([ratio, end, "mean", "", "", "", "", "", ...parts.map((q) => r6(line[q][k])), r6(eng[k])]);
  }
}

// Variants on the central ratio, line arithmetic only (the engine gate covers the construction).
function variant(label, keyOpt, arithOpt) {
  const v = [0, 1].map((k) => [0, 1].reduce((a, i) => {
    const f = facts[i][k], kk = mkeys[i][f.alloc];
    return a + lineArithmetic(f, kk, keysFor(kk, CENTRAL_RATIO, keyOpt), arithOpt).cost / 2;
  }, 0));
  return { label, cost_change_bn: v.map(r6) };
}
const variants = [
  variant("central: all-levels passenger share, under-5 adjustment, licences at the VMT key", {}, {}),
  variant("NHTS ratio applied per resident (no under-5 adjustment)", { ageAdjust: false }, {}),
  variant("passenger share of S&L cost responsibility only (0.751)", { fp: FP.state_local }, {}),
  variant("passenger share of federal cost responsibility only (0.604)", { fp: FP.federal }, {}),
  variant("licences left at the adults key", {}, { licences: false }),
];

// ---------------------------------------------------------------------------------------------------
// 5. Outputs.
const keyRows = [];
for (const i of [0, 1]) for (const a of ALLOCS) for (const ratio of RATIOS) {
  const kk = mkeys[i][a], kz = keysFor(kk, ratio);
  keyRows.push([P.METHODS[i], a, ratio, IN.nhts_driver_vmt_ratio_per_person_5plus[ratio], r6(kk.p), r6(U.group), r6(U.others), r6(kz.s_vmt),
    r6(kz.s_vmt_others), r6(kz.vmt_vs_average_resident), r6(kk.k_cons), r6(kz.fp), r6(kz.k_road), r6(kz.k_road_others), r6(kk.k_old), r6(kk.k_adults)]);
}
const csv = (header, body) => [header.join(","), ...body.map((r) => r.join(","))].join("\n") + "\n";
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "keys.csv"), csv(["method", "allocation", "nhts_ratio", "ratio_per_person_5plus", "per_head_share",
  "under5_group", "under5_others", "vmt_share_group", "vmt_share_others", "vmt_per_head_vs_average_resident", "consumption_share",
  "passenger_share_of_cost", "road_key_group", "road_key_others", "old_key_resources", "adults_key"], keyRows));
fs.writeFileSync(path.join(OUT, "rekey_lines.csv"), csv(["nhts_ratio", "band_end", "method", "allocation", "old_key", "road_key",
  "vmt_share", "consumption_share", "highway_consumption_bn", "road_capital_return_bn", "spending_bn", "gasoline_receipts_bn",
  "licence_receipts_bn", "receipts_bn", "cost_change_bn", "engine_cost_change_bn"], rows));
const out = {
  question: "the road part of economic_affairs_services keyed by driver VMT (passenger) and the consumption key (freight), gasoline taxes and personal motor vehicle licences keyed by the same VMT; a candidate, not an adoption",
  adopted_band_bn: band.map(r6),
  inputs: { highways_bn: { sl: N.sl, federal: N.fed }, gasoline_taxes_bn: r6(GAS), gasoline_share_of_state_motor_fuel_tax: r6(gasShareState),
    licences_bn: LIC, passenger_share_of_cost: FP, nhts_ratios: IN.nhts_driver_vmt_ratio_per_person_5plus, under5_share: U,
    diesel_and_truck_taxes: "diesel (federal $10.379bn and the diesel part of State motor-fuel taxes) and the federal truck excises stay at the consumption key, which is where freight is keyed; business licences sit in other_production_taxes at response 0" },
  by_ratio: Object.fromEntries(RATIOS.map((r) => [r, { spending_bn: results[r].line.spending.map(r6), receipts_bn: results[r].line.receipts.map(r6),
    cost_change_bn: results[r].engine.map(r6), line_arithmetic_bn: results[r].line.cost.map(r6), case_bn: results[r].case_bn.map(r6),
    opex_bn: results[r].line.opex.map(r6), capital_bn: results[r].line.capital.map(r6), gasoline_bn: results[r].line.gasoline.map(r6),
    licences_bn: results[r].line.licences.map(r6) }])),
  central_ratio: CENTRAL_RATIO,
  variants_central_ratio: variants,
  gates: GATES,
};
fs.writeFileSync(path.join(OUT, "summary.json"), JSON.stringify(out, null, 1) + "\n");
if (!GATES.every((g) => g.pass)) { console.error("[BLOCKED] a gate failed"); process.exit(1); }
console.log(JSON.stringify(out.by_ratio, null, 1));
console.log(JSON.stringify(variants, null, 1));
