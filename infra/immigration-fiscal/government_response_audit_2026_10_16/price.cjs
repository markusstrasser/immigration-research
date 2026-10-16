/* Audit-only general-public-services response transport on the frozen v9. */
'use strict';
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const args=process.argv.slice(2),arg=(k,d)=>args.includes(k)?args[args.indexOf(k)+1]:d;
const root=fs.realpathSync(path.resolve(arg('--case-root',path.join(__dirname,'../../..'))));
const out=path.resolve(arg('--out-dir',path.join(__dirname,'derived')));
const read=fs.readFileSync,reads=new Set();
fs.readFileSync=function(f,...rest){if(typeof f==='string'&&f.startsWith(root+'/'))reads.add(path.resolve(f));return read.call(this,f,...rest);};
const P=require(path.join(root,'infra/immigration-fiscal/main_case_2026_10_16/package.cjs'));
const C=require(path.join(root,'infra/immigration-fiscal/main_case_2026_10_16/companions.cjs'));
const sum=a=>a.reduce((x,y)=>x+y,0),mean=a=>sum(a)/a.length,near=(a,b)=>Math.abs(a-b)<1e-7;
const checks=[],gate=(name,pass)=>{checks.push({name,pass:!!pass});if(!pass)throw Error('[BLOCKED] government response audit: '+name);};
const selected=new Set(['general_public_services','gps_sl','gps_fed']);
const compText=read(path.join(out,'finance_composition.csv'),'utf8');
const lines=compText.trimEnd().split('\n').map(s=>s.split(',')),head=lines.shift();
gate('finance CSV rectangular',lines.every(r=>r.length===head.length));
const compositions=lines.map(r=>Object.fromEntries(head.map((k,i)=>[k,r[i]])));
const meta=P.correctionsPayload().meta.responses.general_government;
const finite=b=>(1-Math.pow(1-meta.s,b))/meta.s;
const scenarios=[{name:'canonical',responses:[meta.low,meta.high]},
 {name:'zero_cost_bound',responses:[0,0]}, {name:'half_response_check',responses:[.5,.5]},
 {name:'proportional_cost_scenario',responses:[1,1]}];
for(const c of compositions.filter(c=>c.sample==='all50'))scenarios.push({
 name:c.weight+'_'+c.admin_basket,source:c,
 responses:[Number(c.national_minus_federal_share)*finite(Number(c.admin_beta))+Number(c.federal_tax_financial_share)*finite(Number(c.finance_beta)),finite(Number(c.admin_beta))]});
const published=JSON.parse(read(path.join(root,'infra/immigration-fiscal/main_case_2026_10_16/derived/summary.json'),'utf8')).v9;
const expected={set:[368.02973917888073,436.56152715403437],cash:published.cash_set_bn};
const all={},rows=[],details={};
for(const basis of ['set','cash']){
 const X=basis==='cash'?P.CASH:P,models=P.METHODS.map(method=>X.modelFor('central',method,X.withCentral({})));
 const carriers=X.correctionsPayload().meta.union_completion.carriers;
 const allowedSpending=new Set(['general_public_services',...Object.entries(carriers).filter(([,v])=>selected.has(v.parent_line)).map(([id])=>id)]);
 const central=models.map(m=>X.MAIN_SPECS.map(s=>X.evaluateFull(m,s)));
 const run=scenario=>{
  const costs=[],parts=[];
  for(let k=0;k<models.length;k++){
   costs[k]=[];parts[k]=[];
   for(let i=0;i<X.MAIN_SPECS.length;i++){
    const old=X.MAIN_SPECS[i],end=old.reading==='low'?0:1,response=scenario.responses[end];
    const s={...old,gg:response,line_responses:{...old.line_responses}};
    for(const [id,c] of Object.entries(carriers))if(c.kind==='capital'&&selected.has(c.parent_line))s.line_responses[id]*=response/old.gg;
    const before=central[k][i],r=X.evaluateFull(models[k],s);
    const pieces=[];
    for(const p of X.POST_ENGINE.coverage.by_end[s.reading].decomposition.line_parts)if(selected.has(p.source_line))pieces.push({...p,item:'coverage',value_bn:p.coverage_bn});
    for(const id of ['native_minor_calibration','coverage_tenure'])for(const p of C.countParts(X.POST_ENGINE[id],s.reading))if(selected.has(p.source_line))pieces.push({...p,item:id});
    let post=0;const postByItem={};
    for(const p of pieces){const denominator=p.economic_class==='capital_return'?old.gg:Number(p.source_response);
     if(!(denominator>0))throw Error('[BLOCKED] invalid post source response '+p.line);
     const delta=p.value_bn*(response/denominator-1);post+=delta;postByItem[p.item]=(postByItem[p.item]||0)+delta;
    }
    costs[k][i]=r.cost_bn+post;
    parts[k][i]={engine_and_rate_delta_bn:r.cost_bn-before.cost_bn,post_delta_bn:post,post_by_item_bn:postByItem};
    if(scenario.name==='zero_cost_bound'){
     const unchanged=(a,b,allowed,field)=>a.filter(q=>!allowed.has(q.id)).every(q=>near(q[field],b.find(z=>z.id===q.id)[field]));
     gate(`${basis}/${k}/${i} unrelated spending unchanged`,unchanged(before.evaluation.spending,r.evaluation.spending,allowedSpending,'effect_bn'));
     gate(`${basis}/${k}/${i} receipts unchanged`,unchanged(before.evaluation.receipts,r.evaluation.receipts,new Set(),'effect_bn'));
     gate(`${basis}/${k}/${i} other capital unchanged`,unchanged(before.capital.components,r.capital.components,selected,'return_bn'));
     gate(`${basis}/${k}/${i} selected spending and capital zero`,r.evaluation.spending.filter(q=>allowedSpending.has(q.id)).every(q=>near(q.effect_bn,0))&&r.capital.components.filter(q=>selected.has(q.id)).every(q=>near(q.return_bn,0)));
     gate(`${basis}/${k}/${i} other v9 items unchanged`,Object.entries(before.v9_post_engine.amounts).filter(([id])=>id!=='one_rate').every(([id,v])=>near(v,r.v9_post_engine.amounts[id])));
     gate(`${basis}/${k}/${i} production unchanged`,near(before.evaluation.production_gain_bn,r.evaluation.production_gain_bn));
    }
   }
  }
  const ends=costs.map(a=>[a.indexOf(Math.min(...a)),a.indexOf(Math.max(...a))]);
  return {costs,ends,band_bn:[0,1].map(e=>mean(costs.map((a,k)=>a[ends[k][e]]))),parts_at_ends:ends.map((ix,k)=>ix.map(i=>parts[k][i]))};
 };
 all[basis]={};
 for(const sc of scenarios){const r=run(sc);all[basis][sc.name]=r;rows.push({basis,...sc,band_bn:r.band_bn,delta_bn:r.band_bn.map((v,i)=>v-expected[basis][i]),ends:r.ends,parts_at_ends:r.parts_at_ends});}
 const base=all[basis].canonical,zero=all[basis].zero_cost_bound,one=all[basis].proportional_cost_scenario,half=all[basis].half_response_check;
 gate(basis+' frozen v9 baseline',base.band_bn.every((v,i)=>near(v,expected[basis][i])));
 gate(basis+' baseline post is zero',base.parts_at_ends.flat().every(p=>near(p.post_delta_bn,0)));
 gate(basis+' affine each specification',half.costs.every((a,k)=>a.every((v,i)=>near(v,(zero.costs[k][i]+one.costs[k][i])/2))));
 gate(basis+' nonnegative cost slopes',one.costs.every((a,k)=>a.every((v,i)=>v>zero.costs[k][i])));
 const endSlopes=base.ends.map((ix,k)=>ix.map(i=>one.costs[k][i]-zero.costs[k][i]));
 details[basis]={zero_response_band_bn:zero.band_bn,exposure_at_canonical_ends_bn:base.ends.map((ix,k)=>ix.map(i=>base.costs[k][i]-zero.costs[k][i])),mean_response_change_for_5bn_at_fixed_ends:[0,1].map(e=>5/mean(endSlopes.map(a=>a[e])))};
}
for(const f of Object.keys(require.cache))if(f.startsWith(root+'/')&&f!==__filename)reads.add(f);
const sources=[...reads].sort().map(f=>({path:path.relative(root,f),sha256:crypto.createHash('sha256').update(read(f)).digest('hex')}));
fs.mkdirSync(out,{recursive:true});fs.writeFileSync(path.join(out,'fiscal_sensitivity.json'),JSON.stringify({case:'a24d2468ed51d37ae4919fcec55ba153a343a5e1',units:'2024 USD billion per year; conditional fiscal cost',mapping:'Same component-wise power-cost rule and federal-fixed low premise; no causal interpretation of cross-state slopes',general_government:meta,generator_sha256:crypto.createHash('sha256').update(read(__filename)).digest('hex'),finance_composition_sha256:crypto.createHash('sha256').update(compText).digest('hex'),rows,details,checks,sources},null,2)+'\n');
console.log('Government response: '+checks.length+' checks passed; '+rows.length+' scenario rows.');
