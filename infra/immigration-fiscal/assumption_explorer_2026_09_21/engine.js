/* Evaluator for the complete annual account. One formula, taken from
 * full_account_2026_09_20/welfare.py and service_response.py:
 *
 *   direct  = sum(response_r * receipt_r) - sum(response_s * spending_s)
 *   welfare = P + fiscal_weight * (direct + F)
 *
 * P and F are looked up in the 3,888 executed production scenarios; every receipt and
 * spending amount is an executed allocation. Nothing is estimated here. The same file runs
 * in the page and under node (test_engine.js gates it against the executed exports).
 *
 * Data corrections (main_case_2026_09_24/derived/corrections.json) are edits to executed
 * allocations. applyCorrections() makes the corrected model; a state with data_corrections set
 * evaluates model.corrected, so one state can move between the two data sets.
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
      key_band: {},
      production: production,
      count_production: true,
      fiscal_weight: 1,
      service_response: 1,
      public_goods_response: 0,
      general_government_response: 0,
      school_share: schoolShareBounds(model)[0],
      school_response: 1,
      other_education_response: 1,
      delayed_response: 1,
      transfer_response: 1,
      interest_response: 0,
      subsidy_response: 0,
      direct_receipt_response: 1,
      indirect_receipt_response: 0,
      data_corrections: false,
      response_override: {}
    };
  }

  function clone(state) { return JSON.parse(JSON.stringify(state)); }

  /* A copy of the model with a corrections payload applied: {lines: [{id, family, response_class,
   * label}], edits: [{side: "receipt", line, scenario, by} | {side: "spending", line, key, by}]},
   * by = {personal, shared} in $bn of the group's target. Each edit moves the same amount out of
   * other residents' share, so national totals hold, and rescales the cell's share of its fixed base
   * (target / share is unchanged). Unknown lines, keys or rules fail loudly.
   *
   * Three optional parts serve a revision that splits a line out or re-weights production; a payload
   * without them is applied as before. receipt_lines: [{id, national_bn, cells}] adds receipt lines with
   * a cell for every executed incidence rule and allocation. An edit {side, line, national_bn} scales the
   * line's national total, and every cell's target and other amounts, to that total (shares hold), in order
   * with the other edits. production: {dims, private_wtp_bn, induced_receipts_bn, sampling_se_bn} replaces
   * the production arrays of a grid with the same dimensions. */
  function applyCorrections(model, payload) {
    var m = clone(model), allocations = ["personal", "shared"];
    delete m.corrected;
    function zero() { return { target_bn: 0, other_bn: 0, share: 0 }; }
    (payload.receipt_lines || []).forEach(function (l) {
      if (m.receipts.lines.some(function (x) { return x.id === l.id; })) throw new Error("Correction receipt line exists already: " + l.id);
      if (typeof l.national_bn !== "number" || !isFinite(l.national_bn)) throw new Error("Correction receipt line lacks a national total: " + l.id);
      m.receipts.scenarios.forEach(function (sc) {
        allocations.forEach(function (a) {
          if (!l.cells || !l.cells[sc] || !l.cells[sc][a]) throw new Error("Correction receipt line lacks an executed cell: " + l.id + "/" + sc + "/" + a);
        });
      });
      m.receipts.lines.push(clone(l));
    });
    (payload.lines || []).forEach(function (l) {
      if (m.spending.lines.some(function (x) { return x.id === l.id; })) throw new Error("Correction line exists already: " + l.id);
      m.spending.lines.push({ id: l.id, family: l.family, national_bn: 0, response_class: l.response_class, label: l.label,
        preferred_key: "k", alternative_key: "k", keys: { k: { personal: zero(), shared: zero() } } });
    });
    payload.edits.forEach(function (e) {
      var cell;
      if (e.national_bn !== undefined) { scaleLine(m, e); return; }
      if (e.side === "receipt") {
        var r = m.receipts.lines.filter(function (x) { return x.id === e.line; })[0];
        if (!r || !r.cells[e.scenario]) throw new Error("Not an executed receipt cell: " + e.line + "/" + e.scenario);
        cell = r.cells[e.scenario];
      } else {
        var sp = m.spending.lines.filter(function (x) { return x.id === e.line; })[0];
        if (!sp || !sp.keys[e.key]) throw new Error("Not an executed allocation rule: " + e.line + "/" + e.key);
        cell = sp.keys[e.key];
      }
      allocations.forEach(function (a) {
        var t = cell[a].target_bn, next = t + e.by[a];
        if (t !== 0) cell[a].share *= next / t;
        cell[a].target_bn = next; cell[a].other_bn -= e.by[a];
      });
    });
    if (payload.production) {
      PRODUCTION_DIMS.forEach(function (d) {
        if (!payload.production.dims || JSON.stringify(payload.production.dims[d]) !== JSON.stringify(m.production.dims[d])) {
          throw new Error("Not this model's production grid: dimension " + d);
        }
      });
      ["private_wtp_bn", "induced_receipts_bn", "sampling_se_bn"].forEach(function (k) {
        var xs = payload.production[k];
        if (!Array.isArray(xs) || xs.length !== m.production[k].length) throw new Error("Not this model's production grid: " + k);
        m.production[k] = xs.slice();
      });
    }
    m.corrections = payload.meta || {};
    return m;
  }

  /* A national-scale edit: the line's national total becomes e.national_bn, and every cell's target and
   * other amounts scale by the same factor. */
  function scaleLine(m, e) {
    var lines = e.side === "receipt" ? m.receipts.lines : e.side === "spending" ? m.spending.lines : null;
    var line = lines && lines.filter(function (x) { return x.id === e.line; })[0];
    if (!line) throw new Error("Not an executed line to scale: " + e.side + "/" + e.line);
    if (typeof e.national_bn !== "number" || !isFinite(e.national_bn) || !line.national_bn) {
      throw new Error("Not a national total to scale to: " + e.line + " " + e.national_bn);
    }
    var f = e.national_bn / line.national_bn, cells = e.side === "receipt" ? line.cells : line.keys;
    Object.keys(cells).forEach(function (k) {
      ["personal", "shared"].forEach(function (a) { cells[k][a].target_bn *= f; cells[k][a].other_bn *= f; });
    });
    line.national_bn = e.national_bn;
  }

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
      // The executed grid moves defense and general government together; the page separates them.
      case "public_goods":
        return line.id === "general_public_services" ? state.general_government_response : state.public_goods_response;
      case "interest": return state.interest_response;
      case "subsidy": return state.subsidy_response;
      // Lines added by data corrections: the school and college parts of the education line's
      // correction respond as those parts of the line do; correction constants count in full.
      case "education_school_part": return state.service_response * state.school_share * state.school_response;
      case "education_other_part": return state.service_response * (1 - state.school_share) * state.other_education_response;
      case "correction_constant": return 1;
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
    if (state.data_corrections) {
      if (!model.corrected) throw new Error("No data corrections are loaded for this model");
      model = model.corrected;
    }
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

  /* Dimensions the account itself leaves unresolved, plus the bands a convention declares
   * (school_response_band, general_government_response_band, key_band {line: [keyA, keyB]}):
   * report the span across their cartesian product, never one corner. */
  function unresolvedRange(model, state, outcome) {
    var bounds = schoolShareBounds(model), values = [];
    var schools = state.school_response_band ? state.school_response_band : [state.school_response];
    var governments = state.general_government_response_band ? state.general_government_response_band : [state.general_government_response];
    var keySets = keyBandSets(model, state.key_band || {});
    ["personal", "shared"].forEach(function (allocation) {
      model.production.dims.normalization.forEach(function (normalization) {
        bounds.forEach(function (share) {
          var s = clone(state);
          s.allocation = allocation; s.production.normalization = normalization; s.school_share = share;
          schools.forEach(function (r) {
            s.school_response = r;
            governments.forEach(function (g) {
              s.general_government_response = g;
              keySets.forEach(function (keys) {
                Object.keys(keys).forEach(function (id) { s.key_override[id] = keys[id]; });
                values.push(evaluate(model, s)[outcome]);
              });
            });
          });
        });
      });
    });
    return [Math.min.apply(null, values), Math.max.apply(null, values)];
  }

  /* Every combination of the rules a key band names; a rule the model does not hold fails loudly. */
  function keyBandSets(model, band) {
    var sets = [{}];
    Object.keys(band).forEach(function (id) {
      var line = model.spending.lines.filter(function (l) { return l.id === id; })[0];
      band[id].forEach(function (key) { if (!line || !line.keys[key]) throw new Error("Not an executed allocation rule: " + id + "/" + key); });
      sets = [].concat.apply([], sets.map(function (set) {
        return band[id].map(function (key) { var next = clone(set); next[id] = key; return next; });
      }));
    });
    return sets;
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
    applyCorrections: applyCorrections,
    unresolvedRange: unresolvedRange, attribute: attribute, schoolShareBounds: schoolShareBounds,
    spendingKey: spendingKey, productionIndex: productionIndex };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.Engine = api;
})(typeof window !== "undefined" ? window : globalThis);
