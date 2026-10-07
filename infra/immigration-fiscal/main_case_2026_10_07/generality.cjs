/* G3, the items off: this lane's package, with no item, is v5's package.
 *
 * v5's own scripts (main_case_2026_10_05/main_case.cjs and sign_reversal.cjs) run unmodified, each in a child process,
 * with their require("./package.cjs") resolved to package.cjs caseOf(OCT05, []): this lane's API (forItems' models,
 * evalPackage, central, payloadModel and correctionsPayload, and v5's API under them) with no item, v5's payloads, and
 * HERE that lane's directory. Every other require resolves as it does in that lane, except the scripts' own "fs": its
 * writes into that lane's derived/ go to a temporary directory (main_case.cjs is also given --out-dir there), and any
 * other write stops the run. The scripts run all their own gates (the lineage lane's bands, the payload, the profiles,
 * the history rows, the items of v4, every variant against candidate v4's package, the independent consumer). Their
 * files must equal v5's derived files byte for byte. Nothing is written in either lane but derived/generality.json here.
 *
 * Run from anywhere: node generality.cjs -> derived/generality.json (exit 1 if a script fails or a file differs)
 */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");
const Module = require("module");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const OCT05 = "main_case_2026_10_05";
const SCRIPTS = ["main_case.cjs", "sign_reversal.cjs"];
// v5's own gate records: written by its contract.cjs, generality.cjs and api_check.cjs, which this check does not run.
const NOT_RUN = ["api_check.json", "contract.json", "generality.json"];
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

// Child: run one v5 script with the package swapped. argv: --child <script> <tmp dir>
const argv = process.argv.slice(2);
if (argv[0] === "--child") {
  const [, script, tmp] = argv;
  const N = require(path.join(HERE, "package.cjs"));
  const lane = path.join(FISCAL, OCT05);
  const pkg = Object.assign({}, N.caseOf(N.OCT05, []), { HERE: lane });
  if (pkg.CASE_ITEMS.length || pkg.CASH.CASE_ITEMS.length) throw new Error("[BLOCKED] generality.cjs: the package carries items");
  // The script's fs: writes into the lane's derived/ land in tmp/derived; a write anywhere else outside tmp stops.
  const out = path.join(tmp, "derived");
  const redirect = (p) => {
    const abs = path.resolve(String(p));
    if (abs === path.join(lane, "derived")) return out;
    if (path.dirname(abs) === path.join(lane, "derived")) return path.join(out, path.basename(abs));
    if (abs === tmp || abs.startsWith(tmp + path.sep)) return abs;
    throw new Error(`[BLOCKED] generality.cjs: the v5 script writes outside its derived/: ${abs}`);
  };
  const fsProxy = Object.assign({}, fs, {
    writeFileSync: (p, ...rest) => fs.writeFileSync(redirect(p), ...rest),
    mkdirSync: (p, ...rest) => fs.mkdirSync(redirect(p), ...rest),
  });
  for (const f of ["appendFileSync", "copyFileSync", "renameSync", "rmSync", "unlinkSync", "createWriteStream", "writeFile", "appendFile"]) {
    fsProxy[f] = () => { throw new Error(`[BLOCKED] generality.cjs: the v5 script calls fs.${f}`); };
  }
  const file = path.join(lane, script);
  const mod = new Module(file, module);
  mod.filename = file;
  mod.paths = Module._nodeModulePaths(path.dirname(file));
  const req = mod.require.bind(mod);
  mod.require = (id) => (id === "./package.cjs" ? pkg : id === "fs" ? fsProxy : req(id));
  process.argv = [process.argv[0], file, "--out-dir", out];
  mod._compile(fs.readFileSync(file, "utf8"), file);
  return;
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "g3_oct05_"));
const runs = [];
let failed = false;
try {
  for (const script of SCRIPTS) {
    const r = spawnSync(process.execPath, [__filename, "--child", script, tmp], { encoding: "utf8", maxBuffer: 1 << 26 });
    const out = (r.stdout || "") + (r.stderr || "");
    const lines = out.split("\n");
    const passes = lines.filter((l) => /^\s+PASS /.test(l)).length, fails = lines.filter((l) => /^\s+FAIL /.test(l)).length;
    runs.push({ script: `${OCT05}/${script}`, exit_code: r.status, gates_passed: passes, gates_failed: fails, all_gates_passed: /all gates passed/.test(out) });
    console.log(`[${OCT05}/${script} on this package, the items off] exit ${r.status}, ${passes} gates passed, ${fails} failed`);
    if (r.status !== 0 || fails || !/all gates passed/.test(out)) {
      failed = true;
      console.log(lines.filter((l) => /FAIL|BLOCKED|Error/.test(l)).slice(0, 20).join("\n"));
    }
  }
  const want = fs.readdirSync(path.join(FISCAL, OCT05, "derived")).filter((f) => !NOT_RUN.includes(f)).sort();
  const got = fs.existsSync(path.join(tmp, "derived")) ? fs.readdirSync(path.join(tmp, "derived")).sort() : [];
  const files = [...new Set(want.concat(got))].sort().map((f) => {
    const a = path.join(FISCAL, OCT05, "derived", f), b = path.join(tmp, "derived", f);
    if (!fs.existsSync(a) || !fs.existsSync(b)) return { file: f, identical: false, difference: fs.existsSync(a) ? "not written" : "written, not in v5's lane" };
    const x = fs.readFileSync(a), y = fs.readFileSync(b);
    const same = Buffer.compare(x, y) === 0;
    const rec = { file: f, identical: same, bytes: x.length, sha256: sha(x) };
    if (!same) {
      const xl = x.toString("utf8").split("\n"), yl = y.toString("utf8").split("\n");
      const diffs = [];
      for (let i = 0; i < Math.max(xl.length, yl.length) && diffs.length < 10; i += 1) if (xl[i] !== yl[i]) diffs.push({ line: i + 1, oct05: xl[i], here: yl[i] });
      Object.assign(rec, { bytes_here: y.length, sha256_here: sha(y), lines_differing: diffs });
    }
    return rec;
  });
  for (const f of files) console.log(`  ${f.identical ? "PASS" : "FAIL"} ${f.file}: ${f.identical ? `identical (${f.bytes} bytes)` : JSON.stringify(f.difference || f.lines_differing)}`);
  const pass = !failed && files.length === want.length && files.every((f) => f.identical);
  const record = {
    gate: "G3: with the items off (no item: v5's payloads as the case), this package reproduces v5's derived outputs byte for byte",
    pass,
    method: "v5's main_case.cjs and sign_reversal.cjs, unmodified, each run in a child process with require(\"./package.cjs\") resolved to package.cjs caseOf(OCT05, []) with HERE that lane's directory; the scripts' fs sends their writes into that lane's derived/ to a temporary directory and stops any other write; every other require resolves as in that lane",
    not_compared: NOT_RUN.map((f) => `${OCT05}/derived/${f} (that lane's own gate record; its script is not run here)`),
    payload: { file: `${OCT05}/derived/corrections.json`, sha256: sha(fs.readFileSync(path.join(FISCAL, OCT05, "derived", "corrections.json"))) },
    runs, files,
  };
  fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
  fs.writeFileSync(path.join(HERE, "derived", "generality.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(pass ? "G3 PASS: with the items off every v5 derived file reproduces byte for byte" : "G3 FAIL");
  if (!pass) process.exitCode = 1;
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
