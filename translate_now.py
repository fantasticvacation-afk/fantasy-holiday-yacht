#!/usr/bin/env python3
# translate_now.py - 使用正确的 Google Translate URL

import json
import urllib.parse
import urllib.request
import time

INPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json'
OUTPUT = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json'
PROGRESS = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

def translate_text(text):
    """使用 Google Translate 免费 API 翻译"""
    try:
        encoded = urllib.parse.quote(text)
        url = f'https://translate.google.com/translate_a/single?client=gtx&sl=zh-CN&tl=en&dt=t&q={encoded}'
        
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result[0][0][0]
    except Exception as e:
        print(f'    ✗ 失败: {e}')
        return None

def main():
    print('\n=== 开始翻译 (使用正确的 API) ===')
    
    # 读取未翻译条目
    with open(INPUT, 'r', encoding='utf-8') as f:
        untranslated = json.load(f)
    
    print(f'总数: {len(untranslated)} 条')
    
    # 读取进度
    try:
        with open(PROGRESS, 'r', encoding='utf-8') as f:
            translations = json.load(f)
        print(f'发现进度: {len(translations)} 条已翻译\n')
    except FileNotFoundError:
        translations = {}
        print('从头开始\n')
    
    # 过滤已翻译
    remaining = [e for e in untranslated if e['key'] not in translations]
    print(f'剩余: {len(remaining)} 条\n')
    
    if len(remaining) == 0:
        print('✅ 所有条目已翻译！')
        return
    
    # 逐条翻译
    for i, entry in enumerate(remaining):
        key = entry['key']
        zh = entry['zh']
        
        print(f'[{i+1}/{len(remaining)}] {key}: {zh[:30]}...')
        
        en = translate_text(zh)
        
        if en:
            translations[key] = en
            print(f'  ✓ {en[:50]}')
            
            # 每 10 条保存一次
            if (i + 1) % 10 == 0:
                print(f'  保存进度... ({len(translations)}/{len(untranslated)})')
                with open(PROGRESS, 'w', encoding='utf-8') as f:
                    json.dump(translations, f, ensure_ascii=False, indent=2)
        else:
            translations[key] = zh  # 失败时保留中文
            print(f'  ✗ 使用原文')
        
        # 延迟（避免速率限制）
        if i < len(remaining) - 1:
            time.sleep(1)
    
    # 保存最终结果
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ 翻译完成！')
    print(f'  翻译了 {len(translations)} 条')
    print(f'  保存至: {OUTPUT}')
    
    # 删除进度文件
    try:
        import os
        os.remove(PROGRESS)
        print('✓ 进度文件已删除')
    except:
        pass

if __name__ == '__main__':
    main()
