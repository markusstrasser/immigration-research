/* Evaluator for the complete annual account. One formula, taken from
 * full_account_2026_09_20/welfare.py and service_response.py:
 *
 *   direct  = sum(response_r * receipt_r) - sum(response_s * spending_s)
 *   welfare = P + fiscal_weight * (direct + F)
 *
 * P and F are looked up in the 3,888 executed production scenarios; every receipt and
 * spending amount is an executed allocation. Nothing is estimated here. The same file runs
 * in the page and under node (test_engine.js gates it against the executed exports).
 */
(function (root) {
  "use strict";

  var PRODUCTION_DIMS = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment",
    "labor_supply_elasticity", "capital_tax_retention", "excluded_capital_owner_share"];

  function defaultState(model) {
    var production = {};
    PRODUCTION_DIMS.forEach(function (d) { production[d] = model.production.reference[d]; });
    return {
      allocation: "personal",
      receipt_scenario: model.receipts.reference,
      spending_keys: "preferred",
      key_override: {},
      production: production,
      count_production: true,
      fiscal_weight: 1,
      service_response: 1,
      public_goods_response: 0,
      school_share: schoolShareBounds(model)[0],
      school_response: 1,
      other_education_response: 1,
      delayed_response: 1,
      transfer_response: 1,
      interest_response: 0,
      subsidy_response: 0,
      direct_receipt_response: 1,
      indirect_receipt_response: 0,
      response_override: {}
    };
  }

  function clone(state) { return JSON.parse(JSON.stringify(state)); }

  function schoolShareBounds(model) {
    var shares = model.service.profiles.map(function (p) { return p.school_share; })
      .filter(function (x) { return x > 0; });
    return [Math.min.apply(null, shares), Math.max.apply(null, shares)];
  }

  function levelIndex(levels, value) {
    for (var i = 0; i < levels.length; i++) {
      if (levels[i] === value || (typeof value === "number" && Math.abs(levels[i] - value) < 1e-9)) return i;
    }
    throw new Error("Not an executed level: " + value + " in " + JSON.stringify(levels));
  }

  function productionIndex(model, production) {
    var index = 0;
    PRODUCTION_DIMS.forEach(function (d) {
      var levels = model.production.dims[d];
      index = index * levels.length + levelIndex(levels, production[d]);
    });
    return index;
  }

  function spendingKey(line, state) {
    var key = state.key_override[line.id];
    if (key && line.keys[key]) return key;
    return state.spending_keys === "alternative" ? line.alternative_key : line.preferred_key;
  }

  function spendingResponse(model, line, state) {
    var override = state.response_override[line.id];
    if (typeof override === "number") return override;
    switch (line.response_class) {
      case "household_transfer": return state.transfer_response;
      case "public_goods": return state.public_goods_response;
      case "interest": return state.interest_response;
      case "subsidy": return state.subsidy_response;
      case "service":
        if (line.id === "education_services") {
          return state.service_response * (state.school_share * state.school_response +
            (1 - state.school_share) * state.other_education_response);
        }
        if (model.service.delayed.indexOf(line.id) >= 0) return state.service_response * state.delayed_response;
        return state.service_response;
      default: return 0;  // foreign flows and rounding never enter the resident account
    }
  }

  function evaluate(model, state) {
    var receipts = [], spending = [], classes = {};
    var direct = 0, targetBalance = 0, otherBalance = 0;
    function add(bucket, name, assigned, responsive) {
      var c = classes[name] || (classes[name] = { assigned_bn: 0, responsive_bn: 0, side: bucket });
      c.assigned_bn += assigned; c.responsive_bn += responsive;
    }
    model.receipts.lines.forEach(function (line) {
      var cell = line.cells[state.receipt_scenario][state.allocation];
      var override = state.response_override["receipt:" + line.id];
      var response = typeof override === "number" ? override
        : (cell.direct ? state.direct_receipt_response : state.indirect_receipt_response);
      var name = cell.direct ? "direct_receipts" : "incidence_receipts";
      receipts.push({ id: line.id, national_bn: line.national_bn, key: cell.key, share: cell.share,
        response_class: cell.response_class, group: name, amount_bn: cell.target_bn, response: response,
        effect_bn: response * cell.target_bn });
      add("receipts", name, cell.target_bn, response * cell.target_bn);
      direct += response * cell.target_bn;
      targetBalance += cell.target_bn; otherBalance += cell.other_bn;
    });
    model.spending.lines.forEach(function (line) {
      var key = spendingKey(line, state), cell = line.keys[key][state.allocation];
      var response = spendingResponse(model, line, state);
      spending.push({ id: line.id, family: line.family, national_bn: line.national_bn, key: key, share: cell.share,
        keys: Object.keys(line.keys), response_class: line.response_class, group: line.response_class,
        amount_bn: cell.target_bn, response: response, effect_bn: -response * cell.target_bn });
      add("spending", line.response_class, cell.target_bn, response * cell.target_bn);
      direct -= response * cell.target_bn;
      targetBalance -= cell.target_bn; otherBalance -= cell.other_bn;
    });
    var index = productionIndex(model, state.production);
    var P = state.count_production ? model.production.private_wtp_bn[index] : 0;
    var F = state.count_production ? model.production.induced_receipts_bn[index] : 0;
    var welfare = P + state.fiscal_weight * (direct + F);
    var popShare = model.meta.target_population / model.meta.resident_population;
    var services = classes.service || { assigned_bn: 0, responsive_bn: 0 };
    return {
      welfare_bn: welfare, direct_fiscal_response_bn: direct, private_wtp_bn: P, induced_receipts_bn: F,
      production_gain_bn: P + F, sampling_se_bn: model.production.sampling_se_bn[index],
      effective_service_response: services.assigned_bn ? services.responsive_bn / services.assigned_bn : 0,
      classes: classes, receipts: receipts, spending: spending,
      target_balance_bn: targetBalance, other_balance_bn: otherBalance,
      normalized_gap_bn: targetBalance - popShare * (targetBalance + otherBalance),
      per_target_person: welfare * 1e9 / model.meta.target_population,
      per_other_resident: welfare * 1e9 / (model.meta.resident_population - model.meta.target_population)
    };
  }

  /* Dimensions the account itself leaves unresolved: report the span across them, never one corner. */
  function unresolvedRange(model, state, outcome) {
    var bounds = schoolShareBounds(model), values = [];
    ["personal", "shared"].forEach(function (allocation) {
      model.production.dims.normalization.forEach(function (normalization) {
        bounds.forEach(function (share) {
          var s = clone(state);
          s.allocation = allocation; s.production.normalization = normalization; s.school_share = share;
          var responses = state.school_response_band ? state.school_response_band : [state.school_response];
          responses.forEach(function (r) { s.school_response = r; values.push(evaluate(model, s)[outcome]); });
        });
      });
    });
    return [Math.min.apply(null, values), Math.max.apply(null, values)];
  }

  /* Exact Shapley attribution of outcome(to) - outcome(from) over the controls that differ. */
  function attribute(model, from, to, paths, outcome) {
    function get(s, p) { return p.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, s); }
    function set(s, p, v) {
      var ks = p.split("."), o = s;
      for (var i = 0; i < ks.length - 1; i++) { if (o[ks[i]] == null) o[ks[i]] = {}; o = o[ks[i]]; }
      if (v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = v;
    }
    var changed = paths.filter(function (p) { return JSON.stringify(get(from, p)) !== JSON.stringify(get(to, p)); });
    var n = changed.length, total = 1 << n, cache = new Array(total);
    if (n > 14) throw new Error("Too many changed controls for exact attribution: " + n);
    for (var mask = 0; mask < total; mask++) {
      var s = clone(from);
      for (var i = 0; i < n; i++) if (mask & (1 << i)) set(s, changed[i], clone({ v: get(to, changed[i]) }).v);
      cache[mask] = evaluate(model, s)[outcome];
    }
    var fact = [1]; for (var f = 1; f <= n; f++) fact[f] = fact[f - 1] * f;
    var bits = function (m) { var c = 0; while (m) { c += m & 1; m >>= 1; } return c; };
    return changed.map(function (path, i) {
      var phi = 0;
      for (var mask = 0; mask < total; mask++) {
        if (mask & (1 << i)) continue;
        var k = bits(mask);
        phi += fact[k] * fact[n - k - 1] / fact[n] * (cache[mask | (1 << i)] - cache[mask]);
      }
      return { path: path, from: get(from, path), to: get(to, path), effect_bn: phi };
    });
  }

  var api = { PRODUCTION_DIMS: PRODUCTION_DIMS, defaultState: defaultState, clone: clone, evaluate: evaluate,
    unresolvedRange: unresolvedRange, attribute: attribute, schoolShareBounds: schoolShareBounds,
    spendingKey: spendingKey, productionIndex: productionIndex };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.Engine = api;
})(typeof window !== "undefined" ? window : globalThis);
