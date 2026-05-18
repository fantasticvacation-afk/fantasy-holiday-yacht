#!/usr/bin/env python3
# translate_untranslated.py
# 读取 untranslated.json，批量翻译，保存结果

import json
import time
from deep_translator import GoogleTranslator

INPUT_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/untranslated.json'
OUTPUT_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translations.json'
PROGRESS_PATH = '/Users/hs/.qclaw/workspace/fh-yacht-site/translation_progress.json'

BATCH_SIZE = 50  # 每批翻译数量
DELAY = 2  # 批次间延迟（秒）

def read_progress():
    try:
        with open(PROGRESS_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_progress(translations):
    with open(PROGRESS_PATH, 'w') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)

def translate_batch(texts, keys):
    try:
        translator = GoogleTranslator(source='zh-CN', target='en')
        results = translator.translate_batch(texts)
        return dict(zip(keys, results))
    except Exception as e:
        print(f"✗ 批次翻译失败: {e}")
        return None

def main():
    print('\n=== 开始批量翻译 ===')
    
    # 读取未翻译条目
    with open(INPUT_PATH, 'r') as f:
        untranslated = json.load(f)
    
    print(f'待翻译: {len(untranslated)} 条')
    
    # 读取进度
    translations = read_progress()
    if translations:
        print(f'发现进度文件，已完成: {len(translations)} 条')
    
    # 过滤掉已翻译的
    remaining = [e for e in untranslated if e['key'] not in translations]
    print(f'剩余: {len(remaining)} 条\n')
    
    if len(remaining) == 0:
        print('✅ 所有条目已翻译！')
        return
    
    # 分批翻译
    batches = [remaining[i:i + BATCH_SIZE] for i in range(0, len(remaining), BATCH_SIZE)]
    print(f'总批次数: {len(batches)}')
    print(f'批次大小: {BATCH_SIZE}')
    print(f'预计时间: ~{len(batches) * DELAY / 60:.1f} 分钟\n')
    
    for i, batch in enumerate(batches):
        print(f'[批次 {i+1}/{len(batches)}] 翻译 {len(batch)} 条...')
        
        texts = [e['zh'] for e in batch]
        keys = [e['key'] for e in batch]
        
        results = translate_batch(texts, keys)
        
        if results:
            translations.update(results)
            print(f'  ✓ 完成 {len(results)} 条 (总计: {len(translations)})')
            
            # 保存进度
            save_progress(translations)
            
            # 批次间延迟
            if i < len(batches) - 1:
                print(f'  等待 {DELAY} 秒...')
                time.sleep(DELAY)
        else:
            print(f'  ✗ 批次失败，保存进度并继续...')
            save_progress(translations)
    
    # 保存最终结果
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    
    print(f'\n✅ 翻译完成！')
    print(f'  翻译了 {len(translations)} 条')
    print(f'  保存至: {OUTPUT_PATH}')
    
    # 删除进度文件
    try:
        import os
        os.remove(PROGRESS_PATH)
        print('✓ 进度文件已删除')
    except:
        pass

if __name__ == '__main__':
    main()
