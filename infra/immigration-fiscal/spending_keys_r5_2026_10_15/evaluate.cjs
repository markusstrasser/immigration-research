/* Evaluate v8 unchanged and each candidate post-engine item at fixed 16/11.
 * No v9 package is built. Output records remain in this item lane. */
'use strict';
const fs=require('fs'),path=require('path');
const crypto=require('crypto');
const P=require('../main_case_2026_10_15/package.cjs');
const I=require('./items.cjs');
const sum=xs=>xs.reduce((a,b)=>a+b,0),mean=xs=>sum(xs)/xs.length;
const fail=s=>{throw Error('[BLOCKED] spending keys evaluation: '+s);};
function evaluate() {
 const baseline={},payloads={},rows=[],population=P.correctionsPayload().meta.population_v8.with_coverage;
 const stored=JSON.parse(fs.readFileSync(path.join(__dirname,'../main_case_2026_10_15/derived/summary.json'),'utf8')).v8;
 for(const which of ['set','cash']){
  const api=which==='cash'?P.CASH:P,runs=I.endpointRuns(api);
  baseline[which]=Object.fromEntries(['low','high'].map(end=>[end,mean(runs[end].map(x=>x.r.cost_bn))]));
  const want=which==='set'?stored.band_bn:stored.cash_set_bn;
  for(const [e,end]of ['low','high'].entries())if(Math.abs(baseline[which][end]-want[e])>1e-9)fail('unchanged v8 differs from stored '+which+'/'+end);
  const required=which==='set'?[365.791930,455.981785]:[281.752564,371.942418];
  for(const [e,end]of ['low','high'].entries())if(Math.abs(baseline[which][end]-required[e])>1e-6)fail('unchanged v8 fails task gate');
  payloads[which]={};
  for(const n of [13,14,15]){
   const item=JSON.parse(fs.readFileSync(path.join(__dirname,'derived',`item${n}.json`),'utf8'));
    const arms=['central',...Object.keys(I.REGISTRY.find(x=>x.number===n).arms).filter(x=>x!=='central_conditional')];
   payloads[which][n]={};
   for(const arm of arms){
    const built=I.buildItem(n,{B:P},arm==='central'?null:arm,which),block=built.meta[I.IDS[n]];
    payloads[which][n][arm]=built;
    for(const end of ['low','high']){
     const change=block.by_end[end].total_bn,before=baseline[which][end],after=before+change;
     const parts=block.by_end[end].parts;
     if(Math.abs(change-sum(parts.map(x=>x.delta_bn)))>1e-9)fail('line parts do not close');
     rows.push({item:n,id:I.IDS[n],arm,which,end,before_bn:before,after_bn:after,change_bn:change,change_per_member_usd:change*1e9/population,status:item.status});
     console.log(`item${n} ${arm} ${which} ${end}: ${before.toFixed(9)} -> ${after.toFixed(9)}; delta ${change.toFixed(9)}`);
    }
   }
  }
 }
 const joint={};
 for(const which of ['set','cash'])joint[which]=Object.fromEntries(['low','high'].map(end=>[end,baseline[which][end]+sum([13,14,15].map(n=>payloads[which][n].central.meta[I.IDS[n]].by_end[end].total_bn))]));
 const sources=['main_case_2026_10_15/package.cjs','main_case_2026_10_15/derived/summary.json','main_case_2026_10_15/derived/corrections.json','main_case_2026_10_15/derived/corrections_cash.json','user_fee_allocation_2026_10_07/derived/fee_lines.json',
  ...['build.py','veterans.py','military_health.py','income_security.py','college.py','items.cjs','item13_generations.cjs','evaluate.cjs','derived/item13.json','derived/item14.json','derived/item15.json'].map(f=>'spending_keys_r5_2026_10_15/'+f),
  ...['generation_corrections_oct15.json','generation_corrections_oct15_cash.json',...['a','b'].flatMap(c=>['G1','G2','G3plus'].map(g=>`model_${c==='b'?'b_':''}${g}.json`))].map(f=>'generation_account_2026_09_24/derived/'+f)];
 const source_hashes=Object.fromEntries(sources.map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(path.join(__dirname,'..',f))).digest('hex')]));
 const medical=payloads.set[13].central.detail.extension.health_bridge;
  const va_medical={status:medical.status,outlay_status:medical.outlay_status,application:'Included as the separate va_medical part of item13',central_national_bn:medical.central_national_bn,arms:medical.arms,sets:{}};
 for(const which of ['set','cash']){
   const block=payloads[which][13].central.meta.veterans_compensation,ends={};
  for(const end of ['low','high']){
    const by_method=Object.fromEntries(Object.entries(block.by_end[end].by_method).map(([method,data])=>[method,sum(data.parts.filter(p=>p.part==='va_medical').map(p=>p.delta_bn))]));
    const by_generation=Object.fromEntries(['a','b'].map(conv=>[conv,block.by_generation[conv][end].by_part.va_medical]));
   const change_bn=mean(Object.values(by_method));
    for(const v of Object.values(by_generation))if(Math.abs(sum(Object.values(v))-change_bn)>1e-9)fail('VA medical generation closure');
   ends[end]={change_bn,change_per_member_usd:change_bn*1e9/population,by_method,by_generation};
  }
   va_medical.sets[which]=ends;
 }
  return {baseline,population,rows,payloads,joint_conditional:joint,source_hashes,va_medical,
  interactions:{item9:'No receipt lines touched; domestic corporate-tax scope fixed.',item10:'Existing lineage/native cells and completion carriers are included once.',item11:'Its post-engine tax/credit/benefit removal remains fixed; these spending-service/veterans lines have no new item11 component. Coverage item11 component also remains fixed.',item12:'Only matching typed coverage line/capital parts repriced; residual/calibration and mixed-unit parts held.',items13_14_15:'Disjoint source lines; additive at fixed specifications. No adoption or fresh endpoint optimization.'},
   limits:['Item13 compensation FY-to-CY composition transport is conditional. Four full-line service extensions and the declared approximate VA medical outlay bridge are included; other unbridged mixed service blocks remain outside central.', 'Item14 is incomplete and explicitly DEGRADED; this is a partial scenario, not an identified complete key.',
  'Item15 proportionally transports an IPEDS FY2023 net-function mix; added-person college capital keys proxy operating use; the exact original union use is preserved.',
  'Item14 transports a union caseload share ratio to added people; their distinct caseload profiles are not re-estimated.',
  'Fixed post-engine items apply only to the frozen 16/11 personal endpoints under the stated accounting rules; do not reuse across arbitrary profiles/options.']};
}
function main(){
 const out=path.join(__dirname,'derived'),result=evaluate();fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,'case_changes.json'),JSON.stringify(result,null,2)+'\n');
 const keys=Object.keys(result.rows[0]),cell=x=>{const s=String(x??'');return /[",\n]/.test(s)?'"'+s.replaceAll('"','""')+'"':s;};
 fs.writeFileSync(path.join(out,'case_changes.csv'),[keys,...result.rows.map(r=>keys.map(k=>r[k]))].map(r=>r.map(cell).join(',')).join('\n')+'\n');
 const generationRows=[];
 for(const which of ['set','cash'])for(const [conv,ends] of Object.entries(result.payloads[which][13].central.meta.veterans_compensation.by_generation))for(const [end,data] of Object.entries(ends))for(const p of data.parts)generationRows.push({which,convention:conv,end,part:p.part,generation:p.generation,population:p.population,line:p.line,source_line:p.source_line,key:p.key||'',before_bn:p.before_bn,after_bn:p.after_bn,change_bn:p.delta_bn});
 const gkeys=Object.keys(generationRows[0]);
 fs.writeFileSync(path.join(out,'item13_by_generation.csv'),[gkeys,...generationRows.map(r=>gkeys.map(k=>r[k]))].map(r=>r.map(cell).join(',')).join('\n')+'\n');
 console.log('PASS unchanged v8, fixed 16/11, both methods, both sets, line-part closure');
}
if(require.main===module)main();
module.exports={evaluate};
