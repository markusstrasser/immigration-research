/* oct14 split: v6's designed R1–R4 split, followed by explicitly declared parts.
 * R5 uses only MAIN_SPECS (personal, numbering retained). Convention-b routing
 * uses dependent ownership and pricing-cell age profiles; approximations travel
 * with the result. Unknown parts or changed pinned inputs fail closed.
 * Job-capital targets are re-keyed on the supplied models (R7), including
 * convention b; its recorded shifts were built on convention a.
 * Module only; no outputs. */
"use strict";
const path = require("path"), fs = require("fs"), crypto = require("crypto");
const V6 = require("./v6_split.cjs");
const AGE = require("./age_routing.cjs");
const { X } = V6;
const { Engine, MODEL, ALLOCS, byAlloc, sum, readJson } = X;
const V7_LANE = "main_case_2026_10_14";
const P7 = require(path.join(__dirname, "..", V7_LANE, "package.cjs"));
const V7_FILES = { set: `${V7_LANE}/derived/corrections.json`, cash: `${V7_LANE}/derived/corrections_cash.json` };
const clone = (x) => JSON.parse(JSON.stringify(x));
const blocked = (why) => { throw new Error(`[BLOCKED] oct14 split: ${why}`); };
const FIXES = ["minors", "credits", "tags", "state_prices"];
const readLocal = p => JSON.parse(fs.readFileSync(path.join(__dirname,p),"utf8"));
const ROUTES = readLocal("inputs/routing.json");
function verifyPins() {
  for (const [rel,sha] of Object.entries(readLocal("inputs/pins.json"))) {
    const got=crypto.createHash("sha256").update(fs.readFileSync(path.join(__dirname,"..",rel))).digest("hex");
    if (got!==sha) blocked(`stale routing source ${rel}`);
  }
}
function routeFor(set,it,name,p,e) {
  const r=ROUTES.sets[set]?.[`${it.id}|${name}`];
  if (!r || r.edit!==p.edit || JSON.stringify(r.by)!==JSON.stringify(p.by)
      || JSON.stringify(r.cell)!==JSON.stringify(Object.fromEntries(Object.entries(e).filter(([k])=>k!=="by")))
      || !["G1","G2","G3plus"].includes(r.generation) || !["union","g3","white"].includes(r.kind)) {
    blocked(`unrouted, unknown or changed part ${it.id}|${name}`);
  }
  return r;
}
const ITEMS = new Set(["personal_allocation", "child_credits", "job_capital_taxes", "white_end_tax_keys", "row4_frame"]);
function loadCase(set) {
  verifyPins();
  const old = V6.loadCase(set), rel = V7_FILES[set];
  if (!rel) blocked(`no ${set} payload`);
  const payload = readJson(rel), api = set === "set" ? P7 : P7.CASH;
  if (JSON.stringify(payload) !== JSON.stringify(api.correctionsPayload())) blocked(`${rel} differs from the case package`);
  for (const key of ["lines", "receipt_lines", "production"]) {
    if (JSON.stringify(payload[key]) !== JSON.stringify(old.payload[key])) blocked(`v7 changed ${key}; no split rule`);
  }
  const n = old.payload.edits.length;
  if (JSON.stringify(payload.edits.slice(0, n)) !== JSON.stringify(old.payload.edits)) blocked("v7 does not start with v6's edits");
  if (JSON.stringify(payload.meta.lineage) !== JSON.stringify(old.payload.meta.lineage)) blocked("v7 changed the lineage block");
  const records = payload.meta.items;
  const inherited=ROUTES.inherited[set];
  if(!inherited || JSON.stringify(inherited.lineage.edits)!==JSON.stringify(old.cells.concat([old.row8]))) blocked("undeclared or changed lineage edit");
  for(const it of old.items) {
    const r=inherited[it.id];
    if(!r || JSON.stringify(r.record)!==JSON.stringify(it.record)) blocked(`undeclared or changed inherited item ${it.id}`);
    const rules=Object.fromEntries(Object.entries(V6.RULES[it.id]).filter(([k])=>!k.endsWith("*")));
    Object.assign(rules,r.rules);
    // Remove the inherited prefix matcher from this consumer's live rule table.
    V6.RULES[it.id]=rules;
  }
  const previous = old.records.length;
  if (JSON.stringify(records.slice(0, previous)) !== JSON.stringify(old.records)) blocked("v7 changed the v6 registry records");
  let at = n;
  const added = [];
  for (const r of records.slice(previous)) {
    if (!ITEMS.has(r.id)) blocked(`item ${r.id} has no authorized split rule`);
    if (r.kind === "allocation") {
      if (r.id !== "personal_allocation" || (r.edits && r.edits.count !== 0)) blocked(`unknown allocation item ${r.id}`);
      continue;
    }
    if (r.kind !== "edit_set" || !r.applied || !r.edits || r.edits.first !== at || !(r.edits.count > 0)) blocked(`invalid edit record ${r.id}`);
    const edits = payload.edits.slice(at, at + r.edits.count);
    added.push({ id: r.id, record: r, first: at, edits, receipt_lines: [] });
    at += r.edits.count;
  }
  if (at !== payload.edits.length) blocked("registry does not cover all v7 edits");
  const names=added.flatMap(it=>Object.keys(it.record.parts).map(name=>`${it.id}|${name}`)).sort();
  if (JSON.stringify(names)!==JSON.stringify(Object.keys(ROUTES.sets[set] || {}).sort())) blocked("declared routes do not cover exactly the case parts");
  for (const it of added) for (const [name,p] of Object.entries(it.record.parts)) routeFor(set,it,name,p,it.edits[p.edit]);
  if (payload.meta.allocation.group_total !== "personal" || api.MAIN_SPECS.length !== 32) blocked("case allocation is not 32 personal specifications");
  return Object.assign({}, old, { rel, payload, api, records, items: old.items.concat(added), added, old });
}
function layer(L, gens, top, models29, union29, opts) {
  opts=opts || {};
  const fixes=new Set(opts.fixes===undefined?FIXES:opts.fixes), conv=opts.convention || "a";
  for (const f of fixes) if (!FIXES.includes(f)) blocked(`unknown routing fix ${f}`);
  if (!["a","b"].includes(conv)) blocked(`unknown convention ${conv}`);
  const lay = V6.layer(L.old, gens, top, models29, union29, {alt:opts.alt || []});
  const parts = clone(lay.parts), record = clone(lay.items);
  const age=AGE.build(L), adjustments=[];
  const credit=fixes.has("credits") || fixes.has("tags") ? readLocal("derived/credit_routing.json") : null;
  const minorScale=opts.minorScale===undefined?1:opts.minorScale;
  if (!(minorScale>=0 && minorScale<=1)) blocked(`invalid minor scale ${minorScale}`);
  const hit=G=> {const hs=gens.filter(g=>top[g]===G); if(hs.length!==1) blocked(`need one declared ${G} cell`); return hs[0];};
  const adjust=(fix,e,values)=> {
    if(ALLOCS.some(a=>Math.abs(sum(gens.map(g=>values[g][a])))>=1e-9)) blocked(`nonconserving ${fix} ${e.line}`);
    for(const g of gens) parts[g].edits.push(Object.assign(clone(e),{by:values[g]}));
    adjustments.push({fix,cell:AGE.id(e),by_generation:clone(values)});
  };
  const move=(fix,e,by)=>adjust(fix,e,Object.fromEntries(gens.map(g=>[g,byAlloc(a=>g===hit("G2")?by[a]:g===hit("G3plus")?-by[a]:0)])));
  if(conv==="b" && fixes.has("minors")) {
    for(const e of L.cells) move("minors",e,byAlloc(a=>age.cells[AGE.id(e)][a].move_minor*minorScale));
    for(const it of lay.items) for(const ed of it.edits) for(const p of ed.parts || []) {
      if(p.rule!=="lineage") continue;
      const e=L.old.items.find(x=>x.id===it.id).edits[ed.edit];
      const share=byAlloc(a=>AGE.partShare(age,e,"g3",a));
      move("minors",e,byAlloc(a=>p.union_bn[a]*share[a]*minorScale));
    }
    for(const k of ["private_wtp_bn","induced_receipts_bn"]) {
      const d=L.dp[k].map(v=>v*age.production_minor_share*minorScale);
      if(!parts[hit("G2")].production) parts[hit("G2")].production=Object.fromEntries(["private_wtp_bn","induced_receipts_bn"].map(x=>[x,L.dp[x].map(()=>0)]));
      parts[hit("G2")].production[k]=parts[hit("G2")].production[k].map((v,i)=>v+d[i]);
      parts[hit("G3plus")].production[k]=parts[hit("G3plus")].production[k].map((v,i)=>v-d[i]);
    }
  }
  const current = Object.fromEntries(gens.map((g) => [g, V6.withStep(models29[g], parts[g].edits, parts[g].receipt_lines)]));
  for (const it of L.added) {
    const rec = { id: it.id, first: it.first, count: it.edits.length, edits: [] };
    for (const g of gens) parts[g].item_receipt_lines[it.id] = [];
    it.edits.forEach((e, j) => {
      if (e.national_bn !== undefined) blocked(`new item ${it.id} has a national-scale edit with no rule`);
      const pieces = Object.entries(it.record.parts || {}).filter(([, p]) => p.edit === j);
      if (!pieces.length) blocked(`item ${it.id} edit ${j} has no parts`);
      if (ALLOCS.some((a) => Math.abs(sum(pieces.map(([, p]) => p.by[a])) - e.by[a]) > 1e-9)) blocked(`item ${it.id} edit ${j} parts do not close`);
      const routed = pieces.map(([name, p]) => {
        const route=routeFor(L.set,it,name,p,e), lineage=route.kind!=="union";
        const G = route.generation, hits = gens.filter((g) => top[g] === G);
        if (hits.length !== 1) blocked(`item ${it.id} part ${name}: ${hits.length} ${G} cells; need an authoritative within-generation split`);
        const g = hits[0];
        let by = clone(p.by);
        if (it.id === "job_capital_taxes" && !lineage) {
          const targets = P7.ITEM_DETAIL.job_capital_taxes[L.set].new_parts[`${e.line}|${e.scenario}`][`union_${G}`];
          const old = models29[g].receipts.lines.find((l) => l.id === e.line).cells[e.scenario];
          by = byAlloc((a) => targets[a] - old[a].target_bn);
        }
        const bn=Object.fromEntries(gens.map(h=>[h,byAlloc(()=>0)]));
        bn[g]=clone(by);
        if(conv==="b" && fixes.has("tags") && it.id==="child_credits" && route.kind==="union") {
          const rows=credit.r6_b_parts.filter(p=>p.part===route.component && p.line===e.line);
          if(rows.length!==1) blocked(`R6 has ${rows.length} owner measurements for ${name}`);
          const measured=rows[0].per_generation_bn, den=sum(Object.values(measured));
          if(!den && ALLOCS.some(a=>by[a]!==0)) blocked(`R6 zero owner denominator ${name}`);
          for(const h of gens) bn[h]=byAlloc(a=>den?by[a]*measured[top[h]]/den:0);
        }
        if(conv==="b" && fixes.has("tags") && lineage && it.id!=="job_capital_taxes") {
          let fraction=byAlloc(a=>AGE.partShare(age,e,route.kind,a));
          if(it.id==="child_credits") {
            // Child-credits source has no age-specific lineage credit measurement.
            // The term is per G3-priced member; use the refundable-key profile.
            fraction=byAlloc(a=>AGE.partShare(age,{side:"spending",line:"refundable_tax_credits",key:"refundable_credits"},"g3",a));
          }
          if(it.id==="row4_frame" && ["part_a_split","benefit_tax"].includes(route.component)) {
            const other=AGE.build(V6.loadCase(L.set==="set"?"cash":"set"));
            const kind=route.kind, cell=AGE.id(e);
            fraction=byAlloc(a=> {
              const x=age.cells[cell][a],y=other.cells[cell][a],keep=route.component==="part_a_split"?1-L.base.meta.pension_accrual.part_a_share:1;
              const den=x[`${kind}_total`]-keep*y[`${kind}_total`],num=x[`${kind}_minor`]-keep*y[`${kind}_minor`];
              return den===0?(num===0?0:blocked(`zero ${route.component} difference`)):num/den;
            });
          }
          const moved=byAlloc(a=>by[a]*fraction[a]*minorScale);
          bn[hit("G2")]=moved; bn[g]=byAlloc(a=>by[a]-moved[a]);
        }
        const share=Object.fromEntries(gens.map(h=>[h,byAlloc(a=>by[a]===0?(h===g?1:0):bn[h][a]/by[a])]));
        return { name, rule: "declared", route, union_bn: by, share, bn };
      });
      if(conv==="b" && fixes.has("tags") && it.id==="row4_frame") {
        const components=[...new Set(routed.filter(p=>p.route.kind==="union").map(p=>p.route.component))];
        const originalModels=Object.fromEntries(gens.map(g=>[g,Engine.applyCorrections(readJson(`generation_account_2026_09_24/derived/model_${top[g]}.json`),
          readJson(`generation_account_2026_09_24/derived/generation_corrections_sept29${L.set==="cash"?"_cash":""}.json`).payloads.a[top[g]])]));
        const cashModels=comp=>comp==="benefit_tax"?Object.fromEntries(["a","b"].map(c=>[c,Object.fromEntries(gens.map(g=>[g,
          Engine.applyCorrections(readJson(`generation_account_2026_09_24/derived/${c==="a"?"model_":"model_b_"}${top[g]}.json`),
            readJson("generation_account_2026_09_24/derived/generation_corrections_sept29_cash.json").payloads[c][top[g]])]))])):null;
        const benefitCash=cashModels(components.includes("benefit_tax")?"benefit_tax":null);
        const charge=(m,comp,g,c)=> {
          if(comp==="oasdi_ratio") return X.V4.oasdiOf(m);
          if(comp==="part_a") return X.V4.hiOf(m);
          const cell=comp==="benefit_tax"?AGE.cells(benefitCash[c][g]).get("spending|social_security|social_security"):AGE.cells(m).get(AGE.id(e));
          if(!cell) blocked(`no ${comp} charge ${AGE.id(e)}`); return byAlloc(a=>cell[a].target_bn);
        };
        for(const comp of components) for(const a of ALLOCS) {
          const ps=routed.filter(p=>p.route.kind==="union" && p.route.component===comp), total=sum(ps.map(p=>p.union_bn[a]));
          const scaled=ps.map(p=> {const g=hit(p.route.generation), old=charge(originalModels[g],comp,g,"a")[a],cur=charge(models29[g],comp,g,"b")[a];
            if(!old && p.union_bn[a]) blocked(`zero ${comp} source charge`); return old?p.union_bn[a]*cur/old:0;});
          const den=sum(scaled); if(!den && total) blocked(`zero ${comp} reroute`);
          ps.forEach((p,i)=> {const v=den?scaled[i]*total/den:0,g=hit(p.route.generation); p.union_bn[a]=v;
            for(const h of gens) p.bn[h][a]=h===g?v:0;});
        }
      }
      if (ALLOCS.some((a) => Math.abs(sum(routed.map((p) => p.union_bn[a])) - e.by[a]) > 1e-9)) {
        blocked(`item ${it.id} edit ${j}: re-keyed generation parts do not add to the case's edit`);
      }
      for (const g of gens) {
        const ed = Object.assign(clone(e), { by: byAlloc((a) => sum(routed.map((p) => p.bn[g][a]))) });
        parts[g].item_edits.push(ed);
        parts[g].edits.push(ed);
        current[g] = V6.withStep(current[g], [ed], []);
      }
      rec.edits.push({ edit: j, side: e.side, line: e.line, key: e.key, scenario: e.scenario, parts: routed });
    });
    record.push(rec);
  }
  if(fixes.has("credits")) {
    const C=credit, methods=Object.keys(C.base);
    for(const side of ["spending","receipt"]) {
      const line=side==="spending"?"refundable_tax_credits":"federal_income_tax";
      const scenarios=side==="spending"?["refundable_credits"]:Object.keys(models29[gens[0]].receipts.lines.find(l=>l.id===line).cells);
      for(const scenario of scenarios) {
        const e={side,line}; e[side==="spending"?"key":"scenario"]=scenario;
        adjust("credits",e,Object.fromEntries(gens.map(g=>[g,byAlloc(a=>a==="shared"?0:sum(methods.map(m=> {
          const v=C.base[m][conv][top[g]][side][line].personal; return side==="spending"?v:v[scenario];
        }))/methods.length)])));
      }
    }
  }
  let state_diagnostics=null;
  if(fixes.has("state_prices")) {
    const S=readLocal("derived/generation_state_indexes.json"), ix=S.conventions[conv], V4=X.V4;
    state_diagnostics={raw_charge_mean:{},conditional_se:{},replicate_adjustments:[]};
    const centered=(functionName,charges)=> {
      const den=sum(gens.map(g=>charges[g])); if(!den) blocked(`zero state charge ${functionName}`);
      const values=Array.from({length:161},(_,r)=> {
        const mean=sum(gens.map(g=>charges[g]*ix[functionName][top[g]].replicates[r]))/den;
        return Object.fromEntries(gens.map(g=>[g,charges[g]*(ix[functionName][top[g]].replicates[r]-mean)]));
      });
      state_diagnostics.raw_charge_mean[functionName]=sum(gens.map(g=>charges[g]*ix[functionName][top[g]].index))/den;
      return values;
    };
    for(const line of V4.SP_LINES) {
      const rows=V4.SP_SPEND.filter(r=>r.line===line), vals=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>0)]));
      const reps=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>Array(161).fill(0))]));
      for(const a of ALLOCS) {
        const charges=Object.fromEntries(gens.map(g=> {
          const l=models29[g].spending.lines.find(l=>l.id===line), key=V4.SP_KEY[line] || l.preferred_key;
          return [g,l.keys[key][a].target_bn/l.national_bn];
        }));
        for(const row of rows) {
          const v=centered(row.function,charges);
          for(const g of gens) for(let r=0;r<161;r++) reps[g][a][r]+=Number(row.sl_amount_bn)*v[r][g];
        }
        for(const g of gens) vals[g][a]=reps[g][a][0];
      }
      adjust("state_prices",{side:"spending",line:V4.SP_SYN[line],key:"k"},vals);
      state_diagnostics.replicate_adjustments.push({edit:{side:"spending",line:V4.SP_SYN[line],key:"k"},by_generation:reps});
      state_diagnostics.conditional_se[V4.SP_SYN[line]]=Object.fromEntries(gens.map(g=>[g,byAlloc(a=>Math.sqrt(4/160*sum(reps[g][a].slice(1).map(v=>(v-reps[g][a][0])**2))))]));
    }
    for(const line of Object.keys(V4.SP_RECEIPT)) for(const scenario of Object.keys(models29[gens[0]].receipts.lines.find(l=>l.id===line).cells)) {
      const info=V4.SP_RECEIPT[line], vals=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>0)]));
      const reps=Object.fromEntries(gens.map(g=>[g,byAlloc(()=>Array(161).fill(0))]));
      for(const a of ALLOCS) {
        const charges=Object.fromEntries(gens.map(g=>[g,models29[g].receipts.lines.find(l=>l.id===line).cells[scenario][a].target_bn/(1+info.factor)]));
        const v=centered(line,charges); for(const g of gens) {
          reps[g][a]=v.map(r=>info.sl_bn/info.national_bn*r[g]); vals[g][a]=reps[g][a][0];
        }
      }
      adjust("state_prices",{side:"receipt",line,scenario},vals);
      state_diagnostics.replicate_adjustments.push({edit:{side:"receipt",line,scenario},by_generation:reps});
    }
  }
  return Object.assign({}, lay, { parts, items: record, routing_adjustments:adjustments, age_routing:age, fixes:[...fixes], convention:conv,state_diagnostics });
}
function evaluator(payload, api) {
  const ev = V6.evaluator(payload, api);
  const specs = ev.specs.filter((s) => s.allocation === payload.meta.allocation.group_total);
  return Object.assign({}, ev, { specs });
}
function adoptedPackage(L) {
  return { source: `${V7_LANE}/package.cjs${L.set === "cash" ? " CASH" : ""}`, specs: L.api.MAIN_SPECS,
    cost: (m, i) => L.api.evaluateFull(m, L.api.MAIN_SPECS[i], L.api.MAIN_PROFILE).cost_bn };
}
function oracle(set) {
  const S = readJson(`${V7_LANE}/derived/summary.json`).v7;
  const rows = X.P.csvRows(`${V7_LANE}/derived/main_case_bands.csv`);
  const variant = set === "set" ? "adopted" : "cash_set";
  const r = rows.find((x) => x.variant === variant && x.profile === P7.MAIN_PROFILE);
  const ends = S.end_specifications.by_method[set];
  if (!r || !ends.length || !ends.every((x) => x[0] === ends[0][0] && x[1] === ends[0][1])) blocked("case band/ends are missing or disagree across methods");
  return { source: `${V7_LANE}/derived/main_case_bands.csv (${variant})`, specs: ends[0],
    band: [Number(r.cost_low_bn), Number(r.cost_high_bn)],
    full: { source: `${V7_LANE}/derived/summary.json v7`, band: set === "set" ? S.band_bn : S.cash_set_bn } };
}
function perSpec(set) {
  if (set !== "set") return null;
  const rows = X.P.csvRows(`${V7_LANE}/derived/per_spec.csv`).filter((r) => r.in_band === "true" || r.in_band === "1");
  const out = new Map();
  for (const i of [...new Set(rows.map((r) => Number(r.spec)))]) {
    const rs = rows.filter((r) => Number(r.spec) === i);
    if (rs.length !== X.METHODS.length || !X.METHODS.every((m) => rs.some((r) => r.method === m))) blocked(`spec ${i}: not one row per method`);
    out.set(i, sum(rs.map((r) => Number(r.cost_bn))) / rs.length);
  }
  return { source: `${V7_LANE}/derived/per_spec.csv cost_bn (in_band)`, cost: out };
}
module.exports = { V7_LANE, V7_FILES, P7, X, loadCase, layer, evaluator, adoptedPackage, oracle, perSpec,
  FIXES, routeFor,
  payloadOf: (p,part)=>clone(V6.payloadOf(p,part)), withStep: V6.withStep, addedAdults: V6.addedAdults,
  ALTERNATIVES: V6.ALTERNATIVES };
