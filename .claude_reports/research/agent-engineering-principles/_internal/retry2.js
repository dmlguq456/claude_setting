const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = '/home/nas/user/Uihyeop/.claude_reports/research/agent-engineering-principles/_internal';
const EXTRACTS = path.join(OUT, 'browser_extracts');
const SHOTS = path.join(OUT, 'screenshots');

const jobs = [
  { slug: 'loop-engineering-playbook', url: 'https://cobusgreyling.medium.com/loop-engineering-playbook-4460e01e88d8' },
  { slug: 'agent-model-harness', url: 'https://cobusgreyling.medium.com/agent-model-harness-0d018f3d5014' },
];
const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function run(browser, job) {
  for (let tries = 1; tries <= 5; tries++) {
    const ctx = await browser.newContext({
      userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      viewport: { width: 1920, height: 1080 }, locale: 'en-US',
      extraHTTPHeaders: { 'Referer': 'https://www.google.com/', 'Accept-Language': 'en-US,en;q=0.9' },
    });
    await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
    const page = await ctx.newPage();
    try {
      const resp = await page.goto(job.url, { waitUntil: 'domcontentloaded', timeout: 40000 });
      const status = resp ? resp.status() : 0;
      await sleep(6000);
      let bodyText = await page.innerText('body');
      if (bodyText.includes('something went wrong on our end')) {
        // try in-page reload
        await page.reload({ waitUntil: 'domcontentloaded', timeout: 40000 }).catch(()=>{});
        await sleep(6000);
        bodyText = await page.innerText('body');
      }
      if (bodyText.includes('something went wrong on our end')) {
        await ctx.close();
        await sleep(6000 * tries);
        continue;
      }
      for (let i = 0; i < 5; i++) { await page.evaluate(() => window.scrollBy(0, document.body.scrollHeight/5)); await sleep(900); }
      let text = '';
      const article = await page.$('article');
      if (article) text = await article.innerText();
      bodyText = await page.innerText('body');
      if (text.length < 500) text = bodyText;
      await page.screenshot({ path: path.join(SHOTS, job.slug + '.png') }).catch(()=>{});
      const lower = bodyText.toLowerCase();
      const paywalled = lower.includes('member-only story') || lower.includes('upgrade to read');
      const header = `URL: ${job.url}\nSLUG: ${job.slug}\nEXTRACTED_CHARS: ${text.length}\nTRUNCATED: ${paywalled}\nNOTE: ${paywalled?'PAYWALL partial':''}\nHTTP_STATUS: ${status} (attempt ${tries})\n${'='.repeat(70)}\n\n`;
      fs.writeFileSync(path.join(EXTRACTS, job.slug + '.txt'), header + text + (paywalled?'\n\n[--- TRUNCATED: paywall ---]\n':'\n'));
      await ctx.close();
      return { slug: job.slug, ok: text.length > 800, chars: text.length, tries, paywalled };
    } catch (e) {
      await ctx.close();
      await sleep(6000 * tries);
    }
  }
  return { slug: job.slug, ok: false, chars: 0, tries: 5, note: '500 after 5 tries' };
}

(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--disable-blink-features=AutomationControlled','--no-sandbox','--disable-dev-shm-usage'] });
  const results = [];
  try { for (const job of jobs) { results.push(await run(browser, job)); await sleep(4000); } }
  finally { await browser.close(); }
  console.log('=== RETRY2 ===');
  for (const r of results) console.log(`${r.ok?'OK ':'FAIL'} | ${r.slug} | chars=${r.chars} | tries=${r.tries} | ${r.note||(r.paywalled?'paywall':'')}`);
})();
