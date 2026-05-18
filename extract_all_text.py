"""
提取所有 HTML 文件中的中文文字，去重，输出为待翻译列表
"""
import os, re, json
from bs4 import BeautifulSoup

def extract_text(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    texts = set()
    for tag in soup.find_all(True):
        if tag.name in {'script', 'style', 'svg'}: continue
        if tag.string:
            t = tag.string.strip()
            if t and len(t) > 1 and not re.match(r'^[\d\s\.\-\+\(\)\/:]+$', t):
                texts.add(t)
    return texts

all_texts = set()
html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'footer-template.html']
print(f"扫描 {len(html_files)} 个 HTML 文件...")

for f in html_files:
    texts = extract_text(f)
    all_texts.update(texts)

print(f"去重后共 {len(all_texts)} 条唯一中文短语")

# 保存
with open('all_unique_texts.json', 'w', encoding='utf-8') as f:
    json.dump(sorted(list(all_texts)), f, ensure_ascii=False, indent=2)

print(f"✓ 已保存到 all_unique_texts.json")
print(f"  现在集中翻译这个文件，再批量回填到各页面")
