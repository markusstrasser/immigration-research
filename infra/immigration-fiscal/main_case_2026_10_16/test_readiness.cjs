"use strict";
const assert=require("assert"),fs=require("fs"),os=require("os"),path=require("path"),crypto=require("crypto");
const {requireItem13}=require("./readiness.cjs");
const root=fs.mkdtempSync(path.join(os.tmpdir(),"v9-readiness-")),here=path.join(root,"case");
try{
 fs.mkdirSync(path.join(here,"inputs"),{recursive:true});
 const source="spending_keys_r5_2026_10_15/derived/item13.json",input=path.join(root,source);
 fs.mkdirSync(path.dirname(input),{recursive:true});fs.writeFileSync(input,"source bytes");
 assert.throws(()=>requireItem13({here}),/\[BLOCKED\].*receipt absent/);
 const receipt=path.join(here,"inputs/item13_ready.json");
 const ready={completion_marker:"L1 STEP 3 DONE",item13_source:source,item13_sha256:crypto.createHash("sha256").update("source bytes").digest("hex")};
 fs.writeFileSync(receipt,JSON.stringify({...ready,completion_marker:"L1 STEP 2 DONE"}));
 assert.throws(()=>requireItem13({here}),/\[BLOCKED\].*incomplete/);
 fs.writeFileSync(receipt,JSON.stringify(ready));assert.deepStrictEqual(requireItem13({here}),ready);
 fs.writeFileSync(input,"changed source");assert.throws(()=>requireItem13({here}),/\[BLOCKED\].*stale/);
 // Exercise the actual package and source checker without altering captured files.
 for(const [script,name]of [["package.cjs","item13_ready.json"],["source_check.cjs","item21_ready.json"]]){
  const exists=fs.existsSync;
  try{
   fs.existsSync=p=>String(p)===path.join(__dirname,"inputs",name)?false:exists(p);
   assert.throws(()=>require("./"+script),/\[BLOCKED\].*receipt absent/);
  }finally{fs.existsSync=exists;}
 }
 console.log("PASS readiness: missing, weak, stale, valid; actual package/source checker reject missing custody");
}finally{fs.rmSync(root,{recursive:true,force:true});}
