/* Explicit record relocation only: recorded hashes continue to verify the same bytes. */
"use strict";
const path=require("path");
const ROOT=path.resolve(__dirname,"../../.."),RELOCATIONS=require("./historical_record_paths.json");
function relocatedRecord(file){
 const relative=path.relative(ROOT,path.resolve(file));
 return Object.hasOwn(RELOCATIONS,relative)?path.join(ROOT,RELOCATIONS[relative]):file;
}
module.exports={relocatedRecord,RELOCATIONS};
