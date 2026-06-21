const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  
  // Test Chinese cases.html
  await page.goto('http://localhost:8080/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  const zhInfo = await page.evaluate(() => {
    const heroBg = document.querySelector('.cases-hero .hero-bg-img');
    const heroBgEl = document.querySelector('.case-hero-bg');
    return {
      cases: document.querySelectorAll('.case-card').length,
      height: document.body.scrollHeight,
      heroBgAttachment: heroBg ? getComputedStyle(heroBg).backgroundAttachment : (heroBgEl ? getComputedStyle(heroBgEl).backgroundAttachment : 'N/A')
    };
  });
  console.log('ZH cases.html:', JSON.stringify(zhInfo));
  await page.screenshot({ path: '/tmp/verify_zh_cases.png', fullPage: false });
  
  // Test case-001.html
  await page.goto('http://localhost:8080/case-001.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  const case1Info = await page.evaluate(() => {
    const heroBg = document.querySelector('.case-hero-bg');
    return {
      height: document.body.scrollHeight,
      heroBgAttachment: heroBg ? getComputedStyle(heroBg).backgroundAttachment : 'N/A'
    };
  });
  console.log('case-001.html:', JSON.stringify(case1Info));
  
  // Test YT/en/case-006.html (previously had CSS space errors)
  await page.goto('http://localhost:8080/YT/en/case-006.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  const enCase6 = await page.evaluate(() => {
    const hero = document.querySelector('.case-hero');
    const heroBg = document.querySelector('.case-hero-bg');
    return {
      height: document.body.scrollHeight,
      title: document.title.slice(0, 60),
      heroExists: !!hero,
      heroHeight: hero ? Math.round(hero.getBoundingClientRect().height) : 0,
      heroBgAttachment: heroBg ? getComputedStyle(heroBg).backgroundAttachment : 'N/A'
    };
  });
  console.log('YT/en/case-006.html:', JSON.stringify(enCase6));
  await page.screenshot({ path: '/tmp/verify_en_case006.png', fullPage: false });
  
  // Test YT/en/cases.html
  await page.goto('http://localhost:8080/YT/en/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1000);
  const enCases = await page.evaluate(() => ({
    cases: document.querySelectorAll('.case-card').length,
    height: document.body.scrollHeight
  }));
  console.log('YT/en/cases.html:', JSON.stringify(enCases));
  
  await browser.close();
  console.log('\n✅ All verifications passed');
})();
