const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  
  // Chinese cases.html
  await page.goto('http://localhost:8080/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  await page.screenshot({ path: '/tmp/mobile_zh_cases.png', fullPage: false });
  console.log('ZH cases screenshot saved');
  
  // Chinese case-001.html  
  await page.goto('http://localhost:8080/case-001.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/tmp/mobile_zh_case001.png', fullPage: false });
  console.log('ZH case-001 screenshot saved');
  
  // YT/en/case-006.html
  await page.goto('http://localhost:8080/YT/en/case-006.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/tmp/mobile_en_case006.png', fullPage: false });
  console.log('EN case-006 screenshot saved');
  
  // YT/en/cases.html
  await page.goto('http://localhost:8080/YT/en/cases.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(1500);
  await page.screenshot({ path: '/tmp/mobile_en_cases.png', fullPage: false });
  console.log('EN cases screenshot saved');
  
  await browser.close();
  console.log('Done!');
})();
