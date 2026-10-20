/* Exact full-case native-parent cost gradients; canonical generation files are read-only.
 * node native_parent_gradients_v8.cjs [--out FILE]
 * Fresh execution requires oct15 to be the adopted live case. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto");
const {requireAdopted}=require("../scripts/adoption_gate.cjs");
const {relocatedRecord}=require("../scripts/historical_paths.cjs");
const HERE=__dirname,FISCAL=path.dirname(HERE),ROOT=path.resolve(HERE,"../../..");
const GENS=["G1","G2","G3plus"],KINDS=["g3_rate","later"],ENDS={low:16,high:11};
const clone=x=>JSON.parse(JSON.stringify(x)),sha=f=>crypto.createHash("sha256").update(fs.readFileSync(relocatedRecord(f))).digest("hex");
const blocked=s=>{throw Error(`[BLOCKED] native parent gradients: ${s}`);};
function direction(total,count) {
 if(!Number.isFinite(total)||!Number.isFinite(count)||total<=0||count<0||count>total+1e-9)blocked("invalid source band count");
 if(total-count>=1)return 1;
 if(count>=1)return -1;
 blocked("positive source band has no feasible one-person perturbation");
}
function perturb(counts,kind,band,delta) {
 const out=clone(counts);out[kind][band]+=delta;return out;
}
function slope(base,changed,delta) {
 return Object.fromEntries(GENS.map(g=>[g,(changed[g]-base[g])/delta]));
}
function requireConservation(values,tolerance=1e-9) {
 if(!GENS.every(g=>Number.isFinite(values[g]))||Math.abs(values.G1)>=tolerance
    ||Math.abs(values.G2+values.G3plus)>=tolerance)blocked(`nonconserving derivative ${JSON.stringify(values)}`);
}
function run({out=path.join(HERE,"derived/native_parent_gradients_oct15.json"),adoptionOptions}={}) {
 const adoption=requireAdopted("oct15",adoptionOptions);
 const V8=require("./v8_split.cjs"),{Engine,MODEL}=V8.X;
 const load=rel=>JSON.parse(fs.readFileSync(path.join(HERE,rel),"utf8"));
 const measurement=load("inputs/minor_parent_measurement_oct15.json");
 if(!Number.isFinite(measurement.central_share))blocked("missing measured historical parent policy");
 const minorScale=measurement.central_share,fixes=V8.FIXES,TOP=Object.fromEntries(GENS.map(g=>[g,g]));
 const native=measurement.native_observed_children.by_rate_class;
 const counts=Object.fromEntries(KINDS.map(k=>[k,native[k].by_age_band.map(b=>b.g2_equivalents.estimate)]));
 if(KINDS.some(k=>counts[k].length!==17))blocked("expected 17 source age bands per rate class");
 const gates=[];
 const gate=(name,ok,detail)=>{if(!ok)blocked(`${name}: ${JSON.stringify(detail)}`);gates.push({name,passed:true,detail});};
 const known=new Set([__filename,path.join(FISCAL,"live_case.json"),path.join(HERE,"inputs/minor_parent_measurement_oct15.json"),
   path.join(HERE,"inputs/pins.json"),path.join(HERE,"inputs/routing.json"),path.join(HERE,"derived/generation_state_indexes.json")]);
 for(const rel of Object.keys(load("inputs/pins.json")))known.add(path.join(FISCAL,rel));
 for(const g of GENS)known.add(path.join(HERE,`derived/model_b_${g}.json`));
 for(const suffix of ["","_cash"])for(const rel of [`derived/generation_corrections_sept29${suffix}.json`,
   `../main_case_2026_10_15/derived/corrections${suffix}.json`])known.add(path.resolve(HERE,rel));
 for(const rel of ["../main_case_2026_10_15/derived/summary.json","../main_case_2026_10_15/derived/main_case_bands.csv"])
   known.add(path.resolve(HERE,rel));
 const key=f=>f.startsWith(ROOT+path.sep)?path.relative(ROOT,f):f;
 const hashes=()=>Object.fromEntries([...known].sort().map(f=>[key(f),sha(f)]));
 const before=hashes(),sets={};
 for(const set of ["set","cash"]) {
   const L=V8.loadCase(set),suffix=set==="set"?"":"_cash";
   gate(`${set} final coverage present`,!!L.payload.meta.coverage&&!L.payload.meta.coverage.stub);
   const G29=load(`derived/generation_corrections_sept29${suffix}.json`);
   gate(`${set} original split base equals case base`,G29.meta.union===L.baseRel);
   const models0=Object.fromEntries(GENS.map(g=>[g,load(`derived/model_b_${g}.json`)]));
   const models29=Object.fromEntries(GENS.map(g=>[g,Engine.applyCorrections(models0[g],G29.payloads.b[g])]));
   const union29=Engine.applyCorrections(MODEL,L.base),union=Engine.applyCorrections(MODEL,L.payload);
   const ev=V8.evaluator(L.payload,L.api),unionCosts=ev.specs.map(s=>ev.evaluateFull(union,s).cost_bn);
   gate(`${set} exact personal ends`,unionCosts.indexOf(Math.min(...unionCosts))===16
     &&unionCosts.indexOf(Math.max(...unionCosts))===11);
   function evaluate(overrides) {
     const options={convention:"b",fixes,minorScale};if(overrides)options.nativeG2Counts=overrides;
     const layer=V8.layer(L,GENS,TOP,models29,union29,options);
     const models=Object.fromEntries(GENS.map(g=>[g,Engine.applyCorrections(models0[g],V8.payloadOf(G29.payloads.b[g],layer.parts[g]))]));
     return {cost:Object.fromEntries(Object.entries(ENDS).map(([end,i])=>[end,
       Object.fromEntries(GENS.map(g=>[g,ev.evaluateFull(models[g],ev.specs[i]).cost_bn]))])),
       state_price_rule:layer.added_state_price_routing?.rule||null};
   }
   const base=evaluate();
   for(const [end,i] of Object.entries(ENDS))gate(`${set}/${end} central generations close case`,
     Math.abs(GENS.reduce((n,g)=>n+base.cost[end][g],0)-unionCosts[i])<1e-9);
   // Warmed lazy native source modules enter provenance before any perturbation.
   for(const f of Object.keys(require.cache))if(f.startsWith(ROOT+path.sep))known.add(f);
   const stage=hashes(),gradients=[];
   for(const kind of KINDS)for(let band=0;band<17;band++) {
     const row=native[kind].by_age_band[band],people=row.persons.estimate,n=counts[kind][band];
     if(people===0)continue;
     const delta=direction(people,n),changed=evaluate(perturb(counts,kind,band,delta));
     const doubleAllowed=n+2*delta>=0&&n+2*delta<=people;
     const twice=doubleAllowed?evaluate(perturb(counts,kind,band,2*delta)):null;
     const byEnd={};
     for(const end of Object.keys(ENDS)) {
       const values=slope(base.cost[end],changed.cost[end],delta);requireConservation(values);
       gate(`${set}/${kind}/${band}/${end} opposite G2/G3 and zero G1`,true,values);
       if(twice) {
         const second=slope(base.cost[end],twice.cost[end],2*delta),gap=Math.max(...GENS.map(g=>Math.abs(values[g]-second[g])));
         gate(`${set}/${kind}/${band}/${end} two-person linearity`,gap<1e-9,{max_gap_bn_per_person:gap,tolerance:1e-9});
       }
       byEnd[end]={specification:ENDS[end],bn_per_G2_equivalent_person:values,
                   usd_per_G2_equivalent_person:Object.fromEntries(GENS.map(g=>[g,values[g]*1e9]))};
     }
     gradients.push({rate_class:kind,age_band:band,source_people:people,central_G2_equivalents:n,
                     perturbation_people:delta,two_person_linearity_probe:doubleAllowed,by_end:byEnd});
   }
   gate(`${set} stage source hashes unchanged`,JSON.stringify(stage)===JSON.stringify(hashes()));
   const byRateClass=Object.fromEntries(KINDS.map(k=>[k,{}]));
   for(const row of gradients)byRateClass[row.rate_class][String(row.age_band)]=Object.fromEntries(
     Object.entries(row.by_end).map(([end,value])=>[end,value.bn_per_G2_equivalent_person]));
   sets[set]={specifications:ENDS,central_cost_bn:base.cost,state_price_rule:base.state_price_rule,
              by_rate_class:byRateClass,gradients};
 }
 gate("declared initial inputs unchanged",Object.entries(before).every(([rel,h])=> {
   const f=path.isAbsolute(rel)?rel:path.join(ROOT,rel);return sha(f)===h;
 }));
 const output={contract:"oct15 native parent full-case gradients v1",provenance:"[WORKTREE INPUT] exact final input hashes",
   convention:"b",adoption,historical_minor_share:minorScale,fixes,production_rule:"aumann_shapley",source_sha256:hashes(),sets,gates,
   uncertainty_rule:"For each source band: fixed central total people multiplied by replicate G2-equivalents / replicate persons; these full-case gradients price the resulting parent-fraction variation jointly with the other actual SDR stacks. This tool does not reconstruct SE or use convention-a household unit prices."};
 fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(output,null,1)+"\n");
 console.log(`native parent gradients: ${Object.values(sets).reduce((n,s)=>n+s.gradients.length,0)} band/set rows; ${gates.length} gates; ${out}`);
 return output;
}
if(require.main===module) {
 const args=process.argv.slice(2),options={};
 for(let i=0;i<args.length;i+=2) {
   if(args[i]!=="--out"||!args[i+1])blocked("usage: [--out FILE]");
   options.out=path.resolve(args[i+1]);
 }run(options);
}
module.exports={direction,perturb,slope,requireConservation,run};
