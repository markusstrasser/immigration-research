/* G2: preserve every v8 output contract; values change, existing names do not. */
"use strict";
const fs=require("fs"),path=require("path"),assert=require("assert");
const HERE=__dirname,OLD=path.join(HERE,"../main_case_2026_10_15/derived"),OUT=path.join(HERE,"derived");
const OWN=["api_check.json","contract.json","generality.json","g1.json","coverage_check.json"];
const ROWKEY={"main_case_bands.csv":["profile","variant"],"components.csv":["component"],"per_spec.csv":["method","spec"],"sign_reversal.csv":["measure"]};
const TYPE_CHANGES=Object.fromEntries(["corrections.json","corrections_cash.json"].map(f=>[f,{"meta.adopted":"string -> null: v9 is a candidate; the parent controls adoption"}]));
const csv=text=>text.trimEnd().split("\n").map(l=>{const out=[];let cur="",q=false;for(let i=0;i<l.length;i++){const ch=l[i];if(ch==='"'){if(q&&l[i+1]==='"'){cur+='"';i++;}else q=!q;}else if(ch===","&&!q){out.push(cur);cur="";}else cur+=ch;}if(q)throw Error("[BLOCKED] G2 unclosed CSV quote");out.push(cur);return out;});
const type=x=>Array.isArray(x)?"array":x===null?"null":typeof x;
function paths(x,segs=[],out=new Map()){
 if(Array.isArray(x)){for(const el of x)if(el&&typeof el==="object")paths(el,segs.concat("[]"),out);}
 else if(x&&typeof x==="object")for(const [k,v]of Object.entries(x)){const p=segs.concat(k),id=JSON.stringify(p);if(!out.has(id))out.set(id,[p,type(v)]);paths(v,p,out);}
 return out;
}
const show=s=>s.join(".");
function compareCsv(a,b,file){
 const [ha,...ra]=csv(a),[hb,...rb]=csv(b),key=(h,row)=>(ROWKEY[file]||[h[0]]).map(k=>row[h.indexOf(k)]).join("|");
 const ka=ra.map(r=>key(ha,r)),kb=rb.map(r=>key(hb,r)),missing=ka.filter(k=>!kb.includes(k));
 const common=ka.filter(k=>kb.includes(k)),order=common.every((k,i)=>!i||kb.indexOf(k)>kb.indexOf(common[i-1]));
 const r={columns_same_order:ha.every((c,i)=>hb[i]===c),columns_added:hb.filter(c=>!ha.includes(c)),columns_missing:ha.filter(c=>!hb.includes(c)),rows:{oct15:ka.length,here:kb.length,missing,added:kb.filter(k=>!ka.includes(k)),order_kept:order}};
 r.pass=r.columns_same_order&&!r.columns_missing.length&&!missing.length&&order;return r;
}
function compareJson(a,b,file){
 const pa=paths(a),pb=paths(b),missing=[],changed=[],documented=[];
 for(const [id,[segs,t]]of pa){if(!pb.has(id)){missing.push(show(segs));continue;}const nt=pb.get(id)[1];if(t===nt)continue;const why=TYPE_CHANGES[file]?.[show(segs)];if(why?.startsWith(`${t} -> ${nt}:`))documented.push(`${show(segs)}: ${why}`);else changed.push(`${show(segs)}: ${t} -> ${nt}`);}
 const added=[...pb.values()].filter(([s])=>!pa.has(JSON.stringify(s))).map(([s])=>s),addedIds=new Set(added.map(s=>JSON.stringify(s)));
 const parent=s=>{const p=s.slice(0,-1);while(p.at(-1)==="[]")p.pop();return p;};
 return {pass:!missing.length&&!changed.length,key_paths:{oct15:pa.size,here:pb.size,added:added.length},missing,type_changed:changed,type_changes_documented:documented,relocated:[],added_paths:added.map(show),added_subtrees:added.filter(s=>!addedIds.has(JSON.stringify(parent(s)))).map(show)};
}
// Negative controls establish that this gate rejects destructive contract changes.
const selfChecks=[];
function negative(name,ok){assert(ok,`[BLOCKED] G2 negative probe ${name}`);selfChecks.push({name,pass:true});}
negative("missing CSV row",!compareCsv("component,n\na,1\nb,2\n","component,n\na,1\n","components.csv").pass);
negative("missing CSV column",!compareCsv("component,n\na,1\n","component\na\n","components.csv").pass);
negative("reordered CSV rows",!compareCsv("component,n\na,1\nb,2\n","component,n\nb,2\na,1\n","components.csv").pass);
negative("missing JSON key",!compareJson({a:{b:1}},{a:{}},"x.json").pass);
negative("undocumented JSON type change",!compareJson({a:1},{a:"1"},"x.json").pass);
const want=fs.readdirSync(OLD).filter(f=>!OWN.includes(f)).sort(),have=fs.readdirSync(OUT).sort();
const report={gate:"G2: every v8 file, column, row and key is present; additions and type changes listed",files_missing:want.filter(f=>!have.includes(f)),files_added:have.filter(f=>!want.includes(f)&&!OWN.includes(f)),gate_records:OWN,self_checks:selfChecks,files:{}};
for(const f of want.filter(f=>have.includes(f))){const a=fs.readFileSync(path.join(OLD,f),"utf8"),b=fs.readFileSync(path.join(OUT,f),"utf8");report.files[f]=f.endsWith(".csv")?compareCsv(a,b,f):f.endsWith(".json")?compareJson(JSON.parse(a),JSON.parse(b),f):{pass:true,kind:"presence-only non-tabular file"};}
require("./memory_guard.cjs").requireWithinBudget("G2");
report.pass=!report.files_missing.length&&Object.values(report.files).every(r=>r.pass);
report.verdict=report.pass?"PASS":"FAIL";
fs.writeFileSync(path.join(OUT,"contract.json"),JSON.stringify(report,null,1)+"\n");
for(const [file,r]of Object.entries(report.files))console.log(`${r.pass?"PASS":"FAIL"} ${file}: ${r.rows?`${r.rows.oct15} -> ${r.rows.here} rows`:`${r.key_paths?.oct15} -> ${r.key_paths?.here} key paths`}`);
if(report.files_missing.length)console.log(`FAIL missing files: ${report.files_missing.join(", ")}`);
console.log(`G2 ${report.verdict}: ${want.length} v8 files, ${selfChecks.length} negative probes; maxRSS ${process.resourceUsage().maxRSS} KiB`);
if(!report.pass)process.exitCode=1;
