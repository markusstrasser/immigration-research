/* The generation lane's split of the case, line by line, for the world ledger's generation rows.
 *
 * The generation lane (generation_account_2026_09_24/run_generations.cjs) evaluates the case once per
 * generation: each generation's uncorrected model (model_{G1,G2,G3plus}.json, convention (a): each person in their
 * own generation) takes its netted corrections payload (generation_corrections.json) and is evaluated with the
 * case package's engine state at every specification. This script repeats that evaluation at the case's two band
 * ends and writes every line, so the world ledger values the generation lane's own split and never a second one.
 * The band ends are the union's cheapest and dearest specifications, the first on a tie, as that lane picks them
 * (48 and 11 in both cases here). The allocation of household flows is the specification's: shared at the low
 * end, personal at the high end.
 *
 * It also evaluates the uncorrected models at the same specifications, for split_residual.py, which shows how the
 * lane's split departs from splitting each corrected line by the generations' shares of it.
 *
 * Inputs: the generation lane's files at the case's generation pin (pins.json), read with git show; the case's
 * package (read-only, as run_generations.cjs reads it). Rows: every spending line and receipt with the engine's key
 * (receipts: scenario:key), its amount, response and effect (the engine's signs: receipts +, spending -), each
 * capital-return component (under sept27; amount = stock x rate x key, effect = -return), and per generation the
 * totals: the direct fiscal response, the capital return, the production term and the cost. Gates: the corrected
 * cost equals generation_results.csv convention (a) `cost_bn`, and the uncorrected cost its `uncorrected_same_spec_bn`,
 * to 1e-6.
 *
 * Run from the repository root:
 *   node infra/immigration-fiscal/world_ledger_2026_09_27/generation_lines.cjs --case sept26_schools|sept27
 * Output: derived/generation_lines_<case>.csv, derived/generation_lines_uncorrected_<case>.csv.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const REPO = path.join(FISCAL, "..", "..");
const argv = process.argv.slice(2);
const arg = (name, dflt) => { const i = argv.indexOf(name); return i < 0 ? dflt : argv[i + 1]; };
// The package lane of each case, as run_generations.cjs maps them.
const CASES = { sept27: "main_case_long_run_2026_09_27", sept26_schools: "main_case_schools_full_2026_09_26" };
const CASE = arg("--case", "sept26_schools");
if (!CASES[CASE]) throw new Error(`--case must be one of ${Object.keys(CASES).join(", ")}`);
const ON27 = CASE === "sept27";
const PIN = JSON.parse(fs.readFileSync(path.join(HERE, "pins.json"), "utf8"))[CASE].generation;
if (!PIN) throw new Error(`[BLOCKED] no generation pin for ${CASE}`);
const GREL = "infra/immigration-fiscal/generation_account_2026_09_24/derived";
const show = (f) => execFileSync("git", ["-C", REPO, "show", `${PIN}:${GREL}/${f}`], { maxBuffer: 1 << 30 }).toString("utf8");
const P = require(path.join(FISCAL, CASES[CASE], "package.cjs"));
const { Engine, MAIN_SPECS } = P;
const GENS = ["G1", "G2", "G3plus"];

const fails = [];
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? ` (${detail})` : ""}`);
  if (!ok) fails.push(label);
}

const corr = JSON.parse(show("generation_corrections.json"));
gate(`generation_corrections.json at ${PIN} is the ${CASE} case's (${corr.meta.union})`, corr.meta.union.startsWith(CASES[CASE] + "/"));
const raw = Object.fromEntries(GENS.map((g) => [g, show(`model_${g}.json`)]));
// Each model is parsed on its own, so the corrected model never shares objects with the uncorrected one.
const MODELS = {
  corrected: Object.fromEntries(GENS.map((g) => [g, Engine.applyCorrections(JSON.parse(raw[g]), corr.payloads.a[g])])),
  uncorrected: Object.fromEntries(GENS.map((g) => [g, JSON.parse(raw[g])])),
};
// run_generations.cjs's partsAt(): evaluateFull() under sept27, the engine on stateFor() otherwise.
const partsAt = (m, spec) => (ON27 ? P.evaluateFull(m, spec, P.MAIN_PROFILE)
  : { evaluation: Engine.evaluate(m, P.stateFor(m, spec, P.MAIN_PROFILE)), capital: { total_bn: 0, components: [] } });
const costOf = (r) => -r.evaluation.welfare_bn + r.capital.total_bn;

const union = MAIN_SPECS.map((s) => GENS.reduce((t, g) => t + costOf(partsAt(MODELS.corrected[g], s)), 0));
const lo = union.indexOf(Math.min(...union)), hi = union.indexOf(Math.max(...union));
const results = execFileSync("git", ["-C", REPO, "show", `${PIN}:${GREL}/generation_results.csv`]).toString("utf8")
  .trim().split("\n").map((l) => l.split(","));
const col = Object.fromEntries(results[0].map((k, i) => [k, i]));
const laneRow = (g, end) => {
  const r = results.slice(1).filter((x) => x[col.convention] === "a" && x[col.generation] === g && x[col.band_end] === end);
  if (r.length !== 1) throw new Error(`[BLOCKED] generation_results.csv has ${r.length} rows for (a) ${g} ${end}`);
  return { cost: Number(r[0][col.cost_bn]), uncorrected: Number(r[0][col.uncorrected_same_spec_bn]),
    allocation: r[0][col.allocation] };
};

const f = (x) => x.toFixed(9);
const HEAD = ["case", "band_end", "spec", "allocation", "generation", "side", "line", "key", "amount_bn", "response", "effect_bn"].join(",");
const out = { corrected: [HEAD], uncorrected: [HEAD] };
let worst = 0;
for (const [end, i] of [["low", lo], ["high", hi]]) {
  const spec = MAIN_SPECS[i];
  for (const g of GENS) {
    const lane = laneRow(g, end);
    for (const which of ["corrected", "uncorrected"]) {
      const m = MODELS[which][g];
      const r = partsAt(m, spec), ev = r.evaluation;
      const scenario = P.stateFor(m, spec, P.MAIN_PROFILE).receipt_scenario;
      const put = (side, id, key, amount, response, effect) =>
        out[which].push([CASE, end, i, spec.allocation, g, side, id, key, f(amount), f(response), f(effect)].join(","));
      for (const x of ev.spending) put("spending", x.id, x.key, x.amount_bn, x.response, x.effect_bn);
      for (const x of ev.receipts) put("receipt", x.id, `${scenario}:${x.key}`, x.amount_bn, x.response, x.effect_bn);
      for (const c of r.capital.components) put("capital", `capital_${c.id}`, "", c.stock_charged_bn * spec.rate * c.key, c.response, -c.return_bn);
      // Totals, as positive costs to other residents: the direct response (spending less receipts), the capital
      // return, the production term (private gain plus induced receipts, signed as a cost) and the cost itself.
      const lines = ev.spending.reduce((t, x) => t - x.effect_bn, 0) - ev.receipts.reduce((t, x) => t + x.effect_bn, 0);
      put("total", "direct_fiscal", "", 0, 0, -ev.direct_fiscal_response_bn);
      put("total", "capital_return", "", 0, 0, r.capital.total_bn);
      put("total", "production", "", 0, 0, -(ev.private_wtp_bn + ev.induced_receipts_bn));
      put("total", "cost", "", 0, 0, costOf(r));
      worst = Math.max(worst, Math.abs(lines + ev.direct_fiscal_response_bn));
      const target = which === "corrected" ? lane.cost : lane.uncorrected;
      gate(`(a) ${g} ${end} (spec ${i}, ${spec.allocation}), ${which}: the cost equals generation_results.csv`,
        Math.abs(costOf(r) - target) < 1e-6 && lane.allocation === spec.allocation,
        `${costOf(r).toFixed(6)} against ${target.toFixed(6)} (${lane.allocation})`);
    }
  }
}
gate("the lines add to the engine's direct response", worst < 1e-9, `max |diff| ${worst.toExponential(2)} bn`);
if (fails.length) {
  console.log(`✗ ${fails.length} gate(s) failed, nothing written`);
  process.exit(1);
}
fs.writeFileSync(path.join(HERE, "derived", `generation_lines_${CASE}.csv`), out.corrected.join("\n") + "\n");
fs.writeFileSync(path.join(HERE, "derived", `generation_lines_uncorrected_${CASE}.csv`), out.uncorrected.join("\n") + "\n");
console.log(`  wrote derived/generation_lines_${CASE}.csv and generation_lines_uncorrected_${CASE}.csv: band ends ${lo} and ${hi}, `
  + `${out.corrected.length - 1} and ${out.uncorrected.length - 1} rows`);
