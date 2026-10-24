/* G4 for v10, adapted from main_case_2026_10_16/api_check.cjs: v9 consumer calls still work on v10, raw-engine and
payload-only routes reproduce v10's cost, and the new items' payload records price item 22 without items.cjs.
Writes derived/api_check.json (or --out-dir). Reads derived/ancestry.json from the same directory. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs"), V9 = P.V9_PACKAGE, I = P.ITEMS;
const args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(__dirname, "derived"));
const records = [], sum = (a) => a.reduce((x, y) => x + y, 0);
const near = (a, b, t = 1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a - b) <= t;
process.on("uncaughtExceptionMonitor", (error) => { fs.mkdirSync(OUT, { recursive: true }); fs.writeFileSync(path.join(OUT, "api_check.json"), JSON.stringify({ gate: "G4 v10", pass: false, error: String(error), checks: records.length, records }, null, 1) + "\n"); });
const gate = (name, ok, details = null) => { records.push({ name, pass: !!ok, details }); console.log(`${ok ? "PASS" : "FAIL"} ${name}`); if (!ok) { if (details !== null) console.log(JSON.stringify(details)); throw Error(`[BLOCKED] G4 ${name}`); } };
const rejects = (name, fn, re = /BLOCKED/) => { let stopped = false; try { fn(); } catch (e) { stopped = re.test(String(e)); } gate(`guard ${name}`, stopped); };
function routeGenerations(parts) { const out = { G1: 0, G2: 0, G3plus: 0 }; for (const [g, n] of Object.entries(parts)) { const target = g === "added_G3plus" || g === "added" ? "G3plus" : g; if (!Object.hasOwn(out, target) || !Number.isFinite(n)) throw Error(`[BLOCKED] G4 unmapped generation ${g}`); out[target] += n; } return out; }

for (const key of Object.keys(V9)) gate(`v9 exported name ${key} retained`, key in P);
for (const key of ["modelFor", "payloadModel", "correctionsPayload", "withItems", "withCentral", "specsFor", "responsesFor", "evaluateFull", "viaCandidate", "cost", "bandFor", "band", "evalPackage", "central", "withSyntheticLines", "stateFor", "postFor", "postFor9", "postEngine"]) gate(`callable ${key}`, typeof P[key] === "function");
gate("all three specification collections retained", [P.MAIN_SPECS, P.SHARED_SPECS, P.ALL_SPECS].every((s) => Array.isArray(s) && s.length > 0));
gate("new items off returns the adopted v9 module", P.caseOf(P.OCT05, V9.CANDIDATE) === V9);
const ANC = JSON.parse(fs.readFileSync(path.join(OUT, "ancestry.json"), "utf8"));
gate("ancestry file built on this rate file", ANC.rate_source.sha256 === I.RATE_SOURCE.sha256);
const strip = (m) => ({ ...m, corrections: null });
for (const [which, X] of [["set", P], ["cash", P.CASH]]) {
  const pl = X.correctionsPayload(), pm = X.payloadModel(), raw = P.Engine.applyCorrections(P.MODEL, pl);
  // The engine stores the payload's meta as model.corrections; v10's meta differs from v9's, its edits do not.
  gate(`${which} payload applies with raw engine (all but the stored meta)`, JSON.stringify(strip(raw)) === JSON.stringify(strip(pm)));
  for (const i of [16, 11, 0, 31]) gate(`${which}/${i} raw-applied payload model prices as the case model`, near(X.cost(raw, X.MAIN_SPECS[i]), X.cost(pm, X.MAIN_SPECS[i])));
  gate(`${which} candidate stamp`, pl.meta.adopted === null && /^candidate: /.test(pl.meta.status) && pl.meta.decision === P.DECISION && pl.meta.source === P.LANE + "/package.cjs");
  gate(`${which} full selected registry declared`, JSON.stringify(pl.meta.v10.selected_items) === JSON.stringify(P.CANDIDATE) && JSON.stringify(pl.meta.v9.selected_items) === JSON.stringify(V9.CANDIDATE));
  rejects(`${which} flat-rate reader stops on v10`, () => { const f = pl.meta.one_rate.flat_real_equivalent; if (!Number.isFinite(f)) throw Error("[BLOCKED] consumer: no flat capital rate"); });
  for (const method of P.METHODS) {
    const m = X.modelFor("central", method, X.withCentral({}));
    for (const i of [16, 11, 0, 31]) {
      const s = X.MAIN_SPECS[i], r = X.evaluateFull(m, s), post = X.postFor(m, s), base = X.V9_API.evaluateFull(m, s);
      gate(`${which}/${method}/${i} viaCandidate`, near(r.cost_bn, X.viaCandidate(m, s).cost_bn));
      gate(`${which}/${method}/${i} cost`, r.cost_bn === X.cost(m, s));
      gate(`${which}/${method}/${i} v10 postFor closes`, near(sum(Object.values(post.amounts)), post.total_bn) && near(r.v10_post_engine.total_bn, post.total_bn) && near(sum(post.rows.map((q) => q.delta_bn)), post.total_bn));
      gate(`${which}/${method}/${i} v9 cost plus v10 post route`, near(base.cost_bn + post.total_bn, r.cost_bn));
    }
  }
  for (const i of [16, 11]) {
    const s = X.MAIN_SPECS[i], ev = P.Engine.evaluate(pm, X.stateFor(pm, s)), ref = X.evaluateFull(pm, s);
    gate(`${which}/${i} stateFor carrier responses`, near(ev.welfare_bn, ref.evaluation.welfare_bn));
    gate(`${which}/${i} raw engine plus v9 and v10 declared post amounts closes`, near(-ev.welfare_bn + ref.capital.total_bn + X.V9_BASE.postEngine(s) + X.postFor9(pm, s).total_bn + X.postFor(pm, s).total_bn, ref.cost_bn));
    gate(`${which}/${i} postEngine returns the full canonical post amount`, near(X.postEngine(s), ref.post_engine.total_bn));
  }
  for (const o of [{ allocation: "shared" }, { incomeTax: "row3", tax_key: "cbo_2022" }]) {
    const cp = X.correctionsPayload(o), m = P.Engine.applyCorrections(P.MODEL, cp), b = X.bandFor(m, null, X.specsFor(o)), want = X.central(o);
    gate(`${which} options payload ${JSON.stringify(o)}`, b.every((n, i) => near(n, want[i])), { payload: b, central: want });
  }
  rejects(`${which} payload rate guard retained`, () => X.correctionsPayload({ capital: false }), /moves the specification field rate/);
  // Payload-only consumer: item 22 from post_engine_by_end parts and meta.v10.rates alone.
  const rates = pl.meta.v10.rates;
  for (const id of P.ACTIVE_NEW) {
    const rec = pl.meta.items.find((x) => x.id === id);
    gate(`${which}/${id} post-engine registry route`, !!rec && rec.kind === "post_engine" && rec.edits.count === 0 && !!rec.post_engine_by_end);
    for (const [end, e] of [["low", 0], ["high", 1]]) {
      const z = rec.post_engine_by_end[end];
      gate(`${which}/${id}/${end} method mean`, near(sum(Object.values(z.by_method).map((q) => q.total_bn)) / P.METHODS.length, z.total_bn));
      for (const [method, q] of Object.entries(z.by_method)) {
        gate(`${which}/${id}/${end}/${method} sub-rows close`, near(sum(q.rows.map((x) => x.delta_bn)), q.total_bn));
        if (id === I.IDS[22]) {
          const priced = sum(q.parts.map((x) => x.at_case_rate_bn * (rates.rate_by_level_by_end[rates.level_by_component[x.line]][rates.end_index[end]] / rates.case_rate - 1)));
          gate(`${which}/${end}/${method} payload-only item 22`, near(priced, q.total_bn), { priced, total: q.total_bn });
        }
      }
      const g = ANC.generation_at_ends[which][end][id], routed = routeGenerations({ G1: g.G1, G2: g.G2, G3plus: g.G3plus, added: g.added });
      gate(`${which}/${id}/${end} generation parts close to the payload-model amount`, near(sum(Object.values(routed)), g.total_bn) && near(g.total_bn, z.total_bn, 1e-6), { g: g.total_bn, z: z.total_bn });
    }
  }
  for (const id of ["native_minor_calibration", "coverage_tenure", "health_residual_key"]) {
    const block = pl.meta[id], rec = pl.meta.items.find((r) => r.id === id);
    gate(`${which}/${id} inherited post-engine route`, !!block && !!rec && rec.post_engine_by_end);
    for (const end of ["low", "high"]) { const z = block.by_end[end]; gate(`${which}/${id}/${end} inherited generation parts close`, near(sum(Object.values(routeGenerations(z.by_generation_bn))), z.total_bn)); }
  }
  const pop = pl.meta.population_v9;
  gate(`${which} denominator is v9's (no people added)`, JSON.stringify(pop) === JSON.stringify(V9.correctionsPayload().meta.population_v9));
}
const order = P.NEW_IDS;
for (const [name, fn] of [
  ["v10 items out of order", () => P.caseOf(P.OCT05, V9.CANDIDATE.concat([order[1], order[0]]))],
  ["v10 items before v9 items", () => P.caseOf(P.OCT05, [order[0]].concat(V9.CANDIDATE))],
  ["item 25 without a land lane", () => I.post(V9, V9.evaluateFull(V9.payloadModel(), V9.MAIN_SPECS[16]), V9.MAIN_SPECS[16], new Set([25]), { land: null })],
  ["generation consumer rejects unknown destination", () => routeGenerations({ G4: 1 })],
]) if (!(name === "item 25 without a land lane" && I.LAND)) rejects(name, fn);
const noRate = P.caseOf(P.OCT05, V9.CANDIDATE.concat(I.IDS[23]));
gate("a variant without item 22 keeps item 20's flat rate", Number.isFinite(noRate.correctionsPayload().meta.one_rate.flat_real_equivalent) && noRate.correctionsPayload().meta.v10.rates === null);
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "api_check.json"), JSON.stringify({ gate: "G4 v10", pass: true, verdict: "PASS", checks: records.length, records }, null, 1) + "\n");
console.log(`G4 v10 PASS ${records.length} checks; maxRSS ${process.resourceUsage().maxRSS} KiB`);
