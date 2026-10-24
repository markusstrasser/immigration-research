/* Candidate v10 items 22-25: post-engine capital and price terms on any v9 case API.

Every term is derived inside the run it prices: per specification and method, from the v9 evaluator's own capital
components, union-completion carriers, own coverage parts, items 16/17 count parts, item 15 college capital and
item 21 health capital. Nothing here edits the engine model; v10 adds no edits and no people.

  22 capital_rate_theta_bound   each end's rate (theta = 1 low, theta = 0 high) on every capital piece item 20 prices
  23 k12_capital_where_enrolled K-12 capital where enrolled, divisor with the embedded preferred school price k
  24 where_used_prices          matched municipal parks (operating) + covered-college gross-book capital proxy
  25 public_land                land under public capital, read from V10_LAND_LANE; off when unset

Sources (read-only): public_capital_rate_2026_10_24/derived/rate_model.json theta_pairing.bound;
school_capital_where_enrolled_2026_10_24/derived/summary.json; where_used_prices_2026_10_24/derived/{parks.json,
college_factors.csv}; user_fee_allocation_2026_10_07/derived/fee_lines.json;
state_priced_services_2026_09_29/derived/corrections.csv.
*/
"use strict";
const fs = require("fs"), path = require("path");
const FISCAL = path.join(__dirname, "..");
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
const END = { low: 0, high: 1 };

// Item 22: the bound over theta (operator, 2026-10-24 15:00 JST). Rates by end index [low, high].
const RATE_MODEL = read("public_capital_rate_2026_10_24/derived/rate_model.json");
const BOUND = RATE_MODEL.theta_pairing.bound;
const RC = RATE_MODEL.r_c;
if (Math.abs(RC - 0.020810698764237804) > 1e-15) fail("case rate moved");
if (JSON.stringify(BOUND.theta_by_end) !== "[1,0]") fail("bound is not theta 1 low / 0 high");
const RATES = { state_local: BOUND.rate_state_local_by_end, state_local_highways: BOUND.rate_state_local_highways_by_end, federal: BOUND.rate_federal_by_end };
// rate_model.py level_of: hwy_sl alone takes the federal-aid blend; any line at the federal level the federal margin.
const levelOf = (c) => c.id === "hwy_sl" ? "state_local_highways" : c.level === "federal" ? "federal" : c.level === "state_local" ? "state_local" : fail("unknown capital level " + c.id + " " + c.level);

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

// Item 25: per-line land values from a lane directory (derived/land_by_line.csv). Off when unset.
function loadLand(dir, { group_ratio_override = {} } = {}) {
  if (!dir) return null;
  const file = path.resolve(dir, "derived/land_by_line.csv");
  if (!fs.existsSync(file)) fail("land lane has no derived/land_by_line.csv: " + file);
  const rows = csvRows(file), lines = {};
  // K-12 land is the where-enrolled weighted value; its ratio may differ by value variant (school caps), so a lane
  // gives group_ratio and optionally group_ratio_low / group_ratio_high; other lines default to 1.
  const num = (x) => x !== undefined && x !== "" ? +x : undefined;
  for (const r of rows) {
    for (const k of ["value_central_bn", "value_low_bn", "value_high_bn"]) if (!Number.isFinite(+r[k])) fail(`land ${r.line} ${k} not numeric`);
    const o = group_ratio_override[r.line];
    const central = o !== undefined ? (typeof o === "number" ? o : o.central) : num(r.group_ratio);
    if (r.line === "k12" && central === undefined) fail("land lane gives no K-12 group_ratio column");
    const ratio = { central: central ?? 1 };
    for (const v of ["low", "high"]) ratio[v] = o !== undefined && typeof o === "object" ? o[v] : num(r["group_ratio_" + v]) ?? ratio.central;
    if (!Object.values(ratio).every((x) => Number.isFinite(x) && x > 0)) fail("bad land group_ratio " + r.line);
    lines[r.line] = { central: +r.value_central_bn, low: +r.value_low_bn, high: +r.value_high_bn, group_ratio: ratio };
  }
  return { dir: path.relative(path.resolve(FISCAL, "../.."), path.resolve(dir)), file: path.relative(path.resolve(FISCAL, "../.."), file), lines };
}
const LAND_ENV = process.env.V10_LAND_LANE || null;
const LAND = loadLand(LAND_ENV);

// Per-API caches (the API object is immutable for a run).
const metaCache = new WeakMap();
function apiMeta(X) {
  if (metaCache.has(X)) return metaCache.get(X);
  const physical = Object.fromEntries(X.capitalMeta(X.withCentral({})).components.map((c) => [c.id, c.of_component || c.id]));
  const out = { physical, carriers: X.POST_ENGINE.union_completion?.carriers || {}, count: {}, lr: {} };
  for (const end of ["low", "high"]) out.count[end] = ["native_minor_calibration", "coverage_tenure"].flatMap((id) => C.countParts(X.POST_ENGINE[id], end));
  metaCache.set(X, out);
  return out;
}

/* Capital pieces of one evaluated run at item 20's rate R20, by capital component.
   Construction as public_land_2026_10_24/case_contract.cjs, which closes to the 7% arm at the ends. */
function capitalPieces(X, r, s) {
  if (!s.rate || !r.capital?.components?.length) return { charged: false, R20: 0, pieces: [] };
  const M = apiMeta(X), R20 = RATE20.rateFor(X.POST_ENGINE.one_rate, s), scale = R20 / s.rate, toR20 = R20 / RATE20.RATE;
  const cov = X.POST_ENGINE.coverage?.by_end[s.reading]?.decomposition?.line_parts || [];
  const col = r.v9_post_engine?.parts?.public_college_response || [];
  const health = r.v9_post_engine?.parts?.health_residual_key || [];
  const pieces = r.capital.components.map((c) => {
    if (Math.abs(c.return_bn - c.stock_charged_bn * c.key * c.response * s.rate) > 1e-9) fail("engine capital identity " + c.id);
    const parts = {
      engine: c.return_bn * scale,
      completion: sum(r.evaluation.spending.filter((q) => M.carriers[q.id]?.kind === "capital" && M.carriers[q.id].parent_line === c.id).map((q) => q.amount_bn * q.response)) * scale,
      college: sum(col.filter((q) => q.kind === "college_capital" && q.source_line === c.id).map((q) => q.delta_bn)) * scale,
      coverage: sum(cov.filter((q) => q.source_side === "capital" && q.source_line === c.id).map((q) => q.coverage_bn)) * toR20,
      count: sum(M.count[s.reading].filter((q) => q.economic_class === "capital_return" && q.source_line === c.id).map((q) => q.value_bn)) * toR20,
      health: sum(health.filter((q) => q.side === "capital" && q.source_line === c.id).map((q) => q.delta_bn)),
    };
    return { id: c.id, physical: M.physical[c.id] || c.id, level: levelOf(c), stock_charged_bn: c.stock_charged_bn, key: c.key, response: c.response, parts, at_r20_bn: sum(Object.values(parts)) };
  });
  return { charged: true, R20, pieces };
}

const rateFor = (piece, s, R20, on22) => on22 ? RATES[piece.level][END[s.reading]] : R20;

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

/* The v10 post-engine additions for one run. `on` is a set of item numbers; `land` a loadLand() result. */
function post(X, r, s, on, { land = LAND, evaluate = null } = {}) {
  const amounts = {}, parts = {};
  const has = (n) => on.has(n);
  if (has(25) && !land) fail("item 25 selected without a land lane");
  const cp = capitalPieces(X, r, s), on22 = has(22);
  if (on22 && cp.charged && Math.abs(cp.R20 - RC) > 1e-15) fail("item 22 needs item 20 at arm B (the case rate)");
  const at = (p) => p.at_r20_bn * rateFor(p, s, cp.R20, on22) / cp.R20;
  if (has(22)) {
    const rows = cp.pieces.map((p) => ({ line: p.id, level: p.level, at_case_rate_bn: p.at_r20_bn, rate: rateFor(p, s, cp.R20, true), delta_bn: at(p) - p.at_r20_bn }));
    amounts[IDS[22]] = sum(rows.map((q) => q.delta_bn)); parts[IDS[22]] = rows;
  }
  if (has(23)) {
    const k = embeddedK(s.allocation), k12 = cp.pieces.filter((p) => K12_IDS.has(p.id));
    let ret = 0, key, rule;
    if (cp.charged) {
      const stock = k12[0].stock_charged_bn;
      if (!k12.every((p) => p.stock_charged_bn === stock)) fail("K-12 fee offset does not share the stock");
      ret = sum(k12.map(at)); key = sum(k12.map((p) => p.at_r20_bn)) / (stock * cp.R20); rule = "return at this specification's rate; depreciation on its K-12 capital key and response";
    } else {
      if (!evaluate) fail("item 23 in a no-capital reading needs the v9 evaluator");
      const lr = longRunK12(X, s, evaluate), edu = r.evaluation.spending.find((q) => q.id === "education_services");
      key = lr.key * edu.response / lr.education_response; rule = "no capital return in this reading; depreciation at the matched long-run K-12 key, transported by the education_services response ratio";
    }
    const ret_bn = ret * (K12A.F_stock_combined / k - 1);
    const dep_bn = key * (K12_DEP_NATIONAL.structures * (K12A.F_structures / k - 1) + K12_DEP_NATIONAL.equipment * (K12A.F_equipment / k - 1));
    amounts[IDS[23]] = ret_bn + dep_bn;
    parts[IDS[23]] = [{ part: "return", k12_return_bn: ret, factor: K12A.F_stock_combined / k, delta_bn: ret_bn }, { part: "depreciation", k12_key: key, embedded_k: k, delta_bn: dep_bn, rule }];
  }
  if (has(24)) {
    const M = apiMeta(X), ids = new Set(["recreation_culture"]);
    const cov = X.POST_ENGINE.coverage?.by_end[s.reading]?.decomposition?.line_parts || [];
    const op = sum(r.evaluation.spending.filter((q) => ids.has(q.id) || (M.carriers[q.id]?.kind === "line" && M.carriers[q.id]?.side === "spending" && ids.has(M.carriers[q.id].parent_line))).map((q) => q.amount_bn * q.response))
      + sum(cov.filter((q) => q.source_side === "spending" && ids.has(q.source_line)).map((q) => q.coverage_bn))
      + sum(M.count[s.reading].filter((q) => q.source_side === "spending" && ids.has(q.source_line)).map((q) => q.value_bn));
    const parent = r.evaluation.spending.find((q) => q.id === "recreation_culture");
    const park_bn = op * PARK_SL / parent.national_bn * PARK_INDEX_DELTA;
    const college_capital = cp.charged ? sum(cp.pieces.filter((p) => COLLEGE_IDS.has(p.id)).map(at)) : 0;
    const college_bn = college_capital * HIGHER_FRACTION * (COLLEGE_FACTOR - 1);
    amounts[IDS[24]] = park_bn + college_bn;
    parts[IDS[24]] = [{ part: "parks_matched_municipal", unpriced_operating_bn: op, delta_bn: park_bn }, { part: "college_gross_book_capital", college_capital_bn: college_capital, higher_fraction: HIGHER_FRACTION, factor: COLLEGE_FACTOR, delta_bn: college_bn }];
  }
  if (has(25)) {
    const rows = [];
    for (const [line, v] of Object.entries(land.lines)) {
      const ps = cp.pieces.filter((p) => p.physical === line);
      if (cp.charged && !ps.length) fail("land line has no capital component " + line);
      const stock = ps[0]?.stock_charged_bn;
      if (!ps.every((p) => p.stock_charged_bn === stock)) fail("land line fee offsets do not share the stock " + line);
      // value x key x response x rate = value x (full capital return at this rate) / stock; no depreciation.
      const coef = cp.charged ? sum(ps.map(at)) / stock : 0;
      rows.push({ line, group_ratio: v.group_ratio, value_central_bn: v.central, coef_at_rate: coef, rate: cp.charged ? rateFor(ps[0], s, cp.R20, on22) : 0,
        delta_bn: v.central * v.group_ratio.central * coef, low_value_bn: v.low * v.group_ratio.low * coef, high_value_bn: v.high * v.group_ratio.high * coef });
    }
    amounts[IDS[25]] = sum(rows.map((q) => q.delta_bn)); parts[IDS[25]] = rows;
  }
  for (const v of Object.values(amounts)) if (!Number.isFinite(v)) fail("nonfinite v10 amount");
  return { amounts, parts, total_bn: sum(Object.values(amounts)), capital_at_case_rate_bn: sum(cp.pieces.map((p) => p.at_r20_bn)) };
}

module.exports = { IDS, ORDER, RATES, RC, BOUND, LAND, LAND_ENV, loadLand, capitalPieces, post, levelOf,
  constants: { k12: { F_structures: K12A.F_structures, F_equipment: K12A.F_equipment, F_stock_combined: K12A.F_stock_combined, embedded_k: embeddedK("personal"), applied_factors: { structures: K12A.F_structures / embeddedK("personal"), equipment: K12A.F_equipment / embeddedK("personal"), stock_combined: K12A.F_stock_combined / embeddedK("personal") }, depreciation_national_bn: K12_DEP_NATIONAL },
    parks: { index_delta: PARK_INDEX_DELTA, sl_budget_bn: PARK_SL }, college: { factor: COLLEGE_FACTOR, higher_fraction: HIGHER_FRACTION } } };
