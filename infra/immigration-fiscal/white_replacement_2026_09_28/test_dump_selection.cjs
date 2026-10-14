"use strict";
const assert = require('node:assert/strict');
const {selectionFor} = require('./dump_selection.cjs');
const Engine = require('../assumption_explorer_2026_09_21/engine.js');

// Actual engine witness: the selected scenario and returned liability key differ.
const cell = {key: 'federal_liability', target_bn: 1, other_bn: 2, direct: true};
const model = {receipts: {reference: 'cbo_collective', lines: [
  {id: 'federal_income_tax', national_bn: 3, cells: {cbo_collective: {personal: cell}}}]},
  spending: {lines: []}, service: {delayed: []}, production: {dims: {}, sampling_se_bn: [0]},
  meta: {target_population: 1, resident_population: 10}};
const state = {receipt_scenario: 'cbo_collective', allocation: 'personal', response_override: {},
  direct_receipt_response: 1, indirect_receipt_response: 1, count_production: false, fiscal_weight: 1,
  production: {}};
for (const name of Engine.PRODUCTION_DIMS) {
  model.production.dims[name] = [0];
  state.production[name] = 0;
}
const evaluated = Engine.evaluate(model, state).receipts[0];
assert.equal(evaluated.key, 'federal_liability');
assert.deepEqual(selectionFor('receipts', evaluated, model),
  {scenario: 'cbo_collective', cell_key: 'federal_liability'});
assert.deepEqual(selectionFor('spending', {id: 'defense', key: 'population'}, model), {key: 'population'});
assert.throws(() => selectionFor('receipts', evaluated, {receipts: {}}), /\[BLOCKED\]/);
console.log('[PASS] receipt scenario differs from its cell key; missing selections block');
