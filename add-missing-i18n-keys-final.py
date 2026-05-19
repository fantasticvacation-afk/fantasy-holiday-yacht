#!/usr/bin/env python3
"""
添加缺失的 i18n 键到 i18n.js - 修复版
"""

import re
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

print("📝 检查缺失的 i18n 键...")

# 读取 i18n.js
i18n_file = BASE_DIR / "i18n.js"
i18n_content = i18n_file.read_text(encoding='utf-8')

# 提取所有定义的键 - 改进正则表达式
defined_keys = set()
for match in re.finditer(r'"([^"]+)":\s*\{', i18n_content):
    key = match.group(1)
    # 确保这是字典键（不是嵌套对象）
    prev_char_pos = match.start() - 1
    if prev_char_pos >= 0 and i18n_content[prev_char_pos] in ['\n', ' ', ',', '{']:
        defined_keys.add(key)

print(f"i18n.js 中已定义 {len(defined_keys)} 个键")

# 检查所有 HTML 文件中使用的键
html_files = [f for f in BASE_DIR.glob("*.html") if f.name not in ['nav-template.html', 'footer-template.html']]

missing_keys = set()
used_keys_with_text = {}

for html_file in html_files:
    content = html_file.read_text(encoding='utf-8')

    # 提取所有 data-i18n 属性
    for match in re.finditer(r'data-i18n="([^"]+)"', content):
        key = match.group(1)
        if key not in defined_keys:
            missing_keys.add(key)

            # 尝试提取对应的文本
            # 查找这个属性之后的内容
            next_part = content[match.end():match.end()+200]
            text_match = re.search(r'[^>]*>([^<]+)<', next_part)
            if text_match:
                text = text_match.group(1).strip()
                if text and key not in used_keys_with_text:
                    used_keys_with_text[key] = text

print(f"发现 {len(missing_keys)} 个缺失的键")

if not missing_keys:
    print("✅ 没有缺失的键！")
    exit(0)

# 找到字典结束位置
lines = i18n_content.split('\n')
dict_end_line = None
for i, line in enumerate(lines):
    if line.strip() == '};' and i > 76000:  # 在字典结束附近
        dict_end_line = i
        break

if dict_end_line is None:
    print("❌ 无法找到字典结束位置")
    exit(1)

print(f"字典结束行: {dict_end_line + 1}")

# 生成需要添加的键值对
new_lines = []
for key in sorted(missing_keys):
    text = used_keys_with_text.get(key, key.split('.')[-1])

    # 转义引号和特殊字符
    text_escaped = text.replace('\\', '\\\\').replace('"', '\\"')

    new_lines.append(f'  "{key}": {{ "zh": "{text_escaped}", "en": "{text_escaped}" }},')

print(f"需要添加 {len(new_lines)} 个键")

# 找到最后一个键的行（在 }; 之前）
last_key_line = dict_end_line - 1

# 确保最后一行有逗号
lines[last_key_line] = lines[last_key_line].rstrip()
if not lines[last_key_line].endswith(','):
    lines[last_key_line] += ','

# 插入新键
for i, new_line in enumerate(new_lines):
    lines.insert(last_key_line + 1 + i, new_line)

# 写回文件
i18n_file.write_text('\n'.join(lines), encoding='utf-8')
print(f"✅ 已添加 {len(new_lines)} 个键到 i18n.js")
