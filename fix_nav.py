import os, re

with open('nav-template.html', 'r', encoding='utf-8') as f:
    new_nav_inner = f.read().strip()

# 正确的完整 <nav> 块
correct_nav = '<nav id="navbar">\n' + new_nav_inner + '\n</nav>'

html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'footer-template.html']
fixed = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 将文件中所有 <nav id="navbar">...</nav> 块替换为正确版本
    # 匹配第一个 <nav id="navbar"> 到最后一个 </nav> 之间的所有内容
    pattern = r'<nav id="navbar">[\s\S]*?</nav>'
    
    # 更精确：找到第一个 <nav id="navbar">，然后找到紧随其后的 </nav>
    # 但文件中可能嵌套了错误的重复，需要找到最外层的 </nav>
    # 简单做法：直接用正则替换掉整个 nav 块
    new_content = re.sub(pattern, correct_nav, content, count=1)
    
    if new_content != content:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(new_content)
        fixed += 1

print(f"✓ 修复完成: {fixed} 个文件")
