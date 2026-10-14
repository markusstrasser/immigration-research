/* Actual v8 source-side exposures; construction amounts are held fixed. */
"use strict";
const fs = require("fs"), path = require("path"), crypto = require("crypto");
const P = require("../main_case_2026_10_15/package.cjs");
const F = path.resolve(__dirname, ".."), summary = P.readJson("main_case_2026_10_15/derived/summary.json");
const records = {}, sourceHashes = {};
for (const file of ["main_case_2026_10_15/derived/corrections.json", "main_case_2026_10_15/derived/corrections_cash.json", "main_case_2026_10_15/derived/summary.json"])
  sourceHashes[file] = crypto.createHash("sha256").update(fs.readFileSync(path.join(F, file))).digest("hex");
for (const [which, api] of [["set", P], ["cash", P.CASH]]) {
  const payload = api.correctionsPayload(), meta = payload.meta;
  const saved = P.readJson(`main_case_2026_10_15/derived/corrections${which === "cash" ? "_cash" : ""}.json`);
  if (JSON.stringify(saved) !== JSON.stringify(payload) || meta.coverage.stub) throw Error("[BLOCKED] v8 exposures need final, matching payloads");
  const costs = api.MAIN_SPECS.map(spec => api.evaluateFull(api.payloadModel(), spec).cost_bn);
  const ends = [costs.indexOf(Math.min(...costs)), costs.indexOf(Math.max(...costs))];
  const want = which === "cash" ? summary.cash_set.band_bn : summary.main_case;
  records[which] = {};
  for (const [j, end] of ["low", "high"].entries()) {
    const full = api.evaluateFull(api.payloadModel(), api.MAIN_SPECS[ends[j]]);
    if (Math.abs(full.cost_bn - want[j]) > 1e-9) throw Error(`[BLOCKED] v8 exposures ${which}/${end} does not reproduce the case`);
    const oracle = api.csvRows("main_case_2026_10_15/derived/main_case_bands.csv").find(r =>
      r.variant === (which === "cash" ? "cash_set" : "adopted") && r.profile === api.MAIN_PROFILE);
    if (!oracle || Math.abs(full.cost_bn - Number(oracle[`cost_${end}_bn`])) > 5e-5) throw Error("[BLOCKED] v8 exposure band oracle differs");
    const lines = {};
    const add = (side, id, amount, response) => {
      const k = `${side}|${id}`;
      if (!lines[k]) lines[k] = {side, id, amount_bn: 0, response};
      if (Math.abs(lines[k].response - response) > 1e-12) throw Error(`[BLOCKED] ${k} carrier/parent responses differ`);
      lines[k].amount_bn += amount;
    };
    for (const r of full.evaluation.receipts) add("receipt", r.id, r.amount_bn, r.response);
    for (const r of full.evaluation.spending) {
      const source = meta.union_completion.carriers[r.id];
      if (!source) add("spending", r.id, r.amount_bn, r.response);
      else if (source.kind === "line" && r.response !== 0) add(source.side, source.parent_line,
        source.side === "receipt" ? -r.amount_bn : r.amount_bn, r.response);
    }
    records[which][end] = {specification: ends[j], case_bn: full.cost_bn, lines,
      fixed_post_engine: full.post_engine, population: meta.population_v8};
  }
}
const output = {case_key: "oct15", source_hashes: sourceHashes, records,
  coverage_reweighted: false, mixed_unit_reweighted: false,
  rule: "Actual native corrected line amounts plus reporter source-side carriers; first-order measured-CPS key ratios transport to these exposures. Public-capital/production and post-engine constructions stay fixed."};
fs.writeFileSync(path.join(__dirname, "derived/v8_exposures.json"), JSON.stringify(output, null, 1) + "\n");
console.log("v8 source-side exposures: exact set/cash/end and external-band gates pass; coverage held fixed");
