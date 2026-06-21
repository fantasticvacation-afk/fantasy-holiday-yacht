const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true, hasTouch: true });
  const page = await ctx.newPage();
  
  const errors = [];
  page.on('console', msg => { if (msg.type() === 'error') errors.push(msg.text()); });
  page.on('pageerror', err => errors.push('PAGE_ERROR: ' + err.message));
  
  // Check live site
  try {
    const resp = await page.goto('https://www.fantastic-vacation.com/cases.html', { waitUntil: 'networkidle', timeout: 20000 });
    console.log(`Live cases.html status: ${resp.status()}`);
    await page.waitForTimeout(2000);
    
    const info = await page.evaluate(() => {
      const cases = document.querySelectorAll('.case-card, .case-item');
      const sections = document.querySelectorAll('section');
      return {
        caseCount: cases.length,
        bodyHeight: document.body.scrollHeight,
        contentLen: document.body.innerText.length,
        title: document.title,
        sections: Array.from(sections).map(s => ({
          cls: s.className.slice(0, 30),
          visible: s.getBoundingClientRect().width > 0,
          height: Math.round(s.getBoundingClientRect().height)
        })),
        // Check CSS loaded
        cssLoaded: Array.from(document.styleSheets).length,
        // Check style.css href
        styleHref: document.querySelector('link[rel="stylesheet"]')?.href || 'N/A'
      };
    });
    console.log('Live cases.html info:', JSON.stringify(info, null, 2));
    
    await page.screenshot({ path: '/tmp/live_cases.png', fullPage: false });
  } catch(e) {
    console.log(`Live error: ${e.message.slice(0, 100)}`);
  }
  
  if (errors.length > 0) {
    console.log('\nErrors:');
    errors.forEach(e => console.log(`  ${e.slice(0, 120)}`));
  }
  
  // Also test the homepage on live and click the nav
  console.log('\n--- Live homepage nav test ---');
  await page.goto('https://www.fantastic-vacation.com/', { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(1000);
  
  // Check hamburger
  const hamInfo = await page.evaluate(() => {
    const h = document.querySelector('.hamburger');
    const m = document.querySelector('.mobile-menu');
    return {
      hamExists: !!h,
      hamDisplay: h ? getComputedStyle(h).display : 'N/A',
      menuExists: !!m,
      menuDisplay: m ? getComputedStyle(m).display : 'N/A'
    };
  });
  console.log('Hamburger:', JSON.stringify(hamInfo));
  
  if (hamInfo.hamExists && hamInfo.hamDisplay !== 'none') {
    await page.click('.hamburger');
    await page.waitForTimeout(500);
    
    // Check mobile menu visibility
    const menuVisible = await page.evaluate(() => {
      const m = document.querySelector('.mobile-menu');
      if (!m) return false;
      const rect = m.getBoundingClientRect();
      return rect.width > 0 && rect.height > 0;
    });
    console.log('Mobile menu visible after click:', menuVisible);
    
    if (menuVisible) {
      // Find and click cases link
      const caseLink = await page.$('.mobile-menu a[href*="cases"]');
      if (caseLink) {
        await caseLink.click();
        await page.waitForTimeout(2000);
        console.log('After click, URL:', page.url());
        const h = await page.evaluate(() => document.body.scrollHeight);
        const cases = await page.evaluate(() => document.querySelectorAll('.case-card').length);
        console.log(`Height: ${h}, Cases: ${cases}`);
        await page.screenshot({ path: '/tmp/live_after_nav.png', fullPage: false });
      } else {
        console.log('Case link not found in mobile menu');
      }
    } else {
      console.log('Mobile menu not visible after hamburger click');
      await page.screenshot({ path: '/tmp/live_ham_click.png', fullPage: false });
    }
  }
  
  await browser.close();
})();
