#!/usr/bin/env python3
"""高效翻译脚本 - 处理未翻译条目"""
import json, time, sys, urllib.request, urllib.parse, re, subprocess

I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def translate_google(text):
    """Google Translate API"""
    if not text or not text.strip():
        return text
    try:
        encoded = urllib.parse.quote(text[:200])
        url = f'https://translate.google.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded}'
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode('utf-8'))
            return data[0][0][0] if data and data[0] else None
    except:
        return None

def smart_translate(text):
    """智能翻译：处理各种类型"""
    if not text or not text.strip():
        return text
    
    # 纯英文/数字/符号 - 保持原样
    if not any('\u4e00' <= c <= '\u9fff' for c in text):
        return text
    
    # 纯中文 - 翻译
    if all('\u4e00' <= c <= '\u9fff' or c in '，。！？、：；""''（）—…' or c.isspace() or c.isdigit() for c in text if c.strip()):
        return translate_google(text) or text
    
    # 中英混合 - 提取中文部分翻译
    return translate_google(text) or text

def extract_untranslated():
    """提取未翻译条目"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"'
    entries = re.findall(pattern, content)
    
    untranslated = []
    for key, zh, en in entries:
        if zh == en or not en.strip():
            # 检查是否需要翻译
            if any('\u4e00' <= c <= '\u9fff' for c in zh):
                untranslated.append({'key': key, 'zh': zh})
            else:
                # 纯英文，无需翻译
                pass
    
    return untranslated

def apply_translations(translations):
    """应用翻译到i18n.js"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    count = 0
    for key, en in translations.items():
        if not en:
            continue
        escaped_key = key.replace('\\', '\\\\').replace('"', '\\"')
        escaped_en = en.replace('\\', '\\\\').replace('"', '\\"')
        pattern = rf'("{escaped_key}":\s*\{{\s*"zh":\s*"[^"]*",\s*"en":\s*")[^"]*(")'
        replacement = rf'\g<1>{escaped_en}\g<2>'
        new_content, n = re.subn(pattern, replacement, content)
        if n > 0:
            content = new_content
            count += 1
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return count

print('\n=== 高效翻译 7342 条 ===\n')

# 加载进度
try:
    with open(PROGRESS_PATH) as f:
        progress = json.load(f)
except:
    progress = {}

untranslated = extract_untranslated()
print(f'需翻译: {len(untranslated)} 条')

remaining = [e for e in untranslated if e['key'] not in progress]
print(f'待处理: {len(remaining)} 条\n')

if not remaining:
    print('全部完成!')
    sys.exit(0)

# 处理
start = time.time()
for i, entry in enumerate(remaining):
    key = entry['key']
    zh = entry['zh']
    
    en = smart_translate(zh)
    progress[key] = en
    
    status = '✓' if en and en != zh else '○'
    print(f'[{i+1}/{len(remaining)}] {status} {zh[:25]} → {en[:25] if en else "N/A"}')
    
    if (i+1) % 50 == 0:
        with open(PROGRESS_PATH, 'w') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)
        elapsed = time.time() - start
        rate = (i+1) / elapsed * 60
        print(f'  保存 | {i+1}/{len(remaining)} | {rate:.0f}/min\n')
    
    time.sleep(0.8)

# 最终保存
with open(PROGRESS_PATH, 'w') as f:
    json.dump(progress, f, ensure_ascii=False, indent=2)

print('\n=== 应用翻译 ===')
count = apply_translations(progress)
print(f'应用: {count} 条')

# 验证
r = subprocess.run(['node', '-c', I18N_PATH], capture_output=True, text=True)
print(f'语法: {r.stdout.strip() or r.stderr.strip() or "OK"}')

print(f'\n✅ 完成! {len(progress)} 条')