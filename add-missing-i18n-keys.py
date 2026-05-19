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
i18n_content = i18n_file.read_text(encoding='utf-8')

# 提取所有定义的键
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
        if key not in defined_keys:
            missing_keys[key].append(html_file.name)
            if key not in used_keys_with_text:
                used_keys_with_text[key] = text

print(f"发现 {len(missing_keys)} 个缺失的键")

# 生成需要添加的键值对
new_entries = []
for key in sorted(missing_keys.keys()):
    text = used_keys_with_text.get(key, key.split('.')[-1])

    # 检查是否是中文
    is_chinese = any('\u4e00' <= c <= '\u9fff' for c in text)

    if is_chinese:
        new_entries.append(f'  "{key}": {{ "zh": "{text}", "en": "{text}" }}')
    else:
        new_entries.append(f'  "{key}": {{ "zh": "{text}", "en": "{text}" }}')

print(f"\n需要添加 {len(new_entries)} 个键")

# 找到 i18n.js 中字典的结束位置（最后一个键之后）
dict_end_match = re.search(r'\}\s*;?\s*//.*?字典结束', i18n_content)
if not dict_end_match:
    # 尝试找到最后一个键
    dict_end_match = re.search(r'\}\s*\};?\s*$', i18n_content)

if dict_end_match:
    insert_pos = dict_end_match.start()

    # 构建新内容
    new_content = ',\n'.join(new_entries)
    insertion = ',\n' + new_content + '\n'

    # 插入新键
    updated_content = i18n_content[:insert_pos] + insertion + i18n_content[insert_pos:]

    # 写回文件
    i18n_file.write_text(updated_content, encoding='utf-8')
    print(f"✅ 已添加 {len(new_entries)} 个键到 i18n.js")
else:
    print("❌ 无法找到字典结束位置")
