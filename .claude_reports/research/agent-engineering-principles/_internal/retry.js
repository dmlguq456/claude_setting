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

async function attempt(browser, job) {
  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    viewport: { width: 1920, height: 1080 }, locale: 'en-US',
  });
  await ctx.addInitScript(() => { Object.defineProperty(navigator, 'webdriver', { get: () => undefined }); });
  const page = await ctx.newPage();
  try {
    await page.goto(job.url, { waitUntil: 'networkidle', timeout: 45000 }).catch(()=>{});
    await sleep(7000);
    for (let i = 0; i < 5; i++) {
      await page.evaluate(() => window.scrollBy(0, document.body.scrollHeight / 5));
      await sleep(900);
    }
    let text = '';
    const article = await page.$('article');
    if (article) text = await article.innerText();
    const bodyText = await page.innerText('body');
    if (text.length < 500) text = bodyText;
    await page.screenshot({ path: path.join(SHOTS, job.slug + '.png') }).catch(()=>{});
    const is500 = bodyText.includes('something went wrong on our end');
    return { text, bodyText, is500, ctx };
  } catch (e) {
    return { text: '', bodyText: '', is500: false, ctx, err: e.message.split('\n')[0] };
  }
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const results = [];
  try {
    for (const job of jobs) {
      let final = null;
      for (let tries = 1; tries <= 3; tries++) {
        const r = await attempt(browser, job);
        if (r.text && r.text.length > 800 && !r.is500) { final = r; await r.ctx.close(); break; }
        await r.ctx.close();
        await sleep(5000 * tries);
        if (tries === 3) final = r;
      }
      const text = final.text || '';
      const ok = text.length > 800 && !final.is500;
      const lower = (final.bodyText||'').toLowerCase();
      const paywalled = lower.includes('member-only story') || lower.includes('upgrade to read');
      const note = final.is500 ? 'Medium 500 error after retries' : (paywalled ? 'PAYWALL partial' : (ok ? '' : 'short content'));
      const header = `URL: ${job.url}\nSLUG: ${job.slug}\nEXTRACTED_CHARS: ${text.length}\nTRUNCATED: ${paywalled}\nNOTE: ${note}\n${'='.repeat(70)}\n\n`;
      if (ok || text.length > 169) {
        fs.writeFileSync(path.join(EXTRACTS, job.slug + '.txt'), header + text + (paywalled ? '\n\n[--- TRUNCATED: paywall ---]\n' : '\n'));
      }
      results.push({ slug: job.slug, ok, chars: text.length, note });
      await sleep(3000);
    }
  } finally {
    await browser.close();
  }
  console.log('=== RETRY RESULTS ===');
  for (const r of results) console.log(`${r.ok?'OK ':'FAIL'} | ${r.slug} | chars=${r.chars} | ${r.note}`);
})();
