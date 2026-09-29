/* G2, the contract: this lane's derived files against the September 27 lane's (main_case_long_run_2026_09_27/derived).
 *
 * Every September 27 file must exist here. In each CSV the September 27 columns must lead in the same order, and every
 * September 27 row name must be here: main_case_bands.csv (profile, variant), components.csv (component), per_spec.csv
 * (method, spec) and sign_reversal.csv (measure). In summary.json and corrections.json every September 27 key path must
 * be here with the same JSON type (an array's elements count as one element, "[]"), except the relocations RELOCATED
 * documents, each of which must be found at its new path. Every difference is listed: added files, columns, rows and
 * keys, relocations, and anything missing, which fails the gate.
 *
 * Run from anywhere (after main_case.cjs and sign_reversal.cjs): node contract.cjs -> derived/contract.json
 */
"use strict";
const fs = require("fs");
const path = require("path");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const SEPT27 = path.join(FISCAL, "main_case_long_run_2026_09_27", "derived");
const MINE = path.join(HERE, "derived");
// This lane's gate records (G2, G3, G4): not part of the September 27 contract, listed apart from added files.
const OWN = ["api_check.json", "contract.json", "generality.json"];
// The September 27 key paths that move, and where to (summary.json): the September 27 case's own change from the
// schools case, by its additions, sits under change_at_fixed_specifications.sept27_case; the top level holds v4's
// change from the September 27 case, by item.
const RELOCATED = { "summary.json": { from: ["change_at_fixed_specifications"], to: ["change_at_fixed_specifications", "sept27_case"],
  keep: ["total", "note"] } };

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

const report = { gate: "G2: every September 27 derived file exists here with its columns, rows and keys; every difference listed", files: {} };
let fail = 0;
const want = fs.readdirSync(SEPT27).sort(), have = fs.readdirSync(MINE).sort();
report.files_missing = want.filter((f) => !have.includes(f));
report.files_added = have.filter((f) => !want.includes(f) && !OWN.includes(f));
report.gate_records = OWN;
fail += report.files_missing.length;
const ROWKEY = { "main_case_bands.csv": ["profile", "variant"], "components.csv": ["component"], "per_spec.csv": ["method", "spec"], "sign_reversal.csv": ["measure"] };
for (const f of want.filter((x) => have.includes(x))) {
  const a = path.join(SEPT27, f), b = path.join(MINE, f);
  const r = { };
  if (f.endsWith(".csv")) {
    const [ha, ...ra] = readCsv(a), [hb, ...rb] = readCsv(b);
    r.columns_same_order = ha.every((c, i) => hb[i] === c);
    r.columns_added = hb.filter((c) => !ha.includes(c));
    r.columns_missing = ha.filter((c) => !hb.includes(c));
    const keyOf = (h, row) => (ROWKEY[f] || [h[0]]).map((k) => row[h.indexOf(k)]).join("|");
    const ka = ra.map((row) => keyOf(ha, row)), kb = rb.map((row) => keyOf(hb, row));
    r.rows = { sept27: ka.length, here: kb.length, missing: ka.filter((k) => !kb.includes(k)), added: kb.filter((k) => !ka.includes(k)) };
    const common = ka.filter((k) => kb.includes(k));
    r.rows.order_kept = common.every((k, i) => i === 0 || kb.indexOf(k) > kb.indexOf(common[i - 1]));
    if (!r.columns_same_order || r.columns_missing.length || r.rows.missing.length || !r.rows.order_kept) fail += 1;
  } else if (f.endsWith(".json")) {
    const pa = paths(JSON.parse(fs.readFileSync(a, "utf8")), [], new Map()), pb = paths(JSON.parse(fs.readFileSync(b, "utf8")), [], new Map());
    const rel = RELOCATED[f];
    const under = (segs, prefix) => prefix.every((k, i) => segs[i] === k);
    const missing = [], relocated = [], typeChanged = [];
    for (const [id, [segs, t]] of pa) {
      if (pb.has(id)) { if (pb.get(id)[1] !== t) typeChanged.push(`${show(segs)}: ${t} -> ${pb.get(id)[1]}`); continue; }
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
    Object.assign(r, { key_paths: { sept27: pa.size, here: pb.size, added: added.length }, missing, type_changed: typeChanged, relocated, added_subtrees: addedRoots });
    if (missing.length || typeChanged.length) fail += 1;
  }
  report.files[f] = r;
}
report.pass = fail === 0;
fs.writeFileSync(path.join(MINE, "contract.json"), JSON.stringify(report, null, 1) + "\n");

console.log(`[G2: the September 27 contract] files: ${want.length} September 27, missing ${report.files_missing.length}${report.files_missing.length ? " (" + report.files_missing.join(", ") + ")" : ""}; added ${report.files_added.join(", ") || "none"} (gate records ${OWN.join(", ")} apart)`);
for (const [f, r] of Object.entries(report.files)) {
  if (r.rows) {
    console.log(`  ${f}: columns ${r.columns_same_order && !r.columns_missing.length ? "kept in order" : "CHANGED"}${r.columns_added.length ? `, added ${r.columns_added.join(" ")}` : ""}; rows ${r.rows.sept27} -> ${r.rows.here}, missing ${r.rows.missing.length}${r.rows.missing.length ? " (" + r.rows.missing.join("; ") + ")" : ""}, added ${r.rows.added.length}${r.rows.added.length ? " (" + r.rows.added.join("; ") + ")" : ""}${r.rows.order_kept ? "" : ", ORDER CHANGED"}`);
  } else {
    console.log(`  ${f}: key paths ${r.key_paths.sept27} -> ${r.key_paths.here}; missing ${r.missing.length}${r.missing.length ? " (" + r.missing.join("; ") + ")" : ""}; type changed ${r.type_changed.length}${r.type_changed.length ? " (" + r.type_changed.join("; ") + ")" : ""}; relocated ${r.relocated.length}; added ${r.key_paths.added} paths in ${r.added_subtrees.length} subtrees`);
    for (const x of r.relocated) console.log(`      relocated ${x}`);
    for (const x of r.added_subtrees) console.log(`      added ${x}`);
  }
}
console.log(report.pass ? "G2 PASS: every September 27 file, column, row and key is here (additions and the documented relocation listed)" : "G2 FAIL");
if (!report.pass) process.exitCode = 1;
