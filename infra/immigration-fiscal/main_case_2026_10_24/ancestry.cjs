/* v9's two structural ancestry-share readings on candidate v10 (generation.cjs), set and cash, plus the v10 terms'
generation split at the end specifications. Writes derived/ancestry.json; main_case.cjs reads it.
Run: node ancestry.cjs [--out-dir DIR]. */
"use strict";
const fs = require("fs"), path = require("path");
const P = require("./package.cjs"), GEN = require("./generation.cjs"), I = P.ITEMS;
const HERE = __dirname, args = process.argv.slice(2), OUT = path.resolve(args.includes("--out-dir") ? args[args.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
const started = performance.now();
const out = { rate_source: I.RATE_SOURCE, selected_items: P.CANDIDATE, rule: "generation.cjs: v9 per-specification ancestry costs plus the ancestry-share-weighted v10 terms by generation" };
for (const which of ["set", "cash"]) out[which] = GEN.ancestry(P, which);
// The v10 terms by generation at the end specifications (payload model), by item: for generation consumers.
out.generation_at_ends = {};
for (const which of ["set", "cash"]) out.generation_at_ends[which] = Object.fromEntries(Object.entries(P.END_SPECS).map(([end, i]) => [end,
  Object.fromEntries(P.ACTIVE_NEW.map((id) => [id, GEN.split(P, which, P.MAIN_SPECS[i], [id])]))]));
fs.mkdirSync(OUT, { recursive: true });
fs.writeFileSync(path.join(OUT, "ancestry.json"), JSON.stringify(out, null, 1) + "\n");
console.log(JSON.stringify({ ancestry: Object.fromEntries(out.set.map((r) => [r.scenario, { set: r.band_bn, cash: out.cash.find((z) => z.scenario === r.scenario).band_bn, change: r.change_from_v9_bn }])), seconds: (performance.now() - started) / 1000, maxRSS_MiB: process.resourceUsage().maxRSS / 1024 }));
