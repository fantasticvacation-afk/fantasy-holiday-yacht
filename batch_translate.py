"""批量翻译 all_unique_texts.json 中的中文到英文"""
import json, time
from deep_translator import GoogleTranslator

with open('all_unique_texts.json', 'r', encoding='utf-8') as f:
    texts = json.load(f)

print(f"待翻译: {len(texts)} 条")

results = {}
batch_size = 50
translated = 0

for i in range(0, len(texts), batch_size):
    batch = texts[i:i+batch_size]
    # 过滤掉纯数字、符号、英文
    to_translate = []
    indices = []
    for j, t in enumerate(batch):
        if not t or t.strip() == '':
            continue
        # 跳过纯ASCII（已经是英文/数字）
        try:
            t.encode('ascii')
            results[t] = t  # 已经是英文，直接保留
        except UnicodeEncodeError:
            to_translate.append(t)
            indices.append(j)
    
    if not to_translate:
        print(f"  批次 {i//batch_size + 1}: 无需翻译 (已是英文/数字)")
        continue
    
    try:
        # 批量翻译
        translated_batch = GoogleTranslator(source='zh-cn', target='en').translate_batch(to_translate)
        for orig, en in zip(to_translate, translated_batch):
            results[orig] = en
            translated += 1
        print(f"  批次 {i//batch_size + 1}: 翻译 {len(to_translate)} 条")
        time.sleep(1)  # 避免 API 限流
    except Exception as e:
        print(f"  批次 {i//batch_size + 1} 失败: {e}")
        for orig in to_translate:
            results[orig] = orig  # 翻译失败，保留原文

# 保存结果
with open('all_unique_texts_en.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\n✓ 翻译完成！")
print(f"  总条数: {len(texts)}")
print(f"  已翻译: {translated}")
print(f"  跳过(已是英文): {len(texts) - translated - (len(texts) - len(results))}")
print(f"  结果: all_unique_texts_en.json")
