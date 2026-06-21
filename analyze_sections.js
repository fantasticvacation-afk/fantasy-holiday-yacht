const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
  const page = await ctx.newPage();
  await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  
  const sections = await page.evaluate(() => {
    const results = [];
    document.querySelectorAll('section, footer, .section-padding').forEach(el => {
      const rect = el.getBoundingClientRect();
      results.push({
        tag: el.tagName,
        id: el.id || '',
        class: el.className.slice(0, 60),
        top: Math.round(rect.top + window.scrollY),
        height: Math.round(rect.height),
        padding: getComputedStyle(el).padding
      });
    });
    return results;
  });
  
  sections.forEach(s => console.log(`${s.tag} #${s.id} .${s.class} | top:${s.top} h:${s.height} pad:${s.padding}`));
  
  // Also check for large gaps
  const gaps = await page.evaluate(() => {
    const results = [];
    const all = document.querySelectorAll('section, footer');
    let prevBottom = 0;
    all.forEach(el => {
      const rect = el.getBoundingClientRect();
      const top = rect.top + window.scrollY;
      if (prevBottom > 0 && top - prevBottom > 20) {
        results.push({ gap: Math.round(top - prevBottom), at: Math.round(top) });
      }
      prevBottom = top + rect.height;
    });
    return results;
  });
  console.log('\n--- GAPS > 20px ---');
  gaps.forEach(g => console.log(`Gap: ${g.gap}px at y=${g.at}`));
  
  await browser.close();
})();
