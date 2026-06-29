const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const OUT = '/home/nas/user/Uihyeop/.agent_reports/research/agent-engineering-principles/_internal';
const EXTRACTS = path.join(OUT, 'browser_extracts');
const SHOTS = path.join(OUT, 'screenshots');

const jobs = [
  { slug: 'loop-engineering', url: 'https://cobusgreyling.medium.com/loop-engineering-62926dd6991c' },
  { slug: 'loop-engineering-playbook', url: 'https://cobusgreyling.medium.com/loop-engineering-playbook-4460e01e88d8' },
  { slug: 'rise-of-ai-harness-engineering', url: 'https://cobusgreyling.medium.com/the-rise-of-ai-harness-engineering-5f5220de393e' },
  { slug: 'agent-model-harness', url: 'https://cobusgreyling.medium.com/agent-model-harness-0d018f3d5014' },
];

const sleep = (ms) => new Promise(r => setTimeout(r, ms));

async function extractOne(browser, job, results) {
  const ctx = await browser.new_context
    ? null
    : await browser.newContext({
        userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 },
        locale: 'en-US',
      });
  await ctx.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });
  const page = await ctx.newPage();
  let res = { slug: job.slug, url: job.url, ok: false, chars: 0, truncated: false, note: '' };
  try {
    await page.goto(job.url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await sleep(6000);
    // scroll to trigger lazy content
    for (let i = 0; i < 4; i++) {
      await page.evaluate(() => window.scrollBy(0, document.body.scrollHeight / 4));
      await sleep(800);
    }
    await page.screenshot({ path: path.join(SHOTS, job.slug + '.png'), fullPage: false }).catch(() => {});

    // Prefer the <article> element if present
    let text = '';
    const article = await page.$('article');
    if (article) {
      text = await article.innerText();
    }
    const bodyText = await page.innerText('body');
    if (text.length < 500) text = bodyText;

    // paywall detection
    const lower = bodyText.toLowerCase();
    const paywalled = lower.includes('member-only story') ||
                      lower.includes('this story is for medium members') ||
                      lower.includes('upgrade to read') ||
                      lower.includes('read more from') && text.length < 1500;

    res.truncated = paywalled;
    res.note = paywalled ? 'PAYWALL detected (member-only) — partial content only' : '';
    res.chars = text.length;
    res.ok = text.length > 300;

    const header = `URL: ${job.url}\nSLUG: ${job.slug}\nEXTRACTED_CHARS: ${text.length}\nTRUNCATED: ${res.truncated}\nNOTE: ${res.note}\n${'='.repeat(70)}\n\n`;
    fs.writeFileSync(path.join(EXTRACTS, job.slug + '.txt'), header + text + (res.truncated ? '\n\n[--- TRUNCATED: Medium paywall, content above may be partial ---]\n' : '\n'));
  } catch (e) {
    res.note = 'ERROR: ' + e.message.split('\n')[0];
    fs.writeFileSync(path.join(EXTRACTS, job.slug + '.txt'),
      `URL: ${job.url}\nSLUG: ${job.slug}\nFAILED: ${res.note}\n`);
  } finally {
    await ctx.close();
  }
  results.push(res);
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    args: ['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-dev-shm-usage'],
  });
  const results = [];
  try {
    for (const job of jobs) {
      await extractOne(browser, job, results);
      await sleep(3000); // rate limit same-domain
    }

    // Job 5: resolve "Configured, not coded" via Medium search
    let resolved = null;
    try {
      const ctx = await browser.newContext({
        userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        viewport: { width: 1920, height: 1080 }, locale: 'en-US',
      });
      const page = await ctx.newPage();
      await page.goto('https://medium.com/search?q=Configured%2C%20not%20coded%20Cobus%20Greyling', { waitUntil: 'domcontentloaded', timeout: 30000 });
      await sleep(6000);
      const links = await page.$$eval('a[href*="/"]', as => as.map(a => ({ href: a.href, text: a.innerText })));
      const cand = links.filter(l => /configured/i.test(l.text) || /configured-not-coded/i.test(l.href));
      if (cand.length) resolved = cand[0].href.split('?')[0];
      // also dump all candidate-ish links for debugging
      fs.writeFileSync(path.join(OUT, 'search_links_debug.txt'),
        links.filter(l => /cobusgreyling|configured/i.test(l.href)).map(l => l.href + ' :: ' + (l.text||'').slice(0,60)).join('\n'));
      await ctx.close();
    } catch (e) {
      fs.writeFileSync(path.join(OUT, 'search_links_debug.txt'), 'SEARCH ERROR: ' + e.message.split('\n')[0]);
    }

    if (resolved) {
      await extractOne(browser, { slug: 'configured-not-coded', url: resolved }, results);
    } else {
      results.push({ slug: 'configured-not-coded', url: 'UNRESOLVED', ok: false, chars: 0, truncated: false, note: 'Could not resolve URL via Medium search' });
    }
  } finally {
    await browser.close();
  }

  console.log('=== RESULTS ===');
  for (const r of results) {
    console.log(`${r.ok ? 'OK ' : 'FAIL'} | ${r.slug} | chars=${r.chars} | trunc=${r.truncated} | ${r.url} | ${r.note}`);
  }
})();
