/* Item 10: union completion. Source own-record keys are preserved in the source's
 * per-line price export. This bridge turns them back into signed raw amounts,
 * on transparent zero-national spending carriers. The case copies each real
 * parent line's selected key and response onto its carrier at evaluation time.
 * New keys not in the two source endpoint snapshots transport the preferred-key
 * own/canonical ratio; endpoint snapshots and the exact joint credit delta gate
 * the central result. Raw national totals of the source lines never change.
 */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto"), Module = require("module");
const FISCAL = path.resolve(__dirname, ".."), SOURCE = "union_completion_2026_10_14";
const P = require("../main_case_2026_10_14/package.cjs");
const CHILD = require("./child_records.cjs");
const clone = x => JSON.parse(JSON.stringify(x));
const read = rel => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha = rel => crypto.createHash("sha256").update(fs.readFileSync(path.join(FISCAL, rel))).digest("hex");
const block = s => { throw Error(`[BLOCKED] item union_completion: ${s}`); };
const END = ["low", "high"], SPECS = [16, 11], ALLOCS = ["personal", "shared"];
const S = { lane: SOURCE, file: `${SOURCE}/derived/candidate.json`, stub: false };
S.sha256 = sha(S.file);
const CAND = read(S.file), COUNTS = read(`${SOURCE}/derived/count_replicates.json`);
const CREDIT = read(`${SOURCE}/derived/credits_interaction.json`);
const ORIGINAL_RATES = read(`${SOURCE}/derived/added_band_prices.json`);
const PEOPLE_FILE = path.join(__dirname, "derived/union_people.json");
if (!fs.existsSync(PEOPLE_FILE)) block("run export_union_people.py before building the case");
const PEOPLE = JSON.parse(fs.readFileSync(PEOPLE_FILE, "utf8"));
const CREDIT_PARTS_FILE = path.join(__dirname, "derived/union_credit_parts.json");
const TABLE = fs.readFileSync(path.join(FISCAL, SOURCE, "derived/pricing_lines.csv"), "utf8").trim().split("\n");
const HEADER = TABLE.shift().split(",");
const PRICE = TABLE.map(s => Object.fromEntries(s.split(",").map((v, i) => [HEADER[i], i >= 5 ? Number(v) : v])));
const SNAP = Object.fromEntries(["set", "cash"].map(w => [w, read(`${SOURCE}/_cache/${w}/oct14/lines.json`)]));
const ARMS = { broad_report: { label: "all omitted Mexican-origin reporters plus the observed biological nonreporters", source_arm: "all_observed_completion" },
  all_age_extrapolation: { label: "one-US-parent reporters plus extrapolated nonreporting loss, observed children not added twice", source_arm: "central_all_age_extrapolation" } };
const both = n => ({ personal: n, shared: n });
const sum = xs => xs.reduce((s, x) => s + x, 0);
const sumMain = x => sum(x.map(r => r[0]));
const stat = x => ({ estimate: x[0], se: Math.sqrt(4 / 160 * sum(x.slice(1).map(v => (v - x[0]) ** 2))) });
const referenceEdits = JSON.stringify(P.correctionsPayload().edits);
const keyedRatesCache = new Map();
const sorted = x => x && typeof x === "object" && !Array.isArray(x)
  ? Object.fromEntries(Object.keys(x).sort().filter(k => x[k] !== undefined).map(k => [k, sorted(x[k])]))
  : Array.isArray(x) ? x.map(sorted) : x;
const optionsKey = o => {
  const common = Object.assign({}, o || {}); delete common.pension4;
  if (common.foreign_source_tax === false) delete common.foreign_source_tax;
  if (common.item6_first_year === false) delete common.item6_first_year;
  if (common.item6_low_corporate_response === 1) delete common.item6_low_corporate_response;
  if (common.allocation === "personal") delete common.allocation;
  if (common.profile === P.MAIN_PROFILE) delete common.profile;
  return JSON.stringify(sorted(P.withCentral(common)));
};
const centralOptionsKey = optionsKey({});
let jobNewParts = null;
function allSourceJobParts(wage, model) {
  if (!jobNewParts) {
    const file = path.join(FISCAL,"main_case_2026_10_14/item_job_capital.cjs");
    const source = fs.readFileSync(file,"utf8");
    if (source.split("function newParts(blk, wage, m) {").length !== 2) block("job source newParts boundary changed");
    const mod = new Module(file,module); mod.filename=file;
    mod.paths=Module._nodeModulePaths(path.dirname(file));
    mod._compile(source+"\nmodule.exports.unionNewParts = newParts;\n",file);
    if (typeof mod.exports.unionNewParts !== "function") block("job source newParts is unavailable");
    jobNewParts=mod.exports.unionNewParts;
  }
  return jobNewParts(P.JOBCAP.CENTRAL,wage,model);
}
const inactiveLine = (side, id, o) =>
  (side === "receipt" && id === "tenant_occupied_property" && o.property === "none")
  || (side === "spending" && ["roads_vmt_sl", "roads_vmt_fed"].includes(id) && o.roads === "resources");

function optionRates(B, options = {}, captureRaw = false) {
  if (options.item6_low_corporate_response !== undefined && !Number.isFinite(options.item6_low_corporate_response)) {
    block("item6_low_corporate_response is not a finite number");
  }
  const legacyDomestic = B.ITEM_ARMS?.job_capital_taxes === "foreign_source_removed";
  const domesticScope = !!options.foreign_source_tax || legacyDomestic;
  const editKey = JSON.stringify(B.correctionsPayload().edits);
  const optKey = optionsKey(options), key = captureRaw
    ? editKey + "|raw|foreign=" + domesticScope : editKey + "|" + optKey;
  if (!captureRaw && (B === P || editKey === referenceEdits) && optKey === centralOptionsKey) return ORIGINAL_RATES;
  if (keyedRatesCache.has(key)) return keyedRatesCache.get(key);
  // Read-only adapter of the source's full unit-band engine route. The only
  // computation change is the package supplied to that route. Its frozen-v7
  // oracle is retained in metadata but is not a gate on changed options.
  const file = path.join(FISCAL, SOURCE, "added_band_prices.cjs");
  let src = fs.readFileSync(file, "utf8");
  const anchor = 'const P = require(path.join(FISCAL, "main_case_2026_10_14/package.cjs"));';
  const gate = 'if (gates.some((g) => !g.pass)) block(JSON.stringify(gates));';
  const cells = 'const edits = P.AGE_MIX.cellsOf(m).map((c) =>';
  const mix = 'const MIX = read("added_age_mix_2026_10_07/derived/age_mix.json");';
  const units = 'const g3Unit = unit("g3"), g3 = g3Unit.rates, white = unit("white").rates, whiteRaw = unit("white", false).rates;';
  const costs = 'function costs(m, w) {';
  if ([anchor, gate, cells, mix, units, costs].some(a => src.split(a).length !== 2)) block("unit-band adapter source boundary changed");
  src = src.replace(anchor, "const P = module.unionPackage;").replace(gate,
    'const optionOriginalMixControl = gates.map(g => ({...g}));')
    .replace(cells, 'const edits = P.AGE_MIX.cellsOf(m).filter(c => !P.unitInactiveLine(c.side, c.line)).map((c) =>')
    .replace(mix, mix + '\n  MIX.meta.c3 = P.ITEM_DETAIL.added_age_mix.counts.c3;')
    .replace(units, 'const g3Unit = unit("g3"), whiteUnit = unit("white"), g3 = g3Unit.rates, white = whiteUnit.rates, whiteRaw = unit("white", false).rates;\n    if (module.captureRaw) module.unitModels.push({ band, g3: g3Unit.models, white: whiteUnit.models });')
    .replace(costs, costs + '\n    if (module.captureRaw) return [0, 0];');
  const mod = new Module(file, module); mod.filename = file;
  mod.paths = Module._nodeModulePaths(path.dirname(file));
  mod.captureRaw = captureRaw; mod.unitModels = [];
  const raw = Object.assign({}, P, B);
  if (domesticScope) raw.JOBCAP = Object.assign({}, raw.JOBCAP, {
    CENTRAL: raw.JOBCAP.blockOf("foreign_source_removed") });
  const routeChecks = { evaluations: 0, capital_disabled: options.capital === false,
    max_abs_capital_bn: 0, first_year_item6: !!options.item6_first_year,
    foreign_source_tax: domesticScope, legacy_domestic_arm: legacyDomestic };
  function wrap(api) {
    // The source deliberately prices set and cash together. A caller's fully
    // expanded options belong to its active set; retain each paired API's own
    // pension switch while applying their common economic options to both.
    const ownPension = api.withCentral({}).pension4;
    const opts = o => Object.assign({}, o || {}, options, { pension4: ownPension });
    const specsFor = o => {
      const specs = api.specsFor(opts(o));
      if (options.item6_low_corporate_response !== undefined) {
        for (const spec of specs) if (spec.reading === "low") {
          for (const id of ["corporate_capital", "corporate_labor"]) {
            spec.line_responses[`receipt:${id}`] = options.item6_low_corporate_response;
          }
        }
      }
      if (options.item6_first_year) {
        const FY = require("../break_conditions_2026_09_29/first_year_item6.cjs"), c = FY.calibration();
        for (const spec of specs) for (const id of ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"]) {
          const name = `receipt:${id}`;
          if (!Number.isFinite(spec.line_responses[name])) block(`first-year unit price lacks response ${name}`);
          spec.line_responses[name] *= FY.multiplier(id, "fixed_capital", c);
        }
      }
      return specs;
    };
    const selectedSpecs = specsFor({});
    return Object.assign({}, api, { withCentral: o => api.withCentral(opts(o)),
      modelFor: (name, method, o) => api.modelFor(name, method, api.withCentral(opts(o))),
      specsFor, MAIN_SPECS: selectedSpecs, MAIN_PROFILE: options.profile || api.MAIN_PROFILE || P.MAIN_PROFILE,
      evaluateFull: (m, spec, profile) => {
        const i = mod.unionPackage.MAIN_SPECS.indexOf(spec);
        const result = api.evaluateFull(m, i >= 0 ? selectedSpecs[i] : spec, profile);
        routeChecks.evaluations++;
        routeChecks.max_abs_capital_bn = Math.max(routeChecks.max_abs_capital_bn,
          Math.abs(result.capital.total_bn || 0));
        if (routeChecks.capital_disabled && routeChecks.max_abs_capital_bn !== 0) block("capital:false unit route charged public capital");
        return result;
      } });
  }
  mod.unionPackage = wrap(raw);
  mod.unionPackage.CASH = wrap(Object.assign({}, P.CASH, B.CASH));
  mod.unionPackage.unitInactiveLine = (side, id) => inactiveLine(side, id, options);
  mod._compile(src, file);
  const out = mod.exports.buildPrices();
  out.meta.option_prices = { options: clone(P.withCentral(options)), endpoints: SPECS.slice(),
    first_year_item6: !!options.item6_first_year,
    interpolation: "fresh engine prices at source specifications 16/11 under these options; changed specification ends are not a new source-age fit" };
  out.meta.price_route_checks = routeChecks;
  if (captureRaw) {
    out.unit_models = mod.unitModels;
    out.meta.raw_capture = "transformed raw G3/white unit models; scalar costs skipped, independently gated after native engine application";
  }
  keyedRatesCache.set(key, out); return out;
}
function byLine(m, side, id) { return m[side === "receipt" ? "receipts" : "spending"].lines.find(l => l.id === id); }
function creditAt(api, id, key, g3only) {
  if (!["federal_income_tax", "refundable_tax_credits"].includes(id)) return 0;
  const payload = api.correctionsPayload(), rec = payload.meta.items.find(i => i.id === "child_credits");
  if (!rec) return 0;
  return sum(Object.entries(rec.parts).filter(([name, part]) => {
    if (g3only && !name.startsWith("union_G3plus:") && !name.startsWith("lineage_g3plus:")) return false;
    const e = payload.edits[rec.edits.first + part.edit];
    return e.line === id && (e.scenario || e.key) === key;
  }).map(([, part]) => part.by.personal));
}
function zeroCell() { return Object.fromEntries(ALLOCS.map(a => [a, { target_bn: 0, other_bn: 0, share: 0 }])); }
function makeCarrier(id, keys, preferred, source) {
  return { id, family: "union_completion_carrier", label: `union completion: ${source.parent_line || source.kind}`,
    national_bn: 0, response_class: "service", preferred_key: preferred,
    keys: Object.fromEntries(keys.map(k => [k, zeroCell()])), union_source: source };
}
function modelCosts(api, m, ei, options = {}) {
  const tag = m.candidate ? Object.assign({}, m.candidate, m.candidate.v3 || {}, m.candidate.v4 || {}) : {};
  const ownOptions = Object.assign({}, tag, options, { allocation: "personal" });
  const spec = api.specsFor(ownOptions)[SPECS[ei]];
  if (!spec) block(`source option has no endpoint specification ${SPECS[ei]}`);
  const r = api.evaluateFull(m, spec, ownOptions.profile || P.MAIN_PROFILE);
  return { r, rows: r.evaluation.spending.concat(r.evaluation.receipts),
    capital: r.capital.components, production: -(r.evaluation.private_wtp_bn + r.evaluation.induced_receipts_bn) };
}

function build(ctx, arm, which) {
  if (!["set", "cash"].includes(which)) block(`unknown set ${which}`);
  if (arm && !ARMS[arm]) block(`unknown arm ${arm}`);
  const broad = arm === "broad_report", extrapolate = arm === "all_age_extrapolation";
  const ownField = broad ? "all_bn" : "central_bn";
  const api = which === "set" ? ctx.B : ctx.B.CASH;
  const central = which === "set" ? P : P.CASH;
  const baseModel = central.payloadModel(), currentModel = api.payloadModel();
  const jobWages = ctx.B.ITEM_DETAIL.job_capital_taxes[which].wage_share;
  const allSourceJobs = allSourceJobParts(jobWages,currentModel);
  function allSourceJobTarget(id, key) {
    // Reconstruct v7 item 6's all-source target on THIS lineage option, using
    // its authoritative newParts formula. currentModel may already have the
    // legacy domestic-source arm, so it cannot be the all-source denominator.
    // The source reporter's own job quantity stays fixed when lineage counts
    // change; only an actual source-tax re-key changes its tax numerator.
    const parts = allSourceJobs[`${id}|${key}`];
    if (!parts) block(`no source all-source job parts for ${id}/${key}`);
    const value = sum(P.JOBCAP.PARTS.map(p=>parts[p].personal));
    if (!Number.isFinite(value)) block(`non-finite source all-source job target for ${id}/${key}`);
    return value;
  }
  const option = ctx.B.correctionsPayload().meta.lineage;
  const c3 = ctx.DETAIL && ctx.DETAIL.added_age_mix && ctx.DETAIL.added_age_mix.counts
    ? ctx.DETAIL.added_age_mix.counts.c3 : ORIGINAL_RATES.meta.c3;
  const rows = PRICE.filter(r => r.basis === which).flatMap(r => {
    if (r.line === "business_property") return [{ ...r, line: "remaining_production_property" }];
    if (r.line !== "corporate") return [r];
    const source = SNAP[which].generations.G3plus[r.end].rows;
    const tax = source.filter(s => ["corporate_capital", "corporate_labor"].includes(s.id));
    const total = sum(tax.map(s => s.amount_bn));
    return tax.map(s => ({ ...r, line: s.id, central_bn: r.central_bn * s.amount_bn / total,
      all_bn: r.all_bn * s.amount_bn / total }));
  });
  const ng = COUNTS.observed_g3_rate_by_age, nl = COUNTS.observed_later_by_age;
  const nr = COUNTS[`reporter_${broad ? "all" : "central"}_by_age`];
  const reporterN = sumMain(nr), observedN = sumMain(ng) + sumMain(nl);
  const projected = COUNTS.reporter_central_by_age.map(r => r.map((v, i) => v * COUNTS.loss_ratio[i]));
  const lossN = extrapolate ? sumMain(projected) : observedN;
  const creditKey = broad ? "all_outsiders_plus_observed" : extrapolate ? "one_us_parent" : "one_us_parent_plus_observed";
  const credit = CREDIT.results[creditKey];
  if (!fs.existsSync(CREDIT_PARTS_FILE)) block("run export_union_credit_parts.py before building the case");
  const creditParts = JSON.parse(fs.readFileSync(CREDIT_PARTS_FILE, "utf8")).results[creditKey];
  if (!creditParts) block(`no generation-by-side credit parts for ${creditKey}`);
  const spending_lines = [], responses = {}, carrierMap = {}, plans = [], fixedPlans = [], parts = {};
  const sourceRows = Object.fromEntries(END.map(e => [e, SNAP[which].generations.G3plus[e].rows]));
  const realIds = new Set(sourceRows.low.concat(sourceRows.high).map(r => r.id));
  const groups = new Map();
  for (const r of rows) {
    if (!groups.has(r.line)) groups.set(r.line, []);
    groups.get(r.line).push(r);
  }
  // One real-line carrier holds every original key. Its own-record numerator is
  // anchored separately wherever the source evaluated a different key.
  for (const [id, rr] of groups) {
    if (!realIds.has(id)) continue;
    const sr = sourceRows.low.find(r => r.id === id) || sourceRows.high.find(r => r.id === id);
    const side = sr.side, original = byLine(baseModel, side, id);
    if (!original) block(`missing parent ${side}/${id}`);
    const originalCells = side === "receipt" ? original.cells : original.keys;
    const pref = side === "receipt" ? baseModel.receipts.reference : original.preferred_key;
    const anchors = {};
    for (const end of END) {
      const source = sourceRows[end].find(r => r.id === id);
      if (!source || !source.response) continue;
      const key = side === "receipt" ? source.scenario : source.key;
      const cost = sum(rr.filter(r => r.end === end).map(r => r[ownField]));
      const rawSigned = cost / source.response;
      const denominator = source.amount_bn - creditAt(central, id, key, true);
      const ratio = denominator ? rawSigned / denominator : 0;
      if (anchors[key] && Math.abs(anchors[key].rawSigned - rawSigned) > 1e-9) block(`${id}/${key} differs across source endpoints`);
      anchors[key] = { rawSigned, ratio, source_amount_bn: source.amount_bn, end };
    }
    const fallback = anchors[pref] || Object.values(anchors)[0];
    if (!fallback) continue;
    const keys = Object.keys(originalCells);
    for (const key of keys) {
      const cid = `union_completion_${id}_${key}`;
      const source = { kind: "line", side, parent_line: id, parent_key: key,
        keys: { k: key }, source_keys: Object.keys(anchors),
        extrapolated_key: !anchors[key], signed_spending_carrier: true };
      spending_lines.push(makeCarrier(cid, ["k"], "k", source)); carrierMap[cid] = source;
      const at = anchors[key] || fallback;
      // The source's G3+ numerator includes the placed original lineage, while
      // its own-record denominator is identified G3+. An option changes only
      // that numerator: add its model-cell difference on the same observed key.
      const ref = originalCells[key].personal.target_bn;
      const baseSigned = anchors[key] ? at.rawSigned : at.rawSigned * ref / originalCells[pref].personal.target_bn;
      const job = ["corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"].includes(id);
      const jobRef = job ? allSourceJobTarget(id, key) : ref;
      plans.push({ id: cid, key, parent: id, side,
        ref: job ? jobRef : ref - creditAt(central, id, key, false),
        current_credit: creditAt(api, id, key, false), baseSigned,
        ratio: job && jobRef ? baseSigned / jobRef : at.ratio,
        option_rule: job ? "own job-record quantity fixed; all-source target reconstructed on this lineage option, so legacy or later domestic-source re-keys change the numerator once" : "pooled G3 source amount changes on the same own-record key",
        part: `union_G3plus:${id}:${key}` });
    }
  }
  // Capital and production are explicit endpoint carriers. They retain source
  // own-record category prices and reprice on the corresponding option output.
  for (const [id, rr] of groups) {
    if (realIds.has(id)) continue;
    for (let ei = 0; ei < 2; ei++) {
      const end = END[ei], cost = sum(rr.filter(r => r.end === end).map(r => r[ownField]));
      const cid = `union_completion_${id}_${end}`;
      const kind = id === "production" ? "production" : "capital";
      const source = { kind, parent_line: id, end, source_cost_bn: cost };
      spending_lines.push(makeCarrier(cid, ["k"], "k", source)); carrierMap[cid] = source;
      responses[cid] = { receipt: false, override: cid, low: ei === 0 ? 1 : 0, high: ei === 1 ? 1 : 0 };
      const sourceCapital = SNAP[which].generations.G3plus[end].capital.find(c => c.id === id);
      const denom = kind === "production" ? SNAP[which].generations.G3plus[end].production.cost_bn : sourceCapital && sourceCapital.cost_bn;
      if (denom === undefined) block(`no ${kind} denominator for ${id}`);
      fixedPlans.push({ id: cid, key: "k", cost, denom, kind, source_id: id, ei,
        part: `union_G3plus:${id}:${end}` });
    }
  }
  // CHILD.build reads only the raw unit bundle and these two line-presence
  // switches. Cache immutable coefficients within this fixed arm/C3 context;
  // specification responses still enter the engine on every evaluation.
  const childrenByRaw = new WeakMap();
  const childAt = options => {
    const raw = optionRates(ctx.B, options, true), key = JSON.stringify([options.property === "none", options.roads === "resources"]);
    let variants = childrenByRaw.get(raw);
    if (!variants) { variants = new Map(); childrenByRaw.set(raw, variants); }
    if (!variants.has(key)) variants.set(key, CHILD.build(ctx, arm, which, options, raw));
    return variants.get(key);
  };
  const child = childAt({});
  const withProduction = (m, delta) => {
    if (JSON.stringify(m.production.dims) !== JSON.stringify(delta.dims)) block("child production grid differs from active model");
    for (const f of ["private_wtp_bn", "induced_receipts_bn"]) m.production[f] = m.production[f].map((v, i) => v + delta[f][i]);
    return m;
  };
  const childBumped = withProduction(P.Engine.applyCorrections(currentModel, { edits: child.edits, meta: currentModel.corrections }), child.production_delta);
  const childCosts = END.map((_, i) => modelCosts(api, childBumped, i).r.cost_bn - modelCosts(api, currentModel, i).r.cost_bn);
  const creditEdits = P.V6_PACKAGE.expand([{ side: "receipt", line: "federal_income_tax",
    by: { personal: credit.delta_receipt_edit_bn, shared: 0 } }]);
  const creditSpending = byLine(baseModel, "spending", "refundable_tax_credits");
  creditEdits.push({ side: "spending", line: "refundable_tax_credits", key: creditSpending.preferred_key,
    by: { personal: credit.delta_spending_edit_bn, shared: 0 } });
  const baseCosts = END.map((_, i) => modelCosts(central, baseModel, i));
  function editsAt(m, options = {}) {
    const out = plans.map(p => {
      const l = byLine(m, p.side, p.parent);
      if (!l && inactiveLine(p.side, p.parent, options)) return {
        side: "spending", line: p.id, key: "k", by: both(0) };
      if (!l) block(`option model lacks ${p.side}/${p.parent}`);
      const cell = p.side === "receipt" ? l.cells[p.key] : l.keys[p.key];
      if (!cell) block(`option model lacks key ${p.parent}/${p.key}`);
      return { side: "spending", line: p.id, key: "k",
        by: both(p.baseSigned + p.ratio * (cell.personal.target_bn - p.current_credit - p.ref)) };
    });
    const costs = END.map((_, i) => modelCosts(api, m, i, options));
    for (const p of fixedPlans) {
      if (p.kind === "capital" && (options.capital === false
        || (options.capital_variant === "k12_at_pupil_share" && p.source_id === "k12_user_fees"))) {
        out.push({ side: "spending", line: p.id, key: "k", by: both(0) });
        continue;
      }
      const currentComponent = p.kind === "capital" ? costs[p.ei].capital.find(c => c.id === p.source_id) : null;
      if (p.kind === "capital" && !currentComponent) block(`capital option lacks source component ${p.source_id}; no implicit zero`);
      const current = p.kind === "production" ? costs[p.ei].production : currentComponent.return_bn;
      const ref = p.kind === "production" ? baseCosts[p.ei].production : baseCosts[p.ei].capital.find(c => c.id === p.source_id).return_bn;
      out.push({ side: "spending", line: p.id, key: "k", by: both(p.cost + (p.denom ? p.cost / p.denom * (current - ref) : 0)) });
    }
    return out.concat(childAt(options).edits, clone(creditEdits));
  }
  const edits = editsAt(currentModel);
  for (let i = 0; i < edits.length; i++) {
    const e = edits[i];
    const childStart = plans.length + fixedPlans.length;
    if (i >= childStart && i < childStart + child.edits.length) {
      parts[`lineage_g3plus:observed_nonreporters:${e.side}:${e.line}:${e.scenario || e.key}`] = { edit: i, by: clone(e.by) };
      continue;
    }
    if (!e.line.startsWith("union_completion_")) {
      const sourceTotal = e.side === "receipt" ? credit.delta_receipt_edit_bn : credit.delta_spending_edit_bn;
      const field = e.side === "receipt" ? "receipt_edit_bn" : "spending_edit_bn";
      const scale = sourceTotal ? e.by.personal / sourceTotal : 0;
      let accumulated = 0;
      for (const [j, g] of ["G1", "G2", "G3+"].entries()) {
        const value = j === 2 ? e.by.personal - accumulated : creditParts[g][field] * scale;
        accumulated += value;
        const generation = g === "G3+" ? "G3plus" : g;
        parts[`union_${generation}:credit_interaction:${e.line}:${e.scenario || e.key}`] = {
          edit: i, by: { personal: value, shared: 0 } };
      }
      continue;
    }
    const name = i < plans.length ? plans[i].part : e.line.startsWith("union_completion_nonreporters")
      ? `lineage_g3plus:observed_nonreporters:${e.line}` : e.line.startsWith("union_completion_")
        ? `union_G3plus:${e.line}` : `union_G3plus:credit_interaction:${e.line}:${e.scenario || e.key}`;
    parts[name] = { edit: i, by: clone(e.by) };
  }
  const candidateArm = broad ? "all_observed_completion" : extrapolate ? "central_all_age_extrapolation" : "central_observed_completion";
  const sourceDelta = END.map(end => CAND.results[which][end].arms[candidateArm].delta_bn);
  const counts = { total: reporterN + lossN, reporters: reporterN, nonreporters: lossN,
    reporting_union_addition: reporterN, added_lineage: lossN,
    by_generation: { G1: 0, G2: 0, G3plus: reporterN + lossN },
    reporters_by_generation: { G1: 0, G2: 0, G3plus: reporterN },
    nonreporters_by_generation: { G1: 0, G2: 0, G3plus: lossN },
    observed_g3_rate: sumMain(ng), observed_later: sumMain(nl),
    baseline_account_union: CAND.counts.baseline.account_union,
    baseline_lineage_population: CAND.counts.baseline.lineage_population,
    reporting_union: CAND.counts.baseline.account_union + reporterN,
    lineage_population: (option && option.counts ? option.counts.lineage_population : CAND.counts.baseline.lineage_population) + reporterN + lossN };
  const approximations = ["Unobserved source line keys transport the measured preferred-key own/canonical ratio; the source's two endpoint keys are exact.",
    "Reporter option repricing keeps own-record numerators and identified-G3 denominators fixed and changes the pooled G3 source amount by the option's full-model cell difference.",
    "Reporter capital and production retain their source endpoint own-record shares. Nonreporting children use native transformed own-age G3/white line cells and production arrays at each option C3, so every actual key, service response, public-capital rule and production specification applies directly.",
    "Reporter capital and production use endpoint source own-record share transport; there are no child endpoint carriers or fixed child service charges.",
    "Shared-allocation reporter carriers transport the personal own-record raw amount; the source did not measure newly expanded shared boundaries."];
  const meta = { union_completion: { source: S, arm: arm || "central", counts, c3, carriers: carrierMap,
    source_delta_bn: sourceDelta, credit_interaction_bn: credit.delta_bn,
    observed_records: PEOPLE.records.filter(r => (broad ? r.broad_reporter : r.central_reporter) || (!extrapolate && r.observed_nonreporter)),
    record_key: PEOPLE.key, unlocated_extrapolation_people: extrapolate ? lossN : 0,
    production_delta: { generation: "G3plus", population: "added", part: "lineage_g3plus:observed_nonreporters", ...clone(child.production_delta) },
    nonreporter_age_counts: { g3_rate: ng.map(r => r[0]), later: nl.map(r => r[0]) },
    credit_interaction_se_bn: credit.delta_se_bn, credit_parts_by_generation_by_side: creditParts,
    credit_generation_changes_bn: Object.fromEntries(["G1", "G2", "G3+"].map(g => [g, credit.by_generation[g] - CREDIT.results.canonical.by_generation[g]])),
    paired_replicate_delta_bn: END.map(end => CAND.results[which][end].arms[candidateArm].replicate_delta_bn),
    approximations, source_hashes: Object.fromEntries([S.file, `${SOURCE}/derived/pricing_lines.csv`, `${SOURCE}/derived/added_band_prices.json`, `${SOURCE}/derived/counts.csv`, `${SOURCE}/derived/credits_interaction.json`,
      "main_case_2026_10_14/item_job_capital.cjs", `${SOURCE}/added_band_prices.cjs`, `${SOURCE}/derived/count_replicates.json`].map(f => [f, sha(f)])) } };
  const partsByEdit = new Map();
  for (const entry of Object.entries(parts)) {
    const index = entry[1].edit;
    if (!partsByEdit.has(index)) partsByEdit.set(index, []);
    partsByEdit.get(index).push(entry);
  }
  function partsAt(m, options = {}) {
    const identity = e => [e.side,e.line,e.scenario||e.key].join("|");
    const original = new Map(), seen = new Map();
    edits.forEach((e,i) => {
      const key = identity(e), ordinal = seen.get(key)||0; seen.set(key,ordinal+1);
      original.set(key+"|"+ordinal,i);
    });
    const out = {}; seen.clear();
    editsAt(m,options).forEach((e,i) => {
      const key = identity(e), ordinal = seen.get(key)||0; seen.set(key,ordinal+1);
      const prior = original.get(key+"|"+ordinal);
      if (prior===undefined) block(`native child option introduced unregistered cell ${key}`);
      const old = partsByEdit.get(prior) || [];
      if (!old.length) block(`native child option cell lacks parts ${key}`);
      const sums = {personal:0,shared:0};
      old.forEach(([name,p],j)=>{
        const by = Object.fromEntries(ALLOCS.map(a=>[a,j===old.length-1?e.by[a]-sums[a]:p.by[a]]));
        for(const a of ALLOCS)sums[a]+=by[a];
        out[name]={edit:i,by};
      });
    });
    return out;
  }
  return { edits, editsAt, parts, partsAt, spending_lines, receipt_lines: [], responses, meta,
    production_delta: child.production_delta,
    productionDeltaAt: (m, options = {}) => childAt(options).production_delta,
    record: { counts, source_delta_bn: sourceDelta, credit_interaction_bn: credit.delta_bn, approximations },
    detail: { counts, child_cost_bn: childCosts, source_delta_bn: sourceDelta, carriers: carrierMap,
      reporter_plans: plans, fixed_plans: fixedPlans, credit_interaction_bn: credit.delta_bn, credit_edits: creditEdits,
      child_native: child.detail, source_candidate: candidateArm, approximations } };
}
module.exports = { S, ARMS, build, CAND, COUNTS, CREDIT, ORIGINAL_RATES, optionRates,
  inactiveParent: (m, side, id, options = {}) => {
    const tags = m.candidate ? Object.assign({}, m.candidate, m.candidate.v3 || {}, m.candidate.v4 || {}) : {};
    return inactiveLine(side, id, Object.assign({}, tags, options));
  } };
if (require.main === module) {
  const started = performance.now(), checks = [], nativeChildGates = [];
  for (const which of ["set", "cash"]) for (const arm of [null, ...Object.keys(ARMS)]) {
    const api = which === "set" ? P : P.CASH, m = api.payloadModel();
    const x = build({ B: P, DETAIL: P.ITEM_DETAIL }, arm, which);
    const bumped = P.Engine.applyCorrections(m, { lines: x.spending_lines, edits: x.edits, meta: m.corrections });
    for (const f of ["private_wtp_bn", "induced_receipts_bn"]) bumped.production[f] = m.production[f].map((v, i) => v + x.production_delta[f][i]);
    for (let ei = 0; ei < 2; ei++) {
      const spec = P.MAIN_SPECS[SPECS[ei]], base = api.evaluateFull(m, spec, P.MAIN_PROFILE);
      const lr = Object.assign({}, spec.line_responses);
      for (const [id, source] of Object.entries(x.meta.union_completion.carriers)) {
        if (source.kind === "line") {
          const row = (source.side === "receipt" ? base.evaluation.receipts : base.evaluation.spending).find(r => r.id === source.parent_line);
          const key = source.side === "receipt" ? m.receipts.reference : row.key;
          lr[id] = key === source.parent_key ? row.response : 0;
        } else lr[id] = x.responses[id][END[ei]];
      }
      const got = api.evaluateFull(bumped, Object.assign({}, spec, { line_responses: lr }), P.MAIN_PROFILE).cost_bn - base.cost_bn;
      const want = x.record.source_delta_bn[ei].estimate;
      if (Math.abs(got - want) > 1e-6) block(`${which}/${arm}/${END[ei]} source gate ${got} != ${want}`);
      checks.push({ which, arm: arm || "central", end: END[ei], got_bn: got, want_bn: want,
        gap_bn: got - want, pass: true });
    }
    const partSums = x.edits.map(() => ({ personal: 0, shared: 0 }));
    for (const p of Object.values(x.parts)) for (const a of ALLOCS) partSums[p.edit][a] += p.by[a];
    if (!x.edits.every((e, i) => ALLOCS.every(a => e.by[a] === partSums[i][a]))) block("parts do not add exactly");
  }
  // Representation regression: an endpoint cost carrier used to charge child
  // services even at service_response=0. Native cells must inherit the actual
  // response at evaluation time, independently of endpoint reconstruction.
  for (const which of ["set", "cash"]) {
    const api = which === "set" ? P : P.CASH, m = api.payloadModel();
    const child = CHILD.build({B:P,DETAIL:P.ITEM_DETAIL},null,which,{},optionRates(P,{},true));
    const bumped = P.Engine.applyCorrections(m,{edits:child.edits,meta:m.corrections});
    const state = P.Engine.defaultState(m); state.allocation="personal";
    state.receipt_scenario=m.receipts.reference; state.service_response=0;
    const before=P.Engine.evaluate(m,state),after=P.Engine.evaluate(bumped,state);
    const serviceIds=m.spending.lines.filter(l=>l.response_class==="service").map(l=>l.id);
    const gap=Math.max(0,...serviceIds.map(id=>Math.abs(after.spending.find(r=>r.id===id).effect_bn-before.spending.find(r=>r.id===id).effect_bn)));
    if(gap!==0)block(`native child service spending survives zero response (${which}, ${gap})`);
    nativeChildGates.push({which,name:"native child service spending is zero when service response is zero",lines:serviceIds.length,max_gap_bn:gap,pass:true});
  }
  const options = [];
  for (const opt of ["arm_a", "arm_c", "c3_minus_se", "c3_plus_se"]) {
    const B = P.caseOf(P.OCT05, P.CANDIDATE, {}, opt);
    for (const which of ["set", "cash"]) {
      const x = build({ B, DETAIL: B.ITEM_DETAIL }, null, which);
      if (!x.edits.every(e => ALLOCS.every(a => Number.isFinite(e.by[a])))) block(`${opt}/${which} non-finite`);
      options.push({ option: opt, which, c3: x.meta.union_completion.c3,
        children_bn: x.detail.child_cost_bn, lineage_population: x.meta.union_completion.counts.lineage_population, pass: true });
    }
  }
  const target = path.join(__dirname, "derived/union_probe_checks.json");
  fs.writeFileSync(target, JSON.stringify({ checks, native_child_gates: nativeChildGates, options, counts: PEOPLE.counts,
    person_key: PEOPLE.key, credit_interaction_bn: CREDIT.results.one_us_parent_plus_observed.delta_bn,
    credit_interaction_se_bn: CREDIT.results.one_us_parent_plus_observed.delta_se_bn }, null, 2) + "\n");
  console.log(JSON.stringify({ source_gates: checks.length, option_gates: options.length,
    elapsed_seconds: (performance.now() - started) / 1000, maxRSS: process.resourceUsage().maxRSS }));
}
