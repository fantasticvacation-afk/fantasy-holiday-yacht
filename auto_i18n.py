"""
自动 i18n 标注脚本
功能：
  1. 解析 HTML，找出所有文字节点
  2. 自动生成 data-i18n key
  3. 将中文文字标注到元素上
  4. 输出翻译字典模板到 i18n.js

用法：python3 auto_i18n.py [文件名]
  不指定文件时，处理所有 HTML 文件（跳过已处理过的）
"""

import os, re, json, html as html_parser
from html.parser import HTMLParser

# 不需要翻译的标签 / 属性
SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'path', 'circle', 'line', 'polyline', 'rect', 'ellipse'}
SKIP_CLASSES = {'yacht-price', 'stat-number', 'contact-value', 'footer-col-title'}

class I18NExtractor(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.output_lines = []
        self.stack = []  # 当前标签栈
        self.in_skip = 0   # skip 深度
        self.translations = {}
        self.key_counter = 0
        self.current_attrs = {}
        
    def add_key(self, text):
        """为一段文字生成 key，返回 key"""
        key = f"page.{os.path.splitext(self.filename)[0]}.{self.key_counter}"
        self.key_counter += 1
        self.translations[key] = {'zh': text.strip(), 'en': ''}
        return key
    
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        self.stack.append(tag)
        
        if tag in SKIP_TAGS:
            self.in_skip += 1
        
        # 将当前标签属性存起来（供 handle_data 使用）
        self.current_attrs = attrs_dict
    
    def handle_endtag(self, tag):
        if self.stack and self.stack[-1] == tag:
            self.stack.pop()
        if tag in SKIP_TAGS and self.in_skip > 0:
            self.in_skip -= 1
    
    def handle_data(self, data):
        text = data.strip()
        if not text or len(text) < 1:
            return
        if self.in_skip > 0:
            return
        
        # 跳过纯数字、纯符号
        if re.match(r'^[\d\s\.\-\+\(\)]+$', text):
            return
        
        # 生成 key
        key = self.add_key(text)
        # 在输出中记录：文件名 + 文字 + key
        self.output_lines.append({
            'file': self.filename,
            'text': text,
            'key': key
        })

def process_file(fpath):
    """处理单个文件，返回提取出的翻译词条"""
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parser = I18NExtractor(os.path.basename(fpath))
    parser.feed(content)
    
    return parser.translations, parser.output_lines

if __name__ == '__main__':
    import sys
    
    html_files = []
    if len(sys.argv) > 1:
        html_files = [sys.argv[1]]
    else:
        html_files = [f for f in os.listdir('.') if f.endswith('.html') and f != 'footer-template.html']
    
    all_translations = {}
    all_lines = []
    
    for fname in html_files[:3]:  # 先处理前3个文件做测试
        print(f"处理: {fname}")
        trans, lines = process_file(fname)
        all_translations.update(trans)
        all_lines.extend(lines)
    
    # 输出翻译模板
    output = {'dict': all_translations, 'lines': all_lines}
    with open('i18n-template.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 提取完成: {len(all_translations)} 条文字")
    print(f"  输出到: i18n-template.json")
    print(f"\n请人工翻译 i18n-template.json 中的 'en' 字段，然后运行合并脚本")
