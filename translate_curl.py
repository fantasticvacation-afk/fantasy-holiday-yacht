#!/usr/bin/env python3
"""翻译剩余 7342 条目，使用 curl 调用 Google Translate API"""
import json, subprocess, time, sys

INPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json'
PROGRESS = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'
OUTPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json'

def translate(text):
    try:
        url = f'https://translate.google.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={text}'
        r = subprocess.run(['curl', '-s', '-A', 'Mozilla/5.0', url], capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            data = json.loads(r.stdout)
            return data[0][0][0]
    except Exception as e:
        print(f'    ERR: {e}', file=sys.stderr)
    return None

print('\n=== 开始翻译 7342 条 ===\n')
with open(INPUT) as f:
    untranslated = json.load(f)
print(f'总数: {len(untranslated)}')

try:
    with open(PROGRESS) as f:
        translations = json.load(f)
    print(f'已翻: {len(translations)}')
except:
    translations = {}

remaining = [e for e in untranslated if e['key'] not in translations]
print(f'剩余: {len(remaining)}\n')

if not remaining:
    print('全部完成')
    sys.exit(0)

start = time.time()
for i, e in enumerate(remaining):
    en = translate(e['zh'])
    if en:
        translations[e['key']] = en
        print(f'[{i+1}/{len(remaining)}] ✓ {en[:50]}')
    else:
        translations[e['key']] = e['zh']
        print(f'[{i+1}/{len(remaining)}] ✗ 原文')
    
    if (i+1) % 20 == 0:
        with open(PROGRESS, 'w') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        elapsed = time.time() - start
        rate = (i+1) / elapsed * 60
        eta = (len(remaining) - i - 1) / rate
        print(f'  进度保存 | 速度: {rate:.1f}/min | 预计剩余: {eta:.0f}min\n')
    
    time.sleep(1.1)

with open(OUTPUT, 'w') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)
with open(PROGRESS, 'w') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)
print(f'\n✅ 完成! 翻译了 {len(translations)} 条')