const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, isMobile: true });
  const page = await ctx.newPage();
  
  // Listen for console errors
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  
  await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  
  // Check what "精选案例" links to
  const caseLinks = await page.evaluate(() => {
    const links = [];
    document.querySelectorAll('a').forEach(a => {
      const text = a.textContent.trim();
      if (text.includes('案例') || text.includes('case') || text.includes('Case') || text.includes('精选')) {
        links.push({ text: text.slice(0, 40), href: a.href, target: a.target });
      }
    });
    return links;
  });
  console.log('Case-related links on homepage:');
  caseLinks.forEach(l => console.log(`  "${l.text}" → ${l.href} target=${l.target}`));
  
  // Check nav menu for cases
  const navLinks = await page.evaluate(() => {
    const links = [];
    document.querySelectorAll('.nav-dropdown-menu a, .nav-links a').forEach(a => {
      const text = a.textContent.trim();
      if (text.includes('案例') || text.includes('Case') || text.includes('case')) {
        links.push({ text: text.slice(0, 40), href: a.href });
      }
    });
    return links;
  });
  console.log('\nNav case links:');
  navLinks.forEach(l => console.log(`  "${l.text}" → ${l.href}`));
  
  // Try navigating to cases.html
  console.log('\n--- Testing cases.html ---');
  try {
    const resp = await page.goto('http://localhost:8080/cases.html', { waitUntil: 'networkidle', timeout: 10000 });
    console.log(`Status: ${resp.status()}`);
    const height = await page.evaluate(() => document.body.scrollHeight);
    const content = await page.evaluate(() => document.body.innerText.length);
    console.log(`Height: ${height}px, Content length: ${content}`);
  } catch(e) {
    console.log(`cases.html: ${e.message.slice(0, 80)}`);
  }
  
  // Try case-001.html  
  console.log('\n--- Testing case-001.html ---');
  try {
    const resp = await page.goto('http://localhost:8080/case-001.html', { waitUntil: 'networkidle', timeout: 10000 });
    console.log(`Status: ${resp.status()}`);
    const height = await page.evaluate(() => document.body.scrollHeight);
    console.log(`Height: ${height}px`);
  } catch(e) {
    console.log(`case-001.html: ${e.message.slice(0, 80)}`);
  }
  
  // Check mobile menu hamburger
  console.log('\n--- Testing mobile menu ---');
  await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle', timeout: 10000 });
  await page.waitForTimeout(1000);
  
  const menuInfo = await page.evaluate(() => {
    const hamburger = document.querySelector('.hamburger, .mobile-menu-toggle, #hamburger');
    const mobileMenu = document.querySelector('.mobile-menu, .nav-mobile, #mobileMenu');
    return {
      hamburgerExists: !!hamburger,
      hamburgerDisplay: hamburger ? getComputedStyle(hamburger).display : 'N/A',
      mobileMenuExists: !!mobileMenu,
      mobileMenuDisplay: mobileMenu ? getComputedStyle(mobileMenu).display : 'N/A',
      mobileMenuClass: mobileMenu ? mobileMenu.className : 'N/A'
    };
  });
  console.log('Mobile menu info:', JSON.stringify(menuInfo, null, 2));
  
  // Click hamburger and see what happens
  if (menuInfo.hamburgerExists) {
    await page.click('.hamburger, .mobile-menu-toggle, #hamburger');
    await page.waitForTimeout(1000);
    
    const afterClick = await page.evaluate(() => {
      const mobileMenu = document.querySelector('.mobile-menu, .nav-mobile, #mobileMenu');
      return {
        mobileMenuDisplay: mobileMenu ? getComputedStyle(mobileMenu).display : 'N/A',
        mobileMenuClass: mobileMenu ? mobileMenu.className : 'N/A',
        visibleLinks: []
      };
    });
    
    // Get all visible links in mobile menu
    const menuLinks = await page.evaluate(() => {
      const links = [];
      document.querySelectorAll('.mobile-menu a, .nav-mobile a, #mobileMenu a').forEach(a => {
        const rect = a.getBoundingClientRect();
        if (rect.width > 0 && rect.height > 0) {
          links.push({ text: a.textContent.trim().slice(0, 30), href: a.href });
        }
      });
      return links;
    });
    console.log('Mobile menu links after hamburger click:');
    menuLinks.forEach(l => console.log(`  "${l.text}" → ${l.href}`));
    
    // Look for case links in mobile menu
    const caseMenuLinks = menuLinks.filter(l => l.text.includes('案例') || l.text.includes('Case'));
    console.log(`\nCase links in mobile menu: ${caseMenuLinks.length}`);
    caseMenuLinks.forEach(l => console.log(`  "${l.text}" → ${l.href}`));
  }
  
  if (errors.length > 0) {
    console.log('\nConsole errors:');
    errors.forEach(e => console.log(`  ${e.slice(0, 100)}`));
  }
  
  // Screenshot
  await page.screenshot({ path: '/tmp/debug_cases.png', fullPage: false });
  
  await browser.close();
})();
