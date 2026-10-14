"use strict";

// engine.js returns a receipt cell's key, while the case carrier router selects
// by model.receipts.reference. Keep both declarations; they are different axes.
function selectionFor(side, line, model) {
  const selected = side === 'spending' ? {key: line.key}
    : side === 'receipts' ? {scenario: model.receipts?.reference, cell_key: line.key} : null;
  if (!selected || Object.values(selected).some(value => typeof value !== 'string' || !value)) {
    throw Error(`[BLOCKED] ${side}|${line.id}: no selected key/scenario/cell key`);
  }
  return selected;
}

module.exports = {selectionFor};
