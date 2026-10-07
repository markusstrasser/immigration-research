/* G1's identity: with no item, this lane's own scripts are v5's. main_case.cjs and sign_reversal.cjs run here with
 * --items none (package.cjs caseOf(OCT05, []): v5's payloads, unstamped, and v5's API under forItems), each in a child
 * process writing to a temporary directory, and every file they write must equal v5's derived file byte for byte
 * (main_case_2026_10_05/derived: main_case_bands.csv, components.csv, per_spec.csv, summary.json, corrections.json,
 * corrections_cash.json and sign_reversal.csv). The item code is then all that separates this lane's outputs from v5's.
 * Nothing is written in either lane but derived/zero_items.json here.
 *
 * Run from anywhere (after main_case.cjs): node zero_items.cjs -> derived/zero_items.json (exit 1 if a script fails or
 * a file differs)
 */
"use strict";
const fs = require("fs");
const os = require("os");
const path = require("path");
const crypto = require("crypto");
const { spawnSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const OCT05 = "main_case_2026_10_05";
const SCRIPTS = ["main_case.cjs", "sign_reversal.cjs"];
// v5's own gate records, which these scripts do not write.
const NOT_RUN = ["api_check.json", "contract.json", "generality.json"];
const sha = (buf) => crypto.createHash("sha256").update(buf).digest("hex");

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "g1_zero_items_"));
const runs = [];
let failed = false;
try {
  const out = path.join(tmp, "derived");
  fs.mkdirSync(out);
  for (const script of SCRIPTS) {
    const r = spawnSync(process.execPath, [path.join(HERE, script), "--items", "none", "--out-dir", out], { encoding: "utf8", maxBuffer: 1 << 26 });
    const text = (r.stdout || "") + (r.stderr || "");
    const lines = text.split("\n");
    const passes = lines.filter((l) => /^\s+PASS /.test(l)).length, fails = lines.filter((l) => /^\s+FAIL /.test(l)).length;
    runs.push({ script: `${path.basename(HERE)}/${script} --items none`, exit_code: r.status, gates_passed: passes, gates_failed: fails, all_gates_passed: /all gates passed/.test(text) });
    console.log(`[${script} --items none] exit ${r.status}, ${passes} gates passed, ${fails} failed`);
    if (r.status !== 0 || fails || !/all gates passed/.test(text)) {
      failed = true;
      console.log(lines.filter((l) => /FAIL|BLOCKED|Error/.test(l)).slice(0, 20).join("\n"));
    }
  }
  const want = fs.readdirSync(path.join(FISCAL, OCT05, "derived")).filter((f) => !NOT_RUN.includes(f)).sort();
  const got = fs.readdirSync(out).sort();
  const files = [...new Set(want.concat(got))].sort().map((f) => {
    const a = path.join(FISCAL, OCT05, "derived", f), b = path.join(out, f);
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
    gate: "G1, the identity: with no item, this lane's main_case.cjs and sign_reversal.cjs write v5's derived files byte for byte",
    pass,
    method: "each script run in a child process with --items none --out-dir <temporary directory>: package.cjs caseOf(OCT05, []), v5's payloads unstamped; the files compared with main_case_2026_10_05/derived byte for byte",
    not_compared: NOT_RUN.map((f) => `${OCT05}/derived/${f} (v5's own gate record; these scripts do not write it)`),
    runs, files,
  };
  fs.mkdirSync(path.join(HERE, "derived"), { recursive: true });
  fs.writeFileSync(path.join(HERE, "derived", "zero_items.json"), JSON.stringify(record, null, 1) + "\n");
  console.log(pass ? "G1 identity PASS: with no item every file this lane's scripts write is v5's, byte for byte" : "G1 identity FAIL");
  if (!pass) process.exitCode = 1;
} finally {
  fs.rmSync(tmp, { recursive: true, force: true });
}
