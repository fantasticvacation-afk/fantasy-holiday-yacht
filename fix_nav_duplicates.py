#!/usr/bin/env python3
"""修复重复的 <nav id="navbar"> 标签"""
import os
import re
import glob

def fix_nav_duplicates(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 删除连续重复的 <nav id="navbar"> 标签，只保留一个
    # 匹配连续的 <nav id="navbar">\n<nav id="navbar">... 模式
    original = content
    
    # 方法1：直接替换连续的重复标签
    while '<nav id="navbar">\n<nav id="navbar">' in content:
        content = content.replace('<nav id="navbar">\n<nav id="navbar">', '<nav id="navbar">')
    
    # 方法2：处理可能的空格/缩进情况
    pattern = r'(<nav id="navbar">)\s*(<nav id="navbar">)+'
    content = re.sub(pattern, r'\1', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

print('=== 修复重复的 nav 标签 ===\n')

html_files = sorted(glob.glob('*.html'))
fixed_count = 0

for f in html_files:
    if fix_nav_duplicates(f):
        fixed_count += 1
        print(f'✓ 修复: {f}')

print(f'\n完成! 共修复 {fixed_count} 个文件')
