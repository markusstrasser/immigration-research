/* G3, the new items off: this lane's package, with v7's items and none of v8's, is v7's package.
 *
 * v7's own scripts (main_case_2026_10_14/main_case.cjs, sign_reversal.cjs and lineage_addition.cjs) run unmodified,
 * each in a child process, with their package resolved to this lane's: package.cjs caseOf(OCT05, v7's CANDIDATE) (v7's
 * caseOf with no v8 item, which hands back v7's case) and the module's exports restricted to exactly v7's symbols
 * (REGISTRY, CANDIDATE and NEW_IDS v7's, caseOf refusing a v8 item), with HERE that lane's directory. Every other require
 * resolves as it does in that lane, except the scripts' own "fs": its writes into that lane's derived/ go to this
 * lane's _cache/g3/derived (main_case.cjs and sign_reversal.cjs also get --out-dir there); any other write stops.
 * The scripts run all their own gates (the adopted bands pinned, the payload, the profiles, the history rows, every
 * variant, the companions, the independent consumer). Their files must equal v7's derived files byte for byte. Nothing
 * is written outside this lane's _cache/g3 and derived/generality.json.
 *
 * Run from anywhere: node generality.cjs -> derived/generality.json (exit 1 if a script fails or a file differs)
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const Module = require("module");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const OCT14 = "main_case_2026_10_14";
const SCRIPTS = [["main_case.cjs", ["--out-dir", "{out}"]], ["sign_reversal.cjs", ["--out-dir", "{out}"]], ["lineage_addition.cjs", []]];
// v7's own gate records: written by its contract.cjs, generality.cjs, zero_items.cjs and api_check.cjs, which this
// check does not run.
const NOT_RUN = ["api_check.json", "contract.json", "generality.json", "zero_items.json"];
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

// Child: run one v7 script with the package swapped. argv: --child <script> <tmp dir> [args]
const argv = process.argv.slice(2);
if (argv[0] === "--child") {
  const started = process.hrtime.bigint();
  const [, script, tmp, ...rest] = argv;
  const N = require(path.join(HERE, "package.cjs"));
  if (N.correctionsPayload().meta.coverage?.stub) console.log("[STUB] v8 module initialized with coverage stub; G3's tested case has every v8 item, including coverage, OFF");
  const lane = path.join(FISCAL, OCT14);
  const V7 = require(path.join(lane, "package.cjs"));
  const V7REG = V7.REGISTRY, V7CAND = V7.CANDIDATE;
  const oldIds = new Set(V7REG.map((it) => it.id));
  const caseOf = (B, ids, sel, lineage) => {
    if (ids.some((id) => !oldIds.has(id))) throw new Error(`[BLOCKED] generality.cjs: v7's script asks for an item outside its own registry (${ids.join(", ")})`);
    return N.caseOf(B, ids, sel, lineage);
  };
  const base = N.caseOf(N.OCT05, V7CAND);
  if (JSON.stringify(base.ITEM_IDS) !== JSON.stringify(V7.ITEM_IDS) || JSON.stringify(base.correctionsPayload()) !== JSON.stringify(V7.correctionsPayload())
    || JSON.stringify(base.CASH.correctionsPayload()) !== JSON.stringify(V7.CASH.correctionsPayload())) throw new Error("[BLOCKED] generality.cjs: caseOf(OCT05, V7.CANDIDATE) differs from v7's IDs or payloads");
  // No v8 export may enter: the keys are exactly those of v7's original module. Values come from the new route and
  // its inherited module exports, except the original registry, new-v7 IDs, identity and guarded caseOf.
  const pkg = Object.fromEntries(Object.keys(V7).map((k) => [k, Object.prototype.hasOwnProperty.call(base, k) ? base[k] : N[k]]));
  Object.assign(pkg, { REGISTRY: V7REG, CANDIDATE: V7CAND, NEW_IDS: V7.NEW_IDS, V7: V7.V7, HERE: lane, caseOf });
  if (JSON.stringify(Object.keys(pkg).sort()) !== JSON.stringify(Object.keys(V7).sort())) throw new Error("[BLOCKED] generality.cjs: injected export symbols differ from v7's");
  const missing = Object.keys(pkg).filter((k) => pkg[k] === undefined && V7[k] !== undefined);
  if (missing.length) throw new Error(`[BLOCKED] generality.cjs: missing inherited exports ${missing.join(", ")}`);
  // The script's fs: writes into the lane's derived/ land in tmp/derived; a write anywhere else outside tmp stops.
  const out = path.join(tmp, "derived");
  const redirect = (p) => {
    const abs = path.resolve(String(p));
    if (abs === path.join(lane, "derived")) return out;
    if (path.dirname(abs) === path.join(lane, "derived")) return path.join(out, path.basename(abs));
    if (abs === tmp || abs.startsWith(tmp + path.sep)) return abs;
    throw new Error(`[BLOCKED] generality.cjs: the v7 script writes outside its derived/: ${abs}`);
  };
  const fsProxy = Object.assign({}, fs, {
    writeFileSync: (p, ...r) => fs.writeFileSync(redirect(p), ...r),
    mkdirSync: (p, ...r) => fs.mkdirSync(redirect(p), ...r),
  });
  for (const f of ["appendFileSync", "copyFileSync", "renameSync", "rmSync", "unlinkSync", "createWriteStream", "writeFile", "appendFile", "open", "openSync", "write", "writeSync", "truncate", "truncateSync", "ftruncate", "ftruncateSync", "mkdir", "rmdir", "rmdirSync", "cp", "cpSync", "chmod", "chmodSync", "chown", "chownSync", "symlink", "symlinkSync", "link", "linkSync", "utimes", "utimesSync"]) {
    fsProxy[f] = () => { throw new Error(`[BLOCKED] generality.cjs: the v7 script calls fs.${f}`); };
  }
  const promises = Object.assign({}, fs.promises);
  for (const f of Object.keys(promises)) if (!/^(access|constants|lstat|opendir|readFile|readdir|readlink|realpath|stat|statfs|watch)$/.test(f)) promises[f] = () => { throw new Error(`[BLOCKED] generality.cjs: v7 calls fs.promises.${f}`); };
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
  mod._compile(fs.readFileSync(file, "utf8"), file);
  const maxRSS = process.resourceUsage().maxRSS;
  console.log(`[resources] ${script}: elapsed_seconds=${(Number(process.hrtime.bigint() - started) / 1e9).toFixed(3)}, process.resourceUsage().maxRSS=${maxRSS} KiB`);
  if (maxRSS * 1024 > 2.5e9) throw new Error(`[BLOCKED] generality.cjs: ${script} exceeds the 2.5 GB memory budget`);
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
    const r = spawnSync(process.execPath, profileArgs.concat([__filename, "--child", script, tmp], args), { encoding: "utf8", maxBuffer: 1 << 26 });
    const out = (r.stdout || "") + (r.stderr || "");
    fs.writeFileSync(path.join(tmp, `${script}.log`), out);
    const lines = out.split("\n");
    const passes = lines.filter((l) => /^\s+PASS /.test(l)).length, fails = lines.filter((l) => /^\s+FAIL /.test(l)).length;
    // main_case.cjs and sign_reversal.cjs end "all gates passed"; lineage_addition.cjs prints its gate count and the file.
    const done = /all gates passed/.test(out) || (script === "lineage_addition.cjs" && /gates pass\]/.test(out) && /wrote /.test(out));
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
  const want = fs.readdirSync(path.join(FISCAL, OCT14, "derived")).filter((f) => !NOT_RUN.includes(f)).sort();
  const got = fs.existsSync(path.join(tmp, "derived")) ? fs.readdirSync(path.join(tmp, "derived")).sort() : [];
  const files = [...new Set(want.concat(got))].sort().map((f) => {
    const a = path.join(FISCAL, OCT14, "derived", f), b = path.join(tmp, "derived", f);
    if (!fs.existsSync(a) || !fs.existsSync(b)) return { file: f, identical: false, difference: fs.existsSync(a) ? "not written" : "written, not in v7's lane" };
    const x = fs.readFileSync(a), y = fs.readFileSync(b);
    const same = Buffer.compare(x, y) === 0;
    const rec = { file: f, identical: same, bytes: x.length, sha256: sha(x) };
    if (!same) {
      const xl = x.toString("utf8").split("\n"), yl = y.toString("utf8").split("\n");
      const diffs = [];
      for (let i = 0; i < Math.max(xl.length, yl.length) && diffs.length < 10; i += 1) if (xl[i] !== yl[i]) diffs.push({ line: i + 1, oct07: xl[i], here: yl[i] });
      Object.assign(rec, { bytes_here: y.length, sha256_here: sha(y), lines_differing: diffs });
    }
    return rec;
  });
  for (const f of files) console.log(`  ${f.identical ? "PASS" : "FAIL"} ${f.file}: ${f.identical ? `identical (${f.bytes} bytes)` : JSON.stringify(f.difference || f.lines_differing).slice(0, 600)}`);
  const pass = !failed && files.length === want.length && files.every((f) => f.identical);
  const record = {
    gate: "G3: with the new items off (v7's items, none of v8's), this package reproduces v7's derived outputs byte for byte",
    pass,
    stub: runs.some((r) => r.stub),
    verdict: `${runs.some((r) => r.stub) ? "STUB: " : ""}${pass ? "PASS" : "FAIL"}`,
    method: "v7's main_case.cjs, sign_reversal.cjs and lineage_addition.cjs, unmodified, each run in a child process with its package resolved to v8 package.cjs caseOf(OCT05, V7.CANDIDATE), the module's exports restricted to exactly v7's original symbols, its registry and identity; the scripts' fs redirects derived writes into main_case_2026_10_15/_cache/g3/derived and stops any other write; every other require resolves as in v7",
    not_compared: NOT_RUN.map((f) => `${OCT14}/derived/${f} (that lane's own gate record; its script is not run here)`),
    payload: { file: `${OCT14}/derived/corrections.json`, sha256: sha(fs.readFileSync(path.join(FISCAL, OCT14, "derived", "corrections.json"))) },
    runs, files,
  };
  fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
  fs.writeFileSync(path.join(HERE, "derived", "generality.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(pass ? "G3 PASS: with the new items off every v7 derived file reproduces byte for byte" : "G3 FAIL");
  if (!pass) process.exitCode = 1;
} finally {
  // Retain probe outputs and logs under this lane for inspection.
}
