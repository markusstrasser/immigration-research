/* Observed nonreporting children as native engine cells and production deltas.
 * Their service prices therefore follow every actual evaluation specification.
 * Raw units come from the unchanged source route's transformed unit models.
 */
"use strict";
const fs = require("fs"), path = require("path");
const FISCAL = path.resolve(__dirname, ".."), SOURCE = "union_completion_2026_10_14";
const COUNTS = JSON.parse(fs.readFileSync(path.join(FISCAL, SOURCE, "derived/count_replicates.json"), "utf8"));
const ALLOCS = ["personal", "shared"];
const sum = xs => xs.reduce((s, x) => s + x, 0);
const block = s => { throw Error(`[BLOCKED] child_records: ${s}`); };
const clone = x => JSON.parse(JSON.stringify(x));
function build(ctx, arm, which, options, rawBundle) {
  const units = rawBundle && rawBundle.unit_models;
  if (!units || units.length !== 17) block("exactly 17 transformed raw unit bands required");
  const c3 = ctx.DETAIL.added_age_mix.counts.c3;
  const ng = COUNTS.observed_g3_rate_by_age.map(r => r[0]);
  const nl = COUNTS.observed_later_by_age.map(r => r[0]);
  const extrapolated = arm === "all_age_extrapolation";
  let gRate = ng, later = nl;
  if (extrapolated) {
    const share = sum(ng)/(sum(ng)+sum(nl)), ratio = COUNTS.loss_ratio[0];
    const count = COUNTS.reporter_central_by_age.map(r => r[0]*ratio);
    gRate = count.map(n => n*share); later = count.map(n => n*(1-share));
  }
  const map = new Map();
  const add = (side, id, key, by) => {
    const k = [side,id,key].join("|");
    if (!map.has(k)) map.set(k, {side,line:id,[side === "receipt" ? "scenario" : "key"]:key,by:{personal:0,shared:0}});
    const e = map.get(k); for (const a of ALLOCS) e.by[a] += by[a];
  };
  let production = null;
  for (let b=0; b<17; b++) for (const [kind,n] of [["g3",later[b]+(1-c3)*gRate[b]],["white",c3*gRate[b]]]) {
    const m = units[b][kind][which];
    if (!production) production = {dims:clone(m.production.dims),private_wtp_bn:m.production.private_wtp_bn.map(()=>0),induced_receipts_bn:m.production.induced_receipts_bn.map(()=>0)};
    if (JSON.stringify(production.dims)!==JSON.stringify(m.production.dims)) block("unit production dimensions disagree");
    for (const side of ["spending","receipt"]) for (const l of m[side === "receipt" ? "receipts" : "spending"].lines) {
      if ((side === "receipt" && l.id === "tenant_occupied_property" && options.property === "none")
        || (side === "spending" && ["roads_vmt_sl","roads_vmt_fed"].includes(l.id) && options.roads === "resources")) continue;
      for (const [key,c] of Object.entries(side === "receipt" ? l.cells : l.keys)) add(side,l.id,key,
        Object.fromEntries(ALLOCS.map(a=>[a,n*c[a].target_bn])));
    }
    for (const f of ["private_wtp_bn","induced_receipts_bn"]) for(let i=0;i<production[f].length;i++) production[f][i]+=n*m.production[f][i];
  }
  // Observed losses exclude the source's imputed fixed G3 credit projection;
  // the exact joint membership-dependent credit edits enter separately.
  const gPeople = sum(later)+(1-c3)*sum(gRate);
  if (!extrapolated) {
    const api = which === "set" ? ctx.B : ctx.B.CASH, p = api.correctionsPayload();
    const rec = p.meta.items.find(i=>i.id === "child_credits");
    const d = ctx.DETAIL.added_age_mix.counts, denominator = d.later+(1-c3)*d.g3_rate;
    if (!rec || !(denominator>0)) block("source G3 credit projection unavailable");
    for(const [name,part] of Object.entries(rec.parts)) if(name.startsWith("lineage_g3plus:")) {
      const e=p.edits[rec.edits.first+part.edit];
      add(e.side,e.line,e.scenario||e.key,Object.fromEntries(ALLOCS.map(a=>[a,-gPeople*part.by[a]/denominator])));
    }
  }
  const edits = [...map.values()].filter(e=>ALLOCS.some(a=>e.by[a]!==0));
  const parts = Object.fromEntries(edits.map((e,i)=>[
    `lineage_g3plus:observed_nonreporters:${e.side}:${e.line}:${e.scenario||e.key}`,{edit:i,by:clone(e.by)}]));
  return {edits,parts,production_delta:production,counts:{g3_priced:gPeople,white_priced:c3*sum(gRate),total:sum(gRate)+sum(later)},
    detail:{method:"native cells and production grid from transformed own-age G3/white source units",c3,
      economic_class_counts:{g3_rate:sum(gRate),later:sum(later)},removed_source_credit_projection:!extrapolated}};
}
module.exports = {build};
