/* Preload for running another lane's script without writing into it.
 * Intercepts fs.writeFileSync and fs.mkdirSync for paths under NO_WRITE_ROOT: nothing is written;
 * each intercepted write is compared with the file already on disk, and the comparison is appended
 * to NO_WRITE_REPORT (a JSON-lines file inside this lane).
 */
"use strict";
const fs = require("fs");
const path = require("path");

const root = path.resolve(process.env.NO_WRITE_ROOT || "/nonexistent");
const report = process.env.NO_WRITE_REPORT;
const realWrite = fs.writeFileSync.bind(fs);
const realMkdir = fs.mkdirSync.bind(fs);
const realAppend = fs.appendFileSync.bind(fs);

function inside(p) {
  const abs = path.resolve(String(p));
  return abs === root || abs.startsWith(root + path.sep);
}

fs.writeFileSync = function (p, data, options) {
  if (!inside(p)) return realWrite(p, data, options);
  const abs = path.resolve(String(p));
  const existing = fs.existsSync(abs) ? fs.readFileSync(abs) : null;
  const incoming = Buffer.isBuffer(data) ? data : Buffer.from(String(data));
  const line = JSON.stringify({ path: abs, existed: existing !== null, identical: existing !== null && existing.equals(incoming),
    bytes: incoming.length }) + "\n";
  if (report) realAppend(report, line);
};
fs.mkdirSync = function (p, options) {
  if (inside(p)) return undefined;
  return realMkdir(p, options);
};
