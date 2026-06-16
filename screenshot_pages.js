const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch();
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    deviceScaleFactor: 2
  });
  
  const pages = [
    { url: 'http://localhost:8080/index.html', name: 'homepage' },
    { url: 'http://localhost:8080/about.html', name: 'about' },
    { url: 'http://localhost:8080/fleet.html', name: 'fleet' },
    { url: 'http://localhost:8080/membership.html', name: 'membership' },
    { url: 'http://localhost:8080/news.html', name: 'news' },
    { url: 'http://localhost:8080/contact.html', name: 'contact' },
    { url: 'http://localhost:8080/YT/index.html', name: 'yt_homepage' },
  ];
  
  const outDir = '/tmp/site_screenshots';
  fs.mkdirSync(outDir, { recursive: true });
  
  for (const p of pages) {
    try {
      const page = await context.newPage();
      await page.goto(p.url, { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(1000);
      
      // Full page screenshot
      await page.screenshot({ 
        path: path.join(outDir, `${p.name}_full.png`),
        fullPage: true
      });
      
      // Top viewport screenshot
      await page.screenshot({ 
        path: path.join(outDir, `${p.name}_top.png`),
        fullPage: false
      });
      
      await page.close();
      console.log(`✓ ${p.name}`);
    } catch (e) {
      console.log(`✗ ${p.name}: ${e.message}`);
    }
  }
  
  await browser.close();
  console.log('Done');
})();
