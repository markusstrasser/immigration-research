/* G2 for v10, adapted from main_case_2026_10_16/contract.cjs: every v9 output file a consumer reads is written, with
every v9 column, row and key path; additions, documented type changes and documented removals are listed.
Run: node contract.cjs [--out-dir DIR]. Writes contract.json there; exit 1 on failure. */
"use strict";
const fs = require("fs"), path = require("path"), assert = require("assert");
const HERE = __dirname, OLD = path.join(HERE, "../main_case_2026_10_16/derived");
const args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
// v10's own gate records and new outputs.
const OWN = ["api_check.json", "contract.json", "checks.json", "independent_check.json", "ancestry.json", "per_spec_cash.csv"];
// v9 files v10 does not write, with the reason. A consumer re-pointed to oct24 reads these from v9 or stops.
const NOT_WRITTEN = {
  "g1.json": "v9's G1 gate record; v10's gates are checks.json",
  "generality.json": "v9's generality gate record over v9's own items",
  "api_check.json": "replaced by v10's own api_check.json (in OWN)",
  "contract.json": "replaced by v10's own contract.json (in OWN)",
  "coverage_check.json": "v9 input check of item 12 coverage; v10 adds no people and carries v9's coverage",
  "source_checks.json": "v9 input check of item 21's sources; unchanged inputs",
  "market_check.json": "v9 input check; unchanged inputs",
  "rate_check.json": "v9's item 20 rate arms; v10 reprices item 20's capital through item 22 (summary.v10.item22)",
  "union_credit_parts.json": "v8 union-completion input carried by v9; v10 adds no edits",
  "union_people.json": "v8 union-completion input carried by v9; v10 adds no people",
  "union_probe_checks.json": "v8 union-completion check carried by v9",
  "mixed_overlap.json": "v8 item 11 input carried by v9; v10 adds no edits",
  "lineage_addition.json": "NOT RECOMPUTED for v10: v9's lineage-addition dollars omit items 22-23; a consumer of it must read v9's file and add the v10 terms' added-lineage parts (derived/ancestry.json generation_at_ends.*.added) or stop",
};
const ROWKEY = { "main_case_bands.csv": ["profile", "variant"], "components.csv": ["component"], "per_spec.csv": ["method", "spec"], "sign_reversal.csv": ["measure"] };
const TYPE_CHANGES = Object.fromEntries(["corrections.json", "corrections_cash.json"].map((f) => [f, {
  "meta.adopted": "string -> null: v10 is a candidate; the parent controls adoption",
  "meta.decision": "string -> null: no v10 decision record exists yet",
}]));
TYPE_CHANGES["summary.json"] = { decision: "string -> null: no v10 decision record exists yet" };
const REMOVED = Object.fromEntries(["corrections.json", "corrections_cash.json"].map((f) => [f, {
  "meta.one_rate.flat_real_equivalent": "removed with item 22 on, so that a flat-rate reader stops; rates are meta.v10.rates",
}]));
const csv = (text) => text.trimEnd().split("\n").map((l) => { const out = []; let cur = "", q = false; for (let i = 0; i < l.length; i++) { const ch = l[i]; if (ch === '"') { if (q && l[i + 1] === '"') { cur += '"'; i++; } else q = !q; } else if (ch === "," && !q) { out.push(cur); cur = ""; } else cur += ch; } if (q) throw Error("[BLOCKED] G2 unclosed CSV quote"); out.push(cur); return out; });
const type = (x) => Array.isArray(x) ? "array" : x === null ? "null" : typeof x;
function paths(x, segs = [], out = new Map()) {
  if (Array.isArray(x)) { for (const el of x) if (el && typeof el === "object") paths(el, segs.concat("[]"), out); }
  else if (x && typeof x === "object") for (const [k, v] of Object.entries(x)) { const p = segs.concat(k), id = JSON.stringify(p); if (!out.has(id)) out.set(id, [p, type(v)]); paths(v, p, out); }
  return out;
}
const show = (s) => s.join(".");
function compareCsv(a, b, file) {
  const [ha, ...ra] = csv(a), [hb, ...rb] = csv(b), key = (h, row) => (ROWKEY[file] || [h[0]]).map((k) => row[h.indexOf(k)]).join("|");
  const ka = ra.map((r) => key(ha, r)), kb = rb.map((r) => key(hb, r)), missing = ka.filter((k) => !kb.includes(k));
  const common = ka.filter((k) => kb.includes(k)), order = common.every((k, i) => !i || kb.indexOf(k) > kb.indexOf(common[i - 1]));
  const r = { columns_same_order: ha.every((c, i) => hb[i] === c), columns_added: hb.filter((c) => !ha.includes(c)), columns_missing: ha.filter((c) => !hb.includes(c)), rows: { v9: ka.length, here: kb.length, missing, added: kb.filter((k) => !ka.includes(k)), order_kept: order } };
  r.pass = r.columns_same_order && !r.columns_missing.length && !missing.length && order; return r;
}
function compareJson(a, b, file) {
  const pa = paths(a), pb = paths(b), missing = [], removed = [], changed = [], documented = [];
  for (const [id, [segs, t]] of pa) {
    if (!pb.has(id)) { const why = REMOVED[file]?.[show(segs)]; if (why) removed.push(`${show(segs)}: ${why}`); else missing.push(show(segs)); continue; }
    const nt = pb.get(id)[1]; if (t === nt) continue;
    const why = TYPE_CHANGES[file]?.[show(segs)]; if (why?.startsWith(`${t} -> ${nt}:`)) documented.push(`${show(segs)}: ${why}`); else changed.push(`${show(segs)}: ${t} -> ${nt}`);
  }
  const added = [...pb.values()].filter(([s]) => !pa.has(JSON.stringify(s))).map(([s]) => s), addedIds = new Set(added.map((s) => JSON.stringify(s)));
  const parent = (s) => { const p = s.slice(0, -1); while (p.at(-1) === "[]") p.pop(); return p; };
  return { pass: !missing.length && !changed.length, key_paths: { v9: pa.size, here: pb.size, added: added.length }, missing, removed_documented: removed, type_changed: changed, type_changes_documented: documented, added_subtrees: added.filter((s) => !addedIds.has(JSON.stringify(parent(s)))).map(show) };
}
// Negative controls: the gate rejects destructive contract changes.
const selfChecks = [];
function negative(name, ok) { assert(ok, `[BLOCKED] G2 negative probe ${name}`); selfChecks.push({ name, pass: true }); }
negative("missing CSV row", !compareCsv("component,n\na,1\nb,2\n", "component,n\na,1\n", "components.csv").pass);
negative("missing CSV column", !compareCsv("component,n\na,1\n", "component\na\n", "components.csv").pass);
negative("reordered CSV rows", !compareCsv("component,n\na,1\nb,2\n", "component,n\nb,2\na,1\n", "components.csv").pass);
negative("missing JSON key", !compareJson({ a: { b: 1 } }, { a: {} }, "x.json").pass);
negative("undocumented JSON type change", !compareJson({ a: 1 }, { a: "1" }, "x.json").pass);
negative("undocumented removal of the flat rate elsewhere", !compareJson({ meta: { one_rate: { flat_real_equivalent: 1 } } }, { meta: { one_rate: {} } }, "summary.json").pass);
const v9files = fs.readdirSync(OLD).sort(), want = v9files.filter((f) => !NOT_WRITTEN[f]), have = fs.readdirSync(OUT).sort();
const report = { gate: "G2 v10: every v9 output file a consumer reads is present with every v9 column, row and key; additions, type changes and removals listed",
  files_missing: want.filter((f) => !have.includes(f)), files_not_written: NOT_WRITTEN, unlisted_v9_files: v9files.filter((f) => !want.includes(f) && !NOT_WRITTEN[f]),
  files_added: have.filter((f) => !v9files.includes(f)), own: OWN, self_checks: selfChecks, files: {} };
for (const f of want.filter((f) => have.includes(f))) {
  const a = fs.readFileSync(path.join(OLD, f), "utf8"), b = fs.readFileSync(path.join(OUT, f), "utf8");
  report.files[f] = f.endsWith(".csv") ? compareCsv(a, b, f) : f.endsWith(".json") ? compareJson(JSON.parse(a), JSON.parse(b), f) : { pass: true, kind: "presence-only" };
}
report.pass = !report.files_missing.length && !report.unlisted_v9_files.length && report.files_added.every((f) => OWN.includes(f)) && Object.values(report.files).every((r) => r.pass);
report.verdict = report.pass ? "PASS" : "FAIL";
fs.writeFileSync(path.join(OUT, "contract.json"), JSON.stringify(report, null, 1) + "\n");
for (const [file, r] of Object.entries(report.files)) console.log(`${r.pass ? "PASS" : "FAIL"} ${file}: ${r.rows ? `${r.rows.v9} -> ${r.rows.here} rows` : `${r.key_paths?.v9} -> ${r.key_paths?.here} key paths`}${r.missing?.length ? " missing " + r.missing.slice(0, 5).join(", ") : ""}${r.type_changed?.length ? " changed " + r.type_changed.slice(0, 5).join(", ") : ""}`);
if (report.files_missing.length) console.log(`FAIL missing files: ${report.files_missing.join(", ")}`);
console.log(`G2 v10 ${report.verdict}: ${want.length} v9 files checked, ${Object.keys(NOT_WRITTEN).length} not written (listed), ${selfChecks.length} negative probes`);
if (!report.pass) process.exitCode = 1;
