/* G2, the contract: this lane's derived files against v5's (main_case_2026_10_05/derived), so a consumer that reads
 * v5's files reads these by changing the lane.
 *
 * Every v5 file must exist here, except the lanes' gate records (OWN). In each CSV v5's columns must lead in the same
 * order, and every v5 row name must be here, in its order: main_case_bands.csv (profile, variant), components.csv
 * (component), per_spec.csv (method, spec) and sign_reversal.csv (measure). In summary.json and the payloads every v5
 * key path must be here with the same JSON type (an array's elements count as one element, "[]"), except the
 * relocation RELOCATED documents, which must be found at its new path, and the type changes TYPE_CHANGES documents.
 * Every difference is listed: added files, columns, rows and keys, the relocation, the type changes, and anything
 * missing or changed otherwise, which fails the gate.
 *
 * Run from anywhere (after main_case.cjs and sign_reversal.cjs): node contract.cjs -> derived/contract.json
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const OCT05 = path.join(FISCAL, "main_case_2026_10_05", "derived");
const MINE = path.join(HERE, "derived");
// Each lane's own gate records (G1's zero_items, G2, G3, G4): not part of the contract, listed apart from added files.
const OWN = ["api_check.json", "contract.json", "generality.json", "zero_items.json"];
// v5's key paths that move, and where to (summary.json): v5's own change from the September 29 case, by part of the
// lineage line (with the September 29 case's under it), sits under change_at_fixed_specifications.oct05_case; the top
// level holds v6's change from v5, by item.
const RELOCATED = { "summary.json": { from: ["change_at_fixed_specifications"], to: ["change_at_fixed_specifications", "oct05_case"],
  keep: ["total", "note"] } };
// v5's key paths whose JSON type changes, and why. None since the adoption (2026-10-07): the payloads carry the
// adoption date in meta.adopted, a string as in v5's. The candidate carried null there (candidate v4's convention).
const TYPE_CHANGES = {};
const readCsv = (f) => fs.readFileSync(f, "utf8").trim().split("\n").map((l) => {
  const out = []; let cur = "", q = false;
  for (const ch of l) { if (ch === "\"") q = !q; else if (ch === "," && !q) { out.push(cur); cur = ""; } else cur += ch; }
  out.push(cur);
  return out;
});
const typeOf = (x) => (Array.isArray(x) ? "array" : x === null ? "null" : typeof x);
// Key paths as segment lists (keys may hold dots: file names), mapped by their JSON text to [segments, type].
function paths(x, segs, out) {
  if (Array.isArray(x)) {
    for (const el of x) if (el && typeof el === "object") paths(el, segs.concat("[]"), out);
  } else if (x && typeof x === "object") {
    for (const [k, v] of Object.entries(x)) {
      const p = segs.concat(k), id = JSON.stringify(p);
      if (!out.has(id)) out.set(id, [p, typeOf(v)]);
      paths(v, p, out);
    }
  }
  return out;
}
const show = (segs) => segs.join(".");

const report = { gate: "G2: every v5 derived file exists here with its columns, rows and keys; every difference listed", files: {} };
let fail = 0;
const want = fs.readdirSync(OCT05).filter((f) => !OWN.includes(f)).sort(), have = fs.readdirSync(MINE).sort();
report.files_missing = want.filter((f) => !have.includes(f));
report.files_added = have.filter((f) => !want.includes(f) && !OWN.includes(f));
report.gate_records = OWN;
fail += report.files_missing.length;
const ROWKEY = { "main_case_bands.csv": ["profile", "variant"], "components.csv": ["component"], "per_spec.csv": ["method", "spec"], "sign_reversal.csv": ["measure"] };
for (const f of want.filter((x) => have.includes(x))) {
  const a = path.join(OCT05, f), b = path.join(MINE, f);
  const r = { };
  if (f.endsWith(".csv")) {
    const [ha, ...ra] = readCsv(a), [hb, ...rb] = readCsv(b);
    r.columns_same_order = ha.every((c, i) => hb[i] === c);
    r.columns_added = hb.filter((c) => !ha.includes(c));
    r.columns_missing = ha.filter((c) => !hb.includes(c));
    const keyOf = (h, row) => (ROWKEY[f] || [h[0]]).map((k) => row[h.indexOf(k)]).join("|");
    const ka = ra.map((row) => keyOf(ha, row)), kb = rb.map((row) => keyOf(hb, row));
    r.rows = { oct05: ka.length, here: kb.length, missing: ka.filter((k) => !kb.includes(k)), added: kb.filter((k) => !ka.includes(k)) };
    const common = ka.filter((k) => kb.includes(k));
    r.rows.order_kept = common.every((k, i) => i === 0 || kb.indexOf(k) > kb.indexOf(common[i - 1]));
    if (!r.columns_same_order || r.columns_missing.length || r.rows.missing.length || !r.rows.order_kept) fail += 1;
  } else if (f.endsWith(".json")) {
    const pa = paths(JSON.parse(fs.readFileSync(a, "utf8")), [], new Map()), pb = paths(JSON.parse(fs.readFileSync(b, "utf8")), [], new Map());
    const rel = RELOCATED[f];
    const under = (segs, prefix) => prefix.every((k, i) => segs[i] === k);
    const missing = [], relocated = [], typeChanged = [], typeDocumented = [];
    for (const [id, [segs, t]] of pa) {
      if (pb.has(id)) {
        if (pb.get(id)[1] === t) continue;
        const why = (TYPE_CHANGES[f] || {})[show(segs)];
        if (why && why.startsWith(`${t} -> ${pb.get(id)[1]}:`)) typeDocumented.push(`${show(segs)}: ${why}`);
        else typeChanged.push(`${show(segs)}: ${t} -> ${pb.get(id)[1]}`);
        continue;
      }
      if (rel && segs.length > rel.from.length && under(segs, rel.from) && !rel.keep.includes(segs[rel.from.length])) {
        const q = rel.to.concat(segs.slice(rel.from.length)), qid = JSON.stringify(q);
        if (pb.has(qid) && pb.get(qid)[1] === t) { relocated.push(`${show(segs)} -> ${show(q)}`); continue; }
      }
      missing.push(show(segs));
    }
    // An added subtree is one difference: list the added paths whose nearest object parent is not itself added.
    const added = [...pb.values()].filter(([segs]) => !pa.has(JSON.stringify(segs)) && !(rel && under(segs, rel.to))).map(([segs]) => segs);
    const addedIds = new Set(added.map((x) => JSON.stringify(x)));
    const parentOf = (segs) => { const q = segs.slice(0, -1); while (q.length && q[q.length - 1] === "[]") q.pop(); return q; };
    const addedRoots = added.filter((segs) => { const q = parentOf(segs); return !q.length || !addedIds.has(JSON.stringify(q)); }).map(show);
    Object.assign(r, { key_paths: { oct05: pa.size, here: pb.size, added: added.length }, missing, type_changed: typeChanged, type_changes_documented: typeDocumented, relocated, added_subtrees: addedRoots });
    if (missing.length || typeChanged.length) fail += 1;
  }
  report.files[f] = r;
}
report.pass = fail === 0;
fs.writeFileSync(path.join(MINE, "contract.json"), JSON.stringify(report, null, 1) + "\n");

console.log(`[G2: v5's contract] files: ${want.length} v5, missing ${report.files_missing.length}${report.files_missing.length ? " (" + report.files_missing.join(", ") + ")" : ""}; added ${report.files_added.join(", ") || "none"} (gate records ${OWN.join(", ")} apart)`);
for (const [f, r] of Object.entries(report.files)) {
  if (r.rows) {
    console.log(`  ${f}: columns ${r.columns_same_order && !r.columns_missing.length ? "kept in order" : "CHANGED"}${r.columns_added.length ? `, added ${r.columns_added.join(" ")}` : ""}; rows ${r.rows.oct05} -> ${r.rows.here}, missing ${r.rows.missing.length}${r.rows.missing.length ? " (" + r.rows.missing.join("; ") + ")" : ""}, added ${r.rows.added.length}${r.rows.added.length ? " (" + r.rows.added.join("; ") + ")" : ""}${r.rows.order_kept ? "" : ", ORDER CHANGED"}`);
  } else {
    console.log(`  ${f}: key paths ${r.key_paths.oct05} -> ${r.key_paths.here}; missing ${r.missing.length}${r.missing.length ? " (" + r.missing.join("; ") + ")" : ""}; type changed ${r.type_changed.length}${r.type_changed.length ? " (" + r.type_changed.join("; ") + ")" : ""}; relocated ${r.relocated.length}; added ${r.key_paths.added} paths in ${r.added_subtrees.length} subtrees`);
    for (const x of r.relocated) console.log(`      relocated ${x}`);
    for (const x of r.type_changes_documented) console.log(`      type change ${x}`);
    for (const x of r.added_subtrees) console.log(`      added ${x}`);
  }
}
console.log(report.pass ? "G2 PASS: every v5 file, column, row and key is here (additions, the documented relocation and the documented type changes listed)" : "G2 FAIL");
if (!report.pass) process.exitCode = 1;
