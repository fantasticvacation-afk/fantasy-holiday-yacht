import os, re, glob

# 要注入的搜索建议项点击事件代码
SUGGESTION_JS = """window.addEventListener("DOMContentLoaded",function(){document.querySelectorAll(".search-suggestion-item").forEach(function(el){el.addEventListener("click",function(){var t=this.textContent.trim();if(t.indexOf("全系")!==-1||t.indexOf("All Yachts")!==-1)window.location.href="yachts.html";else if(t.indexOf("定制")!==-1||t.indexOf("Custom")!==-1)window.location.href="custom.html";else if(t.indexOf("航线")!==-1||t.indexOf("Routes")!==-1)window.location.href="charter.html";else if(t.indexOf("联系")!==-1||t.indexOf("Contact")!==-1||t.indexOf("顾问")!==-1||t.indexOf("Advisor")!==-1)window.location.href="contact.html"})})});"""

files = glob.glob('*.html')
updated = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    
    # 检查是否已有搜索建议事件（避免重复）
    if 'search-suggestion-item' in content and 'suggestion-item").forEach' not in content:
        # 在最后一个 </script> 标签前（即 i18n.js 引用前的 script 结束标签）插入
        # 找到内联 script 的结束位置: </script>\n<script src="i18n.js">
        pattern = r'(window\.addEventListener\("DOMContentLoaded",function\(\)\{var isDark=localStorage[^<]*\}\);)</script>'
        match = re.search(pattern, content)
        if match:
            new_content = content[:match.end(1)] + SUGGESTION_JS + '</script>' + content[match.end(1)+len('</script>'):]
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(new_content)
            updated += 1
            print(f"✓ 已更新: {f}")
        else:
            print(f"⚠ 未匹配到script模式: {f}")
    elif 'search-suggestion-item' in content:
        print(f"  已有事件: {f}")

print(f"\n完成! 更新了 {updated} 个文件")
