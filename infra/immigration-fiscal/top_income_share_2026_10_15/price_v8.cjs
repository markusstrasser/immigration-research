// Price pre-stack union-share changes through the case's own stack and evaluator.
// This is a fixed-other-corrections sensitivity, not an adopted v8 replacement.
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const HERE = __dirname, F = path.resolve(HERE, ".."), OUT = path.join(HERE, "derived");
const P = require("../main_case_2026_10_15/package.cjs");
const J = p => JSON.parse(fs.readFileSync(p, "utf8"));
const summary = J(path.join(F, "main_case_2026_10_15/derived/summary.json"));
const federal = J(path.join(OUT, "federal_arms.json"));
const state = J(path.join(OUT, "state_arms.json"));
const gates = [];
function gate(name, pass, detail = "") {
  gates.push({name, pass: Boolean(pass), detail});
  if (!pass) throw Error(`[BLOCKED] ${name}: ${detail}`);
}
const near = (a,b,tol=1e-9) => Number.isFinite(a) && Number.isFinite(b) && Math.abs(a-b)<=tol;
const mean = xs => xs.reduce((a,b)=>a+b,0)/xs.length;
const line = (m,id) => m.receipts.lines.find(l=>l.id===id);
const rows = [], detail = [];
const sets = [["set", P, summary.main_case], ["cash", P.CASH, summary.cash_set.band_bn]];
gate("corrected d1a24d47 v8 reference", summary.main_case.every((v,i)=>near(v,[365.7919302554848,455.9817845889793][i])));
gate("federal current arm has no movement", federal.arms.current.share_change===0);
gate("state current arm has no movement", near(state.arms.current.share_change,0,1e-15));
const armNames = Object.keys(federal.arms);
gate("all substantive federal arms have state counterparts",armNames.every(k=>state.arms[k]||k==="carry_500k_pre_joint_rake"));
for (const [which, api, oracle] of sets) {
  const ends = summary.v8.end_specifications[which][0];
  gate(`${which}: personal ends 16/11`, JSON.stringify(ends)==="[16,11]"
    && ends.every(i=>api.MAIN_SPECS[i].allocation==="personal"));
  const methodResults = [];
  for (const method of P.METHODS) {
    const model = api.modelFor("central",method,api.withCentral({}));
    const baseline = ends.map(i=>api.evaluateFull(model,api.MAIN_SPECS[i]).cost_bn);
    const factors = Object.fromEntries(["federal_income_tax","state_local_income_tax"].map(id=>
      [id,P.stackFactor(P.STACKS[`row4+status_state_aware|central|${method}`],"receipt",id).personal]));
    for (const id of Object.keys(factors)) gate(`${which}/${method}: finite positive ${id} stack`,factors[id]>0&&Number.isFinite(factors[id]));
    const got = {};
    for (const arm of armNames.concat(["current_CA_admin"])) {
      const df = arm==="current_CA_admin"?0:federal.arms[arm].share_change;
      const ds = (arm==="carry_500k_pre_joint_rake"?state.arms.current:state.arms[arm]).share_change;
      const fb = factors.federal_income_tax*line(model,"federal_income_tax").national_bn*df;
      const sb = factors.state_local_income_tax*line(model,"state_local_income_tax").national_bn*ds;
      gate(`${which}/${method}/${arm}: finite moves`,[df,ds,fb,sb].every(Number.isFinite));
      const edited = api.Engine.applyCorrections(model,{lines:[],edits:api.expand([
        {side:"receipt",line:"federal_income_tax",by:{personal:fb,shared:0}},
        {side:"receipt",line:"state_local_income_tax",by:{personal:sb,shared:0}},
      ])});
      for (const id of ["federal_income_tax","state_local_income_tax"])
        gate(`${which}/${method}/${arm}: ${id} national fixed`,line(edited,id).national_bn===line(model,id).national_bn);
      const costs = ends.map(i=>api.evaluateFull(edited,api.MAIN_SPECS[i]).cost_bn);
      gate(`${which}/${method}/${arm}: receipt-cost closure`,costs.every((v,i)=>near(v-baseline[i],-fb-sb)));
      for (const [ei,i] of ends.entries()) {
        const before = api.evaluateFull(model,api.MAIN_SPECS[i]).evaluation;
        const after = api.evaluateFull(edited,api.MAIN_SPECS[i]).evaluation;
        for (const [id,delta] of [["federal_income_tax",fb],["state_local_income_tax",sb]]) {
          const a=after.receipts.find(l=>l.id===id),b=before.receipts.find(l=>l.id===id);
          gate(`${which}/${method}/${arm}/${i}: ${id} evaluated amount`,near(a.amount_bn-b.amount_bn,delta)&&near(a.response,1));
        }
        detail.push({set:which,method,arm,end:["low","high"][ei],spec:i,
          federal_stack_factor:factors.federal_income_tax,state_stack_factor:factors.state_local_income_tax,
          baseline_bn:baseline[ei],federal_receipt_change_bn:fb,state_receipt_change_bn:sb,
          cost_change_bn:costs[ei]-baseline[ei],cost_bn:costs[ei]});
      }
      got[arm]={costs,fb,sb};
    }
    methodResults.push({baseline,arms:got});
  }
  gate(`${which}: method-mean baseline exact`,ends.every((_,e)=>near(mean(methodResults.map(r=>r.baseline[e])),oracle[e])));
  for (const arm of armNames.concat(["current_CA_admin"])) for (let e=0;e<2;e++) {
    const fb=mean(methodResults.map(r=>r.arms[arm].fb)), sb=mean(methodResults.map(r=>r.arms[arm].sb));
    rows.push({arm,set:which,end:["low","high"][e],spec:ends[e],baseline_bn:oracle[e],
      federal_receipt_change_bn:fb,state_receipt_change_bn:sb,federal_cost_change_bn:-fb,
      state_cost_change_bn:-sb,cost_change_bn:-fb-sb,cost_bn:mean(methodResults.map(r=>r.arms[arm].costs[e]))});
  }
}
function csv(records) {
  const keys=Object.keys(records[0]);
  return [keys.join(","),...records.map(r=>keys.map(k=>r[k]).join(","))].join("\n")+"\n";
}
fs.writeFileSync(path.join(OUT,"arms_v8.csv"),csv(rows));
fs.writeFileSync(path.join(OUT,"arms_v8_by_method.csv"),csv(detail));
const paths=["main_case_2026_10_15/package.cjs","main_case_2026_10_15/derived/summary.json",
  "main_case_2026_10_15/derived/corrections.json","main_case_2026_10_15/derived/corrections_cash.json",
  "top_income_share_2026_10_15/derived/federal_arms.json","top_income_share_2026_10_15/derived/state_arms.json"];
const inputs_sha256=Object.fromEntries(paths.map(p=>[p,crypto.createHash("sha256").update(fs.readFileSync(path.join(F,p))).digest("hex")]));
fs.writeFileSync(path.join(OUT,"v8_gates.json"),JSON.stringify({gates,inputs_sha256,
  propagation:"exact case-method stack factors, including row4/status, then additive receipt edits expanded to all incidence rules and evaluated at declared personal ends; set/cash separately",
  held_fixed:federal.held_fixed,
  interpretation:"fixed-other-corrections sensitivity: added/nonreporting people and mixed-unit/coverage post-engine dollars are not re-estimated; national totals unchanged"},null,2)+"\n");
console.log(`PASS ${gates.length} v8 gates; wrote arms tables`);
