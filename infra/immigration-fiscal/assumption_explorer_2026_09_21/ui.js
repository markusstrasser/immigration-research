/* Page logic. All numbers come from Engine.evaluate(MODEL, state); this file only draws. */
(function () {
  "use strict";
  var M = window.MODEL, PRESETS = window.PRESETS.presets, CONTEXT = window.CONTEXT.items || [];
  var E = window.Engine, $ = function (id) { return document.getElementById(id); };
  var state, lens = "welfare_bn", activePreset = null, history = [];

  var LABEL = {
    federal_income_tax: "Federal income tax", employer_oasdi: "Social Security tax, employer half",
    employee_oasdi: "Social Security tax, employee half", general_sales_tax: "General sales tax",
    excise_selective_sales: "Excise and selective sales taxes", state_local_income_tax: "State and local income tax",
    modeled_owner_property: "Property tax, owner-occupied (modelled)", government_asset_income: "Government asset income",
    employee_hi: "Medicare tax, employee half", corporate_capital: "Corporate tax borne by capital",
    employer_hi: "Medicare tax, employer half", corporate_labor: "Corporate tax borne by labor",
    personal_current_transfers: "Fees, fines and personal transfers", remaining_production_property: "Property tax, business and rental",
    other_domestic_social_contributions: "Other social contributions", self_employment_oasdi_hi: "Self-employment payroll tax",
    medicare_supplementary_premiums: "Medicare premiums", customs_duties: "Customs duties",
    other_production_taxes: "Other production taxes", business_current_transfers: "Business transfers to government",
    personal_motor_vehicle: "Motor vehicle licences", other_personal_tax: "Other personal taxes",
    personal_property_tax: "Personal property tax", enterprise_surplus: "Government enterprise surplus",
    education_services: "Education (schools and colleges)", domestic_interest: "Interest on existing debt",
    medicaid_and_chip_other_medical: "Medicaid, CHIP and other medical", defense: "National defense",
    public_order_safety: "Police, courts, prisons, fire", general_public_services: "General government",
    economic_affairs_services: "Roads, transport, economic affairs", income_security_services: "Welfare administration and services",
    health_services: "Public health services", refundable_tax_credits: "Refundable tax credits (EITC, CTC)",
    snap: "SNAP", ssi: "SSI", recreation_culture: "Parks, recreation, culture", housing_community_services: "Housing and community services"
  };
  function label(id) { return LABEL[id] || id.replace(/_/g, " ").replace(/^./, function (c) { return c.toUpperCase(); }); }
  var CLASS_LABEL = { direct_receipts: "Taxes households remit directly", incidence_receipts: "Corporate, property and asset receipts (incidence only)",
    household_transfer: "Cash and in-kind benefits", service: "Public services", public_goods: "Defense and general government",
    interest: "Interest on existing debt", subsidy: "Business and housing subsidies", foreign: "Foreign flows", rounding: "Rounding" };

  var levels = function (d) { return M.production.dims[d]; };
  var CONTROLS = [
    { group: "What counts as a cost", id: "service_response", label: "Public services that scale with population", type: "slider",
      help: "Share of schools, police, health and other services assumed to shrink if the group were absent. 1 = average cost; 0 = services are free at the margin. The account executes 0, 0.5 and 1.", affects: ["service"] },
    { group: "What counts as a cost", id: "school_response", label: "K-12 school budgets respond", type: "slider", marks: [0.63, 0.66],
      help: "CBO's evidence puts the school-spending response at 63-66%. Applies to the school share of education only.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "school_share", label: "School share of education spending", type: "slider", min: E.schoolShareBounds(M)[0], max: E.schoolShareBounds(M)[1],
      help: "National bounds 71.5-86.5%, transported to this group under a common-composition assumption.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "other_education_response", label: "Colleges and other education respond", type: "slider", affects: ["education_services"],
      help: "No estimate exists; the account runs both 0 and 1." },
    { group: "What counts as a cost", id: "delayed_response", label: "Roads, economic affairs, parks respond", type: "slider", affects: ["economic_affairs_services", "recreation_culture"],
      help: "Slow-adjusting categories. The CBO-informed headline holds them fixed (0)." },
    { group: "What counts as a cost", id: "public_goods_response", label: "Defense and general government respond", type: "slider", affects: ["public_goods"],
      help: "Held at zero in the headline BY ASSUMPTION, not from CBO. 1 charges the full per-capita share." },
    { group: "What counts as a cost", id: "interest_response", label: "Interest on existing debt responds", type: "slider", affects: ["interest"],
      help: "Legacy debt does not shrink with population; zero in every executed case." },
    { group: "What counts as a cost", id: "transfer_response", label: "Benefits paid to the group are saved", type: "slider", affects: ["household_transfer"],
      help: "Medicaid, Social Security, Medicare, credits. 1 in every executed case." },
    { group: "What counts as revenue", id: "direct_receipt_response", label: "Taxes remitted by the group are lost", type: "slider", affects: ["direct_receipts"],
      help: "Income, payroll, sales and excise taxes. 1 in every executed case." },
    { group: "What counts as revenue", id: "indirect_receipt_response", label: "Corporate and property incidence is lost", type: "slider", affects: ["incidence_receipts"],
      help: "Receipts assigned to the group only through incidence rules. 0 in the account: counting them risks double counting the production block." },
    { group: "What counts as revenue", id: "receipt_scenario", label: "Tax incidence rules", type: "levels", levels: M.receipts.scenarios, affects: ["direct_receipts", "incidence_receipts"],
      help: "Eight executed incidence conventions (CBO collective is the reference; NAS 80%, Treasury 81.5% and others are stress cases)." },
    { group: "Production side", id: "count_production", label: "Count the production gain to other residents", type: "levels", levels: [true, false], affects: ["production"],
      help: "Private gain to other residents plus induced tax receipts from a CES production model. A pure tax-and-spending tally leaves it out." },
    { group: "Production side", id: "production.sigma", label: "Substitution elasticity between skill groups", type: "levels", levels: levels("sigma"), affects: ["production"], help: "Higher = workers are closer substitutes = smaller gain." },
    { group: "Production side", id: "production.capital_adjustment", label: "Capital has adjusted", type: "levels", levels: levels("capital_adjustment"), affects: ["production"],
      help: "0 = short run, capital fixed (large gain to capital owners); 1 = long run. The executed grid pairs this with the service response as one capacity path." },
    { group: "Production side", id: "production.labor_share", label: "Labor share of income", type: "levels", levels: levels("labor_share"), affects: ["production"], help: "" },
    { group: "Production side", id: "production.labor_supply_elasticity", label: "Native labor supply elasticity", type: "levels", levels: levels("labor_supply_elasticity"), affects: ["production"], help: "" },
    { group: "Production side", id: "production.capital_tax_retention", label: "Capital-tax gain kept by government", type: "levels", levels: levels("capital_tax_retention"), affects: ["production"], help: "" },
    { group: "Production side", id: "production.excluded_capital_owner_share", label: "Capital owned outside the beneficiary group", type: "levels", levels: levels("excluded_capital_owner_share"), affects: ["production"],
      help: "0 = all capital gains accrue to other US residents (the favourable core case). 0.5 and 1 are unestimated endpoints." },
    { group: "Production side", id: "production.split", label: "Who counts as the competing skill group", type: "levels", levels: levels("split"), affects: ["production"], help: "" },
    { group: "Production side", id: "production.proxy", label: "Earnings measure", type: "levels", levels: levels("proxy"), affects: ["production"], help: "" },
    { group: "Accounting conventions", id: "allocation", label: "Household resources", type: "levels", levels: ["personal", "shared"], affects: ["all"], help: "Personal = each person's own flows; shared = pooled within the household. Unresolved; the headline spans both." },
    { group: "Accounting conventions", id: "production.normalization", label: "Production normalised to", type: "levels", levels: levels("normalization"), affects: ["production"], help: "Unresolved; the headline spans both." },
    { group: "Accounting conventions", id: "spending_keys", label: "Spending allocation keys", type: "levels", levels: ["preferred", "alternative"], affects: ["spending"], help: "Preferred proxies or the executed alternative proxy for every category. Change single lines in the ledger below." },
    { group: "Accounting conventions", id: "fiscal_weight", label: "Value of a budget dollar to other residents", type: "slider", affects: ["all"], help: "1 = dollar for dollar. 0 is a valuation endpoint, not a bound." }
  ];
  var PATHS = CONTROLS.map(function (c) { return c.id; }).concat(["school_response_band", "key_override", "response_override"]);

  function get(s, p) { return p.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, s); }
  function set(s, p, v) { var ks = p.split("."), o = s; for (var i = 0; i < ks.length - 1; i++) o = o[ks[i]]; if (v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = v; }
  function fmt(x, d) { if (x == null || !isFinite(x)) return "n/a"; var s = Math.abs(x).toFixed(d == null ? 1 : d).replace(/\B(?=(\d{3})+(?!\d))/g, ","); return (x < -1e-9 ? "−" : "") + s; }
  function signed(x, d) { return (x > 1e-9 ? "+" : "") + fmt(x, d); }
  function show(v) { return typeof v === "number" ? String(Math.round(v * 1000) / 1000) : v === true ? "yes" : v === false ? "no" : String(v).replace(/_/g, " "); }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }

  function presetState(p) {
    var s = E.defaultState(M);
    (p.settings || []).forEach(function (x) { if (x.path) set(s, x.path, JSON.parse(JSON.stringify(x.value))); });
    return s;
  }
  var CENTRAL = presetState(PRESETS.filter(function (p) { return p.id === "repo_central"; })[0]);

  function outcome(s, key) {
    var out = E.evaluate(M, s), range = E.unresolvedRange(M, s, key || lens);
    return { out: out, value: out[key || lens], range: range };
  }

  function executedStatus(s) {
    var d = E.defaultState(M), contract = ["transfer_response", "interest_response", "subsidy_response", "direct_receipt_response", "indirect_receipt_response"]
      .every(function (k) { return s[k] === d[k]; }) && !Object.keys(s.key_override).length && !Object.keys(s.response_override).length && s.count_production;
    if (!contract) return ["own", "Your own assumption set: same formula, settings the account never ran"];
    var flat = s.school_response === 1 && s.other_education_response === 1 && s.delayed_response === 1 && !s.school_response_band;
    var onLevels = [0, 0.5, 1].indexOf(s.service_response) >= 0 && [0, 1].indexOf(s.public_goods_response) >= 0 && [0, 1].indexOf(s.fiscal_weight) >= 0;
    if (flat && onLevels && s.service_response === s.production.capital_adjustment) return ["grid", "Executed case: a row of the 497,664-row scenario grid"];
    var ref = M.production.reference, atRef = E.PRODUCTION_DIMS.every(function (k) { return k === "normalization" || s.production[k] === ref[k]; });
    if (atRef && s.service_response === 1 && s.public_goods_response === 0 && s.fiscal_weight === 1 && s.receipt_scenario === M.receipts.reference && s.spending_keys === "preferred")
      return ["grid", "Executed case: a category service-response case at the reference production scenario"];
    return ["formula", "Exact formula, off the executed grid: the account is linear in these responses"];
  }

  /* ---------- drawing ---------- */
  function drawPresets() {
    var vals = PRESETS.map(function (p) { return outcome(presetState(p)); });
    var lo = Math.min.apply(null, vals.map(function (v) { return Math.min(v.range[0], 0); }));
    var hi = Math.max.apply(null, vals.map(function (v) { return Math.max(v.range[1], 0); }));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("presets").innerHTML = PRESETS.map(function (p, i) {
      var v = vals[i], a = x(Math.min(v.range[0], v.range[1])), b = x(Math.max(v.range[0], v.range[1]));
      return '<button class="preset' + (activePreset === p.id ? " on" : "") + '" data-preset="' + p.id + '" id="preset-' + p.id + '">' +
        '<span class="pk">' + esc(p.kind_label) + '</span><span class="pl">' + esc(p.label) + '</span>' +
        '<span class="pv">' + fmt(v.range[0], 0) + (Math.abs(v.range[1] - v.range[0]) > 0.5 ? " to " + fmt(v.range[1], 0) : "") + '</span>' +
        '<span class="track"><i class="zero" style="left:' + x(0) + '%"></i><i class="span ' + (v.value < 0 ? "neg" : "pos") + '" style="left:' + a + '%;width:' + Math.max(b - a, 0.8) + '%"></i></span></button>';
    }).join("");
  }

  function drawHeadline() {
    var o = outcome(state), c = outcome(CENTRAL), st = executedStatus(state);
    var names = { welfare_bn: "Annual effect on all other US residents", target_balance_bn: "Accounting balance of the group (everything at average cost)", normalized_gap_bn: "Balance relative to an equal per-capita share" };
    $("h-name").textContent = names[lens];
    $("h-value").textContent = fmt(o.value, 1);
    $("h-value").className = "big " + (o.value < 0 ? "neg" : "pos");
    $("h-range").textContent = "Unresolved conventions span " + fmt(o.range[0], 0) + " to " + fmt(o.range[1], 0) + " bn (household pooling, normalisation, school share" + (state.school_response_band ? ", 63-66% school response" : "") + ")";
    $("h-per").textContent = lens === "welfare_bn" ? "$" + fmt(o.out.per_other_resident, 0) + " per other resident · $" + fmt(o.out.per_target_person, 0) + " per group member"
      : "$" + fmt(o.value * 1e9 / M.meta.target_population, 0) + " per group member";
    $("h-status").textContent = st[1]; $("h-status").className = "status " + st[0];
    var parts = E.attribute(M, CENTRAL, state, PATHS, lens).filter(function (p) { return Math.abs(p.effect_bn) > 0.05; })
      .sort(function (a, b) { return Math.abs(b.effect_bn) - Math.abs(a.effect_bn); });
    var byId = {}; CONTROLS.forEach(function (k) { byId[k.id] = k; });
    $("diff-title").textContent = parts.length ? "Distance from the repo's central case: " + signed(o.value - c.value, 1) + " bn, split exactly across the assumptions that differ"
      : "This is the repo's central case";
    var max = Math.max.apply(null, parts.map(function (p) { return Math.abs(p.effect_bn); }).concat([1]));
    $("diff").innerHTML = parts.map(function (p) {
      var k = byId[p.path] || { label: p.path.replace(/_/g, " ") };
      return '<li data-affects="' + (k.affects || []).join(" ") + '"><span class="dl">' + esc(k.label) + '<em>' + esc(show(p.from)) + " → " + esc(show(p.to)) + '</em></span>' +
        '<span class="db"><i class="' + (p.effect_bn < 0 ? "neg" : "pos") + '" style="width:' + Math.abs(p.effect_bn) / max * 100 + '%"></i></span><span class="dv">' + signed(p.effect_bn, 1) + '</span></li>';
    }).join("");
  }

  function bridgeSteps(out, s) {
    var w = s.fiscal_weight, c = out.classes, g = function (k) { return c[k] || { assigned_bn: 0, responsive_bn: 0 }; };
    var edu = out.spending.filter(function (l) { return l.id === "education_services"; })[0];
    if (lens !== "welfare_bn") {
      var steps = [["Taxes remitted directly", g("direct_receipts").assigned_bn, 0, "direct_receipts"], ["Corporate, property, asset receipts", g("incidence_receipts").assigned_bn, 0, "incidence_receipts"],
        ["Benefits received", -g("household_transfer").assigned_bn, 0, "household_transfer"], ["Education", -edu.amount_bn, 0, "education_services"],
        ["Other public services", -(g("service").assigned_bn - edu.amount_bn), 0, "service"], ["Defense and general government", -g("public_goods").assigned_bn, 0, "public_goods"],
        ["Interest and subsidies", -(g("interest").assigned_bn + g("subsidy").assigned_bn), 0, "interest subsidy"]];
      if (lens === "normalized_gap_bn") steps.push(["Less an equal per-capita share of the resident balance", out.normalized_gap_bn - out.target_balance_bn, 0, "all"]);
      return steps;
    }
    return [["Taxes the group remits", w * g("direct_receipts").responsive_bn, g("direct_receipts").assigned_bn - g("direct_receipts").responsive_bn, "direct_receipts"],
      ["Corporate, property, asset receipts", w * g("incidence_receipts").responsive_bn, g("incidence_receipts").assigned_bn - g("incidence_receipts").responsive_bn, "incidence_receipts"],
      ["Benefits paid to the group", -w * g("household_transfer").responsive_bn, -(g("household_transfer").assigned_bn - g("household_transfer").responsive_bn), "household_transfer"],
      ["Production gain to other residents", out.private_wtp_bn + w * out.induced_receipts_bn, 0, "production"],
      ["Education", w * edu.effect_bn, -(edu.amount_bn + edu.effect_bn), "education_services"],
      ["Other public services", -w * (g("service").responsive_bn + edu.effect_bn), -((g("service").assigned_bn - edu.amount_bn) - (g("service").responsive_bn + edu.effect_bn)), "service"],
      ["Defense and general government", -w * g("public_goods").responsive_bn, -(g("public_goods").assigned_bn - g("public_goods").responsive_bn), "public_goods"],
      ["Interest and subsidies", -w * (g("interest").responsive_bn + g("subsidy").responsive_bn), -((g("interest").assigned_bn + g("subsidy").assigned_bn) - (g("interest").responsive_bn + g("subsidy").responsive_bn)), "interest subsidy"]];
  }

  function drawBridge() {
    var out = E.evaluate(M, state), steps = bridgeSteps(out, state), cSteps = bridgeSteps(E.evaluate(M, CENTRAL), CENTRAL);
    var run = 0, pts = [0], lo = 0, hi = 0;
    steps.forEach(function (s) { var ghost = run + s[1] + s[2]; run += s[1]; pts.push(run); lo = Math.min(lo, run, ghost); hi = Math.max(hi, run, ghost); });
    var W = 760, rowH = 34, left = 250, right = 70, H = (steps.length + 1) * rowH + 30, x = function (v) { return left + (v - lo) / (hi - lo || 1) * (W - left - right); };
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Bridge from taxes paid to the result"><line class="axis" x1="' + x(0) + '" x2="' + x(0) + '" y1="4" y2="' + (H - 24) + '"/>';
    run = 0;
    steps.forEach(function (s, i) {
      var y = 8 + i * rowH, a = run, b = run + s[1], ghostEnd = b + s[2]; run = b;
      var delta = s[1] - cSteps[i][1];
      svg += '<g class="step" data-affects="' + s[3] + '"><title>' + esc(s[0]) + ": " + signed(s[1], 1) + " bn counted" + (Math.abs(s[2]) > 0.05 ? "; " + fmt(Math.abs(s[2]), 1) + " bn assigned to the group but not counted" : "") + '</title>' +
        '<text class="lab" x="' + (left - 12) + '" y="' + (y + 16) + '" text-anchor="end">' + esc(s[0]) + '</text>';
      if (Math.abs(s[2]) > 0.05) svg += '<rect class="ghost" x="' + Math.min(x(b), x(ghostEnd)) + '" y="' + (y + 4) + '" width="' + Math.abs(x(ghostEnd) - x(b)) + '" height="18" rx="3"/>';
      svg += '<rect class="' + (s[1] < 0 ? "neg" : "pos") + '" x="' + Math.min(x(a), x(b)) + '" y="' + (y + 4) + '" width="' + Math.max(Math.abs(x(b) - x(a)), 1) + '" height="18" rx="3"/>' +
        '<text class="val" x="' + (Math.max(x(a), x(b), x(ghostEnd)) + 6) + '" y="' + (y + 17) + '">' + signed(s[1], 1) + (Math.abs(delta) > 0.05 ? ' <tspan class="dlt">(' + signed(delta, 1) + " vs central)</tspan>" : "") + '</text>' +
        '<line class="link" x1="' + x(b) + '" x2="' + x(b) + '" y1="' + (y + 22) + '" y2="' + (y + rowH + 4) + '"/></g>';
    });
    var yEnd = 8 + steps.length * rowH;
    svg += '<text class="lab tot" x="' + (left - 12) + '" y="' + (yEnd + 16) + '" text-anchor="end">Result</text><rect class="' + (run < 0 ? "neg" : "pos") + ' total" x="' + Math.min(x(0), x(run)) + '" y="' + (yEnd + 3) + '" width="' + Math.max(Math.abs(x(run) - x(0)), 1) + '" height="20" rx="3"/>' +
      '<text class="val tot" x="' + (Math.max(x(0), x(run)) + 6) + '" y="' + (yEnd + 18) + '">' + fmt(run, 1) + ' bn</text></svg>';
    $("bridge").innerHTML = svg;
  }

  function drawTornado() {
    var base = E.evaluate(M, state)[lens];
    var rows = CONTROLS.map(function (k) {
      var ends = k.type === "slider" ? [k.min == null ? 0 : k.min, k.max == null ? 1 : k.max] : k.levels;
      var vals = ends.map(function (v) { var s = E.clone(state); set(s, k.id, v); if (k.id === "school_response") delete s.school_response_band; return { v: v, y: E.evaluate(M, s)[lens] }; });
      vals.sort(function (a, b) { return a.y - b.y; });
      return { k: k, lo: vals[0], hi: vals[vals.length - 1], swing: vals[vals.length - 1].y - vals[0].y };
    }).filter(function (r) { return r.swing > 0.05; }).sort(function (a, b) { return b.swing - a.swing; });
    var lo = Math.min.apply(null, rows.map(function (r) { return r.lo.y; }).concat([base])), hi = Math.max.apply(null, rows.map(function (r) { return r.hi.y; }).concat([base]));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("tornado").innerHTML = rows.map(function (r) {
      return '<li data-affects="' + r.k.affects.join(" ") + '" data-control="' + r.k.id + '"><span class="tl">' + esc(r.k.label) + '</span><span class="tb"><i class="bar" style="left:' + x(r.lo.y) + '%;width:' + (x(r.hi.y) - x(r.lo.y)) + '%"></i><i class="now" style="left:' + x(base) + '%"></i></span>' +
        '<span class="tv">' + fmt(r.lo.y, 0) + " (" + esc(show(r.lo.v)) + ") … " + fmt(r.hi.y, 0) + " (" + esc(show(r.hi.v)) + ")</span></li>";
    }).join("") || "<li>No control moves this outcome.</li>";
    $("tornado-note").textContent = "Each bar: the result across that control's full executed range, everything else held where it is now. The tick marks the current result, " + fmt(base, 1) + " bn.";
  }

  function drawControls() {
    var groups = {}, order = [];
    CONTROLS.forEach(function (k) { if (!groups[k.group]) { groups[k.group] = []; order.push(k.group); } groups[k.group].push(k); });
    $("controls").innerHTML = order.map(function (g) {
      return '<fieldset><legend>' + esc(g) + '</legend>' + groups[g].map(function (k) {
        var v = get(state, k.id), c = get(CENTRAL, k.id), differs = JSON.stringify(v) !== JSON.stringify(c), input;
        if (k.type === "slider") {
          var min = k.min == null ? 0 : k.min, max = k.max == null ? 1 : k.max;
          input = '<input type="range" id="c-' + k.id + '" data-path="' + k.id + '" min="' + min + '" max="' + max + '" step="' + ((max - min) / 100) + '" value="' + v + '"><output>' + show(v) + (k.id === "school_response" && state.school_response_band ? " (band 0.63-0.66)" : "") + '</output>';
        } else {
          input = '<span class="seg">' + k.levels.map(function (l) {
            return '<button type="button" data-path="' + k.id + "\" data-value='" + JSON.stringify(l) + "' class=\"" + (JSON.stringify(l) === JSON.stringify(v) ? "on" : "") + '">' + esc(show(l)) + '</button>'; }).join("") + '</span>';
        }
        return '<div class="ctl' + (differs ? " differs" : "") + '" data-affects="' + k.affects.join(" ") + '"><label for="c-' + k.id + '">' + esc(k.label) + (differs ? '<button type="button" class="reset" data-reset="' + k.id + '" title="Back to the central value">central: ' + esc(show(c)) + '</button>' : "") + '</label>' + input + (k.help ? '<p class="help">' + esc(k.help) + '</p>' : "") + '</div>';
      }).join("") + '</fieldset>';
    }).join("");
  }

  function drawLedger() {
    var out = E.evaluate(M, state);
    function table(lines, side) {
      var groups = {}; lines.forEach(function (l) { (groups[l.group] = groups[l.group] || []).push(l); });
      var max = Math.max.apply(null, lines.map(function (l) { return Math.abs(l.amount_bn); }));
      return Object.keys(groups).map(function (g) {
        var rows = groups[g].filter(function (l) { return Math.abs(l.amount_bn) > 0.005; }).sort(function (a, b) { return Math.abs(b.amount_bn) - Math.abs(a.amount_bn); });
        var sum = rows.reduce(function (s, l) { return s + l.amount_bn; }, 0), counted = rows.reduce(function (s, l) { return s + Math.abs(l.effect_bn); }, 0);
        if (!rows.length) return "";
        return '<tbody data-affects="' + g + '"><tr class="grp"><th colspan="3">' + esc(CLASS_LABEL[g] || g) + '</th><td class="num">' + fmt(sum, 1) + '</td><td class="num">' + fmt(counted, 1) + '</td><td></td></tr>' + rows.map(function (l) {
          var oid = (side === "receipts" ? "receipt:" : "") + l.id, overridden = typeof state.response_override[oid] === "number";
          var keyCell = side === "spending" && l.keys.length > 1 ? '<select data-key="' + l.id + '" id="k-' + l.id + '">' + l.keys.map(function (k) { return '<option' + (k === l.key ? " selected" : "") + '>' + esc(k) + '</option>'; }).join("") + '</select>' : esc(l.key);
          return '<tr data-affects="' + l.id + " " + g + '"><td>' + esc(label(l.id)) + '</td><td class="key">' + keyCell + '</td><td class="num">' + (l.share * 100).toFixed(1) + '%</td><td class="num">' + fmt(l.amount_bn, 1) + '</td>' +
            '<td class="num">' + fmt(Math.abs(l.effect_bn), 1) + '</td><td class="resp"><input type="number" min="0" max="1" step="0.05" id="r-' + oid + '" data-resp="' + oid + '" value="' + (Math.round(l.response * 1000) / 1000) + '"' + (overridden ? ' class="ov"' : "") + '><span class="mini"><i style="width:' + Math.abs(l.amount_bn) / max * 100 + '%"></i><b style="width:' + Math.abs(l.effect_bn) / max * 100 + '%"></b></span></td></tr>';
        }).join("") + '</tbody>';
      }).join("");
    }
    var head = '<thead><tr><th>Line</th><th>Allocated by</th><th class="num">Group share</th><th class="num">Assigned, bn</th><th class="num">Counted, bn</th><th>Response</th></tr></thead>';
    $("ledger-receipts").innerHTML = head + table(out.receipts, "receipts");
    $("ledger-spending").innerHTML = head + table(out.spending, "spending");
  }

  function drawPresetNote() {
    var p = PRESETS.filter(function (q) { return q.id === activePreset; })[0];
    if (!p) { $("preset-note").hidden = true; return; }
    $("preset-note").hidden = false;
    $("preset-note").innerHTML = '<h3>' + esc(p.label) + '</h3><p>' + esc(p.summary) + '</p>' + (p.scope_note ? '<p class="scope">' + esc(p.scope_note) + '</p>' : "") +
      '<table class="basis"><thead><tr><th>Setting</th><th>Basis</th><th>Why</th></tr></thead><tbody>' + (p.settings || []).map(function (s) {
        return '<tr><td>' + esc(s.label || s.path) + (s.path ? ": " + esc(show(s.value)) : "") + '</td><td><span class="tag ' + esc(s.basis) + '">' + esc(s.basis) + '</span></td><td>' + esc(s.note) + (s.ref ? ' <code>' + esc(s.ref) + '</code>' : "") + '</td></tr>'; }).join("") + '</tbody></table>' +
      (p.misses && p.misses.length ? '<h4>Left out of this view of the account</h4><ul>' + p.misses.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' : "");
  }

  function drawContext() {
    var tagText = { inside_headline: "already inside the result", overlaps_headline: "overlaps the result: do not add", outside_not_addable: "outside the account: not addable", different_object: "a different object: compare, never add" };
    $("context").innerHTML = CONTEXT.map(function (c) {
      return '<article><header><span class="tag ' + esc(c.relation_to_headline) + '">' + esc(tagText[c.relation_to_headline] || c.relation_to_headline) + '</span>' + (c.faq_entry ? '<span class="faq">FAQ ' + esc(c.faq_entry) + '</span>' : "") + '</header>' +
        (c.objection ? '<p class="obj">' + esc(c.objection) + '</p>' : "") + '<p>' + esc(c.finding) + '</p><ul>' + (c.values || []).map(function (v) {
          return '<li><b>' + esc(typeof v.value === "number" ? fmt(v.value, Math.abs(v.value) < 10 ? 2 : 0) : v.value) + '</b> ' + esc(v.unit || "") + ' <span>' + esc(v.label) + '</span></li>'; }).join("") + '</ul>' +
        (c.combining_rule ? '<p class="rule">' + esc(c.combining_rule) + '</p>' : "") + '<footer><code>' + esc(c.memo || "") + '</code></footer></article>';
    }).join("") || "<p>No context items were compiled into this build.</p>";
  }

  function render() { drawPresets(); drawHeadline(); drawBridge(); drawTornado(); drawControls(); drawLedger(); drawPresetNote(); }

  function commit(mutator, keepPreset) { history.push(JSON.stringify({ s: state, p: activePreset })); if (history.length > 50) history.shift(); mutator(); if (!keepPreset) activePreset = null; render(); }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-preset],[data-value],[data-reset],[data-lens],#undo,#reset-all"); if (!t) return;
    if (t.dataset.preset) commit(function () { var p = PRESETS.filter(function (q) { return q.id === t.dataset.preset; })[0]; state = presetState(p); activePreset = p.id; }, true);
    else if (t.dataset.value) commit(function () { set(state, t.dataset.path, JSON.parse(t.dataset.value)); });
    else if (t.dataset.reset) commit(function () { set(state, t.dataset.reset, JSON.parse(JSON.stringify(get(CENTRAL, t.dataset.reset)))); if (t.dataset.reset === "school_response") state.school_response_band = CENTRAL.school_response_band; });
    else if (t.dataset.lens) { lens = t.dataset.lens; Array.prototype.forEach.call(document.querySelectorAll("[data-lens]"), function (b) { b.classList.toggle("on", b === t); }); render(); }
    else if (t.id === "undo" && history.length) { var h = JSON.parse(history.pop()); state = h.s; activePreset = h.p; render(); }
    else if (t.id === "reset-all") commit(function () { state = E.clone(CENTRAL); activePreset = "repo_central"; }, true);
  });
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t.type === "range" && t.dataset.path) { set(state, t.dataset.path, parseFloat(t.value)); if (t.dataset.path === "school_response") delete state.school_response_band; activePreset = null; t.nextElementSibling.textContent = show(parseFloat(t.value)); drawPresets(); drawHeadline(); drawBridge(); drawTornado(); drawLedger(); }
  });
  document.addEventListener("change", function (e) {
    var t = e.target;
    if (t.type === "range") { history.push(JSON.stringify({ s: state, p: activePreset })); drawControls(); }
    else if (t.dataset.key) commit(function () { state.key_override[t.dataset.key] = t.value; });
    else if (t.dataset.resp) commit(function () { var v = parseFloat(t.value); if (isFinite(v)) state.response_override[t.dataset.resp] = Math.max(0, Math.min(1, v)); else delete state.response_override[t.dataset.resp]; });
  });
  function highlight(tokens, on) {
    Array.prototype.forEach.call(document.querySelectorAll("[data-affects]"), function (el) {
      var mine = el.dataset.affects.split(" "), hit = on && tokens.some(function (t) { return t === "all" || mine.indexOf(t) >= 0 || mine.indexOf("all") >= 0; });
      el.classList.toggle("lit", !!hit);
    });
  }
  document.addEventListener("mouseover", function (e) { var t = e.target.closest("[data-affects]"); if (t) highlight(t.dataset.affects.split(" "), true); });
  document.addEventListener("mouseout", function (e) { if (e.target.closest("[data-affects]")) highlight([], false); });

  state = E.clone(CENTRAL); activePreset = "repo_central";
  $("scope").textContent = M.meta.target + ": " + (M.meta.target_population / 1e6).toFixed(1) + " million people, income year 2024, " + M.meta.units + ". A stock in a stationary comparison, not the effect of an admission or removal policy.";
  drawContext(); render();
})();
