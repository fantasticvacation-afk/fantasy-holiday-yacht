/* main.js - 奇幻假期游艇网站主逻辑 */

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

/* === 搜索框切换 === */
function toggleSearch() {
  var overlay = document.getElementById("searchOverlay");
  if (!overlay) return;
  overlay.classList.toggle("active");
  if (overlay.classList.contains("active")) {
    setTimeout(function() {
      var input = document.getElementById("searchInput");
      if (input) input.focus();
    }, 100);
  }
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
  var name = document.getElementById("custom_name");
  var phone = document.getElementById("custom_phone");
  var series = document.getElementById("custom_series");

  if (!name || !name.value.trim()) { alert("请输入您的姓名"); name && name.focus(); return false; }
  if (!phone || !phone.value.trim()) { alert("请输入您的联系电话"); phone && phone.focus(); return false; }
  var phoneVal = phone.value.trim();
  if (!/^[\d\s\-+()（）]{7,20}$/.test(phoneVal)) { alert("请输入有效的联系电话"); phone.focus(); return false; }
  if (series && !series.value.trim()) { alert("请选择感兴趣的船型系列"); series.focus(); return false; }

  var btn = form.querySelector("button[type=submit]");
  var orig = btn.textContent;
  btn.textContent = "⏳ 提交中...";
  btn.disabled = true;

  var data = new FormData(form);
  fetch(form.action, { method: "POST", body: data, headers: { "Accept": "application/json" } })
    .then(function(r) {
      if (r.ok) {
        alert("✅ 定制咨询已提交成功！我们的顾问将在24小时内与您联系。");
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
