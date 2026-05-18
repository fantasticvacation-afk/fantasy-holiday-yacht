#!/usr/bin/env python3
"""批量翻译剩余7342条 - 使用MyMemory API，分批处理"""
import json, time, sys, urllib.request, urllib.parse, re

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def translate_mymemory(text):
    """使用MyMemory API翻译"""
    if not text or not text.strip():
        return text
    try:
        encoded = urllib.parse.quote(text[:500])
        url = f'https://api.mymemory.translated.net/get?q={encoded}&langpair=zh-CN|en'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode('utf-8'))
            return data['responseData']['translatedText']
    except Exception as e:
        print(f'    ERR: {e}', file=sys.stderr)
        return None

def extract_untranslated_from_i18n():
    """从i18n.js提取未翻译条目"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取所有条目
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    # 筛选未翻译的（zh == en）
    untranslated = []
    for key, zh, en in entries:
        if zh == en or not en.strip():
            untranslated.append({'key': key, 'zh': zh})
    
    return untranslated

def apply_translations_to_i18n(translations):
    """将翻译应用到i18n.js"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for key, en in translations.items():
        if not en or en.strip() == '':
            continue
        # 转义特殊字符
        escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
        escaped_en = en.replace('\\', '\\\\').replace('"', '\\"')
        
        # 匹配并替换 en 字段
        pattern = rf'("{escaped_key}":\s*\{{\s*"zh":\s*"[^"]*",\s*"en":\s*")[^"]*(")'
        replacement = rf'\g<1>{escaped_en}\g<2>'
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            content = new_content
            count += 1
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

print('\n=== MyMemory 批量翻译 ===\n')

# 加载进度
try:
    with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
        translations = json.load(f)
    print(f'已翻译: {len(translations)} 条')
except:
    translations = {}

# 提取未翻译条目
untranslated = extract_untranslated_from_i18n()
print(f'未翻译: {len(untranslated)} 条')

# 筛选待翻译
remaining = [e for e in untranslated if e['key'] not in translations]
print(f'待处理: {len(remaining)} 条\n')

if not remaining:
    print('全部完成!')
    sys.exit(0)

# 分批处理，每批100条
BATCH_SIZE = 100
total_batches = (len(remaining) + BATCH_SIZE - 1) // BATCH_SIZE

print(f'分 {total_batches} 批处理，每批 {BATCH_SIZE} 条\n')

start_time = time.time()
for batch_num in range(total_batches):
    start_idx = batch_num * BATCH_SIZE
    end_idx = min(start_idx + BATCH_SIZE, len(remaining))
    batch = remaining[start_idx:end_idx]
    
    print(f'\n=== 批次 {batch_num + 1}/{total_batches} ({start_idx + 1}-{end_idx}) ===')
    
    for i, entry in enumerate(batch):
        key = entry['key']
        zh = entry['zh']
        
        if key in translations:
            continue
        
        en = translate_mymemory(zh)
        if en and en.strip():
            translations[key] = en.strip()
            print(f'[{start_idx + i + 1}/{len(remaining)}] ✓ {en[:50]}...')
        else:
            translations[key] = zh  # 保留原文
            print(f'[{start_idx + i + 1}/{len(remaining)}] ✗ 保留原文')
        
        time.sleep(0.5)  # 避免速率限制
    
    # 每批后保存进度
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    elapsed = time.time() - start_time
    rate = len(translations) / elapsed * 60 if elapsed > 0 else 0
    print(f'\n保存进度 | 已翻译: {len(translations)} | 速度: {rate:.0f}/min')

# 应用所有翻译到i18n.js
print('\n=== 应用翻译到 i18n.js ===')
count = apply_translations_to_i18n(translations)
print(f'应用了 {count} 条翻译')

# 验证语法
import subprocess
r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
print(f'语法检查: {r.stdout.strip() or r.stderr.strip() or "OK"}')

print(f'\n✅ 完成! 翻译了 {len(translations)} 条')