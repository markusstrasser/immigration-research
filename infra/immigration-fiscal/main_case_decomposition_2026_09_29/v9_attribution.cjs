/* v9 factor intervention. Universal source-price rules apply to all eight
 * states; group-specific calibration/coverage are explicit post terms.
 * National additions are equal-count average residents, never group prices.
 */
"use strict";
const clone = x => JSON.parse(JSON.stringify(x));
const sum = xs => xs.reduce((a,b) => a+b,0);
const fail = s => { throw Error("[BLOCKED] v9 decomposition: " + s); };
const capitalPart=p=>p.kind==='college_capital'||p.side==='capital'||p.source_side==='capital'
  ||p.economic_class==='capital_return'||Object.hasOwn(p,'capital_stock_delta_bn');
function transportPart(p,f){
  const out={...p};
  for(const key of ['delta_bn','before_bn','after_bn','amount_bn','donor_before_bn','donor_after_bn',
    'capital_stock_before_bn','capital_stock_delta_bn'])if(Number.isFinite(p[key]))out[key]=p[key]*f;
  return out;
}
function build(api, cash, ends, old, caseSummary, gate) {
  const live = cash ? api.CASH : api, base = cash ? api.OCT15.CASH : api.OCT15;
  const meta = live.correctionsPayload().meta;
  const selected = meta.items.filter(x => x.applied && api.NEW_IDS.includes(x.id)).map(x => x.id);
  if (selected.includes("passthrough_source_tax")) fail("central comparator cannot select beside item19");
  const which = cash ? "cash" : "set", actual = {}, raw = {}, changes = {}, records = {};
  const engineDelta = {};
  const mixedMeta=meta.mixed_unit_removal;
  const mixedInput=mixedMeta.source.files.replicates;
  const fs=require('fs'),path=require('path'),crypto=require('crypto');
  const mixedPath=path.resolve(__dirname,'../../..',mixedInput.path);
  if(crypto.createHash('sha256').update(fs.readFileSync(mixedPath)).digest('hex')!==mixedInput.sha256)
    fail('mixed-unit source replicate hash changed');
  const mixedRows=base.csvRows(mixedInput.path.replace(/^infra\/immigration-fiscal\//,''));
  const mixedParts={};
  for(const [end]of ends){
    const [health,aca,snap]=mixedMeta.by_end[end].envelope_arm.split('|');
    const definitions=[['M1_federal','receipts','federal_income_tax'],['M2_state','receipts','state_local_income_tax'],
      ['M3_refunds','spending','refundable_tax_credits'],['M5_owner_property','receipts','modeled_owner_property'],
      ['M5_housing_key','spending','housing_subsidies'],['M5_consumption','receipts','consumption_receipts_composite'],
      ['health_latent_'+health,'spending','medicaid_and_chip_other_medical','diagnostic','low'],
      ['health_latent_'+aca,'spending','medicaid_and_chip_other_medical','diagnostic','low'],
      ['SNAP_latent_'+snap,'spending','snap','diagnostic','low']];
    const components=[];
    for(const [component,side,line,method=which,sourceEnd=end]of definitions){
      const rows=mixedRows.filter(r=>r.component===component&&r.method===method&&r.end===sourceEnd);
      if(rows.length!==3)fail('mixed source generation cells missing: '+component+'/'+method+'/'+sourceEnd);
      components.push({component,side,line,value_bn:sum(rows.map(r=>Number(r.r0)))});
    }
    const total=sum(components.map(r=>r.value_bn));
    const m6=mixedRows.filter(r=>r.component==='M6_biological_children'&&r.method===which&&r.end===end);
    if(m6.length!==3)fail('mixed M6 source generation cells missing '+which+'/'+end);
    const unlocated={M6_biological_children:sum(m6.map(r=>Number(r.r0))),
      D_added_residual:mixedMeta.by_end[end].D_added_residual_bn};
    gate(`mixed ${end}: located categories plus source composite remainders close (1e-9)`,
      Math.abs(total+sum(Object.values(unlocated))-mixedMeta.by_end[end].total_bn)<1e-9);
    mixedParts[end]={components,classified_bn:total,
      unlocated_bn:mixedMeta.by_end[end].total_bn-total,total_bn:mixedMeta.by_end[end].total_bn,
      unlocated_components:unlocated,
      unlocated_rule:'M6 is a federal-income/refund/state-tax composite (round2.py54–58), and D_added transports Df+Dc federal-income/refund composite (removal.py381–390, round2.py71–73); neither identifies a single tax or benefit category. Consumption composite is assigned only to its known consumption-tax category, never split across individual lines.'};
  }
  for (const [end,i] of ends) {
    const spec = live.MAIN_SPECS[i];
    actual[end] = live.evaluateFull(live.payloadModel(),spec);
    raw[end] = base.evaluateFull(base.payloadModel(),base.MAIN_SPECS[i]);
    changes[end] = {...actual[end].v9_post_engine.amounts};
    engineDelta[end] = actual[end].cost_bn - raw[end].cost_bn - actual[end].v9_post_engine.total_bn;
    changes[end].consumption_tax_bases = (changes[end].consumption_tax_bases || 0) + engineDelta[end];
    records[end] = clone(actual[end].v9_post_engine.parts);
    for(const p of records[end].health_residual_key||[])if(capitalPart(p))
      gate(`v9 ${end}: item21 capital uses the selected live Trustees rate (1e-9)`,
        Number.isFinite(p.capital_stock_delta_bn)&&Math.abs(p.delta_bn-p.capital_stock_delta_bn*api.RATE.RATE)<1e-9);
    const pair=caseSummary.v9.interactions.pairs['native_minor_calibration+coverage_tenure']?.[which]?.[end==='low'?0:1]||0;
    changes[end].native16_tenure17_interaction=pair;
    changes[end].coverage_tenure-=pair;
    const rateParts=records[end].one_rate||[];
    records[end].college15_rate20_interaction=rateParts.filter(p=>p.component==='college_capital_interaction');
    records[end].one_rate=rateParts.filter(p=>p.component!=='college_capital_interaction');
    const collegeRate=sum(records[end].college15_rate20_interaction.map(p=>p.delta_bn));
    changes[end].college15_rate20_interaction=collegeRate;
    changes[end].one_rate-=collegeRate;
    gate(`v9 ${end}: every selected item and coverage repricing closes to the live case (1e-9)`,
      Math.abs(sum(Object.values(changes[end])) + raw[end].cost_bn - actual[end].cost_bn) < 1e-9);
  }
  const ids = [...new Set([...Object.keys(changes.low),...Object.keys(changes.high),"calibrated_count_national"])];
  const universalNumbers = [13,15,21].filter(n => api.SPEND.IDS[n] && selected.includes(api.SPEND.IDS[n]));
  const sourcePayload = base.correctionsPayload();
  delete sourcePayload.meta.coverage;
  const sourceApi = {...base, correctionsPayload: () => sourcePayload};
  const source = n => live.V9_BUILT.find(b => b.item.id === api.SPEND.IDS[n]);
  const anchors = {};
  const sourceBaskets = {};
  const stateSources = {};
  function lineRatio(part, full, anchor) {
    if (part.delta_bn===0) return 1;
    if (['capital_reporter','capital_count_interaction','capital_own_coverage_rate_interaction',
      'pension_source','pension_coverage_interaction','pension_count_interaction'].includes(part.component)) return 1;
    if (capitalPart(part) || part.component?.startsWith("capital_")) {
      const id = part.capital_source_line || part.source_line || part.line;
      const a = anchor.capital.components.find(c => c.id === id)?.return_bn;
      const b = full.capital.components.find(c => c.id === id)?.return_bn;
      if (Number.isFinite(a) && a !== 0 && Number.isFinite(b)) return b/a;
      fail('capital part has no state age-key anchor: '+id);
    }
    const id = part.source_line || part.line;
    const a = anchor.evaluation.spending.find(r => r.id === id)?.amount_bn;
    const b = full.evaluation.spending.find(r => r.id === id)?.amount_bn;
    if(Number.isFinite(a)&&a!==0&&Number.isFinite(b))return b/a;
    fail('spending part has no state age-key anchor: '+id);
  }
  function at(plan,st,full,nationalFull,profileData) {
    const end = plan.spec.reading, out = Object.fromEntries(ids.map(id => [id,0]));
    // GGG is independently evaluated by the live canonical package. Other
    // group-profile states retain the existing per-age source-key transport.
    if (!anchors[end]) fail("GGG state anchor must be supplied before state evaluation");
    const anchor = anchors[end], national = st[2] === "N";
    const nationalScale = meta.population_v9.with_coverage / old.base_population;
    const countChange = meta.population_v9.with_coverage - old.population;
    out.calibrated_count_national = national ? countChange / old.base_population * nationalFull.cost_bn : 0;
    const fiscalNational = {};
    const universalRows = [];
    for (const id of ids.filter(id => id !== "calibrated_count_national")) {
      const rows = records[end][id];
      if (universalNumbers.some(n => api.SPEND.IDS[n] === id)) {
        if (national) {
          const n = universalNumbers.find(n => api.SPEND.IDS[n] === id), b = source(n);
          let terms = api.SPEND.deltaParts(n,b.x.detail,sourceApi,full,plan.spec,b.arm)
            .filter(p => p.population !== "coverage");
          if(n===21){
            if(!profileData?.health21)fail('own national item21 profiles are required');
            const h=profileData.health21;
            const ratio=st[0]==='N'?1:h.ratio_at_group_ages;
            const row=full.evaluation.spending.find(r=>r.id==='health_services');
            const fraction=b.x.detail.national_bn.residual/b.x.detail.national_bn.health_services;
            const capital=full.capital.components.find(c=>c.id==='health_sl');
            if(!row||!capital)fail('source21 national health consumption/capital anchor absent');
            const statePrice=full.evaluation.spending.find(r=>r.id==='state_price_health_services');
            if(!statePrice||Math.abs(statePrice.amount_bn)>1e-12)fail('national-use health geographic-price convention changed');
            const cap=capital.return_bn*(api.RATE.RATE/plan.spec.rate);
            terms=[{item:id,line:'health_services',source_line:'health_services',population:'national',side:'spending',
              before_bn:row.amount_bn*fraction,after_bn:row.amount_bn*fraction*ratio,
              delta_bn:row.amount_bn*fraction*(ratio-1),rule:'own normalized national restricted-payer donor age key; no Mexican ethnic ratio'},
              {item:id,line:'state_price_health_services',source_line:'state_price_health_services',population:'national',side:'spending',
                before_bn:0,after_bn:0,delta_bn:0,rule:'inherited factor intervention holds geographic-price corrections at zero under national use'},
              {item:id,line:'health_sl',source_line:'health_sl',population:'national',side:'capital',
                delta_bn:cap*(ratio-1),effective_capital_rate:api.RATE.RATE}];
          }
          if (n === 15) {
            // At national service use, the source's original-group offset is
            // absent. The capital key is the declared operating-use proxy.
            const fee = base.readJson("user_fee_allocation_2026_10_07/derived/fee_lines.json");
            terms = terms.map(p => {
              if(p.kind!=="college_operating"||p.capital_source_line!=="college")return p;
              const use=fee.higher_ed.U_capital-fee.higher_ed.U,amount=use*b.x.detail.national_exposure_bn;
              return {...p,before_bn:p.before_bn+amount,after_bn:p.after_bn+amount*p.response,
                delta_bn:p.delta_bn+amount*(p.response-1),use_share:p.use_share+use};
            });
          }
          out[id] = sum(terms.map(p => p.delta_bn))*nationalScale;
          universalRows.push(...terms.map(p=>({...transportPart(p,nationalScale),item:id})));
          for (const p of terms.filter(p => !capitalPart(p))) {
            const line = p.source_line || p.line;
            fiscalNational[line] = (fiscalNational[line] || 0)+p.delta_bn*nationalScale;
          }
        } else {
          out[id] = rows ? sum(rows.map(p => p.delta_bn*lineRatio(p,full,anchor))) : changes[end][id];
          universalRows.push(...(rows||[]).map(p=>({...transportPart(p,lineRatio(p,full,anchor)),item:id})));
        }
      } else if (id === "one_rate") {
        if (national) {
          const ratio = api.RATE.RATE/plan.spec.rate-1;
          const capital = full.capital.total_bn*ratio;
          out[id] = capital*nationalScale;
        } else out[id] = sum((rows || []).map(p => p.delta_bn*lineRatio(p,full,anchor)));
      } else if(id==='college15_rate20_interaction') {
        if(national){
          const b=source(15),ratio=api.RATE.RATE/plan.spec.rate-1;
          out[id]=b ? sum(api.SPEND.deltaParts(15,b.x.detail,sourceApi,full,plan.spec,b.arm)
            .filter(p=>p.kind==='college_capital').map(p=>p.delta_bn))*ratio*nationalScale : 0;
        }else out[id]=sum((rows||[]).map(p=>p.delta_bn*lineRatio(p,full,anchor)));
      } else {
        const factor = id === "consumption_tax_bases" ? st[1] : st[2];
        out[id] = factor === "G" ? changes[end][id] : 0;
      }
    }
    if (st === "NNN") {
      const total = {receipts_by_line:{},spending_by_line:{}};
      const add = (obj,side,line,value) => {const basket=obj[side+"_by_line"];basket[line]=(basket[line]||0)+value;};
      const source = require("./v8_attribution.cjs").sourceParts(actual[end],meta.union_completion.carriers);
      for(const side of ["receipts","spending"])Object.assign(total[side+"_by_line"],source[side+"_by_line"]);
      const cov = require("./v8_attribution.cjs").coverageParts(meta.coverage.by_end[end]);
      for(const side of ["receipts","spending"])for(const [line,value]of Object.entries(cov[side+"_by_line"]))add(total,side,line,value);
      for(const id of Object.values(api.SPEND.IDS))for(const p of records[end][id]||[])
        if(p.population!=="coverage"&&!capitalPart(p))add(total,"spending",p.source_line||p.line,p.delta_bn);
      for(const id of ["native_minor_calibration","coverage_tenure"])
        for(const p of api.RATE.countParts(meta[id],end))if(p.economic_class==="fiscal_line")
          add(total,p.source_side==="receipt"?"receipts":"spending",p.source_line,p.delta_cost_bn);
      const total_without_mixed=clone(total);
      for(const p of mixedParts[end].components)add(total,p.side,p.line,p.value_bn);
      const shared = {receipts_by_line:{},spending_by_line:{}};
      const own = require("./v8_attribution.cjs").sourceParts(full);
      for(const side of ["receipts","spending"])for(const [line,value]of Object.entries(own[side+"_by_line"]))
        add(shared,side,line,value*nationalScale);
      for(const [line,value]of Object.entries(fiscalNational))add(shared,"spending",line,value);
      sourceBaskets[end]={shared,total,total_without_mixed};
    }
    if(!universalRows.every(p=>!Number.isFinite(p.before_bn)||!Number.isFinite(p.after_bn)
      ||Math.abs(p.after_bn-p.before_bn-p.delta_bn)<1e-9))fail('universal source before/after closure '+end+'/'+st);
    (stateSources[end] ||= {})[st] = {
      base_receipts:full.evaluation.receipts,base_spending:full.evaluation.spending,
      base_capital:full.capital,base_production:{P_bn:full.evaluation.private_wtp_bn,F_bn:full.evaluation.induced_receipts_bn},
      base_population:old.base_population,live_population:meta.population_v9.with_coverage,
      universal_source_rows:universalRows,changes_bn:out,
      national_added_people_scale:nationalScale,
      source_scope:'Base source rows are the measured-profile frame before explicit v8/v9 group-specific additions; at national states scale by live_population/base_population and add universal_source_rows. Group-specific changes are separate and never called national source taxes/budgets.'};
    return out;
  }
  const interaction = caseSummary.v9.interactions;
  const bridge = {selected_items:selected,changes,engine_delta_bn:engineDelta,mixed_source_baskets:mixedParts,
    population:meta.population_v9.with_coverage, population_v9:meta.population_v9,
    interactions:{native16_tenure17:interaction.pairs["native_minor_calibration+coverage_tenure"]?.[which],
      college15_rate20:interaction.pairs["public_college_response+one_rate"]?.[which],
      total:interaction.total[which], higher_order:interaction.higher_order[which]},
    rule:"[ASSUMPTION] Existing factor intervention and source age-key transport retained. Universal13/15/20/21 apply on every national state; equal-count national additions follow those same rules. Group-specific16/17, partial14 and repriced coverage enter on U; household basket18 on R. National college operating use takes its capital-key proxy without the original-group offset. No group-specific origin calibration, PES residual or mixed-unit solve is imposed on average residents. All are recorded separately.",
    labels:{taxes_at_given_ages:"lower taxes at the same ages, including earned pensions and mixed-household effects",
      service_use_at_given_ages:"use of services at given ages, including the added people's excess"}};
  return {ids,at,anchors,bridge,sourceBaskets,stateSources};
}
module.exports={build};
