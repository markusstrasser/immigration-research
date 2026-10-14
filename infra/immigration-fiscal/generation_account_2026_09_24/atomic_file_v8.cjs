"use strict";
const fs = require("fs");
// Serialize before touching a published file; sibling rename makes readers see
// either complete version. Scientific and resource gates remain caller-owned.
function publish(file, render) {
  const bytes = render();
  const staged = `${file}.pending-${process.pid}`;
  try {
    fs.writeFileSync(staged, bytes, { flag: "wx" });
    fs.renameSync(staged, file);
  } finally {
    if (fs.existsSync(staged)) fs.unlinkSync(staged);
  }
}
module.exports = { publish };
