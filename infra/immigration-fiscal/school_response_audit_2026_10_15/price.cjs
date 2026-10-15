/* Price only the school-response link on the frozen proposed v9, full account. */
'use strict';
const fs = require('fs'), path = require('path'), crypto = require('crypto');
const args = process.argv.slice(2), arg = (name, fallback) => args.includes(name) ? args[args.indexOf(name)+1] : fallback;
const root = fs.realpathSync(path.resolve(arg('--case-root', path.join(__dirname, '../../..'))));
const out = path.resolve(arg('--out-dir', path.join(__dirname, 'derived')));
const reads = new Set(), originalRead = fs.readFileSync;
fs.readFileSync = function(file, ...rest) {
  if (typeof file === 'string' && file.startsWith(root + '/')) reads.add(path.resolve(file));
  return originalRead.call(this, file, ...rest);
};
const P = require(path.join(root, 'infra/immigration-fiscal/main_case_2026_10_16/package.cjs'));
const C = require(path.join(root, 'infra/immigration-fiscal/main_case_2026_10_16/companions.cjs'));
const S = require(path.join(root, 'infra/immigration-fiscal/main_case_schools_full_2026_09_26/package.cjs'));
const mean = a => a.reduce((x,y)=>x+y,0)/a.length, near=(x,y)=>Math.abs(x-y)<1e-7;
const checks = [], gate = (name, pass) => { checks.push({name,pass:!!pass}); if(!pass) throw Error('[BLOCKED] school audit: '+name); };
const finite = b => (1-Math.pow(1-P.S_PUPIL,b))/P.S_PUPIL;
function run(response, basis, namedRule=null) {
  // Register one ephemeral rule in the exported rule table. This preserves every
  // production caller that derives carrier/line responses from the school rule.
  // No production source or on-disk case artifact is changed.
  S.SCHOOL.audit = [response,response]; S.RULES.audit = 'one-link audit response '+response;
  const X = basis==='cash' ? P.CASH : P;
  const options = {school_rule:namedRule || 'audit'};
  const specs = X.specsFor(options);
  const costs = P.METHODS.map(method => {
    const m = X.modelFor('central',method,X.withCentral(options));
    return specs.map(s => C.adjustedRun(X,m,s,'school').cost_bn);
  });
  const ends = costs.map(a => [a.indexOf(Math.min(...a)),a.indexOf(Math.max(...a))]);
  return {band_bn:[0,1].map(e=>mean(costs.map((a,m)=>a[ends[m][e]]))), ends, costs};
}
const expected={set:[344.02328615247666,412.55507412763035],cash:[260.39059043224427,328.922378407397]};
const published=JSON.parse(fs.readFileSync(path.join(root,'infra/immigration-fiscal/main_case_2026_10_16/derived/summary.json'),'utf8')).v9;
const rows=[], full={}, breakdown={};
const scenarios=[['zero_school_cost_bound',0,null],['half_response_linearity_check',.5,null],
 ['existing_within_district',finite(.836),.836],['existing_0836_as_response',.836,null],
 ['long_difference_085_scenario',finite(.85),.85],['near_proportional_093_scenario',finite(.93),.93],
 ['full_average_cost',1,1],['wage_adjusted_1004_scenario',finite(1.004),1.004]];
for(const basis of ['set','cash']) {
  full[basis]={};
  for(const [name,response,beta] of scenarios) {
    const result=run(response,basis); full[basis][name]=result;
    rows.push({basis,scenario:name,response,assumed_elasticity:beta,band_bn:result.band_bn,
      delta_bn:result.band_bn.map((x,i)=>x-expected[basis][i]),ends:result.ends});
  }
  const baseline=full[basis].full_average_cost;
  gate(basis+' exact proposed v9 baseline',baseline.band_bn.every((v,i)=>near(v,expected[basis][i])));
  const native=run(finite(.836),basis,'within_district');
  gate(basis+' official school companion',native.costs.every((a,m)=>a.every((v,i)=>near(v,full[basis].existing_within_district.costs[m][i]))));
  const wanted=published.companions.school_within_district[basis==='cash'?'cash_set_bn':'band_bn'];
  gate(basis+' stored companion',Array.isArray(wanted)&&native.band_bn.every((v,i)=>near(v,wanted[i])));
  const zero=full[basis].zero_school_cost_bound, half=full[basis].half_response_linearity_check;
  gate(basis+' each specification affine in school response',half.costs.every((a,m)=>a.every((v,i)=>near(v,(zero.costs[m][i]+baseline.costs[m][i])/2))));
  gate(basis+' positive cost even with zero school charge',zero.costs.every(a=>a.every(v=>v>0)));
  const slopes=baseline.costs.map((a,m)=>a.map((v,i)=>v-zero.costs[m][i]));
  gate(basis+' all school cost slopes positive',slopes.every(a=>a.every(v=>v>0)));
  // A mean of minima/maxima of affine specifications is piecewise affine.
  const bandAt=r=>[0,1].map(e=>mean(zero.costs.map((a,m)=>{
    const values=a.map((v,i)=>v+r*slopes[m][i]);return e?Math.max(...values):Math.min(...values);
  })));
  const threshold=target=>[0,1].map(e=>{
    let lo=0,hi=1;for(let i=0;i<60;i++){let mid=(lo+hi)/2;if(bandAt(mid)[e]<target[e])lo=mid;else hi=mid;}return (lo+hi)/2;
  });
  breakdown[basis]={school_zero_band_bn:zero.band_bn,
    response_for_5bn_reduction:threshold(baseline.band_bn.map(v=>v-5)),
    minimum_cost_at_nonnegative_response_bn:zero.band_bn,
    note:'No school-only sign break-even exists for response >=0; this is a model bound, not an observed intervention.'};
}
delete S.SCHOOL.audit; delete S.RULES.audit;
for(const file of Object.keys(require.cache)) if(file.startsWith(root+'/') && file!==__filename)reads.add(file);
const sources=Array.from(reads).sort().filter(f=>fs.existsSync(f)).map(file=>({
  path:path.relative(root,file),sha256:crypto.createHash('sha256').update(originalRead(file)).digest('hex')}));
fs.mkdirSync(out,{recursive:true});
fs.writeFileSync(path.join(out,'fiscal_sensitivity.json'),JSON.stringify({
  case:'proposed v9 at fb822a950085142ac424477297902762b4e446ba',
  generator_sha256:crypto.createHash('sha256').update(originalRead(__filename)).digest('hex'),
  units:'2024 USD billions per year, conditional net fiscal cost to other US residents',
  pupil_share_inherited:P.S_PUPIL,scenario_mapping:'inherited power-cost curve; sensitivity only',
  rows,breakdown,checks,sources},null,2)+'\n');
console.log('School sensitivity: '+checks.length+' checks passed; '+rows.length+' scenarios written.');
