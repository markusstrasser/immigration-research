/* The candidate items of the receipt-side long-run lane (BRIEF.md, 2b85073), as importable definitions on the adopted
 * September 27 package (main_case_long_run_2026_09_27/package.cjs, loaded unchanged). probe.cjs and sign_reversal.cjs
 * import this file; it runs nothing and writes nothing.
 *
 * Parameters come from housing.py's derived/housing.json (ACS 2024, FHFA land shares, Saiz elasticities) and are
 * checked on load. Each item is a change to one or two receipt lines of a model and a receipt response:
 *   owner     modeled_owner_property responds at the long-run owner response (no key change: the line's amount,
 *             $24.97bn on the group, is the case's; the ACS gives $24.70bn);
 *   tenant    the tax on tenant-occupied housing is split out of remaining_production_property (national
 *             BEA Table 7.4.5 housing taxes on production x the tenant share of housing output), keyed by the
 *             group's share of contract rent, and responds at the long-run renter response; the capital-keyed rest
 *             keeps every cell's fraction and its response 0;
 *   personal  personal_property_tax (household personal property, NIPA 3.4 line 11) is re-keyed from capital
 *             ownership to the group's share of household vehicles and responds at 1, like the motor-vehicle line.
 * Every change holds each line's national total: the group's gain on a line is other residents' loss on it.
 */
"use strict";
const fs = require("fs");
const path = require("path");
const HERE = __dirname;
const FISCAL = path.resolve(HERE, "..");
const K = require(path.join(FISCAL, "main_case_long_run_2026_09_27", "package.cjs"));
const { Engine, MODEL, ALLOCS, METHODS, MAIN_SPECS, MAIN_PROFILE, stateFor, capitalReturn, evaluateFull, modelFor, withCentral } = K;

const H = JSON.parse(fs.readFileSync(path.join(HERE, "derived", "housing.json"), "utf8"));
const OWNER_LINE = "modeled_owner_property";
const BUSINESS_LINE = "remaining_production_property";
const TENANT_LINE = "tenant_occupied_property";
const PERSONAL_LINE = "personal_property_tax";
const line = (m, id) => m.receipts.lines.find((l) => l.id === id);
const receiptCells = (l) => Object.values(l.cells).flatMap((c) => ALLOCS.map((a) => c[a]));
const finite = (x, lo, hi) => Number.isFinite(x) && x >= lo && x <= hi;
for (const [k, v] of [["owner r", H.owner.r_lr_metro], ["owner low", H.owner.r_lr_national], ["renter r", H.renter.r_lr_metro],
  ["renter low", H.renter.r_lr_national], ["owner short run", H.owner.r_sr], ["owner fixed-stock fall", H.owner.fall_sr_metro],
  ["owner long-run fall", H.owner.fall_lr_metro], ["rent share", H.keys.rent_share], ["vehicle share", H.keys.vehicle_share],
  ["tenant taxes", H.bea_housing.tenant_taxes_bn / 1000]]) {
  if (!finite(v, 0, 1)) throw new Error(`[BLOCKED] housing.json: ${k} = ${v}`);
}

// The long-run responses (RESULT.md, item 2): central at the metro land-price fall, low at the national fall (others
// relocate freely), high at 1 (the benefit view). Beside the range: the short run (fixed stock) with assessment caps
// binding and with every roll following the market down, and the capital-tax view (a fixed national capital stock
// keeps the structures' tax on redeployed capital, so only the land-price fall is lost).
const RESPONSES = {
  owner: { central: H.owner.r_lr_metro, low: H.owner.r_lr_national, high: 1, short_run: H.owner.r_sr,
    short_run_market: H.owner.fall_sr_metro, capital_tax_view: H.owner.fall_lr_metro },
  renter: { central: H.renter.r_lr_metro, low: H.renter.r_lr_national, high: 1, short_run: H.renter.r_sr,
    short_run_market: H.renter.fall_sr_metro, capital_tax_view: H.renter.fall_lr_metro },
};
// The tenant-occupied housing tax: BEA's split (central) and the case-scaled alternative (the case's owner national
// times BEA's tenant-to-owner output ratio), which keeps the case's own owner/tenant scale.
const TENANT_NATIONAL = {
  bea: H.bea_housing.tenant_taxes_bn,
  case_scaled: line(MODEL, OWNER_LINE).national_bn * H.bea_housing.tenant_occupied_output_bn / H.bea_housing.owner_occupied_output_bn,
};
const KEYS = { rent: H.keys.rent_share, gross_rent: H.keys.gross_rent_share, vehicles: H.keys.vehicle_share };

function splitTenant(m0, national, share) {
  const m = Engine.clone(m0);
  const b = line(m, BUSINESS_LINE);
  if (line(m, TENANT_LINE)) throw new Error("[BLOCKED] the tenant line is split already");
  if (!(national > 0 && national < b.national_bn) || !finite(share, 0, 1)) throw new Error(`[BLOCKED] tenant split ${national} at ${share}`);
  const f = (b.national_bn - national) / b.national_bn;
  for (const c of receiptCells(b)) { c.target_bn *= f; c.other_bn *= f; }
  b.national_bn -= national;
  const cell = () => ({ direct: false, key: "renter_contract_rent", response_class: "tenant_housing_property", share,
    target_bn: share * national, other_bn: (1 - share) * national });
  m.receipts.lines.push({ id: TENANT_LINE, national_bn: national,
    cells: Object.fromEntries(m.receipts.scenarios.map((sc) => [sc, { personal: cell(), shared: cell() }])) });
  return m;
}
// A receipt line re-keyed to a share of its national total in every scenario and incidence rule (engine edits).
function rekey(m, id, share) {
  const l = line(m, id);
  const edits = m.receipts.scenarios.map((sc) => ({ side: "receipt", line: id, scenario: sc,
    by: Object.fromEntries(ALLOCS.map((a) => [a, l.national_bn * share - l.cells[sc][a].target_bn])) }));
  return Engine.applyCorrections(m, Object.assign({ lines: [], edits }, { meta: m.corrections }));
}

// The item set: {owner: r | null, tenant: {national, share, r} | null, personal: {share, r} | null}.
const CENTRAL_ITEMS = {
  owner: RESPONSES.owner.central,
  tenant: { national: TENANT_NATIONAL.bea, share: KEYS.rent, r: RESPONSES.renter.central },
  personal: { share: KEYS.vehicles, r: 1 },
};
const NONE = { owner: null, tenant: null, personal: null };
const only = (name, v) => Object.assign({}, NONE, { [name]: v === undefined ? CENTRAL_ITEMS[name] : v });
function itemModel(m0, items) {
  let m = m0;
  if (items.tenant) m = splitTenant(m, items.tenant.national, items.tenant.share);
  if (items.personal) m = rekey(m, PERSONAL_LINE, items.personal.share);
  return m;
}
function itemOverrides(items) {
  const o = {};
  if (items.owner !== null && items.owner !== undefined) o["receipt:" + OWNER_LINE] = items.owner;
  if (items.tenant) o["receipt:" + TENANT_LINE] = items.tenant.r;
  if (items.personal) o["receipt:" + PERSONAL_LINE] = items.personal.r;
  return o;
}
// The case's cost with the items: the package's state, the items' receipt responses on top, the capital return from
// the same evaluation (as evaluateFull does).
function evaluateWith(model, spec, overrides, profile) {
  const state = stateFor(model, spec, profile || MAIN_PROFILE);
  state.response_override = Object.assign({}, state.response_override, overrides);
  const evaluation = Engine.evaluate(model, state);
  const capital = capitalReturn(evaluation, spec);
  return { evaluation, capital, cost_bn: -evaluation.welfare_bn + capital.total_bn };
}
const MODELS = METHODS.map((meth) => modelFor("central", meth, withCentral({})));

module.exports = { K, H, HERE, FISCAL, OWNER_LINE, BUSINESS_LINE, TENANT_LINE, PERSONAL_LINE, RESPONSES, TENANT_NATIONAL, KEYS,
  CENTRAL_ITEMS, NONE, only, splitTenant, rekey, itemModel, itemOverrides, evaluateWith, MODELS, line, receiptCells };
