// One package snapshot for all eight comparator leaves. The expensive case
// construction is cached by Node; the dump modules are evaluated for each leaf.
"use strict";
const path = require('path');
const FISCAL = path.resolve(__dirname, '..');
const original = process.argv.slice();
try {
  const exporters = [
    {file: path.join(__dirname, 'engine_lines.cjs'), load: () => require('./engine_lines.cjs')},
    {file: path.join(FISCAL, 'black_comparator_rough_2026_09_28', 'engine_lines.cjs'),
      load: () => require('../black_comparator_rough_2026_09_28/engine_lines.cjs')},
  ];
  for (const {file, load} of exporters) {
    for (const key of ['oct15', 'oct15_cash', 'oct15_union', 'oct15_union_cash']) {
      process.argv = [original[0], file, key];
      delete require.cache[require.resolve(file)];
      load();
    }
  }
} finally {
  process.argv = original;
}
