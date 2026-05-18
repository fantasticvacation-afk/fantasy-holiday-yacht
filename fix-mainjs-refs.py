#!/usr/bin/env python3
"""给所有 HTML 添加 main.js 引用，并修复损坏的 HTML 标签"""
import os
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html') and os.path.isfile(f)]
updated = 0
fixed_html = 0

for fname in html_files:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. 修复损坏的 HTML 标签
    content = content.replace('<div <="" div="">', '<div></div>')

    # 2. 如果没有 main.js 引用，添加它（在 </body> 之前）
    if 'main.js' not in content:
        # 在 </body> 前插入
        content = re.sub(
            r'(</body>)',
            r'<script src="main.js"></script>\n\1',
            content
        )
        updated += 1

    # 如果有修改
    if content != original:
        fixed_html += 1
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ 已修复: {fname}")
    else:
        print(f"  无变化: {fname}")

print(f"\n完成！添加了 {updated} 个文件的 main.js 引用，修复了 {fixed_html} 个文件")
