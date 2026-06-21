const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  for (const pageName of ['custom', 'charter']) {
    const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
    const page = await ctx.newPage();
    await page.goto(`http://localhost:8080/${pageName}.html`, { waitUntil: 'networkidle', timeout: 15000 });
    await page.waitForTimeout(2000);
    
    const sections = await page.evaluate(() => {
      const results = [];
      document.querySelectorAll('section').forEach(el => {
        const rect = el.getBoundingClientRect();
        results.push({
          id: el.id || '',
          class: el.className.slice(0, 50),
          top: Math.round(rect.top + window.scrollY),
          height: Math.round(rect.height),
        });
      });
      return results;
    });
    console.log(`\n=== ${pageName}.html ===`);
    sections.forEach(s => console.log(`  #${s.id} .${s.class} | top:${s.top} h:${s.height}`));
    const total = sections.length > 0 ? sections[sections.length-1].top + sections[sections.length-1].height : 0;
    console.log(`  Total sections: ${sections.length}, page height: ${total}`);
    await ctx.close();
  }
  await browser.close();
})();
