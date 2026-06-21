const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  
  // Test Chinese cases.html
  await page.goto('http://localhost:8080/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  const zhInfo = await page.evaluate(() => ({
    cases: document.querySelectorAll('.case-card').length,
    height: document.body.scrollHeight,
    heroBg: getComputedStyle(document.querySelector('.cases-hero .hero-bg-img') || document.querySelector('.case-hero-bg') || {}).backgroundAttachment || 'N/A'
  }));
  console.log('ZH cases.html:', JSON.stringify(zhInfo));
  await page.screenshot({ path: '/tmp/verify_zh_cases.png', fullPage: false });
  
  // Test a case detail page
  await page.goto('http://localhost:8080/case-001.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  const case1Info = await page.evaluate(() => ({
    height: document.body.scrollHeight,
    heroBg: document.querySelector('.case-hero-bg') ? getComputedStyle(document.querySelector('.case-hero-bg')).backgroundAttachment : 'N/A'
  }));
  console.log('case-001.html:', JSON.stringify(case1Info));
  
  // Test English version
  await page.goto('http://localhost:8080/YT/en/case-006.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  const enCase6 = await page.evaluate(() => ({
    height: document.body.scrollHeight,
    title: document.title.slice(0, 50),
    heroExists: !!document.querySelector('.case-hero'),
    heroHeight: document.querySelector('.case-hero') ? Math.round(document.querySelector('.case-hero').getBoundingClientRect().height) : 0,
    heroBg: document.querySelector('.case-hero-bg') ? getComputedStyle(document.querySelector('.case-hero-bg')).backgroundAttachment : 'N/A'
  }));
  console.log('YT/en/case-006.html:', JSON.stringify(enCase6));
  await page.screenshot({ path: '/tmp/verify_en_case006.png', fullPage: false });
  
  if (errors.length > 0) {
    console.log('\nConsole errors:', errors.length);
    errors.forEach(e => console.log(`  ${e.slice(0, 100)}`));
  }
  
  await browser.close();
})();
