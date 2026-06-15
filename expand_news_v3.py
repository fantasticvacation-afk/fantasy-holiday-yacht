#!/usr/bin/env python3
"""
扩写10篇新闻详情页内容。
策略：替换现有段落的文本内容为完整长文，同时在i18n.js中更新对应条目。
"""
import re, os, json, shutil

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# 读取内容
with open(os.path.join(BASE, 'news_expansion_content.json'), encoding='utf-8') as f:
    EXPANSION = json.load(f)

def expand_news_page(num_str, data):
    """扩写单个新闻页面：替换现有短段落为长段落"""
    fname = os.path.join(BASE, f'news-{num_str}.html')
    with open(fname, encoding='utf-8') as f:
        content = f.read()
    
    zh_paragraphs = data['zh']
    en_paragraphs = data['en']
    
    # 找到news-article-body区域
    body_start = content.find('news-article-body')
    if body_start < 0:
        print(f"  SKIP {num_str}: no news-article-body")
        return []
    
    article_end = content.find('</article>', body_start)
    body_region = content[body_start:article_end]
    
    # 找到所有现有的 data-i18n="news-XXX.YYY" 段落
    existing_keys = re.findall(r'data-i18n="(news-' + num_str + r'\.\d+)"', body_region)
    
    if not existing_keys:
        print(f"  SKIP {num_str}: no i18n keys found")
        return []
    
    # 策略：保留第一个段落（简介），替换其余段落，追加新段落
    # 第一个段落用第一段新内容替换，其余段落依次替换
    
    new_entries = []
    last_key_num = int(existing_keys[-1].split('.')[1])
    first_key = existing_keys[0]
    
    # 替换现有段落内容
    for i, key in enumerate(existing_keys):
        if i < len(zh_paragraphs):
            zh_text = zh_paragraphs[i]
            en_text = en_paragraphs[i] if i < len(en_paragraphs) else zh_text
            
            # 替换段落内的文本
            pattern = f'({re.escape(key)}">)([^<]+)(</p>)'
            match = re.search(pattern, content)
            if match:
                content = content[:match.start(2)] + zh_text + content[match.end(2):]
                new_entries.append((key, zh_text, en_text))
    
    # 如果新段落多于现有段落，在</article>前追加
    if len(zh_paragraphs) > len(existing_keys):
        insert_point = content.find('</article>', body_start)
        div_close = content.rfind('</div>', body_start, insert_point)
        
        extra_html = ""
        for i in range(len(existing_keys), len(zh_paragraphs)):
            key_num = last_key_num + (i - len(existing_keys)) + 1
            key = f"news-{num_str}.{key_num}"
            zh_text = zh_paragraphs[i]
            en_text = en_paragraphs[i] if i < len(en_paragraphs) else zh_text
            
            extra_html += f'\n<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-bottom:20px" data-i18n="{key}">{zh_text}</p>'
            new_entries.append((key, zh_text, en_text))
        
        content = content[:div_close] + extra_html + '\n' + content[div_close:]
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ news-{num_str}.html: {len(new_entries)} entries updated/added")
    return new_entries


def update_i18n(entries, i18n_path):
    """更新i18n.js文件"""
    with open(i18n_path, encoding='utf-8') as f:
        content = f.read()
    
    updated = 0
    added = 0
    
    for key, zh_text, en_text in entries:
        zh_escaped = zh_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_escaped = en_text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        # 检查key是否已存在
        pattern = f'"{key}"\\s*:\\s*\\{{'
        if re.search(pattern, content):
            # 更新现有条目 - 替换zh和en的值
            # 找到key对应的整个条目
            key_pos = content.find(f'"{key}"')
            if key_pos >= 0:
                # 找到这个条目的zh值
                zh_match = re.search(f'"{key}"\\s*:\\s*\\{{\\s*"zh"\\s*:\\s*"[^"]*"', content[key_pos:key_pos+50000])
                if zh_match:
                    old_zh_start = key_pos + zh_match.start()
                    old_zh_end = key_pos + zh_match.end()
                    content = content[:old_zh_start] + f'"{key}": {{"zh": "{zh_escaped}"' + content[old_zh_end:]
                
                # 替换en值
                key_pos = content.find(f'"{key}"')
                en_match = re.search(f'"en"\\s*:\\s*"[^"]*"', content[key_pos:key_pos+50000])
                if en_match:
                    old_en_start = key_pos + en_match.start()
                    old_en_end = key_pos + en_match.end()
                    content = content[:old_en_start] + f'"en": "{en_escaped}"' + content[old_en_end:]
                
                updated += 1
        else:
            # 添加新条目 - 在最后一个news条目后添加
            last_news = None
            for m in re.finditer(r'"news-\d+\.\d+"\s*:\s*\{[^}]*\}', content):
                last_news = m
            
            if last_news:
                entry_str = f',\n  "{key}": {{"zh": "{zh_escaped}", "en": "{en_escaped}"}}'
                insert_pos = last_news.end()
                content = content[:insert_pos] + entry_str + content[insert_pos:]
                added += 1
    
    with open(i18n_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ {os.path.basename(i18n_path)}: {updated} updated, {added} added")


def main():
    print("🚀 开始扩写新闻详情页内容\n")
    
    for num_str, data in sorted(EXPANSION.items()):
        print(f"Processing news-{num_str}...")
        entries = expand_news_page(num_str, data)
        
        if entries:
            # 更新主 i18n.js
            update_i18n(entries, os.path.join(BASE, 'i18n.js'))
            # 更新 YT/i18n.js
            yt_i18n = os.path.join(BASE, 'YT', 'i18n.js')
            if os.path.exists(yt_i18n):
                update_i18n(entries, yt_i18n)
    
    # 同步HTML到其他语言版本
    print("\nSyncing HTML files...")
    for num_str in EXPANSION.keys():
        fname = f'news-{num_str}.html'
        for subdir in ['en', 'YT', 'YT/en']:
            dst = os.path.join(BASE, subdir, fname)
            if os.path.exists(dst):
                shutil.copy2(os.path.join(BASE, fname), dst)
                print(f"  ✓ {fname} → {subdir}/")
    
    print("\n✅ 完成！")

if __name__ == '__main__':
    main()
