const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const pages = [
    { name: 'homepage', url: 'http://localhost:8080/index.html' },
    { name: 'about', url: 'http://localhost:8080/about.html' },
    { name: 'yachts', url: 'http://localhost:8080/yachts.html' },
    { name: 'membership', url: 'http://localhost:8080/membership.html' },
    { name: 'custom', url: 'http://localhost:8080/custom.html' },
    { name: 'charter', url: 'http://localhost:8080/charter.html' },
    { name: 'news', url: 'http://localhost:8080/news.html' },
    { name: 'contact', url: 'http://localhost:8080/contact.html' }
  ];
  for (const p of pages) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
    const page = await ctx.newPage();
    try {
      await page.goto(p.url, { waitUntil: 'networkidle', timeout: 15000 });
      await page.waitForTimeout(1500);
      await page.screenshot({ path: `/tmp/mobile_${p.name}.png`, fullPage: true });
      const height = await page.evaluate(() => document.body.scrollHeight);
      console.log(`${p.name}: ${height}px`);
    } catch(e) { console.log(`${p.name}: ERROR ${e.message.slice(0,80)}`); }
    await ctx.close();
  }
  await browser.close();
})();
