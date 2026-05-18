import os
import re

# 读取新导航模板
with open('nav-template.html', 'r', encoding='utf-8') as f:
    new_nav = f.read().strip()

# 新导航的 JS 引用（插入到 </body> 前）
i18n_script = '<script src="i18n.js"></script>\n</body>'

html_files = [f for f in os.listdir('.') if f.endswith('.html')]
updated = 0
skipped = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. 替换 <nav id="navbar">...</nav>
    # 匹配从 <nav id="navbar"> 到第一个 </nav> 的内容
    nav_pattern = r'<nav id="navbar">[\s\S]*?</nav>\s*</nav>'
    # 更安全的匹配：匹配到 </nav> 后的空白，然后直到移动端菜单前
    nav_replacement = '<nav id="navbar">\n' + new_nav + '\n</nav>'
    
    # 实际上 nav-template.html 已经是完整 <nav> 标签内容，直接替换
    # 找到旧 nav 并替换
    old_nav_match = re.search(r'<nav id="navbar">[\s\S]*?</nav>', content)
    if old_nav_match:
        content = content[:old_nav_match.start()] + '<nav id="navbar">\n' + new_nav + '\n</nav>' + content[old_nav_match.end():]
    else:
        print(f"  ⚠ 未找到导航栏: {fname}")
        skipped += 1
        continue
    
    # 2. 添加 i18n.js 引用（如果还没有）
    if 'i18n.js' not in content:
        content = content.replace('</body>', i18n_script, 1)
    
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        updated += 1
    else:
        skipped += 1

print(f"✓ 更新完成: {updated} 个文件已更新, {skipped} 个跳过")
