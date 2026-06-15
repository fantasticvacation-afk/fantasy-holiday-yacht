#!/usr/bin/env python3
"""扩写新闻详情页内容 - 从JSON读取内容，修改HTML和i18n.js"""
import re, os, json, shutil

BASE = '/Users/stone/.qclaw/workspace/fantasy-holiday-yacht'

# Last i18n key for each news article (from current HTML)
LAST_KEYS = {
    "001": 907, "002": 915, "003": 922, "004": 929, "005": 936,
    "006": 944, "007": 951, "008": 957, "009": 964, "010": 973
}

def insert_paragraphs(num_str, zh_paragraphs, en_paragraphs):
    """在news-XXX.html的news-article-body末尾追加段落"""
    fname = os.path.join(BASE, f'news-{num_str}.html')
    with open(fname, encoding='utf-8') as f:
        content = f.read()
    
    # 找到 article-body 内最后一个 </p> 之后的位置
    # 寻找 </article> 标记
    article_close = content.find('</article>')
    if article_close < 0:
        print(f"  ERROR: no </article> in {fname}")
        return {}
    
    # 在 </article> 之前找到 news-article-body 的 </div>
    # 向前搜索 </div> 
    body_close = content.rfind('</div>', 0, article_close)
    
    start_key = LAST_KEYS[num_str] + 1  # 从下一个键开始
    
    new_html = ""
    new_entries = {}
    
    for i, (zh, en) in enumerate(zip(zh_paragraphs, en_paragraphs)):
        key_num = start_key + i
        key = f"news-{num_str}.{key_num}"
        
        # HTML段落
        new_html += f'\n<p style="color:var(--text-muted);line-height:2;font-size:15px;margin-bottom:20px" data-i18n="{key}">{zh[:20]}...</p>'
        
        # i18n条目
        new_entries[key] = {"zh": zh, "en": en}
    
    # 插入新段落
    new_content = content[:body_close] + new_html + '\n' + content[body_close:]
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"  ✓ {fname}: {len(zh_paragraphs)} paragraphs, keys {start_key}-{start_key+len(zh_paragraphs)-1}")
    return new_entries


def update_i18n_js(all_entries):
    """更新 i18n.js - 在最后一个条目后添加新条目"""
    fpath = os.path.join(BASE, 'i18n.js')
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    
    # 找到 var dict = { ... } 的结束位置
    # 用更安全的方式：找到文件末尾的闭合结构
    # i18n.js 的结构是 var dict = { ... }; ... 其他代码
    
    # 找到 dict 对象的最后一个属性
    # 用正则找到最后一个 "key": { ... } 模式
    for key in sorted(all_entries.keys(), reverse=True):
        entry = all_entries[key]
        zh_text = entry['zh'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        en_text = entry['en'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        
        entry_str = f',\n  "{key}": {{\n    "zh": "{zh_text}",\n    "en": "{en_text}"\n  }}'
        
        # 在 dict 的闭合 } 之前插入
        # 找到 }; 或 }; 的位置
        # 更安全的做法：找到最后一个已知键之后插入
        # 找最后一个 "news-XXX.YYY": 模式
        last_news_match = None
        for m in re.finditer(r'"news-\d+\.\d+"\s*:\s*\{', content):
            last_news_match = m
        
        if last_news_match:
            # 找到这个条目的结束 }
            search_from = last_news_match.start()
            depth = 0
            end_pos = None
            for pos in range(search_from, min(search_from + 10000, len(content))):
                if content[pos] == '{':
                    depth += 1
                elif content[pos] == '}':
                    depth -= 1
                    if depth == 0:
                        end_pos = pos + 1
                        break
            
            if end_pos:
                content = content[:end_pos] + entry_str + content[end_pos:]
            else:
                print(f"  WARNING: could not find end of entry for {key}")
        else:
            print(f"  WARNING: no existing news entries found in i18n.js")
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  ✓ i18n.js: added {len(all_entries)} entries")


def main():
    # 读取内容JSON
    content_file = os.path.join(BASE, 'news_expansion_content.json')
    with open(content_file, encoding='utf-8') as f:
        all_content = json.load(f)
    
    all_entries = {}
    
    for num_str, data in all_content.items():
        zh = data['zh']
        en = data['en']
        print(f"\nProcessing news-{num_str}...")
        entries = insert_paragraphs(num_str, zh, en)
        all_entries.update(entries)
    
    # 更新i18n.js
    print(f"\nUpdating i18n.js with {len(all_entries)} entries...")
    update_i18n_js(all_entries)
    
    # 同步到其他版本
    print("\nSyncing to language versions...")
    for num_str in all_content.keys():
        fname = f'news-{num_str}.html'
        for subdir in ['en', 'YT', 'YT/en']:
            dst = os.path.join(BASE, subdir, fname)
            if os.path.exists(dst):
                shutil.copy2(os.path.join(BASE, fname), dst)
                print(f"  ✓ {fname} → {subdir}/")
    
    # 也需要更新YT/i18n.js
    yt_i18n = os.path.join(BASE, 'YT', 'i18n.js')
    if os.path.exists(yt_i18n):
        # 同样更新YT的i18n.js
        with open(yt_i18n, encoding='utf-8') as f:
            yt_content = f.read()
        
        for key in sorted(all_entries.keys(), reverse=True):
            entry = all_entries[key]
            zh_text = entry['zh'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            en_text = entry['en'].replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
            
            entry_str = f',\n  "{key}": {{\n    "zh": "{zh_text}",\n    "en": "{en_text}"\n  }}'
            
            last_news_match = None
            for m in re.finditer(r'"news-\d+\.\d+"\s*:\s*\{', yt_content):
                last_news_match = m
            
            if last_news_match:
                search_from = last_news_match.start()
                depth = 0
                end_pos = None
                for pos in range(search_from, min(search_from + 10000, len(yt_content))):
                    if yt_content[pos] == '{':
                        depth += 1
                    elif yt_content[pos] == '}':
                        depth -= 1
                        if depth == 0:
                            end_pos = pos + 1
                            break
                if end_pos:
                    yt_content = yt_content[:end_pos] + entry_str + yt_content[end_pos:]
        
        with open(yt_i18n, 'w', encoding='utf-8') as f:
            f.write(yt_content)
        print(f"  ✓ YT/i18n.js updated")
    
    print(f"\n✅ 完成！共添加 {len(all_entries)} 个i18n条目")

if __name__ == '__main__':
    main()
