/* Decompose the frozen lineage cells by pricing class and age, without changing
 * any case amount. The g3_rate class includes later descendants: assigning its
 * minors G2 parents is an explicit sensitivity, not an observed parent link.
 * The profile construction follows item_age_mix.cjs, gated on every frozen cell. */
"use strict";
const V6 = require("./v6_split.cjs");
const { Engine, ALLOCS, byAlloc, readJson, sum } = V6.X;
const clone = x => JSON.parse(JSON.stringify(x));
const blocked = why => { throw new Error(`[BLOCKED] age routing: ${why}`); };
const id = c => `${c.side}|${c.line}|${c.scenario || c.key}`;
const cells = m => new Map(m.receipts.lines.flatMap(l => Object.entries(l.cells).map(([scenario, cell]) =>
  [id({side:"receipt",line:l.id,scenario}),cell])).concat(m.spending.lines.flatMap(l => Object.entries(l.keys).map(([key,cell]) =>
  [id({side:"spending",line:l.id,key}),cell]))));
const norm = T => { const n=sum(T); if (!n) blocked("zero normalized profile"); return T.map(x=>x/n); };
const comb = parts => parts[0][1].map((_,b)=>sum(parts.map(([n,T])=>n*norm(T)[b])));
const weighted = (T,rho) => sum(T) === 0 ? 1 : sum(T.map((v,b)=>v*rho[b]))/sum(T);

function build(L) {
  const lin=L.lineage, M=lin.age_mix, counts=lin.counts, C3=lin.c3.value;
  const AK=readJson("added_age_mix_2026_10_07/derived/g3_age_keys.json");
  const BL=readJson("added_age_mix_2026_10_07/derived/band_lines.json");
  const PI=M.mixes.identified, NG=counts.identified_g3plus;
  const loadG=set=>Engine.applyCorrections(readJson("generation_account_2026_09_24/derived/model_G3plus.json"),
    readJson(`generation_account_2026_09_24/derived/generation_corrections_sept29${set==="cash"?"_cash":""}.json`).payloads.a.G3plus);
  const G=cells(loadG(L.set)), GC=cells(loadG("cash"));
  const H=readJson("generation_account_2026_09_24/derived/v4_inputs.json").headcount;
  const adults=V6.addedAdults(lin,H.a.G3plus.adults/H.a.G3plus.population);
  const under=M.bands.map((band,b)=>b<3?1:b===3?1-adults.theta:0);
  const PP=L.base.meta.pension_accrual;
  function profile(e,a) {
    const c=G.get(id(e))[a];
    const rp=line=> { const r=G.get(`receipt|${line}|cbo_collective`)[a]; return [r.target_bn,AK.keys.receipt[a][r.key]]; };
    const payroll=hi=> { const se=rp("self_employment_oasdi_hi"); return [rp(hi?"employee_hi":"employee_oasdi"),
      rp(hi?"employer_hi":"employer_oasdi"),[se[0]*(hi?1-PP.se_oasdi_share:PP.se_oasdi_share),se[1]]]; };
    if (L.set==="set" && e.line==="social_security") return comb(payroll(false));
    if (L.set==="set" && e.line==="medicare") {
      const keep=(1-PP.part_a_share)*GC.get(id(e))[a].target_bn, hi=payroll(true), n=sum(hi.map(p=>p[0]));
      return comb([[keep,AK.keys.spending[a][e.key]],...hi.map(([v,T])=>[(c.target_bn-keep)*v/n,T])]);
    }
    if (L.set==="set" && e.line==="federal_income_tax") {
      const cash=GC.get(id(e))[a].target_bn;
      return comb([[cash,AK.keys.receipt[a][c.key]],[c.target_bn-cash,AK.keys.spending[a].social_security]]);
    }
    return e.side==="spending" && AK.line_keys[e.line] ? AK.line_keys[e.line][a] :
      AK.keys[e.side][a][e.side==="receipt"?c.key:e.key] || blocked(`no ${id(e)} ${a} profile`);
  }
  const basis=L.set==="set"?"accrual":"cash", reading=M.reading;
  const result={}, diagnostics={cell_rebuild_gap_bn:0,white_band_rebuild_gap_bn_per_person:0};
  for (const e of L.cells) {
    const key=id(e), by={};
    for (const a of ALLOCS) {
      const T=profile(e,a), amount=G.get(key)[a].target_bn/NG;
      const gPart=mix=>amount*weighted(T,mix.map((p,b)=>p/PI[b]));
      const gMin=amount*weighted(T,M.mixes.g3_rate.map((p,b)=>p/PI[b]*under[b]));
      const line=`${e.side==="receipt"?"receipts":"spending"}|${e.line}`;
      const w=BL.mixes[`${reading}|g3_rate`].white[basis].lines[line];
      const wBands=PI.map((_,b)=>BL.mixes[`band|${b}`].white[basis].lines[line]);
      const wAll=sum(wBands.map((v,b)=>v*M.mixes.g3_rate[b]));
      const wMinRaw=sum(wBands.map((v,b)=>v*M.mixes.g3_rate[b]*under[b]));
      diagnostics.white_band_rebuild_gap_bn_per_person=Math.max(diagnostics.white_band_rebuild_gap_bn_per_person,Math.abs(wAll-w));
      // A line whose pricing involves ratios need not be linear in unit bands.
      // Normalize its band contribution to the frozen mixed-age amount.
      const wMin=wAll===0 ? (w===0?0:blocked(`nonzero white ${line} with zero band total`)) : w*wMinRaw/wAll;
      const total=counts.later_losses*gPart(M.mixes.later)+(1-C3)*counts.at_g3_rate*gPart(M.mixes.g3_rate)+C3*counts.at_g3_rate*w;
      diagnostics.cell_rebuild_gap_bn=Math.max(diagnostics.cell_rebuild_gap_bn,Math.abs(total-e.by[a]));
      by[a]={g3_minor:(1-C3)*counts.at_g3_rate*gMin,white_minor:C3*counts.at_g3_rate*wMin,
        g3_total:counts.later_losses*gPart(M.mixes.later)+(1-C3)*counts.at_g3_rate*gPart(M.mixes.g3_rate),white_total:C3*counts.at_g3_rate*w,
        move_minor:(1-C3)*counts.at_g3_rate*gMin+C3*counts.at_g3_rate*wMin};
    }
    result[key]=by;
  }
  if (!(diagnostics.cell_rebuild_gap_bn<1e-9)) blocked(`lineage reconstruction ${diagnostics.cell_rebuild_gap_bn} bn`);
  const prodRatio=weighted(AK.production,M.mixes.g3_rate.map((p,b)=>p/PI[b]*under[b]));
  const prodDen=counts.later_losses*weighted(AK.production,M.mixes.later.map((p,b)=>p/PI[b]))+
    (1-C3)*counts.at_g3_rate*weighted(AK.production,M.mixes.g3_rate.map((p,b)=>p/PI[b]));
  const floor=readJson("main_case_lineage_2026_10_05/derived/population.json").arms.floor.added;
  return { cells:result, adults, minor_count:counts.at_g3_rate-adults.by_part.g3_rate,
    floor_fraction:floor/counts.at_g3_rate, production_minor_share:(1-C3)*counts.at_g3_rate*prodRatio/prodDen, diagnostics };
}

function partShare(A,e,kind,a,component) {
  const p=A.cells[id(e)]?.[a] || blocked(`no cell profile ${id(e)} ${a}`);
  const num=kind==="white"?p.white_minor:p.g3_minor, den=kind==="white"?p.white_total:p.g3_total;
  // Difference components need the profile of the difference, not the whole line.
  if (component && ["part_a_split","benefit_tax"].includes(component)) blocked(`difference profile needs both sets: ${component}`);
  return den===0 ? (num===0?0:blocked(`zero denominator ${id(e)}`)) : num/den;
}
module.exports={build,partShare,id,cells,clone};
