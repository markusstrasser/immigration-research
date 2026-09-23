/* Page logic. All numbers come from Engine.evaluate(MODEL, state); this file only draws. */
(function () {
  "use strict";
  var M = window.MODEL, P = window.PRESETS, PRESETS = P.presets, CONTEXT = window.CONTEXT.items || [], EV = window.EVIDENCE, LAD = window.LADDER, SRC = window.SOURCES;
  var E = window.Engine, $ = function (id) { return document.getElementById(id); };
  var state, lens = "welfare_bn", activePreset = null, activeControl = null, history = [];
  var ladder = { q: "", topics: {}, all: false, token: null };
  var SMOOTH = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";

  var LABEL = {
    federal_income_tax: "Federal income tax", employer_oasdi: "Social Security tax, employer half",
    employee_oasdi: "Social Security tax, employee half", general_sales_tax: "General sales tax",
    excise_selective_sales: "Excise and selective sales taxes", state_local_income_tax: "State and local income tax",
    modeled_owner_property: "Property tax, owner-occupied (modeled)", government_asset_income: "Government asset income",
    employee_hi: "Medicare tax, employee half", corporate_capital: "Corporate tax borne by capital",
    employer_hi: "Medicare tax, employer half", corporate_labor: "Corporate tax borne by labor",
    personal_current_transfers: "Fees, fines and personal transfers", remaining_production_property: "Property tax, business and rental",
    other_domestic_social_contributions: "Other social contributions", self_employment_oasdi_hi: "Self-employment payroll tax",
    medicare_supplementary_premiums: "Medicare premiums", customs_duties: "Customs duties",
    other_production_taxes: "Other production taxes", business_current_transfers: "Business transfers to government",
    personal_motor_vehicle: "Motor vehicle licenses", other_personal_tax: "Other personal taxes",
    personal_property_tax: "Personal property tax", enterprise_surplus: "Government enterprise surplus",
    education_services: "Education (schools and colleges)", domestic_interest: "Interest on existing debt",
    medicaid_and_chip_other_medical: "Medicaid, CHIP and other medical", defense: "National defense",
    public_order_safety: "Police, courts, prisons, fire (federal agencies included)", general_public_services: "General government (tax collection, administration, legislatures)",
    economic_affairs_services: "Roads, transport, economic affairs", income_security_services: "Welfare administration and services",
    health_services: "Public health services", refundable_tax_credits: "Refundable tax credits (EITC, CTC)",
    snap: "SNAP", ssi: "SSI", recreation_culture: "Parks, recreation, culture", housing_community_services: "Housing and community services",
    social_security: "Social Security", veterans_pension_disability: "Veterans' pensions and disability", rest_world_tax_contributions: "Taxes and contributions from abroad",
    rest_world_current_transfers: "Transfers from abroad", source_rounding: "Rounding in the source tables"
  };
  function label(id) { return LABEL[id] || id.replace(/_/g, " ").replace(/^./, function (c) { return c.toUpperCase(); }); }
  var CLASS_LABEL = { direct_receipts: "Taxes the group pays", incidence_receipts: "Corporate, property and asset receipts",
    household_transfer: "Cash and in-kind benefits", service: "Public services", public_goods: "Defense and general government",
    interest: "Interest on existing debt", subsidy: "Business and housing subsidies", foreign: "Foreign flows", rounding: "Rounding" };

  function elasticity(name) { var r = EV.elasticities.filter(function (x) { return x.scope === "50 states" && x.function.indexOf(name) === 0; })[0]; return r ? r.elasticity : null; }
  var gps = EV.general_public_service_2024_bn;
  var GG_HELP = "The account published on September 20 held this at zero by assumption; the central case adopted on 2026-09-23 lets it grow. " + Math.round(EV.state_local_share * 100) + "% of general government outside interest is state and local. Across the 50 states, administration spending rises " +
    (elasticity("Governmental administration") * 10).toFixed(1) + "% for every 10% more residents (police " + (elasticity("Police") * 10).toFixed(1) + "%, schools " + (elasticity("Elementary") * 10).toFixed(1) + "%). Federal tax collection costs $" + gps.federal_tax_financial.toFixed(1) +
    "bn; the federal executive and legislature $" + gps.federal_executive_legislative.toFixed(1) + "bn. Together that implies a share between " + EV.composite_low + " and " + EV.composite_high + "; the central case enters both. Federal police, courts and prisons, the FBI among them, are charged under police, courts, prisons.";

  var levels = function (d) { return M.production.dims[d]; };
  var CONTROLS = [
    { group: "What counts as a cost", id: "service_response", label: "Public services grow with the population", type: "slider", marks: [0, 0.5, 1],
      help: "How much of schools, police, health and other services would not be needed if the group were absent. 1 charges the average cost per person; 0 treats services as free to add people to. The account was run at 0, 0.5 and 1.", affects: ["service"] },
    { group: "What counts as a cost", id: "school_response", label: "School spending grows with enrollment", type: "slider", marks: [0.63, 0.66],
      help: "Derived from CBO's panel of states: spending per pupil grows 0.37 points slower for each point of enrollment growth, and 0.34 points faster for each point of decline, so total spending moves 63-66% as much as enrollment. An association across states; CBO does not present it as a causal long-run estimate. Applies to the school part of education only.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "school_share", label: "School share of education spending", type: "slider", min: E.schoolShareBounds(M)[0], max: E.schoolShareBounds(M)[1],
      help: "Nationally between 71.5% and 86.5%, depending on how college spending is counted. The account assumes the group's mix matches the nation's.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "other_education_response", label: "College and other education spending grows with enrollment", type: "slider", affects: ["education_services"],
      help: "No estimate exists. The account runs both 0 and 1." },
    { group: "What counts as a cost", id: "delayed_response", label: "Roads, economic affairs and parks grow with the population", type: "slider", affects: ["economic_affairs_services", "recreation_culture"],
      help: "These budgets adjust slowly. The central case holds them fixed (0)." },
    { group: "What counts as a cost", id: "general_government_response", label: "General government grows with the population", type: "slider", marks: [EV.composite_low, EV.composite_high], affects: ["general_public_services"], help: GG_HELP },
    { group: "What counts as a cost", id: "public_goods_response", label: "Defense grows with the population", type: "slider", affects: ["defense"],
      help: "Held at zero: defense spending follows other countries and operations. Intelligence agencies are funded largely through the defense budget. 1 charges a full per-head share." },
    { group: "What counts as a cost", id: "interest_response", label: "Interest on existing debt grows with the population", type: "slider", affects: ["interest"],
      help: "Debt already issued does not shrink when fewer people live here. Zero in every case the account ran." },
    { group: "What counts as a cost", id: "transfer_response", label: "Benefits paid to the group count as a cost", type: "slider", affects: ["household_transfer"],
      help: "Medicaid, Social Security, Medicare, tax credits. 1 in every case the account ran." },
    { group: "What counts as revenue", id: "direct_receipt_response", label: "Taxes the group pays count as revenue", type: "slider", affects: ["direct_receipts"],
      help: "Income, payroll, sales and excise taxes. 1 in every case the account ran." },
    { group: "What counts as revenue", id: "indirect_receipt_response", label: "Corporate and property taxes assigned to the group count as revenue", type: "slider", affects: ["incidence_receipts"],
      help: "Nobody in the group writes these checks; a rule assigns them a share. 0 in the account, because the production side already counts the same income." },
    { group: "What counts as revenue", id: "receipt_scenario", label: "Who is assumed to bear each tax", type: "levels", levels: M.receipts.scenarios, affects: ["direct_receipts", "incidence_receipts"],
      help: "Rule sets the account ran, each changing one rule from CBO's. Only CBO's, the Treasury's and the National Academies' rest on a published source; the others are stress tests the account declares itself." },
    { group: "Production side", id: "count_production", label: "Count what the group's work adds to other residents' incomes", type: "levels", levels: [true, false], affects: ["production"],
      help: "The gain to everyone else from the group's labor, plus the extra tax that gain generates, from a standard production model. A tally of taxes and spending leaves it out." },
    { group: "Production side", id: "production.sigma", label: "How easily workers of different skill replace each other", type: "levels", levels: levels("sigma"), affects: ["production"], help: "Economists call this the elasticity of substitution. Higher means closer substitutes and a smaller gain. The three values follow the range in Colas and Sachs." },
    { group: "Production side", id: "production.capital_adjustment", label: "Investment has caught up with the larger workforce", type: "levels", levels: levels("capital_adjustment"), affects: ["production"],
      help: "0 is the short run, with capital fixed and a large gain to its owners; 1 is the long run. The account's runs pair this with the service setting as one path of adjustment." },
    { group: "Production side", id: "production.labor_share", label: "Labor's share of income", type: "levels", levels: levels("labor_share"), affects: ["production"], help: "The share of national income paid to workers, the rest going to owners of capital. The account cites no source for these three values." },
    { group: "Production side", id: "production.labor_supply_elasticity", label: "How much other residents' hours respond to wages", type: "levels", levels: levels("labor_supply_elasticity"), affects: ["production"], help: "0 means hours do not change when wages move. The account cites no source for these two values." },
    { group: "Production side", id: "production.capital_tax_retention", label: "Share of the capital-tax gain government keeps", type: "levels", levels: levels("capital_tax_retention"), affects: ["production"], help: "The group's work raises returns to capital, and some of that comes back as tax. Nobody has estimated how much stays with government, so the account runs 0, 0.5 and 1." },
    { group: "Production side", id: "production.excluded_capital_owner_share", label: "Capital owned by people outside the count", type: "levels", levels: levels("excluded_capital_owner_share"), affects: ["production"],
      help: "0 gives every capital gain to other US residents, the most favorable case. 0.5 and 1 are endpoints nobody has estimated." },
    { group: "Production side", id: "production.split", label: "Which workers compete with the group", type: "levels", levels: levels("split"), affects: ["production"], help: "Where the line between the two skill groups is drawn." },
    { group: "Production side", id: "production.proxy", label: "Earnings measure", type: "levels", levels: levels("proxy"), affects: ["production"], help: "Total earnings including self-employment, or wage and salary income alone." },
    { group: "Choices the account leaves open", id: "allocation", label: "Household money", type: "levels", levels: ["personal", "shared"], affects: ["all"], help: "Personal counts each person's own taxes and benefits; shared pools them within the household. The published range covers both." },
    { group: "Choices the account leaves open", id: "production.normalization", label: "How the production gain is scaled", type: "levels", levels: levels("normalization"), affects: ["production"], help: "The model's output is set equal either to national GDP or to the earnings reported in the survey divided by labor's share. The published range covers both." },
    { group: "Choices the account leaves open", id: "spending_keys", label: "Rules that assign spending to the group", type: "levels", levels: ["preferred", "alternative"], affects: ["spending"], help: "The preferred rule for every category, or the alternative the account also ran. Single lines can be changed in the ledger below." },
    { group: "Choices the account leaves open", id: "fiscal_weight", label: "What a budget dollar is worth to other residents", type: "slider", affects: ["all"], help: "1 means a dollar of tax money is worth a dollar to other residents. 0 is the opposite extreme; nobody estimates it." }
  ];
  var BY_ID = {}; CONTROLS.forEach(function (k) { BY_ID[k.id] = k; });
  var PATHS = CONTROLS.map(function (c) { return c.id; }).concat(["school_response_band", "general_government_response_band", "key_override", "key_band", "response_override"]);
  var PATH_LABEL = { school_response_band: "School spending, both values", general_government_response_band: "General government, both values",
    key_override: "Allocation rules chosen for single lines", key_band: "Allocation rules with both ends in the range", response_override: "Shares typed into the ledger" };

  function get(s, p) { return p.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, s); }
  function set(s, p, v) { var ks = p.split("."), o = s; for (var i = 0; i < ks.length - 1; i++) o = o[ks[i]]; if (v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = v; }
  function fmt(x, d) { if (x == null || !isFinite(x)) return "n/a"; var r = Math.abs(x).toFixed(d == null ? 1 : d), s = r.replace(/\B(?=(\d{3})+(?!\d))/g, ","); return (x < 0 && parseFloat(r) !== 0 ? "−" : "") + s; }
  function fmtAuto(x) { return fmt(x, Math.abs(x) < 9.95 ? 1 : 0); }  // whole billions, one decimal below ten
  function signed(x, d) { return (x > 1e-9 ? "+" : "") + fmt(x, d); }
  function money(x) { return (x < 0 ? "−$" : "$") + fmt(Math.abs(x), 0); }
  var OPTION = { cbo_collective: "CBO rules: corporate tax 75% on capital income, 25% on wages", treasury_815: "Treasury: 81.5% on capital", nas_80: "National Academies: 80% on capital",
    corporate_all_capital: "All corporate tax on capital", federal_gap_high_agi: "Federal income-tax gap placed on incomes over $500,000", property_residual_consumption: "Business property tax passed on to consumers",
    public_assets_tax_base: "Public asset income split like taxes", medicare_income_weighted: "Medicare premiums weighted by income", PEARNVAL: "all earnings", WSAL_VAL: "wages and salaries only",
    below_ba: "no bachelor's degree", hs_or_less: "high school or less", cash: "survey earnings", gdp: "national GDP", personal: "each person's own", shared: "pooled in the household",
    preferred: "preferred rules", alternative: "alternative rules" };
  // Plain names for the rules that split a national line between people; hovering shows the rule id used in the CSVs.
  // Spending rules: full_account_spending_2026_09_20/builder.py:202-250. Receipt rules: full_account_receipts_2026_09_20/builder.py:80-99.
  var KEY = {
    spending: { population: "Per head", adults: "People aged 18 and over", working_age: "People aged 18 to 64", age65plus: "People aged 65 and over", age5_24: "People aged 5 to 24", age18_24: "People aged 18 to 24",
      medicaid_covered: "People covered by Medicaid", social_security: "Social Security income reported", ssi: "SSI income reported", cash_assistance: "Public assistance income reported",
      unemployment: "Unemployment pay reported", veterans: "Veterans' payments reported", workers_comp: "Workers' compensation reported", wages: "Wages and salaries",
      refundable_credits: "Earned income credit and refundable child credit", all_cash: "All cash benefits reported", snap: "SNAP benefits", energy: "Energy assistance", wic: "WIC benefits",
      housing_support: "Housing subsidy received", resources: "Household resources per member", medicare: "Expected Medicare spending, by age and US or foreign birth",
      medicaid: "Expected Medicaid spending, by age and US or foreign birth", va_medical: "Expected VA medical spending", tricare: "Expected Tricare spending",
      health_other: "Expected VA, Tricare and other public medical spending", school_operating: "School cost at measured enrollment", postsecondary: "Public college cost",
      education_mix: "Schools and public colleges together", external: "Paid abroad, none assigned",
      // Added from the two use lanes (build_model.py use_keys): the preferred rule with the group's part moved.
      use: "By use (custody, arrests, criminal courts)", use_raw_coding: "By use, ethnicity codes as recorded",
      uninsured_use_low: "Medicaid plus uninsured care, low end", uninsured_use_high: "Medicaid plus uninsured care, high end",
      uninsured_use_07_low: "Medicaid plus uninsured care at 0.7× use, low end", uninsured_use_07_high: "Medicaid plus uninsured care at 0.7× use, high end" },
    receipts: { population: "Per head", resident_population: "Per head, counting residents outside the survey", adults: "People aged 18 and over", wage: "Wages and salaries",
      wage_oasdi: "Wages up to the Social Security cap", self_payroll: "Payroll tax owed on self-employment earnings", positive_fica_worker: "Workers who pay payroll tax",
      capital: "Interest, dividends and rent reported", interest_dividend: "Interest and dividends reported", federal_liability: "Federal income tax owed before credits (Census tax model)",
      observed_liability_plus_positive_gap_high_agi: "Federal income tax owed, with the gap to the national total placed on incomes over $500,000",
      state_liability: "State income tax owed after credits (Census tax model)", consumption: "Household resources per member, standing in for consumption", medicare: "People covered by Medicare",
      medicare_income: "People covered by Medicare, weighted by income", modeled_owner_property: "Property tax modeled for owner-occupied homes", none: "Paid from abroad, none assigned" }
  };
  function keyName(side, k) { return KEY[side][k] || String(k).replace(/_/g, " "); }
  function show(v) {
    if (Array.isArray(v)) return v.map(show).join(" and ");  // a band: both values enter the range
    if (v && typeof v === "object") {  // per-line rules (their names say which line) or typed shares, keyed by line
      var ids = Object.keys(v);
      return ids.length ? ids.map(function (id) {
        return typeof v[id] === "number" ? label(id.replace(/^receipt:/, "")) + ": " + show(v[id]) : [].concat(v[id]).map(function (k) { return keyName("spending", k); }).join(" and ");
      }).join("; ") : "none";
    }
    return typeof v === "number" ? String(Math.round(v * 1000) / 1000) : v === true ? "yes" : v === false ? "no" : v == null ? "none" : OPTION[v] || String(v).replace(/_/g, " ");
  }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function same(a, b) { return JSON.stringify(a) === JSON.stringify(b); }

  /* ---------- sources: one registry, cited wherever a claim appears ---------- */
  // External sources first, then documents of this repo (kind "repo"), which open their file in the checkout.
  var SOURCES = SRC.sources.slice().sort(function (a, b) { return ((a.kind === "repo") - (b.kind === "repo")) || (a.authors + " " + a.year).localeCompare(b.authors + " " + b.year); });
  var BY_SUPPORT = {};
  SOURCES.forEach(function (s) { (s.supports || []).forEach(function (id) { (BY_SUPPORT[id] = BY_SUPPORT[id] || []).push(s); }); });
  function citation(s) { return s.authors + " (" + s.year + "). " + s.title + (s.venue ? ". " + s.venue : "") + "."; }
  function sourceHref(s) { return s.kind === "repo" ? repoHref(s.path) : s.url; }
  function citeLinks(ids) {
    var seen = {}, list = [];
    [].concat(ids).forEach(function (id) { (BY_SUPPORT[id] || []).forEach(function (s) { if (!seen[s.key]) { seen[s.key] = 1; list.push(s); } }); });
    return list.map(function (s) { return '<a href="' + esc(sourceHref(s)) + '" target="_blank" rel="noopener" title="' + esc(citation(s)) + '">' + esc(s.short) + '</a>'; }).join(", ");
  }
  function cites(ids, lead) { var links = citeLinks(ids); return links ? '<span class="cites">' + (lead || "Sources: ") + links + '</span>' : ""; }
  function repoHref(path) { return SRC.repo_prefix + "/" + path.split("/").map(encodeURIComponent).join("/"); }
  function repoLinks(text) {  // a file named in a reference opens the local copy; only paths the build found on disk are linked
    return esc(text).replace(/[A-Za-z0-9_][A-Za-z0-9_.\/-]*\.(?:md|py|csv|json|js|sql|html)\b/g, function (tok) {
      var path = SRC.paths[tok]; return path ? '<a class="path" href="' + repoHref(path) + '" target="_blank" rel="noopener">' + tok + '</a>' : tok; });
  }

  function presetState(p) {
    var s = E.defaultState(M);
    (p.settings || []).forEach(function (x) { if (x.path) set(s, x.path, JSON.parse(JSON.stringify(x.value))); });
    return s;
  }
  var CENTRAL_PRESET = PRESETS.filter(function (p) { return p.central; })[0], CENTRAL_ID = CENTRAL_PRESET.id, CENTRAL = presetState(CENTRAL_PRESET);
  // A control whose central value is a band shows both ends; moving it drops the band, going back restores it.
  var BAND_OF = { school_response: "school_response_band", general_government_response: "general_government_response_band" };
  function centralText(k) { return BAND_OF[k.id] && CENTRAL[BAND_OF[k.id]] ? CENTRAL[BAND_OF[k.id]].join("–") : show(get(CENTRAL, k.id)); }
  function restoreBand(s, id) { if (BAND_OF[id]) { if (CENTRAL[BAND_OF[id]]) s[BAND_OF[id]] = E.clone(CENTRAL[BAND_OF[id]]); else delete s[BAND_OF[id]]; } }

  function outcome(s, key) {
    var out = E.evaluate(M, s), range = E.unresolvedRange(M, s, key || lens);
    return { out: out, value: out[key || lens], range: range };
  }

  function executedStatus(s) {
    var d = E.defaultState(M), contract = ["transfer_response", "interest_response", "subsidy_response", "direct_receipt_response", "indirect_receipt_response"]
      .every(function (k) { return s[k] === d[k]; }) && !Object.keys(s.response_override).length && s.count_production;
    if (!contract) return ["own", "Your own assumptions: the account's formula, with settings the account never uses"];
    if (same(s, CENTRAL)) return ["formula", "The central case (" + CENTRAL_PRESET.kind_label + "), computed with the account's formula"];
    // Every rule in the ledger was executed, but the account ran whole sets of rules, never a mix per line.
    var mixed = Object.keys(s.key_override).length || Object.keys(s.key_band || {}).length;
    var flat = s.school_response === 1 && s.other_education_response === 1 && s.delayed_response === 1 && !s.school_response_band;
    var onLevels = [0, 0.5, 1].indexOf(s.service_response) >= 0 && [0, 1].indexOf(s.public_goods_response) >= 0 && s.general_government_response === s.public_goods_response && [0, 1].indexOf(s.fiscal_weight) >= 0;
    if (!mixed && flat && onLevels && s.service_response === s.production.capital_adjustment) return ["grid", "The account ran this exact case (one of its 497,664 rows)"];
    var ref = M.production.reference, atRef = E.PRODUCTION_DIMS.every(function (k) { return k === "normalization" || s.production[k] === ref[k]; });
    if (!mixed && atRef && s.service_response === 1 && s.public_goods_response === 0 && s.general_government_response === 0 && s.fiscal_weight === 1 && s.receipt_scenario === M.receipts.reference && s.spending_keys === "preferred")
      return ["grid", "The account ran this exact case (one of its 60 service-response cases)"];
    return ["formula", "Computed with the account's formula; the account did not run this exact combination"];
  }

  /* ---------- drawing ---------- */
  var LENS_TEXT = { welfare_bn: "The yearly effect of the group's presence on all other US residents: taxes received, benefits and services paid for, and the gain from its labor.",
    target_balance_bn: "What the group pays in minus everything the ledger assigns to it, each line at average cost. No production side.",
    normalized_gap_bn: "The group's balance measured against an equal per-head share of the national balance." };

  function drawBar() {
    var o = outcome(state), c = outcome(CENTRAL), diff = o.value - c.value;
    $("b-value").textContent = fmt(o.value, 1); $("b-value").className = o.value < 0 ? "neg" : "pos";
    $("b-range").innerHTML = "open choices span <b>" + fmtAuto(o.range[0]) + "</b> to <b>" + fmtAuto(o.range[1]) + "</b>";
    $("b-central").innerHTML = "central case <b>" + fmt(c.value, 1) + "</b>";
    $("b-diff").innerHTML = Math.abs(diff) < 0.05 ? "no difference" : "difference <b>" + signed(diff, 1) + "</b>";
    var k = BY_ID[activeControl];
    $("b-active").classList.toggle("live", !!k);  // on a phone the hint is dropped to keep the readout short
    if (!k) { $("b-active").textContent = "Move a slider or pick an option to see its central value and what it alone does to the result."; return; }
    var back = E.clone(state); set(back, k.id, JSON.parse(JSON.stringify(get(CENTRAL, k.id)))); restoreBand(back, k.id);
    var alone = o.value - E.evaluate(M, back)[lens];
    $("b-active").innerHTML = "<b>" + esc(k.label) + "</b>: " + esc(show(get(state, k.id))) + " (central " + esc(centralText(k)) + "). " +
      (same(get(state, k.id), get(CENTRAL, k.id)) ? "" : Math.abs(alone) < 0.05 ? "It does not move this result." : "On its own it moves the result by " + signed(alone, 1) + " bn.");
  }

  function drawPresets() {
    var cards = PRESETS.map(function (p) { return { p: p, v: outcome(presetState(p)) }; });
    if (!activePreset) cards.unshift({ p: { id: "", kind_label: "Live", label: "Your current settings" }, v: outcome(state), current: true });
    var lo = Math.min.apply(null, cards.map(function (c) { return Math.min(c.v.range[0], 0); })), hi = Math.max.apply(null, cards.map(function (c) { return Math.max(c.v.range[1], 0); }));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("presets").innerHTML = cards.map(function (c) {
      var v = c.v, a = x(Math.min(v.range[0], v.range[1])), b = x(Math.max(v.range[0], v.range[1]));
      var inner = '<span class="pk">' + esc(c.p.kind_label).replace(/\d{4}-\d{2}-\d{2}/g, "<span>$&</span>") + '</span><span class="pl">' + esc(c.p.label) + '</span>' +
        '<span class="pv">' + fmtAuto(v.range[0]) + (Math.abs(v.range[1] - v.range[0]) > 0.5 ? " to " + fmtAuto(v.range[1]) : "") + '</span>' +
        '<span class="track"><i class="zero" style="left:' + x(0) + '%"></i><i class="span ' + (v.value < 0 ? "neg" : "pos") + '" style="left:' + a + '%;width:' + Math.max(b - a, 0.8) + '%"></i></span>';
      return c.current ? '<div class="preset current">' + inner + '</div>'
        : '<button class="preset' + (activePreset === c.p.id ? " on" : "") + '" data-preset="' + c.p.id + '" id="preset-' + c.p.id + '">' + inner + '</button>';
    }).join("");
  }

  function drawHeadline() {
    var o = outcome(state), c = outcome(CENTRAL), st = executedStatus(state);
    var parts, exact = true;
    try { parts = E.attribute(M, CENTRAL, state, PATHS, lens); }
    catch (err) {  // too many changed controls for an exact split: fall back to one at a time
      exact = false;
      parts = PATHS.filter(function (p) { return !same(get(CENTRAL, p), get(state, p)); }).map(function (p) {
        var s = E.clone(CENTRAL); set(s, p, E.clone({ v: get(state, p) }).v); return { path: p, from: get(CENTRAL, p), to: get(state, p), effect_bn: E.evaluate(M, s)[lens] - c.value }; });
    }
    parts = parts.filter(function (p) { return Math.abs(p.effect_bn) > 0.05; }).sort(function (a, b) { return Math.abs(b.effect_bn) - Math.abs(a.effect_bn); });
    $("diff-title").textContent = parts.length ? "Why this differs from the central case" : "This is the central case";
    $("h-name").textContent = LENS_TEXT[lens] + (parts.length ? " It stands " + signed(o.value - c.value, 1) + " bn from the central case. " + (exact
      ? "Each bar is one changed assumption's share of that; the shares allow for interactions and add up exactly."
      : "Each bar is one assumption changed alone; too many differ to split their interactions.") : "");
    var max = Math.max.apply(null, parts.map(function (p) { return Math.abs(p.effect_bn); }).concat([1]));
    $("diff").innerHTML = parts.map(function (p) {
      var k = BY_ID[p.path] || { label: PATH_LABEL[p.path] || p.path.replace(/_/g, " ") };
      return '<li data-affects="' + (k.affects || []).join(" ") + '"><span class="dl">' + esc(k.label) + '<em>' + esc(show(p.from)) + " → " + esc(show(p.to)) + '</em></span>' +
        '<span class="db"><i class="' + (p.effect_bn < 0 ? "neg" : "pos") + '" style="width:' + Math.abs(p.effect_bn) / max * 100 + '%"></i></span><span class="dv">' + signed(p.effect_bn, 1) + '</span></li>';
    }).join("");
    var bands = [];  // bands these assumptions declare; the engine's range spans every combination
    if (state.school_response_band) bands.push("both school values, " + show(state.school_response_band));
    if (state.general_government_response_band) bands.push("both general-government values, " + show(state.general_government_response_band));
    Object.keys(state.key_band || {}).forEach(function (id) { bands.push("both ends of the allocation rule for " + label(id)); });
    $("h-range").textContent = "The account leaves three choices open: whether household money is shared, how the production gain is scaled, and the school share of education" +
      (bands.length ? ". These assumptions add " + bands.slice(0, -1).join("; ") + (bands.length > 1 ? "; and " : "") + bands[bands.length - 1] : "") +
      ". Across them the result runs from " + fmtAuto(o.range[0]) + " to " + fmtAuto(o.range[1]) + " bn.";
    $("h-per").textContent = lens === "welfare_bn" ? money(o.out.per_other_resident) + " a year per other resident; " + money(o.out.per_target_person) + " per member of the group."
      : money(o.value * 1e9 / M.meta.target_population) + " a year per member of the group.";
    $("h-status").textContent = st[1]; $("h-status").className = "status " + st[0];
  }

  function bridgeSteps(out, s) {
    var w = s.fiscal_weight, c = out.classes, g = function (k) { return c[k] || { assigned_bn: 0, responsive_bn: 0 }; };
    var edu = out.spending.filter(function (l) { return l.id === "education_services"; })[0], PG = "public_goods defense general_public_services";
    if (lens !== "welfare_bn") {
      var steps = [["Taxes the group pays", g("direct_receipts").assigned_bn, 0, "direct_receipts"], ["Corporate, property and asset receipts", g("incidence_receipts").assigned_bn, 0, "incidence_receipts"],
        ["Benefits paid to the group", -g("household_transfer").assigned_bn, 0, "household_transfer"], ["Education", -edu.amount_bn, 0, "education_services"],
        ["Other public services", -(g("service").assigned_bn - edu.amount_bn), 0, "service"], ["Defense and general government", -g("public_goods").assigned_bn, 0, PG],
        ["Interest and subsidies", -(g("interest").assigned_bn + g("subsidy").assigned_bn), 0, "interest subsidy"]];
      if (lens === "normalized_gap_bn") steps.push(["Less an equal per-head share of the national balance", out.normalized_gap_bn - out.target_balance_bn, 0, "all"]);
      return steps;
    }
    return [["Taxes the group pays", w * g("direct_receipts").responsive_bn, g("direct_receipts").assigned_bn - g("direct_receipts").responsive_bn, "direct_receipts"],
      ["Corporate, property and asset receipts", w * g("incidence_receipts").responsive_bn, g("incidence_receipts").assigned_bn - g("incidence_receipts").responsive_bn, "incidence_receipts"],
      ["Benefits paid to the group", -w * g("household_transfer").responsive_bn, -(g("household_transfer").assigned_bn - g("household_transfer").responsive_bn), "household_transfer"],
      ["Gain to other residents from the group's work", out.private_wtp_bn + w * out.induced_receipts_bn, 0, "production"],
      ["Education", w * edu.effect_bn, -(edu.amount_bn + edu.effect_bn), "education_services"],
      ["Other public services", -w * (g("service").responsive_bn + edu.effect_bn), -((g("service").assigned_bn - edu.amount_bn) - (g("service").responsive_bn + edu.effect_bn)), "service"],
      ["Defense and general government", -w * g("public_goods").responsive_bn, -(g("public_goods").assigned_bn - g("public_goods").responsive_bn), PG],
      ["Interest and subsidies", -w * (g("interest").responsive_bn + g("subsidy").responsive_bn), -((g("interest").assigned_bn + g("subsidy").assigned_bn) - (g("interest").responsive_bn + g("subsidy").responsive_bn)), "interest subsidy"]];
  }

  function drawBridge() {
    var out = E.evaluate(M, state), steps = bridgeSteps(out, state), cSteps = bridgeSteps(E.evaluate(M, CENTRAL), CENTRAL);
    var run = 0, lo = 0, hi = 0;
    steps.forEach(function (s) { var ghost = run + s[1] + s[2]; run += s[1]; lo = Math.min(lo, run, ghost); hi = Math.max(hi, run, ghost); });
    var W = 830, rowH = 30, left = 340, right = 150, H = (steps.length + 1) * rowH + 26, x = function (v) { return left + (v - lo) / (hi - lo || 1) * (W - left - right); };
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Bridge from taxes paid to the result"><line class="axis" x1="' + x(0) + '" x2="' + x(0) + '" y1="4" y2="' + (H - 20) + '"/>';
    run = 0;
    steps.forEach(function (s, i) {
      var y = 8 + i * rowH, a = run, b = run + s[1], ghostEnd = b + s[2]; run = b;
      var delta = s[1] - cSteps[i][1];
      svg += '<g class="step" data-affects="' + s[3] + '"><title>' + esc(s[0]) + ": " + signed(s[1], 1) + " bn counted" + (Math.abs(s[2]) > 0.05 ? "; " + fmt(Math.abs(s[2]), 1) + " bn assigned to the group but left out" : "") + '</title>' +
        '<text class="lab" x="' + (left - 12) + '" y="' + (y + 17) + '" text-anchor="end">' + esc(s[0]) + '</text>';
      if (Math.abs(s[2]) > 0.05) svg += '<rect class="ghost" x="' + Math.min(x(b), x(ghostEnd)) + '" y="' + (y + 6) + '" width="' + Math.abs(x(ghostEnd) - x(b)) + '" height="12"/>';
      svg += '<rect class="' + (s[1] < 0 ? "neg" : "pos") + '" x="' + Math.min(x(a), x(b)) + '" y="' + (y + 6) + '" width="' + Math.max(Math.abs(x(b) - x(a)), 1) + '" height="12"/>' +
        '<text class="val" x="' + (Math.max(x(a), x(b), x(ghostEnd)) + 6) + '" y="' + (y + 17) + '">' + signed(s[1], 1) + (Math.abs(delta) > 0.05 ? ' <tspan class="dlt">(' + signed(delta, 1) + " against central)</tspan>" : "") + '</text>' +
        '<line class="link" x1="' + x(b) + '" x2="' + x(b) + '" y1="' + (y + 18) + '" y2="' + (y + rowH + 6) + '"/></g>';
    });
    var yEnd = 8 + steps.length * rowH;  // one rule above the total, as under a column of figures
    svg += '<line class="sum" x1="' + (left - 120) + '" x2="' + (W - right + 60) + '" y1="' + (yEnd + 1) + '" y2="' + (yEnd + 1) + '"/>' +
      '<text class="lab tot" x="' + (left - 12) + '" y="' + (yEnd + 19) + '" text-anchor="end">Result</text><rect class="' + (run < 0 ? "neg" : "pos") + ' total" x="' + Math.min(x(0), x(run)) + '" y="' + (yEnd + 8) + '" width="' + Math.max(Math.abs(x(run) - x(0)), 1) + '" height="12"/>' +
      '<text class="val tot" x="' + (Math.max(x(0), x(run)) + 6) + '" y="' + (yEnd + 19) + '">' + fmt(run, 1) + ' bn</text></svg>';
    $("bridge").innerHTML = svg;
  }

  function drawTornado() {
    var base = E.evaluate(M, state)[lens];
    var rows = CONTROLS.map(function (k) {
      var ends = k.type === "slider" ? [k.min == null ? 0 : k.min, k.max == null ? 1 : k.max] : k.levels;
      var vals = ends.map(function (v) { var s = E.clone(state); set(s, k.id, v); if (BAND_OF[k.id]) delete s[BAND_OF[k.id]]; return { v: v, y: E.evaluate(M, s)[lens] }; });
      vals.sort(function (a, b) { return a.y - b.y; });
      return { k: k, lo: vals[0], hi: vals[vals.length - 1], swing: vals[vals.length - 1].y - vals[0].y };
    }).filter(function (r) { return r.swing > 0.05; }).sort(function (a, b) { return b.swing - a.swing; });
    var lo = Math.min.apply(null, rows.map(function (r) { return r.lo.y; }).concat([base])), hi = Math.max.apply(null, rows.map(function (r) { return r.hi.y; }).concat([base]));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("tornado").innerHTML = rows.map(function (r) {
      return '<li data-affects="' + r.k.affects.join(" ") + '" data-control="' + r.k.id + '"><span class="tl">' + esc(r.k.label) + '</span><span class="tb"><i class="bar" style="left:' + x(r.lo.y) + '%;width:' + (x(r.hi.y) - x(r.lo.y)) + '%"></i><i class="now" style="left:' + x(base) + '%"></i></span>' +
        '<span class="tv">' + fmtAuto(r.lo.y) + " at " + esc(show(r.lo.v)) + ", " + fmtAuto(r.hi.y) + " at " + esc(show(r.hi.v)) + "</span></li>";
    }).join("") || "<li>No assumption moves this result.</li>";
    $("tornado-note").textContent = "Each bar shows the result across one assumption's full range, with everything else held where it is now. The tick marks the current result, " + fmt(base, 1) + " bn.";
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
          input = '<span class="seg" role="radiogroup" aria-label="' + esc(k.label) + '">' + k.levels.map(function (l) {
            return '<label class="opt"><input type="radio" name="c-' + k.id + '" data-path="' + k.id + "\" data-value='" + JSON.stringify(l) + "'" + (same(l, v) ? " checked" : "") + '><span>' + esc(show(l)) + (same(l, c) ? " <i>(central)</i>" : "") + '</span></label>'; }).join("") + '</span>';
        }
        return '<div class="ctl' + (differs ? " differs" : "") + '" data-control="' + k.id + '" data-affects="' + k.affects.join(" ") + '"><label class="name" for="c-' + k.id + '"><span>' + esc(k.label) + '</span>' +
          (differs ? '<button type="button" class="reset" data-reset="' + k.id + '" title="Back to the central value">back to ' + esc(centralText(k)) + '</button>' : '<span class="cval">central ' + esc(centralText(k)) + '</span>') + '</label>' + input +
          (k.help ? '<p class="help">' + esc(k.help) + '</p>' : "") + (cites("control:" + k.id) || '<span class="cites">No outside source: the account sets this itself.</span>') + '</div>';
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
          var keyCell = side === "spending" && l.keys.length > 1 ? '<select data-key="' + l.id + '" id="k-' + l.id + '" aria-label="Allocation rule for ' + esc(label(l.id)) + '">' + l.keys.map(function (k) { return '<option value="' + esc(k) + '" title="rule id: ' + esc(k) + '"' + (k === l.key ? " selected" : "") + '>' + esc(keyName(side, k)) + '</option>'; }).join("") + '</select>' : '<span title="rule id: ' + esc(l.key) + '">' + esc(keyName(side, l.key)) + '</span>';
          var band = side === "spending" && (state.key_band || {})[l.id];
          if (band) keyCell += '<small title="' + esc(band.map(function (k) { return keyName(side, k); }).join(" and ")) + '">Both ends of this rule enter the range.</small>';
          return '<tr data-affects="' + l.id + " " + g + '"><td>' + esc(label(l.id)) + findButton(l.id) + '</td><td class="key">' + keyCell + '</td><td class="num">' + (l.share * 100).toFixed(1) + '%</td><td class="num">' + fmt(l.amount_bn, 1) + '</td>' +
            '<td class="num">' + fmt(Math.abs(l.effect_bn), 1) + '</td><td class="resp"><div><input type="number" min="0" max="1" step="0.05" id="r-' + oid + '" data-resp="' + oid + '" aria-label="Share counted for ' + esc(label(l.id)) + '" value="' + (Math.round(l.response * 1000) / 1000) + '"' + (overridden ? ' class="ov"' : "") + '><span class="mini"><i style="width:' + Math.abs(l.amount_bn) / max * 100 + '%"></i><b style="width:' + Math.abs(l.effect_bn) / max * 100 + '%"></b></span></div></td></tr>';
        }).join("") + '</tbody>';
      }).join("");
    }
    var head = '<thead><tr><th>Line</th><th>Assigned by</th><th class="num">Group share</th><th class="num">Assigned, bn</th><th class="num">Counted, bn</th><th>Share counted (0 to 1)</th></tr></thead>';
    $("ledger-receipts").innerHTML = head + table(out.receipts, "receipts");
    $("ledger-spending").innerHTML = head + table(out.spending, "spending");
  }

  var BASIS = { stated: "stated in the account", implied: "implied by the evidence", not_addressed: "left out by this convention" };
  function drawPresetNote() {
    var p = PRESETS.filter(function (q) { return q.id === activePreset; })[0];
    if (!p) { $("preset-note").hidden = true; return; }
    $("preset-note").hidden = false;
    $("preset-note").innerHTML = '<h3>' + esc(p.label) + '</h3><p>' + repoLinks(p.summary) + '</p>' + (p.scope_note ? '<p class="scope">' + repoLinks(p.scope_note) + '</p>' : "") +
      '<div class="scroll"><table class="basis"><thead><tr><th>Assumption</th><th>Where it comes from</th><th>Why</th></tr></thead><tbody>' + (p.settings || []).map(function (s) {
        var value = /^key_(override|band)\./.test(s.path || "") ? [].concat(s.value).map(function (k) { return keyName("spending", k); }).join(" and ") : show(s.value);
        return '<tr><td>' + esc(s.label || s.path) + (s.path ? ": " + esc(value) : "") + '</td><td><span class="tag ' + esc(s.basis) + '">' + esc(BASIS[s.basis] || s.basis) + '</span></td><td>' + esc(s.note) + (s.ref ? ' <span class="path">' + repoLinks(s.ref) + '</span>' : "") + '</td></tr>'; }).join("") + '</tbody></table></div>' +
      (p.misses && p.misses.length ? '<h4>Left out of this set of assumptions</h4><ul>' + p.misses.map(function (m) { return '<li>' + repoLinks(m) + '</li>'; }).join("") + '</ul>' : "") + cites("preset:" + p.id);
  }

  function drawStanding() {
    $("standing-title").textContent = P.standing.title;
    $("standing").innerHTML = '<tbody>' + P.standing.rows.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>'; }).join("") + '</tbody>';
    $("standing-text").textContent = P.standing.text;
    $("standing-cites").innerHTML = citeLinks("standing") ? "Sources: " + citeLinks("standing") : "";
  }

  function drawAuthors() {
    $("authors").innerHTML = P.authors.map(function (a) {
      var target = PRESETS.filter(function (p) { return p.id === a.closest.preset; })[0];
      return '<article><h3>' + esc(a.name) + '</h3>' + a.argues.map(function (x, i) {
        return '<p class="q">' + esc(x[0]) + cites("argue:" + a.id + ":" + i, "Original: ") + '<span class="cites">This repo\'s audit: ' + repoLinks(x[1]) + '</span></p>'; }).join("") +
        '<p><b>What the claim is about:</b> ' + esc(a.object) + '</p><p><b>Closest convention in this ledger:</b> ' +
        (target ? '<button type="button" class="link" data-preset="' + target.id + '">' + esc(target.label) + '</button>. ' : '<span class="tag not_addressed">none</span> ') + esc(a.closest.why) + '</p>' +
        '<h4>The argument leaves out</h4><ul>' + a.leaves_out.map(function (m) { return '<li>' + esc(m) + '</li>'; }).join("") + '</ul>' + cites("author:" + a.id, "Also cited: ") + '</article>';
    }).join("");
  }

  function drawContext() {
    var tagText = { inside_headline: "already inside the result", overlaps_headline: "overlaps the result: do not add", outside_not_addable: "outside the account: do not add", different_object: "measures something else: compare, do not add", adds_to_headline: "left out of the result: add it" };
    $("context").innerHTML = CONTEXT.map(function (c) {
      return '<article><header><span class="tag ' + esc(c.relation_to_headline) + '">' + esc(tagText[c.relation_to_headline] || c.relation_to_headline) + '</span>' + (c.faq_entry ? '<span class="faq">FAQ ' + esc(c.faq_entry) + '</span>' : "") + '</header>' +
        (c.objection ? '<p class="obj">' + esc(c.objection) + '</p>' : "") + '<p>' + esc(c.finding) + '</p><ul>' + (c.values || []).map(function (v) {
          var file = String(v.file_line || "").replace(/:\d+(?:[-,]\d+)*$/, ""), path = SRC.paths[file];
          return '<li><b>' + esc(typeof v.value === "number" ? fmt(v.value, Math.abs(v.value) < 10 ? 2 : 0) : v.value) + '</b> ' + esc(v.unit || "") + ' <span>' + esc(v.label) + '</span>' +
            (path ? ' <a class="path" href="' + repoHref(path) + '" target="_blank" rel="noopener" title="' + esc(v.file_line) + '">data</a>' : "") + '</li>'; }).join("") + '</ul>' +
        (c.combining_rule ? '<p class="rule">' + esc(c.combining_rule) + '</p>' : "") + '<footer><span class="path">' + repoLinks(c.memo || "") + '</span>' + cites("card:" + c.id) + '</footer></article>';
    }).join("") || "<p>No objections were included when this page was built.</p>";
  }

  function ladderBody(c) {
    return (c.parts || [{ t: c.text }]).map(function (p) {
      if (p.u) return '<a href="' + esc(p.u) + '" target="_blank" rel="noopener">' + esc(p.t) + '</a>';
      if (p.r) return '<a href="' + repoHref(p.r) + '" target="_blank" rel="noopener">' + esc(p.t) + '</a>';
      return esc(p.t);
    }).join("");
  }

  function drawLadder() {
    var q = ladder.q.trim().toLowerCase(), chosen = Object.keys(ladder.topics).filter(function (t) { return ladder.topics[t]; });
    var cards = LAD.cards.filter(function (c) {
      return ladderVisible(c) && (!q || c.text.toLowerCase().indexOf(q) >= 0 || String(c.n) === q) && (!chosen.length || chosen.some(function (t) { return c.topics.indexOf(t) >= 0; })) && (!ladder.token || c.affects.indexOf(ladder.token) >= 0);
    });
    var counts = { current: 0, qualified: 0, historical: 0 }; LAD.cards.forEach(function (c) { counts[c.status] += 1; });
    $("ladder-note").innerHTML = "The repo's confidence ladder (" + repoLinks(LAD.source) + "), read when this page was built: " + LAD.cards.length + " entries in its own words, with its own links. " + counts.current + " are current, " + counts.qualified +
      " are qualified by a later correction and " + counts.historical + " are historical (the dated earlier layers). Status, topics and ledger links are assigned by keyword rules, so treat them as a way to find entries. Showing " + cards.length + ".";
    $("ladder-topics").innerHTML = (ladder.token ? '<button type="button" class="link" data-find="">Linked to ' + esc(label(ladder.token)) + ': show all</button>' : "") +
      LAD.topics.map(function (t) { return '<label><input type="checkbox" data-topic="' + esc(t) + '"' + (ladder.topics[t] ? " checked" : "") + '>' + esc(t) + '</label>'; }).join("");
    $("ladder").innerHTML = cards.map(function (c) {
      var short = c.text.length > 230 ? c.text.slice(0, 230).replace(/\s+\S*$/, "") + " …" : c.text;
      return '<details class="' + c.status + '" data-affects="' + c.affects.join(" ") + '"><summary><span class="n">' + c.n + '</span><span>' + esc(short) + '</span></summary><p class="body">' + ladderBody(c) + '</p>' +
        (c.note ? '<p class="rule">' + esc(c.note) + '</p>' : "") + '<div class="meta"><span class="tag ' + c.status + '">' + c.status + '</span>' + c.topics.map(function (t) { return '<span class="tag">' + esc(t) + '</span>'; }).join("") +
        '<span class="path">' + repoLinks(LAD.source) + ", line " + c.line + '</span></div></details>';
    }).join("") || "<p>No entry matches.</p>";
  }

  function placeName(id) {
    var parts = id.split(":"), kind = parts[0], rest = parts.slice(1).join(":"), hit;
    if (kind === "control") return BY_ID[rest] ? "assumption: " + BY_ID[rest].label : id;
    if (kind === "card") { hit = CONTEXT.filter(function (c) { return c.id === rest; })[0]; return hit ? "objection card" + (hit.faq_entry ? " (FAQ " + hit.faq_entry + ")" : "") : id; }
    if (kind === "preset") { hit = PRESETS.filter(function (p) { return p.id === rest; })[0]; return hit ? "convention: " + hit.label : id; }
    if (kind === "argue" || kind === "author") { hit = P.authors.filter(function (a) { return a.id === parts[1]; })[0]; return hit ? hit.name : id; }
    return { ledger: "the ledger", production: "the production side", standing: "whose ledger this is" }[id] || id;
  }

  function drawSources() {
    var checked = SOURCES.filter(function (s) { return s.checked && s.checked.ok; }).length, own = SOURCES.filter(function (s) { return s.kind === "repo"; }).length;
    $("sources-note").textContent = (SOURCES.length - own) + " external sources and " + own + " documents of this repo. Each link comes from a citation already in this repo, or was resolved from one and is marked as such. A script fetched every external link once; " + checked +
      " answered, and the rest are marked. A short label elsewhere on the page opens its source directly.";
    $("sources").innerHTML = SOURCES.map(function (s) {
      var places = {}; (s.supports || []).forEach(function (id) { places[placeName(id)] = 1; });
      var host = s.kind === "repo" ? s.path : s.url.replace(/^https?:\/\/(www\.)?/, "").split("/")[0];
      var status = s.kind === "repo" ? "A document of this repo; the build checks that the file exists." : !s.checked ? "" : s.checked.ok ? "Link answered on " + s.checked.date + "." : "Link did not answer the script on " + s.checked.date + " (" + esc(s.checked.status) + "); open it by hand.";
      return '<li id="src-' + esc(s.key) + '">' + esc(s.authors) + " (" + esc(s.year) + "). <i>" + esc(s.title) + "</i>" + (s.venue ? ". " + esc(s.venue) : "") + '. <a href="' + esc(sourceHref(s)) + '" target="_blank" rel="noopener">' + esc(host) + '</a>' +
        '<span class="used">' + (s.repo_ref ? "Cited in this repo at " + repoLinks(s.repo_ref) + ". " : "") + (s.resolved ? "Link resolved on " + esc(s.resolved) + " from the repo's citation. " : "") + status + " Used for " + esc(Object.keys(places).join("; ")) + ".</span></li>";
    }).join("");
  }

  function renderLive() { drawBar(); drawPresets(); drawHeadline(); drawBridge(); drawTornado(); drawLedger(); }
  function render() { renderLive(); drawControls(); drawPresetNote(); }
  function commit(mutator, keepPreset) { history.push(JSON.stringify({ s: state, p: activePreset })); if (history.length > 50) history.shift(); mutator(); if (!keepPreset) activePreset = null; render(); }

  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-preset],[data-value],[data-reset],[data-lens],[data-find],[data-topic],#undo,#reset-all"); if (!t) return;
    if (t.dataset.preset) { commit(function () { var p = PRESETS.filter(function (q) { return q.id === t.dataset.preset; })[0]; state = presetState(p); activePreset = p.id; activeControl = null; }, true); if (t.classList.contains("link")) window.scrollTo({ top: 0, behavior: SMOOTH }); }
    else if (t.dataset.value) { activeControl = t.dataset.path; commit(function () { set(state, t.dataset.path, JSON.parse(t.dataset.value)); }); }
    else if (t.dataset.reset) { activeControl = t.dataset.reset; commit(function () { set(state, t.dataset.reset, JSON.parse(JSON.stringify(get(CENTRAL, t.dataset.reset)))); restoreBand(state, t.dataset.reset); }); }
    else if (t.dataset.lens) { lens = t.dataset.lens; Array.prototype.forEach.call(document.querySelectorAll("[data-lens]"), function (b) { b.classList.toggle("on", b === t); }); render(); }
    else if (t.dataset.find !== undefined) { ladder.token = t.dataset.find || null; drawLadder(); if (ladder.token) $("ladder-section").scrollIntoView({ behavior: SMOOTH }); }
    else if (t.dataset.topic) { ladder.topics[t.dataset.topic] = !ladder.topics[t.dataset.topic]; drawLadder(); }
    else if (t.id === "undo" && history.length) { var h = JSON.parse(history.pop()); state = h.s; activePreset = h.p; render(); }
    else if (t.id === "reset-all") commit(function () { state = E.clone(CENTRAL); activePreset = CENTRAL_ID; activeControl = null; }, true);
  });
  document.addEventListener("input", function (e) {
    var t = e.target;
    if (t.type === "range" && t.dataset.path) {
      set(state, t.dataset.path, parseFloat(t.value)); if (BAND_OF[t.dataset.path]) delete state[BAND_OF[t.dataset.path]];
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
    else if (t.dataset.key) commit(function () { state.key_override[t.dataset.key] = t.value; if (state.key_band) delete state.key_band[t.dataset.key]; });
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

  // The rail and in-page jumps sit below the readout, whatever height it wraps to.
  function syncBar() { document.documentElement.style.setProperty("--bar-h", $("bar").offsetHeight + "px"); }
  if (window.ResizeObserver) new ResizeObserver(syncBar).observe($("bar"));
  syncBar();

  state = E.clone(CENTRAL); activePreset = CENTRAL_ID;
  $("scope").textContent = "Mexican-origin residents of the United States, every generation, age and level of schooling: " + (M.meta.target_population / 1e6).toFixed(1) + " million people, income year 2024, in billions of 2024 dollars. The account compares the country as it is with the same country without this group, holding everything else at 2024 levels. It does not estimate what admitting or removing anyone would do.";
  $("ledger-cites").innerHTML = citeLinks("ledger") ? "Sources: " + citeLinks("ledger") : "";
  $("bridge-cites").innerHTML = citeLinks(["production", "ledger"]) ? "Sources: " + citeLinks(["production", "ledger"]) : "";
  Array.prototype.forEach.call(document.querySelectorAll("a[data-repo]"), function (a) { var path = SRC.paths[a.dataset.repo]; if (path) { a.href = repoHref(path); a.target = "_blank"; a.rel = "noopener"; } });
  drawStanding(); drawAuthors(); drawContext(); drawLadder(); drawSources(); render();
})();
