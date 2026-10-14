/* v8 bridge: preserve the verified historical decomposition, add items 9–12
 * as distinct, evaluated components. Never write any earlier case artifact. */
"use strict";
const fs = require("fs"), path = require("path"), os = require("os"), cp = require("child_process"), crypto = require("crypto");
const HERE = __dirname, FISCAL = path.resolve(HERE, ".."), LANE = "main_case_2026_10_15";
const P = require("../main_case_2026_10_15/package.cjs");
const sum = xs => xs.reduce((a, b) => a + b, 0), mean = xs => sum(xs) / xs.length;
const fail = s => { throw Error(`[BLOCKED] oct15 backcast: ${s}`); };
const near = (a, b, label, tol = 1e-9) => { if (!Number.isFinite(a) || Math.abs(a - b) > tol) fail(`${label}: ${a} != ${b}`); };
const read = rel => JSON.parse(fs.readFileSync(path.join(FISCAL, rel), "utf8"));
const sha = rel => {
  const fd = fs.openSync(path.join(FISCAL, rel), "r"), hash = crypto.createHash("sha256"), buffer = Buffer.alloc(1024 * 1024);
  try { let n; while ((n = fs.readSync(fd, buffer, 0, buffer.length, null)) > 0) hash.update(buffer.subarray(0, n)); }
  finally { fs.closeSync(fd); }
  return hash.digest("hex");
};
const PARENT = {school_reprice: "education_services", college_rekey: "education_services", roads_vmt_sl: "economic_affairs_services",
  roads_vmt_fed: "economic_affairs_services", state_price_public_order_safety: "public_order_safety", state_price_health_services: "health_services",
  state_price_recreation_culture: "recreation_culture"};
function main(outDir) {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "backcast-v8-components-"));
  let data;
  try {
    const control = cp.spawnSync(process.execPath, [path.join(HERE, "case_components.cjs"), "--case", "oct14", "--out-dir", tmp], {encoding: "utf8"});
    if (control.status !== 0) fail(`historical components stop: ${control.stdout.slice(-2000)} ${control.stderr.slice(-2000)}`);
    data = JSON.parse(fs.readFileSync(path.join(tmp, "case_components_oct14.json"), "utf8"));
  } finally { fs.rmSync(tmp, {recursive: true, force: true}); }
  const summary = read(`${LANE}/derived/summary.json`);
  const meta = P.correctionsPayload().meta;
  const coverageTransport = process.env.BACKCAST_COVERAGE_TRANSPORT || "source_piece_profile";
  if (!["source_piece_profile", "per_member_total"].includes(coverageTransport)) fail(`unknown coverage transport ${coverageTransport}`);
  const coverageFile = path.join(HERE, "derived/coverage_components_oct15.json");
  let coverageProfile = null;
  if (coverageTransport === "source_piece_profile") {
    if (!fs.existsSync(coverageFile)) fail("run coverage_components.py after the parent's coverage inputs are final");
    coverageProfile = JSON.parse(fs.readFileSync(coverageFile, "utf8"));
    for (const [rel, digest] of Object.entries(coverageProfile.inputs)) if (sha(path.relative(FISCAL, path.resolve(FISCAL, "../..", rel))) !== digest) fail(`stale coverage source profile ${rel}`);
  }
  const mixedFile = path.join(HERE, "derived/mixed_components_oct15.json");
  if (!fs.existsSync(mixedFile)) fail("run mixed_components.py for the exact item11 source programme parts");
  const mixedProfile = JSON.parse(fs.readFileSync(mixedFile, "utf8"));
  for (const [rel, digest] of Object.entries(mixedProfile.inputs)) if (sha(path.relative(FISCAL, path.resolve(FISCAL, "../..", rel))) !== digest) fail(`stale mixed source profile ${rel}`);
  const liveEnds = summary.v8.end_specifications;
  if (["set", "cash"].some(w => liveEnds[w].some(ends => JSON.stringify(ends) !== JSON.stringify([16, 11])))) fail("live ends moved; historical components need repricing at the new ends");
  data.case = "oct15"; data.lane = LANE;
  data.v8_rule = "Items 9–12 separately, at live personal ends; union completion reporters and nonreporters follow G3+ population path. Post-engine mixed removal and coverage applied once.";
  data.coverage_transport = coverageTransport;
  data.population_v8 = meta.population_v8;
  data.population_counts = {lineage: meta.lineage.counts, completion: meta.union_completion.counts, coverage: meta.coverage};
  const bands = fs.readFileSync(path.join(FISCAL, LANE, "derived/main_case_bands.csv"), "utf8").trim().split("\n").map(s => s.split(","));
  const header = bands.shift();
  const oracle = (profile, variant) => {
    const rows = bands.map(r => Object.fromEntries(header.map((h, i) => [h, r[i]]))).filter(r => r.profile === profile && r.variant === variant);
    if (rows.length === 0 && profile === "proportional_reference" && variant === "cash_set") return null;
    if (rows.length !== 1) fail(`band row ${profile}/${variant}`);
    return [Number(rows[0].cost_low_bn), Number(rows[0].cost_high_bn)];
  };
  // Package construction re-prices 17 child age bands. Build each cumulative
  // item once rather than repeating that work for every concept/method/end.
  const ordered = [], cumulative = [...P.V7_PACKAGE.ITEM_IDS];
  for (const id of P.V8_IDS) {
    cumulative.push(id);
    ordered.push([id, P.caseOf(P.OCT05, cumulative)]);
  }
  for (const [concept, block] of Object.entries(data.concepts)) {
    const byEnd = {}, metadata = {};
    for (const [ei, end] of ["low", "high"].entries()) {
      const methodParts = [], cashTotals = [], fullTotals = [];
      for (const [mi, method] of P.METHODS.entries()) {
        const index = block.end_specifications[mi][end];
        const finalSpec = P.ALL_SPECS[index];
        if (finalSpec.allocation !== "personal") fail("nonpersonal endpoint");
        const options = {profile: block.profile};
        let before = P.V7_PACKAGE, run = api => api.evaluateFull(api.modelFor("central", method, api.withCentral(options)), api.ALL_SPECS[index], block.profile);
        let b = run(before), bc = run(before.CASH), parts = {};
        const add = (name, value, info) => {
          if (name in parts) fail(`duplicate ${name}`);
          parts[name] = value; metadata[name] = info;
        };
        for (const [id, after] of ordered) {
          const a = run(after), ac = run(after.CASH);
          const payload = after.correctionsPayload(options), rec = payload.meta.items.find(x => x.id === id);
          const cashPayload = after.CASH.correctionsPayload(options);
          const setValues = {}, cashValues = {}, infos = {};
          const collect = (api, record, pp, evaluation, dest) => {
            if (record.kind === "post_engine") {
              const z = pp.meta[id].by_end[end];
              if (id === "mixed_unit_removal") {
                const basis = api === after ? "set" : "cash", sourceModel = api.payloadModel();
                for (const piece of mixedProfile.sets[basis].filter(r => r.end === end)) {
                  const name = `v6_${id}_${piece.path}_${piece.generation}_${piece.component}`;
                  const modelLine = sourceModel[piece.side === "receipt" ? "receipts" : "spending"].lines.find(l => l.id === piece.line);
                  dest[name] = piece.value_bn;
                  infos[name] = {...piece, item: id, national_bn: modelLine?.national_bn ?? null, parent: null};
                  if (["G3+", "G3plus"].includes(piece.generation)) infos[name].population_path = "g3plus";
                  delete infos[name].value_bn; delete infos[name].end;
                }
                near(sum(Object.values(dest)), z.total_bn, "mixed exact programme source closure");
                return;
              }
              if (id === "coverage" && coverageProfile) {
                const basis = api === after ? "set" : "cash";
                const sourceModel = api.payloadModel();
                for (const piece of coverageProfile.sets[basis].filter(r => r.end === end)) {
                  const name = `v6_coverage_union_${piece.generation}_${piece.piece}_${piece.line}`;
                  dest[name] = piece.value_bn;
                  const accrual = piece.category === "pension_accrual";
                  if (accrual && !["social_security", "medicare"].includes(piece.line)) fail(`coverage accrual ${piece.line} lacks a source-specific income rule`);
                  const existing = [...Object.values(block.v6_parts), ...Object.values(block.v5_parts), ...Object.values(block.v4_parts)]
                    .find(p => p.side === piece.side && p.line === piece.line && Number.isFinite(p.national_bn));
                  const modelLine = sourceModel[piece.side === "receipt" ? "receipts" : "spending"]?.lines.find(l => l.id === piece.line);
                  infos[name] = {item: id, path: "union", side: piece.side, line: piece.line, national_bn: existing?.national_bn ?? modelLine?.national_bn ?? null,
                    parent: PARENT[piece.line] || null, generation: piece.generation,
                    rule: piece.unlocated || ["lane_constants", "source_rounding"].includes(piece.line) ? "per_person" : piece.side === "capital" ? "capital" : piece.side === "production" ? "production" : accrual ? "accrual" : "line",
                    ...(piece.side === "capital" ? {component: piece.line, level: piece.component_level} : {}),
                    ...(accrual ? {contributions: piece.line === "social_security" ? "oasdi" : "hi"} : {}),
                    ...(piece.generation === "G3plus" ? {population_path: "g3plus"} : {}),
                    ...(piece.unlocated ? {unlocated: true, transport_assumption: piece.rule} : {}),
                    ...(piece.transport_assumption ? {transport_assumption: piece.transport_assumption} : {})};
                }
                near(sum(Object.values(dest)), z.total_bn, "coverage source-piece principal closure");
                return;
              }
              const gens = z.by_generation_bn || z.by_generation;
              const residual = id === "mixed_unit_removal" ? z.D_added_residual_bn : 0;
              for (const [generation, value] of Object.entries(gens)) {
                const name = `v6_${id}_union_${generation}`;
                dest[name] = value - (["G3+", "G3plus"].includes(generation) ? residual : 0);
                infos[name] = {item: id, path: "union", side: id === "coverage" ? "post_engine" : "receipt", line: id === "coverage" ? "coverage" : "federal_income_tax", national_bn: null,
                  parent: null, rule: id === "coverage" ? "coverage" : "line", generation};
              }
              if (residual) {
                const name = `v6_${id}_lineage_D_added_residual`;
                dest[name] = residual; infos[name] = {item: id, path: "lineage", side: "receipt", line: "federal_income_tax", national_bn: null, parent: null, rule: "line"};
              }
              near(sum(Object.values(dest)), z.total_bn, `${id} post-engine parts`);
              return;
            }
            if (record.kind !== "edit_set") fail(`no rule for ${id}/${record.kind}`);
            const edits = pp.edits.slice(record.edits.first, record.edits.first + record.edits.count);
            for (const [tag, part] of Object.entries(record.parts)) {
              const edit = edits[part.edit], carrier = pp.meta.union_completion?.carriers[edit.line];
              const side = edit.side === "receipt" ? "receipts" : "spending";
              const row = evaluation.evaluation[side].find(x => x.id === edit.line);
              if (!row) fail(`missing ${id}/${edit.line}`);
              if ((side === "receipts" && edit.scenario !== api.MODEL.receipts.reference) || (side === "spending" && edit.key !== row.key)) continue;
              const pop = tag.startsWith("union_") ? "union" : tag.startsWith("lineage_") ? "lineage" : fail(`untagged ${id}/${tag}`);
              const line = carrier?.parent_line || edit.line;
              const name = `v6_${id}_${pop}_${carrier?.kind === "capital" ? "capital_" : ""}${line}`;
              // Each zero-national carrier has one owner. Its amount is rebuilt
              // for this fill-in method; the central payload is not that price.
              const amount = carrier ? row.amount_bn : part.by[finalSpec.allocation];
              dest[name] = (dest[name] || 0) + (side === "receipts" ? -1 : 1) * row.response * amount;
              const parentRow = carrier?.kind === "line" ? evaluation.evaluation[carrier.side === "receipt" ? "receipts" : "spending"].find(x => x.id === line) : row;
              infos[name] = {item: id, path: pop, side: carrier?.side || edit.side, line, national_bn: parentRow.national_bn,
                parent: PARENT[line] || null, rule: ["lane_constants", "source_rounding"].includes(line) ? "per_person" : carrier && carrier.kind !== "line" ? ({capital: "capital", production: "production", nonreporters: "per_person"})[carrier.kind] : "line",
                ...(id === "union_completion" && carrier ? {population_path: "g3plus"} : {}),
                ...(carrier?.kind === "capital" ? {component: line} : {}),
                ...(carrier?.kind === "production" ? {line: "private_wtp_bn"} : {})};
            }
          };
          collect(after, rec, payload, a, setValues);
          collect(after.CASH, cashPayload.meta.items.find(x => x.id === id), cashPayload, ac, cashValues);
          const beforeTotal = sum(Object.values(parts));
          for (const name of new Set([...Object.keys(setValues), ...Object.keys(cashValues)])) {
            const info = infos[name], value = setValues[name] || 0, cash = cashValues[name] || 0;
            if (id !== "coverage" && info.side === "spending" && ["social_security", "medicare"].includes(info.line)) {
              const ss = info.line === "social_security", kept = ss ? 0 : 1 - data.pension_accrual.part_a_share;
              add(`${name}_accrual`, value - kept * cash, {...info, rule: "accrual", contributions: ss ? "oasdi" : "hi"});
              add(`${name}_benefits`, cash, {...info, rule: "benefits"});
              add(`${name}_cash`, -(1 - kept) * cash, {...info, rule: "benefits"});
            } else add(name, value, info);
          }
          if (id === "union_completion") {
            // Observed children now enter native original-line cells, their
            // additive production grid, and the ordinary public-capital keys.
            for (const [label, field] of [["private", "private_wtp_bn"], ["receipts", "induced_receipts_bn"]]) {
              const value = -(a.evaluation[field] - b.evaluation[field]);
              const cash = -(ac.evaluation[field] - bc.evaluation[field]);
              near(value, cash, `child ${field} set/cash agreement`);
              add(`v6_${id}_lineage_production_${label}`, value, {item: id, path: "lineage", side: "production", line: field, national_bn: null, parent: null, rule: "production"});
              cashValues[`child_production_${label}`] = cash;
            }
            for (const component of a.capital.components) {
              const old = b.capital.components.find(c => c.id === component.id);
              const value = component.return_bn - old.return_bn;
              const cash = ac.capital.components.find(c => c.id === component.id).return_bn - bc.capital.components.find(c => c.id === component.id).return_bn;
              near(value, cash, `child ${component.id} capital set/cash agreement`);
              add(`v6_${id}_lineage_capital_${component.id}`, value, {item: id, path: "lineage", side: "capital", line: component.id, component: component.id, national_bn: null, parent: null, rule: "capital"});
              cashValues[`child_capital_${component.id}`] = cash;
            }
          } else {
            near(a.capital.total_bn, b.capital.total_bn, `${id} capital unchanged outside carriers`);
            near(a.evaluation.private_wtp_bn + a.evaluation.induced_receipts_bn, b.evaluation.private_wtp_bn + b.evaluation.induced_receipts_bn, `${id} production unchanged outside carriers`);
          }
          near(sum(Object.values(parts)) - beforeTotal, a.cost_bn - b.cost_bn, `${id} set component closure`);
          near(sum(Object.values(cashValues)), ac.cost_bn - bc.cost_bn, `${id} cash component closure`);
          [before, b, bc] = [after, a, ac];
        }
        methodParts.push(parts); cashTotals.push(bc.cost_bn); fullTotals.push(b.cost_bn);
      }
      const principal = mean(fullTotals), e = block.ends[end];
      near(e.cost_bn + mean(methodParts.map(x => sum(Object.values(x)))), principal, `${concept}/${end} full historical closure`);
      e.cost_bn = principal;
      const allNames = new Set(methodParts.flatMap(x => Object.keys(x)));
      for (const name of allNames) e.additions_bn[name] = mean(methodParts.map(x => x[name] || 0));
      byEnd[end] = {set: principal, cash: mean(cashTotals)};
      near(principal, oracle(block.profile, "adopted")[ei], `${concept}/${end} adopted file`, 1e-4);
      const cashOracle = oracle(block.profile, "cash_set");
      if (cashOracle) near(byEnd[end].cash, cashOracle[ei], `${concept}/${end} cash file`, 1e-4);
      byEnd[end].cash_oracle = cashOracle ? "published main-case cash band" : "native evaluated profile and exact component closure; no published proportional cash row";
      console.log(`PASS ${concept}/${end}: set ${principal}, cash ${byEnd[end].cash}; components 1e-9, bands 1e-4`);
    }
    Object.assign(block.v6_parts, metadata);
    block.v8_gates = byEnd;
  }
  for (const rel of [`${LANE}/package.cjs`, `${LANE}/derived/summary.json`, `${LANE}/derived/main_case_bands.csv`, `${LANE}/derived/corrections.json`, `${LANE}/derived/corrections_cash.json`, `${LANE}/item_union.cjs`, `${LANE}/item_foreign.cjs`, `${LANE}/item_mixed.cjs`, `${LANE}/coverage.cjs`]) data.inputs[rel] = sha(rel);
  for (const name of ["v8_components.cjs", "bridge_memory.py", "coverage_components.py"]) {
    const rel = path.relative(FISCAL, path.join(HERE, name)); data.inputs[rel] = sha(rel);
  }
  if (coverageProfile) data.inputs[path.relative(FISCAL, coverageFile)] = sha(path.relative(FISCAL, coverageFile));
  data.inputs[path.relative(FISCAL, mixedFile)] = sha(path.relative(FISCAL, mixedFile));
  near(data.concepts.net_cost_cbo_informed.ends.low.cost_bn, summary.v8.band_bn[0], "summary low");
  near(data.concepts.net_cost_cbo_informed.ends.high.cost_bn, summary.v8.band_bn[1], "summary high");
  if (!meta.coverage || meta.coverage.stub) fail("coverage remains STUB; no oct15 components written");
  const memory = cp.spawnSync("uv", ["run", "--no-project", "python3", path.join(HERE, "bridge_memory.py"), String(process.pid)],
    {encoding: "utf8", cwd: path.resolve(FISCAL, "../..")});
  if (memory.status !== 0) fail(`physical-memory guard: ${memory.stdout} ${memory.stderr}`);
  console.log(memory.stdout.trim());
  const out = path.resolve(outDir); fs.mkdirSync(out, {recursive: true});
  fs.writeFileSync(path.join(out, "case_components_oct15.json"), JSON.stringify(data, null, 1) + "\n");
}
module.exports = {main};
if (require.main === module) main(process.argv.includes("--out-dir") ? process.argv[process.argv.indexOf("--out-dir") + 1] : path.join(HERE, "derived"));
