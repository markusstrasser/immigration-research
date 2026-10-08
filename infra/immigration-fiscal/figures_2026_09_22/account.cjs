/* The complete account as the figures page evaluates it: main case v6 (adopted 2026-10-07,
 * decisions/2026-10-07-main-case-v6.md) through its package, main_case_2026_10_07/package.cjs, on the
 * case's payload model. Each staircase step and matrix cell is one evaluateFull per specification: a copy
 * of the case's specification with that step's or cell's responses, so the engine, the case's added lines
 * and its return on public capital run as the case runs them. The gates compare against the case's own
 * files. build_data.cjs loads it; the prototypes page stays on the September 24 case (account_sept24.cjs).
 */
"use strict";
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

const HERE = __dirname;
const FISCAL = path.join(HERE, "..");
const REPO = path.join(HERE, "..", "..", "..");
const CASE_LANE = "main_case_2026_10_07";
const CASE = path.join(FISCAL, CASE_LANE);
/* The research lanes move with each main case; the page moves when the operator asks (2026-10-08: to main
 * case v6). Lane files are read as they stood on v6, at a commit (git show), so a lane's next case cannot
 * reach the page unasked. The case's payload, which its package reads from the working tree, is pinned by
 * hash. */
const PINS = {
  distribution: "498a6a71", // the who-pays lane on main case v6 (derived/oct07/)
  backcast: "55a8fff7",     // the back-cast of main case v6 (derived/oct07/), with per-lineage-member columns
};
const PAYLOAD = {           // main_case_2026_10_07/derived/ as main_case.cjs wrote v6
  "corrections.json": "f8d346aacf05bcdaed8495f870ba23ac6154ab3eaf34cc0bcf85861f0c85d091",
  "corrections_cash.json": "e9033bfff737299e76d09b0c600e8f42c6b6110713f402fb293a6324b2721e80",
  "summary.json": "547092591e23ebd69e7dfaec28e6eebe441c7cc61a9f3d32f328a3991f321bf3",
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

console.log("\n[main case v6]");
for (const [name, want] of Object.entries(PAYLOAD)) {
  const got = sha256(readText(path.join(CASE, "derived", name)));
  gate(`${CASE_LANE}/derived/${name} is v6's payload`, got === want, got.slice(0, 8));
}
const P = require(path.join(CASE, "package.cjs"));
const { Engine } = P;
gate("one engine: the package's and its September 24 base's", P.P24.Engine === Engine);
const model = P.payloadModel();
const SPECS = P.MAIN_SPECS;
const PROFILE = P.MAIN_PROFILE;
// CBO's school response (63% or 66%), the September 24 case's at the same specification: the matrix's other
// school row. v6 charges schools at their full cost at every specification.
const CBO_SCHOOL = P.P24.MAIN_SPECS.map((s) => s.school);
gate("the September 24 specifications line up with v6's on allocation, normalization, share and keys",
  P.P24.MAIN_SPECS.length === SPECS.length && SPECS.every((s, i) => s.school === 1
    && ["allocation", "normalization", "share", "uc", "justice"].every((k) => s[k] === P.P24.MAIN_SPECS[i][k]))
  && JSON.stringify([...new Set(CBO_SCHOOL)].sort()) === "[0.63,0.66]", `${SPECS.length} specifications`);

const SUMMARY = readJson(path.join(CASE, "derived", "summary.json"));
const MAIN = SUMMARY.main_case;
const CASH = SUMMARY.cash_set.band_bn;
const bands = readCsv(path.join(CASE, "derived", "main_case_bands.csv"));
const band = (profile, variant) => {
  const row = bands.find((b) => b.profile === profile && b.variant === variant);
  if (!row) throw new Error(`no band ${profile} / ${variant}`);
  return [Number(row.cost_low_bn), Number(row.cost_high_bn)];
};
gate("main_case_bands.csv's adopted and cash rows are summary.json's (4 decimals)",
  band(PROFILE, "adopted").every((x, j) => near(x, MAIN[j], 5e-5)) && band(PROFILE, "cash_set").every((x, j) => near(x, CASH[j], 5e-5)),
  `${MAIN.map((x) => x.toFixed(6)).join("–")}; cash ${CASH.map((x) => x.toFixed(6)).join("–")}`);
// Bands on the case's other profiles and variants (4 decimals); the case without its capital return at full
// precision from summary.json.
const BANDS = {
  fixedColleges: band("long_run_non_school_fixed", "adopted"),
  proportional: band("proportional_reference", "adopted"),
  withoutCapital: SUMMARY.without_capital_return,
  ggFixed: band(PROFILE, "general_government_fixed"),
  // The September 24 profile on v6: roads and parks fixed, everything else the case's.
  roadsFixed: band("cbo_category_lag_non_school_full", "with_rental_assistance_capital_and_enterprises"),
};
const caseCosts = SPECS.map((s) => P.cost(model, s, PROFILE));
gate("the payload model reproduces the case (summary.json, 1e-9)",
  near(Math.min(...caseCosts), MAIN[0], 1e-9) && near(Math.max(...caseCosts), MAIN[1], 1e-9),
  `${Math.min(...caseCosts).toFixed(6)}–${Math.max(...caseCosts).toFixed(6)}`);
const GG = [P.RESPONSES.general_government.low, P.RESPONSES.general_government.high];
// The band's ends: its low and high specification, the first of each pair the September 24 school response splits.
const ENDS = [caseCosts.indexOf(Math.min(...caseCosts)), caseCosts.indexOf(Math.max(...caseCosts))];
gate("the band's ends are summary.json's end specifications, in both methods",
  SUMMARY.end_specifications.every((e) => e.low_end.index === ENDS[0] && e.high_end.index === ENDS[1]), ENDS.join(" / "));

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
{
  const serviceLines = model.spending.lines.filter((l) => l.response_class === "service").map((l) => l.id).sort();
  const set = ["education_services"].concat(SERVICES, ROADS, PARKS).sort();
  gate("every service line is set by one choice (schools and colleges, the services, roads, parks)",
    JSON.stringify(serviceLines) === JSON.stringify(set) && new Set(set).size === set.length, serviceLines.length + " lines");
  gate("roads and parks are the case's long-run lines with the lines that follow them",
    JSON.stringify(P.LR_LINES.slice().sort()) === JSON.stringify(["economic_affairs_services", "recreation_culture"])
    && JSON.stringify(P.FOLLOW_LR.slice().sort()) === JSON.stringify(ROADS.concat(PARKS).filter((id) => !P.LR_LINES.includes(id)).sort()));
  const receipts = SPECS.flatMap((s) => Object.keys(s.line_responses).filter((k) => k.startsWith("receipt:")));
  gate("the case's receipt responses are the property taxes' and the enterprises' alone",
    JSON.stringify([...new Set(receipts)].sort()) === JSON.stringify(PROPERTY.concat(ENTERPRISE).sort()), [...new Set(receipts)].join(" "));
  const spending = SPECS.flatMap((s) => Object.keys(s.line_responses).filter((k) => !k.startsWith("receipt:")));
  gate("the case's spending responses are roads, parks, the priced services and rental assistance",
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
 *   capital: false (no return on public capital), "A" (the return without the enterprises' capital) or "D";
 *   production: the gain from their work counted, or not;
 *   uc, justice (optional): the uncompensated-care and justice keys in place of the specification's. */
const NONE = { schools: 0, colleges: 0, police: 0, health: 0, welfare: 0, roads: "fixed", parks: "fixed", gg: 0,
  property: false, constants: false, rental: false, enterprise: false, capital: false, production: false };
const CASE_CHOICE = { schools: 1, colleges: 1, police: 1, health: 1, welfare: 1, roads: "long_run", parks: "long_run",
  gg: "case", property: true, constants: true, rental: true, enterprise: true, capital: "D", production: true };
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
  return Object.assign({}, s, {
    line_responses: lr,
    gg: c.gg === "case" ? s.gg : c.gg,
    rate: c.capital ? s.rate : 0,
    enterprises: c.capital === "D" ? "D" : "A",
    long_run: longRun[0] || longRun[1] ? s.long_run : null,
    uc: c.uc || s.uc,
    justice: c.justice || s.justice,
  });
}
function evaluate(i, c) {
  return P.evaluateFull(model, specAt(i, c), PROFILE);
}
// Cost to everyone else, $bn a year (positive: worse off).
function costAt(i, c) {
  const r = evaluate(i, c);
  return r.cost_bn + (c.production ? 0 : r.evaluation.production_gain_bn);
}
{
  let worst = 0;
  SPECS.forEach((s, i) => { worst = Math.max(worst, Math.abs(costAt(i, CASE_CHOICE) - caseCosts[i])); });
  gate("the case's choices are the case at every specification (1e-9)", worst < 1e-9, `max |diff| ${worst.toExponential(1)}`);
}

/* The receipts under another of the executed tax-incidence rules: the package evaluates the reference rule
 * (CBO's), and its payload carries every receipt edit to all eight, so the rule is set where the engine runs. */
const RECEIPTS = model.receipts.scenarios;
function withReceipts(scenario, f) {
  if (!RECEIPTS.includes(scenario)) throw new Error("no receipt scenario " + scenario);
  const evaluate0 = Engine.evaluate;
  Engine.evaluate = (m, st) => evaluate0(m, Object.assign({}, st, { receipt_scenario: scenario }));
  try { return f(); } finally { Engine.evaluate = evaluate0; }
}
// Each rule's move of the case. Rules that reallocate only receipts the case holds at response 0 (corporate
// taxes, production taxes, the government's asset income) move nothing.
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
 * main_case_2026_10_07/sign_reversal.cjs runs it (its withCase, copied): rental assistance at 1, the
 * enterprise receipts at option D's 1 or at s, every other receipt response at the case's, and the return
 * on public capital from the same evaluation. */
const S24 = require(path.join(FISCAL, "main_case_2026_09_24", "sign_reversal.cjs"));
const GG6 = P.RESPONSES.general_government;
const PAIRS = S24.PAIRS.map((p) => ({ ...p, g: p.end === "least" ? GG6.low : GG6.high }));
const readingOf = (g) => (g === GG6.low ? "low" : g === GG6.high ? "high" : null);
let lastSign = null;
function withCase(variant, f) {
  if (!["enterprises_at_1", "enterprises_at_s"].includes(variant)) throw new Error("unknown variant " + variant);
  const fixed = Object.entries(P.LINE_RESPONSES).filter(([k]) => k.startsWith("receipt:") && !ENTERPRISE.includes(k));
  const evaluate0 = Engine.evaluate;
  Engine.evaluate = (m, st) => {
    const s = st.service_response;
    const reading = readingOf(st.general_government_response);
    if (!reading) throw new Error(`general government at ${st.general_government_response}, neither of the case's responses`);
    const atS = variant === "enterprises_at_s";
    const extra = { [RENTAL]: 1 };
    for (const k of ENTERPRISE) extra[k] = atS ? s : 1;
    for (const [k, e] of fixed) extra[k] = e[reading];
    const ev = evaluate0(m, Object.assign({}, st, { response_override: Object.assign({}, st.response_override, extra) }));
    const cap = P.capitalReturn(ev, { share: st.school_share, reading, rate: P.RATES[reading], enterprises: P.ENTERPRISES, long_run: null });
    const ent = cap.components.filter((c) => c.group === "enterprise").reduce((a, c) => a + c.return_bn, 0);
    const capital = cap.total_bn - (atS ? (1 - s) * ent : 0);
    lastSign = Object.assign({}, ev, { welfare_bn: ev.welfare_bn - capital, capital_return_bn: capital });
    return lastSign;
  };
  try { return f(); } finally { Engine.evaluate = evaluate0; }
}

module.exports = {
  fs, path, HERE, FISCAL, REPO, CASE_LANE, CASE, PINS, PAYLOAD, readText, readJson, readCsv, inputs, P, Engine, model,
  SPECS, PROFILE, CBO_SCHOOL, SUMMARY, MAIN, CASH, BANDS, GG, ENDS, NONE, CASE_CHOICE, specAt, evaluate, costAt,
  RECEIPTS, RECEIPT_MOVES, withReceipts, PROD_SPAN, saneProduction, JUSTICE_KEYS, UC_KEYS, S24, PAIRS, withCase,
  gate, failures, near, round, span, product,
};
