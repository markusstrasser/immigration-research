/* The adopted main case as the page evaluates it (main_case_2026_10_07, adopted 2026-10-07). The case is engine.js's
 * evaluation of the case's corrections payload plus a return on public capital computed after the engine:
 *
 *   cost = -(engine welfare) + capital return
 *
 * Both parts follow the payload consumer (main_case_candidate_v4_2026_09_29/consumer.cjs) rule for rule: the line and
 * receipt responses in meta.responses at the specification's reading, and the components of meta.capital_return.
 * test_engine.js gates this file against the case's bands. What it adds is a state the reader can move. Beside the
 * engine's own fields, a case state has:
 *
 *   benefits     "accrual": the payload, with the Social Security and Medicare Part A promises the group earns as it
 *                works; "cash": the cash set's payload, benefits counted when paid.
 *   long_run     roads, transport and parks, and the lines the case re-keys or prices from them: "case" (their
 *                long-run responses in meta.responses at the reading), 0 (held fixed) or 1 (average cost). The roads
 *                and parks capital follows them, as meta.capital_return's rule says.
 *   capital      the return on public capital: "case" (meta.capital_return.rates at the reading), 0, or "private"
 *                (the rate reported beside the account, at both readings).
 *   enterprises  an option of meta.capital_return.enterprise_option: "D" (every government enterprise responds, its
 *                surplus and its capital) or "A" (they stay out).
 *   reading      the reading of the long-run evidence a point evaluation takes, "low" or "high". A state with
 *                reading_band ["low", "high"] spans both. The case pairs each reading with an end of the
 *                general-government band, so with both bands declared the two move together.
 *
 * response_override holds the reader's own shares, which win over the case's. The case's service responses scale with
 * service_response and rental assistance with transfer_response, as the engine scales the lines it answers itself. The
 * capital return is a public resource cost, so it takes the fiscal weight. Per-member figures divide by the lineage the
 * case counts (meta.lineage.counts.lineage_population).
 */
(function (root) {
  "use strict";
  var E = typeof module !== "undefined" && module.exports ? require("./engine.js") : root.Engine;
  var READINGS = ["low", "high"];
  var SYN_CLASSES = ["education_school_part", "education_other_part", "correction_constant"];
  var KEY_KINDS = ["constant", "receipt_amount_over_national", "lines_amount_over_national", "part_rekeyed"];
  var RESPONSE_KINDS = ["fixed", "enterprises_switch", "line_response", "line_response_over_share", "long_run_subfunction"];
  var CASE_FIELDS = ["benefits", "long_run", "capital", "enterprises", "reading", "reading_band"];
  var clone = E.clone;

  function fail(text) { throw new Error("[BLOCKED] " + text); }

  /* The case from model.json and its two payloads, {accrual, cash}. A payload stamped as adopted without capital
   * components is incomplete, not a case without capital (consumer.cjs's guard). */
  function create(model, payloads) {
    var pa = payloads.accrual, pc = payloads.cash;
    if (!pa || !pc || !pa.meta || !pc.meta) fail("the case needs both payloads, accrual and cash");
    if (!pa.meta.adopted || pc.meta.adopted !== pa.meta.adopted) fail("the two payloads are not one adopted case");
    [pa, pc].forEach(function (p) {
      var K = p.meta.capital_return;
      if (!(K && K.components && K.components.length)) fail("the payload adopted " + p.meta.adopted + " has no meta.capital_return components");
      if (!p.meta.responses || !p.meta.lineage || !p.meta.lineage.counts) fail("the payload lacks meta.responses or meta.lineage");
      p.meta.capital_return.components.forEach(function (c) {
        if (KEY_KINDS.indexOf(c.key.kind) < 0 || RESPONSE_KINDS.indexOf(c.response.kind) < 0) fail(c.id + ": unknown rule kind " + c.key.kind + " / " + c.response.kind);
      });
    });
    // The cash set is the case with the pension switch off: the same lines, responses, capital and people.
    var same = ["lines", "receipt_lines", "production"].every(function (k) { return JSON.stringify(pa[k]) === JSON.stringify(pc[k]); }) &&
      ["responses", "capital_return"].every(function (k) { return JSON.stringify(pa.meta[k]) === JSON.stringify(pc.meta[k]); }) &&
      JSON.stringify(pa.meta.lineage.counts) === JSON.stringify(pc.meta.lineage.counts);
    if (!same) fail("the cash set differs from the case in more than its edits and the pension switch");
    var syn = {};
    SYN_CLASSES.forEach(function (c) {
      var ls = pa.lines.filter(function (l) { return l.response_class === c; });
      if (ls.length !== 1) fail("the payload has " + ls.length + " correction lines of class " + c + ", not one");
      syn[c] = ls[0].id;
    });
    var models = { accrual: E.applyCorrections(model, pa), cash: E.applyCorrections(model, pc) };
    var m = models.accrual, R = pa.meta.responses, K = pa.meta.capital_return;
    var spending = {}, receipts = {};
    m.spending.lines.forEach(function (l) { spending[l.id] = l; });
    m.receipts.lines.forEach(function (l) { receipts[l.id] = l; });
    // The long-run lines and the lines that follow them: the payload's lines whose parent is a long-run line (state
    // pricing's lines and the part_rekeyed components' correction lines, as main_case_2026_09_29/package.cjs reads them).
    var LONG_RUN = {}, parent = {};
    model.service.delayed.forEach(function (id) { LONG_RUN[id] = true; });
    ((pa.meta.state_pricing && pa.meta.state_pricing.lines) || []).forEach(function (x) { parent[x.line] = x.parent; });
    K.components.forEach(function (c) { if (c.key.kind === "part_rekeyed") parent[c.key.correction_line] = c.key.parent_line; });
    Object.keys(parent).forEach(function (id) { if (LONG_RUN[parent[id]]) LONG_RUN[id] = true; });
    // Government enterprises: the enterprise-surplus receipt and the receipt lines split out of it respond as the
    // enterprise option's switch; the switch's value under the case's option must be the receipt's response.
    var ENTERPRISE = K.enterprise_option.receipt.replace(/^receipt:/, ""), REF = m.receipts.reference;
    var enterpriseClass = receipts[ENTERPRISE].cells[REF].personal.response_class, ENTERPRISE_RECEIPTS = {};
    (pa.receipt_lines || []).concat([receipts[ENTERPRISE]]).forEach(function (l) {
      if (l.cells[REF].personal.response_class === enterpriseClass) ENTERPRISE_RECEIPTS[l.id] = true;
    });
    var SWITCH = null;
    K.components.forEach(function (c) {
      if (c.response.kind !== "enterprises_switch") return;
      if (SWITCH && JSON.stringify(SWITCH) !== JSON.stringify(c.response.values)) fail("enterprise components switch differently");
      SWITCH = c.response.values;
    });
    if (!SWITCH || SWITCH[K.enterprises] !== K.enterprise_option.receipt_response) fail("the enterprise switch is not the receipt's response under option " + K.enterprises);
    // The responses meta.responses sets at each reading (consumer.cjs lineResponses), classified once.
    var CASE_LINES = { spending: {}, receipts: {} };
    Object.keys(R).forEach(function (id) {
      var e = R[id];
      if (!e || typeof e !== "object") return;
      if (e.receipt === true) {
        if (!receipts[id] || e.override !== "receipt:" + id) fail("meta.responses." + id + ": not a receipt line's override");
        if (ENTERPRISE_RECEIPTS[id] && e.low !== K.enterprise_option.receipt_response) fail("meta.responses." + id + " is not the enterprise option's response");
        CASE_LINES.receipts[id] = e;
      } else if (spending[id]) CASE_LINES.spending[id] = e;
      else return;
      READINGS.forEach(function (r) { if (typeof e[r] !== "number" || !isFinite(e[r])) fail("meta.responses." + id + " has no " + r + " response"); });
    });
    var classOf = function (id) { return spending[id].response_class; };
    Object.keys(CASE_LINES.spending).forEach(function (id) {
      if (["service", "subsidy"].indexOf(classOf(id)) < 0) fail("meta.responses." + id + ": a " + classOf(id) + " line this page does not scale");
    });
    var counts = pa.meta.lineage.counts, residents = model.meta.resident_population;
    var api = { models: models, payloads: payloads, meta: pa.meta, responses: R, capital_meta: K, syn: syn, long_run_lines: LONG_RUN,
      enterprise_receipts: ENTERPRISE_RECEIPTS, lineage_population: counts.lineage_population, account_union: counts.account_union,
      added_population: counts.added, resident_population: residents };

    /* The engine state of a case state at one reading. */
    function engineState(s, reading) {
      var e = clone(s), over = {};
      CASE_FIELDS.forEach(function (k) { delete e[k]; });
      e.data_corrections = false;  // the case's models are already corrected
      Object.keys(CASE_LINES.spending).forEach(function (id) {
        var v = LONG_RUN[id] ? (s.long_run === "case" ? CASE_LINES.spending[id][reading] : s.long_run) : CASE_LINES.spending[id][reading];
        over[id] = v * (classOf(id) === "service" ? s.service_response : s.transfer_response);
      });
      Object.keys(LONG_RUN).forEach(function (id) {
        if (!(id in over) && spending[id]) over[id] = (s.long_run === "case" ? fail("no long-run response for " + id) : s.long_run) * s.service_response;
      });
      Object.keys(CASE_LINES.receipts).forEach(function (id) {
        over["receipt:" + id] = ENTERPRISE_RECEIPTS[id] ? SWITCH[s.enterprises] : CASE_LINES.receipts[id][reading];
      });
      e.response_override = Object.assign(over, s.response_override || {});
      return e;
    }

    /* The return on public capital on one evaluation (consumer.cjs capitalOf), with the page's three switches. */
    function capitalReturn(ev, s, reading) {
      var rate = s.capital === "case" ? K.rates[reading] : s.capital === "private" ? K.rates.reported : s.capital === 0 ? 0 : fail("capital: " + s.capital);
      if (SWITCH[s.enterprises] === undefined) fail("enterprise option " + s.enterprises);
      var row = function (id) { var r = ev.spending.filter(function (l) { return l.id === id; })[0]; return r || fail("no spending line " + id); };
      var receipt = function (id) { var r = ev.receipts.filter(function (l) { return l.id === id; })[0]; return r || fail("no receipt line " + id); };
      var assigned = 0, components = K.components.map(function (c) {
        var k = c.key, r = c.response, key, response;
        if (k.kind === "constant") key = k.value;
        else if (k.kind === "receipt_amount_over_national") key = receipt(k.line).amount_bn / receipt(k.line).national_bn;
        else if (k.kind === "lines_amount_over_national") key = k.numerator_lines.reduce(function (a, id) { return a + row(id).amount_bn; }, 0) / row(k.denominator_line).national_bn;
        else key = row(k.parent_line).amount_bn / row(k.parent_line).national_bn + row(k.correction_line).amount_bn / k.part_national_bn;
        if (r.kind === "fixed") response = r.value;
        else if (r.kind === "enterprises_switch") response = r.values[s.enterprises];
        else if (r.kind === "line_response") response = row(r.line).response;
        else if (r.kind === "line_response_over_share") response = row(r.line).response / (r.share === "school" ? s.school_share : 1 - s.school_share);
        else {
          var sf = R[r.line].subfunctions.filter(function (x) { return x.id === r.subfunction; })[0];
          if (!sf) fail(c.id + ": no subfunction " + r.subfunction);
          response = s.service_response * (s.long_run === "case" ? sf[reading] : s.long_run);
        }
        assigned += c.stock_charged_bn * rate * key;
        return { id: c.id, label: c.label, part: c.part, level: c.level, key: key, response: response, return_bn: c.stock_charged_bn * rate * key * response };
      });
      return { rate: rate, components: components, assigned_bn: assigned, total_bn: components.reduce(function (a, c) { return a + c.return_bn; }, 0) };
    }

    /* One evaluation: the engine's, with the capital return beside it and the welfare net of it (negative = cost). */
    function evaluate(s, reading) {
      reading = reading || s.reading;
      if (READINGS.indexOf(reading) < 0) fail("reading " + reading);
      if (!models[s.benefits]) fail("benefits " + s.benefits);
      var ev = E.evaluate(models[s.benefits], engineState(s, reading)), cap = capitalReturn(ev, s, reading);
      ev.engine_welfare_bn = ev.welfare_bn;
      ev.capital = cap;
      ev.capital_return_bn = cap.total_bn;
      ev.welfare_bn = ev.engine_welfare_bn - s.fiscal_weight * cap.total_bn;
      ev.cost_bn = -ev.welfare_bn;
      ev.per_target_person = ev.welfare_bn * 1e9 / counts.lineage_population;
      ev.per_other_resident = ev.welfare_bn * 1e9 / (residents - counts.lineage_population);
      ev.reading = reading;
      return ev;
    }

    /* The span across the open choices: the engine's three (household money, the production scaling, the school
     * share), the declared bands (school, general government, per-line rules) and the readings, each reading paired
     * with its end of the general-government band when both are declared. */
    function range(s, outcome) {
      var shares = E.schoolShareBounds(model), values = [];
      var schools = s.school_response_band ? s.school_response_band : [s.school_response];
      var readings = s.reading_band ? s.reading_band : [s.reading];
      var ggs = s.general_government_response_band ? s.general_government_response_band : [s.general_government_response];
      var pairs = [];
      if (s.reading_band && s.general_government_response_band) {
        if (readings.length !== ggs.length) fail("the reading band and the general-government band are not paired");
        readings.forEach(function (r, i) { pairs.push([r, ggs[i]]); });
      } else readings.forEach(function (r) { ggs.forEach(function (g) { pairs.push([r, g]); }); });
      var keySets = keyBandSets(s.key_band || {});
      ["personal", "shared"].forEach(function (allocation) {
        model.production.dims.normalization.forEach(function (normalization) {
          shares.forEach(function (share) {
            schools.forEach(function (school) {
              pairs.forEach(function (pair) {
                keySets.forEach(function (keys) {
                  var x = clone(s);
                  x.allocation = allocation; x.production.normalization = normalization; x.school_share = share; x.school_response = school;
                  x.general_government_response = pair[1];
                  Object.keys(keys).forEach(function (id) { x.key_override[id] = keys[id]; });
                  values.push(evaluate(x, pair[0])[outcome]);
                });
              });
            });
          });
        });
      });
      return [Math.min.apply(null, values), Math.max.apply(null, values)];
    }

    function keyBandSets(band) {
      var sets = [{}];
      Object.keys(band).forEach(function (id) {
        band[id].forEach(function (key) { if (!spending[id] || !spending[id].keys[key]) fail("not an executed allocation rule: " + id + "/" + key); });
        sets = [].concat.apply([], sets.map(function (set) {
          return band[id].map(function (key) { var next = clone(set); next[id] = key; return next; });
        }));
      });
      return sets;
    }

    /* Exact Shapley attribution of outcome(to) - outcome(from) over the paths that differ (engine.js attribute, on
     * this file's evaluation). */
    function attribute(from, to, paths, outcome) {
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
        cache[mask] = evaluate(s)[outcome];
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

    /* The engine's default state with the case's own fields at the case's values. */
    function defaultState() {
      return Object.assign(E.defaultState(m), { benefits: "accrual", long_run: "case", capital: "case", enterprises: K.enterprises, reading: READINGS[0] });
    }

    return Object.assign(api, { READINGS: READINGS, CASE_FIELDS: CASE_FIELDS, engineState: engineState, capitalReturn: capitalReturn,
      evaluate: evaluate, range: range, attribute: attribute, defaultState: defaultState });
  }

  var exported = { create: create, READINGS: READINGS, CASE_FIELDS: CASE_FIELDS };
  if (typeof module !== "undefined" && module.exports) module.exports = exported; else root.Case = exported;
})(typeof window !== "undefined" ? window : globalThis);
