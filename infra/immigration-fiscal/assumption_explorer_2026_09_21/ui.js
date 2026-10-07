/* Page logic. All numbers come from the main case's evaluation (case.js, on engine.js); this file only draws. */
(function () {
  "use strict";
  var M = window.MODEL, P = window.PRESETS, PRESETS = P.presets, CONTEXT = window.CONTEXT.items || [], EV = window.EVIDENCE, LAD = window.LADDER, SRC = window.SOURCES;
  var E = window.Engine, $ = function (id) { return document.getElementById(id); };
  // The adopted main case (main_case_2026_10_07): its two payloads, the case and the cash set, applied once before
  // anything is evaluated. Its meta.responses and meta.capital_return carry the case's responses and capital rules.
  var C = window.Case.create(M, window.CASE_PAYLOADS), R = C.responses, K = C.capital_meta, CORR = C.syn, ADOPTED = C.meta.adopted;
  var PAYLOAD_LINES = {};
  window.CASE_PAYLOADS.accrual.lines.forEach(function (l) { PAYLOAD_LINES[l.id] = l; });
  var state, lens = "welfare_bn", activePreset = null, activeControl = null, history = [];
  var ladder = { q: "", topics: {}, all: false, token: null };
  var SMOOTH = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth";

  // Every line has a plain name here; build_ui.py refuses a payload line without one (the payload's labels are the builders').
  var LABEL = {
    federal_income_tax: "Federal income tax", employer_oasdi: "Social Security tax, employer half",
    employee_oasdi: "Social Security tax, employee half", general_sales_tax: "General sales tax",
    excise_selective_sales: "Excise and selective sales taxes", state_local_income_tax: "State and local income tax",
    modeled_owner_property: "Property tax, owner-occupied (modeled)", government_asset_income: "Government asset income",
    employee_hi: "Medicare tax, employee half", corporate_capital: "Corporate tax borne by capital",
    employer_hi: "Medicare tax, employer half", corporate_labor: "Corporate tax borne by labor",
    personal_current_transfers: "Fees, fines and personal transfers", remaining_production_property: "Property tax, business",
    other_domestic_social_contributions: "Other social contributions", self_employment_oasdi_hi: "Self-employment payroll tax",
    medicare_supplementary_premiums: "Medicare premiums", customs_duties: "Customs duties",
    other_production_taxes: "Other production taxes", business_current_transfers: "Business transfers to government",
    personal_motor_vehicle: "Motor vehicle licenses", other_personal_tax: "Other personal taxes",
    personal_property_tax: "Personal property tax", enterprise_surplus: "Government enterprises' surplus (a loss)",
    housing_enterprise_surplus: "Public housing's operating loss", tenant_occupied_property: "Property tax on rented homes",
    user_fees_key_k12: "User fees, school key (no amount)", user_fees_key_college: "User fees, college key (no amount)", user_fees_key_health: "User fees, health key (no amount)",
    education_services: "Education (schools and colleges)", domestic_interest: "Interest on existing debt",
    medicaid_and_chip_other_medical: "Medicaid, CHIP and other medical", defense: "National defense",
    public_order_safety: "Police, courts, prisons, fire (federal agencies included)", general_public_services: "General government (tax collection, administration, legislatures)",
    economic_affairs_services: "Roads, transport, economic affairs", income_security_services: "Welfare administration and services",
    health_services: "Public health services", refundable_tax_credits: "Refundable tax credits (EITC, CTC)",
    snap: "SNAP", ssi: "SSI", recreation_culture: "Parks, recreation, culture", housing_community_services: "Housing and community services",
    housing_subsidies: "Rental assistance (housing subsidies)",
    social_security: "Social Security", veterans_pension_disability: "Veterans' pensions and disability", rest_world_tax_contributions: "Taxes and contributions from abroad",
    rest_world_current_transfers: "Transfers from abroad", source_rounding: "Rounding in the source tables",
    school_reprice: "Schools, priced where the group enrolls", college_rekey: "Colleges and other education, keyed by use",
    lane_constants: "Care work, shelter and audit items, counted in full",
    roads_vmt_sl: "State and local highways, by vehicle miles and freight", roads_vmt_fed: "Federal highways, by vehicle miles and freight",
    state_price_public_order_safety: "Police, courts, prisons: state price levels", state_price_health_services: "Public health: state price levels",
    state_price_recreation_culture: "Parks and recreation: state price levels"
  };
  function label(id) { return LABEL[id] || id.replace(/_/g, " ").replace(/^./, function (c) { return c.toUpperCase(); }); }
  var CLASS_LABEL = { direct_receipts: "Taxes the group pays", incidence_receipts: "Corporate, property and asset receipts",
    household_transfer: "Cash and in-kind benefits", service: "Public services", public_goods: "Defense and general government",
    interest: "Interest on existing debt", subsidy: "Business and housing subsidies", foreign: "Foreign flows", rounding: "Rounding",
    case_lines: "Lines of the case's own: parts of the lines above, re-priced or re-keyed" };

  function elasticity(name) { var r = EV.elasticities.filter(function (x) { return x.scope === "50 states" && x.function.indexOf(name) === 0; })[0]; return r ? r.elasticity : null; }
  function pair(r) { return r.low.toFixed(2) === r.high.toFixed(2) ? r.low.toFixed(2) : r.low.toFixed(2) + "–" + r.high.toFixed(2); }
  function pct(x) { return Math.round(x * 100) + "%"; }
  // CBO's year-to-year school rates, as the account's executed profiles carry them.
  var CBO_SCHOOL = M.service.profiles.filter(function (p) { return p.profile === "cbo_category_lag_non_school_full"; })
    .map(function (p) { return p.school_response; }).filter(function (x, i, xs) { return xs.indexOf(x) === i; }).sort();
  var gps = EV.general_public_service_2024_bn;
  var GG_HELP = Math.round(EV.state_local_share * 100) + "% of general government outside interest is state and local. Across the 50 states, administration spending rises " +
    (elasticity("Governmental administration") * 10).toFixed(1) + "% for every 10% more residents (police " + (elasticity("Police") * 10).toFixed(1) + "%, schools " + (elasticity("Elementary") * 10).toFixed(1) + "%). Federal tax collection costs $" + gps.federal_tax_financial.toFixed(1) +
    "bn; the federal executive and legislature $" + gps.federal_executive_legislative.toFixed(1) + "bn. Together that implies a marginal rate between " + EV.composite_low + " and " + EV.composite_high + ". The group is " +
    (R.general_government.s * 100).toFixed(1) + "% of residents, and when cost is a power of population, removing a share that large saves more than the marginal rate: " +
    [R.general_government.low, R.general_government.high].map(function (x) { return x.toFixed(3); }).join(" and ") +
    " of average cost, at the low and high readings. Grey ticks mark the marginal rates, dark ticks the responses. Federal police, courts and prisons, the FBI among them, are charged under police, courts, prisons.";
  var RATE = function (name) { return Math.round(K.rates[name] * 100) + "%"; };

  var levels = function (d) { return M.production.dims[d]; };
  var CONTROLS = [
    { group: "What counts as a cost", id: "benefits", label: "Social Security and Medicare Part A are counted", type: "levels", levels: ["accrual", "cash"],
      names: { accrual: "as the group earns them", cash: "when paid" }, affects: ["social_security", "medicare"],
      help: "As earned: the promises the group's payroll taxes buy, at the benefits current law can pay, on the 2026 Trustees Reports and current law's separate OASI and DI funds. When paid: the benefits its retirees draw this year, as a cash budget counts them (the cash set)." },
    { group: "What counts as a cost", id: "service_response", label: "Public services grow with the population", type: "slider", marks: [0, 0.5, 1],
      help: "How much of schools, police, health and other services would not be needed if the group were absent. 1 charges each service at the response the main case gives it, most of them average cost; 0 treats services as free to add people to. The return on the capital they use scales with them.", affects: ["service", "capital"] },
    { group: "What counts as a cost", id: "school_response", label: "School spending grows with enrollment", type: "slider", marks: CBO_SCHOOL, adopted: [R.school.growth],
      help: "The main case charges the full average cost per pupil: a school system sized for the group's pupils. Across districts and across states school spending scales about one for one with enrollment. The grey ticks are CBO's year-to-year rates, " + CBO_SCHOOL.join(" when enrollment grows and ") +
        " when it falls, from its panel of states: what a budget sheds in the first year. Applies to the school part of education, and its capital, only.", affects: ["education_services", "capital"] },
    { group: "What counts as a cost", id: "school_share", label: "School share of education spending", type: "slider", min: E.schoolShareBounds(M)[0], max: E.schoolShareBounds(M)[1],
      help: "Nationally between 71.5% and 86.5%, depending on how college spending is counted. The account assumes the group's mix matches the nation's.", affects: ["education_services"] },
    { group: "What counts as a cost", id: "other_education_response", label: "College and other education spending grows with enrollment", type: "slider", affects: ["education_services", "capital"],
      help: "No estimate exists. The main case charges 1; at 0 college budgets are held fixed too, the case's other benchmark." },
    { group: "What counts as a cost", id: "long_run", label: "Roads, transport and parks grow with the population", type: "levels", levels: ["case", 0, 1],
      names: { case: "at their long-run response", 0: "held fixed", 1: "at average cost" }, affects: ["economic_affairs_services", "recreation_culture", "case_lines", "capital"],
      help: "Long run: how spending on each road, transport and park function scales with population across the states, read over a removal of the group's size: " + pair(R.economic_affairs_services) +
        " for roads and economic affairs and " + pair(R.recreation_culture) + " for parks, at the low and high readings. Held fixed is a first-year budget. The capital of roads and parks follows the choice." },
    { group: "What counts as a cost", id: "general_government_response", label: "General government grows with the population", type: "slider", marks: [EV.composite_low, EV.composite_high],
      adopted: [R.general_government.low, R.general_government.high], affects: ["general_public_services", "capital"], help: GG_HELP },
    { group: "What counts as a cost", id: "public_goods_response", label: "Defense grows with the population", type: "slider", affects: ["defense"],
      help: "Held at zero: defense spending follows other countries and operations. Intelligence agencies are funded largely through the defense budget. 1 charges a full per-head share." },
    { group: "What counts as a cost", id: "interest_response", label: "Interest on existing debt grows with the population", type: "slider", affects: ["interest"],
      help: "Debt already issued does not shrink when fewer people live here. Zero in the main case." },
    { group: "What counts as a cost", id: "transfer_response", label: "Benefits paid to the group count as a cost", type: "slider", affects: ["household_transfer", "housing_subsidies"],
      help: "Medicaid, Social Security, Medicare, tax credits and rental assistance. 1 in the main case." },
    { group: "What counts as a cost", id: "capital", label: "Return on the public capital the group uses", type: "levels", levels: ["case", 0, "private"],
      names: { case: "at " + RATE("low") + " and " + RATE("high") + ", what public borrowing costs", 0: "no return", private: "at " + RATE("reported") + ", the return to private capital" }, affects: ["capital"],
      help: "Budgets charge depreciation on schools, roads and utilities but no return on the money tied up in them. The main case charges a real return of " + RATE("low") + " at the low reading and " + RATE("high") +
        " at the high one, what public borrowing costs. " + RATE("reported") + " prices the capital displaced from private use, a social cost rather than a budget cost. It is an imputed resource cost, never a debt flow." },
    { group: "What counts as a cost", id: "enterprises", label: "Government enterprises", type: "levels", levels: K.enterprise_option.allowed_by_file,
      names: { D: "every one responds", A: "held out" }, affects: ["incidence_receipts", "capital"],
      help: "Transit, public housing, water, sewers, power, airports, ports and tolls run at a loss. If they respond, the group is charged its share of the loss and of the return on their capital; held out, both leave the account." },
    { group: "What counts as revenue", id: "direct_receipt_response", label: "Taxes the group pays count as revenue", type: "slider", affects: ["direct_receipts"],
      help: "Income, payroll, sales and excise taxes. 1 in the main case." },
    { group: "What counts as revenue", id: "indirect_receipt_response", label: "Corporate and business taxes assigned to the group count as revenue", type: "slider", affects: ["incidence_receipts"],
      help: "Nobody in the group writes these checks; a rule assigns them a share. 0, because the production side already counts the same income. The main case counts the property taxes on the group's homes at their long-run response, " +
        pct(R.modeled_owner_property.low) + " for owner-occupied and " + pct(R.tenant_occupied_property.low) + " for rented homes, and the personal property tax in full; a share typed in the ledger changes one." },
    { group: "What counts as revenue", id: "receipt_scenario", label: "Who is assumed to bear each tax", type: "levels", levels: M.receipts.scenarios, affects: ["direct_receipts", "incidence_receipts"],
      help: "Rule sets the account ran, each changing one rule from CBO's. Only CBO's, the Treasury's and the National Academies' rest on a published source; the others are stress tests the account declares itself." },
    { group: "Production side", id: "count_production", label: "Count what the group's work adds to other residents' incomes", type: "levels", levels: [true, false], affects: ["production"],
      help: "The gain to everyone else from the group's labor, plus the extra tax that gain generates, from a standard production model. A tally of taxes and spending leaves it out." },
    { group: "Production side", id: "production.sigma", label: "How easily workers of different skill replace each other", type: "levels", levels: levels("sigma"), affects: ["production"], help: "Economists call this the elasticity of substitution. Higher means closer substitutes and a smaller gain. The three values follow the range in Colas and Sachs." },
    { group: "Production side", id: "production.capital_adjustment", label: "Investment has caught up with the larger workforce", type: "levels", levels: levels("capital_adjustment"), affects: ["production"],
      help: "0 is the short run, with capital fixed and a large gain to its owners; 1 is the long run." },
    { group: "Production side", id: "production.labor_share", label: "Labor's share of income", type: "levels", levels: levels("labor_share"), affects: ["production"], help: "The share of national income paid to workers, the rest going to owners of capital. The account cites no source for these three values." },
    { group: "Production side", id: "production.labor_supply_elasticity", label: "How much other residents' hours respond to wages", type: "levels", levels: levels("labor_supply_elasticity"), affects: ["production"], help: "0 means hours do not change when wages move. The account cites no source for these two values." },
    { group: "Production side", id: "production.capital_tax_retention", label: "Share of the capital-tax gain government keeps", type: "levels", levels: levels("capital_tax_retention"), affects: ["production"], help: "The group's work raises returns to capital, and some of that comes back as tax. Nobody has estimated how much stays with government, so the account runs 0, 0.5 and 1." },
    { group: "Production side", id: "production.excluded_capital_owner_share", label: "Capital owned by people outside the count", type: "levels", levels: levels("excluded_capital_owner_share"), affects: ["production"],
      help: "0 gives every capital gain to other US residents, the most favorable case. 0.5 and 1 are endpoints nobody has estimated." },
    { group: "Production side", id: "production.split", label: "Which workers compete with the group", type: "levels", levels: levels("split"), affects: ["production"], help: "Where the line between the two skill groups is drawn." },
    { group: "Production side", id: "production.proxy", label: "Earnings measure", type: "levels", levels: levels("proxy"), affects: ["production"], help: "Total earnings including self-employment, or wage and salary income alone." },
    { group: "Choices the account leaves open", id: "allocation", label: "Household money", type: "levels", levels: ["personal", "shared"], affects: ["all"], help: "Personal counts each person's own taxes and benefits; shared pools them within the household. The range covers both." },
    { group: "Choices the account leaves open", id: "production.normalization", label: "How the production gain is scaled", type: "levels", levels: levels("normalization"), affects: ["production"], help: "The model's output is set equal either to national GDP or to the earnings reported in the survey divided by labor's share. The range covers both." },
    { group: "Choices the account leaves open", id: "spending_keys", label: "Rules that assign spending to the group", type: "levels", levels: ["preferred", "alternative"], affects: ["spending"], help: "The preferred rule for every category, or the alternative the account also built. The case's corrections sit on the preferred rules. Single lines can be changed in the ledger below." },
    { group: "Choices the account leaves open", id: "fiscal_weight", label: "What a budget dollar is worth to other residents", type: "slider", affects: ["all"], help: "1 means a dollar of tax money is worth a dollar to other residents. 0 is the opposite extreme; nobody estimates it. The return on public capital takes the same weight." }
  ];
  var BY_ID = {}; CONTROLS.forEach(function (k) { BY_ID[k.id] = k; });
  var PATH_LABEL = { school_response_band: "School spending, both values", general_government_response_band: "General government, both values",
    reading_band: "Readings of the long-run evidence, both", reading: "Reading of the long-run evidence",
    key_override: "Allocation rules chosen for single lines", key_band: "Allocation rules with both ends in the range", response_override: "Shares typed into the ledger" };

  function get(s, p) { return p.split(".").reduce(function (o, k) { return o == null ? o : o[k]; }, s); }
  function set(s, p, v) { var ks = p.split("."), o = s; for (var i = 0; i < ks.length - 1; i++) o = o[ks[i]]; if (v === undefined) delete o[ks[ks.length - 1]]; else o[ks[ks.length - 1]] = v; }
  function fmt(x, d) { if (x == null || !isFinite(x)) return "n/a"; var r = Math.abs(x).toFixed(d == null ? 1 : d), s = r.replace(/\B(?=(\d{3})+(?!\d))/g, ","); return (x < 0 && parseFloat(r) !== 0 ? "−" : "") + s; }
  function fmtAuto(x) { return fmt(x, Math.abs(x) < 9.95 ? 1 : 0); }  // whole billions, one decimal below ten
  // Parts rounded to d decimals so that they add to their total rounded once (largest remainder): printed parts add to
  // the printed total. Returns the rounded parts; their sum is the total to print.
  function roundParts(values, d) {
    var u = Math.pow(10, d), total = Math.round(values.reduce(function (a, x) { return a + x; }, 0) * u);
    var floors = values.map(function (x) { return Math.floor(x * u); }), left = total - floors.reduce(function (a, x) { return a + x; }, 0);
    values.map(function (x, i) { return [x * u - floors[i], i]; }).sort(function (a, b) { return b[0] - a[0]; })
      .slice(0, left).forEach(function (r) { floors[r[1]] += 1; });
    return floors.map(function (x) { return x / u; });
  }
  function total(xs) { return xs.reduce(function (a, x) { return a + x; }, 0); }
  function signed(x, d) { return (x > 1e-9 ? "+" : "") + fmt(x, d); }
  function money(x) { return (x < 0 ? "−\u2060$" : "$") + fmt(Math.abs(x), 0); }
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
      medicare_income: "People covered by Medicare, weighted by income", modeled_owner_property: "Property tax modeled for owner-occupied homes", none: "Paid from abroad, none assigned",
      housing_support: "Housing subsidy received", renter_contract_rent: "Contract rent paid", capital_key_offset: "None: it carries a key for the capital return" }
  };
  function keyName(side, k) { return KEY[side][k] || String(k).replace(/_/g, " "); }
  // Numbers print to three decimals at most; the two ends of a band print to the same number of decimals.
  function ends(v) {
    var d = Math.max.apply(null, v.map(function (x) { var t = show(x), i = t.indexOf("."); return i < 0 ? 0 : t.length - i - 1; }));
    return v.map(function (x) { return x.toFixed(d); });
  }
  function show(v) {
    if (Array.isArray(v)) return (v.every(function (x) { return typeof x === "number"; }) ? ends(v) : v.map(show)).join(" and ");  // a band: both values enter the range
    if (v && typeof v === "object") {  // per-line rules (their names say which line) or typed shares, keyed by line
      var ids = Object.keys(v);
      return ids.length ? ids.map(function (id) {
        return typeof v[id] === "number" ? label(id.replace(/^receipt:/, "")) + ": " + show(v[id]) : [].concat(v[id]).map(function (k) { return keyName("spending", k); }).join(" and ");
      }).join("; ") : "none";
    }
    return typeof v === "number" ? String(Math.round(v * 1000) / 1000) : v === true ? "yes" : v === false ? "no" : v == null ? "none" : OPTION[v] || String(v).replace(/_/g, " ");
  }
  // A value as its control names it (a case option such as long_run "case"), else as show() prints it.
  function showAt(path, v) { var k = BY_ID[path]; return k && k.names && k.names[String(v)] !== undefined ? k.names[String(v)] : show(v); }
  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  // Order-blind: a band restored by "back to" lands last in the state, and the state is still the same.
  function canon(v) {
    if (Array.isArray(v)) return "[" + v.map(canon).join(",") + "]";
    if (v && typeof v === "object") return "{" + Object.keys(v).sort().map(function (k) { return JSON.stringify(k) + ":" + canon(v[k]); }).join(",") + "}";
    return JSON.stringify(v === undefined ? null : v);
  }
  function same(a, b) { return canon(a) === canon(b); }

  /* ---------- sources: one registry, cited wherever a claim appears ---------- */
  // External sources first, then documents of this repo (kind "repo"), which open their file in the checkout.
  var SOURCES = SRC.sources.slice().sort(function (a, b) { return ((a.kind === "repo") - (b.kind === "repo")) || (a.authors + " " + a.year).localeCompare(b.authors + " " + b.year); });
  var BY_SUPPORT = {};
  SOURCES.forEach(function (s) { (s.supports || []).forEach(function (id) { (BY_SUPPORT[id] = BY_SUPPORT[id] || []).push(s); }); });
  function citation(s) { return s.authors + " (" + s.year + "). " + s.title + (s.venue ? ". " + s.venue : "") + "."; }
  function sourceHref(s) { return s.kind === "repo" ? repoHref(s.path) : s.url; }
  function sourceLink(s) { return '<a href="' + esc(sourceHref(s)) + '" target="_blank" rel="noopener" title="' + esc(citation(s)) + '">' + esc(s.short) + '</a>'; }
  function citeLinks(ids) {
    var seen = {}, list = [];
    [].concat(ids).forEach(function (id) { (BY_SUPPORT[id] || []).forEach(function (s) { if (!seen[s.key]) { seen[s.key] = 1; list.push(s); } }); });
    return list.map(sourceLink).join(", ");
  }
  // A preset setting's `cite` names sources by key (build_ui.py refuses a key the registry lacks).
  var BY_KEY = {};
  SOURCES.forEach(function (s) { BY_KEY[s.key] = s; });
  function keyLinks(keys) { return keys && keys.length ? ' <span class="cites">Source: ' + keys.map(function (k) { return sourceLink(BY_KEY[k]); }).join(", ") + '</span>' : ""; }
  function cites(ids, lead) { var links = citeLinks(ids); return links ? '<span class="cites">' + (lead || "Sources: ") + links + '</span>' : ""; }
  function repoHref(path) { return SRC.repo_prefix + "/" + path.split("/").map(encodeURIComponent).join("/"); }
  function repoLinks(text) {  // a file named in a reference opens the local copy; only paths the build found on disk are linked
    return esc(text).replace(/[A-Za-z0-9_][A-Za-z0-9_.\/-]*\.(?:md|py|csv|json|js|cjs|sql|html)\b/g, function (tok) {
      var path = SRC.paths[tok]; return path ? '<a class="path" href="' + repoHref(path) + '" target="_blank" rel="noopener">' + tok + '</a>' : tok; });
  }

  // A preset's settings: those of the preset it extends, then its own. A null value removes a band.
  var BY_PRESET = {}; PRESETS.forEach(function (p) { BY_PRESET[p.id] = p; });
  function presetSettings(p) { return (p.extends ? BY_PRESET[p.extends].settings : []).concat(p.settings || []); }
  function presetState(p) {
    var s = C.defaultState();
    presetSettings(p).forEach(function (x) { if (x.path) set(s, x.path, x.value === null ? undefined : JSON.parse(JSON.stringify(x.value))); });
    return s;
  }
  var CENTRAL_PRESET = PRESETS.filter(function (p) { return p.central; })[0], CENTRAL_ID = CENTRAL_PRESET.id, CENTRAL = presetState(CENTRAL_PRESET);
  var PRESET_STATE = {}; PRESETS.forEach(function (p) { PRESET_STATE[p.id] = presetState(p); });
  // Every field of the state, so the attribution's shares add up to the difference whatever a preset changed.
  var PATHS = Object.keys(CENTRAL).reduce(function (a, k) {
    return a.concat(k === "production" ? Object.keys(CENTRAL.production).map(function (d) { return "production." + d; }) : [k]);
  }, []).concat(["school_response_band", "general_government_response_band", "reading_band"].filter(function (p) { return !(p in CENTRAL); }));
  // States the case lane ran too (presets.json lane_readings, each gated by test_engine.js): the central case with stated changes.
  var LANE_STATES = P.lane_readings.rows.map(function (r) {
    var s = E.clone(CENTRAL);
    Object.keys(r.changes).forEach(function (p) { set(s, p, r.changes[p] === null ? undefined : r.changes[p]); });
    return { label: r.label, state: s };
  });
  // A control whose central value is a band shows both ends; moving it drops the band, going back restores it.
  var BAND_OF = { school_response: "school_response_band", general_government_response: "general_government_response_band" };
  function centralText(k) { return BAND_OF[k.id] && CENTRAL[BAND_OF[k.id]] ? ends(CENTRAL[BAND_OF[k.id]]).join("–") : showAt(k.id, get(CENTRAL, k.id)); }
  function restoreBand(s, id) { if (BAND_OF[id]) { if (CENTRAL[BAND_OF[id]]) s[BAND_OF[id]] = E.clone(CENTRAL[BAND_OF[id]]); else delete s[BAND_OF[id]]; } }

  function outcome(s, key) {
    var out = C.evaluate(s), range = C.range(s, key || lens);
    return { out: out, value: out[key || lens], range: range };
  }

  // Amounts that preset and author text name as {assigned:<name>}: read from the ledger of the state the text
  // describes when it is drawn, never typed (build_ui.py refuses a name not defined here).
  function lineSum(o, ids) { return o.spending.filter(function (l) { return ids.indexOf(l.id) >= 0; }).reduce(function (a, l) { return a + l.amount_bn; }, 0); }
  function classSum(o, cls) { return (o.classes[cls] || { assigned_bn: 0 }).assigned_bn; }
  var ASSIGNED = {
    education: function (o) { return lineSum(o, ["education_services", CORR.education_school_part, CORR.education_other_part]); },
    services: function (o) { return classSum(o, "service") + classSum(o, "education_school_part") + classSum(o, "education_other_part"); },
    other_services: function (o) { return classSum(o, "service") - lineSum(o, ["education_services"]); },
    benefits: function (o) { return classSum(o, "household_transfer"); },
    defense_and_interest: function (o) { return lineSum(o, ["defense", "domestic_interest"]); }
  };
  function liveText(text, s) {
    var o = null;
    return String(text == null ? "" : text).replace(/\{assigned:([a-z_]+)\}/g, function (m, name) { o = o || C.evaluate(s); return fmt(ASSIGNED[name](o), 0); });
  }

  function executedStatus(s) {
    if (same(s, CENTRAL)) return ["formula", "The main case (" + CENTRAL_PRESET.kind_label + "), computed as its lane computes it"];
    var hit = LANE_STATES.filter(function (r) { return same(s, r.state); })[0];
    if (hit) return ["formula", "A reading the case lane ran too: " + hit.label + ". The page reproduces the lane's figure"];
    var convention = PRESETS.filter(function (p) { return same(s, PRESET_STATE[p.id]); })[0];
    if (convention) return ["formula", "The convention “" + convention.label + "”, computed with the case's formula; the case lane did not run it"];
    var d = C.defaultState(), contract = ["transfer_response", "interest_response", "subsidy_response", "direct_receipt_response", "indirect_receipt_response"]
      .every(function (k) { return s[k] === d[k]; }) && !Object.keys(s.response_override).length && s.count_production;
    if (!contract) return ["own", "Your own assumptions: the case's formula, with settings the case never uses"];
    return ["formula", "Computed with the case's formula; the case lane did not run this combination"];
  }

  /* ---------- drawing ---------- */
  var LENS_TEXT = { welfare_bn: "The yearly effect of the lineage's presence on all other US residents: taxes received, benefits and services paid for, the return on the public capital it uses, and the gain from its labor.",
    target_balance_bn: "What the group pays in minus everything the ledger assigns to it, each line at average cost. No production side, and no return on public capital, which is not a budget line.",
    normalized_gap_bn: "The group's balance measured against an equal per-head share of the national balance." };

  function drawBar() {
    var o = outcome(state), c = outcome(CENTRAL), diff = o.value - c.value;
    $("b-value").textContent = fmt(o.value, 1); $("b-value").className = o.value < 0 ? "neg" : "pos";
    $("b-range").innerHTML = "open choices span <b>" + fmtAuto(o.range[0]) + "</b> to <b>" + fmtAuto(o.range[1]) + "</b>";
    $("b-central").innerHTML = "main case <b>" + fmt(c.value, 1) + "</b>";
    $("b-diff").innerHTML = Math.abs(diff) < 0.05 ? "no difference" : "difference <b>" + signed(diff, 1) + "</b>";
    var k = BY_ID[activeControl];
    $("b-active").classList.toggle("live", !!k);  // on a phone the hint is dropped to keep the readout short
    if (!k) { $("b-active").textContent = "Move a slider or pick an option to see its central value and what it alone does to the result."; return; }
    var back = E.clone(state); set(back, k.id, JSON.parse(JSON.stringify(get(CENTRAL, k.id)))); restoreBand(back, k.id);
    var alone = o.value - C.evaluate(back)[lens];
    $("b-active").innerHTML = "<b>" + esc(k.label) + "</b>: " + esc(showAt(k.id, get(state, k.id))) + " (central " + esc(centralText(k)) + "). " +
      (same(get(state, k.id), get(CENTRAL, k.id)) ? "" : Math.abs(alone) < 0.05 ? "It does not move this result." : "On its own it moves the result by " + signed(alone, 1) + " bn.");
  }

  var PRESET_OUTCOME = {};  // a preset's result moves only with the lens
  function presetOutcome(p) { var k = lens + " " + p.id; return PRESET_OUTCOME[k] || (PRESET_OUTCOME[k] = outcome(presetState(p))); }
  function drawPresets() {
    var cards = PRESETS.map(function (p) { return { p: p, v: presetOutcome(p) }; });
    if (!activePreset) cards.unshift({ p: { id: "", kind_label: "Live", label: "Your current settings" }, v: outcome(state), current: true });
    // Readouts are costs read from lane files: on the effect lens they sit on the same scale, as negative effects.
    var reads = lens === "welfare_bn" ? P.readouts.map(function (r) { return { p: r, v: { value: -r.band[0], range: [-r.band[1], -r.band[0]] }, readout: true }; }) : [];
    var all = cards.concat(reads);
    var lo = Math.min.apply(null, all.map(function (c) { return Math.min(c.v.range[0], 0); })), hi = Math.max.apply(null, all.map(function (c) { return Math.max(c.v.range[1], 0); }));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("presets").innerHTML = all.map(function (c) {
      var v = c.v, a = x(Math.min(v.range[0], v.range[1])), b = x(Math.max(v.range[0], v.range[1]));
      var inner = '<span class="pk">' + esc(c.p.kind_label).replace(/\d{4}-\d{2}-\d{2}/g, "<span>$&</span>") + '</span><span class="pl">' + esc(c.p.label) + '</span>' +
        '<span class="pv">' + fmtAuto(v.range[0]) + (Math.abs(v.range[1] - v.range[0]) > 0.5 ? " to " + fmtAuto(v.range[1]) : "") + '</span>' +
        '<span class="track"><i class="zero" style="left:' + x(0) + '%"></i><i class="span ' + (v.value < 0 ? "neg" : "pos") + '" style="left:' + a + '%;width:' + Math.max(b - a, 0.8) + '%"></i></span>';
      if (c.readout) return '<a class="preset readout" href="#readout-' + c.p.id + '" title="Read from a lane file; the page does not compute it">' + inner + '</a>';
      return c.current ? '<div class="preset current">' + inner + '</div>'
        : '<button class="preset' + (activePreset === c.p.id ? " on" : "") + '" data-preset="' + c.p.id + '" id="preset-' + c.p.id + '">' + inner + '</button>';
    }).join("");
  }

  // The readouts' notes, once: what each figure holds, its benefits-when-paid twin where the lane has one, and its source.
  function drawReadouts() {
    $("readouts").innerHTML = P.readouts.map(function (r) {
      var band = "$" + fmt(r.band[0], 1) + "–" + fmt(r.band[1], 1) + "bn";
      return '<p class="sub" id="readout-' + r.id + '"><i>' + esc(r.label) + ', ' + band + ' a year.</i> ' + repoLinks(r.summary) +
        (r.cash_band ? " Counting benefits when paid it is $" + fmt(r.cash_band[0], 1) + "–" + fmt(r.cash_band[1], 1) + "bn." : "") +
        (r.rule ? ' The lane\'s rule: ' + esc(r.rule) + '.' : "") + ' <span class="path">' + repoLinks(r.ref) + '</span>' + cites("readout:" + r.id) + '</p>';
    }).join("");
  }

  function drawHeadline() {
    var o = outcome(state), c = outcome(CENTRAL), st = executedStatus(state);
    var parts, exact = true;
    try { parts = C.attribute(CENTRAL, state, PATHS, lens); }
    catch (err) {  // too many changed controls for an exact split: fall back to one at a time
      exact = false;
      parts = PATHS.filter(function (p) { return !same(get(CENTRAL, p), get(state, p)); }).map(function (p) {
        var s = E.clone(CENTRAL); set(s, p, E.clone({ v: get(state, p) }).v); return { path: p, from: get(CENTRAL, p), to: get(state, p), effect_bn: C.evaluate(s)[lens] - c.value }; });
    }
    // Exact shares add up to the difference, so they print rounded to add up to it; changes made alone do not add up.
    var shown = exact ? roundParts(parts.map(function (p) { return p.effect_bn; }), 1) : parts.map(function (p) { return Math.round(p.effect_bn * 10) / 10; });
    parts.forEach(function (p, i) { p.shown = shown[i]; });
    var gap = exact ? total(shown) : o.value - c.value;
    parts = parts.filter(function (p) { return p.shown !== 0; }).sort(function (a, b) { return Math.abs(b.effect_bn) - Math.abs(a.effect_bn); });
    $("diff-title").textContent = parts.length ? "Why this differs from the main case" : "This is the main case";
    $("h-name").textContent = LENS_TEXT[lens] + (parts.length ? " It stands " + signed(gap, 1) + " bn from the main case. " + (exact
      ? "Each bar is one changed assumption's share of that; the shares allow for interactions and add up exactly."
      : "Each bar is one assumption changed alone; too many differ to split their interactions.") : "");
    var max = Math.max.apply(null, parts.map(function (p) { return Math.abs(p.effect_bn); }).concat([1]));
    $("diff").innerHTML = parts.map(function (p) {
      var k = BY_ID[p.path] || { label: PATH_LABEL[p.path] || p.path.replace(/_/g, " ") };
      return '<li data-affects="' + (k.affects || []).join(" ") + '"><span class="dl">' + esc(k.label) + '<em>' + esc(showAt(p.path, p.from)) + " → " + esc(showAt(p.path, p.to)) + '</em></span>' +
        '<span class="db"><i class="' + (p.effect_bn < 0 ? "neg" : "pos") + '" style="width:' + Math.abs(p.effect_bn) / max * 100 + '%"></i></span><span class="dv">' + signed(p.shown, 1) + '</span></li>';
    }).join("");
    var bands = [];  // bands these assumptions declare; the case's range spans every combination, readings paired with general government
    if (state.school_response_band) bands.push("both school values, " + show(state.school_response_band));
    if (state.reading_band && state.general_government_response_band) bands.push("both readings of the long-run evidence, each with its general-government value, " + show(state.general_government_response_band));
    else {
      if (state.reading_band) bands.push("both readings of the long-run evidence");
      if (state.general_government_response_band) bands.push("both general-government values, " + show(state.general_government_response_band));
    }
    Object.keys(state.key_band || {}).forEach(function (id) { bands.push("both ends of the allocation rule for " + label(id)); });
    $("h-range").textContent = "The account leaves three choices open: whether household money is shared, how the production gain is scaled, and the school share of education" +
      (bands.length ? ". These assumptions add " + bands.slice(0, -1).join("; ") + (bands.length > 1 ? "; and " : "") + bands[bands.length - 1] : "") +
      ". Across them the result runs from " + fmtAuto(o.range[0]) + " to " + fmtAuto(o.range[1]) + " bn.";
    var member = function (bn) { return money(bn * 1e9 / C.lineage_population); };
    $("h-per").textContent = (lens === "welfare_bn" ? money(o.out.per_other_resident) + " a year per other resident; " + member(o.value) + " per member of the lineage"
      : member(o.value) + " a year per member of the lineage") + (o.range[1] - o.range[0] > 0.5 ? ", " + member(o.range[0]) + " to " + member(o.range[1]) + " across the open choices." : ".");
    $("h-status").textContent = st[1]; $("h-status").className = "status " + st[0];
  }

  // Each step: [label, counted, assigned but not counted, tokens it touches, optional]. An optional step is drawn
  // only when it is non-zero here or in the main case.
  function bridgeSteps(out, s) {
    var w = s.fiscal_weight, c = out.classes, g = function (k) { return c[k] || { assigned_bn: 0, responsive_bn: 0 }; };
    var line = out.spending.filter(function (l) { return l.id === "education_services"; })[0], PG = "public_goods defense general_public_services";
    // Education carries the two case lines that respond as its school and college parts; fixed is the case line
    // counted in full.
    var parts = [g("education_school_part"), g("education_other_part")], fixed = g("correction_constant"), cap = out.capital;
    var edu = { amount_bn: line.amount_bn + parts[0].assigned_bn + parts[1].assigned_bn, effect_bn: line.effect_bn - parts[0].responsive_bn - parts[1].responsive_bn };
    var EDU = ["education_services", CORR.education_school_part, CORR.education_other_part].join(" "), FIXED = "Care, shelter and audit items";
    if (lens !== "welfare_bn") {
      var steps = [["Taxes the group pays", g("direct_receipts").assigned_bn, 0, "direct_receipts"], ["Corporate, property and asset receipts", g("incidence_receipts").assigned_bn, 0, "incidence_receipts"],
        ["Benefits paid to the group", -g("household_transfer").assigned_bn, 0, "household_transfer"], ["Education", -edu.amount_bn, 0, EDU],
        ["Other public services", -(g("service").assigned_bn - line.amount_bn), 0, "service"], ["Defense and general government", -g("public_goods").assigned_bn, 0, PG],
        ["Interest and subsidies", -(g("interest").assigned_bn + g("subsidy").assigned_bn), 0, "interest subsidy"], [FIXED, -fixed.assigned_bn, 0, CORR.correction_constant, true]];
      if (lens === "normalized_gap_bn") steps.push(["Less an equal per-head share of the national balance", out.normalized_gap_bn - out.target_balance_bn, 0, "all"]);
      return steps;
    }
    return [["Taxes the group pays", w * g("direct_receipts").responsive_bn, g("direct_receipts").assigned_bn - g("direct_receipts").responsive_bn, "direct_receipts"],
      ["Corporate, property and asset receipts", w * g("incidence_receipts").responsive_bn, g("incidence_receipts").assigned_bn - g("incidence_receipts").responsive_bn, "incidence_receipts"],
      ["Benefits paid to the group", -w * g("household_transfer").responsive_bn, -(g("household_transfer").assigned_bn - g("household_transfer").responsive_bn), "household_transfer"],
      ["Gain to other residents from the group's work", out.private_wtp_bn + w * out.induced_receipts_bn, 0, "production"],
      ["Education", w * edu.effect_bn, -(edu.amount_bn + edu.effect_bn), EDU],
      ["Other public services", -w * (g("service").responsive_bn + line.effect_bn), -((g("service").assigned_bn - line.amount_bn) - (g("service").responsive_bn + line.effect_bn)), "service"],
      ["Defense and general government", -w * g("public_goods").responsive_bn, -(g("public_goods").assigned_bn - g("public_goods").responsive_bn), PG],
      ["Interest and subsidies", -w * (g("interest").responsive_bn + g("subsidy").responsive_bn), -((g("interest").assigned_bn + g("subsidy").assigned_bn) - (g("interest").responsive_bn + g("subsidy").responsive_bn)), "interest subsidy"],
      ["Return on public capital", -w * cap.total_bn, -(cap.assigned_bn - cap.total_bn), "capital", true],
      [FIXED, -w * fixed.responsive_bn, -(fixed.assigned_bn - fixed.responsive_bn), CORR.correction_constant, true]];
  }

  function drawBridge() {
    var out = C.evaluate(state), steps = bridgeSteps(out, state), cSteps = bridgeSteps(C.evaluate(CENTRAL), CENTRAL);
    var keep = steps.map(function (s, i) { return !s[4] || Math.abs(s[1]) + Math.abs(s[2]) + Math.abs(cSteps[i][1]) > 0.005; });
    steps = steps.filter(function (s, i) { return keep[i]; }); cSteps = cSteps.filter(function (s, i) { return keep[i]; });
    // Printed values add up: the counted steps to the printed result, their changes to the printed difference.
    var shown = roundParts(steps.map(function (s) { return s[1]; }), 1), moved = roundParts(steps.map(function (s, i) { return s[1] - cSteps[i][1]; }), 1);
    var anyMoved = moved.some(function (m) { return m !== 0; });
    var run = 0, lo = 0, hi = 0;
    steps.forEach(function (s) { var ghost = run + s[1] + s[2]; run += s[1]; lo = Math.min(lo, run, ghost); hi = Math.max(hi, run, ghost); });
    // A column of changes against the main case sits at the right edge when anything moved, under its own heading.
    var rowH = 30, left = 340, plotRight = 680, top = anyMoved ? 22 : 0, W = anyMoved ? 900 : 830, H = (steps.length + 1) * rowH + 26 + top;
    var x = function (v) { return left + (v - lo) / (hi - lo || 1) * (plotRight - left); }, edge = W - 4;
    var svg = '<svg viewBox="0 0 ' + W + " " + H + '" role="img" aria-label="Bridge from taxes paid to the result"><line class="axis" x1="' + x(0) + '" x2="' + x(0) + '" y1="' + (4 + top) + '" y2="' + (H - 20) + '"/>';
    if (anyMoved) svg += '<text class="val dlt" x="' + edge + '" y="14" text-anchor="end">against the main case</text>';
    run = 0;
    steps.forEach(function (s, i) {
      var y = 8 + top + i * rowH, a = run, b = run + s[1], ghostEnd = b + s[2]; run = b;
      svg += '<g class="step" data-affects="' + s[3] + '"><title>' + esc(s[0]) + ": " + signed(shown[i], 1) + " bn counted" + (Math.abs(s[2]) > 0.05 ? "; " + fmt(Math.abs(s[2]), 1) + " bn assigned to the group but left out" : "") + '</title>' +
        '<text class="lab" x="' + (left - 12) + '" y="' + (y + 17) + '" text-anchor="end">' + esc(s[0]) + '</text>';
      if (Math.abs(s[2]) > 0.05) svg += '<rect class="ghost" x="' + Math.min(x(b), x(ghostEnd)) + '" y="' + (y + 6) + '" width="' + Math.abs(x(ghostEnd) - x(b)) + '" height="12"/>';
      svg += '<rect class="' + (s[1] < 0 ? "neg" : "pos") + '" x="' + Math.min(x(a), x(b)) + '" y="' + (y + 6) + '" width="' + Math.max(Math.abs(x(b) - x(a)), 1) + '" height="12"/>' +
        '<text class="val" x="' + (Math.max(x(a), x(b), x(ghostEnd)) + 6) + '" y="' + (y + 17) + '">' + signed(shown[i], 1) + '</text>' +
        (moved[i] !== 0 ? '<text class="val dlt" x="' + edge + '" y="' + (y + 17) + '" text-anchor="end">' + signed(moved[i], 1) + '</text>' : "") +
        '<line class="link" x1="' + x(b) + '" x2="' + x(b) + '" y1="' + (y + 18) + '" y2="' + (y + rowH + 6) + '"/></g>';
    });
    var yEnd = 8 + top + steps.length * rowH;  // one rule above the total, as under a column of figures
    svg += '<line class="sum" x1="' + (left - 120) + '" x2="' + (anyMoved ? edge : plotRight + 60) + '" y1="' + (yEnd + 1) + '" y2="' + (yEnd + 1) + '"/>' +
      '<text class="lab tot" x="' + (left - 12) + '" y="' + (yEnd + 19) + '" text-anchor="end">Result</text><rect class="' + (run < 0 ? "neg" : "pos") + ' total" x="' + Math.min(x(0), x(run)) + '" y="' + (yEnd + 8) + '" width="' + Math.max(Math.abs(x(run) - x(0)), 1) + '" height="12"/>' +
      '<text class="val tot" x="' + (Math.max(x(0), x(run)) + 6) + '" y="' + (yEnd + 19) + '">' + fmt(total(shown), 1) + ' bn</text>' +
      (anyMoved ? '<text class="val tot dlt" x="' + edge + '" y="' + (yEnd + 19) + '" text-anchor="end">' + signed(total(moved), 1) + '</text>' : "") + '</svg>';
    $("bridge").innerHTML = svg;
  }

  function drawTornado() {
    var base = C.evaluate(state)[lens];
    var rows = CONTROLS.map(function (k) {
      var ends = k.type === "slider" ? [k.min == null ? 0 : k.min, k.max == null ? 1 : k.max] : k.levels;
      var vals = ends.map(function (v) { var s = E.clone(state); set(s, k.id, v); if (BAND_OF[k.id]) delete s[BAND_OF[k.id]]; return { v: v, y: C.evaluate(s)[lens] }; });
      vals.sort(function (a, b) { return a.y - b.y; });
      return { k: k, lo: vals[0], hi: vals[vals.length - 1], swing: vals[vals.length - 1].y - vals[0].y };
    }).filter(function (r) { return r.swing > 0.05; }).sort(function (a, b) { return b.swing - a.swing; });
    var lo = Math.min.apply(null, rows.map(function (r) { return r.lo.y; }).concat([base])), hi = Math.max.apply(null, rows.map(function (r) { return r.hi.y; }).concat([base]));
    var x = function (v) { return (v - lo) / (hi - lo || 1) * 100; };
    $("tornado").innerHTML = rows.map(function (r) {
      return '<li data-affects="' + r.k.affects.join(" ") + '" data-control="' + r.k.id + '"><span class="tl">' + esc(r.k.label) + '</span><span class="tb"><i class="bar" style="left:' + x(r.lo.y) + '%;width:' + (x(r.hi.y) - x(r.lo.y)) + '%"></i><i class="now" style="left:' + x(base) + '%"></i></span>' +
        '<span class="tv">' + fmtAuto(r.lo.y) + " " + esc(atLevel(r.k, r.lo.v)) + ", " + fmtAuto(r.hi.y) + " " + esc(atLevel(r.k, r.hi.v)) + "</span></li>";
    }).join("") || "<li>No assumption moves this result.</li>";
    $("tornado-note").textContent = "Each bar shows the result across one assumption's full range, with everything else held where it is now. The tick marks the current result, " + fmt(base, 1) + " bn.";
  }
  function atLevel(k, v) { return k.names ? showAt(k.id, v) : "at " + show(v); }  // a named option reads after the number

  function drawControls() {
    var groups = {}, order = [];
    CONTROLS.forEach(function (k) { if (!groups[k.group]) { groups[k.group] = []; order.push(k.group); } groups[k.group].push(k); });
    $("controls").innerHTML = order.map(function (g) {
      return '<fieldset><legend>' + esc(g) + '</legend>' + groups[g].map(function (k) {
        var v = get(state, k.id), c = get(CENTRAL, k.id), differs = !same(v, c), input;
        if (k.type === "slider") {
          var min = k.min == null ? 0 : k.min, max = k.max == null ? 1 : k.max, pos = function (val) { return "calc(8px + (100% - 16px) * " + ((val - min) / (max - min || 1)) + ")"; };
          input = '<span class="rng"><input type="range" id="c-' + k.id + '" data-path="' + k.id + '" min="' + min + '" max="' + max + '" step="' + ((max - min) / 100) + '" value="' + v + '">' +
            (k.marks || []).map(function (m) { return '<i class="xm" style="left:' + pos(m) + '"></i>'; }).join("") +
            (k.adopted || []).map(function (m) { return '<i class="am" title="adopted response ' + show(m) + '" style="left:' + pos(m) + '"></i>'; }).join("") +
            '<i class="cm" title="central value" style="left:' + pos(c) + '"></i></span><output>' + show(v) + '</output>';
        } else {
          input = '<span class="seg" role="radiogroup" aria-label="' + esc(k.label) + '">' + k.levels.map(function (l) {
            return '<label class="opt"><input type="radio" name="c-' + k.id + '" data-path="' + k.id + "\" data-value='" + JSON.stringify(l) + "'" + (same(l, v) ? " checked" : "") + '><span>' + esc(showAt(k.id, l)) + (same(l, c) ? " <i>(central)</i>" : "") + '</span></label>'; }).join("") + '</span>';
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
    var out = C.evaluate(state);
    $("ledger-corr").textContent = "Amounts are the main case's: the data corrections and the " + (C.added_population / 1e6).toFixed(2) +
      " million added descendants are in every line. The last spending group holds the case's own lines, parts of the lines above that it re-prices or re-keys.";
    function table(lines, side) {
      var groups = {}; lines.forEach(function (l) { var g = PAYLOAD_LINES[l.id] ? "case_lines" : l.group; (groups[g] = groups[g] || []).push(l); });
      var max = Math.max.apply(null, lines.map(function (l) { return Math.abs(l.amount_bn); }));
      return Object.keys(groups).map(function (g) {
        var rows = groups[g].filter(function (l) { return Math.abs(l.amount_bn) > 0.005; }).sort(function (a, b) { return Math.abs(b.amount_bn) - Math.abs(a.amount_bn); });
        if (!rows.length) return "";
        // Counted is in the assigned amount's units: a receipt's effect, a spending line's effect with its sign turned.
        var assigned = roundParts(rows.map(function (l) { return l.amount_bn; }), 1), counted = roundParts(rows.map(function (l) { return side === "spending" ? -l.effect_bn : l.effect_bn; }), 1);
        return '<tbody data-affects="' + g + '"><tr class="grp"><th colspan="3">' + esc(CLASS_LABEL[g] || g) + findButton(g) + '</th><td class="num">' + fmt(total(assigned), 1) + '</td><td class="num">' + fmt(total(counted), 1) + '</td><td></td></tr>' + rows.map(function (l, i) {
          var oid = (side === "receipts" ? "receipt:" : "") + l.id, overridden = typeof state.response_override[oid] === "number", own = !!PAYLOAD_LINES[l.id];
          var keyCell = own ? "The case's own figure" : side === "spending" && l.keys.length > 1 ? '<select data-key="' + l.id + '" id="k-' + l.id + '" aria-label="Allocation rule for ' + esc(label(l.id)) + '">' + l.keys.map(function (k) { return '<option value="' + esc(k) + '" title="rule id: ' + esc(k) + '"' + (k === l.key ? " selected" : "") + '>' + esc(keyName(side, k)) + '</option>'; }).join("") + '</select>' : '<span title="rule id: ' + esc(l.key) + '">' + esc(keyName(side, l.key)) + '</span>';
          var band = side === "spending" && (state.key_band || {})[l.id];
          if (band) keyCell += '<small title="' + esc(band.map(function (k) { return keyName(side, k); }).join(" and ")) + '">Both ends of this rule enter the range.</small>';
          return '<tr data-affects="' + l.id + " " + g + '"><td>' + esc(label(l.id)) + findButton(l.id) + '</td><td class="key">' + keyCell + '</td><td class="num">' + (own ? "" : (l.share * 100).toFixed(1) + "%") + '</td><td class="num">' + fmt(assigned[i], 1) + '</td>' +
            '<td class="num">' + fmt(counted[i], 1) + '</td><td class="resp"><div><input type="number" min="0" max="1" step="0.05" id="r-' + oid + '" data-resp="' + oid + '" aria-label="Share counted for ' + esc(label(l.id)) + '" value="' + (Math.round(l.response * 1000) / 1000) + '"' + (overridden ? ' class="ov"' : "") + '><span class="mini"><i style="width:' + Math.abs(l.amount_bn) / max * 100 + '%"></i><b style="width:' + Math.abs(l.effect_bn) / max * 100 + '%"></b></span></div></td></tr>';
        }).join("") + '</tbody>';
      }).join("");
    }
    var head = '<thead><tr><th>Line</th><th>Assigned by</th><th class="num">Group share</th><th class="num">Assigned, bn</th><th class="num">Counted, bn</th><th>Share counted (0 to 1)</th></tr></thead>';
    $("ledger-receipts").innerHTML = head + table(out.receipts, "receipts");
    $("ledger-spending").innerHTML = head + table(out.spending, "spending");
    drawCapital(out);
  }

  // The return on public capital by the line whose response it follows (meta.capital_return's components); offsets
  // sit with the component they adjust, and every enterprise is one row.
  function capitalRow(c) {
    var comp = K.components.filter(function (x) { return x.id === (c.of_component || c.id); })[0];
    if (comp.part === "enterprise") return "Government enterprises";
    var line = comp.response.line;
    return line === CORR.education_school_part ? "Schools" : line === CORR.education_other_part ? "Colleges and other education" : label(line);
  }
  var CAPITAL_ROWS = [];
  K.components.forEach(function (c) { var r = capitalRow(c); if (CAPITAL_ROWS.indexOf(r) < 0) CAPITAL_ROWS.push(r); });
  function drawCapital(out) {
    var cap = out.capital, rows = {};
    CAPITAL_ROWS.forEach(function (r) { rows[r] = { stock: 0, assigned: 0, counted: 0 }; });
    cap.components.forEach(function (x) {
      var c = K.components.filter(function (y) { return y.id === x.id; })[0], r = rows[capitalRow(c)];
      if (!c.of_component) r.stock += c.stock_charged_bn;
      r.assigned += c.stock_charged_bn * cap.rate * x.key; r.counted += x.return_bn;
    });
    var max = Math.max.apply(null, CAPITAL_ROWS.map(function (r) { return Math.abs(rows[r].assigned); }).concat([1e-9]));
    var col = function (k, d) { return roundParts(CAPITAL_ROWS.map(function (r) { return rows[r][k]; }), d); };
    var stock = col("stock", 0), assigned = col("assigned", 1), counted = col("counted", 1);  // printed rows add to the printed totals
    $("capital-note").textContent = cap.rate ? "Each row: the public capital the line uses, the return on it at " + (cap.rate * 100).toFixed(0) + "% (this reading's rate), the group's part of that return by the line's own key (the group's return), and the share counted, which follows the line's response. Return to the group = stock × rate × the group's key × the share counted."
      : "The current assumptions charge no return on public capital.";
    $("ledger-capital").innerHTML = '<thead><tr><th>Public capital</th><th class="num">Stock, bn</th><th class="num">Group\'s return, bn</th><th class="num">Counted, bn</th><th>Share counted</th></tr></thead><tbody data-affects="capital">' +
      CAPITAL_ROWS.map(function (r, i) {
        var x = rows[r], share = x.assigned ? x.counted / x.assigned : 0;
        return '<tr data-affects="capital"><td>' + esc(r) + '</td><td class="num">' + fmt(stock[i], 0) + '</td><td class="num">' + fmt(assigned[i], 1) + '</td><td class="num">' + fmt(counted[i], 1) + '</td>' +
          '<td class="resp"><div><span class="num">' + (Math.round(share * 1000) / 1000) + '</span><span class="mini"><i style="width:' + Math.abs(x.assigned) / max * 100 + '%"></i><b style="width:' + Math.abs(x.counted) / max * 100 + '%"></b></span></div></td></tr>';
      }).join("") + '<tr class="grp"><th>All public capital</th><td class="num">' + fmt(total(stock), 0) + '</td><td class="num">' + fmt(total(assigned), 1) + '</td><td class="num">' + fmt(total(counted), 1) + '</td><td></td></tr></tbody>';
  }

  var BASIS = { stated: "stated in the account", implied: "implied by the evidence", not_addressed: "left out by this convention" };
  function drawPresetNote() {
    var p = PRESETS.filter(function (q) { return q.id === activePreset; })[0];
    if (!p) { $("preset-note").hidden = true; return; }
    $("preset-note").hidden = false;
    var ps = presetState(p), live = function (t) { return liveText(t, ps); }, base = p.extends && BY_PRESET[p.extends];
    $("preset-note").innerHTML = '<h3>' + esc(p.label) + '</h3><p>' + repoLinks(live(p.summary)) + '</p>' + (p.scope_note ? '<p class="scope">' + repoLinks(live(p.scope_note)) + '</p>' : "") +
      '<div class="scroll"><table class="basis"><thead><tr><th>Assumption</th><th>Where it comes from</th><th>Why</th></tr></thead><tbody>' + (p.settings || []).map(function (s) {
        var value = /^key_(override|band)\./.test(s.path || "") ? [].concat(s.value).map(function (k) { return keyName("spending", k); }).join(" and ") : showAt(s.path, s.value);
        return '<tr><td>' + esc(s.label || s.path) + (s.path ? ": " + esc(value) : "") + '</td><td><span class="tag ' + esc(s.basis) + '">' + esc(BASIS[s.basis] || s.basis) + '</span></td><td>' + esc(live(s.note)) + (s.ref ? ' <span class="path">' + repoLinks(s.ref) + '</span>' : "") + keyLinks(s.cite) + '</td></tr>'; }).join("") + '</tbody></table></div>' +
      (base ? '<p class="help" style="margin-top:6px">Every other assumption is the ' + esc(base.label.toLowerCase()) + '\'s.</p>' : "") +
      (p.misses && p.misses.length ? '<h4>Left out of this set of assumptions</h4><ul>' + p.misses.map(function (m) { return '<li>' + repoLinks(live(m)) + '</li>'; }).join("") + '</ul>' : "") + cites("preset:" + p.id);
  }

  function drawStanding() {
    $("standing-title").textContent = P.standing.title;
    $("standing").innerHTML = '<tbody>' + P.standing.rows.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td><td>' + esc(r[2]) + '</td></tr>'; }).join("") + '</tbody>';
    $("standing-text").innerHTML = repoLinks(P.standing.text);
    $("standing-cites").innerHTML = citeLinks("standing") ? "Sources: " + citeLinks("standing") : "";
  }

  function drawAuthors() {
    var live = function (t) { return liveText(t, CENTRAL); };  // "this ledger" is the main case
    $("authors").innerHTML = P.authors.map(function (a) {
      var target = PRESETS.filter(function (p) { return p.id === a.closest.preset; })[0];
      return '<article><h3>' + esc(a.name) + '</h3>' + a.argues.map(function (x, i) {
        return '<p class="q">' + esc(live(x[0])) + cites("argue:" + a.id + ":" + i, "Original: ") + '<span class="cites">This repo\'s audit: ' + repoLinks(x[1]) + '</span></p>'; }).join("") +
        '<p><b>What the claim is about:</b> ' + esc(live(a.object)) + '</p><p><b>Closest convention in this ledger:</b> ' +
        (target ? '<button type="button" class="link" data-preset="' + target.id + '">' + esc(target.label) + '</button>. ' : '<span class="tag not_addressed">none</span> ') + esc(live(a.closest.why)) + '</p>' +
        '<h4>The argument leaves out</h4><ul>' + a.leaves_out.map(function (m) { return '<li>' + esc(live(m)) + '</li>'; }).join("") + '</ul>' + cites("author:" + a.id, "Also cited: ") + '</article>';
    }).join("");
  }

  function drawContext() {
    var tagText = { inside_headline: "already inside the result", overlaps_headline: "overlaps the result: do not add", outside_not_addable: "outside the account: do not add", different_object: "measures something else: compare, do not add", adds_to_headline: "left out of the result: add it" };
    var adds = CONTEXT.filter(function (c) { return c.relation_to_headline === "adds_to_headline"; }).length;
    $("context-note").textContent = adds ? adds + (adds === 1 ? " card states a result" : " cards state results") + " the main case leaves out, which add to it; no other card does."
      : "No card here adds to the main case: each result is inside it, overlaps it or measures something else.";
    $("context").innerHTML = CONTEXT.map(function (c) {
      return '<article><header><span class="tag ' + esc(c.relation_to_headline) + '">' + esc(tagText[c.relation_to_headline] || c.relation_to_headline) + '</span>' + (c.faq_entry ? '<span class="faq">FAQ ' + esc(c.faq_entry) + '</span>' : "") + '</header>' +
        (c.objection ? '<p class="obj">' + esc(c.objection) + '</p>' : "") + '<p>' + esc(c.finding) + '</p><ul>' + (c.values || []).map(function (v) {
          var file = String(v.file_line || "").replace(/:\d+(?:[-,]\d+)*$/, ""), path = SRC.paths[file];
          // A value printed as text keeps its source's digits; its minus signs print as the page's, and a unit it already names is not repeated.
          var text = typeof v.value === "number" ? fmt(v.value, Math.abs(v.value) < 10 ? 2 : 0) : String(v.value).replace(/(^|[\s(\/→])-(?=[\d$.])/g, "$1−");
          var unit = v.unit && !new RegExp("(^|\\s)" + v.unit.replace(/[.*+?^${}()|[\]\\\/]/g, "\\$&") + "$").test(text) ? v.unit : "";
          return '<li><b>' + esc(text) + '</b> ' + esc(unit) + ' <span>' + esc(v.label) + '</span>' +
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
    if (kind === "readout") { hit = P.readouts.filter(function (r) { return r.id === rest; })[0]; return hit ? "beside the presets: " + hit.label : id; }
    if (kind === "argue" || kind === "author") { hit = P.authors.filter(function (a) { return a.id === parts[1]; })[0]; return hit ? hit.name : id; }
    return { ledger: "the ledger", capital: "the return on public capital", production: "the production side", standing: "whose ledger this is" }[id] || id;
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
  $("scope").innerHTML = esc("The Mexican-origin lineage of the United States, every generation, age and level of schooling: " + (C.lineage_population / 1e6).toFixed(2) + " million people, the " +
    (C.account_union / 1e6).toFixed(2) + " million the survey identifies and " + (C.added_population / 1e6).toFixed(2) + " million descendants who no longer report Mexican origin, counted as whole people. Income year 2024, in billions of 2024 dollars. " +
    "The account compares the country as it is with the same country without the lineage, holding everything else at 2024 levels. It does not estimate what admitting or removing anyone would do. The main case was adopted on ") + '<span style="white-space:nowrap">' + esc(ADOPTED) + "</span>.";
  $("ledger-cites").innerHTML = citeLinks("ledger") ? "Sources: " + citeLinks("ledger") : "";
  $("capital-cites").innerHTML = citeLinks("capital") ? "Sources: " + citeLinks("capital") : "";
  $("bridge-cites").innerHTML = citeLinks(["production", "ledger"]) ? "Sources: " + citeLinks(["production", "ledger"]) : "";
  Array.prototype.forEach.call(document.querySelectorAll("a[data-repo]"), function (a) { var path = SRC.paths[a.dataset.repo]; if (path) { a.href = repoHref(path); a.target = "_blank"; a.rel = "noopener"; } });
  drawStanding(); drawAuthors(); drawContext(); drawLadder(); drawSources(); drawReadouts(); render();
})();
