#!/usr/bin/env python3
"""
fh-yacht-site 全站自动化检查脚本
检查所有链接、文件引用、翻译完整性等
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# 配置
BASE_DIR = Path(__file__).parent
REPORT_FILE = BASE_DIR / "website-audit-report.json"

# 存储检查结果
issues = {
    "broken_links": [],
    "missing_files": [],
    "missing_translations": [],
    "duplicate_ids": [],
    "empty_pages": [],
    "missing_images": [],
    "css_issues": [],
    "js_issues": [],
}

# 统计
stats = {
    "total_html": 0,
    "total_links": 0,
    "total_images": 0,
    "total_translations": 0,
}

print("🔍 开始全站检查...")

# 1. 检查所有 HTML 文件
html_files = list(BASE_DIR.glob("*.html"))
stats["total_html"] = len(html_files)
print(f"📄 找到 {stats['total_html']} 个 HTML 文件")

# 2. 检查所有链接
print("\n🔗 检查所有链接...")
all_links = defaultdict(list)
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')
        
        # 提取所有 href 链接
        hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)
        for href in hrefs:
            if not href.startswith(('#', 'http', 'mailto:', 'tel:', 'javascript:')):
                all_links[href].append(html_file.name)
                stats["total_links"] += 1
                
                # 检查文件是否存在
                target_file = BASE_DIR / href.split('#')[0]
                if not target_file.exists():
                    issues["broken_links"].append({
                        "file": html_file.name,
                        "link": href,
                        "reason": "目标文件不存在"
                    })
    except Exception as e:
        print(f"  ❌ 读取 {html_file.name} 失败: {e}")

print(f"  ✅ 检查了 {stats['total_links']} 个内部链接")
print(f"  ⚠️  发现 {len(issues['broken_links'])} 个失效链接")

# 3. 检查图片引用
print("\n🖼️  检查图片引用...")
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')
        
        # 提取所有图片引用
        img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
        for src in img_srcs:
            if not src.startswith(('http', 'data:')):
                stats["total_images"] += 1
                img_file = BASE_DIR / src
                if not img_file.exists():
                    issues["missing_images"].append({
                        "file": html_file.name,
                        "image": src
                    })
    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 图片失败: {e}")

print(f"  ✅ 检查了 {stats['total_images']} 个图片引用")
print(f"  ⚠️  发现 {len(issues['missing_images'])} 个缺失图片")

# 4. 检查 i18n 翻译完整性
print("\n🌐 检查 i18n 翻译完整性...")
try:
    i18n_js = (BASE_DIR / "i18n.js").read_text(encoding='utf-8')
    
    # 提取字典
    dict_match = re.search(r'var dict = ({[\s\S]+?});', i18n_js)
    if dict_match:
        dict_str = dict_match.group(1)
        # 简单统计
        total_keys = len(re.findall(r'"[^"]+"\s*:', dict_str))
        stats["total_translations"] = total_keys
        print(f"  ✅ i18n.js 包含 {total_keys} 个键")
        
        # 检查是否有中文未翻译（zh == en）
        untranslated = re.findall(r'"([^"]+)":\s*{\s*"zh":\s*"([^"]+)",\s*"en":\s*"\2"', dict_str)
        if untranslated:
            print(f"  ⚠️  发现 {len(untranslated)} 个未翻译条目（zh == en）")
except Exception as e:
    print(f"  ❌ 检查 i18n.js 失败: {e}")

# 5. 检查 CSS 和 JS 文件引用
print("\n📄 检查 CSS/JS 文件引用...")
css_files = list(BASE_DIR.glob("*.css"))
js_files = list(BASE_DIR.glob("*.js"))
print(f"  ✅ 找到 {len(css_files)} 个 CSS 文件, {len(js_files)} 个 JS 文件")

for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')
        
        # 检查 CSS 引用
        css_refs = re.findall(r'href=["\']([^"\']+\.css)["\']', content)
        for css_ref in css_refs:
            if not css_ref.startswith('http'):
                css_file = BASE_DIR / css_ref
                if not css_file.exists():
                    issues["css_issues"].append({
                        "file": html_file.name,
                        "css": css_ref
                    })
        
        # 检查 JS 引用
        js_refs = re.findall(r'src=["\']([^"\']+\.js)["\']', content)
        for js_ref in js_refs:
            if not js_ref.startswith('http'):
                js_file = BASE_DIR / js_ref
                if not js_file.exists():
                    issues["js_issues"].append({
                        "file": html_file.name,
                        "js": js_ref
                    })
    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} CSS/JS 失败: {e}")

print(f"  ⚠️  发现 {len(issues['css_issues'])} 个 CSS 引用问题")
print(f"  ⚠️  发现 {len(issues['js_issues'])} 个 JS 引用问题")

# 6. 检查空白页面
print("\n📋 检查空白页面...")
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')
        
        # 检查是否只有基本结构没有内容
        body_match = re.search(r'<body[^>]*>([\s\S]+?)</body>', content)
        if body_match:
            body_content = body_match.group(1)
            # 移除 script 和 style 标签
            body_content = re.sub(r'<(script|style)[\s\S]+?</\1>', '', body_content)
            # 移除 HTML 标签
            text_content = re.sub(r'<[^>]+>', '', body_content).strip()
            
            if len(text_content) < 100:  # 内容少于100字符
                issues["empty_pages"].append({
                    "file": html_file.name,
                    "content_length": len(text_content)
                })
    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 内容失败: {e}")

print(f"  ⚠️  发现 {len(issues['empty_pages'])} 个空白页面")

# 汇总结果
print("\n" + "="*60)
print("📊 检查完成！汇总结果：")
print("="*60)
print(f"✅ HTML 文件总数: {stats['total_html']}")
print(f"✅ 内部链接总数: {stats['total_links']}")
print(f"✅ 图片引用总数: {stats['total_images']}")
print(f"✅ i18n 键总数: {stats['total_translations']}")
print()
print("⚠️  发现的问题：")
print(f"  - 失效链接: {len(issues['broken_links'])}")
print(f"  - 缺失图片: {len(issues['missing_images'])}")
print(f"  - CSS 引用问题: {len(issues['css_issues'])}")
print(f"  - JS 引用问题: {len(issues['js_issues'])}")
print(f"  - 空白页面: {len(issues['empty_pages'])}")

total_issues = sum(len(v) for v in issues.values())
print(f"\n总计问题数: {total_issues}")

# 保存报告
report = {
    "stats": stats,
    "issues": issues,
    "timestamp": "2026-05-19T10:58:00+08:00"
}

with open(REPORT_FILE, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(f"\n✅ 报告已保存: {REPORT_FILE.name}")
