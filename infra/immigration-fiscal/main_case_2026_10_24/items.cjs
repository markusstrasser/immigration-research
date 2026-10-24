/* Candidate v10 items 22-25: post-engine capital and price terms on any v9 case API.

Every term is derived inside the run it prices: per specification and method, from the v9 evaluator's own capital
components, union-completion carriers, own coverage parts, items 16/17 count parts, item 15 college capital and
item 21 health capital. Nothing here edits the engine model; v10 adds no edits and no people.

  22 capital_rate_theta_bound   each end's rate (theta = 1 low, theta = 0 high) on every capital piece item 20 prices,
                                at the level the rate lane assigns to that capital component
  23 k12_capital_where_enrolled K-12 capital where enrolled, divisor with the embedded preferred school price k
  24 where_used_prices          matched municipal parks (operating) + covered-college gross-book capital proxy;
                                beside the band (not identified), selectable as a variant
  25 public_land                land under public capital, read from V10_LAND_LANE; off when unset

Every term is linear in typed sub-rows (`rows`): each capital piece's engine, completion-carrier, college, coverage,
count and health parts, and the parks line's engine, carrier, coverage and count parts. Each sub-row carries the
routing fields item 20's parts carry (component, line, generation, population), so generation, household and person
consumers can route v10 as they route item 20 (generation.cjs does this for the ancestry companions).

Sources (read-only): public_capital_rate_2026_10_24/derived/rate_model.json theta_pairing.bound
{level_by_component, rate_by_level_by_end, theta_by_end}; school_capital_where_enrolled_2026_10_24/derived/summary.json;
where_used_prices_2026_10_24/derived/{parks.json, college_factors.csv}; user_fee_allocation_2026_10_07/derived/
fee_lines.json; state_priced_services_2026_09_29/derived/corrections.csv.

*/
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const FISCAL = path.join(__dirname, ".."), ROOT = path.resolve(FISCAL, "../..");
const C = require("../main_case_2026_10_16/companions.cjs");
const RATE20 = require("../main_case_2026_10_16/item_rate.cjs");
const sum = (a) => a.reduce((x, y) => x + y, 0);
const fail = (s) => { throw Error("[BLOCKED] v10: " + s); };
const read = (rel) => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
function csvRows(file) {
  const lines = fs.readFileSync(file, "utf8").trimEnd().split("\n");
  const split = (line) => { const r = []; let s = "", q = false; for (let i = 0; i < line.length; i++) { const c = line[i]; if (c === '"') { if (q && line[i + 1] === '"') { s += '"'; i++; } else q = !q; } else if (c === "," && !q) { r.push(s); s = ""; } else s += c; } r.push(s); return r; };
  const head = split(lines[0]);
  return lines.slice(1).map((l) => { const r = split(l); if (r.length !== head.length) fail("CSV row width " + file); return Object.fromEntries(head.map((h, i) => [h, r[i]])); });
}

const IDS = { 22: "capital_rate_theta_bound", 23: "k12_capital_where_enrolled", 24: "where_used_prices", 25: "public_land" };
const ORDER = [22, 23, 24, 25];
const BESIDE = [24];
const END = { low: 0, high: 1 };

// Item 22: the bound over theta (operator, 2026-10-24 15:00 JST). The rate lane owns both the level of every capital
// component and the rate of every level; v10 applies them and stops if either is absent.
const RATE_FILE = path.join(FISCAL, "public_capital_rate_2026_10_24/derived/rate_model.json");
const RATE_BYTES = fs.readFileSync(RATE_FILE);
// Validates a parsed rate_model.json and returns what item 22 reads; stops [BLOCKED] on any missing or bad key.
function readRateModel(model) {
  const bound = model.theta_pairing?.bound || fail("rate lane has no theta_pairing.bound");
  if (Math.abs(model.r_c - RATE20.RATE) > 1e-15) fail("rate lane's case rate is not item 20's rate");
  if (JSON.stringify(bound.theta_by_end) !== "[1,0]") fail("bound is not theta 1 low / 0 high");
  for (const k of ["level_by_component", "rate_by_level_by_end"]) if (!bound[k] || typeof bound[k] !== "object") fail(`rate lane publishes no theta_pairing.bound.${k}`);
  const levels = bound.level_by_component, rates = bound.rate_by_level_by_end;
  for (const [level, r] of Object.entries(rates)) if (!Array.isArray(r) || r.length !== 2 || !r.every((x) => Number.isFinite(x) && x > 0)) fail("bad rate pair for level " + level);
  for (const [id, level] of Object.entries(levels)) if (!rates[level]) fail(`component ${id} maps to level ${level}, which has no rate`);
  return { BOUND: bound, RC: model.r_c, LEVEL_BY_COMPONENT: levels, RATES: rates };
}
const { BOUND, RC, LEVEL_BY_COMPONENT, RATES } = readRateModel(JSON.parse(RATE_BYTES));
const RATE_SOURCE = { file: path.relative(ROOT, RATE_FILE), sha256: crypto.createHash("sha256").update(RATE_BYTES).digest("hex") };
/* The inherited capital-definition range variants add nine components (capital_return_services_2026_09_27
   engine_components.json variants.*.adds) that the rate lane's map, built on the central components, does not list.
   Each takes the level its source declares (state_local or federal, the rate lane's general levels for functions it
   does not measure separately), which must equal its parent line's mapped level where it has one. The table must
   equal the source's added components; a lane mapping wins; any other unmapped component stops. */
const VARIANT_PARENT = { eq_college_sl: "college", eq_pos_sl: "pos_sl", eq_health_sl: "health_sl", eq_gps_sl: "gps_sl", eq_income_security_sl: null,
  eq_pos_fed: "pos_fed", eq_gps_fed: "gps_fed", eq_income_security_fed: null, gps_sl_row8_increment: "gps_sl" };
const VARIANT_LEVEL = (() => {
  const adds = Object.values(read("capital_return_services_2026_09_27/derived/engine_components.json").variants).flatMap((v) => v.adds || []);
  if (JSON.stringify(adds.map((a) => a.id).sort()) !== JSON.stringify(Object.keys(VARIANT_PARENT).sort())) fail("range variants' added components moved: " + adds.map((a) => a.id));
  const out = {};
  for (const a of adds) {
    if (Object.hasOwn(LEVEL_BY_COMPONENT, a.id)) continue;
    if (!RATES[a.level]) fail(`variant component ${a.id} declares level ${a.level}, which has no rate`);
    const parent = VARIANT_PARENT[a.id];
    if (parent !== null && LEVEL_BY_COMPONENT[parent] !== a.level) fail(`variant component ${a.id} declares ${a.level}; its parent ${parent} is at ${LEVEL_BY_COMPONENT[parent]}`);
    out[a.id] = a.level;
  }
  return out;
})();
const levelOf = (c) => Object.hasOwn(LEVEL_BY_COMPONENT, c.id) ? LEVEL_BY_COMPONENT[c.id]
  : Object.hasOwn(VARIANT_LEVEL, c.id) ? VARIANT_LEVEL[c.id] : fail("capital component unmapped by the rate lane: " + c.id);
// Sub-row components the rate lane's map lists but v10 prices on the parent capital component's level (the line a
// completion carrier, coverage part, college, count or health part belongs to).
const ON_PARENT = ["capital_reporter", "capital_coverage", "college_capital_interaction", "capital_count_interaction", "health_capital"];

// Item 23: corrected divisor (school lane, "Correction, 2026-10-24 02:28 JST"; where_used RESULT lines 36-46).
const SCHOOL = read("school_capital_where_enrolled_2026_10_24/derived/summary.json");
const FEE = read("user_fee_allocation_2026_10_07/derived/fee_lines.json");
const K12A = SCHOOL.headline_key_consistent_A.a;
const K12_BASE = SCHOOL.case_base;
// National K-12 depreciation (structures, equipment): the source's keyed base over its effective key.
const K12_DEP_NATIONAL = { structures: K12_BASE.k12_depreciation_base_bn.structures / K12_BASE.effective_key, equipment: K12_BASE.k12_depreciation_base_bn.equipment / K12_BASE.effective_key };
const K12_IDS = new Set(["k12", "k12_user_fees"]);
const embeddedK = (allocation) => { const k = FEE.education_key.by_allocation[allocation]?.k; if (!Number.isFinite(k)) fail("no embedded k for " + allocation); return k; };
if (Math.abs(embeddedK("personal") - 1.0341917412164008) > 1e-12) fail("embedded k moved");
// Depreciation per unit of K-12 capital key at embedded price k.
const k12Dep = (k) => K12_DEP_NATIONAL.structures * (K12A.F_structures / k - 1) + K12_DEP_NATIONAL.equipment * (K12A.F_equipment / k - 1);

// Item 24: parks operating index change and college gross-book factor (case_fall, graduate weight 2).
const PARKS = read("where_used_prices_2026_10_24/derived/parks.json");
const PARK_INDEX_DELTA = PARKS.case_matched_municipal_bridge_index_delta;
const PARK_SL = Number(csvRows(path.join(FISCAL, "state_priced_services_2026_09_29/derived/corrections.csv")).find((q) => q.line === "recreation_culture" && q.function === "parks_libraries").sl_amount_bn);
if (Math.abs(PARK_SL - 48.901) > 1e-9) fail("parks state/local budget moved");
const factorRows = csvRows(path.join(FISCAL, "where_used_prices_2026_10_24/derived/college_factors.csv")).filter((r) => r.concept === "depreciable_gross" && r.scheme === "case_fall" && +r.graduate_weight === 2);
if (factorRows.length !== 1 || factorRows[0].status !== "conditional_allocation_proxy") fail("college gross-book factor not unique");
const COLLEGE_FACTOR = +factorRows[0].factor_vs_case_er_key;
const HIGHER_FRACTION = FEE.nipa.kappa * FEE.higher_ed.U / FEE.higher_ed.U_capital;
const COLLEGE_IDS = new Set(["college", "college_user_fees"]);
const PARK_LINE = "recreation_culture";

/* Item 25: per-line land values from a lane directory (derived/land_by_line.csv). Off when unset.
   Every line needs a group ratio for each value variant v (central, low, high): the lane's
   group_weighted_value_<v>_bn / value_<v>_bn (r2 schema), or an explicit override (the r1 test). */
const VARIANTS = ["central", "low", "high"];
function loadLand(dir, { group_ratio_override = {} } = {}) {
  if (!dir) return null;
  const file = path.resolve(dir, "derived/land_by_line.csv");
  if (!fs.existsSync(file)) fail("land lane has no derived/land_by_line.csv: " + file);
  const rows = csvRows(file), lines = {};
  for (const r of rows) {
    for (const v of VARIANTS) if (!Number.isFinite(+r[`value_${v}_bn`]) || r[`value_${v}_bn`] === "") fail(`land ${r.line} value_${v}_bn not numeric`);
    const o = group_ratio_override[r.line], ratio = {};
    for (const v of VARIANTS) {
      if (o !== undefined) ratio[v] = typeof o === "number" ? o : o[v];
      else {
        const g = r[`group_weighted_value_${v}_bn`];
        if (g === undefined || g === "") fail(`land lane gives no group_weighted_value_${v}_bn for ${r.line}`);
        ratio[v] = +g / +r[`value_${v}_bn`];
      }
      if (!Number.isFinite(ratio[v]) || ratio[v] <= 0) fail(`bad land group ratio ${r.line}/${v}`);
    }
    lines[r.line] = { central: +r.value_central_bn, low: +r.value_low_bn, high: +r.value_high_bn, group_ratio: ratio };
  }
  return { dir: path.relative(ROOT, path.resolve(dir)), file: path.relative(ROOT, file), lines };
}
const LAND_ENV = process.env.V10_LAND_LANE || null;
const LAND = loadLand(LAND_ENV);

// Per-API caches (the API object is immutable for a run).
const metaCache = new WeakMap();
function apiMeta(X) {
  if (metaCache.has(X)) return metaCache.get(X);
  const physical = Object.fromEntries(X.capitalMeta(X.withCentral({})).components.map((c) => [c.id, c.of_component || c.id]));
  const out = { physical, carriers: X.POST_ENGINE.union_completion?.carriers || {}, count: {}, lr: {}, central: {} };
  for (const end of ["low", "high"]) out.count[end] = ["native_minor_calibration", "coverage_tenure"].flatMap((id) => C.countParts(X.POST_ENGINE[id], end).map((q) => ({ ...q, item: id })));
  metaCache.set(X, out);
  return out;
}

/* Capital pieces of one evaluated run at item 20's rate R20, by capital component, with typed sub-rows.
   Construction as public_land_2026_10_24/case_contract.cjs, which closes to the 7% arm at the ends. */
function capitalPieces(X, r, s) {
  if (!s.rate || !r.capital?.components?.length) return { charged: false, R20: 0, pieces: [] };
  const M = apiMeta(X), R20 = RATE20.rateFor(X.POST_ENGINE.one_rate, s), scale = R20 / s.rate, toR20 = R20 / RATE20.RATE;
  const cov = X.POST_ENGINE.coverage?.by_end[s.reading]?.decomposition?.line_parts || [];
  const col = r.v9_post_engine?.parts?.public_college_response || [];
  const health = r.v9_post_engine?.parts?.health_residual_key || [];
  const pieces = r.capital.components.map((c) => {
    if (Math.abs(c.return_bn - c.stock_charged_bn * c.key * c.response * s.rate) > 1e-9) fail("engine capital identity " + c.id);
    const sub = [{ part: "engine", component: "capital_engine", line: c.id, value_bn: c.return_bn * scale }];
    for (const q of r.evaluation.spending) if (M.carriers[q.id]?.kind === "capital" && M.carriers[q.id].parent_line === c.id) sub.push({ part: "completion", component: "capital_reporter", line: q.id, parent_line: c.id, value_bn: q.amount_bn * q.response * scale });
    for (const q of col) if (q.kind === "college_capital" && q.source_line === c.id) sub.push({ part: "college", component: "college_capital_interaction", kind: "college_capital", line: c.id, capital_source_line: c.id, population: q.population, ...(q.generation ? { generation: q.generation } : {}), value_bn: q.delta_bn * scale });
    for (const q of cov) if (q.source_side === "capital" && q.source_line === c.id) sub.push({ part: "coverage", component: "capital_coverage", line: q.line, source_line: c.id, generation: q.generation, population: "coverage", value_bn: q.coverage_bn * toR20 });
    for (const q of M.count[s.reading]) if (q.economic_class === "capital_return" && q.source_line === c.id) sub.push({ part: "count", component: "capital_count_interaction", source_item: q.item, line: q.line, source_line: c.id, generation: q.generation, population: "count", value_bn: q.value_bn * toR20 });
    for (const q of health) if (q.side === "capital" && q.source_line === c.id) sub.push({ part: "health", component: "health_capital", line: q.line, source_line: c.id, generation: q.generation, population: q.population, value_bn: q.delta_bn });
    const parts = {};
    for (const p of ["engine", "completion", "college", "coverage", "count", "health"]) parts[p] = sum(sub.filter((q) => q.part === p).map((q) => q.value_bn));
    return { id: c.id, physical: M.physical[c.id] || c.id, level: levelOf(c), stock_charged_bn: c.stock_charged_bn, key: c.key, response: c.response, parts, sub, at_r20_bn: sum(Object.values(parts)) };
  });
  return { charged: true, R20, pieces };
}

const rateOf = (piece, s, R20, on22) => on22 ? RATES[piece.level][END[s.reading]] : R20;

// Long-run K-12 key for readings that charge no capital (year one): taken at the matched end specification.
function longRunK12(X, s, evaluate) {
  const M = apiMeta(X);
  if (M.lr[s.reading]) return M.lr[s.reading];
  const spec = X.MAIN_SPECS[s.reading === "low" ? 16 : 11], r = evaluate(X.payloadModel(), spec), cp = capitalPieces(X, r, spec);
  const k12 = cp.pieces.filter((p) => K12_IDS.has(p.id)), stock = k12[0].stock_charged_bn;
  const edu = r.evaluation.spending.find((q) => q.id === "education_services");
  M.lr[s.reading] = { key: sum(k12.map((p) => p.at_r20_bn)) / (stock * cp.R20), education_response: edu.response };
  return M.lr[s.reading];
}
// Central long-run run at the matched end specification: the responses at which coverage and count parts are priced.
function centralRun(X, s) {
  const M = apiMeta(X);
  if (!M.central[s.reading]) M.central[s.reading] = X.OCT15.evaluateFull(X.OCT15.payloadModel(), X.OCT15.MAIN_SPECS[s.reading === "low" ? 16 : 11]);
  return M.central[s.reading];
}

/* Item 24's parks base: the run's recreation operating amount (engine line, its carriers, coverage and count spending
   parts). In a reading with no long-run response (year one) the coverage and count parts are transported by the
   source line's response ratio, as companions.cjs companionPost does; in the long run they are held, as v9 holds
   coverage and count parts across a reading's specifications. */
function parkRows(X, r, s) {
  const M = apiMeta(X), rows = [], fy = !s.long_run;
  const responseIn = (run, id) => { const q = run.evaluation.spending.find((x) => x.id === id); if (!q) fail("parks source line absent " + id); return q.response; };
  for (const q of r.evaluation.spending) {
    if (q.id === PARK_LINE) rows.push({ part: "parks_line", component: "spending_line", line: q.id, value_bn: q.amount_bn * q.response });
    else if (M.carriers[q.id]?.kind === "line" && M.carriers[q.id]?.side === "spending" && M.carriers[q.id].parent_line === PARK_LINE) rows.push({ part: "parks_completion", component: "spending_carrier", line: q.id, parent_line: PARK_LINE, value_bn: q.amount_bn * q.response });
  }
  const cov = X.POST_ENGINE.coverage?.by_end[s.reading]?.decomposition?.line_parts || [];
  for (const q of cov) if (q.source_side === "spending" && q.source_line === PARK_LINE) {
    let m = 1;
    if (fy) { if (q.economic_class !== "fiscal_line" || !(q.source_response > 0)) fail("parks coverage part has no source response"); m = responseIn(r, PARK_LINE) / q.source_response; }
    rows.push({ part: "parks_coverage", component: "spending_coverage", line: q.line, source_line: PARK_LINE, generation: q.generation, population: "coverage", central_value_bn: q.coverage_bn, multiplier: m, value_bn: q.coverage_bn * m });
  }
  for (const q of M.count[s.reading]) if (q.source_side === "spending" && q.source_line === PARK_LINE) {
    let m = 1;
    if (fy) {
      if (q.economic_class !== "fiscal_line") fail("parks count part is not a fiscal line");
      const before = responseIn(centralRun(X, s), PARK_LINE), after = responseIn(r, PARK_LINE);
      m = before === 0 ? (after === 0 ? 1 : fail("zero central parks response")) : after / before;
    }
    rows.push({ part: "parks_count", component: "spending_count", source_item: q.item, line: q.line, source_line: PARK_LINE, generation: q.generation, population: "count", central_value_bn: q.value_bn, multiplier: m, value_bn: q.value_bn * m });
  }
  return rows;
}

/* The v10 post-engine additions for one run. `on` is a set of item numbers; `land` a loadLand() result.
   Returns amounts by item id, line-level parts by item id, and `rows`: every amount as routable sub-rows
   ({item, part, component, line, generation?, population?, value_bn, coef, delta_bn}); sum(rows) = total. */
function post(X, r, s, on, { land = LAND, evaluate = null } = {}) {
  const amounts = {}, parts = {}, rows = [];
  const has = (n) => on.has(n);
  if (has(25) && !land) fail("item 25 selected without a land lane");
  const cp = capitalPieces(X, r, s), on22 = has(22);
  if (on22 && cp.charged && Math.abs(cp.R20 - RC) > 1e-15) fail("item 22 needs item 20 at arm B (the case rate)");
  const rel = (p) => rateOf(p, s, cp.R20, on22) / cp.R20;
  const emit = (n, p, coef, extra = {}) => { for (const q of p.sub) rows.push({ item: IDS[n], ...q, piece: p.id, level: p.level, coef, delta_bn: q.value_bn * coef, ...extra }); };
  if (has(22)) {
    const out = cp.pieces.map((p) => {
      const rate = rateOf(p, s, cp.R20, true), coef = rate / cp.R20 - 1;
      emit(22, p, coef);
      return { line: p.id, level: p.level, rate, at_case_rate_bn: p.at_r20_bn, by_part_at_case_rate_bn: p.parts, delta_bn: p.at_r20_bn * coef };
    });
    amounts[IDS[22]] = sum(out.map((q) => q.delta_bn)); parts[IDS[22]] = out;
  }
  if (has(23)) {
    const k = embeddedK(s.allocation), D = k12Dep(k), k12 = cp.pieces.filter((p) => K12_IDS.has(p.id)), Fr = K12A.F_stock_combined / k - 1;
    let ret = 0, key, rule, dep_bn;
    if (cp.charged) {
      const stock = k12[0].stock_charged_bn;
      if (!k12.every((p) => p.stock_charged_bn === stock)) fail("K-12 fee offset does not share the stock");
      ret = sum(k12.map((p) => p.at_r20_bn * rel(p))); key = sum(k12.map((p) => p.at_r20_bn)) / (stock * cp.R20);
      rule = "return at this specification's rate; depreciation on its K-12 capital key and response";
      dep_bn = key * D;
      for (const p of k12) emit(23, p, rel(p) * Fr + D / (stock * cp.R20));
    } else {
      if (!evaluate) fail("item 23 in a no-capital reading needs the v9 evaluator");
      const lr = longRunK12(X, s, evaluate), edu = r.evaluation.spending.find((q) => q.id === "education_services");
      key = lr.key * edu.response / lr.education_response; dep_bn = key * D;
      rule = "no capital return in this reading; depreciation at the matched long-run K-12 key, transported by the education_services response ratio";
      rows.push({ item: IDS[23], part: "depreciation_year_one", component: "spending_line", line: "education_services", value_bn: key, coef: D, delta_bn: dep_bn });
    }
    const ret_bn = ret * Fr;
    amounts[IDS[23]] = ret_bn + dep_bn;
    parts[IDS[23]] = [{ part: "return", k12_return_bn: ret, factor: K12A.F_stock_combined / k, delta_bn: ret_bn }, { part: "depreciation", k12_key: key, embedded_k: k, delta_bn: dep_bn, rule }];
  }
  if (has(24)) {
    const pr = parkRows(X, r, s), parent = r.evaluation.spending.find((q) => q.id === PARK_LINE), pc = PARK_SL / parent.national_bn * PARK_INDEX_DELTA;
    for (const q of pr) rows.push({ item: IDS[24], ...q, coef: pc, delta_bn: q.value_bn * pc });
    const op = sum(pr.map((q) => q.value_bn)), park_bn = op * pc;
    const cf = HIGHER_FRACTION * (COLLEGE_FACTOR - 1), colPieces = cp.pieces.filter((p) => COLLEGE_IDS.has(p.id));
    for (const p of colPieces) emit(24, p, rel(p) * cf);
    const college_capital = sum(colPieces.map((p) => p.at_r20_bn * rel(p))), college_bn = college_capital * cf;
    amounts[IDS[24]] = park_bn + college_bn;
    parts[IDS[24]] = [{ part: "parks_matched_municipal", unpriced_operating_bn: op, transported: !s.long_run, delta_bn: park_bn }, { part: "college_gross_book_capital", college_capital_bn: college_capital, higher_fraction: HIGHER_FRACTION, factor: COLLEGE_FACTOR, delta_bn: college_bn }];
  }
  if (has(25)) {
    const out = [];
    for (const [line, v] of Object.entries(land.lines)) {
      const ps = cp.pieces.filter((p) => p.physical === line);
      if (cp.charged && !ps.length) fail("land line has no capital component " + line);
      const stock = ps[0]?.stock_charged_bn;
      if (!ps.every((p) => p.stock_charged_bn === stock)) fail("land line fee offsets do not share the stock " + line);
      // value x key x response x rate = value x (full capital return at this rate) / stock; no depreciation.
      const coef = cp.charged ? sum(ps.map((p) => p.at_r20_bn * rel(p))) / stock : 0;
      for (const p of ps) emit(25, p, v.central * v.group_ratio.central * rel(p) / stock, { land_line: line });
      out.push({ line, group_ratio: v.group_ratio, value_central_bn: v.central, coef_at_rate: coef, rate: cp.charged ? rateOf(ps[0], s, cp.R20, on22) : 0,
        delta_bn: v.central * v.group_ratio.central * coef, low_value_bn: v.low * v.group_ratio.low * coef, high_value_bn: v.high * v.group_ratio.high * coef });
    }
    amounts[IDS[25]] = sum(out.map((q) => q.delta_bn)); parts[IDS[25]] = out;
  }
  for (const v of Object.values(amounts)) if (!Number.isFinite(v)) fail("nonfinite v10 amount");
  for (const [id, v] of Object.entries(amounts)) if (Math.abs(sum(rows.filter((q) => q.item === id).map((q) => q.delta_bn)) - v) > 1e-9) fail("sub-rows do not close " + id);
  return { amounts, parts, rows, total_bn: sum(Object.values(amounts)), capital_at_case_rate_bn: sum(cp.pieces.map((p) => p.at_r20_bn)), capital_pieces: cp.pieces.map(({ sub, ...p }) => p) };
}

module.exports = { IDS, ORDER, BESIDE, RATES, LEVEL_BY_COMPONENT, VARIANT_LEVEL, VARIANT_PARENT, ON_PARENT, RATE_SOURCE, RC, BOUND, readRateModel, LAND, LAND_ENV, loadLand, capitalPieces, parkRows, post, levelOf, k12Dep,
  constants: { k12: { F_structures: K12A.F_structures, F_equipment: K12A.F_equipment, F_stock_combined: K12A.F_stock_combined, embedded_k: embeddedK("personal"), applied_factors: { structures: K12A.F_structures / embeddedK("personal"), equipment: K12A.F_equipment / embeddedK("personal"), stock_combined: K12A.F_stock_combined / embeddedK("personal") }, depreciation_national_bn: K12_DEP_NATIONAL },
    parks: { index_delta: PARK_INDEX_DELTA, sl_budget_bn: PARK_SL }, college: { factor: COLLEGE_FACTOR, higher_fraction: HIGHER_FRACTION } } };
