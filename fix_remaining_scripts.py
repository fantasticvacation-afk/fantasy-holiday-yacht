import os, re, glob

# 完整的内联JS（从index.html提取的标准版本）
FULL_INLINE_JS = '''<script>
window.addEventListener("DOMContentLoaded",function(){
var loader=document.getElementById("loader");
if(!loader)return;
var progressEl=document.getElementById("progress");
var progress=0;
var interval=setInterval(function(){progress+=Math.random()*12+8;if(progress>=100){progress=100;clearInterval(interval);if(progressEl)progressEl.style.width="100%";setTimeout(function(){if(loader)loader.style.display="none";document.body.style.overflow=""},400)}else if(progressEl)progressEl.style.width=progress+"%"},180);
setTimeout(function(){clearInterval(interval);if(loader)loader.style.display="none";document.body.style.overflow=""},5000);
});
window.addEventListener("scroll",function(){var nav=document.getElementById("navbar");if(window.scrollY>50)nav.classList.add("scrolled");else nav.classList.remove("scrolled")});
function toggleMobile(){document.getElementById("mobile-menu").classList.toggle("active");document.querySelector(".hamburger").classList.toggle("active")}
(function(){var c=document.getElementById("cursor");if(c)document.addEventListener("mousemove",function(e){c.style.left=e.pageX+"px";c.style.top=e.pageY+"px"})})();
(function(){var o=new IntersectionObserver(function(e){e.forEach(function(e){if(e.isIntersecting)e.target.classList.add("revealed")})},{threshold:0.1});document.querySelectorAll(".reveal,.reveal-left,.reveal-right,.reveal-scale").forEach(function(e){o.observe(e)})})();

function toggleSearch(){var s=document.getElementById("searchOverlay");if(s){s.classList.toggle("active");if(s.classList.contains("active")){setTimeout(function(){var i=document.getElementById("searchInput");if(i)i.focus()},100)}}}
document.addEventListener("keydown",function(e){if(e.key==="Escape"){var s=document.getElementById("searchOverlay");if(s&&s.classList.contains("active"))s.classList.remove("active");var m=document.getElementById("mobile-menu");if(m&&m.classList.contains("active")){m.classList.remove("active");var h=document.querySelector(".hamburger");if(h)h.classList.remove("active")}}});function toggleDarkMode(){document.body.classList.toggle("dark-mode");var isDark=document.body.classList.contains("dark-mode");localStorage.setItem("fv-dark",isDark?"1":"0");var moon=document.querySelector(".icon-moon");var sun=document.querySelector(".icon-sun");if(moon)moon.style.display=isDark?"none":"inline";if(sun)sun.style.display=isDark?"inline":"none"}
window.addEventListener("DOMContentLoaded",function(){var isDark=localStorage.getItem("fv-dark")==="1";if(isDark){document.body.classList.add("dark-mode");var moon=document.querySelector(".icon-moon");var sun=document.querySelector(".icon-sun");if(moon)moon.style.display="none";if(sun)sun.style.display="inline"}});window.addEventListener("DOMContentLoaded",function(){document.querySelectorAll(".search-suggestion-item").forEach(function(el){el.addEventListener("click",function(){var t=this.textContent.trim();if(t.indexOf("全系")!==-1||t.indexOf("All Yachts")!==-1)window.location.href="yachts.html";else if(t.indexOf("定制")!==-1||t.indexOf("Custom")!==-1)window.location.href="custom.html";else if(t.indexOf("航线")!==-1||t.indexOf("Routes")!==-1)window.location.href="charter.html";else if(t.indexOf("联系")!==-1||t.indexOf("Contact")!==-1||t.indexOf("顾问")!==-1||t.indexOf("Advisor")!==-1)window.location.href="contact.html"})})});</script>'''

files = glob.glob('*.html')
fixed = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # 检查是否有搜索建议项但缺少toggleSearch
    has_suggestions = 'search-suggestion-item' in content
    has_toggle_search = 'function toggleSearch' in content
    
    if has_suggestions and not has_toggle_search:
        # 在 </body> 前插入完整脚本
        # 找到 i18n.js 引用的位置，在它前面插入
        if '<script src="i18n.js"></script>' in content:
            new_content = content.replace(
                '<script src="i18n.js"></script>',
                FULL_INLINE_JS + '\n<script src="i18n.js"></script>'
            )
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            fixed += 1
            print(f"✓ 已修复: {f}")
        else:
            print(f"⚠ 无i18n引用: {f}")

print(f"\n完成! 修复了 {fixed} 个文件")
