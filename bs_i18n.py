"""
用 BeautifulSoup 精确给 HTML 所有文字加 data-i18n
并处理 index.html 作为示范
"""
import re, json, os
from bs4 import BeautifulSoup

SKIP_TAGS = {'script', 'style', 'svg', 'path', 'line', 'polyline', 'circle', 'rect', 'ellipse', 'defs', 'mask', 'clippath', 'symbol'}
SKIP_CLASSES = {'yacht-price', 'stat-number', 'contact-value', 'footer-col-title', 'gold-text', 'yacht-en'}

def has_data_i18n(tag):
    return tag.has_attr('data-i18n')

def should_skip(tag):
    if tag.name in SKIP_TAGS:
        return True
    if tag.has_attr('class'):
        if set(tag['class']) & SKIP_CLASSES:
            return True
    return False

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    
    base = os.path.splitext(os.path.basename(fpath))[0]
    translations = {}
    counter = [0]
    
    # 遍历所有标签
    for tag in soup.find_all(True):  # True = all tags
        if should_skip(tag):
            continue
        if has_data_i18n(tag):
            continue
        
        # 获取直接文字内容（不含子标签的文字）
        direct_text = tag.string
        if direct_text:
            text = direct_text.strip()
            if text and len(text) > 0 and not re.match(r'^[\d\s\.\-\+\(\)\/:]+$', text):
                key = f"{base}.{counter[0]}"
                counter[0] += 1
                tag['data-i18n'] = key
                translations[key] = {'zh': text, 'en': ''}
        else:
            # 检查是否有混合内容（文字 + 子标签）
            # 例如：<h2>文字 <span>子标签</span> 更多文字</h2>
            # 这种情况需要特殊处理，暂时跳过
            pass
    
    # 写回文件
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return translations

if __name__ == '__main__':
    import sys
    files = sys.argv[1:] if len(sys.argv) > 1 else ['index.html']
    
    all_trans = {}
    for f in files:
        print(f"处理: {f}")
        trans = process_file(f)
        print(f"  添加了 {len(trans)} 个 data-i18n 属性")
        all_trans.update(trans)
    
    out = 'i18n_bs_entries.json'
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(all_trans, f, ensure_ascii=False, indent=2)
    print(f"\n✓ 完成！共 {len(all_trans)} 条")
    print(f"  翻译模板: {out}")
    print(f"  请人工翻译 en 字段后合并到 i18n.js")
