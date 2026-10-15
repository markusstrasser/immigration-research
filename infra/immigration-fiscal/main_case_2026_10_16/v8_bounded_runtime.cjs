/* Isolated CommonJS executions of original v8/item_union source bytes. The only
 * environment change bounds item_union's raw-unit-model memo to two entries.
 * Scalar memo entries, source files, original modules and original caches stay intact. */
"use strict";
const fs=require("fs"),path=require("path"),crypto=require("crypto"),vm=require("vm"),Module=require("module");
const ROOT=path.resolve(__dirname,"../main_case_2026_10_15"),ANCHOR="const keyedRatesCache = new Map();",MODULE_ANCHOR="const mod = new Module(file, module); mod.filename = file;";
const sourceRecords=[];
let rawParent=null;
const block=s=>{throw Error(`[BLOCKED] bounded v8 runtime: ${s}`);};
function read(name){const file=path.join(ROOT,name),bytes=fs.readFileSync(file);sourceRecords.push({file:`main_case_2026_10_15/${name}`,sha256:crypto.createHash("sha256").update(bytes).digest("hex")});return {file,source:bytes.toString("utf8")};}
class RawBoundedMap extends Map{
 constructor(...args){super(...args);this.rawOrder=[];}
 get(key){const value=super.get(key);if(value&&Object.hasOwn(value,"unit_models")){this.rawOrder=this.rawOrder.filter(k=>k!==key);this.rawOrder.push(key);}return value;}
 set(key,value){super.set(key,value);if(value&&Object.hasOwn(value,"unit_models")){this.rawOrder=this.rawOrder.filter(k=>k!==key);this.rawOrder.push(key);while(this.rawOrder.length>2){const oldKey=this.rawOrder.shift(),oldValue=super.get(oldKey);if(!rawParent||!oldValue?.unit_models)block("raw memo owner is unavailable");const owners=rawParent.children.filter(c=>c.unitModels===oldValue.unit_models);if(owners.length!==1||owners[0].parent!==rawParent)block("raw capture Module ownership changed");super.delete(oldKey);rawParent.children=rawParent.children.filter(c=>c!==owners[0]);}}return this;}
}
function execute(record,overrides={},map=Map){
 const mod=new Module(record.file,module);mod.filename=record.file;mod.paths=Module._nodeModulePaths(path.dirname(record.file));
 if(record.file===path.join(ROOT,"item_union.cjs"))rawParent=mod;
 const base=Module.createRequire(record.file),req=id=>Object.hasOwn(overrides,id)?overrides[id]:base(id);
 Object.assign(req,{resolve:base.resolve,cache:require.cache,main:require.main,extensions:require.extensions});mod.require=req;
 // compileFunction supplies a lexical Map without adding/replacing any source byte.
 vm.compileFunction(record.source,["exports","require","module","__filename","__dirname","Map"],{filename:record.file})(mod.exports,req,mod,record.file,path.dirname(record.file),map);
 mod.loaded=true;return mod.exports;
}
let paired=null;
function validateAnchor(source){if(source.split(ANCHOR).length!==2)block("keyedRatesCache source anchor must match exactly once");if(/\bnew Map\s*\(/.test(source.slice(0,source.indexOf(ANCHOR))))block("a Map is constructed before the keyedRatesCache anchor");if(source.split(MODULE_ANCHOR).length!==2)block("capture Module source anchor must match exactly once");return true;}
function packageFor(){
 if(paired)return paired;
 const item=read("item_union.cjs");
 validateAnchor(item.source);
 let first=true;
 function ItemMap(...args){if(first){first=false;return new RawBoundedMap(...args);}return new Map(...args);}
 ItemMap.prototype=Map.prototype;
 const union=execute(item,{},ItemMap);if(first)block("keyedRatesCache constructor was not reached");
 paired=execute(read("package.cjs"),{"./item_union.cjs":union});return paired;
}
function metadata(){return {scope:"isolated original source bytes; raw unit_models memo bounded to 2 and exactly matching evicted capture child unlinked from isolated parent.children; active returned values/model references and scalar cache unchanged; original modules/caches untouched",anchor:ANCHOR,module_anchor:MODULE_ANCHOR,anchor_matches:1,raw_cache_entries:2,sources:sourceRecords.map(x=>({...x}))};}
module.exports={packageFor,metadata,validateAnchor};
