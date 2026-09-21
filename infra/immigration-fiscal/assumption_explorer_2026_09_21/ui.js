/* Page logic. All numbers come from Engine.evaluate(MODEL, state); this file only draws. */
(function () {
  "use strict";
  var M = window.MODEL, P = window.PRESETS, PRESETS = P.presets, CONTEXT = window.CONTEXT.items || [], EV = window.EVIDENCE, LAD = window.LADDER;
  var E = window.Engine, $ = function (id) { return document.getElementById(id); };
  var state, lens = "welfare_bn", activePreset = null, activeControl = null, history = [];
  var ladder = { q: "", topics: {}, all: false, token: null };

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
    public_order_safety: "Police, courts, prisons, fire (federal agencies included)", general_public_services: "General government (tax collection, administration, legislatures)",
    economic_affairs_services: "Roads, transport, economic affairs", income_security_services: "Welfare administration and services",
    health_services: "Public health services", refundable_tax_credits: "Refundable tax credits (EITC, CTC)",
    snap: "SNAP", ssi: "SSI", recreation_culture: "Parks, recreation, culture", housing_community_services: "Housing and community services"
  };
  function label(id) { return LABEL[id] || id.replace(/_/g, " ").replace(/^./, function (c) { return c.toUpperCase(); }); }
  var CLASS_LABEL = { direct_receipts: "Taxes households remit directly", incidence_receipts: "Corporate, property and asset receipts (incidence only)",
    household_transfer: "Cash and in-kind benefits", service: "Public services", public_goods: "Defense and general government",
    interest: "Interest on existing debt", subsidy: "Business and housing subsidies", foreign: "Foreign flows", rounding: "Rounding" };

  function elasticity(name) { var r = EV.elasticities.filter(function (x) { return x.scope === "50 states" && x.function.indexOf(name) === 0; })[0]; return r ? r.elasticity : null; }
  var gps = EV.general_public_service_2024_bn;
  var GG_HELP = "Held at zero in the published account BY ASSUMPTION. " + Math.round(EV.state_local_share * 100) + "% of general government outside interest is state and local; across the 50 states administration spending has a population elasticity of " +
    elasticity("Governmental administration") + " (police " + elasticity("Police") + ", schools " + elasticity("Elementary") + "). Federal tax collection and financial management is $" + gps.federal_tax_financial.toFixed(1) +
    "bn, federal executive and legislative $" + gps.federal_executive_legislative.toFixed(1) + "bn. Implied response " + EV.composite_low + " to " + EV.composite_high + ". Federal police, courts and prisons (FBI included) are not here: they are already charged under police, courts, prisons.";

  var levels = function (d) { return M.production.dims[d]; };
  var CONTROLS = [
    { group: "What counts as a cost", id: "service_response", label: "Public services that scale with population", type: "slider", marks: [0, 0.5, 1],
      help: "Share of schools, police, health and other services assumed to shrink if the group were absent. 1 = average cost; 0 = services are free at the margin. The account executes 0, 0.5 and 1.", affects: ["service"] },
    { group: "What counts as a cost", id: "school_response", label: "K-12 school budgets respond", type: "slider", marks: [0.63, 0.66],
      help: "CBO's evidence puts the school-spending response at 63-66%. Applies to the school share of education only.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "school_share", label: "School share of education spending", type: "slider", min: E.schoolShareBounds(M)[0], max: E.schoolShareBounds(M)[1],
      help: "National bounds 71.5-86.5%, transported to this group under a common-composition assumption.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "other_education_response", label: "Colleges and other education respond", type: "slider", affects: ["education_services"],
      help: "No estimate exists; the account runs both 0 and 1." },
    { group: "What counts as a cost", id: "delayed_response", label: "Roads, economic affairs, parks respond", type: "slider", affects: ["economic_affairs_services", "recreation_culture"],
      help: "Slow-adjusting categories. The CBO-informed headline holds them fixed (0)." },
    { group: "What counts as a cost", id: "general_government_response", label: "General government responds", type: "slider", marks: [EV.composite_low, EV.composite_high], affects: ["general_public_services"], help: GG_HELP },
    { group: "What counts as a cost", id: "public_goods_response", label: "Defense responds", type: "slider", affects: ["defense"],
      help: "Held at zero: defense depends on other countries and operations, not on the number of residents. Intelligence agencies are funded largely through the defense budget. 1 charges the full per-capita share." },
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
  var BY_ID = {}; CONTROLS.forEach(function (k) { BY_ID[k.id] = k; });
  var PATHS = CONTROLS.map(function (c) { return c.id; }).concat(["school_response_band", "key_override", "response_override"]);

  function get(s, p) { return p.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, s); }
  function set(s, p, v) { var ks = p.split("."), o = s; for (var i = 0; i < ks.length - 1; i++) o = o[ks[i]]; if (v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = v; }
  function fmt(x, d) { if (x == null || !isFinite(x)) return "n/a"; var r = Math.abs(x).toFixed(d == null ? 1 : d), s = r.replace(/\B(?=(\d{3})+(?!\d))/g, ","); return (x < 0 && parseFloat(r) !== 0 ? "−" : "") + s; }
  function fmtAuto(x) { return fmt(x, Math.abs(x) < 9.95 ? 1 : 0); }  // whole billions, one decimal below ten
  function signed(x, d) { return (x > 1e-9 ? "+" : "") + fmt(x, d); }
  function show(v) { return typeof v === "number" ? String(Math.round(v * 1000) / 1000) : v === true ? "yes" : v === false ? "no" : String(v).replace(/_/g, " "); }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

  function presetState(p) {
    var s = E.defaultState(M);
    (p.settings || []).forEach(function (x) { if (x.path) set(s, x.path, JSON.parse(JSON.stringify(x.value))); });
    return s;
  }
  var CENTRAL = presetState(PRESETS.filter(function (p) { return p.id === "repo_central"; })[0]);
  function centralText(k) { return k.id === "school_response" && CENTRAL.school_response_band ? CENTRAL.school_response_band.join("–") : show(get(CENTRAL, k.id)); }

  function outcome(s, key) {
    var out = E.evaluate(M, s), range = E.unresolvedRange(M, s, key || lens);
    return { out: out, value: out[key || lens], range: range };
  }

  function executedStatus(s) {
    var d = E.defaultState(M), contract = ["transfer_response", "interest_response", "subsidy_response", "direct_receipt_response", "indirect_receipt_response"]
      .every(function (k) { return s[k] === d[k]; }) && !Object.keys(s.key_override).length && !Object.keys(s.response_override).length && s.count_production;
    if (!contract) return ["own", "Your own assumption set: same formula, settings the account never ran"];
    var flat = s.school_response === 1 && s.other_education_response === 1 && s.delayed_response === 1 && !s.school_response_band;
    var onLevels = [0, 0.5, 1].indexOf(s.service_response) >= 0 && [0, 1].indexOf(s.public_goods_response) >= 0 && s.general_government_response === s.public_goods_response && [0, 1].indexOf(s.fiscal_weight) >= 0;
    if (flat && onLevels && s.service_response === s.production.capital_adjustment) return ["grid", "Executed case: a row of the 497,664-row scenario grid"];
    var ref = M.production.reference, atRef = E.PRODUCTION_DIMS.every(function (k) { return k === "normalization" || s.production[k] === ref[k]; });
    if (atRef && s.service_response === 1 && s.public_goods_response === 0 && s.general_government_response === 0 && s.fiscal_weight === 1 && s.receipt_scenario === M.receipts.reference && s.spending_keys === "preferred")
      return ["grid", "Executed case: a category service-response case at the reference production scenario"];
    return ["formula", "Exact formula, off the executed grid: the account is linear in these responses"];
  }

  /* ---------- drawing ---------- */
  var LENS_SHORT = { welfare_bn: "Effect on other US residents", target_balance_bn: "Accounting balance of the group", normalized_gap_bn: "Versus an equal per-capita share" };

  function drawBar() {
    var o = outcome(state), c = outcome(CENTRAL), diff = o.value - c.value;
    $("b-name").textContent = LENS_SHORT[lens];
    $("b-value").textContent = fmt(o.value, 1); $("b-value").className = o.value < 0 ? "neg" : "pos";
    $("b-range").textContent = "span " + fmtAuto(o.range[0]) + " to " + fmtAuto(o.range[1]);
    $("b-delta").textContent = Math.abs(diff) < 0.05 ? "= central case" : "central " + fmt(c.value, 1) + " · " + signed(diff, 1) + " from it";
    var k = BY_ID[activeControl];
    if (!k) { $("b-active").textContent = "Drag a slider or pick an option: this bar stays in view and shows the setting next to its central value."; return; }
    var back = E.clone(state); set(back, k.id, JSON.parse(JSON.stringify(get(CENTRAL, k.id)))); if (k.id === "school_response") back.school_response_band = CENTRAL.school_response_band;
    var alone = o.value - E.evaluate(M, back)[lens];
    $("b-active").innerHTML = "<b>" + esc(k.label) + "</b>: " + esc(show(get(state, k.id))) + " · central " + esc(centralText(k)) +
      (same(get(state, k.id), get(CENTRAL, k.id)) ? " · at its central value" : Math.abs(alone) < 0.05 ? " · no effect on this outcome" : " · this setting alone: " + signed(alone, 1) + " bn");
  }

  function drawPresets() {
    var cards = PRESETS.map(function (p) { return { p: p, v: outcome(presetState(p)) }; });
    if (!activePreset) cards.unshift({ p: { id: "", kind_label: "Live", label: "Your current settings" }, v: outcome(state), current: true });
    var lo = Math.min.apply(null, cards.map(function (c) { return Math.min(c.v.range[0], 0); })), hi = Math.max.apply(null, cards.map(function (c) { return Math.max(c.v.range[1], 0); }));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("presets").innerHTML = cards.map(function (c) {
      var v = c.v, a = x(Math.min(v.range[0], v.range[1])), b = x(Math.max(v.range[0], v.range[1]));
      var inner = '<span class="pk">' + esc(c.p.kind_label) + '</span><span class="pl">' + esc(c.p.label) + '</span>' +
        '<span class="pv">' + fmtAuto(v.range[0]) + (Math.abs(v.range[1] - v.range[0]) > 0.5 ? " to " + fmtAuto(v.range[1]) : "") + '</span>' +
        '<span class="track"><i class="zero" style="left:' + x(0) + '%"></i><i class="span ' + (v.value < 0 ? "neg" : "pos") + '" style="left:' + a + '%;width:' + Math.max(b - a, 0.8) + '%"></i></span>';
      return c.current ? '<div class="preset current">' + inner + '</div>'
        : '<button class="preset' + (activePreset === c.p.id ? " on" : "") + '" data-preset="' + c.p.id + '" id="preset-' + c.p.id + '">' + inner + '</button>';
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
    var parts, exact = true;
    try { parts = E.attribute(M, CENTRAL, state, PATHS, lens); }
    catch (err) {  // too many changed controls for exact Shapley: fall back to one at a time
      exact = false;
      parts = PATHS.filter(function (p) { return !same(get(CENTRAL, p), get(state, p)); }).map(function (p) {
        var s = E.clone(CENTRAL); set(s, p, E.clone({ v: get(state, p) }).v); return { path: p, from: get(CENTRAL, p), to: get(state, p), effect_bn: E.evaluate(M, s)[lens] - c.value }; });
    }
    parts = parts.filter(function (p) { return Math.abs(p.effect_bn) > 0.05; }).sort(function (a, b) { return Math.abs(b.effect_bn) - Math.abs(a.effect_bn); });
    $("diff-title").textContent = parts.length ? "Distance from the central case: " + signed(o.value - c.value, 1) + " bn, " + (exact ? "split exactly across the assumptions that differ" : "each assumption changed alone (too many differ to split interactions)")
      : "This is the repo's central case";
    var max = Math.max.apply(null, parts.map(function (p) { return Math.abs(p.effect_bn); }).concat([1]));
    $("diff").innerHTML = parts.map(function (p) {
      var k = BY_ID[p.path] || { label: p.path.replace(/_/g, " ") };
      return '<li data-affects="' + (k.affects || []).join(" ") + '"><span class="dl">' + esc(k.label) + '<em>' + esc(show(p.from)) + " → " + esc(show(p.to)) + '</em></span>' +
        '<span class="db"><i class="' + (p.effect_bn < 0 ? "neg" : "pos") + '" style="width:' + Math.abs(p.effect_bn) / max * 100 + '%"></i></span><span class="dv">' + signed(p.effect_bn, 1) + '</span></li>';
    }).join("");
  }

  function bridgeSteps(out, s) {
    var w = s.fiscal_weight, c = out.classes, g = function (k) { return c[k] || { assigned_bn: 0, responsive_bn: 0 }; };
    var edu = out.spending.filter(function (l) { return l.id === "education_services"; })[0], PG = "public_goods defense general_public_services";
    if (lens !== "welfare_bn") {
      var steps = [["Taxes remitted directly", g("direct_receipts").assigned_bn, 0, "direct_receipts"], ["Corporate, property, asset receipts", g("incidence_receipts").assigned_bn, 0, "incidence_receipts"],
        ["Benefits received", -g("household_transfer").assigned_bn, 0, "household_transfer"], ["Education", -edu.amount_bn, 0, "education_services"],
        ["Other public services", -(g("service").assigned_bn - edu.amount_bn), 0, "service"], ["Defense and general government", -g("public_goods").assigned_bn, 0, PG],
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
      ["Defense and general government", -w * g("public_goods").responsive_bn, -(g("public_goods").assigned_bn - g("public_goods").responsive_bn), PG],
      ["Interest and subsidies", -w * (g("interest").responsive_bn + g("subsidy").responsive_bn), -((g("interest").assigned_bn + g("subsidy").assigned_bn) - (g("interest").responsive_bn + g("subsidy").responsive_bn)), "interest subsidy"]];
  }

  function drawBridge() {
    var out = E.evaluate(M, state), steps = bridgeSteps(out, state), cSteps = bridgeSteps(E.evaluate(M, CENTRAL), CENTRAL);
    var run = 0, lo = 0, hi = 0;
    steps.forEach(function (s) { var ghost = run + s[1] + s[2]; run += s[1]; lo = Math.min(lo, run, ghost); hi = Math.max(hi, run, ghost); });
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
        '<span class="tv">' + fmtAuto(r.lo.y) + " (" + esc(show(r.lo.v)) + ") … " + fmtAuto(r.hi.y) + " (" + esc(show(r.hi.v)) + ")</span></li>";
    }).join("") || "<li>No control moves this outcome.</li>";
    $("tornado-note").textContent = "Each bar: the result across that control's full range, everything else held where it is now. The tick marks the current result, " + fmt(base, 1) + " bn.";
  }

  function drawControls() {
    var groups = {}, order = [];
    CONTROLS.forEach(function (k) { if (!groups[k.group]) { groups[k.group] = []; order.push(k.group); } groups[k.group].push(k); });
    $("controls").innerHTML = order.map(function (g) {
      return '<fieldset><legend>' + esc(g) + '</legend>' + groups[g].map(function (k) {
        var v = get(state, k.id), c = get(CENTRAL, k.id), differs = !same(v, c), input;
        if (k.type === "slider") {
          var min = k.min == null ? 0 : k.min, max = k.max == null ? 1 : k.max, pos = function (val) { return "calc(8px + (100% - 16px) * " + ((val - min) / (max - min || 1)) + ")"; };
          input = '<span class="rng"><input type="range" id="c-' + k.id + '" data-path="' + k.id + '" min="' + min + '" max="' + max + '" step="' + ((max - min) / 100) + '" value="' + v + '">' +
            (k.marks || []).map(function (m) { return '<i class="xm" style="left:' + pos(m) + '"></i>'; }).join("") + '<i class="cm" title="central value" style="left:' + pos(c) + '"></i></span><output>' + show(v) + '</output>';
        } else {
          input = '<span class="seg">' + k.levels.map(function (l) {
            return '<button type="button" data-path="' + k.id + "\" data-value='" + JSON.stringify(l) + "' class=\"" + (same(l, v) ? "on" : "") + (same(l, c) ? " central" : "") + '">' + esc(show(l)) + '</button>'; }).join("") + '</span>';
        }
        return '<div class="ctl' + (differs ? " differs" : "") + '" data-control="' + k.id + '" data-affects="' + k.affects.join(" ") + '"><label for="c-' + k.id + '"><span>' + esc(k.label) + '</span>' +
          (differs ? '<button type="button" class="reset" data-reset="' + k.id + '" title="Back to the central value">back to ' + esc(centralText(k)) + '</button>' : '<span class="cval">central ' + esc(centralText(k)) + '</span>') + '</label>' + input + (k.help ? '<p class="help">' + esc(k.help) + '</p>' : "") + '</div>';
      }).join("") + '</fieldset>';
    }).join("");
  }

  function ladderVisible(card) { return ladder.all || card.status === "current"; }
  function findings(token) { return LAD.cards.filter(function (c) { return ladderVisible(c) && c.affects.indexOf(token) >= 0; }).length; }
  function findButton(token) { var n = findings(token); return n ? '<button type="button" class="find" data-find="' + token + '">' + n + ' ladder entr' + (n === 1 ? "y" : "ies") + '</button>' : ""; }

  function drawLedger() {
    var out = E.evaluate(M, state);
    function table(lines, side) {
      var groups = {}; lines.forEach(function (l) { (groups[l.group] = groups[l.group] || []).push(l); });
      var max = Math.max.apply(null, lines.map(function (l) { return Math.abs(l.amount_bn); }));
      return Object.keys(groups).map(function (g) {
        var rows = groups[g].filter(function (l) { return Math.abs(l.amount_bn) > 0.005; }).sort(function (a, b) { return Math.abs(b.amount_bn) - Math.abs(a.amount_bn); });
        var sum = rows.reduce(function (s, l) { return s + l.amount_bn; }, 0), counted = rows.reduce(function (s, l) { return s + Math.abs(l.effect_bn); }, 0);
        if (!rows.length) return "";
        return '<tbody data-affects="' + g + '"><tr class="grp"><th colspan="3">' + esc(CLASS_LABEL[g] || g) + findButton(g) + '</th><td class="num">' + fmt(sum, 1) + '</td><td class="num">' + fmt(counted, 1) + '</td><td></td></tr>' + rows.map(function (l) {
          var oid = (side === "receipts" ? "receipt:" : "") + l.id, overridden = typeof state.response_override[oid] === "number";
          var keyCell = side === "spending" && l.keys.length > 1 ? '<select data-key="' + l.id + '" id="k-' + l.id + '">' + l.keys.map(function (k) { return '<option' + (k === l.key ? " selected" : "") + '>' + esc(k) + '</option>'; }).join("") + '</select>' : esc(l.key);
          return '<tr data-affects="' + l.id + " " + g + '"><td>' + esc(label(l.id)) + findButton(l.id) + '</td><td class="key">' + keyCell + '</td><td class="num">' + (l.share * 100).toFixed(1) + '%</td><td class="num">' + fmt(l.amount_bn, 1) + '</td>' +
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
      '<div class="scroll"><table class="basis"><thead><tr><th>Setting</th><th>Basis</th><th>Why</th></tr></thead><tbody>' + (p.settings || []).map(function (s) {
        return '<tr><td>' + esc(s.label || s.path) + (s.path ? ": " + esc(show(s.value)) : "") + '</td><td><span class="tag ' + esc(s.basis) + '">' + esc(String(s.basis).replace(/_/g, " ")) + '</span></td><td>' + esc(s.note) + (s.ref ? ' <code>' + esc(s.ref) + '</code>' : "") + '</td></tr>'; }).join("") + '</tbody></table></div>' +
      (p.misses && p.misses.length ? '<h4>Left out of this view of the account</h4><ul>' + p.misses.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' : "");
  }

  function drawStanding() {
    $("standing-title").textContent = P.standing.title;
    $("standing").innerHTML = '<tbody>' + P.standing.rows.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>'; }).join("") + '</tbody>';
    $("standing-text").textContent = P.standing.text;
  }

  function drawAuthors() {
    $("authors").innerHTML = P.authors.map(function (a) {
      var target = PRESETS.filter(function (p) { return p.id === a.closest.preset; })[0];
      return '<article><h3>' + esc(a.name) + '</h3>' + a.argues.map(function (x) { return '<p class="q">' + esc(x[0]) + ' <code>' + esc(x[1]) + '</code></p>'; }).join("") +
        '<p><b>What the claim is about:</b> ' + esc(a.object) + '</p><p><b>Closest convention in this ledger:</b> ' +
        (target ? '<button type="button" class="link" data-preset="' + target.id + '">' + esc(target.label) + '</button>. ' : '<span class="tag not_addressed">none</span> ') + esc(a.closest.why) + '</p>' +
        '<h4>The argument leaves out</h4><ul>' + a.leaves_out.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul></article>';
    }).join("");
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

  function drawLadder() {
    var q = ladder.q.trim().toLowerCase(), chosen = Object.keys(ladder.topics).filter(function (t) { return ladder.topics[t]; });
    var cards = LAD.cards.filter(function (c) {
      return ladderVisible(c) && (!q || c.text.toLowerCase().indexOf(q) >= 0 || String(c.n) === q) && (!chosen.length || chosen.some(function (t) { return c.topics.indexOf(t) >= 0; })) && (!ladder.token || c.affects.indexOf(ladder.token) >= 0);
    });
    var counts = { current: 0, qualified: 0, historical: 0 }; LAD.cards.forEach(function (c) { counts[c.status] += 1; });
    $("ladder-note").textContent = "The confidence ladder (" + LAD.source + "), parsed when this page was built: " + LAD.cards.length + " entries in the ladder's own words (" + counts.current + " current, " + counts.qualified +
      " qualified by a later correction, " + counts.historical + " from the dated earlier layers). Status is mechanical and the topic chips and ledger links are keyword rules: a way in, not a classification. Showing " + cards.length + ".";
    $("ladder-topics").innerHTML = (ladder.token ? '<button type="button" class="chip on" data-find="">linked to: ' + esc(label(ladder.token)) + ' ×</button>' : "") +
      LAD.topics.map(function (t) { return '<button type="button" class="chip' + (ladder.topics[t] ? " on" : "") + '" data-topic="' + esc(t) + '">' + esc(t) + '</button>'; }).join("");
    $("ladder").innerHTML = cards.map(function (c) {
      var short = c.text.length > 230 ? c.text.slice(0, 230).replace(/\s+\S*$/, "") + " …" : c.text;
      return '<details class="' + c.status + '" data-affects="' + c.affects.join(" ") + '"><summary><span class="n">' + c.n + '</span><span>' + esc(short) + '</span></summary><p class="body">' + esc(c.text) + '</p>' +
        (c.note ? '<p class="rule">' + esc(c.note) + '</p>' : "") + '<div class="meta"><span class="tag ' + c.status + '">' + c.status + '</span>' + c.topics.map(function (t) { return '<span class="tag">' + esc(t) + '</span>'; }).join("") +
        '<code>' + esc(LAD.source) + ":" + c.line + '</code></div></details>';
    }).join("") || "<p>No entry matches.</p>";
  }

  function renderLive() { drawBar(); drawPresets(); drawHeadline(); drawBridge(); drawTornado(); drawLedger(); }
  function render() { renderLive(); drawControls(); drawPresetNote(); }
  function commit(mutator, keepPreset) { history.push(JSON.stringify({ s: state, p: activePreset })); if (history.length > 50) history.shift(); mutator(); if (!keepPreset) activePreset = null; render(); }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-preset],[data-value],[data-reset],[data-lens],[data-find],[data-topic],#undo,#reset-all"); if (!t) return;
    if (t.dataset.preset) { commit(function () { var p = PRESETS.filter(function (q) { return q.id === t.dataset.preset; })[0]; state = presetState(p); activePreset = p.id; activeControl = null; }, true); if (t.classList.contains("link")) window.scrollTo({ top: 0, behavior: "smooth" }); }
    else if (t.dataset.value) { activeControl = t.dataset.path; commit(function () { set(state, t.dataset.path, JSON.parse(t.dataset.value)); }); }
    else if (t.dataset.reset) { activeControl = t.dataset.reset; commit(function () { set(state, t.dataset.reset, JSON.parse(JSON.stringify(get(CENTRAL, t.dataset.reset)))); if (t.dataset.reset === "school_response") state.school_response_band = CENTRAL.school_response_band; }); }
    else if (t.dataset.lens) { lens = t.dataset.lens; Array.prototype.forEach.call(document.querySelectorAll("[data-lens]"), function (b) { b.classList.toggle("on", b === t); }); render(); }
    else if (t.dataset.find !== undefined) { ladder.token = t.dataset.find || null; drawLadder(); if (ladder.token) $("ladder-section").scrollIntoView({ behavior: "smooth" }); }
    else if (t.dataset.topic) { ladder.topics[t.dataset.topic] = !ladder.topics[t.dataset.topic]; drawLadder(); }
    else if (t.id === "undo" && history.length) { var h = JSON.parse(history.pop()); state = h.s; activePreset = h.p; render(); }
    else if (t.id === "reset-all") commit(function () { state = E.clone(CENTRAL); activePreset = "repo_central"; activeControl = null; }, true);
  });
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t.type === "range" && t.dataset.path) {
      set(state, t.dataset.path, parseFloat(t.value)); if (t.dataset.path === "school_response") delete state.school_response_band;
      activePreset = null; activeControl = t.dataset.path;
      var box = t.closest(".ctl"); box.querySelector("output").textContent = show(parseFloat(t.value));
      box.classList.toggle("differs", !same(get(state, t.dataset.path), get(CENTRAL, t.dataset.path)));
      renderLive();
    } else if (t.id === "ladder-q") { ladder.q = t.value; drawLadder(); }
  });
  document.addEventListener("change", function (e) {
    var t = e.target;
    if (t.type === "range") { history.push(JSON.stringify({ s: state, p: activePreset })); drawControls(); drawPresetNote(); }
    else if (t.id === "ladder-all") { ladder.all = t.checked; drawLadder(); drawLedger(); }
    else if (t.dataset.key) commit(function () { state.key_override[t.dataset.key] = t.value; });
    else if (t.dataset.resp) commit(function () { var v = parseFloat(t.value); if (isFinite(v)) state.response_override[t.dataset.resp] = Math.max(0, Math.min(1, v)); else delete state.response_override[t.dataset.resp]; });
  });
  function highlight(tokens, on) {
    Array.prototype.forEach.call(document.querySelectorAll("[data-affects]"), function (el) {
      var mine = el.dataset.affects.split(" "), hit = on && tokens.some(function (t) { return t && (t === "all" || mine.indexOf(t) >= 0 || mine.indexOf("all") >= 0); });
      el.classList.toggle("lit", !!hit);
    });
  }
  document.addEventListener("mouseover", function (e) {
    var t = e.target.closest("[data-affects]"); if (t) highlight(t.dataset.affects.split(" "), true);
    var c = e.target.closest("[data-control]"); if (c && c.dataset.control !== activeControl) { activeControl = c.dataset.control; drawBar(); }
  });
  document.addEventListener("mouseout", function (e) { if (e.target.closest("[data-affects]")) highlight([], false); });

  state = E.clone(CENTRAL); activePreset = "repo_central";
  $("scope").textContent = M.meta.target + ": " + (M.meta.target_population / 1e6).toFixed(1) + " million people, income year 2024, " + M.meta.units + ". A stock in a stationary comparison, not the effect of an admission or removal policy.";
  drawStanding(); drawAuthors(); drawContext(); drawLadder(); render();
})();
