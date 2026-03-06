/**
 * Fetch a single PSID file via Browserbase.
 * Usage: node psid_fetch_one.js <fileId> [label]
 */
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');

const DOWNLOADS = path.join(__dirname, 'data/psid/downloads');
fs.mkdirSync(DOWNLOADS, { recursive: true });

const fileId = process.argv[2] || '1053';
const label = process.argv[3] || `psid_${fileId}`;

// Load .env.local
const envPath = path.join(__dirname, '../../.env.local');
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const m = line.match(/^([^#=]+)=(.*)$/);
    if (m && !process.env[m[1].trim()]) process.env[m[1].trim()] = m[2].trim();
  }
}

async function createSession() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ projectId: process.env.BROWSERBASE_PROJECT_ID });
    const req = https.request({
      hostname: 'api.browserbase.com', path: '/v1/sessions', method: 'POST',
      headers: { 'x-bb-api-key': process.env.BROWSERBASE_API_KEY, 'Content-Type': 'application/json' },
    }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => res.statusCode >= 300 ? reject(new Error(body)) : resolve(JSON.parse(body)));
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

(async () => {
  console.log(`Fetching file=${fileId} (${label})...`);
  const session = await createSession();
  console.log(`Session: ${session.id}`);

  const browser = await chromium.connectOverCDP(
    `wss://connect.browserbase.com?apiKey=${process.env.BROWSERBASE_API_KEY}&sessionId=${session.id}`
  );
  const page = browser.contexts()[0].pages()[0] || await browser.contexts()[0].newPage();

  // Login
  await page.goto('https://simba.isr.umich.edu/U/Login.aspx', { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(5000);
  const userField = await page.$('#txtUserName, input[name*="UserName"]');
  const passField = await page.$('#txtPassword, input[type="password"]');
  if (userField && passField) {
    await userField.fill(process.env.PSID_USER);
    await passField.fill(process.env.PSID_PASS);
    const btn = await page.$('#btnSubmit, input[type="submit"]');
    if (btn) { await btn.click(); await page.waitForNavigation({ timeout: 30000 }).catch(() => {}); }
    await page.waitForTimeout(3000);
  }
  console.log(`Logged in: ${await page.title()}`);

  // Fetch the file
  const url = `https://simba.isr.umich.edu/Zips/GetFileCDS.aspx?file=${fileId}&mainurl=Y`;
  console.log(`Fetching ${url}...`);

  const result = await page.evaluate(async (fetchUrl) => {
    const resp = await fetch(fetchUrl, { credentials: 'include' });
    if (!resp.ok) return { error: `HTTP ${resp.status}` };
    const cd = resp.headers.get('content-disposition') || '';
    const ct = resp.headers.get('content-type') || '';
    const buf = await resp.arrayBuffer();
    return { data: Array.from(new Uint8Array(buf)), disposition: cd, contentType: ct, size: buf.byteLength };
  }, url);

  if (result.error) {
    console.error('FAILED:', result.error);
    process.exit(1);
  }

  const m = result.disposition.match(/filename[*]?=(?:UTF-8'')?["']?([^"';\n]+)/i);
  const filename = m ? m[1] : `${label}.zip`;
  const savePath = path.join(DOWNLOADS, filename);
  fs.writeFileSync(savePath, Buffer.from(result.data));
  console.log(`Saved: ${filename} (${(result.size / 1024 / 1024).toFixed(1)} MB)`);
  console.log(`Content-Type: ${result.contentType}`);

  await browser.close();
  console.log('Done.');
})().catch(e => { console.error(e); process.exit(1); });
