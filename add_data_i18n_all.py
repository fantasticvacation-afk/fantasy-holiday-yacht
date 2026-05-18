#!/usr/bin/env python3
"""
add_data_i18n_all.py
给所有 HTML 文件添加 data-i18n 属性（框架先行，翻译后补）
"""

from bs4 import BeautifulSoup
import os
import re

HTML_DIR = '/Users/hs/.qclaw/workspace/fh-yacht-site'

def add_i18n_to_file(html_file):
    """给单个 HTML 文件添加 data-i18n 属性"""
    filepath = os.path.join(HTML_DIR, html_file)
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 获取文件前缀（如 index.html -> index）
    prefix = html_file.replace('.html', '')
    
    count = 0
    for i, elem in enumerate(soup.find_all(string=True)):
        text = elem.strip()
        if not text or len(text) < 2:
            continue
        # 跳过脚本、样式、特殊内容
        if elem.parent.name in ['script', 'style', 'noscript']:
            continue
        if any(c in text for c in ['{', '}', '@', '//', 'http', '<', '>']):
            continue
        
        # 添加 data-i18n 属性
        key = f"{prefix}.{i}"
        if elem.parent.get('data-i18n'):
            continue  # 已有属性，跳过
        elem.parent['data-i18n'] = key
        count += 1
    
    # 保存
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    
    return count

# 主程序
if __name__ == '__main__':
    html_files = [f for f in os.listdir(HTML_DIR) if f.endswith('.html')]
    total = 0
    
    print(f"开始处理 {len(html_files)} 个 HTML 文件...")
    
    for html_file in html_files:
        try:
            count = add_i18n_to_file(html_file)
            total += count
            print(f"  ✓ {html_file}: 添加 {count} 个 data-i18n 属性")
        except Exception as e:
            print(f"  ✗ {html_file}: 错误 - {e}")
    
    print(f"\n完成！共添加 {total} 个 data-i18n 属性到 {len(html_files)} 个文件")
