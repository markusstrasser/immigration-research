/* Main case v7 (decisions/2026-10-14-main-case-v7.md, which the parent writes): main case v6 (main_case_2026_10_07,
 * adopted 2026-10-07, consumers key oct07) plus the items the operator adopted from the v6 assumption review
 * (research/immigration-v6-assumption-review-2026-10-14.md, "For the operator" items 1-3) and v6's two measured
 * residuals, which v6 states beside its headline (ladder 298). Consumers key it oct14. It
 * is built as a candidate behind one switch (STATUS): stamped adopted null and status "candidate: ..." until the parent
 * sets STATUS to "adopted", which the package allows only once the decision file exists; adoption changes the stamps and
 * nothing else. The package has v6's API: the same export names, functions and signatures
 * (../main_case_2026_10_07/package.cjs), so a consumer moves from oct07 to oct14 by changing the lane it reads, then
 * routes the new items through meta.items as it routes v6's.
 *
 *   - Item personal_allocation (kind "allocation"): the group total at the personal allocation. v6's band spans 64
 *     specifications per method, both allocations, and its low end (48) is shared. Sharing splits each SPM unit's taxes
 *     and person-level benefits among members and non-members alike, so in mixed units it credits the group with
 *     non-members' taxes, while the headline is the change for all other residents. The case's specifications are v6's
 *     with allocation "personal" (32 per method), numbered as v6 numbers them (0-31), so "16" and "11" keep their names;
 *     SHARED_SPECS (32-63) and ALL_SPECS (all 64) stay available, and specsFor, evalPackage and central take
 *     {allocation: "personal" | "shared" | "all"}. meta.allocation records the rule. Without the item the case is v6's
 *     rule (all 64).
 *   - Item child_credits (edit set, item_child_credits.cjs): the child-related credits that cross the group's boundary in
 *     mixed tax units (mixed_unit_credits_2026_10_14), fixed cell shifts on the union's personal cells, both sets.
 *   - Item job_capital_taxes (edit set with responses, item_job_capital.cjs): the taxes on the business capital that
 *     serves the group's jobs (job_capital_taxes_2026_10_14): four receipt lines re-keyed at every scenario to the
 *     job-capital amount (editsAt: on every model the target becomes that amount, national totals holding) and four
 *     meta.responses entries, which every case specification's line_responses carries.
 *   - Item white_end_tax_keys (edit set, item_row4.cjs): the lineage members priced as third-plus whites with their
 *     income taxes on the case's own keys (white_replacement_2026_09_28's limits_oct07.csv), both sets.
 *   - Item row4_frame (edit set, item_row4.cjs): the five v4 items that summed published CPS weights, on audit row 4's
 *     frame (row4_class_2026_09_29), on the union and the added people; the cash set takes the two that do not touch the
 *     pension switch.
 * The first two edit sets' inputs are the worker lanes' derived/item.json (sources.cjs); items 7 and 8 read committed
 * lane outputs and port the row-4 class lane's construction (row4_oct07.cjs). A stub, which sources.cjs reads only for a lane
 * that names one and has not delivered, sets meta.child_credits.stub or meta.job_capital_taxes.stub true, and
 * main_case.cjs prints [STUB].
 *
 * caseOf(B, ids, sel, lineage) is v6's caseOf with the registry extended: B a v5-style module (v6's OCT05), ids items in
 * registry order (v6's four, then the five above), sel arms, lineage a lineage option (lineage_count.cjs OPTIONS). It
 * builds v6's case for v6's items (V6.caseOf), then the v7 layer on it (caseOn): the edit sets build on that case's
 * models (so a lineage option or an age-mix arm re-prices the added people's job-capital amounts), their edits follow
 * v6's, their meta keys and item 6's responses are added, and the payloads are stamped. With no v7 item the case is
 * v6's, its stamps and API unchanged (generality.cjs runs v6's scripts on it). The case (CANDIDATE, no arm, no option,
 * B = v6's OCT05) is stamped by STATUS; anything else is a variant (adopted null, status "variant: ...").
 *
 * Evaluation. A specification is v6's with item 6's four receipt responses added to its line_responses (after v6's,
 * in meta.responses' order). v6's route reads them (the September 24 stateFor applies every line_responses entry); the
 * item variants' route (candidate v4's evaluateFull at v4's full specification, package.cjs viaCandidate) does not, so
 * evaluateFull and viaCandidate set those rows' responses afterwards: each row's effect, the receipts' class sums, the
 * direct fiscal response and welfare move by (r - r0) x amount (the fiscal weight is 1, checked), and the cost by minus
 * that (the capital return reads none of the four lines). main_case.cjs gates the fix on the case's own options against
 * the engine's route.
 *
 * Run nothing: this is a module. main_case.cjs gates it.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const V6 = require(path.join(__dirname, "..", "main_case_2026_10_07", "package.cjs"));
const CREDITS = require(path.join(__dirname, "item_child_credits.cjs"));
const JOBCAP = require(path.join(__dirname, "item_job_capital.cjs"));
const ROW4 = require(path.join(__dirname, "item_row4.cjs"));
const { Engine, MODEL, METHODS, mean2, span, readJson, sha256, FISCAL } = V6;

const HERE = __dirname;
const LANE = "main_case_2026_10_14";
const CASE_KEY = "oct14";
const DECISION = "decisions/2026-10-14-main-case-v7.md";
const ADOPTED = "2026-10-14";
// The one switch: "candidate" until the parent adopts v7; "adopted" needs the decision file.
const STATUS = "adopted";
const STAMPED = V6.V6.STAMPED.slice();
const DECISION_FILE = path.resolve(FISCAL, "..", "..", DECISION);
const OCT07_LANE = V6.V6.LANE;
const OCT07_FILES = { set: `${OCT07_LANE}/derived/corrections.json`, cash: `${OCT07_LANE}/derived/corrections_cash.json`, summary: `${OCT07_LANE}/derived/summary.json` };
const ALLOCS = ["personal", "shared"];
const ALLOCATIONS = ["personal", "shared", "all"];
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error("[BLOCKED] " + why); };
const isNum = (x) => typeof x === "number" && Number.isFinite(x);
const near = (a, b, tol) => Math.abs(a - b) <= tol;
const nationalsOf = (m) => new Map(m.spending.lines.map((l) => [`spending:${l.id}`, l.national_bn])
  .concat(m.receipts.lines.map((l) => [`receipt:${l.id}`, l.national_bn])));
const lineKey = (e) => `${e.side === "receipt" ? "receipt" : "spending"}:${e.line}`;
if (!["candidate", "adopted"].includes(STATUS)) blocked(`STATUS ${STATUS} is neither candidate nor adopted`);
if (STATUS === "adopted" && !fs.existsSync(DECISION_FILE)) blocked(`STATUS is adopted but ${DECISION} does not exist: the parent writes the decision before adopting`);

// ---------------------------------------------------------------------------------------------------
// Item personal_allocation: the rule and its record.
const ALLOCATION = {
  group_total: "personal",
  rule: "the group total is the change for all other residents, read at the personal allocation: the case's specifications are v6's with allocation personal (0-31 in v6's numbering, 32 per fill-in method), and the band is their minimum and maximum, each method's, averaged",
  reason: "sharing splits each SPM unit's taxes and person-level benefits among its members and non-members alike, so in mixed units it credits the group with non-members' taxes; the headline counts the change for everyone else, which the personal allocation measures (the v6 assumption review, item 1: v6's low end, specification 48, is shared)",
  shared_kept_for: "distribution inside the group and comparisons between groups, where both sides share alike: SHARED_SPECS (32-63), specsFor / central with {allocation: \"shared\"}, the row shared_allocation and summary.json v7.companions.shared_allocation",
  v6_rule: "both allocations, all 64 specifications (ALL_SPECS; {allocation: \"all\"})",
  specifications: { case: "0-31 (personal)", shared: "32-63", numbering: "v6's: index = allocation x 32 + normalization x 16 + share x 8 + school x 4 + reading x 2 + uc, so 16 and 11 keep their names" },
  child_credits: "the term the personal allocation still misses (non-member filers' credits for member children, and the reverse) is item child_credits",
  source: { record: "research/immigration-v6-assumption-review-2026-10-14.md", section: "For the operator, item 1", decision: DECISION },
};
function buildAllocation() {
  return { meta: { allocation: clone(ALLOCATION) }, record: { group_total: "personal", specifications: clone(ALLOCATION.specifications), rule: ALLOCATION.rule } };
}

// ---------------------------------------------------------------------------------------------------
// The registry: v6's items, then v7's, in edit order.
const NEW = [
  { id: "personal_allocation", kind: "allocation",
    label: "the group total at the personal allocation (the case's specifications are v6's personal ones)",
    source: { record: ALLOCATION.source.record, section: ALLOCATION.source.section, decision: DECISION },
    cash: { applies: true, why: "the rule picks the specifications, in both sets" }, arms: {}, build: buildAllocation },
  { id: "child_credits", kind: "edit_set",
    label: "the child-related credits that cross the group's boundary in mixed tax units, at the personal allocation",
    source: { lane: CREDITS.S.lane, file: CREDITS.S.file, stub: CREDITS.S.stub, sha256: CREDITS.S.sha256 },
    cash: { applies: true, why: "credits are paid when claimed: both sets" }, arms: clone(CREDITS.ARMS), build: (ctx, arm, which) => CREDITS.build(ctx, arm, which) },
  { id: "job_capital_taxes", kind: "edit_set",
    label: "the taxes on the business capital that serves the group's jobs: corporate, business property and other production taxes",
    source: { lane: JOBCAP.S.lane, file: JOBCAP.S.file, stub: JOBCAP.S.stub, sha256: JOBCAP.S.sha256 },
    cash: { applies: true, why: "receipts, which both sets price the same way" }, arms: clone(JOBCAP.ARMS), build: (ctx, arm, which) => JOBCAP.build(ctx, arm, which) },
  { id: "white_end_tax_keys", kind: "edit_set",
    label: "the lineage members priced as third-plus whites, with their income taxes on the case's own keys",
    source: { lane: ROW4.SOURCES_7.lane, file: ROW4.SOURCES_7.file, stub: false, sha256: ROW4.SOURCES_7.sha256, ported: ROW4.SOURCES_7.ported },
    cash: { applies: true, why: "the white lane's cash basis: the same rule in both sets" }, arms: {}, build: (ctx, arm, which) => ROW4.buildWhite(ctx, arm, which) },
  { id: "row4_frame", kind: "edit_set",
    label: "the five v4 items that summed published CPS weights, on audit row 4's frame: the owner property key, Part A accrual, the tax on benefits, the state price index and the OASDI ratio",
    source: { lane: ROW4.SOURCES_8.lane, file: ROW4.SOURCES_8.file, stub: false, sha256: ROW4.SOURCES_8.sha256, ported: ROW4.SOURCES_8.ported },
    cash: { applies: true, why: "the owner key and the state index in both sets; Part A, the tax on benefits and the OASDI ratio touch the pension switch and enter the set only" },
    arms: {}, build: (ctx, arm, which) => ROW4.buildRow4(ctx, arm, which) },
];
const NEW_IDS = NEW.map((x) => x.id);
const REGISTRY = V6.REGISTRY.concat(NEW);
const CANDIDATE = V6.CANDIDATE.concat(NEW_IDS);
const V6_IDS = new Set(V6.REGISTRY.map((x) => x.id));

// An edit set's build: v6's edit kinds (cell shifts and national-scale edits) on the case it builds on, its parts adding
// exactly, meta keys new to the payload, and (item 6) receipt responses for lines that have none.
function checkBuilt7(item, x, api, which) {
  const where = `item ${item.id} (${which})`;
  if (!x || !Array.isArray(x.edits) || !x.meta || typeof x.meta !== "object") blocked(`${where}: build() returns no edits and meta`);
  for (const e of x.edits) {
    const shift = e.by !== undefined, scale = e.national_bn !== undefined;
    const fields = Object.keys(e).sort().join(",");
    if (shift === scale || !["receipt", "spending"].includes(e.side) || typeof e.line !== "string") blocked(`${where}: an edit that is not a cell shift or a national-scale edit`);
    if (shift && !(fields === (e.side === "receipt" ? "by,line,scenario,side" : "by,key,line,side") && ALLOCS.every((a) => isNum(e.by[a])) && Object.keys(e.by).length === 2)) {
      blocked(`${where}: a cell shift needs {side, line, ${e.side === "receipt" ? "scenario" : "key"}, by: {personal, shared}}`);
    }
    if (scale && !(fields === "line,national_bn,side" && isNum(e.national_bn))) blocked(`${where}: a national-scale edit needs {side, line, national_bn}`);
  }
  const p0 = api.correctionsPayload(), m = api.payloadModel();
  Engine.applyCorrections(m, { edits: x.edits });
  if (x.editsAt && JSON.stringify(x.editsAt(m)) !== JSON.stringify(x.edits)) blocked(`${where}: editsAt() on the case's payload model is not its edits`);
  for (const k of Object.keys(x.meta)) if (k in p0.meta || V6.RESERVED_META.includes(k)) blocked(`${where} sets meta.${k}, which the payload has or the package stamps`);
  if (x.responses) {
    for (const [id, r] of Object.entries(x.responses)) {
      if (id in p0.meta.responses) blocked(`${where}: meta.responses has ${id} already`);
      if (!(r.receipt === true && r.override === `receipt:${id}` && isNum(r.low) && isNum(r.high) && m.receipts.lines.some((l) => l.id === id))) blocked(`${where}: response ${id} is not {receipt: true, override: "receipt:${id}", low, high} on a receipt line`);
      if (`receipt:${id}` in api.LINE_RESPONSES) blocked(`${where}: the specifications set receipt:${id} already`);
    }
  }
  const sums = x.edits.map(() => ({ personal: 0, shared: 0 }));
  for (const [name, part] of Object.entries(x.parts || {})) {
    const e = x.edits[part.edit];
    if (!e || !e.by || !ALLOCS.every((a) => isNum(part.by[a]))) blocked(`${where}: part ${name} names no cell shift`);
    for (const a of ALLOCS) sums[part.edit][a] += part.by[a];
  }
  if (x.parts && Object.keys(x.parts).length && !x.edits.every((e, k) => !e.by || ALLOCS.every((a) => sums[k][a] === e.by[a]))) blocked(`${where}: its parts do not add to its edits exactly`);
  return Object.assign({ parts: {}, record: {}, detail: {}, responses: null }, x);
}
const headerOf = (item) => ({ id: item.id, label: item.label, kind: item.kind, source: clone(item.source) });

// ---------------------------------------------------------------------------------------------------
// One set's API: the v6-level case's (base), with v7's items after v6's.
function forItems7(base, built, which, stamp, option, alloc) {
  if (!["set", "cash"].includes(which)) blocked(`no set ${which}`);
  if (!ALLOCATIONS.includes(alloc)) blocked(`no allocation rule ${alloc}`);
  const p0 = base.correctionsPayload(), n0 = p0.edits.length;
  const steps = built.filter((b) => b.item.kind === "edit_set" && b[which]).map((b) => ({ id: b.item.id, x: b[which] }));
  const RESP = {};
  for (const s of steps) for (const [id, r] of Object.entries(s.x.responses || {})) {
    if (id in RESP) blocked(`two items set the response of ${id}`);
    RESP[id] = clone(r);
  }
  const RESP_IDS = Object.keys(RESP);
  const EDITS = [], META = {}, RECORDS = [], NAT_AT = [];
  let mAt = base.payloadModel();
  for (const b of built) {
    const head = Object.assign(headerOf(b.item), { arm: b.arm || null, arms: clone(b.item.arms) });
    if (b.item.kind === "allocation") {
      const x = b.item.build();
      for (const [k, v] of Object.entries(x.meta)) META[k] = { by: b.item.id, value: clone(v) };
      RECORDS.push(Object.assign(head, { applied: true, edits: { first: n0 + EDITS.length, count: 0 }, parts: {}, meta_changed: Object.keys(x.meta) }, clone(x.record)));
      continue;
    }
    const x = b[which];
    if (!x) { RECORDS.push(Object.assign(head, { applied: false, why: b.item.cash.why })); continue; }
    for (const [k, v] of Object.entries(x.meta)) {
      if (k in META) blocked(`items ${META[k].by} and ${b.item.id} both set meta.${k}`);
      META[k] = { by: b.item.id, value: clone(v) };
    }
    NAT_AT.push(nationalsOf(mAt));
    const e = x.editsAt ? x.editsAt(mAt) : x.edits;
    if (JSON.stringify(e) !== JSON.stringify(x.edits)) blocked(`item ${b.item.id} (${which}): its edits move with an earlier item's`);
    RECORDS.push(Object.assign(head, { applied: true, edits: { first: n0 + EDITS.length, count: e.length }, parts: clone(x.parts),
      meta_changed: Object.keys(x.meta).concat(x.responses ? ["responses"] : []) }, x.responses ? { responses: Object.keys(x.responses) } : {}, clone(x.record)));
    EDITS.push(...clone(e));
    if (e.length) mAt = Engine.applyCorrections(mAt, { edits: e, meta: mAt.corrections });
  }
  const caseText = (recs) => (recs.some((r) => r.applied)
    ? recs.filter((r) => r.applied).map((r) => `plus item ${r.id}${r.arm ? ` at arm ${r.arm}` : ""} (${r.label})`).join("; ")
    : `no v7 item enters the ${which === "cash" ? "cash set" : "set"}`) + (option ? `; the lineage at option ${option}` : "");
  const applied = (recs) => recs.filter((r) => r.applied).map((r) => r.id);
  const statusOf = (recs) => {
    if (stamp === "variant") return `variant: not adopted; a variant of main case v7 (${STATUS === "adopted" ? `adopted ${ADOPTED}, ${DECISION}` : "the candidate"}): ${caseText(recs)}`;
    if (stamp === "candidate") return `candidate: main case v7, not adopted (${DECISION} not yet written); ${which === "set" ? OCT07_FILES.set : OCT07_FILES.cash} plus items ${applied(recs).join(", ")}, built by ${LANE}/package.cjs`;
    return which === "set"
      ? `adopted ${ADOPTED} (${DECISION}): v6 plus items ${applied(recs).join(", ")}, built by ${LANE}/package.cjs on ${OCT07_FILES.set}`
      : `the cash set of the case adopted ${ADOPTED} (the pension switch off): ${OCT07_FILES.cash} plus items ${applied(recs).join(", ")}, built by ${LANE}/package.cjs`;
  };
  const caseWord = stamp === "adopted" ? `v7, adopted ${ADOPTED}` : stamp === "candidate" ? "v7, the candidate (not adopted)" : `a variant of v7 (${STATUS === "adopted" ? `adopted ${ADOPTED}` : "the candidate"}), not the case`;
  function stamped(p, recs, edits, resp) {
    p.edits = p.edits.concat(clone(edits));
    if (Object.keys(resp).length) p.meta.responses = Object.assign({}, p.meta.responses, clone(resp));
    const items = p.meta.items || [];
    delete p.meta.items;
    for (const [k, v] of Object.entries(META)) p.meta[k] = clone(v.value);
    p.meta.source = `${LANE}/package.cjs`;
    p.meta.adopted = stamp === "adopted" ? ADOPTED : null;
    p.meta.decision = DECISION;
    p.meta.case = `${p.meta.case}; ${caseWord}: ${caseText(recs)}`;
    p.meta.status = statusOf(recs);
    p.meta.items = clone(items).concat(recs);
    return p;
  }
  const payload = stamped(clone(p0), clone(RECORDS), EDITS, RESP);

  // Models: the base's, then the v7 edit sets (editsAt re-keys any model; fixed amounts stop on an option that moves
  // a line they edit, against the case's totals at the item's step).
  function applySteps(m, what) {
    let out = m;
    const all = [];
    steps.forEach((s, k) => {
      if (!s.x.editsAt) {
        const N = nationalsOf(out), moved = [...new Set(s.x.edits.map(lineKey))].filter((key) => N.get(key) !== NAT_AT[k].get(key));
        if (moved.length) blocked(`${what} changes the national total of ${moved.join(", ")}, which item ${s.id} edits by fixed amounts; the item has no rule for it`);
      }
      const e = s.x.editsAt ? s.x.editsAt(out) : s.x.edits;
      all.push(...clone(e));
      if (e.length) out = Engine.applyCorrections(out, { edits: e, meta: out.corrections });
    });
    return { out, all };
  }
  const split = (o) => {
    const rest = Object.assign({}, o || {});
    const a = rest.allocation === undefined ? alloc : rest.allocation;
    delete rest.allocation;
    if (!ALLOCATIONS.includes(a)) blocked(`no allocation ${a} (${ALLOCATIONS.join(", ")})`);
    return { rest, alloc: a };
  };
  function withItems(m, oo) {
    const m6 = base.withItems(m, split(oo).rest);
    if (!steps.length) return m6;
    const { out } = applySteps(m6, "the model");
    if (!("corrections" in m6)) delete out.corrections;
    return out;
  }
  const modelFor = (caseName, method, oo) => {
    const rest = split(oo).rest, m6 = base.modelFor(caseName, method, rest);
    if (!steps.length) return m6;
    const { out } = applySteps(m6, "the model");
    if (!("corrections" in m6)) delete out.corrections;
    return out;
  };
  const withCentral = (o) => { const { rest } = split(o); const oo = base.withCentral(rest); return o && o.allocation !== undefined ? Object.assign(oo, { allocation: o.allocation }) : oo; };
  const payloadModel = () => Engine.applyCorrections(MODEL, payload);
  function correctionsPayload(o) {
    const { rest } = split(o);
    if (!Object.keys(rest).length) return clone(payload);
    const p = base.correctionsPayload(rest);
    const { all } = applySteps(Engine.applyCorrections(MODEL, p), "the option");
    const recs = clone(RECORDS).map((r) => Object.assign(r, r.edits ? { edits: { first: r.edits.first - n0 + p.edits.length, count: r.edits.count } } : {},
      { note: "the item at the case's options (package.cjs forItems7 withItems)" }));
    return stamped(p, recs, all, RESP);
  }
  // Specifications: v6's, at the allocation rule, with the items' receipt responses at the specification's reading.
  const LR7 = Object.fromEntries(RESP_IDS.map((id) => [`receipt:${id}`, clone(RESP[id])]));
  function withResponses(s) {
    if (!RESP_IDS.length) return s;
    s.line_responses = Object.assign({}, s.line_responses, Object.fromEntries(RESP_IDS.map((id) => [`receipt:${id}`, RESP[id][s.reading]])));
    return s;
  }
  function specsFor(o) {
    const { rest, alloc: a } = split(o);
    return base.specsFor(rest).filter((s) => a === "all" || s.allocation === a).map(withResponses);
  }
  function responsesFor(o) { return Object.assign(clone(base.responsesFor(split(o).rest)), clone(RESP)); }
  // The item variants' route reads v4's full specifications, which lack the items' receipt responses: set them after.
  function fixReceipts(r, spec, m0) {
    if (!RESP_IDS.length || !spec || !spec.line_responses) return r;
    let ev = null, d = 0;
    for (const id of RESP_IDS) {
      const want = spec.line_responses[`receipt:${id}`];
      if (want === undefined) continue;
      const src = ev || r.evaluation, k = src.receipts.findIndex((x) => x.id === id);
      if (k < 0) blocked(`the evaluation has no receipt row ${id}`);
      const row = src.receipts[k];
      if (row.response === want) continue;
      if (!ev) {
        const w0 = r.evaluation;
        if (!near(w0.welfare_bn, w0.private_wtp_bn + w0.direct_fiscal_response_bn + w0.induced_receipts_bn, 1e-9 * Math.max(1, Math.abs(w0.welfare_bn)))) {
          blocked("the evaluation's fiscal weight is not 1: the receipt responses cannot be set after it");
        }
        ev = Object.assign({}, w0, { receipts: w0.receipts.slice(), classes: clone(w0.classes) });
      }
      const delta = (want - row.response) * row.amount_bn;
      ev.receipts[k] = Object.assign({}, row, { response: want, effect_bn: want * row.amount_bn });
      ev.classes[row.group].responsive_bn += delta;
      ev.direct_fiscal_response_bn += delta;
      ev.welfare_bn += delta;
      d += delta;
    }
    if (!ev) return r;
    const tp = m0.meta.target_population, rp = m0.meta.resident_population;
    ev.per_target_person = ev.welfare_bn * 1e9 / tp;
    ev.per_other_resident = ev.welfare_bn * 1e9 / (rp - tp);
    return { evaluation: ev, capital: r.capital, cost_bn: r.cost_bn - d, receipts_set_after: RESP_IDS.slice() };
  }
  const evaluateFull = (m0, spec, profile) => fixReceipts(base.evaluateFull(m0, spec, profile), spec, m0);
  const viaCandidate = (m0, spec, profile) => fixReceipts(base.viaCandidate(m0, spec, profile), spec, m0);
  const cost = (m, spec, profile) => evaluateFull(m, spec, profile).cost_bn;
  const bandFor = (m, profile, specs) => span(specs.map((spec) => cost(m, spec, profile)));
  function evalPackage(caseName, method, o) {
    const oo = base.withCentral(split(o).rest);
    return bandFor(modelFor(caseName, method, oo), oo.profile, specsFor(o));
  }
  const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
  const MAIN_SPECS = specsFor({}), SHARED_SPECS = specsFor({ allocation: "shared" }), ALL_SPECS = specsFor({ allocation: "all" });
  const band = (m, profile) => bandFor(m, profile, MAIN_SPECS);
  const LINE_RESPONSES = Object.assign({}, base.LINE_RESPONSES, LR7);
  return Object.assign({}, base, {
    modelFor, payloadModel, correctionsPayload, withItems, withCentral, specsFor, responsesFor, evaluateFull, viaCandidate, cost, bandFor, band,
    evalPackage, central, MAIN_SPECS, SHARED_SPECS, ALL_SPECS, LINE_RESPONSES, RESPONSES: clone(payload.meta.responses), ALLOCATION_RULE: alloc,
    ITEM_EDITS: base.ITEM_EDITS.concat(clone(EDITS)), CASE_ITEMS: (base.CASE_ITEMS || []).concat(clone(RECORDS)), V7_EDITS: clone(EDITS), V7_ITEMS: clone(RECORDS),
    V7_RESPONSES: clone(RESP), V7_BASE_EDITS: n0, fixReceipts,
  });
}

// The v7 layer on a v6-level case Q6 (a set API with CASH, as V6.caseOf returns it): the v7 items ids7 at arms7,
// stamped as stamp ("candidate", "adopted" or "variant"), option the lineage option's name or null.
function caseOn(Q6, ids7, arms7, stamp, option) {
  const items = ids7.map((id) => NEW.find((x) => x.id === id));
  if (items.some((x) => !x)) blocked(`no v7 item ${ids7.join(", ")}`);
  const ctx = { B: Q6, DETAIL: Q6.ITEM_DETAIL || {}, LINEAGE_ITEM: Q6.LINEAGE_ITEM || null, Engine, MODEL, METHODS, readJson, sha256 };
  const built = items.map((item) => {
    const arm = arms7[item.id] || null;
    if (item.kind === "allocation") return { item, arm };
    return { item, arm, set: checkBuilt7(item, item.build(ctx, arm, "set"), Q6, "set"),
      cash: item.cash.applies ? checkBuilt7(item, item.build(ctx, arm, "cash"), Q6.CASH, "cash") : null };
  });
  const alloc = ids7.includes("personal_allocation") ? "personal" : "all";
  const ident = { HERE, LANE, ADOPTED: stamp === "adopted" ? ADOPTED : null, DECISION, STATUS: stamp, STAMPED, CASE_KEY };
  const set = Object.assign(forItems7(Q6, built, "set", stamp, option, alloc), ident);
  const cash = Object.assign(forItems7(Q6.CASH, built, "cash", stamp, option, alloc), { HERE, LANE });
  const detail = Object.assign({}, Q6.ITEM_DETAIL || {}, Object.fromEntries(built.filter((b) => b.set).map((b) => [b.item.id, { set: b.set.detail, cash: b.cash ? b.cash.detail : null }])));
  return Object.assign(set, { CASH: cash, CASH_PAYLOAD: cash.correctionsPayload(), OCT07: Q6, OCT07_CASH: Q6.CASH, OCT07_FILES,
    ITEM_IDS: (Q6.ITEM_IDS || []).concat(ids7), ITEM_ARMS: Object.assign({}, Q6.ITEM_ARMS || {}, arms7), ITEM_DETAIL: detail, V7_IDS: ids7.slice() });
}

// The case: v6's case for v6's items, then v7's layer.
function caseOf(B, ids, sel, lineage) {
  const arms = Object.assign({}, sel || {});
  const order = ids.map((id) => REGISTRY.findIndex((x) => x.id === id));
  if (order.some((k) => k < 0)) blocked(`no item ${ids[order.indexOf(-1)]} in the registry (${REGISTRY.map((x) => x.id).join(", ")})`);
  if (order.some((k, i) => i > 0 && k <= order[i - 1])) blocked("items must be named once each, in registry order");
  for (const [id, arm] of Object.entries(arms)) {
    const it = REGISTRY.find((x) => x.id === id);
    if (!ids.includes(id) || !it || !it.arms[arm]) blocked(`no arm ${arm} of an item ${id} in this case`);
  }
  const ids6 = ids.filter((id) => V6_IDS.has(id)), ids7 = ids.filter((id) => !V6_IDS.has(id));
  const pick = (keep) => Object.fromEntries(Object.entries(arms).filter(([k]) => keep(k)));
  const Q6 = V6.caseOf(B, ids6, pick((k) => V6_IDS.has(k)), lineage);
  if (!ids7.length) return Q6;
  const isCase = B === V6.OCT05 && JSON.stringify(ids) === JSON.stringify(CANDIDATE) && !Object.keys(arms).length && !lineage;
  return caseOn(Q6, ids7, pick((k) => !V6_IDS.has(k)), isCase ? STATUS : "variant", lineage || null);
}

const CASE = caseOf(V6.OCT05, CANDIDATE);
module.exports = Object.assign(CASE, {
  V6: V6.V6, V7: { LANE, CASE_KEY, DECISION, ADOPTED, STATUS, STAMPED, HERE, DECISION_FILE, OCT07_FILES },
  REGISTRY, CANDIDATE, NEW_IDS, SLOTS: V6.SLOTS, PENSION: V6.PENSION, OPEB: V6.OPEB, AGE_MIX: V6.AGE_MIX, FEES: V6.FEES, CREDITS, JOBCAP, ROW4, ALLOCATION,
  RESERVED_META: V6.RESERVED_META, LINEAGE_PAYLOADS: V6.LINEAGE_PAYLOADS, COUNT: V6.COUNT, LINEAGE_OPTIONS: V6.LINEAGE_OPTIONS,
  forItems: V6.forItems, forItems7, caseOf, caseOn, rebase: V6.rebase, checkBuilt: V6.checkBuilt, checkLineage: V6.checkLineage, checkBuilt7,
  V6_PACKAGE: V6,
});
