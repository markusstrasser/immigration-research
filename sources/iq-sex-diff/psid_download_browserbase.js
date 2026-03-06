/**
 * PSID CDS/TAS data downloader via Browserbase.
 *
 * Strategy: Instead of clicking links and waiting for download events
 * (which don't work well over CDP), navigate directly to each GetFile URL
 * and use the browser's fetch() to download the file content using the
 * authenticated session cookies.
 *
 * Usage: node psid_download_browserbase.js
 */

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const https = require('https');

const OUT = path.join(__dirname, 'data/psid');
const DOWNLOADS = path.join(OUT, 'downloads');

// Only the files needed for iq-sex-diff analysis
const TARGET_FILES = [
  // CDS — child cognitive assessments, demographics, behavior
  { file: 1193, label: 'CDS-1997' },
  { file: 1174, label: 'CDS-2002' },
  { file: 1170, label: 'CDS-2007' },
  { file: 1173, label: 'CDS-2014' },
  { file: 1200, label: 'CDS-2019' },
  { file: 1210, label: 'CDS-2021' },
  { file: 1204, label: 'CDS-Cumulative-ID-Map' },

  // TAS — young adult education, employment, cognitive outcomes
  { file: 1166, label: 'TAS-2005' },
  { file: 1167, label: 'TAS-2007' },
  { file: 1168, label: 'TAS-2009' },
  { file: 1169, label: 'TAS-2011' },
  { file: 1172, label: 'TAS-2013' },
  { file: 1184, label: 'TAS-2015' },
  { file: 1189, label: 'TAS-2017' },
  { file: 1196, label: 'TAS-2019' },
  { file: 1208, label: 'TAS-2021' },
  { file: 1215, label: 'TAS-2023' },

  // Cross-year individual — demographics, education, income across all waves
  { file: 1053, label: 'CrossYear-Individual-1968-2023' },

  // Childbirth & Adoption History
  { file: 1109, label: 'Childbirth-Adoption-1985-2023' },

  // Parent Identification
  { file: 1123, label: 'Parent-ID-2023' },
];

// Load .env.local
const envPath = path.join(__dirname, '../../.env.local');
if (fs.existsSync(envPath)) {
  for (const line of fs.readFileSync(envPath, 'utf8').split('\n')) {
    const m = line.match(/^([^#=]+)=(.*)$/);
    if (m && !process.env[m[1].trim()]) process.env[m[1].trim()] = m[2].trim();
  }
}

const BB_KEY = process.env.BROWSERBASE_API_KEY;
const BB_PROJECT = process.env.BROWSERBASE_PROJECT_ID;
const PSID_USER = process.env.PSID_USER;
const PSID_PASS = process.env.PSID_PASS;

for (const [k, v] of [['BROWSERBASE_API_KEY', BB_KEY], ['BROWSERBASE_PROJECT_ID', BB_PROJECT], ['PSID_USER', PSID_USER], ['PSID_PASS', PSID_PASS]]) {
  if (!v) { console.error(`Missing ${k}`); process.exit(1); }
}

async function createSession() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ projectId: BB_PROJECT });
    const req = https.request({
      hostname: 'api.browserbase.com',
      path: '/v1/sessions',
      method: 'POST',
      headers: { 'x-bb-api-key': BB_KEY, 'Content-Type': 'application/json' },
    }, (res) => {
      let body = '';
      res.on('data', d => body += d);
      res.on('end', () => {
        if (res.statusCode >= 300) return reject(new Error(`${res.statusCode}: ${body}`));
        resolve(JSON.parse(body));
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function main() {
  fs.mkdirSync(DOWNLOADS, { recursive: true });

  const existing = new Set(fs.readdirSync(DOWNLOADS));
  console.log(`Already have ${existing.size} files in downloads/`);

  // Create Browserbase session
  console.log('Creating Browserbase session...');
  const session = await createSession();
  console.log(`Session: ${session.id}`);

  const wsUrl = `wss://connect.browserbase.com?apiKey=${BB_KEY}&sessionId=${session.id}`;
  console.log('Connecting to cloud browser...');
  const browser = await chromium.connectOverCDP(wsUrl);
  const context = browser.contexts()[0];
  let page = context.pages()[0] || await context.newPage();

  // Login
  console.log('Logging in...');
  await page.goto('https://simba.isr.umich.edu/U/Login.aspx', {
    waitUntil: 'domcontentloaded', timeout: 60000,
  });
  await page.waitForTimeout(5000);

  const userField = await page.$('#txtUserName, input[name*="UserName"], input[name*="Email"]');
  const passField = await page.$('#txtPassword, input[type="password"]');

  if (userField && passField) {
    await userField.fill(PSID_USER);
    await passField.fill(PSID_PASS);
    const submit = await page.$('#btnSubmit, input[type="submit"], button[type="submit"]');
    if (submit) {
      await submit.click();
      await page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }).catch(() => {});
      await page.waitForTimeout(3000);
    }
    console.log(`Logged in: ${await page.title()}`);
  } else {
    console.log('No login form found');
  }

  // Verify auth by hitting a known page
  const content = await page.content();
  const isLoggedIn = content.includes('Logout') || content.includes('Log Out') || content.includes('Welcome');
  if (!isLoggedIn) {
    console.error('Login may have failed — no auth indicators found');
    await page.screenshot({ path: path.join(OUT, 'bb_login_debug.png') });
  }

  // Download each file by navigating to the GetFile URL directly
  // The browser session is authenticated, so the server will serve the file
  let downloaded = 0, skipped = 0, failed = 0;

  for (let i = 0; i < TARGET_FILES.length; i++) {
    const { file, label } = TARGET_FILES[i];
    const progress = `[${i + 1}/${TARGET_FILES.length}]`;

    // Check if we already have this file
    const alreadyHave = [...existing].some(f =>
      f.toLowerCase().includes(label.toLowerCase().replace(/-/g, ''))
      || f.includes(`${file}`)
    );
    if (alreadyHave) {
      console.log(`${progress} ${label} — skip (exists)`);
      skipped++;
      continue;
    }

    console.log(`${progress} ${label} (file=${file})...`);

    try {
      const fileUrl = `https://simba.isr.umich.edu/Zips/GetFileCDS.aspx?file=${file}&mainurl=Y`;

      // Navigate to the file URL — this may either:
      // 1. Trigger a download (Content-Disposition: attachment)
      // 2. Show an intermediate page with a download link
      // 3. Show a format selection page

      // Use route interception to capture the download
      let downloadData = null;
      let downloadFilename = null;

      // Set up response interception for the file download
      const responsePromise = new Promise((resolve) => {
        page.on('response', async (response) => {
          const url = response.url();
          if (!url.includes('GetFile') && !url.includes('.zip') && !url.includes('.exe')) return;

          const headers = response.headers();
          const disposition = headers['content-disposition'] || '';
          if (disposition.includes('attachment') || headers['content-type']?.includes('application/')) {
            try {
              const body = await response.body();
              const filenameMatch = disposition.match(/filename[*]?=(?:UTF-8'')?["']?([^"';\n]+)/i);
              downloadFilename = filenameMatch ? filenameMatch[1] : `psid_${file}.zip`;
              downloadData = body;
              resolve(true);
            } catch (e) {
              // Response body may not be available
            }
          }
        });

        // Timeout after 60s
        setTimeout(() => resolve(false), 60000);
      });

      await page.goto(fileUrl, {
        waitUntil: 'domcontentloaded',
        timeout: 60000,
      });

      // Check if we landed on an intermediate page
      await page.waitForTimeout(3000);
      const pageTitle = await page.title();
      const pageUrl = page.url();

      // If it's an intermediate page, look for the actual download link or button
      if (pageUrl.includes('GetFile') && !downloadData) {
        // Try to find and click a download button/link on the intermediate page
        const downloadBtn = await page.$('a[href*=".zip"], a[href*="download"], input[value*="Download"], button:has-text("Download")');
        if (downloadBtn) {
          console.log(`  Intermediate page — clicking download button...`);
          await downloadBtn.click();
          await page.waitForTimeout(5000);
        }
      }

      // Wait for intercepted download
      const gotDownload = await responsePromise;

      if (gotDownload && downloadData) {
        const savePath = path.join(DOWNLOADS, downloadFilename);
        fs.writeFileSync(savePath, downloadData);
        const size = fs.statSync(savePath).size;
        console.log(`  ${downloadFilename} (${(size / 1024 / 1024).toFixed(1)} MB)`);
        downloaded++;
        existing.add(downloadFilename);
      } else {
        // Fallback: use fetch() in the browser context to download
        console.log(`  No intercepted download — trying fetch()...`);
        try {
          const result = await page.evaluate(async (url) => {
            const resp = await fetch(url, { credentials: 'include' });
            if (!resp.ok) return { error: `HTTP ${resp.status}` };
            const ct = resp.headers.get('content-type') || '';
            const cd = resp.headers.get('content-disposition') || '';
            const buf = await resp.arrayBuffer();
            return {
              data: Array.from(new Uint8Array(buf)),
              contentType: ct,
              disposition: cd,
              size: buf.byteLength,
            };
          }, fileUrl);

          if (result.error) throw new Error(result.error);

          const filenameMatch = result.disposition.match(/filename[*]?=(?:UTF-8'')?["']?([^"';\n]+)/i);
          const filename = filenameMatch ? filenameMatch[1] : `psid_${label}.zip`;
          const savePath = path.join(DOWNLOADS, filename);
          fs.writeFileSync(savePath, Buffer.from(result.data));
          console.log(`  ${filename} (${(result.size / 1024 / 1024).toFixed(1)} MB)`);
          downloaded++;
          existing.add(filename);
        } catch (fetchErr) {
          throw new Error(`fetch fallback: ${fetchErr.message}`);
        }
      }

      // Small delay between downloads
      await page.waitForTimeout(1000);

    } catch (e) {
      console.log(`  FAILED: ${e.message.slice(0, 150)}`);
      failed++;
      // Try to recover navigation
      try {
        await page.goto('https://simba.isr.umich.edu/Zips/ZipMain.aspx', {
          waitUntil: 'domcontentloaded', timeout: 30000,
        });
        await page.waitForTimeout(2000);
      } catch (e2) {
        console.log(`  Recovery failed — session may be dead`);
        break;
      }
    }
  }

  await browser.close();

  console.log(`\n${'='.repeat(50)}`);
  console.log(`Downloaded: ${downloaded} | Skipped: ${skipped} | Failed: ${failed}`);
  console.log(`${'='.repeat(50)}\n`);

  const allFiles = fs.readdirSync(DOWNLOADS).sort();
  let totalSize = 0;
  for (const f of allFiles) totalSize += fs.statSync(path.join(DOWNLOADS, f)).size;
  console.log(`Total: ${allFiles.length} files, ${(totalSize / 1024 / 1024).toFixed(0)} MB`);
}

main().catch(e => { console.error(e); process.exit(1); });
