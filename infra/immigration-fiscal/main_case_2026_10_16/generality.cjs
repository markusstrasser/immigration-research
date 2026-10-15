/* G3: run v8's case scripts unmodified on v9's old-item route. Redirect only their
 * derived writes, retain original require.main behavior, and compare exact bytes.
 * Immutable bridge inputs are listed separately from executed producer outputs.
 * Run: node generality.cjs -> derived/generality.json (exit 1 on any difference).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const Module = require("module");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const OCT14 = "main_case_2026_10_15";
const SCRIPTS = [["item_union.cjs", []], ["main_case.cjs", ["--out-dir", "{out}"]], ["sign_reversal.cjs", []], ["lineage_addition.cjs", []]];
// v8's own gate records: written by contract, generality, coverage_check and api_check, which this
// check does not run.
const NOT_RUN = ["api_check.json", "contract.json", "generality.json", "coverage_check.json"];
// These are immutable Python-produced bridge inputs, not products of the API being tested.
// Their copied bytes are checked and classified separately from executed case producers.
const INPUTS = ["union_people.json", "union_credit_parts.json", "mixed_overlap.json"];
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

// Child: run one v8 script with the package swapped. argv: --child <script> <tmp dir> [args]
const argv = process.argv.slice(2);
if (argv[0] === "--child") {
  const started = process.hrtime.bigint();
  const [, script, tmp, ...rest] = argv;
  const N = require(path.join(HERE, "package.cjs"));
  const lane = path.join(FISCAL, OCT14);
  const V7 = require(path.join(lane, "package.cjs"));
  const V7REG = V7.REGISTRY, V7CAND = V7.CANDIDATE;
  const oldIds = new Set(V7REG.map((it) => it.id));
  const caseOf = (B, ids, sel, lineage) => {
    if (ids.some((id) => !oldIds.has(id))) throw new Error(`[BLOCKED] generality.cjs: v8's script asks for an item outside its own registry (${ids.join(", ")})`);
    return N.caseOf(B, ids, sel, lineage);
  };
  const base = N.caseOf(N.OCT05, V7CAND);
  if (JSON.stringify(base.ITEM_IDS) !== JSON.stringify(V7.ITEM_IDS) || JSON.stringify(base.correctionsPayload()) !== JSON.stringify(V7.correctionsPayload())
    || JSON.stringify(base.CASH.correctionsPayload()) !== JSON.stringify(V7.CASH.correctionsPayload())) throw new Error("[BLOCKED] generality.cjs: caseOf(OCT05, V8.CANDIDATE) differs from v8's IDs or payloads");
  // No v9-only export may enter: keys exactly match v8's original module. Values come from the new route and
  // inherited module exports, except the original registry, new-v8 IDs, identity and guarded caseOf.
  const pkg = Object.fromEntries(Object.keys(V7).map((k) => [k, Object.prototype.hasOwnProperty.call(base, k) ? base[k] : N[k]]));
  Object.assign(pkg, { REGISTRY: V7REG, CANDIDATE: V7CAND, NEW_IDS: V7.NEW_IDS, V8: V7.V8, V7_PACKAGE: V7.V7_PACKAGE, HERE: lane, caseOf });
  if (JSON.stringify(Object.keys(pkg).sort()) !== JSON.stringify(Object.keys(V7).sort())) throw new Error("[BLOCKED] generality.cjs: injected export symbols differ from v8's");
  const missing = Object.keys(pkg).filter((k) => pkg[k] === undefined && V7[k] !== undefined);
  if (missing.length) throw new Error(`[BLOCKED] generality.cjs: missing inherited exports ${missing.join(", ")}`);
  // The script's fs: writes into the lane's derived/ land in tmp/derived; a write anywhere else outside tmp stops.
  const out = path.join(tmp, "derived");
  const redirect = (p) => {
    const abs = path.resolve(String(p));
    if (abs === path.join(lane, "derived")) return out;
    if (path.dirname(abs) === path.join(lane, "derived")) return path.join(out, path.basename(abs));
    if (abs === tmp || abs.startsWith(tmp + path.sep)) return abs;
    throw new Error(`[BLOCKED] generality.cjs: the v8 script writes outside its derived/: ${abs}`);
  };
  const fsProxy = Object.assign({}, fs, {
    writeFileSync: (p, ...r) => fs.writeFileSync(redirect(p), ...r),
    mkdirSync: (p, ...r) => fs.mkdirSync(redirect(p), ...r),
  });
  for (const f of ["appendFileSync", "copyFileSync", "renameSync", "rmSync", "unlinkSync", "createWriteStream", "writeFile", "appendFile", "open", "openSync", "write", "writeSync", "truncate", "truncateSync", "ftruncate", "ftruncateSync", "mkdir", "rmdir", "rmdirSync", "cp", "cpSync", "chmod", "chmodSync", "chown", "chownSync", "symlink", "symlinkSync", "link", "linkSync", "utimes", "utimesSync"]) {
    fsProxy[f] = () => { throw new Error(`[BLOCKED] generality.cjs: the v8 script calls fs.${f}`); };
  }
  const promises = Object.assign({}, fs.promises);
  for (const f of Object.keys(promises)) if (!/^(access|constants|lstat|opendir|readFile|readdir|readlink|realpath|stat|statfs|watch)$/.test(f)) promises[f] = () => { throw new Error(`[BLOCKED] generality.cjs: v8 calls fs.promises.${f}`); };
  fsProxy.promises = promises;
  const file = path.join(lane, script);
  const mod = new Module(file, module);
  mod.filename = file;
  mod.paths = Module._nodeModulePaths(path.dirname(file));
  const req = mod.require.bind(mod);
  const PKG_FILE = path.join(lane, "package.cjs");
  mod.require = (id) => (id === "./package.cjs" || path.resolve(lane, id) === PKG_FILE ? pkg : ["fs", "node:fs"].includes(id) ? fsProxy : req(id));
  fs.mkdirSync(out, { recursive: true });
  process.argv = [process.argv[0], file].concat(rest.map((a) => a.replace("{out}", out)));
  process.mainModule = mod; // _compile's require.main must see the executed script.
  mod._compile(fs.readFileSync(file, "utf8"), file);
  const maxRSS = process.resourceUsage().maxRSS;
  console.log(`[resources] ${script}: elapsed_seconds=${(Number(process.hrtime.bigint() - started) / 1e9).toFixed(3)}, process.resourceUsage().maxRSS=${maxRSS} KiB`);
  require("./memory_guard.cjs").requireWithinBudget(`G3 ${script}`);
  return;
}

const tmp = path.join(HERE, "_cache", "g3");
fs.rmSync(tmp, { recursive: true, force: true });
fs.mkdirSync(tmp, { recursive: true });
const runs = [];
let failed = false;
try {
  for (const [script, args] of SCRIPTS) {
    const profileArgs = process.env.G3_PROFILE === "1" ? ["--cpu-prof", `--cpu-prof-dir=${tmp}`, `--cpu-prof-name=${script}.cpuprofile`] : [];
    // Runtime module copies preserve original source bytes, bounding only the
    // source's raw pricing memo; no old file, original module or cache is patched.
    const r = spawnSync(process.execPath, ["--max-old-space-size=1536"].concat(profileArgs,[__filename, "--child", script, tmp], args), { env:{...process.env,V9_NEW_ITEMS:"0",V9_CASE_CACHE:"0"}, encoding: "utf8", maxBuffer: 1 << 26 });
    const out = (r.stdout || "") + (r.stderr || "");
    fs.writeFileSync(path.join(tmp, `${script}.log`), out);
    const lines = out.split("\n");
    const passes = lines.filter((l) => /^\s*PASS /.test(l)).length, fails = lines.filter((l) => /^\s*FAIL /.test(l)).length;
    // main_case.cjs and sign_reversal.cjs end "all gates passed"; lineage_addition.cjs prints its gate count and the file.
    const done = /all gates passed/.test(out) || (script === "lineage_addition.cjs" && /gates pass\]/.test(out) && /wrote /.test(out)) || (script === "item_union.cjs" && /"source_gates":\s*[1-9]/.test(out) && /"option_gates":\s*[1-9]/.test(out));
    const stub = lines.some((l) => l.startsWith("[STUB]"));
    runs.push({ script: `${OCT14}/${script}`, sha256: sha(fs.readFileSync(path.join(FISCAL, OCT14, script))), exit_code: r.status, gates_passed: passes, gates_failed: fails, all_gates_passed: done, stub });
    if (stub) console.log("[STUB] G3 loaded the coverage stub during module initialization; tested case coverage is OFF");
    for (const l of lines.filter((x) => x.startsWith("[resources]"))) console.log(l);
    console.log(`[${OCT14}/${script} on this package, the new items off] exit ${r.status}, ${passes} gates passed, ${fails} failed`);
    if (r.status !== 0 || fails || !done) {
      failed = true;
      console.log(lines.filter((l) => /FAIL|BLOCKED|Error/.test(l)).slice(0, 20).join("\n"));
    }
  }
  const inputRecords = INPUTS.map(file => {
    const source=path.join(FISCAL,OCT14,"derived",file),target=path.join(tmp,"derived",file),bytes=fs.readFileSync(source);
    fs.writeFileSync(target,bytes);
    return {file,classification:"immutable bridge input; copied, producer not executed",identical:Buffer.compare(bytes,fs.readFileSync(target))===0,sha256:sha(bytes),bytes:bytes.length};
  });
  const want = fs.readdirSync(path.join(FISCAL, OCT14, "derived")).filter((f) => !NOT_RUN.includes(f)).sort();
  const got = fs.existsSync(path.join(tmp, "derived")) ? fs.readdirSync(path.join(tmp, "derived")).sort() : [];
  const files = [...new Set(want.concat(got))].sort().map((f) => {
    const a = path.join(FISCAL, OCT14, "derived", f), b = path.join(tmp, "derived", f);
    if (!fs.existsSync(a) || !fs.existsSync(b)) return { file: f, identical: false, difference: fs.existsSync(a) ? "not written" : "written, not in v8's lane" };
    const x = fs.readFileSync(a), y = fs.readFileSync(b);
    const same = Buffer.compare(x, y) === 0;
    const rec = { file: f, classification:INPUTS.includes(f)?"immutable bridge input; copied, producer not executed":"executed case producer output", identical: same, bytes: x.length, sha256: sha(x) };
    if (!same) {
      const xl = x.toString("utf8").split("\n"), yl = y.toString("utf8").split("\n");
      const diffs = [];
      for (let i = 0; i < Math.max(xl.length, yl.length) && diffs.length < 10; i += 1) if (xl[i] !== yl[i]) diffs.push({ line: i + 1, oct15: xl[i], here: yl[i] });
      Object.assign(rec, { bytes_here: y.length, sha256_here: sha(y), lines_differing: diffs });
    }
    return rec;
  });
  for (const f of files) console.log(`  ${f.identical ? "PASS" : "FAIL"} ${f.file}: ${f.identical ? `identical (${f.bytes} bytes)` : JSON.stringify(f.difference || f.lines_differing).slice(0, 600)}`);
  const pass = !failed && files.length === want.length && files.every((f) => f.identical);
  const record = {
    gate: "G3: unmodified v8 scripts on v9 with new items off reproduce v8 outputs byte for byte",
    pass,
    stub: runs.some((r) => r.stub),
    verdict: `${runs.some((r) => r.stub) ? "STUB: " : ""}${pass ? "PASS" : "FAIL"}`,
    method: "v8's item_union.cjs, main_case.cjs, sign_reversal.cjs and lineage_addition.cjs, unmodified, each run in a child with package.cjs resolved to v9 caseOf(OCT05, V8.CANDIDATE), exports restricted to v8's original symbols, registry and identity; fs redirects derived writes under v9/_cache/g3/derived and rejects all other writes. Python-produced bridge inputs are copied and hash-checked separately, not counted as executed producers.",
    inputs:inputRecords,
    executed_outputs:files.filter(f=>!INPUTS.includes(f.file)).length,
    child_old_space_limit_mib:1536,
    case_cache:false,
    runtime_adapter:{scope:"isolated original v8/package and item_union source bytes; raw unit_models memo retained at most 2; matching evicted capture Module unlinked from isolated parent.children by exact unitModels identity; active returned values/model references and scalar memo unchanged; original modules and caches untouched",anchor:"const keyedRatesCache = new Map();",module_anchor:"const mod = new Module(file, module); mod.filename = file;",anchor_matches:1,raw_cache_entries:2,sources:["package.cjs","item_union.cjs"].map(file=>({file:`${OCT14}/${file}`,sha256:sha(fs.readFileSync(path.join(FISCAL,OCT14,file)))}))},
    memory_metric:"canonical live lifetime peak physical footprint; Node maxRSS diagnostic only",
    not_compared: NOT_RUN.map((f) => `${OCT14}/derived/${f} (that lane's own gate record; its script is not run here)`),
    payload: { file: `${OCT14}/derived/corrections.json`, sha256: sha(fs.readFileSync(path.join(FISCAL, OCT14, "derived", "corrections.json"))) },
    runs, files,
  };
  fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
  fs.writeFileSync(path.join(HERE, "derived", "generality.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(pass ? "G3 PASS: unmodified v8 scripts reproduce their outputs byte for byte; bridge inputs classified separately" : "G3 FAIL");
  if (!pass) process.exitCode = 1;
} finally {
  // Retain probe outputs and logs under this lane for inspection.
}
