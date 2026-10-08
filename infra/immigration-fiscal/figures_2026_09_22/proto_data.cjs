/* Builds src/generated/proto_<name>.json for the prototypes page (prototypes.html).
 *
 * Each generator proto/<name>.cjs exports build(A), where A is account_sept24.cjs: the September 24
 * case's engine, model, cost() and main-case specs, on which the figures page ran until 2026-10-08.
 * A generator gates its own numbers through A.gate; if any of its gates fail, its file is not written.
 *
 * Run from this directory:
 *   node proto_data.cjs              every prototype
 *   node proto_data.cjs coastline    one prototype
 */
"use strict";
const A = require("./account_sept24.cjs");

const NAMES = ["staircase", "flip", "conventions", "coastline", "dots", "nomogram", "choices", "cube"];
const names = process.argv.length > 2 ? process.argv.slice(2) : NAMES;
let bad = 0;
for (const name of names) {
  if (!NAMES.includes(name)) throw new Error(`unknown prototype ${name}; known: ${NAMES.join(", ")}`);
  console.log(`\n[${name}]`);
  const before = A.failures();
  const data = require(`./proto/${name}.cjs`).build(A);
  if (A.failures() > before) {
    bad += 1;
    console.error(`  ${name}: gates failed; nothing written`);
    continue;
  }
  const file = A.path.join(A.HERE, "src", "generated", `proto_${name}.json`);
  A.fs.writeFileSync(file, JSON.stringify({ generatedBy: `proto/${name}.cjs`, ...data }, null, 1) + "\n");
  console.log(`  wrote src/generated/proto_${name}.json`);
}
if (bad || A.failures()) process.exit(1);
