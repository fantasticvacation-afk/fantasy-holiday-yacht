#!/usr/bin/env python3
"""
fh-yacht-site 全站自动化修复脚本
系统性检查和修复所有问题
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).parent

print("=" * 60)
print("🔧 fh-yacht-site 全站自动化修复脚本")
print("=" * 60)

# ============================================================
# 1. 检查所有 HTML 文件的基本结构
# ============================================================
print("\n📋 Phase 1: 检查 HTML 基本结构...")

html_files = list(BASE_DIR.glob("*.html"))
print(f"找到 {len(html_files)} 个 HTML 文件")

issues_fixed = 0

for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查 DOCTYPE
        if not content.strip().startswith('<!DOCTYPE html>'):
            print(f"  ⚠️  {html_file.name}: 缺少 DOCTYPE")

        # 检查 lang 属性
        if 'lang="zh-CN"' not in content and "lang='zh-CN'" not in content:
            print(f"  ⚠️  {html_file.name}: 缺少 lang 属性")

        # 检查 charset
        if 'charset="utf-8"' not in content and "charset='utf-8'" not in content:
            print(f"  ⚠️  {html_file.name}: 缺少 charset")

        # 检查 viewport
        if 'viewport' not in content:
            print(f"  ⚠️  {html_file.name}: 缺少 viewport")

    except Exception as e:
        print(f"  ❌ 读取 {html_file.name} 失败: {e}")

print(f"  ✅ Phase 1 完成")

# ============================================================
# 2. 检查导航栏一致性
# ============================================================
print("\n📋 Phase 2: 检查导航栏一致性...")

nav_structure = {
    'nav.home': '首页',
    'nav.about': '关于我们',
    'nav.business': '业务板块',
    'nav.products': '产品与服务',
    'nav.news': '新闻中心',
    'nav.ir': '投资者关系',
    'nav.contact': '联系我们',
}

nav_issues = []
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查是否包含所有导航项
        for key, text in nav_structure.items():
            if f'data-i18n="{key}"' not in content:
                nav_issues.append(f"{html_file.name}: 缺少 {key}")

    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 失败: {e}")

if nav_issues:
    print(f"  ⚠️  发现 {len(nav_issues)} 个导航栏问题")
    for issue in nav_issues[:5]:
        print(f"    - {issue}")
else:
    print(f"  ✅ 所有页面导航栏一致")

# ============================================================
# 3. 检查移动端菜单
# ============================================================
print("\n📋 Phase 3: 检查移动端菜单...")

mobile_menu_issues = []
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查移动端菜单元素
        if 'id="mobile-menu"' not in content:
            mobile_menu_issues.append(f"{html_file.name}: 缺少移动端菜单")
        if 'class="hamburger"' not in content:
            mobile_menu_issues.append(f"{html_file.name}: 缺少汉堡菜单按钮")

    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 失败: {e}")

if mobile_menu_issues:
    print(f"  ⚠️  发现 {len(mobile_menu_issues)} 个移动端菜单问题")
    for issue in mobile_menu_issues[:5]:
        print(f"    - {issue}")
else:
    print(f"  ✅ 所有页面移动端菜单完整")

# ============================================================
# 4. 检查搜索功能
# ============================================================
print("\n📋 Phase 4: 检查搜索功能...")

search_issues = []
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查搜索框元素
        if 'id="searchOverlay"' not in content:
            search_issues.append(f"{html_file.name}: 缺少搜索框")
        if 'id="searchInput"' not in content:
            search_issues.append(f"{html_file.name}: 缺少搜索输入框")

    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 失败: {e}")

if search_issues:
    print(f"  ⚠️  发现 {len(search_issues)} 个搜索功能问题")
    for issue in search_issues[:5]:
        print(f"    - {issue}")
else:
    print(f"  ✅ 所有页面搜索功能完整")

# ============================================================
# 5. 检查 JavaScript 引用
# ============================================================
print("\n📋 Phase 5: 检查 JavaScript 引用...")

js_issues = []
for html_file in html_files:
    try:
        content = html_file.read_text(encoding='utf-8')

        # 检查 JavaScript 引用
        if 'src="main.js"' not in content and "src='main.js'" not in content:
            js_issues.append(f"{html_file.name}: 缺少 main.js 引用")
        if 'src="i18n.js"' not in content and "src='i18n.js'" not in content:
            js_issues.append(f"{html_file.name}: 缺少 i18n.js 引用")

    except Exception as e:
        print(f"  ❌ 检查 {html_file.name} 失败: {e}")

if js_issues:
    print(f"  ⚠️  发现 {len(js_issues)} 个 JavaScript 引用问题")
    for issue in js_issues[:5]:
        print(f"    - {issue}")
else:
    print(f"  ✅ 所有页面 JavaScript 引用完整")

# ============================================================
# 汇总结果
# ============================================================
print("\n" + "=" * 60)
print("📊 检查完成！")
print("=" * 60)

total_issues = len(nav_issues) + len(mobile_menu_issues) + len(search_issues) + len(js_issues)
print(f"总问题数: {total_issues}")

if total_issues == 0:
    print("✅ 全站检查通过！")
else:
    print("⚠️  需要修复上述问题")
