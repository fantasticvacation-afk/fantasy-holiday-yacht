#!/usr/bin/env python3
"""
添加缺失的 i18n 键到 i18n.js
"""

import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

print("📝 检查缺失的 i18n 键...")

# 读取 i18n.js
i18n_file = BASE_DIR / "i18n.js"
lines = i18n_file.read_text(encoding='utf-8').split('\n')

# 提取所有定义的键
i18n_content = '\n'.join(lines)
defined_keys = set(re.findall(r'"([^"]+)":\s*{', i18n_content))
print(f"i18n.js 中已定义 {len(defined_keys)} 个键")

# 检查所有 HTML 文件中使用的键
html_files = [f for f in BASE_DIR.glob("*.html") if f.name not in ['nav-template.html', 'footer-template.html']]

missing_keys = defaultdict(list)
used_keys_with_text = {}

for html_file in html_files:
    content = html_file.read_text(encoding='utf-8')

    # 提取所有 data-i18n 属性及其对应的文本
    pattern = r'data-i18n="([^"]+)"[^>]*>([^<]+)<'
    matches = re.findall(pattern, content)

    for key, text in matches:
        text = text.strip()
        if key not in defined_keys and text:  # 确保文本非空
            missing_keys[key].append(html_file.name)
            if key not in used_keys_with_text:
                used_keys_with_text[key] = text

print(f"发现 {len(missing_keys)} 个缺失的键")

# 找到字典结束的行号（第 76659 行，索引 76658）
dict_end_line = 76658

# 生成需要添加的键值对
new_lines = []
for key in sorted(missing_keys.keys()):
    text = used_keys_with_text.get(key, key.split('.')[-1])

    # 检查是否是中文
    is_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)

    # 转义引号
    text_escaped = text.replace('"', '\\"')

    if is_chinese:
        new_lines.append(f'  "{key}": {{ "zh": "{text_escaped}", "en": "{text_escaped}" }},')
    else:
        new_lines.append(f'  "{key}": {{ "zh": "{text_escaped}", "en": "{text_escaped}" }},')

print(f"\n需要添加 {len(new_lines)} 个键")

# 在字典结束前插入新键
# 找到最后一行（不包含逗号的行）
last_key_line = dict_end_line - 1

# 在最后一行添加逗号
lines[last_key_line] = lines[last_key_line].rstrip()
if not lines[last_key_line].endswith(','):
    lines[last_key_line] += ','

# 插入新键（在最后一行之后，结束大括号之前）
for i, new_line in enumerate(new_lines):
    lines.insert(last_key_line + 1 + i, new_line)

# 写回文件
i18n_file.write_text('\n'.join(lines), encoding='utf-8')
print(f"✅ 已添加 {len(new_lines)} 个键到 i18n.js")
