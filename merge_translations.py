#!/usr/bin/env python3
"""将 translations.json 合并到 i18n.js"""
import json, re, sys

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
TRANS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json'

print('=== 合并翻译到 i18n.js ===\n')

with open(TRANS_PATH) as f:
    translations = json.load(f)
print(f'翻译条目: {len(translations)}')

with open(I18N_PATH) as f:
    content = f.read()

count = 0
for key, en in translations.items():
    # Escape key for regex
    escaped = key.replace('\\', '\\\\').replace('"', '\\"')
    # Pattern: "key": { "zh": "...", "en": "..." }
    pattern = rf'("{escaped}":\s*\{{[^}}]*?"zh":\s*")[^"]*?(",\s*"en":\s*")[^"]*?("\s*}})'
    replacement = rf'\g<1>{en}\g<2>{en}\g<3>'
    new_content, n = re.subn(pattern, replacement, content)
    if n > 0:
        content = new_content
        count += 1
    else:
        print(f'  ⚠ 未找到: {key}')

print(f'\n已更新: {count} 条')

with open(I18N_PATH, 'w') as f:
    f.write(content)
print(f'保存至: {I18N_PATH}')

# Verify syntax
import subprocess
r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
print(f'\n语法检查: {r.stdout.strip() or r.stderr.strip() or "OK"}')