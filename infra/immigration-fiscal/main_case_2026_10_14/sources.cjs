/* Where main case v7 reads its two new items' inputs: each worker lane's derived/item.json. A lane has delivered when
 * its item.json exists and its RESULT.md verdict is not "pending", "stub" or "in progress". A lane that has not
 * delivered stops its item, unless LANES names a stub file for it, which the item then reads: every gate that reads a
 * stub prints [STUB] (main_case.cjs), and the payloads' meta blocks carry stub: true, so a stub run cannot pass for a
 * result. Both lanes have delivered and name no stub (stub null): if an item.json goes missing or its verdict turns
 * pending, the item stops.
 *
 * sourceOf(name) -> {name, lane, file, stub, verdict, sha256, data}. Run nothing: a module.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const FISCAL = path.join(__dirname, "..");
const LANES = {
  job_capital_taxes: { lane: "job_capital_taxes_2026_10_14", stub: null },
  child_credits: { lane: "mixed_unit_credits_2026_10_14", stub: null },
};
const NOT_DELIVERED = /\b(pending|stub|in progress)\b/i;
const abs = (rel) => path.join(FISCAL, rel);
const sha256 = (rel) => crypto.createHash("sha256").update(fs.readFileSync(abs(rel))).digest("hex");
function verdictOf(rel) {
  if (!fs.existsSync(abs(rel))) return null;
  const m = fs.readFileSync(abs(rel), "utf8").match(/\*\*Verdict:\*\*\s*([^\n]*)/);
  return m ? m[1].trim() : null;
}
const memo = new Map();
function sourceOf(name) {
  if (memo.has(name)) return memo.get(name);
  const L = LANES[name];
  if (!L) throw new Error(`[BLOCKED] sources.cjs: no item ${name}`);
  const item = `${L.lane}/derived/item.json`, result = `${L.lane}/RESULT.md`;
  const verdict = verdictOf(result);
  const delivered = fs.existsSync(abs(item)) && verdict !== null && !NOT_DELIVERED.test(verdict);
  if (!delivered && !L.stub) throw new Error(`[BLOCKED] sources.cjs: ${L.lane} has not delivered (${item} ${fs.existsSync(abs(item)) ? "exists" : "is missing"}; verdict ${verdict === null ? "none" : JSON.stringify(verdict.slice(0, 60))}) and the item keeps no stub`);
  const file = delivered ? item : L.stub;
  if (!fs.existsSync(abs(file))) throw new Error(`[BLOCKED] sources.cjs: ${file} is missing`);
  const out = { name, lane: L.lane, file, stub: !delivered, verdict, result, sha256: sha256(file), data: JSON.parse(fs.readFileSync(abs(file), "utf8")) };
  memo.set(name, out);
  return out;
}
const tag = (S) => (S.stub ? "[STUB] " : "");

module.exports = { sourceOf, tag, LANES };
