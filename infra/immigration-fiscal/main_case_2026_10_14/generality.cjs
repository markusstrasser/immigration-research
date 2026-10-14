/* G3, the new items off: this lane's package, with v6's items and none of v7's, is v6's package.
 *
 * v6's own scripts (main_case_2026_10_07/main_case.cjs, sign_reversal.cjs and lineage_addition.cjs) run unmodified,
 * each in a child process, with their package resolved to this lane's: package.cjs caseOf(OCT05, v6's CANDIDATE) (v7's
 * caseOf with no v7 item, which hands back v6's case) and the module's other exports restricted to v6's registry
 * (REGISTRY and CANDIDATE v6's, caseOf refusing a v7 item), with HERE that lane's directory. Every other require
 * resolves as it does in that lane, except the scripts' own "fs": its writes into that lane's derived/ go to a temporary
 * directory (main_case.cjs and sign_reversal.cjs are also given --out-dir there), and any other write stops the run.
 * The scripts run all their own gates (the adopted bands pinned, the payload, the profiles, the history rows, every
 * variant, the companions, the independent consumer). Their files must equal v6's derived files byte for byte. Nothing
 * is written in either lane but derived/generality.json here.
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
const OCT07 = "main_case_2026_10_07";
const SCRIPTS = [["main_case.cjs", ["--out-dir", "{out}"]], ["sign_reversal.cjs", ["--out-dir", "{out}"]], ["lineage_addition.cjs", []]];
// v6's own gate records: written by its contract.cjs, generality.cjs, zero_items.cjs and api_check.cjs, which this
// check does not run.
const NOT_RUN = ["api_check.json", "contract.json", "generality.json", "zero_items.json"];
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

// Child: run one v6 script with the package swapped. argv: --child <script> <tmp dir> [args]
const argv = process.argv.slice(2);
if (argv[0] === "--child") {
  const [, script, tmp, ...rest] = argv;
  const N = require(path.join(HERE, "package.cjs"));
  const lane = path.join(FISCAL, OCT07);
  const V6REG = N.REGISTRY.filter((it) => !N.NEW_IDS.includes(it.id)), V6CAND = N.CANDIDATE.filter((id) => !N.NEW_IDS.includes(id));
  const caseOf = (B, ids, sel, lineage) => {
    if (ids.some((id) => N.NEW_IDS.includes(id))) throw new Error(`[BLOCKED] generality.cjs: v6's script asks for a v7 item (${ids.join(", ")})`);
    return N.caseOf(B, ids, sel, lineage);
  };
  const base = N.caseOf(N.OCT05, V6CAND);
  if (base.V7_ITEMS || base.V7_IDS) throw new Error("[BLOCKED] generality.cjs: the package carries a v7 item");
  const pkg = Object.assign({}, base, {
    V6: N.V6, REGISTRY: V6REG, CANDIDATE: V6CAND, SLOTS: N.SLOTS, PENSION: N.PENSION, OPEB: N.OPEB, AGE_MIX: N.AGE_MIX, FEES: N.FEES,
    RESERVED_META: N.RESERVED_META, LINEAGE_PAYLOADS: N.LINEAGE_PAYLOADS, COUNT: N.COUNT, LINEAGE_OPTIONS: N.LINEAGE_OPTIONS,
    forItems: N.forItems, caseOf, rebase: N.rebase, checkBuilt: N.checkBuilt, checkLineage: N.checkLineage, HERE: lane,
  });
  // The script's fs: writes into the lane's derived/ land in tmp/derived; a write anywhere else outside tmp stops.
  const out = path.join(tmp, "derived");
  const redirect = (p) => {
    const abs = path.resolve(String(p));
    if (abs === path.join(lane, "derived")) return out;
    if (path.dirname(abs) === path.join(lane, "derived")) return path.join(out, path.basename(abs));
    if (abs === tmp || abs.startsWith(tmp + path.sep)) return abs;
    throw new Error(`[BLOCKED] generality.cjs: the v6 script writes outside its derived/: ${abs}`);
  };
  const fsProxy = Object.assign({}, fs, {
    writeFileSync: (p, ...r) => fs.writeFileSync(redirect(p), ...r),
    mkdirSync: (p, ...r) => fs.mkdirSync(redirect(p), ...r),
  });
  for (const f of ["appendFileSync", "copyFileSync", "renameSync", "rmSync", "unlinkSync", "createWriteStream", "writeFile", "appendFile"]) {
    fsProxy[f] = () => { throw new Error(`[BLOCKED] generality.cjs: the v6 script calls fs.${f}`); };
  }
  const file = path.join(lane, script);
  const mod = new Module(file, module);
  mod.filename = file;
  mod.paths = Module._nodeModulePaths(path.dirname(file));
  const req = mod.require.bind(mod);
  const PKG_FILE = path.join(lane, "package.cjs");
  mod.require = (id) => (id === "./package.cjs" || path.resolve(lane, id) === PKG_FILE ? pkg : id === "fs" ? fsProxy : req(id));
  fs.mkdirSync(out, { recursive: true });
  process.argv = [process.argv[0], file].concat(rest.map((a) => a.replace("{out}", out)));
  mod._compile(fs.readFileSync(file, "utf8"), file);
  return;
}

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "g3_oct07_"));
const runs = [];
let failed = false;
try {
  for (const [script, args] of SCRIPTS) {
    const r = spawnSync(process.execPath, [__filename, "--child", script, tmp].concat(args), { encoding: "utf8", maxBuffer: 1 << 26 });
    const out = (r.stdout || "") + (r.stderr || "");
    const lines = out.split("\n");
    const passes = lines.filter((l) => /^\s+PASS /.test(l)).length, fails = lines.filter((l) => /^\s+FAIL /.test(l)).length;
    // main_case.cjs and sign_reversal.cjs end "all gates passed"; lineage_addition.cjs prints its gate count and the file.
    const done = /all gates passed/.test(out) || (script === "lineage_addition.cjs" && /gates pass\]/.test(out) && /wrote /.test(out));
    runs.push({ script: `${OCT07}/${script}`, exit_code: r.status, gates_passed: passes, gates_failed: fails, all_gates_passed: done });
    console.log(`[${OCT07}/${script} on this package, the new items off] exit ${r.status}, ${passes} gates passed, ${fails} failed`);
    if (r.status !== 0 || fails || !done) {
      failed = true;
      console.log(lines.filter((l) => /FAIL|BLOCKED|Error/.test(l)).slice(0, 20).join("\n"));
    }
  }
  const want = fs.readdirSync(path.join(FISCAL, OCT07, "derived")).filter((f) => !NOT_RUN.includes(f)).sort();
  const got = fs.existsSync(path.join(tmp, "derived")) ? fs.readdirSync(path.join(tmp, "derived")).sort() : [];
  const files = [...new Set(want.concat(got))].sort().map((f) => {
    const a = path.join(FISCAL, OCT07, "derived", f), b = path.join(tmp, "derived", f);
    if (!fs.existsSync(a) || !fs.existsSync(b)) return { file: f, identical: false, difference: fs.existsSync(a) ? "not written" : "written, not in v6's lane" };
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
    gate: "G3: with the new items off (v6's items, none of v7's), this package reproduces v6's derived outputs byte for byte",
    pass,
    method: "v6's main_case.cjs, sign_reversal.cjs and lineage_addition.cjs, unmodified, each run in a child process with its package (require(\"./package.cjs\"), or the lane's package.cjs by path) resolved to package.cjs caseOf(OCT05, v6's CANDIDATE) and the module's exports restricted to v6's registry, with HERE that lane's directory; the scripts' fs sends their writes into that lane's derived/ to a temporary directory and stops any other write; every other require resolves as in that lane",
    not_compared: NOT_RUN.map((f) => `${OCT07}/derived/${f} (that lane's own gate record; its script is not run here)`),
    payload: { file: `${OCT07}/derived/corrections.json`, sha256: sha(fs.readFileSync(path.join(FISCAL, OCT07, "derived", "corrections.json"))) },
    runs, files,
  };
  fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
  fs.writeFileSync(path.join(HERE, "derived", "generality.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(pass ? "G3 PASS: with the new items off every v6 derived file reproduces byte for byte" : "G3 FAIL");
  if (!pass) process.exitCode = 1;
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
