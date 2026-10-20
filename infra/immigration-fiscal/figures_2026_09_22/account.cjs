/* The complete account as the figures page evaluates it: main case v9 (adopted 2026-10-20,
 * decisions/2026-10-16-main-case-v9.md) through its package, main_case_2026_10_16/package.cjs, on the
 * case's payload model. Each staircase step and matrix cell is one full evaluation per specification: a copy
 * of the case's specification with that step's or cell's responses, so the engine, the case's added lines,
 * its return on public capital and its post-engine items run as the case runs them. The gates compare
 * against the case's own files. build_data.cjs loads it; the prototypes page stays on the September 24 case
 * (account_sept24.cjs).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const REPO = path.join(HERE, "..", "..", "..");
const CASE_LANE = "main_case_2026_10_16";
const CASE_KEY = "oct16";
const CASE = path.join(FISCAL, CASE_LANE);
/* The research lanes move with each main case; the page moves when the operator asks (2026-10-20: to main
 * case v9). Lane files are read as they stood on v9, at a commit (git show), so a lane's next case cannot
 * reach the page unasked. The case's payload, which its package reads from the working tree, is pinned by
 * hash. */
const PINS = {
  distribution: "65b6e01c", // the who-pays lane on main case v9 (derived/oct16/)
  backcast: "e85c0766",     // the back-cast of main case v9 (derived/oct16/), with per-lineage-member columns
};
const PAYLOAD = {           // main_case_2026_10_16/derived/ as main_case.cjs wrote v9
  "corrections.json": "4300b06c5db6c9ddca86e59538be66a7aa6cea71bdf4ca9c13625756a711f530",
  "corrections_cash.json": "bb99e06673cb09daead29be13ed81dd44eabbf74bae56c06845461e2834648f7",
  "summary.json": "0d48ffa601855c68722e1c1524c22615745ff36ef4789969923934aa6f0fc45a",
};

let failureCount = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "✓" : "✗"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failureCount += 1;
}
const failures = () => failureCount;
const near = (a, b, tol = 1e-6) => Math.abs(a - b) < tol;
const round = (x, d = 4) => Math.round(x * 10 ** d) / 10 ** d;
const span = (xs) => [Math.min(...xs), Math.max(...xs)];
function product(dims) {
  return Object.entries(dims).reduce(
    (acc, [name, levels]) => acc.flatMap((spec) => levels.map((v) => ({ ...spec, [name]: v }))),
    [{}],
  );
}

/* Every file the page reads, with the sha256 of the text it read: several lane outputs are ignored or
 * untracked, so figures.json records what built it. A pinned file is read at its commit. The hash reads
 * CRLF line ends as LF, the form the repository stores, so a tracked file written with CRLF hashes the
 * same in this checkout as in a fresh clone. */
const INPUTS = new Map();
const sha256 = (text) => crypto.createHash("sha256").update(text).digest("hex");
const rel = (file) => path.relative(REPO, file);
function tracked(file) {
  try {
    execFileSync("git", ["-C", REPO, "ls-files", "--error-unmatch", rel(file)], { stdio: "ignore" });
    return true;
  } catch (e) {
    return false;
  }
}
function readText(file, pin) {
  if (pin && !PINS[pin]) throw new Error("no pin " + pin);
  const text = pin
    ? execFileSync("git", ["-C", HERE, "show", `${PINS[pin]}:${rel(file)}`], { encoding: "utf8", maxBuffer: 1 << 27 })
    : fs.readFileSync(file, "utf8");
  const key = `${rel(file)}@${pin ? PINS[pin] : "worktree"}`;
  if (!INPUTS.has(key)) {
    INPUTS.set(key, { file: rel(file), commit: pin ? PINS[pin] : null, tracked: pin ? true : tracked(file),
      sha256: sha256(text.replace(/\r\n/g, "\n")) });
  }
  return text;
}
const readJson = (file, pin) => JSON.parse(readText(file, pin));
/* RFC 4180 reader: several lane files quote fields that contain commas. */
function readCsv(file, pin) {
  const text = readText(file, pin);
  const rows = [];
  let row = [], field = "", quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (quoted) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i++; } else quoted = false;
      } else field += c;
    } else if (c === '"') quoted = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field); rows.push(row); row = []; field = "";
    } else field += c;
  }
  if (field !== "" || row.length) { row.push(field); rows.push(row); }
  const [head, ...body] = rows.filter((r) => !(r.length === 1 && r[0] === ""));
  return body.map((r) => Object.fromEntries(head.map((h, i) => [h, r[i]])));
}
const inputs = () => [...INPUTS.values()].sort((a, b) => a.file.localeCompare(b.file));

/* ---------------------------------------------------------------- the case ------------------ */

console.log("\n[main case v9]");
for (const [name, want] of Object.entries(PAYLOAD)) {
  const got = sha256(readText(path.join(CASE, "derived", name)));
  gate(`${CASE_LANE}/derived/${name} is v9's payload`, got === want, got.slice(0, 8));
}
const LIVE = readJson(path.join(FISCAL, "live_case.json"));
gate("live_case.json names this case", LIVE.key === CASE_KEY && LIVE.lane === CASE_LANE, `${LIVE.key} ${LIVE.lane}`);
const P = require(path.join(CASE, "package.cjs"));
const { Engine } = P;
gate("the package is the adopted v9 case", P.V9.STATUS === "adopted" && P.V9.CASE_KEY === CASE_KEY && P.STATUS === "adopted",
  `${P.V9.STATUS} ${P.V9.CASE_KEY}`);
gate("one engine: the package's and its September 24 base's", P.P24.Engine === Engine);
const model = P.payloadModel();
const SPECS = P.MAIN_SPECS;
const PROFILE = P.MAIN_PROFILE;
// CBO's school response (63% or 66%), the September 24 case's at the same specification: the matrix's other
// school row. Since v7 the case keeps the personal allocation only, the first half of the September 24
// specifications; it charges schools at their full cost at every specification.
const P24_SPECS = P.P24.MAIN_SPECS.slice(0, SPECS.length);
const CBO_SCHOOL = P24_SPECS.map((s) => s.school);
gate("the September 24 personal specifications line up with v9's on allocation, normalization, share and keys",
  SPECS.length === 32 && SPECS.every((s, i) => s.school === 1 && s.allocation === "personal"
    && ["allocation", "normalization", "share", "uc", "justice"].every((k) => s[k] === P24_SPECS[i][k]))
  && JSON.stringify([...new Set(CBO_SCHOOL)].sort()) === "[0.63,0.66]", `${SPECS.length} specifications`);

const SUMMARY = readJson(path.join(CASE, "derived", "summary.json"));
const V9 = SUMMARY.v9;
const MAIN = V9.band_bn;
const CASH = V9.cash_set_bn;
const bands = readCsv(path.join(CASE, "derived", "main_case_bands.csv"));
const band = (profile, variant) => {
  const row = bands.find((b) => b.profile === profile && b.variant === variant);
  if (!row) throw new Error(`no band ${profile} / ${variant}`);
  if (/historical/.test(row.v9_price_scope)) throw new Error(`band ${profile} / ${variant} is a historical row, not v9's`);
  return [Number(row.cost_low_bn), Number(row.cost_high_bn)];
};
gate("main_case_bands.csv's adopted and cash rows are summary.json's v9 (4 decimals)",
  band(PROFILE, "adopted").every((x, j) => near(x, MAIN[j], 5e-5)) && band(PROFILE, "cash_set").every((x, j) => near(x, CASH[j], 5e-5)),
  `${MAIN.map((x) => x.toFixed(6)).join("–")}; cash ${CASH.map((x) => x.toFixed(6)).join("–")}`);
// v9's own readings beside the band that the page prints (summary.json v9.companions, full precision).
const COMPANIONS = V9.companions;
const caseCosts = SPECS.map((s) => P.cost(model, s, PROFILE));
gate("the payload model reproduces the case (summary.json v9, 1e-9)",
  near(Math.min(...caseCosts), MAIN[0], 1e-9) && near(Math.max(...caseCosts), MAIN[1], 1e-9),
  `${Math.min(...caseCosts).toFixed(6)}–${Math.max(...caseCosts).toFixed(6)}`);
const GG = [P.RESPONSES.general_government.low, P.RESPONSES.general_government.high];
// The band's ends: its low and high specification, the first of each pair the September 24 school response splits.
const ENDS = [caseCosts.indexOf(Math.min(...caseCosts)), caseCosts.indexOf(Math.max(...caseCosts))];
gate("the band's ends are summary.json's v9 end specifications, in both methods and both sets",
  ["set", "cash"].every((k) => V9.end_specifications[k].every((e) => e[0] === ENDS[0] && e[1] === ENDS[1])), ENDS.join(" / "));
// v9 item 20: one real rate, the Trustees path's flat equivalent, for public capital at both ends.
const ONE_RATE = V9.one_rate.flat_real_equivalent;
gate("public capital earns one rate at both ends (item 20, the Trustees path's flat equivalent)",
  ONE_RATE > 0.02 && ONE_RATE < 0.022 && V9.selected_items.includes("one_rate"), (100 * ONE_RATE).toFixed(4) + "%");

/* ---------------------------------------------------------------- choices ------------------- */

// The lines each choice sets. Their parents (package PARENT) put the state-price and roads-by-miles lines
// with the line they price.
const { SYN, RENTAL, PARENT } = P;
const children = (id) => Object.keys(PARENT).filter((k) => PARENT[k] === id);
const SERVICE_GROUPS = {
  police: ["public_order_safety"], health: ["health_services"], welfare: ["income_security_services", "housing_community_services"],
};
for (const g of Object.keys(SERVICE_GROUPS)) SERVICE_GROUPS[g] = SERVICE_GROUPS[g].flatMap((id) => [id].concat(children(id)));
const SERVICES = Object.values(SERVICE_GROUPS).flat();
const ROADS = ["economic_affairs_services"].concat(children("economic_affairs_services"));
const PARKS = ["recreation_culture"].concat(children("recreation_culture"));
const PROPERTY = ["receipt:modeled_owner_property", "receipt:tenant_occupied_property", "receipt:personal_property_tax"];
const ENTERPRISE = [P.ENTERPRISE_RECEIPT].concat(P.ENTERPRISE_SPLITS.map((id) => "receipt:" + id));
// v7 item 6: the source taxes on the business capital that serves the group's jobs.
const JOBCAP = ["receipt:corporate_capital", "receipt:corporate_labor", "receipt:remaining_production_property", "receipt:other_production_taxes"];
// Union-completion carriers (v8 item 10): a line carrier follows its parent line's key and response inside the
// engine; an endpoint carrier selects its reading and is set as the case sets it.
const CARRIERS = P.correctionsPayload().meta.union_completion.carriers;
const isCarrier = (id) => Object.hasOwn(CARRIERS, id);
// The union-completion capital and production carriers: the completed reporters' return on public capital and
// production term, set by the capital and production choices at the case's endpoint responses.
const CAPITAL_CARRIERS = Object.keys(CARRIERS).filter((id) => CARRIERS[id].kind === "capital");
const PRODUCTION_CARRIERS = Object.keys(CARRIERS).filter((id) => CARRIERS[id].kind === "production");
{
  const serviceLines = model.spending.lines.filter((l) => l.response_class === "service" && !isCarrier(l.id)).map((l) => l.id).sort();
  const set = ["education_services"].concat(SERVICES, ROADS, PARKS).sort();
  gate("every service line other than the union-completion carriers is set by one choice (schools and colleges, the services, roads, parks)",
    JSON.stringify(serviceLines) === JSON.stringify(set) && new Set(set).size === set.length, serviceLines.length + " lines");
  gate("roads and parks are the case's long-run lines with the lines that follow them",
    JSON.stringify(P.LR_LINES.slice().sort()) === JSON.stringify(["economic_affairs_services", "recreation_culture"])
    && JSON.stringify(P.FOLLOW_LR.slice().sort()) === JSON.stringify(ROADS.concat(PARKS).filter((id) => !P.LR_LINES.includes(id)).sort()));
  const receipts = SPECS.flatMap((s) => Object.keys(s.line_responses).filter((k) => k.startsWith("receipt:")));
  const RECEIPT_SET = PROPERTY.concat(ENTERPRISE, JOBCAP);
  gate("the case's receipt responses are the property taxes', the enterprises' and item 6's job-capital taxes'",
    JSON.stringify([...new Set(receipts)].sort()) === JSON.stringify(RECEIPT_SET.sort()), [...new Set(receipts)].join(" "));
  const spending = SPECS.flatMap((s) => Object.keys(s.line_responses).filter((k) => !k.startsWith("receipt:") && !isCarrier(k)));
  gate("the case's other spending responses are roads, parks, the priced services and rental assistance",
    [...new Set(spending)].every((id) => ROADS.concat(PARKS, SERVICES, [RENTAL]).includes(id)), [...new Set(spending)].join(" "));
}

/* One evaluation of specification i under choice c. A choice sets:
 *   schools: "cbo" (CBO's 63% or 66%), 0 or 1; colleges: 0 or 1 (public colleges, fees and Pell);
 *   police, health, welfare: 0 or 1 (police, courts and prisons; public health; welfare administration,
 *     housing and community; each with its state prices);
 *   roads, parks: "fixed", "long_run" (the case's) or "full";
 *   gg: general administration's response, or "case";
 *   property: the long-run property-tax responses of the case, or none;
 *   constants: care work, foster care, shelter and the audited rows (the case counts them in full), or none;
 *   rental: rental assistance at 1, or 0;
 *   enterprise: the enterprises' surpluses at option D's 1, or 0;
 *   capital: false (no return on public capital) or "D" (the return with the enterprises' capital);
 *   production: the gain from their work counted, or not;
 *   jobcap: item 6's taxes on the business capital their jobs use, at the case's responses, or none;
 *   fixed: the case's fixed post-engine costs counted (see FIXED_POST), or not;
 *   uc, justice (optional): the uncompensated-care and justice keys in place of the specification's.
 * The military, administration and college items and the union-completion carriers stay as the case sets them;
 * their post-engine amounts follow the lines and responses they price. Item 21 follows the health choice. */
const NONE = { schools: 0, colleges: 0, police: 0, health: 0, welfare: 0, roads: "fixed", parks: "fixed", gg: 0,
  property: false, constants: false, rental: false, enterprise: false, capital: false, production: false, jobcap: false, fixed: false };
const CASE_CHOICE = { schools: 1, colleges: 1, police: 1, health: 1, welfare: 1, roads: "long_run", parks: "long_run",
  gg: "case", property: true, constants: true, rental: true, enterprise: true, capital: "D", production: true, jobcap: true, fixed: true };
function specAt(i, c) {
  const s = SPECS[i];
  const longRun = [c.roads, c.parks].map((x) => x === "long_run");
  // The long-run variant charges the capital of roads and parks at their subfunctions' long-run responses, on
  // whichever of the two lines sits at its long-run response; it cannot tell a fixed line from a long-run one.
  if (c.capital && longRun[0] !== longRun[1]) throw new Error("with the capital return on, roads and parks take the long-run response together");
  const schools = c.schools === "cbo" ? CBO_SCHOOL[i] : c.schools;
  const lr = Object.assign({}, s.line_responses, {
    education_services: s.share * schools + (1 - s.share) * c.colleges,
    [SYN.school]: s.share * schools, [SYN.college]: (1 - s.share) * c.colleges,
    [SYN.constants]: c.constants ? 1 : 0, [RENTAL]: c.rental ? 1 : 0,
  });
  for (const [g, ids] of Object.entries(SERVICE_GROUPS)) for (const id of ids) lr[id] = c[g];
  const roadsOrParks = (ids, x) => { for (const id of ids) lr[id] = x === "long_run" ? s.line_responses[id] : x === "full" ? 1 : 0; };
  roadsOrParks(ROADS, c.roads);
  roadsOrParks(PARKS, c.parks);
  for (const id of PROPERTY) lr[id] = c.property ? s.line_responses[id] : 0;
  for (const id of ENTERPRISE) lr[id] = c.enterprise ? s.line_responses[id] : 0;
  for (const id of JOBCAP) lr[id] = c.jobcap ? s.line_responses[id] : 0;
  for (const id of CAPITAL_CARRIERS) lr[id] = c.capital ? s.line_responses[id] : 0;
  for (const id of PRODUCTION_CARRIERS) lr[id] = c.production ? s.line_responses[id] : 0;
  return Object.assign({}, s, {
    line_responses: lr,
    gg: c.gg === "case" ? s.gg : c.gg,
    rate: c.capital ? s.rate : 0,
    enterprises: "D",
    long_run: longRun[0] || longRun[1] ? s.long_run : null,
    uc: c.uc || s.uc,
    justice: c.justice || s.justice,
  });
}
/* The case's full evaluation (package evaluateFull) is v8's full evaluation plus v9's post-engine additions,
 * priced on that run. v9's military item reads a specification without a long-run variant as the first year
 * (no replacement veterans yet); here roads and parks fixed or in full are a steady-state choice, so its
 * additions are priced on the specification's own long-run variant while the engine and capital run without it,
 * as the case's sign_reversal.cjs does. */
/* Two v9 items price lines a choice can freeze with amounts the package holds at the case's response: item 21
 * re-keys the health-services residual, its state prices and its capital, at the health response 1, whatever the
 * evaluation; item 15's college operating and capital response leaves a fee-offset remainder when colleges are
 * fixed. A choice that freezes public health or the colleges freezes its item with it. */
const SCALED_ITEMS = { health_residual_key: "health", public_college_response: "colleges" };
function evaluate(i, c, raw = false) {
  const spec = specAt(i, c);
  let r;
  if (spec.long_run === SPECS[i].long_run) r = P.evaluateFull(model, spec, PROFILE);
  else {
    const r0 = P.V9_BASE.evaluateFull(model, spec, PROFILE);
    const d = P.postFor(model, Object.assign({}, spec, { long_run: SPECS[i].long_run }), PROFILE, r0);
    r = { ...r0, cost_bn: r0.cost_bn + d.total_bn, v9_post_engine: d, post_engine: { ...r0.post_engine,
      ...Object.fromEntries(Object.entries(d.amounts).map(([k, v]) => [k + "_bn", v])), total_bn: (r0.post_engine?.total_bn || 0) + d.total_bn } };
  }
  for (const [item, choice] of Object.entries(SCALED_ITEMS)) {
    if (raw || c[choice] === 1) continue;
    if (c[choice] !== 0) throw new Error(`${item}: ${choice} at ${c[choice]}, neither 0 nor 1`);
    const k = item + "_bn", move = -r.post_engine[k];
    r = { ...r, cost_bn: r.cost_bn + move, post_engine: { ...r.post_engine, [k]: 0, total_bn: r.post_engine.total_bn + move } };
  }
  return r;
}
/* Post-engine costs fixed at the case's responses, whatever the choice: v8's item 11 (the non-members who stay
 * in mixed households) and item 12 (the members the Census misses), v9's repricing of item 12, and v9 items 16
 * and 17's count calibration. The payload declares no line or class split that would let them follow a choice,
 * so the staircase adds them as one row at the case's responses, and every matrix cell carries them. */
const FIXED_POST = ["mixed_unit_removal_bn", "coverage_bn", "coverage_repricing_bn", "native_minor_calibration_bn", "coverage_tenure_bn"];
const fixedPost = (r) => FIXED_POST.reduce((t, k) => t + (r.post_engine[k] || 0), 0);
// Cost to everyone else, $bn a year (positive: worse off).
function costAt(i, c, raw = false) {
  const r = evaluate(i, c, raw);
  return r.cost_bn + (c.production ? 0 : r.evaluation.production_gain_bn) - (c.fixed ? 0 : fixedPost(r));
}
{
  let worst = 0;
  SPECS.forEach((s, i) => { worst = Math.max(worst, Math.abs(costAt(i, CASE_CHOICE) - caseCosts[i])); });
  gate("the case's choices are the case at every specification (1e-9)", worst < 1e-9, `max |diff| ${worst.toExponential(1)}`);
  // The fixed costs are fixed: the same at every choice the page runs, specification by specification.
  let drift = 0;
  const probes = [NONE, { ...CASE_CHOICE, roads: "fixed", parks: "fixed", capital: false }, { ...CASE_CHOICE, roads: "full", parks: "full", capital: false },
    { ...CASE_CHOICE, schools: "cbo", colleges: 0, gg: 1 }];
  SPECS.forEach((s, i) => {
    const want = fixedPost(evaluate(i, CASE_CHOICE));
    for (const c of probes) drift = Math.max(drift, Math.abs(fixedPost(evaluate(i, c)) - want));
  });
  gate("the fixed post-engine costs do not move with any choice (1e-9)", drift < 1e-9, drift.toExponential(1));
  // Each scaled item prices only lines its choice sets, at the case's response 1.
  const parts = evaluate(ENDS[0], CASE_CHOICE).v9_post_engine.parts;
  const lines = (item) => [...new Set(parts[item].map((p) => (isCarrier(p.line) ? CARRIERS[p.line].parent_line : p.source_line)))].sort();
  gate("item 21 prices the health-services residual, its state prices and its capital; item 15 the colleges, their fees and capital",
    JSON.stringify(lines("health_residual_key")) === JSON.stringify(["health_services", "health_sl", "state_price_health_services"])
    && JSON.stringify(lines("public_college_response")) === JSON.stringify(["college", "college_user_fees", "education_services"])
    && SERVICE_GROUPS.health.includes("health_services") && SERVICE_GROUPS.health.includes("state_price_health_services")
    && SPECS.every((s) => [undefined, 1].includes(s.line_responses.health_services) && s.school === 1),
    `${lines("health_residual_key").join(" ")}; ${lines("public_college_response").join(" ")}`);
}

/* The receipts under another of the executed tax-incidence rules: the package evaluates the reference rule
 * (CBO's), and its payload carries every receipt edit to all eight, so the rule is set where the engine runs.
 * The fixed post-engine costs stay at the reference rule. */
const RECEIPTS = model.receipts.scenarios;
function withReceipts(scenario, f) {
  if (!RECEIPTS.includes(scenario)) throw new Error("no receipt scenario " + scenario);
  const evaluate0 = Engine.evaluate;
  Engine.evaluate = (m, st) => evaluate0(m, Object.assign({}, st, { receipt_scenario: scenario }));
  try { return f(); } finally { Engine.evaluate = evaluate0; }
}
// Each rule's move of the case. Rules that reallocate only receipts the case holds at response 0 move nothing.
const RECEIPT_MOVES = Object.fromEntries(RECEIPTS.map((sc) => {
  const c = withReceipts(sc, () => SPECS.map((s, i) => costAt(i, CASE_CHOICE)));
  return [sc, span(c.map((x, i) => x - caseCosts[i]))];
}));
gate("the incidence rule reaches the evaluation: the reference rule moves nothing, another rule moves every specification",
  RECEIPT_MOVES[model.receipts.reference].every((x) => x === 0)
  && RECEIPTS.some((sc) => RECEIPT_MOVES[sc][0] > 1e-6 || RECEIPT_MOVES[sc][1] < -1e-6),
  RECEIPTS.map((sc) => `${sc} ${RECEIPT_MOVES[sc].map((x) => x.toFixed(2)).join("/")}`).join("; "));

/* The production grid with private capital adjusted and no capital owners excluded, on the case's grid (the
 * payload's, on the account's row-4 weights): the matrix's outer range. */
const PROD_DIMS = Engine.PRODUCTION_DIMS;
function decode(index) {
  const out = {};
  for (let k = PROD_DIMS.length - 1; k >= 0; k--) {
    const levels = model.production.dims[PROD_DIMS[k]];
    out[PROD_DIMS[k]] = levels[index % levels.length];
    index = Math.floor(index / levels.length);
  }
  return out;
}
const saneProduction = [];
for (let i = 0; i < model.production.private_wtp_bn.length; i++) {
  const d = decode(i);
  if (Engine.productionIndex(model, d) !== i) throw new Error("production index decode mismatch at " + i);
  if (d.capital_adjustment === 1 && d.excluded_capital_owner_share === 0) {
    saneProduction.push(model.production.private_wtp_bn[i] + model.production.induced_receipts_bn[i]);
  }
}
const PROD_SPAN = span(saneProduction);
const JUSTICE_KEYS = Object.keys(model.spending.lines.find((l) => l.id === "public_order_safety").keys);
const UC_KEYS = Object.keys(model.spending.lines.find((l) => l.id === "medicaid_and_chip_other_medical").keys)
  .filter((k) => k === "medicaid" || k.startsWith("uninsured_use"));

/* The sign-reversal definition (main_case_2026_09_24/sign_reversal.cjs) inside the case, as
 * main_case_2026_10_16/sign_reversal.cjs runs it (its withCase, copied): rental assistance at 1, the
 * enterprise receipts at option D's 1 or at s, every other receipt response at the case's, the union-completion
 * carriers mapped to their parents, the return on public capital from the same evaluation, and the case's
 * post-engine costs, item 11 and coverage fixed, the rest priced on the run. */
const S24 = require(path.join(FISCAL, "main_case_2026_09_24", "sign_reversal.cjs"));
const GG9 = P.RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG9.low : GG9.high }));
let lastSign = null;
function withCase(variant, f) {
  if (!["enterprises_at_1", "enterprises_at_s"].includes(variant)) throw new Error("unknown variant " + variant);
  const carrierEntries = Object.entries(CARRIERS);
  const fixed = Object.entries(P.LINE_RESPONSES).filter(([k]) => k.startsWith("receipt:") && !ENTERPRISE.includes(k));
  const evaluate0 = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = st.general_government_response === GG9.low ? "low" : st.general_government_response === GG9.high ? "high" : null;
    if (!reading) throw new Error(`general government at ${st.general_government_response}, neither of the case's responses`);
    const atS = variant === "enterprises_at_s";
    const extra = { [RENTAL]: 1 };
    for (const k of ENTERPRISE) extra[k] = atS ? s : 1;
    for (const [k, e] of fixed) extra[k] = e[reading];
    for (const [id, src] of carrierEntries) if (src.kind !== "line") extra[id] = src.end === reading ? 1 : 0;
    let state = Object.assign({}, st, { response_override: Object.assign({}, st.response_override, extra) });
    let ev = evaluate0(m, state);
    const receiptRows = new Map(ev.receipts.map((row) => [row.id, row]));
    const spendingRows = new Map(ev.spending.map((row) => [row.id, row]));
    for (const [id, src] of carrierEntries) if (src.kind === "line") {
      const parent = (src.side === "receipt" ? receiptRows : spendingRows).get(src.parent_line);
      if (!parent) throw new Error(`missing carrier parent ${src.parent_line}`);
      const key = src.side === "receipt" ? state.receipt_scenario : parent.key;
      extra[id] = key === src.parent_key ? parent.response : 0;
    }
    if (carrierEntries.length) {
      state = Object.assign({}, st, { response_override: Object.assign({}, st.response_override, extra) });
      ev = evaluate0(m, state);
    }
    const cap = P.capitalReturn(ev, { share: st.school_share, reading, rate: P.RATES[reading], enterprises: P.ENTERPRISES, long_run: null });
    const ent = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * ent : 0);
    const spec = { allocation: st.allocation, reading, share: st.school_share, school: st.service_response, gg: st.general_government_response,
      uc: st.uncompensated_care_response, rate: P.RATES[reading], enterprises: P.ENTERPRISES, long_run: true };
    const adjusted = atS ? { ...cap, total_bn: capital, components: cap.components.map((c) => (c.group === "enterprise" ? { ...c, return_bn: c.return_bn * s } : c)) } : cap;
    const post = P.OCT15.postEngine(spec) + P.postFor(m, spec, undefined, { evaluation: ev, capital: adjusted }).total_bn;
    lastSign = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital - post, capital_return_bn: capital, post_engine_bn: post });
    return lastSign;
  };
  try { return f(); } finally { Engine.evaluate = evaluate0; }
}

module.exports = {
  fs, path, HERE, FISCAL, REPO, CASE_LANE, CASE_KEY, CASE, PINS, PAYLOAD, readText, readJson, readCsv, inputs, P, Engine, model,
  SPECS, PROFILE, CBO_SCHOOL, SUMMARY, V9, MAIN, CASH, COMPANIONS, ONE_RATE, GG, ENDS, NONE, CASE_CHOICE, specAt, evaluate, costAt,
  FIXED_POST, fixedPost, SCALED_ITEMS, RECEIPTS, RECEIPT_MOVES, withReceipts, PROD_SPAN, saneProduction, JUSTICE_KEYS, UC_KEYS, S24, PAIRS, withCase,
  CARRIERS, CAPITAL_CARRIERS, PRODUCTION_CARRIERS, gate, failures, near, round, span, product,
};
