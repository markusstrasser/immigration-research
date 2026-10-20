"use strict";
const crypto=require("crypto");

function semanticHash(identity){
 return crypto.createHash("sha256").update(JSON.stringify(identity)).digest("hex").slice(0,20);
}

function sourceRecordId(identity,occurrences){
 const hash=semanticHash(identity),occurrence=occurrences.get(hash)||0;
 occurrences.set(hash,occurrence+1);
 return {id:hash+"_"+occurrence,occurrence};
}

module.exports={semanticHash,sourceRecordId};
