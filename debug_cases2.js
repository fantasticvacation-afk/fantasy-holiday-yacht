const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
  const page = await ctx.newPage();
  
  // Navigate to cases.html and take screenshot
  await page.goto('http://localhost:8080/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  
  // Check what's visible
  const info = await page.evaluate(() => {
    const cases = document.querySelectorAll('.case-card, .cases-masonry .case-card, .case-item');
    const visibleCases = [];
    cases.forEach(c => {
      const rect = c.getBoundingClientRect();
      visibleCases.push({
        visible: rect.width > 0 && rect.height > 0,
        w: Math.round(rect.width),
        h: Math.round(rect.height),
        text: c.textContent.trim().slice(0, 60)
      });
    });
    
    // Check cases-masonry
    const masonry = document.querySelector('.cases-masonry');
    const masonryStyle = masonry ? getComputedStyle(masonry) : null;
    
    return {
      caseCount: cases.length,
      cases: visibleCases.slice(0, 5),
      masonryExists: !!masonry,
      masonryDisplay: masonryStyle ? masonryStyle.display : 'N/A',
      masonryColumns: masonryStyle ? masonryStyle.columns : 'N/A',
      masonryHeight: masonry ? masonry.scrollHeight : 'N/A',
      bodyHeight: document.body.scrollHeight,
      // Check if content is behind navbar or something
      firstCaseTop: cases[0] ? Math.round(cases[0].getBoundingClientRect().top) : 'N/A',
      // Check section visibility
      sections: Array.from(document.querySelectorAll('section')).map(s => ({
        cls: s.className.slice(0, 40),
        top: Math.round(s.getBoundingClientRect().top),
        height: Math.round(s.getBoundingClientRect().height),
        visible: s.getBoundingClientRect().width > 0
      }))
    };
  });
  
  console.log('cases.html info:');
  console.log(JSON.stringify(info, null, 2));
  
  // Screenshot top portion
  await page.screenshot({ path: '/tmp/debug_cases_top.png', fullPage: false });
  // Screenshot full page
  await page.screenshot({ path: '/tmp/debug_cases_full.png', fullPage: true });
  
  // Now test on homepage: click "精选案例" in nav
  console.log('\n--- Testing homepage nav click ---');
  await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  
  // Click hamburger
  await page.click('.hamburger');
  await page.waitForTimeout(500);
  
  // Click "精选案例" link in mobile menu
  const caseLink = await page.$('.mobile-menu a:has-text("精选案例")');
  if (caseLink) {
    await caseLink.click();
    await page.waitForTimeout(2000);
    const url = page.url();
    const height = await page.evaluate(() => document.body.scrollHeight);
    const contentLen = await page.evaluate(() => document.body.innerText.length);
    console.log(`After click: URL=${url}, Height=${height}, Content=${contentLen}`);
    
    // Check what's visible
    const visibleContent = await page.evaluate(() => {
      const sections = document.querySelectorAll('section');
      const visible = [];
      sections.forEach((s, i) => {
        const rect = s.getBoundingClientRect();
        visible.push({
          idx: i,
          cls: s.className.slice(0, 30),
          top: Math.round(rect.top),
          height: Math.round(rect.height),
          visible: rect.width > 0 && rect.height > 0
        });
      });
      return visible;
    });
    console.log('Sections visible after navigation:');
    visibleContent.forEach(v => console.log(`  [${v.idx}] .${v.cls} top=${v.top} h=${v.height} visible=${v.visible}`));
    
    await page.screenshot({ path: '/tmp/debug_after_click.png', fullPage: false });
  } else {
    console.log('Case link not found in mobile menu');
  }
  
  await browser.close();
})();
