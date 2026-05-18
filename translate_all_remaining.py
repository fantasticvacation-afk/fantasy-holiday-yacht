#!/usr/bin/env python3
# translate_all_remaining.py
# 翻译 i18n.js 中所有未翻译的条目（zh == en）
# 使用 deep-translator (GoogleTranslator)
# 支持断点续传

import json
import re
import sys
import time
from deep_translator import GoogleTranslator

# 配置
BATCH_SIZE = 100  # 每批翻译数量
DELAY_BETWEEN_BATCHES = 3  # 批次间延迟（秒）

# 文件路径
I18N_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n.js'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/i18n_progress.json'

def read_i18n():
    """读取 i18n.js，提取所有条目"""
    with open(I18N_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 正则提取所有条目
    pattern = r'"([^"]+)":\s*\{\s*"zh":\s*"([^"]*)",\s*"en":\s*"([^"]*)"\s*\}'
    entries = []
    for match in re.finditer(pattern, content):
        key = match.group(1)
        zh = match.group(2)
        en = match.group(3)
        entries.append({
            'key': key,
            'zh': zh,
            'en': en,
            'is_untranslated': zh == en and zh != ''
        })
    
    return content, entries

def read_progress():
    """读取进度文件"""
    try:
        with open(PROGRESS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_progress(translated_dict):
    """保存进度"""
    with open(PROGRESS_PATH, 'w', encoding='utf-8') as f:
        json.dump(translated_dict, f, ensure_ascii=False, indent=2)

def translate_batch(texts, keys):
    """批量翻译"""
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
        translations = translator.translate_batch(texts)
        return dict(zip(keys, translations))
    except Exception as e:
        print(f"✗ 批次翻译失败: {e}", file=sys.stderr)
        return None

def update_i18n_file(content, entries, translated_dict):
    """更新 i18n.js 文件"""
    for entry in entries:
        key = entry['key']
        if key in translated_dict:
            zh = entry['zh']
            en = translated_dict[key]
            old_entry = f'"{key}": {{ "zh": "{zh}", "en": "{zh}" }}'
            new_entry = f'"{key}": {{ "zh": "{zh}", "en": "{en}" }}'
            content = content.replace(old_entry, new_entry)
    
    with open(I18N_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ 已更新 i18n.js ({len(translated_dict)} 条)")

def main():
    print('\n=== i18n 批量翻译 ===')
    
    # 读取 i18n.js
    content, entries = read_i18n()
    
    untranslated = [e for e in entries if e['is_untranslated']]
    print(f'总条目数: {len(entries)}')
    print(f'未翻译: {len(untranslated)}')
    print(f'已翻译: {len(entries) - len(untranslated)}')
    
    if len(untranslated) == 0:
        print('\n✅ 所有条目已翻译！')
        return
    
    # 读取进度
    translated_dict = read_progress()
    if translated_dict:
        print(f'\n发现进度文件，已翻译: {len(translated_dict)} 条')
    
    # 过滤掉已翻译的
    remaining = [e for e in untranslated if e['key'] not in translated_dict]
    print(f'剩余待翻译: {len(remaining)} 条')
    
    if len(remaining) == 0:
        print('\n✅ 所有条目已从进度文件恢复！')
        update_i18n_file(content, entries, translated_dict)
        return
    
    # 分批翻译
    batches = [remaining[i:i + BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
    print(f'\n总批次数: {len(batches)}')
    print(f'批次大小: {BATCH_SIZE}')
    print(f'预计时间: ~{len(batches) * DELAY_BETWEEN_BATCHES / 60:.1f} 分钟\n')
    
    for i, batch in enumerate(batches):
        print(f'[批次 {i+1}/{len(batches)}] 翻译 {len(batch)} 条...')
        
        texts = [e['zh'] for e in batch]
        keys = [e['key'] for e in batch]
        
        results = translate_batch(texts, keys)
        
        if results:
            translated_dict.update(results)
            print(f'  ✓ 完成 {len(results)} 条 (总计: {len(translated_dict)})')
            
            # 保存进度
            save_progress(translated_dict)
            
            # 批次间延迟
            if i < len(batches) - 1:
                print(f'  等待 {DELAY_BETWEEN_BATCHES} 秒...')
                time.sleep(DELAY_BETWEEN_BATCHES)
        else:
            print(f'  ✗ 批次失败，保存进度并继续...')
            save_progress(translated_dict)
    
    # 最终保存
    print('\n=== 更新 i18n.js ===')
    update_i18n_file(content, entries, translated_dict)
    
    # 删除进度文件
    try:
        import os
        os.remove(PROGRESS_PATH)
        print('✓ 进度文件已删除')
    except:
        pass
    
    print('\n✅ 翻译完成！')
    print(f'  翻译了 {len(translated_dict)} 条')
    print(f'  保存至: {I18N_PATH}')

if __name__ == '__main__':
    main()
