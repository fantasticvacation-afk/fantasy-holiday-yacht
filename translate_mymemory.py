#!/usr/bin/env python3
"""使用 MyMemory API 翻译 - 免费无限制"""
import json, time, sys, urllib.request, urllib.parse

INPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json'
PROGRESS = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'
OUTPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json'

def translate(text):
    try:
        encoded = urllib.parse.quote(text[:500])
        url = f'https://api.mymemory.translated.net/get?q={encoded}&langpair=zh-CN|en'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read().decode('utf-8'))
            return data['responseData']['translatedText']
    except Exception as e:
        print(f'    ERR: {e}', file=sys.stderr)
    return None

print('\n=== MyMemory 翻译 7342 条 ===\n')
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
    if en and en.strip():
        translations[e['key']] = en.strip()
        print(f'[{i+1}/{len(remaining)}] ✓ {en[:55]}')
    else:
        translations[e['key']] = e['zh']
        print(f'[{i+1}/{len(remaining)}] ✗ 原文')

    if (i+1) % 50 == 0:
        with open(PROGRESS, 'w') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
        elapsed = time.time() - start
        rate = (i+1) / elapsed * 60
        eta = (len(remaining) - i - 1) / rate if rate > 0 else 999
        print(f'  保存 | 速度: {rate:.0f}/min | 剩余: ~{eta:.0f}min\n')

    time.sleep(0.3)

with open(OUTPUT, 'w') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)
with open(PROGRESS, 'w') as f:
    json.dump(translations, f, ensure_ascii=False, indent=2)
print(f'\n✅ 完成! 翻译了 {len(translations)} 条')