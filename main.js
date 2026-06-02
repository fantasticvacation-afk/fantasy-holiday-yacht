/* main.js - 奇幻假期游艇网站主逻辑 */

/* === 语言切换按钮智能跳转 === */
(function(){
  var path = window.location.pathname;
  var isEN = path.indexOf('/en/') !== -1;
  var p = path.split('/').pop();
  // Check if this is a detail page that should use in-place i18n switch
  var isDetailPage = /^(news-|case-|partner-)/.test(p);
  
  // For detail pages, skip setting href here — the bottom IIFE (section B) will handle them
  // with in-place i18n language switching instead of page navigation
  
  // Navbar lang switch
  var btn = document.querySelector('.lang-switch-btn');
  if (btn && !isDetailPage) {
    if (isEN) btn.href = path.replace('/en/', '/');
    else {
      var parts = path.split('/');
      var filename = parts[parts.length - 1] || 'index.html';
      btn.href = parts.slice(0, -1).join('/') + '/en/' + filename;
    }
  }
  
  // Mobile menu lang switch
  var mobileBtn = document.querySelector('#mobileLangSwitch');
  if (mobileBtn && !isDetailPage) {
    if (isEN) {
      var cnPath = path.replace('/en/', '/');
      // For sub-pages in membership/, the root is ../
      if (path.indexOf('/membership/') !== -1) {
        // EN membershp page: switch to CN membership/
        cnPath = path.replace(/\/en\/(.*)/, '/$1');
      }
      mobileBtn.href = cnPath;
      if (isEN) mobileBtn.textContent = '🌐 切换到中文';
    } else {
      var filename_m = path.split('/').pop() || 'index.html';
      var dir_m = path.split('/').slice(0, -1).join('/');
      mobileBtn.href = dir_m + '/en/' + filename_m;
      mobileBtn.textContent = '🌐 English Version';
    }
  }
})();

/* === Loading 动画控制 === */
window.addEventListener("DOMContentLoaded", function() {
  var loader = document.getElementById("loader");
  if (!loader) return;
  var progressEl = document.getElementById("progress");
  var progress = 0;
  var interval = setInterval(function() {
    progress += Math.random() * 12 + 8;
    if (progress >= 100) {
      progress = 100;
      clearInterval(interval);
      if (progressEl) progressEl.style.width = "100%";
      setTimeout(function() {
        if (loader) { loader.style.opacity = "0"; setTimeout(function(){ loader.style.display = "none"; }, 400); }
        document.body.style.overflow = "";
      }, 400);
    } else if (progressEl) {
      progressEl.style.width = progress + "%";
    }
  }, 180);
  // 5秒强制隐藏
  setTimeout(function() {
    clearInterval(interval);
    if (loader) { loader.style.opacity = "0"; setTimeout(function(){ loader.style.display = "none"; }, 400); }
    document.body.style.overflow = "";
  }, 5000);
});

/* === 导航栏滚动效果 === */
window.addEventListener("scroll", function() {
  var nav = document.getElementById("navbar");
  if (!nav) return;
  if (window.scrollY > 50) {
    nav.classList.add("scrolled");
  } else {
    nav.classList.remove("scrolled");
  }
});

/* === 移动端菜单切换 === */
function toggleMobile() {
  console.log('toggleMobile() 被调用');
  var menu = document.getElementById("mobile-menu");
  var hamburger = document.querySelector(".hamburger");
  console.log('menu:', menu);
  console.log('hamburger:', hamburger);
  if (menu) {
    menu.classList.toggle("active");
    console.log('menu active:', menu.classList.contains('active'));
  }
  if (hamburger) {
    hamburger.classList.toggle("active");
    console.log('hamburger active:', hamburger.classList.contains('active'));
  }
}

/* === 搜索功能 === */
function toggleSearch() {
  var overlay = document.getElementById("searchOverlay");
  if (!overlay) return;
  overlay.classList.toggle("active");
  if (overlay.classList.contains("active")) {
    setTimeout(function() {
      var input = document.getElementById("searchInput");
      if (input) { input.focus(); input.select(); }
    }, 100);
  }
}

function isEnPage() {
  return (window.location.pathname || '').indexOf('/en/') !== -1;
}

var SEARCH_ROUTES = [
  { keys: ['yacht','游艇','boat','船','ship','艇','sovereign','expedition','flybridge','daycruiser','君临','远征','飞桥','日间','君悦','探险'],            page:'yachts.html' },
  { keys: ['custom','定制','bespoke','tailor','设计','build','专属','personaliz'],                                   page:'custom.html' },
  { keys: ['charter','租赁','rent','航线','route','地中海','加勒比','caribbean','东南亚','southeast'],  page:'charter.html' },
  { keys: ['management','托管','维保','维修','保养','maintenance','service','after sales'],                 page:'management.html' },
  { keys: ['case','案例','portfolio','项目','交付','delivery','幻蓝','phantom'],                          page:'cases.html' },
  { keys: ['news','新闻','资讯','press','媒体','media','动态'],                                                  page:'news.html' },
  { keys: ['about','关于','简介','历史','history','团队','team','文化','culture','使命','mission','愿景','vision'], page:'about.html' },
  { keys: ['member','会员','silver','gold','platinum','diamond','black','tier','等级','权益','privilege','benefit'], page:'membership.html' },
  { keys: ['partner','合作','dealer','代理','agent','marina','品牌','brand'],                               page:'partnership.html' },
  { keys: ['contact','联系','电话','phone','邮箱','email','地址','address','location','office'],             page:'contact.html' },
  { keys: ['ir','investor','投资','财务','financial','财报','公告','announcement','治理','governance'],     page:'ir.html' }
];

function doSearch(q) {
  var kw = (q||'').toLowerCase().trim();
  if (!kw) return;
  var en = isEnPage();
  for (var i = 0; i < SEARCH_ROUTES.length; i++) {
    var r = SEARCH_ROUTES[i];
    for (var j = 0; j < r.keys.length; j++) {
      if (kw.indexOf(r.keys[j]) !== -1) {
        window.location.href = en ? r.page : '../' + r.page;
        return;
      }
    }
  }
  /* fallback */
  var overlay = document.getElementById('searchOverlay');
  if (overlay) overlay.classList.remove('active');
  var input = document.getElementById('searchInput');
  if (input) {
    input.placeholder = en ? 'No result, try: yacht / charter / contact...' : '未找到结果，请尝试：游艇 / 租赁 / 联系...';
    setTimeout(function(){ if (input) input.placeholder = en ? 'Search yachts, news, cases...' : '搜索产品、新闻、案例...'; }, 3000);
  }
}

function closeSearch() {
  var overlay = document.getElementById('searchOverlay');
  if (overlay) overlay.classList.remove('active');
}

function attachSearch() {
  /* 搜索建议点击 */
  var items = document.querySelectorAll('.search-suggestion-item');
  for (var i = 0; i < items.length; i++) {
    (function(el){ el.addEventListener('click', function(){ var t = (el.textContent||'').replace(/^→\s*/,'').trim(); if(t){ closeSearch(); doSearch(t); } }); })(items[i]);
  }
  /* 回车搜索 */
  var input = document.getElementById('searchInput');
  if (input && !input._searchBound) {
    input._searchBound = true;
    input.addEventListener('keydown', function(e){ if(e.key==='Enter'){ e.preventDefault(); closeSearch(); doSearch(this.value); } });
  }
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', attachSearch);
} else {
  attachSearch();
}

/* === ESC 关闭搜索/菜单 === */
document.addEventListener("keydown", function(e) {
  if (e.key === "Escape") {
    var overlay = document.getElementById("searchOverlay");
    if (overlay && overlay.classList.contains("active")) overlay.classList.remove("active");
    var menu = document.getElementById("mobile-menu");
    if (menu && menu.classList.contains("active")) {
      menu.classList.remove("active");
      var hamburger = document.querySelector(".hamburger");
      if (hamburger) hamburger.classList.remove("active");
    }
  }
});

/* === 暗色模式切换 === */
function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
  var isDark = document.body.classList.contains("dark-mode");
  localStorage.setItem("fv-dark", isDark ? "1" : "0");
  var moon = document.querySelector(".icon-moon");
  var sun = document.querySelector(".icon-sun");
  if (moon) moon.style.display = isDark ? "none" : "inline";
  if (sun) sun.style.display = isDark ? "inline" : "none";
}

/* === 初始化暗色模式 === */
window.addEventListener("DOMContentLoaded", function() {
  var isDark = localStorage.getItem("fv-dark") === "1";
  if (isDark) {
    document.body.classList.add("dark-mode");
    var moon = document.querySelector(".icon-moon");
    var sun = document.querySelector(".icon-sun");
    if (moon) moon.style.display = "none";
    if (sun) sun.style.display = "inline";
  }
});

/* === 搜索建议项点击跳转 === */
window.addEventListener("DOMContentLoaded", function() {
  document.querySelectorAll(".search-suggestion-item").forEach(function(el) {
    el.addEventListener("click", function() {
      var text = el.textContent.trim();
      if (text.indexOf("全系") !== -1 || text.indexOf("All Yachts") !== -1) {
        window.location.href = "yachts.html";
      } else if (text.indexOf("定制") !== -1 || text.indexOf("Custom") !== -1) {
        window.location.href = "custom.html";
      } else if (text.indexOf("航线") !== -1 || text.indexOf("Routes") !== -1) {
        window.location.href = "charter.html";
      } else if (text.indexOf("联系") !== -1 || text.indexOf("Contact") !== -1 || text.indexOf("顾问") !== -1 || text.indexOf("Advisor") !== -1) {
        window.location.href = "contact.html";
      }
    });
  });
});

/* === 回到顶部 === */
window.addEventListener("scroll", function() {
  var btn = document.getElementById("backToTop");
  if (!btn) return;
  if (window.scrollY > 400) {
    btn.classList.add("visible");
  } else {
    btn.classList.remove("visible");
  }
});

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/* === 平滑滚动（锚点链接）=== */
document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
  anchor.addEventListener("click", function(e) {
    var target = document.querySelector(this.getAttribute("href"));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth" });
    }
  });
});

/* === 惰性加载（图片）=== */
if ("IntersectionObserver" in window) {
  var lazyImages = document.querySelectorAll("img[data-src]");
  var imageObserver = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        var img = entry.target;
        img.src = img.getAttribute("data-src");
        img.removeAttribute("data-src");
        imageObserver.unobserve(img);
      }
    });
  });
  lazyImages.forEach(function(img) { imageObserver.observe(img); });
}

/* === 数字动画 === */
function animateNumbers() {
  document.querySelectorAll("[data-count]").forEach(function(el) {
    var target = parseInt(el.getAttribute("data-count"));
    var duration = 2000;
    var start = 0;
    var startTime = null;
    function step(timestamp) {
      if (!startTime) startTime = timestamp;
      var progress = Math.min((timestamp - startTime) / duration, 1);
      var ease = 1 - Math.pow(1 - progress, 3); // easeOutCubic
      el.textContent = Math.floor(ease * target);
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target;
      }
    }
    requestAnimationFrame(step);
  });
}

/* === 初始化 === */
window.addEventListener("DOMContentLoaded", function() {
  // 触发数字动画（如果页面有 data-count 元素）
  if (document.querySelector("[data-count]")) {
    var observer = new IntersectionObserver(function(entries) {
      entries.forEach(function(entry) {
        if (entry.isIntersecting) {
          animateNumbers();
          observer.disconnect();
        }
      });
    });
    observer.observe(document.querySelector("[data-count]").parentElement || document.body);
  }
});


/* ===== Scroll Reveal Observer ===== */
(function(){
  if(!("IntersectionObserver" in window)){
    document.querySelectorAll('.reveal').forEach(function(el){ el.classList.add('revealed'); });
    return;
  }
  var revealObserver = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        entry.target.classList.add('revealed');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.reveal').forEach(function(el){ revealObserver.observe(el); });
})();

/* ===== Language Switch ===== */
// Note: Language switching is handled by the top IIFE (page navigation)
// and the bottom IIFE section B (in-place i18n for detail pages).
// This block is kept as a fallback for any page using id="langSwitchBtn".
document.addEventListener('DOMContentLoaded', function(){
  var langBtn = document.getElementById('langSwitchBtn');
  if(langBtn){
    langBtn.addEventListener('click', function(e){
      e.preventDefault();
      var path = window.location.pathname;
      if(path.indexOf('/en/') === -1){
        // CN page → go to EN equivalent
        var parts = path.split('/');
        var filename = parts[parts.length - 1] || 'index.html';
        var dir = parts.slice(0, -1).join('/');
        window.location.href = dir + '/en/' + filename;
      } else {
        // EN page → go to CN equivalent
        window.location.href = path.replace('/en/', '/');
      }
    });
  }
});

/* ===== 预约表单验证与提交 ===== */
function handleSubmit(e) {
  e.preventDefault();
  var form = document.getElementById("bookingForm");
  var name = document.getElementById("booking_name");
  var phone = document.getElementById("booking_phone");
  var email = document.getElementById("booking_email");
  var dest = document.getElementById("booking_destination");
  var depart = document.getElementById("booking_departure");
  var people = document.getElementById("booking_people");
  var budget = document.getElementById("booking_budget");

  if (!name || !name.value.trim()) { alert("请输入您的姓名"); name && name.focus(); return false; }
  if (!phone || !phone.value.trim()) { alert("请输入您的联系电话"); phone && phone.focus(); return false; }
  var phoneVal = phone.value.trim();
  if (!/^[\d\s\-+()（）]{7,20}$/.test(phoneVal)) { alert("请输入有效的联系电话"); phone.focus(); return false; }
  if (email && email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) { alert("请输入有效的电子邮箱"); email.focus(); return false; }
  if (dest && !dest.value.trim()) { alert("请选择意向目的地"); dest.focus(); return false; }
  if (depart && !depart.value.trim()) { alert("请选择出行时间"); depart.focus(); return false; }
  if (people && !people.value.trim()) { alert("请选择同行人数"); people.focus(); return false; }
  if (budget && !budget.value.trim()) { alert("请选择预算区间"); budget.focus(); return false; }

  // 显示提交状态
  var btn = form.querySelector("button[type=submit]");
  var orig = btn.textContent;
  btn.textContent = "⏳ 提交中...";
  btn.disabled = true;

  var data = new FormData(form);
  fetch(form.action, { method: "POST", body: data, headers: { "Accept": "application/json" } })
    .then(function(r) {
      if (r.ok) {
        alert("✅ 预约已提交成功！我们的顾问将在24小时内与您联系。");
        form.reset();
      } else {
        alert("⚠️ 提交失败，请稍后重试。或直接致电 0755-3353-0188");
      }
    })
    .catch(function() {
      alert("⚠️ 网络异常，提交失败。请检查网络连接后重试，或直接致电 0755-3353-0188");
    })
    .finally(function() {
      btn.textContent = orig;
      btn.disabled = false;
    });
  return false;
}

/* ===== 定制表单验证与提交 ===== */
function handleCustomSubmit(e) {
  e.preventDefault();
  var form = document.getElementById("customForm");
  if (!form) return false;

  var name = document.getElementById("custom_name");
  var phone = document.getElementById("custom_phone");
  var series = document.getElementById("custom_series");
  var email = document.getElementById("custom_email");

  var ok = true;
  function mark(el, valid) { if (!el) return; el.style.borderColor = valid ? '' : '#e57373'; if (!valid) ok = false; }

  mark(name, name && name.value.trim().length > 0);
  mark(phone, phone && /^[\d\s\-+()（）]{7,20}$/.test(phone.value.trim()));
  mark(series, series && series.value !== '');
  if (email && email.value.trim() && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    email.style.borderColor = '#e57373'; ok = false;
  }

  if (!ok) { alert('请正确填写必填项（姓名、联系电话、意向船型）'); return false; }

  var btn = document.getElementById('customSubmitBtn');
  if (btn) { btn.textContent = '⏳ 提交中...'; btn.disabled = true; }

  var data = new FormData(form);
  fetch(form.action, { method: 'POST', body: data, headers: { 'Accept': 'application/json' } })
    .then(function() { showCustomSuccess(); })
    .catch(function() { showCustomSuccess(); });
  return false;
}

function showCustomSuccess() {
  var card = document.querySelector('#customForm .cta-form-card');
  var ok = document.getElementById('customSuccess');
  if (card) card.style.display = 'none';
  if (ok) { ok.style.display = 'block'; ok.scrollIntoView({ behavior: 'smooth', block: 'center' }); }
}

/* Attach submit listener if new form exists (no onsubmit attribute) */
(function() {
  var cf = document.getElementById('customForm');
  if (cf && !cf.hasAttribute('onsubmit')) {
    cf.addEventListener('submit', handleCustomSubmit);
  }
  /* Floating label fix for custom form selects */
  document.querySelectorAll('#customForm .form-group select').forEach(function(s) {
    function upd() { s.classList.toggle('has-value', s.selectedIndex > 0); }
    s.addEventListener('change', upd);
    upd();
  });
})();


/* ===== 四大核心系列 查看更多/收起 ===== */
function toggleSeries(){
  var card = document.getElementById("seriesHidden");
  var btn = document.getElementById("seriesToggleBtn");
  if(!card || !btn) return;
  var isHidden = card.classList.contains("yacht-card-hidden");
  if(isHidden){
    card.classList.remove("yacht-card-hidden");
    card.classList.add("yacht-card-expanded");
    btn.classList.add("expanded");
    card.querySelectorAll(".reveal").forEach(function(el){ el.classList.add("revealed"); });
  } else {
    card.classList.add("yacht-card-hidden");
    card.classList.remove("yacht-card-expanded");
    btn.classList.remove("expanded");
  }
  // update button text with i18n support
  try {
    var lang = localStorage.getItem("fv-lang") || "zh";
    var key = isHidden ? "index.toggle_less" : "index.toggle_more";
    var span = btn.querySelector("span:first-child");
    if(span && typeof dict !== "undefined" && dict[key] && dict[key][lang]){
      span.textContent = dict[key][lang];
    }
  } catch(e){}
}

/* ===== CN-only page → EN redirect logic ===== */
(function() {
  var EN_MAP = {
    'about-history.html':'en/about.html','about-culture.html':'en/about.html','about-structure.html':'en/about.html',
    'about-responsibility.html':'en/about.html','about-intro.html':'en/about.html',
    'yachts-sovereign.html':'en/yachts-sovereign.html','yachts-expedition.html':'en/yachts-expedition.html',
    'yachts-flybridge.html':'en/yachts-flybridge.html','yachts-daycruiser.html':'en/yachts-daycruiser.html',
    'press.html':'en/news.html',
    'terms.html':'en/terms.html','privacy.html':'en/privacy.html','sitemap.html':'en/sitemap.html',
    'partner-apply.html':'en/partnership.html','partner-cases.html':'en/partnership.html',
    'partner-list.html':'en/partnership.html','partner-map.html':'en/partnership.html',
    'partner-process.html':'en/partnership.html',
    'partner-type-shipyard.html':'en/partnership.html','partner-type-marina.html':'en/partnership.html',
    'partner-type-aviation.html':'en/partnership.html','partner-type-hotel.html':'en/partnership.html',
    'partner-type-art.html':'en/partnership.html','partner-type-association.html':'en/partnership.html',
    'partner-type-brand.html':'en/partnership.html','partner-type-service.html':'en/partnership.html',
    'partner-type-agent.html':'en/partnership.html','partner-type-tech.html':'en/partnership.html'
  };

  // Helper: given a filename, return the best EN target or null
  function enTarget(filename) {
    if (EN_MAP[filename]) return '/' + EN_MAP[filename];
    if (/^case-/.test(filename)) return '/en/cases.html';
    if (/^news-/.test(filename)) return '/en/news.html';
    if (/^partner-/.test(filename)) return '/en/partnership.html';
    return null;
  }

  var path = window.location.pathname;
  var isEN = path.indexOf('/en/') !== -1;
  var p = path.split('/').pop();

  // A) On EN pages or CN pages showing English: intercept clicks on nav links
  var langParam = /[?&]lang=en/.test(window.location.search);
  var isEnglishMode = isEN || langParam;
  if (isEnglishMode) {
    document.addEventListener('click', function(e) {
      var a = e.target.closest('a[href]');
      if (!a) return;
      // Skip language switch buttons — handled by section B
      if (a.classList.contains('lang-switch-btn') || a.id === 'mobileLangSwitch') return;
      var href = a.getAttribute('href');
      if (!href) return;
      // Skip links that already have ?lang= parameter
      if (href.indexOf('lang=') !== -1) return;
      // Resolve relative ../ hrefs to just the filename
      var parts = href.split('/');
      var filename = parts[parts.length - 1];
      // Skip if filename is empty or a hash
      if (!filename || filename.charAt(0) === '#') return;
      
      if (isEN) {
        // On actual EN pages: use enTarget logic
        var target = enTarget(filename);
        if (target) {
          e.preventDefault();
          e.stopPropagation();
          if (/^(news-|case-|partner-)/.test(filename)) {
            var resolved = new URL(href, window.location.href);
            window.location.href = resolved.pathname + '?lang=en';
          } else {
            // Relative from EN page: strip /en/ prefix → same-directory page
            window.location.href = target.replace('/en/', '');
          }
        }
      } else if (langParam) {
        // On CN detail page showing English: redirect nav links to EN equivalents
        var target = enTarget(filename);
        if (target) {
          // Has EN equivalent page — navigate there with relative path
          e.preventDefault();
          e.stopPropagation();
          window.location.href = target.slice(1);
        } else if (!/^(news-|case-|partner-)/.test(filename)) {
          // No EN equivalent and not a detail page — check if EN version exists
          // EN pages that exist: en/[same-filename]
          var enPages = ['index.html','yachts.html','yachts-sovereign.html','yachts-expedition.html',
            'yachts-flybridge.html','yachts-daycruiser.html','custom.html','charter.html',
            'management.html','cases.html','news.html','about.html','membership.html',
            'partnership.html','contact.html','ir.html','honors.html','terms.html','privacy.html','sitemap.html'];
          if (enPages.indexOf(filename) !== -1) {
            e.preventDefault();
            e.stopPropagation();
            var dir = window.location.pathname.split('/').slice(0, -1).join('/');
            window.location.href = dir + '/en/' + filename;
          }
        }
      }
    }, true);
  }

  // B) On CN-only pages: repurpose language switch
  var target = enTarget(p);
  var isDetailPage = /^(news-|case-|partner-)/.test(p);
  var hasLangParam = /[?&]lang=en/.test(window.location.search);
  
  if (target) {
    var f = function(){
      var btns = document.querySelectorAll('.lang-switch-btn, #mobileLangSwitch');
      for (var i=0; i<btns.length; i++) {
        var b = btns[i];
        
        if (isDetailPage) {
          // Detail pages: navigate to corresponding list page (no EN detail pages exist)
          if (hasLangParam) {
            // Currently showing English via ?lang=en — go back to CN list page
            b.textContent = '中文';
            b.title = '切换到中文';
            b.setAttribute('aria-label','切换到中文');
            // Relative: /en/news.html → news.html (same-directory CN list)
            b.href = target.replace('/en/', '');
          } else {
            // CN detail page — navigate to EN list page
            b.textContent = 'EN';
            b.title = 'Switch to English';
            b.setAttribute('aria-label','Switch to English');
            // Relative: /en/news.html → en/news.html
            b.href = target.slice(1);
          }
          b.style.display = '';
          b.removeAttribute('onclick');
        } else {
          // Non-detail CN-only pages: jump to EN page
          b.textContent = 'EN';
          // Relative: /en/foo.html → en/foo.html
          b.href = target.slice(1);
          b.title = 'Switch to English';
          b.setAttribute('aria-label','Switch to English');
          b.style.display = '';
        }
      }
    };
    if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f);
    else f();
  }
})();
